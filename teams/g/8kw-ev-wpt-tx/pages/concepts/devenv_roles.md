---
tags: [concept, devenv, build, debug, flash, vscode, clangd, workflow, am263p, 8kw-ev-wpt-tx]
source: 코드 분석 + 실측 — PR #10 커밋 50205b9·67eac11·dc33324·9598a6d·b4e3591 직접 확인 (2026-06-26)
date: 2026-06-26
---

# 개발환경 역할 분리 — 빌드/디버그/플래시/편집 (PR #10)

> **8kw-ev-wpt-tx 개발환경 정본.** PR #10에서 역할 기준으로 통합. 도구 하나에 두 역할을 맡기지 않는다.
> 이전의 "CCS IDE 빌드 vs GUI gmake 빌드" 이원화([[build_methods]])는 종료 — 빌드는 gmake 단일.

---

## 1. 역할 분리 한눈 요약

| 역할 | 도구 | 명령 |
|------|------|------|
| **빌드** | gmake | `gmake -C build all` |
| **디버그** | CCS 2100 (IDE 켜야 함) | `build/*.out` 로드, 브레이크포인트 |
| **플래시** | CCS 2100 (IDE 꺼야 함) | `tools/ospi_flash/run_flash_node_8kw.{sh,ps1}` |
| **읽기·편집·탐색** | VSCode + clangd | 빌드 후 `compile_commands.json` 자동 생성 |
| **GUI 모니터** | launch.py | `python tools/gui/launch.py` |

CCS IDE 빌드(`Release/`)는 **휴면(dormant)** — 빌드 이원화 시대 종료(PR #10, 2026-06-26).

---

## 2. 빌드 — gmake 단일

```sh
gmake -C build all
```

산출물: `build/8kw-ev-wpt-tx.out`(ELF) + `build/8kw-ev-wpt-tx.mcelf`(boot image)

- SysConfig 재생성 필요 시: `gmake -C build all SYSTEM_FLAG=false`
- 머신별 이식: `build/config.mk` 3줄(`MCU_PLUS_SDK_PATH`·`CCS_PATH`·`SYSCFG_PATH`)

**빌드 말미에 `compile_commands.json` 자동 생성** — `build/makefile:138`에서 컴파일 시 `-MJ` 플래그로 파일별 `.cdb.json` 조각을 `obj/release/`에 저장, `build/makefile:180-190`에서 repo 루트 `../compile_commands.json`으로 조립. git-ignore이므로 clone 후 첫 빌드에서 생성됨.

SysConfig 생성물·새 소스 파일 등록 규칙은 [[build_methods]] §3·§4.

---

## 3. 디버그 — CCS 2100

**★ CCS 디버그는 gmake 산출물(`build/*.out`)만으로 성립한다.** "CCS로 한 번은 빌드해야 디버그된다"는 전제는 거짓 — 실보드에서 `build/*.out` 로드→브레이크포인트 소스 줄 바인딩→실행 시 hit까지 확인(2026-06-26). 이것이 빌드 단일화의 근거.

절차:
1. `gmake -C build all` — build/ 산출물 생성
2. CCS에서 `build/8kw-ev-wpt-tx.out` 로드 → 디버그 세션 시작

### ccs-debug MCP와 IDE 상주 요건

**`ccs-debug` MCP는 CCS IDE(Theia) GUI가 켜져 있어야 동작한다.** IDE의 상주 cloudagent+DSLite에 attach하는 구조라 헤드리스 불가. flash 스크립트와 MCP는 같은 XDS110 백엔드를 공유하므로, **flash 중에는 CCS 디버그 세션을 닫아야 한다** ([[jtag_flash_clean_host]]).

### CCS 2100 ≠ 정품 MS VSCode

**CCS 2100 = CCS v21 = Eclipse Theia(VSCode UI 기술 기반)다.** TI는 정품 MS VSCode용 Sitara AM263 디버그 어댑터를 제공하지 않는다(TI C2000-IDEA는 C2000 전용). 따라서 "VSCode로 디버그 이전"은 비권장 — ccs-debug MCP를 잃는다.

---

## 4. 플래시 — CCS headless DSS scripting

**flash 전제: CCS IDE 완전 종료** ([[jtag_flash_clean_host]]).

flash 스크립트는 항상 `build/8kw-ev-wpt-tx.mcelf`를 굽는다(`flash_node_8kw.js:51`). `-Source` 인자는 더 이상 없다.

### Linux

```sh
./tools/ospi_flash/run_flash_node_8kw.sh
```

`~/ti/ccs2100/ccs/scripting/run.sh` 하드코딩(`run_flash_node_8kw.sh:7`). CCS가 이 경로에 설치되어 있어야 한다.

### Windows (PowerShell)

```powershell
powershell -ExecutionPolicy Bypass -File tools\ospi_flash\run_flash_node_8kw.ps1
```

`C:\ti\ccs2100\ccs\scripting\run.bat` 하드코딩(`run_flash_node_8kw.ps1:5`).

SBL 경로는 `TI_DIR` 환경변수로 덮을 수 있다 — 미설정 시 Linux=`$HOME/ti`, Windows=`C:/ti`(`flash_node_8kw.js:28`).

메커니즘 상세([[ospi_flash_tooling]]), 부트모드 스트랩 SW1=`0,0,1,1`([[ospi_boot_mode_strap]]).

---

## 5. 읽기·편집·탐색 — VSCode + clangd

`gmake -C build all` 후 clangd가 tiarmclang 컴파일 인수 전체를 인지해 정확한 헤더 해석·심볼 이동·자동완성이 된다.

### 설정 파일 (모두 커밋됨, commit 50205b9)

| 파일 | 핵심 설정 |
|------|---------|
| `.clangd` | `CompilationDatabase: Release/.clangd` — compile DB 디렉터리 경로 |
| `.vscode/settings.json:2` | `"--query-driver=**/bin/tiarmclang"` |
| `.vscode/settings.json:6` | `"C_Cpp.intelliSenseEngine": "disabled"` — ms-cpptools IntelliSense 비활성 |
| `.vscode/extensions.json` | `vscode-clangd` 권장, `ms-vscode.cpptools` 비권장 |

`--query-driver` 설정이 없으면 clangd가 tiarmclang 내장 시스템 헤더 경로를 모른다.

### 초기 셋업 (fresh clone)

1. VSCode 확장 `llvm-vs-code-extensions.vscode-clangd` 설치
2. `gmake -C build all` → `compile_commands.json` 생성
3. VSCode 재로드 → clangd가 DB 읽기 시작

---

## 6. GUI 모니터 — launch.py 단일 진입점

```sh
python tools/gui/launch.py
python tools/gui/launch.py --deadtime 150 --write --build --flash
```

OS별 shim(`run-gui-linux.sh`, `run-gui-windows.bat`)은 PR #10 commit `67eac11`에서 삭제됨 — 더블클릭 워크플로가 아닌 VSCode 터미널 단일 커맨드 워크플로로 전환한 것이 이유. `launch.py`가 venv 자동 생성·의존성 설치를 처리한다.

런치 메커니즘 상세: [[gui_launch_architecture]].

---

## 7. 미사용 enet/sdl 생성물 삭제 근거

`build/generated/ti_enet_*.c/h` + `ti_sdl_config.*` 12개 파일 삭제(commit 50205b9). 안전 근거:
- `example.syscfg`에 enet/sdl/cpsw 모듈 없음 → SysConfig가 생성하지 않음
- `build/makefile` `FILES_common`에 포함 안 됨 → gmake 미컴파일
- `src/` 내 `#include` 참조 0건

CCS Release 빌드(`Release/`)에만 잔재로 포함돼 있던 것. gmake 기준 안전 삭제.

---

## 함께 보기

- SysConfig 생성물·빌드 의존 모델·이원화 역사: [[build_methods]]
- flash 클린 호스트 규율 + "Run > Flash Project" 금지: [[jtag_flash_clean_host]]
- flash 툴링 메커니즘 (OSPI 구조·헬퍼 FW): [[ospi_flash_tooling]]
- GUI 런치 구조·현행 유지 결정: [[gui_launch_architecture]]
- 부트모드 스트랩(SW1=`0,0,1,1`): [[ospi_boot_mode_strap]]
- 현재 위치·다음 시작점: [[status]]
