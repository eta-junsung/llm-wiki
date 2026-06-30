---
date: 2026-06-30
---



# 8kw-ev-wpt-tx — 구현 현황

> 전략 spine은 [[roadmap]], 작업 단위 호는 [[adc]]·[[pwm]].
> ⚠️ ADC 상태는 **branch `adc`의 커밋된 상태에서 코드로 역산**한 것 (commit c512e3b, origin/adc). **A3.5 트리거 EPWM0_SOCA 전환 + PPB HW 평균은 main에 PR #6 `d673e74`로 머지**(feature/adc-trigger-epwm0의 3e5f117·4cffbe1·532e0eb), HW 검증으로 **N=64 확정**. PWM 상태는 **branch `pwm`**(최신 = commit **d01fc0a** — 85 kHz 고정 + dead-time config 분리). UART5 PC 텔레메트리는 **branch `uart5`**(commit **ba241fa**·**979699d**, 실보드 검증 2026-06-11). 프로젝트 트리에 status.md는 없음 — status는 wiki 측에만 존재한다.

## 소스 레이아웃

**PR #5 (`feature/firmware-layering`, `0830b5f`·`9cd0181`, 2026-06-25)에서 BSP·HAL·ALG·App 4레이어로 전면 재구성 완료.** 동작 불변(순수 재구성), 실보드 검증 통과. 구조 상세 → [[firmware_layering_8kw]].

```
src/
├── bsp/   # 부팅 1회 init · 레지스터 · IOMUX  (eta_bsp_iomux/adc/pwm/gpio/uart)
├── hal/   # 동작 중 SDK 래핑 (ADC_/EPWM_/GPIO_/UART_)  (eta_hal_adc/gpio/uart)
├── alg/   # 순수 계산, 하드웨어 무관  (eta_alg_crc, eta_alg_convert)
└── app/   # 오케스트레이션  (main, eta_app_adc/protocol/io)
```

- **의존 방향 불변식**: ALG는 HAL·SDK·레지스터를 모른다. HAL과 ALG가 만나는 자리는 App뿐.
- **네이밍**: `eta_<layer>_<module>_<verb>()` / 파일 `eta_<layer>_<module>.c/.h`. `main()`만 예외(C 진입점).
- **PWM tuning knob**: `src/bsp/eta_bsp_pwm.h`의 `ETA_BSP_PWM_DEADTIME_NS` 단일 소스 (`eta_tuning.h` → `eta_bsp_pwm.h`로 이전됨).
- **gui.py 비자명 결합**: `gui.py:74` regex가 `ETA_BSP_PWM_DEADTIME_NS`를 직접 편집 — 매크로 개명·파일 이동 시 반드시 함께 갱신. 확인은 `gui.py --read` 라운드트립으로.

## 직전 완료 — A3.5: ADC 트리거 EPWM0_SOCA 전환 + PPB HW 평균 N=64 (main PR #6 `d673e74`, HW 검증, 2026-06-26)

6채널 노이즈를 **CPU-free HW 평균**으로 처리. 트리거 RTI1(1 kSPS) → **EPWM0_SOCA(85.032 kHz)**, 방식 = **PPB 누적 평균**(repeater 안 씀). HW 노이즈 측정으로 **N=64 확정**(feature/adc-trigger-epwm0 3커밋 → main #6):

- **`3e5f117` 트리거 전환**: 6 SOC 전부 `soc0Trigger=ADC_TRIGGER_EPWM0_SOCA`(`example.syscfg`:70 등). RTI 카운터 시작 코드 제거(`eta_bsp_adc.c`:194). EPWM0(=CONFIG_EPWM0)는 `4014901` 도입 output-less fan-out 마스터, SOC_A 트리거 `EPWM_SOC_TBCTR_ZERO`(`example.syscfg`:228–229). ★RTI의 `enableIntr0` export 게이트 함정은 **EPWM에 적용 안 됨** — `ETSEL.SOCAEN`이 트리거 XBAR 직접 출력. ★실효 85 kHz는 런타임 override(`eta_bsp_pwm.c`:19 TBPRD=1176)에서 — syscfg 정적 period=1000은 100 kHz. 정본 [[am263p_adc_rti_trigger]] §5.
- **`4cffbe1`+#6 PPB 평균 N=64**: 6채널 PPB 누적 평균. ISR을 EOC→OSINT로(`ADC_readResult`→`ADC_readPPBSum`). 출력 1.33 kHz, 노이즈 √64=÷8, 그룹지연 ~370 µs. ADC1은 SOC0+SOC1 lockstep(OSINT2→INT1). 정본 [[am263p_adc_ppb_averaging]].
- **`532e0eb` N 단일 손잡이**: `eta_bsp_adc.h:28` `ETA_ADC_OVERSAMPLE_LOG2 (6U)` 매크로 하나로 N 제어(6→64, 5→32, ≤10, `_Static_assert`). `eta_bsp_adc_init()`이 전 PPB에 limit/shift 런타임 적용. GUI 통합 없음 — 코드 직접 수정 후 재빌드-flash.
- **repeater 미채택 근거**: 과전류·과전압 보호는 HW 비교기 담당 + 조정루프 대역폭 수백 Hz↓ + 85 kHz에서 repeater **N=64**는 64×285 ns ≈ 18.2 µs > 11.76 µs 주기로 변환시간 예산 초과(정밀 산정 2026-06-29, [[am263p_adc_instance_allocation]] §변환시간 예산 & 리피터 N 상한). ★ **단 기각된 건 N=64이지 리피터 자체가 아님 — N ≤ ~41은 예산 내라 저-N 리피터는 살아있는 선택지**(A5 샘플링 재작업 시 후보).
- **검증 ✓**: 6채널 0/3.3V 추종 OK, OSINT ISR 1.33 kHz 실측 OK, **HW 노이즈 측정으로 N=64 채택**(√64=÷8). A3.5 완료 — 남은 ADC 일은 A4 교차검증.

## 직전 완료 — 펌웨어 4레이어 재구성 (PR #5, 동작 불변, 2026-06-25)

PR #5 (`feature/firmware-layering`, commits `0830b5f`·`9cd0181`). 단일 `src/eta_bsp/` → `src/{bsp,hal,alg,app}/` 4레이어 전면 재구성. 변경 사항:

- **CRC16 통합**: 중복 구현 → `eta_alg_crc16` 단일(동일 다항식·init 유지).
- **raw→mV**: `eta_alg_convert`로 추출. 상수 불변(`raw*3300/4095`).
- **tuning knob 위치 이전**: `ETA_DEADTIME_NS` in `eta_tuning.h` → `ETA_BSP_PWM_DEADTIME_NS` in `src/bsp/eta_bsp_pwm.h`.
- 실보드: ADC·GPIO·PWM deadtime 전부 동일 동작 확인. 디스어셈블로 deadtime 값 바이너리 박힘 확인.

구조 상세 → [[firmware_layering_8kw]].

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

## 직전 완료 — 툴체인 신스택 전환 완전 완료 (2026-06-19, end-to-end PASS)

Phase 1(gmake) 위에 Phase 2(CCS managed build·환경 정리) 완료, 실보드 end-to-end 검증 PASS.

- **CCS managed build Phase 2**: `.cproject` 신스택(CCS21/SDK_06/SysConfig1.28/TICLANG5.1.1)으로 전환. sourceEntries 재추가 entry 제거(중복심볼 해소). All Configurations 적용. 정본 [[syscfg_build_model]] §④⑥.
- **`C:\ti` 구스택 정리**: ccs2050·uniflash·구 SDK(26_00_00_01)·standalone sysconfig_1.27.0·ti_cgt_arm_llvm_4.0.4.LTS 등 ~12.2 GB 삭제. 신스택만 잔존. 정본 [[sdk_ccs_toolchain_migration]] §8.
- **SBL 신스택 prebuilt 갱신**: SDK_06 prebuilt(307,005B, 해시 상이 = cert serial/timestamp 차이, 기능 동등) → `C:/ti/sbl_ospi_am263p.tiimage`. 정본 [[ospi_boot_console_diagnostic]] §4.
- **`gui.bat` 무터미널 런처 + `launch_gui.ps1`**: ASCII 전용 `.bat` 래퍼 → UTF-8 BOM `.ps1` 위임. 정본 [[windows_bat_ps1_launcher]].
- **실보드 end-to-end PASS**: `gui.bat` → deadtime 변경 → flash → 전원사이클 standalone 부팅 → deadtime 변화 측정 → 회귀 없음.

---

## 다음 작업: ADC A4 교차검증 / A5·A6 샘플링 재작업 → PWM P3

**다음 시작점**: **리피터 버스트(N=16) 노이즈 FFT 실측 → 최종 N / 트리거 위상 결정** (리피터 버스트는 **main 머지 완료, PR#11 `2c4ff85`** — branch 아님). 프로브 포인트·결정 트리·MSOX3104T 설정은 정본 [[adc_noise_fft_probe]] — GA_Vin(J3.26)·GA_Iin(J3.29) DC핀 FFT로 백색(→N↑) vs 스위칭 상관(→트리거 위상; 트리거 고정이라 √N 무효) 판별. 측정 마커는 **이미 코드에 있음**: `6993a40`이 EOC ISR에서 GPIO95(J4.31, 스코프 CH4)를 토글(`ETA_BSP_ADC_DBG_MARK_IDX`, 현재 `0U`=I_COIL_SEN/FOD용 — GA_Vin 노이즈 측정 시 `3U`로 변경). 그 다음 **SW 이동평균 `eta_alg_filter`(ALG) 신설** — ISR write로 먼저 구현해 DMA 검증과 분리(권장순). 로드맵 [[adc]] §A5·§A6, 메커니즘 [[am263p_adc_repeater_burst]].

> **병행 활성 트랙 — FOD 1차 관찰 (`6993a40`, 2026-06-30)**: I_COIL_SEN(ADC0) 버스트 완료 시각을 GPIO95로 관측해 코일전류 노이즈/안정성을 판별(이물 감지 선행). 절차는 코드 repo `docs/fod_i_coil_observation.md`. ⚠️ **잠복 충돌**: `eta_hal_gpio`의 DBG_LOOP도 GPIO95 사용 — 후속 정리 필요(`6993a40` 커밋 메시지 명시).

**A5 진척 — PPB 누적(N=64) → 리피터 버스트 블록평균(N=16) 전환 (main 머지 완료, PR#11 `2c4ff85`, CI pass, 실보드 검증)**: 한 트리거 내 16회 백투백 변환 → PPB 블록평균 → **출력 85 kHz/인스턴스 유지**(N 무관). 스코프 OSINT 85 kHz + 6채널 라이브 검증. **N=16은 현 운영 값**(placeholder 아님; 최종 N 튜닝은 FFT 후). ★ **버스트 전환으로 출력이 85 kHz/인스턴스로 복귀** — 종전 PPB 누적 N=64의 "OSINT 1.33 kHz"(및 코드 주석 "2.66 kHz") 수치는 더 이상 적용 안 됨(라이브 재실측 권장). SDK API·`ADC_configureRepeater` 헤더 결함·HW/SW 필터 직교성 정본 [[am263p_adc_repeater_burst]]. EDMA 적재는 가능 확인(SDK)·채택 보류 [[am263p_edma_adc_offload]].

> **검증 교훈**: 전환 직후 "3채널(ADC0/3/4) 死" 관측 → 死/生 레지스터 byte 동일·재실행 시 정상 → 일시/잔류 상태(이전 플래시 잔재)였고 펌웨어 결함 아님. 레지스터-증상 불일치 시 재현·재플래시 먼저.

A3.5(EPWM0_SOCA 트리거 + PPB *누적* 평균)는 **HW 검증으로 N=64 확정·완료**(main PR #6 `d673e74`). 정본 [[am263p_adc_rti_trigger]] §5·[[am263p_adc_ppb_averaging]]. (ADC 외 활성 트랙은 PWM P3 보호.)

### ✅ 직전 완료 — 새 테스트 머신 fresh-clone 검증 완료

`git clone -b test` → README §1 셋업(CCS2100 + SDK_06 + SBL 복사 + Python 3.10+ + SW1=0011 + SAC off) → `gui.bat` 더블클릭 → end-to-end PASS.

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

> **ADC 트리거 관련**: RTI1→EPWM0 전환·PPB HW 평균을 통합 항목(순위 2)으로 선행 진행. 상세 [[am263p_adc_rti_trigger]] §4.

### ADC 잔여 (스펙/HW 대기)

1. **A3 신호별 스케일링 (블로커 유지)** — raw→mV(3.3V/4095)까지만. 물리량(°C/V/A) 변환은 센서 스펙 입수 후. 필요: Temp_Module1/2(V/°C), GA_Vin 분압비, I_LCC_SEN·I_COIL_SEN·GA_Iin_SEN 감도(mV/A)·오프셋. → **PWM P0 스펙과 함께 묶어 확보하면 효율적**.
2. **UART5 PC 텔레메트리 PASS (2026-06-11)** — 단독 루프백(2026-06-10) 위에 **18B 바이너리 패킷 송출 + PC GUI** 얹어 실보드 검증(COM13, 10.067 Hz, 301프레임 0드롭/0CRC). 정본 [[uart5_packet_protocol]]·[[pc_monitor_gui]]. 잔여: **송신 논블로킹화**(현재 polled blocking) + **Phase 2** = 8kw 보드 결합 시 RS-485 차동(THVD1400 U13 DE, `EN_485`=GPIO91=J5.48, [[lp_am263p_uart_epwm_mux]]).
3. **A4 실보드 교차검증** — 멀티미터 기준값으로 6채널 ADC 출력 오차 정량화 (A3 스케일링 후).

## 구현 현황

| 기능 | 상태 | 메모 |
|------|------|------|
| CCS 프로젝트 스캐폴드 (A0 전제) | ✓ | hello_world 기반, Release 빌드 통과 |
| eta_bsp 레이어 도입 | ✓ | `src/eta_bsp/`, eta_ 접두·_loop 접미 (a655de4, edddc31) |
| **펌웨어 4레이어 재구성 (BSP/HAL/ALG/App)** | ✓ | PR #5 (`0830b5f`·`9cd0181`). 동작 불변 실보드 검증. src/{bsp,hal,alg,app}/. 정본 [[firmware_layering_8kw]] |
| 단채널 실보드 검증 (A1) | ✓ | AIN0, RTI 1 kSPS + EOC ISR (2026-06-05) |
| UART 출력 1초 주기화 (A1.5) | ✓ | RTI2 독립 타이머 → flag → eta_uart5_loop. 주기=SysConfig nsecPerTick0(단일 진실원천) (8b85bda) |
| ADC 6채널 완성 (A2) | ✓ | 5 인스턴스(ADC0~4), 6채널 raw→mV 실보드 검증. AIN 핀 hard `$assign` 승격 (c512e3b) |
| eta_adc.c 테이블 주도 리팩토링 | ✓ | ISR/init/loop 통합, 332→232줄, 동작 불변 (c512e3b) |
| 신호별 스케일링 (A3) | ✓ | 5채널 완료·검증(I_COIL_SEN·GA_Iin_SEN·GA_Vin·Temp×2). I_LCC_SEN 스펙 미입수로 드롭. GUI `PHYSICAL_COEFF` 단일 소스([[adc_scaling]]) |
| **UART5 PC 텔레메트리 (바이너리 패킷 + GUI)** | ✓ | branch uart5(ba241fa·979699d). 18B 패킷(SOF/LEN/TYPE/SEQ/raw×6/CRC-16) RTI2 10Hz + PC GUI(`tools/gui/gui.py`). 실보드 COM13 10.067Hz·301프레임·0드롭/0CRC. 정본 [[uart5_packet_protocol]]·[[pc_monitor_gui]] |
| UART5 차동 송신 (RS-485) | ✓ | 단독 루프백 PASS(TCA6416 P00/P14=LOW, J1.4↔J1.3, 2026-06-10). 485_EN DE 자동 토글 구현 완료(branch gpio). 보드 결합 RS-485 차동 검증 드롭 |
| **UART5 양방향 확장 (TYPE=0x02·0x10)** | ✓ | GPIO 상태 TX(TYPE=0x02 7B)·GPIO 커맨드 RX(TYPE=0x10 8B) 구현·실보드 왕복 검증 완료(2026-06-16). GUI GD_EN ON→GPIO93 HIGH Logic2 실측. UART5 RX 1바이트 fix([[uart5_rx_polled_1byte]]). 정본 [[uart5_packet_protocol]]·[[gpio_impl]] |
| **ADC 트리거 EPWM0_SOCA + PPB HW 평균 (A3.5)** | ✓ | main PR #6 `d673e74`(feature 3e5f117·4cffbe1·532e0eb). RTI1→EPWM0_SOCA 85.032 kHz, PPB **N=64** CPU-free 평균(ISR 1.33 kHz, √64=÷8), `ETA_ADC_OVERSAMPLE_LOG2=6` 손잡이. **HW 노이즈 측정으로 N=64 확정**. 정본 [[am263p_adc_rti_trigger]] §5·[[am263p_adc_ppb_averaging]] |
| 실보드 교차검증 (A4) | ✗ | 멀티미터 기준값 교차 (A3 후) |
| **ADC 실질 샘플링 85 kHz (A5, #7)** | △ | **PPB 누적(N=64) → 리피터 버스트 블록평균(N=16) 전환 main 머지**(PR#11 `2c4ff85`, CI pass), 출력 85 kHz/인스턴스. 스코프 OSINT 85 kHz·6채널 라이브 검증. `ETA_ADC_OVERSAMPLE_LOG2=4U`(`eta_bsp_adc.h:31`). **메커니즘 머지·검증 완료, 최종 N·노이즈 FFT 미완**(△ 유지 = 튜닝 미확정). 측정 마커 GPIO95(`6993a40`). 정본 [[am263p_adc_repeater_burst]]·[[adc_noise_fft_probe]] |
| **SW 이동평균 전환 (A6, #8)** | ✗ | ring buffer 이동평균. A5 선행 필요. CPU 부하 실측(R5F @400 MHz, ~784 사이클/ISR [추정]) + N 튜닝 |
| **PWM 전력제어 (P0~P4)** | ✓ (P1 4/4·P2 **완전 완료**·knob flash검증 ✓) | [[pwm]]. **4핀 HS1/LS1/HS2/LS2 ✓실보드 검증**. P2: `ETA_DEADTIME_NS` 단일소스(`8046744`). `d01fc0a`: 85kHz 고정(85.032kHz)·config 분리. **`4014901`: EPWM0 fan-out + isoform — ±2 ns, 4-DT sweep PASS**. **knob flash+boot silicon 검증(2026-06-12): 16/16 ≤2 ns, production 150 ns 확정**. 다음 P3 보호. 핀맵 [[pwm_pinmap]]. 리포트 [[pwm_leg2_isoform_report]]·[[pwm_deadtime_knob_verify]] |
| **GPIO 출력 (485_EN·GD_EN_seed)** | ✓ | `eta_gpio.{c,h}` 구현·실보드 검증(2026-06-16). GPIO91(J5.48) 10Hz 펄스·GPIO93(J4.33) HIGH 확인. PADCONFIG 런타임 mux + TCA6416A PRU_MUX_SEL. 핀맵 [[gpio_pinmap]], 구현 [[gpio_impl]] |
| **툴체인 신스택 전환 완전 완료 (ccs2050→ccs2100)** | ✓ | branch `toolchain-ccs21-sdk2606`(2026-06-19). gmake/GUI/CCS IDE 3경로 신스택 + 실보드 end-to-end PASS. C:\ti 구스택 정리(~12.2GB). 정본 [[sdk_ccs_toolchain_migration]]·[[syscfg_build_model]] |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 추가 정보 필요 / `✗` 미구현

## 미결 사항

### 결정된 다음 작업 (2026-06-24 업무보고, 우선순위순)

1. ~~**GUI 값 소수점 세 자리 표시 (순위 1)**~~ — ✅ **완료(2026-06-26)**: `tools/gui/gui.py` ADC(V)/Physical 컬럼 소수점 3자리 포맷 변경.
2. ~~**ADC SOC 트리거 RTI1→EPWM0 전환 + PPB HW 평균 필터 (순위 2)**~~ — ✅ **완료(2026-06-26, main PR #6 `d673e74`)**: EPWM0_SOCA 85.032 kHz 트리거 + PPB **N=64** HW 평균(CPU-free, ISR 1.33 kHz) + `ETA_ADC_OVERSAMPLE_LOG2=6` N 손잡이. **HW 노이즈 측정으로 N=64 확정**(√64=÷8). 정본 [[am263p_adc_rti_trigger]] §5·[[am263p_adc_ppb_averaging]]. 상세 §직전 완료.
3. **ADC 샘플링 재작업 (승격 2026-06-29)**:
   - **A5 (#7 ADC 실질 샘플링 85 kHz)** — △ 부분완료: 리피터 버스트(N=16)로 전환·검증(branch), 출력 85 kHz/인스턴스. `ETA_ADC_OVERSAMPLE_LOG2=4U`(`src/bsp/eta_bsp_adc.h:31`). **잔여: FFT 노이즈 실측 + 최종 N 확정**. A4와 [추정] 독립(확인 필요). 로드맵 [[adc]] §A5, 정본 [[am263p_adc_repeater_burst]].
   - **A6 (#8 SW 이동평균 전환 검토)**: SW ring buffer 이동평균 `eta_alg_filter`(ALG) — ISR write로 먼저 구현해 DMA 검증과 분리(권장순). 매 샘플 갱신, 스파이크+노이즈 동시. CPU 부하 실측 필요(R5F @400 MHz, ~784 사이클/ISR [추정]), 윈도우 N 튜닝. DMA(EDMA) 전송은 3단계·게이트 [[am263p_edma_adc_offload]]. 로드맵 [[adc]] §A6.
   - A5·A6은 "HW N↓" ↔ "SW 이동평균 보완" 트레이드오프의 양면.
   - **변환시간 예산 정밀 산정(2026-06-29)**: 1회 직렬 cadence ≈ 285 ns(tSH 80 ns + tEOC 205 ns, Table 7-123 PRESCALE=6), 11.76 µs 주기당 ~**41 변환** 수용 → 리피터 N 상한 ~41(단일채널)/합≤41(ADC1). 종전 ~37(315 ns 보수치)에서 상향. **저-N(≤~41) 리피터는 A5 후보로 살아있음**. 전부 정적 산정·라이브 실측 미수행. 정본 [[am263p_adc_instance_allocation]] §변환시간 예산 & 리피터 N 상한.
4. **GUI 화면 녹화 기능 (순위 4, nice-to-have)**: GUI 라이브 화면 녹화. **최저 우선순위 — 있으면 좋고 없으면 말고.** ([[pc_monitor_gui]])

- ~~**toolchain 실보드 부팅 검증**~~ — ✅ **완료(2026-06-19)**: end-to-end PASS(gui.bat → flash → 전원사이클 → deadtime 측정). 정본 [[sdk_ccs_toolchain_migration]]·[[ospi_boot_mode_strap]].
- ~~**CCS GUI Phase 2 마이그레이션**~~ — ✅ **완료(2026-06-19)**: `.cproject` 신스택 전환, sourceEntries 중복심볼 해소, All Configurations 적용. 정본 [[syscfg_build_model]] §④⑥.
- **.codex/ gitignore 추가 검토**: commit 5a5fa44에서 제외됨. `.gitignore`에 `/.codex/` 추가 여부 결정 필요.
- **gmake 빌드가 `.cproject` 자동 수정하는 side effect**: 빌드 시 `build/obj/release` sourceEntry가 `.cproject`에 자동 추가됨. 원인 추적·억제 또는 "빌드 후 `.cproject` diff 무시" 정책 결정 필요.
- ~~**cleanup 브랜치 (미시작)**~~ — ✅ **심화 정리 완료(2026-06-17, 23b12bb→dd2bbdd)**: 1차(임시 산출물·`scratch/` 컨벤션) + 심화 4커밋(SDK 잔재·CCS 생성물 추적해제·고아 트리 삭제·회로도 PDF 추적·`.cproject` CCS exclude 영속화). 확정 정책 → §cleanup 정책 참고.
- **tools/jtag_flash 정리 (다음 세션 예정)**: 폴더명 적정성 점검 + flash 경로 이원화 정책 수립(CCS/Release 개발자용 vs GUI/build HW 엔지니어용). 별도 세션에서 진행.
- ~~GPIO 출력 미구현~~ — ✅ **완료(2026-06-16, branch gpio)**: `eta_gpio.{c,h}` 구현. GPIO91(J5.48) 10Hz 펄스·GPIO93(J4.33) HIGH 실보드 확인. PADCONFIG 런타임 mux + TCA6416A PRU_MUX_SEL. 상세 [[gpio_impl]].
- ~~**GUI GPIO Control 왕복 검증 잔여**~~ — ✅ **완료(2026-06-16)**: GUI GD_EN ON → TYPE=0x10 → `eta_gpio_loop()` → GPIO93 HIGH. Logic2 실측 확인. branch gpio 커밋 예정.

- **Vref 3.3V 확정**: `ETA_ADC_VREFHI_MV=3300` + 사용자 확인(2026-06-24). [[adc_pinmap]] §ADC 파라미터.

- **UART5 PC 도달 경로 제약 (참조)**: UART5는 온보드 XDS110 가상 COM에 안 실리고 **외부 CP210x(COM13, J1.4→THVD1400→J24)로만** PC 도달. ([[pc_monitor_gui]])

- ~~UART 출력 채널 하드코딩~~ — ✅ **해소(branch uart5)**: 구 `eta_uart5.c` 채널별 `DebugP_log` 텍스트 라인 → `eta_packet.c` 채널 루프 직렬화로 대체. ADC 채널 추가 시 출력 라인 수동 추가 불요(eta_adc.c 테이블과 동일하게 자동 추종).
- ~~PWM 레그1 dead-time 단일소스 통일~~ — ✅ **해결(`8046744`)**: 두 레그 모두 `ETA_DEADTIME_NS` 하나로 수렴. 레그1=`eta_pwm_init()`이 `EPWM_setRisingEdgeDelayCount`/`setFallingEdgeDelayCount`로 RED/FED(=ETA_DEADTIME_COUNTS, SysConfig 기본 override), 레그2=CMPB 오프셋. 150/300ns 4ch 실측(레그1 150.3→300.4·레그2 150.0→300.0ns, shoot-through 0). 상세 [[pwm]] §dead-time 단일소스. (`d01fc0a`에서 단일소스 위치를 `eta_tuning.h`로 이전.)
- ~~PWM 주파수 85 kHz 고정 / dead-time config 분리~~ — ✅ **완료(`d01fc0a`)**: 85.032 kHz 실측, dead-time 100/150/400 ns 스윕 PASS(shoot-through 0). 단일소스 `eta_tuning.h ETA_DEADTIME_NS`(100~400 ns `#error` 가드), 주파수·dead-time 모두 `eta_pwm_init()` 런타임 override로 SysConfig 면역.
- ~~PWM dead-time 최종값 미고정~~ — **✅ 해결(2026-06-12)**: flash+boot silicon 검증 완료 후 **`ETA_DEADTIME_NS = 150U` production 기본값 확정**. 100~400 ns 전 범위 실측 PASS([[pwm_deadtime_knob_verify]]). 전력단 브링업에서 재조정 가능하나 현재 정본은 150 ns.
- ~~PWM 레그2 dead-time 비대칭~~ — **✅ 해결(`4014901`)**: EPWM0 fan-out + isoform으로 ~22 ns → **±2 ns**. 최소 갭 ≥ 98 ns. 보드 단계 단일모듈화는 여전히 미래 개선 후보([[pwm_pinmap]] §향후). ([[am263p_epwm_module_sync_deadtime]])
- **빌드 환경 주의 (HW 엔지니어 워크플로우)**: CCS 생성 `Release/makefile`·`Release/syscfg/`는 git 추적 안 함(`.gitignore`). **다른 노트북에서 git clone 후엔 CCS로 프로젝트 import**(=makefile·syscfg 로컬 재생성)해서 빌드. `build/makefile`·`build/config.mk`는 git 추적 유지 — HW 엔지니어 GUI gmake 워크플로우용. 단 **`eta_tuning.h` 변경은 순수 C 컴파일로 반영**되어 syscfg 재생성 불요 — 런타임 override 방식의 이점. `docs/`·`tools/`·`build/`는 CCS Exclude from Build(`.cproject` 영속화) → `Release/` 하위 미러 트리 재생성 차단됨.
- **PWM 회로도 net 라벨 함정 (정본 기록 유지)**: 회로도 net 라벨("EPWM4_B"/"EPWM7_A")과 silicon 채널(EPWM4_A/EPWM7_B) suffix **반대** — 펌웨어 정본=silicon 채널(UG Mode0·pinmux.csv 교차확인). 라벨에 끌려가지 말 것([[pwm_pinmap]]).

- ~~레그2 두 모듈 동기 dead-time 비표준 구현~~ — **해결**(EPWM4→EPWM7 SYNC+CMPB 오프셋, shoot-through 0 실측). 단 향후 보드 리비전 시 한 모듈로 묶도록 수정 요청 예정([[pwm_pinmap]] §향후).
