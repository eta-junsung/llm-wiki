---
tags: [concept, am263p, epwm, sync, deadtime, platform]
source: 2026-06-09~10 8kw-ev-wpt-tx PWM 레그2(EPWM4_A=HS2 / EPWM7_B=LS2 두 모듈) SYNC 상보·dead-time 실보드 검증 (commit 6e6b342 SYNC 상보 + 8046744 dead-time 단일소스·스윕)
date: 2026-06-10
---

# AM263P EPWM 모듈간 SYNC 상보·dead-time (두 모듈 풀브리지 레그)

> **AM263P 플랫폼 지식 정본.** [[am263p_epwm_primary_pad_no_force_io]]·[[am263p_iomux_force_io_enable]] 형제. 풀브리지 한 레그의 HS/LS 게이트가 **서로 다른 EPWM 모듈**에 라우팅되면, 한 모듈 안의 **dead-band 유닛(RED/FED)** 으로 상보+dead-time을 만들 수 없다. 두 모듈을 **SYNC로 위상 정렬 + CMPB 오프셋**으로 상보·dead-time을 만드는 패턴. 8kw 레그2에서 실증.

## 한 줄 요약

**HS와 LS가 다른 EPWM 모듈에 걸친 레그**는 ① master EPWM `syncout=ON_CNTR_ZERO` → slave `syncin`, slave `phaseShift=0`으로 **매 주기 영점에서 카운터 정렬**, ② slave 채널 **AQ 반전 + CMPB 오프셋**으로 상보 PWM + dead-time을 만든다. dead-time은 **`CMPB = TBPRD/2 − DT_COUNTS` (반드시 `< TBPRD/2`)** — `+`부호면 LS ON이 HS OFF 구간을 넘어 **shoot-through**. 같은 모듈 레그(dead-band RED/FED)와 **메커니즘은 다르지만 dead-time ns 소스는 하나**로 공유 가능.

---

## 언제 이 패턴이 필요한가

- 풀브리지/하프브리지 레그의 **HS·LS가 한 EPWM 모듈의 A/B 채널 쌍이 아닐 때.** 보드 라우팅상 두 게이트가 서로 다른 모듈 핀에 묶이면(핀먹스 제약), 모듈 내 dead-band 유닛은 **자기 모듈 A/B에만** dead-time을 넣으므로 쓸 수 없다.
- **판별**: 두 게이트 핀이 노출하는 SoC 채널이 같은 EPWM 인스턴스인가? 아니면(예: EPWM4 vs EPWM7) 이 패턴 필요. 핀↔채널은 UG 핀먹스 표 + 보드 회로도로 확인([[lp_am263p_ug]] Table 2-30).
- **대안(있으면 우선)**: 회로도 단계에서 HS/LS를 **한 모듈의 A/B를 노출하는 핀 쌍**으로 묶으면 dead-band로 단순화 — 보드 개선 후보.

---

## 패턴 (3단)

1. **위상 정렬 (SYNC)**: master EPWM **`syncout = ON_CNTR_ZERO`** → slave EPWM **`syncin = master의 SYNCOUT`**, slave **`phaseShift = 0`**. 두 모듈 카운터를 매 주기 영점에서 정렬한다.
2. **상보 (AQ 반전)**: slave 채널 **Action Qualifier 반전**으로 master(HS)의 반대 위상을 만든다.
3. **dead-time (CMPB 오프셋)**: slave **CMPB**를 `TBPRD/2`에서 dead-time 카운트만큼 **앞당겨** LS의 ON 에지를 HS OFF 뒤로 민다. 모듈 내 dead-band 레지스터 대신 **CMPB 오프셋**이 dead-time을 만든다.
   - **`CMPB_INIT = TBPRD/2 − DT_COUNTS`** (UP_DOWN 카운터 기준).
   - `DT_COUNTS = round(dead_time_ns × TBCLK_HZ)` (정수 floor — [[#dead-time ns 단일소스 연계]]).

---

## ⚠️ 함정

- **CMPB 부호 (shoot-through 직결)**: `CMPB`는 **반드시 `< TBPRD/2`**. `TBPRD/2 + DT`(부호 오류)로 두면 LS ON 구간이 HS OFF 구간을 **넘어 겹쳐 shoot-through**가 난다. 8kw 구현 중 1회 부호 오류로 발생→정정. 부호는 `−`.
- **SYNC-in 기본 disable**: SysConfig 기본 EPWM 인스턴스는 **SYNC-in disable + phaseShift=0**이라 단독 **자유구동(free-run)** 한다. 즉 **단일 모듈 핀은 위상기준 없이 독립 검증 가능**(이 점은 브링업에 유리)하지만, 이 패턴의 모듈간 위상정렬은 **SYNC를 명시 활성화**해야 성립한다 — 기본값으로는 두 모듈이 정렬되지 않는다. ([[pwm_pinmap]] §EPWM 인스턴스·자유구동)

---

## dead-time ns 단일소스 연계

같은 보드에 **dead-band 레그(같은 모듈)** 와 **SYNC+CMPB 레그(두 모듈)** 가 공존해도, dead-time **ns 소스는 하나의 `#define`** 으로 통일할 수 있다 — "**메커니즘 둘·ns 소스 하나**".

- 단일 소스 `ETA_DEADTIME_NS` → `DT_COUNTS = ETA_NS_TO_COUNTS(ns)` 매크로(정수 floor). **TBCLK=200 MHz → 1 count = 5 ns**(절삭손실은 5 ns 배수에서 0).
- 같은 모듈 레그: `EPWM_setRisingEdgeDelayCount`/`setFallingEdgeDelayCount`에 `DT_COUNTS` 적용(RED=FED 대칭).
- 두 모듈 레그: `EPWM_setCounterCompareValue(…COMPARE_B…)`에 `TBPRD/2 − DT_COUNTS` 적용.
- 숫자만 바꿔 재빌드하면 두 레그 dead-time이 함께 추종(**build-per-change**). 상세 매크로·검증표는 [[pwm]] §dead-time 단일소스.

---

## 검증 (8kw 실측)

- **자유구동 단독검증 → SYNC 결선**: master(EPWM4_A=HS2)는 free-run으로 단독 100 kHz/50% 확인 후, slave(EPWM7_B=LS2)를 SYNC 결선해 상보·dead-time 측정.
- **dead-time = 상보쌍 both-LOW 갭 / shoot-through = both-HIGH 겹침** (Saleae 4ch, transition CSV). 150/300 ns 두 빌드 4채널: 두 레그 dead-time이 명목 추종, **shoot-through 0**(양 빌드). 결과표 [[pwm]] §검증 방법·결과.

---

## 대조 — 같은 모듈 dead-band vs 두 모듈 SYNC

| 구분 | 같은 모듈 (dead-band) | 두 모듈 (SYNC+CMPB) |
|------|----------------------|---------------------|
| 상보 | 모듈 dead-band 유닛이 A/B 상보 자동 | slave AQ 반전 |
| dead-time | RED/FED 카운트(대칭, 주기당 갭 2개) | CMPB 오프셋 `TBPRD/2 − DT` |
| 위상 | 한 모듈이라 자동 | master syncout→slave syncin, phaseShift=0 **명시 SYNC 필요** |
| 함정 | (적음) | CMPB 부호(`<TBPRD/2`), SYNC-in 기본 disable |
| 8kw 사례 | 레그1 = EPWM2_A/B | 레그2 = EPWM4_A@J6.52(HS2) + EPWM7_B@J6.51(LS2) |

---

## 8kw 구체 인스턴스 (출처)

- **레그2**: HS2 = **EPWM4_A @ J6.52** (master), LS2 = **EPWM7_B @ J6.51** (slave). EPWM4 `syncout=ON_CNTR_ZERO` → EPWM7 `syncin`, EPWM7 `phaseShift=0`, EPWM7_B AQ 반전 + `ETA_EPWM7_CMPB_INIT = TBPRD/2 − ETA_DEADTIME_COUNTS`. 핀맵 정본 [[pwm_pinmap]].
- **주파수**: 8kw는 **85 kHz 고정**(사용자 확정 2026-06-10). dead-time 조정범위 **100~400 ns**(실험 후 고정 예정). dead-time 카운트는 **TBCLK 기준이라 주파수와 무관**(CMPB의 `TBPRD/2`만 주파수 따라 바뀜). 브링업 검증은 임시 100 kHz(TBPRD=1000)에서 수행됨.
- 근거 커밋: `6e6b342`(SYNC 상보), `8046744`(dead-time 단일소스·스윕). branch pwm.

---

## 관련 페이지

- [[pwm]] — 8kw PWM 작업 호. §dead-time 단일소스(매크로·검증표)·§Pin4(이 패턴의 구현 절).
- [[pwm_pinmap]] — 레그2 핀맵·EPWM 인스턴스 자유구동 사실.
- [[am263p_epwm_primary_pad_no_force_io]] — EPWM primary 패드 출력 정본(형제).
- [[am263p_iomux_force_io_enable]] — alt-function 패드 force 정본(형제).
- [[lp_am263p_ug]] — 핀먹스 Mode0/alt 표(핀↔채널 판별).
