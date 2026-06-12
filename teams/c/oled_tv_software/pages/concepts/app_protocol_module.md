---
tags: [concept, protocol, refactor, app_protocol]
source: projects/c/oled_tv_software (esb 9be1a7a 적출 → 2f2aa65 COMM 이벤트화 → 35b94d0 monitor 바이너리화)
date: 2026-06-10
subsystem: 01_RX_control
---

# app_protocol — 01_RX_control SPI 프로토콜 계층 적출·핸드오프 모듈

01_RX_control의 SPI 패킷 프로토콜 계층을 `common.c`/`common.h`에서 **신규 `app_protocol.c`/`app_protocol.h`로 적출**해, 다른 작업자가 받아 통합할 수 있는 **자립 핸드오프 단위**로 정리한 것. 커밋 `9be1a7a`(esb, 2026-06-09). [[rx_control]] 메인 루프 변화의 근거.

> R1~R4 정리 트랙([[roadmaps/spi-esb-refactor|SPI·ESB 리팩토링]])과 겹치지만 **다른 프레임** — R1~R4는 "3펌웨어 공유/모니터 정리" 중심, 이쪽은 "01의 SPI 프로토콜을 파일 경계로 적출해 자립화" 중심.

## 공개 인터페이스 (받는 쪽이 보는 전부)

- **함수 1개**: `void protocol_loop(void)` — main 루프에서 한 줄 호출 (`app_protocol.h`).
- **전역 3개 (extern)**: `rx_module`(`rx_module_data_t`) / `tx_module`(`tx_module_data_t`) / `rx_cmd`(`rx_cmd_t`, TX Buck Vout 지령 컨테이너 0x51 DATA[6..7]). 소유권이 `common`에서 `app_protocol`로 이전됨.

```c
while (1) {
    adc_proc();        // ADC 6채널
    protocol_loop();   // ← 이 한 줄로 통합
}
```

## 내부 구조 (static)

`protocol_loop()`은 두 내부 함수로 분리:

| 내부 함수 | 역할 |
|-----------|------|
| `exchange_packets()` | SPI 수신 파싱(XOR 체크섬 검사→`if (ok) apply_rx_pkt`, 실패 패킷은 드롭만) + `PACKET_INTERVAL`(10ms) 주기 송신(`pkt_build_rx`→`spi_txrx_dma`). spi_status(LINK) 갱신 포함 |
| `print_packets()` | **(`35b94d0` 바이너리화)** UART 모니터 송출. 1초 주기(`MONITOR_INTERVAL_MS`)로 6개 헤더(0x10/0x11/0x12/0x50/0x51/0x52)를 `pkt_build_tx`/`pkt_build_rx`로 빌드해 **11B 바이너리로 `uart_send()`** 송출(구 텍스트 `[eta-tx>>eta-rx]` 라인 대체). 링크 health(SPI/ESB)는 0x10 d0 bit5/6에 실려 운반 — host([[pc_uart_gui]])가 파싱 |

> ⚠️ **`35b94d0`에서 `print_comm_line_on_change()` 삭제**: `2f2aa65`에 있던 COMM 텍스트 라인(edge 출력) 함수는 monitor 바이너리화로 제거됐다. COMM 텍스트 라인은 더 이상 UART로 나가지 않고, 링크 상태는 0x10 status 패킷 d0 bit5/6으로 운반된다 — [[comm_state_monitoring]] "monitor 바이너리 전환".

보조 static: `apply_rx_pkt`(공유 `pkt_apply_tx` 래퍼 + 01 전용 hb/ble_comm/rx_flt_rst 추출), `build_tx_status_d0`, `inject_rx_dummy_data`. *(`calc_checksum` → `9ad338d`에서 제거, 공유 `pkt_checksum`으로 통일)*

## 핸드오프 — 4파일 자립

받는 쪽은 **4파일만** 받아 `main`에서 `protocol_loop()` 한 줄 호출하면 통합:

```
01_RX_control/Application/Src/app_protocol.c
01_RX_control/Application/Inc/app_protocol.h
_shared/oled_tv_protocol.c
_shared/oled_tv_protocol.h
```

- **자립성**: `app_protocol.c`는 `app_protocol.h`만 include — `common.h` **역의존을 끊었다**(`LOG_EN`·`tx_data_log` 삭제). `app_protocol.h`는 `main.h`·`app_spi.h`·`oled_tv_protocol.h`만 include.

## 설계 결정

- **W1 — 트랜스포트는 받는 쪽 인프라로 전제**: SPI 트랜스포트(`app_spi`: `spi_txrx_dma`, `spi_rx_ready`)는 받는 사람이 이미 가진 것으로 보고 `app_protocol`이 **직접 호출**한다. (트랜스포트를 콜백으로 추상화하지 않음)
- **D1 — 센싱/지령 데이터는 전역 extern 유지**: `rx_module`/`tx_module`/`rx_cmd`를 전역으로 두어, **비-SPI 호출처(`adc_calc`·UART·CAN)는 무수정**으로 같은 전역을 읽고 쓴다.

## 동작 변화 (의도된 정리)

- **더미 주입 토글**: `inject_rx_dummy_data()`를 호출부 **한 줄 주석 토글**로 전환. 기본은 **실센싱(`adc_calc`) 송신** — 단 `zin`/`status_byte`는 실소스가 없어 0 송신. 더미 검증 시 `exchange_packets()`의 해당 한 줄만 주석 해제.
- **모니터 상시 ON**: 구 `main`에서 주석 처리돼 있던 `Monitor_Loop()` → `print_packets()`로 흡수돼 **항상 출력**. ([[rx_control]] 메인 루프의 "Monitor_Loop 주석처리(`175a8f7`)" 미결 항목 **해소**.)
- **LINK UP/DOWN 이벤트 출력 제거**: SPI/ESB `LINK UP/DOWN` edge 콘솔 로그 삭제 — COMM 라인([[comm_state_monitoring]])과 값이 중복이라.
- **(`35b94d0`) monitor 텍스트→바이너리**: `print_packets()`가 사람용 텍스트 대신 11B 바이너리 패킷을 `uart_send()`로 송출. COMM 텍스트 라인(`print_comm_line_on_change`) 삭제, 링크 health는 0x10 d0 bit5/6으로 운반. host 파싱 도구 = [[pc_uart_gui]]. command 채널·응답 printf는 무변경.
- **죽은 코드 삭제**: `monitor_spi_diag`, `spi_ok_cnt`, `build_rx_to_tx_pkt` 래퍼, `LOG_EN`, `tx_data_log`.

## 검증

**(사실)** STM32CubeIDE 실 링크 빌드(`RX_control.elf`) **+ 실보드 동작확인 완료** (적출 2026-06-09, monitor 바이너리화 `35b94d0` 2026-06-10 — host [[pc_uart_gui]]로 파싱 확인). ✓

> ⚠️ **빌드 함정**: STM32CubeIDE는 CLI 빌드 불가(`stm32cubeidec.exe`가 GUI 서브시스템이라 콘솔 출력 없이 즉종료) — IDE에서 **Ctrl+B 직접 빌드**. CubeMX 재생성 금지 규칙 유지. → [[cubeide_cli_build_trap]]

---

## 3펌웨어 표준 패턴 (01 원형, 02·03 완료)

**01_RX_control이 원형, 02·03 적용 완료** — 02: `b92835c`(실보드 검증), 03: `1d7f71a`(빌드 ✓). **접두사**: 01(STM32)은 `app_*` 유지, 02/03(nRF52)은 nRF5 SDK 충돌 회피로 `eta_*` — [[nrf52_module_naming]].

### 모듈 분할 기준

| 모듈 | 역할 | 계층 |
|------|------|------|
| `eta_gpio` | `gpio_init`, LED_Loop, `led_write` 헬퍼 | 저수준 드라이버 |
| `eta_clock` | lfclk/hfclk/timers/millis | 저수준 드라이버 |
| `eta_uart` (`eta_uart.h`) | `uart_init`/event | 저수준 드라이버 |
| `eta_spi` | 저수준 SPIS: `spi_drv_init`, `spi_set_buffers`, `spis_event_handler` ISR | 저수준 드라이버 |
| `eta_esb` | 저수준 ESB: `esb_init`, `esb_event_handler` ISR(헤더 demux 포함), `esb_send_ack` | 저수준 드라이버 |
| `eta_protocol` | 두꺼운 응용 계층: SPI exchange + ESB ACK forwarding + comm_st 판정 + monitor, `protocol_loop()` 단일 진입점 | 응용 계층 |
| `main.c` | fault/assert/bsp/log/pwr/idle 보일러플레이트 + `main()` | 루트 |

> **(정정, `e72b86e`)** 03_TX_ble의 `SPI_Loop`는 `protocol_loop()`에서 **활성 호출**된다. 펌웨어 CLAUDE.md·`eta_protocol.h` docstring에 "SPI_Loop main에서 주석 처리"라고 남아있는 것은 낡은 설명이다 — raw-forward 전환(`e72b86e`) 시 `protocol_loop` 내 호출로 바뀌었다.

### 계층 방향 (단방향 호출)

`app_protocol`이 `app_esb`의 `esb_pkt[]`를 읽고 `esb_send_ack()` 호출,
`app_spi`의 `spi_set_buffers()` 호출 + `spis_xfer_done` 읽기.

- **`esb_pkt[]`(ESB rx 데이터) 소유권 → `app_esb`**
- **SPI 버퍼·`comm_st` 비트 소유권 → `app_protocol`**

SPI↔ESB 양방향 교차 버퍼 참조를 단방향으로 정리 — `app_protocol`이 양쪽 드라이버를 호출하는 팬인 구조.

### 릴레이 헤더 소유 원칙 — init seed (approach A)

**(원칙)** raw-forward 릴레이 노드(02_RX_ble, 03_TX_ble)는 중계하는 패킷 **헤더를 소유**해야 한다. 데이터 출처(ESB 상대방)가 아직 연결되지 않아도, init 시 릴레이 버퍼를 **valid 헤더+LEN+CRC+zero payload로 seed**해야 한다.

이유:
- **다운스트림 CRC 검증**: STM32가 수신 11B의 CRC를 검사해 불일치 패킷을 드롭한다. seed 없이 hdr=0x00 zero 패킷이 흐르면 최초 ESB 데이터 도착 전까지 **모든 SPI 트랜잭션이 드롭**된다.
- **comm_st 운반**: heartbeat 비트(bit5)가 0x10 패킷에 얹혀 흐른다. valid 패킷이 없으면 comm_st가 끊겨 [[comm_state_monitoring]] "구조적 결합"이 발생한다.

**4-MCU 양방향 릴레이(01↔02↔RF↔03↔04)에서 seed 자리:**

| 방향 | source | 미연결 증상 | seed 노드 | 커밋 |
|------|--------|-------------|----------|------|
| TX→RX (0x10/11/12) | 04가 03에 SPI로 공급 | 02가 hdr=0x00 zero 패킷 forward → 01(STM32) 드롭 | **03** `protocol_init` | `e72b86e` |
| RX→TX (0x50/51/52) | 01이 02에 SPI로 공급 | 03이 hdr=0x00 zero 패킷 ACK에 탑재 → 04(STM32) 드롭 | **02** `protocol_init` | `6fc8b92` |

seed는 실데이터가 수신되면 해당 슬롯이 통째로 덮여 **자기소멸** — 별도 해제 불필요.

**`pkt_seed_buffers()`** (`_shared`, `6fc8b92` 추출): seed 루프를 3종 헤더(0x10/11/12 또는 0x50/51/52)에 걸쳐 반복하는 공통 헬퍼. 02/03 `protocol_init`에서 방향별로 호출.

### dummy 소스 원칙 — 양 끝단 STM32만

**(원칙)** dummy 데이터 생성은 **양 끝단 STM32(01_RX_control, 04_tx_control)만** 담당한다. 중간 릴레이 BLE 칩(02_RX_ble, 03_TX_ble)은 릴레이만 수행하며 **자체 dummy 주입 금지**.

이유: 중간 노드가 dummy를 주입하면 01↔04 E2E 검증 경로에 릴레이 코드가 끼어들어, 데이터가 끝단 간 온전히 전달됐는지 확인이 불가능해진다. 04 더미 프로젝트에서 STM32가 자체 dummy를 생성하는 것은 이 원칙에 따른 것 — 02/03 코드에 dummy 생성 코드가 보이면 버그로 봐야 한다.

### 02/03 통합 범위 — 옵션 C (바이트 동일 조각만 _shared)

02(PRX)·03(PTX)는 기능 대칭이나 ESB 역할이 근본 비대칭(수동 ACK-with-payload vs 능동 송신+stall watchdog). `eta_protocol` 완전 통합(`_shared` 단일소스 + `#ifdef PTX/PRX`)은 ESB_Loop·ISR·eta_esb API 비대칭 때문에 ROI 안 맞음 → **"바이트 동일 조각만 `_shared` 헬퍼"** 선택 (옵션 C).

| 항목 | 상태 | 비고 |
|------|------|------|
| `eta_spi.c/.h` | ✓ `_shared` 공용화(`6fc8b92`) | 02/03 바이트 동일 |
| `pkt_seed_buffers()` | ✓ `_shared` 헬퍼(`6fc8b92`) | 위 "릴레이 헤더 소유 원칙" |
| `EsbCommSt` 헬퍼 | 보류 | 판정 입력(rx_cnt vs ack_cnt) 달라 ROI 미미 |
| SPI 검증 `pkt_classify` | 보류 | 02/03 사용 패턴 다름 |

Monitor_Loop 출력 게이트: `seen_mask` 출력 게이트 제거 → **매 윈도우 6줄 고정 스냅샷** (`6fc8b92`) — seed가 zero payload를 보장하므로 미수신이어도 정직한 0 출력.

### `_shared` 공개 API 표면 (`9ad338d` 기준, 세 펌웨어 공유)

| 함수 | 역할 |
|------|------|
| `pkt_checksum` | XOR 누산 체크섬. `9be1a7a`에서 static→공개 승격(02 `calc_checksum` 제거). 01의 `calc_checksum`은 **`9ad338d`에서 제거** → 세 펌웨어 통일 |
| `pkt_build_tx` / `pkt_build_rx` | TX/RX 방향 패킷 직렬화 |
| `pkt_apply_tx` | 수신 패킷 역직렬화 (01의 `apply_rx_pkt`가 래퍼로 호출) |
| `pkt_print_status_line` / `pkt_print_data_line` | 사람용 텍스트 모니터 출력 (02/03 `Monitor_Loop` 전용) |
| `pkt_rd_u16` / `pkt_rd_i16` | `data[]` 바이트 쌍 읽기 |
| `pkt_wr_u16` / `pkt_wr_i16` | `data[]` 바이트 쌍 쓰기 |
| `pkt_seed_buffers()` | forward 버퍼 3슬롯을 valid 헤더+LEN+CRC+zero payload로 seed (`6fc8b92` 추가) |
| `eta_spi.c/.h` | SPIS 저수준 드라이버 (`6fc8b92` _shared 공용화 — 02/03 바이트 동일) |

**`9ad338d`에서 제거된 심볼**: `pkt_print_comm_line`(`35b94d0`에서 호출처 소멸→orphan), `pkt_apply_rx`(참조 0건).

> ⚠️ SES 빌드 환경 함정(`.emProject` 파일 목록 하드코딩·nRF5 SDK 헤더 충돌·전처리기 매크로 스코프) → [[ses_build_conventions]]

## 관련

- [[rx_control]] — 메인 루프(`adc_proc`+`protocol_loop`)·SPI 페리·UART5
- [[spi_packet_format]] — wire 11B·내부 컨테이너 54B/43B (11B는 이제 UART에도 흐름)
- [[comm_state_monitoring]] — monitor 바이너리 전환·링크 health 0x10 d0 bit5/6·spi_status LINK/CRC
- [[pc_uart_gui]] — host 바이너리 모니터 GUI(11B 리더·buck 송신)
- [[cubeide_cli_build_trap]] — CubeIDE Ctrl+B 빌드 함정
- [[roadmaps/spi-esb-refactor]] — R1~R4 정리 트랙(코드가 추월). `_shared` 매크로 점검 `9ad338d` 완료
- [[buck_vout_ref_command_path]] — `rx_cmd` 지령 경로
