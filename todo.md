# LLM Wiki 셋업 — 내일 이어서

> 카파시 패턴 ([원본](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), 로컬: `C:\Users\echog\eta\wiki\llm-wiki.md`) 기반으로 개인 업무용 LLM 위키 구축.
> 오늘은 vault 디렉토리(`C:\Users\echog\eta\wiki`)만 생성. 나머지는 내일 결정.

---

## 내일 결정할 것

### 1. 첫 위키 주제 (시드 도메인)
어떤 도메인 하나로 시작할지. 나중에 폴더 추가해서 확장 가능.

- [ ] AM263P 펌웨어 개발 (TI MCU — TRM/UG, 드라이버, 디버그 노트)
- [ ] LLM/AI 업무 활용 (카파시 위키처럼 LLM 자체에 대한 위키)
- [ ] 회사 업무 전반 (회의록, 결정사항, 사내 시스템)
- [ ] 기타: ______

### 2. 옵시디언 설치 여부
지금은 마크다운 파일만 있어도 됨. 옵시디언은 백링크/그래프 뷰를 보기 위한 뷰어.

- [ ] `winget install Obsidian.Obsidian` 으로 설치
- [ ] 일단 VSCode 마크다운 미리보기로 시작, 나중에 설치
- [ ] 다른 마크다운 뷰어 사용

### 3. Git 저장소로 둘지
카파시 권장 — "wiki is just a git repo of markdown files". eta가 이미 git이면 wiki를 별도 repo로 빼거나 sub-tree로.

- [ ] `wiki/` 디렉토리를 독립 git repo로 init
- [ ] eta repo에 포함
- [ ] git 안 씀 (일단)

---

## 결정 후 셋업 순서 (참고)

1. 디렉토리 구조 생성
   ```
   wiki/
   ├── CLAUDE.md       # 스키마 — LLM에게 위키 구조/규칙 전달
   ├── index.md        # 페이지 카탈로그
   ├── log.md          # 시간순 작업 로그
   ├── raw/            # 원본 소스 (불변)
   │   └── assets/     # 다운로드한 이미지
   └── pages/          # LLM이 생성/유지하는 위키 페이지
       ├── entities/   # 인물/제품/조직 등 개체 페이지
       ├── concepts/   # 개념 페이지
       └── sources/    # 소스별 요약 페이지
   ```
2. `CLAUDE.md` 작성 — 도메인 맥락, 페이지 컨벤션, ingest/query/lint 워크플로
3. `index.md`, `log.md` 빈 템플릿 생성
4. 첫 소스 하나 골라서 ingest 테스트 → 워크플로 검증
5. 옵시디언 설치 후 vault로 `wiki/` 열기

---

## 메모

- 옵시디언 백링크 문법: `[[페이지명]]`
- 옵시디언 Web Clipper(브라우저 확장)로 웹 아티클을 raw/에 마크다운으로 저장 가능
- 카파시 팁: log.md는 `## [YYYY-MM-DD] ingest | 제목` 형식으로 prefix 통일 → grep으로 파싱 가능
