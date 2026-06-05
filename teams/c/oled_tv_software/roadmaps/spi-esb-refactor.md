---
tags: [roadmap, task, spi-esb-refactor, living-doc]
date: 2026-06-05
---

# SPI · ESB 리팩토링 — 작업 로드맵

> 한 작업(task) 단위 호. 프로젝트 전체 호는 [[roadmap]], 기능별 현황·다음 시작점은 [[status]].
> **사실 / 가설 / 모름을 구분. 추정은 "[추정]" 표기.** 현재 단계: **아이디어 (미착수).**

---

## 0. 한 줄 요약

SPI·ESB 코드를 리팩토링해 **다른 사람 작업과 병합(merge) 가능하게 정리**한다. 기능 추가가 아니라 구조 정리 트랙 — [[status]]의 "코드 정리 4개 라운드(별도 트랙)"를 흡수·확장한다.

---

## 1. 컨텍스트 (호의 배경)

- `_shared/oled_tv_protocol.{h,c}`가 **세 펌웨어(01/02/03) 공유 단일 소스** — `pkt_build`/`apply`/`print`, 11B ESB 와이어 패킷. (와이어 사양 [[esb_packet_format]], [[spi_packet_format]], [[rx_to_tx_packets]], [[tx_to_rx_packets]])
- 리팩토링·내부 코드 구조 재설계는 **사용자가 별도 후속으로 분리해둔 트랙** — 본 로드맵이 그 컨테이너.

---

## 2. 마일스톤 호 (= 코드 정리 4개 라운드)

```
[R1] 모니터 1-헤더-1-줄 압축
[R2] 공유 출력 함수 (oled_tv_protocol.c 신설, 3 빌드 등록)
[R3] serialize / deserialize 통합
[R4] SPI_PKT_* → 링크 중립 이름 개명
```

| 라운드 | 내용 | 완료 기준 | 상태 |
|--------|------|-----------|------|
| **R1** | 모니터 출력 1-헤더-1-줄 압축 | 3펌웨어 포맷 통일 | △ 구현·실보드 미검증 ([[status]] 모니터 절, `c9cf6a3`) |
| **R2** | 공유 출력 함수 (`oled_tv_protocol.c` 신설, 3 빌드 등록) | 3빌드 통과 | △ 구현·실보드 미검증 |
| **R3** | serialize / deserialize 통합 | 단일 build/apply 경로 | △ 부분 (`oled_tv_packet_t` 통명, [[status]]) |
| **R4** | `SPI_PKT_*` → 링크 중립 이름 개명 | 명칭 통일 | ✗ 미착수 |

> 위 4라운드는 monitor-formatting 작업 이후 분기된 정리 트랙. 상태 기호 단일 소스는 [[status]].

---

## 3. 현재 위치

→ 대부분 △(구현·미검증) 또는 미착수. merge 목적 정리는 실보드 검증과 병행. 기능별 현황은 [[status]].

---

## 4. 남은 일정 [추정]

| 단계 | 기간 추정 | 비고 |
|------|-----------|------|
| R1~R3 검증 | [추정] | 3펌웨어 실보드 모니터 검증 필요 (현재 △) |
| R4 | [추정] | 명칭 개명 — merge 충돌 최소화 타이밍 조율 |

---

## 5. 환원 후보

- R4 개명 완료 시 [[spi_packet_format]]·[[rx_to_tx_packets]]·[[tx_to_rx_packets]]의 `SPI_PKT_*` 표기 일괄 갱신.
- merge 후 `_shared/oled_tv_protocol.{h,c}` 인터페이스 변경 시 [[comm_state_monitoring]]·[[buck_vout_ref_command_path]]의 build/apply 참조 재확인.
