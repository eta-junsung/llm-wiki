---
tags: [source, debug, esb, spi, rx_to_tx]
source: tasks/spi-debug-log/report.md
date: 2026-05-29
subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
---

# SPI 디버그 로그 검증 결과 (시나리오 A/B)

양방향 ESB 데이터 경로 무결성을 코드 기반으로 분석하고 검증 기준을 확립한 리포트. 두 시나리오로 TX→RX→TX ACK 경로를 검증한다.

## 파생 페이지

- [[rx_to_tx_packets]] — 0x50/0x51/0x52 코드 실측 레이아웃 및 프로토콜 매뉴얼과의 불일치 추가
- [[esb_ptx_ack_assembly]] — PTX 모드 ACK payload 재조립 패턴 (신규)
- [[tx_ble_module]] — Monitor_Loop 출력 포맷 + ISR 안전 패턴 추가

## 시나리오 A: TX_ble 더미 → STM32 Monitor_Loop

```
build_tx_pkt()  [03_TX_ble/Application/main.c:227]
  → nrf_esb_write_payload()  [ESB_Loop():557]
  → RX_ble esb_event_handler() NRF_ESB_EVENT_RX_RECEIVED  [02_RX_ble/Application/main.c:446]
  → apply_spi_rx_pkt()  [SPI_Loop():560]
  → build_rx_pkt(&pkt, rx_rr) → nrf_esb_write_payload(&ack_payload)  [ESB_Loop():522-530]
  → TX_ble NRF_ESB_EVENT_TX_SUCCESS → g_last_ack  [03_TX_ble/Application/main.c:621-628]
  → g_last_ack_by_hdr[] 갱신  [ESB_Loop():518-540]
  → Monitor_Loop() [eta-rx] 출력  [:568-614]
```

## 시나리오 B: RX_control 더미 → TX_ble Monitor_Loop

```
adc_calc()  [01_RX_control/Application/Src/common.c:202]
  → spi_proc() 1000ms 주기  [:186]
  → build_rx_to_tx_pkt()  [:190]
      → inject_rx_dummy_data()  [:63]  ← rx_module.rx_data 덮어씀
      → memset + 직렬화
  → spi_txrx_dma()  [:193]  (STM32 → RX_ble SPI)
  → RX_ble SPI_Loop() apply_spi_rx_pkt()  [02_RX_ble/Application/main.c:560]
  → build_rx_pkt() → ESB ACK 조립
  → TX_ble g_last_ack_by_hdr[]  [03_TX_ble/Application/main.c:518-540]
  → Monitor_Loop() [eta-rx] 출력  [:568-614]
```

## inject_rx_dummy_data 주입 위치 제약

`01_RX_control/Application/Src/common.c:51-59`

```c
static void inject_rx_dummy_data(void) {
    rx_module.rx_data.vrect       = 48.0f;
    rx_module.rx_data.irect       = 1.23f;
    rx_module.rx_data.vout        = 12.0f;
    rx_module.rx_data.iout        = 2.34f;
    rx_module.rx_data.stack_temp1 = 45.0f;
    rx_module.rx_data.stack_temp2 = 46.0f;
}
```

**안전한 주입 위치**: `build_rx_to_tx_pkt()` 진입부(직렬화 직전). `adc_calc()`보다 앞에 넣으면 실측값으로 덮인다 — `adc_calc()`는 ADC 완료 플래그 기반으로 비결정적 타이밍에 `rx_module.rx_data`를 갱신하기 때문. `spi_proc`는 `adc_proc` 이후에만 호출되므로 `build_rx_to_tx_pkt()` 내에서의 주입은 항상 와이어에 실린다.

## 완료 기준

- TX_ble UART/RTT에 `[eta-rx]` 1초 주기 안정 출력
- `Rx_Vrect=48.00V`, `Rx_Vout=12.00V` 더미값 스케일 정확 표시
- UART FIFO/HardFault 없이 ≥ 30초 연속 유지
- 시나리오 A의 STM32 Monitor 출력이 동시에 살아 있음

## Scope 밖 미결 사항

| 항목 | 비고 |
|---|---|
| `PACKET_INTERVAL=1000ms`(코드) vs "10ms cyclic"(wiki) 불일치 | ESB RF 전송 주기(10ms)와 애플리케이션 데이터 갱신 주기(1000ms) 구분 필요 |
| ESB CRC 강화 (현재 1B XOR) | |
| `spi_wr_u16` / `esb_wr_u16` 중복 정리 | |
| `inject_rx_dummy_data` `#ifdef DEBUG_DUMMY` 정책 | 영구 유지 vs 검증 후 제거 |
