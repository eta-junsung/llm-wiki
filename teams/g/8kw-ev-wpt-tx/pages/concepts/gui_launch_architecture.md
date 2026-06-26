---
tags: [concept, gui, launcher, venv, bootstrap, deadtime, decision, 8kw-ev-wpt-tx]
source: repo main 직접 확인 (tools/gui/launch.py·gui.py, commit 316e649·bec434d·67eac11, 2026-06-25/26)
date: 2026-06-26
subsystem: 8kw-ev-wpt-tx, host
---

# GUI 런치 구조 + "현행 유지" 결정

> **8kw-ev-wpt-tx GUI([[pc_monitor_gui]])를 어떻게 띄우는가 + 왜 다른 배포 형태로 안 바꾸는가.**
> 런치 메커니즘은 OS 무관 `launch.py` 부트스트랩 하나로 통일돼 있고(2026-06-19 Windows `.bat`/`.ps1` 체인을 대체), 브라우저화·exe화·단일명령 통합은 **불채택**이 결정이다.

---

## 1. 런치 구조 (사실)

진입은 `launch.py` 단일 소스다.

```
python tools/gui/launch.py  →  (venv python) gui.py
```

OS별 thin shim(`run-gui-linux.sh`, `run-gui-windows.bat`)은 PR #10 commit `67eac11`(2026-06-26)에서 삭제됨. 더블클릭 래퍼로서의 역할만 하던 shim이었고, VSCode 터미널 단일 커맨드 워크플로로 전환함에 따라 제거. `launch.py`가 OS 분기를 내부에서 처리하므로 shim 없이도 동일 동작.

### `tools/gui/launch.py` — OS 무관 부트스트랩 (commit `316e649`)

`sys.platform` 분기로 Windows·Linux/macOS 모두에서 동작하는 단일 부트스트랩:

1. **repo 루트 해석** — `launch.py` 위치에서 **2단계 위** = 저장소 루트(`_repo_root`).
2. **venv 보장** — 루트 `.venv`가 없으면 `venv.create(..., with_pip=True)`로 생성(`_ensure_venv`). 생성 실패 시 OS별 힌트 출력(Linux=`sudo apt install python3.X-venv`, Windows=공식 인스톨러 tcl/tk·pip 옵션).
3. **의존성 설치** — venv pip으로 `tools/gui/requirements.txt` 설치(`--quiet`, 이미 충족이면 빠르게 종료).
4. **gui.py 실행** — venv python으로 `gui.py` 기동, **cwd = 저장소 루트**(CSV 로그가 루트에 모이도록). `launch.py`의 추가 argv는 `gui.py`로 그대로 전달(`--deadtime`·`--write` 등 [[pc_monitor_gui]] CLI passthrough).

venv python 경로는 OS 분기 — Windows `.venv\Scripts\python.exe` / 그 외 `.venv/bin/python`(`_venv_python`).

→ **모든 실제 로직은 `launch.py` 단일 소스.** shim은 삭제됨(commit `67eac11`).

### requirements (핀 고정)

```
pyserial==3.5
matplotlib==3.11.0
```

---

## 2. deadtime 기능 = 개발등급 환경 의존 (사실 — 결정의 핵심 근거)

GUI의 deadtime 컨트롤은 단순 시리얼 통신이 아니라 **소스 수정 → 빌드 → flash** 체인이다(`run_build_flash`). 상세 시퀀스는 [[pc_monitor_gui]] §Dead-time, 빌드 두 갈래는 [[build_methods]].

- **write**: `src/bsp/eta_bsp_pwm.h`의 `#define ETA_BSP_PWM_DEADTIME_NS <n>U`를 정규식 치환(`gui.py:74`). 유효 범위 **100~500 ns**(`DEADTIME_MIN_NS`/`MAX_NS`). ← 이전: `src/eta_bsp/eta_tuning.h`·`ETA_DEADTIME_NS` (PR #5 firmware-layering에서 이전됨).
- **build**: `gmake -C build all`. gmake 탐색 3순위 — ①`build/config.mk`의 `CCS_PATH` → ②`PATH` → ③`C:\ti\ccs*\...\gmake.exe` 최신본.
- **flash**: `FLASH_SCRIPT` 실행 — Windows `powershell -File`, 그 외 `bash`. 스크립트 = `tools/ospi_flash/run_flash_node_8kw.{ps1,sh}` (JTAG).

⟹ **함의: 이 기능을 쓰는 머신은 firmware 소스트리 + `build/` + TI CCS(gmake) + JTAG flash 환경을 전부 갖춰야 한다.** 가벼운 시리얼 뷰어가 아니라 개발등급 환경 의존이다 — 아래 결정의 토대.

---

## 3. 결정 — 런치 구조 현행 유지 (운영 판단)

GUI 런치 구조는 **현행 유지**. 아래 대안 셋 모두 **불채택**:

| 불채택 대안 | 근거 |
|-------------|------|
| 브라우저 기반(Web Serial / 로컬 서버) | — |
| PyInstaller exe 단일 배포 | — |
| 단일명령(OS 양쪽 더블클릭) 통합 파일 | — |

근거:

- **(a) 제로설치 청중 부재** — GUI 사용자는 전원 repo + CCS를 이미 보유한다. 툴체인 없는 "순수 뷰어" 청중이 없으므로 제로설치(브라우저·exe)의 이점이 적용될 곳이 없다.
- **(b) 단일 아티팩트로 번들 불가** — deadtime = 소스 수정 → CCS 빌드 → JTAG flash 의존(§2)이라 어떤 단일 exe·웹앱으로도 묶을 수 없다.
- **(c) OS 양쪽 더블클릭 단일 파일은 메커니즘상 부재** — 한 파일이 Windows·Linux 양쪽에서 더블클릭 실행되는 OS 메커니즘이 없다. 현재의 OS별 thin shim + 공통 `launch.py`가 이 제약 하의 정답.

---

## 4. 환원 후보 — 문서/코드 어긋남 (lint)

repo `README.md`(main 기준)가 실제 런처와 어긋남:

- README §6 "GUI 실행"은 수동 `pip3 install -r tools/gui/requirements.txt` + `python3 tools/gui/gui.py`로만 안내 — `launch.py`/shim/venv 자동 부트스트랩을 언급하지 않음. → 실제 런처와 불일치.
- README:3은 "이 브랜치(`ubuntu`)"라 기술하나 현재 브랜치는 **main**(실측 확인). 문서가 다른 브랜치 가정으로 쓰인 흔적 (왜 main에 남았는지는 [모름]).

→ README 수정은 repo 작업(별도). 여기선 사실만 기록.

---

## 5. 가설 / 모름 (추론 금지)

- **[가설→사실로 좁힘] PyInstaller exe는 현재 미구현.** `gui.py`의 `sys.frozen` 분기(repo 4단계 위 경로 해석)와 `tools/gui/.gitignore`의 `build/`·`dist/` 항목은 exe 빌드를 의도한 흔적이나, **`.spec`·`dist/`·exe 모두 repo에 부재**(실측). 현재 실행 경로는 `python gui.py`뿐. ⟹ [[pc_monitor_gui]]의 종전 "8kw-gui.exe ~39 MB 존재" 서술은 무효 → 그 페이지에서 정정.
- **[모름] macOS 동작 여부** — `run-gui-linux.sh` 주석은 "Linux / macOS"라 적었으나 검증 흔적 없음.
- **[모름] Windows에서 `.bat` 실제 구동·flash 검증 기록 유무.**

---

## 관련

- [[pc_monitor_gui]] — GUI 앱 자체(ADC 모니터 + dead-time 빌드/플래시 컨트롤·CLI). 이 페이지는 "어떻게 띄우는가 + 왜 안 바꾸는가"
- [[build_methods]] — 방법2(HW 엔지니어 GUI gmake 빌드)의 진입점이 이 런처
- [[windows_bat_ps1_launcher]] — 이 런처가 대체한 종전 Windows `.bat`+`.ps1` 패턴(전사 공통 참조로는 유효, 8kw 적용례는 historical)
- [[linux_migration]] — OS 무관 런처 전환의 상위 동인(`.ps1`/`.bat` → cross-OS)
