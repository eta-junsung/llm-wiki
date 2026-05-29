---
tags: [concept, flash, ospi, diagnostic-log, am263p, s3-blocker, append-only]
source: report.md (R19~R27) + roadmap.md §5
date: 2026-05-29
---

# Flash_open S3 블로커 — 진단 라운드 로그

> **이 페이지는 append-only.** 새 라운드는 맨 아래(§다음 위)에 추가하고, 옛 항목은 수정하지 않는다 (틀린 것으로 판명나도 그대로 두고, 다음 라운드에서 반증을 기록한다 — 그게 history의 가치다).
> 증류된 현재 진실(확정 사실/폐기 가설)은 [[flash_open_facts]]를 본다. 여기는 "어떻게 거기 도달했는가"의 서사.

각 라운드 골격: **가설 → 변경 → 관찰 → 결론**.

---

## R7~R19 (요약 블록)

- **R13**: `dummyClksCmd=8` 런타임 패치 → Flash_open hang 해소(이후 NULL 반환으로 증상 전환).
- **R16~R19**: RDCAP 레지스터 4조합(0x121·0x021·0x001·0x101)을 indirect sweep — 전부 실패.
- 이 시기 전제: **"chip이 8D DDR에 있다"** (R20에서 붕괴됨).

## R20 — DQ1-only 최초 관찰

- **관찰**: 8D RDID 응답이 **DQ1 한 라인만 활성**, DQ[7:2]·DQ0 항상 0.
- **결론**: "chip이 8D DDR에 있다"는 R7~R19 전체 전제가 깨짐. 가지 α/β/γ(chip이 1S/reset/8D-PHY문제) 분기 발생.

## R21 / R22 / R24

- **관찰**: 1S RDID = `FF FF FF FF`, 8D RDID = `00 00 00 00` — 어느 프로토콜에서도 유효 RDID 없음.
- **R24**: CONFIG_REG bit30 = DUAL_BYTE_OPCODE_EN, 이미 0임 확인 → **bit 잔류 가설 폐기**.

## R25 — skipHwInit=FALSE 진단 (폐기)

- **가설**: `skipHwInit=FALSE` + OSPI RESET 핀 토글로 chip을 1S로 되돌리면 set888mode가 1S→8D 정상 승격할 것.
- **변경**: `skipHwInit=FALSE` + OSPI RESET 핀 토글 + 1S RDID (60초 캡처).
- **관찰**: `[NOS] 1 SetProto st=-1`, NOS-RDID sweep `02 03 03 03`→`00`, Flash_open FAILED. pin-reset 후 1S RDID = `FF FF FF FF FF`.
- **결론**: `set888mode`가 SBL 잔여 상태에서 쓰기 실패(st=-1), status 누적 구조로 이후 단계 신호 오염 → **skipHwInit=FALSE 진단 라운드 폐기**. DQ1-only sweep(`02 03 03 03`)이 R20과 독립 일치 → **DQ1-only 사실 승격**. `READ_DATA_CAPTURE_REG=0x00000121`(SBL 잔여) 확인.

## R26 — DQS_ENABLE=0 (가설 반증)

- **가설**: `READ_DATA_CAPTURE_REG`의 DQS_ENABLE을 0으로 클리어하면 STIG 캡처가 살아날 것.
- **변경**: `skipHwInit=TRUE` + `DQS_ENABLE=0`(READ_DATA_CAPTURE_REG 클리어).
- **관찰**: 전부 FF, SetRdCap st=-1.
- **결론**: DQS 없으면 8D DDR 캡처 완전 불가 → **DQS_ENABLE=0 가설 반증**. (roadmap §5가 "R25/R26 검증 예정"으로 들고 있던 가설을 여기서 종결)

## R27 — skipHwInit=TRUE 8D 그대로 RDID

- **가설**: Drivers_open이 만든 8D 상태를 그대로 두고 RDID 캡처 delay만 맞추면 통과할 것.
- **변경**: `skipHwInit=TRUE` + 8D 상태 유지 + RDID(dummy=8 / dummy=0 / 1S setProtocol 후 비교).
- **관찰**: 직접 RDID FF, NOS-RDID delay=15에서 `02 03 03 03`, Flash_open FAILED.
- **결론**: delay=1(SBL 잔여)에서 캡처 타이밍 미스, DQ1-only 패턴 지속. `set888mode` opcode가 `0x81`(정상)임을 코드 확인 — `0x71` 혼동 종결. `[DIAG] R27: Flash_open FAILED` — S3 미통과.

### R27 현재 코드 블록 (`cc3351/main.c`)

```c
/* Runtime patches */
gFlashParams[CONFIG_FLASH0].quirksFxn = NULL;
gFlashConfig[CONFIG_FLASH0].skipHwInit = (uint8_t)TRUE;   // 진단용 유지 중
gFlashConfig[CONFIG_FLASH0].devConfig->protocolCfg.dummyClksCmd = 8U;
// RDCAP 현재값 출력 / 8D RDID(dummy=8) / 8D RDID(dummy=0) / 1S RDID(setProtocol 후) / Flash_open
```

---

## 다음 (R28 계획)

**방향: 후보 A — jtag_flasher 성공 공식 이식.** chip을 1S known-state로 되돌린 뒤 `skipHwInit=FALSE`로 정상 승격시킨다.

```c
/* skipHwInit=FALSE (SysConfig 기본값 복귀) */
gFlashConfig[CONFIG_FLASH0].skipHwInit = (uint8_t)FALSE;

/* flashFixUpOspiBoot() 인라인 재현 — OSPI RESET 핀 HW 토글 */
OSPI_Handle oHandle = gOspiHandle[CONFIG_OSPI0];
board_flash_reset(oHandle);              // cc3351 syscfg에 생성되어 있어야 함
OSPI_enableSDR(oHandle);
OSPI_clearDualOpCodeMode(oHandle);
OSPI_setProtocol(oHandle, OSPI_NOR_PROTOCOL(1,1,1,0));
/* 이후 Flash_open이 set888mode(0x81)로 1S→8D 승격 */
```

**선행 확인**: cc3351 `example.syscfg`에 OSPI reset 핀 설정이 없음. `board_flash_reset()`이 cc3351 SysConfig 생성 코드에 있는지, 없으면 `OSPI_setResetPinStatus`만으로 동등한지, jtag_flasher `example.syscfg`와 비교 필요. SDK board lib 재빌드 필요 여부도 확인.

**성공 기준**: `[DIAG] R28: Flash_open OK`, `gFlashHandle[0] != NULL`.

**실패 시 분기**:
- set888mode st=-1 재발 → chip이 1S로 안 돌아옴(RESET 핀 미연결 가능성) → H/W 점검.
- set888mode st=0이나 SetRdCap 실패 → 8D 승격은 됐으나 RDID 캡처 문제 → PHY tuning 경로 재검토.

---

## 함께 보기

- 증류된 확정/폐기: [[flash_open_facts]]
- 다음 시작점/현황: [[status]] · 전략: [[roadmap]]
- 핸드오프 계약: [[sbl_app_flash_handoff]]
