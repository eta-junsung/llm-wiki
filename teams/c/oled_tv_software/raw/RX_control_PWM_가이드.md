# RX Control PWM 개발 가이드

> 대상 보드: RX_control (STM32F103RCT6)  
> 작성일: 2026-04-14

---

## 1. 시스템 구성

```
TIM8 (Advanced Timer) — PWM1
  CH1 → PWM1_P (PC6)
  CH2 → PWM1_N (PC7)
  BKIN → Trip zone 입력 (PA6, active high)

TIM3 (General Purpose Timer) — PWM2
  CH3 → PWM2_P (PC8)
  CH4 → PWM2_N (PC9)
```

- 클럭: SYSCLK 64MHz, TIM8/TIM3 모두 64MHz
- 기본 주파수: 100kHz (PSC=0, ARR=639)
- PWM1 → PWM2 위상 지연: 120도

---

## 2. PWM API

### 2-1. `pwm_init()`

```c
void pwm_init(void);
```

부팅 시 1회 호출. PWM1 시작 → 3us 지연 → PWM2 시작 (120도 위상).

---

### 2-2. `set_duty()`

```c
void set_duty(PWM_Type_t ch, uint32_t duty_pct);
```

| 인자 | 설명 |
|------|------|
| `ch` | `PWM1_P(0)` / `PWM1_N(1)` / `PWM2_P(2)` / `PWM2_N(3)` |
| `duty_pct` | 듀티비 [0~100]. 100 초과 시 50으로 클리핑 |

**주의:** Dead time 미적용. Dead time이 필요하면 `pwm_set_deadtime()` 사용.

---

### 2-3. `pwm_set_freq()`

```c
uint32_t pwm_set_freq(uint32_t freq_hz);
```

PWM1(TIM8), PWM2(TIM3) 주파수를 **동시에** 변경한다.  
현재 듀티비를 유지하고, 변경 후 120도 위상을 재동기한다.

| 인자 | 설명 |
|------|------|
| `freq_hz` | 목표 주파수 [Hz] (1 ~ 500000) |
| 반환값 | 실제 설정된 주파수 [Hz], 범위 초과 시 0 |

```c
// 예시
pwm_set_freq(100000);   // 100kHz
pwm_set_freq(50000);    // 50kHz
```

---

### 2-4. `pwm_set_deadtime()`

```c
uint32_t pwm_set_deadtime(PWM_Type_t pwm_ch, uint32_t deadtime_ns, uint32_t duty_pct);
```

SW CCR offset 방식으로 Dead time을 적용한다.  
TIM8(PWM1), TIM3(PWM2) **모두 동일한 SW 방식** 사용.

**SW CCR offset 원리:**
```
P상 CCR = base_ccr + dt_counts/2  → 늦게 켜짐
N상 CCR = base_ccr - dt_counts/2  → 일찍 꺼짐
```

| 인자 | 설명 |
|------|------|
| `pwm_ch` | `PWM1_P(0)` → TIM8,  `PWM2_P(2)` → TIM3 |
| `deadtime_ns` | 설정할 Dead time [ns] |
| `duty_pct` | 현재 적용할 듀티비 [0~100] |
| 반환값 | 실제 설정된 Dead time [ns] |

```c
// 예시
pwm_set_deadtime(PWM1_P, 400, 50);   // PWM1, dead time 400ns, duty 50%
pwm_set_deadtime(PWM2_P, 400, 50);   // PWM2, dead time 400ns, duty 50%
```

---

### 2-5. Trip Zone

TIM8 BKIN 핀(PA6) active high 입력 시 `HAL_TIMEx_BreakCallback()` 자동 호출.  
PWM1, PWM2 전체 출력 즉시 차단.

---

## 3. UART 명령어 (115200bps)

터미널(PuTTY 등)에서 명령 입력 후 `Enter`.

| 명령 | 예시 | 동작 |
|------|------|------|
| `duty <ch> <pct>` | `duty 0 50` | PWM1_P 듀티 50% |
| `freq <hz>` | `freq 100000` | PWM1+PWM2 동시 100kHz |
| `dt <ch> <ns> <pct>` | `dt 0 400 50` | PWM1 dead time 400ns, duty 50% |
| `reset` | `reset` | MCU 소프트 리셋 |

ch 번호: `0`=PWM1_P, `1`=PWM1_N, `2`=PWM2_P, `3`=PWM2_N  
명령어를 모를 때 아무 문자나 입력하면 사용법이 출력됨.

---

## 4. 하드웨어 검증 순서

### Step 1 — set_duty 검증

```
duty 0 50    → PWM1_P 50% 확인 (오실로스코프)
duty 0 30    → PWM1_P 30% 변화 확인
duty 2 50    → PWM2_P 50% 확인
```

### Step 2 — set_freq 검증

```
freq 100000  → 100kHz 기준 (PSC=0, ARR=639)
freq 50000   → 50kHz, 주기 2배 확인
freq 200000  → 200kHz, 주기 절반 확인
freq 100000  → 복귀, 위상 120도 유지 확인
```

### Step 3 — set_deadtime 검증

```
dt 0 400 50  → PWM1 dead time 400ns, P/N 간 측정
dt 0 200 50  → 200ns, 줄어드는지 확인
dt 0 800 50  → 800ns, 늘어나는지 확인
dt 2 400 50  → PWM2 동일하게 확인
dt 0 400 50  → 400ns 복귀
```

### Step 4 — Trip Zone 검증

PA6(BKIN)에 HIGH 인가 → PWM 전체 출력 차단 확인  
UART 로그: `HAL_TIMEx_BreakCallback()` 출력 확인

---

## 5. 알려진 주의사항

| 항목 | 내용 |
|------|------|
| TIM3 HW Dead time | TIM3는 General Timer라 BDTR 레지스터 없음. SW CCR offset 방식만 사용 가능 |
| set_duty vs set_deadtime | `set_duty()`는 Dead time 미적용 단순 CCR 변경. Dead time 필요 시 반드시 `pwm_set_deadtime()` 사용 |
| ADC_BUCK_VOUT_R128 | DNP(미실장). common.h에서 주석 처리됨. 실수로 사용하지 않도록 주의 |
| pwm_set_freq 후 deadtime | 주파수 변경 시 ARR이 바뀌므로 이후 `pwm_set_deadtime()` 재호출 필요 |
