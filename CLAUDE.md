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
│   └── concepts/         # 운영 전략·방법론 개념 페이지
└── teams/
    └── <팀>/
        └── <프로젝트>/   # 프로젝트 self-contained
            ├── CLAUDE.md # 도메인 schema
            ├── raw/      # 원본 소스 복사본 (immutable)
            └── pages/
                ├── entities/
                ├── concepts/
                └── sources/
```

두 번째 프로젝트는 `teams/<팀>/<프로젝트>/` 동일 패턴으로 추가한다.  
특정 프로젝트에 종속되지 않는 공통 지식은 루트 `pages/`에 작성한다.

---

## 페이지 컨벤션

- 포맷: 마크다운
- 백링크: Obsidian 스타일 `[[페이지명]]`
- YAML frontmatter 필수 필드: `tags`, `source`, `date`
- 파일명: 소문자 + 언더스코어 권장. 한국어 허용 (e.g. `rx_control_pwm_가이드.md`)

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

## 주의

페이지를 만들거나 갱신할 때 항상 해당 도메인의 `CLAUDE.md`(`teams/<팀>/<프로젝트>/CLAUDE.md`)를 먼저 읽는다.
