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
11. **(1244-1255)** **Read Capture Delay sweep** — `origBaudRateDiv` 값부터 시작해서 ID read 성공할 때까지 1씩 줄이며 재시도. 보드 trace delay 흡수용. **`Flash_norOspiReadId`의 STIG dummy resolution은 §RDID dummy 절 참조 — 직전 SetModeDummy 결과를 inherit 하지 않는다.**
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

## RDID(`Flash_norOspiReadId`)의 dummy resolution

Open 시퀀스 11번(capture delay sweep loop)에서 호출되는 `Flash_norOspiReadId`(line 847-913)는 **STIG dummy를 controller register에서 inherit 하지 않고 함수 내부에서 직접 결정한다.**

### 결정 로직 (line 858-867)

```c
uint32_t dummyBits = 0;                              // 초기값 0

if(obj->currentProtocol == FLASH_CFG_PROTO_8D_8D_8D)
{
    dummyBits = idCfg->dummy8;                       // ← devCfg->idCfg.dummy8
    cmdAddr = 0U;
    idNumBytes = 4;                                  // odd byte 못 읽음
}
else
{
    /* default config */                              // ← dummyBits 그대로 0
}

Flash_norOspiCmdRead(config, idCfg->cmd, cmdAddr, numAddrBytes, dummyBits, ...);
```

`Flash_norOspiCmdRead`(line 99-117)는 받은 `dummyBits`를 `rdParams.dummyBits`에 박고 `OSPI_readCmd`로 STIG 발행. **`OSPI_setCmdDummyCycles`로 설정된 controller register는 참조하지 않는다.**

### 의미

| 시나리오 | RDID STIG가 나가는 dummy |
|---|---|
| non-8D protocol (1S-1S-1S 등) | **항상 0** (literal) |
| 8D-8D-8D | **`devCfg->idCfg.dummy8`** (device descriptor 값) |
| SetModeDummy가 직전에 controller cmdDummyCycles=16으로 설정 | **무시됨** |
| `pCfg->dummyClksCmd`가 16 | RDID에는 영향 없음 (RDID는 idCfg.dummy8 사용) |

### Device descriptor의 두 dummy 필드

| 필드 | 사용처 |
|---|---|
| `devCfg->protocolCfg.dummyClksCmd` | 일반 STIG 명령 (status read, register read 등) — `Flash_norOspiSetModeDummy`가 controller에 set, 다른 함수들이 inherit |
| `devCfg->idCfg.dummy8` | **RDID 전용** — 8D-8D-8D 모드의 RDID STIG에만 사용 |

두 필드는 **별도 관리** 책임이 descriptor 작성자에게 있음. IS25LX256 데이터시트(ch08 Table 8.1) 기준 8D-8D-8D RDID dummy = 8 → `idCfg.dummy8 = 8`이어야 정상. descriptor에서 16 같은 다른 값이 들어가면 sweep loop 전체가 실패.

### 8D RDID 실패 시 capture delay sweep이 못 고치는 이유

```
controller에서 보내는 STIG: cmd(0x9F) → dummy(idCfg.dummy8 cycles) → data
chip이 기대하는 시퀀스:        cmd(0x9F) → dummy(8 cycles, 고정) → data
```

`idCfg.dummy8`이 8과 다르면 데이터 위상이 cycle 단위로 어긋나 capture delay(phase 보정)로는 절대 정렬 불가. 첫 데이터 byte 자체가 의미 없는 위치에서 캡처됨.

→ 8D 진입 직후 ReadId가 실패한다면 descriptor의 `idCfg.dummy8`을 먼저 의심. capture delay sweep loop(line 1250-1255)은 헛수고.

## 위험 포인트

- **PHY attack vector 자동 write (line 1281-1306)**: PHY가 켜진 상태에서 첫 boot이고 attack vector가 flash에 없으면 *마지막 sector를 erase+write한다*. 이건 SBL이든 앱이든 마찬가지. 양산 펌웨어가 마지막 sector를 다른 용도로 쓰면 안 됨. `phyTuningOffset`은 `Flash_getPhyTuningOffset(config)`이 반환 (별도 파일).
- **`obj->currentProtocol = 1S_1S_1S` 초기 가정 (line 1228)**: SBL이 8D_8D_8D로 남겼는데 앱이 `skipHwInit=FALSE`로 Open하면, 드라이버는 1S로 가정하고 명령을 보냄 → chip이 8D에 있으니 대응 못 함 → Open 실패. SBL → 앱은 반드시 `skipHwInit=TRUE`.
- **dummy cycle mismatch**: `OSPI_setReadDummyCycles`로 컨트롤러는 무조건 새 값으로 설정됨. 앱이 쓰는 `dummyClksRd` ≠ SBL이 chip NVCR에 박아둔 값이면 read 데이터 깨짐. capture delay sweep으론 보정 안 됨. [[xspi_dummy_cycles]] + [[sbl_app_flash_handoff]] 참조.
- **RDID dummy field 분리 (§RDID dummy resolution)**: `idCfg.dummy8`과 `protocolCfg.dummyClksCmd`는 별도 필드. RDID는 idCfg.dummy8만 사용. descriptor에서 둘이 불일치하면 일반 명령은 통하지만 ReadId는 실패하는 양상 가능 — 진단 시 두 필드를 따로 dump.

## 함께 보기

- 원본 위치: [[mcupsdk_flash_nor_ospi]] (line 1195-1353)
- SBL → 앱 핸드오프: [[sbl_app_flash_handoff]]
- Dummy cycle 표: [[xspi_dummy_cycles]]
- Spansion vs ISSI 분기: [[is25lx256_vs_spansion_quirks]]
