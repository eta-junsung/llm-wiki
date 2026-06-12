---
tags: [entity, pwm, 8kw-ev-wpt-tx, pinmap]
source: 사용자 제공 + [[lp_am263p_ug]] Table 2-30 교차확인 (2026-06-09) — PWM 핀맵·스펙. net/채널 분리 정정(J6.52=EPWM4_A, HS2 실측). EPWM0 fan-out + isoform (2026-06-11, 4014901). dead-time knob flash+boot 검증 (2026-06-12)
date: 2026-06-12
---

# pwm_pinmap — 8kW WPT TX 보드 PWM 핀맵

> LP-AM263P EPWM 출력 → eta 보드 게이트 구동 신호 대응표.
> 작업 호는 [[pwm]], 프로젝트 현재 위치는 [[status]].
> EPWM 트리거·설정 함정(플랫폼 공통)은 [[am263p_adc_rti_trigger]] 형제 — 향후 PWM→ADC SOC 트리거 전환 참조.

---

## 핀맵 (2026-06-09 확정 — 4핀 전부 UG·실보드 검증)

> **3단 구분: 기능 net(게이트 역할) ↔ 커넥터 핀 ↔ SoC EPWM 채널.** 펌웨어 배정의 **정본 = 핀이 노출하는 SoC 채널**([[lp_am263p_ug]] Table 2-30 Mode0/primary, `teams/g/lp-am263p/raw/lp_am263p_ug/ug_lp-am263p.md`).
> - ⚠️ **회로도 net 라벨 함정(레그2 공통 패턴)**: 회사 회로도는 레그2 게이트 net을 채널이름 스타일 **"EPWM4_B"(HS2)·"EPWM7_A"(LS2)** 로 라벨링했는데, 이 **suffix가 핀이 실제 노출하는 silicon 채널과 반대**다 — HS2 실제=**EPWM4_A**, LS2 실제=**EPWM7_B**. **회로도 라벨이 아니라 핀이 강제하는 UG 채널(silicon)로 배정**할 것. ([[adc_pinmap]] l/I 오기 전례와 동류 — 핀 신호명은 wiki/라벨보다 회로도·UG·실측 우선.)
> - 근거: UG Table 2-30 raw (`ug:1600/1601/1641/1640`). **LS2는 wiki↔UG 일치(오기 없음)** + **pinmux.csv 핀 F1=EPWM7_B 교차확인**. (HS2는 이전 wiki가 회로도 라벨에 끌려 silicon 채널을 EPWM4_B로 오기했던 것을 2026-06-09 정정.)

| 기능 net | 역할 | 커넥터 핀 | SoC 채널 (UG Mode0 = **펌웨어 정본**) | 회로도 net 라벨 | 근거 | 검증 |
|----------|------|-----------|----------------------------------------|-----------------|------|------|
| PWM_HS1 | 레그1 HS | J4.39 | **EPWM2_A** | EPWM2_A (일치) | `ug:1600` | ✓ 99.997kHz/50% (Saleae n=10223) |
| PWM_LS1 | 레그1 LS | J4.40 | **EPWM2_B** | EPWM2_B (일치) | `ug:1601` | ✓ 레그1 EPWM2 dead-band 상보 완료 |
| PWM_HS2 | 레그2 HS | J6.52 | **EPWM4_A** | "EPWM4_B" (suffix 반대) | `ug:1641` (Mode0=EPWM4_A) | ✓ 100kHz/50%, dead-time 150ns; 펌웨어 hard `$assign`=EPWM4_A |
| PWM_LS2 | 레그2 LS | J6.51 | **EPWM7_B** | "EPWM7_A" (suffix 반대) | `ug:1640` (Mode0=EPWM7_B) + pinmux.csv 핀 **F1=EPWM7_B** | ✓ 100kHz/47%, dead-time 150ns, shoot-through 0 |

> ✅ **P1 4핀 전부 실보드 검증 완료(2026-06-09, 커밋 `6e6b342` branch pwm).** 레그2 상보·dead-time을 EPWM4↔EPWM7 모듈간 SYNC + CMPB 오프셋으로 해결 — 설계·함정은 [[pwm]] Pin4 절. 실측: 100kHz, HS2 50%/LS2 47%, dead-time 150ns 양 edge, shoot-through 0 (Saleae 125MS/s, 13,421주기 전수 스캔). **표·실측의 100kHz는 브링업 임시값 — 주파수는 85kHz 고정 확정(2026-06-10), dead-time 카운트는 주파수 무관.**

### 핵심 — 레그 구조 (펌웨어 함의)

- **레그1 = EPWM2 단일 모듈**(A=HS1, B=LS1) → 모듈 내 **dead-band 유닛**으로 상보 PWM + dead-time 깔끔히 생성.
- ⚠️ **레그2 = EPWM4_A@J6.52(HS2) + EPWM7_B@J6.51(LS2) — 서로 다른 두 모듈에 걸침** (확정·4핀 실측 2026-06-09). J6.51은 EPWM4_B를 노출하지 않아(EPWM7_B/EPWM5_B만, `ug:1640`) **한 모듈로 못 묶음** → 두 모듈 SYNC 필요.
  - → 레그2 상보 PWM·dead-time은 **모듈 내 dead-band 불가**. **EPWM0 더미 마스터 fan-out**(output-less, `syncout=ON_CNTR_ZERO`) + **비대칭 AQ + 2-compare 합성**으로 상보+dead-time 생성(isoform) — **✓ 구현·4-DT sweep 검증 완료**(`4014901`). 설계 상세는 [[pwm]] §EPWM0 fan-out + 동형화. 레그1(dead-band)과 **메커니즘은 다르나 파형·timing 동형**.
  - dead-time: 레그1=dead-band RED/FED / 레그2=2-compare(CMPA=TBPRD/2±DT, CMPB=TBPRD/2). **ns 소스는 `ETA_DEADTIME_NS` 하나로 수렴**(`eta_tuning.h`) — 매크로·검증표는 [[pwm]] §dead-time 단일소스.
  - **의도된 설계 확인(2026-06-09)** — 현 회사 회로도가 이렇게 라우팅됨. 단 향후 개선 대상(아래 §향후 보드 개선).
- **채널 suffix는 핀이 강제, 회로도 라벨과 반대 (레그2 공통 패턴, 확정)**: 회로도 net 라벨이 "EPWM4_B"(HS2)/"EPWM7_A"(LS2)지만 핀이 노출하는 silicon 채널은 EPWM4_A(`ug:1641`)/EPWM7_B(`ug:1640`, pinmux.csv F1=EPWM7_B 교차확인). **펌웨어 배정·정본은 silicon 채널**(EPWM4_A/EPWM7_B) — 회로도 라벨 suffix에 끌려가지 말 것. 4핀 전부 이 기준으로 실측 통과.
- ✅ **UART5(EPWM15)와 충돌 없음** — PWM은 EPWM2/4/7 사용. ([[am263p_iomux_force_io_enable]] EPWM15 점유 건과 무관)
- **인스턴스 3개: EPWM2(레그1), EPWM4·EPWM7(레그2).**

### 향후 보드 개선 (기억할 것)

⭐ **레그2를 한 EPWM 모듈로 묶도록 회로도 수정 요청 예정.** 현재 레그2(HS2/LS2)가 EPWM4+EPWM7 두 모듈에 걸친 건 **현 회사 회로도 라우팅 결과로 의도된 설계**지만, 레그2 dead-time을 모듈간 동기로 만들어야 해 레그1보다 까다롭다. **사용자가 회로도 수정 요청 기회가 생기면 레그2 HS2/LS2를 한 EPWM 모듈의 A/B로 묶도록 요청할 계획**(예: 둘 다 EPWM4_A/EPWM4_B를 노출하는 핀 쌍으로). 그러면 레그2도 모듈 내 dead-band로 단순화. (사용자 지시 2026-06-09 — 영구 메모리에도 기록)

---

## EPWM 인스턴스·자유구동 사실 (검증 근거, 2026-06-09)

> Pin별 독립 검증이 왜 가능했는지의 근거. 출처는 각 항에 명시(추정 금지).

- **EPWM4는 EPWM2와 독립 인스턴스로 실재.** AM263Px에서 SysConfig가 수용하며, base = `CSL_CONTROLSS_G0_EPWM4_U_BASE`. → 레그2 HS2(EPWM4)가 레그1(EPWM2)과 별개 모듈인 펌웨어 근거. (출처: 사용자 제공 — SysConfig 수용·base 매크로 실측 2026-06-09)
- **SysConfig 기본 EPWM 인스턴스는 SYNC-in disable + phaseShift=0 → 단독 자유구동(free-run).** 위상기준이 없어 **단일 모듈 핀은 다른 레그와 무관하게 독립 검증 가능.** 레그2 HS2(EPWM4_A@J6.52)가 레그1 EPWM2와 무관하게 100kHz(실측 99.998kHz)/50% 토글하는 것을 단독 실증. (출처: 사용자 제공 + Pin3 실측 2026-06-09)
- **함의**: Pin1·Pin3처럼 단일 모듈 출력은 위상 동기 없이 순차 검증 가능. 단 **레그2 상보·dead-time(Pin4 단계)** 은 EPWM4↔EPWM7 모듈간 SYNC를 **명시 활성화**해야 성립 — 자유구동 기본값(SYNC-in disable·phaseShift=0)으로는 두 모듈이 위상정렬되지 않는다. [[pwm]] P2/Pin4 참조.

---

## 스펙 (사용자 제공, 2026-06-09)

- **토폴로지**: 풀브리지 인버터 (4스위치, 2레그). WPT 공진 탱크 구동(LCC 탱크는 [[adc_pinmap]] `I_LCC_SEN` 단서 — 가설 유지).
- **스위칭 주파수**: **85 kHz 고정 — 구현·실측 확정**(`d01fc0a`, **Saleae 85.032 kHz** 측정, `TBPRD=1176`/`cmpA=588`/`EPWM7 CMPB=558`). 런타임 가변 아님. (브링업 임시 100 kHz에서 전환.)
- **Dead-time**: **이것만 가변.** **리얼타임 변경 불필요** — 값 바꿔 **재빌드**(build-per-change). **조정 범위 100~400 ns**(`#error` 범위가드), 실험 후 최종값 고정 예정(**production 기본값 150 ns 확정 2026-06-12**). 두 레그 단일소스 **`ETA_DEADTIME_NS`(`src/eta_bsp/eta_tuning.h`)** — 패턴 정본 [[am263p_epwm_module_sync_deadtime]]. 주파수·dead-time 모두 `eta_pwm_init()` 런타임 override → SysConfig 재생성 면역.
  - ✅ **flash+boot knob silicon 검증 완료 (2026-06-12)**: `ETA_DEADTIME_NS` → flash → VCC 전원사이클 → silicon 핀에서 100~400 ns 전 범위 ≤2 ns 정확도 추종 실측. 상세 [[pwm_deadtime_knob_verify]].
- **레그2 dead-time 비대칭** — **✅ ±2 ns 이하로 감소** (`4014901`, EPWM0 fan-out + isoform). 구 토폴로지 ~22 ns 비대칭 → 현재 방향 비대칭 ~+3 ns 고정(EPWM7 위상 trim=0, `SE_TRIM_COUNTS` 조정 여지). 100 ns 설정 시 최소 갭 = 99 ns. 상세 [[pwm]] §EPWM0 fan-out·[[am263p_epwm_module_sync_deadtime]]·[[pwm_deadtime_knob_verify]] §6.
- **제어**: (현재 범위 밖) 추후 ADC 피드백 제어루프.

---

## 향후 — PWM을 ADC SOC 트리거 소스로

- **현재**: ADC는 **RTI1**(syscfg `CONFIG_RTI0`) 1 kSPS 트리거 사용 ([[adc_pinmap]]·[[am263p_adc_rti_trigger]]).
- **계획**: PWM 구현 완료 후, **ADC SOC 트리거 소스를 RTI → EPWM**으로 전환(전력제어에서 표준 — PWM 주기 특정 시점에 ADC 샘플). **지금은 RTI 그대로 두고**, PWM 안정화 뒤 수정.
- 전환 시 [[am263p_adc_rti_trigger]] §1 "트리거 export 게이트" 류 함정을 EPWM SOC 결선에서 동형으로 점검할 것.

---

## 미확인 / P0 잔여

- ✅ **핀맵·채널 4핀 전부 확정·실측**(레그1 J4.39/40=EPWM2_A/B, 레그2 J6.52=EPWM4_A·J6.51=EPWM7_B). 레그2 두 모듈(EPWM4+EPWM7) SYNC dead-time 구현·검증 완료 — 의도된 현 설계, 향후 단일 모듈 개선 대상(§향후 보드 개선). SysConfig는 핀별 hard `$assign`.
- ✅ 스위칭 주파수 **85 kHz 고정 확정**(2026-06-10). dead-time 100~400 ns 조정·실험 후 고정.
- **게이트 드라이버 입력 극성**: **active-high 가정으로 4핀 검증 통과(상보·dead-time·shoot-through 0 정상) → 가정 실보드 실증.** 단 회로도 원본으로 극성 못 박은 상태 — "가정 실증, 회로도 미확인". shutdown 입력은 미확인 ([[am263p_iomux_force_io_enable]]).
- 보호(trip) 신호 소스 — 과전류/과전압 시 PWM 차단 입력(ADC 비교/외부 trip 핀).
