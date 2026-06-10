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

보조 static: `calc_checksum`(static 강등), `apply_rx_pkt`(공유 `pkt_apply_tx` 래퍼 + 01 전용 hb/ble_comm/rx_flt_rst 추출), `build_tx_status_d0`, `inject_rx_dummy_data`.

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

## 관련

- [[rx_control]] — 메인 루프(`adc_proc`+`protocol_loop`)·SPI 페리·UART5
- [[spi_packet_format]] — wire 11B·내부 컨테이너 54B/43B (11B는 이제 UART에도 흐름)
- [[comm_state_monitoring]] — monitor 바이너리 전환·링크 health 0x10 d0 bit5/6·spi_status LINK/CRC
- [[pc_uart_gui]] — host 바이너리 모니터 GUI(11B 리더·buck 송신)
- [[cubeide_cli_build_trap]] — CubeIDE Ctrl+B 빌드 함정
- [[roadmaps/spi-esb-refactor]] — R1~R4 정리 트랙(코드가 추월) + §6 `_shared` 매크로 소유권 점검
- [[buck_vout_ref_command_path]] — `rx_cmd` 지령 경로
