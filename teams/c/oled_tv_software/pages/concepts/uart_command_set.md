---
tags: [concept, uart, command, rx_control]
source: teams/c/oled_tv_software/pages/sources/uart_cmd_reference_테스트용.md
date: 2026-05-27
subsystem: 01_RX_control
---

# UART 명령어 셋

[[rx_control]] 보드의 UART5 디버그 명령. 터미널에서 명령 입력 후 Enter.

## 설정

| 항목 | 값 |
|---|---|
| 포트 | UART5 |
| Baud Rate | 115200 |
| Format | 8N1 |
| TX Pin | PC12 |
| RX Pin | PD2 |

## 채널 번호 (PWM 공통)

| ch | 이름 | 타이머 | 역할 |
|---|---|---|---|
| 0 | PWM1_P | TIM8 CH1 | High-side |
| 1 | PWM1_N | TIM8 CH2 | Low-side |
| 2 | PWM2_P | TIM3 CH3 | High-side |
| 3 | PWM2_N | TIM3 CH4 | Low-side |

## 명령어

### `duty` — PWM 듀티비 설정

**형식 A (동시 설정):** `duty <pct>`
- PWM1(TIM8) + PWM2(TIM3) 동시 설정
- `pct`: 0~100 [%]
- 예: `duty 50`

**형식 B (개별 채널):** `duty <ch> <pct>`
- `ch`: 0~3
- 예: `duty 0 50`, `duty 2 45`

> P 채널 설정 시 N 채널은 데드타임을 적용해 pair로 자동 갱신됨.

---

### `freq` — PWM 주파수 설정

**형식:** `freq <hz>`
- `hz`: 1~500,000 [Hz]
- TIM8 + TIM3 주파수 동시 변경
- 데드타임 ns값 고정 → [[dead_time#dt_ratio|dt_ratio]] 자동 재계산 (3~5% 클램프)
- 듀티비 유지, 위상 자동 재동기 (current_phase_deg 유지)
- 예: `freq 100000` → `freq actual=100000 Hz, dt=4.0%`

---

### `dt` — 데드타임 설정

**형식:** `dt <ch> <ns>`
- `ch`: 0=PWM1_P/N(TIM8), 2=PWM2_P/N(TIM3)
- `ns`: 데드타임 [nanoseconds]
- SW CCR offset 방식 (→ [[dead_time]])
- 예: `dt 0 400` → `dt ch=0 actual=400 ns`

> `dt` 명령 후 `freq` 실행 시 dt_ratio 3~5% 클램프 적용됨.

---

### `phase` — 위상차 설정

**형식 A (전체):** `phase <deg>`
**형식 B (단축):** `p<deg>`
- `deg`: 0~360 [degree]
- PWM2가 PWM1 대비 지정 각도만큼 지연
- 예: `phase 120`, `p120`, `p0`

---

### `start` — PWM 출력 시작

**형식:** `start`
- 4채널 동시 출력 시작
- current_phase_deg 자동 적용
- BLE rx_buck_en=CONV_START 수신 시 자동 호출

---

### `reset` — 시스템 리셋

**형식:** `reset`
- `NVIC_SystemReset()` 호출 → MCU 소프트웨어 재부팅
- UART5 명령 또는 BLE fault_reset=RESET_REQ 로 트리거 가능

---

## TIM8_BRK 과전류 보호

- 핀: PA6 (PWM_TZ, active high)
- 트립 시 4채널 자동 OFF
- 복귀: `reset` 명령 또는 BLE fault_reset 토글

자세한 동작: [[trip_zone]]

## 관련 페이지

- [[pwm_system]] — PWM 시스템 구성
- [[dead_time]] — SW CCR offset 방식 + dt_ratio 개념

## 출처

- [[uart_cmd_reference_테스트용]] (sources)
