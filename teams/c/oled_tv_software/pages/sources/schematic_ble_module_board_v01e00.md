---
tags: [source, schematic, board, ble_module]
source: teams/c/oled_tv_software/raw/BLE_Module_Board_Ver0.1E00_260318.pdf
date: 2026-06-05
subsystem: 02_RX_ble, 03_TX_ble
---

# BLE Module Board Ver0.1E00 회로도 (260318)

[[rx_ble_module]](nRF52832)의 실물 보드 설계 도면. **02_RX_ble / 03_TX_ble 공용 커스텀 모듈** — 같은 보드에 둘 중 한 펌웨어를 탑재(예: 2026-06-04 `03_TX_ble` 플래싱). 2026-06-01 실물 보드 입고.

## 원본

- **raw 사본**: `raw/BLE_Module_Board_Ver0.1E00_260318.pdf` (2026-06-05 확보, 4시트)
- **원본 파일**: `C:\Users\echog\eta\projects\c\oled_tv_software\docs\Schematic\BLE_Module_Board_Ver0.1E00_260318 1.pdf`
- **버전**: Ver0.1E00, 2026-03-18
- **설계자**: Hyun-Min,Lee / 승인: T.D.YEO
- **모델**: OLED700 WPT
- **총 4시트** (표지, 회로도, 부품배치도, 설계참조)
- **보드 크기**: 35mm × 35mm 이하

## 상태

- 실물 보드 입고: ✓ 2026-06-01
- 회로도 상세 ingest: ✓ 완료 (2026-06-02)
- 실제 PDF 재독·교정: ✓ 2026-06-05 — 커넥터 핀번호 확정(사용자 확인), 전원 아키텍처 교정(PD3V3→필터→BLE_P3V3), System Reset·안테나 절 추가, raw 사본 확보

---

## MCU 모듈

**U1: UTO-NBL-52** (nRF52832 기반 모듈, 39핀 + A1)

| 핀 | 신호 | 비고 |
|---|---|---|
| 1 | SWDCLK | SWD 전용 |
| 2 | SWDIO | SWD 전용 |
| 3 | P0.21/RESET | nRST |
| 9 | VCC | 3.3V |
| 23 | P0.27 | SPI_CLK_uC |
| 25 | P0.25 | SPI_MOSI_uC |
| 26 | P0.26 | SPI_MISO_uC |
| 27 | P0.22 | SPI_nCS_uC |
| 29, 31, 39 | GND | — |
| 30 | ANT | ANT_uC (패턴 안테나) |
| 34 | P0.17 | (펌웨어: PIN_DBG_HB) |

ADC 가용 핀: P0.02/AIN0, P0.03/AIN1, P0.04/AIN2, P0.05/AIN3, P0.28/AIN4, P0.29/AIN5, P0.30/AIN6, P0.31/AIN7

---

## 커넥터 전체 목록

> **주의**: 프로토콜 매뉴얼(source: [[spi_protocol_manual_260513]])은 CN3(SPI), CN4(전원)로 표기하나,
> **회로도·실물 실크에는 CN2(SPI), CN1(전원)** 으로 되어 있어 번호가 다르다.

### CON1 — SWD 프로그래밍/디버그 ★

| 항목 | 내용 |
|---|---|
| 커넥터 | SMAW250-05 (2.5mm pitch, 5핀) |
| 대체품 | MOLEX 22-05-7055 (KK 2.5mm 5핀) |
| 용도 | SWD 프로그래밍·디버그 (`(연결@SWD)`) |

신호 (5핀, 회로도 핀번호 — 사용자 확인 2026-06-05):

| 핀 | 신호 | nRF52832 |
|---|---|---|
| 1 | SWDCLK_uC | SWDCLK (전용 핀) |
| 2 | SWDIO_uC | SWDIO (전용 핀) |
| 3 | SWD_nRST | P0.21/RESET (D1 보호 다이오드 경유, System Reset 회로 공유) |
| 4 | BLE_GND | GND |
| 5 | BLE_P3V3 | VCC (3.3V) |

- D1 (SMD220PL-TP/SOD-123FL): nRST 라인 보호 다이오드
- SW1 (ITS-1107/SMD): 시스템 리셋 버튼 (BLE_GND로 풀다운)

**ST-LINK V2 연결 방법**: SWDIO → ST-LINK 핀7, SWDCLK → ST-LINK 핀9, GND → ST-LINK 핀8, nRST → ST-LINK 핀15(선택). VCC는 보드 자체 전원 사용 시 연결 불요. [[플래싱 가이드|st_link_nrf52_flash]] 참고.

---

### CN2 — SPI 통신 (Board-to-Board @Rx Control Board)

| 항목 | 내용 |
|---|---|
| 커넥터 | HEADER_1.27mm/10P (10핀, Straight Type) |
| 용도 | STM32(Rx Control Board) ↔ nRF52832 SPI 통신 |
| 프로토콜 매뉴얼 표기 | CN3 |

| 핀 | 신호 | nRF52 GPIO |
|---|---|---|
| 1, 2 | PD3V3 (+3.3 VDC, 비절연) | — |
| 3 | SPI_nCS_uC | P0.22 |
| 4 | (NC) | — |
| 5 | SPI_MISO_uC | P0.26 |
| 6 | (NC) | — |
| 7 | SPI_MOSI_uC | P0.25 |
| 8 | SPI_CLK_uC | P0.27 |
| 9, 10 | DGND | — |

핀번호 사용자 확인 2026-06-05 (회로도 기준, [[rx_ble_module]] CN2와 정합). 핀4·6 미사용(NC). PD3V3는 전원분리 필터(B1+FLT1)를 거쳐 nRF VCC(BLE_P3V3)가 된다 — 아래 [전원 아키텍처](#전원-아키텍처).

---

### CN1 — 전원 (Rx OLED Regulator Power B/D)

| 항목 | 내용 |
|---|---|
| 커넥터 | HEADER_1.27mm/6P (6핀, Straight Type) |
| 용도 | 절연 5V 공급 (`COMM_P5V` / `COMM_GND`) |
| 프로토콜 매뉴얼 표기 | CN4 |

| 핀 | 신호 |
|---|---|
| 1, 2, 3 | COMM_P5V (절연 5V) |
| 4, 5, 6 | COMM_GND (절연) |

핀번호 사용자 확인 2026-06-05 ([[rx_ble_module]] CN1과 정합). ⚠ **교정(2026-06-05)**: COMM_P5V(절연 5V)는 ISO6721 UART 절연기의 PC측(field-2) 전원 + CON2 출력으로만 쓰인다 — **nRF 전원이 아니다.** nRF 전원(BLE_P3V3)은 CN2의 PD3V3(비절연 3.3V)에서 파생한다. (이전 판의 "COMM_P5V → B1+FLT1 → BLE_P3V3 생성"은 두 전원 도메인을 뒤섞은 오기 — 아래 [전원 아키텍처](#전원-아키텍처).)

---

### CON2 — UART 모니터링 (절연형, PC 연결)

| 항목 | 내용 |
|---|---|
| 커넥터 | SMAW250-04 (2.5mm pitch, 4핀) |
| 대체품 | MOLEX 22-05-7045 (KK 2.5mm 4핀) |
| 용도 | UART 모니터링 (`(연결@PC Monitoring)`) |

| 핀 | 신호 | 방향 | nRF52 GPIO | 비고 |
|---|---|---|---|---|
| 1 | COMM_P5V | — | — | 절연 5V (CN1에서 공급) |
| 2 | TXD_uC | uC → PC | **P0.15** | ISO6721RBDR 절연 경유 |
| 3 | RXD_uC | PC → uC | **P0.14** | ISO6721RBDR 절연 경유 |
| 4 | COMM_GND | — | — | 절연 GND |

> 물리 핀번호(1~4) 사용자 확인 2026-06-05. UART GPIO 핀 P0.15(TX)/P0.14(RX)는 사용자 확인 2026-06-04, 펌웨어 `custom_board.h`의 `TX_PIN_NUMBER=15 / RX_PIN_NUMBER=14`에 반영. (PCA10040 기본값 TX=6/RX=8과 다름.)

ISOL1 (ISO6721RBDR/SOIC-8): 2채널 디지털 아이솔레이터. D2 (SZNUP2105LT1G/SOT23-3): ESD 보호.

---

## LED 인디케이터

| 부품 | 색상 | 기능 | 신호 | nRF52 GPIO |
|---|---|---|---|---|
| LED1 | Green | System Ready (점등) | LED1_uC | **P0.09** |
| LED2 | Yellow | SPI Comm Status (점멸) | LED2_uC | **P0.08** |
| LED3 | Green | BLE Comm Status (점멸) | LED3_uC | **P0.06** |

구동 방식: PDTC143ZT/SOT-23 (pre-biased NPN) 트랜지스터 — GPIO HIGH → LED 점등(**active-high**, 1=ON).

핀 번호·극성 `03_TX_ble` 실보드 실측 확정 (2026-06-04): LED1(P0.09) 상시 점등, LED2(P0.08)/LED3(P0.06) 200 ms 토글. 펌웨어 핀 정의 단일 소스는 `_shared/oled_tv_protocol.h` `PIN_LED1/2/3 = 9/8/6`. 검증 행 → [[gpio_verification_pinmap]].

> ⚠ **펌웨어 board define 함정**: 펌웨어는 historically `BOARD_PCA10040`로 빌드됐으나 이 보드는 PCA10040 DK가 아니라 UTO-NBL-52 기반 커스텀 보드다. PCA10040 기준이면 P0.06=UART TX·P0.08=UART RX·P0.17~20=온보드 LED라 위 LED 핀과 충돌한다. 2026-06-04 `BOARD_CUSTOM` + `_shared/custom_board.h`로 전환해 회사 보드 UART(P0.15/P0.14)·LED를 분리. 상세 → [[tx_ble_module]].

---

## 전원 아키텍처

**절연 경계 = ISO6721 UART 절연기.** 두 전원 도메인이 분리돼 있다 (회로도 sheet2 `전원분리` 블록 실측, 2026-06-05 교정).

```
[비절연 도메인 — nRF 전원]
CN2 PD3V3 (3.3V, Rx Control B/D 공급)
  └─ B1 (SHH-1M2012-221 페라이트 비드, 2.2A)
       └─ FLT1 (NFM41PC155B1H3L 3단자 피드스루 EMI 필터)
            └─ BLE_P3V3  →  nRF52832 VCC (U1 pin9)        ← 강압 없음, 둘 다 3.3V
                 └─ nRF 내장 DC/DC: L2/L3 (MLZ1608M100/150WT000) → 내부 1.3V 레일
CN2 DGND ──(R5 0Ω, One Point)── BLE_GND

[절연 도메인 — PC 모니터링측]
CN1 COMM_P5V (5V 절연, Rx OLED Regulator Power B/D)
  └─ ISO6721 field-2(PC측) 전원  +  CON2 → PC
CN1 COMM_GND (절연 GND)
```

요점:
- **nRF 전원은 PD3V3(비절연 3.3V)에서 파생** — B1+FLT1은 강압이 아닌 **EMI 필터**(전원분리). ⚠ PD3V3가 사실상 nRF VCC 직결이라 5V 인가 금지.
- **COMM_P5V(절연 5V)는 nRF로 안 간다** — UART 절연기 PC측 + CON2 전용.
- **One Point 접지**: R5 0Ω이 DGND(비절연) ↔ BLE_GND(nRF)를 단일점 접속.
- "1.3V LDO"는 외부 LDO가 아니라 nRF52832 **내장 DC/DC**용 인덕터(L2/L3).

---

## System Reset 회로

`SWD_nRST` 리셋 라인 (sheet2 우하단):

- **SW1** (ITS-1107/SMD): 푸시 리셋 버튼 — 누르면 라인을 BLE_GND로 끌어내림.
- **R12**: 풀업 (BLE_P3V3 → SWD_nRST).
- **R13**: 직렬 저항 → `SWD_nRST_uC` (U1 P0.21/RESET).
- **C12**: 디바운스 캡.

CON1 핀3(SWD_nRST)과 같은 라인 — 디버거 nRST와 버튼이 nRST 라인을 공유한다.

---

## 안테나 회로

U1 `ANT_uC`(pin30) → **L1**(3.9nH, π-매칭 직렬 인덕터) → **PCB 패턴 안테나**. C8/C9는 **DNP**(미실장) — π-매칭 션트 자리만 확보. 외장 안테나 커넥터 없음(패턴 온보드).

---

## 관련

- [[rx_ble_module]] — 모듈 entity (핀맵, 펌웨어 현황)
- [[tx_ble_module]] — 03_TX_ble (같은 보드 공용 — LED·UART 핀맵)
- [[spi_packet_format]] — SPI wire 포맷
- [[st_link_nrf52_flash]] — 플래싱 정본 (CON1 SWD 사용)
- [[spi_protocol_manual_260513]] — 커넥터 CN3/CN4 명칭 출처 (회로도와 번호 상이)
