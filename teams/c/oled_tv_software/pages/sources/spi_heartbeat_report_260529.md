---
tags: [source, esb, spi, heartbeat, comm_health]
source: tasks/spi-heartbeat/report.md
date: 2026-05-29
subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
---

# SPI heartbeat 작업 보고서 (260529)

STM32([[rx_control]]) ↔ nRF52832([[rx_ble_module]]) 간 SPI 통신 안정성 확보 작업. 브랜치 `tasks/spi-heartbeat` → `esb` 머지(`0294ece`). heartbeat 메커니즘 실보드 검증 완료, SPI 10ms 폴링·9MHz 상향은 미달.

## 파생 페이지

- [[spi_link_reliability]] — heartbeat 구현·SPI 오류율 모니터·spi_tx_busy 타임아웃 복구·10ms 폴링/9MHz 현황 (신규)
- [[comm_state_monitoring]] — SPI_Comm_St bit5 사양이 코드(200ms 독립 타이머)로 실현됨 확정
- [[spi_packet_format]] — 사양 "10ms / 9Mbps" vs 실측 현황 주석 추가
- [[rx_ble_module]] — Heartbeat_Loop·P0.17 디버그 핀·펌웨어 현황 갱신

## 완료 (실보드 검증)

- **heartbeat 메커니즘 (3-MCU)**: RX_ble가 0x10 STATUS 패킷 bit5(`TX_STATUS_BIT_SPI_COMM_ST=5`, `_shared/oled_tv_protocol.h:255`) 토글 → STM32가 변화 시각 기반 5초 타임아웃(`SPI_HB_TIMEOUT_MS=5000`)으로 SPI 단절 감지.
- **200ms 독립 타이머**: 기존 `build_tx_pkt()` case 0 내 매 SPI 사이클 토글 → `Heartbeat_Loop()`(`02_RX_ble/Application/main.c:494`, millis 200ms 게이트, `hb_bit ^= 1u`)로 분리. 이로써 매뉴얼 260513 사양(200ms 교번)을 코드가 처음으로 충족.
- **실보드 검증**: RX_ble `P0.17`(`PIN_DBG_HB`)에서 GPIO 토글 오실로스코프 측정. 스크린샷 `tasks/spi-heartbeat/P3NOFO01.PNG` — Δt≈190ms, 1/Δt≈5.26Hz, Vpp 2.79V (≈200ms 주기 일치).

## 완료 (코드, 실보드 장시간 미검증)

- **SPI 오류율 모니터**: `02_RX_ble Monitor_Loop()` 출력에 `ok=%u/sec err=%u.%u%%` 추가. `spi_ok_cnt`/`spi_fail_cnt` 1초 윈도우 카운터. 예: `SPI hdr=0x50 fail=0/sec ok=100/sec err=0.0%`.
- **STM32 spi_tx_busy 타임아웃 복구**: DMA 완료 콜백 미수신 시 `spi_tx_busy=true` 영구 잠금 → CS가 안 내려가는 문제. `SPI_TX_BUSY_TIMEOUT_MS=50ms` 후 `HAL_SPI_Abort()`로 CS 복구 (`01_RX_control/Application/Src/app_spi.c:117~`). 커밋 `4852f4e`.
- **TX_ble stack_temp 실데이터화**: `03_TX_ble/Application/main.c:249` 더미 `1234` → `(int16_t)(tx_module.tx_data.stack_temp * 10.0f)` 구조체 참조.

## 미달 (다음 작업)

- **SPI 10ms 폴링 주기 (✗)**: `PACKET_INTERVAL` 1000 → 10ms 변경(`_shared/oled_tv_protocol.h:45`)했으나 실보드에서 CS가 10ms마다 안 내려감. `spi_tx_busy` 타임아웃 수정만으로 해결 안 됨. **유력 원인: `HAL_SPI_MspInit`에 DMA IRQ(`HAL_NVIC_EnableIRQ`) 활성화 부재 → DMA 완료 콜백이 절대 안 불림.** STM32 리플래시 필요.
  - ⚠️ 주의: 이 10ms는 **앱 SPI 폴링 주기(PACKET_INTERVAL)**다. [[esb_packet_format]]·[[esb_link_layer]]의 "10ms"는 ESB RF wire 주기로 별개 ([[spi_debug_log_report_260529]] 미결 참조).
- **STM32 SPI 클럭 9MHz 상향 (✗)**: 시도(`ee4fc8c`) 후 revert(`7143f55`). nRF52832 SPIS 최대 SCK 클럭 datasheet 미ingest — 재시도 전 선결.
- **다음 시작점**: `tasks/spi-10ms`(가칭) 분리 → DMA IRQ(NVIC) 확인 → 콜백 수신 검증 → CS 10ms 동작·`spi_fail_cnt` 추이 측정.

## 출처

- `tasks/spi-heartbeat/report.md`, 커밋 `b62f4c1`/`fd565e3`/`4852f4e`/`7143f55`/`9b15d34`/`0294ece`
- 오실로 스크린샷 `tasks/spi-heartbeat/P3NOFO01.PNG`
