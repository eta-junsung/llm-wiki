---
tags: [roadmap, oled_tv_software, 04_tx_control, living-doc]
date: 2026-06-11
---

# 04_tx_control 더미 프로젝트 — 작업 로드맵

> 03_TX_ble SPI 출력 단까지 직접 검증하기 위한 STM32 더미 수신 프로젝트.
> 04_tx_control 실물은 타팀 개발 — 이 프로젝트는 "03 SPI_Loop 동작 + Vout Ref 전달 경로" 확인이 목적이다.

---

## 0. 한 줄 요약

01_RX_control 골격을 복사해 STM32 SPI Master 더미(04_tx_control)를 만들고, 03_TX_ble SPI_Loop를 SPIS로 재작성해, **01이 보낸 TX Buck Vout Ref raw 값이 04 UART 모니터까지 도달하는지** 검증한다.

---

## 1. 데이터 흐름

```
01_RX_control (STM32, SPI Master)
  └─ SPI(10ms) ──→ 02_RX_ble (nRF52, SPI Slave, ESB PRX)
                      └─ ESB ACK ──→ 03_TX_ble (nRF52, ESB PTX, SPI Slave ※SPIS 재작성 △e706b53)
                                          └─ SPI(10ms) ──→ 04_tx_control ★신규 △07fbf1f
```

**검증 핀포인트**: 01의 `rx_cmd.tx_buck_vout_ref` → `0x51` DATA[6..7] → 02 → ESB ACK → 03 `g_last_ack_by_hdr[1]` → SPI MISO → 04 UART 모니터 **raw 1200** 표시 (`buck 12.00` 기준).

---

## 2. 마일스톤 호

| 단계 | 내용 | 완료 기준 | 상태 |
|------|------|-----------|------|
| **D0** | 03_TX_ble SPI_Loop ~~활성화~~ → **SPIS 전면 재작성** | emBuild 에러 0 | △ `e706b53` — ⚠️ 기존 코드 SPIM이었음(§4 정정 1). 02 거울 SPIS 재작성. 실보드 미검증 |
| **D1** | 04_tx_control 더미 프로젝트 생성 | CubeIDE Ctrl+B 에러 0 | △ `07fbf1f` — 01 복제·ADC/PWM/CAN/DAC 제거. **.ioc 파일명 `RX_control.ioc` 잔류·CubeIDE 빌드 미수행** |
| **D2** | 03 ↔ 04 SPI 링크 동작 | CS 10ms Δt 오실로 확인, CRC fail 0 | ✗ |
| **D3** | 01→02→ESB→03→04 End-to-end | `buck 12.00` → 04 모니터 raw 1200 표시 | ✗ |

---

## 3. 현재 위치 → [[status]]

---

## 4. 구현 결과 — 전제 정정 (커밋 e706b53·07fbf1f, 2026-06-11)

원 핸드오프 프롬프트(§5)의 전제 중 코드와 어긋났던 자리를 기록한다. 이후 같은 영역 작업 시 아래 정정 내용을 기준으로 삼는다.

### 정정 1 — 03 SPI_Loop: 주석 해제가 아니라 전면 재작성

원 전제: "SPI_Loop 주석을 풀고 활성화". **실제**: 기존 코드가 **`nrf_drv_spi` (SPIM, Master)** 로 `rx_module`(54B 구조체)을 통짜 전송하는 죽은 경로였음 — 11B wire 프로토콜·STM32=Master 스펙 모두 불일치. 단순 활성화 불가, 전면 재작성.

해결: 02_RX_ble의 SPIS(`nrf_drv_spis`) 구현을 거울 복제해 재작성.

### 정정 2 — ADD_SPI는 이미 emProject에 정의돼 있었음

원 전제: "없으면 추가". **실제**: `TX_BLE.emProject` `c_preprocessor_definitions`에 이미 존재. 추가 불요.

### 정정 3 — `pkt_apply_rx` 헬퍼 없음

원 전제: "`exchange_packets()`에서 `pkt_apply_rx`로 역직렬화". **실제**: `_shared`에는 `pkt_apply_tx`만 있음(`pkt_apply_rx`는 `9ad338d`에서 참조 0건으로 삭제됨). 04는 수신 패킷을 역직렬화 없이 `pkt_print_data_line(hdr, data)`로 `data[]` 그대로 출력.

### 정정 4 — 03 데이터 소스: `g_rx_data` → `g_last_ack_by_hdr[3]`

원 전제: "SPI_Loop가 `g_rx_data`(ESB ACK로 받은 RX 패킷들)를 round-robin 직렬화". **실제**: 03에는 `g_rx_data` 없음. ESB ACK demux된 RX 패킷은 **`g_last_ack_by_hdr[3]`**(0x50/0x51/0x52 각 11B)에 존재. SPI_Loop는 이를 round-robin으로 MISO에 서빙.

### 정정 5 — 04 모니터 수치: "12.00V" → raw 1200

원 전제: "`Vout_Ref=12.00V` 표시". **실제**: `pkt_print_data_line`이 ÷100 변환을 하지 않으므로 raw 정수 표시 — `buck 12.00` → 04 모니터 `Tx_Buck_Vout_Ref=1200`. **검증 기준 = raw 1200**.

### 확정된 설계 결정

- **03 SPI 역할**: SPIS(Slave), SPIS1, NRF_SPIS_MODE_2, 핀 = `PIN_SPI_*` 공유 헤더(02와 동일: P0.22/25/26/27). SPI_Loop = `g_last_ack_by_hdr[3]` round-robin MISO 서빙 + 04 TX 패킷 수신·카운트.
- **03의 ESB→04 전달**: ESB ACK에서 받은 0x50/0x51/0x52만. 04 TX 수신은 카운트만 — ESB forward 없음. ESB TX는 `inject_tx_dummy_data` 유지.
- **04 제거된 페리**: ADC/CAN/DAC/PWM 관련 TIM + `app_{adc,can,dac,pwm,tim}` 전부. SPI2+UART5만 잔존.
- **04 .ioc 파일명**: `RX_control.ioc` → `TX_control.ioc` 개명 미수행. D2 이전 정리 후보.
- **브랜치**: `04-tx-control-dummy` (e706b53 03 SPIS 재작성 / 07fbf1f 04 더미). `refactoring-shared`는 `esb`로 FF 머지 후 삭제됨.

---

## 5. 원 핸드오프 프롬프트 (작성 시점 전제 — §4에서 정정됨)

> ⚠️ **§4의 정정 내용을 적용해서 읽을 것**. 특히 "SPI_Loop 주석 해제", "g_rx_data", "pkt_apply_rx", "Vout_Ref=12.00V" 부분은 §4 정정 1·3·4·5로 대체됨.

---

### [작업] oled_tv_software — 04_tx_control 더미 구현 + 03 SPI_Loop 활성화

**목표**: `03_TX_ble`의 SPI 출력 단을 STM32 수신 더미(`04_tx_control`)로 마감해, 01→02→ESB→03→04 전 경로에서 **TX Buck Vout Ref 데이터 전달을 실보드 검증**한다.

이 프로젝트(`04_tx_control`)는 타팀이 실제로 만들 TX 보드 펌웨어가 아니다. **SPI 링크와 데이터 경로 검증만을 위한 최소 더미**다. ADC, PWM, 실제 제어 로직 없음.

---

#### 시스템 현황

펌웨어 레포: `~/eta/oled_tv_software` (별도 repo, wiki는 `~/eta/wiki`)

| 서브프로젝트 | MCU | 역할 | 상태 |
|---|---|---|---|
| 01_RX_control | STM32F103RCT6 | SPI Master, ADC/PWM | ✓ 실보드 검증 |
| 02_RX_ble | nRF52832 | ESB PRX, SPI Slave | ✓ 실보드 검증 (b92835c) |
| 03_TX_ble | nRF52832 | ESB PTX, SPI Slave ← **SPI 비활성** | △ SPI_Loop 주석처리 |
| 04_tx_control | STM32F103RCT6 | SPI Master ← **미존재** | ✗ |

빌드 환경:
- STM32: STM32CubeIDE, Ctrl+B 직접 빌드 (CLI `stm32cubeidec.exe` 불가 — GUI 서브시스템)
- nRF52: Segger Embedded Studio(SES), `emBuild` 가능

---

#### SPI 공통 스펙 (01-02 링크와 동일, 04-03 링크도 동일하게 적용)

**Wire 패킷 (11B 고정)**:
```
[HDR 1B][LEN=0x08][DATA[0..7] 8B][CRC 1B]
CRC = XOR(HDR, LEN, DATA[0..7])   ← _shared/oled_tv_protocol.c pkt_checksum()
```

**HDR 방향**:
- `0x10` TX 시스템 상태 / `0x11` TX 입력 Analog / `0x12` TX 출력 Analog → **04가 03에 전송 (TX→RX 방향)**
- `0x50` RX 시스템 상태 / `0x51` RX 입력+Vout Ref / `0x52` RX 출력 → **04가 03으로부터 수신 (RX→TX 방향)**

**SPI 파라미터**:
- 주기: 10ms cyclic (`PACKET_INTERVAL = 10`)
- CS: Low Active, **STM32가 Master** (클럭 생성)
- STM32 핀: SPI2, PB12(NSS) / PB13(SCK) / PB14(MISO) / PB15(MOSI) ← 01과 동일
- nRF52832 핀: SPIS1, P0.22(SCK) / P0.25(CSN) / P0.26(MISO) / P0.27(MOSI) ← 03도 동일

인코딩: Big-endian, 전압·전류 scale=0.01 (예: 47.95V → 4795)

**검증 핀포인트 — TX Buck Vout Ref 경로** (⚠️ §4 정정 4·5 참조):
```
01: rx_cmd.tx_buck_vout_ref (i16, scale 0.01)
  → pkt_build_rx(): 0x51 DATA[6..7] (wr_i16)
  → SPI → 02 수신 → ESB ACK payload → 03 수신 (g_last_ack_by_hdr[1])
  → 03 SPI_Loop: 0x51 패킷 MISO 서빙 → 04 수신
  → 04 UART 모니터: "0x51 | ...Tx_Buck_Vout_Ref=1200" 출력 (raw, ÷100 없음)
```

01에서 `buck 12.00` UART 명령 → 04 모니터에 raw `1200` 표시되면 검증 완료.

---

#### 작업 1 — 03_TX_ble SPI_Loop (⚠️ §4 정정 1 참조)

03_TX_ble 레포(`03_TX_ble/`) 파일을 확인:
1. `SPI_Loop` 기존 코드 확인 — SPIM이면 전면 재작성(02_RX_ble SPIS 구현 거울 복제).
2. `ADD_SPI` 전처리기 정의가 `.emProject`의 `c_preprocessor_definitions`에 있는지 확인.
3. `eta_spi` 모듈의 SPIS 패턴은 02_RX_ble와 동일 — 02 참조해 구현.
4. SPI_Loop 역할: `g_last_ack_by_hdr[3]` round-robin으로 MISO 서빙 + 04 TX 수신 카운트.
5. `emBuild` 에러 0 확인 후 커밋.

---

#### 작업 2 — 04_tx_control 더미 프로젝트 생성

**01_RX_control을 골격으로 복사**해 만든다.

**04와 01의 차이**:

| | 01_RX_control | 04_tx_control (더미) |
|---|---|---|
| SPI 역할 | Master → 02 수신 | Master → 03 수신 |
| 수신 HDR | 0x10/0x11/0x12 | 0x50/0x51/0x52 |
| 송신 HDR | 0x50/0x51/0x52 | 0x10/0x11/0x12 |
| 송신 데이터 | 실 ADC 센싱 | **더미 고정값** (0x00) |
| ADC | 6채널 실사용 | 불필요 — 제거 |
| PWM/제어 | 실 구현 | 불필요 — 제거 |
| UART 명령 | buck 명령 파싱 | 불필요 (선택) |

**04 구현 최소 범위** (⚠️ §4 정정 3 참조 — pkt_apply_rx 없음):
1. `app_spi.c/.h`: 01 코드 그대로 유지
2. `app_protocol.c`: 대폭 단순화
   - `exchange_packets()`: SPI 수신 + 10ms 주기로 더미 TX 패킷 송신
   - `print_packets()`: 1초 주기로 수신된 0x50/0x51/0x52를 `pkt_print_data_line(hdr, data)` 출력
3. `main.c`: ADC/PWM/CAN/DAC 관련 페리 제거. SPI+UART만 남김.
4. `_shared/` 폴더: 01과 동일.

**중요**: CubeMX 재생성 금지. STM32CubeIDE에서 Ctrl+B 직접 빌드.

---

#### 검증 절차 (D2 → D3)

**D2: SPI 링크 단독 확인**
1. 03_TX_ble DK 보드 + 04_tx_control 보드 SPI 핀 연결 (PB12-15 ↔ P0.22/25/26/27)
2. 04 UART 모니터 연결 (115200)
3. 04 모니터에 수신 카운트 증가 확인
4. 오실로스코프: CS(PB12) 10ms Δt 확인
5. CRC fail 카운트 = 0 확인

**D3: End-to-end Vout Ref**
1. 전체 체인: 01 + 02 + 03 + 04 동시 동작
2. 01 UART5 터미널: `buck 12.00` 명령
3. 04 UART 모니터: `0x51 | ...Tx_Buck_Vout_Ref=1200` 확인 (**raw 1200**)
4. `buck 5.00` → raw 500 으로 바뀌는지 확인

---

#### 참고 파일

wiki (`~/eta/wiki/teams/c/oled_tv_software/`):
- `status.md`, `pages/concepts/spi_packet_format.md`, `pages/concepts/app_protocol_module.md`
- `pages/entities/tx_ble_module.md`, `pages/concepts/nrf52_firmware_conventions.md`

---

#### 하지 말 것

- ADC 실 센싱, PWM/제어 로직, 04 UART 명령 파싱 — 불필요
- CubeMX 재생성, `git add -A`, `git commit --amend` — 금지

---

## 6. 환원 후보

- D2 완료 후: `tx_ble_module.md` SPI_Loop 행 △→✓, status.md 갱신
- D3 완료 후: D3 완료 표시, Vout Ref E2E 검증 사실 status.md 기록
- 04_tx_control entity 페이지 신규 (`pages/entities/tx_control_dummy.md`)
- (정리) 04 `.ioc` 파일명 `RX_control.ioc` → `TX_control.ioc` 개명 결정 후 기록
