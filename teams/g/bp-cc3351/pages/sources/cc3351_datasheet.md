---
tags: [source, cc3351, datasheet, ti, wifi6, ble]
source: cc3351-datasheet.pdf (SWRS284C)
date: 2026-05-26
---

# cc3351_datasheet — TI CC3350/CC3351 데이터시트

**문서**: SWRS284C, April 2024 – Revised October 2025 (Rev.C), 34p  
**대상 칩**: CC3350 (Wi-Fi 6 only) / CC3351 (Wi-Fi 6 + BLE 5.4), Pin-to-pin 호환  
**패키지**: 40-pin WQFN 5×5mm, 0.4mm pitch

---

## 핵심 요약

| 항목 | CC3350 | CC3351 |
|------|--------|--------|
| Wi-Fi | 2.4+5GHz 802.11ax | 2.4+5GHz 802.11ax |
| BLE | — | 5.4 (LE Coded / 2M / HCI) |
| Host I/F | SDIO 4-bit or SPI | SDIO 4-bit or SPI (+UART for BLE) |
| Op Temp | –40~125°C | –40~105°C |
| Package | 40-pin WQFN | 40-pin WQFN |

### 전원 구성
| Rail | 핀 | 전압 |
|------|----|------|
| VMAIN (SRAM/Digital) | 32 | 1.8V |
| VDDA (Analog) | 4, 5 | 1.8V |
| VIO (IO) | 17 | 1.8V |
| VPA (PA) | 39, 40 | 3.3V |
| VPP (OTP) | 35 | 1.8V |

**전원 시퀀싱**: 모든 공급 안정 → nRESET low ≥10µs → nRESET 해제

### Host Interface 핀 매핑

**SPI 모드 (Wi-Fi)**
| 신호 | 핀# | 핀명 |
|------|-----|------|
| CS (active low) | 21 | SDIO_D3 |
| SCLK (max 26MHz) | 19 | SDIO_CLK |
| PICO | 18 | SDIO_CMD |
| POCI | 24 | SDIO_D0 |
| IRQ (WLAN) | 29 | HOST_IRQ_WL |

**UART 모드 (BLE HCI, max 4364kbps)**
| 신호 | 핀# |
|------|-----|
| TX | 14 |
| RX | 13 |
| CTS | 12 |
| RTS | 11 |

### 클럭
- **Fast clock**: 40MHz XTAL 필수 (외부). HFXT_P/M 핀 (6,7). CL 5~13pF, ESR ≤40Ω
- **Slow clock**: 32.768kHz, 내부 생성 가능 (SLOW_CLK_IN 핀 34 미연결). 외부 사용 시 정밀도·전력 개선.

### 전류 소모 (대표값)
| 모드 | VMAIN | VPA |
|------|-------|-----|
| 2.4GHz TX 20dBm | ~100mA | ~270mA |
| 5GHz TX 20dBm | ~170mA | ~250mA |
| RX | 62mA | 0 |
| Sleep (RAM 유지) | 330µA | 2µA |
| Shutdown | 10µA | 2µA |

---

## Raw 챕터 인덱스

| 파일 | 내용 | 원본 페이지 |
|------|------|------------|
| [[ch01_overview]] | Features, Applications, Description, System Diagram | 1–4 |
| [[ch02_pin_config]] | Pin Diagram (40-pin), Pin Attributes 전체 표, SPI 핀맵 | 5–7 |
| [[ch03_specifications]] | AMR, ESD, Operating Conditions, 전기특성, RF 성능, 전류소모, 타이밍 (SDIO/SPI/UART) | 8–19 |
| [[ch04_description_schematic]] | WLAN/BLE 상세 설명, Reference Schematic (회로도 주요 연결) | 20–21 |
| [[ch05_support]] | Tools & Software, Documentation, Revision History | 22–24 |
| [[ch06_packaging]] | Orderable Information, T&R 치수, Package Outline | 25–34 |

---

## 파생 페이지 후보 (lazy — 필요 시 생성)

- `[[cc3351_ic]]` — 칩 entity (part number, 기본 스펙)
- `[[cc3351_pinmap]]` — 40핀 전체 기능 표, SPI/SDIO/UART/Debug 핀 분류
- `[[cc3351_power_rails]]` — VMAIN/VIO/VPA 전원 구성 + 시퀀싱 절차
- `[[cc3351_host_interface]]` — SDIO/SPI/UART 타이밍 파라미터 + 설정 가이드
