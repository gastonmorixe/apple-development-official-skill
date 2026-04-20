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
- `ChatMessageTelemetryv2` dimensions include: dvt_app_name, dvt_build_version, dvt_version, interaction_source, is_auto_apply_enabled, is_context_search_enabled, is_likely_sample_project, model_category, model_name, rate_limit_status, response_failure_reason, response_status, integrated_account_type, bucketed_count_executor_tool_calls, and 9 more.
- `ChatMessageTelemetryv2` measures include: Count.
- `AvailabilityDetailedStatus_V8` tracks availability and download-state fields such as: AppleIntelligenceLocale, buddyStatus, buildVersionPriorToSU, countFactoryAssetInBytes, countFactoryAssets, countPSUSAssetsInBytes, currentMCSubscriptionHash, currentSubscriptionHash, downloadState, errorCount, failingSubsystemOperations, lastMADownloadAttemptErrorAsset, and 20 more.

## Source Files Integrated
- `SYSTEM_INTELLIGENCE_PLIST`
- `SYSTEM_FOUNDATION_MODELS_PLIST`
- `SYSTEM_TASKED_CONFIG_JSON`
