---
tags: [source, user_guide, am263p, launchpad, reference]
source: teams/g/lp-am263p/raw/lp_am263p_ug/ (원본 PDF: 동 디렉토리 ug_lp-am263p.pdf, TI LP-AM263P LaunchPad User Guide)
date: 2026-06-05
---

# LP-AM263P LaunchPad User Guide (소스, 전체 ingest)

TI **LP-AM263P LaunchPad** 개발 보드 사용자 가이드. 60쪽 전체를 `pymupdf4llm`로 단일 마크다운(`raw/lp_am263p_ug/ug_lp-am263p.md`, 텍스트+표+이미지)으로 추출. 이미지 42장은 `raw/lp_am263p_ug/img/`.

이 프로젝트가 **상시 참조**하는 보드 자료(핀맵·부트모드·점퍼·클록·OSPI 배선) → TRM과 달리 통째로 ingest. 진입점은 이 페이지 + 단일 raw 마크다운.

> ⚠️ 이 UG는 **LP-AM263P 보드(온보드 IS25LX256 OSPI 플래시 포함)** 문서다. 얹는 **BP-CC3351 BoosterPack** 자체 자료는 [[bp_cc3351_evm_ug]]·[[bp_cc3351_schematic]]가 단일 소스 — 헷갈리지 말 것.

---

## 한 줄 요약

- AM263Px R5F LaunchPad, USB-C 전원, XDS110 온보드 디버거, 2×BoosterPack 헤더.
- 부트 플래시 = **OSPI IS25LX256**(이 포팅의 S3 블로커 대상) — §2.6.1.
- 보드 단위 핀맵·부트모드 스위치·핀먹스 매핑 수록 → host(AM263P) 측 배선 확인의 1차 소스.

## 섹션 인덱스 (원본 페이지 → 단일 md 내 위치)

raw 파일: [`ug_lp-am263p.md`](../../raw/lp_am263p_ug/ug_lp-am263p.md) (97KB, 헤딩으로 점프).

| 원본 p. | 섹션 | 비고 (이 프로젝트 관련성) |
|---|---|---|
| 6–10 | 2.1.1 Power (입력/LED/Power Tree) | 전원 토폴로지 — R38 전원 배제 교차검증 |
| 11 | 2.1.2 Push Buttons | |
| **12** | **2.1.3 Boot mode Selection** | **SW1 부트모드** — 프로젝트 [[CLAUDE]] 하드웨어 절 SW1 표 원본 |
| 13–14 | 2.1.4 IO Expander | |
| 15 | 2.2 Functional Block Diagram | |
| **16** | **2.3 GPIO Mapping** | host GPIO 핀맵 — WLAN_EN/IRQ 배선 확인 |
| **17–18** | **2.4 Reset** | 리셋 토폴로지 — R38 리셋 게이팅 분석 |
| **19** | **2.5 Clock** | 보드 클록(XTAL) — AM263P 측. CC3351 Y1 40MHz와 구분 |
| **20** | **2.6.1 OSPI** | **부트 플래시 배선** — S3 Flash_open 직결 |
| 21–23 | 2.6.2~4 MMC/eMMC/EEPROM | |
| 30 | 2.10 SPI | LaunchPad SPI 헤더 핀 |
| 33 | 2.11 UART | console/BLE UART 헤더 |
| 34–35 | 2.12 MCAN | |
| 36 | 2.14 JTAG / 2.15 TIVA·Test Automation Header | J11 등 디버그 헤더 — status 프로브 가이드 |
| **44** | **2.20 BoosterPack Headers** | **J1~J4 ↔ SoC 핀** — `CLAUDE`에 "미확인"인 물리 대응표 후보 |
| **45–48** | **2.21 Pinmux Mapping** | 전체 핀먹스 — syscfg pinmux 교차검증 |
| 49 | 3 Hardware Design Files (회로도/BOM) | |
| **50–53** | **5.3 Known Board Changes/Issues** | ⚠️ 아래 함정 절 참조 |

이미지: `raw/lp_am263p_ug/img/` (PNG 42장). 토큰 비용은 Read 시에만 발생.

## ⚠️ 알려진 보드 함정 (§5.3 — flash 디버그 직결)

- **5.3.1 OSPI DQS and LBCLK nets swap** — RevE2→RevA 보드에서 OSPI DQS/LBCLK 배선 swap 이력. **DQS 관련 가설 검토 시 반드시 교차확인** (cf. [[flash_open_facts]] 폐기 가설 중 DQS 관련).
- **5.3.2 XDS110 Debugger Bricking Issue** — 온보드 XDS110 브릭 이슈. SWD/JTAG attach(status 미결 "CC3351 코어 생존") 시도 전 확인.
- **5.3.3 eMMC CMD and CLK nets swap** — (이 프로젝트 비관련, 기록만).

## 추출 도구·품질

- `pymupdf4llm` 1.27.2.3 — 텍스트+표 GFM 변환, 이미지 PNG 별도 추출.
- 60쪽 단일 파일이라 Grep/헤딩 점프로 탐색. 표가 깨진 곳은 원본 PDF 해당 페이지 재추출.

## 파생 페이지·백링크

- 보드 핀맵 상세: [[boosterpack_pinmap]] (BP-CC3351 P1/P2 ↔ AM263P syscfg), 프로젝트 [[CLAUDE]] "하드웨어" 절.
- 부트 플래시: [[is25lx256_datasheet]], [[flash_open_sequence]].
- 검증 프로브: [[status]] 프로브 가이드, [[instruments]].
- TRM(레지스터·내부 동작)은 [[am263p_trm]].

## 주의

- UG는 **보드 레벨**(배선·핀·점퍼), TRM은 **실리콘 레벨**(레지스터·동작). 핀이 어디 나오나 = UG, 그 핀의 IP가 어떻게 동작하나 = TRM.
- BoosterPack 헤더 ↔ SoC 핀 물리 대응표가 프로젝트 `CLAUDE`에 "미확인"으로 남아 있음 → §2.20/2.21이 그 해소 후보. 확정 시 [[boosterpack_pinmap]]에 환원.
