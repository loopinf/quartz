---
title: Market Intel Start
summary: 8081 루트 시작점. 현재 세션에 필요한 문서가 exact-date 기준으로 준비됐는지 자동으로 먼저 보여준다.
---

# Market Intel Start

## 지금 준비 상태 (<span data-mi-current-label="1" data-mi-current-date="2026-04-23" data-mi-current-phase="장중">2026-04-23 KST, 목요일 장중</span>)
- 실시간 KST 기준: <span id="market-intel-now-label">2026-04-23 KST, 목요일 장중</span>
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
- 현재 세션: `2026-04-23` / `장중`
- 오늘 장전 준비 상태: `완료` = `3 / 3`
- [진행상황판 바로 열기](/market-intel/current-readiness-board)
- 자동 확인 기준: `오늘/다음 세션 prep`, `직전 장 validated recap`, `직전 장 close input`이 exact-date로 있는지 확인

- `READY` 오늘 세션 prep: [2026-04-23_next-session-prep](/market-intel/daily/2026-04-23_next-session-prep)
  - 오늘 세션용 prep가 2026-04-23_next-session-prep로 준비되어 있다.
- `READY` 직전 장 validated recap: [2026-04-22_top30_recap](/market-intel/daily/2026-04-22_top30_recap)
  - 직전 장 기준 validated recap가 2026-04-22_top30_recap로 준비되어 있다.
- `READY` 직전 장 close input: [2026-04-22_evening-briefing-input](/market-intel/daily/2026-04-22_evening-briefing-input)
  - 직전 장 close input이 2026-04-22_evening-briefing-input로 준비되어 있다.

## 지금 바로 할 일
1. [진행상황판에서 exact-date readiness 확인](/market-intel/current-readiness-board)
2. [오늘 세션 prep 열기](/market-intel/daily/2026-04-23_next-session-prep)
3. [직전 장 validated recap](/market-intel/daily/2026-04-22_top30_recap)
4. [직전 장 close input](/market-intel/daily/2026-04-22_evening-briefing-input)
5. [prediction workspace](/market-intel/research/prediction-workspace)

## recovery-needed 체크
- recovery-needed 상태 아님

## 최신 usable 문서
- 최신 prep: [2026-04-23_next-session-prep](/market-intel/daily/2026-04-23_next-session-prep)
- 최신 validated recap: [2026-04-22_top30_recap](/market-intel/daily/2026-04-22_top30_recap)
- 최신 close input: [2026-04-22_evening-briefing-input](/market-intel/daily/2026-04-22_evening-briefing-input)
- 최신 evening briefing output: [2026-04-22_evening-briefing](/market-intel/daily/2026-04-22_evening-briefing)
- same-day archive path: `/Users/gbserver/repos/jmkr_kj/data/daily/archive/2026-04-23.json` (missing yet)

## 용어 정리
- `필수 문서`: 현재 세션 시점에 exact-date로 준비돼 있어야 하는 문서
- `최신 fallback`: exact-date 문서가 없을 때 참고 가능한 가장 최근 usable 문서
- `직전 장`: 단순히 최근에 작업한 문서가 아니라, 현재 세션 바로 이전 거래일 기준
- `준비도`: prep / validated recap / close input 3개 중 몇 개가 exact-date 기준으로 준비됐는지

## 섹션 바로가기
- [Market Intel home](/market-intel/)
- [진행상황판](/market-intel/current-readiness-board)
- [daily workspace](/market-intel/daily/)
- [prediction workspace](/market-intel/research/prediction-workspace)
- [최근 변경 로그](/market-intel/MARKET_INTEL_RECENT_CHANGES)
- [큰그림](/market-intel/market-intel-progress-big-picture)
