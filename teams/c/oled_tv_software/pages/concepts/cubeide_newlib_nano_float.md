---
tags: [concept, build, toolchain, cubeide, newlib_nano, gotcha, rx_control]
source: 01_RX_control/.cproject + CubeIDE 설정 (사용자 세션 2026-06-05)
date: 2026-06-05
subsystem: 01_RX_control
---

# CubeIDE newlib-nano float 빌드 설정 (함정)

`01_RX_control`은 newlib-nano C 라이브러리로 빌드된다. nano 버전은 코드 크기를 줄이려고 **printf/scanf의 float 지원을 기본으로 뺀다.** float 입출력이 필요하면 링커 플래그로 명시 활성화해야 한다 — 안 켜면 컴파일·링크는 통과하지만 런타임에 소수 처리가 조용히 깨진다.

## 두 플래그

| 플래그 | `.cproject` 키 | 링커 옵션 | 영향 |
|---|---|---|---|
| printf float | `nanoprintffloat=true` | `-u _printf_float` | `printf("%f")` 등 float **출력** |
| scanf float | `nanoscanffloat=true` | `-u _scanf_float` | `sscanf("%f")` 등 float **입력** |

`01_RX_control/.cproject` 현황:
- `nanoprintffloat=true` — **Debug 구성에만** 설정됨.
- `nanoscanffloat=true` — **이번 세션(2026-06-05)에 활성화.**

> **꺼져 있을 때의 증상**: `buck 15.5` 같은 소수 인자를 `sscanf("%f")`로 받는 [[uart_command_set]] `buck`/`freq` 등이 소수부를 못 받아 값이 깨진다. nanoscanffloat가 이 경로의 선결 조건 — [[buck_vout_ref_command_path]].

## GUI 경로 (CubeIDE)

```
Project Properties
  → C/C++ Build → Settings
  → [Tool Settings] → MCU/MPU Settings
  → ☑ "Use float with printf/scanf from newlib-nano
        (-u _printf_float / -u _scanf_float)"
```

## 주의 — 구성(Configuration)별로 따로 산다

- 위 플래그는 **빌드 구성(Debug/Release)마다 독립**이다. 현재 printf float은 **Debug 구성에만** 있다.
- **Release 빌드로 전환하면 두 플래그 모두 재확인** 필요 — Debug에서 되던 float 입출력이 Release에서 조용히 깨질 수 있다.

## 관련 페이지

- [[uart_command_set]] — `buck`/`freq`의 `sscanf("%f")` 소수 인자 파싱
- [[buck_vout_ref_command_path]] — `buck` float 입력 → RF 지령 경로
- [[rx_control]] — 01_RX_control 보드/빌드 환경
