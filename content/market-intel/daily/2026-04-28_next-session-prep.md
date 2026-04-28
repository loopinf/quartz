---
id: next-session-prep-2026-04-28
note_type: next_session_prep
created_at: 2026-04-27 18:41:36 KST
updated_at: 2026-04-28 06:08:01 KST
session_date: 2026-04-28
source_note: 2026-04-27_top30_recap
supporting_notes:
  - 2026-04-27_evening-briefing-input
  - 2026-04-27_evening-briefing
  - 2026-04-27_top30_recap
  - 2026-04-24_top30_recap
  - 2026-04-23_top30_recap
  - 2026-04-22_top30_recap
  - 2026-04-21_top30_recap
  - 2026-04-27_디스플레이_모멘텀
  - 2026-04-27_로봇_모멘텀
  - 2026-04-27_광통신장비_모멘텀
  - 2026-04-27_반도체_모멘텀
  - 2026-04-27_양자-양자암호_모멘텀
  - 2026-04-27_전력기기_모멘텀
reviewer: 헤르메스(ㅎㅁ)
generation_mode: upgraded_prior_close_scaffold
reconstruction_mode: backfill_preopen_only
lookahead_guard: strict
lookahead_cutoff_kst: 2026-04-28 08:59:00 KST
allowed_sources:
  - market-intel/daily/2026-04-27_top30_recap.md
  - market-intel/daily/2026-04-27_evening-briefing-input.md
  - market-intel/daily/2026-04-27_evening-briefing.md
  - market-intel/daily/2026-04-24_top30_recap.md
  - market-intel/daily/2026-04-23_top30_recap.md
  - market-intel/daily/2026-04-22_top30_recap.md
  - market-intel/daily/2026-04-21_top30_recap.md
  - market-intel/events/2026-04-27_디스플레이_모멘텀.md
  - market-intel/events/2026-04-27_로봇_모멘텀.md
  - market-intel/events/2026-04-27_광통신장비_모멘텀.md
  - market-intel/events/2026-04-27_반도체_모멘텀.md
  - market-intel/events/2026-04-27_양자-양자암호_모멘텀.md
  - market-intel/events/2026-04-27_전력기기_모멘텀.md
  - /Users/gbserver/repos/jmkr_kj/data/signals/high-signals/2026-04-27.json
  - /Users/gbserver/repos/jmkr_kj/data/signals/high-signals/2026-04-24.json
  - /Users/gbserver/repos/jmkr_kj/data/signals/high-signals/2026-04-23.json
  - /Users/gbserver/repos/jmkr_kj/data/signals/high-signals/2026-04-22.json
  - /Users/gbserver/repos/jmkr_kj/data/signals/high-signals/2026-04-21.json
excluded_sources:
  - market-intel/daily/2026-04-28_top30_recap.md
  - market-intel/daily/2026-04-28_evening-briefing-input.md
  - market-intel/daily/2026-04-28_evening-briefing.md
  - any 2026-04-28 intraday tape or post-open observations
  - any hindsight wording based on the 2026-04-28 session outcome
source_scope: prior_close_only
same_day_intraday_excluded: true
---

# 2026-04-28 Next Session Prep

## Why this note exists
- 이 문서는 **2026-04-28 화요일 장전 대응용 prediction anchor**다.
- 기존 exact-date prep는 이미 존재했지만, 최근 5거래일 합성과 look-ahead audit trail이 더 분명히 보이도록 **review-ready 형태로 업그레이드**했다.
- 이 문서는 **2026-04-28 08:59 KST 이전에 알 수 있었던 정보만** 사용한 pre-open hypothesis artifact이며, replay/review 문서가 아니다.

## Guardrail
- 허용 소스는 `2026-04-27` close 기준 validated recap / evening input / evening briefing, 최근 5거래일 validated recap 체인, 04/27 event notes, 최근 5거래일 high-signal snapshot이다.
- 금지 소스는 `2026-04-28` same-day recap / evening-briefing-input / evening-briefing, 장중 테이프, 장마감 결과, 이후 hindsight 해석이다.
- 따라서 아래 가설은 **사전 시나리오**일 뿐이며, 실제 결과 비교는 별도 review 문서에서 해야 한다.

## Recent 5 trading days synthesized context
- [[2026-04-21_top30_recap]] — `이차전지`가 15개로 과집중이었고 `로봇`은 보조 축에 머물렀다.
- [[2026-04-22_top30_recap]] — `로봇 / 반도체소부장 / 조선기자재 / 데이터센터`로 breadth가 넓어지며 전일 이차전지 단일집중에서 분산 구조로 이동했다.
- [[2026-04-23_top30_recap]] — `제약바이오`가 전면에 섰지만, `반도체소부장`과 `전력기기`가 계속 남아 있어 완전한 리더 교체보다는 다축 순환으로 읽힌다.
- [[2026-04-24_top30_recap]] — `반도체소부장`이 8개로 다시 강하게 재집중됐고 `화장품 / 우주항공 / 조선기자재`가 확산 버킷을 형성했다.
- [[2026-04-27_top30_recap]] — `디스플레이(4) / 로봇(3)`가 새 주도 축으로 올라오고 `광통신장비 / 반도체 / 양자·양자암호 / 전력기기`가 보조 확산 축으로 붙었다.

반복 등장 구조와 해석:
- `로봇`은 최근 5거래일 중 3회 등장했다. 단발 headline보다는 **반복 관찰되는 continuation 후보**다.
- `반도체소부장/반도체` 축은 04/22~04/24에 연속적으로 강했고 04/27에도 `한미반도체 / 파두 / 티이엠씨`로 잔존해 **기저 체력 축**으로 남아 있다.
- `전력기기/전력 인프라`는 04/23과 04/27에 반복 확인돼, 메인 리더가 흔들릴 때 재집중되는 **residual rotation bucket**으로 볼 수 있다.
- 최근 1주 흐름은 `이차전지 단일집중 -> 다축 분산 -> 반도체 재집중 -> 디스플레이/로봇 재선별`에 가깝다. 즉 04/28 장전의 핵심은 **04/27의 새 리더가 하루짜리 급등이었는지, 아니면 최근 1주 순환의 다음 주도축인지**를 검증하는 것이다.

## Base context available before the open
- validated recap anchor: [[2026-04-27_top30_recap]]
- close input anchor: [[2026-04-27_evening-briefing-input]]
- close output anchor: [[2026-04-27_evening-briefing]]
- event-proof anchors:
  - [[market-intel/events/2026-04-27_디스플레이_모멘텀|2026-04-27_디스플레이_모멘텀]]
  - [[market-intel/events/2026-04-27_로봇_모멘텀|2026-04-27_로봇_모멘텀]]
  - [[market-intel/events/2026-04-27_광통신장비_모멘텀|2026-04-27_광통신장비_모멘텀]]
  - [[market-intel/events/2026-04-27_반도체_모멘텀|2026-04-27_반도체_모멘텀]]
  - [[market-intel/events/2026-04-27_양자-양자암호_모멘텀|2026-04-27_양자-양자암호_모멘텀]]
  - [[market-intel/events/2026-04-27_전력기기_모멘텀|2026-04-27_전력기기_모멘텀]]
- close-context read:
  - 04/27 validated TOP30 기준 상위 군집은 `디스플레이 4 / 로봇 3 / 광통신장비 2 / 반도체 2 / 양자·양자암호 2 / 전력기기 2`였다.
  - 04/27 evening input/output도 same-day local observation을 별도 관리했지만, 본 prep의 주된 기준선은 validated recap의 군집 구조와 최근 5거래일 continuity다.
  - 따라서 장전 기본 시나리오는 `디스플레이 선도 유지 여부`를 먼저 보고, 그 다음 `로봇 공동주도`와 `광통신장비·반도체 확산`을 확인하는 순서다.

## 신고가 / high-signal 팩트층
- 사용한 snapshot: `2026-04-27, 2026-04-24, 2026-04-23, 2026-04-22, 2026-04-21`의 local high-signal JSON.
- 해석 원칙:
  - `52w/ATH breakout` overlap = 더 강한 기술적 확인
  - `near-52w/ATH` overlap = continuation/follow-through 관찰 후보
  - overlap 부재 = recap/event continuity에 더 의존

### 04/27 carry-over 테마와 겹치는 breakout / near-high 이름
- **디스플레이**
  - breakout overlap: `서울바이오시스`, `동아엘텍`
  - near-high overlap: `서울반도체` (near 52w/ATH 95), `더코디` (04/21 near 52w 90 이력)
  - 읽는 법: 04/27 breadth 1위이면서 기술 팩트 레이어도 일부 받쳐 주므로 **1순위 leader continuation check**로 두기 적절하다.
- **로봇**
  - breakout overlap: `와이제이링크` (04/21~04/24, 52w breakout), `앤로보틱스`는 04/27 near-ATH 90 / near-52w 90, `로보티즈`는 04/27 near-ATH 95 / near-52w 95
  - 읽는 법: breadth 반복성과 technical follow-through가 같이 보여 **공동 주도 또는 후속 확산 후보**다.
- **광통신장비**
  - exact overlap은 상대적으로 약하다.
  - 읽는 법: 04/27 recap과 event note continuity는 있으나, high-signal 확인은 디스플레이/로봇보다 약하므로 **2순위 expansion check**가 맞다.
- **반도체 / 양자·양자암호 / 전력기기**
  - breakout overlap: `한미반도체`, `파두`, `티이엠씨`, `쏘닉스`, `제룡산업`, `세명전기`
  - near-high overlap: `제룡산업`(near ATH 90), `세명전기`(04/23~04/27 near-high/ATH 상태 반복)
  - 읽는 법: 주도 1순위는 아니어도 technical support가 풍부해, 메인 시나리오 약화 시 **residual rotation bucket**으로 무시하면 안 된다.

### Proof bundle
- validated recap anchor: [[2026-04-27_top30_recap]]
- close-context anchors: [[2026-04-27_evening-briefing-input]], [[2026-04-27_evening-briefing]]
- event-proof links:
  - [[market-intel/events/2026-04-27_디스플레이_모멘텀|디스플레이 event]]
  - [[market-intel/events/2026-04-27_로봇_모멘텀|로봇 event]]
  - [[market-intel/events/2026-04-27_광통신장비_모멘텀|광통신장비 event]]
  - [[market-intel/events/2026-04-27_반도체_모멘텀|반도체 event]]
  - [[market-intel/events/2026-04-27_양자-양자암호_모멘텀|양자·양자암호 event]]
  - [[market-intel/events/2026-04-27_전력기기_모멘텀|전력기기 event]]
- raw dataset pointers:
  - `/Users/gbserver/repos/jmkr_kj/data/signals/high-signals/2026-04-27.json`
  - `/Users/gbserver/repos/jmkr_kj/data/signals/high-signals/2026-04-24.json`
  - `/Users/gbserver/repos/jmkr_kj/data/signals/high-signals/2026-04-23.json`
  - `/Users/gbserver/repos/jmkr_kj/data/signals/high-signals/2026-04-22.json`
  - `/Users/gbserver/repos/jmkr_kj/data/signals/high-signals/2026-04-21.json`

## Pre-open hypothesis set
### Hypothesis A — 디스플레이 leader continuation
- 04/27 breadth 1위 군집이었고 `서울바이오시스 / 동아엘텍` breakout support까지 확인돼, 장초 거래대금이 유지되면 가장 먼저 continuation 해석을 줄 수 있다.

### Hypothesis B — 로봇이 공동 주도축으로 승격
- 최근 5거래일 중 3회 등장했고, `앤로보틱스 / 와이제이링크 / 로보티즈`가 breadth + near-high/breakout 팩트층을 일부 공유한다.
- 디스플레이가 단일 리더에 그치지 않고 로봇이 같이 붙으면 `하루짜리 급등`보다 `새 리더 cluster 형성` 가능성이 커진다.

### Hypothesis C — 광통신장비·반도체는 후속 확산, 전력기기·양자는 residual rotation
- `광통신장비`는 04/27 핵심 보조군이지만 technical support는 상대적으로 약하므로 장초 follow-through가 실제로 붙는지 확인이 필요하다.
- 반면 `반도체 / 양자·양자암호 / 전력기기`는 technical overlap이 있어, 메인 리더가 흔들릴 때 재집중되는 대체 시나리오로 볼 수 있다.

## Priority watch order
### 1st priority — leader continuation check
- **디스플레이**
  - 서울바이오시스
  - 동아엘텍
  - 서울반도체
  - 더코디
  - **선정 이유**: 04/27 validated breadth 1위 군집이며 breakout/near-high 팩트층이 가장 직접적으로 확인된다.

### 2nd priority — 공동 주도 / expansion check
- **로봇**
  - 앤로보틱스
  - 와이제이링크
  - 로보티즈
  - **선정 이유**: 최근 5거래일 중 3회 반복 등장했고 04/27에도 상위 군집이었다.
- **광통신장비**
  - 이노인스트루먼트
  - 대한광통신
  - **선정 이유**: 04/27 보조 주도축이었으며, 디스플레이/로봇의 breadth가 시장 전체 확산으로 이어질 때 가장 먼저 확인할 버킷이다.

### 3rd priority — residual / rotation check
- **반도체**
  - 한미반도체
  - 파두
  - **선정 이유**: 최근 주간 기저 체력 축이며 04/27 breakout support가 있다.
- **양자/양자암호**
  - 티이엠씨
  - 쏘닉스
  - **선정 이유**: 04/27 same-day cluster였고 breakout overlap이 있어 메인 시나리오 약화 시 대체 순환 후보가 된다.
- **전력기기**
  - 제룡산업
  - 세명전기
  - **선정 이유**: 04/23과 04/27에 반복 등장했고 기술 팩트층도 남아 있어 observation priority를 유지할 가치가 있다.

## What to check at the open
1. **디스플레이 상위주가 gap-only가 아니라 거래대금 leader로 유지되는지** 확인.
2. **로봇이 일부 종목 급등이 아니라 cluster로 동반 확산하는지** 확인.
3. **광통신장비가 장초 확산 버킷으로 붙는지, 아니면 headline 반응 후 약해지는지** 확인.
4. **반도체 / 양자 / 전력기기**가 메인 시나리오 약화 시 대체 순환으로 재집중되는지 확인.
5. 최근 1주 구조가 `다축 확산`으로 이어지는지, 아니면 다시 `소수 leader 집중`으로 수축하는지 구분.

## Failure / invalidation conditions
- 디스플레이 상위주가 갭만 만들고 바로 밀리면 `04/27 leader continuation` 가설을 빠르게 낮춘다.
- 로봇이 breadth 없이 한두 종목 강세에 그치면 공동 주도축 승격 해석을 보류한다.
- 광통신장비가 거래대금 follow-through를 못 붙이면 expansion 시나리오는 약화된다.
- 반도체/양자/전력기기까지 동시에 약하면 최근 1주 구조는 `새 주도 형성`보다 `단기 과열 후 재선별 지연` 쪽으로 다시 읽어야 한다.

## One-line prep
**2026-04-28 장전의 기본 시나리오는 04/27의 디스플레이 breadth가 진짜 새 leader인지 먼저 확인하고, 로봇이 공동 주도로 승격하는지와 광통신장비·반도체·전력기기 쪽 후속 확산이 붙는지 순서대로 검증하는 것이다.**

## Follow-up note
- 실제 결과 비교, 시나리오 적중/실패 원인, 다음 개선 포인트는 별도 `session-review / replay` 문서에서 다뤄야 한다.
- 이 prep 문서는 **pre-open hypothesis artifact**이며 replay completion으로 간주하지 않는다.

## Conditional probability / entry-rule summary
- current audited pooled baseline: `wait_2d_close`
- status: **risk-adjusted baseline candidate**, not approved as a context-specific production override
- compact evidence line: `20d Sharpe 3.9063 | usable20 27620 | availability 99.32%`
- interpretation: 전구간 breakout baseline에선 `wait_2d_close`가 현재 audited default comparison anchor이고, conditional override는 아직 `exploratory` 단계다.
- review links:
  - [[market-intel/research/2026-04-27-conditional-probability-entry-rule-manager-review|Conditional probability calculation audit / manager review]]
  - [[market-intel/research/wait-2d-close-review|Entry-rule calculation audit (worked example: wait_2d_close)]]
- direct result shortcuts:
  - local: [conditional probability calculation audit](http://127.0.0.1:8081/market-intel/research/2026-04-27-conditional-probability-entry-rule-manager-review) / [entry-rule calculation audit worked example](http://127.0.0.1:8081/market-intel/research/wait-2d-close-review)
  - tailscale: [conditional probability calculation audit](http://gbs-mac-mini.taila43069.ts.net:8081/market-intel/research/2026-04-27-conditional-probability-entry-rule-manager-review) / [entry-rule calculation audit worked example](http://gbs-mac-mini.taila43069.ts.net:8081/market-intel/research/wait-2d-close-review)
- note: `wait_3d_close` / `wait_1d_close` / `next_open`도 top-tier cluster로 남아 있으므로, prep에서는 naked winner claim보다 **audited baseline + click-through review path**를 우선한다.
