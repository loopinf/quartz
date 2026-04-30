from __future__ import annotations

from datetime import date
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SITE_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from ensure_next_session_prep import (  # type: ignore[import-not-found]
    PrepContext,
    RecentRecap,
    ThemeCluster,
    build_content,
    stock_entity_label,
)
from enrich_next_session_prep_with_outcome_summary import build_section  # type: ignore[import-not-found]


def _write_stock_entity(vault_market_intel: Path, name: str, related: list[str] | None = None) -> None:
    related = related or []
    related_lines = "\n".join(f"- [[market-intel/entities/stocks/{item}|{item}]]" for item in related)
    content = f"""# {name}

## Theme Tags
- 전력기기

## Event History
- [[market-intel/events/2026-04-29_전력기기_모멘텀|전력기기 모멘텀]]

## Related Stocks
{related_lines}
"""
    (vault_market_intel / "entities" / "stocks").mkdir(parents=True, exist_ok=True)
    (vault_market_intel / "entities" / "stocks" / f"{name}.md").write_text(content, encoding="utf-8")


def _sample_context(tmp_path: Path) -> PrepContext:
    vault_market_intel = tmp_path / "market-intel"
    daily_dir = vault_market_intel / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    recap_path = daily_dir / "2026-04-29_top30_recap.md"
    recap_path.write_text("# recap\n", encoding="utf-8")
    close_input_path = daily_dir / "2026-04-29_evening-briefing-input.md"
    close_input_path.write_text("# input\n", encoding="utf-8")
    briefing_path = daily_dir / "2026-04-29_evening-briefing.md"
    briefing_path.write_text("# briefing\n", encoding="utf-8")

    _write_stock_entity(vault_market_intel, "선도전기", related=["제일일렉트릭"])
    _write_stock_entity(vault_market_intel, "제일일렉트릭", related=["선도전기"])
    _write_stock_entity(vault_market_intel, "대원전선")
    _write_stock_entity(vault_market_intel, "롯데케미칼")
    _write_stock_entity(vault_market_intel, "이수화학")
    _write_stock_entity(vault_market_intel, "싸이맥스")

    return PrepContext(
        vault_market_intel=vault_market_intel,
        target_date=date(2026, 4, 30),
        base_date=date(2026, 4, 29),
        recap_path=recap_path,
        close_input_path=close_input_path,
        briefing_path=briefing_path,
        existing_path=daily_dir / "2026-04-30_next-session-prep.md",
        event_slugs=["2026-04-29_전력기기_모멘텀"],
        theme_clusters=[
            ThemeCluster("전력기기", 4, ["선도전기", "제일일렉트릭", "대원전선"]),
            ThemeCluster("석유화학", 2, ["롯데케미칼", "이수화학"]),
            ThemeCluster("반도체소부장", 1, ["싸이맥스"]),
        ],
        ungrouped_names=[],
        recent_recaps=[RecentRecap(day=date(2026, 4, 29), path=recap_path, themes=["전력기기", "석유화학"])],
    )


def test_stock_entity_label_links_existing_entity_and_falls_back_when_missing(tmp_path: Path) -> None:
    vault_market_intel = tmp_path / "market-intel"
    _write_stock_entity(vault_market_intel, "선도전기")

    assert stock_entity_label(vault_market_intel, "선도전기") == "[[market-intel/entities/stocks/선도전기|선도전기]]"
    assert stock_entity_label(vault_market_intel, "없는종목") == "없는종목"


def test_build_content_emits_one_file_sections_with_linked_stock_names(tmp_path: Path) -> None:
    context = _sample_context(tmp_path)

    content = build_content(context)

    assert "## 1. Prep / Context" in content
    assert "## 2. Prediction" in content
    assert "## 3. Execution plan" in content
    assert "## 4. Evidence / Appendix" in content
    assert "## 5. Note boundary / review handoff" in content
    assert "[[market-intel/entities/stocks/선도전기|선도전기]]" in content
    assert "[[market-intel/entities/stocks/롯데케미칼|롯데케미칼]]" in content
    assert "leader: [[market-intel/entities/stocks/선도전기|선도전기]] / [[market-intel/entities/stocks/제일일렉트릭|제일일렉트릭]] / [[market-intel/entities/stocks/대원전선|대원전선]]" in content


def test_outcome_summary_links_stock_names_when_entity_pages_exist(tmp_path: Path) -> None:
    vault_market_intel = tmp_path / "market-intel"
    _write_stock_entity(vault_market_intel, "선도전기")

    note_text = """
## 신고가 / high-signal 팩트층
- breakout overlap 종목
  - 선도전기 (04/29, 52w_breakout)
""".strip()

    section = build_section(note_text, vault_market_intel=vault_market_intel)

    assert "[[market-intel/entities/stocks/선도전기|선도전기]]" in section
