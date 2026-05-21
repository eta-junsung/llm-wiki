---
tags: [entity, peripheral, timer, rx_control]
source: projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md
date: 2026-04-14
subsystem: 01_RX_control
---

# TIM3

[[rx_control]] 상의 STM32F103 **General Purpose Timer**. PWM2 생성에 사용.

## 클럭·기본 설정

- 클럭: 64MHz
- 기본 주파수: 100kHz → PSC=0, ARR=639
- 위상: [[tim8]] 대비 120도 지연 시작 (3us)

## 채널·핀

| 채널 | 신호 | 핀 |
|---|---|---|
| CH3 | PWM2_P | PC8 |
| CH4 | PWM2_N | PC9 |

## 제약

- **BDTR 레지스터 없음** — General Timer라 HW Dead time 불가. → 시스템 전체가 SW CCR offset 방식으로 통일됨 ([[dead_time]]).
- **Trip Zone 없음** — Trip 차단은 [[tim8]] BKIN 콜백에서 PWM2까지 함께 꺼주는 방식 ([[trip_zone]]).

## 역할

- **PWM2 생성** — [[pwm_system]]의 두 번째 PWM 채널. [[tim8]](PWM1) 시작 3us 뒤 `pwm_init()`에서 함께 켜진다.
- **Dead time** — [[dead_time]]의 SW CCR offset 방식 적용 (BDTR 없으므로 SW만 가능).
- **Trip Zone** — 자체 입력 없음. [[tim8]] BKIN 콜백에서 PWM2까지 함께 차단 ([[trip_zone]]).

## 출처

- [[rx_control_pwm_가이드]] (sources)
