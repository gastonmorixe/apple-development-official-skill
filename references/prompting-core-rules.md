---
title: Prompting Core Rules
---

# Prompting Core Rules

Base Apple/Xcode steering for how an agent should reason, search, validate, and format Apple-platform coding work.

## Use This For
- General Swift, SwiftUI, UIKit, AppKit, or WidgetKit coding tasks.
- Any task where Xcode's built-in agent policy matters more than generic coding advice.
- Requests that touch new Apple topics such as Liquid Glass or FoundationModels.

## What To Apply
- Prefer Swift-first, Apple-platform-first solutions.
- Use current Apple documentation when a framework or design system may be newer than the model's training cutoff.
- Prefer Swift Concurrency and Swift Testing over older Combine-first or XCTest-only defaults when the source guidance points that way.
- Preserve Apple platform naming and modern SwiftUI conventions such as `@State private var`.

## Source Files Integrated
- `AgentSystemPromptAddition.idechatprompttemplate`
- `BasicSystemPrompt.idechatprompttemplate`
- `ReasoningSystemPrompt.idechatprompttemplate`
- `TextEditorToolSystemPrompt.idechatprompttemplate`
- `ToolAssistedBasicSystemPrompt.idechatprompttemplate`
- `ToolAssistedReasoningSystemPrompt.idechatprompttemplate`
- `VariantASystemPrompt.idechatprompttemplate`
- `VariantBSystemPrompt.idechatprompttemplate`

### Agent System Prompt Addition
- Helps with base system prompting and reasoning.
- Carry forward: Use Apple documentation search when the topic may be newer than cached knowledge.; Validate substantial changes with Xcode build tooling when compile confidence matters.; Prefer fast file diagnostics before a full build when the source prompt points at that workflow.; Use lightweight snippet execution when the source prompt expects experimentation instead of a full build.; Treat Liquid Glass as a new Apple design system and check current guidance instead of relying on older UI instincts..
- Source anchors: Xcode, Apple Developer Documentation, Build Commands, Limiting Changes to the Requested Task, Code Style Guidelines, Validating your work.
- Important terms present: DocumentationSearch, BuildProject, @State private var, View, XcodeRefreshCodeIssuesInFile, ExecuteSnippet, @State, Xcode, You, IDE.

### Basic System Prompt
- Helps with base system prompting and reasoning.
- Carry forward: Avoid falling back to `Combine` when the guidance favors async/await.; Prefer the modern `Testing` framework for unit tests..
- Source anchors: expect(three + seven == 10, "The sums should work out."), expect(sum == 10).
- Important terms present: @Suite, XCTUnwrap, @Test, .swift, You, Below, Your, Whenever, Apple, APIs.

### Reasoning System Prompt
- Helps with base system prompting and reasoning.
- Carry forward: Avoid falling back to `Combine` when the guidance favors async/await..
- Important terms present: .swift, You, Below, Your, Whenever, Apple, APIs, Swift, Always, Objective.

### Text Editor Tool System Prompt
- Helps with base system prompting and reasoning.
- Carry forward: Add `List` only when the source view or task implies list or row context.; Avoid falling back to `Combine` when the guidance favors async/await.; Prefer the modern `Testing` framework for unit tests..
- Source anchors: expect(three + seven == 10, "The sums should work out."), expect(sum == 10).
- Important terms present: @Suite, XCTUnwrap, @Test, You, Below, Your, Whenever, Apple, APIs, Swift.

### Tool Assisted Basic System Prompt
- Helps with base system prompting and reasoning.
- Carry forward: Avoid falling back to `Combine` when the guidance favors async/await.; Prefer the modern `Testing` framework for unit tests..
- Source anchors: SEARCH: TypeName1, SEARCH: a phrase or set of keywords to search for, expect(three + seven == 10, "The sums should work out."), expect(sum == 10).
- Important terms present: @Suite, XCTUnwrap, @Test, .swift, You, Below, Your, Do, Briefly, Search.

### Tool Assisted Reasoning System Prompt
- Helps with base system prompting and reasoning.
- Carry forward: Avoid falling back to `Combine` when the guidance favors async/await..
- Source anchors: SEARCH: TypeName1, SEARCH: a phrase or set of keywords to search for.
- Important terms present: .swift, You, Below, Your, Do, Briefly, Search, Use, SEARCH, TypeName1.

### Variant Asystem Prompt
- Helps with base system prompting and reasoning.
- Carry forward: Avoid falling back to `Combine` when the guidance favors async/await..
- Important terms present: You, Below, Your, Whenever, Apple, APIs, Swift, Always, Objective, Pay.

### Variant Bsystem Prompt
- Helps with base system prompting and reasoning.
- Carry forward: Avoid falling back to `Combine` when the guidance favors async/await..
- Important terms present: viewDidLoad(), You, Below, Your, Whenever, Apple, APIs, Swift, Always, Objective.
