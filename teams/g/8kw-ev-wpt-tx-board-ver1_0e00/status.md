---
date: 2026-06-04
---

# 8kw-ev-wpt-tx-board-ver1_0e00 — 구현 현황

> 전략 spine은 [[roadmap]], 작업 단위 호는 [[adc]].

## 다음 작업: A0 — CCS SysConfig에서 ADC0~ADC4 인스턴스 + 채널 핀 할당

[[adc_pinmap]] 핀맵 기준으로 ADC0(AIN1), ADC1(AIN0·AIN1), ADC2(AIN0), ADC3(AIN0), ADC4(AIN0) 5개 인스턴스를 SysConfig에 추가하고 빌드 성공을 확인한다.

## 구현 현황

| 기능 | 상태 | 메모 |
|------|------|------|
| ADC SysConfig 설정 (A0) | ✗ | 5개 인스턴스, 6채널 핀 할당 |
| 단채널 polling 검증 (A1) | ✗ | ADC1_AIN0(Temp_Module2) |
| 전채널 순차 읽기 (A2) | ✗ | 6채널 UART 출력 |
| 신호별 스케일링 (A3) | ? | 센서 스펙 추가 입수 필요 |
| 실보드 교차검증 (A4) | ✗ | 멀티미터 기준값 교차 |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 추가 정보 필요 / `✗` 미구현

## 미결 사항

- **A3 블로커**: 신호별 센서 스펙 미입수 — Temp_Module1/2 출력 특성(V/°C), GA_Vin 분압비, I_LCC_SEN·I_COIL_SEN 전류 센서 감도(mV/A), GA_lin_SEN 스펙.
