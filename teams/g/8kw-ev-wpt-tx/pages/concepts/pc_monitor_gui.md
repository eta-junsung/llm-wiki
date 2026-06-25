---
tags: [concept, tool, pc-gui, uart, monitor, deadtime, host, 8kw-ev-wpt-tx]
source: 펌웨어 repo branch uart5 (commit ba241fa·979699d) + dead-time 컨트롤 추가 (commit 785b848, 2026-06-12) + 실보드 검증 2026-06-11 + 2026-06-25 main 재확인(런처·경로·범위 정정)
date: 2026-06-25
subsystem: 8kw-ev-wpt-tx, host
---

# PC GUI — 8kW WPT TX ADC 모니터 + Dead-time 빌드/플래시 컨트롤

LP-AM263P 8kW WPT TX 보드의 **하드웨어 엔지니어용 호스트 툴**. 두 역할 통합:

1. **ADC 텔레메트리 모니터** — UART5로 송출하는 18B 바이너리 스트림 수신·표·플롯·CSV 로깅.
2. **Dead-time 빌드/플래시 컨트롤** — `ETA_DEADTIME_NS` 설정값 변경 → 빌드 → JTAG 플래시를 GUI 원클릭으로.

- **파일**: `tools/gui/gui.py`
- **스택**: Python + pyserial + Tkinter + matplotlib
- **기준 커밋**: `785b848` (feat(gui): dead-time 빌드/플래시 컨트롤·헤드리스 CLI 추가)
- **실보드 검증**: ADC 모니터 `ba241fa`(2026-06-11), dead-time CLI `785b848`(2026-06-12)
- 선례: c팀 oled [[pc_uart_gui]] (양방향·buck 지령). 이 GUI는 ADC는 수신 전용, dead-time은 출력 제어(write/build/flash).

---

## 레이아웃 (785b848 기준)

창 크기: 1100×720 (비율 조정 가능).

```
┌──────────── 포트 선택 / 연결 헬스 바 / CSV 로그 버튼 ─────────────┐
│ 왼쪽 칼럼                          │ 오른쪽: Live Plot (V)          │
│  ┌ ADC Channels ─────────────────┐ │                               │
│  │ 체크 | Channel | ADC(V) | 12b | Phys │                         │
│  │  ×6 채널 행                    │ │                               │
│  └───────────────────────────────┘ │                               │
│  ┌ Deadtime ─────────────────────┐ │                               │
│  │  [경로 정보 박스 5줄]          │ │                               │
│  │  Dead-time(ns): [Spinbox] [현재값읽기] │                       │
│  │  [Build & Flash 버튼]          │ │                               │
│  │  주황 안내 라벨                 │ │                               │
│  │  [로그 scrolledtext]           │ │                               │
│  └───────────────────────────────┘ │                               │
└────────────────────────────────────┴───────────────────────────────┘
```

---

## ADC Channels 표

| 컬럼 | 내용 |
|------|------|
| 포함 | 채널 플롯·CSV 포함 체크박스 |
| Channel | 채널 이름 (색상 라벨, 채널별 고정색) |
| ADC(V) | `mV/1000.0` (full-precision), 소수 **3자리** |
| ADC(12bits) | raw count 0~4095 |
| Physical | 계수 테이블 산출 물리량 (계수 미입수 → `— V/A`) |

- mV = `raw * 3300 // 4095` (펌웨어 `eta_adc.c` 정수식 미러, thin-device/smart-host 패턴).
- Physical 계수 테이블: `PHYSICAL_COEFF[]` 배열 단일 소스 — 계수 입수 시 한 곳만 수정하면 전 채널 반영.

### 채널 순서 (ETA_ADC_CH enum)

| idx | 채널명 | ADC 인스턴스 | Physical 상태 |
|-----|--------|-------------|--------------|
| ch0 | Temp_Module2 | ADC1 SOC0 | ✓ NTC Beta (°C) |
| ch1 | Temp_Module1 | ADC2 SOC0 | ✓ NTC Beta (°C) |
| ch2 | GA_Vin | ADC3 SOC0 | ✓ SCALE≈353.39 (V) |
| ch3 | I_LCC_SEN | ADC4 SOC0 | ✗ 미교정 (`— A`) |
| ch4 | I_COIL_SEN | ADC0 SOC0 | ✓ SCALE≈6.770 A/V |
| ch5 | GA_Iin_SEN | ADC1 SOC1 | ✓ SCALE=10 A/V |

변환식 상세 → [[adc_scaling]].

---

## Dead-time 빌드/플래시 컨트롤 (785b848 추가)

### 경로 상수 (코드 내 자동 해결)

```
REPO_ROOT     → gui.py 위치에서 3단계 위 (frozen exe 실행 시 4단계)
TUNING_H      → REPO_ROOT/src/eta_bsp/eta_tuning.h
BUILD_DIR     → REPO_ROOT/build
FLASH_SCRIPT  → REPO_ROOT/tools/ospi_flash/run_flash_node_8kw.{ps1,sh}  # OS 분기: win=.ps1 / 그 외=.sh
gmake         → ①build/config.mk CCS_PATH → ②PATH → ③C:\ti\ccs*\...\gmake.exe 최신본
```

> 종전 본 페이지가 `tools/jtag_flash/`·"PATH→C:\ti 폴백 2단계"로 적었던 것은 stale — flash 경로는 `tools/ospi_flash/`로 rename(2026-06-17)되고 `.sh` OS 분기가 추가됐으며, gmake 탐색은 config.mk를 1순위로 두는 3단계다 (2026-06-25 main 실측 정정).

### GUI 사용 순서

1. Spinbox에 원하는 Dead-time (ns, **100~500 범위**) 입력
2. **Build & Flash** 클릭 → `[write] → [build] → [flash]` 단계별 로그 출력
3. flash 완료 후 **전원 사이클** 실시

### 내부 시퀀스 (`run_build_flash`)

```
do_write → write_deadtime_ns(dt_value)   # eta_tuning.h regex 치환
do_build → gmake -C build all            # subprocess.Popen, stdout streaming
do_flash → (win) powershell -File run_flash_node_8kw.ps1 | (그 외) bash run_flash_node_8kw.sh
→ (True, "완료") | (False, 사유)
```

- 빌드 로그는 실시간 스트리밍으로 로그창에 표시.
- 버튼은 실행 중 disabled, 완료/실패 시 복귀.
- GUI·CLI 양쪽 공유 — `log` 콜백만 다름(GUI: queue / CLI: print).

### 헤드리스 CLI (검증 자동화 경로, 보존 필수)

```sh
python gui.py --read                                   # 현재 ETA_DEADTIME_NS 출력
python gui.py --deadtime 150 --write --build --flash   # 빌드+플래시 자동화
```

dead-time silicon 검증 워크플로([[pwm_deadtime_knob_verify]])에서 이 CLI로 4점 스윕 실시.  
**GUI 개선 시 CLI 인터페이스(`--read/--deadtime/--write/--build/--flash`)를 반드시 보존할 것.**

---

## 기능 (모니터 공통)

- **채널 체크박스**: 플롯 트레이스 + CSV 로깅 포함을 채널별 토글.
- **패킷 헬스**: 레이트(Hz) / SEQ 드롭 / CRC 에러 카운트.
- **라이브 플롯**: matplotlib embed, 200샘플 슬라이딩 윈도우.
- **CSV 로깅**: raw-only(파생값 아님), Start 시점 채널 고정.

## 패킷 리더 — SOF 동기 + CRC 재동기

[[uart5_packet_protocol]] §수신측 재동기와 동일:
- SOF(0xA5) 탐색 → LEN/TYPE 게이트 → CRC-16/CCITT-FALSE 검증 → 실패 시 1바이트 슬라이드.
- ASCII 잡음·가짜 SOF는 자연 폐기.

## 검증 (실보드, 2026-06-11)

COM13(CP210x, J1.4→THVD1400→J24) 29.8 s: **10.067 Hz, 301프레임 전부 유효, SEQ 드롭 0·CRC 에러 0**.  
프레이밍 강건성: 정상 디코드 / 1바이트 손상 재동기 / ASCII 잡음·가짜 SOF 폐기 후 복구 — 전부 PASS.

---

## 실행·배포

- **권장 실행**: OS별 shim → `launch.py`가 venv 자동 생성·의존성 설치 후 `gui.py` 기동. 메커니즘·결정은 [[gui_launch_architecture]].
  - Linux/macOS: `tools/gui/run-gui-linux.sh`  / Windows: `tools/gui/run-gui-windows.bat`  / 직접: `python3 tools/gui/launch.py`
- **수동 실행**: `pip install -r tools/gui/requirements.txt`(pyserial==3.5·matplotlib==3.11.0) 후 `python tools/gui/gui.py`.
- **PyInstaller exe — 현재 미구현(intent-trace만).** `gui.py`의 `sys.frozen` 분기(frozen 시 `sys.executable` 기준 4단계 위=REPO_ROOT)와 `tools/gui/.gitignore`의 `build/`·`dist/`는 exe 빌드를 의도한 흔적이나 **`.spec`·`dist/`·exe 모두 repo에 부재**(2026-06-25 실측). 배포는 py 스크립트 + 런처로 확정([[gui_launch_architecture]] §3). 종전 "8kw-gui.exe ~39 MB 존재" 서술은 무효였음.

---

## 다음 개선 항목 백로그

기준: `785b848`. 하드웨어 엔지니어 운영 편의 위주. 항목별 현황 → 요청/결정.

---

### 1. 상태 배너 (일부 구현됨 → 강화 요청)

**현황**: 로그창(scrolledtext)에 `[write]/[build]/[flash]/[done]/[FAILED]` 단계 메시지 출력. 주의 라벨에 "flash 후 전원 사이클 필요" 표기 있음.

**요청**: 큰 상태 배너 추가 — 로그 스크롤 없이 한눈에 상태 확인.
- 배너 색상 구분: 진행 중=노랑(`#ffcc00` 배경) / 완료=초록 / 실패=빨강
- flash 완료 시 "전원 사이클 하세요" 모달 또는 큰 강조 안내 (엔지니어가 놓치지 않도록)
- 로그창은 상세 단계 기록용으로 유지 (병존, 제거 아님)

---

### 2. 경로 정보 박스 — 표시 범위 결정 (결정 항목)

**현황**: "경로 정보" 박스에 5줄 (Repo root / eta_tuning.h / Build dir / Flash script / gmake 탐색 결과) 표시. 창 너비를 많이 차지.

**결정 필요**:

| 옵션 | 내용 | 고려사항 |
|------|------|----------|
| (a) 그대로 유지 | 풀 경로 5줄 그대로 | 경로 문제 진단 용이, 폭 많이 차지 |
| (b) 가용성만 축약 | gmake·flash script 있음/없음만 색상 표시 | 핵심 정보 유지, 공간 절약 |
| (c) 디버그 토글 | "경로 상세 보기" 체크박스로 접기 | 평상시 깔끔, 초기 설정 때만 펼침 |

핵심 질문: 하드웨어 엔지니어 배포본에서 풀 경로 상시 노출이 필요한가. (b)나 (c) 권장.

---

### 3. 안내문 순서 정리 (일부 구현됨 → 보강 요청)

**현황**: 주황색 안내 라벨 — "flash 전 CCS IDE 종료 / 보드 부트모드 SW1=0,0,1,1(xSPI 8D SFDP) 확인 / flash 후 전원 사이클 필요".

**요청**: 사용 순서 대로 재구성, 번호 매기기.

```
① Dead-time 값 입력 (100~400 ns)
② CCS IDE 종료 확인
③ SW1=0,0,1,1 (xSPI 8D SFDP) 확인
④ Build & Flash 클릭
⑤ flash 완료 후 전원 사이클 실시
```

항목 3과 항목 1 연동: flash 완료 배너(#1)와 이 순서 안내가 합쳐지면 엔지니어가 전원 사이클을 놓칠 가능성 최소화.

---

### 4. 최종 배포 형태 결정 — ✅ 결정됨 (2026-06-25)

**결정**: **(b) py 스크립트 + OS별 런처** 채택. exe·브라우저·단일명령 통합 **불채택**. 근거(제로설치 청중 부재·deadtime 개발등급 환경 의존·OS 양쪽 더블클릭 단일 파일 부재)는 [[gui_launch_architecture]] §3. 종전 "exe 존재" 전제는 사실 오류였음(.spec·dist·exe 부재).

---

### 5. ADC Channels 폭 축소 + Live Plot 확대 (신규)

**현황**: 좌측 ADC Channels 표 LabelFrame 가로폭이 내용 대비 넓어 우측 플롯 공간을 압박.

**요청**: 
- ADC Channels 표 컬럼 width 합산 값에 딱 맞게 LabelFrame 폭을 축소 (minsize 또는 컬럼 width 재조정)
- Deadtime 섹션도 동일하게 좌측 칼럼 폭을 최소화
- 줄어든 만큼 우측 Live Plot이 `expand=True`로 자동 확대

---

### 6. Build & Flash 버튼 위치 이동 (신규)

**현황**: 
```
행 A: Dead-time(ns): [Spinbox] [현재값 읽기]
행 B: [Build & Flash]
```

**요청**: Build & Flash를 행 A로 올려 동일 행에 배치.
```
행 A: Dead-time(ns): [Spinbox] [현재값 읽기] [Build & Flash]
```

구현: `btn_frame`을 `dt_frame`에 통합하거나 `dt_frame`에 버튼 추가. 버튼 너비 조정 필요.

---

### 7. ADC Channels 채널명 굵게 (신규)

**현황**: Channel 컬럼 채널명이 색상 라벨이나 `font` 파라미터 없어 일반(normal) 굵기.

```python
# 현재 (gui.py:553)
name_lbl = tk.Label(ch_frame, text=name, width=14, anchor="w", fg=colors[i])
```

**요청**: bold로 표시해 가시성 향상.
```python
name_lbl = tk.Label(ch_frame, text=name, width=14, anchor="w",
                    fg=colors[i], font=("TkDefaultFont", 9, "bold"))
```

항목 7은 1줄 변경으로 구현 가능 — 다른 항목과 함께 또는 단독으로 선적용 가능.

---

## 빈자리 (미해결)

- **Physical 컬럼 I_LCC_SEN** — 변환 계수 미입수, `— A` 유지 ([[adc_scaling]] §ch3). 5채널은 교정 완료.
- UART5 온보드 XDS110 가상 COM 미지원 — **외부 CP210x(COM13)로만** PC 도달.

---

## 관련

- [[gui_launch_architecture]] — 어떻게 띄우나(launch.py venv 부트스트랩·OS shim) + 배포 형태 현행 유지 결정
- [[uart5_packet_protocol]] — 18B wire 프레임·CRC·재동기 계약
- [[adc_pinmap]] — ADC 6채널·계수 입수 시 채울 스펙 목록
- [[pwm_deadtime_knob_verify]] — dead-time knob CLI 활용 silicon 검증 결과
- [[pc_uart_gui]] — c팀 oled 선례 (양방향·buck 송신)
