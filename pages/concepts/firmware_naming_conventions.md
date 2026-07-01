---
tags: [concept, naming, convention, firmware, misra, living-doc]
source: conversation-2026-06-30 (전사 펌웨어 네이밍 표준 수립 — g-8kw-ev-wpt-tx de-facto 추출 + BARR-C:2018 / MISRA C:2012 / Linux·Zephyr 대조 검증)
date: 2026-06-30
---

# 펌웨어 네이밍 컨벤션 표준 (전사 공통)

모든 팀·프로젝트 공통. eta 펌웨어가 앞으로 **모든 저장소**에 적용하는 C 식별자 네이밍 규약. 단일 프로젝트 결정이 아니라 회사 표준이다. (추후 Claude skill로 승급 예정 — 이 페이지가 런타임 단일 소스.)

> **한 줄 정의: MISRA-필수 룰을 하드룰로 깔고, 그 위에 현대 임베디드 합의(snake·모듈접두사·SCREAMING)를 얹되, BARR-C 헝가리안은 의식적으로 빼고 SDK·POSIX 충돌은 문서화된 편차로 다룬다.**

선례·추출원: g-8kw-ev-wpt-tx (`src/{bsp,hal,alg,app}/`, PR #5 레이어링 이후 de-facto). 레이어드 아키텍처 맥락은 [[firmware_layering]].

---

## 0. 왜 이 자리인가 — 두 진영과 우리의 앵커

펌웨어 네이밍은 철학이 대립하는 두 진영으로 갈린다. 우리는 **둘의 합의 코어 + MISRA 필수 + 실무 하이브리드**에 앉는다.

| 진영 | 대표 | 성격 |
|------|------|------|
| 안전·인증 | **BARR-C:2018 / MISRA C:2012** | 헝가리안 `g_`/`p_`/`b_` 의무·루프변수 3자↑·정적분석 강제·감사 대비 |
| 현대 OSS/RTOS | **Linux kernel / Zephyr** | 헝가리안 "brain damaged" 금지·`i`/`j` 권장·typedef 최소·서브시스템 접두사 |

**핵심 사실 — MISRA ≠ BARR-C 헝가리안.** 기능안전 표준(IEC 61508·ISO 26262)이 인용하는 건 *MISRA*지 BARR-C가 아니다. MISRA의 네이밍 규칙은 **충돌·UB 방지**(유일성·예약식별자)일 뿐 헝가리안을 의무화하지 않는다. 오히려 `_t`는 MISRA가 *지적*하는 쪽(POSIX 예약)이다. ⟹ 기능안전을 정조준해도 `p_`/`b_`를 채택할 이유는 없고, `_t`는 "유지 + 편차 문서화"가 정답.

**우리 제품 맥락 (전력전자 + EV 무선충전)**: GA/TX(off-board 충전기, 현 제품) → IEC 61508 우산 / VA/차량측(만들 경우) → ISO 26262 우산. 둘 다 MISRA 권장. 단 **임박한 인증 제품 없음(2026-06-30)** → baseline + 편차원장 단계. 인증 진입 시 §6 전향 노트.

---

## 1. 코어 치트시트 (이것만 봐도 됨)

| 대상 | 패턴 | 예시 |
|------|------|------|
| **조직 접두사** | 모든 *공개* 식별자에 `eta_` / `ETA_` | `eta_adc_read()` |
| 함수 | `eta_<module>_<verb>()` | `eta_adc_read()`, `eta_alg_crc16()` |
| 파일 | `eta_<module>.c/.h` | `eta_pwm.c` |
| 전역변수 (외부링크) | `g_eta_<module>_<name>` | `g_eta_adc_raw` |
| 파일 static (내부링크) | `s_<name>` — `eta_` 생략 | `s_rx_staging`, `s_seq` |
| 지역변수 | snake, 의미명. 루프 `i`/`j`/`k`·`tmp` 허용 | `adc_ready`, `i` |
| 구조체/공용체 타입 | `eta_<module>_<name>_t` | `eta_adc_sample_t` |
| **구조체 필드** | **snake_case** (SDK 1:1 미러 구조체만 camel) | `raw`, `mv` / SDK: `.socNum` |
| enum 타입 | `eta_<module>_<name>_t` | `eta_adc_ch_t` |
| enum 상수 | `ETA_<MOD>_<GROUP>_<NAME>` + sentinel `_COUNT` | `ETA_ADC_CH_GA_VIN`, `ETA_ADC_CH_COUNT` |
| 매크로·컴파일타임 상수 | `ETA_<MOD>_<NAME>` | `ETA_PKT_SOF`, `ETA_PWM_FREQ_HZ` |
| 헤더가드 | `ETA_<MODULE>_H_` | `ETA_ADC_H_` |
| 술어함수 | `is_`/`has_` (질문형) · `clear_` | `eta_adc_is_ready()` |
| ISR 콜백 | `_isr` 접미 | `eta_adc_eoc_isr()` |
| 단위 접미 | 아래 §3 단위표 | `timeout_ms`, `vbus_mv` |

**동사 어휘 (이 외 신규는 합의 후 추가)**: `init`/`deinit` · `read`/`write` · `get`/`set` · `is`/`has` · `clear` · `request` · `loop` · `isr`

**약어 화이트리스트 (이 외 약어 금지 — 늘리려면 이 목록을 편집)**: `adc` `pwm` `gpio` `uart` `dma` · `ch` `pkt` `idx` `cnt` `len` `req` `en` · `tx`/`rx` · `hwi` `soc` `ppb` `eoc` `osint` · `sen` `vin` `iin` · `comm_st`(communication state — c팀 oled_tv 도메인 표준어, `COMM_ST_*`·`comm_state_monitoring` 참조)

---

## 2. 하드룰 — MISRA 필수 (스타일 아님, 위반=결함)

기능안전 readiness의 실체. 정적분석으로 기계 검증 가능해야 한다.

- **R1. 외부 식별자 31자 내 유일** — 외부링크(비 static) 식별자는 **앞 31자 안에서 서로 구별**돼야 한다 (MISRA 5.1, C99 유효길이). 긴 `g_eta_<layer>_<module>_*`·`ETA_<LAYER>_<MODULE>_*`가 예산을 잠식 → **§4 결정2(공개=모듈만)가 이 룰에 직접 복무**.
- **R2. 같은 스코프 구별** — 같은 스코프·네임스페이스에서 식별자 재사용 금지 (MISRA 5.2~5.5). 매크로명과 다른 식별자 충돌 금지.
- **R3. 예약 식별자 금지** — 선행 언더스코어로 시작 금지, 이름 내 `__`(이중 언더스코어) 금지 (C11 §7.1.3, MISRA 21.1/21.2). ⟹ 헤더가드 트레일링 `_H_`는 안전(선행 `_` 아님), `_ADC_H` 같은 선행형은 금지.
- **R4. 표준·SDK 이름 비충돌** — C 키워드·C 표준 라이브러리·벤더 SDK 공개 식별자와 겹치지 않게 (BARR-C 7.1.b). `eta_` 조직 접두사가 1차 방어.

---

## 3. 단위 접미 (Mars Climate Orbiter 룰)

물리량·인덱스는 **단위·역할을 이름에 인코딩**한다. 정수 raw 카운트엔 안 붙임(`raw`).

| 종류 | 접미 | 예시 |
|------|------|------|
| 전압 | `_mv` `_v` | `vbus_mv` |
| 전류 | `_ma` `_a` | `icoil_ma` |
| 시간 | `_ns` `_us` `_ms` `_s` | `deadtime_ns`, `timeout_ms` |
| 주파수 | `_hz` `_khz` | `pwm_freq_hz` |
| 인덱스/개수/길이 | `_idx` · `_cnt` · `_len` | `ch_idx`, `err_cnt`, `pkt_len` |
| 카운터(타이머틱) | `_counts` | `ETA_DEADTIME_COUNTS` |

`_cnt`(변수 카운터)와 enum sentinel `_COUNT`는 다른 맥락 — 충돌 아님.

---

## 4. 레이어드 아키텍처 부록 (결정2 — 레이어 토큰 기준)

프로젝트가 레이어드 아키텍처(예 BSP/HAL/ALG/App, [[firmware_layering]])를 채택할 때만 적용.

- **공개·공유 식별자(레이어 경계를 넘음) = 모듈만**: `eta_adc_ch_t`, `eta_adc_sample_t`, `ETA_PKT_*`, `ETA_ADC_CH_*`
- **한 레이어 내부 전용 = 레이어 토큰 포함**: `eta_bsp_adc_inst_t`, `eta_bsp_adc_eoc_isr()`, `ETA_HAL_GPIO_PIN_*`, 헤더가드 `ETA_BSP_ADC_H_`
- 함수·파일도 동일: 레이어드면 `eta_<layer>_<module>_<verb>()` / `eta_<layer>_<module>.c`

**근거 둘**: ① 같은 모듈이 여러 레이어에 존재함(`gpio`가 `bsp`·`hal` 양쪽) → 레이어 토큰이 실제로 모호성을 해소. ② 공개명을 짧게 유지해 **R1(31자) 예산 보호**. 비레이어드 프로젝트는 레이어 토큰 없이 `eta_<module>_*`만.

---

## 5. 편차 레지스트리 & 의식적 미채택

### 5.1 문서화된 편차 (Deviation) — 인증 시 그대로 증빙

| # | 편차 | 위배 조항 | 근거 | 범위 |
|---|------|-----------|------|------|
| **D1** | typedef `_t` 접미 | POSIX 예약 네임스페이스 (SEI CERT DCL37-C) | 벤더 SDK 전 생태계(TI MCU+·nRF5·CMSIS)가 `_t` 사용 · `eta_` 접두사로 실충돌 사실상 0 · struct tag 전환은 독자 기대·SDK 대칭 깨짐 | 전 프로젝트 |
| **D2** | 벤더 SDK 식별자 미개명 (`ADC_`/`EPWM_`/PascalCase) | R1·R4 외래 | 서드파티 경계 보존(개명 금지) | 전 프로젝트 |
| **D3** | 짧은 루프변수 `i`/`j`/`k`·`tmp` | BARR-C 7.1.e (최소 3자) | 가독성·관례 · Linux/Zephyr 표준 권장 · MISRA 인증 shop도 일상 편차 | 전 프로젝트 |

### 5.2 의식적 미채택 (BARR-C와의 갈림 — 채택 안 함)

- **헝가리안 `p_`(포인터)·`b_`(불리언)** — BARR-C 7.1.k/m이 의무화하나 **채택 안 함**. MISRA 무관 · Linux "brain damaged(컴파일러가 타입을 안다)" · 코드 부재 · 가독성 noise. 포인터는 타입으로, 불리언은 `is_` 술어로 충분. **스코프 큐 `g_`/`s_`만 채택**(전역은 임베디드에서 위험 → 가시성 큐 가치 있음).
- **`#pragma once`** — 비표준 → 표준 `#ifndef` 가드 사용.

---

## 6. 팀 수렴 & 전향 노트

### 6.1 팀별 정합 (정본 baseline = g-8kw de-facto)

| 대상 | 상태 | 비고 |
|------|------|------|
| g-8kw-ev-wpt-tx | ✓ 정본 원형 | `eta_<layer>_<module>` 정연 — 이 표준의 추출원 |
| c팀 nRF52 (02/03) | ✓ 이미 정렬 | `eta_` 접두사 전환 완료 ([[nrf52_module_naming]]). flat→레이어드는 선택 |
| c팀 STM32 (01) | ◐ grandfather | 무접두사·일부 PascalCase(`Monitor_Loop`) = 레거시. **신규 코드부터 적용**, 손대는 김에 기회적 마이그레이션 |

nRF5 SDK `app_*` 충돌은 `eta_`가 근본 해결 — 상세 [[nrf52_module_naming]] · nRF52 코딩 관습은 [[nrf52_firmware_conventions]].

### 6.2 전향 노트 — 특정 제품 인증 진입 시

GA/충전기 → **IEC 61508**, VA/차량측 → **ISO 26262**. 해당 제품의 qualified 정적분석기(LDRA·Polyspace·cppcheck-MISRA)가 규칙셋을 확정한다. 본 표준 = **baseline + 편차원장(§5.1이 증빙)**. 그때 `p_`/`b_`·루프변수 등은 safety plan에 맞춰 조이고 편차를 재평가. **선제 도입은 금물**(임박 제품 없음).

---

## 관련

- [[firmware_layering]] — 레이어드 아키텍처(BSP/HAL/ALG/App)·§네이밍은 이 페이지로 위임
- [[nrf52_module_naming]] — c팀 nRF52 `eta_` 접두사 규칙(SDK 충돌 해결)
- [[nrf52_firmware_conventions]] — c팀 nRF52 코딩 관습(ISR printf 금지 등)
- [[firmware_git_workflow]] — 전사 공통 git 표준(짝 표준)
- [[contributing_template]] — repo-side CONTRIBUTING.md 템플릿(이 표준 링크 대상)
