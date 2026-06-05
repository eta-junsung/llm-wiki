---
tags: [concept, mcspi, spi, am263p, s6, diagnosis]
source: [[am263p_trm]] §13.1.3 (raw/am263p_trm/ch13_1_general_connectivity.md, 원본 p.1146–1196)
date: 2026-06-05
---

# AM263P MCSPI 컨트롤러 (host측 SPI)

AM263P MCSPI(SPI0)의 **이해된 동작** — S6 블로커 `SPI not responsive!`/`CMD_ERR_TIMEOUT`(host↔CC33xx SPI 무응답) 진단용. host SPI 컨트롤러가 *어떻게 동작하도록 설정돼야 하나*를 TRM에서 환원. 실제 런타임 설정은 코드 `spi_adapt.c`(MCSPI 래퍼)·syscfg가 단일 소스 — 이 페이지는 그 설정을 읽고 판정하는 레퍼런스.

이 데모는 [[am263p_trm]]의 **첫 demand-ingest 예시**(TRM 섹션 → concept 환원 패턴). 원본 표·비트필드는 raw [`ch13_1_general_connectivity.md`](../../raw/am263p_trm/ch13_1_general_connectivity.md) §13.1.3.

> **레이어 구분**: 핀이 어느 헤더에 나오나 = [[lp_am263p_ug]], host SPI IP 동작 = 여기(TRM), CC33xx 칩측 SPI 기대 = [[cc3351_datasheet]].

---

## 확정 사실 (TRM §13.1.3)

- **8개 SPI 모듈**. `SPI0`·`SPI4`만 **CS 2개**, 나머지는 1개. 이 프로젝트는 `SPI0` 사용(프로젝트 [[CLAUDE]] 하드웨어 절: MCSPI `SPI0` 20MHz EDMA).
- **컨트롤러 모드 최대 50 MHz** / 타겟 25 MHz. (status R36 실측 SCLK~16 MHz는 이 범위 내 — 클록 자체는 정상.)
- DMA 지원(채널별 read/write req). **단일 채널만 FIFO** 사용 가능.
- 핵심 레지스터: `MCSPI_CHCONF_0..3`(채널 설정), `MCSPI_CHCTRL`(EN), `MCSPI_CHSTAT`(TXS/RXS/EOT), `MCSPI_TX/RX`, `MCSPI_IRQSTATUS`, `MCSPI_XFERLEVEL`(FIFO).

## CS 프레이밍 — S6 미결 직결 ★

status 미결 "**CS 프레이밍 정합 미확인** — `csDisable=FALSE`(연속 assert) vs CC33xx SDK 워드별 deassert 기대"를 TRM 비트로 환원:

- **`MCSPI_CHCONF[20] FORCE`** — 1이면 SPIEN[i](=CS)를 **워드 사이에도 active로 유지**(연속 assert). 수동 assertion은 single-controller 모드에서만.
- **`MCSPI_CHCONF[6] EPOL`** — CS 극성. 0=active-low, 1=active-high.
- **`MCSPI_CHCONF[22-21] SPIENSLV`**(CHCONF_0 전용) — peripheral 모드에서 CS를 채널0로 재라우팅.

→ **판정 포인트**: CC33xx SDK가 **워드별 CS deassert**를 기대하는데 host가 `FORCE=1`(연속 assert)로 두면 프레이밍 불일치로 NP가 명령을 인식 못해 `CMD_ERR_TIMEOUT` 가능. `spi_adapt.c`/syscfg의 `csDisable`·FORCE·EPOL 설정을 CC33xx 기대치와 대조할 것. (가설 — 실측·코드 확인 필요.)

## 클록·모드 정합

- **Bit rate**: 50 MHz 기준클럭 ÷ `MCSPI_CHCONF[5-2] CLKD`. (`CHCONF[29]` 확장 CLKD=0일 때.) 1→50MHz, 2→25, 4→12.5, 8→6.25 MHz … (Table 13-20).
- **SPI 모드**: `MCSPI_CHCONF[1] POL` × `[0] PHA` → Mode 0~3 (Table 13-21). **CC33xx가 기대하는 모드와 반드시 일치**해야 함 — 불일치면 비트 정렬이 깨져 무응답.
- **워드 길이**: `MCSPI_CHCONF[11-7] WL` (4~32bit). `[13-12] TRM` = TX-only/RX-only/TX-and-RX.

## 전송 시퀀스 (single-channel)

1. 채널 enable: `MCSPI_CHCTRL[0] EN=1` → 첫 enabled 채널이 SPIEN[i] activate(설정된 극성).
2. `MCSPI_TX` 적재 → 전송 시작(`CHSTAT[1] TXS` 조건).
3. 완료: `MCSPI_CHSTAT[2] EOT=1`, 수신은 shift→`MCSPI_RX`, `IRQSTATUS` RXx_FULL.
4. 채널 전환 전 EOT 대기 후 disable.

## EDMA·인터럽트 결선

- **EDMA**: `SPI0`는 read req 4개(`spi0_dma_read_req[0..3]`) + write req 4개, **EDMA_XBAR**(Level) 경유 → [[am263p_trm]] ch11(EDMA) / §13.1.3 DMA Requests 표(raw p.~1180대). EDMA 채널↔XBAR 매핑 syscfg 확인 후보.
- **인터럽트**: `SPI0_intr` = VIM **IN_INTR20**(Level) → ch10 §10.4.1 R5FSS0_CORE0 Interrupt Map.

## 미확인 / 다음

- `spi_adapt.c` 실제 CHCONF 값(FORCE/EPOL/POL/PHA/CLKD) vs CC33xx SDK 기대치 대조 — **미수행**.
- WLAN_IRQ(`PR0_PRU0_GPIO10`)는 MCSPI 인터럽트와 별개(PRU-ICSS GPIO) → [[am263p_trm]] ch07_3 candidate.
- S6 진단 history는 [[flash_open_diagnostic_log]] R32~R38, 사실은 [[flash_open_facts]].

## 백링크

[[am263p_trm]] · [[lp_am263p_ug]] · [[status]] · [[flash_open_facts]] · [[cc3351_datasheet]] · [[boosterpack_pinmap]]
