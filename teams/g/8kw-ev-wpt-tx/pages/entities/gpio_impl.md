---
tags: [entity, gpio, uart5, 8kw-ev-wpt-tx]
source: 펌웨어 repo branch gpio (실보드 검증 2026-06-16). src/eta_bsp/eta_gpio.{c,h}, eta_uart5.{c,h}, tools/gui/gui.py
date: 2026-06-16
---

# gpio_impl — 8kW WPT TX GPIO 출력 구현 상세

LP-AM263P 8kW WPT TX 보드의 GPIO 출력 2핀 구현 및 UART5 양방향 확장 정본.
핀맵 기초는 [[gpio_pinmap]], 프로젝트 현재 위치는 [[status]].

---

## 핀맵 (실보드 검증 완료, 2026-06-16)

| 신호 | GPIO | 커넥터 핀 | 초기값 | 실측 결과 |
|------|------|-----------|--------|-----------|
| 485_EN | 91 | J5.48 | LOW | 10 Hz 펄스 (UART5 DE 자동 토글) 확인 |
| GD_EN_seed | 93 | J4.33 | LOW | HIGH 확인 |

---

## 구현 — `src/eta_bsp/eta_gpio.{c,h}`

### 핀먹스 — PADCONFIG 런타임 mux

`eta_gpio_init()`이 **런타임 직접 PADCONFIG 레지스터**에 `PIN_MODE(7)`(GPIO 모드)를 쓴다. `example.syscfg` 불변 — SysConfig 재생성에 면역.

### TCA6416A U54 PRU_MUX_SEL 헤더 라우팅

**GPIO93(J4.33) 헤더 라우팅에 TCA6416A U54 I2C1(0x20) P07=HIGH 필요.** P07을 HIGH로 쓰지 않으면 J4.33 헤더로 신호가 라우팅되지 않는다.

- I2C 주소: 0x20 (I2C1)
- 레지스터: Output Port 1, bit 7 (P07)
- 값: HIGH = 라우팅 활성

> ⚠️ GPIO91(J5.48)은 별도 보드먹스 없이 직통.

### API

```c
// 공개 (extern in eta_gpio.h)
void eta_gpio_init(void);                      // 양 핀 output 초기화, 초기값 LOW
void eta_gpio_request_gd_en(bool enable);      // GD_EN_seed 요청 enqueue — uart5 RX 파서 호출
void eta_gpio_loop(void);                      // 소비 — main while(1)에서 호출
void eta_gpio_set_485_en(bool enable);         // 485_EN(GPIO91) — TX 타이밍 직결 예외

// 비공개 (eta_gpio.c 내부 static)
// static void eta_gpio_set_gd_en(bool enable);
```

`eta_gpio_set_485_en()`은 UART5 TX 송신 타이밍에 동기로 직접 호출하는 **예외 경로** — DE 토글이라 `eta_gpio_loop()` 경유 시 타이밍이 깨진다.

---

## GPIO 루프 패턴 (ISR→flag→main 소비)

RX 파서가 GPIO를 **직접 구동하지 않는다**. ADC의 `g_eta_adc_ready + eta_adc_loop()` 패턴과 동형:

```
[uart5 RX 파서]
  eta_gpio_request_gd_en(value)   → pending flag + 값 저장

[main while(1)]
  eta_gpio_loop()                 → flag 소비 → GPIO_pinWriteHigh/Low 실행
```

예외: `eta_gpio_set_485_en()`은 `UART_write` 전후에 동기 직접 호출. DE 타이밍은 loop 경유 불가.

> ⚠️ `eta_gpio_set_gd_en()`은 v2부터 **static(비공개)**. 외부에서 직접 호출하지 말 것 — `eta_gpio_request_gd_en()` 경유만 정식 경로.

---

## UART5 양방향 확장

### TX 방향 자동 토글 (485_EN DE)

`eta_uart5.c`의 `UART_write` 래퍼에 DE 토글 삽입:

```
eta_gpio_set_485_en(true)   → UART_write(...)   → eta_gpio_set_485_en(false)
```

RS-485 송신 중에만 DE가 HIGH가 되어 THVD1400 U13을 TX 모드로 전환한다.
**실측**: J5.48에서 10 Hz 펄스(ADC 텔레메트리 10 Hz 주기와 일치) 확인.

### 패킷 확장 — TYPE=0x02 GPIO 상태 TX (MCU→PC, 이벤트 기반)

| 바이트 | 필드 | 값/의미 |
|--------|------|---------|
| [0] | SOF | `0xA5` |
| [1] | LEN | `1` |
| [2] | TYPE | `0x02` |
| [3] | SEQ | `0..255` rolling |
| [4] | GPIO_STATUS | bit0=485_EN, bit1=GD_EN_seed |
| [5..6] | CRC | CRC-16/CCITT-FALSE |

- 총 7B. **이벤트 기반** — `eta_gpio_init()` 직후, `set_gd_en()` 호출 시 자동 송신.
- 정본 [[uart5_packet_protocol]].

### 패킷 확장 — TYPE=0x10 GPIO 커맨드 RX (PC→MCU, fire-and-forget)

| 바이트 | 필드 | 값/의미 |
|--------|------|---------|
| [0] | SOF | `0xA5` |
| [1] | LEN | `2` |
| [2] | TYPE | `0x10` |
| [3] | SEQ | rolling |
| [4] | CMD_ID | `0x01` = GD_EN_seed |
| [5] | VALUE | `0`=LOW / `1`=HIGH |
| [6..7] | CRC | CRC-16/CCITT-FALSE |

- 총 8B. MCU는 수신 후 즉시 `eta_gpio_set_gd_en(VALUE)`를 실행하고 TYPE=0x02 응답 패킷을 반송.
- 정본 [[uart5_packet_protocol]].

---

## PC GUI — GPIO Control 섹션 (`tools/gui/gui.py`)

| 컨트롤 | 대상 | 동작 |
|--------|------|------|
| 상태 라벨 | 485_EN | TYPE=0x02 수신 시 갱신 (읽기 전용) |
| ON/OFF 버튼 + 상태 라벨 | GD_EN_seed | 클릭 시 `send_gpio_cmd()` 호출 → TYPE=0x10 송신 |

`send_gpio_cmd()`: TYPE=0x10 패킷 조립, Lock 포함, CRC-16 적용. 잔여 = 실보드 왕복 검증.

---

## 빌드 시스템 정리

- **CCS IDE `build/` Exclude from Build**: CCS makefile과의 심볼 중복 해소.
- **`flash_node_8kw.js` mcelf 자동 선택**: `Release/` 와 `build/` 두 후보 mcelf의 mtime을 비교해 더 최신을 자동 선택 (콘솔에 어느 쪽이 선택됐는지 출력). 플래시 전 반드시 최신 소스로 빌드 완료 후 실행.
- **`build/makefile FILES_common`**: `eta_gpio.c` 추가.
- **`.theia/launch.json`**: 단일 project-based launch만 유지(중복 제거).

### ⚠️ "Run > Flash Project" 사용 금지

CCS Theia의 **Run > Flash Project**는 SBL(`sbl_ospi_am263p.tiimage`)을 플래시하지 않는다. 전원 사이클 후 standalone 부팅 불가.

올바른 플래시 절차:
1. CCS IDE **완전 종료** (JTAG 백엔드 경합 방지 — [[jtag_flash_clean_host]])
2. `tools/jtag_flash/run_flash_node` 실행 (`ERASE_ALL → SBL@0x00000000 → app@0x00081000` 순서)
3. 전원 사이클

---

## 미확인

- **GD_EN_seed 극성 회로도 미확인**: active-high 가정으로 HIGH 실측 통과 — 가정 실증. 회로도 원본 미확인.
- ~~**GUI 왕복 검증 잔여**~~ — ✅ **완료(2026-06-16)**: GUI GD_EN ON 버튼 → TYPE=0x10 커맨드 → `eta_gpio_request_gd_en()` → `eta_gpio_loop()` → GPIO93(J4.33) HIGH. Logic2 CH0(J4.33) LOW→HIGH 전이 실측 확인. standalone flash 부팅 후 동작 재확인.
