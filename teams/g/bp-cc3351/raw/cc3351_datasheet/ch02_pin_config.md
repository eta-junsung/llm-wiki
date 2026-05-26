# CC3350/CC3351 Datasheet — Ch02 Pin Configuration and Functions
Source: SWRS284C, April 2024 – Revised October 2025
Pages: 5–7

---

## 5.1 Pin Diagram (40-pin WQFN)

Pin numbering goes counter-clockwise from pin 1 (PA_LDO_OUT, top-left).

| Side | Pins |
|------|------|
| Left (bottom→top) | 1 PA_LDO_OUT, 2 RF_BG, 3 GND, 4 VDDA_IN1, 5 VDDA_IN2, 6 HFXT_P, 7 HFXT_M, 8 COEX_GRANT, 9 COEX_PRIORITY, 10 COEX_REQ |
| Bottom (left→right) | 11 UART RTS, 12 UART CTS, 13 UART RX, 14 UART TX, 15 ANT_SEL, 16 GND, 17 VIO, 18 SDIO CMD, 19 SDIO CLK, 20 GND |
| Right (bottom→top) | 21 SDIO D3, 22 SDIO D2, 23 SDIO D1, 24 SDIO D0, 25 GND, 26 SWCLK, 27 SWDIO, 28 LOGGER, 29 HOST_IRQ_WL, 30 HOST_IRQ_BLE |
| Top (right→left) | 31 DIG_LDO_OUT, 32 VDD_MAIN_IN, 33 nRESET, 34 SLOW_CLK_IN, 35 VPP_IN, 36 FAST_CLK_REQ, 37 GND, 38 RF_A, 39 PA_LDO_IN, 40 PA_LDO_IN |
| Exposed pad | 41 EP (GND thermal pad) |

---

## 5.2 Pin Attributes (Table 5-1)

| Pin | Signal Name | Type | Dir | Voltage | Shutdown State | After Power-Up | Description |
|-----|-------------|------|-----|---------|----------------|----------------|-------------|
| 1 | PA_LDO_OUT | Analog | O | — | — | — | RF PA LDO output |
| 2 | RF_BG | RF | I/O | — | — | — | BLE and WLAN 2.4GHz RF port |
| 3 | GND | GND | — | — | — | — | Ground |
| 4 | VDDA_IN1 | POW | — | — | — | — | 1.8V supply for analog domain |
| 5 | VDDA_IN2 | POW | — | — | — | — | 1.8V supply for analog domain |
| 6 | HFXT_P | Analog | — | — | — | — | XTAL_P (40MHz) |
| 7 | HFXT_M | Analog | — | — | — | — | XTAL_N (40MHz) |
| 8 | COEX_GRANT (2) | Digital | O | VIO | PD | PD | External coexistence — grant |
| 9 | COEX_PRIORITY (2) | Digital | I | VIO | PU | PU | External coexistence — priority |
| 10 | COEX_REQ (2) | Digital | I | VIO | PU | PU | External coexistence — request |
| 11 | UART RTS | Digital | O | VIO | PU | PU | Flow control for BLE HCI |
| 12 | UART CTS | Digital | I | VIO | PU | PU | Flow control for BLE HCI |
| 13 | UART RX | Digital | I | VIO | PU | PU | UART RX for BLE HCI |
| 14 | UART TX | Digital | O | VIO | PU | PU | UART TX for BLE HCI |
| 15 | ANT_SEL (2) | Digital | O | VIO | PD | PD | Antenna select control line |
| 16 | GND | GND | — | — | — | — | Ground |
| 17 | VIO | POW | — | — | — | — | 1.8V IO supply |
| 18 | SDIO CMD | Digital | I/O | VIO | HiZ | HiZ | SDIO command **or SPI PICO** |
| 19 | SDIO CLK | Digital | I | VIO | HiZ | HiZ | SDIO clock **or SPI clock** |
| 20 | GND | GND | — | — | — | — | Ground |
| 21 | SDIO D3 | Digital | I/O | VIO | HiZ | PU | SDIO data D3 **or SPI CS** |
| 22 | SDIO D2 | Digital | I/O | VIO | HiZ | HiZ | SDIO data D2 |
| 23 | SDIO D1 | Digital | I/O | VIO | HiZ | HiZ | SDIO data D1 |
| 24 | SDIO D0 | Digital | I/O | VIO | HiZ | HiZ | SDIO data D0 **or SPI POCI** |
| 25 | GND | GND | — | — | — | — | Ground |
| 26 | SWCLK | Digital | I | VIO | PD | PD | Serial wire debug clock |
| 27 | SWDIO | Digital | I/O | VIO | PU | PU | Serial wire debug I/O |
| 28 | LOGGER (3) | Digital | O | VIO | PU | PU | Tracer (UART TX debug logger) |
| 29 | HOST_IRQ_WL (3) | Digital | O | VIO | PD | 0 | Interrupt request to host for WLAN |
| 30 | HOST_IRQ_BLE | Digital | O | VIO | PD | PD | Reserved for future use |
| 31 | DIG_LDO_OUT | Analog | O | — | — | — | Digital LDO output (decoupling cap) |
| 32 | VDD_MAIN_IN | POW | — | — | — | — | 1.8V supply for SRAM and digital |
| 33 | nRESET | Digital | I | VIO | PD | PD | Reset (active low) |
| 34 | SLOW_CLK_IN | Digital | I | VIO | PD | PD | 32.768kHz RTC clock input |
| 35 | VPP_IN | POW | — | — | — | — | 1.8V OTP programming input supply |
| 36 | FAST_CLK_REQ | Digital | O | VIO | PD | PD | Fast clock request from device |
| 37 | GND | GND | — | — | — | — | Ground |
| 38 | RF_A | RF | — | — | — | — | WLAN 5GHz RF port |
| 39 | PA_LDO_IN | POW | — | — | — | — | 3.3V supply for PA |
| 40 | PA_LDO_IN | POW | — | — | — | — | 3.3V supply for PA |
| 41 | EP | GND | — | — | — | — | Exposed thermal pad |

**Notes:**
1. All digital I/Os (except SDIO signals) are Hi-Z in Shutdown mode with internal PU/PD per shutdown state column.
2. See software release notes for support level.
3. LOGGER and HOST_IRQ_WL are sensed by device during boot — see CC33xx Hardware Integration.

### SPI mode pin mapping summary
| SPI signal | CC3351 pin | Pin# |
|------------|-----------|------|
| CS (active low) | SDIO_D3 | 21 |
| SCLK | SDIO_CLK | 19 |
| PICO (host→device) | SDIO_CMD | 18 |
| POCI (device→host) | SDIO_D0 | 24 |
| IRQ | HOST_IRQ_WL | 29 |
