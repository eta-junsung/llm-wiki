---
tags: [concept, am263p, sysconfig, adc, pinmux, platform]
source: 8kw-ev-wpt-tx(adc 브랜치, commit b8b0ad8, 2026-06-08) J3.27/J3.28 ADC 핀 추가 — soft 재배치 사고 진단 + hard assign 수정, 실보드 검증. UART5 점검·AIN soft 잔존 리스크 갱신 (2026-06-09)
date: 2026-06-09
---

# AM263P SysConfig 논리 인스턴스명 ≠ 물리 페리페럴 (soft vs hard assign)

> **AM263P 플랫폼 함정 정본.** SysConfig 논리 `$name`은 물리 인스턴스를 보장하지 않는다. 물리 배정이 soft(`$suggestSolution`)면 새 인스턴스 추가 시 솔버가 기존 배정까지 재최적화해 **다른 핀을 읽게** 만든다. ADC가 발견 경로지만 **일반 원리**. 형제: [[am263p_adc_instance_allocation]], [[am263p_adc_rti_trigger]], [[am263p_iomux_force_io_enable]].

## 핵심 함정

- SysConfig 논리 `$name`(`CONFIG_ADCn` 등)은 **물리 인스턴스를 보장하지 않는다.** 물리 배정이 `$suggestSolution`(**soft**)이면, **새 인스턴스를 `addInstance` 할 때 핀 솔버가 기존 soft 배정까지 자유롭게 재최적화(reshuffle)**한다.
- ADC AIN은 **전용 아날로그 패드라 물리 ADC 인스턴스에 1:1로 고정**돼 있다 → 솔버가 논리↔물리 매핑을 바꾸면 **코드는 같은 `CONFIG_ADCn`을 읽어도 실제로는 다른 물리 핀을 읽는다.**

## 관찰된 사고 (2026-06-08, J3.27 추가)

J3.27(AIN, `CONFIG_ADC4`)이 **soft 배정**이었음. **ADC4를 추가하는 순간** 솔버가:

- `CONFIG_ADC0`을 물리 ADC0 → **ADC2**로,
- `CONFIG_ADC4`를 물리 ADC4가 아닌 **ADC0**으로 밀어냄.

→ 물리 배정이 틀어져 **다른 핀을 읽게** 됨.

**증상 (가장 헷갈리는 함정).** ISR은 정상 발생하고 값도 변환되지만 **인가 전압을 미추종** — 죽은 게 아니라 **엉뚱한 핀을 읽는 것**. "J3.27 추가 전엔 J3.28이 동작했다"는 사실이 곧 **reshuffle-on-add**의 방증.

## 왜 부분 수정이 안 먹히나

`int_xbar` 소스명(`ADCx_INT1`)·base addr·AIN 패드는 **모두 *물리* 기준**이다. 논리 번호로 추론하면 어긋난다. **`int_xbar`만 물리 배정에 맞추는 우회**는 내부 정합만 맞을 뿐 **핀은 여전히 틀림** — 근본 수정이 아니다.

## 수정 (✓ 실보드 검증 2026-06-08)

보드 배선에 묶인 ADC는 **hard assign**으로 물리 인스턴스를 고정한다:

- SysConfig에서 `ADC.$assign = "ADCn"` (+ `AIN → ADCn_AINx`)로 물리 인스턴스 고정.
- 물리 배정이 맞으면 **base addr·`int_xbar` 소스가 자동 정렬**되고, **C 코드(`CONFIG_ADCn_BASE_ADDR`)는 무수정**.
- **검증**: `ti_drivers_config.h`의 `CONFIG_ADCn_BASE_ADDR` == 의도한 `CSL_CONTROLSS_ADCn_U_BASE` 인지 확인 + 실보드 인가 전압 추종 확인.

## 일반화

ADC뿐 아니라 **SysConfig에서 물리 인스턴스/핀이 보드 배선에 고정돼야 하는 모든 페리페럴**은 — `$suggestSolution`(soft)에 맡기지 말고 **처음부터 hard `$assign`**으로 못 박는다. soft에 맡기면 인스턴스 추가 때마다 reshuffle 위험.

## AIN 핀 hard 승격 — 리스크 닫음 (✓, 2026-06-09 commit c512e3b)

직전(b8b0ad8)까지 물리 *인스턴스*만 hard `$assign`이고 **개별 AIN 핀은 `$suggestSolution`(soft)** 이라 인스턴스 추가 시 핀 reshuffle 잔존 리스크가 있었다. 8kw 신규 2채널(J3.25 ADC2 / J3.26 ADC3) 추가 작업에서 **AIN 핀까지 전부 `$suggestSolution`→`$assign`** 으로 hard 승격 → 재생성 후 물리 배정 ADC0~4 유지(재셔플 없음) 확인. **이 페이지 규칙의 실증 사례** — "보드배선 고정 페리페럴은 인스턴스뿐 아니라 핀까지 처음부터 hard"가 6채널까지 확장돼 검증됨.

## 점검 결과 (해소)

- **UART5는 soft 재배치 문제가 아님 (✗, 2026-06-09 확정).** 생성 TXD 패드가 P15로 맞게 나온 게 기확인이고([[am263p_iomux_force_io_enable]]), UART5 미동작의 실제 원인은 ① `UART_write` 블록 주석화(`eta_uart5.c:159-170`) + ② **8kw 보드의** RS-485 트랜시버(THVD1400 U13 — **LP-AM263P 온보드 부품 아님**) DE/`EN_485` 제어 미구현 — soft 재배치와 무관. 상세 [[am263p_iomux_force_io_enable]] §결론.

## 관련 페이지

- [[am263p_adc_instance_allocation]] — 인스턴스를 *어떻게 정하는가*. 이 페이지는 정한 뒤 *물리로 고정하는 방법*.
- [[am263p_adc_rti_trigger]] — ADC 브링업 정본(트리거 결선·검증 측정 시점 함정).
- [[am263p_iomux_force_io_enable]] — UART5 패드 force-enable(UART5 미동작의 다른 가설).
- [[adc_pinmap]] — 8kw J3 ADC 핀맵.
