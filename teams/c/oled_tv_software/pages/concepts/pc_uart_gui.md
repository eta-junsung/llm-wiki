---
tags: [concept, tool, pc-gui, uart, monitor, host]
source: projects/c/oled_tv_software (esb 35b94d0, tools/pc_uart_gui/uart_gui.py) + 실보드 검증 2026-06-10
date: 2026-06-10
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

## 레이아웃

- **2컬럼 세로 배치**: 좌 = TX 패킷(0x10/0x11/0x12), 우 = RX 패킷(0x50/0x51/0x52).
- 필드 이름을 **사전 표기**하고 값만 갱신(필드 행이 고정, 값이 in-place 업데이트).
- **링크 표시**: `Link: SPI [UP/DOWN] ESB [UP/DOWN/-]` — 0x10 status 패킷 d0 **bit5(SPI_Comm_St)/bit6(BLE_Comm_St)**에서 읽는다([[comm_state_monitoring]]). 이게 host가 링크 health를 보는 단일 소스(구 COMM 텍스트 라인 대체).

## buck 지령 입력

- 입력칸 2개(정수부 . 소수2자리) → `buck <v>\r`로 UART5 송신.
- 경로·스케일은 [[buck_vout_ref_command_path]] 그대로: `buck <v>` → 0x51 `DATA[6,7]` = volts×100 (big-endian) → SPI → ESB → 03.
- **확인**: 텍스트 응답이 아니라 GUI가 파싱한 **0x51 `Tx_Buck_Vout_Ref`(volts×100)**로 (예: 123.34 → 12334).
- 소수 입력이 깨지지 않으려면 01 빌드에 newlib-nano float scanf가 켜져 있어야 함 — [[cubeide_newlib_nano_float]].

## 검증

**(사실)** 실보드 검증 완료(2026-06-10, `35b94d0`): 단일 포트 송수신, 11B 파싱·CRC 재동기, 헤더별 값 갱신, buck 송신·0x51 반영 확인.

- **(검증 항목)** SPI 끊김 시 0x10 d0 bit5가 정확히 0으로 떨어져 `Link: SPI DOWN`이 뜨는지 — 실보드 확인 대상([[comm_state_monitoring]] 보류 절).

## 관련

- [[comm_state_monitoring]] — monitor 바이너리 전환·링크 health 0x10 d0 bit5/6 (펌웨어 측)
- [[app_protocol_module]] — `print_packets` 바이너리화·`uart_send` (01 송출 측)
- [[spi_packet_format]] — 11B wire 프레임·인코딩
- [[buck_vout_ref_command_path]] — buck 지령 end-to-end 경로
- [[uart_command_set]] — UART5 command 채널(host→01)
- [[roadmaps/pc-gui]] — 작업 로드맵(G0~G3)
- [[cubeide_cli_build_trap]] — 01 펌웨어 빌드 함정
