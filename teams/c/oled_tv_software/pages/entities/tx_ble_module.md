---
tags: [entity, board, esb]
source: teams/c/oled_tv_software/raw/prd_v1.0.md
date: 2026-05-28
subsystem: 03_TX_ble
---

# TX BLE 모듈 (03_TX_ble, ESB PTX)

TX 보드 측 무선 모듈. nRF52832 기반, ESB PTX로 동작. TX 보드와 SPI로 연결될 예정이나 현재 미구현.

## 역할

- ESB PTX (Primary Transmitter): 10ms 주기로 ESB 패킷 전송 개시
- RX측([[rx_ble_module]], PRX)으로부터 ACK payload로 RX 데이터 수신
- HDR round-robin 송신: TX_STATUS`0x10` → TX_INPUT`0x11` → TX_OUTPUT`0x12`
- ACK에 실려 온 RX 데이터(0x50/0x51/0x52)를 TX 보드로 SPI 전달 (미구현)

## 펌웨어 현황

| 항목 | 상태 |
|---|---|
| ESB PTX 기본 동작 | ✓ 구현됨 |
| ACK payload 수신 (0x50/0x51/0x52) | ✓ 구현됨 |
| round-robin HDR 송신 | ✓ 구현됨 |
| TX 보드 ↔ 03_TX_ble SPI (`SPI_Loop`) | ✗ 전체 주석 처리됨 |
| LED 인디케이터 (LED1 점등 / LED2·3 토글) | ✓ 구현+검증 (2026-06-04 실보드) |
| 보드 분기 (BOARD_CUSTOM + custom_board.h) | ✓ 구현+검증 |
| while(1) 구조 정리 | △ 구현됨·미검증 |
| GPIO P0.17/P0.18 토글 (OSC 검증용) | △ 구현됨·미검증 |
| TX_FAILED 1초 윈도우 카운터 | △ 구현됨·미검증 |
| TX UART 모니터 출력 포맷 개선 | △ 구현됨·미검증 |

## ESB 타이밍 측정값

2026-05-27 오실로스코프 실측. 상세 이미지 → [[esb_timing_measurements]].

| 항목 | 측정값 |
|---|---|
| TX→ACK 왕복 지연 | 약 470 us |
| TX 전송 주기 | 약 920 us |

## Monitor_Loop 출력 포맷

`03_TX_ble/Application/main.c:568-614`, 1000ms 주기. ACK payload(0x50/0x51/0x52)를 디코딩해 UART/RTT 출력.

```
ESB tx=0x000C3E fail=0/s | ACK rx=0x000C3D [0x50 0x51 0x52]
[eta-rx]
0x50 | Rx_Fault_St=0 Rx_Warning_St=0 Rx_Sys_Rdy_St=1 Rx_Buck_St=1 fw=0.1
0x51 | Rx_Vrect=48.00V Rx_Irect=1.23A
0x52 | Rx_Vout=12.00V Rx_Iout=2.34A Rx_T1=45.0C Rx_T2=46.0C
```

`g_rx_seen_mask` 비트가 선 헤더만 출력(초기 0값 방지), 출력 후 리셋. 3헤더 수집 패턴 → [[esb_ptx_ack_assembly]].

## LED 인디케이터 (회사 BLE_Module_Board)

`gpio_init()`이 직접 구동 (SDK BSP LED 경로 미사용 — `custom_board.h`에서 `LEDS_NUMBER 0`). 핀/극성 → [[schematic_ble_module_board_v01e00]], [[gpio_verification_pinmap]].

| LED | 핀 | 동작 | 의미 |
|---|---|---|---|
| LED1 | P0.09 | 상시 점등 (init write 1) | System Ready |
| LED2 | P0.08 | 200 ms 토글 | SPI Comm Status |
| LED3 | P0.06 | 200 ms 토글 | BLE(=ESB) Comm Status |

- 극성 **active-high** (1=ON) — 2026-06-04 실측 확정.
- LED2/LED3는 현재 핀 가시화 전용(토글). ESB 패킷 comm-status 비트 연계는 후속 → [[comm_state_monitoring]].
- 코드는 `#if defined(BOARD_CUSTOM)` 가드 — DK(PCA10040) 빌드 시 미컴파일 (그 핀들이 DK에선 UART라 충돌 회피).

## 보드 분기 (DK ↔ 회사 보드)

같은 nRF52832지만 핀맵이 다르다. `_shared/custom_board.h`(신설) + emProject `BOARD_CUSTOM` define으로 분기.

| | DK (PCA10040) | 회사 보드 (BOARD_CUSTOM) |
|---|---|---|
| UART TX/RX | P0.06 / P0.08 | **P0.15 / P0.14** |
| LED | 미구동 (가드) | P0.09 / P0.08 / P0.06 |
| SPI | P0.22/26/25/27 (공통) | P0.22/26/25/27 (공통) |
| 스코프핀 | P0.17/P0.18 (공통) | P0.17/P0.18 (공통) |

`custom_board.h`: `LEDS_NUMBER 0`, `BUTTONS_NUMBER 0`, `RX_PIN_NUMBER 14`, `TX_PIN_NUMBER 15`, HWFC 미사용. 보드 전환 = emProject `BOARD_PCA10040` ↔ `BOARD_CUSTOM` 한 줄 토글. `02_RX_ble`도 동일 `custom_board.h` 공유 (LED 동작은 03만 구현).

## 통신 인터페이스

- **ESB RF**: [[rx_ble_module]](PRX)과 2.4GHz 링크. 파라미터 → [[esb_link_layer]]
- **TX 보드 SPI**: 미구현. 구현 후 entity 갱신 필요.

## 출처

- [[prd]] (§4.3)
- [[spi_debug_log_report_260529]]
