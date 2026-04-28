from __future__ import annotations

from html.parser import HTMLParser
from typing import Iterable
from xml.etree import ElementTree as ET


class _KrxTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.in_td = False
        self.current_row: list[str] = []
        self.rows: list[list[str]] = []
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # type: ignore[override]
        if tag == "td":
            self.in_td = True
            self._buf = []
        elif tag == "tr":
            self.current_row = []

    def handle_data(self, data: str) -> None:  # type: ignore[override]
        if self.in_td:
            self._buf.append(data)

    def handle_endtag(self, tag: str) -> None:  # type: ignore[override]
        if tag == "td" and self.in_td:
            self.in_td = False
            self.current_row.append("".join(self._buf).strip())
        elif tag == "tr" and self.current_row:
            self.rows.append(self.current_row)


def build_runtime_now_html(fallback_label: str, *, phase_override: str | None = None) -> str:
    escaped = fallback_label.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    phase_js = repr(phase_override) if phase_override is not None else "null"
    return f"""
<span id="market-intel-now-label">{escaped}</span>
<script id="market-intel-now-script">
(() => {{
  const el = document.getElementById('market-intel-now-label');
  if (!el) return;
  const now = new Date();
  const formatter = new Intl.DateTimeFormat('ko-KR', {{
    timeZone: 'Asia/Seoul',
    year: 'numeric', month: '2-digit', day: '2-digit',
    weekday: 'long', hour: '2-digit', minute: '2-digit', hour12: false,
  }});
  const parts = formatter.formatToParts(now);
  const take = (kind) => parts.find((p) => p.type === kind)?.value ?? '';
  const hour = Number(take('hour'));
  const minute = Number(take('minute'));
  const hhmm = hour * 100 + minute;
  const override = {phase_js};
  const phase = override ?? (hhmm < 900 ? '장전' : (hhmm < 1530 ? '장중' : '장후'));
  el.textContent = `${{take('year')}}-${{take('month')}}-${{take('day')}} KST, ${{take('weekday')}} ${{phase}}`;
}})();
</script>
""".strip()


def parse_krx_corp_table(html: str) -> dict[str, str]:
    parser = _KrxTableParser()
    parser.feed(html)
    mapping: dict[str, str] = {}
    for row in parser.rows:
        if len(row) < 3:
            continue
        name = row[0].strip()
        code_candidate = row[2].strip().zfill(6)
        if name and code_candidate.isalnum():
            mapping[name] = code_candidate
    return mapping


def parse_naver_chart_xml(xml_text: str) -> list[dict[str, int | str]]:
    root = ET.fromstring(xml_text)
    rows: list[dict[str, int | str]] = []
    for item in root.findall('.//item'):
        raw = item.attrib.get('data', '')
        parts = raw.split('|')
        if len(parts) < 6:
            continue
        date = parts[0]
        rows.append({
            'date': f'{date[0:4]}-{date[4:6]}-{date[6:8]}',
            'open': int(parts[1]),
            'high': int(parts[2]),
            'low': int(parts[3]),
            'close': int(parts[4]),
            'volume': int(parts[5]),
        })
    return rows


def sparkline_svg(values: Iterable[float], *, width: int = 96, height: int = 24, stroke: str = '#d84f45') -> str:
    points = list(values)
    if not points:
        points = [0.0, 0.0]
    if len(points) == 1:
        points = [points[0], points[0]]
    min_v, max_v = min(points), max(points)
    spread = max(max_v - min_v, 1e-9)
    xs = [i * (width - 4) / (len(points) - 1) + 2 for i in range(len(points))]
    ys = [height - 2 - ((v - min_v) / spread) * (height - 4) for v in points]
    polyline = ' '.join(f'{x:.2f},{y:.2f}' for x, y in zip(xs, ys))
    last_x, last_y = xs[-1], ys[-1]
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="sparkline">'
        f'<polyline fill="none" stroke="{stroke}" stroke-width="1.8" points="{polyline}" />'
        f'<circle cx="{last_x:.2f}" cy="{last_y:.2f}" r="2.2" fill="{stroke}" />'
        '</svg>'
    )


def _relative_percent_series(values: Iterable[float]) -> list[float]:
    points = [float(v) for v in values]
    if not points:
        return [0.0, 0.0]
    if len(points) == 1:
        return [0.0, 0.0]
    base = points[0] or 1.0
    return [((value / base) - 1.0) * 100.0 for value in points]


def performance_sparkline_svg(values: Iterable[float], *, width: int = 96, height: int = 24, stroke: str = '#5b74db') -> str:
    pct_points = _relative_percent_series(values)
    floor = min(min(pct_points), 0.0)
    ceil = max(max(pct_points), 0.0)
    guide_levels = [level for level in (-20.0, -10.0, 0.0, 10.0, 20.0) if floor - 0.5 <= level <= ceil + 0.5]
    if len(pct_points) == 1:
        pct_points = [pct_points[0], pct_points[0]]
    min_v = min(floor, min(pct_points))
    max_v = max(ceil, max(pct_points))
    spread = max(max_v - min_v, 1e-9)
    xs = [i * (width - 4) / (len(pct_points) - 1) + 2 for i in range(len(pct_points))]
    ys = [height - 2 - ((v - min_v) / spread) * (height - 4) for v in pct_points]
    polyline = ' '.join(f'{x:.2f},{y:.2f}' for x, y in zip(xs, ys))
    last_x, last_y = xs[-1], ys[-1]
    guides = ''.join(
        f'<line data-guide="true" x1="2" y1="{height - 2 - ((level - min_v) / spread) * (height - 4):.2f}" '
        f'x2="{width - 1}" y2="{height - 2 - ((level - min_v) / spread) * (height - 4):.2f}" '
        'stroke="currentColor" stroke-opacity="0.16" stroke-width="0.8" />'
        for level in guide_levels
    )
    labels = ''.join(
        f'<text x="{width - 1}" y="{height - 3 - ((level - min_v) / spread) * (height - 4):.2f}" '
        'font-size="4" text-anchor="end" fill="currentColor" fill-opacity="0.42">'
        f'{int(level)}%</text>'
        for level in guide_levels
        if level != 0.0
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" role="img" aria-label="sparkline, start-relative percent move">'
        f'{guides}{labels}'
        f'<polyline fill="none" stroke="{stroke}" stroke-width="1.8" points="{polyline}" />'
        f'<circle cx="{last_x:.2f}" cy="{last_y:.2f}" r="2.2" fill="{stroke}" />'
        '</svg>'
    )


def build_stock_glance_section(cards: list[dict[str, str]]) -> str:
    body = []
    for card in cards:
        body.append(
            "".join([
                '<div class="mi-stock-card">',
                f'<a class="mi-stock-name" href="{card["entity_href"]}">{card["name"]}</a>',
                f'<span class="mi-stock-change">{card["change_text"]}</span>',
                f'<img class="mi-stock-sparkline" src="{card["sparkline_href"]}" alt="{card["name"]} 최근 일봉 sparkline" loading="lazy" />',
                '</div>',
            ])
        )
    cards_html = "".join(body)
    return (
        "## Quick Chart Glance\n\n"
        '<div class="mi-stock-glance-grid">'
        f'{cards_html}'
        '</div>\n'
    )


def build_related_stock_inline_section(cards: list[dict[str, str]]) -> str:
    body = []
    for card in cards:
        delta_text = card.get("sparkline_delta_text", "")
        delta_html = f'<span class="mi-related-inline-delta">{delta_text}</span>' if delta_text else ''
        body.append(
            "".join([
                '<div class="mi-related-inline-item">',
                f'<a class="mi-related-inline-name" href="{card["entity_href"]}">{card["name"]}</a>',
                '<div class="mi-related-inline-spark-wrap">',
                f'<img class="mi-related-inline-sparkline" src="{card["sparkline_href"]}" alt="{card["name"]} 최근 20거래일 흐름" loading="lazy" />',
                delta_html,
                '</div>',
                '</div>',
            ])
        )
    cards_html = "".join(body)
    return (
        '<div class="mi-related-inline-list">'
        f'{cards_html}'
        '</div>'
    )
