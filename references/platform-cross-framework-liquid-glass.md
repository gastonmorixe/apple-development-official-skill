---
title: Platform Cross-Framework Liquid Glass
---

# Platform Cross-Framework Liquid Glass

How Apple frames Liquid Glass across UIKit, AppKit, and WidgetKit rather than only in SwiftUI.

## Use This For
- Liquid Glass adoption outside SwiftUI.
- Cross-framework Apple UI work involving UIKit, AppKit, or WidgetKit.
- Cases where the same design system needs to be applied in multiple Apple UI stacks.

## What To Apply
- Keep the framework boundary clear: UIKit, AppKit, and WidgetKit each expose their own Liquid Glass surface area.
- Reuse the design-system intent across frameworks without assuming API parity.

## Source Files Integrated
- `AppKit-Implementing-Liquid-Glass-Design.md`
- `UIKit-Implementing-Liquid-Glass-Design.md`
- `WidgetKit-Implementing-Liquid-Glass-Design.md`

### AppKit Implementing Liquid Glass Design
- Use this when implementing Liquid Glass in AppKit on macOS.
- Apple topics covered: Implementing Liquid Glass Design in AppKit, Overview, Key Classes, NSGlassEffectView, NSGlassEffectContainerView, Basic Implementation, Creating a Simple Glass Effect View, Customizing Glass Effect Views, and 13 more.
- APIs and patterns present: NSGlassEffectView, NSGlassEffectContainerView, cornerRadius, tintColor, @MainActor, @objc, .viewDidLoad(), .translatesAutoresizingMaskIntoConstraints, .font, .systemFont(ofSize: 16, weight: .medium), .textColor, .white, and 2 more.

### Uikit Implementing Liquid Glass Design
- Use this when implementing Liquid Glass in UIKit instead of SwiftUI.
- Apple topics covered: Implementing Liquid Glass Design in UIKit, Overview, Basic Implementation, Creating a Simple Glass Effect, Customizing the Glass Effect, Interactive Glass Effects, Combining Multiple Glass Elements, Scroll View Edge Effects, and 6 more.
- APIs and patterns present: UIVisualEffectView, UIGlassEffect, UIGlassContainerEffect, .automatic, .hard, .frame, .layer, .cornerRadius, .clipsToBounds, .text, .textAlignment, .center, and 2 more.

### WidgetKit Implementing Liquid Glass Design
- Use this when applying Liquid Glass concepts in WidgetKit.
- Apple topics covered: Implementing Liquid Glass Design in Widgets, Overview, Understanding Widget Rendering Modes, Full Color Mode, Accented Mode, Supporting Liquid Glass in Widgets, Container Backgrounds for Widgets, Optimizing Widget Appearance, and 11 more.
- APIs and patterns present: widgetRenderingMode, widgetAccentable(_:), WidgetAccentedRenderingMode, fullColor, .glass, .paper, .recessed, .elevated, levelOfDetail, @Environment, .widgetRenderingMode, .accented, and 2 more.
