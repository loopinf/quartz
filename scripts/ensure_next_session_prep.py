#!/usr/bin/env python3
from __future__ import annotations

import argparse
import ast
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")
WEEKDAY_KO = ["월", "화", "수", "목", "금", "토", "일"]
DOMINANT_THEME_RE = re.compile(r"^-\s+([^:]+):\s+(\d+)개\s+\((.*)\)\s*$")
LINK_RE = re.compile(r"\[\[(?:[^\]|]+/)?([^\]|]+)(?:\|[^\]]+)?\]\]")
ENTITY_LINK_RE = re.compile(r"\[\[market-intel/entities/stocks/([^\]|]+)(?:\|[^\]]+)?\]\]")
HIGH_SIGNAL_DIR = Path("/Users/gbserver/repos/jmkr_kj/data/signals/high-signals")


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
class EntityMemory:
    name: str
    path: Path
    theme_tags: list[str]
    event_history: list[str]
    related_stocks: list[str]


@dataclass(frozen=True)
class PrepContext:
    vault_market_intel: Path
    target_date: date
    base_date: date
    recap_path: Path
    close_input_path: Path
    briefing_path: Path | None
    existing_path: Path
    event_slugs: list[str]
    theme_clusters: list[ThemeCluster]
    ungrouped_names: list[str]
    recent_recaps: list[RecentRecap]


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


def theme_recurrence_count(recent_recaps: list[RecentRecap]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in recent_recaps:
        for theme in row.themes:
            counts[theme] = counts.get(theme, 0) + 1
    return counts


def recent_recap_reference_lines(recent_recaps: list[RecentRecap]) -> list[str]:
    return [f"- [[{row.path.stem}]] — {', '.join(row.themes[:4]) if row.themes else 'theme parse unavailable'}" for row in recent_recaps]


def has_same_window_high_signal(recent_recaps: list[RecentRecap]) -> bool:
    for row in recent_recaps:
        if (HIGH_SIGNAL_DIR / f"{row.day:%Y-%m-%d}.json").exists():
            return True
    return False


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


def stock_entity_link(name: str) -> str:
    return f"[[market-intel/entities/stocks/{name}|{name}]]"


def stock_entity_path(vault_market_intel: Path, name: str) -> Path:
    return vault_market_intel / "entities" / "stocks" / f"{name}.md"


def review_note_slug(target_date: date) -> str:
    return f"replay-{target_date:%Y-%m-%d}-next-session-prep"


def review_note_link(target_date: date) -> str:
    slug = review_note_slug(target_date)
    return f"[[market-intel/research/{slug}|{slug}]]"


def review_note_path(vault_market_intel: Path, target_date: date) -> Path:
    return vault_market_intel / "research" / f"{review_note_slug(target_date)}.md"


def parse_entity_memory(vault_market_intel: Path, name: str) -> EntityMemory | None:
    path = stock_entity_path(vault_market_intel, name)
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    theme_tags = [line.strip()[2:].strip() for line in section_lines(text, "Theme Tags") if line.strip().startswith("- ")]
    event_history = [line.strip()[2:].strip() for line in section_lines(text, "Event History") if line.strip().startswith("- ")]
    related_stocks: list[str] = []
    for raw_line in section_lines(text, "Related Stocks"):
        match = ENTITY_LINK_RE.search(raw_line)
        if not match:
            continue
        related_name = match.group(1).strip()
        if related_name == name or related_name in related_stocks:
            continue
        related_stocks.append(related_name)
    return EntityMemory(
        name=name,
        path=path,
        theme_tags=theme_tags,
        event_history=event_history,
        related_stocks=related_stocks,
    )


def unique_preserve_order(names: list[str]) -> list[str]:
    out: list[str] = []
    for name in names:
        if name and name not in out:
            out.append(name)
    return out


def build_entity_inputs(context: PrepContext) -> list[str]:
    candidate_names: list[str] = []
    for cluster in context.theme_clusters[:3]:
        candidate_names.extend(limited_members(cluster, 3))
    candidate_names.extend(context.ungrouped_names[:2])
    outputs: list[str] = []
    for name in unique_preserve_order(candidate_names):
        path = stock_entity_path(context.vault_market_intel, name)
        if path.exists():
            outputs.append(f"market-intel/entities/stocks/{name}.md")
    return outputs[:10]


def build_related_entity_links(context: PrepContext) -> list[str]:
    links: list[str] = []
    for item in build_entity_inputs(context):
        name = Path(item).stem
        links.append(stock_entity_link(name))
    return links


def render_entity_memory_sections(context: PrepContext, primary_names: list[str], expansion_names: list[str], residual_names: list[str]) -> list[str]:
    lines = [
        "## Entity memory check",
        "- 이 섹션에서 entity는 **독립 근거가 아니라 graph memory / expansion lookup** 역할이다.",
        "- 따라서 prep의 핵심 주장 자체는 prior recap / prior event proof / same-window technical layer에서 시작하고, entity는 반복 등장 맥락과 related stocks 확장 후보를 확인하는 보조 기억층으로만 쓴다.",
        "",
    ]
    grouped_candidates = [
        ("A. leader entity memory", primary_names[:4]),
        ("B. expansion entity memory", expansion_names[:4]),
        ("C. residual / re-check entity memory", residual_names[:3]),
    ]
    any_group = False
    aggregated_related: dict[str, list[str]] = {"leader": [], "expansion": [], "residual": []}
    bucket_map = {
        "A. leader entity memory": "leader",
        "B. expansion entity memory": "expansion",
        "C. residual / re-check entity memory": "residual",
    }
    for title, names in grouped_candidates:
        memories = [parse_entity_memory(context.vault_market_intel, name) for name in unique_preserve_order(names)]
        memories = [memory for memory in memories if memory is not None]
        if not memories:
            continue
        any_group = True
        lines.append(f"### {title}")
        bucket = bucket_map[title]
        for memory in memories:
            tags = ", ".join(f"`{tag}`" for tag in memory.theme_tags[:3]) if memory.theme_tags else "theme tag unavailable"
            latest_event = memory.event_history[0] if memory.event_history else "event history unavailable"
            related_links = ", ".join(stock_entity_link(name) for name in memory.related_stocks[:3]) if memory.related_stocks else "related stocks link unavailable"
            lines.append(f"- {stock_entity_link(memory.name)} — theme tags: {tags}")
            lines.append(f"  - latest entity memory: {latest_event}")
            lines.append(f"  - related stocks expansion check: {related_links}")
            lines.append(f"  - provenance rule: 이 entity 정보는 [[{context.recap_path.stem}]] / prior event proof / high-signal fact layer와 같이 읽을 때만 prep 판단 근거가 된다.")
            for related_name in memory.related_stocks[:4]:
                if related_name not in aggregated_related[bucket]:
                    aggregated_related[bucket].append(related_name)
        lines.append("")

    if not any_group:
        lines.append("- 현재 priority names와 직접 연결되는 stock entity page를 찾지 못했다. 이 경우 prep는 recap/event/high-signal만으로 작성하고 entity gap을 후속 보강한다.")
        return lines

    lines.extend([
        "## Related stocks expansion check",
        "- 아래 이름들은 priority entity page의 `Related Stocks`에서 끌어온 **확장 관찰 후보**다.",
        "- 메인 leader가 살아 있을 때만 2차 확산 후보로 점검하고, entity 링크만 보고 독립 진입 후보로 격상하지 않는다.",
    ])
    for label, key in [("leader-linked names", "leader"), ("expansion-linked names", "expansion"), ("residual / re-check linked names", "residual")]:
        related_names = aggregated_related[key][:6]
        rendered = ", ".join(stock_entity_link(name) for name in related_names) if related_names else "없음"
        lines.append(f"- {label}: {rendered}")
    return lines


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
    recent_recaps = collect_recent_validated_recaps(daily_dir, base_date, limit=5)
    return PrepContext(
        vault_market_intel=vault_market_intel,
        target_date=target_date,
        base_date=base_date,
        recap_path=recap_path,
        close_input_path=close_input_path,
        briefing_path=briefing_path if briefing_path.exists() else None,
        existing_path=existing_path,
        event_slugs=event_slugs,
        theme_clusters=theme_clusters,
        ungrouped_names=ungrouped_names,
        recent_recaps=recent_recaps,
    )


def build_supporting_notes(context: PrepContext) -> list[str]:
    notes = [context.close_input_path.stem]
    if context.briefing_path:
        notes.append(context.briefing_path.stem)
    notes.extend(row.path.stem for row in context.recent_recaps[:4])
    notes.extend(context.event_slugs[:5])
    deduped: list[str] = []
    for note in notes:
        if note not in deduped:
            deduped.append(note)
    return deduped


def render_follow_up_sections(context: PrepContext) -> list[str]:
    paired_review = review_note_link(context.target_date)
    return [
        "## Follow-up note",
        f"- 이 문서는 `{context.target_date:%Y-%m-%d}` 장전 대응을 위한 **ex-ante hypothesis artifact**다.",
        "- actual vs hypothesis 비교, 질문 수정, replay/review는 별도 review 문서에서 처리한다.",
        f"- paired review: {paired_review}",
        "",
        "## My review notes",
        "- thesis_push:",
        "- disagreement_or_risk:",
        "- missing_piece:",
        "- open_question:",
        "",
        "## Hermes review request",
        "- review_request_status: not_requested",
        "- requested_at_kst:",
        "- focus_question:",
        f"- paired_review_target: {paired_review}",
    ]


def build_review_stub_content(context: PrepContext) -> str:
    created_at = fmt_ts()
    source_links = [
        f'"[[market-intel/daily/{context.target_date:%Y-%m-%d}_next-session-prep|{context.target_date:%Y-%m-%d}_next-session-prep]]"',
        f'"[[market-intel/daily/{context.base_date:%Y-%m-%d}_top30_recap|{context.base_date:%Y-%m-%d}_top30_recap]]"',
        f'"[[market-intel/daily/{context.base_date:%Y-%m-%d}_evening-briefing-input|{context.base_date:%Y-%m-%d}_evening-briefing-input]]"',
    ]
    if context.briefing_path:
        source_links.append(f'"[[market-intel/daily/{context.base_date:%Y-%m-%d}_evening-briefing|{context.base_date:%Y-%m-%d}_evening-briefing]]"')
    related_events = [f'"{event_link(slug)}"' for slug in context.event_slugs[:5]]
    related_entities = [f'"{link}"' for link in build_related_entity_links(context)[:8]]
    lines = [
        "---",
        f"id: {review_note_slug(context.target_date)}",
        "note_type: predictive_replay",
        f"created_at: {created_at}",
        f"updated_at: {created_at}",
        f"event_date: {context.target_date:%Y-%m-%d}",
        f"review_date: {context.target_date:%Y-%m-%d}",
        "reviewer: 헤르메스(ㅎㅁ)",
        "region: KR",
        "session_relation: kr_preopen",
        "review_mode: prep_review",
        "review_request_status: not_requested",
        "entity_review_scope: prep_known_graph_only",
        f"source_prep: [[market-intel/daily/{context.target_date:%Y-%m-%d}_next-session-prep|{context.target_date:%Y-%m-%d}_next-session-prep]]",
        f"source_links: [{', '.join(source_links)}]",
        "user_opinion_captured: false",
        'focus_question: ""',
        'review_scope: ["prep thesis", "priority names", "invalidation logic", "entity graph boundary"]',
        f"related_events: [{', '.join(related_events)}]" if related_events else "related_events: []",
        f"related_entities: [{', '.join(related_entities)}]" if related_entities else "related_entities: []",
        'pattern_labels: ["prep_review", "entity_boundary_check"]',
        f'summary: "{context.target_date:%Y-%m-%d} prep에 대한 paired review workspace. prep anchor는 유지하고, review/replay/entity boundary 판단은 이 문서에서 분리한다."',
        "---",
        "",
        f"# {review_note_slug(context.target_date)}",
        "",
        "## Why this review exists",
        f"- 이 노트는 [[market-intel/daily/{context.target_date:%Y-%m-%d}_next-session-prep|{context.target_date:%Y-%m-%d}_next-session-prep]]에 붙는 paired review다.",
        "- 목적은 prep 본문을 hindsight로 오염시키지 않으면서, 사용자 의견 / Hermes 검토 / 이후 replay를 분리 저장하는 것이다.",
        "",
        "## Review request snapshot",
        "- requested_at_kst:",
        "- requested_by: user",
        "- review_request_status: not_requested",
        "- focus_question:",
        "- review_scope:",
        "  - prep thesis",
        "  - carry-over themes",
        "  - priority names / sectors",
        "  - invalidation conditions",
        "  - entity graph boundary",
        "",
        "## User opinion snapshot",
        "> prep note의 `My review notes`를 그대로 옮기거나 요약.",
        "",
        "- thesis_push:",
        "- disagreement_or_risk:",
        "- missing_piece:",
        "- open_question:",
        "",
        "## What was knowable at review time?",
        "- 이 review note는 `prep_review` 용도다.",
        "- pre-open 검토 기준으로는 same-session outcome을 넣지 않는다.",
        "- post-close replay를 이어 붙일 경우 아래 `Optional post-close replay extension`부터 시점을 분리한다.",
        "",
        "## Entity graph usage boundary",
        "- prep에서 entity는 **proof lookup이 아니라 memory lookup**이다.",
        "- pre-open review에서는 prep cutoff 이전에 이미 존재했고, prior recap / prior event proof / same-window high-signal로 역추적 가능한 entity 정보만 검토 근거로 쓴다.",
        "- later-enriched entity 문구나 post-close에 추가된 link는 hindsight 레이어로 분리 표기한다.",
        "",
        "## Hermes review verdict",
        "### 1. Agree",
        "- ",
        "",
        "### 2. Tighten / revise",
        "- ",
        "",
        "### 3. Missing checks",
        "- ",
        "",
        "### 4. Overreach / unsupported claims",
        "- ",
        "",
        "## Revised operating view",
        "### Base case",
        "- ",
        "",
        "### Alternate case",
        "- ",
        "",
        "### What would change my mind",
        "- ",
        "",
        "## Suggested edits back to prep",
        "- prep 본문을 직접 오염시키지 않는 범위에서, 남겨도 되는 수정만 적는다.",
        "- 예:",
        "  - one-line prep 문장 정교화",
        "  - priority bucket 재배치",
        "  - invalidation 조건 문구 강화",
        "  - supporting link 추가",
        "",
        "## Optional post-close replay extension",
        "### Actual outcome",
        "- ",
        "",
        "### What was right",
        "- ",
        "",
        "### What was missed",
        "- ",
        "",
        "### Rule / workflow update",
        "- ",
        "",
        "## Links",
        f"- prep note: [[market-intel/daily/{context.target_date:%Y-%m-%d}_next-session-prep|{context.target_date:%Y-%m-%d}_next-session-prep]]",
        f"- actual recap (fill after close when created): `{context.target_date:%Y-%m-%d}_top30_recap`",
        f"- prior recap anchor: [[market-intel/daily/{context.base_date:%Y-%m-%d}_top30_recap|{context.base_date:%Y-%m-%d}_top30_recap]]",
        f"- close input: [[market-intel/daily/{context.base_date:%Y-%m-%d}_evening-briefing-input|{context.base_date:%Y-%m-%d}_evening-briefing-input]]",
        "- workflow template: [[market-intel/workflows/next-session-prep-paired-review-template|next-session-prep-paired-review-template]]",
    ]
    return "\n".join(lines).rstrip() + "\n"


def render_frontmatter(context: PrepContext) -> str:
    supporting_notes = ", ".join(f'"{item}"' for item in build_supporting_notes(context))
    entity_inputs = build_entity_inputs(context)
    lines = [
        "---",
        f"id: next-session-prep-{context.target_date:%Y-%m-%d}",
        "note_type: next_session_prep",
        f"created_at: {fmt_ts()}",
        f"updated_at: {fmt_ts()}",
        f"session_date: {context.target_date:%Y-%m-%d}",
        f"source_note: {context.recap_path.stem}",
        f"supporting_notes: [{supporting_notes}]",
        "entity_inputs:",
    ]
    if entity_inputs:
        lines.extend(f"  - {item}" for item in entity_inputs)
    else:
        lines.append("  - []")
    lines.extend([
        "reviewer: 헤르메스(ㅎㅁ)",
        "generation_mode: auto_prior_close_scaffold",
        "source_scope: prior_close_only",
        "same_day_intraday_excluded: true",
        "---",
    ])
    return "\n".join(lines)


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
    recurrence = theme_recurrence_count(context.recent_recaps)

    lines: list[str] = [
        render_frontmatter(context),
        "",
        f"# {context.target_date:%Y-%m-%d} Next Session Prep",
        "",
        "## Why this note exists",
        f"- 이 문서는 **{context.target_date:%Y-%m-%d} {weekday_label(context.target_date)} 장전 대응 문서**다.",
        f"- 기준 close는 `{context.base_date:%Y-%m-%d}`이고, 따라서 이 노트 안에서 `오늘`은 **{context.target_date:%Y-%m-%d} KST pre-open**을 뜻한다.",
        "- 이 문서는 `validated recap + close input + prior event proof + stock entity memory + 저장된 최근 며칠 graph`를 종합한 prior-close-only scaffold이며, same-day intraday/close 정보는 포함하지 않는다.",
        f"- 장마감 정리는 {note_link(context.recap_path.stem)}에, 장전 실행 포인트는 이 문서에 분리한다.",
        "",
        "## Recent 5 trading days synthesized context",
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
        "## Base context available before the open",
        f"- {context.base_date:%m/%d} validated TOP30는 **{join_themes_for_sentence(top_clusters)}** 축이 먼저 보이는 날이었다.",
    ])
    if top_clusters:
        first = top_clusters[0]
        lines.append(f"- 최우선 해석 축은 `{first.name}` continuation 여부이고, leader는 {', '.join(limited_members(first, 4))} 쪽이다.")
    if len(top_clusters) >= 2:
        second = top_clusters[1]
        lines.append(f"- 동시에 `{second.name}`가 보조/공동 주도축으로 붙는지 확인해야 하며, 대표 종목은 {', '.join(limited_members(second, 3))}다.")
    lines.append("- 전날 하루만 보는 게 아니라, 최근 5거래일 정리 데이터에서 `집중 -> 분산 -> 재선별` 흐름이 어떻게 이어졌는지 위 기준선 위에서 판단한다.")

    lines.extend(["", *render_entity_memory_sections(context, primary_names, expansion_names, residual_names), "", "## 신고가 / high-signal 팩트층"])
    if has_same_window_high_signal(context.recent_recaps):
        lines.append("- 최근 5거래일 구간 안에 로컬 high-signal snapshot이 존재한다. carry-over 후보와의 overlap은 별도 high-signal 자동 연결 단계에서 끌어와야 한다.")
    else:
        lines.append("- 현재 로컬 기준 최근 5거래일 구간에는 exact-date high-signal snapshot이 없다.")
    lines.extend([
        "- 따라서 이번 prep은 특정 종목을 `신고가/high-signal confirmed`로 단정하지 않고, **validated recap 기반 군집 연속성 + 최근 5거래일 반복 등장 + leader breadth**를 우선 근거로 쓴다.",
        "- high-signal overlap이 있는 이름은 carry-over theme 선정 근거와 함께 읽어야 한다.",
    ])

    lines.extend(["", "## Carry-over themes 선정 근거"])
    if primary:
        lines.append("### 1순위 primary check")
        for cluster in primary:
            lines.append(f"- {cluster.name}")
            lines.extend(bullet_members(limited_members(cluster, 4)))
            lines.append(f"  - **근거**: {context.base_date:%m/%d} validated recap에서 {cluster.count}개로 상위 군집이었다.")
            if recurrence.get(cluster.name, 0) >= 2:
                lines.append(f"  - **근거**: 최근 5거래일 중 {recurrence[cluster.name]}회 반복 등장해 carry-over 지속성 후보다.")
    if expansion:
        lines.append("")
        lines.append("### 2순위 expansion check")
        for cluster in expansion:
            lines.append(f"- {cluster.name}")
            lines.extend(bullet_members(limited_members(cluster, 3)))
            lines.append("  - **근거**: 당일 메인 leader는 아니지만 후속 확산이 붙으면 해석 강도가 커지는 보조 축이다.")
            if recurrence.get(cluster.name, 0) >= 2:
                lines.append(f"  - **근거**: 최근 5거래일 중 {recurrence[cluster.name]}회 등장해 재등장/재점화 가능성이 있다.")
    if residual or context.ungrouped_names:
        lines.append("")
        lines.append("### 3순위 residual / rotation check")
        for cluster in residual:
            lines.append(f"- {cluster.name}")
            lines.extend(bullet_members(limited_members(cluster, 2)))
            lines.append("  - **근거**: 메인 시나리오가 약해질 때 대체 순환으로 붙는지 보는 residual bucket이다.")
        if context.ungrouped_names:
            lines.append("- 개별주/혼합")
            lines.extend(bullet_members(context.ungrouped_names[:5]))
            lines.append("  - **근거**: 군집보다 개별 수급 반응으로 남은 이름들이다.")

    first_theme = top_clusters[0].name if top_clusters else "주도 테마"
    second_theme = top_clusters[1].name if len(top_clusters) >= 2 else "보조 축"
    third_theme = top_clusters[2].name if len(top_clusters) >= 3 else "후속 확산 테마"
    lines.extend([
        "",
        "## Priority names / sectors 선정 근거",
        "- `A. leader 확인`은 당일 breadth 상위 군집의 중심 이름들이다.",
        "- `B. 후속 확산 확인`은 cluster로 같이 움직이면 해석이 강해지는 이름들이다.",
        "- `C. 재집중 / 반전 확인`은 메인 시나리오 실패 시 대체 순환 후보를 보는 observation bucket이다.",
        "- 즉 이 리스트는 매수 추천이 아니라, **장초 observation priority** 순서다.",
        "",
        "## What to check at the open",
        f"1. **{first_theme}가 장초부터 거래대금 leader로 유지되는지 확인**",
        f"2. **{second_theme}가 {first_theme}와 함께 공동 주도축인지, 아니면 일부 종목 강세에 그치는지 확인**",
        f"3. **{third_theme}가 후속 확산을 만드는지, 아니면 headline 반응 후 약해지는지 확인**",
        "4. **전일 상위 급등주가 gap-only인지, 시초 이후 거래대금까지 유지하는지 확인**",
        "5. **시장이 breadth가 붙는 다축 확산인지, 아니면 소수 leader 집중 구조인지 구분**",
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
        "- 최근 5거래일 흐름상 분산 재편이었는데 장초부터 소수 종목만 남으면 단기 순환매/소화 구간 가능성을 높인다.",
        "",
        "## One-line prep",
        f"**{context.target_date:%Y-%m-%d} 장전의 기본 시나리오는 {first_theme} 중심 continuation 여부를 먼저 확인하되, 최근 5거래일의 집중→분산→재선별 흐름 위에서 {second_theme}/{third_theme}가 새 리더로 굳는지도 함께 판단하는 것이다.**",
        "",
        "## Guardrail",
        "- 이 문서는 prior-close-only scaffold다.",
        "- 실제 결과 비교와 회고는 별도 replay/review 문서로 넘긴다.",
        "",
        *render_follow_up_sections(context),
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
    review_path = review_note_path(vault_market_intel, target_date)
    review_path.parent.mkdir(parents=True, exist_ok=True)
    if args.overwrite or not review_path.exists():
        review_path.write_text(build_review_stub_content(context), encoding="utf-8")
        print(f"WROTE_REVIEW {review_path}")
    else:
        print(f"SKIP_REVIEW existing {review_path}")
    print(f"WROTE {context.existing_path}")
    print(f"TARGET_DATE {target_date:%Y-%m-%d}")
    print(f"BASE_DATE {context.base_date:%Y-%m-%d}")
    print(f"SOURCE_RECAP {context.recap_path.name}")
    print(f"SOURCE_INPUT {context.close_input_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
