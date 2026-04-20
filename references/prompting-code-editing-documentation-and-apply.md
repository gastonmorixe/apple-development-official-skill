---
title: Prompting Code Editing, Documentation, and Apply
---

# Prompting Code Editing, Documentation, and Apply

How Xcode steers code edits, integration, explanation, documentation updates, and fast-apply workflows.

## Use This For
- Code modification requests.
- Documentation comment generation or explanation tasks.
- Cases where the agent should integrate edits rather than produce stand-alone code.

## What To Apply
- Keep edits tightly scoped to the requested change.
- Preserve surrounding project structure unless the source guidance clearly calls for refactoring.
- Separate user intent from code instructions when an integration prompt does that explicitly.
- Use fast-apply style behavior only when a targeted patch is clearly appropriate.

## Source Files Integrated
- `CodingToolTemplateDocument.idechatprompttemplate`
- `CodingToolTemplateExplain.idechatprompttemplate`
- `FastApplyIntegratorSystemPrompt.idechatprompttemplate`
- `FastApplyIntegratorUserPrompt.idechatprompttemplate`
- `GenerateDocumentation.idechatprompttemplate`
- `IntegratorSystemPrompt.idechatprompttemplate`
- `IntegratorUserPrompt.idechatprompttemplate`
- `NewCodeIntegratorSystemPrompt.idechatprompttemplate`
- `NewCodeIntegratorUserPrompt.idechatprompttemplate`

### Coding Tool Template Document
- Helps with documentation or explanation output.
- Important terms present: Selected, Code, Please, XcodeRead, Follow, Swift, Use, Include, Add, Important.

### Coding Tool Template Explain
- Helps with documentation or explanation output.
- Important terms present: Selected, Code, Please, XcodeRead.

### Fast Apply Integrator System Prompt
- Helps with code integration and targeted editing.
- Important terms present: You.

### Fast Apply Integrator User Prompt
- Helps with code integration and targeted editing.
- Important terms present: Merge, Preserve, Output, Do.

### Generate Documentation
- Helps with documentation or explanation output.
- Important terms present: Only, No, Swift.

### Integrator System Prompt
- Helps with code integration and targeted editing.
- Important terms present: You, Your, Rules, READ, FOLLOW, PRESERVE, MAINTAIN, ENSURE, RETURN, ENTIRE.

### Integrator User Prompt
- Helps with code integration and targeted editing.
- Important terms present: Answer.

### New Code Integrator System Prompt
- Helps with code integration and targeted editing.
- Important terms present: You, Your, Rules, READ, FOLLOW, MAINTAIN, ENSURE, RETURN, ENTIRE, When.

### New Code Integrator User Prompt
- Helps with code integration and targeted editing.
- Important terms present: Question, Code, Instructions.
