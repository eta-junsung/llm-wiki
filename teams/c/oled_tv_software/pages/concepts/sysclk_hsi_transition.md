---
tags: [concept, clock, rx_control, hsi]
source: OLED_TV_Rx_Module/Core/Src/main.c SystemClock_Config (2026-06-15 실보드 확인) — ⚠️ 01_RX_control 디렉토리는 HSE 구본일 수 있음, HSI 정본은 OLED_TV_Rx_Module
date: 2026-06-15
subsystem: 01_RX_control, 04_tx_control
---

# SYSCLK HSI 전환 (64 MHz)

[[rx_control]] 보드(STM32F103RCT6)의 클럭 소스를 **HSE → HSI**로 전환한 경위와 확정 클럭 트리.

## 배경 — HSE 발진 실패

회로도 p.2 회로([[schematic_rx_regulator_control_board]] "OSC Clock (8MHz)")에 8 MHz 수동 Pierce 크리스탈(X1) + 부하 커패시터(C2/C3 22pF) + 피드백 저항(R10 1MΩ)이 실장돼 있으나, 실보드에서 **HSERDY 100ms 타임아웃**으로 발진 실패 확인. 부팅이 `SystemClock_Config`의 `Error_Handler` 무한루프에 걸렸다.

- 원인은 HW 이슈(크리스탈 실장/부품값/레이아웃 불일치)로 추정.
- 펌웨어/회로도 정합 문제 아님 — RCC 설정(`RCC_HSE_ON`) 자체는 수동 Pierce 회로에 맞음.
- **해결책**: 내부 RC 오실레이터(HSI) 기반 경로로 전환.

## HSI 경로 제약

`HSI(8 MHz) / 2 × PLL×16 = SYSCLK 64 MHz`

- HSI는 분주 고정(HSI/2 = 4 MHz PLL 입력)
- PLL 체배 최대 ×16 → **SYSCLK 최대 64 MHz**
- **72 MHz는 HSI 경로에서 물리적으로 불가** (HSI/2=4 MHz × max 16 = 64 MHz 상한)

## 확정 클럭 트리

| 레벨 | 경로 | 값 |
|---|---|---|
| SYSCLK | HSI/2 × PLL×16 | **64 MHz** |
| HCLK (AHB) | SYSCLK / 1 | 64 MHz |
| PCLK1 (APB1) | HCLK / 2 | 32 MHz |
| PCLK2 (APB2) | HCLK / 2 | 32 MHz |
| APB1 타이머 클럭 | PCLK1 × 2 (분주≠1) | 64 MHz |
| APB2 타이머 클럭 | PCLK2 × 2 (분주≠1) | 64 MHz |
| ADCCLK | PCLK2 / 4 | 8 MHz |
| Flash latency | — | 2 wait states (64 MHz 범위) |

## 페리퍼럴 영향

### SPI2 속도 (APB1 기반)

- APB1: 36 → 32 MHz (구 72MHz HSE 기준 vs 현 64MHz HSI 기준)
- `BaudRatePrescaler = /4` → **SCLK = 32 / 4 = 8 Mbps** (정본 코드베이스)
- 구 dev 코드베이스는 revert 이후 prescaler=/8 → 4 Mbps.
- 프로토콜 매뉴얼 "9 Mbps 목표"와 여전히 미달 — 목표 유효성 미확정. → [[spi_link_reliability]] 미달 절

### CAN 비트레이트 (확인 필요)

APB1 36 → 32 MHz 변경으로 동일 prescaler/BS1/BS2 조합의 비트레이트가 달라짐. 설계 목표 비트레이트(500 kbps 등)를 64 MHz 기준 PCLK1=32 MHz로 재계산·실측 확인 필요.

### UART5 (영향 없음)

HAL이 PCLK 기준 BRR 자동계산 → 115200 baud 유지. 영향 없음.

### PWM 타이머 (영향 없음)

TIM8(APB2)/TIM3(APB1) 모두 분주≠1 → 타이머 클럭 = 2 × PCLK = 64 MHz 그대로. `PSC=0, ARR=639` → 100 kHz 유지. → [[pwm_system]]

## 검증 상태

- 2026-06-15: 정본 코드베이스 STM32CubeIDE 2.1.1 Debug 빌드 통과, 실보드 flash 완료.
- UART 링크·ESB 실측은 진행 예정(미완).

## 관련

- [[rx_control]] — STM32 entity (SPI 속도·CAN 비트레이트 기술)
- [[schematic_rx_regulator_control_board]] — HSE Pierce 회로도 (OSC Clock 절)
- [[pwm_system]] — 타이머 64 MHz 기반 PWM
- [[spi_link_reliability]] — SPI 속도 미달 현황
