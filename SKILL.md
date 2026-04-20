---
name: apple-development-official
description: Official Xcode-grounded Apple development guidance for Swift, SwiftUI, UIKit, AppKit, WidgetKit, FoundationModels, AppIntents, Liquid Glass, Visual Intelligence, Xcode prompt behavior, and preview/code-edit workflows. Use when Codex needs to answer or edit Apple-platform code, generate or fix \#Preview blocks, interpret bundled Xcode Intelligence prompts/docs, or apply Apple-specific guidance from the selected Xcode and Apple system materials.
---

# Apple Development Official

Use this skill for Apple-platform work where Xcode's own guidance matters more than generic advice: Swift-first app code, SwiftUI/UI framework questions, Liquid Glass, FoundationModels, AppIntents, previews, and Xcode agent behavior.

## Load Order

1. Start with `references/index.md` to choose the right family of docs.
2. Use `references/task-routing.md` for the quick map from task type to reference file.
3. Load only the one or two flat runtime docs that match the task, usually a `prompting-*.md` file plus a `platform-*.md` file.
4. For Xcode assistant behavior, load `references/prompting-core-rules.md`, `references/prompting-planner-executor-and-retrieval.md`, and then the relevant `assistant-*.md` file.
5. For Apple framework and UI work, load the relevant `platform-*.md` file and add `references/prompting-preview-and-playground-generation.md` when the task asks for `#Preview` output.
6. Load `references/system-intelligence-context-and-telemetry.md` only when the task is about system availability, FoundationModels policy, or telemetry vocabulary.

## Working Rules

- Prefer Swift, SwiftUI, UIKit, AppKit, WidgetKit, FoundationModels, AppIntents, and Apple APIs that ship on platform.
- Prefer Swift Concurrency and Swift Testing.
- Use `#Preview` for new SwiftUI previews.
- Prefer the bundled Apple and Xcode references before falling back to generic reasoning.
- Treat local Coding Assistant installation files as audit material, not runtime coding guidance.
- Preserve Apple platform names such as iOS, iPadOS, macOS, watchOS, and visionOS.
- Keep edits minimal unless the reference material clearly says otherwise.
- Do not load `maintenance/` files during routine use.
