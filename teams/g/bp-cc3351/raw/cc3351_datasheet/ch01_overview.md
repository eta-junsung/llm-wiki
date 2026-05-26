# CC3350/CC3351 Datasheet — Ch01 Overview
Source: SWRS284C, April 2024 – Revised October 2025
Pages: 1–4

---

## 1 Features

### Key Features
- Wi-Fi 6 (802.11ax)
- Bluetooth® Low Energy 5.4 in CC3351 devices
- Companion IC to any processor or MCU host capable of running a TCP/IP stack
- Integrated 2.4GHz and 5GHz PA for a complete wireless solution with up to +20.5dBm output power
- Operating temperature: –40°C to +105°C
- Application throughput up to 50Mbps

### Extended Features — Wi-Fi 6
- 2.4GHz and 5GHz, 20MHz, single spatial stream
- MAC, baseband, and RF transceiver with support for IEEE 802.11 a/b/g/n/ax
- OFDMA, trigger frame, MU-MIMO (downlink), BSS coloring, TWT
- Hardware-based encryption/decryption: WPA2 and WPA3
- Multirole support (concurrent STA and AP)
- Optional antenna diversity or selection
- 3-wire or 1-wire PTA for external coexistence with additional 2.4GHz radios (Thread/Zigbee)
- Support for 4-bit SDIO or SPI host interfaces

### Extended Features — Bluetooth Low Energy 5.4
- LE coded PHYs (long range), LE 2M PHY (high speed), advertising extension
- HCI transport: UART or shared SDIO

### Security
- Secured host interface, firmware authentication, anti-rollback protection

### Power/Clock/Package
- VMAIN, VIO, Vpp: 1.8V
- VPA: 3.3V
- Fast clock: 40MHz XTAL; Slow clock: internal or external 32.768kHz
- Package: 40-pin WQFN, 5mm × 5mm, 0.4mm pitch

---

## 2 Applications
- Grid infrastructure (electricity meter, string/micro inverter, EV charging)
- Building/home automation (HVAC, thermostat, camera, garage door)
- Appliances (refrigerator, oven, washer/dryer, water heater, air purifier, vacuum robot)
- Medical (infusion pump, patient monitor, BP monitor, CPAP, ultrasound)
- Retail automation and payment
- Printers

---

## 3 Description

The SimpleLink™ Wi-Fi™ CC33xx family: single-chip Wi-Fi 6 and BLE 5.4. CC3350 and CC3351 are first dual-band devices in this pin-to-pin compatible family.

| Part | Wi-Fi 2.4/5GHz SISO | BLE |
|------|---------------------|-----|
| CC3350ENJARSBR | ✔ | — |
| CC3351ENJARSBR | ✔ | ✔ |

10th-generation connectivity combination chip from TI. Ideal for cost-sensitive embedded applications with Linux® or RTOS host running TCP/IP.

---

## 4 System Diagram (CC3351)

```
                    CC335x 2.4/5GHz Wi-Fi and BLE Companion IC
┌─────────────────────────────────────────────────────────────────────┐
│  System Power  Clock  User OTP  Packet RAM  Execution/Data RAM      │
│                                                                     │
│  Wi-Fi & BLE Core:                                                  │
│    Wi-Fi MAC/Modem │ BLE MAC/Modem │ 2.4/5GHz Wi-Fi/BLE RF         │
│    ELP │ Crypto │ DMA                                               │
│                                                                     │
│  Interfaces: SDIO/SPI │ UART │ Coexistence │ Antenna Diversity      │
└──────────────┬──────────────────────────────────┬───────────────────┘
         nReset │                           2.4GHz ANT │ 5GHz ANT
```

---

## Table of Contents (doc structure reference)

| Ch | Title | Pages |
|----|-------|-------|
| 5 | Pin Configuration and Functions | 5–7 |
| 6 | Specifications | 8–19 |
| 7 | Detailed Description | 20 |
| 8 | Applications, Implementation, and Layout | 21 |
| 9 | Device and Documentation Support | 22–24 |
| 10 | Revision History | 24 |
| 11 | Mechanical, Packaging, and Orderable Information | 25+ |
