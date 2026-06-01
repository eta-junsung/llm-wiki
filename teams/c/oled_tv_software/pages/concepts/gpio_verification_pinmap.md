---
tags: [concept, gpio, verification, pinmap]
source: 기존 wiki 사실 종합 (rx_control, esb_timing_measurements, spi_link_reliability, adc_channel_map) + conversation-2026-06-01
date: 2026-06-01
subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
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
| SPI 클럭 활성 | **PB13** | SPI2_SCK | 전송 중 SCK 버스트, 9.0 Mbps(`/4`) | [[rx_control]] |
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

## 02_RX_ble / 03_TX_ble (nRF52832, ESB)

| 검증 대상 (기능) | 서브시스템 | 프로브 핀 | 신호명 | 트리거 / 기대값 | 근거 |
|---|---|---|---|---|---|
| ESB TX 전송 주기 | 03_TX_ble | **P0.17** | TX 시작 토글 (측정 전용) | ~920 µs 주기 | [[esb_timing_measurements]] |
| ESB TX→ACK 지연 | 03_TX_ble | P0.17 → **P0.18** | TX 시작 → ACK 수신 | ~470 µs (두 엣지 시간차, 커서) | [[esb_timing_measurements]] |
| ESB ACK 수신 주기 | 03_TX_ble | **P0.18** | ACK 수신 토글 (측정 전용) | ~940 µs 주기 | [[esb_timing_measurements]] |
| SPI heartbeat 200 ms | 02_RX_ble | **P0.17** `PIN_DBG_HB` | heartbeat 디버그 토글 | 200 ms 토글 (Δt≈190 ms 실측) | [[spi_link_reliability]] |

> P0.17/P0.18 토글은 측정 전용 디버그 코드 — 검증 종료 후 제거 여부 결정 대상 ([[tx_ble_module]]).
> **P0.17 중복은 충돌 아님**: 02_RX_ble와 03_TX_ble는 동일 nRF52832 **PCA10040** 모델이지만 **물리적으로 별개 보드 2대**다. 같은 핀번호(P0.17)가 각 보드에서 다른 용도(02=heartbeat `PIN_DBG_HB` / 03=TX 시작 토글)로 쓰이는 것이며, 한 핀의 의미 충돌이 아니다.

---

## 확인 필요 (사용자 호명 대기)

추론 금지 — 아래는 보드 자료를 보고 채운다:

1. ✓ (2026-06-01 해소) **P0.17 중복**: 02_RX_ble·03_TX_ble가 별개 PCA10040 보드 2대 → 핀번호 겹침은 충돌 아님. 위 ESB 표 주석 참조.
2. **01_RX_control 추가 디지털 신호 핀번호** (미정): FAULT_RST / LATCH_FAULT / nSYS_RDY / DBG_LED1·2·3 / TEST_MODE1·2 / LSG1·2 — **사용자 확인(2026-06-01): 아직 핀 미정**. 확정 시 [[schematic_rx_regulator_control_board]] 넷리스트/좌표 또는 사용자 호명으로 채움.
3. ✓ (2026-06-01) **기대값**: 현 단계는 위 표의 "~" 근사치로 충분 (사용자 확인). PRD 목표값/실측 확정 시 갱신.

---

## 백링크

장비 [[instruments]] · 보드 [[rx_control]] / [[rx_ble_module]] / [[tx_ble_module]] · 측정 [[esb_timing_measurements]] / [[spi_link_reliability]] · 주변 [[pwm_system]] / [[trip_zone]] / [[adc_channel_map]]
