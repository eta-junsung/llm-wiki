---
tags: [concept, uart, command, rf_link, control_channel, rx_control, tx_ble]
source: 코드 실측 (01_RX_control app_usart.c / _shared/oled_tv_protocol.c / 03_TX_ble Monitor) + 사용자 실보드 검증 2026-06-05
date: 2026-06-05
subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
---

# buck 커맨드 — RF 링크를 건너는 유일한 UART 지령 (end-to-end 검증)

[[uart_command_set]]의 `buck <v>` 명령은 **01_RX_control의 UART 커맨드 중 RF 링크를 건너 tx-nrf(03_TX_ble)까지 도달하는 유일한 지령**이다. 나머지 UART 커맨드(`duty`/`freq`/`dt`/`phase`/`start`/`stop`/`reset`)는 전부 01 로컬 PWM 제어에 그친다.

무선 링크의 **제어 채널** 역할 — RX가 TX에게 Buck 출력 전압 기준값을 보낸다. 패킷 레벨 사양은 [[rx_to_tx_packets]] 0x51 절(`DATA[6..7]` Tx Buck Vout Ref) 참조.

## end-to-end 경로 (검증 완료)

```
01_RX_control UART5 (115200 8N1)
  └ "buck <v>"  입력
      └ 전역 rx_cmd.tx_buck_vout_ref  ← float, 0~300V clamp
          └ build_rx_pkt() : 0x51 DATA[6,7] 에 u16 = volts × 100  (Big-Endian)
              └─ SPI → 02_RX_ble → ESB ACK payload → 03_TX_ble ──┐
          ┌──────────────────────────────────────────────────────┘
          └ apply_rx_pkt() (_shared/oled_tv_protocol.c)
              └ 03_TX_ble Monitor : "tx_buck_vout_ref=<raw>"  ← raw = volts × 100
```

- 직렬화/역직렬화 단일 소스: `_shared/oled_tv_protocol.c`의 `build_rx_*` / `apply_rx_*`.
- 와이어 스케일: **volts × 100** (= 0.01 V LSB). Monitor 출력의 `raw`도 동일 스케일 (volts × 100).
- 클램프: `tx_buck_vout_ref`는 0 ~ 300 V 범위로 clamp 후 적재.

### 실측 검증 (사용자, 2026-06-05)

| 입력 (01) | Monitor 출력 (03) |
|---|---|
| `buck 123.34` | `tx_buck_vout_ref=12334` |

123.34 V × 100 = 12334 — 와이어 스케일·경로 정상 확인.

## 코드 연혁

| 커밋 | 변경 |
|---|---|
| `eca4d96` | buck 지령 기능 추가 (UART → 0x51 DATA[6,7] 적재) |
| `175a8f7` | UART 키워드 단축: `eta-tx buck vout ref` → `buck` |
| `35b94d0` | **경로 불변, 확인 방법만 갱신** — host PC GUI([[pc_uart_gui]]) 입력칸 → `buck <v>\r` UART5 송신. 확인은 텍스트 응답이 아니라 **01이 바이너리로 내보내는 0x51 패킷 `Tx_Buck_Vout_Ref`**(volts×100)로. monitor 텍스트→바이너리 전환([[comm_state_monitoring]]) |

> **(`35b94d0`) 확인 채널 변화**: end-to-end 경로(UART→0x51 DATA[6,7]→SPI→ESB→03)는 그대로다. 다만 01 모니터가 바이너리화되며, host에서 적재값을 확인하려면 GUI가 파싱한 0x51 `Tx_Buck_Vout_Ref` 필드(volts×100)를 본다. 03 Monitor의 `tx_buck_vout_ref=12334` 텍스트(아래 실측)는 03측 표시로 여전히 유효.

## 새 "tx로 보내는 지령"을 늘릴 때의 첫 패턴

이 경로가 **RF 링크 너머로 가는 지령을 추가할 때의 레퍼런스 패턴**이다:

1. **키워드 접두로 로컬과 구분** — 로컬 PWM 커맨드와 헷갈리지 않도록 RF 지령은 식별 가능한 키워드를 둔다 (`buck`).
2. 전역 `rx_cmd_t` 필드에 받는다 (passenger 데이터 — 02_RX_ble 자신의 센싱이 아니라 TX행 지령이므로 별도 보관, [[rx_to_tx_packets]] passenger 인식 절).
3. `_shared/oled_tv_protocol.c`의 `build_rx_*` / `apply_rx_*`에 와이어 매핑(스케일·바이트 위치)을 추가한다.

> float 소수 입력(`buck 15.5`)이 깨지지 않으려면 01_RX_control 빌드에 `nanoscanffloat`가 켜져 있어야 한다 — [[cubeide_newlib_nano_float]].

## 관련 페이지

- [[uart_command_set]] — `buck` 포함 UART5 명령어 전체
- [[pc_uart_gui]] — host GUI: buck 입력칸 송신 + 0x51 `Tx_Buck_Vout_Ref` 파싱 확인
- [[rx_to_tx_packets]] — 0x51 `DATA[6..7]` Tx Buck Vout Ref 와이어 사양 + passenger 인식
- [[comm_state_monitoring]] — passenger 데이터 패턴(SPI_Comm_St·BLE_Comm_St)
- [[cubeide_newlib_nano_float]] — float scanf 빌드 의존성
- [[tx_ble_module]] — 03 Monitor 출력 포맷
