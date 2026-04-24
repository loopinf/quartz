#!/usr/bin/env bash
set -euo pipefail

VAULT_PATH="${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}"
SOURCE="$VAULT_PATH/market-intel"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="$ROOT/content/market-intel"

if [ ! -d "$SOURCE" ]; then
  echo "Source folder not found: $SOURCE" >&2
  exit 1
fi

python3 "$ROOT/scripts/ensure_next_session_prep.py" \
  --vault-path "$VAULT_PATH"

python3 "$ROOT/scripts/update_market_intel_entrypoints.py" \
  --vault-path "$VAULT_PATH" \
  --site-root "$ROOT"

mkdir -p "$TARGET"
rsync -a --delete --exclude 'templates/' "$SOURCE/" "$TARGET/"

echo "  source: $SOURCE"
echo "  target: $TARGET"
