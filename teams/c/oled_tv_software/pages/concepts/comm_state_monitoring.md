---
tags: [concept, protocol, spi, comm_health]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__from-eta_tx-to_etx_rx.CSV
date: 2026-05-13
subsystem: 01_RX_control, 02_RX_esb
---

# 통신 상태 모니터링 (SPI_Comm_St, BLE_Comm_St)

SPI 패킷의 시스템 상태 비트맵 (Header 0x10)에 포함된 통신 헬스체크 비트 두 개. 통신 단절 시 fault 처리하는 로직의 근거.

## SPI_Comm_St (Bit.5 of Buffer[0] in 0x10)

- **무선모듈 ↔ [[rx_control]] 간 SPI 통신 상태** 확인용
- 무선모듈이 **200 ms마다 0과 1을 교번**하여 비트를 갱신
- [[rx_control]]는 일정 시간 변화가 없으면 SPI 단절로 간주
- 통신 불량 시:
  - 시스템 대기 상태에서는 **Warning**
  - 출력 중에는 **Fault 처리 + 출력 차단**
- ESB 전환 후에도 동일 로직 유지 예정 (SPI 구간은 그대로)

> ✅ **구현 확정 (2026-05-29)**: 위 200ms 교번 사양이 코드로 실현됨. 과거 코드는 매 SPI 사이클마다 토글(주기 종속)했으나, `02_RX_ble Heartbeat_Loop()`(millis 200ms 게이트)로 분리되어 사양과 정합. STM32는 5초 무변화 타임아웃(`SPI_HB_TIMEOUT_MS`)으로 단절 판정. 오실로(P0.17) 실보드 검증 완료. 구현 상세·검증 → [[spi_link_reliability]].

## BLE_Comm_St (Bit.6 of Buffer[0] in 0x10)

- **무선 구간 페어링/링크 상태** 확인용 (당시 BLE)
- 0: 통신 대기 또는 통신 불량
- 1: 페어링되어 정상 운용 중
- 무선모듈이 자체적으로 신호를 생성하여 SPI를 통해 [[rx_control]]에 전달

> ⚠️ ESB 전환 시 명칭과 거동이 바뀔 가능성 있음. ESB는 자동 페어링 개념이 BLE와 달라 단순 "linked/not linked" 표현이 부적절할 수 있음. 향후 사양 확정 시 본 페이지 갱신.

## 관련

- [[spi_link_reliability]] — heartbeat 구현·검증·SPI 단절 복구 (구현 측)
- [[spi_packet_format]] — 패킷 위치
- [[tx_to_rx_packets]] — 0x10 Buffer[0] 비트 매핑 전체
- [[spi_protocol_manual_260513]] — 원본
