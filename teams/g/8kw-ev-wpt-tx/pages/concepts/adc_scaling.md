---
tags: [concept, adc, 8kw-ev-wpt-tx, scaling]
source: 구현 역산 + 사용자 확인 (2026-06-24, commit 7335418 + A3 전채널 완료)
date: 2026-06-24
---

# adc_scaling — 8kW WPT TX ADC 물리량 변환식

> ADC raw count → 물리량(A/V/°C) 변환식 모음.
> 아키텍처: **변환은 호스트 GUI(`tools/gui/gui.py`)에서 수행, MCU는 raw/mV만 전송**.
> 핀맵·채널 배치는 [[adc_pinmap]], 작업 호는 [[adc]], GUI 구조는 [[pc_monitor_gui]].

---

## ADC 공통 파라미터

| 항목 | 값 |
|------|-----|
| 분해능 | 12-bit, 0~4095 count |
| Vref | **3.3V 확정** (`ADC_VREF_MV = 3300`) |
| 1 LSB | ≈ 0.806 mV |
| raw→mV | `mv = raw * 3300 // 4095` (정수 내림, MCU·GUI 공용) |
| mV→adc_v | `adc_v = mv / 1000.0` (full-precision) |

---

## 아키텍처 — GUI `PHYSICAL_COEFF` 단일 소스

**물리량 변환은 `tools/gui/gui.py`의 `PHYSICAL_COEFF` 테이블이 단일 소스.**

```python
# 각 채널: (scale, offset, unit)  또는  (callable, None, unit)
PHYSICAL_COEFF = [
    (temp_ntc, None, "°C"),   # ch0 Temp_Module2
    (temp_ntc, None, "°C"),   # ch1 Temp_Module1
    (353.39,   0.0,  "V"),    # ch2 GA_Vin
    (None,     None, "A"),    # ch3 I_LCC_SEN  (미교정)
    (6.770,    4.198,"A"),    # ch4 I_COIL_SEN
    (10.0,    -3.3,  "A"),    # ch5 GA_Iin_SEN
]

def calc_physical(ch, adc_v):
    coeff = PHYSICAL_COEFF[ch]
    fn = coeff[0]
    if fn is None:
        return None                      # 미교정 채널
    if callable(fn):
        return fn(adc_v)                 # 비선형(NTC)
    scale, offset, _ = coeff
    return scale * adc_v + offset        # 선형
```

**설계 결정:**
- **선형 채널**: 보드 물리식을 `scale·adc_v + offset`으로 접어 상수만 주입.
- **비선형(NTC 온도)**: 선형 슬롯으로 표현 불가 → `PHYSICAL_COEFF`가 callable을 받도록 `calc_physical` 후방호환 확장. 동일 회로 채널(Temp_Module1/2)은 함수 1개 공유.
- **도메인 가드**: 정의역 밖(예: NTC 출력 범위 초과)이면 `"— unit"` 표시.
- **보드 상수 명명 규칙**: 매직넘버 직타 금지. `ADC_VREF_MV`, `SQRT_2`, CT/저항 상수 모두 named 상수. `ADC_VREF_MV`에서 `adc_vref = ADC_VREF_MV / 1000.0`으로 파생해 3.3V 중복 회피.
- **MCU 이관 보류**: 현재 변환은 GUI에서만 수행, MCU(`eta_adc.c`)는 raw/mV만 계산·송신. 이관 대비로 물리식·도출 과정·검증 데이터포인트를 `gui.py` 주석으로 보존.

---

## ch0/ch1 Temp_Module2/1 — 온도 [°C] ✓ 검증완료

### 회로 — NTC 저항 분압기

```
Vs (3.3V) ─── NTC(T) ─── adc_v ─── R15 ─── GND
```

### 순변환 (T → adc_v, 설계 확인용)

```
adc_v = Vs × R15 / (NTC(T) + R15)
NTC(T) = NTC_R25 × exp(B × (1/(T + 273.15) − 1/298.15))
```

### 역변환 (adc_v → T, GUI 실제 적용)

```
NTC_R  = Vs × R15 / adc_v − R15
T(°C)  = 1 / (ln(NTC_R / NTC_R25) / B + 1/298.15) − 273.15
```

### 파라미터 (2026-06-24 확정)

| 상수 | 값 | 비고 |
|------|----|------|
| R15 | 3000 Ω | 분압 풀다운 |
| NTC_R25 | 5000 Ω | 25°C 기준 저항 |
| B | 3433 | NTC Beta 계수 |
| Vs | 3.3 V | = `ADC_VREF_MV/1000` |

Temp_Module1·2 동일 회로 → `temp_ntc(adc_v)` 함수 공유.

### 검증 데이터포인트

| adc_v | 계산 온도 | 비고 |
|-------|---------|------|
| 1.2375 V | 25.0 °C | 25°C일 때 NTC=R25=5kΩ, Vout=3.3×3k/8k=1.2375 수식 일치 |
| 0.8 V | 9.57 °C | |

---

## ch2 GA_Vin — 게이트 드라이버 입력 전압 [V] ✓ 검증완료

### 회로 — 저항분압 + 클리핑게인

```
GA_Vin ─── R53~R57(1MΩ×5 직렬) ─── Vclip(2.56V 클리핑) ─── R58(11kΩ) ─── GND
                                              ↓
                                           adc_v
```

- Vclipping 회로: 실제 입력 전압이 클리핑 전압(2.56V) 기준으로 스케일되어 ADC full-scale(3.3V)에 매핑.
- `Gain = ADC_VREF / Vclipping = 3.3 / 2.56 ≈ 1.289`

### 변환식

```
GA_Vin = adc_v / Gain / div_ratio = adc_v × SCALE
div_ratio = R58 / (R53+R54+R55+R56+R57+R58) = 11k / (5×1M + 11k) ≈ 0.002196
SCALE = 1 / (Gain × div_ratio)
```

### 파라미터 (2026-06-24 확정)

| 상수 | 값 |
|------|----|
| R53~R57 | 1 MΩ (각각, 5개 직렬) |
| R58 | 11 kΩ |
| Vclipping | 2.56 V |
| Gain | ≈ 1.289 |
| div_ratio | ≈ 0.002196 |
| **SCALE** | **≈ 353.39 V/V** |

### 검증 데이터포인트

| 기대 GA_Vin | 예상 adc_v | 비고 |
|------------|-----------|------|
| 412 V | ≈ 1.166 V | 412 / 353.39 ≈ 1.166 |

---

## ch3 I_LCC_SEN — LCC 전류 [A] ✗ 미교정

센서 스펙(감도, 오프셋) 미입수. placeholder `— A`.

---

## ch4 I_COIL_SEN — 코일 전류 [A] ✓ 검증완료

### 회로 — CT + 버든저항 분압

```
I = (ADC_V + CAL) × (R33+R34)/R34 × CT_TURNS / (R30‖R31‖R32) / √2
```

- `R30‖R31‖R32`: CT 2차 측 버든저항 3병렬 → 전류→전압 변환
- `CT_TURNS`: CT 2차 턴수 → 1차 전류 복원에 곱함
- `R33`, `R34`: 신호 감쇠 복원 분압기
- `CAL`: ADC 입력 오프셋 보정 전압

선형 접힘: `I = SCALE × ADC_V + OFFSET`, `OFFSET = SCALE × CAL`

### 파라미터 (2026-06-24 확정)

| 상수 | 값 |
|------|----|
| R30 = R31 = R32 | 47 Ω (3병렬 → 15.67 Ω) |
| R33 | 0 Ω |
| R34 | 1200 Ω |
| CAL | 0.62 V |
| CT_TURNS | 150 |
| **SCALE** | **≈ 6.770 A/V** |
| **OFFSET** | **≈ 4.198 A** |

### 검증 데이터포인트

| adc_v | 계산값 | 기대값 | 판정 |
|-------|--------|--------|------|
| 2.64 V | 22.07 A | 22.1 A | ✓ |

커밋: `7335418`, branch `feature/adc-calculation`.

---

## ch5 GA_Iin_SEN — 게이트 드라이버 입력 전류 [A] ✓ 검증완료

### 회로 — Hall-effect 전류 센서

```
I = (adc_v − V_zero) / Sensitivity
```

- `V_zero`: 센서 zero-current 출력 전압 (ADC Vref와 무관한 센서 고유 바이어스)
- `Sensitivity`: V/A 감도

선형 접힘: `I = SCALE × adc_v + OFFSET`

### 파라미터 (2026-06-24 확정)

| 상수 | 값 |
|------|----|
| Sensitivity | 0.1 V/A |
| V_zero | 0.33 V (센서 zero-current 출력) |
| **SCALE** | **10 A/V** (= 1/Sensitivity) |
| **OFFSET** | **−3.3 A** (= −V_zero/Sensitivity) |

### 검증 데이터포인트

| adc_v | 계산값 | 비고 |
|-------|--------|------|
| 2.13 V | 17.99 A | (2.13 − 0.33) / 0.1 = 18.0 |

---

## 검증 방법 — ADC 직접 전압 주입

1. LaunchPad ADC 입력 핀에 정밀 전압 주입(0~3.3V 범위, **초과 금지**).
2. GUI `ADC(V)` / `Physical` 컬럼 표시값이 아래 양자화 체인 기대값과 일치하는지 확인:
   ```
   주입V → raw (ADC 변환) → mv = raw*3300//4095 → adc_v = mv/1000.0 → 물리량
   ```
3. 1 LSB ≈ 0.806 mV이므로 표시 마지막 자리 **±1~2 LSB 흔들림은 양자화 오차**(계산 오류 아님).
4. 표시 정밀도: `ADC(V)`·`Physical` 모두 소수점 **3자리** (계산은 full-precision, 표시 포맷만).
