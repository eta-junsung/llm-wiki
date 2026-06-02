---
tags: [raw, schematic, bp-cc3351, pinmap, reset, power]
source: C:\Users\echog\Downloads\spac003 (1)\Tool Folder Design Files\Schematics\BP-CC3351_Sch.PDF — Sheet 3 of 3
date: 2026-06-02
---

# BP-CC3351 회로도 Sheet 3 — LaunchPad Interface + Power + Reset

PCB Number: MCU121, Rev: B. 11/6/2023.

---

## LaunchPad Interface — P1/P2 커넥터

P1, P2는 각각 2×10핀 = 20핀 BoosterPack 커넥터.  
상세 핀 할당은 concept 페이지 [[boosterpack_pinmap]] 참조.

회로도상 신호명 (3V3 레벨, level shifter 후단):

**P1 좌측 net labels (MCU ↔ BP 인터페이스)**:
- UART_TX_3V3 (from CC3351 → MCU), LP_UART_TX, LP_RESET, SDIO_CLK_3V3, IRQ_WL_3V3, COEX_GRANT_3V3, ANT_SEL_3V3
- (P1.29/P1.30): COEX_REQ_3V3, COEX_PRIORITY_3V3

**P2 우측 net labels**:
- SDIO_D2_3V3, SDIO_D1_3V3, UART_CTS_3V3(?), UART_RTS_3V3, LOGGER_3V3, COEX_REQ_3V3, COEX_PRIORITY_3V3
- SLOW_CLK_IN_3V3, FAST_CLK_REQ_3V3, SDIO_D3_CS_3V3, SDIO_D0_POC0_3V3, SDIO_CMD_PICO_3V3, IRQ_BLE_3V3

---

## Reset 회로 (우하단 "Reset" 섹션)

```
VCC_BRD_3V3 ──R19(10k)──┬── LP_RESET ──────── [P1.5로]
                         │                      [RESET_3V3 → level shifter → RESET_1V8 → CC3351 nRESET]
                         └── Q1(BSS138) drain
                              │ gate ← R21(0Ω) ← XDS_RESET
                              │ source → GND

D1 (Yellow LED) = nRESET 상태 표시
  VCC_BRD_3V3 → D1 → R15(750Ω) → RESET_3V3 node
```

**동작 해석**:
- LP_RESET = HIGH (default, R19 pullup): CC3351 running (reset released)
- LP_RESET = LOW: CC3351 in reset (active-low)
- **MCU(AM263P)가 P1.5를 LOW 구동 → CC3351 reset 어서트**
- **MCU가 P1.5를 HIGH 구동 → CC3351 reset 해제** (WLAN_EN=HIGH = 정상 동작)
- XDS_RESET이 HIGH일 때 Q1 ON → LP_RESET 강제 LOW (XDS110 경로)

> `wlan_TurnOnWlan`에서 WLAN_EN(= AM263P PR0_PRU0_GPIO12 → P1.5)를 LOW→딜레이→HIGH 시퀀스로 reset pulse 생성.

---

## Power Management (중앙 "Power Management" 섹션)

### LDO: TPS7A8801RTR (U2, dual-output)

```
USB J7 → L3/L4(30Ω) → D2/D3(Schottky) ─┐
                                          ├→ VCC_MCU_5V (= P1.21) ─→ U2 IN1/IN2
VCC_MCU_5V from LaunchPad P1.21 ──────────┘    (Schottky OR-ing)

U2 OUT1 (1.8V) → R24(49.9Ω) → J6 jumper → VCC_BRD_1V8
U2 OUT2 (3.3V) → R16(3.57k)/R17(1.87k) → J8 jumper → VCC_BRD_3V3
```

- **J6**: 1.8V 전류 측정 점퍼 (정상 동작 시 shunt 필요)
- **J8**: 3.3V 전류 측정 점퍼
- **J15**: CC3351 1.8V 전용 전류 측정 (VCC_BRD_1V8 → J15 → VBAT_CC_1V8)
- **J16**: CC3351 3.3V 전용 전류 측정 (VCC_BRD_3V3 → J16 → VBAT_CC_3V3)

### Level Shifter 전압 설정

- J12: SDIO/SPI level shifter 전압 (3.3V or 1.8V 선택)
- J13: UART level shifter 전압
- J14: RESET/IRQ level shifter 전압
- AM263P 연결 시: MCU GPIO는 3.3V → J12/J13/J14를 3.3V로 설정

---

## XDS110 Debugger Interface (좌하단)

J11 (20핀 LP-XDS110ET 헤더):
- J11.6: SWCLK
- J11.8: SWDIO
- J11.10: RESET_1V8 (CC3351 nRESET)
- J11.12: UART_TX_1V8
- J11.14: UART_RX_1V8
- J11.16: VCC_BRD_1V8
- J11.18: VCC_BRD_5V
- GND: J11.1, J11.7, J11.13, J11.19, J11.20

J10 (ARM 10핀 SWD, 기본 미실장):
- J10.1: VCC_BRD_1V8, J10.2: SWDIO, J10.4: SWCLK, J10.10: RESET_1V8
- GND: J10.3, J10.5, J10.7, J10.9

XDS110 경로 단절 (X 표시): 현재 회로도에서 J10 SWD lines에 X(no-connect) 표시됨.
