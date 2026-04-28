#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from market_intel_visuals import (  # noqa: E402
    build_related_stock_inline_section,
    parse_krx_corp_table,
    parse_naver_chart_xml,
    performance_sparkline_svg,
    sparkline_svg,
)
from market_session_helper import DEFAULT_CACHE_PATH, detect_market_session  # noqa: E402

KRX_CORP_LIST_URL = "https://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13"
NAVER_CHART_URL = "https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe=day&count={count}&requestType=0"
RELATED_SECTION_RE = re.compile(r"(## Related Stocks\n)(.*?)(?=\n## |\Z)", re.S)
EVENT_DATE_RE = re.compile(r"- (\d{4}-\d{2}-\d{2}):")
WIKILINK_RE = re.compile(r"\[\[(?P<target>[^|\]]+)(?:\|(?P<label>[^\]]+))?\]\]")
INLINE_STYLE_RE = re.compile(r"<style>.*?mi-related-inline-list.*?</style>\n*", re.S)
INLINE_DIV_RE = re.compile(r"<div class=\"mi-related-inline-list\">.*?(?=\n- \[\[|\Z)", re.S)
CHANGE_LINE_RE = re.compile(r"- 상승률:\s*([+-]?\d+(?:\.\d+)?)%\s*\((\d{4}-\d{2}-\d{2}) TOP30 기준\)")

MANUAL_CODES = {
    "삼성SDI": "006400",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Add compact related-stock sparklines to a stock entity note.")
    parser.add_argument("note_path")
    parser.add_argument("--vault-root", default=str(Path.home() / "Documents" / "Obsidian Vault" / "market-intel"))
    parser.add_argument("--count", type=int, default=20)
    parser.add_argument("--refresh-minutes", type=int, default=30)
    parser.add_argument("--force-refresh", action="store_true")
    return parser.parse_args()


def kst_now() -> datetime:
    return datetime.now(timezone(timedelta(hours=9)))


def asset_dir(vault_root: Path, note_stem: str) -> Path:
    return vault_root / "assets" / "stock-related-sparklines" / note_stem


def cache_path(vault_root: Path, note_stem: str) -> Path:
    return asset_dir(vault_root, note_stem) / "_cache.json"


def load_asset_cache(vault_root: Path, note_stem: str) -> dict[str, dict[str, str]]:
    path = cache_path(vault_root, note_stem)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(payload, dict):
        return {}
    cards = payload.get("cards", {})
    return cards if isinstance(cards, dict) else {}


def save_asset_cache(
    vault_root: Path,
    note_stem: str,
    *,
    cards: dict[str, dict[str, str]],
    market_phase: str,
    reference_trade_date: str | None,
    now: datetime,
) -> None:
    path = cache_path(vault_root, note_stem)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "updated_at": now.isoformat(),
        "market_phase": market_phase,
        "reference_trade_date": reference_trade_date,
        "cards": cards,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def expected_series_end_date(today: date, reference_trade_date: str | None) -> str:
    return reference_trade_date or today.isoformat()


def should_refresh_cached_asset(
    *,
    asset_path: Path,
    cache_entry: dict[str, str] | None,
    today: date,
    now: datetime,
    expected_end_date: str | None = None,
    refresh_minutes: int = 30,
    is_trading_day: bool | None = None,
    session_phase: str | None = None,
) -> bool:
    if not asset_path.exists() or not cache_entry:
        return True
    cached_end_date = str(cache_entry.get("series_end_date") or "")
    target_end_date = expected_end_date or today.isoformat()
    if cached_end_date < target_end_date:
        return True
    try:
        fetched_at = datetime.fromisoformat(str(cache_entry.get("fetched_at") or ""))
    except ValueError:
        return True
    if is_trading_day is None or session_phase is None:
        session = detect_market_session(now, cache_path=DEFAULT_CACHE_PATH)
        is_trading_day = session.is_trading_day
        session_phase = session.phase
    if not is_trading_day or session_phase != "장중":
        return False
    return now - fetched_at >= timedelta(minutes=refresh_minutes)



def fetch_text(url: str, encoding: str | None = None) -> str:
    with urllib.request.urlopen(url, timeout=20) as response:
        raw = response.read()
    return raw.decode(encoding or "utf-8", errors="ignore")


def load_krx_mapping() -> dict[str, str]:
    html = fetch_text(KRX_CORP_LIST_URL, encoding="euc-kr")
    mapping = parse_krx_corp_table(html)
    mapping.update(MANUAL_CODES)
    return mapping


def section_match(note_text: str) -> re.Match[str]:
    match = RELATED_SECTION_RE.search(note_text)
    if not match:
        raise SystemExit("Related Stocks section not found")
    return match


def related_names(section_body: str) -> list[str]:
    names: list[str] = []
    for match in WIKILINK_RE.finditer(section_body):
        label = (match.group("label") or "").strip()
        target = match.group("target").strip()
        derived = target.rsplit("/", 1)[-1].strip()
        name = label or derived
        if name and name not in names:
            names.append(name)
    return names


def stock_entity_path(vault_root: Path, stock_name: str) -> Path:
    return vault_root / "entities" / "stocks" / f"{stock_name}.md"


def infer_event_date(note_text: str) -> str:
    dates = EVENT_DATE_RE.findall(note_text)
    if not dates:
        raise SystemExit("Could not infer event date from Event History")
    return max(dates)


def latest_change_text(vault_root: Path, stock_name: str, target_date: str) -> str:
    entity_path = stock_entity_path(vault_root, stock_name)
    if not entity_path.exists():
        return ""
    text = entity_path.read_text(encoding="utf-8")
    for value, date in CHANGE_LINE_RE.findall(text):
        if date == target_date:
            sign = "+" if not value.startswith("-") else ""
            return f"{sign}{value}%"
    return ""


def asset_href(note_stem: str, stock_name: str) -> str:
    return "/market-intel/assets/stock-related-sparklines/{}/{}.svg".format(
        urllib.parse.quote(note_stem),
        urllib.parse.quote(stock_name),
    )


def write_svg_asset(vault_root: Path, note_stem: str, stock_name: str, svg: str) -> Path:
    path = asset_dir(vault_root, note_stem) / f"{stock_name}.svg"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
    return path


def format_compact_percent(value: float) -> str:
    rounded = round(value, 1)
    sign = "+" if rounded > 0 else ""
    text = f"{rounded:.1f}".rstrip("0").rstrip(".")
    return f"{sign}{text}%"


def build_cards(
    vault_root: Path,
    note_stem: str,
    names: list[str],
    code_map: dict[str, str],
    count: int,
    *,
    now: datetime,
    refresh_minutes: int,
    force_refresh: bool,
) -> tuple[list[dict[str, str]], int]:
    cards: list[dict[str, str]] = []
    missing: list[str] = []
    refreshed = 0
    cache = load_asset_cache(vault_root, note_stem)
    session = detect_market_session(now, cache_path=DEFAULT_CACHE_PATH)
    expected_end = now.date().isoformat() if session.is_trading_day else expected_series_end_date(now.date(), session.reference_trade_date)
    updated_cache: dict[str, dict[str, str]] = {}

    for name in names:
        code = code_map.get(name)
        if not code:
            missing.append(name)
            continue
        asset_path = asset_dir(vault_root, note_stem) / f"{name}.svg"
        cache_entry = cache.get(name)
        needs_refresh = force_refresh or should_refresh_cached_asset(
            asset_path=asset_path,
            cache_entry=cache_entry,
            today=now.date(),
            now=now,
            expected_end_date=expected_end,
            refresh_minutes=refresh_minutes,
        )
        series_end_date = str(cache_entry.get("series_end_date") or "") if cache_entry else ""

        if needs_refresh:
            chart_xml = fetch_text(NAVER_CHART_URL.format(code=code, count=count), encoding="euc-kr")
            rows = parse_naver_chart_xml(chart_xml)
            closes = [float(row["close"]) for row in rows]
            svg = performance_sparkline_svg(closes, width=112, height=24, stroke="#5b74db")
            write_svg_asset(vault_root, note_stem, name, svg)
            series_end_date = str(rows[-1]["date"]) if rows else ""
            refreshed += 1

        delta_text = ""
        if asset_path.exists():
            if not needs_refresh:
                chart_xml = fetch_text(NAVER_CHART_URL.format(code=code, count=count), encoding="euc-kr")
                rows = parse_naver_chart_xml(chart_xml)
                closes = [float(row["close"]) for row in rows]
            if closes:
                base = closes[0] or 1.0
                delta_text = format_compact_percent(((closes[-1] / base) - 1.0) * 100.0)

        updated_cache[name] = {
            "code": code,
            "series_end_date": series_end_date,
            "fetched_at": now.isoformat() if needs_refresh else str(cache_entry.get("fetched_at") or now.isoformat()),
        }
        cards.append(
            {
                "name": name,
                "entity_href": f"/market-intel/entities/stocks/{urllib.parse.quote(name)}",
                "sparkline_href": asset_href(note_stem, name),
                "change_text": "",
                "sparkline_delta_text": delta_text,
            }
        )

    save_asset_cache(
        vault_root,
        note_stem,
        cards=updated_cache,
        market_phase=session.phase,
        reference_trade_date=session.reference_trade_date,
        now=now,
    )
    if missing:
        print("Missing codes:", ", ".join(missing))
    return cards, refreshed


def decorate_inline_block(block: str) -> str:
    style = """
<style>
.mi-related-inline-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(220px,100%),1fr));gap:8px 12px;margin:8px 0 10px;max-width:100%;width:100%;overflow-x:clip}
.mi-related-inline-item{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:8px;min-width:0;max-width:100%;box-sizing:border-box;padding:6px 8px;border:1px solid var(--lightgray);border-radius:10px;background:color-mix(in srgb, var(--light) 94%, transparent);overflow:hidden}
.mi-related-inline-name{min-width:0;font-weight:600;text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mi-related-inline-spark-wrap{min-width:0;max-width:100%;width:clamp(84px,30vw,132px);display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;column-gap:4px;margin-left:auto}
.mi-related-inline-sparkline{display:block;min-width:0;width:100%;max-width:100%;height:auto;max-height:24px;opacity:.94}
.mi-related-inline-delta{font-size:.68rem;line-height:1;color:var(--gray);white-space:nowrap}
.mi-related-inline-list ~ ul{display:none}
@media (max-width: 800px){
  .mi-related-inline-list{grid-template-columns:1fr;gap:6px}
  .mi-related-inline-item{gap:6px;padding:6px}
  .mi-related-inline-name{font-size:.92rem}
  .mi-related-inline-spark-wrap{width:clamp(90px,34vw,138px)}
  .mi-related-inline-sparkline{max-height:22px}
}
@media (max-width: 480px){
  .mi-related-inline-item{grid-template-columns:minmax(0,1fr);align-items:stretch;row-gap:4px}
  .mi-related-inline-spark-wrap{width:100%;grid-template-columns:minmax(0,1fr) auto;justify-self:stretch;margin-left:0}
  .mi-related-inline-sparkline{justify-self:stretch;width:100%;max-height:20px}
  .mi-related-inline-delta{font-size:.64rem}
}
</style>
""".strip()
    return f"{style}\n\n{block.strip()}\n"


def inject_inline_block(section_body: str, inline_block: str) -> str:
    cleaned = INLINE_STYLE_RE.sub("", section_body)
    cleaned = INLINE_DIV_RE.sub("", cleaned).lstrip("\n")
    return f"{inline_block.rstrip()}\n\n{cleaned.lstrip()}"


def main() -> int:
    args = parse_args()
    now = kst_now()
    vault_root = Path(args.vault_root).expanduser().resolve()
    note_path = Path(args.note_path).expanduser().resolve()
    note_text = note_path.read_text(encoding="utf-8")
    match = section_match(note_text)
    section_body = match.group(2)
    names = related_names(section_body)
    if not names:
        raise SystemExit(f"No related stock wikilinks found in {note_path}")
    cards, refreshed = build_cards(
        vault_root,
        note_path.stem,
        names,
        load_krx_mapping(),
        args.count,
        now=now,
        refresh_minutes=args.refresh_minutes,
        force_refresh=args.force_refresh,
    )
    inline_block = decorate_inline_block(build_related_stock_inline_section(cards))
    new_body = inject_inline_block(section_body, inline_block)
    updated = note_text[: match.start(2)] + new_body + note_text[match.end(2) :]
    note_path.write_text(updated, encoding="utf-8")
    print(f"Added inline related-stock sparklines to {note_path}")
    print(f"  cards: {len(cards)}")
    print(f"  refreshed: {refreshed}")
    print(f"  refresh_minutes: {args.refresh_minutes}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
