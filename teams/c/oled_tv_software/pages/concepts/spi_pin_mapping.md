---
tags: [concept, spi, pinmap, wiring]
source: schematic_stm32_mini_pro_v10 + rx_ble_module + DK 실측 2026-06-16 + 04_tx_control Nucleo 실측 2026-06-17
date: 2026-06-17
subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble, 04_tx_control
---

# STM32↔nRF52 SPI 배선 핀맵

SPI 링크별 물리 배선 대응표. 현재 두 링크 존재: **01↔02 링크**(RX 사이드), **04↔03 링크**(TX 사이드).

## 01↔02 링크 — 01_RX_control(STM32 Mini Pro) ↔ 02_RX_ble(PCA10040 또는 BLE_Module_Board)

DK 보드 배선 2026-06-16 실측 확인. 출처: [[schematic_stm32_mini_pro_v10]], [[rx_ble_module]].

| 신호 | STM32 핀 (01_RX_control) | nRF52832 핀 (02_RX_ble) | 비고 |
|---|---|---|---|
| SCK | **PB13** | **P0.27** | SPI2_SCK |
| MOSI (STM32→nRF) | **PB15** | **P0.25** | |
| MISO (nRF→STM32) | **PB14** | **P0.26** | ⚠️ 미연결 시 spi_rx_pkt 전부 `0xFF` |
| CS (NSS) | **PB12** | **P0.22** | SW 토글 (SPI_NSS_SOFT), active LOW |

SPI 파라미터: MODE_2 (CPOL=1, CPHA=0), **8 Mbps** (PCLK1=32 MHz, prescaler=/4, HSI 64 MHz 기준), 8-bit, MSB-first. → [[sysclk_hsi_transition]], [[rx_control]]

## 04↔03 링크 — 04_tx_control(NUCLEO-F103RB) ↔ 03_TX_ble(PCA10040 DK)

2026-06-17 실측 확인 (커밋 `47e46db`). 신호 정의는 01↔02 링크와 동일 스펙(MODE_2, 8 Mbps, SPI2, NSS_SOFT).

| 신호 | 04 NUCLEO-F103RB (morpho 실크) | 03 PCA10040 (P4 헤더 실크) | 비고 |
|---|---|---|---|
| SCK | **PB13** | **P0.27** | |
| MOSI (STM32→nRF) | **PB15** | **P0.25** | |
| MISO (nRF→STM32) | **PB14** | **P0.26** | ⚠️ 미연결 시 04 수신 전부 0xFF → 패킷 드롭 → rx_mask 0x00 고착 |
| CS (NSS) | **PB12** | **P0.22** | active LOW |
| GND | morpho/Arduino GND | P4 내 GND | |

**03측 배선 포인트**: 4신호 + GND가 PCA10040 **P4 헤더 한 곳**에 집중 — 실크(P0.xx) 직독 가능. 출처: nRF52 DK User Guide p.15 Figure 10, `_external/nRF5_SDK_17/components/boards/pca10040.h`.

**04측 배선 포인트**: Nucleo morpho 커넥터에서 PBxx 실크 직독. CN10 핀번호: **CN10-16(PB12/CS) / CN10-26(PB15/MOSI) / CN10-28(PB14/MISO) / CN10-30(PB13/SCK)** — 이미지 직독 확인 (2026-06-18). 전체 핀맵 → [[nucleo_f103rb_morpho_pinmap]].

**⚠️ UART 주의**: 04는 STM32F103RBT6(medium-density)라 **UART4/UART5 없음**. 모니터는 USART2(PA2=TX, PA3=RX) 사용 — Nucleo VCP(ST-LINK USB)에 기본 연결.

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
