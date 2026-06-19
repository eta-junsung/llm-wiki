---
tags: [concept, uart, command, rf_link, control_channel, rx_control, tx_ble]
source: 코드 실측 (01_RX_control app_usart.c / _shared/oled_tv_protocol.c / 03_TX_ble Monitor) + 실보드 검증 2026-06-05 / 2026-06-16
date: 2026-06-16
subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
---

# buck 커맨드 — RF 링크를 건너는 유일한 UART 지령 (end-to-end 검증)

[[uart_command_set]]의 `buck <v>` 명령은 **01_RX_control의 UART 커맨드 중 RF 링크를 건너 tx-nrf(03_TX_ble)까지 도달하는 유일한 지령**이다. 나머지 UART 커맨드(`duty`/`freq`/`dt`/`phase`/`start`/`stop`/`reset`)는 전부 01 로컬 PWM 제어에 그친다.

무선 링크의 **제어 채널** 역할 — RX가 TX에게 Buck 출력 전압 기준값을 보낸다. 패킷 레벨 사양은 [[rx_to_tx_packets]] 0x51 절(`DATA[6..7]` Tx Buck Vout Ref) 참조.

## end-to-end 경로 (검증 완료, 2026-06-16)

```
GUI (pc_uart_gui.py) _send_buck()
  └ 바이너리 0x51 패킷 전송 [HDR=0x51|LEN=0x08|DATA[0..5]=0x00|DATA[6..7]=ref×100 u16 BE|XOR CRC]
      └ UART5 → 01_RX_control HAL_UART_RxCpltCallback
          └ 0x51 분기: 11B 수집·CRC 검증 → pkt_apply_rx_cmd()
              └ 전역 rx_cmd.tx_buck_vout_ref  ← float, 0~300V (DATA[6..7] u16 BE ÷100)
                  └ build_rx_pkt() : 0x51 DATA[6,7] 에 u16 = volts × 100  (Big-Endian)
                      └─ SPI → 02_RX_ble → ESB ACK payload → 03_TX_ble ──┐
                  ┌──────────────────────────────────────────────────────┘
                  └ apply_rx_pkt() (_shared/oled_tv_protocol.c)
                      └ 03_TX_ble Monitor : "tx_buck_vout_ref=<raw>"  ← raw = volts × 100
```

- 직렬화/역직렬화 단일 소스: `_shared/oled_tv_protocol.c`의 `build_rx_*` / `apply_rx_*` / `pkt_apply_rx_cmd`.
- 와이어 스케일: **volts × 100** (= 0.01 V LSB, u16 BE). Monitor 출력의 `raw`도 동일 스케일.
- 클램프: `tx_buck_vout_ref`는 0 ~ 300 V 범위로 clamp 후 적재.
- **`pkt_apply_rx_cmd()`** (`_shared` 신설, 2026-06-16): `pkt_build_rx()`(0x51 인코딩)의 역연산. DATA[6..7] u16 BE ÷100 → `rx_cmd.tx_buck_vout_ref`. `pkt_apply_tx()`와 대칭 관계.

### 실측 검증

| 시점 | 입력 | Monitor 출력 (03) | 비고 |
|---|---|---|---|
| 2026-06-05 | `buck 123.34` (ASCII 텍스트) | `tx_buck_vout_ref=12334` | 구 텍스트 커맨드 경로 |
| 2026-06-16 | GUI 바이너리 0x51 패킷 | `Tx_Buck_Vout_Ref` 정상 전파 | 현재 경로, 실보드 검증 완료 |

123.34 V × 100 = 12334 — 와이어 스케일 동일. **입력 채널만 바뀌고 0x51 DATA[6..7] 이후 경로는 불변.**

## 코드 연혁

| 커밋 / 시점 | 변경 |
|---|---|
| `eca4d96` | buck 지령 기능 추가 (UART ASCII "buck <v>" → 0x51 DATA[6,7] 적재) |
| `175a8f7` | UART 키워드 단축: `eta-tx buck vout ref` → `buck` |
| `35b94d0` | **경로 불변, 확인 방법만 갱신** — host GUI([[pc_uart_gui]]) 입력칸 → `buck <v>\r` UART5 ASCII 송신. 확인은 텍스트 응답 → **01이 바이너리 내보내는 0x51 패킷 `Tx_Buck_Vout_Ref`**(volts×100)로. monitor 텍스트→바이너리 전환([[comm_state_monitoring]]) |
| **2026-06-16 (브랜치 merge)** | **입력 채널 바이너리화**: ASCII "buck <v>\r" 텍스트 커맨드 **제거** → host GUI `_send_buck()`가 11B 바이너리 0x51 패킷을 직접 UART5로 전송. 01 `HAL_UART_RxCpltCallback` 0x51 분기 추가·텍스트 buck 분기 제거. `_shared` `pkt_apply_rx_cmd()` 신설(`pkt_build_rx()`의 역). **실보드 검증**: GUI 입력 → 03_TX_ble Monitor `Tx_Buck_Vout_Ref` 정상 전파 확인. |

## 새 "tx로 보내는 지령"을 늘릴 때의 첫 패턴

이 경로가 **RF 링크 너머로 가는 지령을 추가할 때의 레퍼런스 패턴**이다:

1. **키워드 접두로 로컬과 구분** — 로컬 PWM 커맨드와 헷갈리지 않도록 RF 지령은 식별 가능한 키워드를 둔다 (`buck`).
2. 전역 `rx_cmd_t` 필드에 받는다 (passenger 데이터 — 02_RX_ble 자신의 센싱이 아니라 TX행 지령이므로 별도 보관, [[rx_to_tx_packets]] passenger 인식 절).
3. `_shared/oled_tv_protocol.c`의 `build_rx_*` / `apply_rx_*`에 와이어 매핑(스케일·바이트 위치)을 추가한다.

> ~~float 소수 입력(`buck 15.5`)이 깨지지 않으려면 01_RX_control 빌드에 `nanoscanffloat`가 켜져 있어야 한다~~ — **2026-06-16 이후 해소**: 입력이 바이너리 0x51 패킷으로 전환되며 `sscanf("%f")` 파싱이 제거됐다. [[cubeide_newlib_nano_float]] 의존성은 이 경로에서 소멸.

## 관련 페이지

- [[uart_command_set]] — `buck` 포함 UART5 명령어 전체
- [[pc_uart_gui]] — host GUI: buck 입력칸 송신 + 0x51 `Tx_Buck_Vout_Ref` 파싱 확인
- [[rx_to_tx_packets]] — 0x51 `DATA[6..7]` Tx Buck Vout Ref 와이어 사양 + passenger 인식
- [[comm_state_monitoring]] — passenger 데이터 패턴(SPI_Comm_St·BLE_Comm_St)
- [[cubeide_newlib_nano_float]] — float scanf 빌드 의존성
- [[tx_ble_module]] — 03 Monitor 출력 포맷
