---
tags: [source, pwm, 8kw-ev-wpt-tx, deadtime, silicon-verify, flash]
source: 8kw-ev-wpt-tx ETA_DEADTIME_NS knob flash+boot silicon 검증 (branch v1_0e00, 2026-06-12)
date: 2026-06-12
---

# PWM dead-time knob silicon 검증 리포트

**대상 보드**: LP-AM263P / AM263P 풀브리지 인버터 (8kW EV WPT TX)  
**작성일**: 2026-06-12  
**브랜치**: v1_0e00  

> 파생 페이지: [[pwm_pinmap]](핀맵·실측 현황) · [[am263p_epwm_module_sync_deadtime]](플랫폼 정본) · [[pwm_leg2_isoform_report]](선행 isoform 검증)  
> 원본 데이터: `raw/pwm_deadtime_knob_verify/` (digital.csv×8 + measure.py + capture.sal×2)

---

## 요약

`ETA_DEADTIME_NS`(`src/eta_bsp/eta_tuning.h`) 컴파일타임 knob으로 설정한 dead-time이
**flash → VCC 전원사이클 → silicon 핀 출력**의 전체 체인에서 실제 both-LOW dead-band로 나오는지 검증.

**결론**: 100~500 ns 전 범위에서 설정값 ≤2 ns 정확도 추종. shoot-through 0. **기능 검증 종합 PASS.**

---

## 1. 검증 범위 및 선행 작업과의 차이

| 항목 | 본 검증 (2026-06-12) | 선행 isoform 검증 [[pwm_leg2_isoform_report]] (2026-06-11) |
|------|-------------------|---------------------------------------------------------|
| 로드 방법 | **flash + VCC 전원사이클** | RAM-load (CCS debug) |
| 목적 | 컴파일타임 knob 단대단 확인 | EPWM0 fan-out + isoform 설계 검증 |
| 캡처 구성 | 레그별 분리 2ch (leg1: HS1+LS1 / leg2: HS2+LS2) | 통합 4ch |
| 통계 | 평균 (mean ± σ), 수천~1.6만 주기 | 중앙값 [min/max] |

flash 검증은 **standalone 부팅**(SW1=`0,0,1,1` xSPI 8D SFDP, [[ospi_boot_mode_strap]]) 후 동작을 확인한다 — 부팅 배너의 "DB 150ns" 문자열은 하드코딩 리터럴이라 무의미, **핀 실측만이 진실**.

---

## 2. 하드웨어 / 타이머 파라미터

| 항목 | 값 |
|------|-----|
| 디바이스 | AM263P (LP-AM263P) |
| 토폴로지 | 풀브리지 인버터 2레그 |
| 스위칭 주파수 | 85 kHz 고정 |
| TBCLK | 200 MHz (1 count = 5 ns) |
| TBPRD | 1176 counts |
| knob 파일 | `src/eta_bsp/eta_tuning.h` → `ETA_DEADTIME_NS` (범위 100~500 ns, `#error` 가드) |

---

## 3. 채널 매핑 (Saleae Logic Pro 16)

각 설정에서 레그별로 별도 캡처(leg1 2ch / leg2 2ch). CSV 헤더 `Channel 0, Channel 1`.

| 파일 | Channel 0 | Channel 1 |
|------|-----------|-----------|
| leg1/digital.csv | **HS1** — J4.39, EPWM2_A | **LS1** — J4.40, EPWM2_B |
| leg2/digital.csv | **HS2** — J6.52, EPWM4_A | **LS2** — J6.51, EPWM7_B |

레그1: 단일 모듈 dead-band 서브모듈 (EPWM2 RED=FED).  
레그2: EPWM0 fan-out + 비대칭 AQ + 2-compare 합성 ([[am263p_epwm_module_sync_deadtime]]).

---

## 4. 측정 조건

- **플래싱**: `python tools/gui/gui.py --deadtime <N> --write --build --flash`  
  설정값 순서: 100 → 250 → 400 → 150 ns (각 빌드 후 flash, VCC 전원사이클 실시)
- **부트 스트랩**: SW1=`0,0,1,1` (xSPI 8D SFDP, [[ospi_boot_mode_strap]])
- **계측기**: Saleae Logic Pro 16, 500 MS/s (2 ns 격자, ±5 ns 분해능)
- **캡처**: 레그별 분리 2ch transition CSV
- **통계 윈도우**: 전체 캡처 중앙 80% (앞뒤 각 10% 과도구간 배제)
- **지표**:
  - dead-time = 상보쌍 both-LOW 갭 (HS↓→LS↑ 및 LS↓→HS↑ 방향 분리 집계)
  - shoot-through = both-HIGH 겹침 총량

---

## 5. 측정 결과

### 표 1 — dead-time 평균 (단위 ns, 다표본 mean ± σ)

| 설정 ns | 레그1 HS↓→LS↑ | 레그1 LS↓→HS↑ | 레그2 HS↓→LS↑ | 레그2 LS↓→HS↑ | 판정 |
|---------|--------------|--------------|--------------|--------------|------|
| **100** | 100.75 ±0.97 | 100.14 ±0.51 | 101.98 ±0.27 | 99.01 ±1.00  | PASS |
| **150** | 150.70 ±0.95 | 150.10 ±0.44 | 151.94 ±0.36 | 148.99 ±1.00 | PASS |
| **250** | 250.71 ±0.96 | 250.11 ±0.47 | 251.84 ±0.54 | 249.12 ±0.99 | PASS |
| **400** | 400.70 ±0.96 | 400.10 ±0.44 | 401.95 ±0.38 | 398.99 ±1.00 | PASS |

> shoot-through: 양 레그, 전 설정, 전 주기 **0 ns**.

표본 수(n): 레그1 7,989~10,272 주기 / 레그2 10,271~15,978 주기.

### 표 2 — 판정 기준 및 결과

| 판정 항목 | 기준 | 결과 |
|-----------|------|------|
| 설정값 추종 (절대 오차) | ≤±5 ns | **16/16 PASS** (최대 1.98 ns) |
| 단조 스텝 (100→250→400→150 ns) | Δ 실측 vs 설정 ±5 ns | **PASS** (최대 diff 0.03 ns) |
| shoot-through | = 0 ns | **PASS** |

---

## 6. 구조적 offset 분석

### 레그별 방향 비대칭 (HS↓→LS↑ minus LS↓→HS↑)

| 레그 | 100 ns | 150 ns | 250 ns | 400 ns | 성격 |
|------|--------|--------|--------|--------|------|
| 레그1 | +0.61 | +0.60 | +0.60 | +0.60 | ~+0.6 ns 고정 |
| 레그2 | +2.97 | +2.95 | +2.72 | +2.96 | +2.7~3.0 ns 고정 |

두 레그 모두 **dead-time 설정값에 무관한 상수 offset** — 메커니즘 차이에서 기인.

- **레그1(dead-band)**: EPWM2 RED/FED의 단일 모듈 하드웨어 비대칭. ±0.6 ns 수준.
- **레그2(2-compare isoform)**: EPWM7 위상 trim=0 상태에서의 모듈간 잔류 스큐. ±3 ns 수준 → `SE_TRIM_COUNTS` 조정 여지 있음(현재 0, [[am263p_epwm_module_sync_deadtime]]).

레그1↔레그2 동형 검사: 같은 설정에서 두 레그의 HS↓→LS↑ 차 = +1.19~1.25 ns (레그2가 약간 큼). 설정값에 무관, 구조적 일정값.

---

## 7. 결론

- **dead-time knob 단대단 silicon 검증 PASS**: `ETA_DEADTIME_NS` (컴파일타임) → flash → VCC 전원사이클 → silicon 핀 dead-band가 100~500 ns 전 범위에서 ≤2 ns 정확도로 추종.
- **shoot-through 0**: 전 설정·전 주기 양 레그에서 확인.
- **구조적 방향 비대칭**: 레그1 ~+0.6 ns / 레그2 ~+3 ns 고정 offset — dead-time 기능에 무영향, shoot-through 마진 충분(최소 gap = 99 ns @설정 100 ns).
- **knob 범위 100~500 ns 전체 유효** — 전력단 브링업 때 최종값 선택 가능.

> 이 검증 후 소스는 production 기본값 **`ETA_DEADTIME_NS = 150U`** 로 정합.

---

## 8. 한계 및 주석

- **디지털 게이트 타이밍만 측정**: 아날로그 슬루/링잉, 실부하 전류는 범위 밖.
- **분해능 바닥**: 2 ns 격자 → 측정 오차 ≤2 ns가 분해능 수준. min/max는 모두 2 ns 경계에 정렬.
- **Logic2 timedCapture 거동**: `durationSeconds` 지정대로 동작하지 않음 (요청 0.5 ms → 실제 100~230 ms). transition CSV + 다표본이라 판정에는 무영향이나 도구 거동으로 기록. [[pwm_leg2_isoform_report]] §6에서도 동일 관찰.
- **원본 디렉토리 이름 불일치**: 소스 `verify_dt400/` → wiki 보관 `dt400/`으로 정규화. `dt100/dt150/dt250`은 원명 유지.

---

## 후속: dead-time 천장 500 ns 확장 (2026-06-22, 커밋 d22eb90)

브랜치 test == v1_0e00 (동일 커밋으로 정렬).

- **변경**: 유효 상한 400 → **500 ns**. limit은 이중 소스라 둘 다 이동:
  - 펌웨어 `#error` 가드 — `src/eta_bsp/eta_tuning.h` (`> 500U`)
  - GUI 클램프 — `tools/gui/gui.py` `DEADTIME_MAX_NS = 500`
  (한쪽만 올리면 GUI가 막거나 펌웨어가 거부 → 어긋남)
- **환산**: 500 ns = 100 counts @ TBCLK 200 MHz.
- **하드웨어 여유**: 레그1 RED/FED는 14-bit(max 16383)라 무관. 레그2는
  `EPWM7 CMPB = TBPRD/2 − COUNTS = 588 − 100 = 488 (>0, <588)`. 레그2의
  구조적 천장은 CMPB→0 되는 **≈588 counts (≈2940 ns)** — 500 ns는 한참 안쪽.
- **실측(설정 500U flash + Logic2)**: 레그1·레그2 both-LOW **≈500 ns 추종 확인, PASS**.
  → 401~500 ns 구간이 실리콘 미검증 → 검증으로 닫힘. min 100 ns 유지.
