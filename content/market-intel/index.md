---
title: Market Intel Home
summary: 현재 세션 필수 문서가 자동으로 준비됐는지 먼저 확인하고, fallback과 다음 액션을 바로 여는 운영 홈.
---

# Market Intel Home

## 한눈에 보기 (<span data-mi-current-label="1" data-mi-current-date="2026-04-29" data-mi-current-phase="장중">2026-04-29 KST, 수요일 장중</span>)
- 실시간 KST 기준: <span id="market-intel-now-label" data-mi-current-label="1">2026-04-29 KST, 수요일 장중</span>
- 현재 세션: `2026-04-29` / `장중`
- 준비도: `완료` = `3 / 3`
- recovery-needed: `없음`
- 최근 변경 로그: [MARKET_INTEL_RECENT_CHANGES](/market-intel/MARKET_INTEL_RECENT_CHANGES)

## 오늘 바로 열기
1. [진행상황판](/market-intel/current-readiness-board)
2. [오늘 세션 prep](/market-intel/daily/2026-04-29_next-session-prep)
3. [직전 장 validated recap](/market-intel/daily/2026-04-28_top30_recap)
4. [직전 장 close input](/market-intel/daily/2026-04-28_evening-briefing-input)
5. [prediction workspace](/market-intel/research/prediction-workspace)

## 핵심 문서 상태
- 오늘 세션 prep: `READY` — [2026-04-29_next-session-prep](/market-intel/daily/2026-04-29_next-session-prep)
- 직전 장 validated recap: `READY` — [2026-04-28_top30_recap](/market-intel/daily/2026-04-28_top30_recap)
- 직전 장 close input: `READY` — [2026-04-28_evening-briefing-input](/market-intel/daily/2026-04-28_evening-briefing-input)

## 최신 usable 문서
- prep: [2026-04-29_next-session-prep](/market-intel/daily/2026-04-29_next-session-prep)
- validated recap: [2026-04-28_top30_recap](/market-intel/daily/2026-04-28_top30_recap)
- close input: [2026-04-28_evening-briefing-input](/market-intel/daily/2026-04-28_evening-briefing-input)
- evening briefing output: [2026-04-28_evening-briefing](/market-intel/daily/2026-04-28_evening-briefing)
- same-day source archive: `WAITING`

<details><summary>세부 상태 / 용어 / 큰그림 펼치기</summary>

### 자동 생성 체인
### 자동 체인 개요
1. `same-day source recovery/watch` — 장마감 전후 archive 확보/복구 감시 (`jmkr-same-day-auto-recovery-close-window`, `jmkr-top30-same-day-late-check-and-ingest`)
2. `validated recap ingest` — close archive validation 통과 시 exact-date `*_top30_recap` 생성
3. `evening-briefing-input` — 장마감 입력 레이어 생성 (`local-only-evening-briefing-input`)
4. `evening briefing output` — input을 decision-oriented output note로 자동 변환 (`market-intel-evening-briefing-auto-create`, 18:50 KST)
5. `next-session-prep` — 직전 장 문서를 바탕으로 다음 세션 prep 자동 보강 (`market-intel-next-session-prep-auto-create`, 06:05 KST)
6. `Quartz sync/build` — `sync-market-intel.sh`가 entrypoint/readiness를 다시 계산해 8081에 반영

### 현재 체인 상태
- `WAITING` 당일 source archive — 장전/장중에는 아직 없어도 정상
- `READY` 직전 장 validated recap — 2026-04-28_top30_recap
- `READY` 직전 장 close input — 2026-04-28_evening-briefing-input
- `READY` final evening briefing output — 2026-04-28_evening-briefing
- `READY` next-session prep — 2026-04-29_next-session-prep
- 현재 막힘: prior-close -> briefing -> prep 문서 체인은 현재 기준으로 이어져 있다. 남은 불확실성은 same-day source/archive 쪽이다.

### 왜 이렇게 보나
- 수동으로 "어제 문서 열어보자"가 아니라, **현재 시점에 필요한 exact-date 문서가 있는지 자동으로 확인**해야 한다.
- exact-date 문서가 없으면 fallback은 보여주되, 준비 완료로 취급하지 않는다.
- `직전`은 직전 작업 문서가 아니라 **현재 세션 바로 직전 거래일 기준**이다.

### 용어 정리
- `필수 문서`: 현재 세션 시점에 exact-date로 준비돼 있어야 하는 문서
- `최신 fallback`: exact-date 문서가 없을 때 참고 가능한 가장 최근 usable 문서
- `직전 장`: 단순히 최근에 작업한 문서가 아니라, 현재 세션 바로 이전 거래일 기준
- `준비도`: prep / validated recap / close input 3개 중 몇 개가 exact-date 기준으로 준비됐는지

### 큰그림 / 작업공간
- [진행상황판](/market-intel/current-readiness-board)
- [daily workspace](/market-intel/daily/)
- [prediction workspace](/market-intel/research/prediction-workspace)
- [portfolio pilot review dashboard](/market-intel/research/portfolio-pilot-review-dashboard)
- [predictive replay and review system](/market-intel/workflows/predictive-replay-and-review-system)
- [market-intel progress big picture](/market-intel/market-intel-progress-big-picture)
- [SOT — market-intel full pipeline](/market-intel/architecture/sot-market-intel-full-pipeline)

</details>

<details><summary>archive / recovery 상세 펼치기</summary>

## recovery-needed 체크
- recovery-needed 상태 아님

## latest doc detail
- 최신 prep: [2026-04-29_next-session-prep](/market-intel/daily/2026-04-29_next-session-prep)
- 최신 validated recap: [2026-04-28_top30_recap](/market-intel/daily/2026-04-28_top30_recap)
- 최신 close input: [2026-04-28_evening-briefing-input](/market-intel/daily/2026-04-28_evening-briefing-input)
- 최신 evening briefing output: [2026-04-28_evening-briefing](/market-intel/daily/2026-04-28_evening-briefing)
- same-day archive path: `/Users/gbserver/repos/jmkr_kj/data/daily/archive/2026-04-29.json` (missing yet)

</details>
