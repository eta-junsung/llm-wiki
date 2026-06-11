---
tags: [concept, build, ses, nrf52, trap]
source: projects/c/oled_tv_software (02_RX_ble 모듈 분리 리팩토링 2026-06-10, eta_ 전환 b92835c 2026-06-11)
date: 2026-06-11
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

## 2. nRF5 SDK 헤더 이름 충돌 → `eta_` 접두사로 근본 해소

nRF5 SDK 17에는 `components/libraries/uart/app_uart.h` 등 `app_*.h`가 다수 존재한다. `Application/Inc`를 include 경로 맨 앞에 두면 **같은 이름의 프로젝트 헤더가 SDK 헤더를 shadow**하여 빌드가 깨진다.

**해소 (`b92835c`, 2026-06-11, 빌드·실보드 검증 완료)**: 로컬 모듈 접두사를 `app_` → **`eta_`**로 전환. SDK가 `eta_*`를 쓰지 않으므로 충돌 클래스 근본 제거. 헤더(`eta_uart.h`)·소스(`eta_uart.c`) 이름 대칭 회복. 네이밍 규칙 전문 → [[nrf52_module_naming]].

경위: 임시 회피책으로 `app_uart_drv.h`(헤더명 `_drv` suffix·소스명 불일치)를 썼다가 `eta_uart.h/c`로 교체함.

## 3. 전처리기 매크로 스코프 변경 주의 (ADD_SPI 사례)

`ADD_SPI` 매크로는 원래 `main.c` 로컬 `#define`이었으나, SPI 코드가 `app_spi.c`로 분리되면서 `.emProject`의 `c_preprocessor_definitions`(프로젝트 전역)로 이동했다.

**의미 변화**: 이제 모든 TU에 `ADD_SPI`가 전파된다. 해당 매크로가 조건부 컴파일에 쓰인다면 의도치 않은 코드 활성화 가능성이 있다. 현재 빌드·동작에 이상 없음(에러 0·경고 0) — 점검 후 확정 예정.

## 4. `.emProject` `<folder>` 는 가상 그룹 — 빌드·디스크 무영향

SES Solution Explorer의 `<folder Name="...">` 는 **표시 전용 가상 그룹**이며 중첩 가능하다. 각 `<file>` 은 `file_name` 속성으로 실제 디스크 경로를 독립 보유한다.

따라서 Explorer 트리를 어떻게 재편하든(평면→중첩, 폴더명 변경 등) **빌드 대상·디스크 경로·include 경로에 영향 없다** — `file_name` 과 `c_user_include_directories` 를 건드리지 않는 한.

Explorer 트리 정리 = `<folder>` 구조만 바꾸는 순수 표시 변경이다.

## 관련

- [[nrf52_module_naming]] — `eta_` 접두사 규칙 (§2 충돌 해소 결정)
- [[app_protocol_module]] — 표준 모듈 패턴(01이 원형, 02 적용)
- [[rx_ble_module]] — 02_RX_ble entity
- [[cubeide_cli_build_trap]] — STM32CubeIDE CLI 빌드 불가 함정 (01 쪽 유사 패턴)
