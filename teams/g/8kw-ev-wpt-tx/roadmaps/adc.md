---
tags: [roadmap, adc, 8kw-ev-wpt-tx, living-doc]
date: 2026-06-29
---

# adc — 8kW WPT TX 보드 ADC 브링업 작업 호 (A0~A4)

> 단순 기능 확인이 아닌 **eta 보드 신호 정합** 브링업 작업.
> 6채널 ADC(온도 2 + 전압 1 + 전류 2 + 선형 1)를 SysConfig 설정 → polling 검증 → 신호별 스케일링 → 실보드 교차검증 순으로 진행.
> 핀 대응표는 [[adc_pinmap]], 기능별 현황·다음 시작점은 [[status]].

상위 프로젝트 호는 [[roadmap]].

---

## 0. 한 줄 요약

LP-AM263P 5개 ADC 인스턴스(ADC0~ADC4)에 eta 보드 J3 커넥터 6채널(Temp×2, 전압×1, 전류×2, 선형×1)을 SysConfig로 연결하고, 신호별 변환식을 붙여 실측값을 검증한다.

---

## 1. 마일스톤 호 (A0~A4)

| 단계 | 범위 | 완료 기준 | 상태 |
|------|------|---------|------|
| **A0** | SysConfig ADC 설정 | ADC 인스턴스 + 채널 핀 할당 완료, 빌드 성공 | ✓ |
| **A1** | 단채널 검증 | 단일 핀(AIN0) raw count → voltage, UART 출력 확인 | ✓ |
| **A1.5** | UART 주기화 + ADC 리팩토링 | 1초 주기 출력 + `src/eta_bsp/eta_adc.{c,h}` 다핀 확장 정리 | ✓ |
| **A2** | 전채널 순차 읽기 | 6채널 전부 신호 레이블 붙여 UART 출력 | ✓ (6/6, 실보드 검증) |
| **A3** | 신호별 스케일링 적용 | 변환식 구현 (센서 스펙 입수 후 진행) | ✓ (5/6채널, I_LCC_SEN 드롭) |
| **A3.5** | ADC SOC 트리거 RTI→EPWM0 + PPB HW 평균 | EPWM0(85 kHz) 트리거 + PPB 오버샘플 평균값 실보드 검증 | ✓ (HW 검증, N=64 확정) |
| **A4** | 실보드 교차검증 | 멀티미터/소스 기준값으로 ADC 출력 오차 정량화 | ✗ |
| **A5** | ADC 실질 샘플링 85 kHz (#7) | `ETA_ADC_OVERSAMPLE_LOG2` 낮춰 실질 85 kHz 달성, 실보드 노이즈 실측. **A3.5(N=64) 재검토** | ✗ |
| **A6** | SW 이동평균 전환 (#8) | ring buffer 이동평균 구현·CPU 부하 실측. A5 선행 필요 | ✗ |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 추가 정보 필요 / `✗` 미구현

> **설계 변경(2026-06-05)**: A1 원안 "polling 검증"을 **RTI 타이머 주기 트리거 + EOC 인터럽트(ISR-flag 패턴)** 로 전환. 단일 핀(AIN0) 1 kSPS로 실보드 검증 완료. 검증된 패턴·SysConfig 결선 함정(`enableIntr0`)·측정 시점 함정은 AM263P 플랫폼 정본 [[am263p_adc_rti_trigger]]로 환원.
> **A2 완료(2026-06-09, commit c512e3b)**: **6채널 전부 달성·실보드 검증** — 물리 인스턴스 **5개(ADC0~ADC4)**, RTI1 공통 트리거 1 kSPS. AIN 핀까지 hard `$assign` 승격으로 재셔플 리스크 해소. `eta_adc.c` 테이블 주도 리팩토링(332→232줄, 동작 불변) 동반. 남은 것은 A3(스펙 대기)·UART5 차동 복구·A4.

---

## 2. 단계별 작업 내용

### A0 — SysConfig ADC 설정

- CCS SysConfig에서 ADC 인스턴스 5개(ADC0~ADC4) 추가
- 채널 핀 할당: [[adc_pinmap]] 표 기준
  - ADC0: AIN1 (J3.28)
  - ADC1: AIN0 (J3.24), AIN1 (J3.29)
  - ADC2: AIN0 (J3.25)
  - ADC3: AIN0 (J3.26)
  - ADC4: AIN0 (J3.27)
- 샘플링: RTI1 타이머 주기 트리거 + EOC ISR (A1에서 polling 원안 전환). 물리 인스턴스는 hard `$assign`([[am263p_syscfg_soft_vs_hard_assign]]).
- 완료 기준: `ti_drivers_config.c` 생성, 빌드 에러 없음

### A1 — 단채널 검증 ✓ (2026-06-05)

- 단일 핀 **AIN0** 으로 ADC 변환 경로 검증 — **RTI 타이머 1 ms(1 kSPS) 주기 트리거 + EOC 인터럽트**에서 결과 read+flag, main 루프 consuming(ISR-flag 패턴). polling 원안에서 전환.
- 변환: `voltage = (raw * 3.3) / 4095` [Vref=3.3V 확정 — `ETA_ADC_VREFHI_MV=3300`, 2026-06-24]
- UART(115200) 출력으로 수치 확인 — **검증 완료**.
- **트리거 결선 함정**: SysConfig `enableIntr0`(Enable Compare Interrupt) 미설정 시 RTI INT0 이벤트 export가 막혀 ADC SOC 트리거 무동작. SW force로 변환 경로 생존 먼저 확인 후 트리거 결선 문제로 좁힘. 정본 [[am263p_adc_rti_trigger]].

### A1.5 — UART 주기화 + ADC 코드 리팩토링 ✓ (2026-06-09)

1. **UART 모니터링 주기화 ✓** — **RTI2 독립 타이머**(SysConfig 논리명 `CONFIG_RTI1`) compare0 ISR → flag → `eta_uart5_loop`이 **1초 주기 소비**(commit 8b85bda). ADC 트리거(RTI1)와 분리된 독립 타이머. 주기 값은 `#define`이 아니라 **SysConfig `nsecPerTick0=1e9`가 단일 진실원천**(헤더 주석이 desync 위험 #define 금지 명시).
2. **ADC 코드 리팩토링 ✓** — **eta_bsp 레이어 도입**(commit a655de4, edddc31), 디렉토리 `src/eta_bsp/`, 파일 `eta_adc.{c,h}`. **eta_ 접두 + _loop 접미** 컨벤션. ISR은 raw만 저장, `eta_adc_loop`이 `(raw*3300)/4095` 정수 mV 변환(out-param 방식, commit 88d9deb). 다핀 일반화 구조.

### A2 — 전채널 순차 읽기 ✓ (6/6, 실보드 검증, 2026-06-09 commit c512e3b)

**6채널 전부 달성**, 물리 인스턴스 **5개(ADC0~ADC4)** 사용. 핀맵·int_xbar·IRQ는 [[adc_pinmap]] 정본.

| enum | 신호 | ADC/SOC/AIN | J3 핀 | int_xbar / EOC IRQ |
|------|------|-------------|-------|--------------------|
| ETA_ADC_CH_TEMP_MODULE2 | Temp_Module2 | ADC1 SOC0 AIN0 | J3.24 | OUT_0 / IRQ146 |
| ETA_ADC_CH_I_LCC_SEN | I_LCC_SEN | ADC4 SOC0 AIN0 | J3.27 | OUT_2 / IRQ148 |
| ETA_ADC_CH_I_COIL_SEN | I_COIL_SEN | ADC0 SOC0 AIN1 | J3.28 | OUT_1 / IRQ147 |
| ETA_ADC_CH_GA_IIN_SEN | GA_Iin_SEN | ADC1 SOC1 AIN1 | J3.29 | OUT_0 / IRQ146 |
| ETA_ADC_CH_TEMP_MODULE1 | Temp_Module1 | ADC2 SOC0 AIN0 | J3.25 | OUT_3 / IRQ149 |
| ETA_ADC_CH_GA_VIN | GA_Vin | ADC3 SOC0 AIN0 | J3.26 | OUT_4 / IRQ150 |

- **ADC1만 SOC0+SOC1 라운드로빈**(단일 SOC1 EOC ISR로 2채널 수확), 나머지(ADC0/2/3/4)는 SOC0 단독. 트리거 = RTI1(syscfg `CONFIG_RTI0`) 1 kSPS 공유. 배치 근거 [[am263p_adc_instance_allocation]].
- ✅ **AIN 핀 hard `$assign` 승격**: 신규 2채널 추가 시 솔버 재셔플([[am263p_syscfg_soft_vs_hard_assign]])을 막기 위해 물리 인스턴스 hard `$assign`에 더해 **AIN 핀까지 전부 `$suggestSolution`→`$assign`** 으로 승격. 재생성 후 물리 배정 ADC0~4 유지(재셔플 없음) 확인 → soft 잔존 리스크 해소.
- **실보드에서 6채널 raw→mV 변환 경로 검증 완료.**
- **리팩토링 동반**: `eta_adc.c`를 인스턴스 테이블(`g_eta_adc_inst[]`) + 공용 `eta_adc_eoc_isr()` + 인덱스 루프로 통합(332→232줄, 동작 불변). 채널 추가 = enum 1행 + 테이블 1행. 단 `eta_uart5.c` 출력은 채널별 `DebugP_log` 하드코딩이라 출력 라인은 수동 추가 필요.
- 출력 형식(현재): UART0 콘솔(`DebugP_log`)로 6채널 ASCII. UART5 차동 송신은 미동작([[status]] 미결).

### A3 — 신호별 스케일링 적용

**아키텍처 확정(2026-06-24)**: 물리량 변환은 `tools/gui/gui.py`의 `PHYSICAL_COEFF` 테이블 단일 소스. MCU는 raw/mV만 전송. 변환식 상세 → [[adc_scaling]].

| 신호 | 상태 | 비고 |
|------|------|------|
| **I_COIL_SEN** | **✓ 완료·검증** | CT+버든. SCALE≈6.770 A/V (2026-06-24, 7335418) |
| **GA_Iin_SEN** | **✓ 완료·검증** | Hall-effect. SCALE=10 A/V, OFFSET=−3.3 A (2026-06-24) |
| **GA_Vin** | **✓ 완료·검증** | 저항분압+클리핑. SCALE≈353.39 V/V (2026-06-24) |
| **Temp_Module1/2** | **✓ 완료·검증** | NTC Beta. R15=3kΩ, B=3433 (2026-06-24) |
| I_LCC_SEN | — 드롭 | 센서 스펙 미입수, 제거(2026-06-26) |

변환식 상세·검증 데이터포인트 → [[adc_scaling]].

### A3.5 — ADC SOC 트리거 RTI→EPWM0 전환 + PPB HW 평균 필터 ✓ (HW 검증, N=64 확정, 2026-06-26)

**완료(main, PR #6 `d673e74`)**: 6채널 노이즈를 **CPU-free HW 평균**으로 처리. 트리거 EPWM0_SOCA 85.032 kHz, 방식 = **PPB 누적 평균**(repeater 안 씀). HW 노이즈 측정으로 **N=64 확정**.

1. **트리거 전환 ✓ (commit `3e5f117`)** — RTI1(1 kSPS) → EPWM0_SOCA(85.032 kHz). 6 SOC 전부 `soc0Trigger=ADC_TRIGGER_EPWM0_SOCA`(`example.syscfg`:70 등). RTI 카운터 시작 코드 제거(`eta_bsp_adc.c`:194). ★RTI의 `enableIntr0` export 게이트 함정은 EPWM에 적용 안 됨 — `ETSEL.SOCAEN`이 트리거 XBAR로 직접 출력. 경로·함정 정본 [[am263p_adc_rti_trigger]] §5.

2. **PPB HW 평균 ✓ (commit `4cffbe1`, N은 #6에서 64로 확정)** — 6채널 전부 PPB 누적 평균. **N=64 확정**(출력 1.33 kHz, 노이즈 √64=÷8, 그룹지연 ~370 µs). ISR을 EOC→OSINT로 변경, read는 `ADC_readResult`→`ADC_readPPBSum`. 정본 [[am263p_adc_ppb_averaging]].

3. **N 튜닝 손잡이 ✓ (commit `532e0eb`)** — `src/bsp/eta_bsp_adc.h:28`의 `ETA_ADC_OVERSAMPLE_LOG2` 단일 매크로(현재 `6U`→N=64; 5→32, 7→128, ≤10). `eta_bsp_adc_init()`이 전 PPB에 limit=2^LOG2·shift=LOG2 런타임 적용(eta_bsp_pwm.c TBPRD override와 동일 패턴). **GUI 통합 없음** — 코드 직접 수정 후 재빌드-flash.

**repeater 미채택 근거**: ① 과전류·과전압 보호는 HW 비교기 담당, ② 조정루프 대역폭 수백 Hz↓(기존 1 kSPS로도 동작), ③ 85 kHz에서 repeater N=64는 64×315 ns = 20 µs > 11.76 µs 주기로 변환시간 예산 초과([[am263p_adc_instance_allocation]] §변환시간 예산). PPB 누적은 N을 트리거에 걸쳐 분산하므로 예산과 무관.

**~~미검증(△)~~ → 전부 해소(2026-06-26)**:
- ~~△ ADC 인스턴스당 변환시간 실수치~~ → **확정**: 단일 변환 ≈ 315 ns(acq 85 ns + conv 230 ns, ADCCLK 50 MHz). 정적 산정 [[am263p_adc_instance_allocation]] §변환시간 예산.
- ~~△ SDK PPB API~~ → **확정**: `ADC_setupPPB`/`setPPBCountLimit`/`setPPBShiftValue`/`readPPBSum` 인용 정리 [[am263p_adc_ppb_averaging]] §3.
- ~~△ ADC1 SOC0+SOC1 라운드로빈~~ → **확정**: EPWM 전환 후 동일(lockstep, OSINT2→INT1). [[am263p_adc_rti_trigger]] §5.
- ~~△ 노이즈 감소량 실측~~ → **확정(HW)**: 실보드 측정으로 **N=64 채택**(√64=÷8). 6채널 0/3.3V 추종·OSINT ISR(N=64 ⇒ 1.33 kHz) 실측 OK. 이 측정 결과가 N 32→64 상향 근거 — main PR #6 `d673e74`.

---

### A4 — 실보드 교차검증

- 알려진 입력(멀티미터로 측정한 기준 전압)과 ADC 출력 비교
- 목표 오차: TBD (센서 정밀도에 따라)
- 완료 기준: 전채널 오차 정량화, 스펙 범위 내 또는 원인 규명

### A5 — ADC 실질 샘플링 85 kHz 확보 (#7) ✗

> **방향 재검토**: A3.5에서 PPB HW 평균 N=64가 "HW 노이즈 측정으로 확정"됐다([[am263p_adc_ppb_averaging]]). N=64는 **"노이즈 억제 우선(HW-first)"** 선택이었으나, 실질 샘플링을 1.33 kHz(= 85 kHz ÷ 64)로 깎는 부작용이 있다. A5·A6은 이 트레이드오프를 재검토해 **"스파이크 포착 우선"** 방향으로 전환한다. 기존 [[am263p_adc_ppb_averaging]] 계열 결정과 일부 상충.

**목적**: 85 kHz 스위칭 전류·전압 스파이크를 빠짐없이 포착하기 위해 실질 샘플링을 85 kHz로 끌어올린다.

| 항목 | 내용 |
|------|------|
| 현재 실질 샘플링 | ≈ 1.33 kHz (85 kHz ÷ N=64) |
| 목표 | 85 kHz 실샘플링 달성 |
| 손잡이 | `ETA_ADC_OVERSAMPLE_LOG2` (`src/bsp/eta_bsp_adc.h:28`) — 현재 `6U`(N=64) → `0`(N=1, 오버샘플 없음) |
| A4 선후 관계 | [추정] 독립 진행 가능 — A4는 샘플링 레이트 의존 없는 정확도 검증, A5는 샘플링 레이트 변경. 단 A5가 ADC 출력 특성을 바꾸므로 A5 후 A4 재측정 필요성 발생 가능. **확인 필요** |

**절차**:
1. `ETA_ADC_OVERSAMPLE_LOG2`를 낮춰(예: `3`→N=8, `0`→N=1) 재빌드·flash.
2. 실보드에서 노이즈 실측 — 허용 범위 여부 판단.
3. 노이즈 허용 시 A5 완료. 초과 시 A6(SW 이동평균) 착수.

**완료 기준**: N을 낮춘 상태에서 실질 85 kHz 샘플링 실보드 확인, 노이즈 실측값 기록.

### A6 — SW 이동평균 전환 검토 (#8) ✗

> **#7(A5) 선행 필요**: A5 완료 후 착수.

**배경**: A5·A6은 한 트레이드오프의 양면 — **"HW N↓(A5)" ↔ "SW 이동평균 보완(A6)"**. A5(N↓)로 실질 샘플링이 올라가면 HW 블록평균 노이즈 억제 효과가 줄어든다. SW ring buffer 이동평균이 대안 — 매 샘플마다 값 갱신으로 스파이크 감지 + 노이즈 억제를 동시에 달성한다.

| 항목 | 내용 |
|------|------|
| HW PPB 현재(A3.5) | N=64 블록평균 → 그룹지연 ~370 µs, 출력 1.33 kHz |
| A6 제안 | SW ring buffer 이동평균 — 매 샘플마다 값 갱신, 스파이크 감지 + 노이즈 억제 동시 달성 |
| CPU 부하 추정 | ISR @85 kHz × 6채널 ≈ 510,000 ISR/s, R5F @400 MHz ≈ 784 사이클/ISR 예산 [추정] |
| 미결 | R5F CPU 부하 허용 범위 **실측 필요**, 윈도우 크기 N 튜닝 |

**완료 기준**: SW 이동평균 구현·실보드 검증, CPU 부하 실측 허용 범위 내, 윈도우 N 확정.

---

## 3. 현재 위치

→ [[status]] 단일 소스.

A2 완료(2026-06-09, c512e3b) · A3 완료(5/6채널, I_LCC_SEN 드롭, 2026-06-26) · A3.5 **완료**(트리거 EPWM0_SOCA + PPB HW 평균 N=64 HW 확정, main PR #6 `d673e74`). 다음: A4 교차검증 또는 A5 (#7 샘플링 재작업) — [[status]] 참조.

---

## 4. 블로커 / 추가 정보 대기

- ~~**A3 블로커**~~ — I_LCC_SEN 드롭으로 해소(2026-06-26). A3 완료 처리.
- ~~**A3.5 지식 미검증**(변환시간·PPB API)~~ — 해소(2026-06-26): 변환시간 ≈315 ns 정적 확정([[am263p_adc_instance_allocation]]), PPB API 정리([[am263p_adc_ppb_averaging]]).
- ~~**A3.5 HW 실측 잔여**(노이즈 감소량)~~ — ✅ 해소(2026-06-26): HW 측정으로 **N=64 확정**(√64=÷8). main PR #6 `d673e74`. A3.5 ✓.
- **A0 전제**: LP-AM263P CCS 프로젝트 정상 동작 상태 (SysConfig 편집 가능)

---

## 5. 환원 후보

- ~~ADC 변환식 → `pages/concepts/adc_scaling.md`~~ ✅ 환원됨: [[adc_scaling]] (I_COIL_SEN 완료, A3 전체 완료 시 나머지 채울 것)
- ~~SysConfig ADC 설정 노하우 → concept 페이지~~ ✓ 환원됨: [[am263p_adc_rti_trigger]] (lp-am263p, AM263P 플랫폼 정본 — RTI·EPWM 트리거 결선·측정 시점 함정·검증된 설계 패턴).
- ~~PPB HW 오버샘플 평균 → concept 페이지~~ ✓ 환원됨: [[am263p_adc_ppb_averaging]] (lp-am263p, AM263P 플랫폼 정본 — TRM·SDK API 인용, 2026-06-26 신설).
- ~~ADC 변환시간 예산 → concept~~ ✓ 환원됨: [[am263p_adc_instance_allocation]] §변환시간 예산 (단일 변환 ≈315 ns 정적 확정).

---

## 6. 이슈 백로그

**#7(→A5)·#8(→A6)은 2026-06-29 계획 단계로 승격** — 상세는 §A5·§A6.

잔여 후보: **#9 IT6600C WiFi 연동 GUI** (우선순위 낮음·착수 미정, 정본 [[it6600c_wifi_gui]]).
