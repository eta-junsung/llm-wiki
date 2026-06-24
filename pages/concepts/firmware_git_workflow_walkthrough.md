---
tags: [git, workflow, firmware, walkthrough, tutorial, hands-on]
source: g-8kw-ev-wpt-tx 트렁크 기반 워크플로 실습 세션 (2026-06-24) + repo 직접 확인
date: 2026-06-24
---

# 트렁크 기반 Git 워크플로 — 한 사이클 실습 가이드

[[firmware_git_workflow]] 표준을 **처음부터 끝까지 한 바퀴 직접 돌려본 실습 기록**이자, 초심자가 따라 돌릴 수 있는 실전 가이드. 표준(왜·전체 규약)은 [[firmware_git_workflow]], repo 운영 요약은 [[contributing_template]]/repo `CONTRIBUTING.md`, 한 장 요약은 repo `docs/git-workflow-cheatsheet.md`. **이 페이지는 그것들을 "실제로 어떻게 손이 움직이는가"로 잇는다.**

> 실습 대상: `Eta-Electronics/g-8kw-ev-wpt-tx` (AM263P4 R5F nortos, LP-AM263 보드, 8kW EV WPT 송신). 2026-06-24, 사이클 3바퀴(연습 squash / 실전 rebase+태그 / PR 템플릿 squash)를 돌렸다. 마지막 상태: 열린 PR 0, 원격 가지 `main`만, 태그 `v0.1.0`, 작업트리 clean. 명령은 실제로 친 것 위주다.

---

## 0. 한 사이클의 골격 (8단계)

모든 변경은 이 8단계를 거친다. ⑧은 배포(보드에 굽기) 때만.

| # | 단계 | 무엇을 | 왜 | 게이트 |
|---|------|--------|-----|--------|
| ① | 최신 main에서 가지 치기 | `git switch main && git pull --ff-only`<br>`git switch -c feature/<주제>` | 줄기 최신 위에서 시작해야 나중에 충돌이 적다 | base = `main`, 가지는 짧게 산다 |
| ② | 작업 + 커밋 | `git add -p && git commit` | 변경을 의미 단위로 묶는다 | Conventional Commits(§아래), 명령형·50자, 본문에 "왜" |
| ③ | push | `git push -u origin feature/<주제>` | **이때 처음 원격에 닿는다** (그 전까지 전부 로컬) | — |
| ④ | PR 열기 (혼자여도 필수) | `gh pr create --base main` | 변경이 PR 단위로 묶이고 리뷰·CI가 붙는 자리가 생긴다 | self-merge 허용, 그래도 PR은 거친다 |
| ⑤ | CI 빌드 게이트 | self-hosted 러너가 `gmake -C build clean → all → .mcelf` 검증 | "내 PC에서만 빌드됨" 차단 | 빌드 green (현재 informational) |
| ⑥ | merge | `gh pr merge --squash`(기본) 또는 `--rebase` | **트렁크에 들어가는 건 바로 여기** | CI green 선행, 머지 방식은 §아래 |
| ⑦ | 가지 삭제 (로컬+원격) | merge 확인 후 삭제 | 잔재 가지를 쌓지 않는다 | merge 됐는지 확인(§함정 1) |
| ⑧ | (배포 시만) 릴리스 태그 | `git tag -a vX.Y.Z -m "..."`<br>`git push --tags` | 보드에 구운 그 소스를 되짚는 앵커 | 워킹트리 clean + push된 tip, annotated 필수 |

> **흔한 오해 — "로컬/원격 경계가 헷갈린다"**
> ①가지 치기·②작업·②커밋은 **전부 내 PC(로컬)에서만** 일어난다. `main`을 건드리지 않는다 — `feature/...`라는 내 작업 사본일 뿐. 원격(GitHub)에 처음 닿는 건 **③ push**다. 그리고 내 변경이 트렁크(`main`)에 실제로 들어가는 건 **⑥ merge** 한 군데뿐. push ≠ merge다. push는 "내 가지를 서버에 올림", merge는 "그 가지를 줄기에 합침".

---

## 흔한 오해 박스 — "PR"이 대체 뭔가

실습 중 가장 많이 나온 질문 묶음. 초심자가 반드시 걸리는 곳이라 따로 모은다.

> **Q1. 왜 "pull" request인가? 내 가지를 main에 넣는 건 push에 가까운데?**
> 이름은 **받는 쪽(관리자) 관점**이다. 기여자가 가지를 push해 두면, 관리자가 그 가지에서 변경을 **당겨간다(pull)**. 그래서 "내 변경을 pull 해가 달라는 요청" = pull request. 어원은 `git request-pull`(자기 가지를 가져가 달라는 알림을 생성하는 명령). GitLab은 같은 것을 **Merge Request**라 부른다 — 관점이 "합친다"로 바뀐 이름.

> **Q2. "PR을 연다"는 게 커밋 메시지 적는 거랑 같나?**
> 비슷하지만 **다른 계층**이다.
> | | 커밋 메시지 | PR 제목·본문 |
> |---|---|---|
> | 사는 곳 | git 안 (로컬·원격 공통) | GitHub 안 (git 아님) |
> | 단위 | 커밋 하나 | 가지의 변경 묶음 전체 |
> | 역할 | "이 한 덩어리가 뭘 했나" | "이 가지 전체가 왜 들어가야 하나" + 리뷰·CI가 붙는 자리 |
> 커밋 메시지는 `git log`에 영구히 남고, PR 본문은 GitHub 협업 메타데이터다.

> **Q3. PR에도 컨벤션이 있나?**
> [[firmware_git_workflow]] §4의 **Conventional Commits는 "커밋 메시지" 규약**이다. PR 전용 공식 표준은 없다. 관행:
> - **PR 제목** = Conventional Commit 형식으로 쓴다 (`feat(gui): ...`). 특히 **squash 머지면 PR 제목이 그대로 트렁크 커밋 메시지가 되므로** 이 관행이 사실상 강제된다.
> - **PR 본문** = 템플릿을 채운다 (무엇을/왜/영향 타깃/테스트/위험).
> 이 repo엔 PR 규정이 없었어서 → 실습 사이클 C에서 템플릿을 새로 만들었다(§아래).

---

## 1. 사이클 B — 연습용 (squash)

**목적**: 깨끗한 throwaway 변경으로 "처음부터" 한 바퀴. 본 작업과 무관한 문서 추가라 망쳐도 안전.

| 단계 | 한 일 |
|------|-------|
| ①~② | `feature/workflow-cheatsheet` 가지에 `docs/git-workflow-cheatsheet.md`(이 사이클 표를 repo에 박은 치트시트) 추가 → 커밋 `5ea8623` (`docs:` 타입) |
| ③ | push — **이때 self-hosted 러너를 처음 기동**(§러너 기동) |
| ④~⑤ | PR #3 열기 → CI build pass |
| ⑥ | **squash 머지** → `main`에 `e76019b` 한 커밋으로 선형 안착 |
| ⑦ | 가지 로컬+원격 삭제 |

**squash를 쓴 이유**: 연습 가지의 중간 커밋들은 살릴 가치가 없는 잡음 → 트렁크엔 의미 있는 한 줄(`docs: git 워크플로 치트시트 추가 (#3)`)만 남기는 게 깔끔. (머지 방식 선택 기준은 §머지 방식.)

---

## 2. 사이클 A — 실전 (rebase + 태그)

**대상**: 이미 열려 있던 실제 PR #2 `feature/adc-calculations` — ADC raw→물리량 변환, **7개의 의미 있는 Conventional Commit**(I_COIL_SEN·GA_Iin_SEN·GA_Vin·NTC 온도 등 채널별). 이미 ①~⑤(가지·커밋·push·PR·CI)까지 완료된 상태였다.

| 단계 | 한 일 |
|------|-------|
| ⑤ | CI build pass 재확인 |
| ⑥ | **rebase 머지** → 7커밋이 각각 **새 SHA로 `main`에 선형 보존**(`726008a..bec434d`). merge commit 없이 줄기 하나에 7개가 일렬로 붙음 |
| ⑦ | 가지 삭제 |
| ⑧ | **annotated 태그 `v0.1.0`** 박고 push (tip `bec434d`를 가리킴) |

**rebase를 쓴 이유**: 7커밋이 각각 atomic Conventional Commit이라 **커밋 단위로 살릴 가치**가 있었다 — `git bisect`로 회귀를 추적할 때 입자가 커밋 단위로 유지된다. squash로 뭉치면 이 입자가 사라진다.

**태그 실제값** (`git tag -n99 v0.1.0`):
```
v0.1.0 — ADC raw→물리량 변환 (HW 테스트 빌드)

코일 전류·GA 입출력 전압/전류·모듈 NTC 온도 변환을 호스트 GUI에 추가.
LP-AM263 보드 HW 테스트용 첫 릴리스.
```
→ 제목에 "HW 테스트 빌드"를 명시했다. **HW 테스트용도 태그한다**는 결정(§HW 테스트 빌드 태그)의 실물.

---

## 3. 사이클 C — PR 템플릿 (squash)

**목적**: 앞으로 모든 PR이 따를 템플릿을 repo에 박기. 사내 선례가 없어 새로 정한 것.

| 단계 | 한 일 |
|------|-------|
| ①~② | `feature/pr-template` 가지에 `.github/PULL_REQUEST_TEMPLATE.md` 작성 → 커밋 `8158e24` |
| ③~⑤ | push → PR #4 → CI build pass |
| ⑥ | **squash 머지** → `main`에 `6d0556a` |
| ⑦ | 가지 삭제 |

**펌웨어 특유 템플릿 항목** (일반 웹 PR 템플릿과 다른 부분):
- **영향 타깃** — 어느 MCU/보드냐 (예: `AM263P4 R5F / LP-AM263`). 펌웨어는 "어느 칩"이 핵심.
- **실보드 확인 (HW-in-loop)** — 어느 보드에서 무엇을 측정했나. 빌드 green ≠ 보드 동작.
- **위험·회귀·안전** — PWM 타이밍·deadtime·전류·열·폴트 처리에 영향 있나. 전력전자 펌웨어는 버그가 하드웨어를 태운다.

**최종 상태**: 열린 PR 0, 원격 가지 `main`만, 태그 `v0.1.0`, 작업트리 clean.

---

## 진행하며 내린 결정 (표준 미규정 → 합의로 확정)

표준([[firmware_git_workflow]])·CONTRIBUTING에 "명시 없음"이던 항목을 실습 중 합의로 채웠다. 표준 반영 검토 대상이다.

### 머지 방식 — squash 기본 / rebase 예외 / merge commit 금지

세 방식의 차이와 트렁크 기반에 맞는 선택:

| 방식 | 트렁크에 남는 모양 | 언제 쓰나 |
|------|--------------------|-----------|
| **squash** (기본) | PR 1개 = 트렁크 커밋 **1개** | 가지 안 커밋들이 잡음이거나 한 덩어리로 봐도 무방할 때. PR 제목을 Conventional Commits로 → SemVer 도출·changelog·revert가 깔끔 |
| **rebase** (예외) | 가지의 N커밋이 **각각 새 SHA로 선형** 보존 | 커밋들이 각각 살릴 가치가 있는 atomic Conventional Commits일 때(`bisect` 입자 보존). 사이클 A가 이 경우 |
| **merge commit** | **안 씀** | 비선형 거품(머지 커밋)이 트렁크 "줄기 하나" 철학과 안 맞음 |

> 한 줄 규칙: **기본 squash, atomic이면 rebase, merge commit은 쓰지 않는다.**

### HW 테스트 빌드도 태그한다

**"보드에 구우면 무조건 태그."** 이유:
- **추적성** — 이미지에 `git describe` 해시를 임베드(표준 §9, Tier 1). 현장 보드가 자기 버전을 보고할 수 있어야 태그↔펌웨어 매핑이 닫힌다. 태그 없이 구우면 보드 안에 raw 해시만 남아 사람이 못 읽는다.
- **"테스트냐 production이냐"는 태그 유무가 아니라 버전 번호로 구분**한다(아래 SemVer). 테스트라고 태그를 빼면 추적성이 깨진다.

### SemVer 번호 — pre-1.0 = 개발/테스트 grade

- **`v0.x.y` 구간 전체가 "불안정/개발/테스트 grade"를 함의**한다. `v0.1.0`(첫 중간 배포)은 그 자체로 "아직 정식 아님"을 뜻함.
- **`1.0.0` = 첫 production 정식판.**
- 한 버전에서 여러 후보 빌드가 예상되면 `-rc.1` 같은 **pre-release 접미사**를 붙일 수 있다 (예: `v0.2.0-rc.1`).

### 러너 기동 방식

self-hosted 러너 기동은 두 갈래:
- **일회성**: `./run.sh` — 띄워 두는 동안만 잡을 받음. 실습에선 이걸 썼다.
- **상시(게이트 승격 시)**: `sudo ./svc.sh install && sudo ./svc.sh start` — systemd 서비스로 등록해 부팅 시 자동 기동. CI를 merge 필수 게이트로 올릴 때 이쪽으로.

---

## 함정 / 문서 불일치 (주의)

> ⚠️ **함정 1 — squash/rebase 후 `git rev-list --count main..<branch> == 0` 규칙이 깨진다.**
> 표준 §7·CONTRIBUTING은 가지 삭제 전 `git rev-list --count main..<branch>`로 고유 커밋 0을 확인하라고 한다. **이 확인은 로컬 fast-forward merge에서만 깨끗이 통한다.** squash/rebase 머지는 GitHub이 **서버에서 새 SHA로 커밋을 다시 쓰므로**, 로컬 가지의 옛 SHA는 `main`에 그대로는 없다 → count가 0이 아니게 나와 "아직 안 머지됨"으로 오판하게 된다.
> - **대신 확인**: `gh pr view <#> --json state`가 `MERGED`인지, 또는 `git cherry main <branch>`로 동등 변경이 이미 들어갔는지.
> - **삭제도** squash/rebase 후엔 `git branch -d`(소문자)가 "머지 안 됨"이라며 거부 → `git branch -D`(대문자)로 강제 삭제해야 한다.

> ⚠️ **함정 2 — 오래된 가지 작업트리엔 `CONTRIBUTING.md`가 없을 수 있다.**
> 사이클 A의 `adc` 가지는 `CONTRIBUTING.md`가 추가되기 *이전* 커밋에서 분기됐다 → 그 가지 작업트리 기준으로 파일을 Glob하면 `CONTRIBUTING.md`가 안 잡힌다(실제론 `main`에 존재). **탐색은 작업트리가 아니라 base 브랜치(`main`) 기준으로 봐야 한다.**

> ✅ **점검 완료 — ci.yml의 "표준 §8/§8.1" 인용은 현재 wiki와 일치한다.**
> `.github/workflows/ci.yml` 주석이 빌드 게이트를 표준 `§8`, works-on-my-machine 차단을 `§8.1`로 인용한다. 2026-06-24 시점 [[firmware_git_workflow]]는 06-23 갱신에서 번호가 재배열돼(기존 4~9 → 5~11) **§8 = "CI 자동 빌드 게이트", §8.1 = "왜 — 로컬 빌드와 다른 점"** 이므로 **인용은 정확하다.** (06-23 *이전* 번호에선 §8이 "실무 주의"였다 — 그 시절 기억으로 보면 오기로 보이지만, 재배열로 이미 해소됨.)

---

## 한눈에 — 이 사이클을 다시 돌릴 때 (cheat sheet)

```bash
# ① 최신 main에서 가지
git switch main && git pull --ff-only
git switch -c feature/<주제>

# ② 작업 + 커밋 (Conventional Commits)
git add -p && git commit          # feat(scope): 한 줄 요약

# ③ push (여기서 처음 원격에 닿음)
git push -u origin feature/<주제>

# ④ PR (혼자여도 필수)
gh pr create --base main

# ⑤ CI green 확인 (self-hosted 러너: gmake -C build clean→all→.mcelf)
gh pr checks <#>

# ⑥ merge — 기본 squash / atomic이면 rebase
gh pr merge <#> --squash    # 또는 --rebase

# ⑦ 가지 삭제 (squash/rebase 후엔 -D, count 확인 대신 gh pr view 사용)
git switch main && git pull --ff-only
git branch -D feature/<주제>
git push origin --delete feature/<주제>

# ⑧ (배포 시만) annotated 태그 — 워킹트리 clean + push된 tip에서
git tag -a v0.1.0 -m "v0.1.0 — <요약> (HW 테스트 빌드)"
git push --tags
```

---

## 함께 보기

- [[firmware_git_workflow]] — 전사 공통 표준(왜·전체 규약). 이 실습의 근거 문서.
- [[contributing_template]] — repo `CONTRIBUTING.md` 단일 템플릿(운영 요약).
- [[build_methods]] — `gmake -C build all`(CI가 도는 헤드리스 빌드)의 메커니즘.
- [[linux_migration]] — CI self-hosted 러너 = Ubuntu 개발 머신. 전환과 정렬.
</content>
</invoke>
