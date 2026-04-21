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

## Source Content

### Additional Files

- Source file: `XCODE_RESOURCES/AdditionalFiles.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

````text
The user has also provided the following Swift files that may be useful to answer their question:

[repeat for each additional file in additional files]

```<additional file language>:<additional file file name>
<additional file code>
```

[end repeat for each additional file in additional files]
````

### Agent Additional Context

- Source file: `XCODE_RESOURCES/AgentAdditionalContext.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

```text
[if project structure is available]
Project structure:
<project structure>
[end if project structure is available]

[if current file is available]

The user is currently inside this file: <current file file path>
[if current file selection is available]

The user has selected the following code from that file (lines <current file selection start line>-<current file selection end line>):
<current file selection text>
[otherwise]

The user has no code selected.
[end if current file selection is available]

[otherwise]

The user has no file currently open.
[end if current file is available]
```

### Context Items

- Source file: `XCODE_RESOURCES/ContextItems.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

````text
The user has provided the following miscellaneous context that may be useful to answer their question:

[repeat for each context item in context items]

```
<context item code>
```

[end repeat for each context item in context items]
````

### Current File

- Source file: `XCODE_RESOURCES/CurrentFile.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

````text
The user is currently inside this file: <current file file name>
The contents are below:
```<current file language>:<current file file name>
<current file code>
```
````

### Current File Abbreviated

- Source file: `XCODE_RESOURCES/CurrentFileAbbreviated.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

```text
The user is currently inside this file: <current file file name>
Unfortunately, this file is too big to read in full. Doing so will consume your entire context window. `<current file file name>` is <current file line count> lines long.

Instead of seeing the whole file now, try using your file-viewing tool to view smaller line ranges of the file, looking for the information you need to do your job.
```

### Current File Name

- Source file: `XCODE_RESOURCES/CurrentFileName.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

```text
The user is currently inside this file: <current file name>
```

### Current Selection

- Source file: `XCODE_RESOURCES/CurrentSelection.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

````text
The user has selected the following code from that file:
```<selection language>
<selection code>
```
````

### Issues

- Source file: `XCODE_RESOURCES/Issues.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

```text
The following issues have been reported in the code:

[repeat for each issue in issues]

<issue severity>: <issue message>

[end repeat for each issue in issues]
```

### New Knowledge

- Source file: `XCODE_RESOURCES/NewKnowledge.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

```text
Use the following retrieved context as accurate information, even if it includes APIs or code the model may not know:
<new knowledge content>
```

### No Selection

- Source file: `XCODE_RESOURCES/NoSelection.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

```text
The user has no code selected.
```

### Original File

- Source file: `XCODE_RESOURCES/OriginalFile.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

````text
```<original language>:<original file name>
<source code>
```
````

### Search Results

- Source file: `XCODE_RESOURCES/SearchResults.idechatprompttemplate`

- Rendering: adapted from Apple template syntax for skill use.

````text
Your search results are provided below:

[repeat for each file result in file results]

```<file result language>:<file result file name>
<file result code>
```

[end repeat for each file result in file results]

<message>
````
