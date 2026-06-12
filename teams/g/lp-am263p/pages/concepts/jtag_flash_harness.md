---
tags: [concept, flash, jtag, ospi, am263p, tooling, harness, boot, gotcha]
source: 실측 (2026-06-05 + 2026-06-12, 8kw-ev-wpt-tx 실보드 JTAG flash 세션)
date: 2026-06-12
---

# AM263P JTAG flash 자동화 하네스 + 굽기 운영 규율

> **flash-time(굽는 환경) 층위의 정본.** 런타임 `Flash_open()` 블로커([[flash_open_facts]] 등)와 층위가 다르다 — 이 페이지는 "어떻게 안정적으로 굽고, 굽은 걸 어떻게 검증하는가".
> jtag_flasher·flash_node.js는 lp-am263p(cc3351) 원산이고 8kw-ev-wpt-tx가 코드 복제본 → 도구 지식의 정본은 여기 둔다. 사실 전부 2026-06-05 8kw 실보드 세션에서 측정 확정.

---

## 한 줄 요약

AM263P OSPI JTAG flash 자동화는 **① run.bat Node.js(`runAsynch`) 하네스로 / ② CCS IDE 완전 종료한 클린 호스트에서 / ③ 연속 시도 사이 보드 파워 사이클하고 / ④ standalone 부팅 UART banner로 검증한다.** 네 규율 모두 측정으로 확정.

---

## 1. 검증된 하네스 = run.bat Node.js (`runAsynch`); DSS/Rhino(`GEL_RunF`)는 깨진다

| 경로 | 동작 |
|------|------|
| **run.bat Node.js scripting** (`C:\ti\ccs2050\ccs\scripting\run.bat` → `flash_node.js`) | ✓ `runAsynch` + `run(false)`로 R5 resume 후 `gCmd.status` 폴링 → **6/6 OK 완주 다회 검증** |
| **java.exe + uniflash JRE Rhino** (`GEL_RunF()`) | ✗ 깨짐 — OP를 한 번도 완주 못 함 |

**왜 Rhino 경로가 깨지는가** (인과 확정):
- `GEL_RunF()`는 애초에 `runAsynch`가 Java21+XPCOM 환경에서 JVM 크래시해서 **우회한 것**.
- 그런데 `GEL_RunF` resume는 R5를 **JTAG halt 없이 free-run** 상태로 둔다.
- 그 free-run 상태에서 DSS `readData`로 내부/TCM 영역(`gCmd.status` @`0x70038010`)을 읽으면 **`Error 0x400000`으로 거부** → status 폴링이 깨짐 → OP 완주 판정 불가.

→ **결론: AM263P JTAG flash 자동화는 run.bat Node.js(`runAsynch`) 하네스로.** (DSS Rhino는 status 폴링이 구조적으로 깨지므로 자동화에 부적합.)

---

## 2. 굽기는 CCS IDE를 완전히 종료한 클린 호스트에서

요지(전체 서사·증거·확인법은 [[jtag_flash_clean_host]] — 8kw 첫 ingest):
- host-driven 스크립팅(run.bat Node.js / DSS Rhino)은 CCS IDE(Theia) 상주 **cloudagent + DSLite** 디버그 백엔드와 **같은 백엔드를 두고 경합**.
- IDE 켜둔 채 돌리면 `ds.configure()`/`openSession`/`resume` 중 **런마다 다른 지점**에서 죽음(30s `ScriptingTimeoutError`, `DebugServer.1` timeout 등 **비일관** → 펌웨어/보드 오인 위험).
- **`getDebugSessions=[]`(논리 세션 0)라도 cloudagent가 띄운 DSLite는 상주 가능** → 작업관리자에서 `node`(cloudagent)/`DSLite` 프로세스까지 사라졌는지 확인.
- 증거: flashwriter `.out` 바이트 동일(펌웨어 무죄)인데 **IDE 켜둠=ERASE_ALL 실패 / IDE 완전 종료=6/6 OK 완주**.
- **양립 불가**: MCP `loadProgram`(IDE 경유 RAM 로드)은 IDE 켜짐 필요 / 독립 flash 스크립팅은 IDE 꺼짐 필요.

---

## 3. 연속 flash 시도 사이엔 보드 파워 사이클 필수

- **트리거**: 다수의 `loadProgram` / GEL soft reset / 중단된 런 / 직전 굽기를 **파워 사이클 없이 연속**으로 겪으면 R5/OSPI가 **wedged** 된다.
- **증상**: ERASE_ALL에서 magic write·halt까지 OK인데 **run 후 `gCmd.status`가 IDLE(`0x0`)에서 BUSY로 전이조차 안 함** → 300s timeout.
- **해소**: **전원 완전 차단→복원** (단순 JTAG 재연결로는 안 됨).
- **측정 확정**: 파워 사이클 후 동일 하네스로 **OP1이 ~61s에 IDLE 탈출→OK, 3/3 완주**.

→ soft reset류는 wedged 상태를 못 푼다. "전이조차 안 하는 IDLE"을 보면 코드/펌웨어 의심 전에 **파워 사이클** 먼저.

---

## 4. 검증의 ground truth = standalone 부팅 + UART banner

하네스 자기보고(`status=0x2`)나 MCP readback **보다**, SW1을 OSPI boot 모드로 두고 **전원만으로 부팅시켜 UART에 banner가 뜨는지**가 가장 정확한 검증 — ROM→SBL→app **전 경로를 실증**하기 때문.

**성공 부팅 프로파일 (증거)**:

| 항목 | 값 |
|------|-----|
| Boot Media | NOR SPI FLASH |
| Boot Media Clock | 16.667 MHz |
| Boot Image Size | 30 KB |
| SBL Total | ~28967 µs |
| banner | `eta-tx: 8kw-ev-wpt v1.0e00` ⚠️ **구 이미지 기준** — 현재 `src/main.c`:45 배너는 `"eta-tx: 8kw-ev-wpt start"`([[ospi_boot_console_diagnostic]] §5) |

**SW1 부트모드** (정정본, 근거 LP-AM263P UG SPRUJ85B Table 2-5 — 단일 소스는 [[CLAUDE]] "하드웨어" 절):
- **DevBoot = `0,1,0,0`** (SW1.3만 ON, "No SBL") — 개발 편의용. **굽기에 필수는 아님**(굽기는 OSPI(4S)=`1,1,1,1`에서도 성공, 2026-06-12 실측 — 아래 §7). ※ 굽기는 JTAG `loadProgram`로 flashwriter를 RAM에 올리므로 **부트 스트랩과 무관** — 어느 SW1 값이든 굽힌다.
- **standalone 부팅 정답 스트랩 = xSPI 8D (SFDP) = `0,0,1,1`** — 2026-06-12 실증(SBL→app→`eta-tx: 8kw-ev-wpt start`). 정본 [[ospi_boot_mode_strap]].
  - ⚠️ **정정**: 종전 이 줄은 "standalone 부팅 OSPI(4S) `1,1,1,1` — `sbl_ospi_am263p.tiimage`로 실증"이라 적었으나 **오류**. 보드 flash(IS25LX256)는 octal-only라 4S(`0x6B`/QE) 부팅이 물리적으로 불가([[ospi_boot_mode_strap]] §2). `1,1,1,1`은 ROM→SBL 실패(`'C'` ping)를 내던 잘못된 스트랩이었다.
- ※ 과거 cc3351 노트의 `DevBoot=1,1,0,0`은 **오기**(`1,1,0,0`은 OSPI 8S Octal Read 값) — [[CLAUDE]]에서 2026-06-05 정정 완료.

---

## 5. flashwriter / OSPI flash map 사실

**flashwriter** = `jtag_flasher.out` (= SDK `sbl_jtag_uniflash` + `AutoCmd_t` auto-mode). 메모리 인터페이스:

| 심볼 | 주소 |
|------|------|
| gCmd base | `0x70038000` |
| gCmd status | `0x70038010` |
| magic | `0xDEAD1234` |
| 파일 버퍼 | `0x70040020` |

**OSPI flash 맵**: SBL @`0x0`, 앱 mcelf @`0x81000`. (boot flow·플래시 base `0x53808000`는 [[CLAUDE]] "하드웨어" 절.)

**PHY 경고는 무해**: `Flash_norOspiPhyTune:1520 PHY enabling failed!!! Continuing without PHY...` — standalone 부팅이 **이 경고 위에서 성공**함이 증거. (PHY 비활성 운용 시 capture delay 거동은 [[sbl_app_flash_handoff]] §2.)

---

## 6. 하네스 위치

| 프로젝트 | 파일 | 비고 |
|----------|------|------|
| lp-am263p (cc3351) | `flash_node.js` (+ `run.bat`) | 원산 |
| 8kw-ev-wpt-tx | `8kw-ev-wpt-tx/tools/jtag_flash/flash_node_8kw.js` + `run_flash_node_8kw.ps1` | cc3351 `flash_node.js`와 **코드 로직 동일, OPS만 3개로 교체** |

---

## 7. 굽기 부트모드 — DevBoot는 필수 아닌 편의 (FACT, 2026-06-12)

**JTAG flash는 SW1=OSPI(4S)=`1,1,1,1`(DevBoot 아님)에서도 성공한다 → 굽기에 DevBoot는 필수가 아니라 편의.**

- **근거(실측 2026-06-12)**: SW1=`1,1,1,1` 고정(보드가 OSPI에서 standalone 부팅돼 **app이 실행 중**인 상태) + CCS IDE 완전 종료(§2 클린 호스트) 상태에서 `run_flash_node_8kw.ps1` → **3/3 OK, 프로세스 EXIT 0**.
- **메커니즘 — `loadProgram` soft-reset**: 하네스 로그에 매 OP의 `loadProgram`마다 `"CPU reset (soft reset) has been issued through GEL on program load"` 출력. 즉 flasher가 flashwriter `.out`을 RAM에 로드할 때 코어를 **soft-reset**해, **부팅돼 돌던 app으로부터 코어 점유를 깨끗이 인수**한다. → SW1이 OSPI 부팅 모드여서 app이 돌고 있어도 굽기 진입에 지장 없음.
  - **flashFixUpOspiBoot의 chip 1S 리셋과 별개**: 그쪽은 OSPI chip 상태를 1S로 되돌리는 것이고, 여기서 새로 관측된 건 **코어 점유(running app) 문제도 `loadProgram` soft-reset로 해소**된다는 점.
- **이로써 미해결 질문 "DevBoot가 flash에 필수냐 편의냐" 중 굽기 단계 = '편의'로 확정.** DevBoot의 "No SBL"은 굽기 안정성/속도 편의일 뿐, OSPI 부팅 모드에서도 굽힌다.

> ⚠️ **굽기만 확정 — "토글-프리 루프 전체"는 미확정.** 위는 *굽는 절반*만이다. "SW1=`1,1,1,1` 고정한 채 전원사이클만으로 **새 이미지가 standalone 부팅**되는가"(= dead-time 반복 워크플로의 부팅 절반)는 이번에 확정 못 함 → [[toggle_free_flash_loop]]에 OPEN으로 분리 기록.

---

## 8. SBL provenance — 파일 무결성 확정 (2026-06-12)

`flash_node_8kw.js`가 굽는 `C:/ti/sbl_ospi_am263p.tiimage`(307005B, SHA256 `735D12EB...58108B7`)는 SDK 공식 프리빌트 `mcu_plus_sdk_am263px_26_00_00_01/.../sbl_ospi_multicore_elf.release.tiimage`와 **바이트 동일**. 파일명 `am263p`는 공식 rename. SBL 변종(multicore_elf)·실리콘(am263px-lp)·무결성 전부 정합.

**결론**: "SBL 파일이 잘못됐다" 가설 완전 제거. ~~잔여 블로커는 SBL 자체가 아닌 flash 프로그래밍/설정.~~ → **실제 블로커는 부트모드 스트랩 미스매치**였고 strap 교정(`0,0,1,1`)으로 같은 SBL이 정상 부팅([[ospi_boot_mode_strap]]). 상세: [[ospi_boot_console_diagnostic]] §4.

---

## 빈자리 (미검증)

- ~~토글-프리 루프 부팅 절반 미확정~~ — **✅ 해소 (2026-06-12)**: `1,1,1,1`(4S)에서의 `'C'` ping은 **부트모드 스트랩 미스매치** 때문(octal-only 칩). **SW1=`0,0,1,1`(xSPI 8D SFDP)로 교정 → 완전 부팅** → 굽기 ✓ + 부팅 ✓로 루프 닫힘. 정본 [[ospi_boot_mode_strap]], 맥락 [[toggle_free_flash_loop]] §②.
- **OSPI 독립 readback 미검증** — 이번 세션에서 굽기 검증은 **standalone 부팅(§4)으로 대체**했다. 하네스/MCP를 통한 별도 flash 독립 read-back 검증은 수행하지 않음.
- §1 `Error 0x400000`이 R5 free-run + TCM 접근 조합 외 다른 영역(외부 OSPI 매핑)에서도 동일하게 거부되는지 — 미확인(필요시 추가 측정).

---

## 함께 보기

- **부트모드 스트랩 미스매치 = standalone 무부팅 진짜 원인 (해소 정본)**: [[ospi_boot_mode_strap]]
- 토글-프리 dead-time 반복 루프(굽기 ✓ + 부팅 ✓): [[toggle_free_flash_loop]]
- 클린 호스트 deep-dive(8kw 첫 ingest): [[jtag_flash_clean_host]]
- 런타임 `Flash_open()` 블로커(층위 다름): [[flash_open_facts]] · [[flash_open_diagnostic_log]] · [[sbl_app_flash_handoff]] · [[flash_open_sequence]]
- 부트 흐름·SW1 부트모드·플래시 base: [[CLAUDE]] "하드웨어 — 부트 모드 / boot flow" 절
- 전략 spine: [[porting]] · 다음 시작점/현황: [[status]]
- 프로브 인벤토리: [[instruments]]
