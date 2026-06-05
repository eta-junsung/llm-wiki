# log

시간순 작업 로그. 형식: `## [YYYY-MM-DD] <타입> | <제목>`

---

## [2026-06-05] ingest | oled_tv_software — 플래싱 듀얼 프로브 셋업 (드라이버 스왑 종료)

- **사실 확정 (CLI 실측)**: MCU별 전용 프로브 + 네이티브 도구로 분담. ① `01_RX_control`(STM32F103) → **ST-Link V2 네이티브**(STM32_Programmer_CLI v2.22, FW V2J47S7, Device ID 0x414, connect+read만 실측 — write 미측정). ② `03_TX_ble`(nRF52832 회사보드) → **J-OB v2 = J-Link OB-nRF5340-NordicSemi** S/N 1050329071(정품), program+verify 통과(Bank0@0x0 53248B, exit 0). ③ `02_RX_ble` → DK 온보드 J-Link. 드라이버 분리 → 동시 연결·충돌 없음.
- **함정**: J-Link급 프로브 둘(J-OB v2 + SAM-ICE S/N 24012600) 공존 → `-SelectEmuBySN 1050329071` 고정 필수. ST-Link은 S/N이 `@`로 보고(cosmetic).
- **갱신**: [[st_link_nrf52_flash]] 전면 재작성(정본 — 듀얼 프로브 절차·실측·함정, **pyOCD+Zadig 폴백 강등**, ST-Link WinUSB→네이티브 원복 절차). [[instruments]] "프로그래밍/디버그 프로브" 절 신설(프로브 3종 정체·S/N·드라이버). [[rx_ble_module]] CON1 플래싱 비고 갱신. index 2건.
- **교정**: 회사보드 CON2 UART = **TX P0.15 / RX P0.14**(`custom_board.h:16-17`), NRF_LOG는 RTT(SWD) 전용·UART 미출력. (schematic 소스는 2026-06-04에 이미 정정됨 — 잔존 stale은 st_link 페이지 "미확정" 항목뿐이었고 재작성으로 해소.)
- **빈자리(미검증)**: SES 번들 JLinkARM DLL의 SN 선택 동작, ST-Link 실플래시(write), 플래시 펌웨어 런타임 거동(ESB/SPI/LED), SAM-ICE 연결 대상.

---

## [2026-06-05] lint | lp-am263p — SW1 부트모드 표 DevBoot 값 정정

- **오류**: `teams/g/lp-am263p/CLAUDE.md` SW1 표가 DevBoot를 `1,1,0,0`으로 기재 → 실제로는 OSPI (8S) Octal Read 값의 오기.
- **정정**: DevBoot = `0,1,0,0`(SW1.3만 ON). 근거 LP-AM263P UG SPRUJ85B Table 2-5 ([[raw/lp_am263p_ug/ug_lp-am263p.md]] :469), DevBoot 정의 Table 2-6 :494.
- **부가 수정**: 기존 헤더 `SW1 (1,2,3,4)` 라벨이 실제 기입값(UG의 SW1.4-우선 순서)과 불일치 → 헤더를 UG 순서 **SW1.4/3/2/1**로 명시. 전체 6개 모드 값을 Table 2-5와 교차확인해 표 정합성 확보. ON=논리0(:453) 주석 추가.

---

## [2026-06-05] status | oled_tv_software — 회사 커스텀보드 플래싱·LED 점멸 확인 반영

- **사실 확정**: 회사 커스텀보드(BLE_Module_Board_Ver0.1E00, nRF52832) 입고 + `03_TX_ble` ST-LINK V2 + pyOCD 플래싱 성공 + LED 점멸 육안 확인(LED1 상시점등·LED2/LED3 200ms 토글, active-high). 절차·셋업 함정은 기존 [[st_link_nrf52_flash]]에 정리됨(2026-06-04).
- **status.md 갱신**: stale했던 "다음 시작점"(완료된 ST-LINK 플래싱 지목)을 **LED2/LED3 ↔ 실제 comm-status 비트 연계**로 교체. 하드웨어 입수 표에 플래싱 열·LED 확인 추가. frontmatter date → 2026-06-05.
- **예정**: 플래싱 이슈·해결 추가 공유 시 [[st_link_nrf52_flash]] 트러블슈팅에 ingest.

---

## [2026-06-05] ingest | AM263P TRM/UG wiki 통합 + RAG MCP 폐기

- **결정**: AM263P 자료를 위한 별도 RAG MCP 서버(`C:\firmware-rag\`, ChromaDB 벡터검색 + 800단어 청크 + all-MiniLM-L6-v2)를 폐기하고 wiki 단독으로 전환. 근거: ① wiki 철학 = "원본 텍스트가 아닌 이해된 지식" ② 800단어 청킹이 레지스터 표를 절단(TRM 질의의 핵심 손상) ③ "wiki 단독 ≠ LLM이 1725쪽 정독" — 기계추출(토큰 0) + Grep 발견 + demand 환원 구조.
- **기계추출**: `pymupdf4llm` 1.27.2.3로 TRM 1725쪽을 `get_toc()` 기반 26개 챕터 마크다운(텍스트+표, 이미지 제외)으로 → `raw/am263p_trm/chNN_*.md`. ch7·ch13만 level-2 세분. UG 60쪽은 이미지 포함 전체 → `raw/lp_am263p_ug/`(md+img 42장).
- **source 페이지**: [[am263p_trm]](TOC 맵 + "발견은 Grep" 가이드 + ingested/candidate 섹션 인덱스), [[lp_am263p_ug]](핀맵·부트모드·핀먹스·OSPI 배선 + §5.3 보드 함정 — DQS/LBCLK swap·XDS110 bricking).
- **demand-ingest 예시**: [[am263p_mcspi_controller]] — S6 `SPI not responsive` 직결 MCSPI(13.1.3) 환원.
- **폐기 처리**: `~/.claude.json`의 `ti-am263p` mcpServers 등록 제거(재시작 시 도구 사라짐, 다른 CCS 서버 보존). 22MB TRM PDF는 `.gitignore`(디스크 only). `C:\firmware-rag\` rm_db/스크립트 삭제는 사용자 확인 대기.

---

## [2026-06-05] status | 8kw-ev-wpt-tx — CCS 프로젝트 스캐폴드 완료 반영

- A0 전제 완료: hello_world 기반 CCS 프로젝트 생성·Release 빌드 통과·커밋됨 → 구현 현황 ✓ 갱신.
- 다음 시작점 업데이트: A0 착수 전 SysConfig MCP 버전 정합 확인 절차 추가.
- `직전 완료` 섹션 신설 — CCS workspace 참조 import 작업환경 메모 포함.

---

## [2026-06-04] ingest | 8kw-ev-wpt-tx 프로젝트 신설 + adc 작업 호 개설

- eta 보드 J3 커넥터 6채널 ADC 핀맵(사용자 제공) → [[adc_pinmap]] 엔티티 생성.
- `adc` 작업 로드맵(A0~A4) 신설: SysConfig 설정 → 단채널 검증 → 전채널 읽기 → 신호별 스케일링 → 실보드 교차검증.
- A3(스케일링) 블로커: Temp 모듈 특성·전류 센서 감도·분압비 미입수 — 추가 정보 대기.
- lp-am263p에 잘못 붙었던 eta-adc 항목 모두 제거 후 이 프로젝트로 이관.
- 신규 프로젝트 `teams/g/8kw-ev-wpt-tx` 생성 — 8kW EV WPT 송신 보드 Ver1.0E00, LP-AM263P 기반.

---

## [2026-06-04] ingest | oled_tv_software 03_TX_ble LED 인디케이터 + 보드 분기

- 03_TX_ble LED 3개 구현·실보드 검증: LED1(P0.09) System Ready 상시 점등, LED2(P0.08) SPI Comm Status·LED3(P0.06) BLE(ESB) Comm Status 200ms 토글. 극성 **active-high(1=ON)** 실측 확정.
- LED 핀맵 정정 과정: 초기 잘못된 핀(10/9/8) → 실측 혼선 → 정정(9/8/6, = `_shared/oled_tv_protocol.h` 원래 값). 극성도 active-low 오판정 → 정정해 active-high 확정.
- DK(PCA10040) ↔ 회사 보드 핀맵 분기: `_shared/custom_board.h` 신설(`LEDS_NUMBER 0`, UART RX=14/TX=15) + emProject `BOARD_CUSTOM`. LED 코드는 `#if defined(BOARD_CUSTOM)` 가드 — DK에선 P0.06/08이 UART라 충돌 회피.
- 갱신:
  - [[schematic_ble_module_board_v01e00]] — LED 인디케이터 GPIO 핀(P0.09/08/06)·극성, CON2 UART 핀(P0.15/14) 채움
  - [[gpio_verification_pinmap]] — 03_TX_ble LED 검증 행 3개 추가, P0.17 중복 주석 "PCA10040" → "커스텀 보드" 정정
  - [[tx_ble_module]] — LED 인디케이터·보드 분기 섹션 신설 + 현황표 2행 추가

---

## [2026-06-04] ingest | oled_tv_software ST-LINK V2 + pyOCD nRF52832 플래싱 절차 확립

- 계기: BLE_Module_Board_Ver0.1E00(nRF52832)에 `03_TX_ble` 플래싱 성공. SES 내장 다운로더·nrfjprog가 J-Link 전용이라 ST-LINK로 사용 불가 → pyOCD 우회 경로 확립.
- 핵심 함정 3개 (Windows Python 3.14 환경):
  1. `libusb-package` 바이너리 wheel 없음 → cp311 wheel에서 `libusb-1.0.dll` 수동 추출·복사
  2. ST-LINK WinUSB 바인딩(Zadig) → STM32CubeIDE 플래싱 불가(부작용), 장치 관리자로 복구
  3. `target_nRF52.py` CTRL-AP 패치 — `is_locked()`에서 `ProbeError` try/except → `return False` (ST-LINK V2가 AP#1 접근 불가)
- 추가 환원: ST-LINK 드라이버 토글 절차 (WinUSB↔ST 정품, 양방향·모드 확인·동글 2개 팁)
- 생성:
  - concepts: [[st_link_nrf52_flash]] (플래싱 how-to — 셋업·배선·절차·트러블슈팅·드라이버 토글·미확정)
- 갱신:
  - [[status]] — 다음 시작점 참고 줄에 [[st_link_nrf52_flash]] 링크 추가
  - [[rx_ble_module]] — CON1 비고에 역링크 추가
  - [[index]] — Concepts 섹션에 st_link_nrf52_flash 등록
- 미확정 잔류: CON1 물리 핀번호↔네트 매핑 (실크 Pin1 확인 필요), CON2 UART nRF GPIO 핀 라우팅

---

## [2026-06-01] ingest | oled_tv_software SPI 10ms 폴링 진단 (미달 반증·✓ 확정)

- 소스: 진단 세션 직접 보고 + 오실로스코프 캡처 `P3NOFO01.PNG` (CS Δt=10ms, 1/Δt=100Hz, Vpp=3.79V)
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control, 02_RX_ble
- 결론: "SPI 10ms 미동작"은 동작 결함이 아닌 **관측 도구 한계** (단일 필드 덮어쓰기). 10ms 폴링은 처음부터 정상.
- 생성:
  - sources: [[spi_10ms_diagnosis_report_260601]] (진단 경과·3가지 가설 반증·실보드 검증 결과)
  - assets: `spi_cs_10ms_260601.png` (오실로 캡처 — 기존 heartbeat `P3NOFO01.PNG`와 별도)
- 갱신:
  - [[spi_link_reliability]] — "미달 — SPI 10ms 폴링 ✗" → "SPI 10ms 폴링 주기 ✓", 오류율 모니터 카운터명/출력형식 정정(`spi_crc_fail_cnt`·누적+delta), `spi_tx_busy` 주석 정정(근본원인 미확인), 관련 백링크 추가
  - [[status]] — date 갱신(05-29→06-01), 다음 시작점(nRF52832 SPIS SCK datasheet ingest), SPI 10ms ✗→✓, 오류율 모니터 메모 갱신, "SPI 10ms 미동작 원인 규명" 미결 제거
  - [[index]] — spi_link_reliability 설명 갱신, 신규 source 등록
- 핵심 합의: NVIC enable은 `MX_DMA_Init()`에 정상 존재(`app_dma.c:15-19`). `PACKET_INTERVAL=10`도 이미 설정됨. 초당 100tx, CrcFail=0 확인. "미동작" 의심은 `rx_status.spi_status` 단일 필드 덮어쓰기 관측 한계.

---

## [2026-06-01] roadmap | lp-am263p 포팅 로드맵 project/task 분리 + spine 정리

- 계기: 앞으로 프로젝트·작업 로드맵을 wiki에서 작성. 외부 코드-repo `tasks/porting/roadmap.md`는 이미 2026-05-29 wiki `roadmap.md`로 ingest됨(외부보다 wiki가 최신: R27/R28 vs R24/R26) → 외부 파일 legacy화, 기존 wiki roadmap을 비판적으로 개정.
- 비판 검토에서 잡은 수정:
  - A. staleness — §6 "24라운드째"가 R27+와 어긋남(외부 R24 잔존) → R27로 정정.
  - B. "2~4주" false precision — 문서 스스로 "추정 불가"라면서 단일 숫자 제시 → 삭제, S3 게이트 기반 통일.
  - C. S5~S8 난이도 grading — 전부 미도달인데 등급 부여 → "S3 통과 후 재추정"으로 축약.
  - D. altitude 과적재 — §1 칩차이·§3 HW표가 spine 아님 + CLAUDE.md와 중복 → 백링크 위임.
  - E. §7 환원후보 80% 해소 방치 → 미해소 1건만 남기고 나머지는 "facts/handoff 반영 완료" 한 줄.
  - F. §2 "가능성 높음" 약과장 → "불가 근거 없음·미증명"으로 완화·압축.
- 구조 결정(사용자): project/task 2단위로 분리.
  - 신규 `roadmaps/porting.md` — 작업 호. S0~S8 spine·완료 기준 표·현재 위치(→status)·남은 일정·환원후보. 엄격 spine(§1 칩차이→[[is25lx256_vs_spansion_quirks]], 핸드오프→[[sbl_app_flash_handoff]], HW→[[CLAUDE]] 위임).
  - `roadmap.md` 개정 — 얇은 프로젝트 호. 목표·작업 호 인덱스(1행)·현재 위치만. S0~S8 재서술 금지(divergence 방지) → [[porting]] 위임.
- 갱신: [[lp-am263p]] `CLAUDE.md` 3-레이어 표(전략을 프로젝트/작업 2단으로), [[index]].
- 손대지 않음: `status.md`(라운드 갱신 아님, 다음 시작점 R28 유지), [[flash_open_facts]]·[[flash_open_diagnostic_log]](사실/history 단일 소스).

---

## [2026-06-01] schema | 파이프라인 도메인 자산 — 계측 인벤토리 + GPIO 검증 핀맵 + 로드맵 컨벤션

- 계기: `~eta/firmware-dev-pipeline` 두 단계(explorer/planner)가 wiki를 읽어 쓰도록 갱신됨. 그 계약을 wiki schema에 맞게 세 자산으로 빚음.
- 합의: 시작 컨텍스트 `teams/c/oled_tv_software`(핀맵 seed 풍부), 로드맵은 별도 `roadmap.md`(status 확장 아님, lp-am263p 선례), 인벤토리는 root `pages/reference/` 신설, 작업 로드맵은 `roadmaps/<task>.md`.
- 생성:
  - reference: [[instruments]] (회사 공통, Keysight InfiniiVision MSOX3104T — 무엇을·어떻게 측정 + 사용 결. 추가 장비 스텁)
  - oled concepts: [[gpio_verification_pinmap]] (기능→프로브 핀→기대값. 기존 wiki 사실만 seed, 미확인 핀은 "확인 필요"로 호명 — 추론 금지)
  - oled `roadmap.md` (M0~M6 마일스톤 호, 현재 M3 SPI 10ms 막힘, PRD 1~2ms 지연 게이트). lp-am263p 선례 결 계승
  - oled `roadmaps/README.md` (작업 로드맵 폴더 컨벤션 — 파일은 요청 시)
- 갱신:
  - root `CLAUDE.md` — 레이아웃에 reference/·roadmap.md·status.md·roadmaps/ 추가, "로드맵 컨벤션" 절 신설, "파이프라인 — roadmap 읽기/갱신 절차" 절 신설(explorer/planner 읽기 전용·wiki 작성)
  - [[lp-am263p]] `CLAUDE.md` — 3-레이어 표가 root 로드맵 컨벤션의 프로젝트별 구현임을 명시 (중복 정의 회피)
  - oled `CLAUDE.md` — 전략/검증 자산 절 추가 ([[roadmap]]↔[[status]], [[gpio_verification_pinmap]], [[instruments]])
  - [[index]]
- 핵심 결정: 읽기=파이프라인, 작성·갱신=wiki. planner는 핀번호를 추론하지 않고 wiki에 없으면 "확인 필요"로 사용자 호명. 핀맵은 P0.17 의미 충돌(TX 시작 03 vs heartbeat 02)과 RX_control 추가 GPIO 핀번호를 미확정으로 남김 — 사용자 호명 대기.

---

## [2026-05-29] ingest | lp-am263p report.md R19~R27 — 사실 원장/라운드 로그 분리 + CLAUDE.md schema 신설

- 소스: `~/eta/projects/g/lp-am263p/bp-3351/tasks/porting/report.md` (R19~R27 + R28 계획)
- 대상 프로젝트: `teams/g/lp-am263p`
- 핵심 합의: 초장기 디버그 작업의 맥락유실 방지를 위해 "작업 중 밝혀진 사실"을 **사실 원장(제자리 수정) + 라운드 로그(append-only) 2분리**. 3-레이어 = 로드맵(전략)/status(전술)/facts·log(누적).
- 생성:
  - concepts: [[flash_open_facts]] (확정 사실 + **폐기 가설(재시도 금지)** + 최유력 가설), [[flash_open_diagnostic_log]] (R7~R27 + R28 계획, append-only)
  - [[lp-am263p]] 도메인 `CLAUDE.md` 신설 (부재했음) — 3-레이어 분류·SW1 부트모드·boot flow·"자주 어긋나는 자리"
- 갱신:
  - `roadmap.md` — Round 24+→27+, **R26 반증된 `DQS_ENABLE=0` "검증 예정" 줄 제거**(stale), facts/log 위임 백링크, §7 환원후보 1·2·4·5 해소 표시
  - `status.md` — 빈 템플릿 채움: 다음 시작점 R28(jtag_flasher 공식 이식), S0~S8 현황표, 미결 4건
  - [[sbl_app_flash_handoff]] — 후보1에 R25~27 실측, 신규 §flashFixUpOspiBoot 부재(app vs flasher 비대칭), §SW1 4S 핸드오프 질문, 후보3 DQS는 R26 검증(DQS 필수·DQS=0 반증)
  - [[is25lx256_vs_spansion_quirks]] — set888mode=0x81 정정(0x71 혼동 종결), AM243 Quad/AM263P Octal 라인 차이
  - [[index]]
- 핵심 결정: R25(skipHwInit=FALSE)·R26(DQS=0) 두 진단 가설 폐기 기록 → 다음 세션이 facts.md만 읽고 재시도 방지. 최유력 가설 = SBL 잔여 8D + skipHwInit=TRUE 캡처 미스, R28에서 flasher 성공 공식 이식으로 검증.

---

## [2026-05-29] ingest | SPI heartbeat 작업 보고서 (260529)

- 소스: `tasks/spi-heartbeat/report.md` + 오실로 스크린샷 `P3NOFO01.PNG`
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
- 생성:
  - sources: [[spi_heartbeat_report_260529]]
  - concepts: [[spi_link_reliability]] (heartbeat 구현·오류율 모니터·spi_tx_busy 타임아웃 복구·10ms/9MHz 현황)
- 갱신:
  - [[comm_state_monitoring]] — 200ms 교번 사양이 코드(Heartbeat_Loop 200ms 독립 타이머)로 실현됨 확정 + 백링크
  - [[spi_packet_format]] — 전송 파라미터 "10ms/9.0Mbps"를 사양으로 명시, 실측 미달(폴링 1000ms, 9MHz revert) 주석
  - [[rx_ble_module]] — Heartbeat_Loop·P0.17 디버그 핀·펌웨어 현황 3행 추가
  - [[index]], [[status]]
- 핵심 합의:
  - 모순은 wiki↔wiki가 아니라 과거 코드(매 SPI 사이클)↔사양(200ms 매뉴얼). 오늘 코드가 사양 충족.
  - heartbeat만 실보드 검증(✓). 오류율 모니터·spi_tx_busy 복구는 △. SPI 10ms 폴링·9MHz는 ✗.
  - 10ms 미달 유력 원인: STM32 `HAL_SPI_MspInit` DMA IRQ(NVIC) 부재 → 콜백 미발생.
  - "10ms" 용어 구분: 앱 SPI 폴링 주기(PACKET_INTERVAL) ≠ ESB RF wire 주기 ([[spi_debug_log_report_260529]] 미결과 동일).
  - `_ble` 파일명은 잔재이며 ESB 라인의 정식 코드 (사용자 확인).

---

## [2026-05-29] ingest | lp-am263p 포팅 로드맵 — 전략 spine

- 소스: `~/eta/projects/g/lp-am263p/bp-3351/tasks/porting/roadmap.md` (planner roadmap)
- 대상 프로젝트: `teams/g/lp-am263p`
- 생성: `teams/g/lp-am263p/roadmap.md` — 프로젝트 루트 living doc
  - 백링크 spine 방식: 단계 구조(S0~S8)·현재 위치(S3 막힘)·남은 일정만 직접 보유
  - 깊은 디테일은 기존 concept로 위임 — [[is25lx256_vs_spansion_quirks]], [[sbl_app_flash_handoff]], [[flash_open_sequence]], [[xspi_dummy_cycles]]
  - 기능별 현황은 [[status]]와 역할 분담 (로드맵=전략, status=전술)
- 갱신: `index.md` — lp-am263p 섹션에 "Living docs"(roadmap/status) 추가
- 미결: lp-am263p 프로젝트에 도메인 `CLAUDE.md` 부재 (다른 프로젝트는 모두 보유) — 별도 생성 필요

---

## [2026-05-29] ingest | SPI 디버그 로그 검증 결과 (시나리오 A/B)

- 소스: `tasks/spi-debug-log/report.md`
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
- 생성:
  - sources: [[spi_debug_log_report_260529]]
  - concepts: [[esb_ptx_ack_assembly]] (PTX ACK payload 재조립 + ISR printf 금지 패턴)
- 갱신:
  - [[rx_to_tx_packets]] — 코드 실측 DATA 레이아웃 추가, 프로토콜 매뉴얼과의 불일치 정리 (0x50 bit 순서, 0x51 Zin·TxVoutRef 미구현, 0x52 T2 스케일 0.1°C 확인)
  - [[tx_ble_module]] — Monitor_Loop 출력 포맷 + [[esb_ptx_ack_assembly]] 링크 추가
- 핵심 합의:
  - 0x51 코드에 Zin·TxVoutRef 없음 — 프로토콜 매뉴얼 대비 미구현 필드
  - 0x50 bit2=BuckSt / bit3=Warning / bit4=Fault — 매뉴얼과 순서 다름
  - 0x52 T2 스케일은 코드 기준 0.1°C (매뉴얼 "0.01°C" 오기 해소)
  - PTX에서 g_last_ack_by_hdr[3] 패턴 필수 — 1초 윈도우 내 3헤더 보존

## [2026-05-27] ingest | Rx OLED Regulator Control Board 회로도 (OrCAD Design XML)

- 소스: `rx_oled_regulator_control_board_260327.xml` (OrCAD Design XML, 68,941줄) + `Rx_OLED_Regulator_Control_Board_260327.pdf`
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control
- 생성: `sources/schematic_rx_regulator_control_board.md`
- 갱신: `entities/rx_control.md` (CAN·DAC·추가 GPIO 신호 추가), `concepts/adc_channel_map.md` (TEMP1/TEMP2 swap 회로도 확인으로 해소)
- 확인 사항: MCU는 STM32F103VCT6/LQFP64 (OrCAD 라이브러리명 오기), 39개 _uC 신호·24개 _CN 신호 전수 추출, TEMP1_ADC_uC=PC4 좌표 매칭 확인

## [2026-05-27] ingest | RX Control UART5 Command Reference (이미지 PDF)

- 소스: `C:\Users\echog\eta\projects\c\oled_tv_software\docs\매뉴얼 (Uart Commands)_테스트용.pdf` (6p, 이미지형)
- 대상 프로젝트: `teams/c/oled_tv_software`
- 도구: Poppler pdftoppm → PNG 변환 → Claude 시각 읽기 (첫 이미지형 PDF ingest)
- 신규 생성:
  - sources: [[uart_cmd_reference_테스트용]]
- 갱신:
  - [[uart_command_set]] — phase·start 추가, dt 구문 2인자로 수정, UART5 핀(PC12/PD2) 추가
  - [[dead_time]] — dt_ratio 개념 추가, 구버전 3인자 구문 대비 표
  - [[rx_control]] — UART5 핀 테이블 추가 (MCU RCT6 유지, PDF VCT6 오기 확인)
- 핵심 합의:
  - MCU는 STM32F103**RCT6** (64핀). PDF에 VCT6로 기재되어 있으나 문서 오기 — 사용자 확인.
  - `dt` UART 명령 구문 변경: `dt <ch> <ns> <pct>` → `dt <ch> <ns>` (duty 인자 분리됨)
  - `phase`, `start` 명령 신규 확인. start = 4채널 동시 pwm start + current_phase_deg 적용.
  - dt_ratio = 데드타임/주기. freq 명령 시 3~5% 클램프 자동 적용.

---

## [2026-05-26] ingest | CC3350/CC3351 데이터시트 (SWRS284C)

- 소스: `C:\Users\echog\eta\cc3351-datasheet.pdf` (34p, Rev.C, October 2025) — wiki 밖 보관
- 대상 프로젝트: `teams/g/bp-cc3351`
- 도구: PyMuPDF(fitz) — 전체 텍스트 추출 → 챕터별 마크다운 분할 수작업
- 신규 생성:
  - raw: `raw/cc3351_datasheet/ch01_overview.md` — Features, Applications, Description, System Diagram
  - raw: `raw/cc3351_datasheet/ch02_pin_config.md` — 40핀 다이어그램, Pin Attributes 전체 표, SPI 모드 핀맵
  - raw: `raw/cc3351_datasheet/ch03_specifications.md` — AMR/ESD/동작조건/전기특성/RF성능/전류소모/SDIO·SPI·UART 타이밍
  - raw: `raw/cc3351_datasheet/ch04_description_schematic.md` — WLAN/BLE 상세 설명, Reference Schematic 주요 연결
  - raw: `raw/cc3351_datasheet/ch05_support.md` — Tools & Software, 문서 목록, Revision History
  - raw: `raw/cc3351_datasheet/ch06_packaging.md` — Orderable Information, T&R 치수, Package Outline
  - sources: [[cc3351_datasheet]] — 소스 인덱스 + 핵심 요약 + raw 챕터 링크
- 파생 페이지 미생성 (lazy): `cc3351_ic`, `cc3351_pinmap`, `cc3351_power_rails`, `cc3351_host_interface` — lp-am263p 포팅 작업이 trigger할 때 생성
- 핵심 합의:
  - CC3350(Wi-Fi 6 only) vs CC3351(Wi-Fi 6 + BLE 5.4). Pin-to-pin 호환.
  - Host I/F: SDIO 4-bit (≤52MHz) or SPI (≤26MHz) for Wi-Fi, UART (≤4364kbps) for BLE HCI.
  - SPI 핀: CS=SDIO_D3(21), SCLK=SDIO_CLK(19), PICO=SDIO_CMD(18), POCI=SDIO_D0(24), IRQ=HOST_IRQ_WL(29).
  - 전원: VMAIN/VDDA/VIO=1.8V, VPA=3.3V. 전원 시퀀싱: 모든 공급 안정 후 nRESET low ≥10µs → 해제.
  - 클럭: 40MHz XTAL 필수(외부), 32.768kHz 슬로우 클럭 내부 생성 가능.

---

## [2026-05-26] ingest | STM32 mini-pro v10 회로도 — SPI 수동 추출

- 소스: `projects/c/oled_tv_software/docs/Schematic/회로도 (STM32F103RCT6).pdf` — 이미지 기반 PDF, 텍스트 레이어 없음. SPI 연결 부분만 수동 추출.
- 추출 내용: STM32 SPI2 핀맵 (PB12=CS, PB13=SCL, PB14=SDO, PB15=SDI — 슬레이브 관점 표기).
  - SDO(PB14) = MISO (마스터 관점), SDI(PB15) = MOSI (마스터 관점). 기존 코드 분석과 일치.
- 신규 생성:
  - sources: [[schematic_stm32_mini_pro_v10]] — 회로도 레이블·마스터 명칭 대응표 + STM32↔nRF52832 PCA10040 배선표
- 갱신:
  - [[rx_control]] SPI 절 — "transparent bridge" 오기 제거, 새 페이지 링크로 교체
- 미기록: PCA10040 커넥터 헤더 핀 번호 (GPIO→헤더 위치 매핑). 필요 시 PCA10040 Hardware Spec 참조 후 추가.

---

## [2026-05-26] ingest+restructure | PRD v1.0 ingest + SPI/ESB 프레임 분리 재구조화

- 트리거: PRD(`projects/c/oled_tv_software/docs/prd.md`) 최초 ingest. PRD에서 STM32-nRF SPI(56B/45B, HDR 0xC0)와 ESB wire(11B, HDR round-robin)가 서로 다른 포맷임이 명시됨.
- **핵심 정정**: 기존 wiki의 "무선모듈 transparent bridge, SPI 11B = ESB wire" 주장 취소. nRF가 두 포맷을 능동 변환함을 확정.
- 재구조화:
  - `spi_packet_format` 재작성 → STM32-nRF 내부 SPI 프레임 전용 (56B/45B, HDR 0xC0, 20ms)
  - 신규 `esb_packet_format` — ESB wire 포맷 전용 (11B, HDR 0x10-0x52, 10ms, ACK with payload). 기존 spi_packet_format의 ESB 내용 이전.
  - `tx_to_rx_packets`, `rx_to_tx_packets` backlink: `[[spi_packet_format]]` → `[[esb_packet_format]]`
  - `spi_protocol_manual_260513` 소스 페이지: "SPI 매뉴얼"이 아닌 "ESB wire 사양 정의 문서"로 정정. "transparent bridge" 설명 제거.
  - `rx_ble_module` — 통신 페어 절 분리(SPI 내부/ESB wire), 펌웨어 현황 표 추가.
- 신규 생성:
  - raw: `prd_v1.0.md`
  - sources: [[prd]]
  - entities: [[tx_ble_module]] — 03_TX_ble nRF52832 PTX, TX보드 SPI 미구현
  - concepts: [[esb_link_layer]] — ESB 링크 파라미터(10ms, ACK with payload, NRF_ESB_MAX_PAYLOAD_LENGTH=64), 미결 파라미터 목록
- PRD의 미해결 의문점 (기존 wiki 관련):
  1. PWM 주파수 불일치 — [[pwm_system]] 기록 있음, PRD에서 재확인
  2. ADC 물리량 변환 미구현 — [[adc_channel_map]] 기록 있음
  3-5. CAN1/DAC 용도, README 역할 오표기 — 미문서화, 후속 확인 필요
  6. SPI 하드웨어 테스트 미실시
- PRD 업데이트 시: 새 버전 `raw/prd_vX.Y.md` 추가 + `sources/prd.md` frontmatter 갱신.

---

## [2026-05-26] ingest | bp-cc3351 프로젝트 신설 + EVM User Guide ingest

- 배경: lp-am263p 포팅 원본 source 보드(BP-CC3351)를 별도 프로젝트로 분리 결정.
- 합의사항 반영:
  - `wiki/CLAUDE.md` — "크로스 프로젝트 참조 규칙 (first-ingest-wins)" 단락 추가
  - `teams/g/bp-cc3351/CLAUDE.md` — reference-only 성격·lazy ingest 원칙·cross-ref 대상 명시
- 신설 디렉토리:
  - `teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/` — EVM UG 챕터별 마크다운 6개 파일
  - `teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/` — PNG 26장 (파일명에 원본 페이지 번호 인코딩)
  - `teams/g/bp-cc3351/pages/{entities,concepts,sources}/` — scaffold
- 생성 페이지:
  - sources: [[bp_cc3351_evm_ug]] — 챕터 인덱스 + 추출 품질 메모 + lazy ingest 후보 목록
- 갱신:
  - `wiki/index.md` — `## teams/g/bp-cc3351` 섹션 신설
- 핵심 합의:
  - EVM UG 23p → 6 챕터 분할 (`ch00`–`ch05`). 포팅 핵심은 `ch02_hardware.md` — P1/P2 2×20핀 핀맵(Table 2-3/2-4), JTAG 헤더(Table 2-5/2-6), 전원, 클럭.
  - pymupdf4llm 1.27.2.3 추출. GFM 테이블·이미지 모두 정상.
- 파생 페이지 미생성 (lazy): `boosterpack_pinmap`, `jtag_header_bp_cc3351`, `power_rails_bp_cc3351`, `clocking_bp_cc3351` — lp-am263p 포팅 작업이 trigger할 때 생성.

---

## [2026-05-22] ingest | rx_control ADC 채널 매핑 + TEMP 라벨 swap 함정

- 트리거: 사용자 — "STM32에서 ADC 값 읽고 nRF로 보내고 Tx까지 가는 거 맞지? 평가보드 어느 핀에 어떻게 전압 넣어?"
- 소스:
  - `01_RX_control/RX_control.ioc` — ADC1 6채널 매핑, GPIO_Label, sampling
  - `Application/Src/app_adc.c` — `MX_ADC1_Init`, DMA1_Ch1 circular, `adc_conv()`
  - `Application/Src/common.c:157-172` — `adc_calc()` (raw → 0~3.3V만, 분압 미적용)
  - `Application/Inc/common.h:17-31` — Front-end R값 상수 + NTC 모델
  - `_shared/oled_tv_protocol.h:140-148` — `rx_adc_raw_data_t` 구조체 순서
- 발견 (라벨 swap 함정):
  - ioc GPIO_Label: PC4=`TEMP2_ADC`, PC5=`TEMP1_ADC`
  - 그러나 ADC rank 등록 순서 + DMA 버퍼 구조체 필드 순서로 인해 `sensing_data.stack_temp1` = PC4 = silkscreen `TEMP2_ADC`. 보드 라벨과 SW 필드명이 한 쪽 swap 상태.
  - 어느 쪽이 틀린지 (보드 vs SW)는 회로도/실측으로 결정 필요 → 후속.
- 발견 (스케일 미적용):
  - `common.h`에 분압/션트 R값과 NTC β 모델 정의는 있으나 `adc_calc()`는 raw→0~3.3V 단순 환산만. 따라서 `rx_module.rx_data.vrect` 등에 들어가는 값 = 핀 전압 그대로. 0.01V 스케일 uint16 wire 변환은 SPI 송신 코드(미독)에서 이뤄지는 것으로 추정.
- 생성/갱신:
  - 신규 concept [[adc_channel_map]] — 채널 표, swap 함정, 시험 가이드, 스케일 상수 표 + 미적용 사실
  - [[rx_control]] — UART 절 다음에 ADC 절 추가 (요약 + concept 페이지 링크)
  - [[index]] — Concepts에 adc_channel_map 등록
- 데이터 흐름 (위키에 박은 그림): `ADC pin → ADC1 (6ch, cont., DMA circular) → sensing_data → adc_calc → rx_module → SPI2 → SPIS1 → ESB → Tx`. 세 단계 모두 transparent.
- 후속 (페이지 미생성):
  - SPI 송신 코드에서 float → wire uint16 (0.01 스케일) 변환 지점 확인 — 별도 ingest 시 [[adc_channel_map]] §Front-end 절 갱신.
  - 회로도 ingest 후 TEMP1/TEMP2 라벨 swap 진위 결정.

---

## [2026-05-22] update | rx_control↔rx_ble SPI 핀맵·모드 정합 보강

- 트리거: 사용자 — "각자 핀은 어떻게 되있어?" → 매뉴얼/위키엔 커넥터 핀까지만 있고 양쪽 MCU GPIO·페리 인스턴스는 ingest 안 돼 있던 상태.
- 소스 확인:
  - STM32: `01_RX_control/RX_control.ioc` + `Application/Src/app_spi.c:16-29` (`MX_SPI2_Init`)
  - nRF: `02_RX_ble/Application/main.c:103-105, 467-475` + `_shared/oled_tv_protocol.h:69-72`
- 사실:
  - **STM32 SPI2 / PB12-15** (nCS=PB12 SW, SCK=PB13, MISO=PB14, MOSI=PB15). NSS_SOFT, 8-bit, MSB, /4 prescaler → 9.0 Mbps.
  - **STM32 모드 mode 2**: `CLKPolarity=HIGH`+`CLKPhase=1EDGE` → CPOL=1, CPHA=0.
  - **nRF SPIS1 / P0.22(CS)·P0.27(SCK)·P0.25(MOSI)·P0.26(MISO)**. `NRF_SPIS_MODE_2`로 STM32 측과 정합 확인.
  - DMA: STM32 측 TX=DMA1_Ch5, RX=DMA1_Ch4 (byte, NORMAL).
- 갱신 페이지:
  - [[rx_control]] SPI 절 — 페리(SPI2)·핀맵 표·모드·NSS_SOFT·DMA 추가
  - [[rx_ble_module]] CN3 표 — nRF GPIO 컬럼 추가, SPIS1 인스턴스/MODE_2/드라이버 버퍼 명명 함정 명시
- 핵심: nRF 드라이버에서 `tx_module_data_t`를 SPIS **RX 버퍼**로 넘기는 부분이 명명상 헷갈리는 지점 — "어디서 오는가" 기준이라 그렇다는 점을 위키에 박아둠.
- 후속 (미반영): `02_RX_ble`/`03_TX_ble` → ESB 전환 시 CN3 핀맵·모드는 유지 가정, 변경 시 본 페이지들 재갱신.

---

## [2026-05-22] revert | 직전 ESB 페이로드 ingest 철회 + 260513 매뉴얼을 ESB wire 사양으로 복권

- 트리거: 사용자 — "지금 보내준 데이터는 프로그래밍 상에서 데이터를 어떻게 관리할지에 관한 것들로 보임". 직전 ingest가 잘못된 가정 위에 세워졌음.
- 잘못된 가정 (직전 entry): `_shared/oled_tv_protocol.h`의 `tx_module_data_t` / `rx_module_data_t`를 무선 wire format으로 간주.
- 정정: 그 헤더는 **MCU 내부 데이터 모델** (센싱·상태값 관리용). **무선 wire format은 260513 매뉴얼이 정의한 11 B 패킷 (0x10/0x11/0x12 TX→RX, 0x50/0x51/0x52 RX→TX)**. 무선모듈이 transparent bridge라 SPI 11 B 프레임이 곧 무선 페이로드 — ESB 전환 후에도 동일.
- 삭제 페이지:
  - sources: `oled_tv_protocol_h.md`
  - concepts: `esb_payload_tx_to_rx.md`, `esb_payload_rx_to_tx_ack.md`
  - raw: `oled_tv_protocol.h` 사본
- 복원 페이지 (직전 historical 분리 되돌림):
  - [[spi_packet_format]] / [[tx_to_rx_packets]] / [[rx_to_tx_packets]] frontmatter에서 `historical, ble` 제거 + `esb` 태그 추가, 본문 상단 deprecation 노트 제거. `spi_packet_format`에 "ESB 매핑" 절 신설 (PTX/PRX 매핑, ACK payload 운용).
  - [[spi_protocol_manual_260513]] 소스 페이지의 historical 표시 제거, "이 11 B 프레임이 곧 end-to-end 무선 wire 사양"으로 단언.
  - [[rx_control]] SPI 절 원복.
  - `index.md` Historical 서브섹션 제거, 본 영역에 ESB 표시 추가.
- 핵심 교훈:
  - "wire format은 코드의 struct에 있다"고 가정하지 말 것. **수기 매뉴얼이 우선**이고, 코드 struct는 사내 구현 모델일 수 있음.
  - "데이터는 그대로"의 사용자 의미는 **매뉴얼 사양 유지**이지 코드 struct 유지가 아니었음.
- 후속 (페이지 미생성):
  - [[esb_link_layer]] — ESB 무선 파라미터 (역할/채널/주소/bitrate/ACK retry 등) 결정 시 환원.
  - [[nrf_bridge_design]] — nRF 펌웨어 내부 SPI↔ESB 브리지 동작/스케줄 (라운드로빈 vs 묶음).
  - `_shared/oled_tv_protocol.h`의 내부 모델 ↔ 11 B wire 사양 간 매핑(직렬화/역직렬화)이 코드에서 어떻게 구현되는지 — 필요 시 별도 ingest.

---

## [2026-05-22] ingest | OLED TV ESB 페이로드 사양 (BLE 시절 SPI 매뉴얼과 분리) — *REVERTED 2026-05-22*

> **REVERTED.** 위 revert entry 참조. 본 entry는 작업 이력 보존 목적으로만 남김.

- 트리거: 사용자 — "ble 통신을 esb 통신으로 바꿀 예정, 대신 보내는 데이터 자체는 그대로". ESB-TX↔ESB-RX 페이로드 결정 작업 중.
- 소스: `projects/c/oled_tv_software/_shared/oled_tv_protocol.h`
- raw 사본: `teams/c/oled_tv_software/raw/oled_tv_protocol.h`
- 생성 페이지:
  - sources: [[oled_tv_protocol_h]]
  - concepts: [[esb_payload_tx_to_rx]] (45 B), [[esb_payload_rx_to_tx_ack]] (56 B, ACK payload)
- 갱신 페이지:
  - [[rx_control]] — SPI 절을 ESB 기준으로 갱신, BLE 시절 페이지는 historical 링크로 분리
- Historical 분리 (이전 ingest의 가정 변경):
  - [[spi_packet_format]] / [[tx_to_rx_packets]] / [[rx_to_tx_packets]] frontmatter에 `historical, ble` 태그 추가, 본문 상단 deprecation 노트
  - 직전 ingest(260513) 때 "패킷 구조는 ESB에서도 유지"로 가정했지만 실제로는 전 항목이 바뀜: 11 B 고정→가변, 헤더 ID(0x10/0x50 등)→0xC0 단일, CRC→XOR, bit-packed Uint16(0.01 스케일)→struct float, 10 ms→20 ms.
- 핵심 합의:
  - **무선 계층만 교체, 데이터는 그대로**. SPI 브리지 프레임이 곧 ESB 페이로드 (transparent, 단편화 없음).
  - **ACK payload로 양방향**: PTX=ESB-TX(20ms 주기 마스터), PRX=ESB-RX. RX→TX는 PRX가 FIFO에 미리 적재 → PTX 다음 송신 때 piggyback. RX→TX 주기는 PTX에 종속.
  - **wire 호환의 본질**은 `#pragma pack(1)` + 모든 enum `__attribute__((__packed__))`. 두 페이지 모두 `_Static_assert(sizeof == ...)` 단정 권장.
  - 헤더 상단 주석/`RX_BLE_ADV_NAME` 매크로는 BLE 전제 표현 — 구조체는 transport 무관, 주석·매크로만 ESB 표현으로 갱신 필요.
- 후속 (페이지 미생성):
  - [[esb_link_layer]] — ESB 무선 파라미터 (역할/채널/주소/bitrate/ACK retry 등). 사내 결정 또는 SDK 예제 기반으로 결정되면 환원.
  - [[nrf_bridge_design]] — nRF 펌웨어 내부 SPI↔ESB 브리지 동작/버퍼링/타이밍.
  - `02_RX_esb` / `03_TX_esb` 코드는 아직 존재하지 않음 (`02_RX_ble` / `03_TX_ble`만 있음). 구현 시 ingest 대상.

---

## [2026-05-22] ingest+update | IS25LX256 device descriptor 검증 + 진단 트리 작성

- 트리거: 사용자 — "다음에 포팅 과정에서 '왜 이런 문제가 발생했고 무엇이 원인이고 어떻게 해결했더라?' 라는 관점으로 질문할 예정". 미래 자기 질문에 답이 되는 진입점 구조로 정리.
- 발견: IS25LX256 device descriptor 위치 확정
  - SysConfig JSON: `C:\ti\mcu_plus_sdk_am263px_26_00_00_01\source\sysconfig\board\.meta\flash\IS25LX256.json` (111 lines, SDK installer 동봉)
  - **GitHub `TexasInstruments/mcupsdk-core` public 미러에는 미공개** — `source/sysconfig/` 트리 전체가 제외됨. SDK 인스톨러에서만 얻을 수 있음.
- raw 사본 신설: `teams/g/lp-am263p/raw/mcupsdk/source/sysconfig/board/.meta/flash/IS25LX256.json`
- 디스크립터 검증 (datasheet 대조):
  - `rdIdSettings.dummy8 = 8` ✓ (ch08 Table 8.1, 8D-8D-8D RDID dummy=8)
  - `p888d.protoCfg.bitP = 231 (0xE7)` ✓ (ch06.5 VCR 0x00: E7h=Octal DDR with DQS)
  - `p888d.dummyCfg.bitP = 16` ✓ (ch06.5 VCR 0x01: 16 dummy cycles)
  - `p888d.cmdRd/cmdWr = 0x7C/0x84` ✓
  - `flashManfId=0x9D, flashDeviceId=0x5A19` ✓ (ISSI)
  - **디스크립터 자체는 datasheet와 완전 일치 → sweep 실패의 원인은 디스크립터가 아님**
- 갱신 페이지:
  - [[sbl_app_flash_handoff]] — "진단 트리" 절 신설. 사용자 관점("왜/원인/해결") 4가지 원인 후보 정리:
    1. Chip이 8D mode 진입 못 함 (skipHwInit 게이트 문제)
    2. `Flash_quirkSpansionUNHYSADisable` SysConfig 자동매핑 (가능성 높음)
    3. DQS 모드 불일치 (chip은 E7h DQS-on, OSPI 컨트롤러는 DQS-off일 때)
    4. ECC ON 상태에서 dummy table 불일치 (드뭄)
  - [[mcupsdk_flash_nor_ospi]] — "아직 안 읽은 것"에서 디스크립터 항목 ✓ 갱신 (위치 + 검증 결과)
  - [[is25lx256_vs_spansion_quirks]] §6.5 — 진단 트리 cross-link 추가
- 후속: SysConfig가 어디서 `params.quirksFxn`을 `Flash_quirkSpansionUNHYSADisable`에 연결하는지 — `ti_board_config.c` / `ti_board_open_close.c` 정독 시 처리

---

## [2026-05-22] update | `Flash_norOspiReadId` STIG dummy resolution 분석 보강

- 트리거: 사용자 sweep 디버깅 컨텍스트 — "SetModeDummy가 controller dummyClks=16 설정 후 ReadId 호출하면 STIG가 16으로 나가는가?"
- 분석 (flash_nor_ospi.c line 847-913 `Flash_norOspiReadId` + line 99-117 `Flash_norOspiCmdRead`):
  - `Flash_norOspiReadId`는 STIG dummy를 **controller register에서 inherit 하지 않음**. 함수 내부 local `dummyBits` 변수를 직접 STIG에 박는다.
  - non-8D: 항상 `dummyBits=0` (literal, line 858)
  - 8D-8D-8D: `dummyBits = idCfg->dummy8` (line 864) — devCfg->idCfg.dummy8 별도 필드
  - 결론: `OSPI_setCmdDummyCycles(16)` 호출 직후 ReadId 호출해도 STIG dummy는 16 아님. non-8D는 0, 8D는 idCfg.dummy8.
- 함의: `idCfg.dummy8`과 `protocolCfg.dummyClksCmd`는 device descriptor의 별도 필드. RDID는 idCfg.dummy8만 사용. 두 필드 일관성이 descriptor 작성자 책임.
- 8D ReadId 실패 시 capture delay sweep loop(line 1250-1255)으로는 보정 불가 — capture delay는 phase 보정, dummy는 cycle count 차이라 데이터 자체가 시프트.
- 갱신 페이지:
  - [[flash_open_sequence]] — 신규 §RDID dummy resolution (결정 로직, 두 dummy 필드 분리, capture sweep 보정 불가 이유), 위험 포인트에 RDID dummy field 항목 추가
  - [[sbl_app_flash_handoff]] — 정합성 깨짐 지점 §4 신설(idCfg.dummy8 불일치), 진단 절차 dump 대상 필드에 idCfg.dummy8 명시
- 후속: IS25LX256 device descriptor 파일 위치 확인 + idCfg.dummy8 실제 값이 8 (datasheet ch08 Table 8.1)과 일치하는지 검증 — 진행 중

---

## [2026-05-22] update | `Flash_quirkSpansionUNHYSADisable` SysConfig 자동매핑 함정 보강

- 트리거: 사용자가 sweep 디버깅 중 0x71/0x65 opcode를 driver에서 발견. 이 opcode들은 IS25LX256 Command Table(ch08.2)에 존재하지 않음 확인.
- 실측: `flash_nor_ospi.c` line 1374-1403 `Flash_quirkSpansionUNHYSADisable` 함수가 line 1381 `Flash_norOspiRegRead(0x65, 0x00800004)` (Spansion RDAR), line 1399 `Flash_norOspiRegWrite(0x71, 0x04, ...)` (Spansion WRAR)를 호출. 함수는 같은 파일 내에선 호출되지 않음 — caller는 SysConfig 생성 board init이라고 사용자 보고.
- ISSI 측 거동: ch08.1 line 9 "incorrect command → standby" 규칙에 따라 0x65/0x71 모두 디코드 되지 않음. read는 bus default(0xFF) 리턴 → UNHYSA bit가 "이미 1"로 잘못 판단 → write 스킵으로 운 좋게 no-op으로 끝나는 케이스가 흔함. 단 read가 0x00 리턴 시 0x71 write 시도 → WEL 상태 어긋날 위험.
- 갱신 페이지:
  - [[is25lx256_vs_spansion_quirks]] — §2에 ISSI "incorrect command → standby" 인용 추가, §6.5 신설 (SysConfig 자동매핑 함정 + 워크어라운드 + 검증법), 체크리스트에 항목 추가
  - [[mcupsdk_flash_nor_ospi]] — 라인 인덱스 1374-1403 항목에 opcode/주소/caller 정보 보강
- 후속 (미반영, 별도 ingest 후보):
  - **RDID(0x9F) 8D DDR 시퀀스 concept 페이지** — Table 8.1: addr bytes 0, dummy 8, 8-0-8 protocol. sweep 실패 진단 시 진입점.
  - SysConfig에서 IS25LX256 디스크립터의 quirk 매핑 실체 위치 (`Flash_DevConfig` 어느 필드인지) — `flash_nor_ospi.h` ingest 시 처리.

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
