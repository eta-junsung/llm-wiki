---
tags: [concept, architecture, firmware, layering, 8kw-ev-wpt-tx]
source: 펌웨어 repo PR #5 (feature/firmware-layering, 0830b5f·9cd0181, 2026-06-25)
date: 2026-06-25
subsystem: 8kw-ev-wpt-tx
---

# 펌웨어 4레이어 아키텍처 (BSP / HAL / ALG / App)

PR #5 (`feature/firmware-layering`, commits `0830b5f`·`9cd0181`)에서 전면 재구성. 동작 불변(순수 재구성), 실보드 검증 통과.

---

## 레이어 정의

| 레이어 | 디렉토리 | 책임 | 현재 모듈 |
|--------|----------|------|-----------|
| **BSP** | `src/bsp/` | 부팅 1회 init · 레지스터 직접 접근 · IOMUX 설정 | eta_bsp_iomux, eta_bsp_adc, eta_bsp_pwm, eta_bsp_gpio, eta_bsp_uart |
| **HAL** | `src/hal/` | 동작 중 SDK 래핑 (`ADC_`/`EPWM_`/`GPIO_`/`UART_`) · read/write | eta_hal_adc, eta_hal_gpio, eta_hal_uart |
| **ALG** | `src/alg/` | 순수 계산 (하드웨어 무관, host에서도 돎) | eta_alg_crc, eta_alg_convert |
| **App** | `src/app/` | 오케스트레이션 · 레이어 간 접착 | main (진입점), eta_app_adc, eta_app_protocol, eta_app_io |

---

## 불변식 (의존 방향)

```
App
 ├── BSP   (init 호출, 레지스터 tuning knob 읽기)
 ├── HAL   (runtime read/write)
 └── ALG   (순수 계산)

HAL ──→ SDK (TI DriverLib)
BSP ──→ SDK (TI DriverLib) · 레지스터

ALG ──→ (없음: 하드웨어 독립)
```

**ALG는 HAL·SDK·레지스터를 절대 모른다.** HAL과 ALG가 만나는 자리는 App뿐.

---

## 네이밍

전사 네이밍 표준은 [[firmware_naming_conventions]]로 위임 — 여기엔 **레이어드 한정 규칙**만 둔다.

| 대상 | 패턴 | 예시 |
|------|------|------|
| 함수 | `eta_<layer>_<module>_<verb>()` | `eta_hal_adc_read()`, `eta_alg_crc16()` |
| 파일 | `eta_<layer>_<module>.c/.h` | `eta_bsp_pwm.h`, `eta_hal_uart.c` |
| 진입점 | `main()` 예외 (C 진입점, prefix 없음) | `src/app/main.c` |

**레이어 토큰 기준(결정2, [[firmware_naming_conventions]] §4)**: 레이어 경계를 넘는 공개·공유 식별자는 모듈만(`eta_adc_ch_t`/`ETA_PKT_*`), 한 레이어 내부 전용만 레이어 토큰 포함(`eta_bsp_adc_inst_t`/`ETA_HAL_GPIO_*`). 근거 = `gpio`가 bsp·hal 양쪽 존재(모호성 해소) + 외부식별자 31자 예산(MISRA 5.1) 보호.

---

## 하드웨어 종속 산술 배치 원칙

- **duty→CMP 등 HW 종속 산술**: HAL/BSP 내부에 위치. ALG는 비율(0~1) 또는 물리 단위 스칼라만 다룸.
- **PWM tuning knob** (deadtime 등 컴파일타임 상수): `src/bsp/eta_bsp_pwm.h` — `ETA_BSP_PWM_DEADTIME_NS` 단일 소스.
- **ALG의 현재 계산**: `eta_alg_convert` (raw→mV, `raw*3300/4095`), `eta_alg_crc16` (CRC-16/CCITT-FALSE). 이것이 전부 — 의도적.

---

## ALG 레이어가 비어있는 이유

제어/보호 로직은 아직 미착수이므로 ALG 레이어가 거의 비어있는 것이 **정상 상태**다.

빈 경계가 채워지는 시점:

| 경계 | 진입 조건 |
|------|-----------|
| `eta_alg_control` (PI 제어) | P3 보호 스펙 + A3 스케일링(센서 스펙) 입수 후 |
| `eta_hal_pwm` (런타임 duty write) | 위와 동일 |

GUI 물리량 변환(GA_Vin·GA_Iin·NTC) 펌웨어 회수도 A3 스펙 대기로 보류 — 현재 `gui.py`의 `PHYSICAL_COEFF` 단일 소스 유지([[pc_monitor_gui]]).

---

## GUI↔펌웨어 비자명 결합 (⚠️ 변경 시 주의)

`gui.py`는 `src/bsp/eta_bsp_pwm.h`의 `ETA_BSP_PWM_DEADTIME_NS`를 **regex로 직접 편집**한다 (`write→build→flash` 시퀀스).

**결합 지점**: `gui.py:74` — `ETA_BSP_PWM_DEADTIME_NS` 패턴을 매칭하는 정규식.

⟹ 이 매크로를 개명하거나 파일을 이동할 경우 **`gui.py:74`를 반드시 함께 갱신**해야 한다. 펌웨어 빌드 그린만으로는 이 회귀를 잡을 수 없다 — **`gui.py --read` 라운드트립으로 확인**할 것.

상세 → [[pc_monitor_gui]] §Dead-time 빌드/플래시 컨트롤.

---

## 검증 기록 (PR #5, 2026-06-25)

| 항목 | 결과 |
|------|------|
| 빌드 | ✓ 그린 (경고 0) |
| CRC16 통합 | ✓ 중복 구현 → `eta_alg_crc16` 단일, 동일 다항식·init 확인 |
| raw→mV 상수 | ✓ 불변 (`raw*3300/4095`) |
| 실보드 (XDS110 JTAG) | ✓ ADC 0V/3.3V 인가→GUI 표시 / gd_en_seed 버튼→GPIO93 Logic2 확인 / PWM deadtime 250ns·400ns write→build→flash PASS / 디스어셈블로 deadtime 값 바이너리 박힘 확인 |

---

## 관련

- [[status]] — 현재 위치·다음 시작점
- [[roadmap]] — 레이어링이 전체 호에서 어디에 앉는지
- [[pc_monitor_gui]] — GUI↔펌웨어 결합(deadtime regex) 상세
- [[adc_scaling]] — ALG 계산 중 물리량 변환 현황
- [[uart5_packet_protocol]] — ALG CRC-16 사용 컨텍스트
