# 8kw-ev-wpt-tx — 도메인 schema

## 프로젝트 성격

**8kW EV 무선전력전송(WPT) 송신 보드 Ver1.0E00** 펌웨어 개발.
MCU 플랫폼: **LP-AM263P** (TI AM263P LaunchPad).
보드: eta 자체 설계 8kW WPT 송신 보드 — LP-AM263P J3 커넥터로 eta 보드와 연결.

전체 진행 상황은 [[roadmap]], 현재 위치·다음 시작점은 [[status]].

---

## 하드웨어 커넥터

LP-AM263P ↔ eta WPT TX 보드는 J3 커넥터로 연결. 신호 대응은 작업별 엔티티 페이지에 기록:

- ADC 신호: [[adc_pinmap]]

---

## 페이지 분류

| 레이어 | 페이지 | 성격 | 갱신 |
|--------|--------|------|------|
| 전략(프로젝트) | [[roadmap]] | 목표·작업 호 인덱스·현재 위치 | 게이트 통과 시 |
| 전술 | [[status]] | 다음 시작점·기능별 현황·미결 사항 | 매 라운드 |
| 작업 로드맵 | `roadmaps/<task>.md` | 작업 단위 호(단계 spine·완료 기준) | 게이트 통과 시 |

그 외 concept/entity/source는 루트 `CLAUDE.md` 컨벤션을 따른다.

---

## status 갱신 절차

루트 `CLAUDE.md` "파이프라인 — status 갱신 절차" 준수. `status.md` 위치: `teams/g/8kw-ev-wpt-tx/status.md`.
