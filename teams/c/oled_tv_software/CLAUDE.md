# oled_tv_software — 도메인 schema

---

## 프로젝트 소개

OLED TV용 전력 변환 제어 펌웨어. 네 서브프로젝트로 구성된다.

| 서브프로젝트 | MCU | 역할 |
|---|---|---|
| `01_RX_control` | STM32F103RCT6 | PWM 생성·제어, UART 명령 수신, SPI Master(→02) |
| `02_RX_esb` | nRF52832 | ESB PRX, SPI Slave(←01) |
| `03_TX_esb` | nRF52832 | ESB PTX, SPI Slave(←04) |
| `04_TX_control` | STM32F103RCTx | TX측 SPI Master(→03), USART2 모니터, _shared 사용 |

빌드 환경:
- `01_RX_control`, `04_TX_control`: STM32CubeIDE (Ctrl+B 직접 빌드 — CLI 불가 [[cubeide_cli_build_trap]])
- `02_RX_esb`, `03_TX_esb`: Segger Embedded Studio (SES)

공통 자산:
- `_shared/oled_tv_protocol.h` — 공통 프로토콜 정의
- `_external/nRF5_SDK_17` — nRF SDK

---

## 통신 스택

**현재 기준은 ESB.** 코드와 wiki 내용은 ESB 기준으로 작성한다.

BLE 자료는 historical. ingest 시 frontmatter에 `tags: [historical, ble]` 부여.

---

## 도메인 entity 후보 (참고용)

- 보드/MCU: `rx_control`, `rx_esb`, `tx_esb`, `STM32F103RCT6`, `nRF`
- 주요 페리: `TIM8`, `TIM3`, UART, SPI

## 도메인 concept 후보 (참고용)

- PWM 시스템, Dead time, Trip Zone
- UART command set, SPI 통신 규약, ESB 프로토콜

---

## Ingest 도메인 판단

- 어떤 서브프로젝트(01/02/03/04)와 묶이는지 frontmatter `subsystem` 필드 또는 태그로 표기.
- BLE 이전 자료 ingest는 명시적 결정 전까지 보류.

---

## 전략 / 검증 자산

- 전략(목표까지 마일스톤 호 M0~M6) [[roadmap]] ↔ 전술(현재 위치) [[status]]. 컨벤션 전문은 루트 `CLAUDE.md` "로드맵 컨벤션" 절. 작업 단위 호는 `roadmaps/<task>.md`.
- 검증 핀맵 [[gpio_verification_pinmap]] — "기능 → 프로브 핀 → 기대값". 계측 장비는 회사 공통 [[instruments]] (Keysight MSOX3104T).
- status/roadmap 갱신은 루트 `CLAUDE.md` 파이프라인 절 준수.
