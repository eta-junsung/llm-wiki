---
tags: [source, datasheet, flash, xspi, octal]
source: teams/g/lp-am263p/raw/IS25LX256/ (원본 PDF: C:\Users\echog\eta\25LX-WX256-128.pdf, Rev. A14 2026-05-12)
date: 2026-05-22
---

# IS25LX256 / IS25WX256 데이터시트 (소스, ingest 인덱스)

ISSI **256/128Mb Serial Flash Memory** — Octal I/O xSPI 인터페이스, On-CHIP ECC. JEDEC xSPI 호환. SPI 1S-xy-xy(extended) 및 Octal DDR(8D-8D-8D) 프로토콜 지원. 97쪽 PDF를 챕터 단위로 마크다운 추출하여 `raw/IS25LX256/`에 보관.

원본 PDF는 wiki 밖(`C:\Users\echog\eta\25LX-WX256-128.pdf`)에 있으니, **이 소스 페이지 + raw/ 디렉토리**가 진입점.

---

## 한 줄 요약

- 4종 패밀리: IS25LX256/128 (3.0V, 133MHz), IS25WX256/128 (1.8V, SDR 166MHz / DDR 200MHz)
- 패키지: 24-ball BGA (5x5)
- 4-Bank 아키텍처 → Read While Program/Erase 가능
- 128KB sector + 4KB/32KB subsector + 256B page (옵션 64KB sector)
- ECC: 16-byte 경계에서 1-bit correct / 2-bit detect
- 64-byte OTP, 비밀번호 보호, sector 단위 lock, hardware write protect

## 챕터 인덱스 (raw 경로 + 원본 페이지 범위)

| 파일 | 챕터 | 원본 p. | 비고 |
|---|---|---|---|
| [ch00_frontmatter](../../raw/IS25LX256/ch00_frontmatter.md) | FEATURES, GENERAL DESCRIPTION, TOC | 1–5 | 개요·feature list |
| [ch01_pin_configuration](../../raw/IS25LX256/ch01_pin_configuration.md) | PIN CONFIGURATION | 6 | 24-ball BGA 배치도 |
| [ch02_pin_descriptions](../../raw/IS25LX256/ch02_pin_descriptions.md) | PIN DESCRIPTIONS | 7 | C, S#, RESET#, W#, DQ[7:0], DQS, ERR#, PSC, Vpp 정의 |
| [ch03_block_diagram](../../raw/IS25LX256/ch03_block_diagram.md) | BLOCK DIAGRAM | 8 | 내부 블록도 (이미지 위주) |
| [ch04_xspi_signal_protocol](../../raw/IS25LX256/ch04_xspi_signal_protocol.md) | xSPI Signal Protocol Description | 9–10 | Extended SPI vs Octal DDR 시그널 |
| [ch05_system_configuration](../../raw/IS25LX256/ch05_system_configuration.md) | SYSTEM CONFIGURATION (5.1 주소, 5.2 SFDP) | 11–14 | Bank/Block/Sector 주소, SFDP |
| [ch06_registers](../../raw/IS25LX256/ch06_registers.md) | REGISTERS (6.1–6.8) | 15–35 | Status, Flag Status, Configuration(NV/V), Security, Lock, Protection |
| [ch07_device_id](../../raw/IS25LX256/ch07_device_id.md) | DEVICE ID DATA | 36 | Manufacturer/Device ID, JEDEC ID |
| [ch08_device_operation](../../raw/IS25LX256/ch08_device_operation.md) | DEVICE OPERATION (8.1–8.27) | 37–79 | Command set, Read/Program/Erase, Suspend, OTP, XIP, ECC, Reset, RWP/RWE 등 |
| [ch09_electrical_characteristics](../../raw/IS25LX256/ch09_electrical_characteristics.md) | ELECTRICAL CHARACTERISTICS | 80–94 | Abs Max, DC/AC, 타이밍, suspend/resume |
| [ch10_package](../../raw/IS25LX256/ch10_package.md) | PACKAGE TYPE INFORMATION | 95 | 24-ball BGA 6x8mm 도면 |
| [ch11_ordering](../../raw/IS25LX256/ch11_ordering.md) | ORDERING INFORMATION | 96–97 | Part number 디코딩 |

이미지: `raw/IS25LX256/img/` (PNG 52장, 파일명에 원본 페이지 번호 인코딩 — e.g. `...0019-06.png`은 p.19의 6번째 그림).

## 추출 도구·품질

- `pymupdf4llm` 1.27.2.3 (pymupdf + layout-aware extraction)
- 테이블: GFM 마크다운 테이블로 잘 변환됨 (Table 6.1/6.2/6.3 확인). 멀티라인 셀은 `<br>`로 인코딩.
- 이미지: PNG로 별도 추출 후 마크다운에 `![](img/...png)` 참조. 토큰 비용은 0 (실제로 Read tool로 열 때만 비용 발생).
- 텍스트만으로 부족할 때 fallback: 원본 PDF 해당 페이지를 직접 다시 추출하거나, 마크다운에 참조된 PNG를 Read.

## 파생 페이지

작성됨 (lazy ingest):
- concepts: [[xspi_dummy_cycles]] — Octal DDR dummy vs 주파수 표 (Table 6.7 환원)
- concepts: [[is25lx256_vs_spansion_quirks]] — bp-3351 포팅 시 Spansion 분기 제거 체크리스트

후보 (작업 트리거 시 생성):
- entities: [[is25lx256]] (칩 자체), [[am263p_xspi_controller]] (호스트 측, MCU 페리)
- concepts: [[xspi_protocol]], [[octal_ddr_mode]], [[xspi_command_set]], [[xspi_ecc]], [[xspi_xip_mode]], [[xspi_program_erase]], [[xspi_suspend_resume]]

## 주의·관찰

- 패밀리 식별자 4개 (IS25LX256/128, IS25WX256/128) 데이터시트가 하나로 통합되어 있음. 페이지에 적을 때 어느 variant 기준인지 명시할 것.
- LX(3.0V)와 WX(1.8V) 사이 동작 주파수·전기 사양이 다름. ch09 ingest 시 둘 다 표기 필요.
- 일부 옵션 핀은 ordering 옵션에 따라 거동이 바뀜 (Vpp ↔ W#, DNU ↔ PSC). ch11 디코딩 표 같이 봐야 함.
- 원본 PDF는 wiki 밖에 있으므로 이동·삭제되면 raw/ 추출본만 남는다. 표·텍스트는 보존되지만 PDF 자체가 필요할 일 생기면 원본 위치 확인 필요.
