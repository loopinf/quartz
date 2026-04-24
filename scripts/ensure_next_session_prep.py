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
WEEKDAY_KO = ["월", "화", "수", "목", "금", "토", "일"]
DOMINANT_THEME_RE = re.compile(r"^-\s+([^:]+):\s+(\d+)개\s+\((.*)\)\s*$")
LINK_RE = re.compile(r"\[\[(?:[^\]|]+/)?([^\]|]+)(?:\|[^\]]+)?\]\]")


@dataclass(frozen=True)
class ThemeCluster:
    name: str
    count: int
    members: list[str]


@dataclass(frozen=True)
class PrepContext:
    target_date: date
    base_date: date
    recap_path: Path
    close_input_path: Path
    briefing_path: Path | None
    existing_path: Path
    event_slugs: list[str]
    theme_clusters: list[ThemeCluster]
    ungrouped_names: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a next-session-prep note from prior close validated sources.")
    parser.add_argument("--target-date", help="YYYY-MM-DD target session date. Defaults to current required prep date in KST.")
    parser.add_argument("--vault-path", default=str(Path.home() / "Documents" / "Obsidian Vault"))
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing prep note if it already exists.")
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
        if not line.startswith("- "):
            continue
        match = DOMINANT_THEME_RE.match(line)
        if not match:
            continue
        name = match.group(1).strip()
        members = [item.strip() for item in match.group(3).split(",") if item.strip()]
        if name == "개별주":
            ungrouped.extend(members)
            continue
        clusters.append(ThemeCluster(name=name, count=int(match.group(2)), members=members))
    return clusters, ungrouped


def parse_event_slugs(recap_text: str, base_date: date) -> list[str]:
    slugs: list[str] = []
    for raw_line in section_lines(recap_text, "Created Event Notes"):
        match = LINK_RE.search(raw_line)
        if not match:
            continue
        slug = match.group(1).strip()
        if slug not in slugs:
            slugs.append(slug)
    if slugs:
        return slugs
    prefix = f"{base_date:%Y-%m-%d}_"
    seen: list[str] = []
    for cluster in parse_theme_clusters(recap_text)[0][:4]:
        slug = f"{prefix}{cluster.name}_모멘텀"
        if slug not in seen:
            seen.append(slug)
    return seen


def join_themes_for_sentence(clusters: list[ThemeCluster], limit: int = 3) -> str:
    names = [cluster.name for cluster in clusters[:limit]]
    if not names:
        return "뚜렷한 군집이 제한적"
    if len(names) == 1:
        return names[0]
    return " / ".join(names)


def limited_members(cluster: ThemeCluster, limit: int) -> list[str]:
    return cluster.members[:limit]


def bullet_members(names: list[str]) -> list[str]:
    return [f"  - {name}" for name in names]


def note_link(slug: str) -> str:
    return f"[[{slug}]]"


def event_link(slug: str) -> str:
    return f"[[market-intel/events/{slug}|{slug}]]"


def weekday_label(day: date) -> str:
    return f"{WEEKDAY_KO[day.weekday()]}요일"


def build_context(vault_market_intel: Path, target_date: date) -> PrepContext:
    daily_dir = vault_market_intel / "daily"
    base_date = previous_trading_day(target_date)
    recap_path = daily_dir / f"{base_date:%Y-%m-%d}_top30_recap.md"
    close_input_path = daily_dir / f"{base_date:%Y-%m-%d}_evening-briefing-input.md"
    briefing_path = daily_dir / f"{base_date:%Y-%m-%d}_evening-briefing.md"
    existing_path = daily_dir / f"{target_date:%Y-%m-%d}_next-session-prep.md"

    if not recap_path.exists():
        raise FileNotFoundError(f"validated recap missing: {recap_path}")
    if not close_input_path.exists():
        raise FileNotFoundError(f"close input missing: {close_input_path}")

    recap_text = recap_path.read_text(encoding="utf-8")
    recap_frontmatter = parse_frontmatter(recap_text)
    if recap_frontmatter.get("validation_status") != "validated":
        raise RuntimeError(f"recap not validated: {recap_path.name}")

    theme_clusters, ungrouped_names = parse_theme_clusters(recap_text)
    if not theme_clusters and not ungrouped_names:
        raise RuntimeError(f"no dominant theme structure parsed from {recap_path.name}")

    event_slugs = parse_event_slugs(recap_text, base_date)
    return PrepContext(
        target_date=target_date,
        base_date=base_date,
        recap_path=recap_path,
        close_input_path=close_input_path,
        briefing_path=briefing_path if briefing_path.exists() else None,
        existing_path=existing_path,
        event_slugs=event_slugs,
        theme_clusters=theme_clusters,
        ungrouped_names=ungrouped_names,
    )


def build_supporting_notes(context: PrepContext) -> list[str]:
    notes = [context.close_input_path.stem]
    if context.briefing_path:
        notes.append(context.briefing_path.stem)
    notes.extend(context.event_slugs[:5])
    deduped: list[str] = []
    for note in notes:
        if note not in deduped:
            deduped.append(note)
    return deduped


def render_frontmatter(context: PrepContext) -> str:
    supporting_notes = ", ".join(f'"{item}"' for item in build_supporting_notes(context))
    return "\n".join([
        "---",
        f"id: next-session-prep-{context.target_date:%Y-%m-%d}",
        "note_type: next_session_prep",
        f"created_at: {fmt_ts()}",
        f"updated_at: {fmt_ts()}",
        f"session_date: {context.target_date:%Y-%m-%d}",
        f"source_note: {context.recap_path.stem}",
        f"supporting_notes: [{supporting_notes}]",
        "reviewer: 헤르메스(ㅎㅁ)",
        "generation_mode: auto_prior_close_scaffold",
        "source_scope: prior_close_only",
        "same_day_intraday_excluded: true",
        "---",
    ])


def build_content(context: PrepContext) -> str:
    top_clusters = context.theme_clusters
    primary = top_clusters[:2]
    expansion = top_clusters[2:4]
    residual = top_clusters[4:6]
    primary_names = [name for cluster in primary for name in limited_members(cluster, 4)]
    expansion_names = [name for cluster in expansion for name in limited_members(cluster, 3)]
    residual_names = [name for cluster in residual for name in limited_members(cluster, 2)]
    if len(residual_names) < 4:
        residual_names.extend(context.ungrouped_names[: max(0, 4 - len(residual_names))])

    lines: list[str] = [
        render_frontmatter(context),
        "",
        f"# {context.target_date:%Y-%m-%d} Next Session Prep",
        "",
        "## Why this note exists",
        f"- 이 문서는 **{context.target_date:%Y-%m-%d} {weekday_label(context.target_date)} 장전 대응 문서**다.",
        f"- 기준 close는 `{context.base_date:%Y-%m-%d}`이고, 따라서 이 노트 안에서 `오늘`은 **{context.target_date:%Y-%m-%d} KST pre-open**을 뜻한다.",
        "- 이 문서는 `validated recap + close input + prior event notes`만으로 자동 생성한 **prior-close-only scaffold**이며, same-day intraday/close 정보는 포함하지 않는다.",
        f"- 장마감 정리는 {note_link(context.recap_path.stem)}에, 장전 실행 포인트는 이 문서에 분리한다.",
        "",
        "## Base context",
        f"- Validated recap: {note_link(context.recap_path.stem)}",
        f"- Close input: {note_link(context.close_input_path.stem)}",
    ]
    if context.briefing_path:
        lines.append(f"- Evening briefing: {note_link(context.briefing_path.stem)}")
    if context.event_slugs:
        lines.append("- Event notes:")
        for slug in context.event_slugs[:5]:
            lines.append(f"  - {event_link(slug)}")
    lines.extend([
        "",
        "핵심 base read:",
        f"- {context.base_date:%m/%d} validated TOP30는 **{join_themes_for_sentence(top_clusters)}** 축이 먼저 보이는 날이었다.",
    ])
    if top_clusters:
        first = top_clusters[0]
        lines.append(f"- 최우선 해석 축은 `{first.name}` continuation 여부이고, leader는 {', '.join(limited_members(first, 4))} 쪽이다.")
    if len(top_clusters) >= 2:
        second = top_clusters[1]
        lines.append(f"- 동시에 `{second.name}`가 보조/공동 주도축으로 붙는지 확인해야 하며, 대표 종목은 {', '.join(limited_members(second, 3))}다.")
    if context.ungrouped_names:
        lines.append(f"- 개별주/혼합 반응은 {', '.join(context.ungrouped_names[:5])} 쪽이므로, 군집보다 개별 수급으로 흩어지는지 같이 본다.")

    lines.extend(["", "## Carry-over themes"])
    if primary:
        lines.append("### 1순위 primary check")
        for cluster in primary:
            lines.append(f"- {cluster.name}")
            lines.extend(bullet_members(limited_members(cluster, 4)))
    if expansion:
        lines.append("")
        lines.append("### 2순위 expansion check")
        for cluster in expansion:
            lines.append(f"- {cluster.name}")
            lines.extend(bullet_members(limited_members(cluster, 3)))
    if residual or context.ungrouped_names:
        lines.append("")
        lines.append("### 3순위 residual / rotation check")
        for cluster in residual:
            lines.append(f"- {cluster.name}")
            lines.extend(bullet_members(limited_members(cluster, 2)))
        if context.ungrouped_names:
            lines.append("- 개별주/혼합")
            lines.extend(bullet_members(context.ungrouped_names[:5]))

    first_theme = top_clusters[0].name if top_clusters else "주도 테마"
    second_theme = top_clusters[1].name if len(top_clusters) >= 2 else "보조 축"
    third_theme = top_clusters[2].name if len(top_clusters) >= 3 else "후속 확산 테마"
    lines.extend([
        "",
        "## What to check at the open",
        f"1. **{first_theme}가 장초부터 거래대금 leader로 유지되는지 확인**",
        f"2. **{second_theme}가 {first_theme}와 함께 공동 주도축인지, 아니면 일부 종목 강세에 그치는지 확인**",
        f"3. **{third_theme}가 후속 확산을 만드는지, 아니면 headline 반응 후 약해지는지 확인**",
        "4. **전일 상위 급등주가 gap-only인지, 시초 이후 거래대금까지 유지하는지 확인**",
        "5. **시장 breadth가 따라붙는지, 아니면 군집 없이 개별주 순환매로 쪼개지는지 확인**",
        "",
        "## Priority names / sectors",
        "### A. leader 확인",
    ])
    for name in primary_names[:8]:
        lines.append(f"- {name}")
    lines.append("")
    lines.append("### B. 후속 확산 확인")
    for name in expansion_names[:8] or primary_names[4:8]:
        lines.append(f"- {name}")
    lines.append("")
    lines.append("### C. 재집중 / 반전 확인")
    for name in residual_names[:8]:
        lines.append(f"- {name}")

    lines.extend([
        "",
        "## Failure / invalidation conditions",
        f"- {first_theme} 상위주가 갭만 만들고 바로 밀리면 continuation 해석을 빠르게 낮춘다.",
        f"- {second_theme}가 breadth 없이 일부 종목만 강하면 공동 주도축 해석을 약화한다.",
        f"- {third_theme} 포함 후속 테마가 거래대금을 못 붙이면 확산 시나리오를 하향한다.",
        "- 지수/시장 breadth가 약하고 개별주만 튀면 전일 군집 해석보다 단기 순환매/소화 구간 가능성을 높인다.",
        "",
        "## One-line prep",
        f"**{context.target_date:%Y-%m-%d} 장전의 기본 시나리오는 {first_theme} 중심 continuation 여부를 먼저 확인하는 것이고, 장초부터 거래대금이 약하거나 {second_theme}/{third_theme} 쪽으로 분산되면 주도축 해석을 빠르게 조정해야 한다.**",
        "",
        "## Guardrail",
        "- 이 문서는 prior-close-only scaffold다.",
        "- 실제 결과 비교와 회고는 별도 replay/review 문서로 넘긴다.",
    ])
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

    if context.existing_path.exists() and not args.overwrite:
        print(f"SKIP existing {context.existing_path}")
        return 0

    content = build_content(context)
    context.existing_path.parent.mkdir(parents=True, exist_ok=True)
    context.existing_path.write_text(content, encoding="utf-8")
    print(f"WROTE {context.existing_path}")
    print(f"TARGET_DATE {target_date:%Y-%m-%d}")
    print(f"BASE_DATE {context.base_date:%Y-%m-%d}")
    print(f"SOURCE_RECAP {context.recap_path.name}")
    print(f"SOURCE_INPUT {context.close_input_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
