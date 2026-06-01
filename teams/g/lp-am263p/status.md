---
date: 2026-06-01
---

# lp-am263p — 구현 현황

> 전략 spine(S0~S8)은 [[porting]], 프로젝트 호는 [[roadmap]], 확정 사실/폐기 가설은 [[flash_open_facts]], 라운드별 진단 history는 [[flash_open_diagnostic_log]].

## 다음 시작점

R35 — WLAN_EN(ball M15→J1.5→BP P1.5 LP_RESET, active-low) reset 해제 검증: `wlan_irq_adapt.c wlan_TurnOnWlan` 폴리시(Low→High)·타이밍·GPIO 출력값 확인.

## 구현 현황

| 기능 | 상태 | 메모 |
|------|------|------|
| S0 AM263P 마이그레이션 | ✓ | `--device AM263Px` 빌드 성공 |
| S1 MCELF 빌드 + JTAG 플래시 | ✓ | jtag_flasher 6작업 전부 성공 (R10) |
| S2 부팅 + UART 진단 마커 | ✓ | `[DIAG] A..G` 출력 |
| S3 app `Flash_open()` 유효 핸들 | ✓ | pinmux `$assign` 교정으로 R28b 통과. RDID=`9D 5A 19` |
| S4 Drivers_open / Board_open 완주 | ✓ | R31 통과. 표준 Board_flashOpen 단독 동작 실측 검증 |
| S5 CC33xx FW 로드 + NP 기동 | △ | `Hardware init DONE!` 도달(R32). MISO D1 교정(R34)으로 비-0 전환 — NP WSPI 핸드셰이크 미완 |
| S6 SPI/IRQ link-up | ✗ | `SPI not responsive` (R32). MISO 살아남(R34). NP reset/기동 미검증 |
| S7 network_terminal CLI | ✗ | S6의 2차 결과 |
| S8 BLE HCI 경로 | ? | 미도달 |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현

## 미결 사항

- **NP reset/기동 미검증** — WLAN_EN(M15→J1.5→BP P1.5 LP_RESET, active-low) 해제 폴리시/타이밍 확인 필요.
- MOSI(C10/J2.15)·CLK(A11/J1.7) NP 물리 도달 미확인 — scope/LA(사용자 손).
- flash FS 쓰기 미검증 — `osi_filesystem.c:131` "Skip flash writing due to APIs issue".
- [H-A] skipHwInit=TRUE 최소 충분 패치셋 미분리 — quirksFxn/skipHwInit/dummyClksCmd 중 필수 조합 미확인.
