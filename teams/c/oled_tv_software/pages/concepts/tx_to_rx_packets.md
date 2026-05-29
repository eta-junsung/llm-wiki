---
tags: [concept, protocol, spi, esb, tx_to_rx]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__from-eta_tx-to_etx_rx.CSV
date: 2026-05-13
subsystem: 01_RX_control, 02_RX_esb, 03_TX_esb
---

# TX → RX 패킷 (HDR 0x10/0x11/0x12)

Tx 보드 데이터를 무선(BLE/ESB)으로 운반해 [[rx_control]] (Master)에 도달시키는 패킷군. **ESB 환경에서는 PTX(=TX_nRF) 송신, PRX(=RX_nRF) 수신 후 SPI로 전달**. 패킷 골격은 [[esb_packet_format]] 참조 (11 byte, 10 ms cyclic, Motorola).

## 0x10 — Tx 시스템 상태 비트맵

▶ Tx Module의 시스템 상태 / 운용 정보.

| Data              | 의미 (비트별, 0/1)                                                    |
| ----------------- | ---------------------------------------------------------------- |
| `Buffer[0]` Bit.0 | `Tx_Sys_Init_St` — Tx 시스템 초기화 미완료 / 완료                           |
| `Buffer[0]` Bit.1 | `Tx_Sys_Rdy_St` — 출력 준비 안됨 / 준비됨                                 |
| `Buffer[0]` Bit.2 | `Tx_Warning_St` — 정상 / Warning 전환                                |
| `Buffer[0]` Bit.3 | `Tx_Fault_St` — 정상 / Fault 전환                                    |
| `Buffer[0]` Bit.4 | `Rx_Flt_Rst_Cmd` — Rx에서 Fault Reset 지령 (High 200ms 이상 후 Low)     |
| `Buffer[0]` Bit.5 | `SPI_Comm_St` — 200ms 토글 신호 ([[comm_state_monitoring]])          |
| `Buffer[0]` Bit.6 | `BLE_Comm_St` — 0 대기/불량 / 1 페어링·운용 중 ([[comm_state_monitoring]]) |
| `Buffer[1]` Bit.0 | `TxVbus_Steady_St` — Vbus 불안정 / 안정 (정상 375~400 VDC)              |
| `Buffer[1]` Bit.1 | `TxVbus_LowerLmt` — Vbus 정상 / 하한치 이하                             |
| `Buffer[1]` Bit.2 | `TxVbus_UpperLmt` — Vbus 정상 / 상한치 초과                             |
| `Buffer[1]` Bit.3 | `TxIbus_OC` — Ibus 정상 / 과전류 초과                                   |
| `Buffer[2]` Bit.0 | `TxBuck_RunStop_St` — Tx Buck 출력 Off / On                        |
| `Buffer[2]` Bit.1 | `TxNo_Load_St` — 부하 있음(기본) / 무부하 (0.5 A 이하, 출력 On 시 진단)          |
| `Buffer[2]` Bit.2 | `TxVout_SetPoint_St` — 설정 도달 안함 / 도달                             |
| `Buffer[2]` Bit.3 | `TxCtrl_Lmt_St` — 정상 / PWM 제어가 Limit에 의해 출력 제한                   |
| `Buffer[2]` Bit.4 | `TxIout_Upper_Lmt` — 출력 전류 정상 / 상한 도달                            |
| `Buffer[6]`       | F/W Version (예: 0x0100 → Ver1.00)                                |
| 그 외               | Spare                                                            |

## 0x11 — Tx 입력측 Analog

▶ Tx Module 입력단 (DC Bus) 전압·전류.

| Data | 항목 | Type | Scale |
|---|---|---|---|
| `Buffer[0..1]` | Tx Vdc_bus 센싱 (Low, High) | Uint16 | 0.01 V (210.95 V → 21,095) |
| `Buffer[2..3]` | Tx Idc_bus 센싱 (Low, High) | Uint16 | 0.01 A (13.95 A → 1,395) |
| `Buffer[4..7]` | Spare | — | — |

## 0x12 — Tx 출력측 Analog + 온도

▶ Tx Module 출력 + 인버터 Coil 전류 + Power Stack 온도.

| Data | 항목 | Type | Scale |
|---|---|---|---|
| `Buffer[0..1]` | Tx Buck Vout 센싱 | Uint16 | 0.01 V (47.95 V → 4,795) |
| `Buffer[2..3]` | Tx Buck Iout 센싱 | Uint16 | 0.01 A (14.53 A → 1,453) |
| `Buffer[4..5]` | Tx 인버터측 Coil 전류 (RSM) | Uint16 | 0.01 A (12.99 A → 1,299) |
| `Buffer[6..7]` | Tx Power Stack 주변 온도 | Int16 | 0.01 ℃ (120.5 ℃ → 1,205) |

## 출처

- [[spi_protocol_manual_260513]]
