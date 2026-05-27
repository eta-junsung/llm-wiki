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
- `projects/c/oled_tv_software/docs/Schematic/Rx_OLED_Regulator_Control_Board_260327.pdf`
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
| 02 | MCU_Peripheral_Section | MCU U1 전체 핀 배치, 디버그/부트 회로 |
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
| OSC_IN_uC | OSC_IN | 외부 클럭 입력 | 심볼명 |
| OSC_OUT_uC | OSC_OUT | 외부 클럭 출력 | 심볼명 |
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

## 파생 페이지

- [[rx_control]] — STM32 entity (PWM·UART·SPI·CAN·DAC·ADC 전체 핀맵)
- [[adc_channel_map]] — ADC1 채널 매핑 + TEMP swap 최종 확인
- [[pwm_system]] — TIM8/TIM3 PWM 출력
- [[uart_command_set]] — UART5 명령어
