---
tags: [roadmap, task, spi-esb-refactor, living-doc]
date: 2026-06-09
---

# SPI · ESB 리팩토링 — 작업 로드맵

> 한 작업(task) 단위 호. 프로젝트 전체 호는 [[roadmap]], 기능별 현황·다음 시작점은 [[status]].
> **사실 / 가설 / 모름을 구분. 추정은 "[추정]" 표기.**
> **현재 단계 (코드 `9be1a7a` 기준): 코드가 이 호를 추월함** — R1~R3은 이미 부분 구현(공유 `_shared/oled_tv_protocol.{c,h}` + `pkt_build_*`/`pkt_apply_*`/`pkt_print_*`), R4(`SPI_PKT_*` 개명) 표기는 낡음(상수가 이미 링크 중립 `PKT_HDR_*`). 별 프레임의 적출 작업은 [[app_protocol_module]]에서 완료.

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

| 라운드 | 내용 | 완료 기준 | 상태 (코드 `9be1a7a`) |
|--------|------|-----------|------|
| **R1** | 모니터 출력 1-헤더-1-줄 압축 | 3펌웨어 포맷 통일 | △→✓(01) 구현 — `pkt_print_status_line`/`pkt_print_data_line` 1-헤더-1-줄. 01 동작확인([[app_protocol_module]]), 02/03 실보드 재검증 권장 |
| **R2** | 공유 출력 함수 (`oled_tv_protocol.c` 신설, 3 빌드 등록) | 3빌드 통과 | ✓ 구현 — `_shared/oled_tv_protocol.{c,h}` 신설, `pkt_print_*` 공유. 01 빌드·동작확인 완료 |
| **R3** | serialize / deserialize 통합 | 단일 build/apply 경로 | ✓ 대체로 — `pkt_build_tx`/`pkt_build_rx`/`pkt_apply_tx` 단일 경로 (`oled_tv_packet_t` 통명) |
| **R4** | ~~`SPI_PKT_*` → 링크 중립 이름 개명~~ | 명칭 통일 | **표기 낡음 — 코드에 `SPI_PKT_*` 없음, 이미 링크 중립 `PKT_HDR_*`**. R4 목표는 사실상 달성·무효 |

> **(사실)** 코드가 4라운드를 추월. `SPI_PKT_*`는 코드에 존재한 적 없고 상수는 `PKT_HDR_TX_STATUS=0x10`… 식 링크 중립 이름이다 → §5 환원의 "R4 개명 시 일괄 갱신"은 불필요. 상태 기호 단일 소스는 [[status]].

---

## 3. 현재 위치

→ R1~R3 부분 구현됨(공유 함수·링크 중립 상수), R4 무효. 01_RX_control은 [[app_protocol_module]] 적출로 빌드·동작확인 완료. 02/03 ESB 측 실보드 재검증·merge 타이밍이 남은 일. 기능별 현황은 [[status]].

---

## 4. 남은 일정 [추정]

| 단계 | 기간 추정 | 비고 |
|------|-----------|------|
| R1~R3 검증 | [추정] | 3펌웨어 실보드 모니터 검증 필요 (현재 △) |
| R4 | [추정] | 명칭 개명 — merge 충돌 최소화 타이밍 조율 |

---

## 5. 환원 후보

- ~~R4 개명 완료 시 `SPI_PKT_*` 표기 일괄 갱신~~ — **무효**: 코드에 `SPI_PKT_*` 없음, 이미 `PKT_HDR_*`(링크 중립). 갱신할 잔재 없음.
- merge 후 `_shared/oled_tv_protocol.{h,c}` 인터페이스 변경 시 [[comm_state_monitoring]]·[[buck_vout_ref_command_path]]의 build/apply 참조 재확인.

## 6. 남은 후속 라운드 — `_shared` 매크로 소유권 점검 (미착수)

**(사실)** `_shared/oled_tv_protocol.h`의 일부 매크로가 진짜 3펌웨어 공유인지 vs 01(SPI) 전용인지 불분명 — 점검 필요.

- **구체 사례**: `PACKET_INTERVAL`(=10ms, "SPI 전송 주기")은 `_shared`에 정의됐으나 **실제 호출은 01_RX_control(`app_protocol.c:141`) 한 곳뿐** — 02/03은 ESB 1ms 주기(`ESB_TX_INTERVAL_MS`)를 쓰고 `PACKET_INTERVAL`을 참조 안 함. **SPI 전용이므로 분리/개명 후보** (예: `SPI_PACKET_INTERVAL_MS`).
- 점검 범위: `_shared`의 각 매크로가 02/03에서도 실제 참조되는지 grep로 확인 → SPI 전용은 01 헤더로 이전 또는 `SPI_` prefix.
- **점검 대상 소멸 (`2f2aa65`)**: 구 COMM 라인 `esb_crc`=-1 항목은 `pkt_print_comm_line`이 **링크 전용 2인자**로 단순화되며 CRC 인자 자체가 삭제돼 더 이상 점검 대상이 아니다 ([[comm_state_monitoring]]).
