---
title: Assistant Onboarding and Privacy
---

# Assistant Onboarding and Privacy

Apple's onboarding, privacy, and user-consent text for Intelligence in Xcode, integrated into a single runtime reference instead of a mirrored bundle tree.

## Use This For
- Understanding what Apple tells the user about third-party models in Xcode.
- Understanding onboarding scope, supported platforms, and privacy boundaries.
- Understanding how Apple describes MCP access and agentic coding tool permissions.

## Bundle Context
- `CFBundleIdentifier`: `com.apple.onboarding.intelligencexcode`.
- `CFBundleVersion`: `24899.2`.
- `ProjectName`: `CodeIntelligence`.
- `ContentVersion`: `1`.
- `SupportedPlatforms`: macOS.

## Visible Onboarding Copy
- `SPLASH_TITLE`: Intelligence in Xcode & Privacy
- `SPLASH_SUMMARY`: Intelligence in Xcode is designed to put you in control and enable you to choose what to share.
- `BUTTON_TITLE`: About Intelligence in Xcode & Privacy…

## Privacy and Consent Sections
- Preamble: You can choose to enable one or more third-party intelligence models when using Xcode. These models can help you answer coding questions and requests, such as to help you generate and modify code, tests, and documentation or to fix errors. You control when the models are used and must first enable a model before any of your information is shared. After enabling an intelligence model, you may also choose to install and use certain agentic coding tools with Xcode.
- `Using Third-Party Models`: Before any information is sent to a third-party model provider, you must enable a model in Intelligence in Xcode.
- `Data Provided to Third-Party Models`: When using Intelligence in Xcode, you may choose what requests are sent to the third-party model provider.
- `ChatGPT in Xcode`: You can choose to enable ChatGPT in Xcode (where available).
- `Data Provided to ChatGPT in Xcode`: You may choose what requests to send to ChatGPT in Xcode.
- `Using ChatGPT in Xcode Without an Account`: If you enable ChatGPT in Xcode without being signed in to a ChatGPT account, only the data described in the Data Provided to Third-Party Models and Data Provided to ChatGPT in Xcode sections above will be sent to ChatGPT.
- `Using ChatGPT in Xcode with a ChatGPT Account`: You can choose to create a ChatGPT account or sign in to an existing account.
- `Third-Party Agentic Coding Tools`: After enabling a third-party model in Intelligence in Xcode, you may choose to install that third party’s agentic coding tool, where supported.
- `Data Provided to Apple`: When you use Intelligence in Xcode, Apple collects limited data about your requests to the model provider and the provider’s response, such as the number of requests sent, or the approximate size of the request or response, in order to operate the service, prevent fraud, and improve the feature.

If you take steps to upgrade your current ChatGPT plan through your Apple device, Apple may collect limited data about your interactions with the upgrade experience, such as views and clicks, in order to understand and improve the experience.
- `Reporting a Concern`: If you have an issue to report about Intelligence in Xcode, you may report it through Report a Concern.

## Operational Rules Apple States Explicitly
- No model is enabled by default; the user must enable a model before information is shared.
- Conversation history is stored in Xcode and can be viewed or deleted.
- Xcode may send project files and source code to third-party models when the user makes a request.
- Xcode describes MCP-based agentic coding tools as having access to project information and Xcode capabilities, including build and code execution surfaces.
- Apple distinguishes ChatGPT without an account from ChatGPT with an account, and says different OpenAI data-handling terms apply.

## Source Files Integrated
- `XCODE_ONBOARDING_CONTENTS/Info.plist`
- `XCODE_ONBOARDING_CONTENTS/version.plist`
- `XCODE_ONBOARDING_RESOURCES/IntelligenceInXcode.plist`
- `XCODE_ONBOARDING_RESOURCES/en.lproj/IntelligenceInXcode.strings`
