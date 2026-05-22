---
tags: [concept, flash, ospi, sbl, handoff, am263p, ti_mcupsdk, porting]
source: [[mcupsdk_flash_nor_ospi]] (skipHwInit references)
date: 2026-05-22
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

### 4. `obj->currentProtocol = 1S_1S_1S` 초기 가정 (line 1228)

이건 `skipHwInit`와 무관하게 항상 실행. 드라이버 객체의 트래킹 변수만 1S로 초기화되고 직후 `Flash_norOspiSetProtocol`이 8D로 갱신 (line 1232). chip에는 명령 안 나감 (`skipHwInit=TRUE`이면 OE/888 명령 스킵). 단, 만약 protocol switch 단계에서 *어떤 이유로든* chip에 명령을 보내야 한다면 1S 가정으로 보내므로 chip이 8D에 있으면 실패.

## 권장 진단 절차

앱에서 Flash_open 실패 / 깨진 read 발생 시:

1. **앱과 SBL의 `Flash_DevConfig`가 같은 객체 / 같은 빌드 산출물에서 오는지** 확인 (가장 흔한 트랩)
2. `dummyClksRd`, `dummyClksCmd`, `modeClksRd`, `cmdRd`, `cmdWr`, `protocol`, `cmdExtType`, `addrByteSupport`, `enable4BAddr` — 양쪽 값 dump하여 비교
3. PHY 사용 여부 일치 확인. SBL은 PHY ON, 앱은 OFF면 capture delay sweep만으로 ID read 통과해야 함 (가능하지만 timing margin 낮음)
4. chip NVCR/VCR 실제 값을 1S_1S_1S로 복귀 후 dump (방법: 강제로 `Flash_norOspiReset` 호출 → 1S 복귀 → register read). 컨트롤러 측 설정 값과 대조
5. attack vector sector가 *예상치 못한 데이터*로 덮였는지 확인 (PHY 자동 write 의심)

## 함께 보기

- Open 시퀀스 전체: [[flash_open_sequence]]
- Dummy cycle vs 클럭 주파수 표: [[xspi_dummy_cycles]]
- 원본 소스: [[mcupsdk_flash_nor_ospi]]
- Spansion → ISSI 포팅 시 주의: [[is25lx256_vs_spansion_quirks]]
