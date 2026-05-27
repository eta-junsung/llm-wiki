---
tags: [entity, board, rx_control]
source: projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md
date: 2026-04-14
subsystem: 01_RX_control
---

# rx_control 보드

OLED TV 전력 변환 제어 보드. `01_RX_control` 서브프로젝트가 동작하는 타겟.

## MCU

- **STM32F103RCT6** (64핀 LQFP)
- SYSCLK 64MHz
- 빌드: CMake + VSCode / STM32CubeIDE

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
- 내부 SPI 프레임: [[spi_packet_format]] (56B/45B, HDR 0xC0, 20ms) — ESB wire 포맷([[esb_packet_format]], 11B)과 별개. nRF가 능동 변환.
- ESB 페이로드 사양: [[tx_to_rx_packets]], [[rx_to_tx_packets]]
- 통신 헬스체크: [[comm_state_monitoring]]

## 알려진 주의

- **`ADC_BUCK_VOUT_R128`** — DNP(미실장). `common.h`에서 주석 처리됨. 실수로 사용 금지.

## 출처

- [[rx_control_pwm_가이드]] (sources)
