---
tags: [reference, instrument, 계측, company-common]
source: conversation-2026-06-01 + 2026-06-15 프로브 CLI 실측(JLink ShowEmuList·pyocd·Get-PnpDevice)
date: 2026-06-30
---

# 계측 장비 인벤토리 (회사 공통)

eta 펌웨어 검증에 쓰는 계측 장비 + 프로그래밍/디버그 프로브 목록. **여러 프로젝트가 공유**하는 회사 공통 자산이라 root `pages/reference/`에 둔다 (first-ingest-wins 대상 아님 — 처음부터 공통).

파이프라인 계약: **eta-planner(계획 단계)**가 검증 경로를 짤 때 이 페이지에서 "어떤 장비로 무엇을 어떻게 측정하나"를 끌어와, 프로젝트별 검증 핀맵(예: [[gpio_verification_pinmap]])의 핀·기대값과 합쳐 "N번 핀에 스코프, 1kHz 구형파 기대" 식의 측정 가능한 검증 문장을 만든다.

각 장비 섹션 = **모델 / 핵심 spec / 무엇을 측정 / 사용 결**(프로빙·트리거·읽는 법).

---

## Keysight InfiniiVision MSOX3104T 오실로스코프

보유 1대. (기존 측정 페이지 표기 "Keysight MSO-X 3104T"와 동일 장비 — InfiniiVision 3000T X-series.)

**핵심 spec**

| 항목 | 값 |
|---|---|
| 대역폭 | 1 GHz |
| 아날로그 채널 | 4 |
| 디지털 채널 (MSO) | 16 (로직 분석) |
| 최대 샘플레이트 | 5 GSa/s |
| 트리거 | edge / pulse-width / pattern / serial (옵션) 등 |

**무엇을 측정**

- 디지털 신호의 **주기·주파수·펄스폭·듀티** (PWM, 클럭, 토글 핀)
- 두 신호 간 **시간차(latency)** — 한 핀 상승엣지 → 다른 핀 엣지까지 (커서/자동 측정)
- 신호 **레벨·엣지 무결성**, 글리치
- 아날로그 전압 레벨 (센서 출력 등, DC~)

**사용 결** (검증 워크플로)

1. 측정할 기능에 대응하는 **프로브 핀**을 [[gpio_verification_pinmap]] 같은 프로젝트 핀맵에서 확인한다.
2. 해당 핀에 프로브, GND 클립을 보드 GND에. 디버그 전용 GPIO 토글 핀이 있으면 그것을 기준으로 삼는다 (예: ESB TX 시작/ACK 수신 토글 → [[esb_timing_measurements]]).
3. 안정 측정을 위해 기준 핀 엣지로 **트리거** 건다 (보통 rising edge).
4. 주기/주파수는 자동 측정(Meas), 두 핀 시간차는 **커서** 또는 채널 간 delay 측정.
5. 파형 스크린샷을 PNG로 저장해 근거로 첨부 (예: `assets/ptx-tx-period.png`).

**실사용 선례**: [[esb_timing_measurements]] — P0.17(TX 시작)/P0.18(ACK 수신) GPIO 토글을 프로브해 TX→ACK 지연 ~470 µs, TX 주기 ~920 µs, ACK 주기 ~940 µs 측정. heartbeat 200 ms 토글 검증은 [[spi_link_reliability]].

---

## Saleae Logic Pro 16 로직 분석기

보유 1대.

**핵심 spec**

| 항목 | 값 |
|---|---|
| 채널 수 | 16 |
| 최대 샘플레이트 (디지털) | 500 MS/s |
| 최대 샘플레이트 (아날로그) | 50 MS/s |
| 입력 전압 범위 | 1.2V ~ 5V 로직 레벨 지원 |
| 소프트웨어 | Saleae Logic 2 |
| 디코더 | SPI, I²C, UART, I²S, CAN, USB 등 다수 프로토콜 소프트웨어 디코딩 |

**무엇을 측정**

- **SPI/UART/I²C 프로토콜 캡처** — CC33xx WSPI 핸드셰이크, 커맨드/응답 바이트 디코딩
- 16채널 동시 디지털 캡처 — 여러 제어 신호(CS, CLK, MOSI, MISO, IRQ, RESET)를 한 화면에
- 긴 시간 구간 캡처·검색 (오실로스코프보다 긴 기록 버퍼)
- 신호 타이밍·프로토콜 오류 탐지

**사용 결** (검증 워크플로)

1. Logic 2 소프트웨어 실행 → 채널 전압 레벨을 보드 GPIO 전압(3.3V or 1.8V)에 맞게 설정.
2. 캡처할 신호 핀을 프로젝트 핀맵에서 확인 — SPI라면 CS/CLK/MOSI/MISO 4핀 + 필요 시 IRQ/RESET.
3. 트리거: CS active(falling edge) 또는 특정 바이트 패턴.
4. 캡처 후 SPI/UART 디코더 추가 → 바이트 스트림으로 분석.
5. 캡처 결과 `.sal` 또는 CSV export해 근거로 첨부.

**실사용 선례**: 없음 (2026-06-02 등록). SPI0 CS(P2.18)·CLK(P1.7)·MOSI(P2.15)·MISO(P2.14) 캡처로 CC33xx WSPI 핸드셰이크 검증 예정 ([[status]] R35~S6).

---

## 프로그래밍/디버그 프로브 (SWD/JTAG)

펌웨어를 굽고 디버깅하는 프로브. 엄밀히 계측 장비는 아니나 검증 워크플로의 일부이고 **여러 프로젝트가 공유**(한 PC에 동시 연결)하므로 회사 공통 자산으로 함께 등록한다. 각 프로브 = **정체(ProductName·S/N)·드라이버·연결 대상·CLI 진입점**. 셋업·플래싱 절차·실측·함정은 [[st_link_nrf52_flash]](oled_tv_software 플래싱 정본).

> **★ 프로브 식별 규율 (2026-06-15 확립)**: 프로브의 정체·S/N은 **메모상 값이 아니라 매 세션 실측**으로 확인한다 — J-Link급은 `JLink.exe ShowEmuList`, ST-Link는 `pyocd list`. 사람이 부르는 **별명**(예 "J-OB v2")과 펌웨어가 보고하는 **정체**(ProductName/S/N)는 **분리 표기**하고, 둘을 1:1로 못박을 땐 ShowEmuList 실측 근거를 단다. 실측 출처 없이 메모에만 있는 SN/정체는 "현존 미확인"으로 본다. (이 규율은 아래 §정정 — 같은 동글이 세션마다 다른 정체로 기록돼 시간을 버린 사건에서 나왔다.)

### J-Link V9.3 Plus (S/N 69730359) — nRF52832 정본 프로브 [2026-06-15 실측]

현행 nRF52832 플래싱 정본 프로브. ShowEmuList 실측으로 정체 확정.

| 항목 | 값 |
|---|---|
| 정체 (ShowEmuList 실측 2026-06-15) | ProductName **"J-Link CE"**, Nickname "J-Link V9.3 Plus", S/N **69730359** |
| HW / FW | HW **V9.70** / FW "J-Link V9 (compiled Dec 13 2022)" |
| License | RDI, FlashBP, FlashDL, JFlash, GDB |
| 드라이버 | SEGGER J-Link (네이티브). WinUSB·Zadig 불요 |
| USB | VID_1366 PID_0105. CDC UART = COMx (가변, 이번 세션 COM20) |
| 연결 대상 | nRF52832 **커스텀보드** [[schematic_ble_module_board_v01e00]] (UTO-NBL-52 기반) — **02·03 둘 다 flash 실측 통과** (DK 아님, 외부 SWD/CON1) |
| CLI 진입점 | `JLink.exe -device nRF52832_xxAA -if SWD -speed 4000 -SelectEmuBySN 69730359 -NoGui 1 -ExitOnError 1 -CommandFile <script>` / SES Download&Reset / nrfjprog |
| 실측 (2026-06-15) | 공통 SW-DP ID `0x2BA01477`, Cortex-M4 r0p1, Bank0@0x0 **57344 B**, program+verify O.K., **exit 0**. 보드별 FICR DEVICEID[0](`0x10000060`): **02=`0x5FE168DA`**(VTref 3.1~3.3 V), **03=`0xE9775EC9`**(VTref 3.261 V). 빌드 dev HEAD `6fc8b92` |

### ST-Link V2 — STM32 (01_RX_control)

| 항목 | 값 |
|---|---|
| 정체 (pyocd list 실측) | "STM32 STLink", UID `40004100040000433539594E` |
| 드라이버 | ST 정품 STLink (네이티브). WinUSB·Zadig 불요 (단 pyOCD 폴백 사용 중엔 WinUSB 바인딩 → [[st_link_nrf52_flash]]) |
| 연결 대상 | STM32F103RCTx (`01_RX_control`) |
| CLI 진입점 | `STM32_Programmer_CLI.exe` (CubeIDE 2.1.1 번들 v2.22) / CubeIDE F11 / CubeProgrammer GUI |
| 실측 (2026-06-05) | ST-Link FW **V2J47S7**. connect 시 `Device ID 0x414`(F103 High-density), Cortex-M3, NVM 256 KB, 3.27 V |
| ⚠ 함정 | S/N이 `@`로 보고됨(cosmetic) → 다중 ST-Link 시 `sn=` 타게팅 불가, 인덱스 우회. 현재 단일이라 무영향 |

### SAM-ICE (S/N 24012600) — 사용자 별명 "J-OB v2"

| 항목 | 값 |
|---|---|
| 정체 (ShowEmuList 실측 2026-06-15, 버스 단독) | ProductName **"SAM-ICE"**, S/N **24012600** |
| 사람 별명 | 사용자가 "J-OB v2"라 부르는 동글 = 이 유닛 (버스에 단독으로 꽂아 확인) |
| 드라이버 | SEGGER J-Link |
| 연결 대상 / 용도 | **미상**. 현재 nRF flash엔 J-Link V9.3 Plus(69730359)를 쓴다 |
| ⚠ | 종전 인벤토리의 "J-OB v2 = `J-Link OB-nRF5340-NordicSemi` / S/N 1050329071" 귀속과 **모순** — 아래 §정정 |

### ⚠ 정정 — "J-Link OB-nRF5340-NordicSemi" S/N 1050329071 = 현존 미확인 [2026-06-15]

종전(2026-06-05) 인벤토리·플래싱 페이지는 nRF 프로브를 **정품 `J-Link OB-nRF5340-NordicSemi`, S/N 1050329071**로 단정하고, 그 위에 "J-Link급 2개(1050329071 + 24012600) 동시 present → SN 충돌 → `-SelectEmuBySN` 필수" 함정까지 쌓았다. **2026-06-15 실측이 이를 반박한다**:

- S/N **1050329071**은 이번 세션 내내 `ShowEmuList`·`Get-PnpDevice -PresentOnly` 어디에도 **enumerate되지 않음** → 현 책상에 **부재**.
- "J-OB v2"라 부르던 동글을 버스에 **단독**으로 꽂아 확인하니 **SAM-ICE / 24012600**으로 보고됨 → "1050329071(J-OB v2)"과 "24012600(SAM-ICE)"을 **별개 2프로브로 본 전제 재현 불가**. 같은 물리 유닛을 세션마다 다른 정체로 오기록했을 가능성이 높다.
- ∴ **1050329071은 ShowEmuList 재확인 전까지 "현존 미확인"**. 이에 의존한 "2프로브 공존 → SN 충돌" 함정도 전제 미성립 → **강등**. (단 `-SelectEmuBySN`은 J-Link급이 실제 ≥2 present일 때 여전히 권장 — 현재는 69730359 + 24012600 공존이 그 경우다. 정체를 ShowEmuList로 확인한 뒤 SN을 박는다.)
- 2026-06-05의 "1050329071 connect·03 flash 통과(FICR `0x2365A055`)" 기록은 **당시 기록으로만** 보존 — 정체 귀속(1050329071)이 재현되지 않았으므로 현행 정본 아님.

> ⚠ 02·03은 **nRF52 DK가 아니라 커스텀보드**([[schematic_ble_module_board_v01e00]])다 — DK 온보드 J-Link로 굽는다는 종전 서술은 폐기(2026-06-15). 두 nRF 보드 모두 위 외부 J-Link V9.3 Plus(69730359)로 flash. lp-am263p는 TI XDS110 — 해당 프로젝트 페이지 참조.

---

## Rohde & Schwarz RTM3004 오실로스코프

보유 1대.

**핵심 spec**

| 항목 | 값 |
|---|---|
| 아날로그 채널 | 4 |
| 최대 샘플레이트 | 5 GSa/s |
| ADC 해상도 | 10-bit |
| 대역폭 | — (미확인, 추가 필요) |
| 트리거 | — (미확인, 추가 필요) |

**무엇을 측정**

- 10-bit ADC로 **아날로그 파형 정밀 측정** — MSOX3104T(8-bit) 대비 수직 해상도 우위
- 디지털 신호 주기·주파수·펄스폭·듀티
- 두 신호 간 시간차(latency)
- 아날로그 전압 레벨·리플·노이즈 플로어

**사용 결** (검증 워크플로)

MSOX3104T와 동일 절차. 10-bit 해상도가 필요한 아날로그 정밀 측정(예: ADC 노이즈 FFT, 리플 측정)에 우선 사용.

---

## (장비명 — 사용자 호명 대기)

> 추가 보유 장비(멀티미터·전원공급기·함수발생기 등). 사용자가 모델·용도를 불러주면 위 형식(모델/spec/무엇을/사용 결)으로 채운다. **추론으로 장비를 지어내지 않는다.**
