---
tags: [concept, am263p, lp-am263p, gpio, pinmux, debug, reference, platform]
source: LP-AM263P UG SPRUJ85B Table 2-28(J4 pinmux)·Table 2-10(mux)·Table 2-14(I2C) [[raw/lp_am263p_ug/ug_lp-am263p.md]] + MCU+ SDK am263px/pinmux.h + 회로도 [[schematic_lp_am263p]] + 8kw-ev-wpt-tx eta_bsp_gpio/iomux 실측 + PR#11 `2c4ff85`(ISR 디버그 헬퍼 추가) (2026-06-29)
date: 2026-06-29
---

# LP-AM263P J4 디버그 GPIO 핀맵 + 라우팅

> **LP-AM263P 플랫폼 참조 정본.** BoosterPack J4 헤더의 PR0_PRU0_GPIO 핀을 디버그용 범용 GPIO 출력으로 쓸 때의 핀맵·라우팅 게이트(TS3DDR3812 1:2 mux + TCA6416A PRU_MUX_SEL)·점유 현황. 형제: [[lp_am263p_uart_epwm_mux]](U54 UART/EPWM 2:1 mux + U63 IO expander).

## 1. J4 핀맵 (PR0_PRU0_GPIO0/1/2)

근거: UG Table 2-28 ([[raw/lp_am263p_ug/ug_lp-am263p.md]]:1592–1594), Mode7=GPIO 컬럼. SDK `source/drivers/pinmux/am263px/pinmux.h`:242–244 (PIN offset).

| 헤더 핀 | SoC pad (Mode0/alt) | GPIO (Mode7) | PIN offset | 점유 |
|---------|---------------------|--------------|-----------|------|
| **J4.33** | PR0_PRU0_GPIO0 (EPWM25_A) | **GPIO93** | `0x174` | ⚠️ **GD_EN(게이트드라이버 enable) 점유** — 디버그 불가 |
| **J4.32** | PR0_PRU0_GPIO1 (EPWM25_B) | **GPIO94** | `0x178` | ⚠️ 헤더에 신호 안 나옴(아래 빈자리) |
| **J4.31** | PR0_PRU0_GPIO2 (EPWM26_A) | **GPIO95** | `0x17C` | ✓ 디버그 GPIO로 사용 가능(8kw 적용) |

- 셋 다 GPIO0 인스턴스(`CSL_GPIO0_U_BASE=0x52000000`) 뱅크5 bit13/14/15. Mode7=GPIO, force_io 불요(GPIO는 alt-function이 아님 — cf. [[am263p_iomux_force_io_enable]]는 EPWM/primary pad 경우).
- GPIO 설정 패턴: SysConfig GPIO 모듈 없이 **레지스터 직접 RMW**(KICK 언락 → PADCONFIG Mode7 write → 재잠금).

## 2. 라우팅 게이트 — TS3DDR3812 1:2 mux + PRU_MUX_SEL

PR0_PRU0_GPIOx는 SoC에서 헤더로 직결되지 않고 **TS3DDR3812 1:2 mux**를 거친다 (UG:911 "routed to a 1:2 mux (TS3DDR3812RUAR) that selects between ... the Ethernet PHY or the BP headers"):

| PRU_MUX_SEL | mux 선택 (UG Table 2-10 :915–918) |
|---|---|
| **LOW** | Ethernet PHY#2 (Port A↔B) |
| **HIGH** | **BoosterPack 헤더** (Port A↔C) |

→ **BP 헤더로 GPIO를 내보내려면 PRU_MUX_SEL = HIGH 필수.**

**PRU_MUX_SEL = TCA6416A IO expander의 P07 비트(mask 0x80).**
- TCA6416A(U63)는 I2C1 @ 0x20 (UG:1039 Table 2-14, UG:500 "TCA6416ARTWR IO Expander ... through I2C1 bus"; 회로도 [[schematic_lp_am263p]]:25,37 U63=TCA6416 @0x20, mux SEL/EN 구동).
- ★ **P07↔PRU_MUX_SEL 비트 배정·mask 0x80은 UG 본문에 없음**(IO-expander 핀맵은 그림 Figure 2-7 :521). 근거는 **회로도 + 펌웨어**: `src/bsp/eta_bsp_gpio.c`:44 `IO_EXPANDER_I2C_ADDR (0x20U)`, :47 `PRU_MUX_SEL_BIT_MASK (0x80U) /* P07 = PRU_MUX_SEL */`.

## 3. 점유 현황 — GPIO93(J4.33) = GD_EN

J4.33/GPIO93은 8kw에서 **게이트드라이버 enable(GD_EN)**로 이미 점유 → 디버그용 불가:
- `src/hal/eta_hal_gpio.h`:23 `ETA_HAL_GPIO_PIN_GD_EN, /* GPIO93 */`, `eta_hal_gpio.c`:19 `GD_EN_PIN (93U)`.
- `src/bsp/eta_bsp_iomux.c`:53 `GPIO93(GD_EN) → PR0_PRU0_GPIO0, MODE7`; `eta_bsp_gpio.c`:33 `GD_EN_PIN (93U)`, :101/:137 `PRU_MUX_SEL(P07)=HIGH → J4.33/J5.48을 SoC GPIO로 라우팅`.

→ **남는 디버그 GPIO는 J4.31(GPIO95).** PR#11(main `2c4ff85`)에서 BSP에 재사용 ISR 디버그 토글 헬퍼 **`eta_bsp_gpio_debug_isr_high()`** / **`eta_bsp_gpio_debug_isr_low()`** 추가(`src/bsp/eta_bsp_gpio.c`). 능동 호출처 없이 capability만 존재 — 핀=`ETA_BSP_GPIO_DBG_ISR_PIN`=GPIO95=J4.31.

## 4. 사실 / 가설 / 모름 가름

- **사실 (UG·SDK)**: J4.33/32/31 = GPIO93/94/95 Mode7, PIN offset 0x174/0x178/0x17C, TS3DDR3812 1:2 mux(LOW=PHY/HIGH=BP), TCA6416A I2C1@0x20 — 전부 UG/pinmux.h 인용.
- **사실 (회로도+펌웨어)**: PRU_MUX_SEL = TCA6416 P07(mask 0x80). UG 본문 아닌 회로도+`eta_bsp_gpio.c` 근거.
- **사실 (점유)**: GPIO93=GD_EN, J4.31/GPIO95가 가용 디버그 핀.
- **빈자리 (실측으로 드러남 — 봉합 말 것)**: J4.31(GPIO95)·J4.33(GPIO93)은 PRU_MUX_SEL=HIGH로 BP 헤더에 신호 나옴(검증). **그러나 J4.32(GPIO94=PR0_PRU0_GPIO1)는 SoC가 구동해도 헤더에 무신호** — PRU_MUX_SEL 단일 비트가 J4.32를 BP 헤더로 안 보내는 것으로 보임(다른 mux 채널/목적지). **TS3DDR3812 채널 귀속(회로도) 미확인** → J4.32 디버그 출력 쓰려면 회로도 확인 필요.

## 5. 알려진 결함 — eta_bsp_iomux.c GPIO94/95 역할 주석

`src/bsp/eta_bsp_iomux.c`의 GPIO94·GPIO95 역할 주석이 **활성 코드와 뒤바뀐 채 낡아** 있음(PR#11 `2c4ff85` 기준):

- **활성 코드** (`src/bsp/eta_bsp_gpio.c`): GPIO95 = ISR 디버그 토글(`eta_bsp_gpio_debug_isr_high/low()`), `ETA_BSP_GPIO_DBG_ISR_PIN=GPIO95`.
- **iomux.c 주석**: GPIO94·GPIO95 역할이 서로 뒤바뀌어 기술 — iomux 파일만 읽으면 오해 소지.

→ **코드(`eta_bsp_gpio.c`)가 진실, iomux.c 주석은 환원 후보**. 실제 동작은 GPIO95=J4.31이 ISR 토글 핀(검증됨, §3). GPIO94=J4.32는 보드 mux 미라우팅으로 헤더 무신호(§4 빈자리).

---

## 관련 페이지

- [[am263p_adc_repeater_burst]] — 이 GPIO95 핀을 ISR 디버그 토글로 추가한 PR#11의 주요 기능. 리피터 버스트 N=16 적용.
- [[am263p_adc_ppb_averaging]] §제안 검증법 — GPIO95 토글로 ISR 레이트를 스코프 확인 시 PPB COUNT/NSEL/SHIFT readback과 병행 검증.
- [[lp_am263p_uart_epwm_mux]] — U54 UART/EPWM 2:1 mux + U63 TCA6416 IO expander(헤더 mux SEL/EN 구동). 이 페이지의 IO expander 형제.
- [[schematic_lp_am263p]] — U63 TCA6416·TS3DDR3812 mux 결선 근거.
- [[am263p_iomux_force_io_enable]] — EPWM/primary pad의 force_io (GPIO Mode7은 불요).
- [[am263p_trm]] / [[raw/lp_am263p_ug/ug_lp-am263p.md]] — UG Table 2-28/2-10/2-14.
