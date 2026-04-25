---
id: high-signal-entry-rule-review-2025-04-01-2026-04-16
created_at: 2026-04-25 12:54:45 KST
updated_at: 2026-04-25 12:54:45 KST
source_type: technical-entry-backtest-review
source_data:
  - /Users/gbserver/repos/jmkr_kj/data/signals/high-signal-entry-outcomes/vbtpro-recheck-2025-04-01-to-2026-04-16.json
  - /Users/gbserver/repos/jmkr_kj/data/signals/high-signal-entry-outcomes/*.json
source_code:
  - /Users/gbserver/repos/jmkr_kj/scripts/export_high_signal_entry_outcomes.py
  - /Users/gbserver/repos/jmkr_kj/scripts/vbtpro_recheck_high_signal_entry_rules.py
engine: vectorbtpro 2026.4.7
time_verification_status: confirmed
---

# High Signal Entry Rule Review (2025-04-01 ~ 2026-04-16)

이 문서는 `wait_2d_close`가 왜 상위 rule로 보였는지 **사용자가 검토 가능한 근거 형태**로 정리한 review note다.
핵심은 `결론만` 적는 게 아니라, **어떤 표본을 어떤 rule 정의로 어떤 기준으로 비교했는지**를 함께 남기는 것이다.

## Review question
- breakout event 이후 어떤 entry rule이 더 나은가?
- 특히 `wait_2d_close`가 정말 상위 rule인지, 아니면 평균/가용성/표본효과를 착각한 것인지?

## Scope
- range: `2025-04-01 ~ 2026-04-16`
- source universe: JMKR high-signal breakout outcome exports
- event rows inspected: `29,260`
- compared rules:
  - `same_close`
  - `next_open`
  - `wait_1d_close`
  - `wait_2d_close`
  - `wait_3d_close`
  - `pullback_2pct`
  - `pullback_4pct`
- outcome horizons used in summary: `5d / 10d / 20d`

## Method
### 1) Event-level deterministic outcome export
Raw outcome rows come from:
- `[[market-intel/research/high-signal-entry-timing-roadmap|High Signal Entry Timing Roadmap]]`
- code: `/Users/gbserver/repos/jmkr_kj/scripts/export_high_signal_entry_outcomes.py`

This exporter does the following per breakout event:
- loads the exact event date from the high-signal snapshot
- evaluates each entry rule independently
- stores whether entry was available
- stores entry date / entry price / lag
- stores `ret_5d`, `ret_10d`, `ret_20d`, `mfe_20d`, `mae_20d`, `made_new_high_within_*d`

Rule-definition check from code:
- `same_close`: breakout 당일 종가 진입
- `next_open`: breakout 다음 거래일 시가 진입
- `wait_1d_close`: breakout 다음 거래일 종가 진입
- `wait_2d_close`: breakout 후 **2 거래일 뒤 종가** 진입
- `wait_3d_close`: breakout 후 3 거래일 뒤 종가 진입
- `pullback_2pct`: breakout 종가 대비 -2% 눌림 가격 체결 시 진입
- `pullback_4pct`: breakout 종가 대비 -4% 눌림 가격 체결 시 진입

### 2) Recheck summary
Aggregate summary comes from:
- code: `/Users/gbserver/repos/jmkr_kj/scripts/vbtpro_recheck_high_signal_entry_rules.py`
- summary file: `/Users/gbserver/repos/jmkr_kj/data/signals/high-signal-entry-outcomes/vbtpro-recheck-2025-04-01-to-2026-04-16.json`

The summary code filters to:
- `entry_available == True`
- `ret_20d` is not null

Then it computes:
- average return
- median return
- win rate
- Sharpe
- MFE / MAE
- new-high follow-through rate

## Comparison table
### Full-range breakout baseline
| rule | available | available rate | trades used in summary | 5d avg | 10d avg | 20d avg | 20d median | 20d win | 20d sharpe | MFE20 | MAE20 | new high 20d |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `wait_2d_close` | 29061/29260 | 99.3% | 27,232 | 1.02% | 2.12% | 4.43% | 0.34% | 0.5703 | 3.8271 | 18.07% | -10.54% | 0.8202 |
| `wait_3d_close` | 28866/29260 | 98.7% | 27,139 | 0.95% | 2.10% | 4.34% | 0.31% | 0.5683 | 3.7886 | 17.77% | -10.38% | 0.8074 |
| `next_open` | 29257/29260 | 100.0% | 27,337 | 1.12% | 2.11% | 4.47% | 0.35% | 0.5697 | 3.7090 | 18.44% | -10.75% | 0.8345 |
| `wait_1d_close` | 29257/29260 | 100.0% | 27,337 | 1.12% | 2.11% | 4.47% | 0.35% | 0.5697 | 3.7090 | 18.44% | -10.75% | 0.8345 |
| `same_close` | 29260/29260 | 100.0% | 27,472 | 1.41% | 2.31% | 4.61% | 0.34% | 0.5682 | 3.5560 | 19.11% | -10.89% | 0.8594 |
| `pullback_4pct` | 21340/29260 | 72.9% | 19,546 | 1.85% | 3.12% | 4.49% | 1.06% | 0.5346 | 3.4061 | 20.78% | -11.71% | 0.6537 |
| `pullback_2pct` | 23642/29260 | 80.8% | 21,874 | 1.52% | 2.81% | 4.46% | 1.05% | 0.5377 | 3.3981 | 20.19% | -11.62% | 0.7332 |

## Quick read
### What `wait_2d_close` is actually best at
- **20d Sharpe 1위**: `3.8271`
- availability도 매우 높음: `99.3%`
- trade count도 충분히 큼: `27,232`
- 즉 `wait_2d_close`가 좋다고 말할 때의 정확한 표현은:
  - **"이 full-range breakout baseline에서 risk-adjusted 20d 성과(Sharpe)가 가장 좋았다"**

### What `wait_2d_close` is *not* best at
- 20d average return 최고는 `same_close` (`4.61%`)
- 10d / 5d average도 `same_close`, `pullback` 쪽이 더 높게 보이는 구간이 있음
- 따라서 `wait_2d_close`를 **무조건 최고 진입법**처럼 쓰면 과장이다

### Why pullback rules need caution
- `pullback_2pct`: available rate `80.8%`
- `pullback_4pct`: available rate `72.9%`
- 평균수익/중앙값은 좋아 보여도, **실제 체결 안 되는 케이스를 빼고 본 결과**라서 miss-trade bias를 같이 봐야 한다

## Interpretation notes
### Why trade_count is smaller than available count
- `available`는 rule상 진입 시점이 존재한 event 수다
- `trades used in summary`는 그중에서 `ret_20d`까지 계산 가능한 rows만 남긴 값이다
- 즉 범위 끝쪽 이벤트는 20거래일 미래 데이터가 부족해서 summary trade_count에서 빠질 수 있다

### Why `next_open` and `wait_1d_close` look identical here
- 이 범위에선 aggregate 결과가 완전히 동일하게 나왔다
- 원인 후보:
  - 데이터 구조상 `next_open`과 다음날 종가 차이가 aggregate에서 크게 상쇄되었을 가능성
  - 혹은 향후 더 세밀한 분해가 필요한 구조적 이유
- 현재 note에서는 **동일 결과가 나왔다는 사실**까지만 기록하고, 원인 단정은 보류한다

## Operational takeaway for prep
- 장전 operator view에선 `wait_2d_close / wait_3d_close / next_open`을 **상위 risk-adjusted baseline 후보**로 읽는다
- 단, 개별 종목 표본이 충분하면 stock-specific lookup을 먼저 본다
- `pullback`은 평균수익이 높아도 availability가 낮으므로, **놓친 거래까지 포함한 현실성**을 같이 본다
- 따라서 prep에는 이 review note를 직접 링크하고, prep 본문에는 핵심 요약만 두는 게 맞다

## Related notes
- [[market-intel/research/high-signal-entry-timing-roadmap|High Signal Entry Timing Roadmap]]
- [[market-intel/research/high-signal-entry-backtest-sample|High Signal Entry Backtest Sample]]
- [[market-intel/daily/2026-04-24_next-session-prep|2026-04-24 Next Session Prep]]

## Raw file pointers
- summary JSON: `/Users/gbserver/repos/jmkr_kj/data/signals/high-signal-entry-outcomes/vbtpro-recheck-2025-04-01-to-2026-04-16.json`
- event outcome rows: `/Users/gbserver/repos/jmkr_kj/data/signals/high-signal-entry-outcomes/*.json`
- exporter: `/Users/gbserver/repos/jmkr_kj/scripts/export_high_signal_entry_outcomes.py`
- recheck script: `/Users/gbserver/repos/jmkr_kj/scripts/vbtpro_recheck_high_signal_entry_rules.py`

## Follow-up gap
다음 단계에서 더 좋아져야 하는 건:
- context bucket별 분해 (`prior_breakout_1_age_trading_days`, `days_in_90_zone`, `low_52w_age_pct_in_52w`)
- near-high state 자체의 outcome table
- stock-specific review page 자동 생성
- prep에서 표를 자동으로 축약 인용하고 review note로 링크하는 자동화
