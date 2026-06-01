---
tags: [source, spi, diagnosis, esb]
source: direct session report
date: 2026-06-01
subsystem: 01_RX_control, 02_RX_ble
---

# SPI 10ms 폴링 진단 보고서 (260601)

[[spi_heartbeat_report_260529]]이 "미달"로 남긴 "SPI 10ms 폴링 미동작" 문제의 원인 진단 세션. 결론: **동작 결함 아님 — 관측 도구 한계**.

## 파생 페이지

- [[spi_link_reliability]] — "미달 — SPI 10ms 폴링 ✗" → "✓ 실보드 검증 완료"로 갱신

## 진단 경과

### 가설 1 반증: HAL_SPI_MspInit DMA IRQ NVIC 누락

[[spi_heartbeat_report_260529]]의 "다음 시작점"이 지목한 가설. 코드 확인 결과 **반증**:

- NVIC enable은 `MX_DMA_Init()`(`01_RX_control/app_dma.c:15-19`)에 정상 존재
- IRQ 핸들러 `stm32f1xx_it.c:227-250`에 정상 연결
- `MspInit`에 없는 것은 사실이나, NVIC enable이 `MX_DMA_Init`에 있으므로 "누락"이 아님 — 위치 오인이 누락 오판으로 이어진 것

### 가설 2 반증: PACKET_INTERVAL 미변경

코드 확인 결과 **반증**: `PACKET_INTERVAL=10`(`_shared/oled_tv_protocol.h:45`)은 이미 설정됨. `spi_proc()`(`01_RX_control/Application/Src/common.c:186`)이 사용 중.

### 가설 3 반증: SPI Mode/Clock 불일치

| 항목 | STM32 | nRF52832 |
|---|---|---|
| SPI 모드 | MODE_2 (CPOL=1/CPHA=0) `app_spi.c:24-25` | `NRF_SPIS_MODE_2` `main.c:626` |
| SCK | APB1 36MHz / Prescaler8 = **4.5MHz** | 슬레이브 한계 ~8Mbps |

불일치 없음 — **반증**.

### 진단 병목 해소: 관측 도구 한계

기존 `rx_status.spi_status` 단일 필드는 매 수신마다 덮어써지므로 산발 패턴·주기를 관측 불가. 이것이 "미동작"처럼 보인 근원.

**해소**: `common.c:165-185`에 누적 카운터(`spi_ok_cnt` / `spi_crc_fail_cnt`, CRC 이벤트 기반, timeout fail 제외) 추가. `Monitor_Loop()` UART 출력: 누적 + 초당 delta + failrate%.

## 실보드 검증 결과

**UART 출력 (49s)**:
```
spi | ok=4799 crcfail=0 | /s ok=100 crcfail=0 failrate=0%
```
→ 초당 100 트랜잭션 = 평균 10ms 주기. CRC fail 0건 = 통신 100% 정상.

**오실로스코프** (Keysight [[instruments]], RTM3004, C1):
- CS(STM32 PB12) active-low Δt=10ms, 1/Δt=100Hz
- Vpp=3.79V, RMS=3.36V
- 캡처: `assets/spi_cs_10ms_260601.png` (원본: `projects/c/oled_tv_software/P3NOFO01.PNG`)

UART + 오실로 교차 검증 완료. **SPI 10ms 폴링은 처음부터 정상 동작 중이었다.**

## 핵심 참조 (file:line)

| 항목 | 위치 |
|---|---|
| PACKET_INTERVAL=10 | `_shared/oled_tv_protocol.h:45` |
| SPI 패킷 길이 (SPI_PKT_TOTAL_LEN=11) | `_shared/oled_tv_protocol.h:247` |
| STM32 SPI Mode/Prescaler | `app_spi.c:24-27` |
| STM32 NSS_SOFT | `app_spi.c:26` |
| CS 수동 토글 | `app_spi.c:134/142` |
| DMA NVIC enable | `app_dma.c:15-19` |
| CRC 판정 + 카운터 | `common.c:165-185` |
| CS 핀 정의 (PB12) | `Core/Inc/main.h:100` |
| nRF52832 SPIS 모드 | `02_RX_ble/Application/main.c:626` |
| nRF52832 SPI_Loop 재장전 | `02_RX_ble/Application/main.c:558-586` |
