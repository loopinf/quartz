---
id: next-session-prep-paired-review-template
note_type: workflow_template
created_at: 2026-04-28 20:55:00 KST
updated_at: 2026-04-29 18:05:00 KST
reviewer: 헤르메스(ㅎㅁ)
title: next-session prep paired review template
summary: next-session-prep 본문을 hindsight로 오염시키지 않으면서, 사용자 의견·검토 요청·헤르메스 리뷰 결과를 별도 paired review 노트에 저장하기 위한 템플릿.
---

# next-session prep paired review template

## Purpose
- `next-session-prep`는 **prediction anchor**로 유지한다.
- 사용자 의견, Hermes 검토, 이후 replay 포인트는 별도 paired review note에 남긴다.
- 이렇게 해야 prep 본문과 hindsight/review layer가 섞이지 않는다.
- paired review에서 entity graph를 보더라도, prep cutoff 이전에 knowable했던 graph만 `prep_review` 근거로 쓴다.

## Naming / path rule
- 기본 경로: `market-intel/research/replay-YYYY-MM-DD-next-session-prep.md`
- `YYYY-MM-DD`는 대응한 실제 session date를 쓴다.
- 예: `market-intel/research/replay-2026-04-29-next-session-prep.md`

## Minimal link-back rule in prep
`next-session-prep` 본문 하단에는 최소 아래만 남긴다.

```md
## Follow-up note
- 이 문서는 pre-open prep anchor다.
- 사용자 의견 / Hermes 검토 / 실제 replay는 별도 paired review 문서에서 관리한다.
- paired review: [[market-intel/research/replay-YYYY-MM-DD-next-session-prep|replay-YYYY-MM-DD-next-session-prep]]
```

## Suggested request block inside prep
사용자 의견과 검토 요청은 prep note 안에서 아래처럼 짧게 유지한다.

```md
## My review notes
- thesis_push:
- disagreement_or_risk:
- missing_piece:
- open_question:

## Hermes review request
- review_request_status: requested
- requested_at_kst: YYYY-MM-DD HH:MM
- focus_question: 무엇을 검토해줬으면 하는지 1~2문장
- paired_review_target: [[market-intel/research/replay-YYYY-MM-DD-next-session-prep|replay-YYYY-MM-DD-next-session-prep]]
```

---

# Paired Review Note Template

아래를 새 review note에 복사해서 사용.

```md
---
id: replay-YYYY-MM-DD-next-session-prep
note_type: predictive_replay
created_at: YYYY-MM-DD HH:MM:SS KST
updated_at: YYYY-MM-DD HH:MM:SS KST
event_date: YYYY-MM-DD
review_date: YYYY-MM-DD
reviewer: 헤르메스(ㅎㅁ)
region: KR
session_relation: kr_preopen
review_mode: prep_review
review_request_status: reviewed
entity_review_scope: prep_known_graph_only
source_prep: [[market-intel/daily/YYYY-MM-DD_next-session-prep|YYYY-MM-DD_next-session-prep]]
source_links:
  - "[[market-intel/daily/YYYY-MM-DD_next-session-prep|YYYY-MM-DD_next-session-prep]]"
  - "[[market-intel/daily/PREV-DAY_top30_recap|PREV-DAY_top30_recap]]"
  - "[[market-intel/daily/PREV-DAY_evening-briefing-input|PREV-DAY_evening-briefing-input]]"
user_opinion_captured: true
focus_question: ""
review_scope: ["prep thesis", "priority names", "invalidation logic", "entity graph boundary"]
related_events: []
related_entities: []
pattern_labels: ["prep_review", "entity_boundary_check"]
summary: "한 줄 요약"
---

# replay-YYYY-MM-DD-next-session-prep

## Why this review exists
- 이 노트는 [[market-intel/daily/YYYY-MM-DD_next-session-prep|YYYY-MM-DD_next-session-prep]]에 적힌 사용자 의견과 검토 요청을 분리 저장하기 위한 paired review다.
- 목적은 prep 본문을 유지한 채, **어떤 의견을 검토했고 무엇을 동의/수정/보류했는지**를 명확히 남기는 것이다.

## Review request snapshot
- requested_at_kst:
- requested_by: user
- focus_question:
- review_scope:
  - prep thesis
  - carry-over themes
  - priority names / sectors
  - invalidation conditions

## User opinion snapshot
> prep note의 `My review notes`를 그대로 옮기거나 요약.

- thesis_push:
- disagreement_or_risk:
- missing_piece:
- open_question:

## What was knowable at review time?
- 이 검토 시점에 사용 가능한 정보 범위를 적는다.
- pre-open 검토면 same-session outcome을 넣지 않는다.
- close 이후 replay면 hindsight 사용 여부를 명시한다.

## Entity graph usage boundary
- prep에서 entity는 **proof lookup이 아니라 memory lookup**이다.
- pre-open review에서는 prep cutoff 이전에 이미 존재했고, prior recap / prior event proof / same-window high-signal로 역추적 가능한 entity 정보만 검토 근거로 쓴다.
- later-enriched entity 문구나 post-close에 추가된 link는 hindsight layer로 분리 표기한다.

## Hermes review verdict
### 1. Agree
- 사용자의 의견 중 유지할 포인트

### 2. Tighten / revise
- 표현은 맞지만 더 좁혀야 하는 포인트

### 3. Missing checks
- prep에 추가로 확인해야 할 팩트 / 시그널 / 링크

### 4. Overreach / unsupported claims
- 근거 부족, 과도한 일반화, leader/priority 혼동 등

## Revised operating view
### Base case
- 

### Alternate case
- 

### What would change my mind
- 

## Suggested edits back to prep
- prep 본문을 직접 오염시키지 않는 범위에서, 남겨도 되는 수정만 적는다.
- 예:
  - one-line prep 문장 정교화
  - priority bucket 재배치
  - invalidation 조건 문구 강화
  - supporting link 추가

## If keeping prep pure, add only this back-link
```md
- paired review: [[market-intel/research/replay-YYYY-MM-DD-next-session-prep|replay-YYYY-MM-DD-next-session-prep]]
```

## Optional post-close replay extension
- 실제 장 결과까지 이어서 복기할 경우 아래만 추가한다.
- pre-open 검토와 post-close replay를 섞을 때는 시점을 분명히 나눈다.

### Actual outcome
- 

### What was right
- 

### What was missed
- 

### Rule / workflow update
- 

## Links
- prep note: [[market-intel/daily/YYYY-MM-DD_next-session-prep|YYYY-MM-DD_next-session-prep]]
- actual recap (fill after close when created): `YYYY-MM-DD_top30_recap`
- prior recap anchor: [[market-intel/daily/PREV-DAY_top30_recap|PREV-DAY_top30_recap]]
- close input: [[market-intel/daily/PREV-DAY_evening-briefing-input|PREV-DAY_evening-briefing-input]]
```

---

## Recommended operating rule
- **pre-open 검토 요청**이 들어오면 우선 `review_mode: prep_review`로 작성한다.
- 같은 note를 장마감 후 replay까지 확장할 수는 있지만, 섹션 제목으로 시점을 분리한다.
- 더 깔끔하게 가려면:
  - pre-open 의견 검토 = 같은 paired review note 상단
  - post-close 복기 = 같은 note 하단 extension

## Review quality checklist
- prep와 hindsight가 섞이지 않았는가?
- 사용자 의견이 별도 snapshot으로 남았는가?
- Hermes verdict가 agree / revise / missing checks / overreach로 분리되었는가?
- prep로 되돌려보낼 최소 수정만 제안했는가?
- prep note와 review note 사이의 양방향 링크가 있는가?
