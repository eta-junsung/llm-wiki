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

## 관련

- [[nrf52_module_naming]] — `eta_` 접두사 규칙 전문
- [[ses_build_conventions]] — SES emProject 빌드 함정
- [[comm_state_monitoring]] — 모니터링 채널 분리(01 바이너리 vs 02 텍스트)
- [[rx_ble_module]] — 02_RX_ble entity
- [[tx_ble_module]] — 03_TX_ble entity
