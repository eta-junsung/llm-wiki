---
tags: [concept, protocol, spi, comm_health]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__from-eta_tx-to_etx_rx.CSV
date: 2026-06-08
subsystem: 01_RX_control, 02_RX_esb
---

# 통신 상태 모니터링 (SPI_Comm_St, BLE_Comm_St)

SPI 패킷의 시스템 상태 비트맵 (Header 0x10)에 포함된 통신 헬스체크 비트 두 개. 통신 단절 시 fault 처리하는 로직의 근거.

## 두 비트는 서로 다른 링크 — 판정 방식도 다르다 (2026-06-08 정리)

**핵심: SPI_Comm_St와 BLE(ESB)_Comm_St는 대상 링크가 달라 판정 방식이 갈린다.** 한쪽(SPI)은 공식 heartbeat 유지, 다른 쪽(ESB)만 재정의한다.

| 비트 | 대상 링크 | 판정 방식 | 근거 |
|------|----------|----------|------|
| **SPI_Comm_St** | nRF ↔ STM32 **SPI 인터페이스** | **200ms 교번 heartbeat (유지)** | 공식 프로토콜 문서 260513 명시. 변경 없음 |
| **BLE_Comm_St** (현 ESB) | TX nRF → RX nRF **ESB RF 링크** | **CRC-valid 패킷 도착 윈도우 (재정의)** | BLE "페어링" 개념이 ESB에 부재 → 재정의 |

**왜 SPI는 heartbeat가 맞나**: 토글 비트가 **SPI를 건너와** STM32에 도달하는 것 자체가 "SPI 통신이 살아있는지" 테스트다. 변화가 멈추면 인터페이스 불량. 공식 문서가 이 방식을 명시했고 의미상으로도 타당하므로 **유지**한다. (2026-06-08 사용자 확인 — 앞선 CRC 재정의 시도는 SPI에 대해 철회)

**CRC는 SPI에서 보조 fault 경로**: payload 무결성은 heartbeat가 못 본다. STM32에는 이미 **CRC fail + heartbeat timeout을 통합한 로컬 `spi_status`**(LINK DOWN/UP, [[spi_link_reliability]])가 있어 보조로 동작한다 — 비트로 받을 필요 없이 STM32가 로컬 계산. SPI_Comm_St 비트(heartbeat)와 **상호보완**으로 공존.

**ESB 링크 판정식 — CRC AND 도착 윈도우** (BLE_Comm_St에만 적용):

```
ESB 링크 ALIVE  ⟺  최근 T 윈도우 내에 CRC-valid 수신 패킷 ≥ N개
```

- CRC 단독으로는 부족 — RF 단절/침묵 시 **패킷 자체가 안 와** CRC fail 이벤트도 없다. 따라서 "도착(timeout)"과 "무결성(CRC)"의 **AND**.
- ESB RF 링크 상태는 **수신측 nRF([[rx_esb]])만** 안다 (STM32는 RF를 직접 못 봄) → 판정 후 결과를 0x10 bit6에 실어 STM32로 전달.

## SPI_Comm_St (Bit.5 of Buffer[0] in 0x10)

**공식 정의 (매뉴얼 260513) — 200ms 교번 heartbeat. 변경 없음 (2026-06-08 재확인)**:
- nRF 무선모듈 ↔ [[rx_control]] 간 **SPI 인터페이스 통신 상태** 확인용
- 무선모듈이 200 ms마다 0과 1을 교번하여 비트를 갱신
- [[rx_control]]는 일정 시간 변화가 없으면 SPI 단절(인터페이스 통신 불량)로 간주
- 통신 불량 시: 시스템 대기 → **Warning** / 출력 중 → **Fault 처리 + 출력 차단**
- ESB 전환 후에도 동일 로직 유지 (SPI 구간은 그대로)

> 토글 비트가 SPI를 건너와 STM32에 도달하는 것 자체가 "SPI 통신 생존" 테스트다 — 이 방식은 의미상 타당하므로 유지. payload 무결성(CRC)은 STM32 로컬 `spi_status`가 보조로 잡는다([[spi_link_reliability]]). 한때 SPI_Comm_St도 CRC 기반으로 재정의하려다, 공식 문서 명시·의미 타당성으로 heartbeat 유지로 철회 (2026-06-08).

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

**현 정의 (2026-06-08, 재정의)** — ESB RF 링크([[tx_esb]] → [[rx_esb]])가 살아있는지. (SPI_Comm_St와 달리 이쪽은 공식 heartbeat 규정이 없고 BLE "페어링" 개념이 ESB에 부재해 재정의)
- 판정 주체: **nRF([[rx_esb]]) 로컬**. ESB RF 링크 생사는 nRF만 알 수 있다 (SPI 링크와 달리 STM32는 RF를 직접 못 봄).
- 판정식: rx_esb가 **ESB 수신 패킷의 CRC-valid 건이 도착 윈도우 내 ≥ N개**인지로 판정 → 결과를 0x10 bit6에 실어 STM32로 전달. (이 비트는 **반드시 패킷에 실어 전달** — STM32는 RF 상태를 로컬로 알 수 없으므로.)
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
