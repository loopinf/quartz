---
title: current readiness board
summary: 지금 세션 기준으로 필요한 핵심 daily 문서가 자동으로 확인됐는지 한눈에 보는 현황판.
---

# Current Readiness Board

## 지금 세션 자동 판정 (<span data-mi-current-label="1" data-mi-current-date="2026-04-24" data-mi-current-phase="장중">2026-04-24 KST, 금요일 장중</span>)
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
- 현재 세션: `2026-04-24` / `장중`
- 상태판 기준: `오늘 장전 준비 상태`
- 준비도: `완료` = `3 / 3`
- 이 현황판은 sync/build 때 자동 생성된다.

## 자동 확인 결과
- `READY` 오늘 세션 prep: [2026-04-24_next-session-prep](/market-intel/daily/2026-04-24_next-session-prep)
  - 오늘 세션용 prep가 2026-04-24_next-session-prep로 준비되어 있다.
- `READY` 직전 장 validated recap: [2026-04-23_top30_recap](/market-intel/daily/2026-04-23_top30_recap)
  - 직전 장 기준 validated recap가 2026-04-23_top30_recap로 준비되어 있다.
- `READY` 직전 장 close input: [2026-04-23_evening-briefing-input](/market-intel/daily/2026-04-23_evening-briefing-input)
  - 직전 장 close input이 2026-04-23_evening-briefing-input로 준비되어 있다.

## 운영 추가 체크
- `READY` final evening briefing output: [2026-04-23_evening-briefing](/market-intel/daily/2026-04-23_evening-briefing)
  - 현재 세션 기준 briefing output이 2026-04-23_evening-briefing로 존재한다.
- `READY` required close archive: `/Users/gbserver/repos/jmkr_kj/data/daily/archive/2026-04-23.json`
  - 현재 세션에 필요한 close archive가 존재하고 validation 통과: market_close + is_empty=false + TOP30 문구 + 번호 라인 26개
- `WAITING` same-day source archive: `/Users/gbserver/repos/jmkr_kj/data/daily/archive/2026-04-24.json`
  - 장전/장중에는 당일 archive가 아직 없어도 정상일 수 있다. close 이후 READY/RECOVERY_NEEDED로 봐야 한다.
- `READY` telegram parser health
  - parser health=healthy, 직전 장 기준 last_update=2026-04-23 18:41 KST

## 자동 확인이 실제로 들어가 있나
- 자동 확인 트리거: `~/market-intel-site/scripts/sync-market-intel.sh`
- 실제 판정 로직: `~/market-intel-site/scripts/update_market_intel_entrypoints.py`
- 자동 판정 대상:
  - `오늘/다음 세션 prep` = exact-date match
  - `직전 장 validated recap` = exact-date + `validation_status: validated`
  - `직전 장 close input` = exact-date match
  - `final evening briefing output` = exact-date match
  - `same-day source archive` = phase-aware check (`장전/장중`에는 WAITING 가능, `장후`에는 READY/RECOVERY_NEEDED)
- 현재 반영 위치: `/`, `/market-intel/`, `/market-intel/daily/`, `/market-intel/research/prediction-workspace`, `/market-intel/current-readiness-board`
- 한계: 이 확인은 **sync/build 시점 자동화**다. 즉 문서 존재 여부를 자동 판정해 표시하지만, 별도 cron 없이 매분 실시간 재판정하는 구조는 아니다.

## 확인 기준
- prep target: `2026-04-24_next-session-prep`
- validated recap target: `2026-04-23_top30_recap`
- close input target: `2026-04-23_evening-briefing-input`
- briefing output target: `2026-04-23_evening-briefing`
- same-day archive target: `/Users/gbserver/repos/jmkr_kj/data/daily/archive/2026-04-24.json`
- fallback은 참고용이지 readiness 충족으로 보지 않음

## 최신 usable 문서
- 최신 prep: [2026-04-24_next-session-prep](/market-intel/daily/2026-04-24_next-session-prep)
- 최신 validated recap: [2026-04-23_top30_recap](/market-intel/daily/2026-04-23_top30_recap)
- 최신 close input: [2026-04-23_evening-briefing-input](/market-intel/daily/2026-04-23_evening-briefing-input)
- 최신 evening briefing output: [2026-04-23_evening-briefing](/market-intel/daily/2026-04-23_evening-briefing)
- same-day archive path: `/Users/gbserver/repos/jmkr_kj/data/daily/archive/2026-04-24.json` (missing yet)

## 자동 생성 체인 / 현재 막힘 위치
### 자동 체인 개요
1. `same-day source recovery/watch` — 장마감 전후 archive 확보/복구 감시 (`jmkr-same-day-auto-recovery-close-window`, `jmkr-top30-same-day-late-check-and-ingest`)
2. `validated recap ingest` — close archive validation 통과 시 exact-date `*_top30_recap` 생성
3. `evening-briefing-input` — 장마감 입력 레이어 생성 (`local-only-evening-briefing-input`)
4. `evening briefing output` — input을 decision-oriented output note로 자동 변환 (`market-intel-evening-briefing-auto-create`, 18:50 KST)
5. `next-session-prep` — 직전 장 문서를 바탕으로 다음 세션 prep 자동 보강 (`market-intel-next-session-prep-auto-create`, 06:05 KST)
6. `Quartz sync/build` — `sync-market-intel.sh`가 entrypoint/readiness를 다시 계산해 8081에 반영

### 현재 체인 상태
- `WAITING` 당일 source archive — 장전/장중에는 아직 없어도 정상
- `READY` 직전 장 validated recap — 2026-04-23_top30_recap
- `READY` 직전 장 close input — 2026-04-23_evening-briefing-input
- `READY` final evening briefing output — 2026-04-23_evening-briefing
- `READY` next-session prep — 2026-04-24_next-session-prep
- 현재 막힘: prior-close -> briefing -> prep 문서 체인은 현재 기준으로 이어져 있다. 남은 불확실성은 same-day source/archive 쪽이다.

## 이 페이지를 어떻게 써야 하나
- 이 페이지는 **지금 세션에 필요한 문서가 최신인지**를 먼저 확인하는 운영 현황판이다.
- `MISSING`이면 target 문서가 아직 없다는 뜻이고, fallback은 참고용일 뿐 target을 대체한 것으로 간주하지 않는다.
- 장기 로드맵/큰그림은 [market-intel progress big picture](/market-intel/market-intel-progress-big-picture)에서 본다.
- 실제 작업 시작은 [daily workspace](/market-intel/daily/)로 들어간다.

## 다음 액션
1. [진행상황판에서 exact-date readiness 확인](/market-intel/current-readiness-board)
2. [오늘 세션 prep 열기](/market-intel/daily/2026-04-24_next-session-prep)
3. [직전 장 validated recap](/market-intel/daily/2026-04-23_top30_recap)
4. [직전 장 close input](/market-intel/daily/2026-04-23_evening-briefing-input)
5. [prediction workspace](/market-intel/research/prediction-workspace)

## recovery-needed 체크
- recovery-needed 상태 아님

## 관련 페이지
- [Market Intel Home](/market-intel/)
- [daily workspace](/market-intel/daily/)
- [prediction workspace](/market-intel/research/prediction-workspace)
- [market-intel progress big picture](/market-intel/market-intel-progress-big-picture)
