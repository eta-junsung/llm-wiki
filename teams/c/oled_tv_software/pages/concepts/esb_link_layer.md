---
tags: [concept, protocol, esb]
source: teams/c/oled_tv_software/raw/prd_v1.0.md
date: 2026-05-26
subsystem: 02_RX_ble, 03_TX_ble
---

# ESB 링크 레이어

[[tx_ble_module]](PTX) ↔ [[rx_ble_module]](PRX) 간 ESB RF 링크 파라미터. 패킷 내용은 [[esb_packet_format]] 참조.

## 링크 파라미터

| 항목 | 값 |
|---|---|
| 전송 개시 | PTX (`03_TX_ble`) |
| 주기 | 10 ms |
| 패킷 크기 | 11 B (HDR + LEN + DATA[8] + CRC) |
| ACK 방식 | ACK with payload |
| `NRF_ESB_MAX_PAYLOAD_LENGTH` | 64 (SDK 기본 32에서 확장) |

## ACK with payload 동작

PTX가 ESB 패킷(0x10/0x11/0x12 라운드로빈)을 송신하면, PRX가 ACK 패킷에 RX측 데이터(0x50/0x51/0x52 라운드로빈)를 탑재해 응답한다. PRX는 ACK FIFO에 다음 패킷을 미리 적재해두고 PTX의 송신 타이밍에 piggyback되어 전달된다.

RX→TX 방향 전송 주기는 PTX 송신 주기(10ms)에 종속된다.

## 미결 파라미터

아래 항목은 PRD 작성 시점 기준 미문서화. ESB SDK 설정 또는 추가 코드 확인 필요.

- 무선 채널 번호
- ESB 주소
- bitrate (1Mbps / 2Mbps)
- ACK retry 횟수 / 간격

## 출처

- [[prd]] (§3.2)
