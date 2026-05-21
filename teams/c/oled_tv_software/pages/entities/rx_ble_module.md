---
tags: [entity, board, ble_module, historical, ble]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__introduction.CSV
date: 2026-05-13
subsystem: 02_RX_esb
---

# Rx BLE 모듈 (BLE 시절, 02_RX_esb)

[[rx_control]](Master)과 SPI로 연결되어 무선 구간을 처리하는 슬레이브 모듈. 작성 당시 BLE 기반이며 추후 ESB로 교체 예정 → 본 페이지는 **BLE 시절 사양** 기록 (`02_RX_esb` 서브프로젝트로 이어짐).

## 역할

- SPI Slave (CS low active)
- Tx 측 무선모듈과 BLE로 페어링하여 데이터 송수신
- 수신된 Tx 데이터를 SPI 패킷 (0x10/0x11/0x12)으로 [[rx_control]]에 전달
- [[rx_control]]로부터 받은 SPI 패킷 (0x50/0x51/0x52)을 무선으로 Tx 측에 전달
- 자체적으로 [[comm_state_monitoring|SPI/BLE 통신 상태]] 비트를 생성·갱신

## 인터페이스

### CN3 — SPI 통신용 커넥터

| Pin | 신호 |
|---|---|
| 1, 2 | +3.3 VDC (비절연 전원) |
| 3 | SPI CS (Low Active) |
| 4 | N.C |
| 5 | SPI MISO (S→M) |
| 6 | N.C |
| 7 | SPI MOSI (M→S) |
| 8 | SPI Clock (Master 생성) |
| 9, 10 | GND (비절연) |

- 4선 SPI, **9.0 Mbps**
- Byte order Motorola (big-endian)

### CN4 — 관리자 통신용 전원

| Pin | 신호 |
|---|---|
| 1, 2, 3 | +5 VDC (절연 전원) |
| 4, 5, 6 | GND (절연) |

## 통신 페어

- 상위(Master): [[rx_control]]
- 패킷 사양: [[spi_packet_format]], [[tx_to_rx_packets]], [[rx_to_tx_packets]]
- 헬스체크 비트: [[comm_state_monitoring]]

## 이행 메모 (BLE → ESB)

- 본 모듈은 ESB로 교체 예정 (`02_RX_esb`)
- SPI 패킷 구조와 핀맵은 유지 가정
- `BLE_Comm_St` 비트는 명칭/거동 재정의 가능성 — [[comm_state_monitoring]] 참조

## 출처

- [[spi_protocol_manual_260513]]
