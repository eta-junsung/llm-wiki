---
tags: [concept, am263p, iomux, pinmux, padconfig, platform]
source:
  - C:\ti\mcu_plus_sdk_am263px_26_00_00_01\source\drivers\pinmux\am263px\pinmux.h
  - C:\ti\mcu_plus_sdk_am263px_26_00_00_01\source\drivers\pinmux\am263px\pinmux.c
  - C:\ti\mcu_plus_sdk_am263px_26_00_00_01\source\drivers\hw_include\am263px\cslr_iomux.h
  - C:\ti\mcu_plus_sdk_am263px_26_00_00_01\source\drivers\hw_include\am263px\cslr_soc_baseaddress.h
  - C:\Users\echog\eta\projects\g\lp-am263p\evaluations\uart5\empty.c
  - C:\Users\echog\eta\projects\g\8kw-ev-wpt-tx\src\eta_bsp\eta_uart5.c
date: 2026-06-09
---

# AM263P IOMUX PADCONFIG force_io_enable 패턴

> **AM263P 플랫폼 지식 정본.** UART5 사례로 발견했지만 **모든 alt-function 패드에 일반화 가능**. 8kw-ev-wpt-tx·lp-am263p 공용. 형제 정본: [[am263p_adc_rti_trigger]], [[jtag_flash_harness]].

## 한 줄 요약

**SysConfig 핀먹스만으로는 alt-function 패드의 입·출력 버퍼가 안 켜진다.** PADCONFIG의 OE/IE override 필드를 SysConfig는 `00`(IP default)으로 남기고, `Pinmux_config()`는 RMW가 아닌 plain write로 쓰기 때문. KICK 언락 후 PADCONFIG를 직접 RMW해 OE/IE override를 `01`(force-enable)로 OR-set 하는 **force_io_enable**이 필수다. ★ **OE/IE는 active-low가 아니다 — 켜려면 비트를 set, clear가 아님.**

---

## 확정 사실 (코드·헤더 교차검증)

### 1. PADCONFIG OE/IE override는 2비트 필드 (active-low 아님)

| override | 비트 필드 | force-enable (01) | force-disable (11) |
|----------|-----------|-------------------|--------------------|
| OUTPUT enable | **[7:6]** | `PIN_FORCE_OUTPUT_ENABLE = 0x1<<6 = 0x40` | `PIN_FORCE_OUTPUT_DISABLE = 0x3<<6 = 0xC0` |
| INPUT enable | **[5:4]** | `PIN_FORCE_INPUT_ENABLE = 0x1<<4 = 0x10` | `PIN_FORCE_INPUT_DISABLE = 0x3<<4 = 0x30` |

- 값 의미: `01` = force-enable / `11` = force-disable / `00` = IP default (override 안 함).
- 출처: `pinmux.h:93-100`.
- ★ **핵심 함정**: TI 다른 SoC의 OE 직관(0으로 clear하면 출력 ON)과 **반대**다. AM263P는 출력 버퍼를 켜려면 `|= 0x40`(OR-set)이 올바른 방향. `00`(default)·`11`(force-disable) 둘 다 출력이 안 나올 수 있다.

### 2. SysConfig 단독으로는 alt-function 패드 버퍼가 절대 안 켜진다

- SysConfig 생성 핀먹스(`ti_pinmux_config.c`)는 OE/IE override 필드를 **`00`(IP default)으로 남긴다**. 생성 설정값에는 `PIN_MODE`·`PIN_PULL_*`·`PIN_SLEW_RATE_*`만 있고 force 비트가 없다 (`ti_pinmux_config.c:42-51`).
- `Pinmux_config()`는 PADCONFIG를 **RMW가 아니라 plain write**로 쓴다 — `CSL_REG32_WR(regAddr, pinmuxCfg->settings)` (`pinmux.c:94`). 따라서 생성값에 없는 OE/IE 비트는 매번 `00`으로 덮어쓰여진다.
- => **결론**: mux mode를 alt-function(예 UART5)으로 바꿔도, 해당 패드의 IP default가 buffer-disabled면 입·출력이 죽은 채로 남는다. syscfg만으로는 절대 못 켠다. KICK 언락 후 PADCONFIG 직접 RMW(force_io_enable)가 필수.

### 3. force_io_enable 패턴

```
1. IOMUX KICK 언락:  KICK0 ← 0x83E70B13,  KICK1 ← 0x95A4F1E0
2. PADCONFIG RMW:    val = RD(pad); val |= PIN_FORCE_OUTPUT_ENABLE; WR(pad, val)
                     (RX 필요 시: val |= PIN_FORCE_INPUT_ENABLE)
3. IOMUX 재잠금:     KICK0 ← 0x00000000,  KICK1 ← 0x00000000
```

- KICK 매직값 출처: `pinmux.c:56-58` (`IOMUX_KICK0_UNLOCK_VAL`=0x83E70B13, `IOMUX_KICK1_UNLOCK_VAL`=0x95A4F1E0, lock=0).
- **호출 시점**: `Drivers_open()` / `Board_driversOpen()` 이후 (syscfg가 PADCONFIG를 plain-write로 깔아둔 다음에 RMW해야 덮어쓰이지 않음).
- TX 핀 → `|= PIN_FORCE_OUTPUT_ENABLE`. RX 핀 → `|= PIN_FORCE_INPUT_ENABLE` (수신 필요 시에만).
- 일반화: UART뿐 아니라 **SysConfig가 alt-function으로 먹싱하는 모든 패드**에서 출력이 안 나오거나 입력이 안 들어오면 이 패턴을 의심.

### 4. IOMUX 레지스터 좌표 (확정)

| 항목 | 값 | 출처 |
|------|-----|------|
| `CSL_IOMUX_U_BASE` | `0x53100000` | `cslr_soc_baseaddress.h:416` |
| `CSL_IOMUX_IO_CFG_KICK0` (offset) | `0x298` | `cslr_iomux.h:395` |
| `CSL_IOMUX_IO_CFG_KICK1` (offset) | `0x29C` | `cslr_iomux.h:396` |
| `PIN_EPWM15_A` (offset) | `0x124` | `pinmux.h:222` |
| `PIN_EPWM15_B` (offset) | `0x128` | `pinmux.h:223` |

각 PADCONFIG 절대주소 = `CSL_IOMUX_U_BASE + offset`.

---

## UART5 사례 (발견 경로)

UART5는 LaunchPad에서 **전용 핀이 없어 EPWM15 패드를 alt-function(`PIN_MODE(1)`)으로 빌려 쓴다** — 이 alt-function 패드의 IP default가 buffer-disabled라 force가 필요했다. 8kw-ev-wpt-tx와 lp-am263p가 **동일 핀·레지스터 좌표**를 공유한다.

| UART5 신호 | mux | ball | PADCONFIG offset | 절대주소 |
|------------|-----|------|------------------|----------|
| UART5_TXD | EPWM15_A | **P15** | `PIN_EPWM15_A = 0x124` | `0x53100124` |
| UART5_RXD | EPWM15_B | **R16** | `PIN_EPWM15_B = 0x128` | `0x53100128` |

- SysConfig 생성 PADCONFIG 값 = `PIN_MODE(1) | PIN_PULL_DISABLE | PIN_SLEW_RATE_LOW` = **`0x501`** (OE/IE override 없음). 두 프로젝트 `ti_pinmux_config.c:42-51` 동일.
- **lp-am263p 레퍼런스** (loopback, RX+TX 둘 다 force): `evaluations/uart5/empty.c:52-88` (force_io 함수), `:107-113` (call site). 외부 loopback 배선 J1.4(TX) ↔ J1.3(RX). RX input buffer가 안 켜지면 `UART_read`가 영원히 블록된다 — 이게 발견 계기 (`empty.c:52-57` 주석).
- **8kw-ev-wpt-tx** (TX 전용 디버그 송신): `src/eta_bsp/eta_uart5.c:64-94` — TX(EPWM15_A)만 `PIN_FORCE_OUTPUT_ENABLE`, RX force는 의도적으로 주석 처리(TX 전용). call site `eta_uart5.c:121-122` (`eta_uart5_init` 진입 직후). **lp-am263p TX 경로와 byte-identical.** TXD=EPWM15_A=J1.4.

### 이번 8kw UART5 미동작 건 결론 (갱신 2026-06-09)

펌웨어 IOMUX/PADCONFIG 처리는 **원인이 아니다.** 8kw의 TX force-output-enable이 검증된 lp-am263p 예제와 동일하고, OE 비트 극성(set=enable)도 확정됐다.

★ **현재 상태(branch adc)**: TX force-enable 코드(`:64-94`, `:121-122`)는 **살아있으나**, UART5 차동라인으로 실제 바이트를 내보내는 `snprintf`+`UART_write` 블록은 **통째로 주석 처리**됨(`eta_uart5.c:159-170`) → **현재 UART5 차동 송신은 시도조차 안 함.** 1초 주기 출력은 UART0 콘솔(`DebugP_log`)로만 나간다. 또한 **RS-485 DE/485_EN(THVD1400 U13) 제어 코드 미구현**(src 전체 `485`/`DE`/`THVD` 토큰 0건).

따라서 미동작은 ① `UART_write` 비활성 + ② RS-485 DE 제어 부재 두 층 모두에서 기인. → 복구 작업: `UART_write` 주석 해제 + EN_485 GPIO 제어 구현·검증. 8kw [[status]] 미결 참조.

**DE 핀 확정 (2026-06-10)**: THVD1400 U13 DE·485_EN 공통 연결 → **LP-AM263P J5.48 = GPIO91** (UG Table 2-30 Mode6/7). 코드 식별자 = **`EN_485`** (`485_EN`은 C 식별자 선두 숫자 금지로 변경). SysConfig GPIO 인스턴스를 `EN_485`로 추가, `GPIO91` hard assign 필요.

---

## 미검증 / 확인 필요

- **런타임 PADCONFIG 전체 비트 분해 미검증**: bit6(OE) set 자체는 확인됐으나, P15 PADCONFIG(`0x53100124`)의 런타임 전체 값을 JTAG로 직접 read해 확정한 적은 없다.
  - 코드 기준 **기대값** `[추정·헤더 계산]`: syscfg write `0x501` → force 후 `0x501 | 0x40 = 0x541`. (RX라면 `0x501 | 0x10 = 0x511`.)
  - => 다음에 JTAG로 `0x53100124` 직접 read해 `0x541`과 일치하는지 확정 필요.
- **EPWM15_A/B 패드의 IP default = buffer-disabled** 라는 전제: 근거는 SDK 예제 코드 주석(`empty.c:53-55`)이며, **TRM/cslr PADCONFIG 리셋값으로는 미확인.** ([[am263p_trm]] PADCONFIG 리셋값 챕터에서 교차확인 후보.)

---

## 관련 페이지

- [[am263p_adc_rti_trigger]] — 형제 AM263P 브링업 정본 (RTI→ADC 트리거 결선 함정). "syscfg 한 줄 누락이 게이트를 막는다"는 동형 함정.
- [[jtag_flash_harness]] — flash-time 층위 정본. 플랫폼 지식을 lp-am263p에 두고 8kw 백링크하는 동일 패턴.
- [[lp_am263p_ug]] — LP-AM263P 핀맵·핀먹스·J1 헤더.
- [[am263p_trm]] — PADCONFIG 리셋값 교차확인용.
