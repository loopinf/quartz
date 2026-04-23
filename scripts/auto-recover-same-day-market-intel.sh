#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
JMKR_ROOT="${JMKR_ROOT:-/Users/gbserver/repos/jmkr_kj}"
VAULT_PATH="${OBSIDIAN_VAULT_PATH:-/Users/gbserver/Documents/Obsidian Vault}"
TARGET_DATE="${1:-$(TZ=Asia/Seoul date +%F)}"
ALLOW_PRECLOSE="${ALLOW_PRECLOSE:-0}"

phase_info="$(TZ=Asia/Seoul python3 - <<'PY'
from datetime import datetime
from zoneinfo import ZoneInfo
now = datetime.now(ZoneInfo('Asia/Seoul'))
hhmm = now.hour * 100 + now.minute
if hhmm < 900:
    phase = '장전'
elif hhmm < 1530:
    phase = '장중'
else:
    phase = '장후'
print(f"{now:%Y-%m-%d}|{phase}|{now:%Y-%m-%d %H:%M:%S KST}")
PY
)"
CURRENT_DATE="${phase_info%%|*}"
rest="${phase_info#*|}"
CURRENT_PHASE="${rest%%|*}"
CURRENT_TS="${rest#*|}"

ARCHIVE_PATH="$JMKR_ROOT/data/daily/archive/$TARGET_DATE.json"

echo "[auto-recover] now=$CURRENT_TS phase=$CURRENT_PHASE target_date=$TARGET_DATE"

if [[ "$ALLOW_PRECLOSE" != "1" && "$TARGET_DATE" == "$CURRENT_DATE" && "$CURRENT_PHASE" != "장후" ]]; then
  echo "[auto-recover] skip: current phase is $CURRENT_PHASE, waiting until 장후"
  exit 0
fi

validate_archive() {
  python3 - "$1" <<'PY'
import json, re, sys
from pathlib import Path
path = Path(sys.argv[1])
if not path.exists():
    print("missing")
    raise SystemExit(2)
try:
    payload = json.loads(path.read_text(encoding='utf-8'))
except Exception as exc:
    print(f"invalid_json:{exc}")
    raise SystemExit(3)
text = payload.get('originalText') or ''
message_type = payload.get('messageType')
parsing_info = payload.get('parsing_info') or {}
numbered_lines = len(re.findall(r'(?m)^\s*\d+\.\s', text))
has_top30 = any(tok in text for tok in ('상승률 TOP30', '상승률TOP30', '상승률 TOP 30'))
if message_type != 'market_close':
    print(f"invalid:messageType={message_type!r}")
    raise SystemExit(4)
if parsing_info.get('is_empty') is not False:
    print('invalid:is_empty')
    raise SystemExit(5)
if not has_top30:
    print('invalid:no_top30_phrase')
    raise SystemExit(6)
if numbered_lines < 20:
    print(f'invalid:numbered_lines={numbered_lines}')
    raise SystemExit(7)
print(f"valid:numbered_lines={numbered_lines}")
PY
}

if validate_archive "$ARCHIVE_PATH"; then
  echo "[auto-recover] archive already valid: $ARCHIVE_PATH"
else
  echo "[auto-recover] attempting recovery for $TARGET_DATE"
  (
    cd "$JMKR_ROOT"
    node services/telegram-parser-node/index.js debug "$TARGET_DATE" || true
    node services/telegram-parser-node/index.js parse-date "$TARGET_DATE" --force
  )
  validate_archive "$ARCHIVE_PATH"
fi

(
  cd "$JMKR_ROOT"
  python3 scripts/ingest_top30_to_market_intel.py "$TARGET_DATE" --apply
)

(
  cd "$ROOT"
  python3 scripts/update_market_intel_entrypoints.py --vault-path "$VAULT_PATH" --site-root "$ROOT" --jmkr-root "$JMKR_ROOT"
  ./scripts/sync-market-intel.sh
  npx quartz build -d content
)

echo "[auto-recover] done for $TARGET_DATE"
