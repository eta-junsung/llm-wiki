---
tags: [concept, protocol, spi, esb]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__introduction.CSV
date: 2026-05-13
subsystem: 01_RX_control, 02_RX_esb, 03_TX_esb
---

# SPI 패킷 포맷 (= 무선 wire 사양)

[[rx_control]]과 무선통신 모듈 사이의 SPI 통신 패킷 골격. 무선모듈은 transparent bridge로 동작하여 **이 11 B 패킷이 그대로 무선구간(BLE→ESB) wire format**이 된다. ESB 전환 시 transport만 교체, 패킷 구조는 그대로 유지.

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

| HDR | 방향 (end-to-end) | 페이로드 종류 | 페이지 |
|---|---|---|---|
| 0x10 | TX → RX | Tx 시스템 상태 비트맵 | [[tx_to_rx_packets]] |
| 0x11 | TX → RX | Tx 입력측 Analog (Vdc_bus, Idc_bus) | [[tx_to_rx_packets]] |
| 0x12 | TX → RX | Tx 출력측 Analog + 온도 | [[tx_to_rx_packets]] |
| 0x50 | RX → TX | Rx 시스템 상태 비트맵 | [[rx_to_tx_packets]] |
| 0x51 | RX → TX | Rx 입력측 Analog + Tx Buck Vout Ref | [[rx_to_tx_packets]] |
| 0x52 | RX → TX | Rx 출력측 Analog + 온도 #1·#2 | [[rx_to_tx_packets]] |

- `0x10`대 ↔ `0x50`대가 같은 의미 카테고리에서 방향만 반대 (상태/입력/출력).
- 무선모듈은 transparent bridge — SPI로 들어온 11 B 프레임을 그대로 무선(BLE/ESB)으로 운반.

## ESB 매핑 (운용 시 함의)

- 한 패킷 11 B → nRF52 ESB dynamic payload(max 252 B) 한참 여유.
- 자연스러운 매핑: **TX_nRF = PTX** (0x10/0x11/0x12 라운드로빈 송신), **RX_nRF = PRX** (ACK payload에 0x50/0x51/0x52 라운드로빈 회신). 0x51의 `Buffer[6..7]` (Tx Buck Vout Ref)이 RX→TX 제어 채널이라 ACK 회수가 의미 있음.
- 송신 스케줄(매 10ms 한 패킷씩 라운드로빈 vs 묶음 송신)은 nRF 펌웨어 설계 사항 — `[[esb_link_layer]]`에서 결정 예정.

## 공통 스케일

- 전압·전류: **0.01 스케일** (예: 210.95 V → 21,095)
- 온도: 헤더별로 0.1[℃] 또는 0.01[℃]가 섞여 있음 — 원문 그대로. [[tx_to_rx_packets]], [[rx_to_tx_packets]] 표 참조 (Header 0x52에서 Power Stack#1과 #2의 스케일 표기가 다름 — 원문 오기 가능성).

## 출처

- [[spi_protocol_manual_260513]]
