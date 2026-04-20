# Apple Development Official

A public Codex skill built from Apple-shipped Xcode Agentic Coding material, reorganized into a clean, agent-friendly reference set for serious Apple platform development.

![Version](https://img.shields.io/badge/version-0.1.0-black)
![Xcode](https://img.shields.io/badge/Xcode-26.4.1-blue)
![License](https://img.shields.io/badge/license-MIT-green)

`Apple Development Official` turns the Apple development guidance bundled inside Xcode into a usable skill for real coding work.

It is not a raw dump of Xcode files.

It is a curated, flattened, public-release skill that preserves the value of Apple's original prompt templates, docs, onboarding copy, model wiring, and system context while reorganizing them into practical references an agent can actually use.

## Why This Exists

Modern Apple development is moving fast. SwiftUI patterns change. Liquid Glass is new. FoundationModels is new. Xcode itself now ships prompt templates, retrieval hints, model metadata, onboarding text, and Apple-authored docs specifically meant to support coding workflows.

This skill captures that material and makes it reusable outside the Xcode bundle layout.

## What You Get

- Apple-grounded prompting guidance for code editing, preview generation, planner/executor behavior, context assembly, and response shaping.
- Apple-authored platform guidance for SwiftUI, Liquid Glass, FoundationModels, AppIntents, Visual Intelligence, Swift Concurrency, SwiftData, StoreKit, MapKit, Charts, and widgets.
- Xcode assistant wiring docs covering model pairings, tool surfaces, onboarding/privacy, and system-level Apple Intelligence context.
- A flat `references/` directory organized by what each document helps with, not by Apple's internal bundle paths.
- A maintenance trail for future Xcode refreshes without polluting the runtime skill.

## Source Basis

This release is based on the material shipped with:

- `Xcode 26.4.1`
- `IDEIntelligenceChat 24899.2`
- `DTXcodeBuild 17E201`

Runtime references are built from:

- `46` Xcode `*.idechatprompttemplate` files
- `20` bundled Apple markdown guides from `AdditionalDocumentation`
- Xcode assistant metadata and onboarding sources
- system Apple Intelligence policy and telemetry context

User-local Coding Assistant files are intentionally excluded from runtime references and kept only in maintenance for audit and future update work.

## How It Is Organized

The skill is intentionally flat and functional.

Instead of mirroring `Contents/Resources/...` and similar internal Apple paths, the runtime corpus is split into clear reference docs such as:

- `prompting-core-rules.md`
- `prompting-code-editing-documentation-and-apply.md`
- `prompting-preview-and-playground-generation.md`
- `platform-swiftui-liquid-glass-and-modern-ui.md`
- `platform-foundation-models-intents-and-intelligence.md`
- `assistant-models-versions-and-pairings.md`
- `assistant-onboarding-and-privacy.md`
- `system-intelligence-context-and-telemetry.md`

Start with:

- [`references/index.md`](./references/index.md)
- [`references/task-routing.md`](./references/task-routing.md)

## Installation

Place the skill in your Codex skills directory, or symlink it from your managed skills folder.

```bash
mkdir -p ~/.codex/skills
ln -sfn ~/.agents/skills/apple-development-official ~/.codex/skills/apple-development-official
```

If you keep skills directly in `~/.codex/skills`, you can copy the folder there instead.

## Usage

Use this skill when the task needs Apple-specific development guidance rather than generic coding advice.

Examples:

- “Add a Liquid Glass treatment to this SwiftUI view and keep it idiomatic for current Xcode.”
- “Generate a `#Preview` for this view the way Xcode expects.”
- “Help me refactor this SwiftUI screen using current Apple patterns, not old representable workarounds.”
- “Explain how Xcode steers agentic edits and model/tool behavior.”
- “Show me how FoundationModels and AppIntents fit together for this feature.”

## Design Principles

- Preserve Apple meaning, API names, and behavioral guidance.
- Do not mirror Apple's internal folder tree.
- Merge or split sources by usefulness to an agent, not by original container structure.
- Keep runtime references focused and readable.
- Keep machine-local assistant artifacts out of the runtime corpus.

## Repository Layout

- [`SKILL.md`](./SKILL.md): skill entrypoint and loading rules
- [`references/`](./references): flat runtime reference set
- [`scripts/build_reference_corpus.py`](./scripts/build_reference_corpus.py): rebuilds the runtime corpus from source materials
- [`scripts/scan_sources.sh`](./scripts/scan_sources.sh): rescans upstream Apple/Xcode inputs
- [`maintenance/`](./maintenance): provenance, source inventory, selection rationale, and coverage tracking

## Updating For A New Xcode Release

1. Run [`scripts/scan_sources.sh`](./scripts/scan_sources.sh) to inspect what changed upstream.
2. Review the affected Apple/Xcode inputs.
3. Run [`scripts/build_reference_corpus.py`](./scripts/build_reference_corpus.py) to regenerate the flattened runtime docs and maintenance ledger.
4. Revalidate the skill.

## Public Release Notes

- This project is derived from Apple-shipped Xcode Intelligence material, but it is reorganized and published as an independent skill.
- It is designed for practical agent use, not for reproducing Apple's internal on-disk structure.
- It is not affiliated with or endorsed by Apple.

## License

MIT
