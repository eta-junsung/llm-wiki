---
tags: [reference, instrument, 계측, company-common]
source: conversation-2026-06-01
date: 2026-06-01
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

펌웨어를 굽고 디버깅하는 프로브. 엄밀히 계측 장비는 아니나 검증 워크플로의 일부이고 **여러 프로젝트가 공유**(한 PC에 동시 연결)하므로 회사 공통 자산으로 함께 등록한다. 각 프로브 = **정체(S/N)·드라이버·연결 대상·CLI 진입점**. 셋업·플래싱 절차·실측·함정은 [[st_link_nrf52_flash]](oled_tv_software 플래싱 정본).

> ⚠ 이 PC엔 **J-Link급 프로브가 둘**(J-OB v2 + SAM-ICE) → JLink.exe 무지정 시 connect 실패. 반드시 `-SelectEmuBySN <S/N>`로 못박는다.

### ST-Link V2 — STM32 (01_RX_control)

| 항목 | 값 |
|---|---|
| 드라이버 | ST 정품 STLink (네이티브). WinUSB·Zadig 불요 |
| 연결 대상 | STM32F103RCTx (`01_RX_control`) |
| CLI 진입점 | `STM32_Programmer_CLI.exe` (CubeIDE 2.1.1 번들 v2.22) / CubeIDE F11 / CubeProgrammer GUI |
| 실측 (2026-06-05) | ST-Link FW **V2J47S7**. connect 시 `Device ID 0x414`(F103 High-density), Cortex-M3, NVM 256 KB, 3.27 V |
| ⚠ 함정 | S/N이 `@`로 보고됨(cosmetic) → 다중 ST-Link 시 `sn=` 타게팅 불가, 인덱스 우회. 현재 단일이라 무영향 |

### J-Link OB-nRF5340-NordicSemi ("J-OB v2") — nRF52832 회사보드 (03_TX_ble)

| 항목 | 값 |
|---|---|
| 정체 | `J-Link OB-nRF5340-NordicSemi` (Nordic 정품, **클론 아님**, FW mismatch 경고 없음) |
| S/N | **1050329071** |
| HW / License | HW V1.00 / RDI, FlashBP, FlashDL, JFlash, GDB |
| 드라이버 | SEGGER J-Link |
| 설치 | `C:\Program Files\SEGGER\JLink_V948\JLink.exe` (V942도 공존) |
| 연결 대상 | nRF52832 회사 커스텀보드 (`03_TX_ble`) |
| CLI 진입점 | JLink.exe / nrfjprog / SES Download&Reset |
| 실측 (2026-06-05) | `nRF52832_xxAA`, SWD 4000 kHz, SW-DP ID `0x2BA01477`, Cortex-M4 r0p1, VTref 3.300 V, FICR `0x10000060=0x2365A055`. program+verify 통과 (Bank0@0x0 53248 B, exit 0) |
| ⚠ 함정 | SAM-ICE와 공존 → `-SelectEmuBySN 1050329071` 고정 필수 (무지정 시 connect 실패) |

### SAM-ICE — (연결 대상 미상)

| 항목 | 값 |
|---|---|
| 정체 | `SAM-ICE` (Atmel/Microchip 브랜드 J-Link급 프로브) |
| S/N | **24012600** |
| 드라이버 | SEGGER J-Link |
| 연결 대상 | 빈자리 — 미상 (현재는 J-OB v2와의 **SN 충돌원**으로만 인지) |

> nRF52 DK(`02_RX_ble`)는 **보드 온보드 J-Link**라 별도 외부 프로브가 아니다 — 위 인벤토리 밖. (lp-am263p는 TI XDS110 사용 — 해당 프로젝트 페이지 참조.)

---

## (장비명 — 사용자 호명 대기)

> 추가 보유 장비(멀티미터·전원공급기·함수발생기 등). 사용자가 모델·용도를 불러주면 위 형식(모델/spec/무엇을/사용 결)으로 채운다. **추론으로 장비를 지어내지 않는다.**
