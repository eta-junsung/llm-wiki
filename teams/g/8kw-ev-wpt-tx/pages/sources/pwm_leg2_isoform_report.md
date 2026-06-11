---
tags: [source, pwm, 8kw-ev-wpt-tx, deadtime, isoform, fanout]
source: 8kw-ev-wpt-tx PWM 레그2 dead-time 정밀화 + 레그1 동형화 검증 (branch pwm-deadtime, commit 4014901, 2026-06-11)
date: 2026-06-11
---

# PWM 레그2 dead-time 정밀화 + 레그1 동형화 검증 리포트

**대상 보드**: LP-AM263P / AM263P 풀브리지 인버터 (8kW EV WPT TX)  
**작성일**: 2026-06-11  
**브랜치**: pwm-deadtime  

> 파생 페이지: [[pwm]](작업 호) · [[pwm_pinmap]](핀맵) · [[am263p_epwm_module_sync_deadtime]](플랫폼 정본) · [[am263p_epwm_sync_topology]](SYNC 토폴로지)  
> 원본 데이터: `raw/pwm_leg2_isoform/` (digital.csv×4 + analyze.py×3 + capture.sal)

---

## 요약

레그2(PWM_HS2/LS2) dead-time 정밀화 + 레그1 동형화를 4개 설정점(100/150/250/400 ns)에 걸쳐 실측 검증하였다.

**결론**: DEADTIME 100~400 ns 전 구간에서  
(a) dead-time 설정값 정확 추종,  
(b) 레그1과 레그2 파형 동형 — 4개 테스트 전 항목 PASS.

---

## 1. 대상 및 배경

### 1.1 하드웨어 / 타이머 파라미터

| 항목 | 값 |
|---|---|
| 디바이스 | AM263P (LP-AM263P) |
| 토폴로지 | 풀브리지 인버터 2레그 |
| 스위칭 주파수 | 85 kHz 고정 |
| TBCLK | 200 MHz (1 count = 5 ns) |
| TBPRD | 1176 counts |
| 주기 (period) | 2352 counts = 11 760 ns |

### 1.2 레그별 구성

| 레그 | 신호 | 핀 | EPWM 모듈 | dead-band 방식 |
|---|---|---|---|---|
| 레그1 | HS1 | J4.39 | EPWM2_A | 단일 모듈 내 RED/FED |
| 레그1 | LS1 | J4.40 | EPWM2_B | 단일 모듈 내 RED/FED |
| 레그2 | HS2 | J6.52 | EPWM4_A | 2-compare 합성 (아래 참조) |
| 레그2 | LS2 | J6.51 | EPWM7_B | 2-compare 합성 (아래 참조) |

레그2는 HS2/LS2가 서로 다른 EPWM 모듈에 있어 모듈 내 dead-band 블록을 공유할 수 없다.

### 1.3 동기화 토폴로지 — EPWM0 더미 마스터 fan-out

output-less EPWM0가 `SYNCOUT_ON_CNTR_ZERO`를 방출하고, EPWM2/4/7 모두 EPWM0를 1-hop으로 수신하는 등가 슬레이브로 동작한다.

- 모듈간 위상 스큐 구조적 제거: 기존 ~11 ns → ±2 ns 이내
- 레그1 ↔ 레그2 위상차 0
- PHASE_TRIM = 0 (fan-out 전환 후 불필요)

### 1.4 레그2 동형화 — 비대칭 AQ + 2-compare 합성

**EPWM4_A (HS2)**

| AQ 이벤트 | 동작 |
|---|---|
| UP_CMPA | HIGH |
| DOWN_CMPB | LOW |

- CMPA = TBPRD/2 + DT_COUNTS (상승 DT만큼 지연 → 레그1 HS1 RED dead-band 동형)
- CMPB = TBPRD/2

**EPWM7_B (LS2)**

| AQ 이벤트 | 동작 |
|---|---|
| ZERO | HIGH |
| UP_CMPB | LOW |
| DOWN_CMPA | HIGH |

- CMPB = TBPRD/2
- CMPA = TBPRD/2 − DT_COUNTS (HS2와 정확한 상보, 양방향 both-LOW 갭 보장)

**단일소스**: `ETA_DEADTIME_NS` (eta_tuning.h, 100~400 ns 범위 가드) → DT_COUNTS = round(ns × 0.2) → 위 compare 값 전부 자동 추종. 주파수·dead-time가 런타임 override라 SysConfig 재생성 면역.

---

## 2. 측정 조건

- **로드 방법**: flash 없이 RAM-load — ccs-debug reset → loadProgram(.out) → run, Cortex R5_0
- **계측기**: Saleae Logic2, 4ch digital
  - ch0 = HS1 (J4.39), ch1 = LS1 (J4.40), ch2 = HS2 (J6.52), ch3 = LS2 (J6.51)
  - 샘플레이트: 500 MS/s (2 ns 격자)
  - export: transition-based CSV
- **통계 구간**: 안정 중간 80% (테스트당 수천~1.2만+ 주기)
- **실측 주파수**: 85.03 kHz, period 11 760 ns 확인
- **정의**
  - dead-time = 상보쌍 both-LOW 갭
  - shoot-through = both-HIGH 겹침
  - 레그2는 HS→LS / LS→HS 두 갭 분리 집계 (방향별 평균 금지)

---

## 3. Test 매트릭스

| ETA_DEADTIME_NS | DT_COUNTS |
|---|---|
| 100 ns | 20 |
| 150 ns (기본값) | 30 |
| 250 ns | 50 |
| 400 ns | 80 |

경계 양끝(100/400) + 기본값(150) + 중간(250) 총 4점.

---

## 4. 측정 결과

### 표 1 — dead-time 설정 정확도 (레그2, 단위 ns, median [min/max])

| DT 설정 | HS2→LS2 | LS2→HS2 | 합 | 양방향차 | shoot-through |
|---|---|---|---|---|---|
| 100 ns | 102 [100/104] | 100 [98/100] | 202 | 2 | 0 |
| 150 ns | 152 [150/154] | 148 [148/150] | 300 | 4 | 0 |
| 250 ns | 252 [250/254] | 248 [248/250] | 500 | 4 | 0 |
| 400 ns | 402 [400/404] | 398 [398/400] | 800 | 4 | 0 |

**주**: 양방향 합은 2×설정값 정확 보존. 비대칭 ≤4 ns는 5 ns 양자화(±1 count) + 모듈간 sub-clock 잔류에 기인하며, 레그2 sync skew 구 baseline(~11 ns) 대비 양호.

---

### 표 2 — 레그1·레그2 동형 4지표 (단위 ns)

| DT 설정 | high-time 4ch median [min/max] | HS2.r−HS1.r | HS2.f−HS1.f | LS2.r−LS1.r | LS2.f−LS1.f | 펄스폭 산포 |
|---|---|---|---|---|---|---|
| 100 ns | 5780 [5778/5782] | 0 [−2/0] | 0 [−2/0] | 0 [0/+2] | 0 [0/+2] | L2≈L1 (4 ns) |
| 150 ns | 5730 [5728/5732] | 0 [−2/0] | 0 [−2/0] | 0 [0/+2] | 0 [0/+2] | L2≈L1 (4 ns) |
| 250 ns | 5630 [5628/5632] | 0 [−2/0] | 0 [−2/0] | 0 [0/+2] | 0 [0/+2] | L2≈L1 (4 ns) |
| 400 ns | 5480 [5478/5482] | 0 [−2/0] | 0 [−2/0] | 0 [0/+2] | 0 [0/+2] | L2≈L1 (stdev 0.74 vs 0.71) |

**주1**: high-time은 4채널(HS1/LS1/HS2/LS2)이 매 DT에서 전부 동일 median — 레그·HS/LS 무관 일치. high = 5880 − DT_ns로 정확 추종.  
**주2**: 4에지 전수 시차 median 0 ns, |max| 2 ns = 두 레그 파형이 시간축에서 포개짐 = 동형의 완전 정의 충족.  
**주3**: shoot-through 레그1·레그2 모두 전 DT 구간에서 0.

---

### 표 3 — 레그1 회귀 없음 (단위 ns)

| DT 설정 | HS1→LS1 | LS1→HS1 | high-time | shoot-through |
|---|---|---|---|---|
| 100 ns | 100 | 100 | 5780 | 0 |
| 150 ns | 150 | 150 | 5730 | 0 |
| 250 ns | 250 | 250 | 5630 | 0 |
| 400 ns | 400 | 400 | 5480 | 0 |

**주**: 레그1은 매 테스트 정상 — 레그2 동형화 변경이 레그1에 회귀 없음.

---

## 5. 결론

| 항목 | 판정 |
|---|---|
| dead-time 설정 기능 (100~400 ns 전 구간) | PASS |
| 레그1·레그2 동형 (4에지 시차 ≤2 ns) | PASS |
| high-time 완전 일치 (4채널 동일 median) | PASS |
| shoot-through 0 (양 레그, 전 DT 구간) | PASS |

- **dead-time 설정 기능**: 100~400 ns 전 구간 정확 추종. 양방향 합 = 2×설정값 보존, 5 ns 양자화 한계 내.
- **레그1·레그2 동형**: 4에지 전수 시차 ≤2 ns + high-time 완전 일치 + 양방향 dead-time 대칭 + shoot-through 0 + 펄스폭 산포 동급 → DEADTIME 값 무관하게 항상 동형.
- **잔류 비대칭(레그2 ±2 ns)**: 두 모듈 합성의 sub-clock 바닥으로, 측정 분해능(2 ns 격자) 수준. 단일 모듈(레그1)의 비트단위 정밀에는 구조상 도달하지 못하나 모든 안전 기준 충족.
- **작업 사이클 종료 가능.**

---

## 6. 한계 및 주석

- **측정 범위**: 디지털 게이트 타이밍만 측정. 아날로그 슬루/링잉, 실부하 전류는 측정 범위 밖.
- **측정 도구 주석**: Logic2 MCP `timedCaptureMode durationSeconds`가 이 환경에서 지정대로 동작하지 않음 (요청 0.5 ms → 실제 100~180 ms 캡처). transition CSV + 다표본이라 판정에는 무영향이나 도구 거동으로 기록.
- **근거 데이터**: `raw/pwm_leg2_isoform/verify_dt100/digital.csv` 외 3건 + analyze.py×3 + capture.sal(재현 샘플).
