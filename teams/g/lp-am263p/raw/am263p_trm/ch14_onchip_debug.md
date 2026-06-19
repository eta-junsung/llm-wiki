<!-- AM263P TRM | 14 On-Chip Debug | 원본 p.1694-1718 | pymupdf4llm text+tables, images omitted -->

_On-Chip Debug_ 

www.ti.com 

## _Chapter 14_ _**On-Chip Debug**_ 

**==> picture [506 x 40] intentionally omitted <==**

The debug subsystem contains the OneMCU DEBUGSS at its core and enables JTAG interface access to device components. The debug subsystem is designed to provide the following debug features: 

- JTAG debug access to debug resources, mapped through an ARM SWJ-DP and TI ICEPickM scan module 

- System memory access without halting the processor 

- ETM-based trace for ARM R5F 

- Cross trigger to halt and restart cores and peripherals based on events such as watchdog, timers, DMA, and time-stamp events 

- Capability to read the device ID data 

**14.1 On-Chip Debug** ..................................................................................................................................................... 1695 **14.2 Arm[®] Debug Links** ................................................................................................................................................1718 

1694 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

## **14.1 On-Chip Debug** 

This chapter describes the on-chip debug support, including details on the various capabilities and features available through the SoC debug framework. 

## _**14.1.1 On-Chip Debug Overview**_ 

This chapter describes the properties and capabilities of the various features available through the On-Chip Debug framework deployed on this device - also known as Debug SS. 

The On-Chip Debug framework enables various Debug and Trace use-cases, including: 

- JTAG Tooling – Access to on-chip debug resources is supported by an IEEE 1149.1 (JTAG) compliant interface that is supported by an Arm® CoreSight™ DAP JTAG-DP. 

- Self-Hosted Tooling – code running on programmable cores within the device is able to use on-chip debug resources to enable embedded tooling solutions. 

- PCB-level interconnect testing – IEEE 1149.1 and IEEE 1149.6 compliant Boundary Scan supports product level integration testing 

- Stop Mode debugging – Debug of embedded processors is supported using various mechanisms that can halt the pipeline of a CPU. Breakpoints (Software and Hardware), Watchpoints, Cross-Triggering, and Ondemand (e.g. user requested) halt request mechanisms may be supported based on the capabilities of a given processor. 

- Debug-aware Peripherals – Peripheral awareness of processor execution state allows safe suspension of peripheral operation. Supported by select peripherals. 

- Synchronized Debug – Wide deployment of Cross-Triggering allows multiple processors and/or debug elements to be grouped together to process various actions based on a common event occurrence. 

- Processor Trace – Support for the generation of a trace stream with the encoding of processor state that may include some combination of program flow, timing details (execution and stall), and memory references (address and/or data) with the goal of facilitating processor state reconstruction for debug purposes. 

- Software Messaging Trace – Support for software messaging trace where embedded code running within the device can be instrumented to use memory writes to send important debug information to a trace stream. 

- Trace Correlation (through timestamping) – Support for the correlation of different trace streams is enabled through the use of a common global timestamp that is distributed to supported trace sources. 

- Trace data movement – Trace data movement on chip is supported using standard Arm ATB trace infrastructure components. Concurrent use of the trace bus by multiple trace sources is supported, with each trace source identifiable through a unique ID. An Arm® CoreSight™ Trace Router supports sending a trace stream off-chip (TPIU), to dedicated memory on-chip (ETB), or broadcasted to both (TPIU + ETB). 

- The trace buffer used for trace data movement is ARM CSETB 32KB. Refer to ARM CSETB TRM for more details. 

- On-Chip trace collection via dedicated buffer – An on-chip trace buffer is supported by logic that implements capturing trace data until either the memory fills (stop-on-full, system-bridge) or continuously until a request to stop is received (circular buffer). Interleaving of multiple trace streams is made possible through the use of a standardized encoding that embeds trace data along with the corresponding trace source ID. 

- Trace export over TPIU – Trace data is exported over device LVCMOS pins using a standard protocol that embeds trace data along with the corresponding trace source ID. 

## _**14.1.2 On-Chip Debug Features**_ 

The On-Chip Debug framework provides a comprehensive hardware platform for a rich debug and development experience. The On-Chip Debug framework in this device supports these features: 

- An IEEE 1149.1 (JTAG and Boundary Scan) compliant device interface to provide debug access to debug resources through ARM SWJ-DP module. 

- System Memory access without halting the processors 

- Trace port device interface 

- ETM based program flow trace for ARM R5F 

- Software instrumentation trace using STM 

- Breakpoint-based debug 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1695 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

- Cross-trigger to halt and restart various R5F cores and M4 CPU based on SOC internal and external events such as timers and other peripheral interrupts 

- Trace capture on-chip via dedicated buffer 

- Arm® CoreSight™ compliant debug components deployed to streamline 3rd party tooling support 

## _**14.1.3 On-Chip Debug Functional Description**_ 

## **14.1.3.1 On-Chip Debug Block Diagram** 

The Debug subsystem is responsible for supporting the debug features of this device. 

An overview of the interconnectivity of the debug ports and trace ports are shown in Figure 14-1. 

**==> picture [434 x 166] intentionally omitted <==**

**Figure 14-1. Debug SS Overview** 

A logical partitioning of the On-Chip Debug features deployed on this device is illustrated in Figure 14-2. 

1696 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

**==> picture [396 x 307] intentionally omitted <==**

**Figure 14-2. On Chip Debug Block Diagram** 

## **14.1.3.2 Device Interfaces** 

On-Chip Debug features are supported through two device interfaces. 

**JTAG** : IEEE 1149.1 compliant interface that provides access to Boundary Scan and acts as the primary interface for off-chip access to On-Chip debug resources (see Section 14.1.3.2.1). 

**Trace Port** : Arm TPIU compliant Trace Port interface is used to facilitate export of trace (see Section 14.1.3.2.2). 

Texas Instruments supports a variety of eXtended Development System (XDS) JTAG controllers with various debug capabilities beyond only JTAG support. The following document is a good reference for guidelines: Emulation and Trace Headers. More information can also be found here:XDS Target Connection Guide. 

## _**14.1.3.2.1 JTAG Interface**_ 

**Table 14-1. JTAG Interface Signals** 

|**Signal Name**|**I/O Type**|**Description**|
|---|---|---|
|TCK|I|_Test Clock_. Controls the timing of the test interface independently from any<br>system clocks. TCK is pulsed by the equipment controlling the test and not<br>by the tested device.|
|TMS|I|_Test Mode Select_. Controls the transitions of the test interface state<br>machine|
|TDI|I|_Test Data Input_. Supplies the data to the JTAG registers|
|TDO|O/Z|_Test Data Output_. Used to serially output the data from the JTAG registers<br>to the equipment controlling the test.|



## _**14.1.3.2.2 Trace Port Interface**_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1697 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

**Table 14-2. Trace Port Signals** 

|**Signal Name**|**I/O Type**|**Description**|
|---|---|---|
|TRC_CLK|O|Trace Clock|
|TRC_CTL|O|Trace Control|
|TRC_DATA[15:0]|O|Trace Data|



## **Note** 

The Trace Port interface signals are associated with device pins that are multiplexed with other signal functions. 

## **14.1.3.3 Debug and Boundary Scan Access and Control** 

On-Chip debug resources are made available through two mechanisms: 

- JTAG access via DAP and related APs 

- JTAG access via Boundary Scan TAP 

## _**14.1.3.3.1 DAP**_ 

Off-chip debug tools are able to access On-Chip debug resources via the JTAG interface. 

A CoreSight™ Compliant DAP architecture provides access via a DP and a collection of APs: 

- SWJ-DP: Arm® CoreSight™ compliant SWJ Debug Port provides support for a JTAG interface with a 4-bit IR Note: Even though an SWJ-DP is implemented on-chip, only JTAG is supported. This device does not support SWD. 

- APB-AP: Arm® CoreSight™ APB Access Port provides access to the Debug-APB address space which is the primary configuration space for On-Chip Debug resources. 

- AHB-AP: Arm® CoreSight™ AHB Access Port provides access to the SoC address space, allowing visibility and control over system resources. 

- Config-AP: TI Configuration AP supports access to SoC debug management registers 

- Power-AP: TI Configuration AP supports reset management 

The DAPBUS Interconnect functions in the DebugSS core clock domain. DAPBUS Async bridges are implemented DAPBUS and the Security-AP controller (Security logic clock), and the DAPBUS and the AHB-AP (system bus clock). 

**==> picture [346 x 76] intentionally omitted <==**

DAP logically consists of two parts, the Debug Port and the Access Ports, it supports two types of access: 

- Access to the Debug Port (DP) registers. This is provided by Debug Port accesses (DPACC). 

- Access to the Access Port (AP) registers. This is provided by Access Port accesses (APACC). 

A DAP can include multiple Access Ports. An AP is responsible for accessing debug component registers, such as processor debug logic, ETM and trace port registers. These accesses are made in response to APACC accesses in a manner defined by the AP. The DebugSS has core DAPBUS interconnect that maps the controller interface of the SWJ-DP to the target interfaces on the various APs and CortexM ports. Table below shows the mapping of the targets on the interconnect. 

**Table 14-3. DAPBUS Address Mapping** 

|**APSEL**|**Target**|
|---|---|
|0x0|CortexM[0]|



1698 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

**Table 14-3. DAPBUS Address Mapping (continued)** 

|**APSEL**|**Target**|
|---|---|
|0x1|Reserved|
|0x2|Reserved|
|0x3|Reserved|
|0x4|CFG-AP|
|0x5|APB-AP*|
|0x6|AHB-AP*|
|0x7|Power-AP*|
|0x8|Security-AP*|
|0x9|Reserved|
|0xA|Reserved|
|0xB - 0xFF|Reserved|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1699 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

## _**14.1.3.3.1.1 Debug Subsystem Address Map**_ 

The memory map view for DAP AHB is the same as SOC memory map view seen by Cortex R5F CPU (except for dedicated R5F Core memories and peripherals). 

Table 14-4 shows the APB AP address map for this device. 

**Table 14-4. APB AP Memory Map** 

|**APB PORT**|**Block Name**|**Start Address**|**End Address**|**Size**|**Register Details**|
|---|---|---|---|---|---|
|APB INTERNAL PORT0|Debugss ROM Table|0x0000 0000|0x0000 0FFF|4KB|ROM LUT|
|APB INTERNAL PORT0|Debugss CTI|0x0000 1000|0x0000 1FFF|4KB|CTI register summary|
|APB INTERNAL PORT0|Debugss TPIU|0x0000 2000|0x0000 2FFF|4KB|TPIU register summary|
|APB EXTERNAL PORT 0|Ext Port0 ROM TABLE|0x0001 0000|0x0001 0FFF|4KB|ROM LUT|
|APB EXTERNAL PORT 0|ATB REPLICATOR|0x0001 1000|0x0001 1FFF|4KB|ATB register summary|
|APB EXTERNAL PORT 0|CSETB|0x0001 2000|0x0001 2FFF|4KB|ETB register summary|
|APB EXTERNAL PORT 0|STM|0x0001 3000|0x0001 3FFF|4KB||
|APB EXTERNAL PORT 0|STM-CTI|0x0001 4000|0x0001 4FFF|4KB|CTI register summary|
|APB EXTERNAL PORT 0|HSM CM4 CTI|0x0001 5000|0x0001 5FFF|4KB|CTI register summary|
|APB EXTERNAL PORT 1|R5SS0 ROM Table|0x0002 0000|0x0002 0FFF|4KB|ROM LUT|
|APB EXTERNAL PORT 1|R5SS0 CPU0|0x0003 0000|0x0003 0FFF|4KB|R5 Core Debug Register Summary|
|APB EXTERNAL PORT 1|R5SS0 CPU1|0x0003 2000|0x0003 2FFF|4KB|R5 Core Debug Register Summary|
|APB EXTERNAL PORT 1|R5SS0 CPU0 CTI|0x0003 8000|0x0003 8FFF|4KB|CTI register summary|
|APB EXTERNAL PORT 1|R5SS0 CPU1 CTI|0x0003 9000|0x0003 9FFF|4KB|CTI register summary|
|APB EXTERNAL PORT 1|R5SS0 CPU0 ETM|0x0003 C000|0x0003 CFFF|4KB|ETM register summary|
|APB EXTERNAL PORT 1|R5SS0 CPU1 ETM|0x0003 D000|0x0003 DFFF|4KB|ETM register summary|
|APB EXTERNAL PORT 2|R5SS1 ROM Table|0x0004 0000|0x0004 0FFF|4KB|ROM LUT|
|APB EXTERNAL PORT 2|R5SS1 CPU0|0x0005 0000|0x0005 0FFF|4KB|R5 Core Debug Register Summary|
|APB EXTERNAL PORT 2|R5SS1 CPU1|0x0005 2000|0x00052FFF|4KB|R5 Core Debug Register Summary|
|APB EXTERNAL PORT 2|R5SS1 CPU0 CTI|0x0005 8000|0x00058FFF|4KB|CTI register summary|
|APB EXTERNAL PORT 2|R5SS1 CPU1 CTI|0x0005 9000|0x00059FFF|4KB|CTI register summary|
|APB EXTERNAL PORT 2|R5SS1 CPU0 ETM|0x0005 C000|0x0005CFFF|4KB|ETM register summary|
|APB EXTERNAL PORT 2|R5SS1 CPU1 ETM|0x0005 D000|0x0005DFFF|4KB|ETM register summary|



## **CTI register summary** 

Seehere for more details on the below registers: 

1700 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|CTICONTROL|0x000|RW|0x00000000|CTI Control Register|
|CTIINTACK|0x010|WO|0x00000000|CTI Interrupt Acknowledge Register|
|CTIAPPSET|0x014|RW|0x00000000|CTI Application Trigger Set Register|
|CTIAPPCLEAR|0x018|WO|0x00000000|CTI Application Trigger Clear Register|
|CTIAPPPULSE|0x01C|WO|0x00000000|CTI Application Pulse Register|
|CTIINEN0|0x020|RW|0x00000000|CTI Trigger 0 to Channel Enable Register|
|CTIINEN1|0x024|RW|0x00000000|CTI Trigger 1 to Channel Enable Register|
|CTIINEN2|0x028|RW|0x00000000|CTI Trigger 2 to Channel Enable Register|
|CTIINEN3|0x02C|RW|0x00000000|CTI Trigger 3 to Channel Enable Register|
|CTIINEN4|0x030|RW|0x00000000|CTI Trigger 4 to Channel Enable Register|
|CTIINEN5|0x034|RW|0x00000000|CTI Trigger 5 to Channel Enable Register|
|CTIINEN6|0x038|RW|0x00000000|CTI Trigger 6 to Channel Enable Register|
|CTIINEN7|0x03C|RW|0x00000000|CTI Trigger 7 to Channel Enable Register|
|CTIOUTEN0|0x0A0|RW|0x00000000|CTI Channel to Trigger 0 Enable Register|
|CTIOUTEN1|0x0A4|RW|0x00000000|CTI Channel to Trigger 1 Enable Register|
|CTIOUTEN2|0x0A8|RW|0x00000000|CTI Channel to Trigger 2 Enable Register|
|CTIOUTEN3|0x0AC|RW|0x00000000|CTI Channel to Trigger 3 Enable Register|
|CTIOUTEN4|0x0B0|RW|0x00000000|CTI Channel to Trigger 4 Enable Register|
|CTIOUTEN5|0x0B4|RW|0x00000000|CTI Channel to Trigger 5 Enable Register|
|CTIOUTEN6|0x0B8|RW|0x00000000|CTI Channel to Trigger 6 Enable Register|
|CTIOUTEN7|0x0BC|RW|0x00000000|CTI Channel to Trigger 7 Enable Register|
|CTITRIGINSTATUS|0x130|RO|0x00000000|CTI Trigger In Status Register|
|CTITRIGOUTSTATUS|0x134|RO|0x00000000|CTI Trigger Out Status Register|
|CTICHINSTATUS|0x138|RO|0x00000000|CTI Channel In Status Register|
|CTICHOUTSTATUS|0x13C|RO|0x00000000|CTI Channel Out Status Register|
|CTIGATE|0x140|RW|0x0000000F|Enable CTI Channel Gate Register|
|ASICCTL|0x144|RW|0x00000000|External Multiplexer Control Register|
|ITCHINACK|0xEDC|WO|0x00000000|ITCHINACK Register|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1701 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|ITTRIGINACK|0xEE0|WO|0x00000000|ITTRIGINACK Register|
|ITCHOUT|0xEE4|WO|0x00000000|ITCHOUT Register|
|ITTRIGOUT|0xEE8|WO|0x00000000|ITTRIGOUT Register|
|ITCHOUTACK|0xEEC|RO|0x00000000|ITCHOUTACK Register|
|ITTRIGOUTACK|0xEF0|RO|0x00000000|ITTRIGOUTACK Register|
|ITCHIN|0xEF4|RO|0x00000000|ITCHIN Register|
|ITTRIGIN|0xEF8|RO|0x00000000|ITTRIGIN Register|
|ITCTRL|0xF00|RW|0x00000000|Integration Mode Control Register|
|CLAIMSET|0xFA0|RW|0x0000000F|Claim Tag Set Register|
|CLAIMCLR|0xFA4|RW|0x00000000|Claim Tag Clear Register|
|LAR|0xFB0|WO|0x00000000|Lock Access Register|
|LSR|0xFB4|RO|0x00000003|Lock Status Register|
|AUTHSTATUS|0xFB8|RO|0x00000005|Authentication Status Register|
|DEVID|0xFC8|RO|0x00040800|Device Configuration Register|
|DEVTYPE|0xFCC|RO|0x00000014|Device Type Identifier Register|
|PIDR4|0xFD0|RO|0x00000004|Peripheral ID4 Register|
|PIDR5|0xFD4|RO|0x00000000|Peripheral ID5 Registers|
|PIDR6|0xFD8|RO|0x00000000|Peripheral ID6 Registers|
|PIDR7|0xFDC|RO|0x00000000|Peripheral ID7 Registers|
|PIDR0|0xFE0|RO|0x00000006|Peripheral ID0 Register|
|PIDR1|0xFE4|RO|0x000000B9|Peripheral ID1 Register|
|PIDR2|0xFE8|RO|0x0000003B|Peripheral ID2 Register|
|PIDR3|0xFEC|RO|0x00000000|Peripheral ID3 Register|
|CIDR0|0xFF0|RO|0x0000000D|Component ID0 Register|
|CIDR1|0xFF4|RO|0x00000090|Component ID1 Register|
|CIDR2|0xFF8|RO|0x00000005|Component ID2 Register|
|CIDR3|0xFFC|RO|0x000000B1|Component ID3 Register|



1702 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

## **ETB Register Summary** 

See here for more details on the below registers: 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|RDP|0x004|RO|0x00000000|ETB RAM Depth Register|
|STS|0x00C|RO|0x00000008|ETB Status Register|
|RRD|0x010|RO|0x00000000|ETB RAM Read Data Register|
|RRP|0x014|RW|0x00000000|ETB RAM Read Pointer Register|
|RWP|0x018|RW|0x00000000|ETB RAM Write Pointer Register|
|TRG|0x01C|RW|0x00000000|ETB Trigger Counter Register|
|CTL|0x020|RW|0x00000000|ETB Control Register|
|RWD|0x024|WO|0x00000000|ETB RAM Write Data Register|
|FFSR|0x300|RO|0x00000002|ETB Formatter and Flush Status Register|
|FFCR|0x304|RW|0x00000000|ETB Formatter and Flush Control Register|
|ITMISCOP0|0xEE0|WO|0x00000000|Integration Test Miscellaneous Output Register 0|
|ITTRFLINACK|0xEE4|WO|0x00000000|Integration Test Trigger In and Flush In Acknowledge Register|
|ITTRFLIN|0xEE8|RO|0x00000000|Integration Test Trigger In and Flush In Register|
|ITATBDATA0|0xEEC|RO|0x00000000|Integration Test ATB Data Register 0|
|ITATBCTR2|0xEF0|WO|0x00000000|Integration Test ATB Control Register 2|
|ITATBCTR1|0xEF4|RO|0x00000000|Integration Test ATB Control Register 1|
|ITATBCTR0|0xEF8|RO|0x00000000|Integration Test ATB Control Register 0|
|ITCTRL|0xF00|RW|0x00000000|Integration Mode Control Register|
|CLAIMSET|0xFA0|RW|0x0000000F|Claim Tag Set Register|
|CLAIMCLR|0xFA4|RW|0x00000000|Claim Tag Clear Register|
|LAR|0xFB0|WO|0x00000000|Lock Access Register|
|LSR|0xFB4|RO|0x00000003|Lock Status Register|
|AUTHSTATUS|0xFB8|RO|0x00000000|Authentication Status Register|
|DEVID|0xFC8|RO|0x00000000|Device Configuration Register|
|DEVTYPE|0xFCC|RO|0x00000021|Device Type Identifier Register|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1703 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|PIDR4|0xFD0|RO|0x00000004|Peripheral ID4 Register|
|PIDR5|0xFD4|RO|0x00000000|Peripheral ID5 Registers|
|PIDR6|0xFD8|RO|0x00000000|Peripheral ID6 Registers|
|PIDR7|0xFDC|RO|0x00000000|Peripheral ID7 Registers|
|PIDR0|0xFE0|RO|0x00000007|Peripheral ID0 Register|
|PIDR1|0xFE4|RO|0x000000B9|Peripheral ID1 Register|
|PIDR2|0xFE8|RO|0x0000003B|Peripheral ID2 Register|
|PIDR3|0xFEC|RO|0x00000000|Peripheral ID3 Register|
|CIDR0|0xFF0|RO|0x0000000D|Component ID0 Register|
|CIDR1|0xFF4|RO|0x00000090|Component ID1 Register|
|CIDR2|0xFF8|RO|0x00000005|Component ID2 Register|
|CIDR3|0xFFC|RO|0x000000B1|Component ID3 Register|



## **ATB Register Summary** 

See here for more details on the below registers: 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|Ctrl_Reg|0x000|RW|0x00000300|Funnel Control Register|
|Priority_Ctrl_Reg|0x004|RW|0x00000000|Priority Control Register|
|ITATBDATA0|0xEEC|RW|0x00000000|Integration Test ATB Data0 Register|
|ITATBCTR2|0xEF0|RW|0x00000000|Integration Test ATB Control 2 Register|
|ITATBCTR1|0xEF4|RW|0x00000000|Integration Test ATB Control 1 Register|
|ITATBCTR0|0xEF8|RW|0x00000000|Integration Test ATB Control 0 Register|
|ITCTRL|0xF00|RW|0x00000000|Integration Mode Control Register|
|CLAIMSET|0xFA0|RW|0x0000000F|Claim Tag Set Register|
|CLAIMCLR|0xFA4|RW|0x00000000|Claim Tag Clear Register|
|LOCKACCESS|0xFB0|WO|0x00000000|Lock Access Register|
|LOCKSTATUS|0xFB4|RO|0x00000003|Lock Status Register|
|AUTHSTATUS|0xFB8|RO|0x00000000|Authentication Status Register|



1704 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|DEVID|0xFC8|RO|0x00000038|Device Configuration Register|
|DEVTYPE|0xFCC|RO|0x00000012|Device Type Identifier Register|
|PIDR4|0xFD0|RO|0x00000004|Peripheral ID4 Register|
|PIDR5|0xFD4|RO|0x00000000|Peripheral ID5 Registers|
|PIDR6|0xFD8|RO|0x00000000|Peripheral ID6 Registers|
|PIDR7|0xFDC|RO|0x00000000|Peripheral ID7 Registers|
|PIDR0|0xFE0|RO|0x00000008|Peripheral ID0 Register|
|PIDR1|0xFE4|RO|0x000000B9|Peripheral ID1 Register|
|PIDR2|0xFE8|RO|0x0000002B|Peripheral ID2 Register|
|PIDR3|0xFEC|RO|0x00000000|Peripheral ID3 Register|
|CIDR0|0xFF0|RO|0x0000000D|Component ID0 Register|
|CIDR1|0xFF4|RO|0x00000090|Component ID1 Register|
|CIDR2|0xFF8|RO|0x00000005|Component ID2 Register|
|CIDR3|0xFFC|RO|0x000000B1|Component ID3 Register|



## **STM Register Summary** 

See here for more details on the below registers: 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|STMDMASTARTR|0xC04|WO|-|ARM STM Specification|
|STMDMASTOPR|0xC08|WO|-|ARM STM Specification|
|STMDMASTATR|0xC0C|RO|-|ARM STM Specification|
|STMDMACTLR|0xC10|RW|0x00000000|DMA Control Register|
|STMDMAIDR|0xCFC|RO|0x00000002|ARM STM Specification|
|STMHEER|0xD00|RW|-|ARM STM Specification|
|STMHETER|0xD20|RW|-|ARM STM Specification|
|STMHEBSR|0xD60|RW|0x00000000|ARM STM Specification|
|STMHEMCR|0xD64|RW|0x00000000|ARM STM Specification|
|STMHEEXTMUXR|0xD68|RW|0x00000000|Hardware Event External Multiplex Control Register|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1705 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|STMHEMASTR|0xDF4|RO|0x00000080|Hardware Event Initiator Number Register|
|STMHEFEAT1R|0xDF8|RO|0x30200035|Hardware Event Features 1 Register|
|STMHEIDR|0xDFC|RO|0x00000011|Hardware Event ID Register|
|STMSPER|0xE00|RW|0x00000000|ARM STM Specification|
|STMSPTER|0xE20|RW|0x00000000|ARM STM Specification|
|STMSPSCR|0xE60|RW|0x00000000|ARM STM Specification|
|STMSPMSCR|0xE64|RW|0x00000000|ARM STM Specification|
|STMSPOVERRIDER|0xE68|RW|0x00000000|ARM STM Specification|
|STMSPMOVERRIDER|0xE6C|RW|0x00000000|ARM STM Specification|
|STMSPTRIGCSR|0xE70|RW|0x00000000|ARM STM Specification|
|STMTCSR|0xE80|RW|-|Trace Control and Status Register|
|STMTSSTIMR|0xE84|WO|-|ARM STM Specification|
|STMTSFREQR|0xE8C|RW|0x00000000|ARM STM Specification|
|STMSYNCR|0xE90|RW|0x00000000|ARM STM Specification|
|STMAUXCR|0xE94|RW|0x00000000|Auxiliary Control Register|
|STMFEAT1R|0xEA0|RO|0x006587D1|STM Features 1 Register|
|STMFEAT2R|0xEA4|RO|0x000114F2|STM Features 2 Register|
|STMFEAT3R|0xEA8|RO|0x0000007F|STM Features 3 Register|
|STMITTRIGGER|0xEE8|WO|-|Integration Test for Cross-trigger Outputs Register|
|STMITATBDATA0|0xEEC|WO|-|Integration Mode ATB Data 0 Register|
|STMITATBCTR2|0xEF0|RO|-|Integration Mode ATB Control 2 Register|
|STMITATBID|0xEF4|WO|-|Integration Mode ATB Identification Register|
|STMITATBCTR0|0xEF8|WO|-|Integration Mode ATB Control 0 Register|
|STMITCTRL|0xF00|RW|0x00000000|Integration Mode Control Register|
|STMCLAIMSET|0xFA0|RW|0x0000000F|ARM STM Specification|
|STMCLAIMCLR|0xFA4|RW|0x00000000|ARM STM Specification|
|STMLAR|0xFB0|WO|-|Lock Access Register|
|STMLSR|0xFB4|RO|-|Lock Status Register|



1706 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|STMAUTHSTATUS|0xFB8|RO|0x000000AA|Authentication Status Register|
|STMDEVARCH|0xFBC|RO|0x47710A63|Device Architecture Register|
|STMDEVID|0xFC8|RO|0x00010000|Device Configuration Register|
|STMDEVTYPE|0xFCC|RO|0x00000063|Device Type Identifier Register|
|STMPIDR0|0xFE0|RO|0x00000063|Peripheral ID0 Register|
|STMPIDR1|0xFE4|RO|0x000000B9|Peripheral ID1 Register|
|STMPIDR2|0xFE8|RO|0x0000000B|Peripheral ID2 Register|
|STMPIDR3|0xFEC|RO|0x00000000|Peripheral ID3 Register|
|STMPIDR4|0xFD0|RO|0x00000004|Peripheral ID4 Register|
|STMCIDR0|0xFF0|RO|0x0000000D|Component ID0 Register|
|STMCIDR1|0xFF4|RO|0x00000090|Component ID1 Register|
|STMCIDR2|0xFF8|RO|0x00000005|Component ID2 Register|
|STMCIDR3|0xFFC|RO|0x000000B1|Component ID3 Register|



## **ETM Register Summary** 

See here for more details on the below registers: 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|ETMCR|0x000|RW|0x00000441|Main Control Register|
|ETMCCR|0x004|RO|0x8D014024|Configuration Code Register|
|ETMTRIGGER|0x008|RW|-|Trigger Event Register in the ARM ETM Specification|
|ETMASICCTLR|0x00C|RW|0x00000000|ASIC Control Register|
|ETMSR|0x010|RW|-|ETM Status Register in the ARM ETM Specification|
|ETMSCR|0x014|RO|0x00020C0C|System Configuration Register in the ARM ETM Specification|
|ETMTSSCR|0x018|RW|-|TraceEnable Start/Stop Control Register in the ARM ETM<br>Specification|
|ETMTECR2|0x01C|RW|-|TraceEnable Control 2 Register in the ARM ETM Specification|
|ETMTEEVR|0x020|RW|-|TraceEnable Event Register in the ARM ETM Specification|
|ETMTECR1|0x024|RW|-|TraceEnable Control 1 Register in the ARM ETM Specification|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1707 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|ETMFFLR[e]|0x02C|RW|-|FIFOFULL Level Register in the ARM ETM Specification|
|ETMVDEVR|0x030|RW|-|ViewData Event Register in the ARM ETM Specification|
|ETMVDCR1|0x034|RW|-|ViewData Control 1 Register in the ARM ETM Specification|
|ETMVDCR3|0x03C|RW|-|ViewData Control 3 Register in the ARM ETM Specification|
|ETMACVR1-8|0x40 - 0x58|RW|-|Address Comparator Value Registers in the ARM ETM<br>Specification|
|ETMACTR1-8|0x80 - 0x98|RW|-|Address Comparator Access Type Registers in the ARM ETM<br>Specification|
|ETMDCVR1[f]|0x0C0|RW|-|Data Comparator Value Registers in the ARM ETM Specification|
|ETMDCVR3[f]|0x0D0|RW|-|Data Comparator Value Registers in the ARM ETM Specification|
|ETMDCMR1[f]|0x100|RW|-|Data Comparator Mask Registers in the ARM ETM Specification|
|ETMDCMR3[f]|0x110|RW|-|Data Comparator Mask Registers in the ARM ETM Specification|
|ETMCNTRLDVR1-2|0x140, 0x144|RW|-|Counter Reload Value Registers in the ARM ETM Specification|
|ETMCNTENR1-2|0x150, 0x154|RW|-|Counter Enable Registers in the ARM ETM Specification|
|ETMCNTRLDEVR1-2|0x160, 0x164|RW|-|Counter Reload Event Registers in the ARM ETM Specification|
|ETMCNTVR1-2|0x170, 0x174|RW|-|Counter Value Registers in the ARM ETM Specification|
|ETMSQEVR|0x180 - 0x194|RW|-|Sequencer State Transition Event Registers in the ARM ETM<br>Specification|
|ETMSQR|0x19C|RW|-|Current Sequencer State Register in the ARM ETM Specification|
|ETMEXTOUTEVR1-2|0x1A0, 0x1A4|RW|-|External Output Event Registers in the ARM ETM Specification|
|ETMCIDCVR|0x1B0|RW|-|Context ID Comparator Value Registers in the ARM ETM<br>Specification|
|ETMCIDCMR|0x1BC|RW|-|Context ID Comparator Mask Register in the ARM ETM<br>Specification|
|ETMSYNCFR|0x1E0|RW|0x00000400|Synchronization Frequency Register in the ARM ETM<br>Specification|
|ETMIDR|0x1E4|RO|0x4104F23x|ID Register|
|ETMCCER|0x1E8|RO|0x000009BA|Configuration Code Extension Register|
|ETMEXTINSELR|0x1EC|RW|-|Extended External Input Selection Register|



1708 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|ETMTRACEIDR|0x200|RW|0x00000000|CoreSight Trace ID Register in the ARM ETM Specification|
|ETMPDSR|0x314|RO|-|Power-Down Status Register|
|ITETMIF|0xED8|RO [h]|-|Processor-ETM Interface Register|
|ITMISCOUT|0xEDC|WO|-|Miscellaneous Outputs Register|
|ITMISCIN|0xEE0|RO [h]|-|Miscellaneous Inputs Register|
|ITTRIGGERACK|0xEE4|RO [h]|-|Trigger Acknowledge Register|
|ITTRIGGERREQ|0xEE8|WO|-|Trigger Request Register|
|ITATBDATA0|0xEEC|WO|-|ATB Data Register 0|
|ITATBCTR2|0xEF0|RO [h]|-|ATB Control Register 2|
|ITATBCTR1|0xEF4|WO|-|ATB Control Register 1|
|ITATBCTR0|0xEF8|WO|-|ATB Control Register 0|
|ETMITCTRL|0xF00|RW|0x00000000|Integration Mode Control Register in the ARM ETM Specification|
|ETMCLAIMSET|0xFA0|RW|0x000000FF|Claim Tag Set Register in the ARM ETM Specification|
|ETMCLAIMCLR|0xFA4|RW|0x00000000|Claim Tag Clear Register in the ARM ETM Specification|
|ETMLAR|0xFB0|WO|-|Lock Access Register in the ARM ETM Specification|
|ETMLSR|0xFB4|RO|0x00000003|Lock Status Register in the ARM ETM Specification|
|ETMAUTHSTATUS|0xFB8|RO|-|Authentication Status Register in the ARM ETM Specification|
|ETMDEVID|0xFC8|RO|0x00000000|CoreSight Device Configuration Register in the ARM ETM<br>Specification|
|ETMDEVTYPE|0xFCC|RO|0x00000013|CoreSight Device Type Register in the ARM ETM Specification|
|ETMPIDR0-7|0xFD0 - 0xFEC|RO|-|Peripheral Identification Registers|
|ETMCIDR0-3|0xFF0 - 0xFFC|RO|-|ETM Component Identification Registers|



## **TPIU Register Summary** 

See here for more details on the below registers: 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|TPIU_SPORTSZ|0x000|RO|0x00000001|Supported Port Size Register|
|TPIU_CPORTSZ|0x004|RW|0x00000001|Current Port Size Register|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1709 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|TPIU_STRIGM|0x100|RO|0x0000011F|Supported Trigger Modes Register|
|TPIU_TRIGCNT|0x104|RW|0x00000000|Trigger Counter Value Register|
|TPIU_TRIGMUL|0x108|RW|0x00000000|Trigger Multiplier Register|
|TPIU_STSTPTRN|0x200|RO|0x0003000F|Supported Test Patterns/Modes Register|
|TPIU_CTSTPTRN|0x204|RW|0x00000000|Current Test Pattern/Modes Register|
|TPIU_TPRCNTR|0x208|RW|0x00000000|TPIU Test Pattern Repeat Counter Register|
|TPIU_FFSTS|0x300|RO|0x00000000|Formatter and Flush Status Register|
|TPIU_FFCTRL|0x304|RW|0x00000000|Formatter and Flush Control Register|
|TPIU_FSCNTR|0x308|RW|0x00000040|Formatter Synchronization Counter Register|
|TPIU_EXCTLIN|0x400|RO|0x00000000|TPIU EXCTL Port Register - In|
|TPIU_EXCTLOUT|0x404|RW|0x00000000|TPIU EXCTL Port Register - Out|
|TPIU_ITTRFLINACK|0xEE4|WO|0x00000000|Integration Test Trigger In and Flush In Acknowledge Register|
|TPIU_ITTRFLIN|0xEE8|RO|0x00000000|Integration Test Trigger In and Flush In Register|
|TPIU_ITATBDATA0|0xEEC|RO|0x00000000|Integration Test ATB Data Register 0|
|TPIU_ITATBCTR2|0xEF0|WO|0x00000000|Integration Test ATB Control Register 2|
|TPIU_ITATBCTR1|0xEF4|RO|0x00000000|Integration Test ATB Control Register 1|
|TPIU_ITATBCTR0|0xEF8|RO|0x00000000|Integration Test ATB Control Register 0|
|TPIU_ITCTRL|0xF00|RW|0x00000000|Integration Mode Control Register|
|TPIU_CLAIMSET|0xFA0|RW|0x0000000F|Claim Tag Set Register|
|TPIU_CLAIMCLR|0xFA4|RW|0x00000000|Claim Tag Clear Register|
|TPIU_LAR|0xFB0|WO|0x00000000|Lock Access Register|
|TPIU_LSR|0xFB4|RO|0x00000003|Lock Status Register|
|TPIU_AUTHSTATUS|0xFB8|RO|0x00000000|Authentication Status Register|
|TPIU_DEVID|0xFC8|RO|0x000000A0|Device Configuration Register|
|TPIU_DEVTYPE|0xFCC|RO|0x00000011|Device Type Identifier Register|
|TPIU_PIDR4|0xFD0|RO|0x00000004|Peripheral ID4 Register|
|TPIU_PIDR5|0xFD4|RO|0x00000000|Peripheral ID5 Register|
|TPIU_PIDR6|0xFD8|RO|0x00000000|Peripheral ID6 Register|



1710 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

|**Name**|**Offset**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|
|TPIU_PIDR7|0xFDC|RO|0x00000000|Peripheral ID7 Register|
|TPIU_PIDR0|0xFE0|RO|0x00000012|Peripheral ID0 Register|
|TPIU_PIDR1|0xFE4|RO|0x000000B9|Peripheral ID1 Register|
|TPIU_PIDR2|0xFE8|RO|0x0000004B|Peripheral ID2 Register|
|TPIU_PIDR3|0xFEC|RO|0x00000000|Peripheral ID3 Register|
|TPIU_CIDR0|0xFF0|RO|0x0000000D|Component ID0 Register|
|TPIU_CIDR1|0xFF4|RO|0x00000090|Component ID1 Register|
|TPIU_CIDR2|0xFF8|RO|0x00000005|Component ID2 Register|
|TPIU_CIDR3|0xFFC|RO|0x000000B1|Component ID3 Register|



## **R5 Core Debug Register Summary** 

See here for more details on the below registers: 

|**Mnemonic**|**Register number**|**Offset**|**Access**|**Description**|
|---|---|---|---|---|
|DIDR|c0|0x000|R|CP14 c0, Debug ID Register|
|-|c1-c5|0x004-0x014|R|RAZ (Reads as zero)|
|WFAR|c6|0x18|RW|Watchpoint Fault Address Register|
|VCR|c7|0x01C|RW|Vector Catch Register|
|-|c8|0x020|R|RAZ (Reads as zero)|
|ECR|c9|0x024|RW|Not implemented. Reads as zero.|
|DSCCR|c10|0x028|RW|Debug State Cache Control Register|
|-|c11|0x02C|R|RAZ (Reads as zero)|
|-|c12-c31|0x030-0x07C|R|RAZ (Reads as zero)|
|DTRRX|c32|0x080|RW|Data Transfer Register|
|ITR|c33|0x084|W|Instruction Transfer Register|
|DSCR|c34|0x088|RW|CP14 c1, Debug Status and Control Register|
|DTRTX|c35|0x08C|RW|Data Transfer Register|
|DRCR|c36|0x090|W|Debug Run Control Register|
|-|c37-c63|0x094-0x0FC|R|RAZ (Reads as zero)|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1711 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

|**Mnemonic**|**Register number**|**Offset**|**Access**|**Description**|
|---|---|---|---|---|
|BVR|c64-c71|0x100-0x11C|RW|Breakpoint Value Registers|
|-|c72-c79|0x120-0x13C|R|RAZ (Reads as zero)|
|BCR|c80-c87|0x140-0x15C|RW|Breakpoint Control Registers|
|-|c88-c95|0x160-0x17C|R|RAZ (Reads as zero)|
|WVR|c96-c103|0x180-0x19C|RW|Watchpoint Value Registers|
|-|c104-c111|0x1A0-0x1BC|R|RAZ (Reads as zero)|
|WCR|c112-c119|0x1C0-0x1DC|RW|Watchpoint Control Registers|
|-|c120-c127|0x1E0-0x1FC|R|RAZ (Reads as zero)|
|-|c128-c191|0x200-0x2FC|R|RAZ (Reads as zero)|
|OSLAR|c192|0x300|R|Not implemented. Reads as zero.|
|OSLSR|c193|0x304|R|Operating System Lock Status Register|
|OSSRR|c194|0x308|R|Not implemented. Reads as zero.|
|-|c195|0x30C|R|RAZ (Reads as zero)|
|PRCR|c196|0x310|RW|Device Power-down and Reset Control Register|
|PRSR|c197|0x314|R|Device Power-down and Reset Status Register|
|-|c198-c511|0x318-0x7FC|R|RAZ (Reads as zero)|
|-|c512-575|0x800-0x8FC|R|RAZ (Reads as zero)|
|-|c576-c831|0x900-0xCFC|R|RAZ (Reads as zero)|
|-|c832-c895|0xD00-0xDFC|R|Processor ID Registers|
|-|c896-c927|0xE00-0xE7C|R|RAZ (Reads as zero)|
|-|c928-c959|0xE80-0xEFC|-|Integration Test Registers|
|-|c960-c1023|0xF00-0xFFC|-|Management Registers|



1712 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

## _**14.1.3.3.2 Boundary Scan**_ 

This device supports boundary scan using an IEEE 1149.1 compliant JTAG TAP. IEEE 1149.1 and 1149.6 Boundary Scan support are defined in device-specific BSDL files that can be found in the respective device’s product folder on ti.com. 

## **14.1.3.4 Reset Management** 

**Reset isolation** : critical configuration and trace datapaths and logic are not sensitive to warm reset. 

**Configuration independence** : debug configuration occurs over a debug-only interconnect, separate from SoC traffic to ensure debug logic remains available even during deadlock scenarios. 

**Power-AP** : a CoreSight™ compliant Access Port (AP) developed by TI that provides a standard interface for debug tooling to access status and control over power, reset, and clocking for the system. Power-AP can control the reset of the system through the following registers: 

- SYSTEMRESET_SPREC: Asserts system reset. A pulse to level signal is needed 

- WIRREG_SPREC: Extends the system reset in RCM 

- NRESET_SPREC: Reads the status of system reset 

- GLOBALRELEASEWIR_SPREC: Writing 1 releases the WIRREQ 

- PWRAP_SPREC: Writing 1 to bit 0 initiates system reset. Bit 8 toggles from 0 to 1 to 0, and users need to wait for the sequence to finish 

These registers are not memory mapped, so the registers can only be accessed by typing register name in expression window of DAP connection. 

## **14.1.3.5 Debug Cross Triggering** 

This device supports an Arm® CoreSight™ compliant four-channel programmable on-chip cross triggering network. 

Conceptually, each channel of cross triggering can be viewed as mapping of a user-defined set of events to a user-defined set of actions, where the occurrence of any event in the set-of-events results in the generation of the set-of-actions. 

The cross triggering network of this device is shown in Figure 14-3. 

**==> picture [500 x 251] intentionally omitted <==**

**Figure 14-3. Cross Trigger Network** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1713 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

## _**14.1.3.5.1 R5F CTI Trigger Connections**_ 

**Table 14-5. R5F CTI Trigger Input Connections (One per R5F Core)** 

|**Trigger Input Bit**|**Source**|**Comments**|
|---|---|---|
|[7]|Muxed VIM Interrupt sources|A mux selects which of the VIM interrupt event is<br>routed as Trigger<br>MSS_CTRL. R5SS*_CTI_TRIG_SEL.TRIG*[7:0] bits<br>control the mux.|
|[6]|ETM: ETMTRIGGER|ETM managed Trigger. Generated internal to Cortex<br>R5 Susbsystem|
|[5]|CORE:COMMTX|Communications channel transmit. Generated internal<br>to Cortex R5 Susbsystem|
|[4]|CORE:COMMRX|Communications channel receive. Generated internal<br>to Cortex R5 Susbsystem|
|[3]|ETM:ETMEXTOUT[1]|ETM managed External Output Event 1. Generated<br>internal to Cortex R5 Susbsystem|
|[2]|ETM:ETMEXTOUT[0]|ETM managed External Output Event 0. Generated<br>internal to Cortex R5 Susbsystem|
|[1]|CORE: PMUIRQ|Interrupt request from performance monitoring unit.<br>Generated internal to Cortex R5 Subsystem|
|[0]|CORE: DBGTRIGGER|CPU is entering the debug state (halted). Generated<br>internal to Cortex R5 Susbsystem|



**Table 14-6. R5F CTI Trigger Output Connections (One per R5F Core)** 

|**Trigger Output Bit**|**Destination**|**Comments**|
|---|---|---|
|[7]|CORE:DBGRESTART|External restart request|
|[6]|Not Used||
|[5]|Not Used||
|[4]|Not Used||
|[3]|VIM :CTI Interrupt|VIM Interrupt|
|[2]|ETM:EXTIN[1]|ETM External Input 1|
|[1]|ETM:EXTIN[0]|ETM External Input 0|
|[0]|CORE: EDBGRQ|External debug request|



## _**14.1.3.5.2 Cortex M4 CTI Trigger Connections**_ 

**Table 14-7. M4 CTI Trigger Input Connections** 

|**Trigger Input Bit**|**Source Signal**|**Comments**|
|---|---|---|
|[7]|Reserved||
|[6]|DWT:ETMTRIGGER[2]|DWT generated Trigger 2|
|[5]|DWT:ETMTRIGGER[1]|DWT generated Trigger 1|
|[4]|DWT:ETMTRIGGER[0]|DWT generated Trigger 0|
|[3]|Reserved||
|[2]|Reserved||
|[1]|Reserved||
|[0]|CORE:HALTED|CPU Has Halted|



1714 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

**Table 14-8. M4 CTI Trigger Output Connections** 

|**Trigger Output Bit**|**Destination**|**Comments**|
|---|---|---|
|[7]|CORE:DBGRESTART|External restart request|
|[6]|Not Used||
|[5]|Not Used||
|[4]|Not Used||
|[3]|NVIC:CTI_IRQ0|NVIC Interrupt. Refer to Processor Interrupt Map for more<br>details|
|[2]|NVIC:CTI_IRQ1|NVIC Interrupt. Refer to Processor Interrupt Map for more<br>details|
|[1]|Not Used|-|
|[0]|CORE:EDBGRQ|External Debug Request.|



## _**14.1.3.5.3 STM CTI Trigger Connections**_ 

**Table 14-9. STM CTI Trigger Input Connections** 

|**Trigger Input Bit**|**Source Signal**|**Comments**|
|---|---|---|
|[7]|Reserved||
|[6]|Reserved||
|[5]|Reserved||
|[4]|Reserved||
|[3]|Reserved||
|[2]|STM:ASYNCOUT|Alignment synchronization output. The STM asserts this<br>signal for one clock cycle when an ASYNC-VERSION-<br>FREQ sequence is output on the ATB interface, and the<br>**ASYNCOUT**signal can be used for cross-triggering.|
|[1]|STM:TRIGOUTSW|The STM asserts this signal for one clock cycle when a<br>trigger event is generated on writes to a TRIG location in the<br>extended stimulus port registers|
|[0]|STM:TRIGOUTSPTE|The STM asserts this signal for one clock cycle when a<br>trigger event is detected on a match using the STMSPTER.|



## _**14.1.3.5.4 DEBUGSS CS-CTI Trigger Connections**_ 

**Table 14-10. DEBUGSS CS-CTI Trigger Input Connections** 

|**Trigger Input Bit**|**Source**|**Comments**|
|---|---|---|
|[7]|Muxed VIM3 Interrupt Inputs|Select any one of the 256 VIM3 interrupt. Configure by writing to<br>MSS_CTRL.DBGSS_CTI_TRIG_SEL.TRIG3|
|[6]|Muxed VIM2 Interrupt Inputs|Select any one of the 256 VIM2 interrupt. Configure by writing to<br>MSS_CTRL.DBGSS_CTI_TRIG_SEL.TRIG2|
|[5]|Muxed VIM1 Interrupt Inputs|Select any one of the 256 VIM1 interrupt. Configure by writing to<br>MSS_CTRL.DBGSS_CTI_TRIG_SEL.TRIG1|
|[4]|Muxed VIM0 Interrupt Inputs|Select any one of the 256 VIM0 interrupt. Configure by writing to<br>MSS_CTRL.DBGSS_CTI_TRIG_SEL.TRIG0|
|[3]|Reserved|Reserved|
|[2]|Reserved|Reserved|
|[1]|Reserved|Reserved|
|[0]|PWR-AP:SYNCRUNOUT|Debugss Power AP|



## **Table 14-11. DEBUGSS CS-CTI Trigger Output Connections** 

|**Trigger Output Bit**|**Destination**|**Comments**|
|---|---|---|
|[7]|Not Used|Not Used|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1715 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

**Table 14-11. DEBUGSS CS-CTI Trigger Output Connections (continued)** 

|**Trigger Output Bit**|**Destination**|**Comments**|
|---|---|---|
|[6]|Not Used|Not Used|
|[5]|Not Used|Not Used|
|[4]|CS-ETB: TRIGIN|Embedded Trace Buffer (ETB)|
|[3]|Not Used|Not Used|
|[2]|Not Used|Not Used|
|[1]|TPIU:FLUSHIN|DEBUGSS TPIU FLUSH|
|[0]|TPIU: TRIGIN|DEBUGSS TPIU TRIGGER|



## **14.1.3.6 SOC Debug and Trace** 

This device includes debug capabilities deployed at the system level, including: 

- Software messaging trace 

- Debug-aware peripherals 

- Global timestamping for trace 

More details for each of these capability areas can be found in the corresponding sections below. 

## _**14.1.3.6.1 Software Messaging Trace**_ 

Software messaging trace is supported on this device by an MIPI STP-V2 compliant Arm® CoreSight™ STM with supporting logic that maps initiator IDs to specific STP Major Source IDs. The following device initiators support software messaging. 

**Table 14-12. STM Apperture Assignment** 

|**16 MB Address Apperture of STM**|**Controller**|
|---|---|
|0|R5SS0_CORE0_AXI_W|
|1|R5SS0_CORE1_AXI_W|
|2|R5SS1_CORE0_AXI_W|
|3|R5SS1_CORE1_AXI_W|
|4|HSM|
|5|ICSS PRU0|
|6|ICSS PRU1|



## _**14.1.3.6.2 Debug Aware Peripherals**_ 

Select peripherals support a debug feature that allows them to react to the debug state of a controlling processor. For instance, a timer peripheral that is allocated to a particular processor could be configured to stop counting when the associated processor is in the halted state. This device includes programmable support for shared peripherals that allows the developer to select the processor whose debug state a given peripheral should receive. 

The Halt enable control register corresponding to the peripheral can be programmed to select which R5F CPU when halted will suspend the peripheral. 

**Table 14-13. Suspend Peripherals** 

|**Peripherals**|**Halt Enable Control Register**|
|---|---|
|MCAN* [0-7]|MSS_CTRL: MCAN*_HALTEN|
|LIN* [0-4]|MSS_CTRL: LIN*_HALTEN|
|I2C* [0-3]|MSS_CTRL: I2C*_HALTEN|
|RTI* [0-3] RTI* [0-7]|MSS_CTRL: RTI*_HALTEN|
|CPSW|MSS_CTRL: CPSW_HALTEN|
|MCRC0|MSS_CTRL: MCRC0_HALTEN|
|EPWM*[0-31]|CONTROLSS_CTRL: EPWM*_HALTEN|



1716 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

**Table 14-13. Suspend Peripherals (continued)** 

|**Peripherals**|**Halt Enable Control Register**|
|---|---|
|CMPSSA* [0-9]|CONTROLSS_CTRL: CMPSSA*_HALTEN|
|CMPSSB* [0-9]|CONTROLSS_CTRL: CMPSSB*_HALTEN|
|ECAP*[0-9]|CONTROLSS_CTRL: ECAP*_HALTEN|
|EQEP*[0-2]|CONTROLSS_CTRL: EQEP*_HALTEN|



## **14.1.3.7 Trace Infrastructure** 

Trace traffic originates from a trace source, is distributed across the device using Arm® CoreSight™ compliant trace infrastructure components, and reaches one of two possible trace sinks. The trace infrastructure is shown in Figure 14-4. 

**==> picture [500 x 299] intentionally omitted <==**

**Figure 14-4. Trace Infrastructure** 

## _**14.1.3.7.1 Trace Sources**_ 

The following trace sources are present in this device: 

- STM 

- HSM M4 ITM 

- R5FSS0 Core0 ETM 

- R5FSS0 Core1 ETM 

- R5FSS1 Core 0 ETM 

- R5FSS1 Core 1 ETM 

## _**14.1.3.7.2 Trace Distribution**_ 

Trace distribution is accomplished using standard Arm® CoreSight™ compliant trace infrastructure components: 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1717 

Copyright © 2025 Texas Instruments Incorporated 

_On-Chip Debug_ 

www.ti.com 

CoreSight™ Trace Funnels (CSTF): Non-programmable CSTFs are used at points of interleaving where multiple trace sources converge and form a single stream of trace traffic. This device includes one instance of a CSTF that is deployed immediately before the TPIU. 

CoreSight™ Trace Replicator (CSREP): A programmable CSREP is used as a routing device, that can be used to forward trace traffic, based on its ID, to one, both, or none of the device trace sinks. This device includes one instance of a CSTF that is deployed immediately before the TPIU to route the trace traffic to either CS-ETB or TPIU. 

## _**14.1.3.7.3 Trace Sinks**_ 

Two trace sinks are supported on this device: 

Arm® CoreSight™ TPIU: TPIU supports export of trace off-chip via LVCMOS device pins (See 1.3.2.2) for capture by an external receiver. 

CS-ETB Trace Buffer with 34KB of storage: CS-ETB can be setup to capture trace data until the internal buffer fills system bridge mode supports interrupt and event notification capabilities that support integration with device level CPUs and/or DMAs to support. 

## **14.2 Arm[®] Debug Links** 

CTI Register Summary: https://developer.arm.com/documentation/ddi0480/b/Programmers-Model/CTI-registersummary 

ETB[™] Register Summary: https://developer.arm.com/documentation/ddi0480/b/Programmers-Model/ETBregister-summary 

ATB[™] Register Summary: https://developer.arm.com/documentation/ddi0480/b/Programmers-Model/ATB-funnelregister-summary 

TPIU Register Summary: https://developer.arm.com/documentation/ddi0480/b/Programmers-Model/TPIUregister-summary 

STM Register Summary: https://developer.arm.com/documentation/ddi0528/b/Programmers-Model/Registersummary 

ETM[™] Register Summary: https://developer.arm.com/documentation/ddi0469/b/programmers-model/registersummary 

Arm Cortex[™] -R5 Debug Register Interface Summary: https://developer.arm.com/documentation/ddi0363/e/ debug/debug-register-interface/memory-mapped-registers 

1718 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

