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
- [[spi_packet_format]] — STM32-nRF 내부 SPI 프레임 (56B/45B, HDR 0xC0, 20ms). ESB wire 포맷과 별개
- [[esb_packet_format]] — ESB wire 포맷 (11B, HDR round-robin 0x10-0x12/0x50-0x52, 10ms, ACK with payload)
- [[esb_link_layer]] — ESB 링크 파라미터 (10ms, ACK with payload, NRF_ESB_MAX_PAYLOAD_LENGTH=64) + 미결 파라미터
- [[tx_to_rx_packets]] — TX→RX: 0x10 시스템상태 / 0x11 입력 Analog / 0x12 출력 Analog+온도
- [[rx_to_tx_packets]] — RX→TX (ESB ACK payload): 0x50 시스템상태 / 0x51 입력+Tx Vout Ref / 0x52 출력+온도
- [[comm_state_monitoring]] — SPI_Comm_St 200ms 토글, BLE_Comm_St 페어링 상태

### Sources

- [[rx_control_pwm_가이드]] — RX_control PWM 개발 가이드 (2026-04-14)
- [[uart_cmd_reference_테스트용]] — RX Control UART5 Command Reference (이미지 PDF, Ver 0.1E00). phase·start 추가 + dt 구문 변경 + UART5 핀 확인
- [[spi_protocol_manual_260513]] — OLED TV 프로토콜 매뉴얼 (2026-05-13). ESB wire 포맷(11B) 정의 문서
- [[prd]] — 시스템 PRD v1.0 (2026-05-26). 인수 시점 이해 스냅샷, 펌웨어 현황·미해결 의문점 일람
- [[schematic_stm32_mini_pro_v10]] — STM32 mini-pro v10 회로도 (이미지 PDF, SPI 수동 추출). STM32↔nRF52832 PCA10040 배선표 포함

---

## teams/g/bp-cc3351

### Sources

- [[bp_cc3351_evm_ug]] — TI BP-CC3351 EVM User Guide (SWAU132A, 23p). BoosterPack 2×20핀 핀맵·JTAG 헤더·전원·클럭 raw 추출 인덱스
- [[cc3351_datasheet]] — TI CC3350/CC3351 데이터시트 (SWRS284C Rev.C, 34p). 핀맵·전원·SPI/SDIO/UART 타이밍·레퍼런스 회로도

---

## teams/g/lp-am263p

### Concepts

- [[xspi_dummy_cycles]] — IS25LX256 Octal DDR(8D-8D-8D) dummy cycle vs 클럭 주파수 표 + 자주 쓰는 값 (16.67/33.33/50/100/133 MHz)
- [[is25lx256_vs_spansion_quirks]] — bp-3351→AM263P 포팅 시 Spansion 분기 제거 체크리스트 (UNHYSA 부재, RDAR/WRAR 부재, 레지스터 주소 맵 차이)
- [[flash_open_sequence]] — `Flash_norOspiOpen` 단계별 시퀀스 + 종료 시 OSPI 컨트롤러/chip 상태 표
- [[sbl_app_flash_handoff]] — `skipHwInit` 게이트, SBL → 앱 핸드오프 시 정합성 깨지는 지점·진단 절차

### Sources

- [[is25lx256_datasheet]] — ISSI IS25LX/WX 256/128Mb xSPI Flash 데이터시트 (Rev. A14, 챕터별 raw 추출 인덱스)
- [[mcupsdk_flash_nor_ospi]] — TI MCU+ SDK `flash_nor_ospi.c` (NOR OSPI 공용 드라이버), 라인 인덱스 + 파생 페이지 링크
