---
tags: [concept, flash, boot, ospi, am263p, workflow, deadtime, open]
source: 실측 (2026-06-12, 8kw-ev-wpt-tx 실보드 — 굽기 절반 확정 / 부팅 절반 미확정) + 문서조사 (2026-06-12, AM263P TRM §5.4.1·UG·IS25LX256 데이터시트·회로도 — §③)
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
- **다음 세션 가름 방법**: ⓪ **이번 "전원사이클"이 (a)진짜 VCC 완전 제거 / (b)SW2 `PORz` 버튼 / (c)SW3 `RESETz` 버튼 중 무엇이었는지부터 확정** — §③ TRM Note 때문에 갈린다. (b)·(c)는 flash를 POR 못 하므로 flash가 4-byte로 stuck이면 boot 실패=A 확정, (a)만 flash 3-byte 복귀를 보장. ① **UART 텔레메트리**(18B 패킷 [[uart5_packet_protocol]])로 **독립 부팅 증거** 확보 — 패킷이 흐르면 부팅·런타임 살아있음 → (B)로 좁힘. ② **GND/프로브 결선 재확인** 후 PWM 재측정. 셋으로 (A)/(B)를 분리.

> ⚠️ **이 무토글 관측을 PWM PASS 실적과 혼동 금지.** PWM 4채널은 별도 세션에서 **Saleae로 의도된 검증을 통과**했다(commit `4014901`, 4-DT sweep PASS, [[pwm_leg2_isoform_report]]·[[status]]). 이번 무토글은 **토글-프리 루프로 flash한 이미지 + 다른 측정 셋업**에서의 별개 관측이며, 위 PASS를 뒤집는 증거가 아니다 — 부팅/측정 어느 쪽이 원인인지 미진단일 뿐.

---

## ③ TRM/UG 근거 — boot 경로는 정당, 단 reset 방법이 결정적 (2026-06-12 문서조사)

TRM(`raw/am263p_trm/ch05_initialization.md`)·UG·IS25LX256 데이터시트·보드 회로도로 OPEN을 조사한 결과. **문서는 ②의 무토글 관측을 직접 닫지는 못하지만**, ① 토글-프리 *boot* 경로가 아키텍처적으로 정당함을 확정하고 ② "warm reset 후 chip-state" 미확정의 **근본 메커니즘을 닫는다**.

### 토글-프리 boot 경로는 silicon상 정당 (FACT)

- **BOOTMODE 핀은 매 POR/reset release마다 재샘플링** — TRM §5.1.1(:111)·§5.3(:480 "After every POR, they are the main source"). ⟹ SW1=`1,1,1,1` 고정이면 **매 전원사이클이 결정적으로 OSPI(4S) 부팅 재진입**. DevBoot 토글이 boot에 필요한 게 아님.
- **OSPI(4S) boot은 non-XIP** — TRM §5.4.1.3.1.1(:761): ROM이 매 부팅 시 flash→on-chip RAM으로 이미지를 **새로 복사** 후 실행. ⟹ 재flash 이미지는 **다음 전원사이클에 그대로 반영**. (굽기 ✓ + 전원사이클 = 새 이미지 적재.)
- 2026-06-05 banner 부팅도 **SW1=`1,1,1,1`(OSPI 4S)** 에서 났다 → 이 경로는 이 보드에서 동작 실증됨(단 §미확정대로 다른 이미지·세션).

### reset 방법이 결정적 — >128Mb flash 3-byte/4-byte 위험 (FACT, "warm-reset chip-state"의 근본원인)

TRM §5.4.1 Note(`ch05_initialization.md`:530):
> ">128 Mb flash는 RESET 신호 패키지 필수. ROM은 3-byte(24-bit) 주소만 쓰는데 SW는 보통 4-byte로 전환한다. **warm reset 시 ROM은 3-byte 기대 / flash는 4-byte로 남음** → flash를 RESET 신호로 리셋해야 3-byte 복귀. **ROM은 software reset 명령을 내지 않는다.**"

우리 케이스에 정확히 적용:
- IS25LX256 = **256 Mb(>128Mb)**, Octal DDR에서 **주소 4-byte 고정**(`raw/IS25LX256/ch00_frontmatter.md`:161). ROM은 4S/8S에서 3-byte(:735).
- ⟹ app이 flash를 Octal DDR(4-byte)로 둔 상태에서 **flash를 POR하지 못하는 리셋**(아래 버튼 둘 / WDT 180s warm reset — TRM:2098 / flasher `loadProgram` soft-reset)이 나면 **ROM이 SBL을 못 읽어 boot 실패**. flash RESET# 어서트 또는 **full POR만 해소**.
- **보드 버튼 둘 다 flash를 POR하지 못한다**(회로도 sheet 6 + UG Fig 2-10/2-11 — 단일 소스 [[CLAUDE]] "리셋/푸시버튼"): **SW2 `PORz`**(콜드급 PORz — UG:431)도 **SW3 `RESETz`**(warm reset — UG:432)도, 그 리셋 트리에 flash 3.3V 전원도 flash RESET#도 묶여 있지 않음. 둘 다 SoC만 리셋·SOP(부트모드) 재래치할 뿐 flash 상태는 그대로 둔다.
- 보드는 flash RESET#을 **실제 배선**: `AM263P_OSPI0_RST`(직렬 R99 22Ω) → SoC OSPI_RESET_OUT 핀(UG GPIO19/20 = OSPI_RESET_OUT0/1). flasher의 `flashFixUpOspiBoot()`가 이 핀을 토글해 1S 복귀([[sbl_app_flash_handoff]]:86). **그러나 ROM은 bare reset에선 이 핀을 안 건드린다**(:530 "ROM does not issue a software reset").
- 부수 전제: 4S boot은 flash **QE bit가 NV config에 SET** 필요(TRM:757) — 06-05에 4S로 부팅됐으니 충족된 것으로 보임.

> **루프 운영 규칙(문서 도출):** 반복 사이 reset은 반드시 **진짜 전원 차단(flash VCC 제거 → flash POR → 기본 1S/3-byte 복귀)**이어야 하고, **SW2 `PORz`·SW3 `RESETz` 버튼 어느 것도 안 된다**(둘 다 flash를 POR 못 함, [[CLAUDE]] "리셋/푸시버튼"). 이것이 [[jtag_flash_harness]] §3 "파워 사이클 필수"의 silicon 근거다. ②의 무토글이 (A)냐 (B)냐는, 그 "전원사이클"이 **(a)진짜 전원 차단 / (b)SW2 PORz / (c)SW3 RESETz** 중 무엇이었는지에 달림 — §② 가름 ⓪.

---

## 미확정 (정직하게 — 추론 금지)

- **warm reset 후 chip-state**: 메커니즘은 §③으로 **닫힘**(>128Mb flash warm-reset 4-byte stuck, full POR만 해소, TRM:530). 남은 미확정은 **실측 한 가지** — 이번 ②의 "전원사이클"이 진짜 VCC 제거였는지 SW3 warm reset였는지(→ §② 가름 ⓪). VCC 제거였다면 주소-불일치 실패는 배제, (B)로 무게 이동.
- **OSPI 모드 부팅 후 PWM 미관측 근본원인**: 위 (A)/(B) 어느 쪽인지 미진단. 부팅 자체가 됐는지조차 이번 세션 UART로 확인 안 함.
- ※ 2026-06-05 세션에서 standalone 부팅 banner(`eta-tx: 8kw-ev-wpt v1.0e00`)는 떴으나([[jtag_flash_harness]] §4), 그건 **다른(이전) 이미지·세션**의 증거다. 이번 토글-프리 루프 이미지의 부팅 증거로 전용하지 말 것.

---

## 함께 보기

- 굽기 메커니즘 정본(flash-time): [[jtag_flash_harness]] §7 · 클린 호스트 [[jtag_flash_clean_host]]
- SW1 부트모드 표(단일 소스): [[CLAUDE]] "하드웨어 — 부트 모드 / boot flow" 절
- 부팅 증거 채널(UART 텔레메트리): [[uart5_packet_protocol]] · [[pc_monitor_gui]]
- 측정 대상 PWM 핀·실측 PASS: [[pwm_pinmap]] · [[pwm_leg2_isoform_report]] · [[status]]
- 프로브 인벤토리: [[instruments]]
- §③ 근거: TRM [[am263p_trm]] §5.4.1(`ch05_initialization.md`:530·:761·:757·:2098) · flash 데이터시트 [[is25lx256_datasheet]] · OSPI RESET 핸드오프 [[sbl_app_flash_handoff]]
