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

## Source Content

### Map Kit Geo Toolbox Place Descriptors

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/MapKit-GeoToolbox-PlaceDescriptors.md`

### Using Place Descriptors with MapKit and GeoToolbox

#### Overview

Place descriptors provide a standardized way to represent physical locations across different mapping services. The `GeoToolbox` framework allows you to create `PlaceDescriptor` structures that can be used with MapKit and third-party mapping systems. This guide covers how to work with place descriptors, integrate them with MapKit, and leverage their capabilities for location-based applications.

Key concepts:
- **PlaceDescriptor**: A structure containing identifying information about a place
- **PlaceRepresentation**: Common ways to represent a place (coordinates, addresses)
- **SupportingPlaceRepresentation**: Proprietary identifiers for places from different mapping services
- **MapKit integration**: Converting between MapKit objects and place descriptors

#### Creating Place Descriptors

##### From an Address String

```swift
import GeoToolbox

// Create a place descriptor with an address and common name
let fountain = PlaceDescriptor(
    representations: [.address("121-122 James's St \n Dublin 8 \n D08 ET27 \n Ireland")],
    commonName: "Obelisk Fountain"
)
```

##### From Coordinates

```swift
import GeoToolbox

// Create a place descriptor with coordinates
let eiffelTower = PlaceDescriptor(
    representations: [.coordinate(CLLocationCoordinate2D(latitude: 48.8584, longitude: 2.2945))],
    commonName: "Eiffel Tower"
)
```

##### From an MKMapItem

```swift
import MapKit
import GeoToolbox

// Convert an MKMapItem to a PlaceDescriptor
func convertMapItemToDescriptor(mapItem: MKMapItem) -> PlaceDescriptor? {
    guard let descriptor = PlaceDescriptor(item: mapItem) else {
        print("Failed to create place descriptor from map item")
        return nil
    }
    return descriptor
}
```

##### With Multiple Representations

```swift
// Create a place descriptor with multiple representations
let statue = PlaceDescriptor(
    representations: [
        .coordinate(CLLocationCoordinate2D(latitude: 40.6892, longitude: -74.0445)),
        .address("Liberty Island, New York, NY 10004, United States")
    ],
    commonName: "Statue of Liberty"
)
```

#### Working with Place Representations

##### Understanding PlaceRepresentation

`PlaceRepresentation` is an enumeration that represents a physical place using common mapping concepts:

```swift
// Available PlaceRepresentation cases
// .coordinate(CLLocationCoordinate2D) - A location with latitude and longitude
// .address(String) - A full address string
```

##### Accessing Representations

```swift
// Access the representations from a place descriptor
func printPlaceRepresentations(descriptor: PlaceDescriptor) {
    for representation in descriptor.representations {
        switch representation {
        case .coordinate(let coordinate):
            print("Coordinate: \(coordinate.latitude), \(coordinate.longitude)")
        case .address(let address):
            print("Address: \(address)")
        }
    }
}
```

##### Extracting Coordinate

```swift
// Get the coordinate from a place descriptor if available
func getCoordinate(from descriptor: PlaceDescriptor) -> CLLocationCoordinate2D? {
    return descriptor.coordinate
}
```

##### Extracting Address

```swift
// Get the address from a place descriptor if available
func getAddress(from descriptor: PlaceDescriptor) -> String? {
    return descriptor.address
}
```

#### Supporting Place Representations

##### Understanding SupportingPlaceRepresentation

`SupportingPlaceRepresentation` contains proprietary identifiers for places from different mapping services:

```swift
// Available SupportingPlaceRepresentation cases
// .serviceIdentifiers([String: String]) - Maps service provider IDs to place IDs
```

##### Working with Service Identifiers

```swift
// Create a place descriptor with service identifiers
let landmark = PlaceDescriptor(
    representations: [.address("1 Infinite Loop, Cupertino, CA 95014")],
    commonName: "Apple Park",
    supportingRepresentations: [
        .serviceIdentifiers(["com.apple.maps": "ABC123XYZ", 
                            "com.google.maps": "ChIJq6qq6jK1j4ARzl-WRHNx9CI"])
    ]
)
```

##### Retrieving Service Identifiers

```swift
// Get a specific service identifier
func getAppleMapsIdentifier(from descriptor: PlaceDescriptor) -> String? {
    return descriptor.serviceIdentifier(for: "com.apple.maps")
}
```

#### Geocoding with MapKit

##### Forward Geocoding (Address to Coordinates)

```swift
// Convert an address string to coordinates
func geocodeAddress(address: String) async throws -> [MKMapItem] {
    guard let request = MKGeocodingRequest(addressString: address) else {
        throw NSError(domain: "GeocodingError", code: 1, userInfo: nil)
    }
    
    return try await request.mapItems
}
```

##### Reverse Geocoding (Coordinates to Address)

```swift
// Convert coordinates to address information
func reverseGeocode(coordinate: CLLocationCoordinate2D) async throws -> [MKMapItem] {
    let location = CLLocation(latitude: coordinate.latitude, longitude: coordinate.longitude)
    
    guard let request = MKReverseGeocodingRequest(location: location) else {
        throw NSError(domain: "ReverseGeocodingError", code: 1, userInfo: nil)
    }
    
    return try await request.mapItems
}
```

##### Creating PlaceDescriptor from Geocoding Results

```swift
// Create a place descriptor from geocoding results
func createDescriptorFromGeocodingResult(address: String) async throws -> PlaceDescriptor? {
    let mapItems = try await geocodeAddress(address: address)
    
    guard let firstItem = mapItems.first else {
        return nil
    }
    
    return PlaceDescriptor(item: firstItem)
}
```

#### Practical Examples

##### Creating and Using Place Descriptors

```swift
// Example: Creating and using a place descriptor for a landmark
func workWithLandmark() {
    // Create a place descriptor for a landmark
    let landmark = PlaceDescriptor(
        representations: [
            .coordinate(CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194)),
            .address("San Francisco, CA, USA")
        ],
        commonName: "San Francisco"
    )
    
    // Access the common name
    if let name = landmark.commonName {
        print("Landmark name: \(name)")
    }
    
    // Access the coordinate
    if let coordinate = landmark.coordinate {
        print("Latitude: \(coordinate.latitude), Longitude: \(coordinate.longitude)")
    }
    
    // Access the address
    if let address = landmark.address {
        print("Address: \(address)")
    }
}
```

##### Converting Between MapKit and GeoToolbox

```swift
// Example: Converting between MKMapItem and PlaceDescriptor
func convertBetweenMapKitAndGeoToolbox() async throws {
    // Start with an address
    let address = "1 Apple Park Way, Cupertino, CA 95014"
    
    // Geocode to get MKMapItem
    guard let request = MKGeocodingRequest(addressString: address) else {
        print("Failed to create geocoding request")
        return
    }
    
    let mapItems = try await request.mapItems
    
    guard let mapItem = mapItems.first else {
        print("No results found")
        return
    }
    
    // Convert MKMapItem to PlaceDescriptor
    guard let descriptor = PlaceDescriptor(item: mapItem) else {
        print("Failed to create descriptor from map item")
        return
    }
    
    // Use the descriptor
    print("Created descriptor for: \(descriptor.commonName ?? "Unknown place")")
    
    // Create a new MKMapItem from the descriptor's information
    if let coordinate = descriptor.coordinate {
        let location = CLLocation(latitude: coordinate.latitude, longitude: coordinate.longitude)
        let address = MKAddress()
        let newMapItem = MKMapItem(location: location, address: address)
        
        print("Created new map item at: \(newMapItem.location.coordinate.latitude), \(newMapItem.location.coordinate.longitude)")
    }
}
```

##### Working with Multiple Mapping Services

```swift
// Example: Working with identifiers from multiple mapping services
func workWithMultipleServices() {
    // Create a place descriptor with identifiers for multiple services
    let place = PlaceDescriptor(
        representations: [.coordinate(CLLocationCoordinate2D(latitude: 51.5074, longitude: -0.1278))],
        commonName: "London Eye",
        supportingRepresentations: [
            .serviceIdentifiers([
                "com.apple.maps": "AppleMapsID123",
                "com.google.maps": "GoogleMapsID456",
                "com.openstreetmap": "OSM789"
            ])
        ]
    )
    
    // Get identifiers for different services
    if let appleID = place.serviceIdentifier(for: "com.apple.maps") {
        print("Apple Maps ID: \(appleID)")
    }
    
    if let googleID = place.serviceIdentifier(for: "com.google.maps") {
        print("Google Maps ID: \(googleID)")
    }
    
    if let osmID = place.serviceIdentifier(for: "com.openstreetmap") {
        print("OpenStreetMap ID: \(osmID)")
    }
}
```

#### References

- [GeoToolbox Framework](https://developer.apple.com/documentation/GeoToolbox)
- [PlaceDescriptor](https://developer.apple.com/documentation/GeoToolbox/PlaceDescriptor)
- [MapKit Framework](https://developer.apple.com/documentation/MapKit)
- [MKMapItem](https://developer.apple.com/documentation/MapKit/MKMapItem)
- [MKGeocodingRequest](https://developer.apple.com/documentation/MapKit/MKGeocodingRequest)
- [MKReverseGeocodingRequest](https://developer.apple.com/documentation/MapKit/MKReverseGeocodingRequest)
- [MKAddress](https://developer.apple.com/documentation/MapKit/MKAddress)
- [MKAddressRepresentations](https://developer.apple.com/documentation/MapKit/MKAddressRepresentations)

### Store Kit Updates

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/StoreKit-Updates.md`

### StoreKit Updates

#### Overview

StoreKit is Apple's framework for implementing in-app purchases, subscriptions, and App Store interactions. Recent updates have introduced significant enhancements to the core framework, new SwiftUI views for merchandising subscriptions, and improved tools for testing and development.

#### Core Framework Updates

##### AppTransaction Updates (iOS 18.4+)

`AppTransaction` now includes two new fields:

- **appTransactionID**: A globally unique identifier for each Apple Account that downloads your app
  - Unique for each family group member for apps supporting Family Sharing
  - Back-deployed to iOS 15
  
- **originalPlatform**: Indicates the platform on which the customer originally purchased the app
  - Values include iOS, macOS, tvOS, or visionOS
  - Helps support business model changes and entitle customers appropriately

```swift
// Example of accessing AppTransaction properties
Task {
    do {
        let appTransaction = try await AppTransaction.shared
        
        // Access the new properties
        let transactionID = appTransaction.appTransactionID
        let platform = appTransaction.originalPlatform
        
        // Use these values for business logic
        if platform == .iOS {
            // Handle iOS-specific logic
        }
    } catch {
        print("Failed to get app transaction: \(error)")
    }
}
```

##### Transaction Updates (iOS 18.4+)

The `Transaction` type represents a successful In-App Purchase and has been enhanced with:

- **New API**: `Transaction.currentEntitlements(for:)` replaces `Transaction.currentEntitlement(for:)`
  - Returns an asynchronous sequence of transactions entitling the customer to a given product
  - Supports multiple entitlements through different means

- **New Fields**:
  - `appTransactionID`: Links transactions to the app download
  - `offerPeriod`: Details the subscription period associated with a redeemed offer
  - `advancedCommerceInfo`: Applies only to apps using the Advanced Commerce API

```swift
// Example of using the new currentEntitlements API
Task {
    for await verificationResult in Transaction.currentEntitlements(for: "your.product.id") {
        switch verificationResult {
        case .verified(let transaction):
            // Handle verified transaction
            let appTransactionID = transaction.appTransactionID
            if let offerPeriod = transaction.offerPeriod {
                // Handle offer period information
            }
        case .unverified(let transaction, let verificationError):
            // Handle unverified transaction
            print("Verification failed: \(verificationError)")
        }
    }
}
```

##### RenewalInfo Updates (iOS 18.4+)

The `RenewalInfo` type for auto-renewable subscriptions has been enhanced with:

- **Enhanced API**: `SubscriptionStatus` can now query subscription statuses using a Transaction ID
- **Four New Fields**: Providing more comprehensive insights into subscription details
- **Expiration Reasons**: Valuable for understanding customer behavior and tailoring strategies
  - Example: If a subscription expires due to a price increase, you can offer win-back promotions

```swift
// Example of accessing subscription status with a transaction ID
Task {
    do {
        let status = try await Product.SubscriptionInfo.Status(transactionID: "transaction_id_here")
        
        // Access renewal info
        if let renewalInfo = status.renewalInfo {
            // Check expiration reason if applicable
            if let expirationReason = renewalInfo.expirationReason {
                switch expirationReason {
                case .priceIncrease:
                    // Offer a win-back promotion
                case .billingError:
                    // Prompt to update payment method
                default:
                    // Handle other expiration reasons
                }
            }
        }
    } catch {
        print("Failed to get subscription status: \(error)")
    }
}
```

#### StoreKit Views

##### SubscriptionOfferView

A new SwiftUI view for merchandising auto-renewable subscriptions:

```swift
// Basic usage with product ID
SubscriptionOfferView(productID: "your.subscription.id")
    .prefersPromotionalIcon(true)

// Using a loaded product
SubscriptionOfferView(product: loadedSubscriptionProduct)

// With custom icon
SubscriptionOfferView(productID: "your.subscription.id") {
    Image("custom_icon")
        .resizable()
        .frame(width: 40, height: 40)
}

// With placeholder icon while loading
SubscriptionOfferView(productID: "your.subscription.id") {
    Image("custom_icon")
        .resizable()
        .frame(width: 40, height: 40)
} placeholderIcon: {
    Image(systemName: "hourglass")
        .resizable()
        .frame(width: 40, height: 40)
}
```

##### Configuring SubscriptionOfferView

Add detail action to direct customers to subscription store:

```swift
SubscriptionOfferView(productID: "your.subscription.id")
    .subscriptionOfferViewDetailAction {
        // Action when detail link is tapped
        isShowingSubscriptionStore = true
    }
```

##### Displaying Different Plans Based on Customer Status

Configure which subscription plan to display using the `visibleRelationship` parameter:

```swift
// Using a subscription group ID
SubscriptionOfferView(groupID: "your.group.id", visibleRelationship: .upgrade)

// Available relationships:
// - .upgrade: Shows a plan one level higher than current
// - .downgrade: Shows a plan one level lower than current
// - .crossgrade: Shows equivalent tier plans with best value
// - .current: Shows customer's current plan
// - .all: Shows all plans in the group
```

##### Tracking Subscription Status

Use the `subscriptionStatusTask` modifier to determine customer status:

```swift
@main
struct MyApp: App {
    @State private var customerStatus: SubscriptionStatus = .unknown
    
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.customerSubscriptionStatus, customerStatus)
                .subscriptionStatusTask(for: "your.group.id") { statuses in
                    // Translate StoreKit statuses to your app's model
                    if statuses.contains(where: { $0.state == .subscribed }) {
                        customerStatus = .subscribed
                    } else if statuses.contains(where: { $0.state == .expired }) {
                        customerStatus = .expired
                    } else {
                        customerStatus = .notSubscribed
                    }
                }
        }
    }
}
```

#### In-App Purchase Request Signing

StoreKit now requires JSON Web Signatures (JWS) for certain Purchase Option and View Modifier APIs:

- Setting customer eligibility for introductory offers
- Signing promotional offers

The App Store Server Library simplifies the JWS signing process:

1. Retrieve your In-App Purchase signing key from App Store Connect
2. Use the key with the App Store Server Library to create signed requests

```swift
// Example of using the App Store Server Library for signing
import AppStoreServerLibrary

// Create a signed JWS for a promotional offer
func createSignedOfferJWS(productID: String, offerID: String) async throws -> String {
    let signingKey = try SigningKey(
        privateKeyFilePath: "path/to/key.p8",
        keyID: "YOUR_KEY_ID",
        issuerID: "YOUR_ISSUER_ID"
    )
    
    let library = try AppStoreServerLibrary(
        signingKey: signingKey,
        environment: .production
    )
    
    return try library.createOfferSignature(
        productIdentifier: productID,
        subscriptionOfferID: offerID,
        applicationUsername: nil,
        nonce: UUID().uuidString,
        keyIdentifier: "YOUR_KEY_ID",
        timestamp: Int(Date().timeIntervalSince1970)
    )
}
```

#### Testing and Development

##### StoreKit Testing in Xcode

Create a local StoreKit configuration file to test In-App Purchases without App Store Connect setup:

1. Select File > New > File From Template
2. Search for "storekit" and select "StoreKit Configuration File"
3. Name the file (e.g., `LocalConfiguration.storekit`)
4. Define products in the configuration file

##### Transaction Manager

Use the Transaction Manager window in Xcode to:

- Create and inspect transactions
- Modify transaction properties
- Test different purchase scenarios

##### Testing Subscription Offers

1. Set up subscription offers in your local configuration file
2. Implement the necessary JWS signing for offers
3. Test different offer scenarios using the Transaction Manager

#### Advanced Commerce API

The Advanced Commerce API enables easier support for:

- In-App Purchases for large content catalogs
- Creator experiences
- Subscriptions with optional add-ons

This API is accessible through the new `advancedCommerceInfo` field in the `Transaction` model.

#### References

- [StoreKit Documentation](https://developer.apple.com/documentation/storekit)
- [What's new in StoreKit and In-App Purchase (WWDC 2025)](https://developer.apple.com/videos/play/wwdc2025/241/)
- [Getting started with In-App Purchase using StoreKit views](https://developer.apple.com/documentation/StoreKit/getting-started-with-in-app-purchases-using-storekit-views)
- [Understanding StoreKit workflows](https://developer.apple.com/documentation/StoreKit/understanding-storekit-workflows)
- [App Store Server Library on GitHub](https://github.com/apple/app-store-server-library-swift)

### Swift Charts 3 D Visualization

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/Swift-Charts-3D-Visualization.md`

### Using 3D Charts with Swift Charts

#### Overview

Swift Charts provides powerful 3D visualization capabilities through the `Chart3D` component, allowing developers to create immersive three-dimensional data visualizations. This guide covers how to create, customize, and interact with 3D charts in SwiftUI applications using the Swift Charts framework.

Key components for 3D charts include:
- `Chart3D`: The main container view for 3D chart content
- `SurfacePlot`: For visualizing 3D surface data
- `Chart3DPose`: For controlling the viewing angle and perspective
- `Chart3DSurfaceStyle`: For styling the appearance of 3D surfaces

#### Basic Setup

##### Importing Required Frameworks

```swift
import SwiftUI
import Charts
```

##### Creating a Simple 3D Chart

The most basic 3D chart can be created using a mathematical function that maps x,y coordinates to z values:

```swift
struct Basic3DChartView: View {
    var body: some View {
        Chart3D {
            SurfacePlot(
                x: "X Axis",
                y: "Y Axis",
                z: "Z Axis",
                function: { x, y in
                    // Simple mathematical function: z = sin(x) * cos(y)
                    sin(x) * cos(y)
                }
            )
        }
    }
}
```

##### Creating a 3D Chart from Data

You can also create 3D charts from collections of data:

```swift
struct DataPoint3D: Identifiable {
    var x: Double
    var y: Double
    var z: Double
    var id = UUID()
}

struct Data3DChartView: View {
    let dataPoints: [DataPoint3D] = [
        // Your 3D data points
    ]
    
    var body: some View {
        Chart3D(dataPoints) { point in
            // Create appropriate 3D visualization for each point
        }
    }
}
```

#### Customizing 3D Charts

##### Setting the Chart Pose (Viewing Angle)

Control the viewing angle of your 3D chart using `Chart3DPose`:

```swift
struct CustomPose3DChartView: View {
    // Create a state variable to store the pose
    @State private var chartPose: Chart3DPose = .default
    
    var body: some View {
        Chart3D {
            SurfacePlot(
                x: "X Axis",
                y: "Y Axis",
                z: "Z Axis",
                function: { x, y in
                    sin(x) * cos(y)
                }
            )
        }
        // Apply the pose to the chart
        .chart3DPose(chartPose)
    }
}
```

You can use predefined poses:
- `.default`: The default viewing angle
- `.front`: View from the front
- `.back`: View from the back
- `.top`: View from the top
- `.bottom`: View from the bottom
- `.right`: View from the right side
- `.left`: View from the left side

Or create a custom pose with specific azimuth and inclination angles:

```swift
Chart3DPose(azimuth: .degrees(45), inclination: .degrees(30))
```

##### Interactive Pose Control

Allow users to interact with the chart by binding the pose to a state variable:

```swift
struct Interactive3DChartView: View {
    @State private var chartPose: Chart3DPose = .default
    
    var body: some View {
        Chart3D {
            SurfacePlot(
                x: "X Axis",
                y: "Y Axis",
                z: "Z Axis",
                function: { x, y in
                    sin(x) * cos(y)
                }
            )
        }
        // Bind the pose to enable interactive rotation
        .chart3DPose($chartPose)
    }
}
```

##### Setting the Camera Projection

Control the camera projection of the points in a 3D chart using `Chart3DCameraProjection`:

```swift
struct CustomProjection3DChartView: View {
    // Create a state variable to store the pose
    @State private var cameraProjection: Chart3DCameraProjection = .perspective
    
    var body: some View {
        Chart3D {
            SurfacePlot(
                x: "X Axis",
                y: "Y Axis",
                z: "Z Axis",
                function: { x, y in
                    sin(x) * cos(y)
                }
            )
        }
        // Apply the camera projection to the chart
        .chart3DCameraProjection(cameraProjection)
    }
}
```

You can use the following camera projection styles:
- `.automatic`: Automatically determines the camera projection
- `.orthographic`: Objects maintain size regardless of depth
- `.perspective`: Objects appear smaller with distance

#### Working with Surface Plots

##### Basic Surface Plot

```swift
SurfacePlot(
    x: "X Axis",
    y: "Y Axis",
    z: "Z Axis",
    function: { x, y in
        // Mathematical function defining the surface
        sin(sqrt(x*x + y*y))
    }
)
```

##### Styling Surface Plots

Apply different styles to your surface plots:

```swift
SurfacePlot(
    x: "X Axis",
    y: "Y Axis",
    z: "Z Axis",
    function: { x, y in
        sin(x) * cos(y)
    }
)
.foregroundStyle(Color.blue)
```

Available surface styles:
- `.heightBased`: Colors the surface based on the height (y-value)
- `.normalBased`: Colors the surface based on the surface normal direction

##### Custom Gradient Surface Style

Create a custom gradient for your surface:

```swift
let customGradient = Gradient(colors: [.blue, .purple, .red])

SurfacePlot(
    x: "X Axis",
    y: "Y Axis",
    z: "Z Axis",
    function: { x, y in
        sin(x) * cos(y)
    }
)
.foregroundStyle(LinearGradient(gradient: customGradient, startPoint: .topLeading, endPoint: .bottomTrailing))
```

##### Controlling Surface Roughness

Adjust the roughness of the surface:

```swift
SurfacePlot(
    x: "X Axis",
    y: "Y Axis",
    z: "Z Axis",
    function: { x, y in
        sin(x) * cos(y)
    }
)
.roughness(0.3) // 0 is smooth, 1 is completely rough
```

#### Advanced Techniques

##### Combining Multiple Surface Plots

```swift
Chart3D {
    // First surface plot
    SurfacePlot(
        x: "X",
        y: "Y",
        z: "Z",
        function: { x, y in
            sin(x) * cos(y)
        }
    )
    
    // Second surface plot
    SurfacePlot(
        x: "X",
        y: "Y",
        z: "Z",
        function: { x, y in
            cos(x) * sin(y) + 2 // Offset to avoid overlap
        }
    )
}
```

##### Specifying Y-Range for Height-Based Styling

Control the color mapping by specifying the y-range:

```swift
SurfacePlot(
    x: "X Axis",
    y: "Y Axis",
    z: "Z Axis",
    function: { x, y in
        sin(x) * cos(y)
    }
)
.foregroundStyle(Chart3DSurfaceStyle.heightBased(yRange: -1.0...1.0))
```

##### Custom Gradient with Y-Range

```swift
let customGradient = Gradient(colors: [.blue, .green, .yellow, .red])

SurfacePlot(
    x: "X Axis",
    y: "Y Axis",
    z: "Z Axis",
    function: { x, y in
        sin(x) * cos(y)
    }
)
.foregroundStyle(Chart3DSurfaceStyle.heightBased(customGradient, yRange: -1.0...1.0))
```

#### Complete Example: Interactive 3D Visualization

Here's a complete example that demonstrates an interactive 3D chart with customized styling:

```swift
import SwiftUI
import Charts

struct Interactive3DSurfaceView: View {
    // State for interactive rotation
    @State private var chartPose: Chart3DPose = .default
    
    // Custom gradient for surface coloring
    let surfaceGradient = Gradient(colors: [
        .blue,
        .cyan,
        .green,
        .yellow,
        .orange,
        .red
    ])
    
    var body: some View {
        VStack {
            Text("Interactive 3D Surface Visualization")
                .font(.headline)
            
            Chart3D {
                SurfacePlot(
                    x: "X Value",
                    y: "Y Value",
                    z: "Result",
                    function: { x, y in
                        // Interesting mathematical function
                        sin(sqrt(x*x + y*y)) / sqrt(x*x + y*y + 0.1)
                    }
                )
                .roughness(0.2)
            }
            .chart3DPose($chartPose)
            .frame(height: 400)
            
            Text("Drag to rotate the visualization")
                .font(.caption)
                .foregroundColor(.secondary)
            
            HStack {
                Button("Front View") {
                    withAnimation {
                        chartPose = .front
                    }
                }
                
                Button("Top View") {
                    withAnimation {
                        chartPose = .top
                    }
                }
                
                Button("Default View") {
                    withAnimation {
                        chartPose = .default
                    }
                }
            }
            .buttonStyle(.bordered)
        }
        .padding()
    }
}
```

#### References

- [Apple Developer Documentation: Chart3D](https://developer.apple.com/documentation/Charts/Chart3D)
- [Apple Developer Documentation: SurfacePlot](https://developer.apple.com/documentation/Charts/SurfacePlot)
- [Apple Developer Documentation: Chart3DPose](https://developer.apple.com/documentation/Charts/Chart3DPose)
- [Apple Developer Documentation: Chart3DSurfaceStyle](https://developer.apple.com/documentation/Charts/Chart3DSurfaceStyle)
- [Apple Developer Documentation: Creating a chart using Swift Charts](https://developer.apple.com/documentation/Charts/Creating-a-chart-using-Swift-Charts)

### Widgets For Vision Os

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/Widgets-for-visionOS.md`

### Widgets for visionOS

#### Overview

Widgets in visionOS provide a powerful way to display glanceable information from your app in a spatial computing environment. Unlike traditional 2D widgets on other platforms, visionOS widgets are three-dimensional objects that can be placed in a user's physical space, either mounted on surfaces (walls, tables) or floating in the environment. They support unique features like proximity awareness, different mounting styles, and specialized textures that help them blend naturally into the spatial environment.

Key concepts for visionOS widgets include mounting styles (elevated or recessed), textures (glass or paper), proximity awareness, and support for various widget families including extra-large sizes. This guide covers the essential APIs and implementation details for creating effective widgets in visionOS.

#### Widget Mounting Styles

In visionOS, widgets can be mounted in two different styles:

- **Elevated**: Widgets sit on top of horizontal or vertical surfaces (default style)
- **Recessed**: Widgets appear embedded into vertical surfaces like walls

```swift
struct WeatherWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(
            // Configuration details
        ) { entry in
            WeatherWidgetView(entry: entry)
        }
        .configurationDisplayName("Weather Widget")
        // Specify supported mounting styles
        .supportedMountingStyles([.elevated, .recessed]) // Default is both
        // Or limit to just one style
        // .supportedMountingStyles([.recessed])
    }
}
```

If your widget only supports the recessed mounting style, users won't be able to place it on horizontal surfaces.

#### Widget Textures

visionOS offers two texture options for widgets:

- **Glass**: The default texture that gives widgets a transparent glass-like appearance
- **Paper**: An alternative texture that provides a poster-like look

```swift
struct CaffeineTrackerWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(
            // Configuration details
        ) { entry in
            CaffeineTrackerWidgetView(entry: entry)
        }
        .configurationDisplayName("Caffeine Tracker")
        // Specify the widget texture
        .widgetTexture(.glass) // Default
        // Or use paper texture
        // .widgetTexture(.paper)
    }
}
```

#### Proximity Awareness

A key feature of widgets in visionOS is their ability to respond to a user's proximity. Widgets can display different levels of detail based on how close or far away the user is viewing them from.

```swift
struct TotalCaffeineView: View {
    // Access the level of detail environment variable
    @Environment(\.levelOfDetail) var levelOfDetail
    
    // Other properties
    
    var body: some View {
        VStack {
            Text("Total Caffeine")
                .font(.caption)
            Text(totalCaffeine.formatted())
                .font(caffeineFont)
        }
    }
    
    // Adjust font size based on proximity
    var caffeineFont: Font {
        if levelOfDetail == .simplified {
            return .largeTitle // Larger text when viewed from a distance
        } else {
            return .title // Normal size when viewed up close
        }
    }
}
```

The `levelOfDetail` environment variable can have two values:
- `.default`: Used when the user is close to the widget
- `.simplified`: Used when the user is viewing from a distance

When a user's distance to a widget changes, the system automatically animates the layout changes between these two states.

#### Supporting Widget Families

visionOS supports all system family widget sizes, from small to extra large:

```swift
struct MyVisionWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(
            // Configuration details
        ) { entry in
            MyWidgetView(entry: entry)
        }
        .configurationDisplayName("My Widget")
        .supportedFamilies([
            .systemSmall,
            .systemMedium,
            .systemLarge,
            .systemExtraLarge,
            .systemExtraLargePortrait // visionOS-specific
        ])
    }
}
```

The extra large widget families (`.systemExtraLarge` and `.systemExtraLargePortrait`) are particularly effective when using the paper texture for a poster-like appearance.

#### Rendering Modes

Widgets in visionOS support both full color and accented rendering modes:

- **Full Color**: The default mode that displays the widget with its complete design
- **Accented**: A simplified mode where the background is removed and replaced with a solid color that complements the user's selected color theme

```swift
// No special code is needed to support accented mode
// Just ensure your widget looks good with or without its background

// Use containerBackground to mark removable backgrounds
var body: some View {
    VStack {
        // Widget content
    }
    .containerBackground(for: .widget) {
        Color.gameBackground
    }
}
```

To detect whether a widget appears with or without a background, use the `showsWidgetContainerBackground` environment variable.

#### Complete Widget Example

Here's a complete example of a widget configured for visionOS:

```swift
struct WeatherWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(
            kind: "com.example.weather",
            provider: WeatherProvider()
        ) { entry in
            WeatherWidgetView(entry: entry)
                .containerBackground(for: .widget) {
                    Color.skyBlue.opacity(0.8)
                }
        }
        .configurationDisplayName("Weather")
        .description("Current weather conditions")
        .supportedFamilies([.systemSmall, .systemMedium, .systemExtraLarge])
        .supportedMountingStyles([.elevated, .recessed])
        .widgetTexture(.glass)
    }
}

struct WeatherWidgetView: View {
    var entry: WeatherProvider.Entry
    @Environment(\.levelOfDetail) var levelOfDetail
    
    var body: some View {
        if levelOfDetail == .simplified {
            // Simplified view for distance viewing
            VStack {
                Image(systemName: entry.weatherIcon)
                    .font(.system(size: 40))
                Text("\(entry.temperature)°")
                    .font(.system(size: 36, weight: .bold))
            }
        } else {
            // Detailed view for close viewing
            VStack(alignment: .leading) {
                HStack {
                    Image(systemName: entry.weatherIcon)
                        .font(.title)
                    Spacer()
                    Text("\(entry.temperature)°")
                        .font(.title)
                }
                
                Spacer()
                
                Text(entry.location)
                    .font(.caption)
                Text(entry.condition)
                    .font(.caption2)
            }
            .padding()
        }
    }
}
```

#### Widget Preview

Use the `Preview` macro to preview your widget in different configurations:

```swift
#Preview("Weather Widget", as: .systemSmall) {
    WeatherWidget()
} timelineProvider: {
    WeatherProvider()
}
```

#### Background Removal

To ensure your widget appears correctly in different contexts, mark your background views as removable:

```swift
var body: some View {
    VStack {
        // Widget content
    }
    .containerBackground(for: .widget) {
        // This background will be automatically removed when needed
        Color.widgetBackground
    }
}
```

If you need to detect whether a widget appears with or without a background, use:

```swift
@Environment(\.showsWidgetContainerBackground) var showsBackground
```

#### References

- [Updating your widgets for visionOS](https://developer.apple.com/documentation/WidgetKit/Updating-your-widgets-for-visionOS)
- [Support recessed and elevated mounting styles](https://developer.apple.com/documentation/WidgetKit/Updating-your-widgets-for-visionOS#Support-recessed-and-elevated-mounting-styles)
- [Support visionOS rendering styles and extra large widgets](https://developer.apple.com/documentation/WidgetKit/Updating-your-widgets-for-visionOS#Support-visionOS-rendering-styles-and-extra-large-widgets)
- [Add proximity awareness to your widget](https://developer.apple.com/documentation/WidgetKit/Updating-your-widgets-for-visionOS#Add-proximity-awareness-to-your-widget)
- [Developing a WidgetKit strategy](https://developer.apple.com/documentation/WidgetKit/Developing-a-WidgetKit-strategy)
- [Displaying the right widget background](https://developer.apple.com/documentation/WidgetKit/Displaying-the-right-widget-background)
