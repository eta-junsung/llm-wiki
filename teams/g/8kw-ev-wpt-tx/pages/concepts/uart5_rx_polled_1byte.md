---
tags: [concept, uart5, am263p, sdk-gotcha, 8kw-ev-wpt-tx]
source: 실보드 디버그 (2026-06-16, branch gpio UART5 RX 파서 검증)
date: 2026-06-16
---

# UART5 RX POLLED 모드 — 1바이트씩 read 필수

> **SDK 함정.** AM263Px SDK의 `UART_read()`를 `POLLED + SystemP_NO_WAIT + UART_READ_RETURN_MODE_FULL` 조합으로 쓰면 `rx.count`가 앱 transaction에 반영되지 않아 stale 버퍼가 매 루프 주입된다.

---

## 증상

```c
UART_Transaction rx;
UART_Transaction_init(&rx);
rx.count = 8;                               // 8바이트 요청
rx.timeout  = SystemP_NO_WAIT;
rx.readMode = UART_READ_RETURN_MODE_FULL;
UART_read(gUart5Handle, buf, &rx);

if (rx.count > 0U) {                        // 항상 true — 버그 경로
    // stale 0x00 버퍼를 staging에 주입 → SOF(0xA5) 탐색 불가
}
```

- SDK 내부 lld 구조체에는 실제 수신 바이트 수를 기록하지만 **앱 `UART_Transaction`의 `count` 필드에는 반영하지 않음**.
- `count`가 요청값(8) 그대로 남아 `if (rx.count > 0U)`가 항상 true.
- 결과: 수신 없어도 stale `0x00` 버퍼가 매 루프 staging에 주입 → SOF(`0xA5`) 탐색 불가.

---

## 수정

```c
UART_Transaction rx;
UART_Transaction_init(&rx);
rx.count    = 1;                            // 1바이트씩 read
rx.timeout  = SystemP_NO_WAIT;
rx.readMode = UART_READ_RETURN_MODE_FULL;

uint8_t byte;
int32_t ret = UART_read(gUart5Handle, &byte, &rx);
if (ret == SystemP_SUCCESS) {               // count 값 무시, 반환값으로 판단
    // staging에 적재
}
```

- `rx.count = 1`로 **1바이트씩** read.
- `UART_read()` **반환값 `== SystemP_SUCCESS`** 를 조건으로 — count에 의존하지 않음.
- SOF 탐색은 staging 버퍼에서 수행하므로 1바이트씩 쌓아도 프레이밍 로직에 영향 없음.

---

## 영향 범위

| 경로 | 영향 |
|------|------|
| RX POLLED + NO_WAIT + FULL | 버그 경로 — 1바이트 fix 적용 |
| TX (`UART_write`, RTI ISR 경유) | 무영향 — 별도 write transaction |

---

## 관련

- [[uart5_packet_protocol]] — TYPE=0x10 RX 파서가 이 패턴을 사용
- [[gpio_impl]] — 파서 수신 후 `eta_gpio_request_gd_en()` 호출 흐름
