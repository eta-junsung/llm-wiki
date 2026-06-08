---
tags: [concept, protocol, spi, comm_health]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__from-eta_tx-to_etx_rx.CSV
date: 2026-06-08
subsystem: 01_RX_control, 02_RX_esb
---

# 통신 상태 모니터링 (SPI_Comm_St, BLE_Comm_St)

SPI 패킷의 시스템 상태 비트맵 (Header 0x10)에 포함된 통신 헬스체크 비트 두 개. 통신 단절 시 fault 처리하는 로직의 근거.

## 0x10 Data[0] 바이트는 두 성격이 섞여 있다 (2026-06-08 확정)

0x10 패킷의 `Data[0]` 한 바이트 안에 **성격이 다른 두 묶음**이 들어 있다. 혼동 주의:

| 비트 | 묶음 | 의미 |
|------|------|------|
| bit0~4 | **TX 보드 물리 상태** (진짜 tx_status) | SYS_INIT / SYS_RDY / WARNING / FAULT / RX_FLT_RST |
| **bit5·bit6** | **통신 링크 heartbeat 상태** | SPI_Comm_St / BLE_Comm_St — **0x10에 함께 실릴 뿐 TX 보드 상태가 아니다** |

→ bit5/6은 "TX 보드가 어떤 상태인가"가 아니라 "그 링크가 살아있는가"를 나타낸다. 이 의미 구분이 아래 심볼 네이밍(`COMM_ST_BIT_*`를 `TX_STATUS_BIT_*`에서 분리)의 근거다.

## 심볼·네이밍 컨벤션 (커밋 `e5e3efc`, 2026-06-08)

링크 상태 비트를 tx_status에서 의미적으로 분리하기 위해 매크로 prefix를 갈랐다. **심볼명과 모니터 라벨 문자열은 서로 다름**에 주의.

| 구분 | 이전 | 현재 | 비고 |
|------|------|------|------|
| 비트 매크로 (SPI) | `TX_STATUS_BIT_SPI_COMM_ST`(5) | `COMM_ST_BIT_SPI`(5) | prefix `TX_STATUS_BIT_`→`COMM_ST_BIT_` (tx_status 아니므로) |
| 비트 매크로 (BLE) | `TX_STATUS_BIT_BLE_COMM_ST`(6) | `COMM_ST_BIT_BLE`(6) | 동일 |
| heartbeat 일반명 | `hb_bit` / `hb_time` / `Heartbeat_Loop` | `spi_comm_st_bit` / `spi_comm_st_time` / `SpiCommSt_Loop` | 3종 펌웨어 전체 통일 |
| | `hb_last` / `hb_last_change` / `hb_seen` | `spi_comm_st_*` | 동일 |
| timeout 매크로 | `SPI_HB_TIMEOUT_MS`(5000) | `SPI_COMM_ST_TIMEOUT_MS`(5000) | 값 유지, 이름만 |
| 모니터 라벨 문자열 | `"SPI_Comm_St"` / `"BLE_Comm_St"` | **변경 없음 (유지)** | 프로토콜 문서 260513 표시명 — 심볼명(`COMM_ST_BIT_SPI`)과 다름 |

> ⚠️ **심볼명 ≠ 라벨 문자열**: 코드 심볼은 `COMM_ST_BIT_SPI`로 바뀌었으나 UART 모니터에 찍히는 문자열은 문서 표시명 `"SPI_Comm_St"`를 그대로 쓴다. 둘을 혼동하지 말 것.

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

**구현 현황 (커밋 `e5e3efc`, 2026-06-08 실보드 검증 — 검증 5/5 PASS)**:

| 항목 | 상태 | 비고 |
|------|------|------|
| 200ms 교번 비트 생성 (nRF) | ✓ 실보드 검증 | `SpiCommSt_Loop()` millis 게이트, P0.17 오실로 Δt≈190ms |
| bit5 적재 (02_RX_ble) | ✓ | `ESB_Loop()`의 0x10 보관 **직후 인라인 clear+set** — `build_tx_pkt()` 아님 (낡은 단서 정정) |
| 5s 무변화 → SPI_FAIL 판정 (STM32) | ✓ 실보드 검증 | `SPI_COMM_ST_TIMEOUT_MS=5000`, 케이블 분리 확인 |
| heartbeat + CRC fail 단일 `spi_status` 통합 | ✓ 실보드 검증 | 두 FAIL 경로(무변화 timeout · CRC fail)를 하나의 `spi_status`로 |
| SPI_FAIL 전이 시 UART 경고 출력 | ✓ 실보드 검증 | `spi \| LINK DOWN` / `spi \| LINK UP` (edge trigger 1회) 콘솔 확인 |
| LED2(P0.08) = `spi_comm_st_bit` mirror | ✓ 실보드 검증 | blink 확인. [[tx_ble_module]] |
| Warning 플래그 set / 대기 상태 머신 | ✗ 미구현 | `rx_status.warning` 항상 0 송신 |
| Fault 플래그 set / 출력 중 상태 머신 | ✗ 미구현 | `rx_status.fault` 항상 0 송신 |
| PWM 출력 차단 (pwm_stop) | ✗ 미구현 | SPI_FAIL이 PWM 제어 경로와 미연결 |

> ⚠️ **오인 주의**: 공식 사양의 후속("Warning/Fault+출력차단")은 **아직 코드로 실현되지 않았다**.
> 현재 구현된 것은 "단절/복구 전이 시 UART 경고 출력 + LED2 mirror"까지다 — 상태 머신 설계 없이 가시성 먼저.
> `rx_status.warning`/`.fault`는 죽은 필드(소비처 없음). [[spi_link_reliability]] 참조.

## BLE_Comm_St (Bit.6 of Buffer[0] in 0x10) — 현 명칭상 ESB 링크 상태

**현 정의 (2026-06-08, 재정의)** — ESB RF 링크([[tx_esb]] → [[rx_esb]])가 살아있는지. (SPI_Comm_St와 달리 이쪽은 공식 heartbeat 규정이 없고 BLE "페어링" 개념이 ESB에 부재해 재정의)
- 판정 주체: **nRF([[rx_esb]]) 로컬**. ESB RF 링크 생사는 nRF만 알 수 있다 (SPI 링크와 달리 STM32는 RF를 직접 못 봄).
- 판정식: rx_esb가 **ESB 수신 패킷의 CRC-valid 건이 도착 윈도우 내 ≥ N개**인지로 판정 → 결과를 0x10 bit6에 실어 STM32로 전달. (이 비트는 **반드시 패킷에 실어 전달** — STM32는 RF 상태를 로컬로 알 수 없으므로.)
- BLE 시절 "페어링" 개념 → "ESB CRC-valid 도착 윈도우 기반 링크 활성"으로 재정의. (사용자 결정 2026-06-08)

**원본 사양 (매뉴얼 260513, historical)** — 문서 원문은 두 줄뿐:
- "Bluetooth 통신상태를 확인하기 위한 Bit이며, Bluetooth 모듈에서 통신상태 신호를 **자체 생성**한다"
- 비트맵 0/1 의미: 0 통신 대기/불량 / 1 페어링·정상 운용 중 ([[tx_to_rx_packets]])

> **문서가 고정한 것 vs 비운 것**: SPI_Comm_St와 달리 BLE_Comm_St는 **생성 주체(무선모듈 자체 생성)와 전달(SPI 비트로 [[rx_control]]에)만** 못박고, **판정 방식(method)은 명시하지 않았다**. 따라서 "어떻게 살아있다고 판정하나"는 우리 설계 결정 — ESB에 BLE "페어링" 개념이 없으므로 CRC-valid 도착 윈도우로 채운다. 자체 생성·비트 전달 구조는 문서대로 유지하므로 충돌 없음. **생성 주체 = STM32에 붙어 무선을 받아 브리지하는 RX측 nRF = [[rx_esb]](구 02_RX_ble)**.

> **구현 현황 (2026-06-08)**: `03_TX_ble`의 `ble_link` 변수 항상 0 — ESB 수신 상태와 미연결. SPI 0x10 DATA[0] bit6은 죽은 필드(소비처 없음). 판정 주체는 송신측 03이 아니라 **수신측 02_RX_esb**임에 주의 (구 메모의 "esb_rx_cnt" 위치 재확인 필요).
> **후속 task (미착수)**: `rx_esb`에서 ESB 수신 CRC-valid 카운터 윈도우 판정 → bit6 적재. LED3(P0.06) 구동과 연계.

## 관련

- [[spi_link_reliability]] — heartbeat 구현·검증·SPI 단절 복구 (구현 측)
- [[spi_packet_format]] — 패킷 위치
- [[tx_to_rx_packets]] — 0x10 Buffer[0] 비트 매핑 전체
- [[spi_protocol_manual_260513]] — 원본
