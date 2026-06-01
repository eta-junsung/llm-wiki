---
tags: [concept, flash, ospi, facts, diagnosis, am263p, s3-blocker]
source: [[flash_open_diagnostic_log]] + report.md (R19~R27)
date: 2026-05-29
---

# Flash_open S3 블로커 — 사실 원장

> **증류된 "현재 진실".** 라운드별 시간순 서사는 [[flash_open_diagnostic_log]]에 있고, 여기는 그로부터 확정/폐기된 것만 짧게 모은다. 라운드마다 **제자리 수정**한다.
> 새 라운드 결과 반영 순서: ① log에 append → ② 여기 facts 갱신 → ③ [[status]] 위임 갱신(게이트 통과 시 [[porting]]/[[roadmap]]).

이 작업의 핵심 안티-맥락유실 장치는 아래 **"폐기된 가설"** 절이다. 새 라운드를 설계하기 전 반드시 먼저 읽어, 이미 죽은 길을 다시 파지 않는다.

---

## 확정 사실 (재현 방지)

| 사실 | 출처 |
|------|------|
| app `Flash_open(IS25LX256)`은 **NULL 반환** (hang 아님 — R13 `dummyClksCmd=8`로 hang 해소). SDK 마커: SetProtocol/SetAddressBytes/SetModeDummy = SUCCESS, **SetRdCap(RdDataCapture sweep) = FAILURE** | R13~, roadmap §5-2 |
| **DQ1-only 패턴** — 8D RDID 응답이 DQ1 한 라인만 활성(`02 03 03 03`), DQ[7:2]·DQ0 항상 0 | R20 최초, R25·R27 독립 재확인 → **사실 승격** |
| `READ_DATA_CAPTURE_REG = 0x00000121` = **SBL 잔여 상태** (DQS_ENABLE bit8=1, SAMPLE_EDGE bit5=1, delay=1) | R25/R26/R27 레지스터 덤프 |
| `set888mode` opcode = **`0x81`** (IS25LX256 VCR write, 정상) | R27, `flash_nor_ospi.c:664` |
| jtag_flasher 성공 공식 = `flashFixUpOspiBoot()`(OSPI RESET 핀 HW 토글 → 1S) + `skipHwInit=FALSE`(set888mode로 1S→8D 승격) | `jtag_flasher/main.c:414`, `ti_board_config.c:60` |
| cc3351 app에는 `board_flash_reset`/`flashFixUpOspiBoot` 호출이 **전무** → app vs flasher 비대칭의 **단일 최대 원인** | cc3351/main.c 직접 확인 |
| `dummyClksCmd=8`, `quirksFxn=NULL` 필수 (런타임 패치 `cc3351/main.c:211-213`) | 과거 라운드 확정 |
| E9 소프트리셋(`0x66`+`0x99`)은 Flash_open 경로에서 금지 — `SetProtocol st=-1` 유발 | 과거 라운드 확정 |
| 빌드/플래시/부팅/진단 경로는 안정 동작 | R10~ |

칩 클래스 차이(AM243 `S25HL512T` Quad vs AM263P `IS25LX256` Octal native)는 [[is25lx256_vs_spansion_quirks]], dummy 근거는 [[xspi_dummy_cycles]], Open 시퀀스는 [[flash_open_sequence]] 참조.

---

## 폐기된 가설 (재시도 금지)

| 폐기된 길 | 반증 | 라운드 |
|-----------|------|--------|
| `DQS_ENABLE=0` (READ_DATA_CAPTURE_REG 클리어)로 캡처 살리기 | DQS 없으면 8D DDR 캡처 **전부 FF** → SetRdCap st=-1. 8D DDR엔 DQS 필수 | **R26 반증** |
| `set888mode` opcode = `0x71` | 실제 `0x81`. `0x71`은 Spansion WRAR로 quirksFxn 경로 전용(이미 NULL 차단), set888mode와 무관 | **R27 폐기** |
| `skipHwInit=FALSE`로 진단 | SBL 잔여 상태에서 `set888mode` 쓰기 st=-1, status 누적 구조로 이후 단계 신호 오염 → 진단 라운드 자체가 무효 | **R25 폐기** |
| CONFIG_REG bit30 DUAL_BYTE_OPCODE_EN 잔류가 원인 | 이미 0임을 확인 | **R24 폐기** |
| RDCAP 레지스터 4조합(0x121·0x021·0x001·0x101) 튜닝으로 해결 | 전부 indirect sweep 실패 | R16~R19 |

---

## 현재 최유력 가설 (미채택)

> chip은 SBL이 남긴 **8D 상태**에 있다. app `Flash_open(skipHwInit=TRUE)`은 chip을 건드리지 않고 8D로 가정하여 RDID 캡처 타이밍(RDCAP delay) 최적화만 시도한다. 그러나 8D RDID가 DQ1-only를 돌려주므로 SetRdCap이 항상 실패한다.

DQ1-only의 원인은 미확정 — 두 갈래가 살아 있다:
- chip이 진짜 8D 응답하는데 DQ1만 잡히는 것(PHY/캡처 문제)인가?
- chip이 8D가 아닌 Quad 상태이고 DQ1이 그 Quad 응답의 잔상인가?

**해법 후보 (R28 예정)**: jtag_flasher 성공 공식 이식 — `board_flash_reset()`(OSPI RESET 핀 HW 토글 → chip 1S known-state) + `OSPI_enableSDR` + `OSPI_clearDualOpCodeMode` + `setProtocol(1,1,1,0)` → `skipHwInit=FALSE`로 `Flash_open`의 `set888mode`가 chip을 1S→8D 정상 승격. 계획 상세는 [[flash_open_diagnostic_log]] §다음.

---

## 모름 / 미확인

- chip이 현재 **1S인지 / reset됐는지 / 8D인데 PHY 문제인지** (가지 α/β/γ) — 미확정.
- SBL이 SW1="OSPI 4S Quad(1,1,1,1)" 부팅 시 chip을 **어느 프로토콜로 app에 넘기는가** (가지 α) — SBL 소스 또는 TRM OSPI boot 절차 확인 필요.
- cc3351 `example.syscfg`에 **OSPI reset 핀 설정 부재** — `board_flash_reset()` 생성 코드 유무를 jtag_flasher syscfg와 비교 필요 (R28 선행 조건).
- BoosterPack 헤더 ↔ SoC 핀 물리 대응표 — 미확인.

---

## 함께 보기

- 라운드별 시간순 기록: [[flash_open_diagnostic_log]]
- 전략 spine: [[roadmap]] · 다음 시작점/현황표: [[status]]
- SBL→app 핸드오프 계약: [[sbl_app_flash_handoff]]
- Spansion↔ISSI 포팅 차이: [[is25lx256_vs_spansion_quirks]]
- Open 시퀀스: [[flash_open_sequence]]
