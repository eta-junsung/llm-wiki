---
date: 2026-05-29
---

# lp-am263p — 구현 현황

> 전략 spine은 [[roadmap]], 확정 사실/폐기 가설은 [[flash_open_facts]], 라운드별 진단 history는 [[flash_open_diagnostic_log]].

## 다음 시작점

**R28** — `cc3351/main.c`의 R27 블록을 jtag_flasher 성공 공식으로 교체: `skipHwInit=FALSE` 복귀 + `flashFixUpOspiBoot()` 인라인 재현(`board_flash_reset` → `OSPI_enableSDR` → `OSPI_clearDualOpCodeMode` → `OSPI_setProtocol(1,1,1,0)`) → 이후 `Flash_open`의 `set888mode(0x81)`이 1S→8D 승격.
**선행 확인**: cc3351 `example.syscfg`에 OSPI reset 핀 설정 유무를 jtag_flasher `example.syscfg`와 비교 — `board_flash_reset()`이 생성 코드에 없으면 `OSPI_setResetPinStatus` 직접 호출로 대체 가능한지 확인.
**성공 기준**: `[DIAG] R28: Flash_open OK`, `gFlashHandle[0] != NULL`.

## 구현 현황

| 기능 | 상태 | 메모 |
|------|------|------|
| S0 AM263P 마이그레이션 | ✓ | `--device AM263Px` 빌드 성공 |
| S1 MCELF 빌드 + JTAG 플래시 | ✓ | jtag_flasher 6작업 전부 성공 (R10) |
| S2 부팅 + UART 진단 마커 | ✓ | `[DIAG] A..G` 출력 |
| S3 app `Flash_open()` 유효 핸들 | ✗ | NULL 반환, SetRdCap FAILURE. R27째 미해소. DQ1-only 패턴 |
| S4 Drivers_open / Board_open 완주 | ✗ | S3의 2차 결과로 실패 |
| S5 CC33xx FW 로드 + NP 기동 | ? | 미도달 |
| S6 SPI/IRQ link-up | ? | 미도달 |
| S7 network_terminal CLI | ? | 미도달 |
| S8 BLE HCI 경로 | ? | 미도달 |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현

## 미결 사항

- cc3351 `example.syscfg`에 OSPI reset 핀 설정 부재 — R28 선행 확인.
- DQ1-only 원인 미확정 — 진짜 8D PHY 문제인가 vs Quad 상태 잔상인가.
- SBL이 SW1="OSPI 4S Quad(1,1,1,1)" 부팅 시 chip을 어느 프로토콜로 app에 넘기는가 (SBL 소스 또는 TRM OSPI boot 절차 확인).
- BoosterPack 헤더(J1~J4) ↔ SoC 핀 물리 대응표 미확인.
