---
id: conditional-probability-field-glossary
title: "Conditional probability field glossary / manager explainer"
summary: manager-facing plain-language glossary for conditional probability axes, buckets, statuses, and entry-rule labels used in audit pages.
updated_at: 2026-04-28 13:25:00
source_type: glossary
time_verification_status: confirmed
---

# Conditional probability field glossary / manager explainer

이 페이지는 conditional probability audit를 볼 때 나오는 **축 이름, bucket 표기, 상태값, 진입 rule 이름**을 사람 말로 풀어쓴 설명 페이지다.

## Manager shortcut
- 이 glossary의 목적은 **"이 축이 뭘 뜻하는지"**를 즉시 이해하게 하는 것이다.
- 이 glossary의 목적은 **"이 변수 자체를 production feature로 승인한다"**가 아니다.
- 승인 여부는 항상 각 audit 페이지의 coverage / stability / validator status를 같이 봐야 한다.

## 먼저 읽는 법
### 1) single-axis / pairwise 뜻
- **single-axis**: 변수 하나만 잘라서 본 것
  - 예: `days_in_90_zone` 하나만 기준으로 bucket을 나눔
- **pairwise**: 변수 두 개를 동시에 묶어서 본 것
  - 예: `signal_type × days_in_90_zone`

### 2) bucket 표기 읽는 법
- `0_5` = 0~5 구간
- `6_20` = 6~20 구간
- `21_60` = 21~60 구간
- `61_plus` = 61 이상
- `0.25_0.5` = 25%~50% 구간
- `lt_30B` = 300억 미만
- `30_100B` = 300억~1,000억
- `100_300B` = 1,000억~3,000억
- `300B_plus` = 3,000억 이상
- `unknown` = 원천 데이터가 비었거나 아직 계산 불가라 bucket에 넣지 못한 상태
- `none` = 값이 0이라기보다, **이전 대상 자체가 없어서 비율을 계산할 분모가 없는 상태**로 읽는 편이 안전하다

### 3) 상태값 읽는 법
- `promoted`: 현재 기준으로는 context override 후보로 검토해볼 수 있는 상태
- `exploratory`: 패턴은 보이지만 아직 production override로 승인 못 하는 상태
- `too_sparse`: 표본이 너무 적어서 해석 자체를 보류해야 하는 상태

## Axis glossary

### `signal_type`
**무슨 종류의 breakout/event인가**를 뜻한다.
- 예: `52w_breakout`, `ath_breakout`
- manager 질문으로 바꾸면: **"같은 신고가라도 어떤 종류의 돌파냐?"**

### `prior_breakout_1_age_trading_days`
**직전 동일 breakout이 지금으로부터 몇 거래일 전에 있었는가**를 뜻한다.
- 0에 가까우면: 최근에 이미 breakout이 한 번 있었던 재돌파 성격
- 값이 크면: 직전 breakout과 시간이 꽤 벌어진 케이스
- manager 질문으로 바꾸면: **"이건 방금 재돌파한 건가, 한참 쉬다가 다시 돌파한 건가?"**

### `days_in_90_zone`
**현재 breakout 전에, 가격이 직전 기준 신고가의 90% 이상 구간에 얼마나 머물렀는가**를 뜻한다.
- 짧으면: 신고가 근처 체류가 짧았음
- 길면: 신고가 근처에서 버티거나 압축한 시간이 길었음
- manager 질문으로 바꾸면: **"이 breakout 전 압축/체류 시간이 짧았나 길었나?"**

### `low_52w_age_pct_in_52w`
**52주 최저가가 현재 52주 창 안에서 얼마나 최근/오래전인가**를 0~1 비율로 본 값이다.
- 0에 가까울수록: 52주 최저가가 최근 → 추세 초입 가능성
- 1에 가까울수록: 52주 최저가가 오래전 → 이미 추세가 많이 진행됐을 가능성
- manager 질문으로 바꾸면: **"이 breakout은 긴 추세의 후반인가, 아직 초입인가?"**

### `avg_turnover_20d_B`
**최근 20거래일 평균 거래대금을 억/십억 단위 bucket으로 나눈 것**이다.
- 사실상 liquidity / size proxy로 읽으면 된다.
- manager 질문으로 바꾸면: **"유동성이 작은 종목군과 큰 종목군에서 winner가 달라지나?"**

### `event_breadth_n`
**그날 같은 이벤트/테마/cluster에 몇 종목이 같이 잡혔는가**를 뜻한다.
- 값이 크면 breadth가 넓다
- 값이 작으면 소수 종목 중심이다
- manager 질문으로 바꾸면: **"오늘은 혼자 움직인 건가, 아니면 군집으로 번진 건가?"**
- 현재 audit에선 missingness가 높아서 **coverage-gap monitor** 성격이 강하다.

### `carryover_ratio_from_prev_day`
**전일 군집 멤버 중 오늘도 이어서 남아 있는 비율**이다.
- 높으면: 군집 continuity가 높다
- 낮으면: 전일 멤버가 빠지고 새 멤버로 교체되거나 군집이 흩어진다
- manager 질문으로 바꾸면: **"이 테마는 어제 멤버가 계속 가는가, 아니면 판이 갈아끼워지는가?"**
- 현재 audit에선 missingness가 높아서 **coverage-gap monitor** 성격이 강하다.

## Entry-rule glossary

### `same_close`
- breakout 당일 종가 기준 진입
- 가장 즉시 반응하는 rule

### `next_open`
- 다음 거래일 시가 기준 진입
- overnight gap 영향을 바로 받는 rule

### `wait_1d_close`
- 하루 기다린 뒤 그날 종가에 진입

### `wait_2d_close`
- 이틀 기다린 뒤 그날 종가에 진입
- 현재 pooled breakout baseline에서 **audited default comparison anchor**로 쓰는 rule

### `wait_3d_close`
- 3일 기다린 뒤 그날 종가에 진입

### `pullback_4pct`
- breakout 이후 일정 pullback 조건(약 -4%)이 왔을 때만 진입하는 rule
- 평균 성과가 좋아 보여도 availability/usability 문제가 같이 따라올 수 있다

## Metric legend
### `Sharpe20`
- 20거래일 horizon 수익률의 risk-adjusted score
- 값이 높을수록, 변동성을 감안한 성과가 더 좋았다는 뜻
- 여기서는 **descriptive research metric**이지 production portfolio 승인 지표는 아님

### `usable20`
- 20거래일 horizon까지 실제로 계산 가능한 표본 수
- entry signal이 있었더라도 미래 20거래일 데이터가 부족하면 여기서 빠질 수 있다

### `unknown rate`
- 해당 axis 값이 비어 있어서 bucket 분석에 못 쓴 비율
- 높을수록 그 변수는 설명용 diagnostic에 가깝고, allocation rule로 쓰기 어렵다

## How to read the audit page quickly
1. 먼저 `unknown rate`가 높은 축인지 본다.
2. 높으면 winner가 보여도 바로 승인하지 않는다.
3. `single-axis`에서 winner가 보여도 `pairwise`에서 뒤집히는지 확인한다.
4. `promoted`가 아니라 `exploratory`면 가설 지도일 뿐, production override가 아니다.
5. 결국 manager가 승인하는 것은 **숫자 자체**가 아니라 **coverage + stability + method clarity**다.

## Related audit pages
- [Conditional probability calculation audit / manager review](/market-intel/research/2026-04-27-conditional-probability-entry-rule-manager-review)
- [Entry-rule calculation audit (worked example: wait_2d_close)](/market-intel/research/wait-2d-close-review)
