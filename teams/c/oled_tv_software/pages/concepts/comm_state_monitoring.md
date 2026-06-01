---
tags: [concept, protocol, spi, comm_health]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__from-eta_tx-to_etx_rx.CSV
date: 2026-06-01
subsystem: 01_RX_control, 02_RX_esb
---

# 통신 상태 모니터링 (SPI_Comm_St, BLE_Comm_St)

SPI 패킷의 시스템 상태 비트맵 (Header 0x10)에 포함된 통신 헬스체크 비트 두 개. 통신 단절 시 fault 처리하는 로직의 근거.

## SPI_Comm_St (Bit.5 of Buffer[0] in 0x10)

**원본 사양 (매뉴얼 260513)**:
- 무선모듈 ↔ [[rx_control]] 간 SPI 통신 상태 확인용
- 무선모듈이 200 ms마다 0과 1을 교번하여 비트를 갱신
- [[rx_control]]는 일정 시간 변화가 없으면 SPI 단절로 간주
- 통신 불량 시: 시스템 대기 → **Warning** / 출력 중 → **Fault 처리 + 출력 차단**
- ESB 전환 후에도 동일 로직 유지 예정 (SPI 구간은 그대로)

**구현 현황 (2026-06-01 기준)**:

| 항목 | 상태 | 비고 |
|------|------|------|
| 200ms 교번 비트 생성 (nRF) | ✓ 실보드 검증 | `Heartbeat_Loop()` millis 게이트, P0.17 오실로 Δt≈190ms |
| 5s 무변화 → SPI_FAIL 판정 (STM32) | ✓ 실보드 검증 | `SPI_HB_TIMEOUT_MS=5000`, `spi_proc()`, 케이블 분리 확인 |
| SPI_FAIL 전이 시 UART 경고 출력 | ✓ 실보드 검증 | `spi \| LINK DOWN` / `spi \| LINK UP` (edge trigger 1회). 커밋 `fe5bf14`, 2026-06-01 |
| Warning 플래그 set / 대기 상태 머신 | ✗ 미구현 | `rx_status.warning` 항상 0 송신 |
| Fault 플래그 set / 출력 중 상태 머신 | ✗ 미구현 | `rx_status.fault` 항상 0 송신 |
| PWM 출력 차단 (pwm_stop) | ✗ 미구현 | SPI_FAIL이 PWM 제어 경로와 미연결 |

> ⚠️ **오인 주의**: 위 사양("Warning/Fault+출력차단")은 아직 코드로 실현되지 않았다.
> 이번(fe5bf14)에 구현된 것은 "단절/복구 전이 시 UART 경고 출력"뿐이며,
> 그것도 의도적 단기 결정이다 — 상태 머신 설계 없이 최소 가시성 먼저.
> `rx_status.warning`/`.fault`는 죽은 필드(소비처 없음). [[spi_link_reliability]] 참조.

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
