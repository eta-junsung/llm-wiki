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
- [[rx_ble_module]] — Rx 무선모듈 (BLE 시절, 02_RX_esb로 교체 예정). SPI Slave 9Mbps

### Concepts

- [[pwm_system]] — TIM8/TIM3 64MHz·100kHz·120도 위상, `pwm_init`/`set_duty`/`pwm_set_freq`
- [[dead_time]] — SW CCR offset 방식. TIM3에 BDTR 없어 두 타이머 통일
- [[trip_zone]] — TIM8 BKIN(PA6) → `HAL_TIMEx_BreakCallback`로 PWM 전체 차단
- [[uart_command_set]] — `duty`/`freq`/`dt`/`reset` (115200bps)
- [[spi_packet_format]] — Rx ↔ 무선모듈 SPI 11-byte 패킷 (HDR+Len+Data[8]+CRC), 10ms cyclic
- [[tx_to_rx_packets]] — 0x10 시스템상태 / 0x11 입력 Analog / 0x12 출력 Analog+온도
- [[rx_to_tx_packets]] — 0x50 시스템상태 / 0x51 입력 Analog+Tx Vout Ref / 0x52 출력+온도
- [[comm_state_monitoring]] — SPI_Comm_St 200ms 토글, BLE_Comm_St 페어링 상태

### Sources

- [[rx_control_pwm_가이드]] — RX_control PWM 개발 가이드 (2026-04-14)
- [[spi_protocol_manual_260513]] — OLED TV SPI 프로토콜 매뉴얼 (2026-05-13, BLE 시절)
