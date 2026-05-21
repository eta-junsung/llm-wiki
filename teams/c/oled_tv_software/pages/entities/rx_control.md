---
tags: [entity, board, rx_control]
source: projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md
date: 2026-04-14
subsystem: 01_RX_control
---

# rx_control 보드

OLED TV 전력 변환 제어 보드. `01_RX_control` 서브프로젝트가 동작하는 타겟.

## MCU

- **STM32F103RCT6**
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

## UART

- 115200bps
- 명령어 셋: [[uart_command_set]]

## SPI (무선모듈과의 통신)

- Master, 4선, 9.0 Mbps, Motorola byte order
- 페어: [[rx_ble_module]] (현재 BLE, 추후 ESB)
- 패킷 사양: [[spi_packet_format]], [[tx_to_rx_packets]], [[rx_to_tx_packets]]
- 통신 헬스체크: [[comm_state_monitoring]]

## 알려진 주의

- **`ADC_BUCK_VOUT_R128`** — DNP(미실장). `common.h`에서 주석 처리됨. 실수로 사용 금지.

## 출처

- [[rx_control_pwm_가이드]] (sources)
