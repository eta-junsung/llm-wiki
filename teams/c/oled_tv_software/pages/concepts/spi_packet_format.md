---
tags: [concept, protocol, spi]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__introduction.CSV
date: 2026-05-13
subsystem: 01_RX_control, 02_RX_esb
---

# SPI 패킷 포맷 (Rx Module ↔ 무선모듈)

[[rx_control]]과 무선통신 모듈([[rx_ble_module]], 향후 ESB) 사이의 SPI 통신 패킷 골격. 패킷 구조 자체는 ESB 전환 시에도 유지.

## 패킷 구조 (총 11 byte)

| 필드 | 크기 | 비트 범위 | 의미 |
|---|---|---|---|
| ① HDR (Header) | 1 byte | [0..7] | 명령어 종류 구분 + 패킷 시작 |
| ② Length | 1 byte | [8..15] | 데이터 필드 길이, **고정 0x08** |
| ③ Data Buffer | 8 byte | [16..79] | 페이로드 (Data[0]..Data[7]) |
| ④ CRC (CheckSum) | 1 byte | [80..87] | HDR ~ Data[7] 영역의 CheckSum |

- **Byte order**: Motorola (big-endian)
- **데이터 타입**: 기본 Uint16, 온도는 Int16
- **전송 주기**: 10 ms cyclic (모든 헤더 공통, 개발자 조정 가능)

## 헤더 ID 매핑

| HDR | 방향 | 페이로드 종류 | 페이지 |
|---|---|---|---|
| 0x10 | 무선모듈 → Rx | Tx 시스템 상태 비트맵 | [[tx_to_rx_packets]] |
| 0x11 | 무선모듈 → Rx | Tx 입력측 Analog (Vdc_bus, Idc_bus) | [[tx_to_rx_packets]] |
| 0x12 | 무선모듈 → Rx | Tx 출력측 Analog + 온도 | [[tx_to_rx_packets]] |
| 0x50 | Rx → 무선모듈 | Rx 시스템 상태 비트맵 | [[rx_to_tx_packets]] |
| 0x51 | Rx → 무선모듈 | Rx 입력측 Analog + Tx Buck Vout Ref | [[rx_to_tx_packets]] |
| 0x52 | Rx → 무선모듈 | Rx 출력측 Analog + 온도 #1·#2 | [[rx_to_tx_packets]] |

- `0x10`대 ↔ `0x50`대가 같은 의미 카테고리에서 방향만 반대 (상태/입력/출력).
- 무선모듈은 Tx 측에서 받은 패킷을 Rx 측 MCU에 그대로 SPI로 전달하는 브리지 역할.

## 공통 스케일

- 전압·전류: **0.01 스케일** (예: 210.95 V → 21,095)
- 온도: 헤더별로 0.1[℃] 또는 0.01[℃]가 섞여 있음 — 원문 그대로. [[tx_to_rx_packets]], [[rx_to_tx_packets]] 표 참조 (Header 0x52에서 Power Stack#1과 #2의 스케일 표기가 다름 — 원문 오기 가능성).

## 출처

- [[spi_protocol_manual_260513]]
