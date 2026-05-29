---
tags: [concept, flash, ospi, sbl, handoff, am263p, ti_mcupsdk, porting]
source: [[mcupsdk_flash_nor_ospi]] (skipHwInit references) + report.md R25~R27
date: 2026-05-29
---

# SBL → 앱 flash 핸드오프 — `skipHwInit` 계약

AM263P 부트 흐름에서 SBL이 OSPI flash를 8D DDR로 올린 뒤 앱으로 점프하면, 앱도 자기 `Flash_open()`을 호출한다. 이 두 번째 Open은 flash chip을 **다시 초기화하면 안 된다** (chip은 이미 8D DDR 상태). 이걸 차단하는 게이트가 `config->skipHwInit` 플래그.

## 게이트 의미

`Flash_Config::skipHwInit` (boolean):
- `FALSE` (기본): chip register write 다 수행. cold boot 가정.
- `TRUE`: **flash chip register는 건드리지 않고, OSPI 컨트롤러만 재구성**. 앱이 SBL 뒤를 이어 받을 때 사용.

## `skipHwInit=TRUE`일 때 스킵되는 것 (전부 chip register 명령)

| 동작 | 라인 | 명령 / 효과 |
|---|---|---|
| QE bit set (1S_1S_4S, 4S_4S_4S, 4S_4D_4D) | 777, 805 | `Flash_setQeBit` |
| OE bit set (1S_1S_8S, 8S_8S_8S, 8D_8D_8D) | 790, 821 | `Flash_setOeBit` |
| 444 mode entry | 805 | `Flash_set444mode` (0x38 / 0x35 / register write) |
| 888 mode entry | 821 | `Flash_set888mode` (0xE8 / `cmdWren`+`0x72` register) |
| Dummy register write | 527 | `Flash_norOspiSetRegCfg(dummyCfg)` (NVCR/VCR `0x01h` for ISSI) |
| 4B addr enable 명령 (`0xB7`) | 260, 265 | non-WREN / WREN 두 variant |

## `skipHwInit=TRUE`라도 *실행되는* 것 (전부 OSPI 컨트롤러 레지스터)

| 동작 | 라인 | 의미 |
|---|---|---|
| `OSPI_setDeviceSize(page, block)` | 1212 | 컨트롤러가 알아야 하는 메모리 geometry |
| `OSPI_setCmdExtType(cmdExtType)` | 1215 | 8D 명령 확장 인코딩 (`repeat`/`invert`/`none`) |
| `OSPI_setProtocol(8D_8D_8D)` | 840 | 컨트롤러 측 protocol register |
| `OSPI_setNumAddrBytes(4)` | 323 | 컨트롤러가 명령 byte 개수 셋 |
| `OSPI_setXferOpCodes(cmdRd, cmdWr)` | 1238 | 컨트롤러에 read/write opcode 셋 |
| `OSPI_setReadDummyCycles(dummyClksRd)` | 523 | **컨트롤러 측** dummy cycles |
| `OSPI_setCmdDummyCycles(dummyClksCmd)` | 524 | 컨트롤러 측 cmd dummy cycles |
| `OSPI_enableModeBitsCmd/Read`, `OSPI_setModeBits` | 513-521 | 컨트롤러 mode bits |
| Capture delay sweep (ID read) | 1247-1255 | 보드 trace delay 흡수 |
| PHY tune (옵션) | 1259-1339 | DDR PHY tuning |

핵심: **앱은 OSPI 컨트롤러를 SBL과 동일 파라미터로 *재구성*하지만, chip 측은 건드리지 않는다.** 따라서 양쪽 `Flash_DevConfig`가 *bit-exact 일치*해야 함.

## 정합성이 깨질 수 있는 지점

### 1. Dummy cycle 불일치 (가장 흔함)

SBL이 chip NVCR `0x01h`에 박은 값(예: ISSI `0x12` = 16 cycles)과 앱이 `OSPI_setReadDummyCycles`로 컨트롤러에 넣는 값이 다르면:
- 컨트롤러는 자기가 가진 dummy로 명령 송신
- chip은 자기 NVCR에 따라 응답
- 데이터 잘림 / shift / 0xFF
- **capture delay sweep으로 보정 안 됨** (capture delay는 phase 보정용이지 cycle count 보정 아님)

→ 진단: `OSPI_phyReadAttackVector` 또는 ID read 시 데이터 패턴이 일정 bit shift된 모양이면 의심.

### 2. Capture delay sweep이 컨트롤러 상태를 바꾼다

Open 종료 시 컨트롤러의 `readDataCaptureDelay`는 *마지막으로 ID read가 통과한 값*. SBL이 PHY 켜고 종료했다면 SBL의 capture delay가 박혀 있고, 앱이 PHY 안 켜면 sweep으로 덮어쓴다. PHY 비활성 운용 시엔 capture delay 값이 *runtime마다 다를 수 있다*.

### 3. PHY attack vector 자동 write

`skipHwInit=TRUE`라도 PHY 경로는 그대로 탄다 (line 1259-1339 전체에 `skipHwInit` 가드 없음). attack vector가 flash에 없으면 *마지막 sector를 erase+write*. SBL이 attack vector를 이미 써놓았어야 안전.

### 4. RDID 전용 dummy 필드(`idCfg.dummy8`) 불일치

`Flash_norOspiReadId`(line 847-913)는 STIG dummy를 **controller register에서 inherit 하지 않고** 자체적으로 결정:

- non-8D 경로: literal `0`
- 8D-8D-8D 경로: `devCfg->idCfg.dummy8` (device descriptor의 별도 필드)

→ `protocolCfg.dummyClksCmd`가 SBL과 앱에서 일치하더라도, **`idCfg.dummy8`이 어긋나면 앱의 capture delay sweep loop가 통째로 실패**한다. SBL이 chip 측을 정상으로 남겨놨더라도 앱 descriptor의 idCfg.dummy8이 datasheet 값과 다르면 Open이 RDID에서 죽음.

상세: [[flash_open_sequence]] §RDID dummy resolution.

진단 시 dump 대상 필드에 `idCfg.dummy8` 추가 필수 — 일반 dummy 필드만 비교하면 이 케이스를 놓침.

### 5. `obj->currentProtocol = 1S_1S_1S` 초기 가정 (line 1228)

이건 `skipHwInit`와 무관하게 항상 실행. 드라이버 객체의 트래킹 변수만 1S로 초기화되고 직후 `Flash_norOspiSetProtocol`이 8D로 갱신 (line 1232). chip에는 명령 안 나감 (`skipHwInit=TRUE`이면 OE/888 명령 스킵). 단, 만약 protocol switch 단계에서 *어떤 이유로든* chip에 명령을 보내야 한다면 1S 가정으로 보내므로 chip이 8D에 있으면 실패.

## `flashFixUpOspiBoot()` 부재 — app vs flasher 비대칭 (핵심)

같은 보드·같은 칩·같은 SDK `Flash_open(IS25LX256)` 경로인데 **jtag_flasher에서는 성공(R10), app(cc3351)에서는 NULL**이다. 결정적 차이:

- **jtag_flasher**: `Flash_open` *전에* `flashFixUpOspiBoot()`(`jtag_flasher/main.c:414`)를 호출해 **OSPI RESET 핀을 HW 토글 → chip을 1S SDR known-state로 되돌린 뒤** `skipHwInit=FALSE`로 연다 → `set888mode`(0x81)가 1S→8D 정상 승격.
- **app cc3351**: `cc3351/main.c`에 `board_flash_reset`/`flashFixUpOspiBoot` 호출이 **전혀 없음**. SBL이 남긴 8D 잔여 상태 위에서 곧장 `Flash_open` → 위 후보1 증상.

이것이 app vs flasher 비대칭의 **단일 최대 원인**. ROM 부팅(flasher, 잔여 상태 없음)에서는 1S→8D 승격이 정상 동작한다는 대조 증거이기도 하다.

TI E2E에서 동일 패턴 보고: SBL이 Octal DDR 플래시를 리셋 없이 넘기면 다음 단계 `Flash_open`/RDID가 실패하며, `flashFixUpOspiBoot()`(1S 리셋 후 재진입)가 표준 해법 — [#1379297](https://e2e.ti.com/support/microcontrollers/arm-based-microcontrollers-group/arm-based-microcontrollers/f/arm-based-microcontrollers-forum/1379297/mcu-plus-sdk-am243x-flash-protocol-changes), [#1534082](https://e2e.ti.com/support/microcontrollers/arm-based-microcontrollers-group/arm-based-microcontrollers/f/arm-based-microcontrollers-forum/1534082/mcu-plus-sdk-am263x-rom-bootloader-behavior-and-ospi).

→ **R28 해법 후보**: 이 함수를 app에 인라인 재현. 진행 상태는 [[flash_open_diagnostic_log]] §다음(R28 계획).

## 미해결 질문 — SBL이 chip을 어느 프로토콜로 넘기는가 (가지 α)

SW1="OSPI 4S Quad Read(1,1,1,1)" 부팅 시 SBL이 chip을 8D로 두는지, Quad로 두는지, 1S로 두는지 **미확인**. R20의 DQ1-only는 "SBL이 애초에 8D로 안 둔다"(가지 α)를 시사할 수 있다. SBL 소스 또는 TRM OSPI boot 절차에서 확인 필요. → [[flash_open_facts]] 모름/미확인.

## 권장 진단 절차

앱에서 Flash_open 실패 / 깨진 read 발생 시:

1. **앱과 SBL의 `Flash_DevConfig`가 같은 객체 / 같은 빌드 산출물에서 오는지** 확인 (가장 흔한 트랩)
2. `dummyClksRd`, `dummyClksCmd`, **`idCfg.dummy8`**, `modeClksRd`, `cmdRd`, `cmdWr`, `protocol`, `cmdExtType`, `addrByteSupport`, `enable4BAddr` — 양쪽 값 dump하여 비교. **`idCfg.dummy8`을 빼먹지 말 것** (8D ReadId 전용 별도 필드, §4)
3. PHY 사용 여부 일치 확인. SBL은 PHY ON, 앱은 OFF면 capture delay sweep만으로 ID read 통과해야 함 (가능하지만 timing margin 낮음)
4. chip NVCR/VCR 실제 값을 1S_1S_1S로 복귀 후 dump (방법: 강제로 `Flash_norOspiReset` 호출 → 1S 복귀 → register read). 컨트롤러 측 설정 값과 대조
5. attack vector sector가 *예상치 못한 데이터*로 덮였는지 확인 (PHY 자동 write 의심)

## 진단 트리 — `Flash_norOspiOpen`이 capture delay sweep loop에서 실패할 때

증상: `Flash_norOspiOpen`이 line 1247-1255 loop를 모두 돌아도 `Flash_norOspiReadId`가 한 번도 성공 못 함.

### 먼저 — IS25LX256 device descriptor는 의심하지 마라

`source/sysconfig/board/.meta/flash/IS25LX256.json` (SDK installer 동봉, GitHub public 미러에는 **미공개**) 검증 완료 (2026-05-22):

| 필드 | JSON 값 | datasheet 일치? |
|---|---|---|
| `rdIdSettings.cmd` | `0x9F` | ✓ |
| `rdIdSettings.dummy8` | **`8`** | ✓ (ch08 Table 8.1: 8D-8D-8D RDID dummy=8) |
| `rdIdSettings.addressBytesSize` | `0` | ✓ |
| `p888d.protoCfg.bitP` | **`231` (0xE7)** | ✓ (ch06.5 VCR 0x00: E7h=Octal DDR with DQS) |
| `p888d.dummyCfg.bitP` | **`16`** | ✓ (ch06.5 VCR 0x01: 16 cycles for ≤162MHz ECC OFF) |
| `p888d.cmdRd/cmdWr` | `0x7C/0x84` | ✓ (Table 8.1, Octal DDR에서 사용 가능) |
| `flashManfId` | `0x9D` | ✓ (ISSI) |
| `flashDeviceId` | `0x5A19` | ✓ |

raw 사본: `teams/g/lp-am263p/raw/mcupsdk/source/sysconfig/board/.meta/flash/IS25LX256.json` (SDK 버전 `mcu_plus_sdk_am263px_26_00_00_01`)

→ **descriptor는 정상**. sweep 실패의 원인은 다른 곳.

### 원인 후보 (가능성 순)

#### 후보 1. Chip이 8D mode로 진입 못 했다

증상: ReadId STIG가 dummy=8(idCfg.dummy8)로 정상 송신되지만 chip이 0xFF만 반환. capture delay 어떤 값에서도 같은 패턴.

원인:
- SBL이 chip을 이미 8D로 남겼는데 앱이 `skipHwInit=FALSE`로 `Flash_open` → 드라이버는 line 1228에서 `currentProtocol=1S_1S_1S` 가정 → `Flash_set888mode`가 VCR write 명령(0x81, addr=0x00, data=0xE7)을 1S 프로토콜로 송신 → chip은 8D니까 명령 디코드 실패 → chip은 여전히 8D, host는 8D로 ReadId 보내지만 chip은 그 사이 standby 상태로 들어가 있을 수 있음
- 또는 cold boot인데 VCR write가 성공하지 못한 경우 (WEL이 안 셋되어 있다거나, 명령 시퀀스 깨짐)

검증:
1. AM263P xSPI 핀에 logic analyzer 부착 후 Open 진입 직후 0x06(WREN) → 0x81 0x00..00 0xE7 시퀀스가 보이는지 확인
2. 안 보이면 → `obj->currentProtocol` 초기값 문제 또는 SBL→앱 핸드오프 미스
3. 보이지만 다음 ReadId가 실패 → chip 측 VCR이 실제로 0xE7로 안 바뀜. logic analyzer로 READ VCR(0x85, addr=0x00) 시퀀스를 1S로 직접 발행하여 확인 (`Flash_norOspiReset` 호출하여 1S 복귀 후)

해결: 앱 측 `Flash_open` 호출 시 `skipHwInit=TRUE`. §1-5의 모든 게이트 동작.

> **R25~R27 실측 갱신 (2026-05-29)** — `skipHwInit=TRUE`만으로는 부족함이 드러남:
> - SBL 잔여 상태에서 **1S RDID 무응답(항상 `FF`)**, 8D RDID는 **DQ1-only**(`02 03 03 03`) — R20·R25·R27 독립 재확인.
> - `READ_DATA_CAPTURE_REG=0x00000121`로 SBL이 PHY/DQS 켜고 delay=1로 넘긴 상태 확인.
> - 즉 chip이 SBL 잔여 8D에 있고 app이 그 위에서 캡처 delay만 맞추려다 실패. 현재 최유력 해법은 `skipHwInit=TRUE` 단독이 아니라 **flasher 성공 공식(아래 절)**으로 chip을 1S로 되돌린 뒤 `skipHwInit=FALSE`로 정상 승격. 확정/폐기 가설은 [[flash_open_facts]].

#### 후보 2. `Flash_quirkSpansionUNHYSADisable`가 호출되어 bus 상태 망가뜨림

증상: 8D 진입은 성공한 것 같은데 (logic analyzer로 VCR write 확인됨) 그 직후 ReadId 실패. logic analyzer에서 **0x65 또는 0x71 opcode**가 잡힘.

원인: SysConfig output (`ti_board_open_close.c`)이 IS25LX256에 quirksFxn pointer를 `Flash_quirkSpansionUNHYSADisable`로 자동 매핑. 이 함수가 8D bus에 Spansion RDAR(0x65)/WRAR(0x71) 송신 → ISSI 미정의 → standby → 이후 ReadId 깨짐.

검증: `ti_board_open_close.c`에서 `params.quirksFxn` 또는 `gFlashConfig_*.flashOpenParams.quirksFxn` 값 확인. NULL이거나 ISSI 전용 함수여야 함.

해결: [[is25lx256_vs_spansion_quirks]] §6.5 워크어라운드.

#### 후보 3. DQS 모드 불일치

증상: 8D 진입 성공, ReadId가 매번 같은 값 반환하지만 데이터가 깨짐 (예: 4 byte 모두 동일).

원인: JSON `p888d.protoCfg.bitP=231(0xE7)`이므로 chip은 **DQS enabled** Octal DDR. AM263P OSPI 컨트롤러도 DQS read enable 돼야 데이터 캡처 가능. SysConfig OSPI Module에서 "Enable DQS"가 꺼져 있으면 데이터 캡처 phase가 자유롭게 떠다님 → capture delay sweep으로 우연히 맞을 수도, 영원히 안 맞을 수도.

검증: SysConfig OSPI Module 설정에서 PHY/DQS 관련 옵션 확인. 또는 OSPI 컨트롤러 register dump (DQS_CONFIG_REG 류).

해결: OSPI Module의 DQS enable 켜기. 또는 (드물게) JSON을 fork하여 0xC7 (DQS 없는 Octal DDR)로 변경.

> **R26 검증 (2026-05-29)** — 경로 구분 주의: 본 후보3은 *indirect read 경로* 관점이었으나, **STIG 경로**에서 `READ_DATA_CAPTURE_REG.DQS_ENABLE=0`으로 클리어하면 8D DDR 캡처가 **전부 FF**가 됨(SetRdCap st=-1). 즉 **8D DDR엔 DQS 필수 — "DQS를 꺼서 캡처를 살린다"는 방향은 반증됨(폐기 가설)**. 켜는 방향만 유효. [[flash_open_facts]] 폐기 가설 참조.

#### 후보 4. (드뭄) ECC ON 상태인데 dummy cycle table 불일치

증상: 위 세 후보 모두 배제, 그러나 ReadId 데이터가 일정 cycle 만큼 shift된 패턴.

원인: IS25LX256 default는 ECC OFF (VCR 0x0B bit 0 = 1). 어떤 이유로 ECC가 ON이면 datasheet ch06.5 Table 6.7의 ECC ON 컬럼 사용 → 같은 클럭에서 더 많은 dummy 필요. 그런데 JSON `dummyClksRd=16`은 ECC OFF 기준.

검증: chip VCR 0x0B (또는 NVCR 0x0B) bit 0 dump.

해결: ECC OFF로 되돌리거나 JSON dummy 값 조정.

### 진단 시 dump해야 할 것 (요약)

1. `Flash_DevConfig` 필드 — 위 §"권장 진단 절차" 2번. **`idCfg.dummy8` 빼먹지 말 것**
2. `params.quirksFxn` — NULL이어야 함 (후보 2)
3. AM263P xSPI 핀 logic analyzer trace — Open 진입~ReadId 첫 시도까지 (후보 1, 2, 3 모두 진단)
4. Chip VCR 0x00, 0x01, 0x0B 실제 값 (1S 복귀 후 read) — 후보 1, 4 진단
5. SysConfig OSPI Module DQS 설정 — 후보 3

## 함께 보기

- 확정 사실/폐기 가설 원장: [[flash_open_facts]] · 라운드별 진단 로그: [[flash_open_diagnostic_log]]
- Open 시퀀스 전체: [[flash_open_sequence]]
- Dummy cycle vs 클럭 주파수 표: [[xspi_dummy_cycles]]
- 원본 소스: [[mcupsdk_flash_nor_ospi]]
- Spansion → ISSI 포팅 시 주의: [[is25lx256_vs_spansion_quirks]]
- IS25LX256 데이터시트 ch06.5 (VCR) / ch08 (Command Table): [[is25lx256_datasheet]]
