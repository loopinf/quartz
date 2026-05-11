#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/launchd/com.gbserver.market-intel-hermes-inbox.plist"
DEST="$HOME/Library/LaunchAgents/com.gbserver.market-intel-hermes-inbox.plist"
LABEL="com.gbserver.market-intel-hermes-inbox"

mkdir -p "$HOME/Library/LaunchAgents" "$ROOT/logs"
cp "$SRC" "$DEST"
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$DEST"
launchctl kickstart -k "gui/$(id -u)/$LABEL"

echo "Installed and started $LABEL"
launchctl print "gui/$(id -u)/$LABEL" | sed -n '1,120p'
