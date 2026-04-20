---
title: Platform FoundationModels, Intents, and Intelligence
---

# Platform FoundationModels, Intents, and Intelligence

Apple guidance around FoundationModels, AppIntents, Visual Intelligence, and related system-facing intelligence features.

## Use This For
- On-device model integration with FoundationModels.
- AppIntents, shortcuts-style behavior, or system intelligence features.
- Visual Intelligence or Assistive Access related work.

## What To Apply
- Treat FoundationModels as its own modern Apple framework with structured generation support.
- Keep AppIntents and Visual Intelligence aligned with Apple platform affordances instead of generic LLM patterns.
- Preserve accessibility-facing constraints when Assistive Access guidance is relevant.

## Source Files Integrated
- `AppIntents-Updates.md`
- `FoundationModels-Using-on-device-LLM-in-your-app.md`
- `Implementing-Assistive-Access-in-iOS.md`
- `Implementing-Visual-Intelligence-in-iOS.md`

### App Intents Updates
- Use this when current AppIntents capabilities matter.
- Apple topics covered: AppIntents Updates, Overview, New System Integrations, Visual Intelligence Integration, Onscreen Entities, User Experience Refinements, Intent Modes, Continuing in Foreground, and 15 more.
- APIs and patterns present: supportedModes, .background, .foreground(.immediate), .foreground(.dynamic), .foreground(.deferred), [.background, .foreground], [.background, .foreground(.dynamic)], [.background, .foreground(.deferred)], @ComputedProperty, @DeferredProperty, @UnionValue, @Parameter, and 2 more.

### Foundation Models Using On Device Llm In Your App
- Use this when integrating on-device model workflows with FoundationModels.
- Apple topics covered: Foundation Models: Using Apple's On-Device LLM in Your Apps, Overview, Getting Started, Check Model Availability, Create a Session, Basic Usage, Provide Instructions to the Model, Provide a Prompt to the Model, and 18 more.
- APIs and patterns present: LanguageModelSession, isResponding, @Generable, PartiallyGenerated, LanguageModelSession.GenerationError.exceededContextWindowSize, GenerationOptions, Transcript, @Guide, .default, .availability, .available, .unavailable(.deviceNotEligible), and 2 more.

### Implementing Assistive Access In I Os
- Use this when Assistive Access constraints affect the implementation.
- Apple topics covered: Implementing Assistive Access in iOS, Overview, Setting Up Assistive Access in Your App, 1. Enable Assistive Access Support, 2. Full Screen Support (Optional), Creating an Assistive Access Scene, SwiftUI Implementation, Preview(traits: .assistiveAccess), and 8 more.
- APIs and patterns present: Info.plist, AssistiveAccess, .assistiveAccess, @main, @Environment, .navigationTitle("My App"), .ConnectionOptions, .role, .windowAssistiveAccessApplication, .delegateClass, .self, .accessibilityAssistiveAccessEnabled, and 2 more.

### Implementing Visual Intelligence In I Os
- Use this when implementing Visual Intelligence features in iOS.
- Apple topics covered: Implementing Visual Intelligence in iOS, Overview, Setting Up Visual Intelligence, Required Frameworks, Implementation Steps, Working with SemanticContentDescriptor, Key Properties, Accessing Visual Data, and 13 more.
- APIs and patterns present: IntentValueQuery, SemanticContentDescriptor, DisplayRepresentation, AppEntity, @Dependency, @UnionValue, @Parameter, .pixelBuffer, .search(matching: pixelBuffer), .int, .init(named: landmark.thumbnailImageName), .result(), and 2 more.
