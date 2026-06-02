---
date: 2026-06-02
---

# oled_tv_software — 구현 현황

## 다음 시작점

**03_TX_ble → BLE Module Board (nRF52832) ST-LINK V2 플래싱**

1. CON1(SWD, 2.5mm 5핀) 실물 Pin1 마킹 확인 → ST-LINK V2 배선 (SWDIO·SWDCLK·GND·nRST)
2. OpenOCD 또는 pyOCD 설치 확인 (`openocd --version` / `pyocd --version`)
3. 03_TX_ble SES 빌드 → .hex 생성
4. 플래싱 명령:
   - OpenOCD: `openocd -f interface/stlink.cfg -f target/nrf52.cfg -c "program <파일>.hex verify reset exit"`
   - pyOCD: `pyocd flash --target nrf52832 <파일>.hex`
5. CON2(절연 UART 4핀, MOLEX 22-05-7045) → PC 연결, UART 모니터 출력 확인

참고: [[schematic_ble_module_board_v01e00]] — CON1(SWD), CON2(UART) 커넥터 상세. nrfjprog는 J-Link 전용이라 사용 불가.

---

코드 정리 4개 라운드 (플래싱 검증 후): ① 모니터 1-헤더-1-줄 압축, ② 공유 출력 함수(`oled_tv_protocol.c` 신설, 3 빌드 등록), ③ serialize/deserialize 통합, ④ `SPI_PKT_*` → 링크 중립 이름 개명.

## 구현 현황

### SPI 통신 — STM32(01_RX_control) ↔ nRF52832(02_RX_ble)

| 기능 | 상태 | 메모 |
|------|------|------|
| heartbeat 메커니즘 (3-MCU) | ✓ | RX_ble가 0x10 STATUS bit5(`TX_STATUS_BIT_SPI_COMM_ST`) 토글 → STM32 5s 타임아웃(`SPI_HB_TIMEOUT_MS`)으로 SPI 단절 감지. 오실로 200ms 토글 확인(`P3NOFO01.PNG`, Δt≈190ms) |
| heartbeat 200ms 독립 타이머 | ✓ | `Heartbeat_Loop()` millis 게이트로 분리, SPI 사이클 종속 제거. 오실로 검증 완료 |
| SPI 오류율 모니터 (ok/fail/err%) | △ | `spi_ok_cnt/spi_crc_fail_cnt` 누적+delta UART 출력(`spi | ok=… | /s ok=100 crcfail=0 failrate=0%`). 49s 검증, 장시간 안정성 미확인 |
| STM32 spi_tx_busy 타임아웃 복구 | △ | DMA 콜백 미수신 시 50ms 타임아웃 후 `HAL_SPI_Abort()`로 CS 복구. 실보드 장시간 미검증 |
| TX_ble stack_temp 실데이터화 | △ | 더미 1234 → `tx_module.tx_data.stack_temp` 구조체 참조. 실측 값 확인 필요 |
| SPI 10ms 폴링 주기 | ✓ | 초당 100 트랜잭션(UART ok=4799/49s, crcfail=0), 오실로 CS(PB12) Δt=10ms 교차검증. "미동작"은 단일 필드 덮어쓰기 관측 한계 ([[spi_10ms_diagnosis_report_260601]]) |
| SPI 단절/복구 UART 경고 | ✓ | `spi \| LINK DOWN` / `spi \| LINK UP` edge trigger 1회. 케이블 분리·재연결 실보드 확인 (커밋 `fe5bf14`, 2026-06-01) |
| SPI_FAIL 응답 — Warning/Fault 플래그·PWM 차단 | ✗ | 미구현. `rx_status.warning/.fault` 죽은 필드(항상 0). 상태 머신·pwm_stop 미연결 |
| STM32 SPI 클럭 9MHz 상향 | ✗ | 시도 후 revert(`7143f55`). nRF52832 SPIS 최대 SCK datasheet 선결 필요 |

### 프로토콜·모니터 (tasks/monitor-formatting, 2026-06-01)

| 기능 | 상태 | 메모 |
|------|------|------|
| 모니터 출력 포맷 통일 (3펌웨어) | △ | `[{eta-rx/eta-tx}:{spi/esb}:{in/out}]` 공통 포맷, 1초 주기, `0xNN\|이름=값`. 3빌드(SES×2+CubeIDE) 통과 (2026-06-01). 실보드 미검증 (커밋 `c9cf6a3`) |
| 0x50 비트맵 매뉴얼 정합 | △ | bit2=Warning, bit3=Fault, BuckRunStop=data[2].bit0. DATA[1..2] 비트 매크로 신설. 3빌드 통과, 실보드 미검증 |
| oled_tv_packet_t 통명 (spi_packet_t alias) | △ | 11B wire 링크 중립 통합 형식. 03_TX_ble 자체 esb_packet_t 제거. 3빌드 통과, 실보드 미검증 |
| 0x51 Zin·Tx Buck Vout Ref 와이어 전송 | △ | data[4..5]=Zin, data[6..7]=Tx_Buck_Vout_Ref. rx_cmd_t 신설(passenger 분리). 3빌드 통과. Uint16 vs i16 잔여 차이 미확인 |

### ESB — 02_RX_esb / 03_TX_esb

| 기능 | 상태 | 메모 |
|------|------|------|
| ESB TX 전송 (03_TX_esb) | △ | while(1) 구조 정리 완료, 실보드 연속 동작 확인 필요 |
| ESB RX 수신 (02_RX_esb) | △ | 수신 모니터링 추가, 실보드 연속 수신 확인 필요 |
| GPIO P0.17/P0.18 토글 (TX 주기 검증용) | △ | 오실로스코프 측정 완료 (920us), 제거 여부 결정 필요 |
| TX_FAILED 1초 윈도우 카운터 | △ | UART 출력 확인, 실보드 장시간 안정성 미확인 |
| RX/TX UART 모니터 출력 | △ | 포맷 정리 완료, 실보드 장시간 동작 미확인 |
| ESB TX→ACK latency | ✓ | 오실로스코프 측정: 약 470us |
| ESB TX 전송 주기 | ✓ | 오실로스코프 측정: 약 920us |
| ESB ACK 수신 주기 | ✓ | 오실로스코프 측정: 약 940us |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현

## 하드웨어 입수

| 보드 | 입고 | 비고 |
|---|---|---|
| BLE_Module_Board_Ver0.1E00 (nRF52832, `02_RX_ble`) | ✓ 2026-06-01 | 회로도 [[schematic_ble_module_board_v01e00]] |

## 미결 사항

- 0x51 Zin·Tx Buck Vout Ref: 코드 Type 재확인 (매뉴얼 Uint16 vs 코드 i16 잔여 차이)
- nRF52832 SPIS 최대 SCK 클럭 datasheet 미ingest — 9MHz 상향 재시도 전 선결
- SPI_FAIL 응답 — Warning/Fault 플래그·PWM 차단·상태 머신 미구현 ([[comm_state_monitoring]])
- BLE_Comm_St ESB-health 연결 — `ble_link` 항상 0, `esb_rx_cnt` 윈도우 기반 판정 미착수
- SPI 오류율 모니터 / spi_tx_busy 타임아웃 복구 실보드 장시간 안정성 검증
- TX_ble stack_temp 실측 값 정상 여부 확인
- (ESB) 실보드 장시간 안정성, GPIO 토글 핀 제거 여부, 01_RX_control ↔ 02_RX_esb UART 브리지 동작 확인
