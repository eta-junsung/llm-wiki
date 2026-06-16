---
tags: [concept, spi, pinmap, wiring]
source: schematic_stm32_mini_pro_v10 + rx_ble_module + DK 실측 2026-06-16
date: 2026-06-16
subsystem: 01_RX_control, 02_RX_ble
---

# STM32↔nRF52 SPI 배선 핀맵

01_RX_control(STM32 Mini Pro)과 02_RX_ble(nRF52832 PCA10040 또는 회사 BLE_Module_Board) 사이의 SPI2 물리 배선 대응표. DK 보드 배선은 2026-06-16 실측 확인.

## 핀 대응표

| 신호 | STM32 핀 (01_RX_control) | nRF52832 핀 (02_RX_ble) | 비고 |
|---|---|---|---|
| SCK | **PB13** | **P0.27** | SPI2_SCK |
| MOSI (STM32→nRF) | **PB15** | **P0.25** | |
| MISO (nRF→STM32) | **PB14** | **P0.26** | ⚠️ 미연결 시 spi_rx_pkt 전부 `0xFF` |
| CS (NSS) | **PB12** | **P0.22** | SW 토글 (SPI_NSS_SOFT), active LOW |

SPI 파라미터: MODE_2 (CPOL=1, CPHA=0), **8 Mbps** (PCLK1=32 MHz, prescaler=/4, HSI 64 MHz 기준), 8-bit, MSB-first. → [[sysclk_hsi_transition]], [[rx_control]]

## MISO 미연결 증상 — spi_rx_pkt 전부 0xFF

MISO 라인(PB14↔P0.26)이 물리적으로 미연결이면:

1. STM32 SPI2 MISO 라인이 pull-up 상태 유지 → 수신 바이트 전부 `0xFF`
2. `spi_rx_pkt`(11B) 전 필드 `0xFF` → XOR 체크섬 불일치 → **패킷 드롭** (`exchange_packets()` ok=false)
3. 01_RX_control이 유효 0x10 패킷을 받지 못함 → heartbeat 토글 bit5가 갱신 안 됨
4. `SPI_COMM_ST_WINDOW_MS`(1000ms) 초과 → **SPI_Comm_St DOWN** (GUI `Link: SPI DOWN`)

→ SpiCommSt DOWN 발생 시 MISO 배선(PB14↔P0.26)을 **가장 먼저** 점검. 진단 전체 경로는 [[comm_state_monitoring]] "SpiCommSt DOWN 진단 경로".

## 관련

- [[rx_control]] — SPI2 페리 설정 (MODE_2, prescaler=/4, DMA, NSS_SOFT)
- [[rx_ble_module]] — nRF52 SPIS1 핀 설정 (P0.22/25/26/27)
- [[spi_packet_format]] — 11B wire 포맷·체크섬 (드롭 조건)
- [[comm_state_monitoring]] — SpiCommSt 판정·DOWN 진단 경로
- [[sysclk_hsi_transition]] — HSI 64 MHz 기준 PCLK1=32 MHz, SPI 8 Mbps
- [[schematic_stm32_mini_pro_v10]] — STM32 Mini Pro 회로도 (SPI 핀 원출처)
