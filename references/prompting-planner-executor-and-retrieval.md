---
title: Prompting Planner, Executor, and Retrieval
---

# Prompting Planner, Executor, and Retrieval

Planner/executor orchestration plus the retrieval-style prompt fragments Xcode uses for search and infill support.

## Use This For
- Multi-step or agentic Apple-platform tasks.
- Questions about how Xcode decides between planning, retrieval, and execution.
- Requests that benefit from understanding vector search or retrieval expansion behavior.

## What To Apply
- Separate planning from execution when the prompt family does so.
- Use retrieval expansion only as a support mechanism for context discovery or infill.
- Treat the planner/executor prompts as workflow steering, not as product API documentation.

## Source Files Integrated
- `InstructionEmbeddingsQueryExpansion.idechatprompttemplate`
- `LocalInfillEmbeddingsQueryExpansion.idechatprompttemplate`
- `PlannerExecutorStyleNoClassify.idechatprompttemplate`
- `PlannerExecutorStylePlannerSystemPrompt-gpt_5.idechatprompttemplate`
- `PlannerExecutorStylePlannerSystemPrompt.idechatprompttemplate`

### Instruction Embeddings Query Expansion
- Helps with query handling and response shaping.
- Important terms present: Given, Examples, How, The, To, BakeryCakeItem, Is, SoupOrderFulfiller.

### Local Infill Embeddings Query Expansion
- Helps with query handling and response shaping.
- Important terms present: How, The, To, BakeryCakeItem, Is, SoupOrderFulfiller.

### Planner Executor Style No Classify
- Helps with planner/executor orchestration.
- Carry forward: Assume SwiftUI patterns may have evolved and favor current Apple-native approaches.; Use `#Preview` for modern SwiftUI preview generation when the template is preview-related.; Avoid falling back to `Combine` when the guidance favors async/await.; Prefer the modern `Testing` framework for unit tests..
- Source anchors: Instructions, Guidelines for Modern Swift, Modern Swift Testing, expect(three + seven == 10, "The sums should work out."), expect(sum == 10), Modern Previews, and 2 more.
- Important terms present: viewDidLoad(), @Suite, XCTUnwrap, PreviewProvider, #Preview, @Test, You, Your, Instructions, Sometimes.

### Planner Executor Style Planner System Prompt GPT 5
- Helps with planner/executor orchestration.
- Carry forward: Assume SwiftUI patterns may have evolved and favor current Apple-native approaches.; Use `#Preview` for modern SwiftUI preview generation when the template is preview-related.; Add `List` only when the source view or task implies list or row context.; Prefer the modern `Testing` framework for unit tests..
- Source anchors: expect(three + seven == 10, "The sums should work out."), expect(sum == 10).
- Important terms present: aVariableName, MyFile.swift, RobotViewModel.swift, #Preview, @Suite, @Test, .swift, You, Apple, Xcode.

### Planner Executor Style Planner System Prompt
- Helps with planner/executor orchestration.
- Carry forward: Assume SwiftUI patterns may have evolved and favor current Apple-native approaches.; Use `#Preview` for modern SwiftUI preview generation when the template is preview-related.; Add `List` only when the source view or task implies list or row context.; Avoid falling back to `Combine` when the guidance favors async/await.; Prefer the modern `Testing` framework for unit tests..
- Source anchors: Instructions, Message Classification, General Hints, Editing Code, Explaining Code, As you're responding to a user's question:, and 7 more.
- Important terms present: viewDidLoad(), @Suite, XCTUnwrap, PreviewProvider, #Preview, @Test, You, Your, Instructions, Message.
