---
tags: [concept, build, flash, ccs, gmake, gui, workflow, am263p, 8kw-ev-wpt-tx]
source: 코드 분석 — build/makefile · build/config.mk · tools/gui/gui.py · tools/ospi_flash/run_flash_node_8kw.ps1 · flash_node_8kw.js 직접 확인 (2026-06-19, 신스택 CCS21/SDK_06); PR #10 갱신(2026-06-26)
date: 2026-06-26
---

# 빌드·플래시·편집 — gmake 단일 빌드 + 역할 분리

> **8kw-ev-wpt-tx 정본 — "이거 어떻게 빌드·플래시하나" 진입 페이지.**
> PR #10(2026-06-26)에서 빌드를 **gmake 단일 경로**로 통합했다. CCS IDE 빌드(`Release/`)는 **휴면(dormant)**. 역할 분리 전체 그림은 [[devenv_roles]].
> SysConfig 생성물 의존 모델·함정은 [[syscfg_build_model]], flash 툴링 메커니즘은 [[ospi_flash_tooling]], 툴체인 경로 배선은 [[sdk_ccs_toolchain_migration]].

---

## 1. 빌드 방식 (현재: gmake 단일)

| 항목 | gmake 빌드 ✓ | CCS IDE 빌드 (휴면) |
|------|-------------|------------------|
| **명령** | `gmake -C build all` | CCS managed build (`.cproject`) |
| **산출물** | `build/8kw-ev-wpt-tx.out` + `.mcelf` | `Release/8kw-ev-wpt-tx.out` + `.mcelf` |
| **진입점** | 터미널 직접, 또는 GUI `--build` | CCS IDE Build 버튼 |
| **상태** | **활성** | **휴면(dormant, PR #10 2026-06-26)** |

flash 스크립트는 항상 `build/` 산출물을 사용 — `-Source` 인자 없음(`flash_node_8kw.js:51`).

`gmake.exe` 탐색 순서 = `build/config.mk`의 `CCS_PATH` → `PATH` → `C:\ti\ccs*\...\gmake.exe` 최신본.

### CLI 명령 모음

```sh
# 빌드
gmake -C build all

# GUI (모니터·dead-time 빌드/플래시)
python tools/gui/launch.py

# headless dead-time 변경+빌드+플래시
python tools/gui/launch.py --deadtime 150 --write --build --flash
```

---

## 2. 공통 스택 (CCS21 / SDK_06 신스택)

두 방법 모두 동일한 툴 인스턴스를 쓴다:

| 구성요소 | 경로 |
|----------|------|
| MCU+ SDK | `C:/ti/mcu_plus_sdk_am263px_26_00_00_06` |
| 컴파일러 (tiarmclang) | `C:/ti/ccs2100/ccs/tools/compiler/ti-cgt-armllvm_5.1.1.LTS` |
| SysConfig | `C:/ti/ccs2100/ccs/utils/sysconfig_1.28.0` |
| node | `C:/ti/ccs2100/ccs/tools/node/node` |

- **타겟**: AM263P4, ZCZ_C, core `r5fss0-0`, OS = NoRTOS.
- **머신별 경로 이식**은 `build/config.mk` **3줄**(`MCU_PLUS_SDK_PATH` / `CCS_PATH` / `SYSCFG_PATH`)만 수정하면 된다.
- `imports.mak`이 박는 구버전 경로는 `build/makefile` 상단에서 신스택 경로로 덮어쓴다. (배선 메커니즘 상세: [[sdk_ccs_toolchain_migration]])

---

## 3. SysConfig 생성물 규칙 (두 방법 공통, 함정)

- `generated/`는 **커밋되어 있고**, 기본 `SYSTEM_FLAG=true`이면 syscfg 재생성을 건너뛰고 커밋된 `generated/`를 그대로 사용한다.
- `example.syscfg`를 바꿨을 때만 재생성한다:

  ```sh
  gmake -C build all SYSTEM_FLAG=false
  ```

- ⚠️ `generated/`를 통째로 `.gitignore`하면 gmake 빌드가 깨진다 — 미사용 모듈도 stub으로 emit되어 빌드에 필요하다.

심층(SYSTEM_FLAG 분기·stub emit·CCS vs gmake 바이너리 비동일 등): [[syscfg_build_model]].

---

## 4. 새 소스 파일 추가 시

CCS IDE 빌드가 휴면이므로 **gmake 쪽만 등록하면 된다.**

| 빌드 | 등록 위치 |
|------|-----------|
| gmake (활성) | `build/makefile`의 `FILES_common` (필요 시 `FILES_PATH_common` / `INCLUDES_common`) |
| CCS IDE (휴면) | `.cproject`의 `sourceEntries` — CCS 빌드가 필요할 때만 |

---

## 5. 플래시

flash 스크립트는 항상 `build/` 산출물을 굽는다(`flash_node_8kw.js:51`). `-Source` 인자는 더 이상 없다.

| OS | 명령 |
|----|------|
| Linux | `./tools/ospi_flash/run_flash_node_8kw.sh` |
| Windows | `powershell -ExecutionPolicy Bypass -File tools\ospi_flash\run_flash_node_8kw.ps1` |

**절차**: XDS110 JTAG 접속 → `ERASE_ALL` → SBL @0x00000000 → app `.mcelf` @0x00081000.

**전제**:

- 보드 JTAG 연결. `gmake -C build all` 완료.
- CCS 디버그 세션/IDE **완전 종료** — DSLite 백엔드 경합 (상세 [[jtag_flash_clean_host]]).
- **부팅 스트랩**: standalone 부팅은 **SW1 = `0,0,1,1`(xSPI 8D SFDP)** ([[ospi_boot_mode_strap]]).

플래시 메커니즘(헬퍼 FW를 RAM에 올려 OSPI 굽기) 상세: [[ospi_flash_tooling]].

---

## 6. CCS는 디버그·플래시 전용 (PR #10 확정)

- **산출물명이 두 빌드에서 동일**: `build/8kw-ev-wpt-tx.out`·`Release/8kw-ev-wpt-tx.out` 동일 이름, 디렉터리로만 구분됨 (`build/makefile:27` `OUTNAME`, `:140` `.mcelf` 타겟).
- **★ CCS 디버그는 gmake 산출물(`build/*.out`)만으로 성립한다.** 실보드에서 `build/*.out` 로드→브레이크포인트 소스 줄 바인딩→실행 시 hit 확인(2026-06-26). CCS 안에서 다시 빌드(managed build)할 의무 없음.
- **완료(PR #10, 2026-06-26)**: 빌드를 gmake 단일로 통합, CCS는 디버그·flash 전용. [[devenv_roles]] 참조.

## 7. VSCode + clangd 네비게이션

빌드 후 `compile_commands.json`이 repo 루트에 생성된다(`build/makefile:180-190`). `.clangd`·`.vscode/settings.json`이 커밋돼 있어 초기 셋업은 아래로 충분:

1. `llvm-vs-code-extensions.vscode-clangd` 확장 설치
2. `gmake -C build all` 실행
3. VSCode 재로드

`--query-driver=**/bin/tiarmclang`(`.vscode/settings.json:2`)이 없으면 clangd가 tiarmclang 내장 헤더 경로를 인식하지 못한다.

`compile_commands.json`은 git-ignore(머신별 절대경로 포함) — clone 후 빌드로 생성.

---

## 함께 보기

- 역할 분리 전체 그림·비자명 사실 4개: [[devenv_roles]]
- SysConfig 생성물 빌드 의존 모델·함정: [[syscfg_build_model]]
- OSPI flash 툴링 메커니즘: [[ospi_flash_tooling]]
- CCS IDE 종료 규율 (flash 전 전제): [[jtag_flash_clean_host]]
- OSPI 부트모드 스트랩 (SW1 정답 `0,0,1,1`): [[ospi_boot_mode_strap]]
- 툴체인 경로 배선·마이그레이션 함정: [[sdk_ccs_toolchain_migration]]
- GUI 상세 (dead-time 빌드/플래시 컨트롤): [[pc_monitor_gui]]
- GUI 런처 구조·배포 결정: [[gui_launch_architecture]]
- 현재 위치·다음 시작점: [[status]]
