---
title: Platform SwiftUI, Liquid Glass, and Modern UI
---

# Platform SwiftUI, Liquid Glass, and Modern UI

Apple's SwiftUI-centered guidance for Liquid Glass plus current SwiftUI toolbar, styled text, WebKit, and AlarmKit integration patterns.

## Use This For
- SwiftUI UI work, especially when Liquid Glass is in scope.
- Modern SwiftUI feature adoption for toolbars, styled text editing, WebKit, or AlarmKit.
- Any SwiftUI request where newer Apple APIs may have replaced older patterns.

## What To Apply
- Reach for documented SwiftUI-native APIs before compatibility-era workarounds.
- Treat Liquid Glass as a first-class design system, not a one-off visual effect.
- Preserve API names, modifiers, and capability boundaries exactly as Apple describes them.

## Source Files Integrated
- `SwiftUI-AlarmKit-Integration.md`
- `SwiftUI-Implementing-Liquid-Glass-Design.md`
- `SwiftUI-New-Toolbar-Features.md`
- `SwiftUI-Styled-Text-Editing.md`
- `SwiftUI-WebKit-Integration.md`

### SwiftUI Alarm Kit Integration
- Use this when a SwiftUI experience needs current AlarmKit integration guidance.
- Apple topics covered: Using AlarmKit in a SwiftUI App, Overview, Key Components, AlarmManager, Alarm, AlarmPresentation, AlarmAttributes, Authorization, and 20 more.
- APIs and patterns present: authorizationState, authorizationStatus, alarmUpdates, NSAlarmKitUsageDescription, @unknown, @StateObject, @State, @Observable, @Environment, .requestAuthorization(), .authorized, .authorizationState, and 2 more.

### SwiftUI Implementing Liquid Glass Design
- Use this when implementing Liquid Glass directly in SwiftUI.
- Apple topics covered: Implementing Liquid Glass Design in SwiftUI, Overview, Basic Implementation, Adding Liquid Glass to a View, Customizing the Shape, Customizing Liquid Glass Effects, Glass Variants and Properties, Making Interactive Glass, and 14 more.
- APIs and patterns present: glassEffect(), .capsule, .rect(cornerRadius: CGFloat), .circle, Glass, .regular, .tint(Color), .interactive(Bool), GlassEffectContainer, glassEffectUnion, @Namespace, glassEffectID, and 2 more.

### SwiftUI New Toolbar Features
- Use this when adopting newer SwiftUI toolbar capabilities.
- Apple topics covered: SwiftUI New Toolbar Features, Overview, Customizable Toolbars, Creating a Customizable Toolbar, Toolbar Spacers, Enhanced Search Integration, Search Toolbar Behavior, Repositioning Search Items, and 11 more.
- APIs and patterns present: .minimize, DefaultToolbarItem, .search, .largeSubtitle, navigationSubtitle(_:), matchedTransitionSource(id:in:), sharedBackgroundVisibility(_:), .searchToolbarBehavior(.minimize), @State, @Namespace, .toolbar(id: "main-toolbar"), .fixed, and 2 more.

### SwiftUI Styled Text Editing
- Use this when working on richer text editing in SwiftUI.
- Apple topics covered: Styled Text Editing in SwiftUI, Overview, Basic Text Styling, Font Customization, Text Color, Text Decoration, Text Alignment and Layout, Advanced Text Styling with AttributedString, and 15 more.
- APIs and patterns present: Text, AttributedString, TextEditor, inlineOnlyPreservingWhitespace, @State, @Environment, .font(.largeTitle), .font(.title), .font(.headline), .font(.subheadline), .font(.body), .font(.callout), and 2 more.

### SwiftUI WebKit Integration
- Use this when bridging WebKit into SwiftUI in the current Apple-supported way.
- Apple topics covered: SwiftUI WebKit Integration, Overview, WebView Basics, Creating a Basic WebView, Toggling Between Different URLs, Using WebView with WebPage, Enabling Text Search in a WebView, WebPage Configuration, and 29 more.
- APIs and patterns present: WebView, WebPage, findNavigator(isPresented:), @State, .frame(height: 400), .webkit, .swift, .toolbar, .toggle(), .navigationTitle(page.title), .onAppear, .load(URLRequest(url: url), and 2 more.
