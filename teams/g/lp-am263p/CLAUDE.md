# lp-am263p — 도메인 schema

## 프로젝트 성격

TI **LP-AM263P** LaunchPad에 **BP-CC3351**(Wi-Fi 6 + BLE BoosterPack)을 얹어, CC33XX SDK 공식 예제 `CC3xx_thick_mac_network_terminal`을 구동하는 포팅 작업.

원본 예제의 타겟은 **LP-AM243**이며, CC33XX SDK(R8.1)는 AM263P용 공식 예제·targetConfig·syscfg를 제공하지 않는다 → **이 포팅은 TI 공식 지원 밖(비공식)**. syscfg·드라이버·플래시 정합성을 직접 맞춰야 한다.

현재 상태: **S3 블로커** — 부팅 직후 app의 `Flash_open()`(AM263P 부트 플래시 IS25LX256)이 NULL 반환하는 단계에서 27+ 라운드째 막혀 있음. 전체 그림은 [[roadmap]], 지금/다음은 [[status]].

코드 repo: `~/eta/projects/g/lp-am263p/bp-3351/` (이 wiki와 별개).

---

## 페이지 분류 — 3-레이어 (초장기 디버그 작업용)

이 프로젝트는 초장기 진단 작업이라 "맥락 유실 방지"가 wiki의 1차 목적. 페이지를 세 성격으로 분리한다:

| 레이어 | 페이지 | 성격 | 갱신 |
|--------|--------|------|------|
| 전략(프로젝트) | [[roadmap]] (`roadmap.md`) | 프로젝트 목표·작업 호 인덱스·현재 위치. 단계 spine은 작업 로드맵 위임 | 게이트 통과 시 |
| 전략(작업) | [[porting]] (`roadmaps/porting.md`) | S0~S8 단계 spine·완료 기준 표·남은 일정. 디테일은 concept 백링크 위임 | 게이트 통과 시 |
| 전술 | [[status]] (`status.md`) | 다음 시작점 한 줄·기능별 구현 현황표·미결 사항 | 매 라운드 (파이프라인) |
| 누적 사실 | [[flash_open_facts]] | **확정 사실 + 폐기 가설(재시도 금지)**. 증류된 현재 진실. 제자리 수정 | 매 라운드 |
| 누적 history | [[flash_open_diagnostic_log]] | R7~ 라운드별 가설→변경→관찰→결론. **append-only, 옛 항목 불변** | 매 라운드 append |

**규칙**: 새 라운드 결과는 ① `flash_open_diagnostic_log`에 append → ② 확정/폐기된 것을 `flash_open_facts`에 반영 → ③ 필요 시 status·roadmap 갱신. 사실 나열은 facts/log가 단일 소스이고, roadmap/status는 그곳으로 위임만 한다.

그 외 concept/source/entities/raw는 루트 `CLAUDE.md` 컨벤션을 따른다. 위 전략/전술(roadmap·status) 짝의 일반 규약은 루트 `CLAUDE.md` "로드맵 컨벤션" 절을 따른다 — 이 표는 그 프로젝트별 구현. 작업 단위 호가 필요하면 `roadmaps/<task>.md`.

---

## 하드웨어 — 부트 모드 / boot flow

**SW1 부트 모드 스위치** — 근거: LP-AM263P UG SPRUJ85B Table 2-5 ([[raw/lp_am263p_ug/ug_lp-am263p.md]] :463–470).

컬럼 순서는 UG 표기 그대로 **SW1.4 / SW1.3 / SW1.2 / SW1.1** (왼→오른쪽). 스위치 ON = SOP 핀을 GND로 당김 = **논리 0** (:453) — SOP 레벨의 논리 반전임에 주의.

| 모드 | SW1.4 | SW1.3 | SW1.2 | SW1.1 |
|---|---|---|---|---|
| OSPI (4S) Quad Read | 1 | 1 | 1 | 1 |
| UART | 1 | 1 | 1 | 0 |
| OSPI (1S) Single Read | 1 | 1 | 0 | 1 |
| OSPI (8S) Octal Read | 1 | 1 | 0 | 0 |
| **DevBoot** | **0** | **1** | **0** | **0** |
| xSPI 8D (SFDP) | 0 | 0 | 1 | 1 |

> 정정(2026-06-05): 기존 표는 DevBoot를 `1,1,0,0`으로 적었으나 이는 **OSPI (8S) Octal Read** 값의 오기였다. DevBoot 정확값은 `0,1,0,0`(SW1.3만 ON) — UG Table 2-5 :469. DevBoot = "No SBL. Used for development purposes only." (Table 2-6 :494). 기존 헤더 `SW1 (1,2,3,4)` 라벨도 실제 기입값이 UG의 SW1.4-우선 순서였어 혼동을 유발 → 헤더를 UG 순서로 명시.

**boot flow**: ROM → SBL(`sbl_ospi_am263p.tiimage`) → app @`0x81000`. 부트 플래시는 OSPI **IS25LX256**(ISSI, 32MB, Octal xSPI 8D DDR), base `0x53808000`. BoosterPack과 무관한 AM263P 온보드 플래시.

**리셋/푸시버튼** — 근거: UG Table 2-4(:431), Figure 2-10/2-11(:586–657) · 회로도 sheet 6 `PROC171_AM263P_2_Clock_Reset_Boot_JTAG.SchDoc`.

| 버튼 | 신호 | 성격 | 묶이는 곳 |
|---|---|---|---|
| **SW2** | **PORz** | **Power-On Reset(콜드급)** — SoC MAIN 도메인 | SoC PORz 입력 + Boot mode State Driver **U4** OE(`PORZ_DELAY` RC ~1ms로 SOP 핀 `tSOP.hold` 유지) |
| SW3 | RESETz / WARMRESETn | warm reset | SoC WARMRESETN + **양 Ethernet PHY reset** + μSD load switch(GPIO122 AND) |
| SW4 | INT1 | user interrupt | — |

PORz는 **3-입력 AND**(3.3V 벅 PG `PG_VSYS_3V3` · 1.2V 벅 PG `PG_VDD_1V2` · SW2 비눌림)로 생성, PMOS 풀다운으로 `TA_PORZ`(테스트자동화)·`BP_PORZ`(BoosterPack)도 assert 가능. SW2 PORz를 누르면 SOP 핀(SW1 부트모드) 재래치 + ROM 콜드 재실행.

> ⚠️ **SW2 PORz·SW3 RESETz 어느 버튼도 OSPI flash를 POR하지 못한다** — PORz/WARMRESETn 트리에 flash 3.3V 전원도 flash RESET#(`AM263P_OSPI0_RST`, SoC OSPI_RESET_OUT가 SW 구동)도 묶여 있지 않음. >128Mb flash가 4-byte stuck이면 버튼 리셋으론 ROM(3-byte) 부팅이 안 풀린다 → **진짜 VCC 제거(flash POR)만이 3-byte 기본값 복귀**. 근거·맥락 [[toggle_free_flash_loop]] §③, TRM §5.4.1 Note.

host↔CC33xx 인터페이스(syscfg 기준): MCSPI `SPI0` 20MHz EDMA, WLAN_EN=`PR0_PRU0_GPIO12`, WLAN_IRQ=`PR0_PRU0_GPIO10`(RISE), BLE HCI=`USART2` 9600, console=`USART0` 115200. BoosterPack 헤더(J1~J4)↔SoC 핀 물리 대응표는 **미확인**.

---

## 자주 어긋나는 자리 (페이지 만들기/갱신 전 필독)

- **E9 소프트리셋(`0x66`+`0x99`) 금지** — Flash_open 경로에서 `SetProtocol st=-1` 유발.
- **`dummyClksCmd=8`, `quirksFxn=NULL` 필수** — 런타임 패치 `cc3351/main.c`. 근거 [[xspi_dummy_cycles]].
- **`set888mode` opcode=`0x81`** (IS25LX256 VCR write, 정상). `0x71`은 Spansion WRAR로 quirksFxn 경로 전용 — set888mode와 무관. [[is25lx256_vs_spansion_quirks]] §6.5.
- **`idCfg.dummy8`은 RDID 전용 별도 필드** — 일반 dummy와 분리. 진단 시 빼먹지 말 것. [[flash_open_sequence]].
- **"커밋됨 ≠ 실보드 검증됨"** — status 표 상태 기호 `△`(미검증)와 `✓`(검증) 구분 엄수.
- **폐기 가설 재시도 금지** — DQS_ENABLE=0(R26 반증) 등은 [[flash_open_facts]] "폐기된 가설" 절에서 먼저 확인.

---

## cross-project 참조 (first-ingest-wins)

- 원본 보드 자료(회로도·핀맵·전원)는 [[bp-cc3351]] 프로젝트가 보관 → 백링크 참조.
- flash 데이터시트 [[is25lx256_datasheet]]는 이 프로젝트에 first-ingest됨.

## status 갱신 절차

루트 `CLAUDE.md` "파이프라인 — status 갱신 절차" 준수. `status.md` 위치: `teams/g/lp-am263p/status.md`.
