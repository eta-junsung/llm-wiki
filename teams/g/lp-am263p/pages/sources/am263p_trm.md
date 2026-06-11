---
tags: [source, trm, am263p, reference]
source: teams/g/lp-am263p/raw/am263p_trm/ (원본 PDF: 동 디렉토리 trm_am263p.pdf, 1725쪽 — .gitignore, 디스크 only)
date: 2026-06-05
---

# AM263P Technical Reference Manual (소스, 전체 기계추출 + Grep 탐색)

TI **AM263Px Technical Reference Manual** — 실리콘 레벨 레지스터·IP 동작 레퍼런스. 1725쪽을 `pymupdf4llm`로 **챕터 단위 마크다운**(텍스트+표, 이미지 제외)으로 추출해 `raw/am263p_trm/chNN_*.md`에 보관.

> **이 페이지는 RAG MCP를 대체한다.** 이전엔 `ti-am263p` 벡터검색 MCP(ChromaDB)로 TRM을 질의했으나, 800단어 청킹이 레지스터 표를 절단하고 임베딩이 기술 용어에 약해 폐기(2026-06-05). 대신 **Grep + 이 TOC 맵**이 발견을, **concept 환원**이 이해를 담당한다. 근거·전환 기록은 [[log]] 2026-06-05.

---

## 발견(검색)은 Grep으로

용어를 알면 Grep이 의미검색보다 정확하다(`MCSPI_CHCONF`·`HSDIV`·`IN_INTR20` 같은 식별자는 정확매칭이 우월하고 표가 안 깨짐). 단 **용어는 AM263P TRM 표기를 써야 한다** — 예: 클록은 `HFXT`(CC3351 표기) 아닌 `HSDIV`/`HFOSC`, 플래시 ID는 `RDID`(칩측) 아닌 OSPI 컨트롤러 용어:

```
Grep pattern="MCSPI_CHCONF.*FORCE"  path=teams/g/lp-am263p/raw/am263p_trm/  output_mode=content
Grep pattern="FORCE|EPOL|SPIENSLV"  path=.../raw/am263p_trm/ch13_1_general_connectivity.md
```

용어를 모르면 **아래 TOC 맵**으로 챕터를 좁힌 뒤 해당 `chNN_*.md`를 Read/Grep. 이 맵 + 챕터 헤딩이 옛 벡터검색의 "어디 있나"를 대체한다.

## 챕터 인덱스 (raw 파일 → 원본 페이지 → 핵심 IP/용어)

level-1 챕터 기준. 거대 챕터 **ch7(Processors)·ch13(Peripherals)** 만 level-2로 세분.

| 파일 | 원본 p. | 핵심 내용 / 용어 |
|---|---|---|
| [ch00_read_this_first](../../raw/am263p_trm/ch00_read_this_first.md) | 9–11 | 표기 규약·약어 |
| [ch01_introduction](../../raw/am263p_trm/ch01_introduction.md) | 12–26 | SoC 개요, 서브시스템 일람(R5FSS/PRU-ICSS/EDMA/GPIO/SPI/OSPI/MCAN) |
| [ch02_memory_map](../../raw/am263p_trm/ch02_memory_map.md) | 27–39 | 메모리 맵, R5FSS/PRU-ICSS 맵, **페리페럴 base 주소** |
| [ch03_system_interconnect](../../raw/am263p_trm/ch03_system_interconnect.md) | 40–75 | 인터커넥트, 버스 |
| [ch04_module_integration](../../raw/am263p_trm/ch04_module_integration.md) | 76–177 | **모듈 integration** — GPIO(4.12)/SPI(4.14)/UART(4.15)/**OSPI(4.18)**/MCAN(4.19)/XBAR. 핀먹스·클록·인터럽트 결선 |
| [ch05_initialization](../../raw/am263p_trm/ch05_initialization.md) | 178–223 | 부트, **OSPI Boot(5.4.1)**/UART Boot, **PLL Configuration(5.6)** |
| [ch06_device_configuration](../../raw/am263p_trm/ch06_device_configuration.md) | 224–315 | CTRLMMR·IOMUX·TOPRCM/MSS_RCM, **Clocking(6.4)**·Clock Gating·Clocking Registers |
| [ch07_1_r5fss](../../raw/am263p_trm/ch07_1_r5fss.md) | 317–354 | Arm Cortex-R5F 서브시스템 |
| [ch07_2_tmu](../../raw/am263p_trm/ch07_2_tmu.md) | 355–364 | Trigonometric Math Unit |
| [ch07_3_pru_icss](../../raw/am263p_trm/ch07_3_pru_icss.md) | 365–505 | **PRU-ICSS** — PRU 코어·INTC·**WLAN_IRQ가 매핑된 PR0_PRU0_GPIO**·UART/ECAP/MII/IEP |
| [ch07_4_hsm](../../raw/am263p_trm/ch07_4_hsm.md) | 506–508 | Hardware Security Module |
| [ch07_5_controlss](../../raw/am263p_trm/ch07_5_controlss.md) | 509–932 | **CONTROLSS** (ADC/EPWM/CMPSS 등) — 거대. 필요 시 level-3 재추출 |
| [ch07_6_optiflash](../../raw/am263p_trm/ch07_6_optiflash.md) | 933–936 | OptiFlash 개요 |
| [ch08_ipc](../../raw/am263p_trm/ch08_ipc.md) | 937–949 | IPC, Spinlock |
| [ch09_memory_controllers](../../raw/am263p_trm/ch09_memory_controllers.md) | 950–951 | 메모리 컨트롤러 |
| [ch10_interrupts](../../raw/am263p_trm/ch10_interrupts.md) | 952–1029 | **VIM**·Interrupt Routers·**Interrupt Sources/Map** (R5FSS0_CORE0) |
| [ch11_data_movement_edma](../../raw/am263p_trm/ch11_data_movement_edma.md) | 1030–1096 | **EDMA** (MCSPI/OSPI DMA 전송) |
| [ch12_time_sync](../../raw/am263p_trm/ch12_time_sync.md) | 1097–1109 | Time Sync |
| [ch13_1_general_connectivity](../../raw/am263p_trm/ch13_1_general_connectivity.md) | 1111–1263 | **GPIO(13.1.1 p1112)·I2C·★MCSPI(13.1.3 p1146–1196)·UART(13.1.4)** |
| [ch13_2_highspeed_serial](../../raw/am263p_trm/ch13_2_highspeed_serial.md) | 1264–1374 | CPSW Gigabit Ethernet |
| [ch13_3_memory_interfaces](../../raw/am263p_trm/ch13_3_memory_interfaces.md) | 1375–1485 | MMC, **OptiFlash Submodules(13.3.2 p1415) — OSPI/FOTA/PHY** |
| [ch13_4_industrial_control](../../raw/am263p_trm/ch13_4_industrial_control.md) | 1486–1595 | MCAN, LIN |
| [ch13_5_timer_modules](../../raw/am263p_trm/ch13_5_timer_modules.md) | 1596–1621 | RTI/WWDT |
| [ch13_6_diagnostics](../../raw/am263p_trm/ch13_6_diagnostics.md) | 1622–1693 | DCC/ECC/ESM/MCRC/STC/PBIST |
| [ch14_onchip_debug](../../raw/am263p_trm/ch14_onchip_debug.md) | 1694–1718 | On-Chip Debug, Arm Debug Links |
| [ch15_revision_history](../../raw/am263p_trm/ch15_revision_history.md) | 1719–1725 | 개정 이력 |

## Ingested 섹션 (concept 환원됨)

작업 트리거 시 lazy ingest. 이해된 지식은 아래 concept이 단일 소스, 위 raw는 출처:

- [[am263p_mcspi_controller]] — MCSPI(13.1.3) 환원. S6 `SPI not responsive` 디버그용 (CS 프레이밍·EDMA·클록).
- [[am263p_epwm_sync_topology]] — EPWM Time-Base Counter Synchronization(§7.5.6.4.3.3, p.651–654) 환원: per-module fan-out MUX·hop당 고정 지연 모델·Figure 7-181/7-182 직독. 8kw 모듈간 스큐 근본 + fan-out 0-스큐 토폴로지. **검증(2026-06-11)**: ch07_5_controlss.md :5683–5953은 PDF를 충실 재현, 본문 누락 없음(끊긴 cross-ref ":5801 Refer to for…"는 PDF p.652의 TI 원본 버그). device-specific sync-order 표는 TRM에 부재 — Table 7-153 참조는 Table 7-154 선택행렬을 가리킴.

## Candidate 섹션 (현재 블로커 기반, 미ingest)

[[status]] 미결 사항 → 우선 환원 후보:

- **S6 SPI link-up**: ch11 EDMA(MCSPI 전송 경로), ch10 VIM/Interrupt Map(WLAN_IRQ), ch07_3 PRU-ICSS GPIO(WLAN_IRQ=PR0_PRU0_GPIO10·WLAN_EN=GPIO12).
- **부트/클록**: ch05 §5.4.1 OSPI Boot·§5.6 PLL, ch06 §6.4 Clocking — SBL 핸드오프·클록 설정.
- **OSPI 컨트롤러(host측)**: ch13_3 §13.3.2 OptiFlash/OSPI, ch04 §4.18 OSPI Integration — [[flash_open_sequence]] 보강.

## 추출 도구·품질·이미지

- `pymupdf4llm` 1.27.2.3 — 텍스트+표 GFM. **이미지는 제외**(1725쪽 일괄 추출 = repo 비대화).
- **이미지가 필요하면 demand 재추출**: 해당 페이지 범위만 `pymupdf4llm.to_markdown(PDF, pages=[...], write_images=True, image_path=...)`. 추출 스크립트 패턴은 IS25LX256(`raw/IS25LX256/img/`) 참고.
- 표 깨짐·텍스트 부족 시 fallback: 원본 PDF(`raw/am263p_trm/trm_am263p.pdf`, gitignore라 로컬 only) 해당 페이지 재추출.

## 백링크

- 보드 레벨(핀·배선·점퍼): [[lp_am263p_ug]]. **핀이 어디 나오나=UG, 그 IP가 어떻게 동작하나=TRM**.
- 부트 플래시 칩: [[is25lx256_datasheet]]. 드라이버: [[mcupsdk_flash_nor_ospi]], [[flash_open_sequence]].
- 진단: [[flash_open_facts]], [[flash_open_diagnostic_log]], [[status]].
