# CC3350/CC3351 Datasheet — Ch04 Detailed Description & Reference Schematic
Source: SWRS284C, April 2024 – Revised October 2025
Pages: 20–21

---

## 7 Detailed Description

CC335x offers Wi-Fi 6 (802.11ax) and BLE 5.4 (CC3351 only) while maintaining compatibility with Wi-Fi 4 (802.11 a/b/g/n) and Wi-Fi 5 (802.11ac).

Ideal for cost-sensitive embedded applications with Linux or RTOS host running TCP/IP. Integrated 2.4GHz and 5GHz PA, up to +20.5dBm output power, –40°C to +105°C, 50Mbps application throughput.

BSD-3 clause software distributed in integrated ROM. License terms in product software manifest (CC33XX-Software).

### 7.1 WLAN Features
- 2.4GHz and 5GHz, 20MHz, single spatial stream
- MAC, baseband, RF transceiver: IEEE 802.11 a/b/g/n/ax
- OFDMA, trigger frame, MU-MIMO (downlink), BSS coloring, TWT
- Hardware WPA2/WPA3 encryption/decryption
- Multirole: concurrent STA and AP on different RF channels
- Optional antenna diversity or selection
- 3-wire or 1-wire PTA for coexistence (Thread, Zigbee)
- 4-bit SDIO or SPI host interfaces

### 7.2 Bluetooth Low Energy Features
- BLE 5.4
- LE coded PHYs (long range), LE 2M PHY (high speed), advertising extension
- HCI transport: UART or shared SDIO

---

## 8 Applications, Implementation, and Layout

### Reference Schematic (Figure 8-1)

Key connections from CC3351 reference design:

**Power rails:**
- VDD_MAIN_IN (pin 32), VDDA_IN1 (4), VDDA_IN2 (5) → 1V8
- PA_LDO_IN (39, 40) → 3V3
- VIO (17) → 1V8
- VPP_IN (35) → 1V8
- DIG_LDO_OUT (31) → 0.1µF + 1.0µF decoupling to GND
- PA_LDO_OUT (1) → 0.1µF + 1.0µF decoupling to GND

**Clock:**
- HFXT_P/M (6,7) → TZ3877AAA044 40MHz XTAL with 6.8pF loading caps (C10, C11)
- SLOW_CLK_IN (34) → Optional external 32.768kHz (LFSPXO073707REEL). DNP if using internal.

**RF section:**
- RF_BG (2) → 50Ω → SAW filter FL1 (DEA162450BT-1295A1) → Diplexer U1 (DPX167125DT-8197B1) Low-Band port
- RF_A (38) → 50Ω → Diplexer U1 High-Band port
- Diplexer Common_Port → antenna connector (via matching L1, L2)
- ANT_SEL (15) → antenna diversity control

**Host interface:**
- SDIO_CLK (19), SDIO_CMD (18), SDIO_D0–D3 (24,23,22,21) → host MCU
- IRQ_WL = HOST_IRQ_WL (29) → host MCU interrupt
- UART_TX/RX/CTS/RTS (14,13,12,11) → host MCU (for BLE HCI)

**Debug/Control:**
- nRESET (33) → host MCU
- SWCLK (26), SWDIO (27) → SWD debug header
- LOGGER (28) → debug UART logger output
- FAST_CLK_REQ (36) → host MCU (fast clock request signal)
- COEX_GRANT/PRIORITY/REQ (8,9,10) → coexistence interface (optional)

**Notes from schematic:**
1. Slow clock can be generated internally; external is optional for better power.
2. For antenna selection and matching, see CC33xx Hardware Integration document.
