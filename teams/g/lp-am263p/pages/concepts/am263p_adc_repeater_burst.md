---
tags: [concept, am263p, adc, repeater, sysconfig, sdk, platform]
source: AM263P MCU+ SDK v2 `source/drivers/adc/v2/adc.h`·`adc.c` 함수 시그니처 실측 + 8kw-ev-wpt-tx `feature/adc-repeater-burst` 적용 코드(`src/bsp/eta_bsp_adc.c`) 역산·실보드 검증. TRM ch07_5_controlss.md(7.5.2.6.2 Trigger Repeaters) (2026-06-29)
date: 2026-06-29
---

# AM263P ADC 트리거 리피터 버스트 — SDK 사용법 + 헤더 결함

> **AM263P 플랫폼 공통 ADC 노하우 정본.** 한 트리거에서 SOC를 N회 **백투백 버스트**시켜 PPB가 한 트리거 안에서 블록평균하는 메커니즘과 SDK v2 API 매핑. 형제 정본: [[am263p_adc_ppb_averaging]](누적 평균 — N개 트리거에 분산), [[am263p_adc_instance_allocation]] §변환시간 예산(버스트 N은 변환시간 예산에 묶임), [[am263p_adc_rti_trigger]](트리거 결선).

## 1. 리피터란 (아키텍처)

각 ADC 인스턴스는 **트리거 리피터 모듈 2개**를 가진다(TRM `ch07_5_controlss.md`:753 "Each ADC instance contains two trigger repeater modules"). 리피터는 임의의 ADC 트리거를 선택해 **(NSEL+1)개의 반복 펄스**를 만든다. 오버샘플링 모드(TRM :787–789): 초기 트리거를 통과시킨 뒤, 그 트리거를 받는 SOC가 전부 in-progress/완료되면 다음 펄스를 발행 — `(NSEL+1)`회까지 반복 → **한 ePWM 트리거 한 번으로 백투백 다중 샘플**.

**누적(PPB accumulate)과의 결정적 차이**:

| | 리피터 버스트 | PPB 누적([[am263p_adc_ppb_averaging]]) |
|---|---|---|
| N회 변환이 일어나는 시점 | **한 트리거 안에** 백투백 | **N개 트리거에 걸쳐** 분산 |
| 출력(OSINT) 레이트 | 트리거 레이트 그대로(85 kHz) | 트리거 레이트 / N (85 kHz/64 = 1.33 kHz) |
| 변환시간 예산 | **N×cadence를 한 주기 안에 소모** → 예산에 묶임 | 주기당 SOC 단발 → N과 **무관** |
| 노이즈 억제 대상 | 한 트리거 시점 좁은 창의 순간 잡음 | 트리거 주기에 걸친 저속 평균 |

따라서 리피터 버스트의 N 상한은 [[am263p_adc_instance_allocation]] §변환시간 예산의 cadence(~285 ns) × N ≤ 트리거 주기(11.76 µs)에 묶인다 → **N ≤ ~41**(단일채널), ADC1 2 SOC면 합 ≤ ~41.

## 2. SDK v2 사용법 (읽어 확인 — 실보드 동작)

체인: **EPWM0_SOCA → 리피터(오버샘플링 N) → SOC N회 백투백 → PPB(count=N, shift=LOG2) 블록평균 → OSINT 매 트리거**.

| 단계 | API / 심볼 | 값 | 출처 (SDK `source/drivers/adc/v2/`) |
|------|-----------|----|------|
| 리피터 설정 | `ADC_configureRepeater(base, repInstance, *config)` | — | `adc.c`:101–103 (⚠️ 헤더에 프로토타입 없음, §4) |
| config 구조체 | `ADC_RepeaterConfig{repMode, repTrigger, repSyncin, repCount, repPhase, repSpread}` | — | `adc.h`:797–802 |
| 오버샘플링 모드 | `ADC_REPMODE_OVERSAMPLING` | `0x0` | `adc.h`:785 |
| 반복 횟수 | `repCount` = **N − 1** ((repCount+1)개 트리거 생성) | 0~127 | doc `adc.h`:3876–3879 / assert `adc.c`:110 (`repCount <= 127` → 최대 N=128) |
| 리피터 인스턴스 | `ADC_REPINST1`(0x0) / `ADC_REPINST2`(0x1) (인스턴스당 2개) | — | `adc.h`:773–774; assert `repInstance <= 2` `adc.c`:109 |
| 리피터 트리거원 | `repTrigger = ADC_TRIGGER_EPWM0_SOCA` | `0x08` | `adc.h`:235 |
| SOC 트리거 재지정 | `ADC_setupSOC(.., ADC_TRIGGER_REPEATER1/2, ..)` | `0x7E`/`0x7F` | `adc.h`:319–320 |
| 위상 동기 비활성 | `repSyncin = ADC_SYNCIN_DISABLE` | `0x00` | `adc.h`:509 |
| 즉시 백투백 | `repPhase = repSpread = 0` | 0 | — |

**핵심 포인트**: SOC 자신의 트리거를 ePWM에서 `ADC_TRIGGER_REPEATERn`으로 **재지정**하고, 리피터가 ePWM 트리거를 받아 버스트를 만든다. 리피터 모드(오버샘플링)에서 출력 레이트는 트리거 레이트 그대로 유지된다(N 무관) — PPB 누적과 대비되는 점.

## 3. 8kw 적용 (`feature/adc-repeater-burst`, commit `2af8642`)

PPB 누적 평균(N=64, 1.33 kHz)을 **리피터 버스트 블록평균(N=16, 출력 85 kHz/인스턴스)**으로 전환·실보드 검증. (`src/bsp/eta_bsp_adc.c`)

- **N 손잡이**: `ETA_ADC_OVERSAMPLE_LOG2 = 4U` → N=2^4=16 (`src/bsp/eta_bsp_adc.h`:31, `_Static_assert ≤ 10` :33–34). `eta_bsp_adc_init()`이 `repCount=(1<<LOG2)−1` + PPB `setPPBCountLimit(2^LOG2)`/`setPPBShiftValue(LOG2)` 런타임 재기입(`eta_bsp_adc.c`:186–214, PWM TBPRD override와 동일 패턴).
- **인스턴스당 SOC j → REPINSTj** 매핑: SOC0→REPINST1/REPEATER1, SOC1→REPINST2/REPEATER2 (`eta_bsp_adc.c`:202–204). ADC1(2 SOC)은 두 리피터를 각각 씀.
- **검증 ✓**: 스코프로 OSINT 85 kHz 확인 + 6채널 라이브 갱신(0/3.3V 인가) — `feature/adc-repeater-burst` 브랜치 (main 미머지). **단 N=16은 측정 전 placeholder** — 최종 N은 노이즈 FFT 실측 후 확정(아래 빈자리).

## 4. ⚠️ SDK 헤더 결함 (플랫폼 호명)

**`ADC_configureRepeater`는 `adc.h`에 프로토타입이 없다.** `adc.h`에서 `ADC_configureRepeater`는 doc-comment 3곳(767·779·791)에만 나오고 **선언이 없음**. 심볼은 `adc.c`:101–103에 plain extern 함수로만 존재(다른 ADC API와 달리 `static inline` 아님, lib에 컴파일됨). 헤더만 include한 호출부는 **implicit-declaration 경고**를 받는다.

**우회 (8kw 채택)**: 호출부에서 로컬 `extern` 선언 (`eta_bsp_adc.c`:43–46):
```c
/* ADC_configureRepeater 프로토타입이 adc.h에 없어 로컬 선언.
 * 정의: mcu_plus_sdk .../adc/v2/adc.c:102, lib에 포함됨. */
extern void ADC_configureRepeater(uint32_t base, uint16_t repInstance,
                                  ADC_RepeaterConfig *config);
```
타 AM263P 프로젝트가 리피터를 쓸 때 동일 우회가 필요하다.

## 5. 직교성 — HW 블록평균 vs SW 이동평균 (개념, 재사용 가치)

리피터 버스트(HW)와 SW 이동평균은 **경쟁이 아니라 직교** — 서로 다른 시간 축에서 동작하므로 같이 쓴다:

| 방식 | 동작 창 | 억제 대상 | 그룹지연 | 출력 레이트 | N/M 제약 |
|------|---------|----------|---------|------------|---------|
| **리피터 버스트(HW)** | 한 트리거 시점의 좁은 창(burst 내 연속 변환) | 순간 백색·양자화 잡음 | ≈ 버스트길이/2 ≈ 수 µs | 트리거 레이트(85 kHz) 유지 | **변환시간 예산에 묶임**(N≤~41) |
| **SW 이동평균** | M개의 서로 다른 트리거 시점(M×11.76 µs) | 시간축 저역통과 | (M−1)/2 × 11.76 µs | 트리거 레이트(매 샘플 갱신) | **변환 예산 무관**(CPU·허용지연만) |

- 백색/양자화 잡음이면 둘 다 √N·√M로 억제. **스위칭 상관 피크**(85 kHz 주기성)면 평균 깊이보다 **트리거 위상/동기**가 더 큰 레버.

## 6. 사실 / 가설 / 모름 가름

- **사실 (SDK API)**: §2 표 전부 SDK 인용 확정. 오버샘플링 모드 (repCount+1) 트리거, REPINST 2개/인스턴스, 헤더 프로토타입 결함 — 전부 `adc.h`/`adc.c` 실측.
- **사실 (8kw 적용·검증)**: N=16 리피터 버스트 전환 구현·스코프 OSINT 85 kHz·6채널 라이브 검증(`feature/adc-repeater-burst`, main 미머지).
- **가설**: 직교성 표의 그룹지연·억제 특성은 신호처리 일반론 — 8kw 실신호 노이즈 스펙트럼으로 검증 안 됨.
- **빈자리 (봉합 말 것)**:
  - **최종 N 미확정** — N=16은 placeholder. 스코프 FFT로 노이즈 거동(백색 vs 스위칭 상관) 측정 후 √N 평균 유효성 판단 필요.
  - **변환시간 예산 상한 정밀도** — N 상한 ~41은 정적 산정([[am263p_adc_instance_allocation]]), tLAT 마감 보정·데이터시트 최소 S+H 미반영, 라이브 실측 미수행.

## 관련 페이지

- [[am263p_adc_ppb_averaging]] — PPB 블록/누적 평균. 누적(N개 트리거 분산)과 버스트(한 트리거 N회)의 대비가 이 페이지의 출발점.
- [[am263p_adc_instance_allocation]] §변환시간 예산 & 리피터 N 상한 — 버스트 N은 cadence×N ≤ 트리거 주기에 묶임. N=64 기각·N≤~41 생존 근거.
- [[am263p_adc_rti_trigger]] — EPWM0_SOCA 트리거 결선(리피터 트리거원).
- [[am263p_trm]] — 7.5.2.6.2 Trigger Repeaters.
