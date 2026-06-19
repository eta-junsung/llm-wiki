---
tags: [briefing, oled_tv_software, team]
source: status·roadmap 기반 수작업 정리
date: 2026-06-19
---

# oled_tv_software — 팀 업무보고 참고 자료

> 주간 팀 보고 시 이 페이지를 열고 아래 흐름 순서로 설명.
> 기술 수치·상태 기호는 [[status]]·[[roadmap]]이 단일 소스 — 보고 직전 확인.

---

## 보고 스냅샷 이력 (주차별 — 다음주 diff 기준)

| 보고일 | 위치 | 그 주 핵심 | 다음 계획 |
|--------|------|-----------|-----------|
| **2026-06-12** | 별트랙 거의 완료 | **① SPI·ESB comm-state 비트 2개 실보드 검증 완료**(bit5 heartbeat / bit6 presence), **② PC UART 바이너리 모니터 + GUI 완성·실보드 검증**(6패널·Physical 변환·FW 버전 표시), **③ TX Buck Set E2E 실측 확인**(GUI `222.22V` → 03 터미널 `Tx_Buck_Vout_Ref=22222`), **④ 02 리팩토링·eta_ 전환 ✓ / 03 리팩토링 빌드 ✓ / _shared 다듬기 ✓**, **⑤ 03 SPIS 재작성 + 04_tx_control 더미 신설(4보드 E2E 준비)** | 04 CubeIDE 빌드 → 4보드 플래시 → 03↔04 SPI 링크 검증 → E2E(`buck 12.00`→04 raw 1200) |
| **2026-06-19** | 4보드 E2E 완료 + 커스텀 보드 도착 | **① 01 정본 코드(HSI 64MHz) DK 재검증 완료**(STEP1), **② 실보드 UART 검증 완료**(STEP2), **③ 4보드 E2E 전 체인 완료** — 04 Nucleo 포팅·03↔04 SPI 링크(D2)·`buck 12.00`→04 raw `1200`(D3), **④ UTO-NBK-52 커스텀 보드 입수·flash·LED active-HIGH 확정**, **⑤ 02 esb_pkt seed 누락 버그 발견·DK 검증(미커밋)** | 점퍼 수령 → 커스텀 보드 SPI 배선 → comm_st 4케이스 재검증 → seed 수정 커밋 |

---

## 이번주 진행 & 만난 문제 (6/12 ~ 6/18)

### 진행

1. **01 정본 코드베이스 전환 + DK 재검증 (6/15~6/17, STEP 1)**: Sean 원본(AppSequence/AppCtrl) HSI 64MHz 기준으로 코드베이스 전환. PCLK1=32MHz, SPI 8Mbps 확정. STM32 Mini Pro + PCA10040 DK 보드에서 UART5 수신·SPI bit5 토글·ESB bit6 확인 완료.
2. **실보드 UART 검증 (6/17, STEP 2)**: 실보드에서 PC GUI 11B 바이너리 수신 정상 확인.
3. **4보드 E2E 전 체인 완료 (6/16~6/17, D1~D3)**:
   - D1: 04 CubeIDE 빌드 에러 0, 4보드 플래시
   - D2: 03↔04 SPI CS 10ms Δt 확인
   - D3: GUI `buck 12.00` → 04 TeraTerm(VCP, USART2) raw `1200` 도달 확인
   - 04 Nucleo 포팅: NUCLEO-F103RB(STM32F103RBT6), UART5→USART2(PA2/PA3, VCP), HSI 64MHz
4. **UTO-NBK-52 커스텀 보드 입수·flash (6/17~6/18)**: #02/#03 2장 입수. SES `Build+Erase All+Download`로 flash 완료. LED active-HIGH 확정(`LED*_ON=1u`, `LED*_OFF=0u` 수정 → LED1 정상 점등, 이전 "개체 결함" 기록 폐기).
5. **02 esb_pkt seed 누락 버그 발견·수정 (6/18)**: 01+02만 구동 시 SPI DOWN 오판의 root cause. `eta_protocol.c:227-232` `pkt_seed_buffers(esb_pkt, ...)` 추가 → DK 보드 "SPI UP / ESB DOWN" 정상 판정 확인. **미커밋**.

### 만난 문제 & 해결

| 문제 | 원인 | 해결 |
|------|------|------|
| 커스텀 보드 LED 미점등 | firmware active-LOW 가정, 커스텀 보드는 active-HIGH | `LED*_ON=1u`/`LED*_OFF=0u` 수정, `CONFIG_NFCT_PINS_AS_GPIOS` 추가 |
| stale .hex nrfjprog 시 HardFault | emBuild incremental-skip으로 이전 .hex 재사용 | 빌드 전 `Output/Debug` 폴더 삭제 안전책 확립([[st_link_nrf52_flash]]) |
| 01+02만 구동 시 SPI DOWN 오판 | 02 `esb_pkt` seed 누락 — 초기화 없는 ESB forward 버퍼가 heartbeat bit 오염 | `eta_protocol.c:227-232` `pkt_seed_buffers(esb_pkt, ...)` 추가, DK 검증 통과 |

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

### 별트랙 완료 현황 (6/19 기준)

```
[B1] comm-state 비트 2개 (SPI heartbeat / ESB presence)   ✓  실보드 검증
[B2] app_protocol 적출 (protocol_loop() 단일 진입점)       ✓  실보드 검증
[B3] PC UART 바이너리 모니터 + GUI                         ✓  실보드 검증
[B4] 02_RX_ble 모듈 분리 + eta_ 접두사 전환               ✓  실보드 검증
[B5] _shared 프로토콜 다듬기 (심볼 정리·상수화)            ✓  실보드 검증
[B6] 03_TX_ble 모듈 분리 리팩토링                          △  빌드 ✓, 실보드 미검증
[B7] 03 SPI_Loop SPIS 재작성                               △  빌드 ✓, 실보드 미검증
[B8] 04_tx_control 더미 (E2E 검증용 STM32)                 ✓  Nucleo 포팅 완료 (6/17)
[STEP1] DK 보드 재검증 (정본 HSI 기준)                     ✓  완료 (6/17)
[STEP2] 실보드 UART 검증                                   ✓  완료 (6/17)
[D1] 04 빌드·플래시                                        ✓  완료 (6/17)
[D2] 03↔04 SPI 링크 검증                                   ✓  완료 (6/17)
[D3] E2E: buck 12.00 → 04 raw 1200                        ✓  완료 (6/17)
[STEP3] 커스텀 보드 comm_st 재검증                         ▶  진행 중 (점퍼 수령 대기)
```

---

## 3. 이번주 진행 & 만난 문제 (6/12 ~ 6/18)

→ 상단 "이번주 진행 & 만난 문제 (6/12 ~ 6/18)" 절 참조.

### 누적 진행 이력 (6/5 ~ 6/11)

1. **comm-state 완성 (6/8)**: SPI_Comm_St(bit5, 200ms heartbeat) + ESB_Comm_St(bit6, 200ms presence) 모두 실보드 검증 완료.
2. **PC UART GUI 완성 (6/10)**: 01 UART5 텍스트 → 11B 바이너리 전환. GUI 6패널, Physical 변환. E2E 실측: GUI `222.22V` → 03 터미널 `Tx_Buck_Vout_Ref=22222`.
3. **코드 정리 3종 (6/9~6/11)**: `app_protocol` 적출, 02 리팩토링(6모듈·eta_ 전환), `_shared` 다듬기 — 3펌웨어 실보드 검증.
4. **E2E 준비 (6/11)**: 03 SPI_Loop SPIM→SPIS 재작성, 04_tx_control 더미 신설.

---

## 4. 지금 어디 / 막힌 곳

### 4-1. 완료

- **SPI·ESB 링크 health 모니터링**: 3-MCU comm-state 비트 2개 실보드 검증 완료.
- **PC UART GUI + E2E**: 바이너리 전환·host 도구·4보드 E2E 전 체인 완료.
- **코드 구조 정리**: 01 app_protocol·02 리팩토링·_shared 다듬기 실보드 검증.
- **4보드 E2E (D1~D3)**: 04 Nucleo 포팅·03↔04 SPI 링크·buck E2E 완료 (6/17).
- **DK/실보드 검증 (STEP1·2)**: 정본 HSI 코드 DK 재검증 + 실보드 UART 수신 확인 완료 (6/17).
- **커스텀 보드 입수·flash**: UTO-NBK-52 #02/#03 flash, LED active-HIGH 확정 (6/18).

### 4-2. 완료 (추가, 6/19 확인)

- **STEP3 커스텀 보드 comm_st 재검증**: SPI 배선 후 4케이스 + "02만 ON → SPI UP/ESB DOWN" 신규 케이스 확인 완료.
- **02 seed 수정 커밋**: `eta_protocol.c` seed 수정 commit & push 완료.
- **03_TX_ble 실보드 검증**: ESB PTX 동작·P0.17/18 오실로 확인 완료.

---

## 5. 다음 작업 — 어떻게 진행할 예정인가

**시립대 보드 전달 준비 (01·02·03, 04는 시립대 자체 준비)**

```
[P1] 각 보드 핀맵 정리 (01 STM32 / 02 nRF52 RX / 03 nRF52 TX)
     — SPI 배선, UART5, 전원, 디버그 핀 포함
[P2] 각 보드 구동 확인 절차 정리
     — 플래싱 방법, 전원 투입 순서, 정상 동작 판별 기준
[P3] PC GUI 사용법 및 기타사항 정리
     — uart_gui.py 실행·설정·패널 설명, buck 설정법, SPI/ESB 상태 해석
```

---

> 상세 기술 맥락: [[status]] (현재 위치·다음 시작점) · [[roadmap]] (M호·별트랙 전체) · [[comm_state_monitoring]] (링크 health 비트) · [[app_protocol_module]] (protocol_loop) · [[pc_uart_gui]] (host GUI) · [[nrf52_firmware_conventions]] · [[nrf52_module_naming]]
