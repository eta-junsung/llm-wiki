---
tags: [source, verification, pc-gui, e2e, screenshot]
source: 실보드 스크린샷 2026-06-12 (raw/pc_uart_gui/)
date: 2026-06-12
subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble, host
---

# PC UART GUI 실보드 검증 스크린샷 (2026-06-12)

> 원본 이미지: `raw/pc_uart_gui/eta-c-oled-monitor.png`, `raw/pc_uart_gui/eta-c-oled-tx-buck-set.png`

3보드 연결(01 STM32 + 02 nRF52 RX + 03 nRF52 TX) 상태에서 GUI 전체 동작 및 TX Buck Set E2E를 실측 확인한 스크린샷 2종.

---

## 스크린샷 1 — GUI 전체 화면 (`eta-c-oled-monitor.png`)

**측정 조건**: COM17(CP210x), SPI UP + ESB UP, 3보드 정상 연결.

### 확인 사실

| 항목 | 실측값 |
|------|--------|
| 포트 | COM17, Connected |
| 링크 상태 | SPI UP, ESB UP |
| TX FW 버전 | 11.22 |
| RX FW 버전 | 33.44 |

**0x10 TX Status — 활성 비트(=1, 굵게 표시):**

| Byte | Bit | Name | 의미 |
|------|-----|------|------|
| [0] | 0 | Tx_Sys_Init_St | 초기화 완료 |
| [0] | 1 | Tx_Sys_Rdy_St | 시스템 준비 |
| [0] | 5 | SPI_Comm_St | SPI 링크 UP |
| [0] | 6 | BLE_Comm_St | ESB 링크 UP |
| [1] | 0 | TxVbus_Steady_St | TX 버스 전압 안정 |
| [2] | 0 | TxBuck_RunStop_St | TX Buck 동작 중 |

**0x11 TX Input (Physical 변환 실측):**

| Field | Raw | Physical |
|-------|-----|----------|
| Vdc_bus | 5000 | 50.00 V |
| Idc_bus | 123 | 1.23 A |

**0x12 TX Output:**

| Field | Raw | Physical |
|-------|-----|----------|
| Buck_Vout | 1200 | 12.00 V |
| Buck_Iout | 233 | 2.33 A |
| Icoil | 345 | 3.45 A |
| Stack_Temp | 450 | 45.00 °C |

**0x51 RX Input (TX Buck Set 전, Tx_Buck_Vout_Ref = 0):**

| Field | Raw | Physical |
|-------|-----|----------|
| Vrect | 175 | 1.75 V |
| Irect | 161 | 1.61 A |
| Zin | 0 | 0.00 Ω |
| Tx_Buck_Vout_Ref | 0 | 0.00 V |

**0x52 RX Output:**

| Field | Raw | Physical |
|-------|-----|----------|
| Vout | 175 | 1.75 V |
| Iout | 161 | 1.61 A |
| Stack_Temp1 | 17 | 1.70 °C |
| Stack_Temp2 | 16 | 1.60 °C |

---

## 스크린샷 2 — TX Buck Set E2E 확인 (`eta-c-oled-tx-buck-set.png`)

**측정 조건**: 동일 3보드 연결. 03_TX_ble를 SEGGER Embedded Studio + J-Link로 디버깅 중.

### E2E 경로 및 확인 결과

```
GUI 입력: 222.22 V
   ↓ [GUI] Send 버튼 → 피드백: "Sent: buck 222.22"
   ↓ UART5 → "buck 222.22\r" 문자열
01_RX_control (STM32)
   ↓ sscanf → rx_cmd.tx_buck_vout_ref = 222.22
   ↓ pkt_build_rx → 0x51 DATA[6,7] = 22222 (u16 big-endian)
   ↓ SPI Master → 02_RX_ble
02_RX_ble (nRF52)
   ↓ SPI Slave 수신 → ESB ACK payload 조립
   ↓ ESB 무선 →
03_TX_ble (nRF52) — SEGGER 디버그 터미널 확인
   0x51 Tx_Buck_Vout_Ref=22222
```

**GUI 0x51 RX Input 갱신:**

| Field | Raw | Physical |
|-------|-----|----------|
| Tx_Buck_Vout_Ref | **22222** | **222.22 V** |

**03_TX_ble SEGGER 디버그 터미널 출력 (직접 확인):**
```
0x51 Vrect=176 Irect=161 Zin=0 Tx_Buck_Vout_Ref=22222
```

### 확정 사실

- GUI → UART5 → STM32 → SPI → ESB → 03_TX_ble **E2E 경로 정상 동작**.
- `buck <v>` 명령 소수 2자리 정확 전달 (`222.22` → 22222 raw, 오차 없음).
- 실보드 3개(01/02/03) 동시 연결 상태에서 SPI UP + ESB UP 유지.

---

## 파생 페이지

- [[pc_uart_gui]] — GUI 구조·레이아웃·검증 사실
- [[buck_vout_ref_command_path]] — E2E 지령 경로
- [[comm_state_monitoring]] — 링크 health 비트 (SPI_Comm_St·BLE_Comm_St)
