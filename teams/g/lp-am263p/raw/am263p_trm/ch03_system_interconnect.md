<!-- AM263P TRM | 3 System Interconnect | 원본 p.40-75 | pymupdf4llm text+tables, images omitted -->

_System Interconnect_ 

www.ti.com 

## _Chapter 3_ _**System Interconnect**_ 

**==> picture [506 x 40] intentionally omitted <==**

## This chapter describes the device system interconnect. 

System interconnect provides a multi-layered crossbar network among initiators and targets within SoC. This mutli-layered crossbar network supports multiple in-flight transactions to improve both latency and throughput 

**3.1 System Interconnect Overview** ................................................................................................................................. 41 **3.2 CORE VBUSM Interconnect** .......................................................................................................................................42 **3.3 CORE VBUSP Interconnect** ....................................................................................................................................... 44 **3.4 PERI VBUSP Interconnect** ......................................................................................................................................... 46 **3.5 INFRA0 VBUSP Interconnect** .....................................................................................................................................48 **3.6 INFRA1 VBUSP Interconnect** .....................................................................................................................................49 **3.7 R5SS0 CONFIG SLV Interconnect** ............................................................................................................................. 49 **3.8 R5SS1 CONFIG SLV Interconnect** ............................................................................................................................. 50 **3.9 CONTROLSS Interconnect** .........................................................................................................................................51 **3.10 Interconnect Safety** .................................................................................................................................................. 54 **3.11 Bus Safety Errors** ..................................................................................................................................................... 54 **3.12 System Memory Protection Unit (MPU)/Firewalls** ................................................................................................. 59 

40 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## **3.1 System Interconnect Overview** 

The device implements a system interconnect using TI’s Common Bus Architecture (CBA), composed of the VBUSM and VBUSP protocols. 

The system is based on a multi-layered interconnect approach designed to meet high-performance system requirements. The core interconnect structure consists of a full crossbar implementation, where every initiator has an independent communication path with every target. In other words, any initiator can access any target on the interconnect while another initiator can access a different target simultaneously without any contention,such that, transactions from each initiator has access to full interconnect bandwidth. Arbitration will only happen at the target end point (when the same target is accessed by two or more initiators) with round-robin prioritization. Targets cannot generate read/write requests directly. However, they can respond to these requests by generating error events (as defined by the CBA protocol), interrupts, and DMA requests. 

The device interconnect is partitioned into the following sections: 

- CORE VBUSM Interconnect 

- CORE VBUSP Interconnect 

- R5SS0 VBUSM Interconnect 

- R5SS1 VBUSM Interconnect 

- PERI VBUSP Interconnect 

- INFRA0 VBUSP Interconnect 

- INFRA1 VBUSP Interconnect 

- R5SS0 CONFIG TARGET Interconnect 

- R5SS1 CONFIG TARGET Interconnect 

- CONTROLSS VBUSP Interconnect 

**==> picture [480 x 185] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPSW EDMA DEBUSSS HSM ICSS-M<br>VBUSM SAFETY CORE VBUSM Interconnect<br>INITIATOR<br>NO SAFETY<br>VBUSM SAFETY<br>R5SS0 VBUSM Interconnect R5SS1 VBUSM Interconnect<br>R5SS0_CONFIG_SLV R5SS1_CONFIG_SLV<br>R5SS0-0 R5SS0-1 R5SS1-0 R5SS1-1<br>INFRA-0 VBUSP Interconnect INFRA-1 VBUSP Interconnect<br>PERI VBUSP Interconnect VIM Interconnect VIM Interconnect VIM Interconnect VIM Interconnect<br>CORE VBUSP Interconnect<br>MISC MISC  FSI FSI EPWM EPWM EPWM EPWM ADC ADC ADC ADC ADC ADC ADC<br>PERIPH CONFIG 0 1 G0 G1 G2 G3 0 1 2 3 4 R0 R1<br>Control-SS VBUSP Interconnect<br>**----- End of picture text -----**<br>


**Figure 3-1. Top-Level System Interconnect** 

## **Note** 

CORE VBUSM, R5SS0 VBUSM and R5SS1 VBUSM Interconnects are 64-bit wide interconnect (i.e. 64-bit data bus width). Rest of the above interconnects are 32-bit wide (i.e. 32-bit data bus width). 

There are multiple targets for each of the above interconnects, these are detailed in later sections of the chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

41 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## **3.2 CORE VBUSM Interconnect** 

The device Core Interconnect (CORE VBUSM) utilizes the VBUSM architecture to enable extensive transaction pipelining configuration along with support for multiple outstanding transactions; this dramatically increases system performance at the cost of higher complexity and additional logic. The diagram below shows the device peripherals with Core Interconnect target ports. 

## **Figure 3-2. Core Interconnect Diagram** 

**==> picture [500 x 190] intentionally omitted <==**

**----- Start of picture text -----**<br>
R5FSS0 R5FSS0 R5FSS1 R5FSS1<br>-0 -1 -0 -1<br>HSM debugSS<br>CPSW EDMA_TC0 EDMA_TC1 ICSS_M MPU MPU MPU MPU MPU MPU MPU MPU<br>CPSW MPU<br>Interconnect R5SS0 VBUSM R5SS1 VBUSM<br>VBUSM CORE Interconnect<br>MPU MPU MPU MPU MPU<br>ICSSM_PRU0<br>512KB<br>L2OCRAM-BANK4<br>CFG interface SCRP_G1 From  L2OCRAM-BANK0 512KB L2OCRAM-BANK1 512KB L2OCRAM-BANK2 512KB L2OCRAM-BANK3 512KB<br>R5FSS0-0_W R5FSS0-0_R R5FSS0-1_W R5FSS0-1_R R5FSS1-0_W R5FSS1-0_R R5FSS1-1_W R5FSS1-1_R<br>HSM_TC0_R HSM_TC0_W HSM_TC1_R HSM_TC1_W SoC_TC0_R SoC_TC0_W SoC_TC1_R SoC_TC1_W ICSSM_PRU1<br>MMC0 MCRC0 DTHE 512KB<br>STM_STIM<br>MBOX_SRAM<br>L2OCRAM-BANK5<br>FLASH_DATA_REG0,1,3 To CORE VBUSP- Port 0 To CORE VBUSP- Port 1<br>**----- End of picture text -----**<br>


The red blocks in the diagram above indicate designated MPU (Memory protection units) on the associated target ports. The device MPUs allow for up to 8 programmable regions. Additional details related the Memory Protection Unit, can be found in the device Section 3.12 chapter. 

## **Note** 

The placement of 6 L2OCRAM Banks across the 3 interconnects (R5SS0 VBUSM, R5SS1 VBUSM and VBUSM CORE Interconnect) has been done such that cores in a cluster can have faster access (lesser latency) to the banks closer to that particular cluster. In other words, R5SS0_Core0 and R5SS0_Core1 cores will have faster access latency to its near L2OCSRAM banks (BANK0 and BANK1) placed on R5SS0 VBUSM interconnect. Similarly, R5SS1_Core0 and R5SS1_Core1 cores will have faster access latency to its near L2OCSRAM banks (BANK2 and BANK3) placed on R5SS1 VBUSM interconnect. All the 4 cores, will have the same but slower access latency to the common L2OCSRAM banks (BANK4 and BANK5) as compared to their near banks. Furthermore, all the 4 cores will have slower access latency to their far L2OCSRAM banks (BANK2 and BANK3 for cluster R5SS0 and BANK0 and BANK1 for cluster R5SS1) as compared to common banks. 

To summarize, for particular cores in a cluster, below is the L2OCRAM Bank access latency comparison: 

Access latency of near banks < Access latency of common banks < Access latency of far banks 

42 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## **Table 3-1. CORE VBUSM Initiator-Target Table** 

This table lists initiator and target end point connections for the CORE VBUSM Interconnect. A cell can contain one of the following: 

- Y – Connection **does** exist between initiator and target. 

- N – Connection **does NOT** exist between initiator and target. 

|**Targets**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**R5FSS**<br>**0-0***|**R5FSS**<br>**0-1***|**R5FSS**<br>**1-0***|**R5FSS**<br>**1-1***|**HSM**|**HSM_TC0**<br>**R/W***|**HSM_TC1**<br>**R/W***|**SoC_TC0**<br>**R/W***|**SoC_TC1**<br>**R/W***|**DEBUGS**<br>**S**|**ICSSM**<br>**PRU0**|**ICSSM**<br>**PRU1**|**CPSW3**<br>**G**|
|R5FSS0-0|N|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|R5FSS0-1^|Y|N|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|R5FSS1-0|Y|Y|N|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|R5FSS1-1^|Y|Y|Y|N|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|OCSRAM<br>(BANK0)|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|OCSRAM<br>(BANK1)|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|OCSRAM<br>(BANK2)|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|OCSRAM<br>(BANK3)|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|OCSRAM<br>(BANK4)|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|OCSRAM<br>(BANK5)|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|FLASH_DATA<br>_REG0,1,3|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|MBOX_SRAM|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|HSM|Y|Y|Y|Y|N|Y|Y|Y|Y|Y|Y|Y|Y|
|DTHE|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|FSS/OSPI|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|ICSSM|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|N|N|Y|
|MMC0|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|STM_STIM|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|MCRC|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|Y|
|CORE VBUSP<br>(Port0)|N|N|N|N|N|Y|N|Y|N|Y|Y|N|N|
|CORE VBUSP<br>(Port1)|N|N|N|N|Y|N|Y|N|Y|N|N|Y|N|



## **Note** 

* These initiators have separate read and write ports. 

## **Note** 

^ Accessible only with LOCKSTEP mode disabled. Any access with LOCKSTEP mode enabled results in an error response. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

43 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## **3.3 CORE VBUSP Interconnect** 

VBUSP is a very simple and easy to implement protocol that is pended such that only a single transaction can be outstanding at any given time. VBUSP protocol is classified as a point-to-point, pended interface protocol. The design is split into multi layers of VBUSP interconnect for performance requirements. The diagram below shows the peripherals which are target ports for the CORE VBUSP interconnect. 

VIM interconnect is a local VBUSP interconnect which allows a low latency path to the dedicated VIM from each R5SS. Since this is locally connected before the CORE VBUSP interconnect, access is restricted only from each R5SS core to its own VIM module. 

**==> picture [493 x 224] intentionally omitted <==**

**----- Start of picture text -----**<br>
R5FSS1 R5FSS1<br>R5FSS0 R5FSS0 -0 -1<br>-0 -1<br>VIM  VIM<br>VIM1-0 VIM1-1<br>From CORE  From CORE  VIM0-0 VIM  VIM  VIM0-1 interconnect interconnect<br>interconnect interconnect<br>VBUSM  VBUSM<br>Port 0 Port 1<br>MPU MPU<br>MPU MPU MPU MPU<br>VBUSP CORE Interconnect<br>PERI interconnect CONTROLSS interconnect<br>TOP_CTRL DEBUGSS SPINLOCK<br>X4 - R5F<br>X2 - Main VBUSM MSS_CTRL<br>/ / / /<br>**----- End of picture text -----**<br>


**Figure 3-3. CORE VBUSP Interconnect Diagram** 

The grey blocks are MPU (Memory Protection Units) on the target ports. These are used to protect data and configuration spaces by managing the accesses to these memory regions. The MPUs above can have up to 16 programmable regions. For more details on MPU, please refer to Section 3.12 . 

44 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## **Table 3-2. CORE VBUSP Initiator-Target Table** 

This table lists the initiator and target end point connections for the CORE VBUSP Interconnect. A cell can contain one of the following: 

- Y – Connection **does** exist between initiator and target. 

- N – Connection **does NOT** exist between initiator and target. 

||**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|
|---|---|---|---|---|---|---|
|**Targets**|**R5FSS**<br>**0-0_AHB**|**R5FSS**<br>**0-1_AHB**|**R5FSS**<br>**1-0_AHB**|**R5FSS**<br>**1-1_AHB**|**CORE VBUSM**<br>**(Port0)**|**CORE VBUSM**<br>**(Port1)**|
|EPWM_G0|Y|Y|Y|Y|Y|Y|
|EPWM_G1|Y|Y|Y|Y|Y|Y|
|EPWM_G2|Y|Y|Y|Y|Y|Y|
|EPWM_G3|Y|Y|Y|Y|Y|Y|
|EPWM_G0_WLINK|Y|Y|Y|Y|Y|Y|
|EPWM_G1_WLINK|Y|Y|Y|Y|Y|Y|
|EPWM_G2_WLINK|Y|Y|Y|Y|Y|Y|
|EPWM_G3_WLINK|Y|Y|Y|Y|Y|Y|
|SCR_ADC_0|Y|N|N|N|N|N|
|SCR_ADC_1|N|Y|N|N|N|N|
|SCR_ADC_2|N|N|Y|N|N|N|
|SCR_ADC_3|N|N|N|Y|N|N|
|SCR_ADC_4|N|N|N|N|Y|N|
|SCR_ADC_5|N|N|N|N|N|Y|
|MISC PERIPH|Y|Y|Y|Y|Y|Y|
|SCR_FSI_0|Y|Y|Y|Y|Y|Y|
|SCR_FSI_1|Y|Y|Y|Y|Y|Y|
|MISC CONFIG0|Y|Y|Y|Y|Y|Y|
|MISC CONFIG1|Y|Y|Y|Y|Y|Y|
|PERI_R5FSS0-0*|Y|N|N|N|N|N|
|PERI_R5FSS0-1*|N|Y|N|N|N|N|
|PERI_R5FSS1-0*|N|N|Y|N|N|N|
|PERI_R5FSS1-1*|N|N|N|Y|N|N|
|PERI VBUSP (Port0)*|N|N|N|N|Y|N|
|PERI VBUSP (Port1)*|N|N|N|N|N|Y|
|SPINLOCK|Y|Y|Y|Y|Y|Y|
|DEBUGSS|Y|Y|Y|Y|Y|Y|
|MSS_CTRL|Y|Y|Y|Y|Y|Y|
|TOP_CTRL|Y|Y|Y|Y|Y|Y|
|VIM0-0|Y|N|N|N|N|N|
|VIM0-1|N|Y|N|N|N|N|
|VIM1-0|N|N|Y|N|N|N|
|VIM1-1|N|N|N|Y|N|N|



## **Note** 

*These targets connect to initiator ports on the PERI interconnect. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

45 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## **3.4 PERI VBUSP Interconnect** 

PERI VBUSP interconnect connects with the CORE VBUSP interconnect through the target ports each dedicated for individual initiators on the CORE VBUSP. The diagram below shows the peripherals which are target ports for the CORE VBUSP interconnect. 

**Figure 3-4. PERI VBUSP Interconnect Diagram** 

**==> picture [500 x 249] intentionally omitted <==**

**----- Start of picture text -----**<br>
PERI Interconnect<br>R5FSS0-0_AHB R5FSS0-1_AHB R5FSS1-0_AHB R5FSS1-1_AHB VBUSM PORT0 VBUSM PORT1<br>INFRA1 INFRA0 CANFDx8 GPIOx4 RTIx8 WDTx4 SPIx8 LINx5 UARTx6 I2Cx4<br>R5SS0_CONFIG_SLV R5SS1_CONFIG_SLV<br>**----- End of picture text -----**<br>


46 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## **Table 3-3. PERI VBUSP Initiator-Target Table** 

This table lists initiator and target end point connections for the PERI VBUSP Interconnect. A cell may contain one of the following: 

- Y – Connection **does** exist between initiator and target. 

- N – Connection **does NOT** exist between initiator and target. 

||**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|
|---|---|---|---|---|---|---|
|**Targets**|**R5FSS**<br>**0-0_AHB**|**R5FSS**<br>**0-1_AHB**|**R5FSS**<br>**1-0_AHB**|**R5FSS**<br>**1-1_AHB**|**PERI VBUSP**<br>**(Port0)**|**PERI VBUSP**<br>**(Port1)**|
|GPIO0|Y|N|N|N|Y|Y|
|GPIO1|N|Y|N|N|Y|Y|
|GPIO2|N|N|Y|N|Y|Y|
|GPIO3|N|N|N|Y|Y|Y|
|WDT0|Y|N|N|N|Y|Y|
|WDT1|N|Y|N|N|Y|Y|
|WDT2|N|N|Y|N|Y|Y|
|WDT3|N|N|N|Y|Y|Y|
|SPI0|Y|Y|Y|Y|Y|Y|
|SPI1|Y|Y|Y|Y|Y|Y|
|SPI2|Y|Y|Y|Y|Y|Y|
|SPI3|Y|Y|Y|Y|Y|Y|
|SPI4|Y|Y|Y|Y|Y|Y|
|SPI5|Y|Y|Y|Y|Y|Y|
|SPI6|Y|Y|Y|Y|Y|Y|
|SPI7|Y|Y|Y|Y|Y|Y|
|UART0|Y|Y|Y|Y|Y|Y|
|UART1|Y|Y|Y|Y|Y|Y|
|UART2|Y|Y|Y|Y|Y|Y|
|UART3|Y|Y|Y|Y|Y|Y|
|UART4|Y|Y|Y|Y|Y|Y|
|UART5|Y|Y|Y|Y|Y|Y|
|LIN0|Y|Y|Y|Y|Y|Y|
|LIN1|Y|Y|Y|Y|Y|Y|
|LIN2|Y|Y|Y|Y|Y|Y|
|LIN3|Y|Y|Y|Y|Y|Y|
|LIN4|Y|Y|Y|Y|Y|Y|
|I2C0|Y|Y|Y|Y|Y|Y|
|I2C1|Y|Y|Y|Y|Y|Y|
|I2C2|Y|Y|Y|Y|Y|Y|
|I2C3|Y|Y|Y|Y|Y|Y|
|RTI0|Y|Y|Y|Y|Y|Y|
|RTI1|Y|Y|Y|Y|Y|Y|
|RTI2|Y|Y|Y|Y|Y|Y|
|RTI3|Y|Y|Y|Y|Y|Y|
|RTI4|Y|Y|Y|Y|Y|Y|
|RTI5|Y|Y|Y|Y|Y|Y|
|RTI6|Y|Y|Y|Y|Y|Y|
|RTI7|Y|Y|Y|Y|Y|Y|
|CANFD0|Y|Y|Y|Y|Y|Y|
|CANFD1|Y|Y|Y|Y|Y|Y|
|CANFD2|Y|Y|Y|Y|Y|Y|
|CANFD3|Y|Y|Y|Y|Y|Y|
|CANFD4|Y|Y|Y|Y|Y|Y|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 47 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-3. PERI VBUSP Initiator-Target Table (continued)** 

This table lists initiator and target end point connections for the PERI VBUSP Interconnect. A cell may contain one of the following: 

- Y – Connection **does** exist between initiator and target. 

- N – Connection **does NOT** exist between initiator and target. 

||**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|**Initiators**|
|---|---|---|---|---|---|---|
|**Targets**|**R5FSS**<br>**0-0_AHB**|**R5FSS**<br>**0-1_AHB**|**R5FSS**<br>**1-0_AHB**|**R5FSS**<br>**1-1_AHB**|**PERI VBUSP**<br>**(Port0)**|**PERI VBUSP**<br>**(Port1)**|
|CANFD5|Y|Y|Y|Y|Y|Y|
|CANFD6|Y|Y|Y|Y|Y|Y|
|CANFD7|Y|Y|Y|Y|Y|Y|
|INFRA0|Y|Y|Y|Y|Y|Y|
|INFRA1|Y|Y|Y|Y|Y|Y|



## **3.5 INFRA0 VBUSP Interconnect** 

INFRA0 VBUSP interconnect connects with the PERI VBUSP interconnect through a single target port catering to all initiators on the PERI VBUSP. Accessing a particular target by multiple initiators at the same time will be arbitrated in this interconnect. The diagram below shows the peripherals which are target ports for the INFRA0 VBUSP interconnect. 

**==> picture [500 x 193] intentionally omitted <==**

**----- Start of picture text -----**<br>
�<br>INFRA0 Interconnect<br>ESM DCCx4<br>CPSW_CFG<br>EDMA0_TC0_CFG EDMA0_TC1_CFG EDMA0_CC_CFG Xbar control x5<br>All Ini<br>ators<br>**----- End of picture text -----**<br>


There is no access restriction since its a single initiator, multiple target interconnect. 

48 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## **3.6 INFRA1 VBUSP Interconnect** 

INFRA1 VBUSP interconnect connects with the PERI VBUSP interconnect through a single target port catering to all initiators on the PERI VBUSP. Accessing a particular target by multiple initiators at the same time will be arbitrated in this interconnect. The diagram below shows the peripherals which are target ports for the INFRA1 VBUSP interconnect. 

**==> picture [452 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
INFRA1 Interconnect<br>MPU_SLV<br>All Init<br>ators<br>PBIST IOMUX<br>TOP_RCM MSS_RCM<br>TOP_EFUSE_FARM OPTI_FLASH_CFG ECC aggregators x5<br>**----- End of picture text -----**<br>


There is no access restriction since its a single initiator, multiple target interconnect. 

## **3.7 R5SS0 CONFIG SLV Interconnect** 

The diagram below shows the peripherals which are target ports for the R5SS0 CONFIG SLV interconnect. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

49 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**==> picture [374 x 279] intentionally omitted <==**

**----- Start of picture text -----**<br>
R5SS0_CONFIG_SLV<br>All Init<br>ators<br>STC<br>RL2x2 CCMR<br>TMU_ROMx2<br>ECC_aggregatorx2<br>**----- End of picture text -----**<br>


There is no access restriction since its a single initiator, multiple target interconnect. 

## **3.8 R5SS1 CONFIG SLV Interconnect** 

The diagram below shows the peripherals which are target ports for the R5SS1 CONFIG SLV interconnect. 

50 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**==> picture [374 x 279] intentionally omitted <==**

**----- Start of picture text -----**<br>
R5SS1_CONFIG_SLV<br>All Init<br>ators<br>STC<br>RL2x2 CCMR<br>TMU_ROMx2<br>ECC_aggregatorx2<br>**----- End of picture text -----**<br>


There is no access restriction since its a single initiator, multiple target interconnect. 

## **3.9 CONTROLSS Interconnect** 

CONTROLSS interconnect is divided into below list of separate interconnect connected to the CORE VBUSP interconnect individually. Since these are connected to the CORE VBUSP interconnect separately, each of this interconnect can be accessed in parallel by different initiators without any arbitration. Accessing a single CONTROLSS interconnect by multiple initiators at the same time will be arbitrated. 

- MISC PERIPH 

- MISC CONFIG0 

- MISC CONFIG1 

- SC_FSI0 (FSITX[0:1] and FSIRX[0:1]) 

- SCR_FSI1 (FSITX[2:3] and FSIRX[2:3]) 

- G0_EPWM, G1_EPWM, G2_EPWM, G3_EPWM 

- ADC0, ADC1, ADC2, ADC3, ADC4, ADC5 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

51 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**==> picture [500 x 559] intentionally omitted <==**

**----- Start of picture text -----**<br>
MISC PERIPH MISC CONFIG0 MISC CONFIG1 SCR_FSI0 SCR_FSI1<br>xN corresponds to<br>number of IPs xN corresponds to<br>number of IPs<br>G0_EPWM<br>G1_EPWM<br>SCR_ADC0<br>G2_EPWM SCR_ADC1<br>SCR_ADC2<br>G3_EPWM SCR_ADC3<br>SCR_ADC4<br>SCR_ADC5<br>2:1 Mux 2:1 Mux<br>2:1 Mux ADC_0 ADC_n<br>2:1 Mux<br>2:1 Mux _n corresponds to number of IPs<br>2:1 Mux<br>2:1 Mux<br>2:1 Mux<br>4:1 Mux 4:1 Mux<br>_n corresponds to<br>number of IPs<br>• EPWM_0 EPWM_n<br>EPWM_n<br>All init All init All init All init All init<br>ators ators ators ators ators<br>DAC<br>CMPSS12AxN CMPSS12BxN ECAPxN QEPxN SDFMxN ADC_cfg xN /   OTTO calibrat Resolver CONTROLSS_CTRL Safety Tile x 12 ADC_R0:port0 ADC_R0_cfg ADC_R1:port0 ADC_R1_cfg inputxbar pwmxbar mdlxbar iclxbar intxbar dmaxbar pwmsyncoutxbar outputxbar FSI_TX_0 FSI_TX_1 FSI_Rx_0 FSI_RX_1 FSI_TX_2 FSI_TX_3 FSI_Rx_2 FSI_RX_3<br>on xN<br>All init<br>ators<br>All init R5FSS1-0<br>R5FSS1-1<br>ators<br>VBUSM PORT0<br>VBUSM PORT1<br>EPWM_0 EPWM_n<br>EPWM_0 EPWM_n<br>EPWM_WLINK_G0 EPWM_WLINK_G0<br>EPWM_0 EPWM_n<br>EPWM_WLINK_G1<br>EPWM_WLINK_G1 EPWM_0<br>EPWM_WLINK_G2<br>EPWM_WLINK_G2<br>EPWM_WLINK_G3<br>EPWM_WLINK_G3<br>R5FSS0-0<br>R5FSS0-1<br>All initiators<br>All initiators<br>**----- End of picture text -----**<br>


- MISC PERIPH, MISC CONFIG0, MISC CONFIG1, SCR_FSI0 and SCR_FSI1 are single initiator, multiple targets as shown in the diagram. 

- EPWM interconnect are divided into 4 groups G0_EPWM, G1_EPWM, G2_EPWM and G3_EPWM accessed using different address regions in the memory map. Any initiator can access an EPWM group while another initiator is accessing a different EPWM group simultaneously. Each interconnect 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

52 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

has n target ports depending on number of EPWM in the design. After the interconnect, a 4:1 Static Mux can be configured per EPWM using CONTROLSS_GLOBAL_CTRL.EPWM_STATICXBAR_SEL0 & CONTROLSS_GLOBAL_CTRL.EPWM_STATICXBAR_SEL1 register, which statically assigns that EPWM to any of the selection groups – G0 to G3. 

- Additionally, for each EPWM group, there is a 4KB write only alias region added in the device memory map ( CONTROLSS_G0_EPWM_WLINK to CONTROLSS_G3_EPWM_WLINK), using which selected EPWM instances of that particular group can be written together in a single write. The registers CONTROLSS_GLOBAL_CTRL.CONTROLSS_G0_EPWM_WLINK to CONTROLSS_GLOBAL_CTRL.CONTROLSS_G3_EPWM_WLINK contains EPWM enables to select which instances can be written together. 

SCR_ADC0, SCR_ADC1,.. SCR_ADCn are different interconnect per intiator (R5FSS0-0_AHB, R5FSS0-1_AHB,R5FSS1-0_AHB, R5FSS1-1_AHB, CORE VBUSP (Port0), and CORE VBUSP (Port1)). The target ports are based on number of ADCs in the design. Each initiator can independently access any ADC register without any arbitration. In other words, the same ADC result register can be accessed by multiple initiators simultaneously without contention. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

53 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## **3.10 Interconnect Safety** 

In order to ensure the safety of data through the interconnect, redundancy has been implemented in VBUSM and VBUSP interconnect. For VBUSP, data and control signals are passed through a redundant interconnect and compared. For VBUSM, ECC of the data is generated and is passed through redundant interconnect. The comparison will happen for ECC of the data. The control signals are directly compared without any ECC generation. The status of comparison from Main and Redundant interconnect are available in MSS_CTRL MMR. 

**==> picture [184 x 175] intentionally omitted <==**

**Figure 3-5. VBUSM Interconnect** 

The following interconnects are safety compliant: 

1. CORE VBUSM 

2. CORE VBUSP 

3. PERI VBUSP 

4. R5SS0 VBUSM 

5. R5SS1 VBUSM 

The VBUSM Interconnect follows the ECC based VBUSM safety architecture as shown above in Figure 3-5. CORE VBUSP and PERI VBUSP follows VBUSP Safety architecture as shown below in Figure 3-6. All the Initiators/Targets of these Interconnects are safety compliant. 

**==> picture [174 x 148] intentionally omitted <==**

**Figure 3-6. VBUSP Interconnect** 

## **3.11 Bus Safety Errors** _**3.11.1 Error Signaling Integration**_ 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

54 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

The bus safety errors which gets generated from VBUSP and VBUSM Interconnects will get aggregated and are available as status registers in the MSS_CTRL. The Registers which contain various error status are: 

1. ***_INTAGG_STATUS_RAW** – These Registers capture raw error status for each safety compliant Initiator/ Target. 

2. ***_INTAGG_STATUS** – These Registers capture masked error status for each Initiator/Target which are safety compliant. The masking is done by programming the register - ***_INTAGG_MASK** with appropriate value. Masking will override the corresponding bit to be default value irrespective of raw error status. 

3. ***_RD_BUS_SAFETY_ERR** – This Register contains more information such as Single error, Double Error that had occurred in the data. Additionally, it contains if an error occurred in command bus, write bus, write status, or read bus of the Target Port. 

The Masked errors from various Targets are aggregated and sent to ESM. There are three such signals : Aggregated_VBUSP_error_H, Aggregated_VBUSM_error_H and Aggregated_VBUSM_error_L. The Initiators/ Targets errors which are aggregated and used for generation of these signals are given in the below table. 

**Table 3-4. Initiators/Targets errors aggregated and sent to ESM GROUP0** 

|**MSS ESM**<br>**GROUP0**<br>**Channel No.**|**Description**|**Comments**|
|---|---|---|
|31|Aggregated_VBUSP_error_H<br>•<br>R5SS0_0_AHB<br>•<br>R5SS0_1_AHB<br>•<br>R5SS1_0_AHB<br>•<br>R5SS1_1_AHB<br>•<br>MAIN_VBUSP (Aggregated error for all VBUSP Initiators and Targets)<br>•<br>PERI_VBUSP (Aggregated error for all VBUSP Initiators and Targets)|Aggregated High interrupt line for VBUSP<br>peripherals. Only compare error is mapped<br>to this line.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

55 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-5. Initiators/Targets errors aggregated and sent to ESM GROUP1** 

|**MSS ESM**<br>**GROUP1**<br>**Channel No.**|**Description**|**Comment**|
|---|---|---|
|1|Aggregated_VBUSM_error_H<br>•<br>R5SS0_0_RD<br>•<br>R5SS0_1_RD<br>•<br>R5SS0_0_WR<br>•<br>R5SS0_1_WR<br>•<br>R5SS0_0_S<br>•<br>R5SS0_1_S<br>•<br>R5SS1_0_RD<br>•<br>R5SS1_1_RD<br>•<br>R5SS1_0_WR<br>•<br>R5SS1_1_WR<br>•<br>R5SS1_0_S<br>•<br>R5SS1_1_S<br>•<br>Debugss<br>•<br>HSM_M<br>•<br>CPSW<br>•<br>OCSRAM(Bank0)<br>•<br>OCSRAM(Bank1)<br>•<br>OCSRAM(Bank2)<br>•<br>OCSRAM(Bank3)<br>•<br>OCSRAM(Bank4)<br>•<br>OCSRAM(Bank5)<br>•<br>SoC_TC_0_RD<br>•<br>SoC_TC_1_RD<br>•<br>SoC_TC_0_WR<br>•<br>SoC_TC_1_WR<br>•<br>HSM_TC_0_RD<br>•<br>HSM_TC_1_RD<br>•<br>HSM_TC_0_WR<br>•<br>HSM_TC_1_WR<br>•<br>ICSS0_PRU0<br>•<br>ICSS0_PRU1<br>•<br>OSPI<br>•<br>MCRC<br>•<br>DTHE<br>•<br>SCRP0<br>•<br>SCRP1<br>•<br>HSM|Aggregated High interrupt line for VBUSM<br>peripherals. DED(Double Error Detection) of<br>data and compare errors of control signals<br>are mapped to this line.|



56 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-5. Initiators/Targets errors aggregated and sent to ESM GROUP1 (continued)** 

|**MSS ESM**<br>**GROUP1**<br>**Channel No.**|**Description**|**Comment**|
|---|---|---|
|2|Aggregated_VBUSM_error_L<br>•<br>R5SS0_0_RD<br>•<br>R5SS0_1_RD<br>•<br>R5SS0_0_WR<br>•<br>R5SS0_1_WR<br>•<br>R5SS0_0_S<br>•<br>R5SS0_1_S<br>•<br>R5SS1_0_RD<br>•<br>R5SS1_1_RD<br>•<br>R5SS1_0_WR<br>•<br>R5SS1_1_WR<br>•<br>R5SS1_0_S<br>•<br>R5SS1_1_S<br>•<br>Debugss<br>•<br>HSM_M<br>•<br>MSS_CPSW<br>•<br>OCSRAM(Bank0)<br>•<br>OCSRAM(Bank1)<br>•<br>OCSRAM(Bank2)<br>•<br>OCSRAM(Bank3)<br>•<br>OCSRAM(Bank4)<br>•<br>OCSRAM(Bank5)<br>•<br>SoC_TC_0_RD<br>•<br>SoC_TC_1_RD<br>•<br>SoC_TC_0_WR<br>•<br>SoC_TC_1_WR<br>•<br>HSM_TC_0_RD<br>•<br>HSM_TC_0_WR<br>•<br>HSM_TC_1_RD<br>•<br>HSM_TC_1_WR<br>•<br>ICSS0_PRU0<br>•<br>ICSS0_PRU1<br>•<br>OSPI<br>•<br>MCRC<br>•<br>DTHE<br>•<br>CORE VBUSP(Port0)<br>•<br>CORE VBUSP(Port1)<br>•<br>HSM_S<br>•<br>ICSS<br>•<br>MBOX_SRAM<br>•<br>STM_STIM<br>•<br>MMC|Aggregated Low interrupt line for VBUSM<br>peripherals. SEC (Single Error Correction)<br>error is mapped to this line.|



## _**3.11.2 Programming sequence**_ 

Bus Infrastructure Safety is disabled by default. 

- The first step is to enable Bus Safety for the MSS subsystem globally. For this, write 0x7 to **MSS_CTRL.MSS_BUS_SAFETY_CTRL.MSS_BUS_SAFETY_CTRL_ENABLE** . 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

57 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

- User can enable safety on a node mentioned in above table by writing to the multibit field – **MSS_CTRL.<NODE>_BUS_SAFETY_CTRL_ENABLE** 

   - Write 0x7: To enable safety for the Node 

   - Write 0x0: To disable safety for the Node 

## _**3.11.3 Diagnostic Check Mechanism**_ 

1. Enable MSS bus safety errors. 

   - **MSS_CTRL.MSS_BUS_SAFETY_CTRL.MSS_BUS_SAFETY_CTRL _ENABLE** = 0x7 

2. Enable bus safety for each interface. Taking MSS L2 Bank A VBUSM interface as a reference. 

   - Set the mask bit for the respective source in **MSS_CTRL.MSS_VBUSM_SAFETY_x_ERRAGG_MASK** register. In this example, 

## **MSS_CTRL.MSS_VBUSM_SAFETY_H0_ERRAGG_MASK.MSS_VBUSM_SAFETY_H0_ERRAGG_ MASK_L2RAM0_VBUSM_ERRH** = 1 

## **Note** 

x can be a high or low priority setting for the corresponding source. 

- **MSS_CTRL.MSS_L2_A_BUS_SAFETY_CTRL.MSS_L2_A_BUS_SAFETY_CTRL_ENABLE** = 0x7 

- 3. For double/single error injection on data, 

   - **MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI.MSS_L2_A_BUS_SAFETY_FI_DED** = 0x1; (For Double Error Detection) 

**MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI.MSS_L2_A_BUS_SAFETY_FI_SEC** = 0x1; (For Single Error Correction) 

- **MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI.MSS_L2_A_BUS_SAFETY_FI_DATA** = 0x1<<i; 

   - Double/single errors can be injected only on 32-bit segments of data at a time. 

   - – i=0 for data[31:0] 

i=1 for data[63:32] 

i=2 for data[95:64] and so on. 

   - For controller interfaces, it will be read data to which error will be injected, and for target interfaces it will be write data to which error will get injected. 

- The write access is to be followed by a read to the endpoint of the bus interface. The address should be selected based on the FI_DATA value. 

   - **WR_MEM_32(MSS_L2_U_BASE + 0x2000 + i*0x4, wr_data)** ; // sufficient for targets like MSS_L2 

   - **rd_data = RD_MEM_32(MSS_L2_U_BASE + 0x2000 + i*0x4)** ; // sufficient for controllers like CR5A_AXI_READ 

- Upon detection of DED/SEC error on the interface, an ESM error gets triggered and the following sequence needs to be executed by the ISR to clear the error. 

   - 

         - **MSS_CTRL.MSS_L2_A_BUS_SAFETY_CTRL.MSS_L2_A_BUS_SAFETY_CTRL_ERR_CLEAR** = 0x1; 

      - Once the error at the interface is cleared, clear the ESM status register. 

      - Register **MSS_CTRL.MSS_L2_A_BUS_SAFETY_ERR** is read to confirm whether the ERROR is SEC/DED. 

   - Before Exiting the ISR need to do the below setting to ensure the fault injection is removed. 

      - **MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI.MSS_L2_A_BUS_SAFETY_FI_SEC** = 0x0 

      - **MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI.MSS_L2_A_BUS_SAFETY_FI_DED** = 0x0 

   - All the Bus-Safety SEC errors in MSS are aggregated to a single ESM line. So, before exiting the ISR, the corresponding bit in the aggregated registers **MSS_CTRL.MSS_VBUSM/P_x_ERRAGG_STATUS** should be written 1 to clear the status. 

4. For redundancy on the bus interface signals, 

58 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

- – **MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI.MSS_L2_A_BUS_SAFETY_FI_MAIN** = 0x1<<i; 

      - i=0 checks redundancy on the main command interface 

      - i=1 checks redundancy on the main write interface 

      - i=2 checks redundancy on the main write status interface 

      - i=3 checks redundancy on the main read interface 

      - For vbusp interfaces, only the main command interface is checked. 

   - **MSS_CTRL_Ptr.MSS_L2_A_BUS_SAFETY_FI.MSS_L2_A_BUS_SAFETY_FI_SAFE** = 0x1<<i; 

      - i=0 checks redundancy on the safe command interface 

      - i=1 checks redundancy on the safe write interface 

      - i=2 checks redundancy on the safe write status interface 

      - i=3 checks redundancy on the safe read interface 

      - For vbusp interfaces, only the safe command interface is checked. 

   - To inject redundancy errors on all the command, read, write and write status interface signals simultaneously, the following sequence is executed, 

      - **MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI.MSS_L2_A_BUS_SAFETY_FI_GLOBAL_MAIN** = 0x1; // for the main interface 

      - **MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI.MSS_L2_A_BUS_SAFETY_FI_GLOBAL_SAFE** = 0x1; // for the safe interface 

- Upon detection of a redundancy error on the interface, an ESM error gets triggered and the following sequence needs to be executed by the ISR to clear the error. 

   - **MSS_CTRL.MSS_L2_A_BUS_SAFETY_CTRL.MSS_L2_A_BUS_SAFETY_CTRL_ERR_CLEAR** = 0x1; 

   - Once the error at the interface is cleared, clear the ESM status register. 

- Before Exiting the ISR, one needs to do the below setting to ensure the fault injection is removed. 

   - **MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI_ST. MSS_L2_A_BUS_SAFETY_FI_MAIN** = 0x0 

   - 

   - **MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI_ST. MSS_L2_A_BUS_SAFETY_FI_SAFE** = 0x0 

- **MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI_ST.MSS_L2_A_BUS_SAFETY_FI_GLOBAL_MAIN** = 0x0 

- **MSS_CTRL.MSS_L2_A_BUS_SAFETY_FI_ST.MSS_L2_A_BUS_SAFETY_FI_GLOBAL_SAFE** = 0x0 

## **3.12 System Memory Protection Unit (MPU)/Firewalls** 

The device incorporates multiple system Memory Protection Units (MPU) aka Firewall in the interconnect for security purpose or to ensure freedom from interference (FFI) in safety application. Note that these are distinct from the MPU which is part of R5FSS (explained in section _R5FSS Features_ ).The choice of using the MPU for security or for FFI is an application level decision. 

The MPU works by allowing access to the underlying memory map (Peripheral or Memory) for authorized initiators and disallowing access to other initiators. 

## _**3.12.1 MPU Overview**_ 

The MPU has the following features: 

- Supports multiple programmable address ranges 

- Supports secure and debug access privileges 

- Supports read, write, and execute access privileges 

- Distinguishes access from different initiators based on an Identifier (Privilege ID) 

- Generates an interrupt when there is addressing or protection violation 

## _**3.12.2 MPU Instances**_ 

There are 23 MPU firewall instances in the device placed at various points in the interconnect topology. The firewalls are referred to as "Initiator side firewall" (firewall is located right at the initiator port) or "Target side firewall" (firewall is located right before the target port), depending on where the firewalls are present in the topology. All MPUs are identical from application perspective. However, all the target side MPUs have 8 Regions and Initiator side MPUs have 16 regions (initiator MPUs provide more regions to handle peripheral spaces) As 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 59 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

evident from Figure3-1, the Initiator side firewalls are intended to protect the peripheral space while the Target side firewalls protect individual Target memory space (memory bank or a unique target space). 

## **Initiator side MPUs** 

The Initiator side firewalls as shown in Figure 3-3 (CORE VBUSP Interconnect Diagram) are listed below. 

- SCRM2SCRP0 

- SCRM2SCRP1 

- R5SS0_CORE0_AHB_MST 

- R5SS0_CORE1_AHB_MST 

- R5SS1_CORE0_AHB_MST 

- R5SS1_CORE1_AHB_MST 

## **Target side MPUs** 

The Target side firewalls as shown in Figure 3-2 (Core Interconnect Diagram) are listed below. 

- R5SS0_CORE0_AXIS_SLV 

- R5SS0_CORE1_AXIS_SLV 

- R5SS1_CORE0_AXIS_SLV 

- R5SS1_CORE1_AXIS_SLV 

- L2OCRAM_BANK0_SLV 

- L2OCRAM_BANK1_SLV 

- L2OCRAM_BANK2_SLV 

- L2OCRAM_BANK3_SLV 

- L2OCRAM_BANK4_SLV 

- L2OCRAM_BANK5_SLV 

- FSS_CONFIG_SLV 

- MBOX_RAM_SLV 

- HSM_SLV 

- DTHE_SLV 

- FSS/OSPI_SLV 

- R5SS0_CONFIG_SLV 

- R5SS1_CONFIG_SLV 

60 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## _**3.12.3 MPU Functional Description**_ 

## **3.12.3.1 Functional Operation** 

The MPU performs access permission check for each Bus access reaching the MPU and decides to allow the access to pass unmodified further to the target memory if it passes the permission check OR disallow the access and fault the access back to the initiator if it fails the permission check. 

**==> picture [318 x 215] intentionally omitted <==**

**Figure 3-7. MPU Top Level Diagram** 

## **Privilege ID (PrivID)** 

Every initiator is associated with an Identifier referred to as Priv ID. See section **ISC (Initiator-side Security Control)** for how to assign a PrivID to each initiator. This PrivID identifies the controller for privilege purposes and accompanies all bus accesses made on behalf of that controller. That is, when a controller triggers a bus access command, the PrivID is carried alongside the command. 

## **Privilege Level (Priv)** 

Every initiator access on the input bus is associated with a privilege level. Two privilege levels are supported: supervisor and user. The privilege level is inherited from the code running on the corresponding processor. For example, ARM processor has User mode and Supervisor Mode. 

## **Secure/Non Secure Access** 

Every initiator is associated with a security level identifier Secure or Non Secure. When an initiator triggers a bus access command, the security level is carried alongside the command. See section **ISC (Initiator-side Security Control)** for how to assign a security level to each initiator. 

## **Debugger Access** 

When a JTAG based debugger makes access to a peripheral or Memory through the AHB-Ap port, such an access is qualified by a EMU (Emulator) signal. 

## **MPU Region** 

Each MPU is associated with multiple MPU regions. Each region of the MPU is programmable. The programming specifies which Initiators are allowed access, the address range where the access is allowed and additional access attributes such as read/Write/execute etc. 

A high level view of each MPU region is shown below: 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

61 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**==> picture [273 x 182] intentionally omitted <==**

• The start address PROGRAMMABLE_n_START_ADDRESS specifies the start address of the memory protection region ‘n’. 

- The End address PROGRAMMABLE_n_END_ADDRESS specifies the end address of the memory protection region ‘n’. 

## **Note** 

The granularity of the MPU in this device is 1KB. The lower 10 bits of the Programmable start and end address are a don’t care. 

Actual MPU_start_address[31:0] = PROGRAMMABLE_n_START_ADDRESS[ 31:10] : 10’b0 

Actual MPU_end_address[31:0] = PROGRAMMABLE_n_END_ADDRESS[31:10]:10’b1111111111 

• The MPPA(Memory Protection Permission Attribute) register PROGRAMMABLE_n_MPPA specifies the permission attributes for region ‘n’. AID15_0 field (Register bits 25-10) specifies the privID’s for which the rule of this region applies. There is an AID register bit for each possible privID (0 to 15) and an AIDX that covers privIDs not configured. The other bits specify the access attributes such as User Read/Write/Execute or Supervisor ReadWrite/Execute as well as Non secure access and Emulation/Debugger access. 

## **Rule** 

1. The MPU works by first checking the transfer’s privID against the AID settings. The privID is used to lookup the associated AID bit. If the AID bit is 0, then the range does not cover that Initiator/ID and the range is not checked (although other ranges with different AID setting will) for this transfer. If the AID bit is 1, then the range does cover that Initiator/PrivID and the permissions are checked. 

2. The transfer secure and debug parameters are checked against the MPPA values to detect an allowed access. The two bits (NS and EMU) provide 3 permission levels. 

- If the NS is set, the range is non-secure and any security or debug initiator may access the range. 

- If the NS is not set, the range is secure only and only secure level accesses are allowed. 

- If Emulation(debugger) access is happening then the permission check is only two bits EMU and NS 

   - If EMU is set then the region allows access to debugger (does not check for R/W/PRiv permissions ) 

   - If NS is set then region allows access to debugger (does not check for R/W/Priv permissions) 

3. For Non Debugger(Regular Initiator access from within the Device) the read, write and execute permissions are also checked. 

62 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-6. Protection Levels for Secure and Debug attributes** 

|**NS**|**EMU**|**Description**|
|---|---|---|
|0|0|Region_x_is secure without debug:<br>Only secure accesses are allowed. Debug accesses are not allowed.<br>Non-secure accesses are also not allowed|
|0|1|Region_x_is secure with debug:<br>Only secure and debug accesses are allowed.<br>Non-secure accesses are not allowed|
|1|-|Region_x_is non-secure:<br>All accesses (non-secure, secure and debug) are allowed.|



4. There is a set of permissions for supervisor mode and another for user mode. The “priv” attribute of the transfer determines the mode of access. 

- If priv = 1, the supervisor rwx bits are checked 

- If priv = 0, the user rwx bits are checked against the same attributes 

The Priv attribute signal on the bus depends on the mode of the CPU making the bus access. 

**Table 3-7. Request Type Access Controls** 

|**Bit**|**Description**|
|---|---|
|PROGRAMMABLE_x_MPPA[5] SR|Supervisor may read|
|PROGRAMMABLE_x_MPPA[4] SW|Supervisor may write|
|PROGRAMMABLE_x_MPPA[3] SX|Supervisor may execute|
|PROGRAMMABLE_x_MPPA[2] UR|User may read|
|PROGRAMMABLE_x_MPPA[1] UW|User may write|
|PROGRAMMABLE_x_MPPA[0] UX|User may execute|



For each bit, a value of 1 permits the access type, and 0 denies it. So, setting the UX bit to 1 means that a controller in user mode may execute from corresponding region. The MPU allows the programmer to specify each of these 6 bits separately. Thus 64 different combinations are possible but programs might not use all of them . 

5. Each region outputs whether the transfer is allowed or disallowed or don’t care. 

- If the AIDs match and the transfer is within the address range and the permissions match, the region indicates access allowed. 

- If the AIDs match and the transfer is within the address range and the permissions don’t match , the region indicates access disallowed. 

- In all other cases the region is a don’t care. 

The region outputs are aggregated to decide if the access is allowed or disallowed. 

The MPU configuration used in this device does not allow access by default (Blocking by default). 

- If none of the region allow access, the access is not allowed 

- In case of overlapping regions, If any of the region does not allow access, the access is not allowed. 

- The access is allowed only if one or more regions allow access and none of the regions disallow access. 

In other words the final permission is the lowest of each type of permission from any hit range. (So If a transfer hits 2 regions , one that is rw and another r, the final permission is just r). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 63 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## **Note** 

Due to MPU architecture limitation, in case of a Cacheable access from R5 CPU, if the cache line(32Byte) access falls in the last 32Bytes of the MPU region, the MPU incorrectly indicates an access fault. Hence it is recommended that the application does not perform a cacheable access on the last 32Bytes of an MPU region. This limitation does not exist for non Cacheable access from R5 or any access from non R5 initiators. 

## **3.12.3.2 Protection of the MPU Configuration Registers** 

Accesses to the PROGRAMMABLE_x_START_ADDRESS, PROGRAMMABLE_x_END_ADDRESS and PROGRAMMABLE_x_MPPA registers are also protected. All non-debug writes must be by a supervisor controller. If the PROGRAMMABLE_x_MPPA[7] NS bit is 0, then all writes must be by a secure controller. In addition, the NS bit can be modified only by a secure controller. A register write with invalid permissions results in protection fault and interrupt generation. 

A debug write is only allowed if NS = 1 or the EMU = 1 regardless of the secure or privilege attributes. Neither faults are recorded nor interrupts are generated for debug accesses. 

## **3.12.3.3 MPU Interrupt Requests** 

The MPU module generates the following interrupts when there is any kind of MPU violation: 

**Table 3-8. MPU Interrupts** 

|**Interrupt**|**Description**|
|---|---|
|mpu_addr_err_intr|Addressing violation interrupt|
|mpu_prot_err_intr|Protection violation interrupt.|



The **mpu_addr_err_intr** interrupt occurs when a read or write access is made to a non-existent register address in the MPU configuration space. 

The **mpu_prot_err_intr** interrupt occurs when there is a protection violation. Two kinds of protection violation is possible. 

1. When the access on the input bus violates the MPU rules as defined in Functional Operation section or 

2. When the access violates the protection of MPU configuration registers as defined in Protection of the MPU Configuration Registers section. 

The transfer parameters that caused the above violations are saved in **MPU.FAULT_ADDRESS** and **MPU.FAULT_STATUS** registers. This violation status MMRs can be cleared by writing to **MPU.FAULT_CLEAR** register. 

The above interrupts can be enabled by writing to **MPU.INTERRUPT_ENABLE** register. The register **MPU.INTERRUPT_RAW_STATUSSET** register can be read to know the raw interrupt status. The register **MPU.INTERRUPT_ENABLED_STATUSCLEAR** can be read to know the enabled interrupt status. The interrupt can be cleared by writing ‘1’ to **MPU.INTERRUPT_ENABLED_STATUSCLEAR** register. 

## **MPU Interrupt Aggregation** 

The error Interrupts from all MPUs in the device are aggregated and provided to each R5SS core as **R5FSSx_COREy_INTR_MPU_ADDR_ERRAGG (#69** ) and **R5FSSx_COREy_INTR_MPU_PROT_ERRAGG(#70)** interrupts. 

This aggregated address error interrupt can be controlled by the MMR **MSS_CTRL.MPU_ADDR_ERRAGG_R5SSx_CPUy_MASK** . There is one register per associated R5SS Core. Each bit represents one MPU which can be masked or enabled to generate the aggregated interrupt. The status of the Address error interrupt can be read from the MMRs 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

64 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**MSS_CTRL.MPU_ADDR_ERRAGG_R5SSx_CPUy_STATUS** and the raw status can be read from **MSS_CTRL.MPU_ADDR_ERRAGG_R5SSx_CPUy_STATUS_RAW .** The aggregated interrupt can be cleared by writing ‘1’ to the **MSS_CTRL.MPU_ADDR_ERRAGG_R5SSx_CPUy_STATUS** register. The raw status can be cleared by writing ‘1’ to the **MSS_CTRL.MPU_ADDR_ERRAGG_R5SSx_CPUy_STATUS_RAW** register. 

Note: To clear the aggregated status, the source MPU error interrupt must be cleared first followed by clearing the aggregated interrupt STATUS register. 

Similarly the aggregated protection error interrupt is associated with the registers **MSS_CTRL.MPU_PROT_ERRAGG_R5SSx_CPUy_MASK** , **MSS_CTRL.MPU_PROT_ERRAGG_R5SSx_CPUy_STATUS** and **MSS_CTRL.MPU_PROT_ERRAGG_R5SSx_CPUy_STATUS_RAW.** 

Similar to the above mechanism, the interrupts from all the MPUs in the device are aggregated and provided to HSM-ESM as **HSM_MPU_AGGR_ADDR_ERR** (#22) and **HSM_MPU_AGGR_PROT_ERR** (#23) Error. 

The relevant MMRs to mask/enable individual MPU errors is **HSM_SOC_CTRL.HSM_MPU_ERRAGG_MASK0 and HSM_SOC_CTRL. HSM_MPU_ERRAGG_MASK1 respectively.** 

Note: The MPU source interrupt can be cleared only by the entity who has access to the respective MPU config space (Typically HSM. However, other cores can be given access to MPU by opening up the HSM_SLV MPU). The aggregated interrupt can be cleared by the respective R5 Core themselves, by writing to the respective aggregated status register once the source interrupt is cleared. 

## **CPU Behavior when its access is faulted by MPU** 

When a violation is triggered in a MPU, the corresponding R5 CPU whose access caused this violation will receive a suitable response from the Bus interconnect. 

1. When a MPU present on CORE VBUSM interconnect violates, both Read or Write transaction causing the violation will result in the corresponding R5 Core taking an Abort exception. 

2. When a MPU present on CORE VBUSP interconnect violates during a Read transaction, the corresponding R5 Core will take an Abort exception. 

3. When a MPU present on the CORE VBUSP interconnect violates during a Write transaction the corresponding R5 Core will get an interrupt on the interrupt line 

   - **R5FSSx_COREy_INTR_AHB_WRITE_ERR(#135).** It will not take an Abort exception. 

## _**3.12.4 MPU Parameters**_ 

The position of the MPU with respect to the interconnect topology (Fig 3-2 and Fig 3-3) decides what the MPU is responsible for protecting and which initiators can perform access through a given MPU. 

For example : Notice that for MPU R5SS0_CORE_AHB_MST, R5SS0_CORE0 is the only initiator. Hence any regions configured inside this MPU only refer to the R5SS0_COR0 AID and not bother about other AIDs. 

Another example is MPU SCRM2SCRP0 where the R5SS cores do not have access (Refer to the Interconnect Initiator-Target Table ). The access is possible from HSM EDMA or SOC EDMA or ICSS or Debugger. 

There are 23 MPUs in this device. The parameters of each MPU and the memory regions associated with each MPU is listed in Table 6-15 . 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

65 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-9. MPU Parameters Table** 

|**MPU**|**Controller/**<br>|**ID**|**MPU**<br>|**Num of**<br>|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|
|---|---|---|---|---|---|---|---|---|---|
||**Target**||**Config**<br>**Addr**|**MPU**<br>**Regions**|**Num of protected**<br>**segments***|**Segment**<br>**Num**|**Segment**<br>**Start**<br>**Address**|**Segment**<br>**Size**|**Segment**<br>**Name**|
|R5SS0_C<br>ORE0_AXI<br>S_SLV|Target|0|0x400A000<br>0|8|5|0|0x7800000<br>0|64*1024|R5SS0_<br>CORE0_<br>TCMA|
|||||||1|0x7810000<br>0|64*1024|R5SS0_<br>CORE0_<br>TCMB|
|||||||2|0x7400000<br>0|8*1024*10<br>24|R5SS0_<br>CORE0_I<br>CACHE|
|||||||3|0x7480000<br>0|8*1024*10<br>24|R5SS0_<br>CORE0_<br>DCACHE|
|||||||4|0x7806000<br>0|1024|R5SS0_<br>CORE0_<br>TMU|
|R5SS0_C<br>ORE1_AXI<br>S_SLV|Target|1|0x400C000<br>0|8|5|0|0x7820000<br>0|32*1024|R5SS0_<br>CORE1_<br>TCMA|
|||||||1|0x7830000<br>0|32*1024|R5SS0_<br>CORE1_<br>TCMB|
|||||||2|0x7500000<br>0|8*1024*10<br>24|R5SS0_<br>CORE1_I<br>CACHE|
|||||||3|0x7580000<br>0|8*1024*10<br>24|R5SS0_<br>CORE1_<br>DCACHE|
|||||||4|0x7826000<br>0|1024|R5SS0_<br>CORE1_<br>TMU|
|R5SS1_C<br>ORE0_AXI<br>S_SLV|Target|2|0x400E000<br>0|8|5|0|0x7840000<br>0|64*1024|R5SS1_<br>CORE0_<br>TCMA|
|||||||1|0x7850000<br>0|64*1024|R5SS1_<br>CORE0_<br>TCMB|
|||||||2|0x7600000<br>0|8*1024*10<br>24|R5SS1_<br>CORE0_I<br>CACHE|
|||||||3|0x7680000<br>0|8*1024*10<br>24|R5SS1_<br>CORE0_<br>DCACHE|
|||||||4|0x7846000<br>0|1024|R5SS1_<br>CORE0_<br>TMU|



66 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-9. MPU Parameters Table (continued)** 

|**MPU**|**Controller/**<br>|**ID**|**MPU**<br>|**Num of**<br>|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|
|---|---|---|---|---|---|---|---|---|---|
||**Target**||**Config**<br>**Addr**|**MPU**<br>**Regions**|**Num of protected**<br>**segments***|**Segment**<br>**Num**|**Segment**<br>**Start**<br>**Address**|**Segment**<br>**Size**|**Segment**<br>**Name**|
|R5SS1_C<br>ORE1_AXI<br>S_SLV|Target|3|0x4010000<br>0|8|5|0|0x7860000<br>0|32*1024|R5SS1_<br>CORE1_<br>TCMA|
|||||||1|0x7870000<br>0|32*1024|R5SS1_<br>CORE1_<br>TCMB|
|||||||2|0x7700000<br>0|8*1024*10<br>24|R5SS1_<br>CORE1_I<br>CACHE|
|||||||3|0x7780000<br>0|8*1024*10<br>24|R5SS1_<br>CORE1_<br>DCACHE|
|||||||4|0x7866000<br>0|1024|R5SS1_<br>CORE1_<br>TMU|
|L2OCRAM<br>_BANK0_S<br>LV|Target|4|0x4002000<br>0|8|1|0|0x7000000<br>0|512*1024|L2OCRA<br>M_BANK<br>0|
|L2OCRAM<br>_BANK1_S<br>LV|Target|5|0x4004000<br>0|8|1|0|0x7008000<br>0|512*1024|L2OCRA<br>M_BANK<br>1|
|L2OCRAM<br>_BANK2_S<br>LV|Target|6|0x4006000<br>0|8|1|0|0x7010000<br>0|512*1024|L2OCRA<br>M_BANK<br>2|
|L2OCRAM<br>_BANK3_S<br>LV|Target|7|0x4008000<br>0|8|1|0|0x7018000<br>0|512*1024|L2OCRA<br>M_BANK<br>3|
|L2OCRAM<br>_BANK4_S<br>LV|Target|18|0x402C000<br>0|8|1|0|0x7020000<br>0|512*1024|L2OCRA<br>M_BANK<br>4|
|L2OCRAM<br>_BANK5_S<br>LV|Target|19|0x402E000<br>0|8|1|0|0x7028000<br>0|512*1024|L2OCRA<br>M_BANK<br>5|
|FSS/<br>OSPI_SLV|Target|11|0x4016000<br>0|8|3|0|0x6000000<br>0|128*1024*<br>1024|FSS_DA<br>TA_REG<br>0|
|||||||1|0x8000000<br>0|128*1024*<br>1024|FSS_DA<br>TA_REG<br>1|
|||||||2|0x8800000<br>0|128*1024*<br>1024|FSS_DA<br>TA_REG<br>3|
|MBOX_RA<br>M_SLV|Target|8|0x4014000<br>0|8|1|0|0x7200000<br>0|16*1024|MBOX_S<br>RAM|
|HSM_SLV|Target|9|0x4024000<br>0|8|2|0|0x2000000<br>0|128*1024*<br>1024|HSM_RA<br>M|
|||||||1|0x4000000<br>0|128*1024*<br>1024|HSM_SO<br>C_CTRL|
|DTHE_SLV|Target|10|0x4012000<br>0|8|1|0|0xCE0000<br>00|16*1024*1<br>024|HSM_DT<br>HE|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 67 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-9. MPU Parameters Table (continued)** 

|**MPU**|**Controller/**<br>|**ID**|**MPU**<br>|**Num of**<br>|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|
|---|---|---|---|---|---|---|---|---|---|
||**Target**||**Config**<br>**Addr**|**MPU**<br>**Regions**|**Num of protected**<br>**segments***|**Segment**<br>**Num**|**Segment**<br>**Start**<br>**Address**|**Segment**<br>**Size**|**Segment**<br>**Name**|
|FSS_CON<br>FIG_SLV|Target|20|0x4026000<br>0|4|11|0|0x5380000<br>0|4*1024|FSS_CF<br>G<br>(FLASH_<br>CONFIG<br>_REG0)|
|||||||1|0x5380100<br>0|4*1024|FSAS_C<br>FG<br>(FLASH_<br>CONFIG<br>_REG1)|
|||||||2|0x5380200<br>0|4*1024|FSAS_O<br>TFA_CF<br>G<br>(FLASH_<br>CONFIG<br>_REG2)|
|||||||3|0x5380600<br>0|4*1024|OSPI_CF<br>G<br>(FLASH_<br>CONFIG<br>_REG6)|
|||||||4|0x5380700<br>0|4*1024|OSPI0_E<br>CC_AGG<br>(FLASH_<br>CONFIG<br>_REG7)|
|||||||5|0x5380800<br>0|4*1024|OSPI0_F<br>LASH_A<br>PB<br>(FLASH_<br>CONFIG<br>_REG8)|
|||||||6|0x5380B00<br>0|4*1024|FOTA_M<br>MR_CFG<br>(FLASH_<br>CONFIG<br>_REG11)|
|||||||7|0x5380C00<br>0|4*1024|FOTA_P<br>DMEM_C<br>FG<br>(FLASH_<br>CONFIG<br>_REG12)|
|||||||8|0x5380D00<br>0|4*1024|FOTA_IM<br>EM_CFG<br>(FLASH_<br>CONFIG<br>_REG13)|
|||||||9|0x5380E00<br>0|4*1024|FOTA_W<br>BUF_CF<br>G<br>(FLASH_<br>CONFIG<br>_REG14)|
|||||||10|0x5380F00<br>0|4*1024|FSAS_E<br>CC_AGG<br>R<br>(FLASH_<br>CONFIG<br>~~REG15)~~|
||||||||||~~_~~<br>|
|68<br>_AM263_~~_P_~~_Technical Refer_~~_e_~~_nce Manual_|||||S~~P~~RUJ55D –~~S~~EPTEMBER~~2~~023 – REVIS~~E~~D JULY 202<br>_Submit Document Feedbac_|||||



Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-9. MPU Parameters Table (continued)** 

|**MPU**|**Controller/**<br>|**ID**|**MPU**<br>|**Num of**<br>|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|
|---|---|---|---|---|---|---|---|---|---|
||**Target**||**Config**<br>**Addr**|**MPU**<br>**Regions**|**Num of protected**<br>**segments***|**Segment**<br>**Num**|**Segment**<br>**Start**<br>**Address**|**Segment**<br>**Size**|**Segment**<br>**Name**|
|R5SS0_C<br>ONFIG_SL<br>V|Target|21|0x4028000<br>0|4|8|0|0x5300000<br>0|528|ECC_AG<br>G_R5SS<br>0_CORE<br>0|
|||||||1|0x5300300<br>0|528|ECC_AG<br>G_R5SS<br>0_CORE<br>1|
|||||||2|0x5321000<br>0|60|R5SS0_<br>CCMR|
|||||||3|0x5350000<br>0|172|R5SS0_S<br>TC|
|||||||4|0x5302000<br>0|8*1024|TMU_RO<br>M_R5SS<br>0_CORE<br>0|
|||||||5|0x5302400<br>0|8*1024|TMU_RO<br>M_R5SS<br>0_CORE<br>1|
|||||||6|0x5321200<br>0|1024|RL2_R5S<br>S0_COR<br>E0|
|||||||7|0x5321300<br>0|1024|RL2_R5S<br>S0_COR<br>E1|
|R5SS1_C<br>ONFIG_SL<br>V|Target|22|0x402A000<br>0|4|8|0|0x5300400<br>0|528|ECC_AG<br>G_R5SS<br>1_CORE<br>0|
|||||||1|0x5300700<br>0|528|ECC_AG<br>G_R5SS<br>1_CORE<br>1|
|||||||2|0x5321100<br>0|60|R5SS1_<br>CCMR|
|||||||3|0x5351000<br>0|172|R5SS1_S<br>TC|
|||||||4|0x5302800<br>0|8*1024|TMU_RO<br>M_R5SS<br>1_CORE<br>0|
|||||||5|0x5302C00<br>0|8*1024|TMU_RO<br>M_R5SS<br>1_CORE<br>1|
|||||||6|0x5321400<br>0|1024|RL2_R5S<br>S1_COR<br>E0|
|||||||7|0x5321500<br>0|1024|RL2_R5S<br>S1_COR<br>E1|
|SCRM2SC<br>RP0|Controller|12|0x4018000<br>0|16|1|0|0x5000000<br>0|256*1024*<br>1024|SCRM2S<br>CRP0|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 69 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-9. MPU Parameters Table (continued)** 

|**MPU**|**Controller/**<br>|**ID**|**MPU**<br>|**Num of**<br>|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|**Memory/Peripheral space Protected by the MPU**|
|---|---|---|---|---|---|---|---|---|---|
||**Target**||**Config**<br>**Addr**|**MPU**<br>**Regions**|**Num of protected**<br>**segments***|**Segment**<br>**Num**|**Segment**<br>**Start**<br>**Address**|**Segment**<br>**Size**|**Segment**<br>**Name**|
|SCRM2SC<br>RP1|Controller|13|0x401A000<br>0|16|1|0|0x5000000<br>0|256*1024*<br>1024|SCRM2S<br>CRP1|
|R5SS0_C<br>ORE0_AH<br>B_MST|Controller|14|0x401C000<br>0|16|1|0|0x5000000<br>0|256*1024*<br>1024|R5SS0_<br>CORE0_<br>AHB|
|R5SS0_C<br>ORE1_AH<br>B_MST|Controller|15|0x401E000<br>0|16|1|0|0x5000000<br>0|256*1024*<br>1024|R5SS0_<br>CORE1_<br>AHB|
|R5SS1_C<br>ORE0_AH<br>B_MST|Controller|16|0x4020000<br>0|16|1|0|0x5000000<br>0|256*1024*<br>1024|R5SS1_<br>CORE0_<br>AHB|
|R5SS1_C<br>ORE1_AH<br>B_MST|Controller|17|0x4022000<br>0|16|1|0|0x5000000<br>0|256*1024*<br>1024|R5SS1_<br>CORE1_<br>AHB|
|* - Each segment is a contiguous address range in the memory map of the device which the corresponding MPU is responsible for<br>protecting. The Segment start address and Segment size columns lists these segments.||||||||||



70 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## _**3.12.5 MPU Default HW Configuration**_ 

Each MPU region has a default value based on the Device type. The default value of MPU region based on device type is captured in table below 

**Table 3-10. Default Hardware MPU Configurations: HSFS Device** 

|**MPU Instance/Region#**|**PROGRAMMABLESTART**<br>**_ADDRESS**|**PROGRAMMABLEEND_A**<br>**DDRESS**|**PROGRAMMABLEMPPA**|**Priv**<br>**IDsAllowed**|**Initiator access**<br>**Allowance****|
|---|---|---|---|---|---|
|R5SS0_CORE0_AXIS_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0 to 15|Open to All Initiators|
|R5SS0_CORE1_AXIS_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0 to 15|Open to All Initiators|
|R5SS1_CORE0_AXIS_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0 to 15|Open to All Initiators|
|R5SS1_CORE1_AXIS_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0 to 15|Open to All Initiators|
|L2OCRAM_BANK0_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0 to 15|Open to All Initiators|
|L2OCRAM_BANK1_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0 to 15|Open to All Initiators|
|L2OCRAM_BANK2_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0 to 15|Open to All Initiators|
|L2OCRAM_BANK3_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0 to 15|Open to All Initiators|
|MBOX_RAM_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0 to 15|Open to All Initiators|
|HSM_SLV/ Region1|0x00000000|0xFFFFFFFF|0x00000838|1|HSM Only|
|HSM_SLV/Region2|0x 44000000|0x440007FF|0x03FFFFFF|0-15|Open to All Initiators|
|DTHE_SLV/ Region1|0x00000000|0xFFFFFFFF|0x00000838|1|HSM Only|
|L2OCRAM_BANK4_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0-15|Open to All Initiators|
|SCRM2SCRP0<br>SCRM2SCRP1<br>R5SS0_CORE0_MST<br>R5SS0_CORE1_MST<br>R5SS1_CORE0_MST<br>R5SS1_CORE1_MST<br>(Regions 1 to 5)|0x50000000|0x535FFFFF|0x0000087F|0-15|Open to All Initiators*|
||0x53600000|0x53600FFF|0x0000087F|1|HSM*|
||0x53601000|0x53801FFF|0x0000087F|0-15|Open to All Initiators*|
||0x53802000|0x53802FFF|0x0000087F|1|HSM*|
||0x53803000|0x5FFFFFFF|0x0000087F|0-15|Open to All Initiators*|
|L2OCRAM_BANK5_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0-15|Open to All Initiators|
|FSS_DATA_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0-15|Open to All Initiators|
|FSS_CONFIG_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0-15|Open to All Initiators|
|R5SS0_CONFIG_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0-15|Open to All Initiators|
|R5SS1_CONFIG_SLV/ Region1|0x00000000|0xFFFFFFFF|0x03FFFFFF|0-15|Open to All Initiators|
|*Modifed by ROM||||||
|**Access allowance interpretation based on the default ISC Configuration Table for PrivID-Initiator Mapping||||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 71 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-11. Default Hardware/ROM MPU Configurations: HSSE Device** 

|**MPU Instance/Region#**|**PROGRAMMABLE_STAR**<br>**T_ADDRESS**|**PROGRAMMABLE_END_**<br>**ADDRESS**|**PROGRAMMABLE_MPPA**|**Priv IDs**<br>**Allowed**|**Priv ID Enabled ****|
|---|---|---|---|---|---|
|R5SS0_CORE0_AXIS_SLV/ Region1|0x00000000|0xFFFFFFFF|0x00000838|1|HSM Only|
|R5SS0_CORE1_AXIS_SLV/ Region1|0x00000000|0xFFFFFFFF|0x00000838|1|HSM Only|
|R5SS1_CORE0_AXIS_SLV/ Region1|0x00000000|0xFFFFFFFF|0x00000838|1|HSM Only|
|R5SS1_CORE1_AXIS_SLV/ Region1|0x00000000|0xFFFFFFFF|0x00000838|1|HSM Only|
|L2OCRAM_BANK0_SLV/ Region1|0x70000000|0x7007FFFF|0x0000487F|1,4|HSM*,R5CORE0*, EDMA-<br>TC0 (MSS TPTC0)*,<br>EDMA-TC1 (MSS TPTC1)*|
|L2OCRAM_BANK1_SLV/ Region1|0x70080000|0x700FFFFF|0x0000487F|1,4|HSM*,R5CORE0*, EDMA-<br>TC0 (MSS TPTC0)*,<br>EDMA-TC1 (MSS TPTC1)*|
|L2OCRAM_BANK2_SLV/ Region1|0x70100000|0x7017FFFF|0x0000487F|1,4|HSM*,R5CORE0*, EDMA-<br>TC0 (MSS TPTC0)*,<br>EDMA-TC1 (MSS TPTC1)*|
|L2OCRAM_BANK3_SLV/ Region1|0x70180000|0x701FFFFF|0x0000487F|1,4|HSM*,R5CORE0*, EDMA-<br>TC0 (MSS TPTC0)*,<br>EDMA-TC1 (MSS TPTC1)*|
|MBOX_RAM_SLV/ Region1|0x72000000|0x72003FFF|0x0000487F|1,4|HSM*,R5CORE0*|
|HSM_SLV/Region1|0x00000000|0xFFFFFFFF|0x00000838|1|HSM Only|
|HSM_SLV/Region2|0x 44000000|0x440007FF|0x03FFFFFF|1|HSM Only|
|DTHE_SLV/ Region1|0x00000000|0xFFFFFFFF|0x00000838|1|HSM Only|
|SCRM2SCRP0<br>SCRM2SCRP1<br>R5SS0_CORE0_MST<br>R5SS0_CORE1_MST<br>R5SS1_CORE0_MST<br>R5SS1_CORE1_MST<br>(Regions 1 to 5)|0x50000000|0x535FFFFF|0x0000487F|1,4|HSM*,R5CORE0*, EDMA-<br>TC0 (MSS TPTC0)*,<br>EDMA-TC1 (MSS TPTC1)*|
||0x53600000|0x53600FFF|0x0000087F|1|HSM*|
||0x53601000|0x53801FFF|0x0000487F|1,4|HSM*,R5CORE0*, EDMA-<br>TC0 (MSS TPTC0)*,<br>EDMA-TC1 (MSS TPTC1)*|
||0x53802000|0x53802FFF|0x0000087F|1|HSM*|
||0x53803000|0x5FFFFFFF|0x0000487F|1,4|HSM*,R5CORE0*, EDMA-<br>TC0 (MSS TPTC0)*,<br>EDMA-TC1 (MSS TPTC1)*|
|L2OCRAM_BANK4_SLV/ Region1|0x70200000|0x7027FFFF|0x0000487F|1,4|HSM*,R5CORE0*, EDMA-<br>TC0 (MSS TPTC0)*,<br>EDMA-TC1 (MSS TPTC1)*|
|L2OCRAM_BANK5_SLV/ Region1|0x70280000|0x702FFFFF|0x0000487F|1,4|HSM*,R5CORE0*, EDMA-<br>TC0 (MSS TPTC0)*,<br>EDMA-TC1 (MSS TPTC1)*|



72 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-11. Default Hardware/ROM MPU Configurations: HSSE Device (continued)** 

|**MPU Instance/Region#**|**PROGRAMMABLE_STAR**<br>**T_ADDRESS**|**PROGRAMMABLE_END_**<br>**ADDRESS**|**PROGRAMMABLE_MPPA**|**Priv IDs**<br>**Allowed**|**Priv ID Enabled ****|
|---|---|---|---|---|---|
|FSS_DATA_SLV/ Region1|0x60000000|0x61FFFFFF|0x0000487F|1,4|HSM*,R5CORE0*, EDMA-<br>TC0 (MSS TPTC0)*,<br>EDMA-TC1 (MSS TPTC1)*|
|FSS_CONFIG_SLV/ Region1|0x53800000|0x5387FFFF|0x0000487F|1,4|HSM*,R5CORE0*|
|R5SS0_CONFIG_SLV/ Region1|0x00000000|0xFFFFFFFF|0x00000838|1|HSM Only|
|R5SS1_CONFIG_SLV/ Region1|0x00000000|0xFFFFFFFF|0x00000838|1|HSM Only|
|*Modified by ROM||||||
|**Access allowance interpretation based on the default ISC Configuration Table for PrivID-Initiator Mapping||||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

73 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

## _**3.12.6 ISC (Initiator-side Security Control)**_ 

The Initiator side Security Control (ISC) module is responsible for assigning the PrivID values to the Initiators. Each initiator is associated with a ID allocation register which assigns the Priv ID to the corresponding initiator. 

Allocation of PrivIDs to all initiators based on the ID Allocation register must be done under the control of HSM. 

The default Hardware ISC configuration is shown in below table. 

**Table 3-12. Default Hardware ISC Configurations** 

|**ISC Config Addr**|**Config Address**|**Priv ID at Reset**|
|---|---|---|
|ISC_CTRL_REG_HSM_CM4|0x4000 0400|0x1|
|ISC_CTRL_REG_HSM_TPTC_A0|0x4000 0404|0x1|
|ISC_CTRL_REG_HSM_TPTC_A1|0x4000 0408|0x1|
|ISC_CTRL_REG_MSS_R5FA0_AXI|0x4000 0800|0x4|
|ISC_CTRL_REG_MSS_R5FB0_AXI|0x4000 0804|0x5|
|ISC_CTRL_REG_MSS_R5FA1_AXI|0x4000 0808|0x6|
|ISC_CTRL_REG_MSS_R5FB1_AXI|0x4000 080C|0x7|
|ISC_CTRL_REG_MSS_TPTC_A0|0x4000 0810|0x4|
|ISC_CTRL_REG_MSS_TPTC_A1|0x4000 0814|0x4|
|ISC_CTRL_REG_MSS_ETHERNET_DMA|0x4000 0818|0xA|
|ISC_CTRL_REG_DBG_JTAG|0x4000 081C|0xB|
|ISC_CTRL_REG_ICSS0_PDSP0|0x4000 0820|0x9|
|ISC_CTRL_REG_ICSS0_PDSP1|0x4000 0824|0x9|



## **Note** 

The PrivID for the JTAG debugger is determined by the DOM signal from HSM 

## **Note** 

It is recommended to have only the HSM PrivID to be 0x1. 

## **Note** 

The ISC has bypass control which when set, will mean the Initiator will drive the Priv ID instead of being assigned from ISC ID allocation register. This Bypass needs to be set for EDMA initiators since they are capable of inheriting the PrivID from the CPU programing the DMA transfer task. 

## **3.12.6.1 ID Allocation** 

The general format of the ID allocation register ISC_CTRL_REG_<INITIATOR> is shown in **ISC ID allocation Register** below: 

## _**3.12.6.1.1**_ 

**Table 3-13. ISC ID allocation Register** 

|**Bit**|**Name**|**Type**|**Reset**|**Description**|**In**<br>**the device**|**Routed to IP**|
|---|---|---|---|---|---|---|
|31:22|reserved|r|0x0|Reserved|Reserved|N|
|21|PASS|rw|0|No privID replacement. A value of 1 will pass<br>through privid value. A value of 0 will replace privid<br>with priv_id field value|Yes|N|



74 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_System Interconnect_ 

www.ti.com 

**Table 3-13. ISC ID allocation Register (continued)** 

|**Bit**|**Name**|**Type**|**Reset**|**Description**|**In**<br>**the device**|**Routed to IP**|
|---|---|---|---|---|---|---|
|20|NONSEC|rw|0|Make outgoing non-secure. A value of 1 forces<br>secure clear, others do nothing. Do not set both<br>sec and nonsec.|Yes|Y|
|19|reserved|r|0x0|Reserved|Reserved|N|
|18:16|SEC|rw|0x0|Make outgoing secure. A value of 3&APOS;B111<br>forces secure set, others do nothing. Do not set<br>both sec and nonsec.|Yes|Y|
|15:12|reserved|r|0x0|Reserved|Reserved|N|
|11:08|PRIVID|rw|0x1|Privilege ID configuration|Yes|Y|
|07:00|reserved|r|0x0|Reserved|Reserved|N|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

75 

Copyright © 2025 Texas Instruments Incorporated 

