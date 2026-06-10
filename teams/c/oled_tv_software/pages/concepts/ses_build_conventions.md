---
tags: [concept, build, ses, nrf52, trap]
source: projects/c/oled_tv_software (02_RX_ble 모듈 분리 리팩토링, 2026-06-10)
date: 2026-06-10
subsystem: 02_RX_ble, 03_TX_ble
---

# SES 빌드 환경 컨벤션 & 함정 (nRF52832)

02_RX_ble 모듈 분리 리팩토링(2026-06-10) 과정에서 발견·확인된 SEGGER Embedded Studio(SES) + nRF5 SDK 17 빌드 환경 고유 함정. CLI 빌드는 `emBuild` 사용.

## 1. `.emProject` 파일 목록 하드코딩 (와일드카드 없음)

SES `.emProject`는 소스 파일과 include 경로가 **모두 명시적으로 하드코딩**된다 — 디렉토리 와일드카드 없음.

모듈 추가/이동 시 **두 곳을 반드시 갱신**:
1. `<file file_name="..."/>` 태그 — 소스 파일 컴파일 대상 등록
2. `c_user_include_directories="..."` 속성 — include 경로 추가

새 `.c`를 `Application/Src/`에 넣어도 자동으로 빌드 대상에 포함되지 않는다.

## 2. nRF5 SDK 헤더 이름 충돌 (app_uart.h shadow)

nRF5 SDK 17에는 `components/libraries/uart/app_uart.h`가 이미 존재한다. `Application/Inc`를 include 경로 맨 앞에 두면 **같은 이름의 프로젝트 헤더가 SDK 헤더를 shadow**하여 빌드가 깨진다.

현 회피책: uart 드라이버 헤더를 `app_uart_drv.h`로 명명 (02_RX_ble 리팩토링 기준 임시 결정 — 미결).

| 옵션 | 비고 |
|------|------|
| `_drv` suffix 유지 | 즉시 동작. `app_uart` 모듈명과 헤더명 불일치 |
| 모듈명을 `app_console` 등으로 변경 | 의미 명확, 파일명 일괄 변경 비용 |
| include 순서 조정 (SDK 우선) | 다른 프로젝트 헤더 접근 방식 변경 필요 |

> nRF5 SDK 내 `app_*.h` 전체 목록과의 충돌 여부 사전 점검 권장.

## 3. 전처리기 매크로 스코프 변경 주의 (ADD_SPI 사례)

`ADD_SPI` 매크로는 원래 `main.c` 로컬 `#define`이었으나, SPI 코드가 `app_spi.c`로 분리되면서 `.emProject`의 `c_preprocessor_definitions`(프로젝트 전역)로 이동했다.

**의미 변화**: 이제 모든 TU에 `ADD_SPI`가 전파된다. 해당 매크로가 조건부 컴파일에 쓰인다면 의도치 않은 코드 활성화 가능성이 있다. 현재 빌드·동작에 이상 없음(에러 0·경고 0) — 점검 후 확정 예정.

## 관련

- [[app_protocol_module]] — 표준 모듈 패턴(01이 원형, 02 적용)
- [[rx_ble_module]] — 02_RX_ble entity
- [[cubeide_cli_build_trap]] — STM32CubeIDE CLI 빌드 불가 함정 (01 쪽 유사 패턴)
