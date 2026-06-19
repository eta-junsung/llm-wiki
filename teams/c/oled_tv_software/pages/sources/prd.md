---
tags: [source, prd]
source: teams/c/oled_tv_software/raw/prd_v1.0.md
date: 2026-05-26
subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
---

# PRD — OLED TV 무선 전력 전송 시스템 (v1.0, 2026-05-26)

인수 프로젝트 현재 이해 스냅샷. 전력 전송 자체가 아닌 **TX↔RX 제어 신호 교환** 펌웨어의 구조·현황·미해결 의문점을 정리한 문서. 코드·문서 파악 중인 시점의 기록이며 `[확인 필요]` 항목이 다수 존재.

**핵심 요구사항**: TX↔RX 제어 신호 지연 1~2ms 이내 (README 명시 기준).

---

## 시스템 구성

| 서브시스템 | MCU | 역할 |
|---|---|---|
| `01_RX_control` | STM32F103RCTx | 전력 제어 (SPI Master, PWM 4ch, ADC 6ch) |
| `02_RX_ble` | nRF52832 | ESB PRX — RX측 무선 모듈, SPI Slave |
| `03_TX_ble` | nRF52832 | ESB PTX — TX측 무선 모듈 |

```
[TX 보드] ─SPI(미구현)─ [03_TX_ble (PTX)]
                               │
                         ESB RF 2.4GHz
                               │
         [01_RX_control] ─SPI─ [02_RX_ble (PRX)]
```

---

## 통신 레이어 요약

- **STM32↔nRF SPI** (내부): 11B 고정, HDR 0x10~0x12/0x50~0x52, 10ms → [[spi_packet_format]]
- **ESB wire** (무선): 11B, HDR round-robin 0x10-0x12/0x50-0x52, 10ms, ACK with payload → [[esb_packet_format]], [[esb_link_layer]]

두 포맷은 별개. nRF가 능동적으로 변환한다.

---

## 펌웨어 현황 스냅샷

### 01_RX_control

구현됨: PWM 4ch(TIM8/TIM3), ADC 6ch DMA, SPI2 DMA Master, UART, trip zone, fault reset GPIO.

미완료: ADC 물리량 변환(`adc_calc()`가 0~3.3V 원시 전압만 전달. 분압비·NTC 변환 미적용) → [[adc_channel_map]]

비활성: CAN1(`#if 0`), DAC(초기화만), TIM2/4/5(핸들러 미구현)

### 02_RX_ble

구현됨: ESB PRX 기본 동작, SPI Slave 송수신, 버그 수정(커밋 `89e8609`).

미완료: ESB 타임아웃 stale 마킹 — `esb_recv`가 끊길 때 `tx_module.hdr=0x00`으로 STM32에 알리는 로직 없음.

### 03_TX_ble

구현됨: ESB PTX 기본 동작, ACK payload 수신, round-robin HDR 송신.

미완료: TX 보드 ↔ `03_TX_ble` SPI(`SPI_Loop`) — 전체 주석 처리됨.

---

## 미해결 의문점 (`[확인 필요]`)

1. **PWM 주파수 불일치**: `RX_control_PWM_가이드.md` 100kHz(PSC=0/ARR=639) vs `app_tim.c` ~1kHz(PSC=71/Period=999) → [[pwm_system]]
2. **ADC 물리량 변환 미구현**: 분압비/NTC 변환 어느 자리에서 할지 결정 필요 → [[adc_channel_map]]
3. **CAN1 용도**: 어떤 외부 장치와 통신하는지 미문서화.
4. **DAC 용도**: 초기화만 있고 사용처 없음.
5. **README 역할 오표기**: README에 `02=PTX, 03=PRX`라고 적혀 있으나 코드는 반대(`02=PRX, 03=PTX`). README 수정 필요.
6. **SPI 하드웨어 테스트 미실시**: `02_RX_ble` 코드 수정 후 STM32 실측 검증 전.

---

## 파생 페이지

- [[spi_packet_format]] — STM32-nRF 내부 SPI 프레임 (wire 11B, 컨테이너 43B/54B; HDR 0xC0은 구 표기)
- [[esb_packet_format]] — ESB wire 포맷 (11B, HDR round-robin)
- [[esb_link_layer]] — ESB 링크 파라미터
- [[rx_control]] — 01_RX_control STM32 entity
- [[rx_ble_module]] — 02_RX_ble nRF52832 PRX entity
- [[tx_ble_module]] — 03_TX_ble nRF52832 PTX entity

---

## 버전 관리

PRD 업데이트 시 새 버전 파일을 `raw/prd_vX.Y.md`로 추가하고 본 sources 페이지의 source frontmatter와 날짜를 갱신한다.
