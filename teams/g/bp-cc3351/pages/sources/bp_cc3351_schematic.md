---
tags: [source, schematic, bp-cc3351, reference]
source: C:\Users\echog\Downloads\spac003 (1)\Tool Folder Design Files\Schematics\BP-CC3351_Sch.PDF
date: 2026-06-02
---

# BP-CC3351 회로도 (소스, ingest 인덱스)

TI BP-CC3351 BoosterPack 회로도. PCB Number MCU121 Rev A (Sheet 1) / Rev B (Sheet 3). 3장 PDF (684.9KB).  
다운로드 경로: TI BP-CC3351 tool folder → Design Files → Schematics (spac003.zip 내 `Tool Folder Design Files/Schematics/BP-CC3351_Sch.PDF`).

원본 PDF 현재 위치: `C:\Users\echog\Downloads\spac003 (1)\Tool Folder Design Files\Schematics\BP-CC3351_Sch.PDF`

---

## 한 줄 요약

AM263P 포팅 시 필요한 **P1/P2 핀맵, Reset 회로, 전원 토폴로지, CC3351 IC 핀 연결**의 원본 소스. 특히 P1.5 LP_RESET(WLAN_EN) + Reset circuit은 S6 블로커(NP 기동 미검증) 직접 참조 대상.

---

## Sheet 인덱스 (raw 경로)

| 파일 | 시트 | 내용 |
|---|---|---|
| [sheet01_cc3351_target](../../raw/bp_cc3351_sch/sheet01_cc3351_target.md) | Sheet 1 (Rev A, 2/6/2024) | CC3351 IC 핀 연결, 클럭(Y1/Y2), RF(diplexer/SMA/chip antenna), SoP MODES |
| sheet02_assembly_notes | Sheet 2 (Rev A, 11/2/2023) | Assembly notes(ZZ1~ZZ3), SH-J 점퍼 위치 메모 — 내용 없음, ingest 생략 |
| [sheet03_launchpad_interface](../../raw/bp_cc3351_sch/sheet03_launchpad_interface.md) | Sheet 3 (Rev B, 11/6/2023) | P1/P2 LaunchPad 인터페이스, 전원(TPS7A8801RTR), Reset 회로(Q1 BSS138), XDS110(J10/J11) |

---

## 파생 페이지

- [[boosterpack_pinmap]] — P1/P2 2×20핀 전체 할당 표 (Sheet 3 + UG Table 2-3/2-4에서 추출, **생성 완료**)

## 주요 발견 (회로도에서만 알 수 있는 사실)

- **Reset 회로**: LP_RESET(P1.5)은 R19(10k)로 VCC_BRD_3V3에 풀업. Q1(BSS138)이 XDS110의 XDS_RESET으로 LP_RESET을 LOW로 당길 수 있음. MCU(AM263P)는 P1.5를 직접 구동 — LOW=reset, HIGH=running.
- **D1 Yellow LED** = nRESET 상태 표시 (UG에서는 D5라고 부름). LP_RESET=HIGH이면 LED on → CC3351 정상 동작.
- **Level shifter 전압 점퍼(J12/J13/J14)**: AM263P 연결 시 3.3V 선택 필요.
- **전원 OR-ing**: LaunchPad P1.21(5V)과 USB J7(5V) Schottky OR-ing → TPS7A8801RTR LDO → 1.8V/3.3V.
