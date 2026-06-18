---
tags: [roadmap, 8kw-ev-wpt-tx, living-doc]
date: 2026-06-19
---

# 8kw-ev-wpt-tx — 프로젝트 로드맵

> 프로젝트 목표까지의 전체 호. 단계 spine은 작업 로드맵으로 위임하고, 여기는 **목표·작업 호 인덱스·현재 위치**만 둔다.
> 전술(기능별 현황·다음 시작점)은 [[status]]가 단일 소스.

---

## 0. 목표

**eta 8kW EV WPT 송신 보드(Ver1.0E00) 펌웨어 구현** — LP-AM263P 기반으로 ADC 계측, PWM 전력 제어 등 송신 보드 기능을 구현하는 것이 목표.

---

## 1. 작업 호 (tasks)

| task | 범위 | 호 | 상태 |
|------|------|----|------|
| **adc** | eta 보드 J3 6채널 ADC 브링업 (온도·전압·전류·선형) | A0~A4 → [[adc]] | A2 ✓ (6채널 실보드 검증·AIN hard assign·테이블 리팩토링). 다음 = A3 스케일링(스펙 대기) |
| **pwm** | EPWM 전력제어 (인버터 게이트 구동·보호·제어루프) | P0~P4 → [[pwm]] | **P1 ✓**(4핀 실보드 검증·shoot-through 0 `6e6b342`) **+ P2 ✓**(`ETA_DEADTIME_NS` 단일소스·150/300ns `8046744`, **85 kHz 고정·100/150/400ns 스윕 PASS·`eta_tuning.h` config 분리 `d01fc0a`**, 85.032 kHz 실측). 다음 = P3 보호 / dead-time 최종값(전력단 브링업) / 보호신호 스펙 |

| **gpio** | GPIO 출력 브링업 (485_EN·GD_EN_seed) + UART5 양방향 확장 | G0~G1 → [[gpio_impl]] | **G0 ✓** (eta_gpio.{c,h}·실보드 검증·UART5 양방향·GUI GPIO Control, 2026-06-16). 잔여 = GUI 왕복 검증 완료 후 커밋 |

| **toolchain** | CCS/SDK 이중 빌드 스택업 — gmake+CCS GUI (ccs2050→ccs2100) | — | △ gmake 신 스택 경고 0 성공(branch `toolchain-ccs21-sdk2606`, 5a5fa44, 2026-06-19). 실보드 부팅 검증·CCS GUI Phase 2 미완. 정본 [[sdk_ccs_toolchain_migration]] |

추가 후속 작업이 생기면 `roadmaps/<task>.md`로 추가하고 위 표에 행을 더한다.

---

## 2. 현재 위치

- **전략 단계**: `adc` 작업 **A2 완료** — 6채널 ADC 실보드 검증(2026-06-09, commit c512e3b). 물리 인스턴스 5개(ADC0~4) + AIN 핀 모두 hard `$assign`, RTI1 공통 트리거, eta_adc.c 테이블 주도 리팩토링. ADC 잔여 = A3 스케일링(센서 스펙 대기·블로커) / UART5 차동 송신 복구(미해결) / A4 교차검증.
- **활성 트랙**: `gpio` 작업 호 — **G0 구현·실보드 검증 완료(2026-06-16)**. GUI 왕복 검증 후 커밋. 완료 후 다음 = PWM P3 보호(블로커: 보호신호 스펙).
- **완료 트랙**: `pwm` 작업 호([[pwm]], P0~P4) — **P1 완료**(EPWM2/4/7 4핀 실보드 검증, 레그2 두 모듈 SYNC 상보, shoot-through 0) **+ P2 완료**(`ETA_DEADTIME_NS` 단일소스·150/300ns `8046744`) **+ 85 kHz 고정·dead-time config 분리(`d01fc0a`)** — **85.032 kHz 실측**, dead-time 100/150/400ns 스윕 4ch PASS(shoot-through 0), `eta_tuning.h` knob 분리(100~400ns `#error` 가드)·주파수/dead-time 런타임 override로 SysConfig 면역. 레그2 SYNC dead-time·모듈간 비대칭(~11ns)은 plat 정본 [[am263p_epwm_module_sync_deadtime]]. 다음 = P3 보호(trip-zone) / dead-time 최종값(전력단 브링업) / 보호신호·게이트 극성 회로도 스펙 확보.
- **별트랙 완료(2026-06-11)**: UART5 PC 텔레메트리 — 18B 바이너리 패킷([[uart5_packet_protocol]]) + PC GUI([[pc_monitor_gui]]) 실보드 검증(branch uart5, ba241fa·979699d). A1.5 UART 출력의 진화(채널 하드코딩 해소). 잔여 = 송신 논블로킹화·RS-485 Phase 2.
- **신규 트랙 (2026-06-19)**: `toolchain` — branch `toolchain-ccs21-sdk2606`. gmake 신 스택 경고 0 성공(commit 5a5fa44). 실보드 부팅 검증·CCS GUI Phase 2 진행 중.
- **전술(다음 시작점·기능별 현황)**: [[status]] 단일 소스.

---

## 3. 남은 일정 / 환원 후보

→ [[adc]] §단계별 작업 내용, [[pwm]] §마일스톤 호 참조.
