---
tags: [concept, uart, command, rx_control]
source: teams/c/oled_tv_software/pages/sources/uart_cmd_reference_테스트용.md
date: 2026-05-27
subsystem: 01_RX_control
---

# UART 명령어 셋

[[rx_control]] 보드의 UART5 디버그 명령. 터미널에서 명령 입력 후 Enter.

> **방향 주의 (`35b94d0`·2026-06-16)**: 이 페이지는 **host→01 command 채널**(UART5)을 다룬다. 두 종류가 한 포트에 공존:
> - **텍스트 커맨드** (`duty`/`freq`/`dt`/`phase`/`start`/`stop`/`reset`): 라인 단위·텍스트·ISR 파싱 — **무변경**.
> - **`buck` 지령 (2026-06-16 변경)**: ASCII "`buck <v>\r`" 텍스트가 **제거**되고 host([[pc_uart_gui]])가 **11B 바이너리 0x51 패킷**을 직접 UART5로 전송하는 방식으로 전환. `HAL_UART_RxCpltCallback`에 0x51 바이너리 분기 추가. ([[buck_vout_ref_command_path]])
>
> 반대 방향 **01→host 모니터 출력은 `35b94d0`부터 11B 바이너리 패킷**([[comm_state_monitoring]] "monitor 바이너리 전환", [[pc_uart_gui]]). command 응답 printf는 텍스트로 남아 한 포트(UART5)에 섞임 — TeraTerm 디버그용.

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

### `stop` / `start` — PWM 정지/시작

**형식:** `stop`, `start`
- `stop`: 4채널 출력 정지. `start`: 4채널 동시 출력 시작 (위 `start` 절 참조).

---

### `buck` — **(RF 지령)** Tx Buck 출력 전압 Ref

> ⚠️ **2026-06-16 변경**: ASCII "`buck <v>`" 텍스트 커맨드가 **제거**됐다. host GUI([[pc_uart_gui]])가 **11B 바이너리 0x51 패킷**을 UART5로 직접 전송한다.

- 패킷 포맷: `[HDR=0x51 | LEN=0x08 | DATA[0..5]=0x00 | DATA[6..7]=ref×100 u16 BE | XOR CRC]`
- 01 수신 경로: `HAL_UART_RxCpltCallback` 0x51 분기 → 11B 프레임 수집·CRC 검증 → `pkt_apply_rx_cmd()` → `rx_cmd.tx_buck_vout_ref` (float)
- 공유 함수 `pkt_apply_rx_cmd()` (`_shared/oled_tv_protocol.h/.c`): `pkt_build_rx()`(0x51 인코딩)의 역연산, `pkt_apply_tx()`와 대칭. DATA[6..7] u16 BE ÷100 → `rx_cmd.tx_buck_vout_ref`.
- 이후 경로 불변: `rx_cmd.tx_buck_vout_ref` → `build_rx_pkt()` → 0x51 DATA[6,7] → SPI → 02 → ESB ACK → 03_TX_ble.
- 실보드 검증 완료 (2026-06-16): GUI 입력 → 03 Monitor `Tx_Buck_Vout_Ref` 정상 전파.
- **UART 채널 중 RF 링크 너머 03_TX_ble까지 가는 유일한 지령.** 나머지는 전부 로컬 PWM 제어.
- 전체 경로·패턴: [[buck_vout_ref_command_path]]

---

## 명령어 요약표

| 커맨드 | 동작 |
|---|---|
| `duty <pct>` / `duty <ch> <pct>` | PWM 듀티 (ch: 0=PWM1_P 1=PWM1_N 2=PWM2_P 3=PWM2_N) |
| `freq <hz>` | 주파수, dt_ratio 자동 3~5% 재계산 |
| `dt <ch> <ns>` | 데드타임 (ch 0=TIM8, 2=TIM3) |
| `phase <deg>` / `p<deg>` | 위상차 |
| `start` / `stop` / `reset` | PWM 시작 / 정지 / 시스템 리셋 |
| ~~`buck <v>`~~ | *(2026-06-16 제거)* GUI 바이너리 0x51 패킷으로 대체 — [[buck_vout_ref_command_path]] |

---

## 수신·파싱 메커니즘

소스: `app_usart.c` `HAL_UART_RxCpltCallback`.

### 인터럽트 구동 (폴링 아님)

- `HAL_UART_Receive_IT`로 **1바이트씩** 수신 → `UART5_IRQHandler` → `HAL_UART_RxCpltCallback`(ISR).
- 부팅 시 `uart_init()`(while 루프 진입 **전**)에서 1회 무장. 이후 **콜백이 매 바이트 자기 재무장**한다.
- UART5 IRQ 우선순위 **14**.

### 0x51 바이너리 분기 (2026-06-16 추가)

콜백 진입 시 **텍스트 라인 파싱보다 먼저** 평가되는 0x51 프레임 수집 로직.

- 11B 프레임을 바이트 단위로 수집: HDR(`0x51`) 매칭 → LEN·DATA[8]·CRC 순서대로 버퍼에 누적.
- 11B 완성 시 XOR CRC 검증 → 통과하면 `pkt_apply_rx_cmd()` 호출 → `rx_cmd.tx_buck_vout_ref` 업데이트.
- 검증 실패(CRC 불일치·HDR 불일치) 시 버퍼 리셋 후 재동기.
- **이 분기에서 소비된 바이트는 텍스트 파싱으로 내려가지 않는다.**

### 라인 단위 파싱 (텍스트 커맨드)

- `cmd_buf[64]`에 누적, `\r` / `\n`에서 한 라인 확정. **63자 초과분은 폐기.**
- **커맨드 파싱·실행이 ISR 컨텍스트에서 직접 일어난다** — main loop로 디퍼하지 않음. 즉 엔터를 친 순간 main loop를 선점해 처리한다. (main loop 구성은 [[rx_control#메인-루프]])

### 분기 = else-if `strncmp` prefix 매칭

- 명령 분기는 `else-if strncmp` prefix 매칭 체인. **분기 순서 = 우선순위.**
- prefix 매칭이라 **트레일링 문자는 무시** — `stopXYZ`도 `stop`에 걸린다.
- `phase ` (끝 공백) 형식은 공백이 필수.
- ~~`buck`~~ 분기는 2026-06-16에 **제거**됨 — 위 "0x51 바이너리 분기"로 대체.

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

- [[uart_cmd_reference_테스트용]] (sources) — `duty`/`freq`/`dt`/`phase`/`start`/`reset` 매뉴얼
- 코드 실측 (`app_usart.c`, 사용자 세션 2026-06-05) — `buck` 지령, 수신·파싱 메커니즘(ISR 구동·prefix 매칭)
