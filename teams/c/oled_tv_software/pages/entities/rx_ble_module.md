---
tags: [entity, board, ble_module, historical, ble]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__introduction.CSV
date: 2026-05-28
subsystem: 02_RX_esb
---

# Rx BLE 모듈 (BLE 시절, 02_RX_esb)

[[rx_control]](Master)과 SPI로 연결되어 무선 구간을 처리하는 슬레이브 모듈. 작성 당시 BLE 기반이며 추후 ESB로 교체 예정 → 본 페이지는 **BLE 시절 사양** 기록 (`02_RX_esb` 서브프로젝트로 이어짐).

## 역할

- SPI Slave (CS low active)
- Tx 측 무선모듈과 BLE로 페어링하여 데이터 송수신
- 수신된 Tx 데이터를 SPI 패킷 (0x10/0x11/0x12)으로 [[rx_control]]에 전달
- [[rx_control]]로부터 받은 SPI 패킷 (0x50/0x51/0x52)을 무선으로 Tx 측에 전달
- 자체적으로 [[comm_state_monitoring|SPI/BLE 통신 상태]] 비트를 생성·갱신
- SPI heartbeat 생성: `Heartbeat_Loop()`(main.c:494)가 200ms마다 `hb_bit` 토글 → 0x10 STATUS bit5. 디버그 핀 `P0.17`(`PIN_DBG_HB`)로 오실로 검증. 상세 → [[spi_link_reliability]]

## 인터페이스

### CN3 / CN2 — SPI 통신용 커넥터

> 프로토콜 매뉴얼은 CN3, 회로도 실크는 **CN2** (HEADER_1.27mm/10P). 실물 보드에서 CN2로 확인할 것.

| Pin | 신호 | nRF52 GPIO |
|---|---|---|
| 1, 2 | +3.3 VDC (비절연 전원) | — |
| 3 | SPI CS (Low Active) | **P0.22** (`PIN_SPI_NSS`) |
| 4 | N.C | — |
| 5 | SPI MISO (S→M) | **P0.26** (`PIN_SPI_MISO`) |
| 6 | N.C | — |
| 7 | SPI MOSI (M→S) | **P0.25** (`PIN_SPI_MOSI`) |
| 8 | SPI Clock (Master 생성) | **P0.27** (`PIN_SPI_SCK`) |
| 9, 10 | GND (비절연) | — |

- 4선 SPI, **9.0 Mbps**, Byte order Motorola (big-endian)
- nRF 페리: **SPIS1** 인스턴스 (`NRF_DRV_SPIS_INSTANCE(1)`)
- 모드: **`NRF_SPIS_MODE_2`** = CPOL=1, CPHA=0. Master([[rx_control]] SPI2)와 정합.
- 핀 정의 출처: `_shared/oled_tv_protocol.h:69-72` — `PIN_SPI_NSS/MISO/MOSI/SCK = 22/26/25/27`
- 드라이버: `nrf_drv_spis` 더블 버퍼 (RX 버퍼 = `tx_module_data_t`, TX 버퍼 = `rx_module_data_t`. 명칭이 "어디서 오는가" 기준이라 SPIS의 RX/TX와 반대)

### CN4 / CN1 — 전원 커넥터

> 프로토콜 매뉴얼은 CN4, 회로도 실크는 **CN1** (HEADER_1.27mm/6P). 실물 보드에서 CN1로 확인할 것.

| Pin | 신호 |
|---|---|
| 1, 2, 3 | +5 VDC (절연 전원, COMM_P5V) |
| 4, 5, 6 | GND (절연, COMM_GND) |

### CON1 — SWD 프로그래밍/디버그

| 항목 | 내용 |
|---|---|
| 커넥터 | SMAW250-05 (2.5mm 5핀) / 대체품 MOLEX 22-05-7055 |
| 신호 | SWDCLK, SWDIO, nRST(D1 보호 다이오드 경유), BLE_P3V3, GND |
| 비고 | ST-LINK V2 + OpenOCD/pyOCD로 플래싱 가능. nrfjprog는 J-Link 전용이라 불가 |

### CON2 — UART 모니터링 (절연형)

| 항목 | 내용 |
|---|---|
| 커넥터 | SMAW250-04 (2.5mm 4핀) / 대체품 MOLEX 22-05-7045 |
| 신호 | TXD_uC, RXD_uC (ISO6721RBDR 절연), COMM_P5V, COMM_GND |
| 비고 | PC 모니터링 전용. 절연형이라 COMM 전원(5V) 별도 공급 필요 |

## 펌웨어 현황 (PRD v1.0 기준)

| 항목 | 상태 |
|---|---|
| ESB PRX 기본 동작 | ✓ 구현됨 |
| SPI Slave 수신/송신 | ✓ 구현됨 |
| 버그 수정 (커밋 `89e8609`) | ✓ 완료 |
| ESB 타임아웃 stale 마킹 | ✗ 미구현 (`esb_recv` 끊길 때 `tx_module.hdr=0x00`으로 STM32에 알리는 로직 없음) |
| SPI 하드웨어 테스트 | ✗ 미실시 (코드 수정 후 실측 검증 전) |
| ESB 수신 모니터링 추가 | △ 구현됨·미검증 |
| RX UART 모니터 출력 포맷 개선 | △ 구현됨·미검증 |
| SPI heartbeat (200ms 독립 타이머) | ✓ 실보드 검증 (P0.17 오실로, 260529) |
| SPI 오류율 모니터 (ok/fail/err%) | △ 구현됨·장시간 미검증 (260529) |
| SPI 10ms 폴링 주기 | ✓ 실보드 검증 (CS Δt=10ms 오실로, ok=4799/49s, crcfail=0, 2026-06-01) |

## ESB 타이밍 측정값

2026-05-27 오실로스코프 실측 (PTX 측 GPIO 프로브). 상세 이미지 → [[esb_timing_measurements]].

| 항목 | 측정값 |
|---|---|
| ACK 수신 주기 (PRX 응답 주기) | 약 940 us |

## 통신 페어

- 상위(Master): [[rx_control]]
- STM32-nRF 내부 SPI 프레임: [[spi_packet_format]] (56B/45B, HDR 0xC0)
- ESB wire 패킷: [[esb_packet_format]] (11B, HDR round-robin)
- 방향별 페이로드: [[tx_to_rx_packets]], [[rx_to_tx_packets]]
- 헬스체크 비트: [[comm_state_monitoring]]
- SPI 링크 안정성(heartbeat 구현·복구): [[spi_link_reliability]]
- ESB 상대방: [[tx_ble_module]] (PTX)

## 이행 메모 (BLE → ESB)

- 본 모듈은 ESB로 교체 예정 (`02_RX_esb`)
- SPI 패킷 구조와 핀맵은 유지 가정
- `BLE_Comm_St` 비트는 명칭/거동 재정의 가능성 — [[comm_state_monitoring]] 참조

## 물리 보드

| 항목 | 내용 |
|---|---|
| 보드명 | BLE_Module_Board_Ver0.1E00 |
| MCU 모듈 | UTO-NBL-52 (nRF52832 기반) |
| 회로도 | `docs/Schematic/BLE_Module_Board_Ver0.1E00_260318 1.pdf` ([[schematic_ble_module_board_v01e00]]) |
| 보드 크기 | 35mm × 35mm 이하 |
| 실물 입고 | 2026-06-01 |
| 비고 | 명칭은 BLE 시절 잔재, 현재 ESB 펌웨어(`02_RX_ble`) 탑재 대상 |

## 출처

- [[spi_protocol_manual_260513]]
- [[schematic_ble_module_board_v01e00]]
