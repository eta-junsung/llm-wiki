---
tags: [concept, flash, ospi, jtag, tooling, node, am263p, 8kw-ev-wpt-tx]
source: 코드 분석 + 실측 (2026-06-17, 8kw-ev-wpt-tx cleanup 브랜치 — tools/ospi_flash/ rename, argv 구조 확인)
date: 2026-06-17
---

# OSPI flash 툴링 — tools/ospi_flash/ 메커니즘과 진입 구조

> **8kw-ev-wpt-tx 정본.** 이름은 "JTAG flash"지만 동작은 XDS110/JTAG로 **헬퍼 펌웨어를 타겟 RAM에 올린 뒤 그 헬퍼가 OSPI를 굽는** 구조다. 진입 경로·mcelf 소스 분기·DSLite 경합 함정을 기록한다. 클린 호스트 규율 상세는 [[jtag_flash_clean_host]].

---

## 1. 위치

```
tools/ospi_flash/           ← 현재 이름 (구: tools/jtag_flash/ — 2026-06-17 cleanup rename)
  run.bat                   ← Windows 진입점
  launcher.mjs              ← Node.js ESM 런처
  flash_node_8kw.js         ← 실제 플래시 로직 (DSS API 호출)
```

`tools/jtag_flash/`는 2026-06-17 cleanup 브랜치에서 `tools/ospi_flash/`로 rename됐다. 동작이 "JTAG 전송"이 아니라 "JTAG 경유 OSPI 굽기"라 `ospi_flash`가 정확한 이름.

---

## 2. 메커니즘

```
XDS110 / JTAG
    │
    └─ ds.configure → openSession → loadProgram(jtag_flasher.out)
            ↓  헬퍼 펌웨어가 타겟 R5F RAM에서 실행
            ↓  AutoCmd 구조체 (0x70038000) — op / offset / size 기록 + MAGIC trigger
            ↓  헬퍼가 status 폴링 후 완료 응답
            ↓
    IS25LX256 (OSPI flash)
            ├─ @0x00000000 → SBL  (sbl_ospi_am263p.tiimage)
            └─ @0x00081000 → app  (*.mcelf)
```

`ERASE_ALL → SBL write → app write` 순서를 한 런에 완주한다. SBL 없이 app만 굽으면 전원사이클 후 standalone 부팅 불가([[jtag_flash_clean_host]] §"Run > Flash Project" 금지).

---

## 3. 진입 구조 — argv 흐름

```
run.bat
  └─ node launcher.mjs [--source release|build]
        └─ flash_node_8kw.js
              process.argv[3]  ←  "--source release" 또는 "--source build"
```

- `launcher.mjs`는 `argv[2]`(스크립트 경로)만 소비하고, **`argv[3]` 이후는 그대로 보존해** flash 스크립트에 전달.
- `--source release`(기본): `Release/` 하위 `.mcelf` 선택 — CCS IDE managed build 산출물.
- `--source build`: `build/` 하위 `.mcelf` 선택 — 수제 gmake 산출물.
- **소스 자동 선택 fallback**: `Release/`와 `build/`의 mtime을 비교해 더 최신 쪽을 선택하고 콘솔에 출력. 굽기 전 해당 경로 빌드 완료가 전제.

두 빌드 갈래 상세: [[syscfg_build_model]].

---

## 4. DSLite 경합·콜드스타트 함정

| 원인 | 증상 | 해소 |
|------|------|------|
| CCS IDE(Theia) 상주 DSLite 경합 | 런마다 다른 단계 실패 — 비일관성이 함정 | **CCS IDE 완전 종료** 후 재시도 |
| DSLite 백엔드 콜드스타트 지연 | 첫 `ds.configure()` 30s ScriptingTimeoutError | IDE 종료 확인 후 재시도 |
| 고아 `node`/`DSLite` 프로세스 잔존 | 단일 런 지속 실패 | 작업관리자에서 프로세스 직접 종료 |

`getDebugSessions=[]`가 빈 배열이어도 cloudagent가 띄운 DSLite는 백그라운드에 상주할 수 있다 — **세션 목록 비어 있음 ≠ 백엔드 내려감**. 프로세스 레벨로 확인해야 한다.

상세: [[jtag_flash_clean_host]] §클린 호스트 확인법.

---

## 5. 사실 / 모름

- **FACT**: 동작은 JTAG 전송이 아닌 "헬퍼를 RAM에 올려 OSPI를 굽는" 방식.
- **FACT**: `ERASE_ALL → SBL@0x00000000 → app@0x00081000` 순서.
- **FACT**: `--source release|build` argv로 mcelf 소스 분기, mtime fallback 자동 선택.
- **FACT**: CCS IDE 상주 DSLite와 독립 스크립팅 경합 → 비일관 실패 (2026-06-05 실측 [[jtag_flash_clean_host]]).
- **모름**: PowerShell 래퍼(`-Source` param 형식)의 현재 파일 존재 여부 — 이번 세션 미확인.

---

## 함께 보기

- 클린 호스트 규율 + "Run > Flash Project" 금지 상세: [[jtag_flash_clean_host]]
- OSPI 부트모드 스트랩(SW1 정답 `0,0,1,1`): [[ospi_boot_mode_strap]]
- 부팅 진단 채널·triage recipe: [[ospi_boot_console_diagnostic]]
- 두 빌드 갈래(CCS vs gmake) + generated/ 커밋 필수: [[syscfg_build_model]]
