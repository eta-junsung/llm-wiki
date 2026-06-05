---
date: 2026-06-05
---

# 8kw-ev-wpt-tx — 구현 현황

> 전략 spine은 [[roadmap]], 작업 단위 호는 [[adc]].

## 직전 완료 (2026-06-04) — A0 전제: CCS 프로젝트 스캐폴드

- LP-AM263P(AM263P4/ZCZ_C, r5fss0-0, nortos, ti-arm-clang) **hello_world 기반 CCS 프로젝트**를 repo 루트(`g/8kw-ev-wpt-tx`)에 in-place 생성. 프로젝트명 `8kw-ev-wpt-tx`.
- SDK hello_world projectspec(MCU_PLUS_SDK_AM263Px@26.00.00)에서 생성, ADC는 아직 미설정(순수 hello_world).
- **Release 빌드 통과** 확인(`.out`/`.mcelf` 생성). 첫 커밋·푸시 완료(`origin/master`).
- 작업환경 메모: CCS workspace는 git 저장소 밖 전용 폴더(또는 상위 폴더 Open Folder)로 두고, 프로젝트는 git 트리에 둔 채 "Copy into workspace 해제"로 참조 import.

## 다음 작업: A0 — CCS SysConfig에서 ADC0~ADC4 인스턴스 + 채널 핀 할당

[[adc_pinmap]] 핀맵 기준으로 ADC0(AIN1), ADC1(AIN0·AIN1), ADC2(AIN0), ADC3(AIN0), ADC4(AIN0) 5개 인스턴스를 SysConfig에 추가하고 빌드 성공을 확인한다.
- 착수 전: SysConfig MCP 버전과 `example.syscfg` 버전 정합 확인(`getActiveSysConfigMCPVersion` → 필요시 `changeSysConfigVersion`).

## 구현 현황

| 기능 | 상태 | 메모 |
|------|------|------|
| CCS 프로젝트 스캐폴드 (A0 전제) | ✓ | hello_world 기반, Release 빌드 통과, 커밋됨 |
| ADC SysConfig 설정 (A0) | ✗ | 5개 인스턴스, 6채널 핀 할당 |
| 단채널 polling 검증 (A1) | ✗ | ADC1_AIN0(Temp_Module2) |
| 전채널 순차 읽기 (A2) | ✗ | 6채널 UART 출력 |
| 신호별 스케일링 (A3) | ? | 센서 스펙 추가 입수 필요 |
| 실보드 교차검증 (A4) | ✗ | 멀티미터 기준값 교차 |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 추가 정보 필요 / `✗` 미구현

## 미결 사항

- **A3 블로커**: 신호별 센서 스펙 미입수 — Temp_Module1/2 출력 특성(V/°C), GA_Vin 분압비, I_LCC_SEN·I_COIL_SEN 전류 센서 감도(mV/A), GA_lin_SEN 스펙.
