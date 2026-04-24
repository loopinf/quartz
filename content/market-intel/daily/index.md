---
title: daily workspace
summary: 현재 세션 필수 daily 문서가 exact-date 기준으로 준비됐는지 한 번에 확인하는 허브.
---

# Daily Workspace

## 오늘 장전 준비 상태 (<span data-mi-current-label="1" data-mi-current-date="2026-04-24" data-mi-current-phase="장중">2026-04-24 KST, 금요일 장중</span>)
- 실시간 KST 기준: <span id="market-intel-now-label">2026-04-24 KST, 금요일 장중</span>
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
- 준비도: `완료` = `3 / 3`
- [진행상황판](/market-intel/current-readiness-board)
- 자동 확인 순서: `prep → validated recap → close input`

- `READY` 오늘 세션 prep: [2026-04-24_next-session-prep](/market-intel/daily/2026-04-24_next-session-prep)
  - 오늘 세션용 prep가 2026-04-24_next-session-prep로 준비되어 있다.
- `READY` 직전 장 validated recap: [2026-04-23_top30_recap](/market-intel/daily/2026-04-23_top30_recap)
  - 직전 장 기준 validated recap가 2026-04-23_top30_recap로 준비되어 있다.
- `READY` 직전 장 close input: [2026-04-23_evening-briefing-input](/market-intel/daily/2026-04-23_evening-briefing-input)
  - 직전 장 close input이 2026-04-23_evening-briefing-input로 준비되어 있다.

## recovery-needed 체크
- recovery-needed 상태 아님

## 오늘 바로 열 것
1. [진행상황판에서 exact-date readiness 확인](/market-intel/current-readiness-board)
2. [오늘 세션 prep 열기](/market-intel/daily/2026-04-24_next-session-prep)
3. [직전 장 validated recap](/market-intel/daily/2026-04-23_top30_recap)
4. [직전 장 close input](/market-intel/daily/2026-04-23_evening-briefing-input)
5. [prediction workspace](/market-intel/research/prediction-workspace)

## 최근 usable 기록
### Session prep
- [2026-04-24_next-session-prep](/market-intel/daily/2026-04-24_next-session-prep)
- [2026-04-23_next-session-prep](/market-intel/daily/2026-04-23_next-session-prep)
- [2026-04-22_next-session-prep](/market-intel/daily/2026-04-22_next-session-prep)
- [2026-04-21_next-session-prep](/market-intel/daily/2026-04-21_next-session-prep)

### Validated recap
- [2026-04-23_top30_recap](/market-intel/daily/2026-04-23_top30_recap)
- [2026-04-22_top30_recap](/market-intel/daily/2026-04-22_top30_recap)
- [2026-04-21_top30_recap](/market-intel/daily/2026-04-21_top30_recap)
- [2026-04-20_top30_recap](/market-intel/daily/2026-04-20_top30_recap)

### Close input
- [2026-04-23_evening-briefing-input](/market-intel/daily/2026-04-23_evening-briefing-input)
- [2026-04-22_evening-briefing-input](/market-intel/daily/2026-04-22_evening-briefing-input)
- [2026-04-21_evening-briefing-input](/market-intel/daily/2026-04-21_evening-briefing-input)
- [2026-04-20_evening-briefing-input](/market-intel/daily/2026-04-20_evening-briefing-input)

## 용어 정리
- `필수 문서`: 현재 세션 시점에 exact-date로 준비돼 있어야 하는 문서
- `최신 fallback`: exact-date 문서가 없을 때 참고 가능한 가장 최근 usable 문서
- `직전 장`: 단순히 최근에 작업한 문서가 아니라, 현재 세션 바로 이전 거래일 기준
- `준비도`: prep / validated recap / close input 3개 중 몇 개가 exact-date 기준으로 준비됐는지
