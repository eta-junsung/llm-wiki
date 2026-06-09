---
tags: [roadmap, oled_tv_software, living-doc]
date: 2026-06-09
---

# oled_tv_software — 전체 로드맵

> 전략 큰그림(big picture). 목표까지의 마일스톤 호(arc)와 현재 위치의 spine만 여기 둔다.
> 깊은 디테일은 concept 페이지로 백링크 위임, **기능별 구현 현황·다음 시작점은 [[status]]** (status.md)에서 관리한다.
> **사실 / 가설 / 모름을 구분한다. 추정은 "[추정]" 표기.**

---

## 0. 한 줄 요약

OLED TV 무선 전력 전송 시스템의 **3-MCU 제어신호 교환 펌웨어**(전력 전송 자체 아님). 인수받은 코드를 ESB 기준으로 안정화하는 중. SPI 10 ms 폴링(M3) 확정 + comm-state 비트 2개(SPI·BLE/ESB) 실보드 검증 완료 → **현재 스코프(M0~M3) 달성**. M4(9 MHz 상향)·M5(PRD 1~2 ms 지연)·M6(장시간 안정성/브리지)는 **2026-06-09 결정으로 보류**(지금 불필요). 구성·프로토콜은 [[prd]].

---

## 1. 시스템 구성 (호의 배경)

| 서브시스템 | MCU | 역할 | entity |
|---|---|---|---|
| 01_RX_control | STM32F103RCT6 | PWM 4ch·ADC 6ch, SPI Master | [[rx_control]] |
| 02_RX_ble | nRF52832 | ESB PRX, SPI Slave | [[rx_ble_module]] |
| 03_TX_ble | nRF52832 | ESB PTX | [[tx_ble_module]] |

링크: STM32↔nRF 내부 SPI([[spi_packet_format]]), nRF↔nRF 무선 ESB([[esb_packet_format]], [[esb_link_layer]]).

---

## 2. 마일스톤 호 전체 구조

```
[M0] 펌웨어 인수 + 구조 파악 ─┐
[M1] ESB 무선 링크 동작        ─┤ (대체로 동작)
[M2] STM32↔nRF SPI 링크 안정화 ─┘
        ▼
[M3] SPI 10 ms 폴링 주기 달성   ✓ 확정 (2026-06-01)
        ▼
   (현재 스코프 종료 — M4~M6 보류)
```

| 단계 | 달성 목표 | 완료 기준 | 상태 |
|------|-----------|-----------|------|
| **M0** | 코드·문서 인수, 구조 이해 | [[prd]] 스냅샷 작성 | ✓ (사실) |
| **M1** | ESB TX/RX 동작 | TX 주기·ACK 수신 실측 | △ 동작·장시간 미검증 (TX~920 µs/ACK~940 µs 실측, [[esb_timing_measurements]]) |
| **M2** | SPI 링크 안정화 (heartbeat·오류율·복구) | heartbeat 실보드 검증 | △ heartbeat ✓, 오류율 모니터·`spi_tx_busy` 복구 미검증 ([[spi_link_reliability]]) |
| **M3** | SPI 10 ms 폴링 주기 | CS 10 ms 주기 동작 + `spi_fail_cnt` 안정 | ✓ ok=4799/49s, crcfail=0, 오실로 Δt=10ms ([[spi_10ms_diagnosis_report_260601]]) |

> **(사실)** M3 확정(2026-06-01): "미동작"은 동작 결함이 아닌 관측 도구 한계였음 — `rx_status.spi_status` 단일 필드 덮어쓰기로 패턴 불가시. NVIC enable은 `MX_DMA_Init()`에 정상 존재. ([[spi_10ms_diagnosis_report_260601]])

> **(사실)** M3 이후 comm-state 비트 2개 완료(2026-06-08): SPI_Comm_St heartbeat(`e5e3efc`)·BLE(ESB)_Comm_St presence 판정(`6cd7e6c`) 모두 실보드 검증. M 호에는 없던 별트랙 작업 — 상세는 [[comm_state_monitoring]], 현황은 [[status]].

---

## 3. 현재 어디인가 — 현재 스코프(M0~M3) 달성, 후속은 별트랙

> 기능별 실측·다음 시작점은 [[status]]가 단일 소스. 여기는 요지만.

- **(사실)** M3 통과(2026-06-01): SPI 10 ms 폴링 확정. 초당 100 트랜잭션, CRC fail 0건.
- **(사실)** heartbeat 200 ms 독립 타이머 실보드 검증 완료(✓).
- **(사실)** comm-state 비트 2개(SPI/BLE) 실보드 검증 완료(2026-06-08).
- **남은 활성 작업은 M 호 밖의 별트랙뿐** — comm-state (T,N) 상수 통일·spi_status LINK/CRC 분리·COMM 라인 완료(`d2232fe`), 다음 = 02/03 COMM 라인 와이어링·N=20 실측·회사보드 LED3 전환. 단일 소스 [[status]] "다음 시작점".

---

## 4. 보류된 단계 (M4~M6 — 2026-06-09 결정, 지금 불필요)

> 삭제가 아니라 **보류**. 필요 시 아래를 호로 되살린다. 보류 시점 사실 스냅샷.

| 단계 | 달성 목표 | 보류 시점 상태 | 비고 |
|------|-----------|-----------------|------|
| **M4** | SPI SCK 9 MHz 상향 | ✗ revert(`7143f55`), 현재 4.5 MHz 동작 | 재시도 시 nRF52832 SPIS 최대 SCK datasheet ingest 선결 (현재 "모름") |
| **M5** | 제어신호 지연 1~2 ms (PRD 핵심 목표) | ? 미도달 | end-to-end 왕복 측정 셋업 미정. SPI 10 ms 폴링이 병목 가능성 |
| **M6** | 장시간 안정성·UART 브리지 | ? 미도달 | ESB 연속 동작 + 01↔02 브리지 확인 |

> **주의:** M5는 원래 PRD 핵심 목표(TX↔RX 지연 1~2 ms)였다. 보류는 곧 **PRD 목표 검증을 현재 스코프에서 제외**한다는 뜻 — 재개 결정 시 이 함의를 먼저 확인할 것.

---

## 5. 환원 후보 (wiki ↔ 코드 어긋남)

- 코드 정리 라운드 (tasks/monitor-formatting 이후, 미착수): ① 모니터 1-헤더-1-줄 압축, ② 공유 출력 함수(`oled_tv_protocol.c` 신설, 3 빌드 등록), ③ serialize/deserialize 통합, ④ `SPI_PKT_*` → 링크 중립 이름 개명. eta-explorer로 묶어 시작 권장. → 작업 로드맵 [[roadmaps/spi-esb-refactor|SPI·ESB 리팩토링]].
- PC GUI (아이디어·미착수): UART 패킷 모니터링 + `buck` 설정 호스트 툴. 설정 포트(01 UART5)와 모니터 포트(03 Monitor/01 Monitor_Loop) 조합 결정 선행. → 작업 로드맵 [[roadmaps/pc-gui|PC GUI]].
- ~~BLE_Comm_St ESB-health 연결~~ ✓ 완료(`6cd7e6c`, 2026-06-08): presence 리셋 윈도우(`esb_rx_cnt`/`esb_ack_cnt` delta) 판정→0x10 bit6. `ble_link` 심볼은 코드에 없었음(폐기). 상세 [[comm_state_monitoring]]. 후속(`d2232fe`, 2026-06-09): (T,N) 상수 통일(N 3→20)·spi_status LINK/CRC 분리·COMM 라인. 다음 = 02/03 COMM 라인·N=20 실측.
- `spi_wr_u16`에 음수 ADC 패턴 교정: `03_TX_ble build_tx_pkt case1·2` → `spi_wr_i16` 신설 — 별도 task, 미착수.
- (보류) nRF52832 SPIS 최대 SCK datasheet ingest — M4 재개 시 선결. [[esb_link_layer]] 또는 신규 source 페이지.
- (보류) M5(PRD 1~2 ms 지연) end-to-end 측정 방법 미정 — 재개 시 [[gpio_verification_pinmap]]에 검증 행 추가.
