---
tags: [concept, fod, adc, 8kw-ev-wpt-tx, verification, noise]
source: 코드 repo `docs/fod_i_coil_observation.md` (branch feature/adc-noise-fft) 환원 + 회로도 [[board_schematic_v1_0e00]] 신호체인. 측정 미수행 — 관찰 절차·결정 로직.
date: 2026-07-01
---

# fod_i_coil_observation — FOD I_COIL_SEN 1차 관찰

> **목적**: FOD(Foreign Object Detection — 송/수신 코일 사이 이물 감지) 구현의 **1차 단계**. **I_COIL_SEN** 값이 *정상* vs *이물 존재*에서 어떻게 변하는지 관찰하고, 그 값을 **저노이즈로 안정적으로** 잡을 수 있는지 판별한다.
> 브랜치 **`feature/adc-noise-fft`**. 노이즈 판별 로직(백색 vs 스위칭)은 [[adc_noise_fft_probe]]와 공유, 신호체인 출처 [[board_schematic_v1_0e00]], 핀맵 [[adc_pinmap]], 장비 [[instruments]](MSOX3104T), 디버그 GPIO [[am263p_lp_debug_gpio]]. 로드맵 [[adc]] §A5.

---

## 1. 신호체인 — 왜 이 노드가 FOD 프로브로 적합한가

```
TX 코일전류 → CT(T1 PA6322, 7 mV/A) → CR3~6(CUS10S30) 쇼트키 정류·클램프
            → R30~32 + C55 2.2 µF RC 평활 → J3.28 (ADC0 AIN1)
```

- **★ ADC가 보는 노드는 85 kHz AC가 아니라 정류·평활된 느린 DC 포락선이다.** (RMS `/√2` 환산은 GUI가 정현파 가정으로 하고, 펌웨어는 raw→mV 선형만.)
  → 종전 [[adc_noise_fft_probe]] §2의 "I_COIL_SEN = 85 kHz 신호 자체라 부적합" 서술은 **CT 1차측(센싱 대상)** 기준이었고, **J3.28 노드(ADC 입력)는 DC 포락선**이라는 점을 정정.
- **FOD 가설**: 이물이 코일 결합·부하를 바꾸면 코일전류가 변하고 → 이 **DC 레벨 시프트**로 나타난다. 그래서 이 노드가 이물 판별 프로브로 적합.
- ADC0은 EPWM0 SOCA(스위칭 주기마다 TBCTR=ZERO) 트리거 → 리피터 버스트 N=16 블록평균 → **주기당 값 1개(≈85k samples/s)**. 정본 [[am263p_adc_repeater_burst]].
- **⚠️ OC 제약**: 같은 센서 노드를 `I_COIL_OC` 과전류 비교기(TLV3231)가 탭한다. 이물 실험은 **반드시 OC 임계 이하**로 유지.

---

## 2. 측정 셋업 — 2 트랙 동시 캡처

전제: **전력단 실제 스위칭 중**(PWM 활성 + HV 버스 인가). idle이면 신호/노이즈 없어 측정 무의미. GND 클립은 **DGND에만**(PRI_GND/HV 직접 프로빙 금지 — 절연 거친 0~3.3 V 저전압 노드).

### 프로브 맵 (MSOX3104T, 10:1 패시브 + 짧은 스프링팁 GND)

| CH | 신호 | 위치 | 용도 |
|----|------|------|------|
| **CH1** | **I_COIL_SEN** | **J3.28** | FOD 1차 신호. DC=레벨, AC=노이즈 (트랙 A) |
| CH3 | EPWM2_A (HS1) | J4.39 | 스코프 트리거(rising) + 스위칭 기준 시각 |
| CH4 | GPIO95 | J4.31 | ADC0 버스트-끝 마커 (주기당 펄스 1개, 상승엣지=샘플링 끝) |

- **디버그 마커**: `src/bsp/eta_bsp_adc.c`의 `#define ETA_BSP_ADC_DBG_MARK_IDX 0U` → EOC ISR이 **ADC0(I_COIL_SEN)** 버스트 완료 시 GPIO95 토글(진입 HIGH/종료 LOW). 다른 채널은 값만 바꿔 재빌드(`3U`=GA_Vin, `1U`=GA_Iin). **측정용 디버그 스캐폴딩**(측정 후 제거 대상). ⚠️ `eta_hal_gpio` DBG_LOOP도 GPIO95 사용 → 잠복 충돌, 후속 정리.

### 트랙 A — 스코프 (풀레이트 아날로그, J3.28의 풀밴드 진실)

같은 CH1 프로브를 **커플링만 토글**해 본다:
1. **DC 커플링** — 절대 레벨. 정상 baseline 기록 → 이물 투입 시 레벨 시프트(Δ) 직접 관측 = **FOD 신호 본체**.
2. **AC 커플링 + V/div 확대** — DC 빼고 그 위 리플·노이즈 확대.
3. **FFT(Math)** — Hanning, 0~500 kHz, RMS 평균, 트리거 CH3 rising. **평탄 플로어=백색** / **85·170·255 kHz 피크=스위칭 상관**.
4. **시간축** — CH3 스위칭 엣지 ↔ CH4 상승엣지 간격 = 샘플링 구간(이론 N=16 → 4.56 µs). 샘플링 창이 스위칭 과도·리플 위에 올라타는지 확인.

### 트랙 B — 디지털 (PC 모니터, 10 Hz)

- `python3 tools/gui/launch.py` → Port 선택 → Connect. **I_COIL_SEN = ch4** 라이브(V·A).
- **Start Log** → `wpt_log_<ts>.csv`(헤더 `timestamp, seq, <채널>_raw`, raw counts 10 Hz) → **Stop Log** → `scratch/`로 이동.
- 10 Hz는 UART 대역폭 한계 — **정상상태 레벨/델타엔 충분, 빠른 과도엔 부족**(풀레이트 디지털은 §4로 미룸).

---

## 3. 절차 · 판정

각 조건에서 트랙 A(스코프)와 트랙 B(CSV)를 **동시** 캡처:

1. **정상(이물 없음)**: DC 레벨·AC 노이즈·FFT·시간축 캡처 + CSV 로깅 → I_COIL_SEN_raw **평균·표준편차 σ**(노이즈 플로어, counts).
2. **이물 투입**(OC 임계 이하): 같은 항목 재캡처 → 레벨 시프트 **Δ counts**·노이즈 변화 기록.
3. **검출성 = `Δ(이물) / σ(정상 노이즈)`**:
   - 충분히 크면 → 현 센싱으로 FOD 가능, 임계 설계로.
   - 마진 부족 → 센싱 안정화 필요(아래).

### 센싱 안정화 결정 (FFT 노이즈 성격으로 가름 — [[adc_noise_fft_probe]] §4 공유)

- **백색(평탄 플로어)** → 오버샘플 N 상향(`eta_bsp_adc.h:31` `ETA_ADC_OVERSAMPLE_LOG2`). 단 버스트 N×285 ns ≤ 변환예산(~41, ADC1은 2 SOC 합).
- **스위칭 상관(피크)** → 트리거 위상 조절(N↑은 헛수고 — 위상고정→coherent→√N 무효). EPWM0 SOCA 시점(현재 TBCTR=ZERO)을 조용한 창으로, 또는 리피터 repPhase(`eta_bsp_adc.c`).

---

## 4. 미뤄둔 것 — 풀레이트 디지털 가시성

ADC는 이미 ~85k samples/s를 만들지만 텔레메트리는 10 Hz만 떠간다. PC에서 풀레이트를 보려면(연속 UART 스트리밍은 대역폭상 불가) **온타깃 버스트 캡처 + 1회 UART 덤프**(예: 연속 2048 샘플 일괄 송신)가 필요. 1차 관찰은 스코프(아날로그 풀레이트)+10 Hz(정상상태 레벨)로 충분하므로 **다음 작업으로 미룸**. (런타임 FOD 로직을 타깃에서 돌리면 칩 내부에서 풀레이트를 공짜로 쓰므로 PC 풀레이트는 개발·검증용.)

---

## 5. 환원 후보 (측정 후)

- 스코프 캡처·CSV → `raw/adc_noise_fft/`(또는 `scratch/`) 보관, 이 페이지에 정상 레벨·σ·이물 Δ·FFT 백색/상관·CH4 정렬 결과 환원.
- 위상을 택했다면 EPWM0 SOC 트리거 시점 변경 구현은 [[am263p_adc_repeater_burst]]·[[am263p_adc_rti_trigger]] §5에 환원.
- 검출성(Δ/σ) 결론 → FOD 임계 설계 or 풀레이트 디지털(§4) 착수 판단.
