---
tags: [concept, nrf52, gpio, nfc, pinconfig]
source: 2026-06-17 커스텀 보드 UTO-NBK-52 LED1 NFC 핀 이슈 실측 + 2026-06-18 비점등≠NFC모드 사례
date: 2026-06-18
subsystem: 02_RX_ble, 03_TX_ble
---

# nRF52832 NFC 핀 GPIO 전용화 (CONFIG_NFCT_PINS_AS_GPIOS)

## 배경

nRF52832에서 **P0.09·P0.10은 기본 NFC 안테나 핀**(NFC1/NFC2)이다. GPIO로 쓰려면 빌드 정의 `CONFIG_NFCT_PINS_AS_GPIOS`가 필요하다.

커스텀 보드 [[uto_nbk_52]]가 **LED1을 P0.09**에 두므로, 02_RX_ble·03_TX_ble 빌드에 이 define이 필수다.

## 동작 원리

`CONFIG_NFCT_PINS_AS_GPIOS` 정의 시, SDK `system_nrf52.c`의 `SystemInit()`이 부팅 시:

1. `UICR.NFCPINS`(`0x1000120C`)를 읽어 NFC 모드인지 확인
2. NFC 모드(`bit0=1`)이면 `0x1000120C`를 `0xFFFFFFFE`(bit0=0)로 써서 GPIO 모드로 전환
3. 자기 리셋(`NVIC_SystemReset()`) 수행 — 설정 즉시 반영

## UICR.NFCPINS 값

| 값 | 의미 |
|----|------|
| `0xFFFFFFFF` (erase 상태) | NFC 모드 (bit0=PROTECT=1) |
| `0xFFFFFFFE` (bit0=0) | GPIO 모드 ← 원하는 상태 |

SES 메모리뷰 또는 `mem32 0x1000120C 1`으로 확인.

## ⚠️ 함정 — 디버거 부팅 시 미반영

`CONFIG_NFCT_PINS_AS_GPIOS` 정의 + 최초 플래시 후:

- **SES/J-Link 디버거 세션 중** 부팅하면 자가설정이 미반영될 수 있다 → LED1(P0.09) 미점등
- **올바른 확인 방법**: 디버거 없이 **전원 재인가(cold boot)** 하거나 SES `Target > Download & Reset` 후 디버거 분리 → LED1 점등이면 정상
- UICR은 한 번 써지면 이후 플래시에도 유지됨(UICR erase 없는 한)

## 빌드 적용 위치

`02_RX_ble/RX_BLE.emProject` 및 `03_TX_ble/TX_BLE.emProject`의 `c_preprocessor_definitions`에 `CONFIG_NFCT_PINS_AS_GPIOS` 추가. (`47e46db`, 2026-06-17)

## ⚠️ 추가 함정 — LED 비점등 ≠ NFC 모드 (2026-06-18 사례)

UICR.NFCPINS가 올바르게 `0xFFFFFFFE`(GPIO 모드)이어도 **LED가 켜지지 않는 경우가 있다** — NFC 모드 잔류가 아니라 **펌웨어 극성 오기** 가능성을 먼저 확인할 것.

**UTO-NBK-52 LED 극성: active-HIGH** (HIGH=점등). 확정 근거 (2026-06-18 실보드 실측):
- 03 보드(DEVICEID `0xE9775EC9`) P0.9 HIGH 기록 → LED1 점등 ⟹ HIGH=ON
- LED3(P0.6) LOW 기록(ESB UP 시) → 소등 ⟹ LOW=OFF
- 4점이 active-HIGH로만 모순 없이 설명됨

**02 보드(DEVICEID `0x09741932`) LED1 미점등 원인 추정**: firmware `LED1_ON=0u`(active-LOW 가정)로 LOW를 써서 꺼진 것 — **하드웨어 개체 결함 아님. 재측정 대상.** firmware 극성 수정(`LED1_ON=1u`) 후 재검증 필요.

→ **진단 게이트**: JLink `mem32`로 GPIO 레지스터 확인:
- `PIN_CNF[9]` DIR/OUTPUT 방향 ✓
- NFCPINS = `0xFFFFFFFE` ✓
- 위 조건 정상인데 미점등 → **firmware가 쓰는 값(OUT bit)** 확인. active-HIGH 보드에 LOW를 쓰면 꺼짐.

## 관련

- [[uto_nbk_52]] — UTO-NBK-52 보드 핀맵 (LED1=P0.09 사용 보드, LED **active-HIGH** 확정)
- [[nrf52_firmware_conventions]] — nRF52 빌드 컨벤션
- [[st_link_nrf52_flash]] — UICR 레지스터 읽기 절차 (메모리뷰 / mem32)
