---
date: 2026-06-24
tags: [weekly-report, 8kw-ev-wpt-tx, toolchain, adc]
project: 8kw-ev-wpt-tx
---

# g팀 8kW EV WPT TX 주간 업무 보고

**기간**: 2026-06-17 ~ 2026-06-23  
**보드**: 8kW EV 무선전력전송(WPT) 송신 보드 Ver1.0E00  
**MCU**: TI AM263P (LP-AM263P LaunchPad)

---

## 요약

이번 주는 두 개의 작업을 완료하고 한 개의 작업을 착수했다.

1. **툴체인 신스택 전환 완전 완료**: CCS 20.5 / SDK 26_00_00_01 / TICLANG 4.0.4 구스택에서 CCS 21 / SDK 26_00_00_06 / TICLANG 5.1.1 신스택으로 전환을 마쳤다. gmake(Phase 1)에 이어 CCS managed build(Phase 2)까지 완료하고, 실보드 end-to-end PASS를 확인했다.

2. **새 테스트 머신 fresh-clone 검증 완료**: 새 노트북에서 `git clone -b test` → README 셋업 → `gui.bat` 더블클릭 → 빌드·플래시·standalone 부팅·deadtime 측정까지 단대단 검증을 완료했다.

3. **ADC A3 물리량 변환 착수**: I_COIL_SEN · GA_Iin_SEN · GA_Vin 3채널 스케일링 구현을 시작했다.

---

## 1. 툴체인 신스택 전환 완전 완료

### 1.1 전환 대상 및 변경 구성 요소

| 구성 요소 | 구 | 신 |
|----------|---|---|
| CCS | 20.5 / ccs2050 | 21 / ccs2100 |
| SDK | MCU+ SDK 26_00_00_01 | MCU+ SDK 26_00_00_06 |
| SysConfig | 1.27.0 | 1.28.0+4696 |
| TICLANG | 4.0.4.LTS | 5.1.1.LTS |

---

### 1.2 Phase 1 — gmake 빌드 전환

브랜치 `toolchain-ccs21-sdk2606`에서 gmake(build/) 측 신스택 경고 0 빌드 성공.

주요 변경:

- **`config.mk` 경로 3종**: SDK / CGT / SYSCFG_NODE 신 경로로 갱신
- **`makefile`**: SDK 경로 + CGT/SYSCFG_NODE override(`imports.mak` `=` 우회, include 이후 재정의) + `genimage_am26x.py` → `genimage.py` 리네임
- **`example.syscfg` `@versions`**: SysConfig 1.28.0+4696으로 갱신
- **`generated/`**: enet·SDL stub 12개 신 SDK SysConfig로 재생성
- **`ospi_flash` 스크립팅 호스트 경로**: `ccs2050` → `ccs2100`

---

### 1.3 Phase 2 — CCS Managed Build 전환 및 환경 정리

| 항목 | 내용 |
|------|------|
| `.cproject` 전환 | 신스택(CCS21/SDK_06/SysConfig1.28/TICLANG5.1.1)으로 갱신. sourceEntries 중복 심볼 해소, All Configurations 적용 |
| SBL prebuilt 갱신 | SDK_06 prebuilt(307,005B) → `C:/ti/sbl_ospi_am263p.tiimage` |
| `gui.bat` 런처 | ASCII 전용 `.bat` 래퍼 → UTF-8 BOM `.ps1` 위임 구조로 재작성 |
| 구스택 정리 | `C:\ti` 구스택(ccs2050·uniflash·SDK_01·sysconfig_1.27.0·TICLANG4.0.4) ~12.2 GB 삭제 — 신스택만 잔존 |

---

### 1.4 실보드 end-to-end 검증 결과

| 검증 단계 | 결과 |
|----------|------|
| gmake 빌드 (mcelf 생성) | 경고 0, PASS |
| flash + 전원사이클 standalone 부팅 | 정상 부팅 확인 |
| `gui.bat` → deadtime 변경 → 재flash → 재측정 | 동작 정상, 회귀 없음 |

---

## 2. 새 테스트 머신 fresh-clone 검증

새 노트북 환경에서 README §1 셋업 절차를 따라 처음부터 구성하고 단대단 검증을 완료했다.

### 2.1 셋업 체크리스트 (README §1 기준)

| 항목 | 내용 |
|------|------|
| CCS | CCS 21 (ccs2100) 설치 |
| SDK | MCU+ SDK 26_00_00_06 설치 |
| SBL 복사 | `sbl_prebuilt/am263px-lp/sbl_ospi_multicore_elf.release.tiimage` → `C:/ti/sbl_ospi_am263p.tiimage` |
| Python | 3.10+ 설치 |
| 보드 SW1 | `0,0,1,1` (xSPI 8D SFDP 부트모드) |
| Smart App Control | 해제 |
| CCS | 완전 종료 (flash 스크립트 실행 전) |

### 2.2 검증 결과

`gui.bat` 더블클릭 → gmake 빌드(.mcelf 생성) → 플래시 → 전원사이클 → standalone 부팅 → ADC 텔레메트리 수신 및 deadtime 변경 스모크 테스트 **PASS**.

---

## 3. ADC A3 물리량 변환 착수

### 3.1 배경

A2까지 구현된 ADC 경로는 raw count(0~4095) → mV(`raw × 3300 / 4095`)까지만이다. A3는 mV → 물리량(A·V·°C) 변환을 추가하는 단계.

### 3.2 이번 주 착수 채널 (3채널)

| 채널 | 신호 | 물리량 | 비고 |
|------|------|--------|------|
| I_COIL_SEN | ADC0 SOC0 AIN1 (J3.28) | 코일 전류 (A) | 스케일링 구현 중 |
| GA_Iin_SEN | ADC1 SOC1 AIN1 (J3.29) | 입력 전류 (A) | 스케일링 구현 중 |
| GA_Vin | ADC3 SOC0 AIN0 (J3.26) | 입력 전압 (V) | 스케일링 구현 중 |

### 3.3 잔여 채널

| 채널 | 신호 | 물리량 | 상태 |
|------|------|--------|------|
| Temp_Module1 | ADC2 SOC0 AIN0 (J3.25) | 온도 (°C) | 센서 출력 특성 미입수 — 블로커 |
| Temp_Module2 | ADC1 SOC0 AIN0 (J3.24) | 온도 (°C) | 센서 출력 특성 미입수 — 블로커 |
| I_LCC_SEN | ADC4 SOC0 AIN0 (J3.27) | LCC 전류 (A) | — |

---

## 잔여 항목

| 항목 | 상태 | 비고 |
|------|------|------|
| ADC A3 물리량 변환 (3채널) | 진행 중 | I_COIL_SEN·GA_Iin_SEN·GA_Vin 구현 중 |
| ADC A3 — Temp_Module1/2 | 블로커 | 센서 출력 특성(V/°C) 미입수 |
| PWM P3 보호 (trip-zone) | 착수 전 | trip-zone 입력 핀·보호 신호 스펙 확보 필요 |
| UART5 RS-485 차동 검증 | 구현 완료·미검증 | 8kW 보드 결합 시 THVD1400 차동 라인 실측 |
| UART5 송신 논블로킹화 | 잔여 | 제어루프 병행 시 DMA/콜백 전환 필요 |
| GUI Physical 단위 표시 | 블로커 | 센서 계수 입수 후 `PHYSICAL_COEFF[]` 한 곳만 수정 |

---

## 다음 작업 결정 사항 (2026-06-24 업무보고)

업무보고에서 다음 작업 우선순위를 아래 4건으로 확정했다.

| 순위 | 작업 | 범위 | 비고 |
|------|------|------|------|
| 1 | **GUI 값 소수점 세 자리 표시** | `tools/gui/gui.py` 표시 포맷 — 예) `1.23 V` → `1.234 V` | 표 ADC(V) / Physical 컬럼 포맷 변경 |
| 2 | **ADC 값 필터 추가** | 들어오는 값의 널뛰기(노이즈)가 심함 → 필터링 | **SW 구현 vs MCU ADC 자체 기능(오버샘플링/HW 평균) 중 택일은 작업 착수 시점에 판단** |
| 3 | **ADC 트리거 전환 (RTI → EPWM0)** | 현재 SOC 트리거 = RTI1(1 kSPS) → **PWM 마스터 클럭 EPWM0(85 kHz)** 로 전환 | PWM 로드맵 [[pwm]] P4 ADC 트리거 전환 항목. EPWM0 = `4014901`에서 도입한 더미 마스터 fan-out |
| 4 | **GUI 화면 녹화 기능** | GUI 라이브 화면 녹화 | **최저 우선순위 — 있으면 좋고 없으면 말고(nice-to-have)** |

### 메모

- **항목 2·3의 연계**: ADC 트리거를 EPWM0(85 kHz)로 올리면 샘플레이트가 현재 1 kSPS → 최대 85 kSPS로 크게 상승하므로, 고속 샘플 위에 필터(오버샘플링/이동평균)를 얹는 흐름이 자연스럽다. 필터 구현 위치(SW/HW)는 트리거 전환 후 노이즈 거동을 보고 함께 판단.
- 항목 1은 펌웨어 변경 없이 GUI 표시 포맷만 손대는 독립 작업.
- 정본: GUI = [[pc_monitor_gui]], ADC 트리거 = [[adc_pinmap]]·[[am263p_adc_rti_trigger]], PWM 마스터 EPWM0 = [[pwm]] §EPWM0 fan-out.
