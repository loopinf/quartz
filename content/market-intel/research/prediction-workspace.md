---
title: prediction workspace
summary: 오늘 세션 prep 준비 여부를 먼저 확인한 뒤 예측 후보와 복기로 이어지는 작업공간.
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
1. [daily workspace에서 오늘 세션 prep 상태 확인](/market-intel/daily/)
2. [portfolio pilot review dashboard](/market-intel/research/portfolio-pilot-review-dashboard)
3. [portfolio pilot batch — additional samples](/market-intel/research/portfolio-pilot-batch-additional-samples)
4. [predictive replay and review system](/market-intel/workflows/predictive-replay-and-review-system)
- latest prep fallback: [2026-04-22_next-session-prep](/market-intel/daily/2026-04-22_next-session-prep)

## 먼저 확인
- [daily workflow](/market-intel/daily/)
- [직전 장 validated recap — 2026-04-22_top30_recap](/market-intel/daily/2026-04-22_top30_recap)
- [직전 장 close input — 2026-04-22_evening-briefing-input](/market-intel/daily/2026-04-22_evening-briefing-input)

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
