---
tags: [concept, am263p, edma, adc, dma, analysis, platform]
source: AM263P TRM ch07_5_controlss.md(ADC)·ch11_data_movement_edma.md(EDMA)·ch04_module_integration.md(DMA Requests) + MCU+ SDK v2 SysConfig dma_xbar/edma .meta 실측 + 8kw-ev-wpt-tx ADC 필터 전환 검토 세션 분석 (2026-06-29)
date: 2026-06-29
---

# AM263P EDMA의 ADC ring buffer 적재 적합성 (분석 — 결정 보류)

> **AM263P 플랫폼 분석 노트.** "고레이트 ADC 결과를 CPU 없이 ring buffer에 적재하려면 EDMA가 답인가"를 HW 근거·SDK 지원·실효 이득으로 따진 결과. **결정은 보류** — 채택 전 전제(85 kHz 실적재 + ISR 폭증)가 충족되어야 의미. 형제: [[am263p_adc_repeater_burst]](버스트가 출력 85 kHz를 만들어 ISR 폭증을 유발), [[am263p_adc_ppb_averaging]].

## 1. ADC→EDMA 연동 HW 근거 (읽어 확인)

- **TDMAEN으로 DMA read를 결과 래치 후로 정렬** — 찢김(torn read) 방지. `ADCCTL1.TDMAEN=1`이면 DMA 트리거가 EOC 결과 래치 후로 정렬되고, 0이면 tINT에 발생해 래치 전에 읽을 위험. (TRM `ch07_5_controlss.md`:2120, tDMA 행)
- **결과 레지스터가 메모리 버스 컨트롤러별로 복제** → 무경합. ADC 결과·PPB 결과는 시스템의 각 버스 컨트롤러(모든 R5FSS 코어 + DMA TC[0:1])마다 복제되어, 여러 컨트롤러가 동시에 읽어도 contention 없음·접근 설정 불요. (TRM :2467, 7.5.2.20.4 Result Register Mapping)
- **EDMA 이벤트는 DMA Trigger XBAR 경유** (TRM `ch11_data_movement_edma.md`:2589 "Events are mapped through DMA Trigger XBAR"; 헤더 11.2.6 :2587).
- **EDMA 자원**: DMA 채널 **64개**(TRM :349 Table 11-3, :205), 체인 동기(한 전송 완료가 다음 전송 트리거, :211), 2D/3D 전송(:229 — 소스·목적지 독립 인덱스, TPCC가 3번째 차원 관리). ★ "ping-pong"은 TRM의 명시 기능어가 아니라 **연결 PaRAM 세트(link set, :219)로 구성하는 응용 패턴**.
- 프로젝트에 EDMA 사용처 없음(MCSPI 선례 [[am263p_mcspi_controller]]만).

## 2. 핵심 빈자리 해소 — ADC를 EDMA 트리거로 쓸 수 있는가? (해소: 가능)

> 종전 미확정이던 "DMA Trigger XBAR에 ADC EOC/INT가 입력으로 매핑되는가"를 TRM·SDK 양쪽에서 확인 — **결론: SDK가 지원(가능)**. 단 TRM 표에는 누락.

- **TRM에는 ADC가 DMA 트리거 소스로 표에 없음.** ch04의 per-module "DMA Requests" 표는 I2C(:782)·SPI(:1068)·UART(:1392)·MMCSD·OSPI·MCAN·LIN·RTI(:3023)·MCRC·GPIO에만 있고 **ADC용 DMA Requests 표가 없다**(§4.1 ADC Integration :29–81은 그림뿐). `ch11`에는 "adc" 문자열 0건. → TRM만 보면 "ADC는 DMA로 못 받는다"는 오해 가능.
- **그러나 SDK SysConfig는 ADC INT를 DMA 크로스바 소스로 명시 제공** (읽어 확인):
  - `source/sysconfig/xbar/.meta/dma_xbar/soc/dma_xbar_am263px.syscfg.js`:69–93 — `ADC0_INT1..INT4` + `ADC0_EVTINT`(및 ADC1~ADC4 동일)을 DMA 크로스바 선택 소스로 열거. EPWM SOCA/SOCB도 같은 크로스바(:5–68).
  - `source/sysconfig/drivers/.meta/edma/soc/edma_am263px.syscfg.js`:88 — `masterXbarList: ["dma_trig_xbar"]` (EDMA 채널 트리거가 DMA trigger xbar 경유).
- ⇒ **ADC INT/EVTINT → DMA Trigger XBAR → EDMA 채널 적재는 SDK상 구성 가능.** 전 크로스바 입력의 완전한 열거는 TRM 표가 아니라 SDK `dma_xbar` 소스 목록에만 존재.

## 3. 분석 결론 (가설 — 결정 보류)

이 시나리오(**NoRTOS 단일코어 모니터링 경로**)에서 "CPU 절감 외 EDMA 이유"는 대부분 약하다. 실질 채택 이유는 둘뿐:

1. **고레이트 ISR 폭증 회피** — 85 kHz × 6채널 = **510k 이벤트/s**. 매 변환 ISR이면 R5F 부담 폭증. EDMA가 ring buffer에 적재하고 CPU는 블록 단위로 소비.
2. **리피터 버스트 burst-N 블록을 원자적으로 전송** — 한 트리거의 N개 결과를 묶어 DMA.

둘 다 **"실제 85 kHz 적재"를 전제**한다. PPB 누적(전환 전, 1.33 kHz)에선 EDMA가 무의미했다. **리피터 버스트(현재 N=16, 출력 85 kHz/인스턴스, [[am263p_adc_repeater_burst]])로 전환되면서 ISR 폭증이 실재**하게 됐다 — 이때부터 EDMA가 의미를 가진다.

**캐시 일관성은 이점이 아니라 비용**: EDMA가 부과하는 부담(R5F 캐시 + MPU 설정, DMA 버퍼 invalidate/clean)이며, EDMA를 정당화하지 않는다.

## 4. 사실 / 가설 / 모름 가름

- **사실 (HW·SDK)**: §1 TDMAEN·결과레지스터 복제·EDMA 자원, §2 ADC INT가 dma_xbar 소스 — 전부 TRM/SDK 인용 확정.
- **가설 (분석)**: §3 "EDMA 실질 이유는 ISR 폭증 회피·burst 원자전송 둘뿐", "캐시는 비용" — 설계 판단이며 프로파일링 미수행.
- **빈자리 (채택 전 — 봉합 말 것)**:
  - **EDMA-ADC 경로 미실증** — SDK 구성 가능은 확인했으나 8kw에서 실제 결선·동작 미수행. ring buffer 적재 ISR 폭증 회피 효과 미측정.
  - **ISR 폭증 실측 미수행** — 85 kHz×6채널 ISR이 R5F @400 MHz에서 실제로 한계인지 사이클 프로파일 없음. (SW 이동평균 CPU 부하 추정 ~784 사이클/ISR도 [추정] — [[adc]] §A6.)
  - **결정 보류** — 위 둘이 측정되기 전엔 EDMA 채택 판단 보류. 현 단계는 SW 이동평균(ISR write)을 먼저 구현해 DMA 검증과 분리하는 것이 권장순서([[adc]] §A6).

## 관련 페이지

- [[am263p_adc_repeater_burst]] — 버스트가 출력 85 kHz를 만들어 ISR 폭증(EDMA 동기)을 유발.
- [[am263p_adc_ppb_averaging]] — 누적 모드(1.33 kHz)에선 EDMA 무의미했던 이유.
- [[am263p_mcspi_controller]] — 프로젝트의 유일한 기존 EDMA 사용 선례(MCSPI 20 MHz EDMA).
- [[am263p_trm]] — ch07_5(ADC tDMA·결과레지스터)·ch11(EDMA)·ch04(per-module DMA Requests, ADC 누락).
