---
title: Prompting Preview and Playground Generation
---

# Prompting Preview and Playground Generation

How Xcode asks for `#Preview` output, preview wrapping rules, and playground scaffolding.

## Use This For
- Preview generation or preview repair tasks.
- SwiftUI examples that need `#Preview` blocks.
- Playground generation or minimal runnable demonstration code.

## What To Apply
- Use `#Preview` for new SwiftUI previews.
- Wrap previews in `NavigationStack` or `List` only when the source view implies that context.
- Return code-only output when the source prompt explicitly requires it.
- Prefer small runnable examples for playground-style generation.

## Source Files Integrated
- `CodingToolTemplateGeneratePlayground.idechatprompttemplate`
- `CodingToolTemplateGeneratePreview.idechatprompttemplate`
- `GeneratePlayground.idechatprompttemplate`
- `GeneratePreview.idechatprompttemplate`

### Coding Tool Template Generate Playground
- Helps with playground generation.
- Source anchors: Playground {.
- Important terms present: Swift, Playground, Selected, Code, Please, XcodeRead, Imports, Includes, Provides, Has.

### Coding Tool Template Generate Preview
- Helps with preview generation.
- Carry forward: Assume SwiftUI patterns may have evolved and favor current Apple-native approaches.; Use `#Preview` for modern SwiftUI preview generation when the template is preview-related.; Add `NavigationStack` only when the source view or task implies navigation context.; Add `List` only when the source view or task implies list or row context..
- Important terms present: @Previewable, @available, .navigation, .toolbar, SwiftUI, Preview, Selected, Code, Please, XcodeRead.

### Generate Playground
- Helps with playground generation.

### Generate Preview
- Helps with preview generation.
- Carry forward: Assume SwiftUI patterns may have evolved and favor current Apple-native approaches.; Use `#Preview` for modern SwiftUI preview generation when the template is preview-related.; Add `NavigationStack` only when the source view or task implies navigation context.; Add `List` only when the source view or task implies list or row context.; Return code only when the prompt explicitly requires a code-only answer..
- Source anchors: Preview {.
- Important terms present: List, Binding, @Binding, #Preview, @Previewable, @escaping, @MainActor, @availability, .navigation, .toolbar.
