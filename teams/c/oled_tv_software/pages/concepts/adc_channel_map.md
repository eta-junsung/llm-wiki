---
tags: [concept, adc, pinmap, sensing]
source: projects/c/oled_tv_software/01_RX_control/{RX_control.ioc, Application/Src/app_adc.c, Application/Src/common.c, Application/Inc/common.h}
date: 2026-05-22
subsystem: 01_RX_control
---

# ADC 채널 매핑 (01_RX_control)

[[rx_control]] 보드의 ADC1 6채널 매핑 + 평가보드 시험 시 전압 인가 가이드. ADC 데이터는 `sensing_data` → `rx_module.rx_data` → SPI([[spi_packet_format]]) → 무선 → Tx 측으로 전파된다.

## 데이터 흐름

```
ADC 핀 ─→ ADC1 (6ch scan, continuous) ─DMA1_Ch1 circular─→ sensing_data (uint16×6)
                                                              ↓ adc_calc()
                                                         rx_module.rx_data (float)
                                                              ↓ 패킷화
            SPI2 → nRF52 SPIS1 ([[rx_ble_module]]) ─ESB─→ Tx 측
```

## 채널 표 (rank = DMA 버퍼 순서)

| sensing_data 필드 | STM32 핀 | 보드 라벨 | ADC ch | rank | Sampling | wire 패킷 도착지 |
|---|---|---|---|---|---|---|
| `vrect`       | **PA0** | `VRECT_ADC` | IN0  | 1 | 1.5 cy  | [[rx_to_tx_packets]] 0x51 Buffer[0..1] |
| `irect`       | **PA1** | `IRECT_ADC` | IN1  | 2 | 1.5 cy  | 0x51 Buffer[2..3] |
| `vout`        | **PA2** | `VOUT_ADC`  | IN2  | 3 | 1.5 cy  | 0x52 Buffer[0..1] |
| `iout`        | **PA3** | `IOUT_ADC`  | IN3  | 4 | 1.5 cy  | 0x52 Buffer[2..3] |
| `stack_temp1` | **PC4** | `TEMP2_ADC` ⚠ | IN14 | 5 | 13.5 cy | 0x52 Buffer[4..5] (Rx Power Stack #1 온도) |
| `stack_temp2` | **PC5** | `TEMP1_ADC` ⚠ | IN15 | 6 | 13.5 cy | 0x52 Buffer[6..7] (Rx Power Stack #2 온도) |

- V/I 채널 sampling = 1.5 cy (낮은 임피던스 센서). 온도 = 13.5 cy (NTC + 풀업, 임피던스 높음).
- 핀들은 `MspInit`에서 `GPIO_MODE_ANALOG`, 풀업/풀다운 없음.

## ⚠ TEMP1 / TEMP2 라벨 swap

`RX_control.ioc`의 GPIO_Label:
- PC4 → `TEMP2_ADC`
- PC5 → `TEMP1_ADC`

하지만 `MX_ADC1_Init()` (`app_adc.c`)은 **PC4(CH14)를 rank 5**, **PC5(CH15)를 rank 6**으로 등록.
DMA 버퍼 구조체 순서:

```c
typedef struct {
    uint16_t vrect, irect, vout, iout, stack_temp1, stack_temp2;
} rx_adc_raw_data_t;       // _shared/oled_tv_protocol.h:140-148
```

→ 결론:
- `sensing_data.stack_temp1` = PC4 = 보드 라벨 **`TEMP2_ADC`**
- `sensing_data.stack_temp2` = PC5 = 보드 라벨 **`TEMP1_ADC`**

**보드 silkscreen `TEMP1_ADC`(PC5)에 전압 인가 → 패킷 "Rx Power Stack #2 온도"로 도착**. 적어도 한쪽(보드 라벨 vs SW 필드명) 중 하나는 swap 상태. 시험·디버깅 시 라벨 그대로 믿지 말고 본 표 기준.

**회로도 XML 좌표 분석으로 해소 (2026-05-27):** [[schematic_rx_regulator_control_board]] 회로도 MCU 페이지에서 오프페이지 커넥터 좌표 추출 결과, `TEMP1_ADC_uC` 신호(회로도 명칭)가 PC4(절대 Y=440)에 연결됨이 좌표 일치로 확인. 즉 **회로도는 PC4를 TEMP1로 정의**하고, `.ioc`가 PC4에 `TEMP2_ADC`를 붙인 것이 Swap의 원인. `.ioc` GPIO_Label이 틀린 것.

## Front-end 스케일 (현재 미적용)

`common.h:17-25`에 분압비 상수가 정의됨:

| 상수 | 값 | 용도 |
|---|---|---|
| `ADC_VRECT_R102`    | 560.0  | Vrect 분압 |
| `ADC_IRECT_R116`    | 1000.0 | Irect 션트 → OP 게인 |
| `ADC_BUCK_VOUT_R125`| 560.0  | Vout 분압 |
| `ADC_BUCK_IOUT_R130`| 1000.0 | Iout 션트/게인 |
| `ADC_BUCK_IOUT_R133`| 2000.0 | Iout 션트/게인 (2단) |
| `ADC_TEMP1_R131`    | 2200.0 | TEMP1 풀업 |
| `ADC_TEMP1_R136`    | 3300.0 | TEMP1 분압 |
| `ADC_TEMP2_R137`    | 2200.0 | TEMP2 풀업 |
| `ADC_TEMP2_R140`    | 3300.0 | TEMP2 분압 |
| `ADC_BUCK_VOUT_R128`| — | **DNP/미실장** — 사용 금지 ([[rx_control]] 주의 사항) |

NTC 모델 (`common.h:27-31`): R0=10 kΩ, T0=298.15 K, β=3570, 풀업 10 kΩ @ VCC=5 V.

**현재 `adc_calc()`(`common.c:157-172`)는 raw → 0~3.3 V 변환만 하고 위 상수를 적용하지 않음**. 따라서 `rx_module.rx_data.vrect` 등에 들어가는 값은 "핀에 인가된 전압(0~3.3 V)" 그대로. 0.01 V 스케일 uint16 wire 변환은 별도 단계에서 이뤄지는지 — SPI 송신 코드 ingest 시 확인 필요.

## 평가보드 시험 가이드

1. **전압 인가**: 가변 DC 전원(0~3.3 V) 또는 가변 저항(3.3 V ↔ GND 분압)을 위 표의 STM32 핀에 직접 연결. ADC 핀은 풀업/풀다운 없으므로 무인가 시 floating — 측정값 의미 없음.
2. **검증 경로(빠른 순)**:
   - SWD: `sensing_data.<필드>` raw 값 watch (가장 직접적)
   - SPI 후단: nRF 측 SPIS RX 버퍼 (`tx_module` 구조체 명명 함정 — [[rx_ble_module]] 참조) 덤프
   - 무선 후단: Tx 측에 도달한 패킷 (0x51/0x52) 로깅
3. **온도 채널 NTC 시험**: 실제 NTC 사용 시 보드의 5 V 풀업 회로(`common.h` NTC_VCC_V=5.0f) 필요. 가변 전압원만으로 시험하면 펌웨어상 NTC 모델 (β/R0) 미적용이라 raw V만 통과.
4. **TEMP 라벨 swap 주의** (위 §). 의도한 wire 도착지에서 값이 안 보이면 PC4↔PC5 바꿔 시도.

## 출처

- `01_RX_control/RX_control.ioc` — ADC1 channel, sampling, GPIO_Label
- `01_RX_control/Application/Src/app_adc.c` — `MX_ADC1_Init`, `adc_conv`, DMA start
- `01_RX_control/Application/Src/common.c:157-172` — `adc_calc()`
- `01_RX_control/Application/Inc/common.h:17-31` — Front-end 상수 + NTC 모델
- `_shared/oled_tv_protocol.h:140-148` — `rx_adc_raw_data_t`
