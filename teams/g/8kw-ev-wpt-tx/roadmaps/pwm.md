---
tags: [roadmap, pwm, 8kw-ev-wpt-tx, living-doc]
date: 2026-06-10
---

# pwm — 8kW WPT TX 보드 PWM 전력제어 작업 호 (P0~P4)

> ADC 계측 브링업([[adc]]) 다음의 **전력제어** 작업 호. **P1 완료(`6e6b342`) — 4핀 실보드 검증·레그2 SYNC 상보·shoot-through 0. P2 dead-time 단일소스(`8046744`). 85 kHz 고정 + dead-time config 분리(`d01fc0a`) — 85.032 kHz 실측·100/150/400 ns 스윕 PASS.** 현재 위치·다음 시작점은 [[status]].
> 핀맵 정본 [[pwm_pinmap]]. 상위 프로젝트 호는 [[roadmap]].

---

## 0. 한 줄 요약

LP-AM263P의 **EPWM2·EPWM4·EPWM7**(레그1=EPWM2 / 레그2=EPWM4+EPWM7)로 8kW WPT 송신 **풀브리지 인버터**(4스위치, 2레그)를 상보 PWM + dead-time으로 구동한다. 기본 출력 → dead-time 튜닝 → 보호(trip-zone) → ADC 피드백 제어 순.

---

## 1. 사실 / 가설 / 모름 (2026-06-09 사용자 스펙으로 갱신)

- **사실 (사용자 제공 + UG 교차확인 2026-06-09 — 핀맵 정본 [[pwm_pinmap]])**:
  - **인버터 = 풀브리지(4스위치, 2레그). 인스턴스 3개.**
    - **레그1 = EPWM2 단일 모듈**: EPWM2_A=HS1@J4.39, EPWM2_B=LS1@J4.40. (UG·사용자 일치)
    - **레그2 = EPWM4 + EPWM7 두 모듈**: EPWM4_A=HS2@J6.52 (`ug:1641`), **EPWM7_B=LS2@J6.51** (`ug:1640` + pinmux.csv F1=EPWM7_B 교차확인). 4핀 전부 실측 확정. ⚠️ 회로도 net 라벨("EPWM4_B"/"EPWM7_A")과 silicon 채널 suffix **반대** — 펌웨어 정본=silicon 채널(EPWM4_A/EPWM7_B), 라벨에 끌려가지 말 것([[pwm_pinmap]]).
  - ✅ **레그2 두 모듈 SYNC 상보·dead-time 해결**: EPWM4 syncout(ON_CNTR_ZERO)→EPWM7 syncin, phaseShift=0 위상정렬 + EPWM7_B AQ 반전 + CMPB 오프셋(`CMPB=TBPRD/2−DT`, 부호 `−` 엄수). 레그1(단일 모듈 dead-band)과 비대칭. 상세 [[pwm_pinmap]]·§3 Pin4.
  - ✅ **UART5(EPWM15)와 충돌 없음** — PWM은 EPWM2/4/7.
  - **스위칭 주파수 = 85 kHz 고정 — 구현·실측 확정**(`d01fc0a`, 런타임 가변 아님). 브링업 임시값 100 kHz → **85 kHz로 전환·실측**. UP_DOWN: `TBPRD = TBCLK/(2·f_sw) = 200MHz/(2·85kHz) = 1176`, `cmpA = TBPRD/2 = 588`(50% duty), `EPWM7 CMPB = 588 − 30 = 558`(@150 ns). **Saleae 실측 85.032 kHz**(계산 1176과 일치).
  - **TBCLK = 200 MHz 확정 사실**(더 이상 전제 아님): 85.032 kHz@TBPRD=1176 + P1의 100 kHz@TBPRD=1000 양쪽 실측 일치 → **1 count = 5 ns**.
  - **Dead-time만 가변** — 리얼타임 변경 불필요, **dead-time 바꿀 때마다 새로 빌드**해 테스트(**build-per-change**). **조정 범위 100~400 ns**(실험 후 값 고정 예정, 현재 150 ns 베이스라인). ✅ **두 레그 모두 `ETA_DEADTIME_NS` #define 단일소스로 통일**(레그1 dead-band RED/FED·레그2 CMPB 오프셋, 메커니즘 둘·소스 하나) — 패턴 정본 [[am263p_epwm_module_sync_deadtime]], 150/300ns(`8046744`) + 100/150/400ns@85kHz(`d01fc0a`) 4ch 실측 통과(§3 §dead-time 단일소스). **단일소스 위치는 `eta_pwm.h` → `src/eta_bsp/eta_tuning.h`로 이전**(`d01fc0a`, 100~400 ns `#error` 범위가드). dead-time 카운트는 TBCLK 기준이라 주파수와 무관.
  - ADC는 **현재 RTI1 트리거 유지**. PWM 완료 후 **ADC SOC 트리거를 EPWM으로 전환 예정**([[pwm_pinmap]] §향후, [[am263p_adc_rti_trigger]]).
  - 보드 계측: LCC 전류(I_LCC_SEN)·코일 전류(I_COIL_SEN)·입력 전압/전류(GA_Vin/GA_Iin) — P4 피드백 후보 ([[adc_pinmap]]).
- **가설**:
  - 공진 탱크 = **LCC**(ADC `I_LCC_SEN` 단서). [가설 유지]
- **모름 (확인 필요)**:
  - ~~스위칭 주파수 확정값~~ — **확정: 85 kHz 고정**(사용자 2026-06-10). dead-time은 **100~400 ns 조정 가능, 실험 후 고정 예정**.
  - ~~레그2 두-모듈 SYNC 상보·dead-time 설계~~ — **해결**(§3 Pin4 / 정본 [[am263p_epwm_module_sync_deadtime]], shoot-through 0 실측).
  - duty 범위·위상 시프트 제어 여부.
  - **게이트 드라이버 입력 극성**: active-high 가정으로 4핀 검증 통과 → **가정 실보드 실증**, 단 **회로도 원본 미확인**. shutdown 입력·trip(보호) 신호 소스 미정.

---

## 2. 마일스톤 호 (P0~P4)

| 단계 | 범위 | 완료 기준 | 상태 |
|------|------|---------|------|
| **P0** | PWM 요구사항·핀맵 확정 | 핀맵·토폴로지·채널·dead-time 방식 확정 + EPWM 핀 배정표 | △ (핀맵·토폴로지·dead-time·4핀 채널·**주파수 85kHz 구현·실측 확정**·게이트 극성 active-high 실증 / 보호신호 소스·극성 회로도 확인 미정) |
| **P1** | 기본 PWM 출력 | EPWM2/4/7 SysConfig 설정 → 4채널 PWM 실보드 출력, 오실로로 주파수·dead-time(~150ns) 검증 | ✓ **완료 (4/4) — HS1/LS1/HS2/LS2 전부 실보드 검증** (커밋 `6e6b342` branch pwm) |
| **P2** | dead-time 튜닝·레그 정합 + 주파수 확정 | 레그1(EPWM2 dead-band)·레그2(EPWM4+7 모듈간 동기) dead-time 정합, build-per-change 스윕, **주파수 85 kHz 고정** | ✓ **완료** — 단일소스 통일·150/300ns(`8046744`) + **85 kHz 고정·100/150/400ns 스윕 4ch PASS·config 분리(`d01fc0a`)**. dead-time **최종값**은 전력단 브링업 때 확정(인프라는 완료) |
| **P3** | 보호 (trip-zone) | 과전류/과전압 시 PWM 즉시 차단 — ADC/비교기/외부 trip 입력 연동, 실보드 차단 검증 | ✗ |
| **P4** | 제어 루프 연동 | ADC 피드백(전류·전압) → duty/위상 갱신. **이때 ADC SOC 트리거를 RTI→EPWM으로 전환** | ✗ |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 추가 정보 필요 / `✗` 미구현

> **P0 대부분 해소(2026-06-09~10)**: 핀맵 4핀 확정·실측([[pwm_pinmap]])·풀브리지 3인스턴스(EPWM2/4/7)·dead-time 방식(build-per-change, 100~400ns 조정)·UART5 무충돌·게이트 극성 active-high 실증·**주파수 85kHz 확정**. 잔여 = 보호신호 소스·게이트 극성 회로도 확인. **레그2 두 모듈 SYNC dead-time은 P1에서 해결(shoot-through 0).**

---

## 3. 단계별 작업 내용

### P0 — 요구사항·핀맵 확정 (△ 대부분 해소)

- ✅ 핀맵·토폴로지·채널(4핀)·dead-time 방식 확정 → [[pwm_pinmap]] 정본. UART5 무충돌 확인.
- ✅ **게이트 극성 active-high 가정 실보드 실증**(4핀 상보·dead-time·shoot-through 0 정상) — 단 회로도 원본 미확인.
- ✅ **스위칭 주파수 85 kHz 고정·구현·실측 확정**(`d01fc0a`, 85.032 kHz 측정). dead-time 100~400 ns 조정·실험 후 최종값 고정(현재 150 ns 베이스라인).
- 잔여: 보호(trip) 신호 소스, 게이트 극성 회로도 확인·shutdown 입력.
- 물리 인스턴스/핀은 처음부터 hard `$assign`([[am263p_syscfg_soft_vs_hard_assign]]) — ADC soft 재셔플 함정 회피.

### P1 — 기본 PWM 출력 (✓ 완료 4/4)

진척 (핀별) — **4핀 전부 실보드 검증**:

| 핀 | 채널 (UG 정본) | 상태 | 메모 |
|----|------|------|------|
| **Pin1 PWM_HS1** | EPWM2_A → J4.39 | ✓ **구현·실보드 검증** | Saleae 실측 **99.997 kHz / duty 49.998%**(n=10223). **force_io 없이 SysConfig 핀먹스만으로 출력** (EPWM=핀 primary function — 정본 [[am263p_epwm_primary_pad_no_force_io]]) |
| **Pin2 PWM_LS1** | EPWM2_B → J4.40 | ✓ **구현·실보드 검증** | 레그1 EPWM2 **모듈 내 dead-band**로 HS1 상보 |
| **Pin3 PWM_HS2** | EPWM4_A → J6.52 | ✓ **구현·실보드 검증** | 펌웨어 hard `$assign`=EPWM4_A, **100 kHz / 50%**. EPWM4=EPWM2와 독립 인스턴스(base `CSL_CONTROLSS_G0_EPWM4_U_BASE`), SYNC-in disable·phaseShift=0이라 단독 자유구동 검증 후 SYNC 결선 ([[pwm_pinmap]] §EPWM 인스턴스·자유구동) |
| **Pin4 PWM_LS2** | EPWM7_B → J6.51 | ✓ **구현·실보드 검증** | 레그2 LS, **100 kHz / 47%**, dead-time 150ns, **shoot-through 0**. EPWM4↔EPWM7 모듈간 SYNC 상보 — 설계 아래 |

- **검증 실측치(Saleae 125MS/s, 13,421주기 전수 스캔)**: 100 kHz, HS2 50%/LS2 47%, dead-time **150 ns 양 edge**, shoot-through **0**. HS1은 99.997kHz/50%(별도 측정).
- **주파수 85 kHz 고정 확정**(2026-06-10). 위 실측은 브링업 임시 100 kHz에서 수행 — 85 kHz 재빌드 시 TBPRD만 바뀌고(dead-time 카운트 불변) 검증 결론 동일.
- **채널은 핀이 강제하는 UG Mode0**(EPWM4_A@J6.52 `ug:1641`, EPWM7_B@J6.51 `ug:1640`) — ⚠️ 회로도 net 라벨("EPWM4_B"/"EPWM7_A")과 suffix 반대. 펌웨어 정본=silicon 채널 ([[pwm_pinmap]]).
- 출력 force-enable: **EPWM이 핀 primary function이면 불필요**(Pin1로 실증). alt-function 패드일 때만 필요 — [[am263p_epwm_primary_pad_no_force_io]] vs [[am263p_iomux_force_io_enable]].

#### Pin4 LS2 — 두 모듈 SYNC 상보 설계 (SDK 1:1 예제 없던 자리, 해결)

레그2는 EPWM4(HS2)·EPWM7(LS2)가 **다른 모듈**이라 레그1처럼 모듈 내 dead-band를 못 쓴다. 해결 설계:

1. **위상 정렬**: EPWM4 **syncout = ON_CNTR_ZERO** → EPWM7 **syncin = SYNCOUT_EPWM4**, EPWM7 **phaseShift = 0**. 두 모듈 카운터를 매 주기 영점에서 정렬.
2. **상보 + dead-time**: EPWM7_B **AQ(Action Qualifier) 반전** + **CMPB 오프셋**으로 LS를 HS의 반전+dead-time만큼 시프트. (레그1의 dead-band 유닛 대신 **CMPB 오프셋 방식**.)
3. ⚠️ **설계 함정 (구현 중 1회 부호 오류로 shoot-through 잡음)**: **`CMPB = TBPRD/2 − DT_COUNTS`** 여야 하며 **반드시 `< TBPRD/2`**. **+부호**로 두면 LS ON 구간이 HS OFF 구간을 넘어 **shoot-through 발생**. 부호는 `−`.

→ 결과: shoot-through 0, dead-time 150ns 양 edge 실측 확인. **이 패턴(두 모듈 SYNC 상보·CMPB dead-time)은 플랫폼 정본 [[am263p_epwm_module_sync_deadtime]]으로 승격.**

#### dead-time 단일소스 #define 패턴 — 두 레그, 두 메커니즘, 하나의 ns 소스 (✓ commit `8046744`)

레그1·레그2가 **dead-band(RED/FED) vs CMPB 오프셋**으로 메커니즘은 다르지만, dead-time ns 소스는 **`src/eta_bsp/eta_tuning.h`의 `#define ETA_DEADTIME_NS` 하나**로 수렴한다. (`d01fc0a`에서 `eta_pwm.h` → 신설 `eta_tuning.h`로 이전 — HW 엔지니어가 만지는 컴파일타임 튜닝 knob 전용 파일.) 이 숫자만 바꿔 재빌드하면 **두 레그 dead-time이 함께 추종**(**build-per-change** — 런타임 조절 코드 없음).

- **단일 소스**: `#define ETA_DEADTIME_NS 150U` (레그1·레그2 공유, `eta_tuning.h`). **유효범위 100~400 ns — 이탈 시 `#error`로 빌드 차단**(오타·범위 이탈 컴파일타임 방어). 100 ns→20 count, 400 ns→80 count(모두 5 ns 배수라 절삭손실 0).
- **변환 매크로**: `ETA_NS_TO_COUNTS(ns) = (uint16_t)((uint32_t)ns * (TBCLK_HZ/1MHz) / 1000)` — 정수 **floor 절삭**. **TBCLK = 200 MHz**(`ETA_PWM_TBCLK_HZ`) → **1 count = 5 ns**. 150 ns→**30 count**, 300 ns→**60 count**(정수라 **절삭손실 0**). dead-time 카운트는 **TBCLK 기준이라 주파수와 무관.**
- **`ETA_DEADTIME_COUNTS = ETA_NS_TO_COUNTS(ETA_DEADTIME_NS)`** (= 30 @150 ns).
- **TBPRD은 주파수 따라, dead-time 카운트는 무관**: 85 kHz 고정(`d01fc0a`) → `TBPRD = 1176`(`200MHz/(2·85kHz)`, UP_DOWN), `cmpA = 588`(50%), `EPWM7 CMPB = 588 − 30 = 558`(@150 ns). 브링업 임시 100 kHz는 TBPRD=1000·cmpA=500·CMPB=470이었음 — **주파수 바뀌어도 dead-time 카운트(=30)는 불변**, CMPB의 `TBPRD/2` 베이스만 재계산된다. **주파수·dead-time 둘 다 `eta_pwm_init()`이 런타임 override** → SysConfig(`example.syscfg`) 재생성으로 기본값 덮여도 면역(§빌드 환경).

**레그1 (EPWM2 — dead-band 유닛 방식)**:
- `eta_pwm_init()`이 `EPWM_setRisingEdgeDelayCount(CONFIG_EPWM2_BASE_ADDR, ETA_DEADTIME_COUNTS)` + `EPWM_setFallingEdgeDelayCount(…)`로 **RED/FED에 재적용**.
- **RED = FED 대칭** → 한 주기에 대칭 dead-band 갭 2개. SysConfig 부팅 기본값(RED/FED=30)을 init이 override.

**레그2 (EPWM4_A=HS2 / EPWM7_B=LS2 — 두 모듈 CMPB 오프셋 방식)**:
- `ETA_EPWM7_CMPB_INIT = TBPRD/2 − ETA_DEADTIME_COUNTS` (= **558** @150 ns @85 kHz(`TBPRD/2=588−30`, `d01fc0a`); 브링업 100 kHz 때는 **470**(`500−30`)이었음). `eta_pwm_init()`이 `EPWM_setCounterCompareValue(CONFIG_EPWM7_BASE_ADDR, EPWM_COUNTER_COMPARE_B, …)`로 적용.
- ⚠️ **CMPB < TBPRD/2 여야 dead-time** (초과 시 shoot-through) — `−` 부호 엄수, §Pin4 함정과 동일 사실.

> 핀맵·채널 대응은 [[pwm_pinmap]] 단일 소스 (여기서 중복 서술 안 함).

#### 검증 방법·결과 (dead-time 스윕, ✓ commit `8046744`)

**검증 레시피**:
- flash 없이 **RAM-load(OCRAM) → run** + **Saleae Logic2**, 4채널 digital, **500 MS/s(2 ns 격자)**, **transition-based CSV export**. (.sal보다 transition CSV가 오프라인 수치분석에 유리; binary raw는 이 규모에선 불요.)
- **측정 정의**: **dead-time = 상보쌍 both-LOW 갭**, **shoot-through = 상보쌍 both-HIGH 겹침**. 샘플레이트는 타임스탬프 격자 GCD로 추정.

**결과** (branch pwm, `ETA_DEADTIME_NS` 150·300 두 빌드, 4채널 실측 — 브링업 임시 100 kHz):

| 항목 | 150 ns 빌드 | 300 ns 빌드 |
|------|------------|------------|
| 주파수 (4ch) | 100 kHz ±0.1%, 상보 유지 | 100 kHz ±0.1%, 상보 유지 |
| 레그1 dead-time | 150.3 ns | 300.4 ns (1.998×) |
| 레그2 dead-time | 150.0 ns | 300.0 ns (2.000×) |
| shoot-through | **0** (양 레그) | **0** (양 레그) |
| 레그1 RED=FED 대칭 | ✓ (주기당 갭 2개) | ✓ |

> ⚠️ **해석 주의**: 측정 평균이 명목보다 **+0.3 ns 큰 것은 2 ns 격자 양자화 바이어스**이지 floor 절삭/타이밍 오차가 아니다 — 30·60 count는 정수라 **절삭손실 0**.

#### 85 kHz 고정 + config 분리 검증 (✓ commit `d01fc0a`)

주파수 85 kHz 전환 + dead-time knob을 `eta_tuning.h`로 분리한 뒤 재검증. **Saleae 4채널**(ch0=HS1 J4.39 / ch1=LS1 J4.40 / ch2=HS2 J6.52 / ch3=LS2 J6.51), **dead-time 100/150/400 ns 스윕**, 전 주기 측정:

| 항목 | 결과 |
|------|------|
| 주파수 (4ch, 세 빌드) | **85.032 kHz** (+0.002%, 주기 11.7603 µs, 지터 σ≈0.74 ns) |
| duty (HS) | 49.15 / 48.73 / 46.60% (100/150/400 ns) — **`50% − dt/T` 공식 정확 추종**(AHC 정상, **결함 아님**) |
| dead-time | 100/150/400 ns **완벽 선형 추종**(20/30/80 counts). 레그1 오차 ~0(σ<1 ns) |
| shoot-through | **양 레그 전 주기 0건**. 최소 DT 89 ns 양수 마진 |
| 판정 | **PASS** |

> duty가 50%보다 작은 것은 dead-time 갭만큼 HS ON이 줄어든 정상 동작(`50% − dt/T`) — AHC(Active-High-Complementary) 정상이며 결함이 아니다.

#### ⚠️ 레그2 dead-time 비대칭 (향후 참조 — P3/P4 마진 검토)

레그2(HS2=EPWM4_A / LS2=EPWM7_B)는 **서로 다른 EPWM 모듈을 동기시켜 만든 상보쌍**이라 모듈간 **~11 ns(≈2.2 counts) 고정 위상 스큐**가 있다 → dead-time이 **HS→LS +11 ns / LS→HS −11 ns 비대칭**(합은 항상 정확히 2×설정값). 레그1(EPWM2 한 모듈 HW dead-band)은 비대칭 없음.

- **현 스펙(100~400 ns)에선 무해** — 최소 89 ns 마진(LS2→HS2 = 100−11 ≈ 89 ns).
- **50 ns 이하로 갈 계획이면** LS2→HS2가 `설정−11 ns`까지 줄어 마진 재확인 필요.
- **대칭이 필요하면** EPWM7 CMPB에 약 **+2 counts 트림** 검토(스큐 보정).
- 근본 원인·패턴은 플랫폼 정본 [[am263p_epwm_module_sync_deadtime]]. 향후 보드 리비전에서 레그2를 한 모듈로 묶으면 비대칭 자체가 사라짐([[pwm_pinmap]] §향후).

### P2 — dead-time 튜닝·레그 정합 (✓ 단일소스 통일·150/300ns 스윕 + 85kHz 100/150/400ns 스윕, commit `8046744`·`d01fc0a`)

- dead-time을 **리얼타임이 아니라 build-per-change**로 스윕 — 값 바꿔 빌드→RAM-load→Saleae 측정. (런타임 가변 코드 불필요)
- ✅ **두 레그 모두 `ETA_DEADTIME_NS` 단일소스로 통일**: 레그1=EPWM2 **dead-band RED/FED**(`EPWM_setRisingEdgeDelayCount`/`setFallingEdgeDelayCount`), 레그2=EPWM7 **CMPB 오프셋**(`EPWM_setCounterCompareValue`). **메커니즘 둘·ns 소스 하나.** `d01fc0a`에서 단일소스를 `eta_tuning.h`로 이전 + 100~400 ns `#error` 범위가드. 상세·매크로는 위 §dead-time 단일소스.
- ✅ **150↔300 ns(`8046744`, 100 kHz) + 100/150/400 ns(`d01fc0a`, 85 kHz) 4채널 실측 통과**(선형 추종, shoot-through 0, 최소 마진 89 ns). 결과표는 위 §검증 방법·결과 / §85 kHz 검증.
- ✅ **주파수 85 kHz 고정·실측 확정**(85.032 kHz). 주파수·dead-time 모두 `eta_pwm_init()` 런타임 override로 SysConfig 면역.
- 잔여(인프라 완료, 값만 미정): **dead-time 최종값 고정** — 현재 150 ns 베이스라인, **전력단 브링업 때 100~400 ns 중 확정**.
- (개념 참조: oled rx_control [[dead_time]]·[[pwm_system]] — STM32 TIM 기반이라 레지스터는 다름, 개념만.)

### P3 — 보호 (trip-zone)

- EPWM trip-zone(TZ)로 과전류/과전압 즉시 차단. ADC 한계비교/내부 비교기/외부 trip 핀 소스 결정(P0 잔여).
- (개념 참조: oled [[trip_zone]] — BKIN→PWM 차단 패턴, 개념만.)

### P4 — 제어 루프 연동 + ADC 트리거 전환

- ADC 피드백(I_LCC/I_COIL/GA_Iin/GA_Vin) → duty 또는 위상 갱신.
- ★ **ADC SOC 트리거를 RTI1 → EPWM으로 전환** — 현재 ADC는 RTI 트리거([[adc_pinmap]]). PWM 주기 특정 시점 샘플이 전력제어에 표준. 전환 시 트리거 export 게이트 함정 점검([[am263p_adc_rti_trigger]] §1 동형).

---

## 빌드 환경 주의 — HW 엔지니어 워크플로우

- **소스 레이아웃**: PWM은 `src/eta_bsp/eta_pwm.{c,h}` + **`src/eta_bsp/eta_tuning.h`**(신설 — dead-time 등 컴파일타임 튜닝 knob 전용).
- **dead-time 조정**: `eta_tuning.h`의 `ETA_DEADTIME_NS` **한 줄만** 바꿔 재빌드(**build-per-change**). 100~400 ns 이탈 시 `#error`. `ETA_DEADTIME_COUNTS`·EPWM7 CMPB 등 파생값 자동 추종.
- ⚠️ **CCS makefile 절대경로 함정**: CCS 생성 makefile(`Release/subdir_rules.mk`)이 **절대경로**(`C:/ti/...`, `C:/Users/echog/...`)를 박고 있고, 빌드 시 `Release/syscfg`를 `example.syscfg`에서 재생성한다. **다른 노트북에서 git clone 후엔 반드시 CCS로 프로젝트 import**(=makefile을 로컬 경로로 재생성)한 뒤 빌드할 것.
- ✅ **`eta_tuning.h` 변경은 순수 C 컴파일로 반영** → syscfg 재생성 불요. 주파수·dead-time을 `eta_pwm_init()`이 런타임 override하므로 `example.syscfg`를 안 건드려도 됨(=런타임 override 방식의 이점).

---

## 4. 현재 위치

→ [[status]] 단일 소스. **P1 완료 4/4**(4핀 실보드 검증) **+ P2 dead-time 단일소스 통일·150/300ns 스윕(`8046744`) + 85 kHz 고정·100/150/400ns 스윕 PASS·config 분리(`d01fc0a`, 85.032 kHz 실측, shoot-through 0).** 다음 = P3 보호(trip-zone) / dead-time 최종값 고정(전력단 브링업) / 보호신호·게이트 극성 회로도 스펙 확보 / P4 제어루프.

---

## 5. 블로커 / 선결

- ~~레그2 두 모듈(EPWM4+EPWM7) 동기 dead-time~~ — **해결**(EPWM4→EPWM7 SYNC + CMPB 오프셋, shoot-through 0 실측, §3 Pin4). **향후 보드 리비전 시 한 모듈로 묶도록 수정 요청 예정**([[pwm_pinmap]] §향후 보드 개선).
- ~~주파수 확정값 미정~~ — **확정: 85 kHz 고정·구현·실측(`d01fc0a`, 85.032 kHz)**.
- **dead-time 최종값 미고정** — 인프라(100~400 ns 스윕)·config 분리 완료, 현재 150 ns 베이스라인. 전력단 브링업 때 확정.
- **보호(trip) 신호 소스 미정** — P3 선결(과전류/과전압 입력).
- **게이트 극성 회로도 미확인** — active-high는 실보드 실증됨, 회로도 원본 확인은 잔여.
- ~~핀맵 UG 불일치~~ — **해소**(4핀 UG·실측 확정, [[pwm_pinmap]]).
- ~~UART5 핀 충돌~~ — **해소**(UART5=EPWM15와 무관).

---

## 6. 환원 후보

- PWM 핀맵 → ✓ [[pwm_pinmap]] (2026-06-09, 4핀 확정·회로도 라벨 함정).
- AM263P EPWM 설정 노하우 → ✓ 1차 환원: [[am263p_epwm_primary_pad_no_force_io]] (EPWM primary 패드는 force_io 불필요).
- **레그2 두 모듈 SYNC 상보·dead-time 설계** → ✅ **concept 승격 완료: [[am263p_epwm_module_sync_deadtime]]** (AM263P 플랫폼 정본, lp-am263p concepts). §3 Pin4는 8kw 구현 기록.
- **dead-time 단일소스 #define 패턴**(`ETA_DEADTIME_NS`→레그1 RED/FED·레그2 CMPB, build-per-change, `eta_tuning.h` knob 분리·`#error` 범위가드·런타임 override로 SysConfig 면역) → ✓ §3 §dead-time 단일소스에 매크로·검증표 기록 + [[am263p_epwm_module_sync_deadtime]] §dead-time ns 단일소스 연계.
- **레그2 모듈간 위상 스큐 → dead-time 비대칭(~11 ns)** → ✓ §3 §레그2 dead-time 비대칭 기록 + [[am263p_epwm_module_sync_deadtime]]에 플랫폼 일반 사실로 반영. P3/P4·저 dead-time 시 마진 검토 단서.
- **보드 개선 요청 (향후)**: 레그2(HS2/LS2)를 한 EPWM 모듈로 묶도록 회로도 수정 요청 — 기회 생길 때. 상세 [[pwm_pinmap]] §향후 보드 개선.
