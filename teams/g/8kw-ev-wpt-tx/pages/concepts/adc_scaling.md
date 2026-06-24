---
tags: [concept, adc, 8kw-ev-wpt-tx, scaling]
source: 구현 역산 + 사용자 확인 (2026-06-24, commit 7335418)
date: 2026-06-24
---

# adc_scaling — 8kW WPT TX ADC 물리량 변환식

> ADC raw count → 물리량(A/V/°C) 변환식 모음.
> 아키텍처: **변환은 호스트 GUI(`tools/gui/gui.py`)에서 수행, MCU는 raw/mV만 전송**.
> 핀맵·채널 배치는 [[adc_pinmap]], 작업 호는 [[adc]], GUI 구조는 [[pc_monitor_gui]].

---

## 아키텍처 결정 — GUI 단일 소스

**물리량 변환은 `tools/gui/gui.py`의 `PHYSICAL_COEFF` 테이블이 단일 소스.**

```python
physical = scale * adc_v + offset
```

- MCU(`eta_adc.c`)는 `(raw * 3300) / 4095` 정수 mV만 계산해 UART 패킷으로 전송.
- R·CAL·CT 상수는 `gui.py` named 상수로 관리 — 편집 후 재실행으로 적용.
- MCU 이관은 보류 — gui.py에 식·도출·검증 데이터포인트를 MCU 이관 대비 주석으로 보존.

---

## I_COIL_SEN (ch4) — 코일 전류 [A] ✓ 검증완료

### 물리식

```
I = (ADC_V + CAL) × (R33+R34)/R34 × CT_TURNS / (R30‖R31‖R32) / √2
```

**부품 역할:**
- `R30‖R31‖R32`: CT 2차 측 버든저항 3개 병렬 — 전류→전압 변환
- `CT_TURNS`: CT 2차 턴수 — 1차 전류 복원에 곱함
- `R33`, `R34`: 신호 감쇠 복원 분압기
- `CAL`: ADC 입력 오프셋 보정 전압

### 선형 접힘

```
I = SCALE × ADC_V + OFFSET,  OFFSET = SCALE × CAL
```

### 현재 파라미터 (2026-06-24 확정)

| 상수 | 값 | 비고 |
|------|----|------|
| R30 = R31 = R32 | 47 Ω | 버든저항 3병렬 → 15.67 Ω |
| R33 | 0 Ω | (인입 없음) |
| R34 | 1200 Ω | 분압 복원 |
| CAL | 0.62 V | ADC 입력 오프셋 |
| CT_TURNS | 150 | CT 2차 턴수 |
| **SCALE** | **≈6.770 A/V** | |
| **OFFSET** | **≈4.198 A** | = SCALE × CAL |

### 검증 데이터포인트

| ADC_V | 계산값 | 기대값 | 판정 |
|-------|--------|--------|------|
| 2.64 V | 22.07 A | 22.1 A | ✓ 일치 |

커밋: `7335418` (feat: I_COIL_SEN ADC raw→코일 전류 변환), branch `feature/adc-calculation`.

---

## I_LCC_SEN (ch3) — LCC 전류 [A] ✗ 미교정

placeholder — 센서 스펙 미입수.

---

## GA_Iin_SEN (ch5) — 게이트 드라이버 입력 전류 [A] ✗ 미교정

placeholder — 다음 세션 진행 예정.

---

## GA_Vin (ch2) — 게이트 드라이버 입력 전압 [V] ✗ 미교정

placeholder — 분압비 미입수.

---

## Temp_Module1/2 (ch0, ch1) — 온도 [°C] ✗ 미교정

placeholder — 모듈 출력 특성(V/°C) 미입수.
