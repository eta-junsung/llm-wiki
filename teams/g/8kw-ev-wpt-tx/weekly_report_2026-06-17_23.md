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
