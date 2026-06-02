---
date: 2026-06-03
---

# lp-am263p — 구현 현황

> 전략 spine(S0~S8)은 [[porting]], 프로젝트 호는 [[roadmap]], 확정 사실/폐기 가설은 [[flash_open_facts]], 라운드별 진단 history는 [[flash_open_diagnostic_log]].

## 다음 시작점

R37 — NP(CC33xx) 비응답 원인 규명: ① NP 부팅 시퀀스(`HINT_ROM_LOADER_INIT_COMPLETE` / `Init device FAILED` 경로, WLAN_EN 타이밍·LP_RESET 순서, 2nd-loader 다운로드 위치) ② CS 프레이밍(`csDisable=FALSE` 연속 assert vs CC33xx SDK 워드별 deassert 기대) 정합 확인. Saleae MISO/IRQ 변화가 검증 기준.

## 구현 현황

| 기능 | 상태 | 메모 |
|------|------|------|
| S0 AM263P 마이그레이션 | ✓ | `--device AM263Px` 빌드 성공 |
| S1 MCELF 빌드 + JTAG 플래시 | ✓ | jtag_flasher 6작업 전부 성공 (R10) |
| S2 부팅 + UART 진단 마커 | ✓ | `[DIAG] A..G` 출력 |
| S3 app `Flash_open()` 유효 핸들 | ✓ | pinmux `$assign` 교정으로 R28b 통과. RDID=`9D 5A 19` |
| S4 Drivers_open / Board_open 완주 | ✓ | R31 통과. 표준 Board_flashOpen 단독 동작 실측 검증 |
| S5 CC33xx FW 로드 + NP 기동 | △ | `Hardware init DONE!` 도달(R32). MCSPI 정상·SCLK~16 MHz 물리 확정(R36). NP 부팅/2nd-loader 완료 여부 미확인 |
| S6 SPI/IRQ link-up | ✗ | MISO flat·WLAN_IRQ flat(R36 Saleae). `SPI not responsive/CMD_ERR_TIMEOUT`. CS 프레이밍 정합 미확인 |
| S7 network_terminal CLI | ✗ | S6의 2차 결과 |
| S8 BLE HCI 경로 | ? | 미도달 |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현

## 미결 사항

- **NP(CC33xx) 비응답 원인 미확인** — MCSPI 정상·SCLK 물리 확정(R36). MISO(P2.14)·WLAN_IRQ(P1.8) flat 확인. NP 부팅 시퀀스(2nd-loader 다운로드·HINT_ROM_LOADER_INIT_COMPLETE) 완료 여부 미확인.
- **CS 프레이밍 정합 미확인** — `csDisable=FALSE`(연속 assert) vs CC33xx SDK 워드별 deassert 기대 여부 미검증.
- flash FS 쓰기 미검증 — `osi_filesystem.c:131` "Skip flash writing due to APIs issue".
- [H-A] skipHwInit=TRUE 최소 충분 패치셋 미분리 — quirksFxn/skipHwInit/dummyClksCmd 중 필수 조합 미확인.
