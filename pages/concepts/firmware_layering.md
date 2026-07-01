---
tags: [concept, architecture, firmware, layering, convention, living-doc]
source: conversation-2026-06-30 (전사 아키텍처 표준 승격 — g-8kw 4레이어 de-facto 일반화) + g-8kw PR #5 (feature/firmware-layering, 2026-06-25); conversation-2026-07-01 (c팀 oled_tv 02_rx_esb/_shared 리뷰 환원 — 계약 헤더 위생 리트머스)
date: 2026-07-01
---

# 펌웨어 레이어드 아키텍처 표준 (전사 공통)

모든 팀·프로젝트 공통. eta 펌웨어가 신규 코드에 적용하는 레이어 구조 표준. 짝 표준 = [[firmware_naming_conventions]](식별자), [[firmware_git_workflow]](git). 단일 프로젝트 결정이 아니라 회사 아키텍처 표준이다.

> **한 줄 정의: 펌웨어를 BSP / HAL / ALG / App 4레이어로 나누고, 의존은 App → {BSP, HAL, ALG} 단방향, ALG는 하드웨어를 절대 모른다.**

선례·추출원: g-8kw-ev-wpt-tx 풀 4레이어 적용([[firmware_layering_8kw]], PR #5). 이 표준은 그 구조를 플랫폼 무관하게 일반화한 것.

> **전사 skill 배포 (2026-07-01)**: 이 페이지 + [[firmware_naming_conventions]]에서 추출한 Claude skill **`eta-firmware-conventions`**가 플러그인으로 배포됨 — `eta/eta-ai-tools/eta-firmware-conventions`(`.claude-plugin/plugin.json` + `skills/eta-firmware-conventions/{SKILL.md, references/layering.md, references/naming.md}`). 펌웨어 C **작성**(레이어 배치→네이밍 순 안내)·**리뷰**(규약 위반 점검)를 양방향으로 수행. 범위 제외 = git workflow([[firmware_git_workflow]]). **이 위키 두 페이지가 정본 단일 소스** — 표준이 바뀌면 SKILL.md·references를 재동기화한다(정본→skill 단방향). ⚠️ SKILL.md "출처" 경로가 타 머신 기준(`/Users/jun/eta/wiki/...`)이라 재동기화 시 실제 경로(`/home/eta-junsung/eta/wiki/...`) 확인 필요.

---

## 0. 왜 레이어드인가 (목적)

- **테스트 가능성**: ALG(순수 계산)는 하드웨어 없이 host에서 그대로 돈다 — 단위 테스트·검증 가능.
- **이식성**: MCU·SDK 교체 시 BSP/HAL만 바꾸면 됨. App·ALG는 불변.
- **격리**: 벤더 SDK 의존이 HAL/BSP 한 곳에 갇힘 — SDK 함정이 전역 전파 안 됨.
- **변경 국소성**: 제어 로직(ALG)과 하드웨어 접근(HAL/BSP)이 섞이지 않아 회귀 면적이 좁다.

---

## 1. 레이어 정의 (책임 · 의존 · 무엇이 들어가나)

| 레이어 | 책임 | 의존 | 들어가는 것 |
|--------|------|------|-------------|
| **BSP** (Board Support) | 부팅 1회 init · 레지스터 직접 접근 · IOMUX/핀먹스 · 컴파일타임 tuning knob | SDK · 레지스터 | clock/iomux/adc/pwm/gpio/uart init, `*_DEADTIME_NS` 등 knob |
| **HAL** (HW Abstraction) | 동작 중 SDK 래핑 (read/write) | SDK | runtime `read()`/`write()`, 핸들 관리 |
| **ALG** (Algorithm) | 순수 계산 (하드웨어 무관, host에서도 돎) | **없음** | 제어(PI)·변환(raw→물리)·CRC·필터 |
| **App** (Application) | 오케스트레이션 · 레이어 간 접착 · 진입점 | BSP · HAL · ALG | `main()`, 모듈별 `*_loop()`, 프로토콜 조립 |

---

## 2. 불변식 (의존 방향) — 하드룰

```
App
 ├── BSP   (init 호출, 레지스터 tuning knob 읽기)
 ├── HAL   (runtime read/write)
 └── ALG   (순수 계산)

HAL ──→ SDK (벤더 DriverLib)
BSP ──→ SDK · 레지스터
ALG ──→ (없음: 하드웨어 독립)
```

- **R1. ALG는 HAL·SDK·레지스터를 절대 모른다.** HAL과 ALG가 만나는 자리는 **App뿐**.
- **R2. 의존은 단방향** — 하위 레이어가 상위(App)를 호출 금지, 순환 의존 금지.
- **R3. SDK 식별자(`ADC_`/`EPWM_`/PascalCase)는 HAL/BSP 안에만** — App·ALG는 SDK를 직접 보지 않는다. (SDK 경계 격리, [[firmware_naming_conventions]] D2와 짝)

---

## 3. 무엇을 어디에 두나 (배치 결정 규칙)

- **하드웨어 종속 산술**(duty→CMP, raw→레지스터값 등): **HAL/BSP** 내부. ALG는 **비율(0~1)·물리 단위 스칼라**만 다룬다.
- **컴파일타임 tuning knob**(deadtime 등 상수): **BSP 헤더 단일 소스**(예 `eta_bsp_pwm.h`).
- **순수 변환·제어·CRC**: ALG. host에서 도는지가 리트머스 — 안 돌면 잘못 배치된 것.
- 헷갈리면 "이 코드가 MCU 없이 PC에서 컴파일·실행되나?"로 판정 → 되면 ALG, 안 되면 HAL/BSP.

### 3.1 계약/공유 헤더 위생 (레이어 누출 리트머스, 2026-07-01)

와이어 프로토콜처럼 여러 레이어·여러 노드가 함께 include하는 **계약 헤더**(패킷 구조체·필드·매크로 정의)에도 host 리트머스를 헤더 단위로 좁혀 적용한다: **"이 헤더가 host 빌드에서도 서나?"**

- 계약 헤더는 순수 직렬화만 담고 **`<stdint.h>` 하나로 서야 한다**.
- `stdio.h`(`printf` 등 표시 로직)가 섞이면 **App** 관심사 누출 — App으로 옮긴다.
- 보드 핀 번호·레지스터 상수가 섞이면 **BSP** 관심사 누출 — BSP 헤더로 옮긴다.
- 쓰지 않는 `stdlib.h`/`math.h` 등 include는 그 자체로 경계가 흐려졌다는 신호 — 제거한다.

---

## 4. 레이어는 비어도 되고, 합쳐도 된다 (4개 강제 아님)

핵심은 **불변식(§2)**이지 레이어 *개수*가 아니다.

- **ALG가 비는 건 정상**: 제어/보호 로직 미착수면 ALG는 거의 빈다. 빈 경계는 스펙 진입 시 채운다.
- **단순 플랫폼은 병합 가능**: BSP+HAL을 한 드라이버 레이어로, ALG 생략 — 2레이어(App + Driver)도 표준 준수로 본다. **단 불변식(ALG성 순수계산이 HW를 모름·의존 단방향)은 유지**.
- 즉 4레이어는 *상한 형태*, 프로젝트 복잡도에 맞춰 축소 가능. 늘리지는 않는다(접두사·경계 폭증).

---

## 5. 네이밍 연결

레이어드 채택 시 식별자에 레이어 토큰을 넣는 규칙은 [[firmware_naming_conventions]] §4 — 공개·공유는 모듈만(`eta_adc_*`), 한 레이어 내부 전용만 레이어 포함(`eta_bsp_adc_*`). 진입점 `main()`은 prefix 예외.

---

## 6. 팀 적용 현황 (정본 baseline = g-8kw)

| 프로젝트 | 적용 형태 | 비고 |
|----------|-----------|------|
| **g-8kw-ev-wpt-tx** | ✓ 풀 4레이어 (레퍼런스) | `src/{bsp,hal,alg,app}/`. 이 표준의 추출원 → [[firmware_layering_8kw]] |
| **c-02_RX_esb** | ◐→▶ 4레이어 전환 진행중 | `feature/layering-02`, SES 빌드 통과(2026-07-01)·실보드 검증 대기. _shared 우산-shim 분할 후 02+_shared 함께 검증 예정. [[nrf52_firmware_conventions]] |
| **c-03_TX_esb** | ◐ 2레이어 (App + Driver) | `eta_protocol` → {`eta_esb`,`eta_spi`,`eta_clock`,`eta_gpio`} 단방향 — 불변식 준수. 02 완료 후 미러 예정. |
| **c-04_TX_control** | ◐ 부분 | 01 골격 복사·단순화(`07fbf1f`). _shared 분할 후 수렴 예정. 실보드 검증 미수행. |
| **c-01_RX_control** | ◐ 부분 | `app_protocol` 응용계층 적출·저수준 분리. _shared 우산 shim 위 유지(4레이어 정합은 별도 결정). [[app_protocol_module]] |

신규 펌웨어는 4레이어(또는 축소형 §4)를 목표로, 기존은 기회적 수렴. c팀은 g-8kw 레퍼런스 형태로 적극 수렴 중(기회적 기본값 아님). 적용 순서: 02→_shared→03→04→01 검토.

---

## 관련

- [[firmware_layering_8kw]] — g-8kw 구체 적용(모듈 인스턴스·빈 경계·gui.py 결합·PR #5 검증)
- [[firmware_naming_conventions]] — 레이어 토큰 네이밍(§4 결정2)·SDK 경계(D2)
- [[firmware_git_workflow]] — 전사 git 표준(짝)
- [[nrf52_firmware_conventions]] — c-nRF52 의존 방향(protocol→drivers)
- [[app_protocol_module]] — c-STM32 응용계층 적출 원형
