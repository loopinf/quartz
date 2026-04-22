---
title: Market Intel Home
summary: 오늘 세션 준비 상태를 먼저 보여주고, 필요한 문서가 최신인지 바로 확인하게 하는 운영 홈.
---

# Market Intel Home

## 오늘 준비 상태 (<span data-mi-current-label="1" data-mi-current-date="2026-04-23" data-mi-current-phase="장전">2026-04-23 KST, 목요일 장전</span>)
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
- 현재 세션: `2026-04-23` / `장전`
- 준비도: `partial` = `2 / 3 ready`
- 최근 변경 로그: [MARKET_INTEL_RECENT_CHANGES](/market-intel/MARKET_INTEL_RECENT_CHANGES)

- `MISSING` 오늘 세션 prep: target `2026-04-23_next-session-prep`
  - target은 2026-04-23_next-session-prep인데 아직 없다. 최신 fallback은 2026-04-22_next-session-prep이지만 오늘 세션용 문서는 아직 없다.
  - latest fallback: [2026-04-22_next-session-prep](/market-intel/daily/2026-04-22_next-session-prep)
- `READY` 직전 장 validated recap: [2026-04-22_top30_recap](/market-intel/daily/2026-04-22_top30_recap)
  - 현재 세션 바로 직전 장 기준 validated recap은 2026-04-22_top30_recap이다.
- `READY` 직전 장 close input: [2026-04-22_evening-briefing-input](/market-intel/daily/2026-04-22_evening-briefing-input)
  - 현재 세션 직전 장 close input은 2026-04-22_evening-briefing-input이다.

## 오늘 바로 할 일
1. [daily workspace에서 오늘 세션 prep 상태 확인](/market-intel/daily/)
2. fallback으로 [2026-04-22_next-session-prep](/market-intel/daily/2026-04-22_next-session-prep) 참고
3. [직전 장 validated recap 확인](/market-intel/daily/2026-04-22_top30_recap)
4. [직전 장 close input 확인](/market-intel/daily/2026-04-22_evening-briefing-input)
5. [prediction workspace](/market-intel/research/prediction-workspace)

## 왜 이렇게 보나
- index에서는 **지금 필요한 문서가 최신인지**를 먼저 확인해야 한다.
- `직전`은 "직전 작업한 문서"가 아니라 **현재 세션 바로 직전 장 기준 문서**를 뜻한다.
- 오늘 prep이 없으면 fallback을 보여주되, `MISSING`으로 명확히 남긴다.

## 용어 정리
- `오늘 세션 prep`: 오늘 장 대응용 next-session-prep 문서
- `직전 장 validated recap`: 지금 세션 바로 이전 장의 검증 완료 TOP30 recap
- `직전 장 close input`: 직전 장 마감 뒤 남긴 evening briefing input
- `준비도`: 지금 시점에 필요한 핵심 3문서(prep / recap / close input)가 몇 개 준비됐는지

## 큰그림 / 작업공간
- [daily workspace](/market-intel/daily/)
- [prediction workspace](/market-intel/research/prediction-workspace)
- [portfolio pilot review dashboard](/market-intel/research/portfolio-pilot-review-dashboard)
- [predictive replay and review system](/market-intel/workflows/predictive-replay-and-review-system)
- [market-intel progress big picture](/market-intel/market-intel-progress-big-picture)
- [SOT — market-intel full pipeline](/market-intel/architecture/sot-market-intel-full-pipeline)
