---
tags: [source, adc, 8kw-ev-wpt-tx, filter, iir, lpf]
source: 설계자 전달 필터 스펙 3종 — Digital_Filter.html(계수·차분식·코드매핑) + Digital_filter.xlsx(시뮬레이션) + "Digital Filter Implementation on 16-Bit Microcomputers" PDF(고정소수점 구현 일반 참고). 2026-07-01 수령. 원본 raw/io_iir_lpf/.
date: 2026-07-01
---

# Io 2차 IIR 저역통과 필터 (io_iir_lpf) — 스펙 ingest

> 설계자가 전달한 **Io ADC 스위칭 노이즈 제거용 2차 IIR biquad 저역통과 필터** 스펙. 구현 예정(구현만 먼저, 검증은 ADC 안정화 후). 로드맵 [[adc]], 현황 [[status]].
> 원본(immutable): `raw/io_iir_lpf/io_iir_lpf_spec.html`(핵심) · `raw/io_iir_lpf/io_iir_lpf_sim.xlsx` · `raw/io_iir_lpf/digital_filter_impl_16bit_micros.pdf`.
> ⚠️ HTML이 참조하는 `digital_filter_chart.png`는 미수령 — 차트 이미지 깨짐(스펙 텍스트·계수는 온전).

---

## 요약

- **필터 종류**: Direct Form I, **2차 IIR (biquad) 저역통과** — Butterworth 2차 LP 근사.
- **목적**: Io(코일/전류) ADC의 **85 kHz 스위칭 노이즈 제거**. 차단 주파수 수십~수백 Hz [추정].
- **설계 근거(저역통과 증거)**: `b0 = b2`(대칭 → 선형위상) + `b1 = 2·b0` → Butterworth 2차 LP 형태.
- **동작 샘플레이트**: fs ≈ 85 kHz (CLA/FB 주파수 기준). 현 8kw ADC 출력률(EPWM0_SOCA burst 출력 85 kHz/인스턴스, [[am263p_adc_repeater_burst]])과 일치.
- **출처 코드**: C2000/CLA 스타일(`dsp_adc_LPFMON`, `ADCARESULT_BASE`, `ADC_SOC_NUMBER1`) — AM263P로 **포팅 대상**(복붙 아님).

---

## 1. 차분 방정식 (코드 그대로 — 재유도 금지)

```
out0 = b0·in0 + b1·in1 + b2·in2 + a1·out1 + a2·out2
       └─── 피드포워드(b) ───┘   └─ 피드백(a) ─┘
```

- `in0/in1/in2` = 현재/1샘플전/2샘플전 입력, `out1/out2` = 1샘플전/2샘플전 출력.
- ⚠️ **부호 규약**: `a1/a2`는 이미 부호가 접혀 있어 식에서 **더한다**(`+a1·out1 + a2·out2`). 표준 DF-I의 `−a1·y[n-1] − a2·y[n-2]` 형태가 **아님** — 구현 시 부호를 다시 뒤집지 말 것.

---

## 2. 계수값 — 코드값(85 kHz 설계) 사용

| 계수 | **코드값 (채택)** | Excel값 (40 kHz 설계, 참고) | 역할 |
|------|------------------|-----------------------------|------|
| b0 | **9.75e-6** (0.00000975) | 1.0e-5 | 현재 입력 |
| b1 | **1.95e-5** (0.0000195) | 2.0e-5 | 1샘플 전 입력 |
| b2 | **9.75e-6** (0.00000975) | 1.0e-5 | 2샘플 전 입력 |
| a1 | **1.987473** | 1.987473 | 1샘플 전 출력 피드백 |
| a2 | **−0.987512** | −0.987472 | 2샘플 전 출력 피드백 |

- **왜 코드값?** Excel은 Ts = 1/40,000(40 kHz)로 설계, 코드는 **85 kHz 동작 기준으로 재설계**(Ts ≈ 11.76 µs). a2·b계수 정밀값 차이는 그 결과. 우리 보드가 85 kHz라 **코드값이 정본**.
- 정밀 차단주파수 확인법: `io_iir_lpf_sim.xlsx` C3~C7에 코드값 입력 → sheet1 차트로 주파수 응답 확인(스펙 §7).

---

## 3. 입력 전처리 — 바이폴라 중점 보정

원본 코드는 ADC 원시값에서 중점을 뺀다:

```
in0 = ADC_readResult(...) - Vadc/2      // 전류는 ±방향 모두 측정 → 바이폴라 중점 보정
```

- ⚠️ **이건 필터 스펙이 아니라 우리 보드 프론트엔드가 결정**한다. `−Vadc/2`는 **신호가 바이폴라(±)인데 프론트엔드가 Vref/2로 레벨시프트해 실은 경우에만** 필요(중점을 도로 빼 부호 복원). **0 기준 단극성**(정류→평활 DC 포락선)이면 **빼면 안 됨**(음수로 처박힘). 벤더가 뺀 건 그 벤더 보드(C2000)가 중점 바이어스였기 때문일 가능성 — 우리 보드에 자동 적용 금지.

**판단 기준 (둘 다 확정적):**

1. **회로도 프론트엔드** — I_COIL_SEN→ADC 경로에 **Vref/2 바이어스 회로**(Vref 분압/op-amp Vref/2 기준) 있으면 바이폴라 → 뺀다. CT→**정류(다이오드/브리지)**→RC 뒤 곧장 ADC면 단극성 → 안 뺀다. ⚠️ wiki 정황 갈림: 회로도=T1 PA6322 CT(=AC/바이폴라)([[board_schematic_v1_0e00]]) vs [[fod_i_coil_observation]]=정류→평활 단극성 DC 포락선 → CT 뒤 정류단 실존 여부가 관건.
2. **idle DC 베이스라인 실측 (우리 보드 결정본)** — 전력단 OFF/무전류에서 raw가 **~2048 counts(≈1.65V)** → 중점 바이어스=뺀다 / **~0 counts** 근처(전류 인가 시만 상승) → 안 뺀다. 이 실측은 어차피 **ADC 안정화 1단계(DC baseline 캡처, [[fod_i_coil_observation]]·[[adc_noise_fft_probe]] step1)**에서 나옴.

**권고 — 구현 순서와 맞물림**: biquad(ALG)는 오프셋 무관(순수 계산). App에서 `in0 = raw − offset`로 **오프셋을 파라미터/knob화**(하드코딩 금지), 초기값 0으로 **필터 먼저 구현**(이번 세션 범위=구현만) → 실제 offset은 **ADC 안정화 때 측정한 idle 베이스라인으로 확정**. ★바이폴라여도 공차 때문에 실제 중점≠정확한 Vref/2일 수 있어 **`Vadc/2` 이상값보다 측정된 zero-current 값**을 빼는 게 정확. 선형 필터라 오프셋을 필터 전/후 어디서 빼든(또는 [[adc_scaling]] 물리량 변환단) 필터링엔 영향 없음 → 처리 위치는 신호체인 배치와 함께 결정. **⟹ 이 항목은 필터 구현을 막지 않음.**

---

## 4. 코드→아키텍처 매핑 (구현 지침)

원본 3단계: ① 입력 시프트(in2←in1←in0←새 ADC) → ② 출력 시프트(out2←out1←out0) → ③ 차분식 계산.

4레이어 규약([[firmware_layering_8kw]]) 배치:

- **ALG (순수계산)**: biquad 연산 + 상태(in1,in2,out1,out2)를 `eta_alg_iir_lpf`(또는 계획명 `eta_alg_filter`)에 순수 함수 + 상태 struct로. ALG는 HAL/SDK/레지스터 모름.
- **App/HAL (HW 접점)**: ADC 읽기 + `−Vadc/2` 보정은 App(`eta_app_adc`)에서. ALG엔 깨끗한 `in0` + 이전 상태만 전달.
- **자료형**: R5F 하드웨어 FPU 보유 → **float 직접 사용 권장**(계수도 float). 고정소수점 포팅 불필요(참고 PDF `digital_filter_impl_16bit_micros.pdf`는 그 경우에만).
- **계수 단일 소스**: 헤더 매크로/const 1곳.

---

## 5. Excel 시뮬레이션 (설계 검증)

`io_iir_lpf_sim.xlsx` sheet1: E열 ADC input → K열 DF_result(필터 출력). 랜덤 ADC 입력(파란색)이 출력(빨간색)에서 **약 ~500으로 천천히 수렴** = 노이즈 억제 실증. 첫 3스텝: 입력 601.9/337.4/362.6 → 출력 0.00602/0.02737/0.06486(느린 상승).

---

## 6. 구현 전 확정 필요 (추론으로 채우지 말 것)

1. ~~"Io" = 어느 ADC 채널?~~ **✅ 확정 = I_COIL_SEN (ADC0 SOC0 AIN1, J3.28, IRQ147)** (2026-07-01 사용자 확인). 디버그 마커 `ETA_BSP_ADC_DBG_MARK_IDX 0U`와도 일치. ([[adc_pinmap]])
2. **`−Vadc/2` 바이폴라 보정 적용 여부** — §3 참조. 단극성 DC면 재결정.
3. **신호체인 삽입 위치 + A5/A6와의 관계**: A5(리피터 버스트 블록평균 N=16, [[am263p_adc_repeater_burst]])·A6(SW 이동평균)와 **성격 구분** — 이건 재귀형 IIR LPF. 이 IIR LPF가 A6 이동평균을 **대체**하는지 보완하는지 착수 시 결정.
4. **검증 순서**: 필터는 **구현만 먼저**, 실보드 파형·노이즈 검증은 **ADC 안정화([[adc_noise_fft_probe]]·[[fod_i_coil_observation]]) 이후**.

---

## 관련 페이지

- [[adc]] — ADC 작업 로드맵(필터는 A5/A6 신호체인 안정화 트랙에 인접).
- [[status]] — 현황·다음 시작점(io_iir_lpf 구현 착수).
- [[am263p_adc_repeater_burst]] — A5 리피터 버스트 N=16(HW 평균) — 이 IIR LPF와 직교(HW 평균 vs SW 재귀 LPF).
- [[adc_noise_fft_probe]] · [[fod_i_coil_observation]] — 필터 검증이 올라탈 ADC 노이즈 측정·안정화 트랙.
- [[board_schematic_v1_0e00]] — I_COIL=T1 PA6322 CT 신호체인(바이폴라/단극성 판정 근거).
- [[adc_scaling]] — 물리량 변환(필터 삽입 위치의 신호체인 이웃).
- [[firmware_layering_8kw]] — ALG/App 배치 규약.
