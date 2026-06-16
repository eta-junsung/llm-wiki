---
tags: [concept, uart5, packet, protocol, telemetry, 8kw-ev-wpt-tx]
source: 펌웨어 repo branch uart5 (commit ba241fa·979699d) + 실보드 검증 2026-06-11. branch gpio GPIO 양방향 확장 2026-06-16. src/eta_bsp/eta_packet.{c,h}, eta_uart5.{c,h}
date: 2026-06-16
subsystem: 8kw-ev-wpt-tx
---

# UART5 텔레메트리 패킷 프로토콜 — 펌웨어 ↔ PC 공통 계약

LP-AM263P 8kW WPT TX 보드가 UART5로 PC와 주고받는 **바이너리 패킷 프레임**. 펌웨어와 호스트([[pc_monitor_gui]])가 공유하는 wire 계약이다. branch `uart5`(commit `ba241fa`·`979699d`) 실보드 검증 2026-06-11, branch `gpio` GPIO 양방향 확장 2026-06-16.

선례 = c팀 oled의 [[pc_uart_gui]]/[[spi_packet_format]](11B·XOR·다중 HDR·양방향). 이 8kw 프로토콜은 그 강건성(HDR 동기+체크섬 재동기)을 가져오되 **CRC-16**으로 단순화한 별개 계약이다.

## 공통 프레임 구조 (big-endian)

```
[SOF=0xA5][LEN][TYPE][SEQ][...payload (LEN bytes)...][CRC-16 2B]
```

- **CRC-16/CCITT-FALSE**: poly `0x1021`, init `0xFFFF`, reflect 없음. 계산 범위 = **byte[1..끝-2]** (LEN부터 payload 끝, SOF·CRC 제외).
- **SEQ**: 0~255 rolling, 드롭 감지용.

---

## 패킷 타입

### TYPE=0x01 — ADC 텔레메트리 (MCU→PC, 18B 고정)

| 바이트 | 필드 | 값/의미 |
|--------|------|---------|
| [0] | SOF | `0xA5` |
| [1] | LEN | `12` |
| [2] | TYPE | `0x01` |
| [3] | SEQ | rolling |
| [4..15] | payload | ch0..ch5 raw **u16 big-endian** (6×2=12B) |
| [16..17] | CRC | CRC-16/CCITT-FALSE |

- 송신 주기 **RTI2 10 Hz(100 ms)**, polled blocking.
- 실보드 검증(2026-06-11): 10.067 Hz·301프레임·SEQ 드롭 0·CRC 에러 0.

### TYPE=0x02 — GPIO 상태 (MCU→PC, 7B, 이벤트 기반)

| 바이트 | 필드 | 값/의미 |
|--------|------|---------|
| [0] | SOF | `0xA5` |
| [1] | LEN | `1` |
| [2] | TYPE | `0x02` |
| [3] | SEQ | rolling |
| [4] | GPIO_STATUS | bit0=485_EN, bit1=GD_EN_seed |
| [5..6] | CRC | CRC-16/CCITT-FALSE |

- **이벤트 기반**: `eta_gpio_init()` 직후 및 `set_gd_en()` 호출 시 자동 송신.
- GUI 수신 시 GPIO Control 섹션 상태 라벨 갱신.

### TYPE=0x10 — GPIO 커맨드 (PC→MCU, 8B, fire-and-forget)

| 바이트 | 필드 | 값/의미 |
|--------|------|---------|
| [0] | SOF | `0xA5` |
| [1] | LEN | `2` |
| [2] | TYPE | `0x10` |
| [3] | SEQ | rolling |
| [4] | CMD_ID | `0x01`=GD_EN_seed |
| [5] | VALUE | `0`=LOW / `1`=HIGH |
| [6..7] | CRC | CRC-16/CCITT-FALSE |

- MCU 수신 → `eta_gpio_set_gd_en(VALUE)` 즉시 실행 → TYPE=0x02 응답 반송.
- GUI `send_gpio_cmd()`: Lock 포함, CRC-16 적용.

## payload 채널 순서 (ETA_ADC_CH enum 그대로)

| idx | 신호 | enum |
|-----|------|------|
| ch0 | Temp_Module2 | ETA_ADC_CH_TEMP_MODULE2 |
| ch1 | Temp_Module1 | ETA_ADC_CH_TEMP_MODULE1 |
| ch2 | GA_Vin | ETA_ADC_CH_GA_VIN |
| ch3 | I_LCC_SEN | ETA_ADC_CH_I_LCC_SEN |
| ch4 | I_COIL_SEN | ETA_ADC_CH_I_COIL_SEN |
| ch5 | GA_Iin_SEN | ETA_ADC_CH_GA_IIN_SEN |

핀맵·인스턴스 배치는 [[adc_pinmap]]. wire 순서는 `eta_packet.c`의 채널 루프(=`ETA_ADC_CH` enum)가 단일 소스 — 채널 추가 시 직렬화가 자동 추종한다(payload 길이·LEN도 함께 따라감).

## thin device, smart host

- **wire에는 ADC raw count(0~4095)만** 실린다. mV·물리량(°C/V/A)은 **호스트가 파생**한다.
- mV 변환식은 펌웨어 `eta_adc.c`의 정수식 `mV = raw*3300/4095`을 호스트가 **그대로 미러**한다(부동소수 불일치 방지).
- 보드는 센싱·직렬화만, 표시·스케일링·로깅은 PC가 — 펌웨어를 얇게 유지한다.

## 전송 / 링크

- UART5 **115200 / 8N1**, **polled blocking** 송신.
- ADC 텔레메트리(TYPE=0x01) 주기 = **RTI2 10 Hz(100 ms)**.
- **485_EN(GPIO91) DE 자동 토글**: `UART_write` 전 HIGH → 후 LOW. THVD1400 U13 TX enable 자동 제어 — 별도 코드 불필요.
- 펌웨어 구조: `src/eta_bsp/eta_packet.{c,h}`가 프레임 조립 + CRC, `eta_uart5.c`는 송신·수신·파서 담당. 핀맵 `eta_uart5.h` — **TXD = EPWM15_A = J1.4**.
- ⚠️ UART5_TXD는 alt-function 패드(EPWM15)라 SoC IOMUX force_io 필요([[am263p_iomux_force_io_enable]]) + 온보드 보드먹스(U54/TCA6416 P00/P14=LOW) 게이트([[lp_am263p_uart_epwm_mux]]). 둘 다 충족돼야 J1.4 헤더로 출력.
- ⚠️ **RX 수신은 1바이트씩 read 필수**: SDK `UART_read()` POLLED+NO_WAIT+FULL 조합에서 `rx.count`가 앱 transaction에 반영되지 않아 8바이트 요청 시 stale 버퍼 주입 → SOF 탐색 불가. `count=1`, 반환값 `==SystemP_SUCCESS`로 판단. 상세 [[uart5_rx_polled_1byte]].

## 수신측 재동기 (호스트 파서 계약)

[[pc_monitor_gui]]의 리더가 스트림에서 18B를 떼어내는 규칙:

1. **SOF(0xA5) 탐색** → 2. **LEN/TYPE 게이트**(12/0x01 일치?) → 3. **CRC 검증** → 4. 실패 시 **1바이트 슬라이드 후 재시도**.

1바이트 슬라이딩 덕에 ASCII 잡음·가짜 SOF 같은 비-패킷 바이트는 게이트/CRC가 안 맞아 자연 폐기된다(별도 필터 불필요). oled 선례([[pc_uart_gui]])의 HDR 동기+재동기와 동형.

## 검증 (실보드, 2026-06-11)

**(사실)** COM13(CP210x USB-UART, J1.4→THVD1400→J24 경로) 와이어 읽기, **29.8 s 관찰**:
- 레이트 **10.067 Hz**, **301 프레임 전부 유효**, **SEQ 드롭 0 · CRC 에러 0**.
- 프레이밍 강건성(gui.py 운영 파서로): 정상 디코드 / 1바이트 손상→리젝트+재동기 / ASCII 잡음·가짜 SOF→게이트 폐기 후 복구 — 모두 PASS.

## 빈자리 (미검증/잔여)

- **UART5는 온보드 XDS110 가상 COM에 안 실린다** — 외부 CP210x(COM13)로만 PC 도달.
- **송신이 polled blocking** — 논블로킹(콜백/DMA) 전환은 Phase 2 잔여.
- 물리량(°C/V/A) 미교정 — wire는 raw, host는 mV까지가 종착점(계수 미입수, [[adc_pinmap]] §미확인).
- ~~**TYPE=0x02·0x10 GUI 왕복 검증 잔여**~~ — ✅ **완료(2026-06-16)**: GUI GD_EN ON → TYPE=0x10 PC→MCU → `eta_gpio_loop()` GPIO93 HIGH. Logic2 실측 확인. standalone 부팅 후 재확인.

## 관련

- [[pc_monitor_gui]] — 이 패킷을 소비하는 호스트 PC GUI
- [[adc_pinmap]] — ADC 6채널 핀맵·인스턴스·enum
- [[pc_uart_gui]] — c팀 oled 선례(11B·XOR·다중 HDR·양방향)
- [[am263p_iomux_force_io_enable]] — UART5(EPWM15) alt-function 패드 force_io
- [[lp_am263p_uart_epwm_mux]] — 온보드 U54/TCA6416 보드먹스 게이트
