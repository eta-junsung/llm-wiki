---
tags: [roadmap, oled_tv_software, uart-hw-debug, living-doc]
date: 2026-06-26
---

# oled_tv_software — 01 rx control UART 활성화 (HW 엔지니어 디버그)

> 배경: HW 팀이 Rx Control Board 통신 없이 수동 테스트 중 — ADC·PWM 값 모니터링이 안 되어 디버깅 어려움. 펌웨어 플래시 + UART 연결로 [[pc_uart_gui]] 자력 모니터링 환경 제공.

---

## 0. 한 줄 요약

01_RX_control 펌웨어 플래시 + UART5 물리 연결 + pc_uart_gui 연동 → HW 엔지니어가 ADC·PWM 값 실시간 확인.

---

## 1. 시작 조건

- HW 엔지니어 셋업: Rx Power Board + Rx Regulator Control Board 연결됨 (CN1·CN2 체결)
- **Control Board: 펌웨어 미플래시** — 현 상태
- pc_uart_gui: 구현 완료([[pc_uart_gui]])

---

## 2. 단계 호

| 단계 | 달성 목표 | 완료 기준 | 상태 |
|------|-----------|-----------|------|
| **U1** | 펌웨어 플래시 | CubeIDE Ctrl+B 빌드 + ST-LINK flash 완료 | ✗ |
| **U2** | UART5 물리 연결 | PC ↔ Control Board UART 수신 확인 | ✗ |
| **U3** | pc_uart_gui ADC 값 확인 | 0x11/0x12 패킷에서 ADC 값 실시간 표시 | ✗ |
| **U4** | HW 엔지니어 인계 | 연결 절차 전달 + 자력 사용 확인 | ✗ |

> 현재 위치 → [[status]]

---

## 3. 상세

### U1 — 펌웨어 플래시

- 빌드: STM32CubeIDE **Ctrl+B 직접** ([[cubeide_cli_build_trap]] — CLI 빌드 불가)
- ST-LINK SWD: PA13(SWDIO)/PA14(SWCLK) → CON1(`STM32_SWD_CN`)

### U2 — UART5 물리 연결 옵션

**옵션 A — CON2(RS232) 경유 (Power Board 연결 시 기본 경로):**
- 전제: CN2에서 COMM_P5V(5V) 공급됨 — Power Board 연결 시 자동
- 연결: CON2 → RS232-USB 컨버터 → PC COM 포트
- 신호 레벨: RS232(±12V), 표준 RS232-USB 컨버터 사용

**옵션 B — MCU 핀 직접 프로브 (독립 테스트용):**
- PC12(UART5_TX) → USB-UART RX, PD2(UART5_RX) → USB-UART TX, GND 공통
- 전압: **3.3V 로직** — 반드시 3.3V 내압 USB-UART 사용
- TP17(SCIB_TX)/TP15(SCIB_RX)는 **5V(COMM_P5V)** — 5V 내압 어댑터 필요

### U3 — GUI 확인 항목

| GUI 패킷 | 포함 ADC | 기대 표시 |
|---------|---------|---------|
| 0x11 TX Input | VRECT(PA0), IRECT(PA1) | 핀 전압(0~3.3V) |
| 0x12 TX Output | VOUT(PA2), IOUT(PA3), TEMP1(PC4)/TEMP2(PC5) | 핀 전압(0~3.3V) |
| 0x10 TX Status | 시스템 상태 비트맵 | SPI/ESB DOWN 예상 (BLE 미연결 시) |

> ⚠️ **ADC 표시 한계**: 현재 adc_calc()는 raw→핀전압(0~3.3V) 변환만. 실물리량(VRECT 실제 전압 등)은 front-end 분압비 미적용([[adc_channel_map]] §Front-end 스케일). 핀 전압 이상이 필요하면 별도 스케일 적용 작업 검토.
>
> ⚠️ **BLE 미연결 시 SPI 거동**: 02_RX_ble 미연결 → SPI 트랜잭션 타임아웃(50ms) 후 복구. UART 모니터는 1초마다 정상 송출 — ADC 값 표시는 정상. ([[status]] §spi_tx_busy 타임아웃 복구 △)
>
> ⚠️ **TEMP SWAP**: GUI 표시 TEMP1/TEMP2가 뒤바뀔 수 있음([[adc_channel_map]] §TEMP swap).

---

## 4. 환원 후보

- Front-end 스케일 적용(VRECT/IRECT 실물리량) — HW 팀 요청 시.
