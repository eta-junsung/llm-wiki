---
tags: [concept, uart5, packet, protocol, telemetry, 8kw-ev-wpt-tx]
source: 펌웨어 repo branch uart5 (commit ba241fa·979699d) + 실보드 검증 2026-06-11. src/eta_bsp/eta_packet.{c,h}, eta_uart5.{c,h}
date: 2026-06-11
subsystem: 8kw-ev-wpt-tx
---

# UART5 텔레메트리 패킷 프로토콜 — 펌웨어 ↔ PC 공통 계약

LP-AM263P 8kW WPT TX 보드가 UART5로 PC에 ADC 6채널을 송출하는 **18B 고정 바이너리 프레임**. 펌웨어와 호스트([[pc_monitor_gui]])가 공유하는 wire 계약이다. 단방향(보드→PC) 텔레메트리. branch `uart5`(commit `ba241fa`·`979699d`), 실보드 검증 2026-06-11.

선례 = c팀 oled의 [[pc_uart_gui]]/[[spi_packet_format]](11B·XOR·다중 HDR·양방향). 이 8kw 프로토콜은 그 강건성(HDR 동기+체크섬 재동기)을 가져오되 **CRC-16·단일 패킷·단방향**으로 단순화한 별개 계약이다.

## 프레임 (18B 고정, big-endian)

| 바이트 | 필드 | 값/의미 |
|--------|------|---------|
| [0] | SOF | `0xA5` (start of frame) |
| [1] | LEN | `12` (payload 길이) |
| [2] | TYPE | `0x01` (ADC telemetry) |
| [3] | SEQ | `0..255` rolling (드롭 감지용) |
| [4..15] | payload | ch0..ch5 raw, 각 **u16 big-endian** (6×2 = 12B) |
| [16..17] | CRC | **CRC-16/CCITT-FALSE** |

- **CRC-16/CCITT-FALSE**: poly `0x1021`, init `0xFFFF`, reflect 없음(in/out 모두). 계산 범위 = **byte[1..15]**(LEN·TYPE·SEQ·payload, SOF·CRC 자신 제외 = 15B).
- 전체 18B = 헤더 4B + payload 12B + CRC 2B.

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
- 송신 주기 = **RTI2 10 Hz(100 ms)**.
- 펌웨어 구조: `src/eta_bsp/eta_packet.{c,h}`가 프레임 조립 + CRC, `eta_uart5.c`는 송신만 담당. 핀맵은 `eta_uart5.h` — **TXD = EPWM15_A = J1.4**.
- ⚠️ UART5_TXD는 alt-function 패드(EPWM15)라 SoC IOMUX force_io 필요([[am263p_iomux_force_io_enable]]) + 온보드 보드먹스(U54/TCA6416 P00/P14=LOW) 게이트([[lp_am263p_uart_epwm_mux]]). 둘 다 충족돼야 J1.4 헤더로 출력.

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

## 관련

- [[pc_monitor_gui]] — 이 패킷을 소비하는 호스트 PC GUI
- [[adc_pinmap]] — ADC 6채널 핀맵·인스턴스·enum
- [[pc_uart_gui]] — c팀 oled 선례(11B·XOR·다중 HDR·양방향)
- [[am263p_iomux_force_io_enable]] — UART5(EPWM15) alt-function 패드 force_io
- [[lp_am263p_uart_epwm_mux]] — 온보드 U54/TCA6416 보드먹스 게이트
