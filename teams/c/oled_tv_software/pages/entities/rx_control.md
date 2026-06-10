---
tags: [entity, board, rx_control]
source: projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md
date: 2026-06-09
subsystem: 01_RX_control
---

# rx_control 보드

OLED TV 전력 변환 제어 보드. `01_RX_control` 서브프로젝트가 동작하는 타겟.

## MCU

- **STM32F103RCT6** (64핀 LQFP)
- SYSCLK 64MHz
- 빌드: CMake + VSCode / STM32CubeIDE. float printf/scanf는 newlib-nano 플래그 선결 → [[cubeide_newlib_nano_float]].

## 메인 루프

`Core/Src/main.c:126-130`의 실제 `while(1)`은 **2개 호출** (커밋 `9be1a7a`에서 SPI 프로토콜 계층을 `app_protocol`로 적출하며 정리):

```c
while (1) {
    adc_proc();        // ADC 6채널 시퀀스 처리
    protocol_loop();   // SPI 송수신 + UART 바이너리 모니터 송출(1초) (app_protocol)
}
```

- **`protocol_loop()`** = `app_protocol.c`의 공개 진입점. 내부 static `exchange_packets()`(수신 파싱 + 10ms 주기 송신) + `print_packets()`(1초 `MONITOR_INTERVAL_MS` UART 모니터 송출)로 분리. **`35b94d0`: `print_packets()`가 11B 바이너리 패킷을 `uart_send()`로 송출**(구 텍스트 모니터·`print_comm_line_on_change` 삭제). 구 `spi_proc()`/`Monitor_Loop()`을 통합·대체. 적출·핸드오프 설계는 [[app_protocol_module]], 모니터 바이너리 전환은 [[comm_state_monitoring]], host 파싱은 [[pc_uart_gui]].
- **모니터 출력은 이제 상시 ON** — 구 `Monitor_Loop()` 주석처리(`175a8f7`) 이슈는 `print_packets()`로 흡수돼 **해소**.
- **UART 커맨드 파싱·실행은 이 루프에 없다** — 인터럽트(ISR) 컨텍스트에서 직접 처리되어 main loop를 선점한다. → [[uart_command_set#수신·파싱-메커니즘]]

> **문서 교정 후보 (코드 repo `CLAUDE.md` 낡음)**: ① main loop를 `LED_Loop/SPI_Loop/ESB_Loop/Monitor_Loop` 4종 polling으로 기술하나 그건 nRF52 펌웨어(02/03) 묘사 — 01 실제 루프는 위 2개. ② 패킷 크기 `tx_module_data_t 45B / rx_module_data_t 56B`도 낡음 → 실제 **43B/54B**(static_assert, [[spi_packet_format]]). **코드가 정본.**

## PWM 채널 매핑

| 신호 | 타이머/채널 | 핀 |
|---|---|---|
| PWM1_P | [[tim8]] CH1 | PC6 |
| PWM1_N | [[tim8]] CH2 | PC7 |
| PWM2_P | [[tim3]] CH3 | PC8 |
| PWM2_N | [[tim3]] CH4 | PC9 |
| BKIN (Trip Zone) | [[tim8]] BKIN | PA6 (active high) |

PWM 시스템 전반은 [[pwm_system]]. 트립존 동작은 [[trip_zone]].

## UART5

| 항목 | 값 |
|---|---|
| Baud Rate | 115200 / 8N1 |
| TX Pin | PC12 |
| RX Pin | PD2 |

- 명령어 셋(host→01): [[uart_command_set]]. 라인 단위 ISR 파싱·prefix 매칭.
- **모니터 출력(01→host)은 `35b94d0`부터 11B 바이너리 패킷**(`print_packets`→`uart_send`). command 응답 printf(`buck=.. V` 등)는 텍스트로 남아 한 포트에 섞여 나감 — host([[pc_uart_gui]])가 HDR 동기+CRC로 분리. 상세 [[comm_state_monitoring]] "monitor 바이너리 전환".

명령어 셋: [[uart_command_set]]

## ADC

- 페리: **ADC1**, 6채널 scan + continuous + DMA1_Channel1 circular
- 입력: 0 ~ 3.3 V (Vref+), 12-bit (0..4095)
- 변환: `adc_conv() = adc_raw/4095 * 3.3f` (raw → 핀 전압 V)
- 버퍼: `rx_adc_raw_data_t sensing_data` (uint16 × 6, `_shared/oled_tv_protocol.h:140-148`)
- 컴플리트 플래그: `adc_conv_complete` (콜백에서 토글, 전 6채널 시퀀스 단위)
- 채널·핀 매핑·라벨 swap 함정은 [[adc_channel_map]] 참조.

## SPI (무선모듈과의 통신)

- 페리: **SPI2**, Master, Full-Duplex (2LINES), 8-bit, MSB first
- 9.0 Mbps (`BaudRatePrescaler=/4`, PCLK1=36 MHz 기준)
- **SPI mode 2**: `CLKPolarity=HIGH` + `CLKPhase=1EDGE` → CPOL=1, CPHA=0. nRF 슬레이브 `NRF_SPIS_MODE_2`와 정합.
- `NSS = SPI_NSS_SOFT` → CS는 GPIO(PB12)로 SW 토글
- DMA: TX = DMA1_Channel5 (MEM→PERIPH), RX = DMA1_Channel4 (PERIPH→MEM), byte 단위 NORMAL

### 핀맵 (STM32F103RCT6)

| 신호 | 핀 | 라벨 / 설정 |
|---|---|---|
| SPI nCS | **PB12** | `SPI_nCS` — GPIO_Output, Pull-up, init=HIGH (SW 제어) |
| SPI SCK | **PB13** | `SPI_CLK` — SPI2_SCK (AF) |
| SPI MISO | **PB14** | `SPI_MISO` — SPI2_MISO (AF), Pull-up |
| SPI MOSI | **PB15** | `SPI_MOSI` — SPI2_MOSI (AF) |

상대 보드 nRF 측 GPIO 및 STM32↔nRF 실물 배선은 [[schematic_stm32_mini_pro_v10]], [[rx_ble_module]] 참조.

- 페어: [[rx_ble_module]] (nRF52832 SPIS1, `02_RX_ble`)
- 내부 SPI wire: [[spi_packet_format]] — **11B 고정 패킷**(HDR 0x10–12/0x50–52, 10ms 주기), ESB wire([[esb_packet_format]])와 **동일 구조** — nRF가 SPI↔ESB 중계. 내부 데이터 컨테이너 `rx_module_data_t` 54B / `tx_module_data_t` 43B는 wire 아님(11B로 직렬화). (구 "56B/45B·HDR 0xC0·20ms" 표기는 드리프트·정정)
- ESB 페이로드 사양: [[tx_to_rx_packets]], [[rx_to_tx_packets]]
- 통신 헬스체크: [[comm_state_monitoring]]

## CAN 버스

| 항목 | 값 |
|---|---|
| TX Pin | PA12 (CAN_TX) |
| RX Pin | PA11 (CAN_RX) |
| 커넥터 신호 | CANA_H_CN / CANA_L_CN (CAN 트랜시버 후 차동 출력) |

## DAC

| 신호 | 핀 | 용도 |
|---|---|---|
| DACA_OUT_uC | PA4 (DAC_OUT1) | 미확인 |
| DACB_OUT_uC | PA5 (DAC_OUT2) | 미확인 |

## 추가 디지털 신호 (GPIO 미확인)

| 신호 | 방향 추정 | 비고 |
|---|---|---|
| FAULT_RST_uC / _CN | 입력 | 폴트 리셋 |
| LATCH_FAULT_uC / _CN | 출력 | 래치 폴트 |
| nSYS_RDY_uC / _CN | 출력 | 시스템 준비 (active low) |
| DBG_LED1/2/3_uC | 출력 | 디버그 LED |
| TEST_MODE1/2_uC | 입력 | 테스트 모드 선택 |
| LSG1/2_OP_SEL_uC / _CN | 출력 | Load Sharing Gate 동작 선택 |

정확한 GPIO 핀 번호는 넷리스트 또는 좌표 분석 필요. [[schematic_rx_regulator_control_board]] 참조.

## 알려진 주의

- **`ADC_BUCK_VOUT_R128`** — DNP(미실장). `common.h`에서 주석 처리됨. 실수로 사용 금지.
- OrCAD 라이브러리 파트명 `STM32F042C6T6`는 오기 — 실제 칩은 STM32F103VCT6 계열.

## 출처

- [[rx_control_pwm_가이드]] (sources)
- [[schematic_rx_regulator_control_board]] (sources) — 전체 핀맵·신호 인벤토리
