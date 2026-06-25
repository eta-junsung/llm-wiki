---
tags: [concept, eta-ai-tools, marketplace, tooling, authoring-meta]
source: ~/eta/eta-ai-tools (branch feature/eta-meta-skill-creator) — .claude-plugin/marketplace.json, eta-meta/.claude-plugin/plugin.json
date: 2026-06-25
---

# eta-meta — 마켓플레이스 저작 메타 층

`eta`는 Eta Electronics의 Claude Code 마켓플레이스(`~/eta/eta-ai-tools`, `.claude-plugin/marketplace.json`). plugin 셋을 배포한다:

| plugin | 결 | 자리 |
|--------|----|----|
| **eta-harness** | 펌웨어를 *짠다* | explorer/planner/coder/verifier 4단계 + wiki·layers + commit |
| **eta-md-to-html** | 문서를 *변환한다* | Markdown → eta 하우스 HTML 1파일 |
| **eta-meta** | plugin·스킬을 *짓는다* | 저작 메타 도구 |

## 왜 별도 층인가

eta-meta는 다른 plugin과 스킬을 **짓는** 자리다 — 결이 다르다. eta-harness가 *펌웨어*를 만든다면 eta-meta는 *도구 자체*를 만든다. 메타 작업(스킬을 빚고, 대조하고, 검증)을 펌웨어 harness에 섞으면 두 관심사가 한 plugin 안에서 엉킨다. 그래서 저작 행위를 한 층으로 떼어냈다.

현재 입주: [[skill_creator]](스킬 작법) + [[skill_reviewer_agent]](독립 검토). 앞으로 **command creator·agent creator**도 여기 모은다 — "마켓플레이스 자산을 짓는 모든 도구"가 한 자리에 산다.

설계의 단일 기준은 [[harness_engineering_principles]](책 *하네스 엔지니어링 with 클로드 코드*의 세 원리)다. eta-meta의 모든 도구는 이 세 원리에 비춰 빚어진다 — skill-creator는 그 자체가 세 원리의 도그푸딩 샘플.

스킬을 짓는 전체 흐름은 [[skill_authoring_pipeline]](author→review→verify→deploy)에 있다.

## 발견된 drift (코드 기준 — 2026-06-25)

환원 시점 소스를 직독해 잡은 어긋남. 코드를 믿고 호명한다:

- **README.md가 "플러그인 2개"로 적고 eta-meta를 누락.** `README.md`는 eta-harness·eta-md-to-html만 나열하나, `marketplace.json`은 plugin **3개**(eta-meta 포함)를 등록한다 — README가 뒤처졌다.
- **manifest description이 skill-creator를 "house 골격·Pushy description 공식"으로 적음.** `marketplace.json`·`eta-meta/plugin.json` 두 description 모두 그렇게 쓰지만, 실제 `skill-creator/SKILL.md`는 **house 골격 강제·TEMPLATE.md를 의도적으로 뺐다**([[skill_creator]] 참고) — manifest 문구가 스킬의 실제 범위보다 뒤처졌다. 정본은 SKILL.md.
