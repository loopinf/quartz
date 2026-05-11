#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

export PATH="/Users/gbserver/.hermes/hermes-agent/venv/bin:/Users/gbserver/.hermes/hermes-agent/node_modules/.bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export HERMES_HOME="${HERMES_HOME:-/Users/gbserver/.hermes}"
export HERMES_ENV_FILE="${HERMES_ENV_FILE:-/Users/gbserver/.hermes/.env}"
export HERMES_AUTO_KICKOFF_COMMAND="${HERMES_AUTO_KICKOFF_COMMAND:-/Users/gbserver/.hermes/hermes-agent/venv/bin/hermes}"
export HERMES_INBOX_BIND="${HERMES_INBOX_BIND:-0.0.0.0}"
export HERMES_INBOX_PORT="${HERMES_INBOX_PORT:-8765}"
export HERMES_PREVIEW_PORT="${HERMES_PREVIEW_PORT:-8081}"

cd "$ROOT"
exec /usr/bin/python3 scripts/hermes_inbox_server.py
