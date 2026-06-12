---
tags: [concept, protocol, spi, comm_health]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__from-eta_tx-to_etx_rx.CSV
date: 2026-06-10
subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
---

# 통신 상태 모니터링 (SPI_Comm_St, BLE_Comm_St)

SPI 패킷의 시스템 상태 비트맵 (Header 0x10)에 포함된 통신 헬스체크 비트 두 개. 통신 단절 시 fault 처리하는 로직의 근거.

> **갱신 이력**: 판정 임계·spi_status 구조·공통 출력이 커밋 `d2232fe`(esb, 2026-06-09)에서 바뀌었다. 값·심볼은 d2232fe 기준. 핵심 변경 — ① comm-st 임계를 percent 자동계산이 아닌 **각 링크 (T,N) 직접 상수**로 통일(BLE `MIN_COUNT` 3→**20**, SPI timeout 5000→**1000ms** + `TIMEOUT`→`WINDOW` 개명), ② 01의 `spi_status`를 **LINK 전용**으로 분리하고 CRC는 별도 판정(이전엔 한 필드에 OR), ③ 3칩 공통 한 줄 출력 `pkt_print_comm_line()` 추가(현재 01만 호출).
>
> **갱신 이력 2 (esb `2f2aa65`, 2026-06-10)**: COMM 라인이 **링크 전용·이벤트 기반**으로 단순화됐다. ① `pkt_print_comm_line()` 시그니처가 **2인자(`spi_link`, `esb_link`)**로 축소 — `spi_crc`/`esb_crc` 인자 삭제, 포맷 `"COMM | SPI:%c ESB:%c\r\n"`. ② COMM 라인 출력이 **1초 주기 → 링크 상태 변화 edge에만** 출력(신규 `print_comm_line_on_change()`, `protocol_loop()`에서 매 루프 평가). ③ CRC 헬스가 모니터에서 **완전히 사라짐** — `spi_crc_fail_cnt` 카운터·COMM 라인 CRC 표시 모두 제거. CRC는 이제 **깨진 패킷 드롭(무결성 가드)만** 하고 어디에도 표시 안 됨.
>
> **갱신 이력 3 (esb `35b94d0`, 2026-06-10, 실보드 검증) — ⚠️ 갱신 이력 2의 COMM 텍스트 라인 폐기**: 01_RX_control UART5 모니터 출력이 **텍스트 printf → 11B 바이너리 패킷 송출**로 전환됐다(아래 "monitor 바이너리 전환" 절). ① **COMM 텍스트 라인 제거** — `print_comm_line_on_change()` 삭제, UART로 `COMM | SPI:.. ESB:..` 문자열 더 이상 안 나감. (`pkt_print_comm_line()` 공유 포매터는 호출처 없는 orphan으로 남음.) ② **링크 health는 0x10 status 패킷 d0 bit5/bit6로 운반** — `print_packets()`가 1초 주기로 0x10을 바이너리로 송출하며 bit5=SPI_Comm_St / bit6=BLE_Comm_St를 항상 싣는다. 별도 이벤트 라인 불필요. 이게 host([[pc_uart_gui]])가 링크 UP/DOWN을 읽는 단일 소스. 아래 "pkt_print_comm_line" 절은 historical로 강등.

## 0x10 Data[0] 바이트는 두 성격이 섞여 있다 (2026-06-08 확정)

0x10 패킷의 `Data[0]` 한 바이트 안에 **성격이 다른 두 묶음**이 들어 있다. 혼동 주의:

| 비트 | 묶음 | 의미 |
|------|------|------|
| bit0~4 | **TX 보드 물리 상태** (진짜 tx_status) | SYS_INIT / SYS_RDY / WARNING / FAULT / RX_FLT_RST |
| **bit5·bit6** | **통신 링크 heartbeat 상태** | SPI_Comm_St / BLE_Comm_St — **0x10에 함께 실릴 뿐 TX 보드 상태가 아니다** |

→ bit5/6은 "TX 보드가 어떤 상태인가"가 아니라 "그 링크가 살아있는가"를 나타낸다. 이 의미 구분이 아래 심볼 네이밍(`COMM_ST_BIT_*`를 `TX_STATUS_BIT_*`에서 분리)의 근거다.

## comm_st 비트 위치 — 구조체가 아닌 wire 11B 오버레이 (오인 주의)

**(사실)** SPI/ESB 링크 상태 비트(bit5/bit6)는 `rx_module_data_t`·`tx_module_data_t` **구조체 필드가 아니다**. **wire 11B 패킷 data[0]의 해당 비트에만 존재**하며, 구조체 → wire 직렬화 시 별도로 오버레이·주입된다.

| 노드 | 동작 | 비고 |
|------|------|------|
| **02_RX_ble** | ESB로부터 수신한 0x10 패킷 **복사본**에 `spi_comm_st_bit`(bit5)·`ble_comm_st_bit`(bit6)를 오버레이하고 **CRC를 재계산**해 SPI로 STM32에 전달 | 원본 ESB 페이로드 수정 없이 송신 복사본(`spi_tx_pkt`)에 stamp — "race-free stamp" 절 |
| **01_RX_control** | `build_comm_extra_d0()`로 comm_st 비트를 data[0]에 재구성해 **monitor 0x10 패킷**에 탑재 후 UART5로 송출(`print_packets`) | `status_byte1`/`status_byte2`는 data[1]/[2]로 **별개** |

> ⚠️ **오인 주의**: `status_byte1`/`status_byte2`(= data[1]/data[2])와 `comm_st` 비트(data[0].bit5/6)는 **독립된 바이트에 위치**한다. dummy 테스트 코드가 status_byte를 수정해도 **comm_st 비트는 무관하게 유지**된다 — "dummy가 status_byte를 건드리면 comm_st가 깨진다"는 오진의 전형.

## 심볼·네이밍 컨벤션 (커밋 `e5e3efc`, 2026-06-08)

링크 상태 비트를 tx_status에서 의미적으로 분리하기 위해 매크로 prefix를 갈랐다. **심볼명과 모니터 라벨 문자열은 서로 다름**에 주의.

| 구분 | 이전 | 현재 | 비고 |
|------|------|------|------|
| 비트 매크로 (SPI) | `TX_STATUS_BIT_SPI_COMM_ST`(5) | `COMM_ST_BIT_SPI`(5) | prefix `TX_STATUS_BIT_`→`COMM_ST_BIT_` (tx_status 아니므로) |
| 비트 매크로 (BLE) | `TX_STATUS_BIT_BLE_COMM_ST`(6) | `COMM_ST_BIT_BLE`(6) | 동일 |
| heartbeat 일반명 | `hb_bit` / `hb_time` / `Heartbeat_Loop` | `spi_comm_st_bit` / `spi_comm_st_time` / `SpiCommSt_Loop` | 3종 펌웨어 전체 통일 |
| | `hb_last` / `hb_last_change` / `hb_seen` | `spi_comm_st_*` | 동일 |
| timeout 매크로 | `SPI_HB_TIMEOUT_MS`(5000) | `SPI_COMM_ST_WINDOW_MS`(**1000**) | `e5e3efc`에서 `SPI_COMM_ST_TIMEOUT_MS`(5000)로 개명·값유지 → `d2232fe`에서 다시 `..._WINDOW_MS`(1000)으로 개명·단축. (T,N) 모델 통일 |
| 모니터 라벨 문자열 | `"SPI_Comm_St"` / `"BLE_Comm_St"` | **변경 없음 (유지)** | 프로토콜 문서 260513 표시명 — 심볼명(`COMM_ST_BIT_SPI`)과 다름 |

> ⚠️ **심볼명 ≠ 라벨 문자열**: 코드 심볼은 `COMM_ST_BIT_SPI`로 바뀌었으나 UART 모니터에 찍히는 문자열은 문서 표시명 `"SPI_Comm_St"`를 그대로 쓴다. 둘을 혼동하지 말 것.

## 두 비트는 서로 다른 링크 — 판정 방식도 다르다 (2026-06-08 정리)

**핵심: SPI_Comm_St와 BLE(ESB)_Comm_St는 대상 링크가 달라 판정 방식이 갈린다.** 한쪽(SPI)은 공식 heartbeat 유지, 다른 쪽(ESB)만 재정의한다.

| 비트 | 대상 링크 | 판정 방식 | 근거 |
|------|----------|----------|------|
| **SPI_Comm_St** | nRF ↔ STM32 **SPI 인터페이스** | **200ms 교번 heartbeat (유지)** | 공식 프로토콜 문서 260513 명시. 변경 없음. ✓ 구현(`e5e3efc`) |
| **BLE_Comm_St** (현 ESB) | TX nRF ↔ RX nRF **ESB RF 링크** | **presence 리셋 윈도우 (재정의)** — 각 nRF가 자기 수신 delta로 판정 | BLE "페어링" 개념이 ESB에 부재 → 재정의. ✓ 구현(`6cd7e6c`) |

**왜 SPI는 heartbeat가 맞나**: 토글 비트가 **SPI를 건너와** STM32에 도달하는 것 자체가 "SPI 통신이 살아있는지" 테스트다. 변화가 멈추면 인터페이스 불량. 공식 문서가 이 방식을 명시했고 의미상으로도 타당하므로 **유지**한다. (2026-06-08 사용자 확인 — 앞선 CRC 재정의 시도는 SPI에 대해 철회)

**CRC는 SPI에서 보조 fault 경로**: payload 무결성은 heartbeat가 못 본다. STM32가 비트로 받을 필요 없이 로컬에서 CRC를 계산해 보조로 잡는다. **단, `d2232fe`부터 `spi_status`는 LINK(토글 타임아웃) 전용으로 분리됐고 CRC는 별도 판정**이다 — 아래 "spi_status LINK/CRC 분리" 절. (이전엔 둘이 한 `spi_status`에 OR돼 있었음)

**ESB 링크 판정식 — presence 리셋 윈도우** (BLE_Comm_St에만 적용, 구현 `6cd7e6c`):

```
ESB 링크 ALIVE  ⟺  최근 BLE_COMM_ST_WINDOW_MS(=200ms) 내 수신 delta ≥ BLE_COMM_ST_MIN_COUNT(=20)
```

- **presence(있나 없나)이지 throughput/heartbeat가 아니다** — "패킷이 오긴 오나"만 본다. `N=20`은 헐거운 임계(**링크가 사실상 죽었을 때만 dead**). `ESB_TX_INTERVAL_MS=1ms`이므로 200ms 윈도우 기대 수신 ≈ **200개**, `N=20`은 그 **~10%**. (코드 주석·커밋 `d2232fe` 명시)
- CRC와의 관계: ESB SDK가 콜백 전에 CRC를 검증해 **CRC-fail 패킷은 폐기**(PRX `on_radio_disabled_rx`에서 `CRCSTATUS==0`이면 RX 재시작). 따라서 `NRF_ESB_EVENT_RX_RECEIVED`는 **CRC-valid only** — `esb_rx_cnt`가 CRC-valid만 세는 건 공짜. presence 판정이 곧 "CRC-valid 패킷 도착" 판정.
- ESB RF 링크 상태는 **그 RF를 직접 받는 nRF만** 안다 → 02·03이 **각자 자기 수신 delta로 독립 판정**(아래 노드별 표). 02→03은 ACK 경로뿐이라 02의 verdict를 03으로 못 보내므로, 03은 자기 ACK 수신으로 우회 판정 — 데이터 경로 변경 없음.
- 판정 코드(사실, d2232fe): `02_RX_ble/main.c:391`·`03_TX_ble/main.c:509` 모두 `ble_comm_st_bit = (delta >= BLE_COMM_ST_MIN_COUNT) ? 1 : 0`, 윈도우 주기 `if (millis() - ble_comm_st_time >= BLE_COMM_ST_WINDOW_MS)`.

## comm_st health 판정 비대칭과 구조적 결합

SPI comm_st와 ESB comm_st는 **판정 메커니즘이 다를 뿐 아니라 복구 특성도 비대칭**이다.

| 항목 | SPI comm_st (bit5) | ESB comm_st (bit6) |
|------|------|------|
| 판정 방식 | 02가 **200ms 주기 자체 heartbeat 토글** → 01의 rolling timeout | **수신 카운트 sliding window** (200ms/N=20) |
| 복구 특성 | 02(nRF)가 살아있으면 SPI가 연결될 때 **자동 복구** — 별도 ESB 수신 불필요 | ESB RF 링크 수신 이벤트가 실제로 있어야 복구 |
| 생성 주체 | 02 자체 생성 | 03 PTX 송신 + 02 PRX 수신 |

**(구조적 결합)** heartbeat가 TX 페이로드(0x10)에 얹혀 있다. 02가 릴레이할 **valid 0x10 패킷이 없으면** — 03 연결 이전·ESB init 직후 — heartbeat 토글이 STM32에 도달하지 않아, **SPI 물리 링크가 멀쩡해도 SPI comm_st가 DOWN**으로 표시된다. 이는 "heartbeat를 ESB 릴레이 경로에 편승"시킨 구조에서 자연 발생하는 결합이다.

→ 실무 함의: SPI comm_st DOWN 발생 시 ① SPI 케이블·연결 ② 03 SPIS 미연결 ③ ESB 링크 미수립 세 가지를 함께 점검해야 한다.

## 통신상태 판정 모델 — 각 링크 (T,N) 직접 상수 (커밋 `d2232fe`, 2026-06-09)

**(사실)** comm-st 임계는 percent 자동계산이 아니라 **각 링크가 `(WINDOW_MS, MIN_COUNT) = (T, N)` 쌍을 직접 상수로** 갖는다. 두 링크 상수가 `_shared/oled_tv_protocol.h` **한 블록**("통신 링크 상태 판정 (T, N) 모델")에 모여 있다. **정의는 공유 헤더에 모으되 메커니즘은 링크마다 다르다.**

| 링크 | 메커니즘 | 소비 칩 | 상수 (d2232fe) |
|------|----------|---------|----------------|
| **SPI** | **rolling-timeout** — 마지막 토글 edge 이후 `WINDOW(T)` 경과 시 dead, 윈도우 내 edge 1번이면 alive | **01_RX_control만** | `SPI_COMM_ST_WINDOW_MS=1000`(T), `SPI_COMM_ST_MIN_COUNT=1`(N) |
| **BLE(ESB)** | **윈도우 카운트** — `WINDOW(T)` 동안 수신 이벤트 수 ≥ `MIN_COUNT(N)`이면 alive | **02·03** | `BLE_COMM_ST_WINDOW_MS=200`(T), `BLE_COMM_ST_MIN_COUNT=20`(N) |

- **(사실)** `SPI_COMM_ST_WINDOW_MS=1000`은 01만 소비. SPI 판정 실코드는 `WINDOW`만 참조(MIN_COUNT 미참조). `SPI_COMM_ST_MIN_COUNT=1`은 모델 문서값으로만 존재하다 **`9ad338d`에서 제거**됨(참조 0건).
- **(사실)** `SPI_COMM_ST_WINDOW_MS`는 01만 소비; 02/03은 `BLE_COMM_ST_*` 상수만 사용. `SPI_COMM_ST_MIN_COUNT`는 `9ad338d`에서 _shared에서 삭제됨.

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
| bit5 적재 (02_RX_ble) | ✓ | 판정(`SpiCommSt_Loop`이 `spi_comm_st_bit` set)과 wire 적재를 분리 — **나가는 SPI 송신 복사본 `spi_tx_pkt`에 송신 직전 stamp**(`SPI_Loop`), 공유 RX 버퍼 `esb_pkt[0]` 아님. 아래 "race-free stamp" 절. (`build_tx_pkt()` 아님 — 낡은 단서 정정) |
| 무변화 timeout → SPI_FAIL 판정 (STM32) | ✓ 실보드 검증 | ~~`SPI_COMM_ST_TIMEOUT_MS=5000`~~ → `d2232fe`부터 `SPI_COMM_ST_WINDOW_MS=1000`. 케이블 분리 확인 |
| ~~heartbeat + CRC fail 단일 `spi_status` 통합~~ → **LINK/CRC 분리** | △ (재구조화 `d2232fe`) | `e5e3efc`에서 통합했으나 `d2232fe`에서 **되돌려 분리** — `spi_status`=LINK 전용(토글 타임아웃), CRC는 1초 윈도우 fail로 별도. 실보드 미재검증 |
| SPI_FAIL 전이 시 UART 경고 출력 | ✓ 실보드 검증 | `spi \| LINK DOWN` / `spi \| LINK UP` (edge trigger 1회) 콘솔 확인 |
| LED2(P0.08) = `spi_comm_st_bit` mirror | ✓ 실보드 검증 | blink 확인. [[tx_ble_module]] |
| Warning 플래그 set / 대기 상태 머신 | ✗ 미구현 | `rx_status.warning` 항상 0 송신 |
| Fault 플래그 set / 출력 중 상태 머신 | ✗ 미구현 | `rx_status.fault` 항상 0 송신 |
| PWM 출력 차단 (pwm_stop) | ✗ 미구현 | SPI_FAIL이 PWM 제어 경로와 미연결 |

> ⚠️ **오인 주의**: 공식 사양의 후속("Warning/Fault+출력차단")은 **아직 코드로 실현되지 않았다**.
> 현재 구현된 것은 "단절/복구 전이 시 UART 경고 출력 + LED2 mirror"까지다 — 상태 머신 설계 없이 가시성 먼저.
> `rx_status.warning`/`.fault`는 죽은 필드(소비처 없음). [[spi_link_reliability]] 참조.

## BLE_Comm_St (Bit.6 of Buffer[0] in 0x10) — 현 명칭상 ESB 링크 상태

**현 정의 (✓ 구현 `6cd7e6c`, 2026-06-08 실보드 검증)** — ESB RF 링크([[tx_ble_module]] ↔ [[rx_ble_module]])가 살아있는지. 심볼 `COMM_ST_BIT_BLE`(`_shared/oled_tv_protocol.h`). 판정식은 위 "presence 리셋 윈도우". 심볼명은 `ble_comm_st_*` ↔ SPI측 `spi_comm_st_*` 대칭.

**노드별 동작** — 02·03이 **각자 자기 수신 delta로 독립 판정**:

| 노드 | 판정 입력 | 동작 |
|------|----------|------|
| **02_RX_ble** (PRX) | `esb_rx_cnt` delta (ESB 패킷 수신) | `EsbCommSt_Loop()`가 `ble_comm_st_bit` 판정 → **0x10 bit6에 실어 STM32로 전달** + 로컬 LED3 미러 |
| **03_TX_ble** (PTX) | `esb_ack_cnt` delta (ACK 수신) | `EsbCommSt_Loop()`가 동일 판정 → **자기 LED3 미러만**, STM32 전송 없음 (`pkt_build_tx` extra_d0=0) |
| **01_RX_control** (STM32) | 수신한 0x10 bit6 | `ble_comm`으로 추출(`common.c`) → ESB `LINK UP`/`LINK DOWN` edge 콘솔 로그 (`"esb \| LINK UP/DOWN"`). **소비 주체** |

- **실보드 검증 (양방향)**: 02 중지→01 SPI DOWN/재개→UP, 03 중지→01 ESB DOWN/재개→UP.
- **설계 근거 (재논의 방지)**: ① 판정 주체가 수신측 nRF인 건 RF 상태를 nRF만 보기 때문. 02→03은 ACK 경로뿐이라 02 verdict를 03으로 못 보냄 → 03이 자기 ACK 수신으로 독립 판정해 우회(데이터 경로 변경 없음). ② presence로 정한 건 "패킷이 오긴 오나"만 보면 된다는 합의 — `N=20`은 헐거움(기대 ~200개의 ~10%, 사실상 침묵만 dead; `d2232fe`에서 3→20).

**원본 사양 (매뉴얼 260513, historical)** — 문서 원문은 두 줄뿐:
- "Bluetooth 통신상태를 확인하기 위한 Bit이며, Bluetooth 모듈에서 통신상태 신호를 **자체 생성**한다"
- 비트맵 0/1 의미: 0 통신 대기/불량 / 1 페어링·정상 운용 중 ([[tx_to_rx_packets]])

> **문서가 고정한 것 vs 비운 것**: BLE_Comm_St는 **생성 주체(무선모듈 자체 생성)와 전달(SPI 비트로 [[rx_control]]에)만** 못박고 **판정 방식(method)은 비웠다**. presence 리셋 윈도우는 그 빈칸을 채운 우리 설계 — 자체 생성·비트 전달 구조는 문서대로라 충돌 없음. 생성 주체 = RX측 nRF = [[rx_ble_module]](02_RX_ble).

> **⚠️ 폐기된 기록·설계 (정정)**:
> - `ble_link` 심볼은 **코드에 존재하지 않는다**. 기존 "03_TX_ble `ble_link` 항상 0" 기록 폐기. 실제 변수 = 02·03 로컬 `ble_comm_st_bit`, 01의 `ble_comm`.
> - 구 free-run heartbeat 설계(커밋 `b84b31b`, "03이 0x10 bit6에 더미 토글 송신")는 **완전 폐기**. 이제 03은 bit6을 송신하지 않고(`pkt_build_tx` extra_d0=0) 02가 판정·적재. 03의 구 `g_hb` 더미 토글도 이번에 제거.

## spi_status LINK/CRC 분리 — 두 직교 실패모드 (01_RX_control, `d2232fe`)

**(사실)** `d2232fe`에서 01_RX_control의 `spi_status`가 **두 직교 실패모드로 분리**됐다. 이전(`e5e3efc`)엔 무변화 timeout과 CRC fail이 한 `spi_status`에 OR돼 있었는데, 이제 갈렸다 (`01_RX_control/Application/Src/common.c`).

| 축 | 판정 | 코드 |
|----|------|------|
| **LINK** | 02의 200ms 토글 edge가 `SPI_COMM_ST_WINDOW_MS(=1000ms)` 안에 안 보이면 down — **상대 생존/연결 여부**. comm_st 토글 비트 타임아웃(rolling)으로만 판정, **CRC와 독립** | `spi_status = (spi_comm_st_seen && (tick - last_change) < SPI_COMM_ST_WINDOW_MS) ? SPI_OK : SPI_FAIL` |
| **CRC** | 수신 SPI 패킷 XOR 체크섬 무결성 — **받은 바이트가 안 깨졌나** | `exchange_packets()`의 `if (ok) apply_rx_pkt(...)` — 검증 실패 패킷은 **적용하지 않고 드롭만** |

- **둘은 서로 다른 것을 잡는다**: LINK = 상대가 살아 보내나, CRC = 받은 바이트가 안 깨졌나.
- **(사실, `2f2aa65`) CRC는 제어/모니터 어디에도 물려 있지 않다**: 체크섬 불일치 시 코드가 하는 일은 **깨진 패킷을 적용하지 않고 드롭**하는 것뿐 — 재요청·fault·에러 플래그 없음. 과거 `spi_crc_fail_cnt`는 모니터 표시 전용이었고, `2f2aa65`에서 표시처(COMM 라인 CRC 자리)와 함께 **카운터까지 제거**됐다. 단, **체크섬 검증 + 깨진 패킷 드롭(데이터 무결성)은 유지**된다.
- **(사실)** spi_status의 LINK/CRC 분리 자체는 `d2232fe`: 당시 `spi_proc()`에서 ok 시 `spi_status=SPI_OK`·CRC fail 시 `spi_status=SPI_FAIL`로 적던 **두 줄이 제거**돼 `spi_status`가 토글 타임아웃만으로 결정. (`9be1a7a`에서 `spi_proc`→`app_protocol.c` `exchange_packets()`로 적출 — [[app_protocol_module]].) `2f2aa65`에서 잔존하던 CRC 카운터·COMM 표시까지 마저 떼어내 **CRC는 이제 표면화되지 않는 순수 무결성 가드**가 됐다.

## monitor 바이너리 전환 — 텍스트 printf → 11B 패킷 송출 (`35b94d0`, 2026-06-10 실보드 검증)

**(사실)** 01_RX_control UART5 모니터 출력이 사람용 텍스트가 아니라 **11B 바이너리 패킷**이다. `print_packets()`가 1초 주기로 6개 헤더(0x10/0x11/0x12/0x50/0x51/0x52)를 `pkt_build_tx`/`pkt_build_rx`로 빌드해 `uart_send()`로 송출한다 (`uart_send`는 `app_usart`에 추가된 공개 함수 — SPI의 `spi_txrx_dma`와 같은 결). TeraTerm 등 텍스트 터미널로 열면 깨져 보이는 게 정상.

- **wire 프레임 불변**: `[HDR][LEN=0x08][DATA[8]][CRC]`, big-endian, 전압·전류 scale 0.01 ([[spi_packet_format]]). 같은 11B가 이제 UART에도 그대로 흐른다 — host는 SPI/ESB와 동일 구조로 파싱.
- **링크 health = 0x10 d0 bit5/bit6**: SPI_Comm_St(bit5)·BLE_Comm_St(bit6)가 1초 주기 0x10 바이너리 status 패킷에 항상 실려 전달된다. 별도 COMM 텍스트 라인·이벤트 출력 불필요. host([[pc_uart_gui]])의 `Link: SPI [UP/DOWN] ESB [UP/DOWN/-]` 표시가 이 두 비트를 읽는다.
- **command 채널 무변경**: UART5 라인 단위 ISR 파싱·command 응답 printf(`buck=.. V` 등)는 그대로 남는다 — 수동 TeraTerm 디버그용. monitor 송출(바이너리)과 command 응답(텍스트)이 한 UART5에 섞여 나가므로, host 리더는 11B HDR 동기 + CRC 검증으로 command 텍스트 잡음을 자연 폐기한다([[pc_uart_gui]]).
- **변경 파일**: `app_usart.h/.c`(`uart_send` 추가), `app_protocol.c`(`print_packets` 바이너리화, COMM 비트는 0x10 d0에 반영, `print_comm_line_on_change` 삭제). 무변경: command 파서·응답 printf(`HAL_UART_RxCpltCallback`).

## 모니터링 채널 분리 — 기계 계약 vs 사람 디버그 (b92835c→e85839c, 2026-06-11 확정)

01과 02의 모니터링 출력은 **성격이 다른 두 채널**이다. 혼동하면 02 코드 수정 시 GUI 영향을 오판한다.

| 노드 | 채널 | 포맷 | 소비처 |
|------|------|------|--------|
| **01_RX_control** | UART5 | **11B 바이너리** (HDR 0x10~0x52, `pkt_build_*`→`uart_send`) | `tools/pc_uart_gui/uart_gui.py`가 `decode_packet`으로 파싱 — **기계 파싱 계약** |
| **02_RX_ble** | UART (CON2) | **사람이 읽는 텍스트** (`pkt_print_status_line`의 `"0x10 \| [0]xxxxxxx-"` 비트나열) | 별도 디버그 터미널 — **어떤 기계 파서도 의존하지 않음** |

**결론**: 02의 init/배너 printf 제거, Monitor 텍스트 포맷 변경, `Monitor_Loop` 리팩토링은 **PC GUI(uart_gui.py)에 무관하게 안전하다**. GUI가 파싱하는 것은 01 UART5 바이너리뿐이다.

02 텍스트 Monitor는 "사람 모니터링 계약"으로만 보존하면 된다 — 기계 파서 호환성 고려 불필요.

> ⚠️ **CLAUDE.md 갱신 후보 (펌웨어 repo)**: 펌웨어 CLAUDE.md가 PC UART GUI 계약을 01/02 구분 없이 기술하고 있다면, "GUI 계약 = 01 UART5 바이너리 전용"으로 정정 필요. [[nrf52_firmware_conventions]] 참조.

## pkt_print_comm_line — 3칩 공통 한 줄 출력 (`d2232fe` 신설 → `2f2aa65` 2인자 → `35b94d0` orphan → ⚠️ `9ad338d` _shared에서 제거)

> ⚠️ **제거됨 (`9ad338d`, 2026-06-11)**: `35b94d0`에서 호출처가 사라진 orphan `pkt_print_comm_line()`이 `9ad338d`에서 _shared에서 완전 삭제됐다. 아래는 `2f2aa65`까지의 동작 기록 — 현재 링크 health는 위 "monitor 바이너리 전환"대로 0x10 d0 bit5/6으로 운반된다.

**(사실)** `_shared/oled_tv_protocol.c`에 공통 포매터. `2f2aa65`에서 **링크 전용 2인자로 단순화**됐다 (구 4인자는 `spi_crc`/`esb_crc`를 포함했으나 CRC 표시 자체가 제거되며 삭제):

```c
void pkt_print_comm_line(int8_t spi_link, int8_t esb_link);
/* 출력: "COMM | SPI:%c ESB:%c\r\n"
 * 각 인자: 1 → '1'(up), 0 → '0'(down), 그 외(-1) → '-'(stale/N/A) */
```

- **함수는 칩을 모른다** — 컴파일타임 칩 매크로 없음. 각 펌웨어가 **자기가 아는 값만 넘겨** 칩별 차이가 갈린다.
- **(사실)** 현재 **01_RX_control만 호출**(`2f2aa65` 기준 `app_protocol.c` `print_comm_line_on_change()`). 02/03에도 공유 함수가 컴파일되지만 **호출 안 함**(아래 보류 절). 향후 02/03에 COMM 라인을 붙이려면 이 **2인자 시그니처 기준**.

**01의 COMM 라인 동작 (현재 01만 와이어링, `2f2aa65`부터 이벤트 기반)** — `app_protocol.c`:

| 인자 | 01이 넘기는 값 |
|------|----------------|
| `spi_link` | `spi_status==SPI_OK ? 1 : 0` |
| `esb_link` | SPI link down이면 `-1`(stale), 아니면 relay받은 `ble_comm`(0x10 bit6) ? `1` : `0` |

- **출력 시점 (이벤트 기반)**: `print_comm_line_on_change()`가 `protocol_loop()`에서 `exchange_packets()` 직후 **매 루프 평가**되지만, 링크 상태(SPI/ESB up·down) **변화 edge에만** 출력한다 (1초 주기 아님). 부팅 직후 초기 상태 1회는 찍힌다(`prev` 초기값 `-2`이라 첫 평가에서 무조건 edge). **패킷 덤프**(`[eta-tx>>eta-rx]` 등)는 여전히 `print_packets()`의 1초 게이트(`MONITOR_INTERVAL_MS`) — **두 출력의 주기가 분리됨**.

출력 예 (사실):
- SPI·ESB 모두 up → `COMM | SPI:1 ESB:1`
- **SPI link down** → `COMM | SPI:0 ESB:-` — SPI가 끊기면 ESB relay 경로도 끊긴 것이라 ESB는 stale(`-`).

## race-free stamp — wire 상태비트는 송신 복사본에 stamp (실보드 플래핑으로 발견)

**교훈**: wire 상태비트(bit5 SPI · bit6 BLE)는 공유 RX 버퍼 `esb_pkt[0]`이 아니라 **나가는 SPI 송신 복사본 `spi_tx_pkt`에 송신 직전 stamp**해야 한다 (`02_RX_ble` `SPI_Loop`).

- **이유**: ESB RX ISR(`esb_event_handler`)이 0x10 수신마다 `esb_pkt[0]`을 통째 `memcpy`로 비동기 덮어쓴다 → `esb_pkt[0]`에 상태비트를 stamp하면 ISR과 **race**해 비트가 날아간다.
- **증상**: 01에서 ESB `LINK UP/DOWN` **플래핑**(실측 전이 49→30→0/30s, 최종 fix에서 소멸).
- **bit5가 안 드러난 이유**: STM32가 bit5는 5초 freshness(무변화 timeout)로 봤기 때문에 race가 가려졌고, 즉시 0/1로 읽히는 **bit6만** 표면화했다.
- **원칙**: **판정(`EsbCommSt_Loop`/`SpiCommSt_Loop`의 변수 set)과 wire 적재(`SPI_Loop` 송신 직전 stamp)를 분리**하는 게 단일·race-free 자리.

## 보류·미구현 (35b94d0 시점 — "완료" 아님)

- ~~02/03 COMM 라인 출력~~ — **무의미해짐**: `35b94d0`에서 01의 COMM 텍스트 라인 자체가 제거됐다. 링크 health는 0x10 d0 bit5/6 바이너리 운반으로 일원화 — 02/03이 별도 COMM 텍스트 라인을 낼 이유가 사라졌다.
- **ESB CRC SW 검증 — 구현 안 하기로 결정**. ESB 라디오 HW CRC가 이미 무결성을 보증해 SW XOR 검증은 중복. SPI 측 CRC도 표시 안 함 — 무결성은 깨진 패킷 드롭으로만 처리(위 LINK/CRC 절).
- **(검증 항목) SPI 끊김 시 0x10 d0 bit5 → 0 낙하** — host([[pc_uart_gui]])가 `Link: SPI`를 이 비트로 표시하므로, SPI 단절 시 bit5가 정확히 0으로 떨어지는지 실보드에서 확인 대상.
- (기존 미구현 유지) SPI_FAIL 후속 — Warning/Fault 플래그·PWM 차단 상태 머신. `rx_status.warning/.fault`는 여전히 죽은 필드.

## 관련

- [[spi_link_reliability]] — heartbeat 구현·검증·SPI 단절 복구 (구현 측)
- [[spi_packet_format]] — 패킷 위치·11B wire (이제 UART에도 흐름)
- [[pc_uart_gui]] — host 바이너리 리더·링크 표시(0x10 d0 bit5/6 소비처)
- [[app_protocol_module]] — `print_packets` 바이너리화·`uart_send`
- [[tx_to_rx_packets]] — 0x10 Buffer[0] 비트 매핑 전체
- [[spi_protocol_manual_260513]] — 원본
