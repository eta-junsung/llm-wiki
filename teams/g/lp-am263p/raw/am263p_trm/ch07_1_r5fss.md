<!-- AM263P TRM | 7.1 Arm Cortex R5F Subsystem (R5FSS) | 원본 p.317-354 | pymupdf4llm text+tables, images omitted -->

www.ti.com 

_Processors and Accelerators_ 

## **7.1 Arm Cortex R5F Subsystem (R5FSS)** 

This chapter describes the Arm Cortex R5F real-time microcontroller unit subsystem (R5FSS) in the device. There are two subsystems in the SoC named R5FSS0 and RF5SS1. The only difference between the two subsystem is that RF5SS0 has a ROM image of 128kB and R5FSS1 has no ROM. The SoC memory map for R5FSS0 with and without ROM is provided in _R5FSS Memory Map_ . The ROM image handles initial configuration for the R5FSS0 CORE0 and initiates the secondary boot loader (SBL) for application download. 

**7.1.1 R5FSS Overview** ................................................................................................................................................ 318 **7.1.2 R5FSS Integration** ..............................................................................................................................................320 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

317 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.1.1 R5FSS Overview**_ 

The R5FSS is a dual-core implementation of the Arm® Cortex®-R5F processor configured for Dual-Core or Lockstep operation. It also includes accompanying memories (L1 caches and tightly-coupled memories), standard Arm CoreSight™ debug and trace architecture, integrated vectored interrupt manager (VIM), ECC aggregators, and various other modules for protocol conversion and address translation for easy integration into the SoC. 

## **Note** 

The Cortex-R5F processor is a Cortex-R5 processor that includes the optional floating point unit (FPU) extension. In this TRM, all references to the Cortex-R5 processor apply to the Cortex-R5F processor by default. 

## **7.1.1.1 R5FSS Features** 

Each R5FSS supports the following features: 

- Dual-core Arm Cortex-R5F 

   - Core revision: r1p3 

   - Armv7-R profile 

   - Dual-core and Lockstep mode support 

   - • Dual-core mode: Two independently operating cores (asymmetric multiprocessing, no coherence) 

      - Lockstep mode: One operating core (CORE0) and One lockstep core (CORE1) 

         - CORE0 uses TCM resources of both cores 

         - CORE1 caches and interrupts are unused in this mode 

      - Support for switching to Dual-core mode from Lockstep mode by application (Efuse-enabled/MMR configuration feature) - by triggering a CPU reset. (See device specific data sheet for additional details.) 

   - L1 memory system 

      - 16KB instruction cache per CPU 

         - 4x4KB ways 

         - SECDED ECC protected per 64 bits 

      - 16KB data cache per CPU 

         - 4x4KB ways 

         - SECDED ECC protected per 32 bits 

      - 128KB tightly-coupled memory (TCM) per CPU] 

      - SECDED ECC protected per 32 bits 

      - Readable/writable from system 

      - Configurable reset initialization values through the CTRLMMR 

      - Split into A and B banks (with B further splitting into B0 and B1 interleaved banks) 

         - 32KB TCMA (ATCM) 

         - 48KB TCMB0 (B0TCM) 

         - 48KB TCMB1 (B1TCM) 

      - In Dual-Core mode, CORE0 and CORE1 each have 128KB of TCM: 

         - 32KB TCMA 

         - 48KB TCMB0 + 48KB TCMB1 

      - In Lockstep mode, TCM is 256KB in total for CORE0 of the specific R5FSS: 

         - 64KB TCMA 

         - 96KB TCMB0 + 96B TCMB1 

   - L2 Memory System 

      - AXI L2 port for each core with following features: 

         - 4 Region Address Translator (RAT) 

         - 4 Region Fast Local Copy (FLC) engine to accelerate boot process 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

318 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

   - Remote L2 cache controller with integrated tag RAM 

- 

      - Accelerator support 

      - Each core has a Trignometric Math Unit (TMU) accelerator on the TCMA interface 

   - Full-precision floating point (VFPv3-D16) 

   - 16 region memory protection unit (MPU) (Reference the ARM MPU Documentation for more details) 

   - – 8 breakpoints 

   - 8 watchpoints 

   - Dynamic branch prediction with global history buffer and 4-entry return stack 

   - CoreSight debug access port (DAP) 

   - CoreSight embedded trace macrocell (ETM-R5) interface 

   - Performance monitoring unit (PMU) 

- Interfaces 

   - 64-bit VBUSM initiator pair (1 read, 1 write) for L2 memory accesses (per core) 

   - 64-bit VBUSM target (for both read and write) for TCM access (per core) 

      - Also allows access to cache for debug purposes 

   - 32-bit VBUSP initiator for peripheral access (per core) 

   - 4x 32-bit VBUSP target configuration port (2x ECC Aggregator + 1x CCMR + 1x STC) 

   - – 32-bit VBUSP target debug port 

      - Allows access to all R5FSS internal debug logic 

- Synchronous clock domain crossing on all interfaces 

   - CPU and interface clocks run at a 2:1 frequency ratio or 1:1 frequency ratio. Refer to the Operating Performance Points section of the device data sheet for details on what is supported for each device. 

- Integrated vectored interrupt manager (VIM) 

   - 256 interrupts per core 

      - Only interrupts connected to R5F CORE0 are available in Lockstep mode 

      - Each interrupt programmable as either IRQ or FIQ 

      - Each interrupt has a programmable enable mask 

      - Each interrupt has a programmable 4-bit priority 

   - Priority interrupt supported 

   - Vectored interrupt interface 

      - Compatible with R5F VIC port 

      - Programmable 32-bit vector address per interrupt 

         - 

            - Address is SECDED error protected 

         - Default vector addresses provided on DED 

      - Dual-Core or Lockstep capable 

      - Software interrupt generation 

- Integrated ECC aggregators 

   - Support for error injection to all supported ECC memory blocks to test ECC functionality (add-on function from TI) 

   - 

      - One ECC aggregator per core to cover all RAMs and caches associated with that core 

- Standard Arm CoreSight debug and trace architecture at the R5FSS level 

   - Cross triggering: Supported by cross trigger interface (CTI) (per CORE) and cross trigger matrix (CTM) components 

   - Processor trace: Supported by embedded trace macrocell (ETM) (per CORE) and advanced trace bus (ATB) funnel components 

See R5FSS Functional Description for a functional block diagram and additional details related to the R5FSS. 

## **7.1.1.2 R5FSS Not Supported Features** 

The R5FSS does _not_ support the following native R5F features in this device: 

- ACP port (no coherence) 

- Multiple power domains 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

319 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.1.2 R5FSS Integration**_ 

This section describes the R5FSS integration in the device, including information about clocks, resets, and hardware requests. 

## **7.1.2.1 R5FSS Integration** 

There are 2x R5FSS modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

320 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [326 x 624] intentionally omitted <==**

**----- Start of picture text -----**<br>
DEVICE<br>INFRA1 VBUSP INTERCONNECT CORE VBUSP INTERCONNECT CORE VBUSM INTERCONNECT<br>R5FSS0<br>2x VBUSM Memory Master ports and 2x VBUSM TCM Target ports<br>2x VBUSP Peripheral Master ports<br>VBUSP Config Target ports<br>RCM<br>R5FSS0_CLK CLK<br>R5FSS0_POR_RST POR_RST<br>R5FSS0_CORE0_G_RST CORE0_G_RST<br>R5FSS0_CORE1_G_RST CORE1_G_RST<br>R5FSS0_CORE0_L_RST CORE0_L_RST<br>R5FSS0_CORE1_L_RST CORE1_L_RST<br>R5FSS0_VIM0_RST VIM0_RST<br>R5FSS0_VIM1_RST VIM1_RST<br>R5FSS0<br>R5FSS0_CORE0_INTR_IN_116 R5SS0_COMMRX_0<br>R5FSS0_CORE0_INTR_IN_117 R5SS0_COMMTX_0<br>R5FSS0_CORE0_INTR_IN_118 R5SS0_CPU0_CTI_INT<br>R5FSS0_CORE0_INTR_IN_119 R5SS0_CPU0_VALFIQ<br>R5FSS0_CORE0_INTR_IN_120 R5SS0_CPU0_VALIRQ<br>R5FSS0_CORE0_INTR_IN_121<br>R5FSS0_CORE0_INTR_IN_130 R5SS0_CORE0_FPU_EXP<br>R5FSS0_CORE0_INTR_IN_135 R5SS0_CORE0_AHB_WRITE_ERR<br>R5FSS0_CORE0_INTR_IN_125 R5SS0_LIVELOCK_1<br>R5FSS0_CORE0_INTR_IN_209 R5FSS0_CORE0_TMU_LVF<br>R5FSS0_CORE0_INTR_IN_210 R5FSS0_CORE0_TMU_LUF<br>R5FSS0_CORE0_INTR_IN_243 R5FSS0_CORE0_RL2_ERR_INTR<br>R5FSS0_CORE0_INTR_IN_244 R5FSS0_CORE1_RL2_ERR_INTR<br>R5FSS0_CORE1_INTR_IN_125 R5SS0_LIVELOCK_0<br>R5FSS0_CORE1_INTR_IN_135 R5SS0_CORE1_AHB_WRITE_ERR<br>R5FSS0_CORE1_INTR_IN_130 R5SS0_CORE1_FPU_EXP<br>R5FSS0_CORE1_INTR_IN_121 R5SS0_CPU1_VALIRQ<br>R5FSS0_CORE1_INTR_IN_120 R5SS0_CPU1_VALFIQ<br>R5FSS0_CORE1_INTR_IN_119 R5SS0_CPU1_CTI_INT<br>R5FSS0_CORE1_INTR_IN_118 R5SS0_CORE1_AHB_WRITE_ERR<br>R5FSS0_CORE1_INTR_IN_116 R5SS0_COMMRX_1<br>R5FSS0_CORE1_INTR_IN_117 R5SS0_COMMTX_1<br>R5FSS0_CORE1_INTR_IN_209 R5FSS0_CORE1_TMU_LVF<br>R5FSS0_CORE1_INTR_IN_210 R5FSS0_CORE1_TMU_LUF<br>R5FSS0_CORE1_INTR_IN_243 R5FSS0_CORE0_RL2_ERR_INTR<br>R5FSS0_CORE1_INTR_IN_244 R5FSS0_CORE1_RL2_ERR_INTR<br>R5FSS1<br>R5FSS1_CORE0_INTR_IN_116 R5SS0_CPU0_PMU_INT<br>R5FSS1_CORE1_INTR_IN_116<br>R5FSS1_CORE0_INTR_IN_117 R5SS0_CPU1_PMU_INT<br>R5FSS1_CORE1_INTR_IN_117<br>R5FSS1_CORE0_INTR_IN_126<br>R5FSS1_CORE1_INTR_IN_126<br>R5FSS1_CORE0_INTR_IN_127<br>R5FSS1_CORE1_INTR_IN_127<br>R5FSS1_CORE0_INTR_IN_132 R5SS0_STC_DONE<br>R5FSS1_CORE1_INTR_IN_132<br>R5FSS1_CORE0_INTR_IN_243 R5FSS0_CORE0_RL2_ERR_INTR<br>R5FSS1_CORE0_INTR_IN_244 R5FSS0_CORE1_RL2_ERR_INTR<br>R5FSS1_CORE1_INTR_IN_243 R5FSS0_CORE0_RL2_ERR_INTR<br>R5FSS1_CORE1_INTR_IN_244 R5FSS0_CORE1_RL2_ERR_INTR<br>**----- End of picture text -----**<br>


**Figure 7-1. R5FSS0 Integration Diagram 1** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 321 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **DEVICE** 

|**TOP_ESM**<br>ESM_LVL_IN_10<br>ESM_LVL_IN_52<br>ESM_LVL_IN_11<br>ESM_LVL_IN_14<br>ESM_LVL_IN_53<br>ESM_LVL_IN_54<br>ESM_LVL_IN_51<br>ESM_LVL_IN_47<br>ESM_LVL_IN_48<br>ESM_LVL_IN_15<br>ESM_LVL_IN_49<br>ESM_LVL_IN_50<br>ESM_PLS_IN_5<br>ESM_PLS_IN_6<br>ESM_PLS_IN_23<br>ESM_PLS_IN_24<br>ESM_PLS_IN_25<br>ESM_PLS_IN_29<br>ESM_PLS_IN_7<br>ESM_PLS_IN_8<br>ESM_PLS_IN_20<br>ESM_PLS_IN_19|||**R5FSS0**<br>R5SS0_LIVELOCK_0<br>R5SS0_LIVELOCK_1<br>R5SS0_VIM0_CORR_ERR<br>R5SS0_VIM1_CORR_ERR<br>R5SS0_VIM0_UNCORR_ERR<br>R5SS0_VIM1_UNCORR_ERR<br>R5SS0_CPU0_EVNT (22,23,24,25,40,41,42)<br>R5SS0_CPU0_EVNT (33,34,37,38,39)<br>R5SS0_CPU1_EVNT (22,23,24,25,40,41,42)<br>R5SS0_CPU1_EVNT (33,34,37,38,39)<br>R5SS0_CPU0_TCM_ERR (A,B0, B1)<br>R5SS0_CPU1_TCM_ERR (A,B0, B1)<br>R5SS0_LOCKSTEP_BUSMON_ERR<br>R5SS0_LOCKSTEP_COMP_ERR<br>R5SS0_TMU_COMP_ERR<br>R5SS0_CPU0_TMU_PARITY_ERR<br>R5SS0_CPU1_TMU_PARITY_ERR<br>R5SS0_RL2_COMP_ERR<br>R5SS0_LOCKSTEP_VIMCOMP_ERR<br>R5SS0_LOCKSTEP_CPU_MISCOMP_ERR<br>R5SS0_CCM_LOCKSTEP_COMP_ERR<br>R5SS0_SELFTEST_ERR|
|---|---|---|---|
|||||
|||||
|||||
|||||
||**MSS_CTRL**<br>INT_AGGR<br>R5SS0_CORE0_CORR_ERRAGG<br>INT_AGGR<br>INT_AGGR<br>R5SS0_CORE1_CORR_ERRAGG<br>R5SS0_CORE1_UNCORR_ERRAGG<br>R5SS0_CORE1_TCM_ADDRPARITY_ERRAGG<br>INT_AGGR<br>INT_AGGR<br>INT_AGGR<br>R5SS0_CORE0_UNCORR_ERRAGG<br>R5SS0_CORE0_TCM_ADDRPARITY_ERRAGG|7<br>7<br>5<br>5<br>3<br>3||
|||||
|||||
|||||
|||||
|||||
|||||
|||||
|||||
|||||
|||||



**Figure 7-2. R5FSS0 Integration Diagram 2** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

322 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [316 x 624] intentionally omitted <==**

**----- Start of picture text -----**<br>
DEVICE<br>CORE VBUSM INTERCONNECT<br>R5FSS1<br>2x VBUSM Memory Master ports and 2x VBUSM TCM Target ports<br>2x VBUSP Peripheral Master ports<br>VBUSP Config Target ports<br>RCM<br>R5FSS1_CLK CLK<br>R5FSS1_POR_RST POR_RST<br>R5FSS1_CORE0_G_RST CORE0_G_RST<br>R5FSS1_CORE1_G_RST CORE1_G_RST<br>R5FSS1_CORE0_L_RST CORE0_L_RST<br>R5FSS1_CORE1_L_RST CORE1_L_RST<br>R5FSS1_VIM0_RST VIM0_RST<br>R5FSS1_VIM1_RST VIM1_RST<br>R5FSS1<br>R5FSS1_CORE0_INTR_IN_118 R5SS1_COMMRX_0<br>R5FSS1_CORE0_INTR_IN_119 R5SS1_COMMTX_0<br>R5FSS1_CORE0_INTR_IN_120 R5SS1_CPU0_CTI_INT<br>R5FSS1_CORE0_INTR_IN_121 R5SS1_CPU0_VALFIQ<br>R5FSS1_CORE0_INTR_IN_122 R5SS1_CPU0_VALIRQ<br>R5FSS1_CORE0_INTR_IN_123<br>R5FSS1_CORE0_INTR_IN_130 R5SS1_CORE0_FPU_EXP<br>R5FSS1_CORE0_INTR_IN_135 R5SS1_CORE0_AHB_WRITE_ERR<br>R5FSS1_CORE0_INTR_IN_125 R5SS1_LIVELOCK_1<br>R5FSS1_CORE0_INTR_IN_209 R5SS1_CORE0_TMU_LVF<br>R5FSS1_CORE0_INTR_IN_210 R5SS1_CORE0_TMU_LUF<br>R5FSS1_CORE0_INTR_IN_245 R5SS1_CORE0_RL2_ERR_INTR<br>R5FSS1_CORE0_INTR_IN_246 R5SS1_CORE1_RL2_ERR_INTR<br>R5FSS1_CORE1_INTR_IN_125 R5SS1_LIVELOCK_0<br>R5FSS1_CORE1_INTR_IN_135 R5SS1_CORE1_AHB_WRITE_ERR<br>R5FSS1_CORE1_INTR_IN_130 R5SS1_CORE1_FPU_EXP<br>R5FSS1_CORE1_INTR_IN_123 R5SS1_CPU1_VALIRQ<br>R5FSS1_CORE1_INTR_IN_122 R5SS1_CPU1_VALFIQ<br>R5FSS1_CORE1_INTR_IN_121 R5SS1_CPU1_CTI_INT<br>R5FSS1_CORE1_INTR_IN_120 R5SS1_CORE1_AHB_WRITE_ERR<br>R5FSS1_CORE1_INTR_IN_118 R5SS1_COMMRX_1<br>R5FSS1_CORE1_INTR_IN_119 R5SS1_COMMTX_1<br>R5FSS1_CORE1_INTR_IN_209 R5FSS1_CORE1_TMU_LVF<br>R5FSS1_CORE1_INTR_IN_210 R5FSS1_CORE1_TMU_LUF<br>R5FSS1_CORE1_INTR_IN_245 R5FSS1_CORE0_RL2_ERR_INTR<br>R5FSS1_CORE1_INTR_IN_246 R5FSS1_CORE1_RL2_ERR_INTR<br>R5FSS0<br>R5FSS0_CORE0_INTR_IN_122 R5SS1_CPU0_PMU_INT<br>R5FSS0_CORE1_INTR_IN_122<br>R5FSS0_CORE0_INTR_IN_123 R5SS1_CPU1_PMU_INT<br>R5FSS0_CORE1_INTR_IN_123<br>R5FSS0_CORE0_INTR_IN_126<br>R5FSS0_CORE1_INTR_IN_126<br>R5FSS0_CORE0_INTR_IN_127<br>R5FSS0_CORE1_INTR_IN_127<br>R5FSS0_CORE0_INTR_IN_132 R5SS1_STC_DONE<br>R5FSS0_CORE1_INTR_IN_132<br>R5FSS0_CORE0_INTR_IN_245 R5FSS1_CORE0_RL2_ERR_INTR<br>R5FSS0_CORE0_INTR_IN_246 R5FSS1_CORE1_RL2_ERR_INTR<br>R5FSS0_CORE1_INTR_IN_245 R5FSS1_CORE0_RL2_ERR_INTR<br>R5FSS0_CORE1_INTR_IN_246 R5FSS1_CORE1_RL2_ERR_INTR<br>INFRA1 VBUSP INTERCONNECT CORE VBUSP INTERCONNECT<br>**----- End of picture text -----**<br>


**Figure 7-3. R5FSS1 Integration Diagram 1** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 323 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **DEVICE** 

**==> picture [464 x 531] intentionally omitted <==**

**----- Start of picture text -----**<br>
TOP_ESM R5FSS1<br>ESM_LVL_IN_12 R5SS1_LIVELOCK_0<br>ESM_LVL_IN_13 R5SS1_LIVELOCK_1<br>ESM_LVL_IN_61 R5SS1_VIM0_CORR_ERR<br>ESM_LVL_IN_62 R5SS1_VIM1_CORR_ERR<br>ESM_LVL_IN_59 R5SS1_VIM0_UNCORR_ERR<br>ESM_LVL_IN_60 R5SS1_VIM1_UNCORR_ERR<br>MSS_CTRL<br>ESM_LVL_IN_55 R5SS1_CORE0_CORR_ERRAGG INT_AGGR 7 R5SS1_CPU0_EVNT (22,23,24,25,40,41,42)<br>ESM_LVL_IN_56 R5SS1_CORE0_UNCORR_ERRAGG INT_AGGR 5 R5SS1_CPU0_EVNT (33,34,37,38,39)<br>ESM_LVL_IN_16 R5SS1_CORE0_TCM_ADDRPARITY_ERRAGG INT_AGGR 3 R5SS1_CPU0_TCM_ERR (A,B0, B1)<br>ESM_LVL_IN_57 R5SS1_CORE1_CORR_ERRAGG INT_AGG R 7 R5SS1_CPU1_EVNT (22,23,24,25,40,41,42)<br>ESM_LVL_IN_58 R5SS1_CORE1_UNCORR_ERRAGG INT_AGGR 5 R5SS1_CPU1_EVNT (33,34,37,38,39)<br>ESM_LVL_IN_17 R5SS1_CORE1_TCM_ADDRPARITY_ERRAGG INT_AGGR 3 R5SS1_CPU1_TCM_ERR (A,B0, B1)<br>ESM_PLS_IN_9 R5SS1_LOCKSTEP_BUSMON_ERR<br>ESM_PLS_IN_10 R5SS1_LOCKSTEP_COMP_ERR<br>ESM_PLS_IN_11 R5SS1_LOCKSTEP_VIMCOMP_ERR<br>ESM_PLS_IN_12 R5SS1_LOCKSTEP_CPU_MISCOMP_ERR<br>ESM_PLS_IN_22 R5SS1_CCM_LOCKSTEP_COMP_ERR<br>ESM_PLS_IN_21 R5SS1_SELFTEST_ERR<br>ESM_PLS_IN_26 R5SS1_TMU_COMP_ERR<br>ESM_PLS_IN_27 R5SS1_CPU0_TMU_PARITY_ERR<br>ESM_PLS_IN_28 R5SS1_CPU1_TMU_PARITY_ERR<br>ESM_PLS_IN_30 R5SS1_RL2_COMP_ERR<br>**----- End of picture text -----**<br>


**Figure 7-4. R5FSS1 Integration Diagram2** 

The tables below summarize the device integration details of R5FSS0/1. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

324 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-1. R5FSS[0:1]Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**SoC Interconnect**|
|---|---|
|R5FSS[0:1]_CORE[0:1]|CORE VBUSM Interconnect|
||CORE VBUSP Interconnect|
||INFRA1 VBUSP Interconnect|



## **Table 7-2. R5FSS[0:1] Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock**<br>**Input**|**Source Clock Signal**|**Source**||**Description**|
|---|---|---|---|---|---|
|R5FSS0|CLK|R5FSS0_CLK|MSS_RCM||Functional Clock. Interface clock is derived<br>from functional clock|
|R5FSS1|CLK|R5FSS1_CLK|MSS_RCM||Functional Clock. Interface clock is derived<br>from functional clock|



**Table 7-3. R5FSS[0:1] Resets** 

|**Module Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|R5FSS0|POR_RST|R5FSS0_POR_RST|MSS_RCM|R5FSS0 Power on Reset|
||CORE0_G_RST|R5FSS0_CORE0_G_RST|MSS_RCM|R5FSS0 Core0 Subsystem reset|
||CORE1_G_RST|R5FSS0_CORE1_G_RST|MSS_RCM|R5FSS0 Core1 Subsystem reset|
||CORE0_L_RST|R5FSS0_CORE0_L_RST|MSS_RCM|R5FSS0 Core0 Local Reset|
||CORE1_L_RST|R5FSS0_CORE1_L_RST|MSS_RCM|R5FSS0 Core1 Local Reset|
||VIM0_RST|R5FSS0_VIM0_RST|MSS_RCM|R5FSS0 VIM0 Reset|
||VIM1_RST|R5FSS0_VIM1_RST|MSS_RCM|R5FSS0 VIM1 Reset|
|R5FSS1|POR_RST|R5FSS1_POR_RST|MSS_RCM|R5FSS1 Power on Reset|
||CORE0_RST|R5FSS1_CORE0_G_RST|MSS_RCM|R5FSS1 Core0 Main reset|
||CORE1_RST|R5FSS1_CORE1_G_RST|MSS_RCM|R5FSS1 Core1 Main reset|
||CORE0_L_RST|R5FSS1_CORE0_L_RST|MSS_RCM|R5FSS0 Core0 Local Reset|
||CORE1_L_RST|R5FSS1_CORE1_L_RST|MSS_RCM|R5FSS0 Core1 Local Reset|
||VIM0_RST|R5FSS1_VIM0_RST|MSS_RCM|R5FSS1 VIM0 Reset|
||VIM1_RST|R5FSS1_VIM1_RST|MSS_RCM|R5FSS1 VIM1 Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 325 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-4. R5FSS[0:1] Hardware Requests** 

|**Module**<br>**Instance**|**Module Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Description**|**Type**|
|---|---|---|---|---|---|
|R5FSS0|**R5FSS0 CORE0 Interrupts**|||||
||R5FSS0_COMMRX_0|R5FSS0_CORE0_INTR_IN_116|R5FSS0_CORE0|R5FSS0 CORE0 DTRRX<br>Full Interrupt|R5FSS<br>Internal|
||R5FSS0_COMMTX_0|R5FSS0_CORE0_INTR_IN_117|R5FSS0_CORE0|R5FSS0 CORE0 DTRTX<br>Empty Interrupt|R5FSS<br>Internal|
||R5FSS0_CPU0_CTI_INT|R5FSS0_CORE0_INTR_IN_118|R5FSS0_CORE0|R5FSS0 CORE0 Cross<br>trigger Interrupt|R5FSS<br>Internal|
|||R5FSS0_CORE1_INTR_IN_118|R5FSS0_CORE1|||
||R5FSS0_CPU0_VALFIQ|R5FSS0_CORE0_INTR_IN_119|R5FSS0_CORE0|R5FSS0 CORE0 fast<br>interrupt|R5FSS<br>Internal|
||R5FSS0_CPU0_VALIRQ|R5FSS0_CORE0_INTR_IN_120|R5FSS0_CORE0|R5FSS0 CORE0 normal<br>interrupt|R5FSS<br>Internal|
||R5FSS0_CORE0_FPU_EXP|R5FSS0_CORE0_INTR_IN_130|R5FSS0_CORE0|R5FSS0 CORE0 floating<br>point exception|R5FSS<br>Internal|
||R5FSS0_CORE0_AHB_WRITE_ER<br>R|R5FSS0_CORE0_INTR_IN_135|R5FSS0_CORE0|R5FSS0 CORE0 AHB<br>write error|Pulse|
||R5FSS0_LIVELOCK_0|R5FSS0_CORE0_INTR_IN_125|R5FSS0_CORE0|R5FSS0 CORE0 Live<br>Lock error|R5FSS<br>Internal|
|||R5FSS1_CORE0_INTR_IN_126|R5FSS1_CORE0|||
|||R5FSS1_CORE1_INTR_IN_126|R5FSS1_CORE1|||
||R5FSS0_CPU0_PMU_INT|R5FSS1_CORE0_INTR_IN_116|R5FSS1_CORE0|R5FSS0_CORE0<br>Performance Monitoring<br>Unit interrupt|R5FSS<br>Internal|
|||R5FSS1_CORE1_INTR_IN_116|R5FSS1_CORE1|||
||R5FSS0_STC_DONE|R5FSS1_CORE0_INTR_IN_132|R5FSS1_CORE0|R5FSS0 Store<br>Coprocessor Registers<br>done|Pulse|
|||R5FSS1_CORE1_INTR_IN_132|R5FSS1_CORE1|||
||R5FSS0_CORE0_RL2_ERR_INTR|R5FSS0_CORE0_INTR_IN_243|R5FSS0_CORE0|R5FSS0 CORE0 RL2<br>Compare Error interrupt|Pulse|
|||R5FSS0_CORE1_INTR_IN_243|R5FSS0_CORE1|||
|||R5FSS1_CORE0_INTR_IN_243|R5FSS1_CORE0|||
|||R5FSS1_CORE1_INTR_IN_243|R5FSS1_CORE1|||
||R5FSS0_CORE0_TMU_LVF|R5FSS0_CORE0_INTR_IN_209|R5FSS0_CORE0|R5SS0 CORE0 TMU LVF|Level|
||R5FSS0_CORE0_TMU_LUF|R5FSS0_CORE0_INTR_IN_210|R5FSS0_CORE0|R5SS0 CORE0 TMU LUF|Level|
||**R5FSS0 CORE1 Interrupts**|||||
||R5FSS0_COMMRX_1|R5FSS0_CORE1_INTR_IN_116|R5FSS0_CORE1|R5FSS0 CORE1 DTRRX<br>Full Interrupt|R5FSS<br>Internal|
||R5FSS0_COMMTX_1|R5FSS0_CORE1_INTR_IN_117|R5FSS0_CORE1|R5FSS0 CORE1 DTRTX<br>Full Interrupt|R5FSS<br>Internal|
||R5FSS0_CPU1_CTI_INT|R5FSS0_CORE1_INTR_IN_119|R5FSS0_CORE1|R5FSS0 CORE1 Cross<br>trigger Interrupt|R5FSS<br>Internal|
|||R5FSS0_CORE0_INTR_IN_121|R5FSS0_CORE0|||
||R5FSS0_CPU1_VALFIQ|R5FSS0_CORE1_INTR_IN_120|R5FSS0_CORE1|R5FSS0 CORE1 fast<br>interrupt|R5FSS<br>Internal|
||R5FSS0_CPU1_VALIRQ|R5FSS0_CORE1_INTR_IN_121|R5FSS0_CORE1|R5FSS0 CORE1 normal<br>interrupt|R5FSS<br>Internal|
||R5FSS0_CORE1_FPU_EXP|R5FSS0_CORE1_INTR_IN_130|R5FSS0_CORE1|R5FSS0 CORE1 floating<br>point exception|R5FSS<br>Internal|
||R5FSS0_CORE1_AHB_WRITE_ER<br>R|R5FSS0_CORE1_INTR_IN_135|R5FSS0_CORE1|R5FSS0 CORE1 AHB<br>write error|Pulse|
||R5FSS0_LIVELOCK_1|R5FSS0_CORE0_INTR_IN_125|R5FSS0_CORE0|R5FSS0 CORE1 Live<br>Lock error|R5FSS<br>Internal|
|||R5FSS1_CORE0_INTR_IN_127|R5FSS1_CORE0|||
|||R5FSS1_CORE1_INTR_IN_127|R5FSS1_CORE1|||
||R5FSS0_CPU1_PMU_INT|R5FSS1_CORE0_INTR_IN_117|R5FSS1_CORE0|R5FSS0_CORE1<br>Performance Monitoring<br>Unit interrupt|R5FSS<br>Internal|
|||R5FSS1_CORE1_INTR_IN_117|R5FSS1_CORE1|||



326 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-4. R5FSS[0:1] Hardware Requests (continued)** 

|**Module**<br>**Instance**|**Module Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Description**|**Type**|
|---|---|---|---|---|---|
|R5FSS0|R5FSS0_CORE1_RL2_ERR_INTR|R5FSS0_CORE0_INTR_IN_244|R5FSS0_CORE0|R5FSS0 CORE1 RL2<br>Compare Error interrupt|Pulse|
|||R5FSS0_CORE1_INTR_IN_244|R5FSS0_CORE1|||
|||R5FSS1_CORE0_INTR_IN_244|R5FSS1_CORE0|||
|||R5FSS1_CORE1_INTR_IN_244|R5FSS1_CORE1|||
||R5FSS0_CORE1_TMU_LVF|R5FSS0_CORE1_INTR_IN_209|R5FSS0_CORE1|R5SS0 CORE1 TMU LVF|Level|
||R5FSS0_CORE1_TMU_LUF|R5FSS0_CORE1_INTR_IN_210|R5FSS0_CORE1|R5SS0 CORE1 TMU LUF|Level|
|R5FSS1|**R5FSS1 CORE0 Interrupts**|||||
||R5FSS1_COMMRX_0|R5FSS1_CORE0_INTR_IN_118|R5FSS1_CORE0|R5FSS1 CORE0 DTRRX<br>Full Interrupt|R5FSS<br>Internal|
||R5FSS1_COMMTX_0|R5FSS1_CORE0_INTR_IN_119|R5FSS1_CORE0|R5FSS1 CORE0 DTRTX<br>Empty Interrupt|R5FSS<br>Internal|
||R5FSS1_CPU0_CTI_INT|R5FSS1_CORE0_INTR_IN_120|R5FSS1_CORE0|R5FSS1 CORE0 Cross<br>trigger Interrupt|R5FSS<br>Internal|
|||R5FSS1_CORE1_INTR_IN_120|R5FSS1_CORE1|||
||R5FSS1_CPU0_VALFIQ|R5FSS1_CORE0_INTR_IN_121|R5FSS1_CORE0|R5FSS1 CORE0 fast<br>interrupt|R5FSS<br>Internal|
||R5FSS1_CPU0_VALIRQ|R5FSS1_CORE0_INTR_IN_122|R5FSS1_CORE0|R5FSS1 CORE0 normal<br>interrupt|R5FSS<br>Internal|
||R5FSS1_CORE0_FPU_EXP|R5FSS1_CORE0_INTR_IN_130|R5FSS1_CORE0|R5FSS1 CORE0 floating<br>point exception|R5FSS<br>Internal|
||R5FSS1_CORE0_AHB_WRITE_ER<br>R|R5FSS1_CORE0_INTR_IN_135|R5FSS1_CORE0|R5FSS1 CORE0 AHB<br>write error|Pulse|
||R5FSS1_LIVELOCK_0|R5FSS1_CORE1_INTR_IN_125|R5FSS1_CORE1|R5FSS1 CORE0 Live<br>Lock error|R5FSS<br>Internal|
|||R5FSS1_CORE0_INTR_IN_126|R5FSS1_CORE0|||
|||R5FSS0_CORE1_INTR_IN_126|R5FSS0_CORE1|||
||R5FSS1_CPU0_PMU_INT|R5FSS0_CORE0_INTR_IN_122|R5FSS0_CORE0|R5FSS1_CORE0<br>Performance Monitoring<br>Unit interrupt|R5FSS<br>Internal|
|||R5FSS0_CORE1_INTR_IN_122|R5FSS0_CORE1|||
||R5FSS1_STC_DONE|R5FSS0_CORE0_INTR_IN_132|R5FSS0_CORE0|R5FSS1 Store<br>Coprocessor Registers<br>done|Pulse|
|||R5FSS0_CORE1_INTR_IN_132|R5FSS0_CORE1|||
||R5FSS1_CORE0_RL2_ERR_INTR|R5FSS0_CORE0_INTR_IN_245|R5FSS0_CORE0|R5FSS1 CORE0 RL2<br>Compare Error interrupt|Pulse|
|||R5FSS0_CORE1_INTR_IN_245|R5FSS0_CORE1|||
|||R5FSS1_CORE0_INTR_IN_245|R5FSS1_CORE0|||
|||R5FSS1_CORE1_INTR_IN_245|R5FSS1_CORE1|||
||R5FSS1_CORE0_TMU_LVF|R5FSS1_CORE0_INTR_IN_209|R5FSS1_CORE0|R5SS1 CORE0 TMU LVF|Level|
||R5FSS1_CORE0_TMU_LUF|R5FSS1_CORE0_INTR_IN_210|R5FSS1_CORE0|R5SS1 CORE0 TMU LUF|Level|
||**R5FSS1 CORE1 Interrupts**|||||
||R5FSS1_COMMRX_1|R5FSS1_CORE1_INTR_IN_118|R5FSS1_CORE1|R5FSS1 CORE1 DTRRX<br>Full Interrupt|R5FSS<br>Internal|
||R5FSS1_COMMTX_1|R5FSS1_CORE1_INTR_IN_119|R5FSS1_CORE1|R5FSS1 CORE1 DTRTX<br>Full Interrupt|R5FSS<br>Internal|
||R5FSS1_CPU1_CTI_INT|R5FSS1_CORE1_INTR_IN_121|R5FSS1_CORE1|R5FSS1 CORE1 Cross<br>trigger Interrupt|R5FSS<br>Internal|
|||R5FSS1_CORE0_INTR_IN_123|R5FSS1_CORE0|||
||R5FSS1_CPU1_VALFIQ|R5FSS1_CORE1_INTR_IN_122|R5FSS1_CORE1|R5FSS1 CORE1 fast<br>interrupt|R5FSS<br>Internal|
||R5FSS1_CPU1_VALIRQ|R5FSS1_CORE1_INTR_IN_123|R5FSS1_CORE1|R5FSS1 CORE1 normal<br>interrupt|R5FSS<br>Internal|
||R5FSS1_CORE1_FPU_EXP|R5FSS1_CORE1_INTR_IN_130|R5FSS1_CORE1|R5FSS1 CORE1 floating<br>point exception|R5FSS<br>Internal|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 327 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-4. R5FSS[0:1] Hardware Requests (continued)** 

|**Module**<br>**Instance**|**Module Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Description**|**Type**|
|---|---|---|---|---|---|
|R5FSS1|R5FSS1_CORE1_AHB_WRITE_ER<br>R|R5FSS1_CORE1_INTR_IN_135|R5FSS1_CORE1|R5FSS1 CORE1 AHB<br>write error|Pulse|
||R5FSS1_LIVELOCK_1|R5FSS1_CORE0_INTR_IN_125|R5FSS1_CORE0|R5FSS1 CORE1 Live<br>Lock error|R5FSS<br>Internal|
|||R5FSS0_CORE0_INTR_IN_127|R5FSS0_CORE0|||
|||R5FSS0_CORE1_INTR_IN_127|R5FSS0_CORE1|||
||R5FSS1_CPU1_PMU_INT|R5FSS0_CORE0_INTR_IN_123|R5FSS0_CORE0|R5FSS1_CORE1<br>Performance Monitoring<br>Unit interrupt|R5FSS<br>Internal|
|||R5FSS0_CORE1_INTR_IN_123|R5FSS0_CORE1|||
||R5FSS1_CORE1_RL2_ERR_INTR|R5FSS0_CORE0_INTR_IN_246|R5FSS0_CORE0|R5FSS1 CORE1 RL2<br>Compare Error interrupt|Pulse|
|||R5FSS0_CORE1_INTR_IN_246|R5FSS0_CORE1|||
|||R5FSS1_CORE0_INTR_IN_246|R5FSS1_CORE0|||
|||R5FSS1_CORE1_INTR_IN_246|R5FSS1_CORE1|||
||R5FSS1_CORE1_TMU_LVF|R5FSS1_CORE1_INTR_IN_209|R5FSS1_CORE1|R5SS1 CORE1 TMU LVF|Level|
||R5FSS1_CORE1_TMU_LUF|R5FSS1_CORE1_INTR_IN_210|R5FSS1_CORE1|R5SS1 CORE1 TMU LUF|Level|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

328 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.1.3 R5FSS Functional Description**_ 

## **7.1.3.1 R5FSS Block Diagram** 

Figure 7-5 shows the R5FSS block diagram. 

## **Figure 7-5. R5FSS Block Diagram** 

**==> picture [482 x 526] intentionally omitted <==**

**----- Start of picture text -----**<br>
VBUSP COnfig TCM<br>32b VBUSP  64b VBUSM<br>32 64<br>ECCAGGR0 VBUSM2AXI<br>64 Memory Access<br>64b VBUSM<br>(Read Only)<br>TCMA<br>64 Memory Access<br>64b VBUSM<br>TCMB0 (Write Only)<br>TCMB1<br>R5F CPU0<br>32<br>Peripheral Access<br>32b VBUSP<br>ETM<br>CTI<br>I$ D$<br>Interrupt VIM Config<br>32b VBUSP<br>CTM CTM<br>Trace ATB Funnel Interrupt VIM Config<br>32b ATB 32b VBUSP<br>I$ D$<br>CTI<br>ETM<br>32 Peripheral Access<br>32b VBUSP<br>Debug Config<br>32b APB R5F CPU1<br>TCMA<br>TCMB0 64 Memory Access<br>64b VBUSM<br>TCMB1 (Read Only)<br>Memory Access<br>64 64b VBUSM<br>(Write Only)<br>Lockstep CCM ECCAGGR1 VBUSM2AXI STC<br>Error<br>32 32 64 32<br>VBUSP COnfig VBUSP COnfig TCM VBUSP COnfig<br>32b VBUSP  32b VBUSP  64b VBUSM  32b VBUSP<br>AXI2VBUSM<br>AHB2VBUSP<br>VIM<br>VIM<br>AHB2VBUSP<br>AXI2VBUSM<br>**----- End of picture text -----**<br>


SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

329 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.1.3.2 R5FSS Cortex-R5F Core** 

The Cortex-R5F is a processor from Arm, which is based on the Armv7-R profile. Each R5FSS implements two R5F cores, CPU0 and CPU1, each with their own RAMs and interfaces. While in reset, they can be bootstrapped to work in one of two modes: Dual Core or Lockstep. 

In dual core mode, each R5F core works completely independent from the other (asymmetric multiprocessing, or AMP). Each core uses its own RAMs and interfaces, with no coherence between the two cores. 

In Lockstep mode: 

- CPU0 is the only operating core 

- CPU1 operates as the lockstep core for CPU0 

- CPU1 TCMs are stacked on CPU0 TCMs and are accessible only by CPU0 and CPU0 TCM interface 

- The TCM size for CPU0 is essentially doubled in this mode 

- CPU1 caches and interrupts are not used 

For a brief list of features supported by the R5F processor in this device, see _R5FSS Features_ . For more detailed description of this processor, see the _Arm Cortex-R5 Technical Reference Manual_ . 

## _**7.1.3.2.1 L1 Caches**_ 

The R5F cores have a Harvard cache architrecture, which means each core has an independent L1 instruction cache (16KB) and L1 data cache (16KB). The instruction cache is protected by SECDED ECC per 64 bits. The data cache is protected by SECDED ECC per 32 bits. 

## _**7.1.3.2.2 Tightly-Coupled Memories (TCMs)**_ 

The R5F has two tightly-coupled memories (TCMs), ATCM and BTCM. The BTCM is further broken down into two interleaved banks, B0TCM and B1TCM. 

TCMs are low-latency, tightly integrated memories for the R5F to use. Either TCM can be used for any combination of instruction and/or data. TCM performance is equal to performance on instructions/data that are in cache. However, TCMs have some additional advantages over cache. TCMs can be loaded with instructions that do not cache well (such as ISRs) or preloaded with code by an external source, before that code is needed, to save cache miss time. TCMs are also a good place for blocks of data for intense processing. They can be loaded (or pre-loaded by an external source) before the data is needed, saving cache miss time. The data can then be directly accessed by an external source, instead of needing to do cache evicts. 

As mentioned, TCMs can be accessed (either read or written) by an external source over the TCM VBUSM peripheral interface. This allows instructions or data to be preloaded, or for data to be read out after the R5F has processed it. The VBUSM peripheral has a lower priority to accessing TCMs than the R5F but care must be taken to keep an external source from reading or writing TCM data that the R5F is working on. This handshaking is external to any of the R5FSS hardware. 

TCMs are protected by ECC per 32 bits. For this to work, ECC must be enabled before data is written in to the TCMs (either externally or from the R5F). ECC is enabled via the following R5F system control bits: ACTLR.ATCMPCEN, ACTLR.B0TCMPCEN, and ACTLR.B1TCMPCEN, respectively. 

Whether or not the TCMs are enabled is controlled by the ENABLE bit in the corresponding ATCM/BTCM region register. The default (reset) value of this bit is determined by the CPUn_INITRAMA and CPUn_INITRAMB bootstrap signals having a default value of 1 in this device. ATCM is configured for a size of 32KB and BTCM is configured for a size of 96KB in this device. Note that the BTCM size is the total of both B0TCM and B1TCM ( 48KB each). Note also that the ATCM size for CPU0 is 64KB and the BTCM size for CPU0 is 192KBeach in Lockstep mode. 

If a TCM is not enabled, then it does not appear in the R5F’s memory view, but it can be accessed by an external source. If a TCM is enabled, then its place in the R5F memory map is determined by a combination of bootstrap signal and system register. The base address of ATCM is 0x0000_0000 and the base address of BTCM is 0x0008_0000. 

330 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

It is possible to preload a TCM with instructions and boot from it. See R5FSS Boot Options for details on TCM booting. 

## _**7.1.3.2.3 R5FSS Special Signals**_ 

Table 7-5 through Table 7-6 list some R5FSS features associated with special signals. 

**Table 7-5. R5FSS0 Special Features** 

|**Feature**|**Comment**|
|---|---|
|Cluster affinity group ID|R5F Cluster 0 (ID = 0x0)|
|Exception handling state at reset<br>0 = Arm<br>1 = Thumb|Controlled via MSS_CTRL R5SS0_TEINIT register setting.<br>Defaults to Arm mode|
|Dual core or Lockstep mode<br>0 = Dual Core mode<br>1 = Lockstep mode|Controlled via MSS_CTRL R5SS0_CONTROL register setting.<br>Defaults to a value defined by eFuse/MMR control|
|CPUn execution halt when coming out of reset (CPUn_HALT)|Controlled via MSS_CTRL R5SS0_COREx_HALT register setting.<br>Defaults to halted state. SeeR5 Core Halting and Unhaltingfor more<br>detail.|
|CPUn exception vectors base address|Defaults to Bootvector RAM address 0x0000_0000|
|CPUn VIM base address|0x50F0 0000|
|CPUn non-maskable fast interrupts enable|Disabled|
|CPUn VBUSM peripheral port enabled at reset|Disabled, not used.|
|CPUn VBUSP peripheral port enable at reset|Defaults to Enabled state|
|CPUn VBUSP peripheral port base address|Defaults to 0x5000_0000|
|CPUn VBUSP peripheral port size|Defaults to 256MB<br>0x5000_0000 to 0x5FFFF_FFFF|
|CPUn VBUSM normal peripheral port base address|Not used|
|CPUn VBUSM normal peripheral port size|Not used|
|CPUn VBUSM virtual peripheral port base address|Not used|
|CPUn VBUSM virtual peripheral port size|Not used|
|CPUn WFI state|Status logged into MSS_CTRL R5SS0_COREx_STAT register bit.<br>See theR5 WFIsection.|
|CPUn WFE state|Status logged into MSS_CTRL R5SS0_COREx_STAT register bit.<br>See theR5 WFIsection.|
|CPU Clockgate Control|Controlled via MSS_RCM R5SS0_COREx_GATE register setting.<br>Individual Core clocks can be gated|
|CPUn TCM Bus Parity|Enabled|



**Table 7-6. R5FSS1 Special Features** 

|**Feature**|**Comment**|
|---|---|
|Cluster affinity group ID|R5F Cluster 1 (ID = 0x1)|
|Exception handling state at reset<br>0 = Arm<br>1 = Thumb|Controlled via MSS_CTRL R5SS1_TEINIT register setting.<br>Defaults to Arm mode|
|Dual core or Lockstep mode<br>0 = Dual Core mode<br>1 = Lockstep mode|Controlled via MSS_CTRL R5SS1_CONTROL register setting.<br>Defaults to a value defined by eFuse/MMR control|
|CPUn execution halt when coming out of reset (CPUn_HALT)|Controlled via MSS_CTRL R5SS1_COREx_HALT register setting.<br>Defaults to halted state. SeeR5 Core Halting and Unhaltingfor more<br>detail.|
|CPUn exception vectors base address|Defaults to Bootvector RAM address 0x0000_0000|
|CPUn VIM base address|0x50F0 0000|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 331 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-6. R5FSS1 Special Features (continued)** 

|**Feature**|**Comment**|
|---|---|
|CPUn non-maskable fast interrupts enable|Disabled|
|CPUn VBUSM peripheral port enabled at reset|Disabled, not used.|
|CPUn VBUSP peripheral port enable at reset|Defaults to Enabled state|
|CPUn VBUSP peripheral port base address|Defaults to 0x5000_0000|
|CPUn VBUSP peripheral port size|Defaults to 256MB<br>0x5000_0000 to 0x5FFFF_FFFF|
|CPUn VBUSM normal peripheral port base address|Not used|
|CPUn VBUSM normal peripheral port size|Not used|
|CPUn VBUSM virtual peripheral port base address|Not used|
|CPUn VBUSM virtual peripheral port size|Not used|
|CPUn WFI state|Status logged into MSS_CTRL R5SS1_COREx_STAT register bit.<br>See theR5 WFIsection.|
|CPUn WFE state|Status logged into MSS_CTRL R5SS1_COREx_STAT register bit.<br>See theR5 WFIsection.|
|CPU Clockgate Control|Controlled via MSS_RCM R5SS1_COREx_GATE register setting.<br>Individual Core clocks can be gated|
|CPUn TCM Bus Parity|Enabled|



## **Switching between Dual Core and Lockstep Mode** 

By default, the R5FSS[0-1] will be in lockstep mode. Switching to dual core mode or staying in lockstep mode is handled through setting a combination of eFuse and MMR bits. See Table 7-7 for a summary of possible combinations. 

**Table 7-7. Settings for Dual Core and Lockstep Modes** 

|**eFuse**<br>**BitEFUSE1_ROW_12_R5SS[0-1**<br>**]_FORCE_DUAL_CORE**|**eFuse**<br>**BitEFUSE1_ROW_12_R5SS[0-1**<br>**]_DUAL_CORE_DISABLE**|**MMR**<br>**BitR5SS[0-1]_CONTROL_LOCK**<br>**_STEP**|**R5FSS[0-1] Mode**|
|---|---|---|---|
|0|0|0|Dual Core|
|0|0|1|Lockstep (default)|
|1|X|X|Dual Core|
|0|1|X|Lockstep|



Based on the part number, the eFuse bits will decide whether the MMR can be used for switching to dual core. Follow the below sequence in such cases. 

- Set R5SSx_RST_ASSERDLY and MSS_RCM.R5SSx_RST2ASSERTDLY registers with required reset asserting and holding delay. 

- Set:R5SS[0-1]_CONTROL_LOCK_STEP to 0. 

- Set R5SS[0-1]_CONTROL_LOCK_STEP_SWITCH_WAIT to 0 or 7 based on application use case. Setting to 7 is recommended. 

- By default, reset FSM (or any reset to R5FSS[0-1]_CORE[0-1]) will wait for CPU to go to WFI state for safe handling of system. Setting R5SS[0-1]_FORCE_WFI_ CR5_WFI_OVERIDE to 7 would override the WFI check but this is not recommended. 

- Set R5SS[0-1]_CONTROL_RESET_FSM_TRIGGER to 7 will reset the R5FSS[0-1] and switch mode to dual core. 

- Read R5SS[0-1]_STATUS_REG_ LOCK_STEP for status (0 is dual core and 1 is lockstep). 

332 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.1.3.3 R5FSS Interfaces** 

## _**7.1.3.3.1 Initiator Interfaces**_ 

The R5FSS has several controller interfaces per core: 

- 64-bit VBUSM controller pair (1 read, 1 write) for L2 memory accesses; this is the main memory interface 

- 32-bit VBUSP controller for peripheral access 

   - Includes logic that provides the R5F CPU with a private access to VIM 

   - Enabled at reset 

## _**7.1.3.3.2 Target Interfaces**_ 

The R5FSS has several target interfaces that define its internal memory space: 

- 32-bit VBUSP configuration target (per core) 

   - ECC aggregator block 

- 64-bit VBUSM target (per core) 

   - ATCM 

   - BTCM 

   - Instruction cache RAMs 

   - Data cache RAMs 

- 32-bit VBUSP Configuration target 

   - Lockstep Compare block 

   - Selftest Logic Block 

- 32-bit debug target 

   - Provides access to all R5FSS internal debug logic 

The 64-bit VBUSM target interface provides direct access to the TCM RAMs. Access to the RAMs is arbitrated with access from the R5F’s L1 memory system. Excessive access while the R5F is also attempting access will degrade performance. 

The 64-bit VBUSM target target interface provides access to the cache RAMs for testing purposes. Access to the cache RAMs can only be done while the caches are disabled and should only be done for test purposes. 

In addition to the target interfaces, there are peripherals (VIM) that are only accessible by the R5F. The R5F has an access to these modules via the VBUSP peripheral interface. 

## **7.1.3.4 R5FSS Power, Clocking and Reset** 

## _**7.1.3.4.1 R5FSS Power**_ 

R5FSS is powered by the SoC Core logic supply. 

## _**7.1.3.4.2 R5FSS Clocking**_ 

The R5FSS has a single clock input. Internally, CPU0 and CPU1 clocks are generated from this clock with individual clock gate control per Core. The interface clocks are derived from this clock internally through suitable division. 

The Interface clock is an integer ratio of the CPU clock. The permitted ratio are 1:1 and 1:2 for CPU_CLK:INTERFACE_CLK. The Interface clock shall not exceed 200MHz. 

Refer to R5SS and SYSCLK Clock Tree for more details regarding the sequence for choosing CPU and INTERFACE clocks. 

The CPU core clock can be gated by writing 7 to R5SS[0-1]_CORE[0-1]_GATE_CLKGATE. However, the application code must ensure there are no pending transactions/instructions before executing the gating. 

## _**7.1.3.4.3 R5FSS Reset**_ 

The R5FSS has seven reset inputs: 

- POR_RST : This is the reset for the full R5FSS including debug logic 

- CORE0_G_RST : This resets the entire CPU0 logic including its associated VIM except the debug logic. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 333 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- CORE1_G_RST: This resets the entire CPU1 logic including its associated VIM except the debug logic 

- CORE0_L_RST : THis resets CPU0 core 

- CORE1_L_RST : THis resets CPU1 core 

- VIM0_RST : THis resets VIM0 

- VIM1_RST: This resets VIM1 

The above resets can be controlled through RCM registers. 

In addition to the reset signals, there are two halt signals: 

- CORE0_HALT 

- CORE1_HALT 

These halt signals keep the CPUs from fetching instructions when they come out of reset. The main use is to have the CPUs halted until the TCMs are loaded (when booting from TCM), though halt could be used for any other purpose. See R5 Core Halting and Unhalting for more details. 

## _**7.1.3.4.4 R5FSS Reset Sequencing**_ 

The proper sequence for resetting the R5FSS is as follows: 

- Set R5SSx_RST_ASSERDLY and MSS_RCM.R5SSx_RST2ASSERTDLY registers with required reset asserting and holding delay. 

- By default, the reset FSM (or any reset to R5FSS[0-1]_CORE[0-1]) waits for CPU to go to WFI state for safe handling of system. Setting R5SS[0-1]_FORCE_WFI_ CR5_WFI_OVERIDE to 7 overrides the WFI check but this is not recommended. 

- Set the corresponding reset bit field, refer to R5FSS Reset for further details. 

- Read the R5SS[0-1]_RST_STATUS_CAUSE register to know the status of the initiated reset . 

- Set R5SS[0-1]_RST_CAUSE_CLR_CLR register to reset the captured status of R5SS[0-1]_RST_STATUS_CAUSE register. 

## **Note** 

Care must be taken to read all the R5SS[0-1]_RST_STATUS_CAUSE register status bits before clearing them. 

These resets do not reset the target and initiator ports as these are connected with the common bus to the SoC interconnects. Use INFRA_RST_CTRL_ASSERT bit field to reset the full SoC interconnect infrastructure. This is not recommended for use and must only be used by the application code when there is no pending transactions/tasks. 

## **7.1.3.5 R5FSS Vectored Interrupt Manager (VIM)** 

## **Note** 

For additional details related to the R5FSS VIM, refer to the _Vectored Interrupt Manager (VIM)_ interrupt controller section of the _Interrupts_ chapter. 

## **7.1.3.6 R5FSS ECC Support** 

The R5F provides native ECC and parity support on all related memories, generating and checking the redundancy automatically. The methods for checking and reporting errors are available in the _Arm Cortex-R5 Technical Reference Manual_ . 

The R5FSS adds the capability of testing this logic by allowing errors (single and double bit) to be injected into memories (for testing purposes) via an ECC aggregator (per core). Note that because the R5FSS ECC aggregator is only used in error-injection mode for R5 related memories, it only supports a subset of the generic ECC aggregator functionality for R5 memories. However, the ECC aggregator supports full ECC aggregator functionality for VIM memories. 

For a detailed description of the generic ECC aggregator functionality, see ECC Aggregator. For register descriptions of R5FSS CPU0 and CPU1 ECC aggregators, see _R5FSS_CPU0_ECC_AGGR_CFG_REGS Registers_ and _R5FSS_CPU1_ECC_AGGR_CFG_REGS Registers_ , respectively. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

334 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

Table 7-8 provides the RAM ID for each core. This is needed for bit field [10-0] ECC_VECTOR in the corresponding R5FSS_CPU0_VECTOR / R5FSS_CPU1_VECTOR register (part of the ECC aggregator register space). 

**Table 7-8. RAM ID Map for ECC Aggregator (Per** 

**Core)** 

|**RAM ID**|**Memory Name**|
|---|---|
|0|CPU0/1 ITAG RAM0|
|1|CPU0/1 ITAG RAM1|
|2|CPU0/1 ITAG RAM2|
|3|CPU0/1 ITAG RAM3|
|4|CPU0/1 IDATA BANK0|
|5|CPU0/1 IDATA BANK1|
|6|CPU0/1 IDATA BANK2|
|7|CPU0/1 IDATA BANK3|
|8|CPU0/1 DTAG RAM0|
|9|CPU0/1 DTAG RAM1|
|10|CPU0/1 DTAG RAM2|
|11|CPU0/1 DTAG RAM3|
|12|CPU0/1 DDIRTY RAM|
|13|CPU0/1 DDATA RAM0|
|14|CPU0/1 DDATA RAM1|
|15|CPU0/1 DDATA RAM2|
|16|CPU0/1 DDATA RAM3|
|17|CPU0/1 DDATA RAM4|
|18|CPU0/1 DDATA RAM5|
|19|CPU0/1 DDATA RAM6|
|20|CPU0/1 DDATA RAM7|
|21|CPU0/1 ATCM BANK0|
|22|CPU0/1 ATCM BANK1|
|23|CPU0/1 B0TCM BANK0|
|24|CPU0/1 B0TCM BANK1|
|25|CPU0/1 B1TCM BANK0|
|26|CPU0/1 B1TCM BANK1|
|27|CPU0/1 VIM RAM|
|28|CPU0/1 RL2 TAG RAM|



## **7.1.3.7 R5FSS Memory View** 

The memory view of each R5F (that is, the memory map as seen by each R5F) is a function of several things: 

- Exception vector bootstrap: The R5F exception table (including boot vector) is always 32 bytes at address 0x00000000 as seen by the R5F. 

- TCM locations: TCMs can be enabled or disabled and located at different places in the memory map, depending on bootstrap configuration. In addition, the TCM size varies depending on the mode of CPU being in Dual core or lockstep mode. For more details, see Tightly-Coupled Memories (TCM). 

- Peripheral interface locations: Peripherals are accessed at address 0x5000_0000 over the VBUSP peripheral interface. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 335 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

The combination of the above determines what the R5F sees where in the memory map, and over what interface different transactions come out. Every transaction that does not directly address a TCM or a peripheral interface comes over the main memory interface. 

See _Memory Map_ for the complete R5F memory view for this device. 

## **7.1.3.8 R5FSS Interrupts** 

All interrupts and events generated by the R5FSS are summarized in R5FSS Integration, along with their mapping. These processor events can be divided into the following groups: 

- R5F CPU internal interrupts and events: these include the R5 EVENT signals and PMU interrupts. These are described in the _Arm Cortex-R5 Technical Reference Manual_ . 

- ECC аggregator interrupts: only VIM memory errors generate the interrupt. These are described in the _ECC Aggregator_ chapter. 

- TCM Address parity Error Interrupts: these are described in the _TCM Address Parity Error_ section. 

- Lockstep Compare Interrupts: these are described in the _Lockstep Compare_ section. 

- Selftest Logic Interrupt: interrupts and errors generated by selftest logic. These are described in the _Selftest Controller (STC)_ chapter. 

## **7.1.3.9 R5FSS Debug and Trace** 

The R5FSS supports standard Arm CoreSight debug and trace architecture. For more details, see the _On-chip Debug_ chapter. 

## **7.1.3.10 R5FSS Boot Options** 

R5FSS boots from 0x0000_0000 located in TCM. When the processor exits reset, it fetches the boot vector from this location. 

The software must take the following steps: 

1. Assert the correct bootstraps 

   - a. Enable the ATCM (set CPUn_INITRAMA) or BTCM (set CPUn_INITRAMB). Default state is both are enabled and no additional configuration needed in this device 

   - b. Assert CPUn_LOCZRAMA properly for the desired TCMA. Default state is to boot from ATCM in this device. 

2. Assert CPUn_HALT. Default is HALTED state. 

3. Release the CPU from reset. 

4. Load the desired code into the TCM via the TCM target port. 

   - a. Exception vectors should be located at address 0x00000000 of TCM. 

5. De-assert CPUn_HALT. 

## **7.1.3.11 R5FSS Events** 

The R5F core generates several events as part of event bus. That can be monitored by the PMU for debugging.The R5 core event bus only signals event when it is enabled. Non-invasive or invasive debug mode needs to be enabled to enable the PMU counters. 

The export of the events to the event bus can be enabled by setting the X bit in the Performance Monitor Control Register of the R5 core. For more details, refer to Arm R5 TRM. 

## _**7.1.3.11.1 R5FSS Core Memory ECC Events**_ 

The memory ECC-related events from the event bus are aggregated in MSS_CTRL and exported to ESM for monitoring as shown in _R5FSS Integration_ . 

There are four ECC interrupts to the ESM that aggregate different categories of ECC events: 

- CPU0 correctable error or single bit error 

- CPU1 Correctable error or single but error 

336 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- CPU0 Uncorrectable error or multi bit error 

- CPU1 Uncorrectable error or multibit error 

**Table 7-9. R5 Event Bus Correctable Error or Single-bit Error** 

|**EVENT BUS Bit #**|**Description**|**Associated Status Register in MSS_CTRL**|
|---|---|---|
|40|ATCM single-bit ECC error|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[0]<br>R5SS*_CPU*_ATCM_CORR_ERR|
|42|B1TCM single-bit ECC error|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[1]<br>R5SS*_CPU*_B1TCM_CORR_ERR|
|41|B0TCM single-bit ECC error|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[2]<br>R5SS*_CPU*_B0TCM_CORR_ERR|
|24|Data cache tag or dirty RAM parity error<br>or correctable ECC error, from data-side<br>or ACP|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[3]<br>R5SS*_CPU*_DTAG_CORR_ERR|
|25|Data cache data RAM parity error or<br>correctable ECC error|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[4]<br>R5SS*_CPU*_DDATA_CORR_ERR|
|22|Instruction cache tag RAM parity or<br>correctable ECC error|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[5]<br>R5SS*_CPU*_ITAG_CORR_ERR|
|23|Instruction cache data RAM parity or<br>correctable ECC error|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[6]<br>R5SS*_CPU*_IDATA_CORR_ERR|



**Table 7-10. R5 Event Bus Uncorrectable Error or Multi-bit Error** 

|**EVENT BUS Bit #**|**Description**|**Associated Status Register in MSS_CTRL**|
|---|---|---|
|37|ATCM multi-bit ECC error|R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS[0]<br>R5SS*_CPU*_ATCM_UNCORR_ERR|
|39|B1TCM multi-bit ECC error|R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS[1]<br>R5SS*_CPU*_B1TCM_UNCORR_ERR|
|38|B0TCM multi-bit ECC error|R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS[2]<br>R5SS*_CPU*_B0TCM_UNCORR_ERR|
|34|Data caches tag/dirty RAM fatal ECC<br>error, from data-side or ACP.|R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS[3]<br>R5SS*_CPU*_DTAG_UNCORR_ERR|
|33|Data cache data RAM fatal ECC error|R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS[4]<br>R5SS*_CPU*_DDATA_UNCORR_ERR|



## **7.1.3.12 R5FSS TCM Address Parity Error** 

R5FSS in this device is configured to generate TCM address and control bus parity. Parity error detection logic in the R5FSS detects if there is any parity error on TCM address bus. These errors are aggregated in the MSS_CTRL module and one interrupt per CPU is exported to ESM. 

**Table 7-11. R5 TCM Address Parity Error** 

|**Description**|**Associated Status Register in MSS_CTRL**|
|---|---|
|ATCM bus Address parity Error|R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_STATUS<br>[0]<br>R5SS*_CPU*_ATCM*_PARITY_ERR|
|B0TCM bus Address parity Error|R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_STATUS<br>[1]<br>R5SS*_CPU*_B0TCM*_PARITY_ERR|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

337 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Table 7-11. R5 TCM Address Parity Error (continued)** 

|**Description**|**Associated Status Register in MSS_CTRL**|
|---|---|
|B1TCM bus Address parity Error|R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_STATUS<br>[2]<br>R5SS*_CPU*_B1TCM*_PARITY_ERR|



R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_STATUS_RAW: Provides raw status of TCM address Parity Error for each CPU Core 

R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_STATUS: Provides masked status of TCM Address Parity Error for each CPU Core 

R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_MASK: Mask register for TCM Address Parity Error 

The register R5SS*_TCM_ADDRPARITY_CLR clears Parity Error interrupt. 

The registers R5SS*_CORE*_ADDRPARITY_ERR_*TCM provides the Address location where the TCM address error occurred. 

The R5SS*_TCM_ADDRPARITY_ERRFORCE register can be used to force error on TCM Address parity Error detection logic for diagnostic purpose. 

## **7.1.3.13 R5FSS Lockstep Compare** 

This chapter describes the CPU compare module for the ARM[®] Cortex[®] -R5F (CCM-R5F). Each R5F subsystem (R5FSS) in the device implements two instances of the Cortex-R5F CPU that are running in lockstep to detect faults that may result in unsafe operating conditions. The CCM-R5F detects faults and signals them to the SOC error signaling module. 

**7.1.3.13.1 Overview** ..............................................................................................................................................339 **7.1.3.13.2 Module Operation** ............................................................................................................................... 340 **7.1.3.13.3 Control Registers** ................................................................................................................................348 

338 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.1.3.13.1 Overview**_ 

Safety-critical applications require run-time detection of faults in critical components in the device such as the Central Processing Unit (CPU) and the Vectored Interrupt Controller Module (VIM). For this purpose, the CPU Compare Module for Cortex-R5F (CCM-R5F) compares the core bus outputs of two Cortex-R5F CPUs running in a 1oo1D (one-out-of-one, with diagnostics) lockstep configuration. Each R5FSS also implements two VIM modules in 1oo1D (one-out-of-one, with diagnostic) lockstep configuration. Any difference in the core compare bus outputs of the CPUs or the VIMs is flagged as an error. For diagnostic purposes, the CCM-R5F also incorporates a self-test capability to allow for boot time checking of hardware faults within the CCM-R5F itself. 

In addition to comparing the CPU's and VIM's outputs for fault detection during run-time, the CCM-R5F also incorporates one additional run-time diagnostic feature: the Checker-CPU Inactivity Monitor. 

The Checker-CPU inactivity monitor monitors the checker CPU's key bus signals to the interconnect. When the two CPUs are in lockstep configuration, several key bus signals from the checker CPU which would have indicated a valid bus transaction to the interconnect on the microcontroller will be monitored. A list of the signals to be monitored is provided in theChecker CPU Signals to Monitor table. These signals from the checker CPU are expected to be inactive. All transactions between the lockstep CPUs and the rest of the system should only go through the main CPU. Any signals which indicate activity will be flagged as an error. 

## _**7.1.3.13.1.1 Main Features**_ 

The main features of the CCM-R5F are: 

- Run-time detection of faults 

   - Run-time compare of CPU's outputs 

   - Run-time compare of VIM's outputs 

   - Run-time inactivity monitor on the checker CPU's bus signals to the interconnect 

- self-test capability 

- error forcing capability 

## _**7.1.3.13.1.2 Block Diagram**_ 

Figure 7-6 shows the interconnect diagram of the CCM-R5F with the two Cortex-R5F CPUs and the two VIMs. The core bus outputs of the CPUs are compared in the CCM-R5F. To avoid common mode impacts, the signals of the CPUs to be compared are temporally diverse. The output signals of the primary CPU are delayed 2 cycles while the input signals of checker CPU are delayed 2 cycles. The two cycle delay strategy is also deployed between the two VIM modules. While in lockstep mode, the checker CPU's output signals to the system are clamped to inactive safe values. Key signals which would have indicated a valid bus transaction to the interconnect are monitored by the CCM-R5F. The same approach is used for the key power domains if inactive signals indicate that bus controllers inside these power domains are asserting valid bus transactions. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

339 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 310] intentionally omitted <==**

**----- Start of picture text -----**<br>
Outputs CPU2 to the  Outputs from CPU1 to  cpu1clk<br>system the system<br>CCM-R5F<br>2 cycle delay CPU Bus Compare<br>Compare errors<br>Checker CPU  ESM<br>Inactivity Monitor<br>VIM Bus Compare<br>Lockstep<br>mode<br>VIM1 VIM2<br>Safe values (values that will<br>force the checker CPU’s  CPU2<br>CPU1<br>outputs to inactive states)   (Checker<br>(Main CPU)<br>CPU)<br>Lockstep mode<br>2 cycle delay<br>cpu2clk<br>Inputs to CPU1 Inputs to CPU2<br>**----- End of picture text -----**<br>


**Figure 7-6. Block Diagram** 

## _**7.1.3.13.2 Module Operation**_ 

As described in Overview, there are three different run-time diagnostics supported by the CCM-R5F. The CCM-R5F compares the core bus outputs of the primary and checker Cortex-R5F CPUs on the microcontroller and signals an error on any mismatch. This comparison is started 6 CPU clock cycles after the CPU comes out of reset to ensure that CPU output signals have propagated to a known value after reset. Once comparison is started, the CCM module continues to monitor the outputs of the two CPUs without any software intervention. If an error is detected by the CCM-R5F, a software handler is necessary to implement the appropriate response to the error dependent on application needs. The module principles of operation are applicable to both the CPU output compare as described above as well as to the VIM output compare. 

340 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.1.3.13.2.1 CPU/VIM Output Compare Diagnostic**_ 

CPU / VIM Output Compare Diagnostic can run in one of the following four operating modes: 

1. Active compare lockstep mode 

2. Self-test 

3. Error forcing 

4. Self-test error forcing 

The operating mode can be selected by writing a dedicated key to the key register (MKEYx) of the corresponding diagnostic. 

## **Note** 

MKEY1 and MKEY2 are used to select the operating mode for the CPU Output Compare Diagnostic and VIM Output Compare Diagnostic, respectively. 

## _**7.1.3.13.2.1.1 Active Compare lockstep Mode**_ 

This is the default mode on start-up. In lockstep mode, the bus output signals of both CPUs and VIMs are compared. A difference in the CPU compare bus outputs is indicated by signaling an error to the ESM, which sets the error flag "CCM-R5F - CPU compare" and "CCM-R5F - VIM compare", respectively. 

- CPU types of output signals to be compared: 

   - Global signals 

   - Interrupt signals 

   - All L1 cache interface signals 

   - All cache coherency signals 

   - All L1 TCM interface signals 

   - All L2 AXI interface signals 

   - ETM interface signals 

   - FPU signals 

   - All AHB Peripheral port interface signals 

   - All status and control signals 

- VIM output signals to be compared: 

   - nFIQ 

   - nIRQ 

   - IRQADDRV 

   - IRQVECTADDR 

- CPU types of output signals that are not compared: 

   - All ACP interface signals 

   - All AXI Peripheral port interface signals 

## **Note** 

The CPU compare error asserts “CCM-R5F self-test error” flag as well. By doing this, the CPU compare error has two paths (“CCM-R5F - CPU compare” and “CCM-R5F self-test error” flag) to the ESM, so that even if one of the paths fails, the error is still propagated to the ESM. This is also true for "CCM-R5F - VIM compare" error flag. 

Not all internal registers of the Cortex-R5F CPU have fixed values upon reset. To avoid an erroneous CCM-R5F compare error, the application software needs to ensure that the CPU registers of both CPUs are initialized with the same values before the registers are used, including function calls where the register values are pushed onto the stack. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

341 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.1.3.13.2.1.2 Self-Test Mode**_ 

In self-test mode, the CCM-R5F checks itself for faults. During self-test, the compare error module output signal is deactivated. Any fault detected inside the CCM-R5F will be flagged by ESM error “CCM-R5F - self-test”. 

In self-test mode, the CCM-R5F automatically generates test patterns to look for any hardware faults. If a fault is detected, then a self-test error flag is set, a self-test error signal is asserted and sent to the ESM, and the self-test is terminated immediately. If no fault is found during self-test, the self-test complete flag is set. In both cases, the CCM-R5F CPU / VIM Output Compare Diagnostic remains in self-test mode after the test has been terminated or completed, and the application needs to switch the CCM-R5F mode by writing another key to the mode key register (MKEY1 or MKEY2 depending which diagnostic is selected for self-test). During the self-test operation, the compare error signal output to the ESM is inactive irrespective of the compare result. 

There are two types of patterns generated by CCM-R5F during self-test mode: 

1. Compare Match Test 

2. Compare Mismatch Test 

CCM-R5F first generates Compare Match Test patterns, followed by Compare Mismatch Test patterns. Each test pattern is applied on both CPU signal inputs of the CCM-R5F’s compare block and clocked for one cycle. The duration of self-test for CPU Output Compare Diagnostic is 4947 CPU clock cycles (GCLK1) and 151 system peripheral clock cycles (VCLK) for VIM Output Compare Diagnostic. 

## **Note** 

During self-test, both CPUs can execute normally, but the compare logic will not be checking any CPU signals. Also during self-test, only the compare unit logic is tested and not the memory-mapped register controls for the CCM-R5F. The self-test is not interruptible. 

Self-test of all different diagnostics can be run at the same time. 

## _**7.1.3.13.2.1.2.1 Compare Match Test**_ 

During the Compare Match Test, there are four different test patterns generated to stimulate the CCM-R5F. An identical vector is applied to both input ports at the same time expecting a compare match. These patterns cause the self-test logic to exercise every CPU compare bus output signal in parallel. If the compare unit produces a compare mismatch then the self-test error flag is set, the self-test error signal is generated, and the Compare Match Test is terminated. 

The four test patterns used for the Compare Match Test are: 

- All 1s on both CPU / VIM signal ports 

- All 0s on both CPU / VIM signal ports 

- 0xAs on both CPU / VIM signal ports 

- 0x5s on both CPU / VIM signal ports 

These four test patterns will take four clock cycles to complete. Table 7-12 illustrates the sequence of Compare Match Test. 

**Table 7-12. Compare Match Test Sequence** 

|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**Cl**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**n:8**|**7**|**6**|**5**|**4**|**3**|**2**|**1**|**0**|**n:8**|**7**|**6**|**5**|**4**|**3**|**2**|**1**|**0**|**yce**|
|1s|1|1|1|1|1|1|1|1|1s|1|1|1|1|1|1|1|1|0|
|0s|0|0|0|0|0|0|0|0|0s|0|0|0|0|0|0|0|0|1|
|0xA|1|0|1|0|1|0|1|0|0xA|1|0|1|0|1|0|1|0|2|
|0x5|0|1|0|1|0|1|0|1|0x5|0|1|0|1|0|1|0|1|3|



342 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.1.3.13.2.1.2.2 Compare Mismatch Test**_ 

During the Compare Mismatch Test, the number of test patterns is equal to twice the number of CPU output signals to compare in lockstep mode. An all 1s vector is applied to the CCM-R5F’s CPU1 / VIM1 input port and the same pattern is also applied to the CCM-R5F’s CPU2 /VIM2 input port but with one bit flipped starting from signal position 0. The un-equal vector will cause the CCM-R5F to expect a compare mismatch at signal position 0, if the CCM-R5F logic is working correctly. If, however, the CCM-R5F logic reports a compare match, the self-test error flag is set, the self-test error signal is asserted, and the Compare Mismatch Test is terminated. 

This Compare Mismatch Test algorithm repeats in a domino fashion with the next signal position flipped while forcing all other signals to logic level 1. This sequence is repeated until every single signal position is verified on both CPU signal ports. 

The Compare Mismatch Test is terminated if the CCM-R5F reports a compare match versus the expected compare mismatch. This test ensures that the compare unit is able to detect a mismatch on every CPU signal being compared. Table 7-13 illustrates the sequence of Compare Mismatch Test. There is no error signal sent to ESM if the expected errors are seen with each pattern. 

**Table 7-13. CPU / VIM Compare Mismatch Test Sequence** 

|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 1 (Main CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**CPU 2 (Checker CPU) Signal Position**|**Cl**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**n**|**n–1:8**||**7**|**6**|**5**|**4**|**3**|**2**|**1**|**0**|**n**|**n–1:8**||**7**|**6**|**5**|**4**|**3**|**2**|**1**|**0**|**yce**|
|1|1|1s|1|1|1|1|1|1|1|1|1|1|1s|1|1|1|1|1|1|1|0|0|
|1|1|1s|1|1|1|1|1|1|1|1|1|1|1s|1|1|1|1|1|1|0|1|1|
|1|1|1s|1|1|1|1|1|1|1|1|1|1|1s|1|1|1|1|1|0|1|1|2|
|1|1|1s|1|1|1|1|1|1|1|1|1|1|1s|1|1|1|1|0|1|1|1|3|
|::|||||||||||||||||||||||
|1|1|1s|1|1|1|1|1|1|1|1|1|0|1s|1|1|1|1|1|1|1|1|–1|
|1|1|1s|1|1|1|1|1|1|1|1|0|1|1s|1|1|1|1|1|1|1|1|n|
|1|1|1s|1|1|1|1|1|1|1|0|1|1|1s|1|1|1|1|1|1|1|1|n+1|
|1|1|1s|1|1|1|1|1|1|0|1|1|1|1s|1|1|1|1|1|1|1|1|n+2|
|1|1|1s|1|1|1|1|1|0|1|1|1|1|1s|1|1|1|1|1|1|1|1|n+3|
|1|1|1s|1|1|1|1|0|1|1|1|1|1|1s|1|1|1|1|1|1|1|1|n+4|
|::|||||||||||||||||||||||
|1|0|1s|1|1|1|1|1|1|1|1|1|1|1s|1|1|1|1|1|1|1|1|2n-1|
|0|1|1s|1|1|1|1|1|1|1|1|1|1|1s|1|1|1|1|1|1|1|1|2n|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

343 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.1.3.13.2.1.3 Error Forcing Mode**_ 

In error forcing mode, a test pattern is applied to the CPU / VIM related inputs of the CCM-R5F compare logic to force an error in the compare error output signal of the compare unit. Depending if error forcing mode is applied to the CPU Output Compare Diagnostic or VIM Output Compare Diagnostic, the ESM error flag “CCM-R5F - CPU compare” or “CCM-R5F - VIM compare” is expected after the error forcing mode completes. As a side effect, the “CCM-R5F self-test error” flag is also asserted whenever the CPU compare error is asserted. 

Error forcing mode is similar to the Compare Mismatch Test operation of self-test mode in which an un-equal vector is applied to the CCM-R5F CPU signal ports. The error forcing mode forces the compare mismatch to actually assert the compare error output signal. This ensures that a fault in the path between CCM-R5F and ESM is detected. 

Only one hardcoded test pattern is applied into CCM-R5F during error forcing mode. A repeated 0x5 pattern is applied to CPU1 / VIM1 signal port of CCM-R5F input while a repeated 0xA pattern is applied to the CPU2 / VIM2 signal port of CCM-R5F input. The error forcing mode takes one cycle to complete. Hence, the failing signature is presented for one clock cycle. After that, the mode is automatically switched to lockstep mode. The key register (MKEY1 for CPU output compare and MKEY2 for VIM output compare) will indicate the lockstep key mode once it is switched to lockstep mode. During the one cycle required by the error forcing test, the CPU / VIM output signals are not compared. The user should expect the ESM to trigger a response (report the CCM-R5F fail). If no error is detected by the ESM, then a hardware fault is present. 

## _**7.1.3.13.2.1.4 Self-Test Error Forcing Mode**_ 

In self-test error forcing mode, an error is forced at the self-test error signal. The compare unit is still running in lockstep mode and the key is switched to lockstep after one clock cycle. The ESM error flag “CCM-R5F - self-test” is expected after the self-test error forcing mode completes. Once the expected errors are seen, the application can clean the error through the ESM module. 

Table 7-14 shows what error signals and flags are asserted in different operating mode. The behavior of different modes in this table for CPU compare is also valid for other diagnostics such as VIM compare and Checker CPU Inactivity Monitor. 

**Table 7-14. Error Flags and Error Signals Generation in Each Mode** 

|**Mode**|**Key**|**Self Test**<br>**Error Signal**|**Compare**<br>**Error Signal**|**CMPE**|**STC**|**STET**|**STE**|
|---|---|---|---|---|---|---|---|
|Active<br>Compare<br>Lockstep|0000|Enabled|Enabled|Enabled|Disabled|Disabled|Disabled|
|Self-Test|0110|Enabled|Disabled|Disabled|Enabled|Enabled|Enabled|
|Error Forcing|1001|Error|Error|Disabled|Disabled|Disabled|Disabled|
|Self-Test Error<br>Forcing|1111|Error|Enabled|Enabled|Disabled|Disabled|Disabled|



344 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.1.3.13.2.2 CPU Input Inversion Diagnostic**_ 

There is another way to intentionally create a mismatch between the two CPUs' outputs as a diagnostic test to self-test the CCM-R5F's CPU Output Compare Diagnostic block. Before the CPU1's outputs are taken to the CCM-R5F, eight of the output signals are first exclusive-ORed bitwise with the 8-bit POLARITYINVERT register. After reset, the default value of the POLARITYINVERT register is all zeros. The resultant values of the 8 signals after the XOR logic with the POLARITYINVERT register will still be the same as the original 8 signal values. However, by programming the POLARITYINVERT to a non-zero values it will have the effect to invert the signal values. This intentional inversion on the inputs to the CCM-R5F will cause the CPU Output Compare Diagnostic to detect a compare error. See Figure 7-7 for illustration. 

**==> picture [468 x 182] intentionally omitted <==**

**----- Start of picture text -----**<br>
N N-8 N<br>CPU1<br>8<br>XOR<br>CCM<br>POLARITYINVERT ESM<br>R5F<br>CPU2<br>**----- End of picture text -----**<br>


**Figure 7-7. CPU Input Inversion Scheme** 

**Table 7-15. CPU1 (Main CPU) Signals Being Inverted Before Being Compared** 

|**Signals**|**Remark**|
|---|---|
|AWVALIDM|Indicates write address and control are valid|
|ARVALIDM|Indicates write address and control are valid|
|AWVALIDP|Indicates write address and control are valid|
|ARVALIDP|Indicates write address and control are valid|
|HTRANSP[1:0]|Indicates write address and control are valid|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

345 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.1.3.13.2.3 Checker CPU Inactivity Monitor**_ 

Similar to the CPU / VIM Output Compare Diagnostic, the Checker CPU Inactivity Monitor can also run in one of the following four operating modes: 

1. Active compare 

2. Self-test 

3. Error forcing 

4. Self-test error forcing 

The operating mode can be selected by writing a dedicated key to the key register (MKEY3). 

## _**7.1.3.13.2.3.1 Active Compare Mode**_ 

This is the default mode on start-up. In this mode, several key bus signals such as the bus valid control signals from the checker CPU that would have indicated a valid bus transaction onto the interconnect are compared against their clamped safe values. While the two CPUs are in lockstep configuration, the outputs of the checker CPU are supposed to clamp to the inactive state that is all zeros. A difference between the checker CPU compare bus outputs and their respective inactive states is indicated by signaling an error to the ESM which sets the error flag "CCM-R5F - CPU1 AXIM Bus Monitor Failure". 

**Table 7-16. Checker CPU Signals to Monitor** 

|**Signals**|**Remark**|
|---|---|
|AWVALIDM|When asserted, indicates address and control are valid on the Checker CPU's AXI controller port for<br>write transaction.|
|ARVALIDM|When asserted, indicates address and control are valid on the Checker CPU's AXI controller port for<br>read transaction.|
|AWVALIDP|When asserted, indicates address and control are valid on the Checker CPU's AXI peripheral port for<br>write transaction.|
|ARVALIDP|When asserted, indicates address and control are valid on the Checker CPU's AXI peripheral port for<br>read transaction.|
|BVALIDS|When asserted, indicates that a valid write response is available on the Checker CPU's AXI peripheral<br>port for write transaction|
|RVALIDS|When asserted, indicates address and control are valid on the Checker CPU's AXI peripheral port for<br>read transaction|



## _**7.1.3.13.2.3.2 Self-Test Mode**_ 

Similar to the other self-test described for CPU / VIM Output Compare Diagnostic, the Checker CPU Inactivity Monitor can be placed in self-test mode. In self-test mode, the CCM-R5F checks the Checker CPU Inactivity Monitor itself for faults. During self-test, the compare error module output signal is deactivated. Any fault detected inside the CCM-R5F will be flagged by ESM error ESM_PLS_EVENT_8 (R5FSS0_cpu_miscompare) or ESM_PLS_EVENT_12 (R5FSS1_cpu_miscompare). If a CPU Inactivity Monitor error is asserted while selftest mode is running, the self-test error for that CPU will also be asserted. 

In self-test mode, the CCM-R5F automatically generates test patterns to look for any hardware faults. If a fault is detected, then a self-test error flag is set, a self-test error signal is asserted and sent to the ESM, and the self-test is terminated immediately. If no fault is found during self-test, the self-test complete flag is set. In both cases, the CCM-R5F Checker CPU Inactivity Monitor Diagnostic remains in self-test mode after the test has been terminated or completed, and the application needs to switch the CCM-R5F mode by writing another key to the mode key register (MKEY3). During the self-test operation, the compare error signal output to the ESM is inactive irrespective of the compare result. 

There are also two types of patterns generated by CCM-R5F during self-test mode for Check CPU Inactivity Monitor. The difference here is the number of test patterns applied during self-test. 

1. Compare Match Test 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

346 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## 2. Compare Mismatch Test 

CCM-R5F first generates Compare Match Test patterns, followed by Compare Mismatch Test patterns. 

## _**7.1.3.13.2.3.2.1 Compare Match Test**_ 

Since the comparison is done against the clamped values, and all compared signals are clamped to zero, only one test pattern is applied for the compare match test. A pattern of all-zeros are applied for the compare match test. The test will take one cycle. If the compare unit produces a compare mismatch then the self-test error flag is set, the self-test error signal is generated, and the Compare Match Test is terminated. 

## _**7.1.3.13.2.3.2.2 Compare Mismatch Test**_ 

During the Compare Mismatch Test, the number of test patterns is equal to the number of bus signals on the checker CPU to be monitored. There are a total of 6 signals being monitored on the checker CPU's level 2 interface and hence it takes 6 test patterns for the mismatch test. The mismatch test will take a total of 6 cycles to complete. An all 0's test vector is applied to the CCM-R5F’s but with one bit flipped starting from signal position 0. The un-equal vector will cause the CCM-R5F to expect a compare mismatch at signal position 0, if the CCM-R5F logic is working correctly. If, however, the CCM-R5F logic reports a compare match, the self-test error flag is set, the self-test error signal is asserted, and the Compare Mismatch Test is terminated. 

This Compare Mismatch Test algorithm repeats in a domino fashion with the next signal position flipped while forcing all other signals to logic level 0. This sequence is repeated until every inactivity monitor signal position is verified on the checker CPU . 

Table 7-17 shows the sequence of Compare Mismatch Test. There is no error signal sent to ESM if the expected errors are seen with each pattern. 

**Table 7-17. Checker CPU Inactivity Monitor Compare Mismatch Test** 

|**Signal Position**|**Signal Position**|**Signal Position**|**Signal Position**|**Signal Position**|**Signal Position**||
|---|---|---|---|---|---|---|
|**5**|**4**|**3**|**2**|**1**|**0**|**Cycle**|
|0|0|0|0|0|1|0|
|0|0|0|0|1|0|1|
|0|0|0|1|0|0|2|
|0|0|1|0|0|0|3|
|0|1|0|0|0|0|4|
|1|0|0|0|0|0|5|



## _**7.1.3.13.2.3.3 Error Forcing Mode**_ 

In error forcing mode, a test pattern of all 1's is applied to the check CPU's compare logic to force an error in the compare error output signal of the compare unit. The ESM error flag “CCM-R5F - CPU1 AXIM Bus Inactivity failure” is expected after the error forcing mode completes. As a side effect, the “CCM-R5F self-test error” flag is also asserted whenever the CPU compare error is asserted. 

The error forcing mode takes one cycle to complete. Hence, the failing signature is presented for one clock cycle. After that, the mode is automatically switched to active compare mode. The key register (MKEY3) will indicate the active compare mode once it is switched to active compare mode. During the one cycle required by the error forcing test, the checker CPU Inactivity Monitor is deactivated. User should expect the ESM to trigger a response (report the CCM-R5F fail). If no error is detected by ESM, then a hardware fault is present. 

## _**7.1.3.13.2.3.4 Self-Test Error Forcing Mode**_ 

In self-test error forcing mode, an error is forced at the self-test error signal. The compare unit is still running in active compare mode and the key is switched to active compare after one clock cycle. The ESM error flag “CCM-R5F - self-test” is expected after the self-test error forcing mode completes. Once the expected errors are seen, the application can clean the error through the ESM module. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 347 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.1.3.13.2.4 Operation During CPU Debug Mode**_ 

Certain debug operations place the CPU in a halting debug state where the code execution is halted. Because halting debug events are asynchronous, there is a possibility for the debug requests to cause loss of lockstep. CCM-R5F will disable all functional diagnostics upon detection of halting debug requests. Core compare error will not be generated and flags will not update. A CPU reset is needed to ensure the CPUs are again in lockstep and will also re-enable the CCM-R5F. 

## _**7.1.3.13.3 Control Registers**_ 

Table 7-18 lists the CCM-R5F registers. Each register begins on a 32-bit word boundary. The registers support 32-bit, 16-bit, and 8-bit accesses. The base address for the control registers is FFFF F600h. 

**Table 7-18. Control Registers** 

|**Offset**|**Acronym**|**Register Description**|**Section**|
|---|---|---|---|
|00h|CCMSR1|CCM-R5F Status Register 1|Section|
||||7.1.3.13.3.1|
|04h|CCMKEYR1|CCM-R5F Key Register 1|Section|
||||7.1.3.13.3.2|
|08h|CCMSR2|CCM-R5F Status Register 2|Section|
||||7.1.3.13.3.3|
|0Ch|CCMKEYR2|CCM-R5F Key Register 2|Section|
||||7.1.3.13.3.4|
|10h|CCMSR3|CCM-R5F Status Register 3|Section|
||||7.1.3.13.3.5|
|14h|CCMKEYR3|CCM-R5F Key Register 3|Section|
||||7.1.3.13.3.6|
|18h|CCMPOLCNTRL|Polarity Control Register|Section|
||||7.1.3.13.3.7|



## _**7.1.3.13.3.1 CCM-R5F Status Register 1 (CCMSR1)**_ 

The contents of this register should be interpreted in context of what test was selected. That is, what mode is CCM operating. 

**Figure 7-8. CCM-R5F Status Register 1 (CCMSR1) (Offset = 00h)** 

|**Figure 7-8. CCM-R5F Status Register 1 (CCMSR1) (Offset = 00h)**|**Figure 7-8. CCM-R5F Status Register 1 (CCMSR1) (Offset = 00h)**|**Figure 7-8. CCM-R5F Status Register 1 (CCMSR1) (Offset = 00h)**|**Figure 7-8. CCM-R5F Status Register 1 (CCMSR1) (Offset = 00h)**|**Figure 7-8. CCM-R5F Status Register 1 (CCMSR1) (Offset = 00h)**|**Figure 7-8. CCM-R5F Status Register 1 (CCMSR1) (Offset = 00h)**|**Figure 7-8. CCM-R5F Status Register 1 (CCMSR1) (Offset = 00h)**|**Figure 7-8. CCM-R5F Status Register 1 (CCMSR1) (Offset = 00h)**|
|---|---|---|---|---|---|---|---|
|31<br>17<br>16||||||||
|Reserved||||||CPME1||
|R-0<br>R/W1CP-0<br>15<br>9<br>8<br>7<br>2<br>1<br>0||||||||
|Reserved||||STC1|Reserved|STET1|STE1|
|R-0<br>R-0<br>R-0<br>R-0<br>R-0<br>**Table 7-19. CCM-R5F Status Register 1(CCMSR1) Field Descriptions**||||||||
|**Bit**|**Field**|**Value**|**Description**|||||
|31-17|Reserved|0|Reads return 0. Writes have no effect.|||||



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

348 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-19. CCM-R5F Status Register 1 (CCMSR1) Field Descriptions (continued)** 

|**Bit**|**Field**|**Value**|**Description**|
|---|---|---|---|
|16|CMPE1|0|Compare Error for CPU Output Compare Diagnostic.<br>**Read in User and Privileged mode. Write in Privileged mode only.**<br>Read: CPU signals are identical.<br>Write: Leaves the bit unchanged.|
|||1|Read: CPU signal compare mismatch.<br>Write: Clears the bit.|
|15-9|Reserved||Reads return 0. Writes have no effect.|
|8|STC1|0|Self-test Complete for CPU Output Compare Diagnostic.<br>**Note:**This bit is always 0 when not in self-test mode. Once set, switching from self-test mode to<br>other modes will clear this bit.<br>**Read/Write in User and Privileged mode.**<br>Read: Self-test on-going if self-test mode is entered.<br>Write: Writes have no effect.|
|||1|Read: Self-test is complete.<br>Write: Writes have no effect.|
|7-2|Reserved||Reads return 0. Writes have no effect.|
|1|STET1|0|Self-test Error Type for CPU Output Compare Diagnostic.<br>**Read/Write in User and Privileged mode.**<br>Read: Self-test failed during Compare Match Test if STE1 = 1.<br>Write: Writes have no effect.|
|||1|Read: Self-test failed during Compare Mismatch Test if STE1 = 1.<br>Write: Writes have no effect.|
|0|STE1|0|Self-test Error for CPU Output Compare Diagnostic.<br>**Note:**This bit gets updated when the self-test is complete or an error is detected.<br>**Read/Write in User and Privileged mode.**<br>Read: Self-test passed.<br>Write: Writes have no effect.|
|||1|Read: Self-test failed.<br>Write: Writes have no effect.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 349 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.1.3.13.3.2 CCM-R5F Key Register 1 (CCMKEYR1)**_ 

## **Figure 7-9. CCM-R5F Key Register 1 (CCMKEYR1) (Offset = 04h)** 

|**Figure 7-9. CCM-R5F Key Register 1 (CCMKEYR1) (Offset = 04h)**|**Figure 7-9. CCM-R5F Key Register 1 (CCMKEYR1) (Offset = 04h)**|
|---|---|
|31<br>16||
|Reserved||
|R-0<br>15<br>4<br>3<br>0||
|Reserved|MKEY1|
|R-0<br>R/WP-0||



**Table 7-20. CCM-R5F Key Register 1 (CCMKEYR1) Field Descriptions** 

|**Bit**|**Field**|**Value**|**Description**|
|---|---|---|---|
|31-4|Reserved|0|Reads return 0. Writes have no effect.|
|3-0|MKEY1|0|Mode Key to select operation for CPU Output Compare Diagnostic .<br>**Read in User and Privileged mode. Write in Privileged mode only.**<br>Read: Returns current value of the MKEY1.<br>Write: Active Compare Lockstep mode.|
|||6h|Read: Returns current value of the MKEY1.<br>Write: Self-test mode.|
|||9h|Read: Returns current value of the MKEY1.<br>Write: Error Forcing mode.|
|||Fh|Read: Returns current value of the MKEY1.<br>Write: Self-test Error Forcing mode.|
|||Other values|**Note:**It is recommended to not write any other key combinations. Invalid keys will result in<br>switching operation to lockstep mode.|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

350 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.1.3.13.3.3 CCM-R5F Status Register 2 (CCMSR2)**_ 

## **Figure 7-10. CCM-R5F Status Register 2 (CCMSR2) (Offset = 08h)** 

|**Figure 7-10. CCM-R5F Status Register 2 (CCMSR2) (Offset = 08h)**|**Figure 7-10. CCM-R5F Status Register 2 (CCMSR2) (Offset = 08h)**|**Figure 7-10. CCM-R5F Status Register 2 (CCMSR2) (Offset = 08h)**|**Figure 7-10. CCM-R5F Status Register 2 (CCMSR2) (Offset = 08h)**|**Figure 7-10. CCM-R5F Status Register 2 (CCMSR2) (Offset = 08h)**|**Figure 7-10. CCM-R5F Status Register 2 (CCMSR2) (Offset = 08h)**|**Figure 7-10. CCM-R5F Status Register 2 (CCMSR2) (Offset = 08h)**|**Figure 7-10. CCM-R5F Status Register 2 (CCMSR2) (Offset = 08h)**|
|---|---|---|---|---|---|---|---|
|31<br>17<br>16||||||||
|Reserved||||||CPME2||
|R-0<br>R/W1CP-0<br>15<br>9<br>8<br>7<br>2<br>1<br>0||||||||
|Reserved||||STC2|Reserved|STET2|STE2|
|R-0<br>R-0<br>R-0<br>R-0<br>R-0<br>**Table 7-21. CCM-R5F Status Register 2(CCMSR2) Field Descriptions**||||||||
|**Bit**|**Field**|**Value**|**Description**|||||
|31-17|Reserved|0|Reads return 0. Writes have no effect.|||||
|16|CMPE2|0|Compare Error for VIM Output Compare Diagnostic.<br>**Read in User and Privileged mode. Write in Privileged mode only.**<br>Read: CPU signals are identical.<br>Write: Leaves the bit unchanged.|||||
|||1|Read: CPU signal compare mismatch.<br>Write: Clears the bit.|||||
|15-9|Reserved||Reads return 0. Writes have no effect.|||||
|8|STC2|0|Self-test Complete for VIM Output Compare Diagnostic.<br>**Note:**This bit is always 0 when not in self-test mode. Once set, switching from self-test mode to<br>other modes will clear this bit.<br>**Read/Write in User and Privileged mode.**<br>Read: Self-test on-going if self-test mode is entered.<br>Write: Writes have no effect.|||||
|||1|Read: Self-test is complete.<br>Write: Writes have no effect.|||||
|7-2|Reserved||Reads return 0. Writes have no effect.|||||
|1|STET2|0|Self-test Error Type for VIM Output Compare Diagnostic.<br>**Read/Write in User and Privileged mode.**<br>Read: Self-test failed during Compare Match Test if STE2 = 1.<br>Write: Writes have no effect.|||||
|||1|Read: Self-test failed during Compare Mismatch Test if STE2 = 1.<br>Write: Writes have no effect.|||||
|0|STE2|0|Self-test Error for VIM Output Compare Diagnostic.<br>**Note:**This bit gets updated when the self-test is complete or an error is detected.<br>**Read/Write in User and Privileged mode.**<br>Read: Self-test passed.<br>Write: Writes have no effect.|||||
|||1|Read: Self-test failed.<br>Write: Writes have no effect.|||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 351 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.1.3.13.3.4 CCM-R5F Key Register 2 (CCMKEYR2)**_ 

## **Figure 7-11. CCM-R5F Key Register 2 (CCMKEYR2) (Offset = 0Ch)** 

|**Figure 7-11. CCM-R5F Key Register 2 (CCMKEYR2) (Offset = 0Ch)**|**Figure 7-11. CCM-R5F Key Register 2 (CCMKEYR2) (Offset = 0Ch)**|
|---|---|
|31<br>16||
|Reserved||
|R-0<br>15<br>4<br>3<br>0||
|Reserved|MKEY2|
|R-0<br>R/WP-0||



**Table 7-22. CCM-R5F Key Register 2 (CCMKEYR2) Field Descriptions** 

|**Bit**|**Field**|**Value**|**Description**|
|---|---|---|---|
|31-4|Reserved|0|Reads return 0. Writes have no effect.|
|3-0|MKEY2|0|Mode Key to select operation for VIM Output Compare Diagnostic.<br>**Read in User and Privileged mode. Write in Privileged mode only.**<br>Read: Returns current value of the MKEY2.<br>Write: Active Compare Lockstep mode.|
|||6h|Read: Returns current value of the MKEY2.<br>Write: Self-test mode.|
|||9h|Read: Returns current value of the MKEY2.<br>Write: Error Forcing mode.|
|||Fh|Read: Returns current value of the MKEY2.<br>Write: Self-test Error Forcing mode.|
|||Other values|**Note:**It is recommended to not write any other key combinations. Invalid keys will result in<br>switching operation to lockstep mode.|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

352 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.1.3.13.3.5 CCM-R5F Status Register 3 (CCMSR3)**_ 

## **Figure 7-12. CCM-R5F Status Register 3 (CCMSR3) (Offset = 10h)** 

|**Figure 7-12. CCM-R5F Status Register 3 (CCMSR3) (Offset = 10h)**|**Figure 7-12. CCM-R5F Status Register 3 (CCMSR3) (Offset = 10h)**|**Figure 7-12. CCM-R5F Status Register 3 (CCMSR3) (Offset = 10h)**|**Figure 7-12. CCM-R5F Status Register 3 (CCMSR3) (Offset = 10h)**|**Figure 7-12. CCM-R5F Status Register 3 (CCMSR3) (Offset = 10h)**|**Figure 7-12. CCM-R5F Status Register 3 (CCMSR3) (Offset = 10h)**|**Figure 7-12. CCM-R5F Status Register 3 (CCMSR3) (Offset = 10h)**|**Figure 7-12. CCM-R5F Status Register 3 (CCMSR3) (Offset = 10h)**|
|---|---|---|---|---|---|---|---|
|31<br>17<br>16||||||||
|Reserved||||||CPME3||
|R-0<br>R/W1CP-0<br>15<br>9<br>8<br>7<br>2<br>1<br>0||||||||
|Reserved||||STC3|Reserved|STET3|STE3|
|R-0<br>R-0<br>R-0<br>R-0<br>R-0<br>**Table 7-23. CCM-R5F Status Register 3(CCMSR3) Field Descriptions**||||||||
|**Bit**|**Field**|**Value**|**Description**|||||
|31-17|Reserved|0|Reads return 0. Writes have no effect.|||||
|16|CMPE3|0|Compare Error for Checker CPU Inactivity Monitor.<br>**Read in User and Privileged mode. Write in Privileged mode only.**<br>Read: CPU signals are identical.<br>Write: Leaves the bit unchanged.|||||
|||1|Read: CPU signal compare mismatch.<br>Write: Clears the bit.|||||
|15-9|Reserved||Reads return 0. Writes have no effect.|||||
|8|STC3|0|Self-test Complete for Checker CPU Inactivity Monitor.<br>**Note:**This bit is always 0 when not in self-test mode. Once set, switching from self-test mode to<br>other modes will clear this bit.<br>**Read/Write in User and Privileged mode.**<br>Read: Self-test on-going if self-test mode is entered.<br>Write: Writes have no effect.|||||
|||1|Read: Self-test is complete.<br>Write: Writes have no effect.|||||
|7-2|Reserved||Reads return 0. Writes have no effect.|||||
|1|STET3|0|Self-test Error Type for Checker CPU Inactivity Monitor.<br>**Read/Write in User and Privileged mode.**<br>Read: Self-test failed during Compare Match Test if STE3 = 1.<br>Write: Writes have no effect.|||||
|||1|Read: Self-test failed during Compare Mismatch Test if STE3 = 1.<br>Write: Writes have no effect.|||||
|0|STE3|0|Self-test Error for Checker CPU Inactivity Monitor.<br>**Note:**This bit gets updated when the self-test is complete or an error is detected.<br>**Read/Write in User and Privileged mode.**<br>Read: Self-test passed.<br>Write: Writes have no effect.|||||
|||1|Read: Self-test failed.<br>Write: Writes have no effect.|||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 353 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.1.3.13.3.6 CCM-R5F Key Register 3 (CCMKEYR3)**_ 

## **Figure 7-13. CCM-R5F Key Register 3 (CCMKEYR3) (Offset = 14h)** 

|31<br>16|31<br>16|
|---|---|
|Reserved||
|R-0<br>15<br>4<br>3<br>0||
|Reserved|MKEY3|
|R-0<br>R/WP-0||



**Table 7-24. CCM-R5F Key Register 3 (CCMKEYR3) Field Descriptions** 

|**Bit**|**Field**|**Value**|**Description**|
|---|---|---|---|
|31-4|Reserved|0|Reads return 0. Writes have no effect.|
|3-0|MKEY3|0|Mode Key to select operation for Checker CPU Inactivity Monitor.<br>**Read in User and Privileged mode. Write in Privileged mode only.**<br>Read: Returns current value of the MKEY3.<br>Write: Active Compare Lockstep mode.|
|||6h|Read: Returns current value of the MKEY3.<br>Write: Self-test mode.|
|||9h|Read: Returns current value of the MKEY3.<br>Write: Error Forcing mode.|
|||Fh|Read: Returns current value of the MKEY3.<br>Write: Self-test Error Forcing mode.|
|||Other values|**Note:**It is recommended to not write any other key combinations. Invalid keys will result in<br>switching operation to lockstep mode.|



## _**7.1.3.13.3.7 CCM-R5F Polarity Control Register (CCMPOLCNTRL)**_ 

## **Figure 7-14. CCM-R5F Polarity Control Register (CCMPOLCNTRL) (Offset = 18h)** 

**==> picture [500 x 133] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 16<br>Reserved<br>R-0<br>15 8 7 0<br>Reserved POLARITYINVERT<br>R-0 R/WP-0<br>**----- End of picture text -----**<br>


**Table 7-25. CCM-R5F Polarity Control Register (CCMPOLCNTRL) Field Descriptions** 

|**Bit**|**Field**|**Value**|**Description**|
|---|---|---|---|
|31-8|Reserved|0|Reads return 0. Writes have no effect.|



354 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

