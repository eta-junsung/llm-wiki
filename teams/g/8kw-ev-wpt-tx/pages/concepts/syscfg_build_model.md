---
tags: [concept, build, syscfg, sysconfig, ccs, gmake, am263p, 8kw-ev-wpt-tx]
source: 코드 분석 + CCS managed-build Phase 2 마이그레이션 실증 (2026-06-19, toolchain-ccs21-sdk2606 브랜치, CCS21/SDK_06/SysConfig1.28/TICLANG5.1.1)
date: 2026-06-19
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

⚠️ **dual-build 공존 함정**: CCS managed-build는 소스트리 전체를 스캔한다. `.cproject` sourceEntries에 `build/generated/` 경로가 남아 있으면 CCS가 gmake용 SysConfig 생성물(`.c`)까지 컴파일해 `Release/build/generated/*.o`를 만들고, 이것이 `Release/syscfg/*.o`의 동일 심볼과 충돌해 링크 에러를 낸다(§ 함정 ④).

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

수제 gmake `SYSTEM_FLAG=true` 기본 모드는 **`build/generated/`가 repo에 커밋돼 있어야** 작동한다. `generated/`를 "자동생성 부산물이니 통째 ignore"하면 깨끗한 clone에서 컴파일 실패:

```
No rule to make target 'syscfg'
```

**`generated/`의 `.c`·`.h`·`.cmd`는 "재생성 안 하는 동결 선행조건"으로 취급하고 git 추적을 유지한다.** `.o`·`.d`·`.a`(빌드 산출물)만 ignore.

---

### ② SysConfig는 미사용 모듈도 stub emit

SysConfig는 `.syscfg`에서 활성화하지 않은 모듈도 **빈 stub 파일을 항상 emit**한다.

예: `enet`·`sdl` 미사용인데도:
- `ti_enet_config.c` — 함수 본문 0줄
- `ti_sdl_config.c` — `void Sdl_config(void) {}`

"안 쓰는데 파일이 생겼다" → "다른 `.syscfg`를 쓰는 건 아닌가" 오진 금지. **동일 입력 + 동일 버전이면 생성물 내용은 byte-identical**이다.

---

### ③ CCS vs gmake 최종 바이너리 비동일 — 기능은 동일

| 항목 | CCS IDE | 수제 gmake |
|------|---------|------------|
| stub 파일 링크 여부 | 포함 (inert 심볼) | 제외 |
| 최종 `.out` 바이너리 | stub 심볼 포함 | 없음 |
| 기능 동작 | 동일 | 동일 |

두 경로의 `.out`은 byte-identical이 아니다 — inert 심볼 포함 여부 차이. 실보드 기능 동작 차이는 없다.

---

### ④ CDT 소스 발견 1차 진실은 sourceEntries — filteredResources는 빌드를 안 막는다

**증상**: `.project` filteredResources에 `build/` 제외 필터를 넣었는데도 `Release/sources.mk` SUBDIRS에 `build/generated`가 잔존하고, "duplicate symbol" 링크 에러가 난다.

**원인**: CDT managed-build의 소스 발견은 `.cproject` **sourceEntries**가 1차 진실이다. `.project` filteredResources는 탐색기 표시·인덱서 레이어일 뿐, 빌드 스캔을 막지 않는다. 루트 `excluding="docs|tools|build"` 설정이 있어도 sourceEntries에 `build/generated`·`build/obj`·`tools/*` 재추가 entry가 남아 있으면 무력화된다.

**해결**: `.cproject` sourceEntries에서 해당 재추가 entry를 **명시적으로 제거**한다. Release configuration만 고치면 Debug configuration이 구스택·구 sourceEntries에 남으므로 양쪽(또는 "All Configurations") 적용 필수. (commit e1aca4f)

---

### ⑤ 컴파일러는 CCS 설치 인스턴스에 종속 — 신 버전은 신 CCS에서만 보인다

**증상**: CCS Properties 컴파일러 드롭다운에 TICLANG 5.1.1이 나타나지 않는다.

**원인**: CCS는 컴파일러를 자신의 설치 디렉토리(`<ccs>/tools/compiler/`) 안에서만 발견한다. TICLANG 5.1.1.LTS는 ccs2100에만, 4.0.4.LTS는 ccs2050에만 존재한다.

**해결**: 툴체인 마이그레이션은 반드시 신 컴파일러가 있는 **ccs2100 인스턴스에서** 진행한다. 구 CCS에서 project를 열면 신 컴파일러가 드롭다운에 뜨지 않아 마이그레이션 자체가 불가능하다.

---

### ⑥ Properties 변경은 "All Configurations"로 설정 후 — Release만 적용되는 함정

**증상**: Release는 신 스택으로 마이그레이션됐는데 Debug configuration이 구스택(구 SDK·구 컴파일러)에 남아 있다.

**원인**: CCS Properties 변경 시 드롭다운이 "Active" 또는 "Release"만 가리키고 있으면 해당 configuration에만 적용된다. Debug에는 변경이 전파되지 않는다.

**해결**: Properties 다이얼로그 상단 configuration 드롭다운을 **"All Configurations"** 로 설정한 뒤 변경을 적용한다. 마이그레이션 후 Debug·Release 양쪽 `.cproject` 항목을 diff로 교차 확인.

---

### ⑦ CCS post-build의 genimage 스크립트 경로도 함께 수정해야 한다

**증상**: `.mcelf` 이미지 생성이 에러 없이 조용히 실패한다.

**원인**: SDK_06에서 genimage 스크립트 리네임(`genimage_am26x.py` → `genimage.py`)이 `build/makefile`뿐 아니라 **CCS post-build 경로** (`makefile_ccs_bootimage_gen:54`)에도 반영돼야 한다. CCS post-build에 ignored-error flag가 붙어 있어 실패가 조용히 묻힌다.

**해결**: SDK 업그레이드 시 `build/makefile` + `makefile_ccs_bootimage_gen` 두 곳의 `MCELF_IMAGE_GEN` 경로를 함께 수정. (commit f3d16ff) 연관 정본 [[sdk_ccs_toolchain_migration]] §5.

---

### ⑧ CCS 20/21(Theia 기반) — headless build CLI 없음, Resource Filters UI 없음

**증상**: ① CI/스크립트에서 CCS managed build를 headless로 실행하려 해도 진입점이 없다. ② `.project` Resource Filters를 Properties UI에서 추가·삭제하려 해도 해당 메뉴가 없다.

**원인**: CCS 20/21은 모두 Theia 기반이며, classic Eclipse CDT의 일부 기능이 이식되지 않았다. 특히 headless managed build(`projectBuild` CLI)와 Resource Filters UI가 빠져 있다.

**교훈**: headless 빌드는 **gmake 경로**(`build/makefile`)만 사용. Resource filter 대신 **sourceEntries 직접 제어**(§ 함정 ④)로 소스 포함/제외를 관리한다.

---

## 4. TI 경로 하드코딩과 환경 이식성

### CCS managed build (`Release/`)

`Release/makefile`·`Release/subdir_rules.mk`는 CCS가 **로컬 절대경로**(`C:/ti/ccs2100/...`, `C:/Users/.../...`)를 박아 생성한다 — git 추적 안 함(`.gitignore`). 다른 노트북에서 git clone 후 바로 make하면 깨진다.

→ **CCS로 프로젝트 import**(= 로컬 경로로 makefile 재생성) 후 빌드.

### 수제 gmake (`build/`)

`build/config.mk`에 TI 경로가 하드코딩되어 있다. 현재 신 스택 기준 경로:

```makefile
# config.mk (신 스택, toolchain-ccs21-sdk2606 기준)
MCU_PLUS_SDK_PATH ?= C:/ti/mcu_plus_sdk_am263px_26_00_00_06
CCS_PATH          ?= C:/ti/ccs2100/ccs
SYSCFG_PATH       ?= C:/ti/ccs2100/ccs/utils/sysconfig_1.28.0
```

다른 설치 경로에서는 환경변수 override 가능:

```sh
MCU_PLUS_SDK_PATH=C:/custom/ti/sdk make
```

`tools/ospi_flash/` 내부 TI 경로는 별도 하드코딩이라 env override 범위 밖 — 직접 수정 필요(README §최초 1회 셋업 참고).

### eta_tuning.h — syscfg 재생성 불요 경로

`eta_tuning.h` 변경(dead-time 상수 등)은 순수 C 컴파일로 반영 — syscfg 재생성 불요. 이것이 런타임 override 방식의 이점([[status]] §빌드 환경 주의 참고).

---

## 함께 보기

- 툴체인 마이그레이션 함정 7종: [[sdk_ccs_toolchain_migration]]
- flash 툴링 메커니즘 + mcelf 소스 분기: [[ospi_flash_tooling]]
- CCS IDE 종료 규율 (flash 전 전제 조건): [[jtag_flash_clean_host]]
- OSPI 부트 플로우: [[ospi_boot_mode_strap]]
- 현재 위치·다음 시작점: [[status]]
