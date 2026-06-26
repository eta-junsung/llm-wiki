---
tags: [concept, am263p, adc, rti, sysconfig, 정본]
source: 2026-06-05 8kw-ev-wpt-tx ADC 브링업 실보드 실측 + TI MCU+SDK `examples/drivers/adc/adc_soc_rti`. 6채널(5 인스턴스) 확장 경과 추가 (2026-06-09 c512e3b). EPWM0_SOCA 트리거 경로 정본화 — branch feature/adc-trigger-epwm0(3e5f117) 코드 + SDK etpwm.h/adc.h + TRM 인용 (2026-06-26)
date: 2026-06-26
---

# am263p_adc_rti_trigger — AM263P ADC SOC 트리거 정본 (RTI · EPWM)

> **AM263P 플랫폼 공통 ADC 트리거 정본.** ADC SOC를 주기 트리거(RTI 타이머 §1 / EPWM SOC §5)로 구동할 때의 SysConfig 결선과, JTAG/RAM 레지스터 검증의 측정 시점 함정. RTI 경로와 EPWM 경로는 **활성화 메커니즘이 다르다** — §5 ★함정 주의.
> 2026-06-05 8kw-ev-wpt-tx adc 브링업에서 단일 핀(AIN0) 1 kSPS RTI 트리거로 검증, 2026-06-26 EPWM0_SOCA 85 kHz로 전환(branch feature/adc-trigger-epwm0). flash-time 도구 정본([[jtag_flash_harness]])과 동일 패턴 — AM263P 플랫폼 지식은 lp-am263p에 둔다.
> PPB HW 평균은 별도 정본 [[am263p_adc_ppb_averaging]]로 분리(§4는 요약·위임). 8kw 적용 호 [[adc]], 핀맵 [[adc_pinmap]].
> ⚠️ **파일명은 역사적 이유로 `am263p_adc_rti_trigger`** (RTI 브링업에서 출발). 내용은 RTI+EPWM 일반 트리거 정본으로 확장됨 — 백링크 13곳 보존을 위해 `am263p_adc_trigger`로의 개명은 보류(향후 일괄 개명 후보).

---

## 1. RTI 타이머를 ADC SOC 트리거로 쓸 때의 결선 함정 (핵심)

**증상.** ADC가 완전히 설정되고(`ADCCTL1.ADCPWDNZ=1`, SOC `TRIGSEL=RTI1`), SW force(`ADCSOCFRC1`)로는 변환이 정상인데, **RTI를 주기 트리거로 걸면 변환이 한 번도 안 일어난다.** RTI compare 자체는 발생함(`RTIINTFLAG` 셋 확인됨).

**원인.** ADC 쪽에서 `soc0Trigger = ADC_TRIGGER_RTI1`로 트리거 소스를 고르는 것만으로는 **부족하다.** RTI 인스턴스에서 **compare interrupt를 켜야 한다**(SysConfig `enableIntr0`). 이게 꺼져 있으면 SysConfig 생성 코드(`ti_drivers_open_close.c`)가 `RTI_intDisable(.. INT0_FLAG)`를 내보내, RTI compare0의 **INT0 이벤트 export가 막힌다.** ADC SOC가 tap하는 RTI 이벤트 라인이 바로 이 INT0 라인이라, 게이트가 닫히면 compare가 발생해도 ADC 트리거 입력에 닿지 못한다.

**해결.** SysConfig에서 해당 RTI 인스턴스의 `enableIntr0 = true`(**Enable Compare Interrupt**). 그러면 생성 코드가 `RTI_intEnable(.. INT0_FLAG)`로 바뀌고 주기 트리거가 살아난다.

- RTI ISR 본체는 SysConfig가 **플래그 클리어만 하는 최소 함수로 자동 생성**하므로 별도 작성 불필요.
- **DMA-trigger(`enableDmaTrigger0`)는 불필요** — INT0 event export로 충분(동작 레퍼런스도 DMA 미사용).
- `.syscfg`는 반드시 **SysConfig 도구로 수정**(직접 편집 금지). → 루트 ccs-sysconfig 규약.

**동작 레퍼런스.** SDK `examples/drivers/adc/adc_soc_rti` — 정확히 RTI1 → ADC SOC0 시나리오. 우리 설정과의 **유일한 의미 차이가 `enableIntr0` 한 줄**이었다. AM263P ADC 트리거 디버그 시 이 예제를 diff 기준선으로 삼을 것.

---

## 2. JTAG/RAM로 페리페럴 레지스터 검증 시 측정 시점 함정

`loadProgram` 후 **reset 없이** 레지스터를 읽으면 `Drivers_open()`/SysConfig 설정 블록이 **실행되기 전** 상태(전부 0)를 보게 되어 "ADC 미설정"으로 **오진하기 쉽다.**

**올바른 절차:** `reset → reload → run → init 통과 지점(main loop)까지 진행 → read`. 레지스터가 "전부 0"으로 나오면 결함을 단정하기 전에 **측정 시점부터 의심**한다.

**진단 기법 — SW force로 경로 분리.** SW force(`ADCSOCFRC` 등)로 변환 경로 생존을 먼저 확인하면 **"ADC 설정 문제"와 "트리거 결선 문제"를 분리**해 가를 수 있다. §1의 결함도 이 기법으로 트리거 결선 문제로 좁혔다 (SW force 변환 OK → RTI 주기 트리거 무동작 → 트리거 export 게이트 의심).

> 같은 "측정 시점 / ground-truth" 류 함정은 flash 굽기에서도 반복됨 — [[jtag_flash_harness]]의 standalone 부팅 banner = ground truth, MCP readback 시점 주의 참고.

---

## 3. (참고) 검증된 ADC 설계 패턴 — RTI 트리거 + EOC ISR-flag

8kw-ev-wpt-tx에서 단일 핀(AIN0)으로 **검증 완료(1 kSPS, 1 ms)** 한 패턴:

- **RTI 타이머 주기 트리거** → ADC SOC (트리거 결선은 §1 준수).
- **EOC 인터럽트**에서 결과 read + flag 저장.
- **main 루프가 flag consuming** (ISR-flag 패턴) — ISR은 짧게.
- 샘플레이트는 **SPS(= RTI compare 주기) 기준**으로 설정.

이 패턴이 polling 방식보다 타이밍이 결정적이고 ISR이 가벼워 권장. 다핀 확장 시에는 채널별 결과 버퍼 + main 루프 소비를 유지한 채 ADC 인스턴스/채널을 늘린다.

> **확장 경과(2026-06-09, commit c512e3b)**: 8kw가 이 패턴 그대로 **6채널(5 인스턴스 ADC0~ADC4)**으로 확장·실보드 검증 완료 — 단일 **RTI1**(SysConfig 논리명 `CONFIG_RTI0`) 트리거를 5개 인스턴스가 공유, ADC1만 SOC0+SOC1 라운드로빈으로 **SOC1 EOC 단일 ISR**에서 2채널 coherent read(나머지는 SOC0 단독). ISR은 raw만 저장, main `eta_adc_loop`이 `(raw*3300)/4095` 정수 mV 변환(out-param). 인스턴스별 ISR/init/loop는 인스턴스 테이블 + 공용 ISR로 통합 리팩토링됨. UART 출력 주기화는 별도 **RTI2**(syscfg `CONFIG_RTI1`)로 분리. 적용 현황 [[adc]] §A2.

- **어느 인스턴스/채널에 무엇을 배정하는가** → [[am263p_adc_instance_allocation]] (동시성 요구·변환시간 예산 기준, 안정성 아님).
- **논리 인스턴스명을 물리에 고정하는 법** → [[am263p_syscfg_soft_vs_hard_assign]] (soft `$suggestSolution`은 인스턴스 추가 시 reshuffle돼 엉뚱한 핀을 읽음 — hard `$assign` 필수).

---

## 4. PPB 오버샘플링 / HW 평균 → 별도 정본으로 분리

PPB(Post-Processing Block) HW 평균은 **분량이 커져 전용 정본 [[am263p_adc_ppb_averaging]]로 분리**했다 (2026-06-26). 핵심만:

- PPB가 오버샘플 합/평균을 CPU 없이 계산. **2의 거듭제곱(최대 1024)일 때만** 비트시프트로 HW 자동 평균(`SHIFT=n` → `÷2^n`).
- ISR을 EOC가 아니라 **OSINT(평균완료)**에 건다 → 8kw N=64(HW 확정)·85 kHz ⇒ ISR 1.33 kHz.
- SDK v2 API: `ADC_setupPPB`/`setPPBCountLimit`/`setPPBShiftValue`/`readPPBSum`. 상세·라인 인용은 분리 정본 참조.

### ~~미검증(△)~~ → 해소 (2026-06-26)

- ~~△ ADC 인스턴스당 변환시간 실수치~~ → **확정**: 단일 변환 ≈ 315 ns(ADCCLK 50 MHz). 정적 산정 정본 [[am263p_adc_instance_allocation]] §변환시간 예산. 단 N은 트리거에 걸쳐 누적되므로 변환시간 예산과 무관(repeater와 대비).
- ~~△ SDK PPB API 표면~~ → **확정**: 함수·인수·SysConfig 위젯 매핑 모두 [[am263p_adc_ppb_averaging]] §3에 인용 정리.

---

## 5. EPWM SOC 트리거 경로 (정본 — 2026-06-26 전환 완료)

8kw가 RTI1(1 kSPS) → **EPWM0_SOCA(85.032 kHz)**로 트리거 전환(branch feature/adc-trigger-epwm0, commit `3e5f117`). EPWM0는 commit `4014901`에서 도입된 **output-less 더미 fan-out 마스터**(EPWM2/4/7 SYNC 기준 클럭).

### ADC 쪽 결선 (RTI와 동일 메커니즘)

- 각 ADC 인스턴스가 `ADCSOCxCTL.TRIGSEL`에서 트리거를 **독립 선택**한다 (TRM `ch07_5_controlss.md`:695,719 — "ADCSOCA or ADCSOCB from each ePWM module"). → **단일 EPWM0_SOCA가 5개 인스턴스에 fan-out.** RTI1을 5 인스턴스가 공유하던 것과 동일 메커니즘.
- 값: `ADC_TRIGGER_EPWM0_SOCA = 0x08` (`adc/v2/adc.h`:235). SysConfig `soc0Trigger = "ADC_TRIGGER_EPWM0_SOCA"` (8kw `example.syscfg`:70,73,99,120,141,162 — 6 SOC 전부).

### EPWM 쪽 결선 (SysConfig가 생성)

- `EPWM_enableADCTrigger(base, EPWM_SOC_A)` (`epwm/v1/etpwm.h`:6232) + `EPWM_setADCTriggerSource(base, EPWM_SOC_A, EPWM_SOC_TBCTR_ZERO, 0)` (etpwm.h:6315; `EPWM_SOC_A=0` :1281, `EPWM_SOC_TBCTR_ZERO=1` :1296). up-down 카운터에서 **TBCTR_ZERO = 주기당 1회 = 트리거 레이트.**
- 8kw에선 런타임 호출이 아니라 **SysConfig가 생성**: `epwm4`(=CONFIG_EPWM0) `epwmEventTrigger_EPWM_SOC_A_triggerEnable = true` + `..._triggerSource = "EPWM_SOC_TBCTR_ZERO"` (`example.syscfg`:228–229).

### ★함정1 — RTI의 `enableIntr0` 게이트 함정은 EPWM에 적용 안 된다

§1의 RTI 트리거는 `enableIntr0`(INT0 이벤트 export)를 켜야 ADC에 닿았다. **EPWM 경로엔 이 함정이 없다** — EPWM `ETSEL.SOCAEN`이 SOC 펄스를 트리거 XBAR로 **직접** 내보낸다(중간 게이트 없음). §1 RTI 함정을 EPWM에 투사하지 말 것.

### ★함정2 — 실효 85 kHz는 런타임 override에서 나온다 (SysConfig 정적값 ≠ 실효값)

`example.syscfg`의 EPWM0 정적 period=1000(`example.syscfg`:226)은 **100 kHz**다 (TBCLK=200 MHz·CLKDIV=1·HSPCLKDIV=1, up-down `Fpwm = 200M/(2×TBPRD)`). 실효 **85.032 kHz**는 런타임 override에서 나온다 — `eta_bsp_pwm.c`:19 `EPWM_setTimeBasePeriod(CONFIG_EPWM0_BASE_ADDR, ETA_PWM_TBPRD)`(`ETA_PWM_TBPRD=1176`, eta_bsp_pwm.h:68), `eta_app_main.c`:54 `eta_bsp_pwm_init()`이 `System_init/Board_init`(SysConfig 적용, main.c:46–47) **이후** 호출. ⇒ **N·변환시간 예산 계산은 런타임 85 kHz(11,760 ns/트리거) 기준**으로 잡을 것, syscfg 100 kHz 아님.

### ~~△ ADC1 SOC0+SOC1 라운드로빈~~ → 확정 (EPWM 전환 후 동일 동작)

RTI에서 SOC0→SOC1 라운드로빈 하던 동작은 **EPWM 전환 후에도 유지**된다. lockstep — 한 트리거를 공유하는 SOC들은 우선순위 순서로 모두 변환되므로([[am263p_adc_ppb_averaging]] §4), ADC1의 SOC0·SOC1이 한 EPWM0_SOCA에 직렬 변환되고 두 PPB가 같은 배치 경계를 갖는다. 코드: `example.syscfg`:75 `interrupt1SOCSource = ADC_INT_TRIGGER_OSINT2`(나중 완료하는 SOC1의 OSINT2를 INT1 소스로) → 한 ISR coherent read.

### BSP 코드 함정 (해소됨)

종전 "`eta_bsp_adc.c` 주석은 RTI1인데 코드는 `CONFIG_RTI0` enable" 함정은 **전환으로 해소** — `eta_bsp_adc.c`:194에서 "RTI1(CONFIG_RTI0) 카운터 시작 제거: ADC 트리거가 EPWM0_SOCA로 전환됨" 주석과 함께 RTI 카운터 시작 코드가 제거됨. ADC 트리거 자원 서술이 EPWM0와 일치.

---

## 관련 페이지

- [[adc]] — 8kw-ev-wpt-tx ADC 작업 호(A0~A4). 이 노하우의 적용 현장.
- [[am263p_adc_ppb_averaging]] — PPB HW 오버샘플 평균 정본(§4에서 분리). 트리거→OSINT ISR 결선의 후처리.
- [[am263p_adc_instance_allocation]] — ADC 인스턴스/채널 배치 결정 가이드라인 + 변환시간 예산.
- [[am263p_syscfg_soft_vs_hard_assign]] — 논리↔물리 인스턴스 배정 함정(soft 재배치).
- [[adc_pinmap]] — 8kw eta 보드 J3 6채널 ADC 핀맵.
- [[jtag_flash_harness]] — 동일 "AM263P 플랫폼 정본 in lp-am263p" 패턴. 측정/ground-truth 함정 형제 사례.
- [[am263p_trm]] — ADC/RTI 레지스터 정의 출처(필요 시 demand-ingest).
