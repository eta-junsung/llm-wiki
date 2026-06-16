---
tags: [entity, gpio, 8kw-ev-wpt-tx, pinmap]
source: 사용자 제공 (2026-06-16) — 회로도 전체 미ingest, 해당 신호 핀만 발췌. LP-AM263P UG Table 2-30 GPIO 번호 교차확인.
date: 2026-06-16
---

# gpio_pinmap — 8kW WPT TX 보드 GPIO 핀맵

> eta 보드 → LP-AM263P GPIO 출력 신호 대응표.
> 작업 호는 [[gpio]], 프로젝트 현재 위치는 [[status]].

---

## 핀맵 — GPIO 출력

| 신호명 | 기능 | 커넥터 핀 | GPIO 번호 | 초기값 | 근거 |
|--------|------|-----------|-----------|--------|------|
| 485_EN | RS-485 트랜시버(THVD1400 U13) DE 핀 — HIGH=TX enable, LOW=RX(default) | J5.48 | **GPIO91** | LOW | 사용자 제공 + wiki [[lp_am263p_uart_epwm_mux]] |
| GD_EN_seed | 게이트 드라이버 enable — HIGH=enable | J4.33 | **GPIO93** | LOW | 사용자 제공 + [[lp_am263p_ug]] Table 2-30 `ug:1594` |

### 근거 — J4.33 = GPIO93

UG Table 2-30 (`ug:1594`):

```
|J4.33|PR0_PRU0_GPIO0||RMII2_RXD0|RGMII2_RD0|MII2_RXD0|EPWM25_A||GPIO93|||EPWM25_A|
```

Mode 8 = GPIO93. 사용자 회로도 net명 `GD_EN_seed`.

---

## 미확인

- **GD_EN_seed 극성**: active-high(HIGH=enable) 가정 — 회로도 원본으로 확인 잔여.
- **485_EN 초기값 타이밍**: UART5 TX 시작 전 HIGH 전환 시점 — eta_uart5.c 연동 시 확정.
