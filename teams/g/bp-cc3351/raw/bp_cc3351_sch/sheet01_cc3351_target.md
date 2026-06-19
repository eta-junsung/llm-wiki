---
tags: [raw, schematic, bp-cc3351, cc3351]
source: C:\Users\echog\Downloads\spac003 (1)\Tool Folder Design Files\Schematics\BP-CC3351_Sch.PDF — Sheet 1 of 3
date: 2026-06-02
---

# BP-CC3351 회로도 Sheet 1 — CC3351 TARGET + RF SECTION + SoP MODES

PCB Number: MCU121, Rev: A. Drawn: Jonathan Cohen, 2/6/2024.

---

## CC3351 IC (CC3351ENJARSBR)

CC3351 41핀 IC. 핀↔신호 매핑:

| CC3351 Pin | Signal (1V8 level) | 방향 |
|---|---|---|
| 12 | VDD_MAIN_IN | Power |
| 4 | VDDA_IN1 | Power |
| 5 | VDDA_IN2 | Power |
| 17 | VIO | Power |
| 35 | VPP_IN | Power |
| 16, 20, 25 | VSS | GND |
| 41 | EP (exposed pad) | GND |
| 38 | RF_A | RF Output |
| 2 | RF_BG | RF |
| 7 (HFXT_M), ? (HFXT_P) | 40MHz XTAL | Clk |
| 35 | Slow_Clock_In | Input |
| 33 | Reset (RESET_1V8) | Input (active-low) |
| 28 | Logger (LOGGER_1V8) | Output |
| 6 | XTAL_F/EXT | — |
| 36 | TESTP/FAST_CLK_REQ/IFORCE | Output |
| 13 | UART_RX_1V8 | Input |
| 14 | UART_TX_1V8 | Output |
| 12 | UART_CTS_1V8 | Input |
| 11 | UART_RTS_1V8 | Output |
| 19 | SDIO_CLK_1V8 | Input |
| 18 | SDIO_CMD_1V8 | I/O |
| 24 | SDIO_D0_1V8 | I/O |
| 22 | SDIO_D1_1V8 | I/O |
| 23 | SDIO_D2_1V8 | I/O |
| 26 | SDIO_D3_1V8 | I/O |
| 30 | Host_IRQ_BLE (IRQ_BLE_1V8) | Output |
| 29 | Host_IRQ_WL (IRQ_WL_1V8) | Output |
| 8 | COEX_GRANT_1V8 | Output |
| 9 | COEX_PRIORITY_1V8 | I/O |
| 10 | COEX_REQ_1V8 | Input |
| 26 | SWCLK | — (SWD) |
| 27 | SWDIO | — (SWD) |
| 39, 40 | PA_LDO_IN / PA_LDO_OUT | Power (RF PA LDO) |
| 31 | DIG_LDO_OUT | Power (내부 LDO out) |
| 3 | GPIO0 | — |
| 13(?) | GPIO1 | — |
| 21 | ANT_SEL_1V8 | Output |

> 핀 번호는 schematic 이미지 시각 독해값 — datasheet [[cc3351_datasheet]] §2(Pin Configuration)로 검증 필요.

---

## 클럭

- **Y1**: 40MHz XTAL, C6=6.8pF 50V 0201, C7=6.8pF 50V 0201, R1=150Ω (series damping)
- **Y2**: 32.768kHz oscillator (LFSRX007707REEL, 4-pin SOT) — Slow_Clock_In 공급

---

## 전원 (CC3351 측 디커플링)

VBAT_CC_1V8에서 C1(1µF), C2(0.1µF), C3(0.1µF), C4(0.1µF), C8(1µF), C9(1µF) 디커플링.  
VBAT_CC_3V3에서 C5(0.1µF), R25(0Ω) 통해 VDDA_IN2.

---

## RF SECTION

- **Diplexer**: DPX167125DT-8197B1 (-40~+85°C), diplexer Low-Band/High-Band/Common 포트
  - Common → CC3351 RF_BG
  - Low-Band (2.4GHz) → chip antenna 경로
  - High-Band (5GHz) → SMA connector 경로 (기본 not connected via X marks)
- **SMA connector**: J1 (PCB.SMAFSTJ.B.HT)
- **Chip antenna**: E1 (M830520)
- **RF 매칭 커패시터**: C14(10pF COG/NP0), C16(50V), C17(50V 1.9pF), C18(50V 1.9pF) 등
- 기본 rework: 칩 안테나 사용, SMA/U.FL 사용 시 3.9pF 캐패시터 이동 필요 — [[bp_cc3351_evm_ug]] §2.5

---

## SoP MODES (Startup Mode Selection)

VCC_BRD_1V8로 pull-up 저항 + 0Ω/open 조합으로 SoP 핀 전압 결정.  
R7, R8 등 저항이 IRQ_WL_1V8, IRQ_BLE_1V8, LOGGER_1V8 측에 배치되어 있음.

> 구체적 SoP 모드 조합은 CC3351 datasheet SoP 섹션 참조. [[cc3351_datasheet]]
