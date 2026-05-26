---
tags: [concept, protocol, spi]
source: teams/c/oled_tv_software/raw/prd_v1.0.md
date: 2026-05-26
subsystem: 01_RX_control, 02_RX_ble
---

# STM32-nRF SPI 내부 프레임

[[rx_control]](STM32, Master) ↔ [[rx_ble_module]](nRF52832, Slave) 간 SPI 버스의 내부 프레임 포맷. ESB wire 포맷([[esb_packet_format]], 11B)과 **별개** — nRF가 이 SPI 프레임을 파싱해 ESB 패킷으로 재구성(또는 역방향으로 조립)한다.

## 프레임 구조

### STM32 → nRF (`rx_module_data_t`, 56 byte)

| 필드 | 의미 |
|---|---|
| HDR `0xC0` | 프레임 시작 마커 |
| LEN | 페이로드 길이 |
| `rx_status` | RX 시스템 상태 |
| `rx_data` | RX 센싱·제어 데이터 |
| checksum | 오류 검출 |

### nRF → STM32 (`tx_module_data_t`, 45 byte)

| 필드 | 의미 |
|---|---|
| HDR `0xC0` | 프레임 시작 마커 |
| LEN | 페이로드 길이 |
| `tx_status` | TX 시스템 상태 (ESB 수신분) |
| `tx_cmd` | TX 명령 |
| `tx_data` | TX 센싱 데이터 (ESB 수신분) |
| checksum | 오류 검출 |

## 전송 파라미터

- **주기**: 20 ms (STM32가 Master로 개시)
- **SPI 모드**: Mode 2 (CPOL=1 / CPHA=0)
- **DMA**: TX=DMA1_Ch5, RX=DMA1_Ch4. 전송 크기는 56B로 통일 (HAL API 제약). nRF→STM32의 45B는 나머지를 `0xFF`로 패딩.
- **페리**: STM32 SPI2 (PB12-15, NSS_SOFT), nRF52832 SPIS1 (P0.22/25/26/27)

## 명명 주의

드라이버 내부에서 `tx_module_data_t`가 SPIS **RX 버퍼**에, `rx_module_data_t`가 SPIS **TX 버퍼**에 연결됨. 이름이 "어디서 오는가(TX 측 모듈 데이터)" 기준이라 SPIS 방향과 반대로 보임 — 혼동 주의.

## 핀맵

→ [[rx_control]] SPI 절, [[rx_ble_module]] CN3 표 참조.

## 출처

- [[prd]] (§3.1 SPI 아키텍처)
