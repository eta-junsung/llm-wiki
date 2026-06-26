---
tags: [concept, am263p, adc, ppb, oversampling, controlss, 정본]
source: AM263P TRM ch07_5_controlss.md(ControlSS ADC PPB) + MCU+ SDK v2 adc.h(`source/drivers/adc/v2/adc.h`) 함수 시그니처 실측 + 8kw-ev-wpt-tx PPB 적용 코드 역산 (feature/adc-trigger-epwm0 4cffbe1·532e0eb → main PR #6 `d673e74`, HW 검증 후 N=64 확정) (2026-06-26)
date: 2026-06-26
---

# am263p_adc_ppb_averaging — AM263P ControlSS ADC PPB 하드웨어 오버샘플 평균

> **AM263P 플랫폼 공통 ADC 노하우 정본.** PPB(Post-Processing Block)로 오버샘플 변환 평균을 **CPU 개입 없이** 자동 계산하는 메커니즘과 SDK v2 API 매핑. SW 이동평균 대비 RAM 버퍼·루프 연산 불필요 — 제어루프에 논블로킹.
> 형제 정본: [[am263p_adc_rti_trigger]](트리거 결선·OSINT ISR — 파일명은 `am263p_adc_rti_trigger.md`), [[am263p_adc_instance_allocation]](인스턴스/채널 배치·변환시간 예산). 8kw 적용 호 [[adc]], 핀맵 [[adc_pinmap]].

---

## 1. 핵심 — 2의 거듭제곱일 때만 HW 자동 평균

PPB는 오버샘플 변환의 합/최소/최대/카운트를 매 변환마다 자동 누적하고, **sample count가 2의 거듭제곱(최대 1024=2^10)일 때** CPU 없이 평균까지 자동 계산한다 (TRM `ch07_5_controlss.md`:1582, :1771).

**평균 = 우측 비트시프트**이기 때문이다 — `ADCPPBxCONFIG2.SHIFT = n`이면 PPB가 `PSUM ÷ 2^n`을 `ADCPPBxSUM`에 적재한다 (TRM :1771). 2의 거듭제곱이 아니면 시프트로 나눌 수 없어 **CPU가 `SUM÷COUNT`를 직접 나눠야** 한다 (TRM :1773). ⇒ **HW 자동 평균을 쓰려면 N을 2의 거듭제곱으로 고정**하는 것이 핵심 제약.

---

## 2. 동작 원리 (TRM §7.5.2.14.5.1, :1759–1773)

- **누적**: 매 ADC 변환 종료 시 PPB가 `ADCPPBxPSUM`(부분합)·`ADCPPBxPMIN`·`ADCPPBxPMAX`를 갱신하고 `ADCPPBxPCOUNT`를 1 증가 (TRM :1759).
- **배치 완료 조건**: `ADCPPBxPCOUNT == ADCPPBxLIMIT` **또는** HW/SW sync 이벤트 (TRM :1761). 완료 시:
  1. partial → final 레지스터(`ADCPPBxSUM`/`MIN`/`MAX`)로 load (TRM :1763).
  2. `ADCPPBxPCOUNT` → `ADCPPBxCOUNT`로 load.
  3. partial 레지스터 전부 0으로 reset.
  4. **`OSINTx` 오버샘플링 인터럽트 펄스 발생** → `ADCINTSEL*` 설정 시 CPU 인터럽트 트리거 (TRM :1767).
- **자동 평균**: `ADCPPBxLIMIT = 2^n` + `ADCPPBxCONFIG2.SHIFT = n` ⇒ `ADCPPBxSUM = PSUM ÷ 2^n` = 평균(0~4095 범위 유지) (TRM :1771).
- **Outlier rejection**(선택적 SW 보조): `(SUM − MAX − MIN)/(COUNT − 2)`를 ISR에서 계산 — HW 자동 평균과 별개.

---

## 3. SDK v2 API 매핑 (`source/drivers/adc/v2/adc.h`)

| 역할 | 함수 | adc.h 라인 | 비고 |
|------|------|-----------|------|
| PPB ↔ SOC 매핑 | `ADC_setupPPB(base, ppbNumber, socNumber)` | :1746 | 어느 SOC를 후처리할지 결선 |
| 누적 개수(배치 크기) | `ADC_setPPBCountLimit(base, ppbNumber, limit)` | :2024 | `ADCPPBxLIMIT` = N |
| 평균 시프트 | `ADC_setPPBShiftValue(base, ppbNumber, shiftVal)` | :2310 | `SHIFT` = n. **내부 `DebugP_assert(shiftVal <= 10U)` (:2317)** → N ≤ 1024 |
| 평균값 읽기 | `ADC_readPPBSum(resultBase, ppbNumber)` | :2504 | shift 적용된 `ADCPPBxSUM`(=평균, 0~4095) 반환 |
| OSINT 발생 이벤트 선택 | `ADC_selectPPBOSINTSource(base, ppbNumber, osIntSrc)` | :2418 | ★아래 혼동주의 |
| ADC INT를 OSINT에 결선 | `ADC_setInterruptSource(base, intNum, ADC_INT_TRIGGER_OSINTx)` | enum :613–616 | ISR을 EOC가 아니라 평균완료에 건다 |

### ★혼동주의 — `ADC_selectPPBOSINTSource`는 라우팅이 아니다

이 함수는 "PPB → OSINT 라우팅"이 **아니다**. `PPBn → OSINTn`은 **고정 매핑**이다. 이 함수가 고르는 것은 **그 PPB 인터럽트의 *발생 이벤트***다 — `ADCPPBxCONFIG2.OSINTSEL` 비트:

- `ADC_PPB_OS_INT_1 = 0` → **PCount**(배치 카운트 도달=평균 완료)가 인터럽트 발생 (adc.h:571).
- `ADC_PPB_OS_INT_2 = 1` → **PCount/Sync**(sync 이벤트 포함)가 발생 (adc.h:572).

**평균완료 인터럽트엔 기본값 `0`(PCount)이 맞다.**

### ISR이 EOC가 아니라 평균완료(OSINT)에 뜬다

`PPBn → OSINTn` 고정 매핑 위에서, ADC 인터럽트를 `ADC_setInterruptSource(base, intNum, ADC_INT_TRIGGER_OSINTx)`(enum `ADC_INT_TRIGGER_OSINT1=16` … adc.h:613–616)로 OSINT에 걸면, ISR이 **매 변환(EOC)이 아니라 평균완료에만** 뜬다. 8kw에서 트리거 85.032 kHz·**N=64**(HW 검증 확정) ⇒ ISR 레이트 = 85032/64 ≈ **1.33 kHz**.

---

## 4. lockstep — 한 트리거를 공유하는 여러 SOC

한 트리거 이벤트를 공유하는 여러 SOC는 그 이벤트에 **우선순위 순서로 모두 변환**(lockstep)된다. 따라서 각 SOC에 붙은 PPB가 **같은 트리거에 맞춰 같이 누적·완료**된다. 이것이 8kw에서 **ADC1 SOC0+SOC1을 한 EPWM0_SOCA 트리거로 동시 누적**하는 근거다 — 두 PPB(PPB1↔SOC0, PPB2↔SOC1)가 같은 배치 경계를 가지므로, SOC1(나중 완료)의 OSINT2를 INT1 소스로 잡아 한 ISR에서 두 채널을 coherent하게 읽는다.

---

## 5. 8kw 적용 (main, PR #6 `d673e74` — N=64 HW 확정)

- **6채널 전부 PPB HW 평균**(feature `4cffbe1` → main `d673e74`). repeater 안 씀(근거 [[am263p_adc_rti_trigger]] §5·[[adc]] A3.5). SysConfig `example.syscfg`가 각 ADC에 PPB 설정(`AccumulationLimit`/`Rightshift`는 syscfg 기본값이고 런타임이 N으로 덮음):
  - `ppb1SOCNumber=ADC_SOC_NUMBER0`, `ppb1SelectOSINTSource=ADC_PPB_OS_INT_1` (example.syscfg:77,80).
  - ADC1만 PPB2 추가(SOC1, OSINT2 → INT1 소스: `interrupt1SOCSource=ADC_INT_TRIGGER_OSINT2`, example.syscfg:75,82–85).
- **N 단일 손잡이(feature `532e0eb`)**: `src/bsp/eta_bsp_adc.h:28` `ETA_ADC_OVERSAMPLE_LOG2 (6U)` 매크로 하나로 **N=2^6=64**(HW 검증 후 32→64로 확정, main `d673e74`). `eta_bsp_adc_init()`이 전 PPB에 `ADC_setPPBCountLimit(.., 1<<LOG2)`·`ADC_setPPBShiftValue(.., LOG2)`를 **런타임 재기입**(eta_bsp_adc.c:174–179) — SysConfig 기본값을 덮어쓰는 PWM TBPRD override와 동일 패턴. 헤더 `_Static_assert(LOG2 <= 10)`(eta_bsp_adc.h:30)로 N≤1024 컴파일 가드.
- **튜닝**: `ETA_ADC_OVERSAMPLE_LOG2` 한 줄 수정(6→64, 5→32, 7→128, ≤10) 후 재빌드-flash. GUI 통합 없음(코드 직접 수정).

---

## 6. 사실 / 가설 / 모름 가름

- **사실 (아키텍처·API)**: 2의 거듭제곱일 때만 비트시프트로 HW 자동 평균(최대 1024); 누적→limit 도달 시 final load + OSINT; PPBn↔OSINTn 고정; `selectPPBOSINTSource`는 OSINTSEL 이벤트 선택(라우팅 아님). 전부 TRM/adc.h 인용 확정.
- **사실 (HW 검증 — 2026-06-26)**: 실보드 노이즈 측정으로 **N=64 확정**(√64=÷8). ~~△ 노이즈 감소량 미측정~~ 닫힘 — main PR #6 `d673e74`. N을 32에서 64로 올린 근거가 이 실측.
- **빈자리**: outlier-rejection 경로 미구현(현재 단순 평균만). PPB sync(EPWM syncout) 정렬 미사용(EPWM0_SOCA 트리거 직결).

---

## 관련 페이지

- [[am263p_adc_rti_trigger]] — ADC SOC 트리거(RTI/EPWM) 결선 + OSINT ISR. PPB 인터럽트를 어느 트리거에 동기화하는가. (파일명 `am263p_adc_rti_trigger.md`)
- [[am263p_adc_instance_allocation]] — 인스턴스/채널 배치 + 변환시간 예산(PPB 누적이 트리거 주기 예산을 넘지 않는지).
- [[adc]] — 8kw ADC 작업 호 A3.5(PPB HW 평균 적용).
- [[am263p_trm]] — ControlSS ADC PPB 레지스터 정의 출처(`ch07_5_controlss.md` §7.5.2.14.5).
