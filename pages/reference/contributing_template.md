---
tags: [reference, git, workflow, template, contributing, company-common]
source: conversation-2026-06-23 (firmware_git_workflow 표준의 repo-side 산출물)
date: 2026-06-23
---

# CONTRIBUTING.md 템플릿 (회사 공통)

[[firmware_git_workflow]] 표준을 **각 펌웨어 repo 루트에 박는** repo-side 산출물. wiki는 진실의 단일 소스지만, 새로 합류한 사람은 repo부터 본다 — 그래서 규칙 요약을 코드 옆(`CONTRIBUTING.md`)에도 둔다.

**단일 템플릿이 가능한 이유**: git 규칙(PR·Conventional Commits·SemVer·태그·브랜치 위생)은 전사 공통이라 본문이 100% 동일하다. 프로젝트마다 다른 건 상단 **`프로젝트별` 블록 한 덩어리**(프로젝트명·MCU·툴체인·빌드 명령·CI 적용 여부)뿐.

## 사용법

1. 아래 코드블록을 새 repo 루트 `CONTRIBUTING.md`로 복사.
2. 맨 위 `<!-- 프로젝트별 -->` 블록만 그 repo에 맞게 수정 (본문은 손대지 않는다).
3. 표준이 갱신되면 → 이 페이지 + [[firmware_git_workflow]]만 고치고, 각 repo는 본문을 다시 복사. (정본은 wiki, repo는 사본.)

> 정본 승격 경로: GitHub org `.github` repo가 마련되면 이 템플릿을 그곳 `CONTRIBUTING.md`(org 전체 기본값) 또는 `firmware-ci` repo로 올려 복사-붙여넣기를 줄인다. 그 전까지는 wiki가 정본.

## 채워 넣는 예시 (8kw-ev-wpt-tx)

```
- 프로젝트: 8kw-ev-wpt-tx (8kW EV WPT 송신 보드)
- MCU / 툴체인: AM263P4 (LP-AM263P) / TI Clang 5.1.1 + MCU+ SDK 26.00 + SysConfig
- 빌드 명령(헤드리스): gmake -C build all
- CI: ✓ 적용 (헤드리스 빌드 가능)
```

STM32CubeIDE 프로젝트(예 01_RX_control)는 `CI: ✗ 예외 — CLI 헤드리스 빌드 불가, IDE Ctrl+B만`으로 적는다 ([[cubeide_cli_build_trap]]).

---

## 템플릿 (이 코드블록을 복사)

```markdown
# Contributing — <프로젝트명>

이 repo는 **eta 펌웨어 Git 워크플로 표준**을 따릅니다.
전문(왜·전체 규약): 회사 wiki `pages/concepts/firmware_git_workflow.md`.
아래는 일상 운영 요약 — 충돌 시 표준 문서가 우선합니다.

<!-- ── 프로젝트별 (이 블록만 수정) ───────────────────────── -->
- 프로젝트: <이름>
- MCU / 툴체인: <예: AM263P4 / TI Clang 5.1.1 + MCU+ SDK>
- 빌드 명령(헤드리스): `<예: gmake -C build all>`
- CI: <✓ 적용 / ✗ 예외 — 이유>
<!-- ──────────────────────────────────────────────────────── -->

## 브랜치 & PR — 필수
- 줄기는 `main` 하나. `main`은 **항상 빌드 가능** 상태를 유지합니다.
- 모든 변경: `feature/<주제>` 짧은 가지 → push → **PR** → CI green 확인 → `main`에 merge → 가지 삭제.
- **혼자여도 PR을 거칩니다**(self-merge). 정말 사소한 수정(오타 등)만 `main` 직접 push 허용 — 단 빌드는 통과해야 합니다.
- merge 끝난 가지는 로컬·원격 모두 삭제. 삭제 전 `git rev-list --count main..<branch>`로 고유 커밋 0 확인.

## 커밋 메시지 — Conventional Commits
형식: `<type>(<scope>): <한 줄 요약>` + (필요시 본문 + 푸터)

| type | 언제 | 버전 영향 |
|------|------|-----------|
| `feat` | 기능 추가 | MINOR |
| `fix` | 버그 핫픽스 | PATCH |
| `build` | 빌드 시스템·툴체인·makefile | — |
| `refactor` | 동작 불변 구조 개선 | — |
| `docs` / `test` / `chore` | 문서 / 테스트 / 잡일 | — |

- `scope`: 영역명(`pwm`, `flash`, `ble`, MCU면 `01`/`02`/`03`). 생략 가능.
- 호환 깨짐: `feat!:` 또는 본문 `BREAKING CHANGE:` → MAJOR.
- 요약은 명령형·현재형, 50자 내 권장. 본문엔 "왜"를 적습니다.

예시:
```
feat(pwm): dead-time knob 상한 500ns로 확장

기존 400ns로는 leg2 isoform 케이스를 못 덮음.
```

## 버전 & 릴리스 태그
- **SemVer** `vMAJOR.MINOR.PATCH`. 정식 출시 전은 `v0.x.y`로 시작.
- 보드에 굽는 배포는 **annotated 태그**로 박습니다: `git tag -a vX.Y.Z -m "..."` → `git push --tags`. (lightweight 태그 금지.)
- 태그는 **워킹트리가 깨끗하고 push된 tip**에서만.
- 이미지에 **git hash 임베드**(`git describe`) — 현장 보드가 자기 버전을 보고할 수 있어야 합니다.
- 옛 배포본 복원: `git checkout vX.Y.Z`. (동일 *바이너리*는 툴체인+의존성이 같이 고정될 때만 — 표준 §2.1.)

## 현재 적용 범위 (Tier)
이 repo의 현재 단계는 **Tier 1**(혼자/초기): PR 필수 · Conventional Commits · annotated 태그 + git hash 임베드 · 최소 CI 빌드 게이트.
- 두 번째 사람 합류 / `v1.0.0` → Tier 2(main 보호 + 리뷰 require, 코드 서명).
- 필드에 여러 버전 동시 생존 → Tier 3(`release/x.y` 유지 브랜치, 툴체인 핀).
```
