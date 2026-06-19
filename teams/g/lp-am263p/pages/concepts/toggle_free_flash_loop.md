---
tags: [concept, flash, boot, ospi, am263p, workflow, deadtime, open]
source: 실측 (2026-06-12, 8kw-ev-wpt-tx 실보드 — 굽기 ✓ / 부팅 ✗ ROM→SBL 실패 확정) + 문서조사 (2026-06-12, AM263P TRM §5.4.1·UG·IS25LX256 데이터시트·회로도 — §③)
date: 2026-06-12
---

# 토글-프리 flash 반복 루프 — 굽기 ✓ / 부팅 ✗ 실패확정 (ROM→SBL)

> **board-common(lp-am263p) 워크플로 페이지.** SW1 부트모드를 매 반복 토글하지 않고 빌드→flash→전원사이클을 도는 루프가 성립하는가에 대한 현재 진실.
> 굽기 메커니즘의 정본은 [[jtag_flash_harness]] §7. 부팅 실패 진단 채널·triage recipe는 [[ospi_boot_console_diagnostic]].
>
> ⚠️ **2026-06-12 해소 — 부팅 절반의 진짜 원인은 부트모드 스트랩 미스매치였다.** 아래 §②/§③은 SW1을 잘못된 스트랩(`1,1,1,1`=OSPI 4S Quad)에 고정한 채 루프를 돌려 ROM→SBL 실패(`'C'` ping)를 본 기록이다. 보드 flash(IS25LX256)는 octal-only라 4S(`0x6B`/QE)가 물리적으로 불가 — **SW1=`0,0,1,1`(xSPI 8D SFDP)로 교정하니 같은 이미지가 완전 부팅**. ⟹ "flash 프로그래밍/설정 잔여 블로커"는 무효. 정본 [[ospi_boot_mode_strap]]. 아래 본문은 그 맥락에서 읽을 것.

---

## 동기 (왜 이 루프인가)

8kw-ev-wpt-tx(AM263P, R5F nortos) dead-time 테스트 펌웨어를 CCS 없이 GUI/스크립트로 빌드·flash하는 워크플로. HW 엔지니어가 `ETA_DEADTIME_NS`([[pwm_pinmap]]·`eta_tuning.h`)를 바꿔 **재빌드 → 재flash → 재부팅**을 반복(build-per-change)한다. **매 반복마다 SW1 부트모드 토글(DevBoot `0,1,0,0` ↔ OSPI(4S) `1,1,1,1`)을 피하는 것**이 목표 — SW1을 OSPI에 고정해 둔 채 루프를 돌 수 있으면 가장 편하다.

정본 flash 하네스 = `flash_node_8kw.js`(Node.js `runAsynch`, CCS2050 `run.bat`). `flash_8kw.js`(Rhino/`GEL_RunF`)는 deprecated([[jtag_flash_harness]] §1).

---

## 루프의 두 절반 — 현재 상태

| 절반 | 내용 | 상태 | 근거 |
|------|------|------|------|
| **① 굽기** | SW1=OSPI(4S)=`1,1,1,1` 고정(app 부팅돼 돌던 상태)에서 flash | **✓ 확정** | run_flash_node_8kw 3/3 OK·EXIT 0, `loadProgram` soft-reset로 코어 인수 ([[jtag_flash_harness]] §7) |
| **② 부팅** | **올바른 스트랩(SW1=`0,0,1,1`=xSPI 8D SFDP)** 에서 전원사이클만으로 새 이미지 standalone 부팅·구동 | **✓ 확정 (2026-06-12)** | VCC 완전 제거 후 재인가 → SBL → `"Image loading done, switching to application"` → app → `eta-tx: 8kw-ev-wpt start`. 정본 [[ospi_boot_mode_strap]] |
| ②′ (오설정) | ~~SW1=`1,1,1,1`(4S Quad)에서 부팅~~ | **✗ 불가** | octal-only 칩이 ROM `0x6B`/QE 기대를 못 받음 → `'C'` ping. 2026-06-12 무부팅의 직접 원인. [[ospi_boot_mode_strap]] |

→ **올바른 스트랩에서 ①(굽기)·②(부팅) 양쪽 확정 → 토글-프리 루프 닫힘.** (단 매 반복 사이 reset은 §③대로 진짜 VCC 차단이어야 한다 — SW1 모드 토글은 불요.)

---

## ① 굽기 절반 (✓ 확정) — 요약

[[jtag_flash_harness]] §7 정본. 핵심만:
- SW1=`1,1,1,1`(보드가 OSPI에서 부팅돼 **app 실행 중**) + CCS IDE 완전 종료(클린 호스트, §2)에서 **3/3 OK, EXIT 0**.
- 메커니즘: 하네스가 매 OP `loadProgram` 시 `"CPU reset (soft reset) has been issued through GEL on program load"` — 코어를 soft-reset해 돌던 app으로부터 점유를 깨끗이 인수.
- ⟹ 굽기에 DevBoot는 **필수 아닌 편의**. (DevBoot의 "No SBL"은 안정성/속도 편의일 뿐.)

---

## ② 부팅 절반 (✗ 실패는 **잘못된 스트랩** 때문 — 2026-06-12 strap 교정으로 ✓ 해소)

> 아래는 SW1=`1,1,1,1`(OSPI 4S Quad)에 고정한 채 본 ROM→SBL 실패 기록이다. triage(C ping = ROM→SBL 실패)는 정확했으나, 그 원인을 §③ "flash 프로그래밍/설정"으로 귀속한 것은 **오류** — 진짜 원인은 octal-only 칩에 4S 스트랩이 어긋난 것. [[ospi_boot_mode_strap]].

굽기(§①) 직후 **SW1=`1,1,1,1` 유지 + 전원사이클(VCC 완전 제거 — USB-unplug 확인)** 후 COM4(= SoC UART0 콘솔, "XDS110 Class Application/User UART") 115200/8N1 캡처:

- **관측**: ROM UART fallback `0x43('C')` XMODEM ping + ID 블롭(`"AM263PX"/cdab=0xABCD/32B hash`) 주기 반복. **SBL banner · app banner(`eta-tx: 8kw-ev-wpt start`) 전무.**
- **판정**: **(A) 부팅 실패 — ROM→SBL 로드 단계에서 막힘.** 근거:
  - `'C'` ping은 **ROM만 송신** (TRM `ch05_initialization.md`:877).
  - ROM은 OSPI 부팅 "any failures"면 UART fallback 진입 (TRM ch05:133).
  - ROM이 SBL 점프 성공하면 그 뒤 SBL이 죽어도 ROM 레벨 fallback 없음 → **`'C'` ping = ROM이 SBL 로드 자체 실패. SBL→app 핸드오프 상류.**
- **전원사이클 방법 확정**: 전부 USB-unplug VCC 완전 차단·SW2/SW3 버튼 안 씀 → §③의 >128Mb flash 4-byte stuck 경로 **완전 배제**.
- **원인 (2026-06-12 확정)**: warm reset 주소 불일치도, flash 프로그래밍/설정도 아니다 — **SW1=`1,1,1,1`(4S Quad) 스트랩이 octal-only IS25LX256과 미스매치**. ROM이 `0x6B`+QE를 기대하나 칩에 없음 → read 실패 → `'C'`. **SW1=`0,0,1,1`(xSPI 8D SFDP)로 교정 → 같은 이미지 완전 부팅.** 정본 [[ospi_boot_mode_strap]]. (종전 "flash 프로그래밍/설정 잔여 블로커" 가설은 무효.)
- Logic2 PWM 무토글 관측은 부팅 실패의 귀결 — ROM 단계에서 부팅이 실패했으니 PWM 초기화도 없음. **commit `4014901` Saleae PWM PASS와 혼동 금지** (그쪽은 다른 이미지·셋업에서 정상 부팅 후 의도된 검증 — 이번 무토글이 그 PASS를 뒤집는 증거가 아님).

상세 진단 채널·boot stage triage recipe·SBL provenance: [[ospi_boot_console_diagnostic]].

---

## ③ TRM/UG 근거 — boot 경로는 정당, 단 reset 방법이 결정적 (2026-06-12 문서조사)

TRM(`raw/am263p_trm/ch05_initialization.md`)·UG·IS25LX256 데이터시트·보드 회로도로 OPEN을 조사한 결과. **토글-프리 boot 경로의 일반 원리(SW1 고정 → 매 POR 같은 모드 재진입)는 정당**하나, 당시 고정한 모드(`1,1,1,1`=4S)가 칩과 어긋난 것이 핵심이었다.

### 토글-프리 boot 경로는 silicon상 정당 (FACT) — 단 **올바른 모드여야 한다**

- **BOOTMODE 핀은 매 POR/reset release마다 재샘플링** — TRM §5.1.1(:111)·§5.3(:480 "After every POR, they are the main source"). ⟹ SW1 고정이면 **매 전원사이클이 결정적으로 같은 부팅 모드 재진입**. DevBoot 토글이 boot에 필요한 게 아님. (올바른 모드 = **xSPI 8D SFDP `0,0,1,1`**, [[ospi_boot_mode_strap]]; ~~4S `1,1,1,1`~~은 octal-only 칩에 불가.)
- **OSPI boot은 non-XIP** — TRM §5.4.1.3.1.1(:761): ROM이 매 부팅 시 flash→on-chip RAM으로 이미지를 **새로 복사** 후 실행. ⟹ 재flash 이미지는 **다음 전원사이클에 그대로 반영**. (굽기 ✓ + 전원사이클 = 새 이미지 적재.)
- ⚠️ **모순**: 종전 기록은 "2026-06-05 banner 부팅도 SW1=`1,1,1,1`(OSPI 4S)에서 났다"고 적었으나, **octal-only 칩에서 4S 부팅은 물리적으로 불가**(§②′·[[ospi_boot_mode_strap]] §2). 당시 SW1 라벨 식별이 틀렸을 가능성이 큼([추정] — 라벨이 이번 세션 전까지 잘못돼 있었음). 06-05에 실제 물리 스위치가 어디였는지는 **미확정(모름)**.

### reset 방법이 결정적 — >128Mb flash 3-byte/4-byte 위험 (FACT, "warm-reset chip-state"의 근본원인)

TRM §5.4.1 Note(`ch05_initialization.md`:530):
> ">128 Mb flash는 RESET 신호 패키지 필수. ROM은 3-byte(24-bit) 주소만 쓰는데 SW는 보통 4-byte로 전환한다. **warm reset 시 ROM은 3-byte 기대 / flash는 4-byte로 남음** → flash를 RESET 신호로 리셋해야 3-byte 복귀. **ROM은 software reset 명령을 내지 않는다.**"

우리 케이스에 정확히 적용:
- IS25LX256 = **256 Mb(>128Mb)**, Octal DDR에서 **주소 4-byte 고정**(`raw/IS25LX256/ch00_frontmatter.md`:161). ROM은 4S/8S에서 3-byte(:735).
- ⟹ app이 flash를 Octal DDR(4-byte)로 둔 상태에서 **flash를 POR하지 못하는 리셋**(아래 버튼 둘 / WDT 180s warm reset — TRM:2098 / flasher `loadProgram` soft-reset)이 나면 **ROM이 SBL을 못 읽어 boot 실패**. flash RESET# 어서트 또는 **full POR만 해소**.
- **보드 버튼 둘 다 flash를 POR하지 못한다**(회로도 sheet 6 + UG Fig 2-10/2-11 — 단일 소스 [[CLAUDE]] "리셋/푸시버튼"): **SW2 `PORz`**(콜드급 PORz — UG:431)도 **SW3 `RESETz`**(warm reset — UG:432)도, 그 리셋 트리에 flash 3.3V 전원도 flash RESET#도 묶여 있지 않음. 둘 다 SoC만 리셋·SOP(부트모드) 재래치할 뿐 flash 상태는 그대로 둔다.
- 보드는 flash RESET#을 **실제 배선**: `AM263P_OSPI0_RST`(직렬 R99 22Ω) → SoC OSPI_RESET_OUT 핀(UG GPIO19/20 = OSPI_RESET_OUT0/1). flasher의 `flashFixUpOspiBoot()`가 이 핀을 토글해 1S 복귀([[sbl_app_flash_handoff]]:86). **그러나 ROM은 bare reset에선 이 핀을 안 건드린다**(:530 "ROM does not issue a software reset").
- ~~부수 전제: 4S boot은 flash **QE bit가 NV config에 SET** 필요(TRM:757) — 06-05에 4S로 부팅됐으니 충족된 것으로 보임.~~ **무효**: 이 칩(IS25LX256)에는 QE bit 자체가 없고(octal-only), 4S로 부팅한 적도 없다. TRM:757 인용은 정확하나 "이 보드가 4S 부팅"이라는 전제가 오류. [[ospi_boot_mode_strap]] §2.

> **루프 운영 규칙(문서 도출):** 반복 사이 reset은 반드시 **진짜 전원 차단(flash VCC 제거 → flash POR → 기본 1S/3-byte 복귀)**이어야 하고, **SW2 `PORz`·SW3 `RESETz` 버튼 어느 것도 안 된다**(둘 다 flash를 POR 못 함, [[CLAUDE]] "리셋/푸시버튼"). 이것이 [[jtag_flash_harness]] §3 "파워 사이클 필수"의 silicon 근거다.
>
> **2026-06-12 실측 갱신**: ②의 전원사이클은 USB-unplug VCC 완전 제거로 확정(§②) → 4-byte stuck 경로 배제 완료. ~~부팅 실패 원인은 flash 프로그래밍/설정 문제~~ → **부팅 실패 원인은 부트모드 스트랩 미스매치로 확정, strap 교정으로 해소**([[ospi_boot_mode_strap]]).

---

## 미확정 (정직하게 — 추론 금지)

- ~~warm reset 후 chip-state~~ — **✅ 해소**: ②의 전원사이클이 USB-unplug VCC 제거로 확정(§②) → §③의 4-byte stuck 경로 완전 배제.
- ~~OSPI 모드 부팅 후 PWM 미관측 근본원인~~ — **✅ 해소**: (A) ROM→SBL 로드 단계 실패로 확정(§②, COM4 UART0 진단). (B) 측정 배선 문제 배제.
- ~~flash 프로그래밍/설정 미확정 (잔여 블로커)~~ — **✅ 해소(무효 가설)**: ROM이 SBL을 못 읽은 건 (a)cell 영속성·(b)QE bit 때문이 아니라 **부트모드 스트랩이 octal-only 칩과 미스매치**였기 때문. strap 교정(`0,0,1,1`)으로 같은 flash가 정상 부팅 → cell·QE 문제 모두 부존재. 정본 [[ospi_boot_mode_strap]].
- ~~현재 이미지로 standalone 부팅 증거 없음~~ — **✅ 해소(2026-06-12)**: 올바른 스트랩에서 현재 route② 이미지가 `eta-tx: 8kw-ev-wpt start` banner까지 완전 부팅([[ospi_boot_console_diagnostic]] §5). (2026-06-05 banner `...v1.0e00`는 여전히 구 이미지.)
- **모름**: 2026-06-05 부팅이 실제 어느 스트랩이었는지 — "1,1,1,1"이라는 기록은 octal-only 칩에 불가하므로 라벨 오기 추정([추정]), 물리 스위치 위치 미확정.

---

## 함께 보기

- 굽기 메커니즘 정본(flash-time): [[jtag_flash_harness]] §7 · 클린 호스트 [[jtag_flash_clean_host]]
- **standalone 무부팅 진짜 원인 = 부트모드 스트랩 미스매치 (해소 정본)**: [[ospi_boot_mode_strap]]
- 부팅 진단 채널·triage recipe: [[ospi_boot_console_diagnostic]]
- SW1 부트모드 표(단일 소스): [[CLAUDE]] "하드웨어 — 부트 모드 / boot flow" 절
- 부팅 증거 채널(UART 텔레메트리): [[uart5_packet_protocol]] · [[pc_monitor_gui]]
- 측정 대상 PWM 핀·실측 PASS: [[pwm_pinmap]] · [[pwm_leg2_isoform_report]] · [[status]]
- 프로브 인벤토리: [[instruments]]
- §③ 근거: TRM [[am263p_trm]] §5.4.1(`ch05_initialization.md`:530·:761·:757·:2098) · flash 데이터시트 [[is25lx256_datasheet]] · OSPI RESET 핸드오프 [[sbl_app_flash_handoff]]
