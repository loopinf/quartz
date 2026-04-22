#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from market_intel_visuals import build_runtime_now_html

KST = ZoneInfo("Asia/Seoul")
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_(.+)\.md$")
WEEKDAY_KO = ["월", "화", "수", "목", "금", "토", "일"]


@dataclass(frozen=True)
class NoteRef:
    date: str
    slug: str
    title: str
    path: Path


@dataclass(frozen=True)
class DocStatus:
    code: str
    label: str
    expected_slug: str
    note: NoteRef | None
    latest_fallback: NoteRef | None
    summary: str


@dataclass(frozen=True)
class ExtraStatus:
    code: str
    label: str
    target_text: str
    href: str | None
    link_text: str | None
    summary: str


@dataclass(frozen=True)
class CurrentState:
    now: datetime
    today_date: str
    today_label: str
    phase: str
    checklist_title: str
    required_prep_date: str
    required_recap_date: str
    required_close_input_date: str
    required_briefing_output_date: str
    same_day_archive_date: str
    same_day_archive_path: Path
    required_archive_path: Path
    required_prep: NoteRef | None
    required_recap: NoteRef | None
    required_close_input: NoteRef | None
    required_briefing_output: NoteRef | None
    latest_prep: NoteRef | None
    latest_validated_recap: NoteRef | None
    latest_close_input: NoteRef | None
    latest_briefing_output: NoteRef | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh current-date Market Intel entrypoint pages and sidebar constants.")
    parser.add_argument("--vault-path", default=str(Path.home() / "Documents" / "Obsidian Vault"))
    parser.add_argument("--site-root", default=str(Path.home() / "market-intel-site"))
    parser.add_argument("--jmkr-root", default=str(Path.home() / "repos" / "jmkr_kj"))
    return parser.parse_args()


def market_phase(now: datetime) -> str:
    hhmm = now.hour * 100 + now.minute
    if hhmm < 900:
        return "장전"
    if hhmm < 1530:
        return "장중"
    return "장후"


def current_label(now: datetime) -> str:
    weekday = WEEKDAY_KO[now.weekday()]
    return f"{now:%Y-%m-%d} KST, {weekday}요일 {market_phase(now)}"


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    frontmatter = {}
    for raw_line in parts[0].splitlines()[1:]:
        line = raw_line.strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"')
    return frontmatter


def parse_json_payload(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def archive_passes_validation(payload: dict | None) -> tuple[bool, str]:
    if not isinstance(payload, dict):
        return False, "archive JSON을 읽지 못했다."
    message_type = payload.get("messageType")
    parsing_info = payload.get("parsing_info") or {}
    original_text = payload.get("originalText") or ""
    numbered_lines = len(re.findall(r"(?m)^\s*\d+\.\s", original_text))
    has_top30_phrase = any(token in original_text for token in ("상승률 TOP30", "상승률TOP30", "상승률 TOP 30"))
    if message_type != "market_close":
        return False, f"messageType={message_type!r}"
    if parsing_info.get("is_empty") is not False:
        return False, "parsing_info.is_empty != false"
    if not has_top30_phrase:
        return False, "TOP30 문구가 없다"
    if numbered_lines < 20:
        return False, f"번호 라인이 부족함 ({numbered_lines})"
    return True, f"market_close + is_empty=false + TOP30 문구 + 번호 라인 {numbered_lines}개"


def format_kst_timestamp(raw: str | None) -> str:
    if not raw:
        return "unknown"
    try:
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(KST)
        return dt.strftime("%Y-%m-%d %H:%M KST")
    except Exception:
        return raw


def parser_health_snapshot(jmkr_root: Path, state: CurrentState | None = None) -> tuple[str, str]:
    try:
        result = subprocess.run(
            ["node", "services/telegram-parser-node/index.js", "health"],
            cwd=jmkr_root,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    except Exception as exc:
        return "UNKNOWN", f"parser health 실행 실패: {exc}"

    merged = (result.stdout or "") + "\n" + (result.stderr or "")
    start = merged.find("{")
    end = merged.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return "UNKNOWN", "parser health JSON 응답을 읽지 못했다."
    try:
        payload = json.loads(merged[start : end + 1])
    except Exception:
        return "UNKNOWN", "parser health JSON 파싱 실패"

    status = payload.get("status")
    last_update = payload.get("last_update")
    last_update_label = format_kst_timestamp(last_update)
    if status != "healthy":
        return "WARNING", f"parser health={status}, last_update={last_update_label}"

    if state is None:
        return "READY", f"parser health=healthy, last_update={last_update_label}"

    try:
        last_update_date = datetime.fromisoformat(last_update.replace("Z", "+00:00")).astimezone(KST).strftime("%Y-%m-%d")
    except Exception:
        return "WARNING", f"parser health=healthy, 하지만 last_update 파싱 실패 ({last_update_label})"

    if state.phase == "장후":
        if last_update_date >= state.today_date:
            return "READY", f"parser health=healthy, today 기준 last_update={last_update_label}"
        return "WARNING", f"parser health=healthy, 하지만 today 기준 last_update가 stale ({last_update_label})"

    if last_update_date >= state.required_recap_date:
        return "READY", f"parser health=healthy, 직전 장 기준 last_update={last_update_label}"
    return "WARNING", f"parser health=healthy, 하지만 직전 장 기준 last_update가 stale ({last_update_label})"


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


def iter_matching_notes(daily_dir: Path, suffix: str, *, require_validated: bool = False) -> list[NoteRef]:
    matches: list[NoteRef] = []
    for path in daily_dir.glob(f"*_{suffix}.md"):
        match = DATE_RE.match(path.name)
        if not match:
            continue
        date_part, suffix_part = match.groups()
        if suffix_part != suffix:
            continue
        if require_validated:
            frontmatter = parse_frontmatter(path)
            if frontmatter.get("validation_status") != "validated":
                continue
        matches.append(NoteRef(date=date_part, slug=path.stem, title=path.stem, path=path))
    return sorted(matches, key=lambda item: item.date)


def find_latest_note(
    daily_dir: Path,
    suffix: str,
    *,
    require_validated: bool = False,
    exact_date: str | None = None,
    on_or_before: str | None = None,
) -> NoteRef | None:
    matches = iter_matching_notes(daily_dir, suffix, require_validated=require_validated)
    filtered: list[NoteRef] = []
    for item in matches:
        if exact_date is not None and item.date != exact_date:
            continue
        if on_or_before is not None and item.date > on_or_before:
            continue
        filtered.append(item)
    return max(filtered, key=lambda item: item.date, default=None)


def build_state(vault_market_intel: Path, jmkr_root: Path) -> CurrentState:
    now = datetime.now(KST)
    today = now.date()
    today_date = today.strftime("%Y-%m-%d")
    phase = market_phase(now)
    daily_dir = vault_market_intel / "daily"

    if phase == "장후":
        required_prep_date = next_trading_day(today).strftime("%Y-%m-%d")
        required_recap_date = today_date
        required_close_input_date = today_date
        required_briefing_output_date = today_date
        checklist_title = "다음 세션 준비 상태"
    else:
        prior = previous_trading_day(today)
        required_prep_date = today_date
        required_recap_date = prior.strftime("%Y-%m-%d")
        required_close_input_date = prior.strftime("%Y-%m-%d")
        required_briefing_output_date = prior.strftime("%Y-%m-%d")
        checklist_title = "오늘 장전 준비 상태"

    required_prep = find_latest_note(daily_dir, "next-session-prep", exact_date=required_prep_date)
    required_recap = find_latest_note(
        daily_dir,
        "top30_recap",
        require_validated=True,
        exact_date=required_recap_date,
    )
    required_close_input = find_latest_note(
        daily_dir,
        "evening-briefing-input",
        exact_date=required_close_input_date,
    )
    required_briefing_output = find_latest_note(
        daily_dir,
        "evening-briefing",
        exact_date=required_briefing_output_date,
    )

    latest_prep = find_latest_note(daily_dir, "next-session-prep")
    latest_validated_recap = find_latest_note(
        daily_dir,
        "top30_recap",
        require_validated=True,
        on_or_before=required_recap_date,
    )
    latest_close_input = find_latest_note(
        daily_dir,
        "evening-briefing-input",
        on_or_before=required_close_input_date,
    )
    latest_briefing_output = find_latest_note(
        daily_dir,
        "evening-briefing",
        on_or_before=required_briefing_output_date,
    )
    same_day_archive_path = jmkr_root / "data" / "daily" / "archive" / f"{today_date}.json"
    required_archive_path = jmkr_root / "data" / "daily" / "archive" / f"{required_recap_date}.json"

    return CurrentState(
        now=now,
        today_date=today_date,
        today_label=current_label(now),
        phase=phase,
        checklist_title=checklist_title,
        required_prep_date=required_prep_date,
        required_recap_date=required_recap_date,
        required_close_input_date=required_close_input_date,
        required_briefing_output_date=required_briefing_output_date,
        same_day_archive_date=today_date,
        same_day_archive_path=same_day_archive_path,
        required_archive_path=required_archive_path,
        required_prep=required_prep,
        required_recap=required_recap,
        required_close_input=required_close_input,
        required_briefing_output=required_briefing_output,
        latest_prep=latest_prep,
        latest_validated_recap=latest_validated_recap,
        latest_close_input=latest_close_input,
        latest_briefing_output=latest_briefing_output,
    )


def note_link(note: NoteRef | None) -> str:
    return f"/market-intel/daily/{note.slug}" if note else "/market-intel/daily/"


def current_label_span(state: CurrentState) -> str:
    return (
        f'<span data-mi-current-label="1" data-mi-current-date="{state.today_date}" '
        f'data-mi-current-phase="{state.phase}">{state.today_label}</span>'
    )


def required_doc_statuses(state: CurrentState) -> list[DocStatus]:
    statuses: list[DocStatus] = []

    if state.required_prep:
        statuses.append(
            DocStatus(
                code="READY",
                label="오늘 세션 prep",
                expected_slug=f"{state.required_prep_date}_next-session-prep",
                note=state.required_prep,
                latest_fallback=state.latest_prep if state.latest_prep != state.required_prep else None,
                summary=f"오늘 세션용 prep가 {state.required_prep.slug}로 준비되어 있다.",
            )
        )
    else:
        statuses.append(
            DocStatus(
                code="MISSING",
                label="오늘 세션 prep",
                expected_slug=f"{state.required_prep_date}_next-session-prep",
                note=None,
                latest_fallback=state.latest_prep,
                summary=(
                    f"필요 문서는 {state.required_prep_date}_next-session-prep인데 아직 없다."
                    if state.latest_prep
                    else f"필요 문서는 {state.required_prep_date}_next-session-prep인데 fallback으로 쓸 prep도 없다."
                ),
            )
        )

    if state.required_recap:
        statuses.append(
            DocStatus(
                code="READY",
                label="직전 장 validated recap",
                expected_slug=f"{state.required_recap_date}_top30_recap",
                note=state.required_recap,
                latest_fallback=state.latest_validated_recap if state.latest_validated_recap != state.required_recap else None,
                summary=f"직전 장 기준 validated recap가 {state.required_recap.slug}로 준비되어 있다.",
            )
        )
    else:
        statuses.append(
            DocStatus(
                code="MISSING",
                label="직전 장 validated recap",
                expected_slug=f"{state.required_recap_date}_top30_recap",
                note=None,
                latest_fallback=state.latest_validated_recap,
                summary=(
                    f"필요 문서는 {state.required_recap_date}_top30_recap인데 exact-date validated recap가 없다."
                    if state.latest_validated_recap
                    else f"필요 문서는 {state.required_recap_date}_top30_recap인데 validated recap 자체를 찾지 못했다."
                ),
            )
        )

    if state.required_close_input:
        statuses.append(
            DocStatus(
                code="READY",
                label="직전 장 close input",
                expected_slug=f"{state.required_close_input_date}_evening-briefing-input",
                note=state.required_close_input,
                latest_fallback=state.latest_close_input if state.latest_close_input != state.required_close_input else None,
                summary=f"직전 장 close input이 {state.required_close_input.slug}로 준비되어 있다.",
            )
        )
    else:
        statuses.append(
            DocStatus(
                code="MISSING",
                label="직전 장 close input",
                expected_slug=f"{state.required_close_input_date}_evening-briefing-input",
                note=None,
                latest_fallback=state.latest_close_input,
                summary=(
                    f"필요 문서는 {state.required_close_input_date}_evening-briefing-input인데 exact-date close input이 없다."
                    if state.latest_close_input
                    else f"필요 문서는 {state.required_close_input_date}_evening-briefing-input인데 close input 자체를 찾지 못했다."
                ),
            )
        )

    return statuses


def readiness_summary(state: CurrentState) -> tuple[str, int, int]:
    statuses = required_doc_statuses(state)
    ready_count = sum(1 for item in statuses if item.code == "READY")
    total = len(statuses)
    if ready_count == total:
        return "완료", ready_count, total
    if ready_count == 0:
        return "미준비", ready_count, total
    return "부분준비", ready_count, total


def render_status_lines(state: CurrentState) -> str:
    lines: list[str] = []
    for item in required_doc_statuses(state):
        if item.note:
            lines.append(f"- `{item.code}` {item.label}: [{item.note.slug}]({note_link(item.note)})")
        else:
            lines.append(f"- `{item.code}` {item.label}: 필요 문서 `{item.expected_slug}`")
        lines.append(f"  - {item.summary}")
        if item.latest_fallback:
            lines.append(f"  - 최신 fallback: [{item.latest_fallback.slug}]({note_link(item.latest_fallback)})")
    return "\n".join(lines)


def render_latest_lines(state: CurrentState) -> str:
    lines = [
        f"- 최신 prep: [{state.latest_prep.slug}]({note_link(state.latest_prep)})" if state.latest_prep else "- 최신 prep: 없음",
        (
            f"- 최신 validated recap: [{state.latest_validated_recap.slug}]({note_link(state.latest_validated_recap)})"
            if state.latest_validated_recap
            else "- 최신 validated recap: 없음"
        ),
        (
            f"- 최신 close input: [{state.latest_close_input.slug}]({note_link(state.latest_close_input)})"
            if state.latest_close_input
            else "- 최신 close input: 없음"
        ),
        (
            f"- 최신 evening briefing output: [{state.latest_briefing_output.slug}]({note_link(state.latest_briefing_output)})"
            if state.latest_briefing_output
            else "- 최신 evening briefing output: 없음"
        ),
        (
            f"- same-day archive path: `{state.same_day_archive_path}`"
            + (" (exists)" if state.same_day_archive_path.exists() else " (missing yet)")
        ),
    ]
    return "\n".join(lines)


def render_extra_status_lines(state: CurrentState) -> str:
    lines: list[str] = []

    if state.required_briefing_output:
        lines.append(
            f"- `READY` final evening briefing output: [{state.required_briefing_output.slug}]({note_link(state.required_briefing_output)})"
        )
        lines.append(
            f"  - 현재 세션 기준 briefing output이 {state.required_briefing_output.slug}로 존재한다."
        )
    else:
        lines.append(
            f"- `MISSING` final evening briefing output: 필요 문서 `{state.required_briefing_output_date}_evening-briefing`"
        )
        if state.latest_briefing_output:
            lines.append(
                f"  - 최신 fallback output: [{state.latest_briefing_output.slug}]({note_link(state.latest_briefing_output)})"
            )
        else:
            lines.append("  - 아직 reusable evening briefing output 문서를 찾지 못했다.")

    required_archive_payload = parse_json_payload(state.required_archive_path) if state.required_archive_path.exists() else None
    required_archive_valid, required_archive_detail = archive_passes_validation(required_archive_payload)
    if state.required_archive_path.exists() and required_archive_valid:
        lines.append(f"- `READY` required close archive: `{state.required_archive_path}`")
        lines.append(f"  - 현재 세션에 필요한 close archive가 존재하고 validation 통과: {required_archive_detail}")
    elif state.required_archive_path.exists():
        lines.append(f"- `WARNING` required close archive: `{state.required_archive_path}`")
        lines.append(f"  - 파일은 있지만 validation 실패: {required_archive_detail}")
    else:
        lines.append(f"- `MISSING` required close archive: `{state.required_archive_path}`")
        lines.append("  - 현재 세션에 필요한 close archive 파일 자체가 없다.")

    same_day_payload = parse_json_payload(state.same_day_archive_path) if state.same_day_archive_path.exists() else None
    same_day_valid, same_day_detail = archive_passes_validation(same_day_payload)
    if state.same_day_archive_path.exists() and same_day_valid:
        lines.append(f"- `READY` same-day source archive: `{state.same_day_archive_path}`")
        lines.append(f"  - today archive가 존재하고 validation 통과: {same_day_detail}")
    elif state.same_day_archive_path.exists():
        lines.append(f"- `WARNING` same-day source archive: `{state.same_day_archive_path}`")
        lines.append(f"  - today archive 파일은 있지만 validation 실패: {same_day_detail}")
    elif state.phase == "장후":
        lines.append(f"- `MISSING` same-day source archive: `{state.same_day_archive_path}`")
        lines.append("  - 장후 기준으로는 당일 archive가 있어야 하는데 아직 없다.")
    else:
        lines.append(f"- `WAITING` same-day source archive: `{state.same_day_archive_path}`")
        lines.append("  - 장전/장중에는 당일 archive가 아직 없어도 정상일 수 있다. close 이후 READY/MISSING으로 봐야 한다.")

    parser_code, parser_summary = parser_health_snapshot(state.required_archive_path.parents[3], state)
    lines.append("- `" + parser_code + "` telegram parser health")
    lines.append(f"  - {parser_summary}")

    return "\n".join(lines)


def render_recent_list(title: str, notes: list[NoteRef]) -> str:
    lines = [f"### {title}"]
    if not notes:
        lines.append("- 없음")
    else:
        for note in notes:
            lines.append(f"- [{note.slug}]({note_link(note)})")
    return "\n".join(lines)


def latest_notes_for_list(daily_dir: Path, suffix: str, *, require_validated: bool = False, limit: int = 3) -> list[NoteRef]:
    notes = iter_matching_notes(daily_dir, suffix, require_validated=require_validated)
    return sorted(notes, key=lambda item: item.date, reverse=True)[:limit]


def next_action_lines(state: CurrentState) -> str:
    lines: list[str] = ["1. [진행상황판에서 exact-date readiness 확인](/market-intel/current-readiness-board)"]
    if state.required_prep:
        lines.append(f"2. [오늘 세션 prep 열기]({note_link(state.required_prep)})")
    elif state.latest_prep:
        lines.append(f"2. [fallback prep 확인]({note_link(state.latest_prep)})")
    else:
        lines.append("2. [/market-intel/daily/ 에서 오늘 세션 prep 생성 필요](/market-intel/daily/)")

    idx = len(lines) + 1
    if state.required_recap:
        lines.append(f"{idx}. [직전 장 validated recap]({note_link(state.required_recap)})")
    elif state.latest_validated_recap:
        lines.append(f"{idx}. [fallback validated recap]({note_link(state.latest_validated_recap)})")
    idx = len(lines) + 1
    if state.required_close_input:
        lines.append(f"{idx}. [직전 장 close input]({note_link(state.required_close_input)})")
    elif state.latest_close_input:
        lines.append(f"{idx}. [fallback close input]({note_link(state.latest_close_input)})")
    idx = len(lines) + 1
    lines.append(f"{idx}. [prediction workspace](/market-intel/research/prediction-workspace)")
    return "\n".join(lines)


def terminology_block() -> str:
    return """- `필수 문서`: 현재 세션 시점에 exact-date로 준비돼 있어야 하는 문서
- `최신 fallback`: exact-date 문서가 없을 때 참고 가능한 가장 최근 usable 문서
- `직전 장`: 단순히 최근에 작업한 문서가 아니라, 현재 세션 바로 이전 거래일 기준
- `준비도`: prep / validated recap / close input 3개 중 몇 개가 exact-date 기준으로 준비됐는지"""


def root_markdown(state: CurrentState) -> str:
    runtime_now_html = build_runtime_now_html(state.today_label)
    readiness_text, ready_count, total_count = readiness_summary(state)
    return f"""---
title: Market Intel Start
summary: 8081 루트 시작점. 현재 세션에 필요한 문서가 exact-date 기준으로 준비됐는지 자동으로 먼저 보여준다.
---

# Market Intel Start

## 지금 준비 상태 ({current_label_span(state)})
- 실시간 KST 기준: {runtime_now_html}
- 현재 세션: `{state.today_date}` / `{state.phase}`
- {state.checklist_title}: `{readiness_text}` = `{ready_count} / {total_count}`
- [진행상황판 바로 열기](/market-intel/current-readiness-board)
- 자동 확인 기준: `오늘/다음 세션 prep`, `직전 장 validated recap`, `직전 장 close input`이 exact-date로 있는지 확인

{render_status_lines(state)}

## 지금 바로 할 일
{next_action_lines(state)}

## 최신 usable 문서
{render_latest_lines(state)}

## 용어 정리
{terminology_block()}

## 섹션 바로가기
- [Market Intel home](/market-intel/)
- [진행상황판](/market-intel/current-readiness-board)
- [daily workspace](/market-intel/daily/)
- [prediction workspace](/market-intel/research/prediction-workspace)
- [최근 변경 로그](/market-intel/MARKET_INTEL_RECENT_CHANGES)
- [큰그림](/market-intel/market-intel-progress-big-picture)
"""


def market_home_markdown(state: CurrentState) -> str:
    runtime_now_html = build_runtime_now_html(state.today_label)
    readiness_text, ready_count, total_count = readiness_summary(state)
    return f"""---
title: Market Intel Home
summary: 현재 세션 필수 문서가 자동으로 준비됐는지 먼저 확인하고, fallback과 다음 액션을 바로 여는 운영 홈.
---

# Market Intel Home

## 오늘 준비 상태 ({current_label_span(state)})
- 실시간 KST 기준: {runtime_now_html}
- 현재 세션: `{state.today_date}` / `{state.phase}`
- {state.checklist_title}: `{readiness_text}` = `{ready_count} / {total_count}`
- [진행상황판](/market-intel/current-readiness-board)
- 최근 변경 로그: [MARKET_INTEL_RECENT_CHANGES](/market-intel/MARKET_INTEL_RECENT_CHANGES)

{render_status_lines(state)}

## 오늘 바로 할 일
{next_action_lines(state)}

## 최신 usable 문서
{render_latest_lines(state)}

## 왜 이렇게 보나
- 수동으로 "어제 문서 열어보자"가 아니라, **현재 시점에 필요한 exact-date 문서가 있는지 자동으로 확인**해야 한다.
- exact-date 문서가 없으면 fallback은 보여주되, 준비 완료로 취급하지 않는다.
- `직전`은 직전 작업 문서가 아니라 **현재 세션 바로 직전 거래일 기준**이다.

## 용어 정리
{terminology_block()}

## 큰그림 / 작업공간
- [진행상황판](/market-intel/current-readiness-board)
- [daily workspace](/market-intel/daily/)
- [prediction workspace](/market-intel/research/prediction-workspace)
- [portfolio pilot review dashboard](/market-intel/research/portfolio-pilot-review-dashboard)
- [predictive replay and review system](/market-intel/workflows/predictive-replay-and-review-system)
- [market-intel progress big picture](/market-intel/market-intel-progress-big-picture)
- [SOT — market-intel full pipeline](/market-intel/architecture/sot-market-intel-full-pipeline)
"""


def daily_index_markdown(state: CurrentState, daily_dir: Path) -> str:
    runtime_now_html = build_runtime_now_html(state.today_label)
    readiness_text, ready_count, total_count = readiness_summary(state)
    recent_prep = latest_notes_for_list(daily_dir, "next-session-prep", limit=4)
    recent_recap = latest_notes_for_list(daily_dir, "top30_recap", require_validated=True, limit=4)
    recent_close = latest_notes_for_list(daily_dir, "evening-briefing-input", limit=4)
    return f"""---
title: daily workspace
summary: 현재 세션 필수 daily 문서가 exact-date 기준으로 준비됐는지 한 번에 확인하는 허브.
---

# Daily Workspace

## {state.checklist_title} ({current_label_span(state)})
- 실시간 KST 기준: {runtime_now_html}
- 준비도: `{readiness_text}` = `{ready_count} / {total_count}`
- [진행상황판](/market-intel/current-readiness-board)
- 자동 확인 순서: `prep → validated recap → close input`

{render_status_lines(state)}

## 오늘 바로 열 것
{next_action_lines(state)}

## 최근 usable 기록
{render_recent_list('Session prep', recent_prep)}

{render_recent_list('Validated recap', recent_recap)}

{render_recent_list('Close input', recent_close)}

## 용어 정리
{terminology_block()}
"""


def prediction_workspace_markdown(state: CurrentState) -> str:
    runtime_now_html = build_runtime_now_html(state.today_label)
    prep_link = note_link(state.required_prep or state.latest_prep)
    prep_label = (state.required_prep or state.latest_prep).slug if (state.required_prep or state.latest_prep) else "prep 없음"
    recap_link = note_link(state.required_recap or state.latest_validated_recap)
    recap_label = (state.required_recap or state.latest_validated_recap).slug if (state.required_recap or state.latest_validated_recap) else "없음"
    close_link = note_link(state.required_close_input or state.latest_close_input)
    close_label = (state.required_close_input or state.latest_close_input).slug if (state.required_close_input or state.latest_close_input) else "없음"
    return f"""---
title: prediction workspace
summary: 예측 후보 검토 전에 현재 세션 준비 상태를 먼저 확인하는 prediction 허브.
---

# Prediction Workspace

## 오늘 바로 할 일 ({current_label_span(state)})
- 실시간 KST 기준: {runtime_now_html}
- 먼저 [진행상황판](/market-intel/current-readiness-board)에서 exact-date readiness 확인
1. [{prep_label}]({prep_link})
2. [portfolio pilot review dashboard](/market-intel/research/portfolio-pilot-review-dashboard)
3. [portfolio pilot batch — additional samples](/market-intel/research/portfolio-pilot-batch-additional-samples)
4. [predictive replay and review system](/market-intel/workflows/predictive-replay-and-review-system)

## 먼저 확인
- [daily workspace](/market-intel/daily/)
- [validated recap — {recap_label}]({recap_link})
- [close input — {close_label}]({close_link})

## 용어 정리
- 예측 후보 검토 전에 **현재 세션 prep이 exact-date로 있는지** 먼저 확인해야 한다.
- exact-date prep이 없으면 fallback prep을 보더라도 상태는 `준비 완료`가 아니다.
- replay / dashboard는 readiness 확인 뒤 들어가는 보조 작업공간이다.
"""


def current_session_status_markdown(state: CurrentState) -> str:
    runtime_now_html = build_runtime_now_html(state.today_label)
    readiness_text, ready_count, total_count = readiness_summary(state)
    return f"""---
title: current readiness board
summary: 지금 세션 기준으로 필요한 핵심 daily 문서가 자동으로 확인됐는지 한눈에 보는 현황판.
---

# Current Readiness Board

## 지금 세션 자동 판정 ({current_label_span(state)})
- 실시간 KST 기준: {runtime_now_html}
- 현재 세션: `{state.today_date}` / `{state.phase}`
- 상태판 기준: `{state.checklist_title}`
- 준비도: `{readiness_text}` = `{ready_count} / {total_count}`
- 이 현황판은 sync/build 때 자동 생성된다.

## 자동 확인 결과
{render_status_lines(state)}

## 운영 추가 체크
{render_extra_status_lines(state)}

## 자동 확인이 실제로 들어가 있나
- 자동 확인 트리거: `~/market-intel-site/scripts/sync-market-intel.sh`
- 실제 판정 로직: `~/market-intel-site/scripts/update_market_intel_entrypoints.py`
- 자동 판정 대상:
  - `오늘/다음 세션 prep` = exact-date match
  - `직전 장 validated recap` = exact-date + `validation_status: validated`
  - `직전 장 close input` = exact-date match
  - `final evening briefing output` = exact-date match
  - `same-day source archive` = phase-aware check (`장전/장중`에는 WAITING 가능, `장후`에는 READY/MISSING)
- 현재 반영 위치: `/`, `/market-intel/`, `/market-intel/daily/`, `/market-intel/research/prediction-workspace`, `/market-intel/current-readiness-board`
- 한계: 이 확인은 **sync/build 시점 자동화**다. 즉 문서 존재 여부를 자동 판정해 표시하지만, 별도 cron 없이 매분 실시간 재판정하는 구조는 아니다.

## 확인 기준
- prep target: `{state.required_prep_date}_next-session-prep`
- validated recap target: `{state.required_recap_date}_top30_recap`
- close input target: `{state.required_close_input_date}_evening-briefing-input`
- briefing output target: `{state.required_briefing_output_date}_evening-briefing`
- same-day archive target: `{state.same_day_archive_path}`
- fallback은 참고용이지 readiness 충족으로 보지 않음

## 최신 usable 문서
{render_latest_lines(state)}

## 이 페이지를 어떻게 써야 하나
- 이 페이지는 **지금 세션에 필요한 문서가 최신인지**를 먼저 확인하는 운영 현황판이다.
- `MISSING`이면 target 문서가 아직 없다는 뜻이고, fallback은 참고용일 뿐 target을 대체한 것으로 간주하지 않는다.
- 장기 로드맵/큰그림은 [market-intel progress big picture](/market-intel/market-intel-progress-big-picture)에서 본다.
- 실제 작업 시작은 [daily workspace](/market-intel/daily/)로 들어간다.

## 다음 액션
{next_action_lines(state)}

## 관련 페이지
- [Market Intel Home](/market-intel/)
- [daily workspace](/market-intel/daily/)
- [prediction workspace](/market-intel/research/prediction-workspace)
- [market-intel progress big picture](/market-intel/market-intel-progress-big-picture)
"""


def ts_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def current_ts(state: CurrentState) -> str:
    keep_entries: list[str] = [
        "market-intel/MARKET_INTEL_RECENT_CHANGES",
        "market-intel/current-readiness-board",
        "market-intel/market-intel-progress-big-picture",
        "market-intel/daily/index",
        "market-intel/research/prediction-workspace",
        "market-intel/research/portfolio-pilot-review-dashboard",
        "market-intel/workflows/predictive-replay-and-review-system",
    ]
    labels: dict[str, str] = {
        "MARKET_INTEL_RECENT_CHANGES": "최근 변경 로그",
        "current-readiness-board": "진행상황판",
        "market-intel-progress-big-picture": "큰그림",
        "index": "Daily Workspace",
        "prediction-workspace": "Prediction Workspace",
        "portfolio-pilot-review-dashboard": "예측 후보 대시보드",
        "predictive-replay-and-review-system": "Predictive Replay",
    }
    if state.required_prep:
        keep_entries.append(f"market-intel/daily/{state.required_prep.slug}")
        labels[state.required_prep.slug] = "오늘 세션 prep"
    elif state.latest_prep:
        keep_entries.append(f"market-intel/daily/{state.latest_prep.slug}")
        labels[state.latest_prep.slug] = f"fallback prep ({state.latest_prep.date})"
    if state.required_recap:
        keep_entries.append(f"market-intel/daily/{state.required_recap.slug}")
        labels[state.required_recap.slug] = "직전 장 validated recap"
    elif state.latest_validated_recap:
        keep_entries.append(f"market-intel/daily/{state.latest_validated_recap.slug}")
        labels[state.latest_validated_recap.slug] = f"fallback recap ({state.latest_validated_recap.date})"
    if state.required_close_input:
        keep_entries.append(f"market-intel/daily/{state.required_close_input.slug}")
        labels[state.required_close_input.slug] = "직전 장 close input"
    elif state.latest_close_input:
        keep_entries.append(f"market-intel/daily/{state.latest_close_input.slug}")
        labels[state.latest_close_input.slug] = f"fallback close ({state.latest_close_input.date})"

    keep_block = "\n".join(f'  "{ts_string(item)}",' for item in keep_entries)
    label_lines = [
        '  "market-intel": "Market Intel Home",',
        '  "daily": "Daily",',
        '  "research": "Prediction / Research",',
        '  "workflows": "Workflows",',
        '  "architecture": "Architecture",',
        '  "events": "Events",',
        '  "entities": "Stocks",',
        '  "templates": "Templates",',
        '  "scripts": "Scripts",',
    ]
    for key, value in labels.items():
        label_lines.append(f'  "{ts_string(key)}": "{ts_string(value)}",')
    labels_block = "\n".join(label_lines)
    return f"""export const MARKET_INTEL_EXPLORER_KEEP_ENTRIES = [
{keep_block}
] as const

export const MARKET_INTEL_EXPLORER_LABELS: Record<string, string> = {{
{labels_block}
}}
"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    vault_path = Path(args.vault_path).expanduser().resolve()
    site_root = Path(args.site_root).expanduser().resolve()
    jmkr_root = Path(args.jmkr_root).expanduser().resolve()
    vault_market_intel = vault_path / "market-intel"
    if not vault_market_intel.exists():
        raise SystemExit(f"market-intel folder not found in vault: {vault_market_intel}")
    if not site_root.exists():
        raise SystemExit(f"site root not found: {site_root}")
    if not jmkr_root.exists():
        raise SystemExit(f"jmkr root not found: {jmkr_root}")

    state = build_state(vault_market_intel, jmkr_root)
    daily_dir = vault_market_intel / "daily"

    write(site_root / "content/index.md", root_markdown(state))
    write(vault_market_intel / "index.md", market_home_markdown(state))
    write(vault_market_intel / "daily/index.md", daily_index_markdown(state, daily_dir))
    write(vault_market_intel / "research/prediction-workspace.md", prediction_workspace_markdown(state))
    write(vault_market_intel / "current-readiness-board.md", current_session_status_markdown(state))
    write(site_root / "market-intel-current.ts", current_ts(state))

    readiness_text, ready_count, total_count = readiness_summary(state)
    print(f"Updated current Market Intel entrypoints for {state.today_label}")
    print(f"  checklist: {state.checklist_title}")
    print(f"  readiness: {readiness_text} ({ready_count}/{total_count})")
    print(f"  required_prep: {state.required_prep_date} -> {state.required_prep.slug if state.required_prep else 'missing'}")
    print(f"  required_recap: {state.required_recap_date} -> {state.required_recap.slug if state.required_recap else 'missing'}")
    print(f"  required_close_input: {state.required_close_input_date} -> {state.required_close_input.slug if state.required_close_input else 'missing'}")
    print(f"  latest_prep: {state.latest_prep.slug if state.latest_prep else 'missing'}")
    print(f"  latest_validated_recap: {state.latest_validated_recap.slug if state.latest_validated_recap else 'missing'}")
    print(f"  latest_close_input: {state.latest_close_input.slug if state.latest_close_input else 'missing'}")
    print(f"  required_briefing_output: {state.required_briefing_output_date} -> {state.required_briefing_output.slug if state.required_briefing_output else 'missing'}")
    print(f"  latest_briefing_output: {state.latest_briefing_output.slug if state.latest_briefing_output else 'missing'}")
    print(f"  same_day_archive: {state.same_day_archive_path} -> {'exists' if state.same_day_archive_path.exists() else 'missing'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
