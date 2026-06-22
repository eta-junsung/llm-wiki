---
tags: [concept, gpio, verification, pinmap]
source: 기존 wiki 사실 종합 (rx_control, esb_timing_measurements, spi_link_reliability, adc_channel_map) + conversation-2026-06-01 + 2026-06-17 UTO-NBK-52 실측
date: 2026-06-17
subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble, 04_tx_control
---

# GPIO 검증 핀맵 (oled_tv_software)

**파이프라인 계약**: eta-planner(계획 단계)가 검증 경로를 짤 때 읽는 표. "어떤 기능을 확인하려면 **몇 번 핀**에 스코프를 찍고 **무슨 값**을 보면 되는가"를 한 줄로 끌어간다. 장비는 [[instruments]], 핀의 1차 사실 출처는 entity 페이지([[rx_control]] 등)다 — 이 페이지는 그 사실을 **검증 목적**으로 재배열한 뷰.

> ⚠ 핀 번호·신호·기대값은 보드 자료에서 확인된 것만 적는다. 미확인은 빈칸(`?`)으로 호명하고 **추론으로 채우지 않는다**. 아래 "확인 필요" 절 참조.

기본 계측 장비는 [[instruments]]의 **Keysight InfiniiVision MSOX3104T** (별도 표기 없으면 이것).

---

## 01_RX_control (STM32F103RCT6)

| 검증 대상 (기능) | 프로브 핀 | 신호명 | 트리거 / 기대값 | 근거 |
|---|---|---|---|---|
| SPI CS 폴링 주기 (10ms 검증) | **PB12** | SPI nCS (`SPI_nCS`, SW 토글) | CS low 주기 측정 — 목표 10 ms. **현재 미동작**(다음 시작점 검증 대상) | [[rx_control]], [[spi_link_reliability]] |
| SPI 클럭 활성 | **PB13** | SPI2_SCK | 전송 중 SCK 버스트, **8.0 Mbps**(`/4`, PCLK1=32 MHz, HSI 기준) | [[rx_control]], [[sysclk_hsi_transition]] |
| PWM1 출력 | **PC6 / PC7** | PWM1_P / PWM1_N ([[tim8]] CH1/CH2) | 100 kHz 구형파, 듀티 가변 | [[rx_control]], [[pwm_system]] |
| PWM2 출력 | **PC8 / PC9** | PWM2_P / PWM2_N ([[tim3]] CH3/CH4) | 100 kHz, PWM1 대비 120° 위상지연(=3 µs) | [[pwm_system]] |
| Trip Zone 차단 | **PA6** | BKIN (active high) | PA6 high → PWM 전출력 차단 확인 | [[trip_zone]] |
| ADC 센싱 입력 | **PA0~PA3, PC4, PC5** | ADC1 6ch (아날로그) | 센서 전압 0~3.3 V. TEMP1/TEMP2 라벨 swap 함정 주의 | [[adc_channel_map]] |
| FAULT_RST | `?` | FAULT_RST_uC | `?` (핀번호 미확인) | [[rx_control]] "추가 디지털 신호" |
| LATCH_FAULT | `?` | LATCH_FAULT_uC | `?` | [[rx_control]] |
| nSYS_RDY | `?` | nSYS_RDY_uC (active low 추정) | `?` | [[rx_control]] |
| DBG_LED1/2/3 | `?` | DBG_LED*_uC | `?` | [[rx_control]] |
| TEST_MODE1/2 | `?` | TEST_MODE*_uC | `?` | [[rx_control]] |
| LSG1/2 게이트 | `?` | LSG*_OP_SEL_uC | `?` | [[rx_control]] |

## 01_RX_control UART5 검증 세팅 (보드 단독)

이 보드만으로 UART5(PC12/PD2)를 검증하려면 **두 전원 도메인을 별도 공급**해야 한다. COMM_P5V(5V)는 ISOL2 통신측·MAX232 전원 — 없으면 TP17/TP15 신호 미출력.

### 필수 전원

| 공급 | 진입점 | GND | 용도 |
|---|---|---|---|
| **3.3V** | CN1.1 또는 CN1.2 | CN1.27 또는 CN1.28 (DGND) | MCU(STM32) + ISOL2 MCU측 |
| **5V** | CON2.1 (COMM_P5V) | CN1.27 공용 가능 (※) | ISOL2 통신측 + MAX232 |

> ※ p.4 B3(SHH-1M2012-221 페라이트 비드) One Point 결합: DGND ↔ COMM_GND가 DC 기준 공유됨 → CN1.27 GND 한 선으로 두 전원 GND를 묶어도 됨.

### 옵션 A — CON2 경유 (RS232, 설계 의도 경로)

```
STM32 TX → ISOL2 → MAX232 T1IN → T1OUT → CON2.3 (SCIB_TXD232_CN)
STM32 RX ← ISOL2 ← MAX232 R1OUT ← R1IN ← CON2.2 (SCIB_RXD232_CN)
```

| 항목 | 내용 |
|---|---|
| 필요 어댑터 | **USB-to-RS232** (USB-to-TTL 직접 연결 불가 — RS232 레벨) |
| PC RX (STM32→PC) | **CON2.3** (SCIB_TXD232_CN) |
| PC TX (PC→STM32) | **CON2.2** (SCIB_RXD232_CN) |

### 옵션 B — TP17/TP15 경유 (5V TTL, MAX232 우회)

```
STM32 TX → ISOL2 → TP17 (SCIB_TX, 5V TTL) ── 직접 프로브
STM32 RX ← ISOL2 ← TP15 (SCIB_RX, 5V TTL) ── 직접 프로브
```

| 항목 | 내용 |
|---|---|
| 필요 어댑터 | **5V 허용 USB-to-TTL** (3.3V 전용 어댑터는 5V 신호로 손상 위험) |
| PC RX (STM32→PC) | **TP17** (SCIB_TX, p.4 ISOL2 B2 출력) |
| PC TX (PC→STM32) | **TP15** (SCIB_RX, p.4 ISOL2 B1 출력) |
| GND | COMM_GND (CN1.27과 B3 결합, 공통 GND 사용 가능) |

### 옵션 비교

| | A (CON2 RS232) | B (TP17/TP15 TTL) |
|---|---|---|
| 어댑터 | USB-to-RS232 필요 | 5V-tolerant USB-to-TTL |
| 납땜 | 불필요 (커넥터 있음) | TP에 핀헤더/와이어 납땜 필요 |
| 신호 레벨 | RS232 (±V) | 5V TTL |
| COMM_P5V 필요 | ✓ (MAX232 전원) | ✓ (ISOL2 통신측 전원) |

---

## 02_RX_ble / 03_TX_ble (nRF52832, ESB)

| 검증 대상 (기능) | 서브시스템 | 프로브 핀 | 신호명 | 트리거 / 기대값 | 근거 |
|---|---|---|---|---|---|
| ESB TX 전송 주기 | 03_TX_ble | **P0.17** | TX 시작 토글 (측정 전용) | ~920 µs 주기 | [[esb_timing_measurements]] |
| ESB TX→ACK 지연 | 03_TX_ble | P0.17 → **P0.18** | TX 시작 → ACK 수신 | ~470 µs (두 엣지 시간차, 커서) | [[esb_timing_measurements]] |
| ESB ACK 수신 주기 | 03_TX_ble | **P0.18** | ACK 수신 토글 (측정 전용) | ~940 µs 주기 | [[esb_timing_measurements]] |
| SPI heartbeat 200 ms | 02_RX_ble | **P0.17** `PIN_DBG_HB` | heartbeat 디버그 토글 | 200 ms 토글 (Δt≈190 ms 실측) | [[spi_link_reliability]] |
| LED1 System Ready | 03_TX_ble | **P0.09** `PIN_LED1` | LED1_uC (회사 보드) | 상시 점등 (active-high, 1=ON) | [[schematic_ble_module_board_v01e00]] |
| LED2 SPI Comm Status | 03_TX_ble | **P0.08** `PIN_LED2` | LED2_uC | 200 ms 토글 (점멸) | [[schematic_ble_module_board_v01e00]] |
| LED3 BLE(=ESB) Comm Status | 03_TX_ble | **P0.06** `PIN_LED3` | LED3_uC | ESB UP → **상시 점등** / DOWN → 소등 | [[schematic_ble_module_board_v01e00]] |

> P0.17/P0.18 토글은 측정 전용 디버그 코드 — 검증 종료 후 제거 여부 결정 대상 ([[tx_ble_module]]).
> **P0.17 중복은 충돌 아님**: 02_RX_ble와 03_TX_ble는 동일 nRF52832 커스텀 보드(UTO-NBL-52 기반) **물리적으로 별개 보드 2대**다. 같은 핀번호(P0.17)가 각 보드에서 다른 용도(02=heartbeat `PIN_DBG_HB` / 03=TX 시작 토글)로 쓰이는 것이며, 한 핀의 의미 충돌이 아니다.

> LED 핀/극성은 **회사 BLE_Module_Board(BOARD_CUSTOM 빌드)** 기준 — 2026-06-04 실보드 실측 확정. PCA10040 DK로 빌드하면 P0.06/08은 UART, P0.17~20은 온보드 LED라 의미가 다르며, LED 코드는 `#if defined(BOARD_CUSTOM)` 가드로 회사 빌드에서만 컴파일된다. LED 핀맵 1차 출처 → [[schematic_ble_module_board_v01e00]].

---

## 02_RX_ble / 03_TX_ble — 커스텀 보드 UTO-NBK-52 (2026-06-17 실측)

> PCA10040 DK와 핀·극성이 다름. DK 핀맵은 위 "02_RX_ble / 03_TX_ble" 절.

| 검증 대상 | 핀 | 신호 | 기대값 | 비고 |
|----------|----|------|--------|------|
| LED1 System Ready | **P0.09** | active-high | 상시 점등 | NFC 핀 → `CONFIG_NFCT_PINS_AS_GPIOS` 필수. cold-boot 후 확인 ([[nfc_pins_gpio]]) |
| LED2 SPI Comm St | **P0.08** | active-high | 200ms 점멸 (SPI UP 시) | SPI heartbeat |
| LED3 BLE Comm St | **P0.06** | active-high | 200ms 점멸 (ESB UP 시) | ESB health |
| UART TXD (모니터) | **P0.15** | 격리형 UART | nRF 텍스트 모니터 출력 | 별도 USB-to-TTL 필요 (DK VCP 아님) |
| SPI NSS | **P0.22** | active LOW | CS 10ms 주기 | STM32 PB12 대응 |
| RESET (SW1) | **P0.21** | PINRESET | CPU+RADIO 전정지 | comm_st 케이스 검증용. halt 금지(라디오 auto-ACK) |

→ 보드 전체 핀맵·빈자리: [[uto_nbk_52]]

## 확인 필요 (사용자 호명 대기)

추론 금지 — 아래는 보드 자료를 보고 채운다:

1. ✓ (2026-06-01 해소) **P0.17 중복**: 02_RX_ble·03_TX_ble가 **별개 커스텀보드 2대**([[schematic_ble_module_board_v01e00]], UTO-NBL-52 기반 — DK/PCA10040 아님; FICR DEVICEID 02=`0x5FE168DA`/03=`0xE9775EC9`) → 핀번호 겹침은 충돌 아님. 위 ESB 표 주석 참조.
2. **01_RX_control 추가 디지털 신호 핀번호** (미정): FAULT_RST / LATCH_FAULT / nSYS_RDY / DBG_LED1·2·3 / TEST_MODE1·2 / LSG1·2 — **사용자 확인(2026-06-01): 아직 핀 미정**. 확정 시 [[schematic_rx_regulator_control_board]] 넷리스트/좌표 또는 사용자 호명으로 채움.
3. ✓ (2026-06-01) **기대값**: 현 단계는 위 표의 "~" 근사치로 충분 (사용자 확인). PRD 목표값/실측 확정 시 갱신.

---

## 백링크

장비 [[instruments]] · 보드 [[rx_control]] / [[rx_ble_module]] / [[tx_ble_module]] · 측정 [[esb_timing_measurements]] / [[spi_link_reliability]] · 주변 [[pwm_system]] / [[trip_zone]] / [[adc_channel_map]]
