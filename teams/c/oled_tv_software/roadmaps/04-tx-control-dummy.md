---
tags: [roadmap, oled_tv_software, 04_tx_control, living-doc]
date: 2026-06-11
---

# 04_tx_control 더미 프로젝트 — 작업 로드맵

> 03_TX_ble SPI 출력 단까지 직접 검증하기 위한 STM32 더미 수신 프로젝트.
> 04_tx_control 실물은 타팀 개발 — 이 프로젝트는 "03 SPI_Loop 동작 + Vout Ref 전달 경로" 확인이 목적이다.

---

## 0. 한 줄 요약

01_RX_control 골격을 복사해 STM32 SPI Master 더미(04_tx_control)를 만들고, 03_TX_ble SPI_Loop를 활성화해 **01이 보낸 TX Buck Vout Ref 값이 04 UART 모니터까지 도달하는지** 검증한다.

---

## 1. 데이터 흐름

```
01_RX_control (STM32, SPI Master)
  └─ SPI(10ms) ──→ 02_RX_ble (nRF52, SPI Slave, ESB PRX)
                      └─ ESB ACK ──→ 03_TX_ble (nRF52, ESB PTX, SPI Slave ※활성화 필요)
                                          └─ SPI(10ms) ──→ 04_tx_control ★신규
```

**검증 핀포인트**: 01의 `rx_cmd.tx_buck_vout_ref` → `0x51` DATA[6..7] → 02 → ESB ACK → 03 → SPI → 04 UART 모니터 표시.

---

## 2. 마일스톤 호

| 단계 | 내용 | 완료 기준 | 상태 |
|------|------|-----------|------|
| **D0** | 03_TX_ble SPI_Loop 활성화 | 빌드 통과, 핀 연결 전 smoke test | ✗ |
| **D1** | 04_tx_control 더미 프로젝트 생성 | SPI Master 빌드 통과 | ✗ |
| **D2** | 03 ↔ 04 SPI 링크 동작 | CS 10ms Δt 오실로 확인, CRC fail 0 | ✗ |
| **D3** | 01→02→ESB→03→04 End-to-end | 01 `buck=Xv` 명령 → 04 모니터 Vout Ref 표시 | ✗ |

---

## 3. 현재 위치 → [[status]]

---

## 4. 핸드오프 프롬프트 (구현 세션용)

> 이 절이 단독 Claude 세션에 그대로 전달되는 자급자족 프롬프트다.

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

**검증 핀포인트 — TX Buck Vout Ref 경로**:
```
01: rx_cmd.tx_buck_vout_ref (i16, scale 0.01)
  → pkt_build_rx(): 0x51 DATA[6..7] (wr_i16)
  → SPI → 02 수신 → ESB ACK payload → 03 수신 (g_rx_data 버퍼)
  → 03 SPI_Loop: 0x51 패킷 전달 → 04 수신
  → 04 UART 모니터: "0x51 | ...Vout_Ref=X.XXV" 출력
```

01에서 `buck=12.00V` UART 명령 → 04 모니터에 `12.00V` 표시되면 검증 완료.

---

#### 작업 1 — 03_TX_ble SPI_Loop 활성화

03_TX_ble 레포(`03_TX_ble/`) 파일을 확인:
1. `SPI_Loop` 함수 전체가 주석 처리돼 있음. 코드를 찾아 활성화할 것.
2. `ADD_SPI` 전처리기 정의가 `.emProject`의 `c_preprocessor_definitions`에 있는지 확인. 없으면 추가.
3. `eta_spi` 모듈(`eta_spi.c`/`eta_spi.h`)의 `spi_drv_init`·`spi_set_buffers`·`spis_xfer_done` 플래그 사용 패턴은 02_RX_ble와 동일 — 02 참조해 구현.
4. SPI_Loop가 수행할 일: `g_rx_data`(ESB ACK로 받은 RX 패킷들)를 `spi_tx_pkt`에 round-robin으로 직렬화해 STM32(04)에 전달. 반대로 STM32에서 수신한 `spi_rx_pkt`에서 TX 데이터 파싱.
5. `emBuild` 에러 0·경고 0 확인 후 커밋.

---

#### 작업 2 — 04_tx_control 더미 프로젝트 생성

**01_RX_control을 골격으로 복사**해 만든다. 둘은 같은 STM32F103RCT6, SPI2 동일 핀, `_shared` 동일 패킷 포맷을 사용한다.

**04와 01의 차이**:

| | 01_RX_control | 04_tx_control (더미) |
|---|---|---|
| SPI 역할 | Master → 02 수신 | Master → 03 수신 |
| 수신 HDR | 0x10/0x11/0x12 | 0x50/0x51/0x52 |
| 송신 HDR | 0x50/0x51/0x52 | 0x10/0x11/0x12 |
| 송신 데이터 | 실 ADC 센싱 | **더미 고정값** (0x00 or 상수) |
| ADC | 6채널 실사용 | 불필요 — 제거 |
| PWM/제어 | 실 구현 | 불필요 — 제거 |
| UART 명령 | buck 명령 파싱 | 불필요 (선택) |

**04 구현 최소 범위**:
1. `app_spi.c/.h`: 01 코드 그대로 유지 (SPI2 Master, DMA, 동일 핀)
2. `app_protocol.c`: 대폭 단순화
   - `exchange_packets()`: SPI 수신(`pkt_apply_rx`로 역직렬화) + 10ms 주기로 더미 TX 패킷 송신
   - `print_packets()`: 1초 주기로 **수신된 0x50/0x51/0x52 내용** UART 출력. `pkt_print_status_line`·`pkt_print_data_line` 활용하거나 직접 printf.
3. `main.c`: ADC, PWM, CubeIDE 생성 페리 제거. SPI+UART만 남김.
4. `_shared/` 폴더: 01과 동일하게 링크/복사.

**중요**: CubeMX 재생성 금지. STM32CubeIDE에서 Ctrl+B 직접 빌드.

---

#### 검증 절차 (D2 → D3)

**D2: SPI 링크 단독 확인**
1. 03_TX_ble DK 보드 + 04_tx_control 보드 SPI 핀 연결 (PB12-15 ↔ P0.22/25/26/27)
2. 04 UART 모니터 연결 (115200)
3. 03만 먼저 단독 동작 → 04 모니터에 수신 카운트 증가 확인
4. 오실로스코프: CS(PB12) 10ms Δt 확인
5. CRC fail 카운트 = 0 확인

**D3: End-to-end Vout Ref**
1. 전체 체인: 01 + 02 + 03 + 04 동시 동작
2. 01 UART5 터미널: `buck=12.00V` 명령 전송
3. 04 UART 모니터: 수신된 `0x51 | ...Vout_Ref=12.00V` 표시 확인
4. 다른 값(`buck=5.00V`)으로 바꿨을 때 04도 따라 변경되는지 확인

---

#### 참고 파일

wiki (`~/eta/wiki/teams/c/oled_tv_software/`):
- `status.md` — 현재 구현 상태 전체
- `pages/concepts/spi_packet_format.md` — wire 11B 스펙 + round-robin 상수
- `pages/concepts/app_protocol_module.md` — 01의 프로토콜 계층 구조 상세
- `pages/entities/tx_ble_module.md` — 03 현황 (SPI_Loop 주석처리 상태)
- `pages/concepts/nrf52_firmware_conventions.md` — ISR 규칙, eta_ 모듈 의존 방향

펌웨어 레포 참고 파일:
- `01_RX_control/Application/Src/app_protocol.c` — 04 골격용 원본
- `01_RX_control/Application/Src/app_spi.c` — SPI Master DMA 그대로 재사용
- `03_TX_ble/Application/Src/main.c` (또는 eta_protocol.c) — SPI_Loop 주석 찾기
- `_shared/oled_tv_protocol.c/.h` — 공유 패킷 빌더·파서

---

#### 하지 말 것 (범위 외)

- ADC 실 센싱 → 더미 고정값으로 충분
- PWM/제어 로직 → 전혀 불필요
- 04의 UART 명령 파싱 → 선택사항, 검증에 필요 없음
- CubeMX 재생성 → 금지
- `git add -A` → 금지; `git commit --amend` → 금지
- 04를 실제 TX 보드 스펙에 맞출 것 → 더미이므로 무관

---

## 5. 환원 후보

- D2 완료 후: `tx_ble_module.md` SPI_Loop 행 ✗→✓, status.md 갱신
- D3 완료 후: roadmap §3 D3 완료 표시, Vout Ref 경로 검증 사실 status.md 기록
- 04_tx_control entity 페이지 신규 (`pages/entities/tx_control_dummy.md`)
