---
tags: [entity, pwm, 8kw-ev-wpt-tx, pinmap]
source: 사용자 제공 (2026-06-09) — PWM 핀맵·스펙
date: 2026-06-09
---

# pwm_pinmap — 8kW WPT TX 보드 PWM 핀맵

> LP-AM263P EPWM 출력 → eta 보드 게이트 구동 신호 대응표.
> 작업 호는 [[pwm]], 프로젝트 현재 위치는 [[status]].
> EPWM 트리거·설정 함정(플랫폼 공통)은 [[am263p_adc_rti_trigger]] 형제 — 향후 PWM→ADC SOC 트리거 전환 참조.

---

## 핀맵 (2026-06-09 확정 — 사용자 핀번호 정정 + UG 교차확인)

> 사용자가 J4.38→**J4.39**로 정정(2026-06-09) → 레그1이 [[lp_am263p_ug]] 핀먹스 표(Table 2-28/2-30)와 완전 일치. **구현(SysConfig) 기준 = UG Mode0 채널.** 레그2 A/B suffix는 사용자 net 라벨과 다르나, 물리 핀이 노출하는 채널이 강제하므로 UG 기준 확정.

| 8kw 신호 | 역할 | LP-AM263P 핀 | EPWM 채널 (구현=UG Mode0) | 사용자 net 라벨 | 비고 |
|----------|------|--------------|---------------------------|-----------------|------|
| PWM_HS1 | 레그1 High | J4.39 | **EPWM2_A** | EPWM2_A | ✅ UG·사용자 일치. **실측 검증됨(2026-06-09, Saleae 100kHz/50%, 정본↔실측 불일치 없음)** |
| PWM_LS1 | 레그1 Low | J4.40 | **EPWM2_B** | EPWM2_B | ✅ UG·사용자 일치 |
| PWM_HS2 | 레그2 High | J6.52 | **EPWM4_A** | EPWM4_B | 모듈 EPWM4 일치, suffix는 J6.52가 _A만 노출 |
| PWM_LS2 | 레그2 Low | J6.51 | **EPWM7_B** | EPWM7_A | 모듈 EPWM7 일치, suffix는 J6.51이 _B(Mode0)/EPWM5_B(Mode10)만 노출 |

### 핵심 — 레그 구조 (펌웨어 함의)

- **레그1 = EPWM2 단일 모듈**(A=HS1, B=LS1) → 모듈 내 **dead-band 유닛**으로 상보 PWM + dead-time 깔끔히 생성.
- ⚠️ **레그2 = EPWM4(HS2) + EPWM7(LS2) — 서로 다른 두 모듈에 걸침.** J6.51이 EPWM4_B를 노출하지 않아(EPWM7_B/EPWM5_B만) **한 모듈로 못 묶음.**
  - → 레그2 상보 PWM·dead-time은 **모듈 내 dead-band 불가**. **EPWM 동기(SYNCO→SYNCI) + 위상/카운터 오프셋**으로 두 모듈 간 dead-time을 만들어야 함. 레그1과 **비대칭 구현**.
  - dead-time 튜닝(build-per-change, 시작 150ns)도 레그1=dead-band 레지스터 / 레그2=모듈간 오프셋으로 **경로가 다름**.
  - **의도된 설계 확인(2026-06-09)** — 현 회사 회로도가 이렇게 라우팅됨. 단 향후 개선 대상(아래 §향후 보드 개선).
- **A/B suffix 확정(UG 기준, 2026-06-09)**: 사용자 schematic net 라벨(레그2 _B/_A)과 silicon 노출 채널(_A/_B)이 반대. **펌웨어 배정은 핀이 강제하는 UG 채널**(EPWM4_A@J6.52, EPWM7_B@J6.51) 기준 — net 이름에 끌려가지 말 것.
- ✅ **UART5(EPWM15)와 충돌 없음** — PWM은 EPWM2/4/7 사용. ([[am263p_iomux_force_io_enable]] EPWM15 점유 건과 무관)
- **인스턴스 3개: EPWM2(레그1), EPWM4·EPWM7(레그2).**

### 향후 보드 개선 (기억할 것)

⭐ **레그2를 한 EPWM 모듈로 묶도록 회로도 수정 요청 예정.** 현재 레그2(HS2/LS2)가 EPWM4+EPWM7 두 모듈에 걸친 건 **현 회사 회로도 라우팅 결과로 의도된 설계**지만, 레그2 dead-time을 모듈간 동기로 만들어야 해 레그1보다 까다롭다. **사용자가 회로도 수정 요청 기회가 생기면 레그2 HS2/LS2를 한 EPWM 모듈의 A/B로 묶도록 요청할 계획**(예: 둘 다 EPWM4_A/EPWM4_B를 노출하는 핀 쌍으로). 그러면 레그2도 모듈 내 dead-band로 단순화. (사용자 지시 2026-06-09 — 영구 메모리에도 기록)

---

## 스펙 (사용자 제공, 2026-06-09)

- **토폴로지**: 풀브리지 인버터 (4스위치, 2레그). WPT 공진 탱크 구동(LCC 탱크는 [[adc_pinmap]] `I_LCC_SEN` 단서 — 가설 유지).
- **스위칭 주파수**: **고정형**. 단 **값 미정**(추후 확정). → 런타임 가변 아님.
- **Dead-time**: **이것만 가변.** 다만 **리얼타임 변경 불필요** — dead-time 바꿀 때마다 **새로 빌드**하는 방식으로 테스트. **시작값 ≈ 150 ns.**
- **제어**: (현재 범위 밖) 추후 ADC 피드백 제어루프.

---

## 향후 — PWM을 ADC SOC 트리거 소스로

- **현재**: ADC는 **RTI1**(syscfg `CONFIG_RTI0`) 1 kSPS 트리거 사용 ([[adc_pinmap]]·[[am263p_adc_rti_trigger]]).
- **계획**: PWM 구현 완료 후, **ADC SOC 트리거 소스를 RTI → EPWM**으로 전환(전력제어에서 표준 — PWM 주기 특정 시점에 ADC 샘플). **지금은 RTI 그대로 두고**, PWM 안정화 뒤 수정.
- 전환 시 [[am263p_adc_rti_trigger]] §1 "트리거 export 게이트" 류 함정을 EPWM SOC 결선에서 동형으로 점검할 것.

---

## 미확인 / P0 잔여

- 핀맵·채널 확정(위 표, UG 기준). 레그2 두 모듈(EPWM4+EPWM7) 동기 dead-time은 의도된 현 설계 — 향후 개선 대상(§향후 보드 개선). SysConfig는 핀별 hard `$assign`.
- 스위칭 주파수 확정값.
- 게이트 드라이버 입력 극성(active-high/low)·shutdown 입력 — 출력 force-enable/극성 설정 시 필요 ([[am263p_iomux_force_io_enable]]).
- 보호(trip) 신호 소스 — 과전류/과전압 시 PWM 차단 입력(ADC 비교/외부 trip 핀).
