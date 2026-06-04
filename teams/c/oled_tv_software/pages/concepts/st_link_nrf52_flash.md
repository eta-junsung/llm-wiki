---
tags: [concept, howto, flashing, nrf52832, st-link, pyocd]
source: 2026-06-04 03_TX_ble 플래싱 성공 경험
date: 2026-06-04
subsystem: 02_RX_ble, 03_TX_ble
---

# ST-LINK V2 + pyOCD로 nRF52832 보드 플래싱

[[rx_ble_module]](BLE_Module_Board_Ver0.1E00, nRF52832)에 `02_RX_ble` / `03_TX_ble` 펌웨어를 **ST-LINK V2 + pyOCD**로 굽는 검증된 절차. 2026-06-04 `03_TX_ble` 플래싱 성공으로 확립.

---

## 왜 pyOCD인가

SES(SEGGER Embedded Studio)의 내장 다운로드와 `nrfjprog`는 **J-Link 전용** → ST-LINK로 사용 불가.
따라서 SES는 **.hex 빌드까지만** 쓰고, **플래싱은 pyOCD**로 우회한다. (OpenOCD도 가능하나 동일하게 WinUSB 필요.)

---

## 전제 (Windows)

- Python 설치(pip 사용 가능). 본 환경은 Python 3.14.
- `pip install pyocd`. Scripts가 PATH에 없으면 `python -m pyocd ...`로 호출.

---

## 일회성 호스트 셋업 (처음 한 번, 3개 함정)

### 1. libusb 네이티브 DLL 공급

Python 3.14엔 `libusb-package` 바이너리 wheel이 없어 DLL이 빠진다. cp311 wheel을 받아 `libusb-1.0.dll`만 추출해 현재 환경 `site-packages/libusb_package/`에 복사.

없으면 `pyocd list`가 `"no libusb library was found"`로 ST-Link를 못 본다.

### 2. ST-LINK를 WinUSB로 바인딩

Zadig로 ST-LINK 인터페이스(USB ID `0483:3748`)를 WinUSB로 교체.

⚠️ **부작용**: 이 동글로는 **STM32CubeIDE/CubeProgrammer 플래싱이 불가**해진다. 장치관리자에서 드라이버 제거 → 재인식으로 복구.

증상 식별: libusb가 ST-Link를 열거는 하나 string descriptor 읽기 실패(`"no langid"`).

### 3. pyOCD CTRL-AP 패치

ST-LINK V2 펌웨어는 nRF52의 보조 AP(CTRL-AP, AP#1) 접근을 못 한다. pyOCD nRF52 init이 `is_locked()`에서 CTRL-AP의 `APPROTECTSTATUS`를 읽다 `STLink error (29): Bad AP`로 죽는다.

`site-packages/pyocd/target/family/target_nRF52.py`의 `is_locked()`에 `try/except`로 `ProbeError`를 잡아 `return False`(= unlocked 간주) 추가.

- AHB-AP가 살아있으면 칩은 정상이며 잠기지도 않았으므로 안전.
- **pyocd 재설치 시 패치 소실 → 재적용 필요.**

---

## 배선 (전원 + SWD)

커넥터 상세 → [[schematic_ble_module_board_v01e00]] CON1 절.

- **CON1(SWD, 5핀)** 신호: `SWDCLK_uC / SWDIO_uC / SWD_nRST / BLE_P3V3 / BLE_GND`. 물리 핀 순서는 회로도에 핀번호 없음 → **실물 실크 Pin1 마킹** 기준.
- **급전**: CON1의 `BLE_P3V3` 핀에 **3.3V**(ST-LINK V2의 3.3V 출력 사용). GND는 `BLE_GND`.
- TP1/TP2 테스트핀이 `BLE_GND` → 측정 기준점으로 사용.
- **확인 필수**: `BLE_P3V3` ↔ TP1 전압이 **3.3V**인지 멀티미터 실측(ST-LINK 3.3V 핀이 VTREF면 전원이 안 들어옴).

⚠️ **전원 금지사항**: CN2(SPI, 매뉴얼 CN3)의 **핀1·2 = PD3V3(3.3V), 핀9·10 = GND**. 핀2는 GND가 아니다. PD3V3는 강압 없이 nRF VCC에 직결 → **5V 인가 금지(과전압)**.

---

## 플래싱 절차

```
# 1. 빌드 (SES CLI)
'C:/Program Files/SEGGER/SEGGER Embedded Studio 8.28/bin/emBuild.exe' \
  -config Debug 03_TX_ble/TX_BLE.emProject
# → 산출: 03_TX_ble/Output/Debug/Exe/TX_BLE.hex

# 2. 프로브 확인
python -m pyocd list
# → STM32 STLink 등장 확인
# ⚠️ TI XDS110(AM263P용, UID S26E0086)이 공존 → 반드시 ST-Link UID로 못박을 것

# 3. 연결 점검
python -m pyocd cmd -t nrf52832 -u <ST-LINK-UID> -c "reset halt"
# → "Successfully halted"

# 4. 플래싱
python -m pyocd flash --target nrf52832 -u <ST-LINK-UID> "<hex 경로>"
# → "programmed N bytes" 확인

# 5. 실행
python -m pyocd cmd -t nrf52832 -u <ST-LINK-UID> -c "reset"
```

이번 환경 ST-LINK UID 예: `40004100040000433539594E`.

---

## 트러블슈팅

| 증상 | 원인 | 조치 |
|---|---|---|
| `pyocd list`에 ST-Link 없음, `"no libusb"` | libusb DLL 부재 | 셋업 1 |
| ST-Link 열거되나 `"no langid"` / 접근 실패 | 드라이버 비-WinUSB | 셋업 2 (Zadig) |
| `STLink error (29): Bad AP` | ST-Link가 CTRL-AP(AP#1) 접근 불가 | 셋업 3 (pyocd 패치). `-t cortex_m`으로 `reset halt` + `readdp 0`=`0x2ba01477`이면 칩 정상·미잠금 확인 |
| `STLink error (9): Get IDCODE error` | SWDIO/SWDCLK 스왑 또는 미접촉 | SWD 두 선 바로잡기 |
| 무응답 · `Bad AP` 지속 | 전원 미급전 / GND 미연결 | `BLE_P3V3`=3.3V · GND 실측 |

---

## 미확정

- CON1 물리 핀번호 ↔ 네트 매핑 (실크 Pin1 확인 필요).
- B1(SHH-1M2012-221) / FLT1(NFM41PC155B1H3L)이 필터인지 (강압 없음 강력 시사, 데이터시트 미확인).
- CON2 UART의 nRF GPIO 핀 (펌웨어는 PCA10040 P0.06/P0.08 사용, 회사 보드 라우팅 미확인).

---

## 관련

- [[rx_ble_module]] — CON1(SWD) 커넥터 스펙
- [[schematic_ble_module_board_v01e00]] — 회로도 상세 (CON1 신호, 전원 아키텍처)
