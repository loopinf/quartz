from __future__ import annotations

from datetime import date, datetime, timezone
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SITE_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from market_intel_visuals import (  # type: ignore[import-not-found]
    build_related_stock_inline_section,
    build_runtime_now_html,
    build_stock_glance_section,
    parse_krx_corp_table,
    parse_naver_chart_xml,
    performance_sparkline_svg,
    sparkline_svg,
)
from enrich_stock_note_related_sparklines import (  # type: ignore[import-not-found]
    decorate_inline_block,
    inject_inline_block,
    related_names,
    should_refresh_cached_asset,
)


def test_build_runtime_now_html_exposes_runtime_hook_ids() -> None:
    html = build_runtime_now_html("2026-04-22 KST, 수요일 장중")
    assert "market-intel-now-label" in html
    assert "market-intel-now-script" in html
    assert "장중" in html
    assert "Intl.DateTimeFormat" in html


def test_parse_krx_corp_table_extracts_name_code_mapping() -> None:
    html = """
    <table>
      <tr><th>회사명</th><th>시장구분</th><th>종목코드</th></tr>
      <tr><td>씨아이에스</td><td>코스닥</td><td>222080</td></tr>
      <tr><td>에이에프더블류</td><td>코스닥</td><td>312610</td></tr>
    </table>
    """
    mapping = parse_krx_corp_table(html)
    assert mapping["씨아이에스"] == "222080"
    assert mapping["에이에프더블류"] == "312610"


def test_parse_naver_chart_xml_reads_close_series() -> None:
    xml_text = """<?xml version='1.0' encoding='EUC-KR' ?>
    <protocol>
      <chartdata symbol='222080'>
        <item data='20260418|1000|1100|900|1050|10000' />
        <item data='20260419|1050|1200|1000|1190|12000' />
      </chartdata>
    </protocol>
    """
    rows = parse_naver_chart_xml(xml_text)
    assert rows[0]["date"] == "2026-04-18"
    assert rows[0]["close"] == 1050
    assert rows[1]["close"] == 1190


def test_sparkline_svg_contains_polyline_and_last_point() -> None:
    svg = sparkline_svg([100, 110, 105, 125], width=80, height=24)
    assert svg.startswith("<svg")
    assert "polyline" in svg
    assert "circle" in svg
    assert "viewBox=\"0 0 80 24\"" in svg


def test_build_stock_glance_section_renders_stock_cards() -> None:
    section = build_stock_glance_section(
        [
            {
                "name": "씨아이에스",
                "entity_href": "/market-intel/entities/stocks/씨아이에스",
                "sparkline_href": "/market-intel/assets/sparklines/2026-04-21-battery/씨아이에스.svg",
                "change_text": "+29.96%",
            }
        ]
    )
    assert "Quick Chart Glance" in section
    assert "씨아이에스" in section
    assert "img" in section
    assert "/market-intel/assets/sparklines/2026-04-21-battery/씨아이에스.svg" in section


def test_build_related_stock_inline_section_renders_lightweight_rows_with_compact_delta_meta() -> None:
    section = build_related_stock_inline_section(
        [
            {
                "name": "엘티씨",
                "entity_href": "/market-intel/entities/stocks/엘티씨",
                "sparkline_href": "/market-intel/assets/stock-related-sparklines/코스텍시스/엘티씨.svg",
                "change_text": "+18.42%",
                "sparkline_delta_text": "+12%",
            },
            {
                "name": "OCI",
                "entity_href": "/market-intel/entities/stocks/OCI",
                "sparkline_href": "/market-intel/assets/stock-related-sparklines/코스텍시스/OCI.svg",
                "change_text": "",
                "sparkline_delta_text": "",
            },
        ]
    )
    assert "mi-related-inline-list" in section
    assert "mi-related-inline-item" in section
    assert "mi-related-inline-spark-wrap" in section
    assert "mi-related-inline-delta" in section
    assert "엘티씨" in section
    assert "+18.42%" not in section
    assert "+12%" in section
    assert "/market-intel/assets/stock-related-sparklines/코스텍시스/엘티씨.svg" in section
    assert "최근 20거래일 흐름" in section


def test_related_names_supports_aliased_and_plain_wikilinks() -> None:
    section_body = """
- [[market-intel/entities/stocks/엘티씨|엘티씨]]
- [[market-intel/entities/stocks/OCI]]
- [[네패스아크]]
""".strip()
    assert related_names(section_body) == ["엘티씨", "OCI", "네패스아크"]


def test_should_refresh_cached_asset_when_missing_or_stale(tmp_path: Path) -> None:
    asset_path = tmp_path / "sparks" / "고영.svg"
    now = datetime(2026, 4, 28, 10, 0, tzinfo=timezone.utc)

    assert should_refresh_cached_asset(
        asset_path=asset_path,
        cache_entry=None,
        today=date(2026, 4, 28),
        now=now,
    )

    asset_path.parent.mkdir(parents=True, exist_ok=True)
    asset_path.write_text("<svg />", encoding="utf-8")

    assert should_refresh_cached_asset(
        asset_path=asset_path,
        cache_entry={"series_end_date": "2026-04-27", "fetched_at": "2026-04-27T15:40:00+00:00"},
        today=date(2026, 4, 28),
        now=now,
    )


def test_should_refresh_cached_asset_respects_intraday_ttl_and_closed_market(tmp_path: Path) -> None:
    asset_path = tmp_path / "sparks" / "네패스아크.svg"
    asset_path.parent.mkdir(parents=True, exist_ok=True)
    asset_path.write_text("<svg />", encoding="utf-8")

    market_hours_entry = {"series_end_date": "2026-04-28", "fetched_at": "2026-04-28T09:00:00+00:00"}
    assert should_refresh_cached_asset(
        asset_path=asset_path,
        cache_entry=market_hours_entry,
        today=date(2026, 4, 28),
        now=datetime(2026, 4, 28, 10, 0, tzinfo=timezone.utc),
        refresh_minutes=30,
        is_trading_day=True,
        session_phase="장중",
    )

    assert not should_refresh_cached_asset(
        asset_path=asset_path,
        cache_entry={"series_end_date": "2026-04-28", "fetched_at": "2026-04-28T09:45:00+00:00"},
        today=date(2026, 4, 28),
        now=datetime(2026, 4, 28, 10, 0, tzinfo=timezone.utc),
        refresh_minutes=30,
        is_trading_day=True,
        session_phase="장중",
    )

    assert not should_refresh_cached_asset(
        asset_path=asset_path,
        cache_entry=market_hours_entry,
        today=date(2026, 4, 28),
        now=datetime(2026, 4, 28, 18, 0, tzinfo=timezone.utc),
        refresh_minutes=30,
        is_trading_day=True,
        session_phase="장후",
    )


def test_performance_sparkline_svg_adds_reference_guides_and_percent_labels() -> None:
    svg = performance_sparkline_svg([100, 110, 120, 118], width=84, height=20)
    assert svg.startswith("<svg")
    assert 'data-guide="true"' in svg
    assert ">10%<" in svg
    assert ">20%<" in svg
    assert 'aria-label="sparkline' in svg


def test_decorate_inline_block_uses_dynamic_mobile_safe_sparkline_sizing() -> None:
    styled = decorate_inline_block('<div class="mi-related-inline-list"></div>')
    assert 'minmax(min(220px,100%),1fr)' in styled
    assert 'width:100%' in styled
    assert 'overflow-x:clip' in styled
    assert '@media (max-width: 480px)' in styled
    assert 'grid-template-columns:minmax(0,1fr)' in styled
    assert 'justify-self:stretch' in styled


def test_inject_inline_block_replaces_previous_injected_markup() -> None:
    original = """
<style>
.mi-related-inline-list{display:grid}
.mi-related-inline-list ~ ul{display:none}
</style>

<div class="mi-related-inline-list">old</div>

- [[market-intel/entities/stocks/엘티씨|엘티씨]]
- [[market-intel/entities/stocks/OCI|OCI]]
""".strip()
    updated = inject_inline_block(original, '<div class="mi-related-inline-list">new</div>')
    assert updated.count('mi-related-inline-list') == 1
    assert 'old' not in updated
    assert 'new' in updated
    assert '[[market-intel/entities/stocks/엘티씨|엘티씨]]' in updated
