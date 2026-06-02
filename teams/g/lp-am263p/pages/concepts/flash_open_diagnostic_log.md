---
tags: [concept, flash, ospi, diagnostic-log, am263p, s3-blocker, append-only]
source: report.md (R19~R27) + roadmap.md §5
date: 2026-06-01
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

## R28 — pinmux 스크램블 발견 + S3 통과 ✓

- **가설 진입**: jtag_flasher 성공 공식 이식 계획으로 시작. syscfg 비교 중 pinmux 차이 발견 → pinmux 교정 단독 실험(R28b)으로 방향 전환.
- **발견**: cc3351 `example.syscfg`가 `$suggestSolution`(soft), jtag_flasher가 `$assign`(hard) — SysConfig 솔버가 8핀(CSn0/D0/D1/D2/D3/D5/D7/RESET_OUT0)을 EPWM/MCAN pad에 MODE6으로 오배치. ccs-sysconfig MCP 경유, OSPI 12핀 전부 `$assign` hard-lock으로 교정. 올바른 핀맵: CLK/CSn0/D0/D1/D2/D3 = native OSPI pad(MODE0), D4-D7 = MCAN pad(MODE2), DQS = UART1_TXD pad, RESET = EPWM11_B/J1 pad. **main.c 변경 없음**, pinmux 교정만 적용(R28b). 커밋 **bb56630**.
- **관찰** (`round28b.log`):
  - RDID = `9D 5A 19` (IS25LX256, manf=`0x9D` ISSI, dev=`0x5A19`). "DQ1-only" 패턴 소멸.
  - `[DIAG] R27: Flash_open OK` — 진단 Flash_open 성공.
- **결론**:
  - **S3 블로커 근본 원인 확정** = cc3351 `example.syscfg` OSPI pinmux 스크램블 (`$suggestSolution` → SysConfig 7핀 오배치). R7~R27의 SBL-핸드오프/skipHwInit/DQS/RDCAP-tuning 귀인은 "pinmux 정상" 잘못된 전제 위에 쌓인 것 → **일괄 폐기**.
  - "DQ1-only RDID"는 8D-PHY 문제(가지 γ)가 아니라 **핀 스크램블 증상**이었음.
  - **새 블로커**: freertos_main의 R27 진단 스캐폴딩(드라이버 인라인 open + 수동 Flash_open)이 network_terminal_entry 자체 init과 **이중 open 충돌** → 스캐폴딩 제거 필요 (하드웨어 문제 아님).

---

## R29 — 스캐폴딩 제거 + CLI 도달 ✓

**배경**: R28b로 S3 통과. 진단 스캐폴딩(freertos_main 인라인 Drivers_open + 수동 Flash_open 블록) 잔존.

**실패 시도 (round30)**: freertos_main에서 `Drivers_open`+`Board_driversOpen` 직접 호출 → **double-open st=-1** 실측. 원인: `network_terminal_entry()` 내부에서 `Drivers_open`(:1205)+`Board_driversOpen`(:1206) 자체 수행, 반환 직전 `Board_driversClose`(:1265)+`Drivers_close`(:1266). → **freertos_main은 드라이버를 건드리지 않는다.**

**해법 (round31)**:
- freertos_main을 원본 구조(`network_terminal_entry(NULL)` + `vTaskDelete`)로 복원.
- `ti_board_open_close.c` 전역 `gFlashParams`/`gFlashConfig`에 `network_terminal_entry` 호출 전 in-place 패치: `quirksFxn=NULL`, `skipHwInit=TRUE`, `dummyClksCmd=8`. `Board_driversOpen`이 그대로 읽는다.

**관찰 (round31.log)**:
- Flash_open st=0, RDID=`9D 5A 19`.
- "Network Terminal upper_mac_3.0.5.12" 배너 + 명령어 목록 + `user:` 프롬프트 도달.

**결론**: S4(`Board_driversOpen` 완주) ✓. ★ **표준 Board_flashOpen 단독 동작 최초 실측 검증** (skipHwInit=TRUE + dummyClksCmd=8 + quirksFxn=NULL + R28-A pinmux 조합). S5/S6/S7은 배너·프롬프트 도달로 추정됨 — `wlan_scan` 미실측. 커밋 **3a06ab8**.

**미검증 가설 [H-A]**: `skipHwInit=TRUE`는 `Flash_norOspiSetProtocol` 내부 쓰기(4ByteAddr/protocol/set888 VCR)만 가드 — `SetRdCap`(:1332)·`PhyTune`(:1336)은 가드 밖 항상 실행. skipHwInit=TRUE 성공이 "SBL 핸드오프 8D 유지"에 의존한 것인지 미확정. R28b 최소 충분 패치셋(quirksFxn/skipHwInit/dummyClksCmd 3종 조합)도 미분리.

---

## R30 — CLI 인터랙티브 실측: WiFi 기동 새 블로커 발견

**배경**: R29로 CLI 프롬프트 도달. S5/S6/S7 미독립검증 상태. 목표 두 가지: (A) skipHwInit/dummyClksCmd/quirksFxn 최소 패치셋 분리, (B) end-to-end 실동작. 현 보드가 이미 CLI 빌드(3a06ab8)이므로 **B 먼저**(재플래시 0회).

**도구 추가**: `jtag_flasher/cli_interact.ps1` 신규 — UART 송신+수신 루프. **per-char 페이싱(기본 15ms) 필수** — 보드 콘솔이 polled single-byte read+echo 구조라 burst 송신 시 RX FIFO 오버플로로 드롭 (B1 첫 시도 `w`만 echo로 발견). 페이싱 후 전체 명령 정상 echo.

**관찰** (cli_b0~b2 로그):
- **B0 (빈 Enter, CR)**: 송신 후 `user:` 재출력 → CLI UART RX 수용 확정, 줄끝=CR, 하니스 정상 동작.
- **`wlan_get_fw_ver`**: `Version read failure with error 22555` — device stopped 상태 읽기 실패(별도 블로커 아님).
- **`wlan_scan`**: `not role id STA` — STA role 선행 필요.
- **`wlan_sta_role_up`**: `Chosen domain is WW` + `Device is stopped, run wlan_start.`
- **`wlan_start`**: ❌ **FreeRTOS 커널 ASSERT** — `FreeRTOS-Kernel/queue.c:xQueueReceive:1517: !((pvBuffer==NULL) && (uxItemSize!=0)) failed`. assert 후 프롬프트 미복귀(보드 멈춤).

**결론**:
- **S5/S6 실질 블로커** = `wlan_start`에서 FreeRTOS 큐 assert 크래시. `xQueueReceive(q, NULL, ...)` 호출 — NULL buffer인데 itemSize≠0 큐에 사용. 큐/세마포어 NULL 핸들이거나 CC33xx OS 어댑테이션 레이어(`osi_*` / WiFi_adaptation_layer)가 FreeRTOS 큐 의미와 어긋난 것으로 추정.
- `osi_filesystem.c` write stub과 같은 어댑테이션 레이어 미완성의 연장선 가능성.
- **Flash_open 성공 ≠ 포팅 완료** 명시적 입증.
- 목표 A(최소 패치셋 분리) 미수행 — [H-A] 여전히 open.

---

## R32 — heap 증설로 wlan_start assert 해소, SPI 링크 새 블로커

**가설**: R30 `wlan_start` FreeRTOS 큐 assert(`xQueueReceive(q, NULL)`)는 `eventEntryThread`의 `os_malloc`(`control_cmd_fw.c:1295`) NULL 반환 → 32KB 공유 힙(`.sysmem`; linker.cmd 주석: libc malloc + FreeRTOS `pvPortMalloc` heap_3 공유) 고갈.

**변경**: ccs-sysconfig `/memory_configurator/general` heap_size 32768→262144(256KB). cc3351 재빌드(SDK lib 재빌드 불요), `.sysmem=0x40000` 재링크 확인. 재플래시(6/6 OK).

**관찰** (`cli_r32_wlanstart.log`):
- assert 소멸. `Hardware init DONE!` → `getting device info.....` → `SPI not responsive!`
- `SendTransactions failed eStatus:6` / `WLAN_EVENT_ERROR 0x80005826` / `CMD_ERR_TIMEOUT` / `cmd_Send error 0x8000581d`.

**결론**:
- **heap 고갈 = R30 assert 근본 원인 확정 + 수정.** JTAG 라이브 포착 불가(connect 항상 리셋 → SBL 미재실행 → 무음 크래시)였으나 정적 증거 + heap 증설 실측으로 가설 입증.
- **새 블로커 S6**: AM263P ↔ CC33xx SPI 전송 링크 무응답 — `SPI not responsive!` / `CMD_ERR_TIMEOUT`.
- wlan_start 에러 후 CLI 프롬프트 미복귀 (보드 settling/retry 추정, 미확정).

---

## R33 — SPI 무응답 진단: MISO 전부-0

(R32 커밋 853f3ac)

**도구**: 기존 `cli_interact.ps1` 활용 + `spi_adapt.c`/`wlan_irq_adapt.c`에 `[R33-SPI]`/`[R33-EN]` 마커 추가. 커밋 0e0e0c8.

**JTAG 라이브 포착 불가 확정**: `ccs-debug connectTarget`가 항상 코어 리셋 → continue가 SBL 미재실행으로 앱을 prereq 없이 cold 실행 → 무음 크래시. 부팅된 앱에 리셋 없이 attach 불가 → 진단은 UART 마커(`cli_interact.ps1`)로 고정.

**핀맵 확보 (BP-CC3351 SWAU132A Table 2-3/2-4, 사용자 직접 확인 결선)**:
- BP P1.5=LP_RESET(active-low), P1.7=SPI CLK, P1.8=IRQ_WL, P2.14=MISO/POCI, P2.15=MOSI/PICO, P2.18=CS.
- LP J1↔BP P1, LP J2/J4↔BP P2. J1.7=SPI0_CLK(A11), J2.15=SPI0_D0(C10/MOSI), J2.14=SPI0_D1(B11/MISO), J2.18=SPI0_CS0(C11), J1.5=WLAN_EN(M15/PR0_PRU0_GPIO12), J1.8=WLAN_IRQ(G18/PR0_PRU0_GPIO10).

**관찰** (`cli_r33_markers.log`):
- `[R33-EN] WLAN_EN toggled on` 출력.
- `[R33-SPI] rd#0..7 w0=0 w1=0` 전부-0 — NP가 MISO 무응답.

**mux 가설 약화**: TI MCU+ SDK LP SPI0 예제(`mcspi_external_loopback/am263px-lp`)가 mux init no-op로 동일 핀(A11/C10/B11/C11) 동작 → SPI0에 mux SW 설정 불필요 추정.

**결론**: SPI MISO 전부-0 확인. MCSPI inputSelect=D0(MOSI 라인) 설정 의심.

---

## R34 — MCSPI 수신선 D0→D1 교정

**가설**: cc3351 MCSPI inputSelect=D0 + dpe0(D0)=TX_ENABLED = SysConfig invalid combo(TX·RX 동일선/3-wire). 4-wire 배선상 MOSI=D0(C10/J2.15), MISO=D1(B11/J2.14).

**변경**: ccs-sysconfig inputSelect D0→D1(dpe0=TX_ENABLED 유지). 커밋 71b732e.

**관찰** (`cli_r34_wlanstart.log`):
- SPI read 전부-0 → D1 비-0(`0xFFFFFFFF`/변동)으로 전환 — 실제 MISO 읽기 시작.
- `SPI not responsive` 여전 — NP WSPI 핸드셰이크 미완.

**결론**:
- RX 설정 교정 정당(유지). NP가 아직 응답하지 않음.
- 잔여 블로커 후보: ① WLAN_EN(M15→J1.5→BP P1.5 LP_RESET, active-low) reset 해제 폴리시/타이밍, ② MOSI(C10/J2.15)/CLK(A11/J1.7) NP 실제 도달, ③ SPI clock mode. R35로 이월.

---

## R35 — Saleae 물리 실측: CS 어서트 확인 / CLK 무신호 확인

**측정 환경**: Saleae Logic Pro 16(logic2), 임계 3.3V, 125 MS/s.  
프로브: D0=CS(P2.18), D1=CLK(P1.7), D2=MOSI(P2.15), D3=MISO(P2.14), D4=WLAN_IRQ(P1.8), GND=P2.20.  
캡처: ① 10초 블라인드 ② CS 하강엣지 트리거 (두 방법 동일 결과).

**관찰**:
- **CS(P2.18)**: ~1.008µs LOW 펄스 **1회만** 발생 — 어서트 자체는 물리 핀까지 도달 확인.
- **CLK(P1.7): 토글 0회** — 클럭이 핀에 전혀 안 나옴.
- MOSI(P2.15): 무변화(HIGH 고정), MISO/IRQ: 무변화.
- 패턴: "CS는 핀에 나오는데 CLK/MOSI는 안 나온다" = **zero-clock CS 프레임**.
- 펌웨어: init → RTOS 스케줄러 통과 → `vApplicationIdleHook`(`port.c:405`) 안착. 크래시 아님 — app task 종료 또는 블록 상태.

**pinmux 가설 반증**:
- SPI0_CLK/D0/D1/CS0 pinmux가 `evaluations/spi0` 실증 빌드와 cc3351이 **PIN_MODE(0)로 동일** (`cc3351 ti_pinmux_config.c:125-148` ↔ `spi0 ti_pinmux_config.c:42-64`).
- cc3351도 `Pinmux_init()` 경유 (`ti_drivers_config.c:335`).
- → CLK 침묵 원인은 **IOMUX 바깥**.
- 유일 차이 `inputSelect(D0↔D1)`는 MISO 선 설정이라 CLK 출력과 무관.

**caveat**:
- D1(CLK) 프로브 연결 미확정 — CPOL=0(idle=LOW), 연결 양호·불량 구분 불가. **CS 토글(D0=LOW 포착)은 정상이므로 GND/전압은 OK**. D1이 정말 J1.7에 닿아 있으면 클럭이 있었을 때 포착됨. 단, D1 닿음 여부 자체는 사용자 확인 필요.

**결론**:
- CS pinmux + SPI0 CS 배선 정상 (물리 어서트 확인).
- CLK/MOSI 무신호 — MCSPI 드라이버가 SPI 클럭을 실제로 구동하지 않음. pinmux가 아님.
- 후보: ① `MCSPI_transfer` 미호출/반환 직전 종료 (app task block) ② `evaluations/spi0`가 외부핀 실증인지 미확인.

### R35 (cont.) — Saleae 계측 체인 known-good 검증 (spi0 eval)

**목적**: cc3351 CLK 침묵 해석 전, 계측 체인(Saleae+logic2+프로브+핀)이 정확한지 known-good 기준으로 검증.

**spi0 빌드 성질 확인 (소스 읽기)**:
- `evaluations/spi0/mcspi_loopback.c:92-100` → `while(1)` 무한송신으로 개조됨 (주석: "Pinmap probe: transfer forever so the scope always sees signal").
- `mcspi_loopback.c:67` 런타임 `bitRate=12500` 덮어씀 → 실제 SPI 클럭 12.5 kHz.
- `dpe0=ENABLE/trMode=TX_RX` → 외부 핀에 CLK·CS·MOSI(0xFF) 실토글, MISO(D1) 미구동.
- `.out` timestamp(13:19:24) > 소스(13:19:20) → 재빌드 불필요.

**측정**: 프로브 미이동(cc3351 측정과 동일 핀·헤더). D0=CS(P2.18), D1=CLK(P1.7), D2=MOSI(P2.15), D3=MISO(P2.14), GND=P2.20. 12.5 MS/s, 임계 3.3V, CS 하강엣지 트리거.

**결과 — 전 항목 합격**:
- CLK: 1024 사이클, 주기 80µs (12.5 kHz 정확).
- CS: burst 동안 active-low 프레임.
- MOSI: 128바이트 전부 0xFF 디코드 (POL0/PHA0, MSB, 8bit, CS active-low).
- MISO: 미구동 HIGH → 0xFF 읽힘 (정상).
- 단일 GND로 디코드 무결 → GND 추가 불필요 (저속 조건).

**레퍼런스 산출물**: `bp-3351/saleae_spi0_raw/` — `spi0_knowngood_12k5_0xFF.sal`(Logic2 캡처), `spi_decoded.csv`(128B 0xFF), `digital.csv`(raw 전이 1024클럭).

**캐비엣 해소 (cc3351 진단에 결정적)**:
프로브 미이동 + 동일 SPI0 핀 → spi0=1024클럭 / cc3351=0클럭. 측정·배선·pinmux·물리 매핑 전부 배제.

| 이전 caveat | 상태 |
|---|---|
| D1(CLK) 프로브 연결 미확정 | **✓ proven good** — 동일 프로브로 1024클럭 포착 |
| BP P1.7=SPI0_CLK 물리 매핑 미확정 | **✓ proven correct** — CLK 경로 실접속 확인 |
| Saleae/logic2 계측 체인 정확도 | **✓ proven** — 12.5 kHz 정밀 일치 |

**최종 결론**: cc3351 CLK 침묵 원인 = **펌웨어/SoC SPI 동작 자체** (MCSPI_transfer 실호출 여부·채널 enable·기능 클럭).

---

## R36 — MCSPI_transfer 마커 + 레지스터 덤프 → R35 "0클럭" 반증

**가설**: R35 CLK 0회 = MCSPI_transfer 미호출.

**변경**: `[R36-SPI] transfer count/ret` 마커 추가 — 호출·반환값 런타임 기록.

**관찰**:
- `[R36-SPI]` 로그: device-info 8회 전송 전부 `ret=SystemP_SUCCESS`, `status=MCSPI_TRANSFER_COMPLETED`.
- `transferTimeout=WAIT_FOREVER` 설정 — 무클럭이면 영구 hang, 완료 불가.
- 레지스터 덤프: `CH0CONF=0x20160FC8` (mode0/WL32/full-duplex/IS=D1/CLKD=2/CLKG=1/EPOL=1), `MODULCTRL=0x1` (single master), `SYSSTATUS=1`.
- SCLK ≈ 48 MHz / 3 ≈ **16 MHz** (CLKD=2, CLKG=1).
- MISO `rd#0/1=0xFFFFFFFF`, `rd#2~7=0x0` — NP 응답 부재.

**결론**:
- **R35 "CLK 0회" 반증** — MCSPI 마스터 정상 클럭·완료. R35 0클럭 관측은 **샘플링 아티팩트**: Saleae 12.5 MS/s로 16 MHz SPI 캡처 불가 (Shannon: ≥32 MS/s 필요). known-good 12.5 kHz는 12.5 MS/s로 충분했지만 16 MHz에는 턱없이 부족.
- **S6 블로커 재정의**: MCSPI(마스터) 정상. 원인 = **NP(CC33xx) SPI 비응답** — WLAN_IRQ 미발생, SPI not responsive/CMD_ERR_TIMEOUT.
- MISO rd#0/1 0xFFFFFFFF는 라인 부동(high) 상태, rd#2~7 0x0으로 전환 = NP가 초기에 라인을 구동하다가 멈추거나 전혀 준비되지 않은 것으로 추정.

### R36 (cont.) — Saleae 125 MS/s 물리 확인

**측정**: 125 MS/s, CS 트리거(하강엣지), D0=CS/D1=CLK/D2=MOSI/D3=MISO/D4=IRQ, GND=P2.20. 참고 로그: `saleae_r36_spi/raw6/digital.csv`.

**결과**:
- **CLK(P1.7)**: t≈14.09s에 ~16 MHz, ~4 µs 버스트 실측 — 물리 핀 SCLK 도달 확정.
- **MOSI(P2.15)**: 송신 활성 확인.
- **MISO(P2.14)**: flat 0 (Saleae) — NP가 데이터선을 전혀 구동하지 않음.
- **WLAN_IRQ(P1.8)**: flat — NP가 IRQ를 전혀 올리지 않음.
- **CS(P2.18)**: 전송 중 계속 asserted (프레임별 deassert 없음) — `spi_adapt.c csDisable=FALSE`. Saleae SPI 분석기 0 프레임 디코드의 원인(무클럭 아님).

**추가 확정**:
- 진단 마커 `[R36-SPI]` 블록(`spi_adapt.c`, MCSPI0 베이스=`0x52200000`) 코드에 유지. 커밋 미완 — R37에서 판단.
- **계측 교훈**: cc3351 SPI ~16 MHz·µs급 버스트 → Saleae ≥50 MS/s·CS 트리거 필수.

---

## 다음 계획 (R37)

**목표**: "MCSPI 정상 클럭·송신, NP(CC33xx)가 MISO·IRQ로 전혀 응답 안 함"의 NP측 원인 규명.

**우선순위**:

1. **NP 부팅/기동 경로 추적** — `Software download ! didn't receive HINT_ROM_LOADER_INIT_COMPLETE` / `Init device FAILED` 경로.
   - WLAN_EN(P1.5/M15) 토글 타이밍·레벨, NP 전원 인가, LP_RESET(active-low) 해제 순서 점검.
   - `cc33xx_2nd_loader`(0x900000)·`cc33xx_fw`(0x800000) 다운로드 시퀀스가 어디서 멈추는지 마커 확인.
2. **NP 물리 생존 여부** — 전원 레일·NP 동작 증거 확보. MISO/IRQ 무응답이 NP 미기동 때문인지, 배선/레벨 문제인지 구분.
3. **CS 프레이밍 정합** — `csDisable=FALSE`(연속 assert) vs CC33xx SDK 요구(워드별 CS deassert 기대 여부) 확인. `spi_adapt.c` vs CC33xx host SPI 프레이밍 규약 비교.

**검증 경로**: NP가 IRQ를 한 번이라도 올리거나 MISO를 구동하면 NP 기동 진전. Saleae MISO/IRQ 변화 확인.

---

## 함께 보기

- 증류된 확정/폐기: [[flash_open_facts]]
- 다음 시작점/현황: [[status]] · 전략 spine(S0~S8): [[porting]] · 프로젝트 호: [[roadmap]]
- 핸드오프 계약: [[sbl_app_flash_handoff]]
