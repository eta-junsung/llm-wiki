---
tags: [concept, flash, jtag, ospi, am263p, tooling, gotcha, 8kw-ev-wpt-tx]
source: 실측 (2026-06-05, 8kw-ev-wpt-tx JTAG flash 세션)
date: 2026-06-05
---

# JTAG flash 굽기는 CCS IDE를 완전히 내린 클린 호스트에서

> **운영 함정(environment gotcha).** AM263P OSPI를 JTAG로 굽는 **host-driven 스크립팅**과 CCS IDE는 **같은 디버그 백엔드를 두고 경합**한다. 펌웨어·보드를 의심하기 전에 호스트 상태부터 본다.

---

## 한 줄 규칙

**AM263P OSPI를 JTAG로 굽기 전, CCS IDE(Theia)를 완전히 종료한다.** IDE를 켜둔 채 flash 스크립트를 돌리면 런마다 다른 지점에서 죽는다.

---

## 무엇이 경합하는가

| 경로 | 디버그 백엔드 | IDE 상태 요구 |
|------|--------------|--------------|
| host-driven flash 스크립팅 (`run.bat` / Node.js `flash_node.js`, 또는 DSS Rhino) | 독립 DSLite 세션 | **IDE 꺼짐** |
| MCP `loadProgram` (IDE 경유 RAM 로드) | CCS IDE의 상주 cloudagent+DSLite | **IDE 켜짐** |

CCS IDE(Theia)는 백그라운드에 **cloudagent + DSLite 디버그 백엔드**를 상주시킨다. 독립 flash 스크립트가 `ds.configure()` / `openSession` / `resume`로 같은 백엔드(프로브)에 접근하려 하면 두 주체가 한 디버그 백엔드를 두고 경합한다.

→ **MCP loadProgram(IDE 켜짐)과 독립 flash 스크립팅(IDE 꺼짐)은 양립 불가.** 한쪽을 쓰려면 다른 쪽 전제를 깨야 한다.

---

## 증상 — 비일관 실패라서 위험하다

IDE를 켜둔 채 flash를 돌리면 **런마다 다른 지점**에서 죽는다:

- 30s `ScriptingTimeoutError`
- `DebugServer.1` timeout
- `rd32 Error 0x400000`
- `ds.configure()` / `openSession` / `resume` 중 임의 단계 실패

비일관성 자체가 함정이다 — **펌웨어 결함·보드 결함으로 오인하기 쉽다.** 같은 .out·같은 보드인데 결과가 흔들리면 호스트 경합을 1순위로 의심한다.

---

## 증거 (2026-06-05, 8kw-ev-wpt-tx)

flashwriter `.out` **바이트 동일**(펌웨어 무죄 — 변경 없음)인데:

| 호스트 상태 | 결과 |
|------------|------|
| **IDE 켜둠** | `ERASE_ALL` 실패 |
| **IDE 완전 종료** | **6/6 OK 완주** |

펌웨어 동일·보드 동일·.out 바이트 동일 → 변수는 IDE 상주 여부 하나뿐. 호스트 경합이 단독 원인임을 격리 입증.

---

## 클린 호스트 확인법 — `getDebugSessions=[]`를 믿지 마라

**`getDebugSessions`가 빈 배열(`[]`)이라도 cloudagent가 띄운 DSLite는 상주할 수 있다.** 세션 목록이 비었다 ≠ 백엔드가 내려갔다.

→ **프로세스 레벨로 확인한다**: 작업관리자에서 `node` / `DSLite` 프로세스 잔존 여부를 본다. CCS IDE 창을 닫아도 cloudagent/DSLite가 백그라운드에 남아 있으면 프로세스를 직접 종료한 뒤 flash를 돌린다.

---

## ⚠️ "Run > Flash Project" 사용 금지

CCS Theia 메뉴의 **Run > Flash Project**는 SBL(`sbl_ospi_am263p.tiimage`)을 **플래시하지 않는다**.

- 앱 바이너리만 굽고 SBL은 건드리지 않는다.
- SBL 없이는 **전원 사이클 후 standalone 부팅 불가**.
- 이 방법으로 굽고 파워 사이클 후 부팅이 안 된다면 SBL 누락이 원인.

**올바른 플래시 절차**:
1. CCS IDE 완전 종료 (위 클린-호스트 규칙 준수)
2. `tools/ospi_flash/run.bat` 실행 (`ERASE_ALL → SBL@0x00000000 → app@0x00081000` 순서)
3. 전원 사이클

---

## 함께 보기

- **flash 툴링 메커니즘 전체** (헬퍼 RAM 로드·AutoCmd·mcelf 소스 분기·argv 구조): [[ospi_flash_tooling]]
- **JTAG flash 하네스 정본(lp-am263p)**: [[jtag_flash_harness]] — 이 클린-호스트 규율을 포함한 굽기 도구 전체(runAsynch 하네스 vs DSS Rhino·파워 사이클·standalone 부팅 검증). 이 페이지는 그중 클린-호스트 함정의 deep-dive.
- 프로젝트 현재 위치·다음 시작점: [[status]] · 전략 spine: [[roadmap]]
- AM263P 부트 플래시(IS25LX256)·OSPI 디버그 맥락: [[flash_open_facts]] (lp-am263p) — 단, 그쪽은 **app `Flash_open()` 블로커**(런타임)이고, 이 페이지는 **굽는 호스트 환경**(flash-time) 함정으로 층위가 다르다.
- 프로브 인벤토리: [[instruments]]
