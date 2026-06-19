---
tags: [entity, peripheral, timer, rx_control]
source: projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md
date: 2026-04-14
subsystem: 01_RX_control
---

# TIM8

[[rx_control]] 상의 STM32F103 **Advanced Control Timer**. PWM1 생성에 사용.

## 클럭·기본 설정

- 클럭: 64MHz (SYSCLK 그대로)
- 기본 주파수: 100kHz → PSC=0, ARR=639

## 채널·핀

| 채널 | 신호 | 핀 |
|---|---|---|
| CH1 | PWM1_P | PC6 |
| CH2 | PWM1_N | PC7 |
| BKIN | Trip zone 입력 | PA6 (active high) |

## 역할

- **PWM1 생성** — [[pwm_system]] 참조. PWM1이 먼저 시작되고 3us(120도) 뒤 [[tim3]]가 시작된다.
- **Trip Zone** — BKIN HIGH 시 `HAL_TIMEx_BreakCallback()` 자동 호출, PWM 전체 차단. [[trip_zone]] 참조.
- **HW Dead time** — Advanced Timer라 BDTR 보유. 다만 [[tim3]]와의 통일을 위해 SW CCR offset 방식 사용 ([[dead_time]]).

## 출처

- [[rx_control_pwm_가이드]] (sources)
