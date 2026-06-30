---
tags: [source, schematic, 8kw-ev-wpt-tx, hardware]
source: raw/8kw_inverter_board_260506.pdf — "8kW EV WPT Tx Board, Ver 1.0E00" 회로도 6시트. 설계 J.H.Oh, 검토 D.W.Kim, 승인 T.D.Yeo, 2026.04.27 (시트2 도면일 2026.05.04, 시트5 2026.05.06)
date: 2026-06-30
---

# board_schematic_v1_0e00 — 8kW EV WPT TX 보드 회로도 (Ver 1.0E00)

> eta 자체 설계 8kW WPT 송신 보드 회로도. **LP-AM263P를 그대로 결합**(J9~J12 SSQ-110-03-T-D 소켓 = LaunchPad BoosterPack 헤더 메이팅)해 MCU로 사용하는 구성.
> 원본 PDF: `raw/8kw_inverter_board_260506.pdf` (first-ingest-wins — 다른 프로젝트는 복제 말고 [[board_schematic_v1_0e00]] 백링크).
> ADC 핀 대응은 [[adc_pinmap]], PWM 게이트 핀은 [[pwm_pinmap]], 노이즈 FFT 프로브 결정은 [[adc_noise_fft_probe]].

---

## 시트 구성

| 시트 | 제목 | 핵심 내용 |
|------|------|----------|
| 1 | 표지 | Ver 1.0E00, 200~800 VDC 입력, 8 kW |
| 2 | 입력전원 + 제어전원 | DC 버스 입력·벌크 필름캡·블리더, LDO/DCDC 제어전원 5종, **U1 입력전류 센서** |
| 3 | Inverter Power Stack (H-Bridge) | **풀브리지 SiC 모듈 U6/U7**, 게이트드라이버 U8/U9, DC링크 스너버, **T1 코일전류 CT**, 모듈 NTC |
| 4 | OV/OC 보호 + MCU Pin Connect + Input Sensing | 보호 비교기·게이트 인터록, **MCU 커넥터 J9~J12**, **U16 절연 전압센서** |
| 5 | 부품 배치도 | MCU(좌)·하프브리지 모듈 2개(중앙)·게이트드라이버·필름캡+스너버(우)·COIL_A/B |
| 6 | Revision / 설계참조 | 테스트핀·캐패시터 코드·저항 사이즈·PCB 라우터 폭 |

---

## 전력단 토폴로지 (시트 3)

- **풀브리지 인버터**: 하프브리지 SiC MOSFET 모듈 **2개** — U6, U7 = **FF8MR12W1M1H_B70** (1200 V SiC, 모듈 내 HS/LS + 바디다이오드 + NTC 내장). 레그1=U6, 레그2=U7.
- **게이트 드라이버**: U8(레그2), U9(레그1) = **FR20205VBDN**. 입력 `PWM_HS1/LS1/HS2/LS2` + `GD_EN`(게이트 인에이블), 출력 G1/G2 → 모듈 게이트. → PWM 핀맵 [[pwm_pinmap]].
- **DC 링크 / 스너버**: C27~C46 (22 nF/1 kV/3225) 다수 병렬, 버스 양단. "MLCC 소자 IC 최단 거리 배치" 주석.
- **공진 출력**: TX_COIL_A / TX_COIL_N → 외부 송신 코일(COIL_A/COIL_B 커넥터).

## 센서 신호 체인 (ADC 입력의 출처) — ★ 노이즈 진단 핵심

ADC가 읽는 6신호의 물리적 출처와 컨디셔닝 경로. 노이즈 거동이 신호마다 다른 이유가 여기에 있다.

| 신호 | 센서 / 출처 (시트) | 성격 | 컨디셔닝 → MCU 핀 |
|------|-------------------|------|-------------------|
| **GA_Vin** | **U16 AMC0311RQDWVRQ1** 절연 증폭기, VDC_BUS_P를 R53/55/56/57/58 분압 (시트4 Input Sensing) | **DC 버스전압 미러 (DC-nominal)** | 절연 출력 → 100 Ω + RC → J3.26 (ADC3 AIN0) |
| **GA_Iin_SEN** | **U1 TMCS1126C3AQDVGRQ1** Hall 절연 전류센서, 입력 DC 라인 (시트2) | **입력 DC 전류 (DC-nominal)** | VOUT → 100 Ω + RC → J3.29 (ADC1 AIN1). VOC=GA_Iin_OC(과전류) |
| **I_COIL_SEN** | **T1 PA6322.150NLT 전류 트랜스(CT)**, TX_COIL_N (시트3). Range 7 A, Sens 7 mV/A | **85 kHz 공진전류 = 신호 자체가 스위칭 주파수** | INV_ISEN_P/N → CR3~6(CUS10S30) 정류·클램프 + R30~32 + C55 2.2µF → J3.28 (ADC0 AIN1) |
| **Temp_Module1** | U6 모듈 내장 **NTC** (시트3) | 저속 온도 (DC) | → J3.25 (ADC2 AIN0) |
| **Temp_Module2** | U7 모듈 내장 **NTC** (시트3) | 저속 온도 (DC) | → J3.24 (ADC1 AIN0) |
| I_LCC_SEN | (시트3 영역) — 펌웨어 **드롭**(스펙 미입수) | — | J3.27 (ADC4 AIN0) |

스케일링 변환식은 [[adc_scaling]], 핀↔인스턴스는 [[adc_pinmap]].

### MCU 핀 입력단 RC 필터 (시트 4, J9 영역) — 85 kHz 미감쇠

ADC 신호는 MCU 핀 직전에서 **직렬 100 Ω(R69~R73, 1%/1608) + 션트 캡(330 pF + 1 nF ≈ 1.33 nF)** RC 필터를 거친다. 일부는 페라이트비드(FB3/FB6 MPZ2012S300, 30 Ω@100 MHz)도 통과.

- 컷오프 **fc ≈ 1/(2π·100·1.33 nF) ≈ 1.2 MHz** → **85 kHz 스위칭 성분은 거의 감쇠 없이 ADC 핀에 도달**. 이 필터는 >1 MHz RF만 잡는다.
- ∴ 스위칭 상관 노이즈를 HW 필터가 막아주지 못한다 → 펌웨어 측 레버(N 평균 / 트리거 위상)가 1차 대응. 결정 로직 [[adc_noise_fft_probe]].

## 보호 인터록 (시트 4) — ADC 경로와 분리

- 비교기 U11/U12/U15 (**TLV3231**) → `GA_Vin_OV`(과전압), `I_LCC_OC`, `I_COIL_OC`(과전류).
- U1 센서 → `GA_Iin_OC`(입력 과전류).
- **U10 SN74HCS21**(AND) 이 보호신호 + `GD_EN_seed`(MCU GPIO93) 묶어 `GD_EN_V` → **U14 SN74LVC1G08** → 최종 `GD_EN`(게이트 인에이블).
- ∴ **과전류·과전압 보호는 HW 비교기/로직이 담당** — ADC 평균(N) 트레이드오프가 보호 응답을 늦추지 않는 근거([[am263p_adc_ppb_averaging]] repeater 미채택 논거와 일치). 비교기는 ADC와 같은 센서 노드를 탭하지만 경로는 독립.

## 제어전원 (시트 2)

DC링크에서 절연형 DC PS 경유 DP12V → 파생: **DP5V**(U3/U5 LDL1117S50), **DP3V3**(U2/U4 TLV76733), **DP5V_2**, **AP5V**(PS1 RKK-0505SH 절연 DC/DC, PRI_GND 도메인). 입력 200~800 VDC, 벌크 C3~C7 12µF/1.3kV, 블리더 R1~R9 100k/2W, Y2캡 YC1/YC2.

## 접지 도메인 (★ 프로빙 안전)

- **DGND**: MCU·신호 컨디셔닝 도메인 (ADC 신호는 전부 여기로 절연/레벨시프트되어 들어옴).
- **PRI_GND**: 1차/전력단 도메인 (HV, 위험).
- GA_Vin은 U16 절연증폭기, GA_Iin은 U1 절연 Hall, I_COIL은 CT로 **이미 DGND 측으로 절연** → **MCU ADC 핀은 0~3.3 V·DGND 기준 저전압 노드라 프로빙 안전**. **절대 PRI_GND/HV 측을 직접 찍지 말 것.** 상세 [[adc_noise_fft_probe]].

---

## 파생 / 백링크

- [[adc_pinmap]] — J3 핀 ↔ ADC 인스턴스/채널 ↔ 신호 (이 회로도의 센서 신호가 어느 MCU 핀에 가는지)
- [[adc_scaling]] — 각 센서 변환식 (CT 버든·Hall 감도·분압비·NTC Beta)
- [[pwm_pinmap]] — 게이트 신호 PWM_HS1/LS1/HS2/LS2 ↔ EPWM 핀
- [[adc_noise_fft_probe]] — 이 회로도 기반 스코프 FFT 프로브 포인트 + N vs 트리거 위상 결정 (다음 작업)
- [[am263p_adc_repeater_burst]] · [[am263p_adc_ppb_averaging]] — ADC 평균 필터 구현
