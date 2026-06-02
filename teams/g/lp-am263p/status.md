---
date: 2026-06-03
---

# lp-am263p — 구현 현황

> 전략 spine(S0~S8)은 [[porting]], 프로젝트 호는 [[roadmap]], 확정 사실/폐기 가설은 [[flash_open_facts]], 라운드별 진단 history는 [[flash_open_diagnostic_log]].

## 다음 시작점

R37 — Saleae ≥50 MS/s + CS 트리거로 ~16 MHz SCLK 물리 핀 도달 확정 + NP 비응답 원인(WLAN_IRQ 발생 여부 / 2nd-loader 다운로드 완료 / LP_RESET→WLAN_IRQ 타이밍) 조사.

## 구현 현황

| 기능 | 상태 | 메모 |
|------|------|------|
| S0 AM263P 마이그레이션 | ✓ | `--device AM263Px` 빌드 성공 |
| S1 MCELF 빌드 + JTAG 플래시 | ✓ | jtag_flasher 6작업 전부 성공 (R10) |
| S2 부팅 + UART 진단 마커 | ✓ | `[DIAG] A..G` 출력 |
| S3 app `Flash_open()` 유효 핸들 | ✓ | pinmux `$assign` 교정으로 R28b 통과. RDID=`9D 5A 19` |
| S4 Drivers_open / Board_open 완주 | ✓ | R31 통과. 표준 Board_flashOpen 단독 동작 실측 검증 |
| S5 CC33xx FW 로드 + NP 기동 | △ | `Hardware init DONE!` 도달(R32). MCSPI 정상(R36: 8회 ALL_SUCCESS, SCLK~16 MHz). NP 비응답 — NP 부팅/2nd-loader 미완 추정 |
| S6 SPI/IRQ link-up | ✗ | NP SPI 비응답 — MISO rd#0/1=0xFFFFFFFF·rd#2~7=0x0. `SPI not responsive/CMD_ERR_TIMEOUT`. WLAN_IRQ 미발생 |
| S7 network_terminal CLI | ✗ | S6의 2차 결과 |
| S8 BLE HCI 경로 | ? | 미도달 |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현

## 미결 사항

- **NP(CC33xx) 비응답 원인 미확인** — MCSPI 정상 확정(R36). NP 부팅 시퀀스(LP_RESET 해제→2nd-loader 다운로드→WLAN_IRQ 발생) 완료 여부 미확인. Saleae ≥50 MS/s SCLK 물리 확정도 미완.
- **Saleae SCLK 물리 확정 미완** — R35 12.5 MS/s 캡처는 16 MHz에 샘플링 부족. ≥50 MS/s 재캡처 필요.
- flash FS 쓰기 미검증 — `osi_filesystem.c:131` "Skip flash writing due to APIs issue".
- [H-A] skipHwInit=TRUE 최소 충분 패치셋 미분리 — quirksFxn/skipHwInit/dummyClksCmd 중 필수 조합 미확인.
