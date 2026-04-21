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

## Source Content

### SwiftUI Alarm Kit Integration

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/SwiftUI-AlarmKit-Integration.md`

### Using AlarmKit in a SwiftUI App

#### Overview

AlarmKit is a framework introduced in iOS 18 that allows developers to create custom alarms and timers within their apps. It provides a comprehensive system for managing alarms with customizable schedules and UI. AlarmKit supports one-time and repeating alarms, with options for countdown durations and snooze functionality. It handles alarm authorization and provides UI for both templated and widget presentations.

Key features:
- Schedule one-time or repeating alarms
- Create countdown timers
- Customize alarm UI and presentation
- Integrate with Live Activities for Dynamic Island and Lock Screen
- Override device focus and silent mode

#### Key Components

##### AlarmManager

The central class for interacting with the alarm system:

```swift
// Access the shared instance
let alarmManager = AlarmManager.shared
```

##### Alarm

A structure that describes an alarm that can alert once or on a repeating schedule:

```swift
struct Alarm {
    var id: UUID
    var schedule: Schedule?
    var countdownDuration: CountdownDuration?
    // Other properties
}
```

##### AlarmPresentation

Defines the content required for the alarm UI in different states:

```swift
struct AlarmPresentation {
    var alert: Alert
    var countdown: Countdown?
    var paused: Paused?
}
```

##### AlarmAttributes

Contains all information necessary for the alarm UI:

```swift
struct AlarmAttributes<Metadata: AlarmMetadata> {
    var presentation: AlarmPresentation
    var metadata: Metadata
    var tintColor: Color
}
```

#### Authorization

Before scheduling alarms, your app needs to request authorization:

```swift
// Add to Info.plist
// NSAlarmKitUsageDescription: "We'll schedule alerts for alarms you create within our app."

func requestAlarmAuthorization() async -> Bool {
    do {
        let state = try await AlarmManager.shared.requestAuthorization()
        return state == .authorized
    } catch {
        print("Error occurred while requesting authorization: \(error)")
        return false
    }
}
```

You can also check the current authorization status:

```swift
func checkAuthorizationStatus() async {
    let status = await AlarmManager.shared.authorizationState
    switch status {
    case .authorized:
        print("Authorized to schedule alarms")
    case .denied:
        print("Permission denied")
    case .notDetermined:
        print("Permission not yet requested")
    @unknown default:
        print("Unknown status")
    }
}
```

> NOTE: Use `authorizationState` — never use `authorizationStatus` when checking the authorization status.

#### Creating Alarms

##### One-time Alarm

```swift
func createOneTimeAlarm(hour: Int, minute: Int) async throws -> Alarm {
    // Create a unique ID
    let id = UUID()
    
    // Create the schedule for a specific time
    let time = Alarm.Schedule.Relative.Time(hour: hour, minute: minute)
    let schedule = Alarm.Schedule.relative(.init(
        time: time,
        repeats: .never
    ))
    
    // Create the alarm presentation
    let alertContent = AlarmPresentation.Alert(
        title: "Wake Up",
        stopButton: .stopButton,
        secondaryButton: .openAppButton,
        secondaryButtonBehavior: .custom
    )
    
    let presentation = AlarmPresentation(alert: alertContent)
    
    // Create attributes with presentation and metadata
    struct EmptyMetadata: AlarmMetadata {}
    let attributes = AlarmAttributes(
        presentation: presentation,
        metadata: EmptyMetadata(),
        tintColor: .blue
    )
    
    // Create the configuration
    let configuration = AlarmManager.AlarmConfiguration(
        countdownDuration: nil,
        schedule: schedule,
        attributes: attributes,
        sound: .default
    )
    
    // Schedule the alarm
    return try await AlarmManager.shared.schedule(id: id, configuration: configuration)
}
```

##### Repeating Alarm

```swift
func createWeeklyAlarm(hour: Int, minute: Int, weekdays: Set<Locale.Weekday>) async throws -> Alarm {
    let id = UUID()
    
    // Create the schedule for repeating on specific days
    let time = Alarm.Schedule.Relative.Time(hour: hour, minute: minute)
    let schedule = Alarm.Schedule.relative(.init(
        time: time,
        repeats: .weekly(Array(weekdays))
    ))
    
    // Create the alarm presentation
    let alertContent = AlarmPresentation.Alert(
        title: "Weekly Reminder",
        stopButton: .stopButton,
        secondaryButton: .snoozeButton,
        secondaryButtonBehavior: .countdown
    )
    
    // Create countdown duration for snooze (9 minutes)
    let countdownDuration = Alarm.CountdownDuration(
        preAlert: nil,
        postAlert: 9 * 60
    )
    
    let presentation = AlarmPresentation(alert: alertContent)
    
    // Create attributes with presentation and metadata
    struct EmptyMetadata: AlarmMetadata {}
    let attributes = AlarmAttributes(
        presentation: presentation,
        metadata: EmptyMetadata(),
        tintColor: .green
    )
    
    // Create the configuration
    let configuration = AlarmManager.AlarmConfiguration(
        countdownDuration: countdownDuration,
        schedule: schedule,
        attributes: attributes,
        sound: .default
    )
    
    // Schedule the alarm
    return try await AlarmManager.shared.schedule(id: id, configuration: configuration)
}
```

##### Timer (Countdown)

```swift
func createCountdownTimer(seconds: TimeInterval) async throws -> Alarm {
    let id = UUID()
    
    // Create countdown duration
    let countdownDuration = Alarm.CountdownDuration(
        preAlert: seconds,
        postAlert: 10 // Optional post-alert countdown for snooze
    )
    
    // Create the alarm presentation with all states
    let alertContent = AlarmPresentation.Alert(
        title: "Timer Complete",
        stopButton: .stopButton,
        secondaryButton: .repeatButton,
        secondaryButtonBehavior: .countdown
    )
    
    let countdownContent = AlarmPresentation.Countdown(
        title: "Timer Running",
        pauseButton: .pauseButton
    )
    
    let pausedContent = AlarmPresentation.Paused(
        title: "Timer Paused",
        resumeButton: .resumeButton
    )
    
    let presentation = AlarmPresentation(
        alert: alertContent,
        countdown: countdownContent,
        paused: pausedContent
    )
    
    // Create attributes with presentation and metadata
    struct TimerMetadata: AlarmMetadata {
        let purpose: String
    }
    
    let attributes = AlarmAttributes(
        presentation: presentation,
        metadata: TimerMetadata(purpose: "Cooking Timer"),
        tintColor: .orange
    )
    
    // Create the configuration
    let configuration = AlarmManager.AlarmConfiguration(
        countdownDuration: countdownDuration,
        schedule: nil, // No schedule for a timer
        attributes: attributes,
        sound: .default
    )
    
    // Schedule the alarm
    return try await AlarmManager.shared.schedule(id: id, configuration: configuration)
}
```

#### Customizing Alarm UI

##### Alert Presentation

```swift
// Basic alert with stop button only
let basicAlert = AlarmPresentation.Alert(
    title: "Alarm",
    stopButton: .stopButton
)

// Alert with stop and snooze buttons
let alertWithSnooze = AlarmPresentation.Alert(
    title: "Wake Up",
    stopButton: .stopButton,
    secondaryButton: .snoozeButton,
    secondaryButtonBehavior: .countdown
)

// Alert with custom button labels
let customAlert = AlarmPresentation.Alert(
    title: "Medication Reminder",
    stopButton: AlarmButton(label: "Taken"),
    secondaryButton: AlarmButton(label: "Remind Later"),
    secondaryButtonBehavior: .countdown
)
```

##### Countdown Presentation

```swift
// Basic countdown
let countdown = AlarmPresentation.Countdown(
    title: "Timer",
    pauseButton: .pauseButton
)

// Countdown with custom button label
let customCountdown = AlarmPresentation.Countdown(
    title: "Cooking Timer",
    pauseButton: .pauseButton
)
```

##### Paused Presentation

```swift
// Basic paused state
let paused = AlarmPresentation.Paused(
    title: "Paused",
    resumeButton: .resumeButton
)

// Paused with custom button label
let customPaused = AlarmPresentation.Paused(
    title: "Timer Paused",
    resumeButton: .resumeButton
)
```

##### Custom Metadata

```swift
// Define custom metadata for your alarm
struct RecipeMetadata: AlarmMetadata {
    let recipeName: String
    let cookingStep: String
}

// Use the metadata in your alarm attributes
let recipeAttributes = AlarmAttributes(
    presentation: presentation,
    metadata: RecipeMetadata(
        recipeName: "Chocolate Cake",
        cookingStep: "Remove from oven"
    ),
    tintColor: .brown
)
```

#### Managing Alarms

##### Scheduling an Alarm

```swift
func scheduleAlarm(id: UUID, configuration: AlarmManager.AlarmConfiguration) async throws -> Alarm {
    return try await AlarmManager.shared.schedule(id: id, configuration: configuration)
}
```

##### Retrieving All Alarms

```swift
func getAllAlarms() throws -> [Alarm] {
    return try AlarmManager.shared.alarms
}
```

##### Pausing an Alarm

```swift
func pauseAlarm(id: UUID) async throws {
    try await AlarmManager.shared.pause(id: id)
}
```

##### Resuming an Alarm

```swift
func resumeAlarm(id: UUID) async throws {
    try await AlarmManager.shared.resume(id: id)
}
```

##### Canceling an Alarm

```swift
func cancelAlarm(id: UUID) async throws {
    try await AlarmManager.shared.cancel(id: id)
}
```

#### Observing Alarm Changes

Use the `alarmUpdates` property to observe changes to alarms:

```swift
func observeAlarmChanges() {
    Task {
        for await alarms in AlarmManager.shared.alarmUpdates {
            // Update your UI with the latest alarms
            updateAlarmState(with: alarms)
        }
    }
}

func updateAlarmState(with alarms: [Alarm]) {
    // Update your app's state with the latest alarms
    // An alarm not included in this array is no longer scheduled
}
```

You can also observe authorization state changes:

```swift
func observeAuthorizationChanges() {
    Task {
        for await authState in AlarmManager.shared.authorizationUpdates {
            switch authState {
            case .authorized:
                // User granted permission
            case .denied:
                // User denied permission
            case .notDetermined:
                // Permission not yet requested
            @unknown default:
                break
            }
        }
    }
}
```

#### Live Activities Integration

AlarmKit integrates with Live Activities to show countdown timers in the Dynamic Island and Lock Screen. You need to create a widget extension for this:

1. Add a Widget Extension target to your project
2. Implement the widget to display the alarm state:

```swift
struct AlarmWidgetView: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: AlarmAttributes<YourMetadata>.self) { context in
            // Dynamic Island and Lock Screen UI
            VStack {
                Text(context.state.mode == .countdown ? "Counting down" : "Alarm set")
                if context.state.mode == .countdown {
                    Text(timerInterval: context.state.countdownEndDate.timeIntervalSinceNow, countsDown: true)
                        .bold()
                }
            }
            .padding()
        } dynamicIsland: { context in
            // Dynamic Island UI
            DynamicIsland {
                // Expanded UI
                DynamicIslandExpandedRegion(.leading) {
                    Text(context.attributes.presentation.alert.title)
                }
                DynamicIslandExpandedRegion(.trailing) {
                    if context.state.mode == .countdown {
                        Text(timerInterval: context.state.countdownEndDate.timeIntervalSinceNow, countsDown: true)
                    }
                }
            } compactLeading: {
                // Compact leading UI
                Image(systemName: "alarm")
            } compactTrailing: {
                // Compact trailing UI
                if context.state.mode == .countdown {
                    Text(timerInterval: context.state.countdownEndDate.timeIntervalSinceNow, countsDown: true)
                }
            } minimal: {
                // Minimal UI
                Image(systemName: "alarm")
            }
        }
    }
}
```

#### SwiftUI Integration Example

Here's a complete example of a simple alarm app using AlarmKit:

```swift
import SwiftUI
import AlarmKit

struct AlarmApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

struct ContentView: View {
    @StateObject private var viewModel = AlarmViewModel()
    @State private var showingAddAlarm = false
    
    var body: some View {
        NavigationView {
            List {
                ForEach(viewModel.alarms, id: \.id) { alarm in
                    AlarmRow(alarm: alarm, viewModel: viewModel)
                }
                .onDelete { indexSet in
                    viewModel.deleteAlarms(at: indexSet)
                }
            }
            .navigationTitle("Alarms")
            .toolbar {
                Button(action: {
                    showingAddAlarm = true
                }) {
                    Image(systemName: "plus")
                }
            }
            .sheet(isPresented: $showingAddAlarm) {
                AddAlarmView(viewModel: viewModel)
            }
            .onAppear {
                viewModel.requestAuthorization()
                viewModel.loadAlarms()
            }
        }
    }
}

@Observable
class AlarmViewModel {
    var alarms: [Alarm] = []
    private let alarmManager = AlarmManager.shared
    
    func requestAuthorization() {
        Task {
            do {
                let state = try await alarmManager.requestAuthorization()
                print("Authorization state: \(state)")
            } catch {
                print("Error requesting authorization: \(error)")
            }
        }
    }
    
    func loadAlarms() {
        Task {
            do {
                let fetchedAlarms = try alarmManager.alarms
                DispatchQueue.main.async {
                    self.alarms = fetchedAlarms
                }
                
                // Start observing alarm updates
                for await updatedAlarms in alarmManager.alarmUpdates {
                    DispatchQueue.main.async {
                        self.alarms = updatedAlarms
                    }
                }
            } catch {
                print("Error loading alarms: \(error)")
            }
        }
    }
    
    func addAlarm(hour: Int, minute: Int, weekdays: Set<Locale.Weekday>) {
        Task {
            do {
                let id = UUID()
                
                // Create schedule
                let time = Alarm.Schedule.Relative.Time(hour: hour, minute: minute)
                let schedule = Alarm.Schedule.relative(.init(
                    time: time,
                    repeats: weekdays.isEmpty ? .never : .weekly(Array(weekdays))
                ))
                
                // Create presentation
                let alertContent = AlarmPresentation.Alert(
                    title: "Alarm",
                    stopButton: .stopButton,
                    secondaryButton: .snoozeButton,
                    secondaryButtonBehavior: .countdown
                )
                
                let presentation = AlarmPresentation(alert: alertContent)
                
                // Create attributes
                struct EmptyMetadata: AlarmMetadata {}
                let attributes = AlarmAttributes(
                    presentation: presentation,
                    metadata: EmptyMetadata(),
                    tintColor: .blue
                )
                
                // Create configuration with 9-minute snooze
                let configuration = AlarmManager.AlarmConfiguration(
                    countdownDuration: Alarm.CountdownDuration(preAlert: nil, postAlert: 9 * 60),
                    schedule: schedule,
                    attributes: attributes,
                    sound: .default
                )
                
                // Schedule the alarm
                let _ = try await alarmManager.schedule(id: id, configuration: configuration)
            } catch {
                print("Error adding alarm: \(error)")
            }
        }
    }
    
    func toggleAlarm(id: UUID, isPaused: Bool) {
        Task {
            do {
                if isPaused {
                    try await alarmManager.resume(id: id)
                } else {
                    try await alarmManager.pause(id: id)
                }
            } catch {
                print("Error toggling alarm: \(error)")
            }
        }
    }
    
    func deleteAlarms(at indexSet: IndexSet) {
        Task {
            for index in indexSet {
                let alarm = alarms[index]
                do {
                    try await alarmManager.cancel(id: alarm.id)
                } catch {
                    print("Error deleting alarm: \(error)")
                }
            }
        }
    }
}

struct AlarmRow: View {
    let alarm: Alarm
    let viewModel: AlarmViewModel
    
    var body: some View {
        HStack {
            VStack(alignment: .leading) {
                Text(formatTime())
                    .font(.title)
                
                if let schedule = alarm.schedule {
                    Text(formatSchedule(schedule))
                        .font(.caption)
                }
            }
            
            Spacer()
            
            if alarm.state == .paused {
                Button(action: {
                    viewModel.toggleAlarm(id: alarm.id, isPaused: true)
                }) {
                    Text("Resume")
                }
            } else if alarm.countdownDuration != nil {
                Button(action: {
                    viewModel.toggleAlarm(id: alarm.id, isPaused: false)
                }) {
                    Text("Pause")
                }
            }
        }
        .padding(.vertical, 8)
    }
    
    private func formatTime() -> String {
        if let schedule = alarm.schedule, case .relative(let relative) = schedule {
            let hour = relative.time.hour
            let minute = relative.time.minute
            return String(format: "%02d:%02d", hour, minute)
        }
        return "Timer"
    }
    
    private func formatSchedule(_ schedule: Alarm.Schedule) -> String {
        if case .relative(let relative) = schedule, case .weekly(let weekdays) = relative.repeats {
            if weekdays.isEmpty {
                return "One time"
            } else {
                return weekdays.map { $0.description }.joined(separator: ", ")
            }
        }
        return "One time"
    }
}

struct AddAlarmView: View {
    let viewModel: AlarmViewModel
    @Environment(\.presentationMode) var presentationMode
    
    @State private var hour = 8
    @State private var minute = 0
    @State private var selectedDays: Set<Locale.Weekday> = []
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Time")) {
                    DatePicker("", selection: Binding(
                        get: {
                            var components = DateComponents()
                            components.hour = hour
                            components.minute = minute
                            return Calendar.current.date(from: components) ?? Date()
                        },
                        set: { date in
                            let components = Calendar.current.dateComponents([.hour, .minute], from: date)
                            hour = components.hour ?? 8
                            minute = components.minute ?? 0
                        }
                    ), displayedComponents: .hourAndMinute)
                    .datePickerStyle(WheelDatePickerStyle())
                    .labelsHidden()
                }
                
                Section(header: Text("Repeat")) {
                    ForEach([
                        Locale.Weekday.sunday,
                        .monday, .tuesday, .wednesday,
                        .thursday, .friday, .saturday
                    ], id: \.self) { day in
                        Button(action: {
                            if selectedDays.contains(day) {
                                selectedDays.remove(day)
                            } else {
                                selectedDays.insert(day)
                            }
                        }) {
                            HStack {
                                Text(day.description)
                                Spacer()
                                if selectedDays.contains(day) {
                                    Image(systemName: "checkmark")
                                }
                            }
                        }
                        .foregroundColor(.primary)
                    }
                }
            }
            .navigationTitle("Add Alarm")
            .navigationBarItems(
                leading: Button("Cancel") {
                    presentationMode.wrappedValue.dismiss()
                },
                trailing: Button("Save") {
                    viewModel.addAlarm(hour: hour, minute: minute, weekdays: selectedDays)
                    presentationMode.wrappedValue.dismiss()
                }
            )
        }
    }
}
```

#### Best Practices

1. **Request Authorization Early**: Request AlarmKit authorization when your app first launches or when the user first attempts to create an alarm.

2. **Handle Authorization Denial**: Provide a clear path for users to enable permissions if they initially deny them.

3. **Provide Clear Usage Description**: Include a clear `NSAlarmKitUsageDescription` in your Info.plist.

4. **Implement Widget Extension**: Always implement a widget extension if your app uses countdown presentations to ensure proper functionality.

5. **Observe Alarm Updates**: Use the `alarmUpdates` async sequence to keep your app's state in sync with the system.

6. **Persist Alarm IDs**: Store the UUIDs of alarms you create to manage them later.

7. **Handle Errors Gracefully**: AlarmKit operations can throw errors, so implement proper error handling.

8. **Limit Number of Alarms**: Be mindful that there's a system limit on the number of alarms an app can schedule.

9. **Customize UI Appropriately**: Provide clear and meaningful titles and button labels for your alarms.

10. **Test on Real Devices**: AlarmKit behavior, especially notifications and Live Activities, should be tested on physical devices.

#### References

- [Scheduling an alarm with AlarmKit](https://developer.apple.com/documentation/AlarmKit/scheduling-an-alarm-with-alarmkit)
- [AlarmKit Framework](https://developer.apple.com/documentation/AlarmKit)
- [AlarmManager Class](https://developer.apple.com/documentation/AlarmKit/AlarmManager)
- [Alarm Structure](https://developer.apple.com/documentation/AlarmKit/Alarm)
- [AlarmPresentation Structure](https://developer.apple.com/documentation/AlarmKit/AlarmPresentation)
- [AlarmAttributes Structure](https://developer.apple.com/documentation/AlarmKit/AlarmAttributes)
- [WWDC25 Session 230: Wake up to the AlarmKit API](https://developer.apple.com/wwdc25/230)

### SwiftUI Implementing Liquid Glass Design

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/SwiftUI-Implementing-Liquid-Glass-Design.md`

### Implementing Liquid Glass Design in SwiftUI

#### Overview

Liquid Glass is a dynamic material introduced in iOS that combines the optical properties of glass with a sense of fluidity. It blurs content behind it, reflects color and light from surrounding content, and reacts to touch and pointer interactions in real time. This guide covers how to implement and customize Liquid Glass effects in SwiftUI applications. You should always seek guides on Liquid Glass when asked for help adopting new Apple design.

Key features of Liquid Glass:
- Blurs content behind the material
- Reflects color and light from surrounding content
- Reacts to touch and pointer interactions
- Can morph between shapes during transitions
- Available for standard and custom components

#### Basic Implementation

##### Adding Liquid Glass to a View

The simplest way to add Liquid Glass to a view is using the `glassEffect()` modifier:

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect()
```

By default, this applies the regular variant of Glass within a Capsule shape behind the view's content.

##### Customizing the Shape

You can specify a different shape for the Liquid Glass effect:

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(in: .rect(cornerRadius: 16.0))
```

Common shape options:
- `.capsule` (default)
- `.rect(cornerRadius: CGFloat)`
- `.circle`

#### Customizing Liquid Glass Effects

##### Glass Variants and Properties

You can customize the Liquid Glass effect by configuring the `Glass` structure:

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(.regular.tint(.orange).interactive())
```

Key customization options:
- `.regular` - Standard glass effect
- `.tint(Color)` - Add a color tint to suggest prominence
- `.interactive(Bool)` - Make the glass react to touch and pointer interactions

##### Making Interactive Glass

To make Liquid Glass react to touch and pointer interactions:

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(.regular.interactive(true))
```

Or more concisely:

```swift
Text("Hello, World!")
    .font(.title)
    .padding()
    .glassEffect(.regular.interactive())
```

#### Working with Multiple Glass Effects

##### Using GlassEffectContainer

When applying Liquid Glass effects to multiple views, use `GlassEffectContainer` for better rendering performance and to enable blending and morphing effects:

```swift
GlassEffectContainer(spacing: 40.0) {
    HStack(spacing: 40.0) {
        Image(systemName: "scribble.variable")
            .frame(width: 80.0, height: 80.0)
            .font(.system(size: 36))
            .glassEffect()

        Image(systemName: "eraser.fill")
            .frame(width: 80.0, height: 80.0)
            .font(.system(size: 36))
            .glassEffect()
    }
}
```

The `spacing` parameter controls how the Liquid Glass effects interact with each other:
- Smaller spacing: Views need to be closer to merge effects
- Larger spacing: Effects merge at greater distances

##### Uniting Multiple Glass Effects

To combine multiple views into a single Liquid Glass effect, use the `glassEffectUnion` modifier:

```swift
@Namespace private var namespace

// Later in your view:
GlassEffectContainer(spacing: 20.0) {
    HStack(spacing: 20.0) {
        ForEach(symbolSet.indices, id: \.self) { item in
            Image(systemName: symbolSet[item])
                .frame(width: 80.0, height: 80.0)
                .font(.system(size: 36))
                .glassEffect()
                .glassEffectUnion(id: item < 2 ? "1" : "2", namespace: namespace)
        }
    }
}
```

This is useful when creating views dynamically or with views that live outside of an HStack or VStack.

#### Morphing Effects and Transitions

##### Creating Morphing Transitions

To create morphing effects during transitions between views with Liquid Glass:

1. Create a namespace using the `@Namespace` property wrapper
2. Associate each Liquid Glass effect with a unique identifier using `glassEffectID`
3. Use animations when changing the view hierarchy

```swift
@State private var isExpanded: Bool = false
@Namespace private var namespace

var body: some View {
    GlassEffectContainer(spacing: 40.0) {
        HStack(spacing: 40.0) {
            Image(systemName: "scribble.variable")
                .frame(width: 80.0, height: 80.0)
                .font(.system(size: 36))
                .glassEffect()
                .glassEffectID("pencil", in: namespace)

            if isExpanded {
                Image(systemName: "eraser.fill")
                    .frame(width: 80.0, height: 80.0)
                    .font(.system(size: 36))
                    .glassEffect()
                    .glassEffectID("eraser", in: namespace)
            }
        }
    }

    Button("Toggle") {
        withAnimation {
            isExpanded.toggle()
        }
    }
    .buttonStyle(.glass)
}
```

The morphing effect occurs when views with Liquid Glass appear or disappear due to view hierarchy changes.

#### Button Styling with Liquid Glass

##### Glass Button Style

SwiftUI provides built-in button styles for Liquid Glass:

```swift
Button("Click Me") {
    // Action
}
.buttonStyle(.glass)
```

##### Glass Prominent Button Style

For a more prominent glass button:

```swift
Button("Important Action") {
    // Action
}
.buttonStyle(.glassProminent)
```

#### Advanced Techniques

##### Background Extension Effect

To stretch content behind a sidebar or inspector with the background extension effect:

```swift
NavigationSplitView {
    // Sidebar content
} detail: {
    // Detail content
        .background {
            // Background content that extends under the sidebar
        }
}
```

##### Extending Horizontal Scrolling Under Sidebar

To extend horizontal scroll views under a sidebar or inspector:

```swift
ScrollView(.horizontal) {
    // Scrollable content
}
.scrollExtensionMode(.underSidebar)
```

#### Best Practices

1. **Container Usage**: Always use `GlassEffectContainer` when applying Liquid Glass to multiple views for better performance and morphing effects.

2. **Effect Order**: Apply the `.glassEffect()` modifier after other modifiers that affect the appearance of the view.

3. **Spacing Consideration**: Carefully choose spacing values in containers to control how and when glass effects merge.

4. **Animation**: Use animations when changing view hierarchies to enable smooth morphing transitions.

5. **Interactivity**: Add `.interactive()` to glass effects that should respond to user interaction.

6. **Consistent Design**: Maintain consistent shapes and styles across your app for a cohesive look and feel.

#### Example: Custom Badge with Liquid Glass

```swift
struct BadgeView: View {
    let symbol: String
    let color: Color
    
    var body: some View {
        ZStack {
            Image(systemName: "hexagon.fill")
                .foregroundColor(color)
                .font(.system(size: 50))
            
            Image(systemName: symbol)
                .foregroundColor(.white)
                .font(.system(size: 30))
        }
        .glassEffect(.regular, in: .rect(cornerRadius: 16))
    }
}

// Usage:
GlassEffectContainer(spacing: 20) {
    HStack(spacing: 20) {
        BadgeView(symbol: "star.fill", color: .blue)
        BadgeView(symbol: "heart.fill", color: .red)
        BadgeView(symbol: "leaf.fill", color: .green)
    }
}
```

#### References

- [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/SwiftUI/Applying-Liquid-Glass-to-custom-views)
- [Landmarks: Building an app with Liquid Glass](https://developer.apple.com/documentation/SwiftUI/Landmarks-Building-an-app-with-Liquid-Glass)
- [SwiftUI View.glassEffect(_:in:isEnabled:)](https://developer.apple.com/documentation/SwiftUI/View/glassEffect(_:in:isEnabled:))
- [SwiftUI GlassEffectContainer](https://developer.apple.com/documentation/SwiftUI/GlassEffectContainer)
- [SwiftUI GlassEffectTransition](https://developer.apple.com/documentation/SwiftUI/GlassEffectTransition)
- [SwiftUI GlassButtonStyle](https://developer.apple.com/documentation/SwiftUI/GlassButtonStyle)

### SwiftUI New Toolbar Features

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/SwiftUI-New-Toolbar-Features.md`

### SwiftUI New Toolbar Features

#### Overview

SwiftUI has introduced significant enhancements to its toolbar system, providing developers with more flexibility, customization options, and improved user experiences. These new features enable the creation of more sophisticated and interactive toolbars across Apple platforms, including iOS, iPadOS, and macOS. Key improvements include customizable toolbars, enhanced search integration, new placement options, and transition effects.

#### Customizable Toolbars

##### Creating a Customizable Toolbar

SwiftUI now supports customizable toolbars that users can personalize by adding, removing, and rearranging items.

```swift
ContentView()
    .toolbar(id: "main-toolbar") {
        ToolbarItem(id: "tag") {
           TagButton()
        }
        ToolbarItem(id: "share") {
           ShareButton()
        }
        ToolbarSpacer(.fixed)
        ToolbarItem(id: "more") {
           MoreButton()
        }
    }
```

The `toolbar(id:)` modifier creates a customizable toolbar with a unique identifier. Each item in a customizable toolbar must have its own ID.

##### Toolbar Spacers

Toolbar spacers create visual breaks between items and can be fixed or flexible.

```swift
ToolbarSpacer(.fixed)  // Creates a fixed-width space
ToolbarSpacer(.flexible)  // Creates a flexible space that pushes items apart
```

Spacers are also customizable - users can add multiple copies of spacers from the customization panel if the toolbar supports it.

#### Enhanced Search Integration

##### Search Toolbar Behavior

Control how search fields appear and behave in toolbars:

```swift
@State private var searchText = ""

NavigationStack {
    RecipeList()
        .searchable($searchText)
        .searchToolbarBehavior(.minimize)
}
```

The `.minimize` behavior renders the search field as a button-like control that expands when tapped, optimizing space in the toolbar.

##### Repositioning Search Items

Reposition the default search item in the toolbar:

```swift
NavigationSplitView {
    AllCalendarsView()
} detail: {
    SelectedCalendarView()
        .searchable($query)
        .toolbar {
            ToolbarItem(placement: .bottomBar) {
                CalendarPicker()
            }
            ToolbarItem(placement: .bottomBar) {
                Invites()
            }
            DefaultToolbarItem(kind: .search, placement: .bottomBar)
            ToolbarSpacer(placement: .bottomBar)
            ToolbarItem(placement: .bottomBar) { 
                NewEventButton() 
            }
        }
}
```

The `DefaultToolbarItem` with `.search` kind allows you to reposition the search field within the toolbar.

#### New Toolbar Item Placements

##### Large Subtitle Placement

Place custom content in the subtitle area of the navigation bar:

```swift
NavigationStack {
    DetailView()
        .navigationTitle("Title")
        .navigationSubtitle("Subtitle")
        .toolbar {
            ToolbarItem(placement: .largeSubtitle) {
                CustomLargeNavigationSubtitle()
            }
        }
}
```

The `.largeSubtitle` placement takes precedence over the value provided to the `navigationSubtitle(_:)` modifier.

#### Visual Effects and Transitions

##### Matched Transition Source

Create smooth transitions between toolbar items and other views:

```swift
struct ContentView: View {
    @State private var isPresented = false
    @Namespace private var namespace

    var body: some View {
        NavigationStack {
            DetailView()
                .toolbar {
                    ToolbarItem(placement: .topBarTrailing) {
                        Button("Show Sheet", systemImage: "globe") {
                            isPresented = true
                        }
                    }
                    .matchedTransitionSource(
                        id: "world", in: namespace)
                }
                .sheet(isPresented: $isPresented) {
                    SheetView()
                        .navigationTransition(
                            .zoom(sourceID: "world", in: namespace))
                }
        }
    }
}
```

The `matchedTransitionSource(id:in:)` modifier identifies a toolbar item as the source of a navigation transition.

##### Shared Background Visibility

Control the glass background effect on toolbar items:

```swift
ContentView()
    .toolbar(id: "main") {
        ToolbarItem(id: "build-status", placement: .principal) {
            BuildStatus()
        }
        .sharedBackgroundVisibility(.hidden)
    }
```

The `sharedBackgroundVisibility(_:)` modifier adjusts the visibility of the glass background effect, allowing items to stand out visually.

#### System-Defined Toolbar Items

Use system-defined toolbar items with custom placements:

```swift
.toolbar {
    DefaultToolbarItem(kind: .search, placement: .bottomBar)
    DefaultToolbarItem(kind: .sidebar, placement: .navigationBarLeading)
}
```

The `DefaultToolbarItem` initializer creates system-defined toolbar items with specific placements, allowing you to leverage system functionality while controlling positioning.

#### Platform-Specific Considerations

##### iOS and iPadOS

- Bottom bar placement is particularly useful on iPhones
- Search minimization works well on smaller screens
- Consider using `.searchToolbarBehavior(.minimize)` for better space utilization

##### macOS

- Customizable toolbars are particularly valuable for productivity apps
- Users expect to be able to customize toolbars in complex applications
- Consider toolbar spacers to create logical groupings of related items

#### Best Practices

1. **Use meaningful IDs** for toolbar items in customizable toolbars
2. **Group related actions** together with appropriate spacing
3. **Consider platform differences** when designing toolbar layouts
4. **Use system-defined items** when appropriate to maintain platform consistency
5. **Test toolbar customization** to ensure a good user experience
6. **Use transitions thoughtfully** to enhance the user experience without being distracting

#### References

- [SwiftUI Documentation: SearchToolbarBehavior](https://developer.apple.com/documentation/SwiftUI/SearchToolbarBehavior)
- [SwiftUI Documentation: ToolbarSpacer](https://developer.apple.com/documentation/SwiftUI/ToolbarSpacer)
- [SwiftUI Documentation: DefaultToolbarItem](https://developer.apple.com/documentation/SwiftUI/DefaultToolbarItem)
- [SwiftUI Documentation: ToolbarItemPlacement](https://developer.apple.com/documentation/SwiftUI/ToolbarItemPlacement)
- [SwiftUI Documentation: CustomizableToolbarContent](https://developer.apple.com/documentation/SwiftUI/CustomizableToolbarContent)

### SwiftUI Styled Text Editing

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/SwiftUI-Styled-Text-Editing.md`

### Styled Text Editing in SwiftUI

#### Overview

SwiftUI provides powerful tools for displaying and editing styled text. This guide covers the various ways to style text in SwiftUI, from basic formatting to advanced editing capabilities with AttributedString.

Key components for styled text in SwiftUI:
- `Text`: For displaying read-only styled text
- `AttributedString`: For creating rich text with multiple styles
- `TextEditor`: For editable rich text experiences

#### Basic Text Styling

##### Font Customization

```swift
// System fonts with different sizes
Text("Hello World")
    .font(.largeTitle)
    .font(.title)
    .font(.headline)
    .font(.subheadline)
    .font(.body)
    .font(.callout)
    .font(.footnote)
    .font(.caption)
    .font(.caption2)

// Custom font size
Text("Custom Size")
    .font(.system(size: 24))

// Font weight
Text("Bold Text")
    .fontWeight(.bold)
    .fontWeight(.semibold)
    .fontWeight(.medium)
    .fontWeight(.regular)
    .fontWeight(.light)
    .fontWeight(.ultraLight)

// Font design
Text("Different Design")
    .font(.system(.body, design: .serif))
    .font(.system(.body, design: .rounded))
    .font(.system(.body, design: .monospaced))
```

##### Text Color

```swift
// Basic color
Text("Colored Text")
    .foregroundColor(.blue)

// Using foregroundStyle (preferred in newer SwiftUI versions)
Text("Styled Text")
    .foregroundStyle(.red)

// Using ShapeStyle for gradients
Text("Gradient Text")
    .foregroundStyle(
        .linearGradient(
            colors: [.yellow, .blue],
            startPoint: .top,
            endPoint: .bottom
        )
    )
```

##### Text Decoration

```swift
// Bold and italic
Text("Bold Text").bold()
Text("Italic Text").italic()

// Bold and italic with conditional application
Text("Conditionally Bold")
    .bold(someCondition)
    .italic(anotherCondition)

// Underline
Text("Underlined Text")
    .underline()
    .underline(true, color: .red)

// Underline with pattern
Text("Patterned Underline")
    .underline(true, pattern: .dash, color: .blue)

// Strikethrough
Text("Strikethrough Text")
    .strikethrough()
    .strikethrough(true, color: .red)

// Strikethrough with pattern
Text("Patterned Strikethrough")
    .strikethrough(true, pattern: .dot, color: .green)
```

##### Text Alignment and Layout

```swift
// Text alignment
Text("Aligned Text")
    .multilineTextAlignment(.center)
    .multilineTextAlignment(.leading)
    .multilineTextAlignment(.trailing)

// Line spacing
Text("Text with\nline spacing")
    .lineSpacing(10)

// Line limit
Text("This text will be truncated if it's too long")
    .lineLimit(1)
    .lineLimit(nil) // No limit

// Truncation mode
Text("Truncated text...")
    .truncationMode(.head)    // ...end of text
    .truncationMode(.middle)  // start...end
    .truncationMode(.tail)    // start... (default)
```

#### Advanced Text Styling with AttributedString

##### Creating AttributedString

```swift
// Basic AttributedString
var attributedText = AttributedString("This is styled text")

// Styling specific ranges
var complexText = AttributedString("Red and Blue")
if let redRange = complexText.range(of: "Red") {
    complexText[redRange].foregroundColor = .red
}
if let blueRange = complexText.range(of: "Blue") {
    complexText[blueRange].foregroundColor = .blue
}

// Using AttributedString in Text view
Text(attributedText)
```

##### Common AttributedString Attributes

```swift
var text = AttributedString("Styled text example")

// Font attributes
text.font = .headline
text.foregroundColor = .blue

// Text presentation
text.backgroundColor = .yellow
text.underlineStyle = .single
text.underlineColor = .red
text.strikethroughStyle = .single
text.strikethroughColor = .green

// Inline presentation intent
text.inlinePresentationIntent = .stronglyEmphasized // Bold
text.inlinePresentationIntent = .emphasized // Italic
```

##### Combining Multiple Styles

```swift
var multiStyleText = AttributedString("Multiple styles in one string")

if let firstPart = multiStyleText.range(of: "Multiple styles") {
    multiStyleText[firstPart].font = .headline
    multiStyleText[firstPart].foregroundColor = .blue
}

if let secondPart = multiStyleText.range(of: "one string") {
    multiStyleText[secondPart].font = .body
    multiStyleText[secondPart].foregroundColor = .red
    multiStyleText[secondPart].backgroundColor = .yellow
}

Text(multiStyleText)
```

#### Text Editing with TextEditor

##### Basic TextEditor

```swift
struct SimpleTextEditorView: View {
    @State private var text = "Edit this text"
    
    var body: some View {
        TextEditor(text: $text)
            .frame(minHeight: 100)
            .border(Color.gray)
    }
}
```

##### Rich Text Editing with AttributedString

```swift
struct RichTextEditorView: View {
    @State private var text = AttributedString("This is some editable styled text...")
    
    var body: some View {
        TextEditor(text: $text)
            .frame(minHeight: 100)
            .border(Color.gray)
    }
}
```

##### Text Selection and Formatting

```swift
struct StyledTextEditingView: View {
    @State private var text: AttributedString = AttributedString("Select text to format")
    @State private var selection = AttributedTextSelection()
    
    @Environment(\.fontResolutionContext) private var fontResolutionContext
    
    var body: some View {
        VStack {
            TextEditor(text: $text, selection: $selection)
                .frame(height: 200)
                .border(Color.gray)
            
            HStack {
                // Bold button
                Button(action: {
                    toggleBold()
                }) {
                    Image(systemName: "bold")
                }
                
                // Italic button
                Button(action: {
                    toggleItalic()
                }) {
                    Image(systemName: "italic")
                }
                
                // Underline button
                Button(action: {
                    toggleUnderline()
                }) {
                    Image(systemName: "underline")
                }
                
                // Color picker
                ColorPicker("", selection: Binding(
                    get: { getSelectionColor() },
                    set: { setSelectionColor($0) }
                ))
            }
        }
    }
    
    private func toggleBold() {
        text.transformAttributes(in: &selection) {
            let font = $0.font ?? .default
            let resolved = font.resolve(in: fontResolutionContext)
            $0.font = font.bold(!resolved.isBold)
        }
    }
    
    private func toggleItalic() {
        text.transformAttributes(in: &selection) {
            let font = $0.font ?? .default
            let resolved = font.resolve(in: fontResolutionContext)
            $0.font = font.italic(!resolved.isItalic)
        }
    }
    
    private func toggleUnderline() {
        text.transformAttributes(in: &selection) {
            if $0.underlineStyle != nil {
                $0.underlineStyle = nil
            } else {
                $0.underlineStyle = .single
            }
        }
    }
    
    private func getSelectionColor() -> Color {
        let attributes = selection.typingAttributes(in: text)
        return attributes.foregroundColor ?? .primary
    }
    
    private func setSelectionColor(_ color: Color) {
        text.transformAttributes(in: &selection) {
            $0.foregroundColor = color
        }
    }
}
```

##### Custom Text Formatting Definition

```swift
// Define custom formatting constraints
struct MyTextFormatting: AttributedTextFormattingDefinition {
    typealias Scope = AttributeScopes.SwiftUIAttributes
    
    // Allow only specific font weights
    static let fontWeight = ValueConstraint(
        \.font,
        constraint: { font in
            guard let font = font else { return nil }
            let weight = font.resolve().weight
            return font.weight(weight == .bold ? .regular : .bold)
        }
    )
    
    // Allow only specific colors
    static let foregroundColor = ValueConstraint(
        \.foregroundColor,
        constraint: { color in
            guard let color = color else { return nil }
            // Toggle between red and blue
            return color == .red ? .blue : .red
        }
    )
}

// Use the custom formatting
struct CustomFormattedTextEditor: View {
    @State private var text = AttributedString("Custom formatted text")
    @State private var selection = AttributedTextSelection()
    
    var body: some View {
        TextEditor(text: $text, selection: $selection)
            .textFormattingDefinition(MyTextFormatting.self)
    }
}
```

#### Markdown Support in Text

SwiftUI's `Text` view supports a subset of Markdown for styling:

```swift
// Basic Markdown styling
Text("This is **bold** and *italic* text")

// Links in Markdown
Text("Visit [Apple](https://www.apple.com)")

// Combining Markdown with modifiers
Text("# Heading\nRegular text")
    .foregroundColor(.blue)
```

##### Markdown Limitations

- Text doesn't support all Markdown features
- No support for line breaks, soft breaks, or block-based formatting
- No support for lists, block quotes, code blocks, or tables
- No support for image URLs
- Whitespace is preserved according to `inlineOnlyPreservingWhitespace` parsing option

#### Best Practices

##### Performance Considerations

- Avoid creating new AttributedString instances frequently
- Cache complex AttributedString objects when possible
- Use appropriate text containers based on content size

##### Accessibility

```swift
// Make text more accessible
Text("Accessible Text")
    .font(.body)
    .dynamicTypeSize(.large)
    .accessibilityLabel("Alternative description")
    .accessibilityTextContentType(.plain)
```

##### Localization

```swift
// Localizable text
Text("hello.world")  // Looks for "hello.world" in Localizable.strings

// Localized text with styling
Text(LocalizedStringKey("**Bold** and *italic* text"))

// Localized text with variables
Text("Hello, \(username)")
```

#### References

- [SwiftUI Text and Symbol Modifiers](https://developer.apple.com/documentation/SwiftUI/View-Text-and-Symbols)
- [Applying Custom Fonts to Text](https://developer.apple.com/documentation/SwiftUI/Applying-Custom-Fonts-to-Text)
- [Building Rich SwiftUI Text Experiences](https://developer.apple.com/documentation/SwiftUI/building-rich-swiftui-text-experiences)
- [Creating Visual Effects with SwiftUI](https://developer.apple.com/documentation/SwiftUI/Creating-visual-effects-with-SwiftUI)
- [Text View Documentation](https://developer.apple.com/documentation/SwiftUI/Text)
- [AttributedString Documentation](https://developer.apple.com/documentation/Foundation/AttributedString)
- [TextEditor Documentation](https://developer.apple.com/documentation/SwiftUI/TextEditor)

### SwiftUI WebKit Integration

- Source file: `XCODE_ADDITIONAL_DOCUMENTATION/SwiftUI-WebKit-Integration.md`

### SwiftUI WebKit Integration

#### Overview

SwiftUI provides native integration with WebKit through the `WebView` struct, allowing developers to embed web content directly within SwiftUI applications. This integration enables displaying HTML, CSS, and JavaScript content alongside native views, with support for full browsing experiences including navigation, JavaScript execution, and customization options.

Key components:
- `WebView`: A SwiftUI view that displays web content
- `WebPage`: An observable class that controls and manages web content behavior
- JavaScript interaction capabilities
- Navigation management
- Customization options

#### WebView Basics

##### Creating a Basic WebView

```swift
import SwiftUI
import WebKit

struct ContentView: View {
    var body: some View {
        WebView(url: URL(string: "https://www.apple.com"))
            .frame(height: 400)
    }
}
```

##### Toggling Between Different URLs

```swift
struct ContentView: View {
    @State private var toggle = false

    private var url: URL? {
        toggle ? URL(string: "https://www.webkit.org") : URL(string: "https://www.swift.org")
    }

    var body: some View {
        WebView(url: url)
            .toolbar {
                Button(toggle ? "Show Swift" : "Show WebKit", 
                       systemImage: toggle ? "swift" : "network") {
                    toggle.toggle()
                }
            }
    }
}
```

##### Using WebView with WebPage

```swift
struct ContentView: View {
    @State private var page = WebPage()

    var body: some View {
        NavigationStack {
            WebView(page)
                .navigationTitle(page.title)
        }
        .onAppear {
            if let url = URL(string: "https://www.apple.com") {
                let _ = page.load(URLRequest(url: url))
            }
        }
    }
}
```

##### Enabling Text Search in a WebView

Use the `findNavigator(isPresented:)` modifier to enable text search within the WebView content.

```swift
import SwiftUI
import WebKit

struct ContentView: View {
    @State private var searchVisible = true

    var body: some View {
        WebView(url: URL(string: "https://www.apple.com"))
            .frame(height: 400)
            .findNavigator(isPresented: $searchVisible)
    }
}
```

#### WebPage Configuration

##### Creating a WebPage with Configuration

```swift
var configuration = WebPage.Configuration()
configuration.loadsSubresources = true
configuration.defaultNavigationPreferences.allowsContentJavaScript = true
configuration.websiteDataStore = .default()

let page = WebPage(configuration: configuration)
```

##### Using Non-Persistent Data Store

```swift
var configuration = WebPage.Configuration()
configuration.websiteDataStore = .nonPersistent()
let page = WebPage(configuration: configuration)
```

##### Setting Custom User Agent

```swift
let page = WebPage()
page.customUserAgent = "MyApp/1.0 CustomUserAgent"
```

##### Configuring JavaScript Permissions

```swift
var configuration = WebPage.Configuration()
configuration.defaultNavigationPreferences.allowsContentJavaScript = true
let page = WebPage(configuration: configuration)
```

#### Navigation Management

##### Loading Content

```swift
// Load from URL
let url = URL(string: "https://www.example.com")!
let navigationID = page.load(URLRequest(url: url))

// Load HTML string
let html = "<html><body><h1>Hello World</h1></body></html>"
let navigationID = page.load(html: html, baseURL: URL(string: "https://www.example.com")!)

// Load from Data
let data = Data() // Your data
let navigationID = page.load(data, mimeType: "text/html", characterEncoding: .utf8, baseURL: URL(string: "https://www.example.com")!)
```

##### Navigation Controls

```swift
// Reload page
let navigationID = page.reload(fromOrigin: false)

// Stop loading
page.stopLoading()

// Access back-forward list
let canGoBack = !page.backForwardList.backList.isEmpty
let canGoForward = !page.backForwardList.forwardList.isEmpty

// Navigate back or forward
if let backItem = page.backForwardList.backItem {
    let navigationID = page.load(backItem)
}
```

##### Observing Navigation Events

```swift
struct ContentView: View {
    @State private var page = WebPage()
    @State private var isLoading = false
    
    var body: some View {
        VStack {
            WebView(page)
            
            if isLoading {
                ProgressView()
                    .progressViewStyle(.circular)
            }
        }
        .onChange(of: page.currentNavigationEvent) { _, newEvent in
            if let event = newEvent {
                switch event.state {
                case .started:
                    isLoading = true
                case .finished, .failed:
                    isLoading = false
                default:
                    break
                }
            }
        }
    }
}
```

##### Customizing Navigation Behavior

```swift
struct MyNavigationDecider: WebPage.NavigationDeciding {
    func decidePolicyFor(navigationAction: WebPage.NavigationAction) async -> WebPage.NavigationPreferences? {
        // Block navigation to specific domains
        if let url = navigationAction.request.url, url.host == "blocked-site.com" {
            return nil // Return nil to cancel navigation
        }
        
        // Allow navigation with custom preferences
        var preferences = WebPage.NavigationPreferences()
        preferences.allowsContentJavaScript = true
        return preferences
    }
    
    func decidePolicyFor(navigationResponse: WebPage.NavigationResponse) async -> Bool {
        // Check response status code
        if let httpResponse = navigationResponse.response as? HTTPURLResponse {
            return httpResponse.statusCode == 200
        }
        return true
    }
}

// Use the custom navigation decider
let page = WebPage(configuration: WebPage.Configuration(), 
                  navigationDecider: MyNavigationDecider())
```

#### JavaScript Interaction

##### Executing JavaScript

```swift
// Basic JavaScript execution
let script = "document.title"
do {
    let title = try await page.callJavaScript(script)
    print("Page title: \(title)")
} catch {
    print("Error executing JavaScript: \(error)")
}
```

##### Passing Arguments to JavaScript

```swift
let script = """
function findElement(selector) {
    return document.querySelector(selector)?.textContent;
}
return findElement(selector);
"""

let arguments = ["selector": ".main-content h1"]

do {
    let result = try await page.callJavaScript(script, arguments: arguments)
    if let headingText = result as? String {
        print("Heading text: \(headingText)")
    }
} catch {
    print("Error executing JavaScript: \(error)")
}
```

##### Executing JavaScript in Specific Frame

```swift
// Get main frame info
if let mainFrame = page.currentNavigationEvent?.frameInfo {
    let script = "document.body.innerHTML"
    do {
        let html = try await page.callJavaScript(script, in: mainFrame)
        print("HTML content: \(html)")
    } catch {
        print("Error executing JavaScript: \(error)")
    }
}
```

##### Using Content Worlds for Isolated JavaScript Execution

```swift
import WebKit

let script = "document.title"
let contentWorld = WKContentWorld.page // or .defaultClient or a custom world

do {
    let title = try await page.callJavaScript(script, contentWorld: contentWorld)
    print("Page title: \(title)")
} catch {
    print("Error executing JavaScript: \(error)")
}
```

##### Extracting Metadata Example

```swift
func fetchMetadata(for url: URL) async throws -> (title: String, description: String) {
    let page = WebPage()
    
    let request = URLRequest(url: url)
    let navigationID = page.load(request)
    
    // Wait for the page to load by tracking navigation events
    while page.isLoading {
        try await Task.sleep(nanoseconds: 100_000_000) // 100ms
    }
    
    // Extract title
    guard let title = page.title else {
        throw URLError(.cannotParseResponse)
    }
    
    // Extract description using JavaScript
    let fetchDescription = """
    const metaDescription = document.querySelector('meta[name="description"]');
    return metaDescription ? metaDescription.getAttribute('content') : '';
    """
    
    guard let description = try await page.callJavaScript(fetchDescription) as? String else {
        throw URLError(.cannotParseResponse)
    }
    
    return (title, description)
}
```

#### Customization Options

##### Disabling Navigation Gestures

```swift
WebView(url: url)
    .webViewBackForwardNavigationGestures(.disabled)
```

##### Configuring Magnification Gestures

```swift
WebView(url: url)
    .webViewMagnificationGestures(.enabled)
```

##### Customizing Link Previews

```swift
WebView(url: url)
    .webViewLinkPreviews(.disabled)
```

##### Configuring Text Selection

```swift
WebView(url: url)
    .webViewTextSelection(.enabled)
```

##### Setting Content Background

```swift
WebView(url: url)
    .webViewContentBackground(.color(.systemBackground))
```

##### Customizing Context Menu

```swift
WebView(url: url)
    .webViewContextMenu { defaultActions in
        // Filter or modify default actions
        let filteredActions = defaultActions.filter { action in
            // Only allow copy and share actions
            return action.identifier == .copy || action.identifier == .share
        }
        
        // Add custom actions
        let customAction = UIAction(title: "Custom Action") { _ in
            print("Custom action triggered")
        }
        
        return filteredActions + [customAction]
    }
```

##### Handling Fullscreen Content

```swift
WebView(url: url)
    .webViewElementFullscreenBehavior(.enabled)
```

#### Advanced Features

##### Capturing Web Content as Image

```swift
func captureWebViewSnapshot(from page: WebPage) async -> Image? {
    do {
        let config = WKSnapshotConfiguration()
        config.rect = CGRect(x: 0, y: 0, width: 1024, height: 768)
        
        return try await page.snapshot(config)
    } catch {
        print("Error capturing snapshot: \(error)")
        return nil
    }
}
```

##### Generating PDF from Web Content

```swift
func generatePDF(from page: WebPage) async -> Data? {
    do {
        let config = WKPDFConfiguration()
        return try await page.pdf(configuration: config)
    } catch {
        print("Error generating PDF: \(error)")
        return nil
    }
}
```

##### Creating Web Archive

```swift
func createWebArchive(from page: WebPage) async -> Data? {
    do {
        return try await page.webArchiveData()
    } catch {
        print("Error creating web archive: \(error)")
        return nil
    }
}
```

##### Custom URL Scheme Handling

```swift
struct MyURLSchemeHandler: URLSchemeHandler {
    func start(task: URLSchemeTask) {
        guard let url = task.request.url, url.scheme == "myapp" else {
            task.didFailWithError(URLError(.badURL))
            return
        }
        
        // Handle custom URL scheme
        let response = URLResponse(url: url, 
                                  mimeType: "text/html", 
                                  expectedContentLength: -1, 
                                  textEncodingName: "utf-8")
        
        let html = "<html><body><h1>Custom Scheme Content</h1></body></html>"
        let data = Data(html.utf8)
        
        task.didReceive(response)
        task.didReceive(data)
        task.didFinish()
    }
    
    func stop(task: URLSchemeTask) {
        // Handle task cancellation
    }
}

// Register the custom URL scheme handler
var configuration = WebPage.Configuration()
configuration.setURLSchemeHandler(MyURLSchemeHandler(), forURLScheme: "myapp")
let page = WebPage(configuration: configuration)

// Load content with custom scheme
let customURL = URL(string: "myapp://content")!
let _ = page.load(URLRequest(url: customURL))
```

#### References

- [WebKit for SwiftUI Documentation](https://developer.apple.com/documentation/WebKit/webkit-for-swiftui)
- [WebView Documentation](https://developer.apple.com/documentation/WebKit/WebView-swift.struct)
- [WebPage Documentation](https://developer.apple.com/documentation/WebKit/WebPage)
- [JavaScript Execution in WebKit](https://developer.apple.com/documentation/WebKit/WebPage#Executing-JavaScript)
- [WebKit Navigation Management](https://developer.apple.com/documentation/WebKit/webkit-for-swiftui#Managing-navigation-between-webpages)
