# log

시간순 작업 로그. 형식: `## [YYYY-MM-DD] <타입> | <제목>`

---

## [2026-06-11] ingest | lp-am263p — EPWM Time-Base Counter Synchronization (§7.5.6.4.3.3) + fan-out 스큐 토폴로지

TRM EPWM sync 본문 보완 요청. **핵심 발견: 본문 누락 아님** — raw `ch07_5_controlss.md` :5683–5953은 PDF pp.651–654를 충실 재현(끊긴 cross-ref ":5801 Refer to **for** a list…"는 PDF p.652 TI 원본 버그, 추출 손실 아님). PDF figure 7-181/7-182를 직독해 환원.

- **신규 [[am263p_epwm_sync_topology]]**: ① SYNC는 **모듈별 독립 MUX(fan-out)**, 데이지체인 아님 — `EPWMSYNCINSEL`로 공용 SYNCOUT 풀(Table 7-154: EPWM0~23/ECAP0~9/INPUTXBAR/TIMESYNCXBAR/FSI)에서 소스 1개 선택. ② source→target **hop당 지연 고정**(`TBCLK==EPWMCLK`→2×EPWMCLK, `TBCLK<EPWMCLK`→1×TBCLK), **target 인덱스 무관·누적 없음**. ③ Figure 7-181(SYNCIN MUX·SYNCOUT 로직·SYNCPER)·7-182(EXTSYNCOUT 8 PLLSYSCLK stretch) 직독. ④ 레지스터 표(PHSEN/PHSDIR/TBPHS/PRDLD/PRDLDSYNC/SYNCOUTEN/EPWMSYNCINSEL/EPWM_CLKSYNC/one-shot).
- **검증질문 답**: EPWM2 SYNCOUT을 EPWM4·EPWM7이 각각 fan-out 선택 → **둘 다 1-hop·같은 지연 → 상호 정수클록 스큐 0**(잔여 sub-clock은 TRM 모델 밖, 미검증 예측). 8kw ~11ns 비대칭의 정체 = master 0-hop vs slave 1-hop = 2×EPWMCLK(≈10ns @prescale 1, 200MHz) + 라우팅 ~1ns.
- **Table 7-153 "synchronization order" 해소**: 가리키는 실체는 §7.5.6.4.3.3 = Figure 7-181 MUX + Table 7-154 선택행렬. **device-specific sync-order/체인 표는 TRM에 부재**(SPRUJ55D).
- **갱신**: [[am263p_epwm_module_sync_deadtime]](§함정 "모듈간 위상 스큐" 근본=hop 수 비대칭으로 재서술 + fan-out 0-스큐 토폴로지 추가), [[am263p_trm]](Ingested 섹션 등록 + 본문 누락 없음 확인), index, log.

## [2026-06-11] 환원 | 8kw-ev-wpt-tx — UART5 PC 텔레메트리 (18B 바이너리 패킷 + PC GUI)

UART5로 ADC 6채널을 PC에 송출하는 바이너리 패킷 + 호스트 GUI 작업 환원 (branch uart5, commit ba241fa·979699d, 실보드 검증 2026-06-11). c팀 oled 선례([[pc_uart_gui]]) 형식 참조.

- **신규 [[uart5_packet_protocol]]**: 18B 고정 big-endian `[SOF=0xA5][LEN=12][TYPE=0x01][SEQ][ch0..ch5 raw u16][CRC-16/CCITT-FALSE]`, CRC poly 0x1021·init 0xFFFF·범위 byte[1..15]. RTI2 10Hz·115200/8N1 polled blocking. thin device(wire=raw only)·smart host(mV=raw*3300/4095 미러). 채널 순서=ETA_ADC_CH enum, `eta_packet.c` 직렬화 자동 추종. SOF동기+CRC 1바이트 슬라이드 재동기. 선례 대비 CRC-16·단일 패킷·단방향.
- **신규 [[pc_monitor_gui]]**: `tools/gui/gui.py`(pyserial+Tkinter+matplotlib). 4컬럼 표(Channel/ADC(V)/ADC(12bits)/Physical)·채널 체크박스(플롯·CSV 토글)·패킷 헬스(Hz/SEQ드롭/CRC에러)·라이브 플롯·raw-only CSV·PyInstaller 단일 exe. Physical 계수 테이블 단일 소스(계수 미입수 placeholder).
- **검증**: COM13(CP210x, J1.4→THVD1400→J24) 29.8s — 10.067Hz, 301프레임 전부 유효, SEQ 드롭 0·CRC 에러 0. 프레이밍 강건성(정상/1바이트 손상→재동기/ASCII 잡음·가짜 SOF→폐기 후 복구) 모두 PASS.
- **미결 해소**: A1.5 UART 출력 채널 하드코딩(`DebugP_log`) → `eta_packet.c` 채널 루프 직렬화로 대체(자동 추종).
- **신규 잔여**: UART5 송신 논블로킹화(현재 polled blocking), 물리량 변환 계수 미입수(GUI Physical placeholder), RS-485 Phase 2.
- ⚠️ **핸드오프 프롬프트 전제 정정**: "wiki 루트 빈 슬레이트, status.md 신규" → 오류. 실제로는 ADC(A2)·PWM(P1/P2) 이력이 가득한 기존 디렉토리 → status.md는 **갱신**(덮어쓰기 아님), concept 2개만 신규.
- **갱신**: [[status]](UART5 텔레메트리 직전완료 절·구현현황표 행·미결사항), [[roadmap]](§2 별트랙 완료), index, log.

## [2026-06-11] 환원 | oled_tv_software — 03_TX_ble 리팩토링 완료 + nRF52 코딩 관습 추가

- **03_TX_ble 리팩토링**: 1d7f71a, emBuild 에러 0·경고 0. 02와 동일 6개 eta_ 모듈 구조. 실보드 미검증. SPI_Loop 비활성 보존.
- **nrf52_firmware_conventions 추가**: 모듈 의존 방향(protocol→{esb,spi,clock,gpio} 단방향)·Monitor baseline-delta(unsigned wrap 무해)·ESB health 독립 판정(02=rx_cnt, 03=ack_cnt) 절 신설.
- **tx_ble_module**: DBG_PIN_TX_ATTEMPT/DONE 심볼 추가, 03 리팩토링 행 추가.
- **갱신**: [[status]](다음 시작점·02 행 ✓·03 행 △·미결 사항), [[roadmap]](§3 별트랙 03+_shared 다음), [[nrf52_firmware_conventions]], [[tx_ble_module]], log.

## [2026-06-11] 환원 | oled_tv_software — 02_RX_ble 정리 도메인 사실 (채널 분리·GPIO 구분·코딩 관습)

코드만으로 드러나지 않거나 펌웨어 CLAUDE.md와 어긋난 4가지 사실 환원 (b92835c→e85839c):

- **[1] 모니터링 채널 분리**: 01 UART5 = 11B 바이너리(기계 파싱 계약, uart_gui.py), 02 Monitor_Loop = 사람 텍스트(디버그 터미널, 기계 파서 없음). 02 코드 수정은 GUI 무관. [[comm_state_monitoring]] "모니터링 채널 분리" 절 신설. CLAUDE.md 갱신 후보 표시.
- **[2] GPIO P0.17/18 구분**: "P0.17/18 = ESB 토글 핀, 제거 금지"는 **03_TX_ble 한정**. 02_RX_ble DK에서 P0.17/18/19는 LED1/2/3(System Ready·SPI_Comm_St·BLE_Comm_St). [[rx_ble_module]] "GPIO 핀 현행" 절 신설, [[tx_ble_module]] 경고 주석 추가. CLAUDE.md 갱신 후보 표시.
- **[3] nRF52 코딩 관습** 신규 페이지 [[nrf52_firmware_conventions]]: ISR printf 금지(HardFault 실증)·오류 카운터 패턴(1초 윈도우 블록 끝 append)·init 배너 printf 금지·eta_ 접두사([[nrf52_module_naming]] 위임).
- **[4] NRF_LOG/SEGGER_RTT 잔재**: 02_RX_ble init 코드만 존재·호출 0건. 무해하나 신규 정리 시 혼동 주의. [[nrf52_firmware_conventions]] 수록.
- **갱신**: [[comm_state_monitoring]], [[rx_ble_module]], [[tx_ble_module]], index, log.

## [2026-06-11] 환원 | oled_tv_software — nRF52 모듈 네이밍 관습 + SES emProject 가상 폴더 확정

- **[1] nRF52 로컬 모듈 `eta_` 접두사 규칙** (`b92835c`, 빌드·실보드 검증 완료): `app_`은 nRF5 SDK 네임스페이스(`app_uart`/`app_timer`/`app_fifo` 등 다수)라 로컬 모듈과 충돌. `eta_`로 근본 제거 — 헤더/소스 이름 대칭 회복(`eta_uart.h`+`eta_uart.c`). 적용 범위: 02_RX_ble 완료, 03 후보, 01 해당 없음. 신규 페이지 [[nrf52_module_naming]] 작성.
- **[2] SES `.emProject` `<folder>` 가상 그룹 확정**: `<folder Name="...">` 는 Solution Explorer 표시 전용 — `file_name`·`c_user_include_directories`를 건드리지 않는 한 빌드·디스크 경로 무영향. [[ses_build_conventions]] §4 추가.
- **갱신**: [[ses_build_conventions]](§2 해소 처리·`eta_` 전환 경위·§4 가상 폴더 신설·관련 링크), index, log.

## [2026-06-10] 갱신 | lp-am263p·8kw-ev-wpt-tx — UART5 U54 보드먹스 근본원인 확정·실보드 검증

- **확정 사실**: U54(SN74CB3Q3257) SEL=L→UART(B1), OE#=L→인에이블(SCDS135E Table 6-1). TCA6416 P00/P14=LOW → UART5 헤더 연결. J1.4=GPIO73=UART5_TXD, J1.3=GPIO74=UART5_RXD(post-mux, UG :1525-1526).
- **실보드 PASS (2026-06-10)**: J1.4↔J1.3 루프백 + TCA6416 P00/P14=LOW → TX==RX Logic2 토글. 세팅 전 무토글·후 토글 인과 확증.
- **2026-06-09 오진 정정**: "UART_write 주석·DE 미구현이 원인" → 오진. 실제 근본원인 = ② 보드먹스(U54+TCA6416). ① force_io(SoC PADCONFIG)는 처음부터 정상. 2층 모델([[am263p_iomux_force_io_enable]]) 추가.
- **함정 추가**: TCA6416 출력 레지스터 리셋 디폴트=HIGH → LOW 먼저 쓰고 방향 출력으로 세팅(글리치 방지). I2C1 핀: SCL=I2C1_SCL(D7), SDA=I2C1_SDA(C8) 확정.
- **갱신**: [[lp_am263p_uart_epwm_mux]](가설→확정 재작성), [[am263p_iomux_force_io_enable]](오진 정정·2층 모델), 8kw [[status]](UART5 루프백 PASS·Phase 2 분리).
- **잔여(Phase 2)**: 8kw 보드 결합 시 THVD1400 U13 DE(`EN_485`=GPIO91=J5.48) 구현.

## [2026-06-10] ingest | oled_tv_software — 02_RX_ble 모듈 분리 리팩토링 설계 결정 환원

- **작업**: `02_RX_ble` 단일 `Application/main.c`(618줄) → 관심사별 모듈 분리. 01_RX_control `app_*.c/.h` layering을 기준 삼아 순수 코드 이동(동작 불변 목표). 빌드: `emBuild` 에러 0·경고 0, `RX_BLE.hex` 산출. 실보드 검증 미수행(내일 예정).
- **디렉토리**: `Application/Inc/app_*.h` + `Application/Src/app_*.c`, `main.c`는 루트 잔류.
- **모듈 분할**: `app_gpio`/`app_clock`/`app_uart`/`app_spi`/`app_esb`(저수준 드라이버) + `app_protocol`(두꺼운 응용 계층: SPI exchange·ESB ACK forwarding·comm_st 판정·monitor, `protocol_loop()` 단일 진입점). 계층 방향 단방향 정리(esb_pkt[] = app_esb 소유, SPI 버퍼·comm_st = app_protocol 소유).
- **`_shared` 변경**: `pkt_checksum` static → 공개 함수로 승격. 02 자체 `calc_checksum` 제거. 01 미접촉.
- **미해결 2항목 (내일 결정)**: ① `app_uart_drv.h` 헤더명 최종 결정(nRF5 SDK `app_uart.h` shadow 회피책), ② `ADD_SPI` 매크로 전역 전파(`.emProject` `c_preprocessor_definitions` 이동) 적절성 확인.
- **신규 페이지**: [[ses_build_conventions]] (SES 빌드 함정 3개 정리).
- **갱신**: [[app_protocol_module]](3펌웨어 표준 패턴·모듈 분할·계층 방향·`_shared` 체크섬 API 절 추가), [[status]](다음 시작점·02 리팩토링 행·미결 2항목), [[roadmap]](§3 별트랙), [[roadmaps/spi-esb-refactor]](§3 현재 위치), index, log.

## [2026-06-10] ingest | lp-am263p — TI PROC171A 회로도 UART5 먹스 블록 (Tier 2) + THVD1400 오귀속 정정

- **소스**: TI LP-AM263P 회로도 SPRR503A(`PROC171A`, Rev A). [[schematic_ingest_strategy]] **Tier 2**(PDF 텍스트레이어) — Altium `.SchDoc`이 바이너리 OLE라 Tier 1 네트리스트 export 불가(라이선스). 동봉 SCH PDF는 `pdftotext -layout` 추출 양호. raw `teams/g/lp-am263p/raw/proc171_schematic/`(PDF 전체 + 시트 11/13/21/23 텍스트). 새 소스 [[schematic_lp_am263p]].
- **정정(검증된 오류)**: wiki가 RS-485 트랜시버 **THVD1400 U13을 lp-am263p 부품**처럼 다뤘으나 오류. 네트리스트에 `485`/`THVD`/`RS485` 0건 → **LP-AM263P엔 RS-485 트랜시버 없음**. THVD1400 U13은 **8kw-ev-wpt-tx 커스텀 보드** 부품(LP를 모듈로 결합). J5.48=GPIO91은 LP↔8kw 경계 핀. 수정: [[am263p_iomux_force_io_enable]] :87/:91, [[am263p_syscfg_soft_vs_hard_assign]] :49.
- **핵심 발견 → [[lp_am263p_uart_epwm_mux]]**: UART5_TXD/RXD는 온보드 **U54(SN74CB3Q3257) FET 버스스위치**로 EPWM9와 다중화돼 BP 헤더(`EPWM15_A/B_BP`)로 나감. 먹스 SEL(pin1)/EN(pin15, active-low)은 **TCA6416 IO expander(U63, AM263P_I2C1 @0x20)의 P00/P14**가 구동 — GPIO 아님, 제어선 풀저항 없음. TCA6416 리셋=전포트 입력 → **펌웨어 I2C 설정 전 먹스 미정**.
- **8kw 함의(가설, 미검증)**: 8kw가 BP 헤더(post-mux)에서 UART5 탭하면 LP의 이 먹스가 UART로 설정돼야 신호가 나옴 → 8kw UART5 미동작의 **LP-측 제3 후보 원인**([[am263p_iomux_force_io_enable]] 펌웨어 IOMUX 원인배제 + UART_write 주석 + RS-485 DE 미구현 위에 추가). 검증: 펌웨어 TCA6416 설정 grep + JTAG expander 레지스터 read + 헤더핀 스코프.
- **확인 필요**: BP 헤더 J-핀 정합(회로도 net 핀34/J7.45 vs UG J1.4/J1.3), J1.4 post/pre-mux 여부, SEL 극성, 누가 expander 디폴트 설정(TI Board init?).

## [2026-06-10] ingest | oled_tv_software — UART monitor 텍스트→바이너리 전환 + PC GUI 추가 (commit 35b94d0)

- **근거 커밋**: `35b94d0` (branch esb, 2026-06-10 실보드 검증). 직전 `2f2aa65`(COMM 라인 2인자·이벤트화) 위에, 01_RX_control UART5 모니터를 **텍스트 printf → 11B 바이너리 패킷 송출**로 바꾸고 host PC GUI(`tools/pc_uart_gui/uart_gui.py`)를 추가.
- **monitor 바이너리화**: `print_packets()`가 6헤더(0x10/0x11/0x12/0x50/0x51/0x52)를 `pkt_build_tx`/`pkt_build_rx`로 빌드해 신규 `uart_send()`(app_usart)로 1초 주기 송출. wire 11B(`[HDR][LEN=0x08][DATA[8]][CRC]`, BE, scale 0.01) 불변 — 이제 UART에도 흐름. TeraTerm으로 열면 깨져 보이는 게 정상.
- **COMM 텍스트 라인 폐기**: `print_comm_line_on_change()` 삭제. 링크 health(SPI_Comm_St/BLE_Comm_St)는 0x10 status d0 **bit5/bit6**로 운반(1초 주기 항상 실림) — 별도 이벤트 라인 불필요. `pkt_print_comm_line()` 공유 포매터는 호출처 없는 orphan.
- **PC UART GUI(신규)**: Python+Tkinter+pyserial. 단일 UART5 송수신, 11B HDR 동기+CRC(`pkt_checksum` XOR 포팅) 재동기(1바이트 슬라이드 → command 텍스트 잡음 자연 폐기). 2컬럼(좌 TX 0x10~12/우 RX 0x50~52) 뷰·필드명 사전표기·값만 갱신. `Link: SPI [UP/DOWN] ESB [UP/DOWN/-]`(d0 bit5/6). buck 입력칸 2개→`buck <v>\r` 송신, 확인은 0x51 `Tx_Buck_Vout_Ref`(volts×100).
- **buck 경로 불변**: end-to-end(UART→0x51 DATA[6,7]→SPI→ESB→03)는 그대로, 확인 방법만 텍스트→바이너리 0x51 파싱으로.
- **무변경**: command 채널(UART5 라인 단위 ISR 파싱)·응답 printf(`buck=.. V`)는 수동 TeraTerm 디버그용으로 잔존. command 응답 텍스트와 바이너리 모니터가 한 포트에 섞여 나감.
- **빌드 함정(신규 페이지)**: STM32CubeIDE CLI 빌드 불가(`stm32cubeidec.exe` GUI 서브시스템·즉종료) → IDE Ctrl+B. CubeMX 재생성 금지. [[cubeide_cli_build_trap]].
- **로드맵**: [[roadmaps/pc-gui]] G0~G3 완료(G0 결정=UART5 단일 포트·monitor 바이너리 전환).
- **신규 페이지**: [[pc_uart_gui]], [[cubeide_cli_build_trap]].
- **갱신**: [[comm_state_monitoring]](갱신이력3·monitor 바이너리 전환 절·pkt_print_comm_line historical 강등·보류·관련), [[app_protocol_module]](print_packets 바이너리화·print_comm_line_on_change 삭제·빌드함정·관련), [[spi_link_reliability]](링크표시 행·LINK DOWN/UP·단절후속), [[rx_control]](메인루프·UART5절), [[spi_packet_format]](11B가 UART에도), [[uart_command_set]](방향 주의), [[buck_vout_ref_command_path]](확인방법), [[status]](다음시작점·현황표 행3개·미결·예정), [[roadmap]](§3·§5·date), index, log.
- ⚠️ **직전 환원(2f2aa65 COMM 라인 이벤트화, commit 66e1892)의 'COMM 텍스트 라인' 기술은 이번에 historical 강등** — `35b94d0`이 그 텍스트 라인 자체를 제거했기 때문.

## [2026-06-10] ingest | 8kw-ev-wpt-tx — PWM 주파수 85kHz 고정 + dead-time config 분리 구현·실보드 검증 (commit d01fc0a)

- **근거 커밋**: `d01fc0a` (branch pwm). 직전 `8046744`(dead-time 단일소스)·`6e6b342`(P1 4핀) 위에 **주파수 확정값(85 kHz) 반영 + 튜닝 knob 파일 분리**를 얹어 4채널 실측 PASS. P2 △→✓.
- **주파수 85 kHz 고정·실측**(전엔 "확정 스펙"일 뿐 미구현): `TBPRD 1000→1176`, `cmpA 500→588`, `EPWM7 CMPB 470→558`(@150 ns). Saleae **85.032 kHz**(+0.002%, 주기 11.7603 µs, 지터 σ≈0.74 ns) — 계산 1176과 일치. **TBCLK=200 MHz는 이제 전제 아닌 확정 사실**(1 count=5 ns).
- **dead-time 단일소스 위치 이전**: ~~`eta_pwm.h ETA_DEADTIME_NS`~~ → **`src/eta_bsp/eta_tuning.h`**(신설, HW 엔지니어용 컴파일타임 knob 전용). **유효범위 100~400 ns, 이탈 시 `#error` 빌드 차단**. 한 줄만 바꿔 재빌드→파생값(COUNTS·EPWM7 CMPB) 자동 추종.
- **런타임 override → SysConfig 면역**: 주파수(TBPRD/cmpA)·dead-time 모두 `eta_pwm_init()`이 런타임 override → `example.syscfg` 재생성으로 기본값 덮여도 면역. `example.syscfg`는 안 건드림. ⚠️ **빌드 환경**: CCS makefile이 절대경로 박음 → 다른 노트북 clone 후엔 CCS import로 재생성해 빌드. `eta_tuning.h`는 순수 C 컴파일이라 syscfg 재생성 불요(override 방식 이점).
- **검증(Saleae 4ch: HS1 J4.39/LS1 J4.40/HS2 J6.52/LS2 J6.51, dead-time 100/150/400 ns 스윕, 전 주기)**: duty(HS) 49.15/48.73/46.60% — `50%−dt/T` 정확 추종(AHC 정상, 결함 아님); dead-time 100/150/400 ns 완벽 선형(20/30/80 counts, 레그1 σ<1 ns); **shoot-through 양 레그 전 주기 0건**(최소 DT 89 ns 양수 마진). **PASS.**
- **새 사실 — 레그2 dead-time 비대칭(향후 P3/P4 마진)**: 두 모듈 동기라 모듈간 **~11 ns(≈2.2 counts) 고정 위상 스큐** → dead-time HS→LS +11/LS→HS −11 ns 비대칭(합=2×설정). 레그1(단일 모듈 dead-band)은 없음. 현 스펙(100~400 ns) 무해(89 ns 마진), **50 ns 이하 시 마진 재확인**, 대칭 필요 시 EPWM7 CMPB +2 counts 트림. → 플랫폼 일반 사실로 [[am263p_epwm_module_sync_deadtime]] §함정에 승격.
- **dead-time 최종값은 미결 유지**: 현재 150 ns 베이스라인 커밋, 전력단 브링업 때 100~400 ns 중 확정. (인프라·config 분리는 완료.)
- **갱신**: [[status]](소스레이아웃 eta_pwm/eta_tuning.h·§85kHz 검증절·현황표·미결[비대칭·빌드환경·최종값]·다음), [[pwm]](§1 사실·§2 P0/P2 표·§3 dead-time 단일소스 위치·§85kHz 검증절·§레그2 비대칭절·§빌드 환경절·§4/5/6·date), [[pwm_pinmap]](스펙 85.032kHz·단일소스 위치·비대칭), [[am263p_epwm_module_sync_deadtime]](§함정 위상스큐 비대칭·§검증 85kHz·§8kw 인스턴스 CMPB558/eta_tuning.h), [[roadmap]](pwm 행 P2✓·현재위치), log·index.

## [2026-06-10] ingest | 8kw-ev-wpt-tx — 레그2 SYNC dead-time concept 승격 + 주파수 85kHz 고정 확정·dead-time 100~400ns

- **concept 승격(신규)**: [[am263p_epwm_module_sync_deadtime]] (lp-am263p 플랫폼 concept — 선례 [[am263p_epwm_primary_pad_no_force_io]]와 동일 배치). 풀브리지 레그 HS/LS가 다른 EPWM 모듈에 걸칠 때: master `syncout=ON_CNTR_ZERO`→slave `syncin`·phaseShift=0 위상정렬 + slave AQ 반전 + CMPB 오프셋(`TBPRD/2−DT`, `<TBPRD/2` 엄수). SYNC-in 기본 disable(자유구동) 주의·dead-band 레그와 ns 소스 공유. 8kw 레그2(EPWM4_A→EPWM7_B) 실측 출처. [[pwm]] §3 환원 후보 해소(승격 완료).
- **주파수 확정(사용자 2026-06-10)**: 브링업 임시 100 kHz → **85 kHz 고정**. UP_DOWN `TBPRD=TBCLK/(2·f)=200MHz/(2·85kHz)≈1176`[정수·실측은 코드 확인]. dead-time 카운트는 TBCLK 기준이라 주파수 무관, CMPB의 `TBPRD/2`만 재계산.
- **dead-time 범위 확정**: **100~400 ns 조정 가능, 실험 후 고정 예정**(기존 "시작 150ns" → 범위 명시). 100ns→20·400ns→80 count(5ns 배수라 절삭손실 0). 검증 빌드(150/300ns)는 브링업 100kHz에서 수행 — 85kHz 재빌드 시 결론 동일.
- **갱신**: [[am263p_epwm_module_sync_deadtime]](신규), [[pwm]](주파수·dead-time범위·concept 링크·검증 100kHz 맥락·P0/모름/블로커/환원후보·date), [[pwm_pinmap]](스펙 85kHz·dead-time범위·concept 링크·date), [[status]](스펙·미결·다음·date), [[team_briefing_8kw]](로드맵 P0/P2·스펙·§5·date), [[roadmap]](pwm 행·현재위치·date), index(concept 신규 + pwm·pwm_pinmap 줄).

## [2026-06-09] ingest | 8kw-ev-wpt-tx — PWM dead-time 단일소스 #define 통일(두 레그·두 메커니즘·하나의 ns 소스) + 스윕 검증 (commit 8046744)

- **근거 커밋**: `8046744` (branch pwm). dead-time을 두 레그 모두 `eta_pwm.h` `#define ETA_DEADTIME_NS` 하나로 통일 + 150/300ns 스윕 4채널 실측. (직전 P1 4핀 = `6e6b342`.)
- **사실관계 정정**: 직전 wiki는 "레그1 dead-time 단일소스 미적용 — 향후 통일 예정"으로 적었으나, `8046744`가 **레그1까지 통일 완료** → [[pwm]]·[[status]] 해당 후속 항목 해소.
- **단일소스 패턴(핵심)**: `ETA_DEADTIME_NS`(=150U) → `ETA_NS_TO_COUNTS(ns)=(uint16_t)((uint32_t)ns*(TBCLK_HZ/1MHz)/1000)` 정수 floor. **TBCLK=200MHz → 1 count=5ns**, 150→30·300→60(절삭손실 0), TBPRD=1000(UP_DOWN 100kHz). `ETA_DEADTIME_COUNTS=30@150ns`.
  - **레그1(EPWM2 dead-band)**: `eta_pwm_init()`이 `EPWM_setRisingEdgeDelayCount`/`setFallingEdgeDelayCount`로 RED/FED=ETA_DEADTIME_COUNTS 재적용(RED=FED 대칭, 주기당 갭 2개, SysConfig 기본 override).
  - **레그2(EPWM7 CMPB 오프셋)**: `ETA_EPWM7_CMPB_INIT=TBPRD/2−ETA_DEADTIME_COUNTS`(=470@150ns) → `EPWM_setCounterCompareValue(...COMPARE_B...)`. **CMPB<TBPRD/2 엄수**(초과 시 shoot-through).
  - 요지: **메커니즘 둘(dead-band RED/FED vs CMPB 오프셋)·ns 소스 하나**, build-per-change(숫자만 바꿔 재빌드).
- **검증 방법(환원)**: flash 없이 RAM-load(OCRAM)→run + Saleae Logic2 4ch, **500MS/s(2ns 격자)**, **transition-based CSV export**(오프라인 수치분석 유리). dead-time=상보쌍 both-LOW 갭, shoot-through=both-HIGH 겹침. 샘플레이트=타임스탬프 격자 GCD 추정.
- **검증 결과(150·300ns 두 빌드)**: 4ch 100kHz±0.1% 상보 유지; dead-time 레그1 150.3→300.4ns(1.998×)·레그2 150.0→300.0ns(2.000×); **shoot-through 0**(양 빌드·양 레그); 레그1 RED=FED 대칭 확인. ⚠️ **+0.3ns 초과는 2ns 격자 양자화 바이어스**(floor 절삭/타이밍 오차 아님 — 30·60 정수라 절삭손실 0).
- **wiki 정합 메모**: 작업 지시는 "[[pwm]]/[[status]] dangling, 신설"이었으나 **디스크 확인 결과 둘 다 실존**(`roadmaps/pwm.md`·`status.md`, Obsidian이 파일명으로 해석) — 신설 아닌 기존 §dead-time 단일소스 절 확장으로 처리. P2도 △로 진척 반영.
- **갱신**: [[pwm]](§dead-time 단일소스 절 매크로·양 레그·검증표 확장, §검증 방법·결과 신설, P2 △·마일스톤·현재위치·사실·환원후보), [[status]](후속 해소·현황표·다음), [[pwm_pinmap]](dead-time 두 경로 단일소스 수렴 1줄), [[team_briefing_8kw]](로드맵 P1✓/P2△·보고포인트·§5), [[roadmap]](pwm 행), index.

## [2026-06-09] ingest | oled_tv_software — 패킷 크기 정정(54/43) + app_protocol 적출 + 정리트랙 추월 (esb 9be1a7a)

근거: c-oled_tv_software repo 코드 `9be1a7a`(esb). 코드 직접 확인 후 환원. 네 갈래:

1. **패킷 크기 사실 정정**: 내부 데이터 컨테이너 `rx_module_data_t`/`tx_module_data_t` 크기를 코드 static_assert(`_shared/oled_tv_protocol.h:237-238`) 기준 **rx 54B / tx 43B**로 정정. wiki에 62B/51B(canonical [[spi_packet_format]])·56B/45B(entity·source) 두 드리프트값 혼재 → 모두 코드값으로. wire는 불변 11B. 갱신: [[spi_packet_format]]·[[rx_control]]·[[rx_ble_module]]·[[esb_ptx_ack_assembly]]. (entity 교차참조의 "HDR 0xC0·20ms"도 정정 — 실제 HDR 0x10–12/0x50–52·10ms.) **코드 repo `CLAUDE.md:20`도 45B/56B로 낡음 → 별도 갱신 필요(메모, wiki 밖).** source 스냅샷(prd/manual/schematic)은 historical로 잔존, static_assert가 정본.
2. **정리트랙(spi-esb-refactor) 코드 추월**: R1~R3 부분 구현(공유 `_shared/oled_tv_protocol.{c,h}`+`pkt_build_*`/`pkt_apply_*`/`pkt_print_*`), R4(`SPI_PKT_*` 개명) 무효 — 코드는 이미 링크 중립 `PKT_HDR_*`. [[roadmaps/spi-esb-refactor]] 표·§5 갱신, [[roadmap]] §5·[[status]] 반영.
3. **새 트랙 — app_protocol 적출/핸드오프 (완료·검증)**: 01의 SPI 프로토콜을 `common.c/h`→`app_protocol.c/h`로 적출. 공개 API `protocol_loop()` 하나(내부 static `exchange_packets`/`print_packets`) + 전역 3개. 4파일 자립(common.h 역의존 끊음). W1=트랜스포트 직접 호출, D1=센싱/지령 전역 유지(비-SPI 호출처 무수정). 더미 한 줄 토글·모니터 상시 ON·LINK UP/DOWN 출력 제거(COMM 중복)·죽은코드(monitor_spi_diag/spi_ok_cnt/build_rx_to_tx_pkt/LOG_EN/tx_data_log) 삭제. main 루프 = `adc_proc()`+`protocol_loop()`. **STM32CubeIDE 실 빌드 + 실보드 동작확인 완료(✓).** 신규 [[app_protocol_module]], [[rx_control]] 메인루프 갱신, [[status]] 반영, Monitor_Loop(`175a8f7`) 주석 미결 해소.
4. **남은 후속(미착수)**: `_shared` 매크로 소유권 점검 — `PACKET_INTERVAL`(10ms)은 01만 호출(02/03 ESB 1ms 미사용)이라 SPI 전용 분리/개명(`SPI_PACKET_INTERVAL_MS`) 후보. [[roadmaps/spi-esb-refactor]] §6. (esb_crc=-1은 의도된 설계로 확정 — 점검 대상 아님.)

## [2026-06-09] ingest | 8kw-ev-wpt-tx — PWM P1 완료(4핀) + 레그2 두 모듈 SYNC 상보 설계 + dead-time 단일소스 #define

- **근거 커밋**: `6e6b342` (branch pwm). P1 = PWM 4핀(HS1/LS1/HS2/LS2) 전부 실보드 검증 완료.
- **LS2 = EPWM7_B @ J6.51 확정**: 이전 "핀 미확정"을 해소. UG Table 2-30(`ug:1640`) Mode0=EPWM7_B 일치(오기 없음) + **pinmux.csv 핀 F1=EPWM7_B 교차확인**. 펌웨어 배정 정본=silicon 채널.
- **회로도 net 라벨 함정 정확화**: 회사 회로도가 레그2 net을 채널이름 스타일 "EPWM4_B"(HS2)/"EPWM7_A"(LS2)로 라벨링 — 이 **suffix가 핀 노출 silicon 채널과 반대**(실제 EPWM4_A/EPWM7_B). HS2·LS2 동일 패턴. **정본=silicon 채널**, 라벨 suffix에 끌려가지 말 것([[adc_pinmap]] l/I 오기 동류).
- **레그2 두 모듈 SYNC 상보 설계(SDK 1:1 예제 없던 자리, 해결)**: EPWM4 syncout(ON_CNTR_ZERO)→EPWM7 syncin·phaseShift=0 위상정렬 + EPWM7_B AQ 반전 + CMPB 오프셋으로 상보+dead-time(레그1 dead-band 대신 CMP 오프셋). ⚠️ **함정: `CMPB=TBPRD/2−DT_COUNTS`(반드시 <TBPRD/2). +부호면 LS ON이 HS OFF 넘어 shoot-through** — 구현 중 1회 부호 오류 잡음.
- **dead-time 단일소스 #define 패턴(신규)**: `eta_pwm.h` `ETA_DEADTIME_NS` → `eta_pwm_init()`이 CMPB에 1회 적용, build-per-change(150↔300ns 실측). 레그2 적용, **레그1(EPWM2 dead-band) 미적용 → 향후 통일**(별도 세션).
- **게이트 극성**: active-high 가정으로 4핀 검증 통과(상보·dead-time·shoot-through 0) → **가정 실보드 실증, 회로도 원본 미확인**.
- **검증 실측치**: 100kHz, HS2 50%/LS2 47%, dead-time 150ns 양 edge, shoot-through 0 (Saleae 125MS/s, 13,421주기 전수 스캔). HS1 별도 99.997kHz/50%.
- **갱신**: [[pwm_pinmap]](표 4핀 확정·회로도 라벨 함정·LS2 EPWM7_B·게이트극성·SYNC 요약), [[pwm]](P1 ✓완료·Pin4 SYNC 설계절·dead-time 단일소스절·P2 레그1 통일잔여·블로커 해소·환원후보), [[status]](P1 완료·현황표·미결 재구성), index 2행.

## [2026-06-09] ingest | 8kw-ev-wpt-tx — PWM 핀맵 net/채널 분리 정정 + Pin3 HS2 실보드 검증 + EPWM 인스턴스·자유구동 사실

- **정정 대상**: [[pwm_pinmap]] "사용자 net 라벨" 컬럼이 **보드 net과 SoC 채널을 혼동**. J6.52 행을 "EPWM4_B"로 적었으나 — ① UG가 강제하는 SoC 채널은 **EPWM4_A**(Mode0/primary, `teams/g/lp-am263p/raw/lp_am263p_ug/ug_lp-am263p.md:1641`), ② J6.52에 라우팅된 **보드 net은 PWM_HS2**(레그2 HS 게이트, 사용자 도메인 확인). 펌웨어도 EPWM4_A hard `$assign`으로 실측 통과.
- **정정 방향**: 표를 **3단 모델(커넥터 핀 → SoC 채널 UG Mode0 → 보드 net)** 로 재구성, "EPWM4_B/EPWM7_A" 표기 제거. 이전 [2026-06-09 decision]의 "net 라벨 _B/_A vs 채널 반대" 프레이밍 자체가 net과 채널 혼동이었음 → 정정(net=PWM_HS2/LS2, 채널은 핀이 강제).
- **UG 교차확인**: J4.39=EPWM2_A(`:1600`), J4.40=EPWM2_B(`:1601`), J6.52=EPWM4_A(`:1641`), J6.51=EPWM7_B(Mode0)/EPWM5_B(Mode10)(`:1640`). 레그1·HS2는 UG·실측 정합.
- **Pin3 HS2 검증 환원**: EPWM4_A@J6.52 펌웨어 구현·실측 **99.998kHz/50%** → P1 진행 **1/4→2/4**(Pin1·Pin3 ✓, Pin2 LS1·Pin4 LS2 남음).
- **신규 reference 사실(검증 근거)**: ① **EPWM4는 EPWM2와 독립 인스턴스**(SysConfig 수용, base `CSL_CONTROLSS_G0_EPWM4_U_BASE`). ② **SysConfig 기본 EPWM = SYNC-in disable + phaseShift=0 → 자유구동** → 단일 모듈 핀은 위상기준 없이 독립 검증 가능(HS2 레그1 무관 토글 실증). 단 레그2 상보·dead-time(Pin4)은 EPWM4↔EPWM7 SYNC 명시 활성화 필요.
- **LS2 핀 미확정 명시**: 레그2 LS2는 **EPWM7 모듈만 사용자 확정**, 커넥터 핀 미확정 → J6.51은 "EPWM7 노출 UG 후보 핀"으로만 기재(검증된 사실 아님). Pin4 착수 시 호명.
- **갱신**: [[pwm_pinmap]](표 3단 재구성·net/채널 정정·EPWM 인스턴스 자유구동 절 신설·LS2 핀 미확정·source), [[status]](Pin3 검증·P1 2/4·미결 2항), [[pwm]](P1 표·Pin3/4 행·현재위치), index 2행.

## [2026-06-09] ingest | 8kw-ev-wpt-tx — PWM P1 Pin1(HS1) 구현·실보드 검증 + EPWM primary 패드 force_io 불요 정본

- **출처**: PWM P1 Pin1 = EPWM2_A → J4.39 (PWM_HS1) 실보드 검증.
- **검증 실측(Saleae Logic2)**: **99.997 kHz / duty 49.998%**(n=10223 cycles), 깨끗한 토글·글리치 없음. 100 kHz는 **브링업 임시값**(확정 주파수 pending — 추정 금지).
- **핀맵 정본↔실측 불일치 없음** — EPWM2_A@J4.39(UG Mode0) 그대로 동작. [[pwm_pinmap]] HS1 행에 "검증됨" 마킹.
- **신규 정본 [[am263p_epwm_primary_pad_no_force_io]]** (lp-am263p): EPWM 출력이 핀 **primary function**이면 SysConfig 핀먹스만으로 출력 버퍼 켜짐 → **force_io_enable 불필요**. force는 alt-function 패드(UART5=EPWM15)만 — [[am263p_iomux_force_io_enable]]와 **대조 짝**. 근거=Pin1 force 없이 출력. 판별=UG 핀먹스 Mode0(primary)인지 alt인지. + **검증법 환원**: OCRAM 이미지라 flash 없이 ccs-debug `loadProgram→run` + Saleae로 핀 측정(디버그 끊겨도 RAM 이미지 계속 실행) — dead-time build-per-change 튜닝에 유리.
- **P1 진행 1/4**: Pin1 ✓. 남음 = Pin2 LS1(EPWM2_B@J4.40, 레그1 dead-band 상보) → Pin3 HS2(EPWM4_A@J6.52) → Pin4 LS2(EPWM7_B@J6.51, 레그2 SYNC+위상오프셋).
- **확인 필요(미확정)**: ① 실제 스위칭 주파수 ② 레그2 두-모듈(EPWM4+EPWM7) SYNC+위상오프셋 상보·dead-time 구체 설계 — SDK 1:1 예제 없음, Pin4 착수 시 설계.
- **갱신**: [[pwm]](P1 △1/4·핀별 표·검증법·환원 후보), [[pwm_pinmap]](HS1 검증됨), [[status]](PWM 트랙·현황표 △), [[am263p_epwm_primary_pad_no_force_io]](신규), index 2건(concept 신규·pwm 진행).

## [2026-06-09] ingest | oled_tv_software — comm-state 판정 (T,N) 상수 통일·spi_status LINK/CRC 분리·COMM 라인 환원 (esb d2232fe)

- **근거 커밋**: `d2232fe`(esb, 2026-06-09) "feat(comm): 통신상태 판정 T/N 상수 통일 + 3칩 공통 COMM 라인". 코드 직접 확인 후 환원.
- **낡은 값 정정**: `BLE_COMM_ST_MIN_COUNT` 3→**20**(200ms 윈도우 기대 ~200개의 ~10%; `ESB_TX_INTERVAL_MS=1ms`). SPI는 `SPI_COMM_ST_TIMEOUT_MS=5000`→`SPI_COMM_ST_WINDOW_MS=1000`(개명·단축). 02/03 판정 코드 `delta >= MIN_COUNT` 확인.
- **새 모델**: comm-st 임계 = percent 자동계산 폐기, **각 링크 (T,N) 직접 상수**(헤더 한 블록). SPI=rolling-timeout(01만 소비, `MIN_COUNT=1`은 직접 미참조 문서값, 02/03 unused #define), BLE=윈도우 카운트(02·03 소비).
- **spi_status LINK/CRC 분리**: 01의 `spi_status`가 LINK 전용(토글 타임아웃)으로 분리, CRC는 1초 윈도우 fail로 별도(이전 `e5e3efc` 통합을 환원). diff: `spi_proc()`에서 ok/CRC-fail 시 `spi_status` 적던 두 줄 제거.
- **3칩 공통 COMM 라인**: `pkt_print_comm_line(spi_link,spi_crc,esb_link,esb_crc)` in `_shared/oled_tv_protocol.c`. 출력 `COMM | SPI:{L}{C} ESB:{L}{C}`(1=up/ok,0=down/err,-=N/A). 함수는 칩 무지. **현재 01만 호출**(common.c:200), SPI down이면 ESB 전부 stale `--`.
- **보류·미구현 표기**: 02/03 COMM 라인 미와이어링(unused), ESB CRC는 HW CRC 보증으로 SW 검증 안 하기로 결정(자리는 `-`).
- **재확인(불변)**: race-free stamp 설계(02가 `spi_tx_pkt`에 `SPI_Loop` 송신 직전 stamp, `pkt_build_tx` extra_d0 아님) — d2232fe가 02 미수정, 기존 기록 정확.
- **갱신**: [[comm_state_monitoring]](frontmatter date·심볼표·판정식·(T,N)모델 신설·LINK/CRC분리 신설·COMM라인 신설·보류절), [[status]](다음 시작점·구현현황 2행·BLE행·미결 2항), [[roadmap]](§3·§5 후속 N=20 반영), [[spi_link_reliability]](단절판정·경고출력 LINK/CRC 분리), index.

## [2026-06-09] decision | 8kw-ev-wpt-tx — PWM 레그2 suffix UG 기준 확정 + 레그2 한 모듈 묶기 향후 요청 기억

- **사용자 결정 1 — A/B suffix는 UG 기준**: 레그2 구현 채널 = EPWM4_A@J6.52, EPWM7_B@J6.51로 확정(schematic net 라벨 _B/_A와 반대지만 핀이 강제). [[pwm_pinmap]] "확인 권장" 헤징 제거 → 확정.
- **사용자 결정 2 — 레그2 두 모듈은 의도된 현 설계, 단 향후 수정**: 현 회사 회로도가 레그2(HS2/LS2)를 EPWM4+EPWM7 두 모듈에 라우팅한 것은 의도적. **사용자가 회로도 수정 요청 기회가 생기면 한 EPWM 모듈로 묶도록 요청할 계획** → 그때 상기시킬 것.
- **기억 저장**: 영구 메모리 `project_8kw_pwm_leg2_revision.md`(project type) 신규 + MEMORY.md 포인터. wiki [[pwm_pinmap]] §향후 보드 개선 + [[pwm]] §6 환원/개선 후보에도 기록.
- **갱신**: [[pwm_pinmap]](§핵심·§향후 보드 개선·§미확인), [[pwm]](§5·§6), [[status]](미결 reframe), [[team_briefing_8kw]]. PWM 상태 = 핀맵 확정·P1 착수 대기(불변).

## [2026-06-09] resolve | 8kw-ev-wpt-tx — PWM 핀맵 확정 (J4.38→J4.39 정정 + UG 교차확인) → P1 착수 가능

- **사용자 정정**: J4.38은 오기, 실제 **J4.39**(EPWM2_A=PWM_HS1). → 레그1이 UG와 완전 일치(EPWM2_A@J4.39, EPWM2_B@J4.40)하며 **UG 표 신뢰성 검증**.
- **확정 핀맵([[pwm_pinmap]])**:
  - 레그1 = **EPWM2 단일 모듈**: EPWM2_A=HS1@J4.39, EPWM2_B=LS1@J4.40.
  - 레그2 = **EPWM4+EPWM7 두 모듈**: EPWM4_A=HS2@J6.52, EPWM7_B=LS2@J6.51.
- **A/B suffix 정리**: 레그2에서 사용자 net 라벨(_B/_A)과 silicon 노출 채널(_A/_B)이 반대. 물리 핀이 노출하는 채널은 J6.52=EPWM4_A뿐·J6.51=EPWM7_B(Mode0)뿐이라, **구현 기준은 UG 채널**(EPWM4_A@J6.52, EPWM7_B@J6.51). net 이름에 끌려가지 말 것.
- ★ **레그2 두 모듈 함의**: J6.51이 EPWM4_B를 노출 안 해 한 모듈로 못 묶음 → 레그2 상보·dead-time은 모듈 내 dead-band 불가, **EPWM 동기(SYNC)+위상 오프셋**으로 생성(레그1 단일모듈 dead-band와 비대칭). dead-time 튜닝 경로도 레그1=레지스터/레그2=오프셋으로 다름. 비표준이라 설계 의도 재확인 권장(보드 라우팅은 고정).
- **인스턴스 3개**: EPWM2/4/7. UART5(EPWM15) 무충돌.
- **상태 변화**: 직전 correction(핀맵 UG 불일치·P1 차단) → **해소**. 핀맵·토폴로지·dead-time(150ns build-per-change) 확정 → **P0 대부분 해소, 다음 착수 = P1**. 잔여 = 주파수 확정값·보호신호.
- **갱신**: [[pwm_pinmap]](확정 표·레그2 두모듈 함의), [[pwm]](§0·§1·§2·§3·§5 P1 착수), [[status]](PWM 트랙 P1·현황표·미결), [[team_briefing_8kw]](다이어그램·다음주 보고=P1), index 2건.

## [2026-06-09] correction | 8kw-ev-wpt-tx — PWM 핀맵, UG 교차확인서 불일치 발견 → "확정" 철회·확인 필요

- **정정 대상**: 직전 PWM 핀맵 "확정" entry. **UG 핀먹스 표([[lp_am263p_ug]] Table 2-28 J4 / 2-30 J6) 교차확인 결과, 사용자 제공 4핀 중 3핀 불일치** → 정본 [[pwm_pinmap]]을 "확인 필요"로 다운그레이드.
- **사용자 정정 입력**: J6.51 = **EPWM7_A** (직전 EPWM&_A 오타 → 내가 EPWM4_A로 잠정기입한 것 정정).
- **UG 교차확인 결과**:
  - J4.38: 사용자=EPWM2_A인데 **UG는 EPWM1_B(Mode0)/EPWM4_B(Mode10)** — EPWM2_A는 UG상 **J4.39**(off-by-one 의심).
  - J4.40: 사용자=EPWM2_B, **UG=EPWM2_B ✅ 유일 일치.**
  - J6.52: 사용자=EPWM4_B인데 **UG=EPWM4_A**(J6.52엔 _B 없음).
  - J6.51: 사용자=EPWM7_A인데 **UG=EPWM7_B(Mode0)/EPWM5_B(Mode10)**(J6.51엔 _A 없음).
- **UG-consistent 가설 reading(미확정)**: HS1=EPWM2_A@J4.39, LS1=EPWM2_B@J4.40, HS2=EPWM4_A@J6.52, LS2=EPWM7_B@J6.51. → 이 경우 **레그2가 EPWM4(HS)+EPWM7(LS) 서로 다른 모듈**에 걸쳐 모듈 내 dead-band 불가, 동기체인+위상으로 dead-time 생성 필요(레그1 EPWM2 단일모듈과 비대칭). 인스턴스 2개(EPWM2/4)→**3개(EPWM2/4/7)** 가능성.
- **조치**: [[pwm_pinmap]]에 reconcile 표(사용자 vs UG Mode0/Mode10) + 확인 필요 명시. [[pwm]]·[[status]]·[[team_briefing_8kw]]·index에서 "핀맵 확정→P1 착수"를 "핀맵 reconcile 선결→그 후 P1"로 정정. 게이트 구동 핀이라 확정 전 SysConfig 배정 금지.
- **확정 스펙(불변)**: 풀브리지 4채널·주파수 고정형(값 미정)·dead-time만 가변(build-per-change, 시작 150ns)·UART5(EPWM15) 무충돌·P4서 ADC 트리거 RTI→EPWM 전환.
- **사용자 호명 필요**: 핀번호 off-by-one(J4.38↔39)인지 / A·B suffix 표기 혼동인지 / 다른 핀 넘버링 기준인지 reconcile.

## [2026-06-09] ingest | 8kw-ev-wpt-tx — PWM 핀맵·스펙 확정 (사용자 제공) → P0 대부분 해소, P1 착수 대기

- **출처**: 사용자 제공 PWM 핀맵·스펙 (2026-06-09).
- **신규 [[pwm_pinmap]]**: 풀브리지 인버터 4채널 — J4.38 EPWM2_A=PWM_HS1, J4.40 EPWM2_B=PWM_LS1, J6.51 EPWM4_A=PWM_LS2, J6.52 EPWM4_B=PWM_HS2. **EPWM2=레그1, EPWM4=레그2.** ⚠️ **A/B↔HS/LS 매핑이 인스턴스별 반전**(EPWM2 A=HS, EPWM4 A=LS) → 레그별 상보 극성·dead-time 다르게 설정. ✅ **UART5(EPWM15) 무충돌**(이전 P0 선결 충돌 점검 해소).
- **스펙**: 스위칭 주파수 **고정형**(값 미정·런타임 가변 아님). **dead-time만 가변** — 리얼타임 변경 불필요, **값 바꿀 때마다 새 빌드(build-per-change)**, **시작 ≈150ns**. duty 등 기타 미정.
- **ADC 트리거 향후 계획**: 현재 ADC=RTI1 트리거 유지. **PWM 완료 후 ADC SOC 트리거를 RTI→EPWM으로 전환 예정**(P4). 전력제어 표준(PWM 주기 특정 시점 샘플). 지금은 RTI 그대로.
- **사실/가설/모름 갱신**: 토폴로지·채널·핀·dead-time 방식·UART5 무충돌 = **사실 승격**. LCC 탱크 = 가설 유지. 주파수 확정값·보호신호 소스·게이트 극성 = 모름(P0 잔여, 단 주파수 고정형이라 P1은 임시값 진행 가능).
- **갱신**: [[pwm]](§1 사실/가설/모름·§2 마일스톤 P0 △/P1 다음착수·§3 단계·§5 블로커), [[status]](PWM 트랙 P1 착수·현황표·미결), [[team_briefing_8kw]](PWM 다이어그램·확정 스펙·다음주 보고 포인트=P1), index 2건(pwm.md 갱신·pwm_pinmap 신규). **다음 착수 = P1**(EPWM2/4 4채널 기본 출력, dead-time 150ns, 오실로 검증).

## [2026-06-09] plan | 8kw-ev-wpt-tx — PWM 전력제어 작업 호(P0~P4) 신규 등록 (미착수)

- **계기**: ADC 계측(A2) 완료 후 다음 작업으로 PWM 구현 추가 지시. roadmap.md가 예고한 후속 작업(PWM)을 정식 작업 호로 승격.
- **신규 [[pwm]](roadmaps/pwm.md)**: P0(요구사항·핀맵 확정)~P4(ADC 피드백 제어루프) spine. 전부 미착수(✗). **사실/가설/모름 가름** 명시 — 사실(AM263P EPWM 보유, UART5가 EPWM15 점유 중), 가설(LCC 공진형 토폴로지·~85kHz SAE J2954, ADC `I_LCC_SEN` 단서), 모름(인버터 구조·채널 수·주파수·dead-time·위상·보호신호 = P0 스펙 입수 필요). 추측으로 채우지 않고 "확정 필요"로 남김.
- **P0 핵심 선결**: ① 토폴로지·채널·주파수·dead-time·보호신호 스펙 입수 ② **EPWM15(UART5 점유)와 PWM 채널 핀 충돌 회피** ③ 물리 인스턴스/핀 처음부터 hard `$assign`(ADC soft 재셔플 함정 회피).
- **갱신**: [[roadmap]](task 표 pwm 행 추가·현재 위치 "다음 활성 트랙=PWM"), [[status]](다음 작업 PWM 트랙 선두 배치·현황표 PWM 행·미결 P0 스펙), [[team_briefing_8kw]](작업 호 다이어그램 PWM·다음 작업·다음주 보고 포인트 PWM 착수), index 1행 추가. 외부 업무보고(`eta/업무보고_2026-06-09.md`)도 PWM 다음 작업 반영.
- **위치**: ADC A3가 센서 스펙 대기로 막혀 있어 PWM이 다음 진행 트랙. PWM 스펙과 센서 스펙을 함께 확보하면 두 트랙 동시 해소.

## [2026-06-09] briefing | G팀 주간 업무보고 준비 — lp-am263p briefing 갱신 + 8kw briefing 신규

- **목적**: 주간 팀 보고용 참고 페이지를 다음주 diff 가능하게 정비. 외부 보고서 파일은 wiki 밖(`C:\Users\echog\eta\업무보고_2026-06-09.md`)에 작성, wiki에는 보고 준비용 briefing을 둠.
- **[[team_briefing]] 갱신(lp-am263p)**: 6/2 상태(S6 "SPI 무응답"·원인 미상)→6/9 상태(R35~R38 계측으로 MCU 마스터 정상 입증+카드 NP 전 출력핀 침묵 입증→"NP 코어 미실행" 확정, 1순위 의심=40MHz XTAL Y1 미발진 추론, R39 오실로 측정 예정)로 갱신. **"보고 스냅샷 이력" 표 신설**(주차별 위치·핵심·다음계획 + 다음주 보고 포인트). S3는 과거 해결 사례로 보존. R35 "클럭 0회=샘플링 아티팩트(12.5→125MS/s)" 문제·해결 기록.
- **[[team_briefing_8kw]] 신규(8kw)**: 동일 구조(보고 스냅샷 이력·작업호 A0~A4·진행/문제표·현재위치·다음). 6/9 = ADC 6채널 완성·실보드 검증, 만난 문제표(트리거 결선 `enableIntr0`·soft 재셔플), 막힘=A3 센서 스펙 대기·UART5 차동 미동작.
- **갱신**: index 2건(lp briefing 설명 갱신 + 8kw briefing 신규행), 두 briefing 상호 백링크.
- **다음주 보고 시작점**: 각 briefing "보고 스냅샷 이력" 표 마지막 행 + "다음주 보고 포인트"부터 이어서 작성.

## [2026-06-09] update | 8kw-ev-wpt-tx — A2 완료: 6채널 ADC 실보드 검증 + AIN hard assign + eta_adc.c 테이블 리팩토링 (c512e3b)

- **출처**: branch `adc` commit `c512e3b`(origin/adc) — 6채널 ADC 완성·실보드 검증. 같은 날 앞선 4채널 update에 이어 6/6 달성.
- **A2 완료(6/6, 실보드 검증)**: 신규 2채널 추가 = Temp_Module1(ADC2 SOC0 AIN0 J3.25, int_xbar OUT_3/IRQ149), GA_Vin(ADC3 SOC0 AIN0 J3.26, OUT_4/IRQ150). 물리 인스턴스 **5개(ADC0~ADC4)** 사용. ADC1만 SOC0+SOC1 라운드로빈(SOC1 EOC 단일 ISR 2채널 수확), 나머지 SOC0 단독. RTI1 1 kSPS 공유. 6채널 raw→mV 변환 경로 실보드 검증.
- **AIN 핀 hard `$assign` 승격 (soft 재셔플 리스크 해소)**: 직전(b8b0ad8)까지 물리 인스턴스만 hard, AIN 핀은 soft `$suggestSolution`이었음. 신규 채널 추가 시 솔버 재셔플 방지 위해 **AIN 핀까지 전부 `$assign` hard 승격** → 재생성 후 물리 배정 ADC0~4 유지(재셔플 없음) 확인. [[am263p_syscfg_soft_vs_hard_assign]] 규칙의 실증 사례.
- **리팩토링 — eta_adc.c 테이블 주도화**: 인스턴스별 ISR 5개·init 5블록·loop 5블록(차이=베이스/결과주소·IRQ·ready플래그·SOC→채널)을 → 인스턴스 테이블 `g_eta_adc_inst[]` + 공용 `eta_adc_eoc_isr()` + 인덱스 루프로 통합. **332→232줄**, 동작·핀맵·IRQ 불변. 채널 추가 = enum 1행 + 테이블 1행(`ETA_ADC_CH_COUNT` 일원화). 단 `eta_uart5.c` 출력은 채널별 `DebugP_log` 하드코딩이라 출력 라인은 수동 추가 필요.
- **미해결 유지**: ① A3 센서 스케일링 — mV→물리량 변환 스펙 미입수(블로커). ② UART5 차동 송신 — 6채널 출력은 UART0 콘솔로만, UART5 `UART_write` 주석 + RS-485 DE/485_EN(THVD1400) 미구현.
- **다음 시작점**: A3 스케일링(스펙 대기) / UART5 차동 복구 / A4 교차검증.
- **갱신**: [[status]](전면, A2 ✓), [[adc]](A2 ✓·6채널 표·리팩토링), [[adc_pinmap]](6채널·int_xbar 열·AIN hard), [[roadmap]](A2 완료), [[am263p_syscfg_soft_vs_hard_assign]](AIN hard 승격=리스크 닫음), [[am263p_adc_instance_allocation]](8kw 5인스턴스), [[am263p_adc_rti_trigger]](6채널 확장 경과), index 3건.

## [2026-06-09] update | 8kw-ev-wpt-tx — 코드 진척 반영 (단채널→4채널, UART 주기화 완료, eta_bsp 레이어, UART5 차동 여전히 미동작)

- **출처**: branch `adc` 커밋된 상태(워킹트리 clean) 코드/git/사용자 확인 delta. wiki가 2026-06-05에 머물러 있어 역산 갱신.
- **소스 레이아웃 정정**: `src/bsp/` → **`src/eta_bsp/`**(eta_ 접두 디렉토리까지). 파일 `eta_adc.{c,h}`·`eta_uart5.{c,h}`, eta_ 접두 + _loop 접미 컨벤션. eta_bsp 레이어 도입(a655de4, edddc31).
- **ADC 단채널→4채널(목표 6, 4/6)**: TEMP_MODULE2(ADC1 SOC0 AIN0 J3.24 IRQ146), I_LCC_SEN(ADC4 SOC0 AIN0 J3.27 IRQ148), I_COIL_SEN(ADC0 SOC0 AIN1 J3.28 IRQ147), GA_IIN_SEN(ADC1 SOC1 AIN1 J3.29 IRQ146 SOC1 EOC). ADC1 SOC0+SOC1 라운드로빈→SOC1 EOC 단일 ISR 2채널 수확. 트리거 RTI1(syscfg `CONFIG_RTI0`) 1 kSPS 3인스턴스 공유. ISR raw 저장, `eta_adc_loop` `(raw*3300)/4095` 정수 mV(out-param, 88d9deb). 인스턴스 hard `$assign`(b8b0ad8)이나 **AIN 핀은 아직 soft** = 잔존 리스크.
- **UART 1초 주기화 완료**: RTI2 독립 타이머(syscfg `CONFIG_RTI1`) compare0 ISR→flag→`eta_uart5_loop`(8b85bda). 주기=SysConfig `nsecPerTick0=1e9` 단일 진실원천(#define 아님). 현재 출력은 UART0 콘솔(`DebugP_log`) 4채널 ASCII.
- **UART5 차동 송신 여전히 미동작**: `snprintf`+`UART_write` 블록 통째 주석(`eta_uart5.c:159-170`) → 시도조차 안 함. RS-485 DE/485_EN(THVD1400 U13) 미구현(src `485`/`DE`/`THVD` 0건). TX force-enable(IOMUX)은 살아있음(TXD=EPWM15_A=J1.4). PADCONFIG `0x53100124` 런타임 read 미수행. → soft 재배치 점검(2026-06-09 예정분) 결론: UART5는 soft 아님 확정, 원인=UART_write+RS-485.
- **A3 블로커 유지**: 센서 스펙 미입수, mV→물리량 변환 코드 전무.
- **다음 시작점**: ① 남은 2채널(Temp_Module1 J3.25 ADC2, GA_Vin J3.26 ADC3) → 6채널 ② AIN 핀 hard `$assign` 검토 ③ UART5 차동 복구(UART_write 주석 해제+RS-485 DE 구현) ④ A3(스펙 대기).
- **갱신**: [[status]](전면), [[adc]](A0~A2 상태·src 경로·4채널 표), [[adc_pinmap]](SOC/IRQ/구현 열), [[roadmap]](현재 위치), [[am263p_iomux_force_io_enable]](UART_write 주석·RS-485 결론), [[am263p_syscfg_soft_vs_hard_assign]](UART5 해소·AIN soft 잔존), [[am263p_adc_rti_trigger]](4채널 확장 경과), index 4건. **주의**: 4채널 실보드 전압 재검증 미문서화 → 보드 검증 완료로 단정 안 함(△).

## [2026-06-08] ingest | lp-am263p — ADC 인스턴스 배치 보강 + SysConfig soft/hard 물리배정 정본 (8kw J3.27/J3.28 작업·실보드 검증)

- **출처**: 8kw-ev-wpt-tx adc 브랜치 commit `b8b0ad8` — J3.28/J3.27 ADC 핀 추가 작업 + 실보드 검증. AM263P 플랫폼 공통 지식이라 lp-am263p concept으로, [[am263p_adc_rti_trigger]] 자매.
- **페이지 A (개명+보강)**: 직전 `am263p_adc_instance_placement` → **[[am263p_adc_instance_allocation]]** 개명(`git mv`). 보강분: 각 인스턴스=독립 SAR(자체 S/H·시퀀서·결과레지스터·ADCINT), 마지막 SOC EOC에서 coherent read, 8kw 현황(ADC1=Temp_Module2 SOC0+GA_Iin_SEN SOC1, 1 ISR=IRQ146 / ADC0=I_COIL_SEN·ADC4=I_LCC_SEN 별도), **사실/가설/모름 가름**(아키텍처=사실, △변환시간 예산 수치 미산정, △다중 인스턴스 동시 RTI 트리거 정밀 동시성 미실측).
- **페이지 B (신규)**: **[[am263p_syscfg_soft_vs_hard_assign]]** — SysConfig 논리 `$name`≠물리 페리페럴. 물리 배정이 soft(`$suggestSolution`)면 새 인스턴스 addInstance 시 솔버가 기존 배정까지 reshuffle.
  - **관찰 사고(2026-06-08, J3.27 추가)**: ADC4 추가 순간 솔버가 `CONFIG_ADC0`→물리 ADC2, `CONFIG_ADC4`→물리 ADC0으로 밀어냄. ADC AIN은 물리에 1:1 고정 → **엉뚱한 핀을 읽음**. 증상=ISR·변환 정상인데 인가전압 미추종(가장 헷갈리는 함정, 죽은 게 아님). "J3.27 추가 전 J3.28 동작"이 reshuffle-on-add 방증.
  - **부분수정 안 됨**: int_xbar 소스(`ADCx_INT1`)·base·AIN은 모두 물리 기준. int_xbar만 맞추는 우회는 핀 여전히 틀림.
  - **수정(✓실보드 검증)**: hard `ADC.$assign="ADCn"`(+AIN→ADCn_AINx). 물리 맞으면 base·int_xbar 자동 정렬, C코드 무수정. 검증=`ti_drivers_config.h` `CONFIG_ADCn_BASE_ADDR`==의도 `CSL_CONTROLSS_ADCn_U_BASE`+실보드.
  - **일반화**: 보드배선 고정 모든 페리페럴은 처음부터 hard `$assign`.
  - **△ 후속**: UART5도 같은 soft 재배치인지 점검 후보 — 단 TXD 패드 P15 정상 생성 기확인이라([[am263p_iomux_force_io_enable]]) RS-485 트랜시버 DE/485_EN가 유력. **2026-06-09 점검 예정**.
- **갱신**: [[am263p_adc_rti_trigger]] §3·관련페이지에 두 자매 백링크 추가. [[adc_pinmap]] 헤더 백링크 2건. index 2줄(allocation 개명행 보강 + soft/hard 신규행). 두 페이지 상호 백링크.

## [2026-06-08] ingest | oled_tv_software — BLE(ESB)_Comm_St 구현 완료 환원 + 코드 어긋난 기록 정정

- **출처**: 커밋 `6cd7e6c` (esb 브랜치), 실보드 양방향 검증 완료.
- **새 사실 — BLE_Comm_St 구현됨**: `COMM_ST_BIT_BLE`(0x10 bit6). 판정 = **presence 리셋 윈도우** — 최근 `BLE_COMM_ST_WINDOW_MS=200` 내 수신 delta ≥ `BLE_COMM_ST_MIN_COUNT=3`이면 alive. 노드별: **02_RX_ble**(PRX) `esb_rx_cnt` delta→bit6 적재→STM32 전달; **03_TX_ble**(PTX) `esb_ack_cnt` delta→자기 LED3만; **01_RX_control** bit6→`ble_comm`→`esb \| LINK UP/DOWN` 콘솔. 각 nRF가 자기 수신으로 독립 판정(02→03 verdict 못 보내 03이 ACK로 우회). 심볼 `ble_comm_st_*` ↔ `spi_comm_st_*` 대칭. throughput 아닌 presence("오긴 오나")로 합의, N=3 헐거움.
- **race-free 교훈(실보드 플래핑으로 발견)**: wire 상태비트(bit5/6)는 공유 RX 버퍼 `esb_pkt[0]`이 아니라 **송신 복사본 `spi_tx_pkt`에 `SPI_Loop` 송신 직전 stamp**. ESB RX ISR이 0x10 수신마다 `esb_pkt[0]`을 memcpy로 덮어 race→01 LINK 플래핑(49→30→0/30s). bit5는 5초 freshness로 가려졌고 즉시 읽히는 bit6만 표면화. 판정과 wire 적재 분리가 race-free 자리. → [[comm_state_monitoring]] "race-free stamp".
- **코드와 어긋난 기록 정정**: ① `ble_link` 심볼은 코드에 없음(기존 "03 ble_link 항상 0" 폐기, 실제=`ble_comm_st_bit`/`ble_comm`). ② **ESB wire 주기 = `ESB_TX_INTERVAL_MS=1ms`**(기존 "10ms"는 SPI `PACKET_INTERVAL` 혼동 오기 — [[esb_packet_format]]·[[esb_link_layer]] 정정). ③ ESB CRC는 SDK가 콜백 전 검증·폐기(`CRCSTATUS==0`)→`NRF_ESB_EVENT_RX_RECEIVED`는 CRC-valid only. ④ free-run heartbeat 설계(구 `b84b31b`, 03이 bit6 더미 토글)는 완전 폐기(03 `g_hb` 제거, `pkt_build_tx` extra_d0=0). ⑤ bit5 적재 위치도 `ESB_Loop` 인라인→`spi_tx_pkt` stamp로 정정.
- **LED**: LED3 = `ble_comm_st_bit` 미러, `LED3_PIN/ON/OFF` 매크로 수동 교체(보드별 빌드 config 폐기). 체크인 기본 DK P0.19(active-low), 회사보드 P0.06(active-high) 주석.
- **갱신**: [[comm_state_monitoring]](판정식·노드표·설계근거·race-free 절·폐기기록), [[spi_link_reliability]](bit5 stamp·ESB 1ms), [[esb_packet_format]]·[[esb_link_layer]](1ms·CRC-valid), [[tx_ble_module]](LED3 매크로), [[status]](다음=N튜닝·LED3 전환, ESB 표 3행), [[roadmap]](환원후보 완료), index 4건.
- **남은 일**: N=3 임계 실 RF 수신율 대비 튜닝(STM32 모니터 rx `LOG_EN` 게이트), 회사보드 LED3 P0.06 전환, Warning/Fault·PWM 차단 상태머신(별트랙).

## [2026-06-08] ingest | lp-am263p — AM263P ADC 인스턴스 배치 설계 규칙 정본 (8kw ADC0 추가에서 도출)

- **출처**: 사용자 제공 설계 규칙 (8kw ADC0 인스턴스 추가 작업 중 정리). 플랫폼 설계 지식이라 lp-am263p에 정본, 8kw `adc_pinmap` 백링크.
- **생성**: [[am263p_adc_instance_allocation]] (lp-am263p concept; 최초 파일명 `_placement`, 2026-06-08 후속 ingest에서 `_allocation`으로 개명·보강) — [[am263p_adc_rti_trigger]] 형제.
  - **전제 교정**: 멀티 ADC 인스턴스는 **표준·정상** 사용법(ADC0~4 존재 이유=동시 다신호 캡처). 비안정 아님. 차이는 안정성 아닌 ①동시성 ②펌웨어 복잡도.
  - **HW 사실**: 한 인스턴스 다중 SOC=**직렬**(SAR·S/H 1개 → 채널 스큐 + 변환시간 합이 트리거 주기 안에 들어와야). 다른 인스턴스=**병렬**(공통 트리거에 동시 샘플, 스큐 없음).
  - **결정 규칙**(안정성 아닌 신호 특성 기준): 상관·고속(V·I 쌍·코일/입력 전류, 제어루프) → 인스턴스 분산+공통 트리거. 무상관·저속(온도) → 한 인스턴스에 몰고 마지막 EOC 인터럽트 1개.
  - **복잡도 비용**: 인스턴스 +1 = +ISR 1·+int_xbar 라우팅 1·+ready flag 1 (8kw ADC0가 이 비용). "무상관 신호 한 인스턴스에 먼저 채우기"는 복잡도 tiebreaker(안정성 아님).
  - **유일한 실제 instability**: SOC 변환시간 합 > 트리거 주기 → 결과 밀림/덮어씀. 멀티 인스턴스 분산으로 해소.
  - **8kw 적용 메모**: PCB 라우팅이 배치 고정. 현 ADC1=Temp_Module2+GA_Iin_SEN 동거(입력 전류가 온도와 직렬) → 현 보드는 그대로 운용, 다음 보드는 입력 전류를 GA_Vin과 동시 샘플 가능하게 별도 인스턴스 검토.
- **갱신**: [[adc_pinmap]] 헤더에 배치 근거 백링크 추가. index 1건.
- **부가 정정**(직전 별건): 8kw ADC 핀맵 `GA_lin_SEN`→`GA_Iin_SEN`(입력 전류, GA_Vin의 짝) 오타 정정 — adc_pinmap·roadmaps/adc·status·index 라벨/설명 통일.

## [2026-06-08] ingest | lp-am263p — AM263P IOMUX PADCONFIG force_io_enable 정본 (UART5 사례, 8kw 미동작 조사)

- **출처**: 코드·헤더 교차검증 — `pinmux.h:93-100`(force 매크로), `pinmux.c:56-58,85-100`(KICK 매직값·plain-write), `cslr_soc_baseaddress.h:416`(IOMUX base 0x53100000), `cslr_iomux.h:395-396`(KICK offset), `pinmux.h:222-223`(EPWM15 offset), lp-am263p `evaluations/uart5/empty.c:52-88,107-113`(loopback force_io), 8kw `src/eta_bsp/eta_uart5.c:64-94,121-122`(TX 전용 force_io), 두 프로젝트 `ti_pinmux_config.c:42-51`(syscfg 생성 PADCONFIG).
- **생성**: [[am263p_iomux_force_io_enable]] (lp-am263p concept) — 플랫폼 정본. AM263P ADC·flash 정본과 동일하게 **플랫폼 지식은 lp-am263p, 8kw는 백링크** 패턴.
  - **확정**: ① PADCONFIG OE/IE override 2비트 필드(OUTPUT [7:6], INPUT [5:4]), `01`=force-enable/`11`=disable/`00`=IP default. ★OE/IE active-low 아님 — 켜려면 `|=0x40` OR-set(타 TI SoC 직관과 반대). ② SysConfig는 override를 `00`으로 남기고 `Pinmux_config()`는 plain write(`CSL_REG32_WR`, RMW 아님) → syscfg 단독으론 alt-function 패드 버퍼 절대 안 켜짐. KICK 언락 후 PADCONFIG RMW(force_io_enable) 필수. ③ 좌표: IOMUX base 0x53100000, UART5_TXD=EPWM15_A=P15=0x124(절대 0x53100124), RXD=EPWM15_B=R16=0x128.
  - **일반화**: UART5는 발견 경로일 뿐, EPWM15를 alt-func로 빌려 쓰는 모든 패드(및 다른 alt-function 패드)에 동일 적용.
  - **8kw 결론**: UART5 미동작은 펌웨어 IOMUX 원인 **아님** — 8kw TX force-output-enable이 검증된 lp-am263p 예제와 byte-identical. 다음 의심 = IOMUX 밖 THVD1400 RS-485 트랜시버(U13) DE/485_EN 핀.
  - **미검증**: P15 PADCONFIG 런타임 전체 비트 분해(bit6 OE set만 확인, JTAG로 0x53100124 직접 read해 기대값 `0x541`=syscfg `0x501`|`0x40` 확정 필요). EPWM15 패드 IP default=buffer-disabled는 SDK 예제 주석 근거이며 TRM 리셋값 미확인.
- **8kw 갱신**: [[status]] 미결에 "UART5 실보드 송신 미동작·펌웨어 원인 배제·RS-485 트랜시버 의심" 추가. index 1건.

## [2026-06-08] ingest | oled_tv_software — SPI_Comm_St 구현 완료 환원 (심볼 통일 + LED2 mirror, 실보드 검증)

- **출처**: 커밋 `e5e3efc` (refactor(comm): SPI/BLE_Comm_St 심볼·네이밍 통일 + LED2 mirror), esb 브랜치, 실보드 검증 5/5 PASS (LED2 blink, spi LINK UP/DOWN 콘솔).
- **비트 의미론**: 0x10 `Data[0]` 한 바이트가 두 성격 혼재 — bit0~4=TX 보드 물리 상태(진짜 tx_status), **bit5/6=통신 링크 heartbeat 상태(TX 보드 상태 아님, 0x10에 함께 실릴 뿐)**. 이 구분이 매크로 prefix 분리 근거.
- **심볼·네이밍**: `TX_STATUS_BIT_SPI_COMM_ST`→`COMM_ST_BIT_SPI`(BLE도 동일). `hb_*`→`spi_comm_st_*`(`Heartbeat_Loop`→`SpiCommSt_Loop`), `SPI_HB_TIMEOUT_MS`→`SPI_COMM_ST_TIMEOUT_MS`(값 5000 유지), 3종 펌웨어 통일. **모니터 라벨 문자열 `"SPI_Comm_St"`/`"BLE_Comm_St"`는 문서 표시명이라 유지 — 심볼명≠라벨**. bit5 적재 위치 정정: `build_tx_pkt()` 아니라 `02_RX_ble ESB_Loop()`의 0x10 보관 직후 인라인 clear+set.
- **spi_status 통합**: heartbeat timeout(5000ms 무변화) + CRC fail 두 FAIL 경로를 단일 `spi_status`로 (LINK UP/DOWN).
- **LED**: `tx_ble_module` LED2(P0.08)=`spi_comm_st_bit` mirror로 확정(200ms 외형 동일, 비트값 미러). LED3=`BLE_Comm_St` mirror(직전 확정).
- **갱신**: [[comm_state_monitoring]](Data[0] 이중성격 표·심볼 컨벤션 표·구현현황 5/5), [[spi_link_reliability]](heartbeat 심볼 통일·적재위치 정정·LED2 row), [[tx_to_rx_packets]](0x10 bit5/6 의미 구분·심볼명), [[tx_ble_module]](LED2 mirror), [[status]](다음 시작점=ESB 차례·SPI 완료·미결 정정), index 1건.
- **남은 일**: Warning/Fault 플래그·PWM 차단 상태 머신 미구현(범위 밖). BLE(ESB)_Comm_St CRC 도착윈도우 구현이 다음 차례.

## [2026-06-08] update | oled_tv_software — Comm_St 정리: SPI는 heartbeat 유지, ESB만 CRC 재정의

- **계기·경과**: 사용자가 Comm_St 의미를 "칩 생사" → "통신 생사(CRC)"로 재고. 1차로 SPI/ESB 둘 다 CRC 재정의했으나, 사용자가 **공식 프로토콜 문서 260513이 SPI_Comm_St를 200ms 교번 heartbeat로 명시**함을 지적 → **SPI는 heartbeat 유지로 철회**, ESB만 재정의로 정정.
- **확정(사용자 결정 2026-06-08)**:
  - **SPI_Comm_St = 200ms heartbeat 유지** (공식 문서 명시·의미 타당). 토글이 SPI를 건너오는 것 자체가 SPI 통신 생존 테스트. payload 무결성(CRC)은 STM32 로컬 `spi_status`(CRC fail+hb timeout 통합 LINK DOWN/UP)가 **보조 fault 경로**로 이미 존재 — 비트 재정의 불필요, 둘이 상호보완.
  - **BLE(ESB)_Comm_St = CRC-valid 도착 윈도우로 재정의** (`최근 T 내 CRC-valid ≥ N개`). BLE "페어링" 개념이 ESB에 부재. 판정 주체는 **수신측 `02_RX_esb`**(RF는 nRF만 앎) → 0x10 bit6 적재 → STM32 전달.
- **갱신**: [[comm_state_monitoring]] — "두 비트는 서로 다른 링크" 표·판정식, SPI_Comm_St 절 heartbeat 정의 복원, BLE_Comm_St 절 ESB CRC 재정의. [[status]] 다음 시작점·미결 정정.
- **주의**: ESB 판정 주체는 송신 03 아니라 **수신 02_RX_esb** — 구 메모/status의 `esb_rx_cnt`·`ble_link` 위치 코드 대조 재확인 필요(코드 repo 이 PC에 부재).

## [2026-06-05] ingest | lp-am263p — AM263P ADC 브링업 정본(RTI 타이머 트리거) + 8kw adc A1 검증 반영

- **출처**: 2026-06-05 8kw-ev-wpt-tx ADC 브링업 실보드 실측(단일 핀 AIN0, 1 kSPS) + TI SDK `examples/drivers/adc/adc_soc_rti`. flash-time 도구 정본([[jtag_flash_harness]])과 동일 패턴으로 **AM263P 플랫폼 지식 정본을 lp-am263p에 둠**, 8kw가 백링크.
- **생성**: [[am263p_adc_rti_trigger]] (lp-am263p concept) — 3절:
  - **§1 RTI→ADC SOC 트리거 결선 함정(핵심)**: `soc0Trigger=ADC_TRIGGER_RTI1`만으론 부족. RTI 인스턴스 SysConfig `enableIntr0`(Enable Compare Interrupt) 미설정 시 생성 코드가 `RTI_intDisable(..INT0_FLAG)`를 내보내 INT0 이벤트 export가 막힘 → ADC SOC가 tap하는 라인 게이트 닫힘 → compare 발생해도 변환 0회. 해결=`enableIntr0=true`. DMA-trigger 불필요, ISR 본체 자동 생성. 레퍼런스 `adc_soc_rti`와 유일 차이가 이 한 줄.
  - **§2 JTAG/RAM 레지스터 검증 측정 시점 함정**: `loadProgram` 후 reset 없이 read하면 `Drivers_open()` 실행 전(전부 0) 상태를 봐서 "ADC 미설정" 오진. 절차 `reset→reload→run→main loop 도달→read`. SW force(`ADCSOCFRC`)로 변환 경로 생존 먼저 확인 = "설정 문제 vs 트리거 결선 문제" 분리 기법.
  - **§3 검증된 설계 패턴**: RTI 주기 트리거 + EOC ISR(결과 read+flag) + main 루프 consuming(ISR-flag). SPS=RTI compare 주기. AIN0 1 kSPS 검증 완료.
- **8kw 갱신**: [[adc]] A1 ✓(polling→RTI 트리거 설계 전환 명기)·A0 △(단일 채널만)·A1.5 신설(UART 1초 주기화[조절 파라미터]+`src/bsp/adc.{c,h}` 다핀 리팩토링). [[status]] 다음 시작점=UART 주기화→리팩토링→남은 핀(A2), 현황표·미결 갱신. [[roadmap]] task 상태·현재 위치 갱신. index 1건.

---

## [2026-06-05] ingest | oled_tv_software — buck RF 지령 경로·UART 수신 메커니즘·newlib float 함정 + 작업 로드맵 2건

- **buck end-to-end 경로 (실보드 검증)**: 신규 [[buck_vout_ref_command_path]]. 01 UART5 `buck <v>` → 전역 `rx_cmd.tx_buck_vout_ref`(float, 0~300V clamp) → 0x51 `DATA[6,7]` `u16=volts×100`(`_shared/oled_tv_protocol.c` build_rx/apply_rx) → 03 Monitor `tx_buck_vout_ref=<raw>`. 검증 `buck 123.34`→`12334`. **01 UART 커맨드 중 RF 링크 건너 tx-nrf까지 가는 유일한 지령** — 새 tx 지령 추가 패턴(키워드 접두·`rx_cmd_t` passenger·protocol.c 매핑) 정리. 커밋 `eca4d96`(추가)/`175a8f7`(키워드 단축).
- **UART 명령 레퍼런스·수신 메커니즘**: [[uart_command_set]] 갱신 — `buck`(RF 지령)·`stop` 추가, 명령 요약표 신설. 수신·파싱 메커니즘 절: ISR 구동(`HAL_UART_Receive_IT` 1바이트→`UART5_IRQHandler`→`HAL_UART_RxCpltCallback`, 매 바이트 자기 재무장, IRQ pri 14), `cmd_buf[64]` 라인 파싱(63자 초과 폐기), **파싱·실행이 ISR 컨텍스트에서 main loop 선점**, else-if `strncmp` prefix 매칭(분기순=우선순위, `stopXYZ`도 `stop`에 걸림, `phase ` 끝공백 필수).
- **newlib-nano float 빌드 함정**: 신규 [[cubeide_newlib_nano_float]]. `01_RX_control/.cproject` `nanoprintffloat=true`(Debug만)·`nanoscanffloat=true`(이번 세션 활성화). 꺼지면 `buck 15.5` `sscanf("%f")` 소수 깨짐. GUI 경로(MCU/MPU Settings)·구성별 독립·Release 재확인 주의.
- **01 메인 루프 교정**: [[rx_control]] "메인 루프" 절 신설 — 실제 `while(1)`은 `adc_proc(); spi_proc(); Monitor_Loop();` 3개(`Core/Src/main.c:128-130`). 코드 repo CLAUDE.md의 `LED/SPI/ESB/Monitor_Loop` 4종 polling 묘사는 **nRF52(02/03) 펌웨어용** — 코드가 정본. **현재 01 `Monitor_Loop()` 주석처리 비활성**(커밋 `175a8f7`, 03 모니터로 검증하느라 임시로 끔) — [[status]] 미결에 기록.
- **CON2 핀맵**: 변경 없음 — 이미 [[rx_ble_module]]·[[schematic_ble_module_board_v01e00]]에 확정 기재(1 COMM_P5V·2 TXD_uC/P0.15·3 RXD_uC/P0.14·4 COMM_GND, 사용자 확인 2026-06-05). 확정 상태 재확인만.
- **작업 로드맵 2건 (아이디어·미착수)**: [[roadmaps/pc-gui]](G0~G3, UART 모니터링+buck 설정, G0 포트 조합 결정 선행), [[roadmaps/spi-esb-refactor]](R1~R4, 기존 코드 정리 4라운드 흡수). [[roadmap]] 환원 후보·[[status]] 예정 작업에 등재. index 5건.

---

## [2026-06-05] ingest | oled_tv_software — BLE Module Board 회로도 재독·교정 + raw 확보

- **계기**: 사용자가 `BLE_Module_Board_Ver0.1E00_260318 1.pdf` 재ingest 요청 → 이미 [[schematic_ble_module_board_v01e00]]로 ingest됨 확인. 중복 생성 대신 실제 PDF(4시트) 재독으로 미확정 해소·교정.
- **raw 확보**: PDF를 `raw/BLE_Module_Board_Ver0.1E00_260318.pdf`로 복사(483KB), source frontmatter를 raw 경로로 전환. subsystem `02_RX_ble` → `02_RX_ble, 03_TX_ble`(공용 커스텀 모듈).
- **커넥터 핀번호 확정(사용자 확인)**: CON1(SWD) 1 SWDCLK·2 SWDIO·3 nRST·4 GND·5 BLE_P3V3 / CN2(SPI 10P) 1·2 PD3V3·3 nCS·5 MISO·7 MOSI·8 SCK·9·10 DGND(4·6 NC) / CN1(전원 6P) 1~3 COMM_P5V·4~6 COMM_GND. 기존 "확인 필요" 전부 해소. [[st_link_nrf52_flash]] 미확정의 CON1 항목도 해소 표기.
- **전원 아키텍처 교정(모순 해소)**: 기존 페이지 "COMM_P5V(5V)→B1+FLT1→BLE_P3V3"는 오기. 회로도 `전원분리` 블록 실측 = **PD3V3(비절연 3.3V, CN2)→B1 페라이트(SHH-1M2012-221)+FLT1 피드스루(NFM41PC155B1H3L)→BLE_P3V3=nRF VCC**(강압 없음, EMI 필터). COMM_P5V(절연 5V, CN1)은 ISO6721 PC측+CON2 전용. One Point=R5 0Ω DGND↔BLE_GND. (이미 [[st_link_nrf52_flash]]가 "PD3V3 직결"로 맞게 적혀 있던 것과 정합 — 두 페이지 모순 제거.)
- **신규 디테일**: System Reset 회로(SW1 ITS-1107+R12 풀업/R13 직렬/C12 디바운스), 안테나(L1 3.9nH π-매칭→PCB 패턴 안테나, C8/C9 DNP), nRF 내장 DC/DC 인덕터 L2/L3(MLZ1608, 외부 LDO 아님).
- **B1/FLT1 미확정 해소**: 블록 제목 `전원분리`로 필터 확정(강압 아님).

---

## [2026-06-05] ingest | lp-am263p — AM263P JTAG flash 자동화 하네스 + 굽기 운영 규율 (정본)

- **출처**: 2026-06-05 8kw-ev-wpt-tx 실보드 JTAG flash 세션 실측. 도구(jtag_flasher·flash_node.js)는 lp-am263p(cc3351) 원산·8kw 복제 → **flash-time 도구 지식 정본을 lp-am263p에 둠**.
- **생성**: [[jtag_flash_harness]] (lp-am263p concept) — 4대 규율 전부 측정 확정:
  - ① **하네스**: run.bat Node.js `runAsynch`+`run(false)`+`gCmd.status` 폴링 = 6/6 OK. **DSS/Rhino `GEL_RunF`는 깨짐** — GEL_RunF resume가 R5를 JTAG halt 없이 free-run, 그 상태 DSS `readData`로 TCM(`gCmd.status@0x70038010`) 읽으면 `Error 0x400000` 거부 → status 폴링 붕괴.
  - ② **클린 호스트**: IDE 상주 cloudagent+DSLite 경합(요지만, deep-dive는 [[jtag_flash_clean_host]] 위임).
  - ③ **파워 사이클 필수**: 연속 loadProgram/soft reset/중단런으로 R5/OSPI wedged → run 후 status IDLE(0x0)→never BUSY/300s timeout. 전원 차단→복원만 해소(JTAG 재연결 불가). 측정: OP1 ~61s IDLE 탈출, 3/3.
  - ④ **검증 ground truth = standalone 부팅 banner**: 하네스 자기보고/MCP readback보다 정확. 프로파일: NOR SPI FLASH·16.667MHz·30KB·SBL ~28967µs·banner `eta-tx: 8kw-ev-wpt v1.0e00`.
- **보조 사실**: flashwriter(`jtag_flasher.out`=`sbl_jtag_uniflash`+`AutoCmd_t`) gCmd base `0x70038000`/status `0x70038010`/magic `0xDEAD1234`/파일버퍼 `0x70040020`. flash map SBL@`0x0`·app mcelf@`0x81000`. PHY 경고(`PhyTune:1520 PHY enabling failed`) 무해(부팅 성공이 증거). SW1 standalone=`1,1,1,1`/DevBoot=`0,1,0,0`. 하네스 위치 `8kw-ev-wpt-tx/tools/jtag_flash/flash_node_8kw.js`.
- **DevBoot 오기**: 이미 [[CLAUDE]]에서 정정 완료(`1,1,0,0`→`0,1,0,0`, commit 0b59571) — wiki 내 잔존 stale 없음(정정 주석/raw만). 신규 페이지는 정정값 인용.
- **빈자리**: OSPI 독립 readback 미검증(standalone 부팅으로 대체). 갱신: [[flash_open_facts]]·[[jtag_flash_clean_host]] cross-ref, index 1건.

---

## [2026-06-05] ingest | 8kw-ev-wpt-tx — JTAG flash 굽기는 CCS IDE 내린 클린 호스트에서

- **운영 함정 확정 (격리 입증)**: AM263P OSPI를 JTAG로 굽는 host-driven 스크립팅(`run.bat`/Node.js `flash_node.js`, 또는 DSS Rhino)은 CCS IDE(Theia)의 상주 cloudagent+DSLite 디버그 백엔드와 **같은 디버그 백엔드를 두고 경합**. IDE 켜둔 채 flash 돌리면 `ds.configure()`/`openSession`/`resume` 중 런마다 다른 지점에서 죽음 (30s ScriptingTimeoutError / DebugServer.1 timeout / rd32 Error 0x400000 — **비일관 → 펌웨어·보드 결함으로 오인 위험**).
- **증거**: flashwriter `.out` 바이트 동일(펌웨어 무죄)인데 **IDE 켜둠=ERASE_ALL 실패 / IDE 완전 종료=6/6 OK 완주**. 변수는 IDE 상주 여부 하나뿐.
- **확인법 함정**: `getDebugSessions=[]`라도 cloudagent가 띄운 DSLite는 상주 가능 → 작업관리자에서 `node`/`DSLite` **프로세스 레벨**로 확인 후 종료.
- **양립 불가**: MCP `loadProgram`(IDE 경유 RAM 로드)은 IDE 켜짐 필요 / 독립 flash 스크립팅은 IDE 꺼짐 필요.
- **생성**: [[jtag_flash_clean_host]] (8kw concept). index 1건. lp-am263p [[flash_open_facts]]에 cross-ref 추가 (app Flash_open 블로커 ≠ flash-time 호스트 함정, 층위 구분).

---

## [2026-06-05] ingest | oled_tv_software — 플래싱 듀얼 프로브 셋업 (드라이버 스왑 종료)

- **사실 확정 (CLI 실측)**: MCU별 전용 프로브 + 네이티브 도구로 분담. ① `01_RX_control`(STM32F103) → **ST-Link V2 네이티브**(STM32_Programmer_CLI v2.22, FW V2J47S7, Device ID 0x414, connect+read만 실측 — write 미측정). ② `03_TX_ble`(nRF52832 회사보드) → **J-OB v2 = J-Link OB-nRF5340-NordicSemi** S/N 1050329071(정품), program+verify 통과(Bank0@0x0 53248B, exit 0). ③ `02_RX_ble` → DK 온보드 J-Link. 드라이버 분리 → 동시 연결·충돌 없음.
- **함정**: J-Link급 프로브 둘(J-OB v2 + SAM-ICE S/N 24012600) 공존 → `-SelectEmuBySN 1050329071` 고정 필수. ST-Link은 S/N이 `@`로 보고(cosmetic).
- **갱신**: [[st_link_nrf52_flash]] 전면 재작성(정본 — 듀얼 프로브 절차·실측·함정, **pyOCD+Zadig 폴백 강등**, ST-Link WinUSB→네이티브 원복 절차). [[instruments]] "프로그래밍/디버그 프로브" 절 신설(프로브 3종 정체·S/N·드라이버). [[rx_ble_module]] CON1 플래싱 비고 갱신. index 2건.
- **교정**: 회사보드 CON2 UART = **TX P0.15 / RX P0.14**(`custom_board.h:16-17`), NRF_LOG는 RTT(SWD) 전용·UART 미출력. (schematic 소스는 2026-06-04에 이미 정정됨 — 잔존 stale은 st_link 페이지 "미확정" 항목뿐이었고 재작성으로 해소.)
- **빈자리(미검증)**: SES 번들 JLinkARM DLL의 SN 선택 동작, ST-Link 실플래시(write), 플래시 펌웨어 런타임 거동(ESB/SPI/LED), SAM-ICE 연결 대상.

---

## [2026-06-05] lint | lp-am263p — SW1 부트모드 표 DevBoot 값 정정

- **오류**: `teams/g/lp-am263p/CLAUDE.md` SW1 표가 DevBoot를 `1,1,0,0`으로 기재 → 실제로는 OSPI (8S) Octal Read 값의 오기.
- **정정**: DevBoot = `0,1,0,0`(SW1.3만 ON). 근거 LP-AM263P UG SPRUJ85B Table 2-5 ([[raw/lp_am263p_ug/ug_lp-am263p.md]] :469), DevBoot 정의 Table 2-6 :494.
- **부가 수정**: 기존 헤더 `SW1 (1,2,3,4)` 라벨이 실제 기입값(UG의 SW1.4-우선 순서)과 불일치 → 헤더를 UG 순서 **SW1.4/3/2/1**로 명시. 전체 6개 모드 값을 Table 2-5와 교차확인해 표 정합성 확보. ON=논리0(:453) 주석 추가.

---

## [2026-06-05] status | oled_tv_software — 회사 커스텀보드 플래싱·LED 점멸 확인 반영

- **사실 확정**: 회사 커스텀보드(BLE_Module_Board_Ver0.1E00, nRF52832) 입고 + `03_TX_ble` ST-LINK V2 + pyOCD 플래싱 성공 + LED 점멸 육안 확인(LED1 상시점등·LED2/LED3 200ms 토글, active-high). 절차·셋업 함정은 기존 [[st_link_nrf52_flash]]에 정리됨(2026-06-04).
- **status.md 갱신**: stale했던 "다음 시작점"(완료된 ST-LINK 플래싱 지목)을 **LED2/LED3 ↔ 실제 comm-status 비트 연계**로 교체. 하드웨어 입수 표에 플래싱 열·LED 확인 추가. frontmatter date → 2026-06-05.
- **예정**: 플래싱 이슈·해결 추가 공유 시 [[st_link_nrf52_flash]] 트러블슈팅에 ingest.

---

## [2026-06-05] ingest | AM263P TRM/UG wiki 통합 + RAG MCP 폐기

- **결정**: AM263P 자료를 위한 별도 RAG MCP 서버(`C:\firmware-rag\`, ChromaDB 벡터검색 + 800단어 청크 + all-MiniLM-L6-v2)를 폐기하고 wiki 단독으로 전환. 근거: ① wiki 철학 = "원본 텍스트가 아닌 이해된 지식" ② 800단어 청킹이 레지스터 표를 절단(TRM 질의의 핵심 손상) ③ "wiki 단독 ≠ LLM이 1725쪽 정독" — 기계추출(토큰 0) + Grep 발견 + demand 환원 구조.
- **기계추출**: `pymupdf4llm` 1.27.2.3로 TRM 1725쪽을 `get_toc()` 기반 26개 챕터 마크다운(텍스트+표, 이미지 제외)으로 → `raw/am263p_trm/chNN_*.md`. ch7·ch13만 level-2 세분. UG 60쪽은 이미지 포함 전체 → `raw/lp_am263p_ug/`(md+img 42장).
- **source 페이지**: [[am263p_trm]](TOC 맵 + "발견은 Grep" 가이드 + ingested/candidate 섹션 인덱스), [[lp_am263p_ug]](핀맵·부트모드·핀먹스·OSPI 배선 + §5.3 보드 함정 — DQS/LBCLK swap·XDS110 bricking).
- **demand-ingest 예시**: [[am263p_mcspi_controller]] — S6 `SPI not responsive` 직결 MCSPI(13.1.3) 환원.
- **폐기 처리**: `~/.claude.json`의 `ti-am263p` mcpServers 등록 제거(재시작 시 도구 사라짐, 다른 CCS 서버 보존). 22MB TRM PDF는 `.gitignore`(디스크 only). `C:\firmware-rag\` rm_db/스크립트 삭제는 사용자 확인 대기.

---

## [2026-06-05] status | 8kw-ev-wpt-tx — CCS 프로젝트 스캐폴드 완료 반영

- A0 전제 완료: hello_world 기반 CCS 프로젝트 생성·Release 빌드 통과·커밋됨 → 구현 현황 ✓ 갱신.
- 다음 시작점 업데이트: A0 착수 전 SysConfig MCP 버전 정합 확인 절차 추가.
- `직전 완료` 섹션 신설 — CCS workspace 참조 import 작업환경 메모 포함.

---

## [2026-06-04] ingest | 8kw-ev-wpt-tx 프로젝트 신설 + adc 작업 호 개설

- eta 보드 J3 커넥터 6채널 ADC 핀맵(사용자 제공) → [[adc_pinmap]] 엔티티 생성.
- `adc` 작업 로드맵(A0~A4) 신설: SysConfig 설정 → 단채널 검증 → 전채널 읽기 → 신호별 스케일링 → 실보드 교차검증.
- A3(스케일링) 블로커: Temp 모듈 특성·전류 센서 감도·분압비 미입수 — 추가 정보 대기.
- lp-am263p에 잘못 붙었던 eta-adc 항목 모두 제거 후 이 프로젝트로 이관.
- 신규 프로젝트 `teams/g/8kw-ev-wpt-tx` 생성 — 8kW EV WPT 송신 보드 Ver1.0E00, LP-AM263P 기반.

---

## [2026-06-04] ingest | oled_tv_software 03_TX_ble LED 인디케이터 + 보드 분기

- 03_TX_ble LED 3개 구현·실보드 검증: LED1(P0.09) System Ready 상시 점등, LED2(P0.08) SPI Comm Status·LED3(P0.06) BLE(ESB) Comm Status 200ms 토글. 극성 **active-high(1=ON)** 실측 확정.
- LED 핀맵 정정 과정: 초기 잘못된 핀(10/9/8) → 실측 혼선 → 정정(9/8/6, = `_shared/oled_tv_protocol.h` 원래 값). 극성도 active-low 오판정 → 정정해 active-high 확정.
- DK(PCA10040) ↔ 회사 보드 핀맵 분기: `_shared/custom_board.h` 신설(`LEDS_NUMBER 0`, UART RX=14/TX=15) + emProject `BOARD_CUSTOM`. LED 코드는 `#if defined(BOARD_CUSTOM)` 가드 — DK에선 P0.06/08이 UART라 충돌 회피.
- 갱신:
  - [[schematic_ble_module_board_v01e00]] — LED 인디케이터 GPIO 핀(P0.09/08/06)·극성, CON2 UART 핀(P0.15/14) 채움
  - [[gpio_verification_pinmap]] — 03_TX_ble LED 검증 행 3개 추가, P0.17 중복 주석 "PCA10040" → "커스텀 보드" 정정
  - [[tx_ble_module]] — LED 인디케이터·보드 분기 섹션 신설 + 현황표 2행 추가

---

## [2026-06-04] ingest | oled_tv_software ST-LINK V2 + pyOCD nRF52832 플래싱 절차 확립

- 계기: BLE_Module_Board_Ver0.1E00(nRF52832)에 `03_TX_ble` 플래싱 성공. SES 내장 다운로더·nrfjprog가 J-Link 전용이라 ST-LINK로 사용 불가 → pyOCD 우회 경로 확립.
- 핵심 함정 3개 (Windows Python 3.14 환경):
  1. `libusb-package` 바이너리 wheel 없음 → cp311 wheel에서 `libusb-1.0.dll` 수동 추출·복사
  2. ST-LINK WinUSB 바인딩(Zadig) → STM32CubeIDE 플래싱 불가(부작용), 장치 관리자로 복구
  3. `target_nRF52.py` CTRL-AP 패치 — `is_locked()`에서 `ProbeError` try/except → `return False` (ST-LINK V2가 AP#1 접근 불가)
- 추가 환원: ST-LINK 드라이버 토글 절차 (WinUSB↔ST 정품, 양방향·모드 확인·동글 2개 팁)
- 생성:
  - concepts: [[st_link_nrf52_flash]] (플래싱 how-to — 셋업·배선·절차·트러블슈팅·드라이버 토글·미확정)
- 갱신:
  - [[status]] — 다음 시작점 참고 줄에 [[st_link_nrf52_flash]] 링크 추가
  - [[rx_ble_module]] — CON1 비고에 역링크 추가
  - [[index]] — Concepts 섹션에 st_link_nrf52_flash 등록
- 미확정 잔류: CON1 물리 핀번호↔네트 매핑 (실크 Pin1 확인 필요), CON2 UART nRF GPIO 핀 라우팅

---

## [2026-06-01] ingest | oled_tv_software SPI 10ms 폴링 진단 (미달 반증·✓ 확정)

- 소스: 진단 세션 직접 보고 + 오실로스코프 캡처 `P3NOFO01.PNG` (CS Δt=10ms, 1/Δt=100Hz, Vpp=3.79V)
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control, 02_RX_ble
- 결론: "SPI 10ms 미동작"은 동작 결함이 아닌 **관측 도구 한계** (단일 필드 덮어쓰기). 10ms 폴링은 처음부터 정상.
- 생성:
  - sources: [[spi_10ms_diagnosis_report_260601]] (진단 경과·3가지 가설 반증·실보드 검증 결과)
  - assets: `spi_cs_10ms_260601.png` (오실로 캡처 — 기존 heartbeat `P3NOFO01.PNG`와 별도)
- 갱신:
  - [[spi_link_reliability]] — "미달 — SPI 10ms 폴링 ✗" → "SPI 10ms 폴링 주기 ✓", 오류율 모니터 카운터명/출력형식 정정(`spi_crc_fail_cnt`·누적+delta), `spi_tx_busy` 주석 정정(근본원인 미확인), 관련 백링크 추가
  - [[status]] — date 갱신(05-29→06-01), 다음 시작점(nRF52832 SPIS SCK datasheet ingest), SPI 10ms ✗→✓, 오류율 모니터 메모 갱신, "SPI 10ms 미동작 원인 규명" 미결 제거
  - [[index]] — spi_link_reliability 설명 갱신, 신규 source 등록
- 핵심 합의: NVIC enable은 `MX_DMA_Init()`에 정상 존재(`app_dma.c:15-19`). `PACKET_INTERVAL=10`도 이미 설정됨. 초당 100tx, CrcFail=0 확인. "미동작" 의심은 `rx_status.spi_status` 단일 필드 덮어쓰기 관측 한계.

---

## [2026-06-01] roadmap | lp-am263p 포팅 로드맵 project/task 분리 + spine 정리

- 계기: 앞으로 프로젝트·작업 로드맵을 wiki에서 작성. 외부 코드-repo `tasks/porting/roadmap.md`는 이미 2026-05-29 wiki `roadmap.md`로 ingest됨(외부보다 wiki가 최신: R27/R28 vs R24/R26) → 외부 파일 legacy화, 기존 wiki roadmap을 비판적으로 개정.
- 비판 검토에서 잡은 수정:
  - A. staleness — §6 "24라운드째"가 R27+와 어긋남(외부 R24 잔존) → R27로 정정.
  - B. "2~4주" false precision — 문서 스스로 "추정 불가"라면서 단일 숫자 제시 → 삭제, S3 게이트 기반 통일.
  - C. S5~S8 난이도 grading — 전부 미도달인데 등급 부여 → "S3 통과 후 재추정"으로 축약.
  - D. altitude 과적재 — §1 칩차이·§3 HW표가 spine 아님 + CLAUDE.md와 중복 → 백링크 위임.
  - E. §7 환원후보 80% 해소 방치 → 미해소 1건만 남기고 나머지는 "facts/handoff 반영 완료" 한 줄.
  - F. §2 "가능성 높음" 약과장 → "불가 근거 없음·미증명"으로 완화·압축.
- 구조 결정(사용자): project/task 2단위로 분리.
  - 신규 `roadmaps/porting.md` — 작업 호. S0~S8 spine·완료 기준 표·현재 위치(→status)·남은 일정·환원후보. 엄격 spine(§1 칩차이→[[is25lx256_vs_spansion_quirks]], 핸드오프→[[sbl_app_flash_handoff]], HW→[[CLAUDE]] 위임).
  - `roadmap.md` 개정 — 얇은 프로젝트 호. 목표·작업 호 인덱스(1행)·현재 위치만. S0~S8 재서술 금지(divergence 방지) → [[porting]] 위임.
- 갱신: [[lp-am263p]] `CLAUDE.md` 3-레이어 표(전략을 프로젝트/작업 2단으로), [[index]].
- 손대지 않음: `status.md`(라운드 갱신 아님, 다음 시작점 R28 유지), [[flash_open_facts]]·[[flash_open_diagnostic_log]](사실/history 단일 소스).

---

## [2026-06-01] schema | 파이프라인 도메인 자산 — 계측 인벤토리 + GPIO 검증 핀맵 + 로드맵 컨벤션

- 계기: `~eta/firmware-dev-pipeline` 두 단계(explorer/planner)가 wiki를 읽어 쓰도록 갱신됨. 그 계약을 wiki schema에 맞게 세 자산으로 빚음.
- 합의: 시작 컨텍스트 `teams/c/oled_tv_software`(핀맵 seed 풍부), 로드맵은 별도 `roadmap.md`(status 확장 아님, lp-am263p 선례), 인벤토리는 root `pages/reference/` 신설, 작업 로드맵은 `roadmaps/<task>.md`.
- 생성:
  - reference: [[instruments]] (회사 공통, Keysight InfiniiVision MSOX3104T — 무엇을·어떻게 측정 + 사용 결. 추가 장비 스텁)
  - oled concepts: [[gpio_verification_pinmap]] (기능→프로브 핀→기대값. 기존 wiki 사실만 seed, 미확인 핀은 "확인 필요"로 호명 — 추론 금지)
  - oled `roadmap.md` (M0~M6 마일스톤 호, 현재 M3 SPI 10ms 막힘, PRD 1~2ms 지연 게이트). lp-am263p 선례 결 계승
  - oled `roadmaps/README.md` (작업 로드맵 폴더 컨벤션 — 파일은 요청 시)
- 갱신:
  - root `CLAUDE.md` — 레이아웃에 reference/·roadmap.md·status.md·roadmaps/ 추가, "로드맵 컨벤션" 절 신설, "파이프라인 — roadmap 읽기/갱신 절차" 절 신설(explorer/planner 읽기 전용·wiki 작성)
  - [[lp-am263p]] `CLAUDE.md` — 3-레이어 표가 root 로드맵 컨벤션의 프로젝트별 구현임을 명시 (중복 정의 회피)
  - oled `CLAUDE.md` — 전략/검증 자산 절 추가 ([[roadmap]]↔[[status]], [[gpio_verification_pinmap]], [[instruments]])
  - [[index]]
- 핵심 결정: 읽기=파이프라인, 작성·갱신=wiki. planner는 핀번호를 추론하지 않고 wiki에 없으면 "확인 필요"로 사용자 호명. 핀맵은 P0.17 의미 충돌(TX 시작 03 vs heartbeat 02)과 RX_control 추가 GPIO 핀번호를 미확정으로 남김 — 사용자 호명 대기.

---

## [2026-05-29] ingest | lp-am263p report.md R19~R27 — 사실 원장/라운드 로그 분리 + CLAUDE.md schema 신설

- 소스: `~/eta/projects/g/lp-am263p/bp-3351/tasks/porting/report.md` (R19~R27 + R28 계획)
- 대상 프로젝트: `teams/g/lp-am263p`
- 핵심 합의: 초장기 디버그 작업의 맥락유실 방지를 위해 "작업 중 밝혀진 사실"을 **사실 원장(제자리 수정) + 라운드 로그(append-only) 2분리**. 3-레이어 = 로드맵(전략)/status(전술)/facts·log(누적).
- 생성:
  - concepts: [[flash_open_facts]] (확정 사실 + **폐기 가설(재시도 금지)** + 최유력 가설), [[flash_open_diagnostic_log]] (R7~R27 + R28 계획, append-only)
  - [[lp-am263p]] 도메인 `CLAUDE.md` 신설 (부재했음) — 3-레이어 분류·SW1 부트모드·boot flow·"자주 어긋나는 자리"
- 갱신:
  - `roadmap.md` — Round 24+→27+, **R26 반증된 `DQS_ENABLE=0` "검증 예정" 줄 제거**(stale), facts/log 위임 백링크, §7 환원후보 1·2·4·5 해소 표시
  - `status.md` — 빈 템플릿 채움: 다음 시작점 R28(jtag_flasher 공식 이식), S0~S8 현황표, 미결 4건
  - [[sbl_app_flash_handoff]] — 후보1에 R25~27 실측, 신규 §flashFixUpOspiBoot 부재(app vs flasher 비대칭), §SW1 4S 핸드오프 질문, 후보3 DQS는 R26 검증(DQS 필수·DQS=0 반증)
  - [[is25lx256_vs_spansion_quirks]] — set888mode=0x81 정정(0x71 혼동 종결), AM243 Quad/AM263P Octal 라인 차이
  - [[index]]
- 핵심 결정: R25(skipHwInit=FALSE)·R26(DQS=0) 두 진단 가설 폐기 기록 → 다음 세션이 facts.md만 읽고 재시도 방지. 최유력 가설 = SBL 잔여 8D + skipHwInit=TRUE 캡처 미스, R28에서 flasher 성공 공식 이식으로 검증.

---

## [2026-05-29] ingest | SPI heartbeat 작업 보고서 (260529)

- 소스: `tasks/spi-heartbeat/report.md` + 오실로 스크린샷 `P3NOFO01.PNG`
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
- 생성:
  - sources: [[spi_heartbeat_report_260529]]
  - concepts: [[spi_link_reliability]] (heartbeat 구현·오류율 모니터·spi_tx_busy 타임아웃 복구·10ms/9MHz 현황)
- 갱신:
  - [[comm_state_monitoring]] — 200ms 교번 사양이 코드(Heartbeat_Loop 200ms 독립 타이머)로 실현됨 확정 + 백링크
  - [[spi_packet_format]] — 전송 파라미터 "10ms/9.0Mbps"를 사양으로 명시, 실측 미달(폴링 1000ms, 9MHz revert) 주석
  - [[rx_ble_module]] — Heartbeat_Loop·P0.17 디버그 핀·펌웨어 현황 3행 추가
  - [[index]], [[status]]
- 핵심 합의:
  - 모순은 wiki↔wiki가 아니라 과거 코드(매 SPI 사이클)↔사양(200ms 매뉴얼). 오늘 코드가 사양 충족.
  - heartbeat만 실보드 검증(✓). 오류율 모니터·spi_tx_busy 복구는 △. SPI 10ms 폴링·9MHz는 ✗.
  - 10ms 미달 유력 원인: STM32 `HAL_SPI_MspInit` DMA IRQ(NVIC) 부재 → 콜백 미발생.
  - "10ms" 용어 구분: 앱 SPI 폴링 주기(PACKET_INTERVAL) ≠ ESB RF wire 주기 ([[spi_debug_log_report_260529]] 미결과 동일).
  - `_ble` 파일명은 잔재이며 ESB 라인의 정식 코드 (사용자 확인).

---

## [2026-05-29] ingest | lp-am263p 포팅 로드맵 — 전략 spine

- 소스: `~/eta/projects/g/lp-am263p/bp-3351/tasks/porting/roadmap.md` (planner roadmap)
- 대상 프로젝트: `teams/g/lp-am263p`
- 생성: `teams/g/lp-am263p/roadmap.md` — 프로젝트 루트 living doc
  - 백링크 spine 방식: 단계 구조(S0~S8)·현재 위치(S3 막힘)·남은 일정만 직접 보유
  - 깊은 디테일은 기존 concept로 위임 — [[is25lx256_vs_spansion_quirks]], [[sbl_app_flash_handoff]], [[flash_open_sequence]], [[xspi_dummy_cycles]]
  - 기능별 현황은 [[status]]와 역할 분담 (로드맵=전략, status=전술)
- 갱신: `index.md` — lp-am263p 섹션에 "Living docs"(roadmap/status) 추가
- 미결: lp-am263p 프로젝트에 도메인 `CLAUDE.md` 부재 (다른 프로젝트는 모두 보유) — 별도 생성 필요

---

## [2026-05-29] ingest | SPI 디버그 로그 검증 결과 (시나리오 A/B)

- 소스: `tasks/spi-debug-log/report.md`
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
- 생성:
  - sources: [[spi_debug_log_report_260529]]
  - concepts: [[esb_ptx_ack_assembly]] (PTX ACK payload 재조립 + ISR printf 금지 패턴)
- 갱신:
  - [[rx_to_tx_packets]] — 코드 실측 DATA 레이아웃 추가, 프로토콜 매뉴얼과의 불일치 정리 (0x50 bit 순서, 0x51 Zin·TxVoutRef 미구현, 0x52 T2 스케일 0.1°C 확인)
  - [[tx_ble_module]] — Monitor_Loop 출력 포맷 + [[esb_ptx_ack_assembly]] 링크 추가
- 핵심 합의:
  - 0x51 코드에 Zin·TxVoutRef 없음 — 프로토콜 매뉴얼 대비 미구현 필드
  - 0x50 bit2=BuckSt / bit3=Warning / bit4=Fault — 매뉴얼과 순서 다름
  - 0x52 T2 스케일은 코드 기준 0.1°C (매뉴얼 "0.01°C" 오기 해소)
  - PTX에서 g_last_ack_by_hdr[3] 패턴 필수 — 1초 윈도우 내 3헤더 보존

## [2026-05-27] ingest | Rx OLED Regulator Control Board 회로도 (OrCAD Design XML)

- 소스: `rx_oled_regulator_control_board_260327.xml` (OrCAD Design XML, 68,941줄) + `Rx_OLED_Regulator_Control_Board_260327.pdf`
- 대상 프로젝트: `teams/c/oled_tv_software`, subsystem: 01_RX_control
- 생성: `sources/schematic_rx_regulator_control_board.md`
- 갱신: `entities/rx_control.md` (CAN·DAC·추가 GPIO 신호 추가), `concepts/adc_channel_map.md` (TEMP1/TEMP2 swap 회로도 확인으로 해소)
- 확인 사항: MCU는 STM32F103VCT6/LQFP64 (OrCAD 라이브러리명 오기), 39개 _uC 신호·24개 _CN 신호 전수 추출, TEMP1_ADC_uC=PC4 좌표 매칭 확인

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
