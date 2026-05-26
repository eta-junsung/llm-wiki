---
tags: [entity, board, esb]
source: teams/c/oled_tv_software/raw/prd_v1.0.md
date: 2026-05-26
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

## 통신 인터페이스

- **ESB RF**: [[rx_ble_module]](PRX)과 2.4GHz 링크. 파라미터 → [[esb_link_layer]]
- **TX 보드 SPI**: 미구현. 구현 후 entity 갱신 필요.

## 출처

- [[prd]] (§4.3)
