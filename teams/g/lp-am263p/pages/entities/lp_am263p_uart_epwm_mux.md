---
tags: [entity, am263p, launchpad, schematic, uart5, mux, boosterpack, platform]
source:
  - teams/g/lp-am263p/raw/proc171_schematic/ (TI PROC171A LP-AM263P 회로도, SPRR503A)
  - PROC171_AM263P_6_ePWM_eQEP_FSI.SchDoc (Sheet 11) — U54 먹스
  - PROC171_IO_EXPANDER.SchDoc (Sheet 23) — U63 TCA6416
  - SN74CB3Q3257 데이터시트 SCDS135E, Table 6-1 Function Table
date: 2026-06-10
---

# LP-AM263P UART/EPWM 부스터팩 먹스 (U54 SN74CB3Q3257 + U63 TCA6416)

> **AM263P 플랫폼 하드웨어 사실.** LP-AM263P 온보드에 **UART5와 EPWM9를 부스터팩 헤더 핀에 다중화하는 FET 버스스위치 먹스**가 있다. UART5가 BP 헤더로 나가려면 이 먹스가 UART 쪽으로 선택·인에이블돼야 하며, 제어선은 **I2C IO expander(TCA6416 @0x20)** 가 구동한다 — GPIO가 아님. 8kw-ev-wpt-tx·lp-am263p 공용. 형제: [[am263p_iomux_force_io_enable]](핀먹스/PADCONFIG 층위), [[schematic_lp_am263p]](소스).
>
> ⚠️ **UG 본문(`ug_lp-am263p.md :1123` "UART2 & UART5 directly mapped", `:1447` "EPWM 헤더 외부먹스 없음")은 U54 먹스를 명시하지 않는다 — 오해 소지 표기. 회로도(SPRR503A)가 정본.**

## 한 줄 요약

**LP-AM263P의 부스터팩 헤더 핀 J1.4/J1.3은 UART5(GPIO73/74) 또는 EPWM9 중 하나만 통과시키는 다중화 핀이고, 어느 쪽이 나갈지는 U54(SN74CB3Q3257) 먹스가 정한다.** 그 먹스의 SEL·EN은 TCA6416(U63) I2C IO expander 포트(P00/P14)가 구동하므로, **펌웨어가 I2C1로 expander P00/P14=LOW를 세팅하지 않으면 먹스 상태는 미정** — UART5가 헤더에 안 나타날 수 있다. ★ 이것은 [[am263p_iomux_force_io_enable]]의 SoC 핀먹스/PADCONFIG와 **완전히 별개인 보드-레벨 게이트**다.

---

## 확정 사실 (회로도 네트리스트·시트 11/23 + 데이터시트 교차검증)

### 1. 먹스 U54 = SN74CB3Q3257 (4비트 1-of-2 FET 버스스위치)

`PROC171_AM263P_6_ePWM_eQEP_FSI.SchDoc` (Sheet 11). SN74CB3Q3257PWR. A=공통, B1/B2 두 입력을 `S`로 선택, `OE#`로 게이팅.

| 채널 | A (BP 헤더, 공통) | B1 (`S` 한쪽) | B2 (`S` 다른쪽) |
|------|-------------------|---------------|------------------|
| ch1 | `AM263P_EPWM15_A_BP` (1A) → **J1.4 = GPIO73** | `AM263P_UART5_TXD` (1B1) | `AM263P_EPWM9_A` (1B2) |
| ch2 | `AM263P_EPWM15_B_BP` (2A) → **J1.3 = GPIO74** | `AM263P_UART5_RXD` (2B1) | `AM263P_EPWM9_B` (2B2) |

- 제어핀: **pin 1 = `S`(SEL) ← `UART/EPWM_MUX_SEL`**, **pin 15 = `OE#`(EN, active-low) ← `UART/EPWM_MUX_EN`**.
- ch3/ch4는 OSPI_ECS·EPWM11/12 등 다른 BP 공유핀 (이 페이지 범위 밖).
- J1.4/J1.3는 **post-mux** — 8kw SysConfig가 EPWM15_A/B를 탭(UG `ug_lp-am263p.md:1525-1526`). U54가 경로 위에 있다.

### 2. SEL/EN 극성 (SCDS135E Table 6-1 확정)

SN74CB3Q3257 데이터시트 SCDS135E, Table 6-1 Function Table:

| /OE | S | 연결 |
|-----|---|------|
| L | **L** | A ↔ **B1** (UART5_TXD/RXD) |
| L | H | A ↔ B2 (EPWM9_A/B) |
| H | × | Z (disconnect) |

**=> UART5 헤더 연결 조건: SEL(P00)=LOW + OE#(P14)=LOW (둘 다 LOW).**

### 3. TCA6416 IO expander (U63), I2C1 @ 0x20

`PROC171_IO_EXPANDER.SchDoc` (Sheet 23). TCA6416ARTWR, **AM263P_I2C1**(SCL/SDA), **I2C 주소 0x20** (ADDR→IO_ADDR).

| expander 포트 | 신호 | 핀(U63) |
|---------------|------|---------|
| **P00** | `UART/EPWM_MUX_SEL` → U54 pin 1 | pin 1 |
| **P14** | `UART/EPWM_MUX_EN` → U54 pin 15 | pin 14 |

- 같은 expander가 MMC_MUX, BP_MUX_SEL, PRU_MUX_SEL, LED_EN, 각종 RST_EN 등 보드 전체 먹스/인에이블을 일괄 구동.
- **`UART/EPWM_MUX_SEL`·`_EN` 네트에 풀저항 없음** — 기본 상태를 정하는 외부 풀이 없다.

#### ⚠️ TCA6416 리셋 디폴트 함정

TCA6416 리셋 시: **방향 레지스터 = 입력(high-impedance), 출력 레지스터 디폴트 = HIGH(1).**

핀을 방향만 출력(0)으로 바꾸면 P00=HIGH=SEL→EPWM9, P14=HIGH=OE#=HIGH=disconnect → **UART5 차단.**

**필수 세팅 순서 (글리치 방지):**
1. 출력 레지스터에 **먼저 LOW(0) 기록** (P00=0, P14=0)
2. 방향 레지스터를 출력(0)으로 변경

순서가 바뀌면(방향 먼저 출력으로 → 출력값 HIGH로 핀이 잠깐 HIGH) 먹스가 일시 disconnect 상태를 거친다.

#### I2C1 핀 (확정, 2026-06-10)

AM263P I2C1 버스: **SCL = I2C1_SCL(D7)**, **SDA = I2C1_SDA(C8)**. 8kw SysConfig `$hardware=I2C1 BUS`가 동일 핀으로 해소됨. gpio 예제의 boosterpack2.49/2.50과 같은 I2C1 버스. **U63 @0x20 도달 실보드 PASS 확인.**

---

## 8kw-ev-wpt-tx 적용 결과 (확정, 2026-06-10)

> **이 먹스가 UART5 미동작 근본원인이었음을 실보드 인과 확증.** 진단 상세는 [[am263p_iomux_force_io_enable]] §2층 모델 참조.

### 실보드 검증 (2026-06-10, PASS)

- **조건**: J1.4↔J1.3 직결 루프백(TX=GPIO73, RX=GPIO74) + TCA6416 P00/P14=LOW 세팅
- **결과**: 세팅 **전** — 1초 버스트 무토글. 세팅 **후** — Logic2 버스트 토글, TX==RX 수신 확인.
- **인과 확증**: 세팅 전→후 차이가 U54 먹스 세팅 단독 변수이므로 인과 확정.

### Phase 2 잔여 — 8kw 보드 결합 RS-485 차동

J1.4/J1.3(LP 헤더) → THVD1400 U13(8kw 보드 부품) → RS-485 차동 라인.

- THVD1400 U13 DE = **`EN_485`** = **GPIO91** = **LP-AM263P J5.48** (UG Table 2-30 Mode6/7).
- 8kw SysConfig GPIO 인스턴스 `EN_485`로 추가, `GPIO91` hard assign 필요.
- LP-AM263P 온보드 부품이 아님 — 8kw 커스텀 보드 측 부품.

---

## 확인 필요 (잔여)

- **P15 PADCONFIG(`0x53100124`) 런타임 값**: JTAG read로 기대값 `0x541`과 일치 여부. ([[am263p_iomux_force_io_enable]] §미검증 참조.)

---

## 관련 페이지

- [[schematic_lp_am263p]] — 이 사실의 소스(회로도 ingest 인덱스).
- [[am263p_iomux_force_io_enable]] — SoC 핀먹스/PADCONFIG 층위(① 게이트). **이 먹스는 그 아래(보드) 층위(② 게이트)** — 둘 다 통과해야 UART5가 헤더에 산다. 이번 건이 그 교과서 사례.
- [[lp_am263p_ug]] — BP 헤더 핀맵(§2.20/2.21)·IO Expander(§2.1.4) 교차확인.
- 8kw [[status]] — UART5 Phase 2(RS-485 차동) 잔여.
