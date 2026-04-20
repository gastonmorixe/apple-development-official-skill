---
title: Assistant Tools, Surfaces, and Actions
---

# Assistant Tools, Surfaces, and Actions

The Xcode surfaces and hooks exposed by `IDEIntelligenceChat.xcplugindata`: actions, commands, navigators, settings panes, preview surfaces, and evaluation verbs.

## Use This For
- Understanding what Xcode Intelligence can invoke or expose in the UI.
- Understanding the names of built-in Xcode assistant actions and commands.
- Understanding which evaluation and preview surfaces are present in the bundle.

## Stateless Actions
- `DocumentationSearch`.
- `XcodeGetCurrentFile`.
- `XcodeRefreshCodeIssuesInFile`.

## User-Facing Surfaces
- `Coding Assistant`.
- `Coding Assistant`.
- `Intelligence`.
- `Show Coding Tools…`.

## Evaluation Verbs
- `GetAgenticResponse`.
- `GetAssistantResponse`.
- `GetAssistantResponseWaitingForCompleteWorkspace`.
- `GetModels`.
- `GetQueryResponse`.
- `GetQueryResponseWaitingForCompleteWorkspace`.
- `Inference`.
- `ParseResponse`.
- `batchKeywordSearch`.
- `jsonDocumentVectorIndex`.
- `jsonDocumentVectorQuery`.
- `keywordSearch`.
- `modelSearchContext`.

## Provider and Steering Hooks
- `com.apple.dt.intelligence-chat.builtin-tool-rejection`.
- `IDESnapshotPreviewDomainProvider`.
- `IDESnapshotPreviewGeneratedContentProvider`.
- `IDEChatCodePreviewGeneratedContentProvider`.
- `IDEChatPreviewGalleryDomainProvider`.
- `IDESnapshotPreviewGalleryDomainProvider`.
- `IDEDefaultIntelligenceChatServiceProvider`.
- `IDEChatCodePreviewDomainProvider`.

## Source Files Integrated
- `IDEIntelligenceChat.xcplugindata`
