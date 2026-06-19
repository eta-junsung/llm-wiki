---
tags: [concept, am263p, epwm, iomux, pinmux, padconfig, platform]
source: 2026-06-09 8kw-ev-wpt-tx PWM P1 Pin1(HS1, EPWM2_A→J4.39) 실보드 검증 — force_io 없이 SysConfig 핀먹스만으로 출력 확인
date: 2026-06-09
---

# AM263P EPWM primary 패드는 force_io_enable 불필요

> **AM263P 플랫폼 지식 정본.** [[am263p_iomux_force_io_enable]]의 **대조 사례**. alt-function으로 빌려 쓰는 패드(UART5=EPWM15)는 force가 필요했지만, 출력이 그 핀의 **primary function**이면 SysConfig 핀먹스만으로 출력 버퍼가 켜진다. 8kw PWM에서 실증.

## 한 줄 요약

**EPWM 출력이 핀의 primary(default mux) function이면 SysConfig pinmux 설정만으로 출력 버퍼가 켜진다 — KICK 언락 + PADCONFIG OE override RMW(force_io_enable)가 불필요.** force가 필요했던 건 UART5처럼 IP default가 buffer-disabled인 **alt-function 패드를 빌려 쓸 때**뿐이다.

---

## 확정 사실 (실보드 검증)

- **근거**: 8kw-ev-wpt-tx PWM P1 Pin1 = **EPWM2_A → J4.39**. EPWM2_A는 J4.39의 **primary(UG Mode0) function** ([[pwm_pinmap]]·[[lp_am263p_ug]] Table 2-28). SysConfig 핀먹스 설정만으로 — **force_io_enable 호출 없이** — J4.39에서 **100 kHz / duty 50% 출력 확인**(Saleae Logic2, 99.997 kHz / 49.998%, n=10223 cycles, 글리치 없음).
- 즉 primary-function 패드는 IP default가 이미 출력 버퍼를 구동하므로 [[am263p_iomux_force_io_enable]]의 OE override RMW가 불필요.

## 언제 force가 필요한가 (대조)

| 경우 | force_io_enable | 사례 |
|------|-----------------|------|
| 출력이 핀 **primary function** | **불필요** (SysConfig 핀먹스만) | EPWM2_A@J4.39 (이 페이지) |
| 출력이 **alt-function**(IP default buffer-disabled 패드를 빌림) | **필요** (KICK 언락 + PADCONFIG OE RMW) | UART5_TXD=EPWM15_A@P15 ([[am263p_iomux_force_io_enable]]) |

- 판별: 해당 핀의 UG 핀먹스 표에서 쓰려는 신호가 **Mode0(primary)인지 alt-mode인지** 확인. primary면 force 생략 가능, alt면 force 의심.
- 안전망: 출력이 안 나오면 [[am263p_iomux_force_io_enable]] §3 force 패턴 적용 후 재측정.

---

## 검증 방법 (재사용 가능) — flash 없이 OCRAM + ccs-debug + Saleae

이 PWM 빌드는 **OCRAM 이미지**라 flash 굽기 없이 핀 출력을 측정할 수 있다:

1. CCS/ccs-debug로 **`loadProgram`(RAM 로드) → `run`**.
2. **코어는 디버그 연결을 끊어도 RAM 이미지를 계속 실행** → 프로브 붙일 동안 PWM 유지.
3. **Saleae Logic2**로 해당 핀(J4.39 등) 측정 — 주파수/duty/글리치.

- flash 경로([[jtag_flash_harness]]) 대비 **반복 빌드-측정 사이클이 빠름**(dead-time build-per-change 튜닝에 유리).
- 측정 시점 함정은 [[am263p_adc_rti_trigger]] §2와 동일 — `loadProgram` 후 **run 통과** 상태에서 측정.

---

## 관련 페이지

- [[am263p_iomux_force_io_enable]] — **대조 정본**: alt-function 패드는 force 필요. 이 페이지(primary는 불필요)와 짝.
- [[pwm_pinmap]] — 8kw PWM 핀맵(EPWM2/4/7). Pin1 검증 출처.
- [[am263p_adc_rti_trigger]] — 측정 시점/ground-truth 함정 형제.
- [[jtag_flash_harness]] — flash-time 경로(이쪽은 OCRAM이라 flash 불요).
- [[lp_am263p_ug]] — 핀먹스 Mode0/alt 표(primary 판별).
