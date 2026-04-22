---
title: prediction workspace
summary: 예측 후보 검토 전에 현재 세션 준비 상태를 먼저 확인하는 prediction 허브.
---

# Prediction Workspace

## 오늘 바로 할 일 (<span data-mi-current-label="1" data-mi-current-date="2026-04-23" data-mi-current-phase="장전">2026-04-23 KST, 목요일 장전</span>)
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
- 먼저 [진행상황판](/market-intel/current-readiness-board)에서 exact-date readiness 확인
1. [2026-04-22_next-session-prep](/market-intel/daily/2026-04-22_next-session-prep)
2. [portfolio pilot review dashboard](/market-intel/research/portfolio-pilot-review-dashboard)
3. [portfolio pilot batch — additional samples](/market-intel/research/portfolio-pilot-batch-additional-samples)
4. [predictive replay and review system](/market-intel/workflows/predictive-replay-and-review-system)

## 먼저 확인
- [daily workspace](/market-intel/daily/)
- [validated recap — 2026-04-22_top30_recap](/market-intel/daily/2026-04-22_top30_recap)
- [close input — 2026-04-22_evening-briefing-input](/market-intel/daily/2026-04-22_evening-briefing-input)

## 용어 정리
- 예측 후보 검토 전에 **현재 세션 prep이 exact-date로 있는지** 먼저 확인해야 한다.
- exact-date prep이 없으면 fallback prep을 보더라도 상태는 `준비 완료`가 아니다.
- replay / dashboard는 readiness 확인 뒤 들어가는 보조 작업공간이다.
