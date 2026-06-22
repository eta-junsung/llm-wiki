---
tags: [concept, linux, ubuntu, dev-environment, migration, toolchain, company-common]
source: conversation-2026-06-22 (전환 결정) + projects/ 디렉토리 직접 점검 (런처·툴체인 사실 확인)
date: 2026-06-22
---

# Windows → Ubuntu Linux 개발환경 전환 — 결정·근거

> **전사 공통 운영 결정.** 개발 호스트 OS를 Windows 11 → Ubuntu 24.04 LTS로 옮긴다. 모든 펌웨어 프로젝트의 개발환경에 걸치므로 루트 `pages/concepts/`에 둔다([[firmware_git_workflow]]·[[schematic_ingest_strategy]]와 동급의 전사 공통 방법론).
>
> 이 페이지는 **무엇을·왜**(결정·근거·portability 평가). 단계별 **어떻게**(백업→설치→검증 게이트→포팅→파티션 회수)는 단계 로드맵 [roadmaps/linux_migration.md](../../roadmaps/linux_migration.md)로 위임한다.

---

## 1. 결정 사항 (확정 — 사실로 기록)

| 항목 | 결정 | 근거 |
|------|------|------|
| **배포판** | **Ubuntu 24.04 LTS Desktop (amd64), GNOME 기본** | TI CCS Theia 공식 지원 Ubuntu는 20.04/22.04/**24.04**뿐. STM32CubeIDE·SEGGER도 24.04 커버. 24.04는 안정화 완료 + 2029까지 지원. 26.04(벤더 미인증)·비-LTS(`.10`)는 배제 |
| **전략** | **듀얼부팅으로 시작 → 검증 게이트 통과 후 윈도우 파티션 회수** | 검증 게이트 전까지 윈도우 안전망 유지(되돌릴 구석 확보). 회수는 gparted로 윈도우 OS 파티션만 삭제 + Ubuntu 파티션 확장 + `update-grub` |
| **WSL2** | **배제** | 윈도우 OS 자체를 안 쓰고 싶은 게 동기 → WSL2(윈도우 위 리눅스)는 동기와 모순, 무의미 |

### ⚠️ ESP(EFI 시스템 파티션) 절대 삭제 금지

파티션 회수 시 **윈도우 OS 파티션만** 삭제한다. **ESP는 건드리지 않는다** — Ubuntu가 GRUB을 윈도우와 **같은 ESP에 나란히** 설치하므로, ESP를 지우면 Ubuntu 자신도 부팅 불가가 된다. 상세 절차는 로드맵 ⑧단계.

---

## 2. 전환 동기 (왜 하는가)

세 갈래. ①은 삶의 질, ②③은 투자.

1. **윈도우 OS 자체에 대한 거부감** — 하루 8h 머무는 작업환경의 삶의 질 문제.
2. **장기 스킬 투자 (펌웨어 개발자의 Linux 숙련)** — 임베디드 리눅스/Yocto, Zephyr(Linux가 1군 시민), CI/CD·빌드팜·HIL(대부분 Linux), 오픈 툴체인(GCC/OpenOCD/gdb), 전이되는 Unix 셸/make 역량. 펌웨어 커리어의 상방이 대부분 Linux 위에 있다.
3. **Edge AI / TinyML (장기 동인 — 즉시 단계 아님)** — 가까운 미래의 우선 관심사. 모델 학습·변환 파이프라인이 Python/Linux 세계(TF/PyTorch, TFLite Micro, ONNX, microTVM, CUDA GPU 학습, Docker)라, 진지하게 하면 어차피 Linux로 들어간다 → 미리 닦아두는 길.

> **범위 주의**: Edge AI는 **장기 동인으로만** 기록한다 — 로드맵의 즉시 단계엔 넣지 않는다(로드맵 "환원 후보/후속" 참조). FreeRTOS는 Linux 상관이 약하다(POSIX 시뮬레이터/CI 사이드 베네핏 정도, 호스트 OS 무관).

---

## 3. 툴체인별 Linux portability 평가

전환 대상 4개 툴체인 **전부 네이티브 Linux 버전이 존재**한다. 윈도우 전용 IDE(IAR/Keil)는 쓰지 않으므로 전환 가능. (사실 / 가설 / 모름 구분, 추정은 `[추정]`.)

| 프로젝트 (MCU) | 툴체인 | Linux 지원 | 이주 비용 | 함정·근거 |
|---|---|---|---|---|
| `c/oled_tv_software/01_RX_control` (STM32F103) | STM32CubeIDE + ST-Link | ✓ 공식 `.deb`/`.sh` | 낮음 | CLI 헤드리스 빌드 불가는 OS 무관 — IDE Ctrl+B 유지([[cubeide_cli_build_trap]]). CubeMX 재생성 금지 |
| `c/oled_tv_software/02_RX_ble·03_TX_ble` (nRF52832) | SEGGER Embedded Studio 8.28 + J-Link, nRF5 SDK 17 (in-repo `_external/`) | ✓ 네이티브 tarball | 낮음 | `.emProject`는 `$(StudioDir)`+상대경로 → Linux서 그대로 열림. SDK in-repo라 경로 이식 불요. `.emProject` 함정(파일 하드코딩·`eta_` 접두사)은 OS 무관([[ses_build_conventions]]) |
| `g/8kw-ev-wpt-tx`·`g/lp-am263p` (TI AM263Px) | CCS Theia + TI Clang(ti-cgt-armllvm **5.1.1**) + SysConfig + gmake, XDS110 | ✓ Ubuntu 20.04/22.04/24.04 공식 | 중간 | `C:/ti/...` 경로(makefile/`compile_commands.json`)는 CCS/SysConfig가 **자동 재생성** → Linux 재import 시 `~/ti/...`로 재생성(수동 수정 최소). `MCU_PLUS_SDK_PATH`는 `?=` env override 설계([[syscfg_build_model]]) |
| `c/oled_tv_software/tools/pc_uart_gui` | Python3 + tkinter + pyserial | ✓ `apt python3-tk` + `pip pyserial` | 낮음 | `.exe`/`build/`는 PyInstaller 산출물 → Linux서 재빌드 or `.py` 직접 실행 |

### 24.04 알려진 함정 — 우리 스택엔 무해

- **libtinfo5 부재**: TI Clang **4.x 미만**에서만 문제. 우리는 5.1.1 → **해당 없음**. (구 스택 잔재 [[sdk_ccs_toolchain_migration]] §8 참조)
- **chrome-sandbox 권한**(Theia 계열): 설치 후 1회성 `chown root + chmod 4755`로 해소.

### 프로브 (USB 디버그) — udev 룰 필요

| 프로브 | Linux 도구 | udev |
|---|---|---|
| J-Link V9.3 Plus (SN 69730359) — nRF52832 | SEGGER J-Link Linux (`JLinkExe`/nrfjprog) | SEGGER 패키지 동봉 `99-jlink.rules` |
| ST-Link V2 — STM32F103 | STM32CubeProgrammer Linux / openocd | ST `49-stlinkv2.rules` |
| XDS110 (온보드, LP-AM263P) — AM263Px | CCS Linux 번들 | TI `71-ti-permissions.rules` (`<ccs>/.../install_scripts/`) |

> 근거: 프로브 정체·SN은 [[instruments]]. **루트 없이 USB 접근하려면 udev 룰 + `plugdev` 그룹**이 Linux의 핵심 추가 작업(Windows엔 없는 단계). 로드맵 ④단계.

---

## 4. 실제 포팅 필요 항목 (PowerShell/배치 → bash)

런처의 **호출 알맹이**(`dslite`/`uniflash`/`node` DSS/`.js`)는 Linux에 존재한다 — **껍데기(.ps1/.bat)만 교체**하거나, `pwsh`(PowerShell Core) 설치 후 경로변수만 수정하면 된다. (전부 `projects/` 직접 grep 확인 2026-06-22.)

| 런처 | Windows 의존 | 포팅 |
|---|---|---|
| `g/8kw-ev-wpt-tx/tools/ospi_flash/run_flash_node_8kw.ps1` | `C:\ti\ccs2100\ccs\scripting\run.bat` 호출 | `run.sh` (CCS Linux `scripting/run.sh`) |
| `g/8kw-ev-wpt-tx/gui.bat` + `tools/gui/launch_gui.ps1` | ASCII `.bat`→`.ps1` 위임 패턴 | `.sh` 래퍼 (또는 `.desktop` 런처) |
| `g/lp-am263p/bp-3351/jtag_flasher/*.ps1` **11개** | `capture_com4{,_binary,_wait}`·`run_flash{,_dslite}`·`run_uart_flash`·`run_uniflash_{erase,all,one}`·`run_flash_node`·`cli_interact`. ⚠️ **구 `ccs2050` 경로** 참조(8kw는 `ccs2100`) | `.sh`. 재import 시 CCS 버전 통일 검토 |

연결: [[windows_bat_ps1_launcher]](현 .bat/.ps1 패턴의 원형)·[[ospi_flash_tooling]](8kw flash 메커니즘)·[[jtag_flash_clean_host]](클린 호스트 규율 — OS 무관). pc_uart_gui 런처는 [[windows_bat_ps1_launcher]] 레시피의 Linux 대응.

---

## 5. 사실 / 가설 / 모름

- **FACT (repo 확인)**: 4개 툴체인 전부 네이티브 Linux 존재. `.emProject`는 `$(StudioDir)`+상대. nRF5 SDK in-repo. 런처 3계열 Windows 경로 의존(위 §4 표). 전환 동기·배포판·전략은 사용자 확정 결정.
- **FACT (디렉토리)**: 프로젝트 레이아웃은 `projects/<팀>/<프로젝트>`(`c/`,`g/`) — 전환 후 `~/eta/projects/c|g/...`.
- **가설 [추정]**: CCS Linux 재import 시 `~/ti/...` 경로 재생성은 "수동 수정 최소"로 끝난다 — 실 재import로 검증 전까지 가설(로드맵 ⑤·⑥단계에서 확정).
- **모름**: 듀얼부팅 시 디스크 파티션 여유·기존 윈도우 BitLocker 여부(백업 단계서 확인). lp-am263p `ccs2050`/`ccs2100` 혼재를 Linux서 한 버전으로 통일할지(재import 시 결정).

---

## 함께 보기

- 단계별 전환 로드맵(백업→설치→툴4종→udev→재import→검증 게이트→런처 포팅→파티션 회수): [roadmaps/linux_migration.md](../../roadmaps/linux_migration.md)
- 현 Windows 런처 패턴(포팅 원형): [[windows_bat_ps1_launcher]]
- 툴체인별 함정: [[ses_build_conventions]] · [[cubeide_cli_build_trap]] · [[sdk_ccs_toolchain_migration]] · [[syscfg_build_model]]
- flash 절차·메커니즘: [[st_link_nrf52_flash]] · [[ospi_flash_tooling]] · [[jtag_flash_clean_host]]
- 프로브·계측 인벤토리: [[instruments]]
- 전사 공통 git 표준: [[firmware_git_workflow]]
