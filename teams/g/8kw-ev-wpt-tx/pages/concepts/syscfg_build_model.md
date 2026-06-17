---
tags: [concept, build, syscfg, sysconfig, ccs, gmake, am263p, 8kw-ev-wpt-tx]
source: 코드 분석 (2026-06-17, 8kw-ev-wpt-tx cleanup 브랜치 — SYSTEM_FLAG 분기·stub emit 실측)
date: 2026-06-17
---

# SysConfig 생성물 빌드 의존 모델 (CCS managed build vs 수제 gmake)

> **8kw-ev-wpt-tx 정본.** CCS IDE 빌드(`Release/`)와 GUI 수제 gmake 빌드(`build/`) — 두 갈래가 **동일한 `example.syscfg` 하나**를 입력으로 쓰는데, 생성물 처리 방식이 달라 함정이 여럿 있다.

---

## 1. 두 빌드 갈래

| 빌드 경로 | 트리거 | SysConfig 실행 시점 | 생성물 위치 |
|-----------|--------|---------------------|-------------|
| CCS IDE (managed build) | CCS Build 버튼 | **pre-build 자동** — `.syscfg` mtime이 기존 생성물보다 새롭거나 clean이면 재생성 | `Release/syscfg/` |
| 수제 gmake (`build/makefile`) | 터미널 `make` | **SYSTEM_FLAG=true(기본)**: 생성 스킵, 커밋된 `build/generated/` 그대로 사용 / **false**: `syscfg` 타겟이 SysConfig CLI 재생성 | `build/generated/` |

두 갈래 모두 repo 루트 **`example.syscfg` 하나**를 SysConfig 입력 소스로 쓴다.

- **CCS**: managed-build가 소스트리를 자동 탐색해 `example.syscfg`를 발견한다. `Release/subdir_rules.mk`가 내부에서 `--script .../example.syscfg` CLI를 호출.
- **수제 gmake**: `SYSCFG_NODE`·`CLI_PATH`·`SDKPRODUCT` 변수를 SDK `imports.mak`에서 자동 참조 — 별도 배선 불필요.

---

## 2. SYSTEM_FLAG 분기 (수제 gmake)

```
make                     # SYSTEM_FLAG=true(기본) → build/generated/ 그대로 사용
make SYSTEM_FLAG=false   # syscfg 타겟 실행 → SysConfig CLI 재생성
```

`SYSTEM_FLAG=true`(기본)는 "동결된 선행조건" 모드다. SysConfig CLI가 없거나 버전이 다른 환경에서도 빌드할 수 있도록, 커밋된 `build/generated/`를 그대로 쓴다.

---

## 3. 함정

### ① generated/ gitignore 금지 — 수제 gmake 기본 모드의 필수 조건

수제 gmake `SYSTEM_FLAG=true` 기본 모드는 **`build/generated/`가 repo에 커밋돼 있어야** 작동한다. `generated/`를 "자동생성 부산물이니 통째 ignore"하면 깨끗한 clone에서 컴파일 실패 또는:

```
No rule to make target 'syscfg'
```

**`generated/`의 `.c`·`.h`·`.cmd`는 "재생성 안 하는 동결 선행조건"으로 취급하고 git 추적을 유지한다.** `.o`·`.d`·`.a`(빌드 산출물)만 ignore.

### ② SysConfig은 미사용 모듈도 stub emit

SysConfig은 `.syscfg`에서 활성화하지 않은 모듈도 **빈 stub 파일을 항상 emit**한다.

예: `enet`·`sdl` 미사용인데도:
- `ti_enet_config.c` — 함수 본문 0줄
- `ti_sdl_config.c` — `void Sdl_config(void) {}`

"안 쓰는데 파일이 생겼다" → "다른 `.syscfg`를 쓰는 건 아닌가" 오진 금지. **동일 입력 + 동일 버전이면 생성물 내용은 byte-identical**이다.

### ③ CCS vs gmake 최종 바이너리 비동일 — 기능은 동일

| 항목 | CCS IDE | 수제 gmake |
|------|---------|------------|
| stub 파일 링크 여부 | 포함 (inert 심볼) | 제외 |
| 최종 `.out` 바이너리 | stub 심볼 포함 | 없음 |
| 기능 동작 | 동일 | 동일 |

두 경로의 `.out`은 byte-identical이 아니다 — inert 심볼 포함 여부 차이. 실보드 기능 동작 차이는 없다.

---

## 4. TI 경로 하드코딩과 환경 이식성

### CCS managed build (`Release/`)

`Release/makefile`·`Release/subdir_rules.mk`는 CCS가 **로컬 절대경로**(`C:/ti/ccs2050/...`, `C:/Users/.../...`)를 박아 생성한다 — git 추적 안 함(`.gitignore`). 다른 노트북에서 git clone 후 바로 make하면 깨진다.

→ **CCS로 프로젝트 import**(= 로컬 경로로 makefile 재생성) 후 빌드.

### 수제 gmake (`build/`)

`build/config.mk`에 TI 경로가 하드코딩되어 있다. 다른 설치 경로에서는 **3줄 `?=` env override**로 재정의 가능:

```makefile
# config.mk 상단 (기본값은 하드코딩, 환경변수로 override)
TI_DIR         ?= C:/ti
CCS_DIR        ?= $(TI_DIR)/ccs2050/ccs
SDK_DIR        ?= $(TI_DIR)/mcu_plus_sdk_am263px_26_00_00_01
```

shell에서 `TI_DIR=C:/custom/ti make`처럼 env로 넘기거나 `config.mk` 3줄만 수정하면 된다.

`run.bat`·`tools/ospi_flash/` 내부 TI 경로(`C:/ti/ccs2050/...`)는 별도 하드코딩 2자리가 있다 — env override 범위 밖이라 직접 수정 필요 (README §최초 1회 셋업 참고).

### eta_tuning.h — syscfg 재생성 불요 경로

`eta_tuning.h` 변경(dead-time 상수 등)은 순수 C 컴파일로 반영 — syscfg 재생성 불요. 이것이 런타임 override 방식의 이점([[status]] §빌드 환경 주의 참고).

---

## 함께 보기

- flash 툴링 메커니즘 + mcelf 소스 분기: [[ospi_flash_tooling]]
- CCS IDE 종료 규율 (flash 전 전제 조건): [[jtag_flash_clean_host]]
- OSPI 부트 플로우: [[ospi_boot_mode_strap]]
- 현재 위치·다음 시작점: [[status]]
