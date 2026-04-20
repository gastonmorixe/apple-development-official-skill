#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import plistlib
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

SKILL_NAME = "apple-development-official"
ROOT = Path(__file__).resolve().parent.parent
REFERENCES = ROOT / "references"
MAINTENANCE = ROOT / "maintenance"
SCRIPTS = ROOT / "scripts"
HOME = Path.home()
CODEX_HOME = Path(os.environ.get("CODEX_HOME", HOME / ".codex")).expanduser()
ROOT_ANCHOR = Path(HOME.anchor)

SELECTED_DEVELOPER_DIR = Path(
    subprocess.run(
        ["xcode-select", "-p"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
).resolve()
if SELECTED_DEVELOPER_DIR.name != "Developer" or SELECTED_DEVELOPER_DIR.parent.name != "Contents":
    raise RuntimeError(
        "xcode-select -p must point at an Xcode app Developer directory, "
        f"got: {SELECTED_DEVELOPER_DIR}"
    )

XCODE_APP = SELECTED_DEVELOPER_DIR.parent.parent
XCODE_RESOURCES = XCODE_APP / "Contents" / "PlugIns" / "IDEIntelligenceChat.framework" / "Versions" / "A" / "Resources"
XCODE_ADDITIONAL = XCODE_RESOURCES / "AdditionalDocumentation"
XCODE_ONBOARDING_CONTENTS = XCODE_RESOURCES / "OnboardingIntelligenceXcode.bundle" / "Contents"
XCODE_ONBOARDING_RESOURCES = XCODE_ONBOARDING_CONTENTS / "Resources"

SYSTEM_INTELLIGENCE = ROOT_ANCHOR / "System" / "Library" / "OnBoardingBundles" / "com.apple.onboarding.intelligenceengine.bundle" / "Contents" / "Resources" / "Intelligence.plist"
SYSTEM_FOUNDATION_MODELS = ROOT_ANCHOR / "System" / "Library" / "LifecyclePolicy" / "DomainAttributes" / "com.apple.foundationmodels.plist"
SYSTEM_TASKED_CONFIG = ROOT_ANCHOR / "Library" / "CoreAnalytics" / "taskedConfig.json"

LOCAL_BASE = HOME / "Library" / "Developer" / "Xcode" / "CodingAssistant"
XCODE_APP_INFO = plistlib.loads((XCODE_APP / "Contents" / "Info.plist").read_bytes())
XCODE_VERSION = XCODE_APP_INFO.get("CFBundleShortVersionString") or XCODE_APP_INFO.get("CFBundleVersion") or XCODE_APP.name
IDE_INTELLIGENCE_INFO = plistlib.loads((XCODE_RESOURCES / "Info.plist").read_bytes())
IDE_INTELLIGENCE_VERSION = IDE_INTELLIGENCE_INFO.get("CFBundleVersion", "unknown")
IDE_INTELLIGENCE_SOURCE_INFO = plistlib.loads((XCODE_RESOURCES / "version.plist").read_bytes())
IDE_INTELLIGENCE_SOURCE_VERSION = IDE_INTELLIGENCE_SOURCE_INFO.get("SourceVersion", "unknown")


def xr(name: str) -> Path:
    return XCODE_RESOURCES / name


def xa(name: str) -> Path:
    return XCODE_ADDITIONAL / name


def xo(*parts: str) -> Path:
    return XCODE_ONBOARDING_CONTENTS.joinpath(*parts)


def latest_detected_version(provider: str) -> str:
    provider_root = LOCAL_BASE / "Agents" / provider
    if not provider_root.exists():
        return "not-detected"

    def version_key(value: str) -> tuple:
        parts: list[object] = []
        for part in re.split(r"([0-9]+)", value):
            if not part:
                continue
            parts.append(int(part) if part.isdigit() else part)
        return tuple(parts)

    versions = sorted((path.name for path in provider_root.iterdir() if path.is_dir()), key=version_key)
    return versions[-1] if versions else "not-detected"


CLAUDE_VERSION = latest_detected_version("claude")
CODEX_AGENT_VERSION = latest_detected_version("codex")


SPECIAL_PATH_LABELS = {
    SYSTEM_INTELLIGENCE: "SYSTEM_INTELLIGENCE_PLIST",
    SYSTEM_FOUNDATION_MODELS: "SYSTEM_FOUNDATION_MODELS_PLIST",
    SYSTEM_TASKED_CONFIG: "SYSTEM_TASKED_CONFIG_JSON",
}


def symbolic_path(path: Path) -> str:
    for candidate, label in SPECIAL_PATH_LABELS.items():
        if path == candidate:
            return label

    for root, label in [
        (REFERENCES, "SKILL_REFERENCES"),
        (MAINTENANCE, "SKILL_MAINTENANCE"),
        (SCRIPTS, "SKILL_SCRIPTS"),
        (ROOT, "SKILL_ROOT"),
        (XCODE_ONBOARDING_RESOURCES, "XCODE_ONBOARDING_RESOURCES"),
        (XCODE_ONBOARDING_CONTENTS, "XCODE_ONBOARDING_CONTENTS"),
        (XCODE_ADDITIONAL, "XCODE_ADDITIONAL_DOCUMENTATION"),
        (XCODE_RESOURCES, "XCODE_RESOURCES"),
        (XCODE_APP, "SELECTED_XCODE_APP"),
        (SELECTED_DEVELOPER_DIR, "SELECTED_XCODE_DEVELOPER_DIR"),
        (LOCAL_BASE, "LOCAL_XCODE_CODINGASSISTANT_ROOT"),
        (CODEX_HOME, "CODEX_HOME"),
        (HOME, "~"),
    ]:
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if relative == Path("."):
            return label
        return f"{label}/{relative.as_posix()}"

    return path.name


def shell_ref(path: Path) -> str:
    for candidate, label in SPECIAL_PATH_LABELS.items():
        if path == candidate:
            return f'"${label}"'

    for root, label in [
        (XCODE_ADDITIONAL, "XCODE_ADDITIONAL_DOCUMENTATION"),
        (XCODE_RESOURCES, "XCODE_RESOURCES"),
        (LOCAL_BASE, "LOCAL_XCODE_CODINGASSISTANT_ROOT"),
    ]:
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if relative == Path("."):
            return f'"${label}"'
        return f'"${label}/{relative.as_posix()}"'

    return f'"{path.name}"'


@dataclass(frozen=True)
class RuntimeDocSpec:
    filename: str
    title: str
    purpose: str
    when_to_use: list[str]
    apply_rules: list[str]
    source_paths: list[Path]
    doc_kind: str


@dataclass(frozen=True)
class SourceRecord:
    path: Path
    source_type: str
    provenance_tier: str
    handling_mode: str
    output_path: Path | None
    discovery_command: str
    version_context: str


PROMPT_DOCS: list[RuntimeDocSpec] = [
    RuntimeDocSpec(
        filename="prompting-core-rules.md",
        title="Prompting Core Rules",
        purpose="Base Apple/Xcode steering for how an agent should reason, search, validate, and format Apple-platform coding work.",
        when_to_use=[
            "General Swift, SwiftUI, UIKit, AppKit, or WidgetKit coding tasks.",
            "Any task where Xcode's built-in agent policy matters more than generic coding advice.",
            "Requests that touch new Apple topics such as Liquid Glass or FoundationModels.",
        ],
        apply_rules=[
            "Prefer Swift-first, Apple-platform-first solutions.",
            "Use current Apple documentation when a framework or design system may be newer than the model's training cutoff.",
            "Prefer Swift Concurrency and Swift Testing over older Combine-first or XCTest-only defaults when the source guidance points that way.",
            "Preserve Apple platform naming and modern SwiftUI conventions such as `@State private var`.",
        ],
        source_paths=[
            xr("AgentSystemPromptAddition.idechatprompttemplate"),
            xr("BasicSystemPrompt.idechatprompttemplate"),
            xr("ReasoningSystemPrompt.idechatprompttemplate"),
            xr("TextEditorToolSystemPrompt.idechatprompttemplate"),
            xr("ToolAssistedBasicSystemPrompt.idechatprompttemplate"),
            xr("ToolAssistedReasoningSystemPrompt.idechatprompttemplate"),
            xr("VariantASystemPrompt.idechatprompttemplate"),
            xr("VariantBSystemPrompt.idechatprompttemplate"),
        ],
        doc_kind="prompt",
    ),
    RuntimeDocSpec(
        filename="prompting-query-response-and-titles.md",
        title="Prompting Query, Response, and Titles",
        purpose="How Xcode shapes ordinary chat responses, short and detailed query behavior, naming, and lightweight explanation flows.",
        when_to_use=[
            "Ordinary coding questions and conversational responses.",
            "Title generation and response-shaping behavior.",
            "Situations where Xcode wants concise or tool-aware query handling.",
        ],
        apply_rules=[
            "Keep answers direct and task-focused.",
            "Use the detailed guideline variant when the request needs more structure or explicit tool behavior.",
            "Treat titles, snippets, and interface-oriented prompt fragments as response-shaping helpers rather than separate workflows.",
        ],
        source_paths=[
            xr("ChatTitleResolver.idechatprompttemplate"),
            xr("InQueryDetailedGuidelines.idechatprompttemplate"),
            xr("InQueryShortGuidelines.idechatprompttemplate"),
            xr("Interfaces.idechatprompttemplate"),
            xr("Query.idechatprompttemplate"),
            xr("Snippets.idechatprompttemplate"),
            xr("ToolAssistedInQueryDetailedGuidelines.idechatprompttemplate"),
            xr("ToolAssistedInQueryShortGuidelines.idechatprompttemplate"),
        ],
        doc_kind="prompt",
    ),
    RuntimeDocSpec(
        filename="prompting-code-editing-documentation-and-apply.md",
        title="Prompting Code Editing, Documentation, and Apply",
        purpose="How Xcode steers code edits, integration, explanation, documentation updates, and fast-apply workflows.",
        when_to_use=[
            "Code modification requests.",
            "Documentation comment generation or explanation tasks.",
            "Cases where the agent should integrate edits rather than produce stand-alone code.",
        ],
        apply_rules=[
            "Keep edits tightly scoped to the requested change.",
            "Preserve surrounding project structure unless the source guidance clearly calls for refactoring.",
            "Separate user intent from code instructions when an integration prompt does that explicitly.",
            "Use fast-apply style behavior only when a targeted patch is clearly appropriate.",
        ],
        source_paths=[
            xr("CodingToolTemplateDocument.idechatprompttemplate"),
            xr("CodingToolTemplateExplain.idechatprompttemplate"),
            xr("FastApplyIntegratorSystemPrompt.idechatprompttemplate"),
            xr("FastApplyIntegratorUserPrompt.idechatprompttemplate"),
            xr("GenerateDocumentation.idechatprompttemplate"),
            xr("IntegratorSystemPrompt.idechatprompttemplate"),
            xr("IntegratorUserPrompt.idechatprompttemplate"),
            xr("NewCodeIntegratorSystemPrompt.idechatprompttemplate"),
            xr("NewCodeIntegratorUserPrompt.idechatprompttemplate"),
        ],
        doc_kind="prompt",
    ),
    RuntimeDocSpec(
        filename="prompting-preview-and-playground-generation.md",
        title="Prompting Preview and Playground Generation",
        purpose="How Xcode asks for `#Preview` output, preview wrapping rules, and playground scaffolding.",
        when_to_use=[
            "Preview generation or preview repair tasks.",
            "SwiftUI examples that need `#Preview` blocks.",
            "Playground generation or minimal runnable demonstration code.",
        ],
        apply_rules=[
            "Use `#Preview` for new SwiftUI previews.",
            "Wrap previews in `NavigationStack` or `List` only when the source view implies that context.",
            "Return code-only output when the source prompt explicitly requires it.",
            "Prefer small runnable examples for playground-style generation.",
        ],
        source_paths=[
            xr("CodingToolTemplateGeneratePlayground.idechatprompttemplate"),
            xr("CodingToolTemplateGeneratePreview.idechatprompttemplate"),
            xr("GeneratePlayground.idechatprompttemplate"),
            xr("GeneratePreview.idechatprompttemplate"),
        ],
        doc_kind="prompt",
    ),
    RuntimeDocSpec(
        filename="prompting-context-search-and-selection.md",
        title="Prompting Context, Search, and Selection",
        purpose="How Xcode assembles current file context, search results, issues, selections, and supporting files around a request.",
        when_to_use=[
            "Requests that depend on current file or current selection context.",
            "Tasks that need issue lists, search results, or additional files.",
            "Situations where the agent should understand what Xcode provides before answering.",
        ],
        apply_rules=[
            "Respect the difference between full-file, abbreviated-file, filename-only, and selection-only context.",
            "Treat issues and search results as structured context inputs, not narrative prose.",
            "Use no-selection and original-file variants to understand fallback and comparison behavior.",
        ],
        source_paths=[
            xr("AdditionalFiles.idechatprompttemplate"),
            xr("AgentAdditionalContext.idechatprompttemplate"),
            xr("ContextItems.idechatprompttemplate"),
            xr("CurrentFile.idechatprompttemplate"),
            xr("CurrentFileAbbreviated.idechatprompttemplate"),
            xr("CurrentFileName.idechatprompttemplate"),
            xr("CurrentSelection.idechatprompttemplate"),
            xr("Issues.idechatprompttemplate"),
            xr("NewKnowledge.idechatprompttemplate"),
            xr("NoSelection.idechatprompttemplate"),
            xr("OriginalFile.idechatprompttemplate"),
            xr("SearchResults.idechatprompttemplate"),
        ],
        doc_kind="prompt",
    ),
    RuntimeDocSpec(
        filename="prompting-planner-executor-and-retrieval.md",
        title="Prompting Planner, Executor, and Retrieval",
        purpose="Planner/executor orchestration plus the retrieval-style prompt fragments Xcode uses for search and infill support.",
        when_to_use=[
            "Multi-step or agentic Apple-platform tasks.",
            "Questions about how Xcode decides between planning, retrieval, and execution.",
            "Requests that benefit from understanding vector search or retrieval expansion behavior.",
        ],
        apply_rules=[
            "Separate planning from execution when the prompt family does so.",
            "Use retrieval expansion only as a support mechanism for context discovery or infill.",
            "Treat the planner/executor prompts as workflow steering, not as product API documentation.",
        ],
        source_paths=[
            xr("InstructionEmbeddingsQueryExpansion.idechatprompttemplate"),
            xr("LocalInfillEmbeddingsQueryExpansion.idechatprompttemplate"),
            xr("PlannerExecutorStyleNoClassify.idechatprompttemplate"),
            xr("PlannerExecutorStylePlannerSystemPrompt-gpt_5.idechatprompttemplate"),
            xr("PlannerExecutorStylePlannerSystemPrompt.idechatprompttemplate"),
        ],
        doc_kind="prompt",
    ),
]

GUIDE_DOCS: list[RuntimeDocSpec] = [
    RuntimeDocSpec(
        filename="platform-swiftui-liquid-glass-and-modern-ui.md",
        title="Platform SwiftUI, Liquid Glass, and Modern UI",
        purpose="Apple's SwiftUI-centered guidance for Liquid Glass plus current SwiftUI toolbar, styled text, WebKit, and AlarmKit integration patterns.",
        when_to_use=[
            "SwiftUI UI work, especially when Liquid Glass is in scope.",
            "Modern SwiftUI feature adoption for toolbars, styled text editing, WebKit, or AlarmKit.",
            "Any SwiftUI request where newer Apple APIs may have replaced older patterns.",
        ],
        apply_rules=[
            "Reach for documented SwiftUI-native APIs before compatibility-era workarounds.",
            "Treat Liquid Glass as a first-class design system, not a one-off visual effect.",
            "Preserve API names, modifiers, and capability boundaries exactly as Apple describes them.",
        ],
        source_paths=[
            xa("SwiftUI-AlarmKit-Integration.md"),
            xa("SwiftUI-Implementing-Liquid-Glass-Design.md"),
            xa("SwiftUI-New-Toolbar-Features.md"),
            xa("SwiftUI-Styled-Text-Editing.md"),
            xa("SwiftUI-WebKit-Integration.md"),
        ],
        doc_kind="guide",
    ),
    RuntimeDocSpec(
        filename="platform-cross-framework-liquid-glass.md",
        title="Platform Cross-Framework Liquid Glass",
        purpose="How Apple frames Liquid Glass across UIKit, AppKit, and WidgetKit rather than only in SwiftUI.",
        when_to_use=[
            "Liquid Glass adoption outside SwiftUI.",
            "Cross-framework Apple UI work involving UIKit, AppKit, or WidgetKit.",
            "Cases where the same design system needs to be applied in multiple Apple UI stacks.",
        ],
        apply_rules=[
            "Keep the framework boundary clear: UIKit, AppKit, and WidgetKit each expose their own Liquid Glass surface area.",
            "Reuse the design-system intent across frameworks without assuming API parity.",
        ],
        source_paths=[
            xa("AppKit-Implementing-Liquid-Glass-Design.md"),
            xa("UIKit-Implementing-Liquid-Glass-Design.md"),
            xa("WidgetKit-Implementing-Liquid-Glass-Design.md"),
        ],
        doc_kind="guide",
    ),
    RuntimeDocSpec(
        filename="platform-foundation-models-intents-and-intelligence.md",
        title="Platform FoundationModels, Intents, and Intelligence",
        purpose="Apple guidance around FoundationModels, AppIntents, Visual Intelligence, and related system-facing intelligence features.",
        when_to_use=[
            "On-device model integration with FoundationModels.",
            "AppIntents, shortcuts-style behavior, or system intelligence features.",
            "Visual Intelligence or Assistive Access related work.",
        ],
        apply_rules=[
            "Treat FoundationModels as its own modern Apple framework with structured generation support.",
            "Keep AppIntents and Visual Intelligence aligned with Apple platform affordances instead of generic LLM patterns.",
            "Preserve accessibility-facing constraints when Assistive Access guidance is relevant.",
        ],
        source_paths=[
            xa("AppIntents-Updates.md"),
            xa("FoundationModels-Using-on-device-LLM-in-your-app.md"),
            xa("Implementing-Assistive-Access-in-iOS.md"),
            xa("Implementing-Visual-Intelligence-in-iOS.md"),
        ],
        doc_kind="guide",
    ),
    RuntimeDocSpec(
        filename="platform-swift-language-concurrency-and-data.md",
        title="Platform Swift Language, Concurrency, and Data",
        purpose="Apple's current guidance around Swift Concurrency, InlineArray/Span, SwiftData inheritance, and Foundation attributed strings.",
        when_to_use=[
            "Swift language feature adoption.",
            "Concurrency, data modeling, or Foundation text work.",
            "Requests that touch current Swift standard library or data-layer changes.",
        ],
        apply_rules=[
            "Prefer the language and data patterns Apple is actively documenting now.",
            "Keep Swift Concurrency guidance ahead of legacy async models.",
            "Preserve data-model and text-system terminology exactly where Apple has defined it.",
        ],
        source_paths=[
            xa("Foundation-AttributedString-Updates.md"),
            xa("Swift-Concurrency-Updates.md"),
            xa("Swift-InlineArray-Span.md"),
            xa("SwiftData-Class-Inheritance.md"),
        ],
        doc_kind="guide",
    ),
    RuntimeDocSpec(
        filename="platform-maps-storekit-charts-and-widgets.md",
        title="Platform Maps, StoreKit, Charts, and Widgets",
        purpose="Apple reference material for StoreKit, MapKit, Charts, and widget-related platform updates bundled with Xcode Intelligence.",
        when_to_use=[
            "Commerce, maps, charting, or widget work.",
            "visionOS widget questions.",
            "Requests that need newer Apple platform feature guidance outside the core UI and intelligence stacks.",
        ],
        apply_rules=[
            "Load the precise platform update doc rather than guessing from older framework knowledge.",
            "Keep the framework boundary clear across StoreKit, MapKit, Charts, and widget-specific APIs.",
        ],
        source_paths=[
            xa("MapKit-GeoToolbox-PlaceDescriptors.md"),
            xa("StoreKit-Updates.md"),
            xa("Swift-Charts-3D-Visualization.md"),
            xa("Widgets-for-visionOS.md"),
        ],
        doc_kind="guide",
    ),
]

MODELS_DOC = "assistant-models-versions-and-pairings.md"
TOOLS_DOC = "assistant-tools-surfaces-and-actions.md"
ONBOARDING_DOC = "assistant-onboarding-and-privacy.md"
SYSTEM_DOC = "system-intelligence-context-and-telemetry.md"

METADATA_SOURCE_MAP: dict[str, list[Path]] = {
    MODELS_DOC: [
        xr("AgentVersions.plist"),
        xr("ApprovedIntegrationModelPairings.plist"),
        xr("Info.plist"),
        xr("version.plist"),
    ],
    TOOLS_DOC: [
        xr("IDEIntelligenceChat.xcplugindata"),
    ],
    ONBOARDING_DOC: [
        xo("Info.plist"),
        xo("version.plist"),
        xo("Resources", "IntelligenceInXcode.plist"),
        xo("Resources", "en.lproj", "IntelligenceInXcode.strings"),
    ],
    SYSTEM_DOC: [
        SYSTEM_INTELLIGENCE,
        SYSTEM_FOUNDATION_MODELS,
        SYSTEM_TASKED_CONFIG,
    ],
}

def local_audit_sources() -> list[Path]:
    sources: list[Path] = []
    for provider in ("claude", "codex"):
        provider_root = LOCAL_BASE / "Agents" / provider
        if provider_root.exists():
            for version_dir in sorted(path for path in provider_root.iterdir() if path.is_dir()):
                for name in ("Info.plist", provider):
                    candidate = version_dir / name
                    if candidate.exists():
                        sources.append(candidate)

    for relative in [
        Path("codex/.personality_migration"),
        Path("codex/config.toml"),
        Path("codex/rules/xcode.rules"),
        Path("codex/skills/.system/.codex-system-skills.marker"),
        Path("codex/skills/.system/skill-creator/SKILL.md"),
        Path("codex/skills/.system/skill-creator/agents/openai.yaml"),
        Path("codex/skills/.system/skill-creator/references/openai_yaml.md"),
        Path("codex/skills/.system/skill-installer/SKILL.md"),
        Path("codex/skills/.system/skill-installer/agents/openai.yaml"),
    ]:
        candidate = LOCAL_BASE / relative
        if candidate.exists():
            sources.append(candidate)

    return sources

PROMPT_SIGNAL_RULES = [
    ("documentationsearch", "Use Apple documentation search when the topic may be newer than cached knowledge."),
    ("buildproject", "Validate substantial changes with Xcode build tooling when compile confidence matters."),
    ("xcoderefreshcodeissuesinfile", "Prefer fast file diagnostics before a full build when the source prompt points at that workflow."),
    ("executesnippet", "Use lightweight snippet execution when the source prompt expects experimentation instead of a full build."),
    ("liquid glass", "Treat Liquid Glass as a new Apple design system and check current guidance instead of relying on older UI instincts."),
    ("foundationmodels", "Treat FoundationModels as new Apple framework surface area and check current documentation."),
    ("swiftui", "Assume SwiftUI patterns may have evolved and favor current Apple-native approaches."),
    ("#preview", "Use `#Preview` for modern SwiftUI preview generation when the template is preview-related."),
    ("navigationstack", "Add `NavigationStack` only when the source view or task implies navigation context."),
    ("list", "Add `List` only when the source view or task implies list or row context."),
    ("async and await", "Prefer Swift Concurrency over legacy async patterns when the template says so."),
    ("combine", "Avoid falling back to `Combine` when the guidance favors async/await."),
    ("@state private var", "Use `@State private var` for SwiftUI state when the template calls for it."),
    ("testing framework", "Prefer the modern `Testing` framework for unit tests."),
    ("xcuiautomation", "Use `XCUIAutomation` for UI test guidance when the prompt mentions it."),
    ("only return the code", "Return code only when the prompt explicitly requires a code-only answer."),
    ("triple-tick", "Wrap output in fenced markdown only when the prompt explicitly requires that formatting."),
]

GUIDE_USE_CASES = {
    "SwiftUI-Implementing-Liquid-Glass-Design.md": "Use this when implementing Liquid Glass directly in SwiftUI.",
    "SwiftUI-New-Toolbar-Features.md": "Use this when adopting newer SwiftUI toolbar capabilities.",
    "SwiftUI-Styled-Text-Editing.md": "Use this when working on richer text editing in SwiftUI.",
    "SwiftUI-WebKit-Integration.md": "Use this when bridging WebKit into SwiftUI in the current Apple-supported way.",
    "SwiftUI-AlarmKit-Integration.md": "Use this when a SwiftUI experience needs current AlarmKit integration guidance.",
    "UIKit-Implementing-Liquid-Glass-Design.md": "Use this when implementing Liquid Glass in UIKit instead of SwiftUI.",
    "AppKit-Implementing-Liquid-Glass-Design.md": "Use this when implementing Liquid Glass in AppKit on macOS.",
    "WidgetKit-Implementing-Liquid-Glass-Design.md": "Use this when applying Liquid Glass concepts in WidgetKit.",
    "FoundationModels-Using-on-device-LLM-in-your-app.md": "Use this when integrating on-device model workflows with FoundationModels.",
    "AppIntents-Updates.md": "Use this when current AppIntents capabilities matter.",
    "Implementing-Visual-Intelligence-in-iOS.md": "Use this when implementing Visual Intelligence features in iOS.",
    "Implementing-Assistive-Access-in-iOS.md": "Use this when Assistive Access constraints affect the implementation.",
    "Swift-Concurrency-Updates.md": "Use this when updating concurrency patterns to current Swift guidance.",
    "Swift-InlineArray-Span.md": "Use this when new Swift standard library collection/storage features are in scope.",
    "SwiftData-Class-Inheritance.md": "Use this when SwiftData inheritance behavior matters.",
    "Foundation-AttributedString-Updates.md": "Use this when current AttributedString behavior or APIs matter.",
    "StoreKit-Updates.md": "Use this when StoreKit behavior or new StoreKit APIs matter.",
    "MapKit-GeoToolbox-PlaceDescriptors.md": "Use this when current MapKit place descriptor guidance matters.",
    "Swift-Charts-3D-Visualization.md": "Use this when building or updating 3D Charts experiences.",
    "Widgets-for-visionOS.md": "Use this when designing or implementing widgets for visionOS.",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def short_list(items: list[str], limit: int = 8) -> str:
    if not items:
        return ""
    if len(items) <= limit:
        return ", ".join(items)
    return ", ".join(items[:limit]) + f", and {len(items) - limit} more"


def dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.add(item)
            output.append(item)
    return output


def clean_title(name: str) -> str:
    stem = name
    for suffix in [".idechatprompttemplate", ".plist", ".strings", ".xcplugindata", ".md", ".json", ".yaml", ".toml"]:
        stem = stem.replace(suffix, "")
    stem = stem.replace(".", " ")
    stem = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", stem)
    stem = stem.replace("-", " ")
    stem = stem.replace("_", " ")
    title = " ".join(stem.split()).title()
    replacements = {
        "Swift Ui": "SwiftUI",
        "App Kit": "AppKit",
        "Widget Kit": "WidgetKit",
        "Web Kit": "WebKit",
        "Foundationmodels": "FoundationModels",
        "Appintents": "AppIntents",
        "Ll M": "LLM",
        "Xcode": "Xcode",
        "Ide": "IDE",
        "Mcp": "MCP",
        "Gpt 5": "GPT 5",
    }
    for old, new in replacements.items():
        title = title.replace(old, new)
    return title


def extract_headings(text: str) -> list[str]:
    headings = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.append(stripped.lstrip("#").strip())
    return dedupe(headings)


def extract_code_terms(text: str, limit: int = 14) -> list[str]:
    terms: list[str] = []
    ignored_exact = {
        "Provide",
        "Respond",
        "Don",
        "File",
        "FilePath",
        "Lines",
        "StartLine",
        "EndLine",
        "SelectedCode",
        ".g",
        ".name",
        ".com",
        ".org",
        ".apple",
        ".shared",
        ".plist",
    }
    terms.extend(re.findall(r"`([^`\n]{2,80})`", text))
    terms.extend(re.findall(r"@[A-Za-z_][A-Za-z0-9_]+", text))
    terms.extend(re.findall(r"\.[A-Za-z_][A-Za-z0-9_]*(?:\([^)\n]{0,50}\))?", text))
    terms.extend(re.findall(r"\b[A-Z][A-Za-z0-9_]+(?:\.[A-Za-z_][A-Za-z0-9_]+)?\b", text))
    cleaned: list[str] = []
    for item in terms:
        candidate = " ".join(item.strip().split())
        if len(candidate) < 2 or len(candidate) > 80:
            continue
        if "{" in candidate or "}" in candidate:
            continue
        if candidate.startswith("http"):
            continue
        if candidate in ignored_exact:
            continue
        if candidate.lower() in {"swiftui", "uikit", "appkit", "widgetkit", "foundationmodels", "appintents"}:
            cleaned.append(candidate)
            continue
        if candidate.islower() and "." not in candidate and "@" not in candidate:
            continue
        cleaned.append(candidate)
    return dedupe(cleaned)[:limit]


def prompt_topic(name: str) -> str:
    if "Preview" in name:
        return "preview generation"
    if "Playground" in name:
        return "playground generation"
    if "Integrator" in name or "FastApply" in name:
        return "code integration and targeted editing"
    if "CurrentFile" in name or "Selection" in name or "Issues" in name or "SearchResults" in name or "AdditionalFiles" in name:
        return "context assembly around the user's current workspace state"
    if "PlannerExecutor" in name:
        return "planner/executor orchestration"
    if "Query" in name or "Title" in name or "Snippets" in name or "Interfaces" in name:
        return "query handling and response shaping"
    if "Embeddings" in name:
        return "retrieval and search expansion"
    if "Document" in name or "Explain" in name:
        return "documentation or explanation output"
    return "base system prompting and reasoning"


def prompt_source_bullets(path: Path) -> list[str]:
    text = read_text(path)
    lower = text.lower()
    bullets = [f"Helps with {prompt_topic(path.name)}."]
    matched = []
    for needle, sentence in PROMPT_SIGNAL_RULES:
        if needle in lower:
            matched.append(sentence)
    if matched:
        bullets.append("Carry forward: " + "; ".join(dedupe(matched)[:5]) + ".")
    headings = extract_headings(text)
    if headings:
        bullets.append("Source anchors: " + short_list(headings, 6) + ".")
    terms = extract_code_terms(text, 10)
    if terms:
        bullets.append("Important terms present: " + short_list(terms, 10) + ".")
    return bullets[:4]


def guide_source_bullets(path: Path) -> list[str]:
    text = read_text(path)
    bullets = [GUIDE_USE_CASES.get(path.name, f"Use this when the topic in `{path.name}` is directly relevant.")]
    headings = extract_headings(text)
    if headings:
        bullets.append("Apple topics covered: " + short_list(headings, 8) + ".")
    terms = extract_code_terms(text, 14)
    if terms:
        bullets.append("APIs and patterns present: " + short_list(terms, 12) + ".")
    return bullets


def frontmatter(title: str) -> list[str]:
    return ["---", f"title: {title}", "---", ""]


def render_runtime_doc(spec: RuntimeDocSpec) -> str:
    lines = frontmatter(spec.title)
    lines.extend(
        [
            f"# {spec.title}",
            "",
            spec.purpose,
            "",
            "## Use This For",
        ]
    )
    lines.extend(f"- {item}" for item in spec.when_to_use)
    lines.extend(["", "## What To Apply"])
    lines.extend(f"- {item}" for item in spec.apply_rules)
    lines.extend(["", "## Source Files Integrated"])
    lines.extend(f"- `{path.name}`" for path in spec.source_paths)
    for path in spec.source_paths:
        lines.extend(["", f"### {clean_title(path.name)}"])
        bullets = prompt_source_bullets(path) if spec.doc_kind == "prompt" else guide_source_bullets(path)
        lines.extend(f"- {bullet}" for bullet in bullets)
    return "\n".join(lines)


def load_plist(path: Path):
    return plistlib.loads(path.read_bytes())


def render_models_versions_doc() -> str:
    info = load_plist(xr("Info.plist"))
    version = load_plist(xr("version.plist"))
    agent_versions = load_plist(xr("AgentVersions.plist"))
    pairings = load_plist(xr("ApprovedIntegrationModelPairings.plist")).get("pairings", {})
    lines = frontmatter("Assistant Models, Versions, and Pairings")
    lines.extend(
        [
            "# Assistant Models, Versions, and Pairings",
            "",
            "Apple's bundled model metadata for the Xcode coding assistant stack: build context, downloadable agent versions, and approved integration pairings.",
            "",
            "## Use This For",
            "- Understanding which agent binaries Apple references from the Xcode bundle.",
            "- Understanding which model names map to which executor model inside Xcode.",
            "- Tying the skill back to a specific Xcode/IDEIntelligenceChat build.",
            "",
            "## Build Context",
            f"- `CFBundleIdentifier`: `{info.get('CFBundleIdentifier')}`.",
            f"- `CFBundleVersion`: `{info.get('CFBundleVersion')}`.",
            f"- `DTXcodeBuild`: `{info.get('DTXcodeBuild')}`.",
            f"- `DTSDKName`: `{info.get('DTSDKName')}`.",
            f"- `SourceVersion`: `{version.get('SourceVersion')}`.",
            "",
            "## Agent Packages Apple References",
        ]
    )
    for provider, meta in sorted(agent_versions.items()):
        host = urlparse(meta.get("url", "")).netloc or meta.get("url", "")
        lines.append(
            f"- `{provider}`: version `{meta.get('version')}`, checksum present, source host `{host}`."
        )
    lines.extend(["", "## Approved Integration Pairings"])
    for model_name, configs in sorted(pairings.items()):
        formatted = ", ".join(f"{entry.get('role')} -> {entry.get('modelName')}" for entry in configs)
        lines.append(f"- `{model_name}`: {formatted}.")
    lines.extend(
        [
            "",
            "## Source Files Integrated",
            "- `AgentVersions.plist`",
            "- `ApprovedIntegrationModelPairings.plist`",
            "- `Info.plist`",
            "- `version.plist`",
        ]
    )
    return "\n".join(lines)


def render_tools_surfaces_doc() -> str:
    data = load_plist(xr("IDEIntelligenceChat.xcplugindata"))
    extensions = list(data.get("plug-in", {}).get("extensions", {}).values())
    stateless_actions = sorted(
        [ext.get("name") for ext in extensions if ext.get("point") == "Xcode.DVTFoundation.StatelessAction" and ext.get("name")]
    )
    cmd_titles = sorted(
        [ext.get("title") for ext in extensions if ext.get("point") == "Xcode.IDEKit.CmdDefinition" and ext.get("title")]
    )
    navigator_titles = sorted(
        [
            ext.get("title") or ext.get("name")
            for ext in extensions
            if ext.get("point") in {"Xcode.IDEKit.Navigator", "Xcode.IDEKit.NavigatorGroup", "IDEKit.IDESettingsPane"}
            and (ext.get("title") or ext.get("name"))
        ]
    )
    evaluation_verbs = sorted(
        [ext.get("verb") for ext in extensions if "IDEEvaluationCommand" in str(ext.get("point")) and ext.get("verb")]
    )
    provider_hooks = dedupe(
        [
            ext.get("extensionID")
            for ext in extensions
            if ext.get("extensionID")
        ]
        + [
            ext.get("providerClass")
            for ext in extensions
            if ext.get("providerClass")
        ]
    )
    lines = frontmatter("Assistant Tools, Surfaces, and Actions")
    lines.extend(
        [
            "# Assistant Tools, Surfaces, and Actions",
            "",
            "The Xcode surfaces and hooks exposed by `IDEIntelligenceChat.xcplugindata`: actions, commands, navigators, settings panes, preview surfaces, and evaluation verbs.",
            "",
            "## Use This For",
            "- Understanding what Xcode Intelligence can invoke or expose in the UI.",
            "- Understanding the names of built-in Xcode assistant actions and commands.",
            "- Understanding which evaluation and preview surfaces are present in the bundle.",
            "",
            "## Stateless Actions",
        ]
    )
    lines.extend(f"- `{name}`." for name in stateless_actions)
    lines.extend(["", "## User-Facing Surfaces"])
    lines.extend(f"- `{name}`." for name in navigator_titles + cmd_titles)
    lines.extend(["", "## Evaluation Verbs"])
    lines.extend(f"- `{verb}`." for verb in evaluation_verbs)
    lines.extend(["", "## Provider and Steering Hooks"])
    lines.extend(f"- `{hook}`." for hook in provider_hooks[:16])
    lines.extend(["", "## Source Files Integrated", "- `IDEIntelligenceChat.xcplugindata`"])
    return "\n".join(lines)


def render_onboarding_privacy_doc() -> str:
    info = load_plist(xo("Info.plist"))
    version = load_plist(xo("version.plist"))
    plist_data = load_plist(xo("Resources", "IntelligenceInXcode.plist"))
    strings_data = load_plist(xo("Resources", "en.lproj", "IntelligenceInXcode.strings"))
    footer = strings_data.get("FOOTER_TEXT", "")
    known_headings = [
        "Using Third-Party Models",
        "Data Provided to Third-Party Models",
        "ChatGPT in Xcode",
        "Data Provided to ChatGPT in Xcode",
        "Using ChatGPT in Xcode Without an Account",
        "Using ChatGPT in Xcode with a ChatGPT Account",
        "Third-Party Agentic Coding Tools",
        "Data Provided to Apple",
        "Reporting a Concern",
    ]
    paragraphs = [chunk.strip() for chunk in footer.split("\n\n") if chunk.strip()]
    preamble = footer
    section_pairs: list[tuple[str, str]] = []
    if paragraphs and known_headings and known_headings[0] in paragraphs:
        first_heading_index = paragraphs.index(known_headings[0])
        preamble = "\n\n".join(paragraphs[:first_heading_index]).strip()
        current_heading = None
        current_body: list[str] = []
        for paragraph in paragraphs[first_heading_index:]:
            if paragraph in known_headings:
                if current_heading is not None:
                    section_pairs.append((current_heading, "\n\n".join(current_body).strip()))
                current_heading = paragraph
                current_body = []
            else:
                current_body.append(paragraph)
        if current_heading is not None:
            section_pairs.append((current_heading, "\n\n".join(current_body).strip()))
    lines = frontmatter("Assistant Onboarding and Privacy")
    lines.extend(
        [
            "# Assistant Onboarding and Privacy",
            "",
            "Apple's onboarding, privacy, and user-consent text for Intelligence in Xcode, integrated into a single runtime reference instead of a mirrored bundle tree.",
            "",
            "## Use This For",
            "- Understanding what Apple tells the user about third-party models in Xcode.",
            "- Understanding onboarding scope, supported platforms, and privacy boundaries.",
            "- Understanding how Apple describes MCP access and agentic coding tool permissions.",
            "",
            "## Bundle Context",
            f"- `CFBundleIdentifier`: `{info.get('CFBundleIdentifier')}`.",
            f"- `CFBundleVersion`: `{info.get('CFBundleVersion')}`.",
            f"- `ProjectName`: `{version.get('ProjectName')}`.",
            f"- `ContentVersion`: `{plist_data.get('ContentVersion')}`.",
            f"- `SupportedPlatforms`: {short_list(plist_data.get('SupportedPlatforms', []), 10)}.",
            "",
            "## Visible Onboarding Copy",
            f"- `SPLASH_TITLE`: {strings_data.get('SPLASH_TITLE')}",
            f"- `SPLASH_SUMMARY`: {strings_data.get('SPLASH_SUMMARY')}",
            f"- `BUTTON_TITLE`: {strings_data.get('BUTTON_TITLE')}",
            "",
            "## Privacy and Consent Sections",
            f"- Preamble: {preamble.splitlines()[0]}",
        ]
    )
    for heading, body in section_pairs:
        first_sentence = body.split(". ")[0].strip()
        if first_sentence and not first_sentence.endswith("."):
            first_sentence += "."
        lines.append(f"- `{heading}`: {first_sentence}")
    lines.extend(
        [
            "",
            "## Operational Rules Apple States Explicitly",
            "- No model is enabled by default; the user must enable a model before information is shared.",
            "- Conversation history is stored in Xcode and can be viewed or deleted.",
            "- Xcode may send project files and source code to third-party models when the user makes a request.",
            "- Xcode describes MCP-based agentic coding tools as having access to project information and Xcode capabilities, including build and code execution surfaces.",
            "- Apple distinguishes ChatGPT without an account from ChatGPT with an account, and says different OpenAI data-handling terms apply.",
            "",
            "## Source Files Integrated",
            "- `XCODE_ONBOARDING_CONTENTS/Info.plist`",
            "- `XCODE_ONBOARDING_CONTENTS/version.plist`",
            "- `XCODE_ONBOARDING_RESOURCES/IntelligenceInXcode.plist`",
            "- `XCODE_ONBOARDING_RESOURCES/en.lproj/IntelligenceInXcode.strings`",
        ]
    )
    return "\n".join(lines)


def parse_ndjson(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in read_text(path).splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def render_system_context_doc() -> str:
    onboarding = load_plist(SYSTEM_INTELLIGENCE)
    foundation = load_plist(SYSTEM_FOUNDATION_MODELS)
    ndjson_rows = parse_ndjson(SYSTEM_TASKED_CONFIG)
    chat_transform = None
    availability_transform = None
    for row in ndjson_rows:
        transform = row.get("addTransform")
        if not isinstance(transform, dict):
            continue
        if transform.get("name") == "ChatMessageTelemetryv2":
            chat_transform = transform
        if transform.get("name") == "AvailabilityDetailedStatus_V8":
            availability_transform = transform
    restriction = foundation.get("CompileDraftModel", {}).get("Restriction", {})
    attribute_group = foundation.get("CompileDraftModel", {}).get("AttributeGroups", [{}])[0]
    attributes = attribute_group.get("Attributes", [])
    running_policy = []
    for attr in attributes:
        attr_class = attr.get("Class")
        if attr_class == "RBSDurationAttribute":
            running_policy.append(
                f"duration `{attr.get('InvalidationDuration')}` seconds with warning `{attr.get('WarningDuration')}` seconds"
            )
        elif attr_class == "RBSCPUAccessGrant":
            running_policy.append(f"CPU role `{attr.get('Role')}`")
        elif attr_class == "RBSJetsamPriorityGrant":
            running_policy.append(f"jetsam band `{attr.get('Band')}`")
        elif attr_class == "RBSRunningReasonAttribute":
            running_policy.append(f"running reason `{attr.get('RunningReason')}`")
        elif attr_class in {"RBSPreserveBaseMemoryGrant", "RBSPreventIdleSleepGrant"}:
            running_policy.append(attr_class)
    lines = frontmatter("System Intelligence Context and Telemetry")
    lines.extend(
        [
            "# System Intelligence Context and Telemetry",
            "",
            "System-level Apple Intelligence context that helps explain platform availability, FoundationModels process policy, and the telemetry vocabulary around Xcode chat activity.",
            "",
            "## Use This For",
            "- Understanding how system Apple Intelligence support is framed outside Xcode.",
            "- Understanding the entitlement and process policy tied to FoundationModels work.",
            "- Understanding which Xcode chat metrics Apple appears to track in CoreAnalytics configuration.",
            "",
            "## System Availability Context",
            f"- Supported platforms in system onboarding bundle: {short_list(onboarding.get('SupportedPlatforms', []), 10)}.",
            "",
            "## FoundationModels Process Policy",
            f"- Restriction entitlement: `{restriction.get('Entitlement')}`.",
            f"- Running policy cues: {short_list(running_policy, 10)}.",
            "",
            "## Telemetry Vocabulary Relevant To Xcode Chat",
        ]
    )
    if chat_transform:
        dimensions = [item.get("name") for item in chat_transform.get("dimensions", []) if item.get("name")]
        measures = [item.get("name") for item in chat_transform.get("measures", []) if item.get("name")]
        lines.append(f"- `ChatMessageTelemetryv2` dimensions include: {short_list(dimensions, 14)}.")
        lines.append(f"- `ChatMessageTelemetryv2` measures include: {short_list(measures, 10)}.")
    if availability_transform:
        dimensions = [item.get("name") for item in availability_transform.get("dimensions", []) if item.get("name")]
        lines.append(f"- `AvailabilityDetailedStatus_V8` tracks availability and download-state fields such as: {short_list(dimensions, 12)}.")
    lines.extend(
        [
            "",
            "## Source Files Integrated",
            "- `SYSTEM_INTELLIGENCE_PLIST`",
            "- `SYSTEM_FOUNDATION_MODELS_PLIST`",
            "- `SYSTEM_TASKED_CONFIG_JSON`",
        ]
    )
    return "\n".join(lines)


ALL_RUNTIME_DOCS = PROMPT_DOCS + GUIDE_DOCS


def references_path(filename: str) -> Path:
    return REFERENCES / filename


def runtime_doc_map() -> dict[Path, Path]:
    mapping: dict[Path, Path] = {}
    for spec in ALL_RUNTIME_DOCS:
        output = references_path(spec.filename)
        for source in spec.source_paths:
            mapping[source] = output
    for filename, source_paths in METADATA_SOURCE_MAP.items():
        output = references_path(filename)
        for source in source_paths:
            mapping[source] = output
    return mapping


def classify_source(path: Path, output: Path | None) -> SourceRecord:
    if str(path).startswith(str(XCODE_RESOURCES)):
        source_type = "binary" if path.name in {"claude", "codex"} else (path.suffix.lstrip(".") or "file")
        provenance = "canonical-xcode"
        if path.suffix == ".idechatprompttemplate" or path.parent == XCODE_ADDITIONAL:
            handling = "extract-and-incorporate"
            root_label = "XCODE_RESOURCES" if path.suffix == ".idechatprompttemplate" else "XCODE_ADDITIONAL_DOCUMENTATION"
            discovery = f'fd -H -t f -a -e {path.suffix.lstrip(".")} . "${root_label}"'
        else:
            handling = "summarize-structured"
            discovery = f"plutil -p {shell_ref(path)}"
        version_context = f"Selected Xcode {XCODE_VERSION} / IDEIntelligenceChat {IDE_INTELLIGENCE_VERSION}"
        return SourceRecord(path, source_type, provenance, handling, output, discovery, version_context)
    if path in {SYSTEM_INTELLIGENCE, SYSTEM_FOUNDATION_MODELS, SYSTEM_TASKED_CONFIG}:
        source_type = path.suffix.lstrip(".") or "file"
        provenance = "system-apple"
        handling = "summarize-structured"
        discovery = f"plutil -p {shell_ref(path)}" if path.suffix == ".plist" else f"sed -n '1,120p' {shell_ref(path)}"
        version_context = "System Apple Intelligence / FoundationModels policy / CoreAnalytics telemetry"
        return SourceRecord(path, source_type, provenance, handling, output, discovery, version_context)
    source_type = "binary" if path.name in {"claude", "codex"} else (path.suffix.lstrip(".") or "file")
    discovery = 'fd -H -t f -a . "$LOCAL_XCODE_CODINGASSISTANT_ROOT"'
    if source_type == "binary":
        discovery = f"file {shell_ref(path)} && shasum -a 256 {shell_ref(path)}"
    return SourceRecord(
        path=path,
        source_type=source_type,
        provenance_tier="local-xcode-assistant",
        handling_mode="maintenance-only",
        output_path=None,
        discovery_command=discovery,
        version_context="Local Xcode Coding Assistant stack",
    )


def clean_generated_outputs() -> None:
    shutil.rmtree(REFERENCES, ignore_errors=True)
    REFERENCES.mkdir(parents=True, exist_ok=True)


def build_records() -> list[SourceRecord]:
    mapping = runtime_doc_map()
    records = [classify_source(path, output) for path, output in mapping.items()]
    for path in local_audit_sources():
        records.append(classify_source(path, None))
    return sorted(records, key=lambda item: str(item.path))


def write_reference_files() -> None:
    for spec in ALL_RUNTIME_DOCS:
        write_text(references_path(spec.filename), render_runtime_doc(spec))
    write_text(references_path(MODELS_DOC), render_models_versions_doc())
    write_text(references_path(TOOLS_DOC), render_tools_surfaces_doc())
    write_text(references_path(ONBOARDING_DOC), render_onboarding_privacy_doc())
    write_text(references_path(SYSTEM_DOC), render_system_context_doc())

    index_lines = frontmatter("Apple Development Official Reference Index")
    index_lines.extend(
        [
            "# Apple Development Official Reference Index",
            "",
            "Flat runtime reference set grouped by function rather than by Apple's on-disk bundle layout.",
            "",
            "## Prompting",
            "- `prompting-core-rules.md`: base Apple/Xcode steering for coding behavior.",
            "- `prompting-query-response-and-titles.md`: ordinary query handling, response shaping, and title behavior.",
            "- `prompting-code-editing-documentation-and-apply.md`: integration, explanation, documentation, and fast-apply behavior.",
            "- `prompting-preview-and-playground-generation.md`: preview and playground output rules.",
            "- `prompting-context-search-and-selection.md`: current-file, selection, issues, and search context assembly.",
            "- `prompting-planner-executor-and-retrieval.md`: planner/executor behavior plus retrieval and infill support.",
            "",
            "## Platform Guidance",
            "- `platform-swiftui-liquid-glass-and-modern-ui.md`: SwiftUI, Liquid Glass, toolbar, text editing, WebKit, and AlarmKit guidance.",
            "- `platform-cross-framework-liquid-glass.md`: UIKit, AppKit, and WidgetKit Liquid Glass guidance.",
            "- `platform-foundation-models-intents-and-intelligence.md`: FoundationModels, AppIntents, Visual Intelligence, and Assistive Access.",
            "- `platform-swift-language-concurrency-and-data.md`: Swift Concurrency, InlineArray/Span, SwiftData, and AttributedString updates.",
            "- `platform-maps-storekit-charts-and-widgets.md`: MapKit, StoreKit, Charts, and visionOS widgets.",
            "",
            "## Assistant Wiring",
            "- `assistant-models-versions-and-pairings.md`: bundled model metadata, versions, and approved pairings.",
            "- `assistant-tools-surfaces-and-actions.md`: Xcode assistant actions, commands, navigators, and evaluation verbs.",
            "- `assistant-onboarding-and-privacy.md`: onboarding copy, consent model, MCP framing, and privacy constraints.",
            "- `system-intelligence-context-and-telemetry.md`: system availability, FoundationModels process policy, and chat telemetry vocabulary.",
        ]
    )
    write_text(references_path("index.md"), "\n".join(index_lines))

    routing_lines = frontmatter("Apple Development Official Task Routing")
    routing_lines.extend(
        [
            "# Apple Development Official Task Routing",
            "",
            "## SwiftUI, Liquid Glass, and UI Work",
            "- Start with `platform-swiftui-liquid-glass-and-modern-ui.md`.",
            "- Add `platform-cross-framework-liquid-glass.md` when UIKit, AppKit, or WidgetKit are involved.",
            "- Add `prompting-preview-and-playground-generation.md` when the task asks for `#Preview` output.",
            "",
            "## General Apple Code Editing",
            "- Start with `prompting-core-rules.md` and `prompting-code-editing-documentation-and-apply.md`.",
            "- Add `platform-swift-language-concurrency-and-data.md` when concurrency, data, or Foundation text behavior matters.",
            "",
            "## FoundationModels, AppIntents, and Intelligence Features",
            "- Start with `platform-foundation-models-intents-and-intelligence.md`.",
            "- Add `assistant-models-versions-and-pairings.md` when the request is about model/provider wiring inside Xcode.",
            "",
            "## Xcode Assistant Behavior",
            "- Start with `prompting-core-rules.md` and `prompting-planner-executor-and-retrieval.md`.",
            "- Add `assistant-tools-surfaces-and-actions.md` and `assistant-onboarding-and-privacy.md` when the task is about Xcode Intelligence itself.",
            "",
            "## Context Assembly and Search",
            "- Load `prompting-context-search-and-selection.md` when current-file, search-result, issue, or selection behavior matters.",
            "",
            "## StoreKit, Maps, Charts, and Widgets",
            "- Load `platform-maps-storekit-charts-and-widgets.md`.",
            "",
            "## System-Level Apple Intelligence Context",
            "- Load `system-intelligence-context-and-telemetry.md` when the task is about system availability, FoundationModels process policy, or telemetry vocabulary.",
        ]
    )
    write_text(references_path("task-routing.md"), "\n".join(routing_lines))


def write_maintenance(records: list[SourceRecord]) -> None:
    MAINTENANCE.mkdir(parents=True, exist_ok=True)
    manifest_lines = frontmatter("Apple Development Official Skill Manifest")
    manifest_lines.extend(
        [
            "# Skill Manifest",
            "",
            "- `skill_version`: `26.4.1.1`",
            f"- `snapshot_date`: `{date.today().isoformat()}`",
            "- `runtime_structure`: flat `references/` directory with functional docs instead of mirrored Apple/Xcode paths.",
            "- `selected_xcode_developer_dir`: `SELECTED_XCODE_DEVELOPER_DIR`",
            "- `selected_xcode_app`: `SELECTED_XCODE_APP`",
            f"- `xcode_version`: `{XCODE_VERSION}`",
            f"- `xcode_build`: `{IDE_INTELLIGENCE_INFO.get('DTXcodeBuild', 'unknown')}`",
            f"- `ide_intelligencechat_version`: `{IDE_INTELLIGENCE_VERSION}`",
            f"- `ide_intelligencechat_source_version`: `{IDE_INTELLIGENCE_SOURCE_VERSION}`",
            f"- `claude_version`: `{CLAUDE_VERSION}`",
            f"- `codex_version`: `{CODEX_AGENT_VERSION}`",
            "- `install_path`: `SKILL_ROOT`",
            f"- `symlink_path`: `CODEX_HOME/skills/{SKILL_NAME}`",
            "- `runtime_scope_note`: runtime references are limited to canonical Apple/Xcode and system Apple Intelligence material.",
            "- `exclusion_note`: local Coding Assistant files are tracked only for audit and update review.",
        ]
    )
    write_text(MAINTENANCE / "skill-manifest.md", "\n".join(manifest_lines))

    selection_lines = frontmatter("Apple Development Official Source Selection")
    selection_lines.extend(
        [
            "# Source Selection",
            "",
            "## Runtime Organization",
            "- `references/` is flat and grouped by what each doc helps with: prompting, platform guidance, assistant wiring, and system context.",
            "- Multiple Apple source files are intentionally merged into each runtime doc when that makes the guidance more usable for an agent.",
            "- The runtime layout does not mirror Xcode bundle folders, `Contents`, `Resources`, plist filenames, or bundle names.",
            "",
            "## Runtime Sources Included",
            "- Xcode `*.idechatprompttemplate` files.",
            "- Apple bundled markdown guides from `AdditionalDocumentation`.",
            "- Xcode assistant metadata and onboarding sources when they materially explain behavior, consent, model pairing, or exposed tooling.",
            "- System Apple Intelligence sources when they materially explain availability, policy, or telemetry vocabulary.",
            "",
            "## Sources Excluded From Runtime References",
            "- User-local `LOCAL_XCODE_CODINGASSISTANT_ROOT` files.",
            "- Local Claude/Codex binaries and manifests.",
            "- Local copies of helper skills such as `skill-creator` and `skill-installer`.",
            "",
            "## Reason",
            "- Those local files describe a particular machine's assistant installation, not Apple's platform-development guidance.",
            "- They are kept in maintenance only so the skill can be updated deliberately when Apple changes what Xcode ships.",
        ]
    )
    write_text(MAINTENANCE / "source-selection.md", "\n".join(selection_lines))

    inventory_lines = frontmatter("Apple Development Official Source Inventory")
    inventory_lines.extend(
        [
            "# Source Inventory",
            "",
            "| Source | Type | Provenance | Mode | Output | SHA256 | Discovery Command | Version Context |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        output = symbolic_path(record.output_path) if record.output_path else "maintenance-only"
        inventory_lines.append(
            "| "
            + " | ".join(
                [
                    f"`{symbolic_path(record.path)}`",
                    record.source_type,
                    record.provenance_tier,
                    record.handling_mode,
                    output,
                    sha256(record.path),
                    record.discovery_command.replace("|", "\\|"),
                    record.version_context,
                ]
            )
            + " |"
        )
    write_text(MAINTENANCE / "source-inventory.md", "\n".join(inventory_lines))

    output_groups: dict[str, list[SourceRecord]] = {}
    for record in records:
        key = str(record.output_path) if record.output_path else "maintenance-only"
        output_groups.setdefault(key, []).append(record)
    checklist_lines = frontmatter("Apple Development Official Source Coverage Checklist")
    checklist_lines.extend(
        [
            "# Source Coverage Checklist",
            "",
            "## Runtime Docs",
        ]
    )
    for output, grouped_records in sorted(output_groups.items()):
        if output == "maintenance-only":
            continue
        checklist_lines.append(f"- [x] `{Path(output).name}` integrates {len(grouped_records)} source files.")
    checklist_lines.extend(["", "## Maintenance-Only Audit Coverage"])
    maintenance_records = output_groups.get("maintenance-only", [])
    checklist_lines.append(f"- [x] `maintenance-only`: {len(maintenance_records)} local audit files are tracked without being loaded at runtime.")
    checklist_lines.extend(["", "## File-Level Coverage"])
    for record in records:
        target = symbolic_path(record.output_path) if record.output_path else "maintenance-only"
        checklist_lines.append(f"- [x] `{symbolic_path(record.path)}` -> `{target}`")
    write_text(MAINTENANCE / "source-coverage-checklist.md", "\n".join(checklist_lines))


def write_scan_script() -> None:
    content = """#!/usr/bin/env bash
set -euo pipefail

SELECTED_DEVELOPER_DIR="$(xcode-select -p)"
XCODE_APP="$(cd "$SELECTED_DEVELOPER_DIR/../.." && pwd)"
XCODE_RESOURCES="$XCODE_APP/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources"
XCODE_ADDITIONAL_DOCUMENTATION="$XCODE_RESOURCES/AdditionalDocumentation"
LOCAL_XCODE_CODINGASSISTANT_ROOT="$HOME/Library/Developer/Xcode/CodingAssistant"
ROOT_ANCHOR="$(python3 - <<'PY'
from pathlib import Path
print(Path.home().anchor, end="")
PY
)"
SYSTEM_INTELLIGENCE_PLIST="${ROOT_ANCHOR}System/Library/OnBoardingBundles/com.apple.onboarding.intelligenceengine.bundle/Contents/Resources/Intelligence.plist"
SYSTEM_FOUNDATION_MODELS_PLIST="${ROOT_ANCHOR}System/Library/LifecyclePolicy/DomainAttributes/com.apple.foundationmodels.plist"
SYSTEM_TASKED_CONFIG_JSON="${ROOT_ANCHOR}Library/CoreAnalytics/taskedConfig.json"

echo "fd -H -t f -a -e idechatprompttemplate . $XCODE_RESOURCES | sort"
fd -H -t f -a -e idechatprompttemplate . "$XCODE_RESOURCES" | sort
echo
echo "fd -H -t f -a -e md . $XCODE_ADDITIONAL_DOCUMENTATION | sort"
fd -H -t f -a -e md . "$XCODE_ADDITIONAL_DOCUMENTATION" | sort
echo
echo "fd -H -t f -a . $LOCAL_XCODE_CODINGASSISTANT_ROOT | sort"
fd -H -t f -a . "$LOCAL_XCODE_CODINGASSISTANT_ROOT" | sort
echo
echo "plutil -p $XCODE_RESOURCES/ApprovedIntegrationModelPairings.plist"
plutil -p "$XCODE_RESOURCES/ApprovedIntegrationModelPairings.plist"
echo
echo "plutil -p $XCODE_RESOURCES/IDEIntelligenceChat.xcplugindata"
plutil -p "$XCODE_RESOURCES/IDEIntelligenceChat.xcplugindata"
echo
echo "plutil -p $SYSTEM_INTELLIGENCE_PLIST"
plutil -p "$SYSTEM_INTELLIGENCE_PLIST"
echo
echo "plutil -p $SYSTEM_FOUNDATION_MODELS_PLIST"
plutil -p "$SYSTEM_FOUNDATION_MODELS_PLIST"
echo
echo "sed -n '1,120p' $SYSTEM_TASKED_CONFIG_JSON"
sed -n '1,120p' "$SYSTEM_TASKED_CONFIG_JSON"
"""
    write_text(SCRIPTS / "scan_sources.sh", content)
    (SCRIPTS / "scan_sources.sh").chmod(0o755)


def main() -> None:
    clean_generated_outputs()
    write_reference_files()
    records = build_records()
    write_maintenance(records)
    write_scan_script()


if __name__ == "__main__":
    main()
