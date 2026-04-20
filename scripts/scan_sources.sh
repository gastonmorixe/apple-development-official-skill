#!/usr/bin/env bash
set -euo pipefail

SELECTED_DEVELOPER_DIR="$(xcode-select -p)"
XCODE_APP="$(cd "$SELECTED_DEVELOPER_DIR/../.." && pwd)"
XCODE_RESOURCES="$XCODE_APP/Contents/PlugIns/IDEIntelligenceChat.framework/Versions/A/Resources"
XCODE_ADDITIONAL_DOCUMENTATION="$XCODE_RESOURCES/AdditionalDocumentation"
LOCAL_XCODE_CODINGASSISTANT_ROOT="$HOME/Library/Developer/Xcode/CodingAssistant"
ROOT_ANCHOR="$(python3 - <<'PY'
from pathlib import Path
print(Path.home().anchor, end="")
PY
)"
SYSTEM_INTELLIGENCE_PLIST="${ROOT_ANCHOR}System/Library/OnBoardingBundles/com.apple.onboarding.intelligenceengine.bundle/Contents/Resources/Intelligence.plist"
SYSTEM_FOUNDATION_MODELS_PLIST="${ROOT_ANCHOR}System/Library/LifecyclePolicy/DomainAttributes/com.apple.foundationmodels.plist"
SYSTEM_TASKED_CONFIG_JSON="${ROOT_ANCHOR}Library/CoreAnalytics/taskedConfig.json"

echo "fd -H -t f -a -e idechatprompttemplate . $XCODE_RESOURCES | sort"
fd -H -t f -a -e idechatprompttemplate . "$XCODE_RESOURCES" | sort
echo
echo "fd -H -t f -a -e md . $XCODE_ADDITIONAL_DOCUMENTATION | sort"
fd -H -t f -a -e md . "$XCODE_ADDITIONAL_DOCUMENTATION" | sort
echo
echo "fd -H -t f -a . $LOCAL_XCODE_CODINGASSISTANT_ROOT | sort"
fd -H -t f -a . "$LOCAL_XCODE_CODINGASSISTANT_ROOT" | sort
echo
echo "plutil -p $XCODE_RESOURCES/ApprovedIntegrationModelPairings.plist"
plutil -p "$XCODE_RESOURCES/ApprovedIntegrationModelPairings.plist"
echo
echo "plutil -p $XCODE_RESOURCES/IDEIntelligenceChat.xcplugindata"
plutil -p "$XCODE_RESOURCES/IDEIntelligenceChat.xcplugindata"
echo
echo "plutil -p $SYSTEM_INTELLIGENCE_PLIST"
plutil -p "$SYSTEM_INTELLIGENCE_PLIST"
echo
echo "plutil -p $SYSTEM_FOUNDATION_MODELS_PLIST"
plutil -p "$SYSTEM_FOUNDATION_MODELS_PLIST"
echo
echo "sed -n '1,120p' $SYSTEM_TASKED_CONFIG_JSON"
sed -n '1,120p' "$SYSTEM_TASKED_CONFIG_JSON"
