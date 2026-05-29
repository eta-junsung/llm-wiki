---
date: 2026-05-29
---

# oled_tv_software — 구현 현황

## 다음 시작점

`tasks/spi-10ms`(가칭) 브랜치 분리 후, STM32 `01_RX_control`의 `HAL_SPI_MspInit`에 DMA IRQ(`HAL_NVIC_EnableIRQ`) 활성화 코드가 빠져 있는지 먼저 확인한다 — DMA 완료 콜백 미수신이 10ms 미동작의 유력 원인. 콜백 수신을 검증한 뒤 `PACKET_INTERVAL=10`(`_shared/oled_tv_protocol.h:45`) 상태로 STM32 리플래시하여 CS가 10ms 주기로 내려가는지 + `spi_fail_cnt` 추이를 측정한다.

## 구현 현황

### SPI 통신 — STM32(01_RX_control) ↔ nRF52832(02_RX_ble)

| 기능 | 상태 | 메모 |
|------|------|------|
| heartbeat 메커니즘 (3-MCU) | ✓ | RX_ble가 0x10 STATUS bit5(`TX_STATUS_BIT_SPI_COMM_ST`) 토글 → STM32 5s 타임아웃(`SPI_HB_TIMEOUT_MS`)으로 SPI 단절 감지. 오실로 200ms 토글 확인(`P3NOFO01.PNG`, Δt≈190ms) |
| heartbeat 200ms 독립 타이머 | ✓ | `Heartbeat_Loop()` millis 게이트로 분리, SPI 사이클 종속 제거. 오실로 검증 완료 |
| SPI 오류율 모니터 (ok/fail/err%) | △ | `Monitor_Loop()` 1초 윈도우 출력 추가, 장시간 추이 미확인 |
| STM32 spi_tx_busy 타임아웃 복구 | △ | DMA 콜백 미수신 시 50ms 타임아웃 후 `HAL_SPI_Abort()`로 CS 복구. 실보드 장시간 미검증 |
| TX_ble stack_temp 실데이터화 | △ | 더미 1234 → `tx_module.tx_data.stack_temp` 구조체 참조. 실측 값 확인 필요 |
| SPI 10ms 폴링 주기 | ✗ | `PACKET_INTERVAL=10` 반영했으나 실보드에서 CS 10ms 미동작. DMA IRQ(NVIC) 부재 의심 |
| STM32 SPI 클럭 9MHz 상향 | ✗ | 시도 후 revert(`7143f55`). nRF52832 SPIS 최대 SCK datasheet 선결 필요 |

### ESB — 02_RX_esb / 03_TX_esb

| 기능 | 상태 | 메모 |
|------|------|------|
| ESB TX 전송 (03_TX_esb) | △ | while(1) 구조 정리 완료, 실보드 연속 동작 확인 필요 |
| ESB RX 수신 (02_RX_esb) | △ | 수신 모니터링 추가, 실보드 연속 수신 확인 필요 |
| GPIO P0.17/P0.18 토글 (TX 주기 검증용) | △ | 오실로스코프 측정 완료 (920us), 제거 여부 결정 필요 |
| TX_FAILED 1초 윈도우 카운터 | △ | UART 출력 확인, 실보드 장시간 안정성 미확인 |
| RX/TX UART 모니터 출력 | △ | 포맷 정리 완료, 실보드 장시간 동작 미확인 |
| ESB TX→ACK latency | ✓ | 오실로스코프 측정: 약 470us |
| ESB TX 전송 주기 | ✓ | 오실로스코프 측정: 약 920us |
| ESB ACK 수신 주기 | ✓ | 오실로스코프 측정: 약 940us |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현

## 미결 사항

- SPI 10ms 폴링 미동작 원인 규명 — STM32 DMA IRQ(`HAL_NVIC_EnableIRQ`) 활성화 여부 (선결)
- nRF52832 SPIS 최대 SCK 클럭 datasheet 미ingest — 9MHz 상향 재시도 전 선결
- SPI 오류율 모니터 / spi_tx_busy 타임아웃 복구 실보드 장시간 안정성 검증
- TX_ble stack_temp 실측 값 정상 여부 확인
- (ESB) 실보드 장시간 안정성, GPIO 토글 핀 제거 여부, 01_RX_control ↔ 02_RX_esb UART 브리지 동작 확인
