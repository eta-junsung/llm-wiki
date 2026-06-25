---
tags: [concept, build, flash, ccs, gmake, gui, workflow, am263p, 8kw-ev-wpt-tx]
source: 코드 분석 — build/makefile · build/config.mk · tools/gui/gui.py · tools/ospi_flash/run_flash_node_8kw.ps1 · flash_node_8kw.js 직접 확인 (2026-06-19, 신스택 CCS21/SDK_06)
date: 2026-06-19
---

# 두 가지 빌드 방법 — 개발자(CCS IDE) vs HW 엔지니어(GUI gmake)

> **8kw-ev-wpt-tx 정본 — "이거 어떻게 빌드·플래시하나" 진입 페이지.** 펌웨어를 빌드하는 길은 둘이다: 개발자가 IDE 안에서 빌드하는 **CCS IDE 빌드(`Release/`)**, HW 엔지니어가 IDE 없이 GUI로 빌드→플래시까지 한 번에 하는 **GUI gmake 빌드(`build/`)**. 두 길은 **동일한 `example.syscfg` 하나**를 입력으로 쓰고, 플래시 다운스트림도 같은 스크립트를 공유한다.
> 생성물 의존 메커니즘·함정의 심층은 [[syscfg_build_model]], flash 툴링 메커니즘은 [[ospi_flash_tooling]], 툴체인 경로 배선은 [[sdk_ccs_toolchain_migration]].

---

## 1. 방법1 vs 방법2 — 한눈 비교

| 항목 | 방법 1 — CCS IDE 빌드 | 방법 2 — GUI gmake 빌드 |
|------|----------------------|------------------------|
| **용도** | 개발자가 IDE 안에서 편집·디버그하며 빌드 | HW 엔지니어가 IDE 없이 빌드→플래시 원클릭 |
| **방식** | CCS managed build(`.cproject`), Release 프로파일 | `gmake -C build all` (내부 호출) |
| **진입점** | CCS IDE Build 버튼 | `tools/gui/run-gui-{linux.sh,windows.bat}` 더블클릭 → `tools/gui/launch.py`(venv 부트스트랩) → `tools/gui/gui.py` ([[gui_launch_architecture]]) |
| **빌드 명령** | CCS managed build (IDE 내부) | `gmake -C build all` |
| **산출물** | `Release/8kw-ev-wpt-tx.mcelf` (+ `.out`/`.map`) | `build/8kw-ev-wpt-tx.mcelf` |
| **플래시 소스** | `run_flash_node_8kw.ps1 -Source release` (기본값) | GUI가 `run_flash_node_8kw.ps1 -Source build` 호출 |

방법 2의 `gmake.exe` 탐색 순서 = `build/config.mk`의 `CCS_PATH` → `<CCS>/utils/bin/gmake.exe`.

### 방법 2 — CLI 동등 명령 (헤드리스)

GUI 없이 같은 일을 명령줄로:

```sh
gmake -C build all
python tools/gui/gui.py --deadtime <ns> --write --build --flash
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

## 4. 새 소스 파일 추가 시 (반드시 강조)

**새 `.c` 파일은 두 빌드 시스템에 각각 등록해야 한다.** 한쪽만 추가하면 다른 빌드에서 미컴파일/링크 누락이 난다.

| 빌드 | 등록 위치 |
|------|-----------|
| 방법 1 — CCS IDE | `.cproject`의 `sourceEntries` |
| 방법 2 — gmake | `build/makefile`의 `FILES_common` (필요 시 `FILES_PATH_common` / `INCLUDES_common`) |

---

## 5. 플래시 (두 방법 공통 다운스트림)

두 방법 모두 같은 스크립트로 굽는다 — 차이는 `-Source` 인자뿐:

```
tools/ospi_flash/run_flash_node_8kw.ps1 -Source <release|build>
```

**절차**: XDS110 JTAG 접속 → `ERASE_ALL` → SBL(`C:/ti/sbl_ospi_am263p.tiimage`) @0x00000000 → app `.mcelf` @0x00081000.

**전제**:

- 보드 JTAG 연결.
- CCS 디버그 세션/IDE **미상주** — 플래시 스크립팅과 DSLite 백엔드가 경합한다 (상세 [[jtag_flash_clean_host]]).
- **부팅 스트랩**: standalone 부팅은 **SW1 = `0,0,1,1`(xSPI 8D SFDP)**. `1,1,1,1`(4S)는 이 옥타 플래시(IS25LX256)에서 부팅 안 됨 (정본 [[ospi_boot_mode_strap]]).

플래시 메커니즘(헬퍼 FW를 RAM에 올려 OSPI 굽기)·`--source` argv 분기 상세: [[ospi_flash_tooling]].

---

## 함께 보기

- SysConfig 생성물 빌드 의존 모델·함정: [[syscfg_build_model]]
- OSPI flash 툴링 메커니즘 + mcelf 소스 분기: [[ospi_flash_tooling]]
- CCS IDE 종료 규율 (flash 전 전제): [[jtag_flash_clean_host]]
- OSPI 부트모드 스트랩 (SW1 정답 `0,0,1,1`): [[ospi_boot_mode_strap]]
- 툴체인 경로 배선·마이그레이션 함정: [[sdk_ccs_toolchain_migration]]
- 방법 2 GUI 상세 (dead-time 빌드/플래시 컨트롤): [[pc_monitor_gui]]
- 방법 2 런처 구조·배포 결정: [[gui_launch_architecture]]
- 현재 위치·다음 시작점: [[status]]
