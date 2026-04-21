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

## Privacy and Consent Text

You can choose to enable one or more third-party intelligence models when using Xcode. These models can help you answer coding questions and requests, such as to help you generate and modify code, tests, and documentation or to fix errors. You control when the models are used and must first enable a model before any of your information is shared. After enabling an intelligence model, you may also choose to install and use certain agentic coding tools with Xcode.

### Using Third-Party Models

Before any information is sent to a third-party model provider, you must enable a model in Intelligence in Xcode. By default, no models are enabled. Enabling a model allows you to send coding-related requests in Xcode to a third-party model provider. You can choose to disable a model at any time on your Mac by going to Xcode > Settings > Intelligence, tapping a model provider, then tapping to turn off the model in Xcode.

Your conversation history with models will be stored in Xcode, and you can view or delete them at any time.

### Data Provided to Third-Party Models

When using Intelligence in Xcode, you may choose what requests are sent to the third-party model provider. When you make a request, third-party models may have access to project-related information from Xcode, such as your project files and source code. The third-party model provider’s data privacy policies will apply. This means the provider may log your request, session history, and attachments, including your project’s files and sources, and may use this data to train or improve their models, unless you are using ChatGPT in Xcode without a ChatGPT account, as described below.

### ChatGPT in Xcode

You can choose to enable ChatGPT in Xcode (where available). Your data sent from Xcode will not be used by Apple Intelligence features on your system and will be connected only to the ChatGPT account used in Xcode.

### Data Provided to ChatGPT in Xcode

You may choose what requests to send to ChatGPT in Xcode. In addition to the data described in the Data Provided to Third-Party Models section above, limited data associated with the request, such as current time zone, country, device type, language, and feature being used when making the request, will be sent to ChatGPT to answer your request and enable ChatGPT to provide you accurate and relevant results.

When using ChatGPT in Xcode, your IP address is obscured from ChatGPT. Your general location, which is approximated by matching the IP address of your internet connection to a geographic region, is provided to ChatGPT for purposes such as enabling ChatGPT to prevent fraud and comply with applicable law.

### Using ChatGPT in Xcode Without an Account

If you enable ChatGPT in Xcode without being signed in to a ChatGPT account, only the data described in the Data Provided to Third-Party Models and Data Provided to ChatGPT in Xcode sections above will be sent to ChatGPT. OpenAI will not receive any data tied to your Apple Account. OpenAI must process your data solely for the purpose of fulfilling it and not store your request or any responses it provides, unless required under applicable laws. OpenAI also must not use your request to improve or train its models.

### Using ChatGPT in Xcode with a ChatGPT Account

You can choose to create a ChatGPT account or sign in to an existing account. If you are a ChatGPT subscriber, you will be able to access paid features from your Xcode experience.

When you are signed in, your ChatGPT account settings and OpenAI’s data privacy policies will apply. This means OpenAI may log your request, attachments, and session history, and use this data to train or improve their models. To learn more about OpenAI’s privacy practices, visit https://openai.com/policies/row-privacy-policy.

### Third-Party Agentic Coding Tools

After enabling a third-party model in Intelligence in Xcode, you may choose to install that third party’s agentic coding tool, where supported. Third-party agentic coding tools — whether installed through Xcode or other means, and accessed within Xcode, the command line, or other third-party clients — can be granted access to project information and Xcode’s capabilities through the Model Context Protocol (MCP). Project information includes but is not limited to source code, build settings, and target information. Capabilities include but are not limited to code searching, retrieving build logs, building source code, and arbitrary code execution. Agents launched from within Xcode are automatically granted this access, and agents launched by other clients are prompted for access in Xcode upon each invocation.
All access, use, and processing of data on your device, account, and systems, including within Xcode, by an agentic coding tool will be subject to the terms and conditions and privacy policies of that tool. This includes OpenAI’s agentic coding tool. None of the limitations referenced above in the Data Provided to ChatGPT in Xcode section are applicable when using the OpenAI agentic coding tool.

### Data Provided to Apple

When you use Intelligence in Xcode, Apple collects limited data about your requests to the model provider and the provider’s response, such as the number of requests sent, or the approximate size of the request or response, in order to operate the service, prevent fraud, and improve the feature.

If you take steps to upgrade your current ChatGPT plan through your Apple device, Apple may collect limited data about your interactions with the upgrade experience, such as views and clicks, in order to understand and improve the experience. This data is not tied to your Apple Account.

### Reporting a Concern

If you have an issue to report about Intelligence in Xcode, you may report it through Report a Concern. When you report a concern, you may make a separate choice to share information about the concern with Apple. For more information, visit www.apple.com/legal/privacy/data/en/report-concern.

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
