---
date: 2026-06-26
tags: [weekly-report, oled_tv_software, comm_st, esb, handover]
project: oled_tv_software
---

# c팀 OLED TV 소프트웨어 업무 보고

**기간**: 2026-06-19 ~ 2026-06-25
**시스템**: OLED TV 전력 변환 제어 펌웨어 (01_RX_control / 02_RX_ble / 03_TX_ble)

---

## 요약

이번 주는 두 가지 작업을 완료했다.

1. **커스텀 보드(UTO-NBK-52) comm_st 재검증 완료**: SPI 배선 후 통신 상태 4케이스 전체 검증, 신규 케이스 확인, 02 seed 버그 수정 커밋, 03_TX_ble 실보드 검증 완료.
2. **시립대 보드 전달 완료**: 핀맵·구동 절차·PC GUI 사용법 문서 작성 후 01·02·03 보드 전달.

---

## 1. 커스텀 보드 comm_st 재검증

### 1.1 SPI 배선 및 케이스 검증

UTO-NBK-52(#02·#03) SPI 배선(P0.22/P0.25/P0.26/P0.27) 완료 후 comm_st 케이스를 재검증했다.

| 케이스 | SPI (bit5) | ESB (bit6) | GUI | 결과 |
|--------|-----------|-----------|-----|------|
| 01+02+03 전부 ON | UP | UP | SPI UP / ESB UP | ✓ |
| 01+02 ON, 03 OFF | UP | DOWN | SPI UP / ESB DOWN | ✓ |
| SPI 배선 단선 | DOWN | DOWN | SPI DOWN / ESB DOWN | ✓ |
| **02만 ON (신규)** | UP | DOWN | SPI UP / ESB DOWN | ✓ |

신규 케이스: 02만 단독으로 켰을 때 SPI UP / ESB DOWN이 정상 표시됨을 추가 확인했다.

### 1.2 02 seed 버그 수정

"01+02 only 구동 시 SPI DOWN 오판" 버그의 원인을 확인하고 수정 커밋했다.

- **원인**: `eta_protocol.c`에서 `esb_pkt`(ESB 수신 → SPI forward) 버퍼를 초기화하지 않아, 01이 미초기화 패킷을 SPI로 수신 → heartbeat 비트 판정 실패 → SPI DOWN 오판.
- **수정**: `eta_protocol.c:227-232`에 `esb_pkt` seed 추가. DK 보드에서 01+02 only 구동 시 SPI UP / ESB DOWN 정상 확인.

### 1.3 03_TX_ble 실보드 검증

| 검증 항목 | 방법 | 결과 |
|----------|------|------|
| ESB PTX 동작 | Monitor_Loop UART 출력 확인 | ✓ |
| P0.17 (`DBG_PIN_TX_ATTEMPT`) | 오실로스코프 측정 | ✓ (~920 us 주기) |
| P0.18 (`DBG_PIN_TX_DONE`) | 오실로스코프 측정 | ✓ |

---

## 2. 시립대 보드 전달

### 2.1 전달 문서 작성

| 문서 항목 | 내용 |
|----------|------|
| 핀맵 | SPI(CS/SCK/MISO/MOSI) · UART 배선, STM32 ↔ nRF52 대응 |
| 구동 확인 절차 | 전원 투입 순서, LED 정상 상태, comm_st 케이스별 기대 동작 |
| PC GUI 사용법 | `rx_gui.exe` 실행, COM 포트 연결, buck 지령 입력 방법 |

전달 문서 전문: [[시립대_전달]]

### 2.2 전달 내역

01_RX_control(STM32), 02_RX_ble(UTO-NBK-52), 03_TX_ble(UTO-NBK-52) 보드 3종 전달 완료.

---

## 다음 작업

| 순위 | 작업 | 내용 |
|------|------|------|
| 1 | **SPI 폴링 주기 단축** | 01-02, 03-04 양쪽 `PACKET_INTERVAL` 10ms → 5ms 변경 후 실보드 재검증 |
| 2 | **01·04 상호 SPI 링크 상태 인지** | 04-03 SPI 단절 시 01이 인지 / 01-02 SPI 단절 시 04가 인지. 02·03이 자체적으로 SPI 통신 상태를 파악하는 메커니즘 필요 — 구체 구현 방향은 작업 진입 시 결정 |
