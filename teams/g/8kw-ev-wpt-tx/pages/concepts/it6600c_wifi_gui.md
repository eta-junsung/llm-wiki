---
tags: [concept, tool, equipment, it6600c, scpi, 8kw-ev-wpt-tx]
source: GitHub 이슈 #9 (2026-06-26)
date: 2026-06-26
---

# IT6600C 양방향 전원공급장치 WiFi 연동 PC GUI

> GitHub 이슈 #9. ITECH IT6600C Bi-directional Power Supply를 LAN/WiFi로 연결해 실시간 전압·전류·전력 데이터를 수신·표시하고 CSV 로깅하는 PC 도구.
> 당장 착수 예정 없음 — 나중에 이어갈 수 있도록 기록.

---

## 1. 장비

**ITECH IT6600C** — 양방향 전원공급장치. 회사 공통 계측 장비 인벤토리: [[instruments]].

---

## 2. 요청 기능

- LAN/WiFi로 IT6600C 연결
- PC GUI에서 실시간 전압·전류·전력 데이터 수신 및 표시
- CSV 로깅

---

## 3. 설계 검토

### 통신 프로토콜

IT6600C는 **SCPI(Standard Commands for Programmable Instruments) over LAN(VISA/TCP)** 지원. 일반적인 쿼리 패턴:

```
MEAS:VOLT?   → 전압
MEAS:CURR?   → 전류
MEAS:POW?    → 전력
```

확인 필요: IT6600C 원격제어 매뉴얼 (VISA 포트 번호·SCPI 명령셋 확정).

### 구현 방식

`tools/` 하위 신설. 선례: [[pc_monitor_gui]] (`tools/gui/gui.py`, Python + Tkinter + pyserial).

| 옵션 | 비고 |
|------|------|
| Python + `pyvisa` + Tkinter | 선례 스택 — VISA 어댑터로 SCPI 쿼리, Tkinter GUI |
| Python + `socket` (raw TCP) | `pyvisa` 없이 직접 소켓 — 설치 의존성 최소 |
| Node.js + Electron | GUI 완성도 높지만 배포 무거움 |

**권장 방향**: Python + `pyvisa`(또는 raw TCP) + Tkinter — 기존 개발환경 재사용, [[pc_monitor_gui]]와 동일 스택.

### CSV 로깅

Python `csv` 모듈, 타임스탬프 + 전압/전류/전력 컬럼.

---

## 4. 미결

- IT6600C 통신 인터페이스 확정 (LAN vs USB, VISA 주소 포맷)
- SCPI 명령셋 IT6600C 매뉴얼 교차확인
- 샘플링 주기 결정 (표시 갱신 주기 / CSV 로깅 주기)
- `tools/it6600c/` 또는 `tools/gui/` 하위 위치 결정
