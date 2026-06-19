# bp-cc3351 — 도메인 schema

## 프로젝트 성격

**BP-CC3351**은 TI CC3351 Dual-Band Wi-Fi 6 + BLE BoosterPack 평가 모듈. eta 내부에서는 **AM263P 포팅 작업(`teams/g/lp-am263p/`)의 원본 source 보드**로 사용된다.

현재 상태: **reference-only** — 이 보드 자체에 대한 신규 개발은 없음. wiki 역할은 lp-am263p 포팅 작업이 "원본 보드에서는 어땠는가"를 질문할 때 답을 제공하는 것.

## 파생 페이지 생성 원칙 — lazy ingest

`pages/entities/`, `pages/concepts/` 페이지는 **lp-am263p 포팅 작업이 실제로 해당 정보를 요구할 때만** 생성한다. 자료가 raw/에 있더라도 미리 환원하지 않는다.

현재 후보(미생성):
- entities: `bp_cc3351_board` (보드 전체), `cc3351_ic` (칩)
- concepts: `boosterpack_pinmap` (2×20핀 P1/P2 헤더 할당), `jtag_header` (J10/J11 SWD), `power_rails` (전원 구성), `clocking` (클럭 소스)

## 주요 cross-ref

- [[lp-am263p]] 프로젝트가 주 소비자. 회로도·핀맵·전원 정보를 포팅 시 참조.
- [[is25lx256_datasheet]] — flash는 lp-am263p 프로젝트에 ingest됨 (first-ingest-wins).

## 디렉토리 레이아웃

```
bp-cc3351/
├── CLAUDE.md             # 이 파일
├── raw/
│   └── bp_cc3351_evm_ug/ # EVM User Guide 챕터별 마크다운 추출본
│       └── img/           # PNG 이미지
└── pages/
    ├── entities/          # 보드·IC 개체 (lazy)
    ├── concepts/          # 핀맵·전원·클럭 등 (lazy)
    └── sources/           # 소스 인덱스 페이지
```
