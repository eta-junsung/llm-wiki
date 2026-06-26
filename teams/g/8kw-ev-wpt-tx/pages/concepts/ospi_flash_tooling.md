---
tags: [concept, flash, ospi, jtag, tooling, node, am263p, 8kw-ev-wpt-tx]
source: 코드 분석 + 실측 (2026-06-17 cleanup 브랜치 rename; 2026-06-26 PR #10 — launcher.mjs 제거·항상 build/ 반영)
date: 2026-06-26
---

# OSPI flash 툴링 — tools/ospi_flash/ 메커니즘과 진입 구조

> **8kw-ev-wpt-tx 정본.** 이름은 "JTAG flash"지만 동작은 XDS110/JTAG로 **헬퍼 펌웨어를 타겟 RAM에 올린 뒤 그 헬퍼가 OSPI를 굽는** 구조다. 진입 경로·mcelf 소스 분기·DSLite 경합 함정을 기록한다. 클린 호스트 규율 상세는 [[jtag_flash_clean_host]].

---

## 1. 위치

```
tools/ospi_flash/                           ← (구: tools/jtag_flash/ — 2026-06-17 rename)
  run_flash_node_8kw.sh                     ← Linux 진입점
  run_flash_node_8kw.ps1                    ← Windows 진입점
  flash_node_8kw.js                         ← 실제 플래시 로직 (DSS API 호출, :29에 헬퍼 경로)
  Release/ospi_flasher.out                  ← 헬퍼 FW 바이너리 (.gitignore negation으로 추적)
  targetConfigs/AM263Px.ccxml               ← XDS110 타겟 설정 (.gitignore negation으로 추적)
```

2026-06-17: `tools/jtag_flash/` → `tools/ospi_flash/` rename, `run.bat`+`launcher.mjs` → OS별 `run_flash_node_8kw.{sh,ps1}` 대체(PR #10 2026-06-26). 내부 변수·파일명 `jtag_flasher` → `ospi_flasher` 일괄 정정(`flash_node_8kw.js:29` 포함).

### 추적 바이너리 자산 (.gitignore negation)

`Release/ospi_flasher.out`와 `targetConfigs/AM263Px.ccxml`는 CCS 빌드 산출물이 아닌 **고정 자산**이지만, 상위 `.gitignore`가 `Release/`·`*.ccxml`을 ignore할 수 있어 negation으로 강제 추적한다:

```gitignore
# tools/ospi_flash/.gitignore
!Release/ospi_flasher.out
!targetConfigs/AM263Px.ccxml
```

fresh clone 후 이 파일들이 없으면 `loadProgram(ospi_flasher.out)` 단계에서 즉시 실패한다.

---

## 2. 메커니즘

```
XDS110 / JTAG
    │
    └─ ds.configure → openSession
         │
         └─ loadProgram(Release/ospi_flasher.out)   ← 헬퍼 FW를 타겟 R5F RAM에 적재
                ↓  auto_check_marker 브레이크포인트에서 멈춤 (헬퍼 초기화 완료 신호)
                ↓
         flash_node_8kw.js가 gCmd@0x70038000 에 명령 구조체 기록
                  op      ← ERASE_ALL / WRITE_SBL / WRITE_APP
                  offset  ← 0x00000000(SBL) / 0x00081000(app)
                  size    ← 바이트 길이
         gFileBuf@0x70040020 에 파일 데이터 스트림 기록
         MAGIC 트리거 → 헬퍼 resume → status 폴링 → 완료 응답
                ↓
    IS25LX256 (OSPI flash)
            ├─ @0x00000000 → SBL  (C:/ti/sbl_ospi_am263p.tiimage)
            └─ @0x00081000 → app  (build/*.mcelf 또는 Release/*.mcelf)
```

`ERASE_ALL → SBL write → app write` 순서를 한 런에 완주한다. SBL 없이 app만 굽으면 전원사이클 후 standalone 부팅 불가([[jtag_flash_clean_host]] §"Run > Flash Project" 금지).

SBL 파일 출처·재빌드 레시피: [[sbl_ospi_provenance]] (실테스트 확증 후 작성 예정).

---

## 3. 진입 구조

```
run_flash_node_8kw.sh   (Linux)   ┐
run_flash_node_8kw.ps1  (Windows) ┘
  └─ ~/ti/ccs2100/ccs/scripting/run.sh   (Linux)
     C:\ti\ccs2100\ccs\scripting\run.bat (Windows)
        └─ flash_node_8kw.js  ← DSS API 글로벌 inject 후 실행
```

**flash 소스는 `build/`로 고정** (`flash_node_8kw.js:51` `APP_MCELF = "../../build/8kw-ev-wpt-tx.mcelf"`). `-Source` 인자는 PR #10에서 제거됐다 — 빌드가 gmake 단일로 통합됐기 때문.

SBL 경로: `join(TI_DIR, "sbl_ospi_am263p.tiimage")`. `TI_DIR`는 환경변수 `TI_DIR`로 덮을 수 있고 미설정 시 Linux=`$HOME/ti`, Windows=`C:/ti`(`flash_node_8kw.js:28`).

두 빌드 갈래 역사: [[build_methods]], [[syscfg_build_model]].

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
- **FACT**: 헬퍼 바이너리명 `ospi_flasher.out` (구 `jtag_flasher.out`, 2026-06-17 rename).
- **FACT**: `gCmd@0x70038000`(명령 구조체) + `gFileBuf@0x70040020`(파일 스트림) + `auto_check_marker` BP (코드 분석).
- **FACT**: flash 소스는 `build/`로 고정(`flash_node_8kw.js:51`). `-Source` 인자 없음(PR #10 제거).
- **FACT**: `Release/ospi_flasher.out`·`targetConfigs/AM263Px.ccxml` .gitignore negation 추적 (2026-06-17 확정).
- **FACT**: CCS IDE 상주 DSLite와 독립 스크립팅 경합 → 비일관 실패 (2026-06-05 실측 [[jtag_flash_clean_host]]).
- **모름**: `C:/ti/sbl_ospi_am263p.tiimage`가 SDK LP prebuilt 그대로인지 8kw 보드 OSPI 핀맵에 맞춰 재빌드한 것인지 — fresh clone 실테스트로 확증 예정([[sbl_ospi_provenance]]).

---

## 함께 보기

- 클린 호스트 규율 + "Run > Flash Project" 금지 상세: [[jtag_flash_clean_host]]
- OSPI 부트모드 스트랩(SW1 정답 `0,0,1,1`): [[ospi_boot_mode_strap]]
- 부팅 진단 채널·triage recipe: [[ospi_boot_console_diagnostic]]
- 두 빌드 갈래(CCS vs gmake) + generated/ 커밋 필수: [[syscfg_build_model]]
