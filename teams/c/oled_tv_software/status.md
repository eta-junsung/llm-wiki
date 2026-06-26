---
date: 2026-06-26
---

# oled_tv_software — 구현 현황

## 다음 시작점

**[STEP 1] STM32 DK 보드 재검증 (정본 HSI 기준)** — ✓ 완료 (2026-06-17)

정본 코드(Sean + ESB/SPI relay·UART 이식) DK 보드(STM32 Mini Pro + PCA10040) 검증 완료.
- ① UART5 모니터 수신 ✓ ② SPI heartbeat bit5 토글 ✓ ③ ESB bit6 상태 ✓ ④ PWM 100kHz 출력 — 스킵(검증 대상 아님)

**[STEP 2] 실보드 UART 검증** — ✓ 완료 (2026-06-17)

실보드에서 [[pc_uart_gui]] 11B 바이너리 수신 정상 확인.

**[STEP 3] 커스텀 보드(UTO-NBK-52) comm_st 재검증** ✓ 완료 (2026-06-19)

**완료 (2026-06-19)**:
- SPI 배선(P0.22/P0.25/P0.26/P0.27) 후 comm_st 4케이스 재검증 완료 + "02만 ON → SPI UP/ESB DOWN" 신규 케이스 확인
- **02 `eta_protocol.c` seed 수정 commit & push** 완료 (미커밋 해소)
- **03_TX_ble 실보드 검증** 완료 (ESB PTX 동작·P0.17/18 오실로 확인)

~~**시립대 보드 전달 준비 (01·02·03)** — **완료 (2026-06-26)**: 핀맵·구동 절차·PC GUI 사용법 정리 및 보드 전달 완료.~~

**다음 시작점**:

**예정 작업**:

1. **SPI 폴링 주기 10ms → 5ms** (01-02, 03-04 양쪽): `PACKET_INTERVAL`(또는 `SPI_PACKET_INTERVAL_MS`) 변경 후 01·04 양쪽 실보드 재검증.
2. **01·04 상호 SPI 링크 상태 인지**: 04-03 SPI 단절 시 01이 알도록, 01-02 SPI 단절 시 04가 알도록. 이를 위해 02·03이 자체적으로 SPI 통신 상태를 파악하는 메커니즘 필요 — 구체적인 구현 방향은 작업 진입 시 결정.
2. **N=20 실측 검증**: `BLE_COMM_ST_MIN_COUNT=20`(=200ms 윈도우 기대 ~200개의 ~10%)가 실 RF 수신율 대비 적정한지 확인.
3. **`_shared` 매크로 소유권 점검**: `PACKET_INTERVAL`(=10ms)은 `_shared`에 있으나 01만 호출(02/03은 ESB 1ms) → SPI 전용 분리/개명(`SPI_PACKET_INTERVAL_MS`) 후보. [[roadmaps/spi-esb-refactor]] §6.
4. **회사보드 실장 시 LED3 매크로 전환**: 체크인 기본은 DK P0.19(active-low) — 회사 BLE_Module_Board에는 `LED3_PIN`을 P0.06(active-high)으로 수동 교체. [[tx_ble_module]].
5. **(별트랙)** SPI_FAIL/ESB_FAIL 응답 — Warning/Fault 플래그·PWM 차단 상태 머신은 여전히 미구현.

> ⚠️ 01 빌드는 **CubeIDE Ctrl+B 직접** — CLI 빌드 불가([[cubeide_cli_build_trap]]).

참고: [[pc_uart_gui]] — host 바이너리 GUI. [[comm_state_monitoring]] — monitor 바이너리 전환·링크 health 0x10 d0 bit5/6·spi_status LINK/CRC. [[app_protocol_module]] — `print_packets` 바이너리화·`uart_send`. [[spi_packet_format]] — wire 11B(이제 UART에도). [[tx_ble_module]] — LED mirror. [[st_link_nrf52_flash]] — 플래싱.

---

코드 정리 4개 라운드 (별도 트랙) — **코드 `9be1a7a` 추월·부분 구현**: ① 모니터 1-헤더-1-줄 ✓(01), ② 공유 출력 함수(`_shared/oled_tv_protocol.{c,h}`) ✓, ③ serialize/deserialize 통합 ✓ 대체로, ④ ~~`SPI_PKT_*` 개명~~ 무효(이미 `PKT_HDR_*`). → [[roadmaps/spi-esb-refactor]].

완료 작업: [[roadmaps/pc-gui|PC GUI]] ✓(`35b94d0`, 실보드 검증) — UART 바이너리 모니터 + buck 설정 호스트 툴 [[pc_uart_gui]]. 예정(미착수): [[roadmaps/spi-esb-refactor|SPI·ESB 리팩토링]] (02/03 검증·merge·`_shared` 매크로 점검).

## 구현 현황

### SPI 통신 — STM32(01_RX_control) ↔ nRF52832(02_RX_ble)

| 기능 | 상태 | 메모 |
|------|------|------|
| SPI_Comm_St heartbeat (3-MCU) | ✓ | RX_ble가 0x10 Data[0] bit5(`COMM_ST_BIT_SPI`) 토글 → STM32 타임아웃(`d2232fe`: `SPI_COMM_ST_WINDOW_MS=1000`, 구 5s)으로 SPI 단절 감지. 오실로 200ms 토글 확인(Δt≈190ms). 검증 5/5 PASS (`e5e3efc`) |
| 01 SPI 프로토콜 `app_protocol` 적출 | ✓ | `9be1a7a`. `common.c/h`→`app_protocol.c/h`. 공개 API `protocol_loop()`(내부 `exchange_packets`+`print_packets`). 4파일 핸드오프 자립. STM32CubeIDE 실 빌드 + 실보드 동작확인 완료 ([[app_protocol_module]]) |
| `spi_status` LINK/CRC 분리 (이전 통합 환원) | ✓(01) | `e5e3efc` 통합 → `d2232fe`에서 분리: `spi_status`=LINK 전용(토글 타임아웃 `SPI_COMM_ST_WINDOW_MS=1000`), CRC는 1초 윈도우 fail로 별도. 01 실보드 동작확인(`9be1a7a`) ([[comm_state_monitoring]]) |
| UART monitor 바이너리 전환 | ✓ | `35b94d0`(실보드 검증). 01 `print_packets`가 6헤더(0x10~12/0x50~52)를 `pkt_build_*`→`uart_send`로 **11B 바이너리** 송출(구 텍스트 모니터 대체). 링크 health는 0x10 d0 bit5/6 운반. ([[comm_state_monitoring]] "monitor 바이너리 전환", [[app_protocol_module]]) |
| PC UART GUI (`tools/pc_uart_gui`) | ✓ | `35b94d0`(실보드 검증). Python+Tkinter+pyserial. 단일 UART5, 11B HDR 동기+CRC 재동기, 2컬럼 TX/RX 뷰, `Link: SPI/ESB [UP/DOWN]`(d0 bit5/6), buck 입력→`buck <v>\r`→0x51 확인. [[pc_uart_gui]], [[roadmaps/pc-gui]] |
| ~~3칩 공통 COMM 텍스트 라인 `pkt_print_comm_line()`~~ | 제거 | `2f2aa65` 링크 전용 2인자·이벤트 출력 → `35b94d0` **텍스트 라인 자체 폐기**(`print_comm_line_on_change` 삭제). `pkt_print_comm_line()` 포매터는 호출처 없는 orphan. 링크 상태는 0x10 d0 bit5/6 바이너리로 대체 ([[comm_state_monitoring]]) |
| heartbeat 200ms 독립 타이머 | ✓ | `SpiCommSt_Loop()` millis 게이트로 분리, SPI 사이클 종속 제거. bit5 적재는 송신 복사본 `spi_tx_pkt`에 `SPI_Loop` 송신 직전 stamp(race-free). 오실로 검증 완료 |
| LED2(P0.08) = spi_comm_st_bit mirror | ✓ | 200ms blink 외형 동일, 비트값 정확히 미러. 실보드 검증 (`e5e3efc`). [[tx_ble_module]] |
| 심볼·네이밍 통일 (`COMM_ST_BIT_*`, `spi_comm_st_*`) | ✓ | 3종 펌웨어. bit5/6은 tx_status 아니므로 prefix 분리. 라벨 문자열은 문서 표시명 유지 ([[comm_state_monitoring]]) |
| ~~SPI 오류율 모니터 / CRC 카운터~~ | 제거 | `9be1a7a` `spi_ok_cnt`·`monitor_spi_diag` 삭제 → `2f2aa65` `spi_crc_fail_cnt` 카운터·COMM CRC 표시까지 전부 제거. CRC fail = 깨진 패킷 드롭만(플래그·재요청 없음), 무결성 검증은 유지 ([[comm_state_monitoring]]) |
| STM32 spi_tx_busy 타임아웃 복구 | △ | DMA 콜백 미수신 시 50ms 타임아웃 후 `HAL_SPI_Abort()`로 CS 복구. 실보드 장시간 미검증 |
| TX_ble stack_temp 실데이터화 | △ | 더미 1234 → `tx_module.tx_data.stack_temp` 구조체 참조. 실측 값 확인 필요 |
| SPI 10ms 폴링 주기 | ✓ | 초당 100 트랜잭션(UART ok=4799/49s, crcfail=0), 오실로 CS(PB12) Δt=10ms 교차검증. "미동작"은 단일 필드 덮어쓰기 관측 한계 ([[spi_10ms_diagnosis_report_260601]]) |
| ~~SPI 단절/복구 UART 경고 (LINK DOWN/UP)~~ | 제거 | `fe5bf14`에 구현(실보드 확인)됐으나 `9be1a7a`에서 **출력 제거** — COMM 라인 `SPI:%c`와 값 중복이라. 링크 상태는 이제 COMM 라인(edge 출력, `2f2aa65`)으로 |
| SPI_FAIL 응답 — Warning/Fault 플래그·PWM 차단 | ✗ | 미구현. `rx_status.warning/.fault` 죽은 필드(항상 0). 상태 머신·pwm_stop 미연결 |
| STM32 SPI 클럭 9MHz 상향 | ✗ | (보류 M4, 2026-06-09) 시도 후 revert(`7143f55`). 재개 시 nRF52832 SPIS 최대 SCK datasheet 선결 ([[roadmap]] §4) |
| **01 정본 코드베이스 전환 (HSI 64MHz)** | ✓ | 2026-06-15 빌드·flash. **2026-06-16 DK 보드 검증 완료** (STM32 Mini Pro + PCA10040). 정본 경로 `OLED_TV_Rx_Module/` (브랜치 merge). 팀원(Sean) 작성 전력제어 중심 정본(AppSequence/AppCtrl/Soft MHz, main.c 통합형)으로 교체, ESB/SPI relay·UART 모니터 함수 이식. ([[sysclk_hsi_transition]] — HSI SYSCLK 64MHz 확정, PCLK1=32MHz, SPI 8Mbps. [[spi_pin_mapping]] — SPI 배선 핀맵) |

### 프로토콜·모니터 (tasks/monitor-formatting, 2026-06-01)

| 기능 | 상태 | 메모 |
|------|------|------|
| 모니터 출력 포맷 | ✓(01 바이너리·02 텍스트)/△(03 텍스트) | 01은 `35b94d0` 11B 바이너리(실보드 검증). 02는 `99c893f`(실보드 검증) 배너 줄 제거·말미 개행 통일 완료. 03 텍스트 실보드 미검증 |
| `_shared` 프로토콜 다듬기 | ✓ | `9ad338d`(실보드 검증) 죽은 심볼(`pkt_print_comm_line`·`pkt_apply_rx`) 제거, 매직넘버 상수화(`PKT_KIND_COUNT=3`/`PKT_RR_STATUS=0`/`INPUT=1`/`OUTPUT=2`·`PKT_DATA_FW_OFFSET=6`), `calc_checksum`→`pkt_checksum` 통일(01 포함). `99c893f`(실보드 검증) 02 배너·개행 정리 |
| 0x50 비트맵 매뉴얼 정합 | △ | bit2=Warning, bit3=Fault, BuckRunStop=data[2].bit0. DATA[1..2] 비트 매크로 신설. 3빌드 통과, 실보드 미검증 |
| oled_tv_packet_t 통명 (spi_packet_t alias) | △ | 11B wire 링크 중립 통합 형식. 03_TX_ble 자체 esb_packet_t 제거. 3빌드 통과, 실보드 미검증 |
| 0x51 Zin·Tx Buck Vout Ref 와이어 전송 | ✓ | data[4..5]=Zin, data[6..7]=Tx_Buck_Vout_Ref (u16 BE, volts×100). rx_cmd_t 신설(passenger 분리). 2026-06-16: GUI 바이너리 0x51 → `pkt_apply_rx_cmd()` → rx_cmd.tx_buck_vout_ref, 실보드 GUI→03 Monitor 정상 전파 확인. u16 BE 확정. ([[buck_vout_ref_command_path]]) |

### ESB — 02_RX_esb / 03_TX_esb

| 기능 | 상태 | 메모 |
|------|------|------|
| 02_RX_ble 모듈 분리 리팩토링 | ✓ | `b92835c`(2026-06-11) eta_ 접두사 전환·실보드 검증 완료. 모듈 구조: eta_gpio/clock/uart/spi/esb(저수준) + eta_protocol(응용 계층). 잔여 점검: `ADD_SPI` 전역 전파 확인(빌드·동작 정상이나 TU 전파 범위 미확인). ([[app_protocol_module]], [[ses_build_conventions]], [[nrf52_module_naming]]) |
| 03_TX_ble 모듈 분리 리팩토링 | ✓ | `1d7f71a`(2026-06-11) `emBuild` 에러 0·경고 0. **실보드 검증 완료 (2026-06-19)**: ESB PTX 동작·P0.17/18 오실로 확인. ([[tx_ble_module]], [[nrf52_module_naming]], [[nrf52_firmware_conventions]]) |
| 03_TX_ble SPI_Loop SPIS 재작성 | ✓ | `e706b53`(2026-06-11) 기존 SPIM 코드 폐기 → 02 거울 SPIS(`nrf_drv_spis`, MODE_2, PIN_SPI_* 동일) 전면 재작성. `g_last_ack_by_hdr[3]` round-robin MISO 서빙. **실보드 검증 완료 (2026-06-19)**. ([[roadmaps/04-tx-control-dummy]] §4) |
| 04_tx_control 더미 프로젝트 | △ | `07fbf1f`(2026-06-11) 01_RX_control 복제 → ADC/PWM/CAN/DAC 제거, pkt_print 수신 모니터 추가. SPI2+UART5 잔존. **.ioc 파일명 `RX_control.ioc` 잔류. STM32CubeIDE Ctrl+B 빌드 미수행**. ([[roadmaps/04-tx-control-dummy]]) |
| 릴레이 양방향 미연결 견고화 | △ | `e72b86e`(TX→RX 03 seed) + `6fc8b92`(RX→TX 02 seed, 2026-06-12) + **미커밋**(TX→RX 02 `esb_pkt` seed, 2026-06-18). 02 `esb_pkt`(ESB수신→SPI forward) seed 누락이 "01+02만 구동 시 SPI DOWN 오판" 버그 원인 — `eta_protocol.c:227-232` seed 추가, DK 보드 검증 통과(01+02 only, SPI UP/ESB DOWN). **커스텀 보드 실보드 미검증**. ([[app_protocol_module]] "02 esb_pkt seed 누락", [[comm_state_monitoring]] "구조적 결합 정밀 메커니즘") |
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
| BLE_Module_Board_Ver0.1E00 (회사 커스텀 UTO-NBL-52, nRF52832) | ✓ 2026-06-01 | ✓ 2026-06-04 `03_TX_ble` | 회로도 [[schematic_ble_module_board_v01e00]]. ST-LINK V2 + pyOCD 성공, LED 점멸 육안 확인 (LED1 상시점등·LED2/LED3 200ms 토글, active-high). 절차·함정 [[st_link_nrf52_flash]] |
| UTO-NBK-52 #02 (커스텀, nRF52832) | ✓ 2026-06-17 | ✓ 2026-06-18 `02_RX_ble` | DEVICEID `0x09741932`. `LED1_ON=1u` 수정 후 LED1 정상 점등 확인 — **HW 정상**. [[uto_nbk_52]] |
| UTO-NBK-52 #03 (커스텀, nRF52832) | ✓ 2026-06-17 | ✓ 2026-06-18 `03_TX_ble` | DEVICEID `0xE9775EC9`. LED1 정상 점등(**active-HIGH** 확정). [[uto_nbk_52]] |

> 플래싱 셋업 함정 3개(libusb DLL·Zadig WinUSB 바인딩·pyOCD CTRL-AP 패치)와 트러블슈팅은 [[st_link_nrf52_flash]]에 정리됨. 추가 이슈/해결 공유 시 해당 페이지에 ingest.

## 미결 사항
