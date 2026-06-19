# pwm_deadtime_knob_verify — raw 데이터

**날짜**: 2026-06-12  
**브랜치**: v1_0e00  
**목적**: `ETA_DEADTIME_NS` knob → flash → VCC 전원사이클 → silicon 핀 출력 검증

---

## 디렉토리 구조

```
pwm_deadtime_knob_verify/
├── measure.py          # 분석 스크립트 (전 설정 공통 로직)
├── dt100/leg1/digital.csv   # 100 ns, 레그1 (HS1+LS1)
├── dt100/leg2/digital.csv   # 100 ns, 레그2 (HS2+LS2)
├── dt150/leg1/digital.csv   # 150 ns, 레그1
├── dt150/leg1/capture.sal   # 150 ns, 레그1 (Saleae 보조 원본)
├── dt150/leg2/digital.csv   # 150 ns, 레그2
├── dt150/leg2/capture.sal   # 150 ns, 레그2 (Saleae 보조 원본)
├── dt250/leg1/digital.csv   # 250 ns, 레그1
├── dt250/leg2/digital.csv   # 250 ns, 레그2
├── dt400/leg1/digital.csv   # 400 ns, 레그1
└── dt400/leg2/digital.csv   # 400 ns, 레그2
```

정본은 **digital.csv** (텍스트·전이 기반·자기설명). `.sal`은 Saleae Logic2 보조 원본.

---

## CSV 채널 매핑

헤더: `Time [s], Channel 0, Channel 1`  
포맷: transition-based (상태 변화 행만 기록, 500 MS/s = 2 ns 격자)

| 파일 | Channel 0 | Channel 1 |
|------|-----------|-----------|
| leg1/digital.csv | **HS1** — J4.39, EPWM2_A (레그1 High-Side) | **LS1** — J4.40, EPWM2_B (레그1 Low-Side) |
| leg2/digital.csv | **HS2** — J6.52, EPWM4_A (레그2 High-Side) | **LS2** — J6.51, EPWM7_B (레그2 Low-Side) |

레그1: 단일 모듈 dead-band (EPWM2 RED/FED).  
레그2: 2-compare 합성 (EPWM0 fan-out + EPWM4_A/EPWM7_B 비대칭 AQ).

---

## 분석 재현

```sh
python measure.py
```

`measure.py` 내 경로는 원본 소스 경로 기준. wiki 복사본에서 실행 시 경로를 아래로 수정:

```python
analyze(r"<wiki_root>/teams/g/8kw-ev-wpt-tx/raw/pwm_deadtime_knob_verify/dt100/leg1/digital.csv", "HS1","LS1","LEG1")
analyze(r"<wiki_root>/teams/g/8kw-ev-wpt-tx/raw/pwm_deadtime_knob_verify/dt100/leg2/digital.csv", "HS2","LS2","LEG2")
```

결과 해석 정본: [[pwm_deadtime_knob_verify]]
