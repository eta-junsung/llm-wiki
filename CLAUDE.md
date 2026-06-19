# wiki — 루트 schema

LLM이 읽고 쓰는 지식 저장소. Andrej Karpathy의 "wiki 패턴" 기반 — 소스를 이해한 결과를 페이지로 구조화하고, 페이지 간 백링크로 연결한다. 원본 텍스트가 아닌 이해된 지식이 쌓이는 곳.

---

## 디렉토리 레이아웃

```
wiki/
├── CLAUDE.md             # 이 파일 — 운영 규약
├── index.md              # 전체 페이지 카탈로그
├── log.md                # 시간순 작업 로그
├── llm-wiki.md           # 카파시 패턴 원본 (참고용)
├── pages/                # 루트 공통 지식 (모든 팀·프로젝트에 해당)
│   ├── concepts/         # 운영 전략·방법론 개념 페이지
│   └── reference/        # 회사 공통 참조 자산 (계측 장비 인벤토리 등)
└── teams/
    └── <팀>/
        └── <프로젝트>/   # 프로젝트 self-contained
            ├── CLAUDE.md  # 도메인 schema
            ├── roadmap.md # 전략 — 목표까지 마일스톤 호 (living-doc)
            ├── status.md  # 전술 — 호 위 현재 위치 (파이프라인 갱신)
            ├── roadmaps/  # 작업별(task) 로드맵
            ├── raw/       # 원본 소스 복사본 (immutable)
            └── pages/
                ├── entities/
                ├── concepts/
                └── sources/
```

두 번째 프로젝트는 `teams/<팀>/<프로젝트>/` 동일 패턴으로 추가한다.  
특정 프로젝트에 종속되지 않는 공통 지식은 루트 `pages/`에 작성한다 — 운영 전략·방법론은 `pages/concepts/`, 여러 프로젝트가 참조하는 참조 자산(계측 장비 등)은 `pages/reference/`.

---

## 페이지 컨벤션

- 포맷: 마크다운
- 백링크: Obsidian 스타일 `[[페이지명]]`
- YAML frontmatter 필수 필드: `tags`, `source`, `date`
- 파일명: 소문자 + 언더스코어 권장. 한국어 허용 (e.g. `rx_control_pwm_가이드.md`)

---

## 로드맵 컨벤션

**로드맵 = "목표까지 가는 길 전체"(마일스톤 호), status = "그 호 위 지금 어디".** 둘은 짝이다 — 로드맵은 단계 spine을 그리고, 현재 위치는 `[[status]]`로 위임한다. 로드맵은 living-doc이며 게이트(마일스톤) 통과 시 갱신한다.

두 단위:

| 단위 | 위치 | 성격 |
|------|------|------|
| 프로젝트 로드맵 | `teams/<팀>/<프로젝트>/roadmap.md` | 프로젝트 목표까지의 전체 마일스톤 호 |
| 작업 로드맵 | `teams/<팀>/<프로젝트>/roadmaps/<task>.md` | 한 작업(task) 단위 호. `status.md` "다음 시작점"이 가리키는 task 브랜치와 1:1 |

규약:

- frontmatter: `tags: [roadmap, <프로젝트 또는 task>, living-doc]`, `date`.
- 권장 섹션: **한 줄 요약 / 마일스톤 호(단계 spine + 완료 기준 표) / 현재 위치(→ `[[status]]` 위임) / 남은 일정([추정]) / 환원 후보**.
- 디테일은 concept 백링크로 위임 — 로드맵은 spine만. 기능별 현황·다음 시작점은 status가 단일 소스.
- **사실 / 가설 / 모름을 구분**하고 추정은 `[추정]` 표기.
- 상태 기호는 status와 동일: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현.

선례: `teams/g/lp-am263p/roadmap.md` (S0~S8), `teams/c/oled_tv_software/roadmap.md` (M0~M6).

---

## 워크플로

### Ingest

소스 → 지식. 순서:

1. 소스 읽기
2. 사용자와 핵심 합의 (인식 정렬)
3. `sources/<소스명>.md` 생성 — 요약 + 파생 페이지로의 백링크
4. 파생 `entities/`, `concepts/` 페이지 생성·갱신
5. `index.md` 갱신
6. `log.md`에 entry 추가: `## [YYYY-MM-DD] ingest | <제목>`

### Query

`index.md` 진입 → 관련 페이지 정독 → 답변. 가치 있는 답은 페이지로 환원.

### Lint

모순·오래된 진술·orphan 페이지·cross-ref 누락 점검.

---

## 크로스 프로젝트 참조 규칙 — first-ingest-wins

여러 프로젝트가 참조할 수 있는 자료(datasheet, user guide 등)는 **먼저 ingest한 프로젝트에 raw와 sources 페이지를 둔다**. 나중에 같은 자료가 필요한 프로젝트는 raw를 복제하지 않고 Obsidian 백링크(`[[페이지명]]`)로 cross-project 참조한다. 셋 이상의 프로젝트가 명확히 공유하는 자료만 루트 `wiki/pages/`로 승격을 검토한다.

---

## 파이프라인 — roadmap 읽기/갱신 절차

파이프라인 두 단계가 wiki를 읽어 쓴다. **읽기는 파이프라인, 작성·갱신은 wiki 몫**이다.

**eta-explorer (탐색 단계) — 읽기 전용**:
- 작업 진입 시 해당 프로젝트의 `roadmap.md`(작업 단위면 `roadmaps/<task>.md`)를 읽어, **이 task가 전체 호의 어디에 앉는지**로 탐색을 정향한다.
- roadmap을 **수정하지 않는다** — 정향용으로만 읽는다.

**eta-planner (계획 단계) — 읽기 전용**:
- 검증 경로를 제안할 때 [[instruments]](계측 장비)와 프로젝트 검증 핀맵(예: [[gpio_verification_pinmap]])에서 **구체 사실**(핀 번호·신호·기대값·장비)을 인출해, "N번 핀에 스코프, 1kHz 구형파 기대" 식의 **측정 가능한** 검증 문장을 만든다.
- 핀 번호가 wiki에 없으면 **추론으로 채우지 않는다** — 검증 핀맵의 "확인 필요"로 남기고 사용자에게 호명.

**wiki (작성·갱신)**:
- 마일스톤(게이트) 통과 시 `roadmap.md` 상태표·현재 위치를 갱신하고 커밋한다 (`wiki: <프로젝트> roadmap 갱신 YYYY-MM-DD`).
- 사실 갱신의 단일 소스는 status/facts — roadmap은 그곳으로 위임만 한다.

---

## 파이프라인 — status 갱신 절차

코드 repo 작업을 마친 파이프라인 Claude가 "프로젝트 status 갱신" 요청을 받으면:

1. 현재 작업 중인 프로젝트를 확인한다 (코드 repo 디렉토리·커밋 컨텍스트 기준).
2. 오늘 커밋을 분석한다 — 기능별로 **구현됨/미검증/미구현** 여부를 판단한다. "커밋됨 ≠ 실보드 검증됨"에 주의.
3. `teams/<팀>/<프로젝트>/status.md`를 읽는다.
4. 아래 규칙으로 갱신 후 덮어쓴다:
   - `다음 시작점`: 다음 작업 세션의 첫 번째 행동 한 줄. 구체적으로 (파일명·함수명·측정 방법 포함).
   - `구현 현황` 표: 상태 기호 `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현.
   - `미결 사항`: 새로 생긴 미결 항목 추가. 해소된 항목 제거.
   - frontmatter `date`를 오늘 날짜로 갱신.
5. 커밋한다 (`wiki: <프로젝트> status 갱신 YYYY-MM-DD`).

status.md 위치: `teams/c/oled_tv_software/status.md`, `teams/g/lp-am263p/status.md`

---

## 주의

페이지를 만들거나 갱신할 때 항상 해당 도메인의 `CLAUDE.md`(`teams/<팀>/<프로젝트>/CLAUDE.md`)를 먼저 읽는다.
