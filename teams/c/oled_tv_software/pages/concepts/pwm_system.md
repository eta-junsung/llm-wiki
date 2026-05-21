---
tags: [concept, pwm, rx_control]
source: projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md
date: 2026-04-14
subsystem: 01_RX_control
---

# PWM 시스템

[[rx_control]] 보드의 PWM 출력 시스템. [[tim8]] → PWM1, [[tim3]] → PWM2를 120도 위상차로 운용.

## 구성

```
TIM8 (Advanced)  PWM1   CH1=PWM1_P(PC6)  CH2=PWM1_N(PC7)  BKIN=PA6
TIM3 (General)   PWM2   CH3=PWM2_P(PC8)  CH4=PWM2_N(PC9)
```

- 두 타이머 모두 64MHz·100kHz(PSC=0, ARR=639) 기본
- PWM1 → PWM2 위상 지연: 120도 (= 100kHz 기준 3us)

채널 번호 매핑: `PWM1_P=0`, `PWM1_N=1`, `PWM2_P=2`, `PWM2_N=3`.

## API

### `pwm_init()`

부팅 시 1회. PWM1 시작 → 3us 지연 → PWM2 시작 (120도 위상).

### `set_duty(ch, duty_pct)`

```c
void set_duty(PWM_Type_t ch, uint32_t duty_pct);
```

| 인자 | 설명 |
|---|---|
| `ch` | `PWM1_P(0)` / `PWM1_N(1)` / `PWM2_P(2)` / `PWM2_N(3)` |
| `duty_pct` | 듀티비 [0~100]. **100 초과 시 50으로 클리핑** |

**Dead time 미적용**. 단순 CCR 변경. Dead time이 필요하면 [[dead_time]]의 `pwm_set_deadtime()` 사용.

### `pwm_set_freq(freq_hz)`

```c
uint32_t pwm_set_freq(uint32_t freq_hz);   // 반환: 실제 설정된 Hz, 범위 초과 시 0
```

- 범위: 1 ~ 500000 Hz
- PWM1·PWM2 **동시** 변경
- 현재 듀티비 유지, 변경 후 120도 위상 재동기
- **주의:** ARR이 바뀌므로, 사용 중이라면 직후 `pwm_set_deadtime()` 재호출 필요 ([[dead_time]])

## 검증 (원본 §4 Step 1·2)

### set_duty

```
duty 0 50    → PWM1_P 50% 확인
duty 0 30    → 30% 변화 확인
duty 2 50    → PWM2_P 50% 확인
```

### set_freq

```
freq 100000  → 100kHz 기준 (PSC=0, ARR=639)
freq 50000   → 주기 2배
freq 200000  → 주기 절반
freq 100000  → 복귀, 위상 120도 유지
```

UART 명령 자체는 [[uart_command_set]].

## 출처

- [[rx_control_pwm_가이드]] (sources)
