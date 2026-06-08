---
tags: [concept, protocol, spi, comm_health]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__from-eta_tx-to_etx_rx.CSV
date: 2026-06-08
subsystem: 01_RX_control, 02_RX_esb
---

# 통신 상태 모니터링 (SPI_Comm_St, BLE_Comm_St)

SPI 패킷의 시스템 상태 비트맵 (Header 0x10)에 포함된 통신 헬스체크 비트 두 개. 통신 단절 시 fault 처리하는 로직의 근거.

## 정의 변천 — "칩 생사" → "통신 생사" (2026-06-08 재정의)

이 두 비트의 판정 의미는 두 번 바뀌었다. 혼동을 막기 위해 명시한다.

| 세대 | 판정 대상 | 방식 | 비고 |
|------|----------|------|------|
| (구) 매뉴얼 260513 | 무선 구간 **페어링/링크** | BLE 자체 신호 | BLE 시절 |
| (중) heartbeat 기반 | **상대 칩의 생사** | 200ms 토글 관측·무변화 timeout | 2026-06-01 구현 (SPI측) |
| **(현) 통신 생사** | **해당 링크가 살아있는지** | **CRC-valid 패킷이 도착 윈도우 내 수신** | 2026-06-08 재정의, 미구현 |

**현 정의(통신 생사)의 판정식 — CRC AND 도착 윈도우**:

```
링크 ALIVE  ⟺  최근 T 윈도우 내에 CRC-valid 패킷 ≥ N개 수신
```

- CRC 단독으로는 부족 — 케이블 단선/침묵 시 **패킷 자체가 안 와** CRC fail 이벤트도 없다. 따라서 "도착(timeout)"과 "무결성(CRC)"의 **AND**.
- 각 칩은 **자기가 수신하는 링크**의 CRC를 본다. CRC는 11B 패킷 말미 1바이트(HDR~Data[7] 체크섬, [[spi_packet_format]]).
- heartbeat 토글을 버리는 게 아니라, "토글 관측" 역할을 "CRC-valid 패킷 도착 윈도우 판정"으로 교체하는 형태. STM32 측은 이미 timeout+CRC를 통합 포착([[spi_link_reliability]] `spi_status`)하므로 SPI측은 사실상 기존 신호 재연결에 가깝다.

## SPI_Comm_St (Bit.5 of Buffer[0] in 0x10)

**현 정의 (2026-06-08)** — SPI 링크(무선모듈 ↔ [[rx_control]])가 살아있는지.
- 판정 주체: **STM32([[rx_control]]) 로컬**. SPI 링크 생사는 STM32가 자기 수신 패킷(0x10/0x11/0x12)의 CRC+도착 윈도우로 직접 판정 가능 → `spi_status` 사용.
- 따라서 이 비트를 0x10 패킷에 실어 STM32가 받을 필요가 없어진다. 0x10 bit5는 (a) 폐기하거나 (b) nRF→STM32 방향의 보조 heartbeat로만 잔존. **확정: STM32 로컬 `spi_status` 사용** (사용자 결정 2026-06-08).
- 통신 불량 시 후속(Warning/Fault/출력 차단)은 여전히 미구현.

**원본 사양 (매뉴얼 260513, historical)**:
- 무선모듈 ↔ [[rx_control]] 간 SPI 통신 상태 확인용
- 무선모듈이 200 ms마다 0과 1을 교번하여 비트를 갱신
- [[rx_control]]는 일정 시간 변화가 없으면 SPI 단절로 간주
- 통신 불량 시: 시스템 대기 → **Warning** / 출력 중 → **Fault 처리 + 출력 차단**
- ESB 전환 후에도 동일 로직 유지 예정 (SPI 구간은 그대로)

**구현 현황 (2026-06-01 기준)**:

| 항목 | 상태 | 비고 |
|------|------|------|
| 200ms 교번 비트 생성 (nRF) | ✓ 실보드 검증 | `Heartbeat_Loop()` millis 게이트, P0.17 오실로 Δt≈190ms |
| 5s 무변화 → SPI_FAIL 판정 (STM32) | ✓ 실보드 검증 | `SPI_HB_TIMEOUT_MS=5000`, `spi_proc()`, 케이블 분리 확인 |
| SPI_FAIL 전이 시 UART 경고 출력 | ✓ 실보드 검증 | `spi \| LINK DOWN` / `spi \| LINK UP` (edge trigger 1회). 커밋 `fe5bf14`, 2026-06-01 |
| Warning 플래그 set / 대기 상태 머신 | ✗ 미구현 | `rx_status.warning` 항상 0 송신 |
| Fault 플래그 set / 출력 중 상태 머신 | ✗ 미구현 | `rx_status.fault` 항상 0 송신 |
| PWM 출력 차단 (pwm_stop) | ✗ 미구현 | SPI_FAIL이 PWM 제어 경로와 미연결 |

> ⚠️ **오인 주의**: 위 사양("Warning/Fault+출력차단")은 아직 코드로 실현되지 않았다.
> 이번(fe5bf14)에 구현된 것은 "단절/복구 전이 시 UART 경고 출력"뿐이며,
> 그것도 의도적 단기 결정이다 — 상태 머신 설계 없이 최소 가시성 먼저.
> `rx_status.warning`/`.fault`는 죽은 필드(소비처 없음). [[spi_link_reliability]] 참조.

## BLE_Comm_St (Bit.6 of Buffer[0] in 0x10) — 현 명칭상 ESB 링크 상태

**현 정의 (2026-06-08)** — ESB RF 링크([[tx_esb]] → [[rx_esb]])가 살아있는지.
- 판정 주체: **nRF([[rx_esb]]) 로컬**. ESB RF 링크 생사는 nRF만 알 수 있다 (SPI 링크와 달리 STM32는 RF를 직접 못 봄).
- 판정식: rx_esb가 **ESB 수신 패킷의 CRC-valid 건이 도착 윈도우 내 ≥ N개**인지로 판정 → 결과를 0x10 bit6에 실어 STM32로 전달. (SPI측과 달리 이 비트는 **반드시 패킷에 실어 전달**해야 한다 — STM32는 RF 상태를 로컬로 알 수 없으므로.)
- BLE 시절 "페어링" 개념 → "ESB CRC-valid 도착 윈도우 기반 링크 활성"으로 재정의. (사용자 결정 2026-06-08)

**원본 사양 (매뉴얼 260513, historical)**:
- **무선 구간 페어링/링크 상태** 확인용 (당시 BLE)
- 0: 통신 대기 또는 통신 불량 / 1: 페어링되어 정상 운용 중
- 무선모듈이 자체적으로 신호를 생성하여 SPI를 통해 [[rx_control]]에 전달

> **구현 현황 (2026-06-08)**: `03_TX_ble`의 `ble_link` 변수 항상 0 — ESB 수신 상태와 미연결. SPI 0x10 DATA[0] bit6은 죽은 필드(소비처 없음). 판정 주체는 송신측 03이 아니라 **수신측 02_RX_esb**임에 주의 (구 메모의 "esb_rx_cnt" 위치 재확인 필요).
> **후속 task (미착수)**: `rx_esb`에서 ESB 수신 CRC-valid 카운터 윈도우 판정 → bit6 적재. LED3(P0.06) 구동과 연계.

## 관련

- [[spi_link_reliability]] — heartbeat 구현·검증·SPI 단절 복구 (구현 측)
- [[spi_packet_format]] — 패킷 위치
- [[tx_to_rx_packets]] — 0x10 Buffer[0] 비트 매핑 전체
- [[spi_protocol_manual_260513]] — 원본
