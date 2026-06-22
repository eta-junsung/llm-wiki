---
tags: [roadmap, linux-migration, living-doc]
date: 2026-06-22
---

# Linux 전환 로드맵 — Windows 11 → Ubuntu 24.04 LTS

> **한 줄 요약**: 듀얼부팅으로 Ubuntu 24.04 LTS를 깔고, 4개 툴체인 재설치 → 각 보드 **빌드→플래시→브레이크포인트 디버깅**까지 검증 게이트(L6)를 통과한 뒤에야 런처를 포팅하고 윈도우 파티션을 회수한다. **L6 전까지 윈도우 안전망 유지**.
>
> 결정·근거·툴체인 portability·포팅 대상 디테일은 개념 페이지 [[linux_migration]]로 위임 — 이 로드맵은 **단계 spine + 완료/검증 기준**만.

이 로드맵은 전사 공통 운영 로드맵이라 짝이 되는 프로젝트 `status.md`가 없다 → **현재 위치는 아래 단계표 상태기호로 직접 표기**(프로젝트 로드맵이 `[[status]]`로 위임하는 것과 다른 점). 상태기호: `✓` 완료+검증 / `△` 진행·미검증 / `?` 불명 / `✗` 미착수.

---

## 마일스톤 호 (L1 → L8)

| 단계 | 내용 | 완료/검증 기준 | 상태 |
|------|------|----------------|------|
| **L1 사전 백업** | 윈도우 전용 파일·툴 라이선스·측정 데이터 백업. 설치 USB는 **Ventoy**(여러 ISO 한 USB) | 백업본이 외장/클라우드에 이중화. 회수 불가 자산 0건 확인 | ✗ |
| **L2 듀얼부팅 설치** | Ubuntu 24.04 LTS amd64를 윈도우 옆에 설치. **회수를 염두에 둔 파티션 배치** | Ubuntu 부팅 + GRUB서 윈도우·Ubuntu 양쪽 부팅 성공. ESP 공유 확인 | ✗ |
| **L3 툴 4종 설치** | ① STM32CubeIDE ② SEGGER ES 8.28 ③ CCS Theia + MCU+ SDK + TI Clang 5.1.1 + SysConfig ④ Python3 + `python3-tk` + pyserial | 각 IDE 기동 + 빈 빌드 1회 통과 | ✗ |
| **L4 JTAG udev 룰 3종** | J-Link / ST-Link / XDS110 udev 룰 + `plugdev` 그룹 | 루트 없이 세 프로브 모두 enumerate (`JLinkExe`/`pyocd list`/CCS) | ✗ |
| **L5 프로젝트 재import·빌드경로 재생성** | `c/`·`g/` 프로젝트 clone/이주. CCS 재import로 `~/ti/...` makefile 재생성, config.mk 경로 점검 | 4개 프로젝트 전부 Linux서 **빌드 통과**(플래시 전) | ✗ |
| **L6 ⛳ 검증 게이트** | **각 보드 빌드→플래시→브레이크포인트 디버깅 끝까지** (01 STM32 / 02·03 nRF52832 / 8kw·lp AM263P) | 보드별로 ① 빌드 ② 플래시 ③ 디버거 브레이크포인트 hit 3종 모두 실측 통과. **통과해야 L7 진입** | ✗ |
| **L7 런처 포팅** | `.ps1`/`.bat` → `.sh` (또는 `pwsh` + 경로변수). 8kw flash·GUI 런처, lp 11개 jtag_flasher 스크립트 | 포팅된 런처로 flash·GUI가 Linux서 동작(L6 수단과 일치 확인) | ✗ |
| **L8 윈도우 파티션 회수** | 실무 안정화 후 gparted로 **윈도우 OS 파티션만** 삭제 → Ubuntu 확장 → `update-grub`. **ESP 절대 삭제 금지** | 회수 후 Ubuntu 단독 부팅 성공. 디스크 공간 회수 확인 | ✗ |

**원칙**: L6(검증 게이트)를 통과하기 전까지 윈도우 파티션·기존 환경을 **그대로 보존**한다. L1~L6에서 막히면 윈도우로 즉시 복귀 가능해야 한다. 회수(L8)는 비가역 — L6·L7로 "Linux만으로 실무가 돈다"를 실증한 뒤에만.

---

## 단계별 디테일 핀

- **L1 백업 주의**: `projects/c/`에 백업 zip 2개(`oled_tv_software_.zip`·`oled_tv_software (Back_up)_원본.zip`)와 거대 전달본 사본 `oled_tv_software_전달본/`(SES 설치 프로그램 `.exe` + nRF5_SDK 통째 + `Firmware/oled_tv.zip`)이 있다. 이미 zip이면 그대로 이주, 전달본은 별도 취급(이주 vs 제외) 판단. [추정] 합산 수 GB 규모.
- **L3 툴 근거**: 배포판이 24.04인 이유·각 툴 Linux 지원은 [[linux_migration]] §3. 24.04 함정(libtinfo5는 TI Clang 5.1.1에 무해, chrome-sandbox 1회성)도 동일.
- **L4 udev**: 프로브 정체·SN → [[instruments]]. J-Link(SN 69730359)/ST-Link V2/XDS110.
- **L5/L6 함정**: CubeIDE CLI 헤드리스 빌드 불가는 OS 무관 → IDE Ctrl+B([[cubeide_cli_build_trap]]). nRF `.emProject` 함정([[ses_build_conventions]]). CCS 재import·경로([[syscfg_build_model]]·[[sdk_ccs_toolchain_migration]]). flash 절차([[st_link_nrf52_flash]]·[[ospi_flash_tooling]]·[[jtag_flash_clean_host]]).
- **L7 포팅 대상 표**: [[linux_migration]] §4 (런처 3계열 + 구 `ccs2050` 경로 정리).
- **L8 ESP 경고**: [[linux_migration]] §1.

---

## 현재 위치

**L0 (미착수)** — 2026-06-22 wiki ingest로 결정·로드맵만 기록. 실제 OS 전환은 미시작. 다음 시작점은 사용자가 전환 착수를 결정할 때 **L1 사전 백업**.

---

## 남은 일정 [추정]

전 단계 미착수. 실작업 시간 추정은 사용자 일정에 종속 → **모름**. 게이트 L6이 임계 — 보드 3종(STM32/nRF52832/AM263P) 디버깅 검증이 가장 불확실(드라이버·udev·프로브 실측). L1~L5는 비교적 기계적.

---

## 환원 후보 / 후속

- **L6 통과 시**: 보드별 Linux 디버깅 실측 결과를 각 프로젝트 wiki에 환원(드라이버·udev·프로브 거동 함정).
- **L7 산출**: 포팅된 `.sh` 런처는 [[windows_bat_ps1_launcher]]의 Linux 대응 절로 환원.
- **장기 후속 (로드맵 밖)**: Edge AI / TinyML 환경(Python 학습·변환 파이프라인·Docker·CUDA)은 [[linux_migration]] §2의 **장기 동인** — Linux 안정화 후 별도 로드맵으로 분리. 즉시 단계 아님.

---

## 함께 보기

- 결정·근거·portability·포팅 대상: [[linux_migration]]
