#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")
OUTCOME_DIR = Path("/Users/gbserver/repos/jmkr_kj/data/signals/high-signal-entry-outcomes")
RULE_ORDER = [
    "same_close",
    "next_open",
    "wait_1d_close",
    "wait_2d_close",
    "wait_3d_close",
    "pullback_2pct",
    "pullback_4pct",
]
OVERLAP_RE = re.compile(r"^-\s+([^\(]+?)\s+\((\d{2}/\d{2}),\s+([^\)]+)\)")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Inject conditional-probability / outcome summary into next-session-prep notes")
    ap.add_argument("--vault-path", default=str(Path.home() / "Documents" / "Obsidian Vault"))
    ap.add_argument("--target-date", help="YYYY-MM-DD target prep date")
    return ap.parse_args()


def market_phase(now: datetime) -> str:
    hhmm = now.hour * 100 + now.minute
    if hhmm < 900:
        return "장전"
    if hhmm < 1530:
        return "장중"
    return "장후"


def next_trading_day(day: date) -> date:
    cursor = day + timedelta(days=1)
    while cursor.weekday() >= 5:
        cursor += timedelta(days=1)
    return cursor


def choose_target_date(raw: str | None) -> date:
    if raw:
        return date.fromisoformat(raw)
    now = datetime.now(KST)
    return next_trading_day(now.date()) if market_phase(now) == "장후" else now.date()


def section_range(lines: list[str], heading: str) -> tuple[int, int] | None:
    needle = f"## {heading}"
    start = None
    for idx, line in enumerate(lines):
        if line.strip() == needle:
            start = idx
            break
    if start is None:
        return None
    end = len(lines)
    for idx in range(start + 1, len(lines)):
        if lines[idx].startswith("## "):
            end = idx
            break
    return start, end


def parse_overlap_names(lines: list[str]) -> dict[str, list[str]]:
    buckets: dict[str, list[str]] = {"breakout": [], "near-high": [], "technical": []}
    current = None
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("- breakout overlap 종목"):
            current = "breakout"
            continue
        if line.startswith("- near-52w-high / near-ATH overlap 종목"):
            current = "near-high"
            continue
        if line.startswith("- carry-over theme와 겹치는 technical support names"):
            current = "technical"
            continue
        if current and line.startswith("  - "):
            m = OVERLAP_RE.match(line.strip())
            if m:
                buckets[current].append(m.group(1).strip())
            else:
                buckets[current].append(line.strip().removeprefix("- ").strip())
        elif line.startswith("-"):
            current = None
    for key, vals in buckets.items():
        seen = []
        for v in vals:
            if v not in seen:
                seen.append(v)
        buckets[key] = seen
    return buckets


def load_all_outcomes() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(OUTCOME_DIR.glob("20*.json")):
        if not path.name[:4].isdigit():
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        rows.extend(payload.get("outcomes", []))
    return rows


def load_global_summary() -> list[dict]:
    path = OUTCOME_DIR / "vbtpro-recheck-2025-04-01-to-2026-04-16.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload.get("summary", [])


def summarize_rule_rows(rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["entry_rule"]].append(row)
    out = []
    for rule in RULE_ORDER:
        rule_rows = grouped.get(rule, [])
        avail = [r for r in rule_rows if r.get("entry_available")]
        ret20 = [r["ret_20d"] for r in avail if r.get("ret_20d") is not None]
        ret10 = [r["ret_10d"] for r in avail if r.get("ret_10d") is not None]
        ret5 = [r["ret_5d"] for r in avail if r.get("ret_5d") is not None]
        out.append({
            "entry_rule": rule,
            "total": len(rule_rows),
            "available": len(avail),
            "available_rate": round(len(avail) / len(rule_rows), 4) if rule_rows else None,
            "ret_5d_avg": round(sum(ret5) / len(ret5), 2) if ret5 else None,
            "ret_10d_avg": round(sum(ret10) / len(ret10), 2) if ret10 else None,
            "ret_20d_avg": round(sum(ret20) / len(ret20), 2) if ret20 else None,
            "ret_20d_win_rate": round(sum(1 for x in ret20 if x > 0) / len(ret20), 4) if ret20 else None,
        })
    return out


def best_rules(summary_rows: list[dict], min_available: int = 20) -> list[dict]:
    def avail_count(r: dict) -> int:
        return int(r.get("available") or r.get("trade_count") or 0)

    eligible = [r for r in summary_rows if avail_count(r) >= min_available and r.get("ret_20d_avg") is not None]
    return sorted(
        eligible,
        key=lambda r: (r.get("ret_20d_sharpe", -999), r.get("ret_20d_avg", -999), r.get("ret_10d_avg", -999)),
        reverse=True,
    )


def format_rule(rule: str) -> str:
    return rule.replace("_", " ")


def build_section(note_text: str) -> str:
    lines = note_text.splitlines()
    hs_range = section_range(lines, "신고가 / high-signal 팩트층")
    if hs_range is None:
        return ""
    hs_lines = lines[hs_range[0] + 1 : hs_range[1]]
    buckets = parse_overlap_names(hs_lines)
    rows = load_all_outcomes()
    global_summary = load_global_summary()
    out: list[str] = ["## Conditional probability / entry-rule summary"]
    if global_summary:
        ranked = best_rules([
            {
                "entry_rule": r["entry_rule"],
                "trade_count": r.get("trade_count", 0),
                "ret_5d_avg": r.get("ret_5d_avg"),
                "ret_10d_avg": r.get("ret_10d_avg"),
                "ret_20d_avg": r.get("ret_20d_avg"),
                "ret_20d_win_rate": r.get("ret_20d_win_rate"),
                "ret_20d_sharpe": r.get("ret_20d_sharpe"),
            }
            for r in global_summary
        ], min_available=100)
        out.append("- full-range breakout baseline (2025-04-01 ~ 2026-04-16, vectorbtpro recheck)")
        for item in ranked[:3]:
            out.append(
                f"  - `{item['entry_rule']}`: 20d avg `{item['ret_20d_avg']}%`, 10d avg `{item.get('ret_10d_avg')}%`, 20d win `{item.get('ret_20d_win_rate')}`"
            )
        out.append("- baseline 해석: 전구간 breakout backtest에선 `wait_2d_close / wait_3d_close / next_open`이 Sharpe 기준 상위권이고, `pullback` 계열은 평균 수익은 강하지만 available 비율을 같이 봐야 한다.")
    else:
        out.append("- full-range vectorbtpro baseline summary unavailable")

    breakout_names = buckets.get("breakout", [])
    near_names = buckets.get("near-high", [])
    technical_names = buckets.get("technical", [])
    names = []
    for n in breakout_names + near_names + technical_names:
        if n not in names:
            names.append(n)

    if names:
        out.append("")
        out.append("### 현재 prep 종목에 대한 lookup")
        for name in names[:8]:
            name_rows = [r for r in rows if r.get("stock_name") == name]
            if not name_rows:
                out.append(f"- `{name}`: historical outcome row가 아직 없다.")
                continue
            summary = summarize_rule_rows(name_rows)
            ranked = [r for r in best_rules(summary, min_available=3) if (r.get('ret_20d_avg') or -999) > 0]
            if ranked:
                top = ranked[:2]
                rule_bits = []
                for item in top:
                    rule_bits.append(
                        f"`{item['entry_rule']}`(20d avg {item['ret_20d_avg']}%, avail {item['available']}/{item['total']})"
                    )
                out.append(f"- `{name}`: stock-specific breakout history 기준 우세 rule → {', '.join(rule_bits)}")
            else:
                out.append(f"- `{name}`: stock-specific 표본이 부족해서 global breakout baseline을 우선 참조해야 한다.")

    if breakout_names:
        breakout_rows = [r for r in rows if r.get("stock_name") in breakout_names]
        breakout_summary = summarize_rule_rows(breakout_rows)
        ranked = best_rules(breakout_summary, min_available=10)
        if ranked:
            out.append("")
            out.append("### breakout overlap basket 요약")
            for item in ranked[:3]:
                out.append(
                    f"- `{item['entry_rule']}`: 20d avg `{item['ret_20d_avg']}%`, 5d avg `{item['ret_5d_avg']}%`, available `{item['available']}/{item['total']}`"
                )
            out.append("- 사용법: breakout overlap 이름들은 기본적으로 `same_close` 추격보다 위 우세 rule을 먼저 검토하고, available 비율이 낮은 pullback rule은 miss-trade bias를 함께 본다.")

    if near_names:
        out.append("")
        out.append("### near-high overlap 해석 규칙")
        out.append("- direct near-high state outcome table는 아직 따로 export되지 않았다.")
        out.append("- 따라서 near-high 이름은 즉시 매매 rule을 단정하기보다, breakout overlap으로 전환되는지와 최근 breakout baseline(`next_open / wait_1d_close / pullback`)을 함께 참조한다.")
        out.append("- 다음 단계는 near-high state 자체를 anchor로 한 별도 outcome table을 추가하는 것이다.")

    if technical_names:
        out.append("")
        out.append("### prep에서 쓰는 요령")
        out.append("- `technical support names` 안에서도 stock-specific 표본이 있는 이름은 개별 lookup을 우선 본다.")
        out.append("- 표본이 약하면 basket 요약과 full-range baseline을 우선 사용한다.")
        out.append("- 이 섹션은 매수 추천이 아니라 **장전 우선 확인 rule lookup**이다.")

    return "\n".join(out)


def inject_section(note_text: str, new_section: str) -> str:
    lines = note_text.splitlines()
    start_end = section_range(lines, "Conditional probability / entry-rule summary")
    insert_before = section_range(lines, "Carry-over themes 선정 근거")
    new_lines = new_section.splitlines()
    if start_end:
        start, end = start_end
        lines = lines[:start] + new_lines + [""] + lines[end:]
    elif insert_before:
        start, _ = insert_before
        lines = lines[:start] + new_lines + [""] + lines[start:]
    else:
        lines.extend(["", *new_lines])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    target_date = choose_target_date(args.target_date)
    prep_path = Path(args.vault_path).expanduser().resolve() / "market-intel" / "daily" / f"{target_date:%Y-%m-%d}_next-session-prep.md"
    if not prep_path.exists():
        print(f"SKIP missing {prep_path}")
        return 0
    text = prep_path.read_text(encoding="utf-8")
    section = build_section(text)
    if not section:
        print(f"SKIP no-high-signal-section {prep_path}")
        return 0
    updated = inject_section(text, section)
    prep_path.write_text(updated, encoding="utf-8")
    print(f"WROTE {prep_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
