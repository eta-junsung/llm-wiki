---
tags: [concept, spi, heartbeat, comm_health, esb]
source: teams/c/oled_tv_software/pages/sources/spi_heartbeat_report_260529.md
date: 2026-05-29
subsystem: 01_RX_control, 02_RX_ble
---

# SPI 링크 안정성 (heartbeat · 오류율 · 타임아웃 복구)

[[rx_control]](STM32, Master) ↔ [[rx_ble_module]](nRF52832, Slave) SPI 버스의 단절 감지·복구·모니터링 메커니즘. 통신 상태 비트 사양은 [[comm_state_monitoring]], wire 포맷은 [[spi_packet_format]] 참조. 본 페이지는 **구현·검증 현황** 중심.

## heartbeat (SPI 단절 감지)

매뉴얼 260513 사양인 SPI_Comm_St 200ms 교번을 코드로 실현한 것. ESB 전환 후에도 SPI 구간은 동일.

| 단계 | 위치 | 내용 |
|---|---|---|
| 비트 정의 | `_shared/oled_tv_protocol.h:255` | `TX_STATUS_BIT_SPI_COMM_ST = 5` (0x10 STATUS bit5) |
| 토글 생성 | `02_RX_ble/Application/main.c:494` `Heartbeat_Loop()` | millis 200ms 게이트로 `hb_bit ^= 1u` (SPI 사이클과 독립) |
| 패킷 적재 | `02_RX_ble/Application/main.c:154` `build_tx_pkt()` case 0 | `hb_bit`를 0x10 STATUS bit5에 실어 STM32로 |
| 변화 감지 | `01_RX_control/Application/Src/common.c:117~127` | hb 비트 변화 시 `hb_last_change` 갱신 |
| 단절 판정 | `01_RX_control/Application/Src/common.c:181~184` | `SPI_HB_TIMEOUT_MS=5000` 초과 무변화 → `spi_status=SPI_FAIL` |

- **200ms 독립화의 의미**: 토글이 SPI 사이클에 종속되지 않으므로, SPI 폴링 주기(PACKET_INTERVAL)를 바꿔도 heartbeat 거동은 불변. STM32는 "토글 주기"가 아니라 "마지막 변화 시각"으로 판정하므로 토글 주기에 무관하게 동작.
- **검증**: RX_ble `P0.17`(`PIN_DBG_HB`) GPIO 토글 오실로 측정 — Δt≈190ms (≈200ms), `P3NOFO01.PNG`. **실보드 검증 완료**.
- 단절 시 거동(Warning/Fault+출력차단)은 [[comm_state_monitoring]] 참조.

## SPI 오류율 모니터 (△ 49s 검증, 장시간 미확인)

`01_RX_control common.c:165-185`에 누적 카운터(`spi_ok_cnt` / `spi_crc_fail_cnt`, CRC 이벤트 기반, timeout fail 제외) 추가. `Monitor_Loop()` UART 출력: 누적 + 초당 delta + failrate%.

- 출력 형식: `spi | ok=4799 crcfail=0 | /s ok=100 crcfail=0 failrate=0%`
- 49s 실보드 확인 (ok=4799, crcfail=0, /s ok=100). 장시간 안정성 미확인

## spi_tx_busy 타임아웃 복구 (코드, 장시간 미검증)

- **문제**: DMA 완료 콜백 미수신 시 STM32 `spi_tx_busy=true` 영구 잠금 → CS가 안 내려가 통신 정지.
- **수정**: `SPI_TX_BUSY_TIMEOUT_MS=50ms` 초과 시 `HAL_SPI_Abort()`로 강제 해제·CS 복구. `01_RX_control/Application/Src/app_spi.c:117~` (커밋 `4852f4e`).
- ⚠️ 이건 증상 완화책. 근본 원인(DMA 콜백이 왜 산발적으로 안 오는가)은 미확인.

## SPI 10ms 폴링 주기 (✓ 실보드 검증)

`PACKET_INTERVAL=10`(`_shared/oled_tv_protocol.h:45`)으로 초당 100 트랜잭션 동작 확인. "미동작"의 실제 원인은 동작 결함이 아닌 **관측 도구 한계** — 기존 `rx_status.spi_status` 단일 필드가 매 수신마다 덮어써져 산발 패턴이 보이지 않았던 것.

- UART: `spi | ok=4799 crcfail=0 | /s ok=100 crcfail=0 failrate=0%` (49s 측정)
- 오실로: CS(STM32 PB12) active-low Δt=10ms, 1/Δt=100Hz, Vpp=3.79V (`assets/spi_cs_10ms_260601.png`)
- DMA IRQ NVIC: `MX_DMA_Init()`(`app_dma.c:15-19`) 정상 존재 — `MspInit` 부재 가설 반증
- 진단 경과: [[spi_10ms_diagnosis_report_260601]]
- ⚠️ **주기 용어 구분**: 이 10ms는 **앱 SPI 폴링 주기(PACKET_INTERVAL)**. [[esb_packet_format]]·[[esb_link_layer]]의 10ms는 ESB RF wire 주기로 별개.

## 미달 — STM32 SPI 9MHz 클럭 상향 (✗)

- 시도 후 revert(`7143f55`). 현재 SPI는 사양 9.0Mbps([[spi_packet_format]])에 미달한 클럭으로 동작.
- **선결**: nRF52832 SPIS 최대 SCK 클럭 datasheet ingest 후 재시도.

## 관련

- [[comm_state_monitoring]] — SPI_Comm_St / BLE_Comm_St 비트 사양·fault 거동
- [[spi_packet_format]] — SPI wire 포맷·전송 파라미터 사양
- [[spi_heartbeat_report_260529]] — heartbeat 작업 보고서 (10ms 미달 기록)
- [[spi_10ms_diagnosis_report_260601]] — 10ms 폴링 진단 보고서 (미달 반증·✓ 확정)
- [[rx_ble_module]] — heartbeat 생성 측 모듈
