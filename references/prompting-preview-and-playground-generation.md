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

## Source Content

### Coding Tool Template Generate Playground

- Source file: `XCODE_RESOURCES/CodingToolTemplateGeneratePlayground.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

````text
I need you to create a Swift Playground to demonstrate and test the following code.
**File**: <file path>
**Lines**: <start line>-<end line>

[if selected code is available]
**Selected Code**:
```
<selected code>
```

[end if selected code is available]

Please use the file-reading tool to read the full file context if needed, then create a complete Swift #Playground that:
- Imports necessary frameworks
- Includes or recreates the selected code
- Provides example usage demonstrating how the code works
- Includes test cases or demonstrations of different scenarios
- Has clear comments explaining what's being tested

The playground should be self-contained and runnable, helping someone understand how to use this code.

To do this, you should use the modern `#Playground { }` syntax. Insert this code at the end of the file. An example of this syntax:

```swift

struct MyFunStruct {
    let name: String
}

#Playground {
    let funStruct = MyFunStruct(name: "Hello, world!")
    print(funStruct.name)
}

```
````

### Coding Tool Template Generate Preview

- Source file: `XCODE_RESOURCES/CodingToolTemplateGeneratePreview.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

````text
I need you to create a SwiftUI #Preview for the following code.

**File**: <file path>
**Lines**: <start line>-<end line>

[if selected code is available]
**Selected Code**:
```
<selected code>
```

[end if selected code is available]

Please use the file-reading tool to read the full file context if needed, then create a #Preview macro that demonstrates this SwiftUI View.

Follow these guidelines:
- Use the #Preview macro format: `#Preview { ... }`
- If the view has navigation modifiers (.navigation*, NavigationLink, .toolbar*, etc.), embed it in a NavigationStack
- If the view has list-related modifiers or ends with "Row", embed it in a List
- If the view takes a Binding, define it within the Preview using @Previewable
- Use static variables or globals when available instead of creating mock data
- Only add @available if required (e.g., when using @Previewable)

**Important**: After creating the #Preview code, use the code-editing tool to insert it at the end of the file. Add the preview code after the existing code with appropriate spacing.
````

### Generate Playground

- Source file: `XCODE_RESOURCES/GeneratePlayground.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

```text
Provide a brief example on how to use `<target symbol>`.
    - Respond only with a single code block.
    - Don't use comments.
    - Don't use print statements.
    - Don't import any additional modules.
```

### Generate Preview

- Source file: `XCODE_RESOURCES/GeneratePreview.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

````text
Your task is to create a Preview for a SwiftUI View and only return the code for the #Preview macro with no additional explanation.

The initializer for a #Preview is the following:

```
init(_ name: String? = nil, body: @escaping @MainActor () -> any View)
```

An example of one is:
```swift
#Preview {
    Text("Hello World!")
}
```

Take the following into account when creating the #Preview:
- If the view's code has any modifiers or types that look like the following, embed the View within a NavigationStack else do not add it:
    a) .navigation.*
    b) NavigationLink
    c) .toolbar.*
    d) .customizationBehavior
    e) .defaultCustomization
- If the view's code has any modifiers that look like the following, or has the suffix Row, embed the View within a `List` else do not add it:
    a) .listItemTint
    b) .listItemPlatterColor
    c) .listRowBackground
    d) .listRowInsets
    e) .listRowPlatterColor
    f) .listRowSeparatorTint
    g) .listRowSpacing
    h) .listSectionSeparatorTint
    i) .listSectionSpacing
    j) .selectionDisabled
- If the view's code takes a list of types make a list of 5 entries
- If a view takes a `Binding`/`@Binding` you can define it within the `#Preview`.
- Do not add @availability unless required. Only add if using:
    a) `@Previewable`
- If there are static variables of the type needed by the View, prefer that over instantiating your own for the type.
- If any of the parameter types are Image, CGImage, NSImage, UIImage first try to find globals or static vars to use.

The View to create the #Preview for is:
`<target symbol>`

Return the #Preview and no additional explanation. ALWAYS wrap the preview in triple-tick markdown code snippet marks.
````
