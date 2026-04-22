---
title: daily workspace
summary: 오늘 세션 준비도와 핵심 daily 문서 상태를 한 번에 확인하는 허브.
---

# Daily Workspace

## 오늘 세션 readiness (<span data-mi-current-label="1" data-mi-current-date="2026-04-23" data-mi-current-phase="장전">2026-04-23 KST, 목요일 장전</span>)
- 실시간 KST 기준: <span id="market-intel-now-label">2026-04-23 KST, 목요일 장전</span>
<script id="market-intel-now-script">
(() => {
  const el = document.getElementById('market-intel-now-label');
  if (!el) return;
  const now = new Date();
  const formatter = new Intl.DateTimeFormat('ko-KR', {
    timeZone: 'Asia/Seoul',
    year: 'numeric', month: '2-digit', day: '2-digit',
    weekday: 'long', hour: '2-digit', minute: '2-digit', hour12: false,
  });
  const parts = formatter.formatToParts(now);
  const take = (kind) => parts.find((p) => p.type === kind)?.value ?? '';
  const hour = Number(take('hour'));
  const minute = Number(take('minute'));
  const hhmm = hour * 100 + minute;
  const phase = hhmm < 900 ? '장전' : (hhmm < 1530 ? '장중' : '장후');
  el.textContent = `${take('year')}-${take('month')}-${take('day')} KST, ${take('weekday')} ${phase}`;
})();
</script>
- 준비도: `partial` = `2 / 3 ready`
- 확인 순서: `오늘 세션 prep → 직전 장 validated recap → 직전 장 close input`

- `MISSING` 오늘 세션 prep: target `2026-04-23_next-session-prep`
  - target은 2026-04-23_next-session-prep인데 아직 없다. 최신 fallback은 2026-04-22_next-session-prep이지만 오늘 세션용 문서는 아직 없다.
  - latest fallback: [2026-04-22_next-session-prep](/market-intel/daily/2026-04-22_next-session-prep)
- `READY` 직전 장 validated recap: [2026-04-22_top30_recap](/market-intel/daily/2026-04-22_top30_recap)
  - 현재 세션 바로 직전 장 기준 validated recap은 2026-04-22_top30_recap이다.
- `READY` 직전 장 close input: [2026-04-22_evening-briefing-input](/market-intel/daily/2026-04-22_evening-briefing-input)
  - 현재 세션 직전 장 close input은 2026-04-22_evening-briefing-input이다.
- latest prep fallback: [2026-04-22_next-session-prep](/market-intel/daily/2026-04-22_next-session-prep)

## 오늘 바로 열 것
1. [daily workspace에서 오늘 세션 prep 상태 확인](/market-intel/daily/)
2. fallback으로 [2026-04-22_next-session-prep](/market-intel/daily/2026-04-22_next-session-prep) 참고
3. [직전 장 validated recap 확인](/market-intel/daily/2026-04-22_top30_recap)
4. [직전 장 close input 확인](/market-intel/daily/2026-04-22_evening-briefing-input)
5. [prediction workspace](/market-intel/research/prediction-workspace)

## 최근 usable 기록
### Session prep
- [2026-04-22_next-session-prep](/market-intel/daily/2026-04-22_next-session-prep)
- [2026-04-20_next-session-prep](/market-intel/daily/2026-04-20_next-session-prep)
- [2026-04-17_next-session-prep](/market-intel/daily/2026-04-17_next-session-prep)

### Validated recap
- [2026-04-22_top30_recap](/market-intel/daily/2026-04-22_top30_recap)
- [2026-04-21_top30_recap](/market-intel/daily/2026-04-21_top30_recap)
- [2026-04-20_top30_recap](/market-intel/daily/2026-04-20_top30_recap)

### Close input
- [2026-04-22_evening-briefing-input](/market-intel/daily/2026-04-22_evening-briefing-input)
- [2026-04-21_evening-briefing-input](/market-intel/daily/2026-04-21_evening-briefing-input)
- [2026-04-20_evening-briefing-input](/market-intel/daily/2026-04-20_evening-briefing-input)

### Supporting context
- [2026-04-16_news_recap](/market-intel/daily/2026-04-16_news_recap)
- [2026-04-16_high-signal-watchlist](/market-intel/daily/2026-04-16_high-signal-watchlist)
- [2026-04-15_us-to-kr-bridge](/market-intel/daily/2026-04-15_us-to-kr-bridge)
- [2026-04-16_us-to-kr-bridge-mythos-banks](/market-intel/daily/2026-04-16_us-to-kr-bridge-mythos-banks)

## 용어 정리
- `오늘 세션 prep`: 오늘 장 대응용 next-session-prep 문서
- `직전 장 validated recap`: 지금 세션 바로 이전 장의 검증 완료 TOP30 recap
- `직전 장 close input`: 직전 장 마감 뒤 남긴 evening briefing input
- `준비도`: 지금 시점에 필요한 핵심 3문서(prep / recap / close input)가 몇 개 준비됐는지
