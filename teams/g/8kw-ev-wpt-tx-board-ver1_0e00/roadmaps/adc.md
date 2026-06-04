---
tags: [roadmap, adc, 8kw-ev-wpt-tx-board-ver1_0e00, living-doc]
date: 2026-06-04
---

# adc — 8kW WPT TX 보드 ADC 브링업 작업 호 (A0~A4)

> 단순 기능 확인이 아닌 **eta 보드 신호 정합** 브링업 작업.
> 6채널 ADC(온도 2 + 전압 1 + 전류 2 + 선형 1)를 SysConfig 설정 → polling 검증 → 신호별 스케일링 → 실보드 교차검증 순으로 진행.
> 핀 대응표는 [[adc_pinmap]], 기능별 현황·다음 시작점은 [[status]].

상위 프로젝트 호는 [[roadmap]].

---

## 0. 한 줄 요약

LP-AM263P 5개 ADC 인스턴스(ADC0~ADC4)에 eta 보드 J3 커넥터 6채널(Temp×2, 전압×1, 전류×2, 선형×1)을 SysConfig로 연결하고, 신호별 변환식을 붙여 실측값을 검증한다.

---

## 1. 마일스톤 호 (A0~A4)

| 단계 | 범위 | 완료 기준 | 상태 |
|------|------|---------|------|
| **A0** | SysConfig ADC 설정 | ADC0~4 인스턴스 + 채널 핀 할당 완료, 빌드 성공 | ✗ |
| **A1** | 단채널 polling 검증 | ADC1_AIN0(Temp_Module2) raw count → voltage, UART 출력 확인 | ✗ |
| **A2** | 전채널 순차 읽기 | 6채널 전부 신호 레이블 붙여 UART 출력 | ✗ |
| **A3** | 신호별 스케일링 적용 | 변환식 구현 (센서 스펙 입수 후 진행) | ? |
| **A4** | 실보드 교차검증 | 멀티미터/소스 기준값으로 ADC 출력 오차 정량화 | ✗ |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 추가 정보 필요 / `✗` 미구현

---

## 2. 단계별 작업 내용

### A0 — SysConfig ADC 설정

- CCS SysConfig에서 ADC 인스턴스 5개(ADC0~ADC4) 추가
- 채널 핀 할당: [[adc_pinmap]] 표 기준
  - ADC0: AIN1 (J3.28)
  - ADC1: AIN0 (J3.24), AIN1 (J3.29)
  - ADC2: AIN0 (J3.25)
  - ADC3: AIN0 (J3.26)
  - ADC4: AIN0 (J3.27)
- 샘플링 모드: 단발(Single) polling — 트리거 없이 SW 기동
- 완료 기준: `ti_drivers_config.c` 생성, 빌드 에러 없음

### A1 — 단채널 polling 검증

- ADC1_AIN0(Temp_Module2) 한 채널로 raw count 폴링
- 변환: `voltage = (raw * 1.8) / 4095` [추정: Vref=1.8V, 12-bit, TRM 확인 필요]
- UART0(115200) 출력으로 수치 확인
- 완료 기준: 보드 통전 상태에서 전압값이 GND~Vref 범위 내 안정적 출력

### A2 — 전채널 순차 읽기

- 6채널 루프로 순차 폴링
- 출력 형식: `[ADC1_AIN0 Temp_Module2] raw=XXXX voltage=X.XXXv`
- 완료 기준: 6채널 전부 출력 확인, floating 핀은 노이즈 range 내

### A3 — 신호별 스케일링 적용

**A3은 센서 스펙 입수 후 진행.** [[adc_pinmap]] §미확인 항목 참조.

| 신호 | 변환 방향 | 필요 정보 |
|------|---------|---------|
| Temp_Module1/2 | voltage → °C | 모듈 출력 특성 (V/°C) |
| GA_Vin | voltage → 실제 전압 | 분압비 |
| I_LCC_SEN | voltage → 전류(A) | 센서 감도 mV/A, 오프셋 |
| I_COIL_SEN | voltage → 전류(A) | 센서 감도 mV/A, 오프셋 |
| GA_lin_SEN | voltage → 물리량 | 선형 센서 스펙 |

### A4 — 실보드 교차검증

- 알려진 입력(멀티미터로 측정한 기준 전압)과 ADC 출력 비교
- 목표 오차: TBD (센서 정밀도에 따라)
- 완료 기준: 전채널 오차 정량화, 스펙 범위 내 또는 원인 규명

---

## 3. 현재 위치

→ [[status]] 단일 소스.

A0 미시작 (2026-06-04).

---

## 4. 블로커 / 추가 정보 대기

- **A3 블로커**: 신호별 센서 스펙 미입수 — Temp 모듈 출력 특성, 전류 센서 감도, 분압비
- **A0 전제**: LP-AM263P CCS 프로젝트 정상 동작 상태 (SysConfig 편집 가능)

---

## 5. 환원 후보

- ADC 변환식 → `pages/concepts/adc_scaling.md` (A3 완료 후)
- SysConfig ADC 설정 노하우 → concept 페이지
