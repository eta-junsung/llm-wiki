<!-- AM263P TRM | 7.3 PRU-ICSS | 원본 p.365-505 | pymupdf4llm text+tables, images omitted -->

www.ti.com 

_Processors and Accelerators_ 

## **7.3 Programmable Real-Time Unit Subsystem (PRU-ICSS)** 

This section describes the Programmable Real-Time Unit Subsystem in the device. 

## **Note** 

The supported set of features and peripherals is device part number dependent. For more information, see the device data sheet. 

## **Note** 

The PRU Subsystem is a subset of the PRU Industrial Communication Subsystem (PRU-ICSS) found on other TI processors. The superset names "PRU-ICSS", "PRUSS", and "ICSSM" are used in some parts of the TRM to refer to the PRU Subsystem. 

**7.3.1 PRU-ICSS Overview** ...........................................................................................................................................366 **7.3.2 PRU-ICSS Environment** .....................................................................................................................................368 **7.3.3 PRU-ICSS Integration** ........................................................................................................................................ 374 **7.3.4 PRU-ICSS Top Level Resources Functional Description** ............................................................................... 375 **7.3.5 PRU-ICSS PRU Cores** ........................................................................................................................................ 380 **7.3.6 PRU-ICSS Broadside Accelerators** ...................................................................................................................411 **7.3.7 PRU-ICSS Local INTC** ........................................................................................................................................ 423 **7.3.8 PRU-ICSS UART Module** ................................................................................................................................... 430 **7.3.9 PRU-ICSS ECAP Module** ................................................................................................................................... 444 **7.3.10 PRU-ICSS MII_RT Module** ................................................................................................................................466 **7.3.11 PRU-ICSS MII MDIO Module** ............................................................................................................................ 490 **7.3.12 PRU-ICSS IEP** ................................................................................................................................................... 497 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 365 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.1 PRU-ICSS Overview**_ 

The Programmable Real-Time Unit Subsystem (PRU-ICSS) consists of: 

- Two 32-bit load/store RISC CPU cores - Programmable Real-Time Units (PRU0 and PRU1) 

- Data RAMs per PRU core (DRAM[0:1]) 

- Instruction RAM per PRU core (IRAM[0]) 

- Shared RAM (SMEM/DRAM[2]) 

- Peripheral modules: UART, ECAP, IEP, MDIO 

- Interrupt Controller (INTC) per core 

The programmable nature of the PRU cores, along with their access to pins, events and all device resources, provides flexibility in implementing fast real-time responses, specialized data handling operations, custom peripheral interfaces, and in offloading tasks from the other processor cores of the device. 

The PRU cores are programmed with a small, deterministic instruction set. Each PRU can operate independently or in coordination with each other and can also work in coordination with the device-level host CPU. This interaction between processors is determined by the nature of the firmware loaded into the PRU’s instruction memory. 

**==> picture [489 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
36-bit CBA Target MMR/<br>CFG<br>PRU-ICSS<br>CBA32 Shared Resources<br>PRU0/PRU1<br>EGPIO / SCU<br>Pins 3-Ch. PERIF Module DRAM08KB DRAM18KB Shared RAMDRAM2 Pins<br>SD Demodulation 32KB<br>EGPI/EGPO PRU<br>12KB IRAM<br>36-bit CBA RAT<br>Broadside Shared Resources<br>MAC<br>PRU SPAD<br>Off- CRC16/32 Bank0 Bank1 Bank2<br>Device  MII_RT \ Port 30, 32-bit 30, 32-bit  30, 32-bit<br>PHY Registers Registers Registers<br>INTC<br>IEP<br>MDIO<br>eCAP<br>UART<br>RX RX<br>XFR2VBUS  XFR2VBUS<br>**----- End of picture text -----**<br>


**Figure 7-19. PRU-ICSS Overview** 

## **7.3.1.1 PRU-ICSS Key Features** 

The PRU-ICSS subsystem includes the following main features: 

- Two 32-bit load/store RISC CPU cores — Programmable Real-Time Units (PRU0 and PRU1), each with: 

   - 20 Enhanced General-Purpose Inputs (EGPI) and 20 Enhanced General-Purpose Outputs (EGPO) 

   - Asynchronous capture [Serial Capture Unit (SCU)] with 3-channel peripheral interface and Sigma-Delta demodulation support 

      - The 3-channel peripheral interface supports multiple different encoder protocols such as EnDAT 2.2, HDSL, and Tamagawa. 

   - 12KB program memory per PRU (PRU0_IRAM and PRU1_IRAM) with ECC 

   - MAC (Multiplier with optional Accumulation) 

   - CRC16/CRC32 hardware accelerator 

   - Broadside (32 Byte) connection to MII_RTn (where n = 1 or 2) 

   - RX XFR2VBUS 

- Scratchpad Memory (SPAD) with 3 banks of 30 × 32-bit registers: 

   - 3 banks shared between the PRU0 and PRU1 cores 

- 32 KB Shared general purpose memory RAM with ECC (SRAM/DRAM2), shared between PRU0 and PRU1 

- Two 8 KB (shared) Data Memories with ECC (DRAM0 and DRAM1) 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

366 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- 36-bit VBUSM Controller Port: 

   - Optional address translation for all transactions to External Host 

- 16 Software Events generated by 2 PRUs 

- Two Real-Time Ethernet ports (MII_RT1 and MII_RT2) configurable to connect to each PRUn (where n = 0 or 1) to support multiple industrial communication protocols 

- One Industrial Ethernet Peripheral (IEP0) to manage/generate Industrial Ethernet functions such as time stamping 

   - Industrial Ethernet 64-bit timers support 10 capture and 16 compare events along with slow and fast compensation 

- One MDIO port to control external Ethernet PHY 

- One Enhanced Capture Module (ECAP0) 

- Interrupt Controller (INTC) 

   - Up to 32 internal events, generated by modules, internal to the PRU-ICSS 

   - Up to 32 external events, generated by the system 

   - Supports up to 10 interrupt channels 

   - Generation of up to 10 Host interrupts: 

      - Up to 2 Host interrupts, exported from the PRU-ICSS for signaling the Arm interrupt controllers (pulse and level provided) 

   - Each system event can be enabled and disabled 

   - Each host event can be enabled and disabled 

   - Hardware prioritization of events 

- One 32-bit VBUSP target port for memory mapped register and internal memories access 

- Flexible power management support 

- Integrated 32-bit Interconnect 

## **7.3.1.2 Not Supported Features** 

The following PRU-ICSS features are not supported: 

- Industrial Communications Subsystem features 

   - Low power clock enable suport 

   - The following GPIO and mux modes are not pinned out: 

      - PR0_PRU0_GPIO7 

         - PR0_PRU0_PERIF2_OUT 

         - PR0_PRU0_SD3_D 

      - PR0_PRU0_GPIO17 

         - PR0_PRU0_SD8_D 

      - PR0_PRU0_GPIO18 

      - PR0_PRU0_GPIO19 

   - SD mode on PRU1 

   - Integrated PWM module 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

367 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.2 PRU-ICSS Environment**_ 

This section describes the PRU-ICSS external connections (environment). 

## **7.3.2.1 PRU-ICSS Internal Pinmux** 

The PRU-ICSS external interface signals are described in Table 7-31. The PRU-ICSS has a large number of available I/O signals. Most of these are multiplexed with other functional signals at the device level. 

The PRU-ICSS also support an internal wrapper multiplexing that expands the device top-level multiplexing. This wrapper multiplexing is controlled by the GPCFGx_REG register (where x = 0 or 1) in the PRU-ICSS CFG register space and allows MII_RT, 3 channel Peripheral Interface (with EnDAT capabilities), and Sigma Delta functionality to be muxed with the PRU GPI/O device signals, as shown in Figure 7-20. The PRU-ICSS wrapper multiplexing is described with the device-level signals in Table 7-31. Note that the device top-level muxing has higher priority over the internal PRU-ICSS muxing. 

**==> picture [326 x 166] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU-ICSS<br>GPIO mode (0)<br>Peripheral IF mode (1)<br>PR0_PRU<n>_GPI/O<br>MII mode (2)<br>SD mode (3)<br>Reserved (4)<br>ICSS_GPCFG0/1<br>[PR0_PRU<n>_GP_MUX_SEL]<br>**----- End of picture text -----**<br>


1. n represents a valid instance of PRU in a domain. 

**Figure 7-20. PRU-ICSS Internal Wrapper Multiplexing** 

## **Note** 

Additionally to PRU-ICSS wrapper multiplexing the device I/O logic maps the PRU-ICSS signals to the different device pins by programming the associated IOMUX CTRLMMR register. 

368 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 500] intentionally omitted <==**

**Figure 7-21. PRU-ICSS External Interface I/Os** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 369 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**PRU-ICSS I/O Signals**_ 

## Table 7-31 describes the PRU-ICSS<k> I/O signals. 

## **Note** 

<k> is the number of PRU-ICSS in the device. See the Data sheet for additional details. 

## **Table 7-31. PRU-ICSS I/O Signals** 

|**Device Level Signal**|**Alternate Function via Internal Multiplexing**<br>**I/O**(1)<br>**Description**<br>**Pin Reset**<br>(2)|**Alternate Function via Internal Multiplexing**<br>**I/O**(1)<br>**Description**<br>**Pin Reset**<br>(2)|
|---|---|---|
||ICSS_GPCFG0_REG[29-26] PR<k>_PRU0_GP_MUX_SEL=||
|PRU0 GP Signals|0h - GPIO mode (default)<br>1h - PERIF mode<br>2h - MII mode<br>3h - SD mode||
|PR<k>_PRU0_GPO0|pr<k>_pru0_pru_r30_out[0]<br>pr<k>_pru0_perif0_clk<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO1|pr<k>_pru0_pru_r30_out[1]<br>pr<k>_pru0_perif0_out<br>pr<k>_pru0_pru_r30_out[1]<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO2|pr<k>_pru0_pru_r30_out[2]<br>pr<k>_pru0_perif0_out_en<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO3|pr<k>_pru0_pru_r30_out[3]<br>pr<k>_pru0_perif1_clk<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO4|pr<k>_pru0_pru_r30_out[4]<br>pr<k>_pru0_perif1_out<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO5|pr<k>_pru0_pru_r30_out[5]<br>pr<k>_pru0_perif1_out_en<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO6|pr<k>_pru0_pru_r30_out[6]<br>pr<k>_pru0_perif2_clk<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO7(5)|pr<k>_pru0_pru_r30_out[7](5)<br>pr<k>_pru0_perif2_out(5)<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO8|pr<k>_pru0_pru_r30_out[8]<br>pr<k>_pru0_perif2_out_en<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO9|pr<k>_pru0_pru_r30_out[9]<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO10|pr<k>_pru0_pru_r30_out[10]<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO11|pr<k>_pru0_pru_r30_out[11]<br>pr<k>_mii1_txd[0](3)<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO12|pr<k>_pru0_pru_r30_out[12]<br>pr<k>_mii1_txd[1](3)<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO13|pr<k>_pru0_pru_r30_out[13]<br>pr<k>_mii1_txd[2](3)<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO14|pr<k>_pru0_pru_r30_out[14]<br>pr<k>_mii1_txd[3](3)<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO15|pr<k>_pru0_pru_r30_out[15]<br>pr<k>_mii1_txen(3)<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO16|pr<k>_pru0_pru_r30_out[16]<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO17(5)|pr<k>_pru0_pru_r30_out[17](5)<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO18(5)|pr<k>_pru0_pru_r30_out[18](5)<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPO19(5)|pr<k>_pru0_pru_r30_out[19](5)<br>O<br>PRU0 R30 Outputs<br>0||
|PR<k>_PRU0_GPI0|pr<k>_pru0_pru_r31_in[0]<br>pr<k>_mii0_rxd[0]<br>pr<k>_pru0_sd0_clk<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI1|pr<k>_pru0_pru_r31_in[1]<br>pr<k>_mii0_rxd[1]<br>pr<k>_pru0_sd0_d<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI2|pr<k>_pru0_pru_r31_in[2]<br>pr<k>_mii0_rxd[2]<br>pr<k>_pru0_sd1_clk<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI3|pr<k>_pru0_pru_r31_in[3]<br>pr<k>_mii0_rxd[3]<br>pr<k>_pru0_sd1_d<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI4|pr<k>_pru0_pru_r31_in[4]<br>pr<k>_mii0_rxdv<br>pr<k>_pru0_sd2_clk<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI5|pr<k>_pru0_pru_r31_in[5]<br>pr<k>_mii0_rxer<br>pr<k>_pru0_sd2_d<br>I<br>PRU0 R31 Inputs<br>HiZ||



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

370 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-31. PRU-ICSS I/O Signals (continued)** 

|**Device Level Signal**|**Alternate Function via Internal Multiplexing**<br>**I/O**(1)<br>**Description**<br>**Pin Reset**<br>(2)|**Alternate Function via Internal Multiplexing**<br>**I/O**(1)<br>**Description**<br>**Pin Reset**<br>(2)|
|---|---|---|
|PR<k>_PRU0_GPI6|pr<k>_pru0_pru_r31_in[6]<br>pr<k>_mii_mr0_clk<br>pr<k>_pru0_sd3_clk<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI7(5)|pr<k>_pru0_pru_r31_in[7](5)<br>pr<k>_pru0_sd3_d(5)<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI8|pr<k>_pru0_pru_r31_in[8]<br>pr<k>_mii0_rxlink<br>pr<k>_pru0_sd4_clk<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI9|pr<k>_pru0_pru_r31_in[9]<br>pr<k>_pru0_perif0_in<br>pr<k>_mii0_col<br>pr<k>_pru0_sd4_d<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI10|pr<k>_pru0_pru_r31_in[10]<br>pr<k>_pru0_perif1_in<br>pr<k>_mii0_crs<br>pr<k>_pru0_sd5_clk<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI11|pr<k>_pru0_pru_r31_in[11]<br>pr<k>_pru0_perif2_in<br>pr<k>_pru0_sd5_d<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI12|pr<k>_pru0_pru_r31_in[12]<br>pr<k>_pru0_sd6_clk<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI13|pr<k>_pru0_pru_r31_in[13]<br>pr<k>_pru0_sd6_d<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI14|pr<k>_pru0_pru_r31_in[14]<br>pr<k>_pru0_sd7_clk<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI15|pr<k>_pru0_pru_r31_in[15]<br>pr<k>_pru0_sd7_d<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI16|pr<k>_pru0_pru_r31_in[16]<br>pr<k>_pru0_pru_r31_in[16]<br>pr<k>_mii_mt1_clk,<br>pr<k>_pru0_pru_r31_in[16]<br>pr<k>_pru0_sd8_clk,<br>pr<k>_pru0_pru_r31_in[16]<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI17(5)|pr<k>_pru0_pru_r31_in[17](5)<br>pr<k>_pru0_sd8_d(5)<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI18(5)|pr<k>_pru0_pru_r31_in[18](5)<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PR<k>_PRU0_GPI19(5)|pr<k>_pru0_pru_r31_in[19](5)<br>I<br>PRU0 R31 Inputs<br>HiZ||
|PRU1 GP Signals|ICSS_GPCFG1_REG[29-26] PR0_PRU1_GP_MUX_SEL=||
||0h - GPIO mode (default)<br>1h - PERIF mode<br>2h - MII mode<br>3h - SD mode(4)||
|PR<k>_PRU1_GPO0|pr<k>_pru1_pru_r30_out[0]<br>pr<k>_pru1_perif0_clk<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO1|pr<k>_pru1_pru_r30_out[1]<br>pr<k>_pru1_perif0_out<br>pr<k>_pru1_pru_r30_out[1]<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO2|pr<k>_pru1_pru_r30_out[2]<br>pr<k>_pru1_perif0_out_en<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO3|pr<k>_pru1_pru_r30_out[3]<br>pr<k>_pru1_perif1_clk<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO4|pr<k>_pru1_pru_r30_out[4]<br>pr<k>_pru1_perif1_out<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO5|pr<k>_pru1_pru_r30_out[5]<br>pr<k>_pru1_perif1_out_en<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO6|pr<k>_pru1_pru_r30_out[6]<br>pr<k>_pru1_perif2_clk<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO7|pr<k>_pru1_pru_r30_out[7]<br>pr<k>_pru1_perif2_out<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO8|pr<k>_pru1_pru_r30_out[8]<br>pr<k>_pru1_perif2_out_en<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO9|pr<k>_pru1_pru_r30_out[9]<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO10|pr<k>_pru1_pru_r30_out[10]<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO11|pr<k>_pru1_pru_r30_out[11]<br>pr<k>_mii0_txd[0](3)<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO12|pr<k>_pru1_pru_r30_out[12]<br>pr<k>_mii0_txd[1](3)<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO13|pr<k>_pru1_pru_r30_out[13]<br>pr<k>_mii0_txd[2](3)<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO14|pr<k>_pru1_pru_r30_out[14]<br>pr<k>_mii0_txd[3](3)<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO15|pr<k>_pru1_pru_r30_out[15]<br>pr<k>_mii0_txen(3)<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO16|pr<k>_pru1_pru_r30_out[16]<br>O<br>PRU1 R30 Outputs<br>0||
|PR<k>_PRU1_GPO17|pr<k>_pru1_pru_r30_out[17]<br>O<br>PRU1 R30 Outputs<br>0||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 371 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-31. PRU-ICSS I/O Signals (continued)** 

|**Device Level Signal**||**Alternate Function via**|**Internal Multiplexing**||**I/O**(1)||**Description**|**Pin Reset**|
|---|---|---|---|---|---|---|---|---|
|||||||||(2)|
|PR<k>_PRU1_GPO18|pr<k>_pru1_pru_r30_out[18]||||O|PRU1|R30 Outputs|0|
|PR<k>_PRU1_GPO19|pr<k>_pru1_pru_r30_out[19]||||O|PRU1|R30 Outputs|0|
|PR<k>_PRU1_GPI0|pr<k>_pru1_pru_r31_in[0]||pr<k>_mii1_rxd[0]|pr<k>_pru1_sd0_clk(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI1|pr<k>_pru1_pru_r31_in[1]||pr<k>_mii1_rxd[1]|pr<k>_pru1_sd0_d(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI2|pr<k>_pru1_pru_r31_in[2]||pr<k>_mii1_rxd[2]|pr<k>_pru1_sd1_clk(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI3|pr<k>_pru1_pru_r31_in[3]||pr<k>_mii1_rxd[3]|pr<k>_pru1_sd1_d(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI4|pr<k>_pru1_pru_r31_in[4]||pr<k>_mii1_rxdv|pr<k>_pru1_sd2_clk(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI5|pr<k>_pru1_pru_r31_in[5]||pr<k>_mii1_rxer|pr<k>_pru1_sd2_d(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI6|pr<k>_pru1_pru_r31_in[6]||pr<k>_mii_mr1_clk|pr<k>_pru1_sd3_clk(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI7|pr<k>_pru1_pru_r31_in[7]|||pr<k>_pru1_sd3_d(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI8|pr<k>_pru1_pru_r31_in[8]||pr<k>_mii1_rxlink|pr<k>_pru1_sd4_clk(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI9|pr<k>_pru1_pru_r31_in[9]|pr<k>_pru1_perif0_in|pr<k>_mii1_col|pr<k>_pru1_sd4_d(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI10|pr<k>_pru1_pru_r31_in[10]|pr<k>_pru1_perif1_in|pr<k>_mii1_crs|pr<k>_pru1_sd5_clk(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI11|pr<k>_pru1_pru_r31_in[11]|pr<k>_pru1_perif2_in||pr<k>_pru1_sd5_d(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI12|pr<k>_pru1_pru_r31_in[12]|||pr<k>_pru1_sd6_clk(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI13|pr<k>_pru1_pru_r31_in[13]|||pr<k>_pru1_sd6_d(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI14|pr<k>_pru1_pru_r31_in[14]|||pr<k>_pru1_sd7_clk(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI15|pr<k>_pru1_pru_r31_in[15]|||pr<k>_pru1_sd7_d(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI16|pr<k>_pru1_pru_r31_in[16]|pr<k>_pru1_pru_r31_in[16]|pr<k>_mii_mt0_clk,|pr<k>_pru1_sd8_clk,|I|PRU1|R31 Inputs|HiZ|
||||pr<k>_pru1_pru_r31_in[16]|pr<k>_pru1_pru_r31_in[16](4)|||||
|PR<k>_PRU1_GPI17|pr<k>_pru1_pru_r31_in[17]|||pr<k>_pru1_sd8_d(4)|I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI18|pr<k>_pru1_pru_r31_in[18]||||I|PRU1|R31 Inputs|HiZ|
|PR<k>_PRU1_GPI19|pr<k>_pru1_pru_r31_in[19]||||I|PRU1|R31 Inputs|HiZ|
|MDIO|MDIO||||||||
|PR<k>_MDIO0_MDC|pr<k>_mdio_mdclk||||O|MDIO|Clock|0|
|PR<k>_MDIO0_MDIO|pr<k>_mdio_data||||I/O|MDIO|Data|HiZ|
|Industrial Ethernet (IEP0)|Industrial Ethernet||||||||
|PR<k>_IEP0_EDIO_OUTVALID|pr<k>_iep0_edio_outvalid||||O|IEP0 Digital I/O Output||0|
|||||||Valid|||
|PR<k>_IEP0_EDIO_DATA_IN_O|pr<k>_iep0_edio_data_in_out[31:||||I/O|IEP0 Digital I/Os Data||HiZ|
|UT[31:30]|30]|||||In/Out|||
|PR<k>_IEP0_EDC_SYNC_OUT0|pr<k>_iep0_edc_sync_out0||||O|IEP0 Distributed Clock||0|
|||||||Sync Out|||
|PR<k>_IEP0_EDC_SYNC_OUT1|pr<k>_iep0_edc_sync_out1||||O|IEP0 Distributed Clock||0|
|||||||Sync Out|||
|PR<k>_IEP0_EDC_LATCH_IN0|pr<k>_iep0_edc_latch_in0||||I|IEP0 Distributed Clock||HiZ|
|||||||Latch In|||



372 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **Table 7-31. PRU-ICSS I/O Signals (continued)** 

|**Device Level Signal**||**Alternate Function via Internal Multiplexing**|**I/O**(1)|**Description**|**Pin Reset**|
|---|---|---|---|---|---|
||||||(2)|
|PR<k>_IEP0_EDC_LATCH_IN1|pr<k>_iep0_edc_latch_in1||I|IEP0 Distributed Clock|HiZ|
|||||Latch In||
|UART0|UART0|||||
|PR<k>_UART0_CTSn|pr<k>_uart0_cts_n||I|UART0 Clear to Send|HiZ|
|PR<k>_UART0_RTSn|pr<k>_uart0_rts_n||O|UART0 Request to Send|1|
|PR<k>_UART0_RXD|pr<k>_uart0_rxd||I|UART0 Receive Data|HiZ|
|PR<k>_UART0_TXD|pr<k>_uart0_txd||O|UART0 Transmit Data|1|
|ECAP0|ECAP0|||||
|PR<k>_ECAP0_IN_APWM_OUT|pr<k>_ecap0_ecap_capin_apwm||I/O|Enhanced capture|HiZ|
||_o|||(ECAP0) input or||
|||||Auxiliary PWM out||
|PR<k>_ECAP0_SYNC_IN|pr<k>_ecap0_ecap_syncin||I|Enhanced capture|0|
|||||(ECAP0) Sync In||
|PR<k>_ECAP0_SYNC_OUT|pr<k>_ecap0_ecap_syncout||O|Enhanced capture|0|
|||||(ECAP0) Sync Out||



(1) I = Input; O = Output 

(2) HiZ = High Impedance 

(3) The PRU internal pinmux mapping provided in the TRM is part of the original hardware definition of the PRU. However, due to the flexibility provided by the IP and associated firmware configurations, this is not necessarily a hard requirement. The first PRU implementation had the MII TX pins swapped during initial SoC integration and this convention was maintained for subsequent PRU revisions to enable firmware reuse. To make use of the SDK firmware, use the SYSCONFIG generated PRU pin mapping. 

(4) SD Mode is not supported on PRU1 

(5) The following IO are not pinned out at the device level and therefore not supported. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 373 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.3 PRU-ICSS Integration**_ 

This section describes modules integration in the device, including information about clocks, resets, and hardware requests. 

374 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.4 PRU-ICSS Top Level Resources Functional Description**_ 

This section provides functional description of the device integrated PRU Subsystems modules. 

The PRUn (where n = 0 or 1) cores within each PRU-ICSS have access to all resources on the SoC through the VBUSM Interface Controller port, and the external host processors can access the PRU-ICSS resources through the VBUSP Interface Target port. The use of XFR2VBUS allows BroadSide 32Bytes of data transfer to/ from SoC CBASS0 Interconnect at 256-bit bursts using the VBUSM Controller port. The 32-bit Internal CBASS Interconnect bus will be the primary interconnect between all components internal to the PRU-ICSS. There are two equally symmetrical halves in each PRU-ICSS known as SLICE0 and SLICE1. Each slice will share several resources while capable of working independently of each other. There are two sets of XFR2VBUS for each Slice. PRUs also has the ability to submit 32-bit bursts transitions, but this will require RAT configuration. 

Each of the Slices contains one RAT (Region based Address Translation) module. The RAT module is used to translate 32-bit address of the PRU core to 48-bit physical address. 

The PRU cores within the subsystems also have access to all resources on the SoC through the External CBASS0 Interconnect. A subsystem local Interrupt Controller — INTC handles system input events and posts events back to the device-level host CPUs. 

Figure 7-22 shows an overview of the PRU-ICSS Functional Block Diagram. 

**==> picture [489 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
36-bit CBA Target MMR/<br>CFG<br>PRU-ICSS<br>CBA32 Shared Resources<br>PRU0/PRU1<br>EGPIO / SCU<br>Pins 3-Ch. PERIF Module DRAM08KB DRAM18KB Shared RAMDRAM2 Pins<br>SD Demodulation 32KB<br>EGPI/EGPO PRU<br>12KB IRAM<br>36-bit CBA RAT<br>Broadside Shared Resources<br>MAC<br>PRU SPAD<br>Off- CRC16/32 Bank0 Bank1 Bank2<br>Device  MII_RT \ Port 30, 32-bit 30, 32-bit  30, 32-bit<br>PHY Registers Registers Registers<br>INTC<br>IEP<br>MDIO<br>eCAP<br>UART<br>RX RX<br>XFR2VBUS  XFR2VBUS<br>**----- End of picture text -----**<br>


**Figure 7-22. PRU-ICSS Functional Block Diagram** 

Table 7-32 summarizes the mapping between hardware modules and ICSS<k> PRU0/1 cores, where <k> is the number of ICSS modules in the device. 

**Table 7-32. Hardware Module Broadside ID Mapping** 

|**Hardware Module**|**Broadside ID**||
|---|---|---|
|MPY/MAC|00|2 copies:<br>PRU1/0|
|CRC16/32|01|2 copies:<br>PRU1/0|
|SPAD Bank0|10|shared between PRU1/0|
|SPAD Bank1|11|shared between PRU1/0|
|SPAD Bank2|12|shared between PRU1/0|
|RX L2|20/21|2 copies:<br>PRU1/0|
|TX L2|40|2 copies:<br>PRU1/0|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 375 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-32. Hardware Module Broadside ID Mapping (continued)** 

|**Hardware Module**|**Broadside ID**||
|---|---|---|
|XFR2VBUSP|0x60 for RD_ID0<br>0x61 for RD_ID1<br>0x62 for WD_ID0<br>0x63 for WD_ID1|2 copies shared of RX per SLICE<br>2 copies shared of TX per SLICE|



## **7.3.4.1 PRU-ICSS Reset Management** 

The device supports warm reset isolation (Hard/Soft Reset, Watchdog Reset) on PRU-ICSS. 

## **7.3.4.2 PRU-ICSS Power and Clock Management** 

The PRU-ICSS supports two levels of clock gating. First level gates all clocks inside the PRU-ICSS when requested by the RCM (Reset Control Manger. The second level allows user software to enable/disable clocks in the clock gating register ICSS_CGR_REG to some internal modules, as follows: 

- IEP 

- ECAP0 

- UART0 

- INTC 

The appropriate configuration registers block controls its local module set inside PRU-ICSS. 

## _**7.3.4.2.1 PRU-ICSS CORE Clock Generation**_ 

**==> picture [411 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
RCM PRU-ICSS<br>ICSS_CORE_CLK_GATE<br>ICSS_IEP_CLK_GATE<br>ICSS_SYS_CLK_GATE CG ICSS_x_IEP_CLK<br>CG ICSS_x_CORE_CLK<br>CG ICSS_x_VBUSP_CLK<br>WUCPUCLK 0<br>EXT_REFCLK 1<br>SYS_CLK 2<br>DPLL_CORE_HSDIV0_CLKOUT0DPLL_PER_HSDIV_CLKOUT0 34 CG ICSS_x_UART_CLK<br>RCCLK10M 5<br>XTALCLK 6<br>DPLL_PER_HSDIV0_CLKOUT2 7<br>RCM<br>ICSSx_UART0_CLK_SRC_SEL<br>ICSSx_UART0_CLK_DIV_VAL<br>ICSSx_UART0_CLK_GATE<br>**----- End of picture text -----**<br>


## **Figure 7-23. PRU-ICSS Clock Diagram** 

The CORE, BUS, and IEP Clock all use the 200 MHz SYS_CLK as a source clock. The UART clock is configurable by configuring the UART clock source select register as well as the UART clock divider value 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

376 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

register. Each of these clock sources has a configurable clock gate that can be configured with the appropriate clock gate register 

## _**7.3.4.2.2 PRU-ICSS Protect**_ 

Write protect block allows software to enable safety protection to prevent corruption of key configuration and debug registers and the Instruction memories (IRAM's) of all PRU cores (PRU0/PRU1). Write protection is also supported for Data RAM0 and Data RAM1. 

This is achived by blocking the byte enables during a write transaction if enabled. When enabled, it will prevent any unwanted write transaction to these elements. To Enable/Disable this feature, software will first need to unlock the write access to this block through the PROT_UNLOCK_KEY register then configure the protection through PROT_CFG register and relock. 

## _**7.3.4.2.3 Module Clock Configurations at PRU-ICSS Top Level**_ 

**Enhanced GPIO clock divider settings:** In certain sample/shift clock settings of the PRU0 and PRU1 EGPIOs (when enabled in serial mode) two cascaded fractional dividers are done in the PRU_ICSS_CFG top level configuration registers PRU_ICSS_GPCFG0 and PRU_ICSS_GPCFG1. In addition, EGPIO clock active edge selection control can be exerted via the bit PRU0_GPI_CLK_MODE for PRU0 EGPIO and PRU1_GPI_CLK_MODE for the PRU1 EGPIO. 

- For the serial PRU0's EGPOs: 

   - PRU_ICSSM_GPCFG0_REG[24-20] PRU0_GPO_DIV1 

   - PRU_ICSSM_GPCFG0_REG[19-15] PRU0_GPO_DIV0 

- For the serial PRU0's EGPIs: 

   - PRU_ICSSM_GPCFG0_REG[12-8] PRU0_GPI_DIV1 

   - PRU_ICSSM_GPCFG0_REG[7-3] PRU0_GPI_DIV0 

- For the serial PRU1's EGPOs: 

   - PRU_ICSSM_GPCFG1_REG[24-20] PRU1_GPO_DIV1 

   - PRU_ICSSM_GPCFG1_REG[19-15] PRU1_GPO_DIV0 

- For the serial PRU1's EGPIs: 

   - PRU_ICSSM_GPCFG1_REG[12-8] PRU1_GPI_DIV1 

   - PRU_ICSSM_GPCFG1_REG[7-3] PRU1_GPI_DIV0 

## **7.3.4.3 Other PRU-ICSS Module Functional Registers at Subsystem Level** 

**Enhanced GPIO** . The other functional mode setting for PRUs EGPIOs at PRU-ICSS top registers level are: 

- PRU_ICSSM_GPCFG0 / PRU_ICSSM_GPCFG1[14] PRU0_GPO_MODE (PRU0 or PRU1) — to select between direct or serial EGPO output mode of operation. 

- PRU_ICSSM_GPCFG0 / PRU_ICSSM_GPCFG1[25] PRU0_GPO_SH_SEL (PRU0 or PRU1) — to select between the EGPO shadow registers 0 and 1 used for output shifting. For more details, refer to the Section 7.3.5.2.2.3.4, _Enhanced General-Purpose Module Outputs (R30)_ . 

- PRU_ICSSM_GPCFG0 / PRU_ICSSM_GPCFG1[1-0] PRU0_GPI_MODE (PRU0 or PRU1) — selects the EGPI input mode of operation ( selects between "direct input", "parallel capture", "28-bit shift" or "MII_RT" modes). 

- PRU_ICSSM_GPCFG0 / PRU_ICSSM_GPCFG1[13] PRU0_GPI_SB (PRU0 or PRU1) — start bit event status for 28-bit EGPI input shift mode. For more details, refer to the Section 7.3.5.2.2.3, _Enhanced GeneralPurpose Module Inputs (R31)_ . 

**PRUs scratchpad (SPAD) memory priority and configuration** related bits are located in the PRU_ICSSM_SPP register. 

## **7.3.4.4 PRU-ICSS Memory Maps** 

The PRU-ICSS comprises various distinct addressable regions that are mapped to both a local and global memory map. The local memory maps are maps with respect to the PRU point of view. The global memory maps are maps with respect to the Host point of view, but can also be accessed by the PRU-ICSS. Each 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 377 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

PRU-ICSS can also access the memories within the other PRU-ICSS subsystem without going through an external port, thanks to PRU-ICSS VBUSP expansion port. 

## _**7.3.4.4.1 PRU-ICSS Local Memory Map**_ 

The PRU-ICSS memory map is documented in Table 7-33 (Instruction Space) and in Table 7-34 (Data Space). Note that these two memory maps are implemented inside the PRU-ICSS and are local to the components of the PRU-ICSS. 

## _**7.3.4.4.1.1 PRU-ICSS Local Instruction Memory Map**_ 

Each PRU (PRU0 and PRU1) has a dedicated 12KB of Instruction Memory which needs to be initialized by an external to PRU-ICSS Host processor before a PRU core executes any instructions. 

## **CAUTION** 

The PRU-ICSS PRU0/1_IRAM regions are ONLY accessible from controllers, external to the PRUICSS (like Arm) when the PRU0/PRU1 is NOT running. The access is via PRU-ICSStarget port on the device CBASS0 interconnect. 

**Table 7-33. PRU-ICSS Local Instruction Memory Map** 

|**Start Address**|**PRU0**|**PRU1**|
|---|---|---|
|0000 0000h|12KB IRAM|12KB IRAM|



## _**7.3.4.4.1.2 PRU-ICSS Local Data Memory Map**_ 

The local data memory map in Table 7-34 allows each PRU core to access the PRU-ICSS addressable regions (both its own subsystem and the other subsystem) and the external host’s memory map. 

**Table 7-34. PRU-ICSS Local Data Memory Map** 

|**Start Address**|**PRU0**|**PRU1**|
|---|---|---|
|0000 0000h|Data 8KB RAM0|Data 8KB RAM1|
|0000 2000h|Data 8KB RAM1|Data 8KB RAM0|
|0000 8000h|RAT_SLICE0|RAT_SLICE0|
|0000 9000h|RAT_SLICE1|RAT_SLICE1|
|0001 0000h|Data 32 KB RAM2 (Shared RAM)|Data 32 KB RAM2 (Shared RAM)|
|0002 0000h|INTC|INTC|
|0002 2000h|PRU0 Control|PRU0 Control|
|0002 4000h|PRU1 Control|PRU1 Control|
|0002 4C00h|PROTECT|PROTECT|
|0002 6000h|CFG|CFG|
|0002 8000h|UART0|UART0|
|0002 E000h|IEP0|IEP0|
|0003 0000h|ECAP0|ECAP0|
|0003 2000h|MII_RT_CFG|MII_RT_CFG|
|0003 2400h|MII_MDIO|MII_MDIO|
|0003 3000h|MII_G_RT_CFG|MII_G_RT_CFG|



## _**7.3.4.4.2 PRU-ICSS Global Memory Map**_ 

The global view of the PRU-ICSS internal memories and control ports is shown in Table 7-35. The offset addresses of each region are implemented inside the PRU-ICSS but the global device memory mapping places the PRU-ICSS target port in the address range shown in the external PRU-ICSS Host top-level memory map. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

378 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

The global memory map is with respect to the Host point of view (that is, device Arm ), but the memory space can also be accessed by the PRU-ICSS itself. Note that PRU0 and PRU1 can use either the local or global addresses to access their internal memories, but using the local addresses provides access time several cycles faster than using the global addresses. This is because when accessing via the global address the access has to be routed through the CBASS0 switch fabric outside PRU-ICSS and back in through the PRU-ICSS target port. 

Each of the PRU cores can access the rest of the device memory (including memory mapped peripheral and configuration registers) using the global memory space addresses. 

**Table 7-35. PRU-ICSS Global Memory Map** 

|**Offset**|**Address**|**PRU-ICSS Target**|
|---|---|---|
|0000|0000h|8KB Data RAM0|
|0000|2000h|8KB Data RAM1|
|0000|8000h|RAT_SLICE0|
|0000|9000h|RAT_SLICE1|
|0001|0000h|32 KB Data RAM2 (Shared Memory)|
|0002|0000h|PRU-ICSS INTC|
|0002|2000h|PRU0 Control|
|0002|2400h|PRU0 Debug|
|0002|4000h|PRU1 Control|
|0002|4400h|PRU1 Debug|
|0002|4C00h|PROTECT|
|0002|6000h|PRU-ICSS CFG|
|0002|8000h|PRU-ICSS UART0|
|0002|E000h|IEP0|
|0002|F000h|Reserved|
|0003|0000h|ECAP0|
|0003|2000h|MII_RT_CFG|
|0003|2400h|MII_MDIO|
|0003|4000h|PRU0 16 KB IRAM|
|0003|8000h|PRU1 16 KB IRAM|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

379 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.5 PRU-ICSS PRU Cores**_ 

This section describes the functionality of the two Programmable Real-time Unit (PRU) processors (PRU0 and PRU1), integrated in the device PRU-ICSS. 

## **7.3.5.1 PRU Cores Overview** 

The PRU is a processor optimized for performing embedded tasks that require manipulation of packed memory mapped data structures, handling of system events that have tight real-time constraints and interfacing with systems external to the SoC. The PRU is both very small and very efficient at handling such tasks. 

The major attributes of the PRU are shown in Table 7-36. 

**Table 7-36. PRU Features** 

|**Attribute**|**Value**|
|---|---|
|IO Architecture|Load/Store|
|Data Flow Architecture|Register to Register|
|_Core Level Bus Architecture_||
|Type|4-Bus Harvard (1 Instruction, 3 Data)|
|Instruction I/F|32-Bit Modified VBUSP Controller|
|Memory I/F 0|32-Bit VBUSP Controller|
|Memory I/F 1|32-Bit VBUSP Controller|
|_Execution Model_||
|Issue Type|Scalar|
|Pipelining|None (Purposefully)|
|Ordering|In Order|
|ALU Type|Unsigned Integer|
|_Registers_||
|General Purpose (GP)|30 (R1 – R30)|
|External Status|0 (R31)|
|GP/Indexing|0 (R0)|
|Addressability in Instruction|Bit, Byte (8-bit), Half-word (16-bit), Word (32-bit),|
||Pointer|
|_Addressing Modes_||
|Load Immediate|16-bit Immediate|
|Load/Store – Memory|Register Base + Register Offset|
||Register Base + 8-bit Immediate Offset|
||Register Base with auto increment/decrement|
||Constant Table Base + Register Offset|
||Constant Table Base + 8-bit Immediate Offset|
||Constant Table Base with auto increment/|
||decrement|
|Data Path Width|32-bit|
|Instruction Width|32-bit|
|Accessibility to Internal PRU Structures|Provides 32-bit VBUSP target with three regions:|
||•<br>Instruction RAM|
||•<br>Control/Status registers|
||•<br>Debug access to internal registers (R0-R31)|
||and constant table|



The processor is based on a four-bus architecture which allows instructions to be fetched and executed concurrently with data transfers. In addition, an input is provided in order to allow external status information 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

380 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

to be reflected in the internal processor status register. Figure 7-24 shows a block diagram of the processing element and the associated instruction RAM/ROM that contains the code that is to be executed. 

**==> picture [491 x 334] intentionally omitted <==**

**----- Start of picture text -----**<br>
Op4 iram_XXX<br>i_data[31:0]<br>R0 Decode and Control<br>R0<br>R1 Instruction<br>. . . OutputShifter RAM/ROM(Clocked)<br>R1 R30 Shift/Mask<br>R31 Program i_addr[31:0]<br>Counter<br>R2<br>R0<br>const_base_sel[4:0]<br>R1 ALU Constants<br>Shift/Mask Data<br>. . . . . . Path I/F Constants Table<br>R30<br>const_base[31:0]<br>R31<br>R29<br>R0 Shift/Mask Memory mem0_XXX<br>I/F<br>R30 R1 mem1_XXX<br>. . .<br>R30<br>R31(Status) R31 Coprocessor I/F regs_XXX<br>Register Execution Unit<br>File<br>R31(Event)<br>Output<br>Multiplexers PRU Core PRU<br>status_in[31:0] events_out[31:0]<br>Destination Selector<br>op1 Mux<br>op2 Mux<br>op3 Mux<br>**----- End of picture text -----**<br>


**==> picture [35 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
icss-005a<br>**----- End of picture text -----**<br>


**Figure 7-24. PRU Block Diagram** 

## **7.3.5.2 PRU Cores Functional Description** 

This section describes the PRU cores supported functionality by describing the constant table, module interface and enhanced GPIOs. 

## _**7.3.5.2.1 PRU Constant Table**_ 

The PRU Constants Table is a structure of hard-coded memory addresses for commonly used peripherals and memories. The constants table is used for more efficiently load/store data to these commonly accessed addresses by: 

- Eliminating the PRU instruction that pre-loads a hard-coded address into the internal register file. 

- Maximizing the usage of the PRU register file for embedded processing applications by moving many of the commonly used constant or deterministically calculated base addresses from the internal register file to an external table. 

**Table 7-37. PRU0/1 Constant Table** 

|**Entry No.**|**Region Pointed To**|**Value [31:0]**|
|---|---|---|
|0|PRU-ICSS INTC (local)|0002_0000h|
|1|PRU-ICSS IEP (local)|0002_F000h|
|2|PRU-ICSS IEP_0x100 (local)|0002_F100h|
|3|PRU-ICSS ECAP0 (local)|0003_0000h|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

381 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-37. PRU0/1 Constant Table (continued)** 

|**Entry No.**|**Region Pointed To**|**Value [31:0]**|
|---|---|---|
|4|PRU-ICSS CFG (local)|0002_6000h|
|5|PRU-ICSS CFG_0x100 (local)|0002_6100h|
|6|PRU-ICSS INTC_0x200 (local)|0002_0200h|
|7|PRU-ICSS UART0 (local)|0002_8000h|
|8|PRU-ICSS IEP0_0x100 (local)|0002_E100h|
|9|PRU-ICSS CFG (local)|0003_3000h|
|10|RESERVED|RSERVED|
|11|PRU-ICSS PRU0 Control (local)|0002_2000h PRU0|
||RESERVED|RESERVED|
||RESERVED|RESERVED|
||PRU-ICSS PRU1 Control (local)|0002_4000h PRU1|
|12|RESERVED|RESERVED|
|13|RESERVED|RESERVED|
|14|RESERVED|RESERVED|
|15|RESERVED|6000_0000h|
|16|RESERVED|7000_0000h|
|17|RESERVED|8000_0000h|
|18|RESERVED|9000_0000h|
|19|RESERVED|A000_0000h|
|20|RESERVED|B000_0000h|
|21|MDIO (local)|0003_2400h|
|22|RAT SLICE0 (local)|0000_8000h PRU0|
||RAT SLICE1 (local)|0000_9000h PRU1|
|23|Reserved|C000_0000h|
|24|PRU-ICSS PRU0/PRU1 Data RAM (local)|0000_0n00h, n = c24_blk_index[3:0]|
|25|PRU-ICSS PRU1/PRU0 Data RAM (local)|0000_2n00h, n = c25_blk_index[3:0]|
|26|PRU-ICSS IEP (local)|0002_En00h, n = c26_blk_index[3:0]|
|27|PRU-ICSS MII_RT/SGMII0_CFG/SGMII1_CFG (local)|0003_2n00h, n = c27_blk_index[3:0]|
|28|PRU-ICSS Shared RAM (local)|00nn_nn00h, nnnn = c28_pointer[15:0]|
|29|RESERVED|0Dnn_nn00h, nnnn = c29_pointer[15:0]|
|30|RESERVED|0Enn_nn00h, nnnn = c30_pointer[15:0]|
|31|RESERVED|0Fnn_nn00h, nnnn = c31_pointer[15:0]|



## **Note** 

The addresses in constants entries 24–31 are partially programmable. Their programmable bit field (for example, c24_blk_index[3:0]) is programmable through the PRU CTRL register space. As a general rule, the PRU should configure this field before using the partially programmable constant entries. 

## _**7.3.5.2.2 PRU Module Interface**_ 

The PRU module interface consists of the PRU internal registers 30 and 31 (R30 and R31). Figure 7-25 shows the PRU module interface and the functionality of R30 and R31. The register R31 serves as an interface with the dedicated PRU general purpose input (GPI) pins and PRU-ICSS INTC. Reading R31 returns status information from the GPI pins and PRU-ICSS INTC via the PRU Real Time Status Interface. Writing to R31 generates PRU 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

382 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

system events via the PRU Event Interface. The register R30 serves as an interface with the dedicated PRU general purpose output (GPO) pins. 

## **Note** 

The below sections cover different functional modes of the PRUn cores, (where n=0,1), enhanced GPIO (EGPIO) interface. The register bits which control EGPIO functionalities are part of the (PRUICSS CFG) space. For descriptions of these EGPIO register bitfield controls, refer to the Section 7.3.4.3. 

**==> picture [388 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU<n><br>i<br>R30 GPO Content PRG<k>_PRU<n>_GPO [ :0] i<br>INTC INTC GPI Content j<br>R31(R) status status PRG<k>_PRU<n>_GPI [ :0] j<br>(bits 29:0)<br>(bit 31) (bit 30)<br>R31(W) INTC System Event Generation<br>**----- End of picture text -----**<br>


**==> picture [23 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
icss-005b<br>**----- End of picture text -----**<br>


**Figure 7-25. PRU Module Interface** 

## _**7.3.5.2.2.1 Real-Time Status Interface Mapping (R31): Interrupt Events Input**_ 

The PRU Real Time Status Interface directly feeds information into register 31 (R31) of the PRU’s internal register file. The firmware on the PRU uses the status information to make decisions during execution. The status interface is comprised of signals from different modules inside of the PRU-ICSS which require some level of interaction with the PRU. More details on the Host interrupts imported into bit 30 and 31 of register R31 of both the PRUs is provided in the , _PRU-ICSS Local Interrupt Controller_ . 

**Table 7-38. Real-Time Status Interface Mapping (R31) Field Descriptions** 

|**Bit**|**Field**|**Description**|
|---|---|---|
|31|pru_intr_in[1]|PRU Host Interrupt 1 from local PRU-ICSS INTC|
|30|pru_intr_in[0]|PRU Host Interrupt 0 from local PRU-ICSS INTC|
|29-0|pru<n>_r31_status[29:0]|Status inputs from primary input via Enhanced GPI port|



## _**7.3.5.2.2.2 Event Interface Mapping (R31): PRU System Events**_ 

This PRU Event Interface directly feeds pulsed event information out of the PRU’s internal ALU. These events are exported out of the PRU-ICSS and need to be connected to the system interrupt controller at the SoC level. The event interface can be used by the firmware to create software interrupts from the PRU to the Host processor. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 383 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [500 x 305] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU0<br>R31(W) 5 3 2 1 0<br>16 ‘d0<br>0 16<br>4 16<br>1<br>enable<br>INTC System Events:<br>PRU1 pr<k>_pru_mst_intr[15:0]_intr_req<br>R31(W) 5 3 2 1 0<br>16 ‘d0<br>0 16<br>4 16<br>1<br>enable<br>**----- End of picture text -----**<br>


**==> picture [21 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
icss-005c<br>**----- End of picture text -----**<br>


**Figure 7-26. Event Interface Mapping (R31)** 

**Table 7-39. Event Interface Mapping (R31) Field Descriptions** 

|**Bit**|**Field**|**Description**|
|---|---|---|
|31-6|Reserved||
|5|pru<n>_r31_vec_valid|Valid strobe for vector output|
|4|Reserved||
|3-0|pru<n>_r31_vec[3:0]|Vector output|



Simultaneously writing a ‘1’ to pru<n>_r31_vec_valid (R31 bit 5) and a channel number from 0 to 15 to pru<n>_r31_vec[3:0] (R31 bits 3-0) creates a pulse on the output of the corresponding pr<k>_pru_mst_intr[x]_intr_req INTC system event. For example, writing ‘100000’ will generate a pulse on prk_pru_mst_intr[0]_intr_req, writing ‘100001’ will generate a pulse on prk_pru_mst_intr[1]_intr_req, and so on to where writing ‘101111’ will generate a pulse on prk_pru_mst_intr[15]_intr_req and writing ‘0xxxxx’ will not generate any system event pulses. The output values from both PRU cores in a subsystem are ORed together. 

The output channels 0-15 are connected to the INTC system events 16-31, respectively. This allows the PRU to assert one of the system events 16-31 by writing to its own R31 register. The system event is used to either post a completion event to one of the host CPUs (Arm) or to signal the other PRU. The host to be signaled is determined by the system interrupt to interrupt channel mapping (programmable). The 16 events are named as prk_pru_mst_intr<15:0>_intr_req. See the _PRU-ICSS Interrupt Requests Mapping,_ in the section _PRU-ICSS Local Interrupt Controller_ , for more details. 

## _**7.3.5.2.2.3 General-Purpose Inputs (R31): Enhanced PRU GP Module**_ 

The PRU-ICSS implements an enhanced General Purpose Input/Output (GPIO) module with SCU that supports the following general-purpose input modes: direct input, 16-bit parallel capture, 28-bit serial shift in, and MII_RT. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

384 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

Register R31 serves as an interface with the general-purpose inputs. Table 7-40 describes the input modes in detail. 

## **Note** 

Each PRU core can only be configured for one GPI mode at a time. Each mode uses the same R31 signals and internal register bits for different purposes. A summary is found in Table 7-41. 

## **Note** 

The PRU_ICSSM_GPCFG0 register, bitfield [29-26] PR1_PRU0_GP_MUX_SEL (PRU0 or PRU1) in the PRU-ICSS CFG register space needs to be set to 0h for GP mode. For a given PRU core, the following IO modes are mutually exclusive: GP mode, Sigma Delta mode, and 3 channel Peripheral I/F mode. 

**Table 7-40. PRU R31 (GPI) Modes** 

|**Mode**|**Function**|**Configuration**|**Configuration**|
|---|---|---|---|
|Direct input|GPI[19:0] feeds directly into the PRU R31|Default state||
|16-bit parallel capture|DATAIN[0:15] is captured by the posedge or negedge|•|Enabled by PRU_ICSSM_GPCFG0 register|
||of CLOCKIN||(PRU0 or PRU1)|
|||•|CLOCKIN edge selected by|
||||PRU_ICSSM_GPCFG0 register|
|28-bit shift in|DATAIN is sampled and shifted into a 28-bit shift|•|Enabled and disabled by PRU_ICSSM_GPECFG0|
||register.||register (PRU0 or PRU1)|
||•<br>Shift Counter (Cnt_16) feature is mapped to|•|Cnt_16 is self clearing and is connected to the|
||pru<n>_r31_status[28].||PRU INTC|
||•<br>SB (Start Bit detection) feature is mapped to|•|Start Bit (SB) is cleared by|
||pru<n>_r31_status[29]||PRU_ICSSM_GPECFG0 register|
|||•|Start Bit value (0h or 1h) selected by|
||||PRU_ICSSM_GPECFG0 register|
|PERIF|The 3 channel Peripheral Interface supports|Enabled by PRU_ICSSM_GPCFG0[1-0]||
||functionality for operations utilized the EnDat 2.2 and|PRU0_GPI_MODE register (value: 1h), where n = 0||
||BiSS protocols.|or 1||
|MII_RT|mii_rt_r31_status [29:0] internally driven by the MII_RT|Enabled by PRU_ICSSM_GPCFG0[1-0]||
||module|PRUn_GPI_MODE register (value: 2h), where n = 0||
|||or 1||
|Sigma Delta|Up to nine channels of concurrent counting with clock|Enabled by PRU_ICSSM_GPCFG0[1-0]||
||source configuration for each channel.|PRUn_GPI_MODE register (value: 3h), where n = 0||
|||or 1||



## **Table 7-41. PRU GPI Signals and Configurations** 

|**Pad Names at Device**<br>|**GPI Modes**|**GPI Modes**|**GPI Modes**|**GPI Modes**|**GPI Modes**|**GPI Modes**|
|---|---|---|---|---|---|---|
|**Level**(1)|**Direct input**|**Parallel Capture**|**28-Bit Shift in**|**PERIF**|**MII**|**Sigma Delta**|
|PR<k>_PRU<n>_GPI0|GPI0|DATAIN0|DATAIN||RXD[0]|SD0_CLK|
|PR<k>_PRU<n>_GPI1|GPI1|DATAIN1|||RXD[1]|SD0_DATA|
|PR<k>_PRU<n>_GPI2|GPI2|DATAIN2|||RXD[3]|SD1_CLK|
|PR<k>_PRU<n>_GPI3|GPI3|DATAIN3|||RXDV|SD1_DATA|
|PR<k>_PRU<n>_GPI4|GPI4|DATAIN4|||RXER|SD2_CLK|
|PR<k>_PRU<n>_GPI5|GPI5|DATAIN5|||RX_CLK|SD2_DATA|
|PR<k>_PRU<n>_GPI6|GPI6|DATAIN6||||SD3_CLK|
|PR<k>_PRU<n>_GPI7|GPI7|DATAIN7|||RXLINK|SD3_DATA|
|PR<k>_PRU<n>_GPI8|GPI8|DATAIN8|||COL|SD4_CLK|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 385 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-41. PRU GPI Signals and Configurations (continued)** 

|**Pad Names at Device**<br>|**GPI Modes**|**GPI Modes**|**GPI Modes**|**GPI Modes**|**GPI Modes**|**GPI Modes**|
|---|---|---|---|---|---|---|
|**Level**(1)|**Direct input**|**Parallel Capture**|**28-Bit Shift in**|**PERIF**|**MII**|**Sigma Delta**|
|PR<k>_PRU<n>_GPI9|GPI9|DATAIN9||PERIF0_IN|CRS|SD4_DATA|
|PR<k>_PRU<n>_GPI1<br>0|GPI10|DATAIN10||PERIF1_IN||SD5_CLK|
|PR<k>_PRU<n>_GPI1<br>1|GPI11|DATAIN11||PERIF2_IN||SD5_DATA|
|PR<k>_PRU<n>_GPI1<br>2|GPI12|DATAIN12||||SD6_CLK|
|PR<k>_PRU<n>_GPI1<br>3|GPI13|DATAIN13||||SD6_DATA|
|PR<k>_PRU<n>_GPI1<br>4|GPI14|DATAIN14||||SD7_CLK|
|PR<k>_PRU<n>_GPI1<br>5|GPI15|DATAIN15||||SD7_DATA|
|PR<k>_PRU<n>_GPI1<br>6|GPI16|CLOCKIN||R31_IN[16]|TX_CLK,R31_IN[<br>16]|SD8_CLK,<br>R31_IN[16]|
|PR<k>_PRU<n>_GPI1<br>7|GPI17|||||SD8_DATA|
|PR<k>_PRU<n>_GPI1<br>8|GPI18||||||
|PR<k>_PRU<n>_GPI1<br>9|GPI19||||||



(1) These pins are also used for Sigma Delta or Peripheral I/F mode. 

## _**7.3.5.2.2.3.1 PRU EGPIs Direct Input**_ 

The pru<n>_r31_status[0:19] bits of the internal PRU register file are mapped to device-level, general purpose input pins (PRU0_GPI[0:19]). In GPI Direct Input mode, PRU0_GPI[0:19] feeds directly to pru<n>_r31_status[0:19]. 

Each PRU of the PRU-ICSS has a separate mapping to device input signals - PRn_PRU0_GPI[19:0] for the PRU0 core and PRn_PRU1_GPI[19:0] for the PRU1 core. There are 40general purpose inputs in total. For more details, refer to the _PRU-ICSS Environment_ . See the device's system reference guide or data sheet for device specific pin mapping. 

## **Note** 

The following PRU IO are not pinned out at the device level: PR0_PRU0_GPIO[7,17,18,19] 

**==> picture [267 x 133] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU<n>_R31<br>0<br>PRU<n>_GPI[0:19] 1<br>20 2<br>…<br>19<br>icss-006<br>**----- End of picture text -----**<br>


**Figure 7-27. PRU R31 (EGPI) Direct Input Mode Block Diagram** 

386 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.5.2.2.3.2 PRU EGPIs 16-Bit Parallel Capture**_ 

The pru<n>_r31_status[0:15] and pru<n>_r31_status[16] bits of the internal PRU register file mapped to devicelevel, general purpose input pins (PRU0_DATAIN [0:15] and PRU0_CLOCKIN, respectively). PRU0_CLOCKIN is designated for an external strobe clock, and is used to capture PRU0_DATAIN [0:15]. 

The PRU<n>_DATAIN can be captured either by the positive or the negative edge of PRU<n>_CLOCK, programmable through the PRU-ICSS CFG register space. If the clocking is configured through the PRU-ICSS CFG register to be positive, then it will equal PRU<n>_CLOCK; however, if the clocking is configured to be negative, then it will equal PRU<n>_CLOCK inverted. 

**==> picture [363 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU<n>_R31<br>16<br>PRU<n>_DATAIN 0<br>1<br>PRU<n>_CLOCKIN …<br>14<br>ICSSM<n>_CORE_CLK<br>Sync Flop 15<br>16<br>ICSSM<n>_CORE_CLK ICSSM<n>_CORE_CLK<br>Sync Flop Sync Flop<br>icss-007<br>**----- End of picture text -----**<br>


**Figure 7-28. PRU R31 (EGPI) 16-Bit Parallel Capture Mode Block Diagram** 

## _**7.3.5.2.2.3.3 PRU EGPIs 28-Bit Shift In**_ 

In 28-bit shift in mode, the device-level, general-purpose input pin PRU<n>_DATAIN is sampled and shifted into a 28-bit shift register on an internal clock pulse. The register fills in LSB order (from bit 0 to 27) and then overflows into a bit bucket. The 28-bit register is mapped to pru<n>_r31_status[0:27] and can be cleared in software through the PRU_ICSS_GPCFG0[13] PRU0_GPI_SB register (PRU0 or PRU1). 

Note that by default, the PRU will continually capture and shift the DATAIN input when the GPI mode has been set. However, clearing the PRU_ICSS_GPCFG0[1] PRU0_GPI_SHIFT_EN bit will freeze the shift operation. 

The shift rate is controlled by the effective divisor of two cascaded dividers applied to the PRUICSS<n>_CORE_CLK clock (200MHz). These cascaded dividers can each be configured through the PRUICSS CFG register space to a value of {1, 1.5, …, 16}. Table 7-42 shows sample effective clock values and the divisor values that can be used to generate these clocks. 

**Table 7-42. PRU EGPIs Effective Clock Values** 

|**Generated clock**|**PRU0_GPI_DIV0**|**PRU0_GPI_DIV1**|
|---|---|---|
|8-MHz|12.5 (17h)|2 (02h)|
|10-MHz|10 (12h)|2 (02h)|
|16-MHz|16 (1Eh)|1 (00h)|
|20-MHz|10 (12h)|1 (00h)|



The 28-bit shift mode also supports the following features: 

- SB (Start Bit detection) is mapped to pru<n>_r31_status[29] and is set when the first 1 (default) or 0 is captured on PRU<n>_DATAIN. The Start Bit value (1 or 0) is configured through the PRU_ICSS_GPECFG0[0] PRU0_GPI_SB_P bit (PRU0 or PRU1). The SB flag in pru<n>_r31_status[29] is cleared in software through the PRU-ICSS CFG register space. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 387 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- Cnt_16 (Shift Counter) is mapped to pru<n>_r31_status[28] and is set on every 16 shift clock samples after the Start Bit has been received. CNT_16 is self clearing and is connected to the local PRU-ICSS INTC. See the _PRU-ICSS Local Interrupt Controller_ for more details. 

- The PRU_ICSS_GPECFG0[1] PRU0_GPI_SHIFT_EN bit can stop or freeze the current shift operation and disable the search for a new Start Bit, if an SB event has not occurred. 

**==> picture [454 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU<n>_R31<br>PRU<n>_DATAIN<br>0<br>27 …<br>28  (Cnt_16)<br>29  (SB)<br>28-bit shift  register<br>Bit Bucket<br>Bit  0 Bit  27<br>ICSSM<n>_CORE_CLK   PRU<n> PRU<n><br>GPO_DIV0 GPO_DIV1<br>pruss-008<br>**----- End of picture text -----**<br>


**Figure 7-29. PRU R31 (EGPI) 28-Bit Shift Mode** 

## _**7.3.5.2.2.3.3.1 PRU EGPI Programming Model**_ 

Follow this steps to configure the PRU EGPI in 28-bit shift input mode: 

1. Clear PRU_ICSS_GPECFG0[1] PRU0_GPI_SHIFT_EN bit (PRU0 or PRU1) 

2. Clear/Set PRU_ICSS_GPECFG0[0] PRU0_GPI_SB_P bit (PRU0 or PRU1) 

3. Clear Start Bit by writing 1h to PRU_ICSS_GPCFG0[13] PRU0_GPI_SB bit 

4. Program the dividers through: PRU_ICSS_GPCFG0[24-20] PRU0_GPO_DIV1 bit (PRU0 or PRU1) PRU_ICSS_GPCFG0[19-15] PRU0_GPO_DIV0 bit (PRU0 or PRU1) 

5. Enable Shift Input Mode by writing to PRU_ICSS_GPECFG0[1] PRU0_GPI_SHIFT_EN bit 

## _**7.3.5.2.2.3.4 General-Purpose Outputs (R30): Enhanced PRU GP Module**_ 

The PRU-ICSS implements an enhanced General Purpose Input/Output (GPIO) module that supports two general-purpose output modes: direct output and shift out. 

Table 7-43 describes these modes in detail. 

## **Note** 

Each PRU core can only be configured for one GPO mode at a time. Each mode uses the same R30 signals and internal register bits for different purposes. A summary is found in Table 7-43. 

## **Note** 

The PRU_ICSS_GPCFG0 register, bitfield [29-26] PR1_PRU0_GP_MUX_SEL (PRU0 or PRU1) in the PRU-ICSS CFG register space needs to be set to 0h for GP mode. For a given PRU core, the following IO modes are mutually exclusive: GP mode, Sigma Delta mode, and 3 channel Peripheral I/F mode. 

388 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-43. PRU R30 (EGPO) Output Mode** 

|**Mode**|**Function**|**Function**|**Configuration**|
|---|---|---|---|
|Direct output|pru<n>_r30[19:0] feeds directly to GPO[19:0]||Default state|
|Shift out|•|pru<n>_r30[0] is shifted out on DATAOUT on every rising edge|Enabled by PRU_ICSS_GPCFG0|
||•<br>•|of pru<n>_r30[1] (CLOCKOUT).<br>LOAD_GPO_SH0 (Load Shadow Register 0) is mapped to<br>pru<n>_r30[29].<br>LOAD_GPO_SH1 (Load Shadow Register 1) is mapped to|register (PRU0 or PRU1)<br>Free Running Clock or Fixed<br>Clock Count Mode selected by<br>PRU_ICSS_GPECFG0 register.|
|||pru<n>_r30[30].||
||•|ENABLE_SHIFT is mapped to pru<n>_r30[31].||



**Table 7-44. GPO Mode Descriptions** 

|**Pad Names at Device Level**(1)|**GPO Modes**|**GPO Modes**|
|---|---|---|
||**Direct output**|**Shift out**|
|PR<k>_PRU<n>_GPO0|GPO0|DATAOUT|
|PR<k>_PRU<n>_GPO1|GPO1|CLOCKOUT|
|PR<k>_PRU<n>_GPO2|GPO2||
|PR<k>_PRU<n>_GPO3|GPO3||
|PR<k>_PRU<n>_GPO4|GPO4||
|PR<k>_PRU<n>_GPO5|GPO5||
|PR<k>_PRU<n>_GPO6|GPO6||
|PR<k>_PRU<n>_GPO7|GPO7||
|PR<k>_PRU<n>_GPO8|GPO8||
|PR<k>_PRU<n>_GPO9|GPO9||
|PR<k>_PRU<n>_GPO10|GPO10||
|PR<k>_PRU<n>_GPO11|GPO11||
|PR<k>_PRU<n>_GPO12|GPO12||
|PR<k>_PRU<n>_GPO13|GPO13||
|PR<k>_PRU<n>_GPO14|GPO14||
|PR<k>_PRU<n>_GPO15|GPO15||
|PR<k>_PRU<n>_GPO16|GPO16||
|PR<k>_PRU<n>_GPO17|GPO17||
|PR<k>_PRU<n>_GPO18|GPO18||
|PR<k>_PRU<n>_GPO19|GPO19||



(1) These pins are also used for Sigma Delta or Peripheral I/F mode. 

## _**7.3.5.2.2.3.4.1 PRU EGPOs Direct Output**_ 

The PRU0_r30 [19:0] bits of the internal PRU register files are mapped to device-level, general-purpose output pins (PRU0_GPO[0:19]). In GPO Direct Output mode, PRU0_r30[0:19] feed directly to PRU0_GPO[0:19]. Each PRU of the PRU-ICSS has a separate mapping to pins, so that there are 40 total general-purpose outputs from the PRU-ICSS. See the device's system reference guide or data sheet for device-specific pin mapping. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 389 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [238 x 110] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU<n>_R30<br>0<br>1 PRU<n>_GPO[0:19]<br>… 20<br>19<br>**----- End of picture text -----**<br>


**==> picture [27 x 7] intentionally omitted <==**

**----- Start of picture text -----**<br>
icss-009<br>**----- End of picture text -----**<br>


**Figure 7-30. PRU R30 (EGPO) Direct Output Mode Block Diagram** 

## _**7.3.5.2.2.3.4.2 PRU EGPO Shift Out**_ 

In shift out mode, data is shifted out of PRU0_r30[0] (PRU0_DATAOUT) on every rising edge of PRU0_r30[1] (PRU0_CLOCK). The shift rate is controlled by the effective divisor of two cascaded dividers applied to the PRU-ICSS<n>_CORE_CLK clock (200MHz). These cascaded dividers can each be configured through the PRU-ICSS CFG register space to a value of {1, 1.5, …, 16}. Table 7-45 shows sample effective clock values and the divisor values that can be used to generate these clocks. Note that shift out mode supports two clocking submodes - Free Running Clock Mode (default) and Fixed Clock Count Mode. The clocking submode is selected through PRU_ICSS_GPECFG0[5] PRU0_GPO_SHIFT_CLK_FREE. In Free Running Clock Mode, PRU0_CLOCKOUT is a free running clock that starts when the PRU GPO mode is set to shift out mode. 

**Table 7-45. Effective Clock Values** 

|**Generated Clock**|**PRU0_GPO_DIV0**|**PRU0_GPO_DIV1**|
|---|---|---|
|8 MHz|12.5 (17h)|2 (02h)|
|10 MHz|10 (12h)|2 (02h)|
|16 MHz|16 (1Eh)|1 (00h)|
|20 MHz|10 (12h)|1 (00h)|



Shift out mode uses two 16-bit shadow registers (GPO_SH0 and GPO_SH1) to support ping-pong buffers. Each shadow register has independent load controls programmable through PRU0_r30[29:30] (PRU0_LOAD_GPO_SH[0:1]). While PRU0_LOAD_GPO_SH[0:1] is set, the contents of PRU<n>_R30[0:15] are loaded into GPO_SH0 and GPO_SH1 shadow registers. 

The data shift will start from the LSB or MSB of GPO_SH0 when PRU<n>_R30[31] (PRU0_ENABLE_SHIFT) is set. The LSB or MSB setting is configurable through PRU_ICSS_GPECFG0[4] PRU0_GPO_SHIFT_SWAP. Note that if no new data is loaded into GPO_SH0/GPO_SH1 after shift operation, the shift operation will continue looping and shifting out the pre-loaded data. 

For Free Running Clock Mode, the shift operation will continue until PRU0_ENABLE_SHIFT is cleared. When PRU0_ENABLE_SHIFT is cleared, the shift operation will finish shifting out the current shadow register, stop, and then reset. 

For Fixed Clock Count Mode, the number of data bits to be shifted out is defined by PRU_ICSS_GPECFG0[15-8] PRU0_GPO_SHIFT_CNT. PRU<n>_CLOCKOUT will stop either high or low with the last data bit. The last data bit will remain persistent. However, the clock stop state is configurable through PRU_ICSS_GPECFG0[16] PRU0_GPO_SHIFT_CLK_HIGH. 

The source of PR<k>_PRU<n>_GPO[2:15] is configurable by PRU_ICSS_GPECFG0[6] PRU0_GPO_SHIFT_GP_EN. By default, if any device-level pins mapped to PRU<n>_R30[2-15] are configured for the PR<k>_PRU<n>_GPO[2:15] pinmux mode, then these pins will reflect the shadow register value written to PRU<n>_R30. Any pin configured for a different pinmux setting will not reflect the shadow register value written to PRU<n>_R30. However, setting PRU_ICSS_GPECFG0[6] PRU0_GPO_SHIFT_GP_EN = 1h allows PRU<n>_R30[2:15] to be controlled by PRU<n>_R30_SHADOW[2-15], which is updated by PRU<n>_R30[2:15] when PRU<n>_R30[28] = 1h. 

390 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [460 x 202] intentionally omitted <==**

**----- Start of picture text -----**<br>
GP_SH0<br>16 16<br>PRU<n>_R30<br>0<br>1<br>15… 16 PRU<n>_DATAOUT<br>… GP_SH1<br>29 (gp_sh0_load)<br>30 (gp_sh1_load) 16 16<br>31 (enable_shift)<br>ICSSM<n>_CORE_CLK GPO_DIV0PRU<n> GPO_DIV1PRU<n> PRU<n>_CLOCKOUT<br>PRG<k>_PRU<n>_GPO[2:15]<br>PRU<n>_R30_SHADOW[2:15]<br>PRUn_GPO_SHIFT_GP_EN<br>icss-010<br>**----- End of picture text -----**<br>


**Figure 7-31. PRU R30 (GPO) Shift Out Mode Block Diagram** 

## _**7.3.5.2.2.3.4.2.1 PRU EGPO Programming Model**_ 

After the PRU is intilized, the software should only enable Shift Out Mode configuration per intilization. 

## _**7.3.5.2.2.3.5 Sigma Delta (SD) Decimation Filtering**_ 

Sigma-delta Sinc filtering is achieved by the combination of PRU hardware and firmware. PRU hardware provides hardware integrators that do the accumulation part of Sinc filtering, while the differentiation part is done in firmware. 

The integrator serves to count the number of 1’s per clock event. Each channel has three cascaded counters, which are the accumulators for the Sinc3 filter. Each counter is 28 bits, giving a maximum count of 268,435,456. Each channel has a free running rollover clock counter. This sample counter updates the count value on the effective clock event for that channel. Each channel also contains a programmable counter compare block, and the compare register has a size of 8 bits. However, the minimum value is 4 and maximum value is 256 due to the 28-bit accumulator. Once sample counter compare value is reached, the shadow register copy is updated and the shadow register copy flag is set. 

Features of the integrators in PRUs SD Demodulator: 

- Up to 9 channels concurrent counting 

- Software can read all 3 stages accumulators 

- Flexible clock source configuration for each channel; option of independent clock source for each channel or one clock source for three channels 

- Programmable, 8-bit sample counter compare register; used to set the OSR of Sinc filter 

- Three 28-bit cascaded counters per channel for accumulation, only Sinc3 and Sinc2 modes supported 

- Common channel enable (all channels are active or none are active) 

- Fast 1 and 0 min/max count sliding programmable window for each of the 9 channels 

## _**7.3.5.2.2.3.5.1 Sigma Delta Block Diagram and Signals**_ 

The Sigma Delta’s I/Os are multiplexed with the PRU GPI/GPO signals, as shown in Table 7-46. 

Note: The PR<k>_PRU<n>_GP_MUX_SEL bitfield in the PRU_ICSS_GPCFG0 register (where k = 0 or 1 and n = 0 or 1) must be set to 3h for configure the GPI/GPO signals for SD mode. 

**Table 7-46. PRU GPI Signals and Configurations for Sigma Delta** 

|**Signal Names at Device Level**(1)|**Sigma Delta (SD) Mode**|**Function**|
|---|---|---|
|PR<k>_PRU<n>_GPI0|SD0_CLK|SD demodulator clock channel 0|
|PR<k>_PRU<n>_GPI1|SD0_D|SD demodulator data channel 0|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

391 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-46. PRU GPI Signals and Configurations for Sigma Delta (continued)** 

|**Signal Names at Device Level**(1)|**Sigma Delta (SD) Mode**|**Function**|
|---|---|---|
|PR<k>_PRU<n>_GPI2|SD1_CLK|SD demodulator clock channel 1|
|PR<k>_PRU<n>_GPI3|SD1_D|SD demodulator data channel 1|
|PR<k>_PRU<n>_GPI4|SD2_CLK|SD demodulator clock channel 2|
|PR<k>_PRU<n>_GPI5|SD2_D|SD demodulator data channel 2|
|PR<k>_PRU<n>_GPI6|SD3_CLK|SD demodulator clock channel 3|
|PR<k>_PRU<n>_GPI7|SD3_D|SD demodulator data channel 3|
|PR<k>_PRU<n>_GPI8|SD4_CLK|SD demodulator clock channel 4|
|PR<k>_PRU<n>_GPI9|SD4_D|SD demodulator data channel 4|
|PR<k>_PRU<n>_GPI10|SD5_CLK|SD demodulator clock channel 5|
|PR<k>_PRU<n>_GPI11|SD5_D|SD demodulator data channel 5|
|PR<k>_PRU<n>_GPI12|SD6_CLK|SD demodulator clock channel 6|
|PR<k>_PRU<n>_GPI13|SD6_D|SD demodulator data channel 6|
|PR<k>_PRU<n>_GPI14|SD7_CLK|SD demodulator clock channel 7|
|PR<k>_PRU<n>_GPI15|SD7_D|SD demodulator data channel 7|
|PR<k>_PRU<n>_GPI16|SD8_CLK|SD demodulator clock channel 8|
|PR<k>_PRU<n>_GPI17|SD8_D|SD demodulator data channel 8|
|PR<k>_PRU<n>_GPI18|-||
|PR<k>_PRU<n>_GPI19|-||



(1) Note: These signals are shared with the GP and Peripheral I/Fs. To configure for Sigma Delta, PRU_ICSS_GPCFG0[29-26] PR1_PRU0_GP_MUX_SEL (where k = 0 or 1 and n = 0 or 1) needs to be set to 3h for SD mode. 

The PR<k>_PRU0_GPI1 signal (muxed with SD0_D) can be used as SD_CLKOUT when PRU-ICSS generates clock. This is a trade-off as PRU application will lose one SD channel. SD_CLKOUT needs to go through a clock generator chip if driving multiple sigma delta modulators and also be looped back into PRU-ICSS as SD_CLKIN, typically pru_gpi16. 

Note: To output the SD clock on PR<k>_PRU0_GPO1, this device requires that the PRU core be configured for both SD and shift out mode (PRU_ICSS_GPCFG0[29-26] PR1_PRU0_GP_MUX_SEL = 3h and PRU_ICSS_GPCFG0[14] PRU<n>_GPO_MODE = 1h). Be sure to configure the shift out mode's clock divisors before enabling shift out mode (PRU_ICSS_GPCFG0[14] PRU<n>_GPO_MODE = 1h). Additionally, the PRU-ICSS, PRU0 SD clock is routed to both PR0_PRU0_GPO1 and PR0_PRU1_GPO1. Figure 7-32 shows a block diagram of the Sigma Delta implementation. Full description of the PRU R30 and R31 registers are shown in Table 7-48 and Table 7-49. 

392 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [500 x 311] intentionally omitted <==**

**----- Start of picture text -----**<br>
Channel 0<br>shadow_update_flag_ovf<br>shadow_update_flag<br>pr<k>_pru<n>_sd0_d data out[27:0]<br>channel_select[3:0]<br>Clock generator channel_en<br>pr<n>_pru<n>_sd8_clk shadow_update_flag_clr<br>CLK_OUT re_init<br>pr<k>_pru<n>_sdi_clk<br>snoop<br>pr<k>_pru<n>_sd0_clk sample_counter_select<br>PRU<n><br>ICSSM_PRUn_SD_CLK_SEL_REGi[1-0] PRUn_SD_CLK_SELi r31_status[29]<br>r31_status[28]<br>ICSSM_PRUn_SD_CLK_SEL_REGi[2] PRUn_SD_CLK_INVi r31_status[27:0]<br>ICSSM_PRUn_SD_SAMPLE_SIZE_REGi[7-0] PRUn_SD_SAMPLE_SIZEi r30[29:26]<br>r30[25]<br>r31[24]<br>r31[23]<br>r30[22]<br>Channel 8 r30[21]<br>shadow_update_flag_ovf<br>shadow_update_flag<br>pr<k>_pru<n>_sd8_d data out[27:0]<br>channel_select[3:0]<br>Clock generator channel_en<br>pr<k>_pru<n>_sd8_clk shadow_update_flag_clr<br>CLK_OUT re_init<br>pr<k>_pru<n>_sdi_clk<br>snoop<br>pr<k>_pru<n>_sd6_clk sample_counter_select<br>ICSSM_PRUn_SD_CLK_SEL_REGi[1-0] PRUn_SD_CLK_SELi<br>ICSSM_PRUn_SD_SAMPLE_SIZE_REGi[7-0] PRUn_SD_SAMPLE_SIZEi<br>pruss-046<br>ICSSM_PRUn_SD_CLK_SEL_REGi[2] PRUn_SD_CLK_INVi<br>Mux/DEMUX<br>...<br>**----- End of picture text -----**<br>


n = 0 or 1 i = 0 to 8 

## **Figure 7-32. Sigma Delta Block Diagram** 

Note: Each channel can independently be configured to use one of three external clock sources. Table 7-47 shows the clock source options, selectable through PRU_ICSS_PRU0_SD_CLK_SELi[1-0] PRU0_SD_CLK_SELi (where n = 0 or 1 and i = 0 to 8). 

**Table 7-47. Sigma Delta External Clock Sources** 

|**PRU0_SD_CLK_SELi value**|**Clock Source**|
|---|---|
|0|pr<k>_pru<n>_sd8_clk|
|1|pr<k>_pru<n>_sd<i>_clk|
|2|pr<k>_pru<n>_sd0_clk for sd0, sd1, and sd2;<br>pr<k>_pru<n>_sd3_clk for sd3, sd4, and sd5;<br>pr<k>_pru<n>_sd6_clk for sd6, sd7, and sd8|



## _**7.3.5.2.2.3.5.2 PRU R30 / R31 Interface**_ 

The PRU uses the R30 and R31 registers to interface with the Sigma Delta interface. Table 7-48 and Table 7-49 shows the R31 and R30 interface for the Sigma Delta mode. Note that only the parameters and data for one channel can be viewed at a time. The channel to be viewed is determined by the r30[29-26] (channel_select). 

**Table 7-48. Sigma Delta PRU Registers: R31** 

|**Bits**|**Field Name**|**Description**|
|---|---|---|
|31-30|Reserved||
|29|shadow_update_flag_ovf|Shadow update flag overflow, set when over sample count equals over sample size|
|||and shadow_update_flag is still set. Set bit R31[24] to clear the flag.|
|28|shadow_update_flag|Shadow update flag, set when over sample count equals over sample size and|
|||shadow_update_flag is still set. Set bit R31[24] to clear the flag.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

393 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-48. Sigma Delta PRU Registers: R31 (continued)** 

||**Bits**|**Field Name**|**Description**|
|---|---|---|---|
|27-0||data_out[27-0]/|data_out[27] (read): most-significant bit of sample data shadow_update_flag_clr|
|||shadow_update_flag_clr (R31[24]) /|(write):|
|||re_init (R31[23])|re_init (write): Set to reset all counters, flags, and shadow copy.|
||||Updates over_sample_size based on the current|
||||PRU_ICSS_PRU0_SD_SAMPLE_SIZEi[7-0] register (where n = 0 or 1 and i = 0|
||||to 8) on the selected channel.|
||||shadow_update_flag_clr (write): Set to clear shadow_update_flag and|
||||shadow_update_flag_ovf (if set).|



## **Table 7-49. Sigma Delta PRU Registers: R30** 

|**Bits**|**Field Name**|**Description**|
|---|---|---|
|31-30|Reserved||
|29-26|channel_select[3-0]|Channel select|
|||0h: Channel 0|
|||...|
|||8h: Channel 8|
|||9h: Reserved|
|||...|
|||Fh: Reserved|
|25|channel_en|Global Channel enable (effects all 9 channels).|
|||0h: All channels disabled. Counters/flags are cleared.|
|||1h: All channels enabled.|
|24-23|Reserved||
|22|snoop|Enable snoop (i.e. fetch data) on the selected channel.|
|||0h: acc1/acc2/acc3 shadow copy|
|||1h: current acc1/acc2/acc3|
|21|sample_counter_select|Read sample counter.|
|||0h: Not selected|
|||1h: Sample count selected|
|20-0|Reserved||



The PRU-ICSS CFG register space has additional registers for controlling the SD demodulator module: 

- PRU_ICSS_PRU0_SD_CLK_SELi[5-4] PRU0_SD_ACC_SELi (where n = 0 or 1, i = 0 to 8) - Selects accumulator 1, 2 or 3 as source (acc1/acc2/acc3). 

- PRU_ICSS_PRU0_SD_CLK_SELi[2] PRU0_SD_CLK_INVi (where n = 0 or 1, i = 0 to 8) - Inverts clock. 

- PRU_ICSS_PRU0_SD_CLK_SELi[1-0] PRU0_SD_CLK_SELi (where n = 0 or 1, i = 0 to 8) - Selects the clock source. 

- PRU_ICSS_PRU0_SD_SAMPLE_SIZEi[7-0] PRU0_SD_SAMPLE_SIZEi (where n = 0 or 1, i = 0 to 8) - Selects number of samples to read before giving output. 

## _**7.3.5.2.2.3.5.3 Sigma Delta Description**_ 

Figure 7-33 shows a block diagram of the Sigma Delta hardware integrators and integration with the PRU R30 / R31 interface for a single channel. 

394 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [500 x 195] intentionally omitted <==**

**----- Start of picture text -----**<br>
ICSSM_PRUn_SD_CLK_SEL_REGi[5-4]<br>PRUn_SD_ACC_SELi<br>fast_detect<br>shadow<br>28 28<br>Capture data_in<br>SD_IN acc1 acc2 acc3<br>CLK_OUT acc1 = acc1+ data_in 28 acc2 = acc2+ acc1 28 acc3 = acc3+ acc2<br>Sync Flop 28<br>if sample_counter =<br>ICSSM_PRUn_SD_SAMPLE_SIZE_REGi[7-0]<br>PRUn_SD_SAMPLE_SIZEi<br>shadow 28<br>Sync Flop 28 r31[27-0]<br>sample_count 28 (data_out)<br>r30[21]<br>(sample_counter_select)<br>**----- End of picture text -----**<br>


**Figure 7-33. Sigma Delta Hardware Integrators Block Diagram (snoop = 0)** 

**==> picture [500 x 205] intentionally omitted <==**

**----- Start of picture text -----**<br>
ICSSM_PRUn_SD_CLK_SEL_REGi[5-4]<br>PRUn_SD_ACC_SELi<br>fast_detect<br>28<br>shadow<br>28 28<br>Capture data_in<br>SD_IN acc1 acc2 acc3<br>CLK_OUT acc1 = acc1+ data_in 28 acc2 = acc2+ acc1 28 acc3 = acc3+ acc2<br>Sync Flop 28<br>if sample_counter =<br>ICSSM_PRUn_SD_SAMPLE_SIZE_REGi[7-0]<br>PRUn_SD_SAMPLE_SIZEi<br>shadow 28<br>Sync Flop 28 r31[27-0]<br>(data_out)<br>sample_count<br>r30[21]<br>(sample_counter_select)<br>28<br>**----- End of picture text -----**<br>


**Figure 7-34. Sigma Delta Hardware Integrators Block Diagram (snoop = 1)** 

The three accumulators (acc1-acc3) for each channel are simple 28 bit adders. The input for acc1 is 1-bit, while the inputs for acc2 and acc3 are 28-bits. On each positive edge of the CLK_OUT, all three 28-bit counters (acc1-acc3) and the sample counter for each channel will get updated as follows: 

```
acc1 = acc1 + data_in
acc2 = acc2 + acc1
acc3 = acc3 + acc2
sample_count = sample_count + 1
```

Each accumulator will rollover at 0xFF_FFFF. For example if acc2 = 0x10 and acc3 = 0xFF_FFFF, then acc3 will update to 0x00_0000F on the next clock event. Sample counter will rollover when it equals the defined sample size (PRU_ICSS_PRU0_SD_SAMPLE_SIZEi[7-0] PRU0_SD_SAMPLE_SIZEi). 

Note that while the channels are not enabled, no operations are performed and all flags and counters are cleared. If a new sample size is to be loaded, the PRU firmware should assert re_init (r31[23]), and all stored count values are cleared to 0. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 395 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

Fast detect block is used to detect fast changes in the amount of ones, presented in a programmable sliding window of 4 to 32 bits. The sliding window is controlled by PRU_ICSS_PRU0_SD_SAMPLE_SIZEi[10-8] PRU0_FD_WINDOW_SIZE_i bit field. 

Fast detect must be enabled through the PRU_ICSS_PRU0_SD_SAMPLE_SIZEi[23] PRU0_FD_EN_i register before SD is enabled. It will start the compare after the first 32 sample clocks. Fast detect block will remain active until a re_init (r31[23]) is asserted. 

The Sigma Delta interface has two status flags: 

- Shadow update flag (r31[28]) 

- Shadow update flag overflow (r31[29]) 

When sample_counter equals the defined sample size (PRU_ICSS_PRU0_SD_SAMPLE_SIZEi[7-0] PRU0_SD_SAMPLE_SIZEi), then the acc1/acc2/acc3 shadow register copy will be updated, the shadow_update_flag (r31[28]) will be set, and sample_counter will rollover to 0. The PRU firmware can clear this flag by writing ‘1’ to shadow_update_flag_clr (r31[28]). If sample_count equals the defined sample size and the shadow_update_flag is still set, then shadow_update_flag_ovf (r31[29]) will be set. Similarly, the PRU firmware can clear this flag by writing ‘1’ to shadow_update_flag_ovf_clr (r31[29]). Note that the clear operation for both flags has a higher priority than the set event. 

The PRU firmware can monitor the acc2/acc3 and sample_counter values through data_out[27-0] (r31[27-0]). Table 7-50 shows the configuration options for data_out[27-0]. 

**Table 7-50. Data_out[27-0] Configuration Options** 

|**snoop (r30[22])**|**sample_counter_select (r30[21])**|**data_out (r31[27-0])**|
|---|---|---|
|0|0|Reads acc1/acc2/acc3 shadow register copy. SeeFigure<br>7-33 _Sigma Delta Hardware Integrators Block Diagram_<br>_(snoop = 0)._|
|1|0|Reads acc1/acc2/acc3 directly. SeeFigure 7-34 _Sigma_<br>_Delta Hardware Integrators Block Diagram (snoop = 1)._|
|0|1|Reads sample_counter shadow register copy. SeeFigure<br>7-33 _Sigma Delta Hardware Integrators Block Diagram_<br>_(snoop = 0)._|
|1|1|Reads sample_counter directly. SeeFigure 7-34 _Sigma_<br>_Delta Hardware Integrators Block Diagram (snoop = 1)._|



## _**7.3.5.2.2.3.5.4 Sigma Delta Basic Programming Example**_ 

The following programming example assumes that the PRU is configured for Sigma Delta Mode ( **PRU_ICSS_GPCFG0** [29-26] PR1_PRU<n>_GP_MUX_SEL = 3h). 

1. Configure clock sources, accumulator source, and sample size: 

   - a. PRU_ICSS_PRU0_SD_CLK_SELi[1-0] PRU0_SD_CLK_SELi (where n = 0 or 1, i = 0 to 8) for clock source 

   - b. PRU_ICSS_PRU0_SD_CLK_SELi[2] PRU0_SD_CLK_INVi (where n = 0 or 1, i = 0 to 8) for clock polarity 

   - c. PRU_ICSS_PRU0_SD_CLK_SELi[5-4] PRU0_SD_ACC_SELi (where n = 0 or 1, i = 0 to 8) - for accumulator source (acc1/acc2/acc3) 

   - d. PRU_ICSS_PRUSS_SD_PRU0_SAMPLE_SIZEi[7-0] PRU0_SD_SAMPLE_SIZE for sample size 

2. Reinitialize all channels whose sample size was configured 

   - a. Select channel by writing to channel_select (r30[29-26]) 

   - b. Delay at least 1 PRU cycle before executing re_int in step 2c. 

   - c. Reinitialize selected channel by writing to re_init (r31[23]) 

   - d. Repeat steps 2a & 2b for all configured channels 

3. Enable all channels by writing ‘1’ to channel_en (r30[25]) 

4. Select channel by writing to channel_select (r30[29-26]) 

396 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

   - a. Poll shadow_update_flag (r31[28]) to detect when acc1/acc2/acc3 shadow register copy data is ready to be read 

   - b. Delay at least 1 PRU cycle before polling shadow_update_flag in Step 4c. 

   - c. Read data_out[27-0] (r31[27-0]) 

   - d. Clear shadow_update_flag by writing ‘1’ to r31[24] 

5. Repeat step 4 for new channel 

## _**7.3.5.2.2.3.6 Three Channel Peripheral Interface**_ 

The 3 channel Peripheral Interface supports functionality for operations utilizing the EnDat 2.2 and BiSS protocols. The 3 channel Peripheral Interface supports both 2 wire and 4 wire serial RS-485 communication. The following table shows the supported encoder protocols for the PRU-ICSS. 

**Table 7-51. Three Channel Peripheral Interface Supported Encoder Protocols** 

|**Encoder Protocol**|**Number of wire in RS-485 Communication**|
|---|---|
|EnDat 2.2|4 wire|
|BiSS|4 wire|
|HDSL|2 wire|
|Tamagawa|2 wire|



This module supports the following features: 

- 3 channels with baud range from 100 kHz to 16 MHz 

- PRU_ICSS_UART_CLK (default) or PRU_ICSS_ICLK controller clock is an input to independent div16fr clock dividers to produce a 1X clock (PERIF<m>_CLK) and oversampling clock 

- Half-duplex (TX and RX are not supported concurrently) 

- TX FIFO size of 32 bits 

- RX FIFO size of 4 bits 

- Configurable shift size/oversampling on RX 

- Optional RX frame size auto shut off 

- Programmable HW delay 1 (wire delay, controlling when the clock signal is first driven low) and delay 2 (tst delay, controlling when the clock signal is first driven high) on TX operation 

- Optional programmable TX termination 

- Individual TX channel start trigger (tx_channel_go) or simultaneous TX start trigger for all channels (tx_global_go) 

- Flexible HW assisted clock output generation to allow free running, stop high and stop low (after last RX data), or stop high (after last TX data) operation with optional software clock override feature 

- Optional SW direct snoop of data input 

- RX Start Bit of '1' or '0' 

## _**7.3.5.2.2.3.6.1 Peripheral Interface Block Diagram and Signal Configuration**_ 

The Peripheral Interface’s I/Os are multiplexed with the PRU GPI/GPO signals, as shown in Table 7-52. The PR1_PRU<n>_GP_MUX_SEL bitfield in the PRU_ICSS_GPCFG0 register (PRU0 or PRU1) must be set to 1h for configure the GPI/GPO signals for Peripheral I/F mode. 

**Table 7-52. PRU GPI/GPO Signals and Configurations for Peripheral I/F**[(1) ] 

|**Pad Names at Device Level**(2) (3)|**Peripheral I/F**|
|---|---|
||**Mode (PRU_ICSS_GPCFG0[29-26]**|
||**PR1_PRU0_GP_MUX_SEL = 1h)**|
|PR<k>_PRU<n>_GPI0||
|PR<k>_PRU<n>_GPI1||
|PR<k>_PRU<n>_GPI2||
|PR<k>_PRU<n>_GPI3||
|PR<k>_PRU<n>_GPI4||
|PR<k>_PRU<n>_GPI5||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 397 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-52. PRU GPI/GPO Signals and Configurations for Peripheral I/F**[(1) ] 

**(continued)** 

|**Pad Names at Device Level**(2) (3)|**Peripheral I/F**|
|---|---|
||**Mode (PRU_ICSS_GPCFG0[29-26]**|
||**PR1_PRU0_GP_MUX_SEL = 1h)**|
|PR<k>_PRU<n>_GPI6||
|PR<k>_PRU<n>_GPI7||
|PR<k>_PRU<n>_GPI8||
|PR<k>_PRU<n>_GPI9|PERIF0_IN|
|PR<k>_PRU<n>_GPI10|PERIF1_IN|
|PR<k>_PRU<n>_GPI11|PERIF2_IN|
|PR<k>_PRU<n>_GPI12||
|PR<k>_PRU<n>_GPI13||
|PR<k>_PRU<n>_GPI14||
|PR<k>_PRU<n>_GPI15||
|PR<k>_PRU<n>_GPI16||
|PR<k>_PRU<n>_GPI17||
|PR<k>_PRU<n>_GPI18||
|PR<k>_PRU<n>_GPI19||
|PR<k>_PRU<n>_GPO0|PERIF0_CLK|
|PR<k>_PRU<n>_GPO1|PERIF0_OUT|
|PR<k>_PRU<n>_GPO2|PERIF0_OUT_EN|
|PR<k>_PRU<n>_GPO3|PERIF1_CLK|
|PR<k>_PRU<n>_GPO4|PERIF1_OUT|
|PR<k>_PRU<n>_GPO5|PERIF1_OUT_EN|
|PR<k>_PRU<n>_GPO6|PERIF2_CLK|
|PR<k>_PRU<n>_GPO7|PERIF2_OUT|
|PR<k>_PRU<n>_GPO8|PERIF2_OUT_EN|
|PR<k>_PRU<n>_GPO9||
|PR<k>_PRU<n>_GPO10||
|PR<k>_PRU<n>_GPO11||
|PR<k>_PRU<n>_GPO12||
|PR<k>_PRU<n>_GPO13||
|PR<k>_PRU<n>_GPO14||
|PR<k>_PRU<n>_GPO15||
|PR<k>_PRU<n>_GPO16||
|PR<k>_PRU<n>_GPO17||
|PR<k>_PRU<n>_GPO18||
|PR<k>_PRU<n>_GPO19||



- (1) Usage of the Peripheral Interface signals are not restricted to only ENDAT interfaces. 

- (2) Note: These signals are shared with the GP, MII and Sigma Delta modes. To configure for Peripheral I/F, PRU_ICSS_GPCFG0[29-26] PR1_PRU0_GP_MUX_SEL needs to be set to 1h. 

- (3) Some devices may not pin out all 29 bits of R31 and all 32 bits of R30. For which pins are available on this device, see _PRUSS Environment_ . See the device-specific Data sheet for device pin mapping. 

A block diagram for the Peripheral I/F is included in Figure 7-35. As shown, each channel is composed of four I/Os: 

- PERIF<m>_IN - RX input data 

398 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- PERIF<m>_CLK - Clock (CLK_OUT) generated by the 1x (or TX) clock. The default value is 1. 

- PERIF<m>_OUT - TX output data. The default value is 0. 

- PERIF<m>_OUT_EN - TX enable output (1 = TX mode, 0 = RX mode). The default value is 0. Note: This signal is auto controlled by hardware. 

**==> picture [498 x 288] intentionally omitted <==**

**----- Start of picture text -----**<br>
From TX FIFO 0<br>Channel 0 0 PRU<n><br>pr0_pru<n>_perif_in0 r31_status[7:0]<br>rx_data_out[7:0] 1<br>ICSS_PRUn_ED_CHm_CFG0_REG[31]<br>val r31_status[24] PRUn_ED_TX_FIFO_SWAP_BITSm<br>ovf r31_status[27]<br>rx_en r30[24] TX FIFO 0..2<br>From TX FIFO 1<br>0 tx_data[7:0]<br>Channel 1 0 r30[7:0]<br>pr0_pru<n>_perif_in1 r31_status[15:8] 1 tx_data[0:7]<br>rx_data_out[7:0] 1 r30[17:16] tx_ch_sel[1:0] pr0_pru<n>_perif0_outpr0_pru<n>_perif0_out_enpr0_pru<n>_perif0_clk<br>r31[18] tx_channel_go<br>r31[19] tx_global_reinit pr0_pru<n>_perif1_out<br>r31[20] tx_global_go pr0_pru<n>_perif1_out_en<br>val r31_status[25] r30[20:19] tx_clk_mode[1:0] pr0_pru<n>_perif1_clk<br>ovf r31_status[28]<br>rx_en From TX FIFO 2 r30[25] tx_fifo_sts[2:0]unrovr pr0_pru<n>_perif2_outpr0_pru<n>_perif2_out_enpr0_pru<n>_perif2_clk<br>tx_global_reinit_act ve/busyi<br>Channel 2 0<br>pr0_pru<n>_perif_in2 r31_status[23:16]<br>rx_data_out[7:0] 1<br>val r31_status[26]<br>ovf r31_status[29]<br>rx_en r30[26]<br>ICSS_PRUn_ED_RX_CFG_REG[2-0]<br>PRUn_ED_RX_SAMPLE_SIZE<br>Clock divider 0 UART_CLK 0 Clock divider<br>1 ICLK 1<br>ICSS_PRUn_ED_RX_CFG_REG[31-16] PRUn_ED_RX_DIV_FACTOR<br>ICSS_PRUn_ED_RX_CFG_REG[15] PRUn_ED_RX_DIV_FACTOR_FRAC ICSS_PRUn_ED_RX_CFG_REG[4] ICSS_PRUn_ED_TX_CFG_REG[4] ICSS_PRUn_ED_TX_CFG_REG[31-16] PRUn_ED_TX_DIV_FACTOR<br>n = 0 to 1 PRUn_ED_RX_CLK_SEL PRUn_ED_TX_CLK_SEL ICSS_PRUn_ED_TX_CFG_REG[15] PRUn_ED_TX_DIV_FACTOR_FRAC<br>To r31_status<br>**----- End of picture text -----**<br>


**==> picture [14 x 3] intentionally omitted <==**

**----- Start of picture text -----**<br>
pruss-046<br>**----- End of picture text -----**<br>


**Figure 7-35. Peripheral I/F Block Diagram** 

## _**7.3.5.2.2.3.6.2 PRU R30 and R31 Interface**_ 

The PRU uses the R30 and R31 registers to interface with the Peripheral I/F. Table 7-53 shows the R31 and R30 interface for the Peripheral I/F RX mode, and Table 7-54 shows the comparable interface for the TX mode. 

**Table 7-53. Peripheral I/F RX** 

|**Register**|**Bits**|**Field name**|**Description**|
|---|---|---|---|
|R31|31-30|Reserved|PRU Host Interrupts 1/0 from local INTC|
||29|ovf2|Overflow Flag for Channel 2. Write 1 to clear.|
||28|ovf1|Overflow Flag for Channel 1. Write 1 to clear.|
||27|ovf0|Overflow Flag for Channel 0. Write 1 to clear.|
||26|val2|Valid Flag for Channel 2. Write 1 to clear.|
||25|val1|Valid Flag for Channel 1. Write 1 to clear.|
||24|val0|Valid Flag for Channel 0. Write 1 to clear.|
||23-16|rx_data_out2|Oversampled Data Output for Channel 2. Note: These bits are shared with the TX Interface.<br>When TX_FIFO has stopped transmission, RX data will be selected.|
||15-8|rx_data_out1|Oversampled Data Output for Channel 1. Note: These bits are shared with the TX Interface.<br>When TX_FIFO has stopped transmission, RX data will be selected.|
||7:0|rx_data_out0|Oversampled Data Output for Channel 0. Note: These bits are shared with the TX Interface.<br>When TX_FIFO has stopped transmission, RX data will be selected.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 399 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-53. Peripheral I/F RX (continued)** 

|**Register**|**Bits**|**Field name**|**Description**|
|---|---|---|---|
|R30|31-27|Reserved||
||26|rx_en2|RX Enable for Channel 2.<br>0h: Channel not enabled, all counters/flags will get reset<br>1h: Channel is enabled|
||25|rx_en1|RX Enable for Channel 1.<br>0h: Channel not enabled, all counters/flags will get reset<br>1h: Channel is enabled|
||24|rx_en0|RX Enable for Channel 0.<br>0h: Channel not enabled, all counters/flags will get reset<br>1h: Channel is enabled|
||23-0|Reserved||



## **Table 7-54. Peripheral I/F TX** 

|**Register**|**Bits**|**Field name**|**Description**|
|---|---|---|---|
|R31|31-30|Reserved||
||29-22|Reserved||
||21|tx_global_reinit_ac<br>tive/ busy2|Tx_global_reinit action has some latency do to clocking. This status shows if action is<br>completed.<br>1h: Active<br>0h: Done<br>For non reinit case, this bit states that last bit is on tx wire. It does not mean the clock is off.<br>1h: Last bit is not done<br>0h: Last bit on tx wire<br>Note that by using rx auto arm feature, the observation is lost at rx enable. This can be used to<br>determine when to enable rx during non-auto arm case.|
||20|tx_global_go|TX global start of all channels.<br>Note: FIFO must not be empty. If empty, transmit will not start.|
||19|tx_global_reinit|Reinit all channels into default mode. This clears all flags and state machines for all channels.<br>Note: Sequence should be assert tx_global_reinit then de-assert rx_en. This will ensure TX and<br>RX are in reset/default state. User must assert this after the frame has been sent and TX is not<br>busy.|
||18|tx_channel_go|TX start the channel transmit (selected by tx_ch_sel).<br>Note: FIFO must not be empty.|
||17|unr2|Under Run Flag for Channel 2. This flag is only set when the tx_frame_count is nonzero and<br>FIFO is empty at time to send data.|
||16|ovr2|Over Run Flag for Channel 2|
||15-14|Reserved||
||13|tx_global_reinit_ac<br>tive/ busy1|Tx_global_reinit action has some latency do to clocking. This status shows if action is<br>completed.<br>1h: Active<br>0h: Done<br>For non reinit case, this bit states that last bit is on tx wire. It does not mean the clock is off.<br>1h: Last bit is not done<br>0h: Last bit on tx wire<br>Note that by using rx auto arm feature, the observation is lost at rx enable. This can be used to<br>determine when to enable rx during non-auto arm case.|
||12-10|tx_fifo_sts1|TX FIFO occupancy status for Channel 1.<br>0 :0 Empty<br>1h: 1 word<br>2h: 2 words<br>3h: 3 words<br>4h: Full<br>5h-7h: Reserved|
||9|unr1|Under Run Flag for Channel 1. This flag is only set when the tx_frame_count is nonzero and<br>FIFO is empty at time to send data.|
||8|ovr1|Over Run Flag for Channel 1|



400 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-54. Peripheral I/F TX (continued)** 

|**Register**|**Bits**|**Field name**|**Description**|
|---|---|---|---|
||7-6|Reserved||
||5|tx_global_reinit_ac<br>tive/ busy0|Tx_global_reinit action has some latency do to clocking. This status shows if action is<br>completed.<br>1h: Active<br>0h: Done<br>For non reinit case, this bit states that last bit is on tx wire. It does not mean the clock is off.<br>1h: Last bit is not done<br>0h: Last bit on tx wire<br>Note that by using rx auto arm feature, the observation is lost at rx enable. This can be used to<br>determine when to enable rx during non-auto arm case.|
||4-2|tx_fifo_sts0|TX FIFO occupancy status for Channel 0.<br>0h: Empty<br>1h: 1 word<br>2h: 2 words<br>3h: 3 words<br>4h: Full<br>5h-7h: Reserved|
||1|unr0|Under Run Flag for Channel 0. This flag is only set when the tx_frame_count is nonzero and<br>FIFO is empty at time to send data.|
||0|ovr0|Over Run Flag for Channel 0|
|R30|31-21|Reserved||
||20-19|clk_mode|CLK_OUT mode.<br>0h: Free-running/stop-low.<br>Clock will remain free-running until the receive module has received the number of bits<br>indicated in rx_frame_counter and then the clock will stop low.<br>1h: Free-running/stop-high (default).<br>Clock will remain free-running until the receive module has received the number of bits<br>indicated in rx_frame_counter and then the clock will stop high. Note: This is the default/reset<br>state, and a hardware reset or reinit will return clk_mode to this state. Note: The initial state of<br>the clock will be high, but the clock will not start until TX GO event.<br>2h: Free-run.<br>NOTE: You must do a reinit to get out of this clock mode then you can update clk_mode to a<br>different mode. Also if you do multiple TX GO, the 2nd go should have tst_delay and wire_delay<br>zero since the clock is free running after the first go.<br>3h: Stop high after transmit. Clock will run until the last TX bit is sent and stops high.|
||18|Reserved||
||17-16|tx_ch_sel|TX channel select.<br>0h: Channel 0<br>1h: Channel 1<br>2h: Channel 2<br>3h: Reserved|
||15-9|Reserved||
||7-0|tx_data|TX data for FIFO.<br>Notes: FIFO transmits MSB first and is 32-bits deep. TX_FIFO_SWAP_BITS bit in the PRU-<br>ICSS CFG register space can be used to flip the load order of bits.<br>The FIFO has 2 modes of operation:<br>1. Preload and Go. This should be done for EnDAT and frames less than 32-bits.<br>2. Continuous mode. This should be done for frames bigger than 32-bits. In continuous mode,<br>software needs to keep up with the line rate and ensure that the FIFO is never empty. When the<br>FIFO is at 2 byte level, software needs to load the next 2 bytes. If software waits till the end of<br>the empty state, it is possible to get the TX into a bad state. The FIFO state can be recovered<br>via re-init.|



## **Note** 

The PRU-ICSS CFG register space has additional registers for controlling the Peripheral I/F module. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 401 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.5.2.2.3.6.3 Clock Generation**_ 

## _**7.3.5.2.2.3.6.3.1 Configuration**_ 

The Peripheral I/F module has two source clock options, PRU_ICSS_UART_CLK (default) and PRU_ICSS_ICLK. There are two independent clock dividers (div16) for the 1x and oversampling (OS) clocks, and each clock divider is configurable by two cascading dividers: 

- [31-16] PRU0_ED_TX_DIV_FACTOR and [15] PRU0_ED_TX_DIV_FACTOR_FRAC for the 1x clock 

- [31-16] PRU0_ED_RX_DIV_FACTOR and [15] PRU0_ED_RX_DIV_FACTOR_FRAC for the OS clock 

The 1x clock is output on the PERIF<m>_CLK signal. In TX mode, the output data is read from the TX FIFO at this 1x clock rate. The default value of this clock is high and the start and stop conditions for this clock are described in Section 3.5.2.2.3.6.3.2 _Clock Output Start Conditions_ and Section 3.5.2.2.3.6.3.3 _Stop Conditions_ . 

In RX mode, the input data is sampled at the OS clock rate. Note: The OS clock rate divided by the 1x clock rate must equal [2-0] PRU0_ED_RX_SAMPLE_SIZE. 

Example clock rates and divisor values relative to the 192-MHz PRU_ICSS_UART_CLK source are shown in Table 7-55. 

**Table 7-55. Clock Rate Examples for 192-MHz PRU_ICSSn_UART_GFCLK Clock Source** 

|**TX_DIV_FACTOR**|**1x Clock**|**RX_DIV_FACTOR**|**RX_DIV_FACTOR_FRAC**|**OS Clock**|**Oversample Factor**|
|---|---|---|---|---|---|
|12|16 MHz|1|1.5|128 MHz|8x|
|16|12 MHz|2|1|96 MHz|8x|
|24|8 MHz|3|1|64 MHz|8x|
|32|6 MHz|4|1|48 MHz|8x|
|48|4 MHz|6|1|32 MHz|8x|
|96|2 MHz|12|1|16 MHz|8x|
|192|1 MHz|24|1|8 MHz|8x|



## _**7.3.5.2.2.3.6.3.2 Clock Output Start Conditions**_ 

This section describes the configurable start conditions for the PERIF<m>_CLK. The software can completely control via PRU_ICSS_PRU0_ED_CHm_CFG0 when bit [29] PRU0_ED_CLK_OUT_OVR_ENm = 1h (where n = 0 or 1 and m = 0 to 2). By default however, the PRU hardware will control the clocks as described in the following sections. 

## **7.3.5.2.2.3.6.3.2.1 TX Mode (RX_EN = 0)** 

In TX mode, the PERIF<m>_CLK begins after the firmware loads the TX FIFO and sets either r31[20] (tx_global_go) or r30[17-16] (tx_channel_go) to 1h. After the “go” bit is set, the delay1 (wire delay) compensation counter for each channel begins. After delay1 is complete, PERIF<m>_CLK is driven low and then the delay2 (tst) counter begins. After the delay2 counter expires, the PERIF<m>_CLK starts running (first low and then high). Therefore, first rising edge of PERIF<m>_CLK (measured from the go bit) = delay1 (tx wire delay) + delay2 (tst_counter delay) + half of the 1x clock frequency (since the clock starts low). 

Figure 7-36 shows the start condition for TX mode. As shown in the figure, the default value of clock is high. The PRU-ICSS CFG register space has additional registers for controlling the TX start timing delay values: 

- Delay 1: PRU_ICSS_PRU0_ED_CHm_CFG0_REG[10-0] PRU0_ED_TX_WDLYm (where n = 0 or 1 and m = 0 to 2) 

- Delay 2: PRU_ICSS_PRU0_ED_CHm_CFG1_REG[15-0] PRU0_ED_TST_DELAY_COUNTERm (where n = 0 or 1 and m = 0 to 2) 

402 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [499 x 111] intentionally omitted <==**

**----- Start of picture text -----**<br>
tx_global_go or<br>tx_channel_go = 1<br>Half of<br>first 1x clock<br>delay1 delay2<br>PERIF<m>_CLK<br>**----- End of picture text -----**<br>


**Figure 7-36. TX Mode Start Condition** 

## **7.3.5.2.2.3.6.3.2.2 RX Mode (RX_EN = 1)** 

In RX mode, the PERIF<m>_CLK will start running whenever the RX_EN is set. Note that the PRU firmware in this mode is responsible for any delay conditions. 

The hardware can also auto-enable RX mode at the end of a TX transaction. The 

PRU_ICSS_PRU0_ED_CHm_CFG1_REG[31-16] PRU0_ED_RX_EN_COUNTERm (where n = 0 or 1 and m = 0 to 2) is used to program a delay between the last TX bit sent and when the RX_EN is set. 

## _**7.3.5.2.2.3.6.3.3 Stop Conditions**_ 

The r30[20-19] (clk_mode[1:0]) value determines the stop condition for PERIF<m>_CLK. There are 4 options available: 

|**clk_mode_value**|**Description**|
|---|---|
|0|Stop low on last RX frame|
|1|Stop high on last RX frame|
|2|Run continuously|
|3|Stop high on last TX bit|



The last RX frame is configured by PRU_ICSS_PRU0_ED_CHm_CFG0_REG[27-16] PRU0_ED_RX_FRAME_SIZEm, and the last TX bit is configured by 

PRU_ICSS_PRU0_ED_CHm_CFG0_REG[15-11] PRU0_ED_TX_FRAME_SIZEm (where n = 0 or 1 and m = 0 to 2). Each stop condition is shown in Figure 7-37 through Figure 7-40. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 403 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [499 x 321] intentionally omitted <==**

**----- Start of picture text -----**<br>
Last RX frame<br>PERIF<m>_IN<br>PERIF<m>_CLK<br>PERIF<m>_OUT_EN<br>**----- End of picture text -----**<br>


**Figure 7-37. PERIF<m>_CLK Stop High on Last RX Frame** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

404 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [499 x 320] intentionally omitted <==**

**----- Start of picture text -----**<br>
Last RX frame<br>PERIF<m>_IN<br>PERIF<m>_CLK<br>PERIF<m>_OUT_EN<br>**----- End of picture text -----**<br>


**Figure 7-38. PERIF<m>_CLK Stop Low on Last RX Frame** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 405 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [499 x 321] intentionally omitted <==**

**----- Start of picture text -----**<br>
Last RX frame<br>PERIF<m>_IN<br>PERIF<m>_CLK<br>PERIF<m>_OUT_EN<br>**----- End of picture text -----**<br>


**Figure 7-39. PERIF<m>_CLK Run Continuously** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

406 

Copyright © 2025 Texas Instruments Incorporated 

**==> picture [504 x 301] intentionally omitted <==**

**----- Start of picture text -----**<br>
www.ti.com Processors and Accelerators<br>Last TX frame<br>PERIF<m>_OUT<br>PERIF<m>_CLK<br>PERIF<m>_OUT_EN<br>**----- End of picture text -----**<br>


**Figure 7-40. PERIF<m>_CLK Stop High on Last TX Bit** 

## _**7.3.5.2.2.3.6.4 Three Peripheral Mode Basic Programming Model**_ 

The following programming models assume that the PRU is configured for 3 Peripheral Mode (PRU_ICSS_GPCFG0[29-26] PR1_PRU0_GP_MUX_SEL = 1h). 

## _**7.3.5.2.2.3.6.4.1 Clock Generation**_ 

Follow these steps to configure Peripheral I/F clocks using the HW control of the clock: 

1. Select TX and RX clock sources: 

   - a. PRU_ICSS_PRU0_ED_TX_CFG_REG[4] PRU0_ED_TX_CLK_SEL for the TX clock source 

   - b. PRU_ICSS_PRU0_ED_RX_CFG_REG[4] PRU0_ED_RX_CLK_SEL for the RX clock source 

2. Configure the 1x (TX) clock frequency: 

   - a. Write Division Factor to PRU_ICSS_PRU0_ED_TX_CFG_REG[31-16] PRU0_ED_TX_DIV_FACTOR 

   - b. Write Fraction division factor to PRU_ICSS_PRU0_ED_TX_CFG_REGISTER[15] PRU0_ED_TX_DIV_FACTOR_FRAC 

3. Configure the oversampling (RX) frequency and oversample size: 

   - a. Write Division Factor to PRU_ICSS_PRU0_ED_RX_CFG_REG[31-16] PRU0_ED_RX_DIV_FACTOR b. Write Fraction division factor to PRU_ICSS_PRU0_ED_RX_CFG_REG[15] PRU0_ED_RX_DIV_FACTOR_FRAC 

   - c. Write RX oversample size to PRU_ICSS_PRU0_ED_RX_CFG_REG[2-0] PRU0_ED_RX_SAMPLE_SIZE 

4. Select the clk_mode to configure how the PERIF<m>_CLK signal ends after TX/RX: 

   - a. Write to r30[20-19] (clk_mode). Note: The clk_mode setting can also be changed per transaction. 

5. Configure the wire, tst, and rx_en_counter delay values: 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 407 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- a. PRU_ICSS_PRU0_ED_CHm_CFG0_REG[10-0] PRU0_ED_TX_WDLYm for wire delay (where n = 0 or 1 and m = 0 to 2) 

- b. PRU_ICSS_PRU0_ED_CHm_CFG1_REG[15-0] PRU0_ED_TST_DELAY_COUNTERm for tst delay (where n = 0 or 1 and m = 0 to 2) 

- c. PRU_ICSS_PRU0_ED_CHm_CFG1_REG[31-16] PRU0_ED_RX_EN_COUNTER for auto-delay between TX and RX (where n = 0 or 1 and m = 0 to 2) 

## _**7.3.5.2.2.3.6.4.2 TX - Single Shot**_ 

Follow these steps to configure the Peripheral I/F channel(s) for a single shot transmission: 

1. (Optional) Configure TX FIFO for MSB (default) or LSB: 

   - a. PRU_ICSS_PRU0_ED_CHm_CFG0_REG[31] PRU0_ED_TX_FIFO_SWAP_BITSm (where n = 0 or 1 and m = 0 to 2) 

2. Pre-load TX FIFO: 

   - a. Select TX channel by writing the desired channel number to R30[17-16] (tx_ch_sel) 

   - b. Write 1-4 bytes of data to r30[7-0] (tx_data). At each r30[7-0] write, data will be pushed into the FIFO. c. Repeat Steps 2a and 2b for all desired channels. 

3. Configure TX frame size if less than 4 full bytes loaded into FIFO: 

   - a. PRU_ICSS_PRU0_ED_CHm_CFG0_REG[15-11] PRU0_ED_TX_FRAME_SIZEm (where n = 0 or 1 and m = 0 to 2) 

4. Push TX FIFO data to PERIF<m>_OUT (see Section 3.5.2.2.3.6.3.2 for the PERIF<m>_CLK and PERIF<m>_OUT start time relationship); 

   - a. To start TX on all channels, set r31[20] = 1 (tx_global_go). 

   - b. To start TX on individual channel: 

      - i. Select TX channel by writing the desired channel number to R30[17-16] (tx_ch_sel) ii. Set R31[18] = 1 (tx_channel_go) 

5. If PRU_ICSS_PRU0_ED_CHm_CFG1_REG[31-16] PRU0_ED_RX_EN_COUNTERm > 0 (where n = 0 or 1 and m = 0 to 2), then the channel will automatically switch into RX mode. See Section 3.5.2.2.3.6.4.4 for an example of how to program and configure RX content. 

6. If PRU_ICSS_PRU0_ED_CHm_CFG1_REG[31-16] PRU0_ED_RX_EN_COUNTERm = 0, poll either r31[21, 13, or 5] (tx_global_reinit_active/busy[2,1,0]) or PRU_ICSS_PRU0_ED_TX_CFG_REG[7, 6, or 5] PRU0_ED_BUSY_m (where m = 0 to 2, indicates channel number) for when TX is complete 

## **Note** 

The PERIF<m>_CLK Peripheral I/F requires that PERIF<m>_CLK be in a high state at the beginning of a new transaction. If the clock ended the single shot transmission in low state, then the clock needs to be reset before sending more data. The steps to reset PERIF<m>_CLK are: 

1. Set R31[19] = 1 (tx_global_reinit) to reset clock high 

2. Wait until PRU0_ED_BUSY_m bit is cleared 

3. Re-configure R30[20-19] (clk_mode), since reinit will reset the clk_mode to "Free-running/stophigh" mode 

## _**7.3.5.2.2.3.6.4.3 TX - Continuous FIFO Loading**_ 

Follow these steps to configure the Peripheral I/F channel(s) for a continuous loading transmission: 

1. (Optional) Configure TX FIFO for MSB (default) or LSB: 

   - a. PRU_ICSS_PRU0_ED_CHm_CFG0_REG[31] PRU0_ED_TX_FIFO_SWAP_BITSm 

2. Pre-load TX FIFO: 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

408 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

   - a. Select TX channel by writing the desired channel number to r30[17-16] (tx_ch_sel) 

   - b. Write 1-4 bytes of data to r30[7-0] (tx_data). At each r30[7-0] write, data will be pushed into the FIFO. c. Repeat Steps 2a and 2b for all desired channels. 

3. Configure TX frame size to continuously transmit the TX FIFO until empty: 

   - a. Set PRU_ICSS_PRU0_ED_CHm_CFG0_REG[15-11] PRU0_ED_TX_FRAME_SIZEm = 0h 

4. Push TX FIFO data to PERIF<m>_OUT (see Section 3.5.2.2.3.6.3.2 for the PERIF<m>_CLK and PERIF<m>_OUT start time relationship): 

   - a. To start TX on all channels, set r31[20] = 1 (tx_global_go). 

   - b. To start TX on individual channel: 

      - i. Select TX channel by writing the desired channel number to r30[17-16] (tx_ch_sel) 

      - ii. Set r31[18] = 1 (tx_channel_go) 

5. Monitor line rate and reload FIFO: 

   - a. Polling r31[xx, 12-10, 4-2] (tx_fifo_sts<m>) 

   - b. When FIFO level is at 2 bytes, load next 2 bytes of data (see Step 2). Do not let the FIFO get close to 0. Once the FIFO runs empty, the hardware will assume the PRU has reached end of the last transmit. Any new writes to the FIFO will NOT be sent until the software sends another tx_channel_go bit. Note: There are also underrun and overrun error flags that can be monitored. 

6. To end TX operation, do not send any new data to FIFO. 

   - a. If PRU_ICSS_PRU0_ED_CHm_CFG1_REG[31-16] PRU0_ED_RX_EN_COUNTERm > 0 (where n = 0 or 1 and m = 0 to 2), then the channel will automatically switch into RX mode. See Section 3.5.2.2.3.6.4.4 for an example of how to program and configure RX content. 

   - b. If PRU_ICSS_PRU0_ED_CHm_CFG1_REG[31-16] PRU0_ED_RX_EN_COUNTERm = 0, poll either r31[21, 13, or 5] (tx_global_reinit_active/busy[2,1,0]) or PRU_ICSS_PRU0_ED_TX_CFG_REG[7, 6, or 5] PRU0_ED_BUSY_m (where m = 0 to 2, indicates channel number) for when TX is complete 

## **Note** 

The PERIF<m>_CLK Peripheral I/F requires that PERIF<m>_CLK be in a high state at the beginning of a new transaction. If the clock ended the continuous loading transmission in low state, then the clock needs to be reset before sending more data. The steps to reset PERIF<m>_CLK are: 

1. Set R31[19] = 1 (tx_global_reinit) to reset clock high 

2. Wait until PRU0_ED_BUSY_m is cleared 

3. Re-configure R30[20-19] (clk_mode), since reinit will reset the clk_mode to "Free-running/stophigh" mode 

## _**7.3.5.2.2.3.6.4.4 RX - Auto Arm or Non-Auto Arm**_ 

Follow these steps to configure the Peripheral I/F channel(s) to receive data: 

1. Configure RX and frame size: 

   - a. PRU_ICSS_PRU0_ED_CHm_CFG0_REG[27-16] PRU0_ED_RX_FRAME_SIZEm (where n = 0 or 1 and m = 0 to 2) 

2. Configure start bit polarity: 

   - a. PRU_ICSS_PRU0_ED_RX_CFG_REG[3] RX_SB_POL (PRU0 or PRU1) 

   - b. For the non-auto arm use case, set r30[26, 25, 24] = 1 (rx_en<m>) 

   - c. For the auto arm use case, rx_en<m> will be automatically enabled at the end of a TX operation when PRU_ICSS_PRU0_ED_CHm_CFG1_REG[31-16] PRU0_ED_RX_EN_COUNTERm > 0 (where n = 0 or 1 and m = 0 to 2) 

3. RX FIFO will start filling on the first start bit (PERIF<m>_IN = 1). The data will be captured on the positive edge of the PERIF<m>_CLK and shifted into the LSB position of the 8-bit shadow register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 409 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

4. Poll for r31[26, 25, 24] (val<m>) assertion. The valid flag will be asserted when n bits of data (determined by PRU_ICSS_PRU0_ED_RX_CFG_REG[2-0] PRU0_ED_RX_SAMPLE_SIZE) have been collected. 

5. Fetch data by reading r31[23-16, 15-8, 7-0] (rx_data_out<m>). The data will remain constant for one data frame, and PRU must read data and clear valid flag within this time. Otherwise, an overflow will occur – r31[29, 28, 27] (ovf<m>) = 1 - indicating that val<m> has been continuously asserted for longer than one data frame. 

6. The clock will be stopped based on the r30[20-19] (clk_mode) configured before the start of the RX operation. 

7. Clear r30[26, 25, 24] (rx_en<m>) to disable RX mode. All counters and flags will be reset. 

## **7.3.5.3 PRU-ICSS RAM Index Allocation** 

The PRU-ICSS module includes integrated ECC Aggregator module to test ECC functionality. 

Table 7-56 shows the mapping of the RAM IDs to the ECC RAMs serviced by the ECC Aggregator. 

**Table 7-56. Mapping of the RAM IDs to the ECC RAMs** 

|**RAM Index**|**ECC RAM Prefix**|**Description**|
|---|---|---|
|0|pr<k>_dram0|Data RAM0 (8KB)|
|1|pr<k>_dram1|Data RAM1 (8KB)|
|2|pr<k>_pru0_iram|PRU0 Instruction Memory (16KB)|
|3|pr<k>_pru1_iram|PRU1 Instruction Memory (16KB)|
|4|pr<k>_ram|Shared Data RAM2 (32KB)|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

410 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.6 PRU-ICSS Broadside Accelerators**_ 

## **7.3.6.1 PRU-ICSS Broadside Accelerators Overview** 

The PRU-ICSS supports a broadside interface, which uses the XFR (XIN, XOUT, or XCHG) instruction to transfer the contents of PRUn (where n = 0 or 1) registers to or from accelerators. This interface enables up to 31 registers (R0-R30, or 124 bytes) to be transferred in a single instruction. This section details the various accelerators that are available to the PRUn through the broadside interface. 

Each of those functions have a unique XIN ID to determine which operation will occur. For more information see Table 7-32. 

## **7.3.6.2 PRU-ICSS Data Processing Accelerators Functional** 

## _**7.3.6.2.1 PRU Multiplier with Accumulation (MPY/MAC)**_ 

This section describes the MAC (multiplier with accumulation) module integrated to PRU0/PRU1 cores. 

Each of the two PRU cores (PRU0/PRU1) has a designated unsigned multiplier with accumulation (MPY/MAC). The MAC supports two modes of operation: Multiply Only and Multiply and Accumulate. 

The MAC is directly connected with the PRU internal registers R25-R29 and uses the broadside load/store PRU interface and XFR instructions to both control and mode of the MAC and import the multiplication results into the PRU. 

The PRU MPY/MAC features are: 

- Configurable Multiply Only and Multiply and Accumulate functionality via PRU register R25 

- 32-bit operands with direct connection to PRU registers R28 and R29 

- 64-bit result (with carry flag) with direct connection to PRU registers R26 and R27 

- One clock cycle per operation 

- PRU broadside interface and XFR instructions (XIN, XOUT) allow for importing multiplication results and initiating accumulate function 

## _**7.3.6.2.1.1 PRU MAC Operations**_ 

## _**7.3.6.2.1.1.1 PRU versus MAC Interface**_ 

The MAC directly connects with the PRU internal registers R25-R29 through use of the PRU broadside interface and XFR instructions. Figure 7-41 shows the functionality of each register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 411 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [426 x 261] intentionally omitted <==**

**----- Start of picture text -----**<br>
Function Function<br>PRU<br>Bit Bit<br>[0] loads current state of MAC_MODE XIN R25 XOUT [0] Loads MAC_MODE, if set to “1”, the<br>[1] loads the current state of MAC mode /status MAC will perform one multiply andaccumulate function.<br>ACC_CARRY<br>Lower 32 bit product XIN R26 R26 [1] write “1” clears ACC_CARRY<br>Lower product<br>XIN R27<br>Upper 32 bit product R27<br>Upper product<br>R28<br>R28 Auto-sampled 32 operands:<br>Operand Sampled every clock.<br>In MAC mode, the product<br>R29 R29 Auto-sampled of R28*R29 will be added<br>Operand to the accumulator on<br>every XOUT of R25.<br>MAC<br>XFR device ID for<br>MPY/MAC = 0<br>icss-022<br>**----- End of picture text -----**<br>


**Figure 7-41. Integration of the PRU and MPY/MAC** 

The XFR instructions (XIN and XOUT) are used to load/store register contents between the PRU core and the MAC. These instructions define the start, size, direction of the operation, and device ID. The device ID number corresponding to the MPY/MAC is shown in Table 7-57. 

**Table 7-57. MPY/MAC XFR ID** 

|**Device ID**|**Function**|
|---|---|
|0|Selects MPY/MAC|



The PRU register R25 is mapped to the MAC_CTRL_STATUS register (Table 7-58). The MAC’s current status (MAC_MODE and ACC_CARRY states) is loaded into R25 using the XIN command on R25. The PRU sets the MAC’s mode and clears the ACC_CARRY using the XOUT command on R25. 

**Table 7-58. MAC_CTRL_STATUS Register (R25) Field Descriptions** 

|**Bit**|**Field**|**Description**|
|---|---|---|
|7-2|RESERVED|Reserved|
|1|ACC_CARRY|Write 1 to clear.<br>It is sticky.<br>It is set 0 cycles after the event.<br>0h: 64-bit accumulator carry has not occurred<br>1h: 64-bit accumulator carry occurred|
|0|MAC_MODE|0h: Accumulation mode disabled and accumulator is cleared<br>1h: Accumulation mode enabled|



The two 32-bit operands for the multiplication are loaded into R28 and R29. These registers have a direction connection with the MAC. Therefore, XOUT is not required to load the MAC. In multiply mode, the MAC samples these registers every clock cycle. In multiply and accumulate mode, the MAC samples these registers every XOUT R25[7-0] transaction when MAC_MODE = 1. 

The product from the MAC is linked to R26 (lower 32 bits) and R27 (upper 32 bits). The product is loaded into register R26 and R27 using XIN. 

412 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.6.2.1.1.2 Multiply only mode(default state), MAC_MODE = 0**_ 

The Figure 7-42 summarizes the MAC operation in "Multiply-only"mode, in which the MAC multiplies the contents of R28 and R29 on every clock cycle. 

**==> picture [428 x 117] intentionally omitted <==**

**----- Start of picture text -----**<br>
R28 R29 R27 R26<br>X =<br>32-bit operand 32-bit operand Upper 32-bit product Lower 32-bit operand<br>Multiply mode :<br>sampled every clock cycle XIN<br>MAC<br>**----- End of picture text -----**<br>


**==> picture [27 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
icss-023<br>**----- End of picture text -----**<br>


**Figure 7-42. MAC Multiply-only Mode- Functional Diagram** 

## _**7.3.6.2.1.1.2.1 Programming PRU MAC in "Multiply-ONLY" mode**_ 

The following steps are performed by the PRU firmware for multiply-only mode: 

1. 1. Enable multiply only MAC_MODE. 

   - a. (a) Clear R25[0] for multiply only mode. 

   - b. (b) Store MAC_MODE to MAC using XOUT instruction with the following parameters: 

      - Device ID = 0 

      - Base register = R25 

      - Size = 1 

2. 2. Load operands into R28 and R29. 

3. 3. Delay at least 1 PRU cycle before executing XIN in step 4. 

4. 4. Load product into PRU using XIN instruction on R26, R27. 

Repeat steps 2 and 4 for each new operand. 

## _**7.3.6.2.1.1.3 Multiply and Accumulate Mode, MAC_MODE = 1**_ 

The Figure 7-43 summarizes the MAC operation in "Multiply and Accumulate" mode. On every XOUT R25_REG[7-0] transaction, the MAC multiplies the contents of R28 and R29, adds the product to its accumulated result, and sets ACC_CARRY if an accumulation overflow occurs. 

**==> picture [428 x 117] intentionally omitted <==**

**----- Start of picture text -----**<br>
R28 R29 R27 R26<br>X =<br>32-bit operand 32-bit operand Upper 32-bit product Lower 32-bit operand<br>Multiply and Accumulate mode<br>sampled every XOUT of R25:<br>XIN<br>MAC<br>**----- End of picture text -----**<br>


**==> picture [27 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
icss-024<br>**----- End of picture text -----**<br>


## **Figure 7-43. MAC Multiply and Accumulate Mode Functional Diagram** 

## _**7.3.6.2.1.1.3.1 Programming PRU MAC in Multiply and Accumulate Mode**_ 

The following steps are performed by the PRU firmware for multiply and accumulate mode: 

1. Enable multiply and accumulate MAC_MODE. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 413 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- (a) Set R25[1-0] = 1 for accumulate mode. 

- (b) Store MAC_MODE to MAC using XOUT instruction with the following parameters: 

- Device ID = 0 

- Base register = R25 

- Size = 1 

2. Clear accumulator and carry flag. 

- (a) Set R25[1-0] = 3 to clear accumulator (R25[1]=1) and preserve accumulate mode (R25[0]=1). 

- (b) Store accumulator to MAC using XOUT instruction on R25. 

3. Load operands into R28 and R29. 

4. Multiply and accumulate, XOUT R25[1-0] = 1 

Repeat step 4 for each multiply and accumulate using same operands. 

Repeat step 3 and 4 for each multiply and accumulate for new operands. 

5. Load the accumulated product into R26, R27, and the ACC_CARRY status into R25 using the XIN instruction. 

## **Note** 

Steps one and two are required to set the accumulator mode and clear the accumulator and carry flag. 

414 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.6.2.2 PRU CRC16/32 Module**_ 

Each of the PRU0/PRU1 cores have a designated CRC16/32 module. 

In general, CRC adds error detection capability to communication systems. The CRC encoder appends redundant bits (or CRC bits) to the systematic data message. During reception of the data message, the received data is also encoded with the same CRC encoder. The 2 sets of CRC bits are compared together. If they match, there were no transmission errors; and if they don’t match, a transmission error has been detected. 

CRC16/32 supports the following features: 

- Supports CRC32: 

   - x[32] +x[26] +x[23] +x[22] +x[16] +x[12] +x[11] +x[10] +x[8] +x[7] +x[5] +x[4] +x[2] +x+1 

- Supports CRC16: 

   - x[16] +x[15] +x[2] +1 

- Supports CRC16 - CCITT: 

   - x[16] +x[12] +x[5] +1 

- PRU broadside interface and XFR instructions (XIN, XOUT) allow for importing CRC results and executing accumulate function 

## _**7.3.6.2.2.1 PRU and CRC16/32 Interface**_ 

The CRC16/32 module directly connects with the PRU internal registers R25-R29 through use of the PRU broadside interface and XFR instructions. Table 7-59 shows the functionality of each register. 

The XFR instructions (XIN/XOUT/XCHG) are used to load/store register contents between the PRU core and the CRC16/32 module. These instructions define the start, size, direction of the operation, and device ID. The XFR device ID number corresponding to the CRC16/32 module is 1. 

**Table 7-59. CRC Register to PRU Port Mapping** 

|**CRC Register**|**R/W**|**Description**|**PRU Mapping**|
|---|---|---|---|
|CRC_CFG|W|Always write all 4 bytes.|R25|
|||bit [0] CRC32_ENABLE:||
|||0: CRC16 mode is selected. Hardware will auto-set init state of||
|||CRC_SEED to 0000_0000h. However, for CRC16-CCITT software will||
|||need to write the init state of FFFF_FFFFh to CRC_SEED. Note: The||
|||CRC16 result value is only 16-bits.||
|||1: CRC32 mode is selected. Hardware will auto-set init state of||
|||CRC_SEED will be FFFF_FFFFh.||
|||bit [1] CRC_32B_NOT_EMPTY:||
|||0: CRC 32Byte buffer is empty||
|||1: CRC 32Byte buffer is not empty||
|||bit [2] CRC16_MOD_ENABLE:||
|||0: CRC16 (x16+x15+x2+1 )||
|||1: CRC16-CCITT (x16+x12+x5+1 ) - Note: CRC32_ENABLE field must =||
|||0.||
|CRC_DATA_8_BFLIP|R|8-bit flip of CRC_DATA. CRC_DATA_8_BFLIP has the same byte order|R27|
|||as CRC_DATA[31-0], but each byte has all bits flipped.||
|||CRC_DATA_32_FLIP[7-0] = CRC_DATA[0-7]||
|||CRC_DATA_32_FLIP[15-8] = CRC_DATA[8-15]||
|||CRC_DATA_32_FLIP[23-16] = CRC_DATA[16-23]||
|||CRC_DATA_32_FLIP[31-24] = CRC_DATA[24-31]||
|||For CRC16, only CRC_DATA_8_BFLIP[15-0] are valid. No auto reset||
|||on CRC_DATA_8_BFLIP read.||
|CRC_SEED|W|CRC SEED value.|R28|
|||Hardware will auto-initialize the CRC_SEED value to 0000_0000h for||
|||CRC16 and FFFF_FFFFh for CRC32. Software only needs to initialize||
|||CRC_SEED if a different default value is required. For CRC16-CCITT,||
|||software needs to update initial CRC_SEED value to FFFF_FFFFh.||
|||Always write 4 bytes.||
|||Note: Reading the CRC_DATA register will reset the CRC value to the||
|||CRC_SEED state.||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

415 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-59. CRC Register to PRU Port Mapping (continued)** 

|**CRC Register**|**R/W**|**Description**|**PRU Mapping**|
|---|---|---|---|
|CRC_DATA_32_BFLIP|R|Full 32-bit flip of CRC_DATA|R28|
|||CRC_DATA_32_BFLIP[0] = CRC_DATA[31] …||
|||CRC_DATA_32_BFLIP[31] = CRC_DATA[0]||
|||For CRC16, only CRC_DATA_32_BFLIP[31-16] are valid.||
|||No auto reset on CRC_DATA_32_BFLIP read.||
|CRC_DATA|RW|For Write, must use a fixed width throughout the session. The CRC|R29|
|||module supports lower 8-bit, or lower 16-bit, or full 32-bit data widths.||
|||For Read, LSB or CRC_DATA[0] is first bit on the wire.||
|||For Read, reset the CRC_DATA back to CRC_SEED state.||
|||Note: Firmware must add 1 to 2 NOPs after the last XOUT to the XIN.||
|||For CRC16, only CRC_DATA[15-0] is valid.||



## _**7.3.6.2.2.2 CRC Programming Model**_ 

The following steps are performed by the PRU firmware to use the CRC module: 

## **Step1: Configuration (optional)** 

1. Configure CRC type: For CRC32 operation, set CRC32_ENABLE using XOUT instruction with the following parameters: 

   - Device ID = 1 

   - Base register = R25 

   - Size = 1 

2. Update CRC_SEED, if required using XOUT with the following parameters: 

   - Device ID = 1 

   - Base register = R28 

   - Size = 1 to 4 

## **Step 2:** 

1. Load new CRC data into R29 

2. Push CRC data to the CRC16/32 module using XOUT with the following parameters: 

   - Device ID = 1 

   - Base register = R29 

   - Size = 1 to 4 

3. 1 or 2 NOPS 

4. Load the accumulated CRC result into the PRU using the XIN instruction with the following parameters: 

   - Device ID = 1 

   - Base register = R29 

   - Size = 4 

Repeat Step 2, numbers 1 and 2 for each new CRC data. 

## **Note** 

When a session starts, the PRU firmware must use the same write data width throughout the session. 

## _**7.3.6.2.2.3 PRU and CRC16/32 Interface (R9:R2)**_ 

The PRU-ICSS system implements a new wide 32-Bytes data path. The firmware can perform one XOUT of 32-Bytes, the hardware will feed the CRC16/32 4-Bytes at a time. This will take 20 clock cycles for CRC16 and 12 clock cycles for CRC32 for a 32-Bytes XOUT. 

**Table 7-60. PRU Register to XFR Mapping** 

||**PRU Register**|**XFR ID**|**Domain/Function**|**Description**|
|---|---|---|---|---|
|R9:R2|Data|1|Data|XOUT Only|



416 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-60. PRU Register to XFR Mapping (continued)** 

|**PRU Register**|**XFR ID**|**Domain/Function**|**Description**|
|---|---|---|---|
||||1-Byte to 32-Bytes in size|
||||LSB packed and no gaps, for example:|
||||32-Bytes push R9:R2|
||||16-Bytes push R5:R2|
||||4-Bytes push R2|
||||7-Bytes push R3(b2.b0):R2|
||||1-Bytes push R2(b0)|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

417 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.6.2.3 PRU-ICSS Scratch Pad Memory**_ 

The PRU-ICSS supports a scratch pad with up to four independent banks accessible by the PRU cores. The PRU cores interact with the scratch pad through broadside load/store PRU interface and XFR instructions. The scratch pad can be used as a temporary place holder for the register contents of the PRU. 

## _**7.3.6.2.3.1 PRU0/1 Scratch Pad Overview**_ 

The PRU-ICSS scratch pad supports the following features: 

- PRU0 and PRU1 cores have three Scratch Pad banks of 30, 32-bit registers (R29 to R0) 

- Flexible load/store options: 

   - Load/store one byte of R<n> or load/store (R29 to R0) to Bank0, Bank1, Bank2 or Bank3 

   - User-defined start byte and length of the transfer 

   - Length of transfer ranges from one byte of a register to the entire register content (R29 to R0) 

   - Simultaneous transaction supported between PRU0 <-> Bank<n> and PRU1 <-> Bank<m> 

- XFR (XIN/XOUT/XCHG) instructions operate in one clock cycle 

- Optional XIN/XOUT shift functionality allows remapping of registers (R<n> -> R<m>) during load store operation 

Figure 7-44 shows a simplified model of the Scratch Pad and PRU cores integration. 

**==> picture [432 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Scratch-Pad Memory (SPAD)<br>Bank0<br>R0<br>R1<br>R2<br>…<br>R28<br>R29<br>PRU0 PRU1<br>Bank1<br>R0 R0<br>R1 R0 R1<br>R2 R1 R2<br>… R2 …<br>R28 … R28<br>R29 R28 R29<br>R29<br>Bank2<br>R0<br>R1<br>R2<br>…<br>R28<br>R29<br>broadside interface broadside interface<br>**----- End of picture text -----**<br>


**==> picture [31 x 7] intentionally omitted <==**

**----- Start of picture text -----**<br>
icss-025<br>**----- End of picture text -----**<br>


**Figure 7-44. Scratch Pad and PRU Integration** 

## _**7.3.6.2.3.2 PRU0 /1 Scratch Pad Operations**_ 

XFR instructions are used to load/store register contents between the PRU cores and the scratch pad banks. These instructions define the start, size, direction of the operation, and device ID. The device ID corresponds to the external source or destination (either a scratch pad bank or the other PRU core). The device ID numbers are shown in Table 7-61. 

**Table 7-61. Scratch Pad XFR ID** 

|**Device ID**|**Function/Operation**|
|---|---|
|10|Selects Bank0|
|11|Selects Bank1|



418 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **Table 7-61. Scratch Pad XFR ID (continued)** 

|**Device ID**|**Function/Operation**|
|---|---|
|12|Selects Bank2|



A collision occurs when two XOUT commands simultaneously access the same asset or device ID. Table 7-62 shows the priority assigned to each operation when a collision occurs. 

**Table 7-62. Scratch Pad XFR Collision and Stall Conditions** 

|**Operation**|**Collision and Stall Handling**|
|---|---|
|PRU<n> XOUT (->) bank[j]|If both PRU cores access the same bank simultaneously, PRU0 is given<br>priority. PRU1 will temporarily stall until the PRU0 operation completes.|



## _**7.3.6.2.3.2.1 Optional XIN/XOUT Shift**_ 

The optional XIN/XOUT shift functionality allows register contents to be remapped or shifted within the destination’s register space. For example, the contents of PRU0 R6-R8 could be remapped to Bank1 R10-12. 

The shift feature is enabled or disabled through the PRU subsystem level register PRU_ICSS_SPP_REG[1] XFR_SHIFT_EN bit. When enabled, R0[4-0] (internal to the PRU) defines the number of 32-bit registers in which content is shifted in the scratch pad bank. Note that scratch pad banks do not have registers R30 or R31. 

## _**7.3.6.2.3.2.2 Scratch Pad Operations Examples**_ 

The following PRU firmware examples demonstrate the shift functionality. Note: These assume the XFR_SHIFT_EN bit of the PRU_ICSS_SPP_REG register of the PRU-ICSS CFG register space has been set. 

## **XOUT Shift By 4 Registers** 

Store R4:R7 to R8:R11 in Bank0: 

- Load 4 into R0.b0 

- XOUT using the following parameters: 

   - Device ID = 10 

   - Base register = R4 

   - Size = 16 

## **XOUT Shift By 9 Registers, With Wrap Around** 

Store R25:R29 to R4:R9 in Bank1: 

- Load 9 into R0.b0 

- XOUT using the following parameters: 

   - Device ID = 11 

   - Base register = R25 

   - Size = 20 

## **XIN Shift By 10 Registers** 

Load R14:R16 from Bank2 to R4:R6: 

- Load 10 into R0.b0 

- XIN using the following parameters: 

   - Device ID = 12 

   - Base register = R4 

   - Size = 12 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

419 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.3.6.3 PRU-ICSS Data Movement Accelerators Functional** 

## _**7.3.6.3.1 PRU-ICSS XFR2VBUS Hardware Accelerator**_ 

The PRU core can write and read data packets to and from port queues, located in the MSMC SRAM into PRU core registers via XFR2VBUS hardware accelerator. Each of the PRU-ICSS Slices has implemented two RX XFR2VBUS hardware accelerators. 

**==> picture [261 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRUSSn CBASS0<br>SLICEn<br>PRUn<br>(Core CPUn)<br>(16KB IRAM) XFR2VBUSP P/M<br>RX/RD<br>pruss-005<br>**----- End of picture text -----**<br>


1. n reprsents a valid instance of PRU in a domain. 

## **Figure 7-45. XFR2VBUS Hardware Accelerator** 

Supported features: 

- 2 x XFR2VBUS RX threads 

XFR2VBUS RX buffer features: 

- 1 x 64 Byte deep RX/Read buffer 

   - 4 Byte, 32 Byte, or 64 Byte read size per RD (read) command 

   - Optional automatic read command with incrementing address on pop of read data 

   - 32 Byte optimization mode available 

The ownership of commands and data is flexible. The XFR2VBUS accelerator is shared between PRU cores. Status is available to both cores. 

Note: The ownership should be preplanned and static per use model. 

The XFR2VBUS is a simple hardware accelerator wich is used to get the lowest read round trip latency from MSMC and to decouple the latency seen by the PRU. Each XFR2VBUS instance is connected to the CBASS0. 

The PRU-ICSS system has a total of 2 XFR2VBUS RX hardware accelerators. 

## _**7.3.6.3.1.1 Blocking Conditions**_ 

The only blocking condition is caused when the VBUSM command/data FIFO is full. It is required that the external bandwidth is very high. All egress commands and data should get sent without head of line blocking. Based on arbitration some delay is possible. 

## _**7.3.6.3.1.2 Read Operation with Auto Disabled**_ 

The XFR2VBUS supports 1 command in its command FIFO, 1 XOUT to define the address and size (4 Byte, 32 Byte, 64 Byte, aligned). This will cause the VBUSP read command to be issued. Only 1 read command can be in flight. The read address defines the offset of the 64 Byte of read data. The read size defines the size of the transfer, 4 Byte, 32 Byte, 64 Byte, aligned Offset + size must be aligned to 32 Byte width of the bus. 1 XIN, the software can see the status of command FIFO and read data FIFO. 

Note: XIN of the read data will fully pop the data, independent of XIN size. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

420 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.6.3.1.3 Read Operation with Auto Enabled**_ 

The same features as Auto Disabled are valid with the following exceptions: 

64 Byte mode: 

- Address needs to be MOD 0x40/64 Byte aligned 

- Size needs to be 64 Byte 

- 1 XOUT to define the start address, which needs to be MOD 0x40/64 Byte aligned 

- The XFR2VBUS will issue 1 new command every time this is 64 Bytes available in the read data FIFO 

- 1 XIN of read data will cause a new command to be issued since, 64 Bytes are available 

- To stop the issuing new read commands, disable auto mode 

32 Byte mode: 

- Size needs to be 32 Byte 

- 1 XOUT to define the start address, which needs to be MOD 0x20/32 Byte aligned 

- The XFR2VBUS will issue 1 new command every time this is 32 Bytes available in the read data FIFO 

- 1 XIN of read data will cause a new command to be issued since, 32 Bytes are available 

- To stop the issuing of new read command, disable auto mode 

Note: XIN of the read data will fully pop the data, independent of XIN size. 

## _**7.3.6.3.1.4 PRU to XFR2VBUS Interface**_ 

RD_ID0 = 0x60 

RD_ID1 = 0x61 

**Table 7-63. Read Commands** 

|**PRU Register**|**BS ID**|**Access Type**|**Register**|**Notes**|
|---|---|---|---|---|
|R17-R2|RD_ID1/0|XIN|RD_DATA|Read Data|
|R18[0]|RD_ID1/0|XOUT|RD_AUTO|Read Auto Mode<br>If 0 -> 1, must write RD_ADDR<br>If 1 -> 0, must not write<br>RD_ADDR,<br>must drain RD_DATA/RD_CMD<br>If 0 -> 0, must write RD_ADDR<br>When set, every RD_DATA pop<br>will cause a new read command<br>and read address to increment by<br>0x20 for the next read command<br>if size is set to 32 Bytes<br>0x40 for the next read command<br>if size is set to 64 Bytes<br>In this case, user must set the<br>address to be ether mod 0x20 or<br>0x40.<br>4 Byte mode is not supported.|
|R18[2-1]|RD_ID1/0|XOUT|RD_SIZE|Read Size<br>0h: 4 Bytes<br>1h: Reserved<br>2h: 32 Bytes<br>3h: 64 Bytes|
|R18[0]|RD_ID1/0|XIN|RD_BUSY|Read Busy Status<br>0h: Idle<br>1h: Active<br>(RD CMD FIFO LEVEL !=0) or<br>(RD DATA FIFO LEVEL !=0)|
|R18[1]|RD_ID1/0|XIN|RD_CMD_FL|Read command FIFO Level<br>0h: Empty<br>1h: Occupied<br>Note: It only pop the read<br>command FIFO after the read<br>data has arrived|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 421 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-63. Read Commands (continued)** 

|**PRU Register**|**BS ID**|**Access Type**|**Register**|**Notes**|
|---|---|---|---|---|
|R18[2]|RD_ID1/0|XIN|RD_DATA_FL|Read data FIFO Level<br>0h: Empty<br>1h: Occupied 32 byte or 64 byte<br>Note: In 64 byte mode, the user<br>must wait for RD_MST_REQ = 0h<br>before reading the FIFO.|
|R18[3]|RD_ID1/0|XIN|RD_MST_REQ|RD MST RED<br>0h = Last data has been latched<br>1h = Last data is still in flight<br>Note: In Auto mode, the user<br>must insure that this bit is 0h<br>and wait an additional NOP<br>before user disables Auto mode<br>to prevent a race condition.|
|R20:R19|RD_ID1/0|XOUT|RD_ADDR|Read address 48-bits<br>0x20 for the next read command<br>if size is set to 32 Bytes<br>0x40 for the next read command<br>if size is set to 64 Bytes<br>The address can be the full 48-<br>bits or just the lower 32-bits of<br>the address, it will use the current<br>state of the upper 16-bits|



## _**7.3.6.3.1.5 XFR2VBUS Programming Model**_ 

Read: 

- Wait RD_BUSY = 0h 

- XOUT R18 (configure RD_AUTO/ RD_SIZE); R19 (RD_ADDR) 

- Wait WR_BUSY = 0h OR RD_DATA_FL = 1h 

- XIN RD_DATA (Repeat if RD_AUTO is enabled and need new RD_DATA, must always check RD_DATA_FL before XIN RD_DATA) 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

422 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.7 PRU-ICSS Local INTC**_ 

The PRU-ICSS interrupt controller (INTC) maps interrupts coming from different parts of the device (mapped to PRU-ICSS) to a reduced set of PRU-ICSS interrupt channels. 

The interrupt controller has the following features: 

- Capturing up to 64 System Events (inputs): 

- Supports up to 10 output interrupt channels. 

- Generation of 10 Host Interrupts 

   - 2 Host Interrupts shared between the PRUs (PRU0 and PRU1). 

   - 8 Host Interrupts exported from the PRU-ICSS internal INTC for signaling the device level interrupt controllers (pulse and level provided). 

- Each event can be enabled and disabled. 

- Each host event can be enabled and disabled. 

- Hardware prioritization of events. 

## **7.3.7.1 PRU-ICSS Interrupt Controller Functional Description** 

The PRU-ICSS INTC supports up to 64 interrupts from different peripherals and PRUs. The INTC maps these events to 10 channels inside the INTC (see Figure 7-46). Interrupts from these 10 channels are further mapped to 10 Host Interrupts. 

- Any of the 64 internal interrupts can be mapped to any of the 10 channels. 

- Multiple interrupts can be mapped to a single channel. 

- An interrupt should not be mapped to more than one channel. 

- Any of the 10 channels can be mapped to any of the 10 host interrupts. It is recommended to map channel “x” to host interrupt “x”, where x is from 0 to 9. 

- A channel should not be mapped to more than one host interrupt 

- For channels mapping to the same host interrupt, lower number channels have higher priority. 

- For interrupts on same channel, priority is determined by the hardware interrupt number. The lower the interrupt number, the higher the priority. 

- Host Interrupt 0 is connected to bit 30 in register 31 (R31) of PRU0 and PRU1 in parallel. 

- Host Interrupt 1 is connected to bit 31 in register 31 (R31) for PRU0 and PRU1 in parallel. 

- Host Interrupts 2 through 9 exported from PRU-ICSS and mapped to device level interrupt controllers. 

**==> picture [442 x 242] intentionally omitted <==**

**----- Start of picture text -----**<br>
Host mapping of channels Channel mapping of system events<br>PRU0/1 Sys_event 1<br>R31 bit 30 Host-0 Channel-0<br>Sys_event 2 Peripheral A<br>PRU0/1 Host-1 Channel-1<br>R31 bit 30<br>Host-2 Channel-2<br>Host-3 Channel-3<br>Host-4 Channel-4<br>Host-5 Channel-5 Sys_event 30<br>pr<n>_host<7:0><br>_intr_pend Sys_event 31<br>Exported Host-6 Channel-6<br>Host-7 Channel-7 Sys_event 34<br>Host-8 Channel-8<br>Peripheral Z<br>Host-9 Channel-9<br>Sys_event 58<br>**----- End of picture text -----**<br>


**Figure 7-46. PRU-ICSS Interrupt Controller Block Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

423 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.7.1.1 PRU-ICSS Interrupt Controller System Events Flow**_ 

The ICSS_INTC module controls the event mapping to the host interrupt interface. Events are generated by the device peripherals or PRUs. The INTC receives the internal interrupts and maps them to internal channels. The channels are used to group interrupts together and to prioritize them. These channels are then mapped onto the host interrupts. Interrupts from the system side are active high in polarity. 

The INTC encompasses many functions to process the system interrupts and prepare them for the host interface. These functions are: processing, enabling, status, channel mapping, host interrupt mapping, prioritization, and host interfacing. Figure 7-47 illustrates the flow of interrupts through the functions to the host. The following subsections describe each part of the flow. 

**==> picture [292 x 135] intentionally omitted <==**

**----- Start of picture text -----**<br>
Status Enabling Processing Interrupts<br>Prioritization<br>Channel Debug Debug Ints<br>Vectorization Int<br>Mapping<br>Host Int Host<br>Host Ints<br>Mapping Interfacing<br>icss-012<br>**----- End of picture text -----**<br>


**Figure 7-47. Flow of System Interrupts to Host** 

## _**7.3.7.1.1.1 PRU-ICSS Interrupt Processing**_ 

This block does following tasks: 

- Synchronization of slower and asynchronous interrupts 

- Conversion of polarity to active high 

- Conversion of interrupt type to pulse interrupts 

After the processing block, all interrupts will be active high pulses. 

## _**7.3.7.1.1.1.1 PRU-ICSS Interrupt Enabling**_ 

The next stage of INTC is to enable interrupts based on programmed settings. The following sequence has to be followed to enable interrupts: 

- Enable required interrupts: System interrupts that are required to get propagated to host are to be enabled individually by writing to [9-0] ENABLE_SET_INDEX bit field in the interrupt enable indexed set register (ICSS_INTC_ENABLE_SET_INDEX_REG). The interrupt to enable is the index value written. This sets the Enable Register bit of the given index. 

- Enable required host interrupts: By writing 1h to the appropriate bit of the [9-0] HINT_ENABLE_SET_INDEX bit field in the host interrupt enable indexed set register (ICSS_INTC_HINT_ENABLE_SET_INDEX_REG), enable the required host interrupts. The host interrupt to enable is the index value written. This enables the host interrupt output or triggers the output again if that host interrupt is already enabled. 

- Enable all host interrupts: By setting the [0] ENABLE_HINT_ANY bit in the global enable register (ICSS_INTC_GLOBAL_ENABLE_HINT_REG) to 1h, all host interrupts will be enabled. Individual host interrupts are still enabled or disabled from their individual enables and are not overridden by the global enable. 

## _**7.3.7.1.1.2 PRU-ICSS Interrupt Status Checking**_ 

The next stage is to capture which interrupts are pending. There are two kinds of pending status: raw status and enabled status. Raw status is the pending status of the interrupt without regards to the enable bit for the interrupt. Enabled status is the pending status of the interrupts with the enable bits active. When the enable bit 

424 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

is inactive, the enabled status will always be inactive. The enabled status of interrupts is captured in interrupt status enabled/clear registers (ICSS_INTC_ENA_STATUS_REG0 to ICSS_INTC_ENA_STATUS_REG4). 

Status of interrupt 'N' is indicated by the N-th bit of ICSS_INTC_ENA_STATUS_REG0 to ICSS_INTC_ENA_STATUS_REG4. Since there are 160 interrupts, five 32-bit registers are used to capture the enabled status of interrupts. The pending status reflects whether the interrupt occurred since the last time the status register bit was cleared. Each bit in the status register can be individually cleared. 

## _**7.3.7.1.1.3 PRU-ICSS Interrupt Channel Mapping**_ 

The INTC has 10 internal channels to which enabled interrupts can be mapped. Channel 0 has highest priority and channel 9 has the lowest priority. Channels are used to group the interrupts into a smaller number of priorities that can be given to a host interface with a very small number of interrupt inputs. 

When multiple interrupts are mapped to the same channel their interrupts are ORed together so that when either is active the output is active. The channel map registers (ICSS_INTC_CH_MAP_REGi) define the channel for each interrupt. There is one register per 4 interrupts; therefore, there are 16 channel map registers for a of 64 interrupts. The channel for each interrupt can be set using these registers. 

## _**7.3.7.1.1.3.1 PRU-ICSS Host Interrupt Mapping**_ 

The hosts can be the local PRU processors (PRU0 and PRU1) as well as device processors located outside PRU-ICSS such as ARM, etc. The 10 channels from the INTC can be mapped to any of the 10 Host interrupts. The Host map registers (ICSS_INTC_HINT_MAP_REG0 to ICSS_INTC_HINT_MAP_REG4) define the channel for each interrupt. There is one register per 4 channels; therefore, there are 3 host map registers for 10 channels. When multiple channels are mapped to the same host interrupt, then prioritization is done to select which interrupt is in the highest-priority channel and which should be sent first to the host. 

## _**7.3.7.1.1.3.2 PRU-ICSS Interrupt Prioritization**_ 

The next stage of the INTC is prioritization. Since multiple interrupts can feed into a single channel and multiple channels can feed into a single host interrupt, it is necessary to read the status of all interrupts to determine the highest priority interrupt that is pending. The INTC provides hardware to perform this prioritization with a given scheme so that software does not have to do this. There are two levels of prioritizations: 

- The first level of prioritization is between the active channels for a host interrupt. Channel 0 has the highest priority and channel 9 has the lowest. So the first level of prioritization picks the lowest numbered active channel. 

- The second level of prioritization is between the active interrupts for the prioritized channel. The interrupt in position 0 has the highest priority and interrupt 159 has the lowest priority. So the second level of prioritization picks the lowest position active interrupt. 

This is the final prioritized interrupt for the host interrupt and is stored in the global prioritized innterrupt register (ICSS_INTC_GLB_PRI_INTR_REG). The highest priority pending interrupt with respect to each host interrupts can be obtained using the host interrupt prioritized interrupt registers (ICSS_INTC_PRI_HINT_REGj where j = 0 to 19). 

## _**7.3.7.1.1.4 PRU-ICSS Interrupt Nesting**_ 

The INTC can also perform a nesting function in its prioritization. Nesting is a method of disabling certain interrupts (usually lower-priority interrupts) when an interrupt is taken so that only those desired interrupts can trigger to the host while it is servicing the current interrupt. The typical usage is to nest on the current interrupt and disable all interrupts of the same or lower priority (or channel). Then the host will only be interrupted from a higher priority interrupt. 

The nesting is done in one of three methods: 

1. Nesting for all host interrupts, based on channel priority: When an interrupt is taken, the nesting level is set to its channel priority. From then, that channel priority and all lower priority channels will be disabled from generating host interrupts and only higher priority channels are allowed. When the interrupt is completely serviced, the nesting level is returned to its original value. When there is no 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 425 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

interrupt being serviced, there are no channels disabled due to nesting. The global nesting level register (ICSS_INTC_GLB_NEST_LEVEL_REG) allows the checking and setting of the global nesting level across all host interrupts. The nesting level is the channel (and all of lower priority channels) that are nested out because of a current interrupt. 

2. Nesting for individual host interrupts, based on channel priority: Always nest based on channel priority for each host interrupt individually. When an interrupt is taken on a host interrupt, then, the nesting level is set to its channel priority for just that host interrupt, and other host interrupts do not have their nesting affected. Then for that host interrupt, equal or lower priority channels will not interrupt the host but may on other host interrupts if programmed. When the interrupt is completely serviced the nesting level for the host interrupt is returned to its original value. The host interrupt nesting level registers (ICSS_INTC_NEST_LEVEL_REGj where j = 0 to 19) display and control the nesting level for each host interrupt. The nesting level controls which channel and lower priority channels are nested. There is one register per host interrupt. 

3. Software manually performs the nesting of interrupts. When an interrupt is taken, the software will disable all the host interrupts, manually update the enables for any or all the interrupts, and then re-enables all the host interrupts. This now allows only the interrupts that are still enabled to trigger to the host. When the interrupt is completely serviced the software must reverse the changes to re-enable the nested out interrupts. This method requires the most software interaction but gives the most flexibility if simple channel based nesting mechanisms are not adequate. 

## _**7.3.7.1.1.5 PRU-ICSS Interrupt Status Clearing**_ 

After servicing the interrupt (after execution of the ISR), interrupt status is to be cleared. If a interrupt status is not cleared, then another host interrupt may not be triggered or another host interrupt may be triggered incorrectly. It is also essential to clear all interrupts before the PRU is halted as the PRU does not power down unless all the interrupt status are cleared. For clearing the status of an interrupt, whose interrupt number is N, write a 1h to the Nth bit position in the interrupt status enabled/clear registers (ICSS_INTC_ENA_STATUS_REG0 to ICSS_INTC_ENA_STATUS_REG4). Interrupt N can also be cleared by writing the value N into the interrupt status indexed clear register (ICSS_INTC_STATUS_CLR_INDEX_REG). 

## _**7.3.7.1.2 PRU-ICSS Interrupt Disabling**_ 

At any time, if any interrupt is not to be propagated to the host, then that interrupt should be disabled. For disabling an interrupt whose interrupt number is N, write a 1h to the Nth bit in the interrupt enable clear registers (ICSS_INTC_ENABLE_CLR_REG0 to ICSS_INTC_ENABLE_CLR_REG4). Interrupt N can also be disabled by writing the value N in the interrupt enable clear index register (ICSS_INTC_ENABLE_CLR_INDEX_REG). 

## **7.3.7.2 PRU-ICSS Interrupt Controller Basic Programming Model** 

Follow these steps to configure the interrupt controller. 

1. Set polarity and type of event through the Interrupt Polarity Registers (ICSS_INTC_POLARITY_REG0 to ICSS_INTC_POLARITY_REG4) and the Interrupt Type Registers (ICSS_INTC_POLARITY_REG0 to ICSS_INTC_POLARITY_REG4). Polarity of all interrupts is always high. Type of all interrupts is always pulse (after the processing block). 

2. Map event to INTC channel through ICSS_INTC_CH_MAP_REGi (where i=0 to 39) channel mapping registers. 

3. Map channel to host interrupt through ICSS_INTC_HINT_MAP_REG0 to ICSS_INTC_HINT_MAP_REG4 registers. Recommended channel “x” to be mapped to host interrupt “x”. 

4. Clear interrupt by writing 1h to ICSS_INTC_ENA_STATUS_REG0 to ICSS_INTC_ENA_STATUS_REG4 registers. 

5. Enable host interrupt by writing index value to ICSS_INTC_HINT_ENABLE_SET_INDEX_REG register. 6. Enable interrupt nesting if desired. 

7. Globally enable all interrupts through register ICSS_INTC_GLOBAL_ENABLE_HINT_REG[0] ENABLE_HINT_ANY bit. 

426 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.3.7.3 PRU-ICSS Interrupt Requests Mapping** 

The PRU-ICSS Interrupt Controller lines 0 through 31 are mapped to internal events which are generated by PRU-ICSS integrated modules. Lines 32 to 63 can be external and generated from different peripherals or internally generated by the PRU-ICSS integrated modules. An internal MUX routes the signals to be internal or external, and is controlled by the select bit MII_RT_REG.MII_RT_EVENT_EN. Table 7-64 shows mapping of the different PRU-ICSS internally sourced IRQ events to PRU-ICSS INTC interrupt lines 0 through 63. 

**Table 7-64. PRU-ICSS IP Interrupts** 

|**Event Number**|**Source**|**Source**|
|---|---|---|
||**MII_RT_REG.MII_RT_EVENT_EN =1 mode (default)**<br>**(Internally Generated)**<br>**MII_RT_REG .MII_RT_EVENT_EN =0 mode**<br>**(Externally Generated)**||
||**PRU-ICSS INTC**||
|63:56|pr1_slv_intr[63:56]_intr_pend(external)|pr1_slv_intr[63:56]_intr_pend(external)|
|55|pr1_mii1_col & pr1_mii1_txen (external)|pr1_slv_intr[55]_intr_pend(external)|
|54|PRU1_RX_EOF|pr1_slv_intr[54]_intr_pend(external)|
|53|MDIO_MII_LINK[1]|pr1_slv_intr[53]_intr_pend(external)|
|52|PORT1_TX_OVERFLOW|pr1_slv_intr[52]_intr_pend(external)|
|51|PORT1_TX_UNDERFLOW|pr1_slv_intr[51]_intr_pend(external)|
|50|PRU1_RX_OVERFLOW|pr1_slv_intr[50]_intr_pend(external)|
|49|PRU1_RX_NIBBLE_ODD|pr1_slv_intr[49]_intr_pend(external)|
|48|PRU1_RX_CRC|pr1_slv_intr[48]_intr_pend(external)|
|47|PRU1_RX_SOF|pr1_slv_intr[47]_intr_pend(external)|
|46|PRU1_RX_SFD|pr1_slv_intr[46]_intr_pend(external)|
|45|PRU1_RX_ERR32|pr1_slv_intr[45]_intr_pend(external)|
|44|PRU1_RX_ERR|pr1_slv_intr[44]_intr_pend(external)|
|43|pr0_mii0_col and<br>pr0_mii0_txen (external)|pr1_slv_intr[43]_intr_pend(external)|
|42|PRU0_RX_EOF|pr1_slv_intr[42]_intr_pend(external)|
|41|MDIO_MII_LINK[0]|pr1_slv_intr[41]_intr_pend(external)|
|40|PORT0_TX_OVERFLOW|pr1_slv_intr[40]_intr_pend(external)|
|39|PORT0_TX_UNDERFLOW|pr1_slv_intr[39]_intr_pend(external)|
|38|PRU0_RX_OVERFLOW|pr1_slv_intr[38]_intr_pend(external)|
|37|PRU0_RX_NIBBLE_ODD|pr1_slv_intr[37]_intr_pend(external)|
|36|PRU0_RX_CRC|pr1_slv_intr[36]_intr_pend(external)|
|35|PRU0_RX_SOF|pr1_slv_intr[35]_intr_pend(external)|
|34|PRU0_RX_SFD|pr1_slv_intr[34]_intr_pend(external)|
|33|PRU0_RX_ERR32|pr1_slv_intr[33]_intr_pend(external)|
|32|PRU0_RX_ERR|pr1_slv_intr[32]_intr_pend(external)|
|31:16|pr1_pru_mst_intr[15:0]_intr_req||
|15|pr1_ecap_intr_req||
|14|sync0_out_pend||
|13|sync1_out_pend||
|12|pr0_latch0_in (input to PRU-ICSS)||
|11|pr0_latch1_in (input to PRU-ICSS)||
|10|pr0_pdi_wd_exp_pend||
|9|pr0_pd_wd_exp_pend||
|8|pr0_digio_event_req||
|7|pr0_iep_tim_cap_cmp_pend||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 427 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Table 7-64. PRU-ICSS IP Interrupts (continued)** 

|**Event Number**|**Source**|**Source**|
|---|---|---|
||**MII_RT_REG.MII_RT_EVENT_EN =1 mode (default)**<br>**(Internally Generated)**<br>**MII_RT_REG .MII_RT_EVENT_EN =0 mode**<br>**(Externally Generated)**||
|6|pr0_uart0_uint_intr_req||
|5|pr0_uart0_utxevt_intr_req||
|4|pr0_uart0_urxevt_intr_req||
|3|reset_iso_req||
|2|pr0_pru1_r31_status_cnt16||
|1|pr0_pru0_r31_status_cnt16||
|0|pr0_ecc_err_intr||



## **Table 7-65. AM263Px-Specific PRU-ICSS Interrupt Mapping** 

|**Event Number**|**Source**|**Source**|
|---|---|---|
||**MII_RT_REG.MII_RT_EVENT_EN =1 mode**<br>**(default)**<br>**MII_RT_REG .MII_RT_EVENT_EN =0 mode**||
||**PRU-ICSS INTC**||
|63|CONTROLSS Output XBAR[15]||
|62|CONTROLSS Output XBAR[14]||
|61|CONTROLSS Output XBAR[13]||
|60|CONTROLSS Output XBAR[12]||
|59|CONTROLSS Output XBAR[11]||
|58|CONTROLSS Output XBAR[10]||
|57|CONTROLSS Output XBAR[9]||
|56|CONTROLSS Output XBAR[8]||
|55|pr0_mii1_col and<br>pr0_mii1_txen (external)|CONTROLSS Output XBAR[7]|
|54|PRU0_RX_EOF|CONTROLSS Output XBAR[6]|
|53|MDIO_MII_LINK[1]|CONTROLSS Output XBAR[5]|
|52|PORT0_TX_OVERFLOW|CONTROLSS Output XBAR[4]|
|51|PORT0_TX_UNDERFLOW|CONTROLSS Output XBAR[3]|
|50|PRU0_RX_OVERFLOW|CONTROLSS Output XBAR[2]|
|49|PRU0_RX_NIBBLE_ODD|CONTROLSS Output XBAR[1]|
|48|PRU0_RX_CRC|CONTROLSS Output XBAR[0]|
|47|PRU0_RX_SOF|PRU-ICSS XBAR INTR[15]|
|46|PRU0_RX_SFD|PRU-ICSS XBAR INTR[14]|
|45|PRU0_RX_ERR32|PRU-ICSS XBAR INTR[13]|
|44|PRU0_RX_ERR|PRU-ICSS XBAR INTR[12]|
|43|pr0_mii0_col and<br>pr0_mii0_txen (external)|PRU-ICSS XBAR INTR[11]|
|42|PRU0_RX_EOF|PRU-ICSS XBAR INTR[10]|
|41|MDIO_MII_LINK[0]|PRU-ICSS XBAR INTR[9]|
|40|PORT0_TX_OVERFLOW|PRU-ICSS XBAR INTR[8]|
|39|PORT0_TX_UNDERFLOW|PRU-ICSS XBAR INTR[7]|
|38|PRU0_RX_OVERFLOW|PRU-ICSS XBAR INTR[6]|
|37|PRU0_RX_NIBBLE_ODD|PRU-ICSS XBAR INTR[5]|
|36|PRU0_RX_CRC|PRU-ICSS XBAR INTR[4]|
|35|PRU0_RX_SOF|PRU-ICSS XBAR INTR[3]|
|34|PRU0_RX_SFD|PRU-ICSS XBAR INTR[2]|



428 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-65. AM263Px-Specific PRU-ICSS Interrupt Mapping (continued)** 

|**Event Number**|**Source**|**Source**|
|---|---|---|
||**MII_RT_REG.MII_RT_EVENT_EN =1 mode**<br>**(default)**<br>**MII_RT_REG .MII_RT_EVENT_EN =0 mode**||
|33|PRU0_RX_ERR32|PRU-ICSS XBAR INTR[1]|
|32|PRU0_RX_ERR|PRU-ICSS XBAR INTR[0]|
|31|pr0_pru_mst_intr[15]_intr_req||
|30|pr0_pru_mst_intr[14]_intr_req||
|29|pr0_pru_mst_intr[13]_intr_req||
|28|pr0_pru_mst_intr[12]_intr_req||
|27|pr0_pru_mst_intr[11]_intr_req||
|26|pr0_pru_mst_intr[10]_intr_req||
|25|pr0_pru_mst_intr[9]_intr_req||
|24|pr0_pru_mst_intr[8]_intr_req||
|23|pr0_pru_mst_intr[7]_intr_req||
|22|pr0_pru_mst_intr[6]_intr_req||
|21|pr0_pru_mst_intr[5]_intr_req||
|20|pr0_pru_mst_intr[4]_intr_req||
|19|pr0_pru_mst_intr[3]_intr_req||
|18|pr0_pru_mst_intr[2]_intr_req||
|17|pr0_pru_mst_intr[1]_intr_req||
|16|pr0_pru_mst_intr[0]_intr_req||
|15|pr0_ecap_intr_req||
|14|pr0_sync0_out_pend||
|13|pr0_sync1_out_pend||
|12|pr0_latch0_in (input to PRU-ICSS)||
|11|pr0_latch1_in (input to PRU-ICSS)||
|10|pr0_pdi_wd_exp_pend||
|9|pr0_pd_wd_exp_pend||
|8|pr0_digio_event_req||
|7|pr0_iep_tim_cap_cmp_pend||
|6|pr0_uart0_uint_intr_req||
|5|pr0_uart0_utxevt_intr_req||
|4|pr0_uart0_urxevt_intr_req||
|3|reset_iso_req||
|2|pr0_pru1_r31_status_cnt16||
|1|pr0_pru0_r31_status_cnt16||
|0|pr0_ecc_err_intr||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

429 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.8 PRU-ICSS UART Module**_ 

This section describes an Universal Asynchronous Receive and Transmit (UART) module integrated into the PRU-ICSS subsystem. Hereinafter the module will be referred as PRU-ICSS UART0. 

## **7.3.8.1 PRU-ICSS UART Overview** 

The PRU-ICSS UART0 peripheral is based on the industry standard TL16C550 asynchronous communications element, which in turn is a functional upgrade of the TL16C450. The information in this chapter assumes that user is familiar with these standards. 

Functionally similar to the TL16C450 on power up (single character or TL16C450 mode), the PRU-ICSS UART0 can be placed in an alternate FIFO (TL16C550) mode. This relieves the CPU of excessive software overhead by buffering received and transmitted characters. The receiver and transmitter FIFOs store up to 16 bytes including three additional bits of error status per byte for the receiver FIFO. 

The PRU-ICSS UART0 performs serial-to-parallel conversions on data received from a peripheral device and parallel-to-serial conversion on data received from the CPU. The CPU can read the PRU-ICSS UART0 status at any time. The PRU-ICSS UART0 includes control capability and a processor interrupt system that can be tailored to minimize software management of the communications link. 

The PRU-ICSS UART0 includes a programmable baud generator capable of dividing the PRU-ICSS UART0 input clock by divisors from 1 to 65535 and producing a 16× reference clock or a 13× reference clock for the internal transmitter and receiver logic. 

## **7.3.8.2 PRU-ICSS UART Environment** 

This section describes the PRU-ICSS UART0 module interface to the device environment. 

## _**7.3.8.2.1 PRU-ICSS UART Pin Multiplexing**_ 

Pin multiplexing is controlled using a combination of hardware configuration at device reset and software programmable register settings. For more information on the PRU-ICSS UART0 pin multiplexing, refer to the IO_MUX Registers chapter of the Register Addendum 

## _**7.3.8.2.2 PRU-ICSS UART Signal Descriptions**_ 

The PRU-ICSS UART0 utilize a minimal number of signal connections to interface with external devices. The PRU-ICSS UART0 signal descriptions are described in Table 7-66. 

**Table 7-66. PRU_ICSS_UART0 Signal Descriptions** 

|**Signal Name**|**Signal Type**|**Function**|
|---|---|---|
|UART0_TXD|Output|Serial data transmit|
|UART0_RXD|Input|Serial data receive|
|UART0_CTS|Input|Clear-to-Send handshaking signal|
|UART0_RTS|Output|Request-to-Send handshaking signal|



## _**7.3.8.2.3 PRU-ICSS UART Protocol Description and Data Format**_ 

## _**7.3.8.2.3.1 PRU-ICSS UART Transmission Protocol**_ 

The PRU-ICSS UART0 transmitter section includes a transmitter hold register (THR), memory mapped in the register UART_RBR_TBR[17-8] TBR_DATA bitfield and a transmitter shift register (TSR), which is NOT memory mapped. When the PRU-ICSS UART0 is in the FIFO mode, THR is a 16-byte FIFO. Transmitter section control is a function of the PRU-ICSS UART0 line control register UART_LCTR. Based on the settings chosen in this register, the PRU-ICSS UART0 transmitter sends the following to the receiving device: 

- 1 START bit 

- 5, 6, 7, or 8 data bits 

- 1 PARITY bit (optional) 

- 1, 1.5, or 2 STOP bits 

430 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

THR receives data from the internal data bus, and when TSR (transmitter shift register) is ready, the PRU-ICSS UART0 moves the data from THR to TSR. The PRU-ICSS UART0 serializes the data in TSR and transmits the data on the UART0_TXD pin. 

In the non-FIFO mode, if THR is empty and the Transmitter Holding Register Empty interrupt (THRE) is enabled in the interrupt enable register (UART_INT_EN[1] ETBEI), an interrupt is generated. This interrupt is cleared when a character is loaded into THR or the interrupt identification register UART_INT_FIFO bitfield [3-1] IIR_INTID is read. In the FIFO mode, the interrupt is generated when the transmitter FIFO is empty, and it is cleared when at least one byte is loaded into the FIFO or UART_INT_FIFO[3-1] IIR_INTID bitfield is read. 

## _**7.3.8.2.3.2 PRU-ICSS UART Reception Protocol**_ 

The PRU-ICSS UART0 receiver section includes a receiver shift register (RSR), that is not memory mapped, and a receiver buffer register (RBR), memory mapped as the register UART_RBR_TBR[7-0] RBR_DATA bitfield. When the PRU-ICSS UART0 is in the FIFO mode, RBR is a 16-byte FIFO. Receiver section control is a function of the PRU-ICSS UART0 line control register - UART_LCTR. Based on the settings chosen in this register, the PRU-ICSS UART0 receiver accepts the following from the transmitting device: 

- 1 START bit 

- 5, 6, 7, or 8 data bits 

- 1 PARITY bit (optional) 

- 1 STOP bit (any other STOP bits transferred with the above data are not detected) 

RSR receives the data bits from the UART0_RXD pin. Then RSR concatenates the data bits and moves the resulting value into RBR (or the receiver FIFO), accessible in the RBR_TBR[7-0] RBR_DATA register bitfield. The PRU-ICSS UART0 also stores three bits of error status information next to each received character, to record a parity error, framing error, or break. 

In the non-FIFO mode, when a character is placed in RBR and the receiver data available interrupt is enabled in the interrupt enable register - UART_INT_EN[0] ERBI, an interrupt is generated. This interrupt is cleared when the character is read from RBR. In the FIFO mode, the interrupt is generated when the FIFO is filled to the trigger level selected in the FIFO control MSB part of the register UART_INT_FIFO, and it is cleared when the FIFO contents drop below the trigger level. 

## _**7.3.8.2.3.3 PRU-ICSS UART Data Format**_ 

The PRU-ICSS UART0 transmits in the following format: 

1 START bit + data bits (5, 6, 7, 8) + 1 PARITY bit (optional) + STOP bit (1, 1.5, 2) 

It transmits 1 START bit; 5, 6, 7, or 8 data bits, depending on the data width selection; 1 PARITY bit, if parity is selected; and 1, 1.5, or 2 STOP bits, depending on the STOP bit selection. 

The PRU-ICSS UART0 receives in the following format: 

1 START bit + data bits (5, 6, 7, 8) + 1 PARITY bit (optional) + 1 STOP bit 

It receives 1 START bit; 5, 6, 7, or 8 data bits, depending on the data width selection; 1 PARITY bit, if parity is selected; and 1 STOP bit. 

The protocol formats are shown in Figure 7-48. 

## **Figure 7-48. PRU-ICSS UART Protocol Formats** 

Transmit/Receive for 5-bit data, parity Enable, 1 STOP bit 

D0 D1 D2 D3 D4 PARITY STOP1 

Transmit/Receive for 6-bit data, parity Enable, 1 STOP bit 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 431 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

D0 D1 D2 D3 D4 D5 PARITY STOP1 

Transmit/Receive for 7-bit data, parity Enable, 1 STOP bit 

||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|
|||D0|D1|D2|D3|D4|D5|D6|PARITY||
||||||||||||
|Transmit/Receive for 8-bit data, parity Enable, 1 STOP bit|||||||||||
||||||||||||
|||D0|D1|D2|D3|D4|D5|D6|D7|PARITY|
||||||||||||



## _**7.3.8.2.3.3.1 Frame Formatting**_ 

Character length is specified using the UART_LCTR[0] WLS0 and UART_LCTR[1] WLS1 bits (see Table 7-68). 

The number of stop-bits is specified using the UART_LCTR[2] STB bit (see Table 7-68). 

The parity bit is programmed using the UART_LCTR[5] SP, UART_LCTR[4] EPS, and UART_LCTR[3] PEN bits (see Table 7-67). 

**Table 7-67. Relationship Between SP, EPS, and PEN Bits in LCTR** 

|**SP Bit**|**EPS Bit**|**PEN Bit**|**Parity Option**|
|---|---|---|---|
|x|x|0|Parity disabled: No PARITY bit is transmitted or checked.|
|0|0|1|Odd parity selected: Odd number of logic 1s.|
|0|1|1|Even parity selected: Even number of logic 1s.|
|1|0|1|Stick parity selected with PARITY bit transmitted and checked as set.|
|1|1|1|Stick parity selected with PARITY bit transmitted and checked as cleared.|



**Table 7-68. Number of STOP Bits Generated** 

|**STB Bit**|**WLS Bit**|**Word Length Selected with WLS Bits**|**Number of STOP Bits Generated**|**Baud Clock (BCLK) Cycles**|
|---|---|---|---|---|
|0|x|Any word length|1|16|
|1|0h|5 bits|1.5|24|
|1|1h|6 bits|2|32|
|1|2h|7 bits|2|32|
|1|3h|8 bits|2|32|



## _**7.3.8.2.4 PRU-ICSS UART Clock Generation and Control**_ 

The PRU-ICSS UART0 bit clock is derived from an input clock to the PRU-ICSS UART0. See the device-specific Data sheet to check the maximum data rate supported by the PRU-ICSS UART0. 

Figure 7-49 is a conceptual clock generation diagram for the PRU-ICSS UART0. The processor clock generator receives a signal from an external clock source and produces a PRU-ICSS UART0 input clock with a programmed frequency. The PRU-ICSS UART0 contains a programmable baud generator that takes an input clock and divides it by a divisor in the range between 1 and (2[16] - 1) to produce a baud clock (BCLK). The frequency of BCLK is sixteen times (16×) the baud rate (each received or transmitted bit lasts 16 BCLK cycles) or thirteen times (13×) the baud rate (each received or transmitted bit lasts 13 BCLK cycles). When the PRU-ICSS UART0 is receiving, the bit is sampled in the 8th BCLK cycle for 16× over sampling mode and on the 6th BCLK cycle for 13× over-sampling mode. The 16× or 13× reference clock is selected by configuring the mode definition register: UART_MODE[0] OSM_SEL bit. The formula to calculate the divisor is: 

**Divisor = UART input clock frequency [MODE.OSM_SEL = 0h] Desired baud rate** x **16** 

icss-13 

432 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Divisor = UART input clock frequency [MODE.OSM_SEL = 1h] Desired baud rate** x **13** 

icss-14 

## Two 8-bit register fields: 

- UART_DIVMSB[7-0] DLH 

- UART_DIVLSB[7-0] DLL, 

called divisor latches, hold this 16-bit divisor. DLH holds the most significant bits of the divisor, and DLL holds the least significant bits of the divisor. For information about these register fields, see the PRU-ICSS UART0 register descriptions in the _PRU_UART_UART0 Registers_ . These divisor latches must be loaded during initialization of the PRU-ICSS UART0 in order to ensure desired operation of the baud generator. Writing to the divisor latches results in two wait states being inserted during the write access while the baud generator is loaded with the new value. 

Figure 7-50 summarizes the relationship between the transferred data bit, BCLK, and the PRU-ICSS UART0 input clock. Note that the timing relationship depicted in Figure 7-50 shows that each bit lasts for 16 BCLK cycles. This is in case of 16x over-sampling mode. For 13× over-sampling mode each bit lasts for 13 BCLK cycles. 

Example baud rates and divisor values relative to a 150MHz PRU-ICSS UART0 input clock and 16× oversampling mode are shown in Table 7-69. 

**==> picture [378 x 200] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRUSS<br>PRUSS UART0<br>Receiver<br>DLH:DLL timing and<br>control<br>Clock UART input clock Baud BCLK<br>Input clock<br>generator generator<br>Transmitter<br>timing and<br>control<br>Other logic<br>pruss-015<br>**----- End of picture text -----**<br>


**Figure 7-49. PRU-ICSS UART Clock Generation Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

433 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

_n_ UART input clock cycles, where _n_ = divisor in DLH:DLL 

**==> picture [486 x 293] intentionally omitted <==**

**----- Start of picture text -----**<br>
UART input clock<br>n<br>BCLK<br>Each bit lasts 16 BCLK cycles.<br>When receiving, the UART samples the bit in the 8th cycle.<br>BCLK<br>UART0_TXD,<br>D1 D2<br>UART0_RXD<br>D0<br>UART0_TXD,<br>START D0 D1 D2 D3 D4 D5 D6 D7 PARITY STOP1 STOP2<br>UART0_RXD<br>**----- End of picture text -----**<br>


icss-016 

**Figure 7-50. Relationships Between PRU-ICSS UART Data Bit, BCLK, and Input Clock** 

**Table 7-69. Baud Rate Examples for 192-MHZ PRU-ICSS UART Input Clock and 16× Over-sampling Mode** 

|**Baud Rate**|**Divisor Value**|**Actual Baud Rate**|**Error (%)**|
|---|---|---|---|
|2400<br>5000<br>2400<br>0.00<br>4800<br>2500<br>4800<br>0.00<br>9600<br>1250<br>9600<br>0.00<br>19200<br>625<br>19200<br>0.00<br>38400<br>313<br>38338.658<br>–0.16<br>56000<br>214<br>56074.766<br>0.13<br>115200<br>104<br>115384.6<br>0.16<br>128000<br>94<br>127659.574<br>–0.27<br>3000000<br>4<br>3000000<br>0.00<br>6000000<br>2<br>3000000<br>0.00<br>12000000<br>1<br>12000000<br>12000000||||



**Table 7-70. Baud Rate Examples for 192-MHZ PRU-ICSS UART Input Clock and 13× Over-sampling Mode** 

|**Baud Rate**|**Divisor Value**|**Actual Baud Rate**|**Error (%)**|
|---|---|---|---|
|2400<br>6154<br>2399.940<br>–0.0025<br>4800<br>3077<br>4799.880<br>–0.0025<br>9600<br>1538<br>9602.881<br>0.03<br>19200<br>769<br>19205.762<br>0.03<br>38400<br>385<br>38361.638<br>–0.10<br>56000<br>264<br>55944.056<br>–0.10<br>115200<br>128<br>115384.6<br>0.16||||



434 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-70. Baud Rate Examples for 192-MHZ PRU-ICSS UART Input Clock and 13× Over-sampling Mode (continued)** 

|**Baud Rate**|**Divisor Value**|**Actual Baud Rate**|**Error (%)**|
|---|---|---|---|
|128000<br>115<br>128428.094<br>0.33||||



## **7.3.8.3 PRU-ICSS UART Functional Description** 

## _**7.3.8.3.1 PRU-ICSS UART Functional Block Diagram**_ 

A functional block diagram of the PRU-ICSS UART0 is shown in Figure 7-51. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 435 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [446 x 525] intentionally omitted <==**

**----- Start of picture text -----**<br>
S<br>e<br>l 8 Receiver 8<br>e FIFO<br>8<br>c<br>t<br>Receiver<br>Peripheral 8 UART0_RXD<br>Bus Data Receiver Shift<br>Bus Buffer Register signal<br>Buffer Register<br>16<br>Receiver<br>Line<br>Timing and<br>Control<br>Control<br>Register<br>Divisor<br>Latch (LS) 16 Baud<br>Generator<br>Divisor<br>Latch (MS)<br>Transmitter<br>Line<br>Status Timing and<br>Control<br>Register<br>8 Transmitter 8 S<br>FIFO e<br>l<br>Transmitter 8 e 8 Transmitter UART0_TXD<br>Holding c Shift<br>Register t Register signal<br>Modem<br>8 Control<br>Control<br>Logic<br>Register<br>Interrupt 8 Interrupt/<br>Enable Event Interrupt to CPU<br>Register Control<br>Logic<br>Event to DMA controller<br>Interrupt 8<br>Identification<br>Register Power and<br>Emulation<br>Control<br>FIFO Register<br>Control<br>Register icss-017<br>**----- End of picture text -----**<br>


NOTE: The value _n_ indicates the applicable UART where there are multiple instances. For the PRU-ICSS, there is only one instance and all UART signals should reflect this (e.g., UART0_TXD instead of UARTn_TXD). 

**Figure 7-51. PRU-ICSS UART Block Diagram** 

## _**7.3.8.3.2 PRU-ICSS UART Reset Considerations**_ 

## _**7.3.8.3.2.1 PRU-ICSS UART Software Reset Considerations**_ 

Two bits in the power and emulation management register - UART_PWR, control resetting the parts of the PRU-ICSS UART0: 

436 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- The bit [14]UTRST controls resetting the transmitter only. If bit [14]UTRST = 1h, the transmitter is enabled and active; 

   - if bit [14]UTRST = 0h, the transmitter is disabled and in reset state. 

- The bit [13]URRST controls resetting the receiver only. If [13]URRST = 1h, the receiver is enabled and active; if bit [13]URRST = 0h, the receiver is disabled and in reset state. 

In each case, putting the receiver and/or transmitter in reset will reset the state machine of the affected portion but will not affect the PRU-ICSS UART0 registers. 

## _**7.3.8.3.2.2 PRU-ICSS UART Hardware Reset Considerations**_ 

When the processor RESET pin is asserted, the entire processor is reset and is held in the reset state until the RESET pin is released. As part of a device reset, the PRU-ICSS UART0 state machine is reset and the PRU-ICSS UART0 registers are forced to their default states. The default states of the registers are shown in . 

## _**7.3.8.3.3 PRU-ICSS UART Power Management**_ 

The PRU-ICSS UART0 peripheral can be placed in reduced-power modes to conserve power during periods of low activity. The power management of the PRU-ICSS UART0 peripheral and other PRU-ICSS peripherals is controlled by the device Reset Control Manager (RCM). The RCM acts as a power management controller for all of the peripherals on the device. For more details on the power management procedures using the PSC, refer to the _Power Management_ section. 

## _**7.3.8.3.4 PRU-ICSS UART Interrupt Support**_ 

## _**7.3.8.3.4.1 PRU-ICSS UART Interrupt Events and Requests**_ 

The PRU-ICSS UART0 generates the interrupt requests described in Table 7-71. All requests are multiplexed through an arbiter to a single PRU-ICSS UART0 interrupt request to the CPU, as shown in Figure 7-52. Each of the interrupt requests has an enable bit in the interrupt enable register (IER) - UART_INT_EN and is recorded in [3-1]IIR_INTID bitfield of UART_INT_FIFO register. 

If an interrupt occurs and the corresponding enable bit is set to 1h, the interrupt request is recorded in corresponding UART_INT_FIFO[3-1] IIR_INTID bitfield and is forwarded to the CPU. If an interrupt occurs and the corresponding enable bit is cleared to 0h, the interrupt request is blocked. The interrupt request is neither recorded in UART_INT_FIFO[3-1] IIR_INTID, nor forwarded to the CPU. 

## _**7.3.8.3.4.2 PRU-ICSS UART Interrupt Multiplexing**_ 

The PRU-ICSS UART0 have dedicated interrupt signals to the CPU and the interrupts are not multiplexed with any other interrupt source. 

**Table 7-71. PRU-ICSS UART Interrupt Requests Descriptions** 

|**PRU-ICSS UART0**|||
|---|---|---|
|**Interrupt Request**|**Interrupt Source**|**Comment**|
|THREINT|THR-empty condition: The transmitter holding register|If THREINT is enabled in UART_INT_EN register by|
||(THR) or the transmitter FIFO is empty. All of the data|setting the [1]ETBEI bit, it is recorded in [3-1]IIR_INTID|
||has been copied from THR, ( i.e. UART_RBR_TBR[7-0]|bitfield.|
||RBR_DATA) to the transmitter shift register (TSR).|As an alternative to using THREINT, the CPU can poll the|
|||THRE bit in the line status register UART_LSR1.|
|RDAINT|Receive data available in non-FIFO mode or trigger level|If RDAINT is enabled in UART_INT_EN register, by|
||reached in the FIFO mode.|setting the [0]ERBI bit, it is recorded in INTID bitfield.|
|||As an alternative to using RDAINT, the CPU can poll the|
|||[0]DR bit in the line status register UART_LSR1. In the|
|||FIFO mode, this is not a functionally equivalent alternative|
|||because the [0]DR bit does not respond to the FIFO|
|||trigger level. The [0]DR bit only indicates the presence|
|||or absence of unread characters.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 437 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-71. PRU-ICSS UART Interrupt Requests Descriptions (continued)** 

|**PRU-ICSS UART0**|**PRU-ICSS UART0**|||||||||||||||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Interrupt Request**||**Interrupt**||||||||**Source**|||||||||||**Comment**|||
|RTOINT||Receiver||||||||time-out condition (in the FIFO||||||||mode only):<br>The receiver time-out interrupt prevents the PRU-ICSS||||||
|||No characters have been removed from or|||||||||||||||||input to the<br>UART0 from waiting indefinitely, in the case when the|||||
|||receiver||||||FIFO during the last four character times (see<br>receiver FIFO level is below|||||||||||||||the trigger level and thus|
|||Table|||7-73),||||||||and there is at least one character in the<br>does not generate a receiver data-ready interrupt.|||||||||||
|||receiver||||||FIFO during this time.|||||||||||||If RTOINT is enabled in UART_INT_EN register,|||
||||||||||||||||||||||by setting the [0]ERBI bit, it is recorded in|||
||||||||||||||||||||||UART_INT_FIFO[3-1] IIR_INTID bitfield.|||
||||||||||||||||||||||There is no status bit to reflect the occurrence of a time-|||
||||||||||||||||||||||out condition.|||
|RLSINT||Receiver||||||||line status condition: An overrun error, parity<br>If RLSINT is enabled in INT_EN register, by setting||||||||||||||
|||error,|||framing error, or break has occurred.||||||||||||||||the [2]ELSI bit, it is recorded in UART_INT_FIFO[3-1]|||
||||||||||||||||||||||IIR_INTID bitfield.|||
||||||||||||||||||||||As an alternative to using RLSINT, the CPU can poll|||
||||||||||||||||||||||the following bits in the line status register UART_LSR1:|||
||||||||||||||||||||||overrun error indicator (bit [1]OE), parity error indicator|||
||||||||||||||||||||||(bit [2]PE), framing error indicator ([3]FE), and break|||
||||||||||||||||||||||indicator ([4]BI).|||
||**Conditions**||||||||||||||**Enable bits**||||**UART interrupt requests**|||||
|Transmitter holding||||||||||||||||||||||||
||register empty||||||||||||||IER(ETBEI)||||||THREINT|||
|||||||||||||||||||||||||
|Receiver data||ready|||||||||||||||||||RDRINT|||
|||||||||||||||||||||||||
|||||||||||||||||||||||||
||||||||||||||||IER(ERBI)||||||RTOINT<br>Arbiter||UART0 interrupt<br>request to CPU|
||Receiver time-out|||||||||||||||||||||||
|||||||||||||||||||||||||
|||||||||||||||||||||||||
||Overrun error|||||||||||||||||||||||
||Parity error<br>Framing error||||||||||||||IER(ELSI)||||||RLSINT|||
|||Break|||||||||||||||||||||icss-018|



**Figure 7-52. PRU-ICSS UART Interrupt Request Enable Paths** 

438 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-72. Interrupt Identification and Interrupt Clearing Information** 

|**Priority**|**IIR Bits**|**IIR Bits**|**IIR Bits**|**IIR Bits**||||
|---|---|---|---|---|---|---|---|
|<br>**Level**|**3**|**2**|**1**|**0**|**Interrupt Type**|**Interrupt Source**|**Event That Clears Interrupt**|
|None|0|0|0|1|None|None|None|
|1|0|1|1|0|Receiver line status|Overrun error, parity error, framing error, or break is<br>detected.|For an overrun error, reading the line status register<br>UART_LSR1, clears the interrupt. For a parity error,<br>framing error, or break, the interrupt is cleared only<br>after all the erroneous data have been read.|
|2|0|1|0|0|Receiver data-ready|Non-FIFO mode: Receiver data is ready.|Non-FIFO mode: The receiver buffer register (RBR) is<br>read.|
|||||||FIFO mode: Trigger level reached. If four character<br>times pass with no access of the FIFO, the interrupt<br>is asserted again.|FIFO mode: The FIFO drops below the trigger level.(1)|
|2|1|1|0|0|Receiver time-out|FIFO mode only: No characters have been removed<br>from or input to the receiver FIFO during the last<br>four character times and there is at least one<br>character in the receiver FIFO during this time.|One of the following events:<br>•<br>A character is read from the receiver FIFO(1)<br>•<br>A new character arrives in the receiver FIFO<br>•<br>The [13]URRST bit in the power and emulation<br>management register (UART_PWR) is loaded with<br>0h.|
|3|0|0|1|0|Transmitter holding<br>register empty|Non-FIFO mode: Transmitter holding register (THR)<br>is empty.|A character is written to the transmitter holding register<br>(UART_RBR_TBR) or the interrupt identification<br>register (UART_INT_FIFO) is read.|
|||||||FIFO mode: Transmitter FIFO is empty.||



(1) In the FIFO mode, the receiver data-ready interrupt or receiver time-out interrupt is cleared by the CPU or by the DMA controller, whichever reads from the receiver FIFO first. 

## _**7.3.8.3.5 PRU-ICSS UART DMA Event Support**_ 

In the FIFO mode, the PRU-ICSS UART0 generates the following two DMA events: 

- **Receive event (URXEVT):** The trigger level for the receiver FIFO (1, 4, 8, or 14 characters) is set with the FIFO control UART_INT_FIFO[7-6] IIR_FIFOEN bitfield. Every time the trigger level is reached or a receiver time-out occurs, the PRU-ICSS UART0 sends a receive event to the UDMA controller. In response, the UDMA controller reads the data from the receiver FIFO by way of the receiver buffer register UART_RBR_TBR[7-0] RBR_DATA. Note that the receive event is not asserted if the data at the top of the receiver FIFO is erroneous even if the trigger level has been reached. 

- **Transmit event (UTXEVT):** When the transmitter FIFO is empty (when the last byte in the transmitter FIFO has been copied to the transmitter shift register), the PRU-ICSS UART0 sends an UTXEVT signal to the UDMA controller. In response, the UDMA controller refills the transmitter FIFO by way of the transmitter holding register (THR) - UART_RBR_TBR[7-0] RBR_DATA. The UTXEVT signal is also sent to the UDMA controller when the PRU-ICSS UART0 is taken out of reset using the [14]UTRST bit in the power and emulation management register (UART_PWR). 

Activity in DMA channels can be synchronized to these events. In the non-FIFO mode, the PRU-ICSS UART0 generates no DMA events. Any DMA channel synchronized to either of these events must be enabled at the time the PRU-ICSS UART0 event is generated. Otherwise, the DMA channel will miss the event and, unless the PRU-ICSS UART0 generates a new event, no data transfer will occur. 

## _**7.3.8.3.6 PRU-ICSS UART Operations**_ 

## _**7.3.8.3.6.1 PRU-ICSS UART FIFO Modes**_ 

The following two modes can be used for servicing the receiver and transmitter FIFOs: 

- FIFO interrupt mode. The FIFO is enabled and the associated interrupts are enabled. Interrupts are sent to the CPU to indicate when specific events occur. 

- FIFO poll mode. The FIFO is enabled but the associated interrupts are disabled. The CPU polls status bits to detect specific events. 

Because the receiver FIFO and the transmitter FIFO are controlled separately, either one or both can be placed into the interrupt mode or the poll mode. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 439 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.8.3.6.1.1 PRU-ICSS UART FIFO Interrupt Mode**_ 

When the receiver FIFO is enabled in the FIFO control register (FCR), mapped in the MSB part of the register UART_INT_FIFO, and the receiver interrupts are enabled in the interrupt enable register UART_INT_EN, the interrupt mode is selected for the receiver FIFO. The following are important points about the receiver interrupts: 

- The receiver data-ready interrupt is issued to the CPU when the FIFO has reached the trigger level that is programmed in FCR. It is cleared when the CPU or the DMA controller reads enough characters from the FIFO such that the FIFO drops below its programmed trigger level. 

- The receiver line status interrupt is generated in response to an overrun error, a parity error, a framing error, or a break. This interrupt has higher priority than the receiver data-ready interrupt. For details, see Section 7.3.8.3.4. 

- The data-ready ([0]DR) bit in the line status register - UART_LSR1, indicates the presence or absence of characters in the receiver FIFO. The [0]DR bit is set when a character is transferred from the receiver shift register (RSR) to the empty receiver FIFO. The [0]DR bit remains set until the FIFO is empty again. 

- A receiver time-out interrupt occurs if all of the following conditions exist: 

   - At least one character is in the FIFO, 

   - The most recent character was received more than four continuous character times ago. A character time is the time allotted for 1 START bit, _n_ data bits, 1 PARITY bit, and 1 STOP bit, where _n_ depends on the word length selected with the WLS0 and WLS1 bits of the line control register UART_LCTR. See Table 7-73. 

   - The most recent read of the FIFO has occurred more than four continuous character times before. 

- Character times are calculated by using the baud rate. 

- When a receiver time-out interrupt has occurred, it is cleared and the time-out timer is cleared when the CPU or the EDMA controller reads one character from the receiver FIFO. The interrupt is also cleared if a new character is received in the FIFO or if the URRST bit is cleared in the power and emulation management register - PWM. 

- If a receiver time-out interrupt has not occurred, the time-out timer is cleared after a new character is received or after the CPU or EDMA reads the receiver FIFO. 

When the transmitter FIFO is enabled in UART_INT_FIFO[0] IIR_IPEND bit and the transmitter holding register empty (THRE) interrupt is enabled in UART_INT_EN[1] ETBEI bit, the interrupt mode is selected for the transmitter FIFO. The THRE interrupt occurs when the transmitter FIFO is empty. It is cleared when the transmitter hold register (THR) UART_RBR_TBR[7-0] RBR_DATA bitfield is loaded (1 to 16 characters may be written to the transmitter FIFO while servicing this interrupt) or the [3-1]IIR_INTID bitfield is read in the interrupt identification register UART_INT_FIFO. 

**Table 7-73. Character Time for Word Lengths** 

|**Word Length (****_n_)**|**Character Time**|**Four Character Times**|
|---|---|---|
|5<br>Time for 8 bits<br>Time for 32 bits<br>6<br>Time for 9 bits<br>Time for 36 bits<br>7<br>Time for 10 bits<br>Time for 40 bits<br>8<br>Time for 11 bits<br>Time for 44 bits|||



## _**7.3.8.3.6.1.2 PRU-ICSS UART FIFO Poll Mode**_ 

When the receiver FIFO is enabled in the FIFO control register (via setting the UART_INT_FIFO[0] IIR_IPEND to 1h) and the receiver interrupts are disabled in the interrupt enable register (UART_INT_EN), the poll mode is selected for the receiver FIFO. Similarly, when the transmitter FIFO is enabled via setting the same bit (UART_INT_FIFO[0] IIR_IPEND to 1h) and the transmitter interrupts are disabled, the transmitted FIFO is in the poll mode. In the poll mode, the CPU detects events by checking bits in the line status register - UART_LSR1: 

- The UART_LSR1[7] RXFIFOE bit indicates whether there are any errors in the receiver FIFO. 

- The UART_LSR1[6] TEMT bit indicates that both the transmitter holding register (THR) and the transmitter shift register (TSR) are empty. 

- The UART_LSR1[5] THRE bit indicates when THR ( mapped in the UART_RBR_TBR[7-0] RBR_DATA bitfield ) is empty. 

440 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- The following line status register - UART_LSR1 bits specify which error or errors have occurred: – UART_LSR1[4] BI - Break Interrupt 

   - UART_LSR1[3] FE – Framing Error 

   - UART_LSR1[2] PE – Parity Error 

   - UART_LSR1[1] OE – Overrun Error 

- The UART_LSR1[0] DR (data-ready) bit is set as long as there is at least one byte in the receiver FIFO. 

Also, in the FIFO poll mode: 

- The interrupt identification ([3-1] IIR_INTID) bit field in register UART_INT_FIFO are not affected by any events because the interrupts are disabled. 

- The PRU-ICSS UART0 does not indicate when the receiver FIFO trigger level is reached or when a receiver time-out occurs. 

## _**7.3.8.3.6.2 PRU-ICSS UART Autoflow Control**_ 

The PRU-ICSS UART0 can employ autoflow control by connecting the UART0_CTS and UART0_RTS signals. The UART0_CTS input must be active before the transmitter FIFO can transmit data. The UART0_RTS becomes active when the receiver needs more data and notifies the sending device. When UART0_RTS is connected to UART0_CTS, data transmission does not occur unless the receiver FIFO has space for the data. Therefore, when two UARTs are connected as shown in Figure 7-53 with autoflow enabled (UART_MCTR[5] AFE = 1h), overrun errors are eliminated. 

**==> picture [452 x 163] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRUSS UART0 UART (another)<br>Serial toParallel UART0_RXD tx Parallel toSerial<br>Receiver Transmitter<br>FIFO FIFO<br>Flow UART0_RTS cts Flow<br>Control Control<br>D[7:0] D[7:0]<br>Parallel to UART0_TXD rx Serial to<br>Serial Parallel<br>Transmitter Receiver<br>FIFO ControlFlow UART0_CTS rts ControlFlow FIFO<br>Off-chip icss-019<br>**----- End of picture text -----**<br>


**Figure 7-53. UART Interface Using Autoflow Diagram** 

## _**7.3.8.3.6.2.1 PRU-ICSS UART Signal UART0_RTS Behavior**_ 

UART0_RTS data flow control originates in the receiver block (see Figure 7-51). When the receiver FIFO level reaches a trigger level of 1, 4, 8, or 14 (see Figure 7-54), UART0_RTS is deasserted. The sending UART may send an additional byte after the trigger level is reached (assuming the sending UART has another byte to send), because it may not recognize the deassertion of UART0_RTS until after it has begun sending the additional byte. For trigger level 1, 4, and 8, UART0_RTS is automatically reasserted once the receiver FIFO is emptied. For trigger level 14, UART0_RTS is automatically reasserted once the receiver FIFO drops below the trigger level. 

**==> picture [488 x 76] intentionally omitted <==**

**----- Start of picture text -----**<br>
UART0_RXD Start Bits N Stop Start Bits N+1 Stop Start<br>UART0_RTS<br>icss-020<br>**----- End of picture text -----**<br>


- A. N = Receiver FIFO trigger level. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 441 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- B. The two blocks in dashed lines cover the case where an additional byte is sent. 

## **Figure 7-54. Autoflow Functional Timing Waveforms for UART0_RTS** 

## _**7.3.8.3.6.2.2 PRU-ICSS UART Signal UART0_CTS Behavior**_ 

The transmitter checks UART0_CTS before sending the next data byte. If UART0_CTS is active, the transmitter sends the next byte. To stop the transmitter from sending the following byte, UART0_CTS must be released before the middle of the last STOP bit that is currently being sent (see Figure 7-55). When flow control is enabled, UART0_CTS level changes do not trigger interrupts because the device automatically controls its own transmitter. Without autoflow control, the transmitter sends any data present in the transmitter FIFO and a receiver overrun error may result. 

**==> picture [498 x 52] intentionally omitted <==**

**----- Start of picture text -----**<br>
Start Bits0-7 Stop Start Bits 0-7 Stop Start Bits 0-7 Stop<br>UART0_TXD<br>UART0_CTS<br>**----- End of picture text -----**<br>


**==> picture [26 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
icss-021<br>**----- End of picture text -----**<br>


- A. When UART0_CTS is active (low), the transmitter keeps sending serial data out. 

- B. When UART0_CTS goes high before the middle of the last STOP bit of the current byte, the transmitter finishes sending the current byte but it does not send the next byte. 

- C. When UART0_CTS goes from high to low, the transmitter begins sending data again. 

## **Figure 7-55. Autoflow Functional Timing Waveforms for UART0_CTS** 

## _**7.3.8.3.6.3 PRU-ICSS UART Loopback Control**_ 

The PRU-ICSS UART0 can be placed in the diagnostic mode using the [4]LOOP bit in the modem control register - UART_MCTR, which internally connects the PRU-ICSS UART0 output back to the PRU-ICSS UART0's input. In this mode, the transmit and receive data paths, the transmitter and receiver interrupts, and the modem control interrupts can be verified without connecting to another UART. 

## _**7.3.8.3.7 PRU-ICSS UART Emulation Considerations**_ 

The [0]FREE bit in the power and emulation management register (UART_PWR) determines how the PRU-ICSS UART0 responds to an emulation suspend event such as an emulator halt or breakpoint. If bit UART_PWR[0] FREE = 0h and a transmission is in progress, the PRU-ICSS UART0 halts after completing the one-word transmission; if bit UART_PWR[0] FREE = 0h and a transmission is not in progress, the PRU-ICSS UART0 halts immediately. If UART_PWR[0] FREE = 1h, the PRU-ICSS UART0 does not halt and continues operating normally. 

Note also that most emulator accesses are transparent to PRU-ICSS UART0 operation. Emulator read operations do not affect any register contents, status bits, or operating states, with the exception of the interrupt identification register (UART_INT_FIFO). Emulator writes, however, may affect register contents and may affect PRU-ICSS UART0 operation, depending on what register is accessed and what value is written. 

The PRU-ICSS UART0 registers can be read from or written to during emulation suspend events, even if the PRU-ICSS activity has stopped. 

## _**7.3.8.3.8 PRU-ICSS UART Exception Processing**_ 

## _**7.3.8.3.8.1 PRU-ICSS UART Divisor Latch Not Programmed**_ 

Since the processor reset signal has no effect on the divisor latch, the divisor latch will have an unknown value after power up. If the divisor latch is not programmed after power up, the baud clock (BCLK) will not operate and will instead be set to a constant logic 1 state. 

The divisor latch values should always be reinitialized following a processor reset. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

442 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.8.3.8.2 Changing Operating Mode During Busy Serial Communication of PRU-ICSS UART**_ 

Since the serial link characteristics are based on how the control registers are programmed, the PRU-ICSS UART0 module will expect the control registers to be static while it is busy engaging in a serial communication. Therefore, changing the control registers while the module is still busy communicating with another serial device will most likely cause an error condition and should be avoided. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

443 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.9 PRU-ICSS ECAP Module**_ 

## **7.3.9.1 PRU-ICSS eCAP Overview** 

## _**7.3.9.1.1 Purpose of the PRU-ICSS eCAP Peripheral**_ 

The device PRU-ICSS integrated **enhanced capture (eCAP)** module targets: 

- Sample rate measurements of audio inputs 

- Speed measurements of rotating machinery (for example, toothed sprockets sensed via Hall sensors) 

- Elapsed time measurements between position sensor pulses 

- Period and duty cycle measurements of pulse train signals 

- Decoding current or voltage amplitude derived from duty cycle encoded current/voltage sensors 

## _**7.3.9.1.2 PRU-ICSS eCAP Features**_ 

The device PRU-ICSS integrated eCAP module (signified as PRU-ICSS_eCAP_0 throughout the _PRU-ICSS eCAP Module_ section) includes the following features: 

- 32-bit time base counter 

- 4-event time-stamp registers (each 32 bits) 

- Edge polarity selection for up to four sequenced time-stamp capture events 

- Interrupt on either of the four events 

- Single shot capture of up to four event time-stamps 

- Continuous mode capture of time-stamps in a four-deep circular buffer 

- Absolute time-stamp capture 

- Difference (Delta) mode time-stamp capture 

- All above resources dedicated to a single input pin 

- When not used in capture mode, the ECAP module can be configured as a single channel PWM output 

## **7.3.9.2 PRU-ICSS ECAP Functional Description** 

For full description of the PRU-ICSS ECAP0 module and functionality, refer to the _Enhanced Capture (eCAP) Module._ 

## _**7.3.9.2.1 PRU-ICSS Capture and APWM Operating Mode**_ 

The PRU-ICSS_eCAP_0 module resources can be used to implement a single-channel PWM generator (with 32 bit capabilities) when it is not being used for input captures. The counter operates in count-up mode, providing a time-base for asymmetrical pulse width modulation (PWM) waveforms. The PRU-ICSS_ECAP_CAP1 and PRU-ICSS_ECAP_CAP2 registers become the active period and compare registers, respectively, while PRUICSS_ECAP_CAP3 and PRU-ICSS_ECAP_CAP4 registers become the period and capture shadow registers, respectively. 

444 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.9.2.2 PRU-ICSS eCAP Capture Mode Description**_ 

Figure 7-56 shows the various components that implement the capture function. 

**==> picture [440 x 474] intentionally omitted <==**

**----- Start of picture text -----**<br>
ECCTL2[SYNCI_EN, SYNCOSEL, SWSYNC]<br>ECCTL2[CAP/APWM]<br>CTRPHS<br>(phase register-32 bit) APWM mode<br>SYNCIn<br>OVF CTR_OVF<br>SYNCOut TSCTR CTR [0-31] PWM<br>(counter-32 bit) Delta-mode PRD [0-31] compare<br>RST<br>logic<br>CMP [0-31]<br>32<br>CTR [0-31] PRDEQ<br>CMPEQ<br>32<br>PRD [0-31]<br>ECCTL1 [ CAPLDEN, CTRRSTx]<br>ECAPx<br>32 CAP1 LD LD1 Polarity<br>(APRD active) select<br>APRD<br>32<br>shadow 32 CMP [0-31]<br>32 CAP2 LD LD2 Polarity<br>(ACMP active) select<br>Event<br>32 ACMP Event<br>shadow qualifier Prescale<br>ECCTL1[EVTPS]<br>32 CAP3 LD LD3 Polarityselect<br>(APRD shadow)<br>32 CAP4 LD LD4 Polarity<br>(ACMP shadow) select<br>Edge Polarity Select<br>4<br>ECCTL1[CAPxPOL]<br>Capture events 4<br>CEVT[1:4]<br>Interrupt Continuous /<br>to Interrupt Trigger Oneshot<br>Controller and CNTOVF Capture Control<br>Flag<br>PRDEQ<br>control<br>CMPEQ<br>ECCTL2 [ RE-ARM, CONT/ONESHT, STOP_WRAP]<br>Registers:  ECEINT, ECFLG, ECCLR, ECFRC<br>SYNC<br>MODE SELECT<br>**----- End of picture text -----**<br>


**Figure 7-56. Capture Function Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 445 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.9.2.2.1 PRU-ICSS eCAP Event Prescaler**_ 

An input capture signal (pulse train) can be prescaled by N = 2-62 (in multiples of 2) or can bypass the prescaler. This is useful when very high frequency signals are used as inputs. Figure 7-57 shows a functional diagram and Figure 7-58 shows the operation of the prescale function. 

**==> picture [234 x 131] intentionally omitted <==**

**----- Start of picture text -----**<br>
Event Prescaler<br>0<br>ECAPx<br>1 / n  Pin<br>(from GPIO)<br>5<br>ECCTL1[13:9]<br>by-pass<br>pre-scaler [5-bits]<br>(counter)<br>**----- End of picture text -----**<br>


- A. When a prescale value of 1 is chosen (PRU-ICSS_ECAP_ECCTL1[13:9] = 0b0000) the input capture signal by-passes the prescale logic completely. 

**Figure 7-57. Event Prescale Control** 

**==> picture [28 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
ECAPx<br>PSout<br>div 2<br>PSout<br>div 4<br>PSout<br>div 6<br>PSout<br>div 8<br>PSout<br>div 10<br>**----- End of picture text -----**<br>


**Figure 7-58. Prescale Function Waveforms** 

446 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.9.2.2.2 PRU-ICSS eCAP Edge Polarity Select and Qualifier**_ 

- Four independent edge polarity (rising edge/falling edge) selection multiplexers are used, one for each capture event. 

- Each edge (up to 4) is event qualified by the Modulo4 sequencer. 

- The edge event is gated to its respective CAP _n_ register by the Mod4 counter. The CAP _n_ register is loaded on the falling edge. 

## _**7.3.9.2.2.3 eCAP Continuous/One-Shot Control**_ 

- The Mod4 (2 bit) counter is incremented via edge qualified events (CEVT1 - CEVT4). 

- The Mod4 counter continues counting (0->1->2->3->0) and wraps around unless stopped. 

- A 2-bit stop register is used to compare the Mod4 counter output, and when equal stops the Mod4 counter and inhibits further loads of the PRU-ICSS_ECAP_CAP1 - PRU-ICSS_ECAP_CAP4 registers. This occurs during one-shot operation. 

The continuous/one-shot block controls the start/stop and reset (zero) functions of the Mod4 counter via a mono-shot type of action that can be triggered by the stop-value comparator and re-armed via software control. 

Once armed, the eCAP module waits for 1-4 (defined by stop-value) capture events before freezing both the Mod4 counter and contents of PRU-ICSS_ECAP_CAP1-4 registers (time-stamps). 

Re-arming prepares the eCAP module for another capture sequence. Also re-arming clears (to zero) the Mod4 counter and permits loading of PRU-ICSS_ECAP_CAP1-4 registers again, providing the CAPLDEN bit is set. 

In continuous mode, the Mod4 counter continues to run (0->1->2->3->0, the one-shot action is ignored, and capture values continue to be written to PRU-ICSS_ECAP_CAP1-4 in a circular buffer sequence. 

## _**7.3.9.2.2.4 PRU-ICSS eCAP 32-bit Counter and Phase Control**_ 

This counter provides the time-base for event captures, and is clocked via the system clock. 

On any of the four event loads, an option to reset the 32-bit counter is given. This is useful for time difference capture. The 32-bit counter value is captured first, then it is reset to 0 by any of the LD1-LD4 signals. 

## **Note** 

The PRU-ICSS_eCAP_0 "SYNCIn" hardware event synchronization input and "SYNCOut" hardware synchronization output are NOT implemented in the PRU-ICSS. However, a software-forced synchronization via bit PRU-ICSS_ECAP_ECCTL2[8] SWSYNC, can be used as an alternative, provided that PRU-ICSS_ECAP_ECCTL2[5] SYNCI_EN bit is set to 0b1. 

## _**7.3.9.2.2.5 PRU-ICSS Enhanced Capture CAP1-CAP4 Registers**_ 

These 32-bit registers are fed by the 32-bit counter timer bus, CTR[0-31] and are loaded (capture a time-stamp) when their respective LD inputs are strobed. 

Loading of the capture registers can be inhibited via control bit CAPLDEN. During one-shot operation, this bit is cleared (loading is inhibited) automatically when a stop condition occurs, StopValue = Mod4. 

PRU-ICSS_ECAP_CAP1 and PRU-ICSS_ECAP_CAP2 registers become the active period and compare registers, respectively, in APWM mode. 

PRU-ICSS_ECAP_CAP3 and PRU-ICSS_ECAP_CAP4 registers become the respective shadow registers (APRD and ACMP) for PRU-ICSS_ECAP_CAP1 and PRU-ICSS_ECAP_CAP2 during APWM operation. 

## _**7.3.9.2.2.6 PRU-ICSS eCAP Interrupt Control**_ 

An Interrupt can be generated on capture events (CEVT1-CEVT4, CNTOVF) or APWM events (CTR = PRD, CTR = CMP). See _Interrupts in PRU-ICSS eCAP Module_ . 

A counter overflow event (FFFF FFFFh->0000 0000h) is also provided as an interrupt source (CNTOVF). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 447 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

The capture events are edge and sequencer qualified (that is, ordered in time) by the polarity select and Mod4 gating, respectively. 

One of these events can be selected as the interrupt source of the PRU-ICSS eCAP module "pr1_ecap_intr_req" aggregated IRQ mapped on the PRU-ICSS1_IRQ_15 input line of the local PRU-ICSS1_INTC. See also Table 7-64. 

Seven interrupt events (CEVT1, CEVT2, CEVT3, CEVT4, CNTOVF, CTR = PRD, CTR = CMP) can be generated. The interrupt enable register (PRU-ICSS_ECAP_ECEINT) is used to enable/disable individual interrupt event sources. The interrupt flag register (PRU-ICSS_ECAP_ECFLG) indicates if any interrupt event has been latched and contains the global interrupt flag bit (INT). An interrupt pulse is generated to the PRUICSS1_INTC local interrupt controller only if any of the interrupt events are enabled, the flag bit is 1, and the INT flag bit is 0. The interrupt service routine must clear the global interrupt flag bit and the serviced event via the interrupt clear register (PRU-ICSS_ECAP_ECCLR) before any other interrupt pulses are generated. You can force an interrupt event via the interrupt force register (PRU-ICSS_ECAP_ECFRC). This is useful for test purposes. 

## _**7.3.9.2.2.7 PRU-ICSS eCAP Shadow Load and Lockout Control**_ 

In capture mode, this logic inhibits (locks out) any shadow loading of PRU-ICSS_ECAP_CAP1 or PRUICSS_ECAP_CAP2 from APRD and ACMP registers, respectively. 

In APWM mode, shadow loading is active and two choices are permitted: 

- Immediate - APRD or ACMP are transferred to PRU-ICSS_ECAP_CAP1 or PRU-ICSS_ECAP_CAP2 immediately upon writing a new value. 

- On period equal, CTR[31-0] = PRD[31-0] 

## _**7.3.9.2.2.8 CEVT Flag Registers**_ 

## **Note** 

The CEVT1, CEVT2, CEVT3, CEVT4 flags are only active in capture mode (PRx_ECAP_ECCTL2[9] CAPAPWM == 0b'0). The CTR = PRD, CTR = CMP flags are only valid in APWM mode (PRx_ECAP_ECCTL2[9] CAPAPWM == 0b'1). CNTOVF flag is valid in both modes. 

## _**7.3.9.2.3 PRU-ICSS eCAP Module APWM Mode Operation**_ 

Main operating highlights of the APWM section: 

- The time-stamp counter bus is made available for comparison via 2 digital (32-bit) comparators. 

- When PRU-ICSS_ECAP_CAP1 / PRU-ICSS_ECAP_CAP2 registers are not used in capture mode, the contents are used as Period and Compare values in APWM mode. 

- Double buffering is achieved via shadow registers APRD and ACMP (PRU-ICSS_ECAP_CAP3/PRUICSS_ECAP_CAP4). The shadow register contents are transferred over to PRU-ICSS_ECAP_CAP1 / PRUICSS_ECAP_CAP2 registers either immediately upon a write, or on a CTR = PRD trigger. 

- In APWM mode, writing to PRU-ICSS_ECAP_CAP1 / PRU-ICSS_ECAP_CAP2 active registers also write the same value to the corresponding shadow registers PRU-ICSS_ECAP_CAP3/PRU-ICSS_ECAP_CAP4. This emulates immediate mode. Writing to the shadow registers PRU-ICSS_ECAP_CAP3/PRUICSS_ECAP_CAP4 invokes the shadow mode. 

- During initialization, you must write to the active registers for both period and compare. This automatically copies the initial values into the shadow values. For subsequent compare updates, during run-time, you only need to use the shadow registers. 

448 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [405 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
TSCTR<br>FFFFFFFF<br>1000h<br>APRD<br>500h<br>ACMP<br>300h<br>0000000C<br>APWMx<br>(o/p pin)<br>Off−time<br>On Period<br>time<br>**----- End of picture text -----**<br>


**Figure 7-59. PWM Waveform Details Of eCAP APWM Mode Operation** 

The behavior of APWM active-high mode (APWMPOL == 0) is: 

```
CMP = 00000000h, output low for duration of period (0% duty)
```

```
CMP = 00000001h, output high 1 cycle
```

```
CMP = 00000002h, output high 2 cycles
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

The behavior of APWM active-low mode (APWMPOL == 1) is: 

```
CMP = 00000000h, output high for duration of period (0% duty)
```

```
CMP = 00000001h, output low 1 cycle
```

```
CMP = 00000002h, output low 2 cycles
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

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 449 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.9.2.4 Use Cases**_ 

The following sections will provide Applications examples and code snippets to show how to configure and operate the eCAP module. For clarity and ease of use, below are useful #defines which will help in the understanding of the examples. 

```
// ECCTL1 ( ECAP Control Reg 1)
//==========================
// CAPxPOL bits
#define    EC_RISING              0x0
#define    EC_FALLING             0x1
// CTRRSTx bits
#define    EC_ABS_MODE            0x0
#define    EC_DELTA_MODE          0x1
// PRESCALE bits
#define    EC_BYPASS              0x0
#define    EC_DIV1                0x0
#define    EC_DIV2                0x1
#define    EC_DIV4                0x2
#define    EC_DIV6                0x3
#define    EC_DIV8                0x4
#define    EC_DIV10               0x5
// ECCTL2 ( ECAP Control Reg 2)
//==========================
// CONT/ONESHOT bit
#define    EC_CONTINUOUS          0x0
#define    EC_ONESHOT             0x1
// STOPVALUE bit
#define    EC_EVENT1              0x0
#define    EC_EVENT2              0x1
#define    EC_EVENT3              0x2
#define    EC_EVENT4              0x3
// RE-ARM bit
#define    EC_ARM                 0x1
// TSCTRSTOP bit
#define    EC_FREEZE              0x0
#define    EC_RUN                 0x1
// SYNCO_SEL bit
#define    EC_SYNCIN              0x0
#define    EC_CTR_PRD             0x1
#define    EC_SYNCO_DIS           0x2
// CAP/APWM mode bit
#define    EC_CAP_MODE            0x0
#define    EC_APWM_MODE           0x1
// APWMPOL bit
#define    EC_ACTV_HI             0x0
#define    EC_ACTV_LO             0x1
// Generic
#define    EC_DISABLE             0x0
#define    EC_ENABLE              0x1
#define    EC_FORCE               0x1
```

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

450 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.9.2.4.1 Absolute Time-Stamp Operation Rising Edge Trigger Example**_ 

Figure 7-60 shows an example of continuous capture operation (Mod4 counter wraps around). In this figure, TSCTR counts-up without resetting and capture events are qualified on the rising edge only, this gives period (and frequency) information. 

On an event, the TSCTR contents (time-stamp) is first captured, then Mod4 counter is incremented to the next state. When the TSCTR reaches FFFF FFFFh (maximum value), it wraps around to 0000 0000h (not shown in Figure 7-60), if this occurs, the CNTOVF (counter overflow) flag is set, and an interrupt (if enabled) occurs, CNTOVF (counter overflow) Flag is set, and an Interrupt (if enabled) occurs. Captured time-stamps are valid at the point indicated by the diagram, after the 4th event, hence event CEVT4 can conveniently be used to trigger an interrupt and the CPU can read data from the CAP _n_ registers. 

**==> picture [440 x 310] intentionally omitted <==**

**----- Start of picture text -----**<br>
CEVT1 CEVT2 CEVT3 CEVT4 CEVT1<br>CAPx pin<br>t4 t5<br>FFFFFFFF t3<br>t2<br>CTR[0−31] t1<br>00000000<br>MOD4<br>0 1 2 3 0 1<br>CTR<br>CAP1 XX t1 t5<br>CAP2 XX t2<br>CAP3 XX t3<br>CAP4 XX t4<br>t<br>Polarity selection All capture values valid<br>(can be read) at this time<br>Capture registers [1−4]<br>**----- End of picture text -----**<br>


**Figure 7-60. Capture Sequence for Absolute Time-Stamp, Rising Edge Detect** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

451 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-74. ECAP Initialization for CAP Mode Absolute Time, Rising Edge Trigger** 

|**Register**|**Bit**|**Value**|
|---|---|---|
|ECCTL1|CAP1POL|EC_RISING|
|ECCTL1|CAP2POL|EC_RISING|
|ECCTL1|CAP3POL|EC_RISING|
|ECCTL1|CAP4POL|EC_RISING|
|ECCTL1|CTRRST1|EC_ABS_MODE|
|ECCTL1|CTRRST2|EC_ABS_MODE|
|ECCTL1|CTRRST3|EC_ABS_MODE|
|ECCTL1|CTRRST4|EC_ABS_MODE|
|ECCTL1|CAPLDEN|EC_ENABLE|
|ECCTL1|PRESCALE|EC_DIV1|
|ECCTL2|CAP_APWM|EC_CAP_MODE|
|ECCTL2|CONT_ONESHT|EC_CONTINUOUS|
|ECCTL2|SYNCO_SEL|EC_SYNCO_DIS|
|ECCTL2|SYNCI_EN|EC_DISABLE|
|ECCTL2|TSCTRSTOP|EC_RUN|



_**Example 7-1. Code Snippet for CAP Mode Absolute Time, Rising Edge Trigger**_ 

```
// Code snippet for CAP mode Absolute Time, Rising edge trigger
// Run Time ( e.g. CEVT4 triggered ISR call)
//==========================================
    TSt1 = ECAPxRegs.CAP1;        // Fetch Time-Stamp captured at t1
    TSt2 = ECAPxRegs.CAP2;        // Fetch Time-Stamp captured at t2
    TSt3 = ECAPxRegs.CAP3;        // Fetch Time-Stamp captured at t3
    TSt4 = ECAPxRegs.CAP4;        // Fetch Time-Stamp captured at t4
    Period1 = TSt2-TSt1;        // Calculate 1st period
    Period2 = TSt3-TSt2;        // Calculate 2nd period
    Period3 = TSt4-TSt3;        // Calculate 3rd period
```

452 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.9.2.4.2 Absolute Time-Stamp Operation Rising and Falling Edge Trigger Example**_ 

In Figure 7-61 the eCAP operating mode is almost the same as in the previous section except capture events are qualified as either rising or falling edge, this now gives both period and duty cycle information: Period1 = t3 – t1, Period2 = t5 – t3, …etc. Duty Cycle1 (on-time %) = (t2 – t1) / Period1 x 100%, etc. Duty Cycle1 (off-time %) = (t3 – t2) / Period1 x 100%, etc. 

**==> picture [456 x 356] intentionally omitted <==**

**----- Start of picture text -----**<br>
CEVT2 CEVT4 CEVT2 CEVT4<br>CEVT1 CEVT3 CEVT1 CEVT3 CEVT1<br>CAPx pin<br>FFFFFFFF t9<br>t8<br>t7<br>t6<br>t5<br>CTR[0−31] t4<br>t3<br>t2<br>t1<br>00000000<br>MOD4<br>0 1 2 3 0 1 2 3 0<br>CTR<br>CAP1 XX t1 t5<br>CAP2 XX t2 t6<br>CAP3 XX t3 t7<br>CAP4 XX t4 t8<br>tt<br>Polarity selection<br>Capture registers [1−4]<br>**----- End of picture text -----**<br>


**Figure 7-61. Capture Sequence for Absolute Time-Stamp, Rising and Falling Edge Detect** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 453 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

|**Table**|**7-75. ECAP Initialization for CAP Mode Absolute Time, Rising and Falling Edge Trigger**|**7-75. ECAP Initialization for CAP Mode Absolute Time, Rising and Falling Edge Trigger**|**7-75. ECAP Initialization for CAP Mode Absolute Time, Rising and Falling Edge Trigger**|
|---|---|---|---|
||**Register**|**Bit**|**Value**|
||ECCTL1|CAP1POL|EC_RISING|
||ECCTL1|CAP2POL|EC_FALLING|
||ECCTL1|CAP3POL|EC_RISING|
||ECCTL1|CAP4POL|EC_FALLING|
||ECCTL1|CTRRST1|EC_ABS_MODE|
||ECCTL1|CTRRST2|EC_ABS_MODE|
||ECCTL1|CTRRST3|EC_ABS_MODE|
||ECCTL1|CTRRST4|EC_ABS_MODE|
||ECCTL1|CAPLDEN|EC_ENABLE|
||ECCTL1|PRESCALE|EC_DIV1|
||ECCTL2|CAP_APWM|EC_CAP_MODE|
||ECCTL2|CONT_ONESHT|EC_CONTINUOUS|
||ECCTL2|SYNCO_SEL|EC_SYNCO_DIS|
||ECCTL2|SYNCI_EN|EC_DISABLE|
||ECCTL2|TSCTRSTOP|EC_RUN|



_**Example 7-2. Code Snippet for CAP Mode Absolute Time, Rising and Falling Edge Trigger**_ 

```
// Code snippet for CAP mode Absolute Time, Rising & Falling edge triggers
// Run Time ( e.g. CEVT4 triggered ISR call)
//==========================================
    TSt1 = ECAPxRegs.CAP1;        // Fetch Time-Stamp captured at t1
    TSt2 = ECAPxRegs.CAP2;        // Fetch Time-Stamp captured at t2
    TSt3 = ECAPxRegs.CAP3;        // Fetch Time-Stamp captured at t3
    TSt4 = ECAPxRegs.CAP4;        // Fetch Time-Stamp captured at t4
    Period1 = TSt3-TSt1;        // Calculate 1st period
    DutyOnTime1 = TSt2-TSt1;    // Calculate On time
    DutyOffTime1 = TSt3-TSt2;    // Calculate Off time
```

454 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.9.2.4.3 Time Difference (Delta) Operation Rising Edge Trigger Example**_ 

Figure 7-62 shows how the eCAP module can be used to collect Delta timing data from pulse train waveforms. Here Continuous Capture mode (TSCTR counts-up without resetting, and Mod4 counter wraps around) is used. In Delta-time mode, TSCTR is Reset back to Zero on every valid event. Here Capture events are qualified as Rising edge only. On an event, TSCTR contents (time-stamp) is captured first, and then TSCTR is reset to Zero. The Mod4 counter then increments to the next state. If TSCTR reaches FFFF FFFFh (maximum value), before the next event, it wraps around to 0000 0000h and continues, a CNTOVF (counter overflow) Flag is set, and an Interrupt (if enabled) occurs. The advantage of Delta-time Mode is that the CAP _n_ contents directly give timing data without the need for CPU calculations: Period1 = T1, Period2 = T2,…etc. As shown in Figure 7-62, the CEVT1 event is a good trigger point to read the timing data, T1, T2, T3, T4 are all valid here. 

**==> picture [436 x 365] intentionally omitted <==**

**----- Start of picture text -----**<br>
CEVT1 CEVT2 CEVT3 CEVT4 CEVT1<br>CAPx pin<br>FFFFFFFF T1 T2 T3 T4<br>CTR[0−31]<br>00000000<br>MOD4<br>CTR 0 1 2 3 0 1<br>CAP1 XX CTR value at CEVT1 t4<br>CAP2 XX t1<br>CAP3 XX t2<br>CAP4 XX t3<br>t<br>Polarity selection<br>Capture registers [1−4] All capture values valid<br>(can be read) at this time<br>**----- End of picture text -----**<br>


**Figure 7-62. Capture Sequence for Delta Mode Time-Stamp, Rising Edge Detect** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 455 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-76. ECAP Initialization for CAP Mode Delta Time, Rising Edge Trigger** 

|**Register**|**Bit**|**Value**|
|---|---|---|
|ECCTL1|CAP1POL|EC_RISING|
|ECCTL1|CAP2POL|EC_RISING|
|ECCTL1|CAP3POL|EC_RISING|
|ECCTL1|CAP4POL|EC_RISING|
|ECCTL1|CTRRST1|EC_DELTA_MODE|
|ECCTL1|CTRRST2|EC_DELTA_MODE|
|ECCTL1|CTRRST3|EC_DELTA_MODE|
|ECCTL1|CTRRST4|EC_DELTA_MODE|
|ECCTL1|CAPLDEN|EC_ENABLE|
|ECCTL1|PRESCALE|EC_DIV1|
|ECCTL2|CAP_APWM|EC_CAP_MODE|
|ECCTL2|CONT_ONESHT|EC_CONTINUOUS|
|ECCTL2|SYNCO_SEL|EC_SYNCO_DIS|
|ECCTL2|SYNCI_EN|EC_DISABLE|
|ECCTL2|TSCTRSTOP|EC_RUN|



_**Example 7-3. Code Snippet for CAP Mode Delta Time, Rising Edge Trigger**_ 

```
// Code snippet for CAP mode Delta Time, Rising edge trigger
// Run Time ( e.g. CEVT1 triggered ISR call)
//==========================================
// Note: here Time-stamp directly represents the Period value.
    Period4 = ECAPxRegs.CAP1;    // Fetch Time-Stamp captured at T1
    Period1 = ECAPxRegs.CAP2;    // Fetch Time-Stamp captured at T2
    Period2 = ECAPxRegs.CAP3;    // Fetch Time-Stamp captured at T3
    Period3 = ECAPxRegs.CAP4;    // Fetch Time-Stamp captured at T4
```

456 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.9.2.4.4 Time Difference (Delta) Operation Rising and Falling Edge Trigger Example**_ 

In Figure 7-63 the eCAP operating mode is almost the same as in previous section except Capture events are qualified as either Rising or Falling edge, this now gives both Period and Duty cycle information: Period1 = T1 + T2, Period2 = T3 + T4, …etc Duty Cycle1 (on-time %) = T1 / Period1 × 100%, etc Duty Cycle1 (off-time %) = T2 / Period1 × 100%, etc 

During initialization, you must write to the active registers for both period and compare. This will then automatically copy the init values into the shadow values. For subsequent compare updates, that is, during run-time, only the shadow registers must be used. 

**==> picture [433 x 356] intentionally omitted <==**

**----- Start of picture text -----**<br>
CEVT2 CEVT4 CEVT2 CEVT4<br>CEVT1 CEVT3 CEVT1 CEVT3 CEVT5<br>CAPx pin<br>T1 T3 T5 T8<br>FFFFFFFF<br>T2 T6<br>T4 T7<br>CTR[0−31]<br>00000000<br>MOD4<br>0 1 2 3 0 1 2 3 0<br>CTR<br>CAP1 XX CTR value at CEVT1 t4<br>CAP2 XX t1 t5<br>CAP3 XX t2 t6<br>CAP4 XX t3 t7<br>t<br>Polarity selection<br>Capture registers [1−4]<br>**----- End of picture text -----**<br>


**Figure 7-63. Capture Sequence for Delta Mode Time-Stamp, Rising and Falling Edge Detect** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 457 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-77. ECAP Initialization for CAP Mode Delta Time, Rising and Falling Edge Triggers** 

|**Register**|**Bit**|**Value**|
|---|---|---|
|ECCTL1|CAP1POL|EC_RISING|
|ECCTL1|CAP2POL|EC_FALLING|
|ECCTL1|CAP3POL|EC_RISING|
|ECCTL1|CAP4POL|EC_FALLING|
|ECCTL1|CTRRST1|EC_DELTA_MODE|
|ECCTL1|CTRRST2|EC_DELTA_MODE|
|ECCTL1|CTRRST3|EC_DELTA_MODE|
|ECCTL1|CTRRST4|EC_DELTA_MODE|
|ECCTL1|CAPLDEN|EC_ENABLE|
|ECCTL1|PRESCALE|EC_DIV1|
|ECCTL2|CAP_APWM|EC_CAP_MODE|
|ECCTL2|CONT_ONESHT|EC_CONTINUOUS|
|ECCTL2|SYNCO_SEL|EC_SYNCO_DIS|
|ECCTL2|SYNCI_EN|EC_DISABLE|
|ECCTL2|TSCTRSTOP|EC_RUN|



_**Example 7-4. Code Snippet for CAP Mode Delta Time, Rising and Falling Edge Triggers**_ 

```
// Code snippet for CAP mode Delta Time, Rising and Falling edge triggers
// Run Time ( e.g. CEVT1 triggered ISR call)
//==========================================
// Note: here Time-stamp directly represents the Duty cycle values.
    DutyOnTime1 =  ECAPxRegs.CAP2;    // Fetch Time-Stamp captured at T2
    DutyOffTime1 = ECAPxRegs.CAP3;    // Fetch Time-Stamp captured at T3
    DutyOnTime2 =  ECAPxRegs.CAP4;    // Fetch Time-Stamp captured at T4
    DutyOffTime2 = ECAPxRegs.CAP1;    // Fetch Time-Stamp captured at T1
    Period1 = DutyOnTime1 + DutyOffTime1;
    Period2 = DutyOnTime2 + DutyOffTime2;
```

458 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.9.2.4.5 Application of the APWM Mode**_ 

## _**7.3.9.2.4.5.1 Simple PWM Generation (Independent Channel/s) Example**_ 

In this example, the eCAP module is configured to operate as a PWM generator. Here a very simple single channel PWM waveform is generated from output pin APWM _n_ . The PWM polarity is active high, which means that the compare value (CAP2 reg is now a compare register) represents the on-time (high level) of the period. Alternatively, if the APWMPOL bit is configured for active low, then the compare value represents the off-time. 

**==> picture [405 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
TSCTR<br>FFFFFFFF<br>1000h<br>APRD<br>500h<br>ACMP<br>300h<br>0000000C<br>APWMx<br>(o/p pin)<br>Off−time<br>On Period<br>time<br>**----- End of picture text -----**<br>


**Figure 7-64. PWM Waveform Details of APWM Mode Operation** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

459 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Table 7-78. ECAP Initialization for APWM Mode** 

|**Register**|**Bit**|**Value**|
|---|---|---|
|CAP1|CAP1|0x1000|
|CTRPHS|CTRPHS|0x0|
|ECCTL2|CAP_APWM|EC_APWM_MODE|
|ECCTL2|APWMPOL|EC_ACTV_HI|
|ECCTL2|SYNCI_EN|EC_DISABLE|
|ECCTL2|SYNCO_SEL|EC_SYNCO_DIS|
|ECCTL2|TSCTRSTOP|EC_RUN|



## _**Example 7-5. Code Snippet for APWM Mode**_ 

```
// Code snippet for APWM mode Example 1
// Run Time (Instant 1, e.g. ISR call)
//======================
   ECAPxRegs.CAP2 = 0x300;      // Set Duty cycle i.e. compare value
// Run Time (Instant 2, e.g. another ISR call)
//======================
   ECAPxRegs.CAP2 = 0x500;      // Set Duty cycle i.e. compare value
```

## _**7.3.9.2.4.5.2 Multichannel PWM Generation with Synchronization Example**_ 

Figure 7-65 takes advantage of the synchronization feature between eCAP modules. Here 4 independent PWM channels are required with different frequencies, but at integer multiples of each other to avoid "beat" frequencies. Hence one eCAP module is configured as the Controller and the remaining 3 are Targets all receiving their synch pulse (CTR = PRD) from the controller. Note the Controller is chosen to have the lower frequency (F1 = 1/20,000) requirement. Here Slave2 Freq = 2 × F1, Slave3 Freq = 4 × F1 and Slave4 Freq = 5 × F1. Note here values are in decimal notation. Also, only the APWM1 output waveform is shown. 

460 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [408 x 624] intentionally omitted <==**

**----- Start of picture text -----**<br>
DC bus<br>Motor Motor Motor Motor<br>dc dc dc dc<br>brush brush brush brush<br>APWM1 APWM2 APWM3 APWM4<br>TSCTR<br>Master APWM(1) module<br>FFFF FFFFh<br>20,000<br>APRD(1)<br>7,000<br>ACMP(1)<br>0000 0000<br>APWM1<br>(o/p pin)<br>PRDEQ<br>(SyncOut) Time<br>Phase = 0°<br>Slave APWM(2−4) module/s<br>10,000<br>APRD(2)<br>0<br>5,000<br>APRD(3)<br>0<br>4,000<br>APRD(4)<br>0 Time<br>**----- End of picture text -----**<br>


**Figure 7-65. Multichannel PWM Example Using 4 eCAP Modules** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

461 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **Table 7-79. ECAP1 Initialization for Multichannel PWM Generation with Synchronization** 

|**Register**|**Bit**|**Value**|
|---|---|---|
|CAP1|CAP1|20000|
|CTRPHS|CTRPHS|0|
|ECCTL2|CAP_APWM|EC_APWM_MODE|
|ECCTL2|APWMPOL|EC_ACTV_HI|
|ECCTL2|SYNCI_EN|EC_DISABLE|
|ECCTL2|SYNCO_SEL|EC_CTR_PRD|
|ECCTL2|TSCTRSTOP|EC_RUN|



## **Table 7-80. ECAP2 Initialization for Multichannel PWM Generation with Synchronization** 

||**Register**|**Bit**|**Value**|
|---|---|---|---|
||CAP1|CAP1|10000|
||CTRPHS|CTRPHS|0|
||ECCTL2|CAP_APWM|EC_APWM_MODE|
||ECCTL2|APWMPOL|EC_ACTV_HI|
||ECCTL2|SYNCI_EN|EC_ENABLE|
||ECCTL2|SYNCO_SEL|EC_SYNCI|
||ECCTL2|TSCTRSTOP|EC_RUN|
|**Table**|**7-81. ECAP3 Initialization for Multichannel PWM Generation with Synchronization**|||
||**Register**|**Bit**|**Value**|
||CAP1|CAP1|5000|
||CTRPHS|CTRPHS|0|
||ECCTL2|CAP_APWM|EC_APWM_MODE|
||ECCTL2|APWMPOL|EC_ACTV_HI|
||ECCTL2|SYNCI_EN|EC_ENABLE|
||ECCTL2|SYNCO_SEL|EC_SYNCI|
||ECCTL2|TSCTRSTOP|EC_RUN|



## **Table 7-82. ECAP4 Initialization for Multichannel PWM Generation with Synchronization** 

|**Register**|**Bit**|**Value**|
|---|---|---|
|CAP1|CAP1|4000|
|CTRPHS|CTRPHS|0|
|ECCTL2|CAP_APWM|EC_APWM_MODE|
|ECCTL2|APWMPOL|EC_ACTV_HI|
|ECCTL2|SYNCI_EN|EC_ENABLE|
|ECCTL2|SYNCO_SEL|EC_SYNCO_DIS|
|ECCTL2|TSCTRSTOP|EC_RUN|



_**Example 7-6. Code Snippet for Multichannel PWM Generation with Synchronization**_ 

```
// Code snippet for APWM mode Example 2
// Run Time (Note: Example execution of one run-time instant)
//============================================================
   ECAP1Regs.CAP2 = 7000;    // Set Duty cycle i.e., compare value = 7000
   ECAP2Regs.CAP2 = 2000;    // Set Duty cycle i.e., compare value = 2000
   ECAP3Regs.CAP2 = 550;     // Set Duty cycle i.e., compare value = 550
   ECAP4Regs.CAP2 = 6500;    // Set Duty cycle i.e., compare value = 6500
```

462 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.9.2.4.5.3 Multichannel PWM Generation with Phase Control Example**_ 

In Figure 7-66, the Phase control feature of the APWM mode is used to control a 3 phase Interleaved DC/DC converter topology. This topology requires each phase to be off-set by 120° from each other. Hence if “Leg” 1 (controlled by APWM1) is the reference Leg (or phase), that is, 0°, then Leg 2 need 120° off-set and Leg 3 needs 240° off-set. The waveforms in Figure 7-66 show the timing relationship between each of the phases (Legs). Note eCAP1 module is the Controller and issues a sync out pulse to the targets (modules 2, 3) whenever TSCTR = Period value. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

463 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [410 x 561] intentionally omitted <==**

**----- Start of picture text -----**<br>
Comple− Comple− Comple−<br>mentary mentary mentary<br>and and and<br>deadband deadband deadband<br>logic logic logic<br>APWM1 APWM2 APWM3<br>Vout<br>TSCTR<br>1200<br>APRD(1)<br>700<br>APRD(1)<br>SYNCO pulse<br>(PRDEQ)<br>APWM1<br>ɸ2=120° CTRPHS(2)=800<br>APWM2<br>ɸ3=240°<br>CTRPHS(3)=400<br>APWM3<br>**----- End of picture text -----**<br>


**Figure 7-66. Multiphase (channel) Interleaved PWM Example Using 3 eCAP Modules** 

464 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-83. ECAP1 Initialization for Multichannel PWM Generation with Phase Control** 

|**Register**|**Bit**|**Value**|
|---|---|---|
|CAP1|CAP1|1200|
|CTRPHS|CTRPHS|0|
|ECCTL2|CAP_APWM|EC_APWM_MODE|
|ECCTL2|APWMPOL|EC_ACTV_HI|
|ECCTL2|SYNCI_EN|EC_DISABLE|
|ECCTL2|SYNCO_SEL|EC_CTR_PRD|
|ECCTL2|TSCTRSTOP|EC_RUN|



**Table 7-84. ECAP2 Initialization for Multichannel PWM Generation with Phase Control** 

|**Register**|**Bit**|**Value**|
|---|---|---|
|CAP1|CAP1|1200|
|CTRPHS|CTRPHS|800|
|ECCTL2|CAP_APWM|EC_APWM_MODE|
|ECCTL2|APWMPOL|EC_ACTV_HI|
|ECCTL2|SYNCI_EN|EC_ENABLE|
|ECCTL2|SYNCO_SEL|EC_SYNCI|
|ECCTL2|TSCTRSTOP|EC_RUN|



## **Table 7-85. ECAP3 Initialization for Multichannel PWM Generation with Phase Control** 

|**Register**|**Bit**|**Value**|
|---|---|---|
|CAP1|CAP1|1200|
|CTRPHS|CTRPHS|400|
|ECCTL2|CAP_APWM|EC_APWM_MODE|
|ECCTL2|APWMPOL|EC_ACTV_HI|
|ECCTL2|SYNCI_EN|EC_ENABLE|
|ECCTL2|SYNCO_SEL|EC_SYNCO_DIS|
|ECCTL2|TSCTRSTOP|EC_RUN|



_**Example 7-7. Code Snippet for Multichannel PWM Generation with Phase Control**_ 

```
// Code snippet for APWM mode Example 3
// Run Time (Note: Example execution of one run-time instant)
//============================================================
// All phases are set to the same duty cycle
  ECAP1Regs.CAP2 = 700;     // Set Duty cycle i.e. compare value = 700
  ECAP2Regs.CAP2 = 700;     // Set Duty cycle i.e. compare value = 700
  ECAP3Regs.CAP2 = 700;     // Set Duty cycle i.e. compare value = 700
```

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 465 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.10 PRU-ICSS MII_RT Module**_ 

## **7.3.10.1 PRU-ICSS MII_RT Introduction** 

The Real-time Media Independent Interface (MII_RT) provides a programmable I/O interface for the PRUs to access and control up to two MII ports. The MII_RT module can also be configured to push and pull data independent of the PRU cores. 

## **Note** 

In order to guarantee the MII_RT I/O timing values published in the device data sheet, the TX_CLK_DELAYn (where n = 0 or 1) bit field in the MII_RT_TXCFG0/1 register must be set to 0h (default value). 

## _**7.3.10.1.1 PRU-ICSS MII_RT Features**_ 

The PRU-ICSS MII_RT module supports: 

- Two MII ports 

   - Each MII port has: 

      - 32-Bytes RX L1 FIFO 

      - 64-Bytes RX L2 FIFO (two memory banks: Bank0 = 32-Bytes and Bank1 = 32-Bytes) 

      - 40-Bytes TX L1 FIFO one per port 

      - 64-Bytes TX L2 FIFO one per port 

   - Rate decoupling on TX L1 FIFO 

   - Configurable pre-amble removal on RX L1 FIFO and insertion on TX L1 FIFO 

   - Sync frame delimiter detection 

   - Configurable TX L1 FIFO trigger (10 bits with 40 ns ticks) 

- MII port multiplexer per direction to support line/ring structure 

   - Link detection through RX_ERR 

- Cyclic redundancy check (CRC) 

   - CRC32 generation on TX path 

   - CRC32 checker on RX path 

## _**7.3.10.1.2 Unsupported Features**_ 

The PRU-ICSS MII_RT module does not support: 

- Auto padding in TX L1 FIFO 

- Dynamic TX multiplexer switching during packet handling: 

   - Can allow one PRU to handle both MII interfaces and a second PRU to manage the host and switch functions. 

## _**7.3.10.1.3 PRU-ICSS MII_RT Block Diagram**_ 

Figure 7-67 shows the MII_RT in context of the PRU-ICSS. 

466 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [499 x 196] intentionally omitted <==**

**----- Start of picture text -----**<br>
32-Bytes/cycle 32-Bytes/cycle from data PRU<br>(XIN) 51.2Gbit/s (XOUT) 51.2Gbit/s 16-bit/3cycles (MOV)<br>1.07Gbit/s (32-Bytes)<br>MII_RT<br>RX L2 FIFO<br>TX L2 FIFO<br>32-BytesBank0 32-BytesBank1 (64-Bytes)<br>to data PRU<br>8-bit/cycles (MOV) R31 Interface 4B/4ns R30 Interface<br>1.6Gbit/s (32-Bytes)<br>RX L1 FIFO(32-Bytes) coupled/delayedline rate TX L1 FIFO TX_ENTX_EOF<br>(40-Bytes)<br>RX_EOF w/Preamble removal Auto<br>forwarding<br>RX Ethernet<br>TX (MII)<br>1Gb transfer domain<br>**----- End of picture text -----**<br>


**Figure 7-67. PRU-ICSS MII_RT Block Diagram** 

## **7.3.10.2 MII_RT Functional Description** 

## _**7.3.10.2.1 MII_RT Data Path Configuration**_ 

The MII_RT module supports three basic data path configurations. These configurations are compared in Table 7-86 and described in the following sections. 

**Table 7-86. MII_RT Data Path Configuration Comparison** 

|**Configuration**|**PRU Dependency**|**Data Servicing**|**Port-to-Port Latency**|
|---|---|---|---|
|Auto-forward|Snoop only|One word in flight|Low|
|8- or 16-bit processing with on-<br>the-fly modifications<br>(RX L1)|Yes|One word or byte in flight|Low|
|32-byte double buffer or ping-<br>pong processing<br>(RX L2)|Yes|Multi-words in flight|Medium (application-dependent)|



## _**7.3.10.2.1.1 Auto-forward with Optional PRU Snoop**_ 

Data is automatically forwarded from the MII RX port to the MII TX port without manipulations, as shown in Figure 7-68. This configuration does not depend on the PRU core. However, it does support an option for PRU to snoop or monitor the received data through the RX L2, shown in Figure 7-69. The PRU does not access data and status bits through R31, and it does not modify and push data. 

**==> picture [391 x 26] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX L1 TX L1<br>MII RX port RX_DV FIFO 32 bytes FIFO 40 bytes TX_DATA MII TX port<br>RX_CLK TX_EN<br>**----- End of picture text -----**<br>


**Figure 7-68. Auto-forward** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 467 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [402 x 111] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX L2<br>Bank 0<br>32 bytes of data XFR<br>PRU<br>Bank 1<br>32 bytes of data<br>RX L1 TX L1<br>MII RX port RX_DV FIFO 32 bytes FIFO 40 bytes TX_DATA MII TX port<br>RX_CLK TX_EN<br>**----- End of picture text -----**<br>


**Figure 7-69. Auto-forward with PRU Snoop** 

## _**7.3.10.2.1.2 8- or 16-bit Processing with On-the-Fly Modifications**_ 

This configuration services one byte or word in flight and has low latency. The PRU has the option to manipulate the received word and control popping data from the RX L1 FIFO and pushing it on the TX L1 FIFO. 

**==> picture [391 x 98] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU<br>RX L1 TX L1<br>MII RX port RX_DV FIFO 32 bytes FIFO 40 bytes TX_DATA MII TX port<br>RX_CLK TX_EN<br>**----- End of picture text -----**<br>


**Figure 7-70. 8- or 16-bit Processing with On-the-Fly Modifications** 

## _**7.3.10.2.1.3 32-byte Double Buffer or Ping-Pong Processing**_ 

This configuration supports high bandwidth, high efficiency transactions. Often implementations using this mode permit relaxed servicing requirements allowing the PRU to manipulate the received data before transmitting. 

Data received in this configuration is passed into the RX L2 buffer. The PRU reads multiple bytes of data from one of the RX L2 banks through the high bandwidth broadside interface and XFR instructions. The PRU can then store or manipulate data before pushing it to the TX L1 FIFO for transmission on the MII TX port. 

**==> picture [391 x 113] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX L2<br>Bank 0<br>32 bytes of data XFR Memory<br>PRU<br>Bank 1<br>32 bytes of data<br>RX L1 TX L1<br>MII RX port RX_DV FIFO 32 bytes FIFO 40 bytes TX_DATA MII TX port<br>RX_CLK TX_EN<br>**----- End of picture text -----**<br>


**Figure 7-71. 32-byte Double Buffer or Ping-Pong Processing** 

468 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.10.2.2 MII_RT Definition and Terms**_ 

## _**7.3.10.2.2.1 MII_RT Data Frame Structure**_ 

The data received and transmitted over MII conforms with the frame structure shown in Table 7-87. 

## **Table 7-87. MII_RT Frame Structure** 

Inter-frame Preamble Start of Frame Delimiter (SFD) Data Cyclic Redundancy Check (CRC) 

The data following the SFD is formatted in a 4-bit nibble structure. Figure 7-72 illustrates the nibble order. The MSB arriving first is on the LSB side of a nibble. When receiving data, the MII_RT receive logic will wait for the next nibble to arrive before constructing a byte and delivering to the PRU. 

**==> picture [268 x 96] intentionally omitted <==**

**----- Start of picture text -----**<br>
Serial Bit Stream<br>LSB MSB<br>D0 D1 D2 D3 D4 D5 D6 D7<br>MII Nibble Stream<br>D0 D1 D2 D3 D0 D1 D2 D3<br>Constructing a byte and LSB MSB LSB MSB<br>sent to PRU and TX L1 FIFO<br>First Nibble Second Nibble<br>**----- End of picture text -----**<br>


**Figure 7-72. Data Nibble Structure** 

## _**7.3.10.2.2.2 PRU R30 and R31**_ 

The PRU registers R30 and R31 are used to receive, transmit, and control the data for the PRU. As shown in Figure 7-73, the R31 is used to access data in the RX L1 FIFO, the R30 is used to transmit data from the PRU, and the R31 output is used the control the flow of receive and transmit. For more details about these registers, see the following sections. 

**==> picture [226 x 105] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU<br>R30 (W):<br>Data<br>TX Interface<br>R31 (R):<br>Data<br>RX Interface<br>R31 (W):<br>RX & TX cmd Interface<br>**----- End of picture text -----**<br>


**Figure 7-73. PRU R30, R31 Operations** 

## _**7.3.10.2.2.3 RX and TX L1 FIFO Data Movement**_ 

To advance the next data byte seen by R31, the PRU must pop the data from the RX L1 FIFO. Likewise, the PRU can push the data from R30 to the TX L1 FIFO. These operations are illustrated in Figure 7-74. 

**==> picture [149 x 104] intentionally omitted <==**

**----- Start of picture text -----**<br>
pop push<br>(R31 cmd) (R31 cmd)<br>RX L1 TX L1<br>ytes<br>-B<br>FIFO 32-Bytes FIFO 40<br>**----- End of picture text -----**<br>


**Figure 7-74. Reading and Writing FIFO Data** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

469 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.10.2.2.4 Receive CRC Computation**_ 

For the incoming data, the MII_RT calculates CRC32 and then compares against the value provided in the incoming frame. If there is a mismatch, the MII_RT signals ERROR_CRC to the PRU. If a previous node or Ethernet device appended an error nibble, the CRC calculation of received packet will be wrong because the longer frame and the frame length will end at a 4-bit boundary instead of the usual 8-bit boundary. When RX_DV goes inactive on the 4-bit boundary, the interface will assert DATA_RDY and BYTE_RDY flag with the ERROR NIBBLE. The error event is also mapped into the PRU-ICSS INTC. 

## _**7.3.10.2.2.5 Transmit CRC Computation**_ 

For the outgoing data, the MII_RT calculates the CRC32 value and inserts it into outgoing packets. The CRC value computed on each MII transmit path is also available in memory map registers that can be read by the PRU and used primarily for debug and diagnostic purposes. The CRC is inserted into the outgoing packet based on the commands received through the R31 register of the PRU. The CRC will be inserted into the TX L1 FIFO, and there must be enough room to store the CRC value in the FIFO or else the FIFO will overflow. As Table 7-88 shows, the CRC programming model supports three sequences that provide more flexibility. Note: “cmdR31” indicates write to the mentioned bits of the R31 command interface. 

**Table 7-88. TX CRC Programming Models** 

||**Table 7-88. TX CRC Programming Models**|
|---|---|
|Option 1|Step 1: cmdR31 [TX_CRC_HIGH + TX_CRC_LOW + TX_EOF]|
|Option 2|**Note: Only valid when TX L2 is disabled.**<br>Step 1: cmdR31 [TX_CRC_HIGH]<br>Step 2: wait > 6 clocks (PRU cycles)<br>Step 3: cmdR31 [TX_CRC_LOW + TX_EOF]|
|Option 3|**Note: Only valid when TX L2 is disabled.**<br>Step 1: cmdR31 [TX_CRC_HIGH]<br>Step 2: wait > 6 clocks (PRU cycles)<br>Step 3: read TX_CRC0[31-0] TX_CRC0 and TX_CRC1[31-0] TX_CRC1<br>Step 4: modify CRC[15-0]<br>Step 5: cmdR31 [TX_PUSH16 + TX_EOF + TX_ERROR_NIBBLE]|



## _**7.3.10.2.2.6 Transmit CRC Computation for fragmented frames**_ 

Fragmented frames have a special CRC32. Each fragment CRC32 is based on the previous fragements, so a running total. In addition TX_CRC_HIGH is inverted for all fragments expect the last fragment. The final fragement has a normal CRC which is based on the full frame. 

## _**7.3.10.2.3 RX MII Interface**_ 

The RX MII interface is composed of multiple components that perform various tasks - latch received data, start of frame detection, start frame delimiter detection, CRC calculation and error detection, enhanced link detection through RX error detection and interface to PRU register R31. 

Table 7-89 includes more details about the internal signals and output of these components 

## _**7.3.10.2.3.1 RX MII Receive Data Latch**_ 

The receive data from the MII interface is stored in the receive data FIFO which is 32 bytes. The PRU can access this data through the register R31. Depending on the configuration settings, the data can be latched on reception of one or two bytes. In each scheme, the configured number of nibbles is assembled before being copied into the PRU registers. Figure 7-75 shows the inputs and outputs of the data latch logic block. 

The receiver logic in MII_RT can be programmed through the MII_RT MII_RT_RXCFG0 and MII_RT MII_RT_RXCFG1 registers to remove or retain the preamble + SFD from incoming frames. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

470 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [213 x 108] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX_DV<br>BYTE_RDY<br>RX_DATA WORD_RDY<br>4x4 Bit<br>8/16 Bit RX_NIBBLE_ODD<br>Output<br>BYTE1 (RX FIFO DATA)<br>RX_CLK<br>BYTE2 (RX FIFO DATA)<br>**----- End of picture text -----**<br>


**Figure 7-75. RX Data Latch** 

## _**7.3.10.2.3.2 RX MII Start of Frame Detection**_ 

The start of frame detection logic tracks the frame boundaries and signals the beginning of a frame to other components of the PRU-ICSS. This logic detects two events: 

- Start of Frame (SOF) event that occurs when Receive Data Valid MII signal is sampled high. 

- Start of Frame Delimiter (SFD) event is seen on MII Receive Data bus. 

These event triggers can be used to add timestamp to the frames. The notification for these events is available through R31 as well as through INTC which is integrated in the PRU-ICSS. Figure 7-76 shows the inputs and outputs of the start of frame detection logic block. 

**==> picture [141 x 68] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX_CLK<br>SOF<br>RX_DV Frame<br>Detection<br>SFD<br>RX_DATA<br>**----- End of picture text -----**<br>


**Figure 7-76. RX MII Start of Frame Detection** 

## _**7.3.10.2.3.3 CRC Error Detection**_ 

For each incoming frame, the CRC is calculated by the MII_RT and compared against the CRC included in the frame. When the two values do not match, a CRC error is flagged. The ERROR_CRC indication is available in the register interface (PRU R31 Receive Interface) as well as in the FIFO interface (RX L2 Status Interface). It is also provided to the INTC which is integrated in the PRU-ICSS. Figure 7-77 shows the inputs and outputs of CRC error detection logic block. 

**==> picture [178 x 76] intentionally omitted <==**

**----- Start of picture text -----**<br>
SFD<br>RX_CLK<br>CRC Checksum ERROR_CRC<br>RX_DV and<br>Error Detection<br>RX_DATA<br>**----- End of picture text -----**<br>


**Figure 7-77. CRC Error Detection** 

## _**7.3.10.2.3.4 RX Error Detection and Action**_ 

The RX error detection logic tracks the receive error signaled by the physical layer and informs the PRU-ICSS INTC whenever an error is detected. Figure 7-78 shows the inputs and outputs of the RX error detection logic block. Note the following dependencies: 

- RX_ERR signal is only sampled when RX_DV is asserted. 

- All nibbles are discarded post RX_ERR event, including the nibble which had RX_ERR asserted. This state will remain until EOF occurs. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 471 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

- Due to this fact, RX L1 FIFO and RX L2 FIFO will never receive any data with RX_ERR or post RX_ERR during that frame. 

## **Note** 

RX error detection logic is supported only for MII mode and this feature is not supported for RGMII and SGMII modes of operation. 

**==> picture [179 x 41] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX_ERR RX Error RX_ERR32<br>Detection 0/1 (interrupt event)<br>**----- End of picture text -----**<br>


**Figure 7-78. RX Error Detection** 

## **Note** 

Note for SGMII and RGMII modes, RX_ERR is sampled after SFD and during the payload if one occurs then it can be detected by R31 and/or INTC same as MII. The MII RX_ERR counter counts for every MII nibble. 

This submodule also keeps track of a running count of receive error events within a 10 μs error detection window, as shown in Figure 7-79. The INTC is notified when 32 or more events have occurred in a 10 μs error detection window. The error detection window is not a sliding window but a non-overlapping window with no specific initialization time with respect to incoming traffic. The timer starts its 10 μs counts immediately after de-assertion of reset to the MII_RT module. 

**==> picture [252 x 138] intentionally omitted <==**

**----- Start of picture text -----**<br>
10 μs<br>(A)<br>10 μs<br>(B)<br>**----- End of picture text -----**<br>


- A. There are fewer than 32 consecutive error events in the 10 μs window. The detection module will not forward to the interrupt controller (INTC). 

- B. There are more or equal to 32 error events in the 10 μs window. The detection module will notify the interrupt controller (INTC). 

## **Figure 7-79. Error Detection Window with Running Counter** 

## _**7.3.10.2.3.5 RX Data Path Options to PRU**_ 

There are two data path options for delivering received data to the PRU, described further in the subsequent sections: 

1. RX MII port → RX L1 FIFO → PRU (one word in flight) 

2. RX MII port → RX L1 FIFO → RX L2 buffer → PRU (multi-word in flight) 

Once the PRU has received RX data, the PRU can both manipulate received data or send data to the TX MII Interface. 

472 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.10.2.3.6 RX MII Port → RX L1 FIFO → PRU**_ 

The RX L1 FIFO to PRU interface is depicted in Figure 7-80. In this mode, the data received from the MII interface is fed into the 32-byte RX L1 FIFO. The first data byte into the FIFO is automatically available in R31 of the PRU. Therefore, the PRU firmware can directly operate on this data without having to read it in a separate instruction. This allows the PRU to access receive data with low latency. 

**==> picture [256 x 89] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU<br>R31<br>RX L1<br>RX_DV<br>MII RX port FIFO 32 bytes<br>RX_CLK<br>**----- End of picture text -----**<br>


**Figure 7-80. RX L1 to PRU Interface** 

When the new data is received, the PRU is provided with up to two bytes at a time in the R31 register, as shown in Figure 7-81. Once the PRU processes the incoming data, it instructs the MII_RT by writing to the R31 command interface bits to pop one or two bytes of data from the 32-byte RX FIFO. The pop operation causes current contents of R31 to be refreshed with new data from the incoming packet. Each time the data is popped, the status bits change to indicate so. If the pop is completed and there is no new data, the status bits immediately change to indicate no new data. 

Note: The current R31 content, including data, will be lost after issuing the pop operation. If this information needs to be accessed later, the PRU should store the existing R31 content before popping new data. 

**==> picture [364 x 183] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU - R31 0:7 8:15 16 17 18 19 20 21 22 23 24 25:29 30:31<br>RESERVED<br><ERR> bits<br>FIFO ERROR_CRC<br>ERROR_NIBBLE<br>RX_SOF<br>MII RX_DV<br>RX_SFD<br>MII RX_CLK<br>RX_EOF<br>RX_ERROR<br>WORD_RDY<br>BYTE_RDY<br>DATA_RDY/TX_EOF<br>**----- End of picture text -----**<br>


**Figure 7-81. MII RX Data to PRU R31 (R) and RX FIFO** 

Table 7-89 describes the receive interface data and status contents provided by the R31 register. These contents are available when R31 is read. To configure this register, the PRU GPI mode should be set for MII_RT mode in the CFG register space. Note the following: 

1. If the data from receive path is not read in time, it could cause an overflow event because the data is still continuously provided to the 32-byte receive FIFO. Due to the receive FIFO overflow, the data gets automatically discarded to avoid lack of space in the FIFO. At the same time, an interrupt is raised to the INTC through a system event (PRU<n>_RX_OVERFLOW). To detect an overflow condition, the PRU should poll for this system event condition and a RX RESET command through the R31 command interface is required to clear out from this condition. Note that the received Ethernet frame is corrupted and should not be used for further processing as bytes have been dropped due to the overflow condition. A FIFO reset is recommended. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 473 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

2. The receive data in the R31 register is available following synchronization to the PRU clock domain. So, there is a finite delay (120 ns) when data is available from MII interface and it is accessible to the PRU. 

3. The receive FIFO also has the capability to be reset through software. When reset, all contents of receive FIFO are purged and it may result in the current frame not being received as expected. When a frame is being received and the PRU resets the RX FIFO, the remaining frame is not placed into the RX FIFO. However, any new frame arriving on the receive MII port will be stored in the FIFO. 

474 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-89. PRU R31: Receive Interface Data and Status (Read Mode)** 

|**Bits**|**Field Name**|**Description**|
|---|---|---|
|31-30|RESERVED|In case of register interface, these bits are provided to PRU by other<br>modules in PRU-ICSS. From the MII_RT module point of view, these<br>bits are always zero.|
|29|RX_MIN_FRM_CNT_ERR|RX_MIN_FRM_CNT_ERR is set to 1 when the count of total bytes of<br>incoming frame is less than the value defined by RX_MIN_FRM_CNT.<br>RX_MIN_FRM_CNT_ERR is cleared by RX_ERROR_CLR.<br>Cleared by RX_ERROR_CLR or RX_L2_DONE.<br>Note, during backpressure the status will not get updated by a new<br>paket in L1 FIFO. The flag is valid for the current paket in L2 FIFO.|
|28|RX_MAX_FRM_CNT_ERR|RX_MAX_FRM_CNT_ERR is set to 1 when the count of total<br>bytes of incoming frame is more than the value defined by<br>RX_MAX_FRM_CNT_ERR. RX_MAX_FRM_CNT_ERR is cleared by<br>RX_ERROR_CLR.<br>Cleared by RX_ERROR_CLR or RX_L2_DONE.<br>Note, during backpressure the status will not get updated by a new<br>paket in L1 FIFO. The flag is valid for the current paket in L2 FIFO.|
|27|RX_EOF_ERROR|RX_EOF_ERROR is set to 1 when an RX_EOF event or RX_ERROR<br>event occurs. RX_EOF_ERROR is cleared by RX_ EOF_CLR and/or<br>RX_ ERROR_CLR.|
|26|RX_MAX_PRE_CNT_ERR|RX_MAX_PRE_CNT_ERR is set to 1 when the number of<br>nibbles equaling 0x5 before SFD event (0xD5) is more than the<br>value defined by PRUSS_MII_RT_RX_PCNT0/1 [RX_MAX_PCNT].<br>RX_MAX_PRE_CNT_ERR is cleared by RX_ERROR_CLR.|
|25|RX_ERR|RX_ERR is set to 1 when pr1_mii0/1_rxer is asserted while<br>pr1_mii0/1_rxdv bit is set. RX_ERR is cleared by RX_ERROR_CLR.|
|24|ERROR_CRC|ERROR_CRC indicates that the frame has a CRC mismatch. This bit is<br>valid when the RX_EOF bit is set. It should be noted that ERROR_CRC<br>bit is ready in early status, which means it is calculated before data is<br>available in RXL1 FIFO. ERROR_CRC is cleared by RX_ERROR_CLR.<br>Cleared by RX_ERROR_CLR or RX_L2_DONE.<br>Note, during backpressure the status will not get updated by a new<br>paket in L1 FIFO. The flag is valid for the current paket in L2 FIFO.|
|23|ERROR_NIBBLE|ERROR_NIBBLE indicates that the frame ended in odd nibble. It should<br>be considered valid only when the RX_EOF bit and pr1_mii0/1_rxdv<br>are set. Nibble counter is enabled post SFD event. It should be noted<br>that ERROR_NIBBLE bit is ready in early status, which means it is<br>calculated before data is available in RXL1 FIFO. ERROR_NIBBLE is<br>cleared by RX_ERROR_CLR.|
|22|RX_SOF|RX_SOF transitions from low to high when the frame data starts to<br>arrive and pr1_mii0/1_rxdv is asserted. Note: There will be a small<br>sync delay of 0ns – 5ns. The recommended time to clear this bit via<br>RX_SOF_CLR is at the end of frame (EOF). It should be noted that<br>RX_SOF bit is ready in early status, which means it is calculated before<br>data is available in RXL1 FIFO.|
|21|RX_SFD|RX_SFD transitions from low to high when the SFD sequence (0xD5)<br>post RX_SOF is observed on the receive MII data. The recommended<br>time to clear this bit via RX_SFD_CLR is at the end of frame (EOF). It<br>should be noted that RX_SFD bit is ready in early status, which means it<br>is calculated before data is available in RXL1 FIFO.|
|20|RX_EOF|RX_EOF indicates that the frame has ended and pr1_mii0/1_rxdv is de-<br>asserted. It also validates the CRC match bit. Note: There will be a small<br>sync delay of 0ns – 5ns. It should be noted that RX_EOF bit is ready<br>in early status, which means it is calculated before data is available in<br>RXL1 FIFO. Note: Also if RX_L2_EOF_SCLR_DIS is set, then this flag<br>will remain asserted when RX_L2 is enabled until RX_EOF_CLR.<br>Cleared by RX_ERROR_CLR or RX_L2_DONE.<br>Note, during backpressure the status will not get updated by a new<br>paket in L1 FIFO. The flag is valid for the current paket in L2 FIFO.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 475 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-89. PRU R31: Receive Interface Data and Status (Read Mode) (continued)** 

|**Bits**|**Field Name**|**Description**|
|---|---|---|
|19|RX_ERROR|RX_ERROR indicates one or more of the following errors occurred:<br>•<br>RX_MAX/MIN_FRM_CNT_ERR<br>•<br>RX_MAX/MIN_PRE_CNT_ERR<br>•<br>RX_ERR<br>RX_ERROR is cleared by RX_ERROR_CLR.|
|18|WORD_RDY|WORD_RDY indicates that all four nibbles in R31 have valid data.<br>There is a 2 clock cycle latency from the command RX_POP16 to<br>WORD_RDY update. Therefore, firmware needs to insure it does not<br>read WORD_RDY until 2 clock cycles after RX_POP16.|
|17|BYTE_RDY|BYTE_RDY indicates that the lower two nibbles in R31 have valid<br>data. There is a 2 clock cycle latency from the command RX_POP8<br>to BYTE_RDY update. Therefore, PRU firmware needs to insure it does<br>not read BYTE_RDY until 2 clock cycles after RX_POP8.|
|16|DATA_RDY/ TX_EOF|When RX_DATA_RDY_MODE_DIS = 0:<br>DATA_RDY indicates there is valid data in R31 ready to be read.<br>This bit goes to zero when the PRU does a POP8/16 and there is<br>no new data left in the receive MII port. This bit is high if there is<br>more receive data for PRU to read. There is a 2 clock cycle latency<br>from the command RX_POP16/8 to WORD_RDY/BYTE_RDY update.<br>Therefore, PRU firmware needs to insure it does not read BYTE_RDY/<br>WORD_RDY until 2 clock cycles after RX_POP16/8.<br>When RX_DATA_RDY_MODE_DIS = 1:<br>TX_EOF indicates an TX EOF event (i.e. a 1 --> 0 transition on TX_EN)<br>has occurred. This bit will clear when TX_RESET is set or when new<br>data is first loaded. PRU firmware can wait until TX_EOF = 1, then start<br>a new TX Frame by immediately loading new data.|
|15-8|BYTE1|Data Byte 1. This data is available such that it is safe to read by the<br>PRU when the DATA_RDY/BYTE_RDY/WORD_RDY bits are asserted.|
|7-0|BYTE0|Data Byte 0. This data is available such that it is safe to read by the<br>PRU when the DATA_RDY/BYTE_RDY/WORD_RDY bits are asserted.|



## _**7.3.10.2.3.7 RX MII Port → RX L1 FIFO → RX L2 Buffer → PRU**_ 

The RX L2 is an optional high performance buffer between the RX L1 FIFO and the PRU. Figure 7-82 illustrates the receive data path using RX L2 buffer. This data path is characterized by multi-word in flight transactions. 

**==> picture [334 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU<br>RX L2<br>Bank 0 R2<br>32 bytes of data XFR …<br>R13<br>Bank 1<br>32 bytes of data R18<br>R31<br>RX L1<br>MII RX port RX_DV FIFO 32 bytes<br>RX_CLK<br>**----- End of picture text -----**<br>


**Figure 7-82. RX L2 to PRU Interface** 

The 64-byte RX L2 buffer is divided into two 32 byte banks, or ping/pong buffers. When the RX L2 is enabled, the incoming data from the MII RX port will transmit first to the 32 byte RX L1 FIFO. RX L1 pushes data into RX L2, starting when the first byte is ready until the final EOF marker. The RX L2 buffer will apply backpressure to the RX L1 FIFO after RX_L2_EOF event occur and until RX_L2_DONE event. Therefore, it is the PRU 

476 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

firmware’s responsibility to fetch the data in RX L2 before it is overwritten by the cyclic buffer. The RX L1 will remain near empty, with only one byte (nibble) stored. 

Each RX L2 bank holds up to 32 bytes of data, and every four nibbles (or 16 bits) of data has a corresponding 8-bit status. The data and status information are stored in packed arrays. In each bank, R2 to R9 contains the data packed array and R10 to R13 contains the status packed array. Figure 7-83 shows the relationship of the data registers and status registers. The RX L2 status registers record status information about the received data, such as ERROR_CRC, RX_ERROR, STATUS_RDY, etc. The RX L2 status register details are described in Table 7-90. Note: RX_RESET clears all Data and Status elements and resets R18. 

|Data Register<br>Status Register|R2|R3|R4|R5|R6|R7|R8|R9|
|---|---|---|---|---|---|---|---|---|
||||||||||
||R10||R11||R12||R13||



**Figure 7-83. Data and Status Register Dependency** 

## _**7.3.10.2.3.7.1 RX L2 Status in mode 0, none IET mode (when ICSS_M_CFG[2] RX_L2_G_EN= 0h)**_ 

**Table 7-90. RX L2 Status in mode 0** 

|**Bit**|**Field Name**|**Description**|
|---|---|---|
|7|ERROR_CRC|ERROR_CRC indicates that the frame has a CRC mismatch. This bit is<br>valid when the RX_EOF bit is set. It should be noted that ERROR_CRC<br>bit is ready in early status, which means it is calculated before data is<br>available in RX L1 FIFO. ERROR_CRC will only be set for one entry,<br>self clear on next entry.|
|6|ERROR_NIBBLE|ERROR_NIBBLE indicates that the frame ended in odd nibble. It should<br>be considered valid only when the RX_EOF bit and pr1_mii0/1_rxdv<br>are set. Nibble counter is enabled post SFD event. It should be noted<br>that ERROR_NIBBLE bit is ready in early status, which means it is<br>calculated before data is available in RX L1 FIFO. ERROR_NIBBLE will<br>only be set for one entry, self clear on next entry.|
|5|RX_SOF|RX_SOF transitions from low to high when the frame data starts to<br>arrive and pr1_mii0/1_rxdv is asserted. Note: There will be a small sync<br>delay of 0ns – 5ns. It should be noted that RX_SOF bit is ready in early<br>status, which means it is calculated before data is available in RX L1<br>FIFO. RX_SOF will only be set for one entry, self clear on next entry.|
|4|RX_SFD|RX_SFD transitions from low to high when the SFD sequence (0xD5)<br>post RX_SOF is observed on the receive MII data. It should be noted<br>that RX_SFD bit is ready in early status, which means it is calculated<br>before data is available in RX + L1 FIFO. RX_SOF will only be set for<br>one entry, self clear on next entry.|
|3|RX_EOF|RX_EOF indicates that the frame has ended and pr1_mii0/1_rxdv is de-<br>asserted. It also validates the CRC match bit. Note: There will be a small<br>sync delay of 0ns – 5ns. It should be noted that RX_EOF bit is ready<br>in early status, which means it is calculated before data is available in<br>RXL1 FIFO. If RX_L2_EOF_SCLR_DIS = 1, then RX_EOF will remain<br>set until RX_EOF_CLR event. Otherwise, RX_ERROR is self-clearing<br>on next entry.|
|2|RX_ERROR|RX_ERROR indicates one or more of the following errors occurred:<br>•<br>RX_MAX/MIN_FRM_CNT_ERR<br>•<br>RX_MAX/MIN_PRE_CNT_ERR<br>•<br>RX_ERR<br>RX_ERROR is cleared by RX_ERROR_CLR.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 477 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-90. RX L2 Status in mode 0 (continued)** 

|**Bit**|**Field Name**|**Description**|
|---|---|---|
|1|STATUS_RDY|STATUS_RDY is set when RX_EOF or write pointer advanced by 2.<br>This is a simple method for software to determine if RX_EOF event has<br>occurred or new data is available. If RX_EOF is not set, all status bits<br>are static.|
|0|RX_ERR|RX_ERR is set to 1 when pr1_mii0/1_rxer is asserted while<br>pr1_mii0/1_rxdv bit is set. It will get set for first pr1_mii0/1_rxer event<br>and self clear on SOF for the next FRAME.|



## _**7.3.10.2.3.7.2 RX L2 XFR Identification**_ 

Bank 0 and Bank 1 are used as ping/pong buffers. RX L2 supports the reading of a write pointer in R18 that allows software to determine which bank has active write transactions, as well as the specific write address within packed data arrays. 

The PRU interacts with the RX L2 buffer using the high performance XFR read instructions and broadside interface. Table 7-91 shows the device XFR ID numbers for each bank. 

**Table 7-91. RX L2 XFR ID** 

|**Device ID**|**Function**|**Description**|
|---|---|---|
|20|Selects RX L2 Bank0|R2:R9 Data packed array<br>R10:R13 Status packed array<br>mode 0|
|21|Selects RX L2 Bank1|R2:R9 Data packed array<br>R10:R13 Status packed array<br>mode 0|
|20/21|Byte pointer of current write|R18[5-0] Pointer indicating location of current write in<br>data packed array.<br>0 = Bank0.R2.Byte0 (default and reset value)<br>1 = Bank0.R2.Byte1<br>2 = Bank0.R2.Byte2<br>3 = Bank0.R2.Byte3<br>4 = Bank0.R3.Byte0<br>…<br>63=Bank1.R9.Byte3|



## _**7.3.10.2.3.7.3 RX L2 XFR Status**_ 

XFR read transactions are passive and have no effect on any status or other states in RX L2. The firmware can also read R18 to determine which Bank has active write transactions and the location of the transaction. With this information, the firmware can read multiple times the stable preserved data. Note: When RX L1 data is written to RX L2, the next status byte gets cleared at the same time the current status byte gets updated. The rest of the status buffer is persistent. When software is accessing any register of the ping/ pong buffer, software needs to issue an XFER read transaction to fetch the latest/current state of the ping/pong buffer. The PRU registers will not reflect the current snapshot of L2 unless an XFER is issued by software. 

## _**7.3.10.2.3.7.4 Broadside Stitch FIFO**_ 

A simple 2 deep by 32 Byte Wide broadside FIFO is attached to ID = 08 to enable the firmware to efficiently pack fragments into aligned data words. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

478 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-92. RX L2 XFR ID** 

|**Device ID**|**Function**|**Description**|
|---|---|---|
|08|64 Bytes XOUT 1 Byte to 32 Bytes, LSB justify XIN<br>32 Bytes. Note: FIFO has less than 32 Bytes, it will<br>only return the valid data LSB justified|R2:R9 Data packed array|
|08|It will subtract 4 bytes from the current wr_ptr|R10[0] Control|
|08|It will reset the rd and wr ptrs|R10[1] Reset|



## _**7.3.10.2.4 PRU-ICSS TX MII Interface**_ 

The PRU core directly drives the MII transmit interface via its R30 internal register. The contents of R30 register and RX Data from receive interface are taken and fed into a transmit FIFO (TX L2 FIFO - 64 Bytes). 

Data to be transmitted is loaded into the TX L1 FIFO. The transmit FIFO (TX L1) stores up to 40 Bytes of transmit data. Note that this includes the preamble bytes. From the transmit FIFO (TX L1), the data is sent to the MII TX port of the PHY by the MII_RT transmit logic. 

The transmit FIFO also has the capability to be reset through software (TX_RESET). When reset, all contents of transmit FIFO are purged and this may result in a frame not getting transmitted as expected, if the transmission is already ongoing. Any new data written in the transmit FIFO results in a new frame being composed and transmitted. An overflow event will require a TX_RESET to recover from this condition. 

There are four dependencies that must be true for TX_EN to assert: 

1. TX L1 FIFO not empty 

2. Interpacket gap (IPG) timer expiration 

3. RX_DV to TX_EN timer expiration 

4. TX_EN compare timer expiration 

The transmit interface also provides an underflow error signal in case there was no data loaded when TX_EN triggered. The transmit underflow signal is mapped to the INTC in PRU-ICSS. The current FIFO fill level cannot be accessed by PRU firmware. The firmware can issue an R31 command via R31 bit 29 (TX_EOF) to indicate that the last byte has been written into the TX FIFO. 

## _**7.3.10.2.4.1 TX Data Path Options to TX L1 FIFO**_ 

There are two data path options for delivering data to the TX L1 FIFO and transmit port, described further in the subsequent sections: 

1. PRU → TX L1 FIFO → TX MII port 

2. RX L1 FIFO → TX L1 FIFO → TX MII port 

## _**7.3.10.2.4.1.1 PRU → TX L1 FIFO → TX MII Port**_ 

The PRU can be used to feed data into the TX L1 FIFO using the R30 and R31 registers, shown in Figure 7-84. The PRU has the option to write up two or four bytes of R30 and then pushes the data into the TX L1 FIFO by writing to the R31 command interface. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 479 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [278 x 190] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU0/1 32-Bytes/cycle<br>(XOUT) CRC32<br>TX L2 FIFO<br>64-Bytes<br>R30<br>R31<br>ICSSM_TXCFGn[8] Transmit Multiplexer<br>TX_MUX_SELn<br>4-Bytes/5ns<br>TX_EN<br>TX_EOF<br>TX L1 FIFO<br>40-Bytes TX_DATA<br>MII TX port<br>n = 0 or 1<br>**----- End of picture text -----**<br>


**Figure 7-84. PRU to TX L1 FIFO Interface** 

## _**7.3.10.2.4.1.1.1 TX L2 FIFO Features**_ 

- 64-Bytes deep TX L2 FIFO which feeds data into a 40-Bytes deep TX L1 FIFO 

- Maximum of 64-Bytes Broad Side load, minimum of 1-Byte Broad Side load, R2.b0(start) 

- **Note: MII_RT_TXCFG0/1[3] TX_BYTE_SWAPn bit (where n = 0 or 1) is not supported for TX L2 FIFO.** 

- • FIFO level status available through MII_RT_TX_FIFO_LEVEL0[7-0] TX_FIFO_LEVEL0 and MII_RT_TX_FIFO_LEVEL1[7-0] TX_FIFO_LEVEL1 registers 

- 2 FIFO threshold events: 32-Bytes (available and empty) or 64-Bytes (available) 

- Total bytes sent for a current/last frame is available for software 

- New frame can start after TX L2 FIFO is empty, but before TX L1 FIFO is empty from an old frame 

   - **Note: Only supported for RGMII and SGMII modes of operation** 

   - New frame can start after 5 or more core clock cycles after it is drained, this is required to finish the CRC for the first frame 

**Table 7-93. TX L2 XFR Mapping** 

|**Device ID**|**Function**|**Description**|
|---|---|---|
|40|Data|R17:R2 Data, XOUT Only<br>1-Byte to 64-Bytes in size<br>LSB packed and no gaps, for example<br>64-Bytes push R17:R2<br>32-Bytes push R9:R2<br>16-Bytes push R5:R2<br>4-Bytes push R2<br>7-Bytes push R3(b2.b0):R2<br>1-Bytes push R2(b0)<br>Can do back to back|
|40|Control|Control of TX L2 FIFO|
|40|Status|Status of TX L2 FIFO|



**Table 7-94. TX L2 Control** 

|**BS ID**|**BS R**|**Bit**|**Name**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|---|---|
|40|R18|1-0|TAG insertion mode|WO|0h|Sets the TAG mode for next frame or current frame. It will have a<br>one time action per frame. After action, software must rearm for<br>a new action 1 cmd per packet.<br>MII_RT_TXCFG0/1[1] TX_AUTO_PREAMBLEn bit (where n = 0<br>or 1) must be set to 1h.<br>Note: This bit is self cleared.|



480 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-94. TX L2 Control (continued)** 

|**BS ID**|**BS R**|**Bit**|**Name**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|---|---|
|40|R18|2|VLAN removal|WO|0h|If set, it will remove 4-Bytes of VLAN.<br>This is only valid when TX L2 FIFO is enabled<br>through ICSS_M_CFG[1] TX_L2_ENABLE bit (value 1h) and<br>MII_RT_TXCFG0/1[1] TX_AUTO_PREAMBLEn = 1h (where n<br>= 0 or 1) then Byte13, Byte14, Byte15, Byte16 will get removed.<br>Note: Byte1 is the first byte which is pushed by PRU<br>core. Note that the first 2 bytes of the VLAN must match<br>the value in MII_RT_TX_VLAN_TYPE_TAG_PORT0/1[15-0]<br>TX_VLAN_TYPE_TAG bit field (reset state is 81h). If not, the<br>4-Bytes will NOT get removed.<br>A RXVLANRemoval flag will get set if the action occurred<br>Allow all combos of TAG + VLAN IN.<br>Note: This will be defined in a matrix.<br>Note: This bit is self cleared.|
|40|R18|4|EXP_FRAME|WO|0h|Must be set for all EXP_FRAME. We have 3 types of frames:<br>•<br>Implicit EXP_FRAME not set PRE_FRAME<br>•<br>Not set SMD == 0xd5 EXP_FRAME (use a SMD_EXP)<br>•<br>EXP_FRAME set PRE_FRAME not set.<br>PRE_FRAME (use MII_RT_SMDT1S_CFG .SMDT1S_n<br>for intial and MII_RT_SMDT1C_CFG .SMDT1C_n +<br>MII_RT_FRAG_CNT_CFG .FRAG_CNT_n for non intial)<br>EXP_FRAME set PRE_FRAME not set.<br>Note: This bit is self cleared on EOF.|
|40|R18|6|RESERVED|R|0h|Reserved|
|40|R18|7|EOF_MCRC_REQ|WO||Set this bit before TX L1 FIFO is empty to generate a MCRC vs<br>CRC.<br>Note: This bit is self cleared on EOF.|
|40|R18|11-8|RESERVED|R|0h|Reserved|



**Table 7-95. TX L2 Status** 

|**BS ID**|**BS R**|**Bit**|**Name**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|---|---|
|40|R19|11-0|TXL2ByteSentCoun<br>t|R|0h|This bit field defines the number of bytes transmitted to TX<br>L1 FIFO. The count will remain persistent until the next frame<br>starts. This will get used to determine the number of bytes which<br>got transmitted after a Preemption event. This includes all data<br>pushed by the PRU core, which did get transmitted. It does not<br>include the CRC.|
|40|R19|12|RESERVED|R|0h|Reserved|
|40|R19|13|RXVLAN Removal|R/W1C|0h|This bit will be set when VLAN removal occured. VLAN<br>removal will only occur if TPID value is equal to<br>the value in MII_RT_TX_VLAN_TYPE_TAG_PORT0/1[15-0]<br>TX_VLAN_TYPE_TAG bit field (reset state is 81h). Software can<br>clear sticky used for debug.|
|40|R19|14|RESERVED|R|0h|Reserved|
|40|R19|15|RESERVED|R|0h|Reserved|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

481 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-95. TX L2 Status (continued)** 

|**BS ID**|**BS R**|**Bit**|**Name**|**Type**|**Reset**|**Description**|
|---|---|---|---|---|---|---|
|40|R19|22-16|TXL2Occ|R|0h|This bit field defines the current number of bytes in TX L2 FIFO.<br>0h: 0 bytes, or empty FIFO buffer<br>1h: 1 byte<br>...<br>64h = 64 bytes, or full FIFO buffer|



**Table 7-96. TX L2 TAG Modes** 

|**TAG Mode**|**At**|**What to Push/Add to the Frame**|
|---|---|---|
|0|None|Nothing|
|1|Push TAG1|Byte 13 = VLAN_PORT<1/0>[7-0]<br>Byte 14 = VLAN_PORT<1/0>[15-8]<br>Byte 15 = VLAN_PORT<1/0>[23-16]<br>Byte 16 = VLAN_PORT<1/0>[31-24]<br>Used for Host.<br>Host -> PRU-ICSS -> add VLAN TAG -> Port SFD offset issues|
|2|Push TAG2|Byte 13 = HTAG_PORT<1/0>[7-0]<br>Byte 14 = HTAG_PORT<1/0>[15-8]<br>Byte 15 = HTAG_PORT<1/0>[23-16]<br>Byte 16 = HTAG_PORT<1/0>[31-24]<br>Byte 17 = SEQ_PORT<1/0>[7-0]<br>Byte 18 = SEQ_PORT<1/0>[15-8]|
|3|Push TAG3|Byte 13 = VLAN_PORT<1/0>[7-0]<br>Byte 14 = VLAN_PORT<1/0>[15-8]<br>Byte 15 = VLAN_PORT<1/0>[23-16]<br>Byte 16 = VLAN_PORT<1/0>[31-24]<br>Byte 17 = HTAG_PORT<1/0>[7-0]<br>Byte 18 = HTAG_PORT<1/0>[15-8]<br>Byte 19 = HTAG_PORT<1/0>[23-16]<br>Byte 20 = HTAG_PORT<1/0>[31-24]<br>Byte 21 = SEQ_PORT<1/0>[7-0]<br>Byte 22 = SEQ_PORT<1/0>[15-8]|



## _**7.3.10.2.4.1.1.2 TX Insertion**_ 

There are 3 TAG Insertion modes that software can select. Note that the mode must be selected before the first byte is pushed into the TX FIFO. The values, pushed into the TX FIFO are defined in the MII_RT_TX_FIFO_LEVEL0/1[7-0] TX_FIFO_LEVELn registers (where n = 0 or 1). 

**Table 7-97. TX VLAN_TAG Cases** 

|**Case**|**RM VLAN**|**ADD VLAN**|**ADD HSR**|**In packet**|**Out packet**|
|---|---|---|---|---|---|
|1|1|0|0|If pkt[B13:B14] == vlan_type_id|B16, B15, B14, B13 will be removed.<br>If packet is less than 64-Bytes, 0s<br>will get added before the CRC.|
|2|1|0|0|If pkt[B13:B14] != vlan_type_id|No effect.|
|3|0|1|0|X|VLAN_TAG added 4-Bytes. Start<br>B13.|
|4|0|0|1|X|HSR_TAG added 6-Bytes. Start B13.|
|5|0|1|1|X|VLAN+TAG and HSR_TAG added<br>10-Bytes. Start B13.|
|6|1|1|0|If pkt[B13:B14] == vlan_type_id|B16, B15, B14, B13 will be replaced<br>with VLAN_TAG.|
|7|1|1|0|If pkt[B13:B14] != vlan_type_id|No effect.|



482 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-97. TX VLAN_TAG Cases (continued)** 

|**Case**|**RM VLAN**|**ADD VLAN**|**ADD HSR**|**In packet**|**Out packet**|
|---|---|---|---|---|---|
|8|1|1|1|If pkt[B13:B14] == vlan_type_id|B16, B15, B14, B13 will be replaced<br>with VLAN_TAG. Then HSR_TAG<br>wil be added.|
|9|1|1|1|If pkt[B13:B14] != vlan_type_id|No effect.|
|10|1|0|1|If pkt[B13:B14] = vlan_type_id|B16, B15, B14, B13 will be removed<br>and HSR_TAG added 6-Bytes. Start<br>B13.|
|11|1|0|1|If pkt[B13:B14] != vlan_type_id|HSR_TAG added 6-Bytes. Start B13|



## _**7.3.10.2.4.1.1.3 TX Preemption**_ 

Case 1) Preemptible frame which got fragmented. 

1. Idle -> preemptible frame when: 

   - PRE_FRAME is set before first data push 

2. preemptible -> frag when 

- EOF_MCRC_REQ is set after the last data is pushed into TX L2 FIFO and before TX L1 FIFO is empty 

- 3. frag -> frag when 

   - PRE_FRAME is set before first data push and EOF_MCRC_REQ is set after the last data is pushed into TX L2 FIFO and before TX L1 FIFO is empty 

4. frag -> Ifrag when: 

   - PRE_FRAME is set before first data push and TX_EOF_REQ set after the last data is pushed into TX L2 FIFO and before TX L1 FIFO is empty 

5. Ifrag -> Idle when CRC is pushed into TX L1 FIFO 

Case 2) Preemptible frame which did not get fragmented. 

1. Idle -> preemptible frame when: 

   - PRE_FRAME is set before first data push 

2. preemptible -> Idle when 

   - TX_EOF_REQ is set before TX L1 FIFO is empty 

Note: Express frames can and will occur between the fragments. 

## **Rules:** 

- Preemptible must get set before the first data is pushed into TX L2 FIFO 

- EOF_MCRC_REQ is set after the last data is pushed into TX L2 FIFO and before TX L1 FIFO is empty 

- TX_EOF_REQ can only get asserted on the last frag or preemptible frame which did not get fragmented. It can not get asserted in none last fragments. 

Note: TX_EOF_REQ can not get asserted when EOF_MCRC_REQ is asserted. 

## _**7.3.10.2.4.1.1.3.1 TX Preemption Programming Model**_ 

Start a new frame. 

1. Wait until R31.TX_EOF event 

2. Load data into TX L2 FIFO until the full frame is completed 

3. Issue a R30.TX_EOF + TX_CRC_HIGH + TX_CRC_LOW 

Figure 7-85 shows the R30 transmit interface. The lower 16 bits of the R30 (or FIFO transmit word) contain transmit data nibbles. When MII_RT_TXCFG0/1[11] TX_32_MODE_ENn = 0h - default value (where n = 0 or 1), then the upper 16 bits contain mask information. Alternatively, when MII_RT_TXCFG0/1[11] TX_32_MODE_ENn = 1h (where n = 0 or 1), then the upper 16 bits contain transmit data nibbles. The operation to be performed on the transmit interface is controlled by PRU writes to the R31 command interface. Table 7-98 describes the supported configurations for 8, 16, and 32 bit TX push operations. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 483 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [438 x 72] intentionally omitted <==**

**----- Start of picture text -----**<br>
PRU R30 0:7 8:15 16:23 24:31<br>TX MASK[15:8] or MII TX DATA<br>MII TX DATA<br>**----- End of picture text -----**<br>


TX MASK[7:0] or MII TX DATA 

**Figure 7-85. PRU to TX MII Interface** 

**Table 7-98. TX Push** 

|**R31[25]**<br>**TX_PUSH16/32**|**R31[24]**<br>**TX_PUSH8/32**|**Supported R30 bits**|**TX_32_MODE_EN**|**TX_BYTE_SWAP**|**TX Push Action**|
|---|---|---|---|---|---|
||||||8 bits of TXDATA|
|0|1|X|0|X|(R30[7-0]) pushed|
||||||post TX mask|
||||||16 bits of TXDATA|
|1|0|X|0|X|(R30[15-0]) pushed|
||||||post TX mask|
|1|1|X|0|X|Illegal|
|X|X|0x000000FF|1|0|8 bits of TXDATA<br>(R30[7-0]) pushed|
|X|X|0x0000FFFF|1|0|16 bits of TXDATA<br>(R30[15-0]) pushed|
|X|X|0xFFFFFFFF|1|X|32 bits of TXDATA<br>(R30[31-0]) pushed|
|X|X|All other - reserved|1|X|Reserved|



Using MII_RT_TXCFG0/1[11] TX_32_MODE_ENn = 0h and the TX mask, the PRU can send a mix of R30 and RX L1 FIFO data to the TX L1 FIFO. Note the TX mask is only available when the PRU is fed one word or byte at a time by the RX L1 FIFO. It is not applicable when the RX L2 buffer is enabled. To disable TX mask, set TXMASK to 0xFFFF. 

As shown in Figure 7-86, the PRU drives the MII transmit interface through its R30 register. The contents of R30 and RX data from the receive interface (RX L1 FIFO) are taken and fed into a 40-Bytes transmit FIFO (TX L1 FIFO). 

If MII_RT_TXCFG0/1[11] TX_32_MODE_ENn = 0h (where n = 0 or 1), then before transmission, a mask is applied to the data portion of the R30 register. By using the mask, the PRU firmware can control whether received data from the RX L1 FIFO is sent to transmit, R30 data is sent to transmit, or a mix of the two is sent. The Boolean equation that is used by MII_RT to compose TX data is: 

TXDATA[7/15-0] = (R30[7/15-0] & MASK[7/15-0]) | (RXDATA[7/15-0] & ~MASK [7/15-0]) 

As shown in the equation, a mask of FFh will lead to the R30[7:0] being transmitted in an 8-bit transmit operation. A mask of 0h will lead to receive data being sent out in a 16-bit transmit operation. 

484 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [498 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
Process data<br>PRU 0/1<br>R30<br>R31<br>TXDATA[7/15:0] = (R30[7/15:0] & MASK[7/15:0]) |<br>(RXDATA[7/15:0] & ~MASK [7/15:0])<br>TX_EN<br>TX L1 FIFO TX_EOF<br>MII RX port RX_DV RX L1 FIFO32-Bytes 40-Bytes TX_DATA MII TX port<br>RX_CLK 1. Push<br>2. Pop Mask<br>**----- End of picture text -----**<br>


**Figure 7-86. TX Mask Mode (MII_RT_TXCFG0/1[TX_32_MODE_ENn] = 0h)** 

## _**7.3.10.2.4.1.2 RX L1 FIFO → TX L1 FIFO (Direct Connection) → TX MII Port**_ 

When MII_RT_TXCFG0/1[9] PRE_TX_AUTO_SEQUENCEn is set to 1h (where n = 0 or 1), the data frame is passed from the RX L1 FIFO to TX L1 FIFO without any interaction of the PRU. This mode of operations is shown in Figure 7-87. The RX L1 FIFO will push data into TX L1 FIFO as long as it is enabled and not full. 

There is no PRU dependency in this mode and no option for the PRU to perform any operation to the TX L1 FIFO. RX_RESET clears all data and status elements. 

**==> picture [451 x 41] intentionally omitted <==**

**----- Start of picture text -----**<br>
TX_EN<br>MII RX port [RX DATA] RX L1 FIFO TX L1 FIFO TX_DATA<br>32-Bytes 40-Bytes MII TX port<br>**----- End of picture text -----**<br>


**Figure 7-87. RX L1 to TX L1 Interface** 

For ESC protocols, software should enable [6]RX_AUTO_FWD_PRE0/1 and [4]RX_L2_EN0/1 bits in MII_RT_RXCFG0/1 registers. 

For non ESC protocols, software can enable MII_RT_TXCFG0/1[1] TX_AUTO_PREAMBLEn and MII_RT_RXCFG0/1[2] RX_CUT_PREAMBLEn bit (where n = 0 or 1) to insure full preamble is generated for each TX frame. 

The PRU core can read the passing through frame by polling the standard R31 register. In Direct mode, the PRU R31 Command is ignored and disabled, except for TX_RESET and RX_RESET. 

The following are the legal configurations supported for Direct Connection: 

- Configuration 1: 

   - PORT1.RX -> PRU1 (snoop only) 

   - PORT1.RX -> PORT0.TX 

- Configuration 2: 

   - PORT0.RX -> PRU0 (snoop only) 

   - – PORT0.RX -> PORT1.TX 

- Configuration 3: 

   - PORT1.RX -> PORT1.TX 

- Configuration 4: 

   - PORT0.RX -> PORT0.TX 

## _**7.3.10.2.5 PRU R31 Command Interface**_ 

The PRU uses writes to R31[31-16] to control the reception and transmission of packets in direct and register mode. Table 7-99 lists the available commands. Each bit in the table is a single clock pulse output from the PRU. When more than one action is to be performed in the same instant, the PRU firmware must set those command bits in one instruction. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 485 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-99. PRU R31: Command Interface (Write Mode)** 

|**Bit**|**Command**|**Description**|
|---|---|---|
|31|TX_CRC_ERR|TX_CRC_ERR command when set will add 0xA5 byte to the TX<br>L1 FIFO if the current FCS is valid. This bit can only be set with<br>the TX_EOF command and optionally with the TX_ERROR_NIBBLE<br>command. It cannot get set with any other commands, and the PRU<br>firmware must wait > 2 clocks from the last command. Note: For proper<br>operations auto-forward preamble must be enabled.|
|30|TX_RESET|TX_RESET command is used to reset the transmit FIFO and clear all its<br>contents. This is required to recover from a TX FIFO overrun.|
|29|TX_EOF|TX_EOF command is used to indicate that the data loaded is<br>considered last for the current frame|
|28|TX_ERROR_NIBBLE|TX_ERROR_NIBBLE command is used to insert an error nibble. This<br>makes the frame invalid. Also, it will add 0x0 after the 32-bit CRC.|
|27|TX_CRC_HIGH|TX_CRC_HIGH command ends the CRC calculations and pushes<br>CRC[31-16] to append to the outgoing frame in the TX L1 FIFO. Note:<br>TX_CRC0/1 will become valid after 6 clock cycles.|
|26|TX_CRC_LOW|TX_CRC_LOW command pushes CRC[15-0] to append to the outgoing<br>frame in the TX L1 FIFO.|
|25|TX_PUSH16|TX_PUSH16 command pushes R30[15-0] when MII_RT_TXCFG0/1[11]<br>TX_32_MODE_ENn = 0h (where n = 0 or 1). SeeTable 7-98,_TX_<br>_Push_for more details. Note: There are no restrictions on concurrent<br>PUSH/POP nor R30 requirements to maintain data. Back to back PUSH<br>is supported.|
|24|TX_PUSH8|TX_PUSH8 command pushes R30[7-0] when MII_RT_TXCFG0/1[11]<br>TX_32_MODE_ENn = 0h (where n = 0 or 1). SeeTable 7-98,_TX_<br>_Push_for more details. Note: There are no restrictions on concurrent<br>PUSH/POP nor R30 requirements to maintain data. Back to back PUSH<br>is supported.|
|23|RX_ ERROR_CLR|RX_ERROR_CLR command is used to clear RX_ ERROR indicator bit<br>by writing 1h.|
|22|RX_EOF_CLR|RX_EOF_CLR command is used to clear RX_EOF status indicator bit<br>by writing 1h.|
|21|RX_SFD_CLR|RX_SFD_CLR command is used to clear RX_SFD indicator bit by<br>writing 1h.|
|20|RX_SOF_CLR|RX_SOF_CLR command is used to clear RX_SOF indicator bit by<br>writing 1h.|
|19|Reserved|Reserved|
|18|RX_RESET|RX_RESET is used to reset the receive FIFO and clear all contents.<br>This is required to recover from a RX FIFO overrun, if software does<br>not want to undrain. The typical use case is assertion after RX_EOF. If<br>asserted during an active frame, the following actions will occur:<br>1.<br>Terminate the current frame<br>2.<br>Block/terminate all new data<br>3.<br>Flush/clear all FIFO elements<br>4.<br>Cause RX state machine into an idle state<br>5.<br>Cause EOF event<br>6.<br>Cause minimum frame error, if you abort before minimum size<br>reached|
|17|RX_POP16|RX_POP16 command advances the receive traffic by two bytes. This is<br>only required when you are using R31 to read the data. After R31[15-0]<br>is ready to read by PRU, it will set 1h to WORD_RDY, and the next new<br>data will be allowed to advance. RX_POP16 to WORD_RDY update<br>has 2 clock cycles latency. Firmware needs to insure it does not read<br>WORD_RDY/BYTE_RDY until 2 clock cycles after RX_POP16.|



486 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-99. PRU R31: Command Interface (Write Mode) (continued)** 

|**Bit**|**Command**|**Description**|
|---|---|---|
|16|RX_POP8|RX_POP8 command advances the receive traffic by one bytes. This is<br>only required when you are using R31 to read the data. After R31[7-0]<br>is ready to read by PRU, it will set 1h to BYTE_RDY, and the next<br>new data will be allowed to advance. RX_POP8 to BYTE_RDY update<br>has 2 clock cycles latency. Firmware needs to insure it does not read<br>WORD_RDY/BYTE_RDY until 2 clock cycles after RX_POP8.|



## _**7.3.10.2.6 Other Configuration Options**_ 

## _**7.3.10.2.6.1 Nibble and Byte Order**_ 

The PRU core is little endian. To support big endian, the MII_RT supports optional nibble swapping on both the RX and TX side. 

On the receive side, the order of the two data bytes in RX R31 and the RX L2 buffer are configurable through the RX_BYTE_SWAP0/1 bit in the MII_RT_RXCFG0/1 registers, as shown in Table 7-100. Note: The Nibble0 is the first nibble received. 

**Table 7-100. RX Nibble and Byte Order** 

|**Configuration**|**Order**|
|---|---|
|MII_RT_RXCFG0/1[5] RX_BYTE_SWAPn = 0h (default), where n = 0<br>or 1|R31[15-8] / RXL2[15-8] = Byte1{Nibble3,Nibble2}<br>R31[7-0] / RXL2[7-0] = Byte0{Nibble1,Nibble0}|
|MII_RT_RXCFG0/1[5] RX_BYTE_SWAPn = 1h, where n = 0 or 1|R31[15-8] / RXL2[15-8] = Byte0{Nibble1,Nibble0}<br>R31[7-0] / RXL2[7-0] = Byte1{Nibble3,Nibble2}|



On the transmit side, the order of the two data bytes and mask bytes in TX R30 are configurable through the TX_BYTE_SWAP0/1 bit in the MII_RT_TXCFG0/1 registers, as shown in Table 7-101. Note the Nibble0 is the first nibble transmitted. 

**Table 7-101. TX Nibble and Byte Order** 

|**Configuration**|**Order**|
|---|---|
|MII_RT_TXCFG0/1[3] TX_BYTE_SWAPn = 0h (default), where n = 0<br>or 1|If MII_RT_TXCFG0/1[11] TX_32_MODE_ENn = 0h, where n = 0 or 1<br>R30[15-8] = Byte1{Nibble3,Nibble2}<br>R30[7-0] = Byte0{Nibble1,Nibble0}<br>R30[31-24] = TX_MASK[15-8]<br>R30[23-16] = TX_MASK[7-0]<br>If MII_RT_TXCFG0/1[11] TX_32_MODE_ENn = 1h,<br>R30[31-24] = Byte3{Nibble7,Nibble6}<br>R30[23-16] = Byte2{Nibble5,Nibble4}<br>R30[15-8] = Byte1{Nibble3,Nibble2}<br>R30[ 7-0] = Byte0{Nibble1,Nibble0}|
|MII_RT_TXCFG0/1[3] TX_BYTE_SWAPn = 1h, where n = 0 or 1|If MII_RT_TXCFG0/1[11] TX_32_MODE_EN = 0h,<br>R30[15-8] = Byte0{Nibble1,Nibble0}<br>R30[7-0] = Byte1{Nibble3,Nibble2}<br>R30[31-24] = TX_MASK[7-0]<br>R30[23-16] = TX_MASK[15-8]<br>If MII_RT_TXCFG0/1[11] TX_32_MODE_EN = 1h,<br>Only 32-bit push is supported.<br>R30[31-24] = Byte0{Nibble1,Nibble0}<br>R30[23-16] = Byte1{Nibble3,Nibble2}<br>R30[15-8] = Byte2{Nibble5,Nibble4}<br>R30[ 7-0] = Byte3{Nibble7,Nibble6}|



## _**7.3.10.2.6.2 MII_RT Preamble Source**_ 

The MII_RT module has the option to preserve and forward a received preamble in the TX data stream, use a preamble provided by the PRU, or auto-generate a preamble. These configurations are highlighted in Table 7-102. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 487 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-102. Preamble Configuration Options** 

|**Table 7-102. Preamble**|**Configuration Options**|
|---|---|
|RX_CUT_PREAMBLE|Determines whether RX preamble is passed to the RX L1/L2 FIFO|
|RX_AUTO_FWD_PRE|Determines whether RX preamble is automatically passed to TX L1<br>FIFO|
|TX_AUTO_PREAMBLE|TX interface logic auto-generates and appends preamble to TX data<br>stream with the first push of data into the TX L1 FIFO. Note that<br>enabling this option does fill the TX FIFO with the preamble length,<br>hence software has to consider this to not overrun the TX FIFO.|



## _**7.3.10.2.6.3 PRU and MII Port Multiplexer**_ 

The MII_RT module supports configurable PRU core to MII TXn / RXn port mapping. By default, PRU0 is mapped to TX1 and RX0 and PRU1 is mapped to TX0 and RX1. However, the system supports the flexibility to map any PRU core to any TX and RX port. For example, the input to PRU0 can be either RX_MII0 or RX_MII1. Similarly, the input to TX_MII0 can be either PRU0 or PRU1. 

## _**7.3.10.2.6.3.1 Receive Multiplexer**_ 

A multiplexer is provided to allow selecting either of the two MII interfaces (RX_MII0 or RX_MII1) for the receive data that is sent to PRU. Figure 7-88 shows a simple diagram of PRU receive multiplexer. 

**==> picture [290 x 94] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX_DATA[3:0]<br>RX_MII0<br>RX_DV RX_DATA[3:0]<br>RX MII<br>Multiplexer PRU0/1<br>RX_DV<br>RX_DATA[3:0] (PRU0/1)<br>RX_MII1<br>RX_DV<br>**----- End of picture text -----**<br>


**Figure 7-88. MII Receive Multiplexer** 

There are two receive multiplexer instances to enable selection of RX MII path for each PRU. The select lines of the RX multiplexers are driven from the PRU-ICSS programmable registers (MII_RT_RXCFG0/1[3] RX_MUX_SELn, where n = 0 or 1). 

## _**7.3.10.2.6.3.2 Transmit Multiplexer**_ 

On the MII transmit ports, there is a multiplexer for each MII transmit port that enables selection of either the transmit data from the PRUs or from the RX MII interface of the other MII interface. Figure 7-89 shows a simple diagram of PRU transmit multiplexer. 

**==> picture [293 x 143] intentionally omitted <==**

**----- Start of picture text -----**<br>
TX_DATA[3:0]<br>TX_PRU0<br>TX_EN<br>TX_DATA[3:0]<br>TX_DATA[3:0]<br>TX MII<br>TX_PRU1 TX_EN<br>TX_EN Multiplexer TX_MII1/0<br>(Port 0/1)<br>TX_SOF<br>TX_DATA[3:0]<br>RX_MII0/1<br>TX_EN<br>**----- End of picture text -----**<br>


**Figure 7-89. MII Transmit Multiplexer** 

The transmit multiplexers enable the PRU-ICSS to either operate in a bypass mode where the PRU is not involved in processing MII traffic or use of one of the PRU cores for transmitting data into the MII interface. There 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

488 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

are two instances of the TX MII multiplexer and the select lines for each TX multiplexer are provided by the PRU-ICSS programmable registers (MII_RT_TXCFG0/1[8] TX_MUX_SELn, where n = 0 or 1). The select lines are common between register and FIFO interface. It is expected that the select lines will not change during the course of a frame so that can avoid data exchange error. 

## _**7.3.10.2.6.4 RX L2 Scratch Pad**_ 

When the RX L2 is disabled (MII_RT_RXCFG0/1[4] RX_L2_ENn = 0h, where n = 0 or 1), the RX L2 banks can be used as a generic scratch pad. In scratch pad mode, RX L2 Bank0 and RX L2 Bank1 operate like simple read/write memory mapped registers. All XFR size and start operations are supported. RX_RESET has no effect in this mode. This mode is shown in Figure 7-90. 

**==> picture [216 x 77] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX L2<br>PRU<br>Bank 0<br>32 bytes of data XFR R0<br>Bank 1 …<br>R31<br>32 bytes of data<br>**----- End of picture text -----**<br>


**Figure 7-90. Scratch Pad Mode** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 489 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.11 PRU-ICSS MII MDIO Module**_ 

This section describes the PRU-ICSS (where n = 0 or 1) integrated MII management interface (MII_MDIO module). 

## **7.3.11.1 PRU-ICSS MII MDIO Overview** 

The following features are supported: 

- Clause 22 and Clause 45. 

- Up to 32 PHY addresses. 

- Two user access registers to control and monitor up to two PHYs simultaneously. 

- Peripheral interface for configuration and control (MII RT MDIO CFG) 

- Each PHY can be individually enabled to be polled. 

- The inter-poll gap between PHY polls can be changed. 

- State Change Mode of operation to monitor up to 32 PHYs simultaneously. 

- Manual control by software for GPIO operations. 

The PRU-ICSS MII MDIO management I/F module implements the _802.3 serial management interface_ to interrogate and control two Ethernet PHYs simultaneously using a shared two-wire bus. Figure 7-91 shows a device with two MACs, each connected to an Ethernet PHY, being managed by the MII interface module using a shared bus. 

The Figure 7-91 gives an overview of the MII MDIO management interface. 

## **Note** 

This MDIO Interface is dedicated for the PRU-ICSS MII Ports. This device also makes use of another MDIO interface that is dedticated for the CPSW. 

**==> picture [260 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>MII MDIO<br>Management<br>Ethernet<br>MAC0 PHY0<br>MII0<br>Ethernet<br>MAC1 PHY1<br>MII1<br>Local Shared Bus<br>**----- End of picture text -----**<br>


**==> picture [27 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
icss-041<br>**----- End of picture text -----**<br>


**Figure 7-91. Device PRU-ICSS MII MDIO Management Interface Overview** 

## **7.3.11.2 PRU-ICSS MII MDIO Functional Description** 

The MII Management interface incorporates: 

- _MDIO Registers_ - The MDIO register block provides a VBUSP 3.0 compliant peripheral interface to the MDIO module. Host interaction with this module is facilitated through the registers in this block. 

- _Control and Schedule_ - The control and register logic in the MDIO module contain the state machine and scheduling logic which control the wire side operation. 

- _MDIO Interface_ - The MDIO interface block provides the serial interface to the MDIO interface. 

The MDIO logic is fully synchronous to the PRU-ICSS local shared bus clock. 

## _**7.3.11.2.1 MDIO Clause 22 Frame Formats**_ 

The below Table 7-103 shows the read and write format of the Clause 22 Management interface frames. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

490 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**Table 7-103. MDIO Clause 22 Frame Formats** 

|**Preamble**|**Start Delimiter**|**Operation**<br>**Code**|**PHY Address**|**Register Address**|**Turnaround**|**Data**|
|---|---|---|---|---|---|---|
|**MDIO Clause 22 Read Frame Format**|||||||
|FFFFFFFFh|01|10|AAAAA|RRRRR|Z0|DDDD.DDDD.DDD<br>D.DDDD|
|**MDIO Clause 22 Write Frame Format**|||||||
|FFFFFFFFh|01|01|AAAAA|RRRRR|10|DDDD.DDDD.DDD<br>D.DDDD|



The default or idle state of the two wire serial interface is a logic one. All tri-state drivers should be disabled and the PHY’s pull-up resistor will pull the MDIO line to a logic one. Prior to initiating any other transaction, the station management entity shall send a preamble sequence of 32 contiguous logic one bits on the MDIO line with 32 corresponding cycles on MDCLK to provide the PHY with a pattern that it can use to establish synchronization. A PHY shall observe a sequence of 32 contiguous logic one bits on MDIO with 32 corresponding MDCLK cycles before it responds to any other transaction. 

## **Preamble** 

The start of a frame is indicated by a preamble, which consists of a sequence of 32 contiguous bits all of which are a “1”. This sequence provides the Ethernet PHY a pattern to use to establish synchronization. 

## **Start Delimiter** 

The preamble is followed by the start delimiter which is indicated by a “01” pattern. The pattern assures transitions from the default logic one state to zero and back to one. 

## **Operation Code** 

The operation code for a read is “10”, while the operation code for a write is a “01”. 

## **Ethernet PHY Address** 

The PHY address is 5 bits allowing 32 unique values. The first bit transmitted is the MSB of the PHY address. 

## **Register Address** 

The Register address is 5 bits allowing 32 registers to be addressed within each PHY. 

## **Turnaround** 

An idle bit time during which no device actively drives the MDIO signal shall be inserted between the _Register Address_ field and the _Data_ field of a read frame in order to avoid contention. During a read frame, the PHY shall drive a zero bit onto MDIO for the first bit time following the idle bit and preceding the Data field. During a write frame, this field shall consist of a one bit followed by a zero bit. 

## **Data** 

The Data field is 16 bits. The first bit transmitted and received is the MSB of the data word. 

## _**7.3.11.2.1.1 PRU-ICSS MDIO Control and Interface Signals**_ 

The Table 7-104 shows the PRU_ICSS (where n = 0 to 2) MII MDIO signals and their availability at the device boundary. 

**Table 7-104. PRU-ICSS MII MDIO Control and Interface Signals** 

|**MDIO Control Signals**|**MDIO Control Signals**|**MDIO Control Signals**|**MDIO Control Signals**|
|---|---|---|---|
|**Pin Name**|**Type**|**Available as device I/O**|**Function**|
|MDIO_LINKINT[1:0]|O|N.A.|Serial interface link change interrupt. Indicates a<br>change in the state of the PHY link.|
|MDIO_USERINT[1:0]|O|N.A.|Serial interface user command event complete<br>interrupt.|
|**MDIO Interface Signals**||||
|**Pin Name**|**Type**|**Available as device I/O**|**Function**|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 491 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-104. PRU-ICSS MII MDIO Control and Interface Signals (continued)** 

|**MDIO Control Signals**|**MDIO Control Signals**|**MDIO Control Signals**|**MDIO Control Signals**|
|---|---|---|---|
|MDIO_I|I|device bidirectioanal**pr0_mdio_data**,<br>and pr1_mdio_mdclk pin in input<br>mode|Serial data input|
|MDIO_O|O|device bidirectional**pr0_mdio_data**<br>and pr1_mdio_mdclk pin in output<br>mode|Serial data output|
|MDIO_OE_N|O|N.A.|Serial data output enable. Asserted "0" when data<br>output is valid|
|MDCLK_O|O|device output -**pr0_mdio_mdclk**<br>pr1_mdio_mdclk|Serial clock output|
|MLINK_I[1:0]|I|N.A.|Optional link status inputs from PHY. Each input is<br>connected to a single PHY. Unused inputs are tied ‘0’.|



## _**7.3.11.2.2 MDIO Clause 45 Frame Formats**_ 

The below Table 7-105 shows the address frame format. Table 7-106 shows read, and write format of the supported Clause 45 frames. Post-increment accesses are not supported. 

**Table 7-105. MDIO Clause 45 Address Frame Formats** 

|**Pre-amble**|**Pre-amble**|**Start Delimiter**|**Operation**<br>**Code**|**PHY Address**|**MMD Number**|**Turnaround**|**Address**|
|---|---|---|---|---|---|---|---|
|**MDIO Clause 45 Address Frame Format**||||||||
|FFFFFFFFh||00|00|AAAAA|RRRRR|10|AAAA.AAAA.AAA<br>A.AAAA|
|**Table 7-106. MDIO Clause 45 Frame Formats**||||||||
|**Pre-amble**|**Start Delimiter**||**Operation**<br>**Code**|**PHY Address**|**MMD Number**|**Turnaround**|**Data**|
|**MDIO Clause 45 Read Frame Format**||||||||
|FFFFFFFFh|00||11|AAAAA|RRRRR|Z0|DDDD.DDDD.DD<br>DD.DDDD|
|**MDIO Clause 45 Write Frame Format**||||||||
|FFFFFFFFh|00||01|AAAAA|RRRRR|10|DDDD.DDDD.DD<br>DD.DDDD|



The default or idle state of the two wire serial interface is a logic one. All tri-state drivers should be disabled and the PHY’s pull-up resistor should pull the MDIO line to a logic one. Prior to initiating any other transaction, the station management entity shall send a preamble sequence of 32 contiguous logic one bits on the MDIO line with 32 corresponding cycles on MDCLK to provide the PHY with a pattern that it can use to establish synchronization. A PHY shall observe a sequence of 32 contiguous logic one bits on MDIO with 32 corresponding MDCLK cycles before it responds to any other transaction. The MDIO_USER_ADDR0_REG/ MDIO_USER_ADDR1_REG registers must be written before a read or write operation is performed to set the address used in the operation. Each read or write operation has a preceeding address frame. 

## **Preamble** 

The start of a frame is indicated by a preamble, which consists of a sequence of 32 contiguous bits all of which are a “1”. This sequence provides the PHY a pattern to use to establish synchronization. The preamble is required in clause 45 operation. 

## **Start Delimiter** 

The preamble is followed by the start delimiter which is indicated by a “00” pattern. 

## **Operation Code** 

The operation code for address is “00". The operation code for a read is “11”, while the operation code for a write is a “01”. 

492 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **Ethernet PHY Address** 

The PHY address is 5 bits allowing 32 unique values. The first bit transmitted is the MSB of the PHY address. 

## **MMD Number** 

The MMD number is 5 bits allowing 32 unique values. The first bit transmitted is the MSB. 

## **Turnaround** 

An idle bit time during which no device actively drives the MDIO signal shall be inserted between the **MMD Number** field and the **Data** field of a read frame in order to avoid contention. During a read frame, the PHY shall drive a zero bit onto MDIO for the first bit time following the idle bit and preceding the Data field. During a write frame, this field shall consist of a one bit followed by a zero bit. 

## **Address** 

The address field is 16-bits on address operations. The first bit transmitted is the MSB of the address word. Each read/write operation initiated has an automatic address operation initiated first that uses the MDIO_USER_ADDR0_REG[15-0] USER_ADDR0 or MDIO_USER_ADDR1_REG[15-0] USER_ADDR1 register values as the 16-bit address. 

## **Data** 

The Data field is 16 bits on read and write operations. The first bit transmitted and received is the MSB of the data word. 

## _**7.3.11.2.3 PRU-ICSS MII MDIO Interractions**_ 

The MDIO module will remain idle until enabled by setting the [30] ENABLE bit in the MDIO MDIO_CONTROL_REG register. The MDIO will then continuously poll the link status from within the Generic Status Register of all possible 32 PHY addresses in turn recording the results in the MDIO MDIO_LINK_REG register. Individual PHY's can be enabled or disabled for polling through the associated bit in the MDIO MDIO_POLL_EN_REG register. The MDIO MDIO_LINK_REG and MDIO_ALIVE_REG register bit values are updated on the poll of each PHY. In _Normal Mode_ , the link status of two of the 32 possible PHY addresses can also be determined using the MLINK pin inputs. The bit [7] LINKSEL in the MDIO MDIO_USER_PHY_SEL_REG_0/1 register determines the status input that is used. A change in the link status of the two PHYs being monitored will set the appropriate bit ([1-0] LINKINTRAW) in the MDIO MDIO_LINK_INT_RAW_REG register and the MDIO_LINK_INT_MASKED_REG[1-0] LINKINTMASKED register, if enabled by the [6] LINKINT_ENABLE bit in the MDIO MDIO_USER_PHY_SEL_REG_0/1 register. In _State Change Mode_ , a change in any PHY status will be indicated on the MDIO_LINK_INT_RAW_REG[0] LINKINTRAW interrupt if enabled. 

The MDIO MDIO_ALIVE_REG register is updated by the MDIO module if the PHY acknowledged the read of the generic status register. In addition, any PHY register read transactions initiated by the host also cause the MDIO MDIO_ALIVE_REG register to be updated. 

At any time, the host can define a transaction for the MDIO module to undertake using the [15-0] DATA, [20-16] PHYADR, [25-21] REGADR, and [30] WRITE fields in a MDIO_USER_ACCESS_REG_0/1 register. When the host sets the [31] GO bit in this register, the MDIO interface module will begin the transaction without any further intervention from the host. Upon completion, the MDIO will clear the [31] GO bit and set the [1-0] USERINTRAW bit field in the MDIO_USER_INT_RAW_REG register corresponding to the MDIO_USER_ACCESS_REG_0/1 register being used. The corresponding bit in the MDIO_USER_INT_MASKED_REG register may also be set depending on the mask setting in the MDIO_USER_INT_MASK_SET_REG and MDIO_USER_INT_MASK_CLEAR_REG registers. A roundrobin arbitration scheme is used to schedule transactions which may queued by the host in different MDIO_USER_ACCESS_REG_0/1 registers. The host should check the status of the [31] GO bit in the MDIO_USER_ACCESS_REG_0/1 register before initiating a new transaction to ensure that the previous transaction has completed. The host can use the [29] ACK bit in the MDIO_USER_ACCESS_REG_0/1 register to determine the status of a read transaction. 

Software may use the MDIO module to set up the auto-negotiation parameters of each PHY attached to a MAC port, retrieve the negotiation results, and set up the MAC Control register in the corresponding MAC. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 493 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.11.2.4 PRU-ICSS MII MDIO Interrupts**_ 

## _**7.3.11.2.4.1 Normal Mode ([30]STATECHANGEMODE = 0h)**_ 

The MDIO will assert the MDIO_LINKINT signals if there is a change in the link state of the Ethernet PHY corresponding to the address in the [4-0] PHYADR_MON field of the MDIO MDIO_USER_PHY_SEL_REG_j (where j = 0 or 1) registers and the corresponding [6] LINKINT_ENABLE bit is set. The MDIO_LINKINT event is also captured in the MDIO MDIO_LINK_INT_MASKED_REG register. MDIO_LINKINT[0] and MDIO_LINKINT[1] correspond to the MDIO MDIO_USER_PHY_SEL_REG_0 and MDIO_USER_PHY_SEL_REG_1 registers, respectively. 

When the [31] GO bit in the MDIO_USER_ACCESS_REG_j (where j = 0 or 1) registers transitions from ‘1’ to ‘0’, indicating the completion of a user access, and the corresponding [1-0] USERINTMASKSET field in the 

MDIO_USER_INT_MASK_SET_REG register is set, the MDIO_USERINT signal is asserted ‘1’. The MDIO_USERINT event is also captured in the MDIO_USER_INT_MASKED_REG register. MDIO_USERINT[0] and MDIO_USERINT[1] correspond to the MDIO_USER_ACCESS_REG_0 and MDIO_USER_ACCESS_REG_1 registers, respectively. 

## _**7.3.11.2.4.2 State Change Mode ([30]STATECHANGEMODE = 1h)**_ 

In _State Change Mode_ , the MDIO will assert MDIO_LINKINT[0] when any bit in the MDIO MDIO_ALIVE_REG or MDIO MDIO_LINK_REG registers changes due to MDIO operations. The MDIO_LINKINT event is also captured in the MDIO MDIO_LINK_INT_MASKED_REG register. MDIO_LINKINT[1] output and the MDIO MDIO_USER_PHY_SEL_REG_j (where j = 0 or 1) registers are unused in _State Change Mode_ . 

## _**7.3.11.2.5 Manual Mode**_ 

_Manual Mode_ allows software to directly control the serial clock output (MDCLK_O), the serial data output enable (MDIO_OE_N), and the serial data output (MDIO_O). The serial data input can also be read (MDIO_I). This mode is enabled when the [31] MANUALMODE bit is set in the MDIO MDIO_POLL_REG register. _Manual Mode_ is intended to be used by software for slow speed general purpose IO operations and not for MDIO PHY operations. 

## **7.3.11.3 PRU-ICSS MII MDIO Receive/Transmit Frame Host Software Interface** 

To facilitate transmission and reception of serial management frames, the host has to perform the following operations: 

- Configure the [20] PREAMBLE and [15-0] CLKDIV fields in the MDIO MDIO_CONTROL_REG register. 

- • Enable the MDIO module by setting the [30] ENABLE bit in the MDIO MDIO_CONTROL_REG register. If Byte access is being used, the [30] ENABLE bit should be written last. 

- The MDIO MDIO_ALIVE_REG register can be read after a delay to determine which Ethernet PHYs responded. 

- Set up the appropriate PHY addresses in the MDIO MDIO_USER_PHY_SEL_REG_j[4-0] PHYADR_MON bits. 

- Set up the appropriate [6] LINKINT_ENABLE bit in the MDIO MDIO_USER_PHY_SEL_REG_j registers. 

- Set up the appropriate [7] LINKSEL bits in the MDIO MDIO_USER_PHY_SEL_REG_j registers. 

- Set up the appropriate [1-0] USERINTMASKEDSET field in the MDIO MDIO_USER_INT_MASK_SET_REG register. 

- To write to an Ethernet PHY register the host should first check to ensure that the [31] GO bit in a MDIO MDIO_USER_ACCESS_REG_j registers is cleared. The [31] GO, [30] WRITE, [25-21] REGADR, [20-16] PHYADR and data fields in that MDIO MDIO_USER_ACCESS_REG_j registers can then be updated to the appropriate value. If byte access is being used, the [31] GO bit should be written last. The write operation to the PHY will be scheduled and completed by the module. Completion of the write operation can be determined by examining the [31] GO bit in the MDIO MDIO_USER_ACCESS_REG_j registers. It also results in a transition on the appropriate MDIO_INT signal and the corresponding bit in the MDIO MDIO_USER_INT_MASKED_REG register based on the setting of the MDIO MDIO_USER_INT_MASK_SET_REG register. 

- To read from an Ethernet PHY register the host should first check to ensure that the [31] GO bit in a MDIO MDIO_USER_ACCESS_REG_j registers is cleared. The [31] GO, [25-21] REGADR, and 

494 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

[20-16] PHYADR fields in that MDIO MDIO_USER_ACCESS_REG_j registers can then be updated to the appropriate value. The read data value will be available in the [15-0] DATA field of the MDIO MDIO_USER_ACCESS_REG_j registers after the module completes the read operation on the serial bus. The completion of the read operation can be determined by examining the [31] GO and [29] ACK bits in the MDIO MDIO_USER_ACCESS_REG_j registers. It also results in a transition on the appropriate MDIO_INT signal and the corresponding bit in the MDIO MDIO_USER_INT_MASKED_REG register based on the setting of the MDIO MDIO_USER_INT_MASK_SET_REG register. 

- The module de-asserts the MDIO_USERINT signal when the host writes to the appropriate [1-0] USERINTMASKED bit field in the MDIO MDIO_USER_INT_MASKED_REG register or the [1-0] USERINTRAW bit field in the MDIO MDIO_USER_INT_RAW_REG register. 

- The host can poll the MDIO MDIO_LINK_REG register periodically or use the MDIO_LINKINT signals to determine the state of the serial interface to a particular Ethernet PHY. 

- The module de-asserts the MDIO_LINKINT when the host writes to the appropriate [1-0] LINKINTRAW bit field in the MDIO_MDIO LINK_INT_RAW_REG register or the [1-0] LINKINTMASKED bit field in the MDIO_MDIO LINK_INT_MASKED_REG register. 

**Table 7-107. Summary of the PRU-ICSS MII MDIO Functional Registers** 

|**Address Offset**|**Register Mnemonic**|**Register Name**|**Register Purpose**|
|---|---|---|---|
|00h|**MDIOVer**|MDIO_MDIO_VERSION_REG|Module version register|
|04h|**MDIOControl**|MDIO_CONTROL_REG|Module control register|
|08h|**MDIOAlive**|MDIO_ALIVE_REG|Ethernet PHY<br>acknowledge status<br>register|
|0Ch|**MDIOLink**|MDIO_LINK_REG|Ethernet PHY link<br>status register|
|10h|**MDIOLinkIntRaw**|MDIO_LINK_INT_RAW_REG|Link status change<br>interrupt register (raw<br>value)|
|14h|**MDIOLinkIntMasked**|MDIO_LINK_INT_MASKED_REG|Link status change<br>interrupt register<br>(masked value)|
|18h|**MDIOLinkIntMaskSet**|MDIO_LINK_INT_MASK_SET_REG|Link status change<br>interrupt mask set<br>register|
|1Ch|**MDIOLinkIntMaskClr**|MDIO_LINK_INT_MASK_CLEAR_REG|Link status change<br>interrupt mask clear<br>register|
|20h|**MDIOUserIntRaw**|MDIO_USER_INT_RAW_REG|User command<br>complete interrupt<br>register (raw value)|
|24h|**MDIOUserIntMasked**|MDIO_USER_INT_MASKED_REG|User command<br>complete interrupt<br>register (masked value)|
|28h|**MDIOUserIntMaskSet**|MDIO_USER_INT_MASK_SET_REG|User interrupt mask set<br>register|
|2Ch|**MDIOUserIntMaskClr**|MDIO_USER_INT_MASK_CLEAR_RE<br>G|User interrupt mask<br>clear register|
|30h|**MDIOManual_IF**|MDIO_MANUAL_IF_REG|Manual interface<br>register|
|34h|**MDIOPoll_IPG**|MDIO_POLL_REG|Poll and IPG register|
|38h|**MDIOPoll_En**|MDIO_POLL_EN_REG|Poll Enable register|
|3Ch|**MDIOClause**|MDIO_CLAUS45_REG|Clause 22 or 45 enable<br>register|
|40h|**MDIOUser_Addr0**|MDIO_USER_ADDR0_REG|User Address register<br>0|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 495 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-107. Summary of the PRU-ICSS MII MDIO Functional Registers (continued)** 

|**Address Offset**|**Register Mnemonic**|**Register Name**|**Register Purpose**|
|---|---|---|---|
|44h|**MDIOUser_Addr1**|MDIO_USER_ADDR1_REG|User Address register<br>1|
|48h – 7Ch|**Reserved**|-|Reserved|
|80h|**MDIOUserAccess0**|MDIO_USER_ACCESS_REG_0|User access register 0|
|84h|**MDIOUserPhySel0**|MDIO_USER_PHY_SEL_REG_0|User PHY select<br>register 0|
|88h|**MDIOUserAccess1**|MDIO_USER_ACCESS_REG_1|User access register 1|
|8Ch|**MDIOUserPhySel1**|MDIO_USER_PHY_SEL_REG_1|User PHY select<br>register 1|
|90h – FFh|**Reserved**|-|Reserved|



496 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## _**7.3.12 PRU-ICSS IEP**_ 

This section describes the Industrial Ethernet Peripheral (IEP) Module which is part of the PRU-ICSS. 

## **7.3.12.1 PRU-ICSS IEP Overview** 

The Industrial Ethernet Peripheral (IEP) performs hardware work required for Industrial Ethernet functions. The IEP module features an industrial ethernet timer with 16 compare events, industrial ethernet sync generator and latch capture, industrial ethernet watchdog timer, and a digital I/O port (DIGIO). 

## **7.3.12.2 PRU-ICSS IEP Functional Description** 

This section provides the functional description of the IEP component. The PRU-ICSS module implements one Industrial Ethernet Peripheral (IEP0). The IEP functional block diagram is shown in Figure 7-92. 

**==> picture [409 x 175] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>IEP0<br>PR[0:1]_IEP0_EDIO_OUTVALID<br>PRU[0:1] Counter (64 bit) EDIO<br>PR[0:1]_IEP0_DATA_IN_OUT[31:30]<br>PR[0:1]_IEP0_EDC_SYNC_OUT0<br>SoC INTC events Compare SYNC PR[0:1]_IEP0_EDC_SYNC_OUT1<br>PR[0:1]_IEP0_EDC_LATCH_IN0<br>triggers Capture LATCH<br>MII_RT PR[0:1]_IEP0_EDC_LATCH_IN1<br>RX_IPG Monitor event Watchdog<br>**----- End of picture text -----**<br>


**Figure 7-92. IEP Functional Block Diagram** 

## _**7.3.12.2.1 PRU-ICSS IEP Clock Generation**_ 

The IEP has a selectable module input clock (PRU_ICSS_IEP_CLK, see also _PRU-ICSS in Module Integration_ ). The clock source is selected by the state of the CTRLMMR_PRU_ICSS_CLKSEL[19-16] IEP_CLKSEL bit within the CTRL_MMR0 register space. Two clock sources are supported for the IEP input clock: 

- PRU_ICSS_IEP_CLK (where n = 0 or 1): The source clock for IEP module can be selected through IEP Clock Multiplexer (see also _PRU-ICSS in Module Integration_ ). The default functional source clock for IEP is MAIN_PLL3_HSDIV1_CLKOUT, derived from PLL3 HSDIV1. The IEP functional clock (PRU_ICSS_IEP_CLK) runs at 200 or 250 MHz. 

- PRU_ICSS_ICLK (where n = 0 or 1): The PRU-ICSS interface clock is derived as divided version of the device PLLCTRL output clock (SYSCLK0/2). 

Switching from PRU_ICSS_IEP_CLK to PRU_ICSS_ICLK is done by writing 1h to the PRU_ICSS_IEPCLK_REG/PRU_ICSS0_IEPCLK_REG[0] IEP_OCP_CLK_EN bit. This is a one time configuration step before enabling the IEP function. Switching back from PRU_ICSS_ICLK to PRU_ICSS_IEP_CLK is only supported through a hardware reset of the PRU-ICSS. 

## **CAUTION** 

When software enables the clock (at PRU-ICSS level) to the IEP module clock input via setting bit PRU_ICSS_IEPCLK_REG/PRU_ICSS0_IEPCLK_REG[0] IEP_OCP_CLK_EN to 1h in the PRUSS_CFG space, there must be NO in-flight transactions to the IEP block. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 497 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **CAUTION** 

Switching from PRU_ICSS_IEP_CLK (the IEP specific functional clock source) to the PRU_ICSS_CORE_CLK source is supported ONLY in software. Switching back from PRU_ICSS_CORE_CLK to PRU_ICSS_IEP_CLK is ONLY supported via assertion of a hardware reset to the PRU-ICSS. 

## _**7.3.12.2.2 PRU-ICSS IEP Timer**_ 

The IEP timer is a simple 64-bit timer. This timer is intended for use by industrial ethernet functions but can also be leveraged as a generic timer in other applications. 

## _**7.3.12.2.2.1 PRU-ICSS IEP Timer Features**_ 

The IEP timer supports the following features: 

- One controller 64-bit count-up counter with an overflow status bit. 

   - 

   - Runs on ICSS_IEP_CLK or ICSS_ICLK clock. 

- Write 1h to clear status. 

- 

      - Supports a programmable increment value from 1 to 16 (default 5). 

   - An optional compensation method allows the increment value to apply compensation increment value from 1 to 16 count up to 2[24] ICSS_IEP_CLK events with additional slow compensation mode. 

- 10× 64-bit capture registers: 

   - 8 capture inputs, with optional synchronous or asynchronous mode: 

      - 6× rise capture registers: ICSS_IEP_CAPRi_REG0/ IEP_CAPRi_REG1 (where i=0 to 5) 

      - 2× rise and fall capture registers: IEP_CAPR6_REG0/ IEP_CAPR6_REG1 and IEP_CAPR7_REG0/ IEP_CAPR7_REG1, each combined with a fall capture - IEP_CAPF6_REG0/ IEP_CAPF6_REG1 and IEP_CAPF7_REG0/ IEP_CAPF7_REG1, respectively 

      - One global event (any capture event) output for interrupt 

- 16× 64-bit compare registers: IEP_CMPj_REG0/ IEP_CMPj_REG1 (where j = 0 to 15) and IEP_CMP_STATUS_REG[15-0] CMP_STATUS 

   - 16 status bits, write 1h to clear 

   - 16 individual event outputs 

   - One global event output for interrupt generation triggered by any compare event 

- 32 outputs, one high-level and one high-pulse for each compare hit event 

- IEP_CMP_CFG_REG[0] CMP0_RST_CNT_EN, if enabled, resets the controller counter on the next ICSS_IEP_CLK/ ICSS_ICLK cycle 

- Controller counter reset-state is programmable 

- Optional 32-bit shadow mode of operation, which can be configured through IEP_CMP_CFG_REG[17] SHADOW_EN bit 

## _**7.3.12.2.3 32-Bit Shadow Mode**_ 

The IEP module can be configured in 32-bit shadow mode when IEP_CMP_CFG_REG[17] SHADOW_EN bit is set to 1h (default value is 0h, e.g. 64-bit mode of operation is enabled). In this mode, the controller counter will be in 32-bit mode of operation. This enables the shadow copy functionality of the compare registers. 

## **Rules of operation:** 

1. Switching the state of the controller counter from 32-bit Shadow mode to 64-bit mode of operation, the counter should be disabled and bit IEP_CMP_CFG_REG[17] SHADOW_EN should be cleared to 0h (default value). 

2. A new compare update (IEP_CMP_CFG_REG[16-1] CMP_EN = 1h - enables CMP[0:15] event, where [0]CMP_EN maps to CMP0) should be set 4 cycle counts before the next rollover or reset of the counter and to insure the correct shadow copy to active update is correct. 

## **Sequence of operation:** 

498 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

1. Disable counter trough IEP_GLOBAL_CFG_REG[0] CNT_ENABLE = 0h (default value). 

2. Clear controller counter through IEP_CMP_CFG_REG[17] SHADOW_EN = 0h (64-bit mode of operation) 

3. Enable 32-bit Shadow mode through IEP_CMP_CFG_REG[17] SHADOW_EN bit (value: 1h) 

4. Program IEP_CMPm_REGn (where m = 0 to 15 and n = 0 to 1); use the upper 32-bits (IEP_CMP0_REG1[31-0] CMP0_1) of the 64-bit CMP 

   - a. The lower 32-bits are the active compare value (IEP_CMPm_REG0[31-0] CMPm_0, where m = 0 to 15), software can only read this bits 

   - b. The upper 32-bits are the shadow copy (IEP_CMPm_REG1[31-0] CMPm_1, where m = 0 to 15), software can write and read this bits 

5. Enable counter trough IEP_GLOBAL_CFG_REG[0] CNT_ENABLE = 1h 

After the counter is enabled, then software can load a new set of CMP[0:15] without affecting the current active values of (IEP_CMPm_REG0[31-0] CMPm_0, where m = 0 to 15). Only when the counter is reset to 32-bit Shadow mode (IEP_CMP_CFG_REG[17] SHADOW_EN = 1h), it will load the shadow copy of IEP_CMPm_REG1[31-0] CMPm_1 into local copy. 

Shadow compare value (IEP_CMPm_REG1[31-0] CMPm_1) is loaded into active register IEP_CMPm_REG0[31-0] CMPm_0 when the controller counter is configured in 32-bit Shadow mode. If IEP_CMP_CFG_REG[0] CMP0_RST_CNT_EN bit is enabled (value 1h) to reset the counter, the next reset event will be defined by the last CMP0 update. 

## _**7.3.12.2.4 PRU-ICSS IEP Timer Basic Programming Sequence**_ 

Follow these basic steps to configure the IEP Timer. 

## **Counter maintains/function:** 

1. Once enabled, the counter will count every PRU_ICSS_IEP_CLK cycle, default rate of 200 MHz. 

2. It is a free running counter with a sticky over flag status bit. 

3. The counter over flow flag (IEP_GLOBAL_STATUS_REG[0] CNT_OVF) will get set when the counter switches/rollsover from 0xFFFF_FFFF to 0x0000_0000. 

4. The counter will continue to count up. The software will need to read/clear the counter over flow flag and increment the MSB in software variable. 

## **Compare function:** 

1. Initialize timer to known state (default values) 

   - Disable counter (IEP_GLOBAL_CFG_REG[0] CNT_ENABLE = 0) 

   - Reset Count Register (IEP_COUNT_REG0, IEP_COUNT_REG1) by writing FFFFFFFFh to clear 

   - Clear overflow status register (IEP_GLOBAL_STATUS_REG[0] CNT_OVF = 1) 

   - Clear compare status (IEP_CMP_STATUS_REG[15-0] CMP_STATUS) by writing FFFFFFFFh to clear 

2. Set compare values IEP_CMPj_REG0, IEP_CMPj_REG1 (where j = 0 to 15) 

3. Enable compare events (IEP_CMP_CFG_REG[16-1] CMP_EN = 1) 

4. Set increment value (IEP_GLOBAL_CFG_REG[7-4] DEFAULT_INC) 

5. Set compensation value (IEP_COMPEN_REG[22-0] COMPEN_CNT) 

6. Enable counter (IEP_GLOBAL_CFG_REG[0] CNT_ENABLE = 1) 

## **Capture function:** 

1. Update/Enable the counter if required 

2. Program the enable the desired capture event 

3. Wait for global capture event 

4. Read/Clear the capture status to determine which capture event occurred 

5. Read the capture count 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

499 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.3.12.2.5 Industrial Ethernet Mapping**_ 

Some of the capture inputs and compare registers are mapped to specific industrial Ethernet functions in hardware, shown in Table 7-108. All capture inputs are mapped to industrial Ethernet functions, and these inputs are not available for any other application. The CMP1 and CMP2 compare registers also function as the start time triggers for SYNC0 and SYNC1, respectively. 

**Table 7-108. IEP Timer Mode Mapping** 

|**Capture Input**|**IEP Line/Function**|
|---|---|
|IEP_CAPR0_REG0/ IEP_CAPR0_REG1, rise only|If EXT_CAP_EN[0] = 0h (Internal source is selected)/<br>PRU0_RX_SOF<br>If EXT_CAP_EN[0] = 1h (External source is selected)/<br>ICSS_IEP_CAP_INTR_REQ0|
|IEP_CAPR1_REG0/ IEP_CAPR1_REG1, rise only|If EXT_CAP_EN[1] = 0h (Internal source is selected)/<br>PRU0_RX_SFD<br>If EXT_CAP_EN[1] = 1h (External source is selected)/<br>ICSS_IEP0_CAP_INTR_REQ1|
|IEP_CAPR2_REG0/ IEP_CAPR2_REG1, rise only|If EXT_CAP_EN[2] = 0h (Internal source is selected)/<br>PRU1_RX_SOF<br>If EXT_CAP_EN[2] = 1h (External source is selected)/<br>ICSS_IEP_CAP_INTR_REQ2|
|IEP_CAPR3_REG0/ IEP_CAPR3_REG1, rise only|If EXT_CAP_EN[3] = 0h (Internal source is selected)/<br>PRU1_RX_SFD<br>If EXT_CAP_EN[3] = 1h (External source is selected)/<br>ICSS_IEP_CAP_INTR_REQ3|
|IEP_CAPR4_REG0/ IEP_CAPR4_REG1, rise only|If EXT_CAP_EN[4] = 0h (Internal source is selected)/<br>PORT0_TX_SOF; For MII mode uses loopback for lower jitter 40ns<br>versus 4ns.<br>If EXT_CAP_EN[4] = 1h (External source is selected)/<br>ICSS_IEP_CAP_INTR_REQ4|
|IEP_CAPR5_REG0/ IEP_CAPR5_REG1, rise only|If EXT_CAP_EN[5] = 0h (Internal source is selected)/<br>PORT1_TX_SOF<br>For MII mode uses loopback for lower jitter 40ns versus 4ns.<br>If EXT_CAP_EN[5] = 1h (External source is selected)/<br>ICSS_IEP_CAP_INTR_REQ5|
|IEP_CAPR6_REG0/ IEP_CAPR6_REG1 - rise and<br>IEP_CAPF6_REG0/ IEP_CAPF6_REG1 - fall|PR_IEP_EDC_LATCH_IN0 (IO inputs at SoC level)|
|IEP_CAPR7_REG0/ IEP_CAPR7_REG1 - rise and<br>IEP_CAPF7_REG0/ IEP_CAPF7_REG1 - fall|PR_IEP_EDC_LATCH_IN1 (IO inputs at SoC level)|
|IEP_CMP1_REG0/ IEP_CMP1_REG1|For SYNC0 trigger of start time|
|IEP_CMP2_REG0/ IEP_CMP2_REG1|For SYNC1 trigger of start time; only valid in the SYNC2 independent<br>mode|
|IEP_CMP3_REG0/ IEP_CMP3_REG1|For MII TX0 start trigger, if MII register MII_RT_TXCFG0/1[2]<br>TX_EN_MODEn is enabled (where n = 0 or 1).|
|IEP_CMP4_REG0/ IEP_CMP4_REG1|For MII TX1 start trigger, if MII register MII_RT_TXCFG0/1[2]<br>TX_EN_MODEn is enabled (where n = 0 or 1).|



## _**7.3.12.2.6 PRU-ICSS IEP Sync0/Sync1 Module**_ 

The industrial ethernet sync block supports the generation of two synchronization signals: SYNC0 and SYNC1. SYNC0 and SYNC1 can be directly mapped to output signals (pr<k>_iep<n>_edc_sync_out0 and pr<k>_iep<n>_edc_sync_out1) for external devices to use. They can also be used for internal synchronization within the PRU-ICSS. These signals are also mapped as system events and can therefore be mapped to the Arm core's Host interrupts. 

## _**7.3.12.2.6.1 PRU-ICSS IEP Sync0/Sync1 Features**_ 

The industrial ethernet sync block supports the following features: 

- Two synchronize generation signals (SYNC0, SYNC1) 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

500 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

   - Activation time synchronized with IEP Timer 

- IEP_CMP1_REG0/ IEP_CMP1_REG1 triggers SYNC0 activation time 

- IEP_CMP2_REG0/ IEP_CMP2_REG1 triggers SYNC1 activation time (only valid in the SYNC2 independent mode) 

   - Pulse width defined by registers or acknowledge mode (remain asserted until software acknowledged) 

   - Cyclic or single-shot operation 

   - Option to enable or disable sync generation 

- Programmable number of clock cycles between the start of SYNC0 to the start of SYNC1 

## _**7.3.12.2.6.2 PRU-ICSS IEP Sync0/Sync1 Generation Modes**_ 

There are four modes of operation for the sync signals: cyclic mode, single shot mode, cyclic with acknowledge mode, and single shot with acknowledge mode. Figure 7-93 shows examples of these modes. The start time is set by the IEP_SYNC_START_REG[31-0] SYNC_START bit field. The cycle time is configured by the IEP_SYNC0_PERIOD_REG[31-0] SYNC0_PERIOD bit field. The pulse length is defined by IEP_SYNC_PWIDTH_REG[31-0] SYNC_HPW bit field. 

**==> picture [459 x 201] intentionally omitted <==**

**----- Start of picture text -----**<br>
Start Time<br>Pulse Length of<br>Activation SYNC0 Cycle Time Sync Signals<br>Cyclic generation<br>SYNC0<br>Defined by<br>Single Shot SYNC_START<br>SYNC0<br>Acknowledge<br>Cyclic generation with acknowledgement<br>SYNC0<br>Acknowledge<br>Single shot with acknowledgement<br>SYNC0<br>pruss-029<br>**----- End of picture text -----**<br>


**Figure 7-93. PRU-ICSS IEP SYNC0 Signal Generation Modes** 

In SYNC1 dependent mode (IEP_SYNC_CTRL_REG[8] SYNC1_IND_EN = 0h), SYNC1 depends on SYNC0 and the start time of the SYNC1 can be defined by the IEP_SYNC1_DELAY_REG register. Figure 7-94 shows different examples when changing the value in the IEP_SYNC1_DELAY_REG register. Note: If the SYNC1 delay time is 0, SYNC1 reflects SYNC0. Cyclic generation cannot be used for network time synchronized applications because only the CMP1/CMP2 hit occurs in the compensated time domain. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 501 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [486 x 120] intentionally omitted <==**

**----- Start of picture text -----**<br>
SYNC0 : Cyclic generation Start time<br>Activation<br>SYNC0_PERIOD SYNC_HPW<br>Field Value<br>SYNC0_CYCLIC_EN 1<br>SYNC0_ACK_EN 0<br>SYNC_START<br>**----- End of picture text -----**<br>


**==> picture [500 x 372] intentionally omitted <==**

**----- Start of picture text -----**<br>
Start time<br>SYNC0 : Single shot<br>Activation<br>Field Value SYNC_HPW<br>SYNC0_CYCLIC_EN 0<br>SYNC0_ACK_EN 0<br>SYNC_START<br>Cyclic generation<br>SYNC0 : Start time<br>with Acknowledge Activation<br>Acknowledge<br>Field Value<br>SYNC0_CYCLIC_EN 1<br>SYNC0_ACK_EN 1<br>SYNC_START<br>SYNC0_PERIOD<br>Single shot<br>SYNC0 : Start time<br>with Acknowledge Activation<br>Acknowledge<br>Field Value<br>SYNC0_CYCLIC_EN 0<br>SYNC0_ACK_EN 1<br>SYNC_START<br>pruss-031<br>**----- End of picture text -----**<br>


**Figure 7-94. Examples of the Dependent Mode of SYNC1** 

## _**7.3.12.2.7 PRU-ICSS IEP WatchDog**_ 

In industrial ethernet applications, the watchdog timer (WD) is used to monitor process data communication and to turn off the outputs of the digital input/output (DIGIO) functional block after a set time. The WD will thereby protect the system from errors or faults by timeout or expiration. The expiration is used to initiate corrective action in order to keep the system in a safe state and restore normal operation based on configuration. Therefore, if the system is stable, the watchdog timer should be regularly reset or cleared to avoid timeout or expiration. 

The IEP watchdog timer supports the following features: 

- One 16-bit pre-divider for generating a WD clock (default 100μs) based on PRU_ICSS_IEP_CLK input 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

502 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- Two 16-bit Watchdog Timers: 

   - PDI_WD for Sync Managers WD, used in conjunction with digital input/output (DIGIO) 

   - PD_WD for data link layer user WD, used in conjunction with data link layer or application layer interface actions 

## **Note** 

For more details on the PRU-ICSS Industrial Ethernet Watchdog timer, refer also to the Watchdog timer register descriptions covered in the PRU_ICSS_IEP chapter of the Register Addendum. 

## _**7.3.12.2.8 PRU-ICSS IEP DIGIO**_ 

The IEP digital I/O (DIGIO) block provides dedicated I/Os for industrial ethernet protocols. The digital inputs can be sampled when specific events occur or continuously as a raw input. Likewise, driving the digital outputs can be triggered by specific events or controlled by software. The timing, delay cycle clocks, data sources, and data valid of the digital input and outputs are controlled by the IEP_DIGIO_CTRL_REG and IEP_DIGIO_EXP_REG registers. Additionally, the IEP DIGIO block can be used as generic I/Os in other applications. 

## _**7.3.12.2.8.1 PRU-ICSS IEP DIGIO Features**_ 

The IEP digital I/O supports the following features: 

- Digital data output: 

   - 4 channels (PR<k>_IEP0_EDIO_DATA_IN_OUT[31:28]) 

   - 

      - Five event options for driving output data output: 

      - End of frame event (PRU0/1_RX_EOF) 

      - SYNC0 events 

      - SYNC1 events 

      - Watchdog trigger 

      - Software enable 

- Digital data out enable (optional tri-state control) 

- Digital data input: 

   - 4 channels (PR<k>_IEP0_EDIO_DATA_IN_OUT[31:28]) 

   - IEP_DIGIO_DATA_IN_RAW_REG supports direct sampling of PR<k>_IEP0_EDIO_DATA_IN_OUT[31:28] 

   - – IEP_DIGIO_DATA_IN_REG supports four event options to trigger sampling of PR<k>_IEP0_EDIO_DATA_IN_OUT[31:28]: 

      - Start of frame event in start of frame (SOF) mode 

      - pr<k>_iep<n>_edc_latch_in<0/1> event 

      - SYNC0 events: pr<k>_iep<n>_edc_sync_out0 

      - SYNC1 events: pr<k>_iep<n>_edc_sync_out1 

The industrial digital I/Os supported by the PRU-ICSS IEP peripheral are described in Table 7-109. 

**Table 7-109. PRU-ICSS IEP Digital IOs** 

|**Direction**|**Port**|**Mapped to Device I/Os**|**Notes**|
|---|---|---|---|
||||Only|
|output|PR<k>_IEP0_EDIO_DATA_IN_OUT[0:3<br>1]|PR0_IEP0_EDIO_DATA_IN_OUT[31:28]|PR<k>_IEP0_EDIO_DATA_IN_OUT[31:<br>28] are exported to device pins as a|
||||bidirectional.|
|output|PR<k>_EDIO_DATA_OUT_EN[0:31]|No|Optional tri-state control for DATA_OUT|
|output|PR<k>_IEP0_EDIO_OUTVALID|PR0_IEP0_EDIO_OUTVALID|Will pulse even same data|
|output|PR<k>_EDIO_SOF|No|PRU<0/1>_RX_SOF defined by<br>IEP_DIGIO_EXP_REG[12] SOF_SEL|
|input|PR<k>_EDIO_OE_EXT|No||
||||Just export of|
|output|PR<k>_EDIO_WD_TRIG|No|IEP_WD_STATUS_REG[0]|
||||PD_WD_STAT|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 503 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**Table 7-109. PRU-ICSS IEP Digital IOs (continued)** 

|**Direction**|**Port**|**Mapped to Device I/Os**|**Notes**|
|---|---|---|---|
|output|PR<k>_EDIO_DATA_ENA|No|Reserved. Driven low.|
|input|PR<k>_IEP<n>_EDC_LATCH_IN0|PR0_IEP<n>_EDC_LATCH_IN0||
|input|PR<k>_IEP<n>_EDC_LATCH_IN1|PR0_IEP<n>_EDC_LATCH_IN1||
|output|PR<k>_IEP<n>_EDC_SYNC_OUT0|PR0_IEP<n>_EDC_SYNC_OUT0||
|output|PR<k>_IEP<n>_EDC_SYNC_OUT1|PR0_IEP<n>_EDC_SYNC_OUT1||



## _**7.3.12.2.8.2 PRU-ICSS IEP DIGIO Block Diagrams**_ 

Figure 7-95 shows the signals and registers for capturing the DIGIO data in. Note that bit field [5-4]IN_MODE in the IEP_DIGIO_CTRL_REG register must be set to 1h for data to be latched on the external PR<k>_IEP<n>_EDC_LATCH_IN0 signal. In PRU0/1_RX_SOF mode, the delay time of capturing PR<k>_IEP0_EDIO_DATA_IN_OUT[31:28] is programmable through the [11-8]SOF_DLY bit of the IEP_DIGIO_EXP_REG register. 

**==> picture [494 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Industrial EthernetPeripheral (IEP)<br>PRG<k>_IEP0_EDIO_DATA_IN_OUT[31:28]<br>DATA_IN_RAW<br>IN_MODE<br>RX_SOF<br>PRU<0/1> Delay function<br>SOF_DLY<br>PRG<k>_IEP<n>_EDC_LATCH_IN0<br>D Q DATA_IN<br>SYNC0 EN<br>SYNC_PWIDTH<br>SYNC0_PERIOD SYNC1<br>SYNC1_DELAY<br>SYNC0/1<br>n = 0 to 1 : (1) : (2) : (3)<br>(1) Register<br>(2) Internal signal wire<br>(3) External pin input/output<br>**----- End of picture text -----**<br>


**Figure 7-95. IEP DIGIO Data In** 

Figure 7-96 shows the signals and registers for driving the DIGIO data out. 

The PR<k>_IEP0_EDIO_DATA_IN_OUT[31:28] is immediately forced to zero when IEP_DIGIO_CTRL_REG[1] OUTVALID_MODE = 1h, pr1_edio_oe_ext = 1h, and pd_wd_exp = 1h, or the next update hardware post pd_wd_exp. Delay assertion of PR<k>_IEP0_EDIO_OUTVALID from PR<k>_IEP0_EDIO_DATA_IN_OUT[31:28] update events are controlled by software through IEP_DIGIO_EXP_REG[2] SW_OUTVALID. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

504 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

**==> picture [500 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
Industrial Ethernet Peripheral (IEP)<br>OUTVALID_OVR_EN Delay function PRG<k>_IEP0_EDIO_OUTVALID<br>SW_OUTVALID<br>OUTVALID_DLY<br>OUT_MODE<br>RX_EOF<br>PRU<0/1> PRG<k>_IEP0_EDIO_DATA_IN_OUT[31:28]<br>SYNC_PWIDTH SYNC0 DATA_OUT D Q<br>SYNC0_PERIOD SYNC1 EN<br>SYNC1_DELAY<br>SYNC0/1<br>SW_DATA_OUT_UPDATE<br>OUTVALID_MODE<br>WatchDog Timer<br>pr1_edio_oe_ext<br>16-bit WD_PREDIV<br>16-bit16-bit PDI_WDPD_WD pd_wd_expWD_MODE FunctionTiming DATA_OUT_EN pr<k>_edio_data_out_en<br>: (1) : (2) : (3)<br>(1) Register<br>(2) Internal signal wire<br>(3) External pin input/output<br>**----- End of picture text -----**<br>


**Figure 7-96. IEP DIGIO Data Out** 

## _**7.3.12.2.8.3 PRU-ICSS IEP Basic Programming Model**_ 

Follow these steps to configure and read the DIGIO Data Input: 

1. Read IEP_DIGIO_DATA_IN_RAW_REG for raw input data 

or 

1. Enable sampling of PR<k>_IEP0_EDIO_DATA_IN_OUT[31:28] by setting IEP_DIGIO_CTRL_REG[5-4] IN_MODE = 1h. 

2. Read IEP_DIGIO_DATA_IN_REG for data sampled upon PR<k>_IEP<n>_EDC_LATCH_IN0 posedge 

Follow these steps to configure and write to the DIGIO Data Output: 

1. Pre-configure DIGIO by setting IEP_DIGIO_EXP_REG[1] OUTVALID_OVR_EN and IEP_DIGIO_EXP_REG[0] SW_DATA_OUT_UP 

2. Write to IEP_DIGIO_DATA_OUT_REG to configure output data. 

3. To HiZ output, set corresponding IEP_DIGIO_DATA_OUT_EN_REG[31-0] DATA_OUT_EN bits to 1h (clear to 0h to drive value stored in IEP_DIGIO_DATA_OUT_REG). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 505 

Copyright © 2025 Texas Instruments Incorporated 

