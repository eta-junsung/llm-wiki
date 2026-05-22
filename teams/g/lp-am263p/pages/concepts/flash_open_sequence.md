---
tags: [concept, flash, ospi, driver, am263p, ti_mcupsdk, init_sequence]
source: [[mcupsdk_flash_nor_ospi]] (lines 1195-1353)
date: 2026-05-22
---

# `Flash_norOspiOpen` — 진행 시퀀스와 종료 시 상태

TI MCU+ SDK의 `Flash_norOspiOpen()`이 무엇을 어떤 순서로 하고, 함수가 리턴된 시점에 **OSPI 컨트롤러**와 **flash chip** 양쪽이 어떤 상태인지 정리.

> 이 페이지는 SBL/앱 양쪽에서 Flash_open이 호출될 때 모두 적용. SBL → 앱 핸드오프 시 *chip register write를 스킵*하는 게이트는 [[sbl_app_flash_handoff]] 참조.

## 시퀀스 (line 번호는 raw `flash_nor_ospi.c` 기준)

1. **(1202)** `OSPI_getHandle(driverInstance)` — OSPI 드라이버 핸들 획득
2. **(1212)** `OSPI_setDeviceSize(pageSize, blockSize)` — 디바이스 geometry 컨트롤러에 전달
3. **(1215)** `OSPI_setCmdExtType(cmdExtType)` — 8D 명령 확장 인코딩 방식 셋 (`repeat`/`invert`/`none`)
4. **(1218-1225)** address byte 결정 — `addrByteSupport==2` (4B-only)면 4, 아니면 3으로 시작
5. **(1228)** `obj->currentProtocol = 1S_1S_1S` — *통신 출발 상태 가정*. chip이 1S에 있다는 전제로 보내야 register write 명령이 도달함
6. **(1231)** `Flash_norOspiSetProtocol(config, ospiHandle, params)` — 핵심 단계:
   - `switch(protocol)` (line 762) 으로 protocol별 enable 시퀀스 디스패치
   - 8D_8D_8D 경로 (line 818): `Flash_setOeBit` (Octal Enable) → `Flash_set888mode` (888 mode 진입 명령. seq 비트 따라 `0xE8` 혹은 register write)
   - 끝에서 `OSPI_setProtocol(controller, 8D_8D_8D)` (line 840)
   - **단, `config->skipHwInit==TRUE`면 chip 측 OE/888 명령 모두 스킵 (line 821) — `OSPI_setProtocol`만 실행**
7. **(1232)** `obj->currentProtocol = devCfg->protocolCfg.protocol` — 드라이버 측 트래킹 갱신
8. **(1235)** `Flash_norOspiSetAddressBytes` — 4B addr 지원이면 `OSPI_setNumAddrBytes(4)` + chip 측 4B enable 명령 (`0xB7` 등). `skipHwInit=TRUE`면 chip 명령 스킵, OSPI 측 4 셋팅은 그대로
9. **(1238)** `OSPI_setXferOpCodes(cmdRd, cmdWr)` — chip read/write opcode를 컨트롤러에 전달
10. **(1241)** `Flash_norOspiSetModeDummy` — mode bit (line 513-521) + dummy clocks (line 523-524) 셋. `skipHwInit=FALSE`일 때만 chip 측 NVCR/VCR 쓰기 발생 (line 527)
11. **(1244-1255)** **Read Capture Delay sweep** — `origBaudRateDiv` 값부터 시작해서 ID read 성공할 때까지 1씩 줄이며 재시도. 보드 trace delay 흡수용
12. **(1259-1339)** **PHY tuning** (PHY 활성화된 경우):
    - Attack vector를 flash에서 읽기 시도 (`OSPI_phyReadAttackVector`)
    - 실패하면 capture delay 8 → 0 sweep
    - 그래도 실패하면 attack vector 자체를 flash 맨 뒤 sector에 *erase+write* (line 1281-1306, **destructive!**)
    - 성공하면 `OSPI_phyTuneDDR` 호출 → `obj->phyEnable=TRUE`, `OSPI_setPhyEnableSuccess(TRUE)`
    - 실패 시 `obj->phyEnable=FALSE`, `status=FAILURE`로 끝
13. **(1343-1346)** `params->quirksFxn(config)` 호출 — 디바이스별 quirk hook (예: `Flash_quirkSpansionUNHYSADisable`)

## 함수 리턴 시점의 상태

### OSPI 컨트롤러 (host side)

| 항목 | 값 / 동작 |
|---|---|
| Protocol register | 8D_8D_8D (혹은 `devCfg->protocolCfg.protocol`)  |
| `numAddrBytes` | 4 (또는 디바이스가 4B 미지원이면 3) |
| Read/Write opcode register | `devCfg->protocolCfg.cmdRd`, `cmdWr` |
| Read dummy cycles | `devCfg->protocolCfg.dummyClksRd` |
| Cmd dummy cycles | `devCfg->protocolCfg.dummyClksCmd` |
| Mode bits cmd/read | `modeClksRd != 0`이면 enabled, value=`modeClksRd` |
| Device size | `attrs->pageSize`, `attrs->blockSize` 셋 |
| Cmd ext type | `devCfg->cmdExtType` 셋 |
| Read Data Capture Delay | ID read가 통과한 sweep 값 (0~`origBaudRateDiv`) |
| PHY | 활성화되면 ON + tuned. 안되면 OFF |
| **DAC (Direct Access) mode** | **OFF** — `enableDacModeFxn`은 별도 호출 |

### Flash chip (device side)

`skipHwInit==FALSE`일 때:

| 항목 | 값 |
|---|---|
| I/O mode | 8D_8D_8D (888 mode entry로 전환됨) |
| Address mode | 4B (4B addr enable 명령 발행됨) |
| NVCR/VCR dummy field | `dummyCfg.cfgRegBitP` 값 |
| QE/OE bit | enable_type에 맞게 set |
| 444/888 mode register | seq 비트별로 명령 발행 완료 |

`skipHwInit==TRUE`일 때: **chip register write는 전부 스킵**. 즉 chip은 SBL이 남겨놓은 상태 그대로. 상세는 [[sbl_app_flash_handoff]].

## 위험 포인트

- **PHY attack vector 자동 write (line 1281-1306)**: PHY가 켜진 상태에서 첫 boot이고 attack vector가 flash에 없으면 *마지막 sector를 erase+write한다*. 이건 SBL이든 앱이든 마찬가지. 양산 펌웨어가 마지막 sector를 다른 용도로 쓰면 안 됨. `phyTuningOffset`은 `Flash_getPhyTuningOffset(config)`이 반환 (별도 파일).
- **`obj->currentProtocol = 1S_1S_1S` 초기 가정 (line 1228)**: SBL이 8D_8D_8D로 남겼는데 앱이 `skipHwInit=FALSE`로 Open하면, 드라이버는 1S로 가정하고 명령을 보냄 → chip이 8D에 있으니 대응 못 함 → Open 실패. SBL → 앱은 반드시 `skipHwInit=TRUE`.
- **dummy cycle mismatch**: `OSPI_setReadDummyCycles`로 컨트롤러는 무조건 새 값으로 설정됨. 앱이 쓰는 `dummyClksRd` ≠ SBL이 chip NVCR에 박아둔 값이면 read 데이터 깨짐. capture delay sweep으론 보정 안 됨. [[xspi_dummy_cycles]] + [[sbl_app_flash_handoff]] 참조.

## 함께 보기

- 원본 위치: [[mcupsdk_flash_nor_ospi]] (line 1195-1353)
- SBL → 앱 핸드오프: [[sbl_app_flash_handoff]]
- Dummy cycle 표: [[xspi_dummy_cycles]]
- Spansion vs ISSI 분기: [[is25lx256_vs_spansion_quirks]]
