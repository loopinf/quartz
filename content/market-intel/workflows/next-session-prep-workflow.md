---
id: next-session-prep-workflow
note_type: workflow_rule
created_at: 2026-04-19 20:02:00 KST
updated_at: 2026-04-29 14:45:00 KST
reviewer: 헤르메스(ㅎㅁ)
title: next-session prep workflow
summary: next-session-prep를 recap / briefing / event / entity / high-signal 입력 계층으로 일원화하고, entity를 독립 증거가 아닌 canonical graph memory로 다루는 운영 기준.
---

# next-session prep workflow

## Why this exists
`next-session-prep`는 단순히 전일 브리핑을 한 번 더 요약하는 문서가 아니다.
이 문서는 **다음 세션 장전에 무엇을 먼저 보고, 어떤 구조를 우선 검증할지 정하는 prediction anchor**다.

이번 업데이트의 핵심 목적은 하나다.

> **prep의 실제 입력 체계와 wiki/entity graph를 하나의 canonical workflow로 일원화한다.**

기존에는:
- recap / evening briefing / event note는 prep에서 직접 많이 쓰였고
- stock entity / related-stock graph는 뒤쪽 저장소처럼 축적되고 있었지만
- prep 생성 규칙 안에서 entity를 **공식 입력층**으로 다루는 표현이 약했다.

이 문서는 그 gap을 닫는다.

---

## One-line operating rule

`next-session-prep`는 아래 입력 계층을 순서대로 읽어 **한 장전 판단 surface**로 압축한다.

1. **recent validated recap chain** — 최근 5거래일 구조
2. **prior close context** — evening-briefing-input / evening-briefing
3. **prior event proof** — exact-date event notes
4. **entity memory layer** — stock entity의 event history / related stocks / theme tags
5. **high-signal technical layer** — breakout / near-high / outcome lookup

중요:
- **entity는 canonical memory다.**
- 하지만 **entity alone은 독립 증거가 아니다.**
- prep의 핵심 주장과 우선순위는 항상 **recap / event / technical fact**로 trace 가능해야 한다.

---

## Canonical source priority

### Tier 1 — mandatory evidence anchors
반드시 먼저 보는 층:
- `market-intel/daily/YYYY-MM-DD_top30_recap.md`
- `market-intel/daily/YYYY-MM-DD_evening-briefing-input.md`
- `market-intel/daily/YYYY-MM-DD_evening-briefing.md` (있으면)
- 최근 5거래일 validated recap chain

이 층이 prep의 **기본 근거층**이다.

### Tier 2 — event proof layer
그다음 붙는 층:
- prior-date exact event notes
- theme momentum notes
- close-context에서 만들어진 proof links

이 층은
- 왜 그 군집을 leader / expansion / residual로 읽는지
- 어떤 headline / interpretation bridge가 붙는지
를 설명한다.

### Tier 3 — entity memory layer
이제 공식 입력으로 승격되는 층:
- `market-intel/entities/stocks/<종목>.md`
- `Theme Tags`
- `Event History`
- `Related Stocks`

이 층의 역할은 세 가지다.
1. **반복 등장 기억** — 이 이름이 최근 어떤 event chain에 자주 등장했는가
2. **확장 후보 확인** — related stocks를 통해 2차 확산 후보가 누구인가
3. **theme label 정렬** — prep bucket과 entity graph의 vocabulary를 맞춘다

하지만 금지 규칙도 명확하다.
- entity page에 적혀 있다고 해서 그 자체를 prep의 독립 근거로 쓰지 않는다.
- entity에서 읽은 내용은 반드시 다시
  - prior recap
  - prior event proof
  - same-window high-signal fact
  중 하나 이상으로 연결해야 한다.

### Tier 4 — high-signal technical layer
마지막 fact-upgrade 층:
- breakout / near-52w / near-ATH snapshot
- overlap names
- stock-specific / basket outcome lookup
- conditional probability / entry-rule audit path

이 층은 leader continuity / expansion / follow-through의 **기술 확인** 역할을 한다.

---

## Entity usage rule

### Core principle
entity는 prep를 위한 **운영 메모리**지만,
prep의 주장 자체를 대신하는 **증거 문서**는 아니다.

### Correct use
좋은 사용:
- "문배철강 entity에서 related stocks가 아주스틸 / 부국철강으로 묶여 있으니, 철강 leader 유지 시 2차 확산 후보로 같이 본다"
- "로보티즈 entity event history를 보니 최근 로봇 event chain에 반복 등장했으므로, 이번에도 공동 주도 여부를 확인한다"

이 경우에도 실제 prep 문장에는 함께 붙어야 한다.
- prior recap anchor
- prior event proof
- high-signal overlap 또는 absence note

### Wrong use
나쁜 사용:
- "entity에 있으니 leader다"
- "related stocks에 있으니 그냥 priority bucket에 넣는다"
- "후행적으로 업데이트된 entity를 과거 prep의 원래 판단 근거처럼 쓴다"

### Look-ahead guard
prep는 ex-ante 문서다.
따라서 entity를 쓰더라도:
- **대상 종목은 prior-close source에서 올라온 이름**이어야 하고
- entity에서 읽은 해석도 **그 시점 이전에 설명 가능한 범위**여야 한다.

실무 rule:
- entity는 `memory lookup`
- recap / event / high-signal은 `proof lookup`

---

## Canonical prep build order

### Step 1. recent 5-day structure 잡기
최근 5거래일 validated recap을 보고
- 집중 → 분산 → 재선별 흐름
- 반복 등장 theme
- 직전일과 충돌하는 중기 반복축
을 정리한다.

### Step 2. prior close base case 잡기
직전일 recap + close input/output으로
- breadth leader
- close-context narrative
- next-open base case
를 적는다.

### Step 3. prior event proof 붙이기
exact-date event notes로
- theme별 근거 링크
- 직접/간접/확산 해석
- prior-close narrative의 source trail
을 붙인다.

### Step 4. entity memory check 수행
priority names 후보에 대해 entity를 본다.
확인할 것:
- theme tags가 현재 bucket과 맞는가
- recent event history가 반복성을 뒷받침하는가
- related stocks에서 2차 확산 후보가 무엇인가

이 단계의 산출물은 적어도 두 섹션으로 남긴다.
- `## Entity memory check`
- `## Related stocks expansion check`

### Step 5. technical fact layer 붙이기
high-signal overlap / entry-rule lookup으로
- leader continuity의 기술 확인
- expansion 후보의 기술 확인 또는 부재
- operator-facing historical rule summary
를 붙인다.

### Step 6. 장전 실행 문장으로 압축
최종적으로 아래를 만든다.
- priority watch order
- open checklist
- failure / invalidation conditions
- one-line prep

---

## Required frontmatter / provenance rule
prep note는 최소 아래 provenance 필드를 유지한다.
- `source_note`
- `supporting_notes`
- `entity_inputs`
- `reconstruction_mode` (backfill인 경우)
- `lookahead_guard`
- `lookahead_cutoff_kst`
- `allowed_sources`
- `excluded_sources`

특히 `entity_inputs`는:
- prep가 어떤 stock entity pages를 공식 memory input으로 봤는지 남기는 필드다.
- 하지만 이 목록이 있다고 해서 entity가 독립 증거가 되는 것은 아니다.

---

## Required sections

### 1. Why this note exists
- prediction anchor 역할
- target session date 명시
- same-day intraday/close exclusion 명시

### 2. Recent 5 trading days synthesized context
- 최근 5거래일 recap chain
- 집중/분산/재선별 구조
- 반복 theme 빈도

### 3. Base context available before the open
- validated recap anchor
- close-context anchor
- prior event proof

### 4. Entity memory check
반드시 들어갈 내용:
- priority entity link
- entity theme tags
- latest event history snapshot
- related stocks expansion hints
- provenance rule 문장

### 5. Related stocks expansion check
- entity graph에서 끌어온 2차 확산 후보
- leader-linked / expansion-linked / residual-linked 구분
- blind promotion 금지 문장

### 6. High-signal fact layer
- breakout / near-high overlap
- overlap 부재 시 그 사실 자체
- proof bundle

### 7. Carry-over themes / hypotheses
- leader / expansion / residual rationale
- 추천이 아니라 observation priority임을 명시

### 8. Priority names / sectors
- leader 확인
- 공동 주도 / expansion 확인
- residual / re-check 확인

### 9. Open checklist
- open 5~30분 내 확인할 포인트

### 10. Failure / invalidation conditions
- 무엇을 보면 시나리오를 낮출지

### 11. One-line prep
- manager-facing 요약 한 줄

### 12. Follow-up note / paired review handoff
- prep는 ex-ante anchor임을 다시 명시
- paired review note 경로를 남긴다
- review/replay는 별도 문서에서 처리한다고 못박는다

### 13. Review request scaffold
- `My review notes`
- `Hermes review request`
- `review_request_status`
- `paired_review_target`

---

## Automation rule
`ensure_next_session_prep.py` 같은 자동 scaffold도 이제 아래 방향을 따라야 한다.
- recap / close input / recent recap chain을 기본으로 읽는다.
- priority names에 연결되는 stock entity가 있으면 `entity_inputs`를 frontmatter에 남긴다.
- 본문에 `Entity memory check`와 `Related stocks expansion check`를 자동 scaffold로 추가한다.
- 단, entity는 **memory lookup only**라는 guardrail 문장을 함께 넣는다.
- prep 하단에 `Follow-up note` / `My review notes` / `Hermes review request` scaffold를 같이 남긴다.
- 가능하면 같은 날짜의 paired review stub도 같이 생성하되, same-day actual recap은 live wikilink로 미리 걸지 말고 placeholder text로 둔다.

즉 자동화 목표는:
- wiki를 예쁘게 쌓는 것
이 아니라
- **wiki가 실제 prep를 공급하는 운영 메모리**가 되게 만드는 것이다.

---

## Verification checklist
성공 기준:
- prep가 recap / briefing / event / entity / high-signal 계층을 모두 가진다.
- entity section이 실제로 priority names와 연결된다.
- related stocks가 보이되 blind recommendation처럼 읽히지 않는다.
- prep의 각 핵심 주장에 proof anchor가 있다.
- entity를 제거해도 proof는 남고,
  proof만 남기면 related-stock expansion memory가 약해지는 구조여야 한다.

실패 신호:
- entity 링크가 하나도 없는데 workflow만 entity-first라고 써둔 경우
- entity를 근거처럼 쓰지만 recap/event/high-signal 출처가 없는 경우
- related stocks를 priority bucket으로 승격시켰는데 why-now가 없는 경우

---

## Review / replay boundary for entity graph
paired review에서도 entity graph는 무제한으로 쓰지 않는다.
- `prep review` 단계에서는 **prep cutoff 이전에 이미 knowable했던 graph**만 검토 대상으로 삼는다.
- later-enriched entity 문장이나 post-close에 추가된 event/entity link는 hindsight layer로 분리 표기한다.
- review note의 verdict는 여전히 recap / event proof / high-signal fact layer로 역추적 가능해야 한다.
- 짧게 말하면:
  - `prep = proof lookup + memory lookup`
  - `prep review = knowable graph boundary audit`
  - `post-close replay = hindsight extension, but clearly labeled`

---

## One-line rule
**prep는 recap/event/high-signal이 증거층이고, entity는 그 증거를 이어주는 canonical memory 층이다. 이 둘을 분리하되 workflow 안에서는 반드시 함께 움직이게 만든다.**
