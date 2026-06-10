---
tags: [entity, am263p, launchpad, schematic, uart5, mux, boosterpack, platform]
source:
  - teams/g/lp-am263p/raw/proc171_schematic/ (TI PROC171A LP-AM263P 회로도, SPRR503A)
  - PROC171_AM263P_6_ePWM_eQEP_FSI.SchDoc (Sheet 11) — U54 먹스
  - PROC171_IO_EXPANDER.SchDoc (Sheet 23) — U63 TCA6416
date: 2026-06-10
---

# LP-AM263P UART/EPWM 부스터팩 먹스 (U54 SN74CB3Q3257 + U63 TCA6416)

> **AM263P 플랫폼 하드웨어 사실.** LP-AM263P 온보드에 **UART5와 EPWM9를 부스터팩 헤더 핀에 다중화하는 FET 버스스위치 먹스**가 있다. UART5가 BP 헤더로 나가려면 이 먹스가 UART 쪽으로 선택·인에이블돼야 하며, 제어선은 **I2C IO expander(TCA6416 @0x20)** 가 구동한다 — GPIO가 아님. 8kw-ev-wpt-tx·lp-am263p 공용. 형제: [[am263p_iomux_force_io_enable]](핀먹스/PADCONFIG 층위), [[schematic_lp_am263p]](소스).

## 한 줄 요약

**LP-AM263P의 부스터팩 헤더 "EPWM15" 핀은 UART5(P15/R16)도 EPWM9도 될 수 있는 다중화 핀이고, 둘 중 무엇이 헤더로 나갈지는 U54(SN74CB3Q3257) 먹스가 정한다.** 그 먹스의 SEL·EN은 TCA6416(U63) I2C IO expander 포트(P00/P14)가 구동하므로, **펌웨어가 I2C1로 expander를 설정하지 않으면 먹스 상태는 미정** — UART5가 헤더에 안 나타날 수 있다. ★ 이것은 [[am263p_iomux_force_io_enable]]의 SoC 핀먹스/PADCONFIG와 **완전히 별개인 보드-레벨 게이트**다.

---

## 확정 사실 (회로도 네트리스트·시트 11/23 교차검증)

### 1. 먹스 U54 = SN74CB3Q3257 (4비트 1-of-2 FET 버스스위치)

`PROC171_AM263P_6_ePWM_eQEP_FSI.SchDoc` (Sheet 11). SN74CB3Q3257PWR. A=공통, B1/B2 두 입력을 `S`로 선택, `OE#`로 게이팅.

| 채널 | A (BP 헤더, 공통) | B1 (`S` 한쪽) | B2 (`S` 다른쪽) |
|------|-------------------|---------------|------------------|
| ch1 | `AM263P_EPWM15_A_BP` (1A) | `AM263P_UART5_TXD` (1B1) | `AM263P_EPWM9_A` (1B2) |
| ch2 | `AM263P_EPWM15_B_BP` (2A) | `AM263P_UART5_RXD` (2B1) | `AM263P_EPWM9_B` (2B2) |

- 제어핀: **pin 1 = `S`(SEL) ← `UART/EPWM_MUX_SEL`**, **pin 15 = `OE#`(EN, active-low) ← `UART/EPWM_MUX_EN`**.
- ch3/ch4는 OSPI_ECS·EPWM11/12 등 다른 BP 공유핀 (이 페이지 범위 밖).
- => BP 헤더의 `EPWM15_A_BP`/`EPWM15_B_BP` 핀은 **UART5_TXD/RXD** 또는 **EPWM9_A/B** 중 하나만 통과시킨다. UART5를 쓰려면 SEL이 UART(B1)쪽 + EN(OE#) 인에이블.

### 2. SEL/EN을 구동하는 것 = TCA6416 IO expander (U63), I2C1 @ 0x20

`PROC171_IO_EXPANDER.SchDoc` (Sheet 23). TCA6416ARTWR, **AM263P_I2C1**(SCL/SDA), **I2C 주소 0x20** (ADDR→IO_ADDR).

| expander 포트 | 신호 | 핀(U63) |
|---------------|------|---------|
| **P00** | `UART/EPWM_MUX_SEL` | pin 1 |
| **P14** | `UART/EPWM_MUX_EN` | pin 14 |

- 같은 expander가 MMC_MUX, BP_MUX_SEL, PRU_MUX_SEL, LED_EN, 각종 RST_EN 등 보드 전체 먹스/인에이블을 일괄 구동.
- **`UART/EPWM_MUX_SEL`·`_EN` 네트에 풀저항 없음** (전 페이지 검색 0건) → 기본 상태를 정하는 외부 풀이 없다. TCA6416은 리셋 시 전 포트가 **입력(하이임피던스)**, 출력 레지스터 디폴트=1. => **펌웨어가 expander를 설정하기 전 두 제어선은 부정(floating)** — 먹스 통과 보장 없음.

---

## 8kw-ev-wpt-tx 함의 (★ UART5 미동작 후보, 가설)

[[am263p_iomux_force_io_enable]]은 8kw UART5 미동작의 펌웨어 IOMUX/PADCONFIG 원인을 배제하고, 남은 원인을 ① `UART_write` 주석 + ② RS-485 DE(`EN_485`) 미구현으로 봤다. 여기에 **LP-측 제3 후보**가 추가된다:

> **[가설, 미검증]** 8kw가 UART5를 BP 헤더(`EPWM15_x_BP`, 멀티플렉스 핀)에서 탭한다면, **LP의 U54 먹스가 UART 쪽으로 선택·인에이블돼 있어야** 신호가 헤더에 나온다. 그 제어는 TCA6416(0x20, I2C1)을 통하므로 **펌웨어가 expander를 설정해야** 한다. 8kw 펌웨어가 TI LP-AM263P Board 초기화(expander 디폴트 설정)를 포함하지 않거나 바꿨다면, 먹스가 UART5를 차단해 콘솔(UART0)은 멀쩡한데 UART5 차동라인만 죽는 현상과 정합한다.

- **대조 필요**: lp-am263p loopback eval(`evaluations/uart5/empty.c`, J1.4↔J1.3)은 UART5 송수신이 **동작했다고 기록됨** ([[am263p_iomux_force_io_enable]] §UART5 사례). 그게 BP 헤더(post-mux) 경로였다면 그 시점 먹스는 UART로 설정돼 있었다는 뜻 → 누가 설정했나(TI Board init?)를 확인하면 8kw에서 빠진 단계가 드러난다.
- **검증 행동**: ① 8kw·lp-am263p 펌웨어에서 TCA6416(0x20) I2C 설정 코드 유무 grep, ② JTAG로 expander 출력 레지스터 read해 P00/P14 실제 구동값 확인, ③ U54 BP 헤더핀에 스코프 — UART 쪽 선택 시에만 UART5 파형.

---

## 확인 필요 / 미검증

- **BP 헤더 J-핀 번호 정합**: 회로도 net은 `EPWM15_A_BP`→핀 34, `EPWM15_B_BP`→J7.45 부근으로 추출됐으나, [[lp_am263p_ug]] 핀맵은 UART5 TXD/RXD를 **J1.4/J1.3**로 표기. 헤더 번호 체계(회로도 J5~J8 물리 vs UG J1~J4 BoosterPack 논리)가 달라 **물리 핀 1:1 정합 미확정.** UG §2.20 BoosterPack Headers / §2.21 Pinmux로 교차확인할 것.
- **J1.4가 post-mux인지 pre-mux(직결 P15 탭)인지 미확정.** 이게 8kw 함의의 전제 — post-mux여야 먹스가 8kw 경로에 든다. (scrambled pdftotext만으론 단정 불가 → 회로도 PDF 해당 핀 시각 확인 또는 IPC 네트리스트 결선 교차.)
- **SEL 극성**: SEL=어느 레벨이 UART(B1)인지 회로도에서 미확정. SN74CB3Q3257은 통상 S=L→B1, S=H→B2. 데이터시트 + expander 출력값으로 확정.
- **TCA6416 디폴트/누가 설정**: 위 가설의 핵심. 펌웨어·SysConfig Board 설정 확인 필요.

---

## 관련 페이지

- [[schematic_lp_am263p]] — 이 사실의 소스(회로도 ingest 인덱스).
- [[am263p_iomux_force_io_enable]] — SoC 핀먹스/PADCONFIG 층위. **이 먹스는 그 아래(보드) 층위** — 둘 다 통과해야 UART5가 헤더에 산다.
- [[lp_am263p_ug]] — BP 헤더 핀맵(§2.20/2.21)·IO Expander(§2.1.4) 교차확인.
- 8kw [[status]] — UART5 미동작 미결(이 가설 반영 대상).
