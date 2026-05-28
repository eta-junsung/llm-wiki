---
tags: [concept, protocol, spi]
source: teams/c/oled_tv_software/pages/sources/spi_protocol_manual_260513.md
date: 2026-05-28
subsystem: 01_RX_control, 02_RX_ble
---

# STM32-nRF SPI 내부 프레임

[[rx_control]](STM32, Master) ↔ [[rx_ble_module]](nRF52832, Slave) 간 SPI 버스의 wire 포맷. **11B 고정 패킷**을 한 번에 하나씩 전송한다. [[esb_packet_format]](ESB wire)와 동일한 패킷 구조를 공유 — nRF가 SPI 수신 패킷을 ESB로 그대로 중계한다.

> **내부 데이터 컨테이너와 구분**: `rx_module_data_t` (56B) / `tx_module_data_t` (45B)는 STM32 코드 내 데이터 저장용 구조체이며 SPI wire 포맷이 아니다 (`oled_tv_protocol.h`). 실제 전송 시 이 구조체의 데이터를 11B 패킷으로 직렬화해 전송한다.

## Wire 패킷 구조 (11 byte 고정)

| 바이트 | 필드 | 크기 | 비고 |
|---|---|---|---|
| 0 | HDR | 1B | 패킷 종류 식별 |
| 1 | Length | 1B | 고정 0x08 |
| 2~9 | Data Buffer[0..7] | 8B | 페이로드 |
| 10 | CRC | 1B | HDR~Data[7] 체크섬 |

## 방향별 패킷 목록

### STM32 → nRF (RX→TX 방향)

| HDR | 내용 | 상세 |
|---|---|---|
| 0x50 | RX 시스템 상태 | [[rx_to_tx_packets]] |
| 0x51 | RX 입력측 Analog + Tx Vout Ref | [[rx_to_tx_packets]] |
| 0x52 | RX 출력측 Analog + 온도 | [[rx_to_tx_packets]] |

### nRF → STM32 (TX→RX 방향)

| HDR | 내용 | 상세 |
|---|---|---|
| 0x10 | TX 시스템 상태 | [[tx_to_rx_packets]] |
| 0x11 | TX 입력측 Analog (Vbus, Ibus) | [[tx_to_rx_packets]] |
| 0x12 | TX 출력측 Analog + 온도 | [[tx_to_rx_packets]] |

## 전송 파라미터

- **주기**: 10ms cyclic
- **SPI 속도**: 9.0 Mbps
- **CS**: Low Active, Master = STM32 (클럭 생성)
- **커넥터**: CN3 (SPI + 3.3V 비절연), CN4 (+5V 절연 — 통신 전원만)
- **STM32 핀**: SPI2, PB12-15 (NSS_SOFT)
- **nRF52832 핀**: SPIS1, P0.22/25/26/27

## 데이터 인코딩

- 바이트 순서: Motorola (Big-endian)
- 전압/전류: scale factor 0.01 (예: 47.95V → 4795)
- 온도: scale factor 패킷별 상이 → [[rx_to_tx_packets]], [[tx_to_rx_packets]] 참조

## 출처

- [[spi_protocol_manual_260513]]
