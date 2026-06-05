---
date: 2026-06-05
---

# 8kw-ev-wpt-tx — 구현 현황

> 전략 spine은 [[roadmap]], 작업 단위 호는 [[adc]].

## 직전 완료 (2026-06-05) — A1: 단채널 ADC 실보드 검증 (RTI 트리거 + EOC ISR)

- **단일 핀 AIN0** 으로 ADC 변환 경로 **실보드 검증 완료** — **1 kSPS(RTI 1 ms 주기 트리거) + EOC 인터럽트에서 결과 read+flag, main 루프 consuming**(ISR-flag 패턴). raw count → voltage → UART 출력 확인.
- **설계 변경**: A1 원안 "polling"에서 **RTI 타이머 트리거 + EOC ISR**로 전환(타이밍 결정성·가벼운 ISR). 검증된 패턴·트리거 결선 함정은 [[am263p_adc_rti_trigger]] 정본으로 환원.
- **핵심 함정 해소**: RTI→ADC SOC 트리거가 안 걸리던 원인은 SysConfig `enableIntr0`(Enable Compare Interrupt) 미설정 → INT0 이벤트 export 게이트 차단. SW force로 변환 경로 생존을 먼저 확인해 "트리거 결선 문제"로 좁힘. 상세 [[am263p_adc_rti_trigger]] §1·§2.

### 그 전 (2026-06-04) — A0 전제: CCS 프로젝트 스캐폴드

- LP-AM263P(AM263P4/ZCZ_C, r5fss0-0, nortos, ti-arm-clang) **hello_world 기반 CCS 프로젝트**를 repo 루트(`g/8kw-ev-wpt-tx`)에 in-place 생성. 프로젝트명 `8kw-ev-wpt-tx`. Release 빌드 통과·커밋·푸시 완료(`origin/master`).
- 작업환경 메모: CCS workspace는 git 저장소 밖 전용 폴더로 두고, 프로젝트는 git 트리에 둔 채 "Copy into workspace 해제"로 참조 import.

## 다음 작업: UART 모니터링 주기화 → ADC 코드 리팩토링 → 남은 핀 추가

순서대로 진행한다 (상세 [[adc]] §향후 작업):

1. **UART 모니터링 주기화** — 현재 매 샘플마다 무제한 print. **1초 주기 출력**으로 변경하되, **주기를 나중에 조절 가능한 파라미터**로 둘 것.
2. **ADC 코드 리팩토링** — 단일 핀으로 설계 검증이 끝났으므로 `src/bsp/adc.{c,h}`를 **다핀 확장에 맞게** 정리(채널별 결과 버퍼 + main 루프 소비 유지).
3. **남은 ADC 핀 추가 (A2)** — 리팩토링 이후, [[adc_pinmap]] 회로도상 나머지 채널 활성화: ADC0(AIN1), ADC1(AIN1), ADC2(AIN0), ADC3(AIN0), ADC4(AIN0).

## 구현 현황

| 기능 | 상태 | 메모 |
|------|------|------|
| CCS 프로젝트 스캐폴드 (A0 전제) | ✓ | hello_world 기반, Release 빌드 통과, 커밋됨 |
| 단채널 ADC SysConfig+트리거 (A0 일부) | ✓ | AIN0 단일 채널 + RTI1 트리거, `enableIntr0` 결선 확정. 나머지 채널 미추가 |
| 단채널 실보드 검증 (A1) | ✓ | AIN0, RTI 1 kSPS + EOC ISR, raw→voltage→UART 검증. 설계 polling→RTI 트리거 전환 |
| UART 모니터링 주기화 | ✗ | 1초 주기(조절 가능 파라미터). 다음 첫 작업 |
| ADC 코드 리팩토링 (다핀 확장) | ✗ | `src/bsp/adc.{c,h}` 정리 |
| 전채널 추가·순차 읽기 (A2) | ✗ | 리팩토링 후 나머지 5채널, 6채널 UART 출력 |
| 신호별 스케일링 (A3) | ? | 센서 스펙 추가 입수 필요 |
| 실보드 교차검증 (A4) | ✗ | 멀티미터 기준값 교차 |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 추가 정보 필요 / `✗` 미구현

## 미결 사항

- **A3 블로커**: 신호별 센서 스펙 미입수 — Temp_Module1/2 출력 특성(V/°C), GA_Vin 분압비, I_LCC_SEN·I_COIL_SEN 전류 센서 감도(mV/A), GA_lin_SEN 스펙.
- **UART 출력 주기 파라미터화**: 현재 하드코딩(매 샘플 print) → 1초 기본·조절 가능 파라미터로 분리 필요.
