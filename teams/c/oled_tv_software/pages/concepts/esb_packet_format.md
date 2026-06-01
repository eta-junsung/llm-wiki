---
tags: [concept, protocol, esb]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__introduction.CSV
date: 2026-05-26
subsystem: 02_RX_ble, 03_TX_ble
---

# ESB 패킷 포맷 (무선 wire 사양)

[[tx_ble_module]](PTX) ↔ [[rx_ble_module]](PRX) 간 ESB RF 구간의 wire 포맷. 총 11 B 고정 길이. SPI wire와 동일한 `oled_tv_packet_t` 구조를 공유하며 — nRF가 SPI 수신 패킷을 ESB로 그대로 중계하므로 포맷 변환이 없다. 03_TX_ble도 자체 `esb_packet_t` 정의를 제거하고 통합 타입으로 통일됨 (2026-06-01, c9cf6a3). STM32 코드 내부 컨테이너(`rx_module_data_t` 62B / `tx_module_data_t` 51B)와는 별개 층위 — [[spi_packet_format]] 참조.

## 패킷 구조 (총 11 byte)

| 필드 | 크기 | 의미 |
|---|---|---|
| ① HDR (Header) | 1 byte | 패킷 종류 구분 (라운드로빈) |
| ② Length | 1 byte | 데이터 필드 길이, **고정 0x08** |
| ③ Data Buffer | 8 byte | 페이로드 (Data[0]..Data[7]) |
| ④ CRC (CheckSum) | 1 byte | HDR ~ Data[7] 영역의 CheckSum |

- **Byte order**: Motorola (big-endian)
- **데이터 타입**: 기본 Uint16, 온도는 Int16
- **전송 주기**: 10 ms cyclic (PTX 기준 — [[esb_link_layer]] 참조)
- **ESB SDK 설정**: `NRF_ESB_MAX_PAYLOAD_LENGTH = 64` (기본 32에서 확장)

## 헤더 ID 매핑

| HDR | 방향 (end-to-end) | 페이로드 종류 | 페이지 |
|---|---|---|---|
| 0x10 | TX → RX (PTX→PRX) | Tx 시스템 상태 비트맵 | [[tx_to_rx_packets]] |
| 0x11 | TX → RX (PTX→PRX) | Tx 입력측 Analog (Vdc_bus, Idc_bus) | [[tx_to_rx_packets]] |
| 0x12 | TX → RX (PTX→PRX) | Tx 출력측 Analog + 온도 | [[tx_to_rx_packets]] |
| 0x50 | RX → TX (PRX ACK payload) | Rx 시스템 상태 비트맵 | [[rx_to_tx_packets]] |
| 0x51 | RX → TX (PRX ACK payload) | Rx 입력측 Analog + Tx Buck Vout Ref | [[rx_to_tx_packets]] |
| 0x52 | RX → TX (PRX ACK payload) | Rx 출력측 Analog + 온도 #1·#2 | [[rx_to_tx_packets]] |

- PTX(`03_TX_ble`)가 0x10→0x11→0x12 라운드로빈으로 10ms마다 한 패킷씩 송신.
- PRX(`02_RX_ble`)는 ACK payload 슬롯에 0x50→0x51→0x52 라운드로빈을 미리 적재. PTX의 다음 송신에 piggyback되어 회수.
- `0x10`대 ↔ `0x50`대가 같은 의미 카테고리에서 방향만 반대 (상태/입력/출력).

## 공통 스케일

- 전압·전류: **0.01 스케일** (예: 210.95 V → 21,095)
- 온도: 헤더별로 0.1[℃] 또는 0.01[℃] 혼재 — [[tx_to_rx_packets]], [[rx_to_tx_packets]] 표 참조 (Header 0x52 스케일 원문 오기 가능성).

## 출처

- [[spi_protocol_manual_260513]] (무선 wire 사양 정의 문서)
- [[prd]] (ESB 파라미터 스냅샷)
