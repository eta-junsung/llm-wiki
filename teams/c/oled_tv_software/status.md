---
date: 2026-06-09
---

# oled_tv_software — 구현 현황

## 다음 시작점

**comm-st (T,N) 상수 통일 + spi_status LINK/CRC 분리 + COMM 라인 완료(`d2232fe`) — 다음은 02/03 COMM 라인 와이어링·N=20 실측 검증**

SPI/BLE_Comm_St 비트 구현·심볼 통일 완료. `d2232fe`(2026-06-09): 판정 임계를 각 링크 (T,N) 직접 상수로 통일(BLE `MIN_COUNT` 3→**20**, SPI timeout 5000→**1000ms**·`TIMEOUT`→`WINDOW` 개명), 01 `spi_status`를 LINK 전용으로 분리(CRC 별도), 3칩 공통 `pkt_print_comm_line()` 추가(01만 호출).

1. **02/03 COMM 라인 와이어링**: `pkt_print_comm_line()`이 02/03엔 컴파일만 되고 호출 안 됨(unused). 02/03에 호출 추가 시 ESB CRC 자리는 `-`(N/A, SW 검증 안 함). [[comm_state_monitoring]].
2. **N=20 실측 검증**: `BLE_COMM_ST_MIN_COUNT=20`(=200ms 윈도우 기대 ~200개의 ~10%)가 실 RF 수신율 대비 적정한지 확인. STM32 모니터 rx 카운트가 `LOG_EN` 게이트로 미관측 — 필요 시 임시 활성.
3. **회사보드 실장 시 LED3 매크로 전환**: 체크인 기본은 DK P0.19(active-low) — 회사 BLE_Module_Board에는 `LED3_PIN`을 P0.06(active-high)으로 수동 교체. [[tx_ble_module]].
4. **(별트랙)** SPI_FAIL/ESB_FAIL 응답 — Warning/Fault 플래그·PWM 차단 상태 머신은 여전히 미구현.

참고: [[comm_state_monitoring]] — 두 비트 링크·(T,N) 모델·spi_status LINK/CRC 분리·COMM 라인·심볼·race-free stamp·노드별 동작. [[spi_link_reliability]] — `spi_status` 구현 측. [[tx_ble_module]] — LED mirror. [[st_link_nrf52_flash]] — 플래싱 절차.

---

코드 정리 4개 라운드 (별도 트랙): ① 모니터 1-헤더-1-줄 압축, ② 공유 출력 함수(`oled_tv_protocol.c` 신설, 3 빌드 등록), ③ serialize/deserialize 통합, ④ `SPI_PKT_*` → 링크 중립 이름 개명.

예정 작업 (아이디어 단계·미착수): [[roadmaps/pc-gui|PC GUI]] (UART 패킷 모니터링 + buck 설정), [[roadmaps/spi-esb-refactor|SPI·ESB 리팩토링]] (타인 작업과 merge — 위 코드 정리 트랙 포함).

## 구현 현황

### SPI 통신 — STM32(01_RX_control) ↔ nRF52832(02_RX_ble)

| 기능 | 상태 | 메모 |
|------|------|------|
| SPI_Comm_St heartbeat (3-MCU) | ✓ | RX_ble가 0x10 Data[0] bit5(`COMM_ST_BIT_SPI`) 토글 → STM32 타임아웃(`d2232fe`: `SPI_COMM_ST_WINDOW_MS=1000`, 구 5s)으로 SPI 단절 감지. 오실로 200ms 토글 확인(Δt≈190ms). 검증 5/5 PASS (`e5e3efc`) |
| `spi_status` LINK/CRC 분리 (이전 통합 환원) | △ | `e5e3efc` 통합 → `d2232fe`에서 분리: `spi_status`=LINK 전용(토글 타임아웃 `SPI_COMM_ST_WINDOW_MS=1000`), CRC는 1초 윈도우 fail로 별도. 실보드 미재검증 ([[comm_state_monitoring]]) |
| 3칩 공통 COMM 라인 `pkt_print_comm_line()` | △ | `d2232fe`. `_shared/oled_tv_protocol.c`. 출력 `COMM \| SPI:{L}{C} ESB:{L}{C}`(1=up/ok,0=down/err,-=N/A). **01만 호출**, 02/03 unused. 실보드 미검증 |
| heartbeat 200ms 독립 타이머 | ✓ | `SpiCommSt_Loop()` millis 게이트로 분리, SPI 사이클 종속 제거. bit5 적재는 송신 복사본 `spi_tx_pkt`에 `SPI_Loop` 송신 직전 stamp(race-free). 오실로 검증 완료 |
| LED2(P0.08) = spi_comm_st_bit mirror | ✓ | 200ms blink 외형 동일, 비트값 정확히 미러. 실보드 검증 (`e5e3efc`). [[tx_ble_module]] |
| 심볼·네이밍 통일 (`COMM_ST_BIT_*`, `spi_comm_st_*`) | ✓ | 3종 펌웨어. bit5/6은 tx_status 아니므로 prefix 분리. 라벨 문자열은 문서 표시명 유지 ([[comm_state_monitoring]]) |
| SPI 오류율 모니터 (ok/fail/err%) | △ | `spi_ok_cnt/spi_crc_fail_cnt` 누적+delta UART 출력(`spi | ok=… | /s ok=100 crcfail=0 failrate=0%`). 49s 검증, 장시간 안정성 미확인 |
| STM32 spi_tx_busy 타임아웃 복구 | △ | DMA 콜백 미수신 시 50ms 타임아웃 후 `HAL_SPI_Abort()`로 CS 복구. 실보드 장시간 미검증 |
| TX_ble stack_temp 실데이터화 | △ | 더미 1234 → `tx_module.tx_data.stack_temp` 구조체 참조. 실측 값 확인 필요 |
| SPI 10ms 폴링 주기 | ✓ | 초당 100 트랜잭션(UART ok=4799/49s, crcfail=0), 오실로 CS(PB12) Δt=10ms 교차검증. "미동작"은 단일 필드 덮어쓰기 관측 한계 ([[spi_10ms_diagnosis_report_260601]]) |
| SPI 단절/복구 UART 경고 | ✓ | `spi \| LINK DOWN` / `spi \| LINK UP` edge trigger 1회. 케이블 분리·재연결 실보드 확인 (커밋 `fe5bf14`, 2026-06-01) |
| SPI_FAIL 응답 — Warning/Fault 플래그·PWM 차단 | ✗ | 미구현. `rx_status.warning/.fault` 죽은 필드(항상 0). 상태 머신·pwm_stop 미연결 |
| STM32 SPI 클럭 9MHz 상향 | ✗ | (보류 M4, 2026-06-09) 시도 후 revert(`7143f55`). 재개 시 nRF52832 SPIS 최대 SCK datasheet 선결 ([[roadmap]] §4) |

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
| BLE(ESB)_Comm_St presence 판정 | ✓ | `EsbCommSt_Loop()`가 수신 delta(02=`esb_rx_cnt`, 03=`esb_ack_cnt`)로 `ble_comm_st_bit` 판정. `BLE_COMM_ST_WINDOW_MS=200`/`MIN_COUNT=20`(`d2232fe`, 이전 3). 양방향 실보드 검증 (`6cd7e6c`) ([[comm_state_monitoring]]) |
| BLE_Comm_St bit6 전달·소비 | ✓ | 02가 0x10 bit6(`COMM_ST_BIT_BLE`) 적재(송신 복사본 race-free)→01 `ble_comm` 추출→`esb \| LINK UP/DOWN` edge 콘솔. 03은 자기 LED3 미러만(STM32 전송 없음) |
| LED3 = ble_comm_st_bit mirror | ✓ | 02·03 모두. 매크로 기본 DK P0.19(active-low), 회사보드 P0.06 주석 ([[tx_ble_module]]) |
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

| 보드 | 입고 | 플래싱 | 비고 |
|---|---|---|---|
| BLE_Module_Board_Ver0.1E00 (회사 커스텀, nRF52832) | ✓ 2026-06-01 | ✓ 2026-06-04 `03_TX_ble` | 회로도 [[schematic_ble_module_board_v01e00]]. ST-LINK V2 + pyOCD 성공, LED 점멸 육안 확인 (LED1 상시점등·LED2/LED3 200ms 토글, active-high). 절차·함정 [[st_link_nrf52_flash]] |

> 플래싱 셋업 함정 3개(libusb DLL·Zadig WinUSB 바인딩·pyOCD CTRL-AP 패치)와 트러블슈팅은 [[st_link_nrf52_flash]]에 정리됨. 추가 이슈/해결 공유 시 해당 페이지에 ingest.

## 미결 사항

- 0x51 Zin·Tx Buck Vout Ref: 코드 Type 재확인 (매뉴얼 Uint16 vs 코드 i16 잔여 차이)
- (보류 M4) nRF52832 SPIS 최대 SCK 클럭 datasheet 미ingest — 9MHz 상향 재개 시 선결 ([[roadmap]] §4)
- SPI_FAIL/ESB_FAIL 응답 — Warning/Fault 플래그·PWM 차단·상태 머신 미구현 ([[comm_state_monitoring]])
- BLE_Comm_St `N=20` 실측 검증 — 실 RF 수신율 대비 적정성 미확인(`d2232fe`로 3→20 설정됨). STM32 모니터 rx 카운트가 `LOG_EN` 게이트로 미관측 (필요 시 임시 활성)
- 02/03 COMM 라인 미와이어링 — `pkt_print_comm_line()` 호출 02/03 추가 필요 (현재 01만). ESB CRC는 SW 검증 안 함(HW CRC 보증) → 02/03에서도 `-`(N/A)
- 회사 BLE_Module_Board 실장 시 LED3 매크로 P0.06(active-high) 전환 — 체크인 기본은 DK P0.19 ([[tx_ble_module]])
- SPI 오류율 모니터 / spi_tx_busy 타임아웃 복구 실보드 장시간 안정성 검증
- TX_ble stack_temp 실측 값 정상 여부 확인
- (ESB) 실보드 장시간 안정성, GPIO 토글 핀 제거 여부, 01_RX_control ↔ 02_RX_esb UART 브리지 동작 확인
- 01_RX_control `Monitor_Loop()` 현재 주석처리 비활성 (커밋 `175a8f7`, 03 모니터로 검증하느라 임시로 끔) — 재활성 시점 미정 ([[rx_control#메인-루프]])
