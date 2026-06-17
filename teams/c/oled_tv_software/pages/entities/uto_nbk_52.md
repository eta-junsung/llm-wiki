---
tags: [entity, board, nrf52832, custom_board]
source: 2026-06-17 실측 (핀 게이트 대조, FICR DEVICEID, LED 검증)
date: 2026-06-17
subsystem: 02_RX_ble, 03_TX_ble
---

# UTO-NBK-52 (커스텀 nRF52832 모듈)

## 개요

oled_tv_software 02_RX_ble·03_TX_ble에 사용하는 커스텀 nRF52832 모듈.

> ⚠️ **NBL vs NBK**: 기존 wiki([[schematic_ble_module_board_v01e00]])는 UTO-**NBL**-52 기반 BLE_Module_Board_Ver0.1E00 기준. NBK는 별개 보드 — 회로도·BOM이 wiki에 없음(빈자리). **NBL의 핀맵을 NBK에 그대로 적용하지 말 것**.

## 핀맵 (2026-06-17 코드 매크로 대조 확인)

### LED

| LED | 핀 | 의미 | 극성 | 비고 |
|-----|----|------|------|------|
| LED1 | **P0.09** | System Ready | active-high | NFC 핀 → `CONFIG_NFCT_PINS_AS_GPIOS` 필수 ([[nfc_pins_gpio]]) |
| LED2 | **P0.08** | SPI Comm St | active-high | SPI heartbeat 200ms 점멸 |
| LED3 | **P0.06** | BLE Comm St | active-high | ESB health 점멸 |

> PCA10040 DK LED는 P0.17/18/19(active-low) — NBK와 핀·극성 모두 다름.

### SPI (SPIS1)

| 신호 | 핀 | 비고 |
|------|----|------|
| NSS (CS) | **P0.22** | active LOW |
| MISO | **P0.26** | nRF→STM32 |
| MOSI | **P0.25** | STM32→nRF |
| SCK | **P0.27** | |

코드 매크로(`_shared/oled_tv_protocol.h` 또는 `eta_spi.h`)와 완벽 일치 확인(2026-06-17). 대응 STM32 핀: PB12(NSS)/PB14(MISO)/PB15(MOSI)/PB13(SCK). → [[spi_pin_mapping]]

### UART (격리형, nRF→PC 모니터)

| 신호 | 핀 | 비고 |
|------|----|------|
| TXD | **P0.15** | nRF→PC 방향 |
| RXD | **P0.14** | PC→nRF 방향 |

> DK PCA10040의 VCP(J-Link USB)와 달리, NBK는 **격리형 UART**로 별도 USB-to-TTL 연결 필요. DK 세션에서 nRF UART 모니터가 안 잡혔던 이유: DK는 다른 핀으로 VCP 출력, 이 UART 핀이 별개 커넥터였기 때문.

### RESET

| 신호 | 핀 | 비고 |
|------|----|------|
| RESET (SW1) | **P0.21** | 푸시버튼, `CONFIG_GPIO_AS_PINRESET` 활성 필요 |

> `CONFIG_GPIO_AS_PINRESET`은 UICR 기록 → 전원사이클 후 적용. DK RESET 버튼의 커스텀 보드 거울. comm_st 검증 시 "반대쪽 nRF만 차단" 케이스에 사용. → [[comm_state_monitoring]] "PCA10040 DK 테스트 방법론 함정"

## 칩 식별

| 항목 | 값 | 비고 |
|------|-----|------|
| MCU | nRF52832-xxAA | |
| FICR.DEVICEID[0] | 보드마다 다름 | 이번 02 칩: `0x09741932`. 보드 교체 시 `0x10000060`에서 매번 확인 |

## 미확인 빈자리

- 32MHz HFXO 크리스탈 실장 여부 — ESB 라디오 의존이므로 추후 확인 필요. 실장 없으면 RC 발진 사용(주파수 정확도 저하 가능)
- NBK 회로도·BOM 미인입
- LED1(P0.09) cold-boot 확인 — UICR.NFCPINS bit0=0 적용 후 점등 여부 미확인 (2026-06-18 TODO)

## 관련

- [[nfc_pins_gpio]] — P0.09 GPIO 전용화 절차·함정
- [[spi_pin_mapping]] — SPI 물리 배선 전체 표
- [[st_link_nrf52_flash]] — flash 절차·DEVICEID 확인·UICR 레지스터
- [[schematic_ble_module_board_v01e00]] — UTO-NBL-52 기반 NBL 회로도 (NBK와 다름, 참고만)
- [[comm_state_monitoring]] — DK 테스트 방법론 함정·RESET 홀드 절차
