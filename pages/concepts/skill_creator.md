---
tags: [concept, eta-ai-tools, eta-meta, skill, authoring-meta]
source: ~/eta/eta-ai-tools/eta-meta/skills/skill-creator/SKILL.md
date: 2026-06-25
status: 완성·커밋됨
---

# skill-creator

SKILL.md를 빚거나 본격 손볼 때 description과 본문을 [[harness_engineering_principles]](세 원리)에 비춰 짓고 대조하는 스킬. [[eta_meta_authoring_layer]]의 첫 입주 도구.

## 무엇이고 왜 이렇게 빚었나

[[harness_engineering_principles|세 원리]]만으로 빚었다. 그리고 **자기 자신이 세 원리의 도그푸딩 샘플**이다 — description은 3단계로, 본문은 층으로, 규칙엔 이유로. SKILL.md 본문이 명시한다: *"막히면 이 파일이 어떻게 쓰였는지를 본다."* 새 스킬을 만들 때 보고 베낄 본보기를 코드 자체로 둔 것.

스킬 검토의 **런타임 루브릭**도 이 파일이다 — [[skill_reviewer_agent]]가 이 SKILL.md를 런타임에 읽어 잣대로 삼는다. "좋은 스킬이란 무엇인가"의 단일 소스를 한 자리(이 파일)에 두어 drift를 막는다.

## 의도적으로 뺀 것 (왜 뺐나)

초안에서 **불필요로 판정해 삭제**한 것들. 환원의 값이 여기 있다 — *무엇을 안 했나*와 *왜*:

- **ETA house 골격 강제** — 본문 골격을 강제하지 않는다. 골격을 박으면 원리 2(필요한 것만 올리기)와 충돌하고, 스킬마다 다른 결을 한 틀에 욱여넣게 된다.
- **그릇 판별 게이트** — skill/subagent/command 중 무엇으로 빚을지 가르는 게이트를 SKILL.md에 두지 않았다.
- **TEMPLATE.md** — 채워 넣는 템플릿 파일을 두지 않았다. 본보기는 SKILL.md 자신이 한다(템플릿보다 도그푸드).

⚠️ 마켓플레이스/plugin manifest description은 아직 skill-creator를 "house 골격·Pushy description 공식"으로 적는다 — **실제 SKILL.md엔 house 골격이 없다.** 정본은 SKILL.md. drift 호명은 [[eta_meta_authoring_layer]].

## frontmatter 결정

- `description`은 세 토막(동사·트리거·경계)을 다 박았다 — 원리 1의 도그푸드. "한 줄 오타나 사소한 문구 수정엔 쓰지 않는다"는 경계 조건까지 포함.
- 본문은 세 원리를 각각 한 섹션으로 + **절차**(새 스킬 / 손질 / 안 쓰는 경우)로 닫는다.

세 원리의 정의·이유는 [[harness_engineering_principles]]에 위임 — 이 페이지는 *skill-creator라는 스킬*에 대한 결정(도그푸드·런타임 루브릭·의도적 삭제)만 담는다.
