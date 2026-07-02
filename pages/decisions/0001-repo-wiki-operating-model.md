---
tags: [decision, adr, wiki-ops]
source: 2026-07-02 운영 설계 논의
date: 2026-07-02
status: accepted
---

# ADR-0001: repo↔wiki 운영 모델 — git=코드 진실 / wiki=의도 진실, 한 방향 의존

## 맥락

wiki(지식·계획)와 코드 repo(구현)가 **물리적으로 분리**된 채 운영돼 왔다 (wiki=`~/eta/wiki`, 프로젝트=`~/eta/projects/<팀>/<프로젝트>`). 사이클은: wiki에서 "다음 작업" 인출 → 코드 세션에서 작업 → 세션 끝에 "환원 프롬프트" 받아 wiki에 복붙 → wiki 갱신.

문제: **wiki 정보와 실제 프로젝트 상태가 자주 어긋났다.** wiki가 "다음 작업"이라 한 게 이미 구현돼 있거나, 코드가 딴 걸 하고 있거나. 원인은 wiki 갱신이 **오직 서술(환원 프롬프트)로만** 이뤄져 lossy·누락·시차에 노출된 것.

핵심 관찰: **wiki 세션에서 프로젝트 repo의 git 로그·working tree를 그대로 읽을 수 있다**(같은 파일시스템·같은 유저, 2026-07-02 실측 확인). 즉 wiki가 진실(git)을 못 읽어서가 아니라 **대조를 안 해서** 어긋난 것이다.

## 결정

1. **진실의 소재를 나눈다** — 코드의 진실 = git 히스토리, 의도·지식의 진실 = wiki. wiki는 "뭐가 구현됐나"를 서술로 복제하지 않고 **git에서 대조**한다.
2. **의존은 한 방향** — `repo ⟸ wiki`. wiki가 repo를 읽어 흡수하되, **코드 세션은 wiki의 존재를 모른다.**
3. **앵커 + 델타** — 각 `status.md`에 "흡수 완료 커밋" 앵커를 두고, 동기화는 `git log <앵커>..HEAD`(및 `git diff ... -- docs/`)로 **델타만** 읽는다.
4. **지식 채널은 repo-native** — 지식은 repo `docs/log.md`(+ `docs/<topic>.md`)에 온다(lazy-create). wiki는 이 **채널(경로)만** 계약으로 알고 읽는다. 코드측이 이를 wiki를 언급하지 않는 엔지니어링 위생으로 남기며, **그 지침을 코드측 어디에 설치하는지(하네스/에이전트/CLAUDE.md 등)는 이 ADR 범위 밖**(코드측 설계 결정). wiki가 writer 정체를 알면 결합·drift.
5. **결정(ADR)의 집은 wiki** — 결정은 의도라 wiki에 산다. bottom-up(log→승격)·top-down(직접 작성) 둘 다 `decisions/`로.

절차 상세(how)는 [[wiki_sync_protocol]].

## 대안과 기각 이유

- **git submodule로 프로젝트를 wiki에 물기** — 기각. submodule이 주는 "특정 커밋 읽기"는 이미 공짜(같은 FS 읽기 가능)인데, 비용은 실재: ①핀이 항상 뒤처져 오히려 드리프트 **고착**(원하는 건 live HEAD인데 submodule은 마지막 핀), ②커밋마다 wiki working tree 더러워지는 ceremony, ③detached HEAD 혼란. submodule은 "빌드 재현성 위해 버전 고정"용이지 "live 상태 대조"의 반대 도구.
- **프로젝트를 wiki 안에 중첩(코드를 wiki repo로)** — 기각. wiki repo가 코드·빌드산출물로 비대해지고 git 히스토리가 지식/코드 churn으로 오염. "wiki가 커진다"는 걱정은 **중첩하지 말아야 할 이유**지 submodule을 쓸 이유가 아님.
- **코드 세션을 wiki-aware로** — 기각. repo에 바깥 wiki 때문에만 존재하는 인공물이 껴 의존이 역류(누수). 이식성·독립가치 훼손. 두 세계를 잇는 건 사람(오케스트레이터) 한 명이면 족함.

## 결과 / 감수

- **얻음**: 복붙 소멸, 환원 누락에 강건(경험이 커밋 시점에 repo에 남음), 드리프트가 `git log <앵커>..HEAD`로 **계산 가능**, 토큰 비용이 파일 크기와 무관(델타만 읽음), 프로젝트 N개로 늘어도 wiki 안 비대해짐.
- **감수**: 사람의 트리거 한마디("동기화해줘")는 남는다(내용 복붙은 아님). 코드 세션의 로깅 **규율**에 의존 — 로그도 커밋도 없이 지나간 경험은 wiki도 못 건짐(이를 습관으로 강제하는 **수단·위치는 코드측 소관**, wiki 범위 밖). `docs/` 구조를 표준화(`docs/log.md`)하는 약한 결합을 받아들인다.
- **적용 범위**: 전 프로젝트 공통. 선행 적용 = 8kw([[status]] 앵커 블록, 2026-07-02 드리프트 0 확인).

## 링크

[[wiki_sync_protocol]] (how) · 8kw [[status]] (선례) · [[firmware_git_workflow]] (커밋·태그 표준)
