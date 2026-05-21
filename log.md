# log

시간순 작업 로그. 형식: `## [YYYY-MM-DD] <타입> | <제목>`

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
