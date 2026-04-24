#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")
DOMINANT_THEME_RE = re.compile(r"^-\s+([^:]+):\s+(\d+)개\s+\((.*)\)\s*$")
LINK_RE = re.compile(r"\[\[(?:[^\]|]+/)?([^\]|]+)(?:\|[^\]]+)?\]\]")
SNAPSHOT_RE = re.compile(r"^-\s+(전일|금일)\s+(거래소|코스닥):\s+(.+)$")


@dataclass(frozen=True)
class ThemeCluster:
    name: str
    count: int
    members: list[str]


@dataclass(frozen=True)
class RecentRecap:
    day: date
    path: Path
    themes: list[str]


@dataclass(frozen=True)
class BriefingContext:
    target_date: date
    input_path: Path
    output_path: Path
    recap_path: Path | None
    recap_validated: bool
    recap_clusters: list[ThemeCluster]
    ungrouped_names: list[str]
    event_slugs: list[str]
    source_type: str
    source_notes: list[str]
    local_tape_lines: list[str]
    continuity_lines: list[str]
    market_snapshot_lines: list[str]
    recent_recaps: list[RecentRecap]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an evening briefing output note from the daily input/recap.")
    parser.add_argument("--target-date", help="YYYY-MM-DD review date. Defaults to required evening-briefing date in KST.")
    parser.add_argument("--vault-path", default=str(Path.home() / "Documents" / "Obsidian Vault"))
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def market_phase(now: datetime) -> str:
    hhmm = now.hour * 100 + now.minute
    if hhmm < 900:
        return "장전"
    if hhmm < 1530:
        return "장중"
    return "장후"


def previous_trading_day(day: date) -> date:
    cursor = day - timedelta(days=1)
    while cursor.weekday() >= 5:
        cursor -= timedelta(days=1)
    return cursor


def choose_target_date(raw: str | None) -> date:
    if raw:
        return date.fromisoformat(raw)
    now = datetime.now(KST)
    return now.date() if market_phase(now) == "장후" else previous_trading_day(now.date())


def fmt_ts(dt: datetime | None = None) -> str:
    dt = dt or datetime.now(KST)
    return dt.strftime("%Y-%m-%d %H:%M:%S KST")


def parse_frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    result: dict[str, object] = {}
    for raw_line in parts[0].splitlines()[1:]:
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not value:
            result[key] = ""
            continue
        try:
            result[key] = ast.literal_eval(value)
            continue
        except Exception:
            pass
        result[key] = value.strip('"')
    return result


def section_lines(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    capture = False
    collected: list[str] = []
    needle = f"## {heading}"
    for line in lines:
        if line.strip() == needle:
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture:
            collected.append(line)
    return collected


def parse_theme_clusters(recap_text: str) -> tuple[list[ThemeCluster], list[str]]:
    clusters: list[ThemeCluster] = []
    ungrouped: list[str] = []
    for raw_line in section_lines(recap_text, "Dominant Themes"):
        line = raw_line.strip()
        match = DOMINANT_THEME_RE.match(line)
        if not match:
            continue
        name = match.group(1).strip()
        members = [item.strip() for item in match.group(3).split(",") if item.strip()]
        if name == "개별주":
            ungrouped.extend(members)
        else:
            clusters.append(ThemeCluster(name=name, count=int(match.group(2)), members=members))
    return clusters, ungrouped


def parse_event_slugs(recap_text: str) -> list[str]:
    slugs: list[str] = []
    for raw_line in section_lines(recap_text, "Created Event Notes"):
        match = LINK_RE.search(raw_line)
        if not match:
            continue
        slug = match.group(1).strip()
        if slug not in slugs:
            slugs.append(slug)
    return slugs


def parse_market_snapshot_lines(recap_text: str) -> list[str]:
    lines: list[str] = []
    for raw_line in section_lines(recap_text, "Market Snapshot"):
        line = raw_line.strip()
        match = SNAPSHOT_RE.match(line)
        if match:
            lines.append(f"- {match.group(1)} {match.group(2)} `{match.group(3)}`")
    return lines


def extract_local_tape_lines(input_text: str) -> list[str]:
    collected: list[str] = []
    for raw_line in section_lines(input_text, "JMKR breadth / market stats"):
        line = raw_line.rstrip()
        if "Local observed tape" in line or "Same-day collected output hints" in line:
            continue
        if line.strip().startswith("- ") and "전체 종목 수" not in line:
            collected.append(line.strip())
    return collected[:6]


def extract_continuity_lines(input_text: str) -> list[str]:
    lines = [line.strip() for line in section_lines(input_text, "Continuity context from existing market-intel notes") if line.strip().startswith("-")]
    return lines[-4:]


def collect_recent_validated_recaps(daily_dir: Path, anchor_date: date, limit: int = 5) -> list[RecentRecap]:
    rows: list[RecentRecap] = []
    cursor = anchor_date
    while len(rows) < limit:
        candidate = daily_dir / f"{cursor:%Y-%m-%d}_top30_recap.md"
        if candidate.exists():
            recap_text = candidate.read_text(encoding="utf-8")
            recap_frontmatter = parse_frontmatter(recap_text)
            if recap_frontmatter.get("validation_status") == "validated":
                clusters, _ = parse_theme_clusters(recap_text)
                rows.append(RecentRecap(day=cursor, path=candidate, themes=[cluster.name for cluster in clusters[:5]]))
        prev = previous_trading_day(cursor)
        if prev == cursor:
            break
        cursor = prev
        if anchor_date - cursor > timedelta(days=14):
            break
    return rows


def summarize_recent_theme_recurrence(recent_recaps: list[RecentRecap]) -> list[str]:
    counts: dict[str, int] = {}
    for row in recent_recaps:
        for theme in row.themes:
            counts[theme] = counts.get(theme, 0) + 1
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [f"- `{theme}`: 최근 {len(recent_recaps)}거래일 중 {cnt}회 등장" for theme, cnt in ordered[:4]]


def recent_recap_reference_lines(recent_recaps: list[RecentRecap]) -> list[str]:
    return [f"- [[{row.path.stem}]] — {', '.join(row.themes[:4]) if row.themes else 'theme parse unavailable'}" for row in recent_recaps]


def summarize_theme_names(clusters: list[ThemeCluster], limit: int = 3) -> str:
    names = [cluster.name for cluster in clusters[:limit]]
    if not names:
        return "뚜렷한 군집"
    if len(names) == 1:
        return names[0]
    return "·".join(names)


def build_context(vault_market_intel: Path, target_date: date) -> BriefingContext:
    daily_dir = vault_market_intel / "daily"
    input_path = daily_dir / f"{target_date:%Y-%m-%d}_evening-briefing-input.md"
    output_path = daily_dir / f"{target_date:%Y-%m-%d}_evening-briefing.md"
    recap_path = daily_dir / f"{target_date:%Y-%m-%d}_top30_recap.md"

    if not input_path.exists():
        raise FileNotFoundError(f"evening briefing input missing: {input_path}")

    input_text = input_path.read_text(encoding="utf-8")
    input_frontmatter = parse_frontmatter(input_text)
    source_type = str(input_frontmatter.get("source_type") or "unknown")
    source_notes = list(input_frontmatter.get("source_notes") or [])

    recap_validated = False
    recap_clusters: list[ThemeCluster] = []
    ungrouped_names: list[str] = []
    event_slugs: list[str] = []
    market_snapshot_lines: list[str] = []
    recap_ref: Path | None = None
    if recap_path.exists():
        recap_text = recap_path.read_text(encoding="utf-8")
        recap_frontmatter = parse_frontmatter(recap_text)
        recap_validated = recap_frontmatter.get("validation_status") == "validated"
        if recap_validated:
            recap_ref = recap_path
            recap_clusters, ungrouped_names = parse_theme_clusters(recap_text)
            event_slugs = parse_event_slugs(recap_text)
            market_snapshot_lines = parse_market_snapshot_lines(recap_text)

    return BriefingContext(
        target_date=target_date,
        input_path=input_path,
        output_path=output_path,
        recap_path=recap_ref,
        recap_validated=recap_validated,
        recap_clusters=recap_clusters,
        ungrouped_names=ungrouped_names,
        event_slugs=event_slugs,
        source_type=source_type,
        source_notes=source_notes,
        local_tape_lines=extract_local_tape_lines(input_text),
        continuity_lines=extract_continuity_lines(input_text),
        market_snapshot_lines=market_snapshot_lines,
        recent_recaps=collect_recent_validated_recaps(daily_dir, target_date, limit=5),
    )


def note_link(slug: str) -> str:
    return f"[[{slug}]]"


def event_link(slug: str) -> str:
    return f"[[market-intel/events/{slug}|{slug}]]"


def make_oneliner(context: BriefingContext) -> str:
    if context.recap_validated and context.recap_clusters:
        lead = context.recap_clusters[0]
        others = summarize_theme_names(context.recap_clusters[1:4], limit=3)
        return f"**{context.target_date:%m/%d}는 {lead.name} 군집이 가장 선명하게 확인된 가운데 {others} 축이 함께 붙은 선택적 순환매 장세였고, 최근 5거래일 흐름상 내일은 breadth가 실제로 이어지는 주도축이 무엇인지 가려내는 것이 핵심이다.**"
    return f"**{context.target_date:%m/%d}는 validated same-day recap 없이 제한된 입력으로만 정리한 partial mode 브리핑이지만, 최근 5거래일 정리 데이터를 바탕으로 내일은 전력·설비·반도체 등 관측된 순환매 축이 실제로 이어지는지 보수적으로 확인해야 한다.**"


def build_what_mattered(context: BriefingContext) -> list[str]:
    lines: list[str] = []
    if context.recap_validated and context.recap_clusters:
        for cluster in context.recap_clusters[:4]:
            members = ", ".join(cluster.members[:6])
            lines.append(f"- **{cluster.name}** 군집이 핵심 축으로 확인됐다.")
            lines.append(f"  - {members}")
        if context.market_snapshot_lines:
            lines.append("- 지수/시장 스냅샷")
            lines.extend([f"  {line[1:]}" if line.startswith("-") else f"  - {line}" for line in context.market_snapshot_lines[:4]])
    else:
        lines.append("- **partial mode**: validated same-day recap이 없어 input 기준 관찰치만 요약한다.")
        for line in context.local_tape_lines[:4]:
            lines.append(line)
    return lines


def build_continuity_change(context: BriefingContext) -> list[str]:
    lines = ["- **continuity**"]
    if context.recap_validated and context.recap_clusters:
        lead = context.recap_clusters[0]
        lines.append(f"  - validated recap 기준 {lead.name}가 당일 최상위 군집으로 확인돼, 다음 세션도 이 축을 기준선으로 봐야 한다.")
        if len(context.recap_clusters) >= 2:
            second = context.recap_clusters[1]
            lines.append(f"  - {second.name}도 보조 주도축으로 붙어 단일 테마 one-shot보다는 다축 선택적 순환매 가능성을 남겼다.")
    else:
        lines.append("  - same-day validated recap 부재로 continuity 판단 자체가 제한적이다.")
    if context.recent_recaps:
        lines.append("  - 최근 5거래일 정리 데이터 기준 반복 등장 테마는 아래와 같다.")
        for line in summarize_recent_theme_recurrence(context.recent_recaps)[:3]:
            lines.append(f"  {line}")
    lines.append("- **change**")
    if context.continuity_lines:
        for line in context.continuity_lines[-2:]:
            lines.append(f"  {line}")
    elif context.recap_validated and context.recap_clusters:
        lines.append("  - 최근 며칠의 단일 과집중 장세와 달리, 이날은 여러 군집이 병행한 선택적 확산 쪽에 더 가까웠다.")
    else:
        lines.append("  - 무엇이 실제 주도축으로 확정됐는지는 validated ingest 확인 후 재판정이 필요하다.")
    return lines


def build_tomorrow_checklist(context: BriefingContext) -> list[str]:
    if context.recap_validated and context.recap_clusters:
        top = context.recap_clusters[0]
        second = context.recap_clusters[1] if len(context.recap_clusters) > 1 else None
        third = context.recap_clusters[2] if len(context.recap_clusters) > 2 else None
        return [
            f"1. **{top.name} 축이 상위 1종목 반응이 아니라 섹터 breadth로 유지되는지 확인**",
            f"2. **{second.name if second else top.name} 축이 보조 반응이 아니라 공동 주도축으로 거래대금을 동반하는지 확인**",
            f"3. **{third.name if third else '후속 군집'} 축이 실제 확산을 만드는지, 아니면 headline one-shot인지 확인**",
            "4. **상위 급등주가 gap-only인지, 시초 이후 follow-through를 유지하는지 확인**",
            "5. **최근 5거래일 흐름 위에서 시장이 breadth 확산인지, 소수 leader 집중인지 구분**",
        ]
    return [
        "1. **partial mode임을 전제로 전력·설비·반도체 관측축이 장초에도 이어지는지 확인**",
        "2. **소수 leader만 살아남는지, breadth가 실제로 붙는지 확인**",
        "3. **validated same-day recap 부재 상태에서 과한 확신형 해석을 피하고 보수적으로 대응**",
    ]


def build_risk_notes(context: BriefingContext) -> list[str]:
    if context.recap_validated and context.recap_clusters:
        top = context.recap_clusters[0].name
        return [
            f"- {top}가 장초 갭만 만들고 breadth 없이 빠르게 압축되면 continuation 해석을 낮춰야 한다.",
            "- 보조 군집이 개별 뉴스 반응에 그치면 다축 순환매 해석은 과대평가일 수 있다.",
            "- 최근 5거래일 정리 데이터와 달리 소수 종목만 남으면 단기 순환매/소화 구간일 수 있다.",
        ]
    return [
        "- `partial mode`: validated same-day recap이 없으므로 확정형 브리핑처럼 쓰면 안 된다.",
        "- local observational input은 same-day theme graph 확정이 아니라 보조 관찰치다.",
    ]


def build_linked_references(context: BriefingContext) -> list[str]:
    lines = [f"- {note_link(context.input_path.stem)}"]
    if context.recap_path:
        lines.append(f"- {note_link(context.recap_path.stem)}")
    for row in context.recent_recaps[:4]:
        lines.append(f"- {note_link(row.path.stem)}")
    for slug in context.event_slugs[:5]:
        lines.append(f"- {event_link(slug)}")
    deduped: list[str] = []
    for line in lines:
        if line not in deduped:
            deduped.append(line)
    return deduped


def render_frontmatter(context: BriefingContext) -> str:
    return "\n".join([
        "---",
        f"id: evening-briefing-{context.target_date:%Y-%m-%d}",
        "note_type: daily_evening_briefing",
        f"created_at: {fmt_ts()}",
        f"updated_at: {fmt_ts()}",
        f"review_date: {context.target_date:%Y-%m-%d}",
        f"source_note: {context.input_path.stem}",
        "reviewer: 헤르메스(ㅎㅁ)",
        f"generation_mode: {'auto_validated_output' if context.recap_validated else 'auto_partial_output'}",
        f"confidence_mode: {'validated' if context.recap_validated else 'partial'}",
        "---",
    ])


def build_content(context: BriefingContext) -> str:
    lines = [
        render_frontmatter(context),
        "",
        f"# {context.target_date:%Y-%m-%d} Evening Briefing",
        "",
        "## Recent 5-trading-day organized context",
    ]
    if context.recent_recaps:
        lines.extend(recent_recap_reference_lines(context.recent_recaps))
        lines.append("")
        lines.append("반복 등장 테마:")
        lines.extend(summarize_recent_theme_recurrence(context.recent_recaps))
    else:
        lines.append("- 최근 5거래일 validated recap reference unavailable")

    lines.extend([
        "",
        "## One-line market read",
        make_oneliner(context),
        "",
        "## What mattered today",
        *build_what_mattered(context),
        "",
        "## Continuity vs change",
        *build_continuity_change(context),
        "",
        "## Tomorrow open checklist",
        *build_tomorrow_checklist(context),
        "",
        "## Risk / invalidation notes",
        *build_risk_notes(context),
        "",
        "## Linked references",
        *build_linked_references(context),
        "",
        "## Note",
    ])
    if context.recap_validated:
        lines.append(f"- 이 브리핑은 {context.target_date:%Y-%m-%d} close 기준 validated recap + input + 최근 5거래일 정리 데이터를 바탕으로 자동 생성됐다.")
        next_day = context.target_date + timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)
        lines.append(f"- 다음 세션 장전 계획은 별도 [[{next_day:%Y-%m-%d}_next-session-prep]] 에서 본다.")
    else:
        lines.append("- `partial mode`: validated same-day recap이 없어 제한된 입력 기반으로만 자동 생성됐다.")
        lines.append("- validated ingest가 들어오면 같은 날짜 output을 overwrite해서 신뢰도를 올릴 수 있다.")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    vault_root = Path(args.vault_path)
    vault_market_intel = vault_root / "market-intel"
    target_date = choose_target_date(args.target_date)
    try:
        context = build_context(vault_market_intel, target_date)
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"SKIP prerequisites for {target_date:%Y-%m-%d}: {exc}")
        return 0

    if context.output_path.exists() and not args.overwrite:
        print(f"SKIP existing {context.output_path}")
        return 0

    context.output_path.write_text(build_content(context), encoding="utf-8")
    print(f"WROTE {context.output_path}")
    print(f"TARGET_DATE {target_date:%Y-%m-%d}")
    print(f"INPUT {context.input_path.name}")
    print(f"MODE {'validated' if context.recap_validated else 'partial'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
