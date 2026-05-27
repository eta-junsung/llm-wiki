---
tags: [source, uart, command, rx_control]
source: projects/c/oled_tv_software/docs/매뉴얼 (Uart Commands)_테스트용.pdf
date: 2026-05-27
subsystem: 01_RX_control
---

# UART5 Command Reference — 테스트용 매뉴얼

RX Control 보드의 UART5 명령어 공식 레퍼런스. 이미지형 PDF(6p), PNG 변환 후 ingest.

- 제품: **Eta Electronics Inc. · OLED700 WPT · Ver 0.1E00**
- MCU: PDF에 STM32F103VCT6로 기재되어 있으나 실제는 **STM32F103RCT6** (문서 오기)
- UART5: TX=PC12, RX=PD2, 115200/8N1

## 문서 구성

| 페이지 | 내용 |
|---|---|
| 1 | 개요 — 핀/속도/명령 목록 |
| 2 | `duty` — 동시 형식 A + 개별 채널 형식 B |
| 3 | `freq` + `dt` |
| 4 | `phase` + `start` + `reset` + TIM8_BRK 경보 |
| 5 | PWM 채널 매핑 + dt_ratio 동작 요약 + GPIO/SPI 핀 + BLE-SPI 패킷 구조 |
| 6 | Quick Reference (전 명령 일람) |

## 파생 페이지

- [[uart_command_set]] — 명령어 전체 (이 소스로 대폭 갱신)
- [[dead_time]] — dt_ratio 개념 + `dt` 구문 변경 반영
- [[rx_control]] — UART5 핀 추가 (MCU는 RCT6 유지, PDF의 VCT6 표기는 오기)
- [[spi_packet_format]] — p.5 BLE-SPI 패킷 구조 (historical, 기존 내용과 일치 확인)

## 원본 위치

```
C:\Users\echog\eta\projects\c\oled_tv_software\docs\매뉴얼 (Uart Commands)_테스트용.pdf
```

이미지형 PDF라 raw/ 텍스트 복사본 없음 — Poppler pdftoppm으로 PNG 변환해 읽음.
