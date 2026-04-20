---
title: Prompting Context, Search, and Selection
---

# Prompting Context, Search, and Selection

How Xcode assembles current file context, search results, issues, selections, and supporting files around a request.

## Use This For
- Requests that depend on current file or current selection context.
- Tasks that need issue lists, search results, or additional files.
- Situations where the agent should understand what Xcode provides before answering.

## What To Apply
- Respect the difference between full-file, abbreviated-file, filename-only, and selection-only context.
- Treat issues and search results as structured context inputs, not narrative prose.
- Use no-selection and original-file variants to understand fallback and comparison behavior.

## Source Files Integrated
- `AdditionalFiles.idechatprompttemplate`
- `AgentAdditionalContext.idechatprompttemplate`
- `ContextItems.idechatprompttemplate`
- `CurrentFile.idechatprompttemplate`
- `CurrentFileAbbreviated.idechatprompttemplate`
- `CurrentFileName.idechatprompttemplate`
- `CurrentSelection.idechatprompttemplate`
- `Issues.idechatprompttemplate`
- `NewKnowledge.idechatprompttemplate`
- `NoSelection.idechatprompttemplate`
- `OriginalFile.idechatprompttemplate`
- `SearchResults.idechatprompttemplate`

### Additional Files
- Helps with context assembly around the user's current workspace state.
- Important terms present: .language, .fileName, .code, The, Swift.

### Agent Additional Context
- Helps with base system prompting and reasoning.
- Important terms present: .filePath, .selection, .startLine, .endLine, .text, Project, The.

### Context Items
- Helps with base system prompting and reasoning.
- Important terms present: .code, The.

### Current File
- Helps with context assembly around the user's current workspace state.
- Important terms present: .fileName, .language, .code, The.

### Current File Abbreviated
- Helps with context assembly around the user's current workspace state.
- Important terms present: .fileName, .lineCount, The, Unfortunately, Doing, Instead.

### Current File Name
- Helps with context assembly around the user's current workspace state.
- Important terms present: The.

### Current Selection
- Helps with context assembly around the user's current workspace state.
- Important terms present: .language, .code, The.

### Issues
- Helps with context assembly around the user's current workspace state.
- Important terms present: .severity, .message, The.

### New Knowledge
- Helps with base system prompting and reasoning.
- Important terms present: Use, APIs.

### No Selection
- Helps with context assembly around the user's current workspace state.
- Important terms present: The.

### Original File
- Helps with base system prompting and reasoning.
- Important terms present: .language, .fileName.

### Search Results
- Helps with context assembly around the user's current workspace state.
- Important terms present: .language, .fileName, .code, Your.
