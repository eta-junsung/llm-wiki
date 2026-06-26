---
tags: [concept, am263p, adc, rti, sysconfig, 정본]
source: 2026-06-05 8kw-ev-wpt-tx ADC 브링업 실보드 실측 + TI MCU+SDK `examples/drivers/adc/adc_soc_rti`. 6채널(5 인스턴스) 확장 경과 추가 (2026-06-09 c512e3b)
date: 2026-06-26
---

# am263p_adc_rti_trigger — AM263P ADC 브링업 노하우 (RTI 타이머 트리거)

> **AM263P 플랫폼 공통 ADC 노하우 정본.** RTI 타이머를 ADC SOC 주기 트리거로 쓸 때 빠지기 쉬운 SysConfig 결선과, JTAG/RAM 레지스터 검증의 측정 시점 함정.
> 2026-06-05 8kw-ev-wpt-tx adc 브링업에서 단일 핀(AIN0) 1 kSPS로 검증된 내용. flash-time 도구 정본([[jtag_flash_harness]])과 동일 패턴 — AM263P 플랫폼 지식은 lp-am263p에 둔다.
> 8kw 적용 호는 [[adc]], 핀맵은 [[adc_pinmap]].

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

## 4. PPB 오버샘플링 / HW 평균 (AM263P ControlSS ADC)

AM263P ADC의 PPB(Post-Processing Block)는 CPU 개입 없이 오버샘플 평균을 하드웨어로 계산한다. SW 이동평균 대비 **RAM 버퍼·루프 연산 불필요** — 제어루프에 논블로킹.

### 동작 원리 (TRM §7.5.2.14.5)

- **PPB 1개가 SOC 1개에 연결**: `ADCPPBxCONFIG.CONFIG` = 연결 대상 SOC 번호. ADC 모듈당 PPB 4개(PPB1~4).
- **누적**: 매 변환 후 `ADCPPBxPSUM`(누적합) · `ADCPPBxPMIN`(최솟값) · `ADCPPBxPMAX`(최댓값) · `ADCPPBxPCOUNT`(카운트) 업데이트.
- **배치 완료 조건**: `ADCPPBxPCOUNT == ADCPPBxLIMIT` OR 외부 sync 이벤트 → partial registers를 final(`ADCPPBxSUM`/`MIN`/`MAX`/`COUNT`)로 이동 + `OSINTx` 인터럽트 발생.
- **자동 평균**: `ADCPPBxLIMIT = 2^n`, `ADCPPBxCONFIG2.SHIFT = n` 설정 시 PPB가 `ADCPPBxPSUM / 2^n`를 `ADCPPBxSUM`에 적재. **최대 1024샘플(2^10)**. CPU 불필요.
- **Outlier rejection** (선택적 SW 보조): `(SUM - MAX - MIN) / (COUNT - 2)`. ISR에서 계산.

### 설정 요약

| 레지스터 | 값 | 효과 |
|----------|-----|------|
| `ADCPPBxCONFIG.CONFIG` | SOC 번호 | PPB를 해당 SOC에 연결 |
| `ADCPPBxLIMIT` | 2^n (1~1024) | 배치 크기(샘플 수) |
| `ADCPPBxCONFIG2.SHIFT` | n | 자동 평균 right-shift — `ADCPPBxSUM` = 평균값 |
| `ADCPPBxCONFIG2.SYNCINSEL` | EPWM syncout 번호(Table 7-118) | 외부 sync(EPWM 주기로 배치 정렬 가능) |

### 미검증(△ — 다음 탐색 대상)

- △ **ADC 인스턴스당 변환시간 실수치**: EPWM0 85 kHz = 11.7 µs/트리거. 5인스턴스(ADC0~ADC4) 순차 배정 시 각 인스턴스 변환시간 미측정 → 오버샘플 가능 횟수 산정에 필수. [[am263p_adc_instance_allocation]] §변환시간 참조.
- △ **SDK PPB API 표면**: `ADC_setupPPB()` 등 함수명·인수 — SysConfig 위젯 매핑 미확인.

---

## 5. EPWM0 트리거 전환 고려사항 + BSP 코드 함정

### EPWM0 트리거 전환

- **EPWM0 인스턴스**: commit `4014901`에서 도입된 output-less 더미 fan-out 마스터. EPWM2/4/7 SYNC 기준 클럭, 85.032 kHz.
- **§1 export 게이트 함정 재점검 필수**: RTI 경로는 `enableIntr0` 켜서 INT0 이벤트 export 활성화가 핵심이었음. EPWM SOC 경로는 활성화 방식이 다름 — SysConfig에서 EPWM SOC 이벤트를 ADC SOC 트리거로 연결하는 경로 재확인.
- △ **ADC1 SOC0+SOC1 라운드로빈**: RTI 단일 트리거로 SOC0→SOC1 라운드로빈 하던 동작이 EPWM 전환 후에도 동일하게 동작하는지 미확인.

### BSP 코드 주석 함정 (EPWM 전환 시 갱신 대상)

`eta_bsp_adc.c` 주석에 "RTI1"이라 적혀 있지만 실제 코드는 `CONFIG_RTI0_BASE_ADDR`를 enable한다. SysConfig 논리명 `CONFIG_RTI0` = 물리 RTI1. EPWM 트리거로 전환 시 이 자원 서술도 함께 갱신할 것.

---

## 관련 페이지

- [[adc]] — 8kw-ev-wpt-tx ADC 작업 호(A0~A4). 이 노하우의 적용 현장.
- [[am263p_adc_instance_allocation]] — ADC 인스턴스/채널 배치 결정 가이드라인.
- [[am263p_syscfg_soft_vs_hard_assign]] — 논리↔물리 인스턴스 배정 함정(soft 재배치).
- [[adc_pinmap]] — 8kw eta 보드 J3 6채널 ADC 핀맵.
- [[jtag_flash_harness]] — 동일 "AM263P 플랫폼 정본 in lp-am263p" 패턴. 측정/ground-truth 함정 형제 사례.
- [[am263p_trm]] — ADC/RTI 레지스터 정의 출처(필요 시 demand-ingest).
