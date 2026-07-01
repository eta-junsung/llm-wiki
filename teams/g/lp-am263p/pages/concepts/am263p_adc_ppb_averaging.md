---
tags: [concept, am263p, adc, ppb, oversampling, controlss, 정본]
source: AM263P TRM ch07_5_controlss.md(ControlSS ADC PPB §7.5.2.14.5.1) + MCU+ SDK v2 adc.h(`source/drivers/adc/v2/adc.h`)·cslr_adc.h·cslr_adc_result.h 레지스터 실측 + 8kw-ev-wpt-tx PPB 적용 코드 역산 (feature/adc-trigger-epwm0 4cffbe1·532e0eb → main PR #6 `d673e74`, HW N=64 확정) + PR#11 `2c4ff85` 리피터 버스트 전환 (2026-06-29) + N=16 버스트 OSINT 레이트 Saleae 실측 충족(§6, 트리거당 1회 85 kHz, ADC0) — [[adc_repeater_burst_timing]] (2026-06-30)
date: 2026-06-30
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
- **★ N 정본: 런타임 매크로가 SysConfig 주석보다 우선** — SysConfig 재생성 주석에 "32회" 등 이전 값이 남아 있는 경우가 있으나, `ETA_ADC_OVERSAMPLE_LOG2=6`(N=64) 런타임 재기입이 정본. 주석이 갱신되지 않아도 동작은 런타임 값 기준.
- **튜닝**: `ETA_ADC_OVERSAMPLE_LOG2` 한 줄 수정(6→64, 5→32, 7→128, ≤10) 후 재빌드-flash. GUI 통합 없음(코드 직접 수정).
- **빈자리 — ADC1 ISR 발화 횟수**: ADC1은 PPB 2개(SOC0→PPB1, SOC1→PPB2). 현재 `interrupt1SOCSource=ADC_INT_TRIGGER_OSINT2`(example.syscfg:75)로 OSINT2만 INT1 소스 — 배치당 ISR 1회 추정. **OSINT1(PPB1)이 별도 인터럽트로도 올라오는지 실측으로 확정 필요**. (2026-06-30 Saleae 측정은 `ETA_BSP_ADC_DBG_MARK_IDX=0U`로 **ADC0 단독 마킹** — ADC0는 "트리거당 OSINT 1회" 확정([[adc_repeater_burst_timing]]), **ADC1은 여전히 미확정**.)

> **후속 (2026-06-29, PR#11 main `2c4ff85`)**: 8kw에서 N=64 분산 누적(ISR 1.33 kHz) → **리피터 버스트 블록평균 N=16**(ISR 85 kHz)으로 전환. PPB 레지스터 구조(LIMIT/SHIFT/SUM/COUNT)는 동일하나 리피터가 한 트리거당 N회 백투백 변환을 공급. 상세 [[am263p_adc_repeater_burst]] §3.

---

## 6. 레지스터 주소·필드 (SDK cslr, ADC2 예)

근거: `hw_include/am263px/cslr_soc_baseaddress.h` + `source/drivers/adc/v2/cslr_adc.h` + `source/drivers/adc/v2/cslr_adc_result.h` 실측.

**베이스 주소 (ADC2)**

| 도메인 | 심볼 | 값 |
|--------|------|---|
| ctrl | `CSL_CONTROLSS_ADC2_U_BASE` | `0x502C2000` |
| result | `CSL_CONTROLSS_ADC2_RESULT_U_BASE` | `0x50102000` |

ADC별 base는 `.._ADC0/1/2/3/4_..` 심볼로 구분 (`hw_include/am263px/cslr_soc_baseaddress.h`).

**리피터 설정 레지스터 (ctrl 도메인)**

| 레지스터 | ctrl offset | 필드 | 비트 | 역할 | cslr_adc.h 라인 |
|----------|-------------|------|------|------|----------------|
| REP1N | `+0x104` | NSEL[6:0] | [6:0] | N−1 (최대 127, N≤128) | 293, 2969–2982 |
| REP1N | `+0x104` | NCOUNT[6:0] | [22:16] | 라이브 반복 카운터 (RO) | 293, 2969–2982 |

**PPB 설정 레지스터 (ctrl 도메인, PPB1 예)**

| 레지스터 | ctrl offset | 필드 | 비트 | 역할 | cslr_adc.h 라인 |
|----------|-------------|------|------|------|----------------|
| ADCPPB1LIMIT | `+0x140` | LIMIT[9:0] | [9:0] | 배치 크기 N | 302, 3175 |
| ADCPPB1CONFIG2 | `+0x148` | SHIFT[3:0] | [3:0] | 우측 시프트 log2(N) | 304, 3203 |

**PPB 결과 레지스터 (result 도메인, PPB1 예)**

| 레지스터 | result offset | 필드 | 비트 | 역할 | cslr_adc_result.h 라인 |
|----------|---------------|------|------|------|----------------------|
| ADCPPB1SUM | `+0x30` | SUM[23:0] | [23:0] | SHIFT 적용 평균값 (=PSUM>>SHIFT) | 136, 366 |
| ADCPPB1SUM | `+0x30` | SIGN[7:0] | [31:24] | 부호 확장 | 136, 366 |
| ADCPPB1COUNT | `+0x34` | COUNT[9:0] | [9:0] | HW 적재 누적 변환수 | 137, 380 |

**SDK API 요약**

| 함수 | 역할 | 헤더/소스 |
|------|------|---------|
| `ADC_readPPBCount(resultBase, ppbNumber)` | ADCPPB1COUNT 읽기 | `adc/v2/adc.h` |
| `ADC_readPPBSum(resultBase, ppbNumber)` | ADCPPB1SUM (평균값) 읽기 | `adc/v2/adc.h` |
| `ADC_setPPBShiftValue(base, ppbNumber, shiftVal)` | SHIFT 설정 | `adc/v2/adc.h` |
| `ADC_setPPBCountLimit(base, ppbNumber, limit)` | LIMIT(=N) 설정 | `adc/v2/adc.h` |
| `ADC_configureRepeater(base, repInstance, *config)` | REP1N 포함 리피터 설정 (헤더 결함 있음 — [[am263p_adc_repeater_burst]] §4) | `adc/v2/adc.c` |

**재사용 노하우 (PPB SUM/COUNT 해석)**

- `ADCPPBxSUM = PSUM >> SHIFT`. 적재 후 PSUM은 0 리셋 → shift 전 원시합 레지스터 없음. **원시합 읽으려면 SHIFT=0**으로 재설정 필요(SUM = PSUM 그대로).
- `ADCPPBxCOUNT`는 HW 적재 누적 변환수. 정상 상태에선 항상 LIMIT(=N)과 같음 → "누적 횟수 N" 증거이지 "트리거당 N번 변환" 단독 증거는 아님. 후자 확인엔 **OSINT 레이트 = 트리거 레이트(85 kHz) 동시 확인** 필요.
  - ✅ **이 동시 확인 충족됨 (2026-06-30, ADC0)**: Saleae로 OSINT(GPIO95 ISR 마커) = **85.03 kHz**, 스위칭 주기당 **정확히 1회**(12,260/12,260) 실측 → 분산 누적(85k/16≈5.3 kHz)이 아니라 **한 트리거당 N회 버스트**임이 실증. 출처·방법 [[adc_repeater_burst_timing]]. (단 이는 리피터 버스트 모드 — 현 8kw 채택 — 의 N=16 확인이고, PPB *누적* 모드는 정의상 OSINT=85k/N.)

---

## 7. 제안 검증법 — CCS 레지스터 readback (미수행)

> ⚠️ 이 절은 **미실행 제안**이다 — 스코프 없이 CCS 레지스터만으로 리피터 N을 확인하는 방법. 측정값 주장 없음.
> **현황 분리 (2026-06-30)**: 스코프 실측으로 **OSINT 레이트·버스트 타이밍은 확인됨**([[adc_repeater_burst_timing]] — 트리거당 OSINT 1회, 버스트 3.12 µs). 그러나 **레지스터 필드값(NSEL/LIMIT/SHIFT/COUNT) readback은 여전히 미수행** — 아래 절차는 그대로 미실행 제안.

스코프 없이 CCS Memory Browser로 ADC2 레지스터를 readback해 리피터 N=16 설정을 확인하는 절차(8kw 기준, `ETA_ADC_OVERSAMPLE_LOG2=4`):

1. **정적 readback** — COUNT, NSEL, LIMIT, SHIFT 읽기:
   - `ADC2 result+0x34`(ADCPPB1COUNT): COUNT[9:0] = 16 기대.
   - `ADC2 ctrl+0x104`(REP1N): NSEL[6:0] = 15 (=N−1) 기대.
   - `ADC2 ctrl+0x140`(ADCPPB1LIMIT): LIMIT[9:0] = 16 기대.
   - `ADC2 ctrl+0x148`(ADCPPB1CONFIG2): SHIFT[3:0] = 4 기대.
   → 네 필드 정합 = "리피터+PPB가 매크로 N에 따라 설정됨" 확인.

2. **차분 확인** — `ETA_ADC_OVERSAMPLE_LOG2` 4→3으로 변경 후 재빌드·flash:
   - 기대: NSEL=7, LIMIT=8, SHIFT=3, COUNT=8로 동반 추종.
   - 추종 확인 시 "매크로 N이 리피터+PPB 모두에 반영됨" 확정.
   - 검증 후 LOG2=4로 원복.

3. **(보강) SHIFT 라이브 poke** (CCS Memory Browser 직접 write):
   - ADCPPB1CONFIG2.SHIFT를 0으로 write → SUM이 SHIFT=4 대비 ≈16배 커지면(안정 DC 조건) "PSUM이 16샘플 누적임" 간접 확인.
   - ⚠️ live 시스템 register write — 게이트드라이버 출력 정지 상태에서 수행. 끝나면 SHIFT=4 원복.

---

## 8. 사실 / 가설 / 모름 가름

- **사실 (아키텍처·API)**: 2의 거듭제곱일 때만 비트시프트로 HW 자동 평균(최대 1024); 누적→limit 도달 시 final load + OSINT; PPBn↔OSINTn 고정; `selectPPBOSINTSource`는 OSINTSEL 이벤트 선택(라우팅 아님). 전부 TRM/adc.h 인용 확정. 레지스터 주소(ADC2 base 0x502C2000/0x50102000, REP1N/LIMIT/SHIFT/SUM/COUNT offset)는 cslr 실측 — §6 표 참조.
- **사실 (HW 검증 — 2026-06-26)**: 실보드 노이즈 측정으로 **N=64 확정**(√64=÷8). main PR #6 `d673e74`. N을 32에서 64로 올린 근거가 이 실측. → **후속 (2026-06-29)**: PR#11로 N=64 분산 누적이 N=16 리피터 버스트 블록평균으로 전환됨([[am263p_adc_repeater_burst]] §3).
- **사실 (실측 — 2026-06-30, ADC0)**: 리피터 버스트 N=16 모드에서 OSINT = 85.03 kHz, 트리거당 정확히 1회([[adc_repeater_burst_timing]]). "트리거당 N회 버스트" 실증.
- **빈자리**: outlier-rejection 경로 미구현(현재 단순 평균만). PPB sync(EPWM syncout) 정렬 미사용. §7 레지스터 필드값 readback 미수행(OSINT 레이트·버스트 타이밍은 스코프로 확인됨). ADC1 OSINT 발화 횟수 미확정(§5).

---

## 관련 페이지

- [[am263p_adc_rti_trigger]] — ADC SOC 트리거(RTI/EPWM) 결선 + OSINT ISR. PPB 인터럽트를 어느 트리거에 동기화하는가. (파일명 `am263p_adc_rti_trigger.md`)
- [[am263p_adc_instance_allocation]] — 인스턴스/채널 배치 + 변환시간 예산(PPB 누적이 트리거 주기 예산을 넘지 않는지).
- [[am263p_adc_repeater_burst]] — **누적 vs 버스트의 짝**. 이 페이지는 N개 트리거에 *분산* 누적(출력 85 kHz/N), 리피터 버스트는 한 트리거 내 N회 *집중*(출력 85 kHz 유지, 변환예산에 묶임). 8kw A5에서 누적→버스트 전환.
- [[adc]] — 8kw ADC 작업 호 A3.5(PPB 누적 평균)·A5(리피터 버스트 전환).
- [[adc_repeater_burst_timing]] — N=16 버스트 OSINT 레이트(85 kHz, 트리거당 1회) 라이브 실측. §6 "트리거당 N회" 노하우의 충족 근거.
- [[am263p_trm]] — ControlSS ADC PPB 레지스터 정의 출처(`ch07_5_controlss.md` §7.5.2.14.5).
