---
date: 2026-06-04
---

# lp-am263p — 구현 현황

> 전략 spine(S0~S8)은 [[porting]], 프로젝트 호는 [[roadmap]], 확정 사실/폐기 가설은 [[flash_open_facts]], 라운드별 진단 history는 [[flash_open_diagnostic_log]].

## 다음 작업: R39 — 오실로스코프로 40MHz XTAL(Y1) 발진 확인 [내일 이어서]

R38 완료: 라인레벨로 NP 전핀 침묵 확정 → "NP 코어 미실행" 판정. 전원/리셋/level-shifter/master SPI 전부 배제. 1순위 의심 = 40MHz XTAL(Y1) 미발진이나 **추론(미측정)**. S6 블로커 = NP 하드웨어 생존.

**R39 계획(미실행)**: 사용자가 오실로스코프(MSOX3104T 1GHz급) 지참 예정. 프로브 지점 확정됨 — 실측만 남음. 측정 순서/판정은 사용자 게이트 후 진행.

### 프로브 가이드 (eta-explorer가 회로도+datasheet 교차검증으로 확정)

**우선순위 1 — Y1 발진 확인 (가장 결정적)**
- 프로브 끝: Y1 신호 단자 / R1(150Ω) 한쪽 / C6·C7(6.8pF) hot side. 핀6(HFXT_P)·핀7(HFXT_M)은 5×5 WQFN이라 직접 불가 → 패시브로 대체.
- GND 클립: P1.22 또는 P2.20.
- ⚠️ **반드시 ÷10 프로브**(÷1 ~100pF는 발진 즉사). 로딩캡 6.8pF+CL마진 5~13pF로 빠듯 — 대는 순간 발진 죽으면 아티팩트, R1 너머 반대 단자로 재시도.
- 판정: 40MHz 정현파(25ns주기)=발진OK / 양단자 DC flat=**미발진 확정(추론→사실 승격)**.
- 스코프: 5~10ns/div, BW limit OFF.

**우선순위 2 — 코어 생존(SWD/전류, Y1과 독립 교차검증)**
- J11(기본 실장, 전부 1.8V): J11.6=SWCLK, J11.8=SWDIO, J11.10=RESET_1V8, J11.16=VCC_BRD_1V8, GND=J11.1/7/13/19/20.
- 간편 판정: J15 점퍼로 CC3351 1.8V 전류 — shutdown~10µA / sleep 330µA / active 수십mA+.

**우선순위 3(선택) — SoP strap 1.8V IC측**
- R7/R8 strap 저항 패드에서 1.8V측 DC read (LP헤더 3.3V측은 R38 리셋 게이팅으로 못 읽음). 어느 저항이 핀28/29/30인지 미확정 → 멀티미터 도통 선확인 필요.

### datasheet로 바로잡은 sheet01 핀번호 어긋남 (환원 후보)
- pin6: sheet01 "XTAL_F/EXT" → datasheet **HFXT_P**
- SLOW_CLK_IN: sheet01 pin35 → datasheet **pin34** (35=VPP_IN)
- SDIO_D3(CS): sheet01 pin26(SWCLK와 충돌) → datasheet **pin21**
- HFXT_P/M = pin6/pin7 확정 (SWCLK/SWDIO = 26/27 ✓)

## 구현 현황

| 기능 | 상태 | 메모 |
|------|------|------|
| S0 AM263P 마이그레이션 | ✓ | `--device AM263Px` 빌드 성공 |
| S1 MCELF 빌드 + JTAG 플래시 | ✓ | jtag_flasher 6작업 전부 성공 (R10) |
| S2 부팅 + UART 진단 마커 | ✓ | `[DIAG] A..G` 출력 |
| S3 app `Flash_open()` 유효 핸들 | ✓ | pinmux `$assign` 교정으로 R28b 통과. RDID=`9D 5A 19` |
| S4 Drivers_open / Board_open 완주 | ✓ | R31 통과. 표준 Board_flashOpen 단독 동작 실측 검증 |
| S5 CC33xx FW 로드 + NP 기동 | △ | `Hardware init DONE!` 도달(R32). MCSPI 정상·SCLK~16 MHz 물리 확정(R36). NP 부팅/2nd-loader 완료 여부 미확인 |
| S6 SPI/IRQ link-up | ✗ | MISO flat·WLAN_IRQ flat(R36 Saleae). `SPI not responsive/CMD_ERR_TIMEOUT`. CS 프레이밍 정합 미확인 |
| S7 network_terminal CLI | ✗ | S6의 2차 결과 |
| S8 BLE HCI 경로 | ? | 미도달 |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현

## 미결 사항

- **NP 코어 미실행 원인 — 1순위 XTAL(R38)** — 전원·리셋·level-shifter 배제 완료. 40MHz XTAL(Y1) 발진 미측정. R39 오실로스코프 대상.
- **CC3351 코어 생존 미확인** — SWD(핀26/27) 또는 BP 온보드 XDS110(J10/J11) attach 미시도.
- **SoP strap 1.8V IC측 미측정** — LP헤더(3.3V)측은 level shifter 리셋 게이팅으로 읽기 불가. R7/R8 직접 프로브 필요.
- **sop2 t=283–293s SCLK 버스트 출처 불명** — wlan_start 176s 뒤. MISO 5전이로 NP 응답 증거 아님이나 반례 후보로 open.
- **CS 프레이밍 정합 미확인** — `csDisable=FALSE`(연속 assert) vs CC33xx SDK 워드별 deassert 기대 여부 미검증.
- flash FS 쓰기 미검증 — `osi_filesystem.c:131` "Skip flash writing due to APIs issue".
- [H-A] skipHwInit=TRUE 최소 충분 패치셋 미분리 — quirksFxn/skipHwInit/dummyClksCmd 중 필수 조합 미확인.
