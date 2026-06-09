# wiki index

전체 페이지 카탈로그. 페이지 추가/갱신 시 여기에 등록한다.

---

## 공통 (모든 팀·프로젝트)

### Concepts

- [[schematic_ingest_strategy]] — 회로도를 비전 처리 없이 텍스트로 ingest하는 Tier별 전략 (EDA export → CSV/netlist)

### Reference

- [[instruments]] — 회사 공통 계측 장비 + 프로그래밍/디버그 프로브 인벤토리 (Keysight MSOX3104T·Saleae Logic Pro 16 / ST-Link V2·J-Link OB SN1050329071·SAM-ICE SN24012600). planner가 검증 경로에 인용

---

## teams/c/oled_tv_software

### Living docs

- [roadmap.md](teams/c/oled_tv_software/roadmap.md) — 전체 로드맵(M0~M6 마일스톤 호·M3 ✓·현재 M4 SPI 9MHz 막힘·PRD 지연 목표 게이트). 전략 spine, 현재 위치는 status 위임
- [roadmaps/pc-gui.md](teams/c/oled_tv_software/roadmaps/pc-gui.md) — `pc-gui` 작업 호(G0~G3, 아이디어·미착수). UART 패킷 모니터링 + buck 설정 호스트 툴. G0 포트 조합 결정 선행
- [roadmaps/spi-esb-refactor.md](teams/c/oled_tv_software/roadmaps/spi-esb-refactor.md) — `spi-esb-refactor` 작업 호(R1~R4, 코드 정리 4라운드). merge 목적 SPI·ESB 구조 정리
- [status.md](teams/c/oled_tv_software/status.md) — 기능별 구현 현황표·다음 시작점 (파이프라인이 커밋마다 갱신)

### Entities

- [[rx_control]] — STM32F103RCT6 보드, PWM 채널 매핑·BKIN 핀·SPI Master
- [[tim8]] — Advanced Timer, PWM1(CH1/CH2) + BKIN(PA6)
- [[tim3]] — General Timer, PWM2(CH3/CH4). BDTR 없음
- [[rx_ble_module]] — 02_RX_ble, nRF52832 ESB PRX. SPI Slave 9Mbps. BLE 시절 명칭 잔류
- [[tx_ble_module]] — 03_TX_ble, nRF52832 ESB PTX. LED(LED1 P0.09·LED2 P0.08=spi_comm_st mirror·LED3=ble_comm_st mirror, 기본 DK P0.19/회사 P0.06 매크로)·DK↔회사 보드 분기(custom_board.h). TX 보드 SPI 미구현

### Concepts

- [[pwm_system]] — TIM8/TIM3 64MHz·100kHz·120도 위상, `pwm_init`/`set_duty`/`pwm_set_freq`
- [[dead_time]] — SW CCR offset 방식. TIM3에 BDTR 없어 두 타이머 통일
- [[trip_zone]] — TIM8 BKIN(PA6) → `HAL_TIMEx_BreakCallback`로 PWM 전체 차단
- [[uart_command_set]] — `duty`/`freq`/`dt`/`phase`/`start`/`stop`/`reset`/`buck` (UART5, 115200/8N1, PC12/PD2). ISR 구동 수신·prefix 매칭 파싱
- [[buck_vout_ref_command_path]] — `buck <v>` = RF 링크 건너는 유일한 UART 지령. 01 UART5 → 0x51 DATA[6,7](volts×100) → 03 Monitor. 검증 `buck 123.34`→`12334`. 새 tx 지령 추가 패턴
- [[cubeide_newlib_nano_float]] — CubeIDE newlib-nano float 함정(`nanoprintffloat`/`nanoscanffloat`). scanf float 꺼지면 `buck 15.5` 소수 깨짐. 구성별 독립·Release 재확인
- [[adc_channel_map]] — ADC1 6채널 핀맵(PA0~PA3, PC4/PC5) + TEMP1/TEMP2 라벨 swap 함정 + 평가보드 시험 가이드
- [[spi_packet_format]] — STM32-nRF 내부 SPI wire 포맷 (11B 고정, HDR 0x10~0x12/0x50~0x52). ESB와 동일 패킷 구조
- [[esb_packet_format]] — ESB wire 포맷 (11B, HDR round-robin 0x10-0x12/0x50-0x52, `ESB_TX_INTERVAL_MS=1ms`, ACK with payload, CRC-valid only 콜백)
- [[esb_link_layer]] — ESB 링크 파라미터 (`ESB_TX_INTERVAL_MS=1ms`, ACK with payload, NRF_ESB_MAX_PAYLOAD_LENGTH=64) + 미결 파라미터
- [[tx_to_rx_packets]] — TX→RX: 0x10 시스템상태 / 0x11 입력 Analog / 0x12 출력 Analog+온도
- [[rx_to_tx_packets]] — RX→TX (ESB ACK payload): 0x50 시스템상태 / 0x51 입력+Tx Vout Ref / 0x52 출력+온도 (코드 실측 레이아웃 + 불일치 추가)
- [[esb_ptx_ack_assembly]] — PTX 모드 ACK payload 재조립: g_last_ack_by_hdr[3] 패턴 + ISR printf 금지
- [[comm_state_monitoring]] — 0x10 Data[0] bit5/6은 tx_status 아닌 통신 링크 비트. SPI_Comm_St=200ms heartbeat(+CRC 통합 spi_status, ✓`e5e3efc`), BLE_Comm_St=ESB presence 리셋윈도우(02·03 각자 수신 delta, ✓`6cd7e6c`). 심볼 `COMM_ST_BIT_*`/`*_comm_st_*` 컨벤션·라벨 문자열 구분·**race-free stamp 교훈(상태비트는 송신복사본 spi_tx_pkt에)**
- [[spi_link_reliability]] — SPI heartbeat 구현(200ms 독립 타이머, P0.17 검증)·오류율 모니터·spi_tx_busy 타임아웃 복구·10ms 폴링 ✓ 검증 완료·9MHz 상향 미달
- [[gpio_verification_pinmap]] — 검증 핀맵: 기능 → 프로브 핀 → 기대값 (SPI CS PB12·PWM PC6~9·ESB P0.17/18·ADC). planner가 검증 경로에 인용. 미확인 핀은 "확인 필요"로 호명
- [[st_link_nrf52_flash]] — 3-MCU 플래싱 정본 (듀얼 프로브: 01 ST-Link 네이티브 / 03 J-Link OB / 02 DK 온보드). SN 고정 함정·CLI 실측·pyOCD 폴백 강등 (2026-06-05)

### Sources

- [[spi_10ms_diagnosis_report_260601]] — SPI 10ms 폴링 진단 보고서 (미달 반증·관측 도구 한계·✓ 확정, 2026-06-01)
- [[spi_debug_log_report_260529]] — 양방향 ESB 데이터 경로 검증 리포트 (시나리오 A/B, 2026-05-29)
- [[spi_heartbeat_report_260529]] — SPI heartbeat 작업 보고서 (heartbeat 200ms 실보드 검증, 10ms/9MHz 미달, 2026-05-29)
- [[rx_control_pwm_가이드]] — RX_control PWM 개발 가이드 (2026-04-14)
- [[uart_cmd_reference_테스트용]] — RX Control UART5 Command Reference (이미지 PDF, Ver 0.1E00). phase·start 추가 + dt 구문 변경 + UART5 핀 확인
- [[spi_protocol_manual_260513]] — OLED TV 프로토콜 매뉴얼 (2026-05-13). ESB wire 포맷(11B) 정의 문서
- [[prd]] — 시스템 PRD v1.0 (2026-05-26). 인수 시점 이해 스냅샷, 펌웨어 현황·미해결 의문점 일람
- [[schematic_stm32_mini_pro_v10]] — STM32 mini-pro v10 회로도 (이미지 PDF, SPI 수동 추출). STM32↔nRF52832 PCA10040 배선표 포함
- [[schematic_rx_regulator_control_board]] — Rx OLED Regulator Control Board 회로도 (OrCAD Design XML + PDF). MCU 전체 핀맵·39개 신호 인벤토리·TEMP swap 회로도 확인
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
- [roadmaps/porting.md](teams/g/lp-am263p/roadmaps/porting.md) — `porting` 작업 호(S0~S8 단계 spine·완료 기준 표·현재 S3 블로커·남은 일정). 디테일은 concept 백링크
- [status.md](teams/g/lp-am263p/status.md) — 기능별 구현 현황표·다음 시작점 (파이프라인이 커밋마다 갱신)

### Concepts

- [[team_briefing]] — **팀 업무보고 참고 자료**: 전체 로드맵·현재 위치·S3 블로커(비유 포함)·남은 사항. 보고 직전 열어서 참고
- [[flash_open_facts]] — **S3 블로커 사실 원장**: 확정 사실 + 폐기 가설(재시도 금지) + 현재 최유력 가설. 라운드마다 제자리 수정 (맥락유실 방지 핵심)
- [[flash_open_diagnostic_log]] — **S3 블로커 진단 라운드 로그** (append-only): R7~R27 가설→변경→관찰→결론 + R28 계획
- [[xspi_dummy_cycles]] — IS25LX256 Octal DDR(8D-8D-8D) dummy cycle vs 클럭 주파수 표 + 자주 쓰는 값 (16.67/33.33/50/100/133 MHz)
- [[is25lx256_vs_spansion_quirks]] — bp-3351→AM263P 포팅 시 Spansion 분기 제거 체크리스트 (UNHYSA 부재, RDAR/WRAR 부재, set888mode=0x81 정정, AM243 Quad/AM263P Octal 라인 차이)
- [[flash_open_sequence]] — `Flash_norOspiOpen` 단계별 시퀀스 + 종료 시 OSPI 컨트롤러/chip 상태 표
- [[sbl_app_flash_handoff]] — `skipHwInit` 게이트, SBL → 앱 핸드오프 시 정합성 깨지는 지점·flashFixUpOspiBoot 비대칭·진단 절차
- [[am263p_mcspi_controller]] — AM263P MCSPI(13.1.3) 환원: CS 프레이밍·EDMA·클록. S6 `SPI not responsive` 디버그용 (TRM demand-ingest 예시)
- [[am263p_adc_instance_allocation]] — **AM263P ADC 인스턴스/채널 배치 설계 규칙 정본**: 멀티 인스턴스는 표준(비안정 아님). 각 인스턴스=독립 SAR(자체 S/H·시퀀서·결과레지스터·ADCINT). 한 인스턴스 다중 SOC=직렬(스큐+변환시간합 예산, 마지막 EOC coherent read), 다른 인스턴스=병렬(동시 샘플). 상관·고속(V·I 쌍·전류)은 인스턴스 분산+공통 트리거, 무상관·저속(온도)은 한 인스턴스에 몰아 ISR 절약. 인스턴스↑=+ISR/+int_xbar/+flag 비용. 유일한 실제 instability=변환시간합>트리거주기(overflow). △미검증: 변환시간 예산 수치·동시성 실측
- [[am263p_syscfg_soft_vs_hard_assign]] — **AM263P SysConfig 논리명≠물리 페리페럴 함정 정본**: 물리 배정이 soft(`$suggestSolution`)면 새 인스턴스 addInstance 시 솔버가 기존 배정까지 reshuffle → ADC AIN은 물리 1:1 고정이라 **엉뚱한 핀을 읽음**(ISR·변환 정상인데 인가전압 미추종 = 가장 헷갈리는 함정). 수정=hard `ADC.$assign="ADCn"`(✓실보드 검증). int_xbar·base·AIN은 물리 기준. 모든 보드배선 고정 페리페럴 일반화. UART5는 soft 재배치 아님 확정(원인=UART_write 주석+RS-485). AIN 핀까지 hard 승격으로 리스크 닫음(✓ 6채널 c512e3b)
- [[am263p_adc_rti_trigger]] — **AM263P ADC 브링업 정본**: RTI 타이머→ADC SOC 트리거 결선 함정(SysConfig `enableIntr0` 미설정 시 INT0 export 게이트 차단) + JTAG/RAM 레지스터 검증 측정 시점 함정(reset 없이 read=전부 0 오진) + 검증된 설계 패턴(RTI 트리거+EOC ISR-flag, 1 kSPS). 레퍼런스 `adc_soc_rti`. 8kw 실측 환원 (2026-06-05)
- [[am263p_iomux_force_io_enable]] — **AM263P IOMUX PADCONFIG force_io_enable 정본**: SysConfig 핀먹스만으론 alt-function 패드 입·출력 버퍼가 안 켜짐(OE/IE override `00` + `Pinmux_config` plain-write). KICK 언락 후 PADCONFIG RMW로 `PIN_FORCE_OUTPUT_ENABLE(0x40)`/`PIN_FORCE_INPUT_ENABLE(0x10)` OR-set 필수. ★OE/IE active-low 아님(set=enable). UART5(EPWM15_A/B) 사례 발견·전 alt-function 패드 일반화. 8kw UART5 미동작 = 펌웨어 원인 아님(RS-485 트랜시버 의심)
- [[jtag_flash_harness]] — **JTAG flash 굽기 정본(flash-time 층위)**: ① runAsynch Node.js 하네스(DSS Rhino GEL_RunF는 R5 free-run+TCM read 0x400000으로 깨짐) ② 클린 호스트(IDE 종료) ③ 연속 시도 사이 파워 사이클(IDLE→never BUSY/300s timeout 해소) ④ standalone 부팅 banner 검증. flashwriter 내부(gCmd 0x70038000)·boot 프로파일·하네스 위치 (2026-06-05 8kw 실측)

### Sources

- [[is25lx256_datasheet]] — ISSI IS25LX/WX 256/128Mb xSPI Flash 데이터시트 (Rev. A14, 챕터별 raw 추출 인덱스)
- [[mcupsdk_flash_nor_ospi]] — TI MCU+ SDK `flash_nor_ospi.c` (NOR OSPI 공용 드라이버), 라인 인덱스 + 파생 페이지 링크
- [[am263p_trm]] — AM263P Technical Reference Manual (1725쪽, 26챕터 raw 추출 + Grep 탐색 가이드). RAG MCP 대체
- [[lp_am263p_ug]] — LP-AM263P LaunchPad User Guide (60쪽 전체 ingest: 핀맵·부트모드·핀먹스·OSPI 배선·보드 함정)

---

## teams/g/8kw-ev-wpt-tx

### Living docs

- [roadmap.md](teams/g/8kw-ev-wpt-tx/roadmap.md) — 프로젝트 로드맵(목표·작업 호 인덱스·현재 위치)
- [roadmaps/adc.md](teams/g/8kw-ev-wpt-tx/roadmaps/adc.md) — `adc` 작업 호(A0~A4). eta 보드 J3 6채널 ADC 브링업, 신호별 스케일링 포함. A2 ✓ 6채널 실보드 검증(2026-06-09 c512e3b). 다음 A3 스케일링(스펙 대기)
- [status.md](teams/g/8kw-ev-wpt-tx/status.md) — 기능별 구현 현황표·다음 시작점 (파이프라인이 커밋마다 갱신)

### Concepts

- [[jtag_flash_clean_host]] — **운영 함정**: AM263P OSPI JTAG 굽기는 CCS IDE를 완전히 내린 클린 호스트에서. host-driven 스크립팅(run.bat/flash_node.js, DSS Rhino) ↔ IDE 상주 cloudagent+DSLite 디버그 백엔드 경합 → 비일관 실패(펌웨어/보드 오인 위험). `getDebugSessions=[]`라도 프로세스 레벨 확인 (2026-06-05 실측)

### Entities

- [[adc_pinmap]] — eta 보드 J3 커넥터 → ADC 인스턴스/SOC/채널/int_xbar/IRQ → 신호 대응표 (6채널: 온도×2, 전압×1, 전류×3, 6/6 구현·실보드 검증, 5 인스턴스, AIN hard assign). 스케일링 스펙 미확인 항목 포함
