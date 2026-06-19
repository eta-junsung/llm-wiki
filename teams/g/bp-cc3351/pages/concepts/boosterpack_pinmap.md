---
tags: [concept, bp-cc3351, pinmap, lp-am263p]
source: [[bp_cc3351_evm_ug]] Table 2-3/2-4 + [[bp_cc3351_schematic]] Sheet 3
date: 2026-06-02
---

# BP-CC3351 BoosterPack P1/P2 핀맵

BP-CC3351의 2×20핀 BoosterPack 커넥터(P1, P2) 전체 핀 할당.  
AM263P 포팅 시 syscfg 신호 ↔ BP 핀 대응 확인에 사용.

---

## P1 (20핀, 좌측 커넥터)

| Pin | 회로도 신호명 | Dir (CC3351 기준) | 설명 |
|-----|-------------|-------------------|------|
| P1.1 | VCC_MCU_3V3 | Input | 기능 없음 (3.3V 참조 공급) |
| P1.2 | Reserved | — | — |
| P1.3 | UART_TX_3V3 | Output (from CC3351) | BLE HCI UART TX (CC3351→Host) |
| P1.4 | UART_RX_3V3 | Input (to CC3351) | BLE HCI UART RX (Host→CC3351) |
| **P1.5** | **LP_RESET** | **Input (active-low)** | **CC3351 nRESET. HIGH=running, LOW=reset** |
| P1.6 | Reserved | — | — |
| P1.7 | SDIO_CLK_3V3 | Input | SDIO clock 또는 SPI clock (Host 구동) |
| P1.8 | IRQ_WL_3V3 | Output (from CC3351) | Wi-Fi 인터럽트 → Host |
| P1.9 | COEX_GRANT_3V3 | Output | 공존 인터페이스 grant (향후 사용) |
| P1.10 | ANT_SEL_3V3 | Output | 안테나 선택 |
| P1.21 | VCC_MCU_5V | Power | LaunchPad 5V → BP-CC3351 LDO 공급 |
| P1.22 | GND | GND | — |
| P1.23~P1.28 | Reserved | — | — |
| P1.29 | COEX_REQ_3V3 | Input | 공존 인터페이스 request (향후 사용) |
| P1.30 | COEX_PRIORITY_3V3 | Input | 공존 인터페이스 priority (향후 사용) |

---

## P2 (20핀, 우측 커넥터)

| Pin | 회로도 신호명 | Dir (CC3351 기준) | 설명 |
|-----|-------------|-------------------|------|
| P2.11 | IRQ_BLE_3V3 | Output (from CC3351) | BLE 인터럽트 → Host |
| P2.12 | Reserved | — | — |
| P2.13 | Reserved | — | — |
| P2.14 | SDIO_D0_3V3 (POCI) | I/O | SDIO D0 또는 SPI POCI (MISO) |
| P2.15 | SDIO_CMD_3V3 (PICO) | I/O | SDIO CMD 또는 SPI PICO (MOSI) |
| P2.16 | Reserved | — | — |
| P2.17 | FAST_CLK_REQ_3V3 | Output (from CC3351) | Fast clock 요청 |
| P2.18 | SDIO_D3_3V3 (CS) | I/O | SDIO D3 또는 SPI CS |
| P2.19 | SLOW_CLK_IN_3V3 | Input | 외부 RTC 32.768kHz 클럭 입력 |
| P2.20 | GND | GND | — |
| P2.31~P2.33 | Reserved | — | — |
| P2.34 | LOGGER_3V3 | Output (from CC3351) | CC3351 debug UART TX |
| P2.35 | Reserved | — | — |
| P2.36 | UART_RTS_3V3 | Output (from CC3351) | BLE HCI RTS (flow control) |
| P2.37 | UART_CTS_3V3 | Input (to CC3351) | BLE HCI CTS (flow control) |
| P2.38 | SDIO_D1_3V3 | I/O | SDIO D1 |
| P2.39 | SDIO_D2_3V3 | I/O | SDIO D2 |
| P2.40 | Reserved | — | — |

---

## AM263P syscfg ↔ BP 핀 대응 (lp-am263p 포팅)

syscfg 기준 (`teams/g/lp-am263p/CLAUDE.md`):

| 기능 | AM263P 신호 | BP 핀 | BP 신호 |
|------|------------|-------|---------|
| **WLAN_EN (reset)** | `PR0_PRU0_GPIO12` (ball M15) | **P1.5** | LP_RESET (active-low) |
| **WLAN_IRQ** | `PR0_PRU0_GPIO10` (RISE edge) | P1.8 | IRQ_WL_3V3 |
| SPI CLK | MCSPI SPI0 CLK | P1.7 | SDIO_CLK_3V3 |
| SPI MOSI (PICO) | MCSPI SPI0 D0 | P2.15 | SDIO_CMD_3V3 |
| SPI MISO (POCI) | MCSPI SPI0 D1 | P2.14 | SDIO_D0_3V3 |
| SPI CS | MCSPI SPI0 CS | P2.18 | SDIO_D3_3V3 |
| BLE HCI TX (MCU→BP) | USART2 TX | P1.4 | UART_RX_3V3 |
| BLE HCI RX (BP→MCU) | USART2 RX | P1.3 | UART_TX_3V3 |

> CLK 경로(BP P1.7 → LP J1.7 → AM263P ball A11 / SPI0_CLK)는 R35(cont.) Saleae known-good 실측으로 물리 접속 확인. MOSI/MISO/CS는 동일 측정에서 SPI 디코드 정합으로 간접 확인 수준. 전체 핀맵 회로도 확인(LP-AM263P LaunchPad 회로도)은 미완.

---

## Level Shifter 전압 (J12/J13/J14)

모든 3V3 신호는 BP-CC3351 내부 level shifter를 통해 1.8V로 변환되어 CC3351에 연결됨.  
AM263P(3.3V GPIO) 연결 시 J12/J13/J14 점퍼를 3.3V 위치로 설정.

---

## 주의사항

- **P1 핀 번호 불연속**: P1.1~P1.10 다음이 P1.21 (P1.11~P1.20은 P2 헤더 내부 연번이므로 존재하지 않음).
- **LP_RESET active-low**: `wlan_TurnOnWlan`에서 LOW→딜레이→HIGH 시퀀스로 NP reset pulse 생성. [[status]] R35 참조. **딜레이 단위**: `osi_Sleep(n)` 인자 단위는 **초(second)** — 밀리초가 아님. 예: `osi_Sleep(2)` = 2초 대기. 포팅 시 지나치게 짧은 딜레이 삽입에 주의.
- **D1 Yellow LED**: LP_RESET=HIGH(running)이면 점등. 보드에서 nRESET 상태 시각 확인 가능.
- **SoP strap은 LP헤더(3.3V측)에서 못 읽음 (R38 confound)**: strap핀(IRQ_WL/IRQ_BLE/LOGGER)을 LP헤더 3.3V측에서 프로브하면 리셋 LOW 구간에 strap이 동반 LOW로 끌려감 — level shifter가 리셋에 게이팅되기 때문. LP헤더에서 본 값은 1.8V IC측 진짜 SoP strap이 아님. 진짜 SoP 확인은 CC3351 1.8V IC측(R7/R8 strap 저항) 직접 프로브 필요. (R38 sop2에서 확인)
