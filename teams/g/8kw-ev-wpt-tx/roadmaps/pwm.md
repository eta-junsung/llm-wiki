---
tags: [roadmap, pwm, 8kw-ev-wpt-tx, living-doc]
date: 2026-06-09
---

# pwm — 8kW WPT TX 보드 PWM 전력제어 작업 호 (P0~P4)

> ADC 계측 브링업([[adc]]) 다음의 **전력제어** 작업 호. **P1 진행 중 — Pin1 HS1 실보드 검증 통과(2026-06-09), 나머지 3핀 남음.** 현재 위치·다음 시작점은 [[status]].
> 핀맵 정본 [[pwm_pinmap]]. 상위 프로젝트 호는 [[roadmap]].

---

## 0. 한 줄 요약

LP-AM263P의 **EPWM2·EPWM4·EPWM7**(레그1=EPWM2 / 레그2=EPWM4+EPWM7)로 8kW WPT 송신 **풀브리지 인버터**(4스위치, 2레그)를 상보 PWM + dead-time으로 구동한다. 기본 출력 → dead-time 튜닝 → 보호(trip-zone) → ADC 피드백 제어 순.

---

## 1. 사실 / 가설 / 모름 (2026-06-09 사용자 스펙으로 갱신)

- **사실 (사용자 제공 + UG 교차확인 2026-06-09 — 핀맵 정본 [[pwm_pinmap]])**:
  - **인버터 = 풀브리지(4스위치, 2레그). 인스턴스 3개.**
    - **레그1 = EPWM2 단일 모듈**: EPWM2_A=HS1@J4.39, EPWM2_B=LS1@J4.40. (UG·사용자 일치)
    - **레그2 = EPWM4 + EPWM7 두 모듈**: EPWM4_A=HS2@J6.52, EPWM7_B=LS2@J6.51. (모듈 일치, suffix는 핀이 강제 — net 라벨과 반대)
  - ⚠️ **레그2가 두 모듈에 걸쳐 dead-time을 모듈 내 dead-band로 못 만듦** → EPWM 동기(SYNC)+위상 오프셋 필요. 레그1(단일 모듈 dead-band)과 비대칭. 상세 [[pwm_pinmap]].
  - ✅ **UART5(EPWM15)와 충돌 없음** — PWM은 EPWM2/4/7.
  - **스위칭 주파수 = 고정형**(런타임 가변 아님), 단 **값 미정**.
  - **Dead-time만 가변** — 리얼타임 변경 불필요, **dead-time 바꿀 때마다 새로 빌드**해 테스트. **시작 ≈ 150 ns.**
  - ADC는 **현재 RTI1 트리거 유지**. PWM 완료 후 **ADC SOC 트리거를 EPWM으로 전환 예정**([[pwm_pinmap]] §향후, [[am263p_adc_rti_trigger]]).
  - 보드 계측: LCC 전류(I_LCC_SEN)·코일 전류(I_COIL_SEN)·입력 전압/전류(GA_Vin/GA_Iin) — P4 피드백 후보 ([[adc_pinmap]]).
- **가설**:
  - 공진 탱크 = **LCC**(ADC `I_LCC_SEN` 단서). [가설 유지]
- **모름 (확인 필요)**:
  - 스위칭 주파수 확정값 (현재 100 kHz는 브링업 임시값).
  - **레그2 두-모듈(EPWM4+EPWM7) SYNC+위상오프셋 상보·dead-time 구체 설계** — SDK 예제에 1:1 대응 없음. Pin4 착수 시 설계 필요.
  - duty 범위·위상 시프트 제어 여부.
  - 게이트 드라이버 입력 극성·shutdown 입력, trip(보호) 신호 소스.

---

## 2. 마일스톤 호 (P0~P4)

| 단계 | 범위 | 완료 기준 | 상태 |
|------|------|---------|------|
| **P0** | PWM 요구사항·핀맵 확정 | 핀맵·토폴로지·채널·dead-time 방식 확정 + EPWM 핀 배정표 | △ (핀맵·토폴로지·dead-time 확정 / 주파수값·보호신호 미정) |
| **P1** | 기본 PWM 출력 | EPWM2/4/7 SysConfig 설정 → 4채널 PWM 실보드 출력, 오실로로 주파수·dead-time(~150ns) 검증 | △ (1/4) ← **Pin1 HS1 ✓검증, Pin2/3/4 남음** |
| **P2** | dead-time 튜닝·레그 정합 | 레그1(EPWM2 dead-band)·레그2(EPWM4+7 모듈간 동기) dead-time 정합, build-per-change 스윕 | ✗ |
| **P3** | 보호 (trip-zone) | 과전류/과전압 시 PWM 즉시 차단 — ADC/비교기/외부 trip 입력 연동, 실보드 차단 검증 | ✗ |
| **P4** | 제어 루프 연동 | ADC 피드백(전류·전압) → duty/위상 갱신. **이때 ADC SOC 트리거를 RTI→EPWM으로 전환** | ✗ |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 추가 정보 필요 / `✗` 미구현

> **P0 대부분 해소(2026-06-09)**: 핀맵 확정([[pwm_pinmap]] — 사용자 J4.38→J4.39 정정 + UG 교차확인)·풀브리지 3인스턴스(EPWM2/4/7)·dead-time 방식(build-per-change, 150ns)·UART5 무충돌. 잔여 = 주파수 확정값·보호신호 소스(주파수 고정형이라 P1은 임시값 진행 가능). **⚠️ 레그2 두 모듈 동기 dead-time 비표준 구현 유의.**

---

## 3. 단계별 작업 내용

### P0 — 요구사항·핀맵 확정 (△ 대부분 해소)

- ✅ 핀맵·토폴로지·채널·dead-time 방식 확정 → [[pwm_pinmap]] 정본. UART5 무충돌 확인.
- 잔여: 스위칭 주파수 확정값, 보호(trip) 신호 소스, 게이트 드라이버 극성/shutdown.
- 물리 인스턴스/핀은 처음부터 hard `$assign`([[am263p_syscfg_soft_vs_hard_assign]]) — ADC soft 재셔플 함정 회피.

### P1 — 기본 PWM 출력 (진행 중, 1/4)

진척 (핀별):

| 핀 | 채널 | 상태 | 메모 |
|----|------|------|------|
| **Pin1 PWM_HS1** | EPWM2_A → J4.39 | ✓ **구현·실보드 검증** | Saleae Logic2 실측 **99.997 kHz / duty 49.998%**(n=10223 cycles), 깨끗한 토글·글리치 없음. **force_io 없이 SysConfig 핀먹스만으로 출력** (EPWM=핀 primary function — 정본 [[am263p_epwm_primary_pad_no_force_io]]) |
| Pin2 PWM_LS1 | EPWM2_B → J4.40 | ✗ | 레그1 dead-band 상보 (EPWM2 모듈 내) |
| Pin3 PWM_HS2 | EPWM4_A → J6.52 | ✗ | 레그2 하이 (EPWM4) |
| Pin4 PWM_LS2 | EPWM7_B → J6.51 | ✗ | 레그2 로우 (EPWM7) — Pin3와 모듈 간 SYNC+위상오프셋 상보·dead-time 필요 |

- 주파수는 고정형, **실측 100 kHz는 브링업 임시값** — 확정값 pending(추정 금지).
- duty 50%(기본), **dead-time ≈ 150 ns로 시작**(build-per-change).
- 검증: 오실로/로직(Saleae)로 주파수·dead-time 폭·레그별 HS/LS 상보 관계.
- ⚠️ **레그2(EPWM4 HS2 + EPWM7 LS2) 상보 + dead-time은 모듈 간 동기(SYNC)+위상 오프셋**으로 — 레그1(EPWM2 단일모듈 dead-band)과 설정 경로가 다름. **SDK 예제에 1:1 대응 없음 → Pin4 착수 시 설계 필요(확인 필요).** net 라벨이 아닌 **UG 채널(EPWM4_A@J6.52, EPWM7_B@J6.51)** 기준.
- 출력 force-enable: **EPWM이 핀 primary function이면 불필요**(Pin1로 실증). alt-function 패드일 때만 필요 — [[am263p_epwm_primary_pad_no_force_io]] vs [[am263p_iomux_force_io_enable]].

### P2 — dead-time 튜닝·레그 정합

- dead-time을 **리얼타임이 아니라 build-per-change**로 스윕 — 값 바꿔 빌드→플래시→오실로 측정 반복. (런타임 가변 코드 불필요)
- **레그1 = EPWM2 dead-band 레지스터 / 레그2 = EPWM4·EPWM7 모듈간 위상 오프셋** — 두 경로의 dead-time을 동일 값으로 정합.
- (개념 참조: oled rx_control [[dead_time]]·[[pwm_system]] — STM32 TIM 기반이라 레지스터는 다름, 개념만.)

### P3 — 보호 (trip-zone)

- EPWM trip-zone(TZ)로 과전류/과전압 즉시 차단. ADC 한계비교/내부 비교기/외부 trip 핀 소스 결정(P0 잔여).
- (개념 참조: oled [[trip_zone]] — BKIN→PWM 차단 패턴, 개념만.)

### P4 — 제어 루프 연동 + ADC 트리거 전환

- ADC 피드백(I_LCC/I_COIL/GA_Iin/GA_Vin) → duty 또는 위상 갱신.
- ★ **ADC SOC 트리거를 RTI1 → EPWM으로 전환** — 현재 ADC는 RTI 트리거([[adc_pinmap]]). PWM 주기 특정 시점 샘플이 전력제어에 표준. 전환 시 트리거 export 게이트 함정 점검([[am263p_adc_rti_trigger]] §1 동형).

---

## 4. 현재 위치

→ [[status]] 단일 소스. **P1 진행 중 1/4 — Pin1 HS1(EPWM2_A@J4.39) 실보드 검증 통과(100kHz/50%).** 다음 = Pin2 LS1(레그1 dead-band 상보) → Pin3 HS2 → Pin4 LS2(레그2 SYNC).

---

## 5. 블로커 / 선결

- ⚠️ **레그2 두 모듈(EPWM4+EPWM7) 동기 dead-time** — 의도된 현 설계(사용자 확인 2026-06-09). 펌웨어가 모듈간 위상 오프셋으로 dead-time 생성. **SDK 1:1 예제 없음 → Pin4 착수 시 설계 필요(확인 필요).** **향후 보드 리비전 시 한 모듈로 묶도록 수정 요청 예정**([[pwm_pinmap]] §향후 보드 개선).
- **주파수 확정값 미정** — 단 고정형이라 P1은 임시값 진행 가능.
- **보호(trip) 신호 소스 미정** — P3 선결(과전류/과전압 입력).
- ~~핀맵 UG 불일치~~ — **해소**(J4.38→J4.39 정정 + UG 교차확인, [[pwm_pinmap]]).
- ~~UART5 핀 충돌~~ — **해소**(UART5=EPWM15와 무관).

---

## 6. 환원 후보

- PWM 핀맵 → ✓ [[pwm_pinmap]] (2026-06-09 생성).
- AM263P EPWM 설정 노하우 → ✓ 1차 환원: [[am263p_epwm_primary_pad_no_force_io]] (EPWM primary 패드는 force_io 불필요). 레그2 SYNC 설계는 Pin4 착수 시 추가 환원.
- **보드 개선 요청 (향후)**: 레그2(HS2/LS2)를 한 EPWM 모듈로 묶도록 회로도 수정 요청 — 기회 생길 때. 상세 [[pwm_pinmap]] §향후 보드 개선.
