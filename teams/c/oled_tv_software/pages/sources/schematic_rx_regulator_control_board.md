---
tags: [source, schematic, hardware]
source: projects/c/oled_tv_software/docs/Schematic/Rx_OLED_Regulator_Control_Board_260327.pdf
source_alt: Downloads/rx_oled_regulator_control_board_260327.xml
date: 2026-05-27
subsystem: 01_RX_control
---

# 회로도 — Rx OLED Regulator Control Board (260327)

`01_RX_control` 실제 양산 설계 보드 회로도. OrCAD Capture Design XML + PDF 조합으로 ingest.

- **PDF**: 이미지 기반 — 블록 배치 파악용
- **XML**: OrCAD Design XML (68,941줄) — 신호명·핀맵·컴포넌트 텍스트 추출용

원본 경로:
- raw 사본: `teams/c/oled_tv_software/raw/Rx_OLED_Regulator_Control_Board_260327.pdf` (immutable)
- 프로젝트 원본: `projects/c/oled_tv_software/docs/Schematic/Rx_OLED_Regulator_Control_Board_260327.pdf`
- `rx_oled_regulator_control_board_260327.xml` (OrCAD 17.4 Design XML export)

---

## MCU 식별

OrCAD 라이브러리 파트명 `STM32F042C6T6`는 오기. `PartValue` 필드 및 핀 집합 기준 실제 칩:

- **STM32F103VCT6 / LQFP64** (또는 동등 핀 호환품)
- Footprint: TQFP-64 0.5mm, 레퍼런스: **U1**
- 동일 핀 번호·기능 → [[rx_control]] 문서의 STM32F103RCT6와 동일 계열

---

## 회로도 페이지 구성

| 페이지 | 이름 | 주요 내용 |
|---|---|---|
| 01 | Schematic_Information | 표지·개정 이력 |
| 02 | MCU_Peripheral_Section | MCU U1 전체 핀 배치 + 7개 서브블록: STM32 Pin Assign / ST-LINK SWD 커넥터 / **OSC Clock (8MHz)** / System Reset 회로부 / 디버깅용 LED Indicator / Boot Mode Selection / Bypass Capacitor. OSC 회로는 아래 "OSC Clock (8MHz)" 절 참조 |
| 03 | LPF_Analog_Signal | ADC 전처리 LPF, 온도 센서, PWM_TZ |
| 04 | UI_Comm | CAN 트랜시버, DAC, UART→RS232, 전원 |
| 05 | Board_to_Board_Connector | PWM 출력, 커넥터 인터페이스 |
| 80 | Components_Placement | PCB 부품 배치도 |
| 90 | Revision_History | 개정 이력 |

---

## 주요 컴포넌트

| 레퍼런스 | 종류 | 비고 |
|---|---|---|
| U1 | STM32F103VCT6 | MCU (라이브러리 오기: STM32F042C6T6) |
| U (AD712) | Op-amp | 아날로그 신호 처리 |
| U (MAX232A) | RS-232 레벨 변환 | UART → RS232 브리지 |
| U (SI8421) | 디지털 아이솔레이터 | 절연 |
| U (EMI_FILTER) | EMI 필터 | CAN 등 |
| ISO (OPTO ISOLATOR-A) | 포토커플러 | |
| Q (KRC101S) | NPN BJT | 드라이버 |
| Q (MOSFET P) | P-MOSFET | 전원 스위치 |
| SW (SW DIP-5) | DIP 스위치 5극 | |
| J (CON10A, CON10) | 10핀 커넥터 | 보드간 |
| X1 | 8 MHz 크리스탈 | HSE 소스, 5032 패키지(5.0×3.2mm). OSC Clock 절 |
| C2, C3 | 22 pF 부하 커패시터 | 마킹 220J, 50V, 1608. 각 OSC_IN/OSC_OUT ↔ DGND |
| R10 | 1 MΩ 피드백 저항 | 마킹 1MF, 1608. 크리스탈 병렬 |
| R11 | 0 Ω 직렬 저항 | 마킹 0RF, 1608. OSC_OUT 직렬 |

---

## MCU 신호 인벤토리

### _uC 신호 (MCU 직접 연결, 39개)

| 신호명 | MCU GPIO | 페리퍼럴 | 근거 |
|---|---|---|---|
| VRECT_ADC_uC | PA0 | ADC1_IN0 | 심볼 Alt Func |
| IRECT_ADC_uC | PA1 | ADC1_IN1 | 심볼 Alt Func |
| VOUT_ADC_uC | PA2 | ADC1_IN2 | 심볼 Alt Func |
| IOUT_ADC_uC | PA3 | ADC1_IN3 | 심볼 Alt Func |
| DACA_OUT_uC | PA4 | DAC_OUT1 | 심볼 Alt Func |
| DACB_OUT_uC | PA5 | DAC_OUT2 | 심볼 Alt Func |
| PWM_TZ_uC | PA6 | TIM8_BKIN (remap) | [[rx_control]] 기존 확인 |
| CAN_RX_uC | PA11 | CAN_RX | 심볼 Alt Func |
| CAN_TX_uC | PA12 | CAN_TX | 심볼 Alt Func |
| TMS_uC | PA13 | JTMS/SWDIO | 심볼 Alt Func |
| TCK_uC | PA14 | JTCK/SWCLK | 심볼 Alt Func |
| TDO_uC | PB3 | JTDO | 심볼 Alt Func |
| SPI_nCS_uC | PB12 | GPIO (SW NSS) | 심볼 Alt Func |
| SPI_CLK_uC | PB13 | SPI2_SCK | 심볼 Alt Func |
| SPI_MISO_uC | PB14 | SPI2_MISO | 심볼 Alt Func |
| SPI_MOSI_uC | PB15 | SPI2_MOSI | 심볼 Alt Func |
| TEMP1_ADC_uC | **PC4** | ADC1_IN14 | 좌표 매칭 Y=440 |
| TEMP2_ADC_uC | **PC5** | ADC1_IN15 | 좌표 매칭 Y≈450 |
| PWM1_P_uC | PC6 | TIM8_CH1 | 심볼 Alt Func + [[rx_control]] |
| PWM1_N_uC | PC7 | TIM8_CH2 | 심볼 Alt Func + [[rx_control]] |
| PWM2_P_uC | PC8 | TIM3_CH3 | 심볼 Alt Func + [[rx_control]] |
| PWM2_N_uC | PC9 | TIM3_CH4 | 심볼 Alt Func + [[rx_control]] |
| UART5_TX_uC | PC12 | UART5_TX | 심볼 Alt Func |
| UART5_RX_uC | PD2 | UART5_RX | 심볼 Alt Func |
| OSC_IN_uC | OSC_IN (핀5) | HSE 크리스탈 입력 | 회로도 p.2 vision 판독 (OSC Clock 절) |
| OSC_OUT_uC | OSC_OUT (핀6) | HSE 크리스탈 출력 (R11 0Ω 경유) | 회로도 p.2 vision 판독 (OSC Clock 절) |
| BOOT0_uC | BOOT0 | 부트 설정 | 심볼명 |
| BOOT1_uC | PB2 | BOOT1 | 심볼 Alt Func |
| nSTM32_RST_uC | NRST | 리셋 | 심볼명 |
| FAULT_RST_uC | 미확인 | GPIO | XML 신호명만 확인 |
| LATCH_FAULT_uC | 미확인 | GPIO | XML 신호명만 확인 |
| nSYS_RDY_uC | 미확인 | GPIO (active low) | XML 신호명만 확인 |
| DBG_LED1_uC | 미확인 | GPIO | XML 신호명만 확인 |
| DBG_LED2_uC | 미확인 | GPIO | XML 신호명만 확인 |
| DBG_LED3_uC | 미확인 | GPIO | XML 신호명만 확인 |
| TEST_MODE1_uC | 미확인 | GPIO | XML 신호명만 확인 |
| TEST_MODE2_uC | 미확인 | GPIO | XML 신호명만 확인 |
| LSG1_OP_SEL_uC | 미확인 | GPIO | Load Sharing Gate 1 |
| LSG2_OP_SEL_uC | 미확인 | GPIO | Load Sharing Gate 2 |

### _CN 신호 (보드간 커넥터 인터페이스, 24개)

MCU 신호와 1:1 대응되는 커넥터 신호 목록. 페이지 05(Board_to_Board_Connector)에서 라우팅.

**커넥터 CN1 — Rx Power Board행 (전원 진입점)** (회로도 p.5 vision 판독):

- 부품: `HEADER_2.0mm / 28P` (TMM-114-06-T-D-SM), 2.0 mm 피치 2열(14×2). 라벨 "연결@Rx OLED Regulator Power B/D" — 평소 전력보드에서 이 헤더로 3.3V·GND·신호가 들어온다.
- **핀 1·2 = PD3V3** (보드 3.3V 레일), **핀 27·28 = DGND**. 가운데 핀(3~26)은 `*_CN` 신호(PWM1/2·LSG1/2·FAULT_RST·nSYS_RDY·LATCH_FAULT·PWM_TZ 등).
- PD3V3는 페이지 02 Bypass 블록의 페라이트 비드(B1)를 거쳐 MCU **VDD**로, DGND는 OSC 블록(C2/C3 접지)과 공통 → **CN1.1/27에 3.3V/GND 주입 시 MCU·OSC 회로가 정규 경로로 전원을 받음**. (단 HSE 발진은 펌웨어 `HSEON` 필요 — OSC Clock 절 "함의" 참조.)
- ⚠ 페이지 05엔 보드투보드 헤더가 2개(CN1 = @Rx Power Board / 별도 = @BLE Module Board). 페이지 02의 ST-LINK 커넥터 `CON1`과는 다른 부품이니 혼동 주의.

| _uC 신호 | _CN 신호 | 비고 |
|---|---|---|
| VRECT_ADC_uC | VRECT_ADC_CN | |
| IRECT_ADC_uC | IRECT_ADC_CN | |
| TEMP1_ADC_uC | TEMP1_ADC_CN | |
| TEMP2_ADC_uC | TEMP2_ADC_CN | |
| VOUT_ADC_uC | — | 로컬 센싱, 커넥터 없음 |
| IOUT_ADC_uC | — | 로컬 센싱, 커넥터 없음 |
| PWM1_P_uC | PWM1_P_CN | |
| PWM1_N_uC | PWM1_N_CN | |
| PWM2_P_uC | PWM2_P_CN | |
| PWM2_N_uC | PWM2_N_CN | |
| PWM_TZ_uC | PWM_TZ_CN | |
| SPI_CLK_uC | SPI_CLK_CN | |
| SPI_MISO_uC | SPI_MISO_CN | |
| SPI_MOSI_uC | SPI_MOSI_CN | |
| SPI_nCS_uC | SPI_nCS_CN | |
| FAULT_RST_uC | FAULT_RST_CN | |
| LATCH_FAULT_uC | LATCH_FAULT_CN | |
| LSG1_OP_SEL_uC | LSG1_OP_SEL_CN | |
| LSG2_OP_SEL_uC | LSG2_OP_SEL_CN | |
| nSYS_RDY_uC | nSYS_RDY_CN | |
| UART5_TX_uC | SCIB_TXD232_CN | RS232 레벨 변환 후 |
| UART5_RX_uC | SCIB_RXD232_CN | RS232 레벨 변환 후 |
| CAN_TX_uC | CANA_H_CN / CANA_L_CN | CAN 트랜시버 후 차동 |
| CAN_RX_uC | CANA_H_CN / CANA_L_CN | CAN 트랜시버 후 차동 |
| — | BUCK_VOUT_ADC_CN | 파워보드→이 보드 (MCU 미연결) |
| — | BUCK_IOUT_ADC_CN | 파워보드→이 보드 (MCU 미연결) |

> `BUCK_VOUT_ADC_CN`, `BUCK_IOUT_ADC_CN`은 _uC 신호 없음 — 전력 보드(`RX_OLED_REGULATOR_POWER_BOARD`)에서 오는 신호이며 이 보드 MCU에 직접 연결되지 않음. 용도 미확인.

---

## TEMP1/TEMP2 Swap 분석

기존 [[adc_channel_map]]에서 PC4/PC5 라벨 swap 의심 상태. 회로도 좌표 분석 결과:

| 근거 | 내용 |
|---|---|
| MCU 페이지 좌표 | TEMP1_ADC_uC 오프페이지 커넥터: Y=440 |
| PC4 절대 좌표 | MCU 배치(locY=140) + hotptY=300 = **Y=440** → 일치 |
| 결론 | **회로도 신호명 TEMP1_ADC_uC = PC4 (ADC_IN14)** |
| 기존 .ioc 라벨 | PC4 → `TEMP2_ADC` (swap) |

→ Swap은 `.ioc` GPIO_Label에서 발생. 회로도 상 TEMP1 = PC4가 정의이고, 펌웨어 IOC가 PC4를 TEMP2로 잘못 라벨링한 것.

---

## OSC Clock (8MHz) — HSE 클럭 회로

페이지 02 우측 서브블록 "OSC Clock (8MHz)". MCU U1의 HSE(고속 외부) 클럭 소스.

> **근거 수준**: 이 절의 모든 사실은 **회로도 p.2 vision 판독**(400 DPI 렌더 크롭 확인)이다. 부품 정수는 **실크 마킹 판독**이며 OrCAD Design XML로 교차검증되지 않았다 — 이 보드 ingest의 다른 절(_uC 신호 인벤토리 등)은 XML 추출 기반이지만 OSC 부품값은 PDF 이미지 전용. 결선(어느 핀이 어느 net인지)도 PDF가 이미지라 **vision 판독 수준**임.

### 방식: 수동 크리스탈 Pierce 발진

HSE 소스는 **수동 크리스탈**(Pierce 발진 구성)이다 — 능동 오실레이터(완성형 클럭 IC)가 **아니다**.

| 레퍼런스 | 값 | 마킹 | 결선 | 근거 |
|---|---|---|---|---|
| X1 | 8 MHz 크리스탈 | `8MHz, 5032` (5.0×3.2mm 패키지) | 전극 2핀 ↔ OSC_IN / OSC_OUT 노드, 케이스 2핀 ↔ DGND | p.2 vision 판독 (마킹) |
| C2 | 22 pF 부하 커패시터 | `220J, 50V, 1608` | OSC_IN ↔ DGND | p.2 vision 판독 (마킹) |
| C3 | 22 pF 부하 커패시터 | `220J, 50V, 1608` | OSC_OUT 노드 ↔ DGND | p.2 vision 판독 (마킹) |
| R10 | 1 MΩ 피드백 저항 | `1MF, 1608` | 크리스탈 병렬 (OSC_IN ↔ OSC_OUT 노드) | p.2 vision 판독 (마킹) |
| R11 | 0 Ω 직렬 저항 | `0RF, 1608` | OSC_OUT 노드 → OSC_OUT_uC (MCU 핀6) | p.2 vision 판독 (마킹) |

결선 토폴로지 (vision 판독):

```
        C2(22pF)            R10(1MΩ, 병렬)
OSC_IN ──┬──── DGND      ┌───[ R10 ]───┐
 (핀5)   │               │             │
         ├───────────────┤ X1 8MHz     ├──── OSC_OUT 노드 ──[ R11 0Ω ]── OSC_OUT_uC (핀6)
         │               └─(케이스→DGND)              │
                                                      └── C3(22pF) ── DGND
```

- **OSC_IN_uC** → MCU `OSC_IN` (STM32F103VCT6/RCT6 **핀 5**)
- **OSC_OUT_uC** → MCU `OSC_OUT` (**핀 6**), R11 0Ω 직렬 경유
- 레이아웃 주의 표기(회로도 주석, 주황색): **"MCU 가장 근접한 곳에 배치"**

### 함의 — 펌웨어 RCC 정합

수동 크리스탈이므로 펌웨어 RCC 설정은 다음이 맞다:

- `RCC_OscInitStruct.HSEState = RCC_HSE_ON` (크리스탈을 STM32 내부 발진기로 **구동**) — **정답**
- `RCC_HSE_BYPASS`(외부 완성 클럭을 그대로 입력받는 모드)는 **아니다**. BYPASS는 능동 오실레이터일 때만.
- HSE 8 MHz → PLL 체배 → SYSCLK 구성과 정합 (예: ×8 → 64 MHz, [[pwm_system]]의 64 MHz 타이머 클럭과 일치).

> 위 RCC 함의는 회로 방식(수동 크리스탈)으로부터의 **연역**이다 — 실제 펌웨어 `RCC_OscConfig` 코드를 직접 확인한 것은 아니므로, 코드 점검 시 `HSEState`/PLL 체배값을 대조할 것.

---

## 파생 페이지

- [[rx_control]] — STM32 entity (PWM·UART·SPI·CAN·DAC·ADC 전체 핀맵)
- [[adc_channel_map]] — ADC1 채널 매핑 + TEMP swap 최종 확인
- [[pwm_system]] — TIM8/TIM3 PWM 출력
- [[uart_command_set]] — UART5 명령어
