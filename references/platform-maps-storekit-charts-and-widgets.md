---
title: Platform Maps, StoreKit, Charts, and Widgets
---

# Platform Maps, StoreKit, Charts, and Widgets

Apple reference material for StoreKit, MapKit, Charts, and widget-related platform updates bundled with Xcode Intelligence.

## Use This For
- Commerce, maps, charting, or widget work.
- visionOS widget questions.
- Requests that need newer Apple platform feature guidance outside the core UI and intelligence stacks.

## What To Apply
- Load the precise platform update doc rather than guessing from older framework knowledge.
- Keep the framework boundary clear across StoreKit, MapKit, Charts, and widget-specific APIs.

## Source Files Integrated
- `MapKit-GeoToolbox-PlaceDescriptors.md`
- `StoreKit-Updates.md`
- `Swift-Charts-3D-Visualization.md`
- `Widgets-for-visionOS.md`

### Map Kit Geo Toolbox Place Descriptors
- Use this when current MapKit place descriptor guidance matters.
- Apple topics covered: Using Place Descriptors with MapKit and GeoToolbox, Overview, Creating Place Descriptors, From an Address String, From Coordinates, From an MKMapItem, With Multiple Representations, Working with Place Representations, and 17 more.
- APIs and patterns present: GeoToolbox, PlaceDescriptor, PlaceRepresentation, SupportingPlaceRepresentation, .address, .coordinate, .coordinate(CLLocationCoordinate2D), .address(String), .representations, .coordinate(let coordinate), .latitude, .longitude, and 2 more.

### Store Kit Updates
- Use this when StoreKit behavior or new StoreKit APIs matter.
- Apple topics covered: StoreKit Updates, Overview, Core Framework Updates, AppTransaction Updates (iOS 18.4+), Transaction Updates (iOS 18.4+), RenewalInfo Updates (iOS 18.4+), StoreKit Views, SubscriptionOfferView, and 10 more.
- APIs and patterns present: AppTransaction, Transaction, Transaction.currentEntitlements(for:), Transaction.currentEntitlement(for:), appTransactionID, offerPeriod, advancedCommerceInfo, RenewalInfo, SubscriptionStatus, visibleRelationship, subscriptionStatusTask, LocalConfiguration.storekit, and 2 more.

### Swift Charts 3 D Visualization
- Use this when building or updating 3D Charts experiences.
- Apple topics covered: Using 3D Charts with Swift Charts, Overview, Basic Setup, Importing Required Frameworks, Creating a Simple 3D Chart, Creating a 3D Chart from Data, Customizing 3D Charts, Setting the Chart Pose (Viewing Angle), and 13 more.
- APIs and patterns present: Chart3D, SurfacePlot, Chart3DPose, Chart3DSurfaceStyle, .default, .front, .back, .top, .bottom, .right, .left, Chart3DCameraProjection, and 2 more.

### Widgets For Vision Os
- Use this when designing or implementing widgets for visionOS.
- Apple topics covered: Widgets for visionOS, Overview, Widget Mounting Styles, Widget Textures, Proximity Awareness, Supporting Widget Families, Rendering Modes, Complete Widget Example, and 4 more.
- APIs and patterns present: levelOfDetail, .default, .simplified, .systemExtraLarge, .systemExtraLargePortrait, showsWidgetContainerBackground, Preview, @Environment, .configurationDisplayName("Weather Widget"), .supportedMountingStyles([.elevated, .recessed]), .supportedMountingStyles([.recessed]), .configurationDisplayName("Caffeine Tracker"), and 2 more.
