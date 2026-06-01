---
tags: [roadmap, porting, living-doc]
source: [[/c/Users/echog/eta/projects/g/lp-am263p/bp-3351/tasks/porting/roadmap.md]] (ingest, 2026-06-01 개정)
date: 2026-06-01
---

# porting — LP-AM243 → LP-AM263P 포팅 작업 호 (S0~S8)

> 작업 단위 호. 단계 spine·현재 위치·남은 일정만 둔다.
> 깊은 디테일(칩 차이·플래시 핸드오프·dummy cycle·하드웨어 핀맵)은 concept/entity 백링크와 프로젝트 [[CLAUDE]]로 위임.
> 기능별 구현 현황·다음 시작점은 [[status]], 확정 사실/폐기 가설은 [[flash_open_facts]], 라운드별 진단 history는 [[flash_open_diagnostic_log]]가 단일 소스 — 여기서는 위임만 한다.
> **사실 / 가설 / 모름을 구분한다. 추정은 "[추정]" 표기.**

상위 프로젝트 호는 [[roadmap]].

---

## 0. 한 줄 요약

LP-AM243 공식 예제(`CC3xx_thick_mac_network_terminal`)를 **LP-AM263P + BP-CC3351**로 옮기는 **비공식 포팅**(CC33XX SDK R8.1은 AM263P 예제·syscfg 미제공). 빌드/플래시/부팅까지 동작하나, **부팅 직후 app의 `Flash_open()`(AM263P 부트 플래시 IS25LX256)이 NULL 반환**하는 단계(S3)에서 막혀 있음(Round 27+).

- **비유**: USB(부트 플래시)에 부팅 파일 일체를 굽고 → 전원 켜면 SBL·app 커널까지 RAM에 올라오나 → RAM에서 도는 커널이 "방금 자기를 띄운 그 USB"를 다시 직접 인식(`Flash_open`)하지 못하는 상황. 즉 *플랫폼 부트/플래시 서브시스템* 문제로, CC33xx WiFi/BLE 동작과는 별개.
- **타당성 (가설)**: CC33xx host 인터페이스는 표준 MCSPI+GPIO(EN/IRQ)+BLE UART라 AM263P에서 **불가 판정 근거는 없음** — 단 WiFi/BLE link-up은 S3 통과 후에야 검증 가능하므로 **미증명**. 칩 차이·왜 AM243 흐름을 그대로 못 옮기는지는 → [[is25lx256_vs_spansion_quirks]].

---

## 1. 마일스톤 호 (S0~S8)

```
[S0] AM263P 마이그레이션 ─┐
[S1] 빌드 + 플래시 경로   ─┤ (완료)
[S2] 부팅 + 진단 출력     ─┘
        ▼
[S3] 부트 플래시 Flash_open 통과  ◄── ★ 현재 막힘 (Round 27+)
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
| **S3** | app `Flash_open()` 유효 핸들 반환 | `gFlashHandle[0] != NULL`, RDID 정상 | ✗ **막힘** (R7~R27) |
| **S4** | EDMA/OSPI/UART 재오픈 완주 | `Board_driversOpen` 무에러 | ✗ (S3의 2차 결과) |
| **S5** | CC33xx FW 로드 + NP 기동 | NP up, 배너 출력 | ? 미도달 |
| **S6** | SPI transfer + WLAN_IRQ link-up | `wlan_start` 성공 | ? 미도달 |
| **S7** | CLI scan/connect 동작 | `wlan_scan` 결과 출력 | ? 미도달 |
| **S8** | BLE HCI 경로 동작 | `ble_start` 성공 | ? 미도달 |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현 ([[status]]와 동일).

- **왜 S3에서 막히나 (배경)**: AM243 부트 플래시는 **S25HL512T(Quad-SPI 중심)**, AM263P는 **IS25LX256(Octal xSPI 8D DDR native)** — 라인 수·프로토콜 진입 시퀀스·RDID 응답 폭·레지스터 opcode가 전부 다르다. 비교표·Spansion quirk 제거 체크리스트는 → [[is25lx256_vs_spansion_quirks]].
- **(가설)** 칩 차이는 "왜 AM243 흐름을 그대로 옮기면 안 되는가"는 잘 설명하나, S3 블로커의 *직접 트리거*가 (a) SBL↔app 프로토콜 핸드오프인지 (b) RDCAP/PHY 타이밍인지 (c) DQS/캡처 설정인지는 미확정. 핸드오프 정합 깨짐 지점·`flashFixUpOspiBoot` 비대칭은 → [[sbl_app_flash_handoff]].
- **하드웨어 인터페이스**(MCSPI `SPI0`/WLAN_EN·IRQ GPIO/BLE·console UART/OSPI 부트 플래시)는 프로젝트 [[CLAUDE]] "하드웨어" 절이 단일 소스. BoosterPack 헤더(J1~J4)↔SoC 핀 물리 대응표는 **미확인**, 원본 핀맵은 → [[bp_cc3351_evm_ug]] / [[cc3351_datasheet]].

---

## 2. 현재 위치 — S3 (Flash_open 통과) 막힘

> 라운드별 실측·다음 시작점은 [[status]], 확정 사실/폐기 가설은 [[flash_open_facts]], 시간순 진단 history는 [[flash_open_diagnostic_log]]. 여기는 블로커 요지만.

**막힌 문제 (사실)**:
- app `Flash_open(IS25LX256)`이 **NULL 반환** (hang은 아님 — R13 `dummyClksCmd=8`로 해소). SDK 마커: SetProtocol/SetAddressBytes/SetModeDummy = SUCCESS, **SetRdCap = FAILURE**.
- 8D RDID 응답이 **DQ1 한 라인만 활성**(DQ1-only) — R20·R25·R27 독립 재확인된 사실. "chip이 8D DDR에 있다"는 R7~R19 전제는 깨짐.

**현재 최유력 가설(미채택)**: chip은 SBL 잔여 8D, app `Flash_open(skipHwInit=TRUE)`이 8D 가정 캡처만 시도 → DQ1-only 반환 → SetRdCap 실패. → 다음 라운드(R28)에서 jtag_flasher 성공 공식(`flashFixUpOspiBoot` 인라인 + `skipHwInit=FALSE`) 이식으로 검증. 상세·다음 시작점은 [[status]] / [[flash_open_facts]] / [[flash_open_diagnostic_log]].

**모름 / 미확인** (전체 목록은 [[status]] 미결 사항):
- chip이 현재 1S인지 / reset됐는지 / 8D인데 PHY 문제인지 (가지 α/β/γ).
- SBL이 SW1=4S Quad 부팅 시 chip을 어느 프로토콜로 app에 넘기는가.
- cc3351 syscfg에 OSPI reset 핀 부재 — R28 선행 확인 항목.

---

## 3. 남은 일정

> **S3 해소가 첫 게이트.** S3가 27라운드째 미해소이고 근본 원인 가설이 여러 갈래라 *S3 자체의 해소 시점이 불확실*하다. S4 이후는 S3 통과 후에야 실측 가능 → **단일 숫자로 기간을 약속하지 말 것.**

| 단계 | 난이도 | 기간 | 비고 |
|------|--------|------|------|
| **S3 해소** | 높음~매우높음 | **추정 불가** | R25·R26 두 진단 가설 소진. 최악의 경우 logic analyzer 등 외부 계측 필요 |
| S4~S8 | — | **S3 통과 후 재추정** | 미도달 영역 — S3 해소 방식에 종속되어 지금 등급/기간 추정은 정보 가치 없음 |

- **게이트 운용**: "S3 해소 여부"를 첫 게이트로 두고, 통과 후 S4(드라이버 재오픈)→S5(FW 로드/기동)→S6(SPI/IRQ link-up)→S7(CLI/WiFi)→S8(BLE)을 순차 재추정한다. S8(BLE)은 WiFi와 독립 검증 가능.

---

## 4. 환원 후보 (wiki ↔ 코드 어긋남)

- **(미해소)** descriptor `dummyClksRd=16`(ECC OFF)과 런타임 패치 `dummyClksCmd=8`(R13)의 관계 → [[xspi_dummy_cycles]]에 명시 필요.
- 그 외 후보(SBL 잔여 8D / DQS 필수·DQS=0 반증 / set888mode=0x81 정정 / `flashFixUpOspiBoot` 비대칭)는 2026-05-29 [[flash_open_facts]] · [[sbl_app_flash_handoff]] · [[is25lx256_vs_spansion_quirks]]에 반영 완료.
