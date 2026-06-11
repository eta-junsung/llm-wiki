---
tags: [concept, tool, pc-gui, uart, monitor, host, 8kw-ev-wpt-tx]
source: 펌웨어 repo branch uart5 (commit ba241fa·979699d, tools/gui/gui.py) + 실보드 검증 2026-06-11
date: 2026-06-11
subsystem: 8kw-ev-wpt-tx, host
---

# PC 모니터 GUI — 8kW WPT TX ADC 텔레메트리 호스트 툴

LP-AM263P 8kW WPT TX 보드가 UART5로 송출하는 ADC 6채널 텔레메트리를 받아 실시간 표시·플롯·로깅하는 PC 호스트 GUI. 펌웨어 변경 없이 [[uart5_packet_protocol]] 18B 바이너리 스트림을 소비하는 단방향 모니터. branch `uart5`(commit `ba241fa`·`979699d`), 실보드 검증 2026-06-11.

- **파일**: `tools/gui/gui.py`
- **스택**: Python + pyserial + Tkinter + matplotlib
- **전제**: 보드 UART5 출력이 [[uart5_packet_protocol]]대로 18B 바이너리. 이 GUI가 그 스트림의 소비처.
- 선례 = c팀 oled [[pc_uart_gui]](단일 포트 송수신·buck 지령). 이 8kw GUI는 **수신 전용**(지령 입력 없음)이라 더 단순.

## 표시 — 4컬럼 표

| 컬럼 | 내용 |
|------|------|
| Channel | 채널 이름(ch0..ch5) |
| ADC (V) | `mV/1000` 소수 2자리 |
| ADC (12bits) | raw count(0~4095) |
| Physical | 채널별 계수로 산출한 물리량(°C/V/A) |

- mV는 펌웨어 정수식 `raw*3300/4095`를 호스트가 미러해 파생([[uart5_packet_protocol]] §thin device, smart host).
- 필드 행 고정, 값만 in-place 갱신.

## Physical 컬럼 — 계수 테이블 단일 소스

- 채널별 변환 계수를 **테이블 한 곳**에서 관리해 Physical 값을 산출.
- **계수 미입수** 상태라 현재: GA_Vin = `— V`, 전류 3채널(I_LCC_SEN/I_COIL_SEN/GA_Iin_SEN) = `— A`, 온도(Temp_Module1/2) = `—`.
- 센서 스펙([[adc_pinmap]] §미확인 — 온도 V/°C, GA_Vin 분압비, 전류 mV/A·오프셋) 입수 시 **이 테이블 한 곳만** 수정하면 전 채널 반영.

## 기능

- **채널 체크박스**: 각 채널의 **플롯 트레이스 + CSV 로깅 포함**을 토글(기본 전체 ON).
- **패킷 헬스**: 레이트(Hz) / SEQ 드롭 / CRC 에러 카운트 표시.
- **라이브 플롯**: matplotlib 실시간 트레이스.
- **CSV 로깅**: **raw-only**(파생값 아님)로 기록 — 원본 보존, 재해석 가능.
- **배포**: PyInstaller 단일 exe(`8kw-gui.spec`). `dist`/`build`는 gitignore.

## 패킷 리더 — SOF 동기 + CRC 재동기

수신 스트림에서 18B를 떼어내는 핵심 로직([[uart5_packet_protocol]] §수신측 재동기와 동일 계약):

- SOF(0xA5) 탐색 → LEN/TYPE 게이트 → CRC-16/CCITT-FALSE 검증 → 실패 시 1바이트 슬라이드 재시도.
- 슬라이딩으로 ASCII 잡음·가짜 SOF는 자연 폐기 — 별도 필터 불필요.

## 검증 (실보드, 2026-06-11)

**(사실)** COM13(CP210x, J1.4→THVD1400→J24 경로) 29.8 s 관찰: **10.067 Hz, 301프레임 전부 유효, SEQ 드롭 0 · CRC 에러 0**.

프레이밍 강건성(gui.py 운영 파서로 직접 검증):
- 정상 디코드 ✓
- 1바이트 손상 → 리젝트 + 재동기 ✓
- ASCII 잡음·가짜 SOF → 게이트 폐기 후 복구 ✓

모두 PASS.

## 빈자리 (미검증/잔여)

- **Physical 컬럼 placeholder** — 물리량 변환 계수 미입수(GA_Vin 분압비, 전류 shunt/게인, 온도 특성). raw/mV가 현재 종착점.
- UART5가 온보드 XDS110 가상 COM에 안 실려 **외부 CP210x(COM13)로만** PC 도달.

## 관련

- [[uart5_packet_protocol]] — 18B wire 프레임·CRC·재동기 계약(펌웨어 측)
- [[adc_pinmap]] — ADC 6채널·계수 입수 시 채울 스펙 목록
- [[pc_uart_gui]] — c팀 oled 선례(Tkinter+pyserial, 양방향·buck 송신)
