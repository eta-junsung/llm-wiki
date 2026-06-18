---
date: 2026-06-19
---


# 8kw-ev-wpt-tx — 구현 현황

> 전략 spine은 [[roadmap]], 작업 단위 호는 [[adc]]·[[pwm]].
> ⚠️ ADC 상태는 **branch `adc`의 커밋된 상태에서 코드로 역산**한 것 (commit c512e3b, origin/adc). PWM 상태는 **branch `pwm`**(최신 = commit **d01fc0a** — 85 kHz 고정 + dead-time config 분리). UART5 PC 텔레메트리는 **branch `uart5`**(commit **ba241fa**·**979699d**, 실보드 검증 2026-06-11). 프로젝트 트리에 status.md는 없음 — status는 wiki 측에만 존재한다.

## 소스 레이아웃

- BSP 디렉토리는 **`src/eta_bsp/`** (eta_ 접두가 디렉토리명까지 적용). eta_bsp 레이어 도입 (commit a655de4, edddc31).
- 파일: `src/main.c`, `src/eta_bsp/eta_adc.{c,h}`, `src/eta_bsp/eta_uart5.{c,h}`, **`src/eta_bsp/eta_pwm.{c,h}`**, **`src/eta_bsp/eta_gpio.{c,h}`**(신설 — GPIO 출력 2핀), **`src/eta_bsp/eta_tuning.h`**(신설 — 컴파일타임 튜닝 knob, `ETA_DEADTIME_NS` 단일소스).
- 컨벤션: **eta_ 접두 + _loop 접미** (`eta_adc_loop`, `eta_uart5_loop` — ISR이 flag만 세우고 main 루프 함수가 소비).
- **튜닝 knob 분리(`eta_tuning.h`)**: dead-time 등 HW 엔지니어가 만지는 컴파일타임 상수를 한 파일에 모음. 한 줄만 바꿔 재빌드(**build-per-change**)하면 파생값 자동 추종. `eta_pwm_init()`이 런타임 override라 **SysConfig 재생성에 면역**(아래 §빌드 환경).

## 직전 완료 — A2: 6채널 ADC 완성 (실보드 검증 완료, commit c512e3b)

ADC 목표 **6채널 전부 달성**. 물리 인스턴스 **5개(ADC0~ADC4)** 사용:

| enum | 신호 | 물리 ADC/SOC/AIN | J3 핀 | int_xbar / EOC IRQ |
|------|------|------------------|-------|--------------------|
| ETA_ADC_CH_TEMP_MODULE2 | Temp_Module2 | ADC1 SOC0 AIN0 | J3.24 | OUT_0 / IRQ146 |
| ETA_ADC_CH_I_LCC_SEN | I_LCC_SEN | ADC4 SOC0 AIN0 | J3.27 | OUT_2 / IRQ148 |
| ETA_ADC_CH_I_COIL_SEN | I_COIL_SEN | ADC0 SOC0 AIN1 | J3.28 | OUT_1 / IRQ147 |
| ETA_ADC_CH_GA_IIN_SEN | GA_Iin_SEN | ADC1 SOC1 AIN1 | J3.29 | OUT_0 / IRQ146 |
| ETA_ADC_CH_TEMP_MODULE1 | Temp_Module1 | ADC2 SOC0 AIN0 | J3.25 | OUT_3 / IRQ149 |
| ETA_ADC_CH_GA_VIN | GA_Vin | ADC3 SOC0 AIN0 | J3.26 | OUT_4 / IRQ150 |

- **ADC1만 SOC0+SOC1 라운드로빈**(단일 SOC1 EOC ISR로 2채널 수확), 나머지(ADC0/2/3/4)는 SOC0 단독. 트리거 = **RTI1**(SysConfig 논리명 `CONFIG_RTI0`) 1 ms 공유 → **1 kSPS**. 인스턴스/채널 배치 근거 [[am263p_adc_instance_allocation]].
- **ISR은 raw count만 저장**, main의 `eta_adc_loop`이 `(raw*3300)/4095` 정수 mV 변환(out-param 방식, commit 88d9deb).
- **실보드에서 6채널 raw→mV 변환 경로 검증 완료.**
- ✅ **AIN 핀 hard `$assign` 승격 (soft 재셔플 리스크 해소)**: 직전까지 물리 인스턴스만 hard `$assign`이고 AIN 핀은 `$suggestSolution`(soft)이었음. 신규 2채널 추가 시 솔버 재셔플([[am263p_syscfg_soft_vs_hard_assign]])을 막기 위해 **AIN 핀까지 전부 `$assign`으로 hard 승격**. 재생성 후 물리 배정 ADC0~4 유지(재셔플 없음) 확인.

## 직전 완료 — 리팩토링: eta_adc.c 테이블 주도화 (commit c512e3b)

- 인스턴스별로 펼쳐져 있던 **ISR 5개 · init 5블록 · loop 5블록**(차이는 베이스주소·결과주소·IRQ·ready플래그·SOC→채널 매핑뿐)을 → **인스턴스 기술 테이블 `g_eta_adc_inst[]` + 공용 `eta_adc_eoc_isr()` + 인덱스 루프**로 통합.
- `eta_adc.c` 약 **100줄 감소(332→232)**, 동작·핀맵·IRQ 매핑 **불변**.
- 향후 채널 추가 = **enum 1행 + 테이블 1행**. 채널 수는 `ETA_ADC_CH_COUNT`(enum)로 일원화, `eta_adc.c`는 테이블 루프라 자동 추종.
- ⚠️ 단 **UART 출력(`eta_uart5.c`)은 여전히 채널별 `DebugP_log` 라인 하드코딩** → 채널 추가 시 출력 라인도 함께 추가해야 함.

## 직전 완료 — UART5 PC 텔레메트리: 바이너리 패킷 + PC GUI (branch uart5, ba241fa·979699d, 실보드 검증 2026-06-11)

UART5로 ADC 6채널을 PC에 송출하는 **18B 고정 바이너리 패킷** + 이를 받는 **PC 모니터 GUI** 완성. 패킷 정본 [[uart5_packet_protocol]], GUI 정본 [[pc_monitor_gui]].

- **패킷(18B, big-endian)**: `[SOF=0xA5][LEN=12][TYPE=0x01][SEQ][ch0..ch5 raw u16×6][CRC-16/CCITT-FALSE]`. CRC poly `0x1021`·init `0xFFFF`·범위 byte[1..15]. 송신 RTI2 **10 Hz(100 ms)**, 115200/8N1 **polled blocking**.
- **thin device, smart host**: wire에는 raw count(0~4095)만, mV·물리량은 호스트가 파생. mV는 펌웨어 `eta_adc.c` 정수식 `raw*3300/4095`을 GUI가 미러.
- **채널 순서 = `ETA_ADC_CH` enum**(ch0 Temp_Module2, ch1 Temp_Module1, ch2 GA_Vin, ch3 I_LCC_SEN, ch4 I_COIL_SEN, ch5 GA_Iin_SEN). `src/eta_bsp/eta_packet.{c,h}`가 채널 루프 직렬화+CRC → **채널 추가 자동 추종**(LEN도 따라감). `eta_uart5.c`는 송신만, 핀맵 `eta_uart5.h`(TXD=EPWM15_A=J1.4).
- **GUI(`tools/gui/gui.py`, pyserial+Tkinter+matplotlib)**: 4컬럼 표(Channel/ADC(V)/ADC(12bits)/Physical) + 채널 체크박스(플롯·CSV 토글) + 패킷 헬스(Hz/SEQ드롭/CRC에러) + 라이브 플롯 + **raw-only CSV 로깅**. Physical은 계수 테이블 단일 소스(계수 미입수라 현재 placeholder). PyInstaller 단일 exe(`8kw-gui.spec`).
- **실보드 검증(2026-06-11)**: COM13(CP210x, J1.4→THVD1400→J24) 29.8 s — **10.067 Hz, 301프레임 전부 유효, SEQ 드롭 0·CRC 에러 0**. 프레이밍 강건성(정상/1바이트 손상→재동기/ASCII 잡음·가짜 SOF→폐기 후 복구) 모두 PASS.
- ⚠️ **선례 차이 명기**: oled([[pc_uart_gui]])는 XOR 체크섬·다중 HDR·양방향, 8kw는 CRC-16·단일 패킷·**단방향 텔레메트리**.
- ✅ **A1.5 UART 출력 채널 하드코딩 미결 해소**: 구 `eta_uart5.c` 채널별 `DebugP_log` 텍스트 라인 → `eta_packet.c` 채널 루프 직렬화로 대체. 채널 추가 시 출력 라인 수동 추가 불요.

## 직전 완료 — GUI GPIO 왕복 검증 + UART5 RX 1바이트 fix (실보드 검증 2026-06-16)

GUI GD_EN ON 버튼 → TYPE=0x10 커맨드 → `eta_gpio_request_gd_en()` → `eta_gpio_loop()` → GPIO93(J4.33) HIGH. Logic2 CH0 LOW→HIGH 전이 실측. standalone flash 부팅 후 동작 재확인.

- **UART5 RX POLLED 1바이트 fix**: SDK `UART_read()` POLLED+NO_WAIT+FULL에서 `rx.count`가 앱 transaction에 미반영 → stale 0x00 버퍼 주입으로 SOF 탐색 불가. `count=1`, 반환값 `==SystemP_SUCCESS` 판정으로 수정. 정본 [[uart5_rx_polled_1byte]].
- **GPIO 루프 패턴 정착**: `eta_gpio_request_gd_en()` enqueue + `eta_gpio_loop()` 소비. `eta_gpio_set_gd_en()`은 static 비공개. `eta_gpio_set_485_en()`만 TX 타이밍 직결 예외 경로 유지.
- **flash_node_8kw.js mcelf 자동 선택**: `Release/` 와 `build/` mtime 비교, 더 최신 선택 (콘솔 출력). 굽기 전 빌드 완료 필수.
- **"Run > Flash Project" 금지**: SBL 미포함 → 전원 사이클 후 standalone 부팅 불가. 정본 [[jtag_flash_clean_host]].

## 직전 완료 — GPIO 출력 구현 + UART5 양방향 확장 (branch gpio, 실보드 검증 2026-06-16)

GPIO 출력 2핀 브링업과 UART5 양방향 확장(GPIO 커맨드 RX + 상태 TX)을 완료. 정본 [[gpio_impl]].

### GPIO 출력 (`eta_gpio.{c,h}` 신설)

| 신호 | GPIO | 커넥터 핀 | 초기값 | 실측 |
|------|------|-----------|--------|------|
| 485_EN | 91 | J5.48 | LOW | 10 Hz 펄스 (UART5 DE 토글) 확인 |
| GD_EN_seed | 93 | J4.33 | LOW | HIGH 확인 |

- **PADCONFIG 런타임 mux** (`PIN_MODE(7)`) — `eta_gpio_init()`이 런타임 직접 설정. `example.syscfg` 불변.
- **TCA6416A U54 PRU_MUX_SEL 헤더 라우팅**: I2C1(0x20) P07=HIGH로 GPIO93(J4.33) 헤더 라우팅 활성화.
- API: `eta_gpio_set_485_en(bool)` / `eta_gpio_set_gd_en(bool)` — 헤더 extern 공개(UART5 연동용).

### UART5 양방향 확장

- **TX 방향 자동 토글**: `UART_write` 전 `eta_gpio_set_485_en(true)`, 후 `false`. **485_EN 자동 DE 구현 완료.**
- **TYPE=0x10 GPIO 커맨드 RX**: PC→MCU. `CMD_ID=0x01`(GD_EN_seed), `VALUE=0/1`. `eta_uart5.c`에 파서 추가.
- **TYPE=0x02 GPIO 상태 TX**: MCU→PC. 7B 이벤트 패킷 — init·set_gd_en 시 자동 송신. `bit0=485_EN, bit1=GD_EN_seed`.

### PC GUI GPIO Control 섹션 (`tools/gui/gui.py`)

- 485_EN: 상태 표시 라벨(읽기 전용).
- GD_EN_seed: ON/OFF 토글 버튼 + 상태 라벨.
- `send_gpio_cmd()`: TYPE=0x10 커맨드 전송, Lock 포함, CRC-16 적용.

### 빌드 시스템 정리

- CCS IDE `build/` Exclude from Build 적용 (makefile 중복 심볼 해소).
- `flash_node_8kw.js` 경로: `build/` → `Release/`.
- `build/makefile FILES_common`에 `eta_gpio.c` 추가.
- `.theia/launch.json`: 단일 project-based launch만 유지.

## 직전 완료 — 툴체인 gmake 스택업: 신 스택 경고 0 빌드 성공 (branch toolchain-ccs21-sdk2606, commit 5a5fa44, 2026-06-19)

브랜치 `toolchain-ccs21-sdk2606`(v1_0e00 190c2de에서 분기, origin 푸시) — **gmake(build/) 측 전부 신 스택 경고 0 성공**.

구 스택 → 신 스택:

| 구성 요소 | 구 | 신 |
|----------|---|---|
| CCS | 20.5 / ccs2050 | 21 / ccs2100 |
| SDK | 26_00_00_01 | 26_00_00_06 |
| SysConfig | 1.27.0 | 1.28.0+4696 |
| TICLANG | 4.0.4.LTS | 5.1.1.LTS |

변경 내용:
- **`config.mk` 경로 3종**: SDK / CGT / SYSCFG_NODE 신 경로로 갱신.
- **`makefile`**: SDK 경로 + CGT/SYSCFG_NODE override(`imports.mak` `=` 우회, include 이후 재정의) + `genimage_am26x.py` → `genimage.py` 리네임.
- **`example.syscfg` `@versions`**: SysConfig 1.28.0+4696으로 갱신.
- **`generated/` enet·SDL stub 12개**: 신 SDK SysConfig로 재생성.
- **`ospi_flash` 스크립팅 호스트 경로**: `ccs2050` → `ccs2100`.
- **resolved 변수 실측 확인**: `MCU_PLUS_SDK_PATH=_06`, `CGT=ti-cgt-armllvm_5.1.1.LTS`, `SYSCFG_NODE=ccs2100/ccs/tools/node/node`.

⚠️ **미완**: 실보드 부팅 검증 미완(gmake Phase 1 완료), CCS GUI `.cproject` Phase 2 마이그레이션 미완.

정본 [[sdk_ccs_toolchain_migration]], [[syscfg_build_model]], [[ospi_flash_tooling]].

---

## 다음 작업: 툴체인 실보드 검증 → CCS GUI Phase 2 / v1_0e00 새 노트북 실테스트 / PWM P3 / ADC(A3·A4) / UART5 Phase 2

**다음 시작점**: **`toolchain-ccs21-sdk2606` 브랜치 실보드 부팅 검증 — `run_flash_node_8kw.ps1 -Source build`(gmake .mcelf) → SW1=0011 파워사이클 → standalone 부팅 확인**.
1. 전제: ① CCS21 IDE 완전 종료(상주 DSLite가 flash 스크립팅과 경합), ② ccs-debug MCP 연결 + allow-list 권한(서브에이전트는 권한 프롬프트 못 띄움), ③ 보드 JTAG(XDS110)·Logic2 연결
2. `run_flash_node_8kw.ps1 -Source build` (gmake `.mcelf`; `Release/` CCS 산출물은 아직 구스택 → 금지)
3. 파워사이클 → standalone 부팅 확인 ([[ospi_boot_mode_strap]] SW1=0011 xSPI 8D SFDP)
4. 기능 스모크(codegen 4.0.4→5.1.1 무회귀): PWM dead-time both-LOW 추종, ADC 전압 추종 (구스택 known-good 값과 비교)
5. **통과 후**: CCS GUI Phase 2 마이그레이션(사용자 IDE 작업 — [[sdk_ccs_toolchain_migration]] §6) → `.cproject`/`.ccsproject` diff 별도 커밋

### v1_0e00 직전 세션 완료 (브랜치 origin push 완료, tip `190c2de`)

- **누락 필수 자산 .gitignore negation 추적 진입**: `tools/ospi_flash/Release/ospi_flasher.out`(flash 엔진 헬퍼 FW), `tools/ospi_flash/targetConfigs/AM263Px.ccxml`.
- **`jtag_flasher` → `ospi_flasher` 리네임**: `flash_node_8kw.js:26` 경로 + 변수명 (디렉터리 `tools/ospi_flash`와 일관).
- **README.md 신설**: ① 최초 1회 셋업 체크리스트(CCS·SDK·SBL 복사·보드 3건: SW1=0011·SAC 해제·IDE 종료) / ② 평소 GUI 사용.
- **TI 경로 하드코딩 유지 + 문서화**: `run.bat`=`C:/ti/ccs2050/...`, `TI_DIR=C:/ti`, `config.mk` 3줄 `?=` env override.
- **이 머신 fresh-clone 시뮬레이션**: 자산 추적·gmake 빌드(mcelf 생성)·flash 경로 해소·리네임 잔재 0건 확인. **실보드 flash/부팅은 새 노트북에서 실검증 예정.**

### 예상 마찰점 (실테스트 실패 시 진단 순서)

1. gmake/SDK 경로 미해소 → `config.mk` 3줄 또는 env 확인
2. flash 스크립트 `run.bat` 없음 → `CCSnode_8kw.ps1:12` 하드코딩 불일치
3. **SBL 부팅 실패** → LP prebuilt가 8kw 보드 OSPI 핀맵과 안 맞을 가능성 (LP 기본 prebuilt 그대로 쓴 건지 8kw 보드용 재빌드인지 미확인)
4. 무부팅 → 부트모드 스트랩 SW1=0011 우선 의심 ([[ospi_boot_mode_strap]])

### ~~cleanup 브랜치 (미시작)~~ — ✅ **심화 정리 완료 (2026-06-17, branch cleanup, 23b12bb→dd2bbdd)**

`cleanup` 브랜치에서 브링업 임시 파일 전량 정리 완료 (1차 + 심화 정리 5개 커밋). **코드 변경 없음** — 파일/디렉터리 삭제 + `.gitignore` 정비 + `build/` gmake 파일 추적 + `scratch/` 컨벤션 도입.

- **23b12bb (1차)**: 임시 측정·진단 산출물 정리, `build/makefile`·`build/config.mk` git 추적, `scratch/` 컨벤션 도입.
- **21f7586**: SDK 예제(`enet/sdl`) 잔재 제거, CCS 생성물(`Release/makefile`·`Release/syscfg/`) 추적 해제, Rhino legacy flash 3종·미사용 code-coverage 스킬 제거.
- **558805e**: 구 레이아웃 고아 트리(`Release/src/bsp`, `Release/build`, `Release/tools` 미러) 삭제, `.cproject` MAP_FILE 산출물명 `hello_world`→`${ProjName}` 정정.
- **96a2500**: docs — 구 리포트 삭제, 보드 회로도 PDF 추적 추가.
- **dd2bbdd**: `.claude/skills` gitignore, CCS exclude-from-build(`docs|tools|build`) `.cproject` 영속화 반영.

#### cleanup 정책 (확정, 앞으로의 규칙)

- **임시 측정/진단 산출물** (Logic2 CSV·`.sal`·일회성 캡처)은 전부 repo 루트 `scratch/` 하나로. `verify_*/`·`dt*/` 식 패턴 나열은 폐기.
- **CCS+SysConfig 자동생성물** (`Release/makefile`, `Release/syscfg/`, `.clangd`, `syscfg_c.rov.xs`)은 git 추적 안 함 (`.gitignore`). 빌드 시 `example.syscfg`에서 재생성.
- **GUI 수제 gmake 빌드 시스템** (`build/makefile`, `build/config.mk`)은 추적 유지. `build/` 산출물(`generated/`·`obj/`·`*.lnkxml` 등)만 ignore.
- **루트 비소스 폴더** (`build/`·`tools/`·`docs/`)는 CCS에서 Exclude from Build, `.cproject` `sourceEntries`에 영속화됨 → `Release/` 하위 미러 트리 재생성 차단.

ADC 잔여는 스펙·HW 대기로 막혀 있어, **GPIO 검증 완료 후 다음 활성 트랙은 PWM P3 보호**.

### 다음 활성 트랙 — PWM 전력제어 (작업 호 [[pwm]], **P1 ✓ + P2 완전 완료** — 단일소스·스윕·85kHz·EPWM0 fan-out+isoform·4-DT sweep PASS)

**핀맵 4핀 확정·실측(2026-06-09, 커밋 `6e6b342` branch pwm, 정본 [[pwm_pinmap]])**: 풀브리지 인버터 4채널, 인스턴스 3개 —
- **레그1 = EPWM2 단일 모듈**: EPWM2_A=HS1@J4.39, EPWM2_B=LS1@J4.40 (UG·실측 일치).
- **레그2 = EPWM4+EPWM7 두 모듈**: EPWM4_A=HS2@J6.52 (`ug:1641`), **EPWM7_B=LS2@J6.51** (`ug:1640` + pinmux.csv F1=EPWM7_B 교차확인). 4핀 전부 실측 확정.
- ⚠️ **회로도 net 라벨("EPWM4_B"/"EPWM7_A")과 silicon 채널 suffix 반대** — 펌웨어 정본=silicon 채널(EPWM4_A/EPWM7_B), 라벨에 끌려가지 말 것([[pwm_pinmap]]).

스펙: **주파수 85 kHz 고정 — 구현·실측 확정(d01fc0a, 85.032 kHz 측정)**, **dead-time만 가변(build-per-change, 100~400 ns 조정·실험 후 고정)**. UART5(EPWM15) 무충돌.

#### ✓ 85 kHz 고정 + dead-time config 분리 + EPWM0 fan-out + 레그2 동형화 (commit `d01fc0a`·`4014901`, 실보드 검증 PASS)

P1·P2(150/300ns 단일소스) 위에 **주파수 확정값(85 kHz) 반영 + 튜닝 knob 파일 분리**를 얹어 검증 완료.

- **주파수 85 kHz 고정 (브링업 100 kHz → 확정)**: `TBPRD 1000→1176`, `cmpA 500→588`, `EPWM7 CMPB 470→558`. (`TBPRD = 200MHz/(2·85kHz) = 1176`, UP_DOWN; `CMPB = TBPRD/2 − DT_COUNTS = 588 − 30` @150 ns.)
- **dead-time 단일소스 위치 이전**: ~~`eta_pwm.h ETA_DEADTIME_NS`~~ → **`src/eta_bsp/eta_tuning.h`의 `ETA_DEADTIME_NS`** 로 이전. 유효범위 **100~400 ns, 이탈 시 `#error`로 빌드 차단**. HW 엔지니어가 **이 파일 한 줄만** 바꿔 재빌드하면 `ETA_DEADTIME_COUNTS`·EPWM7 CMPB 등 파생값 자동 추종.
- **런타임 override → SysConfig 재생성 면역**: 주파수(TBPRD/cmpA)·dead-time **모두 `eta_pwm_init()`이 런타임에 override** → `example.syscfg` 재생성으로 SysConfig 기본값이 덮여도 면역. **`example.syscfg`는 안 건드림.**
- **TBCLK = 200 MHz 실측 확정**: 85.032 kHz 측정(계산 TBPRD=1176과 일치) + P1의 100 kHz@TBPRD=1000. **더 이상 "전제"가 아니라 확정 사실** (1 count = 5 ns).
- **검증(Saleae 4ch: ch0=HS1 J4.39 / ch1=LS1 J4.40 / ch2=HS2 J6.52 / ch3=LS2 J6.51, dead-time 100/150/400 ns 스윕, 전 주기 측정)**:
  - 주파수: 세 파일 모두 **85.032 kHz**(+0.002%, 주기 11.7603 µs, 지터 σ≈0.74 ns).
  - duty(HS): 49.15/48.73/46.60% — **`50% − dt/T` 공식 정확히 추종**(AHC 정상 동작, **결함 아님**).
  - dead-time: 100/150/400 ns **완벽 선형 추종**(20/30/80 counts). 레그1 오차 ~0(σ<1 ns).
  - shoot-through: **양 레그 전 주기 0건**. 최소 DT 89 ns로 양수 마진.
  - **판정: PASS.**
- ✅ **EPWM0 fan-out + 레그2 동형화 (`4014901`)**: output-less EPWM0(SysConfig 인스턴스) → EPWM2/4/7 전부 1-hop. 비대칭 ~22 ns → **±2 ns**. isoform: HS2 CMPA=TBPRD/2+DT / LS2 CMPA=TBPRD/2−DT(양방향 DT). 4-DT sweep(100/150/250/400 ns) 전 항목 PASS, 4에지 시차 ≤2 ns, shoot-through 0. 리포트 [[pwm_leg2_isoform_report]].
- ✅ **dead-time knob flash+boot silicon 검증 (2026-06-12)**: `ETA_DEADTIME_NS` → flash → VCC 전원사이클 → silicon 핀. 100/150/250/400 ns 4점 **16/16 PASS** (최대 오차 1.98 ns, shoot-through 0). production 기본값 **150 ns 확정**. 리포트 [[pwm_deadtime_knob_verify]].

✅ **레그2 두 모듈 SYNC 상보·dead-time 해결**(플랫폼 정본 [[am263p_epwm_module_sync_deadtime]]): EPWM4 syncout(ON_CNTR_ZERO)→EPWM7 syncin·phaseShift=0 위상정렬 + EPWM7_B AQ 반전 + **CMPB 오프셋(`CMPB=TBPRD/2−DT`, 부호 `−` 엄수 — +면 shoot-through)**. 레그1(dead-band)과 비대칭.

**P1 완료 (4/4, 실보드 검증)** — 실측 100kHz, HS2 50%/LS2 47%, dead-time 150ns 양 edge, **shoot-through 0**(Saleae 125MS/s, 13,421주기 전수 스캔):
- ✓ **Pin1 HS1(EPWM2_A→J4.39)** — 99.997kHz/49.998%(n=10223). force_io 없이 핀먹스만으로 출력(정본 [[am263p_epwm_primary_pad_no_force_io]]).
- ✓ **Pin2 LS1(EPWM2_B→J4.40)** — 레그1 EPWM2 모듈 내 dead-band 상보.
- ✓ **Pin3 HS2(EPWM4_A→J6.52)** — EPWM4=EPWM2와 독립 인스턴스(base `CSL_CONTROLSS_G0_EPWM4_U_BASE`), 자유구동 단독 검증 후 SYNC 결선.
- ✓ **Pin4 LS2(EPWM7_B→J6.51)** — 레그2 모듈간 SYNC+CMPB 오프셋 상보.
- ✅ **게이트 극성 active-high 가정 실증**(4핀 상보·dead-time·shoot-through 0 정상). 단 회로도 원본 미확인.
- ✅ **P2 dead-time 단일소스 통일·스윕 검증 완료(`8046744`)**: 두 레그 모두 `ETA_DEADTIME_NS` 하나로 수렴(레그1 dead-band RED/FED·레그2 CMPB 오프셋), 150/300ns 두 빌드 4ch 실측 통과(레그1 150.3→300.4ns·레그2 150.0→300.0ns, shoot-through 0). 상세·검증표 [[pwm]] §dead-time 단일소스. (단일소스 위치는 이후 `d01fc0a`에서 `eta_tuning.h`로 이전.)
- ✅ **85 kHz 고정 + dead-time config 분리(`d01fc0a`)**: 위 §85 kHz 고정 절 — 85.032 kHz 실측, dead-time 100/150/400 ns 스윕 PASS(shoot-through 0), `eta_tuning.h` knob 분리·`#error` 범위가드, 런타임 override로 SysConfig 면역.
- 다음: **dead-time 최종값 고정**(현재 150 ns 베이스라인 — 전력단 브링업 때 100~400 ns 중 확정) → **P3 보호(trip-zone)** → **P4 제어루프 + ADC SOC 트리거 RTI→EPWM 전환** / 게이트 극성 회로도·보호신호 스펙 확보. 상세 [[pwm]].

> **ADC 트리거 관련**: 현재 ADC는 RTI1 트리거 유지. PWM 완료 후 P4에서 **ADC SOC 트리거를 EPWM으로 전환 예정** — 지금은 RTI 그대로.

### ADC 잔여 (스펙/HW 대기)

1. **A3 신호별 스케일링 (블로커 유지)** — raw→mV(3.3V/4095)까지만. 물리량(°C/V/A) 변환은 센서 스펙 입수 후. 필요: Temp_Module1/2(V/°C), GA_Vin 분압비, I_LCC_SEN·I_COIL_SEN·GA_Iin_SEN 감도(mV/A)·오프셋. → **PWM P0 스펙과 함께 묶어 확보하면 효율적**.
2. **UART5 PC 텔레메트리 PASS (2026-06-11)** — 단독 루프백(2026-06-10) 위에 **18B 바이너리 패킷 송출 + PC GUI** 얹어 실보드 검증(COM13, 10.067 Hz, 301프레임 0드롭/0CRC). 정본 [[uart5_packet_protocol]]·[[pc_monitor_gui]]. 잔여: **송신 논블로킹화**(현재 polled blocking) + **Phase 2** = 8kw 보드 결합 시 RS-485 차동(THVD1400 U13 DE, `EN_485`=GPIO91=J5.48, [[lp_am263p_uart_epwm_mux]]).
3. **A4 실보드 교차검증** — 멀티미터 기준값으로 6채널 ADC 출력 오차 정량화 (A3 스케일링 후).

## 구현 현황

| 기능 | 상태 | 메모 |
|------|------|------|
| CCS 프로젝트 스캐폴드 (A0 전제) | ✓ | hello_world 기반, Release 빌드 통과 |
| eta_bsp 레이어 도입 | ✓ | `src/eta_bsp/`, eta_ 접두·_loop 접미 (a655de4, edddc31) |
| 단채널 실보드 검증 (A1) | ✓ | AIN0, RTI 1 kSPS + EOC ISR (2026-06-05) |
| UART 출력 1초 주기화 (A1.5) | ✓ | RTI2 독립 타이머 → flag → eta_uart5_loop. 주기=SysConfig nsecPerTick0(단일 진실원천) (8b85bda) |
| ADC 6채널 완성 (A2) | ✓ | 5 인스턴스(ADC0~4), 6채널 raw→mV 실보드 검증. AIN 핀 hard `$assign` 승격 (c512e3b) |
| eta_adc.c 테이블 주도 리팩토링 | ✓ | ISR/init/loop 통합, 332→232줄, 동작 불변 (c512e3b) |
| 신호별 스케일링 (A3) | ? | 센서 스펙 미입수 — 블로커 |
| **UART5 PC 텔레메트리 (바이너리 패킷 + GUI)** | ✓ | branch uart5(ba241fa·979699d). 18B 패킷(SOF/LEN/TYPE/SEQ/raw×6/CRC-16) RTI2 10Hz + PC GUI(`tools/gui/gui.py`). 실보드 COM13 10.067Hz·301프레임·0드롭/0CRC. 정본 [[uart5_packet_protocol]]·[[pc_monitor_gui]] |
| UART5 차동 송신 (RS-485) | △ | 단독 루프백 PASS(TCA6416 P00/P14=LOW, J1.4↔J1.3, 2026-06-10). **485_EN DE 자동 토글 구현 완료(branch gpio)**. 잔여 = 8kw 보드 결합 RS-485 차동 검증 |
| **UART5 양방향 확장 (TYPE=0x02·0x10)** | ✓ | GPIO 상태 TX(TYPE=0x02 7B)·GPIO 커맨드 RX(TYPE=0x10 8B) 구현·실보드 왕복 검증 완료(2026-06-16). GUI GD_EN ON→GPIO93 HIGH Logic2 실측. UART5 RX 1바이트 fix([[uart5_rx_polled_1byte]]). 정본 [[uart5_packet_protocol]]·[[gpio_impl]] |
| 실보드 교차검증 (A4) | ✗ | 멀티미터 기준값 교차 (A3 후) |
| **PWM 전력제어 (P0~P4)** | ✓ (P1 4/4·P2 **완전 완료**·knob flash검증 ✓) | [[pwm]]. **4핀 HS1/LS1/HS2/LS2 ✓실보드 검증**. P2: `ETA_DEADTIME_NS` 단일소스(`8046744`). `d01fc0a`: 85kHz 고정(85.032kHz)·config 분리. **`4014901`: EPWM0 fan-out + isoform — ±2 ns, 4-DT sweep PASS**. **knob flash+boot silicon 검증(2026-06-12): 16/16 ≤2 ns, production 150 ns 확정**. 다음 P3 보호. 핀맵 [[pwm_pinmap]]. 리포트 [[pwm_leg2_isoform_report]]·[[pwm_deadtime_knob_verify]] |
| **GPIO 출력 (485_EN·GD_EN_seed)** | ✓ | `eta_gpio.{c,h}` 구현·실보드 검증(2026-06-16). GPIO91(J5.48) 10Hz 펄스·GPIO93(J4.33) HIGH 확인. PADCONFIG 런타임 mux + TCA6416A PRU_MUX_SEL. 핀맵 [[gpio_pinmap]], 구현 [[gpio_impl]] |
| **툴체인 gmake 스택업 (ccs2050→ccs2100)** | △ | branch `toolchain-ccs21-sdk2606`(5a5fa44, 2026-06-19). gmake `.out`+`.mcelf` 신 스택 경고 0 빌드 성공. 실보드 부팅 검증·CCS GUI Phase 2 미완. 정본 [[sdk_ccs_toolchain_migration]] |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 추가 정보 필요 / `✗` 미구현

## 미결 사항

- **[다음 단계] toolchain 실보드 부팅 검증**: branch `toolchain-ccs21-sdk2606`. `run_flash_node_8kw.ps1 -Source build` → SW1=0011 파워사이클 → standalone 부팅·기능 스모크(PWM/ADC 무회귀). 전제: CCS21 IDE 종료·JTAG·Logic2. 정본 [[sdk_ccs_toolchain_migration]]·[[ospi_boot_mode_strap]].
- **CCS GUI Phase 2 마이그레이션 (사용자 IDE 작업)**: `.cproject` 아직 구스택(`sysconfig:1.27.0`, `MCU-PLUS-SDK-AM263PX:26.0.0.01`, `superClass TMS470_TICLANG_4.0`). 실보드 검증 통과 후 진행. Project Properties → 제품·컴파일러 변경 또는 구 제품 제거 → 마이그레이션 다이얼로그 → `.cproject`/`.ccsproject` 재생성 → diff 커밋. [[sdk_ccs_toolchain_migration]] §6.
- **.codex/ gitignore 추가 검토**: branch `toolchain-ccs21-sdk2606` commit 5a5fa44에서 제외됨. `.gitignore`에 `/.codex/` 추가 여부 결정 필요.
- ~~**cleanup 브랜치 (미시작)**~~ — ✅ **심화 정리 완료(2026-06-17, 23b12bb→dd2bbdd)**: 1차(임시 산출물·`scratch/` 컨벤션) + 심화 4커밋(SDK 잔재·CCS 생성물 추적해제·고아 트리 삭제·회로도 PDF 추적·`.cproject` CCS exclude 영속화). 확정 정책 → §cleanup 정책 참고.
- **tools/jtag_flash 정리 (다음 세션 예정)**: 폴더명 적정성 점검 + flash 경로 이원화 정책 수립(CCS/Release 개발자용 vs GUI/build HW 엔지니어용). 별도 세션에서 진행.
- ~~GPIO 출력 미구현~~ — ✅ **완료(2026-06-16, branch gpio)**: `eta_gpio.{c,h}` 구현. GPIO91(J5.48) 10Hz 펄스·GPIO93(J4.33) HIGH 실보드 확인. PADCONFIG 런타임 mux + TCA6416A PRU_MUX_SEL. 상세 [[gpio_impl]].
- ~~**GUI GPIO Control 왕복 검증 잔여**~~ — ✅ **완료(2026-06-16)**: GUI GD_EN ON → TYPE=0x10 → `eta_gpio_loop()` → GPIO93 HIGH. Logic2 실측 확인. branch gpio 커밋 예정.
- **A3 센서 스펙 미입수 (블로커 유지)**: mV→물리량(°C/V/A) 변환 코드 전무. `eta_adc_loop`은 raw·mV까지만. Temp_Module1/2 출력 특성(V/°C), GA_Vin 분압비, I_LCC_SEN·I_COIL_SEN·GA_Iin_SEN 감도(mV/A)·오프셋 모두 미입수.
- **UART5 송신 논블로킹화 (신규 잔여)**: 현재 패킷 송신이 **polled blocking**(`eta_uart5.c`). 제어루프와 병행하려면 콜백/DMA 논블로킹 전환 필요. ([[uart5_packet_protocol]] §전송)
- **UART5 Phase 2 — 8kw 보드 결합 RS-485 차동 (잔여)**: 단독 루프백(2026-06-10)·PC 텔레메트리(2026-06-11) PASS. **DE 자동 토글(`EN_485`=GPIO91) 구현 완료(2026-06-16)**. 잔여 = 8kw 보드 결합 시 THVD1400 U13 차동 라인 실물 검증. 정본 [[lp_am263p_uart_epwm_mux]]·[[uart5_packet_protocol]]·[[gpio_impl]].
- **UART5 PC 도달 경로 제약 (참조)**: UART5는 온보드 XDS110 가상 COM에 안 실리고 **외부 CP210x(COM13, J1.4→THVD1400→J24)로만** PC 도달. ([[pc_monitor_gui]])
- **물리량 변환 계수 미입수 (GUI Physical placeholder)**: A3 센서 스펙과 동일 블로커. GUI Physical 컬럼은 계수 테이블 단일 소스라 입수 시 한 곳만 수정(GA_Vin `— V`·전류 3채널 `— A`·온도 `—`). ([[pc_monitor_gui]]·[[adc_pinmap]])
- ~~UART 출력 채널 하드코딩~~ — ✅ **해소(branch uart5)**: 구 `eta_uart5.c` 채널별 `DebugP_log` 텍스트 라인 → `eta_packet.c` 채널 루프 직렬화로 대체. ADC 채널 추가 시 출력 라인 수동 추가 불요(eta_adc.c 테이블과 동일하게 자동 추종).
- ~~PWM 레그1 dead-time 단일소스 통일~~ — ✅ **해결(`8046744`)**: 두 레그 모두 `ETA_DEADTIME_NS` 하나로 수렴. 레그1=`eta_pwm_init()`이 `EPWM_setRisingEdgeDelayCount`/`setFallingEdgeDelayCount`로 RED/FED(=ETA_DEADTIME_COUNTS, SysConfig 기본 override), 레그2=CMPB 오프셋. 150/300ns 4ch 실측(레그1 150.3→300.4·레그2 150.0→300.0ns, shoot-through 0). 상세 [[pwm]] §dead-time 단일소스. (`d01fc0a`에서 단일소스 위치를 `eta_tuning.h`로 이전.)
- ~~PWM 주파수 85 kHz 고정 / dead-time config 분리~~ — ✅ **완료(`d01fc0a`)**: 85.032 kHz 실측, dead-time 100/150/400 ns 스윕 PASS(shoot-through 0). 단일소스 `eta_tuning.h ETA_DEADTIME_NS`(100~400 ns `#error` 가드), 주파수·dead-time 모두 `eta_pwm_init()` 런타임 override로 SysConfig 면역.
- ~~PWM dead-time 최종값 미고정~~ — **✅ 해결(2026-06-12)**: flash+boot silicon 검증 완료 후 **`ETA_DEADTIME_NS = 150U` production 기본값 확정**. 100~400 ns 전 범위 실측 PASS([[pwm_deadtime_knob_verify]]). 전력단 브링업에서 재조정 가능하나 현재 정본은 150 ns.
- ~~PWM 레그2 dead-time 비대칭~~ — **✅ 해결(`4014901`)**: EPWM0 fan-out + isoform으로 ~22 ns → **±2 ns**. 최소 갭 ≥ 98 ns. 보드 단계 단일모듈화는 여전히 미래 개선 후보([[pwm_pinmap]] §향후). ([[am263p_epwm_module_sync_deadtime]])
- **빌드 환경 주의 (HW 엔지니어 워크플로우)**: CCS 생성 `Release/makefile`·`Release/syscfg/`는 git 추적 안 함(`.gitignore`). **다른 노트북에서 git clone 후엔 CCS로 프로젝트 import**(=makefile·syscfg 로컬 재생성)해서 빌드. `build/makefile`·`build/config.mk`는 git 추적 유지 — HW 엔지니어 GUI gmake 워크플로우용. 단 **`eta_tuning.h` 변경은 순수 C 컴파일로 반영**되어 syscfg 재생성 불요 — 런타임 override 방식의 이점. `docs/`·`tools/`·`build/`는 CCS Exclude from Build(`.cproject` 영속화) → `Release/` 하위 미러 트리 재생성 차단됨.
- **PWM 회로도 net 라벨 함정 (정본 기록 유지)**: 회로도 net 라벨("EPWM4_B"/"EPWM7_A")과 silicon 채널(EPWM4_A/EPWM7_B) suffix **반대** — 펌웨어 정본=silicon 채널(UG Mode0·pinmux.csv 교차확인). 라벨에 끌려가지 말 것([[pwm_pinmap]]).
- **PWM 게이트 극성 회로도 미확인**: active-high 가정으로 4핀 검증 통과(shoot-through 0) → 가정 실보드 실증. **회로도 원본으로 극성 확인은 잔여**. shutdown 입력 미확인.
- **PWM 잔여 스펙**: ~~스위칭 주파수~~ **85 kHz 고정·구현·실측 확정(`d01fc0a`)**. ~~dead-time 단일소스/스윕 인프라~~ ✅ 완료. 잔여 = **보호(trip) 신호 소스 미정(P3 선결)** · dead-time 최종값 고정(위 항목).
- ~~레그2 두 모듈 동기 dead-time 비표준 구현~~ — **해결**(EPWM4→EPWM7 SYNC+CMPB 오프셋, shoot-through 0 실측). 단 향후 보드 리비전 시 한 모듈로 묶도록 수정 요청 예정([[pwm_pinmap]] §향후).
