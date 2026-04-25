#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
JMKR_ROOT="${JMKR_ROOT:-$HOME/repos/jmkr_kj}"
VAULT_ROOT="${VAULT_ROOT:-$HOME/Documents/Obsidian Vault}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8081}"

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 path/to/report.md [more reports...]" >&2
  exit 2
fi

for report in "$@"; do
  if [[ "$report" != /* ]]; then
    report="$VAULT_ROOT/$report"
  fi
  echo "[validate] $report"
  python3 "$JMKR_ROOT/scripts/validate_market_intel_claims.py" \
    --report "$report" \
    --jmkr-root "$JMKR_ROOT"

done

echo "[ok] report-claim validation passed"

echo "[hint] run Quartz sync/link validation next if publishing"
echo "  cd $ROOT && ./scripts/sync-market-intel.sh"
echo "  python3 content/market-intel/scripts/validate_quartz_links.py --base-url $BASE_URL --path /market-intel/research/wait-2d-close-review"
