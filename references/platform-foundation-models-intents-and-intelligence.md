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

## Source Content

### App Intents Updates

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/AppIntents-Updates.md`

### AppIntents Updates

#### Overview

AppIntents is a framework that enables apps to extend functionality across the system, allowing users to perform app actions from anywhere, even when not in the app. Recent updates have expanded the capabilities and improved the developer experience for implementing AppIntents.

Key areas of improvement include:
- New system integrations with Apple Intelligence and visual intelligence
- User experience refinements with intent modes and foreground/background execution
- Convenience APIs with new property macros and Swift Package support
- Enhanced interactive snippets
- Improved Spotlight integration

#### New System Integrations

##### Visual Intelligence Integration

AppIntents now supports integration with visual intelligence, allowing users to circle objects in the visual intelligence camera or onscreen and view matching results from your app.

```swift
@UnionValue
enum VisualSearchResult {
    case landmark(LandmarkEntity)
    case collection(CollectionEntity)
}

struct LandmarkIntentValueQuery: IntentValueQuery {
    func values(for input: SemanticContentDescriptor) async throws -> [VisualSearchResult] {
        // Implementation to match visual input to app entities
    }
}

// Implement OpenIntent for each entity type
struct OpenLandmarkIntent: OpenIntent { /* ... */ }
struct OpenCollectionIntent: OpenIntent { /* ... */ }
```

##### Onscreen Entities

Associate app entities with onscreen content using NSUserActivities, enabling users to ask Siri or ChatGPT about things currently visible in your app.

```swift
struct LandmarkDetailView: View {
    let landmark: LandmarkEntity

    var body: some View {
        Group { /* View content */ }
        .userActivity("com.landmarks.ViewingLandmark") { activity in
            activity.title = "Viewing \(landmark.name)"
            activity.appEntityIdentifier = EntityIdentifier(for: landmark)
        }
    }
}
```

#### User Experience Refinements

##### Intent Modes

AppIntents now supports more granular control over how intents execute with the new `supportedModes` property:

```swift
struct GetCrowdStatusIntent: AppIntent {
    static let supportedModes: IntentModes = [.background, .foreground(.dynamic)]

    func perform() async throws -> some ReturnsValue<Int> & ProvidesDialog {
        // Check if the landmark is open
        guard await modelData.isOpen(landmark) else { 
            // Return early if closed
            return .result(value: 0, dialog: "The landmark is currently closed.")
        }

        // Continue in foreground if possible
        if systemContext.currentMode.canContinueInForeground {
            do {
                try await continueInForeground(alwaysConfirm: false)
                await navigator.navigateToCrowdStatus(landmark)
            } catch {
                // Handle case where opening app was denied
            }
        }

        // Retrieve status and return dialog
        let status = await modelData.getCrowdStatus(landmark)
        return .result(value: status, dialog: "Current crowd level: \(status)")
    }
}
```

Available modes include:
- `.background` - Intent performs entirely in the background
- `.foreground(.immediate)` - App is foregrounded immediately before `perform()` runs
- `.foreground(.dynamic)` - App can be foregrounded during execution based on runtime conditions
- `.foreground(.deferred)` - App performs in background initially but will be foregrounded before completion

You can also combine modes:
- `[.background, .foreground]` - Foreground by default, background as fallback
- `[.background, .foreground(.dynamic)]` - Background by default, can request foreground
- `[.background, .foreground(.deferred)]` - Background initially, guaranteed foreground when requested

##### Continuing in Foreground

New APIs to request continuation in the foreground:

```swift
// Request to continue in foreground
try await continueInForeground(alwaysConfirm: false)

// Request to continue in foreground after an error
throw needsToContinueInForegroundError(
    IntentDialog("Need to open app to complete this action"),
    alwaysConfirm: true
)
```

##### Multiple Choice API

Request user input with the new choice API:

```swift
let options = [
    IntentChoiceOption(title: "Option 1", subtitle: "Description 1"),
    IntentChoiceOption(title: "Option 2", subtitle: "Description 2"),
    IntentChoiceOption.cancel(title: "Not now")
]

let choice = try await requestChoice(
    between: options,
    dialog: IntentDialog("Please select an option")
)

// Handle the user's choice
switch choice.id {
case options[0].id: // Option 1 selected
case options[1].id: // Option 2 selected
default: // Cancelled
}
```

#### Convenience APIs

##### New Property Macros

###### ComputedProperty

Use the `@ComputedProperty` macro to create computed properties for AppEntities that directly access the source of truth:

```swift
struct SettingsEntity: UniqueAppEntity {
    @ComputedProperty
    var defaultPlace: PlaceDescriptor {
        UserDefaults.standard.defaultPlace
    }

    init() { }
}
```

###### DeferredProperty

Use the `@DeferredProperty` macro for properties that are expensive to calculate and should only be fetched when explicitly requested:

```swift
struct LandmarkEntity: IndexedEntity {
    @DeferredProperty
    var crowdStatus: Int {
        get async throws {
            await modelData.getCrowdStatus(self)
        }
    }
}
```

##### Swift Package Support

AppIntents can now be included in Swift Packages and static libraries:

```swift
// Framework or dynamic library
public struct LandmarksKitPackage: AppIntentsPackage { }

// App target
struct LandmarksPackage: AppIntentsPackage {
    static var includedPackages: [any AppIntentsPackage.Type] {
        [LandmarksKitPackage.self]
    }
}
```

#### Interactive Snippets

##### Static Snippets

Return a static snippet to show the outcome of an app intent:

```swift
func perform() async throws -> some IntentResult {
    // Perform the intent's action
    
    return .result(view: Text("Some example text.").font(.title))
}
```

##### Interactive Snippets

Return an interactive snippet that allows users to perform follow-up actions:

```swift
func perform() async throws -> some IntentResult {
    // Find information about a nearby landmark
    let landmark = await findNearestLandmark()
    
    // Return an interactive snippet with buttons for follow-up actions
    return .result(
        value: landmark,
        opensIntent: OpenLandmarkIntent(landmark: landmark),
        snippetIntent: LandmarkSnippetIntent(landmark: landmark)
    )
}

// Define the snippet intent
struct LandmarkSnippetIntent: SnippetIntent {
    @Parameter var landmark: LandmarkEntity
    
    var snippet: some View {
        VStack {
            Text(landmark.name).font(.headline)
            Text(landmark.description).font(.body)
            
            HStack {
                Button("Add to Favorites") {
                    // Add to favorites action
                }
                
                Button("Search Tickets") {
                    // Search tickets action
                }
            }
        }
        .padding()
    }
}
```

#### Spotlight Integration

##### Making App Entities Available in Spotlight

1. Create an intent that displays your entity in your app:

```swift
struct OpenLandmarkIntent: OpenIntent {
    static let title: LocalizedStringResource = "Open Landmark"

    @Parameter(title: "Landmark", requestValueDialog: "Which landmark?")
    var target: LandmarkEntity

    func perform() async throws -> some IntentResult {
        return .result()
    }
}
```

2. Make your app entity indexable:

```swift
struct LandmarkEntity: AppEntity, IndexedEntity {
    static var typeDisplayRepresentation = TypeDisplayRepresentation(
        name: "Landmark",
        systemImage: "mountain.2"
    )
    
    var id: String
    var name: String
    var description: String
    var coordinate: CLLocationCoordinate2D
    var activities: [String]
    var regionDescription: String
    
    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(
            title: "\(name)",
            subtitle: "\(regionDescription)",
            image: .init(systemName: "mountain.2")
        )
    }
}
```

3. Implement the searchable attribute set:

```swift
extension LandmarkEntity {
    var searchableAttributes: CSSearchableItemAttributeSet {
        let attributes = CSSearchableItemAttributeSet()
        
        attributes.title = name
        attributes.namedLocation = regionDescription
        attributes.keywords = activities
        
        attributes.latitude = NSNumber(value: coordinate.latitude)
        attributes.longitude = NSNumber(value: coordinate.longitude)
        attributes.supportsNavigation = true
        
        return attributes
    }
}
```

4. Add entities to the Spotlight index:

```swift
func indexLandmarks() async {
    let landmarks = await fetchLandmarks()
    
    do {
        try await CSSearchableIndex.default().indexAppEntities(
            landmarks,
            priority: .normal
        )
    } catch {
        print("Failed to index landmarks: \(error)")
    }
}
```

5. Update the index when data changes:

```swift
func deleteLandmark(_ landmark: LandmarkEntity) async {
    // Delete from data store
    await dataStore.delete(landmark)
    
    // Remove from Spotlight index
    do {
        try await CSSearchableIndex.default().deleteAppEntities(
            identifiedBy: [landmark.id],
            ofType: LandmarkEntity.self
        )
    } catch {
        print("Failed to remove landmark from index: \(error)")
    }
}
```

#### Code Examples

##### Basic App Intent

```swift
struct FindNearestLandmarkIntent: AppIntent {
    static var title: LocalizedStringResource = "Find Nearest Landmark"
    
    @Parameter(title: "Category")
    var category: String?
    
    func perform() async throws -> some IntentResult {
        let landmark = await findNearestLandmark(category: category)
        return .result(value: landmark)
    }
}
```

##### App Shortcut

```swift
struct AppShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: FindNearestLandmarkIntent(),
            phrases: ["Find the closest landmark with \(.applicationName)"],
            systemImageName: "location"
        )
    }
}
```

##### Entity with Indexable Properties

```swift
struct LandmarkEntity: AppEntity, IndexedEntity {
    static var typeDisplayRepresentation = TypeDisplayRepresentation(
        name: "Landmark",
        systemImage: "mountain.2"
    )
    
    var id: String
    
    @Property(title: "Name")
    var name: String
    
    @Property(title: "Description")
    var description: String
    
    @Property(title: "Location", indexingKey: \CSSearchableItemAttributeSet.namedLocation)
    var regionDescription: String
    
    @ComputedProperty(title: "Is Favorite")
    var isFavorite: Bool {
        UserDefaults.standard.favorites.contains(id)
    }
    
    @DeferredProperty(title: "Current Weather")
    var weather: String {
        get async throws {
            try await WeatherService.getWeather(for: coordinate)
        }
    }
    
    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(
            title: "\(name)",
            subtitle: "\(regionDescription)",
            image: .init(systemName: "mountain.2")
        )
    }
}
```

#### References

- [App Intents updates](https://developer.apple.com/documentation/Updates/AppIntents)
- [Adopting App Intents to support system experiences](https://developer.apple.com/documentation/AppIntents/adopting-app-intents-to-support-system-experiences)
- [Making app entities available in Spotlight](https://developer.apple.com/documentation/AppIntents/making-app-entities-available-in-spotlight)
- [Displaying static and interactive snippets](https://developer.apple.com/documentation/AppIntents/displaying-static-and-interactive-snippets)
- [WWDC 2025: Explore new advances in App Intents](https://developer.apple.com/videos/play/wwdc2025/275)
- [WWDC 2025: Get to know App Intents](https://developer.apple.com/videos/play/wwdc2025/244)

### Foundation Models Using On Device Llm In Your App

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/FoundationModels-Using-on-device-LLM-in-your-app.md`

### Foundation Models: Using Apple's On-Device LLM in Your Apps

#### Overview

Foundation Models is an Apple framework that provides access to on-device large language models (LLMs) that power Apple Intelligence. This framework enables developers to enhance their apps with generative AI capabilities without requiring cloud connectivity or compromising user privacy.

Key capabilities include:
- Text generation and understanding
- Content summarization and extraction
- Structured data generation
- Custom tool integration

#### Getting Started

##### Check Model Availability

Always check if the model is available before attempting to use it. Model availability depends on device factors such as Apple Intelligence support, system settings, and device state.

```swift
struct GenerativeView: View {
    // Create a reference to the system language model
    private var model = SystemLanguageModel.default

    var body: some View {
        switch model.availability {
        case .available:
            // Show your intelligence UI
            Text("Model is available")
        case .unavailable(.deviceNotEligible):
            // Show an alternative UI
            Text("Device not eligible for Apple Intelligence")
        case .unavailable(.appleIntelligenceNotEnabled):
            // Ask the person to turn on Apple Intelligence
            Text("Please enable Apple Intelligence in Settings")
        case .unavailable(.modelNotReady):
            // The model isn't ready (downloading or other system reasons)
            Text("Model is downloading or not ready")
        case .unavailable(let other):
            // The model is unavailable for an unknown reason
            Text("Model unavailable: \(other)")
        }
    }
}
```

##### Create a Session

After confirming model availability, create a `LanguageModelSession` to interact with the model:

```swift
// Create a basic session with the system model
let session = LanguageModelSession()

// Create a session with instructions
let instructions = """
    You are a helpful assistant that provides concise answers.
    Keep responses under 100 words and focus on clarity.
    """
let sessionWithInstructions = LanguageModelSession(instructions: instructions)
```

- For single-turn interactions, create a new session each time
- For multi-turn interactions, reuse the same session to maintain context

#### Basic Usage

##### Provide Instructions to the Model

Instructions help steer the model's behavior for your specific use case. The model prioritizes instructions over prompts.

Good instructions typically specify:
- The model's role (e.g., "You are a mentor")
- What the model should do (e.g., "Help extract calendar events")
- Style preferences (e.g., "Respond as briefly as possible")
- Safety measures (e.g., "Respond with 'I can't help with that' for dangerous requests")

```swift
let instructions = """
    You are a cooking assistant.
    Provide recipe suggestions based on ingredients.
    Keep suggestions brief and practical for home cooks.
    Include approximate cooking time.
    """

let session = LanguageModelSession(instructions: instructions)
```

##### Provide a Prompt to the Model

A prompt is the input that the model responds to. Effective prompts are:
- Conversational (questions or commands)
- Focused on a single, specific task
- Clear about the desired output format and length

```swift
// Simple prompt
let prompt = "What's a good month to visit Paris?"

// Specific prompt with output constraints
let specificPrompt = "Write a profile for the dog breed Siberian Husky using three sentences."
```

##### Generate a Response

Call the model asynchronously to get a response:

```swift
// Basic response generation
let response = try await session.respond(to: prompt)
print(response.content)

// With custom generation options
let options = GenerationOptions(temperature: 0.7)
let customResponse = try await session.respond(to: prompt, options: options)
```

Note: A session can only handle one request at a time. Check `isResponding` to verify the session is available before sending a new request.

#### Advanced Features

##### Guided Generation

Guided generation allows you to receive model responses as structured Swift data instead of raw strings. This provides stronger guarantees about the format of the response.

###### 1. Define a Generable Type

```swift
@Generable(description: "Basic profile information about a cat")
struct CatProfile {
    // A guide isn't necessary for basic fields
    var name: String

    @Guide(description: "The age of the cat", .range(0...20))
    var age: Int

    @Guide(description: "A one sentence profile about the cat's personality")
    var profile: String
}
```

###### 2. Request a Response in Your Custom Type

```swift
// Generate a response using the custom type
let catResponse = try await session.respond(
    to: "Generate a cute rescue cat",
    generating: CatProfile.self
)

// Use the structured data
print("Name: \(catResponse.content.name)")
print("Age: \(catResponse.content.age)")
print("Profile: \(catResponse.content.profile)")
```

###### 3. Printing a Response from your Custom Type

When printing values from a LanguageModelSession.Response always use the instance property content. Not output.

For example:

```swift
import FoundationModels
import Playgrounds

@Generable
struct CookbookSuggestions {
    @Guide(description: "Cookbook Suggestions", .count(3))
    var suggestions: [String]
}

#Playground {
    let session = LanguageModelSession()

    let prompt = "What's a good name for a cooking app?"

    let response = try await session.respond(
        to: prompt,
        generating: CookbookSuggestions.self
    )

    // Notice how print values come from content. Not output.
    print(response.content.suggestions)
}
```

##### Tool Calling

Tool calling allows the model to use custom code you provide to perform specific tasks, access external data, or integrate with other frameworks.

###### 1. Create a Custom Tool

```swift
// Define a tool for searching recipes
struct RecipeSearchTool: Tool {
    struct Arguments: Codable {
        var searchTerm: String
        var numberOfResults: Int
    }
    
    func call(arguments: Arguments) async throws -> ToolOutput {
        // Search your recipe database
        let recipes = await searchRecipes(term: arguments.searchTerm, 
                                         limit: arguments.numberOfResults)
        
        // Return results as a string the model can use
        return .string(recipes.map { "- \($0.name): \($0.description)" }.joined(separator: "\n"))
    }
    
    private func searchRecipes(term: String, limit: Int) async -> [Recipe] {
        // Implementation to search your database
        // ...
    }
}
```

###### 2. Provide the Tool to a Session

```swift
// Create the tool
let recipeSearchTool = RecipeSearchTool()

// Create a session with the tool
let session = LanguageModelSession(tools: [recipeSearchTool])

// The model will automatically use the tool when appropriate
let response = try await session.respond(to: "Find me some pasta recipes")
```

###### 3. Handle Tool Errors

```swift
do {
    let answer = try await session.respond("Find a recipe for tomato soup.")
} catch let error as LanguageModelSession.ToolCallError {
    // Access the name of the tool
    print(error.tool.name) 
    
    // Access the underlying error
    if case .databaseIsEmpty = error.underlyingError as? RecipeSearchToolError {
        // Handle specific error
    }
} catch {
    print("Other error: \(error)")
}
```

#### Snapshot streaming

- LLM generate text as short groups of characters called tokens.
- Typically, when streaming tokens, tokens are delivered in what's called a delta. But Foundation Models does this different.
- As deltas are produced, the responsibility for accumulating them usually falls on the developer
- You append each delta as they come in. And the response grows as you do. But it gets tricky when the result has structure.
- If you want to show the greeting string after each delta, you have to parse it out of the accumulation, and that's not trival, especially for complicated structures.
- Structured output is at the core of the Foundation Model framework. Which is why we stream snapshots.

#### Snapshot streaming

- LLM generate text as short groups of characters called tokens.
- Typically, when streaming tokens, tokens are delivered in what's called a delta. But Foundation Models does this different.
- As deltas are produced, the responsibility for accumulating them usually falls on the developer
- You append each delta as they come in. And the response grows as you do. But it gets tricky when the result has structure.
- If you want to show the greeting string after each delta, you have to parse it out of the accumulation, and that's not trival, especially for complicated structures.
- Structured output is at the core of the Foundation Model framework. Which is why we stream snapshots.

##### What are snapshots

- Snapshots represent partically generated response. Their properties are all optinoal. And they get filled in as the model produces more of the response.
- Snapshots are a robust and convenient representation for streaming structure output.
- You are already familar with the `@Generable` macro, and as it turns out, it's also where the definitions for partially generated types come from.
- If you expand the macro, you'll discover it produces a types named `PartiallyGenerated`. It is effectively a mirror of the outer structure except every property is optional.
- The partically generated type comes into play when you call the 'streamResponse` method on your session.

```swift
import FoundationModels
import Playgrounds

@Generable
struct TripIdeas {
    @Guide(description: "Ideas for upcoming trips")
    var ideas: [String]
}

#Playground {
    let session = LanguageModelSession()

    let prompt = "What are some exciting trip ideas for the upcoming year?"

    let stream = session.streamResponse(
        to: prompt,
        generating: TripIdeas.self
    )

    for try await partial in stream {
        print(partial)
    }
}
```

- Stream response returns an async sequence. And the elements of that sequence are instances of a partially generated type.
- Each element in the sequence will contain an updated snapshot.
- These snapshots work great with declarative frameworks like SwiftUI.
- First, create state holding a partially generated type.
- Then, just iterate over a response stream, stores its elements, and watch as your UI comes to life.

#### Best Practices and Limitations

##### Context Size Limits

- The system model supports up to 4,096 tokens per session
- A token is roughly 3-4 characters in languages like English
- All instructions, prompts, and outputs count toward this limit
- If you exceed the limit, you'll get a `LanguageModelSession.GenerationError.exceededContextWindowSize` error
- For large data processing, break it into smaller chunks across multiple sessions

##### Optimizing Performance

- Use `GenerationOptions` to tune model behavior:
  ```swift
  let options = GenerationOptions(temperature: 2.0) // Higher temperature = more creative
  ```
- Use Xcode Instruments to monitor request performance
- Access `Transcript` entries to see model actions during a session:
  ```swift
  let transcript = session.transcript
  ```

##### Prompt Engineering Tips

- Be specific about what you want
- Specify output constraints (e.g., "in three sentences")
- Break complex tasks into multiple simple prompts
- Use examples in instructions to guide the model's output format

#### References

- [Generating content and performing tasks with Foundation Models](https://developer.apple.com/documentation/FoundationModels/generating-content-and-performing-tasks-with-foundation-models)
- [Generating Swift data structures with guided generation](https://developer.apple.com/documentation/FoundationModels/generating-swift-data-structures-with-guided-generation)
- [Expanding generation with tool calling](https://developer.apple.com/documentation/FoundationModels/expanding-generation-with-tool-calling)
- [Human Interface Guidelines: Generative AI](https://developer.apple.com/design/human-interface-guidelines/technologies/generative-ai)

### Implementing Assistive Access In I Os

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/Implementing-Assistive-Access-in-iOS.md`

### Implementing Assistive Access in iOS

#### Overview

Assistive Access is an accessibility feature introduced in iOS and iPadOS 17 designed specifically for people with cognitive disabilities. It provides a streamlined system experience with simplified interfaces, clear pathways, and consistent design practices to reduce cognitive load.

Key characteristics of Assistive Access:
- Streamlined interactions
- Clear pathways to success
- Consistent design language
- Large controls
- Visual alternatives to text
- Reduced cognitive strain

#### Setting Up Assistive Access in Your App

##### 1. Enable Assistive Access Support

Add the following key to your app's `Info.plist`:

```xml
<key>UISupportsAssistiveAccess</key>
<true/>
```

This ensures your app is listed under "Optimized Apps" in Accessibility Settings and launches in full screen when Assistive Access is enabled.

##### 2. Full Screen Support (Optional)

If your app is already designed for cognitive disabilities (e.g., AAC apps) and you want to display it in full screen without modifications:

```xml
<key>UISupportsFullScreenInAssistiveAccess</key>
<true/>
```

This will display your app in full screen rather than in a reduced frame, with the same appearance as when Assistive Access is turned off.

#### Creating an Assistive Access Scene

##### SwiftUI Implementation

1. Add an `AssistiveAccess` scene to your app:

```swift
import SwiftUI

@main
struct MyApp: App {
  var body: some Scene {
    WindowGroup {
      ContentView()
    }
    
    AssistiveAccess {
      AssistiveAccessContentView()
    }
  }
}
```

2. Create a dedicated view for Assistive Access:

```swift
struct AssistiveAccessContentView: View {
  var body: some View {
    // Your streamlined interface for Assistive Access
    NavigationStack {
      List {
        // Simplified controls and options
      }
      .navigationTitle("My App")
    }
  }
}
```

3. Preview your Assistive Access scene:

```swift
#Preview(traits: .assistiveAccess)
AssistiveAccessContentView()
```

##### UIKit Implementation

1. Declare a SwiftUI scene with UIKit:

```swift
import UIKit
import SwiftUI

class AssistiveAccessSceneDelegate: UIHostingSceneDelegate {
  static var rootScene: some Scene {
    AssistiveAccess {
      AssistiveAccessContentView()
    }
  }
}
```

2. Activate the scene:

```swift
import UIKit

@main
class AppDelegate: UIApplicationDelegate {
  func application(_ application: UIApplication, configurationForConnecting connectingSceneSession: UISceneSession, options: UIScene.ConnectionOptions) -> UISceneConfiguration {
    let role = connectingSceneSession.role
    let sceneConfiguration = UISceneConfiguration(name: nil, sessionRole: role)
    if role == .windowAssistiveAccessApplication {
      sceneConfiguration.delegateClass = AssistiveAccessSceneDelegate.self
    }
    return sceneConfiguration
  }
}
```

#### Detecting Assistive Access at Runtime

You can check if Assistive Access is enabled using the environment value:

```swift
struct MyView: View {
  @Environment(\.accessibilityAssistiveAccessEnabled) var assistiveAccessEnabled
  
  var body: some View {
    if assistiveAccessEnabled {
      // Show Assistive Access optimized UI
    } else {
      // Show standard UI
    }
  }
}
```

#### Navigation Icons for Assistive Access

Add navigation icons to make your interface more visually accessible:

```swift
NavigationStack {
  MyView()
    .navigationTitle("My Feature")
    .assistiveAccessNavigationIcon(systemImage: "star.fill")
}
```

Or with a custom image:

```swift
.assistiveAccessNavigationIcon(Image("my-custom-icon"))
```

#### Design Principles for Assistive Access

When designing for Assistive Access, follow these key principles:

1. **Distill to Core Functionality**
   - Focus on one or two essential features
   - Remove distractions and unnecessary options
   - Streamline the experience

2. **Clear, Prominent Controls**
   - Use large, easy-to-tap buttons
   - Provide ample spacing between interactive elements
   - Avoid hidden gestures or timed interactions

3. **Multiple Representations**
   - Present information in multiple ways (text, icons, etc.)
   - Use visual alternatives to text
   - Ensure icons are clear and meaningful

4. **Intuitive Navigation**
   - Create step-by-step pathways
   - Provide clear back buttons
   - Maintain consistent navigation patterns

5. **Safe Interactions**
   - Remove irreversible actions when possible
   - Provide multiple confirmations for destructive actions
   - Offer clear feedback for all interactions

#### Control Styling in Assistive Access

When using the Assistive Access scene, native SwiftUI controls are automatically displayed in the distinctive Assistive Access design:

- Buttons, lists, and navigation titles appear in a more prominent style
- Controls adhere to the grid or row screen layout configured in Assistive Access settings
- No additional styling work is required

#### Testing Assistive Access Implementation

1. **Preview in Xcode**
   Use the `.assistiveAccess` trait in SwiftUI previews:
   ```swift
   #Preview(traits: .assistiveAccess)
   AssistiveAccessContentView()
   ```

2. **Test on Device**
   - Enable Assistive Access in Settings > Accessibility > Assistive Access
   - Verify your app appears in the "Optimized Apps" list
   - Test the full user flow in Assistive Access mode

3. **Accessibility Inspector**
   Use Xcode's Accessibility Inspector to identify and fix accessibility issues

#### Best Practices

- Design for clarity and simplicity
- Focus on essential functionality
- Use consistent UI patterns
- Provide visual alternatives to text
- Test with actual users who have cognitive disabilities
- Combine Assistive Access with other accessibility features

#### References

- [AssistiveAccess (SwiftUI)](https://developer.apple.com/documentation/SwiftUI/AssistiveAccess)
- [assistiveAccessNavigationIcon(_:)](https://developer.apple.com/documentation/SwiftUI/View/assistiveAccessNavigationIcon(_:))
- [accessibilityAssistiveAccessEnabled](https://developer.apple.com/documentation/SwiftUI/EnvironmentValues/accessibilityAssistiveAccessEnabled)
- [WWDC 2025 Session: Customize your app for Assistive Access](https://developer.apple.com/videos/play/wwdc2025/238)
- [What's new in SwiftUI (WWDC 2025)](https://developer.apple.com/videos/play/wwdc2025/256)
- [Principles of inclusive app design](https://developer.apple.com/videos/play/wwdc2025/316)

### Implementing Visual Intelligence In I Os

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/Implementing-Visual-Intelligence-in-iOS.md`

### Implementing Visual Intelligence in iOS

#### Overview

Visual Intelligence is a framework that enables iOS apps to integrate with the system's visual search capabilities. It allows users to find app content that matches their surroundings or objects onscreen by using the visual intelligence camera or screenshots. When a user performs a visual search, your app can provide relevant content that matches what they're looking at.

Key concepts:
- Visual Intelligence framework provides information about objects detected in the camera or screenshots
- App Intents framework facilitates the exchange of information between the system and your app
- Your app searches its content for matches and returns them as app entities
- Results appear directly in the visual search interface, allowing users to view and interact with your content

#### Setting Up Visual Intelligence

##### Required Frameworks

```swift
import VisualIntelligence
import AppIntents
```

##### Implementation Steps

1. Create an `IntentValueQuery` to receive visual search requests
2. Implement the `values(for:)` method to process the `SemanticContentDescriptor`
3. Search your app's content using the provided information
4. Return matching content as app entities

#### Working with SemanticContentDescriptor

The `SemanticContentDescriptor` is the core object that provides information about what the user is looking at.

##### Key Properties

```swift
// A list of labels that Visual Intelligence uses to classify items
let labels: [String]

// The pixel buffer containing the visual data
var pixelBuffer: CVReadOnlyPixelBuffer?
```

##### Accessing Visual Data

You can use either the labels or the pixel buffer (or both) to search for matching content:

```swift
// Using labels
func searchByLabels(_ labels: [String]) -> [AppEntity] {
    // Search your app's content using the provided labels
    return matchingEntities
}

// Using pixel buffer
func searchByImage(_ pixelBuffer: CVReadOnlyPixelBuffer) -> [AppEntity] {
    // Convert pixel buffer to an image and search your content
    return matchingEntities
}
```

#### Creating an IntentValueQuery

The `IntentValueQuery` protocol is the entry point for Visual Intelligence to communicate with your app.

##### Basic Implementation

```swift
struct LandmarkIntentValueQuery: IntentValueQuery {
    @Dependency var modelData: ModelData
    
    func values(for input: SemanticContentDescriptor) async throws -> [VisualSearchResult] {
        // Check if pixel buffer is available
        guard let pixelBuffer = input.pixelBuffer else {
            return []
        }
        
        // Search for matching landmarks using the pixel buffer
        let landmarks = try await modelData.search(matching: pixelBuffer)
        
        return landmarks
    }
}
```

##### Using Union Values for Different Result Types

If your app needs to return different types of results, use a union value:

```swift
@UnionValue
enum VisualSearchResult {
    case landmark(LandmarkEntity)
    case collection(CollectionEntity)
}
```

#### Providing Display Representations

Visual Intelligence uses the `DisplayRepresentation` of your `AppEntity` to present your content in the search results.

##### Creating a Display Representation

```swift
struct LandmarkEntity: AppEntity {
    static var typeDisplayRepresentation: TypeDisplayRepresentation {
        return TypeDisplayRepresentation(
            name: LocalizedStringResource("Landmark", table: "AppIntents"),
            numericFormat: "\(placeholder: .int) landmarks"
        )
    }
    
    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(
            title: "\(name)",
            subtitle: "\(location)",
            image: .init(named: landmark.thumbnailImageName)
        )
    }
    
    // Other required AppEntity properties and methods
}
```

#### Opening Items in Your App

When a user taps on a search result, your app should open to display detailed information about that item.

##### Implementing AppEntity for Deep Linking

```swift
struct LandmarkEntity: AppEntity {
    var id: String
    var name: String
    var location: String
    var thumbnailImageName: String
    
    // Required for deep linking
    static var typeDisplayRepresentation: TypeDisplayRepresentation {
        // As shown above
    }
    
    var displayRepresentation: DisplayRepresentation {
        // As shown above
    }
    
    // Define how to open this entity in your app
    var appLinkURL: URL? {
        URL(string: "yourapp://landmark/\(id)")
    }
}
```

#### Linking to Additional Results

If your app finds many matches, you can provide a "More results" button that opens your app to show the full list.

##### Creating a Semantic Content Search Intent

```swift
struct ViewMoreLandmarksIntent: AppIntent, VisualIntelligenceSearchIntent {
    static var title: LocalizedStringResource = "View More Landmarks"
    
    @Parameter(title: "Semantic Content")
    var semanticContent: SemanticContentDescriptor
    
    func perform() async throws -> some IntentResult {
        // Open your app's search view with the semantic content
        return .result()
    }
}
```

#### Complete Example

Here's a complete example of implementing Visual Intelligence in a landmarks app:

```swift
import SwiftUI
import AppIntents
import VisualIntelligence

// Define the search result types
@UnionValue
enum VisualSearchResult {
    case landmark(LandmarkEntity)
    case collection(CollectionEntity)
}

// Define the landmark entity
struct LandmarkEntity: AppEntity {
    var id: String
    var name: String
    var location: String
    var thumbnailImageName: String
    
    static var typeDisplayRepresentation: TypeDisplayRepresentation {
        return TypeDisplayRepresentation(
            name: LocalizedStringResource("Landmark", table: "AppIntents"),
            numericFormat: "\(placeholder: .int) landmarks"
        )
    }
    
    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(
            title: "\(name)",
            subtitle: "\(location)",
            image: .init(named: thumbnailImageName)
        )
    }
    
    var appLinkURL: URL? {
        URL(string: "yourapp://landmark/\(id)")
    }
}

// Define the collection entity
struct CollectionEntity: AppEntity {
    var id: String
    var name: String
    var landmarks: [LandmarkEntity]
    
    static var typeDisplayRepresentation: TypeDisplayRepresentation {
        return TypeDisplayRepresentation(
            name: LocalizedStringResource("Collection", table: "AppIntents"),
            numericFormat: "\(placeholder: .int) collections"
        )
    }
    
    var displayRepresentation: DisplayRepresentation {
        DisplayRepresentation(
            title: "\(name)",
            subtitle: "\(landmarks.count) landmarks",
            image: .init(systemName: "square.stack.fill")
        )
    }
    
    var appLinkURL: URL? {
        URL(string: "yourapp://collection/\(id)")
    }
}

// Define the intent value query
struct LandmarkIntentValueQuery: IntentValueQuery {
    @Dependency var modelData: ModelData
    
    func values(for input: SemanticContentDescriptor) async throws -> [VisualSearchResult] {
        // Try to use labels first
        if !input.labels.isEmpty {
            let landmarks = try await modelData.search(matching: input.labels)
            return landmarks
        }
        
        // Fall back to pixel buffer if available
        guard let pixelBuffer = input.pixelBuffer else {
            return []
        }
        
        let landmarks = try await modelData.search(matching: pixelBuffer)
        return landmarks
    }
}

// Define the "more results" intent
struct ViewMoreLandmarksIntent: AppIntent, VisualIntelligenceSearchIntent {
    static var title: LocalizedStringResource = "View More Landmarks"
    
    @Parameter(title: "Semantic Content")
    var semanticContent: SemanticContentDescriptor
    
    func perform() async throws -> some IntentResult {
        // Open your app's search view with the semantic content
        return .result()
    }
}

// Example model data service
class ModelData {
    func search(matching labels: [String]) async throws -> [VisualSearchResult] {
        // Search your database for landmarks matching the labels
        // Return matching landmarks as VisualSearchResult objects
        return []
    }
    
    func search(matching pixelBuffer: CVReadOnlyPixelBuffer) async throws -> [VisualSearchResult] {
        // Use image recognition to find landmarks in the pixel buffer
        // Return matching landmarks as VisualSearchResult objects
        return []
    }
}
```

#### Best Practices

1. **Performance**: Return results quickly for a good search experience
   - Limit the number of returned items (consider showing 10-20 most relevant results)
   - Use the "More results" button for additional items
   - Optimize your search algorithms for speed

2. **Quality**: Provide high-quality display representations
   - Use clear, concise titles and subtitles
   - Include relevant images that help identify the content
   - Ensure all text is properly localized

3. **Relevance**: Focus on returning the most relevant results
   - Prioritize exact matches over partial matches
   - Consider the context of the search (location, time, etc.)
   - Filter out irrelevant or low-confidence matches

4. **User Experience**: Make it easy to navigate from search results to your app
   - Implement deep linking to open specific content
   - Maintain context when transitioning to your app
   - Provide a consistent experience between search results and your app

#### Testing

To test your Visual Intelligence integration:
1. Build and run your app on a device
2. Use the visual intelligence camera or take a screenshot
3. Perform a visual search on content relevant to your app
4. Verify that your app's results appear in the search results
5. Test tapping on results to ensure they open correctly in your app

#### References

- [Integrating your app with visual intelligence](https://developer.apple.com/documentation/VisualIntelligence/integrating-your-app-with-visual-intelligence)
- [SemanticContentDescriptor](https://developer.apple.com/documentation/VisualIntelligence/SemanticContentDescriptor)
- [IntentValueQuery](https://developer.apple.com/documentation/AppIntents/IntentValueQuery)
- [DisplayRepresentation](https://developer.apple.com/documentation/AppIntents/DisplayRepresentation)
- [TypeDisplayRepresentation](https://developer.apple.com/documentation/appintents/TypeDisplayRepresentation)
- [App Intents framework](https://developer.apple.com/documentation/AppIntents)
- [Making actions and content discoverable and widely available](https://developer.apple.com/documentation/AppIntents/Making-actions-and-content-discoverable-and-widely-available)
