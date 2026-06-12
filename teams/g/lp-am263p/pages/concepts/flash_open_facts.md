---
tags: [concept, flash, ospi, facts, diagnosis, am263p, s3-blocker]
source: [[flash_open_diagnostic_log]] + report.md (R19~R27)
date: 2026-06-01
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
| **DQ1-only 패턴** — 8D RDID 응답이 DQ1 한 라인만 활성(`02 03 03 03`), DQ[7:2]·DQ0 항상 0. **R28 귀인: pinmux 스크램블 증상으로 확정** — 8D-PHY 문제(가지 γ) 아님 | R20 최초, R25·R27 재확인; R28 귀인 확정 |
| `READ_DATA_CAPTURE_REG = 0x00000121` = **SBL 잔여 상태** (DQS_ENABLE bit8=1, SAMPLE_EDGE bit5=1, delay=1) | R25/R26/R27 레지스터 덤프 |
| `set888mode` opcode = **`0x81`** (IS25LX256 VCR write, 정상) | R27, `flash_nor_ospi.c:664` |
| jtag_flasher 성공 공식 = `flashFixUpOspiBoot()`(OSPI RESET 핀 HW 토글 → 1S) + `skipHwInit=FALSE`(set888mode로 1S→8D 승격) | `jtag_flasher/main.c:414`, `ti_board_config.c:60` |
| cc3351 app에는 `board_flash_reset`/`flashFixUpOspiBoot` 호출이 **전무** → app vs flasher 비대칭 원인 중 하나. ⚠️ R28 정정: **단일 최대 원인** 단정은 pinmux 스크램블(아래) 드러나기 전 결론 — H2(pinmux가 선행 필요조건인가) 검증 전까지 격하 | cc3351/main.c 직접 확인; R28 정정 |
| **cc3351 OSPI pinmux 스크램블 (R28)** — `$suggestSolution` vs `$assign` 한 글자로 7핀 오배치. CLK/DQS/D4/D6만 양쪽 일치. **주의: D4-D7은 MCAN pad(MODE2)가 정상** — "native everywhere" 교정 시 재파손. 상세 비교는 §아래. | R28: `ti_pinmux_config.c` 직접 비교, `example.syscfg` cc3351 L341-353 vs jtag_flasher L54-65 |
| `dummyClksCmd=8`, `quirksFxn=NULL` 필수 (런타임 패치 `cc3351/main.c:211-213`) | 과거 라운드 확정 |
| E9 소프트리셋(`0x66`+`0x99`)은 Flash_open 경로에서 금지 — `SetProtocol st=-1` 유발 | 과거 라운드 확정 |
| 빌드/플래시/부팅/진단 경로는 안정 동작 | R10~ |
| **S3 통과 (R28b 확정)** — pinmux `$assign` 교정 단독으로 RDID = `9D 5A 19` (manf=`0x9D` ISSI, dev=`0x5A19`) 정상 복귀, `Flash_open OK`. main.c 변경 없음. 커밋 bb56630. | R28b: `round28b.log` |
| **double-open 위험** — `network_terminal_entry()` 내부에서 `Drivers_open`(:1205)+`Board_driversOpen`(:1206) 자체 수행, 반환 직전 `Board_driversClose(:1265)`+`Drivers_close(:1266)`. freertos_main이 드라이버를 open/close하면 double-open/double-close st=-1 (round30 실측). | R29: round30.log |
| **in-place 패치 위치** — `ti_board_open_close.c` 전역 `gFlashParams`/`gFlashConfig`에 `network_terminal_entry` 호출 전 패치: `quirksFxn=NULL`, `skipHwInit=TRUE`, `dummyClksCmd=8`. `Board_driversOpen`이 그대로 읽는다. freertos_main은 드라이버를 건드리지 않는다. | R29: round31 검증, 커밋 3a06ab8 |
| **S4 통과 + CLI 도달 (R31 확정)** — Flash_open st=0, "Network Terminal upper_mac_3.0.5.12" 배너 + `user:` 프롬프트. ★ 표준 Board_flashOpen 단독 동작 최초 실측 검증. | R29: round31.log |
| **heap_size≥256KB 필수** — 32KB 공유 힙(`.sysmem`; libc malloc + FreeRTOS `pvPortMalloc` heap_3 공유)은 `wlan_start` 중 `os_malloc` NULL → FreeRTOS 큐 assert. `example.syscfg` general `heap_size=262144`(256KB)로 증설하면 assert 소멸 (`Hardware init DONE!` 도달). | R32: `cli_r32_wlanstart.log`, 커밋 853f3ac |
| **MCSPI inputSelect=D1 (MISO=SPI0_D1/B11/J2.14; MOSI=D0/C10/J2.15)** — inputSelect=D0+dpe0=TX_ENABLED는 SysConfig invalid(TX·RX 동일선/3-wire). D1로 교정 후 MISO 비-0 전환 (`0xFFFFFFFF`/변동). | R34: 커밋 71b732e |
| **JTAG connectTarget 항상 코어 리셋** → 부팅 앱 라이브 attach·assert 포착 불가. 진단은 UART 마커(`cli_interact.ps1`) 고정. | R31/R33 확정 |
| **LP-AM263P ↔ BP-CC3351 SPI/GPIO 확인 결선** — J1.7=SPI0_CLK(A11), J2.15=SPI0_D0(C10/MOSI), J2.14=SPI0_D1(B11/MISO), J2.18=SPI0_CS0(C11), J1.5=WLAN_EN(M15), J1.8=WLAN_IRQ(G18). BP P1.5=LP_RESET(active-low), P1.7=CLK, P2.14=MISO, P2.15=MOSI, P2.18=CS. | 사용자 직접 확인; SWAU132A Table 2-3/2-4 |
| **SPI0↔헤더 mux 설정 불필요 추정** — LP-AM263P SPI0는 2:1 mux(SN74CB3Q3257)+TCA6416 경유이나 TI LP SPI0 예제가 mux init no-op로 동일 핀(A11/C10/B11/C11) 동작. | R33 |
| **CS(P2.18) 물리 어서트 확인** — Saleae 실측: ~1.008µs LOW 펄스 1회. CS pinmux + SPI0 CS 배선 정상. | R35 |
| **CLK(P1.7)/MOSI(P2.15) 물리 핀 무신호 — R36에서 반증** — R35 "0클럭"은 샘플링 아티팩트(Saleae 12.5 MS/s로 SCLK 16 MHz 캡처 불가). MCSPI 마스터는 정상 클럭·완료(R36 firmware-internal 증거). | R35→R36 반증 |
| **CLK 침묵 원인은 IOMUX 바깥** — SPI0_CLK/D0/D1/CS0 pinmux가 evaluations/spi0 실증과 cc3351 모두 PIN_MODE(0) 동일. Pinmux_init() 경유 확인. pinmux 재교정 불필요. | R35 |
| **RTOS idle hook 안착 (크래시 아님)** — wlan_start 후 `vApplicationIdleHook`(port.c:405)에 안착. app task 종료 또는 블록 상태. | R35 |
| **Saleae 계측 체인 proven (저속 한정)** — spi0 known-good(12.5 kHz, 0xFF×128B)에서 D1 프로브·P1.7 물리 매핑·계측 정확도 확인. **단, 12.5 MS/s 샘플링으로 ~16 MHz SPI 캡처 불가** — R35 0클럭 관측의 원인. R37에서 ≥50 MS/s 재캡처 필요. | R35(cont.)·R36 보완 |
| **MCSPI 정상 동작 확정** — transferTimeout=WAIT_FOREVER에서 device-info 8회 전송 전부 `ret=SystemP_SUCCESS·status=MCSPI_TRANSFER_COMPLETED`. CH0CONF=`0x20160FC8`(mode0/WL32/full-duplex/IS=D1/CLKD=2/CLKG=1/EPOL=1), MODULCTRL=`0x1`(single master), SYSSTATUS=1. SCLK ≈ 48 MHz/3 = **16 MHz**. | R36 |
| **S6 블로커 = NP(CC33xx) SPI 비응답 (물리 확인)** — firmware: MISO rd#0/1=0xFFFFFFFF·rd#2~7=0x0. Saleae: MISO(P2.14) flat 0·WLAN_IRQ(P1.8) flat. NP가 데이터선·IRQ 전혀 구동 안 함. `SPI not responsive/CMD_ERR_TIMEOUT`. **[H1 확정 R37]**: 마스터 정상(CH0STAT=0x6=EOT+TXS, RXS=0; CH0CONF WL=32/full-duplex/FFER=1, CSL 헤더 교차확인) + NP 침묵을 R36 단일 로그가 이미 입증. R37 신규 측정은 R36 답의 재발견 — 무게중심 NP 부팅·응답 쪽으로 이동. | R36·R36(cont.)·R37 |
| **CS 연속 assert (csDisable=FALSE)** — `spi_adapt.c csDisable=FALSE`: CS가 전송 중 deassert 안 됨. Saleae SPI 분석기 0프레임 디코드 원인(무클럭 아님). CC33xx SDK의 프레이밍 기대(워드별 CS deassert)와 정합 여부 미확인. | R36(cont.) |
| **R38 라인레벨 — 마스터 정상·NP 전핀 침묵 확정**: SCLK 64사이클(~16.7MHz)·MOSI 12전이·CS 전구간 asserted·MISO 0전이(flat 0)·IRQ_WL/IRQ_BLE/LOGGER 침묵. | R38: saleae_r38_sanity/digital.csv |
| **R38 배제 확정** — 전원(3.266V/1.794V, 디스크 직접 미검증)·nRESET 해제(D1 Yellow LED=LP_RESET HIGH)·level-shifter(J12/J13/J14=3.3V) 정상. master SPI 정상. | R38: 육안 + Saleae |
| **NP 코어 미실행(1순위 XTAL)** — 전원·리셋·클럭공급·level-shifter 갖춰진 상태에서 NP가 SPI·IRQ(WL/BLE)·LOGGER 4계통 전부 침묵. 1순위 의심 40MHz XTAL(Y1) 미발진(추론, 미측정). | R38 |
| **sop2 "LOGGER 활발=생존" 판단 철회** — LOGGER 99.14% idle-high, 2.6s low=공통모드 리셋. 리셋창 밖 low 전부 ≤3µs(UART 아님). 장시간·리셋포함 캡처 "활발=생존" 직관 금지. | R38: saleae_r38_sop2/digital.csv |

칩 클래스 차이(AM243 `S25HL512T` Quad vs AM263P `IS25LX256` Octal native)는 [[is25lx256_vs_spansion_quirks]], dummy 근거는 [[xspi_dummy_cycles]], Open 시퀀스는 [[flash_open_sequence]] 참조.

### cc3351 OSPI pinmux 스크램블 (R28 발견)

cc3351 `example.syscfg`가 OSPI 핀을 `$suggestSolution`(soft 힌트)으로 둬,
SysConfig 솔버가 7개 핀을 엉뚱한 pad에 MODE(6)으로 오배치. jtag_flasher는
`$assign`(hard lock)으로 native pad에 정상 고정 — 이 한 글자 차이가 근원.

| 핀 | jtag_flasher (known-good) | cc3351 (스크램블) |
|----|---------------------------|-------------------|
| CSn0 | OSPI0_CSn0 (P1) M0 | EPWM11_A (H1) M6 |
| D0 | OSPI0_D0 (N1) M0 | OSPI0_CSn0 (P1) M6 |
| D1 | OSPI0_D1 (N4) M0 | EPWM11_B (J1) M6 |
| D2 | OSPI0_D2 (M4) M0 | MCAN0_TX (L1) M6 |
| D3 | OSPI0_D3 (P3) M0 | EPWM13_A (K4) M6 |
| D5 | MCAN0_TX (L1) M2 | EPWM12_A (K2) M6 |
| D7 | MCAN1_TX (K1) M2 | EPWM12_B (J4) M6 |
| RESET_OUT0 | EPWM11_B (J1) M2 | EPWM10_B (J3) M5 |

CLK/DQS/D4/D6는 양쪽 일치. **주의: D4-D7은 native OSPI pad가 아니라 MCAN pad(MODE2)가
정상** — LP-AM263P 물리 배선. "native everywhere"로 교정하면 다시 깨짐.

출처: 양 프로젝트 `Release/syscfg/ti_pinmux_config.c` 직접 비교,
`example.syscfg`(cc3351 L341-353 `$suggestSolution` / jtag_flasher L54-65 `$assign`).

---

## 폐기된 가설 (재시도 금지)

| 폐기된 길 | 반증 | 라운드 |
|-----------|------|--------|
| `DQS_ENABLE=0` (READ_DATA_CAPTURE_REG 클리어)로 캡처 살리기 | DQS 없으면 8D DDR 캡처 **전부 FF** → SetRdCap st=-1. 8D DDR엔 DQS 필수 | **R26 반증** |
| `set888mode` opcode = `0x71` | 실제 `0x81`. `0x71`은 Spansion WRAR로 quirksFxn 경로 전용(이미 NULL 차단), set888mode와 무관 | **R27 폐기** |
| `skipHwInit=FALSE`로 진단 | SBL 잔여 상태에서 `set888mode` 쓰기 st=-1, status 누적 구조로 이후 단계 신호 오염 → 진단 라운드 자체가 무효 | **R25 폐기** |
| CONFIG_REG bit30 DUAL_BYTE_OPCODE_EN 잔류가 원인 | 이미 0임을 확인 | **R24 폐기** |
| RDCAP 레지스터 4조합(0x121·0x021·0x001·0x101) 튜닝으로 해결 | 전부 indirect sweep 실패 | R16~R19 |
| **R7~R27 SBL-핸드오프/skipHwInit/DQS/RDCAP-tuning 귀인 전체** | "pinmux 정상"이라는 잘못된 전제 위에 쌓인 것 — R28b pinmux 교정 단독으로 S3 통과. 귀인 전부 무효 | **R28 일괄 폐기** |
| **R35 "CLK 0회" = MCSPI 클럭 미출력** | R36 firmware-internal: transferTimeout=WAIT_FOREVER에서 8회 전송 ALL_SUCCESS. 원인 = Saleae 12.5 MS/s로 SCLK 16 MHz 캡처 불가(샘플링 부족) | **R36 반증** |

---

## S3 해소 (R28b 확정) / 현재 블로커 (R29)

**S3 해소** — R28b: cc3351 `example.syscfg` OSPI pinmux를 `$assign`(hard lock)으로 교정하자 RDID = `9D 5A 19` (정상), `Flash_open OK`. main.c 변경 없음.

R7~R27에서 쌓인 SBL-핸드오프/skipHwInit/DQS/RDCAP-tuning 귀인은 전부 "pinmux 정상"이라는 잘못된 전제 위에 쌓인 것 → 폐기 (위 표). "DQ1-only RDID"는 8D-PHY 문제(가지 γ)가 아니라 핀 스크램블 증상이었음.

**S4 해소 (R31)** — `ti_board_open_close.c` 전역에 in-place 패치(`quirksFxn=NULL`, `skipHwInit=TRUE`, `dummyClksCmd=8`) + freertos_main 원본 구조 복원 → `Board_driversOpen` 완주, CLI 프롬프트 도달. ★ 표준 Board_flashOpen 단독 동작 최초 실측 검증.

**R36 현황**: MCSPI 정상(8회 ALL_SUCCESS, SCLK~16 MHz). S6 블로커 = NP(CC33xx) SPI 비응답. R37: Saleae ≥50 MS/s로 물리 SCLK 확정 + NP 비응답 원인(WLAN_IRQ/2nd-loader/NP 부팅) 조사.

---

## 모름 / 미확인

- **[H-A] skipHwInit=TRUE 의존성** — `skipHwInit=TRUE`는 `Flash_norOspiSetProtocol` 내부 쓰기(4ByteAddr/protocol/set888 VCR)만 가드. `SetRdCap`(:1332)·`PhyTune`(:1336)은 가드 밖 항상 실행. round31 성공이 "SBL 핸드오프 8D 유지"에 의존한 것인지, PHY tuning이 독립 동작한 것인지 미확정.
- **R28b 최소 충분 패치셋 미분리** — quirksFxn=NULL / skipHwInit=TRUE / dummyClksCmd=8 세 패치를 동시 적용하여 1회 성공. 어느 것이 필수인지 미확인.
- **flash FS 쓰기 미검증** — `osi_filesystem.c:131` "Skip flash writing due to APIs issue" 경고. stub일 수 있음. Flash_open 성공 ≠ flash 읽기/쓰기 동작.
- SBL이 OSPI 부팅 시 chip을 **어느 프로토콜로 app에 넘기는가** — 실용적 중요도 낮아짐. 참고용. (※ 부팅 스트랩은 4S `1,1,1,1`이 아니라 **xSPI 8D SFDP `0,0,1,1`** — octal-only 칩, [[ospi_boot_mode_strap]].)
- BoosterPack 헤더 ↔ SoC 핀 물리 대응표 — CLK(P1.7=SPI0_CLK/A11/J1.7) R36(cont.) 125 MS/s 실측 확인. MOSI/MISO/CS는 spi0 known-good 디코드 정합으로 간접 확인 수준.
- CC33xx `csDisable=FALSE` vs SDK 프레이밍 요구 미확인 — R37 CS 프레이밍 정합 검증 필요.
- **40MHz XTAL(Y1) 발진 미측정** — 1순위 가설이나 직접 측정 없음. R39 오실로스코프 대상.
- **SoP strap 1.8V IC측 미측정** — LP헤더(3.3V측)에선 못 읽음(level shifter 리셋 게이팅). R7/R8 직접 프로브 필요.
- **SPI 링크 1.8V IC측 도달 미검증** — Saleae는 전부 LP헤더(3.3V)측 측정.
- **sop2 t=283–293s SCLK 버스트 출처 불명** — wlan_start 176s 뒤, CS asserted·정상 period. 반례 후보이나 MISO 5전이로 NP 응답 증거 아님.

---

## 함께 보기

> **층위 구분 주의**: 이 페이지(S3~)는 **cc3351 app 런타임 `Flash_open()`** 블로커다. 같은 보드·같은 IS25LX256를 쓰는 **8kw standalone 부팅 무부팅**(별 프로젝트)의 원인은 전혀 다른 층위 — 부트모드 핀 스트랩 미스매치([[ospi_boot_mode_strap]], 2026-06-12 해소)였다. 두 문제를 섞지 말 것. (단 이 페이지의 pinmux 스크램블·skipHwInit 귀인은 standalone 스트랩과 무관하게 유효.)

- 라운드별 시간순 기록: [[flash_open_diagnostic_log]]
- **JTAG flash 하네스·굽기 규율(flash-time, 층위 다름)**: [[jtag_flash_harness]] — runAsynch 하네스 vs DSS Rhino·클린 호스트·파워 사이클·standalone 부팅 검증. 이 페이지(app `Flash_open()` 런타임 블로커)와 별개. 재플래시(6/6 OK)가 흔들리면 1순위 의심. 클린-호스트 deep-dive는 [[jtag_flash_clean_host]].
- 전략 spine: [[roadmap]] · 다음 시작점/현황표: [[status]]
- SBL→app 핸드오프 계약: [[sbl_app_flash_handoff]]
- Spansion↔ISSI 포팅 차이: [[is25lx256_vs_spansion_quirks]]
- Open 시퀀스: [[flash_open_sequence]]
