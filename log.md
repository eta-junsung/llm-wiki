# log

시간순 작업 로그. 형식: `## [YYYY-MM-DD] <타입> | <제목>`

---

## [2026-05-22] ingest | TI MCU+ SDK `flash_nor_ospi.c` (Flash_open 시퀀스 + SBL 핸드오프)

- 소스: `https://github.com/TexasInstruments/mcupsdk-core` (branch `next`), commit `05d3aebbc8d6e9ef7fdb69a646c68676146ff5b5`, file `source/board/flash/ospi/flash_nor_ospi.c` (1429 lines)
- raw 사본: `teams/g/lp-am263p/raw/mcupsdk/source/board/flash/ospi/flash_nor_ospi.c`
- 생성 페이지:
  - sources: [[mcupsdk_flash_nor_ospi]] (라인 인덱스 + 후속 ingest 후보)
  - concepts: [[flash_open_sequence]], [[sbl_app_flash_handoff]]
- 트리거 질문: "SBL이 IS25LX256을 8D DDR로 올릴 때 쓴 dummy cycle, 종료 시 컨트롤러 상태" — prebuilt `.lib` 역분석 없이 소스 레벨에서 SBL → 앱 gap 식별 목적
- 핵심 합의:
  - **Dummy cycle 숫자는 이 파일에 없다** — `devCfg->protocolCfg.dummyClksRd/Cmd`에서 가져옴. 실제 값은 IS25LX256 디바이스 디스크립터(별도 파일, SBL board 패키지 혹은 SysConfig output). 후속 ingest 대상.
  - **`skipHwInit` 게이트가 SBL→앱 핸드오프 계약의 본질**: `TRUE`면 chip register write 전부 스킵, 컨트롤러 측 설정은 그대로 실행. 두 `Flash_DevConfig`가 bit-exact 일치해야 read 안 깨짐.
  - **PHY attack vector 자동 write가 destructive**: `skipHwInit`와 무관하게 PHY 경로는 항상 실행. attack vector 없으면 flash 마지막 sector를 erase+write. 양산 시 sector 사용 충돌 주의.
  - **Capture delay sweep으로는 dummy mismatch 보정 못 함** — capture delay는 phase 보정용, cycle count 다르면 데이터 자체가 shift됨.
  - `Flash_quirkSpansionUNHYSADisable` 실체가 line 1374에 있음 — [[is25lx256_vs_spansion_quirks]]의 quirk #1 보강 가능 (이번엔 미반영, 후속 lint 시 처리)
- 후속 ingest 후보 (페이지 미생성):
  - `flash_nor_ospi.h` 구조체 정의 (`FlashCfg_ProtoEnConfig`, `Flash_DevConfig`)
  - IS25LX256용 `Flash_DevConfig` 디스크립터 (실제 dummy/cmd/proto 값)
  - PHY tuning 동작 (`OSPI_phyReadAttackVector`, `OSPI_phyTuneDDR`)

---

## [2026-05-22] query→pages | IS25LX256 dummy cycle 표 & Spansion quirk 차이

- 사용자 작업 컨텍스트: **bp-3351 → AM263P 포팅** (메모리에 `project_lp_am263p.md` 기록)
- 질문 두 개를 raw에서 답하고 concept 페이지로 환원:
  1. **8D-8D-8D dummy cycle vs 주파수** — Table 6.7 (ch06 p.25-27)에서 직접 발췌. 16.67 MHz=3 cycles, 33.33 MHz=4 cycles. 3 variant(WX 200/ECC-OFF, WX 166/ECC-ON, LX 133) 별 차이 정리.
  2. **UNHYSA 비트 부재 확인** — 전 챕터 grep 결과 0건. ISSI는 sector arch가 ordering 옵션 `B`(factory 64KB)로 결정되고 런타임 토글 불가. Spansion CFR3V[UNHYSA] 가정 코드는 silent corruption 위험.
- 생성 페이지:
  - concepts: [[xspi_dummy_cycles]], [[is25lx256_vs_spansion_quirks]]
- 핵심 합의:
  - 데이터시트 표의 "16/33/...” 숫자는 200 MHz / N 그리드 (16=16.67, 33=33.33).
  - DLPRD dummy = Octal DDR dummy + 2 (학습 시 자주 잊는 +2).
  - 포팅 액션은 `is25lx256_vs_spansion_quirks` 끝의 체크리스트로 통합 — 향후 같은 충돌 의심 재발 시 진입점.

---

## [2026-05-22] ingest | IS25LX256 데이터시트 (raw 추출 + 인덱스)

- 소스: `C:\Users\echog\eta\25LX-WX256-128.pdf` (97쪽, ISSI Rev. A14 2026-05-12) — wiki 밖 보관
- raw 경로: `teams/g/lp-am263p/raw/IS25LX256/` — 12개 챕터 마크다운 + `img/` (PNG 52장)
- 도구: `pymupdf4llm` 1.27.2.3 (pip 설치). 챕터별 페이지 범위로 split 추출.
- 생성 페이지:
  - sources: [[is25lx256_datasheet]] (챕터 인덱스 + 추출 메타)
- 핵심 합의:
  - 97쪽 데이터시트를 한 번에 ingest하지 않는다. raw는 챕터 단위로 보관하고, 실제 작업이 트리거하는 챕터만 lazy하게 entities/concepts로 환원.
  - 이미지 추출 비용은 디스크만 차지 (토큰 0). Read tool로 PNG 열 때만 토큰 발생 → 필요한 그림만 lazy 로딩.
  - 테이블은 pymupdf4llm이 GFM 마크다운 테이블로 충분히 잘 보존 (Table 6.x 검증). 깨진 표는 ingest 단계에서 원본 PDF 재추출로 fallback.
- 새 프로젝트 디렉토리 신설: `teams/g/lp-am263p/` (CLAUDE.md 미작성 — 자산이 더 쌓이면 추가)

---

## [2026-05-21] ingest | 회로도 ingest 전략 (공통)

- 소스: 대화 — 회로도 파일을 wiki에 넘기는 방법 논의
- 생성 페이지:
  - concepts(공통): [[schematic_ingest_strategy]]
- 핵심 합의:
  - PDF 비전 처리는 토큰 과다 + 오인식률 문제로 피한다
  - EDA(Electronic Design Automation) 툴 텍스트 export가 1순위: 네트리스트(.net) + BOM(CSV)
  - PDF 텍스트 레이어 추출(pdftotext)이 2순위, 이미지 crop이 최후 수단
  - 파일명 규약: `YYYYMMDD-<프로젝트>-schematic__<블록명>.<ext>`
- 루트 `pages/` 디렉터리 신설: 프로젝트 비종속 공통 지식 위치

---

## [2026-05-21] ingest | OLED TV SPI 프로토콜 매뉴얼 (BLE 시절)

- 소스: 3개 CSV (`260513-oled_tv-protocol-manual__{introduction, from-eta_tx-to_etx_rx, from-eta_rx-to_etx_tx}.CSV`), 원본 CP949 → UTF-8 변환본 `.utf8.csv` 옆에 보관
- raw 경로: `teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__*.CSV`
- 생성 페이지:
  - sources: [[spi_protocol_manual_260513]]
  - entities: [[rx_ble_module]]
  - concepts: [[spi_packet_format]], [[tx_to_rx_packets]], [[rx_to_tx_packets]], [[comm_state_monitoring]]
- 갱신: [[rx_control]]에 SPI 페어 절 추가
- 핵심 합의:
  - 이 문서는 Rx Module ↔ Rx 무선모듈 간 **SPI 11-byte 패킷** 사양. 무선 구간(BLE→ESB)은 모듈 내부 처리이므로 SPI 패킷 골격은 ESB 전환 후에도 유지.
  - 페이지는 방향별로 묶음 (tx_to_rx / rx_to_tx).
  - BLE 시절 자산: `rx_ble_module`과 `sources` 페이지에만 `tags: [historical, ble]` 부여. 프로토콜 사양 페이지는 ESB와도 공유되므로 historical 태그 미부여.
- 원문 이슈 기록:
  - 0x50 Buffer[2] 비트 라벨 중복 (Bit.3 다회) — `Start Bit` 값으로 재정렬
  - 0x52 Power Stack#1·#2 온도 스케일 표기 불일치 (`0.1[℃]` vs `0.01[℃]`) — 예시값 역산상 둘 다 0.1 ℃ 추정, 구현 시 확인 필요

## [2026-05-21] ingest | RX_control PWM 개발 가이드

- 소스: `projects/c/oled_tv_software/docs/RX_control_PWM_가이드.md` (2026-04-14 작성, `01_RX_control` 서브시스템)
- raw 복사본: `teams/c/oled_tv_software/raw/RX_control_PWM_가이드.md`
- 생성 페이지:
  - sources: [[rx_control_pwm_가이드]]
  - entities: [[rx_control]], [[tim8]], [[tim3]]
  - concepts: [[pwm_system]], [[dead_time]], [[trip_zone]], [[uart_command_set]]
- 핵심 합의: TIM3에 BDTR이 없어 시스템 전체가 SW CCR offset 방식 dead time으로 통일됨. `pwm_set_freq()` 후 ARR이 바뀌므로 `pwm_set_deadtime()` 재호출 필요.
