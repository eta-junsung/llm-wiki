---
tags: [concept, pwm, dead_time, rx_control]
source: projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md
date: 2026-04-14
subsystem: 01_RX_control
---

# Dead time (SW CCR offset)

[[pwm_system]]에서 P상·N상 사이 dead time을 만드는 방식. **[[tim8]]·[[tim3]] 모두 SW CCR offset 방식으로 통일**.

## 왜 SW 방식인가

- [[tim8]]은 Advanced Timer라 BDTR로 HW dead time 가능하지만,
- [[tim3]]은 General Timer라 **BDTR이 없어** HW dead time 불가.
- 두 타이머를 동일하게 다루기 위해 시스템 전체가 SW CCR offset 방식으로 통일됨.

## 원리

```
P상 CCR = base_ccr + dt_counts/2   → 늦게 켜짐
N상 CCR = base_ccr - dt_counts/2   → 일찍 꺼짐
```

P/N 양쪽을 절반씩 어긋나게 해서 dead time을 만든다.

## API

```c
uint32_t pwm_set_deadtime(PWM_Type_t pwm_ch, uint32_t deadtime_ns, uint32_t duty_pct);
```

| 인자 | 설명 |
|---|---|
| `pwm_ch` | `PWM1_P(0)` → [[tim8]],  `PWM2_P(2)` → [[tim3]] |
| `deadtime_ns` | 설정할 dead time [ns] |
| `duty_pct` | 현재 적용할 듀티비 [0~100] |
| 반환값 | 실제 설정된 dead time [ns] |

```c
pwm_set_deadtime(PWM1_P, 400, 50);   // PWM1: dt 400ns, duty 50%
pwm_set_deadtime(PWM2_P, 400, 50);   // PWM2: dt 400ns, duty 50%
```

## 주의

- **`set_duty()`는 dead time 미적용** — 단순 CCR 변경이므로 dead time 필요 시 반드시 `pwm_set_deadtime()`을 써야 한다.
- **주파수 변경 후 재호출 필요** — `pwm_set_freq()`가 ARR을 바꾸므로 dt_counts 기준이 흐트러진다. freq 변경 직후 `pwm_set_deadtime()`을 다시 불러줄 것.

## 검증 (원본 §4 Step 3)

```
dt 0 400 50  → PWM1 dead time 400ns, P/N 간 측정
dt 0 200 50  → 200ns 축소 확인
dt 0 800 50  → 800ns 확장 확인
dt 2 400 50  → PWM2도 동일하게 확인
dt 0 400 50  → 400ns 복귀
```

UART 명령은 [[uart_command_set]].

## 출처

- [[rx_control_pwm_가이드]] (sources)
