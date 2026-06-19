---
tags: [concept, protocol, spi, esb, rx_to_tx, ack_payload]
source: teams/c/oled_tv_software/raw/260513-oled_tv-protocol-manual__from-eta_rx-to_etx_tx.CSV
date: 2026-05-29
subsystem: 01_RX_control, 02_RX_esb, 03_TX_esb
---

# RX → TX 패킷 (HDR 0x50/0x51/0x52)

[[rx_control]] (Master)이 무선모듈에 SPI로 송신, 무선구간을 통해 Tx 보드에 도달하는 패킷군. **ESB 환경에서는 PRX(=RX_nRF)가 ACK payload 슬롯에 적재 → PTX(=TX_nRF)의 다음 송신에 piggyback되어 회수**. 0x51의 `Buffer[6..7]`은 Tx Buck Vout Ref 지령이므로 ACK payload로 회수되는 게 자연스러움. 패킷 골격은 [[esb_packet_format]] 참조.

## 0x50 — Rx 시스템 상태 비트맵

▶ Rx Module의 시스템 상태 / 운용 정보.

| Data              | 의미 (비트별, 0/1)                                           |
| ----------------- | ------------------------------------------------------- |
| `Buffer[0]` Bit.0 | `Rx_Sys_Init_St` — Rx 시스템 초기화 미완료 / 완료                  |
| `Buffer[0]` Bit.1 | `Rx_Sys_Rdy_St` — 출력 준비 안됨 / 준비됨                        |
| `Buffer[0]` Bit.2 | `Rx_Warning_St` — 정상 / Warning 전환                       |
| `Buffer[0]` Bit.3 | `Rx_Fault_St` — 정상 / Fault 전환                           |
| `Buffer[1]` Bit.0 | `RxVrect_Steady_St` — Vrect 불안정 / 안정 (정상 55~200 VDC)    |
| `Buffer[1]` Bit.1 | `RxVrect_LowerLmt` — Vrect 정상 / 하한치 이하                  |
| `Buffer[1]` Bit.2 | `RxVrect_UpperLmt` — Vrect 정상 / 상한치 초과                  |
| `Buffer[1]` Bit.3 | `RxIrect_OC` — Irect 정상 / 과전류 초과                        |
| `Buffer[2]` Bit.0 | `RxBuckRunStop_St` — Rx Buck 출력 Off / On                |
| `Buffer[2]` Bit.1 | `RxNo_Load_St` — 부하 있음(기본) / 무부하 (0.3 A 이하, 출력 On 시 진단) |
| `Buffer[2]` Bit.2 | `RxVout_SetPoint_St` — 설정 도달 안함 / 도달                    |
| `Buffer[2]` Bit.3 | `RxCtrl_Lmt_St` — 정상 / PWM 제어가 Limit에 의해 출력 제한          |
| `Buffer[2]` Bit.4 | `RxIout_Upper_Lmt` — 출력 전류 정상 / 상한 도달                   |
| `Buffer[6]`       | F/W Version (예: 0x0100 → Ver1.00)                       |
| 그 외               | Spare                                                   |

> 원문 0x50 표에서 `Buffer[2]`의 일부 비트가 `Bit.3` 라벨로 중복 표기되어 있음. 본 페이지는 `Start Bit` 값(32부터 1씩 증가)을 기준으로 재정렬.

## 0x51 — Rx 입력측 Analog + Tx Vout Ref

▶ Rx Module 정류단 전압·전류·임피던스 + Tx Buck 출력 전압 Ref.

| Data | 항목 | Type | Scale |
|---|---|---|---|
| `Buffer[0..1]` | Rx Vrect 센싱 (정류단 전압) | Uint16 | 0.01 V (210.95 V → 21,095) |
| `Buffer[2..3]` | Rx Irect 센싱 (정류단 전류) | Uint16 | 0.01 A (13.95 A → 1,395) |
| `Buffer[4..5]` | Rx 입력 임피던스 Zin | Uint16 | 0.01 Ω (50.15 → 5,015) |
| `Buffer[6..7]` | **Tx Buck 출력 전압 Ref.** (Rx → Tx 지령) | Uint16 | 0.01 V (179.95 V → 17,995) |

> `Buffer[6..7]`은 단순 센싱 데이터가 아니라 **Rx가 Tx에게 보내는 Buck 출력 전압 명령**. 무선 링크의 제어 채널 역할.

## 0x52 — Rx 출력측 Analog + 온도

▶ Rx Module 출력 + Power Stack 온도 (2개소).

| Data | 항목 | Type | Scale |
|---|---|---|---|
| `Buffer[0..1]` | Rx Vout 센싱 | Uint16 | 0.01 V (47.95 V → 4,795) |
| `Buffer[2..3]` | Rx Iout 센싱 | Uint16 | 0.01 A (14.53 A → 1,453) |
| `Buffer[4..5]` | Rx Power Stack#1 온도 | Int16 | **0.1 ℃** (120.5 ℃ → 1,205) |
| `Buffer[6..7]` | Rx Power Stack#2 온도 | Int16 | **0.01 ℃** (120.5 ℃ → 1,205) |

> Power Stack#1과 #2의 스케일 표기가 원문에서 다름 (`0.1[℃]` vs `0.01[℃]`). 예시값(120.5 → 1205)을 역산하면 양쪽 모두 0.1 ℃ 스케일이어야 일관됨 — **원문 오기 가능성**. 구현 시 확인 필요.

## 코드 실측 레이아웃 (2026-06-01 갱신)

소스: `02_RX_ble/Application/main.c:246-271`. Wire 포맷: `[ HDR(1) | LEN=0x08(1) | DATA[0..7](8) | CRC(1) ]`, Big-Endian.

### 0x50 코드 비트맵

**DATA[0]**

| 비트 | 코드 필드명 | 비고 |
|---|---|---|
| bit0 | SysInit | 매뉴얼 일치 |
| bit1 | Ready (SysRdy) | 매뉴얼 일치 |
| bit2 | Warning | 매뉴얼 정합 완료 (커밋 `c9cf6a3`, 2026-06-01) — 이전 코드 BuckSt 불일치 해소 |
| bit3 | Fault | 매뉴얼 정합 완료 — 이전 코드 Warning 위치 불일치 해소 |

**DATA[1]·DATA[2]**: Vrect/Irect/Buck 상태 비트 — 매뉴얼 기준 비트 매크로 신설 (c9cf6a3).  
**DATA[2].bit0**: BuckRunStop_St — 정합 후 위치 (이전 코드는 DATA[0].bit2 위치였음).  
**DATA[6]**: FW Major, **DATA[7]**: FW Minor (매뉴얼은 Buffer[6] 단일 바이트).

### 0x51 코드 레이아웃

| DATA 인덱스 | 필드 | Type | Scale | 상태 |
|---|---|---|---|---|
| [0..1] | Vrect | i16 | × 0.01 V | ✓ |
| [2..3] | Irect | i16 | × 0.01 A | ✓ |
| [4..5] | Zin (입력 임피던스) | i16 | × 0.01 Ω | △ 와이어 전송 추가됨 (c9cf6a3) |
| [6..7] | Tx Buck Vout Ref (→TX 지령) | i16 | × 0.01 V | △ 와이어 전송 추가됨 (c9cf6a3) |

> **잔여 차이**: 매뉴얼은 Uint16이나 코드는 i16(부호있음). Zin·Vout_Ref에서 실제 음수가 발생하는지 여부 미확인 — 환원 전 코드 재확인 권장.

> **passenger 데이터 인식**: `DATA[6..7]` Tx Buck Vout Ref는 RX 측이 TX에게 보내는 지령값으로, 이 패킷을 전송하는 `02_RX_ble` 자신의 센싱 데이터가 아님. 방향과 라벨이 어긋나는 passenger. 코드상 `rx_cmd_t`로 분리 보관 (c9cf6a3). 동일 패턴: SPI_Comm_St(02_RX_ble heartbeat), BLE_Comm_St(03_TX_ble/ESB heartbeat) — [[comm_state_monitoring]].

### 0x52 코드 레이아웃

| DATA 인덱스 | 필드 | Type | Scale |
|---|---|---|---|
| [0..1] | Vout | i16 | × 0.01 V |
| [2..3] | Iout | i16 | × 0.01 A |
| [4..5] | T1 (stack_temp1) | i16 | × 0.1 °C |
| [6..7] | T2 (stack_temp2) | i16 | × 0.1 °C |

> 기존 wiki 메모 해소: T2도 0.1 °C 스케일로 코드 확인 — 매뉴얼의 "0.01 °C" 표기는 오기.

## 출처

- [[spi_protocol_manual_260513]] — 프로토콜 매뉴얼 원본
- [[spi_debug_log_report_260529]] — 코드 실측 레이아웃 검증
