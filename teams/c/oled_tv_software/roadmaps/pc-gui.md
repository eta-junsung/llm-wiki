---
tags: [roadmap, task, pc-gui, living-doc]
date: 2026-06-10
---

# PC GUI — 작업 로드맵

> 한 작업(task) 단위 호. 프로젝트 전체 호는 [[roadmap]], 기능별 현황·다음 시작점은 [[status]].
> **사실 / 가설 / 모름을 구분. 추정은 "[추정]" 표기.** 현재 단계: **완료 (`35b94d0`, 2026-06-10 실보드 검증).** 산출물 [[pc_uart_gui]].

---

## 0. 한 줄 요약

PC에서 **UART로 받은 패킷 데이터를 모니터링** + **`buck` 커맨드를 설정**하는 간단한 GUI. 펌웨어 변경 없이 기존 UART 인터페이스 위에 얹는 호스트 툴. **구현·실보드 검증 완료** — `tools/pc_uart_gui/uart_gui.py`(Python+Tkinter+pyserial), [[pc_uart_gui]].

---

## 1. 마일스톤 호

```
[G0] 포트/포맷 결정 ✓ — UART5 단일 포트, monitor 텍스트→바이너리 전환
        ▼
[G1] 시리얼 읽기 + 11B 바이너리 파서 ✓ (HDR 동기+CRC 재동기)
        ▼
[G2] buck 설정 입력 → UART5 송신 ✓
        ▼
[G3] 실시간 모니터 뷰 ✓ (2컬럼 헤더별 값 + 링크 표시)
```

| 단계 | 달성 목표 | 완료 기준 | 상태 |
|------|-----------|-----------|------|
| **G0** | 어느 UART에 무엇을 붙일지 결정 | 포트·포맷 확정 | ✓ UART5 단일 포트, 포맷 텍스트→11B 바이너리 전환 결정 |
| **G1** | monitor 출력 파싱 | 11B 라인 → 구조화 데이터 | ✓ HDR 동기 + CRC 재동기 리더 |
| **G2** | buck 설정 송신 | GUI 입력 → 01 UART5 → 0x51 반영 확인 | ✓ `buck <v>\r` 송신, 0x51 `Tx_Buck_Vout_Ref` 확인 |
| **G3** | 실시간 뷰 | 헤더별 값 갱신 표시 | ✓ 2컬럼(TX/RX) + `Link: SPI/ESB [UP/DOWN]` |

---

## 2. G0 결정 결과 (해소)

> 미착수 시점엔 "포트 2개 조합 미정"이었으나, `35b94d0`에서 다음으로 확정·닫힘:

- **단일 포트 UART5**: 설정(`buck`)·모니터를 **01_RX_control UART5 한 포트**로 처리. (구 안: 모니터를 03 Monitor/01 Monitor_Loop 별도 포트로 받는 방안 — 채택 안 함.)
- **포맷 = 텍스트→바이너리 전환**: 구 텍스트 통일포맷(`[eta-tx>>eta-rx]` 등) 대신 01이 **11B 바이너리 패킷**을 송출하도록 펌웨어를 바꿨다([[comm_state_monitoring]] "monitor 바이너리 전환"). GUI는 11B를 HDR 동기+CRC로 파싱 — command 응답 텍스트 잡음은 자연 폐기.

---

## 3. 현재 위치

→ **완료·실보드 검증**(`35b94d0`). 산출물·구현 상세 [[pc_uart_gui]]. 기능별 현황은 [[status]].

- **남은 검증 항목**: SPI 끊김 시 0x10 d0 bit5 → 0 낙하로 `Link: SPI DOWN`이 정확히 뜨는지 실보드 확인([[comm_state_monitoring]] 보류 절).

---

## 4. 환원 후보 (반영 완료)

- ✓ 산출물 페이지 [[pc_uart_gui]] 생성, monitor 바이너리 전환은 [[comm_state_monitoring]]·[[app_protocol_module]]에 반영.
- ✓ G0 포트/포맷 결정 닫힘 — 위 §2.
