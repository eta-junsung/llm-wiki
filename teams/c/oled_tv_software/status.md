---
date: 2026-06-08
---

# oled_tv_software — 구현 현황

## 다음 시작점

**Comm_St 재정의 반영 — "통신 생사 = CRC-valid 패킷 도착 윈도우" 로 판정 (2026-06-08 결정)**

판정 의미가 "칩 생사(heartbeat)" → "통신 생사(CRC AND 도착 윈도우)"로 바뀜. 판정식: `링크 ALIVE ⟺ 최근 T 윈도우 내 CRC-valid 패킷 ≥ N개`. 상세 [[comm_state_monitoring]] "정의 변천" 절.

1. **SPI_Comm_St → STM32 로컬 `spi_status` 사용**: SPI 링크 생사는 STM32가 자기 수신 패킷 CRC+timeout으로 직접 판정. `01_RX_control common.c`의 `spi_status`(CRC fail·hb timeout 통합)를 LED2(P0.08) 구동에 연결. 0x10 bit5는 패킷 전달 불필요해짐 — 폐기/보조 heartbeat 여부 결정.
2. **BLE(ESB)_Comm_St → `02_RX_esb` 로컬 판정 후 bit6 전달**: rx_esb가 ESB 수신 CRC-valid 카운터 윈도우로 링크 활성 판정 → 0x10 bit6 적재 → STM32 도달 → LED3(P0.06) 구동. (판정 주체는 송신측 03이 아니라 수신측 02임에 주의 — 구 메모의 `esb_rx_cnt`/`ble_link` 위치 재확인 필요)
3. 가드 주의: LED 코드는 `#if defined(BOARD_CUSTOM)` 안. 극성 active-high(1=ON). 빌드(emBuild) → J-Link 플래싱(J-OB v2, [[st_link_nrf52_flash]]) → 오실로/육안 확인

참고: [[comm_state_monitoring]] — Comm_St 정의 변천·판정식·구현 현황. [[spi_link_reliability]] — `spi_status`·CRC 카운터 구현 측. [[tx_ble_module]] — LED 핀맵·동작. [[st_link_nrf52_flash]] — 플래싱 절차.

---

코드 정리 4개 라운드 (별도 트랙): ① 모니터 1-헤더-1-줄 압축, ② 공유 출력 함수(`oled_tv_protocol.c` 신설, 3 빌드 등록), ③ serialize/deserialize 통합, ④ `SPI_PKT_*` → 링크 중립 이름 개명.

예정 작업 (아이디어 단계·미착수): [[roadmaps/pc-gui|PC GUI]] (UART 패킷 모니터링 + buck 설정), [[roadmaps/spi-esb-refactor|SPI·ESB 리팩토링]] (타인 작업과 merge — 위 코드 정리 트랙 포함).

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

| 보드 | 입고 | 플래싱 | 비고 |
|---|---|---|---|
| BLE_Module_Board_Ver0.1E00 (회사 커스텀, nRF52832) | ✓ 2026-06-01 | ✓ 2026-06-04 `03_TX_ble` | 회로도 [[schematic_ble_module_board_v01e00]]. ST-LINK V2 + pyOCD 성공, LED 점멸 육안 확인 (LED1 상시점등·LED2/LED3 200ms 토글, active-high). 절차·함정 [[st_link_nrf52_flash]] |

> 플래싱 셋업 함정 3개(libusb DLL·Zadig WinUSB 바인딩·pyOCD CTRL-AP 패치)와 트러블슈팅은 [[st_link_nrf52_flash]]에 정리됨. 추가 이슈/해결 공유 시 해당 페이지에 ingest.

## 미결 사항

- 0x51 Zin·Tx Buck Vout Ref: 코드 Type 재확인 (매뉴얼 Uint16 vs 코드 i16 잔여 차이)
- nRF52832 SPIS 최대 SCK 클럭 datasheet 미ingest — 9MHz 상향 재시도 전 선결
- SPI_FAIL 응답 — Warning/Fault 플래그·PWM 차단·상태 머신 미구현 ([[comm_state_monitoring]])
- Comm_St 재정의(2026-06-08) 미구현 — "통신 생사 = CRC-valid 도착 윈도우" 판정식을 SPI(STM32 로컬 spi_status)·ESB(02_RX_esb 로컬 판정→bit6)에 반영 + LED2/LED3 연계 ([[comm_state_monitoring]])
- Comm_St 판정 윈도우 파라미터(T, N) 미정 — SPI 10ms 폴링·ESB 10ms wire 기준 적정값 결정 필요
- SPI 오류율 모니터 / spi_tx_busy 타임아웃 복구 실보드 장시간 안정성 검증
- TX_ble stack_temp 실측 값 정상 여부 확인
- (ESB) 실보드 장시간 안정성, GPIO 토글 핀 제거 여부, 01_RX_control ↔ 02_RX_esb UART 브리지 동작 확인
- 01_RX_control `Monitor_Loop()` 현재 주석처리 비활성 (커밋 `175a8f7`, 03 모니터로 검증하느라 임시로 끔) — 재활성 시점 미정 ([[rx_control#메인-루프]])
