---
tags: [concept, boot, uart, diagnostic, flash, ospi, am263p, 8kw]
source: 실측 (2026-06-12, 8kw-ev-wpt-tx 실보드 — UART0 콘솔 캡처·SBL provenance 확인)
date: 2026-06-12
---

# OSPI 부팅 진단 — UART0 콘솔 채널·boot triage recipe·flash 프로그래밍 블로커

> **8kw-ev-wpt-tx 특정 페이지.** 2026-06-12 진단 사이클의 검증된 사실 묶음.
> 부팅 실패 확정 전체 맥락은 [[toggle_free_flash_loop]] §②. JTAG flash 굽기 정본은 [[jtag_flash_harness]].

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
| SBL banner **없음** + `'C'`(0x43) XMODEM ping 반복 | **ROM→SBL 로드 실패** | ROM이 OSPI flash에서 SBL을 읽는 데 실패 → 블로커: flash 프로그래밍/설정(§3) |
| SBL banner(boot profile) **있음** → 이후 `'C'` ping 다시 시작 | **SBL→app 핸드오프 실패** | SBL은 로드됐으나 app mcelf 로드·실행 실패 |
| `"eta-tx: 8kw-ev-wpt start"` (app banner) 출력 | **부팅 정상** — PWM 무토글이라면 측정·배선 문제 |  |

**근거**:
- `'C'` ping은 ROM만 송신 (TRM `raw/am263p_trm/ch05_initialization.md`:877).
- ROM은 OSPI 부팅 "any failures"면 UART fallback 진입 (TRM ch05:133).
- ROM이 SBL 점프 성공하면 그 뒤 SBL/app이 죽어도 ROM 레벨 fallback 없음.

**2026-06-12 실측 결과**: `'C'` ping + ID 블롭(`"AM263PX"/cdab=0xABCD/32B hash`) 반복·SBL banner 전무 → **ROM→SBL 로드 단계 실패** 판정.
VCC 완전 제거(USB-unplug)·SW2/SW3 버튼 안 씀 확인 → [[toggle_free_flash_loop]] §③의 4-byte stuck 경로 완전 배제.

---

## 3. 잔여 블로커 — flash 프로그래밍/설정

boot stage가 ROM→SBL 실패로 확정됐고 4-byte stuck 경로(warm reset 주소 불일치)가 배제됐으므로, 블로커는 **flash 프로그래밍/설정** 중 하나다.

### (a) flash cell 영속성

flashwriter(`jtag_flasher.out` = SDK `sbl_jtag_uniflash`)가 OSPI 컨트롤러를 통해 쓴 데이터가 **flash cell에 실제로 NV 커밋됐는가**.

**readback PASS의 한계**: 굽기 직후 `0x60000000`(SBL magic)·`0x60081000`(ELF magic) readback PASS는 **동일 JTAG 세션의 OSPI 컨트롤러 XIP 뷰**다. JTAG 세션 리셋·전원사이클 후에도 ROM이 같은 주소를 읽어낼 수 있는지(cell 커밋·POR-read 생존)를 **독립 검증하지 않은 상태**.
→ 구 `verify_ospi_8kw.js`는 Rhino API 의존이라 Node `run.bat`에서 동작 안 함([[jtag_flash_harness]] §1). 세션 독립 readback 검증 수단 미확립.

### (b) flash NV config·QE bit

ROM 4S(0x6B Quad Output Fast Read) 실행은 flash **QE(Quad Enable) bit = NV SET** 상태를 기대 (TRM `ch05_initialization.md`:757).
`flashFixUpOspiBoot()`([[sbl_app_flash_handoff]])가 굽기 세션 중 OSPI 1S 복귀를 수행하는데, 그 과정에서 QE bit NV 보존 여부가 미확인.

**다음 검증 방향**: 재전원 후 XDS110 JTAG으로 `0x60000000` 독립 readback — 값이 살아있으면 cell 커밋 ✓(QE 문제로 좁힘), 값이 0xFF면 cell 미커밋.

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

**결론**: "SBL 파일이 잘못됐다" 가설 완전 제거. 블로커는 SBL 자체가 아닌 §3 flash 프로그래밍/설정.

상세(harness 정본): [[jtag_flash_harness]] §8.

---

## 5. route② `.mcelf` standalone 부팅 — 한 번도 실증 안 됨

2026-06-05 standalone 부팅 banner(`eta-tx: 8kw-ev-wpt v1.0e00`)는 **현재 route② build/.mcelf 이미지와 다른 이전 이미지의 증거**:

- 2026-06-05 banner: `eta-tx: 8kw-ev-wpt v1.0e00` ([[jtag_flash_harness]] §4).
- 현재 `src/main.c`:45: `"eta-tx: 8kw-ev-wpt start"` — banner 문구 다름.

→ route② build/.mcelf로 standalone 부팅이 성공한 실적은 **아직 없음**. 진짜 VCC 제거 후 SBL boot profile + app banner가 나오는 것이 미실증 게이트.

> ⚠️ 2026-06-05 banner를 현재 이미지의 부팅 실적으로 전용하지 말 것.

---

## 정정 후보 (미수정)

- **[[jtag_flash_harness]] §4 banner 문구**: `eta-tx: 8kw-ev-wpt v1.0e00`는 구 이미지 기준. 현재 `src/main.c`:45는 `"eta-tx: 8kw-ev-wpt start"`.
- **`tools/gui/gui.py`:553 SW1 라벨**: `"SW1=OSPI (DevBoot 0,1,0,0)"` 표기는 OSPI(4S)=`1,1,1,1`과 DevBoot=`0,1,0,0`을 한 줄에 혼용 — 별개 모드임을 명확히 해야 오해 없음.

---

## 함께 보기

- 토글-프리 루프 전체 맥락: [[toggle_free_flash_loop]]
- JTAG flash 굽기 정본(SBL provenance §8 포함): [[jtag_flash_harness]]
- OSPI RESET·QE bit 핸드오프: [[sbl_app_flash_handoff]]
- ROM boot flow 원문: [[am263p_trm]] §5.4.1 (`ch05_initialization.md`:877·:133·:757)
- UART5 텔레메트리 (독립 부팅 증거 채널): [[uart5_packet_protocol]] · [[pc_monitor_gui]]
