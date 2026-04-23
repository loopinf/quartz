---
id: market-intel-recent-changes
created_at: 2026-04-16 15:23:49 KST
updated_at: 2026-04-23 05:56:00 KST
reviewer: 헤르메스(ㅎㅁ)
---

# Market Intel Recent Changes

## 2026-04-23 05:56:00 KST — missing evening briefing + next-session prep filled for readiness recovery

### Added to market-intel
- Daily note: [[market-intel/daily/2026-04-22_evening-briefing|2026-04-22_evening-briefing]]
- Daily note: [[market-intel/daily/2026-04-23_next-session-prep|2026-04-23_next-session-prep]]

### Updated
- Status board: [[current-readiness-board|current-readiness-board]]
- Root landing: `~/market-intel-site/content/index.md`
- Index: [[index]]
- Daily hub: [[daily/index|daily/index]]
- Prediction workspace: [[market-intel/research/prediction-workspace|prediction-workspace]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- readiness board에서 비어 있던 핵심 gap 두 개(`2026-04-22_evening-briefing`, `2026-04-23_next-session-prep`)를 실제 문서로 채웠다.
- 4/22 evening briefing은 `이차전지 초집중 → 로봇/반도체소부장/조선기자재 분산`으로의 전환을 요약하고, 4/23 장전 핵심 질문을 정리했다.
- 4/23 next-session prep은 4/22 validated recap + evening briefing을 anchor로 삼아 로봇/반도체소부장 이중 주도축 유지 여부를 장전 체크포인트로 올렸다.
- 이 변경으로 readiness board의 core readiness는 green에 더 가까워졌고, 남은 운영 gap은 same-day source archive 쪽으로 더 분명히 보이게 됐다.

## 2026-04-23 05:46:30 KST — readiness board expanded to operational checklist

### Updated
- Quartz layout: `/Users/gbserver/market-intel-site/quartz.layout.ts`
- Entry generator: `/Users/gbserver/market-intel-site/scripts/update_market_intel_entrypoints.py`
- Progress overview: [[market-intel-progress-big-picture]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- left explorer가 사실상 비어 보여 navigation이 막히는 문제가 있어서, sidebar filter를 `엄격한 keep-set만 표시` 방식에서 `market-intel 루트 문서 + 주요 폴더 허브 + current 문서`가 보이도록 완화했다.
- explorer에 `folderClickBehavior: link`를 명시해, 폴더 이름 자체도 더 자연스럽게 navigation entry로 쓰게 했다.
- `market-intel-progress-big-picture` 상단에도 `여기서 바로 이동` 링크 묶음을 추가해, 홈/진행상황판/변경로그/daily/SOT로 바로 튀게 했다.

## 2026-04-23 05:47:14 KST — big-picture lane view switched from mermaid to card-style summary

### Updated
- Status board: [[current-readiness-board|current-readiness-board]]
- Root landing: `~/market-intel-site/content/index.md`
- Index: [[index]]
- Daily hub: [[daily/index|daily/index]]
- Prediction workspace: [[market-intel/research/prediction-workspace|prediction-workspace]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 기존 readiness board가 `prep / validated recap / close input` 3개만 보여줘서, 실제 운영 체크리스트로는 아직 좁았다.
- 그래서 `final evening briefing output`과 `same-day source archive`까지 추가해 **문서 readiness + 운영 체크**를 함께 보게 했다.
- same-day archive는 장전/장중에는 `WAITING`, 장후에는 `READY/MISSING`으로 해석하도록 phase-aware 판정 규칙을 넣었다.
- readiness board가 이제 단순 문서 링크 모음이 아니라, "지금 시점에 뭐가 준비됐고 뭐가 아직 운영상 비어 있는지"를 한눈에 보는 현황판 역할을 하게 됐다.

## 2026-04-23 05:41:41 KST — automatic readiness board added + progress/readiness split clarified

### Updated
- Progress overview: [[market-intel-progress-big-picture]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- `한눈에 보는 lane 맵`을 Mermaid 대신 고정폭 텍스트 기반 카드형 요약으로 바꿨다.
- 핵심 흐름은 `Source → Ingest → Graph → Briefing → Replay → Research`로 유지하되, Quartz에서 글자가 작아지는 문제를 피하려고 도형 수를 줄이고 텍스트를 직접 크게 읽히는 블록으로 분리했다.
- 상태도 별도 `상태만 바로 보기` 블록으로 분리해, 흐름과 현재 상태를 섞지 않게 했다.

## 2026-04-23 05:41:41 KST — automatic readiness board added + progress/readiness split clarified

### Added to market-intel
- Status board: [[current-readiness-board|current-readiness-board]]

### Updated
- Root landing: `/Users/gbserver/market-intel-site/content/index.md`
- Index: [[index]]
- Daily hub: [[daily/index|daily/index]]
- Prediction workspace: [[market-intel/research/prediction-workspace|prediction-workspace]]
- Progress overview: [[market-intel-progress-big-picture]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 기존 index/daily 화면에 readiness는 있었지만, **자동 확인이 실제로 들어가 있는지**와 **장기 진행상황 vs 현재 세션 현황**의 구분이 한눈에 보이지 않았다.
- 그래서 sync/build 시점 자동 판정 결과만 모아 보여주는 `current-readiness-board`를 새로 만들고, root/home/daily/prediction에서 이 보드로 바로 들어가게 했다.
- readiness board에는 자동 트리거, 실제 판정 로직, 판정 대상 문서, 현재 반영 위치, 현재 구조의 한계(sync/build 시점 자동화)를 명시했다.
- `market-intel-progress-big-picture`는 장기 로드맵/큰그림 문서로 두고, 오늘 세션 준비 현황은 readiness board를 먼저 보라고 역할을 분리했다.

## 2026-04-23 05:31:44 KST — index readiness refresh + terminology cleanup

### Updated
- Root landing: `/Users/gbserver/market-intel-site/content/index.md`
- Index: [[index]]
- Daily hub: [[daily/index|daily/index]]
- Prediction workspace: [[market-intel/research/prediction-workspace|prediction-workspace]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- index / daily hub / prediction workspace를 `최근 작업한 문서 나열`이 아니라 **지금 세션에 필요한 문서가 최신인지 확인하는 readiness 화면**으로 다시 정리했다.
- `2026-04-23 장전` 기준으로 `오늘 세션 prep` target은 `2026-04-23_next-session-prep`여야 하는데 아직 없다는 점을 `MISSING`으로 명시하고, fallback `2026-04-22_next-session-prep`를 따로 보여주게 했다.
- `직전 validated recap` / `직전 close input`은 `직전 작업물`이 아니라 **현재 세션 바로 직전 장 기준 문서**라는 뜻으로 용어를 다시 정리했다.
- Quartz explorer도 stale한 `오늘 prep` 라벨 대신 `latest prep fallback` / `직전 장 validated recap` / `직전 장 close input` 중심으로 보이게 맞췄다.

## 2026-04-23 04:52:30 KST — big-picture mermaid simplified for readability

### Updated
- Workflow status: [[market-intel-progress-big-picture]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 기존 lane Mermaid는 박스 수와 텍스트가 많아 한눈에 잘 안 들어오는 문제가 있어서, `Source → Ingest → Graph → Briefing → Replay → Research (+ Publish)`의 초간단 세로 흐름으로 줄였다.
- 세부 설명은 Mermaid 안에 다 넣지 않고, 바로 아래 `각 박스 뜻` bullet로 분리해 글자 가독성을 높였다.
- 상태판도 lane 이름 기준으로 다시 축약해, 시각 흐름과 상태 요약이 서로 섞이지 않게 정리했다.

## 2026-04-23 04:48:38 KST — big-picture mermaid refresh + root overview update

### Added to market-intel
- Root overview refresh: `/Users/gbserver/Documents/Obsidian Vault/overview.md`

### Updated
- Workflow status: [[market-intel-progress-big-picture]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 루트 `overview.md`를 현재 상태에 맞게 다시 정리해, 원래 목표 / 지금까지 한 일 / 현재 위치 / 다음 단계 / 실제 참조 문서를 한 번에 보게 했다.
- `market-intel-progress-big-picture`에 Mermaid lane map을 추가해, same-day source → validated ingest → graph update → briefing → replay/research → Quartz publish 흐름을 시각적으로 파악할 수 있게 했다.
- 현재 어떤 축은 이미 작동 중이고, 어떤 축은 아직 강화가 필요한지(특히 same-day acquisition 안정화와 final briefing output 고정)를 상단에서 바로 읽을 수 있게 했다.

## 2026-04-22 22:56:35 KST — JMKR TOP30 archive ingest (2026-04-22)

### Added to market-intel
- Daily note: [[market-intel/daily/2026-04-22_top30_recap|2026-04-22_top30_recap]]
- Event: [[market-intel/events/2026-04-22_로봇_모멘텀|2026-04-22_로봇_모멘텀]]
- Event: [[market-intel/events/2026-04-22_반도체소부장_모멘텀|2026-04-22_반도체소부장_모멘텀]]
- Event: [[market-intel/events/2026-04-22_조선기자재_모멘텀|2026-04-22_조선기자재_모멘텀]]
- Event: [[market-intel/events/2026-04-22_데이터센터_모멘텀|2026-04-22_데이터센터_모멘텀]]
- Event: [[market-intel/events/2026-04-22_바이오에너지_모멘텀|2026-04-22_바이오에너지_모멘텀]]
- Event: [[market-intel/events/2026-04-22_이차전지_모멘텀|2026-04-22_이차전지_모멘텀]]

### Updated
- Entity: [[market-intel/entities/stocks/핑거|핑거]]
- Entity: [[market-intel/entities/stocks/라이온켐텍|라이온켐텍]]
- Entity: [[market-intel/entities/stocks/정원엔시스|정원엔시스]]
- Entity: [[market-intel/entities/stocks/에이에프더블류|에이에프더블류]]
- Entity: [[market-intel/entities/stocks/동일스틸럭스|동일스틸럭스]]
- Entity: [[market-intel/entities/stocks/포톤|포톤]]
- Entity: [[market-intel/entities/stocks/KEC|KEC]]
- Entity: [[market-intel/entities/stocks/DS단석|DS단석]]
- Entity: [[market-intel/entities/stocks/나노캠텍|나노캠텍]]
- Entity: [[market-intel/entities/stocks/애머릿지|애머릿지]]
- Entity: [[market-intel/entities/stocks/바이젠셀|바이젠셀]]
- Entity: [[market-intel/entities/stocks/플루토스|플루토스]]
- Entity: [[market-intel/entities/stocks/썸에이지|썸에이지]]
- Entity: [[market-intel/entities/stocks/케이알엠|케이알엠]]
- Entity: [[market-intel/entities/stocks/나노|나노]]
- Entity: [[market-intel/entities/stocks/애경케미칼|애경케미칼]]
- Entity: [[market-intel/entities/stocks/OCI|OCI]]
- Entity: [[market-intel/entities/stocks/삼아알미늄|삼아알미늄]]
- Entity: [[market-intel/entities/stocks/미래에셋벤처투자|미래에셋벤처투자]]
- Entity: [[market-intel/entities/stocks/케이프|케이프]]
- Entity: [[market-intel/entities/stocks/이수페타시스|이수페타시스]]
- Entity: [[market-intel/entities/stocks/SGC에너지|SGC에너지]]
- Entity: [[market-intel/entities/stocks/에이프로|에이프로]]
- Entity: [[market-intel/entities/stocks/아모그린텍|아모그린텍]]
- Entity: [[market-intel/entities/stocks/아이엘|아이엘]]
- Entity: [[market-intel/entities/stocks/LG이노텍|LG이노텍]]
- Entity: [[market-intel/entities/stocks/GS글로벌|GS글로벌]]
- Entity: [[market-intel/entities/stocks/이노테크|이노테크]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- validated archive (`2026-04-22.json` / `b56734f77d09cdf9a336fc55d6572f7d0c10ebecb9dcc7420de01a6665d88210`)만 ingest 대상으로 통과시켰다.
- stock entity 중심으로 누적 히스토리를 업데이트하고, 상세 해석은 theme/event note 쪽에 배치했다.
- 중복 ingest 방지를 위해 날짜별 hash/state 기록을 남긴다.

## 2026-04-22 21:20:00 KST — automated breadth-event research system design added

### Added to market-intel
- Workflow: [[market-intel/workflows/automated-breadth-event-research-system|automated-breadth-event-research-system]]

### Updated
- Prediction workspace: [[market-intel/research/prediction-workspace|prediction-workspace]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- breadth 급증, leader/follower 분해, historical analog, entry timing, holding window, conditional probability, playbook 생성을 하나의 자동 연구 시스템으로 묶는 운영 설계 노트를 추가했다.
- 이 설계는 `뉴스 저장`이 아니라 `event detector → research queue → historical analog → conditional probability → execution playbook` 흐름을 명시한다.
- 현재 배터리 breadth 케이스(`2026-04-21 이차전지 모멘텀`)를 첫 benchmark event로 삼아 Phase 1~4 구현 순서를 고정했다.

## 2026-04-22 07:29:27 KST — 8081 daily UX date fix + pre-open entrypoint refresh

### Added to market-intel
- Daily note: [[market-intel/daily/2026-04-22_next-session-prep|2026-04-22_next-session-prep]]

### Updated
- Root landing: `~/market-intel-site/content/index.md`
- Index: [[index]]
- Daily hub: [[daily/index|daily/index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 2026-04-21 validated TOP30 recap이 이미 존재하는데도 루트/홈/데일리 허브가 2026-04-20 기준 recovery 상태를 계속 가리키던 문제를 정정했다.
- `오늘`의 의미를 **2026-04-22 KST 장전**으로 명시하고, 어제 장마감 문서(4/21 recap, 4/21 close input)와 오늘 장전 문서(4/22 prep)를 분리해 전면에 배치했다.
- 오래된 `2026-04-20_next-session-prep`를 첫 진입 CTA로 쓰지 않도록 흐름을 `today prep → last validated recap → last close input`으로 재구성했다.

## 2026-04-21 22:56:43 KST — JMKR TOP30 archive ingest (2026-04-21)

### Added to market-intel
- Daily note: [[market-intel/daily/2026-04-21_top30_recap|2026-04-21_top30_recap]]
- Event: [[market-intel/events/2026-04-21_이차전지_모멘텀|2026-04-21_이차전지_모멘텀]]
- Event: [[market-intel/events/2026-04-21_로봇_모멘텀|2026-04-21_로봇_모멘텀]]

### Updated
- Entity: [[market-intel/entities/stocks/정원엔시스|정원엔시스]]
- Entity: [[market-intel/entities/stocks/씨아이에스|씨아이에스]]
- Entity: [[market-intel/entities/stocks/주성엔지니어링|주성엔지니어링]]
- Entity: [[market-intel/entities/stocks/한중엔시에스|한중엔시에스]]
- Entity: [[market-intel/entities/stocks/에이에프더블류|에이에프더블류]]
- Entity: [[market-intel/entities/stocks/애머릿지|애머릿지]]
- Entity: [[market-intel/entities/stocks/씨이랩|씨이랩]]
- Entity: [[market-intel/entities/stocks/벨로크|벨로크]]
- Entity: [[market-intel/entities/stocks/화인써키트|화인써키트]]
- Entity: [[market-intel/entities/stocks/국일제지|국일제지]]
- Entity: [[market-intel/entities/stocks/이브이첨단소재|이브이첨단소재]]
- Entity: [[market-intel/entities/stocks/중앙첨단소재|중앙첨단소재]]
- Entity: [[market-intel/entities/stocks/파인텍|파인텍]]
- Entity: [[market-intel/entities/stocks/솔루스첨단소재|솔루스첨단소재]]
- Entity: [[market-intel/entities/stocks/지에프아이|지에프아이]]
- Entity: [[market-intel/entities/stocks/APS이노베이션|APS이노베이션]]
- Entity: [[market-intel/entities/stocks/제이오|제이오]]
- Entity: [[market-intel/entities/stocks/삼성SDI|삼성SDI]]
- Entity: [[market-intel/entities/stocks/필에너지|필에너지]]
- Entity: [[market-intel/entities/stocks/엠플러스|엠플러스]]
- Entity: [[market-intel/entities/stocks/엔켐|엔켐]]
- Entity: [[market-intel/entities/stocks/삼기에너지솔루션즈|삼기에너지솔루션즈]]
- Entity: [[market-intel/entities/stocks/HD현대마린솔루션|HD현대마린솔루션]]
- Entity: [[market-intel/entities/stocks/삼천리자전거|삼천리자전거]]
- Entity: [[market-intel/entities/stocks/선익시스템|선익시스템]]
- Entity: [[market-intel/entities/stocks/대우건설|대우건설]]
- Entity: [[market-intel/entities/stocks/이랜텍|이랜텍]]
- Entity: [[market-intel/entities/stocks/킵스파마|킵스파마]]
- Entity: [[market-intel/entities/stocks/KEC|KEC]]
- Entity: [[market-intel/entities/stocks/우진플라임|우진플라임]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- validated archive (`2026-04-21.json` / `9d19de3d1b4e310db4a5335a2ad305e2fb7d16cc7bcd647fb9e11d97cdff9ff9`)만 ingest 대상으로 통과시켰다.
- stock entity 중심으로 누적 히스토리를 업데이트하고, 상세 해석은 theme/event note 쪽에 배치했다.
- 중복 ingest 방지를 위해 날짜별 hash/state 기록을 남긴다.

## 2026-04-21 19:06:13 KST — JMKR TOP30 archive ingest (2026-04-20)

### Added to market-intel
- Daily note: [[market-intel/daily/2026-04-20_top30_recap|2026-04-20_top30_recap]]
- Event: [[market-intel/events/2026-04-20_양자-양자암호_모멘텀|2026-04-20_양자-양자암호_모멘텀]]
- Event: [[market-intel/events/2026-04-20_보안_모멘텀|2026-04-20_보안_모멘텀]]
- Event: [[market-intel/events/2026-04-20_이차전지_모멘텀|2026-04-20_이차전지_모멘텀]]
- Event: [[market-intel/events/2026-04-20_게임_모멘텀|2026-04-20_게임_모멘텀]]
- Event: [[market-intel/events/2026-04-20_디스플레이_모멘텀|2026-04-20_디스플레이_모멘텀]]
- Event: [[market-intel/events/2026-04-20_디지털화폐_모멘텀|2026-04-20_디지털화폐_모멘텀]]

### Updated
- Entity: [[market-intel/entities/stocks/에스아이리소스|에스아이리소스]]
- Entity: [[market-intel/entities/stocks/파인텍|파인텍]]
- Entity: [[market-intel/entities/stocks/씨이랩|씨이랩]]
- Entity: [[market-intel/entities/stocks/벨로크|벨로크]]
- Entity: [[market-intel/entities/stocks/한국정보통신|한국정보통신]]
- Entity: [[market-intel/entities/stocks/드림시큐리티|드림시큐리티]]
- Entity: [[market-intel/entities/stocks/주성엔지니어링|주성엔지니어링]]
- Entity: [[market-intel/entities/stocks/로지시스|로지시스]]
- Entity: [[market-intel/entities/stocks/혜인|혜인]]
- Entity: [[market-intel/entities/stocks/삼천리자전거|삼천리자전거]]
- Entity: [[market-intel/entities/stocks/SGA솔루션즈|SGA솔루션즈]]
- Entity: [[market-intel/entities/stocks/케이씨에스|케이씨에스]]
- Entity: [[market-intel/entities/stocks/위메이드맥스|위메이드맥스]]
- Entity: [[market-intel/entities/stocks/제이오|제이오]]
- Entity: [[market-intel/entities/stocks/나이스정보통신|나이스정보통신]]
- Entity: [[market-intel/entities/stocks/동아엘텍|동아엘텍]]
- Entity: [[market-intel/entities/stocks/더코디|더코디]]
- Entity: [[market-intel/entities/stocks/라닉스|라닉스]]
- Entity: [[market-intel/entities/stocks/오로라|오로라]]
- Entity: [[market-intel/entities/stocks/상신이디피|상신이디피]]
- Entity: [[market-intel/entities/stocks/위메이드|위메이드]]
- Entity: [[market-intel/entities/stocks/삼진엘앤디|삼진엘앤디]]
- Entity: [[market-intel/entities/stocks/DB하이텍|DB하이텍]]
- Entity: [[market-intel/entities/stocks/엠아이큐브솔루션|엠아이큐브솔루션]]
- Entity: [[market-intel/entities/stocks/미코|미코]]
- Entity: [[market-intel/entities/stocks/에스피소프트|에스피소프트]]
- Entity: [[market-intel/entities/stocks/퍼스텍|퍼스텍]]
- Entity: [[market-intel/entities/stocks/한컴위드|한컴위드]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- validated archive (`2026-04-20.json` / `6c5f6fb70d7cddb9772363e82cc2c96bc0457469887549532fa0e2808fa749f1`)만 ingest 대상으로 통과시켰다.
- stock entity 중심으로 누적 히스토리를 업데이트하고, 상세 해석은 theme/event note 쪽에 배치했다.
- 중복 ingest 방지를 위해 날짜별 hash/state 기록을 남긴다.

## 2026-04-21 18:24:12 KST — 2026-04-21 evening briefing input recovery-status 추가

### Added to market-intel
- Daily note: [[daily/2026-04-21_evening-briefing-input|2026-04-21_evening-briefing-input]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 오늘자 JMKR archive(`2026-04-21.json`) 부재를 다시 확인했고, validated ingest는 강제로 돌리지 않고 recovery-status 입력 노트로 상태를 명시했다.
- 이번에는 same-day `sage-analysis` / `collected` 로컬 산출물이 존재해서, breadth·상한가 수·거래집중도와 함께 **배터리/2차전지 주도 흔적**을 partial-input 레벨에서 기록했다.
- 즉 오늘 입력은 validated TOP30 recap이 아니라, `archive missing + same-day local breadth present` 상태를 분리해서 보여주는 장마감 입력 노트다.

## 2026-04-21 12:31:57 KST — multi-horizon path dataset schema 추가

### Added to market-intel
- Research schema: [[research/multi-horizon-path-dataset-schema|multi-horizon-path-dataset-schema]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- replay / success case / high-signal 결과를 같은 primary path vocabulary(`immediate_continuation`, `delayed_spread`, `reignition`, `one_day_fade`, `false_strength`)로 묶는 최소 공통 schema를 추가했다.
- `event / state / path` 3층을 분리하고, D+1과 D+2~5 구간을 나눠 기록하는 기준을 명시해 path dataset 강화 방향을 문서로 고정했다.
- 아직 JSON export를 강제하기보다 먼저 field meaning과 label vocabulary를 8081에서 사람이 바로 검토할 수 있게 만들었다.

## 2026-04-21 11:17:45 KST — Quartz 링크 검증 workflow + validator script 추가

### Added to market-intel
- Workflow rule: [[workflows/quartz-link-validation-workflow|quartz-link-validation-workflow]]
- Script: [[scripts/validate_quartz_links.py|validate_quartz_links.py]]

### Updated
- Research sample: [[research/portfolio-pilot-2025-04-18-context-and-candidates|portfolio-pilot-2025-04-18-context-and-candidates]]
- Research sample: [[research/portfolio-pilot-2026-03-23-context-and-candidates|portfolio-pilot-2026-03-23-context-and-candidates]]
- Research sample: [[research/portfolio-pilot-2026-03-24-context-and-candidates|portfolio-pilot-2026-03-24-context-and-candidates]]
- Research sample: [[research/portfolio-pilot-2026-03-25-context-and-candidates|portfolio-pilot-2026-03-25-context-and-candidates]]
- Research sample: [[research/portfolio-pilot-2026-03-26-context-and-candidates|portfolio-pilot-2026-03-26-context-and-candidates]]
- Research sample: [[research/portfolio-pilot-2026-03-27-context-and-candidates|portfolio-pilot-2026-03-27-context-and-candidates]]
- Research batch note: [[research/portfolio-pilot-batch-additional-samples|portfolio-pilot-batch-additional-samples]]
- Research dashboard: [[research/portfolio-pilot-review-dashboard|portfolio-pilot-review-dashboard]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- Quartz 미리보기(`127.0.0.1:8081` / `localhost:8081`)에서 변경된 market-intel 페이지와 그 내부 링크를 자동으로 다시 fetch해 404를 push 전에 잡는 검증 루틴을 추가했다.
- 실제로 깨져 있던 portfolio pilot sample/dashboard 링크들은 `market-intel/...` 기준으로 다시 연결해 Quartz에서 클릭 검증까지 통과시켰다.
- 이제 publish 직후에는 markdown 원문만 보지 않고, Quartz-visible page + internal link 200 OK를 함께 확인하는 운영 규칙을 기본으로 둔다.

## 2026-04-20 23:05:00 KST — portfolio pilot review dashboard + batch summary JSON 추가

### Added to market-intel
- Research dashboard: [[research/portfolio-pilot-review-dashboard|portfolio-pilot-review-dashboard]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 내일 아침 검토를 위해 개별 샘플 note들을 하나씩 열어보지 않아도 되도록, 날짜별 5일 성과 / dominant themes / core / support / best/worst member를 한눈에 보는 review dashboard를 추가했다.
- repo 쪽에는 `data/signals/portfolio-review/batch-summary-2026-04-20.json`을 만들어 같은 비교 결과를 machine-readable summary로 저장했다.
- 이제 검토는 `review dashboard -> best/worst sample -> schema doc` 순서로 더 빠르게 진행할 수 있다.

## 2026-04-20 22:47:00 KST — portfolio pilot 추가 샘플 5개 생성

### Added to market-intel
- Research batch note: [[research/portfolio-pilot-batch-additional-samples|portfolio-pilot-batch-additional-samples]]
- Research sample: [[research/portfolio-pilot-2026-03-23-context-and-candidates|portfolio-pilot-2026-03-23-context-and-candidates]]
- Research sample: [[research/portfolio-pilot-2026-03-24-context-and-candidates|portfolio-pilot-2026-03-24-context-and-candidates]]
- Research sample: [[research/portfolio-pilot-2026-03-25-context-and-candidates|portfolio-pilot-2026-03-25-context-and-candidates]]
- Research sample: [[research/portfolio-pilot-2026-03-26-context-and-candidates|portfolio-pilot-2026-03-26-context-and-candidates]]
- Research sample: [[research/portfolio-pilot-2025-04-18-context-and-candidates|portfolio-pilot-2025-04-18-context-and-candidates]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 하나의 2026-03-27 샘플만 보는 대신, 추가로 5개 날짜에 대해 같은 `context-candidates` / `portfolio-candidates` 구조를 반복 적용해 비교 가능한 묶음을 만들었다.
- 각 날짜별로 실제 JSON snapshot과 Quartz-visible 연구 노트를 같이 만들었고, batch note에서 equal-weight 5일 결과와 주요 테마/후보를 빠르게 비교할 수 있게 했다.
- 이로써 스키마가 한 사례에만 맞춘 구조인지, 여러 날짜에 반복 적용해도 읽기/검토가 가능한지 직접 확인할 수 있는 상태가 됐다.

## 2026-04-20 22:37:00 KST — 2026-03-27 context-candidates / portfolio-candidates 샘플 추가

### Added to market-intel
- Research sample: [[research/portfolio-pilot-2026-03-27-context-and-candidates|portfolio-pilot-2026-03-27-context-and-candidates]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 스키마 설명 문서만 있는 상태에서 멈추지 않고, 실제 날짜(`2026-03-27`) 기준 샘플 `context-candidates` / `portfolio-candidates`를 생성해 사람이 검토 가능한 예시를 만들었다.
- 샘플 note에 repo-relative/absolute JSON 경로, 후보 카드 요약, 최종 포트폴리오 구성, retrospective 5일 성과를 함께 적어 Quartz에서도 바로 구조와 사용 예를 확인할 수 있게 했다.
- 이제 "문서만 있고 실제 candidates 파일이 없는 상태"가 아니라, 실제 JSON + Quartz-visible 설명 note가 같이 존재하게 됐다.

## 2026-04-20 09:45:00 KST — context-candidates / portfolio snapshot schema v1 추가

### Added to market-intel
- Workflow rule: [[workflows/context-candidates-and-portfolio-snapshot-schema-v1|context-candidates-and-portfolio-snapshot-schema-v1]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 최근 1주 맥락 -> 5거래일 후보 발굴 루프에서 raw / derived / final-portfolio를 분리 저장해야 한다는 원칙을 문서화했다.
- `context-candidates/YYYY-MM-DD.json`를 중간 계산값 canonical snapshot으로, `portfolio-candidates/YYYY-MM-DD.json`를 최종 판단 snapshot으로 정의했다.
- 각 필드의 의미를 함께 적어 `recent_top30_appearances_5d`, `theme_role`, `signal_type`, `days_in_90_zone`, `candidate_thesis` 같은 값이 왜 필요한지 8081에서 바로 확인할 수 있게 했다.

## 2026-04-20 19:13:51 KST — 2026-04-20 evening briefing input recovery-status 갱신

### Added to market-intel
- Daily note: [[daily/2026-04-20_evening-briefing-input|2026-04-20_evening-briefing-input]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 오늘자 JMKR archive(`2026-04-20.json`) 부재를 확인했고, validated ingest를 억지로 진행하지 않고 recovery-status 입력 노트로 상태를 명시했다.
- 같은 노트에 국내 지수 종가, 미국 Nasdaq/SOX 금요일장 carry, 최근 3거래일 continuity, latest ingest state를 묶어 둬서 archive 복구 전에도 저녁 브리핑의 최소 판단 재료를 볼 수 있게 했다.
- 즉 오늘 입력은 `validated same-day recap`이 아니라 `archive-missing recovery note`라는 점을 Quartz/Obsidian에서 바로 확인할 수 있게 됐다.

## 2026-04-19 21:37:00 KST — 코로나 군집 연속성 판단 프레임워크 추가

### Added to market-intel
- Research framework: [[research/corona-cluster-continuation-judgment-framework|corona-cluster-continuation-judgment-framework]]

### Updated
- Event note: [[events/2026-04-17_코로나_모멘텀|2026-04-17_코로나_모멘텀]]
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- Hankyung search를 실제 source surface로 확인하고, `BA.3.2(시카다)` 일반 확산 기사 + 질병청/공식 확인 기사 + 오상헬스케어 종목-specific 기사까지 묶어 코로나 군집 follow-up source 층을 보강했다.
- 코로나 군집이 더 갈지/죽을지 판단하기 위해 breadth, leader quality, 뉴스 확인층, 국장 분위기, high-signal overlap 등을 조건부 확률 후보 변수로 정리한 연구 프레임워크를 추가했다.
- 즉 코로나 군집은 단순 headline read가 아니라, 다음부터는 `cluster breadth + follow-up news + leader quality + technical support` 조합으로 continuation 판단을 더 구조화할 수 있게 됐다.

## 2026-04-19 21:26:00 KST — runbook 실전 1회전 예시 추가 (2026-04-16 -> 2026-04-17)

### Added to market-intel
- Daily briefing: [[daily/2026-04-16_evening-briefing|2026-04-16_evening-briefing]]
- Next-session prep: [[daily/2026-04-17_next-session-prep|2026-04-17_next-session-prep]]

### Updated
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 4월 초 테스트용 날짜를 찾았지만, 현재 JMKR archive 기준으로 `2026-04-01 ~ 2026-04-15` same-day archive가 없어서 실제 source-acquisition 기반 runbook 예시는 가장 이른 4월 archive 가용일인 `2026-04-16 -> 2026-04-17`로 실행했다.
- 이로써 close 기준 `evening-briefing`과 다음 세션용 `next-session-prep`을 실제로 한 번 이어서 만들어, 문서 체인이 실운영에 어떻게 쓰일지 예시를 남겼다.
- 특히 4/16의 보안+양자/PQC 연속성 해석이 4/17 장전 prep에서 어떻게 continuation 시나리오와 rotation 시나리오로 번역돼야 하는지 구조화했다.

## 2026-04-19 21:18:00 KST — one-cycle operating runbook 추가

### Added to market-intel
- Workflow runbook: [[workflows/one-cycle-operating-runbook|one-cycle-operating-runbook]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 지금 시점에서 가장 중요한 다음 액션을 "새 추상 문서 추가"가 아니라, 이미 만든 lane들을 실제 하루~다음 세션 기준으로 한 번 끝까지 돌려보는 실전 runbook으로 정리했다.
- close -> validated ingest -> graph update -> evening briefing -> next-session prep -> intraday handoff -> close recap/replay candidate 순서를 실제 운영 절차로 고정했다.
- 이 문서를 기준으로 실제 1회전을 돌려보면, 어디서 시간이 많이 드는지 / 어떤 팩트가 부족한지 / 어떤 문서가 실사용성이 낮은지 드러나게 된다.

## 2026-04-19 21:14:00 KST — high-signal -> path/review linking workflow 추가

### Added to market-intel
- Workflow rule: [[workflows/high-signal-path-review-linking-workflow|high-signal-path-review-linking-workflow]]

### Updated
- Workflow roadmap: [[workflows/lane-definition-roadmap|lane-definition-roadmap]]
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- high-signal watchlist가 isolated technical 랭킹으로 남지 않고, next-session prep -> intraday/daily outcome -> replay/success case -> path label 구조로 이어져야 한다는 기준을 고정했다.
- 어떤 high-signal 후보를 prep에 흡수하고, 어떤 경우 success case / failure replay 후보로 승격할지의 linking rule을 만들었다.
- 이로써 technical signal lane이 실제 시장 판단/복기 체계와 연결되는 접점을 문서화했다.

## 2026-04-19 21:07:00 KST — intraday/live note vs daily recap boundary workflow 추가

### Added to market-intel
- Workflow rule: [[workflows/intraday-vs-daily-boundary-workflow|intraday-vs-daily-boundary-workflow]]

### Updated
- Workflow rule: [[workflows/next-session-prep-workflow|next-session-prep-workflow]]
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- next-session-prep을 어디까지 업데이트하고, 정규장 시작 이후의 변화는 어디에 기록할지에 대한 경계를 명시했다.
- prep / intraday-live / daily recap / replay의 역할을 분리해, 장전 계획 문서가 장중 로그나 마감 요약으로 오염되지 않도록 기준을 만들었다.
- 당장은 full intraday lane을 항상 강제하지 않고, replay 가치가 높은 날에 우선 intraday/live note를 쓰는 실용적 기준으로 정리했다.

## 2026-04-19 21:00:56 KST — next-session prep timing/update windows 보강

### Updated
- Workflow rule: [[workflows/next-session-prep-workflow|next-session-prep-workflow]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- next-session prep을 언제 갱신해야 하는지에 대한 운영 기준을 추가했다: close draft, pre-open update, NXT 개장~정규장 전 final adjustment, 정규장 직전 handoff로 나눴다.
- 이로써 prep note를 언제까지 업데이트하고, 언제부터는 intraday/daily/replay 문서로 넘겨야 하는지 경계가 더 명확해졌다.
- writing/verification 규칙에도 update window 개념을 반영해, 장전 준비 문서와 장중 기록 문서가 섞이지 않도록 했다.

## 2026-04-19 20:08:00 KST — next-session prep workflow 범위/판단 팩트 보강

### Updated
- Workflow rule: [[workflows/next-session-prep-workflow|next-session-prep-workflow]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- next-session prep이 금요일/주말 전용 문서가 아니라, 본질적으로 **다음 거래 세션 장전 준비 문서**라는 점을 더 명확히 했다.
- 전략 판단 근거로 들어가야 할 팩트 층을 명시했다: same-day TOP30/recap, 국장 분위기와 breadth, 미장/overnight backdrop, 신고가/high-signal 상태, 그리고 직전 시나리오를 바꾸는 변화 팩트.
- 즉 prep note는 감상문이 아니라 실제 장전 판단에 필요한 fact-backed execution note라는 기준을 강화했다.

## 2026-04-19 20:02:00 KST — next-session prep workflow 추가 + 우선순위 조정 근거 반영

### Added to market-intel
- Workflow rule: [[workflows/next-session-prep-workflow|next-session-prep-workflow]]

### Updated
- Workflow roadmap: [[workflows/lane-definition-roadmap|lane-definition-roadmap]]
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 금일 브리핑 output 다음 단계로, 실제 다음 세션 장초 대응 문서를 어떻게 만들지에 대한 workflow를 고정했다.
- replay/signal 심화보다 `next-session-prep`을 먼저 두는 이유를 문서로 남겼다: 사용자의 실제 실행과 더 가깝고, 금요일/주말/overnight carry 문제를 직접 해결하며, 나중에 replay/signal 결과를 prep 문서로 흡수하기 쉽기 때문이다.
- 이에 맞춰 lane roadmap도 실사용 우선순위 기준으로 조정해, `source -> ingest -> graph -> briefing output -> next-session prep` 순서를 먼저 닫는 방향을 명시했다.

## 2026-04-19 18:49:00 KST — evening briefing output workflow 추가

### Added to market-intel
- Workflow rule: [[workflows/evening-briefing-output-workflow|evening-briefing-output-workflow]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- `evening-briefing-input` 이후 단계로, 실제 사용자용 저녁 브리핑 output note가 어떤 역할과 섹션을 가져야 하는지 고정했다.
- 이제 `source 확보 -> validated ingest -> graph update -> briefing output` 앞단 4개 lane이 이어졌고, input note는 data layer, output note는 decision-oriented narrative layer라는 구분이 명확해졌다.
- partial-input 상태에서도 브리핑을 아예 멈추지 않고 limitation을 드러낸 채 partial briefing을 작성할 수 있는 기준을 추가했다.

## 2026-04-19 18:41:00 KST — validated ingest / graph update lane 문서 추가

### Added to market-intel
- Workflow rule: [[workflows/validated-top30-ingest-workflow|validated-top30-ingest-workflow]]
- Workflow rule: [[workflows/event-entity-daily-update-workflow|event-entity-daily-update-workflow]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- source acquisition 다음 단계로, 어떤 archive를 graph에 반영 가능한지 판단하는 `validated TOP30 ingest` lane을 고정했다.
- 이어서 event / entity / daily 3층의 역할 분리를 문서로 고정해, 상세 해석 / 누적 히스토리 / 날짜별 index가 뒤섞이지 않도록 기준을 만들었다.
- 이제 source -> validated ingest -> event/entity/daily update 까지 앞단 3개 lane이 이어졌고, 다음 작업은 `evening-briefing-output-workflow`를 고정하는 쪽이 자연스럽다.

## 2026-04-19 18:33:00 KST — lane definition roadmap + same-day source acquisition workflow 추가

### Added to market-intel
- Workflow plan: [[workflows/lane-definition-roadmap|lane-definition-roadmap]]
- Workflow rule: [[workflows/same-day-source-acquisition-workflow|same-day-source-acquisition-workflow]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 7개 lane을 한 번에 뭉뚱그리지 않고, 어떤 순서로 문서화할지 roadmap을 먼저 고정했다.
- 첫 번째 우선 lane으로 `same-day source acquisition`을 분리해, parser health와 실제 archive 존재 여부를 구분하는 운영 기준을 명시했다.
- 이제부터는 `source 확보 -> validated ingest -> graph update -> briefing output` 순서가 더 명확해지고, source 확보 실패 시에도 partial-input mode를 선언하는 기준이 생겼다.

## 2026-04-19 18:26:00 KST — 태스크 문서화 vs agent 분리 결정 추가

### Added to market-intel
- Workflow note: [[workflows/task-definition-vs-agent-splitting|task-definition-vs-agent-splitting]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 여러 태스크를 각각 전용 agent로 바로 쪼개고 훈련시키는 것보다, 먼저 lane/입출력/검증 기준을 문서로 고정하는 쪽이 현재 단계에 더 적합하다는 결론을 정리했다.
- 권장 모델을 `문서 우선 -> 역할 기반 agent 분리 -> 충분히 반복된 lane만 반자동화 강화` 순서의 하이브리드 구조로 명시했다.
- 즉 지금 Hermes는 `orchestrator + ingest/replay/briefing 역할 agent` 구조로 가는 것이 적절하고, 완전 독립 봇 훈련은 아직 이르다는 판단을 문서화했다.

## 2026-04-19 18:18:58 KST — 진행상황 큰그림 / SOT live status 업데이트

### Added to market-intel
- Research note: [[market-intel/research/ising-split-question-set-2026-04-19|ising-split-question-set-2026-04-19]]

### Updated
- Index: [[market-intel/index|index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- NVIDIA Ising 케이스에서 통합형 한 질문보다, **미국 반응 / 한국 번역 / 장전 판단**을 분리해서 묻는 3문항 세트를 최종안으로 정리했다.
- 이로써 앞으로는 `질문 1 = 미국 반응`, `질문 2 = 한국 번역`, `질문 3 = 장전/replay`로 역할을 분리해 중복을 줄이고 필요한 축만 보강할 수 있다.
- 비교 실험 문서와 별도로, 실제 재사용 가능한 질문 세트를 바로 복붙해서 쓸 수 있게 만들었다.

## 2026-04-19 18:18:58 KST — 진행상황 큰그림 / SOT live status 업데이트

### Updated
- Workflow status: [[market-intel-progress-big-picture]]
- Architecture SOT: [[architecture/sot-market-intel-full-pipeline|sot-market-intel-full-pipeline]]
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 진행상황 큰그림 문서를 최근 실제 상태에 맞게 다시 정리했다. 이제 same-day TOP30 ingest / evening briefing input / US→KR replay / high-signal / Hermes 코드 트랙을 **한 문서에서 같이 보게** 했다.
- 현재 live 규모(entities 421, daily 29, events 108, research 9, workflows 8)와 Quartz `200 OK` 확인 결과를 반영해, 시스템이 더 이상 샘플 단계가 아니라는 점을 명시했다.
- index의 entity count도 실제 누적 수치에 맞게 `30 -> 421`로 교정했다.
- 다음 핵심 과제를 `same-day source 안정화`, `briefing output 정식화`, `US reaction set 반자동화`, `multi-horizon path dataset 강화`로 다시 고정했다.

## 2026-04-19 16:35:00 KST — Ising 질문 비교 실험 추가

### Added to market-intel
- Research note: [[market-intel/research/ising-question-comparison-2026-04-19|ising-question-comparison-2026-04-19]]

### Updated
- Index: [[market-intel/index|index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- NVIDIA Ising 케이스를 실제로 질문 3종(A/B/C) 관점에서 비교해, **주 질문/부 질문/버릴 질문**을 정하는 첫 실험 결과를 남겼다.
- 결론은 `replay / pre-open reconstruction`형 질문(C)을 주 질문으로 두고, `US reaction set`형(A)과 `KR translation`형(B)을 보조로 붙이는 구조가 가장 목적 적합도가 높다는 것이다.
- 즉 앞으로는 질문 설계도 실제 케이스 기반으로 검증하면서 축적한다.

## 2026-04-19 16:20:00 KST — US event 질문 선택 workflow 추가

### Added to market-intel
- Workflow note: [[market-intel/workflows/us-event-question-selection-workflow|us-event-question-selection-workflow]]

### Updated
- Index: [[market-intel/index|index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 미국 원이벤트에 대해 질문도 바로 하나로 고정하지 않고, **질문 후보를 비교한 뒤 주 질문 / 부 질문 / 버릴 질문을 정하는 rule**을 추가했다.
- 앞으로는 답변 품질을 `US reaction set`, `KR translation`, `replay 적합도`, `잡음 비율` 기준으로 비교해 질문 구조 자체를 개선할 수 있게 했다.
- 즉 데이터뿐 아니라 질문 설계도 반복적으로 최적화하는 workflow를 공식화했다.

## 2026-04-19 14:20:00 KST — US reaction set 반자동 로드맵 + SOT 반영

### Added to market-intel
- Daily note: [[market-intel/daily/2026-03-13_top30_recap|2026-03-13_top30_recap]]

### Updated
- Entity: [[market-intel/entities/stocks/HD현대에너지솔루션|HD현대에너지솔루션]]
- Entity: [[market-intel/entities/stocks/한국첨단소재|한국첨단소재]]
- Entity: [[market-intel/entities/stocks/CS|CS]]
- Entity: [[market-intel/entities/stocks/에스에너지|에스에너지]]
- Entity: [[market-intel/entities/stocks/광전자|광전자]]
- Entity: [[market-intel/entities/stocks/후성|후성]]
- Entity: [[market-intel/entities/stocks/이엠앤아이|이엠앤아이]]
- Entity: [[market-intel/entities/stocks/대한광통신|대한광통신]]
- Entity: [[market-intel/entities/stocks/신성이엔지|신성이엔지]]
- Entity: [[market-intel/entities/stocks/퍼스텍|퍼스텍]]
- Entity: [[market-intel/entities/stocks/SK이터닉스|SK이터닉스]]
- Entity: [[market-intel/entities/stocks/애드바이오텍|애드바이오텍]]
- Entity: [[market-intel/entities/stocks/GS글로벌|GS글로벌]]
- Entity: [[market-intel/entities/stocks/옵티시스|옵티시스]]
- Entity: [[market-intel/entities/stocks/넥스틸|넥스틸]]
- Entity: [[market-intel/entities/stocks/알파칩스|알파칩스]]
- Entity: [[market-intel/entities/stocks/MH에탄올|MH에탄올]]
- Entity: [[market-intel/entities/stocks/씨에스윈드|씨에스윈드]]
- Entity: [[market-intel/entities/stocks/머큐리|머큐리]]
- Entity: [[market-intel/entities/stocks/디에이치엑스컴퍼니|디에이치엑스컴퍼니]]
- Entity: [[market-intel/entities/stocks/에이디테크놀로지|에이디테크놀로지]]
- Entity: [[market-intel/entities/stocks/삼성E&A|삼성E&A]]
- Entity: [[market-intel/entities/stocks/씨에스베어링|씨에스베어링]]
- Entity: [[market-intel/entities/stocks/쏘닉스|쏘닉스]]
- Entity: [[market-intel/entities/stocks/안트로젠|안트로젠]]
- Entity: [[market-intel/entities/stocks/태웅|태웅]]
- Entity: [[market-intel/entities/stocks/RF시스템즈|RF시스템즈]]
- Entity: [[market-intel/entities/stocks/기산텔레콤|기산텔레콤]]
- Entity: [[market-intel/entities/stocks/STX엔진|STX엔진]]
- Entity: [[market-intel/entities/stocks/한국카본|한국카본]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- validated archive (`2026-03-13.json` / `86314e800f133ec53f8e97aa75fbb64b7cb83861e1ab4c38a17f032e0a744c41`)만 ingest 대상으로 통과시켰다.
- stock entity 중심으로 누적 히스토리를 업데이트하고, 상세 해석은 theme/event note 쪽에 배치했다.
- 중복 ingest 방지를 위해 날짜별 hash/state 기록을 남긴다.

## 2026-04-19 14:27:59 KST — JMKR TOP30 archive ingest (2026-03-04)

### Added to market-intel
- Daily note: [[market-intel/daily/2026-03-04_top30_recap|2026-03-04_top30_recap]]

### Updated
- Entity: [[market-intel/entities/stocks/아이톡시|아이톡시]]
- Entity: [[market-intel/entities/stocks/인트론바이오|인트론바이오]]
- Entity: [[market-intel/entities/stocks/한탑|한탑]]
- Entity: [[market-intel/entities/stocks/앤디포스|앤디포스]]
- Entity: [[market-intel/entities/stocks/한일사료|한일사료]]
- Entity: [[market-intel/entities/stocks/이엠앤아이|이엠앤아이]]
- Entity: [[market-intel/entities/stocks/SH에너지화학|SH에너지화학]]
- Entity: [[market-intel/entities/stocks/지에스이|지에스이]]
- Entity: [[market-intel/entities/stocks/흥아해운|흥아해운]]
- Entity: [[market-intel/entities/stocks/코퍼스코리아|코퍼스코리아]]
- Entity: [[market-intel/entities/stocks/극동유화|극동유화]]
- Entity: [[market-intel/entities/stocks/SKAI|SKAI]]
- Entity: [[market-intel/entities/stocks/엔지켐생명과학|엔지켐생명과학]]
- Entity: [[market-intel/entities/stocks/대성에너지|대성에너지]]
- Entity: [[market-intel/entities/stocks/제넥신|제넥신]]
- Entity: [[market-intel/entities/stocks/THE E&M|THE E&M]]
- Entity: [[market-intel/entities/stocks/로스웰|로스웰]]
- Entity: [[market-intel/entities/stocks/고려산업|고려산업]]
- Entity: [[market-intel/entities/stocks/STX그린로지스|STX그린로지스]]
- Entity: [[market-intel/entities/stocks/비엘팜텍|비엘팜텍]]
- Entity: [[market-intel/entities/stocks/오가닉티코스메틱|오가닉티코스메틱]]
- Entity: [[market-intel/entities/stocks/피에스케이홀딩스|피에스케이홀딩스]]
- Entity: [[market-intel/entities/stocks/한세엠케이|한세엠케이]]
- Entity: [[market-intel/entities/stocks/제일연마|제일연마]]
- Entity: [[market-intel/entities/stocks/그린리소스|그린리소스]]
- Entity: [[market-intel/entities/stocks/미래생명자원|미래생명자원]]
- Entity: [[market-intel/entities/stocks/캐리소프트|캐리소프트]]
- Entity: [[market-intel/entities/stocks/웰킵스하이텍|웰킵스하이텍]]
- Entity: [[market-intel/entities/stocks/남선알미늄|남선알미늄]]
- Entity: [[market-intel/entities/stocks/에이치엠넥스|에이치엠넥스]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- validated archive (`2026-03-04.json` / `ef9a24685139d6091709af747757c4d0450010c93cf20674d2797b5b248e0c46`)만 ingest 대상으로 통과시켰다.
- stock entity 중심으로 누적 히스토리를 업데이트하고, 상세 해석은 theme/event note 쪽에 배치했다.
- 중복 ingest 방지를 위해 날짜별 hash/state 기록을 남긴다.

## 2026-04-19 14:27:59 KST — JMKR TOP30 archive ingest (2026-03-03)

### Added to market-intel
- Daily note: [[market-intel/daily/2026-03-03_top30_recap|2026-03-03_top30_recap]]

### Updated
- Entity: [[market-intel/entities/stocks/우정바이오|우정바이오]]
- Entity: [[market-intel/entities/stocks/인트론바이오|인트론바이오]]
- Entity: [[market-intel/entities/stocks/모헨즈|모헨즈]]
- Entity: [[market-intel/entities/stocks/한일사료|한일사료]]
- Entity: [[market-intel/entities/stocks/시지메드텍|시지메드텍]]
- Entity: [[market-intel/entities/stocks/이노룰스|이노룰스]]
- Entity: [[market-intel/entities/stocks/에이치엠넥스|에이치엠넥스]]
- Entity: [[market-intel/entities/stocks/성도이엔지|성도이엔지]]
- Entity: [[market-intel/entities/stocks/대성산업|대성산업]]
- Entity: [[market-intel/entities/stocks/성호전자|성호전자]]
- Entity: [[market-intel/entities/stocks/한화시스템|한화시스템]]
- Entity: [[market-intel/entities/stocks/세기상사|세기상사]]
- Entity: [[market-intel/entities/stocks/앤디포스|앤디포스]]
- Entity: [[market-intel/entities/stocks/테크윙|테크윙]]
- Entity: [[market-intel/entities/stocks/RF머트리얼즈|RF머트리얼즈]]
- Entity: [[market-intel/entities/stocks/미래생명자원|미래생명자원]]
- Entity: [[market-intel/entities/stocks/레몬|레몬]]
- Entity: [[market-intel/entities/stocks/국전약품|국전약품]]
- Entity: [[market-intel/entities/stocks/코셈|코셈]]
- Entity: [[market-intel/entities/stocks/웰크론|웰크론]]
- Entity: [[market-intel/entities/stocks/LIG넥스원|LIG넥스원]]
- Entity: [[market-intel/entities/stocks/파인테크닉스|파인테크닉스]]
- Entity: [[market-intel/entities/stocks/디케이티|디케이티]]
- Entity: [[market-intel/entities/stocks/알에스오토메이션|알에스오토메이션]]
- Entity: [[market-intel/entities/stocks/메카로|메카로]]
- Entity: [[market-intel/entities/stocks/압타머사이언스|압타머사이언스]]
- Entity: [[market-intel/entities/stocks/빅텍|빅텍]]
- Entity: [[market-intel/entities/stocks/HLB이노베이션|HLB이노베이션]]
- Entity: [[market-intel/entities/stocks/주성엔지니어링|주성엔지니어링]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- validated archive (`2026-03-03.json` / `0a3fd6c5b28ea4fdff5e3edbb0d2234ba145459431913ba0b8c8736c6e89032c`)만 ingest 대상으로 통과시켰다.
- stock entity 중심으로 누적 히스토리를 업데이트하고, 상세 해석은 theme/event note 쪽에 배치했다.
- 중복 ingest 방지를 위해 날짜별 hash/state 기록을 남긴다.

## 2026-04-18 20:00:00 KST — Mythos / banks predictive replay case 추가

### Added to market-intel
- Replay note: [[research/replay-2026-04-13-anthropic-mythos-banks|replay-2026-04-13-anthropic-mythos-banks]]
- Daily bridge note: [[daily/2026-04-16_us-to-kr-bridge-mythos-banks|2026-04-16_us-to-kr-bridge-mythos-banks]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- Anthropic Mythos 관련 미국발 은행/보안 리스크 프레임을 두 번째 predictive replay 케이스로 정리했다.
- 이번 복기의 핵심은 미국 은행주 약세를 한국 은행주 direct trade로만 보면 부족하고, 한국장에서는 **보안 테마 강세** 로 더 쉽게 번역될 수 있다는 점이다.
- `2026-04-16_보안_모멘텀`과 연결해, 실제 한국장 결과가 direct bank selloff보다 SW/네트워크 보안 군집으로 나타났다는 점을 replay lesson으로 남겼다.
- 마찬가지로 미국 direct losers/winners reaction set을 숫자로 먼저 붙이지 못한 한계를 명시해, 앞으로 replay checklist에 반영했다.

## 2026-04-18 19:45:00 KST — Ising predictive replay case 추가

### Added to market-intel
- Replay note: [[research/replay-2026-04-14-nvidia-ising|replay-2026-04-14-nvidia-ising]]
- Daily bridge note: [[daily/2026-04-15_us-to-kr-bridge|2026-04-15_us-to-kr-bridge]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- NVIDIA Ising 사건을 첫 predictive replay 케이스로 정리해, 당시 한국장 전에 무엇을 알 수 있었고 어떤 추론을 했어야 했는지를 구조화했다.
- 핵심 교훈은 미국 deep-tech 원이벤트를 한국에서 direct beneficiary보다 **양자암호/PQC/보안 테마 번역** 으로 먼저 봤어야 했다는 점이다.
- 동시에 `2026-04-15_us-to-kr-bridge` note를 추가해, overnight 미국 이벤트를 한국장 pre-open 판단으로 바꾸는 bridge layer를 실제 문서로 시작했다.
- 이번 케이스에서는 미국 개별 종목 reaction set을 정량적으로 붙이지 못한 점도 명시적으로 lesson으로 남겨, 이후 replay 품질 개선 포인트로 반영했다.

## 2026-04-18 19:30:00 KST — predictive replay / 복기 시스템 추가

### Added to market-intel
- Workflow note: [[workflows/predictive-replay-and-review-system|predictive-replay-and-review-system]]
- Template: `market-intel/templates/predictive-replay-template.md`
- Template: `market-intel/templates/us-to-kr-bridge-template.md`

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 복기를 단순 회고가 아니라 **예측 성능 향상 루프**로 명시한 workflow note를 추가했다.
- 앞으로 사용자가 케이스를 꺼내면, 당시 한국장 전에 알 수 있었던 정보셋 / pre-open 추론 / 실제 KR path / replay lesson을 같은 구조로 축적할 수 있게 했다.
- `predictive replay note`와 `US to KR bridge note`를 위한 template를 추가해, 대화형 복기 결과를 재사용 가능한 market-intel 문서로 남길 수 있게 했다.
- template는 Quartz publish 대상이 아니므로 8081에서는 workflow note를 진입점으로 사용하고, 실제 작성은 vault의 `market-intel/templates/`에서 진행한다.

## 2026-04-18 13:02:00 KST — 전체 pipeline SOT 문서 추가

### Added to market-intel
- Architecture SOT: [[architecture/sot-market-intel-full-pipeline|sot-market-intel-full-pipeline]]

### Updated
- Index: [[index]]
- Workflow status: [[market-intel-progress-big-picture]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- `architecture/` 아래에 market-intel 전체 프로세스를 한 문서에서 보는 상위 SOT를 추가했다.
- 이제 daily validated ingest, evening briefing input, next-session prep, high-signal, research 흐름을 분리 문서가 아니라 상위 문서에서 먼저 파악할 수 있다.
- 기존 `pipeline-high-signal-big-picture`는 high-signal 축의 세부 큰그림으로 유지하고, 전체 프로세스는 새 SOT 문서가 맡는다.
- 8081 UX를 위해 architecture 문서에는 category prefix보다 **document-type prefix**를 쓰는 방향으로 잡았고, SOT 문서는 `sot-market-intel-full-pipeline`으로 정리했다.
- architecture 문서명은 최종적으로 `sot-* / pipeline-* / audit-*` 형태로 통일했다.


## 2026-04-18 12:34:00 KST — reorg 1차 실제 적용

### Added to market-intel
- Folder: `market-intel/architecture/`
- Folder: `market-intel/research/`
- Workflow plan: [[workflows/market-intel-reorg-execution-plan|market-intel-reorg-execution-plan]]

### Updated
- Index: [[index]]
- Workflow status: [[market-intel-progress-big-picture]]
- Daily note: [[2026-04-16_evening-briefing-input]]
- Daily note: [[2026-04-17_evening-briefing-input]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 루트에 섞여 있던 workflow / architecture / research 문서를 실제 하위 폴더로 분리했다.
- `index.md`를 단순 파일목록 대신 **Today / Next Session / Research / Workflows** 중심 진입면으로 재배치했다.
- `same-day`, `breadth_pct` 같은 내부 표현을 일부 daily note에서 `오늘자 validated TOP30`, `상승종목 비중(%)`으로 교정했다.
- 이번 1차에서는 `daily/`, `events/`, `entities/`는 그대로 두고 루트 혼잡도만 먼저 낮췄다.

## 2026-04-18 12:18:00 KST — reorg 실행안 추가

### Added to market-intel
- Workflow plan: [[workflows/market-intel-reorg-execution-plan|market-intel-reorg-execution-plan]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- market-intel 루트 난잡함을 실제로 정리하기 위한 **단계별 실행안**을 추가했다.
- 어떤 문서를 `workflows / architecture / research`로 옮길지, 어떤 건 루트에 남길지, 어떤 용어를 바꿀지까지 구체적으로 고정했다.
- 금요일 input note와 월요일 next-session-prep를 분리 유지하는 주말 대응 원칙도 reorg 실행안 안에 포함했다.

## 2026-04-18 12:01:07 KST — IA/UX 정리 로드맵 + Monday prep note 추가

### Added to market-intel
- Workflow note: [[market-intel-information-architecture-roadmap]]
- Next session prep note: [[2026-04-20_next-session-prep]]

### Updated
- Daily note: [[2026-04-17_evening-briefing-input]]
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- market-intel 루트가 문서 종류별로 섞여 보이는 문제를 정리하기 위해 정보구조/UX 리팩터링 로드맵을 추가함.
- `same-day TOP30` 같은 표현은 `오늘자 validated TOP30` 방향으로 바꾸고, `breadth_pct`는 실제 의미가 드러나는 `상승종목 비중(%)`으로 설명을 명확히 함.
- 금요일 마감 문서와 월요일 대응 문서를 분리해야 한다는 원칙에 따라 `[[2026-04-20_next-session-prep]]`를 추가했고, 주말 정보 수집이 끝난 뒤 여기서 4/20 장 대응을 마무리하도록 구조를 잡음.

## 2026-04-17 23:08:03 KST — high-signal 1y backfill + full-range vectorbtpro recheck

### Updated
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### External / generated artifacts
- Snapshot backfill: `/Users/gbserver/Documents/github/jmkr_kj/data/signals/high-signals/2025-04-01.json` ~ `/Users/gbserver/Documents/github/jmkr_kj/data/signals/high-signals/2026-04-16.json` (255 trading-day files)
- Outcome backfill: `/Users/gbserver/Documents/github/jmkr_kj/data/signals/high-signal-entry-outcomes/2025-04-01.json` ~ `/Users/gbserver/Documents/github/jmkr_kj/data/signals/high-signal-entry-outcomes/2026-04-16.json` (255 trading-day files)
- vectorbtpro 2026.4.7 recheck: `/Users/gbserver/Documents/github/jmkr_kj/data/signals/high-signal-entry-outcomes/vbtpro-recheck-2025-04-01-to-2026-04-16.json`

### What changed semantically
- `2025-04-01 ~ 2026-04-16` 전 거래일(255일)에 대해 high-signal snapshot과 entry outcome backfill을 모두 재생성했고 실패는 없었다.
- 결과적으로 state 131,833행 / breakout event 29,260행 / entry outcome 204,820행이 같은 범위에서 다시 계산됐다.
- vectorbtpro 2026.4.7 재검증도 표본 축소 없이 동일 전체 범위에 대해 완료했고, `wait_2d_close`가 20일 Sharpe 3.8271로 가장 높았으며 `same_close`는 20일 평균수익률 4.61%로 가장 높았다.

## 2026-04-17 22:18:22 KST — workflow progress page update

### Added to market-intel
- Workflow status note: [[market-intel-progress-big-picture]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 지금까지의 TOP30 ingest, evening briefing input, high-signal, Quartz 노출 상태를 한 문서에서 볼 수 있도록 큰그림 진행상황 페이지를 만들었다.
- 사용자가 "지금 어디까지 왔는지"를 웹에서 바로 확인할 수 있도록 start page에서 접근 가능한 상태로 연결했다.

## 2026-04-17 22:18:22 KST — JMKR TOP30 archive ingest (2026-04-17)

### Added to market-intel
- Daily note: [[market-intel/daily/2026-04-17_top30_recap|2026-04-17_top30_recap]]
- Event: [[market-intel/events/2026-04-17_코로나_모멘텀|2026-04-17_코로나_모멘텀]]
- Event: [[market-intel/events/2026-04-17_광통신장비_모멘텀|2026-04-17_광통신장비_모멘텀]]
- Event: [[market-intel/events/2026-04-17_데이터센터_모멘텀|2026-04-17_데이터센터_모멘텀]]
- Event: [[market-intel/events/2026-04-17_디지털화폐_모멘텀|2026-04-17_디지털화폐_모멘텀]]
- Event: [[market-intel/events/2026-04-17_반도체소부장_모멘텀|2026-04-17_반도체소부장_모멘텀]]
- Event: [[market-intel/events/2026-04-17_우주항공_모멘텀|2026-04-17_우주항공_모멘텀]]

### Updated
- Entity: [[market-intel/entities/stocks/기가레인|기가레인]]
- Entity: [[market-intel/entities/stocks/수젠텍|수젠텍]]
- Entity: [[market-intel/entities/stocks/STX엔진|STX엔진]]
- Entity: [[market-intel/entities/stocks/조이웍스앤코|조이웍스앤코]]
- Entity: [[market-intel/entities/stocks/셀리드|셀리드]]
- Entity: [[market-intel/entities/stocks/빛과전자|빛과전자]]
- Entity: [[market-intel/entities/stocks/링크드|링크드]]
- Entity: [[market-intel/entities/stocks/와이제이링크|와이제이링크]]
- Entity: [[market-intel/entities/stocks/신풍제약|신풍제약]]
- Entity: [[market-intel/entities/stocks/오상헬스케어|오상헬스케어]]
- Entity: [[market-intel/entities/stocks/아이진|아이진]]
- Entity: [[market-intel/entities/stocks/셀레믹스|셀레믹스]]
- Entity: [[market-intel/entities/stocks/후성|후성]]
- Entity: [[market-intel/entities/stocks/아이씨티케이|아이씨티케이]]
- Entity: [[market-intel/entities/stocks/비투엔|비투엔]]
- Entity: [[market-intel/entities/stocks/에이치엠넥스|에이치엠넥스]]
- Entity: [[market-intel/entities/stocks/나노|나노]]
- Entity: [[market-intel/entities/stocks/미래에셋벤처투자|미래에셋벤처투자]]
- Entity: [[market-intel/entities/stocks/랩지노믹스|랩지노믹스]]
- Entity: [[market-intel/entities/stocks/백금T&A|백금T&A]]
- Entity: [[market-intel/entities/stocks/휴온스글로벌|휴온스글로벌]]
- Entity: [[market-intel/entities/stocks/아이앤씨|아이앤씨]]
- Entity: [[market-intel/entities/stocks/디바이스|디바이스]]
- Entity: [[market-intel/entities/stocks/오텍|오텍]]
- Entity: [[market-intel/entities/stocks/한화엔진|한화엔진]]
- Entity: [[market-intel/entities/stocks/누리플렉스|누리플렉스]]
- Entity: [[market-intel/entities/stocks/큐라티스|큐라티스]]
- Entity: [[market-intel/entities/stocks/와이즈버즈|와이즈버즈]]
- Entity: [[market-intel/entities/stocks/성일하이텍|성일하이텍]]
- Entity: [[market-intel/entities/stocks/퍼스텍|퍼스텍]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- validated archive (`2026-04-17.json` / `562e8b823b3f3f9671111647bb5cc49320d0bbde392aefe68810b82208fc9f79`)만 ingest 대상으로 통과시켰다.
- stock entity 중심으로 누적 히스토리를 업데이트하고, 상세 해석은 theme/event note 쪽에 배치했다.
- 중복 ingest 방지를 위해 날짜별 hash/state 기록을 남긴다.

이 노트는 **이벤트 처리 결과가 실제로 무엇을 추가/수정했는지** 웹(8081)에서 바로 확인하기 위한 변경 로그다.

## 2026-04-17 12:58:10 KST — entry outcome tracker + vectorbtpro recheck 시작

### Added to market-intel
- Workflow note: [[high-signal-entry-backtest-sample]]

### Updated
- Workflow note: [[high-signal-entry-timing-roadmap]]
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### External / generated artifacts
- Deterministic outcome tracker: `/Users/gbserver/Documents/github/jmkr_kj/scripts/export_high_signal_entry_outcomes.py`
- vbtpro recheck script: `/Users/gbserver/Documents/github/jmkr_kj/scripts/vbtpro_recheck_high_signal_entry_rules.py`
- Sample deterministic output: `/Users/gbserver/Documents/github/jmkr_kj/data/signals/high-signal-entry-outcomes/2026-04-16.json`
- Sample vbtpro recheck: `/Users/gbserver/Documents/github/jmkr_kj/data/signals/high-signal-entry-outcomes/vbtpro-recheck-2026-03-03-to-2026-03-16.json`

### What changed semantically
- v1.5 entry rule set(`same_close`, `next_open`, `wait_1d/2d/3d_close`, `pullback_2pct`, `pullback_4pct`) 기준의 deterministic outcome tracker를 실제로 구현함.
- `2026-03-03 ~ 2026-03-16` 표본에 대해 vectorbtpro 2026.4.7로 재검증까지 수행했고, 브라우저에서 볼 수 있는 샘플 요약 노트 `[[high-signal-entry-backtest-sample]]`를 추가함.
- 이제 high-signal 파이프라인은 snapshot만이 아니라, breakout 이후 entry timing 질문에 대한 첫 실측 결과를 내기 시작한 상태다.

## 2026-04-17 12:48:50 KST — vectorbtpro 재검증 방향 문서화

### Updated
- Workflow note: [[high-signal-entry-timing-roadmap]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 이 머신에서 `vectorbtpro 2026.4.7` 환경(`~/.local/vectorbtpro-env/.venv/bin/python`)과 `2026.3.1` 환경(`/Users/gbserver/miniconda3/bin/python`)이 실제로 잡히는지 확인함.
- high-signal entry timing 분석은 deterministic pipeline로 원천 outcome table을 만들고, vectorbtpro로 rule/window sweep을 한 번 더 검증하는 2단 구조가 적절하다는 방향을 문서화함.
- 즉 이제 이 로드맵은 단순 아이디어가 아니라, 실제 local 환경을 활용한 backtest/recheck 경로까지 포함한다.

## 2026-04-17 12:41:20 KST — entry timing / backtest window 문서화

### Added to market-intel
- Workflow note: [[high-signal-entry-timing-roadmap]]

### Updated
- Workflow note: [[pipeline-high-signal-big-picture]]
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- breakout event 이후 "언제 들어가야 하나"라는 질문을 별도 `entry decision layer`로 분리해 문서화함.
- `event/state window`, `entry window`, `outcome window`를 구분해서 백테스트해야 한다는 원칙과, 초기 권장 window (`same_close`, `next_open`, `1d wait`, `pullback 2%/4%`, outcome `5d/10d/20d`)를 정리함.
- 즉 이제 high-signal 문서는 단순 signal 설명을 넘어서, 실제 entry timing backtest 로드맵까지 포함하는 상태가 됨.

## 2026-04-17 12:34:10 KST — high-signal big picture 정리 + 첫 visible snapshot 생성

### Added to market-intel
- Daily input note: [[2026-04-17_evening-briefing-input]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 오늘 `2026-04-17.json` TOP30 archive가 없어 validated ingest는 실행하지 못했지만, local-first 저녁 브리핑 입력 노트는 recovery 상태로 계속 축적되도록 했다.
- same-day KOSPI/KOSDAQ, jmkr breadth, 미국 Nasdaq/SOX, 직전 이틀 continuity를 한 노트로 묶어 내일 장초 판단용 입력은 유지했다.
- 즉 archive 누락일에도 `브리핑 입력 레이어`는 비지 않도록 운영 경로를 확인했다.

## 2026-04-17 13:18:00 KST — 첫 local-only evening briefing input note 생성

### Added to market-intel
- Daily input note: [[2026-04-16_evening-briefing-input]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 외부소스 없이도 저녁 브리핑 입력을 축적할 수 있도록, validated TOP30 / breadth / 미국 지수 최소치 / continuity read를 한 노트에 모으는 첫 일일 입력 노트를 만들었다.
- 이제부터는 `daily/YYYY-MM-DD_evening-briefing-input.md` 형식으로 날짜별 누적이 가능하다.

## 2026-04-17 13:05:00 KST — 저녁 브리핑 local-first ingest workflow 정리

### Added to market-intel
- Workflow note: [[evening-briefing-local-ingest-workflow]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- 매일 저녁 브리핑용 ingest의 기본 동작을 `오늘 archive 1건 확인`으로 명확히 고정했다.
- `최근 5거래일 archive 확인`은 기본 동작이 아니라 `복구 / 백필 / 누락 점검 모드`로 재정의했다.
- 외부소스 없이도 당장 돌릴 수 있는 입력 스택을 정리했다: JMKR archive, market-intel graph, KOSPI/KOSDAQ, Nasdaq/SOX, intraday quality 최소 필드.

## 2026-04-17 12:34:10 KST — high-signal big picture 정리 + 첫 visible snapshot 생성

### Added to market-intel
- Workflow note: [[pipeline-high-signal-big-picture]]
- Daily state/event snapshot: [[2026-04-16_high-signal-watchlist]]

### Updated
- Schema draft: [[scripts/high_signal_shared_schema]]
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### External / generated artifacts
- Script: `/Users/gbserver/Documents/github/jmkr_kj/scripts/export_high_signal_snapshot.py`
- JSON snapshot: `/Users/gbserver/Documents/github/jmkr_kj/data/signals/high-signals/2026-04-16.json`

### What changed semantically
- 큰그림 논의를 `[[pipeline-high-signal-big-picture]]`로 정리하고, 신호 체계의 목표를 `state → event → outcome → conditional probability` 흐름으로 고정함.
- JMKR 전체 정상 가정 없이 `stock_prices.db` 직접 계산 방식의 첫 프로토타입을 실행해 2026-04-16 기준 high-signal snapshot을 실제 생성함.
- 그 결과를 `[[2026-04-16_high-signal-watchlist]]`로 노출해서, 사용자가 이제 Quartz/Obsidian에서 실제 결과를 볼 수 있는 상태로 만듦.

## 2026-04-17 12:29:52 KST — JMKR TOP30 archive ingest (2026-04-16)

### Added to market-intel
- Daily note: [[2026-04-16_top30_recap]]
- Event: [[2026-04-16_보안_모멘텀]]
- Event: [[2026-04-16_양자-양자암호_모멘텀]]
- Event: [[2026-04-16_반도체소부장_모멘텀]]
- Event: [[2026-04-16_유리기판_모멘텀]]
- Event: [[2026-04-16_휴대폰부품_모멘텀]]

### Updated
- Multiple stock entities from the 2026-04-16 archive ingest
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- validated archive (`2026-04-16.json`)만 ingest 대상으로 통과시켰다.
- stock entity 중심으로 누적 히스토리를 업데이트하고, 상세 해석은 theme/event note 쪽에 배치했다.
- 중복 ingest 방지를 위해 날짜별 hash/state 기록을 남긴다.

## 2026-04-17 11:00:58 KST — 신고가 schema에 문맥 필드 / state 활용 규칙 추가

### Updated
- Schema draft: [[scripts/high_signal_shared_schema]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- `52주 신고가` event 자체뿐 아니라, 직전 신고가/직전직전 신고가 시점, 52주 저점 위치, 52주 창 안에서의 상대적 위치를 조건부 확률용 문맥 필드로 추가함.
- 위치 정보는 `0~1 float` 정규화 필드로 저장하고, 분석 단계에서 bucketizing 하도록 방향을 명확히 함.
- `state`는 단순 참고 리스트가 아니라 pre-event watchlist / conditioning variable / event 배경 설명 레이어로 사용해야 한다는 운영 규칙을 문서화함.
- raw date 자체보다 age/distance 필드를 cond prob 계산의 주력 feature로 써야 한다는 원칙을 명시함.

## 2026-04-17 10:12:11 KST — 신고가 schema 초안 + 데이터 intake 원칙 추가

### Added to market-intel
- Schema draft: [[scripts/high_signal_shared_schema]]

### Updated
- Index: [[index]]
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- JMKR에 이미 있는 `52주 신고가 breakout` 로직과 `전고점 90% 근접` 스캐너를 한 공통 schema로 묶기 위한 초안을 추가함.
- high-signal ingest는 `JMKR 전체 파이프라인 정상`을 가정하면 안 되고, 최소한 `stock_prices.db`만 있으면 재생성 가능한 구조로 설계해야 한다는 원칙을 추가함.
- 데이터 intake를 `Layer 0: price DB`, `Layer 1: optional enrichment`, `Layer 2: canonical output`의 3계층으로 분리함.

## 2026-04-16 19:15:00 KST — Quantum success case microstructure backfill

### Added to market-intel
- Success case update: [[success-case-2026-04-15-quantum-cluster-nextday]]

### Updated
- Change log: [[MARKET_INTEL_RECENT_CHANGES]]

### What changed semantically
- jmkr 1분봉 backfill로 2026-04-16 양자 관련 6종목의 최소 상한가 패턴 필드를 실제로 채움.
- 이제 이 성공 사례는 단순 breadth 확인을 넘어서, 종목별 `first_limit_time`, `limit_up_type`, `relock_count`, `close_locked`까지 확인된 사례가 됨.

## 2026-04-16 15:23:49 KST — Naver Securities news ingest linkage

### Ingested
- `ingested-events/2026-04-16/2026-04-16_1230_news_daehan-cable_power-bottleneck.md`
- `ingested-events/2026-04-16/2026-04-16_1236_news_nvidia_openai_ising_quantum.md`

### Added to market-intel
- Event: [[2026-04-16_AI-전력병목_대한전선-수급]]
- Event: [[2026-04-14_엔비디아-아이징_공개]]
- Daily note: [[2026-04-16_news_recap]]
- Workflow rule: [[NEWS_INGEST_LINKING_RULES]]

### Updated
- Entity: [[대한전선]]
- Index: [[index]]

### What changed semantically
- 대한전선 관련 뉴스는 기사 저장이 아니라 해석형 이벤트로 연결함.
- 원문 뉴스는 `ingested-events`에 보관하고, `market-intel`에는 재사용 가능한 event/entity 지식만 남김.

<!-- AUTO_CURRENT_STATUS_START -->
## Auto current ops status
- checked_at: 2026-04-23 KST, 목요일 장중
- readiness: 완료 (3/3)
- recovery_needed: 없음
- board: [[current-readiness-board|current-readiness-board]]
- workflow: [[market-intel/workflows/same-day-source-acquisition-workflow|same-day-source-acquisition-workflow]]
<!-- AUTO_CURRENT_STATUS_END -->
