---
tags: [source, schematic, am263p, launchpad, reference]
source: teams/g/lp-am263p/raw/proc171_schematic/ (TI LP-AM263P 회로도 PROC171A, SPRR503A 설계파일 패키지)
date: 2026-06-10
---

# LP-AM263P 회로도 (소스, 선택적 Tier 2 ingest)

TI **LP-AM263P LaunchPad** 회로도. TI 공개 설계파일 패키지 **SPRR503A**(폴더 `PROC171A`, 보드 실크 Rev A) 기반. [[schematic_ingest_strategy]] **Tier 2**(텍스트 레이어 PDF)로 ingest — 전체가 아니라 **필요 블록만 선택적** 추출.

> Tier 결정 근거: 패키지의 Altium 소스(`.SchDoc`/`.PcbDoc`)는 **바이너리 OLE**라 Altium 라이선스 없이 네트리스트 export(Tier 1) 불가. 동봉 산출물 중 **렌더링 PDF에 텍스트 레이어가 살아있어**(`pdftotext -layout` 추출 양호) Tier 2가 최적 경로. BOM은 `.xls`(OLE) → 필요 시 CSV 변환(Tier 1 BOM, 현재 미적재).

## 보드 리비전 주의

패키지에 **PROC171A**(Rev A)와 **PROC171E2A**(Rev E2) 두 폴더 존재. 이 ingest는 **PROC171A** 기준(사용자 실물 보드 = Rev A 확인, 2026-06-10). E2 리비전은 refdes·핀이 다를 수 있음.

## raw 적재 파일

`raw/proc171_schematic/`:

| 파일 | 내용 |
|------|------|
| `20260610-lp-am263p-schematic__full.pdf` | SCH PDF 원본 전체 27시트 (immutable) |
| `20260610-lp-am263p-schematic__serial_conn_p11.txt` | Sheet 11 `ePWM_eQEP_FSI` — **U54 UART/EPWM 먹스** |
| `20260610-lp-am263p-schematic__p23_io_expander.txt` | Sheet 23 IO_EXPANDER — **U63 TCA6416** (먹스 SEL/EN 구동) |
| `20260610-lp-am263p-schematic__p13.txt`, `__p21.txt` | 보조(다른 SN74 먹스 인스턴스·BP 헤더 핀맵) |

> pdftotext `-layout` 출력은 회로도 2D 좌표가 공백으로 흩어져 나옴 → Grep 타깃 조회용. 핀 1:1 결선은 scrambled라 단정 금물, 시각 확인(PDF) 또는 IPC 네트리스트로 교차.

## 이번 ingest 범위 (scope: UART5 먹스 블록)

목적: 8kw·lp-am263p의 **UART5 직결 기능 점검** 정향. UART5_TXD/RXD가 부스터팩 헤더로 어떻게 나가는지 + 차단 요인 확인.

**핵심 발견** → 파생 entity [[lp_am263p_uart_epwm_mux]]:

- LP-AM263P **온보드에 RS-485 트랜시버 없음** (네트리스트 `485`/`THVD`/`RS485` 0건). 8kw가 쓰는 **THVD1400 U13은 8kw 커스텀 보드** 부품. ([[am263p_iomux_force_io_enable]] 정정 반영.)
- UART5_TXD/RXD는 **U54(SN74CB3Q3257) UART/EPWM 먹스**를 거쳐 BP 헤더로. 먹스 SEL/EN은 **TCA6416(U63, I2C1 @0x20)** 이 구동 — 펌웨어 I2C 설정 전엔 먹스 상태 미정.

## 파생 페이지·백링크

- [[lp_am263p_uart_epwm_mux]] — U54 먹스 + U63 expander 상세 (이 ingest의 산출 entity).
- [[am263p_iomux_force_io_enable]] — SoC 핀먹스/PADCONFIG 층위(보드 먹스와 별개 층).
- [[lp_am263p_ug]] — 보드 UG. BP 헤더 핀맵(§2.20/2.21)으로 먹스 J-핀 정합 교차확인.
- [[schematic_ingest_strategy]] — Tier 정책.

## 향후 ingest 후보 (미실행)

- BOM `.xls`→CSV (부품 정본 목록, Tier 1 BOM).
- BP 헤더 시트(21) 전체 J-핀↔SoC 핀 대응 → 프로젝트 `CLAUDE` "미확인" 물리 대응표 해소.
- 8kw 함의 검증 후 8kw [[status]] 미결 갱신.
