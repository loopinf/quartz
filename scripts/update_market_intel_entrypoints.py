#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime
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
class CurrentState:
    now: datetime
    today_date: str
    today_label: str
    phase: str
    expected_prep_slug: str
    required_prep: NoteRef | None
    latest_prep: NoteRef | None
    recap: NoteRef | None
    close_input: NoteRef | None


@dataclass(frozen=True)
class DocStatus:
    code: str
    label: str
    summary: str
    target_slug: str
    note: NoteRef | None
    fallback: NoteRef | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Refresh current-date Market Intel entrypoint pages and sidebar constants.")
    parser.add_argument("--vault-path", default=str(Path.home() / "Documents" / "Obsidian Vault"))
    parser.add_argument("--site-root", default=str(Path.home() / "market-intel-site"))
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
        slug = path.stem
        matches.append(NoteRef(date=date_part, slug=slug, title=slug, path=path))
    return sorted(matches, key=lambda item: item.date)


def find_latest_note(
    daily_dir: Path,
    suffix: str,
    *,
    require_validated: bool = False,
    before_date: str | None = None,
    include_before_date: bool = True,
    exact_date: str | None = None,
) -> NoteRef | None:
    matches = iter_matching_notes(daily_dir, suffix, require_validated=require_validated)
    filtered: list[NoteRef] = []
    for item in matches:
        if exact_date is not None and item.date != exact_date:
            continue
        if before_date is not None:
            if include_before_date:
                if item.date > before_date:
                    continue
            else:
                if item.date >= before_date:
                    continue
        filtered.append(item)
    return max(filtered, key=lambda item: item.date, default=None)


def build_state(vault_market_intel: Path) -> CurrentState:
    now = datetime.now(KST)
    today_date = now.strftime("%Y-%m-%d")
    phase = market_phase(now)
    daily_dir = vault_market_intel / "daily"

    required_prep = find_latest_note(daily_dir, "next-session-prep", exact_date=today_date)
    latest_prep = find_latest_note(daily_dir, "next-session-prep")

    recap_before_today = find_latest_note(
        daily_dir,
        "top30_recap",
        require_validated=True,
        before_date=today_date,
        include_before_date=False,
    )
    recap_on_or_before_today = find_latest_note(
        daily_dir,
        "top30_recap",
        require_validated=True,
        before_date=today_date,
        include_before_date=True,
    )
    close_before_today = find_latest_note(
        daily_dir,
        "evening-briefing-input",
        before_date=today_date,
        include_before_date=False,
    )
    close_on_or_before_today = find_latest_note(
        daily_dir,
        "evening-briefing-input",
        before_date=today_date,
        include_before_date=True,
    )

    if phase == "장후":
        recap = recap_on_or_before_today
        close_input = close_on_or_before_today
    else:
        recap = recap_before_today
        close_input = close_before_today

    return CurrentState(
        now=now,
        today_date=today_date,
        today_label=current_label(now),
        phase=phase,
        expected_prep_slug=f"{today_date}_next-session-prep",
        required_prep=required_prep,
        latest_prep=latest_prep,
        recap=recap,
        close_input=close_input,
    )


def rel_link(note: NoteRef | None) -> str:
    return f"/market-intel/daily/{note.slug}" if note else "/market-intel/daily/"


def note_text(note: NoteRef | None, fallback: str) -> str:
    return note.slug if note else fallback


def current_label_span(state: CurrentState) -> str:
    return (
        f'<span data-mi-current-label="1" data-mi-current-date="{state.today_date}" '
        f'data-mi-current-phase="{state.phase}">{state.today_label}</span>'
    )


def current_date_span(state: CurrentState) -> str:
    return f'<span data-mi-current-date="1">{state.today_date}</span>'


def readiness_doc_statuses(state: CurrentState) -> list[DocStatus]:
    statuses: list[DocStatus] = []
    if state.required_prep:
        statuses.append(
            DocStatus(
                code="READY",
                label="오늘 세션 prep",
                summary=f"{state.required_prep.slug} 문서가 현재 세션용으로 준비되어 있다.",
                target_slug=state.expected_prep_slug,
                note=state.required_prep,
            )
        )
    else:
        fallback = state.latest_prep
        fallback_summary = (
            f"최신 fallback은 {fallback.slug}이지만 오늘 세션용 문서는 아직 없다."
            if fallback
            else "fallback으로 쓸 prep도 아직 없다."
        )
        statuses.append(
            DocStatus(
                code="MISSING",
                label="오늘 세션 prep",
                summary=f"target은 {state.expected_prep_slug}인데 아직 없다. {fallback_summary}",
                target_slug=state.expected_prep_slug,
                note=None,
                fallback=fallback,
            )
        )

    if state.recap:
        statuses.append(
            DocStatus(
                code="READY",
                label="직전 장 validated recap",
                summary=f"현재 세션 바로 직전 장 기준 validated recap은 {state.recap.slug}이다.",
                target_slug=state.recap.slug,
                note=state.recap,
            )
        )
    else:
        statuses.append(
            DocStatus(
                code="MISSING",
                label="직전 장 validated recap",
                summary="직전 장 기준 validated recap을 찾지 못했다.",
                target_slug="",
                note=None,
            )
        )

    if state.close_input:
        statuses.append(
            DocStatus(
                code="READY",
                label="직전 장 close input",
                summary=f"현재 세션 직전 장 close input은 {state.close_input.slug}이다.",
                target_slug=state.close_input.slug,
                note=state.close_input,
            )
        )
    else:
        statuses.append(
            DocStatus(
                code="MISSING",
                label="직전 장 close input",
                summary="직전 장 close input을 찾지 못했다.",
                target_slug="",
                note=None,
            )
        )
    return statuses


def readiness_label(state: CurrentState) -> tuple[str, int, int]:
    statuses = readiness_doc_statuses(state)
    ready_count = sum(1 for status in statuses if status.code == "READY")
    total = len(statuses)
    if ready_count == total:
        return "ready", ready_count, total
    if ready_count == 0:
        return "not-ready", ready_count, total
    return "partial", ready_count, total


def readiness_lines(state: CurrentState, *, root_prefix: str = "/market-intel/daily/") -> str:
    lines: list[str] = []
    for status in readiness_doc_statuses(state):
        if status.note:
            lines.append(f"- `{status.code}` {status.label}: [{status.note.slug}]({root_prefix}{status.note.slug})")
        else:
            lines.append(f"- `{status.code}` {status.label}: target `{status.target_slug}`")
        lines.append(f"  - {status.summary}")
        if status.fallback:
            lines.append(f"  - latest fallback: [{status.fallback.slug}]({root_prefix}{status.fallback.slug})")
    return "\n".join(lines)


def next_action_lines(state: CurrentState) -> str:
    lines: list[str] = []
    if state.required_prep:
        lines.append(f"1. [오늘 세션 prep 열기](/market-intel/daily/{state.required_prep.slug})")
    elif state.latest_prep:
        lines.append("1. [daily workspace에서 오늘 세션 prep 상태 확인](/market-intel/daily/)")
        lines.append(f"2. fallback으로 [{state.latest_prep.slug}](/market-intel/daily/{state.latest_prep.slug}) 참고")
    else:
        lines.append("1. [daily workspace](/market-intel/daily/)에서 오늘 세션 prep부터 만들어야 한다")

    start_index = len(lines) + 1
    if state.recap:
        lines.append(f"{start_index}. [직전 장 validated recap 확인](/market-intel/daily/{state.recap.slug})")
        start_index += 1
    if state.close_input:
        lines.append(f"{start_index}. [직전 장 close input 확인](/market-intel/daily/{state.close_input.slug})")
        start_index += 1
    lines.append(f"{start_index}. [prediction workspace](/market-intel/research/prediction-workspace)")
    return "\n".join(lines)


def terminology_block() -> str:
    return """- `오늘 세션 prep`: 오늘 장 대응용 next-session-prep 문서
- `직전 장 validated recap`: 지금 세션 바로 이전 장의 검증 완료 TOP30 recap
- `직전 장 close input`: 직전 장 마감 뒤 남긴 evening briefing input
- `준비도`: 지금 시점에 필요한 핵심 3문서(prep / recap / close input)가 몇 개 준비됐는지"""


def root_markdown(state: CurrentState) -> str:
    runtime_now_html = build_runtime_now_html(state.today_label)
    readiness_state, ready_count, total_count = readiness_label(state)
    return f"""---
title: Market Intel Start
summary: 8081 루트 시작점. 오늘 세션 준비도와 최신 usable 문서를 가장 먼저 보여준다.
---

# Market Intel Start

## 지금 준비 상태 ({current_label_span(state)})
- 실시간 KST 기준: {runtime_now_html}
- 현재 세션: `{state.today_date}` / `{state.phase}`
- 준비도: `{readiness_state}` = `{ready_count} / {total_count} ready`
- 기준 문서 순서: `오늘 세션 prep → 직전 장 validated recap → 직전 장 close input`

{readiness_lines(state)}

## 지금 바로 할 일
{next_action_lines(state)}

## 해석 기준
- 이 페이지에서 `오늘`은 **현재 KST 운영 날짜**를 뜻한다.
- prep은 **오늘 세션 기준 exact date match**가 있어야 `READY`다.
- recap / close input은 **현재 세션 바로 직전 장 기준** 문서를 보여준다.

## 용어 정리
{terminology_block()}

## 섹션 바로가기
- [Market Intel home](/market-intel/)
- [daily workspace](/market-intel/daily/)
- [prediction workspace](/market-intel/research/prediction-workspace)
- [recent changes](/market-intel/MARKET_INTEL_RECENT_CHANGES)
- [research folder](/market-intel/research/)
- [workflow folder](/market-intel/workflows/)
- [events folder](/market-intel/events/)
- [entities folder](/market-intel/entities/)
"""


def market_home_markdown(state: CurrentState) -> str:
    runtime_now_html = build_runtime_now_html(state.today_label)
    readiness_state, ready_count, total_count = readiness_label(state)
    return f"""---
title: Market Intel Home
summary: 오늘 세션 준비 상태를 먼저 보여주고, 필요한 문서가 최신인지 바로 확인하게 하는 운영 홈.
---

# Market Intel Home

## 오늘 준비 상태 ({current_label_span(state)})
- 실시간 KST 기준: {runtime_now_html}
- 현재 세션: `{state.today_date}` / `{state.phase}`
- 준비도: `{readiness_state}` = `{ready_count} / {total_count} ready`
- 최근 변경 로그: [MARKET_INTEL_RECENT_CHANGES](/market-intel/MARKET_INTEL_RECENT_CHANGES)

{readiness_lines(state)}

## 오늘 바로 할 일
{next_action_lines(state)}

## 왜 이렇게 보나
- index에서는 **지금 필요한 문서가 최신인지**를 먼저 확인해야 한다.
- `직전`은 "직전 작업한 문서"가 아니라 **현재 세션 바로 직전 장 기준 문서**를 뜻한다.
- 오늘 prep이 없으면 fallback을 보여주되, `MISSING`으로 명확히 남긴다.

## 용어 정리
{terminology_block()}

## 큰그림 / 작업공간
- [daily workspace](/market-intel/daily/)
- [prediction workspace](/market-intel/research/prediction-workspace)
- [portfolio pilot review dashboard](/market-intel/research/portfolio-pilot-review-dashboard)
- [predictive replay and review system](/market-intel/workflows/predictive-replay-and-review-system)
- [market-intel progress big picture](/market-intel/market-intel-progress-big-picture)
- [SOT — market-intel full pipeline](/market-intel/architecture/sot-market-intel-full-pipeline)
"""


def daily_index_markdown(state: CurrentState) -> str:
    runtime_now_html = build_runtime_now_html(state.today_label)
    readiness_state, ready_count, total_count = readiness_label(state)
    latest_prep_line = (
        f"- latest prep fallback: [{state.latest_prep.slug}](/market-intel/daily/{state.latest_prep.slug})"
        if state.latest_prep and not state.required_prep
        else ""
    )
    return f"""---
title: daily workspace
summary: 오늘 세션 준비도와 핵심 daily 문서 상태를 한 번에 확인하는 허브.
---

# Daily Workspace

## 오늘 세션 readiness ({current_label_span(state)})
- 실시간 KST 기준: {runtime_now_html}
- 준비도: `{readiness_state}` = `{ready_count} / {total_count} ready`
- 확인 순서: `오늘 세션 prep → 직전 장 validated recap → 직전 장 close input`

{readiness_lines(state)}
{latest_prep_line}

## 오늘 바로 열 것
{next_action_lines(state)}

## 최근 usable 기록
### Session prep
- [{note_text(state.required_prep or state.latest_prep, 'prep 문서 없음')}](/market-intel/daily/{(state.required_prep or state.latest_prep).slug if (state.required_prep or state.latest_prep) else ''})
- [2026-04-20_next-session-prep](/market-intel/daily/2026-04-20_next-session-prep)
- [2026-04-17_next-session-prep](/market-intel/daily/2026-04-17_next-session-prep)

### Validated recap
- [{note_text(state.recap, 'validated recap 없음')}](/market-intel/daily/{state.recap.slug if state.recap else ''})
- [2026-04-21_top30_recap](/market-intel/daily/2026-04-21_top30_recap)
- [2026-04-20_top30_recap](/market-intel/daily/2026-04-20_top30_recap)

### Close input
- [{note_text(state.close_input, 'close input 없음')}](/market-intel/daily/{state.close_input.slug if state.close_input else ''})
- [2026-04-21_evening-briefing-input](/market-intel/daily/2026-04-21_evening-briefing-input)
- [2026-04-20_evening-briefing-input](/market-intel/daily/2026-04-20_evening-briefing-input)

### Supporting context
- [2026-04-16_news_recap](/market-intel/daily/2026-04-16_news_recap)
- [2026-04-16_high-signal-watchlist](/market-intel/daily/2026-04-16_high-signal-watchlist)
- [2026-04-15_us-to-kr-bridge](/market-intel/daily/2026-04-15_us-to-kr-bridge)
- [2026-04-16_us-to-kr-bridge-mythos-banks](/market-intel/daily/2026-04-16_us-to-kr-bridge-mythos-banks)

## 용어 정리
{terminology_block()}
"""


def prediction_workspace_markdown(state: CurrentState) -> str:
    runtime_now_html = build_runtime_now_html(state.today_label)
    prep_line = (
        f"1. [오늘 세션 prep — {state.required_prep.slug}](/market-intel/daily/{state.required_prep.slug})"
        if state.required_prep
        else "1. [daily workspace에서 오늘 세션 prep 상태 확인](/market-intel/daily/)"
    )
    fallback_line = (
        f"- latest prep fallback: [{state.latest_prep.slug}](/market-intel/daily/{state.latest_prep.slug})"
        if state.latest_prep and not state.required_prep
        else ""
    )
    return f"""---
title: prediction workspace
summary: 오늘 세션 prep 준비 여부를 먼저 확인한 뒤 예측 후보와 복기로 이어지는 작업공간.
---

# Prediction Workspace

## 오늘 바로 할 일 ({current_label_span(state)})
- 실시간 KST 기준: {runtime_now_html}
{prep_line}
2. [portfolio pilot review dashboard](/market-intel/research/portfolio-pilot-review-dashboard)
3. [portfolio pilot batch — additional samples](/market-intel/research/portfolio-pilot-batch-additional-samples)
4. [predictive replay and review system](/market-intel/workflows/predictive-replay-and-review-system)
{fallback_line}

## 먼저 확인
- [daily workflow](/market-intel/daily/)
- [직전 장 validated recap — {note_text(state.recap, '없음')}](/market-intel/daily/{state.recap.slug if state.recap else ''})
- [직전 장 close input — {note_text(state.close_input, '없음')}](/market-intel/daily/{state.close_input.slug if state.close_input else ''})

## 용어 정리
- `오늘 세션 prep`이 먼저 준비돼 있어야 예측 후보 해석이 현재 시점과 맞는다.
- `직전 장 validated recap`은 전일 주도 군집 확인용 anchor다.
- `직전 장 close input`은 전일 맥락을 붙이는 보조 입력이다.

## 자주 쓰는 링크
- [portfolio pilot review dashboard](/market-intel/research/portfolio-pilot-review-dashboard)
- [portfolio pilot batch — additional samples](/market-intel/research/portfolio-pilot-batch-additional-samples)
- [predictive replay and review system](/market-intel/workflows/predictive-replay-and-review-system)
- [replay — 2026-04-14 NVIDIA Ising](/market-intel/research/replay-2026-04-14-nvidia-ising)
- [replay — 2026-04-13 Anthropic Mythos · banks](/market-intel/research/replay-2026-04-13-anthropic-mythos-banks)
- [US to KR bridge — 2026-04-16 Mythos · banks](/market-intel/daily/2026-04-16_us-to-kr-bridge-mythos-banks)
"""


def ts_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def current_ts(state: CurrentState) -> str:
    keep_entries: list[str] = [
        "market-intel/MARKET_INTEL_RECENT_CHANGES",
        "market-intel/market-intel-progress-big-picture",
        "market-intel/daily/index",
        "market-intel/research/prediction-workspace",
        "market-intel/research/portfolio-pilot-review-dashboard",
        "market-intel/workflows/predictive-replay-and-review-system",
    ]
    labels: dict[str, str] = {
        "MARKET_INTEL_RECENT_CHANGES": "최근 변경 로그",
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
        labels[state.latest_prep.slug] = "latest prep fallback"
    if state.recap:
        keep_entries.append(f"market-intel/daily/{state.recap.slug}")
        labels[state.recap.slug] = "직전 장 validated recap"
    if state.close_input:
        keep_entries.append(f"market-intel/daily/{state.close_input.slug}")
        labels[state.close_input.slug] = "직전 장 close input"

    keep_block = "\n".join(f'  "{ts_string(item)}",' for item in keep_entries)
    label_lines = [
        '  "market-intel": "Market Intel Home",',
        '  "daily": "Daily",',
        '  "research": "Prediction / Research",',
        '  "workflows": "Workflows",',
        '  "events": "Events",',
        '  "entities": "Stocks",',
    ]
    for key, value in labels.items():
        label_lines.append(f'  "{ts_string(key)}": "{ts_string(value)}",')
    labels_block = "\n".join(label_lines)
    return f"""export const MARKET_INTEL_EXPLORER_KEEP = new Set([
{keep_block}
])

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
    vault_market_intel = vault_path / "market-intel"
    if not vault_market_intel.exists():
        raise SystemExit(f"market-intel folder not found in vault: {vault_market_intel}")
    if not site_root.exists():
        raise SystemExit(f"site root not found: {site_root}")

    state = build_state(vault_market_intel)

    write(site_root / "content/index.md", root_markdown(state))
    write(vault_market_intel / "index.md", market_home_markdown(state))
    write(vault_market_intel / "daily/index.md", daily_index_markdown(state))
    write(vault_market_intel / "research/prediction-workspace.md", prediction_workspace_markdown(state))
    write(site_root / "market-intel-current.ts", current_ts(state))

    readiness_state, ready_count, total_count = readiness_label(state)
    print(f"Updated current Market Intel entrypoints for {state.today_label}")
    print(f"  readiness: {readiness_state} ({ready_count}/{total_count})")
    print(f"  expected_prep: {state.expected_prep_slug}")
    if state.required_prep:
        print(f"  required_prep: {state.required_prep.slug}")
    if state.latest_prep:
        print(f"  latest_prep: {state.latest_prep.slug}")
    if state.recap:
        print(f"  recap: {state.recap.slug}")
    if state.close_input:
        print(f"  close_input: {state.close_input.slug}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
