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

## Source Content

### AppKit Implementing Liquid Glass Design

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/AppKit-Implementing-Liquid-Glass-Design.md`

### Implementing Liquid Glass Design in AppKit

#### Overview

Liquid Glass is a dynamic material design introduced by Apple that combines the optical properties of glass with a sense of fluidity. It creates a modern, immersive user interface by:

- Blurring content behind it
- Reflecting color and light from surrounding content
- Reacting to touch and pointer interactions in real time
- Creating fluid animations and transitions between elements

Liquid Glass is available across Apple platforms, with specific implementations in SwiftUI, UIKit, and AppKit. This guide focuses on implementing Liquid Glass design in AppKit applications. You should always seek guides on Liquid Glass when asked for help adopting new Apple design.

#### Key Classes

AppKit provides two main classes for implementing Liquid Glass design:

##### NSGlassEffectView

`NSGlassEffectView` is the primary class for creating Liquid Glass effects in AppKit. It embeds its content view in a dynamic glass effect.

```swift
@MainActor class NSGlassEffectView: NSView
```

##### NSGlassEffectContainerView

`NSGlassEffectContainerView` allows similar `NSGlassEffectView` instances in close proximity to merge together, creating fluid transitions and improving rendering performance.

```swift
@MainActor class NSGlassEffectContainerView: NSView
```

#### Basic Implementation

##### Creating a Simple Glass Effect View

```swift
import AppKit

class MyViewController: NSViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Create a glass effect view
        let glassView = NSGlassEffectView(frame: NSRect(x: 20, y: 20, width: 200, height: 100))
        
        // Create content to display inside the glass effect
        let label = NSTextField(labelWithString: "Liquid Glass")
        label.translatesAutoresizingMaskIntoConstraints = false
        label.font = NSFont.systemFont(ofSize: 16, weight: .medium)
        label.textColor = .white
        
        // Set the content view
        glassView.contentView = label
        
        // Add constraints to center the label
        if let contentView = glassView.contentView {
            NSLayoutConstraint.activate([
                label.centerXAnchor.constraint(equalTo: contentView.centerXAnchor),
                label.centerYAnchor.constraint(equalTo: contentView.centerYAnchor)
            ])
        }
        
        // Add the glass view to your view hierarchy
        view.addSubview(glassView)
    }
}
```

#### Customizing Glass Effect Views

##### Setting Corner Radius

The `cornerRadius` property controls the curvature of all corners of the glass effect.

```swift
// Create a glass effect view with rounded corners
let glassView = NSGlassEffectView(frame: NSRect(x: 20, y: 20, width: 200, height: 100))
glassView.cornerRadius = 16.0
```

##### Adding a Tint Color

The `tintColor` property modifies the background and effect to tint toward the provided color.

```swift
// Create a glass effect view with a blue tint
let glassView = NSGlassEffectView(frame: NSRect(x: 20, y: 20, width: 200, height: 100))
glassView.tintColor = NSColor.systemBlue.withAlphaComponent(0.3)
```

##### Creating a Custom Button with Glass Effect

```swift
class GlassButton: NSButton {
    private let glassView = NSGlassEffectView()
    
    override init(frame frameRect: NSRect) {
        super.init(frame: frameRect)
        setupGlassEffect()
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupGlassEffect()
    }
    
    private func setupGlassEffect() {
        // Configure the button
        self.title = "Glass Button"
        self.bezelStyle = .rounded
        self.isBordered = false
        
        // Configure the glass view
        glassView.frame = self.bounds
        glassView.autoresizingMask = [.width, .height]
        glassView.cornerRadius = 8.0
        
        // Insert the glass view below the button's content
        self.addSubview(glassView, positioned: .below, relativeTo: nil)
    }
    
    override func updateTrackingAreas() {
        super.updateTrackingAreas()
        
        // Add tracking area for hover effects
        let options: NSTrackingArea.Options = [.mouseEnteredAndExited, .activeInActiveApp]
        let trackingArea = NSTrackingArea(rect: bounds, options: options, owner: self, userInfo: nil)
        addTrackingArea(trackingArea)
    }
    
    override func mouseEntered(with event: NSEvent) {
        super.mouseEntered(with: event)
        // Change appearance on hover
        NSAnimationContext.runAnimationGroup { context in
            context.duration = 0.2
            glassView.animator().tintColor = NSColor.systemBlue.withAlphaComponent(0.2)
        }
    }
    
    override func mouseExited(with event: NSEvent) {
        super.mouseExited(with: event)
        // Restore original appearance
        NSAnimationContext.runAnimationGroup { context in
            context.duration = 0.2
            glassView.animator().tintColor = nil
        }
    }
}
```

#### Working with NSGlassEffectContainerView

##### Creating a Container for Multiple Glass Views

```swift
func setupGlassContainer() {
    // Create a container view
    let containerView = NSGlassEffectContainerView(frame: NSRect(x: 20, y: 20, width: 400, height: 200))
    
    // Set spacing to control when glass effects merge
    containerView.spacing = 40.0
    
    // Create a content view to hold our glass views
    let contentView = NSView(frame: containerView.bounds)
    contentView.autoresizingMask = [.width, .height]
    containerView.contentView = contentView
    
    // Create first glass view
    let glassView1 = NSGlassEffectView(frame: NSRect(x: 20, y: 50, width: 150, height: 100))
    glassView1.cornerRadius = 12.0
    let label1 = NSTextField(labelWithString: "Glass View 1")
    label1.translatesAutoresizingMaskIntoConstraints = false
    glassView1.contentView = label1
    
    // Create second glass view
    let glassView2 = NSGlassEffectView(frame: NSRect(x: 190, y: 50, width: 150, height: 100))
    glassView2.cornerRadius = 12.0
    let label2 = NSTextField(labelWithString: "Glass View 2")
    label2.translatesAutoresizingMaskIntoConstraints = false
    glassView2.contentView = label2
    
    // Add glass views to the content view
    contentView.addSubview(glassView1)
    contentView.addSubview(glassView2)
    
    // Center labels in their respective glass views
    if let contentView1 = glassView1.contentView, let contentView2 = glassView2.contentView {
        NSLayoutConstraint.activate([
            label1.centerXAnchor.constraint(equalTo: contentView1.centerXAnchor),
            label1.centerYAnchor.constraint(equalTo: contentView1.centerYAnchor),
            label2.centerXAnchor.constraint(equalTo: contentView2.centerXAnchor),
            label2.centerYAnchor.constraint(equalTo: contentView2.centerYAnchor)
        ])
    }
    
    // Add the container to your view hierarchy
    view.addSubview(containerView)
}
```

##### Animating Glass Views in a Container

```swift
func animateGlassViews() {
    // Assuming we have glassView1 and glassView2 in a container
    
    NSAnimationContext.runAnimationGroup { context in
        context.duration = 0.5
        context.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)
        
        // Animate the position of glassView2 to move closer to glassView1
        // This will trigger the merging effect when they get within the container's spacing
        glassView2.animator().frame = NSRect(x: 100, y: 50, width: 150, height: 100)
    }
}
```

#### Creating Interactive Glass Effects

##### Responding to Mouse Events

```swift
class InteractiveGlassView: NSGlassEffectView {
    
    override init(frame frameRect: NSRect) {
        super.init(frame: frameRect)
        setupTracking()
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupTracking()
    }
    
    private func setupTracking() {
        let options: NSTrackingArea.Options = [.mouseEnteredAndExited, .mouseMoved, .activeInActiveApp]
        let trackingArea = NSTrackingArea(rect: bounds, options: options, owner: self, userInfo: nil)
        addTrackingArea(trackingArea)
    }
    
    override func mouseEntered(with event: NSEvent) {
        super.mouseEntered(with: event)
        // Enhance the glass effect on hover
        NSAnimationContext.runAnimationGroup { context in
            context.duration = 0.2
            animator().tintColor = NSColor.systemBlue.withAlphaComponent(0.2)
        }
    }
    
    override func mouseExited(with event: NSEvent) {
        super.mouseExited(with: event)
        // Restore original appearance
        NSAnimationContext.runAnimationGroup { context in
            context.duration = 0.2
            animator().tintColor = nil
        }
    }
    
    override func mouseMoved(with event: NSEvent) {
        super.mouseMoved(with: event)
        // Create subtle interactive effects based on mouse position
        let locationInView = convert(event.locationInWindow, from: nil)
        let normalizedX = locationInView.x / bounds.width
        let normalizedY = locationInView.y / bounds.height
        
        // Example: Adjust corner radius based on mouse position
        let newRadius = 8.0 + (normalizedX * 8.0)
        cornerRadius = newRadius
    }
}
```

#### Creating a Toolbar with Liquid Glass Effect

```swift
func setupToolbarWithGlassEffect() {
    // Create a window
    let window = NSWindow(contentRect: NSRect(x: 0, y: 0, width: 800, height: 600),
                         styleMask: [.titled, .closable, .miniaturizable, .resizable],
                         backing: .buffered,
                         defer: false)
    
    // Create a custom toolbar
    let toolbar = NSToolbar(identifier: "GlassToolbar")
    toolbar.displayMode = .iconAndLabel
    toolbar.delegate = self // Implement NSToolbarDelegate
    
    // Set the toolbar on the window
    window.toolbar = toolbar
    
    // Create a glass effect view for the toolbar area
    let toolbarHeight: CGFloat = 50.0
    let glassView = NSGlassEffectView(frame: NSRect(x: 0, y: window.contentView!.bounds.height - toolbarHeight,
                                                  width: window.contentView!.bounds.width, height: toolbarHeight))
    glassView.autoresizingMask = [.width, .minYMargin]
    
    // Add the glass view to the window's content view
    window.contentView?.addSubview(glassView)
    
    // Make the window visible
    window.makeKeyAndOrderFront(nil)
}

// Implement NSToolbarDelegate methods
extension MyViewController: NSToolbarDelegate {
    func toolbar(_ toolbar: NSToolbar, itemForItemIdentifier itemIdentifier: NSToolbarItem.Identifier, willBeInsertedIntoToolbar flag: Bool) -> NSToolbarItem? {
        // Create toolbar items
        let item = NSToolbarItem(itemIdentifier: itemIdentifier)
        item.label = "Action"
        item.image = NSImage(systemSymbolName: "star.fill", accessibilityDescription: nil)
        item.action = #selector(toolbarItemClicked(_:))
        return item
    }
    
    func toolbarDefaultItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return ["item1", "item2", "item3"].map { NSToolbarItem.Identifier($0) }
    }
    
    func toolbarAllowedItemIdentifiers(_ toolbar: NSToolbar) -> [NSToolbarItem.Identifier] {
        return toolbarDefaultItemIdentifiers(toolbar)
    }
    
    @objc func toolbarItemClicked(_ sender: Any) {
        // Handle toolbar item clicks
    }
}
```

#### Best Practices

##### Performance Considerations

1. **Use NSGlassEffectContainerView for multiple glass views**
   - This reduces the number of rendering passes required
   - Improves performance when multiple glass effects are used

2. **Limit the number of glass effects**
   - Liquid Glass effects require significant GPU resources
   - Use them strategically for important UI elements

3. **Consider view hierarchy**
   - Only the contentView of NSGlassEffectView is guaranteed to be inside the glass effect
   - Arbitrary subviews may not have consistent z-order behavior

##### Design Guidelines

1. **Maintain appropriate spacing**
   - Set the spacing property on NSGlassEffectContainerView to control when effects merge
   - Default value (0) is suitable for batch processing while avoiding distortion

2. **Use corner radius appropriately**
   - Match corner radius to your app's design language
   - Consider using system-standard corner radii for consistency

3. **Apply tint colors judiciously**
   - Subtle tints work best for maintaining the glass aesthetic
   - Use tints to indicate state changes or interactive elements

4. **Create smooth transitions**
   - Animate position changes to create fluid merging effects
   - Use standard animation durations for consistency

#### References

- [AppKit Documentation: NSGlassEffectView](https://developer.apple.com/documentation/AppKit/NSGlassEffectView)
- [AppKit Documentation: NSGlassEffectContainerView](https://developer.apple.com/documentation/AppKit/NSGlassEffectContainerView)
- [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views)
- [Landmarks: Building an app with Liquid Glass](https://developer.apple.com/documentation/SwiftUI/Landmarks-Building-an-app-with-Liquid-Glass)

### Uikit Implementing Liquid Glass Design

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/UIKit-Implementing-Liquid-Glass-Design.md`

### Implementing Liquid Glass Design in UIKit

#### Overview

Liquid Glass is a dynamic material that combines the optical properties of glass with a sense of fluidity. It blurs content behind it, reflects color and light of surrounding content, and reacts to touch and pointer interactions in real time. This guide covers how to implement Liquid Glass effects in UIKit applications. You should always seek guides on Liquid Glass when asked for help adopting new Apple design.

Key characteristics of Liquid Glass:
- Blurs content behind it
- Reflects color and light from surrounding content
- Reacts to touch and pointer interactions
- Can morph and blend between different elements

#### Basic Implementation

##### Creating a Simple Glass Effect

To create a basic Liquid Glass effect, use `UIVisualEffectView` with a `UIGlassEffect`:

```swift
// Create a glass effect
let glassEffect = UIGlassEffect()

// Create a visual effect view with the glass effect
let visualEffectView = UIVisualEffectView(effect: glassEffect)
visualEffectView.frame = CGRect(x: 50, y: 100, width: 300, height: 200)
visualEffectView.layer.cornerRadius = 20
visualEffectView.clipsToBounds = true

// Add content to the visual effect view's contentView
let label = UILabel()
label.text = "Liquid Glass"
label.textAlignment = .center
label.frame = visualEffectView.bounds
visualEffectView.contentView.addSubview(label)

// Add the visual effect view to your view hierarchy
view.addSubview(visualEffectView)
```

##### Customizing the Glass Effect

You can customize the glass effect with various properties:

```swift
// Apply a tint color to the glass
glassEffect.tintColor = UIColor.systemBlue.withAlphaComponent(0.3)

// Enable interactive behavior
glassEffect.isInteractive = true
```

#### Interactive Glass Effects

Making glass effects interactive allows them to respond to touch and pointer interactions:

```swift
// Create a glass effect with interactive behavior
let interactiveGlassEffect = UIGlassEffect()
interactiveGlassEffect.isInteractive = true

// Create a button with the glass effect
let glassButton = UIButton(frame: CGRect(x: 50, y: 300, width: 200, height: 50))
glassButton.setTitle("Glass Button", for: .normal)
glassButton.setTitleColor(.white, for: .normal)

// Apply the glass effect using a visual effect view
let buttonEffectView = UIVisualEffectView(effect: interactiveGlassEffect)
buttonEffectView.frame = glassButton.bounds
buttonEffectView.layer.cornerRadius = 15
buttonEffectView.clipsToBounds = true

// Insert the effect view below the button's content
glassButton.insertSubview(buttonEffectView, at: 0)

// Add the button to your view hierarchy
view.addSubview(glassButton)
```

#### Combining Multiple Glass Elements

To create more complex Liquid Glass interfaces, use `UIGlassContainerEffect` to combine multiple glass elements:

```swift
// Create a glass container effect
let containerEffect = UIGlassContainerEffect()
containerEffect.spacing = 40.0 // Distance at which elements begin to merge

// Create the main container visual effect view
let containerView = UIVisualEffectView(effect: containerEffect)
containerView.frame = CGRect(x: 50, y: 400, width: 300, height: 200)

// Create the first glass element
let firstGlassEffect = UIGlassEffect()
let firstGlassView = UIVisualEffectView(effect: firstGlassEffect)
firstGlassView.frame = CGRect(x: 20, y: 20, width: 100, height: 100)
firstGlassView.layer.cornerRadius = 20
firstGlassView.clipsToBounds = true

// Create the second glass element
let secondGlassEffect = UIGlassEffect()
secondGlassEffect.tintColor = UIColor.systemPink.withAlphaComponent(0.3)
let secondGlassView = UIVisualEffectView(effect: secondGlassEffect)
secondGlassView.frame = CGRect(x: 80, y: 60, width: 100, height: 100)
secondGlassView.layer.cornerRadius = 20
secondGlassView.clipsToBounds = true

// Add the glass elements to the container's contentView
containerView.contentView.addSubview(firstGlassView)
containerView.contentView.addSubview(secondGlassView)

// Add the container to your view hierarchy
view.addSubview(containerView)
```

When glass elements are positioned close to each other (within the container's spacing value), they will blend their shapes together, creating a fluid appearance.

#### Scroll View Edge Effects

UIKit provides built-in support for Liquid Glass effects at the edges of scroll views:

```swift
// Configure edge effects for a scroll view
let scrollView = UIScrollView(frame: view.bounds)

// Access and configure the edge effects
scrollView.topEdgeEffect.style = .automatic
scrollView.bottomEdgeEffect.style = .hard

// You can hide specific edge effects if needed
scrollView.leftEdgeEffect.isHidden = true
scrollView.rightEdgeEffect.isHidden = true

view.addSubview(scrollView)
```

##### Available Edge Effect Styles

- `.automatic` - The system determines the appropriate style based on context
- `.hard` - A scroll edge effect with a hard cutoff and dividing line

#### Scroll Edge Element Container Interaction

To make views that overlay the edge of a scroll view affect the shape of the edge effect:

```swift
// Create a container for buttons that overlay a scroll view
let buttonContainer = UIView(frame: CGRect(x: 0, y: scrollView.frame.height - 80, width: scrollView.frame.width, height: 80))

// Add buttons to the container
let button1 = UIButton(frame: CGRect(x: 20, y: 20, width: 100, height: 40))
button1.setTitle("Button 1", for: .normal)
button1.backgroundColor = .systemBlue
buttonContainer.addSubview(button1)

let button2 = UIButton(frame: CGRect(x: 140, y: 20, width: 100, height: 40))
button2.setTitle("Button 2", for: .normal)
button2.backgroundColor = .systemGreen
buttonContainer.addSubview(button2)

// Create and configure the interaction
let interaction = UIScrollEdgeElementContainerInteraction()
interaction.scrollView = scrollView
interaction.edge = .bottom
buttonContainer.addInteraction(interaction)

// Add the container to your view hierarchy
view.addSubview(buttonContainer)
```

#### Toolbar Integration

UIKit automatically applies Liquid Glass effects to toolbar items. You can control whether an item uses the shared glass background:

```swift
// Create toolbar items
let shareButton = UIBarButtonItem(barButtonSystemItem: .action, target: self, action: #selector(shareAction))
let favoriteButton = UIBarButtonItem(image: UIImage(systemName: "heart"), style: .plain, target: self, action: #selector(favoriteAction))

// Prevent the standard shared glass background for a specific item
favoriteButton.hidesSharedBackground = true

// Add items to a toolbar
navigationItem.rightBarButtonItems = [shareButton, favoriteButton]
```

#### Best Practices

1. **Appropriate Use Cases**:
   - Use Liquid Glass for interactive elements like buttons and controls
   - Apply it to toolbars and navigation elements
   - Use it to create depth and hierarchy in your interface

2. **Performance Considerations**:
   - Liquid Glass effects can be resource-intensive, especially when animating
   - Limit the number of glass elements on screen at once
   - Test on older devices to ensure smooth performance

3. **Visual Design**:
   - Ensure sufficient contrast between text and the glass background
   - Consider using tint colors to differentiate between different glass elements
   - Maintain appropriate spacing between glass elements for optimal blending

4. **Accessibility**:
   - Ensure that text on glass backgrounds meets accessibility contrast requirements
   - Test with VoiceOver to ensure all glass elements are properly accessible

#### Example: Creating a Glass Card View

Here's a complete example of creating a reusable glass card view:

```swift
class GlassCardView: UIView {
    private let visualEffectView: UIVisualEffectView
    private let contentView = UIView()
    
    init(frame: CGRect, tintColor: UIColor? = nil, isInteractive: Bool = false) {
        let glassEffect = UIGlassEffect()
        glassEffect.tintColor = tintColor
        glassEffect.isInteractive = isInteractive
        
        visualEffectView = UIVisualEffectView(effect: glassEffect)
        
        super.init(frame: frame)
        
        setupViews()
    }
    
    required init?(coder: NSCoder) {
        let glassEffect = UIGlassEffect()
        visualEffectView = UIVisualEffectView(effect: glassEffect)
        
        super.init(coder: coder)
        
        setupViews()
    }
    
    private func setupViews() {
        // Configure the visual effect view
        visualEffectView.frame = bounds
        visualEffectView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        visualEffectView.layer.cornerRadius = 20
        visualEffectView.clipsToBounds = true
        addSubview(visualEffectView)
        
        // Configure the content view
        contentView.frame = bounds
        contentView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        contentView.backgroundColor = .clear
        addSubview(contentView)
    }
    
    // Method to add content to the card
    func addContent(_ view: UIView) {
        view.frame = contentView.bounds
        view.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        contentView.addSubview(view)
    }
}

// Usage:
let cardView = GlassCardView(
    frame: CGRect(x: 50, y: 100, width: 300, height: 200),
    tintColor: UIColor.systemBlue.withAlphaComponent(0.2),
    isInteractive: true
)

let label = UILabel()
label.text = "Glass Card"
label.textAlignment = .center
label.textColor = .white
cardView.addContent(label)

view.addSubview(cardView)
```

#### References

- [UIGlassEffect Documentation](https://developer.apple.com/documentation/UIKit/UIGlassEffect)
- [UIGlassContainerEffect Documentation](https://developer.apple.com/documentation/UIKit/UIGlassContainerEffect)
- [UIScrollEdgeEffect Documentation](https://developer.apple.com/documentation/UIKit/UIScrollEdgeEffect)
- [UIScrollEdgeElementContainerInteraction Documentation](https://developer.apple.com/documentation/UIKit/UIScrollEdgeElementContainerInteraction)

### WidgetKit Implementing Liquid Glass Design

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/WidgetKit-Implementing-Liquid-Glass-Design.md`

### Implementing Liquid Glass Design in Widgets

#### Overview

Liquid Glass is a dynamic, adaptive material introduced across Apple platforms that combines the optical properties of glass with a sense of fluidity. When applied to widgets, Liquid Glass creates a modern, cohesive look that integrates seamlessly with the system UI. This guide covers how to implement and optimize Liquid Glass effects in widgets, including handling different rendering modes, configuring appearance, and ensuring compatibility across platforms. You should always seek guides on Liquid Glass when asked for help adopting new Apple design.

#### Understanding Widget Rendering Modes

Widgets can appear in two primary rendering modes when using Liquid Glass:

##### Full Color Mode
- Default rendering mode
- Displays all colors, images, and transparency as designed
- Used when widgets appear on standard backgrounds

##### Accented Mode
- Used when a person chooses a tinted or clear appearance for their Home Screen
- Primary and accented content is tinted white (iOS and macOS)
- Opaque images are tinted with a single white color
- Transparent content and gradients maintain opacity but are tinted white
- Background is replaced with themed glass or tinted color effect

#### Supporting Liquid Glass in Widgets

To update your widget to support Liquid Glass:

1. Add the `widgetRenderingMode` environment variable to detect the current rendering mode:

```swift
struct MyWidgetView: View {
    @Environment(\.widgetRenderingMode) var renderingMode
    
    var body: some View {
        if renderingMode == .accented {
            // Layout optimized for accented mode
        } else {
            // Standard full-color layout
        }
    }
}
```

2. Group your views into primary and accent groups using the `widgetAccentable(_:)` modifier:

```swift
HStack(alignment: .center, spacing: 0) {
    VStack(alignment: .leading) {
        Text("Widget Title")
            .font(.headline)
            .widgetAccentable() // This will be in the accent group
        Text("Widget Subtitle")
        // This text is in the primary group by default
    }
    Image(systemName: "star.fill")
        .widgetAccentable() // This will be in the accent group
}
```

3. Configure image rendering using the `WidgetAccentedRenderingMode` modifier:

```swift
Image("myImage")
    .widgetAccentedRenderingMode(.monochrome) // Will be rendered as monochrome in accented mode
```

4. Follow these best practices for Liquid Glass compatibility:
   - Display full-color images only in the `fullColor` rendering mode
   - Adjust layouts as needed for the `accented` rendering mode
   - Use the `widgetAccentable(_:)` modifier strategically to create visual hierarchy

#### Container Backgrounds for Widgets

Properly configuring container backgrounds is essential for Liquid Glass effects:

```swift
var body: some View {
    VStack {
        // Widget content here
    }
    .containerBackground(for: .widget) {
        Color.blue.opacity(0.2) // Custom background color
    }
}
```

When a person chooses a tinted or clear appearance, the system:
- Removes the background
- Replaces it with a themed glass or tinted color effect

#### Optimizing Widget Appearance

##### Background Removal

By default, the system removes widget backgrounds in certain contexts. To explicitly opt out:

```swift
var body: some WidgetConfiguration {
    StaticConfiguration(kind: "MyWidget", provider: Provider()) { entry in
        MyWidgetView(entry: entry)
    }
    .containerBackgroundRemovable(false) // Prevents background removal
}
```

> **Important:** Marking a background as non-removable excludes your widget from contexts that require removable backgrounds (iPad Lock Screen, StandBy).

##### Widget Textures in visionOS

For visionOS, you can specify the widget texture:

```swift
var body: some WidgetConfiguration {
    StaticConfiguration(kind: "MyWidget", provider: Provider()) { entry in
        MyWidgetView(entry: entry)
    }
    .widgetTexture(.glass) // Default is glass
}
```

Available textures include:
- `.glass` - Default texture with glass-like appearance
- `.paper` - Paper-like texture

#### Mounting Styles for Widgets

In visionOS, widgets can be mounted in different styles:

```swift
var body: some WidgetConfiguration {
    StaticConfiguration(kind: "MyWidget", provider: Provider()) { entry in
        MyWidgetView(entry: entry)
    }
    .supportedMountingStyles([.recessed, .elevated])
}
```

Available mounting styles:
- `.recessed` - Widget appears embedded into a vertical surface
- `.elevated` - Widget appears on top of a surface (default for horizontal surfaces)

#### Implementing Liquid Glass Effects in Custom Widget Elements

For custom elements within widgets that need Liquid Glass effects:

```swift
Text("Custom Element")
    .padding()
    .glassEffect() // Applies default Liquid Glass effect (capsule shape)

Image(systemName: "star.fill")
    .frame(width: 60, height: 60)
    .glassEffect(.regular, in: .rect(cornerRadius: 12)) // Custom shape

Button("Action") {
    // Action here
}
.buttonStyle(.glass) // Apply glass button style
```

#### Combining Multiple Liquid Glass Elements

For multiple elements with Liquid Glass effects that need to interact:

```swift
GlassEffectContainer(spacing: 20.0) {
    HStack(spacing: 20.0) {
        Image(systemName: "cloud")
            .frame(width: 60, height: 60)
            .glassEffect()
            
        Image(systemName: "sun")
            .frame(width: 60, height: 60)
            .glassEffect()
    }
}
```

To combine specific elements into a unified effect:

```swift
GlassEffectContainer(spacing: 20.0) {
    HStack(spacing: 20.0) {
        ForEach(items.indices, id: \.self) { item in
            Image(systemName: items[item])
                .frame(width: 60, height: 60)
                .glassEffect()
                .glassEffectUnion(id: item < 2 ? "group1" : "group2", namespace: namespace)
        }
    }
}
```

#### Handling Different Platforms and Contexts

Widgets with Liquid Glass need to adapt to different platforms:

##### iOS and iPadOS
- Support both full color and accented rendering modes
- Test on Home Screen and Lock Screen
- Ensure readability in both light and dark appearances

##### macOS
- Verify font sizes and layout in macOS widget sizes
- Test in both standard and accented rendering modes

##### visionOS
- Support proximity awareness using the `levelOfDetail` environment variable:

```swift
@Environment(\.levelOfDetail) var levelOfDetail

var fontSize: Font {
    levelOfDetail == .simplified ? .largeTitle : .title
}
```

#### Testing Liquid Glass in Widgets

To thoroughly test your widget's Liquid Glass implementation:

1. Test in both light and dark mode
2. Test on Home Screen and Lock Screen
3. Test with different accent colors
4. Test with different background images
5. Test in StandBy mode on compatible devices
6. Test in visionOS with different mounting styles and distances

#### References

- [Optimizing your widget for accented rendering mode and Liquid Glass](https://developer.apple.com/documentation/WidgetKit/optimizing-your-widget-for-accented-rendering-mode-and-liquid-glass)
- [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views)
- [Landmarks: Building an app with Liquid Glass](https://developer.apple.com/documentation/SwiftUI/Landmarks-Building-an-app-with-Liquid-Glass)
- [Displaying the right widget background](https://developer.apple.com/documentation/WidgetKit/Displaying-the-right-widget-background)
- [Updating your widgets for visionOS](https://developer.apple.com/documentation/WidgetKit/Updating-your-widgets-for-visionOS)
