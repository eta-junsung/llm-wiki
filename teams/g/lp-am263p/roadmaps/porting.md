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
| **S3** | app `Flash_open()` 유효 핸들 반환 | `gFlashHandle[0] != NULL`, RDID 정상 | ✓ (R28b, pinmux `$assign` 교정) |
| **S4** | EDMA/OSPI/UART 재오픈 완주 | `Board_driversOpen` 무에러 | ✓ (R31, in-place 패치+원본 구조 복원) |
| **S5** | CC33xx FW 로드 + NP 기동 | NP up, 배너 출력 | △ (`Hardware init DONE!` 출력, device info 읽기서 SPI 무응답) |
| **S6** | SPI transfer + WLAN_IRQ link-up | `wlan_start` 성공 | ✗ **막힘** (`SPI not responsive!`, `CMD_ERR_TIMEOUT` R32 실측) |
| **S7** | CLI scan/connect 동작 | `wlan_scan` 결과 출력 | ✗ (S6의 2차 결과) |
| **S8** | BLE HCI 경로 동작 | `ble_start` 성공 | ? 미도달 |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현 ([[status]]와 동일).

- **S3 막혔던 배경 (역사)**: AM243 부트 플래시는 **S25HL512T(Quad-SPI 중심)**, AM263P는 **IS25LX256(Octal xSPI 8D DDR native)** — 라인 수·프로토콜 진입 시퀀스·RDID 응답 폭·레지스터 opcode가 전부 다르다. 비교표·Spansion quirk 제거 체크리스트는 → [[is25lx256_vs_spansion_quirks]].
- **(R28 확정)** S3 블로커의 직접 트리거는 SBL-핸드오프/RDCAP-PHY가 아니라 **cc3351 `example.syscfg` OSPI pinmux 스크램블**(`$suggestSolution` → 7핀 오배치)이었음. R7~R27의 (a)(b)(c) 귀인 모두 "pinmux 정상" 잘못된 전제 위에 쌓인 것 → 폐기. 상세는 [[flash_open_facts]].
- **하드웨어 인터페이스**(MCSPI `SPI0`/WLAN_EN·IRQ GPIO/BLE·console UART/OSPI 부트 플래시)는 프로젝트 [[CLAUDE]] "하드웨어" 절이 단일 소스. BoosterPack 헤더(J1~J4)↔SoC 핀 물리 대응표는 **미확인**, 원본 핀맵은 → [[bp_cc3351_evm_ug]] / [[cc3351_datasheet]].

---

## 2. 현재 위치 — S7 (network_terminal CLI) 도달 중

> 라운드별 실측·다음 시작점은 [[status]], 확정 사실/폐기 가설은 [[flash_open_facts]], 시간순 진단 history는 [[flash_open_diagnostic_log]]. 여기는 요지만.

**S3 통과 (R28b 확정, 사실)**:
- cc3351 `example.syscfg` OSPI pinmux 스크램블(`$suggestSolution` → SysConfig 8핀 오배치)이 S3 블로커 근본 원인. `$assign`(hard lock) 교정 단독으로 RDID = `9D 5A 19` 정상 복귀, Flash_open OK. 커밋 bb56630.

**S4 통과 (R31 확정)**:
- `ti_board_open_close.c` 전역 in-place 패치(`quirksFxn=NULL`/`skipHwInit=TRUE`/`dummyClksCmd=8`) + freertos_main 원본 구조 복원. `Board_driversOpen` 완주, "Network Terminal upper_mac_3.0.5.12" 배너 + `user:` 프롬프트 도달. 커밋 3a06ab8.

**S5 부분 통과 (R32)**: heap 증설(256KB)로 `wlan_start` FreeRTOS assert 해소. `Hardware init DONE!` 출력됨. device info 읽기서 SPI 무응답 — S5 완료 기준(NP up) 미충족.

**S6 블로커 (R32)**: `SPI not responsive!` / `CMD_ERR_TIMEOUT` — AM263P ↔ CC33xx SPI 전송 링크 무응답. `spi_adapt.c`(MCSPI 래퍼), CS/IRQ 배선, NP 2nd 로더/FW 기동 여부 점검 필요.

**모름 / 미확인** (전체 목록은 [[status]] 미결 사항):
- SPI 링크 무응답 원인 미파악.
- flash FS 쓰기 미검증.
- BoosterPack 헤더(J1~J4) ↔ SoC 핀 물리 대응표 — 미확인.

---

## 3. 남은 일정

> **S7 wlan_scan 실측이 다음 게이트.** S3(R28b)·S4(R31) 통과. S5/S6/S7은 배너·프롬프트 도달로 추정. wlan_scan 미실측. S8은 독립 검증 가능(WiFi와 별도).

| 단계 | 난이도 | 기간 | 비고 |
|------|--------|------|------|
| ~~**S3 해소**~~ | ~~높음~매우높음~~ | ~~추정 불가~~ | ✓ R28b 통과 — pinmux `$assign` 교정 단독 해소 |
| ~~**S4 완주**~~ | ~~?~~ | ~~추정 불가~~ | ✓ R31 통과 — in-place 패치 + 원본 구조 복원 |
| **S7 완주** | ? | **wlan_scan 실측 후 추정** | CLI 프롬프트 도달, scan/connect 미실측 |
| S8 | — | **S7 통과 후 재추정** | BLE — WiFi와 독립 검증 가능 |

- **게이트 운용**: "S3 해소 여부"를 첫 게이트로 두고, 통과 후 S4(드라이버 재오픈)→S5(FW 로드/기동)→S6(SPI/IRQ link-up)→S7(CLI/WiFi)→S8(BLE)을 순차 재추정한다. S8(BLE)은 WiFi와 독립 검증 가능.

---

## 4. 환원 후보 (wiki ↔ 코드 어긋남)

- **(미해소)** descriptor `dummyClksRd=16`(ECC OFF)과 런타임 패치 `dummyClksCmd=8`(R13)의 관계 → [[xspi_dummy_cycles]]에 명시 필요.
- 그 외 후보(SBL 잔여 8D / DQS 필수·DQS=0 반증 / set888mode=0x81 정정 / `flashFixUpOspiBoot` 비대칭)는 2026-05-29 [[flash_open_facts]] · [[sbl_app_flash_handoff]] · [[is25lx256_vs_spansion_quirks]]에 반영 완료.
