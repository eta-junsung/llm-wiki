---
tags: [roadmap, pwm, 8kw-ev-wpt-tx, living-doc]
date: 2026-06-09
---

# pwm — 8kW WPT TX 보드 PWM 전력제어 작업 호 (P0~P4)

> ADC 계측 브링업([[adc]]) 다음의 **전력제어** 작업 호. **미착수** — 이 페이지는 spine 골격이며 P0(요구사항 확정)이 첫 게이트.
> 핀맵·구체 스펙은 P0에서 채운다. 현재 위치·다음 시작점은 [[status]].

상위 프로젝트 호는 [[roadmap]].

---

## 0. 한 줄 요약

LP-AM263P의 **EPWM** 모듈로 8kW WPT 송신 인버터 게이트 구동 PWM을 구현한다. 기본 출력 → 다채널/위상·dead-time → 보호(trip-zone) → ADC 피드백 제어 순.

---

## 1. 사실 / 가설 / 모름 (착수 전 가름)

- **사실**:
  - AM263P는 EPWM 모듈을 가짐(이미 UART5가 EPWM15 패드를 alt-function으로 빌려 쓰는 중 — [[am263p_iomux_force_io_enable]]). PWM 채널 핀 배정 시 **UART5(EPWM15_A/B)와의 충돌 여부 확인 필요**.
  - 보드에 LCC 전류 센서(I_LCC_SEN)·코일 전류(I_COIL_SEN)·입력 전압/전류(GA_Vin/GA_Iin) 계측이 있음([[adc_pinmap]]) → PWM 제어가 이 피드백을 쓸 공산.
- **가설(미확인 — P0에서 확정)**:
  - 토폴로지 = **LCC 공진형 인버터**일 가능성(ADC 신호명 `I_LCC_SEN` 단서). [가설]
  - 스위칭 주파수 = EV WPT 표준대역(SAE J2954, ~85 kHz) 부근일 가능성. [추정·확인 필요]
- **모름(스펙 입수 필요)**:
  - 인버터 구조(풀브리지/하프브리지)·스위치 수 → **PWM 채널 수**.
  - 스위칭 주파수·duty 범위·dead-time 요구값.
  - 위상 시프트 제어 여부(위상천이 전력제어인지).
  - 게이트 드라이버 입력 극성·shutdown 입력, trip(보호) 신호 소스.

---

## 2. 마일스톤 호 (P0~P4) — 전부 미착수

| 단계 | 범위 | 완료 기준 | 상태 |
|------|------|---------|------|
| **P0** | PWM 요구사항·핀맵 확정 | 토폴로지·채널 수·주파수·dead-time·위상·보호신호 + EPWM 인스턴스/핀 배정표(UART5 충돌 점검 포함) | ✗ (스펙 대기) |
| **P1** | 기본 PWM 출력 | EPWM SysConfig 설정 → 단일 채널 PWM 실보드 출력, 오실로로 주파수·duty 검증 | ✗ |
| **P2** | 다채널·위상·dead-time | 인버터 채널 전부 + dead-time 삽입 + (필요 시)위상 시프트, 상보 PWM 검증 | ✗ |
| **P3** | 보호 (trip-zone) | 과전류/과전압 시 PWM 즉시 차단 — ADC/비교기/외부 trip 입력 연동, 실보드 차단 검증 | ✗ |
| **P4** | 제어 루프 연동 | ADC 피드백(전류·전압) → duty/위상 갱신 폐루프, 목표값 추종 | ✗ |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 추가 정보 필요 / `✗` 미구현

---

## 3. 단계별 작업 내용 (초안 — P0 확정 후 구체화)

### P0 — 요구사항·핀맵 확정 (첫 게이트)

- §1 "모름" 항목을 보드 설계자료/요구사항에서 입수해 확정.
- EPWM 인스턴스·출력핀(J? 커넥터/게이트 드라이버 배선) 배정표 작성 → [[adc_pinmap]] 형식의 `pwm_pinmap` 엔티티로 환원.
- **UART5가 점유한 EPWM15_A/B(P15/R16)와 충돌하지 않는 EPWM 인스턴스 선택** 확인.
- 물리 인스턴스/핀은 처음부터 hard `$assign`([[am263p_syscfg_soft_vs_hard_assign]]) — ADC에서 겪은 soft 재셔플 함정 회피.

### P1 — 기본 PWM 출력

- EPWM 1채널 SysConfig 설정(주파수·duty), 실보드 출력 → 오실로로 주파수·duty 폭 검증.
- 출력 force-enable 필요 여부 점검([[am263p_iomux_force_io_enable]] — alt-function 패드 버퍼).

### P2 — 다채널·위상·dead-time

- 인버터 스위치 전부에 상보 PWM + dead-time. 풀브리지면 위상 시프트 제어 가능성.
- (참조: oled rx_control의 dead-time/위상 개념 [[dead_time]]·[[pwm_system]] — 단 STM32 TIM 기반이라 레지스터는 다름, 개념만 참고.)

### P3 — 보호 (trip-zone)

- EPWM trip-zone(TZ)로 과전류/과전압 즉시 차단. ADC 한계비교/내부 비교기/외부 trip 핀 소스 결정.
- (개념 참조: oled [[trip_zone]] — BKIN→PWM 차단 패턴, 개념만.)

### P4 — 제어 루프 연동

- ADC 피드백(I_LCC/I_COIL/GA_Iin/GA_Vin) → duty 또는 위상 갱신. RTI/ISR 주기 제어.

---

## 4. 현재 위치

→ [[status]] 단일 소스. **미착수** — ADC A2 완료 후 다음 활성 트랙 후보. 착수 전 P0(스펙 확정) 선결.

---

## 5. 블로커 / 선결

- **P0 스펙 미확정**: 토폴로지·채널·주파수·dead-time·보호신호 — 보드 설계자료/요구사항 입수 필요(ADC A3 센서 스펙과 함께 묶어 확보하면 효율적).
- **UART5 핀 충돌 점검**: EPWM15가 UART5에 점유됨 — PWM 채널 배정 시 회피 확인.

---

## 6. 환원 후보

- PWM 핀맵 → `pages/entities/pwm_pinmap.md` (P0 완료 후).
- AM263P EPWM 설정 노하우 → lp-am263p concept(`am263p_epwm_*`)으로 환원 (플랫폼 공통, ADC 정본들과 동일 패턴).
