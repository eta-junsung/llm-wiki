---
tags: [entity, adc, 8kw-ev-wpt-tx, pinmap]
source: 사용자 제공 (2026-06-04) — 회로도 전체 미ingest, 해당 신호 핀만 발췌. 6채널 완성·int_xbar/IRQ 코드 역산 갱신 (2026-06-09, commit c512e3b)
date: 2026-06-09
---

# adc_pinmap — 8kW WPT TX 보드 ADC 핀맵

> eta 보드 커넥터(J3) → LP-AM263P ADC 인스턴스/채널 → 신호 이름 대응표.
> 스케일링(변환식, 분압비, 센서 감도)은 [[adc]] 작업 A3 단계에서 채운다.
> 인스턴스 배치 근거·다음 보드 설계 규칙은 [[am263p_adc_instance_allocation]].
> 논리↔물리 인스턴스 고정(soft 재배치 함정)은 [[am263p_syscfg_soft_vs_hard_assign]].

---

## 핀맵

| J3 핀 | ADC 인스턴스 | SOC | 채널 | 신호 | enum | int_xbar / EOC IRQ |
|-------|------------|-----|------|------|------|--------------------|
| J3.24 | ADC1 | SOC0 | AIN0 | Temp_Module2 | ETA_ADC_CH_TEMP_MODULE2 | OUT_0 / IRQ146 |
| J3.25 | ADC2 | SOC0 | AIN0 | Temp_Module1 | ETA_ADC_CH_TEMP_MODULE1 | OUT_3 / IRQ149 |
| J3.26 | ADC3 | SOC0 | AIN0 | GA_Vin | ETA_ADC_CH_GA_VIN | OUT_4 / IRQ150 |
| J3.27 | ADC4 | SOC0 | AIN0 | I_LCC_SEN | ETA_ADC_CH_I_LCC_SEN | OUT_2 / IRQ148 |
| J3.28 | ADC0 | SOC0 | AIN1 | I_COIL_SEN | ETA_ADC_CH_I_COIL_SEN | OUT_1 / IRQ147 |
| J3.29 | ADC1 | SOC1 | AIN1 | GA_Iin_SEN | ETA_ADC_CH_GA_IIN_SEN | OUT_0 / IRQ146 |

- **6채널 전부 구현·실보드 raw→mV 검증 완료**(branch adc, commit c512e3b). 물리 인스턴스 **5개(ADC0~ADC4)** 사용.
- **ADC1만 SOC0(Temp_Module2)+SOC1(GA_Iin_SEN) 라운드로빈** — 인터럽트는 **SOC1 EOC 단일 ISR**로 2채널 동시 수확. 나머지(ADC0/2/3/4)는 SOC0 단독.
- 트리거 = RTI1(SysConfig 논리명 `CONFIG_RTI0`) 1 kSPS, 5개 인스턴스 전부 공유.
- ✅ **물리 인스턴스 + AIN 핀 모두 hard `$assign`** — 신규 채널 추가 시 솔버 재셔플([[am263p_syscfg_soft_vs_hard_assign]]) 방지. 재생성 후 물리 배정 ADC0~4 유지 확인(soft 잔존 리스크 해소).
- 채널 enum은 `eta_adc.c` 테이블(`g_eta_adc_inst[]`)이 단일 소스, `ETA_ADC_CH_COUNT`로 일원화.

---

## ADC 인스턴스 요약

| ADC 인스턴스 | 사용 채널 | 신호 |
|------------|---------|------|
| ADC0 | AIN1 | I_COIL_SEN |
| ADC1 | AIN0, AIN1 | Temp_Module2, GA_Iin_SEN |
| ADC2 | AIN0 | Temp_Module1 |
| ADC3 | AIN0 | GA_Vin |
| ADC4 | AIN0 | I_LCC_SEN |

---

## 미확인 — 추가 스펙 필요

스케일링 단계(A3)에서 아래 정보가 있어야 변환식을 쓸 수 있다:

| 신호 | 상태 | 비고 |
|------|------|------|
| Temp_Module1/2 | ✗ 미교정 | 온도 모듈 출력 특성 (V/°C, 오프셋, 선형 구간) 미입수 |
| GA_Vin | ✗ 미교정 | 분압 저항비 (R_top / R_bot) 미입수 |
| I_LCC_SEN | ✗ 미교정 | 전류 센서 감도 (mV/A), 오프셋 전압 미입수 |
| **I_COIL_SEN** | **✓ 해소** | **SCALE≈6.770 A/V, OFFSET≈4.198 A — 식·파라미터 [[adc_scaling]] §I_COIL_SEN** |
| GA_Iin_SEN | ✗ 미교정 | 다음 세션 진행 예정 |

AM263P ADC 파라미터:
- 분해능: 12-bit (0~4095 count)
- 레퍼런스 전압: **3.3V (VREFHI, 확정 — `ETA_ADC_VREFHI_MV=3300`, 사용자 확인 2026-06-24)** → LSB ≈ 0.81 mV
