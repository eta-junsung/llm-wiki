---
tags: [concept, am263p, epwm, sync, topology, platform, trm]
source: AM263P TRM SPRUJ55D §7.5.6.4.3.3 Time-Base Counter Synchronization (printed pp.651–654, raw [[am263p_trm]] ch07_5_controlss.md :5683–5953) — PDF figures 7-181/7-182 직독 (2026-06-11)
date: 2026-06-11
---

# AM263P EPWM SYNC 토폴로지 — fan-out MUX·hop 지연 모델 (정합 설계 정본)

> **AM263P 플랫폼 지식 정본.** [[am263p_epwm_module_sync_deadtime]]의 "모듈간 위상 스큐" 함정의 **근본 메커니즘**을 TRM에서 환원한 페이지. 응용 패턴(상보·dead-time)은 그쪽, **왜 스큐가 생기고 토폴로지로 어떻게 0으로 만드는가**는 여기.

## 한 줄 요약

EPWM SYNC는 **모듈별 독립 MUX(fan-out)** 다 — 데이지체인(직렬 전파)이 **아니다**. 각 EPWMx가 자기 `EPWMSYNCINSEL`로 **공용 SYNCOUT 풀에서 소스 1개**를 고른다(Table 7-154). source→target **한 hop의 내부 지연은 고정값**(`TBCLK==EPWMCLK`면 **2×EPWMCLK**, `TBCLK<EPWMCLK`면 **1×TBCLK**)이고 **target 인덱스·체인 위치와 무관·누적 없음**. ⟹ **한 소스를 여러 target이 동시에 선택하면 모두 같은 지연** → 상호 스큐 0. 8kw의 ~11ns 비대칭은 "master 0-hop vs slave 1-hop"의 **hop 수 차이**(딱 2×EPWMCLK≈10ns @200MHz)이며, **둘 다 1-hop이 되도록 fan-out**하면 정수클록 스큐는 0으로 사라진다.

---

## 검증 질문 (이 페이지가 답한다)

> EPWM2 SYNCOUT을 EPWM4와 EPWM7이 각각 `SYNCINSEL`로 선택하면, 둘은 EPWM2 영점 이벤트를 **같은 지연**으로 받는가(상대 스큐 0), 아니면 인덱스 차로 **다른 지연**(스큐 잔존)인가?

**문서상 답 = 같은 지연(상대 스큐 0, 정수클록 단위).** 근거(아래 §지연 모델):
- TRM 지연 공식은 "**control module → target module**" **한 쌍당** 적용되는 고정값이고, **target 인덱스가 식에 없다**. EPWM4·EPWM7 둘 다 EPWM2로부터 정확히 1 hop → 각각 2×EPWMCLK(=`TBCLK==EPWMCLK`일 때) → **상호 정렬**.
- SYNC 분배가 **per-module MUX(병렬 fan-out)** 이므로(아래 §토폴로지) "EPWM2 다음에 EPWM4, 그다음 EPWM7" 같은 **순차 전파가 존재하지 않는다** — 둘은 같은 net을 동시에 관측한다.

⚠️ **단, "스큐 0"은 정수클록 단위.** TRM은 hop 지연을 **TBCLK/EPWMCLK 정수배로만** 모델링한다(2×EPWMCLK 또는 1×TBCLK). 두 target이 **같은 TBCLK 에지**에서 TBPHS를 래치하므로 정수클록 스큐는 0이지만, **sub-clock(조합 라우팅) 잔류 스큐**는 TRM 모델 해상도 밖이라 "0 보장"이 아니다. 8kw 실측 11ns 중 **정수부 ~10ns(=2×EPWMCLK)는 fan-out으로 소거 예상**, 잔여 ~1ns(라우팅/측정)는 미지. **이는 예측이며 미검증** — fan-out 결선 후 Saleae 재측이 검증 경로.

---

## SYNC 토폴로지 — per-module MUX (Figure 7-181)

각 EPWM 모듈은 SYNC 신호 3개를 가진다: **SYNCI**(입력)·**SYNCO/SYNCOUT**(출력)·**SYNCPER**(주변장치 동기 출력, CMPSS/DAC용). ("SYNCO와 SYNCOUT은 혼용" — Figure 7-181 노트.)

**핵심: SYNCIN은 글로벌 단일 net이 아니라 모듈마다 독립 MUX다.** Figure 7-181의 SYNCIN 셀렉터:

```
[Disable]
[EPWM1SYNCOUT]
[EPWMxSYNCOUT]        ──┐
[ECAP1SYNCOUT]          ├─MUX──> EPWMxSYNCIN   (선택자 = EPWMSYNCINSEL)
[ECAPySYNCOUT]          │
[Other Sources]       ──┘
```

- **EPWMSYNCINSEL.SEL** (모듈마다 1개) 가 공용 SYNCOUT 풀에서 **소스 1개를 선택**. 풀 = 전 EPWM0~23 SYNCOUT + ECAP0~9 SYNCOUT + INPUTXBAR OUT.4/.20 + TIMESYNCXBAR SYNCPWMOUT0/1 + FSI RX0~3 RXTRIG0~3. 전체 인코딩은 **Table 7-154**(raw :5875–5953).
- 따라서 **N개 모듈이 같은 소스를 동시에 선택 가능**(fan-out). 한 모듈의 SYNCOUT은 net 하나이고 여러 target MUX 입력에 **병렬로 분배**된다. **모듈 번호순 직렬 전파(daisy chain) 개념은 TRM에 없다.**

**SYNCOUT 생성 로직**(Figure 7-181 좌측): `EPWMSYNCOUTEN`의 enable 비트들 — **SWEN/ZEROEN/CMPBEN/CMPCEN/CMPDEN/DCARVT1EN/DCBEVT1EN** — 이 각 이벤트(SWFSYNC·CTR=ZERO·CTR=CMPB/C/D·DCAEVT1.sync·DCBEVT1.sync)를 OR해서 그 모듈의 SYNCOUT을 만든다. + one-shot sync 경로(GLDCTL2[OSHTLD]·TBCTL2[OSHTSYNC/OSHTSYNCMODE]·TBCTL3[OSSFRCEN], One-Shot Latch). 8kw는 `syncout=ON_CNTR_ZERO`(=ZEROEN) 사용.

**SYNCPER**(Figure 7-181 우측): `HRPCTL[PWMSYNCSELX]`가 CTR=CMPC/CMPD UP/DOWN을, `HRPCTL[PWMSYNCSEL]`이 CTR=PRD/CTR=ZERO를 골라 EPWMxSYNCPER 생성 → CMPSS/DAC 동기. HRPWM과 무관(Table 7-153 EPWMxSYNCPER 설명).

**EXTSYNCOUT**(Figure 7-182): EPWM1/EPWMx/ECAP1/ECAPy SYNCOUT 중 `SYNCSEL.SYNCOUT`로 골라 → **8 PLLSYSCLK cycle pulse-stretch** → 핀(EXTSYNCOUT)으로. 칩 외부로 나가는 경로만 stretch이며, **칩 내부 SYNCOUT→SYNCIN 경로의 지연은 아래 2×EPWMCLK 모델**(stretch와 별개).

---

## 지연 모델 — hop당 고정, 인덱스 무관 (§7.5.6.4.3.3)

TBCTL[PHSEN]=1인 모듈은 SYNCIN 펄스에서 **TBPHS→TBCTR** 로드(다음 유효 TBCLK 에지). TRM 원문(raw :5837–5841, PDF p.653):

> *The internal delay from the **control module to the target module** is calculated by the following formula:*
> - *If (TBCLK == EPWMCLK): **2 × EPWMCLK** Delay*
> - *If (TBCLK < EPWMCLK): **1 × TBCLK** Delay*

이 식의 성질(검증 질문의 근거):
- **"control module → target module" 한 쌍당** 적용 — source 1개, target 1개. **target 인덱스가 식에 없다.**
- **TBCLK/EPWMCLK 비(prescale)에만 의존.** prescale=1(TBCLK==EPWMCLK)이면 2×EPWMCLK, prescale>1이면 1×TBCLK.
- **누적항 없음.** 체인 길이·모듈 거리 변수 없음 → "n번째 target일수록 더 늦는다" 같은 항이 **문서상 존재하지 않는다**.
- **에지 양자화.** "next valid TBCLK edge"에 래치 → 같은 TBCLK인 두 target은 **같은 에지**에서 잡음 → 정수클록 상호 스큐 0.

**수치(8kw)**: EPWMCLK=200MHz, prescale=1 ⟹ TBCLK=200MHz, 1 count=5ns. 2×EPWMCLK = **10ns**. 8kw 실측 비대칭 **~11ns**(≈2.2 counts) = 이 10ns(2 counts) + 라우팅/측정 ~1ns. **즉 ~11ns의 정체는 "slave가 1 hop 지연 = 2×EPWMCLK"** 이다.

---

## 왜 8kw에 스큐가 있나 / 어떻게 0으로 — hop 수 정합

현 8kw 레그2(=[[am263p_epwm_module_sync_deadtime]]):
- **EPWM4 = master 겸 출력**: 자기 TBCTR 영점이 기준. SYNCIN 없음 → **0 hop**.
- **EPWM7 = slave**: EPWM4 SYNCOUT을 SYNCIN으로 → TBPHS 로드에 **1 hop = 2×EPWMCLK ≈ 10ns 지연**.
- ⟹ **hop 수 비대칭(0 vs 1)** = 한 hop 지연 = ~10ns 비대칭. **이것이 dead-time 방향별 비대칭의 근원**(합은 2×설정값으로 보존).

**원리: 상호 정렬되려면 hop 수가 같아야 한다.** 같은 origin에서 같은 hop 수면 같은 지연 → 상호 스큐 0. hop 수가 다르면 차이 = (Δhop)×(2×EPWMCLK).

토폴로지 선택지:
| 토폴로지 | EPWM4 hop | EPWM7 hop | 레그2 내부 스큐 | 비고 |
|---|---|---|---|---|
| 현재 (EPWM4 master→EPWM7) | 0 | 1 | ~10ns | 비대칭 |
| **fan-out**: 공용소스(예 EPWM2)→EPWM4·EPWM7 둘 다 | 1 | 1 | **0**(정수클록) | 검증질문 토폴로지 |
| 외부 SYNC(EXTSYNCIN)→둘 다 | 1 | 1 | **0** | 동일 원리 |

⚠️ **풀브리지는 레그 간 정합도 필요.** 레그2 내부를 fan-out으로 맞춰도, **소스 모듈(0-hop) vs 레그2(1-hop)** 사이엔 같은 ~10ns 스큐가 생긴다. 레그1(EPWM2, 단일모듈 dead-band)이 소스면 레그1(0-hop) vs 레그2(1-hop) 스큐. **모든 출력 모듈을 동일 hop으로** 두려면: **공용 sync 소스(전용 더미 EPWM 또는 EXTSYNCIN) 하나에 전 출력 모듈(EPWM2·4·7)을 slave로** 걸어 **전부 1-hop** → 상호 0. 또는 한 모듈을 기준(0-hop)으로 두고 나머지를 **CMPB/TBPHS 트림(2×EPWMCLK≈2 counts)으로 보정**(deadtime 페이지 §함정의 "+2 counts" 후보가 이 보정). 근본 단순화는 보드 단계에서 한 레그를 한 모듈로 묶는 것.

---

## SYNC 관련 레지스터 정의 (토폴로지 전환 시 정합 설계 참조)

| 레지스터/비트 | 역할 | 정합 설계 함의 |
|---|---|---|
| `EPWMSYNCINSEL.SEL` | 모듈별 SYNCIN 소스 선택(Table 7-154) | **fan-out의 핵심** — 여러 모듈에 같은 값 = 공용 소스 |
| `EPWMSYNCOUTEN`(SWEN/ZEROEN/CMPBEN/CMPCEN/CMPDEN/DCARVT1EN/DCBEVT1EN) | 어느 이벤트가 이 모듈 SYNCOUT을 만드나 | 소스 모듈에 ZEROEN=영점 SYNCOUT(8kw `ON_CNTR_ZERO`) |
| `TBCTL[PHSEN]` | 1=SYNCIN시 TBPHS→TBCTR / 0=SYNCIN 무시 | slave는 PHSEN=1 필수. 소스(자유구동)는 0 |
| `TBCTL[PHSDIR]` | up-down 모드 sync 후 카운트 방향 | up/down-only면 무시 |
| `TBPHS` | sync 시 로드되는 위상값 | hop 보정 트림을 여기/CMPB에 |
| `TBCTL[PRDLD]` | 0=TBPRD 셰도(영점 and/or sync 로드) / 1=즉시 | 0이 기본. 가변주파수 정합 시 주의 |
| `TBCTL2[PRDLDSYNC]` | TBPRD 셰도→액티브 로드 시점(영점/sync) | PRDLD=0일 때만 유효 |
| `TBCTL2/3·GLDCTL2`(OSHTSYNC/OSHTSYNCMODE/OSSFRCEN/OSHTLD) | one-shot sync 경로 | 1회성 정렬용 |
| `CONTROLSS_CTRL.EPWM_CLKSYNC` | 인스턴스별 TBCLK 글로벌 정렬(영점에서 첫 TBCLK 에지 맞춤) | **prescale 동일** 시에만 완전 정렬(§7.5.6.4.3.2/.4.4) |

count-mode-after-sync: §7.5.6.4.6(Time-Base Counter Modes). sync 후 방향은 PHSDIR(up-down) 또는 모드 고정(up/down).

---

## 문서 주의 — Table 7-153의 "synchronization order" 참조 / 누락 아님

- Table 7-153(Key Time-Base Signals, EPWMxSYNCI 행)은 *"for the synchronization order of a particular device, see Time-Base Counter Synchronization"* 로 §7.5.6.4.3.3을 가리킨다. **그 절에 별도 "순서 표"나 체인 서술은 없다** — 가리키는 실체는 **Figure 7-181 MUX + Table 7-154 선택 매트릭스** 그 자체다. 즉 "synchronization order" = **어느 모듈이 어느 소스를 고를 수 있나(선택 행렬)** 이지, **모듈 번호순 도달 순서가 아니다**. AM263P TRM에 device-specific sync-order/체인-소속 표는 **존재하지 않음**(SPRUJ55D 기준).
- raw `.md`의 *"Refer to **for** a list of all sync inputs…"*(:5801) 의 끊긴 cross-ref는 **원본 PDF p.652에도 동일하게 끊겨 있음**(TI 문서 버그) — 추출 손실 아님. 가리키려던 대상은 정황상 Table 7-154. **⟹ raw `.md`는 PDF를 충실히 재현했고 본문 누락 없음**(검증: PDF pp.651–654 직독, 2026-06-11).

---

## 관련 페이지

- [[am263p_epwm_module_sync_deadtime]] — 응용(상보·dead-time) 패턴 + 8kw 실측. 이 페이지가 그 §함정 "모듈간 위상 스큐"의 근본.
- [[pwm_pinmap]] — 8kw 레그2 핀맵(EPWM4 master 자유구동·EPWM7 slave).
- [[pwm]] — 8kw PWM 작업 호(dead-time 비대칭 실측 결과).
- [[am263p_trm]] — 출처 TRM. §7.5.6.4.3.3 = ch07_5_controlss.md :5799–5953.
- [[instruments]] — fan-out 토폴로지 스큐 재측용(Saleae Logic Pro 16, transition CSV).
