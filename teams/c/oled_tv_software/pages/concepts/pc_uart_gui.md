---
tags: [concept, tool, pc-gui, uart, monitor, host]
source: projects/c/oled_tv_software (esb 35b94d0, tools/pc_uart_gui/uart_gui.py) + 실보드 검증 2026-06-10 + E2E 스크린샷 2026-06-12
date: 2026-06-12
subsystem: 01_RX_control, host
---

# PC UART GUI — 01_RX_control 바이너리 모니터 + buck 지령 호스트 툴

01_RX_control과 **UART5 단일 포트**로 연결되는 PC 호스트 GUI. 01이 바이너리로 송출하는 11B 패킷을 파싱해 실시간 모니터링하고, `buck` 지령을 입력해 보낸다. 펌웨어 변경 없이 기존 UART 인터페이스 위에 얹는 툴 — [[roadmaps/pc-gui]] 작업의 산출물(G0~G3 완료). 커밋 `35b94d0`(esb, 2026-06-10 실보드 검증).

- **파일**: `tools/pc_uart_gui/uart_gui.py`
- **스택**: Python + Tkinter + pyserial
- **전제**: 01 모니터 출력이 텍스트→11B 바이너리로 전환됨([[comm_state_monitoring]] "monitor 바이너리 전환"). 이 GUI는 그 바이너리 스트림의 소비처.

## 단일 포트 송수신

UART5(115200/8N1) 한 포트로 송신(buck 지령)·수신(모니터)을 모두 처리한다. 01쪽에서 **바이너리 모니터 송출 + command 응답 텍스트(`buck=.. V` 등)**가 한 포트에 섞여 나오므로, 리더가 이를 분리해야 한다.

## 11B 바이너리 리더 — HDR 동기 + CRC 재동기

수신 스트림에서 11B 패킷을 떼어내는 핵심 로직:

- **프레임**: `[HDR][LEN=0x08][DATA[8]][CRC]` 11B 고정 ([[spi_packet_format]]). big-endian, 전압·전류 scale 0.01.
- **CRC**: `pkt_checksum` = `data[0..9]` XOR (펌웨어 체크섬 함수를 host로 포팅).
- **재동기**: CRC 실패 또는 HDR 불일치 시 **1바이트 슬라이드 후 재시도**. 이 슬라이딩 덕에 command 응답 텍스트(`buck=.. V`) 같은 비-패킷 잡음은 HDR/CRC가 안 맞아 **자연 폐기**된다 — 별도 필터 불필요.
- **유효 HDR**: TX→RX 0x10/0x11/0x12, RX→TX 0x50/0x51/0x52.

## 레이아웃 — 6패널 2×3 그리드

**2컬럼 × 3행** 구성. 좌 열 = TX 패킷(01_RX_control 수집), 우 열 = RX 패킷(03_TX_ble→02→01 경유).

```
┌──────────────────┬──────────────────┐
│  0x10 TX Status  │  0x50 RX Status  │
├──────────────────┼──────────────────┤
│  0x11 TX Input   │  0x51 RX Input   │
├──────────────────┼──────────────────┤
│  0x12 TX Output  │  0x52 RX Output  │
└──────────────────┴──────────────────┘
```

### 상태 패킷 (0x10 / 0x50)

- **FW 버전 표시**: 패킷 내 FW 버전 필드를 상단에 `FW: XX.YY` 형식으로 표시 (실측: TX 11.22 / RX 33.44).
- **비트 테이블**: Byte / Bit / Name / Val 4열. **값=1인 행은 굵게** 강조 — 활성 상태를 즉시 식별.
- TX 0x10 실측 활성 비트: `Tx_Sys_Init_St`·`Tx_Sys_Rdy_St`·`SPI_Comm_St`·`BLE_Comm_St`·`TxVbus_Steady_St`·`TxBuck_RunStop_St` (= 1).

### 입출력 패킷 (0x11/0x12 / 0x51/0x52)

- **Field / Raw / Physical** 3열 테이블.
- **Physical 변환 구현됨** (스케일 계수 테이블 단일 소스):

| 신호 유형 | 스케일 | 단위 | 예시 |
|-----------|--------|------|------|
| 전압 (Vdc_bus, Buck_Vout, Vrect, Tx_Buck_Vout_Ref …) | raw × 0.01 | V | 1200 → 12.00 V |
| 전류 (Idc_bus, Buck_Iout, Icoil, Irect …) | raw × 0.01 | A | 233 → 2.33 A |
| 임피던스 (Zin) | raw × 0.01 | Ω | 0 → 0.00 Ω |
| 온도 (Stack_Temp …) | raw × 0.1 | °C | 450 → 45.00 °C |

### 상단 툴바

- **Port 드롭다운 + Refresh / Disconnect 버튼** — COM 포트 선택·재연결.
- **Link 상태**: `Link: SPI [UP/DOWN]  ESB [UP/DOWN]` — 0x10 d0 **bit5(SPI_Comm_St)/bit6(BLE_Comm_St)**에서 실시간 갱신([[comm_state_monitoring]]).

## buck 지령 입력

- **입력 필드**: 정수부 · 소수2자리, `Tx Buck Converter Vout Ref Set (0.00 ~ 300.00)` 레이블.
- **전송**: `Send` 버튼 → `buck <v>\r` UART5 송신 → `Sent: buck <v>` 파란 텍스트로 피드백.
- **확인 경로**: [[buck_vout_ref_command_path]] 그대로 — `buck <v>` → 0x51 `DATA[6,7]` = volts×100 → SPI → ESB → 03 → GUI `0x51 Tx_Buck_Vout_Ref` raw·Physical 갱신.
- 소수 입력이 깨지지 않으려면 01 빌드에 newlib-nano float scanf가 켜져 있어야 함 — [[cubeide_newlib_nano_float]].

## 검증

**(사실)** 실보드 검증 완료 (2026-06-10, `35b94d0`): COM13(CP210x), 10.067Hz, 301프레임, SEQ드롭 0·CRC에러 0.

**(사실)** SPI DOWN / ESB DOWN 표시 동작 확인 (2026-06-12): 각 링크 단절 시 상단 링크 표시가 붉은색 DOWN으로 전환됨. 스크린샷: `raw/pc_uart_gui/eta-c-oled-spi-down.png`, `raw/pc_uart_gui/eta-c-oled-esb-down.png`.

> ⚠️ **더미 데이터**: 위 스크린샷의 수치(Physical 값·FW 버전)는 **펌웨어 더미 데이터** — Physical 변환 로직(스케일 계수)은 구현 완료됐으나 실제 센서값 아님. 실 데이터는 향후 센서 캘리브레이션 단계에서 교체.

**(사실)** TX Buck Set E2E 실측 확인 (2026-06-12, COM17, 3보드 연결):
- GUI 입력 `222.22 V` → `Send` → `Sent: buck 222.22` 피드백.
- 0x51 `Tx_Buck_Vout_Ref`: Raw=22222, Physical=222.22 V.
- 03_TX_ble SEGGER 디버그 터미널: `Tx_Buck_Vout_Ref=22222` 직접 확인.
- SPI UP + ESB UP 동시 확인.
- 검증 스크린샷·상세 기록: [[pc_uart_gui_verification_260612]] (`raw/pc_uart_gui/eta-c-oled-monitor.png`, `eta-c-oled-tx-buck-set.png`).

**(검증 대기)** SPI 끊김 시 0x10 d0 bit5가 정확히 0으로 떨어져 `Link: SPI DOWN`이 뜨는지 — 실보드 확인 대상([[comm_state_monitoring]] 보류 절).

## 관련

- [[comm_state_monitoring]] — monitor 바이너리 전환·링크 health 0x10 d0 bit5/6 (펌웨어 측)
- [[app_protocol_module]] — `print_packets` 바이너리화·`uart_send` (01 송출 측)
- [[spi_packet_format]] — 11B wire 프레임·인코딩
- [[buck_vout_ref_command_path]] — buck 지령 end-to-end 경로
- [[uart_command_set]] — UART5 command 채널(host→01)
- [[roadmaps/pc-gui]] — 작업 로드맵(G0~G3)
- [[cubeide_cli_build_trap]] — 01 펌웨어 빌드 함정
