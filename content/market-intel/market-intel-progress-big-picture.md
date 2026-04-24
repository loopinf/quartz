---
id: market-intel-progress-big-picture
note_type: workflow_status
created_at: 2026-04-17 22:26:00 KST
updated_at: 2026-04-24 10:34:00 KST
reviewer: 헤르메스(ㅎㅁ)
title: market-intel 진행상황 큰그림
summary: validated TOP30 ingest, evening briefing input/output, next-session-prep auto-fill, US→KR replay, high-signal, Quartz 노출까지 한 번에 보는 현재 진행상황 문서.
---

# market-intel 진행상황 큰그림

## TL;DR
현재 상태는 **"기초 ingest + 웹 노출 + replay/review 레이어까지는 이미 실제로 작동하고 있고, 이제 same-day source 안정화 / auto-chain blockage visibility / 예측용 path dataset 강화를 보강하는 단계"**다.

### 여기서 바로 이동
- [Market Intel Home](/market-intel/)
- [진행상황판](/market-intel/current-readiness-board)
- [최근 변경 로그](/market-intel/MARKET_INTEL_RECENT_CHANGES)
- [Daily workspace](/market-intel/daily/)
- [SOT](/market-intel/architecture/sot-market-intel-full-pipeline)

> 오늘 장전/장중 기준으로 필요한 문서가 실제로 준비됐는지 한눈에 보려면 [[current-readiness-board|current readiness board]]를 먼저 본다.
> 이 문서는 장기 진행상황/큰그림용이고, readiness board는 **현재 세션 운영 현황판**이다.

핵심 진척:
- validated TOP30 ingest가 `2026-04-16`, `2026-04-17` 같은 최근 날짜를 넘어 `2026-03-03`, `2026-03-04`, `2026-03-13` 등 과거 archive까지 확장되기 시작함
- `evening-briefing-input` / `next-session-prep` 레이어가 생겨 저녁 브리핑 운영 흐름이 분리되기 시작함
- `US -> KR bridge` / `predictive replay` / `질문 선택 workflow`가 추가되어 복기가 **예측 개선용 운영 레이어**로 승격됨
- high-signal 레이어가 별도 research lane으로 자리잡아, TOP30 기반 graph와 기술적 state/event 연구가 같이 굴러가기 시작함
- Quartz `8081`에서 index / progress / SOT 경로가 지금도 `200 OK`로 확인됨
- Hermes 코드 트랙은 새 대형 기능 추가보다는 gateway/approval 안정화 위주의 정리 단계에 있음

## 한눈에 보는 lane 맵

### 카드형 한눈 요약
```text
┌──────────┐
│ Source   │  same-day source 확보
└────┬─────┘
     ↓
┌──────────┐
│ Ingest   │  validated TOP30 ingest
└────┬─────┘
     ↓
┌──────────┐
│ Graph    │  event → entity → daily update
└────┬─────┘
     ├────────────→ Publish   : Quartz publish / browser verification
     ↓
┌──────────┐
│ Briefing │  input → output → next-session-prep
└────┬─────┘
     ↓
┌──────────┐
│ Replay   │  predictive replay / portfolio review
└────┬─────┘
     ↓
┌──────────┐
│ Research │  high-signal / breadth / path dataset
└──────────┘
```

### 상태만 바로 보기
```text
[작동 중]     Ingest / Graph / Publish / Briefing output / Prep auto-fill / Replay 초입 / Research 축
[보통]        Same-day source recovery / exact-date chain visibility
[보강 필요]   Source 안정화 + path dataset canonical화
```

### 각 카드 뜻
- **Source**: same-day source 확보
- **Ingest**: validated TOP30 ingest
- **Graph**: event → entity → daily update
- **Briefing**: evening-briefing-input → evening briefing output → next-session-prep
- **Replay**: predictive replay / portfolio review
- **Research**: high-signal / breadth / path dataset 강화
- **Publish**: Quartz publish / browser verification

---

## 1. 지금 실제로 돌아가고 있는 축

### A. Daily validated TOP30 ingest 축
대표 문서:
- [[2026-04-16_top30_recap]]
- [[2026-04-17_top30_recap]]
- [[2026-03-13_top30_recap]]
- [[2026-03-04_top30_recap]]
- [[2026-03-03_top30_recap]]

의미:
- raw archive를 그냥 붙여넣는 게 아니라 validated ingest로 통과시킴
- daily recap 생성
- 필요한 theme/event note 반영
- stock entity 누적 업데이트
- hash/state 기록으로 duplicate ingest 방지

현재 해석:
- 이 축은 이제 "개념 검증"이 아니라 **실제 운영 가능한 ingest lane**으로 넘어왔다
- 다만 same-day source acquisition이 매일 자동으로 안정적이진 않아서, acquisition 자체는 아직 강화가 필요하다

### B. Evening briefing input / next-session prep 축
대표 문서:
- [[2026-04-16_evening-briefing-input]]
- [[2026-04-17_evening-briefing-input]]
- [[2026-04-23_evening-briefing]]
- [[2026-04-24_next-session-prep]]
- [[evening-briefing-local-ingest-workflow]]

의미:
- 당일 마감 후 입력 레이어와 다음 세션 대응 레이어를 분리하기 시작함
- 금요일 마감 상태와 월요일 대응 준비를 같은 문서로 섞지 않도록 운영 규칙이 생김
- 이제 missing이면 exact-date `evening-briefing` / `next-session-prep`를 자동으로 메우는 cron까지 붙음
- readiness board에서 **자동 체인 전체와 현재 막힘 위치**를 같이 보이게 바뀜

현재 해석:
- input 레이어는 이미 usable
- output / prep도 exact-date auto-fill까지 연결돼 briefing lane의 뒷단 공백은 많이 줄었다
- 남은 핵심 약점은 여전히 same-day source acquisition과 close archive 안정성이다

### C. US -> KR translation / predictive replay 축
대표 문서:
- [[2026-04-15_us-to-kr-bridge]]
- [[2026-04-16_us-to-kr-bridge-mythos-banks]]
- [[replay-2026-04-14-nvidia-ising]]
- [[replay-2026-04-13-anthropic-mythos-banks]]
- [[predictive-replay-and-review-system]]
- [[us-event-question-selection-workflow]]
- [[ising-question-comparison-2026-04-19]]

의미:
- 복기를 단순 회고가 아니라 **한국장 전 추론력을 높이는 학습 레이어**로 공식화함
- 미국 원이벤트를 바로 설명형 질문 하나로 끝내지 않고, 질문 후보를 비교해 주 질문/보조 질문/버릴 질문을 정하는 workflow까지 추가됨

현재 해석:
- 이 축은 이제 명확한 v1 운영 레이어가 생겼음
- 아직 미국 single-name / ETF reaction set은 반자동 단계가 더 필요함

### D. High-signal technical state/event 축
대표 문서:
- [[pipeline-high-signal-big-picture]]
- [[2026-04-16_high-signal-watchlist]]
- [[high-signal-entry-timing-roadmap]]
- [[high-signal-entry-backtest-sample]]
- [[historical-high-signal-backfill-feasibility]]

의미:
- TOP30 기반 event/entity graph 외에, 별도의 신고가/근접/entry timing 연구 레이어가 실문서로 존재함
- `stock_prices.db` direct recompute를 minimum SOT로 두는 방향이 정리됨

현재 해석:
- 개념 설명을 넘어서 실제 watchlist / roadmap / sample backtest가 존재하는 단계
- 이제 핵심은 이 레이어를 replay/prediction 레이어와 더 잘 연결하는 것

---

## 2. 현재 live snapshot

2026-04-19 저녁 기준 확인된 대략적 규모:
- stock entity notes: **421개**
- daily notes: **29개**
- event notes: **108개**
- research notes: **9개**
- workflow notes: **8개**

이 숫자의 의미:
- 더 이상 "몇 개 샘플만 만든 상태"가 아니다
- 이미 **graph 자체는 누적 구조를 가진 실체**가 있다
- 이제 더 중요한 건 개수보다 **운영 일관성 / 예측용 재사용성 / 브리핑 품질**이다

---

## 3. 실제로 검증된 것

### A. same-day source 자체는 확보 가능함
검증 결과: **예**

실제 확인된 것:
- parser health가 healthy여도 same-day archive가 비어 있을 수 있었음
- 하지만 manual same-day parse를 돌리면 실제로 archive가 생성됨
- 즉 문제는 parser capability 자체보다 **자동 트리거 / 운영 안정성** 쪽이었음

결론:
- **받아오는 기능은 살아 있음**
- **제때 자동으로 들어오는지**를 별도로 점검해야 함

### B. Quartz 웹 노출은 지금도 살아 있음
실제 확인 결과:
- `http://127.0.0.1:8081/market-intel/` → `200 OK`
- `http://127.0.0.1:8081/market-intel/market-intel-progress-big-picture` → `200 OK`
- `http://127.0.0.1:8081/market-intel/architecture/sot-market-intel-full-pipeline` → `200 OK`

결론:
- **문서화 → sync/publish → 브라우저 확인** 루프는 지금도 살아 있다
- 따라서 진행상황 문서는 실제 운영용 대시보드 역할을 할 수 있다

### C. Hermes 코드 트랙은 안정화 위주로 움직이는 중
오늘 live repo 확인 결과:
- repo: `/Users/gbserver/.hermes/hermes-agent`
- uncommitted patch:
  - `gateway/platforms/telegram.py`
  - `scripts/whatsapp-bridge/package-lock.json`
- telegram approval callback 관련 테스트:
  - `python -m pytest tests/gateway/test_telegram_approval_buttons.py -q`
  - 결과: `10 passed`

해석:
- 현재 Hermes 쪽은 거대한 새 product lane 추가보다, **gateway / approval / tool/runtime 운영성 보강** 쪽이 중심이다
- 즉 market-intel product lane은 확장 중이고, Hermes code lane은 이를 뒷받침하는 안정화 페이즈에 가깝다

---

## 4. 아직 불완전한 것

### A. same-day source acquisition 자동 안정화
현재 문제:
- same-day archive가 자동으로 늦게 들어오거나 비는 경우가 있음
- parser health만으로는 same-day archive 존재를 보장할 수 없음

필요한 것:
1. same-day archive 존재 확인
2. 없으면 parser 강제 실행 또는 recovery flow 진입
3. 생성되면 validated ingest
4. 그 다음 briefing input/output 생성

### B. `evening-briefing-input`은 생겼지만 `evening-briefing` output은 아직 초기 단계
지금은:
- `..._evening-briefing-input.md` = 입력 레이어
- `..._next-session-prep.md` = 다음 세션 대응 레이어 일부

앞으로 필요한 것:
- `..._evening-briefing.md` = 실제 사용자용 요약 출력 레이어
- 입력/출력 분리 유지한 채, output note를 standard format으로 만들기

### C. replay는 생겼지만 US reaction set 반자동화는 아직 약함
현재 문제:
- 원이벤트 source와 KR translation replay는 문서화되기 시작했음
- 하지만 미국 single-name / ETF reaction set은 아직 수작업 의존도가 높음

필요한 것:
- event type별 starter watchlist
- 반자동 초안 생성
- data completeness 표시

### D. prediction-oriented multi-horizon path dataset는 아직 1급 canonical lane이 아님
현재 문제:
- replay, success case, high-signal, continuity 패턴은 생겼음
- 하지만 이를 `D+1 / D+2 / within_5d / delayed_spread / one_day_fade / reignition` 같은 공통 label로 묶는 상위 canonical dataset는 아직 약함

필요한 것:
- state / event / path 3층 구분
- replay와 high-signal을 같은 outcome vocabulary로 연결

---

## 5. 지금 큰그림에서 어디까지 와 있나
정리하면 단계는 이렇다.

### Phase 1 — raw ingest / graph 구축
상당 부분 완료
- TOP30 → recap/event/entity 구조 작동
- stock entity 중심 누적 구조 작동
- 과거 archive backfill ingest도 시작됨

### Phase 2 — daily briefing input / next-session prep 축
시작 완료
- 날짜별 input note 생성 시작
- 금요일/주말/다음 세션 분리 규칙 생김

### Phase 3 — US -> KR replay / review 축
시작 완료
- bridge note + replay note + 질문 선택 workflow까지 생김
- 예측 개선용 review loop가 문서화됨

### Phase 4 — high-signal technical state/event 축
작동 중
- watchlist / roadmap / sample backtest가 존재
- 별도의 research lane으로 이미 분리됨

### Phase 5 — same-day acquisition 안정화 + final output 자동화 + path dataset 강화
현재 핵심 진행 구간
- same-day 확보 자동 안정화
- briefing output note 정식화
- replay / high-signal / success case를 multi-horizon path dataset 관점으로 묶기
- `research/multi-horizon-path-dataset-schema.md`로 event/state/path 분리와 5거래일 observation vocabulary를 최소 공통 schema로 고정하기

즉 지금 상태는:
**"저장 구조를 만드는 단계는 이미 지났고, 이제 운영 일관성 / 브리핑 산출물 / 예측 학습 레이어를 강화하는 단계"**다.

---

## 6. 지금 웹에서 어디서 보면 되나

### Start here
- [MARKET_INTEL_RECENT_CHANGES](./market-intel/MARKET_INTEL_RECENT_CHANGES)
- [index](./market-intel/index)
- [market-intel-progress-big-picture](./market-intel/market-intel-progress-big-picture)

### architecture / 큰그림
- [sot-market-intel-full-pipeline](./market-intel/architecture/sot-market-intel-full-pipeline)
- [pipeline-high-signal-big-picture](./market-intel/architecture/pipeline-high-signal-big-picture)
- [audit-jmkr-top30-archive-pipeline](./market-intel/architecture/audit-jmkr-top30-archive-pipeline)

### workflow / operations
- [predictive-replay-and-review-system](./market-intel/workflows/predictive-replay-and-review-system)
- [us-event-question-selection-workflow](./market-intel/workflows/us-event-question-selection-workflow)
- [evening-briefing-local-ingest-workflow](./market-intel/workflows/evening-briefing-local-ingest-workflow)
- [market-intel-information-architecture-roadmap](./market-intel/workflows/market-intel-information-architecture-roadmap)
- [market-intel-reorg-execution-plan](./market-intel/workflows/market-intel-reorg-execution-plan)

### recent daily / replay
- [2026-04-17_top30_recap](./market-intel/daily/2026-04-17_top30_recap)
- [2026-04-17_evening-briefing-input](./market-intel/daily/2026-04-17_evening-briefing-input)
- [2026-04-20_next-session-prep](./market-intel/daily/2026-04-20_next-session-prep)
- [2026-04-15_us-to-kr-bridge](./market-intel/daily/2026-04-15_us-to-kr-bridge)
- [replay-2026-04-14-nvidia-ising](./market-intel/research/replay-2026-04-14-nvidia-ising)
- [replay-2026-04-13-anthropic-mythos-banks](./market-intel/research/replay-2026-04-13-anthropic-mythos-banks)

### high-signal / research
- [2026-04-16_high-signal-watchlist](./market-intel/daily/2026-04-16_high-signal-watchlist)
- [high-signal-entry-timing-roadmap](./market-intel/research/high-signal-entry-timing-roadmap)
- [high-signal-entry-backtest-sample](./market-intel/research/high-signal-entry-backtest-sample)
- [historical-high-signal-backfill-feasibility](./market-intel/research/historical-high-signal-backfill-feasibility)

---

## 7. 다음 우선순위
1. **same-day archive acquisition 안정화**
2. **`evening-briefing-input` → `evening-briefing` output note 정식화**
3. **US reaction set 반자동 초안 레이어 강화**
4. **replay / high-signal / success case를 묶는 multi-horizon path dataset vocabulary 정리**
5. **Hermes 코드 트랙의 현재 변경분(telegram approval hardening 등) 정리 및 커밋 분리**

---

## One-line status
**지금은 "기초 graph + 웹 노출 + replay 레이어는 이미 실제로 돌아가고 있고, 다음 핵심은 same-day source 안정화 / 브리핑 output / multi-horizon prediction dataset 강화" 단계다.**
