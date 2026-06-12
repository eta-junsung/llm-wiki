---
tags: [concept, flash, boot, ospi, am263p, workflow, deadtime, open]
source: 실측 (2026-06-12, 8kw-ev-wpt-tx 실보드 — 굽기 절반 확정 / 부팅 절반 미확정)
date: 2026-06-12
---

# 토글-프리 flash 반복 루프 — 굽기 ✓ / 부팅 OPEN

> **board-common(lp-am263p) 워크플로 페이지.** SW1 부트모드를 매 반복 토글하지 않고 빌드→flash→전원사이클을 도는 루프가 성립하는가에 대한 현재 진실. **굽는 절반은 확정, 부팅하는 절반은 미확정** — 단정 금지.
> 굽기 메커니즘의 정본은 [[jtag_flash_harness]] §7. 이 페이지는 거기에 더해 **부팅 절반의 OPEN 상태**를 구조화해 둔다.

---

## 동기 (왜 이 루프인가)

8kw-ev-wpt-tx(AM263P, R5F nortos) dead-time 테스트 펌웨어를 CCS 없이 GUI/스크립트로 빌드·flash하는 워크플로. HW 엔지니어가 `ETA_DEADTIME_NS`([[pwm_pinmap]]·`eta_tuning.h`)를 바꿔 **재빌드 → 재flash → 재부팅**을 반복(build-per-change)한다. **매 반복마다 SW1 부트모드 토글(DevBoot `0,1,0,0` ↔ OSPI(4S) `1,1,1,1`)을 피하는 것**이 목표 — SW1을 OSPI에 고정해 둔 채 루프를 돌 수 있으면 가장 편하다.

정본 flash 하네스 = `flash_node_8kw.js`(Node.js `runAsynch`, CCS2050 `run.bat`). `flash_8kw.js`(Rhino/`GEL_RunF`)는 deprecated([[jtag_flash_harness]] §1).

---

## 루프의 두 절반 — 현재 상태

| 절반 | 내용 | 상태 | 근거 |
|------|------|------|------|
| **① 굽기** | SW1=OSPI(4S)=`1,1,1,1` 고정(app 부팅돼 돌던 상태)에서 flash | **✓ 확정** | run_flash_node_8kw 3/3 OK·EXIT 0, `loadProgram` soft-reset로 코어 인수 ([[jtag_flash_harness]] §7) |
| **② 부팅** | 같은 SW1=`1,1,1,1`에서 **전원사이클만으로 새 이미지 standalone 부팅·구동** | **? 미확정** | 무토글 PWM 관측 — 부팅 실패 vs 측정환경 분기 미진단 (아래) |

→ **"토글-프리 루프 전체"는 ①만 확인된 상태.** ②가 서야 루프가 닫힌다.

---

## ① 굽기 절반 (✓ 확정) — 요약

[[jtag_flash_harness]] §7 정본. 핵심만:
- SW1=`1,1,1,1`(보드가 OSPI에서 부팅돼 **app 실행 중**) + CCS IDE 완전 종료(클린 호스트, §2)에서 **3/3 OK, EXIT 0**.
- 메커니즘: 하네스가 매 OP `loadProgram` 시 `"CPU reset (soft reset) has been issued through GEL on program load"` — 코어를 soft-reset해 돌던 app으로부터 점유를 깨끗이 인수.
- ⟹ 굽기에 DevBoot는 **필수 아닌 편의**. (DevBoot의 "No SBL"은 안정성/속도 편의일 뿐.)

---

## ② 부팅 절반 (OPEN) — 2026-06-12 무토글 PWM 관측

위 굽기 직후 **SW1=`1,1,1,1` 유지 + 전원사이클** → Logic2(Saleae)로 PWM 4채널(레그1/2 HS/LS, [[pwm_pinmap]]) 측정:

- **관측: 4채널 전부 정적 logic 0 — 토글 없음.** (캡처 길이 아티팩트는 배제됨 — 너무 짧은 윈도우 때문이 아님.)
- **미진단 분기** — 이 무토글이 둘 중 무엇인지 측정만으로 못 가른다:
  - **(A) 부팅/펌웨어 실패** — 새 이미지가 standalone 부팅 안 됐거나, 부팅해도 PWM이 안 나옴.
  - **(B) 측정 배선 문제** — Logic2 공통 GND 미결선·프로브 접촉 불량. (정적 logic 0은 "진짜 신호 0"과 "GND/프로브 미결선" 둘 다로 나타남 — Logic2가 구분 못 함.)
- **다음 세션 가름 방법**: ① **UART 텔레메트리**(18B 패킷 [[uart5_packet_protocol]])로 **독립 부팅 증거** 확보 — 패킷이 흐르면 부팅·런타임 살아있음 → (B)로 좁힘. ② **GND/프로브 결선 재확인** 후 PWM 재측정. 둘로 (A)/(B)를 분리.

> ⚠️ **이 무토글 관측을 PWM PASS 실적과 혼동 금지.** PWM 4채널은 별도 세션에서 **Saleae로 의도된 검증을 통과**했다(commit `4014901`, 4-DT sweep PASS, [[pwm_leg2_isoform_report]]·[[status]]). 이번 무토글은 **토글-프리 루프로 flash한 이미지 + 다른 측정 셋업**에서의 별개 관측이며, 위 PASS를 뒤집는 증거가 아니다 — 부팅/측정 어느 쪽이 원인인지 미진단일 뿐.

---

## 미확정 (정직하게 — 추론 금지)

- **warm reset 후 chip-state**: OSPI 모드 고정 + 전원사이클(또는 flasher soft-reset) 후 OSPI 컨트롤러/chip이 깨끗한 부팅 상태로 돌아오는지 — **wiki에 측정 근거 없음**. ([[flash_open_sequence]] 종료 상태 표는 런타임 `Flash_open` 층위이지 이 warm-reset 층위가 아님.)
- **OSPI 모드 부팅 후 PWM 미관측 근본원인**: 위 (A)/(B) 어느 쪽인지 미진단. 부팅 자체가 됐는지조차 이번 세션 UART로 확인 안 함.
- ※ 2026-06-05 세션에서 standalone 부팅 banner(`eta-tx: 8kw-ev-wpt v1.0e00`)는 떴으나([[jtag_flash_harness]] §4), 그건 **다른(이전) 이미지·세션**의 증거다. 이번 토글-프리 루프 이미지의 부팅 증거로 전용하지 말 것.

---

## 함께 보기

- 굽기 메커니즘 정본(flash-time): [[jtag_flash_harness]] §7 · 클린 호스트 [[jtag_flash_clean_host]]
- SW1 부트모드 표(단일 소스): [[CLAUDE]] "하드웨어 — 부트 모드 / boot flow" 절
- 부팅 증거 채널(UART 텔레메트리): [[uart5_packet_protocol]] · [[pc_monitor_gui]]
- 측정 대상 PWM 핀·실측 PASS: [[pwm_pinmap]] · [[pwm_leg2_isoform_report]] · [[status]]
- 프로브 인벤토리: [[instruments]]
