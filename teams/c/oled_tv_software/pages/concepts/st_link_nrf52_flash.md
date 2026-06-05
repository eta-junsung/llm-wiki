---
tags: [concept, howto, flashing, nrf52832, stm32f103, j-link, st-link, segger, pyocd]
source: 2026-06-05 CLI 실측 (JLink.exe / STM32_Programmer_CLI / emBuild)
date: 2026-06-05
subsystem: 01_RX_control, 02_RX_ble, 03_TX_ble
---

# 3-MCU 플래싱 셋업 (듀얼 프로브 — J-Link / ST-Link 네이티브)

oled_tv_software 세 펌웨어를 실보드에 굽는 **정본** 절차. 2026-06-05 CLI 실측으로 확립.

핵심 전환(2026-06-04 → 06-05): 예전엔 ST-Link V2 하나를 WinUSB(pyOCD)↔ST 정품 드라이버로 **번갈아 끼우며**(드라이버 스왑) STM32와 nRF를 오갔다. 이제 **MCU별 전용 프로브 + 네이티브 도구**로 분담한다 — 드라이버가 분리되어 **동시 연결·충돌 없음**. pyOCD+Zadig 경로는 [폴백](#폴백-pyocd--zadig-강등)으로 강등.

> 프로브 하드웨어 정체(S/N·HW·라이선스)·드라이버는 회사 공통 [[instruments]] "프로그래밍/디버그 프로브" 절에 등록. 이 페이지는 **절차·실측·함정**.

---

## 프로브 분담 (드라이버 스왑 종료)

| 펌웨어 | MCU | 프로브 | 네이티브 도구 |
|---|---|---|---|
| `01_RX_control` | STM32F103RCTx | **ST-Link V2** (네이티브) | STM32CubeProgrammer GUI+CLI / CubeIDE F11 |
| `03_TX_ble` | nRF52832 (회사 커스텀보드) | **J-OB v2** = `J-Link OB-nRF5340-NordicSemi` (정품) | SES Download&Reset / nrfjprog / JLink.exe |
| `02_RX_ble` | nRF52832 (DK PCA10040) | 보드 **온보드 J-Link** | SES / nrfjprog / JLink.exe |

세 프로브는 드라이버가 분리(ST-Link 네이티브 / SEGGER J-Link)되어 한 PC에 동시 꽂아도 충돌하지 않는다.

---

## 03_TX_ble (nRF52832 회사보드) — J-OB v2 / J-Link [정본]

프로브 정체·라이선스 → [[instruments]]. 요점: `J-Link OB-nRF5340-NordicSemi`, S/N **1050329071** (클론 아님, FW mismatch 경고 없음). 설치 경로 `C:\Program Files\SEGGER\JLink_V948\JLink.exe` (V942도 공존).

### ⚠ 함정 — SN 고정 필수

이 PC엔 J-Link급 프로브가 **둘**(J-OB v2 + `SAM-ICE` S/N 24012600) → 무지정 시 어느 것을 쓸지 모호해 **connect 실패**. 반드시 `-SelectEmuBySN 1050329071`로 못박는다.

### 빌드 (SES CLI)

```
'C:/Program Files/SEGGER/SEGGER Embedded Studio 8.28/bin/emBuild.exe' \
  -config Debug 03_TX_ble/TX_BLE.emProject
# → 산출: 03_TX_ble/Output/Debug/Exe/TX_BLE.hex
```

### 플래싱 (JLink.exe, program+verify)

```
JLink.exe -device nRF52832_xxAA -if SWD -speed 4000 \
  -SelectEmuBySN 1050329071 -NoGui 1 -ExitOnError 1 -CommandFile <script>
```

CommandFile 내용 (loadfile = program + 자동 verify):

```
si SWD
speed 4000
connect
loadfile <hex>
r
g
q
```

**connect 실측** (위 명령): device `nRF52832_xxAA`, SWD 4000 kHz, `Found SW-DP ID 0x2BA01477`, `Cortex-M4 r0p1 identified`, VTref=**3.300 V**, FICR `0x10000060 = 0x2365A055`.

**플래시 실측** (program+verify 통과): `Erasing...Done` → `Programming 100% Done` → `Verifying ... O.K.`, **Bank0@0x0 = 53248 bytes**, reset+go, **exit 0**, APPROTECT 잠김 없음.

---

## 01_RX_control (STM32F103) — ST-Link V2 네이티브

ST-Link V2를 ST 정품 드라이버로 둔 채 STM32_Programmer_CLI / CubeIDE로 직접 다룬다 (WinUSB·Zadig 불필요).

CLI 진입점 (CubeIDE 2.1.1 번들, v2.22):

```
C:\ST\STM32CubeIDE_2.1.1\...\cubeprogrammer.win32_2.2.400.*\tools\bin\STM32_Programmer_CLI.exe \
  -l st-link \
  -c port=SWD mode=normal
```

**connect 실측**: ST-Link FW **V2J47S7**, `Device ID 0x414` (STM32F101/F103 High-density), Cortex-M3, NVM **256 KB**, **3.27 V**, UID@0x1FFFF7E8 = `05DAFF36 32374742 57016011`.

> ⚠ 함정 — 이 ST-Link은 S/N이 `@`로 보고됨(cosmetic). 다중 ST-Link 환경이면 `sn=`으로 타게팅 불가 → 인덱스 우회 필요. 현재 단일이라 무영향.

실플래시(write)는 미측정(아래 [빈자리](#미확정-빈자리)) — connect+read까지만 실측. 실플래시는 **CubeIDE F11** 자리.

---

## 02_RX_ble (DK PCA10040) — 온보드 J-Link

DK는 보드에 J-Link가 내장 → 외부 프로브 불요. SES Download&Reset / nrfjprog / JLink.exe 그대로 사용 (J-OB v2와 동일 도구군, SN만 다름).

---

## 모니터 출력 보는 법 — RTT(SWD) vs UART(CON2)

회사 커스텀보드(BOARD_CUSTOM)의 두 출력 경로는 **별개 커넥터**다:

- **NRF_LOG → RTT 전용** (SWD/CON1 경유, J-Link RTT Viewer). UART엔 안 나온다.
- **모니터 printf → app_uart → UART 핀 → ISO6721 절연 → CON2** 로 PC 직결. UART **TX=P0.15 / RX=P0.14** (`_shared/custom_board.h:16-17`, `TX_PIN_NUMBER=15 / RX_PIN_NUMBER=14`). CON2는 SWD용 CON1과 **다른 커넥터**.

> 낡은 기록 교정: 회사보드 CON2 UART를 DK 기본값 P0.06/P0.08로 적은 페이지가 있으면 위 P0.15/P0.14로 본다. (P0.06/P0.08은 회사보드에선 LED3/LED2 핀 — [[schematic_ble_module_board_v01e00]].) 커넥터·핀 1차 출처 → [[schematic_ble_module_board_v01e00]] CON2 절.

---

## 배선 (전원 + SWD)

커넥터 상세 → [[schematic_ble_module_board_v01e00]] CON1 절. (회사보드 nRF는 SWD CON1, 급전은 CON1 `BLE_P3V3`=3.3V / `BLE_GND`. 프로브 3.3V 핀이 VTREF면 전원 미인가이므로 멀티미터로 3.3V 실측.)

⚠ 전원 금지: CN2(SPI)의 PD3V3는 강압 없이 nRF VCC 직결 → **5V 인가 금지**.

---

## 폴백: pyOCD + Zadig (강등)

J-Link/ST-Link 네이티브가 막힐 때만 쓰는 우회로. **현재 불필요** — 드라이버 분리로 스왑 자체가 사라졌다. 2026-06-04 `03_TX_ble`를 ST-Link V2 + pyOCD로 처음 구운 경로이며, 일회성 호스트 셋업에 함정 3개가 있었다:

1. **libusb 네이티브 DLL** — Python 3.14엔 `libusb-package` 바이너리 wheel이 없어 cp311 wheel에서 `libusb-1.0.dll`만 추출해 `site-packages/libusb_package/`에 복사. 없으면 `pyocd list`가 `"no libusb library was found"`로 ST-Link를 못 봄.
2. **ST-Link를 WinUSB로 바인딩** — Zadig로 USB ID `0483:3748`을 WinUSB로 교체. 부작용: 이 동글로 CubeIDE/CubeProgrammer 플래싱 불가.
3. **pyOCD CTRL-AP 패치** — `site-packages/pyocd/target/family/target_nRF52.py`의 `is_locked()`에 `try/except ProbeError → return False` 추가 (ST-Link V2가 nRF CTRL-AP(AP#1) 접근 불가 → `STLink error (29): Bad AP`로 죽음). 재설치 시 패치 소실.

절차: `python -m pyocd flash --target nrf52832 -u <ST-LINK-UID> "<hex>"`. (이번 환경 ST-Link UID 예: `40004100040000433539594E`.)

| 증상 | 원인 | 조치 |
|---|---|---|
| `pyocd list`에 ST-Link 없음 / `"no libusb"` | libusb DLL 부재 | 셋업 1 |
| ST-Link 열거되나 `"no langid"` / 접근 실패 | 드라이버 비-WinUSB | 셋업 2 (Zadig) |
| `STLink error (29): Bad AP` | ST-Link가 CTRL-AP 접근 불가 | 셋업 3 (pyocd 패치) |
| `STLink error (9): Get IDCODE error` | SWDIO/SWDCLK 스왑·미접촉 | SWD 두 선 바로잡기 |
| 무응답 · `Bad AP` 지속 | 전원 미급전 / GND 미연결 | `BLE_P3V3`=3.3V·GND 실측 |

### ST-Link을 WinUSB → ST 정품으로 원복 (네이티브 경로 복귀)

폴백(Zadig WinUSB)을 썼다가 STM32 네이티브로 돌아갈 때: 장치관리자에서 ST-Link(`STM32 STLink`, `0483:3748`) → 우클릭 → **디바이스 제거 + "드라이버 소프트웨어 삭제" 체크** → 재플러그 → Windows가 ST 정품 드라이버 재설치. (Zadig로는 정품 복원 불가.) 확인: CubeProgrammer Connect 성공.

---

## 미확정 (빈자리)

- **SES 번들 JLinkARM DLL의 SN 선택 동작**(`-SelectEmuBySN` 등가) 미검증 — JLink.exe CLI에서만 SN 고정 실측.
- **ST-Link → STM32 실플래시(write)** 미측정 — connect+read까지만. 실플래시는 CubeIDE F11 자리.
- **플래시한 펌웨어의 런타임 거동**(ESB/SPI/LED) 미측정.
- SAM-ICE(S/N 24012600)의 연결 대상·용도 미상 — 현재는 SN 충돌원으로만 인지. → [[instruments]].
- CON1 물리 핀번호 ↔ 네트 매핑 (실크 Pin1 확인 필요) → [[schematic_ble_module_board_v01e00]].

---

## 관련

- [[instruments]] — 프로브 3종 정체·S/N·드라이버 (회사 공통)
- [[rx_ble_module]] — CON1(SWD)·CON2(UART) 커넥터 스펙
- [[tx_ble_module]] — 03_TX_ble LED·보드 분기(custom_board.h)
- [[schematic_ble_module_board_v01e00]] — 회로도 (CON1 SWD·CON2 UART P0.15/14·전원)
