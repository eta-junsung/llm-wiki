---
tags: [source, schematic, board, ble_module]
source: docs/Schematic/BLE_Module_Board_Ver0.1E00_260318 1.pdf
date: 2026-06-01
subsystem: 02_RX_ble
---

# BLE Module Board Ver0.1E00 회로도 (260318)

[[rx_ble_module]](nRF52832, `02_RX_ble`)의 실물 보드 설계 도면. 2026-06-01 실물 보드 입고.

## 원본

- **파일**: `docs/Schematic/BLE_Module_Board_Ver0.1E00_260318 1.pdf`
- **버전**: Ver0.1E00, 2026-03-18
- **형식**: PDF (OrCAD 계열 추정 — 미확인)

## 상태

- 실물 보드 입고: ✓ 2026-06-01
- 회로도 상세 ingest: ✗ 미완 — PDF 텍스트 추출 필요. SPI 커넥터 CN3 핀맵은 [[rx_ble_module]]에 기존 기록 있음

## 알려진 내용 (rx_ble_module에서 교차 확인)

| 커넥터 | 용도 |
|---|---|
| CN3 | SPI 통신 (STM32↔nRF52832, 4선, 10핀) |
| CN4 | 관리자 전원 (+5VDC 절연, 6핀) |

- nRF52832 SPI 핀: CS=P0.22, MISO=P0.26, MOSI=P0.25, SCK=P0.27

## 관련

- [[rx_ble_module]] — 모듈 entity (핀맵 포함)
- [[spi_packet_format]] — SPI wire 포맷
