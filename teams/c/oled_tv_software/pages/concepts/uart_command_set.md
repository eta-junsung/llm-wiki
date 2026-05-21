---
tags: [concept, uart, command, rx_control]
source: projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md
date: 2026-04-14
subsystem: 01_RX_control
---

# UART 명령어 셋

[[rx_control]] 보드의 UART 디버그 명령. PuTTY 등 터미널에서 명령 입력 후 `Enter`.

## 설정

- 115200 bps

## 채널 번호

`0`=PWM1_P, `1`=PWM1_N, `2`=PWM2_P, `3`=PWM2_N

## 명령

| 명령 | 예시 | 동작 | 관련 |
|---|---|---|---|
| `duty <ch> <pct>` | `duty 0 50` | PWM1_P 듀티 50% | [[pwm_system]] |
| `freq <hz>` | `freq 100000` | PWM1+PWM2 동시 주파수 변경 | [[pwm_system]] |
| `dt <ch> <ns> <pct>` | `dt 0 400 50` | PWM1 dead time 400ns, duty 50% | [[dead_time]] |
| `reset` | `reset` | MCU 소프트 리셋 | — |

명령어를 모를 때 아무 문자나 입력하면 사용법이 출력된다.

## 출처

- [[rx_control_pwm_가이드]] (sources)
