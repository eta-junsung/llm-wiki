---
tags: [concept, boot, uart, diagnostic, flash, ospi, am263p, 8kw]
source: 실측 (2026-06-12, 8kw-ev-wpt-tx 실보드 — UART0 콘솔 캡처·SBL provenance 확인)
date: 2026-06-12
---

# OSPI 부팅 진단 — UART0 콘솔 채널·boot triage recipe·flash 프로그래밍 블로커

> **8kw-ev-wpt-tx 특정 페이지.** 2026-06-12 진단 사이클의 검증된 사실 묶음(진단 채널·triage recipe·SBL provenance).
> 부팅 실패 확정 전체 맥락은 [[toggle_free_flash_loop]] §②. JTAG flash 굽기 정본은 [[jtag_flash_harness]].
>
> ⚠️ **§3 갱신 (2026-06-12, standalone 무부팅 해소)**: 이 페이지가 §3에서 잔여 블로커로 지목하던 "flash 프로그래밍/설정(cell 영속성·QE bit NV)"은 **무효**로 판명. 진짜 원인은 **부트모드 핀 스트랩 미스매치**(SW1=`1,1,1,1`=4S Quad가 octal-only 칩과 불일치)였고, SW1=`0,0,1,1`(xSPI 8D SFDP)로 교정해 **완전 부팅 실측**. 정본 [[ospi_boot_mode_strap]]. 아래 §2 triage recipe와 §4 SBL provenance는 여전히 유효.

---

## 1. COM4 = UART0 콘솔 (진단 채널 확정)

- **COM4 = "XDS110 Class Application/User UART"** = **SoC UART0 콘솔**.
  SBL banner와 ROM UART fallback ping(`'C'`) 둘 다 이 포트로 나온다.
- **보드 USB 전원(VCC)과 XDS110/COM4 전원이 분리**돼 있어, 보드 VCC 사이클 중에도 COM4 연결 유지 가능 → 전원사이클 전후를 단일 캡처 세션에서 끊김 없이 수집 = **깨끗한 부팅 캡처**.
- 설정: 115200/8N1.

---

## 2. Boot stage triage recipe

COM4(UART0)에서 관측되는 출력으로 부팅이 어느 단계에서 막혔는지 식별한다.

| 관측 | 판정 | 의미 |
|------|------|------|
| SBL banner **없음** + `'C'`(0x43) XMODEM ping 반복 | **ROM→SBL 로드 실패** | ROM이 OSPI flash에서 SBL을 읽는 데 실패 → 원인: 부트모드 스트랩 미스매치(§3, [[ospi_boot_mode_strap]]) — flash 프로그래밍 아님 |
| SBL banner(boot profile) **있음** → 이후 `'C'` ping 다시 시작 | **SBL→app 핸드오프 실패** | SBL은 로드됐으나 app mcelf 로드·실행 실패 |
| `"eta-tx: 8kw-ev-wpt start"` (app banner) 출력 | **부팅 정상** — PWM 무토글이라면 측정·배선 문제 |  |

**근거**:
- `'C'` ping은 ROM만 송신 (TRM `raw/am263p_trm/ch05_initialization.md`:877).
- ROM은 OSPI 부팅 "any failures"면 UART fallback 진입 (TRM ch05:133).
- ROM이 SBL 점프 성공하면 그 뒤 SBL/app이 죽어도 ROM 레벨 fallback 없음.

**2026-06-12 실측 결과**: `'C'` ping + ID 블롭(`"AM263PX"/cdab=0xABCD/32B hash`) 반복·SBL banner 전무 → **ROM→SBL 로드 단계 실패** 판정.
VCC 완전 제거(USB-unplug)·SW2/SW3 버튼 안 씀 확인 → [[toggle_free_flash_loop]] §③의 4-byte stuck 경로 완전 배제.

> **이 `'C'` ping의 근본 원인(2026-06-12 해소)**: ROM→SBL 실패의 이유는 flash 프로그래밍이 아니라 **부트모드 스트랩 미스매치**였다 — SW1=`1,1,1,1`(4S Quad)에서 ROM이 `0x6B`+QE를 기대하는데 보드 flash(IS25LX256)는 octal-only라 `0x6B`을 디코드 못 함 → "any failures" → UART fallback `'C'`. SW1=`0,0,1,1`(xSPI 8D SFDP)로 교정하니 같은 flash 내용이 정상 부팅. 정본 [[ospi_boot_mode_strap]]. **triage recipe 자체(C ping = ROM→SBL 실패)는 정확했고, 후속 §3의 원인 귀속만 틀렸었다.**

---

## 3. ~~잔여 블로커 — flash 프로그래밍/설정~~ → **해소: 진짜 원인은 부트모드 스트랩 미스매치**

> **이 절의 종전 프레이밍 ((a)flash cell 영속성 / (b)QE bit NV)은 2026-06-12 무효 판정.** 보존을 위해 아래 취소선으로 남기되, **재시도 금지**. 진짜 원인과 해소는 [[ospi_boot_mode_strap]] 정본 참조.

ROM→SBL 실패의 원인은 flash 프로그래밍이 **아니라** SW1 부트모드 스트랩이 보드 flash 프로토콜과 어긋난 것이었다:

- 보드 flash = **IS25LX256 = octal-only**(Extended SPI + Octal DDR만; **quad·`0x6B`·QE bit 물리적 부재** — `raw/IS25LX256/` 전 챕터 grep 0건, [[ospi_boot_mode_strap]] §2).
- SW1=`1,1,1,1`(OSPI 4S Quad)이면 ROM이 `0x6B`(`ch05:749`)+QE NV SET(`ch05:757`)을 기대 → octal 칩이 못 받음 → ROM read 실패 → UART fallback `'C'`.
- **SW1=`0,0,1,1`(xSPI 8D SFDP)** 로 교정 → ROM이 SFDP에서 read cmd 자동 결정 → **같은 flash 내용이 VCC 전원사이클 후 완전 부팅**(SBL→app→`eta-tx: 8kw-ev-wpt start`).

따라서 굽힌 이미지·flash cell·QE 설정에는 애초에 문제가 없었다.

<details><summary>무효가 된 종전 프레이밍 (보존용, 재시도 금지)</summary>

> ### ~~(a) flash cell 영속성~~ — **무효**
> ~~flashwriter가 쓴 데이터가 flash cell에 NV 커밋됐는가. readback PASS는 동일 JTAG 세션 XIP 뷰라 POR-read 생존 미검증.~~ → strap 교정만으로 같은 flash가 정상 부팅했으므로 cell은 정상 커밋돼 있었다.
>
> ### ~~(b) flash NV config·QE bit~~ — **물리적으로 불가**
> ~~ROM 4S(0x6B)는 QE bit NV SET을 기대(TRM ch05:757).~~ **이 칩에 QE bit 자체가 없다** — 4S 부팅이 애초에 성립하지 않는 칩에 "QE를 SET해야 한다"는 명제는 적용 불가. (TRM ch05:757 인용 자체는 정확하나, "이 보드가 4S 부팅이 맞다"는 전제가 오류였다.)

</details>

---

## 4. SBL provenance — 파일 무결성 확정

`flash_node_8kw.js`가 굽는 `C:/ti/sbl_ospi_am263p.tiimage`(307005B, SHA256 `735D12EB...58108B7`)는 SDK 공식 프리빌트와 **바이트 동일**:

```
mcu_plus_sdk_am263px_26_00_00_01\tools\boot\sbl_prebuilt\am263px-lp\
    sbl_ospi_multicore_elf.release.tiimage
```

- 파일명 `am263p`는 공식 rename.
- **SBL 변종**: `multicore_elf` — `.mcelf` 앱과 짝. ✓
- **실리콘**: `am263px-lp` — 이 보드의 SoC와 일치. ✓
- **무결성**: 바이트 동일. ✓

**결론**: "SBL 파일이 잘못됐다" 가설 완전 제거. 블로커는 SBL 자체가 아니었고 — §3대로 **부트모드 스트랩 미스매치**였다([[ospi_boot_mode_strap]]). strap 교정 후 이 동일 SBL이 정상 부팅.

상세(harness 정본): [[jtag_flash_harness]] §8.

### SDK 버전 간 SBL 해시 차이 — 정상 현상

SDK 버전이 바뀌면(예: 26_00_00_01 → 26_00_00_06) prebuilt SBL의 **파일 크기는 동일(307,005B)하나 SHA256 해시가 상이**하다. TI가 SDK 빌드마다 서명 cert의 serial number·timestamp를 재발급하기 때문이며, 기능은 동등하다.

**SBL 확보 방법**: 머신 간 파일 이주 불필요 — SDK만 설치하면 prebuilt에서 직접 복사·리네임:

```
<SDK>/tools/boot/sbl_prebuilt/am263px-lp/sbl_ospi_multicore_elf.release.tiimage
  → C:/ti/sbl_ospi_am263p.tiimage
```

---

## 5. route② `.mcelf` standalone 부팅 — **실증됨 (2026-06-12)**

종전(2026-06-05까지)에는 현재 route② build/.mcelf 이미지로 standalone 부팅이 성공한 실적이 **없었다** — 2026-06-05 banner(`eta-tx: 8kw-ev-wpt v1.0e00`)는 다른 이전 이미지였고(`src/main.c`:45 현재 banner는 `"eta-tx: 8kw-ev-wpt start"`).

**2026-06-12 해소**: SW1을 올바른 스트랩(`0,0,1,1` = xSPI 8D SFDP, [[ospi_boot_mode_strap]])으로 두고 VCC 완전 제거 후 재인가 → SBL → `"Image loading done, switching to application"` → app → `eta_pwm_init`(EPWM2/4/7 85 kHz) → **`eta-tx: 8kw-ev-wpt start`**. banner 문구가 현재 `src/main.c`:45와 일치 → **현재 route② 이미지의 standalone 부팅 실증 게이트 통과**.

> ⚠️ 2026-06-05 banner(`...v1.0e00`)는 구 이미지. 실증의 근거는 2026-06-12 `...start` banner다.

---

## 정정 이력

- ✅ **`tools/gui/gui.py`·`tools/jtag_flash/flash_8kw.js` SW1 라벨 (2026-06-12 수정)**: 종전 `"SW1=OSPI (DevBoot 0,1,0,0)"`·`1,1,1,1` 혼용 라벨이 잘못된 mental model을 강화 → **`0,0,1,1`(xSPI 8D SFDP)로 정정**. 근거 [[ospi_boot_mode_strap]].
- ✅ **[[jtag_flash_harness]] §4 / [[toggle_free_flash_loop]] §③ "1,1,1,1에서 부팅" 기록**: octal-only 칩에서 4S 부팅은 불가 → strap 라벨 오기 추정. 해당 페이지에 모순 표시 완료.
- **[[jtag_flash_harness]] §4 banner 문구**: `eta-tx: 8kw-ev-wpt v1.0e00`는 구 이미지 기준. 현재 `src/main.c`:45는 `"eta-tx: 8kw-ev-wpt start"`(2026-06-12 실증).

---

## 함께 보기

- **부트모드 스트랩 미스매치 = standalone 무부팅 진짜 원인(해소 정본)**: [[ospi_boot_mode_strap]]
- 토글-프리 루프 전체 맥락: [[toggle_free_flash_loop]]
- JTAG flash 굽기 정본(SBL provenance §8 포함): [[jtag_flash_harness]]
- OSPI RESET·QE bit 핸드오프: [[sbl_app_flash_handoff]]
- ROM boot flow 원문: [[am263p_trm]] §5.4.1 (`ch05_initialization.md`:877·:133·:757)
- UART5 텔레메트리 (독립 부팅 증거 채널): [[uart5_packet_protocol]] · [[pc_monitor_gui]]
