---
tags: [briefing, oled_tv_software, team]
source: status·roadmap 기반 수작업 정리
date: 2026-06-12
---

# oled_tv_software — 팀 업무보고 참고 자료

> 주간 팀 보고 시 이 페이지를 열고 아래 흐름 순서로 설명.
> 기술 수치·상태 기호는 [[status]]·[[roadmap]]이 단일 소스 — 보고 직전 확인.

---

## 보고 스냅샷 이력 (주차별 — 다음주 diff 기준)

| 보고일 | 위치 | 그 주 핵심 | 다음 계획 |
|--------|------|-----------|-----------|
| **2026-06-12** | 별트랙 거의 완료 | **① SPI·ESB comm-state 비트 2개 실보드 검증 완료**(bit5 heartbeat / bit6 presence), **② PC UART 바이너리 모니터 + GUI 완성·실보드 검증**(6패널·Physical 변환·FW 버전 표시), **③ TX Buck Set E2E 실측 확인**(GUI `222.22V` → 03 터미널 `Tx_Buck_Vout_Ref=22222`), **④ 02 리팩토링·eta_ 전환 ✓ / 03 리팩토링 빌드 ✓ / _shared 다듬기 ✓**, **⑤ 03 SPIS 재작성 + 04_tx_control 더미 신설(4보드 E2E 준비)** | 04 CubeIDE 빌드 → 4보드 플래시 → 03↔04 SPI 링크 검증 → E2E(`buck 12.00`→04 raw 1200) |

> **다음주(예정) 보고 포인트**: ① **04 더미 D1·D2 완료**: 04 Ctrl+B 빌드 에러 0 → 4보드 플래시 → 03↔04 SPI CS 10ms Δt + CRC fail 0 검증 ② **D3 E2E**: 01 `buck 12.00` → 04 UART `Tx_Buck_Vout_Ref=1200` ③ **03 실보드 검증**: ESB PTX 동작·P0.17/18 오실로 ④ 02 `ADD_SPI` 전역 전파 점검·실보드 재확인

---

## 1. 이 작업이 뭔가

**목표**: OLED TV 무선 전력 전송 시스템의 **3-MCU 제어신호 교환 펌웨어** 완성.
전력 전송 자체가 아닌 **제어 명령이 3개 칩을 건너가는 채널** — STM32(01) ↔ nRF52(02) SPI ↔ nRF52(03) ESB 무선.
인수받은 코드를 ESB 기준으로 안정화하고 있으며, 현재 스코프(M3 10ms 폴링 + comm-state 비트)는 달성 완료.

> **한 줄 비유**: TV 전원 제어 명령이 유선(SPI) → 무선(ESB)을 거쳐 TX 보드까지 전달되는 "신경망 채널"을 만드는 작업.

---

## 2. 시스템 구성 및 작업 호

### 3-MCU 구성

```
[STM32 01_RX_control]
   UART5 ─── PC GUI (uart_gui.py)
   SPI Master ───────────────────────────┐
                                         ▼
                                [nRF52 02_RX_ble] ─── ESB 무선 ─── [nRF52 03_TX_ble]
```

### 마일스톤 호

```
[M0] 코드 인수 + 구조 파악  ✓
[M1] ESB 무선 링크 동작     △ (동작·장시간 미검증)
[M2] SPI 링크 안정화        △ (heartbeat ✓, 장시간 미검증)
[M3] SPI 10ms 폴링 주기     ✓ ← 현재 스코프 달성(2026-06-01)
        ▼
   (현재 스코프 종료 — 별트랙 진행 중)
```

### 별트랙 완료 현황 (6/12 기준)

```
[B1] comm-state 비트 2개 (SPI heartbeat / ESB presence)   ✓  실보드 검증
[B2] app_protocol 적출 (protocol_loop() 단일 진입점)       ✓  실보드 검증
[B3] PC UART 바이너리 모니터 + GUI                         ✓  실보드 검증
[B4] 02_RX_ble 모듈 분리 + eta_ 접두사 전환               ✓  실보드 검증
[B5] _shared 프로토콜 다듬기 (심볼 정리·상수화)            ✓  실보드 검증
[B6] 03_TX_ble 모듈 분리 리팩토링                          △  빌드 ✓, 실보드 미검증
[B7] 03 SPI_Loop SPIS 재작성                               △  빌드 ✓, 실보드 미검증
[B8] 04_tx_control 더미 (E2E 검증용 STM32)                 △  신설, CubeIDE 빌드 미수행
        ▼
   [D1] 04 빌드·플래시   ✗ ← 다음
   [D2] 03↔04 SPI 링크 검증
   [D3] E2E: buck 12.00 → 04 raw 1200
```

---

## 3. 이번주 진행 & 만난 문제 (6/5 ~ 6/11)

### 3-1. 진행

1. **comm-state 완성 (6/8)**: 링크 health 비트 2개 — SPI_Comm_St(bit5, 200ms heartbeat) + BLE/ESB_Comm_St(bit6, 200ms 윈도우 내 ESB presence) 모두 실보드 검증 완료. 판정값이 STM32까지 정확히 전달됨.
2. **PC UART GUI 완성 (6/10) + E2E 실측 (6/12)**: 01 UART5 출력을 텍스트에서 **11B 바이너리 패킷**으로 전환. GUI는 6패널(TX/RX Status·Input·Output), Physical 변환 적용(전압·전류 ×0.01, 온도 ×0.1), FW 버전 표시. 실보드 검증: 10.067Hz, 301프레임, 에러 0. **TX Buck Set E2E 실측 확인**: GUI `222.22V` → 0x51 `Tx_Buck_Vout_Ref=22222` → 03_TX_ble SEGGER 터미널 직접 확인. 스크린샷: `raw/pc_uart_gui/eta-c-oled-monitor.png`, `raw/pc_uart_gui/eta-c-oled-tx-buck-set.png`.
3. **코드 정리 3종 (6/9~6/11)**:
   - `app_protocol` 적출: SPI 프로토콜을 `common.c`에서 독립 모듈로 추출. STM32 실보드 검증.
   - 02_RX_ble 리팩토링: 618줄 단일 파일 → 6개 모듈 분리, `eta_` 접두사 전환, 실보드 검증.
   - `_shared` 다듬기: 죽은 심볼 제거, 매직넘버 상수화(`PKT_KIND_COUNT` 등). 3펌웨어 실보드 검증.
4. **E2E 검증 준비 (6/11)**: 03 SPI_Loop을 SPIM→SPIS로 재작성, 04_tx_control STM32 더미 신설. 다음 세션에서 4보드를 연결해 E2E 검증.

### 3-2. 만난 문제 & 해결

| 문제 | 원인 | 해결 |
|------|------|------|
| ESB comm-st 비트가 불안정하게 플래핑(49→0/30s) | 공유 RX 버퍼(`esb_pkt[0]`)를 ESB ISR이 memcpy로 덮어쓰면서 **race condition** 발생 | 송신 복사본(`spi_tx_pkt`)에 SPI_Loop 직전 stamp — 공유 버퍼를 읽지 않아 race-free |
| nRF52 모듈 파일명이 SDK와 충돌 | `app_` 접두사가 nRF5 SDK 예약 네임스페이스(`app_uart.h` 등 다수) | 로컬 모듈 전체를 `eta_` 접두사로 전환(헤더·소스 대칭 회복) |
| 03 SPI_Loop 코드 방향 오판 | 기존 코드가 SPIM(마스터)이었으나 02 슬레이브 거울 구조(SPIS 필요) | 기존 SPIM 코드 전면 폐기 → 02 참고해 SPIS(`nrf_drv_spis`, MODE_2)로 재작성 |

---

## 4. 지금 어디 / 막힌 곳

### 4-1. 완료 (별트랙 기준)

- **SPI·ESB 링크 health 모니터링**: 3-MCU 전체 comm-state 비트 2개 실보드 검증 완료.
- **PC UART GUI**: 텍스트 → 바이너리 전환 + host 도구 완성·검증.
- **코드 구조 정리**: 01 app_protocol·02 리팩토링·_shared 다듬기 모두 실보드 검증.

### 4-2. 검증 대기 (빌드 완료, 실보드 미검증)

1. **03_TX_ble 리팩토링·SPIS 재작성** (`1d7f71a`·`e706b53`): TX 보드 + 오실로스코프 연결 필요.
2. **04_tx_control 더미** (`07fbf1f`): CubeIDE Ctrl+B 빌드 미수행 상태.

### 4-3. 다음 세션 의존 항목 (검증 대기 해소 후)

- 03↔04 SPI 링크 연결 검증 (CS 10ms Δt, CRC fail 0)
- E2E: 01 `buck 12.00` → 04 UART `Tx_Buck_Vout_Ref=1200`

---

## 5. 다음 작업 — 어떻게 진행할 예정인가

```
[D1] 04 CubeIDE Ctrl+B 빌드 에러 0 확인
[D2] 4보드 플래시(01/02/03/04) → 03↔04 SPI CS 10ms·CRC fail 0 검증
[D3] E2E: 01 buck 12.00 → 04 UART Tx_Buck_Vout_Ref=1200 (raw)
 + 03 실보드 검증(ESB PTX·P0.17/18 오실로)
 + 02 ADD_SPI 전역 전파 점검
```

> 이 단계들이 완료되면 **별트랙 전체 종료**. 이후 M4(SPI 9MHz 상향) 또는 M5(E2E 지연 측정) 재개 여부를 판단.

---

> 상세 기술 맥락: [[status]] (현재 위치·다음 시작점) · [[roadmap]] (M호·별트랙 전체) · [[comm_state_monitoring]] (링크 health 비트) · [[app_protocol_module]] (protocol_loop) · [[pc_uart_gui]] (host GUI) · [[nrf52_firmware_conventions]] · [[nrf52_module_naming]]
