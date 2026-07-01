---
tags: [source, adc, 8kw-ev-wpt-tx, repeater, timing, silicon-verify]
source: 8kw-ev-wpt-tx ADC N=16 리피터 버스트 트리거→버스트끝 타이밍 Saleae Logic2 디지털 캡처. 코드 트리 6993a40 (2026-06-30)
date: 2026-06-30
---

# ADC 리피터 버스트 N=16 타이밍 — Saleae 실측 리포트

**대상 보드**: LP-AM263P / AM263P4-Q1 (R5FSS0-0), MCU+ SDK am263px 26.00.00
**작성일**: 2026-06-30
**코드 트리**: 8kw-ev-wpt-tx `6993a40`

> 정본 환원처: [[am263p_adc_repeater_burst]] §3(버스트 실측 타이밍) · [[am263p_adc_instance_allocation]] §변환시간 예산(첫 라이브 실측) · [[am263p_adc_ppb_averaging]] §6(트리거당 N회 확인).
> 원본 데이터: `raw/adc_repeater_burst_timing/digital.csv` (ch0/ch1, 48,724 엣지, ≈144 ms, 12,260 주기).
> 후속 노이즈 FFT 진단(다른 목적, 같은 GPIO95 마커): [[adc_noise_fft_probe]].

---

## 요약

N=16 리피터 버스트(`ETA_ADC_OVERSAMPLE_LOG2=4`)가 **한 EPWM0_SOCA 트리거당 정확히 OSINT 1회**(=85 kHz)를 내는지, 버스트가 트리거 주기 안에 마감되는지를 디지털 2채널로 실측.

**결론**:
- 트리거당 OSINT **정확히 1회** (12,260/12,260, 누락·중복 0) → **리피터 버스트가 한 트리거에 16변환을 몰아넣음이 실증됨**. (분산 누적이면 85 kHz/16 ≈ 5.3 kHz여야 하나, 실측 OSINT = 85.03 kHz.)
- 트리거→버스트끝(ISR 진입) = **3.12 µs** = 주기(11.76 µs)의 **26.5%** → 마진 충분.
- N=16 실효 cadence **≤ 195 ns/변환** (상한; IRQ 진입지연 포함) — 정적 모델 285 ns보다 **빠름**.

---

## 1. 캡처 구성 (Saleae Logic2)

CSV 헤더 `Time [s], Channel 0, Channel 1`. 디지털 transition 캡처.

| 채널 | 신호 | 프로브 | 역할 |
|------|------|--------|------|
| ch0 | **EPWM2_A** — HS1 게이트 (MCU 3.3V) | J4.39 ([[pwm_pinmap]]) | 스위칭 위상 기준 (EPWM0과 syncin 동기) |
| ch1 | **GPIO95** — ADC0 OSINT ISR 진입 HIGH / 종료 LOW | J4.31 ([[am263p_lp_debug_gpio]]) | ADC0 샘플 완료(버스트 끝) 마커 |

- 기간 ≈ 144 ms, 스위칭 주기 12,260개, 표본 12,259~12,260.
- 마커 코드: `eta_bsp_adc_eoc_isr` 진입 시 GPIO95 HIGH(`eta_bsp_adc.c:156`) / `ADC_readPPBSum` 후 LOW(`:160,172`). `ETA_BSP_ADC_DBG_MARK_IDX = 0U`(`:60`) → **마킹 대상 = ADC0 / I_COIL_SEN 단독**.
- ADC 트리거원 = EPWM0_SOCA @ TBCTR_ZERO, prescale 1(주기당 1트리거) — `example.syscfg:224–231`. EPWM0의 ZERO는 직접 캡처하지 않고 EPWM2_A 위상으로 역산(아래 §3).

---

## 2. 측정값 (사실)

> 전부 디지털 엣지 직접 측정. ADC0 단독 마킹.

| 항목 | 측정값 | 비고 |
|------|--------|------|
| 스위칭 주기 T | **11.7603 µs** (sd 0.8 ns) | EPWM2_A 상승엣지 간격 |
| 스위칭 주파수 f | **85.032 kHz** | = 1/T. [[pwm_pinmap]] TBPRD=1176 UP_DOWN(=11.76 µs)와 합치 |
| EPWM2_A HIGH | 5.480 µs, 듀티 **46.60%** | 데드밴드로 50%에서 −3.4% |
| EPWM2_A 상승 → GPIO95 상승 | **+0.005 µs** (≈5 ns) (sd 55 ns) | 사실상 동시 |
| EPWM2_A *하강* → GPIO95 상승 | 6.285 µs (sd 55 ns) | ※ §방법론 메모 참조 |
| GPIO95 펄스폭 (= ISR 실행시간) | **0.304 µs** (sd 1 ns, max 0.36 µs) | EOC ISR 진입~종료 |
| OSINT 발생 횟수 | GPIO95 상승 **12,260** = EPWM2_A 상승 **12,260** | **주기당 정확히 1회**, 누락·중복 0 |
| 트리거(EPWM0 TBCTR=ZERO) → GPIO95 상승 | **3.12 µs** | 위상법(E2상승−0.265·T) |
| (동) 교차검증 | **3.14 µs** | LOW중점법 — 두 방법 24 ns 내 일치 |

---

## 3. 트리거 시각(EPWM0 ZERO) 역산법

EPWM0의 TBCTR=ZERO(ADC 트리거 발행 시각)는 디지털로 직접 캡처하지 않았다. EPWM2가 EPWM0에 syncin 동기(`example.syscfg:202` `EPWM_SYNC_IN_PULSE_SRC_SYNCOUT_EPWM0`)되어 **EPWM2_A가 EPWM0 ZERO에 고정 위상**을 가지므로 두 방법으로 역산, 24 ns 내 일치:

- **위상법**: 트리거 시각 = EPWM2_A 상승 − 0.265·T.
- **LOW중점법**: EPWM2_A LOW 구간 중점 기준.

⇒ 트리거 → GPIO95 상승 = **3.12 µs** (= 16변환 버스트 + OSINT→IRQ 진입지연).

---

## 4. 역산 — N=16 실효 cadence (추론, 상한)

> **측정값(§2)이 아니라 거기서 나온 역산이다.** 상한·조건을 명시한다.

- 트리거→GPIO95상승 = 3.12 µs = **(16변환 백투백 버스트) + (OSINT→IRQ 진입지연)**.
- ⇒ N=16 실효 cadence **≤ 3.12 µs / 16 = 195 ns/변환**.
  - **상한이다** — 3.12 µs는 IRQ 진입지연을 포함하므로 순수 변환 cadence는 195 ns보다 **작다**. 195 ns를 순수 cadence로 단정하지 말 것.
- **정적 모델 대비**: wiki 정적 산정 cadence = 285 ns(tSH 80 + tEOC 205, [[am263p_adc_instance_allocation]]). 실측 상한(≤195 ns) < 정적 보수치(285 ns) → **실측이 더 빠르다**.
  - 백투백 버스트의 파이프라인 오버랩이 원인으로 보이나 **공식 미확정**(아래 빈자리). 정적 285 ns는 보수 상한으로 유효.
- **주기 점유율**: 버스트+IRQ = 3.12 µs = 주기의 **26.5%**. ISR 실행 0.304 µs 별도. → 마진 충분.
- **ADC1(2 SOC=32변환) 추론**: cadence가 유사하면 ~6.2 µs ≈ 주기의 53% → 오버런 없음. **[추론]** — ADC1은 본 측정 대상 아님.

---

## 5. 사실 / 추론 / 미확정 가름

- **사실 (측정)**: §2 표 전부 — 트리거당 OSINT 1회(85.03 kHz), 트리거→버스트끝 3.12 µs, ISR 0.304 µs, 12,260/12,260 1:1.
- **추론 (상한/조건)**: §4 — 실효 cadence ≤195 ns(IRQ 지연 포함 상한), ADC1 ~53% 점유(미측정).
- **미확정 (봉합 말 것 — 호명 유지)**:
  - **IRQ 진입지연 분해 미수행** — 3.12 µs 중 순수 버스트 vs OSINT→ISR 진입 분리 못 함 → 순수 cadence 절대값 미확정.
  - **마지막 변환 마감 공식 미확정** — 실측이 정적식보다 빠르다는 데이터 포인트는 얻었으나 (N−1)(tSH+tEOC)+(tSH+tLAT) 확정엔 부족.
  - **레지스터 readback(NSEL/LIMIT/SHIFT/COUNT) 미수행** — 스코프로 OSINT 레이트·버스트 타이밍은 확인됐으나 레지스터 필드값은 미확인([[am263p_adc_ppb_averaging]] §7).
  - **ADC1 OSINT 발화 횟수 미확정** — 본 측정 ADC0 단독.

---

## 6. 방법론 메모 (재발 방지)

1차 스코프 판독에서 "EPWM2_A 상승 → GPIO95 상승 ≈ 6.284 µs"로 본 것은 **하강엣지 기준 측정 착오**였다 — E2 *하강* → G95 상승 = 6.285 µs로 정확히 재현된다. 실제 *상승* → 상승은 ≈0(동시, +5 ns). **향후 측정 시 기준 엣지(상승/하강)를 먼저 확인할 것.**

---

## 관련 페이지

- [[am263p_adc_repeater_burst]] — 리피터 버스트 메커니즘·SDK 정본 (이 실측의 §3 환원처).
- [[am263p_adc_instance_allocation]] — 변환시간 예산·N 상한 (정적 285 ns vs 실측 ≤195 ns 병기).
- [[am263p_adc_ppb_averaging]] — PPB 누적/블록평균 (트리거당 N회 확인 노하우).
- [[adc_noise_fft_probe]] — 같은 GPIO95 마커를 쓰는 후속 노이즈 진단(다른 목적).
- [[adc_pinmap]] — 8kw ADC 신호→인스턴스 배치.
