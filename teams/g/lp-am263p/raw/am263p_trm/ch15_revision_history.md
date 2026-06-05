<!-- AM263P TRM | Revision History | 원본 p.1719-1725 | pymupdf4llm text+tables, images omitted -->

_Revision History_ 

www.ti.com 

## _**Revision History**_ 

**==> picture [506 x 40] intentionally omitted <==**

NOTE: Page numbers for previous revisions may differ from page numbers in the current version. 

|**Changes from March 31, 2025 to July 31, 2025 (from Revision C (March 2025) to Revision D**|**Changes from March 31, 2025 to July 31, 2025 (from Revision C (March 2025) to Revision D**|
|---|---|
|**(July 2025))**<br>**Page**||
|•|Added web link to request access for HSM Addendum for AM263Px............................................................508|
|•|[ADC] Updated and resolved some inconsistencies regarding the exact voltage rail to reference buffer|
||connections.....................................................................................................................................................517|
|•|(ADC-CMPSS Signal Connections): Updated the CMPSS and ADC connections diagram..........................522|
|•|Added third paragraph inSection 7.5.2.20.1.................................................................................................568|
|•|[CMPSS Block Diagram] Updated CMPSS Module block diagram ...............................................................618|
|•|(ADC-CMPSS Signal Connections): Updated the CMPSS and ADC connections diagram..........................620|
|•|[Reference DAC] Updated DACOUT formula.................................................................................................622|
|•|Changed TBPHS = 300 inFigure 7-289........................................................................................................771|
|•|Added Externally-triggered frame generation inSection 7.5.9.1.1................................................................848|
|•|FSI integration diagram..................................................................................................................................848|
|•|[Buffer Almost Full] Corrected the register name in the note........................................................................1176|
|•|[Buffer Almost Empty] Corrected the register name in the note...................................................................1176|
|•|[MMCSD Features] Removed 8-bit mode from feature list, as it is not supported on AM26x......................1376|
|•|[Unsupported MMCSD Features] Added clarification that Controller DMA operation not supported refers to|
||ADMA operation...........................................................................................................................................1376|
|•|Updated diagrams for 4-bit MMCSD. 8-bit not supported on AM26x devices..............................................1377|
|•|[MMCSD Pin List] Removed 8-bit mode signals from tables........................................................................1382|
|•|[MMC/SD/SDIO Connected to an MMC, an SD Card, or an SDIO Card] Removed 8-bit mode pins and|
||modified diagrams........................................................................................................................................1384|
|•|[DMA Receive Mode] Updated figure to only show 4-bit mode. 8-bit mode is not supported on AM26x.....1397|
|•|[DMA Transmit Mode] Updated figure to only show 4-bit mode. 8-bit mode is not supported on AM26x....1398|
|•|[Busy Timeout for R1b, R5b Response Type] Updated timing diagram to remove 8-bit mode. AM26x does not|
||support 8-bit mode........................................................................................................................................1404|
|•|[Busy Timeout After Write CRC Status] Updated timing diagram to remove 8-bit mode. AM26x does not|
||support 8-bit mode........................................................................................................................................1404|
|•|[Write CRC Status Timeout] Updated timing diagram to remove 8-bit mode. AM26x does not support 8-bit|
||mode.............................................................................................................................................................1405|
|•|[Read Data Timeout] Updated timing diagram to remove 8-bit mode. AM26x does not support 8-bit mode........|
||......................................................................................................................................................................1405|
|•|Renamed master word with "controller" in CAN chapter..............................................................................1490|
|•|Updated Message RAM Address range table for AM263P..........................................................................1532|
|•|[ECC Aggregator Features] Removed inject only mode for diagnostic purposes from the features list.......1634|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1719 

Copyright © 2025 Texas Instruments Incorporated 

_Revision History_ 

www.ti.com 

|**Changes from May 31, 2024 to March 31, 2025 (from Revision B (May 2024) to Revision C**|**Changes from May 31, 2024 to March 31, 2025 (from Revision B (May 2024) to Revision C**|
|---|---|
|**(March 2025))**<br>**Page**||
|•|[Programmable Real-Time Unit and Industrial Communication Subsystem (PRU-ICSS)] PRUSS references|
||updated to PRU-ICSS......................................................................................................................................18|
|•|Added clarification that 1 WDT per core is present..........................................................................................24|
|•|Updated Memory map......................................................................................................................................28|
|•|Updated R5FSS core-specific Memory Map for AM263P................................................................................37|
|•|Updated top-level System Interconnect diagram..............................................................................................41|
|•|[Interconnect Safety] Adding cross-reference links to the figures in this section..............................................54|
|•|[Error Signaling Integration] Updated ICSSM references to ICSS. Changed 'Slave' to 'Peripheral'.................54|
|•|Updated IDs to match CSL defines file, Updated TMU segments size to 1024 instead of 944Bytes..............65|
|•|[ISC (Initiator-side Security Control)] ICSSM references updated to ICSS......................................................74|
|•|[Module Integration] Added note on interchangable reset signal naming.........................................................76|
|•|Updated the integration diagram......................................................................................................................87|
|•|[SOC_TIMESYNC_XBAR1 Integration] All references to ICSSM updated to ICSS.........................................91|
|•|RTI: Updated integration daigram and clocks table........................................................................................149|
|•|Removed clock mode3 from OSPI Boot mode...............................................................................................184|
|•|Modifed QSPI to OSPI for AM263P................................................................................................................184|
|•|Initial Creation.................................................................................................................................................192|
|•|[IP Blocks] Changing SCIA to UART0 in UART Boot row..............................................................................216|
|•|[IP Blocks] Added filtering for OSPI bootmodes.............................................................................................216|
|•|[PBIST] Updated memory group numbers and descriptions in R5 PBIST table.............................................216|
|•|Changed TOPRCM to MSS_TOPRCM to be consistent with RA...................................................................225|
|•|[MMR Access Error Interrupt] Changed C2K prefix in register names to CONTROLSS prefix......................227|
|•|[MSS_CTRL Integration] Changed TPCC0 → TPCC_A................................................................................231|
|•|[MSS_CTRL Integration] References to ICSSM updated to ICSS.................................................................231|
|•|[L2 OCRAM and Mailbox RAM and EDMA RAM Memory Initialization] fixed enumeration of PARTITIONx and|
||Bank(x) to start at 0 instead of 1, and there are 4 partitions/banks................................................................236|
|•|[ EDMA Global Configuration and Event Aggregation] changing TPCC0 to TPCC_A, TPTC00 to TPTC_A0,|
||TPTC01 to TPTC_A1.....................................................................................................................................237|
|•|[EDMA Error Aggregation] Changed TPCC0 register prefixes to TPCC_A....................................................237|
|•|[ICSSM Global Configuration] ICSSM*_IDLE_CONTROL changed to GLOBAL_CONTROLS.....................238|
|•|Added clarification that section MPU Interrupt Aggregator is about System MPUs.......................................239|
|•|[R5SS TCM Address Parity Error Aggregator] Changed the following register names:|
||R5SS*_CPU*_ECC_CORR_ERRAGG_MASK → R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG,|
||R5SS*_CORE*_ADDRPARITY_ERR_TCM → ERR_PARITY_ATCM0_R5SS0,|
||R5SS*_CORE*_ERR_ADDRPARITY_TCM → ERR_PARITY_B0TCM_R5SS0,|
||R5SS*_CORE*_ERR_ADDRPARITY_B1TCM → ERR_PARITY_B1TCM_R5SS0,|
||R5SS*_TCM_ADDRPARITY_CLR → TCMx_PARITY_CTRL........................................................................245|
|•|[Power Management Overview] Added definitions for FROM and 1.8V Analog supplies..............................253|
|•|Power: Added further detail surrounding connections with the 1.8V LDO......................................................255|
|•|Power: Adding POK and POR modules description.......................................................................................256|
|•|Added type of Temperature sensors...............................................................................................................259|
|•|[Thermal Manager Features] specified which 2 SoC Temperature Monitors are being referred to in feature list|
||- TSENSE0 and TSENSE1.............................................................................................................................259|
|•|[Thermal Alert Comparator]: Combined_Low and High Threshold Alert Mode_and_Single Hot/Cold Alert Mode_|
||into single_Operation with Interrupts_sub-section............................................................................................262|
|•|[Temperature Timestamp Registers] Specified which TSENSE modules the FIFO registers support|
||(TSENSE0 and TSENSE1).............................................................................................................................263|
|•|[FIFO Management] Specified which registers are updated when software stops a certain FIFO (first line in|
||section)...........................................................................................................................................................263|
|•|[ADC Values Versus Temperature] Added note that the conversion table does not apply to TSENSE3........264|
|•|Added note on memories affected by Warm Reset........................................................................................270|



1720 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Revision History_ 

|•|Added more details on ESM interrupts causing warm reset...........................................................................274|
|---|---|
|•|Added clarity on reset type to be used for ROM Eclipse and lockstep to dual-core switch............................274|
|•|Added note on HSDIVIDER CLKOUTS..........................................................................................................281|
|•|Updated R5SS Features for AM263P............................................................................................................318|
|•|Added reference to ARM documentation for details on R5 MPU...................................................................318|
|•|Updated R5SS Integration tables/ images.....................................................................................................320|
|•|[Tightly-Coupled Memories (TCMs)] Changed 'Slave' to 'Peripheral'.............................................................330|
|•|[R5FSS Boot Options] Changed 'Slave' to 'Target'.........................................................................................336|
|•|[Single Operation] Added note clarifying the order in which result registers for two operand operations must|
||be read. Notes are filtered for AM263Px........................................................................................................361|
|•|[PRU-ICSS Key Features] Changed program memory per PRU size from 16KB to 12KB............................366|
|•|[PRU-ICSS I/O Signals] changed first column in table to be PR<k> instead of PR0 to represent multiple|
||instances of PRU-ICSS (if applicable)............................................................................................................370|
|•|[PRU-ICSS Top Level Resources Functional Description] Added details for devices with >1 ICSS instance......|
||........................................................................................................................................................................375|
|•|[PRU-ICSS Local Instruction Memory Map] Updated IMEM/IRAM size to 12KB from 16KB.........................378|
|•|Added AM263Px specfic interrupt mapping to hightlight system specific mapping of CONTROLSS|
||interrupts.........................................................................................................................................................427|
|•|[PRU-ICSS Interrupt Requests Mapping] Updated IP Interrupts Table to match IP Spec. Interrupts [63:32] can|
||be generated from internal or external sources..............................................................................................427|
|•|Remove wording that shows 2 PRUSS..........................................................................................................430|
|•|[PRU-ICSS UART Signal Descriptions] References to PRUSS updated to PRU-ICSS.................................430|
|•|[PRU-ICSS eCAP Features] References to PRUSS updated to PRU-ICSS..................................................444|
|•|[PRU-ICSS Enhanced Capture CAP1-CAP4 Registers] References to PRUSS updated to PRU-ICSS.......447|
|•|[PRU-ICSS eCAP Module APWM Mode Operation] Adding APWM Mode Timing Waveform.......................448|
|•|[PRU-ICSS eCAP Module APWM Mode Operation] References to PRUSS updated to PRU-ICSS.............448|
|•|[PRU-ICSS MII MDIO Overview] Replaced 'slave' with 'peripheral'...............................................................490|
|•|[PRU-ICSS MII MDIO Functional Description] Replaced 'slave' with 'peripheral.'..........................................490|
|•|Section 7.5.2.3.1: Added note regarding maximum ADCCLK frequency (66.67MHz) and minimum|
||PRESCALE value (>=3).................................................................................................................................516|
|•|[ADC] Added details regarding the correct usage of the internal reference buffers.......................................517|
|•|[ADC] Updated Table ADC Input Selection Logic to improve clarity...............................................................520|
|•|(ADC-CMPSS Signal Connections): Updated CMPSS and ADC Connections diagram to show positive input|
||of lower comparator in CMPSSA is selectable between INP and INM signals...............................................522|
|•|External Channel Selection: Details regarding ADC external mux channels have been included.................538|
|•|Including PPB Oversampling section and PPB SYNCINSEL connection table..............................................554|
|•|Added note regarding approximately 3 times longer reference S+H time due to high drive impedance........560|
|•|Inducing links to ADC Open-short Detection (OSD) API and related SDK example......................................562|
|•|Added note to step 2 inSection 7.5.2.17......................................................................................................563|
|•|(ADC-CMPSS Signal Connections): Updated CMPSS and ADC Connections diagram to show positive input|
||of lower comparator in CMPSSA is selectable between INP and INM signals...............................................620|
|•|[ePWM Modules Overview] Updated number of submodules to 8 (from 32).................................................644|
|•|Time-Base Counter Synchronization: Added note on delay from internal control module to target module..652|
|•|ePWM: Added note on missed action qualifier events...................................................................................652|
|•|[APWM Mode Operation] Added note points..................................................................................................797|
|•|Added two note points....................................................................................................................................797|
|•|Changed fourth paragraph and added Note inSection 7.5.8.7.....................................................................837|
|•|AddedSection 7.5.8.10.................................................................................................................................842|
|•|FSI: Updated PING to External Trigger Sources and Index for AM263P.......................................................855|
|•|Added OUTPUTXBAR Input Connection Table for AM263P..........................................................................929|
|•|Updating the block diagram for AM263P........................................................................................................932|
|•|Adding more details on FOTA........................................................................................................................936|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1721 

Copyright © 2025 Texas Instruments Incorporated 

_Revision History_ 

www.ti.com 

• [Spinlock Software Reset] added sentence that reading back value of SOFTRESET bit will always return 0..... ........................................................................................................................................................................946 • [EDMA XBAR INTRTR0] Removed C2K prefix from affected sources in in_intr Hardware Requests table, replaced with CONTROLSS prefix................................................................................................................. 966 • [R5FSS0_CORE0 Interrupt Map] Changed TPCC0 to TPCC_A....................................................................986 • [R5FSS0_CORE1 Interrupt Map] Changed TPCC0 to TPCC_A....................................................................996 • [R5FSS1_CORE0 Interrupt Map] Changed TPCC0 to TPCC_A..................................................................1006 • [R5FSS1_CORE1 Interrupt Map] Changed TPCC0 to TPCC_A..................................................................1016 • [R5FSS1_CORE1 Interrupt Map] Added interrupt type in the Interrupt map................................................1016 • [PRU-ICSS Interrupt Map] Updated SOC_TSXBAR_INTR to SOC_TIMESYNC_XBAR to match Register Addendum naming........................................................................................................................................1025 • [EDMA Interrupt Aggregator] changed TPCC0 to TPCC_A......................................................................... 1036 • [EDMA Error Interrupt Aggregator] changed TPCC0 to TPCC_A................................................................ 1037 • [EDMA Configuration] Changed TPCC0 to TPCC_A, TPTC0 to TPTC_A0, TPTC1 to TPTC_A1...............1037 • [EDMA - Third Party Transfer Controller] Updated block diaghram to show read/write data bus is fixed at 64 bits................................................................................................................................................................ 1041 • [Parameter Set Updates] Changed 'slave' to 'peripheral'............................................................................. 1052 • [Constant Addressing Mode Transfers/Alignment Issues] changed 'slave' to 'target'...................................1058 • [Proxy Memory Protection] changed 'slave' to 'target'.................................................................................. 1078 • [EDMA Transfer Controller (EDMA_TPTC)] Updated for inclusive terminology........................................... 1082 • [Event Dataflow] Updated for inclusive terminology......................................................................................1084 • [GPIO Integration] Updated table introduction sentence to describe correct number of GPIO modules (# 0 to 3)................................................................................................................................................................... 1114 • [GPIO Integration] Updated Integration diagram to show that GPIO#_OUTEN is an active low signal by adding inverter bubble on ENB buffer,.......................................................................................................... 1114 • Added correct sequence to set or clear a GPIO........................................................................................... 1118 • [Trigger Configuration (per Bit)] updated method to return the value of the FAL_TRIG register. User can read SET_FAL_TRIG **or** CLR_FAL_TRIG registers to obtain FAL_TRIG value (rather than SET_FAL_TRIG **and** CLR_FAL_TRIG). .........................................................................................................................................1120 • Section 13.1.1.4.4.3: Qualification period bits/register naming added for AM26x devices........................... 1122 • Changed Figure 13-5 to align the sampling window in the proper timing area.............................................1122 • [GPIO Interrupt Connectivity] Updated Interrupt Router module naming for AM26x devices - GPIO_XBAR_INTROUTER.......................................................................................................................... 1128 • [I2C Interface Typical Connections] Updated the I/O signals table counts................................................... 1132 • [I2C Integration] Added note in clock table that DPLL_CORE_HSDIV0_CLKOUT0 (400MHz) is not supported.yes................................................................................................................................................1138 • [I2C Integration] References to ICSSM updated to PRU-ICSS.yes..............................................................1138 • [MCSPI Protocol and Data Format] Added CLKG bit field information to Programmable MCSPI Clock bullet point.............................................................................................................................................................. 1147 • [MCSPI in Controller Mode] Updated number of peripheral devices connected to in MCSPI Controller Mode (Full Duplex) figure........................................................................................................................................1150 • [Peripheral Receive-Only Mode] Added clarification to definition of full-duplex mode (requires 2 serial data lines)..............................................................................................................................................................1173 • [UART Integration] Added note in clock table that DPLL_CORE_HSDIV0_CLKOUT0 (400MHz) is not supported for all UART instances.................................................................................................................1214 • [UART Integration] References to ICSSM updated to PRU-ICSS................................................................1214 • Deleted the first paragraph for AM26x Devices as there is no reference to the UART hardware requests that is mentioned in the first paragraph............................................................................................................... 1229 • [CPSW Integration] Added note in clock table that DPLL_CORE_HSDIV0_CLKOUT0 (400MHz) and DPLL_CORE_HSDIV0_CLKOUT1 (500MHz) is not supported. ................................................................. 1274 • [CPSW Integration] References to ICSSM updated to PRU-ICSS...............................................................1274 • [CPSW Integration] Removed C2K prefixes from Destination Event Input column entries in Time Sync and Compare Event table, and replaced with CONTROLSS prefix.................................................................... 1274 

1722 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Revision History_ 

• [CPSW InterVLAN Routing]: Updated section to clarify intended usage......................................................1281 • (Address Table Entry): Updated IPv4 and IPv6 Table Entry sections to fix entry definitions and expand on IPv6 table entry operation.............................................................................................................................1282 • [CPSW Inner VLAN Table Entry]: Updated ENTRY_TYPE value from "1h" to "2h" in Inner VLAN Table Entry............................................................................................................................................................. 1287 • [CPSW Rate Limiting}: Added Rate Limiting main section........................................................................... 1305 • [CPSW Ethernet Port Transmit Rate Limiting]: Updated register name references from incorrect Host Port registers to correct Ethernet Port registers...................................................................................................1306 • [CDMA CPPI3.0 Interface Bandwidth] Updated 'master' to 'controller'.........................................................1364 • [MMCSD Features] Removed functional clock source input speed from feature list....................................1376 • [Unsupported MMCSD Features] Removed MMC out of band interrupts from unsupported feature table.. 1376 • [MMCSD Integration] Added note in clock table that DPLL_CORE_HSDIV0_CLKOUT0 (400MHz) is not supported. ....................................................................................................................................................1379 • [MMCSD Connectivity Attributes] Added Physical Address hex value in MMCSD Connectivity Attributes..1381 • [MMCSD Connectivity Attributes] Updated clock domain types to match MMCSD clocks table..................1381 • [MMCSD Clock and Reset Management] Updated table with correct clock signal names and edited first paragraph to reflect table changes............................................................................................................... 1382 • [MMC/SD/SDIO Connected to an MMC, an SD Card, or an SDIO Card] Updated block diagram to show 4 data lines. Removed block diagram showing >1 MMCSD instance............................................................. 1384 • [MMC/SD/SDIO Connected to an MMC, an SD Card, or an SDIO Card] Updated pin definitions for MMC_SDCD, MMC_SDWP, and added definition for MMC_OBI.................................................................1384 • [Normal Mode] Updated register prefix from SD to MMC.............................................................................1391 • [Idle Mode] Updated register prefix from SD to MMC...................................................................................1391 • [Transition from Normal Mode to Smart-Idle Mode] Updated register prefix from SD to MMC.................... 1392 • [Transition from Smart-Idle Mode to Normal Mode] Updated register prefix from SD to MMC.................... 1392 • [Force-Idle Mode] Updated register prefix from SD to MMC........................................................................ 1392 • [Local Power Management] Updated register prefix from SD to MMC.........................................................1393 • [Interrupt Requests] Updated register prefix from SD to MMC.....................................................................1394 • [Interrupt-Driven Operation] Updated register prefix from SD to MMC.........................................................1396 • [Polling] Updated register prefix from SD to MMC........................................................................................1396 • [DMA Responder Mode Operations] Updated register prefix from SD to MMC........................................... 1396 • [DMA Transmit Mode] Updated register prefix from SD to MMC................................................................. 1398 • [Data Buffer] Updated register prefix from SD to MMC................................................................................ 1399 • [Data Buffer Status] Updated register prefix from SD to MMC..................................................................... 1402 • [Different Types of Responses] Updated register prefix from SD to MMCSD.............................................. 1402 • [Transfer or Command Status and Error Reporting] Updated register prefix from SD to MMC................... 1403 • [Busy Timeout for R1b, R5b Response Type] Updated register prefix from SD to MMC............................. 1404 • [Busy Timeout After Write CRC Status] Updated register prefix from SD to MMC.......................................1404 • [Write CRC Status Timeout] Updated register prefix from SD to MMC........................................................ 1405 • [Read Data Timeout] Updated register prefix from SD to MMC................................................................... 1405 • [Transfer Stop] Updated register prefix from SD to MMC.............................................................................1406 • [Transfer Stop] Removed Auto CMD12 feature from MMC/SD/SDIO feature list.........................................1406 • [Output Signals Generation] Updated register prefix from SD to MMC........................................................ 1407 • [Generation on Falling Edge of MMC Clock] Added definitions for labels in timing diagram........................1407 • [Generation on Falling Edge of MMC Clock] Updated register prefix from SD to MMC............................... 1407 • [Generation on Rising Edge of MMC Clock] Added definitions for labels in timing diagram........................ 1407 • [Generation on Rising Edge of MMC Clock] Updated register prefix from SD to MMC................................1407 • [CE-ATA Command Completion Disable Management] Updated register prefix from SD to MMC.............. 1409 • [Test Registers] Updated register prefix from SD to MMC............................................................................1409 • [Surrounding Modules Global Initialization] changed MPU INTC to VIM......................................................1411 • [Set SD Default Capabilities] Updated register prefix from SD to MMC....................................................... 1412 • [Wake-Up Configuration] Updated register prefix from SD to MMC............................................................. 1412 • Updated the FSS Overview section..............................................................................................................1422 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1723 

Copyright © 2025 Texas Instruments Incorporated 

_Revision History_ 

www.ti.com 

|•|Updated the FSS detailed block Diagram....................................................................................................1426|
|---|---|
|•|(OSPI Environment): Updated RESETn_OUT signal descriptions to show pins operate as active low.......1437|
|•|[MCAN Power Down (Sleep Mode)] Added note that power down is not supported at system level, only|
||supported at IP level.....................................................................................................................................1517|
|•|[TX Queue] Added sentence on what indicies are returned in read.............................................................1529|
|•|RTI: Updated integration daigram and clocks table......................................................................................1600|
|•|Updated the Digital watchdog operation diagram.........................................................................................1617|
|•|Removed typo...............................................................................................................................................1631|
|•|Moved all the content to the subsection.......................................................................................................1633|
|•|Updated the overall content..........................................................................................................................1633|
|•|[ECC Aggregator Integration] Changed TPTC00 to TPTC_A0, TPTC01 to TPTC_A1................................1636|
|•|Updated the number of events.....................................................................................................................1646|
|•|[MCRC Features] added supported CRC polynomials to Feature list..........................................................1658|
|•|[PSA Signature Register] added CRC polynomial equations for all supported CRC polynomials...............1662|
|•|[MCRC Power Down Mode] Removed line - When MCRC controller is in power down mode, no data tracing|
||alone will happen - as it is not supported on AM26x devices.......................................................................1669|
|•|[Programmable Build-In Self-Test (PBIST) Module] updated topic for AM26x from Hercules......................1686|
|•|[PBIST vs. Application Software-Based Testing] Updated processor core to Cortex-R5F...........................1687|
|•|[Host Processor Interface to the PBIST Controller Registers] Updated processor core to Cortex-R5F.......1688|
|•|Added details on DAP and APB Interconnect and External Ports................................................................1698|
|•|Made generic to re-use across devices........................................................................................................1700|
|•|[Software Messaging Trace] Changed 'Master' to 'Controller'......................................................................1716|
|•|Adding Arm®debug register description links..............................................................................................1718|



1724 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

## **IMPORTANT NOTICE AND DISCLAIMER** 

TI PROVIDES TECHNICAL AND RELIABILITY DATA (INCLUDING DATA SHEETS), DESIGN RESOURCES (INCLUDING REFERENCE DESIGNS), APPLICATION OR OTHER DESIGN ADVICE, WEB TOOLS, SAFETY INFORMATION, AND OTHER RESOURCES “AS IS” AND WITH ALL FAULTS, AND DISCLAIMS ALL WARRANTIES, EXPRESS AND IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE OR NON-INFRINGEMENT OF THIRD PARTY INTELLECTUAL PROPERTY RIGHTS. 

These resources are intended for skilled developers designing with TI products. You are solely responsible for (1) selecting the appropriate TI products for your application, (2) designing, validating and testing your application, and (3) ensuring your application meets applicable standards, and any other safety, security, regulatory or other requirements. 

These resources are subject to change without notice. TI grants you permission to use these resources only for development of an application that uses the TI products described in the resource. Other reproduction and display of these resources is prohibited. No license is granted to any other TI intellectual property right or to any third party intellectual property right. TI disclaims responsibility for, and you will fully indemnify TI and its representatives against, any claims, damages, costs, losses, and liabilities arising out of your use of these resources. 

TI’s products are provided subject to TI’s Terms of Sale or other applicable terms available either on ti.com or provided in conjunction with such TI products. TI’s provision of these resources does not expand or otherwise alter TI’s applicable warranties or warranty disclaimers for TI products. 

TI objects to and rejects any additional or different terms you may have proposed. IMPORTANT NOTICE 

Mailing Address: Texas Instruments, Post Office Box 655303, Dallas, Texas 75265 Copyright © 2025, Texas Instruments Incorporated 

