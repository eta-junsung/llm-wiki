<!-- AM263P TRM | 13.4 Industrial & Control (MCAN, LIN) | 원본 p.1486-1595 | pymupdf4llm text+tables, images omitted -->

_Peripherals_ 

www.ti.com 

## **13.4 Industrial and Control Interfaces** 

This section describes the industrial and control interfaces in the device. 

1486 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.1 Modular Controller Area Network (MCAN)**_ 

This section describes the Modular Controller Area Network (MCAN) modules in the device. 

## **13.4.1.1 MCAN Overview** 

The Modular Controller Area Network (MCAN) module that implements the CAN interface. CAN is a serial communications protocol which efficiently supports distributed real-time control with a high immunity to electrical interference. In a CAN network, many short messages are broadcast to the entire network, which enables data consistency across every node of the system. 

The MCAN module supports both classic CAN and CAN FD (CAN with Flexible Data-Rate) specifications. CAN FD feature allows high throughput and increased payload per data frame and is compliant to ISO 11898-1:2015. The classic CAN and CAN FD devices can coexist on the same network without any conflict. 

The module connects to the physical layer of a CAN network through external transceivers. 

## _**13.4.1.1.1 MCAN Features**_ 

Each MCAN module implements the following features: 

- Conforms with CAN Protocol 2.0 A, B and ISO 11898-1:2015 

- Full CAN FD support (up to 64 data bytes) 

- SAE J1939 support 

- AUTOSAR support 

- Up to 32 dedicated Transmit Buffers 

- Configurable Transmit FIFO, up to 32 elements 

- Configurable Transmit Queue, up to 32 elements 

- Configurable Transmit Event FIFO, up to 32 elements 

- Up to 64 dedicated Receive Buffers 

- Two configurable Receive FIFOs, up to 64 elements each 

- Up to 128 filter elements 

- Internal Loopback mode for self-test 

- Maskable interrupts, two interrupt lines 

- Two clock domains (CAN clock/Host clock) 

- Parity/ECC support - Message RAM single error correction and double error detection (SECDED) mechanism 

- Local power-down and wakeup support 

- Timestamp Counter 

## _**13.4.1.1.2 MCAN Not Supported Features**_ 

- Host Bus Firewall 

- GPIO Mode 

- Clock Calibration 

- External (IO) Loopback Mode 

- Debug DMA (see Section 13.4.1.4.7.4) 

- TX DMA Channels [31:4] 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1487 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.4.1.2 MCAN Environment** 

All module instances are hereinafter referred to as MCAN module. 

This section describes the external MCAN connections (environment). 

The CAN network physical layer consists of two-wire differential bus, usually twisted pair, and provides high level of interference immunity. An xternal CAN transceiver IC is needed to access a CAN bus by the MCAN. 

Figure 13-164 shows the MCAN typical application. 

**==> picture [440 x 213] intentionally omitted <==**

**----- Start of picture text -----**<br>
120 Ω<br>Device<br>MCAN CAN Node 1<br>CAN Transceiver ..<br>.<br>TX D CANH ...<br>.<br>.<br>RX R CANL ..<br>CAN Node N<br>120 Ω<br>mcan-002<br>**----- End of picture text -----**<br>


**Figure 13-164. MCAN Typical Application** 

Table 13-203 describes the MCAN I/O signals. 

**Table 13-203. MCAN I/O Signals** 

|**Module Pin**|**Device Level Signal**|**I/O**(1)|**Description**|**Module Pin**|
|---|---|---|---|---|
|||||**Reset Value**(1)|
||||**MCAN[0-7]**||
|RX|MCAN0_RX|I|Serial data input from external CAN transceiver|HiZ|
|TX|MCAN0_TX|O|Serial data output to external CAN transceiver|1|
|RX|MCAN1_RX|I|Serial data input from external CAN transceiver|HiZ|
|TX|MCAN1_TX|O|Serial data output to external CAN transceiver|1|
|RX|MCAN2_RX|I|Serial data input from external CAN transceiver|HiZ|
|TX|MCAN2_TX|O|Serial data output to external CAN transceiver|1|
|RX|MCAN3_RX|I|Serial data input from external CAN transceiver|HiZ|
|TX|MCAN3_TX|O|Serial data output to external CAN transceiver|1|
|RX|MCAN4_RX|I|Serial data input from external CAN transceiver|HiZ|
|TX|MCAN4_TX|O|Serial data output to external CAN transceiver|1|
|RX|MCAN5_RX|I|Serial data input from external CAN transceiver|HiZ|
|TX|MCAN5_TX|O|Serial data output to external CAN transceiver|1|
|RX|MCAN6_RX|I|Serial data input from external CAN transceiver|HiZ|
|TX|MCAN6_TX|O|Serial data output to external CAN transceiver|1|
|RX|MCAN7_RX|I|Serial data input from external CAN transceiver|HiZ|
|TX|MCAN7_TX|O|Serial data output to external CAN transceiver|1|



(1) I = Input; O = Output; HiZ = High Impedance 

1488 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

For more information about device level signals (pull-up/down resistors, buffer type, multiplexing and others), see tables Pin Attributes and Pin Multiplexing in the device-specific Data sheet. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1489 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.1.2.1 CAN Network Basics**_ 

- CAN bus is a 2-wire differential bus using Non-Return-to-Zero (NRZ) encoding and has two states: 

   - Recessive state (logical 1) 

   - Dominant state (logical 0) 

- The network is multicontroller. When two or more nodes (ECUs) attempt to transmit at the same time, a non-destructive arbitration technique guarantees messages are sent in order of priority and no messages are lost. 

- The message transmission is multicast. Data messages transmitted are identifier based, not address based. 

- Content of message is labeled by the identifier that is unique throughout the network (for example: rpm, temperature, position, pressure, and so forth). 

- All nodes on network receive the message and each performs an acceptance test on the identifier. If message is relevant, it is processed, otherwise it is ignored. 

- The unique identifier also determines the priority of the message (the lower the numerical value of the identifier, the higher the priority is). 

- Data is transmitted and received using message frames, consisting of the following basic fields: 

   - Arbitration field 

   - Control field 

   - Data field (up to 8 bytes for Classical CAN and up to 64 bytes for CAN FD) 

   - CRC field 

   - ACK field 

For more information, see _ISO 11898-1:2015: CAN data link layer and physical signaling_ . 

1490 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.4.1.3 MCAN Integration** 

There are 8x MCAN modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [420 x 300] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>CAN#<br>CAN#_VBUSCLK<br>CAN#_TX_DMA_REQ<br>4 EDMA<br>CAN#_CORE_FILTER_EVENTS_DMA_REQ<br>SYS_CLK 7<br>XTALCLK<br>CAN#_TXD<br>EXT_REFCLK<br>PER_PLL_HSDIV0_CLKOUT1 ÷   CAN#_CLK CAN#_RXD<br>CORE_PLL_HSDIV0_CLKOUT0<br>RCOSC (10MHz)<br>ICSSM<br>XTALCLK<br>RCOSC (10MHz)<br>R5FSS0-CORE0<br>CAN#_EXT_TS_ROLLOVER_LVL_INT_0 R5FSS0-CORE1<br>RCM<br>CAN#_LVL_INT_0 R5FSS1-CORE0<br>CAN#_CLKSRC_SEL Bit<br>CAN#_CLKDIV_SEL Bit CAN#_LVL_INT_1 R5FSS1-CORE1<br>CAN#_RST_CTRL Bit<br>CAN#_ECC_CORR_LVL_INT<br>ESM<br>CAN#_WARMRESET CAN#_ECC_UNCORR_LVL_INT<br>Warm Reset Sources<br>PERI INTERCONNECT<br>ICSSM XBAR<br>DMA  XBAR<br>**----- End of picture text -----**<br>


**Figure 13-165. MCAN Integration Diagram** 

The tables below summarize the device integration details of MCAN# (where # = 0 to 7). 

**Table 13-204.** _**MCAN**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|MCAN0|✓|Peripheral VBUSP Interconnect|
|MCAN1|✓|Peripheral VBUSP Interconnect|
|MCAN2|✓|Peripheral VBUSP Interconnect|
|MCAN3|✓|Peripheral VBUSP Interconnect|
|MCAN4|✓|Peripheral VBUSP Interconnect|
|MCAN5|✓|Peripheral VBUSP Interconnect|
|MCAN6|✓|Peripheral VBUSP Interconnect|
|MCAN7|✓|Peripheral VBUSP Interconnect|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1491 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-205.** _**MCAN**_ **Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|MCAN0|MCAN0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN0 Interface Clock|
||MCAN0_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN0 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|MCAN1|MCAN1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN1 Interface Clock|
||MCAN1_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN1 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|MCAN2|MCAN2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN2 Interface Clock|
||MCAN2_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN2 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||



1492 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-205.** _**MCAN**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|MCAN3|MCAN3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN3 Interface Clock|
||MCAN3_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN3 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|MCAN4|MCAN4_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN4 Interface Clock|
||MCAN4_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN4 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|MCAN5|MCAN5_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN5 Interface Clock|
||MCAN5_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN5 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1493 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-205.** _**MCAN**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|MCAN6|MCAN6_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN6 Interface Clock|
||MCAN6_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN6 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|MCAN7|MCAN7_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN7 Interface Clock|
||MCAN7_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN7 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||



**Table 13-206.** _**MCAN**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|MCAN0|MCAN0_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN0 Module Reset|
|MCAN1|MCAN1_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN1 Module Reset|
|MCAN2|MCAN2_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN2 Module Reset|
|MCAN3|MCAN3_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN3 Module Reset|
|MCAN4|MCAN4_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN4 Module Reset|
|MCAN5|MCAN5_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN5 Module Reset|



1494 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-206.** _**MCAN**_ **Resets (continued)** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|MCAN6|MCAN6_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN6 Module Reset|
|MCAN7|MCAN7_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN7 Module Reset|



**Table 13-207.** _**MCAN**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN0|MCAN0_INT_0|R5FSS0_CORE0_INTR_IN_27|R5FSS0-0|Level|MCAN0 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_27|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_27|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_27|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_40|PRU_ICSS|||
||MCAN0_INT_1|R5FSS0_CORE0_INTR_IN_28|R5FSS0-0|Level|MCAN0 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_28|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_28|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_28|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_41|PRU_ICSS|||
||MCAN0_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_26|R5FSS0-0|Level|MCAN0 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_26|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_26|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_26|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_39|PRU_ICSS0|||
||MCAN0_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_2|ESM0|Level|MCAN0 ECC Correctable Error<br>Interrupt|
||MCAN0_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_3|ESM0|Level|MCAN0 ECC Uncorrectable<br>Error Interrupt|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1495 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-207.** _**MCAN**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN1|MCAN1_INT_0|R5FSS0_CORE0_INTR_IN_30|R5FSS0-0|Level|MCAN1 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_30|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_30|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_30|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_43|PRU_ICSS|||
||MCAN1_INT_1|R5FSS0_CORE0_INTR_IN_31|R5FSS0-0|Level|MCAN1 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_31|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_31|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_31|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_44|PRU_ICSS|||
||MCAN1_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_29|R5FSS0-0|Level|MCAN1 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_29|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_29|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_29|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_42|PRU_ICSS|||
||MCAN1_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_4|ESM0|Level|MCAN1 ECC Correctable Error<br>Interrupt|
||MCAN1_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_5|ESM0|Level|MCAN1 ECC Uncorrectable<br>Error Interrupt|
|MCAN2|MCAN2_INT_0|R5FSS0_CORE1_INTR_IN_33|R5FSS0-0|Level|MCAN1 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_33|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_33|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_33|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_46|PRU_ICSS|||
||MCAN2_INT_1|R5FSS0_CORE0_INTR_IN_34|R5FSS0-0|Level|MCAN2 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_34|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_34|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_34|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_47|PRU_ICSS|||
||MCAN2_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_32|R5FSS0-0|Level|MCAN2 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_32|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_32|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_32|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_45|PRU_ICSS|||
||MCAN2_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_6|ESM0|Level|MCAN2 ECC Correctable Error<br>Interrupt|
||MCAN2_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_7|ESM0|Level|MCAN2 ECC Uncorrectable<br>Error Interrupt|



1496 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-207.** _**MCAN**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN3|MCAN3_INT_0|R5FSS0_CORE0_INTR_IN_36|R5FSS0-0|Level|MCAN3 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_36|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_36|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_36|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_49|PRU_ICSS|||
||MCAN3_INT_1|R5FSS0_CORE0_INTR_IN_37|R5FSS0-0|Level|MCAN3 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_37|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_37|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_37|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_50|PRU_ICSS|||
||MCAN3_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_35|R5FSS0-0|Level|MCAN3 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_35|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_35|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_35|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_48|PRU_ICSS|||
||MCAN3_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_8|ESM0|Level|MCAN3 ECC Correctable Error<br>Interrupt|
||MCAN3_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_9|ESM0|Level|MCAN3 ECC Uncorrectable<br>Error Interrupt|
|MCAN4|MCAN4_INT_0|R5FSS0_CORE0_INTR_IN_198|R5FSS0-0|Level|MCAN4 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_198|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_198|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_198|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_60|PRU_ICSS|||
||MCAN4_INT_1|R5FSS0_CORE0_INTR_IN_199|R5FSS0-0|Level|MCAN4 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_199|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_199|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_199|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_61|PRU_ICSS|||
||MCAN4_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_197|R5FSS0-0|Level|MCAN4 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_197|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_197|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_197|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_59|PRU_ICSS|||
||MCAN4_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_39|ESM0|Level|MCAN4 ECC Correctable Error<br>Interrupt|
||MCAN4_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_40|ESM0|Level|MCAN4 ECC Uncorrectable<br>Error Interrupt|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1497 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-207.** _**MCAN**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN5|MCAN5_INT_0|R5FSS0_CORE0_INTR_IN_201|R5FSS0-0|Level|MCAN5 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_201|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_201|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_201|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_63|PRU_ICSS|||
||MCAN5_INT_1|R5FSS0_CORE0_INTR_IN_202|R5FSS0-0|Level|MCAN5 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_202|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_202|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_202|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_64|PRU_ICSS|||
||MCAN5_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_200|R5FSS0-0|Level|MCAN5 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_200|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_200|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_200|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_62|PRU_ICSS|||
||MCAN5_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_41|ESM0|Level|MCAN5 ECC Correctable Error<br>Interrupt|
||MCAN5_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_42|ESM0|Level|MCAN5 ECC Uncorrectable<br>Error Interrupt|
|MCAN6|MCAN6_INT_0|R5FSS0_CORE0_INTR_IN_204|R5FSS0-0|Level|MCAN6 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_204|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_204|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_204|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_66|PRU_ICSS|||
||MCAN6_INT_1|R5FSS0_CORE0_INTR_IN_205|R5FSS0-0|Level|MCAN6 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_205|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_205|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_205|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_67|PRU_ICSS|||
||MCAN6_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_203|R5FSS0-0|Level|MCAN6 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_203|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_203|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_203|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_65|PRU_ICSS|||
||MCAN6_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_43|ESM0|Level|MCAN6 ECC Correctable Error<br>Interrupt|
||MCAN6_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_44|ESM0|Level|MCAN6 ECC Uncorrectable<br>Error Interrupt|



1498 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-207.** _**MCAN**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN7|MCAN7_INT_0|R5FSS0_CORE0_INTR_IN_207|R5FSS0-0|Level|MCAN7 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_207|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_207|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_207|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_69|PRU_ICSS|||
||MCAN7_INT_1|R5FSS0_CORE0_INTR_IN_208|R5FSS0-0|Level|MCAN7 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_208|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_208|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_208|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_70|PRU_ICSS|||
||MCAN7_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_206|R5FSS0-0|Level|MCAN7 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_206|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_206|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_206|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_68|PRU_ICSS|||
||MCAN7_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_45|ESM0|Level|MCAN7 ECC Correctable Error<br>Interrupt|
||MCAN7_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_46|ESM0|Level|MCAN7 ECC Uncorrectable<br>Error Interrupt|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1499 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-208.** _**MCAN**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN0|MCAN0_FE_INTR_0|EDMA_XBAR_147|EDMA|Pulse|MCAN0 Receive Filter Event 0<br>DMA Request|
||MCAN0_FE_INTR_1|EDMA_XBAR_148|EDMA|Pulse|MCAN0 Receive Filter Event 1<br>DMA Request|
||MCAN0_FE_INTR_2|EDMA_XBAR_149|EDMA|Pulse|MCAN0 Receive Filter Event 2<br>DMA Request|
||MCAN0_FE_INTR_3|EDMA_XBAR_150|EDMA|Pulse|MCAN0 Receive Filter Event 3<br>DMA Request|
||MCAN0_FE_INTR_4|EDMA_XBAR_151|EDMA|Pulse|MCAN0 Receive Filter Event 4<br>DMA Request|
||MCAN0_FE_INTR_5|EDMA_XBAR_152|EDMA|Pulse|MCAN0 Receive Filter Event 5<br>DMA Request|
||MCAN0_FE_INTR_6|EDMA_XBAR_153|EDMA|Pulse|MCAN0 Receive Filter Event 6<br>DMA Request|
||MCAN0_TXDMA_0|EDMA_XBAR_74|EDMA|Pulse|MCAN0 Transmit Core DMA<br>Request 0|
||MCAN0_TXDMA_1|EDMA_XBAR_75|EDMA|Pulse|MCAN0 Transmit Core DMA<br>Request 1|
||MCAN0_TXDMA_2|EDMA_XBAR_76|EDMA|Pulse|MCAN0 Transmit Core DMA<br>Request 2|
||MCAN0_TXDMA_3|EDMA_XBAR_77|EDMA|Pulse|MCAN0 Transmit Core DMA<br>Request 3|



1500 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-208.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN1|MCAN1_FE_INTR_0|EDMA_XBAR_154|EDMA|Pulse|MCAN1 Receive Filter Event 0<br>DMA Request|
||MCAN1_FE_INTR_1|EDMA_XBAR_155|EDMA|Pulse|MCAN1 Receive Filter Event 1<br>DMA Request|
||MCAN1_FE_INTR_2|EDMA_XBAR_156|EDMA|Pulse|MCAN1 Receive Filter Event 2<br>DMA Request|
||MCAN1_FE_INTR_3|EDMA_XBAR_157|EDMA|Pulse|MCAN1 Receive Filter Event 3<br>DMA Request|
||MCAN1_FE_INTR_4|EDMA_XBAR_158|EDMA|Pulse|MCAN1 Receive Filter Event 4<br>DMA Request|
||MCAN1_FE_INTR_5|EDMA_XBAR_159|EDMA|Pulse|MCAN1 Receive Filter Event 5<br>DMA Request|
||MCAN1_FE_INTR_6|EDMA_XBAR_160|EDMA|Pulse|MCAN1 Receive Filter Event 6<br>DMA Request|
||MCAN1_TXDMA_0|EDMA_XBAR_78|EDMA|Pulse|MCAN1 Transmit Core DMA<br>Request 0|
||MCAN1_TXDMA_1|EDMA_XBAR_79|EDMA|Pulse|MCAN1 Transmit Core DMA<br>Request 1|
||MCAN1_TXDMA_2|EDMA_XBAR_80|EDMA|Pulse|MCAN1 Transmit Core DMA<br>Request 2|
||MCAN1_TXDMA_3|EDMA_XBAR_81|EDMA|Pulse|MCAN1 Transmit Core DMA<br>Request 3|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1501 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-208.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN2|MCAN2_FE_INTR_0|EDMA_XBAR_161|EDMA|Pulse|MCAN2 Receive Filter Event 0<br>DMA Request|
||MCAN2_FE_INTR_1|EDMA_XBAR_162|EDMA|Pulse|MCAN2 Receive Filter Event 1<br>DMA Request|
||MCAN2_FE_INTR_2|EDMA_XBAR_163|EDMA|Pulse|MCAN2 Receive Filter Event 2<br>DMA Request|
||MCAN2_FE_INTR_3|EDMA_XBAR_164|EDMA|Pulse|MCAN2 Receive Filter Event 3<br>DMA Request|
||MCAN2_FE_INTR_4|EDMA_XBAR_165|EDMA|Pulse|MCAN2 Receive Core Filter Event<br>4 DMA Request|
||MCAN2_FE_INTR_5|EDMA_XBAR_166|EDMA|Pulse|MCAN2 Receive Filter Event 5<br>DMA Request|
||MCAN2_FE_INTR_6|EDMA_XBAR_167|EDMA|Pulse|MCAN2 Receiver Filter Event 6<br>DMA Request|
||MCAN2_TXDMA_0|EDMA_XBAR_82|EDMA|Pulse|MCAN2 Transmit Core DMA<br>Request 0|
||MCAN2_TXDMA_1|EDMA_XBAR_83|EDMA|Pulse|MCAN2 Transmit Core DMA<br>Request 1|
||MCAN2_TXDMA_2|EDMA_XBAR_84|EDMA|Pulse|MCAN2 Transmit Core DMA<br>Request 2|
||MCAN2_TXDMA_3|EDMA_XBAR_85|EDMA|Pulse|MCAN2 Transmit Core DMA<br>Request 3|



1502 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-208.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN3|MCAN3_FE_INTR_0|EDMA_XBAR_168|EDMA|Pulse|MCAN3 Receive Filter Event 0<br>DMA Request|
||MCAN3_FE_INTR_1|EDMA_XBAR_169|EDMA|Pulse|MCAN3 Receive Filter Event 1<br>DMA Request|
||MCAN3_FE_INTR_2|EDMA_XBAR_170|EDMA|Pulse|MCAN3 Receive Filter Event 2<br>DMA Request|
||MCAN3_FE_INTR_3|EDMA_XBAR_171|EDMA|Pulse|MCAN3 Receive Filter Event 3<br>DMA Request|
||MCAN3_FE_INTR_4|EDMA_XBAR_172|EDMA|Pulse|MCAN3 Receive Filter Event 4<br>DMA Request|
||MCAN3_FE_INTR_5|EDMA_XBAR_173|EDMA|Pulse|MCAN3 Receive Filter Event 5<br>DMA Request|
||MCAN3_FE_INTR_6|EDMA_XBAR_174|EDMA|Pulse|MCAN3 Receive Filter Event 6<br>DMA Request|
||MCAN3_TXDMA_0|EDMA_XBAR_86|EDMA|Pulse|MCAN3 Transmit Core DMA<br>Request 0|
||MCAN3_TXDMA_1|EDMA_XBAR_87|EDMA|Pulse|MCAN3 Transmit Core DMA<br>Request 1|
||MCAN3_TXDMA_2|EDMA_XBAR_88|EDMA|Pulse|MCAN3 Transmit Core DMA<br>Request 2|
||MCAN3_TXDMA_3|EDMA_XBAR_89|EDMA|Pulse|MCAN3 Transmit Core DMA<br>Request 3|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1503 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-208.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN4|MCAN4_FE_INTR_0|EDMA_XBAR_192|EDMA|Pulse|MCAN4 Receive Filter Event 0<br>DMA Request|
||MCAN4_FE_INTR_1|EDMA_XBAR_193|EDMA|Pulse|MCAN4 Receive Filter Event 1<br>DMA Request|
||MCAN4_FE_INTR_2|EDMA_XBAR_194|EDMA|Pulse|MCAN4 Receive Filter Event 2<br>DMA Request|
||MCAN4_FE_INTR_3|EDMA_XBAR_195|EDMA|Pulse|MCAN4 Receive Filter Event 3<br>DMA Request|
||MCAN4_FE_INTR_4|EDMA_XBAR_196|EDMA|Pulse|MCAN4 Receive Filter Event 4<br>DMA Request|
||MCAN4_FE_INTR_5|EDMA_XBAR_197|EDMA|Pulse|MCAN4 Receive Filter Event 5<br>DMA Request|
||MCAN4_FE_INTR_6|EDMA_XBAR_198|EDMA|Pulse|MCAN4 Receive Filter Event 6<br>DMA Request|
||MCAN4_TXDMA_0|EDMA_XBAR_176|EDMA|Pulse|MCAN4 Transmit Core DMA<br>Request 0|
||MCAN4_TXDMA_1|EDMA_XBAR_177|EDMA|Pulse|MCAN4 Transmit Core DMA<br>Request 1|
||MCAN4_TXDMA_2|EDMA_XBAR_178|EDMA|Pulse|MCAN4 Transmit Core DMA<br>Request 2|
||MCAN4_TXDMA_3|EDMA_XBAR_179|EDMA|Pulse|MCAN4 Transmit Core DMA<br>Request 3|



1504 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-208.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN5|MCAN5_FE_INTR_0|EDMA_XBAR_199|EDMA|Pulse|MCAN5 Receive Filter Event 0<br>DMA Request|
||MCAN5_FE_INTR_1|EDMA_XBAR_200|EDMA|Pulse|MCAN5 Receive Filter Event 1<br>DMA Request|
||MCAN5_FE_INTR_2|EDMA_XBAR_201|EDMA|Pulse|MCAN5 Receive Filter Event 2<br>DMA Request|
||MCAN5_FE_INTR_3|EDMA_XBAR_202|EDMA|Pulse|MCAN5 Receive Filter Event 3<br>DMA Request|
||MCAN5_FE_INTR_4|EDMA_XBAR_203|EDMA|Pulse|MCAN5 Receive Filter Event 4<br>DMA Request|
||MCAN5_FE_INTR_5|EDMA_XBAR_204|EDMA|Pulse|MCAN5 Receive Filter Event 5<br>DMA Request|
||MCAN5_FE_INTR_6|EDMA_XBAR_205|EDMA|Pulse|MCAN5 Receive Filter Event 6<br>DMA Request|
||MCAN5_TXDMA_0|EDMA_XBAR_180|EDMA|Pulse|MCAN5 Transmit Core DMA<br>Request 0|
||MCAN5_TXDMA_1|EDMA_XBAR_181|EDMA|Pulse|MCAN5 Transmit Core DMA<br>Request 1|
||MCAN5_TXDMA_2|EDMA_XBAR_182|EDMA|Pulse|MCAN5 Transmit Core DMA<br>Request 2|
||MCAN5_TXDMA_3|EDMA_XBAR_183|EDMA|Pulse|MCAN5 Transmit Core DMA<br>Request 3|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1505 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-208.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN6|MCAN6_FE_INTR_0|EDMA_XBAR_206|EDMA|Pulse|MCAN6 Receive Filter Event 0<br>DMA Request|
||MCAN6_FE_INTR_1|EDMA_XBAR_207|EDMA|Pulse|MCAN6 Receive Filter Event 1<br>DMA Request|
||MCAN6_FE_INTR_2|EDMA_XBAR_208|EDMA|Pulse|MCAN6 Receive Filter Event 2<br>DMA Request|
||MCAN6_FE_INTR_3|EDMA_XBAR_209|EDMA|Pulse|MCAN6 Receive Filter Event 3<br>DMA Request|
||MCAN6_FE_INTR_4|EDMA_XBAR_210|EDMA|Pulse|MCAN6 Receive Filter Event 4<br>DMA Request|
||MCAN6_FE_INTR_5|EDMA_XBAR_211|EDMA|Pulse|MCAN6 Receive Filter Event 5<br>DMA Request|
||MCAN6_FE_INTR_6|EDMA_XBAR_212|EDMA|Pulse|MCAN6 Receive Filter Event 6<br>DMA Request|
||MCAN6_TXDMA_0|EDMA_XBAR_184|EDMA|Pulse|MCAN6 Transmit Core DMA<br>Request 0|
||MCAN6_TXDMA_1|EDMA_XBAR_185|EDMA|Pulse|MCAN6 Transmit Core DMA<br>Request 1|
||MCAN6_TXDMA_2|EDMA_XBAR_186|EDMA|Pulse|MCAN6 Transmit Core DMA<br>Request 2|
||MCAN6_TXDMA_3|EDMA_XBAR_187|EDMA|Pulse|MCAN6 Transmit Core DMA<br>Request 3|



1506 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-208.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN7|MCAN7_FE_INTR_0|EDMA_XBAR_213|EDMA|Pulse|MCAN7 Receive Filter Event 0<br>DMA Request|
||MCAN7_FE_INTR_1|EDMA_XBAR_214|EDMA|Pulse|MCAN7 Receive Filter Event 1<br>DMA Request|
||MCAN7_FE_INTR_2|EDMA_XBAR_215|EDMA|Pulse|MCAN7 Receive Filter Event 2<br>DMA Request|
||MCAN7_FE_INTR_3|EDMA_XBAR_216|EDMA|Pulse|MCAN7 Receive Filter Event 3<br>DMA Request|
||MCAN7_FE_INTR_4|EDMA_XBAR_217|EDMA|Pulse|MCAN7 Receive Filter Event 4<br>DMA Request|
||MCAN7_FE_INTR_5|EDMA_XBAR_218|EDMA|Pulse|MCAN7 Receive Filter Event 5<br>DMA Request|
||MCAN7_FE_INTR_6|EDMA_XBAR_219|EDMA|Pulse|MCAN7 Receive Filter Event 6<br>DMA Request|
||MCAN7_TXDMA_0|EDMA_XBAR_188|EDMA|Pulse|MCAN7 Transmit Core DMA<br>Request 0|
||MCAN7_TXDMA_1|EDMA_XBAR_189|EDMA|Pulse|MCAN7 Transmit Core DMA<br>Request 1|
||MCAN7_TXDMA_2|EDMA_XBAR_190|EDMA|Pulse|MCAN7 Transmit Core DMA<br>Request 2|
||MCAN7_TXDMA_3|EDMA_XBAR_191|EDMA|Pulse|MCAN7 Transmit Core DMA<br>Request 3|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1507 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.4.1.4 MCAN Functional Description** 

The MCAN module performs CAN protocol communication according to ISO 11898-1:2015. The bit rate can be programmed to values greater than 1 Mbps. Additional transceiver hardware is required for the connection to the physical layer (CAN bus). 

For communication on a CAN network, individual message frames can be configured. The message frames and identifier masks are stored in the Message RAM. 

All functions concerning the handling of messages are implemented in the Message Handler. 

The register set of the MCAN module can be accessed directly via the module interface. These registers are used to control and configure the CAN core and the Message Handler, and to access the Message RAM. 

Figure 13-166 shows the MCAN module block diagram. 

**==> picture [500 x 266] intentionally omitted <==**

**----- Start of picture text -----**<br>
MCAN Subsystem<br>DMA<br>Extension interface<br>Events<br>ICLK<br>RX<br>FCLK<br>CAN Core<br>Clock Stop TX<br>Request /<br>Acknowledge<br>Message Handler<br>RST<br>Rx Handler Tx Handler<br>Message<br>Interrupt RAM<br>Requests Interface<br>Registers and Message<br>Message Object Access RAM<br>Interconnect Module Interface<br>**----- End of picture text -----**<br>


**==> picture [21 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
mcan-004<br>**----- End of picture text -----**<br>


**Figure 13-166. MCAN Block Diagram** 

The MCAN module blocks description: 

- **CAN Core** : the CAN core consists of the CAN protocol controller and the Rx/Tx shift register. It handles all ISO 11898-1:2015 protocol functions and supports 11-bit and 29-bit identifiers. 

- **Message Handler** : the Message Handler (Rx Handler and Tx Handler) is a state machine that controls the data transfer between the single-ported Message RAM and the CAN core's Rx/Tx shift register. It also handles the acceptance filtering and the Interrupt/DMA request generation as programmed in the control registers. 

- **Message RAM** : the main purpose of the Message RAM is to store Rx/Tx messages, Tx Event elements, and Message ID Filter elements (for more information, see Section 13.4.1.4.10, _Message RAM_ ). 

- **Message RAM Interface** : enables connection between the Message RAM and the other blocks in the MCAN module. 

- **Registers and Message Object Access** : data consistency is ensured by indirect accesses to the message objects. The interface registers have the same word-length as the Message RAM. 

1508 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- **Module Interface** : provides connection to the Registers and Message Object Access block and Message RAM Interface block 

- **Clocking** : two clocks are provided to the MCAN module: the peripheral synchronous clock (interface clock ICLK) and the peripheral asynchronous clock (functional clock - FCLK). 

- **Extension Interface** : this interface is used for DMA requests signaling (see Section 13.4.1.4.2.2). 

## _**13.4.1.4.1 Module Clocking Requirements**_ 

Two clocks are provided to the MCAN module: 

- the peripheral synchronous clock (ICLK) as the general module clock source 

- and the peripheral asynchronous clock (FCLK) provided to the CAN core for generating the CAN bit timing. 

Within the MCAN module there is a synchronization mechanism implemented to ensure safe data transfer between the two clock domains. There is synchronization between the signals from the Host clock domain to the CAN clock domain and vice versa and between the reset signal to the Host clock domain and to the CAN clock domain. 

## **Note** 

ICLK must always be higher or equal to FCLK, in order to achieve a stable functionality of the MCAN module. Here, also the frequency shift of the modulated ICLK has to be considered: 

## _f_ 0,ICLK ± Δ _f_ FM,ICLK ≥ _f_ FCLK 

For more information on how to configure the relevant clock source registers, see Section 6.4, _Clocking_ and the device-specific Data sheet. 

## _**13.4.1.4.2 Interrupt and DMA Requests**_ 

The MCAN module provides interrupt and DMA requests. They are configured via the Host CPU. The Suspend Mode is requesting or forcing (based on MCANSS_CTRL[3] DBGSUSP_FREE bit) the MCAN module to go into initialization mode (see MCAN_CCCR[0] INIT bit) in which new interrupts and DMA requests will not be issued, that is to prevents the interrupt and DMA requests from propagating to the Host CPU (for more information, see Section 13.4.1.4.3.8.2, _Suspend Mode_ ). 

## _**13.4.1.4.2.1 Interrupt Requests**_ 

The MCAN module has two interrupt lines. There are 30 internal interrupt sources. Each source can be configured to drive one of the two interrupt lines. The interrupts are 'level high' interrupts. 

The MCAN core provides two interrupt requests (for Line 0 and Line 1). 

For more information, see the following registers: 

- Interrupt Register (MCAN_IR) 

- Interrupt Enable (MCAN_IE) 

- Interrupt Line Select (MCAN_ILS) 

- Interrupt Line Enable (MCAN_ILE) 

The MCAN module is capable of issuing ECC interrupts. After clearing the ECC interrupt source, the application software must also write 1 to EOI register (MCANSS_ECC_SEC_EOI_REG/MCANSS_ECC_DED_EOI_REG). For more information, see _ECC Aggregator_ . 

The MCAN module supports External Timestamp Counter. When the External Timestamp Counter rolls over it produces an interrupt (see _External Timestamp Counter_ ). 

For more information, see the following registers: 

- Interrupt Clear Shadow Register (MCANSS_ICS) 

- Interrupt Raw Status Register (MCANSS_IRS) 

- Interrupt Enable Clear Shadow Register (MCANSS_IECS) 

- Interrupt Enable Register (MCANSS_IE) 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1509 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- Interrupt Enable Status Register (MCANSS_IES) 

- End Of Interrupt Register (MCANSS_EOI) 

- External Timestamp Prescaler Register (MCANSS_EXT_TS_PRESCALER) 

- External Timestamp Unserviced Interrupts Counter Register (MCANSS_EXT_TS_UNSERVICED_INTR_CNTR) 

## _**13.4.1.4.2.2 DMA Requests**_ 

Functional transmit and Filter DMA requests are generated by the MCAN module based on the signaling in the Extension Interface. The DMA signaling uses a simple DMA request active high pulse. 

The active high pulse indicates a pending message is transmitted (see MCAN_TXBRP). This pulse can be used to transfer another message to the Tx Buffer, which would need to be followed by writing 1 to the corresponding MCAN_TXBAR[0] AR bit to mark a new Tx message pending transmission. 

The Parity on Tx DMA Events is available using an EDC Controller which can be accessed through the ECC Aggregator. 

Standard and Extended message filters can be set to issue a pulse when a filter match occurs. These 'Filter Events' can be used to DMA messages from the Rx FIFO. The events are high level single clock cycle pulses (ICLK). 

## _**13.4.1.4.3 Operating Modes**_ 

## _**13.4.1.4.3.1 Software Initialization**_ 

Setting the MCAN_CCCR[0] INIT bit to 1 starts a software initialization. This is done either by software or by a hardware reset, when an uncorrected bit error was detected in the Message RAM, or by going Bus_Off state. While the MCAN_CCCR[0] INIT bit is set, the message transfer is stopped and the status of the output TX pin is recessive (high). The counters of the Error Management Logic (EML) are unchanged. Setting the MCAN_CCCR[0] INIT bit does not change any configuration register. Resetting the MCAN_CCCR[0] INIT bit finishes the software initialization. After waiting for the occurrence of a sequence of 11 consecutive recessive bits (indication for Bus_Idle state) the message transfer starts. 

Access to the MCAN configuration registers is only enabled when both MCAN_CCCR[0] INIT and MCAN_CCCR[1] CCE bits are set (write protection). 

The MCAN_CCCR[1] CCE bit can only be set/reset while the MCAN_CCCR[0] INIT = 1. The MCAN_CCCR[1] CCE bit is automatically reset when the MCAN_CCCR[0] INIT bit is reset. 

The following registers are reset when the MCAN_CCCR[1] CCE bit is set: 

- MCAN_HPMS - High Priority Message Status 

- MCAN_RXF0S - Rx FIFO 0 Status 

- MCAN_RXF1S - Rx FIFO 1 Status 

- MCAN_TXFQS - Tx FIFO/Queue Status 

- MCAN_TXBRP - Tx Buffer Request Pending 

- MCAN_TXBTO - Tx Buffer Transmission Occurred 

- MCAN_TXBCF - Tx Buffer Cancellation Finished 

- MCAN_TXEFS - Tx Event FIFO Status 

The Timeout Counter value MCAN_TOCV[15-0] TOC field is preset to the value configured by the MCAN_TOCC[31-16] TOP field when the MCAN_CCCR[1] CCE bit is set. 

In addition the Tx Handler and Rx Handler are held in idle state while MCAN_CCCR[1] CCE = 1. 

The following registers are only writeable while MCAN_CCCR[1] CCE = 0 

- MCAN_TXBAR - Tx Buffer Add Request 

- MCAN_TXBCR - Tx Buffer Cancellation Request 

1510 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

MCAN_CCCR[7] TEST and MCAN_CCCR[5] MON bits can only be set by the Host CPU while MCAN_CCCR[0] INIT = 1 and MCAN_CCCR[1] CCE = 1. Both bits may be reset at any time. The MCAN_CCCR[6] DAR bit can only be set/reset while MCAN_CCCR[0] INIT = 1 and MCAN_CCCR[1] CCE = 1. 

Table 13-209 shows the steps to configure the MCAN module. 

**Table 13-209. Steps to Configure MCAN Module** 

|**Step**<br>**Operation**<br>**Description**<br>**Pseudo Code**|**Step**<br>**Operation**<br>**Description**<br>**Pseudo Code**|**Step**<br>**Operation**<br>**Description**<br>**Pseudo Code**|**Step**<br>**Operation**<br>**Description**<br>**Pseudo Code**|
|---|---|---|---|
|1|Initialize MCAN_CCCR|Set MCAN_CCCR[0] INIT bit<br>and check that it has been set|INIT = 1;<br>If INIT ≠ 1, wait until it is|
|2|Unlock protected registers|Set MCAN_CCCR[1] CCE bit|CCE = 1;|
|3|Configure CAN mode|Set MCAN_CCCR[8] FDOE bit to CAN FD|FDOE = 1 for CAN FD<br>FDOE = 0 for CAN|
|4|Configure Bit Rate Switching|Set MCAN_CCCR[9] BRSE bit|BRSE = 1 with bit rate<br>switching<br>BRSE = 0 without bit rate<br>switching|
|5|Set bit timing|Set MCAN_NBTP register||
|6|Lock protected registers|Clear MCAN_CCCR[1] CCE bit|CCE = 0;|
|7|Return MCAN module to normal<br>operation|Clear MCAN_CCCR[0] INIT bit<br>and check it has been cleared|INIT = 0;<br>If INIT ≠ 0, wait until it is|



## _**13.4.1.4.3.2 Normal Operation**_ 

Once the MCAN module is initialized and the MCAN_CCCR[0] INIT bit is reset to zero, the MCAN module synchronizes itself to the CAN bus and is ready for communication. After passing the acceptance filtering, received messages including Message Identifier (ID) and Data Length Code (DLC) are stored into a dedicated Rx Buffer or into Rx FIFO 0/Rx FIFO 1. 

For messages to be transmitted dedicated Tx Buffers and/or a Tx FIFO or a Tx Queue can be initialized or updated. 

## **Note** 

Automated transmission on reception of remote frames is not supported. 

## _**13.4.1.4.3.3 CAN FD Operation**_ 

The CAN FD standard allows extended frames to be sent, up to 64 data bytes in a single frame at a higher bit rate for the data phase of a frame, up to 8 Mbps. The CAN FD standard introduces the ability to switch from one bit rate to another. Extended Data Length (EDL), as shown in Figure 13-167, sets a data length of up to 8 or up to 64 data bytes. Bit Rate Switching (BRS) indicates whether two bit rates (the data phase is transmitted at a different bit rate to the arbitration phase) are enabled. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1511 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [489 x 144] intentionally omitted <==**

**----- Start of picture text -----**<br>
Arbitration Field Control Field Data Field CRC Field ACK EOF Int. Bus Idle<br>S I E B E<br>O 11 bit Identifier r D D r R S 4 bit 0 - 64 bytes 21* bit 1 1 1 7 3<br>F 1 E L 0 S I DLC CRC<br>CAN FD CAN FD CAN FD<br>Arbitration Data Arbitration<br>* 17 bit CRC for data fields with up to 16 bytes<br>mcan-004a<br>**----- End of picture text -----**<br>


**Figure 13-167. CAN FD Frame** 

## **Note** 

Figure 13-167 presents CAN FD frame according to the Non-ISO CAN FD (legacy) protocol. In the new ISO CAN FD protocol the CRC Field includes additional 5 bits (three stuff bit counter (SBC) bits and two parity bits). With these additional bits, a weakness identified in the error detection scheme chosen by the original protocol is removed. By setting MCAN_CCCR[15] NISO bit, the ISO or Non-ISO CAN FD format can be chosen. In CAN network ISO CAN FD and non-ISO CAN FD devices should never mix. 

There are two variants of CAN FD frame transmission: 

- CAN FD frame transmission without bit rate switching 

- CAN FD frame transmission where control field, data field, and CRC field are transmitted with a higher bit rate than the beginning and the end of the frame 

In the CAN frames FDF = recessive (logical 1) signifies a CAN FD frame, FDF = dominant (logical 0) signifies a Classic CAN frame. In a CAN FD frame, the two bits following FDF - res and BRS, decide whether the bit rate inside of this CAN FD frame is switched. A CAN FD bit rate switch is signified by res = dominant and BRS = recessive. Note that the coding of res = recessive is reserved for future expansion of the protocol. In case the MCAN module receives a frame with FDF = recessive and res = recessive, it will signal a Protocol Exception Event by setting the MCAN_PSR[14] EXE bit. When Protocol Exception Handling is enabled (MCAN_CCCR[12] PXHD = 0), this causes the operation state to change from Receiver (MCAN_PSR[4-3] ACT = 10) to Integrating (MCAN_PSR[4-3] ACT = 00) at the next sample point. In case Protocol Exception Handling is disabled (MCAN_CCCR[12] PXHD = 1), the MCAN will treat a recessive res bit as an form error and will respond with an error frame. 

CAN FD operation is enabled by programming the MCAN_CCCR[8] FDOE bit. In case MCAN_CCCR[8] FDOE = 1, transmission and reception of CAN FD frames is enabled. Transmission and reception of Classic CAN frames is always possible. Whether a CAN FD frame or a Classic CAN frame is transmitted can be configured via the FDF bit in the respective Tx Buffer element. 

With MCAN_CCCR[8] FDOE = 0, received frames are interpreted as Classic CAN frames, which leads to the transmission of an error frame when receiving a CAN FD frame. When CAN FD operation is disabled, no CAN FD frames are transmitted even if the FDF bit of a Tx Buffer element is set. The MCAN_CCCR[8] FDOE and MCAN_CCCR[9] BRSE bits can only be changed while the MCAN_CCCR[0] INIT and MCAN_CCCR[1] CCE bits are both set. With MCAN_CCCR[8] FDOE = 0, the setting of bits FDF and BRS is ignored and frames are transmitted in Classic CAN format. 

With MCAN_CCCR[8] FDOE = 1 and MCAN_CCCR[9] BRSE = 0, only FDF bit of a Tx Buffer element is evaluated. With MCAN_CCCR[8] FDOE = 1 and MCAN_CCCR[9] BRSE = 1, transmission of CAN FD frames with bit rate switching is enabled. All Tx Buffer elements with bits FDF and BRS set are transmitted in CAN FD format with bit rate switching. 

1512 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

A mode change during CAN operation is only recommended under the following conditions: 

- The failure rate in the CAN FD data phase is significant higher than in the CAN FD arbitration phase. In this case disable the CAN FD bit rate switching option for transmissions. 

- During system startup all nodes are transmitting Classic CAN messages until it is verified that they are able to communicate in CAN FD format. If this is true, all nodes switch to CAN FD operation. 

- Wakeup messages in CAN Partial Networking have to be transmitted in Classic CAN format. 

- End-of-line programming in case not all nodes are CAN FD capable. Non CAN FD nodes are held in Silent mode until programming has completed. Then all nodes switch back to Classic CAN communication. 

In the CAN FD format, the DLC coding differs from the standard CAN format (see Table 13-210). 

**Table 13-210. DLC Coding** 

|**DLC**|**0**|**1**|**2**|**3**|**4**|**5**|**6**|**7**|**8**|**9**|**10**|**11**|**12**|**13**|**14**|**15**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|Number of Data Bytes in Standard<br>CAN|0|1|2|3|4|5|6|7|8|8|8|8|8|8|8|8|
|Number of Data Bytes in CAN FD|0|1|2|3|4|5|6|7|8|12|16|20|24|32|48|64|



For CAN FD frames, the bit timing will be switched inside the frame after the BRS (Bit Rate Switch) bit in case this bit is recessive. In the CAN FD arbitration phase, before the BRS bit, the nominal CAN bit timing (see Figure 13-168) is used as configured by the Nominal Bit Timing and Prescaler Register MCAN_NBTP. In the following CAN FD data phase, the data phase bit timing is used as configured by the Data Bit Timing and Prescaler Register MCAN_DBTP. The bit timing is switched back from the data phase timing at the CRC delimiter or when an error is detected, whichever occurs first. 

**==> picture [255 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
Time Quanta<br>bit n-1 Sync_Seg Prop_Seg Phase_Seg1 Phase_Seg2 bit n+1<br>mcan-022<br>Nominal Bit Timing<br>**----- End of picture text -----**<br>


**Figure 13-168. CAN Bit Timing** 

The maximum configurable data phase bit timing depends on the CAN clock frequency (FCLK). Example: with FCLK = 20 MHz and the shortest configurable bit time of 4 tq (time quanta), the bit rate in the data phase is 5 Mbps. 

In both data frame formats, CAN FD and CAN FD with bit rate switching, the value of the ESI (Error Status Indicator) bit depends on transmitter's error state (see MCAN_PSR[11] RESI bit) monitored at the start of the transmission. If the transmitter has error passive flag the ESI bit is transmitted recessive, else it is transmitted dominant. 

The calculation of the parameters required for CAN bit timing configuration is dependent on a few fundamental equations. The bit rate (bits per second) calculation is based on the speed of the CAN clock, the bit rate pre-scalar value (BRP), and the time segments used to define the sampling point for the bit. The sampling point is the point of time at which the bus level is read and interpreted as the value at that respective time. The typical value of the sampling point is between 75-90%. Time segment 1 (TSEG1) is the time before the sampling point and is defined as the Prog_Seg time plus the Phase_Seg1 time per the CAN Bit Timing diagram. Time segment 2 (TSEG2) is the time after the sampling point which makes it equal to Phase_Seg2. When necessary, the Sync_Seg period of the nominal bit timing interval should be reflected in the equations by adding '1'. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1513 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [446 x 104] intentionally omitted <==**

## _**13.4.1.4.3.4 Transmitter Delay Compensation**_ 

## _**13.4.1.4.3.4.1 Description**_ 

When only one CAN FD node is transmitting and all others are receivers the length of the bus line has no impact. When transmitting via the TX pin the MCAN module receives the transmitted data from its local CAN transceiver via the RX pin. The received data is delayed. If the transmitter delay is greater than TSEG1 (time segment before sample point), a bit error is detected. 

The MCAN module provides a delay compensation mechanism to compensate the transmitter delay. The compensation mechanism enables transmission with higher bit rates during the CAN FD data phase independent of the delay of a specific CAN transceiver. Without transmitter delay compensation the bit rate in the data phase is limited by the transmitter delay. 

The mechanism enables configurations where the data bit time is shorter than the transmitter delay (it is described in detail in ISO 11898-1:2015). The transmitter delay compensation is enabled by setting the MCAN_DBTP[23] TDC bit to 1. 

The delayed transmit data is compared against the received data at the Secondary Sample Point (SSP) in order to check for bit errors during the data phase of transmitting nodes. If a bit error is detected, the transmitter will react on this bit error at the next following regular sample point. During arbitration phase the delay compensation is always disabled. 

The received bit is compared against the transmitted bit at the SSP. The SSP position is defined as the sum of the measured delay from the MCAN's transmit output TX pin through the transceiver to the receive input RX pin plus the transmitter delay compensation offset configured by the MCAN_TDCR[14-8] TDCO field (see Figure 13-169). The transmitter delay compensation offset is used to adjust the position of the SSP inside the received bit (example: half of the bit time in the data phase). The position of the SSP is rounded down to the next integer number of mtq. 

The actual transmitter delay compensation value can be checked by reading the MCAN_PSR[22-16] TDCV field. This field is cleared when the MCAN_CCCR[0] INIT bit is set and is updated at each transmission of CAN FD frame while the MCAN_DBTP[23] TDC bit is set. 

1514 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [432 x 201] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transmitter<br>Delay ESI<br>FDF res BRS DLC<br>TX arbitration phase data phase<br>RX arbitration phase data phase<br>start stop<br>Delay<br>FCLK Delay Counter<br>SSP Position<br>+<br>Delay Compensation Offset<br>MCAN_TDCR[14-8] TDCO<br>**----- End of picture text -----**<br>


mcan-005 

## **Figure 13-169. Transmitter Delay Measurement** 

## _**13.4.1.4.3.4.2 Transmitter Delay Compensation Measurement**_ 

When transmitter delay compensation is enabled (by programming MCAN_DBTP[23] TDC = 1), the measurement is started within each transmitted CAN FD frame at the falling edge of FDF bit to bit res. The measurement is stopped when this edge is seen at the receive input RX pin of the transmitter. The resolution of this measurement is one mtq (see Figure 13-169). The mtq (minimum time quantum) dimension is equal to the CAN clock period (FCLK). 

The use of a transmitter delay compensation filter window can be enabled by programming MCAN_TDCR[6-0] TDCF field. This filter feature defines a minimum value for the SSP position to avoid the case in which a dominant glitch inside the received FDF bit ends the delay compensation measurement before the falling edge of the received res bit, resulting in an early taken SSP position. Dominant edges on the RX pin, that would result in an earlier SSP position are ignored for transmitter delay measurement. The measurement is stopped when the SSP position is at least MCAN_TDCR[6-0] TDCF field and the RX pin is low. 

The following boundary conditions have to be considered: 

- The sum of the measured delay from the TX pin to the RX pin and the configured transmitter delay compensation offset (MCAN_TDCR[14-8] TDCO field) has to be less than 6 bit times in the data phase. 

- The sum of the measured delay from the TX pin to the RX pin and the configured transmitter delay compensation offset (MCAN_TDCR[14-8] TDCO) field has to be less or equal 127 mtq. In case this sum exceeds 127 mtq, the maximum value of 127 mtq is used for transmitter delay compensation. 

- The data phase ends at the sample point of the CRC delimiter, that stops checking of receive bits at the SSPs. 

## _**13.4.1.4.3.5 Restricted Operation Mode**_ 

In Restricted Operation Mode the CAN node is able to receive data and remote frames and acknowledge valid frames, but it does not send data frames, remote frames, active error frames, or overload frames. In case of an error condition or overload condition, it does not send dominant bits, instead it waits for the occurrence of bus idle condition to resynchronize itself to the CAN communication. The receive and transmit error counters (MCAN_ECR[14-8] REC and MCAN_ECR[7-0] TEC) are frozen, while CAN error logging (MCAN_ECR[23-16] CEL) is active. The Host CPU can set the MCAN module into Restricted Operation Mode by setting MCAN_CCCR[2] ASM bit. The bit can only be set by the Host CPU at any time when both MCAN_CCCR[2] CCE and MCAN_CCCR[0] INIT bits are set to 1. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1515 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

The Restricted Operation Mode is automatically entered when the Tx Handler does not read data from the Message RAM in time. To leave Restricted Operation Mode, the Host CPU has to reset MCAN_CCCR[2] ASM bit. This mode can be used in applications that adapt themselves to different CAN bit rates. In this case the application tests different bit rates and leaves the Restricted Operation Mode after it has received a valid frame. 

## **Note** 

Restricted Operation Mode must not be combined with Internal Loopback Mode. 

## _**13.4.1.4.3.6 Bus Monitoring Mode**_ 

Entering Bus Monitoring Mode is done by setting the MCAN_CCCR[5] MON bit to 1. In this mode (see ISO 11898-1:2015, _Bus Monitoring_ section), the MCAN module is able to receive valid data and remote frames, but cannot start a transmission. The MCAN module sends only recessive bits on the CAN bus. If the MCAN module is required to send a dominant bit (ACK bit, overload flag, active error flag), the bit is rerouted internally so that the MCAN module monitors this dominant bit, although the CAN bus may remain in recessive state. In Bus Monitoring Mode the MCAN_TXBRP register is held in reset state. The Bus Monitoring Mode can be used to analyze the traffic on a CAN bus without affecting it by the transmission of dominant bits. Figure 13-170 shows the connection of the TX and RX signals to the MCAN module in Bus Monitoring Mode. 

**==> picture [228 x 157] intentionally omitted <==**

**----- Start of picture text -----**<br>
TX RX<br>MCAN<br>=1<br>• •<br>Tx Rx<br>CAN Core<br>**----- End of picture text -----**<br>


**==> picture [23 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
mcan-006<br>**----- End of picture text -----**<br>


**Figure 13-170. Connection of Signals in Bus Monitoring Mode** 

## _**13.4.1.4.3.7 Disabled Automatic Retransmission (DAR) Mode**_ 

According to the CAN Specification (see ISO11898-1:2015, _Recovery Management_ section), the MCAN module provides means for automatic retransmission of frames that have lost arbitration or that have been disturbed by errors during transmission. By default automatic retransmission is enabled (see the MCAN_CCCR[6] DAR bit). 

## _**13.4.1.4.3.7.1 Frame Transmission in DAR Mode**_ 

In DAR mode all transmissions are automatically cancelled after they started on the CAN bus. A Tx Buffer's Tx Request Pending MCAN_TXBRP[xx] TRPx bit is reset after successful transmission, when a transmission has not yet been started at the point of cancellation, has been aborted due to lost arbitration, or when an error occurred during frame transmission. 

Successful transmission: 

- Corresponding Tx Buffer Transmission Occurred MCAN_TXBTO[xx] TOx bit is set 

- Corresponding Tx Buffer Cancellation Finished MCAN_TXBCF[xx] CFx bit is not set 

Successful transmission in spite of cancellation: 

- Corresponding Tx Buffer Transmission Occurred MCAN_TXBTO[xx] TOx bit is set 

- Corresponding Tx Buffer Cancellation Finished MCAN_TXBCF[xx] CFx bit is set 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1516 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

Arbitration lost or frame transmission disturbed: 

- Corresponding Tx Buffer Transmission Occurred MCAN_TXBTO[xx] TOx bit is not set 

- Corresponding Tx Buffer Cancellation Finished MCAN_TXBCF[xx] CFx bit is set 

In case of a successful frame transmission, and if storage of Tx events is enabled, a Tx Event FIFO element is written with Event Type ET = 10 (transmission in spite of cancellation). 

## _**13.4.1.4.3.8 Power Down (Sleep Mode)**_ 

## **Note** 

The MCAN IP supports Power Down (Sleep Mode), however, this feature is not supported at the system level. 

The entering in Power Down mode is controlled via two sources: 

- PSC (via clock stop request signal) 

- Software (by writing to the MCAN_CCCR[4] CSR bit) 

As long as the clock stop request signal is active, the MCAN_CCCR[4] CSR bit is read as 1. 

When all pending transmission requests have completed, the MCAN module waits until bus idle state is detected. Then the MCAN module sets the MCAN_CCCR[0] INIT bit to 1 to prevent any further CAN transfers. 

The MCAN module acknowledges that it is ready for power down: 

- By asserting clock stop acknowledge signal to the PSC (in case of PSC source). 

- By setting the MCAN_CCCR[3] CSA flag bit to 1 (in case of Software source). 

In this state, before the clocks are switched off, further register accesses can be made. Now the module clock inputs ICLK and FCLK may be switched off. 

To leave power down mode, the application has to turn on the module clocks before resetting the input clock stop request signal respectively the MCAN_CCCR[4] CSR flag bit. The MCAN will acknowledge this by resetting the output clock stop acknowledge signal respectively the MCAN_CCCR[3] CSA flag bit. Afterwards, the application can restart CAN communication by resetting the MCAN_CCCR[0] INIT bit. 

Restoring the clocks from clock stop mode, needs to be done according to how the clock stop was initiated: 

- If Software asserts the MCAN_CCCR[3] CSA flag bit, once the MCAN module goes idle, the MCAN_CCCR[0] INIT bit is set. To get it started again, Software needs to write 0 to the MCAN_CCCR[0] INIT bit. 

- If PSC is issuing a clock stop request, than there are two options for waking up: 

   - After removing clock stop request signal, Software would need to write 0 to the MCAN_CCCR[0] INIT bit, or 

   - If the MCANSS_CTRL[5] AUTOWAKEUP bit is set, than after removing clock stop request signal, an FSM inside the MCAN module will reset the MCAN_CCCR[0] INIT bit (without Software). 

## _**13.4.1.4.3.8.1 External Clock Stop Mode**_ 

The MCAN module supports two external clock stop modes: 

- Immediate 

- Graceful 

In a graceful clock stop mode, when the clock stop request is asserted, the MCAN core will respond with clock stop acknowledge when all pending Tx messages have been processed and an Idle line had been detected. The MCAN_CCCR[0] INIT bit will be set, the MCAN core will go and stay Idle. 

The automatic wakeup feature is enabled by setting the MCANSS_CTRL[5] AUTOWAKEUP and MCANSS_CTRL[4] WAKEUPREQEN bits to 1 (for more information, see Section 13.4.1.4.3.8.3, _Wakeup request_ ). When external clock stop request is removed and no suspend request is active, a read-modify-write to the MCAN_CCCR[0] INIT bit is performed to clear it. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1517 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.1.4.3.8.2 Suspend Mode**_ 

The MCAN module supports two suspend modes: 

- Immediate 

- Graceful 

In a graceful suspend mode (see the MCANSS_CTRL[3] DBGSUSP_FREE bit), when the suspend request is asserted, a clock stop request to the MCAN core is performed. The MCAN core will respond with clock stop acknowledge when all pending Tx messages have been processed and an Idle line had been detected. At that point the MCAN_CCCR[0] INIT bit will be set, the MCAN core will go and stay Idle. The suspend state can be verified by reading MCAN_CCCR[0] INIT bit. 

The automatic wakeup feature is enabled by setting the MCANSS_CTRL[5] AUTOWAKEUP and MCANSS_CTRL[4] WAKEUPREQEN bits to 1 (for more information, see Section 13.4.1.4.3.8.3, _Wakeup request_ ). When suspend request is removed, if no external clock stop request is active, a read-modify-write to the MCAN_CCCR[0] INIT bit is performed to clear it. 

During suspend mode the auto-clear feature is disabled. The following register fields have an auto-clear feature: 

- MCAN_ECR[23-16] CEL 

- MCAN_PSR[2-0] LEC 

- MCAN_PSR[10-8] DLEC 

- MCAN_PSR[11] RESI 

- MCAN_PSR[12] RBRS 

- MCAN_PSR[13] RFDF 

- MCAN_PSR[14] PXE 

## _**13.4.1.4.3.8.3 Wakeup request**_ 

Issuing a clock stop request puts the MCAN module into Power Down mode (Sleep Mode). During transition from IDLE to ACTIVE, if the MCANSS_CTRL[5] AUTOWAKEUP and MCANSS_CTRL[4] WAKEUPREQEN bits are enabled, after the MCAN Core respond to the removal of the clock stop request with removing the clock stop acknowledge, a read-modify-write will be issued to clear the MCAN_CCCR[0] INIT bit and the MCAN core will resume operation. It takes a few FCLK clock cycles for before the write to clear function effects the MCAN_CCCR[0] INIT bit. During clock stop the FCLK clock is turned off and is re-enabled when clock stop request is removed. It takes a few FCLK clock cycles for the FCLK clock to be re-enabled followed by a few more for the synchronization of the MCAN_CCCR[0] INIT bit to take effect. After completion of these steps the MCAN core resumes fully active operation. 

If the MCANSS_CTRL[4] WAKEUPREQEN bit is set, the MCAN module provides a wakeup request on the following wakeup event: 

- The receive RX pin is dominant (logical 0) 

The wakeup request is de-asserted when any of the following conditions occur: 

- Clock stop request is removed and clock stop acknowledge is de-asserted 

- A reset is applied to the MCAN module 

## _**13.4.1.4.3.9 Test Modes**_ 

The MCAN_TEST register write access is enabled by setting the test mode enable MCAN_CCCR[7] TEST bit to 1. The MCAN_TEST register allows the configuration of the test modes and test functions. 

The CAN transmit TX pin has four output functions. One of those functions can be selected by programming the MCAN_TEST[6-5] TX field. Additionally to its default function (the serial data output) it can drive the CAN Sample Point signal to monitor the MCAN's bit timing and it can drive constant dominant or recessive values. 

The actual value of the CAN receive RX pin can be monitored from MCAN_TEST[7] RX bit. Both functions can be used to check the CAN bus physical layer. Due to the synchronization mechanism between CAN clock (FCLK) and Host clock (ICLK) domain, there may be a delay of several Host clock periods between writing to 

1518 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

the MCAN_TEST[6-5] TX field until the new configuration is visible at the output TX pin. This applies also when reading input RX pin via the MCAN_TEST[7] RX bit. 

## **Note** 

Test modes should be used for self test only. The software control for TX pin interferes with all CAN protocol functions. It is not recommended to use test modes for application. 

## _**13.4.1.4.3.9.1 Internal Loopback Mode**_ 

The MCAN module can be set into Internal Loopback Mode by programming MCAN_TEST[4] LBCK and MCAN_CCCR[5] MON bits to 1. The Internal Loopback Mode is used for a 'Hot Selftest'. The 'Hot Selftest' allows the MCAN module to be tested without affecting a running CAN system connected to the TX and RX pins. In this mode RX pin is disconnected from the MCAN module and TX pin is held recessive. Figure 13-171 shows the connection of the TX and RX pins to the MCAN module in case of Internal Loopback Mode. 

**==> picture [229 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
TX RX<br>MCAN<br>=1<br>• •<br>Tx Rx<br>CAN Core<br>mcan-008<br>**----- End of picture text -----**<br>


**Figure 13-171. Internal Loopback Mode** 

## _**13.4.1.4.4 Timestamp Generation**_ 

The MCAN module has integrated a 16-bit wrap-around counter for timestamp generation. The timestamp counter prescaler MCAN_TSCC[19-16] TCP field can be configured to clock the counter in multiples of CAN bit times (1-16). The counter is readable via the MCAN_TSCV[15-0] TSC field. A write access to the MCAN_TSCV register resets the counter to zero. When the timestamp counter wraps around the interrupt MCAN_IR[16] TSW flag is set. On start of a frame reception/transmission the counter value is captured and stored into the timestamp section of an Rx Buffer/Rx FIFO (RXTS[15-0]) or Tx Event FIFO (TXTS[15-0]) element. For more information, see Section 13.4.1.4.10, _Message RAM_ . 

## _**13.4.1.4.4.1 External Timestamp Counter**_ 

For CAN FD operation mode the MCAN core requires an External Timestamp Counter. An externally generated 16-bit vector may substitute the integrated 16-bit CAN bit time counter (internal timestamp counter) for receive and transmit timestamp generation. An external 16-bit timestamp counter can be used by programming the MCAN_TSCC[1-0] TSS field. 

The External Timestamp Counter uses the interface clock (ICLK) as a reference clock. The MCAN Core accepts a 16-bit timestamp. A 24-bit prescaler provides a programmable resolution for the timestamp (see MCANSS_EXT_TS_PRESCALER[23-0] PRESCALER bit field). The External Timestamp Counter counter can be enabled or disabled through the MCANSS_CTRL[6] EXT_TS_CNTR_EN bit. When disabled the counter is reset back to zero. While enabled the counter keeps incrementing. When the timestamp rolls over the MCAN timestamp interrupt is generated. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1519 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

When the timestamp rolls over the MCANSS_IRS register is set (see Figure 13-172). The MCANSS_IE register can be affected by writing to the MCANSS_IESS register to set or to the MCANSS_IECS register to clear. The MCANSS_IESS register is a shadow register mapped to the same address as the MCANSS_IE register. The level interrupt is a reflection of both MCANSS_IRS and MCANSS_IE being set. The MCANSS_IES register reflects the level interrupt. When an rollover event occurs the interrupt counter is incremented. Writing to the MCANSS_ICS register to clear the MCANSS_IRS register will also decrement the interrupt counter. Writing to the MCANSS_EOI register will issue another pulse if the interrupt counter is not zero. 

The rollover event can be artificially simulated by software through writing to the Interrupt Set Shadow register (MCANSS_ISS). The MCANSS_ISS register is a shadow register mapped to the same address as the MCANSS_IRS register. 

**==> picture [278 x 317] intentionally omitted <==**

**----- Start of picture text -----**<br>
External Timestamp Counter<br>Rollover (Pulse)<br>increment MCANSS_ICS MCANSS_ISS<br>decrement<br>Counter<br>increment<br>Counter > 0 MCANSS_EOI<br>MCANSS_IECS MCANSS_IESS<br>MCANSS_IE MCANSS_IRS<br>MCANSS_IES<br>Pulse interrupt Level interrupt<br>mcan-021<br>**----- End of picture text -----**<br>


**Figure 13-172. External Timestamp Counter Interrupt** 

## _**13.4.1.4.5 Timeout Counter**_ 

The MCAN module has integrated a 16-bit Timeout Counter. It is used to signal timeout conditions for the Rx FIFO 0, Rx FIFO 1, and Tx Event FIFO Message RAM elements. The Timeout Counter is configured via the MCAN_TOCC register. It is enabled via the MCAN_TOCC[0] ETOC bit. The Timeout Counter operates as down-counter and uses the same prescaler programmed by the MCAN_TSCC[19-16] TCP field as the Timestamp Counter. The actual counter value can be monitored from the MCAN_TOCV[15-0] TOC field. The Timeout Counter can be started only when MCAN_CCCR[0] INIT = 0 and stopped when MCAN_CCCR[0] INIT = 1 (example: when the MCAN enters Bus_Off state). The operation mode is selected by the MCAN_TOCC[2-1] TOS field. When Continuous Mode is selected, the counter starts when MCAN_CCCR[0] INIT = 0, a write to the MCAN_TOCV register presets the counter to the value configured by the MCAN_TOCC[31-16] TOP field and continues down-counting. 

In case the Timeout Counter is controlled by one of the FIFOs, an empty FIFO presets the counter to the value configured by the MCAN_TOCC[31-16] TOP field. Down-counting is started when the first FIFO element 

1520 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

is stored. Writing to the MCAN_TOCV register has no effect. When the counter reaches zero, the interrupt MCAN_IR[18] TOO flag is set. 

In Continuous Mode, the counter is immediately restarted at the value configured by the MCAN_TOCC[31-16] TOP field. 

## _**13.4.1.4.6 ECC Support**_ 

The Message Memory is wrapped in an ECC wrapper providing SECDED parity functionality. The ECC wrapper is controlled by an ECC Aggregator. 

## _**13.4.1.4.6.1 ECC Wrapper**_ 

The ECC wrapper provides Single Error Correction (SEC) and Double Error Detection (DED) parity to the Message Memory content. It has side band signals for error notification. The ECC Wrapper implements an error injection test mode. 

The error correction is done using a lazy write back. When an error is detected, it is noted in a FIFO Queue which waits for an access gap to write the data back and refresh the memory. If a transaction writes new data to the compromised entry before the lazy write back completes, the write back is discarded. 

## _**13.4.1.4.7 Rx Handling**_ 

The Rx Handler controls the following operations: 

- Acceptance filtering 

- The transfer of received messages to the Rx Buffers or to one of the two Rx FIFOs (Rx FIFO 0 or Rx FIFO 1) 

- Rx FIFO Put and Get Index operations 

## _**13.4.1.4.7.1 Acceptance Filtering**_ 

The MCAN module is capable to configure two sets of acceptance filters - one set for standard and one set for extended identifiers. These filters can be assigned to an Rx Buffer or to one of the two Rx FIFOs. 

The main features of the filter elements are: 

- Each filter element can be configured as: 

   - Range Filter (from - to) 

   - 

      - Filter for specific IDs (for one or two dedicated IDs) 

   - Classic Bit Mask Filter 

- Each filter element can be enabled/disabled individually 

- Each filter element can be configured for acceptance or rejection filtering 

- Filters are checked sequentially and execution (acceptance filtering procedure) stops at the first matching filter element or when the end of the filter list is reached 

Related configuration registers are: 

- Global Filter Configuration (MCAN_GFC) register 

- Standard ID Filter Configuration (MCAN_SIDFC) register 

- Extended ID Filter Configuration (MCAN_XIDFC) register 

- Extended ID AND Mask (MCAN_XIDAM) register 

Depending on the configuration of the filter element (see SFEC/EFEC in Section 13.4.1.4.10, _Message RAM_ ) if filter matches, one of the following actions is performed: 

- Received frame is stored in FIFO 0 or FIFO 1 

- Received frame is stored in Rx Buffer 

- Received frame is stored in Rx Buffer and generation of pulse at filter event pin is performed. This is high level single ICLK pulse. For more information, see Section 13.4.1.4.2.1, _DMA Requests_ . 

- Received frame is rejected 

- Set High Priority Message interrupt flag MCAN_IR[8] HPM 

- Set High Priority Message interrupt flag MCAN_IR[8] HPM and store received frame in 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1521 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## FIFO 0 or FIFO 1 

Acceptance filtering starts when complete Message ID is received. Acceptance filtering stops at the first matching enabled filter element or when the end of the filter list is reached. If a filter element matches - the Rx Handler starts writing the received message data in portions of 32 bit to the matching Rx Buffer or Rx FIFO. If an error condition occurs (for example: CRC error), this message is rejected with the following impact on the affected Rx Buffer or Rx FIFO: 

- Rx Buffer: 

   - New Data flag (MCAN_NDAT1/MCAN_NDAT2) of matching Rx Buffer is not set, but Rx Buffer (partly) overwritten with received data (for error type see MCAN_PSR[2-0] LEC respectively MCAN_PSR[10-8] DLEC fields). 

- Rx FIFO: 

   - Put index of matching Rx FIFO is not updated, but related Rx FIFO element (partly) overwritten with received data (for error type see MCAN_PSR[2-0] LEC respectively MCAN_PSR[10-8] DLEC fields). If matching Rx FIFO is configured to operate in overwrite mode, the boundary conditions described in Section 13.4.1.4.7.2.2 have to be considered. 

## _**13.4.1.4.7.1.1 Range Filter**_ 

Each filter element can be configured to operate as Range Filter (Standard Filter Type SFT = 00/Extended Filter Type EFT = 00). The filter matches for all received message frames with IDs in the range from SFID1 to SFID2 (SFID2 ≥ SFID1) respectively in the range from EFID1 to EFID2 (EFID2 ≥ EFID1). For more information see Section 13.4.1.4.10.5, _Standard Message ID Filter Element_ and Section 13.4.1.4.10.6, _Extended Message ID Filter Element_ . 

There are two options for range filtering of extended frames: 

- Extended Filter Type EFT = 00: The Extended ID AND Mask (MCAN_XIDAM) is used for Range Filtering. The Message ID of received frames is ANDed with the Extended ID AND Mask (MCAN_XIDAM) before the range filter is applied. 

- Extended Filter Type EFT = 11: The Extended ID AND Mask (MCAN_XIDAM) is not used for Range Filtering. 

## _**13.4.1.4.7.1.2 Filter for specific IDs**_ 

Each filter element can be configured to filter one or two dedicated Message IDs (Standard Filter Type SFT =01/ Extended Filter Type EFT =01). To filter only one specific Message ID, the filter element has to be configured with SFID1 = SFID2 respectively EFID1 = EFID2. For more information see Section 13.4.1.4.10.5, _Standard Message ID Filter Element_ and Section 13.4.1.4.10.6, _Extended Message ID Filter Element_ . 

## _**13.4.1.4.7.1.3 Classic Bit Mask Filter**_ 

Classic bit mask filtering can filter groups of Message IDs (Standard Filter Type SFT =10/Extended Filter Type EFT =10). This is done by masking single bits of a received Message ID. In this case SFID1/EFID1 element is used as Message ID filter, while SFID2/EFID2 element is used as filter mask. 

A 0 bit at the filter mask (SFID2/EFID2) will mask out the corresponding bit position of the configured Message ID filter (SFID1/EFID1) and the value of the received Message ID at that bit position is not relevant for acceptance filtering. Only those bits of the received Message ID where the corresponding mask bits are 1 are relevant for acceptance filtering. 

There are two interesting cases: 

- All mask bits are 1: a match occurs only when the received Message ID and the configured Message ID filter are identical. 

- All mask bits are 0: all Message IDs match. 

## _**13.4.1.4.7.1.4 Standard Message ID Filtering**_ 

The standard Message ID (11-bit ID) filtering flow is shown in Figure 13-173. Section 13.4.1.4.10.5, _Standard Message ID Filter Element_ describes the standard Message ID filter element. 

1522 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

The Remote Transmission Request (RTR) and Extended Identifier (XTD) bits of the received frames are compared against the list of configured filter elements. This is controlled by the following registers: 

- Global Filter Configuration (MCAN_GFC) register 

- Standard ID Filter Configuration (MCAN_SIDFC) register 

**==> picture [476 x 441] intentionally omitted <==**

**----- Start of picture text -----**<br>
valid frame received<br>11 bit 29 bit<br>11 / 29 bit identifier<br>yes MCAN_GFC[1] RRFS = ‘1’<br>remote frame reject remote frames<br>no MCAN_GFC[1] RRFS = 0‘’<br>receive filter list enabled<br>MCAN_SIDFC[23-16] LSS > 0<br>match filter element #0 yes<br>no<br>match filter element<br>#(MCAN_SIDFC[23-16] LSS) reject<br>acceptance / rejection<br>yes<br>no accept<br>MCAN_GFC[5] ANFS = ‘1’<br>accept non-matching frames discard frame<br>MCAN_GFC[5] ANFS = ‘0’<br>yes<br>FIFO selected and<br>target FIFO full (blocking)<br>no<br>store frame<br>‘0’<br>=<br>MCAN_SIDFC[23-16] LSS<br>**----- End of picture text -----**<br>


**==> picture [23 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
mcan-009<br>**----- End of picture text -----**<br>


**Figure 13-173. Standard Message ID Filter Path** 

## _**13.4.1.4.7.1.5 Extended Message ID Filtering**_ 

The extended Message ID (29-bit ID) filtering flow is shown in Figure 13-174. Section 13.4.1.4.10.6, _Extended Message ID Filter Element_ describes the extended Message ID filter element. 

The Remote Transmission Request (RTR) and Extended Identifier (XTD) bits of the received frames are compared against the list of configured filter elements. This is controlled by the following registers: 

- Global Filter Configuration (MCAN_GFC) register 

- Extended ID Filter Configuration (MCAN_XIDFC) register 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1523 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

Note that before the filter list is executed the received identifier is ANDed with the Extended ID AND Mask (MCAN_XIDAM). 

**==> picture [479 x 430] intentionally omitted <==**

**----- Start of picture text -----**<br>
valid frame received<br>11 bit 29 bit<br>11 / 29 bit identifier<br>MCAN_GFC[0] RRFE = ‘1’ yes<br>reject remote frames remote frame<br>MCAN_GFC[0] RRFE = ‘0’ no<br>receive filter list enabled<br>MCAN_XIDFC[22-16] LSE > 0<br>yes match filter element #0<br>no<br>match filter element<br>reject #(MCAN_XIDFC[22-16] LSE)<br>acceptance / rejection<br>yes<br>accept no<br>MCAN_GFC[3] ANFE = ‘1’<br>discard frame accept non-matching frames<br>MCAN_GFC[3] ANFE = ‘0’<br>yes FIFO selected and<br>target FIFO full (blocking)<br>no<br>store frame<br>MCAN_XIDFC[22-16] LSE<br>=<br>‘0’<br>**----- End of picture text -----**<br>


**==> picture [24 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
mcan-010<br>**----- End of picture text -----**<br>


**Figure 13-174. Extended Message ID Filter Path** 

## _**13.4.1.4.7.2 Rx FIFOs**_ 

The configuration of the Rx FIFOs (Rx FIFO 0 and Rx FIFO 1) can be done via the MCAN_RXF0C and MCAN_RXF1C registers. Each Rx FIFO can be configured to store up to 64 received messages. 

After acceptance filtering the received messages that passed are transferred to the Rx FIFO. The filter mechanisms available for the Rx FIFO 0 and Rx FIFO 1 is described in Section 13.4.1.4.7.1, _Acceptance Filtering_ . Section 13.4.1.4.10.2, _Rx Buffer and FIFO Element_ describes the Rx FIFO element. 

The Rx FIFO watermark can be used to prevent an Rx FIFO overflow. If the Rx FIFO fill level reaches the Rx FIFO watermark configured by the MCAN_RXFnC[30-24] FnWM field (where: n = 0 or 1) an interrupt flag MCAN_IR[1] RF0W/MCAN_IR[5] RF1W is set. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1524 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

When the Rx FIFO Put Index reaches the Rx FIFO Get Index (MCAN_RXFnS[21-16] FnPI = MCAN_RXFnS[13-8] FnGI) an Rx FIFO Full condition is signalled by the MCAN_RXFnS[24] FnF status bit and interrupt flag MCAN_IR[2] RF0F/MCAN_IR[6] RF1F is set. Figure 13-175 shows Rx FIFO Status. The FIFOs fill level is presented in the MCAN_RXFnS[6-0] FnFL field (the number of elements stored in Rx FIFO). 

**==> picture [319 x 222] intentionally omitted <==**

**----- Start of picture text -----**<br>
Get Index<br>MCAN_RXFnS[13-8] FnGI<br>7 0<br>6 1<br>Put Index 5 2<br>MCAN_RXFnS[21-16] FnPI<br>4 3<br>Fill Level<br>MCAN_RXFnS[6-0] FnFL<br>mcan-011<br>**----- End of picture text -----**<br>


**Figure 13-175. Rx FIFO Status** 

Rx FIFOs start address in the Message RAM (MCAN_RXFnC[15-2] FnSA field) have to be configured when reading from an Rx FIFO (Rx FIFO Get Index - MCAN_RXFnS[13-8] FnGI). Table 13-211 presents Rx Buffer/Rx FIFO Element Size for different Rx Buffer/Rx FIFO Data Field Size which is configured via the MCAN_RXESC register. 

**Table 13-211. Rx Buffer/Rx FIFO Element Size** 

|**MCAN_RXESC[10-8] RBDS**<br>**MCAN_RXESC[2-0] F0DS/**<br>**MCAN_RXESC[6-4] F1DS**|**Data Field**<br>**[bytes]**|**FIFO Element Size**<br>**[RAM words]**|
|---|---|---|
|000|8|4|
|001|12|5|
|010|16|6|
|011|20|7|
|100|24|8|
|101|32|10|
|110|48|14|
|111|64|18|



## _**13.4.1.4.7.2.1 Rx FIFO Blocking Mode**_ 

The Rx FIFO blocking mode is the default operation mode for the Rx FIFOs. It is configured by the MCAN_RXFnC[31] FnOM = 0. 

If an Rx FIFO full condition is reached (MCAN_RXFnS[21-16] FnPI = MCAN_RXFnS[13-8] FnGI), no further messages are written to the corresponding Rx FIFO until at least one message has been read out and the Rx FIFO Get Index has been incremented. An Rx FIFO full condition is signalled by the MCAN_RXFnS[24] FnF = 1 and interrupt flag MCAN_IR[2] RF0F/MCAN_IR[6] RF1F is set. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1525 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

In case a message is received while the corresponding Rx FIFO is full, this message is rejected and the message lost condition is signalled by MCAN_RXFnS[25] RFnL = 1 and interrupt flag MCAN_IR[3] RFnL/ MCAN_IR[25] RFnL is set. 

## _**13.4.1.4.7.2.2 Rx FIFO Overwrite Mode**_ 

The Rx FIFO overwrite mode is configured by the MCAN_RXFnC[31] FnOM = 1. When an Rx FIFO full condition is reached (MCAN_RXFnS[21-16] FnPI = MCAN_RXFnS[13-8] FnGI) signalled by MCAN_RXFnS[24] FnF = 1, the next accepted message for the FIFO will overwrite the oldest FIFO message. Put index/Get index are both incremented by one. 

In overwrite mode if an Rx FIFO full condition is signalled, reading of the Rx FIFO elements should start at least at get index + 1. The reason for that is, that it might happen, that a received message is written to the Message RAM (Put index) while the Host CPU is reading from the Message RAM (Get index). In this case inconsistent data may be read from the respective Rx FIFO element. The problem is solved by adding an offset to the Get index when reading from the Rx FIFO. The offset depends on how fast the Host CPU accesses the Rx FIFO. Figure 13-176 shows an offset of two with respect to the Get index when reading the Rx FIFO. In this case the two messages stored in element 1 and 2 are lost. 

**==> picture [352 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
Rx FIFO Full Rx FIFO Overwritel<br>(MCAN_RXFnS[24] FnF = ‘1’) (MCAN_RXFnS[24] FnF = ‘1’)<br>MCAN_RXFnS[21-16] FnPI<br>element 0 overwritten<br>= MCAN_RXFnS[13-8] FnGI<br>MCAN_RXFnS[21-16] FnPI<br>7 0 7 0 = MCAN_RXFnS[13-8] FnGI<br>6 1 6 1<br>5 2 5 2<br>4 3 4 3<br>read Get Index + 2<br>mcan-012<br>**----- End of picture text -----**<br>


**Figure 13-176. Rx FIFO Overflow Handling** 

After reading from the Rx FIFO, the number of the last element read has to be written to the Rx FIFO Acknowledge Index MCAN_RXFnA[5-0] FnAI. This increments the get index to that element number. In case the Put index has not been incremented to this Rx FIFO element, the Rx FIFO full condition is reset (MCAN_RXFnS[24] FnF = 0). 

## _**13.4.1.4.7.3 Dedicated Rx Buffers**_ 

The MCAN supports up to 64 dedicated Rx Buffers. The start address of the Rx Buffers section in the Message RAM is configured via MCAN_RXBC[15-2] RBSA field. To store in an Rx Buffer a Standard or Extended Message ID Filter Element with SFEC/EFEC = 111 and SFID2/EFID2[10-9] = 00 has to be configured (see Section 13.4.1.4.10.5, _Standard Message ID Filter Element_ and Section 13.4.1.4.10.6, _Extended Message ID Filter Element_ ). 

After a received message has been accepted by a filter element, the message is stored into the Rx Buffer in the Message RAM referenced by the filter element (the format is the same as for an Rx FIFO element). In addition the flag MCAN_IR[19] DRX (Message stored in Dedicated Rx Buffer) is set. 

Table 13-212 shows Example Filter Configuration for Rx Buffers. 

1526 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-212. Example Filter Configuration for Rx Buffers** 

||**Filter**|**Element**|**SFID1[10-0]**<br>**EFID1[28-0]**|**SFID2[10-9]**<br>**EFID2[10-9]**|**SFID2[5-0]**<br>**EFID2[5-0]**|
|---|---|---|---|---|---|
|0|||ID message 1|00|00 0000|
|1|||ID message 2|00|00 0001|
|2|||ID message 3|00|00 0010|



After the last word of a matching received message has been written to the Message RAM, the respective New Data flag in register MCAN_NDAT1/MCAN_NDAT2 is set. As long as the New Data flag is set, the respective Rx Buffer is locked against updates from received matching frames. The New Data flags have to be reset by the Host CPU by writing a 1 to the respective bit position. 

While an Rx Buffer's New Data flag is set, a Message ID Filter Element referencing this specific Rx Buffer will not match, causing the acceptance filtering to continue. Following Message ID Filter Elements may cause the received message to be stored into another Rx Buffer, or into an Rx FIFO, or the message may be rejected, depending on filter configuration. 

## _**13.4.1.4.7.3.1 Rx Buffer Handling**_ 

Rx Buffer Handling include the following steps: 

- Reset interrupt flag MCAN_IR[19] DRX 

- Read New Data registers 

- Read messages from Message RAM 

- Reset New Data flags of processed messages 

## _**13.4.1.4.7.4 Debug on CAN Support**_ 

Debug DMA is not supported feature. Debug messages can be traced through the RX FIFO (see Section 13.4.1.4.7.2). 

## _**13.4.1.4.8 Tx Handling**_ 

The Tx Handler is used to handle the Tx requests. It controls the transfer of transmit messages from the dedicated Tx Buffers, the Tx FIFO, and the Tx Queue to the CAN Core, the Tx Event FIFO, and the Put and Get Index operations. The MCAN module supports up to 32 Tx Buffers. These Tx Buffers can be configured as dedicated Tx Buffers, Tx FIFO, or Tx Queue and as combination of dedicated Tx Buffers/Tx FIFO or dedicated Tx Buffers/Tx Queue. For each Tx Buffer element Classical CAN or CAN FD transmission mode can be configured. Section 13.4.1.4.10.3 describes the Tx Buffer Element. Table 13-213 shows the possible configurations for message transmission. 

**Table 13-213. Possible Configurations for Message Transmission** 

|**MCAN_CCCR**|**MCAN_CCCR**|**Tx**|**Buffer Element**|**Frame Transmission**|
|---|---|---|---|---|
|**MCAN_CCCR[9]**<br>**BRSE**|**MCAN_CCCR[8]**<br>**FDOE**|**FDF**|**BRS**||
|ignored|0|ignored|ignored|Classic CAN|
|0|1|0|ignored|Classic CAN|
|0|1|1|ignored|CAN FD without bit rate switching|
|1|1|0|ignored|Classic CAN|
|1|1|1|0|CAN FD without bit rate switching|
|1|1|1|1|CAN FD with bit rate switching|



When the Tx Buffer Request Pending MCAN_TXBRP register is updated, or when a transmission has been started the Tx Handler starts scanning to check for the highest priority pending Tx request. The Tx Buffer with lowest Message ID has highest priority. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1527 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Note** 

AUTOSAR requires at least three Tx Queue Buffers and support of transmit cancellation. 

## _**13.4.1.4.8.1 Transmit Pause**_ 

The transmit pause feature is intended for use in CAN networks where the CAN Message IDs are specific and cannot easily be changed. These Message IDs may have a higher priority than other defined Message IDs, while in a specific application their relative priority should be inverse. This allows for a case where one ECU sends a burst of CAN messages that cause another ECU's CAN messages to be delayed (paused). 

The transmit pause feature is enabled by the MCAN_CCCR[14] TXP bit. By default this bit is disabled (MCAN_CCCR[14] TXP = 0). Each time after successfully transmitted message, a pause for two CAN bit times occurs before the start of the next transmission. This allows the other CAN nodes in the network to transmit messages even if their Message IDs have lower priority. 

## _**13.4.1.4.8.2 Dedicated Tx Buffers**_ 

Dedicated Tx Buffers are intended for message transmission under complete control of the Host CPU. 

There are two options: 

- Each dedicated Tx Buffer is configured with a specific Message ID. 

- Two or more dedicated Tx Buffers are configured with the same Message ID. In this case the Tx Buffer with the lowest buffer number is transmitted first. 

After the data section has been updated, a transmission is requested by an Add Request. This is done via the MCAN_TXBAR[x]ARn bit (where x = 0 - 31). The requested messages arbitrate internally with messages from an optional Tx FIFO or Tx Queue and externally with messages on the CAN bus, and are sent out according to their Message ID. 

Table 13-214 shows Tx Buffer/Tx FIFO/Tx Queue Element Size. A Dedicated Tx Buffer allocates Element Size 32-bit words in the Message RAM. The start address of a dedicated Tx Buffer in the Message RAM is calculated by adding transmit buffer index from 0 to 31 (MCAN_TXFQS[20-16] TFQPI) × Element Size to the Tx Buffer Start Address MCAN_TXBC[15-2] TBSA field. 

**Table 13-214. Tx Buffer/Tx FIFO/Tx Queue Element Size** 

|**MCAN_TXESC[2-0] TBDS**|**Data Field [bytes]**|**Element Size [RAM words]**|
|---|---|---|
|000|8|4|
|001|12|5|
|010|16|6|
|011|20|7|
|100|24|8|
|101|32|10|
|110|48|14|
|111|64|18|



## _**13.4.1.4.8.3 Tx FIFO**_ 

Tx FIFO mode is configured by setting bit MCAN_TXBC[30] TFQM = 0. The stored in the Tx FIFO messages are transmitted starting with the message referenced by the Get Index MCAN_TXFQS[12-8] TFGI field. After each transmission the Get Index is incremented until the Tx FIFO is empty. The Tx FIFO Free Level MCAN_TXFQS[5-0] TFFL field indicates the number of the available free Tx FIFO elements. The Tx FIFO allows transmission of messages with the same Message ID from different Tx Buffers in the order these messages have been written to the Tx FIFO. 

New transmit messages have to be written to the Tx FIFO starting with the Tx Buffer referenced by the Put Index MCAN_TXFQS[20-16] TFQPI field. After each Add Request (MCAN_TXBAR[x] ARn = 1) the 

1528 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

Put Index is incemented to the next free Tx FIFO element. When the Put Index reaches the Get Index (MCAN_TXFQS[20-16] TFQPI = MCAN_TXFQS[12-8] TFGI), Tx FIFO Full condition is signalled by bit MCAN_TXFQS[21] TFQF = 1. In this case no further messages should be written to the Tx FIFO until the next message has been transmitted and the Get Index has been incremented. 

The number of requested Tx buffers should not exceed the number of free Tx Buffers as indicated by the Tx FIFO Free Level MCAN_TXFQS[5-0] TFFL field. 

In case a transmission request for the Tx Buffer referenced by the Get Index is cancelled, the Get Index is incremented to the next Tx Buffer with pending transmission request and the Tx FIFO Free Level MCAN_TXFQS[5-0] TFFL field is recalculated. In case transmission cancellation is applied to any other Tx Buffer - the Get Index and the FIFO Free Level remain unchanged. 

A Tx FIFO element allocates Element Size 32-bit words in the Message RAM (see Table 13-214). The start address of the next available (free) Tx FIFO Buffer is calculated by adding Tx FIFO/Queue Put Index MCAN_TXFQS[20-16] TFQPI (from 0 to 31) × Element Size to the Tx Buffer Start Address MCAN_TXBC[15-2] TBSA field. 

## _**13.4.1.4.8.4 Tx Queue**_ 

Tx Queue mode is configured by setting bit MCAN_TXBC[30] TFQM = 1. The stored in the Tx Queue messages are transmitted starting with the highest priority message (lowest Message ID). In case two or more Queue Buffers are configured with the same Message ID, the Queue Buffer with the lowest buffer number is transmitted first. 

New transmit messages have to be written to the Tx FIFO starting with the Tx Buffer referenced by the Put Index MCAN_TXFQS[20-16] TFQPI field. Each Add Request cyclically increments the Put Index to the next free Tx Buffer. In case of Tx Queue Full condition (MCAN_TXFQS[21] TFQF = 1), the Put Index is not valid and no further message should be written to the Tx Queue until at least one of the requested messages has been sent out or a pending transmission request has been cancelled. 

In Queue mode, only Full Index and Put Index are returned in read. The other fields - Get Index and Free Level are read as 0. 

The application may use the MCAN_TXBRP register instead of the Put Index and may place messages to any Tx Buffer without pending transmission request. 

A Tx Queue Buffer allocates Element Size 32-bit words in the Message RAM (see Table 13-214). The start address of the next available (free) Tx Queue Buffer is calculated by adding Tx FIFO/Queue Put Index MCAN_TXFQS[20-16] TFQPI (from 0 to 31) × Element Size to the Tx Buffer Start Address MCAN_TXBC[15-2] TBSA field. 

## _**13.4.1.4.8.5 Mixed Dedicated Tx Buffers/Tx FIFO**_ 

For this combination the Tx Buffers section in the Message RAM is separated in two parts: 

- Dedicated Tx Buffers: the number of Dedicated Tx Buffers is configured by the MCAN_TXBC[21-16] NDTB field 

- Tx FIFO: the number of Tx Buffers assigned to the Tx FIFO is configured by the MCAN_TXBC[29-24] TFQS field 

If the MCAN_TXBC[29-24] TFQS field is empty (zero) - only Dedicated Tx Buffers are used. 

Tx prioritization: 

- Scan Dedicated Tx Buffers and oldest pending Tx FIFO Buffer (referenced by the MCAN_TXFQS[12-8] TFGI field) 

- Buffer with lowest Message ID gets highest priority and is transmitted next 

Figure 13-177 shows Mixed Dedicated Tx Buffers/Tx FIFO example. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1529 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [328 x 108] intentionally omitted <==**

**----- Start of picture text -----**<br>
Dedicated Tx Buffers Tx FIFO<br>Buffer Index 0 1 2 3 4 5 6 7 8 9<br>ID 3 ID 15 ID 8 ID 24 ID 4Id4 ID 2Id2<br>Tx Sequence 1. 5. 4. 6. 2. 3.<br>Get Index Put Index<br>**----- End of picture text -----**<br>


**==> picture [23 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
mcan-013<br>**----- End of picture text -----**<br>


**Figure 13-177. Mixed Dedicated Tx Buffers/Tx FIFO (example)** 

## _**13.4.1.4.8.6 Mixed Dedicated Tx Buffers/Tx Queue**_ 

For this combination the Tx Buffers section in the Message RAM is separated in two parts: 

- Dedicated Tx Buffers: the number of Dedicated Tx Buffers is configured by the MCAN_TXBC[21-16] NDTB field 

- Tx Queue: the number of Tx Buffers assigned to the Tx Queue is configured by the MCAN_TXBC[29-24] TFQS field 

If MCAN_TXBC[29-24] TFQS field is empty (zero) - only Dedicated Tx Buffers are used. 

Tx prioritization: 

- Scan all Tx Buffers with activated transmission request 

- Tx Buffer with lowest Message ID gets highest priority and is transmitted next 

Figure 13-178 shows Mixed Dedicated Tx Buffers/Tx Queue example. 

**==> picture [328 x 108] intentionally omitted <==**

**----- Start of picture text -----**<br>
Dedicated Tx Buffers Tx Queue<br>Buffer Index 0 1 2 3 4 5 6 7 8 9<br>ID 3 ID 15 ID 8 ID 24 ID 4Id4 ID 2Id2<br>Tx Sequence 2. 5. 4. 6. 3. 1.<br>Put Index<br>**----- End of picture text -----**<br>


**==> picture [23 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
mcan-014<br>**----- End of picture text -----**<br>


**Figure 13-178. Mixed Dedicated Tx Buffers/Tx Queue (example)** 

## _**13.4.1.4.8.7 Transmit Cancellation**_ 

This feature is especially intended for gateway and AUTOSAR based applications. The Host CPU can cancel a requested transmission from a dedicated Tx Buffer or a Tx Queue Buffer by setting bit MCAN_TXBCR[n] CRn = 1 (where n = 0 - 31). The corresponding bit position n is equivalent to the number of the Tx Buffer. 

Transmit cancellation is not intended for Tx FIFO operation. 

Successful cancellation is signalled by setting the corresponding bit of the MCAN_TXBCF register (MCAN_TXBCF[n] CFn = 1). 

If transmission from a Tx Buffer is already ongoing and a transmit cancellation is requested, the corresponding MCAN_TXBRP[n] TRPn bit remains set as long as the transmission is in progress. If the transmission was successful, the corresponding MCAN_TXBTO[n] TOn and MCAN_TXBCF[n] CFn bits are set. If the transmission was not successful, only the corresponding bit MCAN_TXBCF[n] CFn = 1. 

1530 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

If pending transmission is cancelled immediately before this transmission could have been started, a short time window occurs where no transmission is started even if another message is also pending in this node. This may enable another node to transmit a message which may have a lower priority than the second message in this node. 

## _**13.4.1.4.8.8 Tx Event Handling**_ 

To support Tx Event Handling the Message RAM has implemented a Tx Event FIFO section. Up to 32 Tx Event FIFO elements can be configured. Section 13.4.1.4.10.4 describes the Tx Event FIFO element. After message transmission on the CAN bus, Message ID and Timestamp are stored in a Tx Event FIFO element. To link a Tx Event to a Tx Event FIFO element, the Message Marker from the transmitted Tx Buffer is copied into the Tx Event FIFO element. 

A Tx Event FIFO full condition is signalled by the MCAN_IR[14] TEFF bit. In this case no further elements are written to the Tx Event FIFO until at least one element has been read out and the Tx Event FIFO Get Index has been incremented (MCAN_TXEFS[12-8] EFGI). In case a Tx Event occurs while the Tx Event FIFO is full, this event is rejected and interrupt flag MCAN_IR[15] TEFL bit is set. 

The Tx Event FIFO watermark can be configured to avoid a Tx Event FIFO overflow. When the Tx Event FIFO fill level reaches the Tx Event FIFO watermark configured by the MCAN_TXEFC[29-24] EFWM field, interrupt flag MCAN_IR[13] TEFW is set. When reading from the Tx Event FIFO, two times the Tx Event FIFO Get Index MCAN_TXEFS[12-8] EFGI field has to be added to the Tx Event FIFO start address MCAN_TXEFC[15-2] EFSA field. 

## _**13.4.1.4.9 FIFO Acknowledge Handling**_ 

The Get Indices of the two Rx FIFOs (Rx FIFO 0 or Rx FIFO 1) and the Tx Event FIFO are controlled by writing to the corresponding FIFO Acknowledge Index (see MCAN_RXF0A, MCAN_RXF1A, and MCAN_TXEFA). Writing to the FIFO Acknowledge Index will set the FIFO Get Index to the FIFO Acknowledge Index plus one and thereby updates the FIFO Fill Level. 

There are two use cases: 

- A single element has been read from the FIFO: the Get Index value is written to the FIFO Acknowledge Index. 

- A sequence of elements has been read from the FIFO: the Get Index value (Index of the last element read) is written to the FIFO Acknowledge Index at the end of that read sequence. 

The Host CPU has free access to the Message RAM. The special care has to be taken when reading FIFO elements in an arbitrary order (Get Index not considered). This can be useful when reading a High Priority Message from one of the two Rx FIFOs. In this case the FIFO's Acknowledge Index should not be written because this would set the Get Index to a wrong position and also changes the FIFO's Fill Level. In this case some of the older FIFO elements would be lost. 

## **Note** 

The application has to ensure that a valid value is written to the FIFO Acknowledge Index. The MCAN module does not check for erroneous values. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1531 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.1.4.10 Message RAM**_ 

The MCAN module has implemented Message RAM. The main purpose of the Message RAM is to store: 

- Receive Messages 

- Transmit Messages 

- Tx Event Elements 

- Message ID Filter Elements 

## _**13.4.1.4.10.1 Message RAM Configuration**_ 

The MCAN module is configured to allocate 4352 words in the Message RAM. The Message RAM has a width of 32 bits. 

The following table presents the Message RAM Address Range for all device MCAN instances. 

**Table 13-215. Message RAM Address Range** 

|**Module Instance**|**Region Name**|**Address Range**|**Address Range**|**Size**|
|---|---|---|---|---|
|||**Start**|**End**||
|MCAN0<br>MCAN1<br>MCAN2<br>MCAN3<br>MCAN4<br>MCAN5<br>MCAN6<br>MCAN7|MCAN0_MSGMEM_RAM<br>MCAN1_MSGMEM_RAM<br>MCAN2_MSGMEM_RAM<br>MCAN3_MSGMEM_RAM<br>MCAN4_MSGMEM_RAM<br>MCAN5_MSGMEM_RAM<br>MCAN6_MSGMEM_RAM<br>MCAN7_MSGMEM_RAM|5260 0000h<br>5261 0000h<br>5262 0000h<br>5263 0000h<br>5264 0000h<br>5265 0000h<br>5266 0000h<br>5267 0000h|5260 7FFFh<br>5261 7FFFh<br>5262 7FFFh<br>5263 7FFFh<br>5264 7FFFh<br>5265 7FFFh<br>5266 7FFFh<br>5267 7FFFh|32 KB<br>32 KB<br>32 KB<br>32 KB<br>32 KB<br>32 KB<br>32 KB<br>32 KB|



The Message RAM is capable to include each of the sections listed in Figure 13-179. It is not necessary to configure each of the sections (a section in the Message RAM can be 0) and there is no restriction in regards to the sequence of the sections. For parity checking or ECC, the respective number of bits must to be added to each word. 

The MCAN module addresses 32-bit words when addressing the Message RAM. The start addresses are configurable and are 32-bit word addresses. 

The element size can be configured for: 

- Rx FIFO 0 via the MCAN_RXESC[2-0] F0DS field 

- Rx FIFO 1 via the MCAN_RXESC[6-4] F1DS field 

- Rx Buffers via the MCAN_RXESC[10-8] RBDS field 

- Tx Buffers via the MCAN_TXESC[2-0] TBDS field 

1532 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [290 x 209] intentionally omitted <==**

**----- Start of picture text -----**<br>
Start Address<br>MCAN_SIDFC[15-2] FLSSA 11-bit Filter 128 elements<br>MCAN_XIDFC[15-2] FLESA 29-bit Filter 64 elements<br>MCAN_RXF0C[15-2] F0SA Rx FIFO 0 64 elements<br>MCAN_RXF1C[15-2] F1SA Rx FIFO 1 64 elements<br>MCAN_RXBC[15-2] RBSA Rx Buffers 64 elements<br>MCAN_TXEFC[15-2] EFSA Tx Event FIFO 32 elements<br>MCAN_TXBC[15-2] TBSA Tx Buffers 32 elements<br>32 bit<br>4352 words<br>**----- End of picture text -----**<br>


mcan-015 

**Figure 13-179. Message RAM Configuration** 

The Host CPU configures the following information in the Message RAM: 

- Start addresses of the memory sections 

- Number of elements in each section 

- The size of the elements in some sections 

## **Note** 

The MCAN module does not check for errors in the Message RAM configuration. The configuration of the start addresses of the different sections and the number of elements of each section has to be done carefully to prevent falsification or loss of data. 

## _**13.4.1.4.10.2 Rx Buffer and FIFO Element**_ 

Up to 64 Rx Buffers and two Rx FIFOs can be configured in the Message RAM. Each Rx FIFO section can be configured to store up to 64 received messages. The element size can be configured for storage of CAN FD messages with up to 64 bytes data field via the MCAN_RXESC register. 

Figure 13-180 shows Rx Buffer/Rx FIFO element structure. 

**==> picture [296 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24 23 16 15 8 7 0<br>R0 ID[28-0]<br>R1 FIDX[6-0] DLC[3-0] RXTS[15-0]<br>R2 DB3[7-0] DB2[7-0] DB1[7-0] DB0[7-0]<br>R3 DB7[7-0] DB6[7-0] DB5[7-0] DB4[7-0]<br>... ... ... ... ...<br>Rn DBm[7-0] DBm-1[7-0] DBm-2[7-0] DBm-3[7-0]<br>ESI XTD RTR<br>ANMF RES FDF BRS<br>**----- End of picture text -----**<br>


**==> picture [24 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
mcan-016<br>**----- End of picture text -----**<br>


**Figure 13-180. Rx Buffer/Rx FIFO Element Structure** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1533 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

Table 13-216 shows Rx Buffer/Rx FIFO element field descriptions. 

**Table 13-216. Rx Buffer/Rx FIFO Element Field Descriptions** 

|**Word**|**Bits**<br>**Field Name**<br>**Description**|
|---|---|
|R0|31<br>ESI<br>Error State Indicator<br>•<br>0h = Transmitting node is error active<br>•<br>1h = Transmitting node is error passive|
||30<br>XTD<br>Extended Identifier<br>Signals to the Host CPU whether the received frame has a<br>standard or extended identifier.<br>•<br>0h = 11-bit standard identifier<br>•<br>1h = 29-bit extended identifier|
||29<br>RTR<br>Remote Transmission Request<br>Signals to the Host CPU whether the received frame is a data<br>frame or a remote frame.<br>•<br>0h = Received frame is a data frame<br>•<br>1h = Received frame is a remote frame<br>**Note:**There are no remote frames in CAN FD format. In case<br>a CAN FD frame was received (FDF = 1), RTR bit reflects the<br>state of the reserved r1 bit (RES[23]).|
||28-0<br>ID[28-0]<br>Identifier<br>Standard or extended identifier depending on XTD bit. A<br>standard identifier is stored into ID[28-18].|



1534 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-216. Rx Buffer/Rx FIFO Element Field Descriptions (continued)** 

|**Word**|**Bits**<br>**Field Name**<br>**Description**|
|---|---|
|R1|31<br>ANMF<br>Accepted Non-matching Frame<br>Acceptance of non-matching frames may be enabled via the<br>MCAN_GFC[5-4] ANFS and MCAN_GFC[3-2] ANFE fields.<br>•<br>0h = Received frame matching filter index FIDX field<br>•<br>1h = Received frame did not match any Rx filter element|
||30-24<br>FIDX[6-0]<br>Filter Index<br>0h-7Fh (0-127): Index of matching Rx acceptance filter element<br>(invalid if ANMF = 1).<br>Range is 0 to MCAN_SIDFC[23-16] LSS - 1 respectively<br>MCAN_XIDFC[22-16] LSE - 1.|
||23-22<br>RES<br>Reserved|
||21<br>FDF<br>FD Format<br>•<br>0h = Standard frame format<br>•<br>1h = CAN FD frame format (new DLC-coding and CRC)|
||20<br>BRS<br>Bit Rate Switch<br>•<br>0h = Frame received without bit rate switching<br>•<br>1h = Frame received with bit rate switching|
||19-16<br>DLC[3-0]<br>Data Length Code<br>•<br>0h-8h (0-8) = CAN + CAN FD: received frame has 0-8 data<br>bytes<br>•<br>9h-Fh (9-15) = CAN: received frame has 8 data bytes<br>•<br>9h-Fh (9-15) = CAN FD: received frame has<br>12/16/20/24/32/48/64 data bytes|
||15-0<br>RXTS[15-0]<br>Rx Timestamp<br>Timestamp Counter value captured on start of frame reception.<br>Resolution depending on configuration of the Timestamp<br>Counter Prescaler MCAN_TSCC[19-16] TCP.|
|R2|31-24<br>DB3[7-0]<br>Data Byte 3|
||23-16<br>DB2[7-0]<br>Data Byte 2|
||15-8<br>DB1[7-0]<br>Data Byte 1|
||7-0<br>DB0[7-0]<br>Data Byte 0|
|R3|31-24<br>DB7[7-0]<br>Data Byte 7|
||23-16<br>DB6[7-0]<br>Data Byte 6|
||15-8<br>DB5[7-0]<br>Data Byte 5|
||7-0<br>DB4[7-0]<br>Data Byte 4|
|...|...<br>...<br>...|
|Rn|31-24<br>DBm[7-0]<br>Data Byte m|
||23-16<br>DBm-1[7-0]<br>Data Byte m-1|
||15-8<br>DBm-2[7-0]<br>Data Byte m-2|
||7-0<br>DBm-3[7-0]<br>Data Byte m-3|



**Note:** Depending on the configuration of the element size (MCAN_RXESC), between two and sixteen 32-bit words (Rn = 3-17) are used for storage of a CAN message's data field. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1535 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.1.4.10.3 Tx Buffer Element**_ 

The Tx Buffers section can be configured to hold dedicated Tx Buffers as well as a Tx FIFO/Tx Queue. In case that the Tx Buffers section is shared by dedicated Tx buffers and a Tx FIFO/Tx Queue, the dedicated Tx Buffers start at the beginning of the Tx Buffers section followed by the buffers assigned to the Tx FIFO or Tx Queue. The Tx Handler makes difference between dedicated Tx Buffers and Tx FIFO/Tx Queue via the MCAN_TXBC[29-24] TFQS and MCAN_TXBC[21-16] NDTB fields. The element size can be configured for storage of CAN FD messages with up to 64 bytes data field via the MCAN_TXESC register. 

Figure 13-181 shows Tx Buffer element structure. 

|mcan-018<br>31<br>24 23<br>16 15<br>8 7<br>0<br>E0<br>E1<br>ESI<br>XTD<br>RTR<br>BRS<br>FDF<br>ID[28-0]<br>TXTS[15-0]<br>DLC[3-0]<br>MM[7-0]<br>ET[1-0]<br>**Figure 13-181. Tx Buffer Element Structure**<br>Table 13-217shows Tx Buffer element field descriptions.<br>**Table 13-217. Tx Buffer Element Field Descriptions**|mcan-018<br>31<br>24 23<br>16 15<br>8 7<br>0<br>E0<br>E1<br>ESI<br>XTD<br>RTR<br>BRS<br>FDF<br>ID[28-0]<br>TXTS[15-0]<br>DLC[3-0]<br>MM[7-0]<br>ET[1-0]<br>**Figure 13-181. Tx Buffer Element Structure**<br>Table 13-217shows Tx Buffer element field descriptions.<br>**Table 13-217. Tx Buffer Element Field Descriptions**|
|---|---|
|**Word**|**Bits**<br>**Field Name**<br>**Description**|
|T0|31<br>ESI<br>Error State Indicator<br>•<br>0h = ESI bit in CAN FD format depends only on error<br>passive flag<br>•<br>1h = ESI bit in CAN FD format transmitted recessive<br>**Note:**The ESI bit of the transmit buffer is or'ed with the<br>error passive flag to decide the value of the ESI bit in the<br>transmitted CAN FD frame. As required by the CAN FD<br>protocol specification, an error active node may optionally<br>transmit the ESI bit recessive, but an error passive node will<br>always transmit the ESI bit recessive.|
||30<br>XTD<br>Extended Identifier<br>•<br>0h = 11-bit standard identifier<br>•<br>1h = 29-bit extended identifier|
||29<br>RTR<br>Remote Transmission Request<br>•<br>0h = Transmit data frame<br>•<br>1h = Transmit remote frame<br>**Note:**When RTR = 1, the MCAN module transmits a<br>remote frame according to ISO11898-1:2015, even if the<br>MCAN_CCCR[8] FDOE bit enables the transmission in CAN<br>FD format.|
||28-0<br>ID[28-0]<br>Identifier<br>Standard or extended identifier depending on XTD bit. A<br>standard identifier has to be written to ID[28-18].|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1536 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-217. Tx Buffer Element Field Descriptions (continued)** 

|**Word**|**Bits**<br>**Field Name**<br>**Description**|
|---|---|
|T1|31-24<br>MM[7-0]<br>Message Marker<br>Written by Host CPU during Tx Buffer configuration. Copied into<br>Tx Event FIFO element for identification of Tx message status<br>(see also MM[7-0] field inTable 13-218).|
||23<br>EFC<br>Event FIFO Control<br>•<br>0h = Don't store Tx events<br>•<br>1h = Store Tx events|
||22<br>RES<br>Reserved|
||21<br>FDF<br>FD Format<br>•<br>0h = Frame transmitted in Classic CAN format<br>•<br>1h = Frame transmitted in CAN FD format|
||20<br>BRS<br>Bit Rate Switch<br>•<br>0h = CAN FD frames transmitted without bit rate switching<br>•<br>1h = CAN FD frames transmitted with bit rate switching<br>**Note:**ESI, FDF, and BRS bits are only evaluated when CAN<br>FD operation is enabled vie the MCAN_CCCR[8] FDOE bit.<br>BRS bit is only evaluated when in addition the MCAN_CCCR[9]<br>BRSE = 1.|
||19-16<br>DLC[3-0]<br>Data Length Code<br>•<br>0h-8h (0-8) = CAN + CAN FD: transmit frame has 0-8 data<br>bytes<br>•<br>9h-Fh (9-15) = CAN: transmit frame has 8 data bytes<br>•<br>9h-Fh (9-15) = CAN FD: transmit frame has<br>12/16/20/24/32/48/64 data bytes|
||15-0<br>RES<br>Reserved|
|T2|31-24<br>DB3[7-0]<br>Data Byte 3|
||23-16<br>DB2[7-0]<br>Data Byte 2|
||15-8<br>DB1[7-0]<br>Data Byte 1|
||7-0<br>DB0[7-0]<br>Data Byte 0|
|T3|31-24<br>DB7[7-0]<br>Data Byte 7|
||23-16<br>DB6[7-0]<br>Data Byte 6|
||15-8<br>DB5[7-0]<br>Data Byte 5|
||7-0<br>DB4[7-0]<br>Data Byte 4|
|...|...<br>...<br>...|
|Tn|31-24<br>DBm[7-0]<br>Data Byte m|
||23-16<br>DBm-1[7-0]<br>Data Byte m-1|
||15-8<br>DBm-2[7-0]<br>Data Byte m-2|
||7-0<br>DBm-3[7-0]<br>Data Byte m-3|



**Note:** Depending on the configuration of the element size (MCAN_TXESC), between two and sixteen 32-bit words (Tn = 3-17) are used for storage of a CAN message's data field. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1537 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.1.4.10.4 Tx Event FIFO Element**_ 

Each element stores information about transmitted messages. By reading the Tx Event FIFO the Host CPU gets this information in the order the messages were transmitted. Status information about the Tx Event FIFO can be obtained from the MCAN_TXEFS register. 

Figure 13-182 shows Tx Event FIFO element structure. 

**==> picture [296 x 73] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24 23 16 15 8 7 0<br>E0 ID[28-0]<br>E1 MM[7-0] DLC[3-0] TXTS[15-0]<br>mcan-018<br>ESI XTD RTR<br>ET[1-0] FDF BRS<br>**----- End of picture text -----**<br>


**Figure 13-182. Tx Event FIFO Element Structure** 

Table 13-218 shows Tx Event FIFO element field descriptions. 

**Table 13-218. Tx Event FIFO Element Field Descriptions** 

|**Word**|**Bits**<br>**Field Name**<br>**Description**|
|---|---|
|E0|31<br>ESI<br>Error State Indicator<br>•<br>0h = Transmitting node is error active<br>•<br>1h = Transmitting node is error passive|
||30<br>XTD<br>Extended Identifier<br>•<br>0h = 11-bit standard identifier<br>•<br>1h = 29-bit extended identifier|
||29<br>RTR<br>Remote Transmission Request<br>•<br>0h = Data frame transmitted<br>•<br>1h = Remote frame transmitted|
||28-0<br>ID[28-0]<br>Identifier<br>Standard or extended identifier depending on XTD bit. A<br>standard identifier has to be written to ID[28-18].|



1538 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-218. Tx Event FIFO Element Field Descriptions (continued)** 

|**Word**|**Bits**<br>**Field Name**<br>**Description**|
|---|---|
|E1|31-24<br>MM[7-0]<br>Message Marker<br>Copied from Tx Buffer into Tx Event FIFO element for<br>identification of Tx message status (see also MM[7-0] field in<br>Table 13-217).|
||23-22<br>ET[1-0]<br>Event Type<br>•<br>0h = Reserved<br>•<br>1h = Tx event<br>•<br>2h = Transmission in spite of cancellation (always set for<br>transmissions in DAR mode)<br>•<br>3h = Reserved|
||21<br>FDF<br>FD Format<br>•<br>0h = Standard frame format<br>•<br>1h = CAN FD frame format (new DLC-coding and CRC)|
||20<br>BRS<br>Bit Rate Switch<br>•<br>0h = Frame transmitted without bit rate switching<br>•<br>1h = Frame transmitted with bit rate switching|
||19-16<br>DLC[3-0]<br>Data Length Code<br>•<br>0h-8h (0-8) = CAN + CAN FD: frame with 0-8 data bytes<br>transmitted<br>•<br>9h-Fh (9-15) = CAN: frame with 8 data bytes transmitted<br>•<br>9h-Fh (9-15) = CAN FD: frame with 12/16/20/24/32/48/64<br>data bytes transmitted|
||15-0<br>TXTS[15-0]<br>Tx Timestamp<br>Timestamp Counter value captured on start of frame<br>transmission. Resolution depending on configuration of the<br>Timestamp Counter Prescaler MCAN_TSCC[19-16] TCP field.|



## _**13.4.1.4.10.5 Standard Message ID Filter Element**_ 

Up to 128 filter elements can be configured for 11-bit standard IDs. When accessing a Standard Message ID Filter element, its address is the Filter List Standard Start Address MCAN_SIDFC[15-2] FLSSA field plus the index of the filter element (0-127). 

Figure 13-183 shows Standard Message ID Filter element structure. 

**==> picture [298 x 46] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24 23 16 15 8 7 0<br>S0 RES SFID2[10-0]<br>mcan-019<br>SFEC[2-0] SFID1[10-0]<br>SFT[1-0]<br>**----- End of picture text -----**<br>


**Figure 13-183. Standard Message ID Filter Element Structure** 

Table 13-219 shows Standard Message ID Filter element field descriptions. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1539 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-219. Standard Message ID Filter Element Field Descriptions** 

|**Word**|**Bits**|**Field Name**<br>**Description**|
|---|---|---|
|S0|31-30|SFT[1-0]<br>Standard Filter Type<br>•<br>0h = Range filter from SFID1 to SFID2 (SFID2 ≥ SFID1)<br>•<br>1h = Dual ID filter for SFID1 or SFID2<br>•<br>2h = Classic filter: SFID1 = filter; SFID2 = mask<br>•<br>3h = Filter element disabled<br>**Note:**With SFT = 11 the filter element is disabled and the<br>acceptance filtering continues (same behaviour as with SFEC =<br>000)|
||29-27|SFEC[2-0]<br>Standard Filter Element Configuration<br>All enabled filter elements are used for acceptance filtering of<br>standard frames. Acceptance filtering stops at the first matching<br>enabled filter element or when the end of the filter list is<br>reached. If SFEC = 100, 101, or 110 a match sets interrupt flag<br>MCAN_IR[8]HPM and, if enabled, an interrupt is generated. In<br>this case the MCAN_HPMS register is updated with the status<br>of the priority match.<br>•<br>0h = Disable filter element<br>•<br>1h = Store in Rx FIFO 0 if filter matches<br>•<br>2h = Store in Rx FIFO 1 if filter matches<br>•<br>3h = Reject ID if filter matches<br>•<br>4h = Set priority if filter matches<br>•<br>5h = Set priority and store in FIFO 0 if filter matches<br>•<br>6h = Set priority and store in FIFO 1 if filter matches<br>•<br>7h = Store into Rx Buffer , configuration of SFT[1-0] ignored|
||26-16|SFID1[10-0]<br>Standard Filter ID 1<br>When filtering for Rx Buffers this field defines the ID of a<br>standard message to be stored. The received identifiers must<br>match exactly, no masking mechanism is used.|
||15-11|RES<br>Reserved|
||10-0|SFID2[10-0]<br>Standard Filter ID 2<br>This bit field has a different meaning depending on the<br>configuration of SFEC:<br>•<br>1) SFEC = 001 - 110 Second ID of standard ID filter<br>element<br>•<br>2) SFEC = 111 Filter for Rx Buffers|
|||SFID2[10-9]<br>This field is decides whether the received message is stored<br>into an Rx Buffer or treated as message A, B, or C of the debug<br>message sequence.<br>•<br>0h = Store message into an Rx Buffer<br>•<br>1h = Debug Message A<br>•<br>2h = Debug Message B<br>•<br>3h = Debug Message C<br>**Note:**Debug feature is not supported.|
|||SFID2[8-6]<br>This field is used to control the filter event pins at the<br>Extension Interface. A one at the respective bit position enables<br>generation of a pulse at the related filter event pin with the<br>duration of one MCAN_ICKL period in case the filter matches.<br>**Note:**Only three filter event pins are supported.|
|||This field defines the offset to the Rx Buffer Start Address<br>|
|~~SFID2[5-0]~~<br>~~MCAN~~_~~RXBC[15-2] RBSA field for storage of a matching~~<br>message.<br>1540<br>_AM263P Technical Reference Manual_<br>SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025<br>_Submit Document Feedback_<br>|||
|Copyright © 2025 Texas Instru~~m~~ents Incorporated|||



www.ti.com 

_Peripherals_ 

## _**13.4.1.4.10.6 Extended Message ID Filter Element**_ 

Up to 64 filter elements can be configured for 29-bit extended IDs. When accessing an Extended Message ID Filter element, its address is the Filter List Extended Start Address MCAN_XIDFC[15-2] FLESA field plus two times the index of the filter element (0-63). 

Figure 13-184 shows Extended Message ID Filter element structure. 

||31<br>24|31<br>24|31<br>24|23<br>16|15<br>8|7<br>0|
|---|---|---|---|---|---|---|
|F0|EFEC[2-0]||EFID1[28-0]||||
|F1|EFT[1-0]|RES|EFID2[28-0]||||
|mcan-020|||||||



**Figure 13-184. Extended Message ID Filter Element Structure** 

Table 13-220 shows Extended Message ID Filter element field descriptions. 

**Table 13-220. Extended Message ID Filter Element Field Descriptions** 

|**Word**|**Bits**<br>**Field Name**<br>**Description**|
|---|---|
|F0|31-29<br>EFEC[2-0]<br>Extended Filter Element Configuration<br>All enabled filter elements are used for acceptance filtering<br>of extended frames. Acceptance filtering stops at the first<br>matching enabled filter element or when the end of the filter list<br>is reached. If EFEC = 100, 101, or 110 a match sets interrupt<br>flag MCAN_IR[8]HPM and, if enabled, an interrupt is generated.<br>In this case the MCAN_HPMS register is updated with the<br>status of the priority match.<br>•<br>0h = Disable filter element<br>•<br>1h = Store in Rx FIFO 0 if filter matches<br>•<br>2h = Store in Rx FIFO 1 if filter matches<br>•<br>3h = Reject ID if filter matches<br>•<br>4h = Set priority if filter matches<br>•<br>5h = Set priority and store in FIFO 0 if filter matches<br>•<br>6h = Set priority and store in FIFO 1 if filter matches<br>•<br>7h = Store into Rx Buffer or as debug message,<br>configuration of EFT[1-0] ignored|
||28-0<br>EFID1[28-0]<br>Extended Filter ID 1<br>First ID of extended ID filter element.<br>When filtering for Rx Buffers this field defines the ID of an<br>extended message to be stored. The received identifiers must<br>match exactly, only XIDAM masking mechanism (seeSection<br>13.4.1.4.7.1.5,_Extended Message ID Filtering_) is used.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1541 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-220. Extended Message ID Filter Element Field Descriptions (continued)** 

|**Word**|**Bits**|**Field Name**<br>**Description**|
|---|---|---|
|F1|31-30|EFT[1-0]<br>Extended Filter Type<br>•<br>0h = Range filter from EFID1 to EFID2 (EFID2 ≥ EFID1)<br>•<br>1h = Dual ID filter for EFID1 or EFID2<br>•<br>2h = Classic filter: EFID1 = filter, EFID2 = mask<br>•<br>3h = Range filter from EFID1 to EFID2 (EFID2 ≥ EFID1),<br>XIDAM mask not applied|
||29|RES<br>Reserved|
||28-0|EFID2[28-0]<br>Extended Filter ID 2<br>This bit field has a different meaning depending on the<br>configuration of EFEC:<br>•<br>1) EFEC = 001 - 110 Second ID of extended ID filter<br>element<br>•<br>2) EFEC = 111 Filter for Rx Buffers|
|||EFID2[10-9]<br>This field decides whether the received message is stored into<br>an Rx Buffer or treated as message A, B, or C of the debug<br>message sequence.<br>•<br>0h = Store message into an Rx Buffer<br>•<br>1h = Debug Message A<br>•<br>2h = Debug Message B<br>•<br>3h = Debug Message C<br>**Note:**Debug feature is not supported.|
|||EFID2[8-6]<br>This field is used to control the filter event pins at the<br>Extension Interface. A one at the respective bit position enables<br>generation of a pulse at the related filter event pin with the<br>duration of one MCAN_ICKL period in case the filter matches.<br>**Note:**Only three filter event pins are supported.|
|||EFID2[5-0]<br>This field defines the offset to the Rx Buffer Start Address<br>MCAN_RXBC[15-2] RBSA field for storage of a matching<br>message.|



1542 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.4.1.5 MCAN Programming Guide** 

## **Driver Information** 

Driver features are available at the MCAN driver page 

## **Software API Information** 

The MCAN driver provides an API to configure the MCAN module. Full documentation is located on APIs for MCAN 

## **Example Usage** 

The below links shows an example on how to use MCAN 

- MCAN: 

   - MCAN External Read/Write 

   - MCAN Loopback (Interrupt-based) 

   - MCAN Loopback (Polling-based) 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1543 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.2 Local Interconnect Network (LIN)**_ 

This chapter describes the local interconnect network (LIN) module. This module can also operate as a serial communications interface (SCI) port when configured in SCI/UART mode. However, since the LIN module uses a different register/bit structure, code written for this module cannot be directly ported to the standalone SCI module or vice versa. 

## **13.4.2.1 LIN Overview** 

The LIN module is compliant to the LIN2.1 standard in the _LIN Specification Package_ . This standard is based on the UART serial protocol. The protocol involves a single commander and one or moreresponder nodes with a message identification for multicast transmission between any network nodes. 

Section 13.4.2.3 explains how the LIN module operates in SCI mode, while Section 13.4.2.4 explains how the LIN module operates in LIN mode. The register descriptions specify which register fields are applicable for each mode. 

1544 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.1.1 SCI Mode Features**_ 

When operating in SCI mode, the LIN module includes the following features: 

- Standard universal asynchronous receiver-transmitter (UART) communication 

- Supports full-duplex or half-duplex operation 

- Standard non-return-to-zero (NRZ) format 

- Double-buffered receive and transmit functions 

- Supports two individually enabled interrupt lines: level 0 and level 1 

- Configurable frame format of three to thirteen bits per character based on the following: 

   - One start bit 

   - Data word length programmable from one to eight bits 

   - Additional address bit in address-bit mode 

   - Parity programmable for zero or one parity bit, odd or even parity 

   - Stop programmable for one or two stop bits 

- Asynchronous communication mode 

- Two multiprocessor communication formats allow communication between more than two devices 

- Sleep and wake-up functions for multiprocessor communication 

- Programmable divider to support up to 2[24] different baud rates 

- Capability to use Direct Memory Access (DMA) to transmit and receive data 

- Error and status flags to provide detailed information about SCI events 

- Multibuffer mode for receive and transmit 

## **Note** 

In SCI mode, the LIN module is functionally compatible with the C2000™ SCI module, but not software compatible due to different register definitions. 

The LIN module does not support UART hardware flow control. This feature can be implemented in software using a general-purpose I/O pin. 

The LIN module does not support isosynchronous mode as there is no SCICLK pin. 

## _**13.4.2.1.2 LIN Mode Features**_ 

When operating in LIN mode, the LIN module includes the following features: 

- Compatibility with LIN 1.3 , 2.0, and 2.1 protocols 

- Configurable baud rate up to 20kbps 

- Two external pins: LINRX and LINTX. 

- Multibuffered receive and transmit units 

- Identification masks for message filtering 

- Automatic commander header generation 

   - Programmable synchronization break field 

   - Synchronization field 

   - Identifier field 

- Responder Automatic Synchronization 

   - Synchronization break detection 

   - Optional baud rate update 

   - Synchronization validation 

- 2[31] programmable transmission rates with 7 fractional bits 

- Wakeup on LINRX active level from transceiver 

- Automatic wake-up support 

   - LINTX wake-up signal generation 

   - Wake-up signal timeout 

- Automatic idle bus detection 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1545 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- Error detection 

   - Bit error 

   - Bus error 

   - No-response error 

   - Checksum error 

   - Synchronization field error 

   - Parity error 

- Capability to use Direct Memory Access (DMA) to transmit and receive data. 

- 2 interrupt lines (INT0 and INT1) with user-configurable interrupt sources: 

   - Receive 

   - Transmit 

   - ID, error, and status 

- Support for LIN 2.0 checksum 

- Enhanced synchronizer finite state machine (FSM) support for frame processing 

- Enhanced handling of extended frames 

- Enhanced baud rate generator 

1546 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.1.3 Block Diagram**_ 

The LIN module is based on the SCI module with added sub-blocks to support LIN protocol. 

The three major components of the SCI block are: 

- **Transmitter** (TX) contains two major registers to perform the double-buffering: 

   - The transmitter data buffer register (SCITD) contains data loaded by the CPU to be transferred to the shift register for transmission. 

   - The transmitter shift register (SCITXSHF) loads data from the data buffer (SCITD) and shifts data onto the LINTX pin, one bit at a time. 

- **Baud Clock Generator** 

   - A programmable baud generator produces a baud clock scaled from the input clock VCLK 

   - LIN VCLK is based on the SYSCLK frequency. VCLK input from SYSCLK and can be divided by 1, 2, or 4 using the CLK_CFG_REGS PERCLKDIVSEL.LINxCLKDIV field for each LIN module individually. By default, VCLK input is SYSCLK divided by 2 

- **Receiver** (RX) contains two major registers to perform the double-buffering: 

   - The receiver shift register (SCIRXSHF) shifts data in from the LINRX pin one bit at a time and transfers completed data into the receive data buffer. 

   - The receiver data buffer register (SCIRD) contains received data transferred from the receiver shift register 

There are separate enable and interrupt bits for the LIN receiver and transmitter. The receiver and transmitter can each be operated independently (half-duplex) or simultaneously (full duplex). 

To maintain data integrity, the LIN checks the received data for breaks, parity, overrun, and framing errors. The baud rate (bits per second) is programmable to over 16 million different rates through a 24-bit baud-select register. Figure 13-185 shows the detailed diagram of the SCI block. 

The LIN module is based on the SCI module with the addition of an error detector (parity calculator, checksum calculator, and bit monitor), a mask filter, a synchronizer, and a multibuffered receiver and transmitter. The SCI interface, and the baud generator are modified for compatibility with the LIN standard. Figure 13-186 shows the LIN block diagram. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1547 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [441 x 461] intentionally omitted <==**

**----- Start of picture text -----**<br>
TRANSMITTER<br>SCITXSHF<br>Address bit [†] Shift register<br>TX EMPTY LINTX<br>SCIFLR.11<br>1<br>8<br>TXRDY<br>TX INT ENA<br>SCIFLR.8 TX INT<br>SCISETINT.8<br>TXWAKE Transmit buffer TXENA<br>SCIFLR.10 SCITD SCIGCR1.25<br>VCLK Baud clock<br>Peripheral generator<br>CLOCK<br>SCIGCR1.5<br>SCI<br>Baud rate<br>registers<br>SCIBAUD<br>RECEIVER<br>SCIRXSHF<br>Shift register<br>LINRX<br>BRKDT ERR INT<br>BRKDT INT ENA<br>SCIFLR.0<br>SCISETINT.0<br>RXENA<br>SCIGCR1.24 WAKEUP<br>WAKEUP INT ENA<br>SCIFLR.1<br>SCISETINT.1<br>PE OE  FE<br>8 SCIFLR24:26<br>RXWAKE Receive buffer RXRDY RX INT<br>RX INT ENA<br>SCIFLR.12 SCIRD SCIFLR.9 SCISETINT.9<br>**----- End of picture text -----**<br>


**Figure 13-185. SCI Block** 

1548 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [408 x 436] intentionally omitted <==**

**Figure 13-186. LIN Block Diagram** 

## **13.4.2.2 LIN Integration** 

There are 5x LIN modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1549 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [447 x 310] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>LIN#<br>LIN#_VBUSCLK LIN#_TX_DMA_REQ<br>EDMA<br>LIN#_RX_DMA_REQ<br>SYS_CLK<br>XTALCLK<br>EXT_REFCLK<br>PER_PLL_HSDIV0_CLKOUT1<br>÷   LIN#_CLK LIN#_TXD<br>CORE_PLL_HSDIV0_CLKOUT0<br>RCOSC (10MHz)<br>XTALCLK<br>LIN#_RXD<br>PER_PLL_HSDIV0_CLKOUT0<br>RCM ICSSM<br>LIN#_UART#_CLKSRC_SEL Bit<br>LIN#_UART#_CLKDIV_SEL Bit<br>LIN#_INT_REQ[1:0] R5FSS0-CORE0<br>LIN#_RST_CTRL Bit<br>R5FSS0-CORE1<br>R5FSS1-CORE0<br>LIN#_WARMRESET<br>Warm Reset Sources R5FSS1-CORE1<br>PERI INTERCONNECT<br>ICSSM XBAR<br>DMA  XBAR<br>**----- End of picture text -----**<br>


**Figure 13-187. LIN Integration** 

# = 0 to 4 

The tables below summarize the device integration details of LIN# (where # = 0 to 5). 

**Table 13-221.** _**LIN**_ **Device Integration** 

This table describes the LIN device integration details. 

|**LIN Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|LIN0|✓|Peripheral VBUSP Interconnect|
|LIN1|✓|Peripheral VBUSP Interconnect|
|LIN2|✓|Peripheral VBUSP Interconnect|
|LIN3|✓|Peripheral VBUSP Interconnect|
|LIN4|✓|Peripheral VBUSP Interconnect|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1550 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-222.** _**LIN**_ **Clocks** 

This table describes the LIN clocking signals. 

|**LIN**<br>**Instance**|**LIN Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|LIN0|LIN0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|LIN0 Interface Clock<br>(LIN0_CLK must be<br>running for register access)|
||LIN0_FCLK<br>(LIN_CLK)|XTALCLK|External XTAL|25 MHz|LIN0 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||
|LIN1|LIN1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|LIN1 Interface Clock<br>(LIN1_CLK must be<br>running for register access)|
||LIN1_FCLK<br>(LIN_CLK)|XTALCLK|External XTAL|25 MHz|LIN1 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1551 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-222.** _**LIN**_ **Clocks (continued)** 

This table describes the LIN clocking signals. 

|**LIN**<br>**Instance**|**LIN Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|LIN2|LIN2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|LIN2 Interface Clock<br>(LIN2_CLK must be<br>running for register access)|
||LIN2_FCLK<br>(LIN_CLK)|XTALCLK|External XTAL|25 MHz|LIN2 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||
|LIN3|LIN3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|LIN3 Interface Clock<br>(LIN3_CLK must be<br>running for register access)|
||LIN3_FCLK<br>(LIN_CLK)|XTALCLK|External XTAL|25 MHz|LIN3 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



1552 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-222.** _**LIN**_ **Clocks (continued)** 

This table describes the LIN clocking signals. 

|**LIN**<br>**Instance**|**LIN Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|LIN4|LIN4_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|LIN4 Interface Clock<br>(LIN4_CLK must be<br>running for register access)|
||LIN4_FCLK<br>(LIN_CLK)|XTALCLK|External XTAL|25 MHz|LIN4 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



**Table 13-223.** _**LIN**_ **Resets** 

This table describes the LIN reset signals. 

|**LIN**<br>**Instance**|**LIN Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|LIN0|LIN0_RST<br>(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|LIN0 Asynchronous Reset|
|LIN1|LIN1_RST<br>(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|LIN1 Asynchronous Reset|
|LIN2|LIN2_RST<br>(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|LIN2 Asynchronous Reset|
|LIN3|LIN3_RST<br>(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|LIN3 Asynchronous Reset|
|LIN4|LIN4_RST<br>(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|LIN4 Asynchronous Reset|



**Table 13-224.** _**LIN**_ **Interrupt Requests** 

This table describes the LIN interrupt requests. 

|**LIN Instance**|**LIN Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|LIN0|LIN0_INT_req_0<br>|LIN0_INT_req_0|ALL R5FSS<br>Cores, PRU-<br>ICSS BAR|Pulse|LIN0 Event Interrupts|
||LIN0_INT_req_1<br>|LIN0_INT_req_1||||
|LIN1|LIN1_INT_req_0<br>|LIN1_INT_req_0|ALL R5FSS<br>Cores, PRU-<br>ICSS XBAR|Pulse|LIN1 Event Interrupts|
||LIN1_INT_req_1<br>|LIN1_INT_req_1||||
|LIN2|LIN2_INT_req_0<br>|LIN2_INT_req_0|ALL R5FSS<br>Cores, PRU-<br>ICSS XBAR|Pulse|LIN2 Event Interrupts|
||LIN2_INT_req_1<br>|LIN2_INT_req_1||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1553 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-224.** _**LIN**_ **Interrupt Requests (continued)** 

This table describes the LIN interrupt requests. 

|**LIN Instance**|**LIN Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|LIN3|LIN3_INT_req_0|LIN3_INT_req_0|ALL R5FSS<br>Cores, PRU-<br>ICSS XBAR|Pulse|LIN3 Event Interrupts|
||LIN3_INT_req_1|LIN3_INT_req_1||||
|LIN4|LIN4_INT_req_0|LIN4_INT_req_0|ALL R5FSS<br>Cores, PRU-<br>ICSS XBAR|Pulse|LIN4 Event Interrupts|
||LIN4_INT_req_1|LIN4_INT_req_1||||



**Table 13-225.** _**LIN**_ **DMA Requests** 

## This table describes the LIN DMA requests. 

|**LIN**<br>**Instance**|**LIN DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|LIN0|LIN0_TX_DMA_REQ|LIN0_tx_dma_req|EDMA Crossbar<br>(DMA_XBAR)|Pulse|LIN0 TX DMA Request|
||LIN0_RX_DMA_REQ|LIN0_rx_dma_req|||LIN0 RX DMA Request|
|LIN1|LIN1_TX_DMA_REQ|LIN1_tx_dma_req|EDMA Crossbar<br>(DMA_XBAR)|Pulse|LIN1 TX DMA Request|
||LIN1_RX_DMA_REQ|LIN1_rx_dma_req|||LIN1 RX DMA Request|
|LIN2|LIN2_TX_DMA_REQ|LIN2_tx_dma_req|EDMA Crossbar<br>(DMA_XBAR)|Pulse|LIN2 TX DMA Request|
||LIN2_RX_DMA_REQ|LIN2_rx_dma_req|||LIN2 RX DMA Request|
|LIN3|LIN3_TX_DMA_REQ|LIN3_tx_dma_req|EDMA Crossbar<br>(DMA_XBAR)|Pulse|LIN3 TX DMA Request|
||LIN3_RX_DMA_REQ|LIN3_rx_dma_req|||LIN3 RX DMA Request|
|LIN4|LIN4_TX_DMA_REQ|LIN4_tx_dma_req|EDMA Crossbar<br>(DMA_XBAR)|Pulse|LIN4 TX DMA Request|
||LIN4_RX_DMA_REQ|LIN4_rx_dma_req|||LIN4 RX DMA Request|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

1554 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.4.2.3 Serial Communications Interface Module** 

## _**13.4.2.3.1 SCI Communication Formats**_ 

The SCI module can be configured to meet the requirements of many applications. Because communication formats vary depending on the specific application, many attributes of the SCI/LIN are user configurable. The configuration options are: 

- SCI Frame format 

- SCI Timing modes 

- SCI Baud rate 

- SCI Multiprocessor modes 

## _**13.4.2.3.1.1 SCI Frame Formats**_ 

The SCI uses a programmable frame format. All frames consist of the following: 

- One start bit 

- One to eight data bits 

- Zero or one address bit 

- Zero or one parity bit 

- One or two stop bits 

The frame format for both the transmitter and receiver is programmable through the bits in the SCIGCR1 register. Both receive and transmit data is in nonreturn to zero (NRZ) format, which means that the transmit and receive lines are at logic high when idle. Each frame transmission begins with a start bit, in which the transmitter pulls the SCI line low (logic low). Following the start bit, the frame data is sent and received least significant bit first (LSB). 

An address bit is present in each frame if the SCI is configured to be in address-bit mode but is not present in any frame if the SCI is configured for idle-line mode. The format of frames with and without the address bit is illustrated in Figure 13-188. 

A parity bit is present in every frame when the PARITY ENA bit is set. The value of the parity bit depends on the number of one bits in the frame and whether odd or even parity has been selected using the PARITY ENA bit. Both examples in Figure 13-188 have parity enabled. 

All frames include one stop bit, which is always a high level. This high level at the end of each frame is used to indicate the end of a frame to make sure synchronization between communicating devices. Two stop bits are transmitted, if the STOP bit in SCIGCR1 register is set. The examples shown in Figure 13-188 use one stop bit per frame. 

**==> picture [423 x 142] intentionally omitted <==**

**----- Start of picture text -----**<br>
Idle-line mode<br>0 7<br>Start 1 2 3 4 5 6 Parity Stop<br>(LSBit) (MSBit)<br>Address bit mode<br>0 7<br>Start 1 2 3 4 5 6 Addr Parity Stop<br>(LSBit) (MSBit)<br>Address bit<br>**----- End of picture text -----**<br>


**Figure 13-188. Typical SCI Data Frame Formats** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1555 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.2.3.1.2 SCI Asynchronous Timing Mode**_ 

The SCI can be configured to use the asynchronous timing mode using TIMINGMODE bit in SCIGCR1 register. 

The asynchronous timing mode uses the receive and transmit data lines to interface with devices using the standard universal asynchronous receiver- transmitter (UART) protocol. 

In the asynchronous timing mode, each bit in a frame has a duration of 16 SCI baud clock period (16 samples). When the SCI is using asynchronous mode, the baud rates of all communicating devices must match as closely as possible. Receive errors result from devices communicating at different baud rates. 

With the receiver in the asynchronous timing mode, the SCI detects a valid start bit if the first four samples after a falling edge on the LINRX pin are of logic level 0. As soon as a falling edge is detected on LINRX, the SCI assumes that a frame is being received and synchronizes to the bus. 

To prevent interpreting noise as Start bit SCI expects LINRX line to be low for at least four contiguous SCI baud clock periods to detect a valid start bit. The bus is considered idle if this condition is not met. When a valid start bit is detected, the SCI determines the value of each bit by sampling the LINRX line value during the seventh, eighth, and ninth SCI baud clock periods. A majority vote of these three samples is used to determine the value stored in the SCI receiver shift register. By sampling in the middle of the bit, the SCI reduces errors caused by propagation delays and rise and fall times and data line noises. Figure 13-189 illustrates how the receiver samples a start bit and a data bit in asynchronous timing mode. 

The transmitter transmits each bit for a duration of 16 SCI baud clock periods. During the first clock period for a bit, the transmitter shifts the value of that bit onto the LINTX pin. The transmitter then holds the current bit value on LINTX for 16 SCI baud clock periods. 

**==> picture [420 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
Falling edge Majority<br>vote<br>detected<br>1  2  3  4  5  6  7  8  9 10 11 1213 14 15 16 1 2 3 4 5 6  7  8  9 10 11 12 13 14 15 161 2 3 4 5<br>LINRX<br>Start bit LSB of data<br>16 SCI baud clock periods/bit<br>**----- End of picture text -----**<br>


**Figure 13-189. Asynchronous Communication Bit Timing** 

1556 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.3.1.3 SCI Baud Rate**_ 

The SCI/LIN has an internally generated serial clock determined by the peripheral VCLK and the prescalers P and M in this register. The SCI uses the 24-bit integer prescaler P value in the BRS register to select the required baud rates. The additional 4-bit fractional divider M refines the baud rate selection. 

In asynchronous timing mode, the SCI generates a baud clock according to the following formula: 

_SCICLK Frequency_ = --------------------------------------------------VCLK Frequency **-** P + 1 + ----M **-** 16 _Asynchronous baud value_ = SCICLK--------------------------------------------------------Frequency **-** 16 

For P = 0, 

_Asynchronous baud value_ = VCLK-----------------------------------------------Frequency **-** 32 

## _**13.4.2.3.1.4 SCI Multiprocessor Communication Modes**_ 

In some applications, the SCI can be connected to more than one serial communication device. In such a multiprocessor configuration, several frames of data can be sent to all connected devices or to an individual device. In the case of data sent to an individual device, the receiving devices must determine when the devices are being addressed. When a message is not intended for them, the devices can ignore the following data. When only two devices make up the SCI network, addressing is not needed, so multiprocessor communication schemes are not required. 

SCI supports two multiprocessor communication modes which can be selected using COMM MODE bit: 

- Idle-Line Mode 

- Address Bit Mode 

When the SCI is not used in a multiprocessor environment, software can consider all frames as data frames. In this case, the only distinction between the idle-line and address-bit modes is the presence of an extra bit (the address bit) in each frame sent with the address-bit protocol. 

The SCI allows full-duplex communication where data can be sent and received using the transmit and receive pins simultaneously. However, the protocol used by the SCI assumes that only one device transmits data on the same bus line at any one time. No arbitration is done by the SCI. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1557 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.2.3.1.4.1 Idle-Line Multiprocessor Modes**_ 

In idle-line multiprocessor mode, a frame that is preceded by an idle period (10 or more idle bits) is an address frame. A frame that is preceded by fewer than 10 idle bits is a data frame. Figure 13-190 illustrates the format of several blocks and frames with idle-line mode. 

There are two ways to transmit an address frame using idle-line mode: 

**Method 1:** In software, deliberately leave an idle period between the transmission of the last data frame of the previous block and the address frame of the new block. 

**Method 2:** Configure the SCI to automatically send an idle period between the last data frame of the previous block and the address frame of the new block. 

Although Method 1 is only accomplished by a delay loop in software, Method 2 can be implemented by using the transmit buffer and the TXWAKE bit in the following manner: 

Step 1: Write a 1 to the TXWAKE bit. 

Step 2: Write a dummy data value to the SCITD register. This triggers the SCI to begin the idle period as soon as the transmitter shift register is empty. 

Step 3: Wait for the SCI to clear the TXWAKE flag. 

Step 4: Write the address value to SCITD. 

As indicated by Step 3, software can wait for the SCI to clear the TXWAKE bit. However, the SCI clears the TXWAKE bit at the same time the SCI sets TXRDY (that is, transfers data from SCITD into SCITXSHF). Therefore, if the TX INT ENA bit is set, the transfer of data from SCITD to SCITXSHF causes an interrupt to be generated at the same time that the SCI clears the TXWAKE bit. If this interrupt method is used, software is not required to poll the TXWAKE bit waiting for the SCI to clear the bit. 

When idle-line multiprocessor communications are used, software must make sure that the idle time exceeds 10 bit periods before addresses (using one of the methods mentioned above), and software must also make sure that data frames are written to the transmitter quickly enough to be sent without a delay of 10 bit periods between frames. Failure to comply with these conditions results in data interpretation errors by other devices receiving the transmission. 

**==> picture [418 x 180] intentionally omitted <==**

**----- Start of picture text -----**<br>
Blocks of frames<br>Blocks separated by 10 or more idle bits<br>Data format<br>(pins LINRX,<br>LINTX)<br>Data format One block of frames<br>expanded<br>Address Data Last data<br>Idle period Address frame Data frame Fewer than Data frame<br>10 idle bits<br>Start Start Start<br>Parity Stop Parity Stop Parity Stop<br>**----- End of picture text -----**<br>


**Figure 13-190. Idle-Line Multiprocessor Communication Format** 

1558 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.3.1.4.2 Address-Bit Multiprocessor Mode**_ 

In the address-bit protocol, each frame has an extra bit immediately following the data field called an address bit. A frame with the address bit set to 1 is an address frame; a frame with the address bit set to 0 is a data frame. The idle period timing is irrelevant in this mode. Figure 13-191 illustrates the format of several blocks and frames with the address-bit mode. 

When address-bit mode is used, the value of the TXWAKE bit is the value sent as the address bit. To send an address frame, software must set the TXWAKE bit. This bit is cleared as the contents of the SCITD are shifted from the TXWAKE register so that all frames sent are data except when the TXWAKE bit is written as a 1. 

No dummy write to SCITD is required before an address frame is sent in address-bit mode. The first byte written to SCITD after the TXWAKE bit is written to 1 is transmitted with the address bit set when address-bit mode is used. 

**==> picture [416 x 189] intentionally omitted <==**

**----- Start of picture text -----**<br>
Several blocks of frames<br>Data format<br>(pins LINRX,<br>LINTX)<br>Idle time is not significant<br>Data format<br>expanded Addr 1 Data 0 Addr 1<br>Address frame Idle time Data frame Idle time Address frame<br>(address bit = 1) is of no (address bit = 0) is of no (address bit = 1)<br>significance significance<br>One bloc k<br>Start Start Start<br>Parity Stop Parity Stop Parity Stop<br>**----- End of picture text -----**<br>


**Figure 13-191. Address-Bit Multiprocessor Communication Format** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1559 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.2.3.1.5 SCI Multibuffered Mode**_ 

To reduce CPU load when receiving or transmitting data in interrupt mode or DMA mode, the SCI/LIN module has eight separate receive and transmit buffers. Multibuffered mode is enabled by setting the MBUF MODE bit. 

The multibuffer 3-bit counter counts the data bytes transferred from the SCIRXSHF register to the RDy receive buffers and TDy transmit buffers register to SCITXSHF register. The 3-bit compare register contains the number of data bytes expected to be received or transmitted. the LENGTH value in SCIFORMAT register indicates the expected length and is used to load the 3-bit compare register. 

A receive interrupt (RX interrupt; see the SCIINTVECT0 and SCIINTVECT1 registers), and a receive ready RXRDY flag set in SCIFLR register, as well as a DMA request (RXDMA) can occur after receiving a response if there are no response receive errors for the frame (such as, there is, frame error, and overrun error). 

A transmit interrupt (TX interrupt), and a transmit ready flag (TXRDY flag in SCIFLR register), and a DMA request (TXDMA) can occur after transmitting a response. 

Figure 13-192 and Figure 13-193 show the receive and transmit multibuffer functional block diagram, respectively. 

**==> picture [352 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX 7 0<br>SCIRXSHF<br>CHECKSUM<br>CALCULATOR CE Flag<br>RX DMA Request<br>RX Ready Flag<br>7 0<br>RD0 3-bit<br>7 0 Compare No<br>RD1 Receive<br>7 0 Errors<br>RD2 =<br>7 0 MBUF MODE<br>RD3<br>7 0<br>RD4<br>3-bit<br>7 0 Counter<br>RD5<br>7 0<br>RD6<br>7 0 Not<br>RD7<br>MBUF MODE<br>**----- End of picture text -----**<br>


**Figure 13-192. Receive Buffers** 

1560 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [384 x 290] intentionally omitted <==**

**----- Start of picture text -----**<br>
TX 7 0<br>SCITXSHF<br>CHECKSUM<br>CALCULATOR CE Flag<br>7 TD0 0 3-bit TX Ready Flag<br>7 0 Compare<br>TD1<br>7 0<br>TD2 TX DMA<br>=<br>7 0 MBUF MODE Request<br>TD3<br>7 0<br>TD4<br>3-bit<br>7 0 Counter<br>TD5<br>7 0<br>TD6<br>7 0 Not<br>TD7<br>MBUF MODE<br>**----- End of picture text -----**<br>


**Figure 13-193. Transmit Buffers** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1561 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.2.3.2 SCI Interrupts**_ 

The SCI/LIN module has two interrupt lines, level 0 and level 1, to the vectored interrupt manager (VIM) module (see Figure 13-194). Two offset registers SCIINTVECT0 and SCIINTVECT1 determine which flag triggered the interrupt according to the respective priority encoders. Each interrupt condition has a bit to enable/disable the interrupt in the SCISETINT and SCICLRINT registers, respectively. 

Each interrupt also has a bit that can be set as interrupt level 0(INT0) or as interrupt level 1(INT1). By default, interrupts are in interrupt level 0. SCISETINTLVL sets a given interrupt to level1. SCICLEARINTLVL resets a given interrupt level to the default level 0. 

The interrupt vector registers SCIINTVECT0 and SCIINTVECT1 return the vector of the pending interrupt line INT0 or INT1. If more than one interrupt is pending, the interrupt vector register holds the highest priority interrupt. 

**==> picture [366 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
INT0<br>INT1 Priority Encoder 1 INT 1<br>INT2<br>INT3<br>INT4<br>INT5<br>INT6<br>INT7<br>INT8<br>INT9<br>INT10<br>INT11 Priority Encoder 0 INT 0<br>INT12<br>INT13<br>INT14<br>INT15<br>INT16<br>SCISETINT<br>SCICLRINT<br>SCISETINTL<br>SCICLRL<br>SCIINTFLR<br>SCIINTVECT0<br>SCIINTVECT1<br>**----- End of picture text -----**<br>


**Figure 13-194. General Interrupt Scheme** 

1562 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [351 x 237] intentionally omitted <==**

**----- Start of picture text -----**<br>
Priority 5-bit<br>Encoder 0 INTVECT0<br>...<br>. . .<br>INT0<br>INTx LVL<br>FLAGx<br>ENA INTx<br>INT1<br>...<br>...<br>Priority 5-bit<br>Encoder 1 INTVECT1<br>**----- End of picture text -----**<br>


**Figure 13-195. Interrupt Generation for Given Flags** 

## _**13.4.2.3.2.1 Transmit Interrupt**_ 

To use transmit interrupt functionality, SETTXINT bit must be enabled and SET_TX_DMA bit must be cleared in the SCISETINT register. The transmit ready (TXRDY) flag is set when the SCI transfers the contents of SCITD/TDy to the shift register, SCITXSHF. The TXRDY flag indicates that SCITD/TDy is ready to be loaded with more data. In addition, the SCI sets the TX EMPTY bit if both the SCITD/TDy and SCITXSHF registers are empty. If the SETTXINT bit is set, then a transmit interrupt is generated when the TXRDY flag goes high. The transmit interrupt is not generated immediately after setting the SETTXINT bit unlike the transmit DMA request. The transmit interrupt is generated only after the first transfer from SCITD/TDy to SCITXSHF, that is first data has to be written to SCITD/TDy before any interrupt gets generated. To transmit further data, data can be written to SCITD/TDy in the transmit interrupt service routine. 

Writing data to the SCITD/TDy register clears the TXRDY bit. When this data has been moved to the SCITXSHF register, the TXRDY bit is set again. The interrupt request can be suspended by setting the CLRTXINT bit in the SCICLEARINT register; however, when the SETTXINT bit is again set to 1, the TXRDY interrupt is asserted again. The transmit interrupt request can be eliminated until the next series of values is written to SCITD/TDy, by disabling the transmitter using the TXENA bit, by a software reset SWnRST, or by a device hardware reset. 

## _**13.4.2.3.2.2 Receive Interrupt**_ 

The receive ready (RXRDY) flag is set when the SCI transfers newly received data from SCIRXSHF to SCIRD/ RDy. The RXRDY flag therefore indicates that the SCI has new data to be read. Receive interrupts are enabled by the SETRXINT bit in the SCISETINT register. If the SETRXINT is set when the SCI sets the RXRDY flag, then a receive interrupt is generated. The received data can be read in the Interrupt Service routine. 

On a device with a DMA controller, the SET_RX_DMA bit in the SCISETINT register must be cleared to select interrupt functionality. 

## _**13.4.2.3.2.3 WakeUp Interrupt**_ 

SCI sets the WAKEUP flag if bus activity on the RX line either prevents power-down mode from being entered, or RX line activity causes an exit from power-down mode. If enabled (SCISETINT.SETWAKEUPINT is set), the wakeup interrupt is triggered once the WAKEUP flag in the SCIFLR register is set. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1563 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.2.3.2.4 Error Interrupts**_ 

The following error detections are supported with an interrupt by the SCI module: 

- Parity errors (PE) 

- Frame errors (FE) 

- Break Detect errors (BRKDT) 

- Overrun errors (OE) 

- Bit errors (BE) 

There are 16 interrupt sources in the SCI/LIN module. In SCI mode, 8 interrupts are supported, as listed in Table 13-226. 

If all of these errors (PE, FE, BRKDT, OE, BE) are flagged, an interrupt for the flagged errors is generated if enabled. A message is valid for both the transmitter and the receiver, if there is no error detected until the end of the frame. Each of these flags is located in the receiver status (SCIFLR) register (Table 13-227 and Table 13-228). 

## **Table 13-226. SCI/LIN Interrupts** 

|**Offset**(1)|**Interrupt**|**Applicable to SCI**|**Applicable to LIN**|
|---|---|---|---|
|0|No interrupt|-|-|
|1|Wakeup|Yes|Yes|
|2|Inconsistent-sync-field error (ISFE)|No|Yes|
|3|Parity error (PE)|Yes|Yes|
|4|ID|No|Yes|
|5|Physical bus error (PBE)|No|Yes|
|6|Frame error (FE)|Yes|Yes|
|7|Break detect (BRKDT)|Yes|No|
|8|Checksum error (CE)|No|Yes|
|9|Overrun error (OE)|Yes|Yes|
|10|Bit error (BE)|Yes|Yes|
|11|Receive|Yes|Yes|
|12|Transmit|Yes|Yes|
|13|No-response error (NRE)|No|Yes|
|14|Timeout after wakeup signal (150ms)|No|Yes|
|15|Timeout after three wakeup signals (1.5s)|No|Yes|
|16|Timeout (Bus Idle, 4s)|No|Yes|



(1) Offset 1 is the highest priority. Offset 16 is the lowest priority. 

1564 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Table 13-227. SCI Receiver Status Flags** 

|**SCI Flag**|**Register**|**Bit**|**Value After Reset**(1)|
|---|---|---|---|
|CE|SCIFLR|29|0|
|ISFE|SCIFLR|28|0|
|NRE|SCIFLR|27|0|
|FE|SCIFLR|26|0|
|OE|SCIFLR|25|0|
|PE|SCIFLR|24|0|
|RXWAKE|SCIFLR|12|0|
|RXRDY|SCIFLR|9|0|
|BUSY|SCIFLR|3|0|
|IDLE|SCIFLR|2|1|
|WAKEUP|SCIFLR|1|0|
|BRKDT|SCIFLR|0|0|



(1) The flags are frozen with the reset value while SWnRST = 0. 

## **Table 13-228. SCI Transmitter Status Flags** 

|**SCI Flag**|**Register**|**Bit**|**Value After Reset**(1)|
|---|---|---|---|
|BE|SCIFLR|31|0|
|PBE|SCIFLR|30|0|
|TXWAKE|SCIFLR|10|0|
|TXEMPTY|SCIFLR|11|1|
|TXRDY|SCIFLR|8|1|



(1) The flags are frozen with the reset value while SWnRST = 0. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1565 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.2.3.3 SCI DMA Interface**_ 

DMA requests for receive (RXDMA request) and transmit (TXDMA request) are available for the SCI/LIN module. The DMA must be configured to transfer to/from the SCITD/SCIRD register if multibuffer mode is disabled (MBUFMODE in the SCIGCR1 register is cleared), and to/from the TDy/RDy registers if multibuffer mode is enabled (MBUFMODE in the SCIGCR1 register is set.) 

## _**13.4.2.3.3.1 Receive DMA Requests**_ 

This DMA functionality is enabled/disabled by the CPU using the SETRXDMA/CLRRXDMA bits, respectively. 

In multibuffered SCI mode with DMA enabled, the receiver loads the RDy buffers for each received character. RXDMA request is triggered once the last character of the programmed number of characters (LENGTH) are received and copied to the corresponding RDy buffer successfully. 

If the multibuffer option is disabled, then DMA requests are generated on a byte-per-byte basis. 

In multiprocessor mode, the SCI can generate receiver interrupts for address frames and DMA requests for data frames or DMA requests for both. This is controlled by the SET_RX_DMA_ALL bit. 

In multiprocessor mode with the SLEEP bit set, no DMA request is generated for received data frames. The software must clear the SLEEP bit before data frames can be received. 

## _**13.4.2.3.3.2 Transmit DMA Requests**_ 

DMA functionality is enabled/disabled by the CPU with SET_TX_DMA/CLR_TX_DMA bits, respectively. 

In multibuffered SCI mode once TXRDY bit is set or after a transmission of programmed number of characters (LENGTH) (up to eight data bytes stored in the transmit buffers (TDy) in the LINTD0 and LINTD1 registers), a DMA request is generated to reload the transmit buffer for the next transmission. If the multibuffer option is disabled, then DMA requests are generated on a byte-per-byte basis. 

1566 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.3.4 SCI Configurations**_ 

Before the SCI sends or receives data, the SCI registers can be properly configured. Upon power-up or a system-level reset, each bit in the SCI registers is set to a default state. The registers are writable only after the RESET bit in the SCIGCR0 register is set to 1. Of particular importance is the SWnRST bit in the SCIGCR1 register. The SWnRST is an active-low bit initialized to 0 and keeps the SCI in a reset state until the bit is programmed to 1. Therefore, all SCI configuration can be completed before a 1 is written to the SWnRST bit. 

The following list details the configuration steps that software can perform prior to the transmission or reception of data. As long as the SWnRST bit is cleared to 0 the entire time that the SCI is being configured, the order in which the registers are programmed is not important. 

- Enable SCI by setting the RESET bit to 1. 

- Clear the SWnRST bit to 0 before SCI is configured. 

- Select the desired frame format by programming the SCIGCR1 register. 

- Set both the RX FUNC and TX FUNC bits in SCIPIO0 to 1 to configure the LINRX and LINTX pins for SCI functionality. 

- Select the baud rate to be used for communication by programming the BRS register. 

- Set the CLOCK bit in SCIGCR1 to 1 to select the internal clock. 

- Set the CONT bit in SCIGCR1 to 1 to make SCI not halt for an emulation breakpoint until the current reception or transmission is complete (this bit is used only in an emulation environment). 

- Set the LOOP BACK bit in SCIGCR1 to 1 to connect the transmitter to the receiver internally (this feature is used to perform a self-test). 

- Set the RXENA bit in SCIGCR1 to 1, if data is to be received. 

- Set the TXENA bit in SCIGCR1 to 1, if data is to be transmitted. 

- Set the SWnRST bit to 1 after SCI is configured. 

- Perform receiving or transmitting data (see Section 13.4.2.3.4.1 or Section 13.4.2.3.4.2). 

## _**13.4.2.3.4.1 Receiving Data**_ 

The SCI receiver is enabled to receive messages, if both the RX FUNC bit and the RXENA bit are set to 1. If the RX FUNC bit is not set, the LINRX pin functions as a general-purpose I/O pin rather than as an SCI function pin. 

SCI module can receive data in one of the following modes: 

- Single-Buffer (Normal) Mode 

- Multibuffer Mode 

After a valid idle period is detected, data is automatically received as the data arrives on the LINRX pin. 

## _**13.4.2.3.4.1.1 Receiving Data in Single-Buffer Mode**_ 

Single-buffer mode is selected when the MBUFMODE bit in SCIGCR1 is cleared to 0. In this mode, SCI sets the RXRDY bit when the SCI transfers newly received data from SCIRXSHF to SCIRD. The RXRDY bit is cleared after the new data in SCIRD has been read. Also, as data is transferred from SCIRXSHF to SCIRD, the FE, OE, or PE flags are set if any of these error conditions were detected in the received data. These error conditions are supported with configurable interrupt capability. The wakeup and break-detect status bits are also set if one of these errors occurs, but the bits do not necessarily occur at the same time that new data is being loaded into SCIRD. 

You can receive data by: 

1. Polling the Receive Ready Flag 

2. Receive Interrupt 3. DMA 

In polling method, software can poll for the RXRDY bit and read the data from the SCIRD register once the RXRDY bit is set high. The CPU is unnecessarily overloaded by selecting the polling method. To avoid this, you can use either the interrupt or DMA method. To use the interrupt method, set the SETRXINT bit. To use the DMA 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1567 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

method, set the SET_RX_DMA bit. Either an interrupt or a DMA request is generated the moment the RXRDY bit is set. 

## _**13.4.2.3.4.1.2 Receiving Data in Multibuffer Mode**_ 

Multibuffer mode is selected when the MBUFMODE bit in SCIGCR1 is set to 1. In this mode, SCI sets the RXRDY bit after receiving the programmed number of data in the receive buffer, the complete frame. The error condition detection logic is similar to the single-buffer mode, except that this logic monitors for the complete frame. Like single-buffer mode, use the polling, DMA, or interrupt method to read the data. The RXRDY bit is automatically cleared after the new data in SCIRD has been read. 

## _**13.4.2.3.4.2 Transmitting Data**_ 

The SCI transmitter is enabled if both the TXFUNC bit and the TXENA bit are set to 1. If the TXFUNC bit is not set, the LINTX pin functions as a general-purpose I/O pin rather than as an SCI function pin. Any value written to the SCITD/TDy before TXENA is set to 1 is not transmitted. Both of these control bits allow for the SCI transmitter to be held inactive independently of the receiver. 

The SCI module can transmit data in one of the following modes: 

- Single-Buffer (Normal) Mode 

- Multibuffered or Buffered SCI Mode 

## _**13.4.2.3.4.2.1 Transmitting Data in Single-Buffer Mode**_ 

Single-buffer mode is selected when the MBUFMODE bit in SCIGCR1 is cleared to 0. In this mode, the SCI waits for data to be written to SCITD, transfers the data to SCITXSHF, and transmits the data. The TXRDY and TXEMPTY bits indicate the status of the transmit buffers. That is, when the transmitter is ready for data to be written to SCITD, the TXRDY bit is set. Additionally, if both SCITD and SCITXSHF are empty, then the TXEMPTY bit is also set. 

You can transmit data by: 

1. Polling the Transmit Ready Flag 

2. Transmit Interrupt 3. DMA 

With the polling method, software can poll for the TXRDY bit to go high before writing the data to the SCITD register. The CPU is unnecessarily overloaded by selecting the polling method. To avoid this, you can use the interrupt or DMA method. To use the interrupt method, the SETTXINT bit is set. To use the DMA method, the SET_TX_DMA bit is set. Either an interrupt or a DMA request is generated the moment the TXRDY bit is set. When the SCI has completed transmission of all pending frames, the SCITXSHF register and SCITD are empty, the TXRDY bit is set, and an interrupt/DMA request is generated, if enabled. Because all data has been transmitted, the interrupt/DMA request must be halted. This can either be done by disabling the transmit interrupt (CLRTXINT)/DMA request (CLRTXDMA bit), or by disabling the transmitter (clear TXENA bit). 

## **Note** 

The TXRDY flag cannot be cleared by reading the corresponding interrupt offset in the SCIINTVECT0 or SCIINTVECT1 register. 

## _**13.4.2.3.4.2.2 Transmitting Data in Multibuffer Mode**_ 

Multibuffer mode is selected when the MBUFMODE bit in SCIGCR1 is set to 1. Like single-buffer mode, you can use the polling, DMA, or interrupt method to write the data to be transmitted. The transmitted data has to be written to the SCITD registers. The SCI waits for data to be written to the SCITD register and then transfers the programmed number of bytes to SCITXSHF to transmit one by one automatically. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1568 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.3.5 SCI Low-Power Mode**_ 

The SCI/LIN can be put in either local or global low-power mode. Global low-power mode is asserted by the system and is not controlled by the SCI/LIN. During global low-power mode, all clocks to the SCI/LIN are turned off so the module is completely inactive. 

Local low-power mode is asserted by setting the POWERDOWN bit; setting this bit stops the clocks to the SCI/LIN internal logic and the module registers. Setting the POWERDOWN bit causes the SCI to enter local low-power mode and clearing the POWERDOWN bit causes SCI/LIN to exit from local low-power mode. All the registers are accessible during local power-down mode as any register access enables the clock to SCI for that particular access alone. 

The wakeup interrupt is used to allow the SCI to exit low-power mode automatically when a low level is detected on the LINRX pin and also this clears the POWERDOWN bit. If wakeup interrupt is disabled, then the SCI/LIN immediately enters low-power mode whenever it is requested and also any activity on the LINRX pin does not cause the SCI to exit low-power mode. 

## **Note** 

## **Enabling Local Low-Power Mode During Receive and Transmit** 

If the wakeup interrupt is enabled and low-power mode is requested while the receiver is receiving data, then the SCI immediately generates a wakeup interrupt to clear the powerdown bit and prevents the SCI from entering low-power mode and thus completes the current reception. Otherwise, if the wakeup interrupt is disabled, then the SCI completes the current reception and then enters the low-power mode. 

## _**13.4.2.3.5.1 Sleep Mode for Multiprocessor Communication**_ 

When the SCI receives data and transfers that data from SCIRXSHF to SCIRD, the RXRDY bit is set and if SETRXINT is set, the SCI also generates an interrupt. The interrupt triggers the CPU to read the newly received frame before another one is received. In multiprocessor communication modes, this default behavior can be enhanced to provide selective indication of new data. When the SCI receives an address frame that does not match the address, the device can ignore the data following this non-matching address until the next address frame by using sleep mode. Sleep mode can be used with both idle-line and address-bit multiprocessor modes. 

If sleep mode is enabled by the SLEEP bit, then the SCI transfers data from SCIRXSHF to SCIRD only for address frames. Therefore, in sleep mode, all data frames are assembled in the SCIRXSHF register without being shifted into the SCIRD and without initiating a receive interrupt or DMA request. Upon reception of an address frame, the contents of the SCIRXSHF are moved into SCIRD, and the software must read SCIRD and determine if the SCI is being addressed by comparing the received address against the address previously set in the software and stored somewhere in memory (the SCI does not have hardware available for address comparison). If the SCI is being addressed, the software must clear the SLEEP bit so that the SCI loads SCIRD with the data of the data frames that follow the address frame. 

When the SCI has been addressed and sleep mode has been disabled (in software) to allow the receipt of data, the SCI can check the RXWAKE bit (SCIFLR.12) to determine when the next address has been received. The bit is set to 1, if the current value in SCIRD is an address; the bit is set to 0, if SCIRD contains data. If the RXWAKE bit is set, then software can check the address in SCIRD against the address. If SCIRD is still being addressed, then sleep mode can remain disabled; otherwise, the SLEEP bit can be set again. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1569 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

Following is a sequence of events typical of sleep mode operation: 

- The SCI is configured and both sleep mode and receive actions are enabled. 

- An address frame is received and a receive interrupt is generated. 

- Software compares the received address frame against that set by software and determines that the SCI is not being addressed, so the value of the SLEEP bit is not changed. 

- Several data frames are shifted into SCIRXSHF, but no data is moved to SCIRD and no receive interrupts are generated. 

- A new address frame is received and a receive interrupt is generated. 

- Software compares the received address frame against that set by software and determines that the SCI is being addressed and clears the SLEEP bit. 

- Data shifted into SCIRXSHF is transferred to SCIRD, and a receive interrupt is generated after each data frame is received. 

- In each interrupt routine, software checks RXWAKE to determine if the current frame is an address frame. 

- Another address frame is received, RXWAKE is set, software determines that the SCI is not being addressed and sets the SLEEP bit back to 1. No receive interrupts are generated for the data frames following this address frame. 

By ignoring data frames that are not intended for the device, fewer interrupts are generated. Otherwise, these interrupts require CPU intervention to read data that is of no significance to this specific device. Using sleep mode can help free some CPU resources. 

Except for the RXRDY flag, the SCI continues to update the receiver status flags (see Table 13-227) while sleep mode is active. In this way, if an error occurs on the receive line, an application can immediately respond to the error and take the appropriate corrective action. 

Because the RXRDY bit is not updated for data frames when sleep mode is enabled, the SCI can enable sleep mode and use a polling algorithm if desired. In this case, when RXRDY is set, software knows that a new address has been received. If the SCI is not being addressed, then the software can not change the value of the SLEEP bit and can continue to poll RXRDY. 

## **13.4.2.4 Local Interconnect Network Module** 

## _**13.4.2.4.1 LIN Communication Formats**_ 

The SCI/LIN module can be used in LIN mode or SCI mode. The enhancements for baud generation, DMA controls, and additional receive/transmit buffers necessary for LIN mode operation are also part of the enhanced buffered SCI module. LIN mode is selected by enabling LIN MODE bit in SCIGCR1 register. 

## **Note** 

The SCI/LIN is built around the SCI platform and uses a similar sampling scheme: 16 samples for each bit with majority vote on samples 8, 9, and 10. For the START bit, the first three samples are used. 

The SCI/LIN control registers are located at the SCI/LIN base address. 

## _**13.4.2.4.1.1 LIN Standards**_ 

For compatibility with LIN2.0 standard the following additional features are implemented over LIN1.3: 

1. Support for LIN 2.0 checksum 

2. Enhanced synchronizer FSM support for frame processing 

3. Enhanced handling of extended frames 

4. Enhanced baud rate generator 

5. Update wakeup/go to sleep 

The LIN module covers the CPU performance-consuming features, defined in the _LIN Specification Package_ Revision 1.3 and 2.0 by hardware. The Commander Mode of LIN module is compatible with LIN 2.1 standard. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1570 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.4.1.2 Message Frame**_ 

The LIN protocol defines a message frame format, shown in Figure 13-196. Each frame includes one commander header, one response, one in-frame response space, and inter-byte spaces. In-frame-response and inter-byte spaces can be 0. 

There is no arbitration in the definition of the LIN protocol; therefore, multiple responder nodes responding to a header can be detected as an error. 

The LIN bus is a single-channel wired-AND bus. The bus has a binary level: either dominant for a value of 0 or recessive for a value of 1. 

**==> picture [376 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
Message Frame<br>Commander or Responder<br>Commander Header Response<br>In-frame space<br>Synch Break Synch Field ID Field 1, 2, 3, ...8 Data Fields Checksum<br>**----- End of picture text -----**<br>


## **Figure 13-196. LIN Protocol Message Frame Format: Commander Header and Responder Peripheral Response** 

## _**13.4.2.4.1.2.1 Message Header**_ 

The header of a message is initiated by a commander (see Figure 13-197) and consists of a three fieldsequence: 

- The synchronization break field signaling the beginning of a message 

- The synchronization field conveying bit rate information of the LIN bus 

- The identification field denoting the content of a message 

**==> picture [422 x 93] intentionally omitted <==**

**----- Start of picture text -----**<br>
SYNCH BREAK FIELD SYNCH FIELD ID FIELD<br>**----- End of picture text -----**<br>


**Figure 13-197. Header 3 Fields: Synch Break, Synch, and ID** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1571 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.2.4.1.2.2 Response**_ 

The format of the response is as illustrated in Figure 13-198. There are two types of fields in a response: data and checksum. The data field consists of exactly one data byte, one start bit, and one stop bit, for a total of 10 bits. The LSB is transmitted first. The checksum field consists of one checksum byte, one start bit and one stop bit. The checksum byte is the inverted modulo-256 sum over all data bytes in the data fields of the response. 

**==> picture [248 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
Response<br>Checksum<br>1 to 8 Data Fields<br>Field<br>interbyte spaces<br>**----- End of picture text -----**<br>


**Figure 13-198. Response Format of LIN Message Frame** 

The format of the response is a stream of N data fields and one checksum field. Typically N is from 1 to 8, with the exception of the extended command frames (Section 13.4.2.4.1.6). The length N of the response is indicated either with the optional length control bits of the ID Field (this is used in standards earlier than LIN 1.x); see Table 13-229, or by LENGTH value in SCIFORMAT[18:16] register; see Table 13-230. The SCI/LIN module supports response lengths from 1 to 8 bytes in compliance with LIN 2.0. 

|**Table**|**13-229. Response**|**Length Info Using IDBYTE Field Bits[5:4] for LIN Standards Earlier than v1.3**|**Length Info Using IDBYTE Field Bits[5:4] for LIN Standards Earlier than v1.3**|
|---|---|---|---|
||**ID5**|**ID4**|**Number of Data Bytes**|
||0|0|2|
||0|1|2|
||1|0|4|
||1|1|8|



|**Table 13-230. Response Length with SCIFORMAT[18:16] Programming**|**Table 13-230. Response Length with SCIFORMAT[18:16] Programming**|
|---|---|
|**SCIFORMAT[18:16]**|**Number of Bytes**|
|000|1|
|001|2|
|010|3|
|011|4|
|100|5|
|101|6|
|110|7|
|111|8|



1572 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.4.1.3 Synchronizer**_ 

The synchronizer has three major functions in the messaging between commander and responder nodes. The synchronizer generates the commander header data stream, the synchronizer synchronizes to the LIN bus for responding, and the synchronizer locally detects timeouts. A bit rate is programmed using the prescalers in the BRSR register to match the indicated LIN_speed value in the LIN description file. 

The LIN synchronizer performs the following functions: commander header signal generation, responder detection and synchronization to message header with optional baud rate adjustment, response transmission timing and timeout control. 

The LIN synchronizer is capable of detecting an incoming break and initializing communication at all times. 

## _**13.4.2.4.1.4 Baud Rate**_ 

The transmission baud rate of any node is configured by the CPU at the beginning; this defines the bit time Tbit. The bit time is derived from the fields P and M in the baud rate selection register (BRSR). There is an additional 3-bit fractional divider value, field U in the BRSR register, which further fine-tunes the data-field baud rate. 

The ranges for the prescaler values in the BRSR register are: 

P = 0, 1, 2, 3, . . . , 2[24] - 1 

M = 0, 1, 2, . . . , 15 

U = 0, 1, 2, 3, 4, 5, 6, 7 

The P, M, and U values in the BRSR register are user programmable. The P and M dividers can be used for both SCI mode and LIN mode to select a baud rate. The U value is an additional 3-bit value determining that “ **a T VCLK** “ (with **a** = 0, 1) is added to each Tbit as explained in Section 13.4.2.4.1.4.2. If the ADAPT bit is set and the LIN peripheral is in adaptive baud rate mode, then all these divider values are automatically obtained during header reception when the synchronization field is measured. 

The LIN protocol defines baud rate boundaries as: 

1kHz ≤ FLINCLK ≤ 20kHz 

All transmitted bits are shifted in and out at Tbit periods. 

## _**13.4.2.4.1.4.1 Fractional Divider**_ 

The M field of the BRSR register modifies the integer prescaler P for fine tuning of the baud rate. The M value adds in increments of 1/16 of the P value. 

The bit time, Tbit is expressed in terms of the VCLK period _T VCLK_ as follows: 

For all P other than 0, and all M, 

**==> picture [120 x 30] intentionally omitted <==**

For P = 0 : Tbit = 32TVCLK 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1573 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

Therefore, the LINCLK frequency is given by: 

**==> picture [244 x 39] intentionally omitted <==**

**==> picture [151 x 26] intentionally omitted <==**

## _**13.4.2.4.1.4.2 Superfractional Divider**_ 

The superfractional divider scheme applies to the following modes: 

- LIN commander mode (sync field + identifier field + response field + checksum field) 

- LIN responder mode (response field + checksum field) 

## _**13.4.2.4.1.4.2.1 Superfractional Divider In LIN Mode**_ 

Building on the 4-bit fractional divider M (BRSR[27:24], the superfractional divider uses an additional 3-bit modulating value, illustrated in Table 13-231. The sync field (0x55), the identifier field, and the response field can all be seen as 8-bit data bytes flanked by a start bit and a stop bit. The bits with a 1 in the table have an additional VCLK period added to the Tbit. In LIN commander mode, bit modulation applies to sync field + identifier field + response field. In LIN responder mode, bit modulation applies to identifier field + response field. 

**Table 13-231. Superfractional Bit Modulation for LIN Commander Mode and Responder Mode** 

|**BRSR[30:28]**|**Start Bit**|**D[0]**|**D[1]**|**D[2]**|**D[3]**|**D[4]**|**D[5]**|**D[6]**|**D[7]**|**Stop Bit**|
|---|---|---|---|---|---|---|---|---|---|---|
|0h|0|0|0|0|0|0|0|0|0|0|
|1h|1|0|0|0|0|0|0|0|1|0|
|2h|1|0|0|0|1|0|0|0|1|0|
|3h|1|0|1|0|1|0|0|0|1|0|
|4h|1|0|1|0|1|0|1|0|1|0|
|5h|1|1|1|0|1|0|1|0|1|1|
|6h|1|1|1|0|1|1|1|0|1|1|
|7h|1|1|1|1|1|1|1|0|1|1|



The baud rate varies over a LIN data field to average according to the BRSR[30:28] value by a _d_ fraction of the peripheral internal clock: 0<d<1. 

The instantaneous bit time is expressed in terms of _T VCLK_ as follows: 

For all P other than 0, and all M and d (0 or 1), 

**==> picture [158 x 32] intentionally omitted <==**

For P = 0, Tbit = 32TVCLK 

1574 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

The averaged bit time is expressed in terms of _T VCLK_ as follows: 

For all P other than 0, and all M and d (0 < d <1), 

**==> picture [195 x 32] intentionally omitted <==**

For P = 0, Tbit = 32TVCLK 

## _**13.4.2.4.1.5 Header Generation**_ 

Automatic generation of the LIN protocol header data stream is supported without CPU interaction. The CPU or the DMA triggers the LIN state machine to generate a message header. A commander node initiates header generation on the CPU or DMA writes to the IDBYTE in the LINID register. The header is always sent by the commander to initiate a LIN communication and consists of three fields: synchronization break field, synchronization field, and identification field, as seen in Figure 13-199. 

## **Note** 

The LIN protocol uses the parity bits in the identifier. The control length bits are optional to the LIN protocol. 

**==> picture [421 x 114] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDEL<br>SYNCH BREAK SYNCH FIELD ID FIELD<br>1..4 Tbit<br>13+(0...7) Tbit 10 Tbit 10 Tbit<br>1 0 1 0 1 0 1 0<br>START BIT<br>STOP BIT<br>**----- End of picture text -----**<br>


**Figure 13-199. Message Header in Terms of Tbit** 

- The break field consists of two components: 

   - The synchronization break (SYNCH BREAK) consists of a minimum of 13 (dominant) low bits to a maximum of 20 dominant bits. The sync break length can be extended from the minimum with the 3-bit SBREAK value in the LINCOMP register. 

   - The synchronization break delimiter (SDEL) consists of a minimum of 1 (recessive) high bit to a maximum of 4 recessive bits. The delimiter marks the end of the synchronization break field. The sync break delimiter length depends on the 2-bit SDEL value in the LINCOMP register. 

- The synchronization field (SYNCH FIELD) consists of one start bit, byte 0x55, and a stop bit. SYNCH FIELD is used to convey Tbit information and resynchronize LIN bus nodes. 

- The identifier field ID byte can use 6 bits as an identifier, with optional length control and two optional bits as parity of the identifier. The identifier parity is used and checked if the PARITYENA bit is set. If length control bits are not used, then there can be a total of 64 identifiers plus parity. If neither length control or parity are used there can be up to 256 identifiers. See Figure 13-200 for an illustration of the ID field. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1575 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Note** 

## **Optional Control Length Bits** 

The control length bits only apply to LIN standards prior to LIN 1.3. IDBYTE field conveys response length information if compliant to standards earlier than LIN1.3. The SCIFORMAT register stores the length of the response for later versions of the LIN protocol. 

**==> picture [234 x 98] intentionally omitted <==**

**----- Start of picture text -----**<br>
ID Field<br>ID0 ID1 ID2 ID3 ID4 ID5 P0 P1<br>Optional<br>Optional<br>Length<br>Contro l Parity<br>Bits<br>Bits<br>Start Bit Stop Bit<br>**----- End of picture text -----**<br>


**Figure 13-200. ID Field** 

## **Note** 

If the LIN module, configured as a responder in multibuffer mode, is in the process of transmitting data while a new header comes in, the module can end up responding with the data from the previous interrupted response (not the data corresponding to the new ID). To avoid this scenario, the following procedure can be used: 

1. Check for the Bit Error (BE) during the response transmission. If the BE flag is set, this indicates that a collision has happened on the LIN bus (here because of the new Synch Break). 

2. In the Bit Error ISR, configure the TD0 and TD1 registers with the next set of data to be transmitted on a TX Match for the incoming ID. Before writing to TD0/TD1 make sure that there was not already an update because of a Bit Error; otherwise, TD0/TD1 can be written twice for one ID. 

3. Once the complete ID is received, based on the match, the newly configured data is transmitted by the node. 

1576 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.4.1.5.1 Event Triggered Frame Handling**_ 

The LIN 2.0 protocol uses event-triggered frames that can occasionally cause collisions. Event-triggered frames are handled in software. 

If no responder answers to an event triggered frame header, the commander node sets the NRE flag, and a NRE interrupt occurs if enabled. If a collision occurs, a frame error and checksum error can arise before the NRE error. Those errors are flagged and the appropriate interrupts occur, if enabled. 

Frame errors and checksum errors depend on the behavior and synchronization of the responding responders. If the responders are totally synchronized and stop transmission once the collision occurred, it is possible that only the NRE error is flagged despite the occurrence of a collision. To detect if there has been a reception of one byte before the NRE error is flagged, the BUS BUSY flag can be used as an indicator. 

The BUS BUSY flag is set on the reception of the first bit of the header and remains set until the header reception is complete, and again is set on the reception of the first bit of the response. In the case of a collision, the flag is cleared in the same cycle as the NRE flag is set. 

Software can implement the following sequence: 

- Once the reception of the header is done (poll for RXID flag), wait for the BUS BUSY flag to get set or the NRE flag to get set. 

- If the BUS BUSY flag is not set before the NRE flag, then a true no response is the case (no data has been transmitted onto the bus). 

- If the BUS BUSY flag gets set, then wait for the NRE flag to get set or for successful reception. If the NRE flag is set, then a collision has occurred on the bus. 

Even in the case of a collision, the received (corrupted) data is accessible in the RX buffers; registers LINRD0 and LINRD1. 

## _**13.4.2.4.1.5.2 Header Reception and Adaptive Baud Rate**_ 

A responder node baud rate can optionally be adjusted to the detected bit rate as an option to the LIN module. The adaptive baud rate option is enabled by setting the ADAPT bit. During header reception, a responder measures the baud rate during detection of the synch field. If ADAPT bit is set, then the measured baud rate is compared to the responder node programmed baud rate and adjusted to the LIN bus baud rate if necessary. 

The responder node adjusts to any measured baud rate that is within ±10% of the programmed baud rate. For example, if the expected baud rate is programmed at 20kbps, the responder node detects any baud rate between 18kbps and 22kbps and adjusts accordingly. The MBRSR register prescaler is determined by the following formula: 

**==> picture [91 x 19] intentionally omitted <==**

The LIN synchronizer determines two measurements: BRK_count and BAUD_count (Figure 13-201). These values are always calculated during the Header reception for synch field validation (Figure 13-202). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1577 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [422 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
SYNCH FIELD ID FIELD<br>SYNCH BREAK SDEL 10 Tbit 10 Tbit<br>1 0 1 0 1 0 1 0<br>BRK_count BAUD_count<br>1 2 3 4<br>START BIT STOP BIT<br>**----- End of picture text -----**<br>


**Figure 13-201. Measurements for Synchronization** 

By measuring the values BRK_count and BAUD_count, a valid sync break sequence can be detected as described in Figure 13-202. The four numbered events in Figure 13-201 signal the start/stop of the synchronizer counter. The synchronizer counter uses VCLK as the time base. 

The synchronizer counter is used to measure the sync break relative to the detecting node Tbit. For a responder node receiving the sync break, a threshold of 11 Tbit is used as required by the LIN protocol. For detection of the dominant data stream of the sync break, the synchronizer counter is started on a falling edge and stopped on a rising edge of the LINRX. On detection of the sync break delimiter, the synchronizer counter value is saved and then reset. 

On detection of five consecutive falling edges, the BAUD_count is measured. Bit timing calculation and consistency to required accuracy is implemented following the recommendations of LIN revision 2.0. A responder node can calculate a single Tbit time by division of BAUD_count by 8. In addition, for consistency between the detected edges the following is evaluated: 

BAUD_count + BAUD_count » 2 + BAUD_count » 3 ≤ BRK_count 

The BAUD_count value is shifted 3 times to the right and rounded using the first insignificant bit to obtain a Tbit unit. If the ADAPT bit is set, then the detected baud rate is compared to the programmed baud rate. 

During the header reception processing as illustrated in Figure 13-202, if the measured BRK_count value is less than 11 Tbit, the sync break is not valid according to the protocol for a fixed rate. If the ADAPT bit is set, then the MBRS register is used for measuring BRK_count and BAUD_count values and automatically adjusts to any allowed LIN bus rate (refer to _LIN Specification Package 2.0_ ). 

## **Note** 

In adaptive mode, the MBRS divider can be set to allow a maximum baud rate that is not more than 10% above the expected operating baud rate in the LIN network. Otherwise, a 0x00 data byte can mistakenly be detected as a sync break. 

The break-threshold relative to the responder node is 11 Tbit. The break is 13 Tbit as specified in LIN v1.3. 

1578 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [376 x 570] intentionally omitted <==**

**----- Start of picture text -----**<br>
LINRX=1<br>Wait for falling<br>edge<br>1<br>On LINRX<br>Increment while<br>counter LINRX=0<br>No<br>counter ≥<br>o Reset counter<br>11 Tbit ?<br>Yes<br>Increment<br>counter LINRX=0<br>2 On LINRX<br>Save counter<br>( SBRK_count)<br>and reset it<br>3 On 1st LINRX falling edge<br>increment<br>counter<br>4<br>On 5th LINRX falling edge<br>Save counter ( BAUD_count)<br>Verify valid Synch Field<br>If ADAPT=1, compare baud rate and Baud<br>Update flag is set if baudrates differ<br>Receive ID Field<br>Wait for Response<br>**----- End of picture text -----**<br>


**Figure 13-202. Synchronization Validation Process and Baud Rate Adjustment** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1579 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

If the synch field is not detected within the given tolerances, the inconsistent-sync-field-error (ISFE) flag is set. An ISFE interrupt is generated, if enabled by the respective bit in the SCISETINT register. The ID byte can be received after the synch field validation was successful. Any time a valid break (larger than 11 Tbit) is detected, the receiver state machine can reset to reception of this new frame. This reset condition is only valid during response state, not if an additional synch break occurs during header reception. 

## **Note** 

When an inconsistent synch field (ISFE) error occurs, suggested action for the application is to reset the SWnRST bit and set the SWnRST bit to make sure that the internal state machines are back to the normal states. 

## _**13.4.2.4.1.6 Extended Frames Handling**_ 

The LIN protocol 2.0 and prior includes two extended frames with identifiers 62 (user-defined) and 63 (reserved extended). The response data length of the user-defined frame (ID 62, or 0x3E) is unlimited. The length for this identifier is set at network configuration time to be shared with the LIN bus nodes. 

Extended frame communication is triggered on reception of a header with identifier 0x3E; see Figure 13-203. Once the extended frame communication is triggered, unlike normal frames, this communication needs to be stopped before issuing another header. To stop the extended frame communication the STOP EXT FRAME bit must be set. 

**==> picture [436 x 120] intentionally omitted <==**

**----- Start of picture text -----**<br>
Extended Frame With Embedded Checksum Bytes<br>Commander Header N Data Fields Response<br>In-frame space<br>Synch Break Synch Field ID Field Checksum Checksum Checksum<br>**----- End of picture text -----**<br>


**Figure 13-203. Optional Embedded Checksum in Response for Extended Frames** 

An ID interrupt is generated (if enabled and there is a match) on reception of ID 62 (0x3E). This interrupt allows the CPU using a software counter to keep track of the bytes that are being sent out and decides when to calculate and insert a checksum byte (recommended at periodic rates). To handle this procedure, SC bit is used. A write to the send checksum bit SC initiates an automatic send of the checksum byte. The last data field can always be a checksum in compliance with the LIN protocol. 

The periodicity of the checksum insertion, defined at network configuration time, is used by the receiving node to evaluate the checksum of the ongoing message, and has the benefit of enhanced reliability. 

For the sending node, the checksum is automatically embedded each time the send checksum bit SC is set. For the receiving node, the checksum is compared each time the compare checksum bit CC is set; see Figure 13-204. 

## **Note** 

The LIN 2.0 enhanced checksum does not apply to the reserved identifiers. The reserved identifiers always use the classic checksum. 

1580 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [302 x 170] intentionally omitted <==**

**----- Start of picture text -----**<br>
ChecksumCompare 7 SCIRXSHF 0 RX<br>CHECKSUM CALCULATOR<br>Send<br>Checksum<br>7 SCITXSHF 0 TX<br>**----- End of picture text -----**<br>


**Figure 13-204. Checksum Compare and Send for Extended Frames** 

## _**13.4.2.4.1.7 Timeout Control**_ 

Any LIN node listening to the bus and expecting a response initiated from a commander node can flag a no-response error timeout event. The LIN protocol defines four types of timeout events, which are all handled by the hardware of the LIN module. The four LIN protocol events are: 

- No-response timeout error 

- Bus idle detection 

- Timeout after wakeup signal 

- Timeout after three wakeup signals 

## _**13.4.2.4.1.7.1 No-Response Error (NRE)**_ 

The no-response error occurs when any node expecting a response waits for TFRAME_MAX time and the message frame is not fully completed within the maximum length allowed, TFRAME_MAX. After this time, a no-response error (NRE) is flagged in the NRE bit of the SCIFLR register. An interrupt is triggered, if enabled. 

As specified in the LIN 1.3 standard, the minimum time to transmit a frame is: 

T = T + T + T = 44 + 10N FRAME_MIN HEADER_MIN DATA_FIELD CHECKSUM_FIELD 

where N = number of data fields. 

And the maximum time frame is given by: 

TFRAME_MAX = TFRAME_MIN * 1.4 = (44 + 10N) * 1.4 

The timeout value TFRAME_MAX is derived from the _N_ number of data fields value, see Table 13-232. The _N_ value is either embedded in the header ID field for messages or is part of the description file. In the latter case, the 3-bit CHAR value in SCIFORMAT register indicates the value for _N_ . 

## **Note** 

The length coding of the ID field does not apply to two extended frame identifiers, ID fields of 0x3E (62) and 0x3F (63). In these cases, the ID field can be followed by an arbitrary number of data byte fields. Also, the LIN 2.0 protocol specification mentions that ID field 0x3F (63) cannot be used. For these two cases, the NRE is not handled by the LIN hardware. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1581 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-232. Timeout Values in Tbit Units** 

|**N**|**TDATA_FIELD**|**TFRAME_MIN**|**TFRAME_MAX**|
|---|---|---|---|
|1|10|54|76|
|2|20|64|90|
|3|30|74|104|
|4|40|84|118|
|5|50|94|132|
|6|60|104|146|
|7|70|114|160|
|8|80|124|174|



## _**13.4.2.4.1.7.2 Bus Idle Detection**_ 

The second type of timeout can occur when a node detects an inactive LIN bus: no transitions between recessive and dominant values are detected on the bus. This happens after a minimum of 4 seconds (this is 80,000 FLINCLK cycles with the fastest bus rate of 20kbps). If a node detects no activity in the bus as the TIMEOUT bit is set, assume that the LIN bus is in sleep mode. Application software can use the Timeout flag to determine when the LIN bus is inactive and put the LIN into sleep mode by writing the POWERDOWN bit. 

## **Note** 

After the timeout was flagged, a SWnRESET must be asserted before entering Low-Power Mode. This is required to reset the receiver in case that an incomplete frame is on the bus before the idle period. 

## _**13.4.2.4.1.7.3 Timeout After Wakeup Signal and Timeout After Three Wakeup Signals**_ 

The third and fourth types of timeout are related to the wakeup signal. A node initiating a wakeup must expect a header from the commander within a defined amount of time: timeout after wakeup signal. See Section 13.4.2.5.3 for more details. 

## _**13.4.2.4.1.8 TXRX Error Detector (TED)**_ 

The following sources of error are detected by the TXRX error detector logic (TED). The TED logic consists of a bit monitor, an ID parity checker, and a checksum error. The following errors are detected: 

- Bit errors (BE) 

- Physical bus errors (PBE) 

- Identifier parity errors (PE) 

- Checksum errors (CE) 

All of these errors (BE, PBE, PE, CE) are flagged. An interrupt for the flagged errors is generated if enabled. A message is valid for both the transmitter and the receiver if there is no error detected until the end of the frame. 

1582 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.4.1.8.1 Bit Errors**_ 

A bit error (BE) is detected at the bit time when the bit value that is monitored is different from the bit value that is sent. A bit error is indicated by the BE flag in SCIFLR. After signaling a BE, the transmission is aborted no later than the next byte. The bit monitor makes sure that the transmitted bit in LINTX is the correct value on the LIN bus by reading back on the LINRX pin as shown in Figure 13-205. 

## **Note** 

If a bit occurs due to receiving a header during a responder response, NRE/TIMEOUT flag is not set for the new frame. 

**==> picture [428 x 226] intentionally omitted <==**

**----- Start of picture text -----**<br>
ID-Parity-Error ID<br>ID-Parity Error Flag PARITY<br>ID-Pairty Interrupt CHECKER<br>(if enabled)<br>CHECKSUM<br>Checksum-Error Flag CALCULATOR VBAT<br>Checksum-Error Int.<br>(if enabled) 7 0<br>SCIRXSHF<br>BIT MONITOR<br>Bit-Error Flag<br>Bit-Error Int.Bus-Error Flag(if enabled) = RX LIN BUS<br>Bus-Error Int. (if enabled)<br>7 0 T<br>SCITXSHF X<br>GND<br>**----- End of picture text -----**<br>


**Figure 13-205. TXRX Error Detector** 

## _**13.4.2.4.1.8.2 Physical Bus Errors**_ 

A Physical Bus Error (PBE) has to be detected by a commander, if no valid message can be generated on the bus (bus shorted to GND or VBAT). The bit monitor detects a PBE during the header transmission, if no Synch Break can be generated (for example, because of a bus shortage to VBAT) or if no Synch Break delimiter can be generated (for example, because of a bus shortage to GND). Once the Sync Break Delimiter was validated, all other deviations between the monitored and the sent bit value are flagged as Bit Errors (BE) for this frame. 

## _**13.4.2.4.1.8.3 ID Parity Errors**_ 

If parity is enabled, an ID parity error (PE) is detected if any of the two parity bits of the sent ID byte are not equal to the calculated parity on the receiver node. The two parity bits are generated using the following mixed parity algorithm: 

- _P_ 0 � _ID_ 0 � _ID_ 1 � _ID_ 2 � _ID_ 4 ( _even Parity_ ) _P_ 1 � _ID_ 1 � _ID_ 3 � _ID_ 4 � _ID_ 5 ( _odd Parity_ ) 

If an ID-parity error is detected, the ID-parity error is flagged, and the received ID is not valid. See Section 13.4.2.4.1.9 for details. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1583 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.2.4.1.8.4 Checksum Errors**_ 

A checksum error (CE) is detected and flagged at the receiving end, if the calculated modulo-256 sum over all received data bytes (including the ID byte if the enhanced checksum type) plus the checksum byte does not result in 0xFF. The modulo-256 sum is calculated over each byte by adding with carry, where the carry bit of each addition is added to the LSB of the resulting sum. 

For the transmitting node, the checksum byte sent at the end of a message is the inverted sum of all the data bytes (see Figure 13-206) for classic checksum implementation. The checksum byte is the inverted sum of the identifier byte and all the data bytes (see Figure 13-207) for the LIN 2.0 compliant enhanced checksum implementation. The classic checksum implementation can always be used for reserved identifiers 60 to 63; therefore, the CTYPE bit is overridden in this case. For signal-carrying-frame identifiers (0 to 59) the type of checksum used depends on the CTYPE bit. 

**==> picture [216 x 167] intentionally omitted <==**

**----- Start of picture text -----**<br>
Response<br>Checksum<br>1 to 8 Data Fields<br>Field<br>Checkbyte<br>Modulo-256 sum + INVERT<br>**----- End of picture text -----**<br>


**Figure 13-206. Classic Checksum Generation at Transmitting Node** 

**==> picture [240 x 167] intentionally omitted <==**

**----- Start of picture text -----**<br>
Response<br>From<br>Header<br>Checksum<br>ID Field 1 to 8 Data Fields Field<br>Checkbyte<br>Modulo-256 sum + INVERT<br>**----- End of picture text -----**<br>


**Figure 13-207. LIN 2.0-Compliant Checksum Generation at Transmitting Node** 

1584 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.4.1.9 Message Filtering and Validation**_ 

Message filtering uses the entire identifier to determine which nodes participate in a response, either receiving or transmitting a response. Therefore, two acceptance masks are used as shown in Figure 13-208. During header reception, all nodes filter the ID-Field (ID-Field is the part of the header explained in Figure 13-200) to determine whether the nodes transmit a response or receive a response for the current message. There are two masks for message ID filtering: one to accept a response reception, the other to initiate a response transmission. See Figure 13-208. All nodes compare the received ID to the identifier stored in the ID-Responder Task BYTE of the LINID register and use the RX ID MASK and the TX ID MASK fields in the LINMASK register to filter the bits of the identifier that can not be compared. 

If there is an RX match with no parity error and the RXENA bit is set, there is an ID RX flag and an interrupt is triggered if enabled. If there is a TX match with no parity error and the TXENA bit is set, there is an ID TX flag and an interrupt is triggered if enabled in the SCISETINT register. 

The masked bits become "don’t cares" for the comparison. To build a mask for a set of identifiers, an XOR function can be used. 

**==> picture [438 x 327] intentionally omitted <==**

**----- Start of picture text -----**<br>
Parity Enable<br>ID<br>Parity ID Parity Error<br>Checker<br>23 LINID 16<br>No<br>ID-Parity<br>RX 7 SCIRXSHF 0 Error RXENA<br>RX ID RX<br>7 RX ID Mask 0 AND<br>Match Flag<br>7 ID-Byte 0 0<br>7 ID-Responder Task Byte 0 1 No ID INT<br>From ID-Parity<br>Error<br>SCIRXSHF<br>HGEN CTRL<br>TX ID TX<br>7 TX ID Mask 0 AND<br>Match Flag<br>7 ID-Byte 0 0<br>7 ID-Responder Task Byte 0 1<br>HGEN CTRL<br>**----- End of picture text -----**<br>


**Figure 13-208. ID Reception, Filtering, and Validation** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1585 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

For example, to build a mask to accept IDs 0x26 and 0x25 using LINID[7:0] = 0x20; that is, compare 5 mostsignificant bits (MSBs) and filter 3 least-significant bits (LSBs), the acceptance mask can be: 

(0 _x_ 26 � 0 _x_ 25) � 0 _x_ 20 � 0 _x_ 07 

A mask of all zeros compares all bits of the received identifier in the shift register with the ID-BYTE in LINID[7:0]. If HGEN CTRL is set to 1, a mask of 0xFF always causes a match. A mask of all 1s filters all bits of the received identifier, and thus there is an ID match regardless of the content of the ID-Responder Task BYTE field in the LINID register. 

## **Note** 

When the HGEN CTRL bit = 0, the LIN nodes compare the received ID to the ID-BYTE field in the LINID register, and use the RX ID MASK and the TX ID MASK in the LINMASK register to filter the bits of the identifier that can not be compared. 

If there is an RX match with no parity error and the RXENA bit is set, there is an ID RX flag and an interrupt is triggered if enabled. A mask of all 0s compares all bits of the received identifier in the shift register with the ID-BYTE field in LINID[7:0]. A mask of all 1s filters all bits of the received identifier and there is no match. 

## **If HGEN CTLR = 1:** 

- Received ID is compared with the ID-Responder Task byte, using the RXID mask and the TXID mask. 

- A mask of all 1s always result in a match. 

- A mask of all 0s means all the bits must be the same to result in a match. 

- If a mask has some bits that are 1s, then those bits are not used for the filtering criterion. 

## **If HGEN CTRL = 0:** 

- Received ID is compared with the ID byte, using the RXID mask and the TXID mask. 

- A mask of all 1s results in no match. 

- A mask of all 0s means all the bits must be the same to result in a match. 

- If a mask has some bits that are 1s, then those bits are not used for the filtering criterion. 

During header reception, the received identifier is copied to the Received ID field LINID[23:16]. If there is no parity error and there is either a TX match or an RX match, then the corresponding TX or RX ID flag is set. If the ID interrupt is enabled, then an ID interrupt is generated. 

After the ID interrupt is generated, the CPU can read the Received ID field LINID[23:16] and determine what response to load into the transmit buffers. 

## **Note** 

When byte 0 is written to TD0 (LINTD0[31:24]), the response transmission is automatically generated. 

In multibuffer mode, the TXRDY flag is set when all the response data bytes and checksum byte are copied to the shift register SCITXSHF. In non-multibuffer mode, the TXRDY flag is set each time a byte is copied to the SCITXSHF register, and also for the last byte of the frame after the checksum byte is copied to the SCITXSHF register. 

In multibuffer mode, the TXEMPTY flag is set when both the transmit buffers TDy and the SCITXSHF shift register are emptied and the checksum has been sent. In non-multibuffer mode, TXEMPTY is set each time TD0 and SCITXSHF are emptied, except for the last byte of the frame where the checksum byte must also be transmitted. 

If parity is enabled, all responder receiving nodes validate the identifier using all eight bits of the received ID byte. The SCI/LIN flags a corrupted identifier if an ID-parity error is detected. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1586 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.4.1.10 Receive Buffers**_ 

To reduce CPU load when receiving a LIN N-byte (with N = 1–8) response in interrupt mode or DMA mode, the SCI/LIN module has eight receive buffers. These buffers can store an entire LIN response in the RDy receive buffers. Figure 13-192 illustrates the receive buffers. 

The checksum byte following the data bytes is validated by the internal checksum calculator. The checksum error (CE) flag indicates a checksum error and a CE interrupt is generated if enabled in the SCISETINT register. 

The multibuffer 3-bit counter counts the data bytes transferred from the SCIRXSHF register to the RDy receive buffers if multibuffer mode is enabled, or to RD0 if multibuffer mode is disabled. The 3-bit compare register contains the number of data bytes expected to be received. In cases where the IDBYTE field does not convey message length (see _Note: Optional Control Length Bits_ in Section 13.4.2.4.1.5), the LENGTH value, indicates the expected length and is used to load the 3-bit compare register. Whether the length control field or the LENGTH value is used is selectable with the COMMMODE bit. 

A receive interrupt, and a receive ready RXRDY flag , and a DMA request (RXDMA) can occur after receiving a response, if there are no response receive errors for the frame (such as, there is no checksum error, frame error, and overrun error). The checksum byte is compared before acknowledging a reception. A DMA request can be generated for each received byte or for the entire response depending on whether the multibuffer mode is enabled or not (MBUFMODE bit). 

## **Note** 

In multibuffer mode following are the scenarios associated with clearing the RXRDY flag bit: 

1. The RXRDY flag cannot be cleared by reading the corresponding interrupt offset in the SCIINTVECT0/1 register. 

2. For LENGTH less than or equal to 4, Read to RD0 register clears the RXRDY flag. 

3. For LENGTH greater than 4, Read to RD1 register clears the RXRDY flag. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1587 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.2.4.1.11 Transmit Buffers**_ 

To reduce the CPU load when transmitting a LIN N-byte (with N = 1–8) response in interrupt modeor DMA mode, the SCI/LIN module has 8 transmit buffers, TD0–TD7 in LINTD0 and LINTD1. With these transmit buffers, an entire LIN response field can be preloaded in the TDy transmit buffers. Optionally, a DMA transfer can be done on a byte-per-byte basis when multibuffer mode is not enabled (MBUFMODE bit). Figure 13-193 illustrates the transmit buffers. 

The multibuffer 3-bit counter counts the data bytes transferred from the TDy transmit buffers register if multibuffer mode is enabled, or from TD0 to SCITXSHF if multibuffer mode is disabled. The 3-bit compare register contains the number of data bytes expected to be transmitted. If the ID field is not used to convey message length (see _Note: Optional Control Length Bits_ in Section 13.4.2.4.1.5), the LENGTH value indicates the expected length and is used instead to load the 3-bit compare register. Whether the length control field or the LENGTH value is used is selectable with the COMMMODE bit. 

A transmit interrupt (TX interrupt) and a transmit ready flag (TXRDY flag), as well as a DMA request (TXDMA) can occur after transmitting a response.A DMA request can be generated for each transmitted byte or for the entire response depending on whether multibuffer mode is enabled or not (MBUFMODE bit). 

The checksum byte is automatically generated by the checksum calculator and sent after the data-fields transmission is finished. The multibuffer 3-bit counter counts the data bytes transferred from the TDy buffers into the SCITXSHF register. 

## **Note** 

The transmit interrupt request can be eliminated until the next series of data is written into the transmit buffers LINTD0 and LINTD1, by disabling the corresponding interrupt using the SCICLRINT register or by disabling the transmitter using the TXENA bit. 

1588 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.4.2 LIN Interrupts**_ 

LIN and SCI modes have a common interrupt block, as explained in Section 13.4.2.3.2. There are 16 interrupt sources in the SCI/LIN module, with 8 of them being LIN mode only, as seen in Table 13-226. 

A LIN message frame indicating the timing and sequence of the LIN interrupts that can occur is shown in Figure 13-209. 

**==> picture [500 x 256] intentionally omitted <==**

**----- Start of picture text -----**<br>
T FrameMax<br>Commander Header Responder Response T Bus Idle (4s)<br>In-frame space<br>Synch Break Synch Field ID Field 1, 2, 3, ...8 Data Fields Checksum<br>ISF Error Int.<br>Physical Bus Bit Error Int.<br>Error Int.(Commander)<br>FE FE FE FE<br>Parity Error Int. ID Interrupt TX Int. (single buffer) RX Int. (single buffer) Overrun Error Int. TX Int. (single buffer) RX Int. (single buffer) TX Int. (single buffer) Frame Error Int. (FE) TX Int. (multi-buffer/ last byte single buffer) Checksum Error Int. RX Int. (multi-buffer/ last byte single buffer) No Response Error Int. Timeout - Bus Idle (4s) Int.<br>**----- End of picture text -----**<br>


**Figure 13-209. LIN Message Frame Showing LIN Interrupt Timing and Sequence** 

## _**13.4.2.4.3 Servicing LIN Interrupts**_ 

When servicing an interrupt, clear the corresponding flag in the flag register (SCIFLR) before clearing the global interrupt (LIN_GLB_INT_CLR). The ISR can follow the guidelines below. This prevents any spurious or duplicate interrupt from occurring. 

- Clear the LIN interrupt flag in the SCIFLR register. 

- Read the LIN interrupt status register to make sure the flag is cleared. 

- Clear the global interrupt flag bit in LIN_GLB_INT_CLR. 

## **Note** 

The transmit interrupt is generated before the LIN transmitter is ready to accept new data. Inside of the LIN transmit ISR, the software can wait until the buffer is completely empty before loading the next data. This can be done by polling for the Bus Busy Flag (SCIFLR.BUSY) to be 0. 

## _**13.4.2.4.4 LIN Configurations**_ 

The following list details the configuration steps that software can perform prior to the transmission or reception of data in LIN mode. As long as the SWnRST bit in the SCIGCR1 register is cleared to 0 the entire time that the LIN is being configured, the order in which the registers are programmed is not important. 

- Enable LIN by setting RESET bit (SCIGCR0.0). 

- Clear SWnRST to 0 before configuring the LIN (SCIGCR1.7). 

- Enable the LINRX and LINTX pins by setting the RXFUNC and TXFUNC bits. 

- Select LIN mode by programming the LINMODE bit (SCIGCR1.6). 

- Select commander or responder mode by programming the CLOCK bit. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1589 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- Select the desired frame format (checksum, parity, length control) by programming SCIGCR1. 

- Select multibuffer mode by programming MBUFMODE bit (SCIGCR1.10). 

- Select the baud rate to be used for communication by programming BRSR. 

- Set the maximum baud rate to be used for communication by programming MBRSR. 

- Set the CONT bit to make LIN not halt for an emulation breakpoint until the LIN current reception or transmission is complete (this bit is used only in an emulation environment). 

- Set LOOPBACK bit (SCIGCR1.16) to connect the transmitter to the receiver internally if needed (this feature is used to perform a self-test). 

- Select the receiver enable RXENA bit (SCIGCR1.24), if data is to be received. 

- Select the transmit enable TXENA bit (SCIGCR1.25), if data is to be transmitted. 

- Select the RXIDMASK and the TXIDMASK fields in the LINMASK register. 

- Set SWnRST (SCIGCR1.7) to 1 after the LIN is configured. 

- Receive or Transmit data (see Section 13.4.2.4.1.9, Section 13.4.2.4.4.1, and Section 13.4.2.4.4.2). 

## **Note** 

If TXENA is set and the SWnRST is released, the LIN immediately generates a new DMA request but not a new transmit interrupt request. If using interrupts, the first transmission must be started with software by writing data to the transmit buffer, followed by writing the chosen ID to the LINID register to initiate the transmission. 

1590 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.4.2.4.4.1 Receiving Data**_ 

The LIN receiver is enabled to receive messages if both the RXFUNC bit and the RXENA bit are set to 1. If the RXFUNC bit is not set, the LINRX pin functions as a general-purpose I/O pin rather than as a LIN function pin. 

The IDRXFLAG in the SCIFLR register is set after a valid LINID is received with an RX Match. An ID interrupt is then generated, if enabled. 

## _**13.4.2.4.4.1.1 Receiving Data in Single-Buffer Mode**_ 

Single-buffer mode is selected when the MBUFMODE bit is cleared to 0. In this mode, LIN sets the RXRDY bit when the LIN transfers newly received data from SCIRXSHF to RD0. The SCI clears the RXRDY bit after the new data in RD0 has been read. Also, as data is transferred from SCIRXSHF to RD0, the LIN sets the FE, OE, or PE flags if any of these error conditions were detected in the received data. These error conditions are supported with configurable interrupt capability. 

You can receive data by: 

1. Polling Receive Ready Flag 

2. Receive Interrupt 3. DMA 

In polling method, software can poll for the RXRDY bit and read the data from RD0 byte of the LINRD0 register once the RXRDY bit is set high. The CPU is unnecessarily overloaded by selecting the polling method. To avoid this, you can use the interrupt or DMA method. To use the interrupt method, the SETRXINT bit is set. To use the DMA method, the SET_RX_DMA bit must be set. Either an interrupt or a DMA request is generated the moment the RXRDY bit is set. If the checksum scheme is enabled by setting the Compare Checksum (CC) bit to 1, the checksum is compared on the byte that is currently being received, which is expected to be the checksum byte. The CC bit is cleared once the checksum is received. A CE is immediately flagged, if there is a checksum error. 

## _**13.4.2.4.4.1.2 Receiving Data in Multibuffer Mode**_ 

Multibuffer mode is selected when the MBUFMODE bit is set to 1. In this mode, LIN sets the RXRDY bit after receiving the programmed number of data in the receive buffer and the checksum field, the complete frame. The error condition detection logic is similar to the single-buffer mode, except that this logic monitors for the complete frame. Like single-buffer mode, you can use the polling, DMA, or interrupt method to read the data. The received data has to be read from the LINRD0 and LINRD1 registers, based on the number of bytes. For a LENGTH less than or equal to 4, a read from the LINRD0 register clears the RXRDY flag. For a LENGTH greater than 4, a read from the LINRD1 register clears the RXRDY flag. If the checksum scheme is enabled by setting the Compare Checksum (CC) bit to 1 during the reception of the data, then the byte that is received after the reception of the programmed number of data bytes indicated by the LENGTH field is treated as a checksum byte. The CC bit is cleared once the checksum is received and compared. 

## _**13.4.2.4.4.2 Transmitting Data**_ 

The LIN transmitter is enabled if both the TXFUNC bit and the TXENA bit are set to 1. If the TXFUNC bit is not set, the LINTX pin functions as a general-purpose I/O pin rather than as a LIN function pin. Any value written to the TD0 before the TXENA bit is set to 1 is not transmitted. Both of these control bits allow for the LIN transmitter to be held inactive independently of the receiver. 

The IDTXFLAG bit in the SCIFLR register is set after a valid LIN ID is received with a TX Match. An ID interrupt is then generated, if enabled. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1591 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.4.2.4.4.2.1 Transmitting Data in Single-Buffer Mode**_ 

Single-buffer mode is selected when the MBUFMODE bit is cleared to 0. In this mode, LIN waits for data to be written to TD0, transfers the data to SCITXSHF, and transmits the data. The TXRDY and TXEMPTY bits indicate the status of the transmit buffers. That is, when the transmitter is ready for data to be written to TD0, the TXRDY bit is set. Additionally, if both TD0 and SCITXSHF are empty, then the TXEMPTY bit is also set. 

You can transmit data by: 

1. Polling Transmit Ready Flag 

2. Transmit Interrupt 3. DMA 

In polling method, software can poll for the TXRDY bit to go high before writing the data to the TD0. The CPU is unnecessarily overloaded by selecting the polling method. To avoid this, you can use the interrupt or DMA method. To use the interrupt method, the SETXINT bit is set. To use the DMA method, the SET_TX_DMA bit is set. Either an interrupt or a DMA request is generated the moment the TXRDY bit is set. When the LIN has completed transmission of all pending frames, the SCITXSHF register and the TD0 are empty, the TXRDY bit is set, and an interrupt/DMA request is generated, if enabled. Because all data has been transmitted, the interrupt/DMA request can be halted. This can either be done by disabling the transmit interrupt (CLRTXINT)/DMA request (CLRTXDMA bit) or by disabling the transmitter (clear TXENA bit). If the checksum scheme is enabled by setting the Send Checksum (SC) bit to 1, the checksum byte is sent after the current byte transmission. The SC bit is cleared after the checksum byte has been transmitted. 

## **Note** 

The TXRDY flag cannot be cleared by reading the corresponding interrupt offset in the SCIINTVECT0 or SCIINTVECT1 register. 

## _**13.4.2.4.4.2.2 Transmitting Data in Multibuffer Mode**_ 

Multibuffer mode is selected when the MBUFMODE bit is set to 1. Like single-buffer mode, you can use the polling, DMA, or interrupt method to write the data to be transmitted. The transmitted data has to be written to the LINTD0 and LINTD1 registers, based on the number of bytes. LIN waits for data to be written to Byte 0 (TD0) of the LINTD0 register and transfers the programmed number of bytes to SCITXSHF to transmit one by one automatically. If the checksum scheme is enabled by setting the Send Checksum (SC) bit to 1, the checksum is sent after transmission of the last byte of the programmed number of data bytes, indicated by the LENGTH field. The SC bit is cleared after the checksum byte has been transmitted. 

## **13.4.2.5 Low-Power Mode** 

The LIN module can be put in either local or global low-power mode. Global low-power mode is asserted by the system and is not controlled by the LIN module. During global low-power mode, all clocks to the LIN are turned off so the module is completely inactive. If global low-power mode is requested while the receiver is receiving data, then the LIN completes the current reception and then enters the low-power mode, that is, module enters low-power mode only when Busy bit (SCIFLR.BUSY) is cleared. 

The LIN module can enter low-power mode either when there was no activity on the LINRX pin for more than 4 seconds (this can be either a constant recessive or dominant level) or when a Sleep Command frame was received. Once the Timeout flag (SCIFLR.TIMEOUT) was set or once a Sleep Command was received, the Power down bit (SCIGCR2.POWERDOWN) must be set by the application software to make the module enter local low-power mode. A wakeup signal terminates the sleep mode of the LIN bus. 

1592 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

## **Enabling Local Low-Power Mode During Receive and Transmit** 

If the wakeup interrupt is enabled and low-power mode is requested while the receiver is receiving data, then the LIN immediately generates a wakeup interrupt to clear the power-down bit. Thus, the LIN is prevented from entering low-power mode and completes the current reception. Otherwise, if the wakeup interrupt is disabled, the LIN completes the current reception and then enters the low-power mode. 

## _**13.4.2.5.1 Entering Sleep Mode**_ 

In LIN protocol, a sleep command is used to broadcast the sleep mode to all nodes. The sleep command consists of a diagnostic commander request frame with identifier 0x3C (60), with the first data field as 0x00. There must be no activity in the bus once all nodes receive the sleep command: the bus is in sleep mode. 

Local low-power mode is asserted by setting the POWERDOWN bit; setting this bit stops the clocks to the LIN internal logic and registers. Clearing the POWERDOWN bit causes LIN to exit from local low-power mode. All the registers are accessible during local power-down mode. If a register is accessed in low-power mode, this access results in enabling the clock to the module for that particular access alone. 

## _**13.4.2.5.2 Wakeup**_ 

The wakeup interrupt is used to allow the LIN module to automatically exit a low-power mode. A LIN wakeup is triggered when a low level is detected on the receive RX pin, and this clears the POWERDOWN bit. 

## **Note** 

If the wakeup interrupt is disabled, then the LIN enters low-power mode whenever the LIN is requested to do so, but a low level on the receive RX pin does not cause the LIN to exit low-power mode. 

In LIN mode, any node can terminate sleep mode by sending a wakeup signal, see Figure 13-210. A responder node that detects the bus in sleep mode, and with a wakeup request pending, sends a wakeup signal. The wakeup signal is a dominant value on the LIN bus for TWUSIG; this is at least 5 Tbits for the LIN bus baud rates. The wakeup signal is generated by sending a 0xF0 byte containing 5 dominant Tbits and 5 recessive Tbits. 

**==> picture [427 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
WAKEUP SIGNAL SYNCH BREAK<br>BUS IN<br>BUS IN SLEEP MODE OPERATIONAL MODE<br>T WUSIG T INITIALIZE<br>0.25ms ≤ TWUSIG ≤ 5ms<br>**----- End of picture text -----**<br>


## **Figure 13-210. Wakeup Signal Generation** 

Assuming a bus with no noise or loading effects, a write of 0xF0 to TD0 loads the transmitter to meet the wakeup signal timing requirement for TWUSIG. Then, setting the SCIGCR2.GENWU bit transmits the preloaded value in TD0 for a wakeup signal transmission. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1593 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Note** 

The SCIGCR2.GENWU bit can be set/reset only when SWnRST is set to 1 and the node is in power-down mode. The bit is cleared on a valid synch break detection. A commander sending a wakeup request, exits power-down mode upon reception of the wakeup pulse. The bit is cleared on a SWnRST. This can be used to stop a commander from sending further wakeup requests. 

## _**13.4.2.5.3 Wakeup Timeouts**_ 

The LIN protocol defines the following timeouts for a wakeup sequence. After a wakeup signal has been sent to the bus, all nodes wait for the commander to send a header. If no sync field is detected before 150ms (3,000 cycles at 20kHz) after a wakeup signal is transmitted, a new wakeup is sent by the same node that requested the first wakeup. This sequence is not repeated more than two times. After three attempts to wake up the LIN bus, wakeup signal generation is suspended for a 1.5s (30,000 cycles at 20kHz) period after three breaks. 

## **Note** 

To achieve compatibility to LIN1.3 timeout conditions, the MBRSR.MBR bit-field must be set to make sure that the LIN 2.0 (real-time-based) timings meet the LIN 1.3 bit time base. A node triggering the wakeup can set the MBRSR register accordingly to meet the targeted time as 128 Tbits × programmed prescaler. 

The LIN handles the wakeup expiration times defined by the LIN protocol with a hardware implementation. 

## **13.4.2.6 Emulation Mode** 

In emulation mode, the SCIGCR1.CONT bit determines how the LIN operates when the program is suspended. The LIN counters are affected by this bit during debug mode. When this bit is set, the counters are running even when a debug halt occurs. When cleared, the counters stop counting when a debug halt occurs. 

Any reads in emulation mode to a LIN register do not have any effect on the flags in the SCIFLR register. 

## **Note** 

When emulation mode is entered during a frame transmission or reception and the SCIGCR1.CONT bit is not set, communication is not expected to be successful. The suggested usage is to set the SCIGRC1.CONT bit during emulation mode for successful communication. 

1594 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.4.2.7 LIN Programming Guide** 

## **Driver Information** 

Driver features are available at the LIN driver page . 

## **Software API Information** 

The LIN driver provides an API to configure the LIN module. Full documentation is located on APIs for LIN . 

## **Example Usage** 

The below links shows an example on how to use LIN. 

- LIN: 

   - LIN Internal Loopback (Interrupt-based) 

   - LIN/SCI Internal Loopback (Interrupt-based) 

   - LIN/SCI DMA Loopback 

   - LIN Internal Loopback (Polling-based) 

   - LIN External Commander 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1595 

Copyright © 2025 Texas Instruments Incorporated 

