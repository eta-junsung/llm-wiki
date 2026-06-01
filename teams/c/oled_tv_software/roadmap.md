---
tags: [roadmap, oled_tv_software, living-doc]
date: 2026-06-01
---

# oled_tv_software — 전체 로드맵

> 전략 큰그림(big picture). 목표까지의 마일스톤 호(arc)와 현재 위치의 spine만 여기 둔다.
> 깊은 디테일은 concept 페이지로 백링크 위임, **기능별 구현 현황·다음 시작점은 [[status]]** (status.md)에서 관리한다.
> **사실 / 가설 / 모름을 구분한다. 추정은 "[추정]" 표기.**

---

## 0. 한 줄 요약

OLED TV 무선 전력 전송 시스템의 **3-MCU 제어신호 교환 펌웨어**(전력 전송 자체 아님). 인수받은 코드를 ESB 기준으로 안정화하는 중. **PRD 핵심 목표: TX↔RX 제어 신호 지연 1~2 ms 이내**. 무선(ESB)·내부(SPI) 링크는 동작하나, SPI 10 ms 폴링 주기 미달(M3 막힘)과 장시간 안정성 미검증이 목표 게이트 앞을 막고 있다. 구성·프로토콜은 [[prd]].

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
[M3] SPI 10 ms 폴링 주기 달성   ◄── ★ 현재 막힘 (DMA IRQ 의심)
        ▼
[M4] SPI 클럭 9 MHz 상향
        ▼
[M5] end-to-end 제어신호 지연 1~2 ms 충족 검증  ◄── PRD 목표 게이트
        ▼
[M6] 장시간 안정성 + UART 브리지 완주
```

| 단계 | 달성 목표 | 완료 기준 | 상태 |
|------|-----------|-----------|------|
| **M0** | 코드·문서 인수, 구조 이해 | [[prd]] 스냅샷 작성 | ✓ (사실) |
| **M1** | ESB TX/RX 동작 | TX 주기·ACK 수신 실측 | △ 동작·장시간 미검증 (TX~920 µs/ACK~940 µs 실측, [[esb_timing_measurements]]) |
| **M2** | SPI 링크 안정화 (heartbeat·오류율·복구) | heartbeat 실보드 검증 | △ heartbeat ✓, 오류율 모니터·`spi_tx_busy` 복구 미검증 ([[spi_link_reliability]]) |
| **M3** | SPI 10 ms 폴링 주기 | CS 10 ms 주기 동작 + `spi_fail_cnt` 안정 | ✗ **막힘** — DMA IRQ(NVIC) 부재 의심 |
| **M4** | SPI SCK 9 MHz 상향 | 9 MHz 안정 전송 | ✗ revert(`7143f55`), nRF52832 SPIS 최대 SCK datasheet 선결 |
| **M5** | 제어신호 지연 1~2 ms (PRD) | end-to-end 왕복 지연 실측 ≤ 2 ms | ? 미도달 — M3 종속 |
| **M6** | 장시간 안정성·UART 브리지 | 연속 동작 + 01↔02 브리지 확인 | ? 미도달 |

> **(가설)** M3(10 ms 미동작)의 유력 원인은 STM32 `HAL_SPI_MspInit`의 DMA IRQ(`HAL_NVIC_EnableIRQ`) 부재 → DMA 완료 콜백 미수신. M5(PRD 지연 목표)는 현재 SPI 주기가 사양(10 ms)에 못 미쳐 **측정 전제 자체가 미성립** → M3 통과가 첫 게이트.

---

## 3. 현재 어디인가 — M3 (SPI 10 ms 폴링) 막힘

> 기능별 실측·다음 시작점은 [[status]]가 단일 소스. 여기는 요지만.

- **(사실)** `PACKET_INTERVAL=10`(`_shared/oled_tv_protocol.h`) 반영했으나 실보드에서 CS가 10 ms 주기로 내려가지 않음.
- **(사실)** heartbeat 200 ms 독립 타이머는 실보드 검증 완료(✓).
- **(가설·미채택)** DMA IRQ(NVIC) 미활성 → 콜백 미발생 → 폴링 미진행. 다음 라운드에서 `HAL_SPI_MspInit` 확인 후 CS 주기·`spi_fail_cnt` 측정 (검증 핀: PB12 → [[gpio_verification_pinmap]]).
- **(모름)** nRF52832 SPIS 최대 SCK 클럭 (9 MHz 상향 재시도 전 datasheet 선결).

---

## 4. 앞으로 얼마나 남았는가

> 기간은 [추정]. M3 해소 여부가 첫 게이트 — 통과 전엔 M5(PRD 목표) 측정 불가.

| 단계 | 난이도 | 기간 추정 | 비고 |
|------|--------|-----------|------|
| M3 (10 ms) | 중~높음 | 수일 [추정] | DMA IRQ 확인이 첫 수 |
| M4 (9 MHz) | 중 [추정] | 1~2일 [추정] | datasheet ingest 선결 |
| M5 (PRD 지연) | 중 [추정] | M3·M4 후 재추정 | end-to-end 측정 셋업 필요 |
| M6 (안정성/브리지) | 중 [추정] | 수일 [추정] | 장시간 연속 동작 |

---

## 5. 환원 후보 (wiki ↔ 코드 어긋남)

- nRF52832 SPIS 최대 SCK datasheet 미ingest — M4 선결, ingest 시 [[esb_link_layer]] 또는 신규 source 페이지.
- M5(PRD 1~2 ms 지연)의 end-to-end 측정 방법 미정 — 확정 시 [[gpio_verification_pinmap]]에 검증 행 추가.
