---
title: Platform Swift Language, Concurrency, and Data
---

# Platform Swift Language, Concurrency, and Data

Apple's current guidance around Swift Concurrency, InlineArray/Span, SwiftData inheritance, and Foundation attributed strings.

## Use This For
- Swift language feature adoption.
- Concurrency, data modeling, or Foundation text work.
- Requests that touch current Swift standard library or data-layer changes.

## What To Apply
- Prefer the language and data patterns Apple is actively documenting now.
- Keep Swift Concurrency guidance ahead of legacy async models.
- Preserve data-model and text-system terminology exactly where Apple has defined it.

## Source Files Integrated
- `Foundation-AttributedString-Updates.md`
- `Swift-Concurrency-Updates.md`
- `Swift-InlineArray-Span.md`
- `SwiftData-Class-Inheritance.md`

### Foundation Attributed String Updates
- Use this when current AttributedString behavior or APIs matter.
- Apple topics covered: Updates to AttributedString Support in Foundation, Overview, Core AttributedString Concepts, Creating AttributedStrings, Working with Attributes, Text Alignment and Formatting, TextAlignment Options, Writing Direction Support, and 6 more.
- APIs and patterns present: @Binding, @State, .range(of: "world"), .font, .boldSystemFont(ofSize: 16), .foregroundColor, .red, .backgroundColor, .yellow, .systemFont(ofSize: 14), .range(of: "Styled"), .underlineStyle, and 2 more.

### Swift Concurrency Updates
- Use this when updating concurrency patterns to current Swift guidance.
- Apple topics covered: Concurrent programming updates in Swift 6.2, Data-race safety, Global State, Offloading work to the background, An example, Summary.
- APIs and patterns present: PhotoProcessor, Sticker, extractSticker, Exportable, StickerModel, ImageExporter, @MainActor, extractSubject, @concurrent, .loadTransferable(type: Data.self), .photoProcessor, .extractSticker(data: data, with: item.itemIdentifier), and 2 more.

### Swift Inline Array Span
- Use this when new Swift standard library collection/storage features are in scope.
- Apple topics covered: Swift Standard Library: InlineArray and Span, Overview, InlineArray, What is InlineArray?, Declaration, Key Characteristics, Initialization, Memory Layout, and 16 more.
- APIs and patterns present: InlineArray, Span, @frozen, .size, .stride, .alignment, .append(4), .indices, .count, .isEmpty, .span, .self, and 2 more.

### Swift Data Class Inheritance
- Use this when SwiftData inheritance behavior matters.
- Apple topics covered: Adopting Class Inheritance in Swift Data, Overview, When to Use Inheritance in Swift Data, Good Use Cases, When to Avoid Inheritance, Designing Class Hierarchies, Base Class Design, Subclass Design, and 10 more.
- APIs and patterns present: BusinessTrip, Trip, @Model, @Attribute, @Relationship, @Query, .preserveValueOnDeletion, .cascade, .trip, .destination, .startDate, .endDate, and 2 more.
