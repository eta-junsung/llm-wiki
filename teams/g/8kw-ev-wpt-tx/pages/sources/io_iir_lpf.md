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

- ⚠️ **우리 HW 적용 여부 확인 필요**: 회로도상 I_COIL은 T1 PA6322 **CT(85 kHz 공진전류)**([[board_schematic_v1_0e00]]), 그런데 [[fod_i_coil_observation]]는 I_COIL_SEN을 **CT→정류→RC평활 단극성 DC 포락선**으로 본다. 단극성 DC라면 `−Vadc/2` 바이폴라 보정이 안 맞을 수 있음 → **오프셋 값·유무를 HW로 확정**(추론 금지).

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

1. **"Io" = 어느 ADC 채널?** 후보 I_COIL_SEN(ADC0, J3.28) / I_LCC_SEN / GA_Iin_SEN. 원본 `ADC_SOC_NUMBER1`/Io → I_COIL_SEN 추정, 확정 필요. ([[adc_pinmap]])
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
