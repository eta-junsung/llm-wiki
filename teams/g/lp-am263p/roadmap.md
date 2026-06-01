---
tags: [roadmap, lp-am263p, living-doc]
date: 2026-06-01
---

# lp-am263p — 프로젝트 로드맵

> 프로젝트 목표까지의 전체 호. 단계 spine은 작업 로드맵으로 위임하고, 여기는 **목표·작업 호 인덱스·현재 위치**만 둔다.
> 전술(기능별 현황·다음 시작점)은 [[status]]가 단일 소스.

---

## 0. 목표

**BP-CC3351을 LP-AM263P에서 구동** — 비공식 포팅으로 CC33XX SDK 예제 `CC3xx_thick_mac_network_terminal`을 올려, network_terminal CLI로 **WiFi scan/connect + BLE HCI**가 실제 동작하는 것이 종착점.

---

## 1. 작업 호 (tasks)

현재 프로젝트는 단일 작업(`porting`)으로 구성되며, 그 작업 호가 곧 프로젝트 목표까지의 전체 단계(S0~S8)다.

| task | 범위 | 호 | 상태 |
|------|------|----|------|
| **porting** | AM243→AM263P 마이그레이션 + CC33xx bring-up | S0~S8 → [[porting]] | S3 막힘 (R27+) |

단계 spine·완료 기준 표·남은 일정은 작업 로드맵 [[porting]]에 둔다 — 여기서 병렬로 재서술하지 않는다(divergence 방지). 후속 작업(예: 안정화·제품화)이 생기면 `roadmaps/<task>.md`로 추가하고 위 표에 한 행 더한다.

---

## 2. 현재 위치

- **전략 단계**: S3 (부트 플래시 `Flash_open` 통과) 막힘 — 단계 상세는 [[porting]].
- **전술(다음 시작점·기능별 현황)**: [[status]] 단일 소스 (현재 다음 시작점 = R28 jtag_flasher 성공 공식 이식).

---

## 3. 남은 일정 / 환원 후보

→ [[porting]] §남은 일정 (S3 해소가 첫 게이트, S4~S8은 통과 후 재추정) · §환원 후보.
