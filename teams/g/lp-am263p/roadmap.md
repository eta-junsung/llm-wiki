---
tags: [roadmap, porting, am263p, cc3351, living-doc]
source: [[/c/Users/echog/eta/projects/g/lp-am263p/bp-3351/tasks/porting/roadmap.md]] (planner roadmap ingest)
date: 2026-05-29
---

# lp-am263p + bp-cc3351 포팅 — 전체 로드맵

> 전략 큰그림(big picture). 단계 구조·현재 위치·남은 일정의 spine만 여기 둔다.
> 깊은 디테일(칩 차이·플래시 핸드오프·dummy cycle 등)은 concept 페이지로 백링크 위임,
> 기능별 구현 현황·다음 시작점은 [[status]] (status.md)에서 관리한다.
> **사실 / 가설 / 모름을 구분한다. 추정은 "[추정]" 표기.**

---

## 0. 한 줄 요약

원래 **LP-AM243** 대상 공식 예제(`CC3xx_thick_mac_network_terminal`)를 **LP-AM263P**로 포팅 중.
프로젝트는 이미 AM263P로 마이그레이션되어 빌드/플래시/부팅까지 동작하나, **부팅 직후 app의
`Flash_open()`(AM263P 부트 플래시 IS25LX256)이 NULL 반환**하는 단계(S3)에서 막혀 있음(Round 24+).
이 블로커는 CC33xx WiFi/BLE 동작과 별개인 *플랫폼 부트/플래시 서브시스템* 문제.

**비유**: USB(부트 플래시)에 부팅 파일 일체를 굽고 → 전원 켜면 SBL·app 커널까지 RAM에 올라오나
→ RAM에서 도는 커널이 "방금 자기를 띄운 그 USB"를 다시 직접 인식(`Flash_open`)하지 못하는 상황.

---

## 1. 왜 AM243에선 되고 AM263P에선 안 되는가

- **(사실)** CC33XX SDK(R8.1)는 이 예제를 **AM243x 대상으로만** 제공 — AM263P용 공식 예제·targetConfig·syscfg 부재.
  원본 syscfg `--device "AM243x_ALX_beta"`, targetConfigs에 `AM2434_ALX*.ccxml`만 존재, README "Sitara AM2434" 명시.
- **(사실)** 따라서 이 포팅은 **TI 공식 지원 밖(비공식)** → syscfg·드라이버·플래시 정합성을 직접 맞춰야 함.
- **(사실)** 두 보드의 부트 플래시 칩 클래스가 다름:
  - AM243: **S25HL512T** (Cypress/Infineon, 64MB, **Quad-SPI** 중심) — 보드 실물 확인
  - AM263P: **IS25LX256** (ISSI, 32MB, **Octal xSPI 8D DDR** native)
  - → 라인 수(4선 vs 8선)·프로토콜 진입 시퀀스·RDID 응답 폭·레지스터 접근 opcode가 전부 다름.
  - 상세 비교표·Spansion quirk(`0x65 RDAR`/`0x71 WRAR` 부재 등)는 → [[is25lx256_vs_spansion_quirks]]
- **(가설)** 칩 차이는 "왜 AM243 흐름을 그대로 옮기면 안 되는가"는 잘 설명하나, *S3 블로커의 직접 트리거*가
  (a) SBL↔app 프로토콜 핸드오프인지 (b) RDCAP/PHY 타이밍인지 (c) DQS/캡처 설정인지는 미확정.
  핸드오프 정합 깨짐 지점·진단 절차는 → [[sbl_app_flash_handoff]]

---

## 2. LP-AM263P + BP-CC3351 조합이 가능한가

**판단: 기술적으로 가능성 높음. 단, 미증명.** (가설, 부분 사실 기반)

- **(사실)** CC33xx host 인터페이스는 표준 MCSPI + GPIO(EN/IRQ) + BLE UART. AM263P도 동일 페리페럴 보유,
  syscfg에 SPI0/GPIO/UART 배치 완료.
- **(사실)** 이미 AM263P로 마이그레이션되어 빌드·플래시 성공(R10). CC33xx SDK source/lib는 플랫폼 무관 호스트 드라이버.
- **(사실)** 막힌 자리가 CC33xx 통신이 아니라 부트 플래시 → CC33xx 동작 자체의 불가 근거는 아직 없음.
- **(모름)** WiFi/BLE 실제 link-up은 Flash_open(S3) 통과 후에야 검증 가능 → 지금은 미증명.

---

## 3. 보드 연결 방법 (하드웨어 인터페이스)

> SoC 측 핀(syscfg 기준). BoosterPack 헤더(J1~J4) ↔ SoC 핀 물리 대응표는 **미확인(모름)**.

| 인터페이스 | SoC 측 | 용도 |
|-----------|--------|------|
| MCSPI (host SPI) | `SPI0` (CLK/D0/D1/CS0), 20 MHz, EDMA | host ↔ CC33xx 명령/데이터 |
| GPIO out | WLAN_EN = `PR0_PRU0_GPIO12` | CC33xx enable |
| GPIO in (IRQ) | WLAN_IRQ = `PR0_PRU0_GPIO10`, RISE_EDGE | CC33xx → host 인터럽트 |
| UART (BLE HCI) | `USART2`, 9600 | BLE HCI 전송 |
| UART (console) | `USART0`, 115200 | 진단 로그/터미널 |
| OSPI | 0x53808000, IS25LX256 | **AM263P 부트 플래시(BoosterPack 아님)** |

- **(사실)** OSPI는 BoosterPack과 무관 — AM263P LaunchPad 온보드 부트 플래시. CC33xx와 별개 버스.
- **(사실)** SW1: DevBoot=1,1,0,0 / OSPI 4S Quad=1,1,1,1 (부트 모드 선택).
- 핀 매핑 원본·BoosterPack 헤더 정보는 → [[bp_cc3351_evm_ug]] / [[cc3351_datasheet]]

---

## 4. 포팅 단계 전체 구조

```
[S0] AM263P 마이그레이션 ─┐
[S1] 빌드 + 플래시 경로   ─┤ (완료)
[S2] 부팅 + 진단 출력     ─┘
        ▼
[S3] 부트 플래시 Flash_open 통과  ◄── ★ 현재 막힘 (Round 24+)
        ▼
[S4] Drivers_open / Board_open 완주
        ▼
[S5] CC33xx 펌웨어 로드 + WiFi 프로세서 기동
        ▼
[S6] SPI/IRQ link-up — host ↔ CC33xx 통신
        ▼
[S7] network_terminal CLI (scan/connect)
        ▼
[S8] BLE 경로 검증 (HCI UART)
```

| 단계 | 달성 목표 | 완료 기준 | 상태 |
|------|-----------|-----------|------|
| **S0** | syscfg를 AM243→AM263P 디바이스로 전환 | `AM263Px` 빌드 성공 | ✓ (사실) |
| **S1** | MCELF 빌드 + JTAG 6작업 플래시 | flasher 6작업 전부 성공 | ✓ (사실, R10) |
| **S2** | 부팅 후 UART 진단 마커 수신 | `[DIAG] A..G` 출력 | ✓ (사실) |
| **S3** | app `Flash_open()` 유효 핸들 반환 | `gFlashHandle[0] != NULL`, RDID 정상 | ✗ **막힘** (R7~R24) |
| **S4** | EDMA/OSPI/UART 재오픈 완주 | `Board_driversOpen` 무에러 | ✗ (S3의 2차 결과) |
| **S5** | CC33xx FW 로드 + NP 기동 | NP up, 배너 출력 | ? 미도달 |
| **S6** | SPI transfer + WLAN_IRQ link-up | `wlan_start` 성공 | ? 미도달 |
| **S7** | CLI scan/connect 동작 | `wlan_scan` 결과 출력 | ? 미도달 |
| **S8** | BLE HCI 경로 동작 | `ble_start` 성공 | ? 미도달 |

> **(가설)** S3 블로커가 진짜 부트 정합성 문제인지, 진단 코드 부수효과인지는 R25 결과로 갈림.
> S4 이후 난이도는 S3 해소 방식에 종속 → [추정] 영역.

---

## 5. 현재 어디인가 — S3 (Flash_open 통과) 막힘

> 라운드별 실측·다음 액션은 [[status]] 에서 추적. 여기는 블로커 요지만.

**막힌 문제 (사실)**:
- app `Flash_open(IS25LX256)`이 **NULL 반환** (hang은 아님 — R13 `dummyClksCmd=8`로 해소).
- SDK 마커: SetProtocol/SetAddressBytes/SetModeDummy = SUCCESS, **SetRdCap(RdDataCapture sweep) = FAILURE**.
- 핵심 진단(R20): 8D RDID 응답이 **DQ1 한 라인만 활성** → "chip이 8D DDR에 있다"는 R7~R19 전제가 깨짐.
- R21/R22/R24: 1S RDID=`FF FF FF FF`, 8D RDID=`00 00 00 00` — 어느 프로토콜에서도 유효 RDID 없음.

**확정 사실 (재현 방지)**:
- E9(0x66/0x99) 소프트리셋은 Flash_open 경로에서 금지(SetProtocol st=-1 유발).
- `dummyClksCmd=8`, `quirksFxn=NULL` 필수 (런타임 패치 `cc3351/main.c:211-213`). → dummy 값 근거는 [[xspi_dummy_cycles]]
- Flash_open 단계별 시퀀스·종료 시 chip 상태는 → [[flash_open_sequence]]

**모름 / 미확인**:
- chip이 현재 1S인지 / reset됐는지 / 8D인데 PHY 문제인지 (가지 α/β/γ).
- `READ_DATA_CAPTURE_REG.DQS_ENABLE=0`으로 STIG RDID 재발행 시 응답 살아오는가 — **R25 검증 예정**.
- SBL이 애초에 chip을 8D로 두는가 (가지 α).
- BoosterPack 헤더 ↔ SoC 핀 물리 대응표.

---

## 6. 앞으로 얼마나 남았는가

> **전체 완료 기간은 추정 불가에 가깝다.** S3가 24라운드째 미해소이고 근본 원인 가설이 여러 갈래.

| 단계 | 난이도 | 기간 추정 | 비고 |
|------|--------|-----------|------|
| **S3 해소** | 높음~매우높음 | **추정 불가** (며칠~수주) | 최악의 경우 logic analyzer 등 외부 계측 필요 |
| S4 | 중 [추정] | 1~3일 [추정] | S3 통과하면 대체로 따라옴 |
| S5 (FW 로드/기동) | 중~높음 [추정] | 수일~1주+ [추정] | 미탐색 영역 |
| S6 (SPI link-up) | 중~높음 [추정] | 수일~1주+ [추정] | SPI 타이밍/IRQ 실측 필요 |
| S7 (CLI/WiFi) | 중 [추정] | 수일 [추정] | host 드라이버는 SDK 제공 |
| S8 (BLE) | 중 [추정] | 수일 [추정] | WiFi와 독립 검증 가능 |

- **낙관(가설)**: S3가 R25/R26에서 풀리면 이후 S4~S8 약 **2~4주** [추정].
- **현실**: S3 미해소 지속 시 전체 일정 **추정 불가**.
- **권고**: 기간을 단일 숫자로 약속하지 말 것. "S3 해소 여부"를 첫 게이트로, 통과 후 S4~S8 재추정.

---

## 7. 환원 후보 (wiki ↔ 코드 어긋남)

코드/관찰이 wiki를 앞질렀거나 어긋난 자리 — concept 페이지 환원 대상:

1. [[sbl_app_flash_handoff]] 후보 1은 "SBL이 chip을 8D로 둔다" 가정만 다룸. **R20 증거(DQ1-only)는 가지 α(SBL이 8D로 안 둠)를 시사** → 미반영.
2. [[sbl_app_flash_handoff]] "후보 3 DQS 모드 불일치"는 indirect 경로 관점. R24는 **STIG path에서 DQS_ENABLE 효과 미확인**으로 분리 필요.
3. descriptor `dummyClksRd=16`(ECC OFF)과 런타임 패치 `dummyClksCmd=8`(R13)의 관계 → [[xspi_dummy_cycles]]에 명시 필요.
4. [[is25lx256_vs_spansion_quirks]]에 "AM243=Quad / AM263P=Octal" 라인 수 차이 미반영 → 추가 필요. (AM243 칩 `S25HL512T` 확정으로 Spansion-quirk 전제는 사실로 뒷받침됨)
5. **`flashFixUpOspiBoot()` 부재 — app vs flasher 비대칭.** flasher는 `Flash_open` 전 이 함수(1S SDR 리셋)를 호출하나 app `main.c`엔 없음. TI E2E #1379297·#1534082에서 동일 패턴 보고 → [[sbl_app_flash_handoff]]에 추가 필요.
