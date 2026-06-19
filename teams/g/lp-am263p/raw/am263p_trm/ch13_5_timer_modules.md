<!-- AM263P TRM | 13.5 Timer Modules (RTI/WWDT) | 원본 p.1596-1621 | pymupdf4llm text+tables, images omitted -->

_Peripherals_ 

www.ti.com 

## **13.5 Timer Modules** 

This section describes the timer modules in the device. 

## _**13.5.1 Real Time Interrupts/Windowed Watchdog Timer (RTI/WWDT)**_ 

This section describes the Real Time Interrupt/Windowed Watchdog Timer (RTI/WWDT) module implemented in the device. 

## **13.5.1.1 RTI/WWDT Overview** 

The Real Time Interrupt module of the RTI/WWDT module provides general timer functionality for operating systems and for benchmarking code. The module incorporates several counters, which define the timebases needed for operating system-based scheduling requirements. 

This module is specifically designed to fulfill the requirements for OSEK (“Offene Systeme und deren Schnittstellen für die Elektronik im Kraftfahrzeug”; “Open Systems and the Corresponding Interfaces for Automotive Electronics”) as well as OSEK/Time compliant operating systems. 

The timers also provide the ability to benchmark certain areas of code by reading the counter contents at the beginning and the end of the desired code range and calculating the difference between the values. 

There are eight RTI modules in the device and four WWDT modules in the device. Table 13-233 shows the RTI 

allocation across device domains. 

## **Note** 

Eight instances are configured in RTI-only mode to function as general purpose timers. Another four instances are configured in WWDT-only mode to function as watchdog timers. 

## **Table 13-233. RTI Device Instance Table** 

|**Instance**|**Device**||
|---|---|---|
|RTI0||✓|
|RTI1||✓|
|RTI2||✓|
|RTI3||✓|
|RTI4||✓|
|RTI5||✓|
|RTI6||✓|



1596 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-233. RTI Device Instance Table (continued)** 

|**Instance**|**Device**||
|---|---|---|
|RTI7||✓|



This diagram shows the module overview. 

**==> picture [337 x 407] intentionally omitted <==**

**Figure 13-211. RTI Overview** 

# = 0 to 7 # = 0, 1, 2, 3 

Table 13-234 shows the WWDT allocation across device domains. 

**Table 13-234. WWDT Device Instance Table** 

|**Instance**|**Device**|
|---|---|
|WWDT0|✓|
|WWDT1|✓|
|WWDT2|✓|
|WWDT3|✓|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1597 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

The WWDT instances are intended to function as a digital windowed watchdog for the CPU core that they are associated with: 

- WWDT0 is dedicated to the first R5F CPU core (R5FSS0_CORE0) 

- WWDT1 is dedicated to the second R5F CPU core (R5FSS0_CORE1) 

- WWDT2 is dedicated to the third R5F CPU core (R5FSS1_CORE0) 

- WWDT3 is dedicated to the fourth R5F CPU core (R5FSS1_CORE1) 

All WWDT instances that are provisioned for a particular CPU core should not be used by any other CPU cores. 

**==> picture [348 x 347] intentionally omitted <==**

**Figure 13-212. WWDT Overview** 

## _**13.5.1.1.1 RTI Features**_ 

The RTI modules include the following main features: 

- Windowed Watchdog Timer (WWDT) feature. 

- Two independent 64 bit counter blocks (counter block0 or counter block1). Each block consists of 

   - One 32 bit up counter 

   - One 32 bit free running counter 

   - Two capture registers for capturing the prescale and free running counter on a special event. 

- Free running counter 0 can be incremented by the internal prescale counter. 

- Four configurable compare registers for generating operating system ticks . Each event can be driven by either counter block0 or counter block1. 

- Fast enabling/disabling of events. 

- RTI clock input derived from any of the available clock sources, selectable in the System Module 

1598 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- Optional capability to drive a pulse-width modulated signal out on an interrupt line to the ESM and VIM. 

- DMA requests and events for the RTI-only modules 

## _**13.5.1.1.2 RTI Unsupported Features**_ 

The RTI modules do not support the following features: 

- External clock supervising circuit to switch to internal prescale counter 0, if external clock source fails to increment in a predefined window. 

- DMA requests and events fort the WWDT only modules. 

- Automatic update of all compare registers on compare match to generate periodic interrupts. 

- Capture events to capture timestamps through recording of timer status. 

- Two time-stamp (capture) functions for system or peripheral interrupts, one for each counter block. 

- Analog Watchdog via external RC Network to prevent for runaway code. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1599 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.5.1.2 RTI Integration** 

There are 8x RTI modules integrated in the device. The diagram and tables below show the device integration details. 

## **Figure 13-213. RTI Integration** 

The tables below summarize the integration of RTI# (where # = 0, 1, 2, 3, 4, 5, 6, 7) in the device. Each RTI# instance is supplied by dedicated RTICLK# mux. 

**==> picture [468 x 276] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device RTI #<br>RTI#_VBUSCLK RTI#_DMA[0:3] EDMA<br>SYSCLK<br>XTALCLK<br>EXT_REFCLK RTI0_INT_REQ[0] ADCTRIG1<br>PER_PLL_HSDIV0_CLKOUT1 RTI1_INT_REQ[0] ADCTRIG2<br>RTI#_CLK<br>CORE_PLL_HSDIV0_CLKOUT1 RTI2_INT_REQ[0] ADCTRIG3<br>RCCLK(10MHz)<br>XTALCLK RTI3_INT_REQ[0] ADCTRIG4<br>CPTS_GENF0 RTI4_INT_REQ[0] ADCTRIG5<br>RTI5_INT_REQ[0] ADCTRIG6<br>RCM RTI#_CAPEVT[0:1] RTI6_INT_REQ[0] ADCTRIG7<br>RTI#_CLK_SRC_SE L RTI7_INT_REQ[0] ADCTRIG8<br>RTI#_CLK_DIV_VA L RTI#_INT_REQ[0:3] R5FSS0-CORE0<br>RTI#_RST_CTR L<br>RTI#_WARMRESET<br>Warm Reset Sources R5FSS0-CORE1<br>RTI#_OVERFLOW[0:1]<br>Interrupts<br>PORz RTI#_POR R5FSS1-CORE0<br>R5FSS1-CORE0<br>PERI VBUSP Interconnect<br>DMA  XBAR<br>TIMESYNC XBAR CONTROLSS<br>**----- End of picture text -----**<br>


**Figure 13-214. RTI Integration Diagram** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|RTI0|✓|VBUSP CORE Interconnect|
|RTI1|✓|VBUSP CORE Interconnect|
|RTI2|✓|VBUSP CORE Interconnect|
|RTI3|✓|VBUSP CORE Interconnect|
|RTI4|✓|VBUSP CORE Interconnect|



1600 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|RTI5|✓|VBUSP CORE Interconnect|
|RTI6|✓|VBUSP CORE Interconnect|
|RTI7|✓|VBUSP CORE Interconnect|



## **Table 13-235.** _**RTI**_ **Clocks** 

This table table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|RTI0|RTI0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI0 VBUSP Interface<br>Clock|
||RTI0_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI0 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||
|RTI1|RTI1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI1 VBUSP Interface<br>Clock|
||RTI1_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI1 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1601 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-235.** _**RTI**_ **Clocks (continued)** 

This table table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|RTI2|RTI2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI2 VBUSP Interface<br>Clock|
||RTI2_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI2 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||
|RTI3|RTI3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI3 VBUSP Interface<br>Clock|
||RTI3_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI3 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||



1602 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-235.** _**RTI**_ **Clocks (continued)** 

This table table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|RTI4|RTI4_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI4 VBUSP Interface<br>Clock|
||RTI4_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI4 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||
|RTI5|RTI5_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI5 VBUSP Interface<br>Clock|
||RTI5_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI5 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1603 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-235.** _**RTI**_ **Clocks (continued)** 

This table table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|RTI6|RTI6_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI6 VBUSP Interface<br>Clock|
||RTI6_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI6 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||
|RTI7|RTI7_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI7 VBUSP Interface<br>Clock|
||RTI7_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI7 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||



**Table 13-236.** _**RTI**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|RTI0|RTI0_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI0 Asynchronous Reset|
||RTI0_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI0 Power-On Reset|



1604 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-236.** _**RTI**_ **Resets (continued)** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|RTI1|RTI1_RST<br>RTI1_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI1 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI1 Power-On Reset|
|RTI2|RTI2_RST<br>RTI2_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI2 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI2 Power-On Reset|
|RTI3|RTI3_RST<br>RTI3_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI3 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI3 Power-On Reset|
|RTI4|RTI4_RST<br>RTI4_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI4 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI4 Power-On Reset|
|RTI5|RTI5_RST<br>RTI5_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI5 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI5 Power-On Reset|
|RTI6|RTI6_RST<br>RTI6_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI6 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI6 Power-On Reset|
|RTI7|RTI7_RST<br>RTI7_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI7 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI7 Power-On Reset|



**Table 13-237.** _**RTI**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|RTI0|RTI0_INT_REQ_0|RTI0_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI0 Status Event Interrupt|
||RTI0_INT_REQ_1|RTI0_INT_REQ_1||||
||RTI0_INT_REQ_2|RTI0_INT_REQ_2||||
||RTI0_INT_REQ_3|RTI0_INT_REQ_3||||
||RTI0_OVL_REQ_0|RTI0_OVERFLOW_LEVEL_0|||RTI0 Counter Overflow Event<br>Interrupt|
||RTI0_OVL_REQ_1|RTI0_OVERFLOW_LEVEL_1||||
|RTI1|RTI1_INT_REQ_0|RTI1_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI1 Status Event Interrupt|
||RTI1_INT_REQ_1|RTI1_INT_REQ_1||||
||RTI1_INT_REQ_2|RTI1_INT_REQ_2||||
||RTI1_INT_REQ_3|RTI1_INT_REQ_3||||
||RTI1_OVL_REQ_0|RTI1_OVERFLOW_LEVEL_0|||RTI1 Counter Overflow Event<br>Interrupt|
||RTI1_OVL_REQ_1|RTI1_OVERFLOW_LEVEL_1||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1605 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-237.** _**RTI**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|RTI2|RTI2_INT_REQ_0|RTI2_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI2 Status Event Interrupt|
||RTI2_INT_REQ_1|RTI2_INT_REQ_1||||
||RTI2_INT_REQ_2|RTI2_INT_REQ_2||||
||RTI2_INT_REQ_3|RTI2_INT_REQ_3||||
||RTI2_OVL_REQ_0|RTI2_OVERFLOW_LEVEL_0|||RTI2 Counter Overflow Event<br>Interrupt|
||RTI2_OVL_REQ_1|RTI2_OVERFLOW_LEVEL_1||||
|RTI3|RTI3_INT_REQ_0|RTI3_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI3 Status Event Interrupt|
||RTI3_INT_REQ_1|RTI3_INT_REQ_1||||
||RTI3_INT_REQ_2|RTI3_INT_REQ_2||||
||RTI3_INT_REQ_3|RTI3_INT_REQ_3||||
||RTI3_OVL_REQ_0|RTI3_OVERFLOW_LEVEL_0|||RTI3 Counter Overflow Event<br>Interrupt|
||RTI3_OVL_REQ_1|RTI3_OVERFLOW_LEVEL_1||||
|RTI4|RTI4_INT_REQ_0|RTI4_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI4 Status Event Interrupt|
||RTI4_INT_REQ_1|RTI4_INT_REQ_1||||
||RTI4_INT_REQ_2|RTI4_INT_REQ_2||||
||RTI4_INT_REQ_3|RTI4_INT_REQ_3||||
||RTI4_OVL_REQ_0|RTI4_OVERFLOW_LEVEL_0|||RTI4 Counter Overflow Event<br>Interrupt|
||RTI4_OVL_REQ_1|RTI4_OVERFLOW_LEVEL_1||||
|RTI5|RTI5_INT_REQ_0|RTI5_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI5 Status Event Interrupt|
||RTI5_INT_REQ_1|RTI5_INT_REQ_1||||
||RTI5_INT_REQ_2|RTI5_INT_REQ_2||||
||RTI5_INT_REQ_3|RTI5_INT_REQ_3||||
||RTI5_OVL_REQ_0|RTI5_OVERFLOW_LEVEL_0|||RTI5 Counter Overflow Event<br>Interrupt|
||RTI5_OVL_REQ_1|RTI5_OVERFLOW_LEVEL_1||||
|RTI6|RTI6_INT_REQ_0|RTI6_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI6 Status Event Interrupt|
||RTI6_INT_REQ_1|RTI6_INT_REQ_1||||
||RTI6_INT_REQ_2|RTI6_INT_REQ_2||||
||RTI6_INT_REQ_3|RTI6_INT_REQ_3||||
||RTI6_OVL_REQ_0|RTI6_OVERFLOW_LEVEL_0|||RTI6 Counter Overflow Event<br>Interrupt|
||RTI6_OVL_REQ_1|RTI6_OVERFLOW_LEVEL_1||||
|RTI7|RTI7_INT_REQ_0|RTI7_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI7 Status Event Interrupt|
||RTI7_INT_REQ_1|RTI7_INT_REQ_1||||
||RTI7_INT_REQ_2|RTI7_INT_REQ_2||||
||RTI7_INT_REQ_3|RTI7_INT_REQ_3||||
||RTI7_OVL_REQ_0|RTI7_OVERFLOW_LEVEL_0|||RTI7 Counter Overflow Event<br>Interrupt|
||RTI7_OVL_REQ_1|RTI7_OVERFLOW_LEVEL_1||||



1606 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-238.** _**RTI**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|RTI0|RTI0_DMA_0|RTI0_DMA_REQ_0|EDMA Crossbar<br>(EDMA_XBAR)|Pulse|RTI0 DMA Request|
||RTI0_DMA_1|RTI0_DMA_REQ_1||||
||RTI0_DMA_2|RTI0_DMA_REQ_2||||
||RTI0_DMA_3|RTI0_DMA_REQ_3||||
|RTI1|RTI1_DMA_0|RTI1_DMA_REQ_0|||RTI1 DMA Request|
||RTI1_DMA_1|RTI1_DMA_REQ_1||||
||RTI1_DMA_2|RTI1_DMA_REQ_2||||
||RTI1_DMA_3|RTI1_DMA_REQ_3||||
|RTI2|RTI2_DMA_0|RTI2_DMA_REQ_0|||RTI2 DMA Request|
||RTI2_DMA_1|RTI2_DMA_REQ_1||||
||RTI2_DMA_2|RTI2_DMA_REQ_2||||
||RTI2_DMA_3|RTI2_DMA_REQ_3||||
|RTI3|RTI3_DMA_0|RTI3_DMA_REQ_0|||RTI3 DMA Request|
||RTI3_DMA_1|RTI3_DMA_REQ_1||||
||RTI3_DMA_2|RTI3_DMA_REQ_2||||
||RTI3_DMA_3|RTI3_DMA_REQ_3||||
|RTI4|RTI4_DMA_0|RTI4_DMA_REQ_0|||RTI4 DMA Request|
||RTI4_DMA_1|RTI4_DMA_REQ_1||||
||RTI4_DMA_2|RTI4_DMA_REQ_2||||
||RTI4_DMA_3|RTI4_DMA_REQ_3||||
|RTI5|RTI5_DMA_0|RTI5_DMA_REQ_0|||RTI5 DMA Request|
||RTI5_DMA_1|RTI5_DMA_REQ_1||||
||RTI5_DMA_2|RTI5_DMA_REQ_2||||
||RTI5_DMA_3|RTI5_DMA_REQ_3||||
|RTI6|RTI6_DMA_0|RTI6_DMA_REQ_0|||RTI6 DMA Request|
||RTI6_DMA_1|RTI6_DMA_REQ_1||||
||RTI6_DMA_2|RTI6_DMA_REQ_2||||
||RTI6_DMA_3|RTI6_DMA_REQ_3||||
|RTI7|RTI7_DMA_0|RTI7_DMA_REQ_0|||RTI7 DMA Request|
||RTI7_DMA_1|RTI7_DMA_REQ_1||||
||RTI7_DMA_2|RTI7_DMA_REQ_2||||
||RTI7_DMA_3|RTI7_DMA_REQ_3||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1607 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-239.** _**RTI**_ **Capture Events** 

This table describes the module capture events. 

|**Module**<br>**Instance**|**Module Capture**<br>**Event Input**|**Capture Event Source Signal**|**Source**|**Type**|**Description**|
|---|---|---|---|---|---|
|RTI0|RTI0_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>2|SoC Time<br>Sync Crossbar<br>(TIMESYNC_XBAR)|Pulse|RTI0 Counter Capture Input Event|
||RTI0_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>3||||
|RTI1|RTI1_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>4|||RTI1 Counter Capture Input Event|
||RTI1_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>5||||
|RTI2|RTI2_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>6|||RTI2 Counter Capture Input Event|
||RTI2_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>7||||
|RTI3|RTI3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>8|||RTI3 Counter Capture Input Event|
||RTI3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>9||||
|RT4|RTI3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>12|||RTI4 Counter Capture Input Event|
||RTI3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>13||||
|RTI5|RTI3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>14|||RTI5 Counter Capture Input Event|
||RTI3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>15||||
|RTI6|RTI3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>16|||RTI6 Counter Capture Input Event|
||RTI3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>17||||
|RTI7|RTI3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>18|||RTI7 Counter Capture Input Event|
||RTI3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>19||||



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

1608 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.5.1.3 WWDT Integration** 

There are 4x WWDT modules integrated in the device. The diagram and tables below show the device integration details. 

**==> picture [496 x 362] intentionally omitted <==**

**Figure 13-215. WWDT Integration** 

The tables below summarize the integration of WWDT# (where # = 0, 1, 2, 3) in the device. 

Each WWDT# instance is supplied by dedicated WWDTCLK# mux. 

**Table 13-240.** _**WWDT**_ **Device Integration** 

## This table describes the module device integration details. 

|**Module**<br>**Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|WWDT0|✓|VBUSP CORE Interconnect|
|WWDT1|✓|VBUSP CORE Interconnect|
|WWDT2|✓|VBUSP CORE Interconnect|
|WWDT3|✓|VBUSP CORE Interconnect|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1609 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-241.** _**WWDT**_ **Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|WWDT0|WWDT0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|WWDT0 VBUSP Interface<br>Clock|
||WWDT0_FCLK<br>(WWDT_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|WWDT0 Functional Clock|
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||PER_PLL_HSDIV0_CLKO<br>UT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCOSC (32KHz)|Internal 32 KHz RC<br>Oscillator (RCCLK_32K)|32 KHz||
|WWDT1|WWDT1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|WWDT1 VBUSP Interface<br>Clock|
||WWDT1_FCLK<br>(WWDT_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|WWDT1 Functional Clock|
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||PER_PLL_HSDIV0_CLKO<br>UT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCOSC (32KHz)|Internal 32 KHz RC<br>Oscillator (RCCLK_32K)|32 KHz||



1610 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-241.** _**WWDT**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|WWDT2|WWDT2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|WWDT2 VBUSP Interface<br>Clock|
||WWDT2_FCLK<br>(WWDT_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|WWDT2 Functional Clock|
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||PER_PLL_HSDIV0_CLKO<br>UT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCOSC (32KHz)|Internal 32 KHz RC<br>Oscillator (RCCLK_32K)|32 KHz||
|WWDT3|WWDT3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|WWDT3 VBUSP Interface<br>Clock|
||WWDT3_FCLK<br>(WWDT_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|WWDT3 Functional Clock|
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||PER_PLL_HSDIV0_CLKO<br>UT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCOSC (32KHz)|Internal 32 KHz RC<br>Oscillator (RCCLK_32K)|32 KHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1611 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-242.** _**WWDT**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|WWDT0|WWDT0_RST|Warm Reset<br>(MOD_G_RST)|RCM Reset Control Register +<br>Warm Reset Sources|WWDT0 Asynchronous Reset|
||WWDT0_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|WWDT0 Power-On Reset|
|WWDT1|WWDT1_RST|Warm Reset<br>(MOD_G_RST)|RCM Reset Control Register +<br>Warm Reset Sources|WWDT1 Asynchronous Reset|
||WWDT1_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|WWDT1 Power-On Reset|
|WWDT2|WWDT2_RST|Warm Reset<br>(MOD_G_RST)|RCM Reset Control Register +<br>Warm Reset Sources|WWDT2 Asynchronous Reset|
||WWDT2_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|WWDT2 Power-On Reset|
|WWDT3|WWDT3_RST|Warm Reset<br>(MOD_G_RST)|RCM Reset Control Register +<br>Warm Reset Sources|WWDT3 Asynchronous Reset|
||WWDT3_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|WWDT3 Power-On Reset|



**Table 13-243.** _**WWDT**_ **Interrupt Requests** 

## This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|WWDT0|WWDT0_NMI_REQ|ESM0_PLS_IN_0|ESM0|Pulse|WWDT0 Window Watchdog<br>Violation Non-Maskable Interrupt<br>(NMI) Event|
|||R5FSS0_0_VIM_128|R5FSS0_CORE0|||
|WWDT1|WWDT1_NMI_REQ|ESM0_PLS_IN_1|ESM0|Pulse|WWDT1 Non-Maskable Interrupt<br>(NMI) Event|
|||R5FSS0_1_VIM_128|R5FSS0_CORE1|||
|WWDT2|WWDT2_NMI_REQ|ESM0_PLS_IN_2|ESM0|Pulse|WWDT2 Non-Maskable Interrupt<br>(NMI) Event|
|||R5FSS1_0_VIM_128|R5FSS1_CORE0|||
|WWDT3|WWDT3_NMI_REQ|ESM0_PLS_IN_3|ESM0|Pulse|WWDT3 Non-Maskable Interrupt<br>(NMI) Event|
|||R5FSS1_1_VIM_128|R5FSS1_CORE1|||



1612 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-244.** _**RTI**_ **Capture Events** 

This table describes the module capture events. 

|**Module**<br>**Instance**|**Module Capture**<br>**Event Input**|**Capture Event Source Signal**|**Source**|**Type**|**Description**|
|---|---|---|---|---|---|
|WWDT0|WWDT0_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>2|SoC Time<br>Sync Crossbar<br>(TIMESYNC_XBAR)|Level|WWDT0 Counter Capture Input<br>Event|
||WWDT0_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>3||||
|WWDT1|WWDT1_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>4|||WWDT1 Counter Capture Input<br>Event|
||WWDT1_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>5||||
|WWDT2|WWDT2_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>6|||WWDT2 Counter Capture Input<br>Event|
||WWDT2_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>7||||
|WWDT3|WWDT3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>8|||WWDT3 Counter Capture Input<br>Event|
||WWDT3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>9||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1613 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.5.1.4 RTI Functional Description** 

The RTI# and WWDT# (where # = 0, 1, 2, 3) modules are hereinafter referred to as RTI, RTI_WWDT, or RTI/WWDT. 

## _**13.5.1.4.1 RTI Digital Windowed Watchdog**_ 

## **Note** 

Some of the RTI features described in this section may not be supported on this family of devices. For more information, see _RTI Not Supported Features_ . 

## **Note** 

The following section only applies to the WWDT defined modules. 

## **Note** 

Digital windowed watchdog (DWWD) timer is implemented using the digital windowed watchdog function of the RTI modules. Real time interrupt functionality is not supported. In this mode, the timer should default to disabled and user can adjust the period as desired before enabling the watchdog. 

In addition to the time-out boundary configurable via the digital watchdog (DWD), some applications may also want to configure the start-time boundary of the watchdog. This is enabled by the digital windowed watchdog (DWWD) feature. 

## **Functional Behavior** 

The DWWD opens a configurable time window in which the watchdog must be serviced. Any attempt to service the watchdog outside this time window, or a failure to service the watchdog in this time window, will cause the watchdog to generate either a reset or a non-maskable interrupt to the CPU. This is controlled by configuring the RTI_WWDRXNCTRL register. As stated earlier, when the watchdog needs to be enabled by software, the watchdog counter is disabled on a system reset. When the DWWD is configured to generate a non-maskable interrupt on a window violation, the watchdog counter continues to count down. The RTI_INTR_WWD interrupt handler needs to clear the watchdog violation status flag(s) and then service the watchdog by writing the correct sequence in the watchdog key RTI_WDKEY register. This service will cause the watchdog counter to get reloaded from the preload value and start counting down. If the RTI_INTR_WWD handler does not service the watchdog in time, it could count down all the way to zero and wrap around. No second exception for a time out is generated in this case. 

## **Configuration of DWWD** 

The DWWD preload value (same as DWD preload) can only be configured when the DWWD counter is disabled. The window size and watchdog reaction to a violation can be configured even after the watchdog has been enabled. Any changes to the window size and watchdog reaction configurations will only take effect after the next servicing of the DWWD. 

1614 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [420 x 218] intentionally omitted <==**

**----- Start of picture text -----**<br>
DWD<br>Down Counter<br>100% window OPEN WINDOW OPEN WINDOW OPEN WINDOW<br>50% window<br>25% window<br>12.5% window<br>6.25% window<br>rti-008<br>**----- End of picture text -----**<br>


**Figure 13-216. RTI Digital Windowed Watchdog Timing Example** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1615 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [433 x 404] intentionally omitted <==**

**Figure 13-217. RTI Digital Windowed Watchdog Operation Block Diagram** 

## _**13.5.1.4.1.1 RTI Debug Mode Behavior**_ 

## **Note** 

Some of the RTI features described in this section may not be supported on this family of devices. For more information, see _RTI Not Supported Features_ . 

Once the system enters debug mode, the behavior of the RTI depends on the RTI_GCTRL[15] COS bit. If the bit is cleared and debug mode is active, all counters will stop operation. If the bit is set to one, all counters will be clocked normally and the RTI will work like in normal mode. 

The DWD counter will not decrement in debug mode and will hold its current value, regardless of the RTI_GCTRL[15] COS bit. 

1616 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

The user must not service the watchdog while in debug mode. 

## _**13.5.1.4.2 RTI Digital Watchdog**_ 

## **Note** 

Some of the RTI features described in this section may not be supported on this family of devices. For more information, see _RTI Not Supported Features_ . 

## **Note** 

The following section only applies to the WWDT defined modules. 

Some applications might use a digital watchdog (DWD) integrated in the RTI module. The digital watchdog generates resets after a programmable period, if no correct key sequence is written to the RTI_WDKEY register. Figure 13-218 shows the digital watchdog functional block. 

**==> picture [322 x 272] intentionally omitted <==**

**----- Start of picture text -----**<br>
to reset logic<br>DWD<br>15 0<br>WD FSM<br>RTIWDKEY<br>RESET<br>=0<br>15 0<br>Compare 16 bit<br>24 0 KEY[1-0] out of 2<br>Down Counter<br>RTI_FCLK<br>Suspend<br>nTRST<br>11 0 31 0 31 0<br>Down CounterDWD Preload DWD Ctrl = DWD hardwired<br>Code<br>rti-006<br>**----- End of picture text -----**<br>


**Figure 13-218. RTI Digital Watchdog Functional Block Diagram** 

The digital watchdog functionality is implemented such that it can be enabled by software. 

The DWD starts counting down from the reset value of the RTI_DWDCNTR (DWD Counter Register). The DWD preload register can be configured at any time by the application according to the desired time-out period. 

When enabled by software, the digital watchdog is disabled after system reset. If it should be used, it has to be enabled by writing A98559DAh to the RTI_DWDCTRL register. The DWD timeout period must be configured using the DWD preload register before the DWD is enabled. The DWD cannot be disabled by the application once it is enabled. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1617 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Note** 

When the DWD is enabled by software, any system reset will disable the DWD. This reset could have been generated by the watchdog itself. 

If the correct key sequence is written to the RTI_WDKEY register (E51Ah followed by A35Ch), the 25-bit DWD Down Counter is reloaded with the 12-bit preload value stored in RTI_DWDPRLD register. If any incorrect value is written to the RTI_WDKEY register, a watchdog reset will occur immediately. A reset will also be generated, when the DWD Down Counter is decremented to 0. 

The user has to take into account that the write to the RTI_WDKEY register takes 3 RTI_ICLK cycles. This needs to be considered for the DWD expiration calculation. 

The DWD Down Counter will be decremented with RTI_FCLK frequency. If the RTI_FCLK is switched off via the disable registers of the Clock management, the DWD counter stops decrementing. The DWD module cannot generate a reset under this condition. 

**==> picture [428 x 116] intentionally omitted <==**

**Figure 13-219. RTI Digital Watchdog Operation** 

The expiration time of the DWD Down Counter can be determined with following equation: 

texp= (RTI_DWDPRLD + 1) x 2[13] / RTI_FCLK 

(33) 

where RTI_DWDPRLD = 0...4095 

## _**13.5.1.4.3 RTI Counter Operation**_ 

## **Note** 

Some of the RTI features described in this section may not be supported on this family of devices. For more information, see _RTI Not Supported Features_ . 

Figure 13-220 shows the RTI module counter blocks. The RTI module supports two counter blocks. 

1618 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [496 x 399] intentionally omitted <==**

**----- Start of picture text -----**<br>
Counter block0<br>31 0<br>to Compare Block0<br>Compare Up<br>Counter<br>31 0 31 0<br>RTI_FCLK Up Counter0 = Free RunningCounter0 comparecontrol<br>31 0<br>Capture to Compare Block1<br>31 0 Free Running<br>Counter0<br>Capture Up<br>Counter0<br>compare<br>control<br>Counter block1 31 0<br>Compare Up<br>Counter<br>31 0 31 0<br>to Compare Block2<br>RTI_FCLK Up Counter1 = Free RunningCounter1<br>compare<br>31 0 control<br>Capture<br>31 0 Free Running<br>Counter1<br>Capture Up<br>Counter1<br>to Compare Block3<br>RTI_CAPCTRL source 0 External<br>RTI_CAPCTRL source 1 Control compare<br>control<br>rti-004<br>**----- End of picture text -----**<br>


**==> picture [17 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
rti-004<br>**----- End of picture text -----**<br>


**Figure 13-220. RTI Counters Block Diagram** 

Each block consists of two 32-bit up counters: Up Counter (UC), and Free Running Counter (FRC). The Up Counter (RTI_UC0 or RTI_UC1 register) is driven by the RTI_FCLK, and counts up until the compare value in the Compare Up Counter register (RTI_CPUC0 or RTI_CPUC1) is reached. When the compare matches, the second counter (RTI_FRC0 or RTI_FRC1 register), which is a free running counter, is incremented. At the same time UCx is reset to zero. 

To ensure the consistency of the counters, when both counter values have to be determined, read the Free Running Counter first. This makes sure that at the time when the counter register is read, the Up Counter value has been stored into the counter register. The second read is then performed on the Up Counter register, which holds then the value of the counter cycle of the previous read on the Free Running Counter register. 

Both blocks provide also a capture feature on external events. Two capture sources can trigger the capture event. Which event triggers block 0 or block 1 is configurable from the RTI_CAPCTRL register. The event sources come from the interrupt manager, enabling the device to generate a capture event when a peripheral module generates an interrupt. The peripheral which generates an RTI capture event is configured in the interrupt manager . When the event is detected, UCx and FRCx are stored in Capture Up Counter (RTI_CAUC0 or RTI_CAUC1) and Capture Free Running Counter (RTI_CAFRC0 or RTI_CAFRC1) registers. The read order of the captured values must be in the same order as the counter register reads. So, the CAFRCx must be read first, and then the CAUCx registers are read after the CAFRCx value has been determined. While CAFRCx is 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1619 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

read, the CAUCx value is loaded into a shadow register to maintain data consistency, in case a capture event happens during the two reads. If the application fails to read the two registers before a second capture event happens, the previous data is overwritten. 

Figure 13-221 shows the block diagram for one compare block. The RTI module supports four compare blocks. 

**==> picture [499 x 247] intentionally omitted <==**

**----- Start of picture text -----**<br>
Compare BlockX<br>Update<br>CompareX [31-0]<br>CompareX<br>CLR [31-0]<br>Clear 0<br>= 1 CLR DMA Request<br>INT CLR ENABLE<br>From Counter BlockX (Disable Compare) RTI_WWD_INT<br>= SET<br>CompareX<br>SET [31-0]<br>Update<br>CompareX [31-0]<br>rti-005<br>**----- End of picture text -----**<br>


**Figure 13-221. RTI Compare Block Diagram** 

In order to generate interrupt requests to the interrupt manager, there are four compare registers (RTI_COMP0, RTI_COMP1, RTI_COMP2, and RTI_COMP3). Each of the compare registers can be configured to work either on FRC0 (Counter block0) or FRC1 (Counter block1). When the counter value matches the compare value, an interrupt is generated. This sets an interrupt request line to the interrupt manager. The compare value gets updated automatically with the value stored in Update Compare (RTI_UDCP0, RTI_UDCP1, RTI_UDCP2, and RTI_UDCP3) registers when the compare matches. This gives the ability to generate periodic interrupts/DMA requests without having to update the compare value by software. 

An optional feature allows an application to program another compare value which is then used to clear the interrupt request line. This feature is supported by four compare clear registers (RTI_COMP0CLR, RTI_COMP1CLR, RTI_COMP2CLR, and RTI_COMP3CLR). When the counter value matches the compare clear value, the interrupt line is cleared. This clears the interrupt request line to the interrupt manager. The compare clear value gets updated automatically with the value stored in Update Compare (RTI_UDCPx) registers when the compare matches. 

1620 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.5.1.5 RTI/WWDT Programming Guide** 

## **Driver Information** 

Driver features are available at the RTI driver page and WWDT driver page. 

## **Software API Information** 

The RTI/WWDT driver provides an API to configure the RTI/WWDT module. Full documentation is located on APIs for RTI and APIs for WWDT. 

## **Example Usage** 

The below links shows an example on how to use RTI/WWDT. 

- RTI: 

   - RTI LED Blink 

- WWDT: 

   - Watchdog Reset Mode 

   - Watchdog Interrupt Mode 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1621 

Copyright © 2025 Texas Instruments Incorporated 

