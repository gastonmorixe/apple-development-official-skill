---
title: System Intelligence Context and Telemetry
---

# System Intelligence Context and Telemetry

System-level Apple Intelligence context that helps explain platform availability, FoundationModels process policy, and the telemetry vocabulary around Xcode chat activity.

## Use This For
- Understanding how system Apple Intelligence support is framed outside Xcode.
- Understanding the entitlement and process policy tied to FoundationModels work.
- Understanding which Xcode chat metrics Apple appears to track in CoreAnalytics configuration.

## System Availability Context
- Supported platforms in system onboarding bundle: iOS, macOS, watchOS, xrOS.

## FoundationModels Process Policy
- Restriction entitlement: `com.apple.runningboard.assertions.foundationmodels`.
- Running policy cues: duration `180` seconds with warning `5` seconds, CPU role `RBSRoleNonUserInteractive`, jetsam band `40`, RBSPreserveBaseMemoryGrant, RBSPreventIdleSleepGrant, running reason `20821`.

## Telemetry Vocabulary Relevant To Xcode Chat

## Source Files Integrated
- `SYSTEM_INTELLIGENCE_PLIST`
- `SYSTEM_FOUNDATION_MODELS_PLIST`
- `SYSTEM_TASKED_CONFIG_JSON`
