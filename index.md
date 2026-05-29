# wiki index

전체 페이지 카탈로그. 페이지 추가/갱신 시 여기에 등록한다.

---

## 공통 (모든 팀·프로젝트)

### Concepts

- [[schematic_ingest_strategy]] — 회로도를 비전 처리 없이 텍스트로 ingest하는 Tier별 전략 (EDA export → CSV/netlist)

---

## teams/c/oled_tv_software

### Entities

- [[rx_control]] — STM32F103RCT6 보드, PWM 채널 매핑·BKIN 핀·SPI Master
- [[tim8]] — Advanced Timer, PWM1(CH1/CH2) + BKIN(PA6)
- [[tim3]] — General Timer, PWM2(CH3/CH4). BDTR 없음
- [[rx_ble_module]] — 02_RX_ble, nRF52832 ESB PRX. SPI Slave 9Mbps. BLE 시절 명칭 잔류
- [[tx_ble_module]] — 03_TX_ble, nRF52832 ESB PTX. TX 보드 SPI 미구현

### Concepts

- [[pwm_system]] — TIM8/TIM3 64MHz·100kHz·120도 위상, `pwm_init`/`set_duty`/`pwm_set_freq`
- [[dead_time]] — SW CCR offset 방식. TIM3에 BDTR 없어 두 타이머 통일
- [[trip_zone]] — TIM8 BKIN(PA6) → `HAL_TIMEx_BreakCallback`로 PWM 전체 차단
- [[uart_command_set]] — `duty`/`freq`/`dt`/`phase`/`start`/`reset` (UART5, 115200/8N1, PC12/PD2)
- [[adc_channel_map]] — ADC1 6채널 핀맵(PA0~PA3, PC4/PC5) + TEMP1/TEMP2 라벨 swap 함정 + 평가보드 시험 가이드
- [[spi_packet_format]] — STM32-nRF 내부 SPI wire 포맷 (11B 고정, HDR 0x10~0x12/0x50~0x52). ESB와 동일 패킷 구조
- [[esb_packet_format]] — ESB wire 포맷 (11B, HDR round-robin 0x10-0x12/0x50-0x52, 10ms, ACK with payload)
- [[esb_link_layer]] — ESB 링크 파라미터 (10ms, ACK with payload, NRF_ESB_MAX_PAYLOAD_LENGTH=64) + 미결 파라미터
- [[tx_to_rx_packets]] — TX→RX: 0x10 시스템상태 / 0x11 입력 Analog / 0x12 출력 Analog+온도
- [[rx_to_tx_packets]] — RX→TX (ESB ACK payload): 0x50 시스템상태 / 0x51 입력+Tx Vout Ref / 0x52 출력+온도 (코드 실측 레이아웃 + 불일치 추가)
- [[esb_ptx_ack_assembly]] — PTX 모드 ACK payload 재조립: g_last_ack_by_hdr[3] 패턴 + ISR printf 금지
- [[comm_state_monitoring]] — SPI_Comm_St 200ms 토글, BLE_Comm_St 페어링 상태
- [[spi_link_reliability]] — SPI heartbeat 구현(200ms 독립 타이머, P0.17 검증)·오류율 모니터·spi_tx_busy 타임아웃 복구·10ms/9MHz 미달 현황

### Sources

- [[spi_debug_log_report_260529]] — 양방향 ESB 데이터 경로 검증 리포트 (시나리오 A/B, 2026-05-29)
- [[spi_heartbeat_report_260529]] — SPI heartbeat 작업 보고서 (heartbeat 200ms 실보드 검증, 10ms/9MHz 미달, 2026-05-29)
- [[rx_control_pwm_가이드]] — RX_control PWM 개발 가이드 (2026-04-14)
- [[uart_cmd_reference_테스트용]] — RX Control UART5 Command Reference (이미지 PDF, Ver 0.1E00). phase·start 추가 + dt 구문 변경 + UART5 핀 확인
- [[spi_protocol_manual_260513]] — OLED TV 프로토콜 매뉴얼 (2026-05-13). ESB wire 포맷(11B) 정의 문서
- [[prd]] — 시스템 PRD v1.0 (2026-05-26). 인수 시점 이해 스냅샷, 펌웨어 현황·미해결 의문점 일람
- [[schematic_stm32_mini_pro_v10]] — STM32 mini-pro v10 회로도 (이미지 PDF, SPI 수동 추출). STM32↔nRF52832 PCA10040 배선표 포함
- [[schematic_rx_regulator_control_board]] — Rx OLED Regulator Control Board 회로도 (OrCAD Design XML + PDF). MCU 전체 핀맵·39개 신호 인벤토리·TEMP swap 회로도 확인

---

## teams/g/bp-cc3351

### Sources

- [[bp_cc3351_evm_ug]] — TI BP-CC3351 EVM User Guide (SWAU132A, 23p). BoosterPack 2×20핀 핀맵·JTAG 헤더·전원·클럭 raw 추출 인덱스
- [[cc3351_datasheet]] — TI CC3350/CC3351 데이터시트 (SWRS284C Rev.C, 34p). 핀맵·전원·SPI/SDIO/UART 타이밍·레퍼런스 회로도

---

## teams/g/lp-am263p

### Living docs

- [roadmap.md](teams/g/lp-am263p/roadmap.md) — 포팅 전체 로드맵(S0~S8 단계·현재 S3 블로커·남은 일정). 전략 spine, 디테일은 concept 백링크
- [status.md](teams/g/lp-am263p/status.md) — 기능별 구현 현황표·다음 시작점 (파이프라인이 커밋마다 갱신)

### Concepts

- [[xspi_dummy_cycles]] — IS25LX256 Octal DDR(8D-8D-8D) dummy cycle vs 클럭 주파수 표 + 자주 쓰는 값 (16.67/33.33/50/100/133 MHz)
- [[is25lx256_vs_spansion_quirks]] — bp-3351→AM263P 포팅 시 Spansion 분기 제거 체크리스트 (UNHYSA 부재, RDAR/WRAR 부재, 레지스터 주소 맵 차이)
- [[flash_open_sequence]] — `Flash_norOspiOpen` 단계별 시퀀스 + 종료 시 OSPI 컨트롤러/chip 상태 표
- [[sbl_app_flash_handoff]] — `skipHwInit` 게이트, SBL → 앱 핸드오프 시 정합성 깨지는 지점·진단 절차

### Sources

- [[is25lx256_datasheet]] — ISSI IS25LX/WX 256/128Mb xSPI Flash 데이터시트 (Rev. A14, 챕터별 raw 추출 인덱스)
- [[mcupsdk_flash_nor_ospi]] — TI MCU+ SDK `flash_nor_ospi.c` (NOR OSPI 공용 드라이버), 라인 인덱스 + 파생 페이지 링크
