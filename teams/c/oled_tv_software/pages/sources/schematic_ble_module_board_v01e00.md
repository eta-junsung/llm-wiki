---
tags: [source, schematic, board, ble_module]
source: docs/Schematic/BLE_Module_Board_Ver0.1E00_260318 1.pdf
date: 2026-06-02
subsystem: 02_RX_ble
---

# BLE Module Board Ver0.1E00 회로도 (260318)

[[rx_ble_module]](nRF52832, `02_RX_ble`)의 실물 보드 설계 도면. 2026-06-01 실물 보드 입고.

## 원본

- **파일**: `C:\Users\echog\eta\projects\c\oled_tv_software\docs\Schematic\BLE_Module_Board_Ver0.1E00_260318 1.pdf`
- **버전**: Ver0.1E00, 2026-03-18
- **설계자**: Hyun-Min,Lee / 승인: T.D.YEO
- **모델**: OLED700 WPT
- **총 4시트** (표지, 회로도, 부품배치도, 설계참조)
- **보드 크기**: 35mm × 35mm 이하

## 상태

- 실물 보드 입고: ✓ 2026-06-01
- 회로도 상세 ingest: ✓ 완료 (2026-06-02)

---

## MCU 모듈

**U1: UTO-NBL-52** (nRF52832 기반 모듈, 39핀 + A1)

| 핀 | 신호 | 비고 |
|---|---|---|
| 1 | SWDCLK | SWD 전용 |
| 2 | SWDIO | SWD 전용 |
| 3 | P0.21/RESET | nRST |
| 9 | VCC | 3.3V |
| 23 | P0.27 | SPI_CLK_uC |
| 25 | P0.25 | SPI_MOSI_uC |
| 26 | P0.26 | SPI_MISO_uC |
| 27 | P0.22 | SPI_nCS_uC |
| 29, 31, 39 | GND | — |
| 30 | ANT | ANT_uC (패턴 안테나) |
| 34 | P0.17 | (펌웨어: PIN_DBG_HB) |

ADC 가용 핀: P0.02/AIN0, P0.03/AIN1, P0.04/AIN2, P0.05/AIN3, P0.28/AIN4, P0.29/AIN5, P0.30/AIN6, P0.31/AIN7

---

## 커넥터 전체 목록

> **주의**: 프로토콜 매뉴얼(source: [[spi_protocol_manual_260513]])은 CN3(SPI), CN4(전원)로 표기하나,
> **회로도·실물 실크에는 CN2(SPI), CN1(전원)** 으로 되어 있어 번호가 다르다.

### CON1 — SWD 프로그래밍/디버그 ★

| 항목 | 내용 |
|---|---|
| 커넥터 | SMAW250-05 (2.5mm pitch, 5핀) |
| 대체품 | MOLEX 22-05-7055 (KK 2.5mm 5핀) |
| 용도 | SWD 프로그래밍·디버그 (`(연결@SWD)`) |

신호 (5핀, 핀 번호는 실물 실크스크린에서 Pin1 마킹 확인 필요):

| 신호 | nRF52832 |
|---|---|
| BLE_P3V3 | VCC (3.3V) |
| BLE_GND | GND |
| SWDCLK_uC | SWDCLK (전용 핀) |
| SWDIO_uC | SWDIO (전용 핀) |
| SWD_nRST | P0.21/RESET (D1 보호 다이오드 경유) |

- D1 (SMD220PL-TP/SOD-123FL): nRST 라인 보호 다이오드
- SW1 (ITS-1107/SMD): 시스템 리셋 버튼 (BLE_GND로 풀다운)

**ST-LINK V2 연결 방법**: SWDIO → ST-LINK 핀7, SWDCLK → ST-LINK 핀9, GND → ST-LINK 핀8, nRST → ST-LINK 핀15(선택). VCC는 보드 자체 전원 사용 시 연결 불요. [[플래싱 가이드|st_link_nrf52_flash]] 참고.

---

### CN2 — SPI 통신 (Board-to-Board @Rx Control Board)

| 항목 | 내용 |
|---|---|
| 커넥터 | HEADER_1.27mm/10P (10핀, Straight Type) |
| 용도 | STM32(Rx Control Board) ↔ nRF52832 SPI 통신 |
| 프로토콜 매뉴얼 표기 | CN3 |

| 핀 | 신호 | nRF52 GPIO |
|---|---|---|
| (확인 필요) | +3.3 VDC (비절연) = PD3V3 | — |
| (확인 필요) | GND = DGND | — |
| (확인 필요) | SPI_nCS_uC | P0.22 |
| (확인 필요) | SPI_MISO_uC | P0.26 |
| (확인 필요) | SPI_MOSI_uC | P0.25 |
| (확인 필요) | SPI_CLK_uC | P0.27 |

핀별 순서는 실물 핀맵([[rx_ble_module]] CN3 참조) 기준으로 정합 확인 필요.

---

### CN1 — 전원 (Rx OLED Regulator Power B/D)

| 항목 | 내용 |
|---|---|
| 커넥터 | HEADER_1.27mm/6P (6핀, Straight Type) |
| 용도 | 절연 전원 공급 (`COMM_P5V` / `COMM_GND`) |
| 프로토콜 매뉴얼 표기 | CN4 |

입력 5V(COMM_P5V) → B1(SHH-1M2012-221) + FLT1(NFM41PC155B1H3L) 전원분리 회로 → BLE_P3V3(3.3V) 생성.

---

### CON2 — UART 모니터링 (절연형, PC 연결)

| 항목 | 내용 |
|---|---|
| 커넥터 | SMAW250-04 (2.5mm pitch, 4핀) |
| 대체품 | MOLEX 22-05-7045 (KK 2.5mm 4핀) |
| 용도 | UART 모니터링 (`(연결@PC Monitoring)`) |

| 신호 | 방향 | 비고 |
|---|---|---|
| TXD_uC | uC → PC | ISO6721RBDR 절연 경유 |
| RXD_uC | PC → uC | ISO6721RBDR 절연 경유 |
| COMM_P5V | — | 절연 전원 (CN1에서 공급) |
| COMM_GND | — | 절연 GND |

ISOL1 (ISO6721RBDR/SOIC-8): 2채널 디지털 아이솔레이터. D2 (SZNUP2105LT1G/SOT23-3): ESD 보호.

---

## LED 인디케이터

| 부품 | 색상 | 기능 | 신호 |
|---|---|---|---|
| LED1 | Green | System Ready (점등) | LED1_uC |
| LED2 | Yellow | SPI Comm Status (점멸) | LED2_uC |
| LED3 | Green | BLE Comm Status (점멸) | LED3_uC |

구동 방식: PDTC143ZT/SOT-23 (pre-biased NPN) 트랜지스터. LED GPIO 핀 번호는 펌웨어 board config에서 확인 필요.

---

## 전원 아키텍처

```
CN1 (COMM_P5V, 5V 절연)
  └─ 전원분리 회로 (B1 + FLT1) ─→ BLE_P3V3 (3.3V, nRF52832 전원)
  └─ COMM_GND (절연 GND)

CN2 (PD3V3, 3.3V 비절연 — Rx Control Board에서 공급)
  └─ DGND

BLE_P3V3 ─→ 1.3V LDO (MLZ1608M100WT000 + MLZ1608M150WT000) → RF 전원
```

전원분리 One Point 연결: BLE_GND ↔ COMM_GND 단일점 접지 (R5 0Ω).

---

## 관련

- [[rx_ble_module]] — 모듈 entity (핀맵, 펌웨어 현황)
- [[spi_packet_format]] — SPI wire 포맷
- [[spi_protocol_manual_260513]] — 커넥터 CN3/CN4 명칭 출처 (회로도와 번호 상이)
