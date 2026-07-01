# ADC 리피터 버스트 타이밍 — Saleae 원본 캡처

N=16 리피터 버스트(`ETA_ADC_OVERSAMPLE_LOG2=4`)의 트리거→버스트끝 타이밍 실측 원본.
분석·환원 결과는 [[adc_repeater_burst_timing]] (source 페이지).

## digital.csv

Saleae Logic2 디지털 transition CSV. 헤더 `Time [s], Channel 0, Channel 1`, 48,724 엣지 행.

| 채널 | 신호 | 프로브 |
|------|------|--------|
| Channel 0 | **EPWM2_A** — HS1 게이트 (MCU 3.3V) | J4.39 ([[pwm_pinmap]]) |
| Channel 1 | **GPIO95** — ADC0 OSINT ISR 진입 HIGH / 종료 LOW | J4.31 ([[am263p_lp_debug_gpio]]) |

- 캡처 기간 ≈ 144 ms, 스위칭 주기 12,260개.
- `ETA_BSP_ADC_DBG_MARK_IDX = 0U` → 마킹 대상 = ADC0 / I_COIL_SEN.
- 코드 트리: 8kw-ev-wpt-tx `6993a40`.
