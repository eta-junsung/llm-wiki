---
tags: [source, protocol, spi, historical, ble]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__*.CSV
date: 2026-05-13
subsystem: 01_RX_control, 02_RX_esb
---

# OLED TV SPI 프로토콜 매뉴얼 (소스, 260513)

Rx Module (STM32, Master) ↔ Rx 무선통신 모듈 (Slave) 간 **SPI 통신 프로토콜 사양**. 무선 구간은 작성 당시 BLE였고 추후 ESB로 교체 예정. SPI 패킷 구조 자체는 ESB 전환 후에도 유지.

원본 (CP949 → UTF-8 변환본 옆에 보관):
- `raw/260513-oled_tv-protocol-manual__introduction.CSV` (+ `.utf8.csv`) — 개요·SPI 환경·커넥터·패킷 골격
- `raw/260513-oled_tv-protocol-manual__from-eta_tx-to_etx_rx.CSV` (+ `.utf8.csv`) — 0x10/0x11/0x12 패킷 사양
- `raw/260513-oled_tv-protocol-manual__from-eta_rx-to_etx_tx.CSV` (+ `.utf8.csv`) — 0x50/0x51/0x52 패킷 사양

---

## 한 줄 요약

11-byte SPI 패킷 (`HDR + Length(0x08) + Data[8] + CRC`)을 10ms cyclic로 교환. Tx→Rx 방향은 0x10·0x11·0x12, Rx→Tx 방향은 0x50·0x51·0x52. 페이로드는 Motorola(big-endian), 전압/전류는 0.01 스케일.

## 데이터 흐름

```
[Tx Module STM32] ─SPI─ [Tx 무선모듈] ──(BLE/ESB)── [Rx 무선모듈] ─SPI─ [Rx Module STM32]
```

이 매뉴얼은 **Rx Module ↔ Rx 무선모듈** SPI 구간을 정의. 동일 패킷이 Tx 측에서도 대칭으로 쓰이는지는 별도 문서 ingest 시 확인 필요. 무선 구간은 모듈 내부에서 처리 → SPI 레벨에서는 transparent.

## 파생 페이지

- 패킷 일반: [[spi_packet_format]]
- 방향별: [[tx_to_rx_packets]] (0x10/0x11/0x12), [[rx_to_tx_packets]] (0x50/0x51/0x52)
- 상태 모니터링: [[comm_state_monitoring]]
- 엔티티: [[rx_control]] (Master), [[rx_ble_module]] (Slave, BLE 시절 사양)

## SPI 환경

- 4선 (CS, SCK, MISO, MOSI), 9.0 Mbps
- CS Low Active, Master = Rx Module이 클럭 생성
- 커넥터: CN3 (SPI + 3.3V 비절연), CN4 (+5V 절연 — 통신 전원만)

## 주의: 원본의 모호한 부분

- `Tx_Sys_Init_St`(Bit.0)부터 비트 단위 사양은 명확하나 Header 0x10의 비트 위치 표(`Data Buffer[0] : 시스템 상태` 행)에서 일부 셀이 비어 있어 비트 자리가 곧바로 읽히지 않음. 본 wiki는 텍스트 설명·`Start Bit`(16부터 1비트씩 증가)를 신뢰해 정리.
- "BLE_Comm_St" 같은 BLE 특화 명칭은 ESB 전환 시 명칭/거동이 바뀔 수 있음 → [[comm_state_monitoring]] 참조.
- 0x50의 Data Buffer[2] 비트들이 원문에서 일부 `Bit.3` 라벨 중복 (CSV 변환 오류 아님, 원문 오기). 본 wiki는 `Start Bit` 값으로 정렬.
