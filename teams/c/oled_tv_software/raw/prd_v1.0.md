# OLED TV 무선 전력 전송 시스템 PRD

## 1. 시스템 개요

본 문서는 OLED TV 무선 전력 전송 시스템의 **제어 신호 교환** 펌웨어에 대한 현재 이해 스냅샷이다. 전력 전송 자체가 아니라, TX측과 RX측 사이에서 제어 신호를 주고받는 경로와 그 구현 상태를 다룬다.

인수받은 프로젝트로, 현재 코드·문서 파악 중인 상태이다. 본 PRD는 이 시점의 이해를 정리한 것이며, 검증되지 않은 항목은 `[확인 필요]`로 표기하고 6. 미해결 의문점에 일람했다.

핵심 요구사항: TX↔RX 제어 신호 지연 1~2ms 이내 (README 명시 기준).

---

## 2. 하드웨어 구성

| MCU | 디렉토리 | 역할 |
|-----|----------|------|
| STM32F103RCTx | `01_RX_control` | 전력 제어 유닛 (SPI Master, PWM 4ch, ADC 6ch) |
| nRF52832 | `02_RX_ble` | ESB PRX — RX측 무선 모듈, SPI Slave |
| nRF52832 | `03_TX_ble` | ESB PTX — TX측 무선 모듈 |

```
[TX 보드] ──SPI──> [03_TX_ble (PTX)]
                        │
                  ESB RF 2.4GHz
                        │
[01_RX_control] ──SPI──> [02_RX_ble (PRX)]
```

TX 보드와 `03_TX_ble` 간 SPI는 현재 미구현 — 자세한 내용은 4.3.

---

## 3. 통신 아키텍처

### 3.1 SPI (STM32 ↔ 02_RX_ble)

- 주기: 10ms cyclic
- 속도: 9.0 Mbps
- 마스터: STM32 (`01_RX_control`)
- **wire 포맷**: 11B 고정 (HDR 1B + Length 0x08 + Data[8] + CRC 1B)
  - STM32 → nRF: 0x50 / 0x51 / 0x52 (RX 상태·센싱)
  - nRF → STM32: 0x10 / 0x11 / 0x12 (TX 상태·센싱)
- **내부 데이터 컨테이너** (wire 포맷 아님): `rx_module_data_t` 56B, `tx_module_data_t` 45B (`oled_tv_protocol.h`)

### 3.2 ESB (02_RX_ble ↔ 03_TX_ble)

- 주기: 10ms
- 패킷 크기: 11B (HDR + LEN + DATA[8] + CRC)
- 전송 개시: `03_TX_ble` (PTX)
- ACK 방식: ACK with payload — PRX가 ACK에 RX측 데이터 탑재
- HDR round-robin 3종:
  - TX측 (PTX→PRX): TX_STATUS `0x10` / TX_INPUT `0x11` / TX_OUTPUT `0x12`
  - RX측 (PRX 응답): RX_STATUS `0x50` / RX_INPUT `0x51` / RX_OUTPUT `0x52`
- 설정: `NRF_ESB_MAX_PAYLOAD_LENGTH = 64` (기본값 32에서 확장)

---

## 4. 펌웨어 현황

### 4.1 01_RX_control (STM32F103)

#### 구현됨

- PWM 4채널 (TIM8 / TIM3)
- ADC 6채널 DMA circular
- SPI2 DMA Master
- UART 명령 인터페이스
- Trip zone (TIM8 BKIN)
- Fault Reset GPIO

#### 미구현·미완료

- ADC 물리량 변환: `adc_calc()`이 현재 0~3.3V 원시 전압을 그대로 전달. 분압비 미적용, 온도 NTC 변환 미구현.

#### 비활성 코드 (현재 미사용)

- CAN1: `#if 0` 블록으로 비활성화
- DAC: 초기화만 있고 사용 코드 없음
- TIM2/4/5: 인터럽트 핸들러 미구현

#### 확인 필요

- `[확인 필요]` PWM 주파수: `docs/RX_control_PWM_가이드.md`는 100kHz (PSC=0 / ARR=639)로 명시. 실제 `app_tim.c`는 PSC=71 / Period=999 (~1kHz). 어느 쪽이 현재 의도인지 불명확.
- `[확인 필요]` CAN1 용도 미문서화 — 어떤 외부 장치와 통신할 예정이었는지.
- `[확인 필요]` DAC 용도 미문서화.

---

### 4.2 02_RX_ble (nRF52832, ESB PRX)

#### 구현됨

- ESB PRX 기본 동작
- SPI Slave 수신/송신
- 버그 수정 완료 (코드 레벨, 최근 커밋 `89e8609`)

#### 미구현·미완료

- ESB 타임아웃 stale 마킹: `esb_recv`가 끊길 때 `tx_module.hdr=0x00`으로 표시해 STM32에 알리는 로직 없음.

#### 확인 필요

- `[확인 필요]` SPI 하드웨어 테스트 미실시 — 코드 레벨 수정은 끝났으나 STM32와의 실제 연결 검증 전.

---

### 4.3 03_TX_ble (nRF52832, ESB PTX)

#### 구현됨

- ESB PTX 기본 동작
- ACK payload 수신
- round-robin HDR 전송

#### 미구현·미완료

- TX 보드 ↔ `03_TX_ble` SPI (SPI_Loop): 현재 전체 주석 처리됨.

#### 확인 필요

- (해당 없음 — 위 미구현 항목이 명확한 작업이므로 의문점이 아님)

---

## 5. 작업 우선순위

`tasks/esb-tx/` 흐름 기준의 현재 우선순위:

1. SPI 하드웨어 테스트 (STM32 ↔ `02_RX_ble` 실제 연결)
2. ESB 링크 연결 (SPI 확인 후)
3. ESB 타임아웃 stale 마킹
4. DMA/타이머 인터럽트 우선순위 정리

---

## 6. 미해결 의문점

본문 `[확인 필요]` 마커 자리의 전체 일람.

1. **PWM 주파수**: `docs/RX_control_PWM_가이드.md` (100kHz) vs 실제 코드 `app_tim.c` (~1kHz) 불일치.
2. **ADC 물리량 변환**: 분압비/NTC 파라미터는 정의됐으나 변환 코드 미구현 — 어느 자리에서 변환할지 결정 필요.
3. **CAN1 용도**: 어떤 외부 장치와 통신하는지 미문서화.
4. **DAC 용도**: 초기화만 있고 사용처 없음.
5. **README ESB 역할 오표기**: README는 `02=PTX, 03=PRX`로 적혀 있으나 코드 진실은 반대 (`02=PRX, 03=PTX`). README 수정 필요.
6. **SPI 하드웨어 테스트**: `02_RX_ble` 코드 수정 후 실측 검증 전 상태.
