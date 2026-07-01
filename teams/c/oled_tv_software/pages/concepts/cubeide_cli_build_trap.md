---
tags: [concept, build, toolchain, cubeide, gotcha]
source: projects/c/oled_tv_software (esb 35b94d0 작업 중 실측) 2026-06-10
date: 2026-06-10
subsystem: 01_RX_control
---

# CubeIDE CLI 빌드 함정 — IDE에서 Ctrl+B로 빌드

**(사실)** 01_RX_control(STM32CubeIDE 프로젝트)은 **CLI 헤드리스 빌드가 안 된다**. `stm32cubeidec.exe`가 **GUI 서브시스템 실행파일**이라, 콘솔에서 호출하면 빌드 로그를 stdout으로 내보내지 않고 **즉시 종료**한다(headless `-build` 인자를 줘도 콘솔 출력 없이 빠짐). → 자동화/터미널 빌드로 결과를 확인할 수 없다.

## 해야 할 것

- **STM32CubeIDE를 띄워 `Ctrl+B`(Build All)로 직접 빌드**하고 IDE Console에서 결과를 본다.
- **CubeMX 재생성 금지** 규칙 유지 — 수동 편집한 소스/설정이 `.ioc` 재생성으로 덮어쓰이지 않도록.

## CubeMX 재생성 금지 — 구체 근거 (04_tx_control 사례)

04_tx_control의 `TX_control.ioc`가 이 함정의 실례다:

- **`.ioc` 메타**: ADC1 6채널·CAN·DAC·TIM5/8 선언이 잔재
- **실 `main.c`·`hal_conf_ex.h`**: ADC/CAN/DAC/PWM 관련 init·페리 전부 수동 제거, SPI2+USART2만 잔존

이 상태에서 CubeMX 재생성을 실행하면 **`.ioc` 메타 기준으로 `main.c`·`stm32f1xx_hal_conf.h`를 덮어쓴다** — 수동으로 정리한 페리 제거·링커 스크립트 수정이 모두 손상된다.

➡ `.ioc`는 실코드보다 낡아도 **레퍼런스로만** 두는 것이 올바른 운용. 실코드가 진실이다.

## 함의

- 코드 작업 세션이 "빌드 통과"를 확인하려면 IDE 빌드가 필요하다 — CLI 빌드 출력으로 검증했다고 보고하면 안 된다.
- 02/03(nRF, Segger Embedded Studio)과 01(CubeIDE)은 빌드 경로가 다르다 — 01은 이 함정 적용.

## 관련

- [[rx_control]] — 01_RX_control 보드 (빌드: CMake+VSCode / STM32CubeIDE)
- [[cubeide_newlib_nano_float]] — 또 다른 CubeIDE 함정(float printf/scanf nano 플래그)
- [[app_protocol_module]] — 빌드+실보드 동작확인 절
- [[st_link_nrf52_flash]] — 플래싱 절차(빌드와 별개 층위)
