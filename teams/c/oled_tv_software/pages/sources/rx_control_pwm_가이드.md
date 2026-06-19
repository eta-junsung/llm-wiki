---
tags: [source, pwm, rx_control]
source: projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md
date: 2026-04-14
subsystem: 01_RX_control
---

# RX_control PWM 개발 가이드 (소스)

`01_RX_control` 서브시스템의 PWM 시스템 사용 매뉴얼. API·UART 명령·HW 검증 절차·주의사항을 한 문서에 담은 1차 자료.

원본: `raw/RX_control_PWM_가이드.md`

---

## 한 줄 요약

STM32F103RCT6의 TIM8(PWM1)과 TIM3(PWM2)을 64MHz·100kHz·120도 위상차로 운용하는 [[pwm_system]]. Dead time은 TIM3에 BDTR이 없어 두 타이머 모두 SW CCR offset 방식([[dead_time]])으로 통일한다.

## 파생 페이지

- 보드/페리: [[rx_control]], [[tim8]], [[tim3]]
- 개념: [[pwm_system]], [[dead_time]], [[trip_zone]], [[uart_command_set]]

## 노출 API

| 함수 | 용도 | 관련 페이지 |
|---|---|---|
| `pwm_init()` | 부팅 시 1회. PWM1 시작 → 3us → PWM2 시작 (120도) | [[pwm_system]] |
| `set_duty(ch, duty_pct)` | 단순 CCR 변경 (dead time 미적용) | [[pwm_system]] |
| `pwm_set_freq(freq_hz)` | PWM1·PWM2 동시 주파수 변경 + 120도 재동기 | [[pwm_system]] |
| `pwm_set_deadtime(ch, ns, duty)` | SW CCR offset 방식 dead time 적용 | [[dead_time]] |
| `HAL_TIMEx_BreakCallback()` | BKIN(PA6) HIGH 시 자동 호출, PWM 전체 차단 | [[trip_zone]] |

## UART 명령 ([[uart_command_set]])

115200bps. `duty`, `freq`, `dt`, `reset` — 자세한 인자는 해당 페이지 참조.

## HW 검증 순서

원본 §4. set_duty → set_freq → set_deadtime → Trip Zone 순. 각 개념 페이지의 "검증" 절에 분산 기록.

## 주의사항 (원본 §5 요약)

- **TIM3 HW dead time 불가** — BDTR 없음 → SW 방식으로 통일 ([[dead_time]], [[tim3]])
- **`set_duty()` vs `pwm_set_deadtime()`** — 전자는 dead time 미적용. dead time이 필요하면 후자를 호출 ([[pwm_system]])
- **`ADC_BUCK_VOUT_R128`** — DNP(미실장). `common.h`에서 주석 처리. 사용 금지
- **`pwm_set_freq()` 후 dead time 재호출 필요** — ARR 변경되므로 ([[dead_time]])
