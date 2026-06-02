---
date: 2026-06-02
---

# lp-am263p — 구현 현황

> 전략 spine(S0~S8)은 [[porting]], 프로젝트 호는 [[roadmap]], 확정 사실/폐기 가설은 [[flash_open_facts]], 라운드별 진단 history는 [[flash_open_diagnostic_log]].

## 다음 시작점

R36 — `evaluations/spi0` 빌드가 loopback(`mcspi_loopback.c`)인지 외부핀(`mcspi_external_loopback.c`)인지 확인 후, MCSPI_transfer 실호출 여부 마커(`[R36-SPI] transfer count/ret`) 추가 → CLK 무신호 원인(transfer 미호출 vs 호출 후 무출력) 판정.

## 구현 현황

| 기능 | 상태 | 메모 |
|------|------|------|
| S0 AM263P 마이그레이션 | ✓ | `--device AM263Px` 빌드 성공 |
| S1 MCELF 빌드 + JTAG 플래시 | ✓ | jtag_flasher 6작업 전부 성공 (R10) |
| S2 부팅 + UART 진단 마커 | ✓ | `[DIAG] A..G` 출력 |
| S3 app `Flash_open()` 유효 핸들 | ✓ | pinmux `$assign` 교정으로 R28b 통과. RDID=`9D 5A 19` |
| S4 Drivers_open / Board_open 완주 | ✓ | R31 통과. 표준 Board_flashOpen 단독 동작 실측 검증 |
| S5 CC33xx FW 로드 + NP 기동 | △ | `Hardware init DONE!` 도달(R32). MISO D1 교정(R34). CS 물리 어서트 확인(R35). CLK/MOSI 무신호 — MCSPI_transfer 호출 여부 미판정 |
| S6 SPI/IRQ link-up | ✗ | `SPI not responsive`. CLK 핀 무신호(R35). MCSPI_transfer 미호출 또는 CLK 미출력 원인 미판정 |
| S7 network_terminal CLI | ✗ | S6의 2차 결과 |
| S8 BLE HCI 경로 | ? | 미도달 |

상태 기호: `✓` 구현+검증 / `△` 구현됨·미검증 / `?` 불명 / `✗` 미구현

## 미결 사항

- **MCSPI_transfer 호출 여부 미판정** — 측정·배선·pinmux·물리매핑 원인 R35(cont.) 전부 배제됨. transfer 미호출 vs 호출 후 CLK 미출력 판정만 남음. `[R36-SPI] transfer count/ret` 마커 필요.
- flash FS 쓰기 미검증 — `osi_filesystem.c:131` "Skip flash writing due to APIs issue".
- [H-A] skipHwInit=TRUE 최소 충분 패치셋 미분리 — quirksFxn/skipHwInit/dummyClksCmd 중 필수 조합 미확인.
