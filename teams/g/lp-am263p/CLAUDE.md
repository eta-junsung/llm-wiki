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
| 전략 | [[roadmap]] (`roadmap.md`) | S0~S8 spine·현재 위치·남은 일정. 디테일은 concept 백링크 위임 | 게이트 통과 시 |
| 전술 | [[status]] (`status.md`) | 다음 시작점 한 줄·기능별 구현 현황표·미결 사항 | 매 라운드 (파이프라인) |
| 누적 사실 | [[flash_open_facts]] | **확정 사실 + 폐기 가설(재시도 금지)**. 증류된 현재 진실. 제자리 수정 | 매 라운드 |
| 누적 history | [[flash_open_diagnostic_log]] | R7~ 라운드별 가설→변경→관찰→결론. **append-only, 옛 항목 불변** | 매 라운드 append |

**규칙**: 새 라운드 결과는 ① `flash_open_diagnostic_log`에 append → ② 확정/폐기된 것을 `flash_open_facts`에 반영 → ③ 필요 시 status·roadmap 갱신. 사실 나열은 facts/log가 단일 소스이고, roadmap/status는 그곳으로 위임만 한다.

그 외 concept/source/entities/raw는 루트 `CLAUDE.md` 컨벤션을 따른다.

---

## 하드웨어 — 부트 모드 / boot flow

**SW1 부트 모드 스위치**:

| SW1 (1,2,3,4) | 모드 |
|---|---|
| `1,1,0,0` | DevBoot |
| `1,1,1,1` | OSPI 4S Quad Read |

**boot flow**: ROM → SBL(`sbl_ospi_am263p.tiimage`) → app @`0x81000`. 부트 플래시는 OSPI **IS25LX256**(ISSI, 32MB, Octal xSPI 8D DDR), base `0x53808000`. BoosterPack과 무관한 AM263P 온보드 플래시.

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
