# log

시간순 작업 로그. 형식: `## [YYYY-MM-DD] <타입> | <제목>`

---

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
