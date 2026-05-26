# CC3350/CC3351 Datasheet — Ch03 Specifications
Source: SWRS284C, April 2024 – Revised October 2025
Pages: 8–19

---

## 6.1 Absolute Maximum Ratings

| Parameter | Pins | Min | Max | Unit |
|-----------|------|-----|-----|------|
| VPA (PA supply) | 39,40 | –0.5 | 4.2 (1) | V |
| VMAIN (VDD_MAIN_IN, VDDA_IN1, VDDA_IN2) | 32,4,5 | –0.5 | 2.1 | V |
| VIO | 17 | –0.5 | 2.1 | V |
| Input Voltage to all digital pins | — | –0.5 | VIO+0.5 | V |
| HFXT_P Input Voltage | 6 | –0.5 | 2.1 | V |
| VPP (OTP) | 35 | –0.5 | 2.1 | V |
| TA Operating Ambient | — | –40 | 105 | °C |
| Tstg Storage | — | –55 | 155 | °C |

(1) Above 85°C, conditions beyond recommended operating conditions may cause permanent damage.

---

## 6.2 ESD Ratings

| Model | Pins | Value | Unit |
|-------|------|-------|------|
| HBM (ANSI/ESDA/JEDEC JS-001) | RF pins | ±1000 | V |
| HBM | Other pins | ±2000 | V |
| CDM (ANSI/ESDA/JEDEC JS-002) | RF pins | ±250 | V |
| CDM | Other pins | ±500 | V |

---

## 6.3 Recommended Operating Conditions

| Parameter | Pins | Min | Typ | Max | Unit |
|-----------|------|-----|-----|-----|------|
| VMAIN (VDD_MAIN_IN, VDDA_IN1, VDDA_IN2) | 32,4,5 | 1.62 | 1.8 | 1.98 | V |
| VPA | 39,40 | 3.0 | 3.3 | 3.6 | V |
| VIO | 17 | 1.62 | 1.8 | 1.98 | V |
| VPP | 35 | 1.62 | 1.8 | 1.98 | V |
| TA | — | –40 | — | 105 (1) | °C |
| Max power dissipation | — | — | — | 2 | W |

(1) WLAN/BLE performance may degrade above 85°C.

---

## 6.4 Electrical Characteristics

| Parameter | Min | Max | Unit |
|-----------|-----|-----|------|
| VIH High Level Input | 0.65×VIO | VIO | V |
| VIL Low Level Input | 0 | 0.35×VIO | V |
| VOH High Level Output (4mA) | VIO–0.45 | VIO | V |
| VOL Low Level Output (4mA) | 0 | 0.45 | V |

---

## 6.5 Thermal Resistance

| Metric | Value | Unit |
|--------|-------|------|
| RθJA (junction-to-ambient) | 30.5 | °C/W |
| RθJC(top) | 16.7 | °C/W |
| RθJB | 10 | °C/W |
| ΨJT | 0.1 | °C/W |
| ΨJB | 10 | °C/W |
| RθJC(bot) | 1.7 | °C/W |

---

## 6.6 WLAN Performance: 2.4GHz Receiver

| Parameter | Value | Unit |
|-----------|-------|------|
| Frequency Range | 2412–2472 | MHz |
| Sensitivity 1Mbps DSSS | –98.5 | dBm |
| Sensitivity 11Mbps CCK | –90.5 | dBm |
| Sensitivity 54Mbps OFDM | –76 | dBm |
| Sensitivity HT MCS7 MM | –73.4 | dBm |
| Sensitivity HE MCS7 | –74 | dBm |
| Max input level OFDM54/MCS7 | –9 | dBm |
| RSSI Accuracy (–90 to –30 dBm) | ±3 | dB |

---

## 6.7 WLAN Performance: 2.4GHz Transmitter

| Parameter | Value | Unit |
|-----------|-------|------|
| Frequency Range | 2412–2472 | MHz |
| Max output power 1Mbps DSSS | 20.5 | dBm |
| Max output power 6Mbps OFDM | 20.2 | dBm |
| Max output power 54Mbps OFDM | 17.4 | dBm |
| Max output power HE MCS0 | 20.2 | dBm |
| Max output power HE MCS7 | 17.3 | dBm |

---

## 6.8 WLAN Performance: 5GHz Receiver

| Parameter | Value | Unit |
|-----------|-------|------|
| Frequency Range | 5180–5845 | MHz |
| Sensitivity 6Mbps OFDM | –93.2 | dBm |
| Sensitivity 54Mbps OFDM | –75.8 | dBm |
| Sensitivity HE MCS7 | –73.5 | dBm |
| RSSI Accuracy | ±3 | dB |

---

## 6.9 WLAN Performance: 5GHz Transmitter

| Parameter | Value | Unit |
|-----------|-------|------|
| Frequency Range | 5180–5845 | MHz |
| Max output power 6Mbps OFDM | 19.5 | dBm |
| Max output power 54Mbps OFDM | 15.1 | dBm |
| Max output power HE MCS0 20MHz | 19.5 | dBm |
| Max output power HE MCS7 20MHz | 15.0 | dBm |

---

## 6.10 BLE Performance: Receiver

| PHY | Sensitivity (typ) | Unit |
|-----|-------------------|------|
| 125Kbps LE Coded | –103.6 / –101.4 | dBm |
| 500Kbps LE Coded | –100.7 / –98.6 | dBm |
| 1Mbps LE 1M (37B) | –99.4 / –97.2 | dBm |
| 2Mbps LE 2M | –95.2 / –93.4 | dBm |

RSSI Accuracy: ±4 dB (–90 to –20 dBm range)

---

## 6.11 BLE Performance: Transmitter

| Parameter | Typ | Unit |
|-----------|-----|------|
| Output power (highest setting, 20dBm setting) | 17.8 | dBm |

Supported TX power settings: 0, 5, 10, 20 dBm

---

## 6.12–6.13 Current Consumption: WLAN Static Modes

### 2.4GHz
| Mode | VMAIN typ | VPA typ | Unit |
|------|-----------|---------|------|
| Continuous TX 1Mbps DSSS (20.5dBm) | 92 | 310 | mA |
| Continuous TX 6Mbps OFDM (20.2dBm) | 110 | 270 | mA |
| Continuous RX | 62 | 0 | mA |
| Continuous Listen (Beacon) | 55.5 | 0 | mA |

### 5GHz
| Mode | VMAIN typ | VPA typ | Unit |
|------|-----------|---------|------|
| Continuous TX 6Mbps OFDM (19.5dBm) | 170 | 250 | mA |
| Continuous RX | 110 | 0 | mA |
| Continuous Listen (Beacon) | 88 | 0 | mA |

Peak VPA can hit **450mA** during device calibration.
Peak VMAIN: up to 300mA (≤85°C), up to 350mA (105°C).

---

## 6.14–6.15 Current Consumption: WLAN Use Cases

### 2.4GHz (system with 3.3V DC/DC at 85% efficiency)
| Mode | Typ | Unit |
|------|-----|------|
| DTIM=1 (~102ms) | 562 | µA |
| DTIM=3 (~306ms) | 355 | µA |
| DTIM=5 (~510ms) | 313 | µA |

### 5GHz (system with 3.3V DC/DC at 85% efficiency)
| Mode | Typ | Unit |
|------|-----|------|
| DTIM=1 | 700 | µA |
| DTIM=3 | 417 | µA |
| DTIM=5 | 348 | µA |

---

## 6.16 Current Consumption: BLE Static Modes

| Mode | VMAIN typ | VPA typ | Unit |
|------|-----------|---------|------|
| TX 0dBm | 105 | 50 | mA |
| TX 10dBm | 105 | 130 | mA |
| TX 20dBm | 110 | 270 | mA |
| RX | 62 | 0 | mA |

---

## 6.17 Current Consumption: BLE Use Cases

| Mode | Typ | Unit |
|------|-----|------|
| BLE Advertise 100ms | 3029 | µA |
| BLE Connection 1s | 633 | µA |

---

## 6.18 Current Consumption: Device Modes

| Mode | VMAIN typ | VPA typ | Unit |
|------|-----------|---------|------|
| Shutdown (nReset low) | 10 | 2 | µA |
| Sleep (RAM retention) | 330 | 2 | µA |

---

## 6.19 Timing and Switching Characteristics

### 6.19.1 Power Supply Sequencing
1. All supplies (VDD_MAIN_IN, VDDA, VIO, VPA) must be available **before** nReset is released.
2. For external slow clock: clock must be stable before nReset deasserted.
3. nReset must be held low for **at least 10µs** after power supply stabilization.

### 6.19.2 Clocking Specifications
- Fast clock: 40MHz for WLAN/BLE
- Slow clock: 32.768kHz for low-power modes (internal or external)

#### External Slow Clock Requirements
| Parameter | Min | Typ | Max | Unit |
|-----------|-----|-----|-----|------|
| Frequency (square wave) | — | 32768 | — | Hz |
| Frequency accuracy | — | — | ±250 | ppm |
| Duty cycle | 30% | 50% | 70% | — |
| Rise/fall time (10–90%) | — | — | 100 | ns |
| VIL | 0 | — | 0.35×VIO | V |
| VIH | 0.65×VIO | — | 1.95 | V |
| Input impedance | — | — | 1 | MΩ |
| Input capacitance | — | — | 5 | pF |

#### External Fast Clock (XTAL) Specifications
| Parameter | Min | Typ | Max | Unit |
|-----------|-----|-----|-----|------|
| Frequency | — | 40 | — | MHz |
| Frequency accuracy | — | — | ±20 | ppm |
| Load Capacitance CL (1) | 5 | — | 13 | pF |
| ESR | — | — | 40 | Ω |
| Drive level | — | — | 100 | µW |

(1) CL = [C1×C2]/[C1+C2] + CP. Example: C1=C2=6.2pF, CP=2pF → CL=5pF.

---

## 6.20 Interface Timing Characteristics

### 6.20.1 SDIO — Default Speed (max 26MHz)

| Parameter | Min | Max | Unit |
|-----------|-----|-----|------|
| fclock | — | 26 | MHz |
| tHigh / tLow | 10 | — | ns |
| tISU (setup, input before CLK↑) | 5 | — | ns |
| tIH (hold after CLK↑) | 5 | — | ns |
| tODLY (CLK↓ to output valid) | 2 | 14 | ns |
| CL | 15 | 40 | pF |

### 6.20.1 SDIO — High Speed (max 52MHz)

| Parameter | Min | Max | Unit |
|-----------|-----|-----|------|
| fclock | — | 52 | MHz |
| tHigh / tLow | 7 | — | ns |
| tTLH / tTHL | 3 | — | ns |
| tISU | 6 | — | ns |
| tIH | 2 | — | ns |
| tODLY (CLK↑ to output valid) | 2 | 14 | ns |

### 6.20.2 SPI (max 26MHz)

| Parameter | Min | Max | Unit |
|-----------|-----|-----|------|
| fclock | — | 26 | MHz |
| tHigh / tLow | 10 | — | ns |
| tTLH / tTHL | 3 | — | ns |
| tCSsu (CS valid before CLK↑) | 3 | — | ns |
| tISU (PICO valid before CLK↑) | 3 | — | ns |
| tIH (PICO hold after CLK↑) | 3 | — | ns |
| tDr/tDf Active (CLK→output valid) | 2 | 10 | ns |
| tDr/tDf Sleep | 12 | — | ns |
| CL | 15 | 40 | pF |

### 6.20.3 UART (BLE HCI) — 4-Wire

| Parameter | Min | Max | Unit |
|-----------|-----|-----|------|
| Baud rate | 37.5 | 4364 | kbps |
| Baud rate accuracy per byte | –2.5% | +1.5% | — |
| CTS low to TX_DATA on | 0 | 2 | ms |
| RTS high to RX_DATA off (FIFO 1/4) | — | 16 | byte |
