---
tags: [concept, firmware, nrf52, convention, isr]
source: 02_RX_ble 정리 b92835c→e85839c (2026-06-11, 빌드·실보드 검증 완료)
date: 2026-06-11
subsystem: 02_RX_ble, 03_TX_ble
---

# nRF52 펌웨어 코딩 관습

02_RX_ble 정리 라운드(b92835c→e85839c)에서 확정된 관습. 03_TX_ble에도 적용 예정.

## ISR에서 printf 금지 — HardFault 실증

`esb_event_handler`·`spis_event_handler` 등 ISR 내부에서 printf(UART 송출)를 호출하면 **HardFault** 발생. b92835c 이전 실제로 발생 확인됨.

ISR 안에서 허용:
- 플래그·카운터 갱신
- `memcpy`로 버퍼 복사

→ 이벤트 발생 시 플래그를 세우고, 메인 루프(`while(1)` 또는 `Monitor_Loop`)에서 소비한다.

## 오류 카운터 패턴 — inline printf 대신 1초 윈도우 1줄

평시에도 흔히 발생하는 오류(예: ESB ACK 큐 풀)는 발생 즉시 printf하지 않는다. 카운터로 누적하고 `Monitor_Loop` 1초 윈도우 출력 블록 **끝에 append**한다.

```c
// 나쁜 예 — 빈번 경로 inline printf
nrf_esb_flush_tx();
printf("ESB ACK queue full\r\n");

// 좋은 예 — 카운터 + Monitor 1줄 append
g_esb_tx_full_cnt++;   // ISR-safe (플래그·카운터만)
// Monitor_Loop 1초 윈도우:
printf("...(기타) | tx_full=%u\r\n", g_esb_tx_full_cnt);
g_esb_tx_full_cnt = 0;
```

모니터 데이터 라인 **사이에 끼워넣지 않는다** — 파싱 가독성 유지.

## init/배너 printf 금지

초기화 단계의 "SPI init done"·"ESB init OK"·"Hello" 등 디버그 printf는 두지 않는다. 초기화 완료는 LED1 상시 점등으로 확인한다.

근거: init printf는 GUI 파서와 사람 모니터 어느 쪽에도 유용하지 않고, 시작 직후 UART 버퍼를 오염시킨다([[comm_state_monitoring]] "모니터링 채널 분리").

## 모듈 접두사 — `eta_`

로컬 모듈은 `eta_` 접두사. 규칙 전문 → [[nrf52_module_naming]].

## NRF_LOG / SEGGER_RTT 초기화 잔재 — 무해·인지 필요

02_RX_ble 기준, NRF_LOG/SEGGER_RTT 인프라가 `sdk_config.h` + `main.c` init 코드 수준에서만 존재하고 실제 호출은 **0건**이다. SDK 프로젝트 템플릿의 잔재 — 무해하게 남아 있다.

`NRF_LOG_INIT` 호출이 보인다고 해서 로그 출력이 어딘가 나간다는 의미가 아니다. 활성화된 출력 채널은 01 UART5 바이너리([[pc_uart_gui]])와 02 텍스트 모니터([[comm_state_monitoring]] "모니터링 채널 분리") 뿐이다.

## 모듈 의존 방향 — protocol → {esb, spi, clock, gpio} 단방향

응용 계층 `eta_protocol`이 저수준 드라이버를 호출한다. 역방향 호출 금지.

```
eta_protocol
    ↓
eta_esb / eta_spi / eta_clock / eta_gpio
```

이 방향이 깨지면 순환 의존이 발생한다. 02/03 모두 이 구조를 준수한다.

## Monitor 1초 윈도우 — baseline-delta, unsigned wrap 무해

`Monitor_Loop`가 1초마다 1줄 진단을 출력한다. 카운터는 **누적 전역**(리셋 없음)을 두고, 출력은 **윈도우 delta**로 표시한다:

```c
uint32_t g_esb_rx_cnt;          // 누적 전역
static uint32_t baseline = 0;
uint32_t delta = g_esb_rx_cnt - baseline;   // unsigned 뺄셈
baseline = g_esb_rx_cnt;
printf("rx=%u/s ...\r\n", delta);
```

`uint32_t` overflow 시 wrap해도 unsigned 뺄셈이라 delta는 정확하다 — millis rollover와 같은 패턴.

## ESB health 판정 독립성

02(`esb_rx_cnt` delta)·03(`esb_ack_cnt` delta)이 각자 `BLE_COMM_ST_WINDOW_MS` 윈도우로 **독립 판정**한다. 판정 결과를 상대방에게 보내지 않는다 — RF 상태는 직접 받는 노드만 안다는 설계 원칙. 임계·메커니즘 전문 → [[comm_state_monitoring]].

## 관련

- [[nrf52_module_naming]] — `eta_` 접두사 규칙 전문
- [[ses_build_conventions]] — SES emProject 빌드 함정
- [[comm_state_monitoring]] — 모니터링 채널 분리(01 바이너리 vs 02 텍스트)
- [[rx_ble_module]] — 02_RX_ble entity
- [[tx_ble_module]] — 03_TX_ble entity
