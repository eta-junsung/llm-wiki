---
tags: [entity, adc, lp-am263p, pinmap]
source: 사용자 제공 (2026-06-04) — 회로도 전체 미ingest, 해당 신호 핀만 발췌
date: 2026-06-04
---

# adc_pinmap — LP-AM263P eta 보드 ADC 핀맵

> eta 보드 커넥터(J3) → LP-AM263P ADC 인스턴스/채널 → 신호 이름 대응표.
> 스케일링(변환식, 분압비, 센서 감도)은 [[eta-adc]] 작업 A3 단계에서 채운다.

---

## 핀맵

| J3 핀 | ADC 인스턴스 | 채널 | 신호 | 비고 |
|-------|------------|------|------|------|
| J3.24 | ADC1 | AIN0 | Temp_Module2 | 온도 센서 모듈 2번 |
| J3.25 | ADC2 | AIN0 | Temp_Module1 | 온도 센서 모듈 1번 |
| J3.26 | ADC3 | AIN0 | GA_Vin | 입력 전압 감지 |
| J3.27 | ADC4 | AIN0 | I_LCC_SEN | LCC 전류 센서 |
| J3.28 | ADC0 | AIN1 | I_COIL_SEN | 코일 전류 센서 |
| J3.29 | ADC1 | AIN1 | GA_lin_SEN | 선형 센서 |

ADC1은 AIN0(Temp_Module2)·AIN1(GA_lin_SEN) 두 채널 사용 — SysConfig에서 동일 인스턴스 내 멀티채널로 설정.

---

## ADC 인스턴스 요약

| ADC 인스턴스 | 사용 채널 | 신호 |
|------------|---------|------|
| ADC0 | AIN1 | I_COIL_SEN |
| ADC1 | AIN0, AIN1 | Temp_Module2, GA_lin_SEN |
| ADC2 | AIN0 | Temp_Module1 |
| ADC3 | AIN0 | GA_Vin |
| ADC4 | AIN0 | I_LCC_SEN |

---

## 미확인 — 추가 스펙 필요

스케일링 단계(A3)에서 아래 정보가 있어야 변환식을 쓸 수 있다:

| 신호 | 필요 정보 |
|------|---------|
| Temp_Module1/2 | 온도 모듈 출력 특성 (V/°C, 오프셋, 선형 구간) |
| GA_Vin | 분압 저항비 (R_top / R_bot) 또는 전체 분압 비율 |
| I_LCC_SEN | 전류 센서 감도 (mV/A), 오프셋 전압 |
| I_COIL_SEN | 전류 센서 감도 (mV/A), 오프셋 전압 |
| GA_lin_SEN | 선형 센서 출력 스펙 (V 범위, 단위) |

AM263P ADC 파라미터(참고값 — TRM 검증 필요):
- 분해능: 12-bit (0~4095 count)
- 레퍼런스 전압: 1.8V (VREFHI) → LSB ≈ 0.44 mV
