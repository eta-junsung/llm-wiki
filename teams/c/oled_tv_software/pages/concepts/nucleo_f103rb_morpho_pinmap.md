---
tags: [concept, reference, pinmap, nucleo, stm32f103]
source: 2026-06-18 핀맵 이미지 직독 (NUCLEO-F103RB)
date: 2026-06-18
subsystem: 04_tx_control
---

# NUCLEO-F103RB 모르포 커넥터 핀맵

ST Nucleo-64 폼팩터, STM32F103RBT6. 이미지 직독 기준 (2026-06-18).

> ⚠️ ST 공식 출처: UM1724 (Nucleo-64 User Manual). 이 페이지는 이미지 직독 값 — 의심 핀은 UM1724 원본 대조.

---

## CN10 — 우측 외곽 모르포 (38핀)

| CN10 핀 | 신호 | 비고 |
|---------|------|------|
| 1 | PC8 | |
| 2 | PC9 | (CN5 side) |
| 3 | PC6 | |
| 4 | PC5 | (CN5 side) |
| 5 | PC5 | |
| 6 | U5V | (CN5 side) |
| 7 | U5V | |
| 8 | — | (CN5 side) |
| 9 | NC | |
| 10 | NC | (CN5 side) |
| 11 | — | |
| 12 | PA12 | (CN5 side) |
| 13 | PA12 | |
| 14 | PA11 | (CN5 side) |
| 15 | PA11 | |
| **16** | **PB12** | **SPI2 NSS (CS) ← 04_tx_control** |
| 17 | — | (CN5 side) |
| 18 | PB11 | (CN5 side) |
| 19 | PB11 | |
| 20 | GND | |
| 21 | GND | (CN5 side) |
| 22 | PB2 | (CN5 side) |
| 23 | PB2 | |
| 24 | PB1 | (CN5 side) |
| 25 | PB1 | |
| **26** | **PB15** | **SPI2 MOSI (STM32→nRF) ← 04_tx_control** |
| 27 | — | (CN5 side) |
| **28** | **PB14** | **SPI2 MISO (nRF→STM32) ← 04_tx_control** |
| 29 | — | (CN5 side) |
| **30** | **PB13** | **SPI2 SCK ← 04_tx_control** |
| 31 | — | (CN5 side) |
| 32 | AGND | |
| 33 | AGND | (CN5 side) |
| 34 | PC4 | |
| 35 | PC4 | (CN5 side) |
| 36 | NC | |
| 37 | NC | (CN5 side) |
| 38 | NC | |

> ⚠️ 표의 CN5/CN10 배치가 정확하지 않을 수 있음 — 이미지 직독이라 짝수/홀수 할당 오류 가능성 있음. **실물 실크 직독이 우선**.

---

## 04_tx_control 핵심 핀 요약

| 기능 | 신호 | STM32 핀 | CN10 위치 | 비고 |
|------|------|----------|-----------|------|
| SPI2 CS | NSS | PB12 | **CN10-16** | active LOW |
| SPI2 SCK | SCK | PB13 | **CN10-30** | |
| SPI2 MISO | MISO | PB14 | **CN10-28** | ⚠️ 미연결 시 전부 0xFF |
| SPI2 MOSI | MOSI | PB15 | **CN10-26** | |
| USART2 TX | PA2 | PA2 | CN9 / Arduino D1 | VCP → ST-Link USB |
| USART2 RX | PA3 | PA3 | CN9 / Arduino D0 | VCP → ST-Link USB |

03 nRF 쪽 대응 핀: P0.22(NSS) / P0.27(SCK) / P0.26(MISO) / P0.25(MOSI). → [[spi_pin_mapping]]

---

## CN7 — 좌측 외곽 모르포 (주요 핀)

| 신호 | 비고 |
|------|------|
| PC10, PC12 | |
| VDD | |
| BOOT0 | |
| PA13, PA14, PA15 | SWD: SWDIO=PA13, SWDCLK=PA14 |
| PB7 | |
| PC13 | User LED (LD2=PA5 on Nucleo-64 표준, 단 F103RB는 PA5 또는 PB13 가능) |
| PC14, PC15 | OSC32 |
| PD0, PD1 | OSC |
| VBAT, PC2, PC3 | |

## CN6 — 좌측 내곽 / Arduino 좌측 (주요 핀)

| 신호 | 비고 |
|------|------|
| IOREF | |
| RESET | |
| +3V3 | 3.3V 출력 |
| +5V | 5V 출력 |
| GND | |
| VIN | 외부 입력 |
| PA0~PA4, PB0, PC0~PC1 | Arduino A0~A5 |

## CN5 (Arduino 우측 상단) / CN9 (Arduino 우측 하단)

| Arduino | 신호 | 비고 |
|---------|------|------|
| D15 | PB8 | |
| D14 | PB9 | |
| D13 | PA5 | SPI1 SCK (User LED on Nucleo-64 일부) |
| D12 | PA6 | SPI1 MISO |
| D11 | PA7 | SPI1 MOSI |
| D10 | PB6 | |
| D9 | PC7 | |
| D8 | PA9 | USART1 TX |
| D7 | PA8 | |
| D6 | PB10 | |
| D5 | PB4 | |
| D4 | PB5 | |
| D3 | PB3 | |
| D2 | PA10 | USART1 RX |
| **D1** | **PA2** | **USART2 TX → ST-Link VCP** |
| **D0** | **PA3** | **USART2 RX → ST-Link VCP** |

---

## 관련

- [[spi_pin_mapping]] — 04↔03 SPI 배선 표 (CN10 핀번호 포함)
- [[st_link_nrf52_flash]] — 플래싱 절차
