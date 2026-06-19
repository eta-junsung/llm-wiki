---
tags: [source, schematic, hardware]
source: projects/c/oled_tv_software/docs/Schematic/회로도 (STM32F103RCT6).pdf
date: 2026-05-26
subsystem: 01_RX_control
---

# 회로도 — STM32 mini-pro v10 (STM32F103RCT6)

`01_RX_control` 타겟 보드 회로도. **이미지 기반 PDF** — 텍스트 레이어 없음. 본 페이지는 SPI 연결에 한해 수동 추출한 정보를 보관한다.

원본 경로: `projects/c/oled_tv_software/docs/Schematic/회로도 (STM32F103RCT6).pdf`

---

## STM32F103RCT6 SPI2 핀맵

회로도 표기 기준. 신호명은 nRF(슬레이브) 관점 레이블 — STM32(마스터) 표준 명칭과 대응 관계 병기.

| STM32 핀 | 회로도 레이블 | SPI 마스터 명칭 | 방향 (STM32 기준) |
|---|---|---|---|
| **PB12** | CS | nCS (SW GPIO) | OUT — 슬레이브 선택 |
| **PB13** | SCL | SCK | OUT — 클럭 (STM32가 생성) |
| **PB14** | SDO | MISO | IN — 슬레이브 → 마스터 |
| **PB15** | SDI | MOSI | OUT — 마스터 → 슬레이브 |

> SDO/SDI는 연결 대상(nRF 슬레이브)의 출력/입력을 의미하는 회로도 관습 표기. STM32 마스터 관점 MISO/MOSI와 방향이 역전되어 표시됨에 주의.

---

## STM32 ↔ nRF52832 PCA10040 배선표

`01_RX_control`(STM32 mini-pro v10) ↔ `02_RX_ble`(nRF52832 PCA10040) SPI 실물 연결.

| 신호 | STM32 핀 (mini-pro v10) | nRF GPIO (PCA10040) |
|---|---|---|
| CS (Active Low) | PB12 | P0.22 |
| SCK | PB13 | P0.27 |
| MISO (슬레이브 출력) | PB14 | P0.26 |
| MOSI (슬레이브 입력) | PB15 | P0.25 |

- STM32 측 CS: `NSS_SOFT`, init=HIGH, Active Low
- SPI Mode 2 (CPOL=1 / CPHA=0) 양측 정합
- nRF 페리: SPIS1 인스턴스 (`NRF_DRV_SPIS_INSTANCE(1)`)

> **PCA10040 헤더 위치**: nRF GPIO → PCA10040 커넥터 핀 번호 매핑은 PCA10040 Hardware Specification (PG) 참조 필요. 현재 미기록.

---

## 파생 페이지

- [[rx_control]] — STM32 entity (SPI2 설정, DMA)
- [[rx_ble_module]] — nRF52832 entity (SPIS1 핀맵, CN3 표)
- [[spi_packet_format]] — STM32-nRF 내부 SPI 프레임 (56B/45B, HDR 0xC0)
