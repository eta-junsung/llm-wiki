---
tags: [concept, pwm, trip_zone, rx_control]
source: projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md
date: 2026-04-14
subsystem: 01_RX_control
---

# Trip Zone

[[pwm_system]]의 HW 보호 메커니즘. 외부 신호로 PWM 전체 출력을 즉시 차단.

## 동작

- 입력: [[tim8]] BKIN 핀 = **PA6, active high**
- HIGH 인가 시: `HAL_TIMEx_BreakCallback()` 자동 호출 → [[tim8]] PWM1 + [[tim3]] PWM2 전체 출력 차단
- ([[tim3]]는 자체 BKIN이 없으므로, [[tim8]] 콜백 안에서 같이 꺼주는 구조)

## 검증 (원본 §4 Step 4)

1. PA6(BKIN)에 HIGH 인가
2. PWM 전체 출력 차단 확인 (오실로스코프)
3. UART 로그에 `HAL_TIMEx_BreakCallback()` 출력 확인

## 출처

- [[rx_control_pwm_가이드]] (sources)
