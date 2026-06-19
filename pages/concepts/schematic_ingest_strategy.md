---
tags: [wiki-meta, schematic, ingest]
source: conversation-2026-05-21
date: 2026-05-21
---

# 회로도 ingest 전략

모든 팀·프로젝트 공통. 회로도(PCB 설계 출력물)를 wiki에 ingest할 때 비전 처리를 피하고 텍스트 기반 소스로 변환하는 전략.

## 핵심 원칙

PDF 이미지를 LLM 비전으로 처리하는 것은 **피한다**.  
이유: 토큰 소모 과다 + 벡터 그래픽 오인식률 높음.  
대신 [[EDA]] 툴의 **텍스트 export**를 `raw/` 소스로 사용한다.

## EDA란

EDA(Electronic Design Automation) — 회로 설계 소프트웨어의 통칭.  
대표 툴: KiCad, Altium Designer, Eagle, OrCAD.  
이 툴들은 회로도·PCB 파일 외에 네트리스트·BOM 등 텍스트 포맷 export 기능을 제공한다.

## Tier별 전략

### Tier 1 — EDA 텍스트 export (권장)

| 툴 | export 경로 | 포맷 |
|---|---|---|
| KiCad | File → Export → Netlist | `.net` (XML) |
| Altium | Reports → Netlist → Protel | `.NET` (텍스트) |
| Altium | Reports → Bill of Materials | `.csv` |
| Eagle | File → Export → Netlist | `.net` |

- 네트리스트: 부품 목록 + 연결 관계(nets) → entity/concept 페이지로 직접 변환
- BOM(CSV): `raw/`에 적재 후 기존 CSV ingest 워크플로와 동일하게 처리

### Tier 2 — PDF 텍스트 레이어 추출

규격서·데이터시트 등 텍스트 레이어가 있는 PDF에만 적용.  
실제 회로도 CAD 벡터는 텍스트 추출 안 됨 → Tier 1로 가야 한다.

```powershell
# poppler 설치 후
pdftotext -layout 문서.pdf 문서.txt
```

### Tier 3 — 이미지 crop (최후 수단)

어쩔 수 없이 이미지만 있을 때. **전체 PDF는 절대 넘기지 않는다.**

1. 관심 블록(전원부, MCU 주변 등)만 캡처
2. 사용자가 블록 목적·이름을 텍스트로 먼저 설명
3. 이미지는 연결 확인 보조용으로만 사용

## raw/ 적재 파일명 규약

```
raw/
├── YYYYMMDD-<프로젝트>-schematic__<블록명>.net    ← 네트리스트
├── YYYYMMDD-<프로젝트>-schematic__bom.csv         ← BOM
└── YYYYMMDD-<프로젝트>-schematic__block_note.md   ← 블록 설명 (선택, 사람 작성)
```

기존 규약(`YYYYMMDD-<프로젝트>-<설명>__<섹션>`) 그대로 따른다.
