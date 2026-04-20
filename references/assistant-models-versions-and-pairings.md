---
title: Assistant Models, Versions, and Pairings
---

# Assistant Models, Versions, and Pairings

Apple's bundled model metadata for the Xcode coding assistant stack: build context, downloadable agent versions, and approved integration pairings.

## Use This For
- Understanding which agent binaries Apple references from the Xcode bundle.
- Understanding which model names map to which executor model inside Xcode.
- Tying the skill back to a specific Xcode/IDEIntelligenceChat build.

## Build Context
- `CFBundleIdentifier`: `com.apple.dt.IDEIntelligenceChat`.
- `CFBundleVersion`: `24899.2`.
- `DTXcodeBuild`: `17E201`.
- `DTSDKName`: `macosx26.4.internal`.
- `SourceVersion`: `24899002000000000`.

## Agent Packages Apple References
- `claude`: version `2.1.59`, checksum present, source host `storage.googleapis.com`.
- `codex`: version `0.106.0`, checksum present, source host `github.com`.

## Approved Integration Pairings
- `com.apple.openai.chatgpt`: executor -> gpt-4.1-mini.
- `gpt-4.1`: executor -> gpt-4.1-mini.
- `gpt-4.1-mini`: executor -> gpt-4.1-mini.
- `gpt-5`: executor -> gpt-4.1-mini.
- `o3`: executor -> gpt-4.1-mini.

## Source Files Integrated
- `AgentVersions.plist`
- `ApprovedIntegrationModelPairings.plist`
- `Info.plist`
- `version.plist`
