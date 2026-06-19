---
tags: [concept, am263p, epwm, sync, deadtime, platform]
source: 2026-06-09~11 8kw-ev-wpt-tx PWM 레그2(EPWM4_A=HS2 / EPWM7_B=LS2 두 모듈) SYNC 상보·dead-time + EPWM0 fan-out + 동형화 실보드 검증 (commit 6e6b342 SYNC 상보 + 8046744 단일소스·스윕 + d01fc0a 85kHz + 4014901 fan-out+isoform)
date: 2026-06-11
---

# AM263P EPWM 모듈간 SYNC 상보·dead-time (두 모듈 풀브리지 레그)

> **AM263P 플랫폼 지식 정본.** [[am263p_epwm_primary_pad_no_force_io]]·[[am263p_iomux_force_io_enable]] 형제. 풀브리지 한 레그의 HS/LS 게이트가 **서로 다른 EPWM 모듈**에 라우팅되면, 한 모듈 안의 **dead-band 유닛(RED/FED)** 으로 상보+dead-time을 만들 수 없다. 두 모듈을 **SYNC로 위상 정렬 + CMPB 오프셋**으로 상보·dead-time을 만드는 패턴. 8kw 레그2에서 실증.

## 한 줄 요약

**HS와 LS가 다른 EPWM 모듈에 걸친 레그**는 ① **공통 동기원(EPWM0 더미 마스터 등) fan-out → 모든 출력 모듈이 1-hop**으로 모듈간 정수클록 스큐 0 달성, ② **비대칭 AQ + 2-compare 합성**으로 레그1 dead-band와 동형인 파형 생성. dead-time = **CMPA = TBPRD/2 + DT_COUNTS(HS), CMPA = TBPRD/2 − DT_COUNTS(LS), CMPB = TBPRD/2(공유)** — 양방향 both-LOW 갭이 정확히 DT_COUNTS. 같은 모듈 레그(dead-band RED/FED)와 **메커니즘은 다르지만 dead-time ns 소스는 하나**로 공유 가능. 8kw 실증: 비대칭 ~22 ns→±2 ns, 4에지 시차 ≤2 ns.

---

## 언제 이 패턴이 필요한가

- 풀브리지/하프브리지 레그의 **HS·LS가 한 EPWM 모듈의 A/B 채널 쌍이 아닐 때.** 보드 라우팅상 두 게이트가 서로 다른 모듈 핀에 묶이면(핀먹스 제약), 모듈 내 dead-band 유닛은 **자기 모듈 A/B에만** dead-time을 넣으므로 쓸 수 없다.
- **판별**: 두 게이트 핀이 노출하는 SoC 채널이 같은 EPWM 인스턴스인가? 아니면(예: EPWM4 vs EPWM7) 이 패턴 필요. 핀↔채널은 UG 핀먹스 표 + 보드 회로도로 확인([[lp_am263p_ug]] Table 2-30).
- **대안(있으면 우선)**: 회로도 단계에서 HS/LS를 **한 모듈의 A/B를 노출하는 핀 쌍**으로 묶으면 dead-band로 단순화 — 보드 개선 후보.

---

## 패턴 (3단)

1. **위상 정렬 (SYNC) — fan-out 방식 권장**: **공통 동기원(output-less 더미 EPWM 또는 EXTSYNCIN)을 하나 두고, 모든 출력 모듈이 그것을 1-hop으로 선택** → 모든 출력 모듈의 hop 수가 동일 → 상호 정수클록 스큐 0. (구 방식: master EPWM `syncout=ON_CNTR_ZERO` → slave `syncin`, slave `phaseShift=0`. 이 경우 master 0-hop / slave 1-hop → ~2×EPWMCLK 스큐 잔존. → fan-out으로 대체 권장.)
2. **동형화 (비대칭 AQ + 2-compare)**: HS(master 레그)와 LS(slave 레그)를 레그1 dead-band와 동형으로 만들기 위해 **HS·LS 각각에 2개 compare**를 사용.
   - **HS** (`EPWM4_A` 사례): AQ = UP_CMPA→HIGH / DOWN_CMPB→LOW. **CMPA = TBPRD/2 + DT_COUNTS**, CMPB = TBPRD/2 → 상승 에지가 DT만큼 지연(= RED dead-band 동형).
   - **LS** (`EPWM7_B` 사례): AQ = ZERO→HIGH / UP_CMPB→LOW / DOWN_CMPA→HIGH. CMPB = TBPRD/2, **CMPA = TBPRD/2 − DT_COUNTS** → HS의 정확한 상보(양방향 DT).
3. **dead-time 단일소스**: `DT_COUNTS = round(dead_time_ns × TBCLK_HZ)` (정수 floor — [[#dead-time ns 단일소스 연계]]). HS의 CMPA·LS의 CMPA 양쪽이 `DT_COUNTS`로 추종.

---

## ⚠️ 함정

- **CMPB 부호 (shoot-through 직결)**: `CMPB`는 **반드시 `< TBPRD/2`**. `TBPRD/2 + DT`(부호 오류)로 두면 LS ON 구간이 HS OFF 구간을 **넘어 겹쳐 shoot-through**가 난다. 8kw 구현 중 1회 부호 오류로 발생→정정. 부호는 `−`.
- **SYNC-in 기본 disable**: SysConfig 기본 EPWM 인스턴스는 **SYNC-in disable + phaseShift=0**이라 단독 **자유구동(free-run)** 한다. 즉 **단일 모듈 핀은 위상기준 없이 독립 검증 가능**(이 점은 브링업에 유리)하지만, 이 패턴의 모듈간 위상정렬은 **SYNC를 명시 활성화**해야 성립한다 — 기본값으로는 두 모듈이 정렬되지 않는다. ([[pwm_pinmap]] §EPWM 인스턴스·자유구동)
- ⚠️ **모듈간 위상 스큐 → dead-time 비대칭 (플랫폼 일반 사실)**: SYNC로 정렬해도 두 모듈 사이엔 **고정 잔류 위상 스큐**가 남는다(8kw 실측 **~11 ns ≈ 2.2 counts @200 MHz TBCLK**). **근본 원인은 hop 수 비대칭** — master(EPWM4)는 자기 영점이 기준이라 **0 hop**, slave(EPWM7)는 SYNCIN으로 **1 hop = 2×EPWMCLK(=10 ns @prescale 1)** 지연. 즉 11 ns ≈ 이 1-hop 지연이다. TRM 지연 모델·토폴로지 정본은 [[am263p_epwm_sync_topology]]. 결과로 dead-time이 **HS→LS / LS→HS 방향에 따라 ±스큐만큼 비대칭**(두 갭의 **합은 항상 정확히 2×설정값**으로 보존). **같은 모듈 dead-band 레그(RED/FED)는 비대칭 없음.** 함의: dead-time이 충분히 크면 무해하지만, **설정값이 스큐에 근접할 만큼 작아지면**(예: 8kw 스큐 11 ns에 대해 ≲50 ns) 짧은 쪽 갭이 `설정−스큐`까지 줄어 **shoot-through 마진을 직접 깎는다** → 저 dead-time 설계 시 마진 재확인 필수.
  - **스큐 0 토폴로지 — ✅ 검증됨(8kw `4014901`, 2026-06-11)**: 지연은 hop당 고정·target 인덱스 무관이므로, **더미 EPWM0(output-less)을 공용 소스로 두고 EPWM2/4/7 모두 EPWM0 SYNCOUT을 1-hop으로 선택**하면 **상호 정수클록 스큐 0**(잔여 sub-clock은 TRM 모델 밖 — 실측 ±2 ns). 실측: 비대칭 ~22 ns → **±2 ns(5 ns 양자화 + sub-clock 잔류)**. 풀브리지 전 출력 모듈을 동일 hop으로 두는 것이 정석. 근거·한계·레지스터 표 [[am263p_epwm_sync_topology]].

---

## dead-time ns 단일소스 연계

같은 보드에 **dead-band 레그(같은 모듈)** 와 **SYNC+CMPB 레그(두 모듈)** 가 공존해도, dead-time **ns 소스는 하나의 `#define`** 으로 통일할 수 있다 — "**메커니즘 둘·ns 소스 하나**".

- 단일 소스 `ETA_DEADTIME_NS` → `DT_COUNTS = ETA_NS_TO_COUNTS(ns)` 매크로(정수 floor). **TBCLK=200 MHz → 1 count = 5 ns**(절삭손실은 5 ns 배수에서 0).
- 같은 모듈 레그: `EPWM_setRisingEdgeDelayCount`/`setFallingEdgeDelayCount`에 `DT_COUNTS` 적용(RED=FED 대칭).
- 두 모듈 레그: `EPWM_setCounterCompareValue(…COMPARE_B…)`에 `TBPRD/2 − DT_COUNTS` 적용.
- 숫자만 바꿔 재빌드하면 두 레그 dead-time이 함께 추종(**build-per-change**). 상세 매크로·검증표는 [[pwm]] §dead-time 단일소스.

---

## 검증 (8kw 실측)

- **P1 자유구동 단독검증 → SYNC 결선** (`6e6b342`): EPWM4_A=HS2 free-run 단독 확인 후 SYNC 결선. 100 kHz, shoot-through 0.
- **P2 dead-time 스윕** (`8046744`·`d01fc0a`, Saleae 4ch, transition CSV): 150/300 ns(100 kHz) + 100/150/400 ns(85 kHz). 두 레그 dead-time 명목 선형 추종, shoot-through 0. 레그2 비대칭 ~11 ns(HS→LS vs LS→HS) 첫 실측 — 합 보존 확인. 결과표 [[pwm]] §검증 방법·결과.
- **EPWM0 fan-out + 동형화** (`4014901`, Saleae 4ch 500MS/s): 100/150/250/400 ns 4-DT sweep. **비대칭 ~22 ns → ±2 ns(측정 격자 바닥)**. 4에지 시차 ≤2 ns(레그1·레그2 동형). high-time 4채널 완전 일치. shoot-through 0(전 구간). 레그1 회귀 없음. 리포트 [[pwm_leg2_isoform_report]].

---

## 대조 — 같은 모듈 dead-band vs 두 모듈 SYNC

| 구분 | 같은 모듈 (dead-band) | 두 모듈 (SYNC+CMPB) |
|------|----------------------|---------------------|
| 상보 | 모듈 dead-band 유닛이 A/B 상보 자동 | slave AQ 반전 |
| dead-time | RED/FED 카운트(대칭, 주기당 갭 2개) | CMPB 오프셋 `TBPRD/2 − DT` |
| 위상 | 한 모듈이라 자동 | master syncout→slave syncin, phaseShift=0 **명시 SYNC 필요** |
| 함정 | (적음) | CMPB 부호(`<TBPRD/2`), SYNC-in 기본 disable |
| 8kw 사례 | 레그1 = EPWM2_A/B (dead-band) | 레그2 = EPWM4_A@J6.52(HS2) + EPWM7_B@J6.51(LS2) (isoform AQ+2-compare, EPWM0 fan-out) |

---

## 8kw 구체 인스턴스 (출처)

- **SYNC 토폴로지 (신 — `4014901`, branch pwm-deadtime)**: **output-less EPWM0**(SysConfig 인스턴스, `syncout=ON_CNTR_ZERO`) → EPWM2/4/7 모두 `EPWMSYNCINSEL=EPWM0_SYNCOUT` (1-hop). 모듈간 스큐 ~22 ns → **±2 ns**.
- **레그2 isoform**: HS2 = **EPWM4_A @ J6.52**, LS2 = **EPWM7_B @ J6.51**.
  - EPWM4_A: CMPA = TBPRD/2 + DT, CMPB = TBPRD/2 (AQ: UP_CMPA→HIGH / DOWN_CMPB→LOW).
  - EPWM7_B: CMPA = TBPRD/2 − DT, CMPB = TBPRD/2 (AQ: ZERO→HIGH / UP_CMPB→LOW / DOWN_CMPA→HIGH).
  - @150 ns, TBPRD=1176: EPWM4_A CMPA=588+30=618, CMPB=588. EPWM7_B CMPA=588−30=558, CMPB=588.
- **주파수**: **85 kHz 고정** (`d01fc0a`, Saleae 85.032 kHz). `TBPRD=1176`, TBCLK=200 MHz, 1 count=5 ns.
- **단일소스 위치**: `ETA_DEADTIME_NS`는 `src/eta_bsp/eta_tuning.h`(100~400 ns `#error` 가드). `eta_pwm_init()` 런타임 override → SysConfig 면역.
- 근거 커밋: `6e6b342`(SYNC 상보), `8046744`(단일소스·스윕), `d01fc0a`(85 kHz·비대칭 첫 실측), `4014901`(EPWM0 fan-out+isoform — 비대칭 ~22 ns→±2 ns). branch pwm / pwm-deadtime. 리포트 [[pwm_leg2_isoform_report]].

---

## 관련 페이지

- [[pwm]] — 8kw PWM 작업 호. §dead-time 단일소스(매크로·검증표)·§Pin4(이 패턴의 구현 절).
- [[pwm_pinmap]] — 레그2 핀맵·EPWM 인스턴스 자유구동 사실.
- [[am263p_epwm_primary_pad_no_force_io]] — EPWM primary 패드 출력 정본(형제).
- [[am263p_iomux_force_io_enable]] — alt-function 패드 force 정본(형제).
- [[lp_am263p_ug]] — 핀먹스 Mode0/alt 표(핀↔채널 판별).
