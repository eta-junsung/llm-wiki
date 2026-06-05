<!-- AM263P TRM | 13.6 Internal Diagnostics (DCC/ECC/ESM/MCRC/STC/PBIST) | 원본 p.1622-1693 | pymupdf4llm text+tables, images omitted -->

_Peripherals_ 

www.ti.com 

## **13.6 Internal Diagnostics Modules** 

This section describes the internal diagnostics modules in the device. 

## _**13.6.1 Dual Clock Comparator (DCC)**_ 

This section describes the Dual Clock Comparator (DCC) modules in the device. 

## **13.6.1.1 DCC Overview** 

The Dual Clock Comparator (DCC) is used to determine the accuracy of a clock signal during the time execution of an application. Specifically, the DCC is designed to detect drifts from the expected clock frequency. The desired accuracy can be programed based on calculation for each application. The DCC measures the frequency of a selectable clock source using another input clock as a reference. 

The device has four instances of DCC modules. 

## _**13.6.1.1.1 DCC Features**_ 

The DCC uses two independent clock sources to detect when one is out of specification. Each DCC module implements the following features: 

- Two independent counter blocks count clock pulses from each clock source 

- Each counter block is programmable, however, for proper operation the counters must be programmed with seed values that respect the ratio of the two clock frequencies 

- Configurable timebase for error signal generation 

- Error signal generation when one of the clocks is out of specification 

- Clock frequency measurement 

- Ability to continue the check in continuous mode despite the error. This is programmable capability. 

- Ability to register up-to 4 readings of the error for all associated counts in FIFO. 

- Synchronized handoffs between counting clock domains, processing clock domain or reporting clock domains (bus clock). 

## _**13.6.1.1.2 DCC Not Supported Features**_ 

The DCC does not support the following features: 

- Debug suspend functionality depreciated . Software will have to disable DCCs if it starts messing with clocks during debug. 

## **13.6.1.2 DCC Integration** 

This section describes the DCC integration in the device, including information about clocks, resets, and hardware requests. 

1622 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.6.1.2.1 DCC Integration**_ 

There are 4x DCC modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [500 x 223] intentionally omitted <==**

**Figure 13-222. DCC Integration Diagram** 

The tables below summarize the device integration details of DCC. 

**Table 13-245. DCC Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|DCC0|✓|INFRA0 VBUSP Interconnect|
|DCC1|✓|INFRA0 VBUSP Interconnect|
|DCC2|✓|INFRA0 VBUSP Interconnect|
|DCC3|✓|INFRA0 VBUSP Interconnect|



**Table 13-246. DCC Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock**<br>**Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|DCC0|DCC0_CLK (VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|DCC0 Interface Clock|
|DCC1|DCC1_CLK (VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|DCC1 Interface Clock|
|DCC2|DCC2_CLK (VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|DCC2 Interface Clock|
|DCC3|DCC3_CLK (VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|DCC3 Interface Clock|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1623 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-247. DCC Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|DCC0|DCC0_RST|Warm Reset<br>(SYNC_RST_N)|RCM + Warm Reset Sources|Synchronous Assertion Reset, Active<br>Low|
|DCC1|DCC1_RST|Warm Reset<br>(SYNC_RST_N)|RCM + Warm Reset Sources|Synchronous Assertion Reset, Active<br>Low|
|DCC2|DCC2_RST|Warm Reset<br>(SYNC_RST_N)|RCM + Warm Reset Sources|Synchronous Assertion Reset, Active<br>Low|
|DCC3|DCC3_RST|Warm Reset<br>(SYNC_RST_N)|RCM + Warm Reset Sources|Synchronous Assertion Reset, Active<br>Low|



**Table 13-248. DCC Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|DCC0|DCC0_DONE|DCC0_DONE|ALL R5FSS<br>Cores|Level|DCC0 Done Interrupt|
||DCC0_ERROR|DCC0_ERROR|ESM|Level|DCC0 Error Interrupt|
|DCC1|DCC1_DONE|DCC1_DONE|ALL R5FSS<br>Cores|Level|DCC1 Done Interrupt|
||DCC1_ERROR|DCC1_ERROR|ESM|Level|DCC1 Error Interrupt|
|DCC2|DCC2_DONE|DCC2_DONE|ALL R5FSS<br>Cores|Level|DCC2 Done Interrupt|
||DCC2_ERROR|DCC2_ERROR|ESM|Level|DCC2 Error Interrupt|
|DCC3|DCC3_DONE|DCC3_DONE|ALL R5FSS<br>Cores|Level|DCC3 Done Interrupt|
||DCC3_ERROR|DCC3_ERROR|ESM|Level|DCC3 Error Interrupt|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

1624 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.6.1.3 DCC Functional Description** 

**Figure 13-223. DCC Functional Block Diagram** 

**==> picture [500 x 318] intentionally omitted <==**

**Figure 13-224. DCC Functional Block Diagram** 

## _**13.6.1.3.1 DCC Counter Operation**_ 

DCC has two sets of counters with each set having programmable clock selection. 

- The first set has two counters COUNT0 and VALID0. These operate from Clock0 (reference clock). 

- The second set has one counter COUNT1 that is operated from Clock1 (measured clock). The selection of input clock from list of different counters increases the utility of DCC for debug and test across different clock sources available on the device. 

COUNT0 and COUNT1 are configured based on the ratio between the frequencies of Clock0 and Clock1 (Clock1 frequency * COUNT0 = Clock0 frequency * COUNT1). Further, the tunable counter VALID0 on the Clock0 (reference clock) defines the window of margin for COUNT1 to end after COUNT0. This COUNT1 needs to complete within valid window for operation where clock relationship is as expected. 

The error signal is generated by any one of the following conditions: 

- Clock1 expires before the COUNT0 reaches 0. 

- Clock1 expires after both COUNT0 and VALID0 reach 0. 

- Clock1 not present. 

- Clock0 not present. 

Any of these errors causes the counters to stop counting by default. An application may then read out the counter values to help determine what caused the error. It would take multiple clocks (2-3 in each clock domain i.e. source and VBUSP_CLK) to stop the counters due to the cross-clock domain synchronizations. Counters can also be configured in a mode to reload and continue down-counting despite error so successive error 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1625 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

event is not missed. Error is reported as exception and application is expected to read the counter values for determining quantum and direction of error. 

## **Note** 

Reads of the counter value may not be exact since the read operation is synchronized to the VBUSP_CLK 

Reloads or restarts occur under the following conditions: 

- The module is reset or restarted through software (that is, software starts the module after reset, or software checks an error condition and decides to restart the module). 

- In continuous mode without any error. 

- In continuous mode with error, given CONT_ON_ERR is set, upon which counters restart counting as soon as the error is hit and the error counts are archived. 

## **CAUTION** 

The DCC module does not check jitter for Clock0 or Clock1. 

As the counter preset signal is synchronized to either of the source clock domains, the counters begin downcounting after two corresponding source clock cycles. 

The error signal is to be captured to the VBUSP_CLK domain. There is 1 VBUSP_CLK period uncertainty on either side of the fixed width counting window (VALID0) in generating the error signal since the counters work in a different clock domain. This should be accounted for, when setting the count value for VALID0. 

Operating the DCC with ‘0’ in the COUNTSEED1 or COUNTSEED0 or VALIDSEED0 register will result in undefined operation 

Figure 13-225 through Figure 13-229 shows examples of counters relationship and error generation. 

**==> picture [395 x 183] intentionally omitted <==**

**----- Start of picture text -----**<br>
no error<br>COUNT0 COUNT0<br>Clock0<br>VALID0<br>COUNT1 COUNT1<br>Clock1<br>time<br>reload reload<br>dcc-005<br>Clock1 must expire in this window,<br>otherwise signal error is generated<br>error<br>**----- End of picture text -----**<br>


**Figure 13-225. DCC Clock0 and Clock1 With no Error** 

1626 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [395 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
COUNT0<br>Clock0<br>VALID0<br>COUNT1<br>Clock1<br>time<br>reload<br>dcc-006<br>error<br>**----- End of picture text -----**<br>


**==> picture [187 x 7] intentionally omitted <==**

**----- Start of picture text -----**<br>
Counter1 does not reach 0 before VALID0 reaches 0<br>**----- End of picture text -----**<br>


**Figure 13-226. DCC Clock1 slower than Clock0 results in an error and stops counting** 

**==> picture [395 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
COUNT0<br>Clock0<br>VALID0<br>COUNT1<br>Clock1<br>time<br>reload<br>Counter1 reaches 0 before Counter0 dcc-007<br>error<br>**----- End of picture text -----**<br>


**Figure 13-227. DCC Clock1 faster than Clock0 results in an error and stops counting** 

**==> picture [395 x 175] intentionally omitted <==**

**----- Start of picture text -----**<br>
COUNT0<br>Clock0<br>VALID0<br>COUNT1<br>Counter1 does not count down<br>Clock1 due to an inactive clock1<br>time<br>reload<br>An error signal is generated since Counter1 does not reach 0 dcc-008<br>in the VALID0 window.<br>error<br>**----- End of picture text -----**<br>


**Figure 13-228. DCC Clock1 not present results in an error and stops counting** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1627 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [395 x 177] intentionally omitted <==**

**----- Start of picture text -----**<br>
COUNT0<br>Clock0 COUNT0 and VALID0 do not count down<br>due to inactive Clock0<br>VALID0<br>COUNT1<br>Clock1<br>time<br>reload<br>Counter1 reaches 0 at the right time, but since dcc-009<br>Clock0 is not running, VALID0 hasn’t started, thus an error is generated.<br>error<br>**----- End of picture text -----**<br>


**Figure 13-229. DCC Clock0 not present results in an error and stops counting** 

## _**13.6.1.3.2 DCC Clock Sources**_ 

DCC0 - DCC1 Input Source Clock Mapping and DCC2 - DCC3 Input Source Clock Mapping summarizes the DCC input source clock options for the device. 

**Table 13-249. DCC0 - DCC1 Input Source Clock Mapping** 

|||**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**DCC_CLKSRC0 / DCC_CLKSRC1 value:**||**Input0**||||**Input1**||||||||**Input0**||||**Input1**||||||||
|||**MUX0**||||**MUX1**||||||||**MUX0**||||**MUX1**||||||||
|||**0**|**1**|**2**|**3**|**0**|**1**|**2**|**3**|**4**|**5**|**6**|**7**|**0**|**1**|**2**|**3**|**0**|**1**|**2**|**3**|**4**|**5**|**6**|**7**|
|**Clock Source:**|**Input:**|**CLK0**||||**CLK1**||||||||**CLK0**||||**CLK1**||||||||
|XTALCLK|Crystal Clock|✓|||||||✓|||||✓||||||||||||
|RCCLK10M|Internal 10 MHz RC<br>Oscilator. Always on|||✓||||||||||||✓|||||✓|||||
|EXT_REFCLK|External Ref Clock||✓|||||||✓|||||✓|||||||||||
|RCCLK32K|32 KHz RC Clock||||✓||||||✓||||||✓|||||||||
|PLL_CORE_CLKOUT<br>(PLL_CORE)||||||||||||||||||||||||||
|DPLL_CORE_HSDIV0_CLKO<br>UT0|Root clock for<br>Processor SS and<br>Interconnect<br>(Not Mapped to<br>DCC - covered by<br>SYS_CLK below)|||||||||||||||||||||||||
|DPLL_CORE_HSDIV0_CLKO<br>UT1|CPSW/ICSS<br>RGMII/GMII Clock||||||||||||||||||✓|||||||
|PLL_PER_CLKOUT<br>(PLL_PER)||||||||||||||||||||||||||
|DPLL_PER_HSDIV0_CLKOUT<br>0|UART 5 Mbps<br>Clocking|||||||||||||||||✓||||||||
|DPLL_PER_HSDIV0_CLKOUT<br>1|Peripheral Clocking|||||||||||||||||||✓||||||
|Other IP Clocks||||||||||||||||||||||||||
|R5FSS0_CLK|R5F Cluster 0 Clock||||||✓|||||||||||||||||||
|R5SFS1_CLK|R5F Cluster 1 Clock|||||||✓||||||||||||||||||
|SYS_CLK|Interconnect<br>System Clock|||||✓||||||||||||||||||||
|WDT0_CLK|Watch Dog Timer|||||||||||||||||||||||||
|WDT1_CLK|Watch Dog Timer|||||||||||||||||||||||||
|WDT2_CLK|Watch Dog Timer|||||||||||||||||||||||||
|WDT3_CLK|Watch Dog Timer|||||||||||||||||||||||||



1628 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Table 13-249. DCC0 - DCC1 Input Source Clock Mapping (continued)** 

|||**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC0**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|**MAIN_DCC1**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**DCC_CLKSRC0 / DCC_CLKSRC1 value:**||**Input0**||||**Input1**||||||||**Input0**||||**Input1**||||||||
|||**MUX0**||||**MUX1**||||||||**MUX0**||||**MUX1**||||||||
|||**0**|**1**|**2**|**3**|**0**|**1**|**2**|**3**|**4**|**5**|**6**|**7**|**0**|**1**|**2**|**3**|**0**|**1**|**2**|**3**|**4**|**5**|**6**|**7**|
|**Clock Source:**|**Input:**|**CLK0**||||**CLK1**||||||||**CLK0**||||**CLK1**||||||||
|MCAN0_CLK|MCAN Clock|||||||||||||||||||||||||
|MCAN1_CLK|MCAN Clock|||||||||||||||||||||||||
|TEMPSENSE_32K_CLK|32 KHz Clock<br>(divided down from<br>XTALCLK)|||||||||||||||||||||||||
|RMII1_REFCLK|IO Reference Clock<br>Input|||||||||||||||||||||||||
|RMII2_REFCLK|IO Reference Clock<br>Input|||||||||||||||||||||||||
|RGMII1_RXC|IO Receive Clock<br>Input|||||||||||||||||||||||||
|RGMII2_RXC|IO Receive Clock<br>Input|||||||||||||||||||||||||
|MII1_RXCLK|IO Receive Clock<br>Input|||||||||||||||||||||||||
|MII2_RXCLK|IO Receive Clock<br>Input|||||||||||||||||||||||||
|PR0_MII0_RXCLK|IO Receive Clock<br>Input|||||||||||||||||||||||||
|PR0_MII1_RXCLK|IO Receive Clock<br>Input|||||||||||||||||||||||||
|FSI0_RX_CLK|IO Receive Clock<br>Input|||||||||||||||||||||✓||||
|FSI1_RX_CLK|IO Receive Clock<br>Input||||||||||||||||||||||✓|||
|FSI2_RX_CLK|IO Receive Clock<br>Input|||||||||||||||||||||||✓||
|FSI3_RX_CLK|IO Receive Clock<br>Input||||||||||||||||||||||||✓|



## **Table 13-250. DCC2 - DCC3 Input Source Clock Mapping** 

|||**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**DCC_CLKSRC0 / DCC_CLKSRC1 value:**||**Input0**|||**Input1**||||||||**Input0**|||**Input1**||||||||
|||**MUX0**|||**MUX1**||||||||**MUX0**|||**MUX1**||||||||
|||**[0,**<br>**3-F]**|**1**|**2**|**0**|**1**|**2**|**3**|**4**|**5**|**6**|**7**|**[0,**<br>**3-F]**|**1**|**2**|**0**|**1**|**2**|**3**|**4**|**5**|**6**|**7**|
|**Clock Source:**|**Input:**|**CLK0**|||**CLK1**||||||||**CLK0**|||**CLK1**||||||||
|XTALCLK|Crystal Clock|✓|||||||||||✓|||||||||||
|RCCLK10M|Internal 10 MHz RC<br>Oscilator. Always on|||✓|||||||||||✓|||||||||
|EXT_REFCLK|External Ref Clock||✓|||||||||||✓||||||||||
|RCCLK32K|32 KHz RC Clock|||||||||||||||||||||||
|PLL_CORE_CLKOUT<br>(PLL_CORE)||||||||||||||||||||||||
|DPLL_CORE_HSDIV0_CLKOUT<br>0|Root clock for<br>Processor SS and<br>Interconnect<br>(Not Mapped to<br>DCC - covered by<br>SYS_CLK below)|||||||||||||||||||||||
|DPLL_CORE_HSDIV0_CLKOUT<br>1|CPSW/ICSS RGMII/<br>GMII Clock|||||||||||||||||||||||
|PLL_PER_CLKOUT (PLL_PER)||||||||||||||||||||||||
|DPLL_PER_HSDIV0_CLKOUT0|UART 5 Mbps<br>Clocking|||||||||||||||||||||||
|DPLL_PER_HSDIV0_CLKOUT1|Peripheral Clocking|||||||||||||||||||||||
|Other IP Clocks||||||||||||||||||||||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1629 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-250. DCC2 - DCC3 Input Source Clock Mapping (continued)** 

|||**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC2**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|**MAIN_DCC3**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**DCC_CLKSRC0 / DCC_CLKSRC1 value:**||**Input0**|||**Input1**||||||||**Input0**|||**Input1**||||||||
|||**MUX0**|||**MUX1**||||||||**MUX0**|||**MUX1**||||||||
|||**[0,**<br>**3-F]**|**1**|**2**|**0**|**1**|**2**|**3**|**4**|**5**|**6**|**7**|**[0,**<br>**3-F]**|**1**|**2**|**0**|**1**|**2**|**3**|**4**|**5**|**6**|**7**|
|**Clock Source:**|**Input:**|**CLK0**|||**CLK1**||||||||**CLK0**|||**CLK1**||||||||
|R5SS0_CLK|R5 Cluster 0 Clock|||||||||||||||||||||||
|R5SS1_CLK|R5 Cluster 1 Clock|||||||||||||||||||||||
|SYS_CLK|Interconnect System<br>Clock||||✓|||||||||||||||||||
|WDT0_CLK|Watch Dog Timer|||||✓||||||||||||||||||
|WDT1_CLK|Watch Dog Timer||||||✓|||||||||||||||||
|WDT2_CLK|Watch Dog Timer|||||||✓||||||||||||||||
|WDT3_CLK|Watch Dog Timer||||||||✓|||||||||||||||
|MCAN0_CLK|MCAN Clock|||||||||✓||||||||||||||
|MCAN1_CLK|MCAN Clock||||||||||✓|||||||||||||
|TEMPSENSE_32K_CLK|32 KHz Clock<br>(divided down from<br>XTALCLK)|||||||||||✓||||||||||||
|RMII1_REFCLK|IO Reference Clock<br>Input|||||||||||||||✓||||||||
|RMII2_REFCLK|IO Reference Clock<br>Input||||||||||||||||✓|||||||
|RGMII1_RXC|IO Receive Clock<br>Input|||||||||||||||||✓||||||
|RGMII2_RXC|IO Receive Clock<br>Input||||||||||||||||||✓|||||
|MII1_RXCLK|IO Receive Clock<br>Input|||||||||||||||||||✓||||
|MII2_RXCLK|IO Receive Clock<br>Input||||||||||||||||||||✓|||
|PR0_MII0_RXCLK|IO Receive Clock<br>Input|||||||||||||||||||||✓||
|PR0_MII1_RXCLK|IO Receive Clock<br>Input||||||||||||||||||||||✓|
|FSI0_RX_CLK|IO Receive Clock<br>Input|||||||||||||||||||||||
|FSI1_RX_CLK|IO Receive Clock<br>Input|||||||||||||||||||||||
|FSI2_RX_CLK|IO Receive Clock<br>Input|||||||||||||||||||||||
|FSI3_RX_CLK|IO Receive Clock<br>Input|||||||||||||||||||||||



## **Note** 

Refer to the Application Note DCC computation tool to obtain the register value configurations of desired clock sources to be compared 

## _**13.6.1.3.3 DCC Mode of Operation**_ 

## _**13.6.1.3.3.1 DCC Single-Shot Mode**_ 

The DCC may be programmed to count down one time using single-shot mode. In this mode, the DCC stops operation when: 

- Both COUNT0 and VALID0 reach 0 

- COUNT1 reaches 0 

At the end of one sequence in single-shot mode, the DCC will de-assert the enable value (DCCENA), disabling further counting. At the end of one sequence in single-shot mode, if it is no error that stops counting, then the done status bit is set and a done interrupt is driven. Application must clear the done bit before restarting counts. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1630 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

At the end of a sequence in single-shot mode, if there is an error, then the error status bit will be set. Application must clear the error status bit before starting the next sequence. 

## _**13.6.1.3.3.2 DCC Continuous Mode**_ 

When DCC runs in continuous mode both the counts shall get reloaded with seed value upon completion of counts without error. If the counts end in error DCC stops the operation and counts are not reloaded. 

## _**13.6.1.3.3.2.1 DCC Continue on Error**_ 

During debug, if there are events which are causing clocks to be anomalous over short period covering more than one evaluation window then it would be important to capture trajectory of error event and period around such event. To allow capturing the successive error events DCC can be programmed to continue after error. DCC_GCTRL2[3-0] CONT_ON_ERR shall be set to value other than "0101" to enable this mode. It is recommended to write "1010" to avoid single soft errors. 

## _**13.6.1.3.3.2.2 DCC Error Count**_ 

DCC also counts the number of error pulses generated since reset or since last time the error count is cleared. This is read/write register (DCCERRCNT) for CPU to clear when new trace of number of errors is required to be maintained. 

## _**13.6.1.3.4 DCC Error Trajectory Record**_ 

Once the clock errors out, the host can read the counter values to determine the extent of error to analyze type of failure. For short window comparisons this would become difficult, specially if there are back to back errors due to some transient event. Secondly, for random events which can cause an interrupt during the critical phase of application running, then event if not recorded may get overwritten and also not provide meaningful trace of error. 

## _**13.6.1.3.4.1 DCC FIFO Capturing for Errors**_ 

DCC provides the FIFO for capturing COUNT0, VALID0, and COUNT1 information which captures all three counts upon "Error" event. For "Done" event no results are captured by default. 

## _**13.6.1.3.4.2 DCC FIFO in Continuous Capture Mode**_ 

To track the VALID0 counter values regardless of "Error" or not, FIFOs can be configured to capture the count for each compare window. This is useful in validation and characterization exercise. DCC_GCTRL2 [11-7] FIFO_NONERR control when set to value other than "0101" this mode is set; it is recommended to write "1010" to avoid single soft errors. Note, this capture is applicable only in continuous mode and not in single shot mode. 

## _**13.6.1.3.4.3 DCC FIFO Details**_ 

The FIFO is 4 deep for each count and updates new count information for all the non-full FIFOs. Information is updated on every configured trigger of error or cycle completion. If full, the next values are not written till at-least one entry is read. Application owns responsibility to read the FIFOs uniformly to keep synchronisation between three entries of the FIFO. Both empty and full indications for individual FIFOs is provided through the DCCSTATUS2. 

## _**13.6.1.3.5 DCC Count Read Registers**_ 

DCC has provision to read the counts during operation. This is performed using DCCCNT0, DCCVALID0DCC_CNT0DCCCNT0DCC_VALID0DCCVALID0, and DCC_CNT1DCCCNT1 DCCCNT1 registers. Read from these registers in default mode allows reading the present value of count. This is useful when in single shot mode or mode where DCC stops upon error. 

These registers can be used to read the FIFO through the DCC_GCTRL2[7-4] FIFO_READ configuration. Reads on the empty FIFO shall provide the contents of last pointed location. Application shall track the empty/full conditions of the FIFOs to track the count records consistently. 

Regardless of FIFO_READ configuration, the FIFO internally keeps updating records based on configured triggers until full. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1631 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Note** 

- Input0_clk and input1_clk are two asynchronous clock domains. In a system, VBUS clock may also be asynchronous relative to both Input0_clk and Input1_clk. The module must be able to generate an error when either Input0_clk or Input1_clk is not present. VBUS clock should not sample or affect the clock counting logic in any way. 

- In general, the reference clock should be hooked up to Input0_clk and measured clock should be connected to Input1_clk. The default clock source i.e. ‘0’ should be assigned to connect with device native clock such as internal oscillator reference on both. 

- The error interrupt signal is independent of the error flag bit. If the interrupt is masked, the error flag is still set when an error occurs. The error flag stays set until it is cleared, regardless of the status of the interrupt. 

- The done flag in the DCCSTAT register would be set when the single shot mode completes without error and is independent of the DONEENA bits in the DCCGCTRL register. The done level interrupt would be set only if it is enabled by the DONEENA bits. 

- Upon debug access, the FIFO pointers do not advance, hence not impacting the functional behavior. 

## _**13.6.1.3.6 Limp Mode Generation**_ 

Error on MAIN_DCC0 instance can trigger Limp-mode for added safety. This feature can be enabled by setting the MMR bits in TOP_RCM.LIMP_MODE_EN.DCC0_ERROR_EN 

## **Note** 

More details on LIMP_MODE can be found in the Clocking section of Device Configuration chapter of the TRM 

1632 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.6.2 ECC Aggregator**_ 

This section describes the common ECC aggregator functionality. 

## **13.6.2.1 ECC Aggregator Overview** 

## _**13.6.2.1.1 Memory Protection System using ECC**_ 

To enhance system and functional reliability, various types of memory components (including FIFOs, queues, and SRAMs) are protected using Error Correcting Code (ECC) technology. This protection is implemented through two main components: 

## **ECC Wrapper** 

- Surrounds each memory unit 

- Performs error detection and correction 

- Communicates with the aggregator through a serial interface 

## **ECC Aggregator** 

- Connects to all ECC-protected memories 

- Manages the overall ECC process 

- Features a memory-mapped configuration interface 

Together, the ECC wrapper and aggregator form a unified system (collectively referred to as the ECC aggregator) that ensures data integrity across multiple memory components. 

## **Note** 

Unless specifically distinguished, the term "ECC aggregator" refers to both the wrapper and aggregator components working as an integrated unit. 

Table 13-251 lists the device modules and subsystems which have ECC aggregator. 

**Table 13-251. Device Modules and Subsystems with ECC Aggregator** 

This table lists the device modules and subsystems which have an ECC aggregator 

|**Module Instance**|**ECC Aggregator Support**|**RAM ID Number**|
|---|---|---|
|SoC/Interconnect<br>✓||Not Applicable|
|R5FSS0-0<br>✓||See_R5FSS ECC Support_|
|R5FSS0-1<br>✓||See_R5FSS ECC Support_|
|R5FSS1-0<br>✓||See_R5FSS ECC Support_|
|R5FSS1-1<br>✓||See_R5FSS ECC Support_|
|ICSSM0<br>✓||See_PRU_ICSSM RAM Index Allocation_|
|MCAN0<br>✓||1|
|MCAN1<br>✓||1|
|MCAN2<br>✓||1|
|MCAN3<br>✓||1|
|MCAN4<br>✓||1|
|MCAN5<br>✓||1|
|MCAN6<br>✓||1|
|MCAN7<br>✓||1|
|CPSW<br>✓||See_Memory Error Detection and Correction_|
|FSS_OSPI<br>✓||0|
|FSS_FOTA<br>✓||0|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1633 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.6.2.1.2 ECC Aggregator Features**_ 

The ECC aggregator has the following features: 

- Reduces memory software errors via single error correction (SEC) and double error detection (DED) 

- Provides a mechanism to control and monitor the ECC protected memories in a module or subsystem 

- • Generates an interrupt for correctable error 

- Generates an interrupt for non-correctable error 

- Supports software readable status for single and double-bit ECC errors and associated information such as row address where error has occurred and data bits that have been flipped 

- Supports up to 256 ECC endpoints. An ECC endpoint is ECC RAM 

- Detects single bit error via parity checking on: 

   - Memory mapped configuration interface FIFO 

   - Serial interface FIFO 

   - Serial interface transaction 

- Single bit error detection via parity checking results in a non-correctable error interrupt 

- Supports timeout mechanism on transactions over the ECC serial interface. Timeout occurrence results in a non-correctable error interrupt. 

- Certain control bits have redundancy and if a bit flips an interrupt is generated 

1634 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.6.2.2 ECC Aggregator Integration** 

This section describes an ECC aggregator integration in the device, including information about clocks, resets, and hardware requests. 

## **Note** 

For a list of the device modules and subsystems which have ECC aggregator, see Device Modules and Subsystems with ECC Aggregator. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1635 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.6.2.2.1 ECC Aggregator Integration**_ 

There is 1x ECC Aggregator integrated in the device. The diagram below provides a visual representation of the device integration details. 

**Figure 13-230. ECC Aggregator Integration** 

**==> picture [35 x 9] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>**----- End of picture text -----**<br>


**==> picture [435 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
SOC_ECCAGGR_CORR_LVL<br>ESM<br>SYS_CLK ECC_AGGR_CLK SOC_ECCAGGR_UNCORR_LVL<br>ECC_AGGR<br>ECC Protected Modules<br>FIFO/SRAM/..<br>Warm Reset Sources ECC_AGGR_WARMRESET<br>FIFO/SRAM/..<br>INFRA1 VBUSP INTERCONNECT<br>**----- End of picture text -----**<br>


The tables below summarize the device integration details of ECC Aggregator. 

**Table 13-252.** _**ECC Aggregator**_ **Device Integration** 

## This table describes the ECC Aggregator device integration details. 

|**ECC Aggregator**<br>**Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|ECC Aggregator0|✓|INFRA1 VBUSP Interconnect|



**Table 13-253.** _**ECC Aggregator**_ **Clocks** 

This table describes the ECC Aggregator clocking signals. 

|**ECC**<br>**Aggregator**<br>**Instance**|**ECC Aggregator Clock**<br>**Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|ECC<br>Aggregator0|ECC_AGGR_CLK|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|ECC Aggregator Interface<br>Clock|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1636 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-254.** _**ECC Aggregator**_ **Resets** 

This table describes the ECC Aggregator reset signals. 

|**ECC**<br>**Aggregator**<br>**Instance**|<br>**ECC Aggregator Reset**<br>**Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|ECC<br>Aggregator<br>0|ECC_AGGR_WARMRE<br>SET(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|ECC Aggregator0 Asynchronous<br>Reset|



**Table 13-255.** _**ECC Aggregator**_ **Event Requests** 

This table describes the ECC Aggregator interrupt requests. 

|**ECC**<br>**Aggregat**<br>**or**<br>**Instance**|**ECC Aggregator**<br>**Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|ECC<br>Aggregato<br>r0|SOC_ECCAGGR_UN<br>CORR_LVL_0|SOC_ECCAGGR_UNCORR_L<br>VL_0|ESM|Level|ECC Aggregator0 uncorrectable<br>error event|
||SOC_ECCAGGR_CO<br>RR_LVL_0|SOC_ECCAGGR_CORR_LVL<br>_0|||ECC Aggregator0 correctable error<br>event|



**Table 13-256.** _**Device modules with ECC Aggregator**_ 

This table describes the ECC Aggregator interrupt requests. 

|**ECC Aggregator**|**ECC Aggregator Module instances**|
|---|---|
|ECC Aggregator0|L2OCRAM_BANK0|
||L2OCRAM_BANK1|
||L2OCRAM_BANK2|
||L2OCRAM_BANK3|
||MBOX_SRAM|
||TPTC_A0|
||TPTC_A1|
||L2OCRAM_BANK4|
||L2OCRAM_BANK5|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1637 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.6.2.3 ECC Aggregator Functional Description** 

This section describes the architecture and functional details of the ECC aggregator. 

## _**13.6.2.3.1 ECC Aggregator Block Diagram**_ 

Figure 13-231 shows the ECC aggregator block diagram. 

**==> picture [293 x 175] intentionally omitted <==**

**----- Start of picture text -----**<br>
ECC_AGGR ECC  Protected<br>Module or Subsystem<br>Target configuration<br>ECC  wrapper<br>interface<br>ECC serial interface<br>ECC RAM 0<br>ECC  wrapper<br>ECC_SEC_INT   ECC serial interface<br>ECC_DED_INT ECC RAM 1ECC RAM 1<br>ECC_CLK   ECC  wrapper<br>ECC serial interface<br>ECC_RST ECCECC RAM NRAM N<br>ecc-002<br>..... ...<br>**----- End of picture text -----**<br>


## **Figure 13-231. ECC Aggregator Block Diagram** 

The ECC aggregator is connected to one or more ECC endpoints each of which has assigned a unique ID used when the endpoint is accessed for status information or configuration. The ECC aggregator provides software access to all ECC related registers through its memory mapped target configuration interface while the serial interface is used to communicate with the ECC endpoints. Upon detection of single or double-bit error the corresponding interrupt line is asserted. 

## _**13.6.2.3.2 ECC Aggregator Register Groups**_ 

The ECC aggregator has ECC control, status and interrupt registers for each ECC endpoint in a module or subsystem. These registers are memory mapped and occupy 1 KB address space although part of it may contain reserved locations. The registers are split in the following types: 

- **Global registers** . They are common to all ECC endpoints associated with the ECC aggregator and include the ECC_VECTOR and ECC_REV registers. Each ECC endpoint has assigned a unique ID. When this ID is written to the ECC_VECTOR[10-0] ECC_VECTOR field the corresponding endpoint is selected either for control or for status reading. 

- **ECC control and status registers** . These registers are specific to each ECC endpoint and reside in the range from address offset 0x10 to 0x24 for the ECC RAM endpoint. They are memory mapped but are accessed through the ECC serial interface. They are also selected by the ECC endpoint ID written to the ECC_VECTOR[10-0] ECC_VECTOR field. Because of latency on the serial interface the ECC control and status registers are read by performing special sequence as described in Section 13.6.2.3.3. These registers have also different functionality for types of ECC endpoints. 

- **Interrupt registers** . They include interrupt status, interrupt enable, interrupt disable, and EOI registers. For more information, see Section 13.6.2.3.5. 

## _**13.6.2.3.3 Read Access to the ECC Control and Status Registers**_ 

Read accesses to the ECC control and status registers for each ECC endpoint represent read operations over the ECC serial interface and are triggered by performing the following sequence: 

1. Software writes the following in the ECC_VECTOR register: 

1638 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

   - The ECC endpoint ID in the ECC_VECTOR[10-0] ECC_VECTOR field to select particular ECC endpoint. 

   - The register read address in the ECC_VECTOR[23-16] RD_SVBUS_ADDRESS field to select which register has to be read through the ECC serial interface. 

   - A value of 0x1 in the ECC_VECTOR[15] RD_SVBUS bit to trigger read operation through the ECC serial interface. 

2. Software polls the ECC_VECTOR[24] RD_SVBUS_DONE bit to check if it is 0x1. This indicates that the read operation on the ECC serial interface has completed. 

3. Software reads the data from the register previously selected by the ECC_VECTOR[23-16] RD_SVBUS_ADDRESS field. 

The following is an example for serial read operation: 

1. Write 0x0010 8005 to the ECC_VECTOR register. This sends read request to the ECC_WRAP_REV register (address = 0x10) associated with ECC endpoint with ID = 5. 

2. Poll the ECC_VECTOR[24] RD_SVBUS_DONE bit until value of 0x1 is read. 

3. Read the ECC_WRAP_REV register to get its value. 

## _**13.6.2.3.4 Serial Write Operation**_ 

Write operations over the ECC serial interface are performed as follows: 

1. Software specifies the ECC endpoint ID in the ECC_VECTOR[10-0] ECC_VECTOR field. The ECC_VECTOR[23-16] RD_SVBUS_ADDRESS field is a don't care but the ECC_VECTOR[15] RD_SVBUS bit must be set to 0x0. 

2. Software performs regular write operation to the desired address. If the ECC endpoint ID has already been specified, step 1 can be skipped. Unlike serial read operations it is not necessary to always specify the endpoint ID before performing serial write operation. 

The following is an example for serial write operation: 

1. Write 0x0000 0008 to the ECC_VECTOR register. 

2. Write 0x0000 000F to the ECC_CTRL register. This sends write request with data 0x0000 000F to the ECC_CTRL register associated with ECC RAM with ID = 8. 

## _**13.6.2.3.5 Interrupts**_ 

The ECC aggregator generates the following interrupts: 

- Correctable interrupt (ECC_SEC_INT) where hardware can correct the error but notifies the system in case of SEC. 

- Non-correctable interrupt (ECC_DED_INT) where hardware cannot correct the error in cases of DED, parity check, redundancy check or timeout occurrence. 

The following is the sequence for servicing interrupts: 

- Software enables the interrupts for an ECC endpoint by writing 0x1 to the corresponding bit of the following interrupt enable register: 

   - ECC_SEC_ENABLE_SET_REG0 for the correctable interrupt 

   - ECC_DED_ENABLE_SET_REG0 for the non-correctable interrupt 

- On receiving an interrupt, software checks which ECC endpoint has caused the error by reading the following interrupt status register: 

   - ECC_SEC_STATUS_REG0 for the correctable interrupt 

   - ECC_DED_STATUS_REG0 for the non-correctable interrupt 

- Software performs serial read operations as described in Section 13.6.2.3.3 to read the following status registers that contain details about the error: 

   - The endpoint is ECC RAM: 

      - ECC_ERR_STAT1 

      - ECC_ERR_STAT2 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1639 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

      - ECC_ERR_STAT3 

- After the interrupt has been serviced, depending on the error type, software should clear the corresponding status bits in the ECC_ERR_STAT1 and ECC_ERR_STAT3 registers or in the ECC_CBASS_ERR_STAT1 register. Software has to poll these registers to guarantee that status bits are cleared as there is no other indication for write completion over the ECC serial interface. 

   - The value of the *_PEND_CLR fields in the ECC_CBASS_ERR_STAT1 register must be read and then written back to decrement the count of each field back to 0x0. A further error capture into the ECC_CBASS_ERR_STAT1 register does not occur unless all its fields are 0x0. The decrement value should not be larger than the read value. If a field in the ECC_CBASS_ERR_STAT1 register should not be modified, write a value of 0x0 to that field. 

- Software writes 0x1 to the corresponding end of interrupt register to clear the interrupt: 

   - ECC_SEC_EOI_REG for the correctable interrupt 

   - 

- ECC_DED_EOI_REG for the non-correctable interrupt 

## _**13.6.2.3.6 Inject Only Mode**_ 

There are modules that already perform the ECC generation and checking as part of their data path. In this case, the ECC wrapper may be configured in inject only mode, if needed. In this mode the ECC wrapper does not perform ECC detection and correction. The inject only mode allows users to inject single or double-bit errors so that the module logic can be tested for diagnostic purposes. 

There is error injection logic for testing of the error checking logic (checkers). The injection logic can be configured to inject either single or double bit error. The ECC_ERR_CTRL1 and ECC_ERR_CTRL2 registers should be written first to setup the injection. Then, either the ECC_CTRL[3] FORCE_SEC or the ECC_CTRL[4] FORCE_DED bit must be set to 0x1 to start the injection. Both bits must not be set at the same time. If the injection should continue in incrementing mode, then the ECC_CTRL[5] FORCE_N_BIT bit should be set to 0x1. Once the FORCE_N_BIT is set, then each successive injection can simply write the ECC_CTRL register to set the FORCE_SEC or FORCE_DED again. Reading 0x0 from either the FORCE_SEC or the FORCE_DED bit indicates that the injection has completed, as these bits automatically clear when the checker indicates that it has performed the injection. The time for an injection to complete is not guaranteed, so some delay is needed between successive injections. 

1640 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.6.3 Error Signaling Module (ESM)**_ 

This section describes the Error Signaling Module (ESM) in the device. 

## **13.6.3.1 ESM Overview** 

The Error Signaling Module (ESM) aggregates safety-related events from throughout the SoC into one location. It can signal both low and high priority interrupts to a processor to deal with a safety event and/or manipulate an I/O pin to signal an external system or controller that act upon error to take appropriate action with the SoC Ex: Reset or set the system in a safe, known state. This module does not specify any methods of intervention, but only the facilitates alerting internal CPUs and external monitor(s) of an existing error event. 

_ESM Overview_ shows ESM allocation across the device. 

Figure 13-232 shows the ESM modules overview. 

**==> picture [500 x 373] intentionally omitted <==**

**Figure 13-232. ESM Overview** 

## **13.6.3.2 ESM Features** 

Each ESM module implements the following features: 

- Up to 111 (64 level events + 47 pulse events) error event inputs 

   - Implemented in groups of 32 events 

   - Level or Pulse inputs (Pulse inputs are triple redundant) 

- Selectable low and high priority interrupt error pin prioritization of each error event 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1641 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- Error pin to signal severe device failure to the external world 

   - Support of level or PWM modes 

- Configurable timebase for error signal 

- Error forcing capability for Diagnostic testing 

- Redundant logic to detect pulse events 

1642 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.6.3.3 ESM Integration** 

Figure 13-233 provides a visual representation of the device integration details. 

**==> picture [500 x 274] intentionally omitted <==**

**Figure 13-233. ESM integration Diagram** 

The tables below summarize the device integration details of ESM. 

**Table 13-257.** _**ESM**_ **Device Integration** 

## This table describes the ESM device integration details. 

|**ESM Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|ESM|✓|INFRA0 VBUSP Interconnect|



**Table 13-258.** _**ESM**_ **Clock Integration** 

## This table describes the ESM clocking signals. 

|**ESM**<br>**Instance**|**ESM Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|ESM|ESM_VBUSCLK|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200MHz|ESM VBUSP Interface<br>Clock|
||ESM_CLK||||ESM Functional Clock|



**Table 13-259.** _**ESM**_ **Resets** 

## This table describes the ESM reset signals. 

|**ESM**<br>**Instance**|**ESM Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|ESM|ESM_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|ESM Asynchronous Reset|
||ESM_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|ESM Power-On Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1643 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-260.** _**ESM**_ **Interrupt Requests** 

This table describes the ESM interrupt requests. 

|**ESM**<br>**Instance**|**ESM Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|ESM|ESM_INT_CFG_LVL_<br>0|ESM_INT_CFG_LVL|ALL R5FSS Cores|Level|ESM Configuration Error Interrupt|
||ESM_INT_LOW_LVL_<br>0|ESM_INT_LOW_LVL|||ESM Low Priority Interrupt|
||ESM_INT_HIGH_LVL_<br>0|ESM_INT_HIGH_LVL|||ESM High Priority Interrupt|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

## **13.6.3.4 ESM Functional Description** 

1644 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.6.3.4.1 ESM Functional Operation**_ 

The Error Signaling Module (ESM) centralizes fault reports. The module provides mechanisms to classify errors by severity and to provide programmable error response. The error classification in the ESM is determined by programmed configuration for each individual error input. For each individual error input the configuration can be set to assert an output error pin, or generate an interrupt to a CPU, or both. When an individual error input is configured to generate an interrupt, the configuration also selects whether the interrupt that is generated is high priority or low priority. 

By reporting the faults in a central location, the system can determine what caused the fault and what action can be taken. In general, the faults can be split into two categories: 

- Correctable faults 

- Non-correctable faults 

The ESM reports errors in two ways: 

- An interrupt to a processor inside the device. This enables the device to analyze and try to recover from an error. 

- An external ERROR pin in the device. This enables the system outside of the SoC to monitor for potentially fatal errors (errors that the device cannot self-recover from). Moreover, the external I/O (ERROR pin) can operate in level or PWM modes. In level mode, the output remains asserted (active low) for a minimum period of time. After that period of time, if the error has been cleared by an internal processor, the pin goes inactive (high). If signal does not go inactive in that time, then an external agent must intervene, as an unrecoverable error can occur. In PWM mode, the error causes the output pin to maintain the value for a minimum period of time. After that period of time, if the error has been cleared by an internal processor, the pin continues the PWM pattern. If the signal does not go inactive in that time, then an external agent must intervene, as an unrecoverable error can occur. 

Both mechanisms can be used at the same time for the same fault, signaling both an interrupt and the external ERROR pin. This allows the device to attempt to recover, but if recovery fails, then the external system is still alerted. If recovery succeeds, then the ERROR pin assertion can be removed so that the external system knows that a potentially unsafe condition was avoided. 

Lastly, the ESM does not specify any methods of intervention, only the process of alerting internal CPUs and external monitors of an existing error event. 

ESM Block Diagram shows the ESM module block diagram. 

**==> picture [500 x 207] intentionally omitted <==**

**Figure 13-234. ESM Block Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1645 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.6.3.4.2 Error Event Inputs**_ 

The ESM can have up to 78 error event inputs, configurable by groups of 32. Error event inputs can be either level (default) or pulse. This device is configured with 2 level group events and 1 pulse group events. 

Level error events (active high) are synchronized to the ESM clock. This synchronized value is captured in to a flop. Pulse error events use rising edge detection. Each Pulse Error Event has 3 redundant inputs. Each input has its own edge detection circuit. Multiple transmission protects against Single Event Upsets (SEUs, transient errors) causing a pulse to be lost during transmission and against failure of the edge detection circuit. Once an edge has been detected on any of the three inputs, the raw status is set. Subsequent pulses are likely to come concurrently or quickly enough that software will not have reacted yet. This circuit is intentionally biased against false negatives and towards false positives. An SEU that causes an event where none actually occurred will just cause software to be called in to action. Software will observe that there is no real error and clear the false status. 

## _**13.6.3.4.3 Error Interrupt Outputs**_ 

Error Interrupt Outputs are provided so that a processor in the SoC can be signaled to intervene when an Error Event occurs. Each error event input can be enabled, via software, to cause an Error Interrupt to occur (Error Group N Interrupt Enabled Set Register (Base Address + 0x400 + N*0x20 + 0x08)). Additionally, each error event input can be programmed to influence either the Low Priority (Default) interrupt or the High Priority interrupt (Error Group N Interrupt Priority Register (Base Address + 0x400 + N*0x20 + 0x10)). The Low Priority interrupt is intended for events that are of interest, but do not require immediate intervention. For example, an indication that there was a single bit error that was corrected may signal a low priority interrupt, so that information can be collected for statistical purposes. A High Priority interrupt is intended for events that need immediate attention. For example, an indication that there was an uncorrected two-bit error may be signaled as a high priority interrupt. 

## _**13.6.3.4.4 ESM Error Pin Output**_ 

The Error Pin Output is used to signal an external agent that it needs to (or may need to) intervene because of an error. Each Error Event Input can be programmed, via software, to influence the Error Pin Output (Error Group N Error Pin Influence Set Register (Base Address + 0x400 + N*0x20 + 0x14)). The ESM does not actually incorporate an I/O, this must be done at the SoC level. The Error Pin Output is active low or PWM based on the Error Pin Control register pwm_en field. This pwm_en field should only be modified when the ESM is disabled, based on the Global Enable register. 

During Power-On-Reset, the Error Pin is active (asserted low). It is expected that the SoC drives this via a weak internal pull-down. The I/O is under the control of the SoC. When POR is removed from the ESM, it will be driving the Error Pin so the SoC can hand over control to the ESM. The customer may also add an external pull-down that is only active when the SoC is in reset. 

During a Warm Reset the state of the Error Pin is unchanged (i.e. the Error Pin logic is only reset by a Power-On-Reset). The SoC should leave the I/O active during a warm reset. 

The I/O input from the cell should be looped back to the err_i input. In this way, the status of the error I/O can be directly observed from the I/O buffer loopback path, instead of just from the internal state to the ESM. 

The isolation value for the err_o output of ESM is active (0). 

Figure 13-235 describes the behavior of the Error Pin. Not shown is that a reset (Power-On-Reset only) will immediately transition the Error pin to the ESM_RESET state and a Global Soft Reset will immediately transition the Error pin to the ESM_IDLE state. A Pending Error Event is any error event with the raw state set and the Error Pin Influence enabled. There are two types of “clear” events associated with servicing the Error Pin. The first is to clear the status of the pending event (see section Section 13.6.3.4.9) for how to clear level and pulse pending events). The second is the CLEAR event meant to de-assert the Error Pin. 

1646 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [499 x 355] intentionally omitted <==**

**----- Start of picture text -----**<br>
ESM_RESET<br>(Error Pin Asserted)<br>Yes<br>Power-On Reset<br>Asserted?<br>No<br>(Error Pin De-Asserted)ESM_IDLE No<br>Pending Error No Force Error?<br>Event(s)?<br>Yes Yes<br>Re-Load and Start<br>Minimum Interval ESM_FORCE_ERROR<br>Counter (Error Pin Asserted)<br>Yes Yes No Yes<br>Maximum Interval No Pending Error Yes CLEAR Event? ESM_ERROR CLEAR Event or<br>Expired? Event(s)? (Error Pin Asserted) Normal Mode?<br>No<br>No<br>ESM_WAIT<br>(Error Pin Asserted)<br>esm-007<br>**----- End of picture text -----**<br>


**Figure 13-235. ESM Error Pin State Flowchart** 

If an error event happens that has been programmed to influence the Error Pin, the Error Pin will assert (active low) for a minimum time (as programmed by the Error Pin Counter Pre-Load Register (Base Address + 0x4C)). In order for the Error Pin to de-assert, the following 3 things must happen 

1. The minimum time interval must expire 

2. The event that caused the Error pin to assert must be cleared (see Section 13.6.3.4.9) 

3. A CLEAR must be written to the Error Pin Control Register (Base Address + 0x40) 

## **Note** 

Step 3 should happen after step 2, but either (or both) of these steps may happen before or after step 1. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1647 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [348 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error<br>Event<br>Error Event 0<br>Error Event 1<br>Error Pin<br>Error Pin (PWM)<br>Minimum<br>Interval<br>esm-008<br>**----- End of picture text -----**<br>


**Figure 13-236. ESM Error Pin Assertion** 

If, during the minimum time, CLEAR is written to the error key, then the error pin will de-assert after the minimum interval. 

**==> picture [346 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error<br>Event CLEAR<br>Error Event 0<br>Error Event 1<br>Error Pin<br>Error Pin (PWM)<br>Minimum<br>Interval<br>esm-009<br>**----- End of picture text -----**<br>


**Figure 13-237. ESM Error Pin Assertion with CLEAR during Minimum Interval** 

If CLEAR is not written till after the minimum interval, the error pin will de-assert when CLEAR is written. This is regardless of whether the error event itself is removed before or after the minimum interval, as shown by the dotted line in Figure 13-238 

**==> picture [345 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error<br>Event CLEAR<br>Error Event 0<br>Error Event 1<br>Error Pin<br>Error Pin (PWM)<br>Minimum<br>Interval<br>esm-010<br>**----- End of picture text -----**<br>


**Figure 13-238. ESM Error Pin Asserting with CLEAR after Minimum Interval** 

When in the ESM_ERROR state and a CLEAR event happens, if there are still pending error events, the ESM stays in the ESM_ERROR state with the error pin asserted. Multiple error events when in the ESM_ERROR state do not reset the minimum interval counter. 

1648 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [312 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error Error<br>Event 0 Event 1 CLEAR<br>Error Event 0<br>Error Event 1<br>Error Pin<br>Error Pin (PWM)<br>Minimum<br>Interval<br>**----- End of picture text -----**<br>


**==> picture [24 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
esm-011<br>**----- End of picture text -----**<br>


**Figure 13-239. ESM Error Pin Asserting with Interval Reset by Additional Error Event(s)** 

A CLEAR event causes a re-evaluation of whether there are any pending error events. As such, a single CLEAR can be used to clear the error pin after multiple error events. Multiple CLEAR events can occur (such as the one with the dotted arrow shown in Figure 13-240), but are not necessary. No matter how many error events occur nor when (or how many) CLEAR events occur, the error pin will always be asserted for at least the minimum interval 

**==> picture [345 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error Error<br>Event 0 Event 1 CLEAR CLEAR<br>Error Event 0<br>Error Event 1<br>Error Pin<br>Error Pin (PWM)<br>Minimum<br>Interval<br>esm-012<br>**----- End of picture text -----**<br>


**Figure 13-240. ESM Error Pin Asserting with Single CLEAR for Multiple Events** 

If all error events are cleared and the ESM is in the ESM_WAIT state, waiting for the minimum interval to expire, and a new error interrupt event occurs, the ESM will go back to the ESM_ERROR state. The minimum interval will not reset, but a new CLEAR event will be required. 

**==> picture [311 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
Error Error<br>Event 0 CLEAR Event 1 CLEAR<br>Error Event 0<br>Error Event 1<br>Error Pin<br>Error Pin (PWM)<br>Minimum<br>Interval<br>**----- End of picture text -----**<br>


**==> picture [24 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
esm-013<br>**----- End of picture text -----**<br>


**Figure 13-241. ESM Error Pin Asserting with New Error During Minimum Time Interval** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1649 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.6.3.4.5 Error Pin Behavior During Reset**_ 

Table 13-261 shows some common scenarios of how the error pin status and the values of two associated registers, Error Pin Control Register (Base Address + 0x40) and Error Pin Status Register (Base Address + 0x44), will correspond. 

|0x44), will correspond.||||||
|---|---|---|---|---|---|
|||**Table**|**13-261. ESM Error Pin Scenarios**|||
|**Scenario**||**Error Pin**|**ESM_PIN_CTRL[3-0]**|**ESM_PIN_STS[0] VAL**|**Additional Notes**|
|||**State Value**|**KEY**|**status value**||
|POR Asserted|0||N/A|N/A|Registers are inaccessible.|
||||||Device disables the I/O and|
||||||pulls down internally.|
|After de-assertion of POR|1||0x0 (Normal Mode)|0x0|-|
|After de-assertion of Warm Reset|1||0x0 (Normal Mode)|0x0|-|
|(error was not asserted when||||||
|reset asserted)||||||
|After de-assertion of Warm Reset|0||0x0 (Normal Mode)|0x1|-|
|(error was asserted when reset||||||
|asserted)||||||
|Force error pin|0||0xA (Force Error Mode)|0x0|Forcing error on the pin via|
||||||software.|



## _**13.6.3.4.6 PWM Mode**_ 

If the error output pin is in PWM mode then when no error is detected it will toggle according to programmable MMR widths for high and low periods. When an error occurs, the error pin stops toggling and remains constant until the error is cleared. An external PMIC that is detecting the PWM toggles can identify the error if the pin stops toggling. The periods should be programmed such that they fit within the expectation of the external PMIC. 

## _**13.6.3.4.7 Minimum Time Interval**_ 

The Minimum Time Interval is the minimum amount of time that the Error Pin will be asserted (active low) when an enabled Error Event happens. This value is system dependent, but should be enough time so that the external monitoring agent can always see the Error Pin asserted, but short enough so that if all of the Error Events are cleared, then the Error Pin can be de-asserted before the external agent decides to intervene. This is highly dependent on the application and the Fault Tolerant Time Interval. 

The Minimum Time Interval counter is clock cycle based, therefore the time of the interval is a combination of the value in the Error Pin Counter Pre-Load Register (Base Address + 0x4C) and the clock frequency of the ESM. Software and SoC integration must calculate the value accordingly. The Minimum Time Interval should be set according to the needs of the application. 

## _**13.6.3.4.8 Safety Protection for MMRs**_ 

The configuration MMRs for each Error Group N are backed by 3 flops in order to protect against single or double-bit errors. When written, all 3 bits are set to the same value. When read (and for functioning of the internal state machines) the value is the OR of all 3 bits. Whenever any of the bits disagree, the Configuration Error interrupt is asserted (if enabled). The registers covered by this mechanism are below: 

- Config Error Interrupt Raw Status/Set Register (Base Address + 0x10) 

- Config Error Interrupt Enabled Status/Clear Register (Base Address + 0x14) 

- Config Error Interrupt Enabled Set Register (Base Address + 0x18) 

- Config Error Interrupt Enabled Clear Register (Base Address + 0x1C) 

- Error Group N Event Raw Status/Set Register (Base Address + 0x400 + N*0x20 + 0x00) 

- Error Group N Interrupt Enabled Status/Clear Register (Base Address + 0x400 + N*0x20 + 0x04) 

- Error Group N Interrupt Enabled Set Register (Base Address + 0x400 + N*0x20 + 0x08) 

- Error Group N Interrupt Enabled Clear Register (Base Address + 0x400 + N*0x20 + 0x0C) 

- Error Group N Interrupt Priority Register (Base Address + 0x400 + N*0x20 + 0x10) 

1650 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- Error Group N Error Pin Influence Set Register (Base Address + 0x400 + N*0x20 + 0x14) 

- Error Group N Error Pin Influence Clear Register (Base Address + 0x400 + N*0x20 + 0x18) 

The Error Pin Control Register (Base Address + 0x40) contains a multi-bit field. The Error Pin Counter Pre-Load Register (Base Address + 0x4C) should also be read and checked periodically by software. The key value ensures normal operation on the error pin and that an error even will be generated if one occurs. Software should periodically read check the KEY bit field value and make sure it is 0x0. If the value is not 0x0, software must re-write it to this key value (unless in test mode forcing an error on the pin) to ensure the normal operation. 

Table 13-322 lists the KEY values and their respective meaning. 

**Table 13-262. ESM Error Pin Control Values** 

|**ESM_PIN_CTRL[3-0] KEY**|**Description**|
|---|---|
|N/A|Registers are inaccessible. Device disables the I/O and pulls down internally.|
|0x0 (Normal)|Normal operation mode - Error pin will activate when an enabled error event occurs.|
|0xA (Force Error)|Force error mode - Forces the error pin active. To clear the error pin (return to the ESM_IDLE state)|
||write this field back to normal mode (writing a CLEAR event will also work). Force error mode must|
||be set only while in IDLE. Attempting force error while in another state will have no effect.|
|0x5 (CLEAR)|CLEAR Event - generates a CLEAR event to the ESM state machine. KEY will return to normal|
||mode (0x0) on the next cycle.|
|Other Values|All other values - Normal mode. Writing any of these values will have no effect. When reading any of|
||these values indicates that one or more bits have experienced a single event upset, software should|
||write the field back to 0x0. The ESM will continue to operate in normal mode.|



## _**13.6.3.4.9 ESM Interrupts**_ 

The ESM module generates three output interrupts to the device interrupt controllers: 

- Configuration error interrupt (see Section 13.6.3.4.10.1) 

- High priority error interrupt (see Section 13.6.3.4.10.2) 

- Low priority error interrupt (see Section 13.6.3.4.10.3) 

- Critical priority error interrupt (see _Critical Priority Interrupt_ ) 

The error interrupt outputs are provided so that a processor in the device can be signaled to intervene whenan error event occurs. Each error event input can be enabled, via software, to cause an error interrupt to occur (via the Error Group N Interrupt Enabled Set Register). Additionally, each error event input can be programmed to influence either the low priority (default) interrupt or the high priority interrupt (via the Error Group N Interrupt Priority Register). The low priority interrupt is intended for events that are of interest, but do not require immediate intervention. For example, an indication that there was a single bit error that was corrected may signal a low priority interrupt, so that information can be collected for statistical purposes. A high priority interrupt is intended for events that need immediate attention. For example, an indication that there was an uncorrected two-bit error may be signaled as a high priority interrupt. 

## _**13.6.3.4.10 Programming Guide**_ 

## _**13.6.3.4.10.1 Configuration Error Interrupt**_ 

The Configuration Error Interrupt indicates that there is an inconsistency in the configuration of one (or more) Error Group N MMRs. In such inconsistencies, the internal copies of any of the MMRs caused by a SER associated with Error Group N, the corresponding raw status will be set in the Config Error Interrupt Raw Status/Set Register (Base Address + 0x10). If the corresponding bit is enabled, a Configuration Error Interrupt will be triggered. 

The Configuration Error Interrupt is not enabled by default and it should be enabled by the processor by writing: 

1. Write the respective Error group bit which needs to be monitored for Configuration Error 

   - a. Config Error Interrupt Enabled Set Register (Base Address + 0x18) 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1651 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Note** 

Software should make sure that no status is set in RAW status register of Config Error before enabling the interrupt in SET register. The RAW status register should be read and cleared before enabling the ESM interrupt to avoid triggering of false interrupt to CPU 

2. Enable the Configuration Error Interrupt in VIM for CPU which is configuring the ESM 

## **Note** 

Refer to _R5SS Interrupt Map_ for Interrupt number to be configured in VIM 

When a Configuration Error Interrupt is received, the acting processor should follow these steps: 

1. Read the Config Error Interrupt Enabled Status/Clear Register (Base Address + 0x14) to determine which Group as a configuration error 

2. Write the correct values to the following registers 

## **Note** 

Software should maintain a copy of the correct values to ensure that they can be re-programmed. Software may just try to read back the values, but they cannot be guaranteed to be correct if there was a 2-bit error 

   - a. Error Group N Interrupt Enabled Set Register (Base Address + 0x400 + N*0x20 + 0x08) 

   - b. Error Group N Interrupt Enabled Clear Register (Base Address + 0x400 + N*0x20 + 0x0C) 

   - c. Error Group N Interrupt Priority Register (Base Address + 0x400 + N*0x20 + 0x10) 

   - d. Error Group N Error Pin Influence Set Register (Base Address + 0x400 + N*0x20 + 0x14) 

   - e. Error Group N Error Pin Influence Clear Register (Base Address + 0x400 + N*0x20 + 0x18) 

3. Service any pending interrupts via the steps in the following sections 

   - a. The raw status of any pending interrupts may be inconsistent. Servicing the interrupt will return it to consistency (Error Group N Event Raw Status/Set Register (Base Address + 0x400 + N*0x20 + 0x00)) 

4. Write a 1 to the appropriate bits in the Config Error Interrupt Enabled Status/Clear Register (Base Address + 0x14) 

   - a. This will clear the raw status 

   - b. If the error event is still asserted (or re-asserted) the raw status will be set back to 1 c. If there are no additional errors, the level interrupt will go low 

5. Write the EOI vector to the EOI Interrupt Register (Base Address + 0x30) 

   - a. If there are additional Configuration Error enabled error events pending, then a new pulse will be generated and the level interrupt will remain asserted 

6. If there are no additional Low Priority enabled error events pending, there will be no new pulse 

## _**13.6.3.4.10.2 Low Priority Error Interrupt**_ 

Events mapped to the low priority error interrupt are intended to be events of interest that should be addressed eventually, not events that require immediate attention. An example would be an event indicating a corrected error. The system may want to track this for statistical purposes, but it does not require immediate attention. 

Any error event can be mapped to the low priority error interrupt. It is enabled by programming, 

1. Write the correct value of the register by setting the event bit which needs to be monitored 

   - a. Error Group N Interrupt Enabled Set Register (Base Address + 0x400 + N*0x20 + 0x08) 

1652 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

Software should ensure that no status is set in RAW status register before enabling the interrupt in SET register. The RAW status register should be read and cleared before enabling the ESM interrupt to avoid triggering of false interrupt to CPU. 

2. By default, the priority of all events is set to low. Software should read register and ensure the same or program it by writing 0x0 into Error Group N Interrupt Priority Register (Base Address + 0x400 + N*0x20 + 0x10) to map the events to low priority error interrupt 

3. Enable the ESM Low Priority Error Interrupt in VIM for CPU which is monitoring the safety in system 

## **Note** 

Refer to _R5SS Interrupt Map_ for Interrupt number to be configured in VIM 

When a low priority error interrupt is received, the acting processor must perform the following steps: 

1. Read the Low Interrupt Status Register (Base Address + 0x20) 

   - a. If both low_level_prio and low_pulse prio are equal to 0xFFFF, then END (Interrupt is no longer asserted) 

   - b. If either low_level_pend or low_pulse_pend (or both) are not equal to 0xFFFF, software has two options for determining what event to service 

      - i. First Option: Record the value of value in low_pulse_prio and/or low_level_prio. Determine which one has higher priority. This is the Global Event Number of the highest priority Low Priority Error Event 

      - ii. Second option: 

         1. Read the Low Priority Interrupt Status Register (Base Address + 0x28) to determine which Event Group(s) have pending Low Priority Interrupts 

         2. Read the desired Error Group N Interrupt Enabled Status/Clear Register (Base Address + 0x400 + N*0x20 + 0x04) 

         3. Identify which Low Priority Interrupt to service 

2. Determine based on the ESM Interrupt Mapping of the SoC for the source of the Interrupt 

3. Service the Error Event based on the IP’s specification 

   - a. The system may take several actions including (but not limited to): 

      - i. Fixing the error 

      - ii. Resetting the peripheral that triggered the error 

      - iii. Resetting the device 

      - iv. Communicating outside the SoC for outside intervention 

   - b. The rest of these steps assume that the Error has been handled and the system wants to clear the error event 

   - c. The rest of the handling depends on whether the event is a pulse or level event 

## _**13.6.3.4.10.2.1 Level Event**_ 

1. Clear the Error Event at the Source 

2. Write a 0x1 to the appropriate bit in the Error Group N Interrupt Enabled Status/Clear Register (Base Address + 0x400 + N*0x20 + 0x04) 

   - a. This will clear the raw status 

   - b. If the error event is still asserted (or re-asserted) the raw status will be set back to 1 

   - c. If there are no error events, the level will de-assert. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1653 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Note** 

There is a possible software race condition if software manages to write to the Clear register before the de-asserted level from the source has been synchronized to the ESM clock. If this is an issue, software may perform a read-back at the source IP before writing the clear register to insure order. 

3. Write the EOI vector to the EOI Interrupt Register (Base Address + 0x30) 

   - a. If there are additional Low Priority enabled error events pending, then a new pulse will be generated 

   - b. If there are no additional Low Priority enabled error events pending, there will be no new pulse 

4. Write a CLEAR to the Error Pin Control Register (Base Address + 0x40) 

   - a. This step is optional if the event is not enabled to influence the Error Pin (Error Group N Error Pin Influence Set Register (Base Address + 0x400 + N*0x20 + 0x14)), but may be done regardless as an extra CLEAR is not harmful 

## _**13.6.3.4.10.2.2 Pulse Event**_ 

1. Write a 0x1 to the appropriate bit in the Error Group N Interrupt Enabled Status/Clear Register (Base Address + 0x400 + N*0x20 + 0x04) 

   - a. This will clear the raw status 

   - b. This will de-assert the level interrupt 

2. Write the EOI vector to the EOI Interrupt Register (Base Address + 0x30) 

   - a. If there are additional Low Priority enabled error events pending, then a new pulse will be generated and the level interrupt will remain asserted 

   - b. If there are no additional Low Priority enabled error events pending, there will be no new pulse 

3. Clear the Error Event at the source 

   - a. The source may generate a new pulse which will show up as a new Error Event at the ESM 

4. Write a CLEAR to the Error Pin Control Register (Base Address + 0x40) 

   - a. This step is optional if the event is not enabled to influence the Error Pin (Error Group N Error Pin Influence Set Register (Base Address + 0x400 + N*0x20 + 0x14)), but may be done regardless as an extra CLEAR is not harmful 

## _**13.6.3.4.10.3 High Priority Error Interrupt**_ 

Events mapped to the high priority error interrupt are intended to be events that require immediate intervention from the system because a potentially dangerous error has occurred. An example would be an event indicating an uncorrected error. The system will want to diagnose the issue and intervene so there are no violations. 

Any error event can be mapped to the high priority error interrupt. It is enabled by programming, 

1. Write the correct value of the register by setting the event bit which needs to be monitored 

   - a. Error Group N Interrupt Enabled Set Register (Base Address + 0x400 + N*0x20 + 0x08) 

## **Note** 

Software should make sure that no status is set in RAW status register before enabling the interrupt in SET register. The RAW status register should be read and cleared before enabling the ESM interrupt to avoid triggering of false interrupt to CPU 

2. Set the respective field to 0x1 in Error Group N Interrupt Priority Register (Base Address + 0x400 + N*0x20 + 0x10) to map the events to high priority error interrupt 

3. Enable the ESM High Priority Error Interrupt in VIM for CPU which is monitoring the safety in system 

1654 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

Refer to _R5SS Interrupt Map_ for Interrupt number to be configured in VIM 

When a High Priority Error Interrupt is received, the acting processor should follow these steps: 

1. Read the High Interrupt Status Register (Base Address + 0x24) 

   - a. If both high_level_prio and high_pulse prio are equal to 0xFFFF, then END (Interrupt is no longer asserted) 

   - b. If either high_level_pend or high_pulse_pend (or both) are not equal to 0xFFFF, software has two options for determining what event to service 

      - i. First Option: Record the value of value in high_pulse_prio and/or high_level_prio. Determine which is higher priority. This is the Global Event Number of the highest priority High Priority Error Event 

      - ii. Second option: 

         1. Read the High Priority Interrupt Status Register (Base Address + 0x2C) to determine which Event Group(s) have pending High Priority Interrupts 

         2. Read the desired Error Group N Interrupt Enabled Status/Clear Register (Base Address + 0x400 + N*0x20 + 0x04) 

         3. Identify which High Priority Interrupt to service 

2. Determine based on the ESM Interrupt Mapping of the SoC for the source of the Interrupt 

3. Service the Error Event based on the IP’s specification 

   - a. The system may take several actions including (but not limited to): 

      - i. Fixing the error 

      - ii. Resetting the peripheral that triggered the error 

      - iii. Resetting the device 

      - iv. Communicating outside the SoC for outside intervention 

   - b. The rest of these steps assume that the Error has been handled and the system wants to clear the error event 

   - c. The rest of the handling depends on whether the event is a pulse or level event 

## _**13.6.3.4.10.3.1 Level Event**_ 

1. Clear the Error Event at the Source 

2. Write a 0x1 to the appropriate bit in the Error Group N Interrupt Enabled Status/Clear Register (Base Address + 0x400 + N*0x20 + 0x04) 

   - a. This will clear the raw status 

   - b. If the error event is still asserted (or re-asserted) the raw status will be set back to 1 

   - c. If there are no error events, the level will de-assert. 

## **Note** 

There is a possible software race condition if software manages to write to the Clear register before the de-asserted level from the source has been synchronized to the ESM clock. If this is an issue, software may perform a read-back at the source IP before writing the clear register to insure order. 

3. Write the EOI vector to the EOI Interrupt Register (Base Address + 0x30) 

   - a. If there are additional High Priority enabled error events pending, then a new pulse will be generated 

   - b. If there are no additional High Priority enabled error events pending, there will be no new pulse 

4. Write a CLEAR to the Error Pin Control Register (Base Address + 0x40) 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1655 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- a. This step is optional if the event is not enabled to influence the Error Pin (Error Group N Error Pin Influence Set Register (Base Address + 0x400 + N*0x20 + 0x14)), but may be done regardless as an extra CLEAR is not harmful 

## _**13.6.3.4.10.3.2 Pulse Event**_ 

1. Write a 0x1 to the appropriate bit in the Error Group N Interrupt Enabled Status/Clear Register (Base Address + 0x400 + N*0x20 + 0x04) 

   - a. This will clear the raw status 

   - b. This will de-assert the level interrupt 

2. Write the EOI vector to the EOI Interrupt Register (Base Address + 0x30) 

   - a. If there are additional High Priority enabled error events pending, then a new pulse will be generated and the level interrupt will remain asserted 

   - b. If there are no additional High Priority enabled error events pending, there will be no new pulse 

3. Clear the Error Event at the source 

   - a. The source may generate a new pulse which will show up as a new Error Event at the ESM 

4. Write a CLEAR to the Error Pin Control Register (Base Address + 0x40) 

   - a. This step is optional if the event is not enabled to influence the Error Pin (Error Group N Error Pin Influence Set Register (Base Address + 0x400 + N*0x20 + 0x14)), but may be done regardless as an extra CLEAR is not harmful 

## _**13.6.3.4.10.4 Critical Priority Error Interrupt**_ 

The ESM supports another interrupt output for events which are deemed even more critical than high priority events. For example, an error which should result in a warm reset of a domain or the entire device. Unlike Low/ High Priority Error Events, Critical Priority Error Events don’t require enabling. Instead each Critical Priority Error Event Input can be programmed, via software, to influence the Critical Priority Interrupt Output (Error GroupN Critical Priority Interrupt Influence Set Register. The critical priority interrupt output can trigger immediately or can be programed to trigger after consecutive cycles of aggregate input error event assertion. To trigger immediately, the counter preload value should be programmed to 0 and/or the have the associated input tie-off value assigned to 0. 

## **Note** 

ESM still requires 2-3 cycles to observe an input error event. 

The critical priority interrupt output is sensitive to the ESM’s warm reset input as well as the Global Soft Reset MMR, so it can be tied directly to chip level reset logic if needed. The ESM’s warm reset input is used synchronously. Assertion of the ESM Warm Reset Input disables the ESM Global Enable MMR. When the critical priority interrupt output triggers, the occurrence is logged in the Info Registe. The logging status can only be reset via POR and the Global Soft Reset MMR. 

## _**13.6.3.4.10.4.1 Level Event**_ 

When a critical priority error interrupt occurs: 

1. Software can read the Info Register (Base Address + 0x04) to confirm that the critical priority error output triggered. 

2. Software should read (Error Group N Critical Priority Interrupt Influence Set Register (Base Address + 0x800 + N*0x20 + 0x00)) and the raw status in (Error Group N Event Raw Status/Set Register (Base Address + 0x400 + N*0x20 + 0x00)) to determine the input error event(s) which triggered the critical priority error interrupt. 

1656 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

3. Software would need to perform a Global Soft Reset (Base Address + 0x0C) to clear the Info Register (Base Address + 0x04) critical priority error interrupt status bit as well as all raw interrupt status. 

4. If the critical priority error interrupt resulted in an ESM Warm Reset, software would need to re-enable the Global Enable Register (Base Address + 0x08). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1657 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.6.4 Memory Cyclic Redundancy Check (MCRC) Controller**_ 

This chapter describes the Memory Cyclic Redundancy Check (MCRC) controller in the device. 

## **13.6.4.1 MCRC Overview** 

VBUSM CRC controller is a module which is used to perform CRC (Cyclic Redundancy Check) to verify the integrity of a memory system. A signature representing the contents of the memory is obtained when the contents of the memory are read into MCRC Controller. The responsibility of MCRC controller is to calculate the signature for a set of data and then compare the calculated signature value against a pre-determined good signature value. MCRC controller provides four channels to perform CRC calculation on multiple memories in parallel and can be used on any memory system. 

## _**13.6.4.1.1 MCRC Features**_ 

MCRC has the following features: 

- Four channels to perform background signature verification on any memory subsystem 

- • Data compression on 8-, 16-, 32-, and 64-bit data size 

- Maximum-length PSA (Parallel Signature Analysis) register constructed based on 64-bit primitive polynomial 

- Each channel has a CRC Value Register which contains the pre-determined CRC value 

- Use timed base event trigger from timer to initiate DMA data transfer 

- Programmable 20-bit pattern counter per channel to count the number of data patterns for compression 

- Three modes of operation: 

   - 

      - Auto 

   - Semi-CPU 

   - Full-CPU 

- Supports multiple CRC polynomials: 

   - CRC16 

   - CRC32 

   - CRC64 

   - SAE J1850 (CRC8) 

   - H2F Autosar 4.0 

   - CASTAGNOLI, iSCSI 

   - E2E Profile 4 

- For each channel, CRC can be performed either by MCRC Controller or by CPU 

- Automatically performs signature verification without CPU intervention in AUTO mode 

- Generates interrupt to CPU in Semi-CPU mode to allow CPU to perform signature verification itself 

- Generates CRC fail interrupt in AUTO mode if signature verification fails 

- Generates Timeout interrupt if CRC is not performed within the time limit 

- Generates DMA request per channel to initiate CRC value transfer 

1658 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.6.4.2 MCRC Integration** 

There is 1x MCRC integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [500 x 212] intentionally omitted <==**

**Figure 13-242. MCRC Integration** 

The tables below summarize the device integration details of MCRC# (where # = 1). 

**Table 13-263.** _**MCRC**_ **Device Integration** 

This table describes the MCRC device integration details. 

|**MCRC Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|MCRC0|✓|CORE VBUSM Interconnect|



**Table 13-264.** _**MCRC**_ **Clocks** 

This table describes the MCRC clocking signals. 

|**MCRC**<br>**Instance**|**MCRC Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|MCRC0|MCRC_CLK|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|MCRC0 Interface Clock|



**Table 13-265.** _**MCRC**_ **Resets** 

This table describes the MCRC reset signals. 

|**MCRC**<br>**Instance**|**MCRC Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|MCRC0|MCRC0_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|MCRC0 Asynchronous Reset|



**Table 13-266.** _**MCRC**_ **Interrupt Requests** 

This table describes the MCRC interrupt requests. 

|**MCRC**<br>**Instance**|**MCRC Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCRC0|MCRC0_INT_req|MCRC0_INT_req|ALL R5FSS<br>Cores|Level|MCRC0 Event Interrupt|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1659 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-267.** _**MCRC**_ **DMA Requests** 

This table describes the MCRC DMA requests. 

|**MCRC**<br>**Instance**|**MCRC DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCRC0|MCRC0_DMA_0|MCRC0_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)|Pulse|MCRC0 DMA Request|
||MCRC0_DMA_1|MCRC0_dma_req[1]||||
||MCRC0_DMA_2|MCRC0_dma_req[2]||||
||MCRC0_DMA_3|MCRC0_dma_req[3]||||



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

1660 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.6.4.3 MCRC Functional Description** 

## _**13.6.4.3.1 MCRC Block Diagram**_ 

Figure 13-243 shows the MCRC internal blocks. 

**==> picture [500 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
Command<br>FIFO<br>Target<br>Register<br>Interface One Channel Logic<br>Write data DMA<br>FIFO Request<br>PSA<br>Write Signature<br>Status Signature<br>FIFO CRC Value Compare<br>Read data Register Pattern<br>FIFO File SM<br>INT<br>Gen INT<br>Merge<br>Timer<br>SM<br>Sector<br>SM<br>**----- End of picture text -----**<br>


mcrc-003 

**Figure 13-243. MCRC Block Diagram** 

- **Command FIFO** : The Command FIFO pipelines the commands to the target register interface. The Command and Write FIFOs allow the data to be coincident for processing. If there is no space for writes in the Write Status FIFO or no space in the Read Data FIFO for reads, the command processing will be halted until there is space in the appropriate FIFO. This FIFO is 4 elements deep. 

- **Write FIFO** : The Write FIFO pipelines the write data to the target register interface. The Command and Write FIFOs allow the data to be coincident for processing. If there is no space for writes in the Write Status FIFO or no space in the Read Data FIFO for reads, the command processing will be halted until there is space in the appropriate FIFO. This FIFO is 2 elements deep. 

- **Write Status FIFO** : The Write Status FIFO pipelines the write status back to the VBUSM. A write status will be issued on the final data phase of a write command. This FIFO is 2 elements deep. 

- **Read Data FIFO** : The Read Data FIFO pipelines the read data back to the VBUSM. This FIFO is 3 elements deep. 

- **Target Register Interface** : The Target Register Interface directs the written data to the register file. 

- **PSA Signature** : The PSA Signature creates the signature of the data written. This data will then be compared to the CRC Value or read by software to determine goodness. 

- **Pattern State Machine** : The Pattern State Machine determines when a block of data has been serviced. 

- **Timer State Machine** : The Timer State Machine determines when overrun and under-run events are detected. 

- **Sector State Machine** : The Sector State Machine determines when a sector error should be captured so the software can determine the errant block of data. 

- **Signature Compare** : The Signature Compare block compares the current signature to the CRC Value register and sends the result to the Interrupt Generation block. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1661 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.6.4.3.2 MCRC General Operation**_ 

There are four channels in MCRC controller and for each channel there is a PSA (Parallel Signature Analysis) Signature Register (MCRC_PSA_SIGREGL1-4) and a CRC (Cyclic Redundancy Check) Value Register (MCRC_CRC_REGL1-4). 

A memory can be organized into multiple sectors with each sector consisting of multiple data patterns. A data pattern can be a 8-, 16-, 32-, or 64-bit data. MCRC module performs the signature calculation and compares the signature to a pre-determined value. The PSA Signature Register compresses an incoming data pattern into a signature when it is written. When one sector of data patterns are written into PSA Signature Register, a final signature corresponding to the sector is obtained. CRC Value Register stores the pre-determined signature corresponding to one sector of data patterns. The calculated signature and the pre-determined signature are then compared to each other for signature verification. To minimize CPU’s involvement, data patterns transfer can be carried out at the background of CPU using DMA controller. DMA is setup to transfer data from memory of which the contents to be verified to the memory mapped PSA Signature Register. When DMA transfers data to the memory mapped PSA Signature Register, a signature is generated. 

A programmable 20-bit data pattern counter is used for each channel to define the number of data patterns to calculate for each sector. Signature verification can be performed automatically by MCRC controller in AUTO mode or by CPU itself in Semi-CPU or Full-CPU mode. In AUTO mode, a self-sustained CRC signature calculation can be achieved without any CPU intervention. 

## _**13.6.4.3.3 MCRC Modes of Operation**_ 

MCRC Controller can operate in AUTO, Semi-CPU, and Full-CPU modes. 

## _**13.6.4.3.3.1 AUTO Mode**_ 

In AUTO mode, MCRC Controller in conjunction with DMA controller can perform CRC without CPU intervention. A sustained transfer of data to both the PSA Signature Register (MCRC_PSA_SIGREGL1-4) and a CRC (Cyclic Redundancy Check) Value Register (MCRC_CRC_REGL1-4) are performed in the background of CPU. When a mismatch is detected, an interrupt is generated to the CPU. A 16-bit, current sector ID register (MCRC_CRC_CURSEC_REG1-4) is provided to identify which sector causes a CRC failure. 

## _**13.6.4.3.3.2 Semi-CPU Mode**_ 

In Semi-CPU mode, DMA controller is also utilized to perform data patterns transfer to PSA Signature Register (MCRC_PSA_SIGREGL1-4). Instead of performing signature verification automatically, the CRC controller generates an compression complete interrupt to CPU after each sector is compressed. Upon responding to the interrupt the CPU performs the signature verification by reading the calculated signature stored at the PSA Sector Signature Register (MCRC_PSA_SECSIGREGL1-4) and compare it to a pre-determined CRC value. 

## _**13.6.4.3.3.3 Full-CPU Mode**_ 

In Full-CPU mode, the CPU does the data patterns transfer and signature verification all by itself. When CPU has enough throughput, it can perform data patterns transfer by reading data from the memory system to the PSA Signature Register (MCRC_PSA_SIGREGL1). After certain number of data patterns are compressed, the CPU can read from the PSA Signature Register and compare the calculated signature to the pre-determined CRC signature value. In Full-CPU mode, neither interrupt nor DMA request is generated. All counters are also disabled. 

## _**13.6.4.3.4 PSA Signature Register**_ 

The 64-bit PSA Signature Register (MCRC_PSA_SIGREGL1-4 and MCRC_PSA_SIGREGH1-4) is based on one of the selected CRC polynomials to produce the maximum length LFSR (Linear Feedback Shift Register). 

CRC16: f(x) = x[16] + x[12] + x[5] + 1 (34) CRC32: f(x) = x[32] + x[26] + x[23] + x[22] + x[16] + x[12] + x[11] + x[10] + x[8] + x[7] + x[5] + x[4] + x[2] + x + 1 (35) CRC64: f(x) = x[64 ] + x[4] + x[3] + x + 1 (36) 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1662 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

SAE J1850 CRC8: f(x) = x[8] + x[4] + x[3] + x[2] + 1 (37) H2F Autosar 4.0: f(x) = x[5] + x[3] + x[2] + x + 1 (38) 

CASTAGNOLI, iSCSI: f(x) = x[28] + x[27] + x[26] + x[25] + x[23] + x[22] + x[20] + x[19] + x[18] + x[14] + x[13] + x[11] + x[10] + x[9] + x[8] + x[6] + 1 (39) E2E Profile 4: f(x) = x[31] + x[30] + x[29] + x[28] + x[26] + x[23] + x[21] + x[19] + x[18] + x[15] + x[14] + x[13] + x[12] + x[11] + x[9] + x[8] + x[4] + x + 1 (40) 

- A. More details of the 64-bit primitive polynomial can be found at W. Stahnke, Primitive binary polynomials, Math. Comp. 27 (1973), 977--980. 

There is one PSA Signature Register per CRC channel. PSA Signature Register can be both read and written. When it is written, it can either compress the data or just capture the data depending on the state of CHi_MODE bits (where i = 1 to 4). If CHi_MODE=0x0 (Data Capture), a seed value can be planted in the PSA Signature Register without compression. Other modes other than Data Capture will result with the data compressed by PSA Signature Register when it is written. Each channel can be planted with different seed value before compression starts. When PSA Signature Register is read, it gives the calculated signature. 

MCRC Controller should be used in conjunction with the on-chip DMA controller to produce optimal system performance. The incoming data pattern to PSA Signature Register is typically initiated by the DMA controller. When DMA is properly setup, it would read data from the pre-determined memory system and write them to the memory mapped PSA Signature Register. Each time PSA Signature Register is written a signature is generated. CPU itself can also perform data transfer by reading from the memory system and perform write operation to PSA Signature Register if CPU has enough throughput to handle data patterns transfer. 

After a system reset and when AUTO mode is enabled, MCRC Controller automatically generates a DMA request to request the pre-determined CRC value corresponding to the first sector of memory to be checked. 

In AUTO mode, when one sector of data patterns is compressed, the signature stored at the PSA Signature Register is first copied to the PSA Sector Signature Register (MCRC_PSA_SECSIGREGL1-4) and PSA Signature Register is then cleared out to all zeros. An automatic signature verification is then performed by comparing the signature stored at the PSA Sector Signature Register to the CRC Value Register (MCRC_CRC_REGL1-4). After the comparison the MCRC Controller can generate a DMA request. Upon receiving the DMA request the DMA controller will update the CRC Value Register by transferring the next pre-determined signature value associated with the next sector of memory system. If the signature verification fails then MCRC Controller can generate a CRC fail interrupt. 

In Full-CPU mode, no DMA request and interrupt are generated at all. The number of data patterns to be compressed is determined by CPU itself. Full-CPU mode is useful when DMA controller is not available to perform background data patterns transfer. Software can periodically generate a software interrupt to CPU and use CPU to accomplish data transfer and signature verification. 

MCRC Controller supports double word, word, half word and byte access to the PSA Signature Register. During a non-doubleword write access, all unwritten byte lanes are padded with zeros before compression. Note that comparison between PSA Sector Signature Register and CRC Value Register is always in 64 bits because a compressed value is always expressed in 64 bits. 

There is a software reset per channel for PSA Signature Register. When set, the PSA Signature Register is reset to all zeros. 

PSA Signature Register is reset to zero under the following conditions: 

- System reset 

- PSA Software reset 

- One sector of data patterns is compressed 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1663 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.6.4.3.5 PSA Sector Signature Register**_ 

After one sector of data is compressed, the final resulting signature calculated by PSA Signature Register is transferred to the 64-bit PSA Sector Signature Register (MCRC_PSA_SECSIGREGL1-4 and MCRC_PSA_SECSIGREGH1-4). PSA Signature Register is a read-only register. During Semi-CPU mode, the host CPU must read from the PSA Sector Signature Register instead of reading from PSA Signature Register for signature verification to avoid data coherency issue. The PSA Signature Register can be updated with new signature before the host CPU is able to retrieve it. 

In Semi-CPU mode, no DMA request is generated. When one sector of data patterns is compressed, CRC controller first generates a compression complete interrupt. Responding to the interrupt, CPU will read the PSA Sector Signature Register and compare it to the known good signature or write the signature value to another memory location to build a signature file. In Semi-CPU mode, CPU must perform the signature verification in a manner to prevent any overrun condition. The overrun condition occurs when the compression complete interrupt is generated after one sector of data patterns is compressed and CPU has not read from the PSA Sector Signature Register to perform necessary signature verification before PSA Sector Signature Register is overridden with a new value. An overrun interrupt can be enabled to generate when overrun condition occurs. 

## _**13.6.4.3.6 CRC Value Register**_ 

Associated with each channel there is a 64-bit CRC Value Register (MCRC_CRC_REGL1-4 and MCRC_CRC_REGH1-4). 

The CRC Value Register stores the pre-determined CRC value. After one sector of data patterns is compressed by PSA Signature Register, MCRC Controller can automatically compare the resulting signature stored at the PSA Sector Signature Register with the pre-determined value stored at the CRC Value Register if AUTO mode is enabled. If the signature verification fails, MCRC Controller can be enabled to generate an CRC fail interrupt. When the channel is set up for Semi-CPU mode, CRC controller first generates a compression complete interrupt to CPU. Upon servicing the interrupt, CPU will then read the PSA Sector Signature Register and then read the corresponding CRC value stored at another location and compare them. CPU must not read from the CRC Value Register during Semi-CPU or Full-CPU mode because the CRC Value Register is not updated during these two modes. 

In AUTO mode, for first sector’s signature, DMA request is generated when mode is programmed to AUTO. For subsequent sectors, DMA request is generated after each sector is compressed. Responding to the DMA request, DMA controller reloads the CRC Value Register for the next sector of memory system to be checked. The user software needs to configure the DMA to ensure that the DMA first writes to the MCRC_CRC_REGL1 followed by the MCRC_CRC_REGH1 register in during the AUTO Mode. 

When CRC Value Register is updated with a new CRC value, an internal flag is set to indicate that CRC Value Register contains the most current value. This flag is cleared when CRC comparison is performed. Each time at the end of the final data pattern compression of a sector, MCRC Controller first checks to see if the corresponding CRC Value Register has the most current CRC value stored in it by polling the flag. If the flag is set then the CRC comparison can be performed. If the flag is not set then it means the CRC Value Register contains stale information. A CRC underrun interrupt is generated. When an underrun condition is detected, signature verification is not performed. 

MCRC Controller supports double word, word, half word and byte access to the CRC Value Register. As noted before comparison between PSA Sector Signature Register and CRC Value Register during AUTO mode is carried out in 64 bits. 

## _**13.6.4.3.7 Raw Data Register**_ 

The raw or un-compressed data written to the PSA Signature Register is also saved in the 64-bit Raw Data Register (MCRC_RAW_DATAREGL1-4 and MCRC_RAW_DATAREGH1-4). This register is read only. 

## _**13.6.4.3.8 Example DMA Controller Setup**_ 

DMA controller needs to be setup properly in either AUTO or Semi-CPU mode as DMA controller is used to transfer data patterns. Hardware or a combination of hardware and software DMA triggering are supported. 

1664 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.6.4.3.8.1 AUTO Mode Using Hardware Timer Trigger**_ 

There are two DMA channels associated with each CRC channel when in AUTO mode. One DMA channel is setup to transfer data patterns from the source memory to the PSA Signature Register (MCRC_PSA_SIGREGL1-4). The second DMA channel is setup to transfer the pre-determined signature to the CRC Value Register (MCRC_CRC_REGL1-4 ). The trigger source for the first DMA channel can be either by hardware or by software. As illustrated in Figure 13-244, a timer can be used to trigger a DMA request to initiate transfer from the source memory system to PSA Signature Register. In AUTO mode, MCRC Controller also generates DMA request after one sector of data patterns is compressed to initiate transfer of the next CRC value corresponding to the next sector of memory. Thus a new CRC value is always updated in the CRC Value Register (MCRC_CRC_REGL1-4)by DMA synchronized to each sector of memory. 

A block of memory system is usually divided into many sectors. All sectors are the same size. The sector size is programmed in the MCRC_CRC_PCOUNT_REG1-4 and the number of sectors in one block is programmed in the MCRC_CRC_SCOUNT_REG1-4 of the respective channel. MCRC_CRC_PCOUNT_REG1-4 multiplies MCRC_CRC_SCOUNT_REG1-4 and multiplies transfer size of each data pattern should give the total block size in number of bytes. 

The total size of the memory system to be examined is also programmed in the respective transfer count register inside DMA module. The DMA transfer count register is divided into two parts. They are element count and frame count. Note that a hardware DMA request can be programmed to trigger either one frame or one entire block transfer. In Figure 13-244, a hardware DMA request from a timer is used as a trigger source to initiate DMA transfer. If all four CRC channels are active in AUTO mode then a total of four DMA requests would be generated by MCRC Controller. 

**==> picture [460 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
DMA Controller Memory<br>HW DMA Req<br>Timer HW DMA Req DMA Request Event Sync Sector 1<br>Sector 2<br>DMA Channel 0<br>.........<br>MCRC<br>PSA_SIG_REGH1 Sector n<br>PSA_SIG_REGL1 DMA Channel p<br>CRC_REGH1 DMA Channel q<br>CRC_REGL1 Sector 1 CRC Value<br>Sector 2 CRC Value<br>....<br>.........<br>PSA_SIG_REGH4<br>PSA_SIG_REGL4 DMA Channel 31 Sector n CRC Value<br>CRC_REGH4<br>CRC_REGL4<br>one block<br>**----- End of picture text -----**<br>


mcrc-004 

**Figure 13-244. AUTO Mode Using Hardware Timer Trigger** 

## _**13.6.4.3.8.2 AUTO Mode Using Software Trigger**_ 

The data patterns transfer can also be initiated by software. CPU can generate a software DMA request to activate the DMA channel to transfer data patterns from source memory system to the PSA Signature Register. To generate a software DMA request CPU needs to set the corresponding DMA channel in the DMA software trigger register. Note that just one software DMA request from CPU is enough to complete the entire data patterns transfer for all sectors. Please see AUTO Mode With Software CPU Trigger for illustration. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1665 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [460 x 529] intentionally omitted <==**

**----- Start of picture text -----**<br>
DMA Controller Memory<br>SW DMA Req<br>Sector 1<br>CPU HW DMA Req DMA Request Event Sync<br>Sector 2<br>DMA Channel 0<br>.........<br>MCRC<br>PSA_SIG_REGH1 Sector n<br>PSA_SIG_REGL1 DMA Channel p<br>CRC_REGH1 DMA Channel q<br>CRC_REGL1 Sector 1 CRC Value<br>Sector 2 CRC Value<br>....<br>.........<br>PSA_SIG_REGH4<br>PSA_SIG_REGL4 DMA Channel 31 Sector n CRC Value<br>CRC_REGH4<br>CRC_REGL4<br>mcrc-005<br>Figure 13-245. AUTO Mode With Software CPU Trigger<br>13.6.4.3.8.3 Semi-CPU Mode Using Hardware Timer Trigger<br>During Semi-CPU mode, no DMA request is generated by CRC controller. Therefore, no DMA channel is<br>allocated to update CRC Value Register. CPU should not read from CRC Value Register in semi-CPU mode as<br>it contains stale value. Note that no signature verification is performed at all during this mode. Similar to AUTO<br>mode, either by hardware or by software DMA request can be used as a trigger for data patterns transfer. Figure<br> illustrates the DMA setup using semi-CPU mode with hardware timer trigger.<br>DMA Controller Memory<br>HW DMA Req<br>Sector 1<br>Timer DMA Request Event Sync<br>Sector 2<br>DMA Channel 0<br>.........<br>MCRC<br>PSA_SIG_REGH1 Sector n<br>PSA_SIG_REGL1 DMA Channel p<br>CRC_REGH1 DMA Channel q<br>CRC_REGL1<br>....<br>PSA_SIG_REGH4<br>PSA_SIG_REGL4 DMA Channel 31<br>CRC_REGH4<br>CRC_REGL4<br>one block<br>one block<br>**----- End of picture text -----**<br>


## _**13.6.4.3.8.3 Semi-CPU Mode Using Hardware Timer Trigger**_ 

During Semi-CPU mode, no DMA request is generated by CRC controller. Therefore, no DMA channel is allocated to update CRC Value Register. CPU should not read from CRC Value Register in semi-CPU mode as it contains stale value. Note that no signature verification is performed at all during this mode. Similar to AUTO mode, either by hardware or by software DMA request can be used as a trigger for data patterns transfer. Figure 13-246 illustrates the DMA setup using semi-CPU mode with hardware timer trigger. 

mcrc-006 

**Figure 13-246. Semi-CPU Mode With Hardware Timer Trigger** 

**Table 13-268. DMA Request and Counter Logic Operation According to CRC Mode** 

|**CRC Mode**|**DMA Request**|**Pattern Counter**|**Sector Counter**|**Timeout Counter**|
|---|---|---|---|---|
|AUTO|Active|Active|Active|Active|
|Semi-CPU|Inactive|Active|Active|Active|
|Full CPU|Inactive|Inactive|Inactive|Inactive|



1666 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.6.4.3.9 Pattern Count Register**_ 

There is a 20-bit data pattern counter for every CRC channel. The data pattern counter is a down counter and can be pre-loaded with a programmable value stored in the Pattern Count Register (MCRC_CRC_PCOUNT_REG1-4). When the data pattern counter reaches zero, a compression complete interrupt is generated in Semi-CPU mode and an automatic signature verification is performed in AUTO mode. In AUTO only, DMA request is generated to trigger the DMA controller to update the CRC Value Register. 

## **Note** 

The data pattern count must be divisible by the total transfer count as programmed in DMA controller. The total transfer count is the product of element count and frame count. 

## _**13.6.4.3.10 Sector Count Register/Current Sector Register**_ 

Each channel contains a 16-bit sector counter. The sector count register stores the number of sectors. Sector counter is a free running counter and is incremented by one each time when one sector of data patterns is compressed. When the signature verification fails, the current value stored in the sector counter is saved into current sector register (MCRC_CRC_CURSEC_REG1-4). If signature verification fails, CPU can read from the current sector register to identify the sector which causes the CRC mismatch. To aid and facilitate the CPU in determining the cause of a CRC failure it is advisable to use the following equation during CRC and DMA setup. 

> CRC Pattern Count × CRC Sector Count = DMA Element Count × DMA Frame Count (41) 

The current sector register is frozen from being updated until both the current sector register is read and CRC fail (CHi_CRC_FAIL) status bit is cleared by CPU. If CPU does not respond to the CRC failure in a timely manner before another sector produces a signature verification failure, the current sector register is not updated with the new sector number. An overrun interrupt is generate instead. If current sector register is already frozen with an erroneous sector and emulation is entered with SUSPEND signal goes to high then the register still remains frozen even it is read. 

In Semi-CPU mode, the current sector register is used to indicate the sector for which the compression complete has last happened. 

Current sector register is reset when the PSA software reset is enabled. 

## **Note** 

Both data pattern count and sector count registers must be greater than or equal to one for the counters to count. After reset, pattern count and sector count registers default to zero and the associated counters are inactive. 

## _**13.6.4.3.11 Interrupts**_ 

CRC generate several types of interrupts per channel. Associated with each interrupt there is a interrupt enable bit (see MCRC_CRC_INTS). No interrupt is generated in Full-CPU mode. 

- Compression complete interrupt 

- CRC fail interrupt 

- Overrun interrupt 

- Underrun interrupt 

- Timeout interrupt 

**Table 13-269. Interrupt Conditions Per CRC Mode** 

|**CRC Mode**|**Compression**<br>**Complete**|**CRC Fail**|**Overrun**|**Underrun**|**Timeout**|
|---|---|---|---|---|---|
|AUTO|No|Yes|Yes|Yes|Yes|
|Semi-CPU|Yes|No|Yes|No|Yes|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1667 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-269. Interrupt Conditions Per CRC Mode (continued)** 

|**CRC Mode**|**Compression**<br>**Complete**|**CRC Fail**|**Overrun**|**Underrun**|**Timeout**|
|---|---|---|---|---|---|
|Full-CPU|No|No|No|No|No|



## _**13.6.4.3.11.1 Overrun Interrupt**_ 

Overrun Interrupt is generated in either AUTO or Semi-CPU mode. During AUTO mode, if a CRC fail is detected then the current sector number is recorded in the current sector register (MCRC_CRC_CURSEC_REG1-4). If CRC fail status bit is not cleared and current sector register is not read by the host CPU before another CRC fail is detected for another sector then an overrun interrupt is generated. During Semi-CPU mode, when the data pattern counter finishes counting, it generates a compression complete interrupt. At the same time the signature is copied into the PSA Sector Signature Register (MCRC_PSA_SECSIGREGL1-4). If the host CPU does not read the signature from PSA Sector Signature Register before it is updated again with a new signature value then an overrun interrupt is generated. 

## _**13.6.4.3.11.2 Timeout Interrupt**_ 

To ensure that the memory system is examined within a pre-defined time frame and no loss of incoming data there is a 24-bit timeout counter per CRC channel. The timeout counter can be pre-loaded with two different pre-load values, watchdog timeout pre-load value (MCRC_CRC_WDTOPLD1-4) and block complete timeout pre-load value (MCRC_CRC_BCTOPLD1-4). The timeout counter is clocked by a prescaler clock which is permanently running at division 64 of FICLK clock. 

Watchdog timeout pre-load register (MCRC_CRC_WDTOPLD1-4) is used to check if DMA does supply a block of data responding to a request in a given time frame. Block complete timeout pre-load register (MCRC_CRC_BCTOPLD1-4) is used to check if one complete block of data patterns are compressed within a specific time frame. The timeout counter is first pre-loaded with MCRC_CRC_WDTOPLD1-4 after either AUTO or Semi-CPU mode is selected and starts to down count. If the timeout counter expires before DMA transfers any data pattern to PSA Signature Register then a timeout interrupt is generated. An incoming data pattern before the timeout counter expires will automatically pre-load the timeout counter with MCRC_CRC_BCTOPLD1-4 the block complete timeout pre-load value. 

Block complete timeout pre-load value is used to check it one block of data patterns are compressed within a given time limit. If the timeout counter pre-loaded with MCRC_CRC_BCTOPLD1-4 value expires before one block of data patterns are compressed a timeout interrupt is generated. When one block (pattern count × sector count) of data patterns are compressed before the counter has expired, the counter is pre-loaded with MCRC_CRC_WDTOPLD1-4 value again. If the timeout counter is pre-loaded with zero then the counter is disable and no timeout interrupt is generated. 

## _**13.6.4.3.11.3 Underrun Interrupt**_ 

Underrun interrupt only occurs in AUTO mode. The interrupt is generated when the CRC Value Register is not updated with the corresponding signature when the data pattern counter finishes counting. During AUTO mode, MCRC Controller generates DMA request to update CRC Value Register in synchronization to the corresponding sector of the memory. Signature verification is also performed if underrun condition is detected. And CRC fail interrupt is generated at the same time as the underrun interrupt. 

## _**13.6.4.3.11.4 Compression Complete Interrupt**_ 

Compression complete interrupt is generated in Semi-CPU mode only. When the data pattern counter reaches zero, the compression complete flag is set and the interrupt is generated 

## _**13.6.4.3.11.5 Interrupt Offset Register**_ 

MCRC Controller only generates one interrupt request to interrupt manager. An interrupt offset register (MCRC_CRC_INT_OFFSET_REG) is provided to indicate the source of the pending interrupt with highest priority. Table 13-270 shows the offset interrupt vector address of each interrupt in an ascending order of priority. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1668 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-270. Interrupt Offset Mapping** 

|**Interrupt Condition**|**Offset Value**|
|---|---|
|Phantom|0x0|
|Ch1 CRC Fail|0x1|
|Ch2 CRC Fail|0x2|
|Ch3 CRC Fail|0x3|
|Ch4 CRC Fail|0x4|
|reserved|0x5-0x8|
|Ch1 Compression Complete|0x9|
|Ch2 Compression Complete|0xA|
|Ch3 Compression Complete|0xB|
|Ch4 Compression Complete|0xC|
|reserved|0xD-0x10|
|Ch1 Overrun|0x11|
|Ch2 Overrun|0x12|
|Ch3 Overrun|0x13|
|Ch4 Overrun|0x14|
|reserved|0x15-0x18|
|Ch1 Underrun|0x19|
|Ch2 Underrun|0x1A|
|Ch3 Underrun|0x1B|
|Ch4 Underrun|0x1C|
|reserved|0x1D-0x20|
|Ch1 Timeout|0x21|
|Ch2 Timeout|0x22|
|Ch3 Timeout|0x23|
|Ch4 Timeout|0x24|



## _**13.6.4.3.11.6 Error Handling**_ 

When an interrupt is generated, host CPU must take appropriate actions to identify the source of error and restart the respective channel in DMA and MCRC module. To restart a CRC channel user must perform the following steps in the ISR: 

1. Write to software reset bit in MCRC_CRC_CTRL0 register to reset the respective PSA Signature Register 

2. Reset the CHi_MODE bits to 0 in MCRC_CRC_CTRL2 register as Data capture mode 

3. Set the CHi_MODE bits in MCRC_CRC_CTRL2 register to desired new mode again 

4. Release software reset 

The host CPU must use byte write to restart each individual channel. 

## _**13.6.4.3.12 Power Down Mode**_ 

MCRC module can be put into power down mode when the power down control bit MCRC_CRC_CTRL1[0] PWDN is set. The module wakes up when the PWDN bit is cleared. 

## _**13.6.4.3.13 Emulation**_ 

A read access from a register in functional mode can sometimes trigger a certain internal event to follow. For example, reading interrupt offset register triggers an event to clear the corresponding interrupt status flag. During emulation when SUSPEND signal is high, a read access from any register should only return the register contents to the bus and should not trigger or mask any event as it would have in functional mode. This is to prevent debugger from reading the interrupt offset register, that is, during refreshing screen and cause the 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1669 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

corresponding interrupt status flag to get cleared. Timeout counters are stopped to generate timeout interrupts in emulation mode. No VBUSM bus error will be generated if reading from the unimplemented locations. . 

CEMUDBG is the VBUSM suspend signal which need not explicitly indicate that whether CPU is in suspend mode or not. In data trace mode, a separate suspend signal CPU_EMUSP, is used to indicate MCRC controller that the CPU is in suspend mode or not. 

1670 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.6.4.4 MCRC Programming Examples** 

## _**13.6.4.4.1 Example: Auto Mode Using Time Based Event Triggering**_ 

A large memory area with 2 Mbyte (256 k × 32-bit [doubleword]) is to be checked in the background of CPU. CRC is to be performed every 1 Kbyte (128 doubleword). Therefore there will be 2048 pre-recorded CRC values. For illustration purpose, we map MCRC_CRC_REGL1 register to DMA channel 1 and MCRC_PSA_SIGREGL1 register to DMA channel 2. Let’s assume all DMA transfers are carried out in 64-bit transfer size. 

## _**13.6.4.4.1.1 DMA Setup**_ 

- Setup DMA channel 1 with the starting address from which the pre-determined CRC values are stored. Setup the destination address to the MCRC_CRC_REGL1. Put the source address at post increment addressing mode and put the destination address at constant addressing mode. Use hardware DMA request for channel 1 to trigger a frame transfer. 

- Setup DMA channel 2 with the source address from which the contents of memory to be verified. Setup the destination address to the MCRC_PSA_SIGREGL1. Program the element transfer count to 128 and the frame transfer count to 2048. Program the read and write element size to 64 bits. Put the source address at post increment addressing mode and put the destination address at constant address mode. Use hardware DMA request for channel 2 to trigger an entire block transfer. 

## _**13.6.4.4.1.2 Timer Setup**_ 

The timer can be any general purpose timer which is capable of generating a time based DMA request. 

- Setup Timer to generate DMA request associated with DMA channel 2. For example, software can setup the timer to generate a DMA request every 10 ms. 

## _**13.6.4.4.1.3 CRC Setup**_ 

- Program the pattern count MCRC_CRC_PCOUNT_REG1 to 128 

- Program the sector count MCRC_CRC_SCOUNT_REG1 to 2048 

- For example, we want the entire 2 Mbytes to be compressed within 5 ms. We can program the block complete timeout pre-load (MCRC_CRC_BCTOPLD1-4) value to 15625 (5 ms / (1 FICLK period × 64)) if CRC is operating at 200 MHz. 

- Enable AUTO mode and all interrupts. 

After AUTO mode is selected MCRC Controller automatically generates a DMA request on channel 1. Around the same time the timer module also generates a DMA request on DMA channel 2. When the first incoming data pattern arrives at the MCRC_PSA_SIGREGL1/H1, the MCRC Controller will compress it. After some time, the DMA controller would update the CMCRC_CRC_REGL1/H1 with a pre-determined value matching the calculated signature for the first sector of 128 64-bit data patterns. After one sector of data patterns are compressed, the MCRC Controller generate a CRC fail interrupt if signature stored at the MCRC_PSA_SECSIGREGL1/H1 does not match the MCRC_CRC_REGL1/H1 Register. MCRC Controller generates a DMA request on DMA channel 1 when one sector of data patterns are compressed. This routine will continue until the entire 2 Mbytes are consumed. If the timeout counter reached zero before the entire 2 Mbytes are compressed, a timeout interrupt is generated. After 2Mbytes are transferred, the DMA can generate an interrupt to CPU. The entire operation will continue again when DMA responds to the DMA request from both the timer and MCRC Controller. The CRC is performed totally without any CPU intervention. 

## _**13.6.4.4.2 Example: Auto Mode Without Using Time Based Triggering**_ 

A small but highly secured memory area with 1 Kbytes is to be checked in the background of CPU. CRC is to be performed every 1 Kbytes. Therefore, there is only one pre-recorded CRC value. For illustration purpose, we map channel 1 MCRC_CRC_REGL1/H1 to DMA channel 1 and channel 1 MCRC_PSA_SIGREGL1/H1 to DMA channel 2. Assume all transfers carried out by DMA are in 64-bit transfer size. 

## _**13.6.4.4.2.1 DMA Setup**_ 

- Setup DMA channel 1 with the source address from which the pre-determined CRC value is stored. Setup the destination address to the MCRC_CRC_REGL1 Register. Put the source address at constant addressing 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1671 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

   - mode and put the destination address at constant addressing mode. Use hardware DMA request for channel 1. 

- Setup DMA channel 2 with the source address from which the memory area to be verified. Setup the destination address to the MCRC_PSA_SIGREGL1/H1. Program the element transfer count to 128 and the frame transfer count to 1. Put the source address at post increment addressing mode and put the destination address at constant address mode. Generate a software DMA request on channel 2 after CRC has completed its setup. Enable autoinitiation for DMA channel 2. 

## _**13.6.4.4.2.2 CRC Setup**_ 

- Program the MCRC_CRC_PCOUNT_REG1 to 128 

- Program the MCRC_CRC_SCOUNT_REG1 to 1 

- Leaving the timeout count MCRC_CRC_BCTOPLD1 register with the reset value of zero means no timeout interrupt is generated 

- Enable AUTO mode and all interrupts 

After AUTO mode is selected the MCRC Controller automatically generates a DMA request on channel 1. At the same time the CPU generates a software DMA request on DMA channel 2. When the first incoming data pattern arrives at the MCRC_PSA_SIGREGL1/H1, the MCRC Controller will compress it. After some time, the DMA controller would update the MCRC_CRC_REGL1/H1 with a pre-determined value matching the calculated signature for the first sector of 128 64-bit data patterns. After one sector of data patterns are compressed, the MCRC Controller generate a CRC fail interrupt if signature stored at the MCRC_PSA_SECSIGREGL1/H1 does not match the MCRC_CRC_REGL1/H1. MCRC Controller generate a DMA request on DMA channel 1 again after one sector is compressed. After 1 Kbytes are transferred, the DMA can generate an interrupt to CPU. Responding to the DMA interrupt CPU can restart the CRC routine by generating a software DMA request onto channel 2 again. 

## _**13.6.4.4.3 Example: Semi-CPU Mode**_ 

If DMA controller is available in a system the CRC module can also operate in semi-CPU mode. This means that CPU can still make use of the DMA to perform data patterns transfer to CRC controller in the background. The difference between semi-CPU mode and AUTO mode is that CRC controller does not automatically perform the signature verification. CRC controllers generates a compression complete interrupt to CPU when the one sector of data patterns are compressed. CPU needs to perform the signature verification itself. 

A memory area with 2 Mbytes is to be verified with the help of the CPU. CRC operation is to be performed every 1 Kbyte. Since there are 2 Mbytes (256 K doublewords) of memory to be check and we want to perform a CRC every 1 Kbytes (128 doublewords) and therefore there must be 2048 pre-recorded CRC values. In Semi-CPU mode, the MCRC_CRC_REGL1/H1 is not updated and contains indeterminate data. 

## _**13.6.4.4.3.1 DMA Setup**_ 

- Setup DMA channel 1 with the source address from which the memory area to be verified are mapped. Setup the destination address to the MCRC_PSA_SIGREGL1/H1. Put the starting address at post increment addressing mode and put the destination address at constant address mode. Use hardware DMA request to trigger an entire block transfer for channel 1. Disable autoinitiation for DMA channel 1. 

## _**13.6.4.4.3.2 Timer Setup**_ 

The timer can be any general purpose timer which is capable of generating a time-based DMA request. 

- Setup Timer to generate DMA request associated with DMA channel 1. For example, software can setup the timer to generate a DMA request every 10 ms. 

## _**13.6.4.4.3.3 CRC Setup**_ 

- Program the MCRC_CRC_PCOUNT_REG1 to 128 

- Program the MCRC_CRC_SCOUNT_REG1 to 2048 

- For example, we want the entire 2 Mbytes to be compressed within 5 ms. We can program the block complete timeout pre-load value MCRC_CRC_BCTOPLD1 to 15625 (5 ms / (1 FICLK period × 64)) if CRC is operating at 200 MHz 

- Enable AUTO mode and all interrupts. 

1672 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

The timer module first generates a DMA request on DMA channel 1 when it is enabled. When the first incoming data pattern arrives at the MCRC_PSA_SIGREGL1/H1, the CRC controller will compress it. After one sector of data patterns are compressed, the CRC controller generate a compression complete interrupt. Upon responding to the interrupt the CPU would read from the MCRC_PSA_SECSIGREGL1/H1. It is up to the CPU on how to deal with the PSA value just read. It can compare it to a known signature value or it can write it to another memory location to build a signature file or even transfer the signature out of the device via SCI or SPI. This routine will continue until the entire 2 Mbytes are consumed. The latency of the interrupt response from CPU can cause overrun condition. If CPU does not read from MCRC_PSA_SECSIGREGL1 before the PSA value is overridden with the signature of the next sector of memory, an overrun interrupt will be generated by CRC controller. 

## _**13.6.4.4.4 Example: Full-CPU Mode**_ 

In a system without the availability of DMA controller, the CRC routine can be operated by CPU provided the CPU has enough throughput. CPU needs to read from the memory area from which CRC is to be performed. 

A memory area with 2 Mbytes is to be checked with the help of the CPU. CRC operation is to be performed every 1 Kbyte. In CPU mode, the MCRC_CRC_REGL1/H1 is not updated and contains indeterminate data. 

## _**13.6.4.4.4.1 CRC Setup**_ 

- All control registers can be left in their reset state. Only enable Full-CPU mode. 

CPU itself reads from the memory and write the data to the MCRC_PSA_SIGREGL1/MCRC_PSA_SIGREGH1 inside MCRC Controller. When the first incoming data pattern arrives at the MCRC_PSA_SIGREGL1/ MCRC_PSA_SIGREGH1, the MCRC Controller will compress it. After n data patterns are compressed, CPU can read from the MCRC_PSA_SIGREGL1/MCRC_PSA_SIGREGH1. It is up to the CPU on how to deal with the PSA signature value just read. It can compare it to a known signature value stored at another memory location. 

## _**13.6.5 Self-Test Controller (STC)**_ 

## **13.6.5.1 STC Overview** 

The enhanced Self-Test Controller (STC) is used to test logic cores based on the On-Product Multiple Input Signature Register (OPMISR) scan compression architecture. 

Software-based self-test programs for the cores are available, but offer less test coverage. Due to the complexity of the soft cores, the coverage required can be difficult to achieve and will result in a larger program size. 

For these complex cores, on-chip logic BIST support for the self-test is preferred. 

The main features of the STC include: 

- Implements the OPMISR controller, along with the on-chip self-test controller for the synthesizable module logic, which enables high test coverage. 

- The self-test controller facilitates complete isolation of the logical segment under the test from the rest of the system during the self-test run. Configure critical control signals in the initiator and target ports of the logical segment under the test to a safe state. 

- The self-tested CPU core initiator bus transaction signals are configured to be in idle mode during the self-test run. 

- Time-out counter for the self-test run as a fail-safe feature. 

- Can capture power reduction using dead cycles before and after the capture pulse. 

A self test segment corresponds to a portion of discreet safety-critical logic which can be tested in isolation from the rest of the system by the self test controller and OPMISR logic. 

## _**13.6.5.1.1 Unsupported Features**_ 

- Section 13.6.5.3.7.1 – Launch-on-last-shift. TR_T =1 

- Section 13.6.5.3.7.2 – Transition delay fault model. FT =1 

- Section 13.6.5.3.7.6 – Low-power scan mode. MSS_STC.STCGCR1.LP_SCAN_MODE = 1 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1673 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- Section 13.6.5.3.7.7 and Section 13.6.5.3.7.8 – Coverage improvement techniques – MSS_STC.STCGCR1.ROM_ACCESS_INV =1 Mode 

- Interval-based testing 

- MSS_STC.STC_CLKDIV clock division features 

## _**13.6.5.1.2 STC Memory Map**_ 

## **Table 13-271. STC Memory Map for AM263Px** 

|**Name**|**Start Address**|**Frame Address (Hex)**<br>**End**|**Size**|**Description**|
|---|---|---|---|---|
|R5FSS0_STC|0x5350 0000|0x5350 00A8|172 Bytes|R5FSS0_STC module<br>configuration registers|
|R5FSS1_STC|0x5351 0000|0x5351 00A8|172 Bytes|R5FSS1_STC module<br>configuration registers|



## _**13.6.5.1.3 OPMISR Concept**_ 

**==> picture [500 x 307] intentionally omitted <==**

**Figure 13-247. OPMISR Conceptual Diagram** 

STC enables fetching deterministic ATPG vectors from STC ROM and applies them to the UUT using XoR decompressor. BIST is implemented on the application-critical R5 and HSM cores. 

The self-test controller uses the existing compression scan chains and applies the patterns from ROM. The scan chains are further unloaded into MISR during shift out operation. At the end of self test, the on chip MISR signature is compared with golden signature stored in pattern ROM. 

The On-Product Multiple-Input Signature Register (OPMISR) is a methodology which moves the test pattern generation on-chip. Logic BIST is implemented on functional partitions (BIST’ed COREs) that are speed-critical and have high gate count. 

1674 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

The MISR test structure modifies the typical fullscan scan chain such that each scan data input internally drives many chains. These chains feed to the inserted MISR structure. The chain's values are captured into the MISR during shift, generating a resulting signature that can be shifted out. 

A given Unit Under Test (UUT) is scan-inserted, and the scan chains are hooked to the OPMISR logic. A self-test wrapper is created around the UUT and the OPMISR logic. The inputs to the UUR driving the D pin of flops are overridden with a controllable flop inside the UUT. The outputs of the UUT are isolated by an isolation control signal during the STC operation. These features ensure that the core and UUT are isolated from the rest of the system during the self-test. 

## **13.6.5.2 Block Diagram** 

The STC module is composed of following blocks: 

- ROM interface 

- FSM and sequence control 

- Register file 

- STC bypass / ATE interface 

- Peripheral bus interface (VBUSP interface) 

**==> picture [500 x 369] intentionally omitted <==**

**Figure 13-248. Block Diagram for STC With Multiple Segments** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1675 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.6.5.3 Module Description** 

## _**13.6.5.3.1 ROM Interface**_ 

This block handles the ROM address and control signal generation to read the self-test microcode from the ROM. The test microcode, patterns, and golden signature value for each interval is stored in ROM. 

Detailed information of the ROM microcode is available at ROM. 

## _**13.6.5.3.2 FSM and Sequence Control**_ 

This block generates the signals and data to OPMISR controller based on the test type and scan chain depth. The sequence of operation per interval is defined in Section 13.6.5.3.5. 

## _**13.6.5.3.2.1 Clock Control**_ 

The CLOCK CNTRL sub-block handles the clock selection and clock generation for ROM, OPMISR controller, and BIST’ed CORE clocks. 

## _**13.6.5.3.2.2 MISR Compare Block**_ 

At the end of the each self-test interval, an 896-bit MISR value from the OPMISR controller is shifted into NSTC. This is compared with the MISR_GOLDEN value, which is copied into a buffered register before the start of the interval. The result is updated into the status registers. 

## _**13.6.5.3.3 Register Block**_ 

This block implements the user-programmable control registers that determine when to start a self test and what clock frequency the scan test should be performed. 

The register block also captures various status information of the self test for the user. 

## _**13.6.5.3.4 VBUSP Interface**_ 

The control and the status registers of the STC module can be accessed through the VBUSP interface. During application programming, configuration registers are programmed through the peripheral interface, to enable and run the self-test controller. 

1676 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.6.5.3.5 STC Flow**_ 

**==> picture [500 x 469] intentionally omitted <==**

**Figure 13-249. STC Flow (1 of 2)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1677 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [220 x 425] intentionally omitted <==**

**Figure 13-250. STC Flow (2 of 2)** 

## _**13.6.5.3.6 Programming Sequence**_ 

The following sequence describes the step-by-step guide to trigger a logic Self-Test operation the device cores. 

**Table 13-272. STC - Programming Sequence (Default Mode)** 

|**Step No.**|**Steps**|**Register/Bit Field/Programming**<br>**(For R5SS0/R5SS1/HSM)**|**Value**|
|---|---|---|---|
|1|Configure the number of intervals to be<br>run|STC.STCGCR0.INTCOUNT_B16|0x1|
|2|Configure both cores for Logic Self-<br>Test.|STC.STCGCR1.SEG0_CORE_SEL|0x1|
|3|Scan mode configuration. Fixed<br>Configuration – Only this configuration<br>value is supported.|STC.STCGCR1.LP_SCAN_MODE|0x0|
|4|Scan mode configuration. Fixed<br>Configuration – Only this configuration<br>value is supported.|STC.STCGCR1.CODEC_SPREAD_MODE|0x1|



1678 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-272. STC - Programming Sequence (Default Mode) (continued)** 

|5|Scan mode configuration. Fixed<br>Configuration – Only this configuration<br>value is supported.|STC.STCGCR0.CAP_IDLE_CYCLE|0x3|
|---|---|---|---|
|6|Scan mode configuration. Fixed<br>Configuration – Only this configuration<br>value is supported.|STC.STCGCR0.SCANEN_HIGH_CAP_IDLE_CYCLE|0x3|
|7|Program the Timer Register for max run<br>time|STC.STCTPR|0x18E2E|
|8|Program the Clock Divider Register –<br>Maximum frequency of STC – 200MHz|STC.STC_CLKDIV. CLKDIV0|0x1|
|9|Program the STC ROM start address|STC.SEG0_START_ADDR.SEG_START_ADDR|0x0|
|10|Configure the pointer for STC ROM<br>start address|STC.STCGCR0.RS_CNT_B1|0x1|
|11|Configure this register to disable STC<br>diagnostic check|STC.STCSCSCR.FAULT_INS_B1|0x0|
|12|Disable the key for STC diagnostic<br>check|STC.STCSCSCR. SELF_CHECK_KEY_B4|0x0|
|13|Kick off the test|STC.STCGCR1.ST_ENA_B4|0xA|
|14|Wait for standby – WFI signal from UUT (idle)|||
|15|Wait for Test done Interrupt or ESM error<br>(Test done interrupt for R5SS0 is routed to R5SS1 and vice versa)|||
|16|Read the status register to check the<br>STC test completion.|STC.STCGSTAT.TEST_DONE|0x1(READ)|
|17|Read the register to check the failure<br>status of the STC test.|STC.STCGSTAT.TEST_FAIL|(READ)<br>0x0 - No failure|
|**Table 13-273. STC - Programming Sequence(WFI Override Mode)**||||
|**Step No.**|**Steps**|**Register/Bit Field/Programming**<br>**(For R5SS0/R5SS1/HSM)**|**Value**|
|1|Configure the number of intervals to be<br>run|STC.STCGCR0.INTCOUNT_B16|0x1|
|2|Configure both/single core(s) for Logic<br>Self-Test.|STC.STCGCR1.SEG0_CORE_SEL|0x1|
|3|Scan mode configuration. Fixed<br>Configuration – Only this configuration<br>value is supported.|STC.STCGCR1.LP_SCAN_MODE|0x0|
|4|Scan mode configuration. Fixed<br>Configuration – Only this configuration<br>value is supported.|STC.STCGCR1.CODEC_SPREAD_MODE|0x1|
|5|Scan mode configuration. Fixed<br>Configuration – Only this configuration<br>value is supported.|STC.STCGCR0.CAP_IDLE_DELAY_CYCLE|0x3|
|6|Scan mode configuration. Fixed<br>Configuration – Only this configuration<br>value is supported.|STC.STCGCR0.SCANEN_HIGH_CAP_IDLE_DELAY_CYCL<br>E|0x3|
|7|Program the timer register for max run<br>time|STC.STCTPR|0x18E2E|
|8|Program the Clock Divider Register –<br>Maximum frequency of STC – 200MHz|STC.STC_CLKDIV. CLKDIV0|0x1|
|9|Program the STC ROM start address|STC.SEG0_START_ADD.SEG_START_ADDR|0x0|
|10|Configure the pointer for STC ROM<br>start address|STC.STCGCR0.RS_CNT_B1|0x1|
|11|Configure this register to disable STC<br>diagnostic check|STC.STCSCSCR.FAULT_INS_B1|0x0|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1679 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-273. STC - Programming Sequence (WFI Override Mode) (continued)** 

|12|Disable the key for STC diagnostic<br>check|STC.STCSCSCR.SELF_CHECK_KEY_B4|0x0|
|---|---|---|---|
|13|Kick off the test|STC.STCGCR1.ST_ENA_B4|0xA|
|14|Provide override WFI signal to STC<br>indicating processor idle state|MSS_CTRL.R5SS*_FORCE_WFI.CR5_WFI_OVERIDE|0x7|
|15|Wait for Test done Interrupt or ESM error (Test done interrupt for R5SS0 is routed to R5SS1 and vice versa)|||
|16|Read the status register to check the<br>STC test completion.|STC.STCGSTAT.TEST_DONE|0x1(READ)|
|17|Read the register to check the failure<br>status of the STC test.|STC.STCGSTAT.TEST_FAIL|(READ)<br>0x0 - No failure|



## _**13.6.5.3.7 ROM Organization**_ 

**Table 13-274. ROM Organization for 2 Intervals** 

|**COMMENTS**|**55:40**|**41:32**|**31:16**|**15:8**|**7:4**|**3**|**2**|**1**|**0**|
|---|---|---|---|---|---|---|---|---|---|
||**INTERVAL 0**|||||||||
|CFG for interval 0, when<br>rom_access_inversion =0|Reserved|pattern_cou<br>nt[9:0]|Reserved|Reserved|Reserved|Seg_ID[1]|Seg_ID[0<br>]|FT|TR_T|
|MISR for interval 0, when<br>rom_access_inversion =0|MISR_GOLDEN[895:840]|||||||||
||MISR_GOLDEN[839:784]|||||||||
||MISR_GOLDEN[783:728]|||||||||
||MISR_GOLDEN[727:672]|||||||||
||MISR_GOLDEN[671:616]|||||||||
||MISR_GOLDEN[615:560]|||||||||
||MISR_GOLDEN[559:504]|||||||||
||MISR_GOLDEN[503:448]|||||||||
||MISR_GOLDEN[447:392]|||||||||
||MISR_GOLDEN[391:336]|||||||||
||MISR_GOLDEN[335:280]|||||||||
||MISR_GOLDEN[279:224]|||||||||
||MISR_GOLDEN[223:168]|||||||||
||MISR_GOLDEN[167:112]|||||||||
||MISR_GOLDEN[111:56]|||||||||
||MISR_GOLDEN[55:0]|||||||||



1680 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-274. ROM Organization for 2 Intervals (continued)** 

|**COMMENTS**|**55:40**|**41:32**|**31:16**|**15:8**|**7:4**|**3**|**2**|**1**|**0**|
|---|---|---|---|---|---|---|---|---|---|
|LP_MISR for interval 0, when<br>rom_access_inversion =0|LP_MISR_GOLDEN[895:840]|||||||||
||LP_MISR_GOLDEN[839:784]|||||||||
||LP_MISR_GOLDEN[783:728]|||||||||
||LP_MISR_GOLDEN[727:672]|||||||||
||LP_MISR_GOLDEN[671:616]|||||||||
||LP_MISR_GOLDEN[615:560]|||||||||
||LP_MISR_GOLDEN[559:504]|||||||||
||LP_MISR_GOLDEN[503:448]|||||||||
||LP_MISR_GOLDEN[447:392]|||||||||
||LP_MISR_GOLDEN[391:336]|||||||||
||LP_MISR_GOLDEN[335:280]|||||||||
||LP_MISR_GOLDEN[279:224]|||||||||
||LP_MISR_GOLDEN[223:168]|||||||||
||LP_MISR_GOLDEN[167:112]|||||||||
||LP_MISR_GOLDEN[111:56]|||||||||
||LP_MISR_GOLDEN[55:0]|||||||||
|Patterns for interval 0|P1_SD8[6:0<br>]|P1_SD7[6:0<br>]|P1_SD6[6<br>:0]|….|….|…|P1_SD1[<br>6:0]|||
|||…|…|…|…|…|…|P1_SD9[<br>6:0]||
|||…|…|…|…|…|…|…|…|
|LP_MISR for interval 0, when<br>rom_access_inversion =1|LP_INV_MISR_GOLDEN[55:0]|||||||||
||LP_INV_MISR_GOLDEN[111:56]|||||||||
||LP_INV_MISR_GOLDEN[167:112]|||||||||
||LP_INV_MISR_GOLDEN[223:168]|||||||||
||LP_INV_MISR_GOLDEN[279:224]|||||||||
||LP_INV_MISR_GOLDEN[335:280]|||||||||
||LP_INV_MISR_GOLDEN[391:336]|||||||||
||LP_INV_MISR_GOLDEN[447:392]|||||||||
||LP_INV_MISR_GOLDEN[503:448]|||||||||
||LP_INV_MISR_GOLDEN[559:504]|||||||||
||LP_INV_MISR_GOLDEN[615:560]|||||||||
||LP_INV_MISR_GOLDEN[671:616]|||||||||
||LP_INV_MISR_GOLDEN[727:672]|||||||||
||LP_INV_MISR_GOLDEN[783:728]|||||||||
||LP_INV_MISR_GOLDEN[839:784]|||||||||
||LP_INV_MISR_GOLDEN[895:840]|||||||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1681 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-274. ROM Organization for 2 Intervals (continued)** 

|**COMMENTS**|**55:40**|**41:32**|**31:16**|**15:8**|**7:4**|**3**|**2**|**1**|**0**|
|---|---|---|---|---|---|---|---|---|---|
|MISR for interval 0, when<br>rom_access_inversion =1|INV_MISR_GOLDEN[55:0]|||||||||
||INV_MISR_GOLDEN[111:56]|||||||||
||INV_MISR_GOLDEN[167:112]|||||||||
||INV_MISR_GOLDEN[223:168]|||||||||
||INV_MISR_GOLDEN[279:224]|||||||||
||INV_MISR_GOLDEN[335:280]|||||||||
||INV_MISR_GOLDEN[391:336]|||||||||
||INV_MISR_GOLDEN[447:392]|||||||||
||INV_MISR_GOLDEN[503:448]|||||||||
||INV_MISR_GOLDEN[559:504]|||||||||
||INV_MISR_GOLDEN[615:560]|||||||||
||INV_MISR_GOLDEN[671:616]|||||||||
||INV_MISR_GOLDEN[727:672]|||||||||
||INV_MISR_GOLDEN[783:728]|||||||||
||INV_MISR_GOLDEN[839:784]|||||||||
||INV_MISR_GOLDEN[895:840]|||||||||
|CFG for interval 0,<br>when rom_access_inversion<br>=1 (same as<br>when_rom_access_inversion<br>=0)|Reserved|pattern_cou<br>nt[9:0]|Reserved|Reserved|Reserved|Seg_ID[1]|Seg_ID[0<br>]|FT|TR_T|
||**INTERVAL 1**|||||||||
|CFG for interval 1, when<br>rom_access_inversion =0|Reserved|pattern_cou<br>nt[9:0]|Reserved|Reserved|Reserved|Seg_ID[1]|Seg_ID[0<br>]|FT|TR_T|
|MISR for interval 1, when<br>rom_access_inversion =0|MISR_GOLDEN[895:840]|||||||||
||MISR_GOLDEN[839:784]|||||||||
||MISR_GOLDEN[783:728]|||||||||
||MISR_GOLDEN[727:672]|||||||||
||MISR_GOLDEN[671:616]|||||||||
||MISR_GOLDEN[615:560]|||||||||
||MISR_GOLDEN[559:504]|||||||||
||MISR_GOLDEN[503:448]|||||||||
||MISR_GOLDEN[447:392]|||||||||
||MISR_GOLDEN[391:336]|||||||||
||MISR_GOLDEN[335:280]|||||||||
||MISR_GOLDEN[279:224]|||||||||
||MISR_GOLDEN[223:168]|||||||||
||MISR_GOLDEN[167:112]|||||||||
||MISR_GOLDEN[111:56]|||||||||
||MISR_GOLDEN[55:0]|||||||||



1682 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-274. ROM Organization for 2 Intervals (continued)** 

|**COMMENTS**|**55:40**|**41:32**|**31:16**|**15:8**|**7:4**|**3**|**2**|**1**|**0**|
|---|---|---|---|---|---|---|---|---|---|
|LP_MISR for interval 1, when<br>rom_access_inversion =0|LP_MISR_GOLDEN[895:840]|||||||||
||LP_MISR_GOLDEN[839:784]|||||||||
||LP_MISR_GOLDEN[783:728]|||||||||
||LP_MISR_GOLDEN[727:672]|||||||||
||LP_MISR_GOLDEN[671:616]|||||||||
||LP_MISR_GOLDEN[615:560]|||||||||
||LP_MISR_GOLDEN[559:504]|||||||||
||LP_MISR_GOLDEN[503:448]|||||||||
||LP_MISR_GOLDEN[447:392]|||||||||
||LP_MISR_GOLDEN[391:336]|||||||||
||LP_MISR_GOLDEN[335:280]|||||||||
||LP_MISR_GOLDEN[279:224]|||||||||
||LP_MISR_GOLDEN[223:168]|||||||||
||LP_MISR_GOLDEN[167:112]|||||||||
||LP_MISR_GOLDEN[111:56]|||||||||
||LP_MISR_GOLDEN[55:0]|||||||||
|Patterns for interval 1|P1_SD8[6:0<br>]|P1_SD7[6:0<br>]|P1_SD6[6<br>:0]|….|….|…|P1_SD1[<br>6:0]|||
|||…|…|…|…|…|…|P1_SD9[<br>6:0]||
|||…|…|…|…|…|…|…|…|
|LP_MISR for interval 1, when<br>rom_access_inversion =1|LP_INV_MISR_GOLDEN[55:0]|||||||||
||LP_INV_MISR_GOLDEN[111:56]|||||||||
||LP_INV_MISR_GOLDEN[167:112]|||||||||
||LP_INV_MISR_GOLDEN[223:168]|||||||||
||LP_INV_MISR_GOLDEN[279:224]|||||||||
||LP_INV_MISR_GOLDEN[335:280]|||||||||
||LP_INV_MISR_GOLDEN[391:336]|||||||||
||LP_INV_MISR_GOLDEN[447:392]|||||||||
||LP_INV_MISR_GOLDEN[503:448]|||||||||
||LP_INV_MISR_GOLDEN[559:504]|||||||||
||LP_INV_MISR_GOLDEN[615:560]|||||||||
||LP_INV_MISR_GOLDEN[671:616]|||||||||
||LP_INV_MISR_GOLDEN[727:672]|||||||||
||LP_INV_MISR_GOLDEN[783:728]|||||||||
||LP_INV_MISR_GOLDEN[839:784]|||||||||
||LP_INV_MISR_GOLDEN[895:840]|||||||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1683 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-274. ROM Organization for 2 Intervals (continued)** 

|**COMMENTS**|**55:40**|**41:32**|**31:16**|**15:8**|**7:4**|**3**|**2**|**1**|**0**|
|---|---|---|---|---|---|---|---|---|---|
|MISR for interval 1, when<br>rom_access_inversion =1|INV_MISR_GOLDEN[55:0]|||||||||
||INV_MISR_GOLDEN[111:56]|||||||||
||INV_MISR_GOLDEN[167:112]|||||||||
||INV_MISR_GOLDEN[223:168]|||||||||
||INV_MISR_GOLDEN[279:224]|||||||||
||INV_MISR_GOLDEN[335:280]|||||||||
||INV_MISR_GOLDEN[391:336]|||||||||
||INV_MISR_GOLDEN[447:392]|||||||||
||INV_MISR_GOLDEN[503:448]|||||||||
||INV_MISR_GOLDEN[559:504]|||||||||
||INV_MISR_GOLDEN[615:560]|||||||||
||INV_MISR_GOLDEN[671:616]|||||||||
||INV_MISR_GOLDEN[727:672]|||||||||
||INV_MISR_GOLDEN[783:728]|||||||||
||INV_MISR_GOLDEN[839:784]|||||||||
||INV_MISR_GOLDEN[895:840]|||||||||
|CFG for interval 1,<br>when rom_access_inversion<br>=1 (same as<br>when_rom_access_inversion<br>=0)|Reserved|pattern_cou<br>nt[9:0]|Reserved|Reserved|Reserved|Seg_ID[1]|Seg_ID[0<br>]|FT|TR_T|



The ROM contains the data to be processed by STC for the self-test run. This includes the control fields such as Segment ID, Pattern Count, and Golden MISR value for the STC, and the pattern scan data for the OPMISR controller. 

The ROM space is divided into chunks, with each chunk containing the data corresponding to one OPMISR interval. The size required for an interval varies depending on the number patterns packed into the interval and the length of internal scan chains required. 

Because each interval requires 64 rows of ROM for storing control and Golden MISR values, minimizing the number of intervals by packing more patterns into each interval provides the best ROM size. This works best if the self-test must be run only as a part of the boot-up sequence. However, if the self-test is performed during application IDLE time, the number of patterns that can be packed into each interval will be dictated by the IDLE time available for the self-test, because an interval is the smallest granularity of a self-test run. 

Details of the ROM image micro-code fields are given in the following sections. 

## _**13.6.5.3.7.1 TR_T: Transition Delay Methodology Type**_ 

This specifies the transition delay methodology for the current transition delay interval. 

0 Launch-on-System-Clock 

## _**13.6.5.3.7.2 FT: Fault Model for the BIST Run**_ 

This specifies the fault model for the current interval of the test. 

0 Stuck-at 

## _**13.6.5.3.7.3 SEG_ID[1:0]**_ 

This indicates which logical segment is selected for the associated interval during the self-test run. 

1684 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

|**SEG_**<br>**SEL[**<br>**1:0]**|**Segment Under Test**|
|---|---|
|00|Segment 0|
|01|Segment 1|
|10|Segment 2|
|11|Segment 3|



## _**13.6.5.3.7.4 Pattern Count ( patt_count[9:0] )**_ 

This specifies the number of scan data patterns within a self-test interval. The pattern counts can vary from a minimum of 2 to a maximum of 1024. 

|**patt_**<br>**coun**<br>**t[9:0]**|**Patterns per Interval**|
|---|---|
|00_0<br>000_<br>0000|Not a valid interval<br>[defaults to 2 patterns per<br>interval]|
|00_0<br>000_<br>0001|2 patterns per interval|
|00_0<br>000_<br>0010|3 patterns per interval|
|...|...|
|11_11<br>11_11<br>10|1023 patterns per interval|
|11_11<br>11_11<br>11|1024 patterns per interval|



## _**13.6.5.3.7.5 MISR_GOLDEN[895:0]: Golden Signature Data Bits**_ 

This part of ROM contains the golden signature data of the current interval. This value is used to compare with the actual MISR value, when ST_GCR1.ROM_ACCESS_INV=0 and ST_GCR1.LP_SCAN_MODE=0, to generate the pass/fail information of the interval. 

## _**13.6.5.3.7.6 LP_MISR_GOLDEN[895:0]: Low Power Mode Golden Signature Data Bits**_ 

This part of ROM contains the LP golden signature data of the current interval. This value is used to compare with the actual MISR value, when STCGCR1.ROM_ACCESS_INV=0 and STCGCR1.LP_SCAN_MODE=1, to generate the pass/fail information of the interval. 

## **Note** 

This mode is not supported on AM26xx devices. 

## _**13.6.5.3.7.7 INV_MISR_GOLDEN[895:0]: Inverse Mode Golden Signature Data Bits**_ 

This part of ROM contains the inverse mode golden signature data of the current interval. This value is used to compare with the actual MISR value, when STCGCR1.ROM_ACCESS_INV=1 and STCGCR1.LP_SCAN_MODE=0, to generate the pass/fail information of the interval. 

## **Note** 

This mode is not supported on AM26xx devices. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1685 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.6.5.3.7.8 LP_INV_MISR_GOLDEN[895:0]: Low Power Inverse Mode Golden Signature Data Bits**_ 

This part of ROM contains the low-power inverse mode golden signature data of the current interval. This value is used to compare with the actual MISR value, when STCGCR1.ROM_ACCESS_INV=1 and STCGCR1.LP_SCAN_MODE=1, to generate the pass/fail information of the interval. 

## **Note** 

This mode is not supported on AM26xx devices. 

## _**13.6.5.3.7.9 Pn_SDm[7:0] (n - no. of patterns, m - scan chain length): OP-MISR Scan Data**_ 

This part of the ROM contains the scan data corresponding to each pattern. Each interval can have n number of scan patterns, as defined in the patt_count field. The number of 7bits of scan data in a pattern is equal to the length of the scan chain formed inside the UUT. 

## _**13.6.6 Programmable Built-In Self-Test (PBIST) Module**_ 

This chapter describes the programmable built-in self-test (PBIST) controller module used for testing the on-chip memories on the AM26x family of microcontrollers. 

**13.6.6.1 Overview** .................................................................................................................................................. 1687 **13.6.6.2 PBIST Flow** ...............................................................................................................................................1689 **13.6.6.3 PBIST RAM-ROM Memory and Algorithm Group Configuration** .........................................................1691 **13.6.6.4 Memory Test Algorithms on the On-chip ROM** .....................................................................................1693 

1686 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.6.6.1 Overview** 

The PBIST (Programmable Built-In Self-Test) controller architecture provides a run-time-programmable memory BIST engine for varying levels of coverage across many embedded memory instances. 

## _**13.6.6.1.1 Features of PBIST**_ 

- Information regarding on-chip memories, memory groupings, memory background patterns and test algorithms stored in dedicated on-chip PBIST ROM 

- Host processor interface to configure and start BIST of memories 

- Supports testing of PBIST ROM itself as well 

- Supports testing of each memory at its maximum access speed in application 

- Implements intelligent clock gating to conserve power 

## _**13.6.6.1.2 PBIST vs. Application Software-Based Testing**_ 

The PBIST architecture consists of a small coprocessor with a dedicated instruction set targeted specifically toward testing memories. This coprocessor executes test routines stored in the PBIST ROM and runs them on multiple on-chip memory instances. The on-chip memory configuration information is also stored in the PBIST ROM. The testing is done in parallel for each of the CPU data RAMs, while it is done sequentially for the rest of the memories. 

The PBIST Controller architecture offers significant advantages over tests running on the main Cortex-R5F processor (application software-based testing): 

- Embedded CPUs have a long access path to memories outside the tightly-couple memory sub-system, while the PBIST controller has a dedicated path to the memories specifically for the self-test 

- Embedded CPUs are designed for their targeted use and are often not easily programmed for memory test algorithms. 

- The memory test algorithm code on embedded CPUs is typically significantly larger than that needed for PBIST. 

- The embedded CPU is significantly larger than the PBIST controller. 

## _**13.6.6.1.3 PBIST Block Diagram**_ 

Figure 13-251 illustrates the basic PBIST blocks and its wrapper logic for the device. 

**==> picture [332 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
Host CPU<br>Control Interface<br>Memory<br>Configurations,<br>PBIST PBIST<br>ROM Controller<br>Algorithms,<br>System<br>Backgrouns Memory and<br>Data<br>Path Peripheral<br>Memories<br>Data Logger<br>**----- End of picture text -----**<br>


**Figure 13-251. PBIST Block Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1687 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.6.6.1.3.1 On-chip ROM**_ 

The on-chip ROM contains the information regarding the algorithms and memories to be tested. 

## _**13.6.6.1.3.2 Host Processor Interface to the PBIST Controller Registers**_ 

The Cortex-R5 CPU can select the algorithm and RAM groups for the memories' self-test from the on-chip ROM based on the application requirements. Once the self-test has executed, the CPU can query the PBIST controller registers to identify any memories that failed the self-test and to then take appropriate next steps as required by the application's author. 

## _**13.6.6.1.3.3 Memory Data Path**_ 

This is the read and write data path logic between different system and peripheral memories tightly coupled to the PBIST memory interface. The PBIST controller executes each selected algorithm on each valid memory group sequentially until all the algorithms are executed. 

1688 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.6.6.2 PBIST Flow** 

This section describes the sequence to be followed for enabling memory self-test on any intended memory group. 

## **Note** 

- PBIST Self-Test Key and Reset register has to be programmed before configuring any other PBIST registers for memory test. 

- MSS_CTRL.TOP_PBIST_KEY_RST[3:0] = 0x5, MSS_CTRL.TOP_PBIST_KEY_RST[7:4]=0xA. 

- When testing through R5, ensure PBIST interrupt to R5 CA and CB (VIM modules) is enabled and configured to handle the corresponding ISR. 

- When testing through R4, ensure PBIST interrupt to R4 (VIM modules) is enabled and configured to handle the corresponding ISR. 

Before re-programming PBIST registers to target test for a different memory group, the Self-Test Key and Reset register bits [7:0] should be reset to reset the PBIST controller and hence clear the status of PBIST internal registers. 

MSS_CTRL.TOP_PBIST_KEY_RST[7:0]=0x0 

**Table 13-275. PBIST Flow** 

|**Step #**|**Step**|**Register/Bitfield/Programming**|**Value**|
|---|---|---|---|
|1|Enable the Top PBIST Self-Test Key|MSS_CTRL.TOP_PBIST_KEY_RST[3:0]|0x5|
|2|Bring PBIST controller and MDP logic out of<br>reset|MSS_CTRL.TOP_PBIST_KEY_RST[7:4]|0xA|
|3|Enable the PBIST internal clocks and ROM<br>interface clock|TOP_PBIST.PBIST_PACT|0x1|
|4|Ensure the Loop count register is at its reset<br>value|TOP_PBIST.PBIST_L0<br>TOP_PBIST.PBIST_L1<br>TOP_PBIST.PBIST_L2<br>TOP_PBIST.PBIST_L3|0x0|
|5|Program Override register to allow<br>configuration of memory group and algorithm<br>group registers|TOP_PBIST.PBIST_OVR|0x9|
|6|Program DLR register|TOP_PBIST.PBIST_DLR|0x10|
|7|Clear the memory group registers|TOP_PBIST.PBIST_RINFOL<br>TOP_PBIST.PBIST_RINFOU|0x0|
|8|Clear the algorithm register|TOP_PBIST.PBIST_ALGO|0x0|
|9|Program the algorithm register for the intended<br>algorithm (Refer toPBIST RAM-ROM Memory<br>and Algorithm Group Configuration)|TOP_PBIST.PBIST_ALGO|*Values mentioned inPBIST<br>RAM-ROM Memory and<br>Algorithm Group Configuration|
|10|Program the memory group number on which<br>selected algorithm is to be run. (ReferPBIST<br>RAM-ROM Memory and Algorithm Group<br>Configuration)|TOP_PBIST.PBIST_RINFOL<br>TOP_PBIST.PBIST_RINFOU|*Values mentioned inPBIST<br>RAM-ROM Memory and<br>Algorithm Group Configuration|
|11|Re-Program the Override register to mask<br>overwriting of RINFOL, RINFOU, ALGO<br>registers from PBIST ROM after PBIST<br>execution starts|TOP_PBIST.PBIST_OVR|0x0|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1689 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-275. PBIST Flow (continued)** 

|**Step #**|**Step**|**Register/Bitfield/Programming**|**Value**|
|---|---|---|---|
|12|Ensure ROM MASK Register is set to ensure<br>both Algorithm and memory information is<br>picked from PBIST ROM.|TOP_PBIST.PBIST_ROM|0x3|
|13|Kick off PBIST test|TOP_PBIST.PBIST_DLR|0x021C|
|14|Wait for Interrupt (Refer to Section ‘Top PBIST Interrupt signal Integration’ for interrupt mapping)|||
|15|Read Fail Status Register to check the status<br>of the test|TOP_PBIST.PBIST_FSRF0<br>TOP_PBIST.PBIST_FSRF1|(READ) 0x0 - Test Pass Non-<br>zero value - Test Fail|
|16|Read Address registers to ensure Test has<br>been indeed run|TOP_PBIST.PBIST_CA1<br>TOP_PBIST.PBIST_CA2|(READ)0x0- test has not been<br>runNon- zero – test is correctly<br>run|
|17|Program PACT back to reset value (Gating<br>PBIST internal clocks – test exit sequence )|TOP_PBIST.PBIST_PACT|0x0|
|18|Disable the Top PBIST Self-Test Key and<br>assert reset to PBIST controller and MDP logic|MSS_CTRL.TOP_PBIST_KEY_RST[7:0]|0x0|



1690 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.6.6.3 PBIST RAM-ROM Memory and Algorithm Group Configuration** 

This section describes the memory and algorithm group and corresponding register configuration, which need to be programmed to trigger PBIST test on the allowed memory groups. 

## **Note** 

- The contents of the selected memory after the test will be completely lost. User software must take care of data restoration if required. Typically, the memory Self-Tests are carried out at the beginning of Application software. 

- Only the following register configurations are supported, any other register configuration apart from the below mentioned values will put the design into invalid state. 

- Memory Self-Test of multiple memory groups can be triggered in single trigger, only if the test algorithm (PBIST_ALGO*) is common across the memory groups. The configuration of other register in the table (like PBIST_RINFOL, PBIST_RINFOU) should be logical OR of all the memory groups. 

- Memory Self-Test of multiple memory groups cannot be triggered together across multiple test algorithm groups. 

- Self- Test of memory groups corresponding to Top PBIST will be handled by MSS CR5 – A or B (depending on lockstep or dual-core modes) 

**Table 13-276. Memory and Algorithm Group Configuration** 

|**Memory**<br>**Group #**|**Memory Group Description**|**Algorithm Description**|**Memory Group REG bit**<br>**to be Programmed to**<br>**0x1**|**Algorithm REG bit to be**<br>**programmed to 0x1**|
|---|---|---|---|---|
|1|MEM_MSS_R5_STC|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[0]|PBIST_ALGO[0]|
|2|MEM_MSS_R51_STC|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[1]|PBIST_ALGO[0]|
|3|MEM_MSS_R5SS0_TMU1|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[2]|PBIST_ALGO[1]|
|4|MEM_MSS_R5SS0_TMU2|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[3]|PBIST_ALGO[2]|
|5|MEM_MSS_R5SS0_TMU3|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[4]|PBIST_ALGO[3]|
|6|MEM_MSS_R5SS0_TMU4|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[5]|PBIST_ALGO[1]|
|7|MEM_MSS_R5SS0_TMU5|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[6]|PBIST_ALGO[2]|
|8|MEM_MSS_R5SS0_TMU6|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[7]|PBIST_ALGO[3]|
|9|MEM_MSS_R5SS1_TMU1|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[8]|PBIST_ALGO[1]|
|10|MEM_MSS_R5SS1_TMU2|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[9]|PBIST_ALGO[2]|
|11|MEM_MSS_R5SS1_TMU3|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[10]|PBIST_ALGO[3]|
|12|MEM_MSS_R5SS1_TMU4|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[11]|PBIST_ALGO[1]|
|13|MEM_MSS_R5SS1_TMU5|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[12]|PBIST_ALGO[2]|
|14|MEM_MSS_R5SS1_TMU6|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[13]|PBIST_ALGO[3]|
|15|MEM_TOP_PBISTROM|ROM -<br>Triple_Read_XOR_Read|PBIST_RINFOL[14]|PBIST_ALGO[4]|
|16|MEM_CR5A_ROM0|ROM - Triple_Read_XOR_Read|PBIST_RINFOL[15]|PBIST_ALGO[5]|
|17|MEM_CR5A_ROM1|ROM – Triple_Read_XOR_Read|PBIST_RINFOL[16]|PBIST_ALGO[6]|
|18|MEM_MSS_CPSW|RAM - March 13N Single Port|PBIST_RINFOL[17]|PBIST_ALGO[7]|
|19|MEM_MSS_ECU_PERIPH|RAM - March 13N Single Port|PBIST_RINFOL[18]|PBIST_ALGO[7]|
|20|MEM_MSS_FOTA|RAM - March 13N Single Port|PBIST_RINFOL[19]|PBIST_ALGO[7]|
|21|MEM_MSS_ICSSM|RAM - March 13N Single Port|PBIST_RINFOL[20]|PBIST_ALGO[7]|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1691 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-276. Memory and Algorithm Group Configuration (continued)** 

|**Memory**<br>**Group #**|**Memory Group Description**|**Algorithm Description**|**Memory Group REG bit**<br>**to be Programmed to**<br>**0x1**|**Algorithm REG bit to be**<br>**programmed to 0x1**|
|---|---|---|---|---|
|22|MEM_MSS_MBOX|RAM - March 13N Single Port|PBIST_RINFOL[21]|PBIST_ALGO[7]|
|23|MEM_MSS_L2_0|RAM - March 13N Single Port|PBIST_RINFOL[22]|PBIST_ALGO[7]|
|24|MEM_MSS_L2_1|RAM - March 13N Single Port|PBIST_RINFOL[23]|PBIST_ALGO[7]|
|25|MEM_MSS_L2_2|RAM - March 13N Single Port|PBIST_RINFOL[24]|PBIST_ALGO[7]|
|26|MEM_MSS_L2_3|RAM - March 13N Single Port|PBIST_RINFOL[25]|PBIST_ALGO[7]|
|27|MEM_MSS_L2_4|RAM - March 13N Single Port|PBIST_RINFOL[26]|PBIST_ALGO[7]|
|28|MEM_MSS_L2_5|RAM - March 13N Single Port|PBIST_RINFOL[27]|PBIST_ALGO[7]|
|29|MEM_MSS_TPCC|RAM - March 13N Single Port|PBIST_RINFOL[28]|PBIST_ALGO[7]|
|30|MEM_MSS_OSPI|RAM - March 13N Single Port|PBIST_RINFOL[29]|PBIST_ALGO[7]|
|31|MEM_MSS_R5SS0_VIM0|RAM - March 13N Single Port|PBIST_RINFOL[30]|PBIST_ALGO[7]|
|32|MEM_MSS_R5SS0_VIM1|RAM - March 13N Single Port|PBIST_RINFOL[31]|PBIST_ALGO[7]|
|33|MEM_MSS_R5SS0_RL2_CPU0|RAM - March 13N Single Port|PBIST_RINFOU[0]|PBIST_ALGO[7]|
|34|MEM_MSS_R5SS0_RL2_CPU1|RAM - March 13N Single Port|PBIST_RINFOU[1]|PBIST_ALGO[7]|
|35|MEM_MSS_R5SS1_VIM0|RAM - March 13N Single Port|PBIST_RINFOU[2]|PBIST_ALGO[7]|
|36|MEM_MSS_R5SS1_VIM1|RAM - March 13N Single Port|PBIST_RINFOU[3]|PBIST_ALGO[7]|
|37|MEM_MSS_R5SS1_RL2_CPU0|RAM - March 13N Single Port|PBIST_RINFOU[4]|PBIST_ALGO[7]|
|38|MEM_MSS_R5SS1_RL2_CPU1|RAM - March 13N Single Port|PBIST_RINFOU[5]|PBIST_ALGO[7]|
|39|MEM_MSS_TRACE|RAM - March 13N Single Port|PBIST_RINFOU[6]|PBIST_ALGO[7]|
|40|MEM_MSS_CR5A_ATCM0_R5SS0|RAM - March 13N Single Port|PBIST_RINFOU[7]|PBIST_ALGO[7]|
|41|MEM_MSS_CR5A_ATCM0_R5SS1|RAM - March 13N Single Port|PBIST_RINFOU[8]|PBIST_ALGO[7]|
|42|MEM_MSS_CR5A_BTCM0_R5SS0|RAM - March 13N Single Port|PBIST_RINFOU[9]|PBIST_ALGO[7]|
|43|MEM_MSS_CR5A_BTCM0_R5SS1|RAM - March 13N Single Port|PBIST_RINFOU[10]|PBIST_ALGO[7]|
|44|MEM_MSS_CR5B_ATCM0_R5SS0|RAM - March 13N Single Port|PBIST_RINFOU[11]|PBIST_ALGO[7]|
|45|MEM_MSS_CR5B_ATCM0_R5SS1|RAM - March 13N Single Port|PBIST_RINFOU[12]|PBIST_ALGO[7]|
|46|MEM_MSS_CR5B_BTCM0_R5 SS0|RAM - March 13N Single Port|PBIST_RINFOU[13]|PBIST_ALGO[7]|
|47|MEM_MSS_CR5B_BTCM0_R5 SS1|RAM - March 13N Single Port|PBIST_RINFOU[14]|PBIST_ALGO[7]|
|48|MEM_MSS_R5SS0_C0|RAM - March 13N Single Port|PBIST_RINFOU[15]|PBIST_ALGO[7]|
|49|MEM_MSS_R5SS0_C1|RAM - March 13N Single Port|PBIST_RINFOU[16]|PBIST_ALGO[7]|
|50|MEM_MSS_R5SS1_C0|RAM - March 13N Single Port|PBIST_RINFOU[17]|PBIST_ALGO[7]|
|51|MEM_MSS_R5SS1_C1|RAM - March 13N Single Port|PBIST_RINFOU[18]|PBIST_ALGO[7]|
|52|MEM_MSS_MMCH0|RAM - March 13N Two Port|PBIST_RINFOU[19]|PBIST_ALGO[8]|
|53|MEM_MSS_MMCH1|RAM - March 13N Two Port|PBIST_RINFOU[20]|PBIST_ALGO[8]|



Because the entire memory is corrupted during PBIST test, the memory contents before the test is triggered must be compared to the memory contents after processor execution and test completion. Specific scenarios for Top PBIST are mentioned below: 

1692 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- **TCMB Memories** – Since this memory is used as a data memory by CR5, it may hold some valid data variables and may cause issue with CR5 execution post PBIST test. Should be tested before R5 boot-up in assembly code. 

- **R5 Cache** – Cache should be cleaned and disabled before triggering PBIST test so that after test CR5 should not execute code directly from cache since cache will hold junk data. 

- **R5SS VIM Memories** – Since ISR is stored in VIM memories, if VIM memories are to be tested, polling on interrupt line should be done and not ISR execution. 

## **13.6.6.4 Memory Test Algorithms on the On-chip ROM** 

This section provides a brief description of the test algorithm used for memory self-test. 

1. **March13N:** 

   - March13N is the baseline test algorithm for SRAM testing. It provides the highest overall coverage. 

   - The concept behind the general march algorithm is to indicate: 

      - The bit cell can be written and read as both a 1 and a 0. 

      - The bits around the bit cell do not affect the bit cell. 

   - The basic operation of the march is to initialize the array to a know pattern, then march a different pattern through the memory. 

   - Type of faults detected by this algorithm: 

      - Address decoder faults 

      - Stuck-At faults 

      - Coupled faults 

      - State coupling faults 

      - Parametric faults 

      - Write recovery faults 

      - Read/write logic faults 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1693 

Copyright © 2025 Texas Instruments Incorporated 

