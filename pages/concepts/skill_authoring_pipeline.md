---
tags: [concept, eta-ai-tools, eta-meta, pipeline, authoring-meta]
source: ~/eta/eta-ai-tools/eta-meta/ (skill-creator, reviewer) + 선례 eta-harness/skills/planner, eta-harness/agents/verifier
date: 2026-06-25
status: 설계 합의됨 (verify 단계 미구현)
---

# 스킬 저작 파이프라인

모든 스킬이 거치는 흐름: **author → review → verify → deploy(git)**. [[eta_meta_authoring_layer]]가 이 파이프라인을 위해 존재한다.

## 단계 성격이 그릇을 가른다

eta-harness가 planner=skill·verifier=subagent로 그릇을 가른 *논리 그대로* 저작에 적용했다. 단계의 *성격*이 stance(메인 세션)냐 격리 서브에이전트냐 워크플로냐를 정한다 — 도구가 아니라 결이 그릇을 정한다.

| 단계 | 성격 | 그릇 | 왜 |
|------|------|------|----|
| **author** | 사용자와 라이브 협업·반복 | **stance** ([[skill_creator]]를 메인 세션이 입음) | 격리하면 라이브 협의를 잃는다 |
| **review** | 독립된 눈 + 격리 | **서브에이전트** ([[skill_reviewer_agent]]) | 자기 초안은 자기가 못 본다 |
| **verify** | 여러 실행을 띄워 비교 | **워크플로** | 아직 안 만듦 |
| **deploy** | git | — | push 후 `/plugin marketplace update` |

### author = stance인 이유

skill-creator를 격리 작성 에이전트로 두지 않았다. 스킬 저작은 사용자와 라이브로 협의·반복하는 일인데, 격리하면 그 협의를 잃는다 — **planner가 skill인 이유와 동일**(`eta-harness/skills/planner/SKILL.md`: "협의는 격리된 단발로 안 빚어진다"). 그래서 메인 세션이 skill-creator stance를 *입는다*.

### review = 서브에이전트인 이유

review는 독립된 눈 + 격리가 본질. **verifier가 "쓴 손(coder)에서 판정을 떼어내야 정직하다"는 논리를 *저작*에 적용한 자리**(`eta-harness/agents/verifier.md`: "자기검증은 판단을 흐린다"). 방금 초안을 쓴 컨텍스트가 자기 초안을 판정하면 "맞다"는 쪽으로 기운다 → 격리된 서브에이전트가 산출물만 받아 판정한다.

## review와 verify는 축이 다르다

둘 다 필요한 이유 — 같은 것을 두 번 보는 게 아니라 **다른 축**을 본다:

- **review = 원리를 지켰나** (준수). [[harness_engineering_principles|세 원리]] 루브릭에 댄다. → [[skill_reviewer_agent]].
- **verify = 실제로 도움이 되나** (효능). 현실에 댄다 — description이 *실제로* 불리나, 본문이 default 대비 행동을 *실제로* 바꾸나.

review가 통과여도 verify가 실패할 수 있다(원리를 지켰지만 안 도움). 그 역도 가능. 그래서 둘은 합쳐지지 않는다.

## verify 워크플로 — 미정 (2026-06-26 이어서 설계)

아직 안 만듦. **두 갈래로 합의됨**:

1. **호출 테스트** (원리 1 효능) — description이 불려야 할 때 불리고, 아닐 때 안 불리나.
2. **본문 with/without 테스트** (원리 2·3 효능) — 불린 뒤 본문이 default 대비 행동을 바꾸나.

**충실도 한계 (봉합 금지):** 진짜 로드/언로드 토글이 어려워 "본문 주입 vs 안 함" 근사가 된다. **호출 테스트는 그 근사로 안 잡힌다** — 호출 판단 자체를 토글하는 게 아니라 본문 주입 여부만 토글하기 때문. 이 한계를 어떻게 넘을지가 다음 설계의 핵심.
