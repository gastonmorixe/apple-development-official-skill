---
title: Apple Development Official Source Selection
---

# Source Selection

## Runtime Organization
- `references/` is flat and grouped by what each doc helps with: prompting, platform guidance, assistant wiring, and system context.
- Multiple Apple source files are intentionally merged into each runtime doc when that makes the guidance more usable for an agent.
- The runtime layout does not mirror Xcode bundle folders, `Contents`, `Resources`, plist filenames, or bundle names.

## Runtime Sources Included
- Xcode `*.idechatprompttemplate` files.
- Apple bundled markdown guides from `AdditionalDocumentation`.
- Xcode assistant metadata and onboarding sources when they materially explain behavior, consent, model pairing, or exposed tooling.
- System Apple Intelligence sources when they materially explain availability, policy, or telemetry vocabulary.

## Sources Excluded From Runtime References
- User-local `LOCAL_XCODE_CODINGASSISTANT_ROOT` files.
- Local Claude/Codex binaries and manifests.
- Local copies of helper skills such as `skill-creator` and `skill-installer`.

## Reason
- Those local files describe a particular machine's assistant installation, not Apple's platform-development guidance.
- They are kept in maintenance only so the skill can be updated deliberately when Apple changes what Xcode ships.
