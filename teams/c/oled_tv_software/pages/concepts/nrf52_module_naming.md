---
tags: [concept, naming, nrf52, convention]
source: esb 브랜치 b92835c (2026-06-11, 02_RX_ble eta_ 접두사 전환, 빌드·실보드 검증 완료)
date: 2026-06-11
subsystem: 02_RX_ble, 03_TX_ble
---

# nRF52 로컬 모듈 네이밍 — `eta_` 접두사 규칙

02_RX_ble(nRF52832) 고유 모듈은 **`eta_`** 접두사를 쓴다.

## 규칙

| 층위 | 접두사 | 예시 |
|------|--------|------|
| 로컬 드라이버·응용 모듈 | `eta_` | `eta_gpio`, `eta_clock`, `eta_uart`, `eta_spi`, `eta_esb`, `eta_protocol` |
| SDK 헤더 include | 그대로 | `#include "app_uart.h"` ← SDK 소유, 변경하지 않음 |

신규 모듈도 `eta_`로 만든다.

## 이유 — 충돌 클래스 근본 제거

nRF5 SDK 17에는 `app_uart`, `app_button`, `app_timer`, `app_fifo`, `app_pwm` 등 `app_` 접두사 모듈이 다수 존재한다. 로컬 모듈이 `app_`을 쓰면 SDK 헤더와 이름이 충돌한다.

실제 사례: 리팩토링 초기 로컬 `app_uart.h`가 SDK `components/libraries/uart/app_uart.h`를 shadow하여 빌드가 깨졌다. 임시 회피책으로 `app_uart_drv.h`라는 비대칭 이름을 썼다(헤더명 `_drv` suffix·소스명 `app_uart` 불일치). [[ses_build_conventions]] §2 참조.

`eta_`는 SDK가 사용하지 않는 접두사라 이 충돌 클래스를 근본 제거하고, 헤더(`eta_uart.h`)와 소스(`eta_uart.c`) 이름 대칭을 회복한다.

## 적용 범위

| 서브프로젝트 | 상태 | 비고 |
|---|---|---|
| `02_RX_ble` (nRF52832) | ✓ `b92835c` (2026-06-11, 빌드·실보드 검증) | `app_*` → `eta_*` 전환 완료 |
| `03_TX_ble` (nRF52832) | 후보 | nRF5 SDK 충돌 없음 — 세 칩 네이밍 일관성 차원 추후 검토 |
| `01_RX_control` (STM32) | 해당 없음 | nRF5 SDK 없음, 충돌 없음 |

## 관련

- [[ses_build_conventions]] — SES 빌드 함정. §2 헤더 충돌 원인·`eta_` 전환 전 임시 회피책 기록
- [[app_protocol_module]] — 표준 모듈 패턴 원형(01_RX_control이 원형, 02에 `eta_protocol`로 적용)
- [[rx_ble_module]] — 02_RX_ble entity
