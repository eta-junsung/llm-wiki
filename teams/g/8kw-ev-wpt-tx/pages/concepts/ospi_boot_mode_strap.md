---
tags: [concept, boot, ospi, bootmode, strap, sw1, sfdp, octal, am263p, 8kw, resolved]
source: 실측 (2026-06-12, 8kw-ev-wpt-tx 실보드 — VCC 전원사이클 후 완전 부팅) + 문서조사 (AM263P TRM §5.4.1·LP-AM263P UG §2.1.3·IS25LX256 데이터시트)
date: 2026-06-12
---

# OSPI 부팅 — 부트모드 핀 스트랩 미스매치가 standalone 무부팅의 진짜 원인 (해소)

> **8kw-ev-wpt-tx 정본 — standalone OSPI 무부팅 해소.** 수개월간 "flash 프로그래밍 / cell 영속성 / QE bit NV"로 의심하던 축은 **전부 엉뚱한 축이었다**. 진짜 원인은 **SW1 부트모드 스트랩과 보드 flash 칩 프로토콜의 미스매치**다.
> 한 줄: **보드 flash(IS25LX256)는 octal-only인데, SW1=`1,1,1,1`(OSPI 4S Quad)은 ROM이 `0x6B`+QE를 기대 → octal 칩이 디코드 못 함 → ROM read 실패 → UART fallback `'C'` ping.** SW1을 **`0,0,1,1`(xSPI 8D SFDP)** 로 바꾸자 **진짜 VCC 전원사이클 후 완전 부팅**.

---

## 1. 결론 (실측 FACT, 2026-06-12)

| 항목 | 값 |
|------|-----|
| **잘못된 strap** | SW1 = `1,1,1,1` = **OSPI (4S) Quad Read** — ROM이 `0x6B` + QE bit NV SET 기대 |
| **올바른 strap** | SW1 = `0,0,1,1` = **xSPI 8D (SFDP)** — ROM이 SFDP(JESD216) 읽어 read cmd 자동 결정 |
| **실측 부팅 시퀀스** | (VCC 완전 제거 후 재인가) SBL → `"Image loading done, switching to application"` → app → `eta_pwm_init`(EPWM2/4/7 85 kHz) → `eta-tx: 8kw-ev-wpt start` |

⟹ standalone 무부팅은 **해소(FACT)**. 잔여 블로커였던 "flash 프로그래밍/설정"은 **존재하지 않았던 문제**였음(아래 §4).

> ⚠️ **standalone 부팅 검증은 물리 VCC 전원사이클 필수**: JTAG 리셋(connect GEL이 코어 리셋)으로는 검증 불가 — ROM이 실행되지 않아 SBL 로드 경로를 통과하지 않는다. 반드시 **USB 물리 뽑기(VCC 완전 제거) → 재인가**로 검증.

---

## 2. 왜 `1,1,1,1`(4S Quad)이 이 보드에서 물리적으로 불가능한가

### 보드 flash = IS25LX256 = octal-only

- 보드 부트 flash = **ISSI IS25LX256** (256 Mb, ISSI). 데이터시트상 지원 프로토콜은 **Extended SPI(1S-xy-xy) + Octal DDR(8D-8D-8D) 둘뿐** — [[is25lx256_datasheet]] (요약 ch04 / `raw/IS25LX256/ch04_xspi_signal_protocol.md`).
- **이 칩에는 quad(4S) 모드·`0x6B` Quad Output Fast Read 명령·QE(Quad Enable) bit이 물리적으로 없다.**
  - 근거: `raw/IS25LX256/` 전 챕터(ch00~ch11) grep — `quad` / `0x6B` / `6Bh` / `Quad Enable` / `QE bit` **0건**.
  - 보강: SDK flash descriptor `IS25LX256.json`(p114·p444 = `null`, `enableType=0`) — quad 진입/QE 핸들링 자체가 비어 있음 [추정: 사용자 보고, descriptor 직접 미열람].

### ROM이 4S에서 기대하는 것 (칩에 없는 것)

TRM `raw/am263p_trm/ch05_initialization.md` §5.4.1.3.1 (OSPI 4S Bootloader):
- **ROM 4S 명령 = `0x6B`** (`ch05:749` — "Command issued by ROM in this mode is 0x6B").
- **ROM은 QE bit가 NV config에 SET 돼 있길 기대** (`ch05:757` — "RBL also expects the QE bit is SET in non-volatile configuration so that flash is active in quad mode by default after POR").
- Table 5-1 Note 2 (`ch05:139`): **"4S boot is supported on Flash memories that support 0x6B."**

⟹ octal-only IS25LX256은 `0x6B`을 디코드하지 못함 → ROM이 SBL 이미지를 읽는 데 실패 → "any failures"면 **UART fallback** 진입 → COM4(UART0)에 `'C'`(0x43) XMODEM ping 무한 반복. **이것이 수개월간의 "무부팅" 증상과 정확히 일치** ([[ospi_boot_console_diagnostic]] §2 triage).

### 올바른 경로 — xSPI 8D (SFDP)

Table 5-1 xSPI(1S→8D) 행 (`ch05:138`): *"ROM configures OSPI controller in xSPI 8D mode, Reads SFDP table for read command and downloads image... Flashes with SFDP are of JEDEC standard Rev D only supported."* IS25LX256은 JEDEC xSPI/SFDP 호환([[is25lx256_datasheet]]) → ROM이 SFDP에서 read 명령을 자동 결정하므로 **고정 `0x6B`/QE 의존이 없는 정식 octal 경로**.

> 참고: OSPI(8S) Octal Read(SW=`1,1,0,0`)도 octal이지만 고정 명령 `0x8B`(`ch05:136`)을 쓴다 — 칩이 `0x8B`을 지원해야 함. 이번에 실증된 건 **xSPI 8D SFDP(`0,0,1,1`)** 경로다. 8S 경로는 미시도.

---

## 3. SW1 스위치 극성 — UG 표는 TRM SOP값의 비트반전 (혼동 주의)

부트모드 핀은 두 표기 체계가 있고 **서로 비트반전**이라 라벨 혼동이 잦다 (이번 무부팅 누적의 한 원인).

- **스위치 ON = SOP 핀을 1 kΩ로 GND pull = SOP 논리 `0`** — UG §2.1.3 Note (`raw/lp_am263p_ug/ug_lp-am263p.md:453`).
- 따라서 **UG 스위치표(Table 2-5, `:463-471`)** 의 값은 **TRM SOP 표(Table 5-2, `ch05:498-508`)** 값의 논리 반전.

| Boot mode | UG SW1.4·3·2·1 (Table 2-5) | TRM SOP3·2·1·0 (Table 5-2) |
|-----------|---------------------------|----------------------------|
| OSPI (4S) Quad Read | `1 1 1 1` | `0 0 0 0` |
| UART | `1 1 1 0` | `0 0 0 1` |
| OSPI (1S) Single Read | `1 1 0 1` | `0 0 1 0` |
| OSPI (8S) Octal Read | `1 1 0 0` | `0 0 1 1` |
| DevBoot | `0 1 0 0` | `1 0 1 1` |
| **xSPI 8D (SFDP)** | **`0 0 1 1`** | `1 1 0 0` |

(컬럼 순서는 UG 표기 그대로 SW1.4 / SW1.3 / SW1.2 / SW1.1. 부트모드 설명은 UG Table 2-6 `:489-494`.) **이 보드의 정답 = xSPI 8D (SFDP) = SW1 `0,0,1,1`.** 단일 소스: lp-am263p [[CLAUDE]] "하드웨어 — 부트 모드".

---

## 4. 무효가 된 종전 가설들 (재시도 금지)

이번 발견 이전 [[ospi_boot_console_diagnostic]] §3·[[toggle_free_flash_loop]] §③·[[jtag_flash_harness]] §8이 잔여 블로커로 지목하던 것들은 **전부 strap 미스매치라는 잘못된 전제 위에 쌓여 있었다**:

| 폐기된 가설 | 왜 무효인가 |
|-------------|------------|
| (a) flash cell 영속성 — flashwriter가 cell에 NV 커밋 못 했다 | 굽기는 정상이었음. ROM이 못 읽은 건 cell이 비어서가 아니라 **잘못된 명령(`0x6B`)을 보냈기 때문**. strap 교정만으로 같은 flash 내용이 정상 부팅. |
| (b) QE bit NV SET 안 됨 | **이 칩에 QE bit 자체가 없다**(§2). "QE를 SET해야 4S가 산다"는 명제는 이 보드에 적용 불가 — 애초에 4S로 부팅하면 안 되는 칩. |
| "SBL 파일이 잘못됐다" | 이미 byte-identical로 제거됨([[ospi_boot_console_diagnostic]] §4). strright strap에서 그 SBL이 정상 부팅. |
| ">128Mb warm-reset 4-byte stuck"이 부팅 블로커 | §③ silicon 사실 자체는 유효하나(full POR만 해소), 이번 무부팅의 **원인은 아니었음** — VCC 완전 제거 상태에서도 `1,1,1,1`이면 못 부팅. 원인은 strap. |

> ⚠️ "굽기 ✓ / 부팅 ✗"의 ✗ 절반은 **flash 프로그래밍 결함이 아니라 부트모드 스트랩 오설정**이었다. 굽힌 이미지는 정상이었다.

---

## 5. 코드/툴 반영 (이번 세션)

- `tools/gui/gui.py`·`tools/jtag_flash/flash_8kw.js`의 **SW1 라벨을 `0,0,1,1`(xSPI 8D SFDP)로 수정** (이번 세션). 종전 라벨(`1,1,1,1` 또는 DevBoot 혼용)이 잘못된 mental model을 강화하고 있었음.

---

## 6. 사실 / 가설 / 모름

- **FACT**: IS25LX256 octal-only(quad/`0x6B`/QE 부재) · ROM 4S는 `0x6B`+QE 기대 · SW1 `0,0,1,1`(xSPI 8D SFDP)에서 VCC 전원사이클 후 완전 부팅 실측.
- **FACT**: 종전 "flash 프로그래밍/QE/cell 영속성" 블로커 가설 무효.
- **모름/미확인**: 이전 기록(2026-06-05 banner 등)이 "SW1=`1,1,1,1`(OSPI 4S)에서 부팅했다"고 적은 것은 **octal-only 칩에서 물리적으로 불가** → 당시 strap 라벨 식별이 틀렸을 가능성이 큼([추정]). 실제 06-05에 물리 스위치가 어디였는지는 미확정 → [[jtag_flash_harness]] §4·[[toggle_free_flash_loop]] §③에 모순으로 표시.
- **모름**: OSPI(8S) `0x8B` 경로(SW=`1,1,0,0`)로도 부팅 가능한지 — 미시도.

---

## 함께 보기

- 부팅 진단 채널·triage recipe·종전 블로커 정정: [[ospi_boot_console_diagnostic]]
- 토글-프리 루프(굽기 ✓ / 부팅 — strap 교정으로 해소): [[toggle_free_flash_loop]]
- JTAG flash 굽기 정본(SBL provenance 포함): [[jtag_flash_harness]]
- 보드 flash 칩 octal-only 사실: [[is25lx256_datasheet]] · 포팅 시 Spansion↔ISSI 프로토콜 차이: [[is25lx256_vs_spansion_quirks]] §4
- SW1 부트모드 단일 소스: [[CLAUDE]] "하드웨어 — 부트 모드 / boot flow"
- TRM 원문: [[am263p_trm]] §5.4.1 (`ch05_initialization.md`:138·:139·:498-508·:749·:757·:761) · UG: [[lp_am263p_ug]] §2.1.3 (`:453`·`:463-471`·`:489-494`)
- ⚠️ 별개 층위(혼동 금지) — cc3351 런타임 app `Flash_open()` 블로커: [[flash_open_facts]] · [[sbl_app_flash_handoff]]
