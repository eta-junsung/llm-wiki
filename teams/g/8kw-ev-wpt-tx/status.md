---
date: 2026-06-10
---

# 8kw-ev-wpt-tx — 구현 현황

> 전략 spine은 [[roadmap]], 작업 단위 호는 [[adc]]·[[pwm]].
> ⚠️ ADC 상태는 **branch `adc`의 커밋된 상태에서 코드로 역산**한 것 (commit c512e3b, origin/adc). PWM 상태는 **branch `pwm`**(최신 = commit **d01fc0a** — 85 kHz 고정 + dead-time config 분리). 프로젝트 트리에 status.md는 없음 — status는 wiki 측에만 존재한다.

## 소스 레이아웃

- BSP 디렉토리는 **`src/eta_bsp/`** (eta_ 접두가 디렉토리명까지 적용). eta_bsp 레이어 도입 (commit a655de4, edddc31).
- 파일: `src/main.c`, `src/eta_bsp/eta_adc.{c,h}`, `src/eta_bsp/eta_uart5.{c,h}`, **`src/eta_bsp/eta_pwm.{c,h}`**, **`src/eta_bsp/eta_tuning.h`**(신설 — 컴파일타임 튜닝 knob, `ETA_DEADTIME_NS` 단일소스).
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

## 다음 작업: PWM 전력제어 착수(신규 트랙) / ADC 잔여(A3·A4) / UART5 Phase 2(RS-485, 잔여)

ADC 계측(A2)은 완료. ADC 잔여는 스펙·HW 대기로 막혀 있어, **다음 활성 트랙은 PWM**이다.

### 다음 활성 트랙 — PWM 전력제어 (작업 호 [[pwm]], **P1 ✓ + P2 ✓ + 85 kHz/dead-time config 분리 ✓** — d01fc0a)

**핀맵 4핀 확정·실측(2026-06-09, 커밋 `6e6b342` branch pwm, 정본 [[pwm_pinmap]])**: 풀브리지 인버터 4채널, 인스턴스 3개 —
- **레그1 = EPWM2 단일 모듈**: EPWM2_A=HS1@J4.39, EPWM2_B=LS1@J4.40 (UG·실측 일치).
- **레그2 = EPWM4+EPWM7 두 모듈**: EPWM4_A=HS2@J6.52 (`ug:1641`), **EPWM7_B=LS2@J6.51** (`ug:1640` + pinmux.csv F1=EPWM7_B 교차확인). 4핀 전부 실측 확정.
- ⚠️ **회로도 net 라벨("EPWM4_B"/"EPWM7_A")과 silicon 채널 suffix 반대** — 펌웨어 정본=silicon 채널(EPWM4_A/EPWM7_B), 라벨에 끌려가지 말 것([[pwm_pinmap]]).

스펙: **주파수 85 kHz 고정 — 구현·실측 확정(d01fc0a, 85.032 kHz 측정)**, **dead-time만 가변(build-per-change, 100~400 ns 조정·실험 후 고정)**. UART5(EPWM15) 무충돌.

#### ✓ 85 kHz 고정 + dead-time config 분리 (commit `d01fc0a`, 실보드 검증 PASS)

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
- ⚠️ **레그2 dead-time 비대칭(향후 참조)**: 레그2(HS2=EPWM4_A / LS2=EPWM7_B)는 두 모듈 동기라 모듈간 **~11 ns(≈2.2 counts) 고정 위상 스큐** → dead-time이 **HS→LS +11 ns / LS→HS −11 ns 비대칭**(합은 항상 정확히 2×설정값). 레그1(EPWM2 단일 모듈 HW dead-band)은 비대칭 없음. **현 스펙(100~400 ns)에선 무해**(최소 89 ns 마진). **50 ns 이하로 갈 계획이면 LS2→HS2가 설정−11 ns까지 줄어 마진 재확인 필요**. 대칭 필요 시 EPWM7 CMPB +2 counts 트림 검토. 패턴 정본 [[am263p_epwm_module_sync_deadtime]].

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
2. **UART5 단독 루프백 PASS (2026-06-10)** — J1.4↔J1.3 루프백 + TCA6416 P00/P14=LOW 세팅으로 TX==RX 확인(Logic2 버스트 검증). 근본원인(U54 보드먹스) 해소. 잔여: **Phase 2** = 8kw 보드 결합 시 RS-485 차동(THVD1400 U13 DE, `EN_485`=GPIO91=J5.48). 정본 [[lp_am263p_uart_epwm_mux]].
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
| UART5 차동 송신 | △ | 단독 루프백 PASS(TCA6416 P00/P14=LOW, J1.4↔J1.3, 2026-06-10). Phase 2(8kw 보드 결합 RS-485, `EN_485`=GPIO91) 잔여 |
| 실보드 교차검증 (A4) | ✗ | 멀티미터 기준값 교차 (A3 후) |
| **PWM 전력제어 (P0~P4)** | ✓ (P1 4/4·P2 dt단일소스·**85kHz/config분리**) | [[pwm]]. **4핀 HS1/LS1/HS2/LS2 ✓실보드 검증**. 레그2 EPWM4↔EPWM7 SYNC+CMPB 상보. P2: 두 레그 `ETA_DEADTIME_NS` 단일소스(`8046744`). **`d01fc0a`: 85kHz 고정(85.032kHz 실측)·dead-time `eta_tuning.h` knob 분리(100~400ns `#error` 가드)·100/150/400ns 스윕 PASS(shoot-through 0).** 다음 P3 보호. 핀맵 [[pwm_pinmap]] |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 추가 정보 필요 / `✗` 미구현

## 미결 사항

- **A3 센서 스펙 미입수 (블로커 유지)**: mV→물리량(°C/V/A) 변환 코드 전무. `eta_adc_loop`은 raw·mV까지만. Temp_Module1/2 출력 특성(V/°C), GA_Vin 분압비, I_LCC_SEN·I_COIL_SEN·GA_Iin_SEN 감도(mV/A)·오프셋 모두 미입수.
- **UART5 Phase 2 — 8kw 보드 결합 RS-485 차동 (잔여)**: 단독 루프백(J1.4↔J1.3) PASS(2026-06-10) — 근본원인(U54 보드먹스, TCA6416 P00/P14 미세팅) 해소. 잔여 = 8kw 보드 결합 시 THVD1400 U13 DE(`EN_485`=GPIO91=J5.48) 구현·검증. 정본 [[lp_am263p_uart_epwm_mux]]. (**DE 핀**: THVD1400 U13 → LP-AM263P J5.48 = **GPIO91**, 코드 식별자 `EN_485`.)
- **UART 출력 채널 하드코딩**: `eta_uart5.c`가 채널별 `DebugP_log` 라인 하드코딩 → ADC 채널 추가 시 출력 라인 수동 추가 필요(eta_adc.c 테이블 루프와 달리 자동 추종 안 함).
- ~~PWM 레그1 dead-time 단일소스 통일~~ — ✅ **해결(`8046744`)**: 두 레그 모두 `ETA_DEADTIME_NS` 하나로 수렴. 레그1=`eta_pwm_init()`이 `EPWM_setRisingEdgeDelayCount`/`setFallingEdgeDelayCount`로 RED/FED(=ETA_DEADTIME_COUNTS, SysConfig 기본 override), 레그2=CMPB 오프셋. 150/300ns 4ch 실측(레그1 150.3→300.4·레그2 150.0→300.0ns, shoot-through 0). 상세 [[pwm]] §dead-time 단일소스. (`d01fc0a`에서 단일소스 위치를 `eta_tuning.h`로 이전.)
- ~~PWM 주파수 85 kHz 고정 / dead-time config 분리~~ — ✅ **완료(`d01fc0a`)**: 85.032 kHz 실측, dead-time 100/150/400 ns 스윕 PASS(shoot-through 0). 단일소스 `eta_tuning.h ETA_DEADTIME_NS`(100~400 ns `#error` 가드), 주파수·dead-time 모두 `eta_pwm_init()` 런타임 override로 SysConfig 면역.
- **PWM dead-time 최종값 미고정 (미결 유지)**: 현재 **150 ns 베이스라인으로 커밋**(`d01fc0a`). 메커니즘·스윕 인프라(100~400 ns)는 완료. **전력단 브링업 때 100~400 ns 중 최종값 확정 예정.**
- **PWM 레그2 dead-time 비대칭 (향후 참조, P3/P4 관련)**: 레그2(HS2=EPWM4_A/LS2=EPWM7_B) 두 모듈 동기에 모듈간 **~11 ns(≈2.2 counts) 고정 위상 스큐** → dead-time HS→LS +11 ns / LS→HS −11 ns 비대칭(합=2×설정값). 레그1 비대칭 없음. **현 스펙(100~400 ns) 무해**(최소 89 ns 마진). 50 ns 이하 계획 시 LS2→HS2 마진(설정−11 ns) 재확인 필요, 대칭 필요 시 EPWM7 CMPB +2 counts 트림 검토. ([[am263p_epwm_module_sync_deadtime]])
- **빌드 환경 주의 (HW 엔지니어 워크플로우)**: CCS 생성 makefile(`Release/subdir_rules.mk`)이 **절대경로**(`C:/ti/...`, `C:/Users/echog/...`)를 박고 있고, 빌드 시 `Release/syscfg`를 `example.syscfg`에서 재생성한다. **다른 노트북에서 git clone 후엔 CCS로 프로젝트 import**(=makefile 로컬 경로 재생성)해서 빌드. 단 **`eta_tuning.h` 변경은 순수 C 컴파일로 반영**되어 syscfg 재생성 불요 — 이것이 런타임 override 방식의 이점.
- **PWM 회로도 net 라벨 함정 (정본 기록 유지)**: 회로도 net 라벨("EPWM4_B"/"EPWM7_A")과 silicon 채널(EPWM4_A/EPWM7_B) suffix **반대** — 펌웨어 정본=silicon 채널(UG Mode0·pinmux.csv 교차확인). 라벨에 끌려가지 말 것([[pwm_pinmap]]).
- **PWM 게이트 극성 회로도 미확인**: active-high 가정으로 4핀 검증 통과(shoot-through 0) → 가정 실보드 실증. **회로도 원본으로 극성 확인은 잔여**. shutdown 입력 미확인.
- **PWM 잔여 스펙**: ~~스위칭 주파수~~ **85 kHz 고정·구현·실측 확정(`d01fc0a`)**. ~~dead-time 단일소스/스윕 인프라~~ ✅ 완료. 잔여 = **보호(trip) 신호 소스 미정(P3 선결)** · dead-time 최종값 고정(위 항목).
- ~~레그2 두 모듈 동기 dead-time 비표준 구현~~ — **해결**(EPWM4→EPWM7 SYNC+CMPB 오프셋, shoot-through 0 실측). 단 향후 보드 리비전 시 한 모듈로 묶도록 수정 요청 예정([[pwm_pinmap]] §향후).
