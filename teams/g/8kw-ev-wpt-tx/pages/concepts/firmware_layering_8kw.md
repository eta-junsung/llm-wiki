---
tags: [concept, architecture, firmware, layering, 8kw-ev-wpt-tx]
source: 펌웨어 repo PR #5 (feature/firmware-layering, 0830b5f·9cd0181, 2026-06-25)
date: 2026-06-30
subsystem: 8kw-ev-wpt-tx
---

# g-8kw 레이어드 아키텍처 적용 (BSP/HAL/ALG/App)

전사 아키텍처 표준 [[firmware_layering]]의 **g-8kw 구체 적용**. 레이어 정의·의존 불변식·배치 규칙은 표준으로 위임 — 여기엔 이 프로젝트의 **모듈 인스턴스·빈 경계·GUI 결합·검증 기록**만 둔다.

PR #5 (`feature/firmware-layering`, commits `0830b5f`·`9cd0181`)에서 전면 재구성. 동작 불변(순수 재구성), 실보드 검증 통과.

---

## 현재 모듈 (`src/{bsp,hal,alg,app}/`)

| 레이어 | 모듈 |
|--------|------|
| **BSP** | eta_bsp_iomux, eta_bsp_adc, eta_bsp_pwm, eta_bsp_gpio, eta_bsp_uart |
| **HAL** | eta_hal_adc, eta_hal_gpio, eta_hal_uart |
| **ALG** | eta_alg_crc, eta_alg_convert, eta_alg_iir_lpf |
| **App** | main (진입점), eta_app_adc, eta_app_protocol, eta_app_io |

---

## ALG 의도적 비어있음 + 빈 경계 채워지는 시점

제어 로직 미착수이므로 ALG가 거의 비어있는 것이 **정상 상태**(표준 §4). 현재 ALG = `eta_alg_convert`(raw→mV, `raw*3300/4095`)·`eta_alg_crc16`(CRC-16/CCITT-FALSE)·`eta_alg_iir_lpf`(Io 2차 biquad LP, 2026-07-01 구현 완료, 정본 [[io_iir_lpf]])뿐 — 의도적.

| 빈 경계 | 진입 조건 |
|---------|-----------|
| `eta_alg_control` (PI 제어) | 제어루프(P4) 진입 + A3 스케일링(센서 스펙) 입수 후 |
| `eta_hal_pwm` (런타임 duty write) | 위와 동일 |

GUI 물리량 변환(GA_Vin·GA_Iin·NTC) 펌웨어 회수도 A3 스펙 대기로 보류 — 현재 `gui.py`의 `PHYSICAL_COEFF` 단일 소스 유지([[pc_monitor_gui]]). 현황 → [[adc_scaling]].

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

- [[firmware_layering]] — 전사 아키텍처 표준 (레이어 정의·불변식·배치 규칙)
- [[firmware_naming_conventions]] — 식별자 네이밍 표준 (레이어 토큰 §4)
- [[status]] — 현재 위치·다음 시작점
- [[roadmap]] — 레이어링이 전체 호에서 어디에 앉는지
- [[pc_monitor_gui]] — GUI↔펌웨어 결합(deadtime regex) 상세
- [[adc_scaling]] — ALG 계산 중 물리량 변환 현황
- [[uart5_packet_protocol]] — ALG CRC-16 사용 컨텍스트
- [[io_iir_lpf]] — ALG `eta_alg_iir_lpf` biquad LP 스펙·구현 기록
