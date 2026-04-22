---
title: current readiness board
summary: 지금 세션 기준으로 필요한 핵심 daily 문서가 자동으로 확인됐는지 한눈에 보는 현황판.
---

# Current Readiness Board

## 지금 세션 자동 판정 (<span data-mi-current-label="1" data-mi-current-date="2026-04-23" data-mi-current-phase="장전">2026-04-23 KST, 목요일 장전</span>)
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
- 상태판 기준: `오늘 장전 준비 상태`
- 준비도: `부분준비` = `2 / 3`
- 이 현황판은 sync/build 때 자동 생성된다.

## 자동 확인 결과
- `MISSING` 오늘 세션 prep: 필요 문서 `2026-04-23_next-session-prep`
  - 필요 문서는 2026-04-23_next-session-prep인데 아직 없다.
  - 최신 fallback: [2026-04-22_next-session-prep](/market-intel/daily/2026-04-22_next-session-prep)
- `READY` 직전 장 validated recap: [2026-04-22_top30_recap](/market-intel/daily/2026-04-22_top30_recap)
  - 직전 장 기준 validated recap가 2026-04-22_top30_recap로 준비되어 있다.
- `READY` 직전 장 close input: [2026-04-22_evening-briefing-input](/market-intel/daily/2026-04-22_evening-briefing-input)
  - 직전 장 close input이 2026-04-22_evening-briefing-input로 준비되어 있다.

## 자동 확인이 실제로 들어가 있나
- 자동 확인 트리거: `~/market-intel-site/scripts/sync-market-intel.sh`
- 실제 판정 로직: `~/market-intel-site/scripts/update_market_intel_entrypoints.py`
- 자동 판정 대상:
  - `오늘/다음 세션 prep` = exact-date match
  - `직전 장 validated recap` = exact-date + `validation_status: validated`
  - `직전 장 close input` = exact-date match
- 현재 반영 위치: `/`, `/market-intel/`, `/market-intel/daily/`, `/market-intel/research/prediction-workspace`, `/market-intel/current-readiness-board`
- 한계: 이 확인은 **sync/build 시점 자동화**다. 즉 문서 존재 여부를 자동 판정해 표시하지만, 별도 cron 없이 매분 실시간 재판정하는 구조는 아니다.

## 확인 기준
- prep target: `2026-04-23_next-session-prep`
- validated recap target: `2026-04-22_top30_recap`
- close input target: `2026-04-22_evening-briefing-input`
- fallback은 참고용이지 readiness 충족으로 보지 않음

## 최신 usable 문서
- 최신 prep: [2026-04-22_next-session-prep](/market-intel/daily/2026-04-22_next-session-prep)
- 최신 validated recap: [2026-04-22_top30_recap](/market-intel/daily/2026-04-22_top30_recap)
- 최신 close input: [2026-04-22_evening-briefing-input](/market-intel/daily/2026-04-22_evening-briefing-input)

## 이 페이지를 어떻게 써야 하나
- 이 페이지는 **지금 세션에 필요한 문서가 최신인지**를 먼저 확인하는 운영 현황판이다.
- `MISSING`이면 target 문서가 아직 없다는 뜻이고, fallback은 참고용일 뿐 target을 대체한 것으로 간주하지 않는다.
- 장기 로드맵/큰그림은 [market-intel progress big picture](/market-intel/market-intel-progress-big-picture)에서 본다.
- 실제 작업 시작은 [daily workspace](/market-intel/daily/)로 들어간다.

## 다음 액션
1. [진행상황판에서 exact-date readiness 확인](/market-intel/current-readiness-board)
2. [fallback prep 확인](/market-intel/daily/2026-04-22_next-session-prep)
3. [직전 장 validated recap](/market-intel/daily/2026-04-22_top30_recap)
4. [직전 장 close input](/market-intel/daily/2026-04-22_evening-briefing-input)
5. [prediction workspace](/market-intel/research/prediction-workspace)

## 관련 페이지
- [Market Intel Home](/market-intel/)
- [daily workspace](/market-intel/daily/)
- [prediction workspace](/market-intel/research/prediction-workspace)
- [market-intel progress big picture](/market-intel/market-intel-progress-big-picture)
