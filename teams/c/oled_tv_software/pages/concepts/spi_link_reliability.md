---
tags: [concept, spi, heartbeat, comm_health, esb]
source: teams/c/oled_tv_software/pages/sources/spi_heartbeat_report_260529.md
date: 2026-06-10
subsystem: 01_RX_control, 02_RX_ble
---

# SPI 링크 안정성 (heartbeat · 오류율 · 타임아웃 복구)

[[rx_control]](STM32, Master) ↔ [[rx_ble_module]](nRF52832, Slave) SPI 버스의 단절 감지·복구·모니터링 메커니즘. 통신 상태 비트 사양은 [[comm_state_monitoring]], wire 포맷은 [[spi_packet_format]] 참조. 본 페이지는 **구현·검증 현황** 중심.

## heartbeat (SPI 단절 감지)

매뉴얼 260513 사양인 SPI_Comm_St 200ms 교번을 코드로 실현한 것. ESB 전환 후에도 SPI 구간은 동일. 심볼명은 커밋 `e5e3efc`(2026-06-08)에서 `hb_*`→`spi_comm_st_*`로 3종 펌웨어 통일 — 매핑 표 [[comm_state_monitoring]] "심볼·네이밍 컨벤션".

| 단계 | 위치 | 내용 |
|---|---|---|
| 비트 정의 | `_shared/oled_tv_protocol.h` | `COMM_ST_BIT_SPI = 5` (0x10 Data[0] bit5). 구 `TX_STATUS_BIT_SPI_COMM_ST` |
| 토글 생성 | `02_RX_ble` `SpiCommSt_Loop()` | millis 200ms 게이트로 `spi_comm_st_bit ^= 1u` (SPI 사이클과 독립) |
| 패킷 적재 | `02_RX_ble` `SPI_Loop` | **나가는 SPI 송신 복사본 `spi_tx_pkt`에 송신 직전 stamp** — 공유 RX 버퍼 `esb_pkt[0]` 아님(race). `build_tx_pkt()`도 아님. race-free 근거 → [[comm_state_monitoring]] "race-free stamp" |
| 변화 감지 | `01_RX_control` `app_protocol.c`(구 `common.c`) | bit5 변화 시 `spi_comm_st_last_change` 갱신 (`apply_rx_pkt`) |
| 단절 판정 | `01_RX_control` `app_protocol.c` `exchange_packets()` | `d2232fe`부터 `SPI_COMM_ST_WINDOW_MS=1000`(구 `..._TIMEOUT_MS=5000`) 초과 무변화 → `spi_status=SPI_FAIL`. **이제 `spi_status`는 LINK(토글 타임아웃) 전용** |
| 링크 상태 표시 | `01_RX_control` `app_protocol.c` `print_packets()` | **`35b94d0`: COMM 텍스트 라인 제거** — monitor가 바이너리로 전환되며 `spi_status`(SPI_Comm_St)는 **0x10 status 패킷 d0 bit5**에 실려 host로 운반된다. (연혁: `9be1a7a` `spi\|LINK DOWN/UP` 제거 → `2f2aa65` COMM 텍스트 라인 edge 출력 → `35b94d0` 텍스트 라인 자체 폐기.) `spi_status`는 `d2232fe`부터 LINK 전용(토글 타임아웃) → [[comm_state_monitoring]] "monitor 바이너리 전환". (적출 경위 [[app_protocol_module]], host [[pc_uart_gui]]) |
| LED2 mirror | `03_TX_ble` (custom board) | LED2(P0.08)가 `spi_comm_st_bit` 값을 미러 — [[tx_ble_module]] |

- **200ms 독립화의 의미**: 토글이 SPI 사이클에 종속되지 않으므로, SPI 폴링 주기(PACKET_INTERVAL)를 바꿔도 heartbeat 거동은 불변. STM32는 "토글 주기"가 아니라 "마지막 변화 시각"으로 판정하므로 토글 주기에 무관하게 동작.
- **heartbeat 검증**: RX_ble `P0.17`(`PIN_DBG_HB`) GPIO 토글 오실로 측정 — Δt≈190ms (≈200ms), `P3NOFO01.PNG`. 실보드 검증 완료.
- **LINK DOWN/UP 검증 (historical)**: 실보드, SPI 케이블 분리 시 `LINK DOWN`/재연결 시 `LINK UP` 1회 UART 확인 (2026-06-01, `fe5bf14`). **이 텍스트 출력은 `9be1a7a`→`35b94d0`을 거쳐 완전 제거** — 링크 상태는 이제 0x10 status 패킷 d0 bit5(SPI)/bit6(ESB) 바이너리로 운반, host([[pc_uart_gui]])가 `Link: SPI/ESB [UP/DOWN]`으로 표시.
- **단절 후속 응답 구현 상태**: 링크 상태 가시화는 0x10 d0 bit5/6 바이너리 운반으로 일원화(COMM 텍스트 라인 폐기, `35b94d0`). Warning/Fault 플래그·PWM 차단·상태 머신은 ✗ 미구현. 상세 → [[comm_state_monitoring]].

## SPI 오류율 모니터 / CRC 카운터 — 전부 제거됨 (`9be1a7a`→`2f2aa65`)

구 구현: `01_RX_control common.c`에 누적 카운터(`spi_ok_cnt`/`spi_crc_fail_cnt`) + `Monitor_Loop()` UART 출력(`spi | ok=4799 crcfail=0 | /s ok=100 ... failrate=0%`). 49s 실보드 확인(ok=4799, crcfail=0).

- **`9be1a7a`**: `spi_ok_cnt`·`monitor_spi_diag` 죽은 코드 삭제 → CRC 헬스는 COMM 라인 CRC 자리(1초 윈도우 `spi_crc_fail_cnt` delta)로 임시 잔존.
- **`2f2aa65`**: COMM 라인이 링크 전용으로 단순화되며 **CRC 표시처와 `spi_crc_fail_cnt` 카운터까지 모두 제거**. CRC fail은 이제 어디에도 집계·표시되지 않고 **깨진 패킷 드롭(`if (ok) apply_rx_pkt`)만** 한다 — 재요청·fault·플래그 없음. 데이터 무결성(체크섬 검증+드롭)은 유지. ([[comm_state_monitoring]] "spi_status LINK/CRC 분리", [[app_protocol_module]])

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
- ⚠️ **주기 용어 구분**: 이 10ms는 **앱 SPI 폴링 주기(`PACKET_INTERVAL`)**. ESB RF wire 주기와 별개 — ESB는 `ESB_TX_INTERVAL_MS=1ms`(0x10 3종 round-robin이라 헤더당 실효 ~3ms, 전 헤더 합산 ~1000/s). [[esb_link_layer]]·[[esb_packet_format]] 참조. (구 wiki의 "ESB 10ms"는 이 SPI 폴링값과 혼동된 오기 — 정정됨)

## 미달 — STM32 SPI 9MHz 클럭 상향 (✗)

- 시도 후 revert(`7143f55`). 프로토콜 매뉴얼 사양 9.0Mbps([[spi_packet_format]])에 미달.
- **현재 실동작 속도**: **8.0 Mbps** — 정본 코드베이스 prescaler=/4, PCLK1=32 MHz(HSI 64MHz 기반 APB1). 구 dev revert 이후는 prescaler=/8 → 4 Mbps였음. → [[sysclk_hsi_transition]]
- **선결**: nRF52832 SPIS 최대 SCK 클럭 datasheet ingest 후 재시도.

## 관련

- [[comm_state_monitoring]] — SPI_Comm_St / BLE_Comm_St 비트 사양·fault 거동
- [[spi_packet_format]] — SPI wire 포맷·전송 파라미터 사양
- [[spi_heartbeat_report_260529]] — heartbeat 작업 보고서 (10ms 미달 기록)
- [[spi_10ms_diagnosis_report_260601]] — 10ms 폴링 진단 보고서 (미달 반증·✓ 확정)
- [[rx_ble_module]] — heartbeat 생성 측 모듈
