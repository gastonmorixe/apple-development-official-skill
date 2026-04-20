---
title: Prompting Query, Response, and Titles
---

# Prompting Query, Response, and Titles

How Xcode shapes ordinary chat responses, short and detailed query behavior, naming, and lightweight explanation flows.

## Use This For
- Ordinary coding questions and conversational responses.
- Title generation and response-shaping behavior.
- Situations where Xcode wants concise or tool-aware query handling.

## What To Apply
- Keep answers direct and task-focused.
- Use the detailed guideline variant when the request needs more structure or explicit tool behavior.
- Treat titles, snippets, and interface-oriented prompt fragments as response-shaping helpers rather than separate workflows.

## Source Files Integrated
- `ChatTitleResolver.idechatprompttemplate`
- `InQueryDetailedGuidelines.idechatprompttemplate`
- `InQueryShortGuidelines.idechatprompttemplate`
- `Interfaces.idechatprompttemplate`
- `Query.idechatprompttemplate`
- `Snippets.idechatprompttemplate`
- `ToolAssistedInQueryDetailedGuidelines.idechatprompttemplate`
- `ToolAssistedInQueryShortGuidelines.idechatprompttemplate`

### Chat Title Resolver
- Helps with query handling and response shaping.
- Carry forward: Assume SwiftUI patterns may have evolved and favor current Apple-native approaches..
- Important terms present: You, Apple, When, JSON, This, For, How, The, Since, SwiftUI.

### In Query Detailed Guidelines
- Helps with query handling and response shaping.
- Important terms present: .swift, Guidelines, When, Whenever, To, It, For, FooBar.swift, Do, However.

### In Query Short Guidelines
- Helps with query handling and response shaping.
- Important terms present: If, Answer, English.

### Interfaces
- Helps with query handling and response shaping.
- Important terms present: .language, .code, The, Swift.

### Query
- Helps with query handling and response shaping.
- Important terms present: The.

### Snippets
- Helps with query handling and response shaping.
- Important terms present: .language, .code, The.

### Tool Assisted In Query Detailed Guidelines
- Helps with query handling and response shaping.
- Source anchors: SEARCH: TypeName1, SEARCH: a phrase or set of keywords to search for.
- Important terms present: .swift, Guidelines, Do, Briefly, Search, Use, SEARCH, TypeName1, When, Whenever.

### Tool Assisted In Query Short Guidelines
- Helps with query handling and response shaping.
- Important terms present: If, Answer, English.
