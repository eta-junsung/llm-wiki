---
tags: [concept, esb, ptx, ack_payload, architecture]
source: teams/c/oled_tv_software/pages/sources/spi_debug_log_report_260529.md
date: 2026-05-29
subsystem: 03_TX_ble
---

# ESB PTX ACK Payload 재조립

PTX 모드([[tx_ble_module]])에서 RX 데이터를 완전히 수집하기 위한 헤더별 버퍼 패턴.

## 문제: PTX에서 rx_module이 자동으로 채워지지 않는다

ESB PRX 모드([[rx_ble_module]])에서는 `NRF_ESB_EVENT_RX_RECEIVED`가 발생해 수신 데이터를 직접 처리할 수 있다. 반면 PTX 모드에서는 이 이벤트가 발생하지 않는다 — RX 데이터는 ACK payload에 piggyback되어 `NRF_ESB_EVENT_TX_SUCCESS`에서만 꺼낼 수 있다.

결과: `rx_module_data_t`(54B) 전체를 PTX에서 직접 채울 수 없다. ACK 한 번에 11B([[esb_packet_format]])만 들어오고, RX 측이 0x50→0x51→0x52 round-robin으로 1헤더씩 보내기 때문이다.

## 해법: g_last_ack_by_hdr[3]

`03_TX_ble/Application/main.c:518-540`

```c
// NRF_ESB_EVENT_TX_SUCCESS ISR 내
g_last_ack = ack_payload;  // [:628] — 가장 최근 ACK 11B 보관

// ESB_Loop() 에서
switch (g_last_ack.data[0]) {   // HDR byte
    case 0x50: g_last_ack_by_hdr[0] = g_last_ack; break;
    case 0x51: g_last_ack_by_hdr[1] = g_last_ack; break;
    case 0x52: g_last_ack_by_hdr[2] = g_last_ack; break;
}
g_rx_seen_mask |= (1 << slot);  // 수신 확인 비트 세팅
```

단일 `g_last_ack`만 사용하면 가장 최근 헤더 외 나머지 두 헤더 데이터가 Monitor 출력 시 손실된다. 슬롯 3개로 나눠 보관하면 1초 윈도우(ESB 30ms 주기 × ~33 cycle) 안에 세 헤더를 모두 수집할 수 있다.

## Monitor_Loop 출력 윈도우

`03_TX_ble/Application/main.c:568-614`, 1000ms 주기

- `g_rx_seen_mask` 비트가 선 헤더만 출력 — 초기 0값 방지
- 출력 후 `g_rx_seen_mask = 0` 리셋 (1초 단위 갱신)

출력 예시:
```
ESB tx=0x000C3E fail=0/s | ACK rx=0x000C3D [0x50 0x51 0x52]
[eta-rx]
0x50 | Rx_Fault_St=0 Rx_Warning_St=0 Rx_Sys_Rdy_St=1 Rx_Buck_St=1 fw=0.1
0x51 | Rx_Vrect=48.00V Rx_Irect=1.23A
0x52 | Rx_Vout=12.00V Rx_Iout=2.34A Rx_T1=45.0C Rx_T2=46.0C
```

## ISR 안전 패턴: printf 금지

ESB 이벤트 핸들러(`esb_event_handler`)는 ISR 컨텍스트다. 블로킹 UART TX(printf)를 ISR 내에서 호출하면 HardFault가 발생한다.

올바른 패턴:
```c
// ISR: 원자 카운터만 갱신
nrf_atomic_u32_add(&esb_tx_fail_cnt, 1);

// Monitor_Loop: 안전하게 읽어 printf
uint32_t cnt = nrf_atomic_u32_fetch_store(&esb_tx_fail_cnt, 0);
printf("fail=%u/s", cnt);
```

## 관련 페이지

- [[esb_packet_format]] — 11B wire 포맷
- [[rx_to_tx_packets]] — 0x50/0x51/0x52 페이로드 정의 + 코드 실측 레이아웃
- [[tx_ble_module]] — PTX 엔티티
- [[rx_ble_module]] — PRX 엔티티 (round-robin 송신 측)
