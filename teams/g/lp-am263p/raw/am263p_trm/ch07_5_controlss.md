<!-- AM263P TRM | 7.5 Real-time Control Subsystem (CONTROLSS) | 원본 p.509-932 | pymupdf4llm text+tables, images omitted -->

www.ti.com 

_Processors and Accelerators_ 

## **7.5 Real-time Control Subsystem (CONTROLSS)** 

The integrated real-time Control Subsystem (CONTROLSS) enables closed loop control systems with flexible interconnection between data acquisition, actuator modules, and other control signal resources. The CONTROLSS module consists of the following control peripherals: 

## **Analog Control Peripherals** 

- 5x Analog to Digital Converter (ADC) modules 

   - 12-bit resolution with 4MSPS sample rate 

   - Programmable 6x single-ended or 3x differential channels 

   - 3.2V full scale voltage range with 1.8V reference (32/18 internal input scaling) 

   - Support for internal or external 1.8V ADC VREF reference voltage (2% internal reference accuracy error) 

   - – Two common external calibration pins 

   - 4x Post-processing blocks per ADC 

   - Multiple ADC trigger sources including CPU timers, GPIO/Input XBAR, and EPWM SOCa/SOCb signals. 

- 1x Resolver with 2x dedicated SAR ADCs configurable in the following modes: 

   - 2x motor position sensing units 

   - 2x General Purpose ADCs with 4x channels, 12-bit resolution with 3MSPS sample rate 

- 1x Buffered Digital to Analog (DAC) module 

   - 12-bit resolution 

- 10x Comparator Subsystem A (CMPSSA) 

   - 2 comparators + 2 DACs 

   - Window comparison on one input OR 

   - Compare two inputs OR 

   - Single threshold compare of single input 

- 10x Comparator Subsystem B (CMPSSB) 

   - 2 comparators + 2 DACs 

   - Window comparison on one input OR 

   - Single threshold compare of single input 

## **Digital Control Peripherals** 

- 32x Enhanced Pulse-width Modulation (EPWM) modules 

- 16x Enhanced Capture (ECAP) modules 

- 2x Sigma-Delta Filter (SDFM) modules 

- 3x Enhanced Quadrature Encoder Pulse (EQEP) modules 

- 4x Fast Serial Interface Transmitter (FSITX) modules 

- 4x Fast Serial Interface Receiver (FSIRX) modules 

## _**7.5.1 Real-time Control Subsystem (CONTROLSS) Overview**_ 

The AM263Px Real-time Control subsystem or CONTROLSS enables closed loop control systems with flexible interconnection between data acquisition, actuator modules, and other control signal resources. 

A real-time control system is typically composed of four main elements: 

- _Sensing_ : or feedback acquisition. The application needs to measure several key parameters (voltage, current, motor speed, temperature) in an accurate manner and at a very precise moment in time. 

- _Processing_ : Use the sensing information to apply control algorithms to the incoming data and calculate the next output command. 

- _Control_ : The command is applied to the system, typically via a PWM unit driving the power electronics system, for example, the motor turns faster, the current to the solar installed system is reduced, the car is accelerating. 

- _Interface_ : The ability of the device to communicate to other external components. While not necessarily involved in the control of the system, communications to other system components also has to co-exist with the main control loop. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

509 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

The CONTROLSS consists of various control peripherals to enable full integration the **Sensing** and **Control** functionality of the device within real-time applications. The components of the subsystem are described in the following sections. 

## **Note** 

In regards to various tables, diagrams, and descriptions throughout this chapter in the AM263Px device TRM. 

References to the _C28x_ component/functional block (also referred to as _CPU_ or _processor core_ ) is synonymous with the Arm Cortex-R5F MCU subsystem ( _R5FSS_ ) cores. 

References to SYSCLK are synonymous with the CONTROLSS_PLL/2 (200MHz) source clock. 

References to the Peripheral Interrupt Expansion ( _PIE_ ) unit component/functional block is synonymous with the Vectored Interrupt Manager ( _VIM_ ). 

References to the Control Logic Accelerator ( _CLA_ ) and Configurable Logic Block ( _CLB_ ) component/ functional block are not applicable to this device and can be ignored. 

510 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.2 Analog-to-Digital Converter (ADC)**_ 

The analog-to-digital converter (ADC) module described in this chapter is a Type 4 ADC. 

**7.5.2.1 Introduction (ADC)** ...................................................................................................................................... 512 **7.5.2.2 ADC Integration** ........................................................................................................................................... 513 **7.5.2.3 ADC Configurability** .................................................................................................................................... 516 **7.5.2.4 SOC Principle of Operation** ........................................................................................................................ 524 **7.5.2.5 SOC Configuration** ...................................................................................................................................... 524 **7.5.2.6 Trigger Operation** ........................................................................................................................................ 524 **7.5.2.7 ADC Acquisition (Sample and Hold) Window** ...........................................................................................533 **7.5.2.8 ADC Input Models** ........................................................................................................................................534 **7.5.2.9 Channel Selection** ....................................................................................................................................... 535 **7.5.2.10 SOC Configuration Examples** .................................................................................................................. 543 **7.5.2.11 ADC Conversion Priority** .......................................................................................................................... 543 **7.5.2.12 Burst Mode** .................................................................................................................................................547 **7.5.2.13 EOC and Interrupt Operation** ....................................................................................................................549 **7.5.2.14 Post-Processing Blocks** ........................................................................................................................... 551 **7.5.2.15 Result Safety Checker** .............................................................................................................................. 556 **7.5.2.16 Opens/Shorts Detection Circuit (OSDETECT)** ........................................................................................ 560 **7.5.2.17 Power-Up Sequence** ..................................................................................................................................563 **7.5.2.18 ADC Calibration** .........................................................................................................................................563 **7.5.2.19 ADC Timings** .............................................................................................................................................. 563 **7.5.2.20 Additional Information** .............................................................................................................................. 568 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 511 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.2.1 Introduction (ADC)** 

The ADC module is a 12-bit successive approximation (SAR) style ADC . The ADC is implemented as an analog core with a digital wrapper. The core is composed of the analog circuits which include the channel select MUX, the sample-and-hold (S/H) circuit, the successive approximation circuits, voltage reference circuits, and other analog support circuitry. The wrapper is composed of the digital circuits that configure and control the ADC. These circuits include the logic for programmable conversions, result registers, interfaces to analog circuits, interfaces to the peripheral buses, post-processing circuits, and interfaces to other on-chip modules. 

Each ADC module consists of a single sample-and-hold (S/H) circuit. The ADC wrapper is start-of-conversion (SOC) based (see Section 7.5.2.4). The ADC module is designed to be duplicated multiple times on the same chip, allowing simultaneous sampling or independent operation of multiple ADCs. 

## _**7.5.2.1.1 Features**_ 

Each ADC supports the following features: 

- 3.2V default voltage with support to 3.3V depending on ADC modes. (See _Signal Mode_ and _ADC Modes of Operation_ ). 

- External reference set by VREFHI and VREFLO pins 

- Single-ended (SE) signal conversions 

- Differential-ended (DE) signal conversions 

- Input multiplexer with up to 6 channels 

- External channel mux option to expand available ADC channels 

- 16 configurable SOCs 

- Type 4 digital wrappers that enhances the ADC capabilities to include: 

   - Over and Under Sampling 

   - External Channel support with at least 2 bit external select per ADC 

- 16 individually addressable result registers 

- Two trigger repeater modules , enabling customizable hardware oversamplingand undersampling modes with little or no CPU overhead 

- Multiple trigger sources: 

   - S/W (with available global synchronization for multiple ADCs) - software immediate start 

   - All ePWMs- ADCSOC A or B 

   - GPIO: INPUTXBAR[5] 

   - RTI Timers 0/1/2/3/4/5/6/7 

   - ADCINT1/2 

   - ECAP events in capture mode (CEVT1, CEVT2, CEVT3, and CEVT4) and APWM mode (period match, compare match, or both) 

- Four flexible VIM interrupts triggers 

- Burst mode 

- Four post-processing blocks, each with: 

   - Saturating offset calibration 

   - Error from set-point calculation 

   - High, low, and zero-crossing compare, with interrupt and ePWM trip capability 

   - Trigger-to-sample delay capture 

   - Connections to 12 Simultaneous Compare Blocks (also known as ADC Safety Tiles) 

   - Aggregation functions: max, min, sum and average (binary shift) 

   - Absolute value function 

- Result safety checkers to compare SOC results on same ADC or multiple ADC instances 

Additionally, there are 2 Resolvers ADCs (SAR ADCs also known as ADC_R0 and ADC_R1) that can be used as general-purpose ADC. The SAR ADC_Rs have the additional features: 

- Maximum sampling rate of 3.125 MSPS 

- Up to 50MHz output clock to Resolver 

- Additional RADC details can be found in the _Resolver Features_ and _Resolver Integration_ sections. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

512 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.2.2 ADC Integration** 

There are 5x Analog-to-Digital Converter (ADC) modules integrated in the device. 

## **Note** 

## For each ADC[0:4]: 

- Analog input channels ADCIN[0:5] have dedicated pins. 

- Analog input channels ADCIN[6:7] are tied to shared ADC_CAL[0:1] pins, respectively. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

513 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [680 x 375] intentionally omitted <==**

**Figure 7-98. ADC Integration Diagram - Simplified** 

514 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [680 x 290] intentionally omitted <==**

**Figure 7-99. ADC Integration Diagram - Detailed** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 515 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.2.3 ADC Configurability** 

Some ADC configurations are individually controlled by the SOCs, while others are globally controlled per ADC module. Table 7-112 summarizes the basic ADC options and the level of configurability. The subsequent sections discuss these configurations. 

**Table 7-112. ADC Options and Configuration Levels** 

|**Options**|**Configurability**|
|---|---|
|Clock|Per module(1)|
|Resolution|Not configurable (12-bit only)|
|Signal Mode|Per module|
|Reference Voltage Source|Not configurable (external or internal reference only)|
|Trigger Source|Per SOC(1)|
|Converted Channel|Per SOC|
|Acquisition Window Duration|Per SOC(1)|
|EOC Location|Per module|
|Burst Mode|Per module(1)|



(1) Writing these values differently to different ADC modules can cause the ADCs to operate asynchronously. See Section 7.5.2.20.1 for guidance on when the ADCs are operating synchronously or asynchronously. 

## _**7.5.2.3.1 Clock Configuration**_ 

The base ADC clock is provided directly by the system clock (SYSCLK). SYSCLK is used to generate the ADC acquisition window. The register ADCCTL2 has a PRESCALE field that determines the ADCCLK. ADCCLK is used to clock the converter, and is only active during the conversion phase. At all other times, including during the sample-and-hold window, the ADCCLK signal is gated off. 

The conversion phase process requires approximately 11.5 ADCCLK cycles and 13.5 ADCCLK cycles for ADC_R0/1. The choice of resolution also determines the necessary duration of the acquisition window. Section 7.5.2.20.2. 

## **Note** 

To determine an appropriate value for ADCCTL2.PRESCALE, see the device data sheet for the maximum allowable SYSCLK and ADCCLK frequencies. 

## **Note** 

Unless otherwise stated in data sheet, the maximum ADCCLK frequency allowed for this device is 66.67MHz. If the default 200MHz SYSCLK is used, ADCCTL2.PRESCALE requires a minimum value of 3. 

## _**7.5.2.3.2 Resolution**_ 

The resolution of the ADC determines how finely the analog range is quantized into digital values. Each ADC module supports a fixed resolution of 12 bits. 

516 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.2.3.3 Voltage Reference**_ 

## _**7.5.2.3.3.1 Internal ADC Voltage Reference Buffer Control**_ 

There are three internal ADC reference buffers in the device, REFBUF0, REFBUF1 and REFBUF2, to provide a precise reference of 1.8V to the ADCs. REFBUF0 is internally associated with ADC0. REFBUF1 is internally associated with ADC3 and ADC4. REFBUF2 is internally associated with ADC_R0 and ADC_R1. ADC1 and ADC2 are not associated with any internal REFBUFs. 

The ADC can operate with the internal reference or an external reference. Both internal and external reference are connected to the same package balls. Only one reference can be active at any given time. 

ADC Reference connection is shown in Figure 7-100. 

The voltage rails ADC_VREF*_G0 connect to REFBUF0 and ADC0. 

The voltage rails ADC_VREF*_G1 connects to ADC1 and ADC2. 

The voltage rails ADC_VREF*_G2 connects to REFBUF1, ADC3, and ADC4. 

The voltage rails ADC_VREF*_G3 connects to the REFBUF2, ADC_R0 and ADC_R1 

If the internal reference is used for ADC1 and ADC2, a board connection is required to connect ADC_VREF*_G0 to ADC_VREF*_G1. 

The internal reference is based on internally routed circuitry with added signal conditioning to improve the signal quality of the 1.8V rail. Because of this, there is no situation in which using the VDDA18_LDO as a reference is to be considered. When using the internal reference, the VREF pins cannot have an external reference voltage applied to them. When using the external reference, routing VDDA18_LDO as the external reference keeps the signal conditioning circuits from being leveraged and which results in lower signal quality of the 1.8V rail. 

The internal reference buffers are designed to provide sufficient source current for the maximum operational requirements of each module. Therefore, using a single reference buffer for all ADC modules is not recommended as the buffer is unable to source sufficient current. REFBUF0 is to be used for ADC[0:2] and REFBUF1 is to be used for ADC[3:4] and REFBUF2 is to be used for ADC_R[0:1]. 

**Figure 7-100. ADC Reference Connectivity Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

517 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [276 x 402] intentionally omitted <==**

Internal references are disabled by default in hardware. If an external reference is not used, the internal reference buffers can be enabled by the application for driving the ADC reference. 

The ADC_REFBUF0_CTRL register is used to enable ADC Reference Buffer 0. Similarly, the ADC_REFBUF1_CTRL register is used to enable ADC Reference Buffer 1. 

The MASK_ANA_ISO register must be set to 0x7 before ADC reference buffers are enabled. This prevents any undesirable behavior where the voltage monitors trigger an SOC reset. 

## **Note** 

After the reference buffer is enabled, program the MASK_ANA_ISO back to 0x0 to re-enable the voltage monitors. 

There are voltage monitors on all the reference voltage rails for safe the reliable operation of ADC. 

The TOP_CTRL.ADC_REF_COMP_CTRL register is used to enable the reference monitor comparators. 

- ADC_REF_COMP_CTRL.ADC0_REFOK_EN enables the voltage monitor on ADC_VREF*_G0. 

- ADC_REF_COMP_CTRL.ADC12_REFOK_EN enables the voltage monitor on ADC_VREF*_G1. 

- ADC_REF_COMP_CTRL.ADC34_REFOK_EN enables the voltage monitor on ADC_VREF*_G2. 

- ADC_REF_COMP_CTRL.ADCR01_REFOK_EN enables the voltage monitor on ADC_VREF*_G3 

The status of the ADC reference rails is indicated in the ADC_REF_GOOD_STATUS register. 

518 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **Note** 

ADC cannot be enabled without proper ADC voltage reference. 

## _**7.5.2.3.4 ADC Modes of Operation**_ 

This section describes the ADC Modes of Operation. 

## **Single-ended Mode:** 

The ADC output code is a 12-bit value, but internally it can generates slightly more than 12 effective data bits. There are operating modes that can be selected to clip and/or shift the ADC output to utilize different regions in SE (single-ended) mode. These modes can be selected by utilizing bits adcX_cfg_1p1v[79:80]. The default mode (00) simply clips the output within 0 and 4095 to maintain a 12 bit value; this effectively limits the maximum input of the ADC to 3.2V. 

**Table 7-113. ADC Output Code Clip and Shift Options** 

|**Input**|**Input**|**Output**|**Output**|
|---|---|---|---|
|**Equation**|**Input Voltage**|**Raw O/P**|**Default(00)**|
|3.3/4224 * 0|0|0|0|
|3.3/4224 * 1|0.00078125|1|1|
|3.3/4224 * 2|0.0015625|2|2|
|...|...|...|...|
|3.3/4224 * 127|0.09921875|127|127|
|3.3/4224 * 128|0.1|128|128|
|3.3/4224 * 129|0.10078125|129|129|
|...|...|...|...|
|3.3/4224 * 4094|3.1984375|4094|4094|
|3.3/4224 * 4095|3.19921875|4095|4095|
|3.3/4224 * 4096|3.2|4096|4095|
|...|...|...|...|
|3.3/4224 * 4221|3.29765625|4221|4095|
|3.3/4224 * 4222|3.2984375|4222|4095|
|3.3/4224 * 4223|3.29921875|4223|4095|



## **Differential Mode:** 

In differential mode ADC output code can be estimated using the following equation 

ADC Output Code = floor((VinPX-VinMX) / step_size + 2112 

Where step_size=(VrefP-VrefM)*33/18*2/4096 

Please note the addition factor is 2112 as the ADC generates a full-scale code in raw o/p mode as 4223. This 64 LSB shift can be compensated if adcX_cfg_1p1v[79:80] is set to 01 in differential mode 

## **Input Configuration:** 

The ADC can be operated in both single-ended and differential mode; the inputs can be configuredaccording to ADC Input Selection Logic 

## _**7.5.2.3.5 ADC Usage and Configuration Note**_ 

The bits adcX_cfg_1p1v[79:80] are common to all 5 ADC modules. Depending on the individual ADC (ADC0ADC4) configuration (Single-ended or Differential) the module will behave according to following information. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 519 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **ADC configured in Single-ended Mode:** 

- Selection=00: Normal ADC o/p [+0.0V = code 0 and +3.2V = code 4095] 

- Selection=10: Reserved 

- Selection=11: Reserved 

## **ADC configured in Differential Mode:** 

- Selection=00: Normal ADC Output with a code differential offset of 64. The output code rolls over above input 3.2V. 

   - (A 3.2V to 3.3V input voltage will result in the same output code as 0-100mV input voltage) 

- Selection=01: Normal Differential ADC Output 

   - [-3.2V Differential = code 0 and +3.2V Differential = code 4095] 

- Selection=10: Reserved 

- Selection=11: Reserved 

## _**7.5.2.3.6 Interpreting Conversion Results**_ 

Based on a given ADC conversion result, the corresponding analog input is given in Table 7-114 and Table 7-115. This corresponds to the center of the possible range of analog voltages that can produce this conversion result. 

**Table 7-114. 12-Bit Digital-to-Analog Formulas** 

|**Digital Value**|**Analog Equivalent**||
|---|---|---|
|when ADCRESULTy = 0|ADCINx ≤VREFLO|(2)|
|when 0 < ADCRESULTy < 4095|ADCINx =<br>VREFHI −VREFLO|ADCRESULTy<br>4096<br>+ VREFLO<br>(3)|
|when ADCRESULTy = 4095|ADCINx ≥VREFHI|(4)|



520 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

The ADC can be operated in either single-ended or differential mode; the inputs can be configured according to Table 7-115. 

**Table 7-115. ADC Input Selection Logic** 

|**chsel_1p1v<2:0>**|**diff_mode_1p1v=1**|**diff_mode_1p1v=0**|
|---|---|---|
|000|inp=ch0, inm=ch1|ch0|
|001|inp=ch1, inm=ch0|ch1|
|010|inp=ch2, inm=ch3|ch2|
|011|inp=ch3, inm=ch2|ch3|
|100|inp=ch4, inm=ch5|ch4|
|101|inp=ch5, inm=ch4|ch5|
|110|inp=cal0, inm=cal1|cal0|
|111|inp=cal1, inm=cal0|cal1|



## **Single-ended Mode:** 

The ADC is designed for 12-bit output, but internally the ADC generates slightly more than 12 bits. There are certain modes that can be selected utilizing bits adcX_cfg_1p1v<80:79> to clip and shift the ADC output to utilize different regions in SE (single-ended) mode. The default mode (00) clips the output within 0 and 4095 to maintain a 12-bit value; this effectively limits the maximum input of the ADC to 3.2V. In the shifted mode (01), the ADC effectively shifts the input so that the ADC creates a 12-bit output between 0.1V and 3.3V. 

|**Input**|**Input**|**Output (adcX_cfg_1p1v<80:79>)**|**Output (adcX_cfg_1p1v<80:79>)**|
|---|---|---|---|
|**Equation**|**Input Voltage**|**Raw O/P**|**Default(00)**|
|3.3/4224 * 0|0|0|0|
|3.3/4224 * 1|0.00078125|1|1|
|3.3/4224 * 2|0.0015625|2|2|
|...|...|...|...|
|3.3/4224 * 127|0.09921875|127|127|
|3.3/4224 * 128|0.1|128|128|
|3.3/4224 * 129|0.10078125|129|129|
|...|...|...|...|
|3.3/4224 * 4094|3.1984375|4094|4094|
|3.3/4224 * 4095|3.19921875|4095|4095|
|3.3/4224 * 4096|3.2|4096|4095|
|...|...|...|...|
|3.3/4224 * 4221|3.29765625|4221|4095|
|3.3/4224 * 4222|3.2984375|4222|4095|
|3.3/4224 * 4223|3.29921875|4223|4095|



## **Differential Mode:** 

In differential mode ADC output code can be estimated using the following equation: 

## ADC Output Code = **floor((VinpX-VinmX)/step_size + 2112)** 

Where step_size = (VrefP-VrefM) * 33/18/4224 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

521 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

Note the addition factor is 2112 as the ADC generates a full-scale code in raw o/p mode as 4223. This 64-LSB shift can be compensated if adcX_cfg_1p1v<80:79> is set to (01) in differential mode 

The adcX_cfg_1p1v<80:79> is not normally accessible, but can be overwritten by following the below steps. The bits in this and surrounding registers are critical for ADC functionality. Care must be taken so that only the bits <80:79> are changed as desired, while remaining bits remain in the default programmed state. 

- Write to EFUSE_OVERRIDE_ADC_CFG2 (24-bit value corresponding to adc0_cfg_1p1v<87:64>) 

- Write to EFUSE_OVERRIDE_ADC_CFG_CTRL for the override to take effect. 

## _**7.5.2.3.7 ADC-CMPSS Signal Connections**_ 

In each ADC, two sets of differential pins shall be shared with pins of two CMPSSA and remaining one pair of differential pins shall be connected to two independent pins of CMPSSB. These pins are demonstrated in Figure 7-101 and Table 7-116 where the CHSEL values determine how the inputs are fed into ADC. 

**==> picture [456 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
CMPSS-A CMPSS-A CMPSS-B CMPSS-B<br>12-bit 12-bit 12-bit 12-bit<br>DAC DAC DAC DAC<br>DAC-H DAC-L DAC-H DAC-L<br>12-bit 12-bit 12-bit 12-bit Code Code Code Code<br>DAC DAC DAC DAC<br>DAC-H DAC-L DAC-H DAC-L<br>Code Code Code Code<br>ATB<br>INP-0<br>INM-0<br>INP-1<br>INM-1 12-bit<br>4 MSPS<br>INP-2<br>INM-2<br>CAL-0<br>CAL-1<br>+ – – + + – _ + + – _ + + – _ +<br>**----- End of picture text -----**<br>


**Figure 7-101. CMPSS and ADC Connections** 

**Table 7-116. Connectivity between ADC Inputs to CMPSS Signals** 

|**Signal/Pin Name**|**ADC Input**|**CMPSS Input**|
|---|---|---|
|ADC0 Channels|||
|ADC0_AIN0|ADC0:inp0 (+IN0)|CMPSSA0:inH (+IN)|
|ADC0_AIN1|ADC0:inm0 (-IN0)|CMPSSA0:inL (-IN)|
|ADC0_AIN2|ADC0:inp1 (+IN1)|CMPSSA1:inH (+IN)|
|ADC0_AIN3|ADC0:inm1 (-IN1)|CMPSSA1:inL (-IN)|
|ADC0_AIN4|ADC0:inp2 (+IN2)|CMPSSB0:inH/inL (+IN/-IN)|
|ADC0_AIN5|ADC0:inm2 (-IN2)|CMPSSB1:inH/inL (+IN/-IN)|
|ADC_CAL1|ADC0:inm3 (-IN3)|X|
|ADC_CAL0|ADC0:inp3 (+IN3)|X|
|ADC1 Channels|||
|ADC1_AIN0|ADC1:inp0 (+IN0)|CMPSSA2:inH (+IN)|
|ADC1_AIN1|ADC1:inm0 (-IN0)|CMPSSA2:inL (-IN)|
|ADC1_AIN2|ADC1:inp1 (+IN1)|CMPSSA3:inH (+IN)|
|ADC1_AIN3|ADC1:inm1 (-IN1)|CMPSSA3:inL (-IN)|



522 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-116. Connectivity between ADC Inputs to CMPSS Signals (continued)** 

|**Signal/Pin Name**|**ADC Input**|**CMPSS Input**|
|---|---|---|
|ADC1_AIN4|ADC1:inp2 (+IN2)|CMPSSB2:inH/inL (+IN/-IN)|
|ADC1_AIN5|ADC1:inm2 (-IN2)|CMPSSB3:inH/inL (+IN/-IN)|
|ADC_CAL1|ADC1:inm3 (-IN3)|X|
|ADC_CAL0|ADC1:inp3 (+IN3)|X|
|ADC2 Channels|||
|ADC2_AIN0|ADC2:inp0 (+IN0)|CMPSSA4:inH (+IN)|
|ADC2_AIN1|ADC2:inm0 (-IN0)|CMPSSA4:inL (-IN)|
|ADC2_AIN2|ADC2:inp1 (+IN1)|CMPSSA5:inH (+IN)|
|ADC2_AIN3|ADC2:inm1 (-IN1)|CMPSSA5:inL (-IN)|
|ADC2_AIN4|ADC2:inp2 (+IN2)|CMPSSB4:inH/inL (+IN/-IN)|
|ADC2_AIN5|ADC2:inm2 (-IN2)|CMPSSB5:inH/inL (+IN/-IN)|
|ADC_CAL1|ADC2:inm3 (-IN3)|X|
|ADC_CAL0|ADC2:inp3 (+IN3)|X|
|ADC3 Channels|||
|ADC3_AIN0|ADC3:inp0 (+IN0)|CMPSSA6:inH (+IN)|
|ADC3_AIN1|ADC3:inm0 (-IN0)|CMPSSA6:inL (-IN)|
|ADC3_AIN2|ADC3:inp1 (+IN1)|CMPSSA7:inH (+IN)|
|ADC3_AIN3|ADC3:inm1 (-IN1)|CMPSSA7:inL (-IN)|
|ADC3_AIN4|ADC3:inp2 (+IN2)|CMPSSB6:inH/inL (+IN/-IN)|
|ADC3_AIN5|ADC3:inm2 (-IN2)|CMPSSB7:inH/inL (+IN/-IN)|
|ADC_CAL1|ADC3:inm3 (-IN3)|X|
|ADC_CAL0|ADC3:inp3 (+IN3)|X|
|ADC4 Channels|||
|ADC4_AIN0|ADC4:inp0 (+IN0)|CMPSSA8:inH (+IN)|
|ADC4_AIN1|ADC4:inm0 (-IN0)|CMPSSA8:inL (-IN)|
|ADC4_AIN2|ADC4:inp1 (+IN1)|CMPSSA9:inH (+IN)|
|ADC4_AIN3|ADC4:inm1 (-IN1)|CMPSSA9:inL (-IN)|
|ADC4_AIN4|ADC4:inp2 (+IN2)|CMPSSB8:inH/inL (+IN/-IN)|
|ADC4_AIN5|ADC4:inm2 (-IN2)|CMPSSB9:inH/inL (+IN/-IN)|
|ADC_CAL0|ADC4:inp3 (+IN3)|X|
|ADC_CAL1|ADC4:inm3 (-IN3)|X|



## **Note** 

In the **ADC Input** column in ADC-CMPSS Signal Connectivity Table above, "inp" stands for positive inputs and "inm" stands for negative inputs. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

523 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.2.4 SOC Principle of Operation** 

The ADC triggering and conversion sequencing is accomplished through configurable start-of-conversions (SOCs). Each SOC is a configuration set defining the single conversion of a single channel. In that set, there are three configurations: the trigger source that starts the conversion, the channel to convert, and the acquisition (sample) window duration. Upon receiving the trigger configured for a SOC, the wrapper makes sure that the specified channel is captured using the specified acquisition window duration. 

Multiple SOCs can be configured for the same trigger, channel, and acquisition window as desired. Configuring multiple SOCs to use the same trigger allows the trigger to generate a sequence of conversions. Configuring multiple SOCs to use the same trigger and channel allows for oversampling. 

**==> picture [500 x 361] intentionally omitted <==**

**----- Start of picture text -----**<br>
SOC Arbitration &  SOC15<br>Control<br>SOC2<br>ADCSOC15CTL.ACQPS SOC1<br>SOC0<br>ADCSOC2CTL.ACQPS<br>ADCSOC1CTL.ACQPS<br>ADCSOC0CTL.ACQPS ADCSOC0CTL.ACQPS ADCSOC0CTL.TRIGSEL<br>ADCSOC15CTL.CHSEL<br>0<br>1 ADCTRIG1<br>ADCSOC2CTL.CHSEL<br>2 ADCTRIG2<br>ADCSOC1CTL.CHSEL<br>ADCSOC0CTL.CHSEL ADCSOC0CTL.CHSEL .<br>. GND<br>.<br>ADCSOCFLG1.SOC15 .<br>127 ADCTRIG127<br>SOCOVF<br>ADCSOCFRC1.SOC0<br>ADCSOCFLG1.SOC2 Set<br>ADCSOCFLG1.SOC1<br>ADCSOCFLG1.SOC0 LATCH 0<br>Clear 1 ADCINT1<br>SOC15START<br>2 ADCINT2<br>SOC2START 3 undefined<br>SOC1START<br>SOC0START<br>ADCINTSOCSEL1.SOC0<br>REQSTAMP<br>ADCSOCFLG1.EXTCHSEL15<br>ADCSOCFLG1.EXTCHSEL2<br>ADCSOCFLG1.EXTCHSEL1<br>ADCSOCFLG1.EXTCHSEL0 ADCSOC0CTL.EXTCHSEL<br>ACQPS<br>CHSEL<br>SOC<br>MUX<br>ADCEXT<br>**----- End of picture text -----**<br>


**Figure 7-102. SOC Block Diagram** 

## **7.5.2.5 SOC Configuration** 

Each SOC has a configuration register, ADCSOCxCTL. Within this register, SOCx can be configured for a specific trigger source, channel to convert, optional external channel mux selection, and acquisition (sample) window duration. 

## **7.5.2.6 Trigger Operation** 

Each SOC can be configured to start on one of many input triggers. The primary trigger select for SOCx is in the ADCSOCxCTL.TRIGSEL register, which can select between: 

- Disabled (Software only) 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

524 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- RTI Timers 0/1/../7 

- GPIO: INPUTXBAR.OUT[5] 

- ADCSOCA or ADCSOCB from each ePWM module 

- eCAP events 

- Either of the two trigger repeater blocks. This can be used to achieve oversampling, undersampling, or to apply a trigger delay. 

- A global synchronous software trigger. This is achieved by configuring the ADCSOCFRCGBSEL and ADCSOCFRCGB registers. 

In addition, each SOC can also be triggered when the ADCINT1 flag or ADCINT2 flag is set. This is achieved by configuring the ADCINTSOCSEL1 register (for SOC0 to SOC7) or the ADCINTSOCSEL2 register (for SOC8 to SOC15). This can be useful for creating continuous conversions. 

## _**7.5.2.6.1 Global Software Trigger**_ 

This ADC supports synchronous global software triggers. Synchronous global triggers allow the application to trigger SOCs on multiple ADC instances that are exactly simultaneous in time. To generate a global software trigger, configure the analog subsystem register ADCSOCFRCGBSEL to select the ADC instances to be triggered, then write to ADCSOCFRCGB to trigger the desired SOCs simultaneously on each ADC. 

For example, to trigger SOC0, SOC1, and SOC2 on ADCA and ADCC: 

1. Set ADCSOCFRCGBSEL.ADCA = 1 and ADCSOCFRCGBSEL.ADCC = 1 by writing 0x5 to the ADCSOCFRCGBSEL register. 

2. Trigger SOCs 0, 1, and 2 by writing 0x7 to the ADCSOCFRCGB register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

525 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.2.6.2 Trigger Repeaters**_ 

Each ADC instance contains two trigger repeater modules. These modules can select any of the regular ADC triggers that are selectable by the ADCSOCxCTL.TRIGGER register, and generate a number of repeat pulses as configured in the REPxN.NSEL register. Figure 7-103 shows a functional block diagram of the ADC trigger repeater module. 

Each repeater module can apply four types of trigger modifications: 

- Oversampling mode 

- Undersampling mode 

- Phase delay 

- Re-trigger spread 

Each of these trigger modification features is explained in detail in the following sections. 

**==> picture [500 x 439] intentionally omitted <==**

**----- Start of picture text -----**<br>
REPxCTL.TRIGSEL<br>Re-trigger Logic Delay Logic<br>REPxCTL.MODE<br>MODE = Undersample<br>REPxN.NSEL REPxPHASE.PHASE<br>REPxTRIG Pass First Pulse Delay PHASE ADC TRIGGERS[127:0]<br>Block next NSEL Pulses  SYSCLKS<br>Status Status<br>REPxN.NCOUNT REPxPHASE.<br>PHASECOUNT<br>MODE = Oversample REPxCTL.<br>PHASEOVF<br>REPxN.NSEL<br>Repeat Pulse<br>REPxCTL.SWFRC<br>NSEL + 1 Times<br>ready to<br>Status repeat<br>REPxN.NCOUNT<br>REPxSPREAD.SPREAD<br>Count SPREAD SYSCLK cycles<br>from last pulse<br>Status<br>REPxSPREAD<br>.SPREADCOUNT<br>All associated SOCs<br>no longer pending<br>REPxCTL.SYNCINSEL<br>REPxCTL.BUSY<br>REPxCTL.<br>TRIGOVF<br>HW Sync Sources<br>When a sync. Is received, all<br>logic is reset to an idle and<br>Repeater 1 (of 2) waiting state REPxCTL.SWSYNC<br>PENDING SOCs[15:0]<br>**----- End of picture text -----**<br>


**Figure 7-103. ADC Trigger Repeater Block Diagram** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

526 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.2.6.2.1 Oversampling Mode**_ 

In this mode, the repeater module passes the initial trigger through to the output. As soon as all SOCs configured to receive the trigger are in progress or completed, the repeater issues the trigger again. The process repeats until the configured number of trigger pulses (NSEL + 1) have been issued. 

This mode allows the application to easily perform multiple back-to-back samples from a single trigger pulse. When used in conjunction with the aggregation options in the post-processing block, this mode enables oversampling, averaging, or peak detection. Figure 7-104 shows an example of oversampling SOCs generated from a single ePWM trigger. 

**==> picture [500 x 262] intentionally omitted <==**

**----- Start of picture text -----**<br>
ePWM1 Counter<br>Z AU P AD Z AU P AD<br>ePWM1<br>OutA<br>ePWM1<br>SOCA<br>Repeat1<br>SOC<br>**----- End of picture text -----**<br>


TRIGGER = ePWM SOCA, NSEL = 3, PHASE = 0, MODE = Oversampling, SPREAD = 0 

**Figure 7-104. Oversampled ADC Trigger Example** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

527 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.2.6.2.2 Undersampling Mode**_ 

In this mode, the repeater module passes the initial trigger through to the output, and then blocks subsequent triggers until the configured number of trigger pulses (NSEL + 1) arrive. The result is that only 1 in every (NSEL + 1) pulses passes through to the output. Figure 7-105 shows an example of undersampled SOCs from multiple ePWM triggers. 

This mode enables the application to scale down the trigger frequency for one or more SOCs. This is useful for charge-sharing input drivers which have increased error with higher sampling frequencies. 

**==> picture [500 x 265] intentionally omitted <==**

**----- Start of picture text -----**<br>
ePWM1 Counter<br>Z P Z P Z P Z P Z P Z P Z P Z P Z P Z P Z P Z P Z<br>ePWM1<br>OutA<br>ePWM1<br>SOCA<br>Repeat1<br>SOC<br>**----- End of picture text -----**<br>


TRIGGER = ePWM SOCA, NSEL = 7, PHASE = 0, MODE = Undersampling, SPREAD = (don't care) 

**Figure 7-105. Undersampled ADC Trigger Example** 

## **Note** 

Oversampling and undersampling modes are mutually exclusive for each repeater module. However, multiple repeater modules can (and are intended to) be used in different modes concurrently. 

## _**7.5.2.6.2.3 Trigger Phase Delay**_ 

The repeater module can delay the initial trigger by a specified number of SYSCLK cycles. This feature can be used in combination with oversampling or undersampling modes, or as a standalone delay by setting NSEL = 0. The phase delay does not affect the timing between subsequent repeated oversampled triggers—the phase delay only delays the initial trigger. When PHASE = 0, the initial trigger arrives at the same time as an unmodified trigger. Figure 7-106 shows an example of phase delay combined with oversampling. Figure 7-107 shows an example of a standalone phase delay with a single SOC trigger. 

Phase delay enables the application to tie the trigger start point to an ePWM event while allowing for a necessary sampling delay (for example, settling time). In addition, when phase delay is combined with oversampling functionality, a single trigger can generate an interleaved burst of conversions across multiple ADCs. To achieve this, set PHASE in increments of (tsample/n_interleaved_ADCs). Figure 7-108 shows an example of interleaving 12 samples across 3 ADCs. 

528 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [64 x 7] intentionally omitted <==**

**----- Start of picture text -----**<br>
ePWM1 Counter<br>**----- End of picture text -----**<br>


**==> picture [500 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Z AU P AD Z AU P AD<br>ePWM1<br>OutA<br>ePWM1<br>SOCA<br>Repeat1 PHASE PHASE<br>SOC 100 100<br>SYSCLKS SYSCLKS<br>**----- End of picture text -----**<br>


TRIGGER = ePWM SOCA, NSEL = 3, PHASE = 100, MODE = Oversampling, SPREAD = 0 

**Figure 7-106. Oversampled ADC Trigger Example with Phase Delay** 

**==> picture [500 x 262] intentionally omitted <==**

**----- Start of picture text -----**<br>
ePWM1 Counter<br>Z AU P AD Z AU P AD<br>ePWM1<br>OutA<br>ePWM1<br>SOCA<br>Repeat1 PHASE PHASE<br>SOC 100 100<br>SYSCLKs SYSCLKs<br>**----- End of picture text -----**<br>


TRIGGER = ePWM SOCA, NSEL = 0, PHASE = 100, MODE = (either), SPREAD = (don't care) 

**Figure 7-107. ADC Trigger Example with Phase Delay** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

529 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 344] intentionally omitted <==**

**----- Start of picture text -----**<br>
ePWM1 Counter<br>Z AU P AD Z AU P AD<br>ePWM1<br>OutA<br>ePWM1 Conv. Time<br>60 SYSCLKS<br>SOCA<br>ADCA.<br>Repeat1 PHASE PHASE<br>SOC SYSCLKS0 SYSCLKS0<br>ADCB.<br>Repeat1 PHASE PHASE<br>SOC SYSCLKS20 SYSCLKS20<br>ADCC.<br>Repeat1 PHASE PHASE<br>SOC SYSCLKS40 SYSCLKS40<br>**----- End of picture text -----**<br>


TRIGGER = ePWM SOCA, NSEL = 3, MODE = Oversampling, PHASE = (varies per ADC), SPREAD = 0 

**Figure 7-108. ADC Interleaved Trigger Example (12 Samples Across 3 ADCs)** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

530 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.2.6.2.4 Re-trigger Spread**_ 

If additional time between samples is desired, the application can configure SPREAD equal to the number of SYSCLK cycles desired between samples. Figure 7-109 shows an example of oversampling from an ePWM trigger with a 500-cycle spread between samples. 

- By default, SPREAD = 0, and samples are re-triggered as soon as all associated SOCs are no longer pending. 

- If SPREAD is set to a value smaller than the time needed for the associated SOCs to complete, then the ADC performs the triggered conversions back-to-back, and SPREAD is effectively 0. 

- SPREAD has no effect in undersampling mode, or when NSEL = 0. 

**==> picture [500 x 262] intentionally omitted <==**

**----- Start of picture text -----**<br>
ePWM1 Counter<br>Z AU P AD Z AU P AD<br>ePWM1<br>OutA<br>ePWM1<br>SOCA<br>500 500 500 500 500 500<br>Repeat1 SYSCLKS SYSCLKS SYSCLKS SYSCLKS SYSCLKS SYSCLKS<br>SOC<br>**----- End of picture text -----**<br>


TRIGGER = ePWM SOCA, NSEL = 3, MODE = Oversampling, PHASE=0, SPREAD = 500 

**Figure 7-109. ADC Repeated Trigger Example with Sample Spread** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

531 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.2.6.2.5 Trigger Repeater Configuration**_ 

To configure ADC oversampling or undersampling using the trigger repeater module, follow this procedure: 

1. Set up the SOC by writing to ADCSOCxCTL. Specify one of the two repeater modules (REP1TRIG or REP2TRIG) as the trigger source. 

2. Configure the repeater module by writing to the REPxCTL register: 

   - a. Configure oversampling or undersampling mode using the MODE bit. 

   - b. Specify the desired SOC trigger source in the TRIGGER field. 

   - c. If desired, configure a sync source for the repeater module in the SYNCINSEL field. A sync event resets all repeater registers to a ready and waiting state, while preserving NSEL, PHASE and MODE. A software-initiated sync is also possible by writing 1 to the SWSYNC bit. 

   - d. If desired, clear any previously set phase and trigger overflow flags by writing to the PHASEOVF and TRIGGEROVF bits. 

3. Configure the trigger repeat count by writing to the REPxN.NSEL register. The repeater module supports up to 128 repeats for each trigger. 

4. Configure the repeater phase delay by writing to the REPxPHASE.PHASE register. 

5. To configure a re-trigger spread delay in oversampling mode, write the desired delay value in SYSCLK cycles to the REPxSPREAD.SPREAD register. 

6. Configure the PPBxLIMIT register. This register defines how many samples the post-processing block accumulates before loading the partial sum value in ADCPPBxPSUM into ADCPPBxSUM. 

7. The post-processing block (PPB) and trigger repeater module have independent sync source configurations. To configure the PPB sync source, write to the ADCPPBxCONFIG2 register. For more information on how to configure the ADC post-processing block, see Section 7.5.2.14. 

## **Note** 

When NSEL = 0, the repeater module essentially acts as a pass-through for SOC triggers, but is still useful for applying phase delay. SOC triggers are passed through in both oversampling and undersampling mode, even if there are still pending SOCs. In this scenario, the ADC sets a trigger overflow flag for the individual SOC (ADCSOCOVF1.SOCx), not the repeater module. When oversampling with NSEL > 0, the ADC sets the oversampled trigger overflow flag (REPxCTL.TRIGGEROVF) if a trigger arrives while there are pending SOCs. 

When NSEL = 0, the repeater module does not set the REPxCTL.MODULEBUSY indicator. In this scenario, the application must make sure that all associated SOC flags have completed before enabling oversampling or undersamplingmode by setting NSEL > 0. 

## _**7.5.2.6.2.5.1 Register Shadow Updates**_ 

To avoid latency or processing delays between triggers, the application can write updated values to the NSEL, PHASE and SPREAD registers while the repeater module is still actively working. When a new SOC trigger is received, these values are loaded into the NCOUNT, PHASECOUNT and SPREADCOUNT registers, which then count down to zero as each SOC is triggered by the repeater module. 

In addition, the application can change the repeater module's oversampling or undersampling mode by writing to the REPxCTL.MODE register while the repeater is actively working, without affecting the current operation. The repeater module loads the value of REPxCTL.MODE into REPxCTL.ACTIVEMODE when a new SOC trigger is received. 

532 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.2.6.2.6 Re-Trigger Logic**_ 

The repeater module determines when to re-trigger based on the values of ADCSOCxCTL.TRIGSEL and the SOC flags in ADCSOCFLG1. A repeat trigger is issued when all SOCs configured to be triggered by the repeater module instance are no longer pending. Figure 7-110 describes the trigger repeat logic. Because the SOC pending flag goes low at the end of the sample and hold phase, the module has plenty of time to re-trigger conversions without introducing any latency between repeat conversions. 

**==> picture [380 x 182] intentionally omitted <==**

**----- Start of picture text -----**<br>
ADCSOCFLG1.SOC0<br>All associated SOCs<br>ADCSOC0CTL.TRIGSEL<br>=? no longer pending<br>REP x1 TRIG<br>ADCSOCFLG1.SOC1<br>ADCSOC1CTL.TRIGSEL<br>=?<br>REPxTRIG<br>ADCSOCFLG1.SOC15<br>ADCSOC15CTL.TRIGSEL<br>=?<br>REPxTRIG<br>Repeater Re-Trigger Logic<br>...<br>**----- End of picture text -----**<br>


**Figure 7-110. Trigger Repeater Repeat Logic** 

## **Re-triggering in Burst Mode** 

If the ADC is in burst mode, and the repeater is selected as the BURSTTRIG source, then the repeater fires a re-trigger pulse whenever there are no high-priority associated SOCs pending, and there are no round-robin SOCs pending. 

## _**7.5.2.6.2.7 Multi-Path Triggering Behavior**_ 

With the trigger repeater modules, to have one trigger source take multiple paths to set SOCs in various ways is possible. For example, ePWM1 can directly trigger SOC3 and SOC4, while one repeater block uses ePWM1 to generate oversampling triggers on SOCs 0-2, and the second repeater block generates undersampled triggers to SOC5. Assuming all SOCs are configured for round-robin priority and the various triggers all arrive in the same cycle, the conversion order is SOC0 to SOC5 in increasing order; this is then followed by the oversampled conversions on SOC0-SOC2. 

## **7.5.2.7 ADC Acquisition (Sample and Hold) Window** 

External signal sources vary in the ability to drive an analog signal quickly and effectively. To achieve rated resolution, the signal source needs to charge the sampling capacitor in the ADC core to within 0.5 LSBs of the signal voltage. The acquisition window is the amount of time the sampling capacitor is allowed to charge and is configurable per SOCx by the ADCSOCxCTL.ACQPS register. 

ACQPS is a 9-bit register field that can be set to a value between 0 and 511, resulting in an acquisition window duration of: 

Acquisition Window = (ACQPS + 1) ˟ (System Clock (SYSCLK) cycle time) 

- The acquisition window duration is based on the System Clock (SYSCLK), not the ADC clock (ADCCLK). 

- The selected acquisition window duration must be at least as long as one ADCCLK cycle. 

- The data sheet specifies a minimum acquisition window duration (in nanoseconds). The user is responsible for selecting an acquisition window duration that meets this requirement. 

- For this design, the minimum ACQPS value that can be programmed is 16. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 533 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.2.8 ADC Input Models** 

For single-ended operation, the ADC input characteristics for values in the single-ended input model (see Figure 7-111) can be found in the device data sheet. 

**==> picture [282 x 83] intentionally omitted <==**

**----- Start of picture text -----**<br>
ADC<br>ADCINx<br>Rs<br>Switch Ron<br>AC Cp Ch<br>VREFLO<br>**----- End of picture text -----**<br>


**Figure 7-111. Single-Ended Input Model** 

For differential operation, the ADC input characteristics for values in the differential input model (see Figure 7-112 ) can be found in the device data sheet. 

These input models must be used along with actual signal source impedance to determine the acquisition window duration. See Section 7.5.2.20.2 for more information. 

**==> picture [282 x 83] intentionally omitted <==**

**----- Start of picture text -----**<br>
ADC<br>ADCINxP<br>Rs<br>VREFLO Cp Switch Ron<br>AC Ch<br>Cp<br>ADCINxN Switch Ron<br>Rs<br>**----- End of picture text -----**<br>


**Figure 7-112. Differential Input Model** 

534 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.2.9 Channel Selection** 

Each SOC can be configured to convert any of the ADC channels. This behavior is selected for SOCx by the ADCSOCxCTL.CHSEL register. Depending on the signal mode, the selection is different. For single-ended signal mode, the value in CHSEL selects a single pin as the input. For differential signal mode, the value in CHSEL selects an even-odd pin pair to be the positive and negative inputs. This is summarized in Table 7-117. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

535 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-117. Channel Selection of Input Pins** 

|**Input Mode**|**CHSEL**|**Input**|**Input**||
|---|---|---|---|---|
|Single-Ended|0|ADCIN0||**Negative**<br>**Input**|
||1|ADCIN1|||
||2|ADCIN2|||
||3|ADCIN3|||
||4|ADCIN4|||
||5|ADCIN5|||
||Differential|**CHSEL**|**Positive Input**||
|0||ADCIN0|ADCIN1||
|1||ADCIN1|ADCIN0||
|2||ADCIN2|ADCIN3||
|3||ADCIN3|ADCIN2||
|4||ADCIN4|ADCIN5||
|5||ADCIN5|ADCIN4||



The ADCSOCxCTRL.EXTCHSEL field for each SOC can be used to automatically control an external mux with digital output pins ADCxEXTMUX[3:0]. This functionality enables the application to add additional ADC channels using an external mux, with minimal software overhead. The ADCxEXTMUX[3:0] outputs can be mapped to GPIO pins by configuring the GPIO output crossbar accordingly. The EXTCHSEL field supports up to 4-bit muxes, but fewer mux selection output pins can be configured if desired. 

>To select a specific channel on the external mux, configure ADCSOCxCTRL.CHSEL to select the ADC pin that is connected to the mux output, and configure ADCSOCxCTRL.EXTCHSEL to select the desired mux input channel. There are a variety of potential mux topologies possible. A basic example can be a single external mux connected to a single ADC input channel. This setup is illustrated in _ADC with External Input Mux_ 

536 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [500 x 349] intentionally omitted <==**

**Figure 7-113. ADC with External Input Mux** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 537 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.2.9.1 External Channel Selection**_ 

The ADCSOCxCTRL.EXTCHSEL field for each SOC can be used to automatically control an external mux with digital output pins ADCxEXTMUX[1:0]. This functionality enables the application to add additional ADC channels using an external mux, with minimal software overhead. The ADCxEXTMUXy outputs can be mapped to GPIO pins by configuring the associated IOMUX to use the ADC_EXTCH_XBAR signal accordingly. The EXTCHSEL field supports up to 2-bit muxes, but fewer mux selection output pins can be configured if desired. 

To select a specific channel on the external mux, configure ADCSOCxCTRL.CHSEL to select the ADC pin that is connected to the mux output, and configure ADCSOCxCTRL.EXTCHSEL to select the desired mux input channel. There are a variety of potential mux topologies possible. A basic example can be a single external mux connected to a single ADC input channel. 

- To select ADCxIN0.2, the user configures the SOC with CHSEL = 0 and EXTCHSEL = 2. 

- To select ADCxIN3, the user configures the SOC with CHSEL = 3. The value of EXTCHSEL does not effect the conversion channel selection. 

**==> picture [454 x 200] intentionally omitted <==**

**----- Start of picture text -----**<br>
MCU<br>ADC<br>SOCx (0-n)<br>SOCx (0-15)<br>ADCxEXTMUX[0:a] SOCx (0-15) LEGEND<br>SOC Arbitration  CHSEL<br>CHSEL<br>& Control MCU<br>EXT<br>CHSEL<br>ADC<br>ADCxIN0.0 0 ADC Core<br>ADCxIN0.1 1 ADCxIN0<br>ADCxIN0.2 2 0 SOCx (0-n)<br>... ... ADCxIN1ADCxIN2 12 SOC Arbitration &<br>ADCxIN0.b b ADCxIN3 3 ADC Core Control<br>... ... External MUX<br>ADCxIN* *<br>...<br>...<br>**----- End of picture text -----**<br>


**Figure 7-114. ADC with External Input Mux** 

When using an external channel mux, make sure to comprehend the mux selection and switching delay in the sample/hold time requirement for the SOC. This requirement includes the propagation delay for the output X-BAR (if this is used to configure the mux selection pin), any mux switching delays, and the total resistance and capacitance added to the ADC input network by the external mux device. For more information on calculating the acquisition window size, see Section 7.5.2.20.2. 

There is also an External mux preselect function to allow some of the settling time to be pipelined with during the previous samples conversion time when ADC SOC sequencing is deterministic. 

Refer to the ADC_selectSOCExtChannel() & ADC_enableExtMuxPreselect() APIs. 

Refer to the ADC_selectSOCExtChannel() & ADC_enableExtMuxPreselect() APIs. 

538 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.2.9.2 External Channel Selection Timing**_ 

The ADCxEXTMUX output follows two possible timing schemes, depending on the setting of the EXTMUXPRESELECTEN bit in the ADCCTL1 register: 

- When EXTMUXPRESELECTEN is set to 0, the ADCxEXTMUX output changes at the beginning of the associated SOC's sample and hold period. The applied external mux setting is maintained until the start of the next SOC sample-and-hold period. This is the default configuration at reset. Examples of SOC timings in this mode are shown in Figure 7-115 and Figure 7-117. When external mux preselect is disabled, make sure to configure the SOC acquisition window duration to account for both external mux settling time and internal channel settling time. 

- When EXTMUXPRESELECTEN is set to 1, the ADCxEXTMUX output changes at least one SYSCLK cycle after the end of the sample and hold period. At this point, the ADC sets the external mux selection based on the next highest priority SOC that is pending. If no SOC is pending, then the mux selection is based on the next highest priority SOC, based on the current SOC priority scheme (see Section 7.5.2.11 for more information on SOC priority schemes). Examples of SOC timings in this mode are shown in Figure 7-116 and Figure 7-118. Enabling preselect mode enables the application to avoid increasing the acquisition window duration due to external mux switching and settling delays. 

## **Note** 

When EXTMUXPRESELECTEN is enabled, setting SOC0 as high priority without actually triggering SOC0 conversions is a good way to define an idle value for ADCxEXTMUX. SOC0 always has the highest priority when no SOCs are pending, so the value of ADCSOC0CTL.EXTCHSEL is always pushed onto the mux select pins by default. 

**==> picture [500 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
(1) (2) (3) (4) (5)<br>ePWM1A<br>SOCA<br>S+H SOC1 S+H SOC2 S+H<br>Conversion SOC1  SOC2<br>CONVERSION CONVERSION<br>ADCxEXTMUX SOC1 EXTCHSEL SOC2 EXTCHSEL<br>**----- End of picture text -----**<br>


**Figure 7-115. ADC External Channel Select Timing Example** 

In Figure 7-115, the ADC is configured as follows: 

- SOC1 and SOC2 are triggered from ePWM1A; 

- No high priority SOCs are defined. 

The ADC performs the SOC operation sequence in the following order: 

1. The initial ePWM1A trigger arrives, setting the SOC1 and SOC2 to pending. SOC1 gains priority, and the sample-and-hold period for SOC1 begins. The ADC pushes the value of ADCSOC1CTL.EXTCHSEL onto the ADCxEXTMUX pins at the same time when the SOC1 sample-and-hold begins. 

2. At the end of the sample-and-hold for SOC1, the conversion begins. ADCxEXTMUX remains unchanged until the start of the next SOC sample-and-hold period. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

539 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

3. In this example case, there are no asynchronous high priority triggers defined, so SOC2 sample-andhold starts as soon as SOC1 conversion ends. The ADC pushes ADCSOC2CTL.EXTCHSEL onto the ADCxEXTMUX pins. 

4. At the end of the sample-and-hold for SOC2, there are no more pending SOCs. SOC2 begins conversion, and ADCxEXTMUX is unchanged. 

5. The SOC2 conversion ends. There are no pending SOCs or triggers, so ADCxEXTMUX remains unchanged. 

**==> picture [500 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
(1) (2) (3) (4) (5)<br>ePWM1A<br>SOCA<br>S+H SOC1 S+H SOC2 S+H<br>Conversion SOC1  SOC2<br>CONVERSION CONVERSION<br>ADCxEXTMUX SOC1 EXTCHSEL SOC2 EXTCHSEL SOC3 EXTCHSEL<br>**----- End of picture text -----**<br>


**Figure 7-116. ADC External Channel Timing Example in Preselect Mode** 

In Figure 7-116, the ADC is configured as follows: 

- SOC1 and SOC2 are triggered from ePWM1A; 

- No high priority SOCs are defined. 

The ADC performs the SOC operation sequence in the following order: 

1. The initial ePWM1A trigger arrives, setting the SOC1 and SOC2 to pending. SOC1 gains priority, and the sample-and-hold period for SOC1 begins. The ADC pushes the value of ADCSOC1CTL.EXTCHSEL onto the ADCxEXTMUX pins at the same time when the SOC1 sample-and-hold begins. 

2. At the end of the sample-and-hold for SOC1, the highest priority SOC that is pending is SOC2, so the ADC pushes the value of ADCSOC2CTL.EXTCHSEL onto the ADCxEXTMUX pins. 

3. In this example case, there are no asynchronous high priority triggers defined, so SOC2 sample-andhold starts as soon as SOC1 conversion ends. The ADC pushes ADCSOC2CTL.EXTCHSEL onto the ADCxEXTMUX pins again, but this is already the current value so there is no change. 

4. At the end of the sample-and-hold for SOC2, there are no more pending SOCs. SOC3 has the next highest priority by way of the round-robin pointer, so the ADC pushes the value of ADCSOC3CTL.EXTCHSEL onto ADCxEXTMUX. In this case, the application can set ADCSOC3CTL.EXTCHSEL = ADCSOC1CTL.EXTCHSEL. Although SOC3 is not actually used, this makes sure that the external mux channel is already preselected when the next ePWM1 SOC arrives. 

5. The SOC2 conversion ends. There are no pending SOCs or triggers, so ADCxEXTMUX remains unchanged. 

540 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

**==> picture [504 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
www.ti.com Processors and Accelerators<br>(1) (2) (3) (4) (5) (6) (7)<br>ePWM1A<br>SOCA<br>CPUTIMER1<br>S+H SOC1 S+H SOC0 S+H SOC2 S+H<br>Conversion SOC1  SOC0  SOC2<br>CONVERSION CONVERSION CONVERSION<br>ADCxEXTMUX SOC1 EXTCHSEL SOC0 EXTCHSEL SOC2 EXTCHSEL<br>**----- End of picture text -----**<br>


**Figure 7-117. ADC External Channel Select Timing Example with Asynchronous Trigger** 

In Figure 7-117, the ADC is configured as follows: 

- SOC1 and SOC2 are triggered from ePWM1A; 

- SOC0 is triggered from CPUTIMER1, and has a high priority. 

With this configuration, the ADC performs the SOC operation sequence in the following order: 

1. The initial ePWM1A trigger arrives, setting the SOC1 and SOC2 flags to pending. SOC1 gains priority, and the SOC1 sample-and-hold period begins. The ADC pushes the value of ADCSOC1CTL.EXTCHSEL onto the ADCxEXTMUX pins at the same time when the SOC1 sample-and-hold begins. 

2. At the end of the sample-and-hold for SOC1, the SOC1 conversion begins. ADCxEXTMUX remains unchanged until the start of the next SOC sample-and-hold period. 

3. CPUTIMER1 issues a trigger asynchronously, setting the SOC0 flag to pending. 

4. Since SOC0 has high priority, SOC0 converts next instead of SOC2. The ADC pushes ADCSOC0CTL.EXTCHSEL onto ADCxEXTMUX when the sample-and-hold period for SOC0 starts. 

5. At the end of the sample-and-hold period for SOC0, the conversion for SOC0 begins. ADCxEXTMUX remains unchanged until the start of the next SOC sample-and-hold period. 

6. At the end of the conversion for SOC0, SOC2 is the next pending SOC. SOC2's sample-and-hold period begins, and ADCSOC2CTL.EXTCHSEL is pushed onto the ADCxEXTMUX pins. 

7. The SOC2 conversion begins, and there are no pending SOCs left. ADCxEXTMUX remains unchanged until a new SOC trigger arrives. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 541 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 251] intentionally omitted <==**

**----- Start of picture text -----**<br>
(1) (2) (3) (4) (5) (6) (7)<br>ePWM1A<br>SOCA<br>CPUTIMER1<br>S+H SOC1 S+H SOC0 S+H SOC2 S+H<br>Conversion SOC1  SOC0  SOC2<br>CONVERSION CONVERSION CONVERSION<br>ADCxEXTMUX SOC1 EXTCHSEL SOC2 EXTCHSEL SOC0 EXTCHSEL SOC2 EXTCHSEL SOC0 EXTCHSEL<br>**----- End of picture text -----**<br>


**Figure 7-118. ADC External Channel Timing Example in Preselect Mode with Asynchronous Trigger** 

In Figure 7-118, the ADC is configured as follows: 

- SOC1 and SOC2 are triggered from ePWM1A; 

- SOC0 is triggered from CPUTIMER1, and has a high priority. 

With this configuration, the ADC performs the SOC operation sequence in the following order: 

1. The initial ePWM1A trigger arrives, setting the SOC1 and SOC2 flags to pending. SOC1 gains priority, and the SOC1 sample-and-hold period begins. The ADC pushes the value of ADCSOC1CTL.EXTCHSEL onto the ADCxEXTMUX pins at the same time when the SOC1 sample-and-hold begins. 

2. At the end of the sample-and-hold for SOC1, the highest priority SOC that is pending is SOC2, so the ADC pushes the value of ADCSOC2CTL.EXTCHSEL onto the ADCxEXTMUX pins. 

3. CPUTIMER1 issues a trigger asynchronously, setting the SOC0 flag to pending. 

4. Since SOC0 has high priority, SOC0 converts next instead of SOC2. The ADC overwrites the previous speculative external mux selection (ADCSOC2CTL.EXTCHSEL) with ADCSOC0.EXTCHSEL when the sample-and-hold period for SOC0 starts. In situations like this where asynchronous triggers are possible, make sure to set the acquisition window size of the priority SOC large enough to allow for both external mux settling and internal channel settling. 

5. At the end of the sample-and-hold period for SOC0, the highest priority SOC that is pending is SOC2, so the ADC pushes EXTCHSEL value for SOC2 onto the ADCxEXTMUX pins. SOC0 begins converting. 

6. At the end of the SOC0 conversion, SOC2 is the next highest-priority pending SOC, and so SOC2's sampleand-hold period begins. The ADC again pushes ADCSOC2CTL.EXTCHSEL onto the ADCxEXTMUX pins, but since this is already the current value, the mux pins are unchanged. 

7. At the end of the sample-and-hold period for SOC2, there are no SOCs pending. SOC0 has the next highest priority, since the ADC has been configured to give SOC0 high priority. The ADC pushes ADCSOC0CTL.EXTCHSEL onto the ADCxEXTMUX pins. 

542 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.2.10 SOC Configuration Examples** 

The following sections provide some specific examples of how to configure the SOCs to produce some conversions. 

## _**7.5.2.10.1 Single Conversion from ePWM Trigger**_ 

SOC5 is chosen arbitrarily. Any of the SOCs can be used. 

Assuming a 100ns sample window is desired with a SYSCLK frequency of MHz, then the acquisition window duration must be cycles. The ACQPS field must be set to . 

As configured, when ePWM3 matches the period and generates the SOCB signal, the ADC begins sampling channel ADCINA1 (SOC5) immediately if the ADC is idle. If the ADC is busy, ADCINA1 begins sampling when SOC5 gains priority (see Section 7.5.2.11). The ADC control logic samples ADCINA1 with the specified acquisition window width of 100ns. Immediately after the acquisition is complete, the ADC begins converting the sampled voltage to a digital value. When the ADC conversion is complete, the results are available in the ADCRESULT5 register (see Section 7.5.2.19 for exact sample, conversion, and result latch timings). 

## _**7.5.2.10.2 Oversampled Conversion from ePWM Trigger**_ 

To configure the ADC to oversample ADCINA1 four times, we use the same configurations as the previous example, but apply them to SOC5, SOC6, SOC7, and SOC8. 

As configured, when ePWM3 matches the period and generates the SOCB signal, the ADC begins sampling channel ADCINA1 (SOC5) immediately if the ADC is idle. If the ADC is busy, ADCINA1 begins sampling when SOC5 gains priority (see Section 7.5.2.11). Once the conversion is complete for SOC5, SOC6 begins converting ADCINA1 and the results for SOC5 are placed in the ADCRESULT5 register. All four conversions eventually are completed sequentially, with the results in ADCRESULT5, ADCRESULT6, ADCRESULT7, and ADCRESULT8 for SOC5, SOC6, SOC7, and SOC8, respectively. 

## **Note** 

Possible, but unlikely, that the ADC can begin converting SOC6, SOC7, or SOC8 before SOC5 depending on the position of the round-robin pointer when the ePWM trigger is received. See Section 7.5.2.11 to understand how the next SOC to be converted is chosen. 

## _**7.5.2.10.3 Software Triggering of SOCs**_ 

At any point, whether or not the SOCs have been configured to accept a specific trigger, a software trigger can set the SOCs to be converted. This is accomplished by writing bits in the ADCSOCFRC1 register. 

Software triggering of the previous example without waiting for the CPU1 Timer 2 to generate the trigger can be accomplished by the statement: 

```
AdcaRegs.ADCSOCFRC1.all = 0x000F;        //set SOC flags for SOC0 to SOC3
```

## **7.5.2.11 ADC Conversion Priority** 

When multiple SOC flags are set at the same time, one of two forms of priority determines the converted order. The default priority method is round-robin. In this scheme, no SOC has an inherent higher priority than another. Priority depends on the round-robin pointer (RRPOINTER). The RRPOINTER reflected in the ADCSOCPRIORITYCTL register points to the last SOC converted. The highest priority SOC is given to the next value greater than the RRPOINTER value, wrapping around back to SOC0 after SOC15. At reset the value is 16 since 0 indicates a conversion has already occurred. When RRPOINTER equals 16 the highest priority is given to SOC0. The RRPOINTER is reset when the ADC module is reset or when the reset value is written to the SOCPRICTL register. The ADC module is reset by writing and clearing the SOFTPRES bit corresponding to the ADC instance. 

An example of the round-robin priority method is given in Figure 7-119. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

543 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

The SOCPRIORITY field in the ADCSOCPRIORITYCTL register can be used to assign high priority from a single to all of the SOCs. When configured as high priority, an SOC interrupts the round-robin wheel after any current conversion completes and inserts in as the next conversion. After the conversion completes, the round-robin wheel continues where the conversion was interrupted. If two high priority SOCs are triggered at the same time, the SOC with the lower number takes precedence. 

High priority mode is assigned first to SOC0, then in increasing numerical order. The value written in the SOCPRIORITY field defines the first SOC that is not high priority. In other words, if a value of 4 is written into SOCPRIORITY, then SOC0, SOC1, SOC2, and SOC3 are defined as high priority, with SOC0 the highest. 

An example using high priority SOC’s is given in Figure 7-120. 

544 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [384 x 554] intentionally omitted <==**

**----- Start of picture text -----**<br>
A After reset,SOC7 receives trigger ;SOC0 is highest priority SOC ; A SOC15 SOC0 SOC1<br>SOC7 configured channel is converted SOC SOC<br>immediately. 14 2<br>SOC SOC<br>B RRPOINTER changes to point to SOC 7; 13 3<br>SOC8 is now highest priority SOC .<br>SOC RRPOINTER SOC<br>C SOC2 & SOC12 triggers rcvd. simultaneously ; 12 (default = 16) 4<br>SOC12 is first on round robin wheel ;<br>SOC12 configured channel is converted while SOC SOC<br>SOC2 stays pending. 11 5<br>D RRPOINTER changes to point to SOC 12; SOC SOC<br>SOC2 configured channel is now converted . 10 6<br>SOC SOC<br>9 SOC 7<br>E RRPOINTER changes to point to SOC 2; 8<br>SOC3 is now highest priority SOC .<br>B SOC C SOC<br>SOC 0 SOC SOC 0 SOC<br>15 1 15 1<br>SOC SOC SOC SOC<br>14 2 14 2<br>SOC SOC SOC SOC<br>13 3 13 3<br>SOC RRPOINTER SOC SOC RRPOINTER SOC<br>12 (value = 7) 4 12 (value = 7) 4<br>SOC SOC SOC SOC<br>11 5 11 5<br>SOC SOC SOC SOC<br>10 6 10 6<br>SOC SOC SOC SOC<br>9 SOC 7 9 SOC 7<br>8 8<br>D SOC E SOC<br>SOC 0 SOC SOC 0 SOC<br>15 1 15 1<br>SOC SOC SOC SOC<br>14 2 14 2<br>SOC SOC SOC SOC<br>13 3 13 3<br>SOC RRPOINTER SOC SOC RRPOINTER SOC<br>12 (value = 12) 4 12 (value = 2) 4<br>SOC SOC SOC SOC<br>11 5 11 5<br>SOC SOC SOC SOC<br>10 6 10 6<br>SOC SOC SOC SOC<br>9 SOC 7 9 SOC 7<br>8 8<br>**----- End of picture text -----**<br>


**Figure 7-119. Round Robin Priority Example** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

545 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [442 x 550] intentionally omitted <==**

**----- Start of picture text -----**<br>
Example when SOCPRIORITY = 4 A SOC<br>SOC 4 SOC<br>15 5<br>A After reset, SOC4 is 1 [st] on round robin wheel ; High Priority<br>SOC7 receives trigger ; SOC SOC SOC<br>SOC7 configured channel is converted immediately . 0 14 6<br>B RRPOINTER changes to point to SOC 7; SOC<br>SOC8 is now 1 [st] on round robin wheel . 1<br>SOC RRPOINTER SOC<br>C SOC2 & SOC12 triggers rcvd. simultaneously ; SOC 13 (default = 16) 7<br>2<br>SOC2 interrupts round robin wheel and SOC 2 configured<br>channel is converted while SOC 12 stays pending . SOC SOC SOC<br>3 12 8<br>D RRPOINTER stays pointing to 7;<br>SOC12 configured channel is now converted . SOC SOC<br>11 SOC 9<br>E RRPOINTER changes to point to SOC 12; 10<br>SOC13 is now 1 [st] on round robin wheel .<br>B SOC C SOC<br>SOC 4 SOC SOC 4 SOC<br>High Priority 15 5 High Priority 15 5<br>SOC SOC SOC SOC SOC SOC<br>0 14 6 0 14 6<br>SOC SOC<br>1 1<br>SOC RRPOINTER SOC SOC RRPOINTER SOC<br>SOC 13 (value = 7) 7 SOC 13 (value = 7) 7<br>2 2<br>SOC SOC SOC SOC SOC SOC<br>3 12 8 3 12 8<br>SOC SOC SOC SOC<br>11 SOC 9 11 SOC 9<br>10 10<br>D SOC E SOC<br>SOC 4 SOC SOC 4 SOC<br>High Priority 15 5 High Priority 15 5<br>SOC SOC SOC SOC SOC SOC<br>0 14 6 0 14 6<br>SOC SOC<br>1 1<br>SOC RRPOINTER SOC SOC RRPOINTER SOC<br>SOC 13 (value = 7) 7 SOC 13 (value = 12) 7<br>2 2<br>SOC SOC SOC SOC SOC SOC<br>3 12 8 3 12 8<br>SOC SOC SOC SOC<br>11 SOC 9 11 SOC 9<br>10 10<br>**----- End of picture text -----**<br>


**Figure 7-120. High Priority Example** 

546 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.2.12 Burst Mode** 

Burst mode allows a single trigger to walk through the round-robin SOCs one or more at a time. Setting the bit BURSTEN in the ADCBURSTCTL register configures the ADC wrapper for burst mode. This causes the TRIGSEL field to be ignored, but only for SOCs that are configured for round-robin operation (not high priority). Instead of the TRIGSEL field, all round-robin SOCs are triggered based on the BURSTTRIG field in the ADCBURSTCTL register. Upon reception of the burst trigger, the ADC wrapper does not set all round-robin SOCs to be converted, but only (ADCBURSTCTL.BURSTSIZE + 1) SOCs. The first SOC to be set is the SOC with the highest priority based on the round-robin pointer, and subsequent SOCs are set until BURSTSIZE SOCs have been set. 

## **Note** 

When configuring the ADC for burst mode, the user is responsible for ensuring that each burst of conversions is allowed to complete before the next burst trigger is received. The value of (ADCBURSTCTL.BURSTSIZE + 1) must be less than or equal to the number of SOCs configured for round-robin priority. If the previous burst is not complete at the time when a new burst trigger arrives, for each SOC that was already pending and receives a new trigger, the corresponding overflow flag in ADCSOCOVF1 is set. 

For example, if SOCPRIORITY = 12, that is, SOC12, SOC13, SOC14, and SOC15 are in round-robin, ADCBURSTCTL.BURSTSIZE setting must be ≤3 for burst mode to operate correctly. 

## _**7.5.2.12.1 Burst Mode Example**_ 

Burst mode can be used to sample a different set of signals on every other trigger. In the following example, ADCIN7 and ADCIN5 are converted on the first trigger from CPU1 Timer 2 and every other trigger thereafter. ADCIN2 and ACIN3 are converted on the second trigger from CPU1 Timer 2 and every other trigger thereafter. All signals are converted with 20 SYSCLK cycle wide acquisition windows, but different durations can be configured for each SOC as desired. 

```
AdcaRegs.BURSTCTL.BURSTEN = 1;             //Enable ADC burst mode
AdcaRegs.BURSTCTL.BURSTTRIG = 3;           //CPU1 Timer 2 triggers burst of conversions
AdcaRegs.BURSTCTL.BURSTSIZE = 1;           //conversion bursts are 1 + 1 = 2 conversions long
AdcaRegs.SOCPRICTL.bit.SOCPRIORITY = 12;   //SOC0 to SOC11 are high priority
AdcaRegs.ADCSOC12CTL.bit.CHSEL = 7;        //SOC12 converts ADCINA7
AdcaRegs.ADCSOC12CTL.bit.ACQPS = 19;       //SOC12 uses sample duration of 20 SYSCLK cycles
AdcaRegs.ADCSOC13CTL.bit.CHSEL = 5;        //SOC13 converts ADCINA5
AdcaRegs.ADCSOC13CTL.bit.ACQPS = 19;       //SOC13 uses sample duration of 20 SYSCLK cycles
AdcaRegs.ADCSOC14CTL.bit.CHSEL = 2;        //SOC14 converts ADCINA2
AdcaRegs.ADCSOC14CTL.bit.ACQPS = 19;       //SOC14 uses sample duration of 20 SYSCLK cycles
AdcaRegs.ADCSOC15CTL.bit.CHSEL = 3;        //SOC15 converts ADCINA3
AdcaRegs.ADCSOC15CTL.bit.ACQPS = 19;       //SOC15 uses sample duration of 20 SYSCLK cycles
```

When the first CPU1 Timer 2 trigger is received, SOC12 and SOC13 are converted immediately if the ADC is idle. If the ADC is busy, SOC12 and SOC13 are converted once the SOCs gain priority. The results for SOC12 and SOC13 are in ADCRESULT12 and ADCRESULT13, respectively. After SOC13 completes, the round-robin pointer gives the highest priority to SOC14. Because of this, when the next CPU1 Timer 2 trigger is received, SOC14 and SOC15 is set as pending and eventually converted. The results for SOC14 and SOC15 are in ADCRESULT14 and ADCRESULT15, respectively. Subsequent triggers continue to toggle between converting SOC12 and SOC13, and converting SOC14 and SOC15. 

While the above example toggles between two sets of conversions, three or more different sets of conversions can be achieved using a similar approach. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 547 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.2.12.2 Burst Mode Priority Example**_ 

An example of priority resolution using burst mode and high-priority SOCs is presented in Figure 7-121. 

**==> picture [468 x 581] intentionally omitted <==**

**----- Start of picture text -----**<br>
Example when SOCPRIORITY = 4, BURSTEN = 1, and A SOC<br>BURSTSIZE = 1 SOC 4 SOC<br>After reset, SOC4 is 1st on round robin wheel; PriorityHigh 15 5<br>A BURSTTRIG trigger is received;<br>SOC4 & SOC5 are set and configured channels converted SOC SOC SOC<br>immediately. 0 14 6<br>RRPOINTER changes to point to SOC5; SOC<br>B SOC6 is now 1st on round robin wheel. 1<br>SOC RRPOINTER SOC<br>BURSTTRIG & SOC1 triggers rcvd. simultaneously; 13 (default = 16) 7<br>SOC1, SOC6, and SOC7 are set; SOC<br>C 2<br>SOC1 interrupts round robin wheel and SOC1 configured<br>channel is converted while SOC6 and SOC7 stay pending.<br>SOC SOC SOC<br>RRPOINTER stays pointing to 5; 3 12 8<br>D SOC6/SOC7 configured channels are now converted.<br>SOC SOC<br>E RRPOINTER changes to point to SOC7;SOC8 is now 1st on round robin wheel, waiting for BURSTTRIG. 11 SOC 9<br>10<br>B SOC C SOC<br>SOC 4 SOC SOC 4 SOC<br>High 15 5 High 15 5<br>Priority Priority<br>SOC SOC SOC SOC SOC SOC<br>0 14 6 0 14 6<br>SOC SOC<br>1 1<br>SOC RRPOINTER SOC SOC RRPOINTER SOC<br>13 (value = 5) 7 13 (value = 5) 7<br>SOC SOC<br>2 2<br>SOC SOC SOC SOC SOC SOC<br>3 12 8 3 12 8<br>SOC SOC SOC SOC<br>11 SOC 9 11 SOC 9<br>10 10<br>D SOC E SOC<br>SOC 4 SOC SOC 4 SOC<br>High 15 5 High 15 5<br>Priority Priority<br>SOC SOC SOC SOC SOC SOC<br>0 14 6 0 14 6<br>SOC SOC<br>1 1<br>SOC RRPOINTER SOC SOC RRPOINTER SOC<br>13 (value = 5) 7 13 (value = 7) 7<br>SOC SOC<br>2 2<br>SOC SOC SOC SOC SOC SOC<br>3 12 8 3 12 8<br>SOC SOC SOC SOC<br>11 SOC 9 11 SOC 9<br>10 10<br>**----- End of picture text -----**<br>


**Figure 7-121. Burst Priority Example** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

548 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.2.13 EOC and Interrupt Operation** 

Each SOC has a corresponding end-of-conversion (EOC) signal. This EOC signal can be used to trigger an ADC interrupt. The ADC can be configured to generate the EOC pulse at either the end of the acquisition window or at the end of the voltage conversion. This is configured using the bit INTPULSEPOS in the ADCCTL1 register. See Section 7.5.2.19 for exact EOC pulse location. 

Each ADC module has 4 configurable ADC interrupts. These interrupts can be triggered by any of the 16 EOC signals. The flag bit for each ADCINT can be read directly to determine if the associated SOC is complete or the interrupt can be passed on to the VIM. Each ADCINT flag also has a corresponding ADCINTxRESULT flag. The ADCINTxRESULT flag is only set when results corresponding to the EOC are latched. This is useful for interrupt service routines or CLA tasks with early interrupt timing configured, allowing the application code to perform some pre-processing or setup work, and then acting on the ADC conversion result as soon as the result is latched. 

It is also possible to generate an ADC interrupt based on a PPB oversampling logic event, such as when the sample count matches the configured limit. There are four oversampling interrupt (OSINT) flags available in each module for this purpose. Any of the ADCINT flags can be configured for an OSINT by configuring the INTxSEL field the corresponding ADCINTSELxNy register. 

## **Note** 

The ADCCTL1.ADCBSY bit being clear does not indicate that all conversions in a set of SOCs have completed, only that the ADC is ready to process the next conversion. To determine if a sequence of SOCs is complete, link an ADCINT flag to the last SOC in the sequence and monitor that ADCINT flag. 

_ADC EOC Interrupts_ shows a block diagram of the ADC interrupt structure. The ADCINT1 and ADCINT2 Signals can be configured to generate an SOCx trigger to help create a continuous stream of conversions. 

**==> picture [500 x 249] intentionally omitted <==**

**----- Start of picture text -----**<br>
INT4<br>INT3<br>INT2<br>INT1<br>INTSEL1N2.INT1SEL<br>ADCINT4 to PIE<br>INTSEL1N2.INT1E<br>0 INTSEL1N2.INT1CONT ADCINT3 to PIE<br>1<br>EOC15:EOC0 2 ADCINT2 to PIE<br>1<br>1<br>Set<br>0 ADCINT1 to PIE<br>15 Latch 0<br>16<br>OSINT1:OSINT4<br>Clear<br>19<br>INTOVF<br>ADCINTFLGCLR.ADCINT1 ADCINTFLG.ADCINT1<br>ADC Sample<br>Generation Logic ADC PPB Logic<br>EOC<br>OSINT<br>**----- End of picture text -----**<br>


**Figure 7-122. ADC End-of-Conversion (EOC) Signal Interrupts** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

549 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.2.13.1 Interrupt Overflow**_ 

If the EOC signal sets a flag in the ADCINTFLG register, but that flag is already set, an interrupt overflow occurs. By default, overflow interrupts are not passed on to the VIM module. When an overflow occurs on a given flag in the ADCINTFLG register, the corresponding flag in the ADCINOVF register is set. This overflow flag is only used to detect that an overflow has occurred; the flag does not block further interrupts from propagating to the VIM module. 

When an ADC interrupt overflow occurs, the application must check the appropriate ADCINTOVF flag inside the ISR or in the background loop and take appropriate action when an overflow is detected. 

## _**7.5.2.13.2 Continue to Interrupt Mode**_ 

The INTxCONT bits in the ADCINTSEL1N2 and ADCINTSEL3N4 registers configure how interrupts are handled when an ADCINTFLG has not yet been cleared from a prior interrupt.  This mode is disabled by default and additional overlapping interrupts are not issued to the VIM. By activating this mode, ADC interrupts always reach the VIM. If interrupts occur while ADCINTFLG is set, the ADCINTOVF register remains set regardless of the configuration of the INTxCONT bits. 

## _**7.5.2.13.3 Early Interrupt Configuration Mode**_ 

Enabling early interrupt mode can allow the application to enter the ADC interrupt service routine before the ADC results are ready. This allows the application to do any necessary pre-work so that the application can act on the ADC results immediately when the ADC results become available. If the timing of the early interrupt is too early, then the application needs to waste time until the updated ADC results become available. To prevent this situation, the time the ADC interrupt is entered in early interrupt mode is configurable by way of the DELAY field in the ADCINTCYCLE register. 

- To use the configurable interrupt time, the ADC must be in early interrupt mode. To achieve this, clear the bit INTPULSEPOS to 0 in ADCCTL1. 

- The DELAY value in the ADCINTCYCLE register sets the number of additional SYSCLK cycles after the falling edge of the SOC pulse before the ADCINT flag is set. 

- If the value of DELAY goes beyond EOC, the ADC interrupt is generated along with EOC. 

- Writing values to DELAY when INTPULSEPOS is set to 1 does not have any effect on the interrupt generation. 

To determine exactly when the ADC result has been latched into the ADCRESULT register, poll the ADCINTxRESULT flag bit in the ADCINTFLG register. 

550 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.2.14 Post-Processing Blocks** 

Each ADC module contains post-processing blocks (PPB). These blocks can be associated with any of the RESULT registers using the ADCPPBxCONFIG.CONFIG bit field. The post-processing blocks have the ability to: 

- Remove an offset associated with the ADCIN channel 

- Subtract out a reference value 

- Aggregate successive samples using sum , max, and min calculations 

- Automatically calculate average of oversampled conversions without CPU overhead, when sample count is a power of 2 

- Transform the conversion result into an absolute value 

- Flag a zero-crossing point, with the option to trip a PWM and generate an interrupt 

- Flag a high or low compare limit, with the option to trip a PWM and generate an interrupt 

- Record the delay between the associated SOC trigger and when sampling actually begins 

Figure 7-123 presents the structure of each PPB. Subsequent sections explain the use of each submodule. 

**==> picture [500 x 315] intentionally omitted <==**

**----- Start of picture text -----**<br>
ADC Post Processing Blocks<br>TRIGGER[15:0]   SOCxSTART[15:0]<br>Start DelayCalculation CONFIG Aggregation (t+2)<br>ADCPPBx.SYNCINSEL<br>Latch on<br>SOC Pending<br>REQSTAMPx Latch on HW Sync.<br>+ - � DLYSTAMPxSOC Start results to their final locations and reset Sync.: Transfer all partial aggregation  Options<br>all partial aggregation results. ADCPPBxCONFIG2<br>.SWSYNC<br>Target<br>RESULT ADCPPBxOFFCAL Sample Count ADCPPBxLIMIT Limit Match Sync. + Ext Sync. ADCOSINTx<br>ADCOSINT1<br>+ Partial =? ADCOSINT2<br>saturate � - Sample Count Limit Match Sync. ADCOSINT3<br>Reset ADCPPBxPCOUNT +1 ADCOSINT4<br>Final Increment for  ADCPPBxCONFIG2.<br>Sample Count each new sample OSINTSEL<br>Load ADCPPBxCOUNT<br>Sync. Sync. Sync.<br>+<br>ADCPPBxOFFREF - � Max Min Accumulate ADCEVTINTx<br>ADCPPBxCONFIG. ADCPPBxPMAX ADCPPBxPMIN Limit<br>ABS |x| ADCPPBxMAX ADCPPBxMIN ADCPPBxPSUM Lim it compare compare  ADCEVTINT<br>ADCPPBxPMAXI ADCPPBxPMINI ADCPPBxSHIFT and zero and zero<br>ADCPPBxCONFIG.TWOSCOMPEN -x ADCPPBxMAXI ADCPPBxMINI ADCPPBxSUM crossing locrossin g ic<br>logic<br>ADCPPBxRESULT<br>ADCEVTx<br>ADCEVT1<br>ADCEVT2<br>Post Processing Block (1-4) ADCEVT3<br>ADCEVT4<br>FREECOUNT<br>0–15 Regs<br>ADCRESULT<br>**----- End of picture text -----**<br>


**Figure 7-123. ADC Post-Processing Blocks (PPB) Block Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

551 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.2.14.1 PPB Offset Correction**_ 

In many applications, external sensors and signal sources produce an offset. A global trimming of the ADC offset is not enough to compensate for these offsets, which vary from channel to channel. The post-processing block can remove these offsets with zero overhead, saving numerous cycles in tight control loops. 

Offset correction is accomplished by first pointing the ADCPPBxCONFIG.CONFIG to the desired SOC, then writing an offset correction value to the ADCPPBxOFFCAL.OFFCAL register. The post-processing block automatically adds or subtracts the value in the OFFCAL register from the raw conversion result and stores the value in the ADCRESULT register. 

## **Note** 

- Writing a 0 to the OFFCAL register effectively disables the offset correction feature, passing the raw result unchanged to the ADCRESULT register. 

- It is possible to point multiple PPBs to the same SOC. In this case, the OFFCAL value that is actually applied comes from the PPB with the highest number. 

- In particular, care needs to be taken when using the PPB on SOC0, as all PPBs point to this SOC by default. This can cause unintentional overwriting of offset correction of a lower numbered PPB by a higher numbered PPB. 

## _**7.5.2.14.2 PPB Error Calculation**_ 

In many applications, an error from a set point or expected value must be computed from the digital output of an ADC conversion. In other cases, a bipolar signal is necessary or convenient for control calculations. The PPB can perform these functions automatically, reducing the sample to output latency and reducing software overhead. 

Error calculation is accomplished by first pointing the ADCPPBxCONFIG.CONFIG to the desired SOC, then writing a value to the ADCPPBxOFFCAL.OFFREF register. The post-processing block automatically subtracts the value in the OFFREF register from the ADCRESULT value and stores the value in the ADCPPBxRESULT register. This subtraction produces a sign-extended 32-bit result. It is also possible to selectively invert the calculated value before storing in the ADCPPBxRESULT register by setting the TWOSCOMPEN bit in the ADCPPBxCONFIG register. 

## **Note** 

- In 12-bit mode, do not write a value larger than 12 bits to the ADCPPBxOFFREF register. 

- Since the ADCPPBxRESULT register is unique for each PPB, it is possible to point multiple PPBs to the same SOC and get different results for each PPB. 

- Writing a 0 to the ADCPPBxOFFREF register effectively disables the error calculation feature, passing the ADCRESULT value unchanged to the ADCPPBxRESULT register. 

- Writing a new value to ADCPPBxOFFREF causes an immediate update to the ADCPPBxRESULT register. However, the flags coming out of the PPB do not change until the next end-of-conversion (EOC). For instance, if changing the ADCPPBxOFFREF register causes ADCPPBxRESULT to change signs, but the next conversion brings the result back to the same sign as before the OFFREF change, no ADCPPBxZERO flag is set. 

## _**7.5.2.14.3 PPB Limit Detection and Zero-Crossing Detection**_ 

Many applications perform a limit check against the ADC conversion results. The PPB can automatically perform a check against high and low limits, or whenever ADCPPBxRESULT changes sign. Based on these comparisons, the PPB can generate a trip to the PWM and an interrupt automatically, lowering the sample to 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

552 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

ePWM latency and reducing software overhead. This functionality also enables safety-conscious applications to trip the ePWM based on an out-of-range ADC conversion without any CPU intervention. 

To enable this functionality, first point the ADCPPBxCONFIG.CONFIG to the desired SOC, then write a value to one or both of the registers ADCPPBxTRIPHI.LIMITHI and ADCPPBxTRIPLO.LIMITLO (zero-crossing detection does not require further configuration). Whenever these limits are exceeded, the PPBxTRIPHI bit or PPBxTRIPLO bit is set in the ADCEVTSTAT register. Note that the PPBxZERO bit in the ADCEVTSTAT register is gated by end-of-conversion (EOC), not by the sign change in the ADCPPBxRESULT register. The ADCEVTCLR register has corresponding bits to clear these event flags. The ADCEVTSEL register has corresponding bits which allow the events to propagate through to the PWM. The ADCEVTINTSEL register has corresponding bits that allow the events to propagate through to the PIE. 

One VIM interrupt is shared between all the PPBs for a given ADC module as shown in Figure 7-124. 

## **Note** 

- If different actions need to be taken for different PPB events from the same ADC module, then the ADCEVTINT ISR has to read the PPB event flags in the ADCEVTSTAT register to determine which event caused the interrupt. 

- If different ePWM trips need to be generated separately for high compare, low compare, and zero-crossing, this can be achieved by pointing multiple PPBs to the same SOC. 

- The zero-crossing detect circuit considers a result of zero to be positive. 

**==> picture [418 x 326] intentionally omitted <==**

**----- Start of picture text -----**<br>
Post Processing Block1<br>EVENTx ADCEVT1<br>INTx<br>Post Processing Block2<br>EVENTx ADCEVT2<br>INTx<br>ADCEVTINT<br>Post Processing Block3<br>EVENTx ADCEVT3<br>INTx<br>Post Processing Block4<br>EVENTx ADCEVT4<br>INTx<br>**----- End of picture text -----**<br>


**Figure 7-124. ADC PPB Interrupt Event** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

553 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.2.14.4 PPB Sample Delay Capture**_ 

When multiple control loops are running asynchronously on the same ADC, there is a chance that an ADC request from two or more loops collide, causing one of the samples to be delayed. This shows up as a measurement error in the system. By knowing when this delay occurs and the amount of delay that has occurred, software can employ extrapolation techniques to reduce the error. 

To this effect, each PPB has the field DLYSTAMP in the ADCPPBxSTAMP register. This field contains the number of SYSCLK cycles between when the associate SOC was triggered and when the SOC began converting. 

This is achieved by having a global 12-bit free running counter based off of SYSCLK, which is in the field FREECOUNT in the ADCCOUNTER register. When the trigger for the associated SOC arrives, the value of this counter is loaded into the bit field ADCPPBxTRIPLO.REQSTAMP. When the actual sample window for that SOC begins, the value in REQSTAMP is subtracted from the current FREECOUNT value and stored in DLYSTAMP. 

## **Note** 

If more than 4096 SYSCLK cycles elapse between the SOC trigger and the actual start of the SOC acquisition, the FREECOUNT register can overflow more than once, leading to incorrect DLYSTAMP value. Be cautious when using very slow conversions to prevent this from happening. 

The sample delay capture does not function, if the associated SOC is triggered using software. The sample delay capture, however, correctly records the delay, if the software triggering of a different SOC causes the SOC associated with the PPB to be delayed 

## _**7.5.2.14.5 PPB Oversampling**_ 

This ADC has built-in support for oversampling in the post-processing block, including an accumulator, min/max for peak detection, and outlier removal. The oversampling support module exists at the output of the sample correction module, as shown in Figure 7-123. The oversampling module works by accumulating results in partial registers until either the sample count limit defined in the ADCPPBxLIMIT register is reached, an external hardware sync event occurs, or the software forces a sync event by writing to the SWSYNC bit in the ADCPPBxCONFIG2 register. The application can configure the PPB to sync from any of the hardware sources defined in Table 7-118 by writing to the SYNCINSEL field of the ADCPPBxCONFIG2 register. 

**Table 7-118. PPB SYNCINSEL Connections** 

|**ADCPPBxCONFIG2.SYNCINSEL**|**Connection From:**|
|---|---|
|0|Disable SyncIN to PPBx|
|1|EPWM1SYNCOUT|
|2|EPWM2SYNCOUT|
|3|EPWM3SYNCOUT|
|...|...|
|29|EPWM29SYNCOUT|
|30|EPWM30SYNCOUT|
|31|EPWM31SYNCOUT|
|32|RSVD|
|33|ECAP1SYNCOUT|
|34|ECAP2SYNCOUT|
|35|ECAP3SYNCOUT|
|...|...|
|45|ECAP13SYNCOUT|
|46|ECAP14SYNCOUT|
|47|ECAP15SYNCOUT|



554 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-118. PPB SYNCINSEL Connections (continued)** 

|**ADCPPBxCONFIG2.SYNCINSEL**|**Connection From:**|
|---|---|
|48|RSVD|
|49|INPUTXBAROUT6|
|50|INPUTXBAROUT7|
|51|CPSW.CPTS_SYNC|
|52-63|RSVD|



## _**7.5.2.14.5.1 Accumulation, Minimum, Maximum, and Average Functions**_ 

At the end of each ADC sample conversion, the PPB updates the partial result registers ADCPPBxPSUM, ADCPPBxPMIN, and ADCPPBxPMAX with the newly processed conversion result from the ADCPPBxRESULT register, and the partial conversion count register (ADCPPBxPCOUNT) increments by 1. When the partial conversion count equals the limit defined in ADCPPBxLIMIT, or the PPB receives a hardware or software sync signal, the PPB takes the following actions: 

1. The PPB loads the values of the respective partial result registers into the final result registers ADCPPBxPSUM, ADCPPBxPMIN, and ADCPPBxPMAX. 

2. The PPB loads the partial count in ADCPPBxPCOUNT into the final conversion count register ADCPPBxCOUNT. 

3. The partial count register and partial result registers reset to zero. 

4. The ADC generates an oversampling interrupt (OSINTx) event pulse, which triggers a CPU interrupt if so configured in the ADCINTSEL1N2 or ADCINTSEL3N4 registers. 

The PPB can also be configured to generate an oversampling interrupt when there is a hardware or software sync event. To trigger an OSINTx pulse when a sync event occurs, write 1 to the OSINTSEL bit in the ADCPPBxCONFIG2 register. 

The PPB can automatically compute the average of the accumulated samples if ADCPPBxLIMIT is set to a power of 2 (up to a maximum of 1024 samples). To perform automatic averaging over 2[n] samples, set the SHIFT field in the ADCPPBxCONFIG2 register to n. When this field is set, the PPB divides the value of ADCPPBxPSUM by 2[n] before loading into ADCPPBxSUM. 

To compute an average from the accumulated sum when the number of samples is not a power of 2, divide the value of ADCPPBxSUM by the value of ADCPPBxCOUNT using the CPU. 

## **Note** 

When using a sync signal to the repeater module and post-processing block to reset the ADC, note that the repeater sync signal does not stop or abort any pending SOCs. If both sync signals are issued simultaneously, any additional pending SOCs can propagate through the post-processing block after the sync signal has been issued. To fully clear or reset the ADC when using the repeater and PPB accumulation logic together: 

1. Disable the repeater module trigger source. 

2. Reset the trigger repeater by issuing a sync signal to the repeater module. 

3. Wait for any pending SOCs to complete. 

4. Finally, issue a sync signal to the post-processing block to complete the ADC reset. 

## _**7.5.2.14.5.2 Outlier Rejection**_ 

The post-processing block enables the application to easily perform outlier rejection, by eliminating the largest and smallest samples during each SOC burst. To eliminate outliers, the following formula can be used in a software routine or ISR: 

ADCPPBxSUM −ADCPPBxMAX −ADCPPBxMIN Average = ADCPPBxCOUNT −2 

(5) 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 555 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.2.15 Result Safety Checker** 

For safety-critical applications, this device provides the ability to automatically compare ADC conversion results from multiple ADC modules against each other for consistency. The number of available safety checker tiles is specified in the device data sheet. Each ADC checker tile captures conversion results from the associated ADCs as soon as the conversions are complete, and compares the absolute value of the difference to the configured tolerance. If the computed delta is out of range, the checker can generate a trip event signal that is sent to an ePWM or output crossbar, and can also trigger an CPU interrupt. Figure 7-125 illustrates the structure and operation of an ADC result safety checker tile. 

**==> picture [499 x 254] intentionally omitted <==**

**----- Start of picture text -----**<br>
Safety Checker<br> Result Bus<br>Selector 1 enable tile<br>ADCSEL ADCRESULTSEL<br>CHKEN TOLERANCE<br>y<br>x x out-of-tolerance<br>CHECKRESULT1 |x – y| x > y? OOTFLG.OOTx<br>S SET Q RES1READY<br>set<br>RES1OVF     y<br>READY set when this result is  R CLR Q OOT OOTFLGCLR.OOTx<br>captured, cleared when both  clear<br>results are captured<br>When OOT flag is set, no further<br>CHECKRESULT will be captured<br>ADCSEL ADCRESULTSEL Selector 2 until all CPUs with OOTx enabled  To Checker Interrupt<br>and Event Selection<br>to CHECKINT have cleared the<br>OOTx flag<br>CHECKRESULT2<br>S SET Q RES2READY RES1OVF<br>READY set when this result is  RES2OVF RES2OVF<br>captured, cleared when both  R CLR Q<br>results are captured<br>ADC Result Safety Checker Tile 1<br>ADC Result Safety Checker Tile 2<br>ADC Result Safety Checker Tile 2<br>ADC Result Safety Checker Tile n<br>Safety Checker<br> Result Bus<br>**----- End of picture text -----**<br>


**Figure 7-125. ADC Safety Checker Tile Diagram** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

556 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.2.15.1 Result Safety Checker Operation**_ 

Each ADC result safety checker tile can be configured to automatically compare two ADC conversion results against a set tolerance value, and generate an interrupt if an out-of-tolerance (OOT) event occurs. The selected results can be from the same ADC instance, or from different ADCs. The safety checker tiles exist outside of the ADC module, enabling the user application to compare results from two separate ADCs. To enable result safety checking, the application must first configure one or more ADCs to enable output of the desired results to the safety checker bus, and then configure the safety checker tile to compare those results. 

To configure an ADC result safety checker tile: 

1. Enable output of the desired ADC results for each ADC by writing to the ADC_REGSn.ADCSAFECHECKRESEN register. For each SOC, any one of the conversion result, PPB result, or PPB sum can be enabled for output to the safety checker bus by writing to ADCSAFECHECKRESEN.SOCxCHKEN. 

2. Select the first result to compare by writing to the ADC_SAFECHECK_REGSn.ADCRESSEL1 register. Write to the ADCRESSEL1.ADCSEL field to select the ADC instance to test, and write to the ADCRESSEL1.ADCRESULTSEL field to select the corresponding SOC conversion result from that ADC to compare. 

3. Select the second result to compare by writing to the ADC_SAFECHECK_REGSn.ADCRESSEL2 register. Write to ADCRESSEL2.ADCSEL to select the ADC instance to test, and write to ADCRESSEL2.ADCRESULTSEL to select the SOC conversion result from that ADC to compare. Any one of the SOC results, PPB module results or PPB sums can be selected in the ADCRESULTSEL field. 

4. Configure the checker tolerance by writing to the ADC_SAFECHECK_REGSn.TOLERANCE register. The safety check result is out of tolerance if the difference between the two conversion results exceeds the value configured in TOLERANCE. 

5. Enable the checker tile by writing 1 to ADC_SAFECHECK_REGSn.CHECKCONFIG.CHKEN. 

6. Optionally, write 1 to ADC_SAFECHECK_REGSn.CHECKCONFIG.SWSYNC to force a reset of any currently set result safety checker event flags. 

Each of the two result selectors waits for the configured ADC result to become available on the bus. When an ADC result becomes available, the checker reads the result into the CHECKRESULTx register, and sets the CHECKSTATUS.RESxRDY flag. Once both results are available, the checker clears the RESxRDY flags, compares the two results against each other, and sets the CHECKSTATUS.OOT flag if the configured tolerance is exceeded. This flag is also reflected in the corresponding bit for the selected checker tile in the OOTFLG register, and can be cleared by writing 1 to the corresponding bit in the OOTFLGCLR register. The checker does not perform any new comparisons while the OOT flag is set; to enable new comparisons, the flag must be cleared. 

If two conversion results arrive in one selector before the other selector result becomes available, the checker sets the RESxOVF flag. This overflow flag does not prevent the comparison from occurring—the flag is for information only. To clear the overflow flag, write 1 to the corresponding bit for the selected checker tile in the RESxOVFCLR register. 

## _**7.5.2.15.2 Result Safety Checker Interrupts and Events**_ 

Each ADC result safety checker tile can generate an interrupt signal from out-of-tolerance (OOT) flags and result overflow flags (RESxOVF). These events are aggregated into a single interrupt signal, CHECKINT. Figure 7-126 shows a block diagram of the result checker interrupt aggregation. To enable a checker flag as a source for CHECKINT, write 1 to the corresponding bit in the CHECKINTSEL1, CHECKINTSEL2 or CHECKINTSEL3 register. To clear a previously set checker interrupt flag, write 1 to the CHECKINTFLGCLR.CHECKINTCLR register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

557 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 456] intentionally omitted <==**

**----- Start of picture text -----**<br>
ADC Results Checker<br>INT and EVT Aggregation<br>CHK1.OOT SET ADC Checker INT Selection<br>OOTFLG.OOT1<br>OOTFLGCLR.OOT1 CLR CHECKINTSEL3.OOT1EN<br>CHK2.OOT SET<br>OOTFLG.OOT2<br>OOTFLGCLR.OOT2 CLR CHECKINTSEL3.OOT2EN<br>0SET ADCCHECKINT<br>CHECKINT<br>CLR<br>CHKn.OOT SET CHECKINTFLGCLR.CHECKINTCLR Low pulse<br>OOTFLG.OOTn output<br>OOTFLGCLR.OOTn CLR CHECKINTSEL3.OOTnEN Generates an interrupt pulse when an<br>enabled OOT or OVF event occurs.  No<br>further interrupt pulses will be<br>generated until the interrupt flag is<br>cleared.<br>CHK1.RES1OVF SET<br>RES1OVF1<br>RES1OVFCLR.RES1OVF1 CLR CHECKINTSEL1.RES1OVF1EN<br>CHK2.RES1OVF SET<br>RES1OVF2<br>RES1OVFCLR.RES1OVF2 CLR CHECKINTSEL1.RES1OVF2EN<br>CHKn.RES2OVF SET<br>RES2OVFn<br>RES2OVFCLR.RES2OVFn CLR CHECKINTSEL1.RES2OVFnEN<br>CHK1.RES2OVF SET<br>RES2OVF1<br>RES2OVFCLR.RES2OVF1 CLR CHECKINTSEL2.RES2OVF1EN<br>CHK2.RES2OVF SET<br>RES2OVF2<br>RES2OVFCLR.RES2OVF2 CLR CHECKINTSEL2.RES2OVF2EN<br>CHKn.RES2OVF SET<br>RES2OVFn<br>RES2OVFCLR.RES2OVFn CLR CHECKINTSEL2.RES2OVFnEN<br>**----- End of picture text -----**<br>


**Figure 7-126. ADC Result Checker Interrupt Aggregation** 

In addition, safety checker tiles can also generate events that can be sent to the X-BAR, so that automatic hardware actions such as an ePWM trip can be generated. This device has 4 checker event signals (CHECKEVTx) that can be generated. For each event signal, any number of checker tile OOT or OVF flags can be aggregated into the single event signal. Figure 7-127 shows a block diagram of the ADC result checker event aggregation. To enable a checker flag as a source for a CHECKEVT signal, write 1 to the corresponding bit in the CHECKEVTxSEL1, CHECKEVTxSEL2 or CHECKEVTxSEL3 registers. 

558 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [500 x 511] intentionally omitted <==**

**----- Start of picture text -----**<br>
ADC Results Checker<br>INT and EVT Aggregation<br>CHK1.OOT ADC Checker EVT1 Selection<br>SET<br>OOTFLG.OOT1<br>OOTFLGCLR.OOT1 CLR CHECKEVTSEL3.OOT1EN<br>CHK2.OOT<br>SET<br>OOTFLG.OOT2<br>OOTFLGCLR.OOT2 CLR CHECKEVTSEL3.OOT2EN CHECKEVT1<br>CHECKEVT2<br>CHECKEVT3<br>CHECKEVT4<br>CHKn.OOT<br>SET<br>OOTFLG.OOTn<br>OOTFLGCLR.OOTn CLR CHECKEVTSEL3.OOTnEN<br>CHK1.RES1OVF<br>SET<br>RES1OVF1<br>RES1OVFCLR.RES1OVF1 CLR CHECKEVTSEL1.RES1OVF1EN<br>CHK2.RES1OVF<br>SET<br>RES1OVF2<br>RES1OVFCLR.RES1OVF2 CLR CHECKEVTSEL1.RES1OVF2EN<br>CHKn.RES2OVF<br>SET<br>RES2OVFn<br>RES2OVFCLR.RES2OVFn CLR CHECKEVTSEL1.RES2OVFnEN<br>CHK1.RES2OVF<br>SET<br>RES2OVF1<br>RES2OVFCLR.RES2OVF1 CLR CHECKEVTSEL2.RES2OVF1EN<br>CHK2.RES2OVF<br>SET<br>RES2OVF2<br>RES2OVFCLR.RES2OVF2 CLR CHECKEVTSEL2.RES2OVF2EN<br>CHKn.RES2OVF<br>SET<br>RES2OVFn<br>RES2OVFCLR.RES2OVFn CLR CHECKEVTSEL2.RES2OVFnEN<br>**----- End of picture text -----**<br>


**Figure 7-127. ADC Result Checker Event Aggregation** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 559 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.2.16 Opens/Shorts Detection Circuit (OSDETECT)** 

The opens/shorts detection circuit (OSDETECT) can be used to detect pin faults in the system. The circuit connects to the ADC input after the channel select multiplexer but before the S+H circuit as shown in Figure 7-128. 

## **Note** 

- The divider resistance tolerances can vary widely; hence, this feature must not be used to check for conversion accuracy. 

- See the data sheet for implementation and availability of analog input channels. 

- Due to high drive impedance, a S+H duration much longer than the ADC minimum is needed (approximately 3 times longer for reference). 

**==> picture [268 x 210] intentionally omitted <==**

**----- Start of picture text -----**<br>
Opens/Shorts Detection Circuit<br>VDDA VSSA<br>CHSEL<br>S2 S1<br>ADCIN0 0<br>ADCIN1 1<br>ADCIN2 2 5 kW<br>ADCIN3 3<br>ADCIN4 4 To S+H<br>7 kW<br>ADCINx x<br>S3 S4<br>VDDA VSSA<br>**----- End of picture text -----**<br>


**Figure 7-128. Opens/Shorts Detection Circuit** 

The circuit can be operated by writing a value to the DETECTCFG field in the ADCOSDETECT register. This causes the circuit to source a voltage onto the input during the S+H phase of any conversion. The voltage and drive strength of the OSDETECT circuit for different DETECTCFG settings is given in . 

**Table 7-119. TOP_CTRL ADC OSD Control Settings** 

|**TOP_CTRL.**<br>**ADCx_OSD_CHEN**|**TOP_CTRL.**<br>**ADCx_OSD_CTRL**|**Function**|**Drive Impedance**|**5K Voltage**|**7K Voltage**|
|---|---|---|---|---|---|
|0|0|Off|Open|Open|Open|
|1|0|Zero Scale|5K || 7K|GND|GND|
|1|1|Zero Scale|5K|GND|Open|
|1|2|Zero Scale|7K|Open|GND|
|1|3|Full Scale|5K || 7K|3.3V VDD|3.3V VDD|
|1|4|Full Scale|5K|3.3V VDD|Open|
|1|5|Full Scale|7K|Open|3.3V VDD|
|1|6|5/12 Scale|5K || 7K|GND|3.3V VDD|
|1|7|7/12 Scale|5K || 7K|3.3V VDD|GND|



560 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-120. TOP_CTRL ADC_R OSD Control Settings** 

|**TOP_CTRL.**<br>**adc5adc6_OSD_CTRL**|**Function**|**Drive Impedance**|**5K Voltage**|**7K Voltage**|
|---|---|---|---|---|
|0|Zero Scale|5K || 7K|GND|GND|
|1|Zero Scale|5K|GND|Open|
|2|Zero Scale|7K|Open|GND|
|3|Full Scale|5K || 7K|3.3V VDD|3.3V VDD|
|4|Full Scale|5K|3.3V VDD|Open|
|5|Full Scale|7K|Open|3.3V VDD|
|6|5/12 Scale|5K || 7K|GND|3.3V VDD|
|7|7/12 Scale|5K || 7K|3.3V VDD|GND|



**Table 7-121. Channel Enable Control for ADC_R[0:1]** 

|**adc5adc6_osd_ctrl_1p1v[7:0] (Channel Enable)**|**adc5adc6_osd_ctrl_1p1v[7:0] (Channel Enable)**|**adc5adc6_osd_ctrl_1p1v[7:0] (Channel Enable)**|**adc5adc6_osd_ctrl_1p1v[7:0] (Channel Enable)**|**adc5adc6_osd_ctrl_1p1v[7:0] (Channel Enable)**|**adc5adc6_osd_ctrl_1p1v[7:0] (Channel Enable)**|**adc5adc6_osd_ctrl_1p1v[7:0] (Channel Enable)**|**adc5adc6_osd_ctrl_1p1v[7:0] (Channel Enable)**|
|---|---|---|---|---|---|---|---|
|Bit 0|Bit 1|Bit 2|Bit 3|Bit 4|Bit 5|Bit 6|Bit 7|
|ADC_R0_CH3|ADC_R0_CH2|ADC_R0_CH1|ADC_R0_CH0|ADC_R1_CH0|ADC_R1_CH1|ADC_R1_CH2|ADC_R1_CH3|
|Enabled if 1|Enabled if 1|Enabled if 1|Enabled if 1|Enabled if 1|Enabled if 1|Enabled if 1|Enabled if 1|



## _**7.5.2.16.1 Implementation**_ 

A representative circuit with the OSDETECT implementation consists of the signal source with series resistance RS, shunt capacitor CP, the equivalent OSDETECT resistance ROSDETECT and voltage VOSDETECT is shown in Figure 7-129 and can be used as a basis to calculate the signal level going in to the sampling capacitor. ROSDETECT and VOSDETECT are the equivalent input resistance and voltage source contributed by the OSDETECT circuit with values shown in DETECTCFG Settings for the different configuration settings. Refer to Figure 7-129 when deriving the input signal to S/H if signal source VS is driving while the OSDETECT feature is enabled. 

**==> picture [159 x 99] intentionally omitted <==**

**----- Start of picture text -----**<br>
RS ADCINx<br>TO S/H<br>ROSDETECT<br>VS CP<br>VOSDETECT<br>**----- End of picture text -----**<br>


**Figure 7-129. Input Circuit Equivalent with OSDETECT Enabled** 

The input impedance RS and CP are integral parts of the signal source or can have been implemented in the design to precondition the signal or to control signal settling time to meet S/H requirements. The input path has to be considered when using the OSDETECT feature, as this affects the conversion results. For instance, driving an input signal when this feature is enabled connects signal VS to the OSDETECT circuit through RS and affects the ADC results. Larger CP values (in the order greater than hundreds of pF) require using higher ACQPS to make sure the signal at the input has settled prior to conversion. 

To enable the circuit: 

1. Configure the ADC for conversion (for example, channel, SOC, ACQPS, prescaler, trigger, and so on). 

2. Set up the ADCOSDETECT register for the desired voltage divider connection as shown in DETECTCFG Settings. 

3. Initiate a conversion and inspect the conversion result. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 561 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

Interpret the results based on what is driving on the input side and what are the values of RS and CP. If the VS signal can be disconnected from the input pin, the circuit can be used to detect open and shorted input pins as described in the following sections. 

## _**7.5.2.16.2 Detecting an Open Input Pin**_ 

By cycling through the various OSDETECT settings, the input signal is pulled towards the sourced voltages. An input with good drive strength (pin not open) is minimally affected. However, if the pin is open, the sampled voltages is close to the source voltages specified in DETECTCFG Settings. 

## _**7.5.2.16.3 Detecting a Shorted Input Pin**_ 

By cycling through the various OSDETECT settings, the input signal is pulled towards the sourced voltages. An input with finite drive strength (pin not shorted) is pulled toward each sourced voltage. However, if the pin is shorted, the signal remains at the same voltage. 

## _**7.5.2.16.4 ADC OSD Programming Guide**_ 

## **ADC OSD Software API Information** 

The ADC drivers provide an API to configure the ADC OSD module. 

See ADC_configOSDetectMode 

## **Example Usage** 

The below link shows an example on how to use the ADC OSD function: 

ADC Open Shorts Detection 

562 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.2.17 Power-Up Sequence** 

Upon device power-up or system level reset, the ADC is powered down and disabled. When powering up the ADC, the following sequence must be used: 

1. SYSCLK is used to generate the ADCCLK/acquisition window. 

2. Set the desired ADC clock divider in the PRESCALE field of ADCCTL2. Note that ADCCLK must be divided down to meet the maximum ADCCLK frequency provided in the device data sheet. 

3. Power up the ADC by setting the ADCPWDNZ bit in ADCCTL1. 

4. Allow a delay before sampling. See the data sheet for the necessary time. 

If multiple ADCs are powered up simultaneously, steps 1 and step 3 can each be done for all ADCs in one write instruction. Also, only one delay is necessary as long as the delay occurs after all the ADCs have begun powering up. 

## **7.5.2.18 ADC Calibration** 

During the fabrication and test process, Texas Instruments calibrates the gain, offset, and linearity of the ADCs. These trim settings are stored in TI reserved OTP memory. 

- Calibration information is stored in TOP_CTRL registers and copied to ADC registers ADCINLTRIM1-6 (offsets 0xE0-0xF4) during power up. 

## _**7.5.2.18.1 ADC Zero Offset Calibration**_ 

ADC offset error is determined and calibrated during factory testing. However, the user still has the option to perform offset calibration if the end application specifically requires this. This section describes how to perform offset calibration using internal VREFLO connection for single-ended operation. 

Zero offset error is defined as the difference from 0 that occurs when converting a voltage at VREFLO. The zero offset error can be positive or negative. To correct this error, an adjustment of equal magnitude and opposite polarity is written into the ADCOFFTRIMx register. The value contained in this register is applied before the results are available in the ADC result registers. This operation is fully contained within the ADC core, so the timing of the results is not affected, and the full dynamic range of the ADC is maintained for any trim value. 

## **Note** 

Regardless of the converter resolution, the size of each ADCOFFTRIMx step is (VREFHI-VREFLO)/ 65536. 

Use the following procedure to re-calibrate the ADC offset in 12-bit single-ended mode: 

1. Set ADCOFFTRIMx to +112 steps (0x70). This adds an artificial offset to account for negative offset that can reside in the ADC core. 

2. Perform some multiple of 16 conversions on VREFLO (internal connection), accumulating the results (for example, 32 ˟ 16 conversions = 512 conversions). Use the maximum value of ACQPS to make sure longer settling time to account for parasitic impedance of internal VREFLO connections. 

3. Divide the accumulated result by the multiple of 16 (for example, for 512 conversions, divide by 32). 

4. Set ADCOFFTRIMx to 112 – result from step 3. 

## **7.5.2.19 ADC Timings** 

The process of converting an analog voltage to a digital value is broken down into an S+H phase and a conversion phase. The ADC sample and hold circuits (S+H) are clocked by SYSCLK while the ADC conversion process is clocked by ADCCLK. ADCCLK is generated by dividing down SYSCLK based on the PRESCALE field in the ADCCTL2 register. 

The S+H duration is the value of the ACQPS field of the SOC being converted, plus one, times the SYSCLK period. The user must make sure that this duration exceeds both 1 ADCCLK period and the minimum S+H duration specified in the data sheet. The conversion time is approximately 10.5 ADCCLK cycles. See the timing diagrams and tables in Section 7.5.2.19.1 for exact timings. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 563 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.2.19.1 ADC Timing Diagrams**_ 

The following diagrams show the ADC conversion timings for two SOCs given the following assumptions: 

- SOC0 and SOC1 are configured to use the same trigger. 

- No other SOCs are converting or pending when the trigger occurs. 

- The round robin pointer is in a state that causes SOC0 to convert first. 

- ADCINTSEL is configured to set an ADCINT flag upon end of conversion for SOC0 (whether this flag propagates through to the CPU to cause an interrupt is determined by the configurations in the VIM module). 

## **Table 7-122. ADC Timing Parameter Descriptions** 

|**Parameter**|**Description**|
|---|---|
|tSH|The duration of the S+H window.<br>At the end of this window, the value on the S+H capacitor becomes the voltage to be converted into a digital value. The<br>duration is given by (ACQPS + 1) SYSCLK cycles. ACQPS can be configured individually for each SOC, so tSHis not<br>necessarily the same for different SOCs.<br>**Note:**The value on the S+H capacitor is captured approximately 5ns before the end of the S+H window regardless of<br>device clock settings.|
|tLAT|The time from the end of the S+H window until the ADC results latch in the ADCRESULTx register.<br>If the ADCRESULTx register is read before this time, the previous conversion results are returned.|
|tEOC|The time from the end of the S+H window until the S+H window for the next ADC conversion can begin. The<br>subsequent sample can start before the conversion results are latched.|
|tINT|The time from the end of the S+H window until an ADCINT flag is set (if configured).<br>If the INTPULSEPOS bit in the ADCCTL1 register is set, tINTcoincides with the end of conversion (EOC) signal.<br>If the INTPULSEPOS bit is 0, and the OFFSET field in the ADCINTCYCLE register is not 0, then there is a delay of<br>OFFSET SYSCLK cycles before the ADCINT flag is set. This delay can be used to enter the ISR or trigger the DMA<br>exactly when the sample is ready.<br>If the INTPULSEPOS bit is 0, tINTcoincides with the end of the S+H window. If tINTtriggers a read of the ADC result<br>register (directly through DMA or indirectly by triggering an ISR that reads the result), care must be taken to make sure<br>the read occurs after the results latch (otherwise, the previous results are read).|
|tDMA|The time from the end of the S+H window until a DMA read of the ADC conversion result is triggered, when<br>ADCCTL1.TDMAEN = 1.<br>If TDMAEN is set to 0, then the DMA trigger occurs at TINT. In certain conditions, the ADCINT flag can be set before<br>the ADCRESULT value is latched. To make sure that the DMA read occurs after the ADCRESULT value has been<br>latched, write 1 to ADCCTL1.TDMAEN to enable DMA timings.|



564 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [444 x 329] intentionally omitted <==**

**----- Start of picture text -----**<br>
Sample n<br>Input on SOC0.CHSEL<br>Input on SOC1.CHSEL<br>Sample n+1<br>ADC S+H SOC0 SOC1<br>SYSCLK<br>ADCCLK<br>ADCTRIG<br>ADCSOCFLG.SOC0<br>ADCSOCFLG.SOC1<br>ADCRESULT0 (old data) Sample n<br>ADCRESULT1 (old data) Sample n+1<br>ADCINTFLG.ADCINTx<br>tSH tLAT<br>tEOC<br>tINT<br>**----- End of picture text -----**<br>


**Figure 7-130. ADC Timings for 12-bit Mode in Early Interrupt Mode** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 565 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 381] intentionally omitted <==**

**----- Start of picture text -----**<br>
Sample n<br>Input on SOC0.CHSEL<br>Input on SOC1.CHSEL<br>Sample n+1<br>ADC S+H SOC0 SOC1<br>SYSCLK<br>ADCCLK<br>ADCTRIG<br>ADCSOCFLG.SOC0<br>ADCSOCFLG.SOC1<br>ADCRESULT0 (old data) Sample n<br>ADCRESULT1 (old data) Sample n+1<br>ADCINTFLG.ADCINTx<br>tSH tLAT<br>tEOC<br>tINT<br>**----- End of picture text -----**<br>


**Figure 7-131. ADC Timings for 12-bit Mode in Late Interrupt Mode** 

**Table 7-123. ADC Timings in 12-bit Mode** 

|**ADCCLK Prescale**|**ADCCLK Prescale**|**SYSCLK Cycles**|**SYSCLK Cycles**|**SYSCLK Cycles**|**SYSCLK Cycles**|
|---|---|---|---|---|---|
|**ADCCTL2.**<br>**PRESCALE**|**Prescale Ratio**|**tEOC**|**tLAT**|**tEINT(Early)**|**tLINT(Late)**|
|0|1|11|13|1|11|
|1|1.5|16|18|1|16|
|2|2|21|23|1|21|
|3|2.5|26|38|1|26|
|4|3|31|34|1|31|
|5|3.5|36|39|1|36|
|6|4|41|44|1|41|
|7|4.5|46|49|1|46|
|8|5|51|55|1|51|
|9|5.5|56|60|1|56|
|10|6|61|65|1|61|
|11|6.5|66|70|1|66|



566 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-123. ADC Timings in 12-bit Mode (continued)** 

|**ADCCLK Prescale**|**ADCCLK Prescale**|**SYSCLK Cycles**|**SYSCLK Cycles**|**SYSCLK Cycles**|**SYSCLK Cycles**|
|---|---|---|---|---|---|
|**ADCCTL2.**<br>**PRESCALE**|**Prescale Ratio**|**tEOC**|**tLAT**|**tEINT(Early)**|**tLINT(Late)**|
|12|7|71|76|1|71|
|13|7.5|76|81|1|76|
|14|8|81|86|1|81|
|15|8.5|86|91|1|86|



## **Note** 

By default, tEINT occurs one SYSCLK cycle after the S+H window, if INTPULSEPOS is 0. This can be changed by writing to the OFFSET field in the ADCINTCYCLE register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 567 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.2.20 Additional Information** 

The following sections contain additional practical information. 

## _**7.5.2.20.1 Ensuring Synchronous Operation**_ 

For best performance, all ADCs on the device must be operated synchronously. The device data sheet specifies the performance in both synchronous and asynchronous mode for those parameters which differ between the modes of operation. 

To make sure of synchronous operation, all ADCs on the device must operate in lockstep. This is accomplished by writing configurations to all ADCs that cause the sampling and conversion phases of all ADCs to be exactly aligned. The easiest way to accomplish this is to write identical values to the SOC configurations for each ADC for trigger select and ACQPS (S+H duration). In addition, synchronous ADCs must also configure identical values for the SOC priority control, burst mode, burst trigger, and burst size. 

On some products, ADC types can be combined on the device for versatility. Synchronous operation can be restricted when operating different ADC types simultaneously. Consult the device data sheet, if there are restrictions on simultaneous operation of ADCs of different types to understand if ADC performance is impacted. 

## _**7.5.2.20.1.1 Basic Synchronous Operation**_ 

The following example configures two SOCs each on ADCA and ADCB with identical trigger select and ACQPS values. This results in synchronous operation between ADCA and ADCB. For devices with more than two ADCs, the same principles can be used to synchronize all the ADCs. 

## **Note** 

In the diagram below: 

- ADCA and ADCB can be any two ADC[0:x] 

- CPU Timer can be any RTI[0:x] 

- ePWM3 SOCB can be any EPWM[0:x]_SOCB 

ePWM3B Trigger ADC A SOC0 - S+H SOC0 - Conversion SOC1 - S+H SOC1 - Conversion ADC B SOC0 - S+H SOC0 - Conversion SOC1 - S+H SOC1 - Conversion 

## **Figure 7-132. Example: Basic Synchronous Operation** 

Several things can be noted from Figure 7-132. First, while the ACQPS values must be the same for SOCs with the same number, different ACQPS values can be used for SOCs with different numbers. Because of this, synchronous operation does not require a single global S+H time, but instead only channels sampled simultaneously require identical S+H durations. Another important point from this example is that any channel select value can be used for any SOC. Finally, this example assumes round-robin operation. If high-priority SOCs are to be used, the priority must be configured the same on all ADCs. 

568 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.2.20.1.2 Synchronous Operation with Multiple Trigger Sources**_ 

As long as each set of SOCs has identical trigger select and ACQPS settings, multiple trigger sources can be used while still achieving synchronous operation. 

The following example demonstrates synchronous operation between ADCA and ADCB while using three SOCs and two trigger sources. Figure 7-133 demonstrates that any combination of relative trigger timings still results in synchronous operation. 

## **Note** 

## In the diagram below: 

- ADCA and ADCB can be any two ADC[0:x] 

- CPU Timer can be any RTI[0:x] 

- ePWM3 SOCB can be any EPWM[0:x]_SOCB 

**==> picture [346 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
ePWM3B CPU1 Timer 1<br>Trigger Trigger<br>ADC A  SOC0 - S+H SOC0 - Conversion SOC1 - S+H SOC1 - Conversion SOC2 - S+H SOC2 - Conversion<br>ADC B SOC0 - S+H SOC0 - Conversion SOC1 - S+H SOC1 - Conversion SOC2 - S+H SOC2 - Conversion<br>ePWM3B CPU1 Timer 1<br>Trigger Trigger<br>ADC A  SOC0 - S+H SOC0 - Conversion SOC1 - S+H SOC1 - Conversion SOC2 - S+H SOC2 - Conversion<br>ADC B SOC0 - S+H SOC0 - Conversion SOC1 - S+H SOC1 - Conversion SOC2 - S+H SOC2 - Conversion<br>CPU1 Timer 1  ePWM3B<br>Trigger Trigger<br>ADC A  SOC2 - S+H SOC2 - Conversion SOC0 - S+H SOC0 - Conversion SOC1 - S+H SOC1 - Conversion<br>ADC B SOC2 - S+H SOC2 - Conversion SOC0 - S+H SOC0 - Conversion SOC1 - S+H SOC1 - Conversion<br>**----- End of picture text -----**<br>


**Figure 7-133. Example: Synchronous Operation with Multiple Trigger Sources** 

Note that any trigger source that can be selected in the TRIGSEL field can be used except for software triggering. There is no way to issue the software triggers for all ADCs simultaneously, so this results in asynchronous operation. ADCINT1 or ADCINT2 can also be used as a trigger when the ADCINTSOCSEL1 and ADCINTSOCSEL2 registers are configured identically for all ADCs and software triggering is not used to start the chain of conversions. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

569 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.2.20.1.3 Synchronous Operation with Uneven SOC Numbers**_ 

If only one trigger source is used, one ADC can use more SOCs than the other ADCs while still operating synchronously. 

## **Note** 

In the diagrams below: 

- ADCA and ADCB can be any two ADC[0:x] 

- CPU Timer can be any RTI[0:x] 

- ePWM3 SOCB can be any EPWM[0:x]_SOCB 

**==> picture [334 x 79] intentionally omitted <==**

**----- Start of picture text -----**<br>
ePWM3B<br>Trigger<br>ADC A  SOC0 - S+H SOC0 - Conversion SOC1 - S+H SOC1 - Conversion SOC2 - S+H SOC2 - Conversion<br>ADC B SOC0 - S+H SOC0 - Conversion SOC1 - S+H SOC1 - Conversion<br>**----- End of picture text -----**<br>


## **Figure 7-134. Example: Synchronous Operation with Uneven SOC Numbers** 

Note that if the trigger comes again before all SOCs have completed the conversions, ADCB begins converting immediately on SOC0 while ADCA does not start converting SOC0 again until SOC2 is complete. This results in asynchronous operation, so care must be taken to not overflow the trigger. 

|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|ADC A<br>ADC B<br>ePWM3B<br>Trigger<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC2 - S+H<br>SOC2 - Conversion<br>SOC0 - S+H<br>SOC0 - Conversion<br>SOC1 - S+H<br>SOC1 - Conversion<br>SOC0 - S+H<br>...|||||||||||
|||SOC0 - S+H|SOC0 - Conversion|SOC1 - S+H|SOC1 - Conversion|SOC2 - S+H||SOC2 - Conversion||SOC0 - S+H|...||
||||||||||||||
|||SOC0 - S+H|SOC0 - Conversion|SOC1 - S+H|SOC1 - Conversion|SOC0 - S+H|SOC0 - Conversion||SOC1 - S+H||SOC1 - Conversion||
||||||||||||||
||||||||||||||



**Figure 7-135. Example: Asynchronous Operation with Uneven SOC Numbers – Trigger Overflow** 

570 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.2.20.1.4 Non-overlapping Conversions**_ 

If conversion timings can be made sure to not overlap by the user, then all the SOCs on all ADCs do not have to be identically configured to achieve performance equivalent to synchronous operation. For example, if the two ADC triggers in a system come from two ePWM sources that are always 180-degrees out-of-phase, then SOC0 can be used for both ADCA and ADCB with different trigger sources and different ACQPS values. 

## **Note** 

In the diagram below: 

- ADCA and ADCB can be any two ADC[0:x] 

- CPU Timer can be any RTI[0:x] 

- ePWM3 SOCA can be any EPWM[0:x]_SOCA 

- ePWM3 SOCB can be any EPWM[0:x]_SOCB 

**==> picture [466 x 79] intentionally omitted <==**

**----- Start of picture text -----**<br>
ePWM3B ePWM3A ePWM3B ePWM3A<br>Trigger Trigger Trigger Trigger<br>ADC A  SOC0 - S+H SOC0 - Conversion SOC0 - S+H SOC0 - Conversion<br>ADC B SOC0 - S+H SOC0 - Conversion SOC0 - S+H SOC0 - Conversion<br>**----- End of picture text -----**<br>


**Figure 7-136. Example: Synchronous Equivalent Operation with Non-Overlapping Conversions** 

## _**7.5.2.20.2 Choosing an Acquisition Window Duration**_ 

For correct operation, the input signal to the ADC must be allowed adequate time to charge the sample and hold capacitor, Ch. Typically, the S+H duration is chosen such that the sampling capacitor is charged to within ½ LSB or ¼ LSB of the final value, depending on the tolerable settling error. 

The best methodology to determine the required settling time is to simulate the ADC and ADC driving circuits to make sure adequate settling performance. See _ADC Input Circuit Evaluation for C2000 MCUs_ and _ChargeSharing Driving Circuits for C2000 ADCs_ for additional guidance on ADC signal conditioning circuit design and evaluation. 

An approximation of the required settling time can also be determined using an RC settling model. The time constant for the model is given by the equation: 

**==> picture [446 x 16] intentionally omitted <==**

And the number of time constants needed is given by the equation: 

**==> picture [461 x 36] intentionally omitted <==**

So the total S+H time must be set to at least: 

**==> picture [464 x 11] intentionally omitted <==**

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 571 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

Where the following parameters are provided by the ADC input model in the device data sheet: 

- n = ADC resolution (in bits) 

- RON = ADC sampling switch resistance (provided in Ω) 

- CH = ADC sampling capacitor (provided in pF) 

- Cp = ADC channel parasitic input capacitance (provided in pF) 

And the following parameters are dependent on the application design: 

- settling error = tolerable settling error (in LSBs) 

- Rs = ADC driving circuit source impedance (typically in Ω or kΩ) 

- CS = capacitance on ADC input pin (typically in pF or nF) 

For example, assuming the following parameters: 

- n = 12-bits 

- RON = 500Ω 

- CH = 12.5pF 

- Cp = 12.7pF 

- settling error = ¼ LSB 

- Rs = 180Ω 

- Cs = 150pF 

The time constant is calculated as: 

**==> picture [266 x 10] intentionally omitted <==**

**==> picture [13 x 10] intentionally omitted <==**

And the number of required time constants is: 

**==> picture [464 x 33] intentionally omitted <==**

So the S+H time must be set to at least: 37.8ns ˟ 7.13 = 270ns 

If SYSCLK = , then each SYSCLK cycle is . S+H duration is 270ns/ = SYSCLK cycles, so ACQPS for this input is set to at least CEILING() – 1 = . 

While this gives a rough estimate of the required acquisition window, a better method is to setup a circuit with the ADC input model, a model of the source impedance/capacitance, and any board parasitics in SPICE (or similar software) and simulate to verify that the sampling capacitor settles to the desired accuracy. 

## **Note** 

The device data sheet specifies a minimum ADC S+H window duration. Do not use an ACQPS value that gives a duration less than this specification. 

572 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.2.20.3 Achieving Simultaneous Sampling**_ 

While each ADC does not have dual S+H circuits, achieving simultaneous sampling is accomplished by setting the SOC triggers on two or more ADC modules to use the same trigger source. The following example demonstrates simultaneous sampling on ADCs based on an ePWM3 event. are sampled. An acquisition window of 20 SYSCLK cycles is used, but different durations are possible. 

When the ePWM3 trigger is received, all ADCs begin converting in parallel immediately. All results are stored in the ADCRESULT0 register for each ADC. Note that this assumes that all ADCs are idle when the trigger is received. If one or more ADCs is busy, the samples do not happen at exactly the same time. 

## _**7.5.2.20.4 Result Register Mapping**_ 

The ADC results and the ADC PPB results are duplicated for each memory bus controller in the system. Bus controllers include all R5FSS core present on the specific part family and part number and DMA TC[0:1]. For each bus controller, no access configuration is needed to allow read access to the result registers and no contention occurs in cases where multiple bus controllers try to read the ADC results simultaneously. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

573 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

574 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.3 Resolver to Digital Converter (RDC)**_ 

**7.5.3.1 Overview** ...................................................................................................................................................... 576 **7.5.3.2 Integration** ....................................................................................................................................................579 **7.5.3.3 Programmer's Guide** ................................................................................................................................... 598 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

575 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.3.1 Overview** 

## _**7.5.3.1.1 Principle of Operation**_ 

A **Resolver** is a type of rotary electrical transformer used for measuring degrees of rotation. The resolver is typically directly mounted to the shaft of an electric motor. A typical resolver consists of a rotary transformer (exciter winding) and two windings separated by 90 degrees on the stator. 

Resolver-front-end systems take a PWM Signal from the Resolver to Digital converter subsystem and generate an excitation sinusoidal signal (typically 7 Vrms) which is applied on the excitation coil. Rotation of the motor modulates the excitation signal and causes a modulated sine and cosine output directly related to the mechanical angle of the rotor with respect to stator. This sine and cosine outputs are monitored on the coupled coils or outputs of the Resolver. Electrical Zero (EZ) of a Resolver is defined as the position of the rotor with respect to the stator at which there is minimum voltage amplitude across the Sine winding and the maximum voltage amplitude across the Cosine winding when the input winding is excited with the rated voltage. 

The Resolver to Digital Converter(RDC) subsystem generates an excitation signal as a Sine modulated PWM signal and that signal interfaces to an external amplifier which extracts the Sine wave and excites the excitation coil of the resolver. The sine and cosine outputs from the coils of the resolver after proper voltage scaling using external amplifiers ,are input to the internal SAR ADCs of the Resolver to Digital converter subsystem. The Resolver to Digital converter subsystem reads the output of the ADCs, processes the incoming digital data, and estimates the angle of the rotor and the angular velocity. It also performs diagnostic checks. 

**==> picture [498 x 242] intentionally omitted <==**

**----- Start of picture text -----**<br>
ADC Control Signals<br>ResolverSin Single or Dual Multiplexer/ DC Offset  Demodulation Phase/Gain  Arctan<br>Cos ADC Sequencer Correction Correction<br>Excitation  Auto  Phase/Gain<br>Excitation<br>PWM and Sample  Error  Track-2<br>Amplifier Signal Time Select Estimation<br>Velocity<br>Engine PWM  Diagnostics<br>Sync<br>Optional DAC  Resolver Hardware<br>Resolver Sin/Cos Analog<br>Diagnostic<br>Monitor<br>SOC<br>External<br>Optional  SOC/<br>ADC or  Software<br>Comparator Diagnostics<br>Diagnostic Block also Controls<br>Redundant Channel Angle Data<br>Single Ended Monitoring of<br>ADC Inputs, and Optional<br>Excitation Monitoring<br>**----- End of picture text -----**<br>


**Figure 7-137. Block Diagram of the Resolver** 

## _**7.5.3.1.2 Supported Features**_ 

- 2x Resolver modules with 12 bit SAR ADCs 

   - 3.125 Msps max sampling rate 

   - 50MHz clock to ADC 

- 2x independent resolvers can be interfaced with one AM263P device, each with track2 and arctan function 

- Software can read either arctan or track2 results for position/speed of each resolver 

- Single ended and Differential modes support 

- Flexible SAR ADC usage modes for sin/cos 

   - 2x SAR ADCs sample one resolver channel: 1x ADC samples sine and 1x ADC samples cosine simultaneously 

576 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

   - 1x SAR ADC samples one resolver channel: sine and cosine are sampled sequentially, then post processed to align the sampling phase. Other ADC can be used for general purpose SOC use 

   - 2x SAR ADCs sample two resolver channels: One ADC samples the sine of one resolver, the other ADC samples the cosine of the same resolver simultenously. Next clock cycle both ADCs sample the sine and cosine signal of the other resolver channel enabling simultaneous sampling of each channel 

- Fault detection and Glitch-filtering 

- Auto offset, gain and phase correction 

- Auto sampling phase optimization and phase delay compensation with track-2 

- Programmable sample point count (to be averaged) at peak 

- Auto PWM phase adjust 

- FIR bandpass filter for improved resolution and offset elimination 

- Bypass oversampling/FIR feature for fast but less accurate tracking with arctan 

- Produce a RES0_PWMOUTx for the generation of one common excitation frequency signal with a pwm_sync_in to enable better EMC immunity 

- Diagnostics signals for failures (if enabled) 

## _**7.5.3.1.3 Safety Features**_ 

- Safety SIL-3 and ASIL-D rating targeted 

- Frequency imbalance: Compare zero crossing of sine with zero crossing of adjacent cosine 

- Phase imbalance: Time delay between zero crossing of sine wrt cosine 

- Gain and Offset mismatch 

- Over and Under voltage sampling of Sine and Cosine Signals 

- Individually programmable mask for all fault signals 

- Programmable tracking error threshold and glitch timer 

- Programmable phase, offset and gain error fault thresholds 

- Redundant channel compare fault detection, (arctan to track-2 comparison or track2 to track2) with programmable threshold and glitch timer 

- Window comparators to monitor analog input faults and excitation signal faults with programmable threshold and glitch settings and report type of input fault: Open, Short, Short to Supply, Short to Gnd 

## **Note** 

Any error condition generates an event if enabled. 

## _**7.5.3.1.4 Performance Specification**_ 

- Sin/cos signal 3.3V, SAR: 12 bits with maximum sampling rate of 2.941176Msps 

- Excitation Frequency selectable at 1KHz, 5KHz, 10KHz, 20KHz. 10 bits / 20Msps for motor max RPM 

- Angle accuracy at ±0.1 degree 

- Resolution linearity (±2 LSB) @13 bits 

- Velocity accuracy (±5 LSB) @16 bits 

- Rate(speed) accuracy (±0.03rps) 

- Maximum 8000 rps with 20KHz Excitation frequency supported, in Mode 0 with one Resolver 

- Conversion time < 5µS (Assuming constant speed) 

- Settling time 1ms 

- Static fault modes to be detected: Open, Short, Cross coupling 

- Dynamic fault modes: Programmable Over Voltage and Under Voltage faults, Phase and Amplitude mismatch faults modes 

## _**7.5.3.1.5 Fault Detection Support**_ 

- Freq imbalance: Compare zero crossing of sine with zero crossing of adjacent cosine 

- Phase imbalance: Time delay between zero crossing of sine with respect to cosine (calibrated) 

- Gain mismatch (calibrated) 

- Offset (calibrated) 

- Over Voltage Fault Detection 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 577 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- Under Voltage Fault Detection 

- Redundancy 

- Individual programmable mask for all fault signals 

- Programmable tracking error threshold and glitch timer 

- Programmable phase, offset and gain error fault thresholds 

- Redundant channel compares fault detection, (arctan to track2 comparison) with programmable threshold and glitch timer 

- Analog input faults with programmable threshold and glitch settings and detection of type of input faults: Open, Short, Short to supply, Short to GND 

- Faults of excitation signal with programmable threshold and glitch settings and detection of type of input faults: Open, Short, Short to supply, Short to GND 

- Excitation Frequency fault detection with respect to frequency for Sine and Cosine signals from Resolver 

578 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.3.2 Integration** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

579 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.3.2.1 Resolver to Digital Convertor Integration**_ 

There are 2x Resolver-to-Digital Converter (RDC) modules integrated in the device as shown in Figure 7-138. 

## **Note** 

## For each RDC Module: 

- Resolver Module input channels have ADC_R0_AIN[3:0] and ADC_R1_AIN[3:0] dedicated pins. 

- ADC_VREFLO_G3 and ADC_VREFHI_G3 are dedicated voltage reference pins for Resolver modules. 

- Refer to Figure 7-139 for full list of all RDC pins. 

**==> picture [500 x 170] intentionally omitted <==**

**----- Start of picture text -----**<br>
Resolver to Digital Convertor Sub-System ANACIO –<br>Analog<br>ADC R0 Communications<br>Input Output<br>Signal Processing – RDC0<br>ControlADC RESADC0.[#1]<br>+ resolver_adc0_mux_en<br>Sequencer<br>PinmuxGPIO/ GPO_PWM[1:0] Excitation signal Signal Processing – RDC1 RESADC1.[#1]<br>ADC R1<br>resolver_adc1_mux_en<br>CFG data<br>PWM MMRs MMRs<br>Sync FE<br>Out PWMSyncOutXBar.Out[2]<br>XBar<br>VBUSP 4.0 32-bit data peripheral<br>[#2]<br>**----- End of picture text -----**<br>


**Figure 7-138. RDC Integration Diagram** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

580 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.3.2.2 Functional Description**_ 

The RDC signal processing uses an analog front end (SAR ADC) and Digital Processing unit called RDC Core. Each RDC Core is identical as shown in Figure 7-139. 

**==> picture [480 x 261] intentionally omitted <==**

**----- Start of picture text -----**<br>
AM263P<br>ADC_VREFHI_G3<br>ADC_VREFLO_G3 Reference Ok<br>ADC_CAL[3:2]<br>RDC Sub-System<br>ADC_R0_AIN0<br>sin +ve<br>ADC_R0_AIN1<br>Resolver 0  Interface  sin -ve   +ve Fault<br>ADC_R0_AIN2 ADC0 RDC Core-0<br>(R0) Circuits cos +ve -ve Detection<br>ADC_R0_AIN3<br>cos -ve<br>Position and<br>Sequencer and  Velocity CPU<br>ADC Controller<br>ADC_R1_AIN0 Configurationvia MMR<br>sin +ve<br>ADC_R1_AIN1<br>Resolver 1  Interface  sin -ve   +ve Fault<br>(R1) Circuits cos +ve ADC_R1_AIN2 -ve ADC1 RDC Core-1 Detection<br>ADC_R1_AIN3<br>cos -ve<br>PR0_PRU1_GPOx<br>Excitation Amplifier 0 RES0_PWMOUTx Excitation Frequency PWM<br>Excitation Amplifier 1<br>Open and Short Detection<br>Mux 2:1<br>Mux 2:1<br>**----- End of picture text -----**<br>


**Figure 7-139. Resolver-RDC System Block Diagram** 

## _**7.5.3.2.2.1 Resolver to Digital Converter(RDC) Sub System**_ 

Resolver to Digital Converter(RDC) in AM263P contains all the signal processing blocks needed to extract the position and velocity using the Sine and Cosine signals generated from an external hardware Resolver. As shown on Figure 7-137and Figure 7-139, there are two identical blocks, termed as RDC Core-0(RDC0) and RDC-Core1(RDC1), on the SOC. 

The following sections explain the different signal processing blocks of this RDC sub-system. 

## _**7.5.3.2.2.1.1 Sequencer and RDC Modes of Operation**_ 

The front end is responsible for latching, demuxing, and optional averaging the sin/cos inputs before it is presented to the RDC modules. 

**Table 7-124. Resolver Sampling Modes** 

|**Mode**|**External Resolvers**<br>**connected**|**ADCs used**|**RDC Cores used**|**Sample Sequence _sX**<br>**indicates Xth sample**|**Note**|
|---|---|---|---|---|---|
|0|Resolver0(R0)|ADCR0 and<br>ADCR1|RDC Core-0|R0sin_ADCR0_s0 +<br>R0cos_ADCR1_s0|Sampling of R0's sin and cos signals<br>concurrently across the ADCR0 and<br>ADCR1. This is the Default mode of<br>operation.|
|1|Resolver0(R0)|ADCR0|RDC Core-0|R0sin_ADCR0_s0 -><br>R0cos_ADCR0_s0|Sampling of R0's sin and cos signals in a<br>staggered manner by ADCR0.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

581 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-124. Resolver Sampling Modes (continued)** 

|**Mode**|**External Resolvers**<br>**connected**|**ADCs used**|**RDC Cores used**|**Sample Sequence _sX**<br>**indicates Xth sample**|**Note**|
|---|---|---|---|---|---|
|2|Resolver0(R0)|ADCR0|RDC Core-0|R0sin_ADCR0_s0 -><br>R0cos_ADCR0_s0 -><br>R0cos_ADCR0_s1 -><br>R0sin_ADCR0_s1 ->|Sampling of R0's sin and cos signals<br>in a staggered manner by ADCR0. The<br>2 samples of sin are averaged and 2<br>samples of cos are averaged.Averaging<br>enabled|
|3|Resolver0(R0) and<br>Resolver1(R1)|ADCR0 and<br>ADCR1|RDC Core-0 and<br>RDC Core-1|R0sin_ADCR0_s0 +<br>R0cos_ADCR1_s0 -><br>R1sin_ADCR0_s0 +<br>R1cos_ADCR1_s0 ->|Sampling of R0's sin and cos signals<br>concurrently across ADCR0 and ADCR1.<br>Followed by the sampling of R1's sin and<br>cos signals concurrently across ADCR0<br>and ADCR1. So, the delay is staggered<br>between the 2 resolvers.|
|4|Resolver0(R0) and<br>Resolver1(R1)|ADCR0 and<br>ADCR1|RDC Core-0 and<br>RDC Core-1|R0sin_ADCR0_s0 +<br>R1sin_ADCR1_s0 -><br>R0cos_ADCR0_s0 +<br>R1cos_ADCR1_s0 ->|Sampling of sin signals of both R0<br>and R1 concurrently across ADCR0 and<br>ADCR1. Followed by the sampling of cos<br>signals of both R0 and R1 concurrently<br>across ADCR0 and ADCR1. So, the<br>delay is staggered between the sin and<br>cos signals.|
|5|Resolver0(R0) and<br>Resolver1(R1)|ADCR0 and<br>ADCR1|RDC Core-0 and<br>RDC Core-1|R0sin_ADCR0_s0 +<br>R1sin_ADCR1_s0 -><br>R0cos_ADCR0_s0 +<br>R1cos_ADCR1_s0 -><br>R0cos_ADCR0_s1 +<br>R1cos_ADCR1_s1 -><br>R0sin_ADCR0_s1 +<br>R1sin_ADCR1_s1 ->|Sampling of sin signals of both R0<br>and R1 concurrently across ADCR0 and<br>ADCR1. Followed by the sampling of cos<br>signals of both R0 and R1 concurrently<br>across ADCR0 and ADCR1. Followed<br>by the sampling of cos signals of both<br>R0 and R1 concurrently across ADCR0<br>and ADCR1. Followed by the sampling<br>of sin signals of both R0 and R1<br>concurrently across ADCR0 and ADCR1.<br>The 2 samples of sin are averaged and<br>2 samples of cos are averaged for the<br>respective Resolvers.Averaging enabled<br>So, the delay is staggered between the<br>sin and cos signals.|



The Resolver modes from above are explained using the below diagrams: 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

582 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.3.2.2.1.1.1 Mode 0**_ 

**==> picture [500 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
AM263P<br>ADC_R0_AIN0<br>sin +ve Sequencer Repeat<br>ADC_R0_AIN1<br>sin -ve   +ve<br>Resolver 0 (R0) ADC_R0_AIN2 ADCR0 ADCR0 Sampled Data RDC Core-0<br>-ve<br>ADC_R0_AIN3<br>ADC_R1_AIN0<br>cos +ve<br>ADC_R1_AIN1<br>cos -ve +ve<br>ADC_R1_AIN2 ADCR1 ADCR1 Sampled Data<br>-ve<br>ADC_R1_AIN3<br>R0sin_ADCR0_s0 Sample 1 -<br>Mux 2:1<br>R0cos_ADCR1_s0 Sample 1 -<br>Mux 2:1<br>**----- End of picture text -----**<br>


**Figure 7-140. Mode -0** 

Resolver to Digital Converter(RDCs) used : RDC Core-0 

## Number of External Resolvers connected : 1 

In Mode 0 as shown in Figure 7-140, the Resolver 0's sin and cos signals are concurrently sampled using ADCR0 and ADCR1. 

## **This is the Default mode of operation.** 

## _**7.5.3.2.2.1.1.2 Mode 1**_ 

**==> picture [500 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
AM263P<br>ADC_R0_AIN0<br>sin +ve Sequencer Repeat<br>ADC_R0_AIN1<br>sin -ve   +ve<br>Resolver 0 (R0) ADC_R0_AIN2 ADCR0 ADCR0 Sampled Data RDC Core-0<br>cos +ve -ve<br>ADC_R0_AIN3<br>cos -ve<br>ADC_R1_AIN0<br>ADC_R1_AIN1<br>ADC_R1_AIN2<br>ADC_R1_AIN3<br>Mux 2:1 R0cos_ADCR0_s0 Sample 2 -  R0sin_ADCR0_s0 Sample 1 -<br>**----- End of picture text -----**<br>


**Figure 7-141. Mode -1** 

Resolver to Digital Converter(RDCs) used : RDC Core-0 

## Number of External Resolvers connected : 1 

In Mode 1 as shown in Figure 7-141, the Resolver 0's sin and cos signals are sampled in a staggered manner using ADCR0. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 583 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.3.2.2.1.1.3 Mode 2**_ 

**==> picture [500 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
AM263P<br>ADC_R0_AIN0<br>sin +ve Sequencer Repeat<br>ADC_R0_AIN1 RDC Core-0<br>sin -ve   +ve<br>Resolver 0 (R0) ADC_R0_AIN2 ADCR0 ADCR0 Sampled Data Averaging Enabled<br>cos +ve -ve Samples 1 and 4 are averaged<br>ADC_R0_AIN3 Samples 2 and 3 are averaged<br>cos -ve<br>ADC_R1_AIN0<br>ADC_R1_AIN1<br>ADC_R1_AIN2<br>ADC_R1_AIN3<br>Mux 2:1 R0sin_ADCR0_s1 Sample 4 -  R0cos_ADCR0_s1 Sample 3 -  R0cos_ADCR0_s0 Sample 2 -  R0sin_ADCR0_s0 Sample 1 -<br>**----- End of picture text -----**<br>


**Figure 7-142. Mode -2** 

Resolver to Digital Converter(RDCs) used : RDC Core-0 

Number of External Resolvers connected : 1 

In Mode 2 as shown in Figure 7-142, the Resolver 0's sin and cos signals are sampled in a staggered manner using ADCR0 similar to Mode-1, but here 2 samples of sin and 2 samples of cos are averaged. 

## **Averaging is enabled.** 

## _**7.5.3.2.2.1.1.4 Mode 3**_ 

**==> picture [500 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
AM263P<br>ADC_R0_AIN0<br>sin +ve Sequencer Repeat<br>ADC_R0_AIN1<br>sin -ve   +ve<br>Resolver 0 (R0) ADC_R0_AIN2 ADCR0 ADCR0 Sampled Data RDC Core-0<br>sin +ve -ve<br>ADC_R0_AIN3<br>sin -ve<br>ADC_R1_AIN0<br>cos +ve Repeat<br>ADC_R1_AIN1<br>cos -ve +ve<br>Resolver 1 (R1) ADC_R1_AIN2 ADCR1 ADCR1 Sampled Data RDC Core-1<br>cos +ve -ve<br>ADC_R1_AIN3<br>cos -ve<br>RDC Core-0 No sample to R0sin_ADCR0_s0 Sample 1 -<br>Mux 2:1<br>RDC Core-0 No sample to R0cos_ADCR1_s0 Sample 1 -<br>R1sin_ADCR0_s0 Sample 1 – RDC Core-1 No sample to<br>Mux 2:1<br>R1cos_ADCR1_s0 Sample 1 – RDC Core-1 No sample to<br>**----- End of picture text -----**<br>


**Figure 7-143. Mode -3** 

Resolver to Digital Converter(RDCs) used : RDC Core-0 and RDC Core-1 

Number of External Resolvers connected : 2 

In Mode 3 as shown in Figure 7-143, 

1. First the Resolver 0's sin and cos signals are concurrently sampled using ADCR0 and ADCR1. 

2. Next, the Resolver 1's sin and cos signals are concurrently sampled using ADCR0 and ADCR1 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

584 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.3.2.2.1.1.5 Mode 4**_ 

**==> picture [500 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
AM263P<br>ADC_R0_AIN0<br>sin +ve Sequencer Repeat<br>ADC_R0_AIN1<br>sin -ve   +ve<br>Resolver 0 (R0) ADC_R0_AIN2 ADCR0 ADCR0 Sampled Data RDC Core-0<br>cos +ve -ve<br>ADC_R0_AIN3<br>cos -ve<br>ADC_R1_AIN0<br>sin +ve Repeat<br>ADC_R1_AIN1<br>sin -ve   +ve<br>Resolver 1 (R1) ADC_R1_AIN2 ADCR1 ADCR1 Sampled Data RDC Core-1<br>cos +ve -ve<br>ADC_R1_AIN3<br>cos -ve<br>Mux 2:1 Sample 2 -  Sample 1 -<br>R0cos_ADCR0_s0 R0sin_ADCR0_s0<br>Sample 2 – Sample 1 –<br>Mux 2:1 R1cos_ADCR1_s0 R1sin_ADCR1_s0<br>**----- End of picture text -----**<br>


**Figure 7-144. Mode -4** 

Resolver to Digital Converter(RDCs) used : RDC Core-0 and RDC Core-1 

Number of External Resolvers connected :2 

In Mode 4 as shown in Figure 7-144, 

1. First sin signals of both Resolver 0 and Resolver 1 are concurrently sampled across ADCR0 and ADCR1. 

2. Next, cos signals of both Resolver 0 and Resolver 1 are concurrently sampled across ADCR0 and ADCR1 

## _**7.5.3.2.2.1.1.6 Mode 5**_ 

**==> picture [500 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
AM263P<br>ADC_R0_AIN0<br>sin +ve Sequencer Repeat<br>ADC_R0_AIN1 RDC Core-0<br>sin -ve   +ve<br>Resolver 0 (R0) ADC_R0_AIN2 ADCR0 ADCR0 Sampled Data Averaging Enabled<br>cos +ve -ve Samples 1 and 4 are averaged<br>ADC_R0_AIN3 Samples 2 and 3 are averaged<br>cos -ve<br>ADC_R1_AIN0<br>sin +ve Repeat<br>ADC_R1_AIN1 RDC Core-1<br>sin -ve   +ve<br>Resolver 1 (R1) ADC_R1_AIN2 ADCR1 ADCR1 Sampled Data Averaging Enabled<br>cos +ve -ve Samples 1 and 4 are averaged<br>ADC_R1_AIN3 Samples 2 and 3 are averaged<br>cos -ve<br>Mux 2:1 R0sin_ADCR0_s1 Sample 4 -  R0cos_ADCR0_s1 Sample 3 -  R0cos_ADCR0_s0 Sample 2 -  R0sin_ADCR0_s0 Sample 1 -<br>Sample 4 – Sample 3 – Sample 2 – Sample 1 –<br>Mux 2:1 R1sin_ADCR1_s1 R1cos_ADCR1_s1 R1cos_ADCR1_s0 R1sin_ADCR1_s0<br>**----- End of picture text -----**<br>


**Figure 7-145. Mode -5** 

Resolver to Digital Converter(RDCs) used : RDC Core-0 and RDC Core-1 

Number of External Resolvers connected : 2 

In Mode 5 as shown in Figure 7-145, 

1. First sin signals of both Resolver 0 and Resolver 1 are concurrently sampled across ADCR0 and ADCR1. 

2. Next, cos signals of both Resolver 0 and Resolver 1 are concurrently sampled across ADCR0 and ADCR1. 

3. Next, cos signals of both Resolver 0 and Resolver 1 are concurrently sampled across ADCR0 and ADCR1. 

4. Next, sin signals of both Resolver 0 and Resolver 1 are concurrently sampled across ADCR0 and ADCR1. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 585 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

5. The 2 samples of sin are averaged and 2 samples of cos are averaged, for the respective Resolvers. 

**Averaging is enabled** , thus the delay is staggered between the sin and cos signals. 

## _**7.5.3.2.2.1.2 Excitation Signal and PWM**_ 

The coil of a Resolver needs an excitation signal which gets modulated as per the shaft rotation. This excitation signal, modulated as per the rotation of the shaft is then output as the sine and cosine outputs of the resolver. 

To generate the excitation signal, the Resolver sub-system in AM263P generates a Sinusoidal PWM signal(RESx_PWMOUTx) where the PWM's duty cycle is modulated as per the Sine excitation signal. This PWM signal needs to be passed through an external low pass filter to obtain the sine excitation signal. Refer Figure 7-147 below, showing ALM2403-Q1 application for example. 

The excitation signal is a sine wave with a programmable frequencies of 1KHz, 5KHz, 10KHz, and 20KHz with programmable phase of 0 to 360°. The Resolver Sub-System outputs this Sinusoidal PWM as RESx_PWMOUTx on Mux Mode 8 of AM263P MCUs ball pins namely, PR0_PRU1_GPIO8, PR0_PRU1_GPIO10, PR0_PRU1_GPIO13, PR0_PRU1_GPIO14. 

## **Note** 

One single excitation signal is generated even if both RDCs are working. It is recommended to use two separate amplifiers driving the excitation signals of two external Resolvers. 

**==> picture [500 x 214] intentionally omitted <==**

**Figure 7-146. Excitation Signal Generation through PWM (Example for 20KHz)** 

586 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [435 x 207] intentionally omitted <==**

**----- Start of picture text -----**<br>
R2<br>C3<br>C1 R1 R3 VOUT1<br>±<br>C2<br>PWM input VBIAS +<br>ALM2403-Q1 channel 1<br>CEMC Sin<br>C4<br>R5 CEMC Cos<br>Resolver<br>VOUT1 R4<br>±<br>VBIAS +<br>ALM2403-Q1 channel 2<br>**----- End of picture text -----**<br>


**Figure 7-147. Filter and Amplifier Circuit Converting the RESx_PWMOUTx Signal to an Analog sine Wave Driving the Resolver Excitation Coil** 

The PWM base frequency must meet the requirements of external excitation amplifier’s second order low pass filter, and must be at least 32 times the maximum supported frequency. Using a 800KHz PWM frequency meets that requirement with it being 40 times the highest excitation frequency of 20KHz. RDC can tolerate a second or third harmonic for the excitation signal up to 10% at the final resolver output. 

The PWM generation circuit is shown below in Figure 7-148. 

**==> picture [500 x 208] intentionally omitted <==**

**Figure 7-148. PWM Generation Circuit** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 587 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [292 x 206] intentionally omitted <==**

**Figure 7-149. PWM Generator Block** 

**==> picture [500 x 215] intentionally omitted <==**

**Figure 7-150. PWM Comparator Output (top), and Output of the Counter and Sine Wave (bottom)** 

The top plot of Figure 7-150 shows the PWM comparator output, and the bottom plot shows the output of the counter and sine wave which are inputs to the pwm comparator. Note the sine wave signal attenuation to avoid clipping. This example shows a 20KHz sine wave generation with 40 pulses per sine wave period. 

For PWM generation, a 250-counter counts from 0 to 249 with 200MHz clock. That generates a periodic sawtooth waveform at 800KHz as shown in Figure 7-150. The overflow counter triggers 8000-counter that counts from 0 to 7999 with steps of EXC_FREQ_SEL(register REGS_EXCIT_SAMPLE_CFG1[7:0]). That counter also generates a sawtooth waveform at 800KHz (in total sync with 250-counter) counting from 0 to 7999. After scaling with * 8.192, this value controls a lookup table of 16 bit sine wave entries. The 16 bit values are multiplied by the gain control EXT_AMP_CNTRL(register REGS_EXCIT_SAMPLE_CFG3[7:0]), then left shifted (divided by 2[16] ), resulting in a 8bit digital sine waveform. If ext_amp_cntrl = 250, then the gain is 1. If it is 225, then gain is = 225/250 = 0.9. Further 125 is added to this signed sine wave, and it goes to a comparator comparing it to the incoming sawtooth waveform generating PWM signals. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

588 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

The RDC over-samples the excitation frequency with a programmable integer number, and based on that, a table is provided for supported excitation frequency and oversample ratio combinations. Note that oversample OSR = ADC_SAMPLE_RATE(register REGS_EXCIT_SAMPLE_CFG1[7:0]) × 2, and effective excitation frequency Fexc = 100 × EXC_FREQ_SEL in Hz. 

This PWM excitation block also supports synchronizing ADCs that sample the motor current with the resolver ADC SOC(start of conversion) signals as shown in Figure 7-151. 

The sync pulse(PWMSYNCOUT_XBAR[2]) coming from the motor-PWM-ADC latches the 8000-counter, which indicates the precise phase information. Note that motor PWM might be an integer multiple of excitation frequency, in this case it may trigger the latch at multiple equal intervals of the counter. The user needs to decide which one to use as the resolver ADC sampling time. By reading PWM_PHASE_INFO(register REGS_EXCIT_SAMPLE_CFG2[12:0]) and programming the SOCPEAK_START value, user can control the phase of the resolver ADC SOC (Start Of Conversion) signal. Also if a phase difference is desired between those signals, it can be easily implemented by offsetting this value. SOCPEAK_START and PWM_PHASE_INFO registers map 0 to 7999 to 0 to 360° × (7999/8000). Ideally the resolver ADC should also sample the sine and cosine coils at the peak of the excitation signal. After the motor PWM ADC and resolver ADC sampling times are synchronized, through the phase control of resolver PWM (EXC_FREQ_PHASE_CFG part of register REGS_EXCIT_SAMPLE_CFG1[28:16]), the excitation signal peak needs to be aligned. This can be achieved by software monitoring the (sin[2] + cos[2] ) signal and shifting the phase until maximum value is achieved, thus compensating for any phase delay on board. 

**==> picture [356 x 315] intentionally omitted <==**

**----- Start of picture text -----**<br>
y y = sinx, x∊ [0,2 � ]<br>1<br>x<br>0 � /2 � 3 � /2 2 �<br>–1<br>8000 Counter<br>socpeak_start<12:0><br>Resolver ADC SOC trigger<br>**----- End of picture text -----**<br>


**Figure 7-151. Resolver ADC Start of Conversion Trigger Phase Adjustment with respect to Excitation Frequency** 

## _**7.5.3.2.2.1.3 Offset Correction**_ 

This Offset Correction block shown in Figure 7-152 calculates and eliminates the DC offset. It runs independently on Sine and Cosine channels. The offset correction can be enabled anytime and the external 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

589 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

resolver shaft need not be spinning. DC average of incoming sine (or cosine) signals are averaged independently (through programmable time constants) and corrected. There is a programmable hysteresis to avoid noise affecting the data. 

The registers associated with Offset Correction are REGS_DC_OFF_CFG1_x, REGS_DC_OFF_CFG2_x and REGS_DC_OFFx. 

**==> picture [318 x 199] intentionally omitted <==**

**Figure 7-152. DC Offset Correction Block Diagram** 

## _**7.5.3.2.2.1.4 Auto Sample Time Select**_ 

The resolver excitation signal gets modulated by the rotation of the motor creating sine and cosine envelopes(sine and cosine modulated Excitation signal). The demodulation happens by sampling the incoming sine and cosine signals at the peaks(as shown in Figure 7-153) of the excitation signal. Since there will be a phase delay along the signal chain, in a real system the peaks can be at any point. So to sample at the peaks, the RDC oversamples the excitation signal and runs an auto-detection loop to decide the ideal sampling time. 

The registers associated with Auto Sample Time select are REGS_SAMPLE_CFG1_x, REGS_SAMPLE_CFG2_x and REGS_DEC_GF_CFGx. 

The RDC block has an auto-detect feature to compensate for the delay in signal chain and find the ideal sample point. Before the software enables IDEAL_SAMPLE_TIME(register REGS_SAMPLE_CFG1_x[23:16]) selection logic, it needs to make sure the excitation frequency from the external amplifier has settled. The threshold value SAMPLE_DET_THRESHOLD(register REGS_SAMPLE_CFG2_x[31:16]) is used to ignore unsettled, low amplitude data from external amplifier before peak detection starts. 

590 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [338 x 246] intentionally omitted <==**

**Figure 7-153. Oversampling the Excitation Signal and Deciding Ideal Sampling Time** 

Auto ideal sample detection is performed through positive peak detection of modulation signal peaks on either Sin or Cos channel. Note that depending where the motor and hence Resolver shaft position is, the ideal sample peaks may be negative or positive. 

**==> picture [144 x 104] intentionally omitted <==**

**----- Start of picture text -----**<br>
Q2 Q1<br>�=�/2<br>�����/2<br>�=� � �=0<br>�=-�<br>Q3 �=-�/2 Q4<br>**----- End of picture text -----**<br>


**Figure 7-154. Rotor Position on Ideal Sin-Cos Circle** 

For example, consider the Sin channel being used for peak detection. With respect to the Figure 7-154, if the rotor zero position is in Q1 or Q2 region, note that the positive peaks of the excitation signal will give the correct sampling point. However if the peak detection is run when the zero position of the rotor is in Q3 or Q4 region, then the positive peak detection of excitation signal will cause the angle position to be shifted by 180 degrees which has to be accounted for accordingly. Hence the RDC sub-system's algorithm has different modes, for finding the ideal sampling position as described below in Section 7.5.3.2.2.1.4.1 to Section 7.5.3.2.2.1.4.4 sections. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 591 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [336 x 276] intentionally omitted <==**

**Figure 7-155. Excitation Signal vs Internal Counters** 

If ENABLE_BOTTOM(register REGS_DEC_GF_CFGx[24]) control bit is set, then sin and cos signals are sampled at both positive and negative peaks of the excitation signal. RDC auto-corrects the sign of the sample. 

592 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

This improves the response time of the loop, since without increasing the sampling rate, data rate of angle output is doubled. 

**==> picture [284 x 223] intentionally omitted <==**

**Figure 7-156. Sine Modulated Excitation Frequency** 

**==> picture [268 x 207] intentionally omitted <==**

## **Figure 7-157. Ideal Sampling Points** 

The above two figures show a sine signal(sine modulated excitation frequency signal) and Ideal sample points shown on the sine signal. 

## _**7.5.3.2.2.1.4.1 Ideal Sample Mode 0**_ 

This is the recommended mode of operation if the zero-position of the rotor is in Q1 region(described earlier in Section 7.5.3.2.2.1.4 #none#) during detection. Both Sin and Cos channels will be positive, the algorithm will select the strongest signal. 

Ideal sample time selection is done in two phases. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

593 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Phase-1:** In the first phase RDC checks the sine channel and cosine channels (clock: oversample coefficient × excitation frequency). It has one counter for sine, and one counter for cosine. These counters get incremented each time a sample is above SAMPLE_DET_THRESHOLD. When total number of samples of both counters reach 2[PEAK_AVG_LIMIT] , two counters are compared. The counter with a larger count is selected as the valid channel to detect demodulation peak. If they are equal, sin channel is selected. 

**Phase-2:** In the second phase, a moving average of 3 samples is continuously compared to each other. If the average starts falling down while previously was moving up, or equal, this is recorded as the local peak. In order to avoid false triggers when the signal is low, samples below SAMPLE_DET_THRESHOLD are ignored. After 2[PEAK_AVG_LIMIT] , ideal local peaks are collected and are averaged to find the ideal peak sampling point. 

## _**7.5.3.2.2.1.4.2 Ideal Sample Mode 1**_ 

This is the recommended mode of operation if the zero-position of the rotor is in Q1 or Q2 during detection (ideally between 45 to 135 degrees). Sin channel will be positive. 

Similar to previous Ideal Sample Mode 0, but Phase-1 is bypassed and sine channel is used for Phase-2 to detect ideal peak sampling point. 

## _**7.5.3.2.2.1.4.3 Ideal Sample Mode 2**_ 

This is the recommended mode of operation if the zero-position of the rotor is in Q1 or Q4 during detection (ideally between 45 to -45 degrees ). Sin channel will be positive. 

Similar to Ideal Sample Mode 1, but Phase-1 is bypassed and cosine channel is used for Phase-2 to detect ideal peak sampling point. 

## _**7.5.3.2.2.1.4.4 Ideal Sample Mode 3**_ 

Auto ideal sample time selection is bypassed, IDEAL_SAMPLE_TIME_OVR(register REGS_SAMPLE_CFG1_x[31:24]) register is used to decide sample time. 

Note that in Modes 0 to 2, when the hardware loop detects the IDEAL_SAMPLE_TIME, the loop will also fill out 20 histogram registers. If the ideal sample location is close to 0, with a noisy signal sometimes the loop may converge to 19, or to 0. The average will give an incorrect value of 10 for the ideal sample time location. To avoid this, it’s recommended to check the histogram registers (OBS_PEAKHISTOGRAM). Then software can decide which point to take as ideal sample time location, and program that with IDEAL_SAMPLE_MODE = 3. 

## _**7.5.3.2.2.1.5 Automatic Gain and Phase Correction**_ 

Ideally the external Resolver's sine and cosine coils need to have a 90° phase shift. They are also expected to have identical gains. Due to misalignment of the coils during resolver manufacturing, and impedance mismatch on the signal paths to the RDC, gains and phase of Sine and Cosine signals may not match, yielding to an error in angle detection. The RDC can correct those gains and phase errors after observing multiple rotations of the Resolver shaft. The timing of Auto Gain and Phase correction are depicted in Figure 7-158: 

- **Step 1** : Excitation frequency is generated, incoming DC offset is cancelled by averaging the sin and cos signals over multiple excitation signal periods and correcting for the deviation from ideal mid-point (or bandpass filter needs to be enabled). Ideal sample time is selected, and RDC starts generating angle data. For this loop to work correctly, resolver shaft needs to be rotating. 

- **Step 2** : Over each rotation period, if gain and phase correction is enabled, the gain and phase deviation of sine and cosine signals with respect to each other is calculated. Effect of noise and acceleration can be minimized by averaging over multiple rotations (external Resolver shaft needs to be rotating). 

Only automatic gain correction can be enabled. Or automatic gain and phase correction can be enabled together. This auto gain and phase correction can also be bypassed, and manually adjusted. 

Automatic Gain and Phase correction consists of two blocks: Estimation logic and Correction logic. Estimation logic can be enabled while the correction logic is either enabled or disabled. For Correction logic to be enabled the Estimation logic has to be enabled. These are controlled using the below registers. 

594 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

1. **BYPASSPHASEGAINCORRx** : 0 enables estimation logic, 1 disables estimation logic. Part of register REGS_PG_EST_CFG2_x[3]. 

2. **AUTOPHASECONTROLx** : 0 disables correction logic, 1 enables correction logic. Part of register REGS_PG_EST_CFG2_x[2]. 

3. **AUTOGAINCONTROLx** : 0 disables correction logic, 1 enables correction logic. Part of register REGS_PG_EST_CFG2_x[1]. 

4. **GAINCOSBYPx** : 16 bit unsigned gain control for cos channel if autogaincontrol is disabled. (2[14] corresponds to gain of 1). Part of register REGS_PG_EST_CFG3_x[31:16]. 

5. **GAINSINBYPx** : 16 bit unsigned gain control for sin channel if autogaincontrol is disabled.(2[14] corresponds to gain of 1). Part of register REGS_PG_EST_CFG3_x[15:0]. 

6. **PHASECOSBYPx** : 16 bit signed phase control for cos channel if autophase is bypassed. (2[15 ] corresponds to phase adjust of 90° and -2[15] corresponds to phase adjust of -90°). Part of register REGS_PG_EST_CFG2_x[31:16]. 

Gain and Phase Correction and Timing 

**==> picture [449 x 314] intentionally omitted <==**

**----- Start of picture text -----**<br>
Angle<br>Enable<br>normalizesignals<br>integralcnt<br>phaseinitcntr 0 1 2 3 4 1 2 3 4 1 2<br>Sinsqacc<br>Cossqacc<br>sincosacc<br>Sinsqaccintegral<br>Cossqaccintegral 0 acc1 acc2 acc3 acc4 acc1 acc2 acc3 acc4 acc1 acc2<br>sincosaccintegral<br>Sinsqacctotal<br>Cossqacctotal<br>sincosacctotal<br>phasedataready<br>Sinsqaccfinal<br>Cossqaccfinal<br>sincosaccfinal<br>autophasegainready<br>**----- End of picture text -----**<br>


**Figure 7-158. Gain and Phase Correction and Timing** 

The phase estimation and gain estimation registers can be read to monitor the estimated phase and gain values of sin and cos signals. Writing to the estimation registers to correct Phase and Gain values is also possible. 

To read the estimated gain and phase values and values and calculate the analog value refer to the below formulae: 

- Estimated differential phase error between sin and cos (deg) = PHASEESTIMATEFINAL × 90 / (2[15] ) 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 595 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

   - Part of register PG_EST_CFG4_x[31:16] 

- Estimated analog gain of cos: √ (2[29] / COSSQACCFINAL) 

   - Part of register PG_EST_CFG5_x[31:0] 

- Estimated analog gain of sin : √ (2[29] / SINSQACCFINAL) 

   - Part of register PG_EST_CFG6_x[31:0] 

## **Note** 

Resolver shaft needs to be rotating for Automatic Gain and Phase Correction to work. 

The estimated gain correction values for sin and cos channels will map the sin and cos data path to perfectly full 16 bits scale. In order to avoid clipping (due to noise and glitches), it is recommended to scale the gain values also. 

## _**7.5.3.2.2.1.6 Glitch Filter and Decimation**_ 

The Decimation block demodulates the sin and cos signals from the modulated signals received from external Resolver. 

**==> picture [500 x 263] intentionally omitted <==**

**Figure 7-159. Selecting Ideal Sampling Point for Demodulation** 

The RDC oversamples the excitation frequency (programmable samples per Texc), and decides on the ideal sampling time compensating for phase shift that occurs on excitation signal path. The envelope of the sin and cos signals are re-constructed by the values obtained at the sampling that was done at the peaks of the sin and cos input signals. This results in the sin and cos signals which the RDC can further pass on to the Arctan or Track-2 blocks for calculating angles and velocity. 

## _**7.5.3.2.2.1.7 Arctan**_ 

This is the second option to recover the angle. It feeds the sin and cos to a simple arctan function block, which produces the angle. This block has no noise rejection feedback loop, hence lower latency but higher noise pass through. It has a precision of 16 bits. Refer to Figure 7-137. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

596 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.3.2.2.1.8 Track2**_ 

**==> picture [481 x 223] intentionally omitted <==**

**----- Start of picture text -----**<br>
Resolver calculates the arctan of sin and cos inputs. It then feeds this arctan signal to a second order phase<br>locked loop (Track2).<br>L��� ��� ter<br>Kp (PI)<br>+ +<br>� X ∑ ∑<br>– �<br>� ‘ z [–1]<br>Feed Forward<br>Acceleration  X<br>Correction Path<br>Angle  �
 Angle Estimate Ki<br>Filter Error Estimate z [–1] ω<br>+<br>+<br>filt coeff<br>**----- End of picture text -----**<br>


The rotational speed(in frequency units) can be calculated based on following formula: 

Speed = VELOCITY × (1/Ts) × (1/2[32] ) : This is rotational speed in Hz. 

where 

- EXC_FREQ_SEL : Excitation frequency setting MMR part of EXCIT_SAMPLE_CFG1[7:0] register. 

- ENABLE_BOTTOM(0 or 1) : bottom sampling control MMR part of DEC_GF_CFG[24] register bit: 1 doubles the data rate. 

- Fs = 100 × EXC_FREQ_SEL × (1 + ENABLE_BOTTOM) : This is the effective sampling rate of track2 loop 

- Ts = 1/Fs : This is the effective sampling time of track2 loop 

- VELOCITY: 32b signed register output of track2. Part of VELOCITY_TRACK2_x[31:0] register. 

## _**7.5.3.2.2.1.9 ADC part of Resolver to Digital Converter**_ 

Definition of terms for ADC-RDC timing interface: 

- **System clock freq fsys** = 50MHz 

- **System clock period Tsys** = 5nS 

- **ADC sampling frequency** : fADC= 1/TADC 

- **ADC sampling period** : TADC = (17 + SOC_WIDTH) × Tsys 

- **Resolver excitation frequency** (1KHz to 20KHz): fEXC = EXC_FREQ_SEL × 100 

- **Resolver excitation period** : TEXC = 1/ fEXC (for 10KHz = 0.1mS = 20K × Tsys) 

- **Resolver oversampling ratio (number of ADC samples over one excitation period): OVR** : 2 × ADC_SAMPLE_RATE 

- **Resolver sampling period** : TEXCOVR = TEXC / OVR 

(if TEXC = 0.1mS, and OVR=20, TEXC = 1K × Tsys) 

- **Resolver demodulation frequency** : 

   - = fEXC , if DOUBLESAMPLE = 0 

   - = 2 × fEXC , if DOUBLESAMPLE = 1 

- **Sample_select_counter** : The internal resolver counter that runs from 0 to (OVR - 1). This decides ideal sample location 

   - Positive peak of excitation signal if doublesample = 0 

   - Both positive and negative peak if doublesample = 1 

   - Runs from 0 to (2 × ADC_SAMPLE_RATE – 1) for every time period of TEXC. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 597 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.3.2.2.1.10 Interrupts**_ 

The RDC produces one hardware event output which is active high level and active high pulse. 

All of the error tracking/diagnostic events can get mapped to generate an event to notify the host an error occurred. The software can emulate a hardware event to verify the full path does not have a fault; this is important for safety. 

There are 4 MMRs for SW to interact with: 

- IRQSTATUS_RAW_SYS_x 

- IRQSTATUS_SYS_x 

- IRQENABLE_SET_SYS_x 

- • IRQENABLE_CLR_SYS_x 

The reading of IRQSTATUS_RAW_SYS_x shows the status of the RAW event, if set it is active, if cleared it is inactive. Even if set, the external event can be deasserted because it is not enabled along with corresponding event in the IRQSTATUS_SYS_x status(post mask/enable). The writing of IRQSTATUS_RAW_SYS_x allows software emulate emulate a hardware event, but the software must first enable that event by writing to IRQENABLE_SET_SYS_x. 

The writing of IRQENABLE_SET_SYS_x is required to enable the hardware event to be asserted. 

The reading of IRQSTATUS_SYS_x shows which hardware events are active. It requires the event to get enabled via IRQENABLE_SET_SYS and that the hardware event did occur. To clear the hardware event, software must write 1 to clear that bit in the IRQSTATUS_SYS_x. 

The writing of IRQENABLE_CLR_SYS_x allows the software to disable hardware events. 

The typical software programming model: 

- For normal operation, enable the necessary hardware events via IRQENABLE_SET_SYS_x. 

- For Safety check out, software must set software event by writing to IRQSTATUS_RAW_SYS_x. 

- To clear the event after interrupt is serviced, the software must write 1 to clear that bit in IRQSTATUS_SYS_x. 

The hardware level event output remains asserted as long as one or more events are active. 

## **7.5.3.3 Programmer's Guide** 

Calibration must be done in a controlled setting with a simple constant rotation of the external resolver for the logic to tune the errors in the signal. After tuning, software can read the tuned values which were calculated, and use them in the future. 

Before operating the Resolver-to-Digital-Converter (RDC), all the registers need to be set correctly. 

An externally connected resolver needs an excitation signal to convert rotational information into a Sine and Cosine modulated signal pair, which are then converted to digital angular information through the RDC. This excitation signal is generated by the internal RDC PWM generator which is then filtered and amplified by an external amplifier(outside AM263P). The output of the external amplifier drives the resolver coil. The sine and cosine outputs of the resolver are sampled, converted to digital signals by ADCs, and processed further by RDC. 

**Step-1 Power-On Diagnostics** : Before initiating the PWM signal and activating the RDC, software is recommended to run diagnostic checks on the resolver ADCs: 

There are two types of diagnostic tests dedicated to ADC: 

1. Open-Short tests: Resolver Cos and Sin coils can be connected to RDC ADC inputs through only passive components including pull/up and pull/down bias resistors or they can be connected through an amplifier. During power-on these connections can be checked through ADC internal Open Short Detection(OSD). Please refer to Section 7.5.2.16 of ADC Chapter for more details. 

2. Runtime diagnostic tests with 2 channels dedicated for diagnostics. While ADCs are not sampling the resolver inputs, they will sample two inputs to check full functionality of the ADCs for safety purpose. 

598 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Step-2 Sequencer** : After diagnostic tests, the next step is to select the desired operating mode through sequencer settings in RESOLVER_REGS_GLOBAL_CFG[11:8]. Refer to Section 7.5.3.2.2.1.1 section for details. RDC subsystem can support one or two hardware Resolvers as described. 

**Step-3 Excitation signal** : Next step is to initialize the excitation signal. The resolver sensor will need a sinusoidal excitation signal with a programmable frequency(using RESOLVER_REGS_EXCIT_SAMPLE_CFG1[7:0]) that will be in sync with the ADC sampling. This signal will be a PWM signal from AM263P which is further filtered and amplified externally(outside AM263P). Before RDC processes incoming data, enough time needs to be allocated for the external PWM to analog signal conversion to settle to its operating frequency. A typical excitation signal PWM filter amplifier(ALM2403-Q1) is shown in Filter and Amplifier Circuit figure and its startup time can be referred for typical settling time of a filter amplifier in data sheet of ALM2403-Q1. 

**Step-4 Oversample Ratio, Bandpass filter and/or Offset Correction** : After excitation frequency settles, Sine and Cosine signals from external resolver will be valid, and calibration and decimation process can be started by software. Each period of excitation frequency is over-sampled by a programmable ratio(using RESOLVER_REGS_EXCIT_SAMPLE_CFG1[15:8]). Default over-sample ratio is 20. This oversamplling enables to use a bandpass filter centered around excitation frequency by providing enough bandwidth. Oversampling also enables offset correction to settle faster and more accurately and also to detect the ideal decimation point. 

Software needs to decide whether to have bandpass filter to be enabled or disabled (using RESOLVER_REGS_DC_OFF_CFG1_0[8]). Enabling bandpass filter will introduce phase delay, but it will significantly improve noise rejection. This bandpass filter will also reject DC offset. If bandpass filter is enabled, DC offset correction can be disabled. Enabling DC offset correction when bandpass filter is enabled will not degrade or improve signal. Regardless of DC correction being enabled, DC offset estimation always runs and that way DC offset monitoring can monitor faults. **Note: Bandpass filter is only designed for oversample ratio-20.** 

If bandpass filter is disabled, it is recommended to enable DC offset correction. Note that if there is no valid excitation signal, DC offset correction will saturate the input signal to the RDC. This condition is monitored in fault detection modes. At this point DC offset fault detection and excitation signal monitor fault detection modes need to be enabled. Refer to the previous sections to program bandpass filter and offset correction. 

## **Note** 

If bandpass filter is disabled, and offset correction needs to be enabled, in this case, offset correction needs to be enabled after ideal sample time selection converges. As explained in next step, ideal sample time checks the peaks to decide ideal sampling point. Although any noise will be averaged, offset correction may introduce false peaks, initially reducing the accuracy. 

**Step-5 Ideal Sample time selection, and decimation:** In order to demodulate the rotation signal, resolver needs to sample the input signal during the peak point of the excitation signal. There are multiple considerations for this: 

1. Ideal sample time selection block oversamples the input signal by 20 and decides the ideal sampling point. 

2. Motor PWM currents are sampled by SOC ADCs. It would be a good practice to align sampling of the resolver signals, with the sampling of the corresponding motor PWM currents. This improves the motor control loop by eliminating the latency. A synchronization pulse coming from motor PWM block which should to be used to synchronize RDC-ADC sampling time. 

3. To demodulate the signal, the peak of excitation signal needs to be sampled. Additionally, software can also enable sampling the negative peak of excitation frequency to improve settling. RDC finds the negative peak, and takes care of the sign automatically as explained in Section Section 7.5.3.2.2.1.4. 

4. If DC offset correction is needed, it needs to be enabled after auto-ideal time selection. 

Once the ideal sample time selection is done and configured as manual value, the DC offset correction can be enabled. This will prevent the DC offset correction from interfering with the ideal sample selection algorithm. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 599 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Step-6 Differential Phase and Gain Mismatch Correction:** Ideally sin and cos signals should have a perfect phase delay of 90 degrees, and their amplitudes should match. If there is a common phase delay, this can be handled by the factory calibration by resetting the 0 deg position, and any minor common gain error will cancel out during arctan calculation. Gross common gain errors will be detected by fault detection mechanisms as explained in fault detection section. In real applications, there will be both differential phase and gain mismatch. Phase and Gain Calibration needs to be done after ideal sample time selection has settled. This is done by enabling the estimation, reading the estimated values and replacing them with manual values. The estimated values can be helpful in the diagnostics. 

**Step-7 Arctan and Track2 outputs:** Output of the Phase and Gain correction goes to arctan block. The arctan data feeds to Track-2 loop. Outputs from the Arctan, or the Track-2 can be read directly from the registers. 

## **CAUTION** 

Please note that there is a hardware limitation on Arctan offset and hardware track2 velocity RESOLVER_REGS_VELOCITY_TRACK2_0[31:0] sampling. Thus a Software track2 can be used in place of hardware track2 . The RESOLVER_ANGLE_SPEED from the SDK implements the Software track2 for velocity sampling. 

After enough time is allowed for excitation signal to stabilize, ideal sampling time can be calculated, and offset correction can be enabled. They work independently, so they can be enabled at the same time, or sequentially. 

The next section describes the RDC diagnostics features and the ways of programming the same. 

## _**7.5.3.3.1 RDC Diagnostics**_ 

RDC is designed for meeting stringent safety requirements. There are multiple safety diagnostics supported, and they are classified under two main groups: 

1. Degradation of Signal (DOS) 

2. Loss of Signal (LOS) 

The following are all the safety features or Diagnostic checks supported by RDC, enabling the system to meet strigent safety requirements. 

1. Monitor Sin or Cos DC offset drift(DOS) 

2. Monitor Sin or Cos Gain drift (DOS) 

3. Monitor Sin or Cos Phase drift (DOS) 

4. Monitor degradation/loss of excitation frequency (DOS) 

5. Monitor Rotational Signal Integrity (DOS) 

6. Monitor Signal Integrity by checking Sin[2] + Cos[2] = Constant (DOS) 

7. Monitor Very high amplitude or Saturation of Sine and Cosine Signals (DOS) 

8. Monitor weak Sine and Cosine Signals (LOS) 

These status check and enabling/disabling of the above diagnostics checks can be performed using the registers in below Table 7-125, which are referred to as IRQ registers in the upcoming sections describing these diagnostics checks. For the register names corresponding to the AM263P Register Addendum, prepend "RESOLVER_REGS_" in front of the register names mentioned in the below RDC Diagnostics sections. 

600 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-125. IRQ registers for RDC0 and RDC1** 

|**RDC**<br>**Instance**|**Diagnostic Register Name**|**Description**|**Physical**<br>**Address**|**Offset**|
|---|---|---|---|---|
|RDC0|IRQSTATUS_RAW_SYS_0|Interrupt Raw Status bit. Can be written to force the<br>status for debugging|502C B030h|0x030|
||IRQSTATUS_SYS_0|Interrupt Status bit. Used for reading the status|502C B034h|0x034|
||IRQENABLE_SET_SYS_0|Interrupt Enable bit. Set this bit to enable the<br>corresponding diagnostic|502C B038h|0x038|
||IRQENABLE_CLR_SYS_0|Interrupt Disable bit. Set this bit to disable the<br>corresponding diagnostic|502C B03Ch|0x03c|
|RDC1|IRQSTATUS_RAW_SYS_1|Interrupt Raw Status bit. Can be written to force the<br>status for debugging|502C B200h|0x200|
||IRQSTATUS_SYS_1|Interrupt Status bit. Used for reading the status|502C B204h|0x204|
||IRQENABLE_SET_SYS_1|Interrupt Enable bit. Set this bit to enable the<br>corresponding diagnostic|502C B208h|0x208|
||IRQENABLE_CLR_SYS_1|Interrupt Disable bit. Set this bit to disable the<br>corresponding diagnostic|502C B20Ch|0x20C|



## _**7.5.3.3.1.1 Monitor Sin or Cos DC offset drift (DOS)**_ 

This diagnostics check can be used for detecting any drift in the DC offset of Sine and Cosine Inputs to RDC. The DC offset estimation block of RDC will correct DC offsets, but through software a threshold can be programmed for detecting excessive and unexpected DC offset values in the Sine and Cosine Inputs to RDC. A seperate positive and negative threshold can be programmed and can be of different magnitude/values. The external Resolver connected to RDC needs to be rotating for this diagnostics to work. 

The below Table 7-126 shows the relevant diagnostics registers for both RDC0 and RDC1. 

**Table 7-126. Registers for configuring the Sin or Cosine DC offset drift** 

|**RDC Instance**|**Diagnostic Register Name**|**Physical Address**|**Offset**|
|---|---|---|---|
|RDC0|DIAG1_0|502C B098h|098h|
|RDC1|DIAG1_1|502C B268h|268h|



The below Table 7-127 shows the corresponding bits to be programmed in the diagnostics registers. The typical programmed value can be about 3295d, which is 5% of the signal's total dynamic range. 

**Table 7-127. Register fields for configuring the Sin or Cosine DC offset drift** 

|**Diagnostic**<br>**Register Name**|**Bit**|**Field**|**Type**|**Reset**|**Typical**<br>**Programmed**<br>**Value**|**Description**|
|---|---|---|---|---|---|---|
|DIAG1_0<br>DIAG1_1|31:16|offsetdrift_threshold_lo|R/W|0h|-3295d|An estimated DC Offset lower than the<br>programmed magnitude would trigger<br>change in the status bits|
||15:0|offsetdrift_threshold_hi|R/W|0h|+3295d|An estimated DC Offset higher than the<br>programmed magnitude would trigger<br>change in the status bits|



The below Table 7-128 shows the register bits of IRQ registers to be used for Reading Status, Enabling/ Disabling the Error Diagnostic check. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 601 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-128. IRQ register bits corresponding to Sine and Cosine DC offset drift** 

|**Bit**|**Field**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|23|offsetdrift_cos_hi_err|R/W|0h|Cosine Signal Drift Crossing the High Threshold Error|
|22|offsetdrift_cos_lo_err|R/W|0h|Cosine Signal Drift Crossing the Low Threshold Error|
|21|offsetdrift_sin_hi_err|R/W|0h|Sine Signal Drift Crossing the High Threshold Error|
|20|offsetdrift_sin_lo_err|R/W|0h|Sine Signal Drift Crossing the Low Threshold Error|



## _Programming Sequence_ 

The typical steps for programming the Sine and Cosine DC Offset Drift checks are mentioned below. 

1. Set the threshold low and threshold high values beyond the normally expected range of DC drift values of Sine and Cosine inputs. 

   - a. Threshold Low should be lower than the minimum expected range of DC Offset Drift. 

   - b. Threshold High should be higher than the maximum expected range of DC Offset Drift. 

2. Enable this diagnostic check by setting the corresponding bit of IRQENABLE_SET_SYS_x. 

3. Check this diagnostic check by monitoring the corresponding bit of IRQSTATUS_SYS_x. 

## For diagnostics health check : 

1. Disable the offset drift check by setting the corresponding bit of IRQENABLE_CLR_SYS_x. 

2. Set thresholds to a very low value that is guaranteed to trigger a fault (for example +10d and -10d). 

3. Check status bits for both Sine and Cosine signals by checking corresponding bits of IRQSTATUS_SYS_x. 

   - a. After verifying that very low threshold value triggered the diagnostic, now clear the corresponding bits of IRQSTATUS_SYS_x. 

4. Program threshold values to regular values beyond the normally expected range of DC drift. 

5. Read status bits for both Sine and Cosine signals by checking corresponding bits of IRQSTATUS_SYS_x again to make sure they are reset. 

6. Enable offset drift check by setting the corresponding bit of IRQENABLE_SET_SYS and start monitoring faults. 

Associated AM263Px MCU+ SDK API with this check: Diag_Mon_SinCos_Offset_drift_data 

## _**7.5.3.3.1.2 Monitor Sin or Cos Gain drift (DOS)**_ 

The Phase and Gain correction block can estimate and correct gain errors during rotation. The Phase and Gain correction will not work if there is no rotation. This diagnostics feature can be used for detecting drift in the gains of Sine and Cosine Inputs to RDC. The Phase and Gain Correction Block contains an Estimation Block and a Correction Block. 

The below registers will contain the estimated values from the Phase and Gain estimation block, needed to estimate the respective gains. Note that 'sq' in the name of these registers indicate the gain is squared. 

- cossqaccfinal = (gaincosbyp)[2] × 2[15] 

- sinsqaccfinal = (gainsinbyp)[2] × 2[15] 

The diagnostic block would monitor these and compare with the set low and high Gain Drift thresholds. Typically select low and high Gain Drift thresholds of 0.7 and 0.9 respectively if the external signal conditioning circuitry(Analog Front End of RDC) will set external gain to 80%(0.8 times) of the ADC input range. These checks will be two indepedent parallel checks for Sine and Cosine signals. 

Assuming minimum gain is 0.7 and maximum gain is 0.9 (1 being the normalized full-scale input range of the ADCs): 

- Low Threshold = (0.7 × 0.7) × 2[15] = 16056 

602 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- High Threshold = (0.9 × 0.9) × 2[15] = 26542 

The below Table 7-129 shows the relevant diagnostics registers for both RDC0 and RDC1. 

**Table 7-129. Registers for configuring the Sin or Cosine Gain drift** 

|**RDC Instance**|**Diagnostic Register Name**|**Physical Address**|**Offset**|
|---|---|---|---|
|RDC0|DIAG14_0|502C B0CCh|0CCh|
||DIAG15_0|502C B0D0h|0D0h|
|RDC1|DIAG14_1|502C B22Ch|29Ch|
||DIAG15_1|502C B238h|2A0h|



The below Table 7-130 shows the corresponding bits to be programmed in the diagnostics registers. 

**Table 7-130. Register fields for configuring the Sin or Cosine Gain drift** 

|**Diagnostic**<br>**Register**<br>**Name**|**Bit**|**Field**|**Type**|**Reset**|**Typical**<br>**Programmed**<br>**Value**|**Description**|
|---|---|---|---|---|---|---|
|DIAG14_0<br>DIAG14_1|31:16|gaindrift_threshold_lo|R/W|0h|16056|Gain Drift Low Threshold|
||15:0|gaindrift_threshold_hi|R/W|0h|26542|Gain Drift High Threshold|
|DIAG15_0<br>DIAG15_1|7:0|gaindrift_glitchcount|R/W|0h|-|Counter limit for times drift error is detected<br>before issuing and error|



The below Table 7-131 shows the register bits of IRQ registers to be used for Reading Status, Enabling/ Disabling the Error Diagnostic check. 

**Table 7-131. IRQ register bits corresponding to Sine and Cosine Gain drift** 

|**Bit**|**Field**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|19|gaindrift_cos_hi_err|R/W|0h|Cosine Signal Gain Drift Crossing the High Threshold Error|
|18|gaindrift_cos_lo_err|R/W|0h|Cosine Signal Gain Drift Crossing the Low Threshold Error|
|17|gaindrift_sin_hi_err|R/W|0h|Sine Signal Gain Drift Crossing the High Threshold Error|
|16|gaindrift_sin_lo_err|R/W|0h|Sine Signal Gain Drift Crossing the Low Threshold Error|



## _Programming Sequence_ 

The typical steps for programming the Sine and Cosine DC Gain Drift checks are mentioned below. 

1. Set the Gain Drift threshold low and threshold high values beyond the normally expected range. 

2. Enable this diagnostic check by setting the corresponding bit of IRQENABLE_SET_SYS_x. 

3. Check this diagnostic check by monitoring the corresponding bit of IRQSTATUS_SYS_x. 

For diagnostics health check : 

1. Disable Gain drift check by setting the corresponding bit of IRQENABLE_CLR_SYS_x. 

2. Set both the low and high Gain Drift thresholds to a very high value such that it is guaranteed to trigger a fault. Checking the corresponding Sine and Cosine bits of IRQSTATUS_SYS_x should show low limit error. 

   - a. After verifying that very high threshold value triggered the diagnostic, now clear the corresponding bits of IRQSTATUS_SYS_x. 

3. Set both the low and high Gain Drift thresholds to a very low value such that it is guaranteed to trigger a fault. Checking the corresponding Sine and Cosine bits of IRQSTATUS_SYS_x should show high limit error. 

   - a. After verifying that very low threshold value triggered the diagnostic, now clear the corresponding bits of IRQSTATUS_SYS_x. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 603 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

4. Program threshold values to regular values beyond the normally expected range of Gain Drift. 

5. Read status bits for both Sine and Cosine signals by checking corresponding bits of IRQSTATUS_SYS_x again to make sure they are reset. 

6. Enable Gain drift check by setting the corresponding bit of IRQENABLE_SET_SYS and start monitoring faults. 

Associated AM263Px MCU+ SDK API with this check: Diag_Mon_SinCos_Gain_drift_data 

## _**7.5.3.3.1.3 Monitor Sin or Cos Phase drift (DOS)**_ 

The Phase and Gain correction block can estimate and correct phase errors during rotation. The Phase and Gain correction will not work if there is no rotation. This diagnostics feature can be used for detecting drift in the phase of Cosine Input to RDC. The Phase and Gain Correction Block contains an Estimation Block and a Correction Block. 

The below register will contain the estimated values from the Phase and Gain estimation block, needed to estimate the phase 

- phaseestimatefinal = (phase error in degrees) × (Π/180) × 2[15] 

The diagnostic block would monitor phaseestimatefinal and compare with the Phase Drift thresholds. For selecting a threshold of 3 degrees(an expected value of 3 degrees of mismatch due to board components mismatch and external resolver coils mismatch) program a value of 1716 as shown below for high and low thresholds for Cosine Phase drift 

- phasedrift_threshold_hi = round(3 × (Π/180) × 2[15] ) = 1716 

- phasedrift_threshold_lo = -round(3 × (Π/180) × 2[15] ) = -1716 

The below Table 7-132 shows the relevant diagnostics registers for both RDC0 and RDC1. 

**Table 7-132. Registers for configuring the Sin or Cosine Phase drift** 

|**RDC Instance**|**Diagnostic Register Name**|**Physical Address**|**Offset**|
|---|---|---|---|
|RDC0|DIAG16_0|502C B0D4h|0D4h|
||DIAG17_0|502C B0D8h|0D8h|
|RDC1|DIAG16_1|502C B2A4h|2A4h|
||DIAG17_1|502C B2A8h|2A8h|



The below Table 7-133 shows the register bits of IRQ registers to be used for Reading Status, Enabling/ Disabling the Error Diagnostic check. 

**Table 7-133. Register fields for configuring the Sin or Cosine Phase drift** 

|**Diagnostic**<br>**Register**<br>**Name**|**Bit**|**Field**|**Type**|**Reset**|**Typical**<br>**Programmed**<br>**Value**|**Description**|
|---|---|---|---|---|---|---|
|DIAG16_0<br>DIAG16_1|31:16|phasedrift_threshold_lo|R/W|0h|-|Phase Drift Low Threshold|
||15:0|phasedrift_threshold_hi|R/W|0h|-|Phase Drift High Threshold|
|DIAG17_0<br>DIAG17_1|7:0|phasedrift_glitchcount|R/W|0h|-|Counter limit for times Phase drift error is<br>detected before issuing and error|



The below Table 7-134 shows the register bits of IRQ registers to be used for Reading Status, Enabling/ Disabling the Error Diagnostic check. 

**Table 7-134. IRQ register bits corresponding to Sine and Cosine Phase drift** 

|**Bit**|**Field**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|15|phasedrift_cos_hi_err|R/W|0h|Cosine Signal Gain Drift Crossing the High Threshold Error|



604 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-134. IRQ register bits corresponding to Sine and Cosine Phase drift (continued)** 

|**Bit**|**Field**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|14|phasedrift_cos_lo_err|R/W|0h|Sine Signal Gain Drift Crossing the High Threshold Error|



## _Programming Sequence_ 

The below are the typical steps for programming the Cosine Phase Drift check. 

1. Set the Phase threshold low and threshold high values beyond the normally expected range. 

2. Enable this diagnostic check by setting the corresponding bit of IRQENABLE_SET_SYS_x. 

3. Check this diagnostic check by monitoring the corresponding bit of IRQSTATUS_SYS_x. 

## For diagnostics health check : 

1. Disable Phase drift check by setting the corresponding bit of IRQENABLE_CLR_SYS_x. 

2. Set Phase Drift thresholds to a very low value that is guaranteed to trigger a fault (for example 1d and -1d). 

3. Check status bits of Cosine Phase drift by checking corresponding bits of IRQSTATUS_SYS_x. 

   - a. After verifying that very low threshold value triggered the diagnostic(both low and high error), now clear the corresponding bits of IRQSTATUS_SYS_x. 

4. Program threshold values to regular values beyond the normally expected range of Phase Drift. 

5. Read status bit of Cosine Phase drift by checking corresponding bit of IRQSTATUS_SYS_x again to make sure it is reset. 

6. Enable Phase drift check by setting the corresponding bit of IRQENABLE_SET_SYS and start monitoring faults. 

Associated AM263Px MCU+ SDK API with this check: Diag_Mon_Cos_Phase_drift_data 

## _**7.5.3.3.1.4 Monitor degradation/loss of excitation frequency (DOS)**_ 

This diagnostic check is used for monitoring the degradation or loss of excitation frequency coming back as part of the modulated Sine and Cosine signals from external Resolver to RDC. 

For this diagnostic check, rotation is not required. Even for fixed angle(with external Resolver stationary or with no rotation), there should be an excitation signal component at least on either Sine or Cosine inputs. For example, for a fixed angle of 0(Zero) Degrees, Sine channel will be flat zero amplitude, but Cosine channel will have maximum amplitude signal, containing the modulated component of the Excitation signal. 

For this diagnostic check, Zero crossings of both Sine and Cosine signals are detected, which runs a counter at frequency of = Excitation Frequency × 1000 (20MHz for 20KHz fexct, 10MHz for 10KHz fexct etc.). Between each zero crossing of the Sine and Cosine signals, the count should be 500 for each half cycle. So this counter should return a count of 500 ideally for each half cycle of Sine and Cosine Signals. 

This count is compared to the threshold from excfreqdrift_threshold_hi and excfreqdrift_threshold_lo registers. If the counter is outside of these threshold limits, then this results in an increase in glitch counter. For each fault, the glitch counter of this diagnostic gets increased and gets compared to excfreqdrift_glitchcount register before triggering the error. 

For typical use cases, a tolerance of ±10%, which is 450 and 550 can be used. 

The below Table 7-135 shows the relevant diagnostics registers for both RDC0 and RDC1. 

**Table 7-135. Registers for configuring degradation/loss of excitation frequency check** 

|**RDC Instance**|**Register Name**|**Physical Address**|**Offset**|
|---|---|---|---|
|RDC0|DIAG2_0|502C B09Ch|09Ch|
||DIAG3_0|502C B0A0h|0A0h|
||DIAG4_0|502C B0A4h|0A4h|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 605 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-135. Registers for configuring degradation/loss of excitation frequency check (continued)** 

|**RDC Instance**|**Register Name**|**Physical Address**|**Offset**|
|---|---|---|---|
|RDC1|DIAG2_1|502C B26Ch|26Ch|
||DIAG3_1|502C B270h|270h|
||DIAG4_1|502C B274h|274h|



The below Table 7-136 shows the corresponding bits to be programmed in the diagnostics registers. 

**Table 7-136. Register fields for configuring degradation/loss of excitation frequency check** 

|**Diagnostic**<br>**Register Name**|**Bit**|**Field**|**Type**|**Reset**|**Typical**<br>**Programmed**<br>**Value**|**Description**|
|---|---|---|---|---|---|---|
|DIAG2_0<br>DIAG2_1|31:16|excfreqdetected_cos|R|x|-|Counts zero crossing of Excitation<br>frequency in Cosine Signal|
||15:0|excfreqdetected_sin|R|x|-|Counts zero crossing of Excitation<br>frequency in Sine Signal|
|DIAG3_0<br>DIAG3_1|31:16|excfreqdrift_threshold_lo|R/W|0x0|450|Low threshold count to detect<br>Excitation Frequency Drift|
||15:0|excfreqdrift_threshold_hi|R/W|0x0|550|High threshold count to detect<br>Excitation Frequency Drift|
|DIAG4_0<br>DIAG4_1|23:16|excfreqdrift_glitchcount|R/W|0x1|-|Excitation Frequency Drift counter limit<br>for issuing error|
||15:0|excfreq_level|R/W|0x0|-|Threshold of ADC value which detects<br>zero crossings|



The below Table 7-137 shows the register bits of IRQ registers to be used for Reading Status, Enabling/ Disabling the Error Diagnostic check. 

**Table 7-137. IRQ register bits corresponding to degradation/loss of excitation frequency check** 

|**Bit**|**Field**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|13|excfreqdrift_hi_err|R/W|0x0|Bit showing Excitation frequency high limit crosssed for Cosine|
|12|excfreqdrift_cos_lo_err|R/W|0x0|Bit showing Excitation frequency low limit crosssed for Cosine|
|11|excfreqdrift_sin_lo_err|R/W|0x0|Bit showing Excitation frequency low limit crosssed for Sine|



## _Programming Sequence_ 

The below are the typical steps for programming the Degradation/loss excitation frequency Diagnostics. 

1. Set the excfreq_level to a value high enough to filter out noisy zero crossing detections. 

2. Set the value of excfreqdrift_threshold_hi and excfreqdrift_threshold_lo to values centered around 500. 

   - a. For a typical tolerance of ±10%, set excfreqdrift_threshold_lo as 450 and excfreqdrift_threshold_hi as 550. 

3. Enable this diagnostic check by setting the corresponding bit of IRQENABLE_SET_SYS_x. 

4. Check this diagnostic check by monitoring the corresponding bit of IRQSTATUS_SYS_x. 

For diagnostics health check : 

1. Disable this diagnostic check by setting the corresponding bit of IRQENABLE_CLR_SYS_x. 

2. Set the excfreqdrift_threshold_lo and excfreqdrift_threshold_hi to a very high value such that the zero crossings can never reach that count(for example 800 and 900). Checking the corresponding bit of IRQSTATUS_SYS_x should show low limit error. 

606 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

   - a. After verifying that very high threshold value triggered the diagnostic, now clear the corresponding bits of IRQSTATUS_SYS_x. 

3. Set the excfreqdrift_threshold_lo and excfreqdrift_threshold_hi to a very low value such that the zero crossings will always exceed that count(for example 40 and 50). Checking the corresponding bit of IRQSTATUS_SYS_x should show high limit error. 

   - a. After verifying that very low threshold value triggered the diagnostic, now clear the corresponding bits of IRQSTATUS_SYS_x. 

4. Enable back this diagnostic check by setting the corresponding bit of IRQENABLE_SET_SYS and start monitoring faults. 

Associated AM263Px MCU+ SDK API with this check: Diag_Mon_ExcFreq_Degradation_data 

## _**7.5.3.3.1.5 Monitor Rotational Signal Integrity (DOS)**_ 

As the motor rotates the external Resolver generates Sine and Cosine signals where in 

- There is only one zero crossing of Rotational Sine signal between two zero crossing of Rotational Cosine signal. 

- There is only one zero crossing of Rotational Cosine signal between two zero crossing of Rotational Sine signal. 

Rotational Sine or Cosine, meaning the demodulated signal containing the modulating Sine and Cosine signal, without the excitation signal part. This Diagnostic check monitors the demodulated rotational Sine and Cosine components obtained from the RDC input signals after demodulation and after Phase and Gain correction. 

Since this check depends on the zero crossings 

- The external Resolver connected to the RDC needs to be rotating for this diagnostic check to be meaningful 

- But when the Resolver connected to the RDC is not rotating, this will NOT cause/trigger this diagnostic. 

- Reversal of rotation direction causes this diagnostic to capture as an error. 

A zero crossing is detected on Sine and Cosine signals when they pass from ±rotfreq_level to ∓rotfreq_level. When there is more than 1 zero crossing, between 2 zero crossings of the other signal, this fault is immediately triggered and the sin_multi_zc_error_count counter counts the number of zero crossings of the failing signal. For example, if there are 5 Sine zero crossings between 2 Cosine Zero crossings, sin_multi_zc_error_count = 5. 

The below Table 7-138 shows the relevant diagnostics registers for both RDC0 and RDC1. 

**Table 7-138. Registers for configuring the rotational signal integrity check** 

|**RDC Instance**|**Register Name**|**Physical Address**|**Offset**|
|---|---|---|---|
|RDC0|DIAG12_0|502C B0C4h|0C4h|
||DIAG13_0|502C B0C8h|0C8h|
|RDC1|DIAG12_1|502C B294h|294h|
||DIAG13_1|502C B298h|298h|



The below Table 7-139 shows the corresponding bits to be programmed in the diagnostics registers. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 607 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-139. Register fields for configuring the rotational signal integrity check** 

|**Register**|**Bit**|**Field**|**Type**|**Reset**|**Typical**<br>**Programmed**<br>**Value**|**Description**|
|---|---|---|---|---|---|---|
|DIAG12_0<br>DIAG12_1|31:16|rotpeak_level|R/W|0x0|26214(with Phase<br>and Gain<br>Correction) or<br>18351|Expected value of Peak level of<br>Sine or Cosine when the other<br>signal crossed zero|
||15:0|rotfreq_level|R/W|0x0|128|Expected ±value for detecting<br>Zero Crossing for Sine or Cosine|
|DIAG13_0<br>DIAG13_1|31:24|cos_multi_zc_error_count|R|x||Count of faulty Cosine signal zero<br>crossings|
||23:16|sin_multi_zc_error_count|R|x||Count of faulty Sine signal zero<br>crossings|
||3|cos_neg_zc_peak_mismatch_err|R|x||During negative zero crossing of<br>Cosine signal, the Sine signal is<br>not beyond +ve or -ve peak|
||2|cos_pos_zc_peak_mismatch_err|R|x||During positive zero crossing of<br>Cosine signal, the Sine signal is<br>not beyond +ve or -ve peak|
||1|sin_neg_zc_peak_mismatch_err|R|x||During negative zero crossing of<br>Sine signal, the Cosine signal is<br>not beyond +ve or -ve peak|
||0|sin_pos_zc_peak_mismatch_err|R|x||During positive zero crossing of<br>Sine signal, the Cosine signal is<br>not beyond +ve or -ve peak|



The below Table 7-140 shows the register bits of IRQ registers to be used for Reading Status, Enabling/ Disabling the Error Diagnostic check. 

**Table 7-140. IRQ register bits corresponding to rotational signal integrity check** 

|**Bit**|**Field**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|10|sin_pos_zc_peak_mismatch_err|R/W|0x0|During positive zero crossing of Sine signal, the Cosine signal is not<br>beyond +ve or -ve peak|
|9|sin_neg_zc_peak_mismatch_err|R/W|0x0|During negative zero crossing of Sine signal, the Cosine signal is not<br>beyond +ve or -ve peak|
|8|cos_pos_zc_peak_mismatch_err|R/W|0x0|During positive zero crossing of Cosine signal, the Sine signal is not<br>beyond +ve or -ve peak|
|7|cos_neg_zc_peak_mismatch_err|R/W|0x0|During negative zero crossing of Cosine signal, the Sine signal is not<br>beyond +ve or -ve peak|
|6|sin_multi_zc_error_err|R/W|0x0|Between two Cosine zero crossings, there are multiple Sine zero<br>crossings|
|5|cos_multi_zc_error_err|R/W|0x0|Between two Sine zero crossings, there are multiple Cosine zero<br>crossings|



## _Programming Sequence_ 

The below are the typical steps for programming the Rotational Signal Integrity Diagnostics. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

608 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

1. The expected signal peak would be 2[15] , for zero crossing detection a good low threshold can be (2[15] ) / 256 = 128. So set rot **freq** _level = 128 for zero crossing detection. 

2. For rot **peak** _level 

   - a. If Phase and Gain correction is enabled, peak signal is expected to be close to 2[15] , so the rotpeak_level can be set to 80% of 2[15] = 0.8 × 32768 = 26214. 

   - b. If Phase and Gain correction is not enabled, gain mismatch needs to be taken into account. Set rotpeak_level = Gain × 0.8 × 2[15] . For example for a gain of 0.7, rotpeak_level = 0.7 × 0.8 × 2[15] = 0.56 × 2[15] = 0.56 × 32768 = 18351. 

3. Enable this diagnostic check by setting the corresponding bit of IRQENABLE_SET_SYS_x. 

4. Check this diagnostic check by monitoring the corresponding bit of IRQSTATUS_SYS_x. 

For diagnostics health check : 

1. Disable this diagnostic check by setting the corresponding bit of IRQENABLE_CLR_SYS_x. 

2. Set the rotpeak_level to a very high value such that it is guaranteed to cause a fault. Checking the corresponding bit of IRQSTATUS_SYS_x **after one rotation** should show error. 

   - a. After verifying that very high threshold value triggered the diagnostic, now clear the corresponding bits of IRQSTATUS_SYS_x. 

3. Set the rotpeak_level to a nominal value. Checking the corresponding bit of IRQSTATUS_SYS_x **after one rotation** should not show any error. 

4. Enable back this diagnostic check by setting the corresponding bit of IRQENABLE_SET_SYS and start monitoring faults. 

Associated AM263Px MCU+ SDK API with this check: Diag_Mon_Rotational_Signal_Integrity_data 

## _**7.5.3.3.1.6 Monitor Signal Integrity by checking Sin[2] + Cos[2] = Constant (DOS)**_ 

This diagnostic check monitors the signal integrity of Sine and Cosine input signals to RDC, by checking that Sin[2] + Cos[2] = Constant. This check is performed on demodulated incoming Sine and Cosine signals before the Phase and Gain correction. Rotation of the external Resolver is not necessary for this diagnostic check. 

Since the values of Sine(sampledsin) and Cosine(sampledcos) can be maximum of ±2[15] , squaring both would result in maximum value of ±2[30] . This diagnostic block divides/shifts both by 16 bits resulting in values max of ±2[14] . 

- Assuming the maximum of Sine and Cosine to be 90% of input ADC range then, 

   - Set sinsqcossq_threshold_hi = 0.81 × (2[14] + 2[14] ) = 26542 

- Assuming the minimum of Sine and Cosine to be 70% of input ADC range then, 

   - Set sinsqcossq_threshold_lo = 0.49 × (2[14] + 2[14] ) = 16056 

If it is seen that the incoming signals samples are nominally centered around 60% of ADC range, the above limits can be modified accordingly. 

If the resulting calculated value from this diagnostic check crosses the above limits(the calculated value is higher than high limit, or lower than low limit), then a fault increments the glitch counter. A fault is issued when the glitch counter reaches the programmed glitch threshold in sinsqcossq_glitchcount. 

The below Table 7-141 shows the relevant diagnostics registers for both RDC0 and RDC1. 

**Table 7-141. Registers for configuring the Sin[2] + Cos[2] = Constant Signal Integrity check** 

|**RDC Instance**|**Register Name**|**Physical Address**|**Offset**|
|---|---|---|---|
|RDC0|DIAG9_0|502C B0B8h|0B8h|
||DIAG10_0|502C B0BCh|0BCh|
||DIAG11_0|502C B0C0h|0C0h|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 609 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-141. Registers for configuring the Sin[2] + Cos[2] = Constant Signal Integrity check (continued)** 

|**RDC Instance**|**Register Name**|**Physical Address**|**Offset**|
|---|---|---|---|
|RDC1|DIAG9_1|502C B288h|288h|
||DIAG10_1|502C B28Ch|28Ch|
||DIAG11_1|502C B290h|290h|



The below Table 7-142 shows the corresponding bits to be programmed in the diagnostics registers. 

**Table 7-142. Register fields for configuring the Sin[2] + Cos[2] = Constant Signal Integrity check** 

|**Register**|**Bit**|**Field**|**Type**|**Reset**|**Typical**<br>**Programmed**<br>**Value**|**Description**|
|---|---|---|---|---|---|---|
|DIAG9_0<br>DIAG9_1|31:16|sinsqcossq_threshold_hi|R/W|0x0|26542|High Threshold value for triggering Sin2+<br>Cos2Signal Integrity error|
||15:0|sinsqcossq_threshold_lo|R/W|0x0|16056|Low Threshold value for triggering Sin2+<br>Cos2Signal Integrity error|
|DIAG10_0<br>DIAG10_1|31:16|sinsqcossq_cossq|R|x|-|Value of Cos2when the Sin2+ Cos2<br>Signal Integrity error was triggered|
||15:0|sinsqcossq_sinsq|R|x|-|Value of Sin2when the Sin2+ Cos2<br>Signal Integrity error was triggered|
|DIAG11_0<br>DIAG11_1|7:0|sinsqcossq_glitchcount|R/W|0x1|-|Sin2+ Cos2Signal Integrity Error counter<br>limit for issuing error|



The below Table 7-143 shows the register bits of IRQ registers to be used for Reading Status, Enabling/ Disabling the Error Diagnostic check. 

**Table 7-143. IRQ register bits corresponding Sin[2] + Cos[2] = Constant Signal Integrity check** 

|**Bit**|**Field**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|4|sinsqcossq_hi_err|rw1ts|0x0|Sin2+ Cos2value is too high|
|3|sinsqcossq_lo_err|rw1ts|0x0|Sin2+ Cos2value is too low|



## _Programming Sequence_ 

The below are the typical steps for programming this check. 

1. Set the sinsqcossq_threshold_hi and sinsqcossq_threshold_lo values beyond the normally expected ranges. 

2. Enable this diagnostic check by setting the corresponding bit of IRQENABLE_SET_SYS_x. 

3. Check this diagnostic check by monitoring the corresponding bit of IRQSTATUS_SYS_x. 

For diagnostics health check : 

1. Disable Signal Integrity check by setting the corresponding bit of IRQENABLE_CLR_SYS_x. 

2. Set the sinsqcossq_threshold_hi and sinsqcossq_threshold_lo to very high values such that the calculated value can never reach these thresholds. Checking the corresponding bit of IRQSTATUS_SYS_x should show low limit error. 

   - a. After verifying that very high threshold value triggered the diagnostic, now clear the corresponding bits of IRQSTATUS_SYS_x. 

3. Set the sinsqcossq_threshold_hi and sinsqcossq_threshold_lo to very low values such that the calculated value will always exceed these thresholds. Checking the corresponding bit of IRQSTATUS_SYS_x should show high limit error. 

610 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

   - a. After verifying that very low threshold value triggered the diagnostic, now clear the corresponding bits of IRQSTATUS_SYS_x. 

4. Program threshold values to regular values beyond the normally expected range of Signal Integrity check. 

5. Read status bit of Signal Integrity check by checking corresponding bit of IRQSTATUS_SYS_x again to make sure it is reset. 

6. Enable Signal Integrity check by setting the corresponding bit of IRQENABLE_SET_SYS and start monitoring faults. 

Associated AM263Px MCU+ SDK API with this check: Diag_Mon_Signal_Integrity_SinSq_CosSq 

## _**7.5.3.3.1.7 Monitor Very high amplitude or Saturation of Sine and Cosine Signals (DOS)**_ 

This diagnostic check monitors the amplitude of Sine and Cosine input signals to RDC, before offset correction and demodulation. Any one of the input signals exceeding the threshold set by highamplitude_threshold, causes the glitch counter to increase by one. Once the glitch counter reaches the threshold programmed in highamplitude_glitchcount, it causes an errror. This diagnostic check does not need the external Resolver to be rotating. 

The value in highamplitude_threshold determines the threshold for this error. Setting a value of 0.9 × 2[15] = 29491 makes this diagnostic check to increase the glitch counter when amplitude goes above 90% of the maximum input ADC range of RDC. 

The below Table 7-144 shows the relevant diagnostics registers for both RDC0 and RDC1. 

**Table 7-144. Registers for configuring the Saturation of Sine and Cosine Signals check** 

|**RDC Instance**|**Register Name**|**Physical Address**|**Offset**|
|---|---|---|---|
|RDC0|DIAG7_0|502C B0B0h|0B0h|
||DIAG8_0|502C B0B4h|0B4h|
|RDC1|DIAG7_1|502C B280h|280h|
||DIAG8_1|502C B284h|284h|



The below Table 7-145 shows the corresponding bits to be programmed in the diagnostics registers. 

**Table 7-145. Register fields for configuring the Saturation of Sine and Cosine Signals check** 

|**Register**|**Bit**|**Field**|**Type**|**Reset**|**Typical**<br>**Programmed**<br>**Value**|**Description**|
|---|---|---|---|---|---|---|
|DIAG7_0<br>DIAG7_1|23:16|highamplitude_glitchcount|R/W|0x1|-|High Amplitude Error counter limit for<br>issuing error|
||15:0|highamplitude_threshold|R/W|0x0|29491|Threshold value to detect High<br>Amplitude value. Both Sine and Cosine<br>need to go higher than this.|
|DIAG8_0<br>DIAG8_1|31:16|highamplitude_cos|R|x|-|Value of Cosine Signal at the high<br>amplitude error trigger instant|
||15:0|highamplitude_sin|R|x|-|Value of Sine Signal at the high<br>amplitude error trigger instant|



The below Table 7-146 shows the register bits of IRQ registers to be used for Reading Status, Enabling/ Disabling the Error Diagnostic check. 

**Table 7-146. IRQ register bits corresponding to the Saturation of Sine and Cosine Signals check** 

|**Bit**|**Field**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|2|highamplitude_sin_fault_err|R/W|0x0|Sine signal value crossed high threshold|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 611 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Table 7-146. IRQ register bits corresponding to the Saturation of Sine and Cosine Signals check (continued)** 

|**Bit**|**Field**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|1|highamplitude_cos_fault_err|R/W|0x0|Cosine signal value crossed high threshold|



## _Programming Sequence_ 

The below are the typical steps for programming this check. 

1. Set the highamplitude_threshold to value beyond the normally expected range of Sine and Cosine input signals. 

2. Enable this diagnostic check by setting the corresponding bit of IRQENABLE_SET_SYS_x. 

3. Check this diagnostic check by monitoring the corresponding bit of IRQSTATUS_SYS_x. 

## For diagnostics health check : 

1. Disable this check by setting the corresponding bit of IRQENABLE_CLR_SYS_x. 

2. Set the highamplitude_threshold to a very low value that is guaranteed to trigger a fault. 

3. Check status bits of this diagnostic check from corresponding bits of IRQSTATUS_SYS_x. 

   - a. After verifying that very low threshold value triggered the diagnostic, now clear the corresponding bits of IRQSTATUS_SYS_x. 

4. Program highamplitude_threshold value to regular value beyond the normally expected range of Sine and Cosine input signals. 

5. Read status bit of this check by checking corresponding bit of IRQSTATUS_SYS_x again to make sure it is reset. 

6. Enable this check by setting the corresponding bit of IRQENABLE_SET_SYS and start monitoring faults. 

Associated AM263Px MCU+ SDK API with this check: Diag_Mon_Sin_Cos_High_Amplitude 

## _**7.5.3.3.1.8 Monitor weak Sine and Cosine Signals (LOS)**_ 

This diagnostic check monitors the demodulated Sine and Cosine input signals to RDC, after offset correction and demodulation, but before phase and gain correction. For good set of input signals, the amplitude of either of the demodulated Sine and Cosine signals should be above above a threshold. If neither of the signals are above the threshold set by lowamplitude_threshold, it causes the glitch counter to increase by one. Once the glitch counter reaches the threshold programmed in lowamplitude_glitchcount, it causes an error. This diagnostic check does not need the external Resolver to be rotating. 

The value in lowamplitude_threshold determines the threshold for this error. Since the full scale amplitude value of input signals with gain 1 would be 2[15] , a typical value between 2[13] = 8192 to 2[12] = 4096 can be programmed as lowamplitude_threshold. While programming the lowamplitude_threshold, care has to be taken to ensure it accomodates the Sine and Cosine signal values when they are equal (example when external Resolver connected to RDC is at 45 Degrees). 

The below Table 7-147 shows the relevant diagnostics registers for both RDC0 and RDC1. 

**Table 7-147. Registers for configuring the weak Sin and Cosine signals check** 

|**RDC Instance**|**Register Name**|**Physical Address**|**Offset**|
|---|---|---|---|
|RDC0|DIAG5_0|502C B0A8h|0A8h|
||DIAG6_0|502C B0ACh|0ACh|
|RDC1|DIAG5_1|502C B278h|278h|
||DIAG6_1|502C B27Ch|27Ch|



The below Table 7-148 shows the corresponding bits to be programmed in the diagnostics registers. 

612 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-148. Register fields for configuring the weak Sin and Cosine signals check** 

|**Register**|**Bit**|**Field**|**Type**|**Reset**|**Typical**<br>**Programmed**<br>**Value**|**Description**|
|---|---|---|---|---|---|---|
|DIAG5_0<br>DIAG5_1|23:16|lowamplitude_glitchcount|R/W|0x1|-|Low Amplitude Error counter limit for<br>issuing error|
||15:0|lowamplitude_threshold|R/W|0x0|8192|Threshold value to detect Low<br>Amplitude value. Both Sine and Cosine<br>need to be lower than this.|
|DIAG6_0<br>DIAG6_1|31:16|lowamplitude_cos|R|x|-|Value of Cosine Signal at the low<br>amplitude error trigger instant|
||15:0|lowamplitude_sin|R|x|-|Value of Sine Signal at the low<br>amplitude error trigger instant|



The below Table 7-149 shows the register bit of IRQ registers to be used for Reading Status, Enabling/Disabling this Diagnostic check. 

**Table 7-149. IRQ register bits corresponding to the weak Sin and Cosine signals check** 

|**Bit**|**Field**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|0|lowamplitude_err|rw1ts|0x0|Demodulated Sine and Cosine signals not crossing low amplitude Threshold|



## _Programming Sequence_ 

The below are the typical steps for programming this check. 

1. Set the lowamplitude_threshold to value lower than the normally expected range of Sine and Cosine input signals. 

2. Enable this diagnostic check by setting the corresponding bit of IRQENABLE_SET_SYS_x. 

3. Check this diagnostic check by monitoring the corresponding bit of IRQSTATUS_SYS_x. 

## For diagnostics health check : 

1. Disable this diagnostic check by setting the corresponding bit of IRQENABLE_CLR_SYS_x. 

2. Set the lowamplitude_threshold to a very high value that is guaranteed to trigger a fault(for example 2[15] ). 

3. Check status bit of this diagnostic check from corresponding bits of IRQSTATUS_SYS_x. 

   - a. After verifying that very high threshold value triggered the diagnostic, now clear the corresponding bits of IRQSTATUS_SYS_x 

4. Program lowamplitude_threshold to regular value, lower than the normally expected range of Sine and Cosine input signals. 

5. Read status bit of this check by checking corresponding bit of IRQSTATUS_SYS_x again to make sure it is reset. 

6. Enable this check by setting the corresponding bit of IRQENABLE_SET_SYS and start monitoring faults. 

Associated AM263Px MCU+ SDK API with this check: Diag_Mon_Sin_Cos_Weak_Amplitude 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 613 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.4 Comparator Subsystem (CMPSS)**_ 

The Comparator Subsystem (CMPSS) consists of analog comparators and supporting circuits that are useful for power applications such as peak current mode control, switched-mode power, power factor correction, voltage trip monitoring, and so forth. 

**7.5.4.1 Introduction** ..................................................................................................................................................615 **7.5.4.2 ADC-CMPSS Signal Connections** .............................................................................................................. 620 **7.5.4.3 Reference DAC** ............................................................................................................................................ 622 **7.5.4.4 Ramp Generator** .......................................................................................................................................... 623 **7.5.4.5 Digital Filter** ..................................................................................................................................................627 **7.5.4.6 Using the CMPSS** ........................................................................................................................................ 628 **7.5.4.7 Enabling and Disabling the CMPSS Clock** ................................................................................................630 **7.5.4.8 CMPSS Programming Guide** ...................................................................................................................... 630 

614 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.4.1 Introduction** 

The comparator subsystem is built around a number of modules. Each subsystem contains two comparators, two reference 12-bit DACs, and two digital filters. Comparators are denoted "H" or "L" within each module where “H” and “L” represent high and low, respectively. Each comparator generates a digital output which indicates whether the voltage on the positive input is greater than the voltage on the negative input. The positive input of the comparator is driven from external pins. 

Each comparator output passes through a programmable digital filter that can remove spurious trip signals. An unfiltered output is also available if filtering is not required. The negative input for only COMPH(CMPSSA) can be driven by an external pin or by programmable 12-bit DAC. The negative input for COMPL (CMPSSA) can only be driven by 12-bit DAC. The negative input for CMPSSB (COMPH and COMPL) can only be driven by the programmable 12-bit DAC. 

## _**7.5.4.1.1 Features**_ 

Each CMPSS includes: 

- Two analog comparators 

- Two independently programmable reference 12-bit DACs 

- One decrementing ramp generator 

- Two digital filters, max filter clock prescale = 2[16] 

- Ability to synchronize submodules with EPWMSYNCPER 

- Ability to extend clear signal with EPWMBLANK 

- Ability to synchronize output with SYSCLK 

- Ability to latch output 

- Ability to invert output 

- Option to use hysteresis on the input 

- Option for negative input of comparator to be driven by an external signal or by the reference DAC for COMPH 

- VDACREF is the DAC reference voltage 

- Diode emulation support 

   - The system works with EPWM to support the Diode emulation feature 

   - Details about Diode emulation can be found in _ePWM Modules Overview_ 

- Ramp generator prescaler 

CMPSSA has the above features, and the additional support of INH and INL as a muxable input for the COMPL positive signal. Figure 7-160 and Figure 7-161 show the differences. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

615 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 256] intentionally omitted <==**

**Figure 7-160. CMPSSA Block Diagram** 

**==> picture [500 x 256] intentionally omitted <==**

**Figure 7-161. CMPSSB Block Diagram** 

## _**7.5.4.1.2 Comparator**_ 

Section 7.5.4.1.3 shows several comparators. The comparator generates a high digital output when the voltage on the positive input is greater than the voltage on the negative input, and a low digital output when the voltage on the positive input is less than the voltage on the negative input. The comparator is illustrated in Figure 7-162. 

616 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [154 x 72] intentionally omitted <==**

**----- Start of picture text -----**<br>
A +<br>Comparator Output<br>B _<br>**----- End of picture text -----**<br>


**Figure 7-162. Comparator Block Diagram** 

|**Voltages**|**Output**|
|---|---|
|Voltage A > Voltage B|1|
|Voltage A < Voltage B|0|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

617 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.4.1.3 Block Diagram**_ 

The block diagram for the CMPSS is shown in the images below. 

- CTRIPx(x= "H" or "L") signals are connected to the ePWM X-BAR for ePWM trip response. See the _Enhanced Pulse Width Modulator (ePWM)_ chapter for more details on the ePWM X-BAR mux configuration. 

- CTRIPxOUTx(x= "H" or "L") signals are connected to the Output X-BAR for external signaling. See the _General-Purpose Input/Output (GPIO)_ chapter for more details on the Output X-BAR mux configuration. 

**Figure 7-163. CMPSS Module Block Diagram - Detailed** 

**==> picture [500 x 270] intentionally omitted <==**

618 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 298] intentionally omitted <==**

**Figure 7-164. CMPSSA Module Block Diagram - Integration** 

**==> picture [500 x 301] intentionally omitted <==**

**Figure 7-165. CMPSSB Module Block Diagram - Integration** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

619 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Note** 

Colors help highlight key parts of the diagram, but do not contain meaning otherwise. 

This concludes the CMPSS introduction. Additional foundational material can be found at: 

- Comparator Subsystem Training 

- Real-Time Cntrol Reference Guide (Refer to the Comparator section) 

## **7.5.4.2 ADC-CMPSS Signal Connections** 

In each ADC, two sets of differential pins shall be shared with pins of two CMPSSA and remaining one pair of differential pins shall be connected to two independent pins of CMPSSB. These pins are demonstrated in Figure 7-166 and Table 7-150 where the CHSEL values determine how the inputs are fed into ADC. 

**==> picture [456 x 213] intentionally omitted <==**

**----- Start of picture text -----**<br>
CMPSS-A CMPSS-A CMPSS-B CMPSS-B<br>12-bit 12-bit 12-bit 12-bit<br>DAC DAC DAC DAC<br>DAC-H DAC-L DAC-H DAC-L<br>12-bit 12-bit 12-bit 12-bit Code Code Code Code<br>DAC DAC DAC DAC<br>DAC-H DAC-L DAC-H DAC-L<br>Code Code Code Code<br>ATB<br>INP-0<br>INM-0<br>INP-1<br>INM-1 12-bit<br>4 MSPS<br>INP-2<br>INM-2<br>CAL-0<br>CAL-1<br>+ – – + + – _ + + – _ + + – _ +<br>**----- End of picture text -----**<br>


**Figure 7-166. CMPSS and ADC Connections** 

**Table 7-150. Connectivity between ADC Inputs to CMPSS Signals** 

|**Signal/Pin Name**|**ADC Input**|**CMPSS Input**|
|---|---|---|
|ADC0 Channels|||
|ADC0_AIN0|ADC0:inp0 (+IN0)|CMPSSA0:inH (+IN)|
|ADC0_AIN1|ADC0:inm0 (-IN0)|CMPSSA0:inL (-IN)|
|ADC0_AIN2|ADC0:inp1 (+IN1)|CMPSSA1:inH (+IN)|
|ADC0_AIN3|ADC0:inm1 (-IN1)|CMPSSA1:inL (-IN)|
|ADC0_AIN4|ADC0:inp2 (+IN2)|CMPSSB0:inH/inL (+IN/-IN)|
|ADC0_AIN5|ADC0:inm2 (-IN2)|CMPSSB1:inH/inL (+IN/-IN)|
|ADC_CAL1|ADC0:inm3 (-IN3)|X|
|ADC_CAL0|ADC0:inp3 (+IN3)|X|
|ADC1 Channels|||
|ADC1_AIN0|ADC1:inp0 (+IN0)|CMPSSA2:inH (+IN)|
|ADC1_AIN1|ADC1:inm0 (-IN0)|CMPSSA2:inL (-IN)|
|ADC1_AIN2|ADC1:inp1 (+IN1)|CMPSSA3:inH (+IN)|
|ADC1_AIN3|ADC1:inm1 (-IN1)|CMPSSA3:inL (-IN)|
|ADC1_AIN4|ADC1:inp2 (+IN2)|CMPSSB2:inH/inL (+IN/-IN)|



620 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-150. Connectivity between ADC Inputs to CMPSS Signals (continued)** 

|**Signal/Pin Name**|**ADC Input**|**CMPSS Input**|
|---|---|---|
|ADC1_AIN5|ADC1:inm2 (-IN2)|CMPSSB3:inH/inL (+IN/-IN)|
|ADC_CAL1|ADC1:inm3 (-IN3)|X|
|ADC_CAL0|ADC1:inp3 (+IN3)|X|
|ADC2 Channels|||
|ADC2_AIN0|ADC2:inp0 (+IN0)|CMPSSA4:inH (+IN)|
|ADC2_AIN1|ADC2:inm0 (-IN0)|CMPSSA4:inL (-IN)|
|ADC2_AIN2|ADC2:inp1 (+IN1)|CMPSSA5:inH (+IN)|
|ADC2_AIN3|ADC2:inm1 (-IN1)|CMPSSA5:inL (-IN)|
|ADC2_AIN4|ADC2:inp2 (+IN2)|CMPSSB4:inH/inL (+IN/-IN)|
|ADC2_AIN5|ADC2:inm2 (-IN2)|CMPSSB5:inH/inL (+IN/-IN)|
|ADC_CAL1|ADC2:inm3 (-IN3)|X|
|ADC_CAL0|ADC2:inp3 (+IN3)|X|
|ADC3 Channels|||
|ADC3_AIN0|ADC3:inp0 (+IN0)|CMPSSA6:inH (+IN)|
|ADC3_AIN1|ADC3:inm0 (-IN0)|CMPSSA6:inL (-IN)|
|ADC3_AIN2|ADC3:inp1 (+IN1)|CMPSSA7:inH (+IN)|
|ADC3_AIN3|ADC3:inm1 (-IN1)|CMPSSA7:inL (-IN)|
|ADC3_AIN4|ADC3:inp2 (+IN2)|CMPSSB6:inH/inL (+IN/-IN)|
|ADC3_AIN5|ADC3:inm2 (-IN2)|CMPSSB7:inH/inL (+IN/-IN)|
|ADC_CAL1|ADC3:inm3 (-IN3)|X|
|ADC_CAL0|ADC3:inp3 (+IN3)|X|
|ADC4 Channels|||
|ADC4_AIN0|ADC4:inp0 (+IN0)|CMPSSA8:inH (+IN)|
|ADC4_AIN1|ADC4:inm0 (-IN0)|CMPSSA8:inL (-IN)|
|ADC4_AIN2|ADC4:inp1 (+IN1)|CMPSSA9:inH (+IN)|
|ADC4_AIN3|ADC4:inm1 (-IN1)|CMPSSA9:inL (-IN)|
|ADC4_AIN4|ADC4:inp2 (+IN2)|CMPSSB8:inH/inL (+IN/-IN)|
|ADC4_AIN5|ADC4:inm2 (-IN2)|CMPSSB9:inH/inL (+IN/-IN)|
|ADC_CAL0|ADC4:inp3 (+IN3)|X|
|ADC_CAL1|ADC4:inm3 (-IN3)|X|



## **Note** 

In the **ADC Input** column in ADC-CMPSS Signal Connectivity Table above, "inp" stands for positive inputs and "inm" stands for negative inputs. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 621 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.4.3 Reference DAC** 

Each reference 12-bit DAC can be configured to drive a reference voltage into the negative input of the respective comparator. The reference 12-bit DAC output is internal only and cannot be observed externally. 

Two sets of DACxVAL registers, DACxVALA and DACxVALS, are present for each reference 12-bit DAC. DACxVALA is a read-only register that actively controls the reference 12-bit DAC value. DACxVALS is a writable shadow register that loads into DACxVALA either immediately or synchronized with the next EPWMSYNCPER event. The high and low reference 12-bit DAC (DACx) can optionally source the register DACxVALA value from the ramp generator instead of the register DACxVALS. 

The operating range of the reference 12-bit DAC is bounded by DACREF and VSSA. The high-voltage reference is VDDA by default, but the high voltage reference can be configured to be VDAC using the COMPDACCTL register. The reference 12-bit DAC is illustrated in Figure 7-167. 

**==> picture [304 x 203] intentionally omitted <==**

**----- Start of picture text -----**<br>
COMPDACCTL[SELREF]<br>VDDA<br>0<br>DACREF<br>VDAC 1<br>12-bit DACOUTH<br>DACHVALA<br>DACH<br>To COMPH<br>12-bit DACOUTL<br>DACLVALA<br>DACL<br>To COMPL<br>VSSA<br>**----- End of picture text -----**<br>


**Figure 7-167. Reference DAC Block Diagram** 

The output of the reference 12-bit DAC can be calculated as: 

DACVALA*DACREF 33 DACOUT = × 4096 18 

(11) 

## **Note** 

- In the situations where both the DACH and DACL are driving the high and low comparators, a trip on one comparator can temporarily disturb the DAC output of the other comparator. The amount and length of time of this disturbance is specified in the device data sheet as “CMPSS DAC output disturbance” and “CMPSS DAC disturbance time”, respectively. 

- Users must design their system carefully so that if the input signal crosses either DACH or DACL and trips the associated comparator, the input signal stays more than a “CMPSS DAC output disturbance” away from the other comparator trip point for “CMPSS DAC disturbance time”. 

- The DACH setting must always be higher than the DACL setting. If the user is not using DACL, then DACLVALS register should be programmed to maximum, so that COMPL does not trip and affect DACH. In this case, there is no limitation on the DACHVALS setting. Accordingly, when not using the DACH, the user must set the DACHVALS register to the maximum. 

- The CMPSS instance can be enabled before programming the reference DAC values. 

622 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [500 x 322] intentionally omitted <==**

**Figure 7-168. CMPSS DAC Static Offset** 

## **Note** 

CMPSS DAC threshold value drifts with change in temperature, so one needs to take care of the below characteristics for DAC calibration 

- CMPSS DAC generates 0-3.3V for 12 bit code 

- CMPSS comparator input (aka offset error) is -20 mV to + 20 mV 

- CMPSS DAC Static Offset error is -45 mV to 45 mV and is shown in _CMPSS DAC Static Offset_ 

- CMPSS DAC Static Gain Error is -2 % to 2 % of FSR 

## **7.5.4.4 Ramp Generator** 

This section discusses the characteristics and behavior of the ramp generator. 

## _**7.5.4.4.1 Ramp Generator Overview**_ 

The ramp generator produces a falling ramp input for the high-reference 12-bit DAC when selected. In this mode, the reference 12-bit DAC uses the most-significant 12 bits of the RAMPSTS countdown register as the input. The low 4 bits of the RAMPSTS countdown register effectively act as a prescale for the falling ramp rate configurable with RAMPxSTEPVALA 

The ramp generator is enabled by setting DACSOURCE = 1. When DACSOURCE = 1 is selected, the value of RAMPSTS is loaded from RAMPxREFS and the register remains static until the selected EPWMSYNCPER signal is received. After receiving the selected EPWMSYNCPER signal, the value of RAMPDECVALA is subtracted from RAMPSTS on every subsequent SYSCLK cycle. 

To prevent the subtraction from commencing a SYSCLK cycle after a EPWMSYNCPER event, the RAMPDLYA register that serves as a delay counter can be used to hold off the RAMPSTS subtraction. On receiving a 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 623 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

EPWMSYNCPER event, the value of RAMPDLYA is decremented by one on every SYSCLK cycle until the register reaches zero. So, the RAMPSTS subtraction only begins when RAMPDLYA is zero. 

624 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.4.4.2 Ramp Generator Behavior**_ 

The ramp generator makes state changes on every rising edge of DACSOURCE, EPWMSYNCPER, EPWMSYNCPER_H, and COMPHSTS. 

On the rising edge of DACSOURCE: RAMPHREFA, RAMPHSTEPVALA, and RAMPDLYA are loaded with their shadow registers. RAMPSTS is loaded with RAMPHREFS. 

On the rising edge of the selected EPWMSYNCPER_H: RAMPHREFA, RAMPHSTEPVALA, and RAMPDLYA are loaded with their shadow registers. RAMPSTS is loaded with RAMPHREFS and starts decrementing when RAMPDLYA counter reaches zero. 

On the rising edge of COMPHSTS with RAMPLOADSEL = 1: RAMPHREFA, RAMPxREFA, RAMPxSTEPVALA, and RAMPDLYA are loaded with their shadow registers. RAMPSTS is loaded with RAMPxREFS and stops decrementing. 

On the rising edge of COMPHSTS with RAMPLOADSEL = 0: RAMPSTS is loaded with RAMPHREFA and stops decrementing. 

Additionally, if the value of RAMPSTS reaches zero, the RAMPSTS register remains static at zero until the next EPWMSYNCPER_H is received. These state changes are illustrated in the ramp generator block diagram in Figure 7-169. 

**==> picture [500 x 205] intentionally omitted <==**

**Figure 7-169. Ramp Generator Block Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

625 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.4.4.3 Ramp Generator Behavior at Corner Cases**_ 

Since the ramp generator makes state changes on every rising edge of EPWMSYNCPER_H and COMPHSTS, the following behavior can be expected on instances when these two events occur simultaneously or very close together. 

Case 1: COMPHSTS rising edge occurs one or more cycles before EPWMSYNCPER_H rising edge. RAMPSTS stops decrementing on COMPHSTS rising edge event. RAMPSTS starts decrementing on EPWMSYNCPER_H rising edge event when RAMPDLYA reaches 0. 

Case 2: COMPHSTS rising edge occurs simultaneously as EPWMSYNCPER_H rising edge. EPWMSYNCPER rising edge event takes precedence and RAMPSTS starts decrementing when RAMPDLYA reaches 0. COMPHSTS rising edge event is ignored and does not halt RAMPSTS. 

Case 3: COMPHSTS rising edge occurs one or more cycles after EPWMSYNCPER_H rising edge but before RAMPDLYA reaches 0. RAMPSTS does not decrement when RAMPDLYA reaches 0. 

Case 4: COMPHSTS rising edge occurs simultaneously as RAMPDLYA reaches 0 from EPWMSYNCPER_H rising edge. RAMPSTS does not decrement. 

This behavior is also illustrated in the below image. 

**==> picture [457 x 290] intentionally omitted <==**

**----- Start of picture text -----**<br>
EPWMSYNCPER_H<br>0xFFFF<br>RAMPHREFS<br>CMP_HP<br>RAMPHSTS RAMPHREFS<br>RAMPHREFS<br>CMP_HP RAMPHREFS<br>0x0000<br>COMPHSTS<br>**----- End of picture text -----**<br>


**Figure 7-170. Ramp Generator Behavior** 

626 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.4.5 Digital Filter** 

The digital filter works on a window of FIFO samples (SAMPWIN) taken from the input. The filter output resolves to the majority value of the sample window, where majority is defined by the threshold (THRESH) value. If the majority threshold is not satisfied, the filter output remains unchanged. 

For proper operation, the value of THRESH must be greater than SAMPWIN / 2 and less than or equal to SAMPWIN. 

A prescale function (CLKPRESCALE) determines the filter sampling rate, where the filter FIFO captures one sample every prescale system clocks. Old data from the FIFO is discarded. 

Note that for SAMPWIN, THRESH and CLKPRESCALE, the internal number used by the digital filter is + 1 in all cases. In essence, samples = SAMPWIN + 1, threshold = THRESH + 1 and prescale = CLKPRESCALE + 1. 

A conceptual model of the digital filter is shown in Figure 7-171. 

**==> picture [361 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
Filter Output<br>Digital Filter<br>Filter Input Data Latch 0  1  2  3  4  5  6  7  8  9  10 11 12 …...  NN+1 bit FIFO [Data Discard]<br>SAMPWIN = 9 (Internal Sample Window => 9+1 = 10)<br>CLKPRESCALE THRESH = 5 (Internal Threshold => 5+1 = 6)<br>Example One: Number of 1s = 8<br>1 1 0 1 1 0 1 1 1 1 Filter Output = 1<br>SYSCLK<br>Example Two: Number of 1s = 6<br>1 1 0 1 1 0 1 0 0 1 Filter Output = 1<br>Example Three: Number of 1s = 5<br>0 1 0 1 1 0 1 0 0 1 Filter Output = 0<br>**----- End of picture text -----**<br>


**Figure 7-171. Digital Filter Behavior** 

Equivalent C code of the filter implementation is: 

```
if (FILTER_OUTPUT == 0) {
    if (Num_1s_in_SAMPWIN >= THRESH) {
        FILTER_OUTPUT = 1;
    }
}
else {
    if (Num_0s_in_SAMPWIN >= THRESH) {
        FILTER_OUTPUT = 0;
    }
}
```

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 627 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.4.5.1 Filter Initialization Sequence**_ 

For proper operation of the digital filter, the following initialization sequence is recommended: 

1. Configure and enable the comparator for operation. 

2. Configure the digital filter parameters for operation: 

   - Set SAMPWIN for the number of samples to monitor in the FIFO window. 

   - Set THRESH for the threshold required for majority qualification. 

   - Set CLKPRESCALE for the digital filter clock prescale value. 

3. Initialize the sample values in the digital FIFO window by setting FILINIT. 

4. Clear COMPSTS latch using COMPSTSCLR, if the latched path is desired. 

5. Configure the CTRIP and CTRIPOUT signal paths. 

6. If desired, configure the destination module, for example, ePWM, GPIO, and so on to accept the filtered signals. 

## **7.5.4.6 Using the CMPSS** 

## _**7.5.4.6.1 LATCHCLR, EPWMSYNCPER and EPWMBLANK Signals**_ 

The LATCHCLR signal holds the digital filter, synchronization block, and the latch output in reset (0) after the required delays. The LATCHCLR signal is activated in software using xLATCHCLR (x = H or L). The LATCHCLR signal can also be activated by EPWMSYNCPER when xSYNCCLREN (x = H or L) is set. If a longer LATCHCLR signal is required, the EPWMBLANK signal can be used to extend the LATCHCLR signal by setting BLANKEN. 

EPWMSYNCPER and EPWMBLANK (BLANKWDW) come from the Time-Base and Digital Compare submodules of the EPWM, respectively. For a detailed description of how these two signals are generated, refer to the respective submodule section in the _Enhanced Pulse Width Modulator (ePWM)_ chapter 

The EPWMSYNCPER signal that loads DACxVALA when COMPDACCTL [SWLOADSEL] = 1 is a level trigger load. If TBCTR and TBPRD of the EPWM are both 0, EPWMSYNCPER is held at level high and DACxVALA is loaded immediately from DACxVALS irrespective of the value of COMPDACCTL [SWLOADSEL]. Due to this, configure the EPWM first before setting COMPDACCTL [SWLOADSEL] to 1. 

## **Note** 

The name of the sync signal that the CMPSS receives from the EPWM has been updated from PWMSYNC to EPWMSYNCPER (SYNCPER/PWMSYNCPER/EPWMxSYNCPER) to avoid confusion with the other EPWM sync signals EPWMSYNCINEN and EPWMSYNCOUTEN. For a description of what are these signals, see the _Enhanced Pulse Width Modulator (ePWM)_ chapter. 

## _**7.5.4.6.2 Synchronizer, Digital Filter, and Latch Delays**_ 

The synchronization block adds a delay of 1-2 sysclks. If the digital filter is bypassed (all filter settings are 0), the digital filter adds a delay of 2 sysclks. The latch adds 1 sysclk delay. 

628 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.4.6.3 Calibrating the CMPSS Trip Levels**_ 

The CMPSS has two sources of offset errors: comparator offset error and compdac offset error. In the data sheet the comparator offset error is referred to as _**Input referred offset error**_ and compdac offset error is referred to as _**Static offset error**_ . See the device data sheet for their values. 

If both inputs of the comparator are driven from a pin, only the comparator offset error applies. However if the inverting input of the comparator is driven from the compdac, then only the compdac offset error applies. This is because the compdac offset error includes comparator offset error. 

Due to the offset errors, the CMPSS must be calibrated to make sure trips happen at the expected levels. The following flow outlines how the calibration can be performed if the inverting input of the comparator is driven from the compdac. 

Notes before calibration: 

1. A static DC signal is required on the non-inverting input of the comparator. 

2. Hysteresis can be disabled for calibration and can be re-enabled after calibration is complete. 

3. A noisy input can make calibration difficult, so use the latch with non-zero filter settings depending on how noisy is the signal on the non-inverting input. 

This approach sweeps down the compdac: 

1. Set the starting compdac value to max, 0xFFF. 

   - Optional: Instead of setting the starting compdac value to maximum, set to _**Vtarget**_ + _**Static offset error**_ + _**Margin**_ . Where _**Vtarget**_ is the approximate DC voltage on the non-inverting input, _**Static offset error**_ is the compdac offset error specification and _**Margin**_ is some amount of guard band. This can lead to a faster calibration but only works if _**Vtarget**_ is known. Alternatively, if _**Vtarget**_ is unknown, the ADC can be used to convert _**Vtarget**_ . 

2. Decrement compdac value by 1. 

3. Wait for compdac to settle. 

4. Clear latch. 

5. Wait for possible latch set. 

6. If latch is set, trip code is found exit. 

   - Optional: The trip code can be double checked by: 

      - a. Increasing compdac value by 1. 

      - b. Clear latch. 

      - c. Wait for possible latch set. 

      - d. Latch can be unset. 

7. If latch is unset, go back to step 2 and repeat. 

It is also possible to calibrate the CMPSS, if both inputs of the comparator are driven from a pin. For this case, the flow stays the same but the voltage on the inverting pin of the comparator is swept externally. 

## _**7.5.4.6.3.1 CMPSS Hysteresis**_ 

The CMPSS DAC is used as the reference to determine how much hysteresis to apply. Therefore, hysteresis scales with the CMPASS DAC reference voltage. 

Hysteresis can be disabled for calibration, and Hysteresis can be re-enabled after calibration is complete through COMPLHYS and COMPHHYS. Each of these is a 4 bit field of CMPSS CONFIG1 registers, and bit 2 of the field follow the behavior shown in Figure 7-172 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 629 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [242 x 163] intentionally omitted <==**

**Figure 7-172. Bit 2 Crossing** 

## **7.5.4.7 Enabling and Disabling the CMPSS Clock** 

If the clock to the CMPSS module is disabled while the comparator is active, the following behavior can be expected: 

- The comparator remains unaffected and continues to trip from voltages on the inputs. 

- If the reference 12-bit DAC is driving the negative input of the comparator, the voltage on the negative input remains static and unaffected but DACVALA can no longer be updated from the ramp generator or DACVALS. 

- The ramp generator, synchronize block and digital filter freeze on their current states. 

Enabling the clock to the CMPSS restores the clock to the state before the clock was disabled. 

## **7.5.4.8 CMPSS Programming Guide** 

## **Driver Information** 

Driver features are available at the CMPSS driver page. 

## **Software API Information** 

The CMPSS driver provides an API to configure the CMPSS module. Full documentation is located on APIs for CMPSS 

## **Example Usage** 

The below links shows an example on how to use CMPSS 

- CMPSS Asynchronous trip 

630 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.5 Buffered Digital-to-Analog Converter (DAC)**_ 

The buffered digital-to-analog converter (DAC) is an analog module that can output a programmable, arbitrary reference voltage. 

**7.5.5.1 Introduction** ..................................................................................................................................................632 **7.5.5.2 Using the DAC** ............................................................................................................................................. 632 **7.5.5.3 Lock Registers** .............................................................................................................................................634 **7.5.5.4 DAC Programming Guide** ........................................................................................................................... 634 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

631 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.5.1 Introduction** 

The buffered DAC module consists of an internal 12-bit DAC and an analog output buffer that is capable of driving an external load. For driving even higher loads than typical, a trade-off can be made between load size and output voltage swing. For the load conditions of the buffered DAC, see the device-specific data sheet. The buffered DAC can be used as a general-purpose DAC to generate a DC voltage in addition to AC waveforms such as sine waves, square waves, triangle waves and so forth. Software writes to the DAC value register can take effect immediately or can be synchronized with EPWMSYNCPER events. 

## _**7.5.5.1.1 DAC Features**_ 

Each buffered DAC has the following features: 

- 12-bit programmable internal DAC 

- Selectable reference voltage source 

- x1 and x2 gain modes when using internal VREFHI 

- Pull-down resistor on output 

- Ability to synchronize with EPWMSYNCPER 

## _**7.5.5.1.2 Block Diagram**_ 

The block diagram for the buffered DAC is shown in Figure 7-173. 

**==> picture [499 x 144] intentionally omitted <==**

**----- Start of picture text -----**<br>
DACCTL.DACREFSEL<br>DACVREF[1:0] 0 DACREF<br>VDDA18_LDO 1<br>VDDA1V8<br>DACCTL.LOADMODE<br>SYSCLK CLK<br>EPWM0SYNCPER 0 DACVALS D Q 0<br>EPWM1SYNCPER 1 DACVALA Offset DACVAL 12-bit  BufferOutput DACOUT<br>EPWM2SYNCPER 2 EPWM SYNC CLK Q 1 Correction DAC Buffer<br>D<br>EPWMnSYNCPER N-1 EFUSE_OVERRIDE_DAC_TRIM[2:0] VSSA VSSA VSSA<br>DACCTL.SYNCSEL Default Calibrated Trim<br>OFFSET_TRIM<br>EFUSE_OVERRIDE_DAC_TRIM<br>**----- End of picture text -----**<br>


**Figure 7-173. DAC Module Block Diagram** 

## **7.5.5.2 Using the DAC** 

As seen in Figure 7-173 two sets of DACVAL registers, DACVALA and DACVALS, are present in the buffered DAC module. DACVALA is a read-only register that actively controls the buffered DAC value. DACVALS is a writable shadow register that loads into DACVALA either immediately or synchronized with the next EPWMSYNCPER event. DACVALA update source is selected by the CONTROLSS_DAC0_DACCTL register LOADMODE bit. The power-on default of LOADMODE = 0, which selects the immediate update mode. 

## **Note** 

If the clock to the buffered DAC is disabled while the buffered DAC is outputting a voltage, the output voltage remains unaffected, but DACVALA and DACVALS is no longer updated with register writes. Enabling the clock to the buffered DAC restores the DAC to the state before the clock was disabled. 

The internal DAC reference voltage source, DACREF, is selectable between DACVREF and VDDA18_LDO. The CONTROLSS_DAC0 register DACREFSEL bit selects between these two VREF sources. The DACVREF source routes to the DACVREF pins of the device. The VDDA18_LDO source selects an internal route to the on-die 1.8V analog LDO output. In all normal applications the DACVREF pins must be used as the VREF source. The VDDA18_LDO VREF source option is present only for diagnostic or debug purposes. The power-on default of DACREFSEL = 0, which selects the DACVREF source pins. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

632 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

Before the selected DACVALA register value is applied to the DAC, an additional calibration offset value is applied. During production DACOUT is calibrated to a nominal 1.8V VREF source offset with the calibration offset stored in e-fuse for use by the buffered DAC. The power-on default options select this pre-calibrated offset value. 

Assuming this pre-calibrated, default offset value is used, the output voltage DACOUT (in volts) is calculated with the following equation: 

**==> picture [446 x 15] intentionally omitted <==**

See the below Section 7.5.5.2.2 for more information on the DAC offset adjustment. 

## **Note** 

The output buffer of the buffered DAC can exhibit non-linear behavior near the supply rails (VDDA18/ VSSA). To determine the linear range of the buffered DAC, see the device-specific data sheet. 

## _**7.5.5.2.1 Initialization Sequence**_ 

The following sequence of steps are required to setup the buffered DAC for basic operation. 

1. Enable the buffered DAC clock. See Clock Selection for CONTROLSS_PLL clock controls. 

2. Select the DACREF source with DACREFSEL bit in the DACCTL register. 

3. Power up the buffered DAC with DACOUTEN in the CONTROLSS_DAC0_DACOUTEN register. 

4. Wait for the power-up time to elapse before writing a new voltage value into the CONTROLSS_DAC0_DAC_DACVALS register. See the device-specific data sheet to determine the powerup time of the buffered DAC. 

## **Note** 

For predictable behavior of the buffered DAC, two consecutive writes to DACVALS must not be spaced greater than 1024 codes apart. Consecutive DACVALS values that are within 1024 codes allow for the required settling time of the buffered DAC. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 633 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.5.2.2 DAC Offset Adjustment**_ 

Zero offset error is defined as the difference between the voltage at midcode (2048) and 1.25v (for 2.5v reference voltage). DAC offset error is calibrated at 2.5v reference voltage and loaded into the DAC offset trim register by default If the DAC is used at any reference voltage other than 2.5v, the offset trim must be adjusted to make sure the offset error performance stays within the device-specific data manual limits. The DAC offset register is a 16-bit register that contains the 8-bit signed offset trim in the lower half of the register. Use the function call DAC_tuneOffsetTrim(). 

## _**7.5.5.2.3 EPWMSYNCPER Signal**_ 

The EPWMSYNCPER signal comes from the Time-Base submodule of the EPWM. For a detailed description of how this signal is generated, refer to Enhanced Pulse Width Modulator (ePWM). 

When DACCTL.LOADMODE = 1, the selected EPWMSYNCPER signal loads a new DACVALA value. The EPWMSYNCPER signal operates as a high logic-level trigger load. If TBCTR and TBPRD of the EPWM are both 0, EPWMSYNCPER is held at a high level and DACVALA is immediately loaded from DACVALS irrespective of the value of DACCTL.LOADMODE. To control the timing of this initial EPWMSYNCPER triggered load the EPWM and EPWMSYNCPER output must be configured prior to setting DACCTL.LOADMODE = 1. 

## **Note** 

When using EPWMSYNCPER to load in new DACVALA values, unexpected value changes can be observed in the DAC active value register and resulting DAC output. In this case, the DACVALA register is likely receiving an intermediate value. The DACVALA register takes on the full programmed value after 1 or more EPWM periods. Dividing the EPWM clock by 2, 4, or 8, to reduce the period and can resolve this issue. 

## **7.5.5.3 Lock Registers** 

The CONTROLSS_DAC0_DACLOCK register is provided to prevent spurious writes from modifying the CONTROLSS_DAC0_DACCTL, CONTROLSS_DAC0_DACVALS, and CONTROLSS_DAC0_DACOUTEN registers. Once a register is protected through CONTROLSS_DAC0_DACLOCK, write access are locked out until the device is reset. 

## **Note** 

Once a CONTROLSS_DAC0_DACLOCK field is set, only a full power on reset of the device is required to clear the lock and enable modification of the locked register. 

## **7.5.5.4 DAC Programming Guide** 

## **Drive Information** 

Driver features are available at the DAC driver page. 

## **Software API Information** 

The DAC driver provides an API to configure the DAC module. Full documentation is located on APIs for DAC. 

## **Example Usage** 

The below links show examples on how to use DAC 

- DAC Constant Voltage 

- DAC Ramp Wave 

- DAC Random Voltage 

- DAC Sine DMA 

- DAC Sine Wave 

- DAC Square Wave 

634 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6 Enhanced Pulse Width Modulator (ePWM)**_ 

The enhanced pulse width modulator (ePWM) peripheral is a key element in controlling many of the power electronic systems found in both commercial and industrial equipment. These systems include digital motor control, switch mode power supply control, uninterruptible power supplies (UPS), and other forms of power conversion. The ePWM peripheral can also perform a digital-to-analog (DAC) function, where the duty cycle is equivalent to a DAC analog value; it is sometimes referred to as a power DAC. 

This chapter is applicable for ePWM type 5. Type 5 EPWM is fully compatible with type 4 EPWM. 

**7.5.6.1 Introduction** ..................................................................................................................................................636 **7.5.6.2 EPWM Integration** ........................................................................................................................................644 **7.5.6.3 ePWM Modules Overview** ........................................................................................................................... 644 **7.5.6.4 Time-Base (TB) Submodule** ........................................................................................................................646 **7.5.6.5 Counter-Compare (CC) Submodule** ...........................................................................................................663 **7.5.6.6 Action-Qualifier (AQ) Submodule** .............................................................................................................. 669 **7.5.6.7 Dead-Band Generator (DB) Submodule** .................................................................................................... 682 **7.5.6.8 Minimum Dead-Band (MINDB) + Illegal Combination Logic (ICL) Submodules** ....................................689 **7.5.6.9 PWM Chopper (PC) Submodule** .................................................................................................................693 **7.5.6.10 Trip-Zone (TZ) Submodule** ........................................................................................................................697 **7.5.6.11 Diode Emulation (DE) Submodule** ........................................................................................................... 704 **7.5.6.12 Event-Trigger (ET) Submodule** .................................................................................................................710 **7.5.6.13 Digital Compare (DC) Submodule** ............................................................................................................715 **7.5.6.14 XCMP Submodule** ......................................................................................................................................728 **7.5.6.15 High-Resolution Pulse Width Modulator (HRPWM)** ............................................................................... 736 **7.5.6.16 ePWM Crossbar (XBAR)** ........................................................................................................................... 759 **7.5.6.17 Applications to Power Topologies** ...........................................................................................................760 **7.5.6.18 EPWM Programming Guide** ......................................................................................................................778 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 635 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.6.1 Introduction** 

This chapter includes an overview and information about each submodule: 

- Time Base (TB) Submodule 

- Counter Compare (CC) Submodule 

- Action Qualifier (AQ) Submodule 

- Dead-Band Generator (DB) Submodule 

- PWM Chopper (PC) Submodule 

- Trip Zone (TZ) Submodule 

- Diode Emulation (DE) Submodule 

- Minimum Dead-Band (MINDB) and Illegal Combo Logic (ICL) Submodule 

- Event Trigger (ET) Submodule 

- Digital Compare (DC) Submodule 

An effective PWM peripheral must be able to generate complex pulse width waveforms with minimal CPU overhead or intervention and must be highly programmable and very flexible while being easy to understand and use. The ePWM unit described here addresses these requirements by allocating all needed timing and control resources on a per PWM channel basis. Cross coupling or sharing of resources has been avoided; instead, the ePWM is built up from smaller single channel submodules with separate resources that can operate together as required to form a system. This modular approach results in an orthogonal architecture and provides a more transparent view of the peripheral structure, helping users to understand the operation quickly. 

In this document, the letter x within a signal or submodule name is used to indicate a generic ePWM instance on a device. For example, output signals EPWMxA and EPWMxB refer to the output signals from the ePWMx instance. Thus, EPWM1A and EPWM1B belong to ePWM1 and likewise EPWM4A and EPWM4B belong to ePWM4. 

The ePWM Type 5 is functionally compatible to Type 4. Type 5 has the following enhancements in addition to the Type 4 features: 

- **PWM SYNC Related Enhancements:** Additional external sync option is added in to the EPWMSYNCSEL register. This allows for the configuration of up to 3 independent sync chains with external sync options. 

- **Linking and Global Load Enhancements:** DBRED:DBREDHR and DBREDHR and DBFED:DBFEDHR have the ability to be linked across ePWM modules. 

Global load pulse selection for shadow to active load can now occur when the time-base counter equals CMPCU, CMPCD, CMPDU, or CMPDD. 

- **XCMP Complex Waveform Generator:** XCMP mode has been added to allow for generation of multiple ePWM pulses, with high resolution, in a given ePWM cycle. Up to 8 new compare registers are added to achieve this functionality. 

- **Digital Compare Submodule Enhancements:** Event detection within the digital compare capture module is able to detect an occurrence of a trip event in a configured time window. 

Pulse selection for blanking and capture alignment now includes a blanking window mix selection (BLANKPULSEMIX). This is added for LLC topologies where blanking window settings need to be changed on the fly - providing greater configurability to do this. 

- **Trip-Zone Submodule Enhancements:** A CAPEVENT signal can generate a CBC or One-shot trip event. 

- • **Diode Emulation Submodule:** The diode emulation mode was added to provide hardware features and the necessary hooks into other IPs to implement a robust diode mode sense and control in a noisy environment. 

- **Minimum Dead-Band and Illegal Combo Logic Submodule:** The minimum dead-band logic was added to provide the ability to configure the minimum dead-band duration between a complimentary set of ePWMs. 

- To detect and make sure that under no circumstances, the ePWM states result in potentially hazardous combinations, a Look Up Table (LUT) has been added that can be used to re-configure the ePWM outputs. 

- • **Event Trigger Submodule Enhancements:** To enable unevenly spaced over-sampling of the ePWM period, the event trigger module trigger select is modified such that multiple events can trigger SOCA, SOCB, and INT events (ETINTMIX). 

636 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- **OTTO-HRPWM Enhancement:** OTTO-HRPWM module now has 3 additional delay lines for CMPBHR, DBREDHR, DBFEDHR 

**Table 7-151. OTTOCAL to EPWM instance mapping** 

|**OTTOCAL Instance**|**EPWM Instance**|
|---|---|
|OTTOCAL0|EPWM[0-7]|
|OTTOCAL1|EPWM[8-15]|
|OTTOCAL2|EPWM[16-23]|
|OTTOCAL3|EPWM[24-31]|



The ePWM Type 4 is functionally compatible to Type 2 (a Type 3 does not exist). Type 4 has the following enhancements in addition to the Type 2 features: 

- **Register Address Map:** Additional registers are required for new features on ePWM Type 4. The ePWM register address space has been remapped for better alignment and easy usage. 

- **Delayed Trip Functionality:** Changes have been added to achieve deadband insertion capabilities to support, for example, delayed trip functionality needed for peak current mode control type application scenarios. This has been accomplished by allowing comparator events to go into the Action Qualifier as a trigger event (Events T1 and T2). If comparator T1 / T2 events are used to edit the PWM, changes to the PWM waveform do not take place immediately. Instead, the waveform synchronizes to the next TBCLK. 

- **Dead-Band Generator Submodule Enhancements:** Shadowing of the DBCTL register to allow dynamic configuration changes. 

- **One Shot and Global Load of Registers:** The ePWM Type 4 allows one shot and global load capability from shadow to active registers to avoid partial loads in, for example, multiphase applications. ePWM Type 4 also allows a programmable prescale of shadow to active load events. ePWM Type 4 Global Load can simplify ePWM software by removing interrupts and ensuring that all registers are loaded at the same time. 

- **Trip-Zone Submodule Enhancements:** Independent flags have been added to reflect the trip status for each of the TZ sources. Changes have been made to the trip-zone submodule to support certain power converter switching techniques like valley switching. 

- **Digital Compare Submodule Enhancements:** Blanking window filter register width has been increased from 8 to 16 bits. DCCAP functionality has been enhanced to provide more programmability. 

- **PWM SYNC Related Enhancements:** The ePWM Type 4 allows PWM SYNCOUT generation based on CMPC and CMPD events. These events can also be used for PWMSYNC pulse selection. 

The ePWM Type 2 is fully compatible to Type 1. Type 2 has the following enhancements in addition to the Type 1 features: 

- **High-Resolution Dead-Band Capability:** High-resolution capability is added to dead-band RED and FED in half-cycle clocking mode. 

- **Dead-Band Generator Submodule Enhancements:** The ePWM Type 2 has features to enable both RED and FED on either PWM outputs. Provides increased dead band with 14-bit counters and dead-band / dead-band high-resolution registers are shadowed 

- **High-Resolution Extension available on ePWMxB outputs:** Provides the ability to enable high-resolution period and duty cycle control on ePWMxB outputs. This is discussed in more detail in High-Resolution Pulse Width Modulator (HRPWM). 

- **Counter Compare Submodule Enhancements:** The ePWM Type 2 allows interrupts and SOC events to be generated by additional counter compares CMPC and CMPD. 

- **Event Trigger Submodule Enhancements:** Prescaling logic to issue interrupt requests and ADC start of conversion expanded up to every 15 events. It allows software initialization of event counters on SYNC event. 

- • **Digital Compare Submodule Enhancements:** Digital Compare Trip Select logic [DCTRIPSEL] has up to 12 external trip sources selected by the Input X-BAR logic in addition to an ability to OR all of them (up to 14 [external and internal sources]) to create the respective DCxEVTs. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 637 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- **Simultaneous Writes to TBPRD and CMPx Registers:** This feature allows writes to TBPRD, CMPA:CMPAHR, CMPB:CMPBHR, CMPC and CMPD of any ePWM module to be tied to any other ePWM module, and also allows all ePWM modules to be tied to a particular ePWM module if desired. 

- **Shadow to Active Load on SYNC of TBPRD and CMP Registers:** This feature supports simultaneous writes of TBPRD and CMPA/B/C/D registers. 

The ePWM Type 1 is fully compatible to Type 0. Type 1 has the following enhancements in addition to the Type 0 features: 

- **Increased Dead-Band Resolution:** Dead-band clocking has been enhanced to allow half-cycle clocking to double resolution. 

- **Enhanced Interrupt and SOC Generation:** Interrupts and ADC start-of-conversion can now be generated on both the TBCTR == zero and TBCTR == period events. This feature enables dual edge PWM control. Additionally, the ADC start-of-conversion can be generated from an event defined in the digital compare submodule. 

- **High-Resolution Period Capability:** Provides the ability to enable high-resolution period. This is discussed in more detail in High-Resolution Pulse Width Modulator (HRPWM). 

- **Digital Compare Submodule:** The digital compare submodule enhances the event triggering and trip zone submodules by providing filtering, blanking and improved trip functionality to digital compare signals. Such features are essential for peak current mode control and for support of analog comparators. 

## **Note** 

The name of the sync signal that goes to the CMPSS has been updated from PWMSYNC to EPWMSYNCPER (SYNCPER/PWMSYNCPER/EPWMxSYNCPER) to avoid confusion with the other EPWM sync signals EPWMSYNCI and EPWMSYNCO. For a description of these signals, see Table 7-153. 

## _**7.5.6.1.1 EPWM Related Collateral**_ 

## **Foundational Materials** 

- C2000 Academy - EPWM 

- _Real-Time Control Reference Guide_ 

   - Refer to the EPWM section 

## **Getting Started Materials** 

- _C2000 ePWM Developer's Guide Application Report_ 

- Enhanced Pulse Width Modulator (ePWM) Training for C2000 MCUs (Video) 

- _Flexible PWMs Enable Multi-Axis Drives, Multi-Level Inverters Application Report_ 

- Getting Started with the C2000 ePWM Module (Video) 

- _Using PWM Output as a Digital-to-Analog Converter on a TMS320F280x Digital Signal Control Application Report_ 

   - Chapters 1 to 6 are Fundamental material, derivations, and explanations that are useful for learning about how PWM can be used to implement a DAC. Subsequent chapters are Getting Started and Expert material for implementing in a system. 

- _Using the Enhanced Pulse Width Modulator (ePWM) Module Application Report_ 

## **Expert Materials** 

- C2000 real-time microcontrollers - Reference designs 

   - See TI designs related to specific end applications used. 

- _Leverage New Type ePWM Features for Multiple Phase Control Application Report_ 

638 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.1.2 Submodule Overview**_ 

The ePWM module represents one complete PWM channel composed of two PWM outputs: EPWMxA and EPWMxB. Multiple ePWM modules are instanced within a device as shown in _Multiple ePWM Modules_ Each ePWM instance is identical with one exception. Some instances include a hardware extension that allows more precise control of the PWM outputs. This extension is the high-resolution pulse width modulator (HRPWM) and is described in High-Resolution Pulse Width Modulator (HRPWM). See the device data sheet to determine which ePWM instances include this feature. Each ePWM module is indicated by a numerical value starting with 0. For example, ePWM0 is the first instance and ePWM2 is the third instance in the system and ePWMx indicates any instance. 

The ePWM modules are chained together by way of a clock synchronization scheme that allows them to operate as a single system when required. Additionally, this synchronization scheme can be extended to the capture peripheral submodules (eCAP). The number of submodules is device-dependent and based on target application needs. Submodules can also operate standalone. 

Each ePWM module supports the following features: 

- Dedicated 16-bit time-base counter with period and frequency control 

- Two PWM outputs (EPWMxA and EPWMxB) that can be used in the following configurations: 

   - Two independent PWM outputs with single-edge operation 

   - Two independent PWM outputs with dual-edge symmetric operation 

   - One independent PWM output with dual-edge asymmetric operation 

- Asynchronous override control of PWM signals through software. 

- Programmable phase-control support for lag or lead operation relative to other ePWM modules. 

- Hardware-locked (synchronized) phase relationship on a cycle-by-cycle basis. 

- Dead-band generation with independent rising and falling edge delay control. 

- Programmable trip zone allocation of both cycle-by-cycle trip and one-shot trip on fault conditions. 

- A trip condition can force either high, low, or high-impedance state logic levels at PWM outputs. 

- All events can trigger both CPU interrupts and ADC start of conversion (SOC) 

- Programmable event prescaling minimizes CPU overhead on interrupts. 

- PWM chopping by high-frequency carrier signal, useful for pulse transformer gate drives. 

Each ePWM module is connected to the input/output signals shown in Figure 7-175. The signals are described in detail in subsequent sections. 

Each ePWM module consists of eight submodules and is connected within a system by way of the signals shown in Figure 7-175. The order in which the ePWM modules are connected can differ from what is shown in the figure. See Time-Base Counter Synchronization for the synchronization scheme for a particular device. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

639 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [492 x 475] intentionally omitted <==**

**Figure 7-174. Multiple ePWM Modules** 

640 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [446 x 397] intentionally omitted <==**

**Figure 7-175. Submodules and Signal Connections for an ePWM Module** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 641 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

Figure 7-176 shows more internal details of a single ePWM module. The main signals used by the ePWM module are: 

- **PWM output signals (EPWMxA and EPWMxB)** 

The PWM output signals are made available external to the device 

- **Trip-zone signals (TZ1 to TZ6)** 

These input signals alert the ePWM module of fault conditions external to the ePWM module. Each submodule on a device can be configured to either use or ignore any of the trip-zone signals 

- **Time-base synchronization input (EPWMxSYNCI), output (EPWMxSYNCO), and peripheral (EPWMxSYNCPER) signals** 

For more information, see _Time-Base Counter Synchronization_ 

Each ePWM module also generates another PWMSYNC signal called EPWMxSYNCPER. EPWMxSYNCPER goes to the CMPSS for synchronization purposes. Functionality is configured using the HRPCTL register, but has no relation with the HRPWM. For more information on how EPWMxSYNCPER is used by the CMPSS, see their respective chapters. 

- **ADC start-of-conversion signals (EPWMxSOCA and EPWMxSOCB)** 

Each ePWM module has two ADC start of conversion signals. Any ePWM module can trigger a start of conversion. Whichever event triggers the start of conversion is configured in the event-trigger submodule of the ePWM. 

- **Comparator output signals (COMPxOUT)** 

Output signals from the comparator module can be fed through EPWM X-BAR to one or all of the and in conjunction with the trip zone signals can generate digital compare events. 

- **Peripheral bus** 

The peripheral bus is 32-bits wide and allows both 16-bit and 32-bit writes to the ePWM register file. 

642 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [496 x 544] intentionally omitted <==**

**----- Start of picture text -----**<br>
|||||||
|---|---|---|---|---|---|
|Time-Base (TB)|
|TBPRD Shadow (24)|EXTSYNCIN|ePWM|EXTSYNCOUT|
|TBPRDHR (8)|SYNC|
|TBPRD Active (24)|Scheme|
|CTR=PRD|
|EPWMxSYNCI|
|TBCTL[PHSEN]|
|TBCTL[SWFSYNC]|
|Counter|DCAEVT1/sync|[(A)]|
|Up/Down|
|(16 bit)|DCBEVT1/sync|[(A)]|
|CTR=ZERO|
|TBCTR|CTR=PRD|EPWMx_INT|
|Active (16)|CTR_Dir|CTR=ZERO|
|TBPHSHR (8)|CTR=PRD or ZERO|EPWMxSOCA|
|16|8|CTR=CMPA|Event|On-chip|
|Phase|CTR=CMPB|Trigger|EPWMxSOCB|ADC|
|TBPHS Active (24)|Control|CTR=CMPC|And|
|Interrupt|
|CTR=CMPD|(ET)|ADCSOCOUTSELECT|
|Counter Compare (CC)|CTR_Di|r|
|DCAEVT1.soc|[(A)]|
|Select and pulse stretch|
|DCBEVT1.soc|[(A)]|for external ADC|
|Action|
|CTR=CMPA|Qualifier|Input|ADCSOCAO|
|ADCSOCBO|
|(AQ)|XBAR|
|CMPAHR (8)|MINDB|ICL XBAR|
|16|HiRes PWM (HRPWM)|XBAR|
|CMPAHR (8)|
|CMPA Active (24)|
|ePWMxA|
|CMPA Shadow (24)|EPWMA|
|CTR=CMPB|Dead|PWM|Trip|Diode|Minimum Dead-|
|Band|Chopper|Zone|Emulation|band|
|CMPBHR (8)|(DB)|(DB)|(TZ)|(DE)|(MINDB) and Illegal Combo Logic (ICL)|
|16|
|CMPB Active (16)|EPWMB|ePWMxB|
|CMPB Shadow (16)|
|CMPBHR (8)|
|EPWMA_DB_NO_HR|EPWMA_DE_NO_HR|
|TBCNT (16)|CTR=CMPC|
|EPWMB_DB_NO_HR|EPWMB_DE_NO_HR|
|CMPC[15-0]|16|EPWMx_TZ_INT|
|CTR=ZERO|
|TZ1 to TZ3|
|CMPC Active (16)|DCAEVT1.inter|
|EMUSTOP|
|CMPC Shadow (16)|DCBEVT1.inter|
|CLOCKFAIL|
|DCAEVT2.inter|
|EQEPxERR|
|TBCNT (16)|CTR=CMPD|DCBEVT2.inter|
|CAPEVT.inter|DCAEVT1.force|[(A)]|
|DCBEVT1.force|[(A)]|
|CMPD[15-0]|16|
|DCAEVT2.force|[(A)]|
|CMPD Active (16)|DCBEVT2.force|[(A)]|
|CMPD Shadow (16)|

**----- End of picture text -----**<br>


A. These events are generated by the ePWM Digital Compare (DC) submodule based on the levels of the TRIPIN inputs. 

## **Figure 7-176. ePWM Modules and Critical Internal Signal Interconnects** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

643 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.6.2 EPWM Integration** 

There are 32x EPWM modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**Figure 7-177. ePWM Integration Diagram** 

**==> picture [500 x 304] intentionally omitted <==**

## **7.5.6.3 ePWM Modules Overview** 

8 submodules are included in every ePWM peripheral. Each of these submodules performs specific tasks that can be configured by software. 

Table 7-152 lists the key submodules together with a list of their main configuration parameters. For example, if you need to adjust or control the duty cycle of a PWM waveform, see the counter-compare submodule in Section 7.5.6.5 for relevant details. 

644 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-152. Submodule Configuration Parameters** 

|**Submodule**|**Configuration Parameter or Option**|**Configuration Parameter or Option**|
|---|---|---|
|Time Base (TB)|•|Scale the time-base clock (TBCLK) relative to the ePWM clock (EPWMCLK).|
||•|Configure the PWM time-base counter (TBCTR) frequency or period.|
||•|Set the mode for the time-base counter:|
|||–<br>count-up mode: used for asymmetric PWM|
|||–<br>count-down mode: used for asymmetric PWM|
|||–<br>count-up-and-down mode: used for symmetric PWM|
||•|Configure the time-base phase relative to another ePWM module.|
||•|Synchronize the time-base counter between modules through hardware or software.|
||•|Configure the direction (up or down) of the time-base counter after a synchronization event.|
||•|Simultaneous writes to the TBPRD registers on all PWM's corresponding to the configuration on|
|||EPWMXLINK.|
||•|Configure how the time-base counter behaves when the device is halted by an emulator.|
||•|Specify the source for the synchronization output of the ePWM module|
||•|Configure one shot and global load of registers in this module.|
|Counter Compare (CC)|•|Specify the PWM duty cycle for output EPWMxA and output EPWMxB|
||•|Specify the time at which switching events occur on the EPWMxA or EPWMxB output|
||•|Specify the programmable delay for interrupt and SOC generation with additional comparators|
||•|Simultaneous writes to the CMPA, CMPB, CMPC, CMPD registers on all PWM's corresponding to the|
|||configuration on EPWMXLINK.|
||•|Configure one shot and global load of registers in this module.|
||•|Generate up to four pulses in one ePWM period through the complex waveform (XCMP) mode feature|
|Action Qualifier (AQ)|•|Specify the type of action taken when a time-base counter-compare, trip-zone submodule, or comparator|
|||event occurs:|
|||–<br>No action taken|
|||–<br>Output EPWMxA and EPWMxB switched high|
|||–<br>Output EPWMxA and EPWMxB switched low|
|||–<br>Output EPWMxA and EPWMxB toggled|
||•|Force the PWM output state through software control|
||•|Configure and control the PWM dead band through software|
||•|Configure one shot and global load of registers in this module.|
|Dead-Band Generator|•|Control of traditional complementary dead-band relationship between upper and lower switches|
|(DB)|•|Specify the output rising-edge-delay value|
||•|Specify the output falling-edge delay value|
||•|Bypass the dead-band module entirely. In this case the PWM waveform is passed through without|
|||modification.|
||•|Option to enable half-cycle clocking for double resolution.|
||•|Allow EPWMxB phase shifting with respect to the EPWMxA output.|
||•|Configure one shot and global load of registers in this module.|
||•|Simultaneous writes to the DBRED, DBREDHR, DBFED, DBFEDHR registers on all PWM's corresponding|
|||to the configuration on EPWMXLINK2.|
|PWM Chopper (PC)|•|Create a chopping (carrier) frequency.|
||•|Pulse width of the first pulse in the chopped pulse train.|
||•|Duty cycle of the second and subsequent pulses.|
||•|Bypass the PWM chopper module entirely. In this case the PWM waveform is passed through without|
|||modification.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 645 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-152. Submodule Configuration Parameters (continued)** 

|**Submodule**|**Configuration Parameter or Option**|**Configuration Parameter or Option**|
|---|---|---|
|Trip Zone (TZ)|•|Configure the ePWM module to react to one, all, or none of the trip-zone signals or digital compare events.|
||•|Specify the trip action taken when a fault occurs:|
|||–<br>Force EPWMxA and EPWMxB high|
|||–<br>Force EPWMxA and EPWMxB low|
|||–<br>Force EPWMxA and EPWMxB to a high-impedance state|
|||–<br>Configure EPWMxA and EPWMxB to ignore any trip condition.|
||•|Configure how often the ePWM reacts to each trip-zone signal:|
|||–<br>One-shot|
|||–<br>Cycle-by-cycle|
||•|Enable the trip-zone to initiate an interrupt.|
||•|Bypass the trip-zone module entirely.|
||•|Programmable option for cycle-by-cycle trip clear|
||•|If desired, independently configure trip actions taken when time-base counter is counting down.|
|Diode Emulation|•|Choose any of the comparator outputs as trips to detect entry into DE mode.|
||•|Monitor the DE mode duration and generate a trip event to PWMs.|
||•|Ability to switch the comparator thresholds, dynamically in hardware upon DE mode entry.|
||•|Cycle-by-cycle and one-shot modes of clearing/de-evaluating the DE condition.|
|Minimum Dead-|•|Add a minimum amount of delay between ePWM channels|
|Band(MINDB) and Illegal<br>Combo Logic (ICL)|•|Define non-supported output combinations and drive output high or low if combination occurs|
|Event Trigger (ET)|•|Enable the ePWM events that trigger an interrupt.|
||•|Enable ePWM events that trigger an ADC start-of-conversion event.|
||•|Specify the rate at which events cause triggers (every occurrence or every 2nd or up to 15th occurrence)|
||•|Poll, set, or clear event flags|
|Digital Compare (DC)|•|Enables comparator (COMP) module outputs and trip zone signals which are configured using the Input|
|||X-BAR to create events and filtered events|
||•|Specify event-filtering options to capture TBCTR counter, generate blanking window, or insert delay in|
|||PWM output or time-base counter based on captured value.|



## **7.5.6.4 Time-Base (TB) Submodule** 

Each ePWM module has their own time-base submodule that determines all of the event timing for the ePWM module. Built-in synchronization logic allows the time-base of multiple ePWM modules to work together as a single system. 

Figure 7-178 illustrates the time-base submodule within the ePWM. 

646 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [500 x 271] intentionally omitted <==**

**Figure 7-178. Time-Base Submodule** 

## _**7.5.6.4.1 Purpose of the Time-Base Submodule**_ 

The time-base submodule can be configured for the following: 

- Specify the ePWM time-base counter (TBCTR) frequency or period to control how often events occur. 

- Manage time-base synchronization with other ePWM modules. 

- Maintain a phase relationship with other ePWM modules. 

- Set the time-base counter to count-up, count-down, or count-up-and-down mode. 

- Generate the following events: 

   - CTR = PRD: Time-base counter equal to the specified period (TBCTR = TBPRD). 

   - CTR = Zero: Time-base counter equal to zero (TBCTR = 0x00). 

- Configure the rate of the time-base clock; a prescaled version of the ePWM clock (EPWMCLK). This allows the time-base counter to increment/decrement at a slower rate. 

## **Note** 

If required by the application code to update the TBCTR value through software while the TBCTR is counting, note that the time-base module needs at least 1 TBCLK cycle for the time-base related events to be realized. Hence, the TBCTR can be written with TBCTR = PRD-1 instead of TBCTR = PRD (in case the counter is counting up) and can be written as TBCTR = 1 instead of TBCTR = 0 (in case the counter is counting down) for the events to be realized. 

## _**7.5.6.4.2 Controlling and Monitoring the Time-Base Submodule**_ 

The block diagram in Figure 7-179 shows the critical signals and registers of the time-base submodule. Table 7-153 provides descriptions of the key signals associated with the time-base submodule. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 647 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [450 x 332] intentionally omitted <==**

**Figure 7-179. Time-Base Submodule Signals and Registers** 

648 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-153. Key Time-Base Signals** 

|**Signal**|**Description**|
|---|---|
|EPWMxSYNCI|Time-base synchronization input.|
||Input pulse used to synchronize the time-base counter with the counter of other ePWM modules. For more|
||information on all of the signals available for synchronization, see EPWMSYNCINSEL. For information on the|
||synchronization order of a particular device, seeTime-Base Counter Synchronization|
|EPWMxSYNCO|Time-base synchronization output.|
||This output pulse is used to synchronize the counter of other ePWM modules. Using EPWMSYNCOUTEN,|
||TBCTL2, TBCTL3 and GLDCTL2, the source of the output pulse is selected.|
|EPWMxSYNCPER|Time-base peripheral synchronization output.|
||This output signal is used to synchronize the CMPSS to the EPWM. The output signal can be configured using the|
||HRPCTL register. Note that this signal has no relation with the HRPWM.|
|CTR = PRD|Time-base counter equal to the specified period.|
||This signal is generated whenever the counter value is equal to the active period register value. That is when|
||TBCTR = TBPRD.|
|CTR = Zero|Time-base counter equal to zero|
||This signal is generated whenever the counter value is zero. That is when TBCTR equals 0x00.|
|CTR = CMPB|Time-base counter equal to active counter-compare B register (TBCTR = CMPB).|
||This event is generated by the counter-compare submodule and used by the synchronization out logic|
|CTR_dir|Time-base counter direction.|
||Indicates the current direction of the ePWM's time-base counter. The signal is high when the counter is increasing|
||and the signal is low when the counter is decreasing.|
|CTR_max|Time-base counter equal max value. (TBCTR = 0xFFFF)|
||Generated event when the TBCTR value reaches the maximum value. This signal is only used only as a status bit|
|TBCLK|Time-base clock.|
||This is a prescaled version of the ePWM clock (EPWMCLK) and is used by all submodules within the ePWM. This|
||clock determines the rate at which time-base counter increments or decrements.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

649 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.4.3 Calculating PWM Period and Frequency**_ 

The frequency of PWM events is controlled by the time-base period (TBPRD) register and the mode of the time-base counter. Figure 7-180 shows the period (Tpwm) and frequency (Fpwm) relationships for the up-count, down-count, and up-down-count time-base counter modes when the period is set to 4 (TBPRD = 4). The time increment for each step is defined by the time-base clock (TBCLK) which is a prescaled version of the ePWM clock (EPWMCLK). 

The time-base counter has three modes of operation selected by the time-base control register (TBCTL): 

- **Up-Down Count Mode:** In up-down count mode, the time-base counter starts from zero and increments until the period (TBPRD) value is reached. When the period value is reached, the time-base counter then decrements until the counter reaches zero. At this point, the counter repeats the pattern and begins to increment. 

- **Up-Count Mode:** In up-count mode, the time-base counter starts from zero and increments until the counter reaches the value in the period register (TBPRD). When the period value is reached, the time-base counter resets to zero and begins to increment once again. 

- **Down-Count Mode:** In down-count mode, the time-base counter starts from the period (TBPRD) value and decrements until the counter reaches zero. When the counter reaches zero, the time-base counter is reset to the period value and begins to decrement once again. 

**==> picture [402 x 337] intentionally omitted <==**

**----- Start of picture text -----**<br>
TPWM<br>PRD<br>4 4 4<br>3 3 3<br>2 2 2<br>1 1 Z 1<br>0 0 0<br>For Up Count and Down Count<br>TPWM TPWM = (TBPRD + 1) x TTBCLK<br>PRD<br>FPWM = 1/ (TPWM)<br>4 4 4<br>3 3 3<br>2 2 2<br>1 1 1 Z<br>0 0 0<br>TPWM TPWM<br>For Up and Down Count<br>4 4<br>3 3 3 3 TPWM = 2 x TBPRD x TTBCLK<br>2 2 2 2 FPWM = 1 / (TPWM)<br>1 1 1 1<br>0 0 0<br>CTR_dir Up Down Up Down<br>**----- End of picture text -----**<br>


**Figure 7-180. Time-Base Frequency and Period** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

650 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.4.3.1 Time-Base Period Shadow Register**_ 

The time-base period register (TBPRD) has a shadow register. Shadowing allows the register update to be synchronized with the hardware. The following definitions are used to describe all shadow registers in the ePWM module: 

- **Active Register:** The active register controls the hardware and is responsible for actions that the hardware causes or invokes. 

- **Shadow Register:** The shadow register buffers provide a temporary holding location for the active register and have no direct effect on any control hardware. At a strategic point in time, the shadow register content is transferred to the active register. This prevents corruption or spurious operation due to the register being asynchronously modified by software. 

The memory address of the shadow period register is the same as the active register. Which register is written to or read from is determined by the TBCTL[PRDLD] bit. This bit enables and disables the TBPRD shadow register as follows: 

- **Time-Base Period Shadow Mode:** The TBPRD shadow register is enabled when TBCTL[PRDLD] = 0. Reads from and writes to the TBPRD memory address go to the shadow register. The shadow register contents are transferred to the active register (TBPRD (Active) ← TBPRD (shadow)) when the time-base counter equals zero (TBCTR = 0x00) and/or a sync event as determined by the TBCTL2[PRDLDSYNC] bit. The PRDLDSYNC bit is valid only if TBCTL[PRDLD] = 0. By default the TBPRD shadow register is enabled. The sources for the SYNC input is explained in Section 7.5.6.4.3.3. 

The global load control mechanism can also be used with the time-base period register by configuring the appropriate bits in the global load configuration register (GLDCFG). When global load mode is selected the transfer of contents from shadow register to active register, for all registers that have this mode enabled, occurs at the same event as defined by the configuration bits in Global Shadow to Active Load Control Register (GLDCTL). Global load control mechanism is explained in Section 7.5.6.4.8 

- **Time-Base Period Immediate Load Mode:** If immediate load mode is selected (TBCTL[PRDLD] = 1), then a read from or a write to the TBPRD memory address goes directly to the active register. 

## _**7.5.6.4.3.2 Time-Base Clock Synchronization**_ 

The EPWM_CLKSYNC bit in the CONTROLSS_CTRL register allows all users to globally synchronize all enabled ePWM modules to the time-base clock (TBCLK). When set, all enabled ePWM module clocks are started with the first rising edge of TBCLK aligned. For perfectly synchronized TBCLKs, the prescalers for each ePWM module must be set identically. 

The proper procedure for enabling ePWM clocks is as follows: 

1. Set EPWM_CLKSYNC bit for correspont ePWM instance = 0 

2. Configure ePWM modules 

3. Set EPWM_CLKSYNC bit for corresponding ePWM instance = 1 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

651 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.4.3.3 Time-Base Counter Synchronization**_ 

The ePWM synchronization scheme allows for increased flexibility of synchronization of the ePWM modules. Each ePWM module has a synchronization input (SYNCI), a synchronization output (SYNCO) and a peripheral synchronization output (SYNCPER). In Figure 7-181, EXTSYNCIN1 is sourced from INPUTXBAR5 and EXTSYNCIN2 is sourced from INPUTXBAR6, which can be configured to select any GPIO as the synchronization input. Refer to for a list of all sync inputs including INPUTXBAR5 and INPUTXBAR6. Figure 7-182 shows the sources that can be used for EXTSYNCOUT. 

**==> picture [406 x 433] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTL<br>SWFSYNC<br>CTR=ZERO<br>CTR=CMPB<br>CTR=CMPC<br>CTR=CMPD<br>CLR<br>DCAEVT1.sync One Shot<br>DCBEVT1.sync Latch<br>0<br>Set Q<br>EPWMSYNCOUTEN<br>1<br>SWEN<br>ZEROEN<br>0 0<br>CMPBEN<br>1 EPWMxSYNCOUT<br>CMPCEN OR 1<br>0<br>CMPDEN<br>DCARVT1EN<br>DCBEVT1EN<br>Disable<br>EPWM1SYNCOUT<br>|<br>|<br>|<br>EPWMxSYNCOUT<br>EPWMxSYNCIN HRPCTL[PWMSYNCSELX]<br>ECAP1SYNCOUT CTR=CMPC UP<br>|<br>| CTR=CMPC DOWN<br>|<br>ECAPySYNCOUT CTR=CMPD UP EPWMxSYNCPER<br>Other Sources CTR=CMPD DOWN CMPSS<br>DAC<br>HRPCTL[PWMSYNCSEL]<br>CTR=PRD<br>EPWMSYNCINSEL<br>CTR=ZERO<br>Note: SYNCO and SYNCOUT are used interchangeably<br>Write “1” to Write “1” to<br>GLDCTL2[OSHTLD] TBCTL2[OSHTSYNC] TBCTL3[OSSFRCEN]<br>TBCTL2[OSHTSYNCMODE]<br>**----- End of picture text -----**<br>


**Figure 7-181. Time-Base Counter Synchronization Scheme** 

652 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [324 x 325] intentionally omitted <==**

**----- Start of picture text -----**<br>
EPWM1SYNCOUT<br>EPWMxSYNCOUT<br>Pulse-Stretched EXTSYNCOUT<br>(8 PLLSYSCLK<br>Cycles)<br>ECAP1SYNCOUT<br>ECAPySYNCOUT<br>SYNCSEL.SYNCOUT<br>EPWMxSYNCOUT (where x = number of EPWM and y = number of ECAP modules)<br>**----- End of picture text -----**<br>


**Figure 7-182. ePWM External SYNC Output** 

## **Note** 

See the data sheet for the number of ePWM and eCAP modules available on your specific device. 

Each ePWM module can be configured to use or ignore the synchronization input. If the TBCTL[PHSEN] bit is set, then the time-base counter (TBCTR) of the ePWM module is automatically loaded with the phase register (TBPHS) contents when one of the following conditions occur: 

- **EPWMxSYNCI: Synchronization Input Pulse:** The value of the phase register is loaded into the counter register when an input synchronization pulse is detected (TBPHS → TBCTR). This operation occurs on the next valid time-base clock (TBCLK) edge. 

The internal delay from the control module to the target module is calculated by the following formula: 

   - If (TBCLK == EPWMCLK): 2 x EPWMCLK Delay 

   - If (TBCLK < EPWMCLK): 1 x TBCLK Delay 

- **Software Forced Synchronization Pulse:** Writing a 1 to the TBCTL[SWFSYNC] control bit invokes a software forced synchronization. This pulse is ORed with the synchronization input signal, and therefore has the same effect as a pulse on EPWMxSYNCI. 

- **Digital Compare Event Synchronization Pulse:** DCAEVT1 and DCBEVT1 digital compare events can be configured to generate synchronization pulses which have the same effect as EPWMxSYNCI. 

## **Note** 

If the EPWMxSYNCI signal is held high, the sync does not continuously occur. The EPWMxSYNCI is rising edge activated. Do not implement multiple edges in a single PWM cycle when sync functionality is used. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 653 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Note** 

When modifying the TBPHS register during run-time, missed action qualifier events can occur due to sudden jumps in the TBCTR value at the time of the SYNCIN pulse. To recreate the behavior of missed action qualifier events, configure an action qualifier event on a T1 or T2 event on a SYNCIN event. The T1 or T2 action qualifier event is enabled and disabled during run-time depending on the value of TBPHS. 

This feature enables the ePWM module to be automatically synchronized to the time base of another ePWM module. Lead or lag phase control can be added to the waveforms generated by different ePWM modules to synchronize them. In up-down-count mode, the TBCTL[PHSDIR] bit configures the direction of the time-base counter immediately after a synchronization event. The new direction is independent of the direction prior to the synchronization event. The PHSDIR bit is ignored in count-up or count-down modes. See Figure 7-183 through Figure 7-186 for examples. 

Clearing the TBCTL[PHSEN] bit configures the ePWM to ignore the synchronization input pulse. 

## _**7.5.6.4.3.4 ePWM SYNC Selection**_ 

Table 7-154 specifies the sources for the ePWM SYNC input and output 

**Table 7-154. ePWM SYNC Selection** 

|**EPWMSYNCINSEL.SEL**|**SYNC Source**|
|---|---|
|0x0|Reserved|
|0x1|EPWM0 SYNCOUT|
|0x2|EPWM1 SYNCOUT|
|0x3|EPWM2 SYNCOUT|
|0x4|EPWM3 SYNCOUT|
|0x5|EPWM4 SYNCOUT|
|0x6|EPWM5 SYNCOUT|
|0x7|EPWM6 SYNCOUT|
|0x8|EPWM7 SYNCOUT|
|0x9|EPWM8 SYNCOUT|
|0xA|EPWM9 SYNCOUT|
|0xB|EPWM10 SYNCOUT|
|0xC|EPWM11 SYNCOUT|
|0xD|EPWM12 SYNCOUT|
|0xE|EPWM13 SYNCOUT|
|0xF|EPWM14 SYNCOUT|
|0x10|EPWM15 SYNCOUT|
|0x11|EPWM16 SYNCOUT|
|0x12|EPWM17 SYNCOUT|
|0x13|EPWM18 SYNCOUT|
|0x14|EPWM19 SYNCOUT|
|0x15|EPWM20 SYNCOUT|
|0x16|EPWM21 SYNCOUT|
|0x17|EPWM22 SYNCOUT|
|0x18|EPWM23 SYNCOUT|
|0x19-0x3F|Reserved|
|0x40|ECAP0 SYNCOUT|
|0x41|ECAP1 SYNCOUT|
|0x42|ECAP2 SYNCOUT|



654 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-154. ePWM SYNC Selection (continued)** 

|**EPWMSYNCINSEL.SEL**|**SYNC Source**|
|---|---|
|0x43|ECAP3 SYNCOUT|
|0x44|ECAP4 SYNCOUT|
|0x45|ECAP5 SYNCOUT|
|0x46|ECAP6 SYNCOUT|
|0x47|ECAP7 SYNCOUT|
|0x48|ECAP8 SYNCOUT|
|0x49|ECAP9 SYNCOUT|
|0x4A-0x4F|Reserved|
|0x50|INPUTXBAR OUT.4|
|0x51|INPUTXBAR OUT.20|
|0x52-0x57|Reserved|
|0x58|TIMESYNCXBAR SYNCPWMOUT0|
|0x59|TIMESYNCXBAR SYNCPWMOUT1|
|0x5A-0x5F|Reserved|
|0x60|FSI RX0 RXTRIG0|
|0x61|FSI RX0 RXTRIG1|
|0x62|FSI RX0 RXTRIG2|
|0x63|FSI RX0 RXTRIG3|
|0x64|FSI RX1 RXTRIG0|
|0x65|FSI RX1 RXTRIG1|
|0x66|FSI RX1 RXTRIG2|
|0x67|FSI RX1 RXTRIG3|
|0x68|FSI RX2 RXTRIG0|
|0x69|FSI RX2 RXTRIG1|
|0x6A|FSI RX2 RXTRIG2|
|0x6B|FSI RX2 RXTRIG3|
|0x6C|FSI RX3 RXTRIG0|
|0x6D|FSI RX3 RXTRIG1|
|0x6E|FSI RX3 RXTRIG2|
|0x6F|FSI RX3 RXTRIG3|
|0x70-0x7F|Reserved|



## _**7.5.6.4.4 Phase Locking the Time-Base Clocks of Multiple ePWM Modules**_ 

The CONTROLSS_CTRL.EPWM_CLKSYNC register has bits corresponding to each instance of ePWM. When EPWM_CLKSYNC = 0, the time-base clock of all corredsponding ePWM modules are stopped (default). When EPWM_CLKSYNC = 1, all corresponding ePWMs time-base clocks are started with the rising edge of TBCLK aligned. For perfectly synchronized TBCLKs, the prescaler bits in the TBCTL register of each ePWM module must be set identically. 

The EPWM_CLKSYNC bit can be used to globally synchronize the time-base clocks of all enabled ePWM modules on a device. These bits are part of the CONTROLSS_CTRL register. When EPWM_CLKSYNC = 0, the time-base clock of all corresponding ePWM modules are stopped (default). When EPWM_CLKSYNC = 1, all corresponding ePWM modules' time-base clocks are started with the rising edge of TBCLK aligned. For perfectly synchronized TBCLKs, the prescaler bits in the TBCTL register of each ePWM module must be set identically. The proper procedure for enabling the ePWM clocks is: 

1. Set EPWM_CLKSYNC = 0. This stops the time-base clock within any enabled ePWM module. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 655 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

2. Configure the prescaler values and desired ePWM modes. 

3. Set EPWM_CLKSYNC = 1. 

## _**7.5.6.4.5 Simultaneous Writes to TBPRD and CMPx Registers Between ePWM Modules**_ 

For variable frequency applications, there is a need for simultaneous writes of TBPRD and CMPx registers between ePWM modules. This prevents situations where a CTR = 0 or CTR = PRD pulse forces a shadow to active load of these registers before all registers are updated between ePWM modules (resulting in some registers being loaded from new shadow values while others are loaded from old shadow values). To support this, an ePWM register linking scheme for TBPRD:TBPRDHR, CMPA:CMPAHR, CMPB:CMPBHR, CMPC, and CMPD registers between PWM modules has been added. 

Refer to the register description for EPWMXLINK to see the linked register bit-field values for corresponding ePWM. An example of using the EPWMXLINK is linking ePWM2 CMPA with CMPA of ePWM1 through ePWM2's EPWMXLINK[CMPALINK] register bit-field. In this case, a write to CMPA of ePWM1 also changes the CMPA value for ePWM2. 

656 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.4.6 Time-Base Counter Modes and Timing Waveforms**_ 

The time-base counter operates in one of four modes: 

- Up-count mode that is asymmetrical 

- Down-count mode that is asymmetrical 

- Up-down-count that is symmetrical 

- Frozen where the time-base counter is held constant at the current value 

To illustrate the operation of the first three modes, the following timing diagrams show when events are generated and how the time-base responds to an EPWMxSYNCI signal. 

**==> picture [423 x 323] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR[15:0]<br>0xFFFF<br>TBPRD<br>(value)<br>TBPHS<br>(value)<br>0000<br>EPWMxSYNCI<br>CTR_dir<br>CTR = zero<br>CTR = PRD<br>CNT_max<br>**----- End of picture text -----**<br>


**Figure 7-183. Time-Base Up-Count Mode Waveforms** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 657 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [429 x 289] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR[15:0]<br>0xFFFF<br>TBPRD<br>(value)<br>TBPHS<br>(value)<br>0x000<br>EPWMxSYNCI<br>CTR_dir<br>CTR = zero<br>CTR = PRD<br>CNT_max<br>**----- End of picture text -----**<br>


**Figure 7-184. Time-Base Down-Count Mode Waveforms** 

658 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [429 x 291] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR[15:0]<br>0xFFFF<br>TBPRD<br>(value)<br>TBPHS<br>(value)<br>0x0000<br>EPWMxSYNCI<br>UP UP UP UP<br>CTR_dir<br>DOWN DOWN DOWN<br>CTR�=�zero<br>CTR�=�PRD<br>CNT_max<br>**----- End of picture text -----**<br>


**Figure 7-185. Time-Base Up-Down-Count Waveforms, TBCTL[PHSDIR = 0] Count Down On** 

**Synchronization Event** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 659 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [423 x 279] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR[15:0]<br>0xFFFF<br>TBPRD�(value)<br>TBPHS�(value)<br>0x0000<br>EPWMxSYNCI<br>UP UP UP<br>CTR_dir<br>DOWN DOWN DOWN<br>CTR�=�zero<br>CTR�=�PRD<br>CNT_max<br>**----- End of picture text -----**<br>


## **Figure 7-186. Time-Base Up-Down Count Waveforms, TBCTL[PHSDIR = 1] Count Up On Synchronization Event** 

## _**7.5.6.4.7 Edge Detection Within a Programmable TBCTR Range**_ 

An edge detection within a programmable TBCTR range is added in type 5 ePWM. 

This logic is primarily intended to detect an occurrence of a trip event in a configured time window. The window is configured by MIN and MAX values configured in the XMINMAX register sets. Refer to Event Detection for more details. 

Using the CAPIN signal and the CAPGATE signal, the Capture Control Logic can generate a CAPEVT signal if an edge is **NOT** detected within a specified range of TBCTR values. More information about CAPIN and CAPENT is located in Input Signal Detection. 

660 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.4.8 Global Load**_ 

Figure 7-187 shows the signals and registers associated with the global load feature. 

**==> picture [460 x 298] intentionally omitted <==**

**----- Start of picture text -----**<br>
Write 1 to<br>GLDCTL2[OSHTLD]<br>CNT_ZRO 0000 CLR<br>PRD_EQ 0001 One<br>CNT_ZRO or PRD_EQ 0010 Shot<br>(A)<br>DCAEVT1.sync Latch<br>DCBEVT1.sync(A) SYNCEVT Load Set Q<br>0011 Strobe<br>EPWMxSYNCI<br>TBCTL[SWFSYNC]<br>SYNCEVT 0100 1<br>CNT_ZRO<br>SYNCEVT 0101 0 0 Global<br>PRD_EQ Load<br>SYNCEVT 1 Strobe<br>0110 1<br>CNT_ZRO or PRD_EQ GLDCTL[GLDCNT] 0<br>Load<br>GLDCTL2[GFRCLD] 1111 Load Strobe<br>Strobe<br>clear CNT GLDCTL[OSHTMODE]<br>3-bit<br>Counter 0<br>inc CNT Local<br>GLDCTL[GLDMODE] Load<br>Strobe<br>GLDCTL[GLDPRD]<br>event1<br>event2<br>event3<br>event7<br>LOADMODE<br>…<br>…<br>**----- End of picture text -----**<br>


**Figure 7-187. Global Load: Signals and Registers** 

## **Note** 

The SYNCEVT signal is only propagated through when PHSEN is SET. 

When this feature is enabled, the transfer of contents from the shadow register to the active register, for all registers that have this mode enabled, occurs at the same event as defined by the configuration bits in Global Shadow to Active Load Control Register (GLDCTL[GLDMODE]). When GLDCTL[GLD] = 1, shadow to active load event selection bits for individual shadowed registers are ignored and global load mode takes effect for the corresponding registers enabled by GLDCFG[REGx]., where REGx is the register for which global load mode needs to be set. 

When GLDCTL[GLD] = 1 and GLDCFG[REGx] = 0, global load mode does not affect the corresponding register (REGx). Shadow to active load event selection bits for individual shadowed registers decide how the transfer of contents from shadow register to active register takes place. 

## _**7.5.6.4.8.1 Global Load Pulse Pre-Scalar**_ 

This feature provides the capability to choose shadow to active transfers to happen once in ‘N’ occurrences of selected global load pulse (GLDCTL[GLDMODE]). This pre-scale functionality is not available for registers that cannot or are not configured to use the global load mechanism (that is, GLDCTL[GLD] = 0 or GLDCFG[REGx] = 0). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 661 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.4.8.2 One-Shot Load Mode**_ 

This feature allows users to cause the shadow register to active register transfers to occur once. When GLDCTL2[OSHTLD] = 1 the shadow to active register transfer, for registers that are configured to use the global load mechanism, takes place on the event selected by GLDCTL[GLDMODE]. 

Software force loading of contents from shadow register to active register is possible by using GLDCTL2[GFRCLD]. The GLDCTL2 register can also be linked across multiple PWM modules by using EPWMXLINK[GLDCTL2LINK]. This, along with the one-shot load mode feature discussed above, provides a method to correctly update multiple PWM registers in one or more PWM modules at certain PWM events or, if desired, in the same clock cycle. This is very useful in variable frequency applications and/or multi-phase interleaved applications. 

## **Note** 

One-shot load mode must not be used when high-resolution mode is enabled. 

## _**7.5.6.4.8.3 One-Shot Sync Mode**_ 

To enable the one-shot sync mode to generate a SYNCOUT pulse, configure the TBCTL2[OSHTSYNCMODE] bit and set the TBCTL2[OSHTSYNC] bit as shown in Figure 7-188. 

**==> picture [487 x 176] intentionally omitted <==**

**----- Start of picture text -----**<br>
:ULWH�³1´�WR� CLR<br>TBCTL2[OSHTSYNC]<br>One Shot<br>Latch<br>Set Q<br>ePWM<br>0 0<br>1<br>Syncout 1<br>SYNCOUT<br>0<br>**----- End of picture text -----**<br>


TBCTL2[OSHTSYNCMODE] 

**Figure 7-188. One-Shot Sync Mode** 

662 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.6.5 Counter-Compare (CC) Submodule** 

Figure 7-189 illustrates the counter-compare submodule within the ePWM. 

**==> picture [500 x 272] intentionally omitted <==**

**Figure 7-189. Counter-Compare Submodule** 

## _**7.5.6.5.1 Purpose of the Counter-Compare Submodule**_ 

The counter-compare submodule takes as input the time-base counter value. This value is continuously compared to the counter-compare A (CMPA), counter-compare B (CMPB), counter-compare C (CMPC), and counter-compare D (CMPD) registers. When the time-base counter is equal to one of the compare registers, the counter-compare unit generates an appropriate event. 

The counter-compare: 

- Generates events based on programmable time stamps using the CMPA, CMPB, CMPC, and CMPD registers: 

   - CTR = CMPA: Time-base counter equals counter-compare A register (TBCTR = CMPA) 

   - CTR = CMPB: Time-base counter equals counter-compare B register (TBCTR = CMPB) 

   - CTR = CMPC: Time-base counter equals counter-compare C register (TBCTR = CMPC) 

   - CTR = CMPD: Time-base counter equals counter-compare D register (TBCTR = CMPD) 

- Controls the PWM duty cycle, if the action-qualifier submodule is configured appropriately using countercompare A (CMPA) and counter-compare B (CMPB) 

- Shadows new compare values to prevent corruption or glitches during the active PWM cycle 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 663 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.5.2 Controlling and Monitoring the Counter-Compare Submodule**_ 

The counter-compare submodule operation is shown in Figure 7-190. 

**==> picture [490 x 486] intentionally omitted <==**

**----- Start of picture text -----**<br>
Time TBCTR[15:0] 16<br>Base<br>(TB)<br>Module CTR = CMPA<br>CMPA[15:0] 16 Counter<br>Compare A<br>CMPCTL<br>[LOADASYNC] CMPCTL<br>CMPA [SHDWAFULL]<br>Action<br>DCAEVT1.syncDCBEVT1.syncEPWMxSYNCI(A)(A) 0 Shadow load Compare A Shadow Reg.Compare A Active Reg.CMPA [SHDWAMODE]CMPCTL QualifierModule(AQ)<br>TBCTL[SWFSYNC]<br>CMPCTL<br>[LOADAMODE] 16<br>TBCTR[15:0]<br>CTR = PRD CTR = CMPB<br>CMPB[15:0] 16 Counter<br>CTR = Zero Compare B<br>CMPCTL<br>[LOADBSYNC] CMPCTL<br>CMPB [SHDWBFULL]<br>DCAEVT1.syncDCBEVT1.sync(A)(A) 0 Shadow load Compare B Active Reg.CMPB [SHDWBMODECMPCTL ]<br>EPWMxSYNCI Compare B Shadow Reg.<br>TBCTL[SWFSYNC]<br>CMPCTL<br>[LOADBMODE] 16<br>TBCTR[15:0]<br>CTR = PRD CTR = CMPC<br>CMPC[15:0] 16 Counter<br>CTR = Zero Compare C<br>CMPCTL2<br>[LOADCSYNC] SOCA<br>CMPC CMPCTL2<br>DCAEVT1.syncDCBEVT1.sync(A)(A) 0 Shadow load Compare C Active Reg.CMPC [SHDWCMODE] TriggerEventand SOCB<br>EPWMxSYNCI Compare C Shadow Reg. Interrupt<br>TBCTL[SWFSYNC] (ET) EPWMxINT<br>CMPCTL2<br>[LOADCMODE] 16<br>TBCTR[15:0]<br>CTR = PRD CTR = CMPD<br>CMPD[15:0] 16 Counter<br>CTR = Zero Compare D<br>CMPCTL2<br>[LOADDSYNC]<br>CMPD CMPCTL2<br>DCBEVT1.syncDCAEVT1.sync(A)(A) 0 Shadow load Compare D Active Reg.CMPD [SHDWDMODE]<br>EPWMxSYNCI Compare D Shadow Reg.<br>TBCTL[SWFSYNC]<br>CMPCTL2<br>[LOADDMODE]<br>CTR = PRD<br>CTR = Zero<br>**----- End of picture text -----**<br>


- A. These events are generated by the ePWM digital compare (DC) submodule based on the levels of the TRIPIN inputs (for example, CMPSSx and TZ signals). 

## **Figure 7-190. Detailed View of the Counter-Compare Submodule** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

664 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.5.3 Operational Highlights for the Counter-Compare Submodule**_ 

The counter-compare submodule is responsible for generating events that can be used in the action-qualifier and event-trigger submodules. There are four independent compare events: 

1. CTR = CMPA: Time-base counter equal to counter-compare A register (TBCTR = CMPA). 

2. CTR = CMPB: Time-base counter equal to counter-compare B register (TBCTR = CMPB). 

3. CTR = CMPC: Time-base counter equal to counter-compare C register (TBCTR = CMPC). This event can be used to generate an event in the event trigger submodule only. 

4. CTR = CMPD: Time-base counter equal to counter-compare D register (TBCTR = CMPD). This event can be used to generate an event in the event trigger submodule only 

For up-count or down-count mode, each event occurs only once per cycle. For up-down count mode, each event occurs twice per cycle if the compare value is between 0x00-TBPRD; and once per cycle if the compare value is equal to 0x00 or equal to TBPRD. These events are applied to the action-qualifier submodule where the events are qualified by the counter direction and converted into actions if enabled. Refer to Section 7.5.6.6.1 for more details. 

The counter-compare registers CMPA and CMPB each have an associated shadow register. Shadowing provides a way to keep updates to the registers synchronized with the hardware. When shadowing is used, updates to the active registers only occur at strategic points. This prevents corruption or spurious operation due to the register being asynchronously modified by software. The memory address of the active register and the shadow register is identical. The register that is written to or read from is determined by the CMPCTL[SHDWAMODE] and CMPCTL[SHDWBMODE] bits. These bits enable and disable the CMPC shadow register and CMPD shadow register, respectively. The behavior of the two load modes is: 

## **Shadow Mode:** 

The shadow mode for the CMPA is enabled by clearing the CMPCTL[SHDWAMODE] bit and the shadow register for CMPB is enabled by clearing the CMPCTL[SHDWBMODE] bit. Shadow mode is enabled by default for both CMPA and CMPB. 

If the shadow register is enabled then the content of the shadow register is transferred to the active register on one of the following events as specified by the CMPCTL[LOADAMODE], CMPCTL[LOADBMODE], CMPCTL[LOADASYNC], and CMPCTL[LOADBSYNC] register bits: 

- CTR = PRD: Time-base counter equal to the period (TBCTR = TBPRD). 

- CTR = Zero: Time-base counter equal to zero (TBCTR = 0x00) 

- Both CTR = PRD and CTR = Zero 

- SYNC event caused by DCAEVT1 or DCBEVT1 or EPWMxSYNCI or TBCTL[SWFSYNC] 

- Both SYNC event or a selection made by LOADAMODE/LOADBMODE 

Only the active register contents are used by the counter-compare submodule to generate events to be sent to the action-qualifier. 

## **Note** 

Refer to Section 7.5.6.6.5 for valid configurations of CMPA/CMPB and LOADAMODE/LOADBMODE. 

## **Immediate Load Mode:** 

If the immediate load mode is selected (that is, CMPCTL[SHDWAMODE] = 1 or CMPCTL[SHDWBMODE] = 1), then a read from or a write to the register goes directly to the active register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 665 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Additional Comparators** 

The counter-compare submodule on ePWMs type 2 and later are responsible for generating two additional independent compare events based on two compare registers, which is fed to Event Trigger submodule: 

1. CTR = CMPC: Time-base counter equal to counter-compare C register (TBCTR = CMPC). 

2. CTR = CMPD: Time-base counter equal to counter-compare D register (TBCTR = CMPD). 

The counter-compare registers CMPC and CMPD each have an associated shadow register. By default this register is shadowed. The memory address of the active register and the shadow register is identical. The value in the active CMPC and CMPD register is compared to the time-base counter (TBCTR). When the values are equal, the counter compare module generates a “time-base counter equal to counter compare C or counter compare D ” event respectively. Shadowing of this register is enabled and disabled by the CMPCTL2[SHDWCMODE] and CMPCTL2[SHDWDMODE] bit. These bits enable and disable the CMPC shadow register and CMPD shadow register respectively. The behavior of the two load modes is described below: 

## **Shadow Mode:** 

The shadow mode for the CMPC is enabled by clearing the CMPCTL2[SHDWCMODE] bit and the shadow register for CMPD is enabled by clearing the CMPCTL2[SHDWDMODE] bit. Shadow mode is enabled by default for both CMPC and CMPD. 

If the shadow register is enabled then the content of the shadow register is transferred to the active register on one of the following events as specified by the CMPCTL2[LOADCMODE], CMPCTL2[LOADDMODE], CMPCTL2[LOADCSYNC], and CMPCTL2[LOADDSYNC] register bits: 

- CTR = PRD: Time-base counter equal to the period (TBCTR = TBPRD). 

- CTR = Zero: Time-base counter equal to zero (TBCTR = 0x00) 

- Both CTR = PRD and CTR = Zero 

- SYNC event caused by DCAEVT1 or DCBEVT1 or EPWMxSYNCI or TBCTL[SWFSYNC] 

- Both SYNC event or a selection made by LOADCMODE/LOADDMODE 

Only the active register contents are used by the counter-compare submodule to generate events to be sent to the action-qualifier. 

## **Immediate Load Mode:** 

If the immediate load mode is selected (that is, CMPCTL2[SHDWCMODE] = 1 or CMPCTL2[SHDWDMODE] = 1), then a read from or a write to the register goes directly to the active register. 

## **Global Load Support** 

The global load control mechanism can also be used for all counter-compare registers by configuring the appropriate bits in the global load configuration register (GLDCFG). When the global load mode is selected the transfer of contents from shadow register to active register, for all registers that have this mode enabled, occurs at the same event as defined by the configuration bits in the Global Shadow to Active Load Control Register (GLDCTL). The global load control mechanism is explained in Section 7.5.6.4.8. 

## _**7.5.6.5.4 Count Mode Timing Waveforms**_ 

The counter-compare module can generate compare events in all three count modes: 

- Up-count mode: used to generate an asymmetrical PWM waveform. 

- Down-count mode: used to generate an asymmetrical PWM waveform. 

- Up-down-count mode: used to generate a symmetrical PWM waveform. 

To best illustrate the operation of the first three modes, the timing diagrams in Figure 7-191 through Figure 7-193 show when events are generated and how the EPWMxSYNCI signal interacts. 

666 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

TBCTR[15:0] 

**==> picture [369 x 210] intentionally omitted <==**

**----- Start of picture text -----**<br>
0xFFFF<br>TBPRD<br>(value)<br>CMPA<br>(value)<br>CMPB<br>(value)<br>TBPHS<br>(value)<br>0x0000<br>EPWMxSYNCI<br>CTR�=�CMPA<br>CTR�=�CMPB<br>**----- End of picture text -----**<br>


An EPWMxSYNCI external synchronization event can cause a discontinuity in the TBCTR count sequence. This can lead to a compare event being skipped. This skipping is considered normal operation and must be taken into account. 

**Figure 7-191. Counter-Compare Event Waveforms in Up-Count Mode** 

**==> picture [434 x 242] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR[15:0]<br>0xFFFF<br>TBPRD<br>(value)<br>CMPA<br>(value)<br>CMPB<br>(value)<br>TBPHS<br>(value)<br>0x0000<br>EPWMxSYNCI<br>CTR�=�CMPA<br>CTR�=�CMPB<br>**----- End of picture text -----**<br>


**Figure 7-192. Counter-Compare Events in Down-Count Mode** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 667 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [415 x 250] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR[15:0]<br>0xFFFF<br>TBPRD (value)<br>CMPA (value)<br>CMPB (value)<br>TBPHS (value)<br>0x0000<br>EPWMxSYNCI<br>CTR = CMPB<br>CTR = CMPA<br>**----- End of picture text -----**<br>


**Figure 7-193. Counter-Compare Events In Up-Down-Count Mode, TBCTL[PHSDIR = 0] Count Down On** 

**Synchronization Event** 

**==> picture [430 x 250] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR[15:0]<br>0xFFFF<br>TBPRD<br>(value)<br>CMPA<br>(value)<br>CMPB<br>(value)<br>TBPHS<br>(value)<br>0x0000<br>EPWMxSYNCI<br>CTR = CMPB<br>CTR = CMPA<br>**----- End of picture text -----**<br>


**Figure 7-194. Counter-Compare Events In Up-Down-Count Mode, TBCTL[PHSDIR = 1] Count Up On** 

**Synchronization Event** 

668 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.6.6 Action-Qualifier (AQ) Submodule** 

The action-qualifier submodule has the most important role in waveform construction and PWM generation. The action-qualifier submodule decides which events are converted into various action types, thereby, producing the required switched waveforms at the EPWMxA and EPWMxB outputs. 

Figure 7-195 illustrates the action-qualifer submodule within the ePWM 

**==> picture [500 x 272] intentionally omitted <==**

**Figure 7-195. Action-Qualifier Submodule** 

## _**7.5.6.6.1 Purpose of the Action-Qualifier Submodule**_ 

The action-qualifier submodule is responsible for the following: 

- Qualifying and generating actions (set, clear, toggle) based on the following events: 

   - CTR = PRD: Time-base counter equal to the period (TBCTR = TBPRD). 

   - CTR = Zero: Time-base counter equal to zero (TBCTR = 0x00) 

   - CTR = CMPA: Time-base counter equal to the counter-compare A register (TBCTR = CMPA) 

   - CTR = CMPB: Time-base counter equal to the counter-compare B register (TBCTR = CMPB) 

- T1, T2 events: Trigger events based on comparator, trip or syncin events 

- Managing priority when these events occur concurrently 

- Providing independent control of events when the time-base counter is increasing and when it is decreasing 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 669 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.6.2 Action-Qualifier Submodule Control and Status Register Definitions**_ 

The action-qualifier submodule operation is shown in Figure 7-196. 

**==> picture [388 x 346] intentionally omitted <==**

**Figure 7-196. Action-Qualifier Submodule Inputs and Outputs** 

For convenience, the possible input events are summarized again in Table 7-155 

**Table 7-155. Action-Qualifier Submodule Possible Input Events** 

|**Signal**|**Description**|**Registers Compared**|
|---|---|---|
|CTR = PRD|Time-base counter equal to the period value|TBCTR = TBPRD|
|CTR = Zero|Time-base counter equal to 0|TBCTR = 0x00|
|CTR = CMPA|Time-base counter equal to the counter-compare A|TBCTR = CMPA|
|CTR = CMPB|Time-base counter equal to the counter-compare B|TBCTR = CMPB|
|T1 event|Based on comparator, trip, or syncin events|None|
|T2 event|Based on comparator, trip, or syncin events|None|
|Software forced event|Asynchronous event initiated by software||



The software forced action is a useful asynchronous event. This control is handled by the AQSFRC and AQCSFRC registers. 

670 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **Note** 

If the CSFA is not used in shadow mode, the RLDCSF bit must be configured to disable shadow mode. 

The action-qualifier submodule controls how the two outputs EPWMxA and EPWMxB behave when a particular event occurs. The event inputs to the action-qualifier submodule are further qualified by the counter direction (up or down). This allows for independent action on outputs on both the count-up and count-down phases. 

The possible actions imposed on outputs EPWMxA and EPWMxB are: 

- **Set High:** Set output EPWMxA or EPWMxB to a high level. 

- **Clear Low:** Set output EPWMxA or EPWMxB to a low level. 

- **Toggle:** If EPWMxA or EPWMxB is currently pulled high, then pull the output low. If EPWMxA or EPWMxB is currently pulled low, then pull the output high. 

- **Do Nothing:** Keep outputs EPWMxA and EPWMxB at same level as currently set. Although the "Do Nothing" option prevents an event from causing an action on the EPWMxA and EPWMxB outputs, this event can still trigger interrupts and ADC start of conversion. See the description in Section 7.5.6.12 for details. 

Actions are specified independently for either output (EPWMxA or EPWMxB). Any or all events can be configured to generate actions on a given output. For example, both CTR = CMPA and CTR = CMPB can operate on output EPWMxA. 

For clarity, the illustrations in this chapter use a set of symbolic actions. These symbols are summarized in Figure 7-197. Each symbol represents an action as a marker in time. Some actions are fixed in time (zero and period) while the CMPA and CMPB actions are moveable and their time positions are programmed by way of the counter-compare A and B registers, respectively. To turn off or disable an action, use the "Do Nothing option"(the default at reset). 

||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|
|Zero<br>Comp<br>A<br>Comp<br>B<br>Period<br>**TB Counter equals**<br>**S/W**<br>**force**<br>**Actions**|||||||||||
||Zero|Comp<br>A|||Comp<br>B|||Period|||
|SW|Z|CA||||||P||Do Nothing|
||||CA|||CB|||P||
||||||||||||
|SW|Z|CA||||||P||Clear Lo|
||||CA|||CB|||P||
||||||||||||
|SW|Z|CA||||||P||Set Hi|
||||CA|||CB|||P||
||||||||||||
|SW|Z|CA||||||P||Toggle|
||||CA|||CB|||P||
||||||||||||



**Figure 7-197. Possible Action-Qualifier Actions for EPWMxA and EPWMxB Outputs** 

The Action Qualifier Trigger Event Source Selection register (AQTSRCSEL) is used to select the source for T1 and T2 events. T1/T2 selection and configuration of a trip/digital-compare event in Action Qualifier submodule is independent of the configuration of that event in the Trip-Zone submodule. A particular trip event can or cannot 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 671 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

be configured to cause trip action in the Trip Zone submodule, but the same event can be used by the Action Qualifier to generate T1/T2 for controlling PWM generation. 

## _**7.5.6.6.3 Action-Qualifier Event Priority**_ 

It is possible for the ePWM action qualifier to receive more than one event at the same time. In this case, events are assigned a priority by the hardware. The general rule is events occurring later in time have a higher priority and software forced events always have the highest priority. The event priority levels for up-down count mode are shown in Table 7-156. A priority level of 1 is the highest priority and level 10 is the lowest. The priority changes slightly depending on the direction of TBCTR. 

**Table 7-156. Action-Qualifier Event Priority for Up-Down-Count Mode** 

|**Priority Level**|**Event If TBCTR is Incrementing**|**Event If TBCTR is Decrementing**|
|---|---|---|
||**TBCTR = Zero up to TBCTR = TBPRD**|**TBCTR = TBPRD down to TBCTR = 1**|
|1 (Highest)|Software forced event|Software forced event|
|2|T1 on up-count (T1U)|T1 on down-count (T1D)|
|3|T2 on up-count (T2U)|T2 on down-count (T2D)|
|4|Counter equals CMPB on up-count (CBU)|Counter equals CMPB on down-count (CBD)|
|5|Counter equals CMPA on up-count (CAU)|Counter equals CMPA on down-count (CAD)|
|6|Counter equals zero|Counter equals period (TBPRD)|
|7|T1 on down-count (T1D)|T1 on up-count (T1U)|
|8(Lowest)|T2 on down-count (T2D)|T2 on up-count (T2U)|



Table 7-157 shows the action-qualifier priority for up-count mode. In this case, the counter direction is always defined as up; therefore, down-count events never are taken. 

**Table 7-157. Action-Qualifier Event Priority for Up-Count Mode** 

|**Priority Level**|**Event**|
|---|---|
|1 (Highest)|Software forced event|
|2|Counter equal to period (TBPRD)|
|3|T1 on up-count (T1U)|
|4|T2 on up-count (T2U)|
|5|Counter equal to CMPB on up-count (CBU)|
|6|Counter equal to CMPA on up-count (CAU)|
|7 (Lowest)|Counter equal to Zero|



Table 7-158 shows the action-qualifier priority for down-count mode. In this case, the counter direction is always defined as down; therefore, up-count events never are taken. 

**Table 7-158. Action-Qualifier Event Priority for Down-Count Mode** 

|**Priority Level**|**Event**|
|---|---|
|1 (Highest)|Software forced event|
|2|Counter equal to Zero|
|3|T1 on down-count (T1D)|
|4|T2 on down-count (T2D)|
|5|Counter equal to CMPB on down-count (CBD)|
|6|Counter equal to CMPA on down-count (CAD)|
|7 (Lowest)|Counter equal to period (TBPRD)|



672 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

It is possible to set the compare value greater than the period. In this case, the action takes place as shown in Table 7-159. 

**Table 7-159. Behavior if CMPA/CMPB is Greater than the Period** 

|**Counter Mode**|**Compare on Up-Count Event**|**Compare on Down-Count Event**|
|---|---|---|
||**CAD/CBD**|**CAD/CBD**|
|Up-Count Mode|If CMPA/CMPB ≤ TBPRD period, then the event occurs|Never occurs.|
||on a compare match (TBCTR=CMPA or CMPB).||
||If CMPA/CMPB > TBPRD, then the event does not occur.||
|Down-Count Mode|Never occurs.|If CMPA/CMPB < TBPRD, the event occurs on a|
|||compare match (TBCTR=CMPA or CMPB).|
|||If CMPA/CMPB ≥ TBPRD, the event occurs on a period|
|||match (TBCTR=TBPRD).|
|Up-Down Count|If CMPA/CMPB < TBPRD and the counter is|If CMPA/CMPB < TBPRD and the counter is|
|Mode|incrementing, the event occurs on a compare match|decrementing, the event occurs on a compare match|
||(TBCTR=CMPA or CMPB).|(TBCTR=CMPA or CMPB).|
||If CMPA/CMPB is ≥ TBPRD, the event occurs on a|If CMPA/CMPB ≥ TBPRD, the event occurs on a period|
||period match (TBCTR = TBPRD).|match (TBCTR=TBPRD).|



## _**7.5.6.6.4 AQCTLA and AQCTLB Shadow Mode Operations**_ 

To enable Action Qualifier mode changes which must occur at the end of a period even when the phase changes, shadowing of the AQCTLA and AQCTLB registers has been added on ePWMs type 2 and later. Additionally, shadow to active load on SYNC of these registers is supported as well. Shadowing of this register is enabled and disabled by the AQCTL[SHDWAQAMODE] and AQCTL[SHDWAQBMODE] bits. These bits enable and disable the AQCTLA shadow register and AQCTLB shadow register, respectively. The behavior of the two load modes is: 

## **Shadow Mode:** 

The shadow mode for the AQCTLA is enabled by setting the AQCTL[SHDWAQAMODE] bit, and the shadow register for AQCTLB is enabled by setting the AQCTL[SHDWAQBMODE] bit. Shadow mode is disabled by default for both AQCTLA and AQCTLB. The memory address of the active register and the shadow register is identical. 

If the shadow register is enabled, then the content of the shadow register is transferred to the active register on one of the following events as specified by the AQCTL[LDAQAMODE], AQCTL[LDAQBMODE], AQCTL[LDAQASYNC], and AQCTL[LDAQBSYNC] register bits: 

- CTR = PRD: Time-base counter equal to the period (TBCTR = TBPRD). 

- CTR = Zero: Time-base counter equal to zero (TBCTR = 0x00) 

- Both CTR = PRD and CTR = Zero 

- SYNC event caused by DCAEVT1 or DCBEVT1 or EPWMxSYNCI or TBCTL[SWFSYNC] 

- Both SYNC event or a selection made by LDAQAMODE/LDAQBMODE 

## **Global Load Support** 

Global load control mechanism can also be used for AQCTLA:AQCTLA2, AQCTLB:AQCTLB2, and AQCSFRC registers by configuring the appropriate bits in the global load configuration register (GLDCFG). When global load mode is selected, the transfer of contents from shadow register to active register for all registers that have this mode enabled, occurs at the same event as defined by the configuration bits in the Global Shadow to Active Load Control Register (GLDCTL). The global load control mechanism is explained in Section 7.5.6.4.8. 

## **Immediate Load Mode:** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

673 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

If the immediate load mode is selected (that is, AQCTL[SHDWAQAMODE] = 0 or AQCTL[SHDWAQBMODE] = 0), then a read from or a write to the register goes directly to the active register. See Figure 7-198 and Figure 7-199 

## **Note** 

Shadow to Active Load of Action Qualifier Output A/B Control Register [AQCTLA and AQCTLB] on CMPA = 0 or CMPB = 0 boundary 

If the Counter-Compare A Register (CMPA) or Counter-Compare B Register (CMPB) is set to a value of 0 and the action qualifier action on AQCTLA and AQCTLB is configured to occur in the same instant as a shadow to active load (that is, CMPA=0 and AQCTLA shadow to active load on TBCTR=0 using AQCTL register LDAQAMODE and LDAQAMODE bits), then both events enter contention. It is recommended to use a Non-Zero Counter-Compare when using Shadow to Active Load of Action Qualifier Output A/B Control Register on TBCTR = 0 boundary. 

**==> picture [379 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
16<br>Load PWMx_AQCTLA(16)<br>Strobe Active Reg<br>00<br>AQCTL<br>[PWMx_LDAQAMODE] PWMx_AQCTLAS(16)<br>Shadow Reg<br>CTR = PRD 01<br>10<br>CTR = Zero 00<br>**----- End of picture text -----**<br>


- A. These events are generated by the ePWM digital compare (DC) submodule based on the levels of the TRIPIN inputs (for example, CMPSSx and TZ signals). 

**Figure 7-198. AQCTL[SHDWAQAMODE]** 

**==> picture [378 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
16<br>Load PWMx_AQCTLB(16)<br>Strobe Active Reg<br>00<br>AQCTL<br>[PWMx_LDAQBMODE] PWMx_AQCTLBS(16)<br>Shadow Reg<br>CTR = PRD 01<br>10<br>CTR = Zero 00<br>**----- End of picture text -----**<br>


- A. These events are generated by the ePWM digital compare (DC) submodule based on the levels of the TRIPIN inputs (for example, CMPSSx and TZ signals). 

## **Figure 7-199. AQCTL[SHDWAQBMODE]** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

674 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.6.5 Configuration Requirements for Common Waveforms**_ 

## **Note** 

The waveforms in this chapter show the behavior of the ePWMs for a static compare register value. In a running system, the active compare registers (CMPA and CMPB) are typically updated from their respective shadow registers once every period. Specify when the update takes place: either when the time-base counter reaches zero or when the time-base counter reaches the period. There are some cases when the action based on the new value can be delayed by one period or the action based on the old value can take effect for an extra period. Some PWM configurations avoid this situation. These include, but are not limited to, the following: 

## **Use up-down count mode to generate a symmetric PWM:** 

- If loading CMPA/CMPB on zero, then use CMPA/CMPB values greater than or equal to 1. 

- If loading CMPA/CMPB on period, then use CMPA/CMPB values less than or equal to TBPRD-1. 

This means there is always a pulse of at least one TBCLK cycle in a PWM period which, when very short, tend to be ignored by the system. 

## **Use up-down count mode to generate an asymmetric PWM:** 

- To achieve 50%-0% asymmetric PWM use the following configuration: Load CMPA/CMPB on period and use the period action to clear the PWM and a compare-up action to set the PWM. Modulate the compare value from 0 to TBPRD to achieve 50%-0% PWM duty. 

## **When using up-count mode to generate an asymmetric PWM:** 

- To achieve 0-100% asymmetric PWM, you **must** load CMPA/CMPB on TBPRD. When CMPA/ CMPB is not loaded on TBCTR=PRD, boundary conditions can occur depending on the timing of the write and the value written to CMPA/CMPB. Use the Zero action to set the PWM and a compare-up action to clear the PWM. Modulate the compare value from 0 to TBPRD+1 to achieve 0-100% PWM duty. 

## **When using up-count mode to generate an asymmetric PWM with deadband enabled:** 

- To achieve 0%-100% PWM use the following configuration: When the CMPA value is too close to 0 or PRD such that the following conditions are met (CMPX < Deadband) or (CMPX > PRD – Deadband), the actions specified by the AQCTL register for CMPX do not take effect. To avoid this, the AQCTL settings must be altered under these conditions only to generate either high or low pulses for CAU event (both set or both clear). Make sure that this software update is occurring synchronous to the PWM carrier cycle, and shadow mode is enabled. 

## **When using up-down count mode to generate an asymmetric PWM with deadband enabled:** 

- To achieve 0%-100% PWM use the following configuration: When the CMPA value is too close to 0 or PRD such that the following conditions are met (CMPX < Deadband/2) or (CMPX > PRD – (Deadband)/2), the actions specified by the AQCTL register for CMPX do not take effect. To avoid this, the AQCTL settings must be altered under these conditions only to generate either high or low pulses for both CAU or CAD events (both set or both clear). Make sure that this software update is occurring synchronous to the PWM carrier cycle, and shadow mode is enabled. 

See Using Enhanced Pulse Width Modulator (ePWM) Module for 0-100% Duty Cycle Control. 

Figure 7-200 shows how a symmetric PWM waveform can be generated using the up-down-count mode of the TBCTR. In this mode, 0%-100% DC modulation is achieved by using equal compare matches on the up count and down count portions of the waveform. In the example shown, CMPA is used to make the comparison. When the counter is incrementing, the CMPA match pulls the PWM output high. Likewise when the counter is decrementing, the compare match pulls the PWM signal low. When CMPA = 0, the PWM signal is high for the entire period giving a 100% duty waveform. When CMPA = TBPRD, the PWM signal is low achieving 0% duty. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 675 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

When using this configuration in practice, if loading CMPA/CMPB on zero, then use CMPA/CMPB values greater than or equal to 1. If loading CMPA/CMPB on period, then use CMPA/CMPB values less than or equal to TBPRD-1. This means there is always a pulse of at least one TBCLK cycle in a PWM period which, when very short, tend to be ignored by the system. 

**==> picture [471 x 374] intentionally omitted <==**

**----- Start of picture text -----**<br>
4 4<br>Mode: Up-Down Count 3 3 3 3<br>TBPRD = 4<br>CAU = SET, CAD = CLEAR 2 2 2 2<br>0% - 100% Duty<br>1 1 1 1<br>0 0 0<br>TBCTR<br>TBCTR Direction<br>UP DOWN UP DOWN<br>Case 1: PWMA/PWMB<br>CMPA = 4,  0% Duty<br>Case 2: PWMA/PWMB<br>CMPA = 3, 25% Duty<br>Case 3:<br>PWMA/PWMB<br>CMPA = 2, 50% Duty<br>Case 3:<br>PWMA/PWMB<br>CMPA = 1, 75% Duty<br>Case 4: PWMA/PWMB<br>CMPA = 0, 100% Duty<br>**----- End of picture text -----**<br>


**Figure 7-200. Up-Down Count Mode Symmetrical Waveform** 

The PWM waveforms in Figure 7-201 through Figure 7-207 show some common action-qualifier configurations. Some conventions used in the figures and examples are as follows: 

- TBPRD, CMPA, and CMPB refer to the value written in their respective registers. The active register, not the shadow register, is used by the hardware. 

- CMPx, refers to either CMPA or CMPB. 

- EPWMxA and EPWMxB refer to the output signals from ePWMx 

- Up-Down means count-up-and count-down mode, Up means up-count mode and Down means down-count mode 

- Sym = Symmetric, Asym = Asymmetric 

676 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [446 x 230] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR<br>TBPRD<br>value<br>Z P CB CA Z P CB CA Z P<br>PWMA<br>Z P CB CA Z P CB CA Z P<br>PWMB<br>**----- End of picture text -----**<br>


- A. PWM period = (TBPRD + 1) × TTBCLK 

- B. Duty modulation for EPWMxA is set by CMPA, and is active high (that is, high time duty proportional to CMPA). 

- C. Duty modulation for EPWMxB is set by CMPB and is active high (that is, high time duty proportional to CMPB). 

- D. The "Do Nothing" actions (X) are shown for completeness, but are not shown on subsequent diagrams. 

- E. Actions at zero and period, although appearing to occur concurrently, are actually separated by one TBCLK period. TBCTR wraps from period to 0000. 

**Figure 7-201. Up, Single Edge Asymmetric Waveform, with Independent Modulation on EPWMxA and EPWMxB—Active High** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

677 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [440 x 247] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR<br>TBPRD<br>value<br>P CA P CA P<br>PWMA<br>P CB P CB P<br>PWMB<br>**----- End of picture text -----**<br>


- A. PWM period = (TBPRD + 1) × TTBCLK 

- B. Duty modulation for EPWMxA is set by CMPA, and is active low (that is, the low time duty is proportional to CMPA). 

- C. Duty modulation for EPWMxB is set by CMPB and is active low (that is, the low time duty is proportional to CMPB). 

- D. Actions at zero and period, although appearing to occur concurrently, are actually separated by one TBCLK period. TBCTR wraps from period to 0000. 

## **Figure 7-202. Up, Single Edge Asymmetric Waveform with Independent Modulation on EPWMxA and EPWMxB—Active Low** 

678 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

TBCTR 

**==> picture [440 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBPRD<br>value<br>CA CB CA CB<br>PWMA<br>Z Z Z<br>T T T<br>PWMB<br>**----- End of picture text -----**<br>


- A. PWM frequency = 1/((TBPRD + 1) × TTBCLK) 

- B. Pulse can be placed anywhere within the PWM cycle (0000 - TBPRD) 

- C. High time duty proportional to (CMPB - CMPA) 

**Figure 7-203. Up-Count, Pulse Placement Asymmetric Waveform With Independent Modulation on EPWMxA** 

**==> picture [443 x 203] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR<br>TBPRD<br>value<br>CA CA CA CA<br>PWMA<br>CB CB CB CB<br>PWMB<br>**----- End of picture text -----**<br>


- A. PWM period = 2 x TBPRD × TTBCLK 

- B. Duty modulation for EPWMxA is set by CMPA, and is active low (that is, the low time duty is proportional to CMPA). 

- C. Duty modulation for EPWMxB is set by CMPB and is active low (that is, the low time duty is proportional to CMPB). 

- D. Outputs EPWMxA and EPWMxB can drive independent power switches. 

## **Figure 7-204. Up-Down Count, Dual-Edge Symmetric Waveform, with Independent Modulation on EPWMxA and EPWMxB — Active Low** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 679 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [423 x 198] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR<br>TBPRD<br>value<br>CA CA CA CA<br>PWMA<br>CB CB CB CB<br>PWMB<br>**----- End of picture text -----**<br>


- A. PWM period = 2 × TBPRD × TTBCLK 

- B. Duty modulation for EPWMxA is set by CMPA, and is active low, that is, low time duty proportional to CMPA. 

- C. Duty modulation for EPWMxB is set by CMPB and is active high, that is, high time duty proportional to CMPB. 

- D. Outputs EPWMx can drive upper/lower (complementary) power switches. 

- E. Dead-band = CMPB - CMPA (fully programmable edge placement by software). Note the dead-band module is also available if the more classical edge delay method is required. 

**Figure 7-205. Up-Down Count, Dual-Edge Symmetric Waveform, with Independent Modulation on EPWMxA and EPWMxB — Complementary** 

**==> picture [441 x 195] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR<br>CA CB CA CB<br>PWMA<br>Z P Z P<br>PWMB<br>**----- End of picture text -----**<br>


- A. PWM period = 2 × TBPRD × TBCLK 

- B. Rising edge and falling edge can be asymmetrically positioned within a PWM cycle. This allows for pulse placement techniques. 

- C. Duty modulation for EPWMxA is set by CMPA and CMPB. 

- D. Low time duty for EPWMxA is proportional to (CMPA + CMPB). 

- E. To change this example to active high, CMPA and CMPB actions need to be inverted (that is, Clear on CMPA, Set on CMPB). 

- F. Duty modulation for EPWMxB is fixed at 50% (utilizes spare action resources for EPWMxB). 

## **Figure 7-206. Up-Down Count, Dual-Edge Asymmetric Waveform, with Independent Modulation on EPWMxA—Active Low** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

680 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [421 x 198] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCTR<br>T1U T1D T1U T1D<br>EPWMxA<br>T2U T2D T2U T2D<br>EPWMxB<br>**----- End of picture text -----**<br>


- A. PWM period = 2 × TBPRD × TTBCLK 

- B. Independent T1 event actions when counter is counting up and when the counter is counting down are used to generate EPWMxA output. 

- C. Independent T2 event actions when counter is counting up and when the counter is counting down are used to generate EPWMxB output. 

- D. TZ1 is selected as the source for T1. 

- E. TZ2 is selected as the source for T2. 

**Figure 7-207. Up-Down Count, PWM Waveform Generation Utilizing T1 and T2 Events** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 681 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.6.7 Dead-Band Generator (DB) Submodule** 

Figure 7-208 illustrates the dead-band submodule within the ePWM. 

**==> picture [500 x 272] intentionally omitted <==**

**Figure 7-208. Dead_Band Submodule** 

## _**7.5.6.7.1 Purpose of the Dead-Band Submodule**_ 

The action-qualifier (AQ) module section discussed how the AQ module is possible to generate the required dead band by having full control over edge placement using both the CMPA and CMPB resources of the ePWM module. However, if the more classical edge delay-based dead band with polarity control is required, then the dead-band submodule described here must be used. 

The key functions of the dead-band module are: 

- Generating appropriate signal pairs (EPWMxA and EPWMxB) with dead-band relationship from a single EPWMxA input 

- Programming signal pairs for: 

   - Active high (AH) 

   - Active low (AL) 

   - Active high complementary (AHC) 

   - Active low complementary (ALC) 

- Adding programmable delay to rising edges (RED) 

- Adding programmable delay to falling edges (FED) 

- Can be totally bypassed from the signal path 

682 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.7.2 Dead-band Submodule Additional Operating Modes**_ 

On type 1 ePWM RED can appear on one channel output and FED can appear on the other channel output. 

The following list shows the distinct difference between type 1 and type 4 modules with respect to dead-band operating modes: 

- By adding S6, S7, and S8 in Figure 7-209, RED and FED can appear on both the A-channel and B-channel outputs. Additionally, both RED and FED together can be applied to either the A-channel or B-channel outputs to allow B-channel phase shifting with respect to the A-channel. 

## **Note** 

Phase shifting B-channel with respect to the A-channel using the dead-band submodule additional operating modes has limitations with respect to the choice of RED and FED delay with respect to the operating duty cycle of the ePWMxA and ePWMxB outputs. 

- The dead-band counters have also been increased to 14 bits 

- Deadband and deadband high-resolution registers are now shadowed 

- High-resolution deadband RED and FED have been enabled using the DBREDHR and DBFEDHR registers 

## **Note** 

The PWM chopper is not enabled when high-resolution deadband is enabled. 

High-resolution deadband RED and FED requires half-cycle clocking mode (DBCTL[HALFCYCLE] = 1). 

Cannot have both RED and FED together applied to both ePWMxA and ePWMxB. RED and FED together can be applied only to either OutA OR OutB. 

Phase shifting B-channel with respect to the A-channel: When PWMxB is derived from PWMxA using the DEDB_MODE bit and by delaying rising edge and falling edge by the phase shift amount. When the duty cycle value on PWMxA is less than this phase shift amount, PWMxA’s falling edge has precedence over the delayed rising edge for PWMxB. Make sure the duty cycle value of the current waveform applied to the dead-band module is greater than the required phase shift amount. 

The Type 4 action qualifier and dead-band outputs of the ePWM module are delayed by one TBCLK cycle in comparison to the Type 2 ePWM module, although the Type 4 behavior is the same as the Type 3 PWM. Both PWMA and PWMB signals are delayed under all circumstances. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

683 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Shadow Mode:** 

The shadow mode for the DBRED is enabled by setting the DBCTL[SHDWDBREDMODE] bit and the shadow register for DBFED is enabled by setting the DBCTL [SHDWDBFEDMODE] bit. Shadow mode is disabled by default for both DBRED and DBFED. The memory address of the active register and the shadow register is identical. 

If the shadow register is enabled, then the content of the shadow register is transferred to the active register on one of the following events as specified by the DBCTL [LOADREDMODE] and DBCTL [LOADFEDMODE] register bits: 

- CTR = PRD: Time-base counter equal to the period (TBCTR = TBPRD). 

- CTR = Zero: Time-base counter equal to zero (TBCTR = 0x00) 

- Both CTR = PRD and CTR = Zero 

The DBCTL register can be shadowed. The shadow mode for DBCTL is enabled by setting the DBCTL2[SHDWDBCTLMODE] bit. If the shadow register is enabled then the content of the shadow register is transferred to the active register on one of the following events as specified by the DBCTL2[LOADDBCTLMODE] register bit: 

- CTR = PRD: Time-base counter equal to the period (TBCTR = TBPRD) 

- CTR = Zero: Time-base counter equal to zero (TBCTR = 0x00) 

- Both CTR = PRD and CTR = Zero 

## **Note** 

The application software must enable shadow load mode in the DBCTL[SHDWDBREDMODE] and DBCTL[SHDWDBFEDMODE] **before** programming values for the DBRED and DBFED registers. If the shadow register is enabled **after** programming the DBRED and DBFED registers, the DBRED and DBFED registers are loaded with a value of 0. 

## **Global Load Support** 

Global load control mechanism can also be used for DBRED:DBREDHR, DBFED:DBFEDHR, and DBCTL registers by configuring the appropriate bits in the global load configuration register (GLDCFG). When global load mode is selected the transfer of contents from shadow register to active register, for all registers that have this mode enabled, occurs at the same event as defined by the configuration bits in the Global Shadow to Active Load Control Register (GLDCTL). The Global load control mechanism is explained in Section 7.5.6.4.8. 

## **Note** 

When DBRED/DBFED active is loaded with a new shadow value while DB counters are counting, the new DBRED/DBFED value only affects the NEXT PWMx edge and not the current edge. 

A Deadband value of zero cannot be used when the Global Shadow to Active Load is set to occur at CTR=ZERO. Similarly, a Deadband value of PRD cannot be used when the Global Shadow to Active Load is set to occur at CTR=PRD. 

TBPRDHR cannot be used with Global load. If high-resolution period must be changed in the application, users must write to the individual period registers from an ePWM ISR (The ISR must be synchronous with the PWM switching period), where the Global Load One-Shot bit is also written to. 

## _**7.5.6.7.3 Simultaneous Writes to DBRED and DBFED Registers Between ePWM Modules (Type 5 EPWM)**_ 

**LinkingDBRED and DBFED** Starting with type 5 EPWM, the DBRED and DBFED values can be linked from one ePWM to another. This allowsfor simultaneous writes to all linked ePWM registers. For more information, review the EPWMXLINK2 register. 

Similar to the EPWMXLINK register, the register description for EPWMXLINK2 clearly explains the linked registerbit-field values for corresponding ePWM. An example of using the EPWMXLINK2 is linking ePWM2 

684 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.7.4 Operational Highlights for the Dead-Band Submodule**_ 

The configuration options for the dead-band submodule are shown in Figure 7-209. 

**==> picture [485 x 308] intentionally omitted <==**

**----- Start of picture text -----**<br>
PWMA<br>DBCTL Rising Edge<br>[LOADREDMODE] Delay<br>DBRED<br>0<br>0 Shadow 0 A path 0 S6<br>RED<br>DBRED<br>OutA<br>In Active Out S1<br>S2 1<br>S4 (14-bit counter) 1 1<br>1<br>0<br>S8<br>1<br>Falling Edge 0 S7<br>Delay 0 S3 OutB<br>0 1 DBFED FED 1 S0<br>1<br>In Active Out<br>S5 0 S8 (14-bit counter) 1 0 B path<br>1 DBFED<br>DBCTL<br>Shadow<br>[LOADFEDMODE]<br>DBCTL[HALFCYCLE]<br>PWMB<br>DBCTL[OUT_MODE]<br>DBCTL[IN_MODE] DBCTL[DEDB_MODE] DBCTL[POLSEL] DBCTL[OUTSWAP]<br>**----- End of picture text -----**<br>


**Figure 7-209. Configuration Options for the Dead-Band Submodule** 

Although all combinations are supported, not all are typical usage modes. Table 7-160 documents some classical dead-band configurations. These modes assume that the DBCTL[IN_MODE] is configured such that EPWMxA In is the source for both falling-edge and rising-edge delay. Enhanced, or non-traditional modes can be achieved by changing the input signal source. The modes shown in Table 7-160 fall into the following categories: 

- **Mode 1: Bypass both falling-edge delay (FED) and rising-edge delay (RED):** Allows the user to fully disable the dead-band submodule from the PWM signal path. 

- **Mode 2-5: Classical Dead-Band Polarity Settings:** These represent typical polarity configurations that can address all the active-high and active-low modes required by available industry power switch gate drivers. The waveforms for these typical cases are shown in Figure 7-210 Note that to generate equivalent waveforms to Figure 7-210, configure the action-qualifier submodule to generate the signal as shown for EPWMxA. 

- **Mode 6: Bypass rising-edge-delay and Mode 7: Bypass falling-edge-delay:** Finally the last two entries in Table 7-160 show combinations where either the falling-edge-delay (FED) or rising-edge-delay (RED) blocks are bypassed. 

Figure 7-210 shows waveforms for typical cases where 0% < duty < 100%. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 685 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Table 7-160. Classical Dead-Band Operating Modes** 

||**DBCTL[POLSEL]**<br>**DBCTL[OUT_MODE]**|**DBCTL[POLSEL]**<br>**DBCTL[OUT_MODE]**|
|---|---|---|
|**Mode**<br>**Mode Description**|**S3**<br>**S2**<br>**S1**<br>**S0**||
|1<br>EPWMxA and EPWMxB Passed Through (No Delay)|X<br>X|0<br>0|
|2<br>Active High Complementary (AHC)|1<br>0|1<br>1|
|3<br>Active Low Complementary (ALC)|0<br>1|1<br>1|
|4<br>Active High (AH)|0<br>0|1<br>1|
|5<br>Active Low (AL)|1<br>1|1<br>1|
|6<br>EPWMxA Out = EPWMxA In (No Delay)<br>EPWMxB Out = EPWMxA In with Falling Edge Delay|0 or 1<br>0 or 1|0<br>1|
|7<br>EPWMxA Out = EPWMxA In with Rising Edge Delay<br>EPWMxB Out = EPWMxB In with No Delay|0 or 1<br>0 or 1|1<br>0|



## **Table 7-161. Additional Dead-Band Operating Modes** 

||**DBCTL[DEDB-MODE]**<br>**DBCTL[OUTSWAP]**|**DBCTL[DEDB-MODE]**<br>**DBCTL[OUTSWAP]**|
|---|---|---|
|**Mode Description**|**S8**<br>**S6**<br>**S7**||
|EPWMxA and EPWMxB signals are as defined by OUT-MODE bits.|0|0<br>0|
|EPWMxA = A-path as defined by OUT-MODE bits.<br>EPWMxB = A-path as defined by OUT-MODE bits (rising edge delay or delay-<br>bypassed A-signal path)|0|0<br>1|
|EPWMxA = B-path as defined by OUT-MODE bits (falling edge delay or delay-<br>bypassed B-signal path)<br>EPWMxB = B-path as defined by OUT-MODE bits|0|1<br>0|
|EPWMxA = B-path as defined by OUT-MODE bits (falling edge delay or delay-<br>bypassed B-signal path)<br>EPWMxB = A-path as defined by OUT-MODE bits (rising edge delay or delay-<br>bypassed A-signal path)|0|1<br>1|
|Rising edge delay applied to EPWMxA / EPWMxB as selected by S4 switch (IN-<br>MODE bits) on A signal path only.<br>Falling edge delay applied to EPWMxA / EPWMxB as selected by S5 switch (IN-<br>MODE bits) on B signal path only.|0|X<br>X|
|Rising edge delay and falling edge delay applied to source selected by S4 switch<br>(IN-MODE bits) and output to B signal path only.(1)|1|X<br>X|



(1) When this bit is set to 1, the user can always either set OUT_MODE bits such that Apath = InA or set OUTSWAP bits such that EPWMxA=Bpath. Otherwise, EPWMxA is invalid. 

686 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [316 x 407] intentionally omitted <==**

**----- Start of picture text -----**<br>
Period<br>Original<br>(outA)<br>RE D<br>Rising Edge<br>Delayed (RED)<br>FED<br>Falling Edge<br>Delayed (FED)<br>Active High<br>Complementary<br>(AHC)<br>Active Low<br>Complementary<br>(ALC)<br>Active High<br>(AH)<br>Active Low<br>(AL)<br>**----- End of picture text -----**<br>


**Figure 7-210. Dead-Band Waveforms for Typical Cases (0% < Duty < 100%)** 

The dead-band submodule supports independent values for rising-edge (RED) and falling-edge (FED) delays. The amount of delay is programmed using the DBRED and DBFED registers. These are 10-bit registers and their value represents the number of time-base clock, TBCLK, periods by which a signal edge is delayed. For example, the formula to calculate falling-edge-delay and rising-edge-delay is: 

FED = DBFED × TTBCLK 

RED = DBRED × TTBCLK 

Where TTBCLK is the period of TBCLK, the prescaled version of EPWMCLK. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 687 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

For convenience, delay values for various TBCLK options are shown in Table 7-162. The ePWM input clock frequency that these delay values been computed by is 100 MHz. 

**Table 7-162. Dead-Band Delay Values in μS as a Function of DBFED and DBRED** 

|**Dead-Band Value**||**Dead-Band Delay in μS**||
|---|---|---|---|
|**DBFED, DBRED**|**TBCLK = EPWMCLK/1**|**TBCLK = EPWMCLK /2**|**TBCLK = EPWMCLK/4**|
|1|0.01 μS|0.02 μS|0.04 μS|
|5|0.05 μS|0.10 μS|0.20 μS|
|10|0.10 μS|0.20 μS|0.40 μS|
|100|1.00 μS|2.00 μS|4.00 μS|
|200|2.00 μS|4.00 μS|8.00 μS|
|400|4.00 μS|8.00 μS|16.00 μS|
|500|5.00 μS|10.00 μS|20.00 μS|
|600|6.00 μS|12.00 μS|24.00 μS|
|700|7.00 μS|14.00 μS|28.00 μS|
|800|8.00 μS|16.00 μS|32.00 μS|
|900|9.00 μS|18.00 μS|36.00 μS|
|1000|10.00 μS|20.00 μS|40.00 μS|



When half-cycle clocking is enabled, the formula to calculate the falling-edge-delay and rising-edge-delay becomes: 

FED = DBFED × TTBCLK/2 

RED = DBRED × TTBCLK/2 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

688 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.6.8 Minimum Dead-Band (MINDB) + Illegal Combination Logic (ICL) Submodules** 

Figure 7-211 illustrates the minimum dead-band and illegal combo submodule within the ePWM. 

**==> picture [500 x 272] intentionally omitted <==**

**Figure 7-211. Minimum Dead-Band & Illegal Combo Logic Submodule** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

689 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.8.1 Minimum Dead-Band (MINDB)**_ 

To make sure that the minimum dead band property is not violated, as the application switches between normal mode and DE mode and due to the PWMs potentially switching based on trip inputs, a minimum dead band circuitry show in Figure 7-212 is required. 

**==> picture [501 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
Minimum Dead-Band + Illegal Combo Logic<br>MINDBCFG<br>[INVERTA]<br>MINDB X-BAR 15<br>1<br>0 0 10 0 Falling Edge Delay Logic [SELBLOCKA]MINDBCFG LUTCTLA<br>MINDBCFG MINDBDLY[DELAYA] 0 [SELXBAR] Illegal Combo Logic A(bypassed by default)<br>MINDBCFG [ENABLEA]<br>EPWMxA_DE_NO_HR [SELA] 1 ICL X-BAR [15:0] IN3 3:1 LUT<br>31 0 EPWMxA<br>EPWMxA_DE IN1 OUT<br>1 IN2<br>Diode<br>Emulation LUTCTLA<br>(DE) MINDBCFG [BYPASS]<br>[POLSELA]<br>EPWMxB_DE 31 0 IN2 EPWMxB<br>EPWMxB_DE_NO_HR 1 IN1 OUT<br>1 ICL X-BAR [15:0] IN3<br>MINDBCFG 3:1 LUT<br>[INVERTB] 0<br>MINDB X-BAR 15 1 MINDBCFG MINDBCFG[POLSELB] [SELXBAR]LUTCTLB Illegal Combo Logic B(bypassed by default)<br>1 Falling Edge  [SELBLOCKB]<br>0 0 0 0 Delay Logic [BYPASS]LUTCTLB<br>MINDBCFG MINDBDLY<br>[ENABLEB] [DELAYB]<br>MINDBCFG<br>[SELB]<br>**----- End of picture text -----**<br>


**Figure 7-212. Minimum Dead-Band and Illegal Combo Logic Block Diagram** 

The minimum dead band block provides the ability to configure the minimum dead band duration between a complimentary set of PWMs. 

Minimum dead-band logic involves generating a blocking signal (BLOCKA, BLOCKB) after the falling edge of the EPWMA/B_DE. These block signals are used to block transition on the other signal. The input to BLOCKA(B) signal generators is configurable. Normally the sources are EPWMA/B_DB_NO_HR. However, there is a provision provided to select any of the MINDB X-BAR outputs. This provides flexibility to support some of the other application scenarios. 

The selected source is fed to the BLOCK signal generation logic. Block signal generation involves, detecting the falling edge based on which BLOCK signal goes high and stretching the BLOCK signal for DELAYA/B cycles, which are software configurable. 

**==> picture [365 x 32] intentionally omitted <==**

**----- Start of picture text -----**<br>
Input into “Falling Edge Delay Logic” Block<br>sync sync<br>BLOCKx – Output of “Falling Edge Delay Logic” Block DelayA<br>**----- End of picture text -----**<br>


**Figure 7-213. Minimum Dead-Band Block Signal Generation** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

690 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

In Figure 7-214 and Figure 7-215, EPWMxA_DE and BLOCKB are getting ANDed and EPWMxB_DE and BLOCKA are getting ANDed. 

## **Note** 

Red shade is indicative of incorrect scenario. 

**==> picture [410 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
EPWMxA_DE<br>DelayA DelayA<br>BLOCKA<br>EPWMxB_DE<br>DelayB<br>BLOCKB<br>EPWMxA_MINDB<br>EPWMxB_MINDB<br>**----- End of picture text -----**<br>


**Figure 7-214. Example: Rising Edge on EPWMxA_DE and EPWMxB_DE While Delay is Being Applied** 

**==> picture [418 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
EPWMxA_DE<br>DelayA DelayA<br>BLOCKA<br>EPWMxB_DE<br>DelayB<br>BLOCKB<br>EPWMxA_MINDB<br>EPWMxB_MINDB<br>**----- End of picture text -----**<br>


**Figure 7-215. Example: Rising Edge on EPWMxA_DE while EPWMxB_DE is Still High** 

Figure 7-216 illustrates that a rising edge during the delay application does not affect the BLOCKA generation, same behavior is applied to BLOCKB. 

**==> picture [427 x 80] intentionally omitted <==**

**----- Start of picture text -----**<br>
EPWMxA_DE<br>DelayA DelayA<br>BLOCKA<br>EPWMxA_MINDB low<br>**----- End of picture text -----**<br>


**Figure 7-216. Rising Edge During Delay** 

Figure 7-217 showcases what happens when another falling edge occurs during the delay application. In this scenario, BLOCKA stays low until both DELAYA values are complete, same behavior is applied to BLOCKB. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

691 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [430 x 79] intentionally omitted <==**

**----- Start of picture text -----**<br>
EPWMxA_DE<br>DelayA DelayA<br>BLOCKA<br>EPWMxA_MINDB low<br>**----- End of picture text -----**<br>


**Figure 7-217. Rising Edge and Falling Edge During Delay** 

## _**7.5.6.8.2 Illegal Combo Logic (ICL)**_ 

As PWM generation logic gets more configurable and the interaction between multiple PWM instances increases, there is potential for corner cases during applications resulting in unintended PWM states. To detect and make sure that under no circumstance, the PWM states result in potentially hazardous combinations, a Look Up Table (LUT) has been added. By default, the LUT logic is bypassed, LUTXTLx[BYPASS]. When not bypassed, based on the combination of values on Input 3 (IN3), Input 2 (IN2), and Input 1 (IN1), the value driven on OUT is determined by the bits in the LUTCTLx [23:16] register. Input 3 into the LUT comes from one of the ICL X-BAR inputs. 

**==> picture [414 x 243] intentionally omitted <==**

**----- Start of picture text -----**<br>
LUTCTLx[BYPASS]<br>1<br>OUT (EPWMxA/B)<br>0<br>3:1 LUT<br>EPWMxA/B_MINDB IN1<br>IN2<br>EPWMxA/B_MINDB<br>IN3<br>000<br>001<br>.<br>.<br>LUTCTLx 111<br>[SELXBAR]<br>ICL X-BAR [15:0]<br>16<br>17<br>18<br>19<br>20<br>21<br>LUTCTLx [23:16]<br>22<br>23<br>**----- End of picture text -----**<br>


**Figure 7-218. Illegal Combo Logic Block Diagram** 

692 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.6.9 PWM Chopper (PC) Submodule** 

The PWM chopper submodule allows a high-frequency carrier signal to modulate the PWM waveform generated by the action-qualifier and dead-band submodules. This capability is important if pulse transformer-based gate drivers to control the power switching elements are needed. 

Figure 7-219 illustrates the PWM chopper submodule within the ePWM. 

**==> picture [500 x 272] intentionally omitted <==**

**Figure 7-219. PWM Chopper Submodule** 

## _**7.5.6.9.1 Purpose of the PWM Chopper Submodule**_ 

The key functions of the PWM chopper submodule are: 

- Programmable chopping (carrier) frequency 

- Programmable pulse width of first pulse 

- Programmable duty cycle of second and subsequent pulses 

- Can be fully bypassed if not required 

## _**7.5.6.9.2 Operational Highlights for the PWM Chopper Submodule**_ 

Figure 7-220 shows the operational details of the PWM chopper submodule. The carrier clock is derived from EPWMCLK. The clock frequency and duty cycle are controlled using the CHPFREQ and CHPDUTY bits in the PCCTL register. The one-shot block is a feature that provides a high energy first pulse to make sure hard and fast power switch turn on, while the subsequent pulses sustain pulses, making sure the power switch remains on. The one-shot width is programmed using the OSHTWTH bits. The PWM chopper submodule can be fully disabled (bypassed) using the CHPEN bit. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

693 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [425 x 271] intentionally omitted <==**

**----- Start of picture text -----**<br>
Bypass<br>0<br>EPWMxA<br>EPWMxA Start<br>One OSHT PWMA_ch 1<br>shot<br>Clk<br>Pulse-width<br>EPWMCLK /8<br>PCCTL<br>[OSHTWTH]<br>Divider and PCCTL<br>PSCLK<br>duty control [CHPEN]<br>PCCTL<br>[OSHTWTH]<br>PCCTL[CHPFREQ]<br>PCCTL[CHPDUTY]<br>Pulse-width<br>Clk<br>Oneshot PWMB_ch 1<br>OSHT<br>EPWMxB Start EPWMxB<br>Bypass 0<br>**----- End of picture text -----**<br>


**Figure 7-220. PWM Chopper Submodule Operational Details** 

## _**7.5.6.9.3 Waveforms**_ 

Figure 7-221 shows simplified waveforms of the chopping action only; one-shot and duty-cycle control are not shown. Details of the one-shot and duty-cycle control are discussed in the following sections. 

**==> picture [315 x 197] intentionally omitted <==**

**----- Start of picture text -----**<br>
EPWMxA<br>EPWMxB<br>PSCLK<br>EPWMxA<br>EPWMxB<br>**----- End of picture text -----**<br>


**Figure 7-221. Simple PWM Chopper Submodule Waveforms Showing Chopping Action Only** 

694 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.9.3.1 One-Shot Pulse**_ 

The width of the first pulse can be programmed to any of 16 possible pulse width values. The width or period of the first pulse is given by: 

T1stpulse = TEPWMCLK × 8 × OSHTWTH 

Where TEPWMCLK is the period of the system clock (EPWMCLK) and OSHTWTH is the four control bits (value from 1 to 16) 

Figure 7-222 shows the first and subsequent sustaining pulses and Table 7-163 gives the possible pulse width values for a EPWMCLK = 80 MHz. 

**==> picture [327 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
Start OSHT pulse<br>EPWMxA in<br>PSCLK<br>Prog. pulse width<br>(OSHTWTH)<br>OSHT<br>EPWMxA out<br>Sustaining pulses<br>**----- End of picture text -----**<br>


**Figure 7-222. PWM Chopper Submodule Waveforms Showing the First Pulse and Subsequent Sustaining Pulses** 

**Table 7-163. Possible Pulse Width Values for EPWMCLK = 80 MHz** 

|**OSHTWTH (hex)**|**Pulse Width (nS)**|
|---|---|
|0|100|
|1|200|
|2|300|
|3|400|
|4|500|
|5|600|
|6|700|
|7|800|
|8|900|
|9|1000|
|A|1100|
|B|1200|
|C|1300|
|D|1400|
|E|1500|
|F|1600|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 695 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.9.3.2 Duty Cycle Control**_ 

Pulse transformer-based gate drive designs need to comprehend the magnetic properties or characteristics of the transformer and associated circuitry. Saturation is one such consideration. To assist the gate drive designer, the duty cycles of the second and subsequent pulses have been made programmable. These sustaining pulses make sure the correct drive strength and polarity is maintained on the power switch gate during the on period, and hence a programmable duty cycle allows a design to be tuned or optimized using software control. 

Figure 7-223 shows the duty cycle control that is possible by programming the CHPDUTY bits. One of seven possible duty ratios can be selected ranging from 12.5% to 87.5%. 

**==> picture [442 x 474] intentionally omitted <==**

**----- Start of picture text -----**<br>
PSCLK<br>PSCLK<br>period<br>PSCLK Period<br>75% 50% 25%<br>87.5% 62.5% 37.5% 12.5%<br>Duty<br>1/8<br>Duty<br>2/8<br>Duty<br>3/8<br>Duty<br>4/8<br>Duty<br>5/8<br>Duty<br>6/8<br>Duty<br>7/8<br>**----- End of picture text -----**<br>


**Figure 7-223. PWM Chopper Submodule Waveforms Showing the Pulse Width (Duty Cycle) Control of Sustaining Pulses** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

696 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.6.10 Trip-Zone (TZ) Submodule** 

Each ePWM module is connected to six TZn signals (TZ1 to TZ6). TZ1 to TZ4 are sourced from the GPIO mux. TZ5 is connected to the system error fail logic, and TZ6 is sourced from the EMUSTOP output from the CPU. These signals indicate external fault or trip conditions, and the ePWM outputs can be programmed to respond accordingly when faults occur. 

Figure 7-224 illustrates the trip-zone submodule within the ePWM. 

**==> picture [500 x 272] intentionally omitted <==**

**Figure 7-224. Trip-Zone Submodule** 

## _**7.5.6.10.1 Purpose of the Trip-Zone Submodule**_ 

The key functions of the trip-zone submodule are: 

- Trip inputs TZ1 to TZ6 can be flexibly mapped to any ePWM module. 

- Upon a fault condition, outputs EPWMxA and EPWMxB can be forced to one of the following: 

   - High 

   - Low 

   - High-impedance 

   - No action taken 

- Support for one-shot trip (OSHT) for major short circuits or over-current conditions. 

- Support for cycle-by-cycle tripping (CBC) for current limiting operation. 

- Support for digital compare tripping (DC) based on state of on-chip analog comparator module outputs and TZ1 to TZ3 signals. 

- Each trip-zone input and digital compare (DC) submodule DCAEVT1/2 or DCBEVT1/2 force event can be allocated to either one-shot or cycle-by-cycle operation. 

- Interrupt generation is possible on any trip-zone input. 

- Software-forced tripping is also supported. 

- The trip-zone submodule can be fully bypassed if the submodule is not required. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 697 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.10.2 Operational Highlights for the Trip-Zone Submodule**_ 

The following sections describe the operational highlights and configuration options for the trip-zone submodule. 

The trip-zone signals TZ1 to TZ6 (also collectively referred to as TZn) are active-low input signals. When one of these signals goes low, or when a DCAEVT1/2 or DCBEVT1/2 force happens based on the TZDCSEL register event selection, the indication is that a trip event has occurred. Each ePWM module can be individually configured to ignore or use each of the trip-zone signals or DC events. Which trip-zone signals or DC events are used by a particular ePWM module is determined by the TZSEL register for that specific ePWM module. The trip-zone signals can or cannot be synchronized to the ePWMclock (EPWMCLK) and digitally filtered within the GPIO MUX block. A minimum of 3*TBCLK low pulse width on TZn inputs is sufficient to trigger a fault condition on the ePWM module. If the pulse width is less than this, the trip condition cannot be latched by CBC or OST latches. The asynchronous trip makes sure that if clocks are missing for any reason, the outputs can still be tripped by a valid event present on TZn inputs. The GPIOs or peripherals must be appropriately configured. 

Each TZn input can be individually configured to provide either a cycle-by-cycle or one-shot trip event for an ePWM module. DCAEVT1 and DCBEVT1 events can be configured to directly trip an ePWM module or provide a one-shot trip event to the module. Likewise, DCAEVT2 and DCBEVT2 events can also be configured to directly trip an ePWM module or provide a cycle-by-cycle trip event to the module. This configuration is determined by the TZSEL[DCAEVT1/2], TZSEL[DCBEVT1/2], TZSEL[CBCn], and TZSEL[OSHTn] control bits (where n corresponds to the trip input), respectively. 

## • **Cycle-by-Cycle (CBC):** 

When a cycle-by-cycle trip event occurs, the action specified in the TZCTL[TZA] and TZCTL[TZB] bits is carried out immediately on the EPWMxA and EPWMxB outputs. Table 7-164 lists some of the possible actions. Independent actions can be specified based on the occurrence of the event while the counter is counting up or while the counter is counting down by appropriately configuring bits in the TZCTL2 register. Actions specified in the TZCTL2 register take effect only when the ETZE bit in TZCTL2 is set. 

Additionally, when a cycle-by-cycle trip event occurs, the cycle-by-cycle trip event flag (TZFLG[CBC]) is set and a EPWMx_TZINT interrupt is generated when enabled in the TZEINT register and interrupt controller. A corresponding flag for the event that caused the CBC event is also set in register TZCBCFLG. 

If the CBC interrupt is enabled using the TZEINT register and DCAEVT2 or DCBEVT2 are selected as CBC trip sources using the TZSEL register, it is not necessary to also enable the DCAEVT2 or DCBEVT2 interrupts in the TZEINT register, as the DC events trigger interrupts through the CBC mechanism. 

The specified condition on the inputs is automatically cleared based on the selection made with TZCLR[CBCPULSE] if the trip event is no longer present. Therefore, in this mode, the trip event is cleared or reset every PWM cycle. The TZFLG[CBC] and TZCBCFLG flag bits remain set until the flag bits are manually cleared by writing to the TZCLR[CBC] and TZCBCCLR flag bits. If the cycle-by-cycle trip event is still present when the TZFLG[CBC] and TZCBCFLG register bits are cleared, then these bits are again immediately set. 

- **One-Shot (OSHT):** 

When a one-shot trip event occurs, the action specified in the TZCTL[TZA] and TZCTL[TZB] bits is carried out immediately on the EPWMxA and EPWMxB output. Table 7-164 lists some of the possible actions. Independent actions can be specified based on the occurrence of the event while the counter is counting up and while the counter is counting down by appropriately configuring bits in TZCTL2 register. Actions specified in TZCTL2 register take effect only when ETZE bit in TZCTL2 is set. 

Additionally, when a one-shot trip event occurs, the one-shot trip event flag (TZFLG[OST]) is set and a EPWMx_TZINT interrupt is generated when enabled in the TZEINT register and interrupt controller. A corresponding flag for the event that caused the OST event is also set in register TZOSTFLG. The one-shot trip condition must be cleared manually by writing to the TZCLR[OST] bit. If desired, the TZOSTFLG register bit can be cleared by manually writing to the corresponding bit in the TZOSTCLR register. 

698 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

If the one-shot interrupt is enabled using the TZEINT register and DCAEVT1 or DCBEVT1 are selected as OSHT trip sources using the TZSEL register, it is not necessary to also enable the DCAEVT1 or DCBEVT1 interrupts in the TZEINT register, as the DC events trigger interrupts through the OSHT mechanism. 

## **Note** 

Clear the TZFLG and TZOSTFLG flags after making sure that the TRIPIN source of the OST has become inactive. Otherwise, if interrupts are enabled, depending on when the flags are cleared, an OST interrupt can occur and the OST flags are zero. 

## • **Digital Compare Events (DCAEVT1/2 and DCBEVT1/2):** 

A digital compare DCAEVT1/2 or DCBEVT1/2 event is generated based on a combination of the DCAH/ DCAL and DCBH/DCBL signals as selected by the TZDCSEL register. The signals which source the DCAH/ DCAL and DCBH/DCBL signals are selected using the DCTRIPSEL register and can be either trip zone input pins or analog comparator CMPSSx signals. For more information on the digital compare submodule signals, see Section 7.5.6.13. 

When a digital compare event occurs, the action specified in the TZCTL[DCAEVT1/2] and TZCTL[DCBEVT1/2] bits is carried out immediately on the EPWMxA and EPWMxB output. Table 7-164 lists the possible actions. Independent actions can be specified based on the occurrence of the event while the counter is counting up and while the counter is counting down by appropriately configuring bits in TZCTLDCA and TZCTLDCB register. Actions specified in TZCTLDCA and TZCTLDCB registers take effect only when ETZE bit in TZCTL2 is set. 

In addition, the relevant DC trip event flag (TZFLG[DCAEVT1/2] / TZFLG[DCBEVT1/2]) is set and a EPWMx_TZINT interrupt is generated when enabled in the TZEINT register and interrupt controller. 

The specified condition on the pins is automatically cleared when the DC trip event is no longer present. The TZFLG[DCAEVT1/2] or TZFLG[DCBEVT1/2] flag bit remains set until the flag is manually cleared by writing to the TZCLR[DCAEVT1/2] or TZCLR[DCBEVT1/2] bit. If the DC trip event is still present when the TZFLG[DCAEVT1/2] or TZFLG[DCBEVT1/2] flag is cleared, then the flag is again immediately set. 

## • **Edge detection within a programmable TBCTR range (CAPEVT):** 

An edge detection within a programmable TBCTR range is added in type 5 ePWM. When a CAPIN edge does not occur within a specified range of TBCTR values, the CAPEVT signal is generated. The TBCTR range during which a CAPIN edge must occur is determined by XMINMAX_ACTIVE register. A gating signal CAPGATE can also be used to gate the CAPIN edge. For more information on the CAPEVT signal, see Section 7.5.6.13.4.4. 

In addition, the EPWMx_TZINT interrupt is generated when enabled in the TZEINT register and interrupt controller. 

The TZFLG[CAPEVT] flag bit remains set until the flag is manually cleared by writing to the TZCLR[CAPEVT] bit. If the CAPEVT event is still present when the TZFLG[CAPEVT] flag is cleared, then the flag is again immediately set. 

The action taken when a trip event occurs can be configured individually for each of the ePWM output pins by way of the TZCTL, TZCTL2, TZCTLDCA, and TZCTLDCB register bit fields. Some of the possible actions, shown in Table 7-164, can be taken on a trip event. 

The trip signal generated by the ePWM module can be selected through the TZTRIPOUTSEL register. This register has an ORed version of all the enabled trip signals. The TRIPOUT signal is routed to eCAP Trip Mux,PWM-XBAR and Output-XBAR. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 699 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [424 x 253] intentionally omitted <==**

**----- Start of picture text -----**<br>
Diode Emula � on<br>Submodule TZTRIPOUTSEL<br>OST<br>SYSCLKOUT SYNC<br>CBC<br>ECAP Trip Mux +  TZ1<br>EPWM &<br>Output XBAR TZ2<br>TZ3<br>TZ4<br>TZ5<br>TRIPOUT<br>TZ6<br>DCAEVT1.force<br>DCBEVT1.force<br>DCAEVT2.force<br>DCBEVT2.force<br>CAPEVT<br>**----- End of picture text -----**<br>


**Figure 7-225. Trip-Zone TRIPOUT Selection** 

**Table 7-164. Possible Actions On a Trip Event** 

|**TZCTL Register Bitfield**|**EPWMxA**|**Comment**|
|---|---|---|
|**Settings**|**and**||
||**EPWMxB**||
|0,0|High-Impedance|Tripped|
|0,1|Force to High State|Tripped|
|1,0|Force to Low State|Tripped|
|1,1|No Change|Do Nothing.|
|||No change is made to the output.|



700 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**Example 7-8. Trip-Zone Configurations**_ 

## **Scenario A:** 

- A one-shot trip event on TZ1 pulls both EPWM1A, EPWM1B low and also forces EPWM2A and EPWM2B high. • Configure the ePWM1 registers as follows: 

   - TZSEL[OSHT1] = 1: enables TZ1 as a one-shot event source for ePWM1 

   - TZCTL[TZA] = 2: EPWM1A is forced low on a trip event. 

   - TZCTL[TZB] = 2: EPWM1B is forced low on a trip event. 

- Configure the ePWM2 registers as follows: 

   - TZSEL[OSHT1] = 1: enables TZ1 as a one-shot event source for ePWM2 

   - TZCTL[TZA] = 1: EPWM2A is forced high on a trip event. 

   - TZCTL[TZB] = 1: EPWM2B is forced high on a trip event. 

## **Scenario B:** 

A cycle-by-cycle event on TZ5 pulls both EPWM1A, EPWM1B low. 

A one-shot event on TZ1 or TZ6 puts EPWM2A into a high impedance state. 

- Configure the ePWM1 registers as follows: 

   - TZSEL[CBC5] = 1: enables TZ5 as a cycle-by-cycle event source for ePWM1 

   - TZCTL[TZA] = 2: EPWM1A is forced low on a trip event. 

   - TZCTL[TZB] = 2: EPWM1B is forced low on a trip event. 

- Configure the ePWM2 registers as follows: 

   - TZSEL[OSHT1] = 1: enables TZ1 as a one-shot event source for ePWM2 

   - TZSEL[OSHT6] = 1: enables TZ6 as a one-shot event source for ePWM2 

   - TZCTL[TZA] = 0: EPWM2A is put into a high-impedance state on a trip event. 

   - – TZCTL[TZB] = 3: EPWM2B ignores the trip event. 

## **Note** 

When configuring the GPIOs and INPUT X-BAR/EPWM X-BAR options, be aware that a change in the X-BAR input selections can cause an unwanted event. Therefore, set up the GPIO and X-BAR input configurations before enabling the ePWM Trip-Zone. If a requirement is to change the GPIO/X-BAR configurations while the ePWM Trip-Zone is enabled, the user can turn off the TRIPs by clearing the TZSEL register and reconfiguring the TRIP selection (TZSEL) after the INPUT XBAR selection is changed. 

## _**7.5.6.10.3 Generating Trip Event Interrupts**_ 

Figure 7-226 and Figure 7-227 illustrate the trip-zone submodule control and interrupt logic, respectively. DCAEVT1/2 and DCBEVT1/2 signals are described in further detail in Digital Compare (DC) Submodule. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 701 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [404 x 593] intentionally omitted <==**

**----- Start of picture text -----**<br>
TZCTLDCA[DCAEVT1U, DCAEVT1D, DCAEVT2U, DCAEVT2D]<br>TZCTL[TZA, DCAEVT1, DCAEVT2]<br>TZCTL2[TZAU, TZAD, ETZE]<br>EPWMxA (from PC submodule)<br>EPWMA<br>DCAEVT1.force<br>Trip EPWMxA<br>DCAEVT2.force Logic<br>DCAEVT1.force<br>TRIPx Digital DCAEVT2.force<br>TZCTLDCB[DCBEVT1U, DCBEVT1D,<br>TZx SubmoduleCompare DCBEVT1.force                     DCBEVT2U, DCBEVT2D]<br>DCBEVT2.force TZCTL[TZB, DCBEVT1, DCBEVT2]<br>TZCTL2[TZBU, TZBD, ETZE]<br>EPWMxB (from PC submodule) EPWMB<br>DCBEVT1.force<br>Trip EPWMxB<br>TZCLR[CBCPULSE] DCBEVT2.force<br>Logic<br>CTR = PRD 01<br>Clear<br>10<br>CTR = Zero 00 Clear<br>CBC Latch Trip<br>TZFRC[CBC] Set<br>TZ1 Async<br>TZ2 Sync Set Trip<br>TZ3 TZFLG[CBC]<br>TZCLR[CBC]<br>TZ4 Clear<br>TZ5<br>TZ6<br>DCAEVT2.force<br>Cycle-by-Cycle (CBC)<br>DCBEVT2.force<br>Trip Events<br>CAPEVT<br>TZSEL[CBC1 to CBC6, DCAEVT2, DCBEVT2]<br>                     TZSEL2[CAPEVTCBC]<br>TZCLR[OST] Clear<br>OSHT Latch Trip<br>TZFRC[OSHT] Set<br>TZ1 Async<br>TZ2 Sync Clear Set Trip<br>TZ3 TZFLG[OST]<br>TZ4<br>TZ5<br>TZ6<br>DCAEVT1.force<br>DCBEVT1.force One-Shot (OSHT)<br>CAPEVT Trip Events<br>TZSEL[OSHT1 to OSHT6, DCAEVT1, DCBEVT1]<br>                      TZSEL2[CAPEVTOST]<br>**----- End of picture text -----**<br>


**Figure 7-226. Trip-Zone Submodule Mode Control Logic** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

702 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [412 x 397] intentionally omitted <==**

**----- Start of picture text -----**<br>
TZFLG[CBC]<br>Clear TZCLR[CBC]<br>Latch<br>Set CBC Force<br>TZEINT[CBC]<br>Output Event<br>TZFLG[OST]<br>TZFLG[INT]<br>Clear TZCLR[OST]<br>Latch<br>TZCLR[INT] Clear Set OST Force<br>Latch TZEINT[OST] Output Event<br>Set TZFLG[DCAEVT1]<br>Clear TZCLR[DCAEVT1]<br>Latch<br>Generate Set DCAEVT1.inter<br>TZEINT[DCAEVT1]<br>Interrupt<br>Pulse TZFLG[DCAEVT2]<br>EPWMxTZINT (PIE) When<br>Input = 1 Clear TZCLR[DCAEVT2]<br>Latch<br>Set DCAEVT2.inter<br>TZEINT[DCAEVT2]<br>TZFLG[DCBEVT1]<br>Clear TZCLR[DCBEVT1]<br>Latch<br>Set DCBEVT1.inter<br>TZEINT[DCBEVT1]<br>TZFLG[DCBEVT2]<br>Clear TZCLR[DCBEVT2]<br>Latch<br>Set DCBEVT2.inter<br>TZEINT[DCBEVT2]<br>TZFLG[CAPEVT]<br>Clear TZCLR[CAPEVT]<br>Latch<br>Set CAPEVT.inter<br>TZEINT[CAPEVT]<br>**----- End of picture text -----**<br>


**Figure 7-227. Trip-Zone Submodule Interrupt Logic** 

The signal CAPEVT is generated from the Capture Control Logic and is available in type 5 EPWM. 

These individual flags for the CBC, OST and DCxEVTy can be used to detect the source of the EPWMxTZINT Interrupt. When multiple sources are used to generate the EPWMxTZINT interrupt, reading and clearing the flags takes different actions based on the specific event. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

703 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.6.11 Diode Emulation (DE) Submodule** 

The purpose of the Diode Emulation logic is to provide hardware features and the necessary hooks into other IPs to implement robust diode mode sense and control in a noisy environment. 

Diode Emulation features include: 

- Ability to choose any of the comparator outputs as trips to detect entry into DE mode. 

- Ability to switch the comparator thresholds, dynamically in hardware upon DE mode entry. 

- Two modes of clearing/de-evaluating the DE condition: 

   - Software clear 

   - Cycle-by-cycle clear on PWMSYNC event 

- Configurable source selects of ePWM in DE mode. 

- Ability to monitor the DE mode duration and generate a trip event to ePWMs. 

Figure 7-228 illustrates the diode emulation submodule within the ePWM. 

**==> picture [500 x 271] intentionally omitted <==**

**Figure 7-228. Diode Emulation Submodule** 

Figure 7-229 shows the interfaces to the DE block. As can be seen from the diagram, DE function is associated with an instance of ePWMx. The EPWMxA and EPWMxB signals from a given instance of ePWM module pass through the associated DE block and minimum dead band logic. In addition to EPWMxA and EPWMxB, two signals, EPWMxA_DB_NO_HR and EPWMxB_DB_NO_HR are tapped from the ePWM modules. These two signals are PWM signals that are tapped before the signals pass through the high-resolution delay lines and come from the dead-band submodule outputs. If high-resolution is not used, then EPWMxA_DB_NO_HR and EPWMxB_DB_NO_HR are just the outputs of the dead-band submodule. 

704 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [394 x 519] intentionally omitted <==**

**----- Start of picture text -----**<br>
TRIPH_OR_TRIPL Reentry Delay  DEACTIVE<br>Counter<br>EPWMxSYNCPER<br>DE DEMONTRIP<br>Monitor<br>DECOMPSEL[TRIPH]<br>TRIPH<br>CMP1TRIPH TRIPH_OR_TRIPL<br>CMPnTRIPH<br>TRIPL<br>CMP1TRIPL<br>CMPnTRIPL<br>DECOMPSEL[TRIPL]<br>TRIPH<br>TRIPL<br>EPWMxA EPWMxA_DE<br>DE<br>EPWMxA_DB_NO_HR EPWM  EPWMxA_DE_NO_HR<br>EPWMxB Control EPWMxB_DE<br>EPWMxB_DB_NO_HR EPWMxB_DE_NO_HR<br>EPWMxTRIPOUT<br>DEACTCTL<br>To CMPSS, To ECAP,<br>ECAP, Output  EPWM XBARs<br>XBAR<br>Input X-BAR<br>CLB Input X-BAR<br>Input X-BAR<br>CLB Input X-BAR<br>DEACTIVE<br>DExACTIVE DEMONTRIP<br>**----- End of picture text -----**<br>


**Figure 7-229. Diode Emulation Block Diagram** 

The DE block can be configured to select one of the comparators or one of the outputs of the Input XBAR, as source of trip signals (TRIPH, TRIPL). The selected comparator is responsible for monitoring the current in the external power converter. Comparator thresholds (High and Low threshold) can be set such that, any breach of these thresholds indicates a need to switch to the DE mode. 

Once DE mode is entered, indicated by setting of DEACTIVE flag, the ePWMs sent out of DE block are controlled by configuration registers in the DE block, and are not be the same as ePWMA/B from the associated ePWM instance. Once the DEACTIVE flag is set, the threshold settings of the selected CMPSS are switched to a new set of values (a narrower region). DEACTIVE flag from all of the ePWM instances are hooked up to all the 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 705 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

comparator sub-systems (CMPSSy) to enable threshold value switch on DE mode entry. Refer to the CMPSS chapter for more details on how the new threshold values are set. 

## _**7.5.6.11.1 DEACTIVE Mode**_ 

DE mode is entered when TRIPH_OR_TRIPL signal from the selected comparator (CMPSS) goes high. Once the diode emulation mode is entered, typically TRIPH or TRIPL are set and cleared in a sequence (at a given instance of time, TRIPH is high or TRIPL is high – never both) until the current settles within the threshold band. 

**==> picture [499 x 247] intentionally omitted <==**

**----- Start of picture text -----**<br>
REENTRY_DLY_CNT !=0<br>DEFRC<br>0 1 [DEACTIVE]<br>DECTL<br>[RENTRYDLY]<br>TRIPH_OR_TRIPL Sync 0<br>SET DEACTIVE To CMPSS,  Reentry Delay Counter<br>Q ECAP, and  (REENTRY_DLY_CNT)<br>DEACTIVE  Output X-BAR<br>SYSCLK<br>LATCH<br>CLR<br>Cycle-by-Cycle 0<br>One-Shot   1<br>DECLR<br>[DEACTIVE]<br>DECTL<br>[MODE]<br>EPWMxSYNCPER<br>**----- End of picture text -----**<br>


**Figure 7-230. DEACTIVE Flag Functionality** 

Once the DEACTIVE flag is set, the thresholds on CMPSS are changed to an alternate set of thresholds, and also ePWMA/B out of DE function are being controlled by the DEACTCTL register settings. Figure 7-231 demonstrates an example timing diagram illustrating entry into DE mode. 

**==> picture [54 x 93] intentionally omitted <==**

**----- Start of picture text -----**<br>
DEACTIVE<br>EPWMxA<br>EPWMxB<br>EPWMxSYNCPER<br>TRIPH_OR_TRIPL<br>TRIPH<br>TRIPL<br>**----- End of picture text -----**<br>


**==> picture [211 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
Diode Emulation Phase<br>**----- End of picture text -----**<br>


**==> picture [242 x 118] intentionally omitted <==**

**Figure 7-231. Example Timing Sequence Illustrating DE Mode Entry** 

706 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.11.2 Exiting DE Mode**_ 

DE mode can be exited in two ways, based on the DECTL[MODE] setting: 

- Software clear of DEACTIVE flag, DECLR[CLR] 

- Cycle-by-cycle clear mode, in which TRIPH_OR_TRIPL is evaluated on every EPWMxSYNCPER and if the trip condition is not present, then DEACTIVE flag is cleared. Figure 7-232 illustrates the clearing of the DEACTIVE flag based on EPWMxSYNCPER. 

**==> picture [499 x 102] intentionally omitted <==**

**----- Start of picture text -----**<br>
DEACTIVE<br>EPWMxA<br>EPWMxB<br>EPWMxSYNCPER<br>TRIPH_OR_TRIPL<br>TRIPH<br>TRIPL<br>Diode Emulation Phase<br>**----- End of picture text -----**<br>


**Figure 7-232. Cycle-by-Cycle Mode** 

## _**7.5.6.11.3 Re-Entering DE Mode**_ 

Once DE mode is exited, DE mode can be delayed for a certain duration until reentry. This is accomplished by configuring the DECTL[REENTRYDLY] field. REENTRYDLY determines the window in which TRIP signals are prevented from setting the DEACTIVE flag. On a falling edge of DEACTIVE, an internal counter is loaded with the DECTL[REENTRYDLY] value. The counter is decremented on every EPWMxSYNCPER as long as the count value is greater than 0. While the count value is greater than 0, TRIP signals are blocked and DEACTIVE flag is not set even if TRIP events are active. 

**==> picture [500 x 139] intentionally omitted <==**

**----- Start of picture text -----**<br>
DEACTIVE<br>REENTRY_DLY_CNT 0x00000000 0x00000004 0x00000003 0x00000002 0x00000001<br>EPWMxSYNCPER<br>EPWMxA<br>EPWMxB<br>TRIPH_OR_TRIPL<br>TRIPH<br>TRIPL<br>Diode Emulation Phase<br>**----- End of picture text -----**<br>


**Figure 7-233. DE Mode Reentry Sequence** 

Figure 7-234 illustrates the circuit driving the EPWMxA/B signals from the DE block. As can be observed, when DEACTIVE flag is not set, EPWMxA_DE, EPWMxB_DE, EPWMxA_DE_NO_HR, and EPWMxB_DE_NO_HR are driven by EPWMA/B and EPWMA/B_DB_NO_HR respectively. When DEACTIVE flag is set, EPWMA/ B_DE are be driven by TRIPH, TRIPL, constant 0, or a constant 1 signal based on the configuration of the DEATCTL[PWMA], DEATCTL[PWMB], DEATCTL[TRIPSELA], DEATCTL[TRIPSELB] fields. When a PWMTRIP signal from the associated ePWM trips, EPWMA/B_DE are be driven by the input PWM signals configured through the DECTL[TRIPENABLE] field. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

707 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [497 x 271] intentionally omitted <==**

**----- Start of picture text -----**<br>
EPWMx_DE.sync<br>EPWMxA_DB_NO_HR 0<br>EPWMxA_DE.sclk<br>1<br>EPWMx_DE.async<br>DESTS[DEACTIVE] DEACTCTL EPWMxA 0 EPWMxA_DE<br>EPWMx_DE.sync [TRIPSELA] 1<br>EPWMxTRIPOUT DEACTCTL<br>(Synchronized  [PWMA]<br>in EPWM) TripH Sync 0<br>DEACTCTL[TRIPENABLE] TripL Sync 1 00<br>01<br>0 10<br>1 11<br>DESTS[DEACTIVE]<br>EPWMxB_DB_NO_HR 0<br>EPWMx_DE.async EPWMxB_DE.sclk<br>EPWMxTRIPOUT 1<br>EPWMx_DE.sync<br>DEACTCTL[TRIPENABLE] DEACTCTL EPWMxB 0<br>[TRIPSELB] DEACTCTL 1 EPWMxA_DE<br>[PWMB]<br>0<br>1 00<br>01<br>0 10<br>1 11<br>EPWMx_DE.async<br>**----- End of picture text -----**<br>


**Figure 7-234. Diode Emulation Circuit** 

Figure 7-235 shows an example waveform, in which DEACTCTL[PWMA] is configured to select TripL as the source, DEACTCTL[PWMB] is configured to select TripH as the source and DEACTCTL[PWMAPOL] and DEACTCTL[PWMBPOL] are both 0. 

**==> picture [60 x 133] intentionally omitted <==**

**----- Start of picture text -----**<br>
DEACTIVE<br>REENTRY_DLY_CNT<br>EPWMxSYNCPER<br>EPWMxA<br>EPWMxB<br>TRIPH_OR_TRIPL<br>TRIPH<br>TRIPL<br>EPWMxA_DE<br>EPWMxB_DE<br>**----- End of picture text -----**<br>


**==> picture [438 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
Diode Emulation Phase<br>**----- End of picture text -----**<br>


**Figure 7-235. Diode Emulation Mode Timing Diagram** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

708 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.11.4 DE Monitor**_ 

To detect extended DE phase, which is beyond the expected duration, a DE mode monitor counter, DEMONCNT, is provided. This 16-bit counter monitors the frequency of diode mode trip events. The counter if enabled, DEMONCTL[ENABLE], increments on a PWMSYNC event, in steps of DEMONSTEP[INCSTEP] when TRIPH_OR_TRIPL is high, and decrements on a PWMSYNC event, in steps of DEMONSTEP[DECSTEP] when TRIPH_OR_TRIPL is low. If counter exceeds DEMONTHRES[THRESHOLD], then a DEMONTRIP pulse is generated and the counter is cleared. The counter value is saturated to 0 during an underflow and 0xffff on an overflow. The counter is cleared when DECTL[ENABLE] is cleared. 

**==> picture [500 x 195] intentionally omitted <==**

**----- Start of picture text -----**<br>
DEACTIVE<br>DE_MONITOR_CNT 0x00000000 0x00000000 0x00000001 0x00000002 0x00000003 0x00000000<br>DEMONTRIP<br>EPWMxSYNCPER<br>EPWMxA<br>EPWMxB<br>TRIPH_OR_TRIPL<br>TRIPH<br>TRIPL<br>EPWMxA_DE<br>EPWMxB_DE<br>Diode Emulation Phase<br>**----- End of picture text -----**<br>


**Figure 7-236. DE Mode Monitor Sequence** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

709 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.6.12 Event-Trigger (ET) Submodule** 

The key functions of the event-trigger submodule are: 

- Receives event inputs generated by the time-base, counter-compare, and digital-compare submodules 

- Uses the time-base direction information for up/down event qualification 

- Uses prescaling logic to issue interrupt requests and ADC start of conversion at: 

   - Every event 

   - Every second event 

   - Up to every fifteenth event 

- Provides full visibility of event generation using event counters and flags 

- Allows software forcing of Interrupts and ADC start of conversion 

The event-trigger submodule manages the events generated by the time-base submodule, the counter-compare submodule, and the digital-compare submodule to generate an interrupt to the CPU and a start of conversion pulse to the ADC when a selected event occurs. 

Figure 7-237 illustrates the event-trigger submodule within the ePWM. 

**==> picture [500 x 271] intentionally omitted <==**

**Figure 7-237. Event-Trigger Submodule** 

710 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.12.1 Operational Overview of the ePWM Event-Trigger Submodule**_ 

The event-trigger submodule monitors various event conditions (shown as inputs on the left side of Figure 7-238 and can be configured to prescale these events before issuing an Interrupt request or an ADC start of conversion. The event-trigger prescaling logic can issue Interrupt requests and ADC start of conversion at: 

- Every event 

- Every second event 

- Up to every fifteenth event 

**==> picture [464 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
clear<br>CTR=Zero<br>Event Trigger<br>CTR=PRD Module Logic MCPWMxINT<br>/n PIE<br>ETSEL reg<br>CTR=Zero or PRD<br>count<br>CTRU=PWMx_CMPA ETPERIOD reg<br>clear<br>CTR=PWMx_CMPA CTRD=PWMx_CMPA<br>ETCNT reg<br>Direction<br>qualifier CTRU=PWMx_CMPB<br>SOCEN reg /n<br>CTR=PWMx_CMPA CTRD=PWMx_CMPB SOCA<br>SOCPERIOD reg count SOCB<br>CTRU=CMPC<br>ADC<br>CTR=CMPC CTRD=CMPC SOCCNT reg clear SOCC<br>SOCD<br>CTRU=CMPD INTEN reg<br>/n<br>CTR=CMPD CTRD=CMPD INTFLAG reg<br>count<br>CTR_dir INTFRC reg<br>INTCLR reg<br>**----- End of picture text -----**<br>


**Figure 7-238. Event-Trigger Submodule Showing Event Inputs and Prescaled Outputs** 

- ETSEL - This selects which of the possible events trigger an interrupt or start an ADC conversion. 

- ETPS - This programs the event prescaling options mentioned above. 

- ETFLG - These are flag bits indicating status of the selected and prescaled events. 

- ETCLR - These bits allow clearing the flag bits in the ETFLG register using software. 

- ETFRC - These bits allow software forcing of an event. Useful for debugging or software intervention. 

- ETINTPS - This programs the interrupt event prescaling options, supporting count and period up to 15 events. 

- ETSOCPS - This programs the SOC event prescaling options, supporting count and period up to 15 events. 

- ETCNTINITCTL - These bits enable ETCNTINIT initialization using SYNC event or using software force. 

- ETCNTINIT - These bits allow initializing INT/SOCA/SOCB counters on SYNC events (or software force) with user programmed value. 

A more detailed look at how the various register bits interact with the Interrupt and ADC start of conversion logic are shown in Figure 7-239, Figure 7-240, and Figure 7-241. 

Figure 7-239 shows the event-trigger's interrupt generation logic. The interrupt-period (ETPS[INTPRD]) bits specify the number of events required to cause an interrupt pulse to be generated. The choices available are: 

- Do not generate an interrupt. 

- Generate an interrupt on every event. 

- Generate an interrupt on every second event. 

- Generate an interrupt on every third event. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 711 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

The selection made on ETPS[INTPSSEL] bit determines whether ETPS [INTCNT, and INTPRD] registers or ETINTPS [ INTCNT2, and INTPRD2 ] registers bit fields determine frequency of events (interrupt once every 0-15 events). 

The event that can cause an interrupt is configured by the interrupt selection (ETSEL[INTSEL]) and (ETSEL[INTSELCMP]) bits. The event can be one of the following: 

- Time-base counter equal to zero (TBCTR = 0x00). 

- Time-base counter equal to period (TBCTR = TBPRD). 

- Time-base counter equal to zero or period (TBCTR = 0x00 || TBCTR = TBPRD). 

- Time-base counter equal to the compare A register (CMPA) when the timer is incrementing. 

- Time-base counter equal to the compare A register (CMPA) when the timer is decrementing. 

- Time-base counter equal to the compare B register (CMPB) when the timer is incrementing. 

- Time-base counter equal to the compare B register (CMPB) when the timer is decrementing. 

- Time-base counter equal to the compare C register (CMPC) when the timer is incrementing. 

- Time-base counter equal to the compare C register (CMPC) when the timer is decrementing. 

- Time-base counter equal to the compare D register (CMPD) when the timer is incrementing. 

- Time-base counter equal to the compare D register (CMPD) when the timer is decrementing. 

The number of events that have occurred can be read from the interrupt event counter ETPS[INTCNT] or ETINTPS[INTCNT2] register bits based off of the selection made using ETPS[INTPSSEL]. That is, when the specified event occurs the ETPS[INTCNT] or ETINTPS[INTCNT2] bits are incremented until the bits reach the value specified by ETPS[INTPRD] or ETINTPS[INTPRD2] determined again by the selection made in ETPS[INTPSSEL]. When ETPS[INTCNT] = ETPS[INTPRD], the counter stops counting and the counter output is set. The counter is only cleared when an interrupt is sent to the interrupt controller. 

When ETPS[INTCNT] reaches ETPS[INTPRD], the following behavior occurs. The following behavior is also applicable to ETINTPS[INTCNT2] and ETINTPS[INTPRD2]: 

- If interrupts are enabled, ETSEL[INTEN] = 1 and the interrupt flag is clear, ETFLG[INT] = 0, then an interrupt pulse is generated and the interrupt flag is set, ETFLG[INT] = 1, and the event counter is cleared ETPS[INTCNT] = 0. The counter begins counting events again. 

- If interrupts are disabled, ETSEL[INTEN] = 0, or the interrupt flag is set, ETFLG[INT] = 1, the counter stops counting events when the counter reaches the period value ETPS[INTCNT] = ETPS[INTPRD]. 

- If interrupts are enabled, but the interrupt flag is already set, then the counter holds the output high until the ENTFLG[INT] flag is cleared. This allows for one interrupt to be pending while one is serviced. 

Writing a 0 to the INTPRD bits automatically clears the counter (INTCNT = 0) and the counter output resets (so no interrupts are generated). For all other writes to INTPRD, INTCNT retains the previous value. INTCNT resets when INTCNT overflows. Writing a 1 to the ETFRC[INT] bit increments the event counter INTCNT. The counter behaves as previously described when INTCNT = INTPRD. When INTPRD = 0, the counter is disabled and hence no events are detected and the ETFRC[INT] bit is also ignored. The same applies to ETINTPS[INTCNT2] and ETINTPS[INTPRD2]. 

The previous definition means that an interrupt on every event, on every second event, or on every third event if using the INTCNT and INTPRD can be generated. An interrupt on every event up to 15 events if using the INTCNT2 and INTPRD2 can be generated. 

The INTCNT2 value can be initialized with the value from ETCNTINIT[INTINIT] based on the selection made in ETCNTINITCTL[INTINITEN]. When ETCNTINITCTL[INTINITEN] is set, then initialization of INTCNT2 counter with contents of ETCNTINIT[INTINIT] on a SYNC event or software force is determined by ETCNTINITCTL[INTINITFRC]. 

## **ETINTMIX, ETSOCAMIX and ETSOCBMIX Signals** 

In type 5 ePWM, the Event-Trigger submodule can generate and use ETINTMIX, ETSOCAMIX and ETSOCBMIX signals. 

- **ETINTMIX** : This signal is a generated from the ORed combination of the sources enabled in the ETINTMIXEN register. The ETINTMIX signal can be used as a source for the EPWMxINT interrupt. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

712 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- **ETSOCAMIX** : This signal is a generated from the ORed combination of the sources enabled in the ETSOCAMIXEN register. The ETSOCAMIX signal can be used as a source for the EPWMxSOCA trigger signal. 

- **ETSOCBMIX** : This signal is a generated from the ORed combination of the sources enabled in the ETSOCBMIXEN register. The ETSOCBMIX signal can be used as a source for the EPWMxSOCB trigger signal 

**==> picture [474 x 252] intentionally omitted <==**

**----- Start of picture text -----**<br>
ETFLG[INT]<br>ETPS[INTCNT] ETINTPS[INTCNT2]<br>ETCLR[INT] Clear<br>Latch 0 1<br>Set ETPS[INTPSSEL]<br>ETSEL[INTSEL]<br>Generate 1 0<br>Interrupt Clear CNT 000 0<br>EPWMxINT Pulse<br>001 CTR = Zero<br>When<br>Input = 1 0 Counter4-bit ETFRC[INT] 010011 ETINTMIXCTR = PRD<br>0 CTRU = CMPA<br>ETSEL[INT] Inc CNT 100 1 CTRU = CMPC<br>ETCNTINIT[INTINIT] 4 4 101 01 CTRD = CMPACTRD = CMPC<br>ETCNTINITCTL[INTINITFRC] 0 CTRU = CMPB<br>110<br>1 CTRU = CMPD<br>EPWMxSYNCI<br>0 CTRD = CMPB<br>111<br>1 CTRD = CMPD<br>ETCNTINITCTL[INTINITEN] 0 1 ETPS[INTPSSEL]<br>ETPS[INTPRD] ETINTPS[INTPRD2] ETSEL[INTSELCMP]<br>**----- End of picture text -----**<br>


**Figure 7-239. Event-Trigger Interrupt Generator** 

Figure 7-240 shows the operation of the event-trigger's start-of-conversion-A (SOCA) pulse generator. The enhancements include SOCASELCMP and SOCBSELCMP bit fields defined in the ETSEL register enable CMPC and CMPD events respectively to cause a start of conversion. The ETPS[SOCPSSEL] bit field determines whether SOCACNT2 and SOCAPRD2 take control or not. The ETPS[SOCACNT] counter and ETPS[SOCAPRD] period values behave similarly to the interrupt generator except that the pulses are continuously generated. That is, the pulse flag ETFLG[SOCA] is latched when a pulse is generated, but the interrupt generator does not stop further pulse generation. The enable and disable bit ETSEL[SOCAEN] stops pulse generation, but input events can still be counted until the period value is reached as with the interrupt generation logic. The event that triggers an SOCA and SOCB pulse can be configured separately in the ETSEL[SOCASEL] and ETSEL[SOCBSEL] bits. The possible events are the same events that can be specified for the interrupt generation logic with the addition of the DCAEVT1.soc and DCBEVT1.soc event signals from the digital compare (DC) submodule. The SOCACNT2 initialization scheme is very similar to the interrupt generator with respective enable, value initialize and SYNC or software force options. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 713 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [491 x 252] intentionally omitted <==**

**----- Start of picture text -----**<br>
ETFLG[SOCA]<br>ETPS[SOCACNT] ETSOCPS[SOCACNT2]<br>ETCLR[SOCA] Clear<br>Latch 0 1<br>Set ETPS[SOCPSSEL]<br>ETSEL[SOCASEL]<br>Generate ClrCNT 000 DCAEVT1.soc<br>EPWMxSOCA SOC 001 CTR = Zero<br>Pulse 4-bit ETFRC[SOCA] 010 CTR = PRD<br>When Counter 011 ETSOCAMIX<br>Input = 1<br>ETSEL[SOCA] Inc CNT 100 01 CTRU = CMPCCTRU = CMPA<br>ETCNTINIT[SOCAINIT] 4 4 101 01 CTRD = CMPACTRD = CMPC<br>ETCNTINITCTL[SOCAINITFRC] 110 0 CTRU = CMPB<br>1 CTRU = CMPD<br>EPWMxSYNCI<br>111 0 CTRD = CMPB<br>1 CTRD = CMPD<br>ETCNTINITCTL[SOCAINITEN] 0 1 ETPS[SOCPSSEL]<br>ETPS[SOCAPRD] ETSOCPS[SOCAPRD2] ETSEL[SOCASELCMP]<br>**----- End of picture text -----**<br>


NOTE: The DCAEVT1.soc signals are generated by the Digital Compare (DC) submodule 

**Figure 7-240. Event-Trigger SOCA Pulse Generator** 

Figure 7-241 shows the operation of the event-trigger's start-of-conversion-B (SOCB) pulse generator. The event-trigger's SOCB pulse generator operates the same way as the SOCA. 

**==> picture [456 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>
ETFLG[SOCB]<br>ETPS[SOCBCNT] ETSOCPS[SOCBCNT2]<br>ETCLR[SOCB] Clear<br>Latch 0 1<br>Set ETPS[SOCPSSEL]<br>ETSEL[SOCBSEL]<br>Generate 000 DCBEVT1.soc<br>SOC ClrCNT 001 CTR = Zero<br>EPWMxSOCB Pulse 010 CTR = PRD<br>When 4-bit ETFRC[SOCB] 011 ETSOCBMIX<br>Input = 1 Counter<br>0 CTRU = CMPA<br>ETSEL[SOCB] Inc CNT 100 1 CTRU = CMPC<br>ETCNTINIT[SOCBINIT] 4 4 101 01 CTRD = CMPACTRD = CMPC<br>ETCNTINITCTL[SOCBINITFRC] 0 CTRU = CMPB<br>110<br>1 CTRU = CMPD<br>EPWMxSYNCI<br>111 0 CTRD = CMPB<br>1 CTRD = CMPD<br>ETCNTINITCTL[SOCBINITEN] 0 1 ETPS[SOCPSSEL]<br>ETPS[SOCBPRD] ETSOCPS[SOCBPRD2] ETSEL[SOCBSELCMP]<br>**----- End of picture text -----**<br>


NOTE: The DCBEVT1.soc signals are generated by the Digital Compare (DC) submodule 

**Figure 7-241. Event-Trigger SOCB Pulse Generator** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

714 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.6.13 Digital Compare (DC) Submodule** 

Figure 7-242 illustrates where the digital compare (DC) submodule signals interface to other submodules in the ePWM system. 

**==> picture [500 x 381] intentionally omitted <==**

**Figure 7-242. The Digital Compare Architecture** 

On this device, any of the GPIO pins can be flexibly mapped to be the trip-zone input and trip inputs to the trip-zone submodule and digital compare submodule. The Input X-BAR Input Select (INPUTxSELECT) register defines which GPIO pins gets assigned to be the trip-zone inputs / trip inputs. 

The digital compare (DC) submodule compares signals external to the ePWM module (for instance, CMPSSx signals from the analog comparators) to directly generate PWM events/actions which then feed to the eventtrigger, trip-zone, and time-base submodules. Additionally, blanking window functionality is supported to filter noise or unwanted pulses from the DC event signals. 

## **Note** 

The user is responsible for driving the correct state on the selected pin before enabling the clock and configuring the trip input for the respective ePWM peripheral to avoid spurious latch of the TRIP signal. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 715 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [448 x 253] intentionally omitted <==**

**Figure 7-243. GPIO MUX-to-Trip Input Connectivity** 

716 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.13.1 Purpose of the Digital Compare Submodule**_ 

The key functions of the digital compare submodule are: 

- Analog comparator (COMP) module outputs fed though the Input X-BAR, EPWM X-BAR, externally using the GPIO peripheral, interrupt controller signals, ECC error signals, TZ1, TZ2, and TZ3 inputs generate Digital Compare A High/Low (DCAH, DCAL) and Digital Compare B High/Low (DCBH, DCBL) signals. 

- DCAH/L and DCBH/L signals trigger events that can then either be filtered or applied directly to the trip-zone, event-trigger, and time-base submodules to: 

   - generate a trip zone interrupt 

   - generate an ADC start of conversion 

   - force an event 

   - generate a synchronization event for synchronizing the ePWM module TBCTR. 

- Event filtering (blanking window logic) can optionally blank the input signal to remove noise. 

## _**7.5.6.13.2 Enhanced Trip Action Using CMPSS**_ 

To allow multiple CMPSS at a time to affect DCA/BEVTx events and trip actions, there is a OR logic to bring together ALL trip inputs (up to 15) from sources external to the ePWM module and feed into DCAH, DCAL, DCBH, and DCBL as a “combinational input” using the DCTRIPSEL register. This is configured by selecting “Trip combination input” (value of 0xF) in the DCTRIPSEL register. 

There is a discrete choice of which trip inputs to put through the combinational logic for generating the DCAH, DCAL, DCBH, and DCBL signals. This is achieved using the DCAHTRIPSEL, DCALTRIPSEL, DCBHTRIPSEL, and DCBLTRIPSEL register selections. Inputs selected for combinational input are passed through to the DCTRIPSEL register. 

## _**7.5.6.13.3 Using CMPSS to Trip the ePWM on a Cycle-by-Cycle Basis**_ 

When using the CMPSS to trip the ePWM on a cycle-by-cycle basis, steps can be taken to prevent an asserted comparator trip state in one PWM cycle from extending into the following cycle. The CMPSS can be used to signal a trip condition to the downstream ePWM modules. For applications like peak current mode control, only one trip event per PWM cycle is expected. Under certain conditions, it is possible for a sustained or late trip event (arriving near the end of a PWM cycle) to carry over into the next PWM cycle if precautions are not taken. If either the CMPSS Digital Filter or the ePWM Digital Compare (DC) submodule is configured to qualify the comparator trip signal, “N” number of clock cycles of qualification are introduced before the ePWM trip logic can respond to logic changes of the trip signal. Once an ePWM trip condition is qualified, the trip condition remains active for N clock cycles after the comparator trip signal has de-asserted. If a qualified comparator trip signal remains asserted within N clock cycles prior to the end of a PWM cycle, the trip condition is not cleared until after the following PWM cycle has started. Thus, the new PWM cycle detects a trip condition as soon as the cycle begins. 

To avoid this undesired trip condition, the application can take steps to make sure that the qualified trip signal seen by the ePWM trip logic is deasserted prior to the end of each PWM cycle. This can be accomplished through various methods: 

- Design the system such that a comparator trip is not asserted within N clock cycles prior to the end of the PWM cycle. 

- Activate blanking of the comparator trip signal using the ePWM event filter at least two clock cycles prior to the PWMSYNCPER signal and continue blanking for at least N clock cycles into the next PWM cycle. 

- If the CMPSS COMPxLATCH path is used, clear the COMPxLATCH at least N clock cycles prior to the end of the PWM cycle. The latch can be cleared by software (using COMPSTSCLR) or by generating an early PWMSYNCPER signal. The ePWM modules on this device include the ability to generate PWMSYNCPER upon a CMPC or CMPD match (using HRPCTL) for arbitrary PWMSYNCPER placement within the PWM cycle. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

717 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.13.4 Operation Highlights of the Digital Compare Submodule**_ 

The following sections describe the operational highlights and configuration options for the digital compare submodule. 

## _**7.5.6.13.4.1 Digital Compare Events**_ 

As described in Section 7.5.6.13.1, trip zone inputs (TZ1, TZ2, and TZ3) and CMPSSx signals from the analog comparator (COMP) module can be selected using the DCTRIPSEL bits to generate the Digital Compare A High and Low (DCAH/L) and Digital Compare B High and Low (DCBH/L) signals. Then, the configuration of the TZDCSEL register qualifies the actions on the selected DCAH/L and DCBH/L signals, which generate the DCAEVT1/2 and DCBEVT1/2 events (Event Qualification A and B). 

## **Note** 

The TZn signals, when used as a DCEVT tripping functions, are treated as a normal input signal and can be defined to be active-high or active-low inputs. ePWM outputs are asynchronously tripped when either the TZn, DCAEVTx.force, or DCBEVTx.force signals are active. For the condition to remain latched, a minimum of 3 ˟ TBCLK sync pulse width is required. If pulse width is < 3*TBCLK sync pulse width, the trip condition can or can not get latched by CBC or OST latches. 

The DCAEVT1/2 and DCBEVT1/2 events can then be filtered to provide a filtered version of the event signals (DCEVTFILT) or the filtering can be bypassed. Filtering is discussed further in Event Filtering. Either the DCAEVT1/2 and DCBEVT1/2 event signals or the filtered DCEVTFILT event signals can generate a force to the trip zone module, a TZ interrupt, an ADC SOC, or a PWM sync signal. 

- **force signal:** DCAEVT1/2.force signals force trip zone conditions which either directly influence the output on the EPWMxA pin (using TZCTL, TZCTLDCA, TZCTLDCB register configurations) or, if the DCAEVT1/2 signals are selected as one-shot or cycle-by-cycle trip sources (using the TZSEL register), the DCAEVT1/2.force signals can effect the trip action using the TZCTL or TZCTL2 register configurations. The DCBEVT1/2.force signals behaves similarly, but affect the EPWMxB output pin instead of the EPWMxA output pin. 

The priority of conflicting actions on the TZCTL, TZCTL2, TZCTLDCA and TZCTLDCB registers is as follows (highest priority overrides lower priority): 

## Output EPWMxA: 

- TZA (highest) -> DCAEVT1 -> DCAEVT2 (lowest) 

- TZAU (highest) -> DCAEVT1U -> DCAEVT2U (lowest) 

- TZAD (highest) -> DCAEVT1D -> DCAEVT2D (lowest) 

Output EPWMxB: 

   - TZB (highest) -> DCBEVT1 -> DCBEVT2 (lowest) 

   - TZBU (highest) -> DCBEVT1U -> DCBEVT2U (lowest) 

   - TZBD (highest) -> DCBEVT1D -> DCBEVT2D (lowest) 

- **interrupt signal:** DCAEVT1/2.interrupt signals generate trip zone interrupts to the interrupt controller. To enable the interrupt, set the DCAEVT1, DCAEVT2, DCBEVT1, or DCBEVT2 bits in the TZEINT register. Once one of these events occurs, an EPWMxTZINT interrupt is triggered, and the corresponding bit in the TZCLR register must be set to clear the interrupt. 

- **soc signal:** The DCAEVT1.soc signal interfaces with the event-trigger submodule and can be selected as an event which generates an ADC start-of-conversion-A (SOCA) pulse using the ETSEL[SOCASEL] bit. Likewise, the DCBEVT1.soc signal can be selected as an event which generates an ADC start-of-conversionB (SOCB) pulse using the ETSEL[SOCBSEL] bit. 

- **sync signal:** The DCAEVT1.sync and DCBEVT1.sync events are ORed with the EPWMxSYNCI input signal and the TBCTL[SWFSYNC] signal to generate a synchronization pulse to the time-base counter. 

Figure 7-244 and Figure 7-245 show how the DCxEVT1, DCxEVT2, or DCEVTFLT signals are processed to generate the digital compare A and B event force, interrupt, soc and sync signals. 

718 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

In some of the applications like Phase Shifted Full Bridge (PSFB) Converters, it is required that different actions are taken on a CBC trip event and an OST trip event. This can be achieved using the DCxEVT1LAT. 

- This latch can be cleared on CNT=0, CTR=PRD, and CNT=0 OR CTR=PRD events based on the setting of DCxCTL.EVTy.LATCLRSEL setting. This is similar to CBC latch clear mechanism. 

- DCxEVTy.force signal can be chosen to be either the latched version or the unlatched version based on DCxCTL.EVTyLATSEL value. 

- The status of DCxEVTyLAT signal can be accessed by reading DCxCTL.EVTyLAT field. 

**==> picture [500 x 315] intentionally omitted <==**

**----- Start of picture text -----**<br>
DCxCTL[EVT1LATSEL] DCxCTL[EVT1LATCLRSEL]<br>DCxCTL[EVT1FRCSYNCSEL]<br>DCxCTL[EVT1SRCSEL] CLEAR<br>00 CNT_ZERO<br>SET 01 PRD_EQ<br>1 10<br>DCEVTFILT 1 async DCxEVT1LAT 0 11 Reserved<br>1<br>0<br>DCxEVT1<br>Sync 0<br>DCxEVT1.force<br>TZEINT[DCxEVT1]<br>TBCLK<br>set<br>TBCLK Latch DCxEVT1.inter<br>clear<br>Pulse Gen<br>TZCLR[DCxEVT1] TZFLG[DCxEVT1]<br>DCxEVT1.soc<br>TBCLK<br>TBCLK DCxCTL[EVT1SOCE]<br>Pulse Gen<br>DCxEVT1.sync<br>TZFRC[DCxEVT1]<br>TBCLK<br>DCxCTL[EVT1SYNCE]<br>**----- End of picture text -----**<br>


**Figure 7-244. DCxEVT1 Event Triggering** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

719 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
DCxCTL[EVT2LATSEL] DCxCTL[EVT2LATCLRSEL]<br>DCxCTL[EVT2FRCSYNCSEL]<br>DCxCTL[EVT2SRCSEL] CLEAR<br>00 CNT_ZERO<br>SET 01 PRD_EQ<br>1 10<br>DCEVTFILT 1 async DCxEVT2LAT 0 11 Reserved<br>1<br>0<br>DCxEVT2<br>Sync 0<br>DCxEVT2.force<br>TZEINT[DCxEVT2]<br>TBCLK<br>set<br>TBCLK Latch DCxEVT2.inter<br>clear<br>Pulse Gen<br>TZCLR[DCxEVT2] TZFLG[DCxEVT2]<br>TZFRC[DCxEVT2]<br>TBCLK<br>**----- End of picture text -----**<br>


**Figure 7-245. DCxEVT2 Event Triggering** 

## **Note** 

In some of the applications like Phase Shifted Full Bridge (PSFB) Converters, DCxEVT1LAT can be used on a CBC trip event and an OST trip event. 

720 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.13.4.2 Valley Switching**_ 

Event filtering depicts the valley switching function along with the event filtering logic described in Section 7.5.6.13.4.3. This function can be used to achieve programmable valley switching without any additional external circuitry. This module provides an on-chip hardware mechanism that can: 

- Capture the oscillation period 

- Accurately delay the PWM switching instant 

- Allow a programmable number of edges before the delay takes effect 

- Provide multiple choices of triggers and events 

- Allow easy adaptability for optimum performance under changing system/operating conditions 

The DCxEVTy signal needs further processing to support valley switching. Here is a brief description of how valley switching function is enabled: 

1. Select one of the DCxEVTy events as input to the valley switching block (DCFCTL[SRCSEL]) with an option to add the blanking window (Blank Control Logic). This is where the comparator output (or external input) above is selected as an input to the valley switching block. 

2. Configure the edge filter to capture ‘n’ rising, falling or both edges through the edge selection logic (DCFCTL[EDGEMODE, EDGECOUNT]). 

3. Select the correct event to reset and restart the edge filter (VCAPCTL[TRIGSEL]). Edge capturing event is triggered or armed by this selected edge. 

4. Enable valley capture logic (VCAPCTL[VCAPE]). 

5. Select the start edge that indicates the start of capture for oscillation period measurement (VCNTCFG[STARTEDGE]). This is where the 16-bit counter starts counting. 

6. Select the stop edge (VCNTCFG[STOPEDGE]) that indicates the edge at which the 16-bit counter stops counting. The captured counter value (CNTVAL) provides oscillation period information. 

   - The STOPEDGE value must always be greater than STARTEDGE value. 

7. Configure and apply the captured delay (CNTVAL) to the edge filtered DCxEVTy signal. The CNTVAL value can be applied as is or applied in conjunction with a software programmed value (useful for offset adjustment) (SWVDELVAL) or only a fraction of the delay can be applied with or without SWVDELVAL. This is useful to correctly apply a delay corresponding to the valley point. (VCAPCTL[VDELAYDIV]) 

8. Configure VCAPCTL[EDGEFILTDLYSEL] to apply hardware delay based on the captured value above. 

Once the counter is stopped, counter value is copied into CNTVAL register and counter is reset to zero. No further captures are done until the logic is triggered again by occurrence of event selected by VCAPCTL[TRIGSEL]. In this implementation, the software trigger is used as the source for VCAPCTL[TRIGSEL]. Upon occurrence of the trigger event, irrespective of the current status of the counter, the counter is reset and starts counting from zero upon occurrence of the STARTEDGE. Similarly, upon occurrence of the trigger event, the edge filter is reset and starts counting from zero upon occurrence of the STARTEDGE. 

Output from the valley switching block (DCEVTFILT) is then used to synchronize the PWM time-base. The process is shown in Figure 7-246. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 721 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 375] intentionally omitted <==**

**----- Start of picture text -----**<br>
DCCAP[15:0] Reg<br>TBCNT(16)<br>PRD_eq Blank DCFCTL[BLANKE, PULSESEL]<br>CNT_zero Control DCFOFFSET[OFFSET] PRD_eq<br>TBCLK Logic DCFWINDOW[WINDOW] CNT_zeroTBCLK CaptureControlLogic<br>DCCAPCTL[CAPE, SHDWMODE]<br>BLANKWDW<br>DCFCTL[PULSESEL]<br>DCFCTL[INVERT]<br>Sync 0<br>0     1<br>TBCLK 1<br>DCAEVT1 00<br>DCAEVT2 01 async 0 DCEVTFILT<br>DCBEVT1 10<br>EDGE FILTER<br>DCBEVT2 11  Reset 0 1<br>Edge<br>Selection         Edge Fiter 1<br>Logic Delay  DFCTL[EDGEFILTSEL]<br>DCFCTL[SRCSEL]<br>VCAPCTL[EDGEFILTDLYSEL]<br>DCFCTL[EDGEMODE,<br>1 EDGECOUNT]<br>HWVDELVAL Hardware<br>VCAPCTL[TRIGSEL] VCAPCTL[VCAPE] 0 calculated<br>Delay<br>Software 000 SWVDELVAL Edge Procesisng/ VCAPCTL[VDELAYDIV]<br>CNT_zero 001 Delay generation<br>PRD_eq 010<br>PRDCNT_zero_eq or  011 Edge Start CNTVAL<br>DCAEVT1 100 Capture Stop      16 bit Counter<br>Edge Capture Trigger Logic<br>DCAEVT2 101<br>Reset<br>110<br>DCBEVT1<br>111<br>DCBEVT2<br>TBCLK<br>**----- End of picture text -----**<br>


**Figure 7-246. Valley Switching** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

722 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.13.4.3 Event Filtering**_ 

**Blank Control Logic:** The DCAEVT1/2 and DCBEVT1/2 events can be filtered using event filtering logic to remove noise by optionally blanking events for a certain period of time. This is useful for cases where the analog comparator outputs can be selected to trigger DCAEVT1/2 and DCBEVT1/2 events, and the blank control logic is used to filter out potential noise on the signal prior to tripping the PWM outputs or generating an interrupt or ADC start-of-conversion. Blank control logic is used to define a blanking window, which ignores all event occurrences on the signal while the window is active. The blanking window is configured in the DCFCTL, DCFOFFSET, and DCFWINDOW registers. The DCFCTL register enables the blanking window and aligns the blanking window to either a CTR = PRD pulse or a CTR = 0 pulse or both CTR = PRD and CTR = 0 as specified by DCFCTL[PULSESEL]. DCFCTL[SRCSEL] selects the DCxEVTy event source for the DCEVTFILT signal. An offset value in TBCLK counts is programmed into the DCFOFFSET register, which determines at what point after the CTR = PRD or CTR = 0 pulse the blanking window starts. The duration of the blanking window, in number of TBCLK counts after the offset counter expires, is written to the DCFWINDOW register by the application. Before and after the blanking window ends, events can generate soc, sync, interrupt, and force signals as before. Figure 7-247 shows the details of the event filtering logic. 

**==> picture [452 x 256] intentionally omitted <==**

**----- Start of picture text -----**<br>
DCCAP[15:0] Reg<br>CTR=PRD Blank DCFCTL[BLANKE, PULSESEL]<br>CTR=Zero Control DCFOFFSET[OFFSET]<br>TBCLK Logic TBCTR(16)<br>DCFWINDOW[WINDOW]<br>CTR = PRD Capture<br>CTR = 0<br>BLANKWDW EPWMxBLANK to CMPSS Control<br>TBCLK<br>Logic<br>DCFCTL[INVERT]<br>DCCAPCTL[CAPE, SHDWMODE]<br>DCFCTL[PULSESEL]<br>Sync<br>1      0<br>TBCLK<br>DCAEVT1 00<br>DCAEVT2 01 async DCEVTFILT<br>DCBEVT1 10<br>DCBEVT2 11<br>DCFCTL[SRCSEL]<br>**----- End of picture text -----**<br>


**Figure 7-247. Event Filtering** 

**Capture Control Logic:** The event filtering can also capture the TBCTR value of the selected DCxEVTy event as configured in the DCCAPCTL register. When capture control logic is enabled, the selected DCxEVTy event triggers capture of the TBCTR to the active register. The CPU reads directly from the active register unless shadow mode is enabled by DCCAPCTL[SHDWMODE]. When shadow mode is enabled, the active register information is copied to shadow register on the event specified by DCFCCTL[PULSESEL], and the CPU reads from the shadow register. After the selected DCxEVTy event, no further capture events occur until the event specified by DCCAPCTL[CAPMODE]. The CAPMODE can be configured two ways: (1) no further capture events occur until the event defined by DCFCTL[PULSESEL] or (2) no further capture events occur until the compare-event flag at DCCAPCTL[CAPSTS] is cleared by DCCAPCTL[CAPCLR]. 

Figure 7-248 illustrates several timing conditions for the offset and blanking window within an ePWM period. Notice that if the blanking window crosses the CTR = 0 or CTR = PRD boundary, the next window still starts at the same offset value after the CTR = 0 or CTR = PRD pulse. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 723 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [473 x 278] intentionally omitted <==**

**----- Start of picture text -----**<br>
Period<br>TBCLK<br>CTR = PRD<br>or CTR = 0<br>Offset(n) Offset(n+1)<br>BLANKWDW Window(n) Window(n+1)<br>Offset(n) Offset(n+1)<br>BLANKWDW Window(n) Window(n+1)<br>Offset(n) Offset(n+1) Window(n+1)<br>BLANKWDW Window(n) Not Blanked<br>Overlap<br>Offset(n) Offset(n+1) Window(n+1)<br>BLANKWDW Window(n)<br>Aligned<br>**----- End of picture text -----**<br>


**Figure 7-248. Blanking Window Timing Diagram** 

## **BLANKPULSEMIX Signals** 

The DCFCTL MUX (available for Blank Control Logic and Capture Control Logic) has new options that allows the mux to select the BLANKPULSEMIX signal. The BLANKPULSEMIX signal is used, if the signal is selected by DCFCTL[PULSESEL] 

724 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **BLANKPULSEMIX and DCCAPMIX Signals** 

The CAPCTL MUX (available in the Capture Control Logic) and DCFCTL MUX (available for Blank Control Logic and Capture Control Logic) have new options in type 5 ePWM which allows them to select the DCCAPMIX or BLANKPULSEMIX signal respectively. 

In type 5 ePWM, the shadow load signal for the Capture Control Logic can be different from the blanking window alignment signal (which is selected by DCFCTL[PULSESEL]). The CAPCTL mux can be configured to use the DCCAPMIX signal 

**==> picture [253 x 290] intentionally omitted <==**

**----- Start of picture text -----**<br>
BLANKPULSEMIXSEL<br>Time-Base<br>Events<br>TBCTR == ZRO<br>TBCTR == PRD<br>TBCTR == CAU BLANKPULSEMIX<br>.<br>.<br>.<br>TBCTR == CDU<br>TBCTR == CDD<br>DCCAPMIXSEL<br>Time-Base<br>Events<br>TBCTR == ZRO<br>TBCTR == PRD<br>TBCTR == CAU DCCAPMIX<br>.<br>.<br>.<br>TBCTR == CDU<br>TBCTR == CDD<br>**----- End of picture text -----**<br>


**Figure 7-249. BLANKPULSEMIX and DCCAPMIX Signal Source** 

## _**7.5.6.13.4.4 Event Detection**_ 

This logic is primarily intended to detect an occurrence of a trip event in a configured time window. The window is configured by MIN and MAX values configured in the XMINMAX register sets. 

Figure 7-250 indicates the window spread across MIN and MAX bounds and the edge of the chosen signal occurring in that window. The purpose of this block is to detect the occurrence of such edge. If no such edge occurs, this module generates a trip event as well as an interrupt, if configured. 

**==> picture [82 x 17] intentionally omitted <==**

**----- Start of picture text -----**<br>
MIN<br>MAX<br>**----- End of picture text -----**<br>


**Figure 7-250. MIN, MAX Settings and Window for Capture Event Detection** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 725 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.13.4.4.1 Input Signal Detection**_ 

The CAPTRIPSEL, CAPINTRIPSEL and CAPGATETRIPSEL muxes are used for signal selection. Figure 7-251 shows how the CAPIN and CAPGATE signal source is selected. 

**CAPIN Input** : This signal (any input coming from EPWM X-BAR) can be configured as the signal input on which the edge detection logic is performed. 

**CAPGATE Input** : This signal (any input coming from EPWM X-BAR) can be configured as the gating signal to Min/Max logic. This signal gates the CAPIN input signal. 

**==> picture [472 x 205] intentionally omitted <==**

**----- Start of picture text -----**<br>
TRIPIN1<br>to  Capture<br>TRIPIN15 Control<br>Logic<br>CAPTRIPSEL[CAPGATECOMPSEL] CAPIN.sync<br>TBCLK<br>CAPCTL[SRCSEL]<br>CAPGATE.sync Sync<br>DFCTL[EDGEFILTSEL]<br>TBCLK Sync<br>CAPGATETRIPSEL Blank<br>Control<br>TBCLK Logic<br>CAPIN.sync Sync<br>DCAEVT1<br>DCAEVT2 async<br>DCEVFILT<br>Edge<br>CAPTRIPSEL[CAPINCOMPSEL] Filter<br>Logic<br>CAPINTRIPSEL<br>DCFCTL[SRCSEL] DCFCTL[EDGEFILTSEL]<br>DCBEVT2<br>DCBEVT1<br>CAPEVT<br>CAPEVT.inter<br>**----- End of picture text -----**<br>


**Figure 7-251. CAPIN and CAPGATE Source Selection** 

Once selected, Figure 7-252 demonstrates how the CAPGATE and CAPIN signals propagate into the counter capture logic. The logic works in the following way: 

- CAPCTL[GATEPOL] is used for the polarity selection of the gating input to be optionally inverted or tied to a 0 or 1. 

- CAPCTL[CAPINPOL] can be used to select the edge polarity of CAPIN.sync signal. CAPIN.sync signal is selected from the DCEVTFILT options and the CAPIN signal using CAPCTL[SRCSEL] bits. 

726 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [500 x 288] intentionally omitted <==**

**Figure 7-252. Counter Capture Logic** 

## _**7.5.6.13.4.4.2 MIN and MAX Detection Circuit**_ 

The XMINMAX register has XMIN and XMAX fields that can be programmed to set the MIN and MAX limits of the programmable edge detection window. These registers have 3-level buffering similar to the XCMPn registers. The shadow to active loading of these registers is always in sync with the buffer pointers. Any shadow to active loads occur as per the XLOAD register configuration defined for the XCMPn registers such that the MIN and MAX values used are always in line with the corresponding XPRD/XCMPn values used for a given PWM cycle. 

The logic works in the following way: 

- The TBCNT value is continually monitored and compared against the active MIN value. Match of TBCNT to the active MIN value triggers the edge monitoring occurrence. 

- When the TBCNT value reached the MIN value, the active LOAD signal is monitored waiting for an edge event to occur. 

- If an edge vent occurs before TBCNT reaches the active MAX value, then no further action is taken. The logic resets and TBCNT is compared to the active MIN value again. 

- If no edge occurs and TBCNT reaches the active MAX value, then the CAPEVT signal is set high and a CAP interrupt signal can also be generated. The CAPEVT signal needs to be cleared through software for TBCNT to be monitored against the MIN value again. 

The Min and Max monitoring is enabled and disabled in three ways: 

- By enabling/disabling the circuit via the DCCAPCTL[CAPE] bit 

- By the CAPGATE signal which can be sourced from an TRIPINPUT signal to the module. 

- By writing the same value into the XMIN and XMAX bits. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 727 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [257 x 18] intentionally omitted <==**

**----- Start of picture text -----**<br>
MIN<br>MAX<br>**----- End of picture text -----**<br>


**==> picture [55 x 44] intentionally omitted <==**

**Figure 7-253. Capture Logic Boundary Condition** 

## **Note** 

Possible boundary condition of MIN/MAX window exceeding the period value: In this case, the XMAX bit can have a value lower than the XMIN bit such that the window can go over the period boundary. 

## **7.5.6.14 XCMP Submodule** 

## _**7.5.6.14.1 XCMP Complex Waveform Generator Mode**_ 

The XCMP complex waveform generator mode is available in the type 5 ePWM and is enabled when XCMPEN is set. The main feature of the XCMP mode is to generate multiple ePWM pulses, with high resolution edge placement if needed, within one ePWM period. 

XCMP features include: 

- Up to eight counter compare registers XCMP1-XCMP8 

- High resolution (HRPWM) edge placement support 

- Up-Count counter mode support 

## **Note** 

Down-Count and Up-Down-Count counter modes are not supported 

- Pulse generation is only supported on XCMP1-8 matches (no support for counter events such as PRD and ZRO, or T1/T2 events) 

- ePWM module synchronization is not allowed in XCMP mode 

## **Note** 

The application software must disable the ePWM synchronization when XCMP mode is enabled. 

- XCMP1-8 are loaded through CMPA and CMPB 

## **Note** 

A minimum of 4 cycles difference (including the HR component) between adjacent XCMP values must be maintained to make sure of minimum pulse width. 

- The eight XCMPn registers, can be allocated to either CMPA or CMPB through the application software configuration 

- XAQCTLA and XAQCTLB registers determine the actions taken on the ePWM output for each XCMP1-8 counter matches 

- Up to three ePWM period cycles can be configured at once through three shadow buffers 

   - Each shadow buffer contains shadow registers for XCMP1-8, XTBPRD, XAQCTLA, XAQCTLB, CMPC, CMPD, and XMINMAX (which is used for CAPEVT signal generation) 

   - Shadow buffer SHDW2 and SHDW3 can be repeated up to eight times 

- All ePWM modules can be linked to trigger the start of their shadow loading at the same time through EPWMXLINKXLOAD 

## _**7.5.6.14.2 MIN-MAX Event Logic**_ 

The XMINMAX register has XMIN and XMAX fields that can be programmed to set the MIN and MAX limits of the programmable edge detection window. CAPIN signal (any input coming from EPWM X-BAR) can be 

728 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

configured as the signal input on which the edge detection logic is performed.TheDCCAP captures the rising or falling edge of the gated CAPIN signal. 

The XMIN and XMAX shadowing occurs following the same logic as the XCMPn registers. The XLOADCTL register configures the shadowing for the XMAX and XMIN values. 

## **Note** 

XMIN and XMAX values can be written in way that the TBCTR=PRD event falls within their range. For example, TBPRD = 100, XMIN = 95, XMAC = 5 is a valid configuration. 

## _**7.5.6.14.3 XCMP Shadow Buffers**_ 

Three SHDW buffers are available for XCMP configurations. Each SHDW buffer contains the XCMP1-8 values (CMPA and CMPB values), XTBPRD (TBPRD value), XCMPC (CMPC value), XCMPD (CMPD value), XAQCTLA and XAQCTLB. Each SHDW buffer also contains the XMINMAX values which are used for CAPEVT signal generation. 

With the three SHDW buffer (SHDW1, SHDW2 and SHDW3) the values used for the upcoming ePWM period cycles can be buffered. 

With XCMPEN set, the load of the active registers are controlled by the XLOADCTL and XLOAD registers. The shadow to active loading of the registers (other than XMINMAX, XCMPC, XCMPD) are always done three cycles prior to TBCTR==ZERO event. XMINMAX, XCMPC and XCMPD shadow loading is done at TBCTR==PRD. 

There are two load modes configured by XLOADCTL[LOADMODE]: 

- **LOADONCE** Mode (XLOADCTL[LOADMODE] = 0) 

   - In LOADONCE mode, XLOADCTL[SHDWBUFPTR_ LOADONCE] is used to set the pointer location of the shadow buffer. 

   - XLOADCTL[SHDWBUFPTR_ LOADONCE] is set by the user and is **NOT** automatically decremented. Upon the occurrence of the first load strobe (write of ‘1’ to XLOAD[STARTLD] bit), active register set is loaded from the XLOADCTL[SHDWBUFPTR_ LOADONCE] SHDW selected by the user. Further load strobes are ignored, and ePWM waveform generation continues with the active register set until next XLOAD[STARTLD] is initiated. 

   - When the software sets the XLOAD[STARTLD] bit again, the active register set is loaded from the XLOADCTL[SHDWBUFPTR_ LOADONCE] SHDW selected by the user. If the user wants to initiate a SHDW load from a different shadow register set, then the software can update the XLOADCTL[SHDWBUFPTR_ LOADONCE] register accordingly before setting the XLOADCTL[STARTLD]. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

729 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- **LOADMULTIPLE** Mode (XLOADCTL[LOADMODE] = 1) 

   - XLOADCTL[SHDWBUFPTR_ LOADMULTIPLE] always points to the current shadow register set that is loaded into the active registers set. 

   - Setting the XLOAD[STARTLD] bit initiates a load strobe. The SHDW buffer pointer resets to XLOADCTL[SHDWLEVEL] and the corresponding buffer contents are loaded to the active register set. When the next valid load strobe arrives, XLOADCTL[SHDWBUFPTR_ LOADMULTIPLE] is decremented by 1 and the corresponding buffer contents are loaded to the active register set. This continues until the XLOADCTL[SHDWBUFPTR_ LOADMULTIPLE] value reaches 1. At this time SHDW1 values get copied to the active register set. Further load strobes are ignored and the ePWM waveform generation continues with the active register set until next XLOAD[STARTLD] is initiated. 

   - Once the XLOADCTL[SHDWBUFPTR_ LOADMULTIPLE] value reaches 1, no further decrements to the this pointer are done until the next STARTLD initiation. This means the XLOADCTL[SHDWBUFPTR_ LOADMULTIPLE] remains at value of '1', indicating that the SHDW1 register set is in use till the next load initiation by user. 

   - For a SHDWLEVEL of 3 buffers SHDW3 is loaded first followed by SHDW2 and SHDW1. Then until the next STARTLD write by the software, the SHDW1 values are in use. 

**==> picture [499 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
SHDW1<br>XCMP2:XCMP2HR  XCMP1:XCMP1HR   ModuleBaseTime(TB) TBCNT(16) Comparator CMPA QualifierAction EPWMxA<br>Module<br>CMPA:HR[31-0] (AQ) EPWMxB<br>XCMP8:XCMP8HR   [SHDWBUFPTR_LOADONCE]XLOADCTL CMPA:HR Active Reg<br>CMPA:HR Shadow Reg<br>SHDW2 ACTIVE<br>No<br>XCMP1:XCMP1HR   Shadow Set 00 XCMP1:XCMP1HR   Move to<br>01 the next<br>XCMP2:XCMP2HR   10 XCMP2:XCMP2HR   XCMP<br>11<br>XCMP8:XCMP8HR   XCMP8:XCMP8HR<br>SHDW3<br>XCMP1:XCMP1HR<br>XCMP2:XCMP2HR<br>XCMP8:XCMP8HR<br>**----- End of picture text -----**<br>


**Figure 7-254. XCMP- Load Once Functionality** 

**==> picture [499 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
SHDW1<br>Time<br>XCMP2:XCMP2HR  XCMP1:XCMP1HR   ModuleBase(TB) TBCNT(16) Comparator CMPA QualifierModuleAction EPWMxA<br>[SHDWBUFPTR_LOADMULTIPLE]XLOADCTL CMPA:HR[31-0] (AQ) EPWMxB<br>XCMP8:XCMP8HR   [SHDWLEVEL]XLOADCTL Counter2-bit  CMPA:HR Shadow RegCMPA:HR Active Reg<br>SHDW2 ACTIVE<br>XCMP2:XCMP2HR  XCMP1:XCMP1HR  XCMP2:XCMP2HR  XCMP1:XCMP1HR  SHDW1 Shadow SetNo  000110 SHDW set/s based on SHDWLEVEL selection XCMP2:XCMP2HR  XCMP1:XCMP1HR   Move to the next XCMP<br>11<br>XCMP8:XCMP8HR   XCMP8:XCMP8HR<br>XCMP8:XCMP8HR<br>SHDW3<br>XCMP1:XCMP1HR   SHDW2<br>XCMP1:XCMP1HR   SHDW1<br>XCMP2:XCMP2HR   XCMP1:XCMP1HR<br>XCMP2:XCMP2HR<br>XCMP2:XCMP2HR<br>XCMP8:XCMP8HR<br>XCMP8:XCMP8HR<br>XCMP8:XCMP8HR<br>**----- End of picture text -----**<br>


**Figure 7-255. XCMP- Load Multiple Functionality** 

730 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

With this new loading scheme, the global load functionality also changes when using XCMP mode. In this new configuration, once a write to STARLD occurs, the next time the time base counter equals zero or a force load software write occurs, the shadow buffer pointers get reset, based on the load mode (load once or load multiple). 

**==> picture [450 x 258] intentionally omitted <==**

**----- Start of picture text -----**<br>
Write “1” to CLR<br>XLOAD[STARTLD]<br>XLOADCTL[LOADMOD E] 0 1<br>One Shot<br>Latch<br>Set Q<br>load<br>strobe<br>CNT_ZRO XLOADCTL[SHDWBUFPTR_LOADDMULTIPLE]<br>1<br>XLOAD[FRCLD]<br>0<br>0<br>clear CNT<br>2-bit<br>Counter<br>inc CNT<br>XLOADCTL[SHDWLEVEL]<br>XLOADSTRB<br>Load strobe<br>Used for bu � er loads<br>**----- End of picture text -----**<br>


**Figure 7-256. Global Load: Signals and Registers** 

Shadow buffers can also be repeated more than once. Shadow buffer repeat counters are: 

- Users can optionally repeat each shadow buffer multiple times. This option sets the repeat count for SHDW2 and SHDW3 buffers before the pointer moves to the SHDW1 buffer. SHDW1 buffer by default repeats until the next load is initiated by the software and hence there is no configurable repeat option for SHDW1 buffer. 

- Repeat counter option of the shadow buffers is applicable in LOADMULTIPLE mode. In the LOADONCE mode, user can manually keep track of the repeat counts and move to the SHDW pointer buffer. 

- Each shadow buffer has a 3-bit counter. Each buffer can be set to repeat up to 8 times before moving the pointer to the next buffer. 

- XLOADCTL[RPTBUF2PRD] and XLOADCTL[RPTBUF3PRD] are used to control the repeat period for each SHDW buffer. 

No shadowing can be set by setting the XLOADCTL[SHDWLEVEL] to '0'. In this case, the ACTIVE registers are available for use (XCMP1_ACTIVE, XCMP2_ACTIVE, and so on). 

## _**7.5.6.14.4 XCMP Allocation to CMPA and CMPB**_ 

The first criteria that must be selected is whether both EPWM channel A and channel B outputs are required. If both channel A and channel B are required, XCMP registers must be assigned to both CMPA and CMPB. The XCMPn registers loaded to CMPA are used for configuring the A channel through XAQCTLA actions. The XCMPn registers loaded to CMPB are used for configuring the B channel through XAQCTLB actions. 

XCMP allocation to CMPA and CMPB is done through XCMPCTL1.XCMPSPLIT. If both channel A and channel B are required in the system, then the XCMPCTL1.XCMPSPLIT must be set. This allows CMPA to use XCMP1n (where n has a maximum value of 4) while CMPB uses XCMP5-m (where m has a maximum value of 8). If only channel A is needed, then XCMPCTL1.XCMPSPLIT must be cleared, allowing CMPA to use XCMP1-n (where n has a maximum value of 8), which means up to eight edges can be generated on channel A. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 731 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Note** 

The maximum number of edges that channel B can have is four, when XCMP5-8 are allocated to CMPB and all four XCMP5-8 are used by setting the XCMPB_ALLOC to use all available XCMPs. 

XCMPA_ALLOC and XCMPB_ALLOC determines how many of the available XCMPs for each CMPA and CMPB must be used in the ePWM configuration. 

**==> picture [498 x 498] intentionally omitted <==**

**----- Start of picture text -----**<br>
Time<br>Base(TB) TBCNT(16) Comparator CMPA<br>Module<br>EPWMA<br>CMPA:HR[31-0]<br>XLOADCTL[SHDWBUFPTR_LOADONCE] CMPA:HR Ac � ve Reg<br>XLOADCTL[SHDWBUFPTR_LOADMULTIPLE]<br>CMPA:HR Shadow Reg<br>Ac � on<br>Quali � er<br>Module<br>XCMP1:HR SHDW3 Reg XCMP1:HR SHWD2 Reg XCMP1:HR SHDW1 Reg XCMP1:HR Ac � ve Reg XCMPCTL1[CMPEN]=1 (AQ)<br>XCMP2:HR SHDW3 Reg XCMP2:HR SHDW2 Reg XCMP2:HR SHDW1 Reg XCMP2:HR Ac � ve Reg<br>EPWMB<br>XCMP8:HR SHDW3 Reg XCMP8:HR SHDW2 Reg XCMP8:HR SHDW1 Reg XCMP8:HR Ac � ve Reg<br>Figure 7-257. Allocate All XCMP1-8 to CMPA<br>Time<br>Base(TB) TBCNT(16) Comparator CMPA<br>Module<br>EPWMA<br>CMPA:HR[31-0]<br>XLOADCTL[SHDWBUFPTR_LOADONCE] CMPA:HR Ac � ve Reg<br>XLOADCTL[SHDWBUFPTR_LOADMULTIPLE]<br>CMPA:HR Shadow Reg<br>XCMP1:HR SHDW3 Reg XCMP1:HR SHDW2 Reg XCMP1:HR SHDW1 Reg XCMP1:HR Ac � ve Reg XCMPCTL1[CMPEN]=1<br>XCMP2:HR SHDW3 Reg XCMP2:HR SHDW2 Reg XCMP2:HR SHDW1 Reg XCMP2:HR Ac � ve Reg<br>XCMP3:HR SHDW3 Reg XCMP3:HR SHDW2 Reg XCMP3:HR SHDW1 Reg XCMP3:HR Ac ve Reg<br>XCMP4:HR SHDW3 Reg XCMP4:HR SHDW2 Reg XCMP4:HR SHDW1 Reg XCMP4:HR Ac ve Reg<br>Ac � on<br>Quali � er<br>Module<br>(AQ)<br>TimeBase TBCNT(16) Comparator CMPB<br>(TB) EPWMB<br>Module<br>CMPB:HR[31-0]<br>XLOADCTL[SHDWBUFPTR_LOADONCE] CMPB:HR Ac � ve Reg<br>XLOADCTL[SHDWBUFPTR_LOADMULTIPLE]<br>CMPB:HR Shadow Reg<br>XCMP5:HR SHDW3 Reg XCMP5:HR SHDW2 Reg XCMP5:HR SHDW1 Reg XCMP5:HR Ac � ve Reg XCMPCTL1[CMPEN]=1<br>XCMP6:HR SHDW3 Reg XCMP6:HR SHDW2 Reg XCMP6:HR SHDW1 Reg XCMP6:HR Ac � ve Reg<br>XCMP7:HR SHDW3 Reg XCMP7:HR SHDW2 Reg XCMP7:HR SHDW1 Reg XCMP7:HR Ac � ve Reg<br>XCMP8:HR SHDW3 Reg XCMP8:HR SHDW2 Reg XCMP8:HR SHDW1 Reg XCMP8:HR Ac � ve Reg<br>**----- End of picture text -----**<br>


**Figure 7-258. XCMP1-4 Allocated to CMPA and XCMP5-8 Allocated to CMPB** 

## _**7.5.6.14.5 XCMP Operation**_ 

The XCMP complex waveform generation mode is described in this section. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

732 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

The XCMP mode can be used to generate multiple edges within one ePWM period. The application software must write the location of the ePWM waveform edges to the XCMP registers. Each XCMPn register assigned and used for an ePWM CMPx (CMPA or CMPB) must be spaced out according to the following guidelines to make sure of correct waveform generation. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

733 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

Figure 7-259 shows an example of four XCMP values being loaded into CMPA during one period cycle and the remaining four XCMP values being used for CMPB. When the action for the last XCMP value loaded into CMPA/CMPB in a period is met, the last value for CMPA/CMPB remains until the next time TBCTR=0 due to a new shadow set load. 

**==> picture [499 x 316] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBCNT<br>EPWMA<br>CMPA Ac � ve Register XCMP4 (n-1) XCMP1 (n) XCMP2 (n) XCMP3 (n) XCMP4 (n) XCMP1 (n+1)<br>Ac � on for PWMA<br>XAQCTLA_ACTIVE<br>Changes with XCMPn  [XCMP4(n-1)]   XAQCTLA_ACTIVE[XCMP1(n)]   XAQCTLA_ACTIVE[XCMP2(n)] XAQCTLA_ACTIVE[XCMP3(n)] XAQCTLA_ACTIVE[XCMP4(n)] XAQCTLA_ACTIVE[XCMP1(n+1)]<br>loads in to CMPA<br>EPWMB<br>CMPB Ac � ve Register XCMP8 (n-1) XCMP5 (n) XCMP6 (n) XCMP7 (n) XCMP8 (n) XCMP5 (n+1)<br>Ac � on for PWAB<br>XAQCTLB_ACTIVE<br>Changes with XCMPn  [XCMP8(n-1)]   XAQCTLB_ACTIVE[XCMP5(n)] XAQCTLB_ACTIVE[XCMP6(n)] XAQCTLB_ACTIVE[XCMP7(n)] XAQCTLB_ACTIVE[XCMP8(n)] XAQCTLB_ACTIVE[XCMP5(n+1)]<br>loads in to CMPB<br>**----- End of picture text -----**<br>


**Figure 7-259. CMPA and CMPB values being loaded from XCMP registers** 

Assume XCMP1-3 are assigned and used by CMPA (XCMP4 is not used), and XCMP5-6 are assigned and used by CMPB (XCMP7 and XCMP8 are not used): 

- For XCMP1-8 to be split between CMPA and CMPB, software must write XCMPCTL1[XCMPSPLIT] = 1 

- For CMPA to only use XCMP1-3, software must write XCMPCTL1[CMPA_ALLOC] = 3 

- For CMPB to only use XCMP5-6, software must write XCMPCTL1[CMPB_ALLOC] = 6 

For XCMP1-3 in this scenario, since all are used by CMPA, the values written to XCMP1, XCMP2, and XCMP3 must: 

- Without high-resolution edge placement requirement: XCMP(n+1) > (XCMPn) + 1 

- With high-resolution edge placement requirement: XCMP(n+1) > (XCMPn) + 3 

The requirements above for the minimum difference between XCMP(n+1) and XCMPn must be met in the application software. 

The actions taken for each XCMP1-8 must be configured in XAQCTLA and XAQCTLB. 

If shadowing is required then the XCMP1-8, XAQCTLA and XAQCTLB values must be written to the corresponding shadow buffer. As an example, Table 7-165 shows how the shadow buffers are used in LOADMULTIPLE mode. 

The SHDW buffers 2 and 3 can also be repeated more than once by using the RPTBUF2PRD and RPTBUF3PRD. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

734 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-165. SHDW Buffer Loading Example** 

||**XCMPn, XTBPRD**|**XCMPn, XTBPRD**|**XCMPn, XTBPRD**|**XTBPRD,**<br>**TBPRD**|**XCMPn:**<br>**XCMPnHR**|**CMPA:**<br>**CMPAHR**|**What happens next?**|
|---|---|---|---|---|---|---|---|
||**SHDW3FULL**|**SHDW2FULL**|**SHDW1FULL**|**Active**|**Active**|**Active**||
|CPU Initialization|Set|Set|Set||||Registers initialized<br>by CPU. Load event<br>occurs.|
|ePWM Cycle 1|Clear|Set|Set|XTBPRD_<br>SHDW3|XCMPn_<br>SHDW3|XCMPn_<br>SHDW3|SHDWBUFPTR set to<br>3|
|ePWM Cycle 2|Clear|Clear|Set|XTBPRD_<br>SHDW2|XCMPn_<br>SHDW2|XCMPn_<br>SHDW2|SHDWBUFPTR set to<br>2|
|ePWM Cycle 3|Clear|Clear|Clear|XTBPRD_<br>SHDW1|XCMPn_<br>SHDW1|XCMPn_<br>SHDW1|SHDWBUFPTR set to<br>1|
|ePWM Cycle 4|Clear|Clear|Clear|XTBPRD_<br>SHDW1|XCMPn_<br>SHDW1|XCMPn_<br>SHDW1|SHDWBUFPTR set<br>to 1 No shadow<br>to active loading<br>from buffer. Operation<br>continues with values<br>in XCMPn_ACTIVE<br>registers.|
|ePWM Cycle 5|Clear|Clear|Clear|XTBPRD_<br>SHDW1|XCMPn_<br>SHDW1|XCMPn_<br>SHDW1|SHDWBUFPTR set<br>to 1 Continues<br>operation with<br>same values in<br>XCMPn_ACTIVE until<br>the next buffer load<br>event|
|CPU Load<br>(During ePWM<br>Cycle 5)|Set|Set|Set|XTBPRD_<br>SHDW1|XCMPn_<br>SHDW1|XCMPn_<br>SHDW1|CPU loads new<br>shadow value set.<br>Load event occurs.<br>SHDWBUFPTR set to<br>3|
|ePWM Cycle 6|Clear|Set|Set|XTBPRD_<br>SHDW3|XCMPn_<br>SHDW3|XCMPn_<br>SHDW3|SHDWBUFPTR set to<br>3|
|ePWM Cycle 7|Clear|Clear|Set|XTBPRD_<br>SHDW2|XCMPn_<br>SHDW2|XCMPn_<br>SHDW2|SHDWBUFPTR set to<br>2|
|ePWM Cycle 8|Clear|Clear|Clear|XTBPRD_<br>SHDW1|XCMPn_<br>SHDW1|XCMPn_<br>SHDW1|SHDWBUFPTR set to<br>1|
|ePWM Cycle 9|Clear|Clear|Clear|XTBPRD_<br>SHDW1|XCMPn_<br>SHDW1|XCMPn_<br>SHDW1|Continues operation<br>with the same values<br>in XCMPn_ACTIVE<br>until the next<br>buffer load event.<br>SHDWBUFPTR set to<br>1|
|ePWM Cycle 10|Set|Set|Set|XTBPRD_<br>SHDW1|XCMPn_<br>SHDW1|XCMPn_<br>SHDW1|CPU loads new<br>shadow register set.<br>Load event occurs.<br>SHDWBUFPTR set to<br>3|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 735 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.6.15 High-Resolution Pulse Width Modulator (HRPWM)** 

Figure 7-260 shows a block diagram of the HRPWM. This module extends the time resolution capabilities of the conventionally derived digital pulse width modulator (PWM). HRPWM is typically used when PWM resolution falls below approximately 9-10 bits. The key features of HRPWM are: 

- Extended time resolution capability 

- Used in both duty cycle and phase-shift control methods 

- Finer time granularity control or edge positioning using extensions to the Compare A, Compare B and Phase registers 

- Implemented using the A and B signal path of PWM, that is, on the EPWMxA and EPWMxB output 

- Dead band high-resolution control for falling and rising edge delay in half cycle clocking operation 

- Enables high-resolution output swapping on the EPWMxA and EPWMxB output 

- Enables high-resolution output on EPWMxB signal output using inversion of EPWMxA signal output 

- Enables high-resolution period, duty and phase control on the EPWMxA and EPWMxB output on devices with an ePWM module 

## **Note** 

See the device data sheet to determine if your device has an ePWM module with high-resolution period support. 

**==> picture [470 x 224] intentionally omitted <==**

**----- Start of picture text -----**<br>
TBPHSHR(8)A<br>CMPAHR(8)B<br>CMPBHR(8)B HRPWM HRCNFG/HRCNFG2<br>TBPRDHR(8)A (MEP) Calibration ModuleMicro-edge Positioner<br>Action DBREDHR(7)C HRMSTEP HRPWR<br>Qualifier DBFEDHR(7)C<br>(AQ) High- Resolution PWM (HRPWM)<br>EPWMA EPWMxAO<br>Dead PWM Trip<br>band chopper zone<br>(DB) (PC) (TZ)<br>EPWMB EPWMxBO<br>**----- End of picture text -----**<br>


- A. From ePWM Time-base (TB) submodule 

- B. From ePWM counter-compare (CC) submodule 

- C. From ePWM Deadband (DB) submodule 

**Figure 7-260. HRPWM Block Diagram** 

736 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

The ePWM peripheral is used to perform a function mathematically equivalent to a digital-to-analog converter (DAC). As shown in Figure 7-261, the effective resolution for conventionally generated PWM is a function of PWM frequency (or period) and system clock frequency. 

**==> picture [376 x 98] intentionally omitted <==**

**----- Start of picture text -----**<br>
TPWM PWM resolution (%) = FPWM/FEPWMCLK x 100%<br>PWM resolution (bits) = Log2 (TPWM/TEPWMCLK)<br>PWM<br>t<br>TEPWMCLK<br>**----- End of picture text -----**<br>


**Figure 7-261. Resolution Calculations for Conventionally Generated PWM** 

If the required PWM operating frequency does not offer sufficient resolution in PWM mode, consider using HRPWM. As an example of improved performance offered by HRPWM, Table 7-166 shows resolution in bits for various PWM frequencies. These values assume a MEP step size of 180 ps. See the device data sheet for typical and maximum performance specifications for the MEP. 

**Table 7-166. Resolution for PWM and HRPWM** 

|**PWM Frequency**|**Regular Resolution (PWM)**<br>**100 MHz EPWMCLK**<br>**High Resolution (HRPWM)**|**Regular Resolution (PWM)**<br>**100 MHz EPWMCLK**<br>**High Resolution (HRPWM)**|
|---|---|---|
|<br>**(kHz)**|**Bits**<br>**%**<br>**Bits**<br>**%**||
|20<br>50<br>100<br>150<br>200<br>250<br>500<br>1000<br>1500<br>2000|12.3<br>0.02<br>11<br>0.05<br>10<br>0.1<br>9.4<br>0.15<br>9<br>0.2<br>8.6<br>0.25<br>7.6<br>0.5<br>6.6<br>1<br>6.1<br>1.5<br>5.6<br>2|18.1<br>0.000<br>16.8<br>0.001<br>15.8<br>0.002<br>15.2<br>0.003<br>14.8<br>0.004<br>14.4<br>0.005<br>13.4<br>0.009<br>12.4<br>0.018<br>11.9<br>0.027<br>11.4<br>0.036|



Although each application can differ, typical low-frequency PWM operation (below 250 kHz) does not require HRPWM. HRPWM capability is most useful for high-frequency PWM requirements of power conversion topologies such as: 

- Single-phase buck, boost, and flyback 

- Multiphase buck, boost, and flyback 

- Phase-shifted full bridge 

- Direct modulation of D-Class power amplifiers 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 737 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.15.1 Operational Description of HRPWM**_ 

The HRPWM is based on micro-edge positioner (MEP) technology. MEP logic is capable of positioning an edge very finely by sub-dividing one coarse system clock of a conventional PWM generator. The time step accuracy is on the order of 150 ps. See the device data sheet for the typical MEP step size on a particular device. The HRPWM also has a self-check software diagnostics mode to check if the MEP logic is running as designed under all operating conditions. Details on software diagnostics and functions are in Scale Factor Optimizing Software (SFO). 

Figure 7-262 shows the relationship between one coarse system clock and edge position in terms of MEP steps, which are controlled using an 8-bit field in the Compare A extension register (CMPAHR). The same operating logic applies to CMPBHR as well. 

To generate an HRPWM waveform, configure the ePWM registers to generate a conventional PWM of a given frequency and polarity. The HRPWM works together with the ePWM registers to extend edge resolution. Although many programming combinations are possible, only a few are needed and practical. 

**==> picture [452 x 100] intentionally omitted <==**

**==> picture [437 x 117] intentionally omitted <==**

**----- Start of picture text -----**<br>
(1 EPWMCLK cycle)<br>+ 0.5 (rounding)<br>(upper 8 bits)<br>**----- End of picture text -----**<br>


(0x0080 in Q8 format) 

**Figure 7-262. Operating Logic Using MEP** 

## _**7.5.6.15.1.1 Controlling the HRPWM Capabilities**_ 

The MEP of the HRPWM is controlled by six extension registers. These HRPWM registers are concatenated with the 16-bit TBPHS, TBPRD, CMPA, CMPBM, DBREDM, and DBFEDM registers used to control PWM operation. 

- TBPHSHR - Time Base Phase High Resolution Register 

- CMPAHR - Counter Compare A High Resolution Register; CMPAHR is for use with the AQ output of Channel A, and is not related to CMPA 

- TBPRDHR - Time Base Period High Resolution Register. (available on some devices) 

- CMPBHR - Counter Compare B High Resolution Register; CMPBHR is for use with the AQ output of Channel B, and is not related to CMPB 

- DBREDHR - Dead-band Generator Rising Edge Delay High Resolution Register 

- DBFEDHR - Dead-band Generator Falling Edge Delay High Resolution Register 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

738 

Copyright © 2025 Texas Instruments Incorporated 

**==> picture [504 x 471] intentionally omitted <==**

**----- Start of picture text -----**<br>
www.ti.com Processors and Accelerators<br>31 16 15 8 7 0<br>TBPHSHR (8) Reserved (8)<br>TBPHS (16) TBPHSHR (8) Reserved(8)<br>TBPHS (16)<br>Single 32-bit write<br>31 16 15 8 7 0<br>CMPAHRA (8) Reserved (8) CMPAA (16) CMPAHRA (8) Reserved(8)<br>CMPAA (16)<br>Single 32-bit write<br>31 16 15 8 7 0<br>TBPRDHRA (8) Reserved (8)<br>TBPRD(16) TBPRDHR (8) Reserved(8)<br>TBPRDA (16)<br>Single 32-bit write<br>31 16 15 8 7 0<br>CMPBHRA (8) Reserved (8)<br>CMPB (16) CMPBHR (8) Reserved(8)<br>CMPBA (16)<br>Single 32-bit write<br>31 16 15 9 8 0<br>DBFEDHRA (7) Reserved (9)<br>DBFED(16) DBFEDHR  [(7)] Reserved(8)<br>DBFEDA (16)<br>Single 32-bit write<br>31 16 15 9 8 0<br>DBREDHRA (7) Reserved (9)<br>DBRED(16) DBREDHR(7) Reserved(8)<br>DBREDA (16)<br>Single 32-bit write<br>**----- End of picture text -----**<br>


A. Dependent upon your device, these registers can be mirrored and can be written to at two different memory locations. 

**Figure 7-263. HRPWM Extension Registers and Memory Configuration** 

## **Note** 

HRPWM capabilities on Deadband Rising Edge Delay and Falling Edge Delay is applicable only during dead band half cycle clocking Operation. The number of MEP steps is half in size [bits 15:9 ] than duty and phase high-resolution registers for the same reason. 

HRPWM capabilities are controlled using the Channel A and B PWM signal path. HRPWM support on the Dead band signal path is available by properly configuring the HRCNFG2 register. Figure 7-264 shows how the HRPWM interfaces with the 8-bit extension registers. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 739 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [440 x 524] intentionally omitted <==**

A. These events are generated by the ePWM Digital Compare (DC) submodule based on the levels of the TRIPIN inputs. 

**Figure 7-264. HRPWM System Interface** 

740 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.15.1.2 HRPWM Source Clock**_ 

Each HRPWM module is clocked from the respective EPWMxCLK. HRCAL has a separate clock. For example, HRPWM1 is sourced from EPWM1CLK while HRPWM2 is clocked from the EPWM2CLK. Figure 7-265 shows the HRCAL and HRPWM modules are sourced from their respective HRCAL and ePWM clock source. 

**==> picture [221 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
HRCAL Clock CLK<br>HRCAL<br>HRMSTEP<br>EPWM1CLK ePWM1 CLK HRPWM1<br>EPWM2CLK ePWM2 CLK HRPWM2<br>EPWM3CLK ePWM3 CLK HRPWM3<br>EPWMxCLK ePWMx CLK HRPWMx<br>**----- End of picture text -----**<br>


**Figure 7-265. HRPWM and HRCAL Source Clock** 

## _**7.5.6.15.1.3 Configuring the HRPWM**_ 

Once the ePWM has been configured to provide conventional PWM of a given frequency and polarity, the HRPWM is configured by programming the HRCNFG register in that particular ePWM module's register space. This register provides the following configuration options: 

- **Edge Mode** The MEP can be programmed to provide precise position control on the rising edge (RE), falling edge (FE) or both edges (BE) at the same time. FE and RE are used for power topologies requiring duty cycle control (CMPA or CMPB high-resolution control), while BE is used for topologies requiring phase shifting, for example, phase shifted full bridge (TBPHS or TBPRD high-resolution control). 

- **Control** The MEP is programmed to be controlled either from the CMPAHR/CMPBHR register in case **Mode** of duty cycle control or the TBPHSHR register (phase control). RE or FE control mode can be used with the CMPAHR or CMPBHR register. BE control mode can be used with the TBPHSHR register. When the MEP is controlled from the TBPRDHR register (period control), the duty cycle and phase can also be controlled using their respective high-resolution registers. 

**Shadow** This mode provides the same shadowing (double buffering) option as in regular PWM mode. **Mode** This option is valid only when operating from the CMPAHR, CMPBHR, and TBPRDHR registers and can be chosen to be the same as the regular load option for the CMPA/CMPB register. If TBPHSHR is used, then this option has no effect. 

**High-** The B signal path of an ePWM channel can generate a high-resolution output by outputting an **Resolution B** inverted version of the high-resolution ePWMxA signal on the ePWMxB pin. HRPWM module **Signal** can also enable high-resolution features on the B signal path independently of the A signal path **Control** as well. **Auto-** This mode is used in conjunction with the scale factor optimization (SFO) software only. For a **conversion** type 4 HRPWM module, below is a description of the Auto-conversion Mode taking CMPAHR **Mode** as an example. If auto-conversion is enabled, CMPAHR = fraction(PWMduty*PWMperiod)<<8. The scale factor optimization software calculates the MEP scale factor in the background code and automatically updates the HRMSTEP register with the calculated number of MEP steps 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 741 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

per coarse step. The MEP Calibration Module then uses the values in the HRMSTEP and CMPAHR registers to automatically calculate the appropriate number of MEP steps represented by the fractional duty cycle and moves the high-resolution ePWM signal edge accordingly. If auto-conversion is disabled, the CMPAHR register behaves like a type 0 HRPWM module and CMPAHR = (fraction(PWMduty * PWMperiod) * MEP Scale Factor + 0.5)<<8). All calculations need to be performed by your code in this mode, and the HRMSTEP register is ignored. Auto-conversion for high-resolution period has the same behavior as auto-conversion for highresolution duty cycle. Auto-conversion must always be enabled for high-resolution period mode. 

## **Note** 

If the HRPWM module is configured in UP-DOWN counter mode, the shadow mode for the HRPWM registers must be set to load on both ZERO AND PERIOD. New values from the user are loaded to the shadow registers only at CTR=ZERO, but the shadow mode of for the registers must be set to both ZERO AND PERIOD. The CTR=PRD event is used for specific internal logic inside the HRPWM module. 

Auto-conversion Mode performs the calculation for CMPBHR , DBREDHR, and DBFEDHR. The scale factor optimization software calculates the MEP scale factor in the background code and automatically updates the HRMSTEP register with the calculated number of MEP steps per coarse step. The MEP Calibration Module then uses the values in the HRMSTEP and CMPBHR or DBREDHR/DBFEDHR register to automatically calculate the appropriate number of MEP steps represented by the fractional components and moves the high-resolution ePWM signal edge accordingly. If auto-conversion is disabled, CMPBHR behaves the same as CMPAHR. CMPBHR = (fraction(PWMduty * PWMperiod) * MEP Scale Factor + 0.5)<<8). 

## **Linking CMPBHR to CMPAHR** 

Starting with EPWM Type 5, the user has the option to link the CMPBHR value to the CMPAHR value. This allows for EPWM channel A and EPWM channel B outputs to both be controlled by CMPAHR. This feature is enabled through CMPCTL.LINKDUTYHR register. This feature is commonly used when the HRPWM is configured for complimentary output mode. 

742 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.15.1.4 Configuring High-Resolution in Deadband Rising-Edge and Falling-Edge Delay**_ 

Once the ePWM has been configured to provide conventional PWM of a given frequency, polarity, and dead band enabled in half-cycle clocking mode, the high-resolution operation on dead band RED and FED lines are enabled by programming the HRCNFG2 register in that particular ePWM module register space. This register provides the following configuration options: 

- **Edge Mode** The MEP can be programmed to provide precise position control on the dead band rising edge (RED), dead band falling edge (FED), or both edges (rising edge of DBRED signal and falling edge of DBFED signal) at the same time. 

**Control** Selects the time event that loads the shadow value in the active register for DBRED and **Mode** DBFED in high-resolution mode. Select the pulse to match the selection in the ePWM DBCTL[LOADREDMODE] and DBCTL[LOADFEDMODE] bits. 

## _**7.5.6.15.1.5 Principle of Operation**_ 

The MEP logic is capable of placing an edge in one of 255 (8 bits) discrete time steps (see the device data sheet for typical MEP step size). The MEP works with the TBM and CCM registers to be certain that time steps are applied and that edge placement accuracy is maintained over a wide range of PWM frequencies, system clock frequencies, and other operating conditions. Table 7-167 shows the typical range of operating frequencies supported by the HRPWM. 

**Table 7-167. Relationship Between MEP Steps, PWM Frequency, and Resolution** 

|**System**|**MEP Steps Per**|**PWM Minimum**|**PWM Maximum**|**Resolution at**|
|---|---|---|---|---|
|**(MHz)**|**EPWMCLK**(1) (2) (3)|**(Hz)**(4)|**(MHz)**|**Maximum (Bits)**(5)|
|60.0|93|916|3.00|10.9|
|70.0|79|1068|3.50|10.6|
|80.0|69|1221|4.00|10.4|
|90.0|62|1373|4.50|10.3|
|100.0|56|1526|5.00|10.1|



(1) TBCLK = EPWMCLK. 

(2) Table data based on a MEP time resolution of 180 ps (this is an example value. See the device data sheet for MEP limits) (3) MEP steps applied = TEPWMCLK/180 ps in this example. 

(4) PWM minimum frequency is based on a maximum period value,(TBPRD = 65535). PWM mode is asymmetrical up-count. (5) Resolution in bits is given for the maximum PWM frequency stated. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

743 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.15.1.5.1 Edge Positioning**_ 

## **Note** 

The following example is presented using the [CMPA:CMPAHR] register combination. The theory of operation and equations are the same, if intending to use the [CMPBM:CMPBHRM] for duty cycle control. 

In a typical power control loop, a digital controller issues a duty command, usually expressed in a per unit or percentage terms. Assume that for a particular operating point, the demanded duty cycle is 0.405 or 40.5% on time and the required converter PWM frequency is 1.25MHz. In conventional PWM generation with a system clock of 100MHz, the duty cycle choices are in the vicinity of 40.5%. As shown in Figure 7-266, a compare value of 32 counts (duty = 40%) is the closest to 40.5% that can be attained. This is equivalent to an edge position of 320 ns instead of the desired 324 ns. This data is shown in Table 7-168. 

By utilizing the MEP, an edge position much closer to the desired point of 324 ns can be achieved. Table 7-168 shows that in addition to the CMPA value, 22 steps of the MEP (CMPAHR register) positions the edge at 323.96 ns, resulting in almost zero error. In this example, it is assumed that the MEP has a step resolution of 180ps. 

**==> picture [368 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
Tpwm�=�800�ns<br>324�ns<br>Demanded<br>duty�(40.5%)<br>10�ns�steps<br>30 31 32 33 34<br>0 79<br>EPWM1A<br>37.5% 40.0% 42.5%<br>38.8% 41.3%<br>**----- End of picture text -----**<br>


**Figure 7-266. Required PWM Waveform for a Requested Duty = 40.5%** 

**Table 7-168. CMPA versus Duty (left), and [CMPA:CMPAHR] versus Duty (right)** 

|**CMPA**<br>**(count)**(1) (2) (3)<br>**Duty**<br>**(%)**<br>**High Time**<br>**(ns)**<br>**CMPA**<br>**(count)**<br>**CMPAHR**<br>**(count)**<br>**Duty**<br>**(%)**<br>**High Time**<br>**(ns)**|**CMPA**<br>**(count)**(1) (2) (3)<br>**Duty**<br>**(%)**<br>**High Time**<br>**(ns)**<br>**CMPA**<br>**(count)**<br>**CMPAHR**<br>**(count)**<br>**Duty**<br>**(%)**<br>**High Time**<br>**(ns)**|
|---|---|
|28<br>**_35.0_**<br>280<br>29<br>**_36.3_**<br>290<br>30<br>**_37.5_**<br>300<br>31<br>**_38.8_**<br>310<br>32<br>**_40.0_**<br>320<br>33<br>**_41.3_**<br>330<br>34<br>**_42.5_**<br>340<br>Required<br>32.40<br>**_40.5_**<br>324|32<br>18<br>**_40.405_**<br>323.24<br>32<br>19<br>**_40.428_**<br>323.42<br>32<br>20<br>**_40.450_**<br>323.60<br>32<br>21<br>**_40.473_**<br>323.78<br>32<br>22<br>**_40.495_**<br>323.96<br>32<br>23<br>**_40.518_**<br>324.14<br>32<br>24<br>**_40.540_**<br>324.32<br>32<br>25<br>**_40.563_**<br>324.50<br>32<br>26<br>**_40.585_**<br>324.68<br>32<br>27<br>**_40.608_**<br>324.86|



(1) Assumed MEP step size for the above example = 180 ps. See the device-specific data sheet for typical and maximum MEP values. (2) TBCLK = 100MHz, 10 ns 

(3) For a PWM Period register value of 80 counts, PWM Period = 80 ˟ 10 ns = 800 ns, PWM frequency = 1/800 ns = 1.25MHz 

744 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.15.1.5.2 Scaling Considerations**_ 

The mechanics of how to position an edge precisely in time has been demonstrated using the resources of the standard CMPA and MEP (CMPAHR) registers. In a practical application, however, it is necessary to seamlessly provide the CPU a mapping function from a per-unit (fractional) duty cycle to a final integer (non-fractional) representation that is written to the [CMPA:CMPAHR] register combination. 

To do this, first examine the scaling or mapping steps involved. It is common in control software to express duty cycle in a per-unit or percentage basis. This has the advantage of performing all needed math calculations without concern for the final absolute duty cycle, expressed in clock counts or high time in nanoseconds (ns). Furthermore, it makes the code more transportable across multiple converter types running different PWM frequencies. 

To implement the mapping scheme, a two-step scaling procedure is required. 

## **Assumptions for this example:** 

|**Assumptions for this example:**||
|---|---|
|TBCLK|= 10 ns (100 MHz)|
|PWM frequency|= 1.25 MHz (1/800 ns)|
|Required PWM duty cycle,**PWMDuty**|= 0.405 (40.5%)|
|PWM period in terms of coarse steps,|= 80|
|**PWMPeriod**(800 ns/10 ns)||
|Number of MEP steps per coarse step at|= 55|
|180 ps (10 n/180 ps),**MEP_ScaleFactor**||
|Value to keep CMPAHR within the range of||
|1-255 and fractional rounding constant (default||
|value)|= 0.5 (0080h in Q8 format)|



## **Step 1: Percentage Integer Duty value conversion for CMPA register** 

|CMPA register value|=|int(**PWMDuty*PWMPeriod**); int means integer part|
|---|---|---|
||=|int(0.405 * 80)|
||=|int(32.4)|
|CMPA register value|=|32 (20h)|



## **Step 2: Fractional value conversion for CMPAHR register** 

CMPAHR = (frac( **PWMDuty** * **PWMPeriod** )* **MEP_ScaleFactor** + 0.5) <<8); frac means fractional part = (frac(32.4) * 55 + 0.5) <<8; Shifting is to move the value to the high byte of CMPAHR. = (0.4 * 55 + 0.5) <<8 = (22 + 0.5) <<8 = 22.5 * 256; Shifting left by 8 is the same as multiplying by 256. = 5760 (1680h) CMPAHR = 1680h CMPAHR value = 1600h (lower 8 bits are ignored by hardware). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 745 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Note** 

If the AUTOCONV bit (HRCNFG.6) is set and the MEP_ScaleFactor is in the HRMSTEP register, then CMPAHR / CMPBHR register value = frac (PWMDuty*PWMperiod<<8). The rest of the conversion calculations are performed automatically in hardware, and the correct MEP-scaled signal edge appears on the ePWM channel output. If AUTOCONV is not set, the above calculations must be performed by software. 

The MEP scale factor (MEP_ScaleFactor) varies with the system clock and DSP operating conditions. TI provides an MEP scale factor optimizing (SFO) software C function, which uses the built in diagnostics in each HRPWM and returns the best scale factor for a given operating point. 

The scale factor varies slowly over a limited range so the optimizing C function can be run very slowly in a background loop. 

The CMPA, CMPB, CMPAHR and CMPBHR registers are configured in memory so that the 32-bit data capability of the CPU can write this as a single concatenated value, that is, [CMPA:CMPAHR], [CMPB:CMPBHR], and so on. 

The mapping scheme has been implemented in C, and the actual implementation takes advantage of the 32-bit CPU architecture and examples are provided in the Section 7.5.6.18. 

## _**7.5.6.15.1.5.3 Duty Cycle Range Limitation**_ 

In high-resolution mode, the MEP is not active for 100% of the PWM period and becomes operational: 

- Three EPWMCLK cycles after the period starts when high-resolution period (TBPRDHR) control is not enabled. 

- When high-resolution period (TBPRDHR) control is enabled using the HRPCTL register: 

   - In up-count mode: three EPWMCLK cycles after the period starts until three EPWMCLK cycles before the period ends. 

   - In up-down count mode: when counting up, three cycles after CTR = 0 until three cycles before CTR = PRD, and when counting down, three cycles after CTR = PRD until three cycles before CTR = 0. 

- When using DBREDHR or DBFEDHR, DBRED or DBFED (the register corresponding to the edge with high-resolution displacement) must be greater than or equal to 7. 

Duty cycle range limitations are illustrated in Figure 7-267 to Figure 7-270. This limitation imposes a duty cycle limit on the MEP. For example, precision edge control is not available all the way down to 0% duty cycle. When high-resolution period control is disabled, regular PWM duty control is fully operational down to 0% duty cycle despite the unavailability of HRPWM features in the first three cycles. In most applications, this cannot be an issue as the controller regulation point is usually not designed to be close to 0% duty cycle. To better understand the useable duty cycle range, see Table 7-169. When high-resolution period control is enabled (HRPCTL[HRPE]=1), the duty cycle must not fall within the restricted range; otherwise, there can be undefined behavior on the ePWMxA output. 

746 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [404 x 160] intentionally omitted <==**

**----- Start of picture text -----**<br>
TPWM EPWMCLK =<br>TBCLK<br>0 3 TBPRD<br>EPWM1A<br>**----- End of picture text -----**<br>


**Figure 7-267. Low % Duty Cycle Range Limitation Example (HRPCTL[HRPE] = 0)** 

**Table 7-169. Duty Cycle Range Limitation for Three EPWMCLK/TBCLK Cycles** 

|**PWM Frequency**(1)|**3 Cycles**|**3 Cycles**|
|---|---|---|
|**(kHz)**|**Minimum Duty**|**Maximum Duty**(2)|
|200|0.6%|99.4%|
|400|1.2%|98.8%|
|600|1.8%|98.2%|
|800|2.4%|97.6%|
|1000|3%|97%|
|1200|3.6%|96.4%|
|1400|4.2%|95.8%|
|1600|4.8%|95.2%|
|1800|5.4%|94.6%|
|2000|6%|94%|



(1) EPWMCLK = TBCLK = 100 MHz 

(2) This limitation applies only if high-resolution period (TBPRDHR) control is enabled. 

If the application demands HRPWM operation below the minimum duty cycle limitation, then the HRPWM can be configured to operate in count-down mode with the rising edge position (REP) controlled by the MEP when high-resolution period is disabled (HRPCTL[HRPE] = 0). This is illustrated in Figure 7-268. In this configuration, the minimum duty cycle limitation is no longer an issue. However, there is a maximum duty limitation with same percent numbers as given in Table 7-169. 

## **CAUTION** 

If the application has enabled high-resolution period control (HRPCTL[HRPE]=1), the duty cycle must not fall within the restricted range; otherwise, there can be undefined behavior on the ePWM output. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 747 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [393 x 177] intentionally omitted <==**

**----- Start of picture text -----**<br>
T<br>pwm<br>EPWMCLK<br>0 3<br>TBPRD<br>EPWM1A<br>**----- End of picture text -----**<br>


**Figure 7-268. High % Duty Cycle Range Limitation Example (HRPCTL[HRPE] = 0)** 

**==> picture [501 x 394] intentionally omitted <==**

**----- Start of picture text -----**<br>
Tpwm EPWMCLK=<br>TBCLK<br>TBPRD - 3 TBPRD<br>0 3<br>EPWM1A<br>Figure 7-269. Up-Count Duty Cycle Range Limitation Example (HRPCTL[HRPE]=1)<br>T pwm<br>TBPRD<br>0 3 TBPRD-3 TBPRD-3 3 0<br>**----- End of picture text -----**<br>


**Figure 7-270. Up-Down Count Duty Cycle Range Limitation Example (HRPCTL[HRPE]=1)** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

748 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.15.1.5.4 High-Resolution Period**_ 

High-resolution period control using the MEP logic is supported on devices with a Type 1 ePWM module or greater. 

## **Note** 

When high-resolution period control is enabled, on ePWMxA only, and not ePWMxB output and conversely, the non high-resolution output has ±1 TBCLK cycle jitter in up-count mode and ±2 TBCLK cycle jitter in up-down count mode. 

The scaling procedure described for duty cycle in Section 7.5.6.15.1.5.2 applies for high-resolution period as well: 

## **Assumptions for this example:** 

TBCLK = 10 ns (100MHz) Required PWM frequency = 175kHz (period of 571.428) Number of MEP steps per coarse step at 180 ps = 55 (10 ns / 180ps) (MEP_ScaleFactor) Value to keep TBPRDHR within range of 1-255 and = 0.5 (0080h in Q8 format) fractional rounding constant (default value) 

## **Problem:** 

In up-count mode: 

- If TBPRD = 571, then PWM frequency = 174.82 kHz (period = (571+1)* TTBCLK). 

- If TBPRD = 570, then PWM frequency = 175.13 kHz (period = (570+1)* TTBCLK). 

In up-down count mode: 

- If TBPRD = 286, then PWM frequency = 174.82kHz (period = (286*2)* TTBCLK). 

- If TBPRD = 285, then PWM frequency = 175.44kHz (period = (285*2)* TTBCLK). 

## **Solution:** 

With 55 MEP steps per coarse step at 180ps each: 

## **Step 1: Percentage Integer Period value conversion for TBPRD register** 

Integer period value = 571 * TTBCLK = int (571.428) * TTBCLK = int (PWMperiod) * TTBCLK In up-count mode: TBPRD = 570 (TBPRD = period value - 1) = 023Ah In up-down count mode: = 285 (TBPRD = period value / 2) TBPRD = 011Dh 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 749 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Step 2: Fractional value conversion for TBPRDHR register** 

In up-count mode: TBPRDHR register value = (frac(PWMperiod) * MEP_ScaleFactor + 0.5) If auto-conversion enabled and HRMSTEP = MEP_ScaleFactor value (55): =frac (PWMperiod) << 8 (Shifting is to move the value 

MEP_ScaleFactor value (55): =frac (PWMperiod) << 8 (Shifting is to move the value to the high byte of TBPRDHR) TBPRDHR register value =frac (571.428) << 8 =0.428 × 256 =6D00h The auto-conversion then automatically performs the =((TBPRDHR(15:0) >> 8) × HRMSTEP + 80h) << 8 

The auto-conversion then automatically performs the calculation, such that TBPRDHR MEP delay is scaled by hardware to: 

= (006Dh × 55 + 80h) >> 8 =(17EBh) >> 8 =0017h MEP Steps 

Period MEP delay 

In up-down count mode: TBPRDHR register value If auto-conversion enabled and HRMSTEP = MEP_ScaleFactor value (55): 

TBPRDHR register value 

The auto-conversion then automatically performs the calculation, such that TBPRDHR MEP delay is scaled by hardware to: 

Period MEP delay 

= (frac(PWMperiod) * MEP_ScaleFactor + 0.5) =frac (PWMperiod / 2) << 8 (Shifting is to move the value to the high byte of TBPRDHR) =frac (285.714) << 8 =0.714 × 256 =B600h =((TBPRDHR(15:0) >> 8) × HRMSTEP + 80h) << 8 = (00B6h × 55 + 80h) >> 8 =(279Ah) >> 8 =0027h MEP Steps 

750 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.15.1.5.4.1 High-Resolution Period Configuration**_ 

To use high-resolution period, the ePWMx module must be initialized in the exact order presented. 

The following steps use CMPA with shadow registers and the corresponding HRCNFG bits for high-resolution operation on EPWMxA. For high-resolution operation on EPWMxB, make the appropriate substitutions with the B channel fields. 

1. Enable ePWMx clock 

2. Enable HRPWM clock 

3. Disable EPWM_SYNC 

4. Configure ePWMx registers - AQ, TBPRD, CC, and so on. 

   - ePWMx can only be configured for up-count or up-down count modes. High-resolution period is not compatible with down-count mode. 

   - TBPRD and CC registers must be configured for shadow loads. 

   - CMPCTL[LOADAMODE] 

      - In up-count mode: CMPCTL[LOADAMODE] = 1 (load on CTR = PRD) 

      - In up-down count mode: CMPCTL[LOADAMODE] = 2 (load on CTR=0 or CTR=PRD) 

5. Configure the HRCNFG register such that: 

   - HRCNFG[HRLOAD] = 2 (load on either CTR = 0 or CTR = PRD) 

   - HRCNFG[AUTOCONV] = 1 (Enable auto-conversion) 

   - HRCNFG[EDGMODE] = 3 (MEP control on both edges) 

6. For TBPHS:TBPHSHR synchronization with high-resolution period, set both HRPCTL[TBPSHRLOADE] = 1 and TBCTL[PHSEN] = 1. In up-down count mode these bits must be set to 1 regardless of the contents of TBPHSHR. 

7. Enable high-resolution period control (HRPCTL[HRPE] = 1) 

8. Enable EPWM_CLKSYNC 

9. TBCTL[SWFSYNC] = 1 

10. HRMSTEP must contain an accurate MEP scale factor (# of MEP steps per EPWMCLK coarse step) because auto-conversion is enabled. The MEP scale factor can be acquired using the SFO() function. 

11. To control high-resolution period, write to the TBPRDHR(M) registers. 

## **Note** 

When high-resolution period mode is enabled, an EPWMxSYNC pulse introduces ±1-2 cycle jitter to the PWM (±1 cycle in up-count mode and ±2 cycle in up-down count mode). For this reason, EPWMxSYNCO source cannot be set to CTR = 0 or CTR = CMPB. Otherwise, the jitter occurs on every PWM cycle with the synchronization pulse. 

When EPWMxSYNCI is EPWMxSYNCO source, a software synchronization pulse can be issued only once during high-resolution period initialization. If a software sync pulse is applied while the PWM is running, the jitter appears on the PWM output at the time of the sync pulse. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

751 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.15.1.6 Deadband High-Resolution Operation**_ 

## **Note** 

In up-count mode, the dead-band module is not available when any high-resolution mode is enabled. 

## **Assumptions for this example:** 

System clock = 10 ns (100 MHz) Deadband enabled in half-cycle mode, TBCLK = EPWMCLK Required PWM frequency 1.33 MHz (1 / 750 ns) Required PWM duty cycle 0.5 (50%) Required Deadband Rising Edge Delay 5% over duty Required Deadband Rising Edge Delay in ns (0.05 * 375 ns) = 18.75 ns 

## **Note** 

Similar to the duty cycle restrictions when using HRPWM, the DBRED and DBFED values must be greater than 3 to use high-resolution deadband. 

## **Deadband delay values as a function of DBFED and DBRED:** 

When half-cycle clocking is enabled, the formula to calculate the falling-edge-delay and rising-edge-delay becomes: 

FED = DBFED * TBCLK / 2 

RED = DBRED * TBCLK / 2 

## **DBRED and DBFED calculated values:** 

Required Dead band Rising Edge Delay in ns = 18.75 ns 

DBRED = RED / (TBCLK / 2) 

DBRED = 18.75 ns / 5 ns 

DBRED Required = 3.75 ns 

With 55 MEP steps per coarse step at 180 ps each: 

752 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **Step 1: Integer Deadband value conversion for DBREDM register** 

Integer DBRED value = int (RED / (TBCLK / 2)) = int (3.75) DBRED = 3 

## **Step 2: Fractional value conversion for Deadband high-resolution register DBREDHR** 

DBREDHR register value = (frac(DBRED Required) * MEP_ScaleFactor + 0.5) << 8 (Shifting is to move the value to the high byte of DBREDHR) = (frac (3.75) * 55 + 0.5) << 8 = (0.75 * 55 + 0.5) << 8 = (41.75) * 256 Shifting left by 8 is the same as multiplying by 256. DBREDHR value = 29C0h MEP Steps Hardware ignores lower 9 bits in the above calculated DBREDHR value 

## **Note** 

If the AUTOCONV bit (HRCNFG.6) is set and the MEP_ScaleFactor is in the HRMSTEP register, then DBREDHR:DBRED = frac((required DB value) < <8). The rest of the conversion calculations are performed automatically in hardware, and the correct MEP-scaled signal edge appears on the ePWM channel output. If AUTOCONV is not set, the above calculations must be performed by software. 

## _**7.5.6.15.1.7 Scale Factor Optimizing Software (SFO)**_ 

The micro edge positioner (MEP) logic is capable of placing an edge in one of 255 discrete time steps. As previously mentioned, the size of these steps is on the order of 150 ps (see the device data sheet for typical MEP step size on your device). The MEP step size varies based on worst-case process parameters, operating temperature, and voltage. MEP step size increases with decreasing voltage and increasing temperature and decreases with increasing voltage and decreasing temperature. Applications that use the HRPWM feature can use the TI-supplied MEP scale factor optimization (SFO) software function. The SFO function helps to dynamically determine the number of MEP steps per EPWMCLK period while the HRPWM is in operation. 

To utilize the MEP capabilities effectively, the correct value for the MEP scaling factor needs to be known by the software. To accomplish this, the HRPWM module has built in self-check and diagnostic capabilities that can be used to determine the optimum MEP scale factor value for any operating condition. TI provides a C-callable library containing one SFO function that utilizes this hardware and determines the optimum MEP scale factor. As such, MEP control and diagnostics registers are reserved for TI use. 

A detailed description of the SFO library and examples are listed in Section 7.5.6.18. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 753 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.15.1.8 HRPWM Examples Using Optimized Assembly Code**_ 

The best way to understand how to use the HRPWM capabilities is through two real examples: 

1. Simple buck converter using asymmetrical PWM (count-up) with active high polarity. 

2. DAC function using simple R+C reconstruction filter. 

The following examples all have initialization and configuration code written in C. To make these easier to understand, the #defines shown below are used. 

## _**Example 7-9. #Defines for HRPWM Header Files**_ 

```
// HRPWM (High Resolution PWM) //
================================
// HRCNFG
#define HR_Disable 0x0
#define HR_REP 0x1          // Rising Edge position
#define HR_FEP 0x2          // Falling Edge position
#define HR_BEP 0x3          // Both Edge position #define HR_CMP 0x0 // CMPAHR controlled
#define HR_PHS 0x1          // TBPHSHR controlled #define HR_CTR_ZERO 0x0 // CTR = Zero event
#define HR_CTR_PRD 0x1      // CTR = Period event
#define HR_CTR_ZERO_PRD 0x2 // CTR = ZERO or Period event
#define HR_NORM_B  0x0      // Normal ePWMxB output
#define HR_INVERT_B 0x1     // ePWMxB is inverted ePWMxA output
```

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

754 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.15.1.8.1 Implementing a Simple Buck Converter**_ 

In this example, the PWM requirements are: 

- PWM frequency = 1 MHz (that is, TBPRD = 100) 

- PWM mode = asymmetrical, up-count 

- Resolution = 12.7 bits (with a MEP step size of 150 ps) 

Figure 7-271 and Figure 7-272 show the required PWM waveform. As explained previously, configuration for the ePWM1 module is almost identical to the normal case except that the appropriate MEP options need to be enabled/selected. 

**==> picture [334 x 293] intentionally omitted <==**

**----- Start of picture text -----**<br>
Vin1 Vout1<br>Buck<br>EPWM1A<br>Figure 7-271. Simple Buck Controlled Converter Using a Single PWM<br>T<br>pwrr<br>Z CA Z CA Z<br>EPWM1A<br>**----- End of picture text -----**<br>


**Figure 7-272. PWM Waveform Generated for Simple Buck Controlled Converter** 

The example code shown consists of two main parts: 

- Initialization code (executed once) 

- Run time code (typically executed within an ISR) 

Example 7-10 shows the Initialization code. The first part is configured for conventional PWM. The second part sets up the HRPWM resources. 

This example assumes MEP step size of 150 ps and does not use the SFO library. 

Example 7-11 shows an assembly example of run-time code for the HRPWM buck converter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 755 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**Example 7-10. HRPWM Buck Converter Initialization Code**_ 

```
void HrBuckDrvCnf(void)
 {
// Config for conventional PWM first
EPwm1Regs.TBCTL.bit.PRDLD = TB_IMMEDIATE;         // set Immediate load
EPwm1Regs.TBPRD = 100;                            // Period set for 1000 kHz PWM
hrbuck_period = 200;                              // Used for Q15 to Q0 scaling
EPwm1Regs.TBCTL.bit.CTRMODE = TB_COUNT_UP;
EPwm1Regs.TBCTL.bit.PHSEN = TB_DISABLE;           // EPWM1 is the Sync Source
EPwm1Regs.TBCTL.bit.HSPCLKDIV = TB_DIV1;
EPwm1Regs.TBCTL.bit.CLKDIV = TB_DIV1;
// Note: ChB is initialized here only for comparison purposes, it is not required
EPwm1Regs.CMPCTL.bit.LOADAMODE = CC_CTR_ZERO;
EPwm1Regs.CMPCTL.bit.SHDWAMODE = CC_SHADOW;
EPwm1Regs.CMPCTL.bit.LOADBMODE = CC_CTR_ZERO;     // optional
EPwm1Regs.CMPCTL.bit.SHDWBMODE = CC_SHADOW;       // optional
EPwm1Regs.AQCTLA.bit.ZRO = AQ_SET;
EPwm1Regs.AQCTLA.bit.CAU = AQ_CLEAR;
EPwm1Regs.AQCTLB.bit.ZRO = AQ_SET;                // optional
EPwm1Regs.AQCTLB.bit.CBU = AQ_CLEAR;              // optional
// Now configure the HRPWM resources
EALLOW;                                           // Note these registers are protected
                                                  // and act only on ChA
EPwm1Regs.HRCNFG.all = 0x0;                       // clear all bits first
EPwm1Regs.HRCNFG.bit.EDGMODE = HR_FEP;            // Control Falling Edge Position
EPwm1Regs.HRCNFG.bit.CTLMODE = HR_CMP;            // CMPAHR controls the MEP
EPwm1Regs.HRCNFG.bit.HRLOAD = HR_CTR_ZERO;        // Shadow load on CTR=Zero
EDIS;
MEP_ScaleFactor = 66*256;                         // Start with typical Scale Factor
                                                  // value for 100 MHz
                                                  // Note: Use SFO functions to update
                                                     MEP_ScaleFactor dynamically
}
```

## _**Example 7-11. HRPWM Buck Converter Run-Time Code**_ 

```
EPWM1_BASE .set 0x6800
CMPAHR1 .set EPWM1_BASE+0x8
;===============================================
HRBUCK_DRV; (can execute within an ISR or loop)
;===============================================
     MOVW DP, #_HRBUCK_In
     MOVL XAR2,@_HRBUCK_In       ; Pointer to Input Q15 Duty (XAR2)
     MOVL XAR3,#CMPAHR1          ; Pointer to HRPWM CMPA reg (XAR3)
```

```
; Output for EPWM1A (HRPWM)
     MOV T,*XAR2 ; T <= Duty
     MPYU ACC,T,@_hrbuck_period  ; Q15 to Q0 scaling based on Period
     MOV T,@_MEP_ScaleFactor     ; MEP scale factor (from optimizer s/w)
     MPYU P,T,@AL                ; P <= T * AL, Optimizer scaling
     MOVH @AL,P                  ; AL <= P, move result back to ACC
     ADD ACC, #0x080             ; MEP range and rounding adjustment
     MOVL *XAR3,ACC              ; CMPA:CMPAHR(31:8) <= ACC
```

```
; Output for EPWM1B (Regular Res) Optional - for comparison purpose only
     MOV *+XAR3[2],AH            ; Store ACCH to regular CMPB
```

756 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.15.1.8.2 Implementing a DAC Function Using an R+C Reconstruction Filter**_ 

In this example, the PWM requirements are: 

- PWM frequency = 400 kHz (that is, TBPRD = 250) 

- PWM mode = Asymmetrical, Up-count 

- Resolution = 14 bits (MEP step size = 150 ps) 

Figure 7-273 and Figure 7-274 show the DAC function and the required PWM waveform. As explained previously, configuration for the ePWM1 module is almost identical to the normal case except that the appropriate MEP options need to be enabled/selected. 

**==> picture [214 x 67] intentionally omitted <==**

**----- Start of picture text -----**<br>
EPWM1A VOUT1<br>LPF<br>**----- End of picture text -----**<br>


**Figure 7-273. Simple Reconstruction Filter for a PWM-based DAC** 

**==> picture [364 x 141] intentionally omitted <==**

**----- Start of picture text -----**<br>
T PWM  = 2.5 µs<br>Z CA Z CA Z<br>EPWM1A<br>**----- End of picture text -----**<br>


**Figure 7-274. PWM Waveform Generated for the PWM DAC Function** 

The example code shown consists of two main parts: 

- Initialization code (executed once) 

- Run time code (typically executed within an ISR) 

This example assumes a typical MEP_SP and does not use the SFO library. 

Example 7-12 shows the Initialization code. The first part is configured for conventional PWM. The second part sets up the HRPWM resources. 

Example 7-13 shows an assembly example of run-time code that can execute in a high-speed ISR loop. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 757 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**Example 7-12. PWM DAC Function Initialization Code**_ 

```
void HrPwmDacDrvCnf(void)
{
// Config for conventional PWM first
EPwm1Regs.TBCTL.bit.PRDLD = TB_IMMEDIATE;      // Set Immediate load
EPwm1Regs.TBPRD = 250;                         // Period set for 400 kHz PWM
hrDAC_period = 250;                            // Used for Q15 to Q0 scaling
EPwm1Regs.TBCTL.bit.CTRMODE = TB_COUNT_UP;
EPwm1Regs.TBCTL.bit.PHSEN = TB_DISABLE;        // EPWM1 is the Sync Source
EPwm1Regs.TBCTL.bit.HSPCLKDIV = TB_DIV1;
EPwm1Regs.TBCTL.bit.CLKDIV = TB_DIV1;
// Note: ChB is initialized here only for comparison purposes, it is not required
EPwm1Regs.CMPCTL.bit.LOADAMODE = CC_CTR_ZERO;
EPwm1Regs.CMPCTL.bit.SHDWAMODE = CC_SHADOW;
EPwm1Regs.CMPCTL.bit.LOADBMODE = CC_CTR_ZERO;  // optional
EPwm1Regs.CMPCTL.bit.SHDWBMODE = CC_SHADOW;    // optional
EPwm1Regs.AQCTLA.bit.ZRO = AQ_SET;
EPwm1Regs.AQCTLA.bit.CAU = AQ_CLEAR;
EPwm1Regs.AQCTLB.bit.ZRO = AQ_SET;             // optional
EPwm1Regs.AQCTLB.bit.CBU = AQ_CLEAR;           // optional
// Now configure the HRPWM resources
EALLOW;                                        // Note these registers are protected
                                               // and act only on ChA.
EPwm1Regs.HRCNFG.all = 0x0;                    // Clear all bits first
EPwm1Regs.HRCNFG.bit.EDGMODE = HR_FEP;         // Control falling edge position
EPwm1Regs.HRCNFG.bit.CTLMODE = HR_CMP;         // CMPAHR controls the MEP.
EPwm1Regs.HRCNFG.bit.HRLOAD = HR_CTR_ZERO;     // Shadow load on CTR=Zero.
EDIS;
MEP_ScaleFactor = 66*256;                      // Start with typical Scale Factor
                                               // value for 100 MHz.
                                               // Use SFO functions to update MEP_ScaleFactor
                                               // dynamically.
}
```

_**Example 7-13. PWM DAC Function Run-Time Code**_ 

```
EPWM1_BASE .set 0x6800
CMPAHR1 .set EPWM1_BASE+0x8
;=================================================
HRPWM_DAC_DRV; (can execute within an ISR or loop)
;=================================================
      MOVW DP, #_HRDAC_In
      MOVL XAR2,@_HRDAC_In             ; Pointer to input Q15 duty (XAR2)
      MOVL XAR3,#CMPAHR1               ; Pointer to HRPWM CMPA reg (XAR3)
; Output for EPWM1A (HRPWM
      MOV T,*XAR2                      ; T <= duty
      MPY ACC,T,@_hrDAC_period         ; Q15 to Q0 scaling based on period
      ADD ACC,@_HrDAC_period<<15       ; Offset for bipolar operation
      MOV T,@_MEP_ScaleFactor          ; MEP scale factor (from optimizer s/w)
      MPYU P,T,@AL                     ; P <= T * AL, optimizer scaling
      MOVH @AL,P                       ; AL <= P, move result back to ACC
      ADD ACC, #0x080                  ; MEP range and rounding adjustment
      MOVL *XAR3,ACC                   ; CMPA:CMPAHR(31:8) <= ACC
```

```
; Output for EPWM1B (Regular Res) Optional - for comparison purpose only
      MOV *+XAR3[2],AH                 ; Store ACCH to regular CMPB
```

758 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.6.16 ePWM Crossbar (XBAR)** 

Figure 7-275 shows the architecture of the ePWM Crossbar (XBAR). This module enables selection of various trigger sources into any of the dedicated EPWM trips inputs. 

## **Note** 

Refer to the Crossbar (XBAR) chapter for more information on the XBAR modules, including XBAR flags. 

**==> picture [500 x 302] intentionally omitted <==**

**----- Start of picture text -----**<br>
ePWM X-BAR<br>TRIPIN1<br>TRIPIN2<br>CMPSS CTRIPH/L Signals TRIPIN3<br>ePWM TRIPIN4<br>ADC EVT Signals<br>X-BAR A TRIPIN5<br>SDFM Trip Signals TRIPIN6<br>eQEP Error Signals TRIPIN7<br>ePWMx<br>TRIPIN8<br>ePWM TRIPOUT Signals<br>FSI-RX RX TRIG[3:0] Signals TRIPIN9<br>ePWM  TRIPIN10<br>DE TRIP, ACTIVE Signals ePWM TRIPIN11<br>X-BAR B TRIPIN12<br>eCAP TRIPOUT Signals<br>TRIPIN14<br>Input Input X-BAR Signals TRIPIN15<br>X-BAR<br>CPU Error Signals<br>MCAN FEVTX Signals<br>IINPUTXBARCLB CLB Input X-BAR Signals<br>CLB CLB Output Signals<br>ECAT ECAT Sync Signals<br>**----- End of picture text -----**<br>


**Figure 7-275. ePWM XBAR** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 759 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.6.17 Applications to Power Topologies** 

An ePWM module has all the local resources necessary to operate completely as a standalone module or to operate in synchronization with other identical ePWM modules. 

## _**7.5.6.17.1 Overview of Multiple Modules**_ 

Previously in this chapter, all discussions have described the operation of a single module. To facilitate the understanding of multiple modules working together in a system, the ePWM module described in reference is represented by the more simplified block diagram shown in Figure 7-276. This simplified ePWM block shows only the key resources needed to explain how a multiswitch power topology is controlled with multiple ePWM modules working together. 

**==> picture [272 x 184] intentionally omitted <==**

**Figure 7-276. Simplified ePWM Module** 

760 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.17.2 Key Configuration Capabilities**_ 

The key configuration choices available to each module are as follows: 

- Options for SyncIn 

   - Load own counter with phase register on an incoming sync strobe—enable (EN) switch closed 

   - Do nothing or ignore incoming sync strobe—enable switch open 

   - Sync Source mode, provides a sync at PWM boundaries—SyncOut connected to CTR = PRD 

   - Sync Source mode, provides a sync at any programmable point in time—SyncOut connected to CTR = CMPB 

   - Module is in standalone mode and provides no sync to other modules—SyncOut connected to X (disabled) 

- Options for SyncOut 

   - Sync Source mode, provides a sync at PWM boundaries—SyncOut connected to CTR = PRD 

   - Sync Source mode, provides a sync at any programmable point in time—SyncOut connected to CTR = CMPB 

   - Module is in standalone mode and provides no sync to other modules—SyncOut connected to X (disabled) 

For each choice of SyncOut, a module can also choose to load the counter with a new phase value on a SyncIn strobe input or choose to ignore the value (that is, by the enable switch). Although various combinations are possible, the two most common—Sync Source module and Sync Receiver module modes—are shown in Figure 7-277. 

**==> picture [500 x 181] intentionally omitted <==**

**Figure 7-277. EPWM1 Configured as a Typical Sync Source, EPWM2 Configured as a Sync Receiver** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 761 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.17.3 Controlling Multiple Buck Converters With Independent Frequencies**_ 

One of the simplest power converter topologies is the buck. A single ePWM module configured as a sync source can control two buck stages with the same PWM frequency. If independent frequency control is required for each buck converter, then one ePWM module must be allocated for each converter stage. Figure 7-278 shows four buck stages, each running at independent frequencies. In this case, all four ePWM modules are configured as Sync Sources and no synchronization is used. Figure 7-279 shows the waveforms generated by the setup shown in Figure 7-278; note that only three waveforms are shown, although there are four stages. 

**==> picture [500 x 490] intentionally omitted <==**

- A. φ = X indicates value in phase register is a "don't care" 

**Figure 7-278. Control of Four Buck Stages. Here FPWM1≠ FPWM2≠ FPWM3≠ FPWM4** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

762 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [390 x 506] intentionally omitted <==**

**----- Start of picture text -----**<br>
P P P<br>I I I<br>700 950<br>1200<br>P CA CB P CA P<br>A<br>EPWM1A<br>Pulse center<br>700 1150<br>1400<br>P CA CB P CA<br>A<br>EPWM2A<br>650<br>500<br>800<br>CA P CA P CA P<br>CB<br>A<br>EPWM3A<br>P<br>Indicates this event triggers an interrupt CB Indicates this event triggers an ADC start<br>I<br>A of conversion<br>**----- End of picture text -----**<br>


**Figure 7-279. Buck Waveforms for Control of Four Buck Stages (Note: Only three bucks shown here)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 763 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.17.4 Controlling Multiple Buck Converters With Same Frequencies**_ 

If synchronization is a requirement, ePWM module 2 is configured as a sync receiver and operates at integer multiple (N) frequencies of module 1. The sync signal from sync source to sync receiver makes sure these modules remain locked. Figure 7-280 shows such a configuration; Figure 7-281 shows the waveforms generated by the configuration. 

**==> picture [500 x 351] intentionally omitted <==**

- A. φ = X indicates value in phase register is a "don't care" 

**Figure 7-280. Control of Four Buck Stages. (Note: FPWM2 = N x FPWM1)** 

764 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [445 x 408] intentionally omitted <==**

**----- Start of picture text -----**<br>
Z 600 Z Z<br>I 400 400 I I<br>200 200<br>CA P CA CA P CA<br>A(A) A(A)<br>EPWM1A<br>CB CB CB CB<br>EPWM1B<br>500 500<br>300 300<br>CA CA CA CA<br>EPWM2A<br>CB CB CB CB<br>EPWM2B<br>**----- End of picture text -----**<br>


A. Starts ADC conversion. 

**Figure 7-281. Buck Waveforms for Control of Four Buck Stages (Note: FPWM2 = FPWM1)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

765 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.17.5 Controlling Multiple Half H-Bridge (HHB) Converters**_ 

Topologies that require control of multiple switching elements can also be addressed with these same ePWM modules. It is possible to control a Half-H bridge stage with a single ePWM module. This control can be extended to multiple stages. Figure 7-282 shows control of two synchronized Half-H bridge stages where stage 2 can operate at integer multiple (N) frequencies of stage 1. Figure 7-283 shows the waveforms generated by the configuration shown in Figure 7-282. 

ePWM module 2 (sync receiver) is configured for Sync flow-through; if required, this configuration allows for a third Half-H bridge to be controlled by ePWM module 3 and also, most importantly, to remain in synchronization with sync source ePWM module 1. 

**==> picture [500 x 330] intentionally omitted <==**

**Figure 7-282. Control of Two Half-H Bridge Stages (FPWM2 = N x FPWM1)** 

766 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [434 x 455] intentionally omitted <==**

**----- Start of picture text -----**<br>
Z Z Z<br>I I I<br>600<br>400<br>400<br>200 200<br>Z CB CA Z CB CA<br>A A<br>EPWM1A<br>RED delay CA CB Z RED delay CA CB Z<br>A A<br>EPWM1B<br>Pulse Center<br>500<br>500<br>250 250<br>Z CB CA Z CB CA<br>A A<br>EPWM2A<br>RED Delay CA CB Z RED Delay CA CB Z<br>A A<br>EPWM2B<br>Pulse Cente r<br>**----- End of picture text -----**<br>


**Figure 7-283. Half-H Bridge Waveforms for Control of Two Half-H Bridge Stages (Note: Here** 

**FPWM2 = FPWM1)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 767 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.17.6 Controlling Dual 3-Phase Inverters for Motors (ACI and PMSM)**_ 

The idea of multiple modules controlling a single power stage can be extended to the 3-phase inverter case. In such a case, six switching elements are controlled using three PWM modules, one for each leg of the inverter. Each leg must switch at the same frequency and all legs must be synchronized. A sync receivers configuration easily addresses this requirement. Figure 7-284 shows how six PWM modules control two independent 3-phase inverters; each running a motor. 

As in the cases shown in the previous sections, we have a choice of running each inverter at a different frequency (module 1 and module 4 are sync source as in Figure 7-284), or both inverters can be synchronized by using one sync source (module 1) and five sync receivers. In this case, the frequency of modules 4, 5, and 6 (all equal) can be integer multiples of the frequency for modules 1, 2, and 3 (also all equal). 

**==> picture [500 x 422] intentionally omitted <==**

**Figure 7-284. Control of Dual 3-Phase Inverter Stages as Is Commonly Used in Motor Control** 

768 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [436 x 492] intentionally omitted <==**

**----- Start of picture text -----**<br>
Z Z<br>800<br>I I<br>500 500<br>CA P CA CA P CA<br>A A<br>EPWM1A RED RED<br>EPWM1B FED FED<br>600 600<br>Φ2=0<br>CA CA CA CA<br>EPWM2A<br>RED<br>EPWM2B<br>FED<br>700 700<br>Φ3=0<br>CA CA CA CA<br>EPWM3A RED<br>EPWM3B<br>FED<br>**----- End of picture text -----**<br>


**Figure 7-285. 3-Phase Inverter Waveforms for Control of Dual 3-Phase Inverter Stages (Only One Inverter Shown)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 769 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.17.7 Practical Applications Using Phase Control Between PWM Modules**_ 

So far, none of the examples have made use of the phase register (TBPHS). It has either been set to zero or a don't care. However, by programming appropriate values into TBPHS, multiple PWM modules can address another class of power topologies that rely on phase relationship between legs (or stages) for correct operation. As described in the time-base submodule section, a PWM module can be configured to allow a SyncIn pulse to cause the TBPHS register to be loaded into the TBCTR register. To illustrate this concept, Figure 7-286 shows a sync source and sync receiver module with a phase relationship of 120° (that is, the sync receiver leads the sync source). 

**==> picture [240 x 324] intentionally omitted <==**

**Figure 7-286. Configuring Two PWM Modules for Phase Control** 

Figure 7-287 shows the associated timing waveforms for this configuration. Here, TBPRD = 600 for both sync source and sync receiver. For the sync receiver, TBPHS = 200 (that is, 200/600 x 360° = 120°). Whenever the sync source generates a SyncIn pulse (CTR = PRD), the value of TBPHS = 200 is loaded into the sync receiver TBCTR register so the sync receiver time-base is always leading the sync source time-base by 120°. 

770 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [413 x 253] intentionally omitted <==**

**----- Start of picture text -----**<br>
FFFFh TBCTR[0-15]<br>Sync Source Module<br>600 600<br>TBPRD<br>0000<br>CTR = PRD<br>time<br>(SycnOut)<br>FFFFh TBCTR[0-15]<br>�2 Phase = 120�<br>Sync Receiver Module<br>600 600<br>TBPRD<br>200 200<br>TBPHS<br>0000<br>SyncIn<br>time<br>**----- End of picture text -----**<br>


**Figure 7-287. Timing Waveforms Associated with Phase Control Between Two Modules** 

## _**7.5.6.17.8 Controlling a 3-Phase Interleaved DC/DC Converter**_ 

A popular power topology that makes use of phase-offset between modules is shown in Figure 7-288. This system uses three PWM modules, with module 1 configured as the sync receiver. To work, the phase relationship between adjacent modules must be F = 120°. This is achieved by setting the sync receiver TBPHS registers 2 and 3 with values of 1/3 and 2/3 of the period value, respectively. For example, if the period register is loaded with a value of 600 counts, then TBPHS (sync receiver 2) = 200 and TBPHS (sync receiver 3) = 400. Both sync receiver modules are synchronized to the sync source module 1. 

This concept can be extended to four or more phases, by setting the TBPHS values appropriately. The following formula gives the TBPHS values for N phases: 

TBPHS(N,M) = (TBPRD/N) ˟ (M - 1) 

## Where: 

N = number of phases 

M = PWM module number 

For example, for the 3-phase case (N = 3), TBPRD = 600, 

TBPHS(3,2) = (600/3) ˟ (2 - 1) = 200 (that is, Phase value for Sync Receiver module 2) 

TBPHS(3,3) = 400 (that is, Phase value for Sync Receiver module 3) 

Figure 7-289 shows the waveforms for the configuration in Figure 7-288. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 771 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 427] intentionally omitted <==**

**Figure 7-288. Control of 3-Phase Interleaved DC/DC Converter** 

772 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

**==> picture [504 x 417] intentionally omitted <==**

**----- Start of picture text -----**<br>
www.ti.com Processors and Accelerators<br>Z Z Z Z<br>450<br>I I I I<br>285 285<br>CA P CA CA P CA CA P CA<br>A A A<br>EPWM1A RED RED RED<br>EPWM1B FED FED FED<br>150 �2=120�<br>TBPHS<br>(=300)<br>EPWM2A<br>EPWM2B<br>150 �2=120�<br>TBPHS<br>(=300)<br>EPWM3A<br>EPWM3B<br>**----- End of picture text -----**<br>


**Figure 7-289. 3-Phase Interleaved DC/DC Converter Waveforms for Control of 3-Phase Interleaved DC/DC Converter** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 773 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.17.9 Controlling Zero Voltage Switched Full Bridge (ZVSFB) Converter**_ 

The example given in Figure 7-290 assumes a static or constant phase relationship between legs (modules). In such a case, control is achieved by modulating the duty cycle. It is also possible to dynamically change the phase value on a cycle-by-cycle basis. This feature lends to controlling a class of power topologies known as _phase-shifted full bridge_ , or _zero voltage switched full bridge._ Here the controlled parameter is not duty cycle (this is kept constant at approximately 50 percent); instead it is the phase relationship between legs. Such a system can be implemented by allocating the resources of two PWM modules to control a single power stage, which in turn requires control of four switching elements. Figure 7-291 shows a sync source and sync receiver module combination synchronized together to control a full H-bridge. In this case, both sync source and sync receiver modules are required to switch at the same PWM frequency. The phase is controlled by using the sync receiver phase register (TBPHS). The sync source phase register is not used and therefore can be initialized to zero. 

**==> picture [500 x 291] intentionally omitted <==**

**Figure 7-290. Control of Full-H Bridge Stage (FPWM2 = FPWM1)** 

774 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [453 x 379] intentionally omitted <==**

**----- Start of picture text -----**<br>
Z Z Z<br>I I I<br>1200<br>600<br>200<br>Z CB CA Z CB CA Z<br>A A<br>EPWM1A RED<br>ZVS transition<br>Power phase<br>EPWM1B FED<br>ZVS transition<br>300 Φ2=variable<br>TBPHS<br>=(1200−Φ2) CB CB<br>A A<br>Z Z Z<br>CA<br>CA<br>EPWM2A RED<br>EPWM2B FED<br>Power phase<br>**----- End of picture text -----**<br>


**Figure 7-291. ZVS Full-H Bridge Waveforms** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 775 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.6.17.10 Controlling a Peak Current Mode Controlled Buck Module**_ 

Peak current control techniques offer a number of benefits like automatic over current limiting, fast correction for input voltage variations and reducing magnetic saturation. Figure 7-292 shows the use of ePWM1A along with the on-chip analog comparator for buck converter topology. The output current is sensed through a current sense resistor and fed to the positive terminal of the on-chip comparator. The internal programmable 12-bit DAC can be used to provide a reference peak current at the negative terminal of the comparator. Alternatively, an external reference can be connected at this input. The comparator output is an input to the Digital compare sub-module. The ePWM module is configured in such a way so as to trip the ePWM1A output as soon as the sensed current reaches the peak reference value. A cycle-by-cycle trip mechanism is used. Figure 7-293 shows the waveforms generated by the configuration. 

**==> picture [168 x 99] intentionally omitted <==**

**==> picture [234 x 121] intentionally omitted <==**

**Figure 7-292. Peak Current Mode Control of Buck Converter** 

**==> picture [431 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
ePWM1 TBPRD<br>Time base =300<br>DAC OUT/ Increased Reference<br>COMP1- DAC Out<br>Isense<br>DCAEVT2.force<br>ePWM1A<br>TBCTR = 0 TO 300<br>**----- End of picture text -----**<br>


**Figure 7-293. Peak Current Mode Control Waveforms for Control of Buck Converter** 

776 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.6.17.11 Controlling H-Bridge LLC Resonant Converter**_ 

Various topologies of resonant converters are well-known in the field of power electronics for many years. In addition to these, H-bridge LLC resonant converter topology has recently gained popularity in many consumer electronics applications where high efficiency and power density are required. In this example, single channel configuration of ePWM1 is detailed, yet the configuration can easily be extended to multichannel. Here the controlled parameter is not duty cycle (this is kept constant at approximately 50 percent); instead the parameter is frequency. Although the deadband is not controlled and kept constant as 300ns (that is, 30 at 100MHz TBCLK), the user can update the deadband in real time to enhance the efficiency by adjusting enough time delay for soft switching. 

**==> picture [442 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
Ext Sync In(optional) VDC_bus IntegratedMagnetcis VOUT<br>Sync Source<br>Phase Reg En SyncIn LLC Resonant<br>EPWM1A Transformer<br>X<br>EPWM1A<br>CNT=Zero<br>CNT=CMP B EPWM1B<br>1 X<br>SyncOut<br>EPWM1B Cr<br>**----- End of picture text -----**<br>


NOTE: Θ = X indicates value in phase register is a “don’t care” 

**Figure 7-294. Control of Two Resonant Converter Stages** 

**==> picture [445 x 300] intentionally omitted <==**

**----- Start of picture text -----**<br>
P P P<br>I I I<br>period<br>period/2<br>period/4<br>P CB CA P CB CA P<br>A A<br>EPWMxA RED<br>ZVS<br>transition<br>EPWMxB FED<br>ZVS<br>transition<br>P CB<br>Indicates�this�event�triggers�an�interrupt Indicates�this�event�triggers�an ADC<br>I A start�of�conversion<br>**----- End of picture text -----**<br>


**Figure 7-295. H-Bridge LLC Resonant Converter PWM Waveforms** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

777 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.6.18 EPWM Programming Guide** 

## **Driver Information** 

Driver features are available at the EPWM driver page. 

## **Software API Information** 

The EPWM driver provides an API to configure the EPWM module. Full documentation is located on APIs for EPWM. 

## **Example Usage** 

The below links show examples on how to use the EPWM: 

- EPWM HR Duty Cycle 

- EPWM Trip Zone 

- EPWM DMA 

- EPWM Valley Switching 

- EPWM HR UpDown 

- EPWM Protection Solution using PRU 

- EPWM Minimum Deadband 

- EPWM Deadband 

- EPWM Illegal Combo Logic 

- EPWM HR Deadband SFO 

- EPWM HR Phase Shift SFO 

- EPWM HR Duty Cycle SFO 

778 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.7 Enhanced Capture (eCAP)**_ 

This chapter describes the enhanced capture (eCAP) module, which is used in systems where accurate timing of external events is important. 

The enhanced capture (eCAP) module is a Type 3. 

**7.5.7.1 Introduction** ..................................................................................................................................................780 **7.5.7.2 eCAP Integration** ......................................................................................................................................... 781 **7.5.7.3 Description** ...................................................................................................................................................783 **7.5.7.4 Capture Mode Description** ..........................................................................................................................785 **7.5.7.5 APWM Mode Operation** ...............................................................................................................................797 **7.5.7.6 eCAP Synchronization and Events** ............................................................................................................801 **7.5.7.7 Signal Monitoring Unit** ................................................................................................................................ 805 **7.5.7.8 Application of the eCAP Module** ................................................................................................................810 **7.5.7.9 Application of the APWM Mode** ................................................................................................................. 814 **7.5.7.10 eCAP Programming Guide** ....................................................................................................................... 815 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 779 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.7.1 Introduction** 

## _**7.5.7.1.1 Features**_ 

The features of the eCAP module include: 

- Speed measurements of rotating machinery (for example, toothed sprockets sensed by way of Hall sensors) 

- Elapsed time measurements between position sensor pulses 

- Period and duty cycle measurements of pulse train signals 

- Decoding current or voltage amplitude derived from duty cycle encoded current/voltage sensors 

The eCAP module features described in this chapter include: 

- 32 bit time base with 5nS time resolution when sourced with a 200MHz system clock 

- 4-event time-stamp registers (each 32 bits) 

- Edge polarity selection for up to four sequenced time-stamp capture events 

- Interrupt on either of the four events 

- Single-shot capture of up to four event time-stamps 

- Continuous mode capture of time stamps in a four-deep circular buffer 

- Absolute time-stamp capture 

- Difference (Delta) mode time-stamp capture 

- When not used in capture mode, the eCAP module can be configured as a single-channel PWM output 

The capture functionality of the Type 1 eCAP is enhanced from the Type 0 eCAP with the following added features: 

- Event filter reset bit 

   - Writing a 1 to ECCTL2[CTRFILTRESET] clears the event filter, the modulo counter, and any pending interrupts flags. Resetting the bit is useful for initialization and debug. 

- Modulo counter status bits 

   - The modulo counter (ECCTL2 [MODCNTRSTS]) indicates which capture register is loaded next. In the Type 0 eCAP, to know the current state of the modulo counter was not possible 

- DMA trigger source 

- eCAPxDMA was added as a DMA trigger. CEVT[1-4] can be configured as the source for eCAPxDMA. 

- • Input multiplexer 

   - ECCTL0 [INPUTSEL] selects one of 128 input signals which are detailed in Table 7-170 . 

The capture functionality of the Type 2 eCAP is enhanced from the Type 1 eCAP with the following added features: 

- Added ECAPxSYNCINSEL register 

   - 

- ECAPxSYNCINSEL register is added for each eCAP to select an external SYNCIN. Every eCAP can have a separate SYNCIN signal. 

The capture functionality of the Type 3 eCAP is enhanced from the Type 2 eCAP with the following added features: 

- Two signal monitoring units to monitor edge, pulse width, and period 

- Signal monitoring can optionally be tightly coupled with ePWM global load strobes and trip events 

- • Increased the number of multiplexed capture inputs from 128 to 256 

- DMA event generation capability in PWM mode of operation 

- ADC SOC generation capability, to trigger ADC conversion 

780 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.7.2 eCAP Integration** 

There are 16x eCAP modules integrated in the device. _eCAP Integration Diagram_ provides a visual representation of the device integration details. 

**==> picture [453 x 211] intentionally omitted <==**

**----- Start of picture text -----**<br>
MUNIT_ENABLE<br>CAP_INT<br>SYS_CLK<br>DMA_INT<br>RSTN<br>PWM_OUT<br>See eCAP Input SelectionCAP_IN[255:0] ECAP<br>SOC_EVT<br>SYNC_IN[127:0] All EPWM SYNCOUT signals and<br>From Input XBARs<br>SYNC_OUT<br>TRIP_IN[127:0] from PWM_XBARs and EPWM_TRIPOUT<br>TRIP_OUT<br>GLDSTRB[127:0] All EPWM GLDSTRB signals<br>**----- End of picture text -----**<br>


**Figure 7-296. eCAP Integration** 

- MUNIT_Enable: This bit is used to enable/disable the signal monitoring block. 

- RSTN: This bit is used to reset the eCAP module. 

- SYS_CLK: Its 200MHz system clock which is functional clock for ECAP. 

- CAP_IN: Capture inputs can be connected using the INPUTXBAR, PWMXBAR, adc_evt, etc. (Table 7-170). – 256:1 input multiplexer is used to select the capture input. 

- SYNC_IN: eCAP modules can be synchronized with each other by selecting a common SYNCIN source. SYNCIN source for eCAP can be either software sync-in or external sync-in. 

- TRIP_IN: The signal monitoring block can be disabled from monitoring the signal by external trip signals. It is re-enabled by removing the trip-in signal. 

- GLDSTRB: This signal is used to load shadow values to MIN/MAX reg while signal monitoring. 

- CAP_INT: Interrupt signal generated as a part of capture/PWM event. 

- DMA_INT: DMA request signal. 

- PWM_OUT: PWM output in APWM mode. 

- SOC_EVT: Used to generate SOC signal for ADC during any capture/PWM event. 

- SYNC_OUT: This can be used to synchronize the eCAP with other eCAPs or with other modules like PWM. 

- TRIP_OUT: Trip signal is generated upon signal monitoring error. All the signal monitoring error events are OR-ed and provided as trip out. 

## _**7.5.7.2.1 eCAP Input Selection**_ 

The Input X-BAR connects the device pins to the module as input. Any GPIO on the device can be configured as an input. The GPIO input qualification can be set to synchronous or asynchronous mode. Using synchronized inputs can help with noise immunity but affects the eCAP accuracy by ±2 cycles. 

When using the eCAP module, a 256:1 input multiplexer must also be configured. This multiplexer can select a variety of inputs detailed in Table 7-170 by configuring ECCTL0.INPUTSEL. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 781 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-170. eCAP Input Selection** 

|**Selection of eCAP Input**|**Select Index**|**Selection of eCAP Input**|**Select Index**|**Selection of eCAP Input**|**Select Index**|
|---|---|---|---|---|---|
|FSI_RX0.TRIG0|0|EPWM25.SOCA|79|CMPSSA8.CTRIPL|158|
|FSI_RX0.TRIG1|1|EPWM26.SOCA|80|CMPSSA8.CTRIPH|159|
|FSI_RX0.TRIG2|2|EPWM27.SOCA|81|CMPSSA9.CTRIPL|160|
|FSI_RX0.TRIG3|3|EPWM28.SOCA|82|CMPSSA9.CTRIPH|161|
|FSI_RX1.TRIG0|4|EPWM29.SOCA|83|CMPSSB0.CTRIPL|162|
|FSI_RX1.TRIG1|5|EPWM30.SOCA|84|CMPSSB0.CTRIPH|163|
|FSI_RX1.TRIG2|6|EPWM31.SOCA|85|CMPSSB1.CTRIPL|164|
|FSI_RX1.TRIG3|7|EPWM0.SOCB|86|CMPSSB1.CTRIPH|165|
|FSI_RX2.TRIG0|8|EPWM1.SOCB|87|CMPSSB2.CTRIPL|166|
|FSI_RX2.TRIG1|9|EPWM2.SOCB|88|CMPSSB2.CTRIPH|167|
|FSI_RX2.TRIG2|10|EPWM3.SOCB|89|CMPSSB3.CTRIPL|168|
|FSI_RX2.TRIG3|11|EPWM4.SOCB|90|CMPSSB3.CTRIPH|169|
|FSI_RX3.TRIG0|12|EPWM5.SOCB|91|CMPSSB4.CTRIPL|170|
|FSI_RX3.TRIG1|13|EPWM6.SOCB|92|CMPSSB4.CTRIPH|171|
|FSI_RX3.TRIG2|14|EPWM7.SOCB|93|CMPSSB5.CTRIPL|172|
|FSI_RX3.TRIG3|15|EPWM8.SOCB|94|CMPSSB5.CTRIPH|173|
|EQEP0.SYNCQI|16|EPWM9.SOCB|95|CMPSSB6.CTRIPL|174|
|EQEP0.SYNCQS|17|EPWM10.SOCB|96|CMPSSB6.CTRIPH|175|
|EQEP1.SYNCQI|18|EPWM11.SOCB|97|CMPSSB7.CTRIPL|176|
|EQEP1.SYNCQS|19|EPWM12.SOCB|98|CMPSSB7.CTRIPH|177|
|EQEP2.SYNCQI|20|EPWM13.SOCB|99|CMPSSB8.CTRIPL|178|
|EQEP2.SYNCQS|21|EPWM14.SOCB|100|CMPSSB8.CTRIPH|179|
|EPWM0.DELACTIVE|22|EPWM15.SOCB|101|CMPSSB9.CTRIPL|180|
|EPWM1.DELACTIVE|23|EPWM16.SOCB|102|CMPSSB9.CTRIPH|181|
|EPWM2.DELACTIVE|24|EPWM17.SOCB|103|ADC0.ADCTRIPEVT0|182|
|EPWM3.DELACTIVE|25|EPWM18.SOCB|104|ADC0.ADCTRIPEVT1|183|
|EPWM4.DELACTIVE|26|EPWM19.SOCB|105|ADC0.ADCTRIPEVT2|184|
|EPWM5.DELACTIVE|27|EPWM20.SOCB|106|ADC0.ADCTRIPEVT3|185|
|EPWM6.DELACTIVE|28|EPWM21.SOCB|107|ADC1.ADCTRIPEVT0|186|
|EPWM7.DELACTIVE|29|EPWM22.SOCB|108|ADC1.ADCTRIPEVT1|187|
|EPWM8.DELACTIVE|30|EPWM23.SOCB|109|ADC1.ADCTRIPEVT2|188|
|EPWM9.DELACTIVE|31|EPWM24.SOCB|110|ADC1.ADCTRIPEVT3|189|
|EPWM10.DELACTIVE|32|EPWM25.SOCB|111|ADC2.ADCTRIPEVT0|190|
|EPWM11.DELACTIVE|33|EPWM26.SOCB|112|ADC2.ADCTRIPEVT1|191|
|EPWM12.DELACTIVE|34|EPWM27.SOCB|113|ADC2.ADCTRIPEVT2|192|
|EPWM13.DELACTIVE|35|EPWM28.SOCB|114|ADC2.ADCTRIPEVT3|193|
|EPWM14.DELACTIVE|36|EPWM29.SOCB|115|ADC3.ADCTRIPEVT0|194|
|EPWM15.DELACTIVE|37|EPWM30.SOCB|116|ADC3.ADCTRIPEVT1|195|
|EPWM16.DELACTIVE|38|EPWM31.SOCB|117|ADC3.ADCTRIPEVT2|196|
|EPWM17.DELACTIVE|39|SDFM0.COMP1H|118|ADC3.ADCTRIPEVT3|197|
|EPWM18.DELACTIVE|40|SDFM0.COMP1L|119|ADC4.ADCTRIPEVT0|198|
|EPWM19.DELACTIVE|41|SDFM0.COMPZ1|120|ADC4.ADCTRIPEVT1|199|
|EPWM20.DELACTIVE|42|SDFM0.COMP2H|121|ADC4.ADCTRIPEVT2|200|
|EPWM21.DELACTIVE|43|SDFM0.COMP2L|122|ADC4.ADCTRIPEVT3|201|
|EPWM22.DELACTIVE|44|SDFM0.COMPZ2|123|INPUTXBAR.OUT0|202|



782 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-170. eCAP Input Selection (continued)** 

|**Selection of eCAP Input**|**Select Index**|**Selection of eCAP Input**|**Select Index**|**Selection of eCAP Input**|**Select Index**|
|---|---|---|---|---|---|
|EPWM23.DELACTIVE|45|SDFM0.COMP3H|124|INPUTXBAR.OUT1|203|
|EPWM24.DELACTIVE|46|SDFM0.COMP3L|125|INPUTXBAR.OUT2|204|
|EPWM25.DELACTIVE|47|SDFM0.COMPZ3|126|INPUTXBAR.OUT3|205|
|EPWM26.DELACTIVE|48|SDFM0.COMP4H|127|INPUTXBAR.OUT4|206|
|EPWM27.DELACTIVE|49|SDFM0.COMP4L|128|INPUTXBAR.OUT5|207|
|EPWM28.DELACTIVE|50|SDFM0.COMPZ4|129|INPUTXBAR.OUT6|208|
|EPWM29.DELACTIVE|51|SDFM1.COMP1H|130|INPUTXBAR.OUT7|209|
|EPWM30.DELACTIVE|52|SDFM1.COMP1L|131|INPUTXBAR.OUT8|210|
|EPWM31.DELACTIVE|53|SDFM1.COMPZ1|132|INPUTXBAR.OUT9|211|
|EPWM0.SOCA|54|SDFM1.COMP2H|133|INPUTXBAR.OUT10|212|
|EPWM1.SOCA|55|SDFM1.COMP2L|134|INPUTXBAR.OUT11|213|
|EPWM2.SOCA|56|SDFM1.COMPZ2|135|INPUTXBAR.OUT12|214|
|EPWM3.SOCA|57|SDFM1.COMP3H|136|INPUTXBAR.OUT13|215|
|EPWM4.SOCA|58|SDFM1.COMP3L|137|INPUTXBAR.OUT14|216|
|EPWM5.SOCA|59|SDFM1.COMPZ3|138|INPUTXBAR.OUT15|217|
|EPWM6.SOCA|60|SDFM1.COMP4H|139|INPUTXBAR.OUT16|218|
|EPWM7.SOCA|61|SDFM1.COMP4L|140|INPUTXBAR.OUT17|219|
|EPWM8.SOCA|62|SDFM1.COMPZ4|141|INPUTXBAR.OUT18|220|
|EPWM9.SOCA|63|CMPSSA0.CTRIPL|142|INPUTXBAR.OUT19|221|
|EPWM10.SOCA|64|CMPSSA0.CTRIPH|143|INPUTXBAR.OUT20|222|
|EPWM11.SOCA|65|CMPSSA1.CTRIPL|144|INPUTXBAR.OUT21|223|
|EPWM12.SOCA|66|CMPSSA1.CTRIPH|145|INPUTXBAR.OUT22|224|
|EPWM13.SOCA|67|CMPSSA2.CTRIPL|146|INPUTXBAR.OUT23|225|
|EPWM14.SOCA|68|CMPSSA2.CTRIPH|147|INPUTXBAR.OUT24|226|
|EPWM15.SOCA|69|CMPSSA3.CTRIPL|148|INPUTXBAR.OUT25|227|
|EPWM16.SOCA|70|CMPSSA3.CTRIPH|149|INPUTXBAR.OUT26|228|
|EPWM17.SOCA|71|CMPSSA4.CTRIPL|150|INPUTXBAR.OUT27|229|
|EPWM18.SOCA|72|CMPSSA4.CTRIPH|151|INPUTXBAR.OUT28|230|
|EPWM19.SOCA|73|CMPSSA5.CTRIPL|152|INPUTXBAR.OUT29|231|
|EPWM20.SOCA|74|CMPSSA5.CTRIPH|153|INPUTXBAR.OUT30|232|
|EPWM21.SOCA|75|CMPSSA6.CTRIPL|154|INPUTXBAR.OUT31|233|
|EPWM22.SOCA|76|CMPSSA6.CTRIPH|155|Reserved|234|
|EPWM23.SOCA|77|CMPSSA7.CTRIPL|156|Reserved|...|
|EPWM24.SOCA|78|CMPSSA7.CTRIPH|157|Reserved|256|



## **Note** 

ECAPxIN has to be at least 2 ˟ SYSCLK-cycles wide to be properly captured by the eCAP module; otherwise, the input pulse can get missed from sampling by the SYSCLK. 

## **7.5.7.3 Description** 

The eCAP module represents one complete capture channel that can be instantiated multiple times, depending on the target device. In the context of this guide, one eCAP channel has the following independent key resources: 

- Capture inputs can be connected using the Input XBAR 

- 256:1 input multiplexer 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

783 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- Output XBAR is used to configure output in APWM mode 

- 32-bit time base (counter) 

- 4 x 32-bit time-stamp capture registers (CAP1-CAP4) 

- Four-stage sequencer (modulo4 counter) that is synchronized to external events, eCAP pin rising/falling edges. 

- Modulo counter status register (MODCNTRSTS) to indicate sequencer state 

- Independent edge polarity (rising/falling edge) selection for all four events 

- Input capture signal prescaling (from 2-62 or bypass) 

- One-shot compare register (two bits) to freeze captures after 1-4 time-stamp events 

- Control for continuous time-stamp captures using a four-deep circular buffer (CAP1-CAP4) scheme 

- Interrupt capabilities on any of the four capture events 

- Separate DMA trigger 

- Signal monitoring capability for edge, pulse width, and period 

- DMA event generation capability in APWM mode 

- ADC SOC event generation capability, to trigger ADC conversion 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

784 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.7.4 Capture Mode Description** 

Figure 7-297 shows the various components that implement the capture function. 

**==> picture [500 x 402] intentionally omitted <==**

**----- Start of picture text -----**<br>
ECCTL2 [SYNCI_EN, SYNCOSEL, SWSYNC]<br>ECCTL2[CAP/APWM]<br>CTRPHS<br>(phase register-32 bit) APWM Mode<br>ECAPxSYNCIN<br>ECAPxSYNCOUT (counter-32 bit)TSCTR RSTOVF Delta-ModeCTR_OVF PRD [0-31]CTR [0-31] ComparePWMLogic OutputX-Bar<br>CMP [0-31]<br>32<br>CTR [0-31] CTR=PRD<br>CTR=CMP<br>32<br>PRD [0-31]<br>HRCTRL[HRE] ECCTL1 [CAPLDEN, CTRRSTx]<br>32<br>32 (APRD Active)CAP1 LD LD1 PolaritySelect<br>APRD 32<br>HRCTRL[HRE] shadow 32 CMP [0-31]<br>32 HRCTRL[HRE]<br>32 (ACMP Active)CAP2 LD LD2 PolaritySelect Event Glitch [255:16] OtherSources<br>Prescale Filter<br>HRCTRL[HRE] 32 shadowACMP QualifierEvent ECCTL1[PRESCALE] [15:0] 16 X-BarInput<br>32<br>32 (APRD Shadow)CAP3 LD LD3 PolaritySelect<br>4<br>HRCTRL[HRE] LD[1:4]<br>32 CTR_EQ_PRD ECAPxDMA_INT<br>32 (ACMP Shadow)CAP4 LD LD4 PolaritySelect CTR_EQ_[PRD or CMP]CTR_EQ_CMP<br>4 Edge Polarity Select<br>Capture Events 4 ECCTL1[CAPxPOL] ECCTL2[DMAEVTSEL]<br>ECCTL2[CTRFILTRESET] 4<br>CEVT[1:4] CEVT[1:4]<br>InterruptTriggerFlagand MUNITCTR__xOVF_ERROR_EVTy x*y Capture ControlContinuous /Oneshot MODCNTRSTS CTR_EQ_PRDCTR_EQ_CMP ECAPxSOC_EVT<br>ECAPx Control CTR=PRD CTR_EQ_[PRD or CMP]<br>(to Interrupt Controller) CTR=CMP Edgeand ECCTL2 [ REARM, CONT_ONESHT, STOP_WRAP] ECCTL2[CAP/APWM],<br>Registers: ECEINT, ECFLG, ECCLR, ECFRC MonitoringPulse EPWM Global LD EventsEPWM Trip Signals ECCTL0[SOCEVTSEL]<br>SYSCLKHRCLK HR Submodule [(A)] Capture Pulse MUNIT_x_ERROR_EVTy x*y TRIP<br>ECAPx_HRCAL HR Input<br>(to Interrupt Controller)<br>SYNC<br>**----- End of picture text -----**<br>


**Figure 7-297. eCAP Block Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 785 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.7.4.1 Event Prescaler**_ 

An input capture signal (pulse train) can be prescaled by N = 2-62 (in multiples of 2) or can bypass the prescaler. This is useful when very high frequency signals are used as inputs. Figure 7-298 shows a functional diagram and Figure 7-299 shows the operation of the prescale function. 

**==> picture [254 x 122] intentionally omitted <==**

**----- Start of picture text -----**<br>
Event Prescaler<br>0<br>ECCTL2[CTRFILTRESET]<br>PSout<br>Glitch<br>1 /n<br>Filter<br>5<br>By-pass ECCTL1[PRESCALE]<br>Prescaler [5 bits]<br>(counter)<br>ECCTL0[INPUTSEL]<br>ECAPxIN[255:0]<br>**----- End of picture text -----**<br>


- A. When a prescale value of 1 is chosen (ECCTL1[13:9] = 0,0,0,0,0), the input capture signal bypasses the prescale logic completely. 

- B. The first Rise edge after Prescale configuration change is not passed to Capture logic, prescaler value takes into effect on the second rising edge after the configuration. 

**Figure 7-298. Event Prescale Control** 

**==> picture [408 x 230] intentionally omitted <==**

**==> picture [30 x 216] intentionally omitted <==**

**----- Start of picture text -----**<br>
ECAPx<br>PSout<br>div 2<br>PSout<br>div 4<br>PSout<br>div 6<br>PSout<br>div 8<br>PSout<br>div 10<br>**----- End of picture text -----**<br>


**Figure 7-299. Prescale Function Waveforms** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

786 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.7.4.2 Glitch Filter**_ 

A glitch filter is included to reduce internal and external noise glitches on the source signal being measured by the eCAP. 

The glitch filter can be used to filter out glitches of a specified time period in terms of SYSCLK cycles. The supported range is from 1 to 15 cycles. By default, the glitch filter is disabled (ECCCTL0[QUALPRD] = 0) to maintain compatibility. 

## _**7.5.7.4.3 Input Capture Signal Selection**_ 

Functionality and features include: 

- eCAP has up to 256 input capture sources. These enable pulse width measurements of internal design signals if necessary. 

- ECCCTL0[INPUTSEL] can be used select one of the 256 inputs. 

## _**7.5.7.4.4 Modulo 4 Counter**_ 

Functionality and features include: 

- The Mod4 (2 bit) counter is incremented via edge qualified events (CEVT1-CEVT4) 

The Mod4 counter continues counting (0→1→2→3→0…) and wraps around unless stopped. 

A 2 bit _Stop_ register is used to compare the Mod4 counter output, and when equal, stops the Mod4 counter and inhibits further loads of the CAP1-CAP4 registers. This occurs during _one-shot_ operation. 

## _**7.5.7.4.5 Edge Polarity Select and Qualifier**_ 

Functionality and features include: 

- Four independent edge polarity (rising edge/falling edge) selection muxes are used, one for each capture event. 

- Each edge (up to 4) is event qualified by the Modulo4 sequencer. 

- The edge event is gated to the respective CAPx register by the Mod4 counter. The CAPx register is loaded on the falling edge. 

## _**7.5.7.4.6 Continuous/One-Shot Control**_ 

Operation of eCAP in Continuous/One-Shot mode: 

- The Mod4 (2-bit) counter is incremented using edge qualified events (CEVT1-CEVT4). 

- The Mod4 counter continues counting (0->1->2->3->0) and wraps around unless stopped. 

- During one-shot operation, a 2-bit stop register (STOP_WRAP) is used to compare the Mod4 counter output, and when equal, stops the Mod4 counter and inhibits further loads of the CAP1-CAP4 registers. In this mode, if TSCCTR counter is configured to reset on capture event (CEVTx) by configuring ECCTL1.CTRRSTx bit, the operation still keeps resetting the TSCCTR counter on capture event (CEVTx) after the STOP_WRAP value is reached and re-arm (REARM) has not occurred. 

The continuous/one-shot block controls the start, stop and reset (zero) functions of the Mod4 counter, using a mono-shot type of action that can be triggered by the stop-value comparator and re-armed using software control. 

Once armed, the eCAP module waits for 1-4 (defined by stop-value) capture events before freezing both the Mod4 counter and contents of CAP1-4 registers (time stamps). 

Re-arming prepares the eCAP module for another capture sequence. Also, re-arming clears (to zero) the Mod4 counter and permits loading of CAP1-4 registers again, providing the CAPLDEN bit is set. 

In continuous mode, the Mod4 counter continues to run (0->1->2->3->0, the one-shot action is ignored, and capture values continue to be written to CAP1-4 in a circular buffer sequence. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 787 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [354 x 287] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 1 2 3<br>2:4 MUX<br>ECCTL2[MODCNTRSTS]<br>2<br>CEVT1<br>CEVT2<br>CLK<br>Modulo 4 CEVT3<br>counter CEVT4<br>RST ECCTL2[CTRFILTRESET]<br>Stop<br>Mod_eq<br>One−shot<br>control logic<br>Stop value (2b)<br>ECCTL2[STOP_WRAP] ECCTL2[RE−ARM]<br>ECCTL2[CONT/ONESHT]<br>**----- End of picture text -----**<br>


**Figure 7-300. Details of the Continuous/One-shot Block** 

788 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.7.4.7 32-Bit Counter and Phase Control**_ 

This counter provides the time-base for event captures, and is clocked using the system clock. 

A phase register is provided to achieve synchronization with other counters using a hardware and software forced sync. This is useful in APWM mode when a phase offset between modules is needed. 

On any of the four event loads, an option to reset the 32-bit counter is given. This is useful for time difference capture. The 32-bit counter value is captured first, then the counter value is reset to 0 by any of the LD1-LD4 signals. 

## _**7.5.7.4.8 CAP1-CAP4 Registers**_ 

These 32-bit registers are supplied by the 32-bit counter timer bus, CTR[0-31], and are loaded (capture a time-stamp) when the respective LD inputs are strobed. 

Control bit CAPLDEN can inhibit loading of the capture registers. During one-shot operation, this bit is cleared (loading is inhibited) automatically when a stop condition occurs, StopValue = Mod4. 

CAP1 and CAP2 registers become the active period and compare registers, respectively, in APWM mode. 

CAP3 and CAP4 registers become the respective shadow registers (APRD and ACMP) for CAP1 and CAP2 during APWM operation. 

## _**7.5.7.4.9 eCAP Synchronization**_ 

eCAP modules can be synchronized with each other by selecting a common SYNCIN source. SYNCIN source for eCAP can be either software sync-in or external sync-in. The external sync-in signal can come from ePWM. The SWSYNC of the eCAP module is logical ORed with the SYNC signal as shown in Figure 7-301. The SYNC signal is defined by the selection of ECAPxSYNCINSEL[SEL] as shown in Figure 7-302. 

**==> picture [311 x 228] intentionally omitted <==**

**----- Start of picture text -----**<br>
SYNC<br>ECCTL2[SWSYNC]<br>ECCTL2[SYNCOSEL]<br>SYNCI<br>CTR = PRD<br>Disable SYNCO<br>ECCTL2[SYNCI_EN]<br>Disable<br>Sync out<br>select<br>CTRPHS<br>LD_CTRPHS RST Delta-mode<br>TSCTR<br>(counter 32 b)<br>SYSCLK CLK OVF CTR-OVF<br>CTR[31-0]<br>**----- End of picture text -----**<br>


**Figure 7-301. Details of the Counter and Synchronization Block** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 789 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 228] intentionally omitted <==**

**Figure 7-302. eCAP Synchronization Scheme** 

## _**7.5.7.4.9.1 Example 1 - Using SWSYNC with ECAP Module**_ 

Implement the following steps to use SWSYNC with ECAP1 and ECAP2. 

- Configure ECAP[1..2].ECAPSYNCINSEL.SEL = 0x0 to disable external SYNCIN coming to eCAP1. 

- Configure ECAP[1..2].ECCTL2.SWSYNC = 0x1, to force Software Synchronization of the TSCTR counter. 

To use SWSYNC with other eCAP modules, make sure that the previous eCAP chain is not generating a SYNCOUT signal that interferes with the software synchronization. 

790 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.7.4.10 DMA Interrupt**_ 

On Type 0 eCAP modules, the CPU was required to begin data transfers using DMA. New to the Type 1 eCAP, a separate DMA Trigger (ECAP_DMA_INT) enables continuous transfer of capture data from eCAP registers to on-chip memory using DMA. Any one of the four available interrupt events (CEVT1, CEVT2, CEVT3, and CEVT4) can be selected as the trigger source for ECAP_DMA_INT using ECCTL2 [DMAEVTSEL]. 

New to the Type 3 eCAP is the ability to trigger DMA events in APWM mode. Any one of three available events (period match, compare match, or both) can be selected as the trigger source for ECAP_DMA_INT using ECCTL2 [DMAEVTSEL]. 

## _**7.5.7.4.11 ADC SOC Event**_ 

Type 3 introduces the capability to generate ADC SOC events in capture mode and in APWM mode of operation. The ability to start ADC conversions allows for increased APWM functionality, as well as the ability to synchronize capture events with ADC samples. 

In capture mode, one of the four available interrupt events (CEVT1, CEVT2, CEVT3, and CEVT4) can be selected as ECAP_SOC_EVT using ECCCTL0[SOCEVTSEL]. 

In APWM mode, any one of three available events (period match, compare match, or both) can be selected as ECAP_SOC_EVT using ECCCTL0[SOCEVTSEL]. 

## _**7.5.7.4.12 APWM Mode Operation**_ 

Main operating highlights of the APWM section: 

- The time-stamp counter bus is made available for comparison by way of 2 digital (32-bit) comparators. 

- When CAP1/2 registers are not used in capture mode, the contents can be used as Period and Compare values in APWM mode. 

- Double buffering is achieved using shadow registers APRD and ACMP (CAP3/4). The shadow register contents are transferred over to CAP1/2 registers, either immediately upon a write, or on a CTR = PRD trigger. 

- In APWM mode, writing to CAP1/CAP2 active registers also writes the same value to the corresponding shadow registers CAP3/CAP4. This emulates immediate mode. Writing to the shadow registers CAP3/CAP4 invokes the shadow mode. 

- During initialization, write to the active registers for both period and compare. This automatically copies the initial values into the shadow values. For subsequent compare updates during run-time, use the shadow registers. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

791 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [405 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
TSCTR<br>FFFFFFFF<br>1000h<br>APRD<br>500h<br>ACMP<br>300h<br>0000000C<br>APWMx<br>(o/p pin)<br>Off−time<br>On Period<br>time<br>**----- End of picture text -----**<br>


**Figure 7-303. PWM Waveform Details Of APWM Mode Operation** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

792 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

The behavior of APWM active high mode (APWMPOL == 0) is as follows: 

```
CMP = 0x00000000, output low for duration of period (0% duty)
```

```
CMP = 0x00000001, output high 1 cycle
```

```
CMP = 0x00000002, output high 2 cycles
```

```
CMP = PERIOD, output high except for 1 cycle (<100% duty)
```

```
CMP = PERIOD+1, output high for complete period (100% duty)
```

```
CMP > PERIOD+1, output high for complete period
```

The behavior of APWM active low mode (APWMPOL == 1) is as follows: 

```
CMP = 0x00000000, output high for duration of period (0% duty)
```

```
CMP = 0x00000001, output low 1 cycle
```

```
CMP = 0x00000002, output low 2 cycles
```

```
CMP = PERIOD, output low except for 1 cycle (<100% duty)
```

```
CMP = PERIOD+1, output low for complete period (100% duty)
```

```
CMP > PERIOD+1, output low for complete period
```

**==> picture [336 x 89] intentionally omitted <==**

**----- Start of picture text -----**<br>
TPWM<br>4 4 4<br>3 3 3<br>2 2 2 TPWM �CAP1� 1� u TTSCTR<br>1 1 1<br>1<br>0 0 0 FPWM<br>TPWM<br>**----- End of picture text -----**<br>


**Figure 7-304. Time-Base Frequency and Period Calculation** 

## _**7.5.7.4.13 Signal Monitoring Unit**_ 

The signal monitoring unit can be used for edge, pulse width, and period monitoring of ECAP input signals. This allows for detection that is useful for many applications. For example, EPWM pulse width boundary monitoring can be accomplished for safety applications. 

The high-level features of the signal monitoring unit include: 

- Measure pulse width (high or low) and check if the pulse width is in expected range 

- Measure period (rise-to-rise or fall-to-fall) and check if the period is in expected range 

- Monitor signal edge (rise or fall) and check if the signal edge occurs in a user-programmed time window 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 793 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.7.4.13.1 Pulse Width and Period Monitoring**_ 

The signal monitoring unit has the ability to measure pulse width (either low or high) or period (rise-to-rise edge or fall-to-fall edge) and automatically generate an error when the pulse width is outside of a programmable expected range. 

The expected pulse width range is programmable using the following configuration registers (or their respective shadow registers): 

- MUNIT_#_MIN programs the minimum pulse width capture value 

- MUNIT_#_MAX programs the maximum pulse width capture value 

Any pulse width outside of these programmed bounds triggers one of two error events: 

- MUNIT_#_ERROR_EVT1 generated when measured pulse width is less than MUNIT_#_MIN 

- MUNIT_#_ERROR_EVT2 generated when measured pulse width is greater than MUNIT_#_MAX 

The following diagram provides an example in which the measured pulse width exceeds the MAX value, generating an ERROR_EVT2 event. 

**==> picture [472 x 309] intentionally omitted <==**

**----- Start of picture text -----**<br>
PWM<br>TB Counter<br>PWM<br>End of pulse expected<br>ECAP cnt1 cnt2 cnt3<br>Counter<br>CAP1 cnt1 cnt3<br>CAP2 cnt2<br>tpulse_width_min<br>tpulse_width_max<br>tpulse_width_actual<br>ERROR_EVT2<br>**----- End of picture text -----**<br>


**Figure 7-305. ECAP Signal Monitoring Unit Pulse Width Error Example** 

## **Configuration Requirements** 

To enable this mode, the following settings must be configured: 

- Absolute mode must be set for the ECAP counter, so that the counter is free running and does not get reset on any capture events 

- Continuous mode must be enabled (one-shot mode can be used, but is not recommended given the short duration) 

- Sync feature for the counter must be disabled (ECCTL2.SYNCI_EN = 0) 

- A minimum of two captures must be enabled (ECCTL2.STOP_WRAP >= 1, and at least CAP1 and CAP2 enabled) 

794 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- Capture Edge (ECCTL1.CAPxPOL) of used capture modules (any of CAP1 to CAP4) must be configured to capture two edges of interest 

   - High pulse: one rising edge and one falling edge 

   - Low pulse: one rising edge and one falling edge 

   - Period rise-to-rise: two rising edges 

   - Period fall-to-fall: two falling edges 

## **Note** 

If a pulse width is greater than the MAX value, a second edge can arrive late or never even occur. Because of this, the DISABLE_EARLY_MAX_ERR field in the MUNIT_#_CTL register can be used to choose when a MAX error occurs. By setting the bit to 0, an error is generated as soon as the pulse width is greater than the specified maximum value. By setting the bit to 1, an error is generated when the second event has occurred. 

## _**7.5.7.4.13.2 Edge Monitoring**_ 

The signal monitoring unit has the ability to monitor and check if a rise or fall edge occurs within a specified time window and automatically generate an error when an edge occurs outside of this window. 

The time window of an expected edge event can be programmed using the following configuration registers (or their respective shadow registers): 

- MUNIT_#_MIN programs the minimum pulse width capture value 

- MUNIT_#_MAX programs the maximum pulse with capture value 

Any edge that occurs outside of these programmed bounds triggers the following error event: 

- MUNIT_#_ERROR_EVT1 generated when edge occurs outside the bounds of MUNIT_#_MIN and MUNIT_#_MAX. 

Additionally, ERROR_EVT2 is generated if either MIN or MAX did not occur between two sync events. 

The following diagram provides an example in which a rising edge does not occur during the expected window, generating an ERROR_EVT1 event. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

795 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [459 x 268] intentionally omitted <==**

**----- Start of picture text -----**<br>
PWM<br>TB Counter<br>PWM<br>Rising edge expecte d<br>ECAP<br>Counter<br>CAP1 cnt1 cnt1<br>Sync<br>Event<br>trise_edge_min<br>trise_edge_max<br>trise_edge_actual<br>**----- End of picture text -----**<br>


**==> picture [55 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
ERROR_EVT1<br>**----- End of picture text -----**<br>


**Figure 7-306. ECAP Signal Monitoring Unit Edge Error Example** 

## **Configuration Requirements** 

To enable this mode, the following settings must be configured: 

- The ECAP counter must be synced with an EPWM module 

- Absolute mode must be set for the ECAP counter, so that the counter is free running and does not get reset on any capture events 

- Continuous mode can be enabled (one-shot mode can be used, but is not recommended given the modes short duration) 

- A minimum of one capture can be enabled (ECCTL2.STOP_WRAP >= 0, and at least CAP1 enabled) 

- Capture Edge (ECCTL1.CAPxPOL) of used capture modules (any of CAP1 to CAP4) must be configured to capture an edge of interest 

- The time window defined using MIN and MAX can not cross the sync boundary 

## **Note** 

The following are important considerations when configuring the edge monitoring feature: 

- If the EPWM counter or ECAP counter are loaded with a non-zero phase value, the MIN and MAX values must be adjusted accordingly in SW. This also applies when the glitch filter is enabled, as the glitch filter delays the signal by QUALPRD+1 

- The edge monitoring logic restarts on a sync event. This is to avoid any deadlock in case MIN, MAX, or both events do not occur between two sync events. ERROR_EVT2 is generated, if MIN or MAX match did not occur between two sync events 

- The time window defined using MIN and MAX can not cross the sync boundary 

796 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.7.5 APWM Mode Operation** 

eCAP module is used to implement a single-channel PWM generator (with 32-bit capabilities) when the eCAP module is not being used for input captures. The counter operates in count-up mode, providing a time-base for asymmetrical pulse width modulation (PWM) waveforms. The CAP1 and CAP2 registers become the active period and compare registers, respectively, while CAP3 and CAP4 registers become the period and compare shadow registers, respectively. Figure 7-307 is a high-level view of both the capture and auxiliary pulse-width modulator (APWM) modes of operation. 

**==> picture [354 x 207] intentionally omitted <==**

- A. A single pin is shared between CAP and APWM functions. In capture mode, the pin is an input; in APWM mode, the pin is an output. 

- B. In APWM mode, writing any value to CAP1/CAP2 active registers also writes the same value to the corresponding shadow registers CAP3/CAP4. This emulates immediate mode. Writing to the shadow registers CAP3/CAP4 invokes the shadow mode. 

## **Figure 7-307. eCAP APWM Mode Block Diagram** 

Main operating highlights of the APWM section: 

- The time-stamp counter bus is made available for comparison by way of 2 digital (32-bit) comparators. 

- When CAP1/2 registers are not used in capture mode, the contents can be used as Period and Compare values in APWM mode. 

- Double buffering is achieved using shadow registers APRD and ACMP (CAP3/4). The shadow register contents are transferred over to CAP1/2 registers, either immediately upon a write, or on a CTR = PRD trigger. 

- In APWM mode, writing to CAP1/CAP2 active registers also writes the same value to the corresponding shadow registers CAP3/CAP4. This emulates immediate mode. Writing to the shadow registers CAP3/CAP4 invokes the shadow mode. 

- During initialization, write to the active registers for both period and compare. This automatically copies the initial values into the shadow values. For subsequent compare updates during run-time, use the shadow registers. 

## **Note** 

The ECAP output is not inhibited when in APWM mode, once the ECAP is configured in the APWM mode, the output starts taking effect. Consider enabling the OUTPUTXBAR configuration (or any internal loopbacks) for ECAP APWM after the ECAP has been configured to avoid any unwanted glitches in the output while configurations. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

797 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Note** 

The ECAP Period and Compare active registers are updated with the shadow register values either immediately or at CTR=PRD trigger, when expecting shadow load mode. Shadow values must be updated within the same period of the ECAP APWM to avoid any unexpected Period/Duty Changes 

Figure 7-308 further describes the output of the eCAP in APWM mode based on the CMP and PRD values. 

**==> picture [500 x 173] intentionally omitted <==**

**Figure 7-308. Counter Compare Operation** 

**==> picture [336 x 89] intentionally omitted <==**

**----- Start of picture text -----**<br>
TPWM<br>4 4 4<br>3 3 3<br>2 2 2 TPWM �CAP1� 1� u TTSCTR<br>1 1 1<br>1<br>0 0 0 FPWM<br>TPWM<br>**----- End of picture text -----**<br>


**Figure 7-309. Time-Base Frequency and Period Calculation** 

## **APWM Mode Operation – Active High mode** 

798 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 251] intentionally omitted <==**

**Figure 7-310. APWM Mode Operation (Active High Mode – APWMPOL == 0)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

799 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

The behavior of APWM active high mode (APWMPOL == 0) is as follows: 

```
CMP = 0x00000000, output low for duration of period (0% duty)
```

```
CMP = 0x00000001, output high 1 cycle
```

```
CMP = 0x00000002, output high 2 cycles
```

```
CMP = PERIOD, output high except for 1 cycle (<100% duty)
```

```
CMP = PERIOD+1, output high for complete period (100% duty)
```

```
CMP > PERIOD+1, output high for complete period
```

## **APWM Mode Operation – Active Low mode** 

**==> picture [500 x 251] intentionally omitted <==**

**Figure 7-311. APWM Mode Operation (Active Low Mode – APWMPOL == 1) Details** 

The behavior of APWM active low mode (APWMPOL == 1) is as follows: 

```
CMP = 0x00000000, output high for duration of period (0% duty)
```

```
CMP = 0x00000001, output low 1 cycle
```

```
CMP = 0x00000002, output low 2 cycles
```

```
CMP = PERIOD, output low except for 1 cycle (<100% duty)
```

```
CMP = PERIOD+1, output low for complete period (100% duty)
```

```
CMP > PERIOD+1, output low for complete period
```

800 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.7.6 eCAP Synchronization and Events** 

External events can be used to synchronize the eCAP and send out sync, interrupt, DMA, and SOC events. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

801 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.7.6.1 eCAP Synchronization**_ 

eCAP modules can be synchronized with each other by selecting a common SYNCIN source. SYNCIN source for eCAP can be either software sync-in or external sync-in. The external sync-in signal can come from the EPWM. The SWSYNC of the eCAP module is logical ORed with the SYNC signal as shown in Figure 7-312. The SYNC signal is defined by the selection of ECAPxSYNCINSEL[SEL] as shown in Figure 7-313. 

**==> picture [275 x 229] intentionally omitted <==**

**----- Start of picture text -----**<br>
SYNC<br>ECCTL2[SWSYNC]<br>ECCTL2[SYNCOSEL]<br>SYNCI<br>CTR = PRD<br>Disable SYNCO<br>ECCTL2[SYNCI_EN]<br>Disable<br>Sync out<br>select<br>CTRPHS<br>LD_CTRPHS RST Delta-mode<br>TSCTR<br>(counter 32 b)<br>SYSCLK CLK OVF CTR-OVF<br>**----- End of picture text -----**<br>


CTR[31-0] 

**Figure 7-312. Details of the Counter and Synchronization Block** 

**==> picture [500 x 228] intentionally omitted <==**

**Figure 7-313. eCAP Synchronization Scheme** 

## _**7.5.7.6.1.1 Example 1 - Using SWSYNC with ECAP Module**_ 

Implement the following steps to use SWSYNC with ECAP1 and ECAP2. 

- Configure ECAP[1..2].ECAPSYNCINSEL.SEL = 0x0 to disable external SYNCIN coming to eCAP1. 

- Configure ECAP[1..2].ECCTL2.SWSYNC = 0x1, to force Software Synchronization of the TSCTR counter. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

802 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

To use SWSYNC with other eCAP modules, make sure that the previous eCAP chain is not generating a SYNCOUT signal that interferes with the software synchronization. 

## _**7.5.7.6.2 Interrupt Control**_ 

Operation and features of the eCAP interrupt control include (see Figure 7-314): 

- An interrupt can be generated on capture events (CEVT1-CEVT4, CTROVF) or APWM events (CTR = PRD, CTR = CMP). 

- An interrupt can be generated on signal monitoring errors (MUNIT_1_ERROR_EVT1, MUNIT_1_ERROR_EVT1, MUNIT_2_ERROR_EVT1, MUNIT_2_ERROR_EVT2) 

- A counter overflow event (FFFFFFFF->00000000) is also provided as an interrupt source (CTROVF). 

- The capture events are edge and sequencer-qualified (ordered in time) by the polarity select and Mod4 gating, respectively. 

- One of these events can be selected as the interrupt source (from the eCAPx module) going to the PIE 

- Seven interrupt events (CEVT1, CEVT2, CEVT3, CEVT4, CNTOVF, CTR=PRD, CTR=CMP) can be generated. 

- An additional four interrupt events (MUNIT_1_ERROR_EVT1, MUNIT_1_ERROR_EVT1, MUNIT_2_ERROR_EVT1, MUNIT_2_ERROR_EVT2) can be generated from the signal monitoring unit. 

- The interrupt enable register (ECEINT) is used to enable/disable individual interrupt event sources. The interrupt flag register (ECFLG) indicates if any interrupt event has been latched and contains the global interrupt flag bit (INT). An interrupt pulse is generated to the PIE only if any of the interrupt events are enabled, the flag bit is 1, and the INT flag bit is 0. The interrupt service routine must clear the global interrupt flag bit and the serviced event using the interrupt clear register (ECCLR) before any other interrupt pulses are generated. All interrupt flags are cleared upon an event filter reset by writing a 1 to ECCTL2[CLRFILTRESET]. To force an interrupt event, use the interrupt force register (ECFRC). This is useful for test purposes. 

## **Note** 

The CEVT1, CEVT2, CEVT3, CEVT4 flags are only active in capture mode (ECCTL2[CAP/APWM == 0]). The CTR=PRD, CTR=CMP flags are only valid in APWM mode (ECCTL2[CAP/APWM == 1]). CNTOVF flag is valid in both modes. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

803 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [436 x 414] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 0<br>0 CEVT1<br>ECCTL2.CAP_APWM<br>1 0<br>0 CEVT2<br>ECCTL2.CAP_APWM<br>1 0<br>0 CEVT3<br>ECCTL2.CAP_APWM<br>1 0<br>0 CEVT4<br>ECCTL2.CAP_APWM<br>1 PRDEQ<br>0 0<br>ECCTL2.CAP_APWM<br>1 CMPEQ<br>0 0<br>ECCTL2.CAP_APWM<br>**----- End of picture text -----**<br>


**Figure 7-314. Interrupts in eCAP Module** 

804 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.7.6.3 DMA Interrupt**_ 

On Type 0 eCAP modules, the CPU was required to begin data transfers using DMA. New to the Type 1 eCAP, a separate DMA Trigger (ECAP_DMA_INT) enables continuous transfer of capture data from eCAP registers to on-chip memory using DMA. Any one of the four available interrupt events (CEVT1, CEVT2, CEVT3, and CEVT4) can be selected as the trigger source for ECAP_DMA_INT using ECCTL2 [DMAEVTSEL]. 

New to the Type 3 eCAP is the ability to trigger DMA events in APWM mode. Any one of three available events (period match, compare match, or both) can be selected as the trigger source for ECAP_DMA_INT using ECCTL2 [DMAEVTSEL]. 

## **Note** 

ECAPxINT interrupt cannot be used as DMA trigger because after first interrupt, no further ECAPxINT is generated until CPU clears ECFLG[INT] in interrupt service routine which is not possible on DMA without CPU intervention. 

## _**7.5.7.6.4 ADC SOC Event**_ 

Type 3 introduces the capability to generate ADC SOC events in capture mode and in APWM mode of operation. The ability to start ADC conversions allows for increased APWM functionality, as well as the ability to synchronize capture events with ADC samples. 

In capture mode, one of the four available interrupt events (CEVT1, CEVT2, CEVT3, and CEVT4) can be selected as ECAP_SOC_EVT using ECCCTL0[SOCEVTSEL]. 

In APWM mode, any one of three available events (period match, compare match, or both) can be selected as ECAP_SOC_EVT using ECCCTL0[SOCEVTSEL]. 

## _**7.5.7.6.5 Shadow Load and Lockout Control**_ 

In capture mode, this logic inhibits (locks out) any shadow loading of CAP1 or CAP2 from APRD and ACMP registers, respectively. 

In APWM mode, shadow loading is active and two choices are permitted: 

- Immediate - APRD or ACMP are transferred to CAP1 or CAP2 immediately upon writing a new value. 

- On period equal, CTR[31:0] = PRD[31:0]. 

## **7.5.7.7 Signal Monitoring Unit** 

The signal monitoring unit can be used for edge, pulse width, and period monitoring of eCAP input signals. This allows for detection that is useful for many applications. For example, ePWM pulse width boundary monitoring can be accomplished for safety applications. 

The high-level features of the signal monitoring unit include: 

- Measure pulse width (high or low) and check if it is in expected range 

- Measure period (rise-to-rise or fall-to-fall) and check if it is in expected range 

- Monitor signal edge (rise or fall) and check if it occurs in a user-programmed time window 

## _**7.5.7.7.1 Pulse Width and Period Monitoring**_ 

The signal monitoring unit has the ability to measure pulse width (either low or high) or period (rise-to-rise edge or fall-to-fall edge) and automatically generate an error when the pulse width is outside of a programmable expected range. 

The expected pulse width range is programmable using the following configuration registers (or their respective shadow registers): 

- MUNIT_#_MIN programs the minimum pulse width capture value 

- MUNIT_#_MAX programs the maximum pulse width capture value 

Any pulse width outside of these programmed bounds triggers one of two error events: 

- MUNIT_#_ERROR_EVT1 generated when measured pulse width is less than MUNIT_#_MIN 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 805 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- MUNIT_#_ERROR_EVT2 generated when measured pulse width is greater than MUNIT_#_MAX 

The following diagram provides an example in which the measured pulse width exceeds the MAX value, generating an ERROR_EVT2 event. 

**==> picture [472 x 308] intentionally omitted <==**

**----- Start of picture text -----**<br>
PWM<br>TB Counter<br>PWM<br>End of pulse expected<br>ECAP cnt1 cnt2 cnt3<br>Counter<br>CAP1 cnt1 cnt3<br>CAP2 cnt2<br>tpulse_width_min<br>tpulse_width_max<br>tpulse_width_actual<br>ERROR_EVT2<br>**----- End of picture text -----**<br>


**Figure 7-315. eCAP Signal Monitoring Unit Pulse Width Error Example** 

## **Configuration Requirements** 

To enable this mode, the following settings must be configured: 

- Absolute mode must be set for the eCAP counter, so that the counter is free running and does not get reset on any capture events 

- Continuous mode must be enabled (one-shot mode can be used, but is not recommended given the short duration) 

- Sync feature for the counter must be disabled (ECCTL2.SYNCI_EN = 0) 

- A minimum of two captures must be enabled (ECCTL2.STOP_WRAP >= 1, and at least CAP1 and CAP2 enabled) 

- Capture Edge (ECCTL1.CAPxPOL) of used capture modules (any of CAP1 to CAP4) must be configured to capture two edges of interest 

   - High pulse: one rising edge and one falling edge 

   - Low pulse: one rising edge and one falling edge 

   - Period rise-to-rise: two rising edges 

   - Period fall-to-fall: two falling edges 

806 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **Note** 

If a pulse width is greater than the MAX value, a second edge can arrive late or never even occur. Because of this, the DISABLE_EARLY_MAX_ERR field in the MUNIT_#_CTL register can be used to choose when a MAX error occurs. By setting the bit to 0, an error is generated as soon as the pulse width is greater than the specified maximum value. By setting the bit to 1, an error is generated when the second event has occurred. 

## _**7.5.7.7.2 Edge Monitoring**_ 

The signal monitoring unit has the ability to monitor and check if a rise or fall edge occurs within a specified time window and automatically generate an error when an edge occurs outside of this window. 

The time window of an expected edge event can be programmed using the following configuration registers (or their respective shadow registers): 

- MUNIT_#_MIN programs the minimum pulse width capture value 

- MUNIT_#_MAX programs the maximum pulse with capture value 

Any edge that occurs outside of these programmed bounds triggers the following error event: 

- MUNIT_#_ERROR_EVT1 generated when edge occurs outside the bounds of MUNIT_#_MIN and MUNIT_#_MAX. 

Additionally, ERROR_EVT2 is generated if either MIN or MAX did not occur between two sync events. 

## **Configuration Requirements** 

To enable this mode, the following settings must be configured: 

- The eCAP counter must be synced with an ePWM module 

- Absolute mode must be set for the eCAP counter, so that the counter is free running and does not get reset on any capture events 

- Continuous mode can be enabled (one-shot mode can be used, but is not recommended given the modes short duration) 

- A minimum of one capture can be enabled (ECCTL2.STOP_WRAP >= 0, and at least CAP1 enabled) 

- Capture Edge (ECCTL1.CAPxPOL) of used capture modules (any of CAP1 to CAP4) must be configured to capture an edge of interest 

## **Note** 

The following are important considerations when configuring the edge monitoring feature: 

- If the ePWM counter or eCAP counter are loaded with a non-zero phase value, the MIN and MAX values must be adjusted accordingly in SW. This also applies when the glitch filter is enabled, as the glitch filter delays the signal by QUALPRD+1 

- The edge monitoring logic restarts on a sync event. This is to avoid any deadlock in case MIN, MAX, or both events do not occur between two sync events. ERROR_EVT2 is generated, if MIN or MAX match did not occur between two sync events 

- The time window defined using MIN and MAX can not cross the sync boundary 

- MIN and MAX are counter values (or number of clock cycles for a 200 MHz system clock). For width monitoring, the pulse/period width is between MIN and MAX no. of counter counts (or MIN*5 ns < pulse/period < MAX*5 ns). For edge monitoring, the edge is expected to occur between counter values of MIN and MAX after the sync (or MIN*5 ns < edge < MAX*5 ns, with reference to sync). 

The following diagram provides an example in which a rising edge does not occur during the expected window, generating an ERROR_EVT1 event. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

807 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [459 x 268] intentionally omitted <==**

**----- Start of picture text -----**<br>
PWM<br>TB Counter<br>PWM<br>Rising edge expecte d<br>ECAP<br>Counter<br>CAP1 cnt1 cnt1<br>Sync<br>Event<br>trise_edge_min<br>trise_edge_max<br>trise_edge_actual<br>**----- End of picture text -----**<br>


**==> picture [55 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
ERROR_EVT1<br>**----- End of picture text -----**<br>


**Figure 7-316. eCAP Signal Monitoring Unit Edge Error Example** 

## _**7.5.7.7.3 Error Events**_ 

When a signal monitoring error occurs, the signal monitoring is disabled by clearing MUNIT_x_CTL.EN. In addition, further captures are disabled by clearing ECCTL1.CAPLDEN, but time stamp values in CAP1..4 are retained for debug purpose. To re-enable signal monitoring MUNIT_x_CTL.EN and ECCTL1.CAPLDEN need to be set again. CEVTx is generated even after an error is detected and further captures are disabled. 

## _**7.5.7.7.4 Disabling the Signal Monitoring Unit**_ 

When monitoring the PWMs, PWMs can be tripped by the external trip event that is forced to a known state. Under this condition, PWM signal monitoring is disabled temporarily until the trip condition is cleared. To support this feature, PWM trip signals are brought into eCAP module through external XBARs. In addition, an internal MUX is provided to select one of many XBAR signals. Signal monitoring is disabled as long on selected trip signal is active. Note that signal monitoring is automatically enabled when trip condition is cleared. 

**==> picture [432 x 106] intentionally omitted <==**

**Figure 7-317. ECAP Signal Monitoring Unit Trip Signals** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

808 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **Note** 

EPWM trips are asynchronous in nature, PWM are tripped asynchronously and immediately. As a result of this, there can be a race condition that can lead to signal monitoring error. This can’t be avoided and has to be handled in SW. 

## _**7.5.7.7.5 Shadow Control**_ 

Shadow registers for MIN and MAX values enable the application to change these values dynamically as the PWM configuration changes. However, shadow to active loading need to happen at certain point of time to keep these in sync with ePWM module. Global load strobe (EPWMx.GLDSTRB) from ePWM is used for this purpose. Since a given eCAP module can be associated with any ePWM module, a mux is provided select one of EPWMx.GLDSTRB in a system. 

Shadow registers are copied to active registers on following events: 

- SW event by writing ‘1’ to MUNIT_{#}_SHADOW_CTL.SWSYNC 

   - Usage: User programs shadow registers and writes ‘1’ to MUNIT_{#}_SHADOW_CTL.SWSYNC to copy these values to active registers 

- On eCAP sync event selected by ECAPSYNCINSEL.SEL 

- On ePWM Global Load event selected by MUNIT_COMMON_CTL.GLDSTRBSEL 

**==> picture [372 x 192] intentionally omitted <==**

**Figure 7-318. ECAP Signal Monitoring Unit Shadow Control** 

## **Note** 

If shadow to active event occurs while signal monitoring in the midst of pulse (after first edge has occurred) or edge (after time window started) monitoring, the current check gets aborted and new values then take effect from next pulse or sync cycle respectively. This is to make sure that false errors are not generated. 

## _**7.5.7.7.6 Trip Signal**_ 

Trip signal is generated upon signal monitoring errors. All the signal monitoring error events are OR-ed and provided as a trip output. The trip signal remains active until interrupt flags are cleared in ECFLG register. Trip cannot be disabled in eCAP, instead the trip has to be deselected in external XBAR if there is no intent to use the feature. 

The ECAPx.TRIPOUT signal can be used to trip the EPWM modules. This can cause the EPWMx.TRIPOUT signal, which is fed back to eCAP module to also trip, which can disable the monitoring function and also cause a false trip if this feature is enabled. Therefore, if ECAPx.TRIPOUT is used, it is recommended that EPWMx.TRIPOUT be disabled. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 809 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.7.8 Application of the eCAP Module** 

The following sections provide applications examples to show how to operate the eCAP module. 

## _**7.5.7.8.1 Example 1 - Absolute Time-Stamp Operation Rising-Edge Trigger**_ 

Figure 7-319 shows an example of continuous capture operation (Mod4 counter wraps around). In this figure, TSCTR counts-up without resetting and capture events are qualified on the rising edge only, this gives period (and frequency) information. 

On an event, the TSCTR contents (time-stamp) is first captured, then Mod4 counter is incremented to the next state. When the TSCTR reaches FFFFFFFF (maximum value), the Mod4 counter wraps around to 00000000 (not shown in Figure 7-319), if this occurs, the CTROVF (counter overflow) flag is set, and an interrupt (if enabled) occurs. Captured Time-stamps are valid at the point indicated by the diagram (after the fourth event); hence, event CEVT4 can conveniently be used to trigger an interrupt and the CPU can read data from the CAPx registers. 

**==> picture [440 x 311] intentionally omitted <==**

**----- Start of picture text -----**<br>
CEVT1 CEVT2 CEVT3 CEVT4 CEVT1<br>CAPx pin<br>t4 t5<br>FFFFFFFF t3<br>t2<br>CTR[0−31] t1<br>00000000<br>MOD4<br>0 1 2 3 0 1<br>CTR<br>CAP1 XX t1 t5<br>CAP2 XX t2<br>CAP3 XX t3<br>CAP4 XX t4<br>t<br>Polarity selection All capture values valid<br>(can be read) at this time<br>Capture registers [1−4]<br>**----- End of picture text -----**<br>


**Figure 7-319. Capture Sequence for Absolute Time-stamp and Rising-Edge Detect** 

810 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.7.8.2 Example 2 - Absolute Time-Stamp Operation Rising- and Falling-Edge Trigger**_ 

In Figure 7-320, the eCAP operating mode is almost the same as in the previous section except capture events are qualified as either rising or falling edge, this now gives both period and duty cycle information, that is: Period1 = t3 – t1, Period2 = t5 – t3, …and so on. Duty Cycle1 (on-time %) = (t2 – t1) / Period1 x 100%, and so on. Duty Cycle1 (off-time %) = (t3 – t2) / Period1 x 100%, and so on. 

**==> picture [456 x 356] intentionally omitted <==**

**----- Start of picture text -----**<br>
CEVT2 CEVT4 CEVT2 CEVT4<br>CEVT1 CEVT3 CEVT1 CEVT3 CEVT1<br>CAPx pin<br>FFFFFFFF t9<br>t8<br>t7<br>t6<br>t5<br>CTR[0−31] t4<br>t3<br>t2<br>t1<br>00000000<br>MOD4<br>0 1 2 3 0 1 2 3 0<br>CTR<br>CAP1 XX t1 t5<br>CAP2 XX t2 t6<br>CAP3 XX t3 t7<br>CAP4 XX t4 t8<br>tt<br>Polarity selection<br>Capture registers [1−4]<br>**----- End of picture text -----**<br>


**Figure 7-320. Capture Sequence for Absolute Time-stamp with Rising- and Falling-Edge Detect** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 811 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.7.8.3 Example 3 - Time Difference (Delta) Operation Rising-Edge Trigger**_ 

Figure 7-321 shows how the eCAP module can be used to collect delta timing data from pulse train waveforms. Here Continuous Capture mode (TSCTR counts-up without resetting, and Mod4 counter wraps around) is used. In Delta-time mode, TSCTR is reset back to zero on every valid event. Here capture events are qualified as rising edge only. On an event, TSCTR contents (Time-Stamp) is captured first, and then TSCTR is reset to zero. The Mod4 counter then increments to the next state. If TSCTR reaches FFFFFFFF (maximum value), before the next event, the Mod4 counter wraps around to 00000000 and continues, a CNTOVF (counter overflow) flag is set, and an interrupt (if enabled) occurs. The advantage of Delta-time mode is that the CAPx contents directly give timing data without the need for CPU calculations, that is, Period1 = T1, Period2 = T2, and so on. As shown in Figure 7-321, the CEVT1 event is a good trigger point to read the timing data, T1, T2, T3, T4 are all valid here. 

**==> picture [436 x 365] intentionally omitted <==**

**----- Start of picture text -----**<br>
CEVT1 CEVT2 CEVT3 CEVT4 CEVT1<br>CAPx pin<br>FFFFFFFF T1 T2 T3 T4<br>CTR[0−31]<br>00000000<br>MOD4<br>CTR 0 1 2 3 0 1<br>CAP1 XX CTR value at CEVT1 t4<br>CAP2 XX t1<br>CAP3 XX t2<br>CAP4 XX t3<br>t<br>Polarity selection<br>Capture registers [1−4] All capture values valid<br>(can be read) at this time<br>**----- End of picture text -----**<br>


**Figure 7-321. Capture Sequence for Delta Mode Time-stamp and Rising Edge Detect** 

812 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.7.8.4 Example 4 - Time Difference (Delta) Operation Rising- and Falling-Edge Trigger**_ 

In Figure 7-322, the eCAP operating mode is almost the same as in previous section except capture events are qualified as either rising or falling edge, this now gives both period and duty cycle information, that is: Period1 = T1+T2, Period2 = T3+T4, and so on. Duty Cycle1 (on-time %) = T1 / Period1 x 100%, Duty Cycle1 (off-time %) = T2 / Period1 x 100%, and so on. 

During initialization, write to the active registers for both period and compare. This action automatically copies the init values into the shadow values. For subsequent compare updates during run-time, the shadow registers must be used. 

**==> picture [433 x 356] intentionally omitted <==**

**----- Start of picture text -----**<br>
CEVT2 CEVT4 CEVT2 CEVT4<br>CEVT1 CEVT3 CEVT1 CEVT3 CEVT5<br>CAPx�pin<br>T1 T3 T5 T8<br>FFFFFFFF<br>T2 T6<br>T4 T7<br>CTR[0−31]<br>00000000<br>MOD4<br>0 1 2 3 0 1 2 3 0<br>CTR<br>CAP1 XX CTR�value�at�CEVT1 t4<br>CAP2 XX t1 t5<br>CAP3 XX t2 t6<br>CAP4 XX t3 t7<br>t<br>Polarity�selection<br>Capture�registers�[1−4]<br>**----- End of picture text -----**<br>


**Figure 7-322. Capture Sequence for Delta Mode Time-stamp with Rising- and Falling-Edge Detect** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 813 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.7.9 Application of the APWM Mode** 

In this example, the eCAP module is configured to operate as a PWM generator. Here, a very simple singlechannel PWM waveform is generated from the APWMx output pin. The PWM polarity is active high, which means that the compare value (CAP2 reg is now a compare register) represents the on-time (high level) of the period. Alternatively, if the APWMPOL bit is configured for active low, then the compare value represents the off-time. 

## _**7.5.7.9.1 Example 1 - Simple PWM Generation (Independent Channels)**_ 

**==> picture [405 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
TSCTR<br>FFFFFFFF<br>1000h<br>APRD<br>500h<br>ACMP<br>300h<br>0000000C<br>APWMx<br>(o/p pin)<br>Off−time<br>On Period<br>time<br>**----- End of picture text -----**<br>


**Figure 7-323. PWM Waveform Details of APWM Mode Operation** 

814 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.7.10 eCAP Programming Guide** 

## **Driver Information** 

Driver features are available at the ECAP driver page. 

## **Software API Information** 

The eCAP driver provides an API to configure the eCAP module. Full documentation is located on APIs for ECAP. 

## **Example Usage** 

The below links show examples on how to use the eCAP module: 

- ECAP Capture PWM 

- ECAP APWM Mode 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

815 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.8 Enhanced Quadrature Encoder Pulse (eQEP)**_ 

The enhanced quadrature encoder pulse (eQEP) module is used for direct interface with a linear or rotary incremental encoder to get position, direction, and speed information from a rotating machine for use in a high-performance motion and position-control system. 

**7.5.8.1 Introduction** ..................................................................................................................................................817 **7.5.8.2 Configuring Device Pins** .............................................................................................................................819 **7.5.8.3 EQEP Integration** .........................................................................................................................................820 **7.5.8.4 Description** ...................................................................................................................................................821 **7.5.8.5 Quadrature Decoder Unit (QDU)** ................................................................................................................ 826 **7.5.8.6 Position Counter and Control Unit (PCCU)** ...............................................................................................829 **7.5.8.7 eQEP Edge Capture Unit** ............................................................................................................................ 837 **7.5.8.8 eQEP Watchdog** ...........................................................................................................................................841 **7.5.8.9 eQEP Unit Timer Base** .................................................................................................................................841 **7.5.8.10 QMA Module** ...............................................................................................................................................842 **7.5.8.11 eQEP Interrupt Structure** .......................................................................................................................... 845 **7.5.8.12 EQEP Programming Guide** .......................................................................................................................845 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

816 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.8.1 Introduction** 

An incremental encoder disk is patterned with a track of slots along the periphery, as shown in Figure 7-324. These slots create an alternating pattern of dark and light lines. The disk count is defined as the number of dark and light line pairs that occur per revolution (lines per revolution). As a rule, a second track is added to generate a signal that occurs once per revolution (index signal: QEPI), which can be used to indicate an absolute position. Encoder manufacturers identify the index pulse using different terms such as index, marker, home position, and zero reference 

**==> picture [200 x 109] intentionally omitted <==**

**----- Start of picture text -----**<br>
QEPA<br>QEPB<br>QEPI<br>**----- End of picture text -----**<br>


**Figure 7-324. Optical Encoder Disk** 

To derive direction information, the lines on the disk are read out by two different photo-elements that "look" at the disk pattern with a mechanical shift of 1/4 the pitch of a line pair between them. This shift is detected with a reticle or mask that restricts the view of the photo-element to the desired part of the disk lines. As the disk rotates, the two photo-elements generate signals that are shifted 90° out of phase from each other. These are commonly called the quadrature QEPA and QEPB signals. The clockwise direction for most encoders is defined as the QEPA channel going positive before the QEPB channel and conversely, as shown in Figure 7-325. 

**==> picture [455 x 228] intentionally omitted <==**

**----- Start of picture text -----**<br>
T0 Clockwise shaft rotation/forward movement<br>0 1 2 3 4 5 6 7 N−6 N−5 N−4 N−3 N−2 N−1 0<br>QEPA<br>QEPB<br>QEPI<br>T0 Anti-clockwise shaft rotation/reverse movement<br>0 N−1 N−2 N−3 N−4 N−5 N−6 N−7 6 5 4 3 2 1 0 N−1 N−2<br>QEPA<br>QEPB<br>QEPI<br>Legend: N = lines per revolution<br>**----- End of picture text -----**<br>


**Figure 7-325. QEP Encoder Output Signal for Forward/Reverse Movement** 

The encoder wheel typically makes one revolution for every revolution of the motor, or the wheel can be at a geared rotation ratio with respect to the motor. Therefore, the frequency of the digital signal coming from the QEPA and QEPB outputs varies proportionally with the velocity of the motor. For example, a 2000-line encoder 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 817 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

directly coupled to a motor running at 5000 revolutions-per-minute (rpm) results in a frequency of 166.6kHz, so by measuring the frequency of either the QEPA or QEPB output, the processor can determine the velocity of the motor. 

Quadrature encoders from different manufacturers come with two forms of index pulse (gated index pulse or ungated index pulse) as shown in Figure 7-326. A nonstandard form of index pulse is ungated. In the ungated configuration, the index edges are not necessarily coincident with A and B signals. The gated index pulse is aligned to any of the four quadrature edges and width of the index pulse and can be equal to a quarter, half, or full period of the quadrature signal. 

**==> picture [437 x 210] intentionally omitted <==**

**----- Start of picture text -----**<br>
T0<br>QEPA<br>QEPB<br>0.25T0 ±0.1T0<br>QEPI<br>(gated to<br>A and B)<br>0.5T0 ±0.1T0<br>QEPI<br>(gated to A)<br>T0 ±0.5T0<br>QEPI<br>(ungated)<br>**----- End of picture text -----**<br>


**Figure 7-326. Index Pulse Example** 

Some typical applications of shaft encoders include robotics and computer input in the form of a mouse. Inside your mouse you can see where the mouse ball spins a pair of axles (a left/right, and an up/down axle). These axles are connected to optical shaft encoders that effectively tell the computer how fast and in what direction the mouse is moving. 

**General Issues:** Estimating velocity from a digital position sensor is a cost-effective strategy in motor control. Two different first order approximations for velocity can be written as: 

**==> picture [463 x 61] intentionally omitted <==**

where: 

- v(k) = Velocity at time instant k 

- x(k) = Position at time instant k 

- x(k-1) = Position at time instant k-1 

- T = Fixed unit time or inverse of velocity calculation rate 

- ΔX = Incremental position movement in unit time 

- t(k) = Time instant "k" 

- t(k-1) = Time instant "k-1" 

- X = Fixed unit position 

- ΔT = Incremental time elapsed for unit position movement 

818 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

Equation 13 is the conventional approach to velocity estimation and requires a time base to provide a unit time event for velocity calculation. Unit time is basically the inverse of the velocity calculation rate. 

The encoder count (position) is read once during each unit time event. The quantity [x(k) - x(k-1)] is formed by subtracting the previous reading from the current reading. Then the velocity estimate is computed by multiplying by the known constant 1/T (where T is the constant time between unit time events and is known in advance). 

Estimation based on Equation 13 has an inherent accuracy limit directly related to the resolution of the position sensor and the unit time period T. For example, consider a 500 line-per-revolution quadrature encoder with a velocity calculation rate of 400Hz. When used for position, the quadrature encoder gives a four-fold increase in resolution; in this case, 2000 counts-per-revolution. The minimum rotation that can be detected is, therefore, 0.0005 revolutions, which gives a velocity resolution of 12rpm when sampled at 400Hz. While this resolution can be satisfactory at moderate or high speeds, for example 1% error at 1200rpm, this resolution clearly proves inadequate at low speeds. In fact, at speeds below 12rpm, the speed estimate is erroneously zero much of the time. 

At low speed, Equation 14 provides a more accurate approach. It requires a position sensor that outputs a fixed interval pulse train, such as the aforementioned quadrature encoder. The width of each pulse is defined by motor speed for a given sensor resolution. Equation 14 can be used to calculate motor speed by measuring the elapsed time between successive quadrature pulse edges. However, this method suffers from the opposite limitation, as does Equation 13. A combination of relatively large motor speeds and high sensor resolution makes the time interval ΔT small, and thus more greatly influenced by the timer resolution. This can introduce considerable error into high-speed estimates. 

For systems with a large speed range (that is, speed estimation is needed at both low and high speeds), one approach is to use Equation 14 at low speed and have the DSP software switch over to Equation 13 when the motor speed rises above some specified threshold. 

## **7.5.8.2 Configuring Device Pins** 

The GPIO mux registers must be configured to connect this peripheral to the device pins. 

For proper operation of the eQEP module, input GPIO pins must be configured using the GPIO MUX registers. See the GPIO chapter starting at Section 13.1.1 for more details on GPIO MUX settings. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

819 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.8.3 EQEP Integration** 

There are 3x EQEP modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [500 x 436] intentionally omitted <==**

**Figure 7-327. EQEP Integration Diagram** 

820 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.8.4 Description** 

This section provides the eQEP inputs, memory map, and functional description. 

## _**7.5.8.4.1 EQEP Inputs**_ 

The eQEP inputs include two pins for quadrature-clock mode or direction-count mode, an index (or 0 marker), and a strobe input. The eQEP module requires that the QEPA, QEPB, and QEPI inputs are synchronized to SYSCLK prior to entering the module. The application code can enable the synchronous GPIO input feature on any eQEP-enabled GPIO pins. 

- **QEPA/XCLK and QEPB/XDIR** 

These two pins can be used in quadrature-clock mode or direction-count mode. 

- Quadrature-clock Mode 

The eQEP encoders provide two square wave signals (A and B) 90 electrical degrees out of phase. This phase relationship is used to determine the direction of rotation of the input shaft and number of eQEP pulses from the index position to derive the relative position information. For forward or clockwise rotation, QEPA signal leads QEPB signal and conversely. The quadrature decoder uses these two inputs to generate quadrature-clock and direction signals. 

- Direction-count Mode 

In direction-count mode, direction and clock signals are provided directly from the external source. Some position encoders have this type of output instead of quadrature output. The QEPA pin provides the clock input and the QEPB pin provides the direction input. 

- **QEPI: Index or Zero Marker** 

The eQEP encoder uses an index signal to assign an absolute start position from which position information is incrementally encoded using quadrature pulses. This pin is connected to the index output of the eQEP encoder to optionally reset the position counter for each revolution. This signal can be used to initialize or latch the position counter on the occurrence of a desired event on the index pin. 

- **QEPS: Strobe Input** 

This general-purpose strobe signal can initialize or latch the position counter on the occurrence of a desired event on the strobe pin. This signal is typically connected to a sensor or limit switch to notify that the motor has reached a defined position. 

Input signals to the eQEP (QEPA, QEPB, QEPI and QEPS) can come from multiple sources; that is, device pin, CMPSSx, or PWMXBARx. One typical use case is if SinCos transducers are used in the motor control system to estimate the position of motor shaft and Index signal is coming from traditional rotary encoder, source of the eQEP signals (QEPA, QEPB and QEPI) can be configured as output of CMPSSx which decodes the Sin, Cos and Index signals. Figure 7-328 illustrates the use case. 

Selection of the source of Input signals (QEPA, QEPB, and QEPI) is user-configurable through the QEPSRCSEL register as shown in eQEP Input Source Select Table. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

821 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [400 x 436] intentionally omitted <==**

**Figure 7-328. Using eQEP to Decode Signals from SinCos Transducer** 

822 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-171. eQEP Input Source Select Table** 

|**QEPSRCSEL.**<br>**QEPASEL**|**Source for QEPA**|**QEPSRCSEL.**<br>**QEPBSEL**|**Source for QEPB**|
|---|---|---|---|
|0|Tie-low|0|Tie-low|
|1|EQEP_A_PAD|1|EQEP_B_PAD|
|2|PWMXBAR.OUT0|2|PWMXBAR.OUT0|
|3|PWMXBAR.OUT1|3|PWMXBAR.OUT1|
|4|PWMXBAR.OUT2|4|PWMXBAR.OUT2|
|5|PWMXBAR.OUT3|5|PWMXBAR.OUT3|
|6|PWMXBAR.OUT4|6|PWMXBAR.OUT4|
|7|PWMXBAR.OUT5|7|PWMXBAR.OUT5|
|8|PWMXBAR.OUT6|8|PWMXBAR.OUT6|
|9|PWMXBAR.OUT7|9|PWMXBAR.OUT7|
|10|PWMXBAR.OUT8|10|PWMXBAR.OUT8|
|11|PWMXBAR.OUT9|11|PWMXBAR.OUT9|
|12|PWMXBAR.OUT10|12|PWMXBAR.OUT10|
|13|PWMXBAR.OUT11|13|PWMXBAR.OUT11|
|14|PWMXBAR.OUT12|14|PWMXBAR.OUT12|
|15|PWMXBAR.OUT13|15|PWMXBAR.OUT13|
|16|PWMXBAR.OUT14|16|PWMXBAR.OUT14|
|17|PWMXBAR.OUT15|17|PWMXBAR.OUT15|
|18|PWMXBAR.OUT16|18|PWMXBAR.OUT16|
|19|PWMXBAR.OUT7|19|PWMXBAR.OUT7|
|20|PWMXBAR.OUT18|20|PWMXBAR.OUT18|
|21|PWMXBAR.OUT19|21|PWMXBAR.OUT19|
|22|PWMXBAR.OUT20|22|PWMXBAR.OUT20|
|23|PWMXBAR.OUT21|23|PWMXBAR.OUT21|
|24|PWMXBAR.OUT22|24|PWMXBAR.OUT22|
|25|PWMXBAR.OUT23|25|PWMXBAR.OUT23|
|26|PWMXBAR.OUT24|26|PWMXBAR.OUT24|
|27|PWMXBAR.OUT25|27|PWMXBAR.OUT25|
|28|PWMXBAR.OUT26|28|PWMXBAR.OUT26|
|29|PWMXBAR.OUT27|29|PWMXBAR.OUT27|
|30|PWMXBAR.OUT28|30|PWMXBAR.OUT28|
|31|PWMXBAR.OUT29|31|PWMXBAR.OUT29|



## **Note** 

Configuration of QEPSRCSEL register to select the source of QEPA, QEPB, and QEPI signals can lead to unexpected transition on these signals, which can cause an undesirable outcome if eQEP is already running. Please make sure eQEP is disabled before configuring the QEPSRCSEL register for input signals. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 823 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.8.4.2 Functional Description**_ 

The eQEP peripheral contains the following major functional units (as shown in Figure 7-329): 

- Programmable input qualification for each pin (part of the GPIO MUX) 

- Quadrature Decoder Unit (QDU) 

- Position Counter and Control Unit (PCCU) for position measurement 

- Quadrature edge-capture (QCAP) unit for low-speed measurement 

- Unit time(UTIME) base for speed/frequency measurement 

- Watchdog timer for detecting stalls (QWDOG) 

**==> picture [456 x 341] intentionally omitted <==**

**Figure 7-329. Functional Block Diagram of the eQEP Peripheral** 

824 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.8.4.3 eQEP Memory Map**_ 

EQEP Memory Map Summary lists the registers with the memory locations, sizes, and reset values. 

**Table 7-172. EQEP Memory Map Summary** 

|**Register Name**|**Offset**|**Size (Bits)**|**Reset**|**Register Description**|
|---|---|---|---|---|
|QPOSCNT|0x00|32|0x00|eQEP Position Counter|
|QPOSINIT|0x04|32|0x00|eQEP Position Counter Init|
|QPOSMAX|0x08|32|0x00|eQEP Maximum Position Count|
|QPOSCMP|0x0C|32|0x00|eQEP Position Compare|
|QPOSILAT|0x10|32|0x00|eQEP Index Position Latch|
|QPOSSLAT|0x14|32|0x00|eQEP Strobe Position Latch|
|QPOSLAT|0x18|32|0x00|eQEP Position Latch|
|QUTMR|0x1C|32|0x00|eQEP Unit Timer|
|QUPRD|0x20|32|0x00|eQEP Unit Period|
|QWDTMR|0x24|16|0x00|eQEP Watchdog Timer|
|QWDPRD|0x26|16|0x00|eQEP Watchdog Period|
|QDECCTL|0x28|16|0x00|Quadrature Decoder Control|
|QEPCTL|0x2A|16|0x00|eQEP Control|
|QCAPCTL|0x2C|16|0x00|Quadrature Capture Control|
|QPOSCTL|0x2E|16|0x00|Position Compare Control|
|QEINT|0x30|16|0x00|eQEP Interrupt Control|
|QFLG|0x32|16|0x00|eQEP Interrupt Flag|
|QCLR|0x34|16|0x00|eQEP Interrupt Clear|
|QFRC|0x36|16|0x00|eQEP Interrupt Force|
|QEPSTS|0x38|16|0x80|eQEP Status|
|QCTMR|0x3A|16|0x00|eQEP Capture Timer|
|QCPRD|0x3C|16|0x00|eQEP Capture Period|
|QCTMRLAT|0x3E|16|0x00|eQEP Capture Latch|
|QCPRDLAT|0x40|16|0x00|eQEP Capture Period Latch|
|REV|0x60|32|0x11|eQEP Revision Number|
|QEPSTROBESEL|0x64|32|0x00|eQEP Strobe Select Register (NOTE: This feature is not applicable<br>for AM26x devices)|
|QMACTRL|0x68|32|0x00|QMA Control Register|
|QEPSRCSEL|0x6C|32|0x00|eQEP Source Select Register|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

825 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.8.5 Quadrature Decoder Unit (QDU)** 

Figure 7-330 shows a functional block diagram of the QDU. 

**==> picture [432 x 485] intentionally omitted <==**

**----- Start of picture text -----**<br>
�������� ���������� ������������ �����������<br>PHE EQEPxAIN<br>0<br>EQEPA<br>iCLK QA 0<br>00<br>xCLK 1<br>QCLK 01<br>xCLK 1<br>10 xCLK Quadrature EQEPxBIN<br>11 decoder 0<br>EQEPB<br>QB 0<br>iDIR 1<br>00<br>xDIR 1<br>QDIR 01<br>10 1 �����������<br>11<br>0<br>x1<br>x2<br>2 x1, x2<br>������������ ����������� �����������<br>EQEPxIIN<br>0<br>0<br>QI<br>1<br>1<br>QDECCTL:IGATE EQEPxSIN<br>0<br>QS<br>1<br>QDECCTL:SPSEL �����������<br>���������<br>������ 0<br>���������<br>1<br>QDECCTL:SPSEL<br>EQEPxIOE<br>0<br>QDECCTL:SOEN<br>EQEPxSOE<br>1<br>**----- End of picture text -----**<br>


**Figure 7-330. Functional Block Diagram of Decoder Unit** 

## _**7.5.8.5.1 Position Counter Input Modes**_ 

Clock and direction input to the position counter is selected using QDECCTL[QSRC] bits, based on interface input requirement as follows: 

- Quadrature-count mode 

- Direction-count mode 

- UP-count mode 

- DOWN-count mode 

826 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.8.5.1.1 Quadrature Count Mode**_ 

The quadrature decoder generates the direction and clock to the position counter in quadrature count mode. 

- **Direction** The direction decoding logic of the eQEP circuit determines which one of the sequences **Decoding** (QEPA, QEPB) is the leading sequence and accordingly updates the direction information in the QEPSTS[QDF] bit. Table 7-173 and Figure 7-331 show the direction decoding logic in truth table and state machine form. Both edges of the QEPA and QEPB signals are sensed to generate count pulses for the position counter. Therefore, the frequency of the clock generated by the eQEP logic is four times that of each input sequence. Figure 7-332 shows the direction decoding and clock generation from the eQEP input signals. 

**Table 7-173. Quadrature Decoder Truth Table** 

|**Previous Edge**|**Present Edge**|**QDIR**|**QPOSCNT**|
|---|---|---|---|
|QA↑|QB↑<br>QB↓<br>QA↓|UP<br>DOWN<br>TOGGLE|Increment<br>Decrement<br>Increment or Decrement|
|QA↓|QB↓<br>QB↑<br>QA↑|UP<br>DOWN<br>TOGGLE|Increment<br>Decrement<br>Increment or Decrement|
|QB↑|QA↑<br>QA↓<br>QB↓|DOWN<br>UP<br>TOGGLE|Decrement<br>Increment<br>Increment or Decrement|
|QB↓|QA↓<br>QA↑<br>QB↑|DOWN<br>UP<br>TOGGLE|Decrement<br>Increment<br>Increment or Decrement|



**==> picture [431 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
Increment Increment<br>counter counter<br>(00) (11)<br>(A,B)= 10<br>(10) (01)<br>Decrement Decrement<br>QEPA counter counter<br>00 11<br>QEPB Decrement Decrement<br>counter counter<br>01<br>eQEP signals<br>Increment Increment<br>counter counter<br>**----- End of picture text -----**<br>


**Figure 7-331. Quadrature Decoder State Machine** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

827 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [443 x 324] intentionally omitted <==**

**----- Start of picture text -----**<br>
QA<br>QB<br>QCLK<br>QDIR<br>QPOSCNT +1 +1 +1 +1 +1 +1 +1 −1 −1 −1 −1 −1 −1 −1 −1 −1 −1 −1 +1 +1 +1<br>QA<br>QB<br>QCLK<br>QDIR<br>QPOSCNT −1 −1 −1 −1 −1 −1 −1 +1 +1 +1 +1 +1 +1 +1 +1 +1 +1 +1 −1 −1 −1<br>**----- End of picture text -----**<br>


**Figure 7-332. Quadrature-clock and Direction Decoding** 

**Phase Error Flag** In normal operating conditions, quadrature inputs QEPA and QEPB is 90 degrees out of phase. The phase error flag (PHE) is set in the QFLG register and the QPOSCNT value can be incorrect and offset by multiples of 1 or 3. That is, when edge transition is detected simultaneously on the QEPA and QEPB signals to optionally generate interrupts. State transitions marked by dashed lines in Figure 7-331 are invalid transitions that generate a phase error. 

**Count** The eQEP position counter provides 4x times the resolution of an input clock by generating **Multiplication** a quadrature-clock (QCLK) on the rising/falling edges of both eQEP input clocks (QEPA and QEPB) as shown in Figure 7-332. 

**Reverse Count** In normal quadrature count operation, QEPA input is applied to the QA input of the quadrature decoder and the QEPB input is applied to the QB input of the quadrature decoder. Reverse counting is enabled by setting the SWAP bit in the QDECCTL register. This swaps the input to the quadrature decoder; thereby, reversing the counting direction. 

## _**7.5.8.5.1.2 Direction-Count Mode**_ 

Some position encoders provide direction and clock outputs, instead of quadrature outputs. In such cases, direction-count mode can be used. The QEPA input provides the clock for the position counter and the QEPB input has the direction information. The position counter is incremented on every rising edge of a QEPA input when the direction input is high, and decremented when the direction input is low. 

828 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.8.5.1.3 Up-Count Mode**_ 

The counter direction signal is hard-wired for up-count and the position counter is used to measure the frequency of the QEPA input. Clearing the QDECCTL[XCR] bit enables clock generation to the position counter on both edges of the QEPA input; thereby, increasing the measurement resolution by a factor of 2x. In up-count mode, we recommend that the application not configure QEPB as a GPIO mux option, or make sure that a signal edge is not generated on the QEPB input. 

## _**7.5.8.5.1.4 Down-Count Mode**_ 

The counter direction signal is hardwired for a down-count and the position counter is used to measure the frequency of the QEPA input. Clearing the QDECCTL[XCR] bit enables clock generation to the position counter on both edges of a QEPA input, thereby increasing the measurement resolution by a factor of 2x. In down-count mode, the application must not configure QEPB as a GPIO mux option or make sure that a signal edge is not generated on the QEPB input. 

## _**7.5.8.5.2 eQEP Input Polarity Selection**_ 

Each eQEP input can be inverted using QDECCTL[8:5] control bits. As an example, setting the QDECCTL[QIP] bit inverts the index input. 

## _**7.5.8.5.3 Position-Compare Sync Output**_ 

The enhanced eQEP peripheral includes a position-compare unit that is used to generate the position-compare sync signal on compare match between the position-counter register (QPOSCNT) and the position- compare register (QPOSCMP). This sync signal can be output using an index pin or strobe pin of the EQEP peripheral. 

Setting the QDECCTL[SOEN] bit enables the position-compare sync output and the QDECCTL[SPSEL] bit selects either an eQEP index pin or an eQEP strobe pin. 

## **7.5.8.6 Position Counter and Control Unit (PCCU)** 

The position-counter and control unit provides two configuration registers (QEPCTL and QPOSCTL) for setting up position-counter operational modes, position-counter initialization/latch modes and position-compare logic for sync signal generation. 

## _**7.5.8.6.1 Position Counter Operating Modes**_ 

Position-counter data can be captured in different manners. In some systems, the position counter is accumulated continuously for multiple revolutions and the position-counter value provides the position information with respect to the known reference. An example of this is the quadrature encoder mounted on the motor controlling the print head in the printer. Here the position counter is reset by moving the print head to the home position and then the position counter provides absolute position information with respect to home position. 

In other systems, the position counter is reset on every revolution using index pulse, and the position counter provides a rotor angle with respect to the index pulse position. 

The position counter can be configured to operate in following four modes 

- Position-Counter Reset on Index Event 

- Position-Counter Reset on Maximum Position 

- Position-Counter Reset on the first Index Event 

- Position-Counter Reset on Unit Time Out Event (Frequency Measurement) 

In all the above operating modes, the position counter is reset to 0 on overflow and to the QPOSMAX register value on underflow. Overflow occurs when the position counter counts up after the QPOSMAX value. Underflow occurs when the position counter counts down after 0. The Interrupt flag is set to indicate overflow/underflow in QFLG register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 829 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.8.6.1.1 Position Counter Reset on Index Event (QEPCTL[PCRM] = 00)**_ 

If the index event occurs during the forward movement, then the position counter is reset to 0 on the next eQEP clock. If the index event occurs during the reverse movement, then the position counter is reset to the value in the QPOSMAX register on the next eQEP clock. 

The first index marker is defined as the quadrature edge following the first index edge. The eQEP peripheral records the occurrence of the first index marker (QEPSTS[FIMF]) and direction on the first index event marker (QEPSTS[FIDF]) in QEPSTS registers, the eQEP peripheral also remembers the quadrature edge on the first index marker so that same relative quadrature transition is used for index event reset operation. 

For example, if the first reset operation occurs on the falling edge of QEPB during the forward direction, then all the subsequent reset must be aligned with the falling edge of QEPB for the forward rotation and on the rising edge of QEPB for the reverse rotation as shown in Figure 7-333. 

The position-counter value is latched to the QPOSILAT register and direction information is recorded in the QEPSTS[QDLF] bit on every index event marker. The position-counter error flag (QEPSTS[PCEF]) and error interrupt flag (QFLG[PCE]) are set if the latched value is not equal to 0 or QPOSMAX. The position-counter error flag (QEPSTS[PCEF]) is updated on every index event marker and an interrupt flag (QFLG[PCE]) is set on error that can be cleared only through software. 

The index event latch configuration QEPCTL[IEL] must be configured to 00 or 11 when pcrm = 0 and the position counter error flag/interrupt flag are generated only in index event reset mode. The position counter value is latched into the IPOSLAT register on every index marker. 

**==> picture [410 x 252] intentionally omitted <==**

**Figure 7-333. Position Counter Reset by Index Pulse for 1000-Line Encoder (QPOSMAX = 3999 or 0xF9F)** 

## **Note** 

In case of a boundary condition where the time period between the Index Event and the previous QCLK edge is less than SYSCLK period, then QPOSCNT gets reset to zero or QPOSMAX in the same SYSCLK cycle and does not wait for the next QCLK edge to occur. 

830 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.8.6.1.2 Position Counter Reset on Maximum Position (QEPCTL[PCRM] = 01)**_ 

If the position counter is equal to QPOSMAX, then the position counter is reset to 0 on the next eQEP clock for forward movement and position counter overflow flag is set. If the position counter is equal to ZERO, then the position counter is reset to QPOSMAX on the next QEP clock for reverse movement and position-counter underflow flag is set. Figure 7-334 shows the position-counter reset operation in this mode. 

The first index marker fields (QEPSTS[FIDF] and QEPSTS[FIMF]) are not applicable in this mode. 

**==> picture [445 x 395] intentionally omitted <==**

**----- Start of picture text -----**<br>
QA<br>QB<br>QCLK<br>QDIR<br>QPOSCNT 1 2 3 4 0 1 2 1 0 4 3 2 1 0 4 3 2 1 2 3 4 0<br>OV/UF<br>QA<br>QB<br>QCLK<br>QDIR<br>QPOSCNT 1 0 4 3 2 1 0 1 2 3 4 0 1 2 3 4 0 1 0 4 3<br>OV/UF<br>**----- End of picture text -----**<br>


**Figure 7-334. Position Counter Underflow/Overflow (QPOSMAX = 4)** 

## _**7.5.8.6.1.3 Position Counter Reset on the First Index Event (QEPCTL[PCRM] = 10)**_ 

If the index event occurs during forward movement, then the position counter is reset to 0 on the next eQEP clock. If the index event occurs during the reverse movement, then the position counter is reset to the value in the QPOSMAX register on the next eQEP clock. Note that this is done only on the first occurrence and subsequently the position-counter value is not reset on an index event; rather, the position-counter value is reset based on the maximum position as described in Section 7.5.8.6.1.2. 

The first index marker fields (QEPSTS[FIDF] and QEPSTS[FIMF]) are not applicable in this mode. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 831 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.8.6.1.4 Position Counter Reset on Unit Time-out Event (QEPCTL[PCRM] = 11)**_ 

In this mode, QPOSCNT is set to 0 or QPOMAX, depending on the direction mode selected by QDECCTL[QSRC] bits on a unit time event. This is useful for frequency measurement. 

## _**7.5.8.6.2 Position Counter Latch**_ 

The eQEP index and strobe input can be configured to latch the position counter (QPOSCNT) into QPOSILAT and QPOSSLAT, respectively, on occurrence of a definite event on these pins. 

## _**7.5.8.6.2.1 Index Event Latch**_ 

In some applications, it is not desirable to reset the position counter on every index event and instead it can be required to operate the position counter in full 32-bit mode (QEPCTL[PCRM] = 01 and QEPCTL[PCRM] = 10 modes). 

In such cases, the eQEP position counter can be configured to latch on the following events and direction information is recorded in the QEPSTS[QDLF] bit on every index event marker. 

- Latch on Rising edge (QEPCTL[IEL] = 01) 

- Latch on Falling edge (QEPCTL[IEL] = 10) 

- Latch on Index Event Marker (QEPCTL[IEL] = 11) 

This is particularly useful as an error checking mechanism to check if the position counter accumulated the correct number of counts between index events. As an example, the 1000-line encoder must count 4000 times when moving in the same direction between the index events. 

The index event latch interrupt flag (QFLG[IEL]) is set when the position counter is latched to the QPOSILAT register. The index event latch configuration bits (QEPCTL[IEL]) are ignored when QEPCTL[PCRM] = 00. 

**Latch on Rising Edge** The position-counter value (QPOSCNT) is latched to the QPOSILAT register **(QEPCTL[IEL] = 01)** on every rising edge of an index input. **Latch on Falling Edge** The position-counter value (QPOSCNT) is latched to the QPOSILAT register **(QEPCTL[IEL] = 10)** on every falling edge of index input. **Latch on Index Event** The first index marker is defined as the quadrature edge following the **Marker/Software Index Marker** first index edge. The eQEP peripheral records the occurrence of the first **(QEPCTL[IEL] = 11** index marker (QEPSTS[FIMF]) and the direction on the first index event marker (QEPSTS[FIDF]) in the QEPSTS registers. The eQEP peripheral also remembers the quadrature edge on the first index marker so that the same relative quadrature transition is used for latching the position counter (QEPCTL[IEL] = 11). 

Figure 7-335 shows the position counter latch using an index event marker. 

832 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [412 x 252] intentionally omitted <==**

**Figure 7-335. Software Index Marker for 1000-line Encoder (QEPCTL[IEL] = 1)** 

## _**7.5.8.6.2.2 Strobe Event Latch**_ 

The position-counter value is latched to the QPOSSLAT register on the rising edge of the strobe input by clearing the QEPCTL[SEL] bit. 

If the QEPCTL[SEL] bit is set, then the position-counter value is latched to the QPOSSLAT register on the rising edge of the strobe input for forward direction, and on the falling edge of the strobe input for reverse direction as shown in Figure 7-336. 

The strobe event latch interrupt flag (QFLG[SEL) is set when the position counter is latched to the QPOSSLAT register. 

**==> picture [435 x 216] intentionally omitted <==**

**----- Start of picture text -----**<br>
QA<br>QB<br>QS<br>QCLK<br>QEPST:QDF<br>F9D F9F FA1 FA3 FA4 FA2 FA0 F9E F9C F9A F98<br>QPOSCNT F9C FA5 F97<br>F9E FA0 FA2 FA4 FA3 FA1 F9F F9D F9B F99<br>QIPOSSLAT F9F F9F<br>**----- End of picture text -----**<br>


**Figure 7-336. Strobe Event Latch (QEPCTL[SEL] = 1)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 833 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.8.6.3 Position Counter Initialization**_ 

The position counter can be initialized using the following events: 

- Index event 

- Strobe event 

- Software initialization 

**Index Event** The QEPI index input can be used to trigger the initialization of the position counter at the **Initialization** rising or falling edge of the index input. If the QEPCTL[IEI] bits are 10, then the position **(IEI)** counter (QPOSCNT) is initialized with a value in the QPOSINIT register on the rising edge of index input. Conversely, if the QEPCTL[IEI] bits are 11, initialization is on the falling edge of the index input. 

**Strobe Event** If the QEPCTL[SEI] bits are 10, then the position counter is initialized with a value in the **Initialization** QPOSINIT register on the rising edge of strobe input. **(SEI)** If QEPCTL[SEL] bits are 11, then the position counter is initialized with a value in the QPOSINIT register on the rising edge of strobe input for forward direction and on the falling edge of strobe input for reverse direction. 

|**Initialization**<br>**(SEI)**|QPOSINIT register on the rising edge of strobe input.<br>If QEPCTL[SEL] bits are 11, then the position counter is initialized with a value in the<br>QPOSINIT register on the rising edge of strobe input for forward direction and on the falling<br>edge of strobe input for reverse direction.|
|---|---|
|**Software**|The position counter can be initialized in software by writing a 1 to the QEPCTL[SWI] bit.|
|**Initialization**|This bit is not automatically cleared. While the bit is still set, if a 1 is written to the bit again,|
|**(SWI)**|the position counter is re-initialized.|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

834 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.8.6.4 eQEP Position-compare Unit**_ 

The eQEP peripheral includes a position-compare unit that is used to generate a sync output and interrupt on a position-compare match. Figure 7-337 shows a diagram. The position-compare (QPOSCMP) register is shadowed and shadow mode can be enabled or disabled using the QPOSCTL[PSSHDW] bit. If the shadow mode is not enabled, the CPU writes directly to the active position compare register. 

**==> picture [414 x 193] intentionally omitted <==**

**----- Start of picture text -----**<br>
QPOSCTL:PCSHDW<br>QPOSCTL:PCLOAD<br>QPOSCMP QFLG:PCR<br>QFLG:PCM QPOSCTL:PCSPW QPOSCTL:PCPOL<br>12<br>32<br>PCEVENT Pulse<br>0<br>stretcher PCSOUT<br>32<br>1<br>QPOSCNT<br>**----- End of picture text -----**<br>


**Figure 7-337. eQEP Position-compare Unit** 

In shadow mode, you can configure the position-compare unit (QPOSCTL[PCLOAD]) to load the shadow register value into the active register on the following events, and to generate the position-compare ready (QFLG[PCR]) interrupt after loading. 

- Load on compare match 

- Load on position-counter zero event 

The position-compare match (QFLG[PCM]) is set when the position-counter value (QPOSCNT) matches with the active position-compare register (QPOSCMP) and the position-compare sync output of the programmable pulse width is generated on compare-match to trigger an external device. 

For example, if QPOSCMP = 2, the position-compare unit generates a position-compare event on 1 to 2 transitions of the eQEP position counter for forward counting direction and on 3 to 2 transitions of the eQEP position counter for reverse counting direction (see Figure 7-338). 

See the register section for the layout of the eQEP Position-Compare Control Register (QPOSCTL) and description of the QPOSCTL bit fields. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

835 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [398 x 196] intentionally omitted <==**

**----- Start of picture text -----**<br>
4 4<br>3 3 3 3<br>2 2 2 2<br>eQEP counter POSCMP=2<br>1 1 1 1<br>0 0 0<br>PCEVNT<br>PCSOUT (active HIGH)<br>PCSPW<br>PCSOUT (active LOW)<br>**----- End of picture text -----**<br>


**Figure 7-338. eQEP Position-compare Event Generation Points** 

The pulse stretcher logic in the position-compare unit generates a programmable position-compare sync pulse output on the position-compare match. In the event of a new position-compare match while a previous positioncompare pulse is still active, then the pulse stretcher generates a pulse of specified duration from the new position-compare event as shown in Figure 7-339. 

**==> picture [371 x 242] intentionally omitted <==**

**----- Start of picture text -----**<br>
DIR<br>QPOSCMP<br>QPOSCNT<br>PCEVNT<br>PCSPW<br>PCSPW<br>PCSPW<br>PCSOUT (active HIGH)<br>**----- End of picture text -----**<br>


**Figure 7-339. eQEP Position-compare Sync Output Pulse Stretcher** 

836 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.8.7 eQEP Edge Capture Unit** 

The eQEP peripheral includes an integrated edge capture unit to measure the elapsed time between the unit position events as shown in Figure 7-340. This feature is typically used for low-speed measurement using the following formula: 

**==> picture [463 x 25] intentionally omitted <==**

where: 

- X = Unit position is defined by integer multiple of quadrature edges (see Figure 7-341) 

- ΔT = Elapsed time between unit position events 

- v(k) = Velocity at time instant "k" 

The eQEP capture timer (QCTMR) runs from prescaled SYSCLKOUT and the prescaler is programmed by the QCAPCTL[CCPS] bits. The capture timer (QCTMR) value is latched into the capture period register (QCPRD) on every unit position event and then the capture timer is reset, a flag is set in QEPSTS:UPEVNT to indicate that new value is latched into the QCPRD register. Software can check this status flag before reading the period register for low speed measurement, and clear the flag by writing 1. 

Time measurement (ΔT) between unit position events is correct if the following conditions are met: 

- No more than 65,535 counts have occurred between unit position events. 

- No direction change between unit position events. 

If the QEP capture timer overflows between unit position events, then the timer sets the QEP capture overflow flag (QEPSTS[COEF]) in the status register. 

## **Note** 

The QCPRDLAT register is not set to 0xFFFF if the QEPSTS[COEF] bit gets set. 

If direction change occurs between the unit position events, then the direction error flag (QEPSTS[CDEF]) is set in the status register and the QCPRDLAT register is set to 0xFFFF. 

The Capture Timer (QCTMR) and Capture Period register (QCPRD) can be configured to latch on the following events: 

- CPU read of QPOSCNT register 

- Unit time-out event 

If the QEPCTL[QCLM] bit is cleared, then the capture timer and capture period values are latched into the QCTMRLAT and QCPRDLAT registers, respectively, when the CPU reads the position counter (QPOSCNT). 

If the QEPCTL[QCLM] bit is set, then the position counter, capture timer, and capture period values are latched into the QPOSLAT, QCTMRLAT and QCPRDLAT registers, respectively, on unit time out. 

Figure 7-342 shows the capture unit operation along with the position counter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 837 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [456 x 332] intentionally omitted <==**

**----- Start of picture text -----**<br>
16<br>0xFFFF<br>QEPSTS:COEF<br>16<br>QCTMR QCTMRLAT QCAPCTL:UPPS<br>QCAPCTL:CCPS QCPRD QCPRDLAT<br>3 16 16 QEPSTS:UPEVNT 4<br>SYSCLKOUT 3-bit binarydivider CAPCLK Capture timer UPEVNT 4-bit binarydivider QCLK<br>control unit<br>x1, 1/2, 1/4..., x1, 1/2, 1/4...,<br>(CTCU)<br>1/128 1/2048<br>QCAPCTL:CEN QEPSTS:CDEF Rising/falling QDIR<br>edge detect<br>UTIME<br>QEPCTL:UTE QFLG:UTO<br>SYSCLKOUT<br>QUTMR<br>UTOUT<br>QUPRD<br>**----- End of picture text -----**<br>


**Figure 7-340. eQEP Edge Capture Unit** 

## **CAUTION** 

The QCAPCTL[UPPS] prescaler cannot be modified dynamically (such as switching the unit event prescaler from QCLK/4 to QCLK/8). Doing so can result in undefined behavior. The QCAPCTL[CPPS] prescaler can be modified dynamically (such as switching CAPCLK prescaling mode from SYSCLK/4 to SYSCLK/8) only after the capture unit is disabled. 

838 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [413 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
P<br>QA<br>QB<br>QCLK<br>UPEVNT<br>X=N x P<br>**----- End of picture text -----**<br>


N = Number of quadrature periods selected using QCAPCTL[UPPS] bits 

**Figure 7-341. Unit Position Event for Low Speed Measurement (QCAPCTL[UPPS] = 0010)** 

**==> picture [455 x 339] intentionally omitted <==**

**----- Start of picture text -----**<br>
QEPA<br>QEPB<br>QCLK<br>QPOSCNT ∆X x(k)<br>x(k−1)<br>UPEVNT<br>t(k)<br>∆T<br>QCTMR<br>t(k−1)<br>T<br>UTOUT<br>Figure 7-342. eQEP Edge Capture Unit - Timing Details<br>**----- End of picture text -----**<br>


SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

839 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

Velocity calculation equation: 

**==> picture [152 x 22] intentionally omitted <==**

(16) 

where: 

- v(k) = Velocity at time instant k 

- x(k) = Position at time instant k 

- x(k-1) = Position at time instant k-1 

- T = Fixed unit time or inverse of velocity calculation rate 

- ΔX = Incremental position movement in unit time 

- X = Fixed unit position 

- ΔT = Incremental time elapsed for unit position movement 

- t(k) = Time instant "k" 

- t(k-1) = Time instant "k-1" 

Unit time (T) and unit period (X) are configured using the QUPRD and QCAPCTL[UPPS] registers. Incremental position output and incremental time output is available in the QPOSLAT and QCPRDLAT registers. 

|**Parameter**|**Relevant Register to Configure or Read the Information**|
|---|---|
|T|Unit Period Register (QUPRD)|
|ΔX|Incremental Position = QPOSLAT(k) - QPOSLAT(K-1)|
|X|Fixed-unit position defined by sensor resolution and QCAPCTL[UPPS] bits|
|ΔT|Capture Period Latch (QCPRDLAT)|



840 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.8.8 eQEP Watchdog** 

The eQEP peripheral contains a 16-bit watchdog timer (Figure 7-343) that monitors the quadrature clock to indicate proper operation of the motion-control system. The eQEP watchdog timer is clocked from SYSCLKOUT/64 and the quadrature clock event (pulse) resets the watchdog timer. If no quadrature clock event is detected until a period match (QWDPRD = QWDTMR), then the watchdog timer times out and the watchdog interrupt flag is set (QFLG[WTO]). The time-out value is programmable through the watchdog period register (QWDPRD). 

**==> picture [396 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
QWDOG<br>QEPCTL:WDE<br>SYSCLKOUT SYSCLKOUT<br>/64 QWDTMR<br>16<br>QCLK RESET WDTOUT<br>16<br>QWDPRD QFLG:WTO<br>**----- End of picture text -----**<br>


**Figure 7-343. eQEP Watchdog Timer** 

## **7.5.8.9 eQEP Unit Timer Base** 

The eQEP peripheral includes a 32-bit timer (QUTMR) that is clocked by SYSCLKOUT to generate periodic interrupts for velocity calculations, see Figure 7-344. Whenever the unit timer (QUTMR) matches the unit period register (QUPRD), the eQEP peripheral resets the unit timer (QUTMR) and also generates the unit time out interrupt flag (QFLG[UTO]). The unit timer gets reset whenever timer value equals to configured period value. 

The eQEP peripheral can be configured to latch the position counter, capture timer, and capture period values on a unit time out event so that latched values are used for velocity calculation as described in Section 7.5.8.7. 

**==> picture [404 x 165] intentionally omitted <==**

**----- Start of picture text -----**<br>
UTIME<br>QEPCTL:UTE<br>SYSCLKOUT<br>QUTMR<br>32<br>UTOUT<br>32<br>QUPRD QFLG:UTO<br>**----- End of picture text -----**<br>


**Figure 7-344. eQEP Unit Timer Base** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

841 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.8.10 QMA Module** 

The QEP Mode Adapter (QMA) is designed to extend the eQEP module capabilities to support the additional modes described. Figure 7-345 depicts how the QMA module is integrated into to the eQEP module. 

At reset, by default QMA logic is bypassed and the EQEPA and EQEPB inputs from the pins go directly into the eQEP module. When QMA module is enabled by configuring the QMACTRL[MODE] register, the EQEPA and EQEPB input are processed by this module and modified version of EQEPA and EQEPB signals are sent to the eQEP module. The QMA module requires the eQEP module to be configured in the Direction-Count mode and generates a clock signal on EQEPA input and direction signal on EQEPB input as needed for the proper operation of the intended mode. 

- The xCLKMOD block inside the QMA module looks at the transitions on external EQEPA and EQEPB signals to generate the clock signal on the EQEPA input to the eQEP module. 

- The xDIRMOD block inside the QMA module looks at the transitions on external EQEPA and EQEPB signals to generate the direction signal on the EQEPB input to the eQEP module. 

The QMA module has error detection logic to detect illegal transitions on EQEPA and EQEPB input signals. The QMA module’s error and interrupt are integrated inside the eQEP module as described in Section 7.5.8.11. In addition, the QMACTRL register configuration can be locked using the QMALOCK register. Refer to the register description for more details. 

**==> picture [500 x 218] intentionally omitted <==**

**----- Start of picture text -----**<br>
QEPA_Pin QEPB_Pin<br>QMA_error<br>EQEP TYPE2<br>A Error<br>B Detec � on Logic<br>A ! (1 or 2)<br>A B xCLKMOD Block xCLK_mod (1 or 2) QEPA<br>EQEPERR<br>QMACTRL.MODE ModuleEQEP (to Interrupt Controller)EQEPINTn<br>A xDIRMOD<br>B  Block xDIR_mod (1 or 2)<br>B ! (1 or 2) QEPB<br>QEP Mode Adapter<br>(QMA)<br>**----- End of picture text -----**<br>


**Figure 7-345. QMA Module Block Diagram** 

842 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.8.10.1 Modes of Operation**_ 

The QMA module can be operated in the following modes by configuring the QMACTRL register: 

- QMA Mode-1 (QMACTRL[MODE] = 1) 

- QMA Mode-2 (QMACTRL[MODE] = 2) 

## _**7.5.8.10.1.1 QMA Mode-1 (QMACTRL[MODE] = 1)**_ 

This mode is used when the default state of EQEPA and EQEPB inputs is high. In this mode, outputs of QMA correspond to the following as shown in Figure 7-346: 

- EQEPA Output of QMA is the AND of EQEPA and EQEPB inputs coming from the pin 

- EQEPB Output of QMA is the direction signal generated by QMA based on EQEPA and EQEPB inputs 

**==> picture [500 x 423] intentionally omitted <==**

**----- Start of picture text -----**<br>
E Q E P A<br>E Q E P B<br>E Q E P A<br>O u tp u t o f Q M A<br>E Q E P B<br>O u tp u t o f Q M A<br>Q P O S C N T<br>(in s id e  e Q E P )<br>**----- End of picture text -----**<br>


**Figure 7-346. QMA Mode-1** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

843 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.8.10.1.2 QMA Mode-2 (QMACTRL[MODE] = 2)**_ 

This mode is used when the default state of EQEPA and EQEPB inputs is low. In this mode, outputs of QMA correspond to the following as shown in Figure 7-347: 

- EQEPA Output of QMA is the OR of EQEPA and EQEPB inputs coming from the pin 

- EQEPB Output of QMA is the direction signal generated by QMA based on EQEPA and EQEPB inputs 

**==> picture [454 x 382] intentionally omitted <==**

**----- Start of picture text -----**<br>
E Q E P A<br>E Q E P<br>E Q E P A<br>O u tp u t o f Q M A<br>E Q E P B<br>O u tp u t o f Q M A<br>Q P O S C N T<br>(in s id e  e Q E P )<br>**----- End of picture text -----**<br>


**Figure 7-347. QMA Mode-2** 

## _**7.5.8.10.2 Interrupt and Error Generation**_ 

The error detection logic detects illegal transitions on EQEPA and EQEPB signals and generates an error signal. This error signal can be used to generate eQEP interrupt and error output. Refer to Section 7.5.8.11 for details. 

844 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.8.11 eQEP Interrupt Structure** 

Figure 7-348 shows how the interrupt mechanism works in the eQEP module. 

**==> picture [430 x 236] intentionally omitted <==**

**----- Start of picture text -----**<br>
QMAE<br>EQEPERROR<br>PHE<br>QEINT:QMAE<br>Clr QCLR:QMAE<br>Set Clr QCLR:INT Latch<br>QFRC:QMAE<br>Set<br>Latch QFLG:INT QFLG:QMAE QMAE<br>Other Interrupt Sources<br>EQEPxINT Pulse 0 0<br>generator<br>when<br>input=1 1 QEINT:PHE<br>Clr QCLR:PHE<br>Latch<br>QFRC:PHE<br>Set<br>QFLG:PHE PHE<br>QEINT:PCE<br>Clr QCLR:PCE<br>Latch<br>QFRC:PCE<br>Set<br>QFLG:PCE PCE<br>**----- End of picture text -----**<br>


**Figure 7-348. eQEP Interrupt Generation** 

Eleven interrupt events (PCE, PHE, QDC, WTO, PCU, PCO, PCR, PCM, SEL, IEL, and UTO) can be generated. The interrupt control register (QEINT) is used to enable/disable individual interrupt event sources. The interrupt flag register (QFLG) indicates if any interrupt event has been latched and contains the global interrupt flag bit (INT). 

An interrupt pulse is generated to VIM when: 

1. Interrupt is enabled for eQEP event inside QEINT register 

2. Interrupt flag for eQEP event inside QFLG register is set, and 

3. Global interrupt status flag bit QFLG[INT] had been cleared for previously generated interrupt event. The interrupt service routine needs to clear the global interrupt flag bit and the serviced event, by way of the interrupt clear register (QCLR), before any other interrupt pulses are generated. If either flags inside the QFLG register are not cleared, further interrupt events do not generate an interrupt to VIM. You can force an interrupt event by way of the interrupt force register (QFRC), which is useful for test purposes. 

## **7.5.8.12 EQEP Programming Guide** 

## **Driver Information** 

Driver features are available at the eQEP driver page 

## **Software API Information** 

The eQEP driver provides an API to configure the eQEP module. Full documentation is located on APIs for eQEP 

## **Example Usage** 

The below links show examples on how to use eQEP 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

845 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- eQEP Frequency Measurement 

- eQEP Position Speed 

846 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9 Fast Serial Interface (FSI)**_ 

This chapter contains a general description of the Fast Serial Interface (FSI) module. The FSI is a serial peripheral capable of reliable high-speed communication across isolation barriers. 

**7.5.9.1 Introduction** ..................................................................................................................................................848 **7.5.9.2 System-level Integration** .............................................................................................................................850 **7.5.9.3 FSI Functional Description** .........................................................................................................................857 **7.5.9.4 FSI Programming Guide** ............................................................................................................................. 883 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

847 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.9.1 Introduction** 

The Fast Serial Interface (FSI) module is a serial communication peripheral capable of reliable high-speed communication across isolation devices. Galvanic isolation devices are used in situations where two different electronic circuits, which do not have common power and ground connections, must exchange information. Though isolation devices facilitate these signal communications, isolation devices can also introduce a large delay on the signal lines and add skew between the signals. The FSI is designed specifically to make sure reliable high-speed communication for system scenarios that involve communication across isolation barriers without adding components. 

The FSI consists of independent transmitter (FSITX) and receiver (FSIRX) cores. The FSITX and FSIRX cores are configured and operated independently. 

For additional information on the FSI module, refer to _Fast Serial Interface (FSI) Skew Compensation_ . 

## _**7.5.9.1.1 FSI Features**_ 

The FSI module includes the following features: 

- Independent transmitter and receiver cores 

- Source-synchronous transmission 

- Double Data Rate (DDR) 

- One or two data lines 

- Programmable data length 

- Skew adjustment block to compensate for board and system delay mismatches 

- Frame error detection 

- Programmable frame tagging for message filtering 

- Hardware ping to detect line breaks during communication (ping watchdog) 

- Two interrupts per FSI core 

- Externally-triggered frame generation 

- Hardware- or software-calculated CRC 

- Embedded ECC computation module 

- Register write protection 

- FSI-SPI compatibility mode (limited features available) 

- Tag match notifications 

## _**7.5.9.1.2 FSI Block Diagram**_ 

This device contains 4 instance of FSI TX and FSI RX cores. The integration details are captured below: 

848 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [500 x 306] intentionally omitted <==**

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

849 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.9.2 System-level Integration** 

This section describes the device-level integration of the FSI module. Some of the features can require additional configuration of modules that are not within the scope of this chapter, the details can be found elsewhere in this TRM. 

**==> picture [500 x 219] intentionally omitted <==**

The FSI IP clock provided is the 200MHz system clock with 

the option to gate using GLOBAL_CTRLSS_FSI_RX[x]_CLK_GATE:CLK_GATE and GLOBAL_CTRLSS_FSI_TX[x]_CLK_GATE:CLK_GATE. 

Software generated reset is provided and can be controlled using GLOBAL_CTRL_FSI_RX[x]_RST:RST and GLOBAL_CTRL_FSI_TX[x]_RST:RST. 

850 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.2.1 Signal Description**_ 

FSI is a point-to-point communication protocol. Hence, an FSI transmitter core communicates directly to a single FSI receiver core. Similarly, an FSI receiver core receives data from a single FSI transmitter core. 

Each FSI core has three signals: one clock and two data signals. Data is always transmitted or received with the most-significant bit of each frame field being first. If multi-lane transmissions are not used, the TXD1 and RXD1 signals can be left unconnected and their GPIOs repurposed for other application needs. Table 7-174 and Table 7-175 describe the various signals that can be selected by the PADCONFIG register to be brought out to device pins. 

**CAUTION** The maximum RXCLK rate is SYSCLK/2 and must not exceed this limit. 

## **Table 7-174. FSI Receiver Core Signals** 

|**Signal Name**|**Direction**|**Description**|**Inactive Level**(1)|
|---|---|---|---|
|RXCLK|Input|This is the receive clock input signal for the FSI receive module.|Logic High|
|||This must be connected to TXCLK of the transmitting FSI module.||
|RXD0|Input|This is the primary data input line for reception. This must be connected to the TXD0|Logic High|
|||of the transmitting FSI module.||
|RXD1|Input|This is an additional data input line for reception. This signal must be connected to|Logic High|
|||the TXD1 of the transmitting FSI module, if multi-lane transmission is used.||



(1) Inactive level refers to the state of the pin while the module is not actively receiving data. 

**Table 7-175. FSI Transmitter Core Signals** 

|**Signal Name**|**Direction**|**Description**|**Inactive Level**(1)|
|---|---|---|---|
|TXCLK|Output|This is the transmit clock and is driven by the FSI transmit module.|Logic High|
|||During a transmission, four clock edges are transmitted before the start of frame||
|||phase (preamble) and four clock edges follow the last bit of the frame (postamble).||
|||Data is transmitted on both edges of the clock.||
|||In FSI-SPI compatibility mode, the preamble and the post frame clock edges are not||
|||transmitted. Data is transmitted only on one edge of the clock. Data transmits on||
|||rising edge and received on falling edge of the clock.||
|TXD0|Output|This is the primary data output line for transmission and is driven by the FSI transmit|Logic High|
|||module.||
|||When the FSI is configured for multi-lane transmission, TXD0 contains all the even||
|||numbered bits of the data and CRC bytes. Other frame fields such as frame type,||
|||start-of-frame, tag, and end-of-frame are transmitted in full.||
|TXD1|Output|This is an additional data output line for transmission, if the FSI is configured for|Logic High|
|||multi-lane transmission. This signal is driven by the FSI transmit module.||
|||During transmission, the data bits are split between TXD0 and TXD1. TXD1 contains||
|||all the odd numbered bits of the data and CRC bytes. This applies only to the data||
|||words and the CRC bytes. Other data frame related information like Frame Type,||
|||Start-of-Frame, Tag and End-of-frame, the state of this line are identical to TXD0.||



(1) Inactive level refers to the state of the pin while the module is not actively transmitting, or held in reset. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

851 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.9.2.1.1 Configuring Device Pins**_ 

The GPIO mux registers must be configured to connect this peripheral to the device pins. 

Some IO functionality is defined by GPIO register settings independent of this peripheral. For input signals, the GPIO input qualification must be set to asynchronous mode by setting the appropriate QUAL_SEL register bits to 0x3. The internal pullups can be configured with the PUPDSEL register bit. See the _General Purpose Input-Output (GPIO)_ chapter for more details on the GPIO mux and settings. 

## _**7.5.9.2.2 FSI Interrupts**_ 

Each FSI module contains multiple interrupt sources that can be assigned to two different interrupt vectors: INT1 and INT2. Each interrupt source has an associated status flag, force, and clear bits in the EVT_STS, EVT_FRC, and the EVT_CLR registers, respectively. 

Each interrupt can be assigned to either interrupt vector, INT1 and INT2, to allow for two priority levels. Alternately, the interrupt source can be prevented from generating any interrupt, though the status flag can still be set and monitored by software. The transmitter events are assigned to either interrupt vector in the TX_INT_CTRL register. The receiver events are assigned an interrupt vector using RX_INT1_CTRL and RX_INT2_CTRL registers. If an interrupt is not required, make sure the bit is not set in the respective INT_CTRL register. 

## _**7.5.9.2.2.1 Transmitter Interrupts**_ 

The transmitter can generate the following interrupts: 

- **Frame Done (FRAME_DONE):** This event indicates that FSI has completed transmitting a frame. 

- **Buffer Underrun (BUF_UNDERRUN):** This event indicates that the transmit buffer has experienced underrun. Buffer underrun occurs when the transmitter tries to read data from a location which has not yet be written to by the CPU, or DMA. 

- **Buffer Overrun (BUF_OVERRUN):** The buffer overrun interrupt is generated when the buffer has experienced overrun. Buffer overrun can occur if a piece of data is overwritten before the data has been transmitted. 

- **Ping Frame Triggered (PING_TRIGGERED):** The ping frame triggered interrupt is generated when the ping frame has been triggered. This bit is set when the ping counter has timed out or an external ping trigger event has occurred. 

852 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.2.2.2 Receiver Interrupts**_ 

The receiver core is capable of generating interrupts from many different events: 

- **Ping Watchdog Timeout (PING_WD_TO):** This event indicates that the ping watchdog timer has timed out. The receiver has not received a valid frame within the time period specified in the RX_PING_WD_REF register. 

- **Frame Watchdog Timeout (FRAME_WD_TO):** This event indicates that the frame watchdog timer has timed out. The conditions of this timeout are set using the RX_FRAME_WD_CTRL register. As soon as the start of frame phase is detected, the frame watchdog counter starts counting from 0. The end of frame phase must complete by the time the watchdog counter reaches the reference value. If this does not happen, the watchdog times out and this event is generated. If this event occurs, the receiver must undergo a soft reset and subsequent resynchronization to resume proper operation. 

- **CRC Error (CRC_ERR):** This error indicates that a CRC error has occurred. A CRC error is generated when the received CRC and the computed CRC do not match. 

- **Frame Type Error (TYPE_ERR):** This error indicates that an invalid frame type has been received. If this error occurs, the receiver must undergo a soft reset and subsequent resynchronization to resume proper operation. 

- **End-of-Frame Error (EOF_ERR):** This error indicates that an invalid end-of-frame bit pattern has been received. If this error occurs, the receiver must undergo a soft reset and subsequent resynchronization to resume proper operation. 

- **Receive Buffer Overrun (BUF_OVERRUN):** This event indicates that an overrun condition has occurred in the receive buffer. 

- **Receive Buffer Underrun (BUF_UNDERRUN):** This event indicates that an underrun condition has occurred in the receive buffer. This condition occurs when software reads an empty buffer. 

- **Frame Done (FRAME_DONE):** This event indicates that a valid frame has been received without error. 

- **Error Frame Received (ERR_FRAME):** This event indicates that an error frame has been received. 

- **Ping Frame Received (PING_FRAME):** This event indicates that a ping frame has been received. 

- **Frame Overrun (FRAME_OVERRUN):** This event indicates that a new frame has been received while the FRAME_DONE flag was still set. 

- **Data Frame Received (DATA_FRAME):** This event indicates that a data frame has been received. 

- **Ping Tag Matched (PING_TAG_MATCH):** This event indicates that a ping frame with a matching tag has been received. 

- **Data Tag Matched (DATA_TAG_MATCH):** This event indicates that a data frame with a matching tag has been received. 

- **Error Tag Matched (ERROR_TAG_MATCH):** This event indicates that an error frame with a matching tag has been received. 

## _**7.5.9.2.2.3 Configuring Interrupts**_ 

To configure interrupts on the FSI, the application must select the interrupt vector for each desired event using the TX_INT_CTRL register for the transmitter, and RX_INT1_CTRL_ALT1_ and RX_INT2_CTRL_ALT1_ registers for the receiver. There is no module-level interrupt enable bit to configure. 

## **Note** 

If an event is registered for both interrupt vectors, both interrupts fire. There are no hardware checks for overlapping interrupt vector assignments. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 853 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.9.2.2.4 Handling Interrupts**_ 

Inside the interrupt service routine (ISR), the user must clear the event flag using the EVT_CLR register and then acknowledge the CPU interrupt. 

If the one event occurs multiple times before the corresponding bit is cleared by software, no new interrupt is generated. 

If multiple events occur simultaneously, or very close in time, it is possible to handle multiple conditions within a single interrupt. Each flag is independently set by hardware and must be cleared by application software. If multiple different events occur, the ISR can handle each in whatever order is deemed necessary by the application. It is not advisable to clear the full interrupt status register in every ISR. This can cause the application to miss events that can be detrimental to the application. A sample sequence for handling interrupts on the receiver follows; the transmitter routine is similar. 

- On receiving an interrupt, copy the current state of the receive event and error status flag register (RX_EVT_STS_ALT1_) into a local snapshot variable. 

- Read all of the bits from the snapshot to determine the events that require action. 

- Perform the necessary actions for each of the events seen in the snapshot. 

- Write to the receive event and error clear register (RX_EVT_CLR_ALT1_) with the snapshot to clear only those interrupts that were set at the beginning of the ISR. 

- Repeat this sequence for every generated ISR. 

There is a chance that another event occurred during the just-handled ISR since only the snapshot of events was handled and then cleared; an event flag can still be set at the end of the ISR. As soon as the ISR completes, a new interrupt is generated and this flag is still set and can be handled accordingly. 

Software accesses tied to multiple events and handled within the same ISR can cause race conditions that cause the software to not function as desired. For example, it is recommended to use different interrupt lines if the user wants to enable events for both ping and data frames. If both events are handled within the same interrupt line, the software can only respond to one of the events if both events occur close in time. 

## _**7.5.9.2.3 DMA Interface**_ 

Both the transmitter and receiver are capable of using the DMA for automatic data transfers. The DMA trigger is independent from the interrupt signals. DMA events are only triggered on the completion of a data frame. 

The transmitter DMA trigger is enabled by setting TX_DMA_CTRL.DMA_EVT_EN to 1. The transmitter must also set TX_OPER_CTRL_LO_ALT2_.START_MODE to 0x2 to allow either a write to the TX_FRAME_CTRL.START bit or to the TX_FRAME_TAG_UDATA register to start the transmission. 

The receiver DMA trigger is enabled by setting RX_DMA_CTRL.DMA_EVT_EN to 1. 

Refer to Section 7.5.9.3.2 and Section 7.5.9.3.3 for more DMA information specific to each FSI Module. 

854 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.2.4 External/PING Trigger Sources**_ 

The FSITX has two muxes connected to the transmitter core, EXTRIG and PINGTRIG. These muxes are used to select external signals as a trigger to start generic frames, and ping frames. The muxes are independently configured for each type of frame. The application can select one trigger source per frame type. Note that the use of these triggers is optional. 

The generic frame trigger is configured by setting TX_OPER_CTRL_HI_ALT1_.EXT_TRIG_SEL to the index of the desired trigger. TX_OPER_CTRL_LO_ALT1_.START_MODE must be set to 0x1 for a frame to be transmitted by an external trigger. 

The external ping frame trigger is configured by setting TX_PING_CTRL_ALT1_.EXT_TRIG_SEL to the index of the desired trigger. TX_PING_CTRL.EXT_TRIG_EN must also be set to allow the trigger to generate a ping frame. 

## **Note** 

Triggers generated by PWMXBAR are asynchronous and must be at least 3 SYSCLKs wide. 

**Table 7-176. FSITX[x] External/PING Trigger Source Table** 

|**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**|**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**|**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**|**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**|**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**|**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**|**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**|**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**<br>**Index**<br>**Source**|
|---|---|---|---|---|---|---|---|
|0|FSI_RX[x]:**PING**<br>FRAME_TAG_MATCH|16|EPWM8.SOCB|32|NC|48|OUTPUTXBAR.OUT0|
|1|FSI_RX[x]:**ERROR**<br>FRAME_TAG_MATCH|17|EPWM9.SOCB|33|NC|49|OUTPUTXBAR.OUT1|
|2|FSI_RX[x]:**DATA**<br>FRAME_TAG_MATCH|18|NC|34|NC|50|OUTPUTXBAR.OUT2|
|3|NC|19|NC|35|NC|51|OUTPUTXBAR.OUT3|
|4|FSI_RX[x].TRIG0|20|NC|36|NC|52|OUTPUTXBAR.OUT4|
|5|FSI_RX[x].TRIG1|21|NC|37|NC|53|OUTPUTXBAR.OUT5|
|6|FSI_RX[x].TRIG2|22|NC|38|NC|54|OUTPUTXBAR.OUT6|
|7|FSI_RX[x].TRIG3|23|NC|39|NC|55|OUTPUTXBAR.OUT7|
|8|EPWM0.SOCB|24|NC|40|ICSS_PORT0.16|56|OUTPUTXBAR.OUT8|
|9|EPWM1.SOCB|25|NC|41|ICSS_PORT0.17|57|OUTPUTXBAR.OUT9|
|10|EPWM2.SOCB|26|NC|42|ICSS_PORT0.18|58|OUTPUTXBAR.OUT10|
|11|EPWM3.SOCB|27|NC|43|ICSS_PORT0.19|59|OUTPUTXBAR.OUT11|
|12|EPWM4.SOCB|28|NC|44|ICSS_PORT1.16|60|OUTPUTXBAR.OUT12|
|13|EPWM5.SOCB|29|NC|45|ICSS_PORT1.17|61|OUTPUTXBAR.OUT13|
|14|EPWM6.SOCB|30|NC|46|ICSS_PORT1.18|62|OUTPUTXBAR.OUT14|
|15|EPWM7.SOCB|31|NC|47|ICSS_PORT1.19|63|OUTPUTXBAR.OUT15|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 855 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Note** 

FRAME_TAG_MATCH and TRIG[0:3] signals are only available from the equivalent FSIRX instance. (FSITX0 =FSIRX0, FSITX1 = FSIRX1, etc...) 

856 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.9.3 FSI Functional Description** 

## _**7.5.9.3.1 Introduction to Operation**_ 

The Fast Serial Interface Transmitter and Receiver modules (FSITX/FSIRX) are two unique modules on the device. Each module has a dedicated set of control registers, clocking, and interrupts. The following sections describe the Fast Serial Interface frame format and the different initialization and configuration procedures for both the transmitter and receiver. 

## _**7.5.9.3.2 FSI Transmitter Module**_ 

The FSI transmitter (FSITX) module handles the framing of data, CRC generation, and signal generation of TXCLK, TXD0, and TXD1, as well as interrupt generation. The operation of the transmitter core is controlled and configured through programmable control registers. The transmitter control registers allow the CPU to program, control, and monitor the operation of the FSI receiver. The transmit data buffer is accessible by the CPU and the DMA. 

The transmitter has the following features: 

- Automated ping frame generation 

- Externally triggered ping frames 

- Externally triggered data frames 

- Software-configurable frame lengths 

- Programmable TX delay line control 

- 16-word data buffer 

- Data buffer underrun and overrun detection 

- Hardware-generated CRC on data bits 

- Software ECC calculation on select data 

- DMA support 

Figure 7-349 shows the high-level block diagram of the FSI transmitter. Figure 7-350 shows the block diagram of the transmitter core submodule. 

The following sections describe the various aspects of the FSI transmitter in greater detail. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

857 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [438 x 267] intentionally omitted <==**

**----- Start of picture text -----**<br>
FSITX<br>PLLRAWCLK<br>SYSRSN<br>SYSCLK<br>Transmit Clock  TXCLKIN TXCLK = TXCLKIN/2FSI Mode:<br>Generator SPI Signaling Mode:<br>Register Interface TXCLK = TXCLKIN<br>Core Reset<br>FSITXINT1<br>Control Registers,  TXCLK<br>FSITXINT2 Interrupt Management<br>FSITX_DMA_EVT Ping Time-out Counter<br>TXD0<br>Transmitter Core<br>External Frame Triggers TXD1<br>Transmit Data<br>Buffer<br>ECC Logic<br>**----- End of picture text -----**<br>


**Figure 7-349. FSI Transmitter Block Diagram** 

**==> picture [378 x 296] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transmitter Core TXCLK<br>TXD0<br>TXCLKIN Serializer<br>TXD1<br>Core Reset<br>Configuration and settings<br>CRC Submodule<br>Protocol State Machine<br>Transmit Buffer Data<br>Ping Request<br>Frame Arbitration Block<br>Transfer Request<br>**----- End of picture text -----**<br>


**Figure 7-350. FSI Transmitter Core Block Diagram** 

858 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.2.1 Initialization**_ 

On the first initialization or after a module reset due to an underrun condition, the transmitter module executes the following initialization sequence to start or resume transmit operations. 

1. Initialize the transmitter clock by setting TX_CLK_CTRL.CLK_RST to 1 and subsequently clearing the bit. 

2. Set the clock to the transmitter core to PLLRAWCLK by setting TX_OPER_CTRL_LO_ALT2_.SEL_PLLCLK to 1. 

3. Set the clock prescaler value to the desired rate by writing to TX_CLK_CTRL.PRESCALE_VAL. 

4. Enable the transmitter clock divider by setting TX_CLK_CTRL.CLK_EN to 1. 

5. Assert the transmitter module soft reset by writing 0xA501 to TX_MAIN_CTRL. 

6. Wait four TXCLK cycles. 

7. Release the transmitter core from reset by writing 0xA500 to TX_MAIN_CTRL. 

After initialization and configuration, the transmitter module synchronizes with the receiver module before transmitting. The synchronization sequence is described in Section 7.5.9.4.1. 

## **CAUTION** 

Do not change TX_CLK_CTRL.PRESCALE_VAL while the clock is enabled (TX_CLK_CTRL.CLK_EN = 1). Doing so can cause undefined behavior. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

859 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.9.3.2.2 FSI_TX Clocking**_ 

The transmitter core registers and control logic run off of the device system clock (SYSCLK). 

The FSI Transmit Clock (TXCLK) is derived from PLLRAWCLK. PLLRAWCLK is divided down by configuring the clock prescaler value (TX_CLK_CTRL.PRESCALE_VAL) then setting the clock divider enable bit (TX_CLK_CTRL.CLK_EN). The clock prescaler value can be set to divide PLLRAWCLK by 1 (TX_CLK_CTRL.PRESCALE_VAL = 0x0 or 0x1) through 255(TX_CLK_CTRL.PRESCAL_VAL = 0xFF). Though TXCLK and SYSCLK are both derived from PLLRAWCLK, TXCLK is asynchronous with respect to SYSCLK. 

## **CAUTION** 

TXCLK must never be configured to be faster than SYSCLK/2. 

## _**7.5.9.3.2.3 Transmitting Frames**_ 

On the transmitter, the ping frame is the only frame that can be set up and transmitted without any further software or DMA intervention. Ping frames can be transmitted by any (or all) of the three sources: automatic ping timer, software, or external triggers. 

Each available frame type can be sent multiple ways. Generically, the following steps must be executed before the frame is sent. These steps can be executed in any order before the start condition is set. 

1. Configure the frame type 

2. Set the frame tag 

3. If the frame to be sent is a data frame: 

   - Set the user data 

   - Write to the data buffer 

   - Set the word length if the frame is a software defined frame length 

4. Set the start condition 

## **Note** 

Transmit Frame Start Restriction: 

A new frame transmission can be initiated by one of the methods selected in the TX_OPER_CTRL_LO_ALT2_.START_MODE bits. If there is already a PING frame transmission taking place, due to a hardware initiated PING timer, the new frame transmission begins as soon as the on-going PING transmission is completed. 

Once a START of frame has been initiated, the next START of frame is recognized when the first frame has started transmitting the End-of-Frame (EOF) field. If a new START trigger arrives before the current transmission has reached the EOF field, the trigger is lost without a notification. 

## **Note** 

There is no hardware check implemented to check whether the type field written by software is valid or not. If an invalid type is used and a frame transmission is initiated, the behavior is: 

- The transmitted frame structure is exactly like an NWORD data frame. The size of the data frame is determined by the value in the TX_FRAME_CTRL.N_WORDS register. 

- The frame type field of the transmitted data frame is transmitted as programmed. If this is received by an FSI receiver, a Type error is generated. 

This mechanism can be used for force a Type error in a received frame for testing purposes. 

The following sections describe the specific configuration for each frame type and start condition. 

860 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.2.3.1 Software Triggered Frames**_ 

The most basic way to transmit a data frame is through software. Each step must be handled by the application. To send a data frame using software, the following steps must be executed. Steps 1-6 can be executed in any order before setting TX_FRAME_CTRL.START. Some fields do not need to be reconfigured for every transmission. The frame tag, user data, and frame type are sticky and are retransmitted in the subsequent frame unless modified by software. 

1. Write the data to be transmitted to the next location of the transmit data buffer. 

2. Set TX_FRAME_CTRL.FRAME_TYPE to the appropriate value for the type of frame to be transmitted. 

3. Set TX_FRAME_CTRL.N_WORDS to 1 less than the number of words to be transmitted if TX_FRAME_CTRL.FRAME_TYPE is set to 0011, the frame type of the software-defined length data frame. That is, if 16 words are transmitted, N = 16, set TX_FRAME_CTRL.N_WORDS to 15. 

4. When the frame is assembled before transmitting, the FSITX hardware calculates the CRC to be transmitted. If TX_OPER_CTRL_LO_ALT2_.SW_CRC is 1, the application can calculate a custom CRC value and then set TX_USER_CRC to the result. 

5. Set TX_FRAME_TAG_UDATA.FRAME_TAG to the desired tag. 

6. Set TX_FRAME_TAG_UDATA.USER_DATA to the desired user data. 

7. Set TX_FRAME_CTRL.START to 1 to initiate the transmission of the data frame. 

Once the frame transmission has started, the TX_FRAME_CTRL.START is cleared by hardware. To monitor if the frame has completed, the software can poll TX_EVT_STS.FRAME_DONE. 

## _**7.5.9.3.2.3.2 Externally Triggered Frames**_ 

The transmitter can transmit frames when triggered by an external source. See Section 7.5.9.2.4 for more information on the available external triggers. 

To transmit frames using an external trigger, the application must follow the same procedure as described in Section 7.5.9.3.2.3.1. The only difference is that in Step 7, the start condition is automatically set when the external trigger condition is met rather than by software. 

Note that by externally triggering frames, the frame information to be sent is pulled from the same registers described in the previous section. Because of this, it is possible to send any type of frame from an external trigger including ping, error, and data frames. Also, there is no hardware mechanism by which the FSI can determine if multiple triggers occur. The FSITX takes the data as is, and the application software makes sure that this data has been updated as necessary. 

Using TX_EVT_STS fields either by polling or by interrupts, the application can populate or update the frame information to be sent in the next frame 

## _**7.5.9.3.2.3.3 Ping Frame Generation**_ 

Assuming the FSI transmitter has already been properly initialized, the following sequences can be used to configure and send ping frames. 

## _**7.5.9.3.2.3.3.1 Automatic Ping Frames**_ 

To generate periodic ping frames, the following steps must be followed: 

1. Initialize the ping counter by writing 1 to TX_PING_CTRL_ALT1_.CNT_RST. 

2. Set the desired ping tag to TX_PING_TAG.TAG. 

3. Set the ping timer reference value to TX_PING_TO_REF.TO_REF. 

4. Enable the ping timer by writing 1 to TX_PING_CTRL_ALT1_.TIMER_EN. 

The ping timer is a free-running counter that counts up from 0. The current value of the ping timer counter is found in TX_PING_TO_CNT. When the current value of TX_PING_TO_CNT matches the reference value TX_PING_TO_REF.TO_REF, the TX_EVT_STS.PING_TRIGGERED is set. TX_PING_TO_CNT resets to 0 and resumes counting until the next match has occurred or the ping timer is halted by software (TX_PING_CTRL.TIMER_EN is set to 0). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

861 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.9.3.2.3.3.2 Software Triggered Ping Frame**_ 

Software can also manually generate a ping frame. The process for sending a ping frame with software is very similar to sending the other types of frames. The following steps must be followed: 

1. Set TX_FRAME_CTRL.FRAME_TYPE to 0000’b to denote that the frame being sent is a Ping Frame. 

2. Set TX_FRAME_TAG_UDATA.FRAME_TAG to the desired value. 

3. Write 1 to TX_FRAME_CTRL.START. This starts the transmission. 

Once the frame transmission has started, the TX_FRAME_CTRL.START is cleared by hardware. To monitor if the frame has completed, the software can poll TX_EVT_STS.FRAME_DONE. 

## _**7.5.9.3.2.3.3.3 Externally Triggered Ping Frame**_ 

The last source for generating ping frames is an external trigger. One of up to 32 different triggers can be selected. See Section 7.5.9.2.4 for the list of input sources. 

## **CAUTION** 

Ping frames can be triggered by both an external trigger source and the internal ping timer. If TX_PING_CTRL_ALT1_.EXT_TRIG_EN is set to 1, the external trigger source takes precedence and the ping timer is ignored. 

## _**7.5.9.3.2.3.4 Transmitting Frames with DMA**_ 

The FSI transmitter can send data that is continuously applied with the DMA. A DMA trigger is generated every time a data frame transmission is completed. This is concurrent with the FRAME_DONE signal that sets the TX_EVT_STS.FRAME_DONE flag. 

To transmit continuous data with the DMA, some configurations need to be made on the transmitter: 

First, set TX_DMA_CTRL.DMA_EVT_EN to 1. This allows the DMA trigger to propagate to the DMA module. Next, TX_OPER_CTRL_LO_ALT2_.START_MODE must be set to 0x2. The transmitter is now able to start a transmission using a software write to TX_FRAME_CTRL.START or TX_FRAME_TAG_UDATA.. 

The DMA must also be configured properly for the FSI to send the data. One way of using the DMA to continuously feed the transmit buffer is: 

- Set up two DMA channels to be triggered by the same FSI transmitter and DMA trigger. 

- Configure one channel to fill the transmit buffer. 

- Configure the other channel to set the frame tag and user data fields 

- Since the FSI transmit buffer is a 16-word circular buffer, make sure the DMA channel servicing the data buffer wraps the after 16 words are copied. 

## **Note** 

Because the frame tag and user data must be written in to initiate the transmission of the frame, use two consecutive DMA channels. This makes sure that the DMA channels are always executed in sequence. The DMA channel servicing the data buffer must be the lower numbered channel and the tag/user data channel must be the next. For example, configure DMA channel 3 to service the data buffer, and configure DMA channel 4 to service the tag and user data. 

862 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.2.4 Delay Line Control**_ 

The transmitter module has a programmable delay line on each of the external signal inputs: TXCLK, TXD0, and TXD1. The delay elements introduce delays on the respective lines and are placed before the FSITX signals are sent to the TDM signal selection mux (controlled by the SEL_TDM_PATH signal). This is to facilitate adjustment for signal delays introduced by system level components such as signal buffers, ferrite beads, isolators, and so on, or board delays such as uneven trace lengths, long cable length, and so on. The length of the delay is controlled by setting the TX_DLY_LINE_CTRL register values for each line. By default, no delay is introduced by the delay line elements. The delay values should only be adjusted while the FSITX is held in soft reset, ensuring that there are no active transmissions during this process. Figure 7-351 shows a representation of the delay line circuitry for the input signals. The implementation for TXCLK, TXD0, and TXD1 are replicas of this diagram. All circuits will behave similarly. 

**==> picture [432 x 143] intentionally omitted <==**

**Figure 7-351. Delay Line Control Circuit** 

For more information on skew compensation, refer to the _Fast Serial Interface (FSI) Skew Compensation Application Report_ . 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

863 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.9.3.2.5 Transmit Buffer Management**_ 

The FSI transmitter has a 16-word buffer that the FSI transmitter pulls data to transmit. This buffer is implemented as a circular buffer, not a FIFO, so some care must be taken to properly interpret buffer overrun and underrun, as well as the TX_BUF_PTR_STS register. These flags and pointers work under the assumption that the software or DMA is using the buffer as a circular buffer. This mode of operation is the only way that the overrun, underrun, and pointer status are meaningful. If data is being sourced by the DMA and there is some other periodic trigger mechanism trying to initiate transfers, underrun becomes a critical error. If an underrun happens, a buffer went out of sync. This not only affects the current transfer, but all future transfers also cannot be sure of due to the ring buffer. Under such conditions, the underrun needs a soft reset to cleanly recover. Alternately, the software can manually stop the transmitting, reset the buffer pointers, clear the remaining error conditions, and then restart transmission. The software method involves a few steps, while the soft reset is a single action and makes sure of a full reset of the control registers. 

Due to the flexibility of the transmit buffer, software can implement a simple ping-pong buffer or randomly load and send from any location of the buffer. If the buffer is used in this manner, error flags and status fields can be ignored without adversely affecting the transmitter capability. Additionally, the CURR_WORD_CNT is also invalid if used in this way. The application can set the buffer pointer manually by writing the 4-bit index to TX_BUF_PTR_LOAD. This forces the transmitter to start picking the data from the indicated location in the buffer. 

## _**7.5.9.3.2.6 CRC Submodule**_ 

The FSI transmitter can supply the CRC to the frame being transmitted through the embedded hardware CRC submodule or by supplying a user-defined value. This is controlled by setting TX_OPER_CTRL_LO_ALT2_.SW_CRC appropriately. 

If hardware CRC generation is selected (TX_OPER_CTRL_LO_ALT2_.SW_CRC = 0, the default), the CRC is computed by hardware on the data and user data fields using the CRC polynomial 0x7 (x[8] + x[2] + x + 1). The transmitter module automatically computes the CRC on the data fields without user intervention when the frame is transmitted. For more information on how the CRC is generated by the CRC submodule, refer to Section 7.5.9.3.7. 

If software CRC generation is selected (TX_OPER_CTRL_LO_ALT2_.SW_CRC = 1), the CRC must be computed by software and placed in the TX_USER_CRC register. The next frame to be transmitted uses the value placed in the TX_USER_CRC register in place of the CRC value generated by the hardware. 

As the TX_USER_CRC register is software-programmable, the application can use this field as an extra data field for application-specific purposes. If TX_USER_CRC is used in this manner, the CRC detection on the receiver is not valid and must be ignored. 

## _**7.5.9.3.2.7 Conditions in Which the Transmitter Must Undergo a Soft Reset**_ 

Unlike the receiver, there are no detectable errors that require a soft reset. A buffer overrun or underrun interrupt can or cannot require a soft reset to resume proper operation. This determination is up to the application software. Refer to Section 7.5.9.3.2.5 for more information on the transmit buffer. 

## _**7.5.9.3.2.8 Reset**_ 

The entire transmitter module and all transmitter registers are reset by SYSRSn. The transmitter core is reset by SYSRSn or by writing a 1 to TX_MAIN_CTRL.CORE_RST. 

A module reset causes the registers to be reset to their default state. 

864 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.3 FSI Receiver Module**_ 

The receiver module interfaces to the FSI clock (RXCLK), and data lines (RXD0 and RXD1) after they pass through an optional programmable delay line. The receiver core handles the data framing, CRC computation, and frame-related error checking. The receiver bit clock and state machine are run by the RXCLK input, which is asynchronous to the device system clock. 

The receiver control registers allow the CPU to program, control, and monitor the operation of the FSI receiver. The receive data buffer is accessible by the CPU and the DMA. 

The receiver core has the following features: 

- 16-word data buffer 

- Multiple supported frame types 

- Ping frame watchdog 

- Frame watchdog 

- CRC calculation and comparison in hardware 

- ECC detection 

- Programmable delay line control on incoming signals 

- DMA support 

- FSI-SPI compatibility mode 

Figure 7-352 provides a high-level overview of the internal modules present in the FSI receiver. Figure 7-353 shows a view of the FSI receiver core submodule. Not all data paths and internal connections are shown. 

The following sections describe the various aspects of the FSI receiver module. 

**==> picture [456 x 267] intentionally omitted <==**

**----- Start of picture text -----**<br>
FSIRX<br>SYSRSn<br>SYSCLK<br>Frame Watchdog<br>Register Interface<br>Core Reset<br>FSIRXINT1<br>Control Registers,<br>FSIRXINT2 Interrupt Management<br>RXCLK<br>FSIRX_DMA_EVT Ping Watchdog<br>Receiver Core Skew<br>RXD0<br>Control<br>RXD1<br>Receive Data<br>Buffer<br>ECC Check<br>Logic<br>**----- End of picture text -----**<br>


**Figure 7-352. FSI Receiver Block Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

865 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [392 x 307] intentionally omitted <==**

**----- Start of picture text -----**<br>
Receiver Core<br>RXCLK<br>RXD0<br>Deserializer<br>RXD1<br>Core Reset<br>Configuration and settings<br>Computed CRC CRC Submodule<br>Received CRC<br>Frame Analyzer and<br>Decoder<br>Frame Information<br>Received Data<br>**----- End of picture text -----**<br>


**Figure 7-353. FSI Receiver Core Block Diagram** 

## _**7.5.9.3.3.1 Initialization**_ 

On the first initialization or after a module reset following any frame error, the receiver module asserts and releases the receiver core reset bit (RX_MAIN_CTRL_ALTC_.CORE_RST) prior to any other initialization. Once the receiver module is initialized, the following steps are executed: 

1. If required, assign interrupt sources to the necessary interrupt line. 

2. If required, configure the ping watchdog to periodically check for an active link to the transmitter. See Section 7.5.9.3.3.4 for configuration details. 

3. If required, configure the frame watchdog to make sure that each frame is received within a predetermined window. See Section 7.5.9.3.3.5 for configuration details. 

4. Initialize the receive buffer pointer by writing to the RX_BUF_PTR_LOAD register. Received data is placed into the buffer starting with the address loaded in this register. 

5. Make sure all errors and flags have been cleared from the RX_EVT_STS_ALT1_ register. 

At this point the receiver is ready to receive any incoming frames. Software can now either poll on the RX_EVT_STS_ALT1_ register for various conditions. For example, when the 

RX_EVT_STS_ALT1_.FRAME_DONE and no other flags are set, the receiver has successfully received a frame without error. 

Next, the application configures the various features such as the ping and frame watchdogs, DMA, external triggering, and so on. These features are described in subsequent sections. The receiver module is now ready to synchronize with the transmitter then begin reception. The synchronization sequence is described in Section 7.5.9.4.1. 

866 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.3.2 FSI_RX Clocking**_ 

The receiver module registers and control logic are clocked by the device system clock (SYSCLK). The receiver state machine is clocked by the receiver input clock pin (RXCLK). 

## **CAUTION** 

RXCLK must never be faster than SYSCLK. 

## _**7.5.9.3.3.3 Receiving Frames**_ 

Once the receiver has been properly configured and synchronized, incoming messages are handled as described below. Note that there is no equivalent to a chip-select signal to gate incoming data. Every valid clock edge latches data into the receiver. 

The header information of the received frame is placed in their respective register fields. 

- RX_FRAME_INFO.FRAME_TYPE contains the received frame type. 

- RX_FRAME_TAG_UDATA.FRAME_TAG contains the received frame tag. 

- RX_FRAME_TAG_UDATA.USER_DATA contains the received user data. 

If any error conditions occur during reception such as a CRC mismatch, frame error, frame timeout, buffer overrun, or ping watchdog timeout, the corresponding flag is set in the RX_EVT_STS_ALT1_ register. 

## **Note** 

If at any point during operation a frame error occurs, the receiver module must be reset and resynchronized with the transmitter before the next frame can be successfully received. The follow errors are classified as frame errors: 

- Type error 

- CRC error 

- End of frame error 

## _**7.5.9.3.3.3.1 Receiving Frames with DMA**_ 

The FSI receiver can continuously receive data and move the data from the receiver buffer with the DMA. A DMA trigger is generated every time a data frame has been received. This is concurrent with the FRAME_DONE signal that sets the RX_EVT_STS_ALT1_.FRAME_DONE flag. To receive continuous data with the DMA, some configurations need to be made on the receiver. 

First, set RX_DMA_CTRL.DMA_EVT_EN to 1. This allows the DMA trigger to propagate to the DMA module. The receiver is now able to trigger a DMA event upon the reception of a data frame. 

The DMA must also be configured properly for the FSI to receive the data. One way for using the receiver to continuously feed the DMA is: 

- Set up two DMA channels to be triggered by the FSI Receiver DMA Trigger. 

- Configure one DMA channel to copy data from the receive buffer to a larger data buffer. 

- Configure the next DMA channel to copy the received frame tag and user data to another data buffer. 

- Since the FSI receive buffer is a 16-word circular buffer, make sure the DMA channel servicing the data buffer wraps after 16 words are copied. 

Unlike the transmitter, there is no requirement to have the DMA channel which is handling the data buffer, execute before the DMA channel handling the received tag and user data. 

## _**7.5.9.3.3.4 Ping Frame Watchdog**_ 

The ping frame watchdog is a hardware-enabled automatic error detection of the connection status to the transmitter. This watchdog monitors the time elapsed between ping frames. If the transmitter has been set up to 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 867 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

periodically send out a ping frame, the receiver can be set up to monitor whether this frame has been received within a specified amount of time. If the time between ping frames has exceeded the programmed number of clock cycles, an event is triggered that can generate an interrupt or be monitored by software. 

This watchdog has a dedicated counter that is reset and restarted upon the successful reception of a ping frame. The watchdog counter is incremented at the rate of SYSCLK. Optionally, the watchdog can be configured to be reset upon the successful reception of any frame. This option allows the receiver to monitor for any successful frame to indicate that the connection is still alive and the transmitter is still functioning as expected. 

To configure the ping frame watchdog for operation: 

1. Reset the ping watchdog counter by setting RX_PING_WD_CTRL.PING_WD_RST to 1 and then subsequently clearing the bit to 0. 

2. Set RX_OPER_CTRL.PING_WD_RST_MODE to the desired watchdog reset event, set to 0 for ping frames only or set to 1 for any frame. 

3. Set RX_PING_WD_REF to the maximum time between frames. Add 10 additional SYSCLK cycles to account for clock synchronization. 

4. Enable the ping watchdog by setting RX_PING_WD_CTRL.PING_EN to 1. 

The ping watchdog is now enabled and can now monitor for ping frames. 

If the RX_PING_WD_CNT value reaches the value programmed in RX_PING_WD_REF, the RX_EVT_STS.PING_WD_TO flag is set. If configured, an interrupt can be generated on this event. 

## _**7.5.9.3.3.5 Frame Watchdog**_ 

The frame watchdog is an additional feature the receiver can use to monitor for any error conditions. This dedicated watchdog monitors the duration for a single frame to be received. The watchdog starts incrementing at the time the receiver detects a proper start of frame condition. If the end of frame condition is not detected within the expected number of SYSCLK cycles, the frame watchdog is triggered that can generate an interrupt or be monitored by software. 

This watchdog is automatically started and stopped at the start-of-frame and end-of-frame conditions, respectively. The frame watchdog is connected to SYSCLK. 

To configure the frame watchdog for operation: 

1. Reset the frame watchdog counter by setting RX_FRAME_WD_CTRL. FRAME_WD_CNT_RST to 1 and then subsequently clearing the bit to 0. 

2. Set RX_FRAME_WD_REF.FRAME_WD_REF to the maximum number of SYSCLK cycles expected to be in the longest frame that can be received. Add an additional 10 SYSCLK cycles to account for clock synchronization. 

3. Enable the frame watchdog by setting RX_FRAME_WD_CTRL.FRAME_WD_CNT_EN to 1. 

The frame watchdog is now enabled and can detect a failed frame. 

If the RX_FRAME_WD_CNT reaches the value programmed in RX_FRAME_WD_REF, the RX_EVT_STS_ALT1_.FRAME_WD_TO flag is set. If enabled, an interrupt can be generated on this event. 

If the frame watchdog interrupt ever occurs, the receiver core is in an invalid state to receive a new transmission. The only way to recover from a frame watchdog time out is to undergo a soft reset, and subsequently resynchronizing with the transmitter. 

868 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.3.6 Delay Line Control**_ 

The receiver module has a programmable delay line on each of the external signal inputs: RXCLK, RXD0, and RXD1. The delay elements introduce delays on the respective lines. This is to facilitate adjustment for signal delays introduced by system level components such as signal buffers, ferrite beads, isolators, and so on, or board delays such as uneven trace lengths, long cable length, and so on. The length of the delay is controlled by setting the RX_DLY_LINE_CTRL register values for each line. By default, no delay is introduced by the delay line elements. The delay values must only be adjusted while the FSIRX is held in soft reset, making sure that there are no active transmissions during this process. Figure 7-354 shows a representation of the delay line circuitry for the input signals. The implementation for RXCLK, RXD0, and RXD1 are replicas of this diagram. All circuits behave similarly. 

**==> picture [366 x 131] intentionally omitted <==**

**----- Start of picture text -----**<br>
Delay Delay Delay Delay Delay Delay<br>Element Element Element Element Element Element<br>1 2 3 29 30 31<br>RXCLK<br>Input<br>RXCLK to<br>FSIRX<br>**----- End of picture text -----**<br>


**Figure 7-354. Delay Line Control Circuit** 

For more information on skew compensation, refer to _Fast Serial Interface (FSI) Skew Compensation_ . 

## _**7.5.9.3.3.7 Buffer Management**_ 

The FSI receiver has a 16-word buffer that the data is copied to when the data has been received. This buffer is implemented as a circular buffer, not a FIFO, so some care must be taken to properly interpret buffer overrun and underrun as well as the RX_BUF_PTR_STS register. These flags and pointers work under the assumption that the software or DMA is using the buffer as a circular buffer. If the receiver state machine enters into an erroneous state, there is no way for software to cleanly handle this because there is no specified receive clock. For the receiver to detect a clean resynchronization, the state machine needs to be operational and not in the error state. The only way to recover from the error state is to reset the entire receiver module. For overrun and underrun, the receiver can no longer verify that values in the buffer are valid. As such, the best way to recover is to reset the FSI and resynchronize with the transmitter. 

Due to the flexibility of the receive buffer, it is possible for software to implement a simple ping-pong buffer, or to randomly receive and read from any location of the buffer. If the buffer is used in this manner, these flags and status fields can be ignored without adversely affecting the receiver capability. Additionally, the CURR_WORD_CNT is also invalid if used in this way. The application can set the buffer pointer manually by writing the 4-bit index to RX_BUF_PTR_LOAD. This forces the receiver to start storing the received data starting at the indicated location in the buffer. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

869 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.9.3.3.8 CRC Submodule**_ 

The receive module automatically calculates the CRC on the incoming data. The received CRC value is placed into RX_CRC_INFO.RX_CRC. The CRC value calculated by hardware on the received data is placed into RX_CRC_INFO.CALC_CRC. These values are compared by hardware and RX_EVT_STS_ALT1_.CRC_ERROR is set if there is a mismatch. The receiver can generate an interrupt based on RX_EVT_STS_ALT1_.CRC_ERROR if enabled. 

Since the CRC is only used in data frames, the values found in RX_CRC_INFO.RX_CRC and RX_CRC_INFO.CALC_CRC are undefined during ping and error frames. 

For more information on how the CRC is calculated, refer to Section 7.5.9.3.7. 

If the transmitting module is sending a software-defined CRC value (FSITX.TX_OPER_CTRL_LO_ALT2_.SW_CRC = 1), the receiver module triggers a CRC error event if the received value does not match the hardware-calculated value. As this is an application-level decision, the FSIRX can safely disregard the CRC error event. Application software needs to calculate and verify the incoming CRC using the same custom algorithm used on the transmitter and act appropriately. 

The CRC field can also be used as an application-specific value, not a CRC. The application can use the RX_CRC_INFO.RX_CRC as required. All CRC errors and flags can be ignored in this situation. 

## _**7.5.9.3.3.9 Using the Zero Bits of the Receiver Tag Registers**_ 

The receiver tag registers (receiver frame tag and user data (RX_FRAME_TAG_UDATA) register and receiver ping tag (RX_PING_TAG) register)) have the least-significant bit set to 0. The actual received tag is in the bit positions 4:1. The reason for this is to facilitate user software to create a table of functions that can be called depending on the tag value. A function pointer needs a 32-bit storage space and, hence, each successive pointer is offset by 2. If the first pointer is at address x, then the second pointer is at address x + 2, the third at address x + 4, and so on. By keeping the LSB to 0, the five bits of the tag register (bits 4:0) can now be directly used as an index into a table of function pointers. 

## _**7.5.9.3.3.10 Conditions in Which the Receiver Must Undergo a Soft Reset**_ 

The receiver receives data on every clock edge. While there are specific patterns that determine the a start of a frame, and denote the end of a frame, these patterns are able to occur at any point during normal operation inside of the frame. If there ever is a point at which the receiver fails to detect a successful frame, the module must be reset to make sure that subsequent frames are received properly. 

When any of the following errors occur in a received frame, the receiver can be required to be reset and resynchronized with the transmitter: 

- Frame type error 

- End of frame error 

- Ping frame watchdog timeout 

- Frame watchdog timeout 

- Receiver in an invalid state due to noisy clock 

The receiver core status (RX_VIS_1.RX_CORE_STS) can be monitored to determine if the receiver core has entered into an error state requiring a soft reset to resume communication. Incorrect frame type and end of frame errors always cause this bit to become set. A soft reset is required in these cases. A frame watchdog timeout always requires a reset due to the fact that the receiver state machine is still expecting more information when the watchdog timed out. RX_CORE_STS can be used to determine if a noise event was the cause of the failed frame. The ping frame watchdog also does not cause RX_CORE_STS to be set. Similar to the frame watchdog, a corrupt receiver may not be the reason for the ping frame to have timed out. The transmitter could have gone offline and never sent a ping frame. Alternately, during idle time, a noise event could have occurred, thereby putting the receiver into a corrupt state. As the receiver is able to detect this during the ping frame watchdog timeout interrupt handler, this type of event is not lost and the application can act appropriately. 

870 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

As the receiver is clocked by RXCLK, not SYSCLK, a noisy clock or data line can cause some internal design constraints to be violated, putting the receiver core logic into undefined states. Make sure that the clock and data lines satisfy the Electrical Characteristics and timing requirements of the FSI module found in the device data sheet. Failure to do so can cause the receiver state machine to go into an unrecoverable error state. The receiver can only be recovered by undergoing a soft reset. To determine the state of the receiver core after an unexpected frame error, the application must check the receiver core status bit. 

In addition to the above errors, buffer overrun or underrun can warrant a soft reset to resynchronize with the local application software. Refer to Section 7.5.9.3.3.7 for more information on the receive buffers. The requirement of resetting the receiver due to overrun or underrun is up to the application. 

After the receiver has been placed into soft reset, the application must notify the other device's transmitter to begin a new synchronization phase. The simplest way to achieve this is through a ping or error frame sent with a designated tag. If the application is not using the FSITX on the device with the detected error, some other method must be established. The other device must stop transmitting and begin a new synchronization phase. 

## _**7.5.9.3.3.11 FSI_RX Reset**_ 

The receiver module and the registers are reset by SYSRSn. The receiver core is reset by SYSRSn or by writing a 1 to RX_MAIN_CTRL_ALTC_.CORE_RST. 

A module reset causes the registers to be reset to their default state. After a module reset, the receiver module must be re-initialized and the data link re-established. 

## _**7.5.9.3.4 Frame Format**_ 

The FSI module transmits and receives information in frames. Each frame contains multiple phases where different information can be found. The number of phases as well as the total length of the frame varies depending on the frame type being transmitted. Frames can be as short as 16-bits long for a ping or error frame or 288-bits long for a 16-word data frame. 

In normal transmission mode, there are four preamble clock edges before the start of the frame and four post-frame clock edges (postamble). Data is transmitted on both edges of the clock (double data rate). The basic frame structure is shown in Table 7-177. Each phase of the frame (such as start-of-frame, frame type, and so on) is transmitted with the most-significant bit first. Table 7-177 describes the basic frame structure used by the FSI and adapted according to which frame type is transmitted. 

**Table 7-177. Basic Frame Structure** 

|**Idle State**|**Preamble**|**Start of**<br>**Frame**|**Frame**<br>**Type**|**User Data**|**Data**<br>**Words**|**CRC Byte**|**Frame Tag**|**End of**<br>**Frame**|**Postamble**|**Idle State**|
|---|---|---|---|---|---|---|---|---|---|---|
||1111|1001|4 bits|8 bits|1-16<br>words|8 bits|4 bits|0110|1111||



The FSI also supports a FSI-SPI compatibility mode. The SPI compatible frame structure is similar to a standard FSI frame, but there are differences. Refer to Section 7.5.9.3.10 for more information on how to configure and use the FSI-SPI compatibility mode. 

## **Note** 

One word of the FSI refers to 16 bits. 

The terms “frame” and “packet” can be used interchangeably to describe the signaling format of the FSI. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

871 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.9.3.4.1 FSI Frame Phases**_ 

The different phases of the frame structure are described in detail. 

- **Idle State:** During the idle state, the clock and data lines are driven high, the inactive state. 

- **Preamble:** The preamble phase contains four clock edges (or two complete clock pulses) with the data signals held in the high state. These clock edges serve to flush the receiver logic and prepare the receiver logic for receiving a new frame. This phase is not present in SPI compatibility mode. 

- **Start of Frame:** The start of frame phase contains two clock pulses with four bits, 1001, transmitted on the data lines. 

- **Frame Type:** The frame type phase contains two clock pulses with the 4-bit frame type code being transmitted on the data lines. The different frame types are described in detail in Section 7.5.9.3.4.2. The transmitter must set the TX_FRAME_CTRL.FRAME_TYPE field before transmitting a frame. The received frame type is stored in the RX_FRAME_INFO.FRAME_TYPE. 

- **User Data:** The user data phase contains a fully user-configurable data field. There are no restrictions on how this field is used. This phase is only available in data frames. The user data to be transmitted is set by writing to TX_FRAME_TAG_UDATA.USER_DATA. The received user data is stored in RX_FRAME_TAG_UDATA.USER_DATA. 

- **Data:** The data phase contains the data that is being transmitted. The data is pulled from the transmit buffer of the transmitter and is placed in the receive buffer of the receiver. Word 0 is transmitted first. This phase is only present in data frames. Depending on the type of frame transmitted, this can contain anywhere between 1 and 16 words depending on the frame type selected. More information on data frames is found in Section 7.5.9.3.4.2.3. 

- **CRC Byte:** The CRC byte contains the CRC of the transmitted data. The value present in this phase can be sourced from either hardware or software based on the TX_OPER_CTRL_LO_ALT2_.SW_CRC bit. Refer to the module-specific section of the CRC Submodule for more information on the CRC is generated or used, for the transmitter and receiver modules respectively. The CRC byte is only present in data frames. 

- **Frame Tag:** The frame tag contains the 4-bit user-defined frame tag. There are no restrictions on how this field is used in an application. The transmitter supplies this tag into the TX_FRAME_TAG_UDATA.FRAME_TAG bits for data frames. Ping frames use the tag defined in TX_PING_TAG.TAG. The receiver can access the received frame tag in RX_FRAME_TAG_UDATA.FRAME_TAG. 

- **End of Frame:** The end of frame contains four clock edges with four bits, 0110, transmitted on the data lines. 

- • **Postamble:** The postamble contains four additional clock edges with the data lines held in the high state. After the postamble, the clock and data lines are driven high, their inactive state. This phase is not present in FSI-SPI compatibility mode. 

872 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.4.2 Frame Types**_ 

The FSI hardware can generate and handle many predefined frame types. The different frame types can be used by the application to signal different types of events or convey different information to the receiver. The different frame types influence which phases and data fields to include in the transmitted frames. 

Table 7-178 provides a short overview of the different frame types used by the FSI. Each frame type is described in more detail in the following subsections. 

**Table 7-178. Frame Types and Their 4-bit Codes** 

|**Frame Type**|**4-bit Frame Code**|**Description**|
|---|---|---|
|PING|0000|This is the ping frame that can be sent either by software or automatically by|
|||hardware.|
|ERROR|1111|This must be used typically during error conditions or any condition where one side|
|||wants to signal the other side for attention. However, the user software can use this|
|||for any purpose.|
|DATA_1_WORD|0100|1 word data packet (16 bits of data)|
|DATA_2_WORD|0101|2 word data packet (32 bits of data)|
|DATA_4_WORD|0110|4 word data packet (64 bits of data)|
|DATA_6_WORD|0111|6 word data packet (96 bits of data)|
|DATA_N_WORD|0011|N(1-16) word data packet where software has programmed the number of the data|
|||words in a designated register. Both transmitter and receiver modules must have|
|||the same value programmed.|
|Reserved|0001, 0010, and|Reserved|
||1000-1110||



## _**7.5.9.3.4.2.1 Ping Frames**_ 

Ping frames are one of the most basic frames that can be generated by the FSI. Table 7-179 shows the structure of the ping frames. 

**Table 7-179. Ping Frame** 

|**Idle State**|**Preamble**|**SOF**|**Frame Type**|**Frame Tag**|**EOF**|**Postamble**|**Idle State**|
|---|---|---|---|---|---|---|---|
||1111|1001|0000|xxxx|0110|1111||



The ping frame type is always 0000. The frame tag is defined by the application. Separate frame tags exist for timer and software initiated ping frames. No data or CRC is transmitted in a ping frame. 

The main purpose of the ping frame is to periodically send a notification to the receiver to make sure an active connection between the transmitter and receiver. The transmitter and receiver cores implement different features to allow the ping frame to operate as a line break detect feature. 

On the transmitter, the ping frame is the only frame that can be set up and transmitted without any further software or DMA intervention. Ping frames can be transmitted by any (or all) of the three sources: automatic ping timer, software, or external triggers. See Section 7.5.9.3.2.3.3 for information on how the transmitter configures and sends the ping frames. 

The receiver has a ping watchdog that can detect if a ping frame has not been received in a predetermined window. This allows the receiver to know if the connection between the receiver and the transmitter has been broken. See Section 7.5.9.3.3.4 for information on how the receiver handles ping frames. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 873 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.9.3.4.2.2 Error Frames**_ 

Error frames are similar to ping frames in that there are no data fields transmitted. Despite the naming of this frame as an “error frame,” the usage of it is up to the application, as no restrictions are placed on how and when this type of frame is transmitted. Table 7-180 shows the structure of an error frame. 

## **Table 7-180. Error Frame** 

|**Idle State**|**Preamble**|**SOF**|**Frame Type**|**Frame Tag**|**EOF**|**Postamble**|**Idle State**|
|---|---|---|---|---|---|---|---|
||1111|1001|1111|xxxx|0110|1111||



The structure of the error frame is the same as a ping frame. No data or CRC values are transmitted. The frame type is 1111 for all error frames, and the frame tag is defined by software in the TX_FRAME_TAG_UDATA register. 

The receiver can detect if an error frame has been received based on the frame type field. Because of this, the receiver can read the incoming frame tag from the RX_FRAME_TAG_UDATA register and act on up to 16 different conditions. 

## _**7.5.9.3.4.2.3 Data Frames**_ 

Data frames are the most complex frames. As the name indicates, these frames are used to transfer data. Table 7-181 shows the general structure of data frames. 

## **Table 7-181. Data Frame** 

|**Idle State**|**Preamble**|**SOF**|**Frame**<br>**Type**|**User Data**|**Data**<br>**Words**|**CRC Byte**|**Frame Tag**|**EOF**|**Postamble**|**Idle State**|
|---|---|---|---|---|---|---|---|---|---|---|
||1111|1001|0xxx|xxxx xxxx|1-16 words|xxxx xxxx|xxxx|0110|1111||



The frame type field reflects the 4-bit code of the frame type. A list of frame types can be seen in Table 7-178. The number of the data words transmitted is determined by the frame type chosen. 

There are four fixed-length data frames supported by the frame type: 1 word, 2 words, 4 words, and 6 words. 

Additionally, there is a user-defined data length frame type where the number of data words is fixed by software. Anywhere from 1 to 16 words can be transmitted in this frame type. This length must be configured in the N_WORDS field of the transmitter’s TX_FRAME_CTRL register and receiver’s RX_OPER_CTRL register. 

## _**7.5.9.3.4.3 Multi-Lane Transmission**_ 

The FSI is capable of transmitting and receiving data on two parallel data lines. When enabled, data bits are split between the data lines while the start of frame, frame type, frame tag, and end of frame fields are identical and complete on each line. The user data, data, and CRC fields are split between the data lines. Starting with the most-significant bit, the odd-numbered bits appear on D0 and even-numbered bits appear on D1. 

In the following example, assume the following: 

8-bit user data: u7u6u5u4u3u2u1u0 

16-bit data: d15d14d13d12…d1d0 

8-bit CRC: c7c6c5c4c3c2c1c0 

**Table 7-182. Multi-Lane Frame Format** 

|**Idle State**|**Preamble**|**SOF**|**Frame**<br>**Type**|**User Data**|**Data**<br>**Words**|**CRC Byte **|**Frame Tag**|**EOF**|**Postamble**|**Idle State**|
|---|---|---|---|---|---|---|---|---|---|---|
|TXD0|1111|1001|0011|u7u5u3u1|d15d13…d1|c7c5c3c1|xxxx|0110|1111||
|TXD1|1111|1001|0011|u6u4u2u0|d14d12…d0|c6c4c2c0|xxxx|0110|1111||



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

874 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.5 Flush Sequence**_ 

Every time there is a soft reset of the receiver, the receiver requires a flush sequence from the transmitter before the receiver can receive and decode frames. The receiver core has an asynchronous reset mechanism that allows the receive module to be reset even in the absence of the receive clocks. However, due to the design, this reset is released synchronous to the receive clock (RXCLK). Thus, the receiver requires five full clock pulses to be able to come out of reset. Sending the flush pattern makes sure that these clock edges are received and any subsequent frames sent to the receiver are correctly interpreted. 

The flush sequence consists of a single toggle on both of the data lines as well as five consecutive pulses on the clock line. 

If the FSI receiver is receiving data from a standard SPI, a data word of 0xFFFF from the SPI has the same effect as a flush sequence. 

Figure 7-355 shows a sample plot of the flush sequence. 

**==> picture [421 x 90] intentionally omitted <==**

**----- Start of picture text -----**<br>
FSITXCLK<br>FSITXD0<br>FSITXD1<br>**----- End of picture text -----**<br>


**Figure 7-355. Flush Sequence Signals** 

## _**7.5.9.3.6 FSI Internal Loopback**_ 

The transmitter and receiver cores can be connected together internally to allow for development and debug. This is achieved by setting RX_MAIN_CTRL_ALTC_.INT_LOOPBACK to 1. Internal loopback routes the signals from the corresponding transmitter to the appropriate receiver pin. No configuration needs to be done in the transmitter. 

Figure 7-356 shows the signal connections with internal loopback. 

**==> picture [290 x 218] intentionally omitted <==**

**Figure 7-356. FSI with Internal Loopback** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

875 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-183. Loopback Connections** 

|**TX Module**|**RX Modules**|
|---|---|
|FSI0 TX|FSI0 RX|
|FSI1 TX|FSI1 RX|
|FSI2 TX|FSI2 RX|
|FSI3 TX|FSI3 RX|



## _**7.5.9.3.7 CRC Generation**_ 

The FSI uses CRC-8 with the polynomial 0x07 for the internal hardware CRC generation. This polynomial is also represented as x[8] +x[2] +x+1. 

For example, for a 2-word data packet the following calculation occurs: 

Data-1 = 0x4433 

Data-0 = 0x2211 

User Data = 0xAA 

The CRC is computed with the bytes being taken in the following order (first to last): 

0xAA – Byte 0, User Data 

0x11 – Byte 1, Data-0, Least-significant byte 

0x22 – Byte 2, Data-0, Most-significant byte 

- 0x33 – Byte 3, Data-1, Least-significant byte 

- 0x44 – Byte 4, Data-1, Most-significant byte 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

876 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.8 ECC Module**_ 

The FSI module comes with a 16-bit or 32-bit ECC computation module in both the transmitter and receiver. Use of this module is optional. 

Note that the ECC is independent and unrelated to the hardware CRC computation module present in both the transmitter and receiver cores. 

The following example shows a scenario in which the application requires ECC be calculated and transmitted on a 2-word data frame. 

In the FSITX module: 

1. Configure the ECC module for 32-bit data by setting TX_OPER_CTRL_HI_ALT1_.ECC_SEL to 1. 

2. Write the data to the TX_ECC_DATA register as well as the transmit buffer. 

3. Read TX_ECC_VAL Register. This register contains the 8-bit ECC value calculated on the data. 

4. Copy the 8-bit data from TX_ECC_VAL to TX_FRAME_TAG_UDATA.USER_DATA. 

5. Set the Start Condition to begin the transmission. 

The reverse process is followed on the FSIRX module. Once the data frame is received, user software can do the following: 

1. Copy the data from the receive buffer to the RX_ECC_DATA register. 

2. Copy the received user data that contains the transmitted ECC value from RX_FRAME_TAG_UDATA.USER_DATA to the RX_ECC_VAL register. 

3. Read the RX_ECC_LOG register. This contains the result of the ECC computation using the RX_ECC_DATA and RX_ECC_VAL registers. 

   - a. If no ECC errors were detected, RX_ECC_LOG is 0. The correct data is available in RX_ECC_SEC_DATA. 

   - b. If a single bit error was detected, RX_ECC_LOG.SBE is 1. The autocorrected data is available in RX_ECC_SEC_DATA. 

   - c. If multiple bit errors occurred, RX_ECC_LOG.MBE is 1. The data in RX_ECC_SEC_DATA is invalid and must not be used. 

Using a 2-word data frame plus using the user data for the ECC is one possible implementation for ECC detection. Another option is to use a larger data frame a allocate one of the data words to be the ECC value. 

## _**7.5.9.3.9 FSI Trigger Generation**_ 

The RX_TRIGx external trigger can be used to initiate FSITX transmission. RX_TRIG0 must be used if TDM mode (multi-node configuration) is required. RX_TRIG0 must be used as the trigger source for start of transmission while the programmable stretch width RX_TRIG0 signal is used as the SEL_TDM_PATH signal (which decides whether the local FSITX is active or put in bypass mode). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

877 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [406 x 342] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX_TRIG_CTRL_0<br>TRIG_SEL<br>RX Trigger Source<br>Select Signals TRIG_EN<br>PING_PKT_RCVD TRIG_DLY<br>DATA_PKT_RCVD Delay Trigger RX_TRIG_0<br>Other Sources<br>RX_TRIG_CTRL_1 RX_TRIG_1<br>RX_TRIG_CTRL_2 RX_TRIG_2<br>RX_TRIG_CTRL_3 RX_TRIG_3<br>EXT_TRIG_SEL<br>External Trigger Select<br>EPWM SOC<br>CLB<br>Other Sources<br>FSI TX Trigger<br>RX_TRIG_0<br>RX_TRIG_1 RX_TRIG_WIDTH_0<br>RX_TRIG_2 Stretch Width SEL_TDM_PATH<br>RX_TRIG_3<br>**----- End of picture text -----**<br>


**Figure 7-357. RX_TRIGx FSI Trigger** 

The signal source for the RX_TRIGx signal is selected through the RX_TRIG_CTRL_x.TRIG_SEL bits, as listed in Table 7-184. 

**Table 7-184. RX_TRIGx Trigger Select Signals** 

|**RX_TRIG_CTRLx.TRIG_SEL**|**Selected Signal**|
|---|---|
|0|Ping Packet Received|
|1|Data Packet Received|
|2|Error Packet Received|
|3|Ping Frame Tag Match Occurred|
|4|Data Frame Tag Match Occurred|
|5|Error Frame Tag Match Occurred|
|6|Frame Done|
|7|Reserved|
|8 to 15|Reserved|



The RX_TRIGx signals can optionally be delayed (this can be used in TDM scenarios) through the RX_TRIG_CTRL_x.TRIG_DLY. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

878 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.10 FSI-SPI Compatibility Mode**_ 

The FSI supports a SPI compatibility mode. While the FSI can communicate with a standard SPI module, the FSI supports a limited configuration. The features of this compatibility mode are: 

- Data transmits on rising edge and receive on falling edge of the clock. 

- Only 16-bit word size is supported. 

- TXD1 is driven like an active-low, chip-select signal. The signal is low for the duration for the full frame transmission. 

- No receiver chip-select input is required. RXD1 is not used. Data is shifted into the receiver on every active clock edge. 

- No preamble or postamble clocks are transmitted. All signals return to the IDLE state after the frame phase is finished. 

- It is not possible to transmit in the SPI peripheral configuration because the FSI TXCLK cannot take an external clock source. 

Table 7-185 lists the frame structure of the FSI-SPI compatibility mode. Each frame phase is present in this mode. If the FSI is transmitting to a standard SPI module, the SPI must decode the frame structure. Similarly, if the FSI is configured as a SPI peripheral, the standard SPI must encode the transmission to be sent. 

**Table 7-185. FSI-SPI Compatibility Frame Structure** 

|**Idle State**|**Start of**<br>**Frame**|**Frame Type**|**User Data**|**Data Words**|**CRC byte**(1)|**Frame Tag**|**End of**<br>**Frame**|**Idle State**|
|---|---|---|---|---|---|---|---|---|
||1001|4 bits|8 bits|1-16 words|8 bits|4 bits|0110||



(1) The CRC byte is present only in data frames. 

Because of the requirement that the standard SPI module encodes the various frame data, this limits the type of modules that can be connected to the FSI in SPI mode. The paired SPI module must have enough functionality to encode and decode the frames. 

If the FSI is transmitted to a standard 16-bit SPI, the data is arranged in the following manner. The example provided in Table 7-186 assumes a DATA_2_WORD frame has been sent. 

**Table 7-186. Contents of Data Received by a Standard SPI** 

|**SPI Data**|**Data Contents**|
|---|---|
|SPI word 0|1001, 0100, 8-bit User Data|
|SPI word 1|Data word 1|
|SPI word 2|Data word 2|
|SPI word 3|8-bit CRC, 4-bit Frame Tag, 0110|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 879 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.9.3.10.1 Available SPI Modes**_ 

There are a few wiring schemes available for the FSI to use when communicating with an SPI module. 

## _**7.5.9.3.10.1.1 FSITX as SPI Controller, Transmit Only**_ 

The FSITX can operate as an independent SPI controller module. In this condition, TXCLK is connected to SPICLK, TXD0 is connected to SPIPICO, and TXD1 is connected to SPIPTE , the chip select. 

**==> picture [324 x 109] intentionally omitted <==**

**----- Start of picture text -----**<br>
FSI TX SPI Peripheral<br>SPI Controller<br>Transmit<br>TXCLK SPICLK<br>TXD0 SPIPICO<br>TXD1 SPIPTE<br>**----- End of picture text -----**<br>


**Figure 7-358. FSITX as SPI Controller, Transmit Only** 

When the FSI is an SPI transmitter, the application has the ability to check for frame errors, line breaks, CRC errors, and ECC checks on data. These are all encoded by hardware in every FSI frame. The SPI receiver requires some software to act upon this information. 

**Table 7-187. FSI as Controller Transmitter, SPI as Peripheral Receiver** 

|**Capability**|**Availability**|**Comment**|
|---|---|---|
|Framing checks on the data frames|Yes|Can be implemented in software on the SPI receiver.|
|Ability to detect line breaks|Yes|Can be implemented in software on the SPI receiver but requires|
|||additional software overhead such as a timer or watchdog.|
|CRC check|Yes|Can be implemented in software on the SPI receiver. For devices|
|||that have , this is more efficient.|
|ECC on data|Yes|Can be implemented in software on the SPI receiver|
|Detection of abruptly terminated frames|No||
|Double edge data rate|No||
|Recovery from glitches on signal lines|No||
|between frames|||
|Skew adjustment on signal lines|No||



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

880 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.10.1.1.1 Initialization**_ 

To configure the FSITX module to be an SPI controller for transmit only, proceed through the standard FSITX initialization procedure. Before releasing the FSITX from reset, set TX_OPER_CTRL_LO_ALT2_.SPI_MODE to 1. This enables the SPI clocking scheme and signaling structure. 

## _**7.5.9.3.10.1.1.2 Operation**_ 

The operation of the FSITX module in FSI-SPI Compatibility mode is the same as if the module is in standard FSI mode. The application can utilize the frame timer, ping frames, external frame triggers, and so on. Refer to Section 7.5.9.3.2 for more information on each of these features. 

## _**7.5.9.3.10.1.2 FSIRX as SPI Peripheral, Receive Only**_ 

The FSIRX can operate as an independent SPI peripheral module. In this usage, RXCLK is connected to SPICLK and RXD0 is connected to SPIPICO. RXD1 is unused. There is no requirement for a chip select signal to be used when connected to the FSIRX. This is because the FSIRX responds to any incoming clock edge. If there is any noise or unwanted clock transitions, a flush sequence is required to resynchronize the FSIRX module with the controller. 

**==> picture [280 x 95] intentionally omitted <==**

**----- Start of picture text -----**<br>
FSI RX SPI Controller<br>SPI Peripheral<br>RXCLK SPICLK<br>RXD0 SPIPICO<br>RXD1<br>**----- End of picture text -----**<br>


**Figure 7-359. FSIRX as SPI Peripheral, Receive Only** 

When the FSI is an SPI receiver communicating with an SPI transmitter, the application has the ability to detect frame errors, line breaks, CRC errors, ECC checks on data, as well as abruptly terminated frames. Note that the FSI can handle all of this in hardware, but the SPI transmitter must encode the information into the data to be transmitted. 

**Table 7-188. SPI as Controller Transmitter, FSI as Peripheral Receiver** 

|**Capability**|**Availability**|**Comment**|
|---|---|---|
|Framing checks on the data frames|Yes|Standard on FSI|
|Ability to detect line breaks|Yes|Can be implemented in software on the SPI transmitter but requires|
|||the use of a timer or watchdog in the transmitting SPI device.|
|CRC check|Yes|Can be implemented in software on the SPI transmitter.|
|ECC on data|Yes|Can be implemented in software on the SPI transmitter.|
|Detection of abruptly terminated frames|Yes|This is accomplished with the FSI setting up the frame watchdog|
|||counter.|
|Double edge data rate|No||
|Recovery from glitches on signal lines|Yes|Whenever glitches occur on either the clock or data lines in between|
|between frames||transmissions, the initial flush pattern of a frame discards the effects|
|||of these glitches and causes the receiver to resynchronize when the|
|||real “start-of-frame” pattern is seen. So, the ability to reject glitches in|
|||between frames is very high.|
|Skew adjustment on signal lines|Yes|The FSI receiver has the ability to add delays to the incoming signal|
|||lines.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

881 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.9.3.10.1.2.1 Initialization**_ 

To configure the FSIRX module to be an SPI peripheral for receiving only, proceed through the standard FSIRX initialization procedure. Before releasing the FSIRX from reset, set RX_OPER_CTRL.SPI_MODE to 1. This enables the SPI clocking scheme and signaling structure. 

## _**7.5.9.3.10.1.2.2 Operation**_ 

The operation of the FSIRX module in FSI-SPI compatibility mode is the same as if the module is in standard FSI mode. The application can utilize the Frame and Ping Watchdogs, CRC and ECC checks, and so on. Refer to Section 7.5.9.3.3 for more information on each of these features. 

## _**7.5.9.3.10.1.3 FSITX and FSIRX Emulating a Full Duplex SPI Controller**_ 

In this configuration, the FSITX is the controller clock. The FSITX module drives TXCLK (SPICLK), TXD0 (SPIPICO), and TXD1 (SPISTE/chip select) to the SPI peripheral. The SPIPOCI signal is connected back to the RXD0 signal. RXCLK can be applied either using the internal SPI pairing feature or externally wired, depending on the application requirements. Since the FSITX and RX modules are independent, the FSIRX can also be thought of as an additional SPI peripheral. Some software logic is required for the FSI to emulate an SPI controller fully. 

**==> picture [324 x 222] intentionally omitted <==**

**----- Start of picture text -----**<br>
FSI TX SPI Peripheral<br>SPI Controller<br>Transmit<br>TXCLK SPICLK<br>TXD0 SPIPICO<br>SPIPOCI<br>TXD1 SPIPTE<br>FSI RX<br>SPI Controller<br>Receive<br>RXCLK<br>RXD0<br>RXD1<br>**----- End of picture text -----**<br>


**Figure 7-360. FSITX and FSIRX as SPI Controller, Full Duplex** 

## _**7.5.9.3.10.1.3.1 Initialization**_ 

To configure both FSITX and RX modules for full duplex SPI controller operation, follow the initialization instructions for each module described in the preceding sections. Both FSITX and RX modules must set their respective SPI_MODE bits. This enables the SPI clocking scheme and signaling structures. 

If internal clock loopback is desired, the FSIRX module must also set RX_MAIN_CTRL_ALTC_.SPI_PAIRING to 1. This internally connects TXCLK to RXCLK. If using internal clock loopback, the GPIO used for RXCLK can be reallocated to other application requirements. 

If the application requires an external clock loopback, make sure that TXCLK is connected to RXCLK. This is required if the SPI peripheral is across an isolation barrier and there is latency between TXCLK being launched and SPIPOCI data being received on RXD0. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

882 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.3.10.1.3.2 Operation**_ 

In this mode of operation, some higher level software must be written to emulate a full SPI controller module. There is no path for the transmit module to determine what the receive module received. Both the TX and RX modules are still able to utilize the various other features available, such as the ping frame timer, ping frame and frame watchdogs, CRC and ECC error checkers, and so on. The procedure for configuring these features is described elsewhere in this document. 

## **7.5.9.4 FSI Programming Guide** 

This section describes various operational sequences and features for the FSI. 

## _**7.5.9.4.1 Establishing the Communication Link**_ 

Once the transmitter and receiver modules have been configured, some synchronization must occur before the modules exchange data. Since the receiver accepts data on any clock transition, the receiver core logic must be flushed to properly interpret the start of a new, valid frame. This is especially true when the FSI modules reside on separate devices and are possibly isolated. 

The following example provides a suggested approach for establishing a clean communication link on two separate devices that power up in an arbitrary order. Note that this is only a sample synchronization. Depending on application requirements, a different approach can be followed. The single, most important aspect of synchronization is to make sure that the receiver is properly flushed and ready to receive a complete frame without error. How to achieve this is up to the application. 

Figure 7-361 shows the connection of the devices in this example. While there is no true concept of a main device or a remote device node in the FSI protocol, the example uses this nomenclature as a simple way to describe the data flow. 

**==> picture [354 x 120] intentionally omitted <==**

**----- Start of picture text -----**<br>
FSI TX FSI RX<br>Device 1  Device 2<br>(Main) (Remote Peripheral)<br>FSI RX FSI TX<br>Isolator<br>**----- End of picture text -----**<br>


**Figure 7-361. Point to Point Connection** 

Device 1 is the main node; it is the driver of the initialization sequence. Device 2 is the remote node; it responds to the main device commands. In this example, as well as in a real world use-case, neither the main device nor the remote device knows precisely when the other is ready to receive communication. 

Sample sequences for both the main device and remote device are provided in the following subsections. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 883 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.9.4.1.1 Establishing the Communication Link from the Main Device**_ 

The following sequence is an example of how the main device node establishes the communication link with the remote device without external signals outside of the standard communication link. 

1. Assert the core reset to both the FSITX and FSIRX modules, and then deassert the resets. 

2. Configure the transmitter and receiver for desired operation. 

3. Set up the receiver interrupts to detect an incoming transmission. 

4. Begin the ping loop: 

   - Send the flush sequence. 

   - Send a ping frame with the frame tag 0000. 

   - Wait for some time. (determined by application) 

   - If the FSIRX has received a valid ping frame, continue; else iterate the loop again. 

   - If the received ping frame tag was 0001, continue; else iterate the loop again. 

5. Send a ping frame with the frame tag 0001. 

At this point, both the main transmit and receive channels have successfully received a frame from their remote counterparts. The link has been established and standard application communication can begin. 

## _**7.5.9.4.1.2 Establishing the Communication Link from the Remote Device**_ 

The following sequence is an example of how the remote device node establishes the communication link with the main device without external signals outside of the standard communication link. 

1. Apply the core reset to both the FSITX and FSIRX modules, and then release the reset. 

2. Configure the transmitter and receiver for desired operation. 

3. Set up the receiver interrupts to detect an incoming transmission. 

4. Wait for a receiver interrupt. 

5. If the FSIRX has received a valid ping frame, continue; else return to step 4. 

6. If the received frame tag was 0000, continue; else discard the transmission and return to step 4. 7. Send the flush sequence. 

8. Send a ping frame with the frame tag 0001. 

9. Wait for a receiver interrupt. 

10. If the FSIRX has received a valid ping frame, continue; else return to step 4. 

11. If the received ping frame tag was 0001, continue; else if the received frame tag was 0000, return to step 9. This can happen if a second ping frame was already in transit before receiving the remote device response in step 8. 

At this point, both the transmit and receive modules have successfully received ping frames from their main counterparts. The link has been established and regular communication can now proceed. The application can configure periodic ping frames from the transmitter, initialize the receiver ping and frame watchdogs, and begin the communication required by the application. 

884 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.9.4.2 Register Protection**_ 

Both the FSITX and FSIRX modules contain control registers that have embedded write protection. This is accomplished through register keys and a main register lock. These protections make sure that no spurious writes or unintentional modifications to these registers are accepted. . 

## **Register Key Protection** 

bits in the FSI registers are protected by a key. To write to these bits, the key must be written at the same time. For example, to put the transmitter core into reset, TX_MAIN_CTRL.CORE_RST must be set. To do this, write 0xA501 to TX_MAIN_CTRL, where 0xA500 is the KEY value, and 0x0001 is the CORE_RST value. Refer to the _Registers_ section for more information on which registers have write keys added. 

## **Control Register Lock Protection** 

There also exists a main lock to prevent any modifications to the control registers. There is an independent lock for each FSI module. For the list of registers that are protected by this control register lock, refer to the _Registers_ section. The control register lock prevents any writes to the control registers until the lock is released. To set the control register lock, write 0xA501 to RX_LOCK_CTRL and TX_LOCK_CTRL for the receiver and transmitter, respectively. 

The control register lock cannot be disabled by the application until a SYSRSn has been asserted. This can occur at the device level, or by writing to the appropriate peripheral soft reset register (DEV_CFG_REGS.SOFTPRESx) for the FSI module. 

## _**7.5.9.4.3 Emulation Mode**_ 

There is no specific emulation mode or configuration supported. The FSI cores are always in free running mode. CPU halts do not have any effect on the operation of the FSI. Reads of registers and data buffers by the debugger do not affect any flags or status of the data buffers. 

If you want to stop the operation of either FSI module when the debugger halts, the following steps are required: 

1. Set the debugger to real-time emulation mode. 

2. Mark the FSI interrupt group as a time-critical interrupt. That is, enable the corresponding bit in the DBGIER register. 

3. The ISR can check the DSTAT register and to determine if the ISR was called when the debugger was halted. 

4. FSI operations can be disabled and the ISR can branch to a debug-specific halt location. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

885 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.10 Sigma Delta Filter Module (SDFM)**_ 

The sigma delta filter module (SDFM) is a four-channel digital filter designed specifically for current measurement and resolver position decoding in motor control applications. Each input channel can receive an independent delta-sigma (ΔΣ) modulator bit stream. The bit streams are processed by four individuallyprogrammable digital decimation filters. The filter set includes a fast comparator (secondary filter) for immediate digital threshold comparisons for over-current and under-current monitoring, and zeros crossing detection. 

**7.5.10.1 Introduction** ................................................................................................................................................887 **7.5.10.2 SDFM Integration** .......................................................................................................................................891 **7.5.10.3 Configuring Device Pins** ...........................................................................................................................893 **7.5.10.4 Input Qualification** .....................................................................................................................................894 **7.5.10.5 Input Control Unit** ......................................................................................................................................895 **7.5.10.6 SDFM Clock Control** ..................................................................................................................................895 **7.5.10.7 Sinc Filter** ................................................................................................................................................... 896 **7.5.10.8 Data (Primary) Filter Unit** .......................................................................................................................... 899 **7.5.10.9 Comparator (Secondary) Filter Unit** ........................................................................................................ 904 **7.5.10.10 Theoretical SDFM Filter Output** ..............................................................................................................910 **7.5.10.11 Interrupt Unit** ............................................................................................................................................912 **7.5.10.12 SDFM Programming Guide** .....................................................................................................................914 

886 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.10.1 Introduction** 

Figure 7-362 shows the SDFM CPU Interface. 

**==> picture [419 x 263] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDyFLTxDRINT<br>SOCA/B<br>SDyERR<br>SDyFLTxDRINT<br>SDFM<br>SDyFLTxCMPH<br>SDyFLTxCMPL<br>SDyFLTxCMPHZ<br>GLOBAL_CTRL<br>SDFM1_CLK0_SEL<br>SDy-D[0:3] SDy-CLK[1:3] SD0_CLK0 SD1_CLK0<br>GPIO/PINMUX<br>EPWMy INT  XBAR<br>DMA  XBAR<br>R5FSS<br>ECAP,<br>Registers<br>OUTPUTXBAR  & PWMXBAR<br>**----- End of picture text -----**<br>


**Figure 7-362. Sigma Delta Filter Module (SDFM) CPU Interface** 

## **Note** 

For this image and all images in _Sigma Delta Filter Module (SDFM)_ , x represents 1-4 and y stands for SDFM1 and SDFM2. 

## **Note** 

The SDFM Data signals are enumerated as SDFM_D[0:3] while the corresponding registers are enumerated as [1:4]. 

## **Note** 

SDFM1_CLK0_SEL signal is controlled by register in Global Control Register Space 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 887 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.10.1.1 Features**_ 

SDFM features include: 

- Eight external pins per SDFM module 

   - 

      - Four sigma-delta data input pins per SDFM module (SDFMy_Dx, where x = 0 to 3) 

   - Four sigma-delta clock input pins per SDFM module (SDFMy_CLKx where x = 0 to 3) 

- Modulator clock rate equals the modulator data rate 

- Four independent, configurable secondary filter (comparator) units per SDFM module: 

   - 

   - Four different filter type selection (Sinc1/Sinc2/SincFast/Sinc3) options available 

- Ability to detect over-value condition, under-value condition, and Threshold-crossing conditions 

   1. Two independent Higher Threshold comparators (used to detect over-value condition) 

   2. Two independent Lower Threshold comparators (used to detect under-value condition) 

   3. One independent Threshold-Crossing comparator (used to measure duty cycle/frequency with eCAP) 

- 

      - OSR value for comparator filter unit (COSR) programmable from 1 to 32 

- Four independent configurable primary filter (data filter) units per SDFM module: 

   - 

   - Four different filter type selection (Sinc1/Sinc2/SincFast/Sinc3) options available 

- OSR value for data filter unit (DOSR) programmable from 1 to 256 

- 

      - Ability to enable or disable (or both) individual filter module 

   - Ability to synchronize all four independent filters of an SDFM module by using the Main Filter Enable (MFE) bit or by using PWM signals 

- Data filter output can be represented in either 16 bits or 32 bits. 

- Data filter unit has a programmable mode FIFO to reduce interrupt overhead. The FIFO has the following features: 

   - The primary filter (data filter) has a 16-deep x 32-bit FIFO. 

   - The FIFO can interrupt the CPU after programmable number of data-ready events. 

   - FIFO Wait-for-Sync feature: Ability to ignore data-ready events until the PWM synchronization signal (SDSYNC) is received. Once the SDSYNC event is received, the FIFO is populated on every data-ready event. 

   - Data filter output can be represented in either 16 bits or 32 bits. 

- PWMx.SOCA/SOCB can be configured to serve as SDSYNC source on a per-data-filter-channel basis. 

- Configurable Input Qualification available for both SDFMy-CLKx and SDFMy-Dx 

- Ability to use one filter channel clock (SDFMy-CLK0) to provide clock to other filter clock channels. 

- Configurable digital filter available on comparator filter events to blankout comparator events caused by spurious noise 

888 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.10.1.2 Block Diagram**_ 

Each SDFM module has four independent filter modules. These filter modules are identical and can be configured independently. Each individual filter module has the following units: 

- Input control unit 

- Primary filter (data filter) unit 

- Secondary filter (comparator filter) unit with 4 independent comparators 

Figure 7-363 shows the SDFM module block diagram. The SDFM port operation is configured and controlled by the registers listed in the _SDFM Registers_ section of the Register Addendum. 

**==> picture [500 x 277] intentionally omitted <==**

**Figure 7-363. SDFM Integration Diagram** 

- A. The Enumeration shown has each SDFM data and clock signal as [1:4]. The signal naming in the AM263Px data sheet for these signals is [0:3] and maps accordingly. 

Each filter module shown in Figure 7-364 has a primary (data) filter and a secondary (comparator) filter pair that receives the same bit stream. Except for the input bit stream, both the primary and secondary filter are completely independent of each other. Each of these filter modules can be independently configured. So, in a SDFM module, there is a total of four primary filters and four secondary filters. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 889 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [486 x 409] intentionally omitted <==**

**----- Start of picture text -----**<br>
Comparator Filter Unit COMPHZ<br>HTLZ<br>COMPH1<br>HTL1<br>SINCx COMPH2<br>HTL2<br>COMPL1<br>LLT1<br>COMPL2<br>LLT2<br>SDCDATAx<br>Input Control Unit<br>Data Filter Unit<br>SDDATAx<br>SINCx Data<br>SDFMy_Dx<br>Shift<br>Decoding<br>SDFMy_CLKx<br>FIFO<br>SDSYNC DRINT (Data Ready)<br>SDSYNC<br>SYSCLK SDDATFIFOx<br>WTSYNCEN<br>PWM SDDFPARM.SDSYNCEN<br>LEGEND<br>Interrupt / trigger sources from SDFM<br>Internal secondary filter signals<br>**----- End of picture text -----**<br>


**Figure 7-364. Block Diagram of One Filter Module** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

890 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.10.2 SDFM Integration** 

There are 4x SDFM modules integrated in the CONTROLSS. The diagrams below provides a visual representation of the device integration details. 

**==> picture [419 x 263] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDyFLTxDRINT<br>SOCA/B<br>SDyERR<br>SDyFLTxDRINT<br>SDFM<br>SDyFLTxCMPH<br>SDyFLTxCMPL<br>SDyFLTxCMPHZ<br>GLOBAL_CTRL<br>SDFM1_CLK0_SEL<br>SDy-D[0:3] SDy-CLK[1:3] SD0_CLK0 SD1_CLK0<br>GPIO/PINMUX<br>EPWMy INT  XBAR<br>DMA  XBAR<br>R5FSS<br>ECAP,<br>Registers<br>OUTPUTXBAR  & PWMXBAR<br>**----- End of picture text -----**<br>


**Figure 7-365. SDFM Integration Diagram (Simple)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 891 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 255] intentionally omitted <==**

**Figure 7-366. SDFM Integration Diagram (Detailed)** 

892 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.10.3 Configuring Device Pins** 

For proper SDFM operation, use the following GPIO input qualification. Other GPIO qualifications are not supported. 

- GPIO Input qualification is ASYNC, make sure to check the SDFM Electrical Data and Timing (Using ASYNC) requirement is met and be aware of the following caution message. SDFM Input Qualification feature is used to provide protection against random noise glitches. 

## **CAUTION** 

The SDFM clock inputs (SDFMy_CLKy pins) directly clock the SDFM module. Any glitches or ringing noise on these inputs can corrupt the SDFM module operation. Special precautions must be taken on these signals to make sure of a clean and noise-free signal that meets SDFM timing requirements. Precautions such as series termination for ringing due to any impedance mismatch of the clock driver and spacing of traces from other noisy signals are recommended. 

## **Note** 

The SDFM module expects SDFMy-Dx to change on the falling edge of SDFMy_CLKx and strobes for SDFMy-Dx on the rising edge. But some SD-modulators in the market change SDFMy-Dx on the rising edge and expect SDFM to strobe for data on the falling edge. In such cases, the GPIO inversion feature (GPxINV) is used on SDFMy-CLKx pin to change polarity and make it compatible with the SDFM. 

See the _General-Purpose Input/Output (GPIO)_ chapter for more details on GPIO mux and settings. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

893 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.10.4 Input Qualification** 

Impulse noise sources such as EMI, crosstalk, and so on, has the possibility of corrupting SDCLK and SDDATA bit streams, resulting in corrupted SDFM filtered data. This impulse noise effects can be mitigated when using the input qualification feature that synchronizes SDCLK/SDDATA signals with PLLCLK. By default, both SDCLK and SDDATA bit stream are not synchronized. SDCLK can be synchronized to PLLCLK by setting SDCTLPARMx.SDCLKSYNC = 1 and SDDATA can be synchronized to PLLCLK by setting SDCTLPARMx.SDDATASYNC = 1. Figure 7-367 shows optional Input Qualification option on SDCLK and SDDATA lines. 

**==> picture [484 x 261] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDFMy_CLKx to Input<br>Control Unit<br>Synchronized SDFMy_CLKx<br>SDFMy_CLKx SYNC<br>SDCTLPRMx.SDCLKSYNC<br>SDFMy_Dx to Input<br>Control Unit<br>Synchronized SDFMy_Dx<br>SDFMy_Dx SYNC<br>SDCTLPRMx.SDDATASYNC<br>**----- End of picture text -----**<br>


**Figure 7-367. Input Qualification on SDFMy-CLKx and SDFMy-Dx** 

## **Note** 

SDFM PLL clock needs to be configured in case synchronizers inside SDFM are used. 

894 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.10.5 Input Control Unit** 

The input control unit receives sigma delta modulated data and a sigma delta modulated clock. The modulated data received is captured and passed on to the data filter unit and comparator unit. This unit can be configured to receive the modulated data in only mode 0. Table 7-189 and Figure 7-368 show how SDCTLPARMx.MOD bits can be configured in mode 0. 

## **Table 7-189. Modulator Clock Modes** 

|**Modulator Mode [MOD]**|**Description**|
|---|---|
|0|The modulator clock is running with the modulator data rate. The modulator data is strobed|
||at every rising edge of the modulator clock.|
|1|Reserved|
|2|Reserved|
|3|Reserved|



## **Note** 

To achieve the maximum value, the sigma-delta modulator has to be operated at absolute maximum positive or negative full scale, which is outside of the recommended full scale range of 80% of most sigma-delta modulators. 

**==> picture [500 x 111] intentionally omitted <==**

**Figure 7-368. Different Modulator Modes Supported** 

## **7.5.10.6 SDFM Clock Control** 

In systems, the modulator clock can be generated using PWMs. Assuming all the SD-CLKs see the same delay on board traces, you can potentially use just one clock to clock multiple filters; thereby, saving on the number of pins used for SDFM. To enable this, Filter1 SDCLK (SDFM-CLK0) can possibly apply to other filter channels if required. The SDCTLPARAMx.SDCLKSEL register bit field can be configured to select filter channel SDCLK. It is also possible to drive SD0 FILTER0 clock from the pinmux to SD1 FILTER0 by configuring CONTROLSS_CTRL.SDFM1_CLK0_SEL. See Figure 7-369 to view this feature. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 895 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

|SDFM0_CLK0<br>SDFM0_D0<br>SDFM0_CLK1<br>SDFM0_D1<br>SDFM0_CLK2<br>SDFM0_D2<br>SDFM0_CLK3<br>SDFM0_D3<br>SDFM1_CLK0<br>SDFM1_D0<br>SDFM1_CLK1<br>SDFM1_D1<br>SDFM1_CLK2<br>SDFM1_D2<br>SDFM1_CLK3<br>SDFM1_D3|||||SDFM0<br>SD Filter 0<br>CLK0<br>D0<br>CLK1<br>SD Filter 1<br>SD Filter 2<br>SD Filter 3<br>SDCLKSEL<br>D1<br>CLK2<br>SDCLKSEL<br>D2<br>CLK3<br>SDCLKSEL<br>D3|
|---|---|---|---|---|---|
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
||||||SDFM1<br>SD Filter 0<br>CLK0<br>D0<br>CLK1<br>SD Filter 1<br>SD Filter 2<br>SD Filter 3<br>SDCLKSEL<br>D1<br>CLK2<br>SDCLKSEL<br>D2<br>CLK3<br>SDCLKSEL<br>D3|
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||
|||||||



**Figure 7-369. SDFM Clock Control** 

## **7.5.10.7 Sinc Filter** 

Both the comparator filter and data filter available in SDFM have the Sinc[N] filter as the core. The Sinc[N] filter is essentially a low-pass filter that converts the input bit stream into digital data by digital filtering and decimation. This filtered digital data represents analog input given to the sigma delta modulator. Simplified Sinc[N] architecture consists of cascaded integrators and differentiators separated by a down-sampler as shown in Figure 7-370. The Z-transfer function of the Sinc filter of order N is shown in Figure 7-371. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

896 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [414 x 76] intentionally omitted <==**

**----- Start of picture text -----**<br>
Integrator Differentiator<br>Input digital bit-stream N N Filtered Digital data<br>OSR 1- Z [-1]<br>1<br>1- Z [-1]<br>**----- End of picture text -----**<br>


**Figure 7-370. Simplified Sinc Filter Architecture** 

**==> picture [131 x 100] intentionally omitted <==**

**----- Start of picture text -----**<br>
N<br>1- Z [-OSR]<br>H(Z) =<br>1- Z [-1]<br>N     = Order of Sinc filter<br>OSR = Over Sampling Ratio<br>**----- End of picture text -----**<br>


**Figure 7-371. Z-Transform of Sinc Filter of Order N** 

Effective resolution of the Sinc filter (ENOB) depends upon filter type, OSR and sigma-delta modulator frequency. Typically, higher resolution or ENOB can be achieved by higher OSR for a given filter type; however, the tradeoff is increased filter delay. It is important to choose the right sigma delta modulator by studying the optimal speed versus resolution tradeoff. Refer to the corresponding sigma delta modulator data sheet to determine the effective resolution for a given Sinc filter configuration. Figure 7-372 shows the frequency response of different filter structures when OSR = 32 and when the sigma delta modulator frequency is 10 MHz. 

**==> picture [360 x 239] intentionally omitted <==**

**Figure 7-372. Frequency Response of Different Sinc Filters** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

897 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

The order of different sinc filter is shown in Table 7-190. 

**Table 7-190. Order of Sinc Filter** 

|**Filter Type**|**Order of Sinc Filter**|
|---|---|
|Sinc1|1|
|Sinc2|2|
|Sinc3|3|
|SincFast|3|



## _**7.5.10.7.1 Data Rate and Latency of the Sinc Filter**_ 

The data rate of the sinc filter (filter throughput) represented in samples/sec is calculated by the following formula: 

_Modulator data rate Data rate of Sinc filter_ � _OSR_ (17) 

The latency of the sinc filter represented in secs is defined as the amount of time taken by a sinc filter type to deliver the correct filtered output upon initiation. For a given filter type, latency is calculated by the following formula: 

_Order of Sinc filter Latency of Sinc filter_ � _Data rate of Sinc filter_ 

**==> picture [19 x 11] intentionally omitted <==**

## _**Example configuration:**_ 

Sinc filter type = sinc3 Modulator data rate = 10 MHz OSR = 256 Data rate of Sinc Filter = 10 MHz / 256 = 39.1 K samples / sec Sinc filter latency = 76.8 µs Sinc filter type = sinc2 Modulator data rate = 10 MHz OSR = 256 Data rate of Sinc Filter = 10 MHz / 256 = 39.1 K samples / sec Sinc filter latency =51.2 µs 

898 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.10.8 Data (Primary) Filter Unit** 

The data filter is a configurable Sinc filter which supports the following filter types: Sinc1, Sinc2, Sinc3, and SincFast. The data filter OSR (DOSR) settings can be configured from 1 to 256 and is independent of the comparator filter. Effective resolution of the data filter (ENOB) depends upon Data filter type, DOSR, and sigma-delta modulator frequency. By default, the data filter is disabled and setting of SDDFPARMx.FEN = 1 enables the data filter. The data filter output is represented in 26-bit signed integer in two’s complement format. This filter unit translates a low input signal as ‘-1’ and a high input signal as ‘1’. The resulting calculation gives both positive and negative values for the output of the data filter. Table 7-191 shows the different full scale values that the data filter can store using different OSRs. 

See Section 7.5.10.7.1 to understand how to calculate data rate and latency of data filter. 

**Table 7-191. Peak Data Values for Different DOSR/Filter Combinations** 

|**DOSR**|**Sinc1**|**Sinc2**|**Sinc3**|**SincFast**|
|---|---|---|---|---|
|x|x|x2|x3|2x2|
|4|–4 to 4|–16 to 16|–64 to 64|–32 to 32|
|8|–8 to 8|–64 to 64|–512 to 512|–128 to 128|
|16|–16 to 16|–256 to 256|–4096 to 4096|–512 to 512|
|32|–32 to 32|–1024 to 1024|–32,768 to 32,768|–2048 to 2048|
|64|–64 to 64|–4096 to 4096|–262,144 to 262,144|–8192 to 8192|
|128|–128 to 128|–16,384 to 16,384|–2,097,152 to 2,097,152|–32,768 to 32,768|
|256|–256 to 256|–65,536 to 65,536|–16,777,216 to 16,777,216|–131,072 to 131,072|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

899 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.10.8.1 32-bit or 16-bit Data Filter Output Representation**_ 

The data filter output can be represented in either 32-bit or 16-bit format. 

## **32-bit data filter representation:** 

- When SDDPARMx.DR = 1, data filter output is represented in 32-bit format. Writes to shift control bits do not have any bearing on the output of the data filter in this configuration. 

## **16-bit data filter representation:** 

- By default, data filter output is represented in 16-bit format 

- When SDDPARMx.DR = 0, data filter output is represented in 16-bit format. But it is the responsibility of the user to configure the corresponding shift control bits in the SDDPARMx register to control which 16-bit part of the 32-bit word is sent to the register map. 

For example, for the data filter configuration below: 

- Filter type = Sinc3 

- OSR = 128 

- SDDPARMx.DR = 0 

The data filter with a 26-bit signed output value can be in the range of –16,777,216 to 16,777,216. But, 16-bit signed output supports values only from –32,768 to 32,767. Therefore, it is required to configure shift control bits (SDDPARMx.SH) to 7 to represent the data filter output correctly in 16-bit format. Table 7-192 shows the configuration settings of shift control bits for different OSR and filter types. 

**Table 7-192. Shift Control Bit Configuration Settings** 

|**OSR**|**Sinc1**|**Sinc2**|**SincFast**|**Sinc3**|
|---|---|---|---|---|
|1 to 31|0|0|0|0|
|32 to 40|0|0|0|1|
|41 to 50|0|0|0|2|
|51 to 63|0|0|0|3|
|64 to 80|0|0|0|4|
|81 to 101|0|0|0|5|
|102 to 127|0|0|0|6|
|128 to 161|0|0|1|7|
|162 to 181|0|0|1|8|
|182 to 203|0|1|2|8|
|204 to 255|0|1|2|9|
|256|0|2|3|10|



## **CAUTION** 

Configuring shift control bits incorrectly results in getting an incorrect 16-bit data filter output. 

## _**7.5.10.8.2 Data FIFO**_ 

Each primary (data) filter channel has a 16-level deep, 32-bit FIFO. 

FIFOs can be configured to collect a programmable number of data filter samples before issuing data-ready interrupt. This reduces the number of data-ready interrupts generated and resulting interrupt overhead for managed data flow. 

By default, FIFO operation is disabled. FIFOs can be enabled by setting SDFIFOCTLx.FFEN = 1. When FIFO is enabled, each data-ready event from the data filter populates the FIFO, and the status of the FIFO at any given time is updated in the SDFIFOCTLx.SDFFST bit field. 

900 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **Setting up FIFO to interrupt after receiving programmable number of data ready events:** 

- Enable SDFM FIFO (Set SDFIFOCTLx.FFEN = 1) 

- Enable SDFM FIFO interrupt (Set SDFIFOCTLx.FFIEN = 1) 

- Configure SDFIFOCTLx.SDFFIL bit field to any value between 0 to 16 

- Configure SDFM data ready event to interrupt on FIFO interrupt (SDFFINT) (Set SDFFINTx = 1) 

- Select data-ready interrupt source is SDFFINTx (DRINTx = SDFFINTx) (SDFIFOCTLx.DRINTSEL = 1) 

When the SDFIFOCTLx.SDFFST >= SDFIFOCTLx.SDFFIL condition is met, the SDIFLG.SDFFINTx bit is set and an interrupt is generated on the DRINTx. SDIFLG.SDFFINTx flag can be cleared by setting the SDIFLGCLR. SDFFINTx bit field. 

## **Wait for Sync feature:** 

The FIFO wait for sync feature can be used to ignore data-ready events from the data filter until the SDSYNC (from PWM) event is triggered. 

By default, the Wait for Sync feature is disabled. This feature can be enabled by setting SDSYNCx.WTSYNCEN = 1 

## **When the wait for sync feature is disabled:** 

FIFOs get populated on every data ready event until the FIFO gets full (or) when SDFIFOCTLx.SDFFST >= SDFIFOCTLx.SDFFIL. 

## **When the wait for sync feature enabled:** 

FIFOs do not get populated on every data ready event until the FIFO receives a SDSYNC event. On a SYSYNC event, the FIFO sets SDSYNCx.WTSYNFLG = 1 and data ready events from the primary filter start populating the FIFO until either the FIFOs get full or when SDFIFOCTLx.SDFFST >= SDFIFOCTLx.SDFFIL. WTSYNFLG can be cleared either automatically or manually. 

When WTSYNFLG = 0, FIFOs contents are frozen and subsequent data ready events do not populate FIFO until next SDSYNC event. 

## **WTSYNFLG automatic clear mode:** 

By default, this mode is enabled. When SDSYNCx.WTSCLREN = 1, WTSYNFLG is automatically cleared on SDFFINT event. 

## **WTSYNFLG manual clear mode:** 

Setting SDSYNCx.WTSYNCLR = 1 can be used to clear WTSYNFLG manually. 

## **Clearing FIFO contents:** 

FIFO contents can cleared by any of the following methods:- 

- Disabling FIFO clear FIFO contents. This can be done by clearing SDFIFOCTLx.FFEN = 0. 

- Disabling Primary filter clear FIFO contents. This can done by either clearing SDDFPARMx.FEN = 0 (or) by clearing SDMFILEN.MFE = 0. 

- FIFO contents can also be automatically cleared upon receiving the SDSYNC event. By default, this feature is disabled and this feature can be enabled by setting FIFO Clear-on-SDSYNC enable (SDSYNCx.FFSYNCCLREN = 1). 

**Note:** The above feature is only enabled when wait for sync feature is enabled (SDSYNCx. WTSYNCEN = 1). 

## **FIFO debug access behavior:** 

Debug access of the SDDATFIFOx registers does not affect the FIFO pointers. On a CPU/RTDMA access to the SDDATFIFOx register, the FIFO read pointers advance to the next available entry in the FIFO. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 901 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.10.8.3 SDSYNC Event**_ 

Primary (data) filters can be synchronized with respect to the PWM event (called SDSYNC event). The SDSYNC signal from the PWM module is used to reset the DOSR counter. This feature is by default disabled and can be enabled by setting SDDFPARMx.SDSYNCEN = 1. Each primary filter can be synchronized from any of the available PWMx SOCA/SOCB signals. The SDSYNCx.SDSYNCSEL bits allow the user to configure which PWM signal provides the SDSYNC pulse to the primary filter. Figure 7-373 shows how device PWM signals are connected to the SDFM modules. 

**Table 7-193. SDSYNCx.SYNCSEL** 

|**SYNCSEL[5:0]**|**SDSYNCx.SYNCSEL[5:0]**|**SDSYNCx.SYNCSEL[5:0]**|**SDSYNCx.SYNCSEL[5:0]**|**SDSYNCx.SYNCSEL[5:0]**|
|---|---|---|---|---|
||**1**|**2**|**3**|**4**|
|0|PWM0.SOCA|PWM0.SOCA|PWM0.SOCA|PWM0.SOCA|
|1|PWM0.SOCB|PWM0.SOCB|PWM0.SOCB|PWM0.SOCB|
|2|PWM1.SOCA|PWM1.SOCA|PWM1.SOCA|PWM1.SOCA|
|3|PWM1.SOCB|PWM1.SOCB|PWM1.SOCB|PWM1.SOCB|
|4|PWM2.SOCA|PWM2.SOCA|PWM2.SOCA|PWM2.SOCA|
|5|PWM2.SOCB|PWM2.SOCB|PWM2.SOCB|PWM2.SOCB|
|6|PWM3.SOCA|PWM3.SOCA|PWM3.SOCA|PWM3.SOCA|
|7|PWM3.SOCB|PWM3.SOCB|PWM3.SOCB|PWM3.SOCB|
|8|PWM4.SOCA|PWM4.SOCA|PWM4.SOCA|PWM4.SOCA|
|9|PWM4.SOCB|PWM4.SOCB|PWM4.SOCB|PWM4.SOCB|
|10|PWM5.SOCA|PWM5.SOCA|PWM5.SOCA|PWM5.SOCA|
|11|PWM5.SOCB|PWM5.SOCB|PWM5.SOCB|PWM5.SOCB|
|12|PWM6.SOCA|PWM6.SOCA|PWM6.SOCA|PWM6.SOCA|
|13|PWM6.SOCB|PWM6.SOCB|PWM6.SOCB|PWM6.SOCB|
|14|PWM7.SOCA|PWM7.SOCA|PWM7.SOCA|PWM7.SOCA|
|15|PWM7.SOCB|PWM7.SOCB|PWM7.SOCB|PWM7.SOCB|
|16|PWM8.SOCA|PWM8.SOCA|PWM8.SOCA|PWM8.SOCA|
|17|PWM8.SOCB|PWM8.SOCB|PWM8.SOCB|PWM8.SOCB|
|18|PWM9.SOCA|PWM9.SOCA|PWM9.SOCA|PWM9.SOCA|
|19|PWM9.SOCB|PWM9.SOCB|PWM9.SOCB|PWM9.SOCB|
|20|PWM10.SOCA|PWM10.SOCA|PWM10.SOCA|PWM10.SOCA|
|21|PWM10.SOCB|PWM10.SOCB|PWM10.SOCB|PWM10.SOCB|
|22|PWM11.SOCA|PWM11.SOCA|PWM11.SOCA|PWM11.SOCA|
|23|PWM11.SOCB|PWM11.SOCB|PWM11.SOCB|PWM11.SOCB|
|24|PWM12.SOCA|PWM12.SOCA|PWM12.SOCA|PWM12.SOCA|
|25|PWM12.SOCB|PWM12.SOCB|PWM12.SOCB|PWM12.SOCB|
|26|PWM13.SOCA|PWM13.SOCA|PWM13.SOCA|PWM13.SOCA|
|27|PWM13.SOCB|PWM13.SOCB|PWM13.SOCB|PWM13.SOCB|
|28|PWM14.SOCA|PWM14.SOCA|PWM14.SOCA|PWM14.SOCA|
|29|PWM14.SOCB|PWM14.SOCB|PWM14.SOCB|PWM14.SOCB|
|30|PWM15.SOCA|PWM15.SOCA|PWM15.SOCA|PWM15.SOCA|
|31|PWM15.SOCB|PWM15.SOCB|PWM15.SOCB|PWM15.SOCB|
|32|PWM16.SOCA|PWM16.SOCA|PWM16.SOCA|PWM16.SOCA|
|33|PWM16.SOCB|PWM16.SOCB|PWM16.SOCB|PWM16.SOCB|
|34|PWM17.SOCA|PWM17.SOCA|PWM17.SOCA|PWM17.SOCA|
|35|PWM17.SOCB|PWM17.SOCB|PWM17.SOCB|PWM17.SOCB|
|36|PWM18.SOCA|PWM18.SOCA|PWM18.SOCA|PWM18.SOCA|



902 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-193. SDSYNCx.SYNCSEL (continued)** 

|**SYNCSEL[5:0]**|**SDSYNCx.SYNCSEL[5:0]**|**SDSYNCx.SYNCSEL[5:0]**|**SDSYNCx.SYNCSEL[5:0]**|**SDSYNCx.SYNCSEL[5:0]**|
|---|---|---|---|---|
||**1**|**2**|**3**|**4**|
|37|PWM18.SOCB|PWM18.SOCB|PWM18.SOCB|PWM18.SOCB|
|38|PWM19.SOCA|PWM19.SOCA|PWM19.SOCA|PWM19.SOCA|
|39|PWM19.SOCB|PWM19.SOCB|PWM19.SOCB|PWM19.SOCB|
|40|PWM20.SOCA|PWM20.SOCA|PWM20.SOCA|PWM20.SOCA|
|41|PWM20.SOCB|PWM20.SOCB|PWM20.SOCB|PWM20.SOCB|
|42|PWM21.SOCA|PWM21.SOCA|PWM21.SOCA|PWM21.SOCA|
|43|PWM21.SOCB|PWM21.SOCB|PWM21.SOCB|PWM21.SOCB|
|44|PWM22.SOCA|PWM22.SOCA|PWM22.SOCA|PWM22.SOCA|
|45|PWM22.SOCB|PWM22.SOCB|PWM22.SOCB|PWM22.SOCB|
|46|PWM23.SOCA|PWM23.SOCA|PWM23.SOCA|PWM23.SOCA|
|47|PWM23.SOCB|PWM23.SOCB|PWM23.SOCB|PWM23.SOCB|
|48|PWM24.SOCA|PWM24.SOCA|PWM24.SOCA|PWM24.SOCA|
|49|PWM24.SOCB|PWM24.SOCB|PWM24.SOCB|PWM24.SOCB|
|50|PWM25.SOCA|PWM25.SOCA|PWM25.SOCA|PWM25.SOCA|
|51|PWM25.SOCB|PWM25.SOCB|PWM25.SOCB|PWM25.SOCB|
|52|PWM26.SOCA|PWM26.SOCA|PWM26.SOCA|PWM26.SOCA|
|53|PWM26.SOCB|PWM26.SOCB|PWM26.SOCB|PWM26.SOCB|
|54|PWM27.SOCA|PWM27.SOCA|PWM27.SOCA|PWM27.SOCA|
|55|PWM27.SOCB|PWM27.SOCB|PWM27.SOCB|PWM27.SOCB|
|56|PWM28.SOCA|PWM28.SOCA|PWM28.SOCA|PWM28.SOCA|
|57|PWM28.SOCB|PWM28.SOCB|PWM28.SOCB|PWM28.SOCB|
|58|PWM29.SOCA|PWM29.SOCA|PWM29.SOCA|PWM29.SOCA|
|59|PWM29.SOCB|PWM29.SOCB|PWM29.SOCB|PWM29.SOCB|
|60|PWM30.SOCA|PWM30.SOCA|PWM30.SOCA|PWM30.SOCA|
|61|PWM30.SOCB|PWM30.SOCB|PWM30.SOCB|PWM30.SOCB|
|62|PWM31.SOCA|PWM31.SOCA|PWM31.SOCA|PWM31.SOCA|
|63|PWM31.SOCB|PWM31.SOCB|PWM31.SOCB|PWM31.SOCB|
|SDSYNC Mux<br>PWMx<br>**SYNCSEL**<br>~~**SOCB**~~<br>~~**SOCA**~~<br>~~**SDyFLTx.SDSYNC**~~|||||



**Figure 7-373. SDSYNC Event** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

903 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Note** 

Make sure that only one SDSYNC event is generated per PWM timer period. Using PWM in up-count or down-count mode can automatically make sure that only SDSYNC events are generated. But, if up-down count mode is used, then make sure that only one SDSYNC event per PWM cycle is generated; otherwise, the filter synchronizer corrupts SDFM timing by providing two pulses per PWM cycle. 

Because of the inherent architecture of the Sinc filter (Sinc1, Sinc2, Sinc3, SincFast), the first few samples, depending upon filter type, are incorrect. Table 7-194 shows the number of incorrect samples on the following conditions: 

- When Sinc filter is enabled and configured for first time. 

- When Sinc filter is disabled and re-enabled or reconfigured in the middle of operation. 

- When data filter receives SDSYNC event from PWM. 

**Table 7-194. Number of Incorrect Samples Tabulated** 

|**Filter Type**|**Number of Incorrect Samples After the Filter is Enabled and**<br>**Configured**|
|---|---|
|Sinc1|No incorrect sample.|
|Sinc2|The first sample of the Sinc2 filter is incorrect.|
|SincFast|The first two samples of the SincFast filter are incorrect.|
|Sinc3|The first two samples of the Sinc3 filter are incorrect.|



## **CAUTION** 

SDFM comparator interrupts can be enabled only after providing sufficient settling time to make sure the comparator filter does not trip on these incorrect samples. Therefore, SDFM comparator interrupts (CMPxH and CMPxL) can be enabled only after a sufficient delay is provided after the comparator filter is configured. This sufficient delay is calculated by adding the latency of the comparator filter and 5 SDFM-CLKx clock cycles. 

## **7.5.10.9 Comparator (Secondary) Filter Unit** 

Most control systems require protection of the system by tripping the PWM in case the current or voltage goes out of bounds. The primary purpose of the secondary (comparator) filter is to allow the user to monitor input conditions with a fast settling time. This allows the user to trip PWMs to protect the system from potential damage. 

## **Note** 

The secondary (comparator) filter cannot be synchronized with respect to the PWM event (SDSYNC event). 

The comparator filter is a configurable Sinc filter that supports the following filter types: Sinc1, Sinc2, Sinc3, and SincFast. The comparator OSR (COSR) settings can be configured from 1 to 32 and is independent of the data filter. Effective resolution of the comparator filter (ENOB) depends upon the comparator filter type, COSR, and sigma-delta modulator frequency. By default, the comparator filter is disabled and setting SDCPARMx.CEN = 1 enables the comparator filter. The comparator filter output is represented in 16-bit unsigned format. This filter unit translates a low input signal as 0 and a high input signal as 1. The resulting calculations give only positive values for the output of the comparator filter. Table 7-195 shows the different full-scale values that the comparator filter can store using different OSRs. 

**Table 7-195. Peak Data Values for Different OSR/Filter Combinations** 

|**OSR**|**Sinc1**|**Sinc2**|**Sinc3**|**SincFast**|
|---|---|---|---|---|
|x|0 to x|0 to x2|0 to x3|0 to 2x2|



904 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-195. Peak Data Values for Different OSR/Filter Combinations (continued)** 

|**OSR**|**Sinc1**|**Sinc2**|**Sinc3**|**SincFast**|
|---|---|---|---|---|
|4|0 to 4|0 to 16|0 to 64|0 to 32|
|8|0 to 8|0 to 64|0 to 512|0 to 128|
|16|0 to 16|0 to 256|0 to 4096|0 to 512|
|32|0 to 32|0 to 1024|0 to 32,768|0 to 2048|



See Section 7.5.10.7.1 to understand how to calculate data rate and latency of comparator filter. 

The output of the comparator filter is memory-mapped and can be read in the SDCDATAx register. This register, SDCDATAx, is updated every COSR number of SDFM-CLKx cycles. The comparator filter digital output is connected to digital comparators explained below. 

## **Note** 

The enumeration between the SDFM Data and Clock signals is described as [0:3] in the device data sheet but the Register Addendum maps the [0:3] Data and Clock signals to [1:4]. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

905 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [388 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>
Comparator Unit<br>HLT<br>COMPH1<br>SD-Cx SINCx LLT COMPH1 COMPH1 (or) COMPL1<br>COMPL1<br>COMPL1<br>HLT2<br>SD-Dx COMPH2<br>COMPH2<br>COMPH2 (or) COMPL2<br>LLT2<br>COMPL2<br>COMPL2<br>ZCT<br>COMPZ<br>SDCDATAx<br>**----- End of picture text -----**<br>


**==> picture [342 x 247] intentionally omitted <==**

**----- Start of picture text -----**<br>
COMPH1<br>00 CEVT1OUT<br>COMPL1 (or) COMPH1<br>CEVT1<br>Digital Filter Core 01<br>COMPH2<br>COMPL2 (or) COMPH2 SDCOMPxCTL.<br>SDCOMPxEVT1FLTCTL<br>CEVT1DIGFILTSEL<br>SDCOMPxEVT1FLTCLKCTL<br>SDCPARMx.CEVT1SEL<br>COMPL1<br>00 CEVT2OUT<br>COMPL1 (or) COMPH1<br>CEVT2<br>Digital Filter Core 01<br>COMPL2<br>COMPL2 (or) COMPH2 SDCOMPxEVT2FLTCTL SDCOMPxCTL.<br>CEVT2DIGFILTSEL<br>SDCOMPxEVT2FLTCLKCTL<br>SDCPARMx.CEVT2SEL<br>**----- End of picture text -----**<br>


**Figure 7-374. Comparator Unit Structure** 

906 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.10.9.1 Higher Threshold (HLT) Comparators**_ 

- High threshold comparator can be used to detect over-value condition. 

- When comparator data > = higher threshold register, a high threshold event is generated. 

- Higher threshold comparator events except for COMPHZx can be configured to trigger following events: CPU interrupt, PWM trip. 

- This device has three high threshold comparators: 

   - 

## **Higher Threshold 1 (HLT1) Comparator** : 

   - When comparator data > = (SDFLTxCMPH1.HLT), HLT1 comparator generates COMPH1 event. 

   - The COMPH1 event is connected to both CEVT1 and CEVT2. 

- 

## **Higher Threshold 2 (HLT2) Comparator** : 

   - When comparator data > = (SDFLTxCMPH2.HLT), HLT2 comparator generates COMPH2 event. 

   - The COMPH2 event is connected to both CEVT1 and CEVT2. 

- 

## **Higher Threshold (HTLZ) Comparator** : 

- When comparator data > = (SDFLT1CMPHZ.CMPHZ), it can generate a Higher Threshold (B) event (COMPHZx) and sets the corresponding SDSTATUS.HZx flag. But, this event cannot be configured to generate SDFM interrupt (SDx_ERR). 

## _**7.5.10.9.2 Lower Threshold (LLT) Comparators**_ 

- The low threshold comparator can be used to detect under-value condition. 

- When comparator data < = Lower Threshold register, a low threshold event is generated. 

- Lower threshold comparator events can be configured to trigger following events: CPU interrupt, PWM trip. 

- Lower threshold comparator events can be used in conjunction with ECAP to measure the frequency / duty cycle of Threshold crossing 

- This device has two low threshold comparators. . 

   - 

## **Lower Threshold 1 (LLT1) Comparator** 

   - When comparator data < = (SDFLTxCMPL1.LLT), the LLT1 comparator generates COMPL1 event. 

   - The COMPL1 event is connected to both CEVT1 and CEVT2. 

- 

## **Lower Threshold 2 (LLT2) Comparator** 

- When comparator data < = (SDFLTxCMPL2.LLT), LLT2 comparator generates COMPL2 event. 

- The COMPL2 event is connected to both CEVT1 and CEVT2. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

907 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.5.10.9.3 Digital Filter**_ 

The digital filter works on a window of FIFO samples (SAMPWIN + 1) taken from the input. The filter output resolves to the majority value of the sample window, where majority is defined by the threshold (THRESH) value. If the majority threshold is not satisfied, the filter output remains unchanged. 

For proper operation, the value of THRESH must be greater than SAMPWIN / 2. 

A prescale function (CLKPRESCALE) determines the filter sampling rate, where the filter FIFO captures one sample every CLKPRESCALE system clocks. Old data from the FIFO is discarded. 

A conceptual model of the digital filter is shown in Figure 7-375. 

**==> picture [436 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDCOMPxEVT1/2FLTCTL.SAMPWIN<br>SDCOMPxEVT1/2FLTCTL.THRESH<br>FL_CEVT1/2<br>Digital Filter<br>CEVT1/2 32-bit FIFO<br>Data Latch 0  1  2  3  4  5  6  7  8  9  «...  28  29  30  31 [Data Discard]<br>SDCOMPxEVT1/2FLTCTL CLKPRESCALE<br>SYSCLK<br>**----- End of picture text -----**<br>


**Figure 7-375. Digital Filter** 

Equivalent C code of the filter implementation is: 

```
if (FILTER_OUTPUT == 0) {
    if (Num_1s_in_SAMPWIN >= THRESH) {
        FILTER_OUTPUT = 1;
    }
}
else {
    if (Num_0s_in_SAMPWIN >= THRESH) {
        FILTER_OUTPUT = 0;
    }
}
```

The configurable digital filter output is for filtering glitches. The application chooses between filtered or raw output of the comparator, and the output can reach the event flag register (SDIFLG.FLTx_FLG_CEVTx) and the CEVETxOUT event output of the SDFM module as show in _Digital Filter Outputs_ . The figure also shows rise edge detection logic along the path from the filter to flag register. 

908 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [500 x 246] intentionally omitted <==**

## **Figure 7-376. Digital Filter Outputs** 

When the digital filter path is chosen, the event flag register is set only once on the rise edge of digital filter output. If the event flag register is cleared, the flag is not set again even if the comparator output is maintained high. The issue is not present on the CEVETxOUT event going to XBAR nor if the raw output path is chosen (aka CEVTxDIGFILTSEL = 0). 

## **Filter Initialization Sequence** 

To make sure of proper operation of the digital filter, the following initialization sequence is recommended: 

1. Configure the digital filter parameters for operation: 

   - Set SAMPWIN for the number of samples to monitor in the FIFO window. 

   - Set THRESH for the threshold required for majority qualification. 

   - Set CLKPRESCALE for the digital filter clock prescale value. 

2. Initialize the sample values in the digital FIFO window by setting FILINIT = 1. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 909 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.10.10 Theoretical SDFM Filter Output** 

The following equations can be used to derive a theoretical filter output of an SDFM filter output for both a comparator filter and a data filter. 

**==> picture [465 x 28] intentionally omitted <==**

## Where: 

- Vclipping = maximum differential voltage input range of modulator 

- Input voltage = Differential input voltage applied to the modulator 

> Comparator Filter Output Theoretical� � Density of ones in bitstream u Maximum Filter Output FilterType, COSR� � (20) 

FilterOutput = -°®absolute�Input voltage� ½°u¾ Maximum Filter Output FilterType, DOSR� � °¯ Vclipping °¿ (21) -FilterOutput          if Input Voltage is +ve voltage ° Data Filter Output_32bit �Theoretical� = °°® ° 2's complement   if input voltage is -ve voltage ° °¯of FilterOutput (22) 

> Data Filter Output_16bit �Theoretical� = 

> Data Filter Output_32bit �Theoretical� !! Shift value�FilterType, OSR� 

(23) 

910 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## For example, when using the AMC1306x25 modulator: 

|AMC1306x25|Vclipping =<br>Input voltage (AINP - AINN) =|320 mV<br>100 mV|
|---|---|---|
|SDFM filter settings|Filter type =<br>Comparator OSR (COSR) =<br>Data filter OSR (DOSR) =|3<br>32<br>100|



|Density of ones in bitstream|UsingEquation 19|0.65625|
|---|---|---|
|Comparator filter output<br>Filter type = Sinc3<br>COSR = 32|UsingEquation 20|21504|
|Data filter output (32-bit)<br>Filter type = Sinc3<br>DOSR = 100|UsingEquation 21andEquation 22|312500|
|Data filter output (32-bit)<br>Filter type = Sinc3<br>DOSR = 100<br>(Right shift by 5)|UsingEquation 23|9765|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

911 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.10.11 Interrupt Unit** 

Each SDFM can generate five CPU interrupts such as SDFM Error (SDy_ERR) and SDFM data ready (SDy_DRINTx) interrupts for each filter module. 

## _**7.5.10.11.1 SDFM (SDy_ERR) Interrupt Sources**_ 

Figure 7-377 shows the structure of SDy_ERR interrupt. SDy_ERR interrupt can be triggered by any of these 16 events. 

**==> picture [500 x 180] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDFLTxCMPL1<br>COMPL1<br>SDIFLGCLR.FLTx_FLG_CEVT1 SDCPARMx.EN_CEVT1 Modulator failure SDCTL.MIE MFx flag bit<br>S Q<br>SDFLTxCMPL2 R Q FLTx_FLG_CEVT1<br>COMPL2 SDCTL.MIE SDIFLGCLR.MFx R SDCPARMx.MFIE<br>CEVT1<br>S<br>SDCTL.MIE<br>Comparator filter output SDCTL.MIE FIFO Overflow condition SDFFOVFx flag bit<br>SDFLTxCMPH1 COMPH1 CEVT2 S Q FLTx_FLG_CEVT2 S Q<br>R SDFIFOCTLx.OVFIEN<br>R SDIFLGCLR.SDFFOVFx<br>SDFLTxCMPH2 SDCPARMx.EN_CEVT2<br>COMPH2<br>SDIFLGCLR.FLTx_FLG_CEVT2<br>FLTx_FLG_CEVT1  flag bit<br>SDCPARMx.CEVT1SEL<br>SDCPARMx.CEVT2SEL FLTx_FLG_CEVT2  flag bit<br>SDFLTxCMPHZ COMPHZ S Q SDCTL.MIE HZx flag bit MFx flag bit SDy_ERR<br>SDFFOVFx bit<br>R SDCPARMx. HZEN<br>SDCTL.HZx<br>**----- End of picture text -----**<br>


**Figure 7-377. SDFM Error (SD_ERR) Interrupt Sources** 

## **1. Comparator Event1 (CEVT1)** 

CEVT1 events from any of the four comparator filter module can trigger CPU interrupt. This event can be configured to trigger SDy_ERR interrupt only if below configurations are made: 

- Enable Main interrupt enable (SDCTL.MIE = 1) 

- Enable comparator Event1 interrupt (SDCPARMx.EN_CEVT1 = 1) 

On a CEVT1 event, SDIFLG.FLTx_FLG_CEVT1 flag bit is set. This flag bit can only be reset if the corresponding bit in SDIFLGCLR register is set and if the interrupt source is no longer active. 

## **2. Comparator Event2 (CEVT2)** 

CEVT2 events from any of the four comparator filter module can trigger CPU interrupt. This event can be configured to trigger SDy_ERR interrupt only if below configurations are made: 

- Enable Main interrupt enable (SDCTL.MIE = 1) 

- Enable comparator event1 interrupt (SDCPARMx.EN_CEVT2 = 1) 

On a CEVT2 event, SDIFLG.FLTx_FLG_CEVT2 flag bit is set. This flag bit can only be reset if the corresponding bit in SDIFLGCLR register is set and if the interrupt source is no longer active. 

## **3. Modulator Failure (MFx) event** 

Modulator failures (MFx) are generated when SD-Cx goes missing. The modulator clock is considered missing if SD-Cx does not toggle for 64-SYSCLKs. MFx events from any of the four filter modules can trigger CPU interrupt. This event can be configured to trigger SDy_ERR interrupt only if below configurations are made: 

- Enable Main Interrupt Enable (SDCTL.MIE = 1) 

- Enable modulator clock failure interrupt source (SDCPARMx.MFIE = 1) 

On a MFx event, SDIFLG.MFx flag bit is set. This flag bit can only be reset if the corresponding bit in SDIFLGCLR register is set and if the interrupt source is no longer active. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

912 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **4. FIFO overflow (SDFFOVFx) event** 

The number of filter data available in FIFO at any given point can be tracked in SDFIFOCTLx.SDFFST. If the number of words received in FIFO is greater than Max FIFO depth (16), SDFFOVFx event is generated. SDFFOVFx events from any of the four filter modules can trigger CPU interrupt. This event can be configured to trigger SDy_ERR interrupt, only if below configurations are made: 

- Enable SDFM FIFO (Set SDFIFOCTLx.FFEN = 1) 

- Enable SDFM FIFO overflow interrupt (Set SDFIFOCTLx.OVFIEN = 1) and 

- Enable Main interrupt enable (Set SDCTL.MIE = 1) 

On a SDFFOVFx event, all subsequent data (primary) filter data is lost and is not stored in FIFO. SDIFLG.SDFFOVFx flag bit is set on a FIFO overflow event and this bit can be cleared if the corresponding bit in SDIFLGCLR register is set and if the interrupt source is no longer active. 

## _**7.5.10.11.2 Data Ready (DRINT) Interrupt Sources**_ 

Figure 7-378 shows the structure of interrupt SDy_DRINTx interrupt. Each SDy_DRINTx interrupt is triggered by corresponding Data Filter channel. 

**==> picture [482 x 236] intentionally omitted <==**

**----- Start of picture text -----**<br>
16<br>15<br>3<br>FIFO Data Ready<br>SDFFST 2 SDFFIL<br>1<br>FFINTx SDFFINTx flag bit<br>SDFIFOCTLx.FFIEN S Q<br>SDy_DRINTx<br>SDIFLGCLR.SDFFINTx<br>R<br>New data filter data<br>AFx AFx flag bit<br>S Q<br>SDDFPARMx. AE<br>DRINTSEL<br>SDIFLGCLR.AF x R<br>**----- End of picture text -----**<br>


**Figure 7-378. SDFM Data Ready (SDy_DRINTx) Interrupt** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

913 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **1. Data Acknowledge (AFx)** 

When the primary filter is ready with a new filter data, AFx event is generated. AFx events from each filter can generate their own SDy_DRINTx interrupt. This event can be configured to trigger SDy_DRINTx interrupt only if below configurations are made: 

- Enable individual filter interrupts (SDDFPARMx. AE = 1) 

- Select data-ready interrupt source AFx (DRINTx = AFx) (SDFIFOCTLx.DRINTSEL = 0) 

On an AFx event, the SDIFLG.AFx flag bit is set. This flag bit can only be reset, if the corresponding bit in SDIFLGCLR register is set and if the interrupt source is no longer active. 

## **2. Four FIFO Data ready interrupt (SDFFINTx)** 

FIFO Data Ready event is generated whenever SDFIFOCTLx.SDFFST >= SDFIFOCTLx.SDFFIL condition is met. FIFO data ready events from each filter can generate their own SDy_DRINTx interrupt. This event can be configured to trigger SDy_DRINTx interrupt only if below configurations are made: 

Table 7-196 shows how the DRINTx output is selected. 

- Enable SDFM FIFO (Set SDFIFOCTLx.FFEN = 1) and 

- Enable SDFM FIFO interrupt (Set SDFIFOCTLx.FFIEN = 1) 

- Select data-Ready interrupt source is SDFFINTx (DRINTx = SDFFINTx) (SDFIFOCTLx.DRINTSEL = 1) 

**Table 7-196. SDFM Data-Ready Interrupt (SDy_DRINTx) Output Selection** 

|**DRINTSEL**|**AE**|**FFIEN**|**FFEN**|**DRINTx**|
|---|---|---|---|---|
|0|0|x|X|0|
|0|1|x|X|AFx|
|1|x|0|X|0|
|1|x|x|0|0|
|1|x|1|1|SDFFINTx|



## **7.5.10.12 SDFM Programming Guide** 

## **Driver Information** 

Driver features are available at the SDFM driver page. 

## **Software API Information** 

The SDFM driver provides an API to configure the SDFM module. Full documentation is located on APIs for SDFM 

## **Example Usage** 

The below links shows an example on how to use SDFM 

- SDFM EPWM sync CPU read 

- SDFM Filter sync CPU read 

- SDFM single channel filter sync CPU read 

914 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.11 Crossbar (XBAR)**_ 

The crossbars (referred to as XBAR throughout this chapter) provide flexibility to connect device inputs, outputs, and internal resources in a variety of configurations. 

**==> picture [500 x 294] intentionally omitted <==**

**Figure 7-379. CONTROLSS XBAR Diagram** 

The real time control subsystem contains a total of eight XBARs: 

- INPUTXBAR 

- PWMXBAR 

- MDLXBAR 

- ICLXBAR 

- INTXBAR 

- DMAXBAR 

- OUTPUTXBAR 

- PWMSYNCOUTXBAR 

Each of the XBARs is named according to signal source routed to the inputs. For example, the INPUTXBAR brings external signals "in" to the device. The OUTPUTXBAR takes internal signals "out" of the device to a GPIO. The PWMXBAR takes the signal to the trip inputs of the PWM. Similarly, the Diode Emulation logic synchronous values are routed to the Min Dead-Band logic (MDL) and Illegal Combo logic (ICL) of the PWMs via the MDLXBAR and the ICLXBAR respectively. The INTXBAR routes the large quantity of real-time CONTROLSS interrupts efficiently to the SoC interrupt controller. The DMAXBAR routes DMA requests from the real-time CONTROLSS to the SOC EDMA module. Both the INTXBAR and DMAXBAR limit the number of interrupt and DMA requests going from CONTROLSS to the SOC. The PWMSYNCOUTXBAR routes all the PWM sync outputs to SoC TIMESYNC logic and the OUTPUTXBAR. 

Further details about each of these XBARs can be found in the following sections. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

915 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**7.5.11.1 INPUTXBAR** ................................................................................................................................................917 **7.5.11.2 PWMXBAR** ..................................................................................................................................................919 **7.5.11.3 MDLXBAR** ...................................................................................................................................................920 **7.5.11.4 ICLXBAR** .....................................................................................................................................................922 **7.5.11.5 INTXBAR** .....................................................................................................................................................923 **7.5.11.6 DMAXBAR** .................................................................................................................................................. 925 **7.5.11.7 OUTPUTXBAR** ............................................................................................................................................926 **7.5.11.8 PWMSYNCOUTXBAR** ................................................................................................................................ 932 **7.5.11.9 XBAR Programming Guide** .......................................................................................................................932 

916 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.11.1 INPUTXBAR** 

The INPUTXBAR routes the signals from any GPIO to different IP blocks such as the eCAP(s), ePWM(s), ICSS GPI(s), and the PWMXBAR. The INPUTXBAR has access to every GPIO and can route each signal to any (or multiple) of the IP blocks previously mentioned. This flexibility relieves some of the constraints on peripheral muxing by enabling any available GPIO pin to be used for slow changing I/O signals by the CONTROLSS. It is important to note that the function selected on the GPIO multiplexer does not affect the INPUTXBAR. The INPUTXBAR simply connects the signal on the input buffer to the selected destination. This flexibility enables routing the output of one peripheral to another (for example, measure the output of an ePWM with an eCAP for a frequency test). Apart from GPIOs, ICSS GPO(s), can also be used as inputs to the INPUTXBAR and be used in a similar fashion to any GPIO source. 

The architecture of the INPUTXBAR is composed of multiple input unit XBARs which routes any of the INPUTXBAR sources to the single output of the XBAR. The two step multiplexer logic ensures that only one source is routed to the output. 

The INPUTXBAR is configured by writing to the [INPUTXBAR[0-31]_G[0-1].SEL and INPUTXBAR[31:0].GSEL] registers. The Figure 7-380 shows all IP sources and destinations and Table 7-197 provides a comprehensive list of the destinations. For more information on configuration, see the CONTROLSS_INPUTXBAR register definitions in the XBAR register section. 

## **Note** 

INPUTXBAR routes GPIO pin to any of its 32 outputs and is not a OR implementation like most of CONTROLSSS XBARs 

**==> picture [500 x 312] intentionally omitted <==**

**Figure 7-380. INPUTXBAR Functional Block Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

917 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Note** 

Parameters for table below w=[4:0] x=[15:0] y=[31:16] z=[31:0] u=[9:0] 

**Table 7-197. INPUTXBAR Output Destinations** 

|**INPUTXBAR Outputs**|**Destination-1**|**Destination-2**|**Destination-3**|
|---|---|---|---|
|INPUTXBAR.Out0|PWMXBAR.G4.0|EPWMx.TZ1|ECAPu.ECAPIN.202|
|INPUTXBAR.Out1|PWMXBAR.G4.1|EPWMx.TZ2|ECAPu.ECAPIN.203|
|INPUTXBAR.Out2|PWMXBAR.G4.2|EPWMx.TZ3|ECAPu.ECAPIN.204|
|INPUTXBAR.Out3|PWMXBAR.G4.3|EPWMx.TZ4|ECAPu.ECAPIN.205|
|INPUTXBAR.Out4|PWMXBAR.G4.4|EPWMz.SYNCIN.80|ECAPu.ECAPIN.206|
|INPUTXBAR.Out5|PWMXBAR.G4.5|ADCw.TRIG.5|ECAPu.ECAPIN.207|
|INPUTXBAR.Out6|PWMXBAR.G4.6|Not Used|ECAPu.ECAPIN.208|
|INPUTXBAR.Out7|PWMXBAR.G4.7|Not Used|ECAPu.ECAPIN.209|
|INPUTXBAR.Out8|PWMXBAR.G4.8|Not Used|ECAPu.ECAPIN.210|
|INPUTXBAR.Out9|PWMXBAR.G4.9|Not Used|ECAPu.ECAPIN.211|
|INPUTXBAR.Out10|PWMXBAR.G4.10|Not Used|ECAPu.ECAPIN.212|
|INPUTXBAR.Out11|PWMXBAR.G4.11|Not Used|ECAPu.ECAPIN.213|
|INPUTXBAR.Out12|PWMXBAR.G4.12|Not Used|ECAPu.ECAPIN.214|
|INPUTXBAR.Out13|PWMXBAR.G4.13|Not Used|ECAPu.ECAPIN.215|
|INPUTXBAR.Out14|PWMXBAR.G4.14|Not Used|ECAPu.ECAPIN.216|
|INPUTXBAR.Out15|PWMXBAR.G4.15|Not Used|ECAPu.ECAPIN.217|
|INPUTXBAR.Out16|PWMXBAR.G4.16|EPWMy.TZ1|ECAPu.ECAPIN.218|
|INPUTXBAR.Out17|PWMXBAR.G4.17|EPWMy.TZ2|ECAPu.ECAPIN.219|
|INPUTXBAR.Out18|PWMXBAR.G4.18|EPWMy.TZ3|ECAPu.ECAPIN.220|
|INPUTXBAR.Out19|PWMXBAR.G4.19|EPWMy.TZ4|ECAPu.ECAPIN.221|
|INPUTXBAR.Out20|PWMXBAR.G4.20|EPWMz.SYNCIN.81|ECAPu.ECAPIN.222|
|INPUTXBAR.Out21|PWMXBAR.G4.21|Not Used|ECAPu.ECAPIN.223|
|INPUTXBAR.Out22|PWMXBAR.G4.22|Not Used|ECAPu.ECAPIN.224|
|INPUTXBAR.Out23|PWMXBAR.G4.23|Not Used|ECAPu.ECAPIN.225|
|INPUTXBAR.Out24|PWMXBAR.G4.24|Not Used|ECAPu.ECAPIN.226|
|INPUTXBAR.Out25|PWMXBAR.G4.25|Not Used|ECAPu.ECAPIN.227|
|INPUTXBAR.Out26|PWMXBAR.G4.26|Not Used|ECAPu.ECAPIN.228|
|INPUTXBAR.Out27|PWMXBAR.G4.27|Not Used|ECAPu.ECAPIN.229|
|INPUTXBAR.Out28|PWMXBAR.G4.28|Not Used|ECAPu.ECAPIN.230|
|INPUTXBAR.Out29|PWMXBAR.G4.29|Not Used|ECAPu.ECAPIN.231|
|INPUTXBAR.Out30|PWMXBAR.G4.30|Not Used|ECAPu.ECAPIN.232|
|INPUTXBAR.Out31|PWMXBAR.G4.31|Not Used|ECAPu.ECAPIN.233|



For more information on configuration, see the INPUTXBAR register definitions. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

918 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.5.11.2 PWMXBAR** 

The PWMXBAR routes the trip events of different real-time CONTROLSS instances to either different ePWM trip inputs or to ICSSM GPI inputs. The sources of trip events to ePWM can be any of the following: compare subsystem trip high and low events, SDFM filter events, ADC events, INPUTXBAR outputs, ePWM tripout events, diode emulation trip/active signals, eQEP error events, FSIRX triggers, and eCAP trip outputs. 

The architecture of the PWMXBAR includes unit XBARs which allow any of the PWMXBAR inputs to be routed to a single output of the XBAR. Multiple PWMXBAR outputs can have the same trip source routed to them. PWMXBAR outputs can also trigger ICSSM GPI inputs and can capture any inputs to the ePWM trip inputs. Each unit XBAR also has an associated set of PWMXBAR_STATUS and PWMXBAR_FLAG registers which can be used to inform the application of events. The PWMXBAR_FLAG_CLR register allows the application to clear the flags of captured events in a controlled fashion. 

The PWMXBAR is configured by writing to the [PWMXBAR[0-29]_G[0-9].SEL] registers. The Figure 7-381 shows all IP sources and destinations and Table 7-198 provides a comprehensive list of the destinations. For more information on configuration, see the CONTROLSS_PWMXBAR register definitions in the XBAR register section. 

**==> picture [500 x 358] intentionally omitted <==**

**Figure 7-381. PWMXBAR Functional Block Diagram** 

**Note** 

Parameters for table below x=[15:0],y=[31:16] 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 919 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-198. PWMXBAR Output Destinations** 

|**PWMXBAR Outputs**|**Destination-1**|**Destination-2**|**Destination-3**|
|---|---|---|---|
|PWMXBAR.Out0|EPWMx.TripInput.1|ICSSM.GPI_Port0.0|ICSSM.GPI_Port1.0|
|PWMXBAR.Out1|EPWMx.TripInput.2|ICSSM.GPI_Port0.1|ICSSM.GPI_Port1.1|
|PWMXBAR.Out2|EPWMx.TripInput.3|ICSSM.GPI_Port0.2|ICSSM.GPI_Port1.2|
|PWMXBAR.Out3|EPWMx.TripInput.4|ICSSM.GPI_Port0.3|ICSSM.GPI_Port1.3|
|PWMXBAR.Out4|EPWMx.TripInput.5|ICSSM.GPI_Port0.4|ICSSM.GPI_Port1.4|
|PWMXBAR.Out5|EPWMx.TripInput.6|ICSSM.GPI_Port0.5|ICSSM.GPI_Port1.5|
|PWMXBAR.Out6|EPWMx.TripInput.7|ICSSM.GPI_Port0.6|ICSSM.GPI_Port1.6|
|PWMXBAR.Out7|EPWMx.TripInput.8|ICSSM.GPI_Port0.7|ICSSM.GPI_Port1.7|
|PWMXBAR.Out8|EPWMx.TripInput.9|ICSSM.GPI_Port0.8|ICSSM.GPI_Port1.8|
|PWMXBAR.Out9|EPWMx.TripInput.10|ICSSM.GPI_Port0.9|ICSSM.GPI_Port1.9|
|PWMXBAR.Out10|EPWMx.TripInput.11|ICSSM.GPI_Port0.10|ICSSM.GPI_Port1.10|
|PWMXBAR.Out11|EPWMx.TripInput.12|ICSSM.GPI_Port0.11|ICSSM.GPI_Port1.11|
|PWMXBAR.Out12|EPWMx.TripInput.13|ICSSM.GPI_Port0.12|ICSSM.GPI_Port1.12|
|PWMXBAR.Out13|EPWMx.TripInput.14|ICSSM.GPI_Port0.13|ICSSM.GPI_Port1.13|
|PWMXBAR.Out14|EPWMx.TripInput.15|ICSSM.GPI_Port0.14|ICSSM.GPI_Port1.14|
|PWMXBAR.Out15|EPWMy.TripInput.1|ICSSM.GPI_Port0.15|ICSSM.GPI_Port1.15|
|PWMXBAR.Out16|EPWMy.TripInput.2|ICSSM.GPI_Port0.16|ICSSM.GPI_Port1.16|
|PWMXBAR.Out17|EPWMy.TripInput.3|ICSSM.GPI_Port0.17|ICSSM.GPI_Port1.17|
|PWMXBAR.Out18|EPWMy.TripInput.4|ICSSM.GPI_Port0.18|ICSSM.GPI_Port1.18|
|PWMXBAR.Out19|EPWMy.TripInput.5|ICSSM.GPI_Port0.19|ICSSM.GPI_Port1.19|
|PWMXBAR.Out20|EPWMy.TripInput.6|ICSSM.GPI_Port0.20|ICSSM.GPI_Port1.20|
|PWMXBAR.Out21|EPWMy.TripInput.7|ICSSM.GPI_Port0.21|ICSSM.GPI_Port1.21|
|PWMXBAR.Out22|EPWMy.TripInput.8|ICSSM.GPI_Port0.22|ICSSM.GPI_Port1.22|
|PWMXBAR.Out23|EPWMy.TripInput.9|ICSSM.GPI_Port0.23|ICSSM.GPI_Port1.23|
|PWMXBAR.Out24|EPWMy.TripInput.10|ICSSM.GPI_Port0.24|ICSSM.GPI_Port1.24|
|PWMXBAR.Out25|EPWMy.TripInput.11|ICSSM.GPI_Port0.25|ICSSM.GPI_Port1.25|
|PWMXBAR.Out26|EPWMy.TripInput.12|ICSSM.GPI_Port0.26|ICSSM.GPI_Port1.26|
|PWMXBAR.Out27|EPWMy.TripInput.13|ICSSM.GPI_Port0.27|ICSSM.GPI_Port1.27|
|PWMXBAR.Out28|EPWMy.TripInput.14|ICSSM.GPI_Port0.28|ICSSM.GPI_Port1.28|
|PWMXBAR.Out29|EPWMy.TripInput.15|ICSSM.GPI_Port0.29|ICSSM.GPI_Port1.29|



## **7.5.11.3 MDLXBAR** 

The MDLXBAR is able to route one of three input signals to the Minimum Dead-Band submodule inside the ePWM module. The input signals comprise of either PWMA or PWMB after having passed through the Diode Emulation block, or the ICSSM GPO ports. For information on MDLXBAR use cases, refer to ePWM module specification. 

The MDLXBAR architecture allows for each MDL unit XBAR to select from any of the three aforementioned signals and routes the signal to a single output of the XBAR. The output of MDLXBAR can be sourced to each of the 32 Minimum Dead-Band logic (MDL) submodules inside the ePWM module. 

920 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

The MDLXBAR is configured by writing to the MDLXBAR[0-15].G[0-2].SEL registers. The Figure 7-382 shows all IP sources and destinations and Table 7-199 provides a comprehensive list of the destinations. For more information on configuration, see the CONTROLSS_MDLXBAR register definitions. 

**==> picture [500 x 300] intentionally omitted <==**

**Figure 7-382. MDLXBAR Functional Block Diagram** 

**Note** 

Parameters for table below x=[31:0] 

**Table 7-199. MDL XBAR Output Destinations** 

|**MDLXBAR Outputs**|**Destination-1**|
|---|---|
|MDLXBAR.Out0|Not Used|
|MDLXBAR.Out1|EPWMx.MDLXBARIN.1|
|MDLXBAR.Out2|EPWMx.MDLXBARIN.2|
|MDLXBAR.Out3|EPWMx.MDLXBARIN.3|
|MDLXBAR.Out4|EPWMx.MDLXBARIN.4|
|MDLXBAR.Out5|EPWMx.MDLXBARIN.5|
|MDLXBAR.Out6|EPWMx.MDLXBARIN.6|
|MDLXBAR.Out7|EPWMx.MDLXBARIN.7|
|MDLXBAR.Out8|EPWMx.MDLXBARIN.8|
|MDLXBAR.Out9|EPWMx.MDLXBARIN.9|
|MDLXBAR.Out10|EPWMx.MDLXBARIN.10|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 921 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-199. MDL XBAR Output Destinations (continued)** 

|**MDLXBAR Outputs**|**Destination-1**|
|---|---|
|MDLXBAR.Out11|EPWMx.MDLXBARIN.11|
|MDLXBAR.Out12|EPWMx.MDLXBARIN.12|
|MDLXBAR.Out13|EPWMx.MDLXBARIN.13|
|MDLXBAR.Out14|EPWMx.MDLXBARIN.14|
|MDLXBAR.Out15|EPWMx.MDLXBARIN.15|



## **7.5.11.4 ICLXBAR** 

The ICLXBAR is able to route one of three input signals to the Illegal Combination Logic (ICL) submodules inside the PWM module. The input signals comprise of either PWMA or PWMB after having passed through the Minimum Dead-Band block, or the ICSSM GPO ports. For information on ICLXBAR use cases, refer to ePWM module specification. 

The ICLXBAR architecture allows for each ICL unit XBAR to select from any of the three aforementioned signals and routes the signal to a single output of the XBAR. The output of ICLXBAR can be sourced to each of the 32 ICL submodules inside the ePWM module. 

The ICLXBAR is configured by writing to the ICLXBAR[0-15].G[0-2].SEL registers. The Figure 7-383 shows all IP sources and destinations and Table 7-200 provides a comprehensive list of the destinations. For more information on configuration, see the CONTROLSS_ICLXBAR register definitions. 

**==> picture [488 x 309] intentionally omitted <==**

**Figure 7-383. ICLXBAR Functional Block Diagram** 

Parameters for table below 

922 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-200. ICLXBAR Output Destinations** 

|**ICLXBAR outputs**|**Desination-1**|
|---|---|
|ICLXBAR.Out0|EPWMx.ICLXBARIN.0|
|ICLXBAR.Out1|EPWMx.ICLXBARIN.1|
|ICLXBAR.Out2|EPWMx.ICLXBARIN.2|
|ICLXBAR.Out3|EPWMx.ICLXBARIN.3|
|ICLXBAR.Out4|EPWMx.ICLXBARIN.4|
|ICLXBAR.Out5|EPWMx.ICLXBARIN.5|
|ICLXBAR.Out6|EPWMx.ICLXBARIN.6|
|ICLXBAR.Out7|EPWMx.ICLXBARIN.7|
|ICLXBAR.Out8|EPWMx.ICLXBARIN.8|
|ICLXBAR.Out9|EPWMx.ICLXBARIN.9|
|ICLXBAR.Out10|EPWMx.ICLXBARIN.10|
|ICLXBAR.Out11|EPWMx.ICLXBARIN.11|
|ICLXBAR.Out12|EPWMx.ICLXBARIN.12|
|ICLXBAR.Out13|EPWMx.ICLXBARIN.13|
|ICLXBAR.Out14|EPWMx.ICLXBARIN.14|
|ICLXBAR.Out15|EPWMx.ICLXBARIN.15|



## **7.5.11.5 INTXBAR** 

On this device, the INT x-bar is used to route real-time CONTROLSS peripheral interrupts to the SoC interrupt controller. The idea is to limit the number of interrupts to 32 within real-time CONTROLSS before connecting to the SOC interrupt controller. 

The INT x-bar is further made up of unit x-bars, its architecture allows multiple interrupt sources to be active. For ease of readability, the interrupt sources are grouped together based on IP generating the same. Interrupt sources are active low and before entering the x-bar, these are inverted to be active high. 

The INT x-bar configured by way of the INTXBAR[31:0].G[9:0].SEL registers. The available IP source for each INPUTx is shown in INTXBAR figure below. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 923 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 280] intentionally omitted <==**

**Figure 7-384. INXBAR Block Diagram** 

**Table 7-201. INTXBAR Output Destinations** 

|**INTXBAR Outputs**|**Destination-1**<br>**VIM Cluster-0**<br>**Core0**|**Destination-2**<br>**VIM Cluster-0**<br>**Core1**|**Destination-3**<br>**VIM Cluster-1**<br>**Core0**|**Destination-4**<br>**VIM Cluster-1**<br>**Core1**|
|---|---|---|---|---|
|INTXBAR.Out0|VIM_IRQ146|VIM_IRQ146|VIM_IRQ146|VIM_IRQ146|
|INTXBAR.Out1|VIM_IRQ147|VIM_IRQ147|VIM_IRQ147|VIM_IRQ147|
|INTXBAR.Out2|VIM_IRQ148|VIM_IRQ148|VIM_IRQ148|VIM_IRQ148|
|INTXBAR.Out3|VIM_IRQ149|VIM_IRQ149|VIM_IRQ149|VIM_IRQ149|
|INTXBAR.Out4|VIM_IRQ150|VIM_IRQ150|VIM_IRQ150|VIM_IRQ150|
|INTXBAR.Out5|VIM_IRQ151|VIM_IRQ151|VIM_IRQ151|VIM_IRQ151|
|INTXBAR.Out6|VIM_IRQ152|VIM_IRQ152|VIM_IRQ152|VIM_IRQ152|
|INTXBAR.Out7|VIM_IRQ153|VIM_IRQ153|VIM_IRQ153|VIM_IRQ153|
|INTXBAR.Out8|VIM_IRQ154|VIM_IRQ154|VIM_IRQ154|VIM_IRQ154|
|INTXBAR.Out9|VIM_IRQ155|VIM_IRQ155|VIM_IRQ155|VIM_IRQ155|
|INTXBAR.Out10|VIM_IRQ156|VIM_IRQ156|VIM_IRQ156|VIM_IRQ156|
|INTXBAR.Out11|VIM_IRQ157|VIM_IRQ157|VIM_IRQ157|VIM_IRQ157|
|INTXBAR.Out12|VIM_IRQ158|VIM_IRQ158|VIM_IRQ158|VIM_IRQ158|
|INTXBAR.Out13|VIM_IRQ159|VIM_IRQ159|VIM_IRQ159|VIM_IRQ159|
|INTXBAR.Out14|VIM_IRQ160|VIM_IRQ160|VIM_IRQ160|VIM_IRQ160|
|INTXBAR.Out15|VIM_IRQ161|VIM_IRQ161|VIM_IRQ161|VIM_IRQ161|
|INTXBAR.Out16|VIM_IRQ162|VIM_IRQ162|VIM_IRQ162|VIM_IRQ162|
|INTXBAR.Out17|VIM_IRQ163|VIM_IRQ163|VIM_IRQ163|VIM_IRQ163|
|INTXBAR.Out18|VIM_IRQ164|VIM_IRQ164|VIM_IRQ164|VIM_IRQ164|
|INTXBAR.Out19|VIM_IRQ165|VIM_IRQ165|VIM_IRQ165|VIM_IRQ165|



924 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-201. INTXBAR Output Destinations (continued)** 

|**INTXBAR Outputs**|**Destination-1**<br>**VIM Cluster-0**<br>**Core0**|**Destination-2**<br>**VIM Cluster-0**<br>**Core1**|**Destination-3**<br>**VIM Cluster-1**<br>**Core0**|**Destination-4**<br>**VIM Cluster-1**<br>**Core1**|
|---|---|---|---|---|
|INTXBAR.Out20|VIM_IRQ166|VIM_IRQ166|VIM_IRQ166|VIM_IRQ166|
|INTXBAR.Out21|VIM_IRQ167|VIM_IRQ167|VIM_IRQ167|VIM_IRQ167|
|INTXBAR.Out22|VIM_IRQ168|VIM_IRQ168|VIM_IRQ168|VIM_IRQ168|
|INTXBAR.Out23|VIM_IRQ169|VIM_IRQ169|VIM_IRQ169|VIM_IRQ169|
|INTXBAR.Out24|VIM_IRQ170|VIM_IRQ170|VIM_IRQ170|VIM_IRQ170|
|INTXBAR.Out25|VIM_IRQ171|VIM_IRQ171|VIM_IRQ171|VIM_IRQ171|
|INTXBAR.Out26|VIM_IRQ172|VIM_IRQ172|VIM_IRQ172|VIM_IRQ172|
|INTXBAR.Out27|VIM_IRQ173|VIM_IRQ173|VIM_IRQ173|VIM_IRQ173|
|INTXBAR.Out28|VIM_IRQ174|VIM_IRQ174|VIM_IRQ174|VIM_IRQ174|
|INTXBAR.Out29|VIM_IRQ175|VIM_IRQ175|VIM_IRQ175|VIM_IRQ175|
|INTXBAR.Out30|VIM_IRQ176|VIM_IRQ176|VIM_IRQ176|VIM_IRQ176|
|INTXBAR.Out31|VIM_IRQ177|VIM_IRQ177|VIM_IRQ177|VIM_IRQ177|



## **7.5.11.6 DMAXBAR** 

On this device, the DMA x-bar is used to route DMA requests from real-time control subsystem peripherals to the SoC EDMA. The idea is to limit the number of DMA requests to 16 within real-time control subsystem before connecting it to the SOC EDMA. 

The DMA x-bar is further made up of unit x-bars, which allows 2 tier selection of any one of the DMA request sources. Except for the ePWM(s) SOCA and SOCB, rest of the DMA sources are active low and before entering the x-bar, these are inverted to be active high. 

The DMA x-bar configured by way of the DMAXBar[31:0].G[6:0].SEL and DMAXBAR[6:0].GSEL registers. The available IP sources for each INPUTx is shown in DMA x-bar figure below 

## **Note** 

Please note DMAXBAR routes DMA requests from CONTROLSS IPs to any of its 16 outputs and is not a OR implementation like most of CONTROLSSS XBARs 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

925 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [481 x 266] intentionally omitted <==**

**----- Start of picture text -----**<br>
Repeated x16 DMAXBar.G0.SEL DMAXBar.GSEL<br>G0.0 0<br>G0.0 DMA XBar 0 DMAXBar.Out[0] 0<br>G0.31 31<br>All EPWM SOCA<br>G0.31 DMA XBar 1 DMAXBar.Out[1] DMAXBar.G1.SEL<br>G1.0 0<br>G1.0<br>1<br>All EPWM SOCB<br>G1.31 31<br>G1.31<br>DMAXBar.G2.SEL<br>G2.0<br>G2.0 0<br>ADC0-4 DMAINT1/2/3/4, EVTINT<br>G2.24 2 DMAXBar.Out[x]<br>G2.24 24<br>139<br>G3.0 Inputs DMAXBar.G3.SEL<br>All FSI-RX/TX RX/TX_DMA_EVTRX_PING/DATA_TAG_MATCH G3.0 0<br>G3.15<br>3<br>G3.15 15<br>G4.0<br>All SD Filters DRINT DMAXBar.G4.SEL<br>G4.7<br>G4.0 0<br>4<br>G5.0<br>G4.7 7<br>All ECAP DMA_INT<br>G5.15 DMAXBar.G5.SEL<br>G6.0 DMA XBar 14 DMAXBar.Out[14] G5.0 0<br>ADC5-6 DMAINT1/2/3/4, EVTINT 5<br>G6.9 DMA XBar 15 DMAXBar.Out[15] G5.15 15<br>DMAXBar.G6.SEL<br>G5.0 0<br>6<br>G5.9 9<br>**----- End of picture text -----**<br>


**Figure 7-385. DMAXBAR Block Diagram** 

**Table 7-202. DMAXBAR Output Destinations** 

|**DMAXBAR Outputs**|**Destination**<br>**MSS EDMA**|
|---|---|
|DMAXBAR.Out0|dma_req115|
|DMAXBAR.Out1|dma_req116|
|DMAXBAR.Out2|dma_req117|
|DMAXBAR.Out3|dma_req118|
|DMAXBAR.Out4|dma_req119|
|DMAXBAR.Out5|dma_req120|
|DMAXBAR.Out6|dma_req121|
|DMAXBAR.Out7|dma_req122|
|DMAXBAR.Out8|dma_req123|
|DMAXBAR.Out9|dma_req124|
|DMAXBAR.Out10|dma_req125|
|DMAXBAR.Out11|dma_req126|
|DMAXBAR.Out12|dma_req127|
|DMAXBAR.Out13|dma_req128|
|DMAXBAR.Out14|dma_req129|
|DMAXBAR.Out15|dma_req130|



## **7.5.11.7 OUTPUTXBAR** 

On this device, the OUTPUT x-bar is used to route signals from all the control peripheral trip events to the output x-bar mapped pads or to the PRU-ICSS interrupts. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

926 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

The source of these trip events is EPWM trip outputs, SOCA, SOCB, Diode Emulation Logic (DEL) generated active and trip events, SD filter events, compare subsystem high and low trips, ADC events, PWM syncout x-bar sync outputs, EQEP index and strobe, and ECAP outputs. 

The architecture of the output x-bar is composed of output unit x-bars which routes any of the output x-bar inputs to the single output of the unit x-bar. If needed, the same trip source can be routed to multiple OUTPUT x-bar outputs by suitable programming. Each output unit x-bar also has an associated set of status and clear/flags which can be used by application to know about an event by reading the status bit. The clear flags allows to clear the captured events in a controlled fashion. Since the output x-bar is routed to GPIOs, the internal low width pulses to be stretched to 16 or 32 cycles of 200MHz real-time control subsystem clock. The polarity of the latched signal is controlled by the status registers. 

The OUTPUTXBAR is configured by way of the OUTPUTxSELECT registers. The available IP sources for each INPUTx is shown in OUTPUTXBAR figure below. While the Output x-bar outputs destination is show in the table below. 

**==> picture [500 x 257] intentionally omitted <==**

**Figure 7-386. OUTPUTXBAR Block Diagram** 

Parameters for table below x=[3:0] 

|**OUTPUTXBAR Outputs**|**Destination-1**|**Destination-2**|**Destination-3**|**Destination-3**|**Destination-4**|
|---|---|---|---|---|---|
|OUTPUTXBAR.Out0|QSPI0_CSn1_PAD|FSI_TXx.EXTTRIG<br>GER63|FSI_TXx.EXTPING<br>TRIGGER63|FSI_TXx.EXTPING<br>TRIGGER63|ICSSM.PR1_SLV_I<br>NTR.16|
|OUTPUTXBAR.Out1|SPI1_CS0_PAD|FSI_TXx.EXTTRIG<br>GER62|FSI_TXx.EXTPING<br>TRIGGER62|FSI_TXx.EXTPING<br>TRIGGER62|ICSSM.PR1_SLV_I<br>NTR.17|
|OUTPUTXBAR.Out2|SPI1_CLK_PAD|FSI_TXx.EXTTRIG<br>GER61|FSI_TXx.EXTPING<br>TRIGGER61|FSI_TXx.EXTPING<br>TRIGGER61|ICSSM.PR1_SLV_I<br>NTR.18|
|OUTPUTXBAR.Out3|SPI1_D0_PAD|FSI_TXx.EXTTRIG<br>GER60|FSI_TXx.EXTPING<br>TRIGGER60|FSI_TXx.EXTPING<br>TRIGGER60|ICSSM.PR1_SLV_I<br>NTR.19|
|OUTPUTXBAR.Out4|SPI1_D1_PAD|FSI_TXx.EXTTRIG<br>GER59|FSI_TXx.EXTPING<br>TRIGGER59|FSI_TXx.EXTPING<br>TRIGGER59|ICSSM.PR1_SLV_I<br>NTR.20|
|OUTPUTXBAR.Out5|LIN1_RXD_PAD|FSI_TXx.EXTTRIG<br>GER58|FSI_TXx.EXTPING<br>TRIGGER58|FSI_TXx.EXTPING<br>TRIGGER58|ICSSM.PR1_SLV_I<br>NTR.21|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 927 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

|**OUTPUTXBAR Outputs**|**Destination-1**|**Destination-2**|**Destination-3**|**Destination-3**|**Destination-4**|
|---|---|---|---|---|---|
|OUTPUTXBAR.Out6|LIN1_TXD_PAD|FSI_TXx.EXTTRIG<br>GER57|FSI_TXx.EXTPING<br>TRIGGER57|FSI_TXx.EXTPING<br>TRIGGER57|ICSSM.PR1_SLV_I<br>NTR.22|
|OUTPUTXBAR.Out7|I2C1_SCL_PAD|FSI_TXx.EXTTRIG<br>GER56|FSI_TXx.EXTPING<br>TRIGGER56|FSI_TXx.EXTPING<br>TRIGGER56|ICSSM.PR1_SLV_I<br>NTR.23|
|OUTPUTXBAR.Out8|I2C1_SDA_PAD|FSI_TXx.EXTTRIG<br>GER55|FSI_TXx.EXTPING<br>TRIGGER55|FSI_TXx.EXTPING<br>TRIGGER55|ICSSM.PR1_SLV_I<br>NTR.24|
|OUTPUTXBAR.Out9|UART0_RTSn_PAD|FSI_TXx.EXTTRIG<br>GER54|FSI_TXx.EXTPING<br>TRIGGER54|FSI_TXx.EXTPING<br>TRIGGER54|ICSSM.PR1_SLV_I<br>NTR.25|
|OUTPUTXBAR.Out10|UART0_CTSn_PAD|FSI_TXx.EXTTRIG<br>GER53|FSI_TXx.EXTPING<br>TRIGGER53|FSI_TXx.EXTPING<br>TRIGGER53|ICSSM.PR1_SLV_I<br>NTR.26|
|OUTPUTXBAR.Out11|PR0_PRU1_GPIO1<br>3_PAD|FSI_TXx.EXTTRIG<br>GER52|FSI_TXx.EXTPING<br>TRIGGER52|FSI_TXx.EXTPING<br>TRIGGER52|ICSSM.PR1_SLV_I<br>NTR.27|
|OUTPUTXBAR.Out12|PR0_PRU1_GPIO1<br>4_PAD|FSI_TXx.EXTTRIG<br>GER51|FSI_TXx.EXTPING<br>TRIGGER51|FSI_TXx.EXTPING<br>TRIGGER51|ICSSM.PR1_SLV_I<br>NTR.28|
|OUTPUTXBAR.Out13|PR0_PRU1_GPIO1<br>9_PAD|FSI_TXx.EXTTRIG<br>GER50|FSI_TXx.EXTPING<br>TRIGGER50|FSI_TXx.EXTPING<br>TRIGGER50|ICSSM.PR1_SLV_I<br>NTR.29|
|OUTPUTXBAR.Out14|PR0_PRU1_GPIO1<br>8_PAD|FSI_TXx.EXTTRIG<br>GER49|FSI_TXx.EXTPING<br>TRIGGER49|FSI_TXx.EXTPING<br>TRIGGER49|ICSSM.PR1_SLV_I<br>NTR.30|
|OUTPUTXBAR.Out15|EXT_REFCLK0_PA<br>D|FSI_TXx.EXTTRIG<br>GER48|FSI_TXx.EXTPING<br>TRIGGER48|FSI_TXx.EXTPING<br>TRIGGER48|ICSSM.PR1_SLV_I<br>NTR.31|



928 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.5.11.7.1 OUTPUTXBAR Input Connection Table**_ 

|**Group0**<br>**Input**|**Source**<br>**Module-Signal**|**Group1**<br>**Input**|**Source**<br>**Module-Signal**|**Group2**<br>**Input**|**Source**<br>**Module-Signal**|**Group3**<br>**Input**|**Source**<br>**Module-Signal**|**Group4**<br>**Input**|**Source**<br>**Module-Signal**|
|---|---|---|---|---|---|---|---|---|---|
|G0-0|EPWM0-TRIPOUT|G1-0|EPWM0-SOCA|G2-0|EPWM0-SOCB|G3-0|DEL0-ACTIVE|G4-0|DEL0-TRIP|
|G0-1|EPWM1-TRIPOUT|G1-1|EPWM1-SOCA|G2-1|EPWM1-SOCB|G3-1|DEL1-ACTIVE|G4-1|DEL1-TRIP|
|G0-2|EPWM2-TRIPOUT|G1-2|EPWM2-SOCA|G2-2|EPWM2-SOCB|G3-2|DEL2-ACTIVE|G4-2|DEL2-TRIP|
|G0-3|EPWM3-TRIPOUT|G1-3|EPWM3-SOCA|G2-3|EPWM3-SOCB|G3-3|DEL3-ACTIVE|G4-3|DEL3-TRIP|
|G0-4|EPWM4-TRIPOUT|G1-4|EPWM4-SOCA|G2-4|EPWM4-SOCB|G3-4|DEL4-ACTIVE|G4-4|DEL4-TRIP|
|G0-5|EPWM5-TRIPOUT|G1-5|EPWM5-SOCA|G2-5|EPWM5-SOCB|G3-5|DEL5-ACTIVE|G4-5|DEL5-TRIP|
|G0-6|EPWM6-TRIPOUT|G1-6|EPWM6-SOCA|G2-6|EPWM6-SOCB|G3-6|DEL6-ACTIVE|G4-6|DEL6-TRIP|
|G0-7|EPWM7-TRIPOUT|G1-7|EPWM7-SOCA|G2-7|EPWM7-SOCB|G3-7|DEL7-ACTIVE|G4-7|DEL7-TRIP|
|G0-8|EPWM8-TRIPOUT|G1-8|EPWM8-SOCA|G2-8|EPWM8-SOCB|G3-8|DEL8-ACTIVE|G4-8|DEL8-TRIP|
|G0-9|EPWM9-TRIPOUT|G1-9|EPWM9-SOCA|G2-9|EPWM9-SOCB|G3-9|DEL9-ACTIVE|G4-9|DEL9-TRIP|
|G0-10|EPWM10-TRIPOUT|G1-10|EPWM10-SOCA|G2-10|EPWM10-SOCB|G3-10|DEL10-ACTIVE|G4-10|DEL10-TRIP|
|G0-11|EPWM11-TRIPOUT|G1-11|EPWM11-SOCA|G2-11|EPWM11-SOCB|G3-11|DEL11-ACTIVE|G4-11|DEL11-TRIP|
|G0-12|EPWM12-TRIPOUT|G1-12|EPWM12-SOCA|G2-12|EPWM12-SOCB|G3-12|DEL12-ACTIVE|G4-12|DEL12-TRIP|
|G0-13|EPWM13-TRIPOUT|G1-13|EPWM13-SOCA|G2-13|EPWM13-SOCB|G3-13|DEL13-ACTIVE|G4-13|DEL13-TRIP|
|G0-14|EPWM14-TRIPOUT|G1-14|EPWM14-SOCA|G2-14|EPWM14-SOCB|G3-14|DEL14-ACTIVE|G4-14|DEL14-TRIP|
|G0-15|EPWM15-TRIPOUT|G1-15|EPWM15-SOCA|G2-15|EPWM15-SOCB|G3-15|DEL15-ACTIVE|G4-15|DEL15-TRIP|
|G0-16|EPWM16-TRIPOUT|G1-16|EPWM16-SOCA|G2-16|EPWM16-SOCB|G3-16|DEL16-ACTIVE|G4-16|DEL16-TRIP|
|G0-17|EPWM17-TRIPOUT|G1-17|EPWM17-SOCA|G2-17|EPWM17-SOCB|G3-17|DEL17-ACTIVE|G4-17|DEL17-TRIP|
|G0-18|EPWM18-TRIPOUT|G1-18|EPWM18-SOCA|G2-18|EPWM18-SOCB|G3-18|DEL18-ACTIVE|G4-18|DEL18-TRIP|
|G0-19|EPWM19-TRIPOUT|G1-19|EPWM19-SOCA|G2-19|EPWM19-SOCB|G3-19|DEL19-ACTIVE|G4-19|DEL19-TRIP|
|G0-20|EPWM20-TRIPOUT|G1-20|EPWM20-SOCA|G2-20|EPWM20-SOCB|G3-20|DEL20-ACTIVE|G4-20|DEL20-TRIP|
|G0-21|EPWM21-TRIPOUT|G1-21|EPWM21-SOCA|G2-21|EPWM21-SOCB|G3-21|DEL21-ACTIVE|G4-21|DEL21-TRIP|
|G0-22|EPWM22-TRIPOUT|G1-22|EPWM22-SOCA|G2-22|EPWM22-SOCB|G3-22|DEL22-ACTIVE|G4-22|DEL22-TRIP|
|G0-23|EPWM23-TRIPOUT|G1-23|EPWM23-SOCA|G2-23|EPWM23-SOCB|G3-23|DEL23-ACTIVE|G4-23|DEL23-TRIP|
|G0-24|EPWM24-TRIPOUT|G1-24|EPWM24-SOCA|G2-24|EPWM24-SOCB|G3-24|DEL24-ACTIVE|G4-24|DEL24-TRIP|
|G0-25|EPWM25-TRIPOUT|G1-25|EPWM25-SOCA|G2-25|EPWM25-SOCB|G3-25|DEL25-ACTIVE|G4-25|DEL25-TRIP|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 929 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

|**Group0**<br>**Input**|**Source**<br>**Module-Signal**|**Group1**<br>**Input**|**Source**<br>**Module-Signal**|**Group2**<br>**Input**|**Source**<br>**Module-Signal**|**Group3**<br>**Input**|**Source**<br>**Module-Signal**|**Group4**<br>**Input**|**Source**<br>**Module-Signal**|
|---|---|---|---|---|---|---|---|---|---|
|G0-26|EPWM26-TRIPOUT|G1-26|EPWM26-SOCA|G2-26|EPWM26-SOCB|G3-26|DEL26-ACTIVE|G4-26|DEL26-TRIP|
|G0-27|EPWM27-TRIPOUT|G1-27|EPWM27-SOCA|G2-27|EPWM27-SOCB|G3-27|DEL27-ACTIVE|G4-27|DEL27-TRIP|
|G0-28|EPWM28-TRIPOUT|G1-28|EPWM28-SOCA|G2-28|EPWM28-SOCB|G3-28|DEL28-ACTIVE|G4-28|DEL28-TRIP|
|G0-29|EPWM29-TRIPOUT|G1-29|EPWM29-SOCA|G2-29|EPWM29-SOCB|G3-29|DEL29-ACTIVE|G4-29|DEL29-TRIP|
|G0-30|EPWM30-TRIPOUT|G1-30|EPWM30-SOCA|G2-30|EPWM30-SOCB|G3-30|DEL30-ACTIVE|G4-30|DEL30-TRIP|
|G0-31|EPWM31-TRIPOUT|G1-31|EPWM31-SOCA|G2-31|EPWM31-SOCB|G3-31|DEL31-ACTIVE|G4-31|DEL31-TRIP|



|**Group5**<br>**Input**|**Source**<br>**Module-Signal**|**Group6**<br>**Input**|**Source**<br>**Module-Signal**|**Group7**<br>**Input**|**Source**<br>**Module-Signal**|**Group8**<br>**Input**|**Source**<br>**Module-Signal**|**Group9**<br>**Input**|**Source**<br>**Module-Signal**|**Group10**<br>**Input**|**Source**<br>**Module-Signal**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|G5-0|SD0-FILT1COMPH|G6-0|CMP12SSA0-<br>CTRIPOUTL|G7-0|CMP12SSB0-<br>CTRIPOUTL|G8-0|ADC0-EVT1|G9-0|PWMSYNCOUTXBAR<br>-SYNCOUT0|G10-0|FSIRX0_TRIG0|
|G5-1|SD0-FILT1COMPL|G6-1|CMP12SSA0-<br>CTRIPOUTH|G7-1|CMP12SSB0-<br>CTRIPOUTH|G8-1|ADC0-EVT2|G9-1|PWMSYNCOUTXBAR<br>-SYNCOUT1|G10-1|FSIRX0_TRIG0|
|G5-2|SD0-FILT1COMPZ|G6-2|CMP12SSA1-<br>CTRIPOUTL|G7-2|CMP12SSB1-<br>CTRIPOUTL|G8-2|ADC0-EVT3|G9-2|PWMSYNCOUTXBAR<br>-SYNCOUT2|G10-2|FSIRX0_TRIG0|
|G5-3|SD0-FILT2COMPH|G6-3|CMP12SSA1-<br>CTRIPOUTH|G7-3|CMP12SSB1-<br>CTRIPOUTH|G8-3|ADC0-EVT4|G9-3|PWMSYNCOUTXBAR<br>-SYNCOUT3|G10-3|FSIRX0_TRIG0|
|G5-4|SD0-FILT2COMPL|G6-4|CMP12SSA2-<br>CTRIPOUTL|G7-4|CMP12SSB2-<br>CTRIPOUTL|G8-4|ADC1-EVT1|G9-4|EQEP0-I_OUT|G10-4|FSIRX0_TRIG1|
|G5-5|SD0-FILT2COMPZ|G6-5|CMP12SSA2-<br>CTRIPOUTH|G7-5|CMP12SSB2-<br>CTRIPOUTH|G8-5|ADC1-EVT2|G9-5|EQEP0-S_OUT|G10-5|FSIRX0_TRIG1|
|G5-6|SD0-FILT3COMPH|G6-6|CMP12SSA3-<br>CTRIPOUTL|G7-6|CMP12SSB3-<br>CTRIPOUTL|G8-6|ADC1-EVT3|G9-6|EQEP1-I_OUT|G10-6|FSIRX0_TRIG1|
|G5-7|SD0-FILT3COMPL|G6-7|CMP12SSA3-<br>CTRIPOUTH|G7-7|CMP12SSB3-<br>CTRIPOUTH|G8-7|ADC1-EVT4|G9-7|EQEP1-S_OUT|G10-7|FSIRX0_TRIG1|
|G5-8|SD0-FILT3COMPZ|G6-8|CMP12SSA4-<br>CTRIPOUTL|G7-8|CMP12SSB4-<br>CTRIPOUTL|G8-8|ADC2-EVT1|G9-8|EQEP2-I_OUT|G10-8|FSIRX0_TRIG2|
|G5-9|SD0-FILT4COMPH|G6-9|CMP12SSA4-<br>CTRIPOUTH|G7-9|CMP12SSB4-<br>CTRIPOUTH|G8-9|ADC2-EVT2|G9-9|EQEP2-S_OUT|G10-9|FSIRX0_TRIG2|
|G5-10|SD0-FILT4COMPL|G6-10|CMP12SSA5-<br>CTRIPOUTL|G7-10|CMP12SSB5-<br>CTRIPOUTL|G8-10|ADC2-EVT3|G9-10|ECAP0-OUT|G10-10|FSIRX0_TRIG2|
|G5-11|SD0-FILT4COMPZ|G6-11|CMP12SSA5-<br>CTRIPOUTH|G7-11|CMP12SSB5-<br>CTRIPOUTH|G8-11|ADC2-EVT4|G9-11|ECAP1-OUT|G10-11|FSIRX0_TRIG2|
|G5-12|SD1-FILT1COMPH|G6-12|CMP12SSA6-<br>CTRIPOUTL|G7-12|CMP12SSB6-<br>CTRIPOUTL|G8-12|ADC3-EVT1|G9-12|ECAP2-OUT|G10-12|FSIRX0_TRIG3|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

930 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

|**Group5**<br>**Input**|**Source**<br>**Module-Signal**|**Group6**<br>**Input**|**Source**<br>**Module-Signal**|**Group7**<br>**Input**|**Source**<br>**Module-Signal**|**Group8**<br>**Input**|**Source**<br>**Module-Signal**|**Group9**<br>**Input**|**Source**<br>**Module-Signal**|**Group10**<br>**Input**|**Source**<br>**Module-Signal**|
|---|---|---|---|---|---|---|---|---|---|---|---|
|G5-13|SD1-FILT1COMPL|G6-13|CMP12SSA6-<br>CTRIPOUTH|G7-13|CMP12SSB6-<br>CTRIPOUTH|G8-13|ADC3-EVT2|G9-13|ECAP3-OUT|G10-13|FSIRX0_TRIG3|
|G5-14|SD1-FILT1COMPZ|G6-14|CMP12SSA7-<br>CTRIPOUTL|G7-14|CMP12SSB7-<br>CTRIPOUTL|G8-14|ADC3-EVT3|G9-14|ECAP4-OUT|G10-14|FSIRX0_TRIG3|
|G5-15|SD1-FILT2COMPH|G6-15|CMP12SSA7-<br>CTRIPOUTH|G7-15|CMP12SSB7-<br>CTRIPOUTH|G8-15|ADC3-EVT4|G9-15|ECAP5-OUT|G10-15|FSIRX0_TRIG3|
|G5-16|SD1-FILT2COMPL|G6-16|CMP12SSA8-<br>CTRIPOUTL|G7-16|CMP12SSB8-<br>CTRIPOUTL|G8-16|ADC4-EVT1|G9-16|ECAP6-OUT|G10-16|INPUTXBAR_OUT7|
|G5-17|SD1-FILT2COMPZ|G6-17|CMP12SSA8-<br>CTRIPOUTH|G7-17|CMP12SSB8-<br>CTRIPOUTH|G8-17|ADC4-EVT2|G9-17|ECAP7-OUT|G10-17|INPUTXBAR_OUT15|
|G5-18|SD1-FILT3COMPH|G6-18|CMP12SSA9-<br>CTRIPOUTL|G7-18|CMP12SSB9-<br>CTRIPOUTL|G8-18|ADC4-EVT3|G9-18|ECAP8-OUT|G10-18|INPUTXBAR_OUT23|
|G5-19|SD1-FILT3COMPL|G6-19|CMP12SSA9-<br>CTRIPOUTH|G7-19|CMP12SSB9-<br>CTRIPOUTH|G8-19|ADC4-EVT4|G9-19|ECAP9-OUT|G10-19|INPUTXBAR_OUT31|
|G5-20|SD1-FILT3COMPZ|-|-|-|-|G8-20|ADCR0-EVT1|G9-20|ECAP10-OUT|G10-20|INPUTXBAR_OUT7|
|G5-21|SD1-FILT4COMPH|-|-|-|-|G8-21|ADCR0-EVT2|G9-21|ECAP11-OUT|G10-21|INPUTXBAR_OUT15|
|G5-22|SD1-FILT4COMPL|-|-|-|-|G8-22|ADCR0-EVT3|G9-22|ECAP12-OUT|-|-|
|G5-23|SD1-FILT4COMPZ|-|-|-|-|G8-23|ADCR0-EVT4|G9-23|ECAP13-OUT|-|-|
|-|-|-|-|-|-|G8-24|ADCR1-EVT1|G9-24|ECAP14-OUT|-|-|
|-|-|-|-|-|-|G8-25|ADCR1-EVT2|G9-25|ECAP15-OUT|-|-|
|-|-|-|-|-|-|G8-26|ADCR1-EVT3|-|-|-|-|
|-|-|-|-|-|-|G8-27|ADCR1-EVT4|-|-|-|-|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 931 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.5.11.8 PWMSYNCOUTXBAR** 

On this device, the PWM SyncOut x-bar is used to route signals from ePWM(s) sync output(s) to Output x-bar and SoC time sync logic. 

The PWM SyncOut x-bar configured by way of the PWMSyncOutXBar[3:0].G[1:0].SEL registers. The available IP sources for each input is shown in PWMSYNCOUTXBAR figure below while the PWM SyncOut x-bar destinations is shown in the table below. 

**==> picture [483 x 107] intentionally omitted <==**

**----- Start of picture text -----**<br>
Repeated x4<br>32 G0.0 PWMSyncOutXBar.G0.SEL[0]<br>Inputs G0.31<br>PWMSyncOutXBar.G0.SEL[31]<br>G0.0 PWMSyncOutXBar.Out[x]<br>All EPWM All SYNCOUT Signals PWM SyncOut XBar 0 PWMSyncOutXBar.Out[0] G1.0<br>G0.31 16 PWMSyncOutXBar.G1.SEL[0]<br>PWM SyncOut XBar 1 PWMSyncOutXBar.Out[1] Inputs G1.15 PWMSyncOutXBar.G1.SEL[15]<br>G1.0 PWM SyncOut XBar 2 PWMSyncOutXBar.Out[2] Note:  An unselected signal feeds 0 to OR gate input.<br>All ECAP All SYNCOUT Signals G1.15 PWM SyncOut XBar 3 PWMSyncOutXBar.Out[3]<br>**----- End of picture text -----**<br>


**Figure 7-387. PWMSYNCOUT XBAR Block diagram** 

|**PWMSYNCOUTXBAR Outputs**|**Destination-1**|**Destination-2**|
|---|---|---|
|PWMSYNCOUTXBAR.Out0|OUTPUTXBAR.G9.0|SOC_TIMESYNC_XBAR1.IN_IN<br>TR6|
|PWMSYNCOUTXBAR.Out1|OUTPUTXBAR.G9.1|SOC_TIMESYNC_XBAR1.IN_IN<br>TR7|
|PWMSYNCOUTXBAR.Out2|OUTPUTXBAR.G9.2|SOC_TIMESYNC_XBAR1.IN_IN<br>TR8|
|PWMSYNCOUTXBAR.Out3|OUTPUTXBAR.G9.3|SOC_TIMESYNC_XBAR1.IN_IN<br>TR9|



## **7.5.11.9 XBAR Programming Guide** 

## **Driver Information** 

Driver features are available at the XBAR driver page. 

## **Software API Information** 

The XBAR driver provides an API to configure the XBAR module. Full documentation is located on APIs for XBAR. 

932 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

