# wiki index

전체 페이지 카탈로그. 페이지 추가/갱신 시 여기에 등록한다.

---

## 공통 (모든 팀·프로젝트)

### Living docs

- [roadmaps/linux_migration.md](roadmaps/linux_migration.md) — **Windows→Ubuntu 전환 로드맵**(L1 백업~L8 파티션 회수, living-doc). 듀얼부팅→**검증 게이트 L6**(보드별 빌드·플래시·디버깅)→런처 포팅→회수. 현재 L0 미착수(2026-06-22 결정만). 결정·근거는 [[linux_migration]]

### Concepts

- [[linux_migration]] — **Windows 11 → Ubuntu 24.04 LTS 개발환경 전환 결정·근거**(전사 공통): 배포판 선택(CCS 공식지원 24.04)·듀얼부팅+회수 전략(**ESP 삭제 금지**·WSL2 배제)·동기 3종(거부감/장기 Linux 스킬/Edge AI 장기동인)·툴체인 4종 portability 평가표(전부 네이티브 Linux)·런처 포팅 대상(`.ps1`/`.bat`→`.sh`). 단계는 [roadmaps/linux_migration.md](roadmaps/linux_migration.md) 위임
- [[schematic_ingest_strategy]] — 회로도를 비전 처리 없이 텍스트로 ingest하는 Tier별 전략 (EDA export → CSV/netlist)
- [[firmware_git_workflow]] — **펌웨어 Git 워크플로 표준(전사 공통)**: 트렁크 기반(`main` 단일)+annotated 릴리스 태그(SemVer `v0.x.y`). 핵심=**태그는 소스만 고정, 동일 바이너리는 고정 툴체인+의존성과 함께일 때만**(cf. [[sdk_ccs_toolchain_migration]]). **Tier 계층**: 지금 active=Tier 1(**PR 필수**·**Conventional Commits**·annotated 태그+git hash 임베드·**최소 CI 빌드 게이트**·repo `CONTRIBUTING.md`) / Tier 2(2번째 사람·v1.0.0→리뷰 require·코드서명) / Tier 3(다중 버전→`release/x.y`·Docker 툴체인 핀·west). CI 전제=헤드리스 빌드(TI gmake ✓·STM32CubeIDE 막힘 [[cubeide_cli_build_trap]], [[linux_migration]]와 정렬). 핫픽스 forward-only

### Reference

- [[instruments]] — 회사 공통 계측 장비 + 프로그래밍/디버그 프로브 인벤토리 (Keysight MSOX3104T·Saleae Logic Pro 16 / ST-Link V2·**J-Link V9.3 Plus SN69730359**(nRF 정본)·SAM-ICE SN24012600). **2026-06-15 §정정: J-Link OB SN1050329071 현존 미확인·프로브 식별은 ShowEmuList 실측 규율**. planner가 검증 경로에 인용
- [[contributing_template]] — **CONTRIBUTING.md 단일 템플릿(회사 공통)**: [[firmware_git_workflow]] 표준의 repo-side 산출물. 본문 100% 공통 + 상단 `프로젝트별` 블록(프로젝트명·MCU·툴체인·빌드 명령·CI 여부)만 수정해 어느 repo에도 복사. 정본=wiki(org `.github`/`firmware-ci` 마련 시 승격)

---

## teams/c/oled_tv_software

### Living docs

- [roadmap.md](teams/c/oled_tv_software/roadmap.md) — 전체 로드맵(M0~M3 현재 스코프 달성·M4~M6 보류 2026-06-09). 전략 spine, 현재 위치는 status 위임
- [roadmaps/pc-gui.md](teams/c/oled_tv_software/roadmaps/pc-gui.md) — `pc-gui` 작업 호(G0~G3 **✓ 완료** `35b94d0`, 실보드 검증). UART 바이너리 모니터링 + buck 설정 호스트 툴. G0 결정=UART5 단일 포트·monitor 텍스트→바이너리. 산출물 [[pc_uart_gui]]
- [roadmaps/spi-esb-refactor.md](teams/c/oled_tv_software/roadmaps/spi-esb-refactor.md) — `spi-esb-refactor` 작업 호(R1~R4) — **코드 `9be1a7a` 추월: R1~R3 부분 구현·R4 무효(이미 `PKT_HDR_*`)**. §6 `_shared` 매크로 점검. 적출은 [[app_protocol_module]]
- [roadmaps/04-tx-control-dummy.md](teams/c/oled_tv_software/roadmaps/04-tx-control-dummy.md) — `04_tx_control` 더미 작업 호(D0~D3) — 03 SPI_Loop 활성화 + STM32 SPI Master 더미 프로젝트. 최종 목표: 01→02→ESB→03→04 Vout Ref 전달 E2E 검증
- [status.md](teams/c/oled_tv_software/status.md) — 기능별 구현 현황표·다음 시작점 (파이프라인이 커밋마다 갱신)

### Entities

- [[rx_control]] — STM32F103RCT6 보드, PWM 채널 매핑·BKIN 핀·SPI Master
- [[tim8]] — Advanced Timer, PWM1(CH1/CH2) + BKIN(PA6)
- [[tim3]] — General Timer, PWM2(CH3/CH4). BDTR 없음
- [[rx_ble_module]] — 02_RX_ble, nRF52832 ESB PRX. SPI Slave(STM32 Master 확정). BLE 시절 명칭 잔류
- [[tx_ble_module]] — 03_TX_ble, nRF52832 ESB PTX. LED(LED1 P0.09·LED2 P0.08=spi_comm_st mirror·LED3=ble_comm_st mirror, 기본 DK P0.19/회사 P0.06 매크로)·DK↔회사 보드 분기(custom_board.h). TX 보드 SPI=SPIS 재작성(△ 미검증, `e706b53`)
- [[uto_nbk_52]] — 커스텀 nRF52832 모듈(02·03 사용). **UTO-NBL-52와 별개 보드**(NBK 회로도·BOM 미인입). LED 3개 모두 **active-HIGH**(P0.09/08/06) 실보드 확정·SPI(SPIS1 P0.22/25/26/27)·격리형 UART(P0.15/14)·RESET(P0.21)·DEVICEID 보드 식별

### Concepts

- [[team_briefing_oled]] — C팀 oled_tv_software 주간 업무보고 참고 자료 (보고 스냅샷 이력·작업 호 현황·진행/문제·다음계획 living-doc)
- [[sysclk_hsi_transition]] — HSE 발진 실패(HSERDY 100ms 타임아웃) → HSI 전환. 확정 클럭 트리(HCLK 64/APB 32/타이머 64/ADC 8 MHz). SPI 8Mbps·CAN 비트레이트 재계산 필요. (2026-06-15)
- [[pwm_system]] — TIM8/TIM3 64MHz·100kHz·120도 위상, `pwm_init`/`set_duty`/`pwm_set_freq`
- [[dead_time]] — SW CCR offset 방식. TIM3에 BDTR 없어 두 타이머 통일
- [[trip_zone]] — TIM8 BKIN(PA6) → `HAL_TIMEx_BreakCallback`로 PWM 전체 차단
- [[uart_command_set]] — `duty`/`freq`/`dt`/`phase`/`start`/`stop`/`reset`/`buck` (UART5, 115200/8N1, PC12/PD2). ISR 구동 수신·prefix 매칭 파싱. ⚠️ command 채널(host→01)은 텍스트, 반대 모니터(01→host)는 `35b94d0`부터 바이너리
- [[buck_vout_ref_command_path]] — `buck <v>` = RF 링크 건너는 유일한 UART 지령. 01 UART5 → 0x51 DATA[6,7](volts×100) → 03. 검증 `buck 123.34`→`12334`. `35b94d0`: host 확인은 바이너리 0x51 파싱([[pc_uart_gui]]). 새 tx 지령 추가 패턴
- [[pc_uart_gui]] — **host PC GUI**(`tools/pc_uart_gui/uart_gui.py`, Python+Tkinter+pyserial, `35b94d0` ✓실보드). 단일 UART5, 11B HDR 동기+CRC 재동기, **6패널 2×3**(TX/RX Status·Input·Output), Physical 변환 적용(V·A ×0.01/°C ×0.1), FW 버전 표시, 활성 비트 굵게, `Link: SPI/ESB [UP/DOWN]`, buck 송신. **TX Buck Set E2E 실측 ✓(2026-06-12, COM17, 3보드, `Tx_Buck_Vout_Ref=22222`)**. 스크린샷 [[pc_uart_gui_verification_260612]]
- [[cubeide_newlib_nano_float]] — CubeIDE newlib-nano float 함정(`nanoprintffloat`/`nanoscanffloat`). scanf float 꺼지면 `buck 15.5` 소수 깨짐. 구성별 독립·Release 재확인
- [[cubeide_cli_build_trap]] — CubeIDE **CLI 빌드 불가**(`stm32cubeidec.exe` GUI 서브시스템·즉종료) → IDE **Ctrl+B** 직접 빌드. CubeMX 재생성 금지
- [[adc_channel_map]] — ADC1 6채널 핀맵(PA0~PA3, PC4/PC5) + TEMP1/TEMP2 라벨 swap 함정 + 평가보드 시험 가이드
- [[spi_packet_format]] — STM32-nRF 내부 SPI wire 포맷 (11B 고정, HDR 0x10~0x12/0x50~0x52). ESB와 동일 패킷 구조
- [[spi_pin_mapping]] — STM32↔nRF52 SPI 물리 배선 핀맵 (SCK PB13↔P0.27 / MOSI PB15↔P0.25 / **MISO PB14↔P0.26** / CS PB12↔P0.22). MISO 미연결 시 spi_rx_pkt 전부 0xFF → SpiCommSt DOWN. (DK 실측 2026-06-16)
- [[nucleo_f103rb_morpho_pinmap]] — NUCLEO-F103RB morpho 커넥터 핀맵(04_tx_control SPI 배선용). CN10-16(PB12/CS)·CN10-26(PB15/MOSI)·CN10-28(PB14/MISO)·CN10-30(PB13/SCK) 이미지 직독 (2026-06-18). [[spi_pin_mapping]] 04↔03 링크 보강
- [[esb_packet_format]] — ESB wire 포맷 (11B, HDR round-robin 0x10-0x12/0x50-0x52, `ESB_TX_INTERVAL_MS=1ms`, ACK with payload, CRC-valid only 콜백)
- [[esb_link_layer]] — ESB 링크 파라미터 (`ESB_TX_INTERVAL_MS=1ms`, ACK with payload, NRF_ESB_MAX_PAYLOAD_LENGTH=64) + 미결 파라미터
- [[esb_timing_measurements]] — ESB 실측 타이밍(오실로): TX→ACK ~470µs / TX 주기 ~920µs / ACK 주기 ~940µs. P0.17/18 GPIO 프로브, 03_TX_esb esb 브랜치
- [[tx_to_rx_packets]] — TX→RX: 0x10 시스템상태 / 0x11 입력 Analog / 0x12 출력 Analog+온도
- [[rx_to_tx_packets]] — RX→TX (ESB ACK payload): 0x50 시스템상태 / 0x51 입력+Tx Vout Ref / 0x52 출력+온도 (코드 실측 레이아웃 + 불일치 추가)
- [[esb_ptx_ack_assembly]] — PTX 모드 ACK payload 재조립: g_last_ack_by_hdr[3] 패턴 + ISR printf 금지
- [[comm_state_monitoring]] — 0x10 Data[0] bit5/6은 tx_status 아닌 통신 링크 비트. SPI_Comm_St=200ms heartbeat(✓`e5e3efc`), BLE_Comm_St=ESB presence 리셋윈도우(02·03 각자 수신 delta, ✓`6cd7e6c`). `d2232fe`: (T,N) 직접 상수·`spi_status` LINK/CRC 분리. **`35b94d0`(2026-06-10): monitor 텍스트→11B 바이너리 전환, COMM 텍스트 라인 폐기 — 링크 health는 0x10 d0 bit5/6으로 운반(host [[pc_uart_gui]])**. 심볼 컨벤션·라벨 구분·**race-free stamp(상태비트는 송신복사본 spi_tx_pkt에)**
- [[spi_link_reliability]] — SPI heartbeat 구현(200ms 독립 타이머, P0.17 검증)·오류율 모니터·spi_tx_busy 타임아웃 복구·10ms 폴링 ✓ 검증 완료·9MHz 상향 미달
- [[app_protocol_module]] — 01_RX_control SPI 프로토콜 계층 적출·핸드오프(`9be1a7a`). 공개 API `protocol_loop()` 하나 + 전역 3개(rx_module/tx_module/rx_cmd), 내부 `exchange_packets`/`print_packets`. 4파일 자립(common.h 역의존 끊음), W1 트랜스포트 직접호출·D1 전역 유지. **`35b94d0`: `print_packets` 11B 바이너리 송출(`uart_send`)·`print_comm_line_on_change` 삭제**. STM32CubeIDE 빌드+실보드 동작확인 ✓. **3펌웨어 표준 패턴 원형**: app_spi/app_esb=저수준·app_protocol=두꺼운 응용 계층·`protocol_loop()` 단일 진입점 — 02_RX_ble 동일 패턴 적용 완료(빌드 ✓, 실보드 △), 03 예정
- [[nrf52_module_naming]] — **nRF52 로컬 모듈 `eta_` 접두사 규칙**: `app_`은 nRF5 SDK 네임스페이스 → 충돌. `eta_`로 근본 제거(`b92835c`, ✓실보드). 02_RX_ble 적용·03 후보·01 해당 없음
- [[nrf52_firmware_conventions]] — **nRF52 코딩 관습**(b92835c→e85839c 확정): ISR printf 금지(HardFault 실증)·오류 카운터 패턴(1초 윈도우 append)·init/배너 printf 금지·NRF_LOG 초기화 잔재(호출 0건) 인지
- [[ses_build_conventions]] — SES `.emProject` 함정: ①파일 목록 하드코딩(와일드카드 없음) ②nRF5 SDK 헤더 충돌(→`eta_` 접두사로 해소·[[nrf52_module_naming]]) ③`ADD_SPI` 전역 전파 주의 ④`<folder>` 는 가상 그룹·빌드 무영향
- [[gpio_verification_pinmap]] — 검증 핀맵: 기능 → 프로브 핀 → 기대값 (SPI CS PB12·PWM PC6~9·ESB P0.17/18·ADC). planner가 검증 경로에 인용. 미확인 핀은 "확인 필요"로 호명
- [[nfc_pins_gpio]] — nRF52 P0.09(LED1)·P0.10이 NFC 안테나 핀 기본 → `CONFIG_NFCT_PINS_AS_GPIOS`로 GPIO 전용화(UICR.NFCPINS=`0xFFFFFFFE`, 전원사이클 후 적용). LED1 cold-boot 미점등 진단·**active-HIGH 확정**(2026-06-18)
- [[시립대_전달]] — 시립대 전달 통합 문서: P1 핀맵(SPI/UART) · P2 구동 절차(전원 순서·LED·comm_st 케이스) · P3 GUI 사용법(연결·buck 지령·스크린샷)
- [[st_link_nrf52_flash]] — 3-MCU 플래싱 정본 (01 ST-Link V2 네이티브 / 02·03 nRF = 커스텀보드 + **J-Link V9.3 Plus SN69730359** 외부 SWD, **02·03 둘 다 flash 2026-06-15 실측 통과**). 프로브 식별 ShowEmuList 규율·DEVICEID 보드 식별 게이트(02=0x5FE168DA/03=0xE9775EC9)·JLink connect 트러블슈팅(VTref↔데이터선)·pyOCD 폴백 강등. 종전 J-Link OB SN1050329071·02 DK 오기록 정정

### Sources

- [[pc_uart_gui_verification_260612]] — PC UART GUI 실보드 검증 스크린샷 (2026-06-12, 3보드 COM17, TX Buck Set E2E `222.22V→22222`, 6패널 Physical 변환 실측). 원본 이미지 `raw/pc_uart_gui/`
- [[spi_10ms_diagnosis_report_260601]] — SPI 10ms 폴링 진단 보고서 (미달 반증·관측 도구 한계·✓ 확정, 2026-06-01)
- [[spi_debug_log_report_260529]] — 양방향 ESB 데이터 경로 검증 리포트 (시나리오 A/B, 2026-05-29)
- [[spi_heartbeat_report_260529]] — SPI heartbeat 작업 보고서 (heartbeat 200ms 실보드 검증, 10ms/9MHz 미달, 2026-05-29)
- [[rx_control_pwm_가이드]] — RX_control PWM 개발 가이드 (2026-04-14)
- [[uart_cmd_reference_테스트용]] — RX Control UART5 Command Reference (이미지 PDF, Ver 0.1E00). phase·start 추가 + dt 구문 변경 + UART5 핀 확인
- [[spi_protocol_manual_260513]] — OLED TV 프로토콜 매뉴얼 (2026-05-13). ESB wire 포맷(11B) 정의 문서
- [[prd]] — 시스템 PRD v1.0 (2026-05-26). 인수 시점 이해 스냅샷, 펌웨어 현황·미해결 의문점 일람
- [[schematic_stm32_mini_pro_v10]] — STM32 mini-pro v10 회로도 (이미지 PDF, SPI 수동 추출). STM32↔nRF52832 PCA10040 배선표 포함
- [[schematic_rx_regulator_control_board]] — Rx OLED Regulator Control Board 회로도 (OrCAD Design XML + PDF). MCU 전체 핀맵·39개 신호 인벤토리·TEMP swap 회로도 확인·OSC Clock(8MHz HSE 수동 크리스탈 X1+C2/C3+R10/R11, RCC_HSE_ON 함의). **⚠️ 실보드 HSE 발진 실패 — 현재 HSI 동작([[sysclk_hsi_transition]])**
- [[schematic_ble_module_board_v01e00]] — BLE Module Board Ver0.1E00 회로도 (02_RX_ble/03_TX_ble 공용 nRF52832 모듈). 커넥터 핀맵(CON1/CN1/CN2) 확정·전원 아키텍처 교정(PD3V3→필터→BLE_P3V3)·System Reset·안테나. raw PDF 사본 보유 (2026-06-05 재독)

---

## teams/g/bp-cc3351

### Concepts

- [[boosterpack_pinmap]] — P1/P2 2×20핀 전체 할당표 (SDIO/SPI/UART/IRQ/RESET/전원) + AM263P syscfg 대응표

### Sources

- [[bp_cc3351_evm_ug]] — TI BP-CC3351 EVM User Guide (SWAU132A, 23p). BoosterPack 2×20핀 핀맵·JTAG 헤더·전원·클럭 raw 추출 인덱스
- [[bp_cc3351_schematic]] — BP-CC3351 회로도 (MCU121 Rev A/B, 3장). P1/P2 핀맵·Reset 회로(Q1 BSS138)·전원(TPS7A8801RTR)·CC3351 IC 연결
- [[cc3351_datasheet]] — TI CC3350/CC3351 데이터시트 (SWRS284C Rev.C, 34p). 핀맵·전원·SPI/SDIO/UART 타이밍·레퍼런스 회로도

---

## teams/g/lp-am263p

### Living docs

- [roadmap.md](teams/g/lp-am263p/roadmap.md) — 프로젝트 로드맵(목표·작업 호 인덱스·현재 위치). 단계 spine은 작업 로드맵 위임
- [roadmaps/porting.md](teams/g/lp-am263p/roadmaps/porting.md) — `porting` 작업 호(S0~S8 단계 spine·완료 기준 표·현재 S6 막힘(NP 코어 미실행, R38)·남은 일정). 디테일은 concept 백링크
- [status.md](teams/g/lp-am263p/status.md) — 기능별 구현 현황표·다음 시작점 (파이프라인이 커밋마다 갱신)

### Concepts

- [[team_briefing]] — **팀 업무보고 참고 자료(lp-am263p)**: 주차별 보고 스냅샷 이력(6/2·6/9 diff)·로드맵·S6 현재 위치(R35~R38 원인 좁힘, R39 예정)·비유표. 보고 직전 열어서 참고
- [[flash_open_facts]] — **S3→S6 블로커 사실 원장**: 확정 사실 + 폐기 가설(재시도 금지) + 현재 최유력 가설(NP 코어 미실행·1순위 XTAL). S3/S4 해소는 history 보존, 현재 블로커 S6. 라운드마다 제자리 수정 (맥락유실 방지 핵심)
- [[flash_open_diagnostic_log]] — **진단 라운드 로그** (append-only): R7~R38 가설→변경→관찰→결론. S3 블로커(R7~R28b 해소)부터 S6 블로커(R32~R38, NP 코어 미실행·1순위 XTAL)까지 시간순 history
- [[xspi_dummy_cycles]] — IS25LX256 Octal DDR(8D-8D-8D) dummy cycle vs 클럭 주파수 표 + 자주 쓰는 값 (16.67/33.33/50/100/133 MHz)
- [[is25lx256_vs_spansion_quirks]] — bp-3351→AM263P 포팅 시 Spansion 분기 제거 체크리스트 (UNHYSA 부재, RDAR/WRAR 부재, set888mode=0x81 정정, AM243 Quad/AM263P Octal 라인 차이)
- [[flash_open_sequence]] — `Flash_norOspiOpen` 단계별 시퀀스 + 종료 시 OSPI 컨트롤러/chip 상태 표
- [[sbl_app_flash_handoff]] — `skipHwInit` 게이트, SBL → 앱 핸드오프 시 정합성 깨지는 지점·flashFixUpOspiBoot 비대칭·진단 절차
- [[am263p_mcspi_controller]] — AM263P MCSPI(13.1.3) 환원: CS 프레이밍·EDMA·클록. S6 `SPI not responsive` 디버그용 (TRM demand-ingest 예시)
- [[am263p_adc_instance_allocation]] — **AM263P ADC 인스턴스/채널 배치 설계 규칙 정본**: 멀티 인스턴스는 표준(비안정 아님). 각 인스턴스=독립 SAR(자체 S/H·시퀀서·결과레지스터·ADCINT). 한 인스턴스 다중 SOC=직렬(스큐+변환시간합 예산, 마지막 EOC coherent read), 다른 인스턴스=병렬(동시 샘플). 상관·고속(V·I 쌍·전류)은 인스턴스 분산+공통 트리거, 무상관·저속(온도)은 한 인스턴스에 몰아 ISR 절약. 인스턴스↑=+ISR/+int_xbar/+flag 비용. 유일한 실제 instability=변환시간합>트리거주기(overflow). △미검증: 변환시간 예산 수치·동시성 실측
- [[am263p_syscfg_soft_vs_hard_assign]] — **AM263P SysConfig 논리명≠물리 페리페럴 함정 정본**: 물리 배정이 soft(`$suggestSolution`)면 새 인스턴스 addInstance 시 솔버가 기존 배정까지 reshuffle → ADC AIN은 물리 1:1 고정이라 **엉뚱한 핀을 읽음**(ISR·변환 정상인데 인가전압 미추종 = 가장 헷갈리는 함정). 수정=hard `ADC.$assign="ADCn"`(✓실보드 검증). int_xbar·base·AIN은 물리 기준. 모든 보드배선 고정 페리페럴 일반화. UART5는 soft 재배치 아님 확정(원인=UART_write 주석+RS-485). AIN 핀까지 hard 승격으로 리스크 닫음(✓ 6채널 c512e3b)
- [[am263p_adc_rti_trigger]] — **AM263P ADC 브링업 정본**: RTI 타이머→ADC SOC 트리거 결선 함정(SysConfig `enableIntr0` 미설정 시 INT0 export 게이트 차단) + JTAG/RAM 레지스터 검증 측정 시점 함정(reset 없이 read=전부 0 오진) + 검증된 설계 패턴(RTI 트리거+EOC ISR-flag, 1 kSPS). 레퍼런스 `adc_soc_rti`. 8kw 실측 환원 (2026-06-05)
- [[am263p_epwm_module_sync_deadtime]] — **AM263P EPWM 모듈간 SYNC 상보·dead-time 정본**: 풀브리지 레그의 HS/LS가 다른 EPWM 모듈에 걸치면 모듈 dead-band 못 씀 → **더미 EPWM0 fan-out**(전 출력 모듈 1-hop) + **비대칭 AQ + 2-compare isoform**(HS: CMPA=TBPRD/2+DT / LS: CMPA=TBPRD/2−DT). dead-band 레그와 ns 소스(`ETA_DEADTIME_NS`) 공유 — 메커니즘 둘·소스 하나. 8kw 레그2 실측: 비대칭 ~22 ns→**±2 ns**, 4-DT sweep 전 항목 PASS(`4014901`)
- [[am263p_epwm_sync_topology]] — **AM263P EPWM SYNC 토폴로지·지연 모델 정본**: SYNC는 모듈별 독립 MUX(fan-out), 데이지체인 아님. `EPWMSYNCINSEL`로 공용 SYNCOUT 풀(Table 7-154)에서 소스 1개 선택. source→target **hop당 지연 고정**(`TBCLK==EPWMCLK`면 2×EPWMCLK, else 1×TBCLK)·**target 인덱스 무관·누적 없음**. ⟹ 한 소스를 여러 모듈이 fan-out 선택하면 상호 정수클록 스큐 0. 8kw ~11ns 비대칭 = master 0-hop vs slave 1-hop. **더미 EPWM0 fan-out으로 비대칭 ~22 ns→±2 ns 검증완료**(`4014901`)
- [[am263p_epwm_primary_pad_no_force_io]] — **AM263P EPWM primary 패드는 force_io 불필요 정본**: 출력이 핀 primary(Mode0) function이면 SysConfig 핀먹스만으로 출력 버퍼 켜짐 — KICK+PADCONFIG OE RMW 불요. force는 alt-function 패드(UART5=EPWM15)만. force_io 정본과 대조 짝. 근거=8kw PWM Pin1 EPWM2_A@J4.39 실측(100kHz/50%, force 없이). + OCRAM/ccs-debug+Saleae 검증법
- [[am263p_iomux_force_io_enable]] — **AM263P IOMUX PADCONFIG force_io_enable 정본**: SysConfig 핀먹스만으론 alt-function 패드 입·출력 버퍼가 안 켜짐(OE/IE override `00` + `Pinmux_config` plain-write). KICK 언락 후 PADCONFIG RMW로 `PIN_FORCE_OUTPUT_ENABLE(0x40)`/`PIN_FORCE_INPUT_ENABLE(0x10)` OR-set 필수. ★OE/IE active-low 아님(set=enable). UART5(EPWM15_A/B) 사례 발견·전 alt-function 패드 일반화. 8kw UART5 미동작 = 펌웨어 IOMUX 원인 아님(THVD1400 U13은 8kw 보드 부품·LP 아님 / LP-측 후보=UART/EPWM 먹스 [[lp_am263p_uart_epwm_mux]])
- [[lp_am263p_uart_epwm_mux]] — **LP-AM263P UART/EPWM 부스터팩 먹스 사실**: UART5_TXD/RXD는 온보드 U54(SN74CB3Q3257) FET 버스스위치로 EPWM9와 다중화돼 BP 헤더로 나감. 먹스 SEL/EN은 TCA6416 IO expander(U63, I2C1 @0x20, P00/P14)가 구동 — GPIO 아님, 풀 없음. 펌웨어가 expander 설정 전엔 먹스 미정 → UART5 헤더 미출력 가능. SoC 핀먹스([[am263p_iomux_force_io_enable]])와 별개 보드-레벨 게이트. ★8kw UART5 미동작 LP-측 제3 후보(가설). 회로도 PROC171A ingest 산출
- [[jtag_flash_harness]] — **JTAG flash 굽기 정본(flash-time 층위)**: ① runAsynch Node.js 하네스(DSS Rhino GEL_RunF는 R5 free-run+TCM read 0x400000으로 깨짐) ② 클린 호스트(IDE 종료) ③ 연속 시도 사이 파워 사이클(IDLE→never BUSY/300s timeout 해소) ④ standalone 부팅 banner 검증. flashwriter 내부(gCmd 0x70038000)·boot 프로파일·하네스 위치 (2026-06-05 8kw 실측). **§7(2026-06-12): 굽기는 OSPI(4S)=`1,1,1,1`에서도 성공 — DevBoot 필수 아닌 편의, `loadProgram` soft-reset로 돌던 app서 코어 인수**
- [[toggle_free_flash_loop]] — **토글-프리 dead-time 반복 루프(board-common)**: SW1 토글 없이 빌드→flash→전원사이클 루프가 서는가. **굽기 ✓ + 부팅 ✓ 양쪽 확정(2026-06-12)** — 단, ②(부팅)은 올바른 스트랩 SW1=`0,0,1,1`(xSPI 8D SFDP)에서. 종전 `1,1,1,1`(4S)에서의 `'C'` ping은 부트모드 스트랩 미스매치였음(octal-only 칩, 정본 [[ospi_boot_mode_strap]]). §③: 반복 사이 reset은 진짜 VCC 차단 필수(>128Mb flash warm-reset 4-byte stuck, full POR만 해소, TRM §5.4.1:530)

### Sources

- [[is25lx256_datasheet]] — ISSI IS25LX/WX 256/128Mb xSPI Flash 데이터시트 (Rev. A14, 챕터별 raw 추출 인덱스)
- [[mcupsdk_flash_nor_ospi]] — TI MCU+ SDK `flash_nor_ospi.c` (NOR OSPI 공용 드라이버), 라인 인덱스 + 파생 페이지 링크
- [[am263p_trm]] — AM263P Technical Reference Manual (1725쪽, 26챕터 raw 추출 + Grep 탐색 가이드). RAG MCP 대체
- [[lp_am263p_ug]] — LP-AM263P LaunchPad User Guide (60쪽 전체 ingest: 핀맵·부트모드·핀먹스·OSPI 배선·보드 함정)
- [[schematic_lp_am263p]] — LP-AM263P 회로도 (TI PROC171A, SPRR503A). Tier 2 선택적 ingest — Altium 소스 바이너리라 PDF 텍스트레이어 추출. UART5 먹스 블록 산출, RS-485 부재 확인. raw `proc171_schematic/`

---

## teams/g/8kw-ev-wpt-tx

### Living docs

- [roadmap.md](teams/g/8kw-ev-wpt-tx/roadmap.md) — 프로젝트 로드맵(목표·작업 호 인덱스·현재 위치)
- [roadmaps/adc.md](teams/g/8kw-ev-wpt-tx/roadmaps/adc.md) — `adc` 작업 호(A0~A4). eta 보드 J3 6채널 ADC 브링업, 신호별 스케일링 포함. A2 ✓ 6채널 실보드 검증(2026-06-09 c512e3b). 다음 A3 스케일링(스펙 대기)
- [roadmaps/pwm.md](teams/g/8kw-ev-wpt-tx/roadmaps/pwm.md) — `pwm` 작업 호(P0~P4). EPWM 전력제어. 풀브리지 4채널(레그1=EPWM2, 레그2=EPWM4+7 두 모듈), dead-time 100~400ns build-per-change(실험후 고정), 주파수 85kHz 고정, P4서 ADC 트리거 RTI→PWM 전환. **P1 ✓ 4/4**(HS1/LS1/HS2/LS2 실측·shoot-through 0, `6e6b342`) **+ P2 완전 완료**(단일소스 `8046744`, 85kHz `d01fc0a`, **EPWM0 fan-out + isoform `4014901` — 비대칭 ~22ns→±2ns, 4-DT sweep 100/150/250/400ns 전 항목 PASS**). 다음 P3 보호
- [status.md](teams/g/8kw-ev-wpt-tx/status.md) — 기능별 구현 현황표·다음 시작점 (파이프라인이 커밋마다 갱신)

### Concepts

- [[adc_scaling]] — **8kW WPT TX ADC 물리량 변환식 모음**: GUI `PHYSICAL_COEFF` 단일소스·callable 비선형 확장(NTC), **5채널 완료**(Temp×2 NTC Beta·GA_Vin 저항분압·I_COIL_SEN CT버든·GA_Iin_SEN Hall-effect), I_LCC_SEN 미교정. 검증방법(직접전압 주입·LSB 흔들림). (2026-06-24)
- [[team_briefing_8kw]] — **팀 업무보고 참고 자료(8kw)**: 주차별 보고 스냅샷 이력·작업 호(A0~A4)·ADC 6채널 완료 현재 위치·만난 문제표(트리거 결선·soft 재셔플)·다음(A3 스펙 대기/UART5 복구). 보고 직전 참고
- [[build_methods]] — **두 가지 빌드 방법 진입 페이지**(2026-06-19): 방법1 개발자 CCS IDE 빌드(`Release/`) vs 방법2 HW 엔지니어 GUI gmake 빌드(`build/`, `gui.bat`→`launch_gui.ps1`→`gui.py`→`gmake -C build all`). 비교표(용도/진입점/빌드명령/산출물/플래시 소스) + 공통스택(CCS21/SDK_06, config.mk 3줄 이식) + syscfg 함정(`generated/` 커밋·gitignore 금지) + 새 .c 파일 양쪽(.cproject·FILES_common) 등록 + 플래시 공통(`run_flash_node_8kw.ps1 -Source release|build`, SW1=`0,0,1,1`)
- [[jtag_flash_clean_host]] — **운영 함정 2종**: ①AM263P OSPI JTAG 굽기는 CCS IDE 완전 종료 후(IDE 상주 DSLite 경합 → 비일관 실패, 2026-06-05 실측). ②"Run > Flash Project" **금지** — SBL 미포함, 전원사이클 후 standalone 부팅 불가(2026-06-16). 올바른 경로: `tools/ospi_flash/run.bat` (구 `tools/jtag_flash/`, 2026-06-17 rename)
- [[ospi_flash_tooling]] — **OSPI flash 툴링 메커니즘 정본**(2026-06-17): XDS110/JTAG → 헬퍼 펌웨어 RAM 로드 → AutoCmd(0x70038000) → IS25LX256 굽기(SBL@0x00·app@0x00081000). `--source release|build` argv 분기 + mtime fallback 자동 선택. DSLite 콜드스타트/경합 함정
- [[syscfg_build_model]] — **SysConfig 생성물 빌드 의존 모델**(2026-06-17): CCS managed build(`Release/`) vs 수제 gmake(`build/`) — 동일 `example.syscfg` 공유. gmake `SYSTEM_FLAG=true`(기본)=`build/generated/` 커밋본 사용·**gitignore 금지**. SysConfig 미사용 모듈 stub emit 함정. CCS vs gmake 바이너리 비동일(inert 심볼 차이, 기능 동일)
- [[sdk_ccs_toolchain_migration]] — **MCU+ SDK/CCS 툴체인 마이그레이션 함정 6종**(2026-06-18): ①SDK 릴리스노트·minToolVersion이 요구 툴체인 정본 ②imports.mak CGT 하드`=`·override는 include 이후 ③`export VAR ?=`가 config.mk보다 앞이면 config.mk 가림 ④CCS 번들 SysConfig=CLI전용·gmake는 standalone 필요 ⑤genimage 스크립트 리네임·정답은 SDK example makefile ⑥workspace 로드≠툴체인 마이그레이션
- [[uart5_rx_polled_1byte]] — **SDK 함정**: AM263Px `UART_read()` POLLED+NO_WAIT+FULL에서 `rx.count`가 앱 transaction에 미반영 → stale 0x00 버퍼 주입·SOF 탐색 불가. 수정: `count=1`·반환값 `==SystemP_SUCCESS` (2026-06-16 실보드 검증)
- [[uart5_packet_protocol]] — **UART5 텔레메트리 패킷 정본**(branch uart5 ba241fa·979699d, ✓실보드): 18B 고정 big-endian `[SOF=0xA5][LEN=12][TYPE=0x01][SEQ][raw u16×6][CRC-16/CCITT-FALSE]`, CRC 범위 byte[1..15]. RTI2 10Hz·115200/8N1 polled. thin device(raw만 wire)·smart host(mV=raw*3300/4095 미러). 채널 순서=ETA_ADC_CH enum, eta_packet.c 직렬화 자동 추종. SOF동기+CRC 1바이트 슬라이드 재동기. 선례 oled 대비 CRC-16·단일·단방향
- [[pc_monitor_gui]] — **host PC GUI**(`tools/gui/gui.py`, `785b848`, 2026-06-12): ADC 텔레메트리 모니터(18B 수신·6ch 표·플롯·CSV) + **dead-time 빌드/플래시 컨트롤**(Spinbox→write→build→flash, headless CLI `--deadtime N --build --flash`). 백로그 7항목(상태배너·경로박스·안내문·배포형태·폭축소·버튼이동·채널명굵게) 포함
- [[ospi_boot_mode_strap]] — **OSPI standalone 무부팅 해소 정본(8kw, 2026-06-12)**: 진짜 원인 = 부트모드 핀 스트랩 미스매치. 보드 flash IS25LX256는 **octal-only**(quad/`0x6B`/QE 물리적 부재) → SW1=`1,1,1,1`(4S Quad)에서 ROM `0x6B`+QE 기대 미충족 → `'C'` ping. **SW1=`0,0,1,1`(xSPI 8D SFDP)로 교정 → VCC 전원사이클 후 완전 부팅 실측**(SBL→app→`eta-tx: 8kw-ev-wpt start`). 종전 "flash 프로그래밍/cell/QE" 블로커 가설 전부 무효. TRM Table 5-1/5-2·UG Table 2-5·IS25LX256 cross-link
- [[ospi_boot_console_diagnostic]] — **OSPI 부팅 진단 정본(8kw, 2026-06-12)**: COM4=UART0 콘솔(XDS110, VCC 독립)·boot stage triage recipe(banner별 ROM/SBL/app 가름)·SBL provenance 확정(byte-identical SDK 프리빌트)·route② mcelf standalone 부팅 실증(2026-06-12). **§3 갱신: 잔여 블로커였던 flash 프로그래밍/QE bit 가설은 무효 → 진짜 원인 부트모드 스트랩([[ospi_boot_mode_strap]])**

### Entities

- [[pwm_pinmap]] — LP-AM263P EPWM → 8kw 게이트 신호 핀맵 (풀브리지 4채널, **4핀 확정·실측 2026-06-09**). 레그1=EPWM2(HS1 J4.39/LS1 J4.40), 레그2=EPWM4(HS2 J6.52)+EPWM7(LS2 **J6.51=EPWM7_B 확정**) **두 모듈 → EPWM0 fan-out + isoform**. ⚠️ **회로도 net 라벨("EPWM4_B"/"EPWM7_A")과 silicon 채널(EPWM4_A/EPWM7_B) suffix 반대** — 펌웨어 정본=silicon 채널(UG Mode0·pinmux.csv F1 교차확인). dead-time 비대칭 **±2 ns**(`4014901`)
- [[adc_pinmap]] — eta 보드 J3 커넥터 → ADC 인스턴스/SOC/채널/int_xbar/IRQ → 신호 대응표 (6채널: 온도×2, 전압×1, 전류×3, 6/6 구현·실보드 검증, 5 인스턴스, AIN hard assign). 스케일링 스펙 미확인 항목 포함

### Sources

- [[pwm_leg2_isoform_report]] — PWM 레그2 dead-time 정밀화 + 레그1 동형화 검증 리포트 (branch pwm-deadtime, commit 4014901, 2026-06-11). EPWM0 fan-out + isoform. 4-DT sweep(100/150/250/400 ns) 전 항목 PASS. 원본 데이터 `raw/pwm_leg2_isoform/`
- [[pwm_deadtime_knob_verify]] — `ETA_DEADTIME_NS` knob flash+boot silicon 검증 리포트 (v1_0e00, 2026-06-12). 100/150/250/400 ns 4점 16/16 PASS(≤2 ns, shoot-through 0). production 150 ns 확정. 원본 데이터 `raw/pwm_deadtime_knob_verify/`

### Weekly Reports

- [weekly_report_2026-06-09_16.md](teams/g/8kw-ev-wpt-tx/weekly_report_2026-06-09_16.md) — 주간 업무 보고 2026-06-09~16: PWM 전력제어 브링업(85kHz·dead-time 150ns 확정·EPWM0 fan-out·4-DT sweep PASS) + PC↔MCU UART 통신·GPIO 양방향 제어 완료
- [weekly_report_2026-06-17_23.md](teams/g/8kw-ev-wpt-tx/weekly_report_2026-06-17_23.md) — 주간 업무 보고 2026-06-17~23: 툴체인 신스택 전환 완전 완료(CCS21/SDK_06, end-to-end PASS) + 새 테스트 머신 fresh-clone 검증 완료 + ADC A3 물리량 변환 착수(I_COIL_SEN·GA_Iin_SEN·GA_Vin 3채널)
