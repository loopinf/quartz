---
id: 2026-05-11-daehan-optic-entry-scenario-evaluation-framework
note_type: research_framework
created_at: 2026-05-11 23:12:00 KST
updated_at: 2026-05-12 08:33:55 KST
reviewer: 헤르메스(ㅎㅁ)
title: 대한광통신 진입 시나리오 평가 프레임워크
summary: 대한광통신/광통신장비 군집에서 첫 급등 추격보다 pullback→재돌파, 동종군 확산 후 leader 복귀 같은 아이디어를 어떻게 테스트 가능한 시나리오로 바꿀지 정리한 연구 프레임워크.
linked_stocks:
  - "[[market-intel/entities/stocks/대한광통신|대한광통신]]"
linked_events:
  - "[[market-intel/events/2026-04-17_광통신장비_모멘텀|2026-04-17 광통신장비 모멘텀]]"
  - "[[market-intel/events/2026-04-27_광통신장비_모멘텀|2026-04-27 광통신장비 모멘텀]]"
  - "[[market-intel/events/2026-05-07_광통신장비_모멘텀|2026-05-07 광통신장비 모멘텀]]"
  - "[[market-intel/events/2026-05-11_광통신장비_모멘텀|2026-05-11 광통신장비 모멘텀]]"
---

# 대한광통신 진입 시나리오 평가 프레임워크

## Why this exists
이 스레드의 핵심 질문은 단순히
- "대한광통신이 좋다/나쁘다"
가 아니라,
- **언제 사야 하는가**
- **첫 급등 추격보다 구조가 생긴 뒤 진입하는 게 실제로 더 나은가**
- **동종군 확산 뒤 leader 복귀가 continuation인지 exhaustion인지 어떻게 구분할 것인가**
를 숫자로 답하는 것이다.

즉 이 문서는 대한광통신 사례를 중심으로,
- `첫 급등일 추격`
- `진정 뒤 재돌파`
- `동종군 확산 후 leader 복귀`
같은 직관을 **테스트 가능한 시나리오**로 바꾸기 위한 프레임워크다.

---

## Scope
기본 관찰 대상:
- [[market-intel/entities/stocks/대한광통신|대한광통신]]
- 광통신장비 / 통신기기 / 통신장비 cluster

참고 event anchor:
- [[market-intel/events/2026-04-17_광통신장비_모멘텀|2026-04-17 광통신장비 모멘텀]]
- [[market-intel/events/2026-04-27_광통신장비_모멘텀|2026-04-27 광통신장비 모멘텀]]
- [[market-intel/events/2026-05-07_광통신장비_모멘텀|2026-05-07 광통신장비 모멘텀]]
- [[market-intel/events/2026-05-11_광통신장비_모멘텀|2026-05-11 광통신장비 모멘텀]]

비교 목적상 peer 후보:
- [[market-intel/entities/stocks/RF머트리얼즈|RF머트리얼즈]]
- [[market-intel/entities/stocks/라이콤|라이콤]]
- [[market-intel/entities/stocks/오이솔루션|오이솔루션]]
- [[market-intel/entities/stocks/옵티코어|옵티코어]]
- [[market-intel/entities/stocks/이노인스트루먼트|이노인스트루먼트]]

---

## The practical research question
검증하려는 질문을 한 줄로 쓰면:

> **Under what exact conditions is waiting for structure better than chasing first impulse?**

조금 더 풀면 아래 3개다.
1. `D0 chase`보다 `pullback → rebreak`가 더 나은가?
2. peer spread가 일어난 뒤 leader 복귀를 타는 것이 단순 재진입보다 더 나은가?
3. breadth 확산은 continuation filter인가, exhaustion warning인가?

---

## Scenario registry (first-pass)
이 문서에서는 우선 아래 4개만 정식 시나리오로 둔다.

### 1. `d0_chase`
정의:
- 첫 급등일(D0) close 또는 D+1 open 추격 진입

목적:
- 다른 구조적 진입의 baseline

핵심 해석:
- upside는 크지만 MAE/갭리스크가 클 수 있음

### 2. `pullback_rebreak`
정의:
- D0 급등 후 1~3 거래일 내 pullback
- pullback이 완전 붕괴는 아님
- 이후 D0 high 또는 최근 short pivot reclaim 시 진입

핵심 가설:
- 첫 impulse 추격보다 risk-adjusted 성과가 나을 수 있음

### 3. `peer_spread_leader_return`
정의:
- leader 급등 후 1~3일 사이 peer/follower가 확산
- leader는 급락하지 않고 압축
- 이후 leader가 peer basket 대비 상대강도 재확인 시 진입

핵심 가설:
- breadth가 붙은 뒤 leader로 자금이 재집중될 때 continuation quality가 높을 수 있음

### 4. `breadth_burst_leader_only`
정의:
- 같은 narrative에서 다수 종목이 동시 확산
- basket 전체가 아니라 top leader 또는 top-2 leader만 진입

핵심 가설:
- breadth 자체는 regime filter이고, 실제 수익은 leader에 집중될 수 있음

---

## Each scenario must have 4 exact parts
각 시나리오는 반드시 아래 4개를 separately 정의한다.

1. **Context condition**
   - 어떤 배경/상태에서만 시나리오를 인정할지
2. **Entry trigger**
   - 정확히 언제 매수하는지
3. **Invalidation**
   - 무엇이 깨지면 아이디어가 틀린 것인지
4. **Exit rule**
   - 언제/어떻게 매도하는지

이 4개가 없으면 결과 해석이 흔들린다.

---

## Concrete rule draft

### A. `d0_chase`
- context: event-driven surge day, same-day top mover
- entry option 1: D0 close
- entry option 2: D+1 open
- invalidation: D+1 시가가 D0 close 대비 과도한 gap-up + 장초반 즉시 이탈
- first-pass exits:
  - fixed D+3
  - fixed D+5
  - close below prior-day low

### B. `pullback_rebreak`
초안 규칙:
- D0 close >= +15%
- D1~D3 사이 pullback 발생
- max pullback depth from D0 high: 8%~20%
- D0 low 종가 이탈 금지
- reclaim day 거래대금 or volume가 20d average 대비 의미 있게 유지
- entry: D0 high 또는 최근 2일 pivot 고점 종가 돌파
- invalidation: reclaim 실패 후 종가 기준 D0 low 하회
- exits:
  - D+3 / D+5 fixed hold
  - close below breakout-day low
  - 2일 내 새 고점 실패 시 exit

### C. `peer_spread_leader_return`
초안 규칙:
- D0 leader가 cluster 내 top rank
- 다음 1~3일 안에 peer >= 2~3개가 breakout-style move
- leader pullback depth < peer median pullback depth
- leader가 peer basket 대비 상대성과 재개
- entry: leader가 prior 2-day high 종가 돌파 + relative return > peer basket
- invalidation: peer 확산은 있었지만 leader가 상대강도 회복 실패
- exits:
  - D+3 / D+5 fixed hold
  - leader underperform vs peer basket for 2 consecutive days

### D. `breadth_burst_leader_only`
초안 규칙:
- same theme breadth bucket 진입 (`2-4`, `5-9`, `10+`)
- leader만 또는 top-2만 진입
- entry timing은 D0 close / D+1 open / D+1 reclaim으로 별도 분리 비교
- invalidation: breadth는 넓지만 leader turnover/lock quality가 약함
- exits:
  - fixed horizon
  - leader breakdown
  - breadth next-day collapse

---

## Minimum data fields to save per event/sample
아래 정도면 first-pass 비교가 가능하다.

### Core identifiers
- `event_date`
- `stock_code`
- `stock_name`
- `theme`
- `scenario_id`

### Structure / context
- `is_leader_on_d0`
- `leader_rank_in_cluster`
- `theme_breadth_d0`
- `theme_breadth_d1`
- `peer_spread_happened`
- `peer_spread_count`
- `prior_day_presence`
- `news_confirmed`
- `company_specific_followup`

### Pullback / rebreak state
- `pullback_days`
- `pullback_depth_pct`
- `d0_high_reclaimed`
- `recent_pivot_reclaimed`
- `reclaim_volume_vs_20d`

### Entry / risk / exit
- `entry_rule`
- `entry_date`
- `entry_price`
- `stop_rule`
- `exit_rule`
- `exit_date`
- `exit_price`

### Outcome
- `ret_1d`
- `ret_3d`
- `ret_5d`
- `mfe_5d`
- `mae_5d`
- `new_high_within_5d`
- `failed_within_2d`

---

## Canonical machine-readable schema (minimal v1)
이제부터는 “좋아 보이는 조건”을 말로만 두지 말고, 아래 최소 스키마로 고정해서 비교한다.

```yaml
scenario_registry_version: 1
scenario_id: pullback_rebreak
status: priority_scenario
family: structure_after_impulse
thesis: D0 추격보다 pullback 뒤 reclaim이 risk-adjusted 우위일 수 있다.
required_context:
  signal_day_gain_pct_min: 15
  lookback_days_after_d0: [1, 2, 3]
  theme_cluster_required: true
entry_variants:
  - d0_close
  - d1_open
  - d0_high_reclaim_close
invalidation:
  - close_below_d0_low
  - failed_reclaim_within_2d
exit_variants:
  - hold_3d
  - hold_5d
  - close_below_breakout_day_low
comparison_baseline:
  - d0_chase
promotion_gate:
  min_sample_count: 20
  min_availability_rate: 0.15
  must_improve_one_of:
    - avg_ret_5d
    - win_rate_5d
    - mae_5d
    - failure_rate_2d
```

핵심 필드만 남기면 아래 8개다.
- `scenario_id`
- `status`
- `family`
- `required_context`
- `entry_variants`
- `invalidation`
- `exit_variants`
- `comparison_baseline`

---

## Scenario status taxonomy
조건 셋은 모두 같은 급으로 다루지 않는다.

- `core_baseline`
  - 반드시 같이 계산하는 baseline
  - 현재는 `d0_chase`
- `priority_scenario`
  - 지금 바로 표본을 만들 1차 후보
  - 현재는 `pullback_rebreak`, `peer_spread_leader_return`, `breadth_burst_leader_only`
- `exploratory`
  - 아이디어는 있지만 정의/표본이 아직 약함
- `deferred`
  - 좋아 보여도 지금은 데이터/구현 부족으로 보류
- `rejected`
  - post-hoc 냄새가 강하거나 재현성이 약해 제외

즉 앞으로는
- “좋아 보인다”가 아니라
- **어느 status에 올려둘 것인가**
로 관리한다.

---

## Combination registry (first-pass)
사용자 관점의 핵심은 종목 스토리가 아니라 **반복되는 조건 세트**다.
그래서 시나리오와 별도로 combo registry를 둔다.

### Registry row template
- `combo_id`
- `status`
- `scenario_id`
- `leader_state`
- `breadth_bucket`
- `peer_spread_state`
- `pullback_bucket`
- `reclaim_state`
- `news_state`
- `sample_count`
- `promotion_note`

### First-pass combo candidates
1. `combo_pb1`
   - `scenario_id: pullback_rebreak`
   - `leader_state: leader_on_d0`
   - `breadth_bucket: 2_4`
   - `pullback_bucket: 8_12pct`
   - `reclaim_state: d0_high_reclaim_close`
   - `status: priority_scenario`
2. `combo_pb2`
   - `scenario_id: pullback_rebreak`
   - `leader_state: leader_on_d0`
   - `breadth_bucket: 5_9`
   - `pullback_bucket: 12_20pct`
   - `reclaim_state: recent_pivot_reclaim`
   - `status: exploratory`
3. `combo_lr1`
   - `scenario_id: peer_spread_leader_return`
   - `peer_spread_state: peers_2plus`
   - `breadth_bucket: 5_9`
   - `leader_state: relative_strength_recovery`
   - `status: priority_scenario`
4. `combo_bb1`
   - `scenario_id: breadth_burst_leader_only`
   - `breadth_bucket: 10_plus`
   - `leader_state: top1_only`
   - `news_state: confirmed_theme_tailwind`
   - `status: exploratory`

이 registry의 목적은:
- 어떤 조합을 실제로 봤는지 남기고
- 어떤 조합은 보류/제외했는지 기록하고
- 나중에 결과가 좋아도 post-hoc처럼 보이지 않게 하는 것.

---

## Sample snapshot row schema
실제 비교용 표본 row는 아래 정도면 충분하다.

```yaml
event_id: 2026-05-07_대한광통신
scenario_id: pullback_rebreak
combo_id: combo_pb1
entry_rule: d0_high_reclaim_close
stock_name: 대한광통신
event_date: 2026-05-07
is_leader_on_d0: true
theme_breadth_bucket: 2_4
peer_spread_state: peers_1
pullback_depth_bucket: 8_12pct
reclaim_state: d0_high_reclaim_close
ret_3d: null
ret_5d: null
mfe_5d: null
mae_5d: null
```

중요한 건 필드를 많이 넣는 게 아니라:
- **scenario_id**
- **combo_id**
- **entry_rule**
- **context bucket들**
- **outcome fields**
를 분리하는 것이다.

---

## Promotion ladder
결론도 1번에 승격하지 않는다.

1. `observation`
   - 차트/이벤트 관찰 단계
2. `registered`
   - scenario + combo 정의 완료
3. `sampled`
   - 표본 row 생성 완료
4. `compared`
   - baseline 대비 표 비교 완료
5. `promoted`
   - 재현성 있는 조건 셋으로 계속 추적

즉 앞으로는 “대한광통신이 또 갈까?”보다
- 어떤 아이디어가 아직 observation인지
- 어떤 combo가 compared까지 왔는지
를 보는 게 맞다.

---

## Evaluation table template
시나리오 평가는 최소 아래 표를 채워야 한다.

- `scenario_id`
- `sample_count`
- `availability_rate`
- `win_rate_3d`
- `win_rate_5d`
- `avg_ret_3d`
- `avg_ret_5d`
- `median_ret_5d`
- `mfe_5d`
- `mae_5d`
- `pct_gt_3pct`
- `pct_gt_5pct`
- `pct_gt_10pct`
- `failure_rate_2d`
- `notes`

핵심은:
- return만 보지 말고
- **MAE / 실패속도 / 실행가능성**까지 같이 본다.

---

## The first comparisons that matter
처음부터 복잡하게 가지 말고 아래 3개만 먼저 비교한다.

### Q1. Entry timing baseline
- `d0_chase` vs `pullback_rebreak`
- 같은 holding horizon으로 비교

### Q2. Leader-return effect
- `pullback_rebreak` 전체 vs `peer_spread_leader_return`
- peer spread 발생 유무로 split

### Q3. Breadth regime effect
- breadth bucket:
  - `2-4`
  - `5-9`
  - `10+`
- leader-only 결과가 breadth에 따라 어떻게 달라지는지 확인

---

## Interpretation rules
좋은 결론은 아래처럼 나와야 한다.

### Good answer examples
- `D0 chase`는 평균 upside는 높지만 MAE가 너무 크다.
- `pullback_rebreak`는 빈도는 낮지만 5d risk-adjusted 결과가 더 낫다.
- `peer_spread_leader_return`은 breadth가 실제로 붙고 leader가 상대강도를 회복할 때만 의미가 있다.
- breadth가 과도하면 basket continuation은 약해져도 top leader는 여전히 작동할 수 있다.

### Bad answer examples
- 재돌파가 좋아 보인다.
- leader가 다시 가는 것 같다.
- breadth가 크면 대체로 좋다.

---

## Promotion criteria (first-pass)
아래 조건을 동시에 만족해야 “계속 볼 가치 있는 시나리오”로 본다.

1. sample count가 너무 작지 않을 것
2. baseline(`d0_chase`) 대비
   - MAE가 개선되거나
   - 5d win rate가 개선되거나
   - failure rate가 의미 있게 낮을 것
3. rule이 차트 재량에만 의존하지 않고 재현 가능할 것
4. breadth / leader / peer spread 같은 state field로 분해했을 때 논리가 유지될 것

---

## Where this should be organized
이 주제는 market-intel 안에서 아래 레이어로 정리하는 게 맞다.

1. **Stock entity**
   - [[market-intel/entities/stocks/대한광통신|대한광통신]]
   - 개별 종목의 event history와 연결점 보관

2. **Event pages**
   - `market-intel/events/2026-04-17_광통신장비_모멘텀.md`
   - `market-intel/events/2026-04-27_광통신장비_모멘텀.md`
   - `market-intel/events/2026-05-07_광통신장비_모멘텀.md`
   - `market-intel/events/2026-05-11_광통신장비_모멘텀.md`
   - 각 날짜별 trigger / members / Hermes 해석 보관

3. **Research framework**
   - 이 문서: `market-intel/research/2026-05-11-대한광통신-entry-scenario-evaluation-framework.md`
   - 아이디어를 testable rule로 승격하는 공간

4. **Later machine-readable outputs**
   - 필요시 repo 쪽 `data/signals/...` 또는 별도 scenario snapshot으로 저장
   - 그다음 Quartz-visible review note로 연결

즉,
- 사건 기록은 event
- 종목 누적 관찰은 entity
- 진입 아이디어 검증 설계는 research
로 나누는 구조다.

---

## Immediate next step
다음 실무 단계는 아래 순서가 적절하다.

1. 대한광통신 + 광통신장비 peers 기준 sample date 목록 확정
2. 위 4개 scenario를 machine-readable schema로 고정
3. D0/D+1/D+3/D+5 outcome 표본 생성
4. first-pass comparison note 작성
5. 조건이 보이면 breadth / leader / peer-spread conditional slice로 확장

---

## One-line takeaway
핵심은 “좋아 보이는 그림”을 더 말하는 게 아니라,

> `첫 급등 추격` vs `구조 형성 후 진입`을 같은 기준으로 비교 가능한 시나리오 집합으로 만드는 것

이다.
