---
tags: [source, user_guide, evm, bp-cc3351, reference]
source: teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/ (원본 PDF: C:\Users\echog\eta\evm-user-guide-bp_cc3351.pdf)
date: 2026-05-26
---

# BP-CC3351 EVM User Guide (소스, ingest 인덱스)

TI **SimpleLink CC3351 Dual-Band Wi-Fi 6 + Bluetooth Low Energy BoosterPack** 평가 모듈 사용 가이드. SWAU132A, April 2024 – Revised August 2025. 23쪽 PDF를 챕터 단위로 마크다운 추출하여 `raw/bp_cc3351_evm_ug/`에 보관.

원본 PDF는 wiki 밖(`C:\Users\echog\eta\evm-user-guide-bp_cc3351.pdf`)에 있으니, **이 소스 페이지 + raw/ 디렉토리**가 진입점.

---

## 한 줄 요약

CC3351 Wi-Fi 6 + BLE 컴패니언 IC를 탑재한 2×20핀 BoosterPack 모듈. LaunchPad/MPU 시스템에 꽂아 사용. AM263P 포팅 시 **P1/P2 핀맵 (SPI/SDIO/UART/IRQ/RESET)** 과 **JTAG 헤더 (J10 ARM 10핀, J11 20핀 LP-XDS110ET)** 가 핵심 참조 대상.

## 챕터 인덱스 (raw 경로 + 원본 페이지 범위)

| 파일 | 챕터 | 원본 p. | 비고 |
|---|---|---|---|
| [ch00_frontmatter](../../raw/bp_cc3351_evm_ug/ch00_frontmatter.md) | Cover + Description + Features | 1 | 보드 소개, 주요 feature 목록 |
| [ch01_overview](../../raw/bp_cc3351_evm_ug/ch01_overview.md) | Ch.1 EVM Overview | 2–3 | 소개, Kit 내용물, 규격, 디바이스 정보 |
| [ch02_hardware](../../raw/bp_cc3351_evm_ug/ch02_hardware.md) | Ch.2 Hardware | 4–11 | **핵심**: 보드 overview, LED/점퍼, P1/P2 BoosterPack 핀맵, JTAG 헤더(J10/J11), 전원, 클럭, SMA 안테나 |
| [ch03_implementation](../../raw/bp_cc3351_evm_ug/ch03_implementation.md) | Ch.3 Implementation Results | 12–15 | MCU+RTOS, Linux/BeagleBone, 독립 RF 테스트 |
| [ch04_design_files](../../raw/bp_cc3351_evm_ug/ch04_design_files.md) | Ch.4 Hardware Design Files + Ch.5/6 | 16–17 | 회로도·PCB·BOM 다운로드 링크, 지원 리소스, 개정 이력 |
| [ch05_std_terms](../../raw/bp_cc3351_evm_ug/ch05_std_terms.md) | STANDARD TERMS FOR EVALUATION MODULES | 18–23 | TI 법적 보일러플레이트 |

이미지: `raw/bp_cc3351_evm_ug/img/` (PNG 26장, 파일명에 원본 페이지 번호 인코딩 — e.g. `...0006-04.png`은 p.6의 4번째 그림).

## 추출 도구·품질

- `pymupdf4llm` 1.27.2.3 (pymupdf + layout-aware extraction) — [[is25lx256_datasheet]] 추출과 동일 환경
- 테이블: GFM 마크다운 테이블로 변환됨 (P1/P2 핀맵 Table 2-3/2-4, JTAG Table 2-5/2-6 확인).
- 이미지: PNG로 별도 추출 후 마크다운에 `![](img/...png)` 참조. 보드 사진/회로 블록도 포함.
- 그림 내 텍스트는 `**----- Start of picture text -----**` 블록으로 함께 추출됨.

## 파생 페이지 후보 (lazy ingest — lp-am263p 포팅 작업이 trigger할 때 생성)

- entities: `[[bp_cc3351_board]]` (보드 전체 개체), `[[cc3351_ic]]` (CC3351 칩)
- concepts: `[[boosterpack_pinmap]]` — P1/P2 2×20핀 전체 할당 표 (SPI CS/PICO/POCI/CLK, SDIO, UART, IRQ_WL, IRQ_BLE, COEX, RESET, 전원 핀)
- concepts: `[[jtag_header_bp_cc3351]]` — J10 ARM 10핀, J11 20핀 LP-XDS110ET 헤더 매핑 + SWD/UART/RESET 핀
- concepts: `[[power_rails_bp_cc3351]]` — 3.3V / 1.8V 이중 전원, J6/J8/J15/J16 점퍼, USB fallback (J7), 전류 측정법
- concepts: `[[clocking_bp_cc3351]]` — 40MHz XTAL (Y1) + 32.768kHz OSC (Y2), 외부 slow clock 입력(P2.19) rework

## 주의·관찰

- **P1 핀 번호 불연속**: P1.1–P1.10 다음이 P1.21. 2×20핀 커넥터 표준상 P1.11–P1.20은 P2 헤더의 일부. UG 표에 P1.11–P1.20 항목 없음 — 실제 핀 배치도(Figure 2-3)의 그림 텍스트로 보완 필요.
- **Level shifter 전압**: J12/J13/J14 점퍼로 호스트 전압(3.3V↔1.8V) 선택. AM263P 연결 시 호스트 GPIO 전압 레벨 확인 필요.
- **SMA 안테나 rework**: 기본은 칩 안테나. SMA/U.FL 사용 시 3.9pF 캐패시터 이동 필요. 단일 2.4GHz 전용 사용 시 diplexer 바이패스 + 50Ω 종단.
- 원본 PDF는 wiki 밖에 있으므로 이동·삭제되면 raw/ 추출본만 남는다.
