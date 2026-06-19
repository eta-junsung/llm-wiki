<!-- AM263P TRM | 6 Device Configuration | 원본 p.224-315 | pymupdf4llm text+tables, images omitted -->

_Device Configuration_ 

www.ti.com 

_Chapter 6_ _**Device Configuration**_ 

**==> picture [506 x 40] intentionally omitted <==**

This chapter describes the device configuration details including information related to Control MMR's, Power, Reset, and Clocking. 

**6.1 Control Module** ......................................................................................................................................................... 225 **6.2 Power** .........................................................................................................................................................................253 **6.3 Reset** ..........................................................................................................................................................................269 **6.4 Clocking** .....................................................................................................................................................................278 

224 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **6.1 Control Module** 

## _**6.1.1 Control Overview**_ 

The Control module is the main controller for top-level device behavior in various states. This module contains registers for configuration, bootstrap (SOP) signals, I/O terminal pad multiplexing, clock selection, and many other device-level configuration options. MMR (Memory Mapped Registers) are used by software to program the hardware. The register is directly accessible from software because it is mapped into a memory location of the memory-map, such that writing to and reading from that memory location corresponds to writing to and reading from the hardware register. There are various Control Module or CTRLMMR modules defined in this device: 

## General SoC Control Modules 

- TOP_CTRL (CTRLMMR0): SoC-level configuration registers 

- MSS_CTRL (CTRLMMR1): SoC and peripheral-level configuration registers 

- CONTROLSS_CTRL (CTRLMMR2): CONTROLSS-level configuration registers including general control, reset, and clocking-related functions for the real time control subsystem (CONTROLSS)) 

## Pad Configuration Control Modules 

- IOMUX (PADCFG_CTRLMMR0): SoC-level terminal configuration control registers 

## Reset and Clocking Control Modules 

- MSS_TOPRCM (RCM_CTRLMMR0): SoC-level Clock and Reset control registers 

- MSS_RCM (RCM_CTRLMMR1): SoC and Peripheral-level Clock and Reset control registers 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

225 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **6.1.1.1 MMR Write Protection** 

All Control Module MMR have a protection mechanism which prevents spurious writes from changing register values. LOCK0_KICK0 and LOCK0_KICK1 registers are used for this purpose. The sequence to unlock these MMR is as follows: 

1. Write exact unlock value (Table 6-1) to <Control Module>LOCK0_KICK0:KEY field 

2. Write exact unlock value (Table 6-1) to <Control Module>LOCK0_KICK1:KEY field 

The sequence to lock the MMR is as follows: 

1. Write zero (or anyother value other than the unlock value)Table 6-1) to <Control Module>LOCK0_KICK1:KEY field 

2. Write zero (or anyother value other than the unlock value)Table 6-1) to <Control Module>LOCK0_KICK0:KEY field 

- 

## **Note** 

If the above sequence for locking the IOMUX is not followed, an AHB_WRITE_ERROR interrupt will occur (if enabled). 

For example, to unlock Control Module MSS_CTRL the sequence is as below: 

1. Write 0x01234567 to MSS_CTRL.LOCK0_KICK0:KEY 

2. Write 0xFEDCBA8 to MSS_CTRL.LOCK0_KICK1:KEY 

To lock the Control Module MSS_CTRL the sequence is as below: 

1. Write 0x0 to MSS_CTRL.LOCK0_KICK1:KEY 

2. Write 0x0 to MSS_CTRL.LOCK0_KICK0:KEY 

Any writes to locked memory region will result in assertion of the MMR_ACCESS_ERR_WR event by the respective control modules. This assertion can be enabled or disabled by writing the appropriate value to <Control Module>.INTR_ENABLE.KICK_ERR_EN field. 

The table below shows the values that must be written to the LOCK0_KICK0 and LOCK0_KICK1 registers to unlock the various Control modules' MMR. 

**Table 6-1. Kick Protection Register Unlock Values** 

|**Protected Register**|**LockKick Register**|**Unlock Value**|
|---|---|---|
|TOP_CTRL|LOCK0_KICK0|0x01234567|
||LOCK0_KICK1|0xFEDCBA8|
|MSS_CTRL|LOCK0_KICK0|0x01234567|
||LOCK0_KICK1|0xFEDCBA8|
|CONTROLSS_CTRL|LOCK0_KICK0|0x01234567|
||LOCK0_KICK1|0xFEDCBA8|
|TOP_RCM|LOCK0_KICK0|0x01234567|
||LOCK0_KICK1|0xFEDCBA8|
|MSS_RCM|LOCK0_KICK0|0x01234567|
||LOCK0_KICK1|0xFEDCBA8|
|IOMUX|LOCK0_KICK0|0x83E70B13|
||LOCK0_KICK1|0x95A4F1E0|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

226 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **Note** 

To maintain that all registers from a given partition are write protected, software must always re-lock the protection mechanism after completing the register writes. 

The kick protection registers described in this section are an exception and are not write protected by the protection mechanism. 

## **6.1.1.2 MMR Access Error Interrupt** 

The Control Modules can generate the access error interrupts MMR_ACCESS_ERR_WR and 

MMR_ACCESS_ERR_RD. The interrupts are asserted when one or more of the following accesses are made: 

- (a) write access when MMR are locked 

- (b) access to illegal address in the control module 

The following registers are related to handling of these errors inside the respective Control Module. 

- <Control Module>INTR_RAW_STATUS - Interrupt Raw Status/Set register 

- <Control Module>INTR_ENABLED_STATUS_CLEAR - Interrupt Enabled Status/Clear register 

- <Control Module>INTR_ENABLE - Interrupt Enable register 

- <Control Module>INTR_ENABLE_CLEAR - Interrupt Enable Clear register 

The following applies for the interrupt behavior of each Control Module: 

- The Control Module only asserts the interrupt line if the interrupt is enabled. 

   - Interrupts are **enabled** by setting the corresponding bits in the INTR_ENABLE register to 1h. 

   - Interrupts are **disabled** by setting the corresponding bits in the INTR_ENABLE_CLEAR register to 1h. 

- After an interrupt has been serviced, software must clear the corresponding status flag. This is done by setting to 1h the corresponding bit in the INTR_ENABLED_STATUS_CLEAR register which also clears the corresponding bit in the INTR_RAW_STATUS register. The status flags in the INTR_RAW_STATUS register are set even if the corresponding interrupt is disabled. The INTR_ENABLED_STATUS_CLEAR register is only set if the corresponding interrupt is enabled. 

- An interrupt is generated by the control module if the relevant bit in the INTR_RAW_STATUS register is set to 1h and the interrupt is enabled through the INTR_ENABLE register. This feature is useful during user software debugging. In addition, even if interrupts are disabled, the corresponding raw flag in the INTR_RAW_STATUS register is set to 1h when an interrupt condition occurs. 

- If interrupts are disabled, the corresponding raw flag in the INTR_RAW_STATUS register is set to 1h when an interrupt condition occurs. The INTR_RAW_STATUS can be cleared by setting the corresponding bit in the INTR_RAW_STATUS register to 1h. 

The MSS_CTRL module aggregates the Control Module interrupts MMR_ACCESS_ERR_WR and MMR_ACCESS_ERR_RD and generates MMR_ACCESS_ERRAGGR to the R5 Cores (see Section 6.1.3.2.7). 

## **Note** 

CONTROLSS_GLOBAL_CTRL is not aggregated into MSS_CTRL's MMR_ACCESS_ERR_WR and MMR_ACCESS_ERR_RD 

Table 6-2 lists the interrupt events which can assert the MSS_CTRL Access Error. 

**Table 6-2. MSS_CTRL Access Error Interrupt Events** 

|**Event Name**|**Event Flag**|**Event Mask**|**Description**|
|---|---|---|---|
|MMR_ACCESS_ERR_WR|INTR_RAW_STATUS.KICK_ERR|INTR_ENABLE.KICK_ERR_EN|Lock violation interrupt. Occurs<br>when writing to a register in a<br>locked control module.|
|MMR_ACCESS_ERR_RD|INTR_RAW_STATUS.ADDR_ERR|INTR_ENABLE.ADDR_ERR_EN|Read addressing violation<br>interrupt. Occurs when reading<br>an illegal address inside the<br>control module.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 227 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-2. MSS_CTRL Access Error Interrupt Events (continued)** 

|**Event Name**|**Event Flag**|**Event Mask**|**Description**|
|---|---|---|---|
|MMR_ACCESS_ERR_WR|INTR_RAW_STATUS.ADDR_ERR|INTR_ENABLE.ADDR_ERR_EN|Write addressing violation<br>interrupt. Occurs when writing an<br>illegal address inside the control<br>module.|



When an error event as described in Table 6-2 above occurs, the associated error details are captured in the FAULT_ADDRESS, FAULT_TYPE_STATUS, and FAULT_ATTR_STATUS registers. 

FAULT_ADDRESS contains the address of the first fault access. FAULT_TYPE_STATUS and FAULT_ATTR_STATUS contain status attributes associated with the first fault access. To clear the contents of these three registers and allow them to latch the attributes of the next fault the FAULT_CLEAR.FAULT_CLR bit must be set to 1h. 

## _**6.1.2 TOP_CTRL**_ 

The TOP_CTRL (CTRLMMR0) module has MMR associated with the following functions: 

- _Power OK (POK) Modules_ 

- _Thermal Manager_ 

228 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **6.1.2.1 TOP_CTRL Integration** 

**==> picture [341 x 382] intentionally omitted <==**

**----- Start of picture text -----**<br>
THRHLD_LOW_INTR<br>THRHLD_HIGH_INT<br>R5SS*_CORE*<br>R5SS*_CORE*<br>R5SS*_CORE* THERMAL<br>R5SS*_CORE* MANAGER<br>ESM VMON_ERR_H<br>VMON_ERR_L POK<br>SYSCLK<br>RCCLK<br>TOP RCM<br>TEMPSENSE_32K_CLK<br>RSTn<br>MMR_ACCESS_ERR_RD<br>MSS CTRL<br>MMR_ACCESS_ERR_WR<br>MMR<br>Configuration<br>Port<br>TOP CTRL<br>VIM<br>Interconnect<br>VBUSP CORE<br>**----- End of picture text -----**<br>


**Figure 6-1. TOP_CTRL Integration Diagram** 

**Table 6-3. TOP_CTRL Device Integration** 

|**Module Instance**|**Device Allocation**|**Interconnect**|
|---|---|---|
|TOP_CTRL|✔|VBUSP CORE Interconnect|



**Table 6-4. TOP_CTRL Clocks and Resets** 

|**Clocks**|**Clocks**|**Clocks**|**Clocks**|**Clocks**|
|---|---|---|---|---|
|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Description**|
|TOP_CTRL|CLK|SYSCLK|TOP_RCM|Functional and Interface Clock|
|TOP_CTRL|RCCLK|RCCLK10M|TOP_RCM|POK Filter clock|
|TOP_CTRL|TEMPSENSE_32K_CLK|XTAL_TEMPSENSE_32K_CLK|TOP_RCM|Thermal Manager clock|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 229 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-5. TOP_CTRL Resets** 

|**Resets**|**Resets**|**Resets**|**Resets**|**Resets**|
|---|---|---|---|---|
|**Module Instance**|**Module Input**|**Source Signal**|**Source**|**Description**|
|TOP_CTRL|RST|SYSRESET|TOP_RCM|TOP_CTRL Reset|
|TOP_CTRL|TSENSE_RESET|TSENSE_RESET|MSS_RCM|Thermal Manager Reset|



## **Table 6-6. TOP_CTRL Interrupt Requests** 

|**Module**<br>**Instance**|**Module Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|TOP_CTRL|MMR_ACCESS_ERR_RD|TOP_CTRL_RD_ACCESS_ERR|MSS_CTRL|Level|Read Access<br>Error Interrupt<br>indicating protection,<br>addressing, or lock<br>violation|
||MMR_ACCESS_ERR_WR|TOP_CTRL_WR_ACCESS_ERR|||Write Access<br>Error Interrupt<br>indicating protection,<br>addressing, or lock<br>violation|
||THRHLD_HIGH_INTR<br>(INTR_TSENSE_H)|R5SS*_CORE*_INTR_IN_133|R5SS*_CORE*_VIM||Temperature High<br>Threshold Interrupt|
||THRHLD_LOW_INTR<br>(INTR_TSENSE_L)|R5SS*_CORE*_INTR_IN_134|||Temperature Low<br>threshold Interrupt|



**Table 6-7. TOP_CTRL ESM Interrupts** 

|**Module**<br>**Instance**|**Module Interrupt Signal**|**Destination Interrupt**<br>**Input**|**Destination **|**Type**|**Description**|
|---|---|---|---|---|---|
|TOP_CTRL|VMON_ERR_H|ESM_LVL_EVENT_41|ESM|Level|POK Voltage monitor error high interrupt|
||VMON_ERR_L|ESM_LVL_EVENT_42|||POK Voltage monitor error low interrupt|



230 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.1.3 MSS_CTRL**_ 

The MSS_CTRL module has MMR associated with the following functions: 

- R5FSS CPU Global Configuration and Control 

- Memory Initialization 

- EDMA Global Configuration and Event Aggregation 

- CPSW Global Configuration 

- 

- _OSPI Global Configuration_ 

- _USB Global Configuration_ 

- MPU Interrupt Aggregator 

- MMR Access Error Interrupt Aggregator 

- Safety Registers 

- Interconnect Safety 

- MSS_CTRL MMR Kick Protection Registers 

- MSS_CTRL MMR Access Error 

## **6.1.3.1 MSS_CTRL Integration** 

**==> picture [467 x 304] intentionally omitted <==**

**----- Start of picture text -----**<br>
MMR_ACCESS_ERRAGGR<br>/4 R5SS*_CORE*_INTR_MPU_PROT_ERRAGG<br>/4 R5SS*_CORE*_INTR_MPU_ADDR_ERRAGG<br>R5SS*_CORE* /4 R5SS*_CORE*_INTR_SW_IRQ<br>R5SS*_CORE* /4 R5SS*_CORE*_INTR_MBOX_READ_DONE<br>R5SS*_CORE* /4 R5SS*_CORE*_INTR_MBOX_READ_REQ<br>R5SS*_CORE*<br>TPCC0_INTAGGR<br>TPCC0_ERRAGGR IP/SoC Control & Events<br>VBUSP_ERRAGG_H<br>ESM /2/4 VBUSM_ERRAGG_H/LR5SS*_CORE*_INTR_TCM_ADDRPARITY_ERRAGG MMR<br>Configuration<br>/4 R5SS*_CORE*_INTR_ECC_UNCORR_ERRAGG Port<br>/4 R5SS*_CORE*_INTR_ECC_CORR_ERRAGG<br>SYSCLK<br>TOP RCM RSTn<br>MMR_ACCESS_ERR_RD<br>MMR_ACCESS_ERR_WR<br>ICSSM Interrupt  /2 ICSSM*MBOX_READ_DONE<br>xBAR /2 ICSSM*MBOX_READ_REQ<br>MSS CTRL<br>VIM<br>Interconnect<br>VBUSP CORE<br>**----- End of picture text -----**<br>


**Figure 6-2. MSS_CTRL Integration Diagram** 

**Table 6-8. MSS_CTRL Integration Attributes** 

|**Module Instance**|**Attributes**|
|---|---|
||**Interconnect**|
|MSS_CTRL|VBUSP CORE Interconnect|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

231 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-9. MSS_CTRL Clocks and Resets** 

|**Module Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Description**|
|---|---|---|---|---|
|**Clocks**|||||
|MSS_CTRL|CLK|SYSCLK|TOP_RCM|Functional and Interface<br>Clock|
|**Resets**|||||
|MSS_CTRL|RST|SYSRESET|TOP_RCM|MSS_CTRL Reset|



**Table 6-10. MSS_CTRL Hardware Requests** 

|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|
|---|---|---|---|---|---|
|**Module**<br>**Instance**|**Module Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Description**|**Type**|
|MSS_CTRL|ICSS_PRU0_MBOX_READ_REQ|IN_INTR51|PRU_ICSS_XBAR_INTR<br>TR0|Interrupt<br>indicating<br>Mailbox Read<br>Request to<br>PRU0|Level|
|MSS_CTRL|ICSS_PRU0_MBOX_READ_DONE|IN_INTR53|PRU_ICSS_XBAR_INTR<br>TR0|Interrupt<br>indicating<br>Mailbox Read<br>Done to PRU0|Level|
|MSS_CTRL|ICSS_PRU1_MBOX_READ_REQ|IN_INTR52|PRU_ICSS_XBAR_INTR<br>TR0|Interrupt<br>indicating<br>Mailbox Read<br>Request to<br>PRU0|Level|
|MSS_CTRL|ICSS_PRU1_MBOX_READ_DONE|IN_INTR54|PRU_ICSS_XBAR_INTR<br>TR0|Interrupt<br>indicating<br>Mailbox Read<br>Done to PRU0|Level|
|MSS_CTRL|R5FSS0_CORE0_INTR_MBOX_READ<br>_REQ|R5SS0_CORE0_INTR_IN_136|R5SS0_CORE0_VIM|Interrupt<br>indicating<br>Mailbox Read<br>Request to<br>R5SS0 CORE0|Level|
|MSS_CTRL|R5FSS0_CORE0_INTR_MBOX_READ<br>_DONE|R5SS0_CORE0_INTR_IN_137|R5SS0_CORE0_VIM|Interrupt<br>indicating<br>Mailbox Read<br>Done to R5SS0<br>CORE0|Level|
|MSS_CTRL|R5FSS0_CORE1_INTR_MBOX_READ<br>_REQ|R5SS0_CORE1_INTR_IN_136|R5SS0_CORE1_VIM|Interrupt<br>indicating<br>Mailbox Read<br>Request to<br>R5SS0 CORE1|Level|
|MSS_CTRL|R5FSS0_CORE1_INTR_MBOX_READ<br>_DONE|R5SS0_CORE1_INTR_IN_137|R5SS0_CORE1_VIM|Interrupt<br>indicating<br>Mailbox Read<br>Done to R5SS0<br>CORE1|Level|
|MSS_CTRL|R5FSS1_CORE0_INTR_MBOX_READ<br>_REQ|R5SS1_CORE0_INTR_IN_136|R5SS1_CORE0_VIM|Interrupt<br>indicating<br>Mailbox Read<br>Request to<br>R5SS1 CORE0|Level|
|MSS_CTRL|R5FSS1_CORE0_INTR_MBOX_READ<br>_DONE|R5SS1_CORE0_INTR_IN_137|R5SS1_CORE0_VIM|Interrupt<br>indicating<br>Mailbox Read<br>Done to R5SS1<br>CORE0|Level|



232 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-10. MSS_CTRL Hardware Requests (continued)** 

|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|
|---|---|---|---|---|---|
|**Module**<br>**Instance**|**Module Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Description**|**Type**|
|MSS_CTRL|R5FSS1_CORE1_INTR_MBOX_READ<br>_REQ|R5SS1_CORE1_INTR_IN_136|R5SS1_CORE1_VIM|Interrupt<br>indicating<br>Mailbox Read<br>Request to<br>R5SS1 CORE1|Level|
|MSS_CTRL|R5FSS1_CORE1_INTR_MBOX_READ<br>_DONE|R5SS1_CORE1_INTR_IN_137|R5SS1_CORE1_VIM|Interrupt<br>indicating<br>Mailbox Read<br>Done to R5SS1<br>CORE1|Level|
|MSS_CTRL|R5FSS0_CORE0_INTR_SW_IRQ|R5SS0_CORE0_INTR_IN_129|R5SS0_CORE0_VIM|Interrupt<br>indicating SW<br>Interrupt to<br>R5SS0 CORE0|Level|
|MSS_CTRL|R5FSS0_CORE1_INTR_SW_IRQ|R5SS0_CORE1_INTR_IN_129|R5SS0_CORE1_VIM|Interrupt<br>indicating SW<br>Interrupt to<br>R5SS0 CORE1|Level|
|MSS_CTRL|R5FSS1_CORE0_INTR_SW_IRQ|R5SS1_CORE0_INTR_IN_129|R5SS1_CORE1_VIM|Interrupt<br>indicating SW<br>Interrupt to<br>R5SS1 CORE0|Level|
|MSS_CTRL|R5FSS1_CORE1_INTR_SW_IRQ|R5SS1_CORE1_INTR_IN_129|R5SS1_CORE1_VIM|Interrupt<br>indicating SW<br>Interrupt to<br>R5SS1 CORE1|Level|
|MSS_CTRL|R5FSS0_CORE0_INTR_MPU_PROT_<br>ERRAGG|R5SS0_CORE0_INTR_IN _70|R5SS0_CORE0_VIM|Aggregated<br>Interrupt<br>indicating MPU<br>Protection<br>Error to R5SS0<br>CORE0|Level|
|MSS_CTRL|R5FSS0_CORE1_INTR_MPU_PROT_<br>ERRAGG|R5SS0_CORE1_INTR_IN _70|R5SS0_CORE1_VIM|Aggregated<br>Interrupt<br>indicating MPU<br>Protection<br>Error to R5SS0<br>CORE1|Level|
|MSS_CTRL|R5FSS1_CORE0_INTR_MPU_PROT_<br>ERRAGG|R5SS1_CORE0_INTR_IN _70|R5SS1_CORE0_VIM|Aggregated<br>Interrupt<br>indicating MPU<br>Protection<br>Error to R5SS1<br>CORE0|Level|
|MSS_CTRL|R5FSS1_CORE1_INTR_MPU_PROT_<br>ERRAGG|R5SS1_CORE1_INTR_IN _70|R5SS1_CORE1_VIM|Aggregated<br>Interrupt<br>indicating MPU<br>Protection<br>Error to R5SS1<br>CORE1|Level|
|MSS_CTRL|R5FSS0_CORE0_INTR_MPU_ADDR_<br>ERRAGG|R5SS0_CORE0_INTR_IN _69|R5SS0_CORE0_VIM|Aggregated<br>Interrupt<br>indicating MPU<br>Address Error<br>to R5SS0<br>CORE0|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 233 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-10. MSS_CTRL Hardware Requests (continued)** 

|**Interrupt Requests**|**Interrupt Requests**|||||
|---|---|---|---|---|---|
|**Module**<br>**Instance**|**Module Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Description**|**Type**|
|MSS_CTRL|R5FSS0_CORE1_INTR_MPU_ADDR_<br>ERRAGG|R5SS0_CORE1_INTR_IN _69|R5SS0_CORE1_VIM|Aggregated<br>Interrupt<br>indicating MPU<br>Address Error<br>to R5SS0<br>CORE1|Level|
|MSS_CTRL|R5FSS1_CORE0_INTR_MPU_ADDR_<br>ERRAGG|R5SS1_CORE0_INTR_IN _69|R5SS1_CORE0_VIM|Aggregated<br>Interrupt<br>indicating MPU<br>Address Error<br>to R5SS1<br>CORE0|Level|
|MSS_CTRL|R5FSS1_CORE1_INTR_MPU_ADDR_<br>ERRAGG|R5SS1_CORE1_INTR_IN _69|R5SS1_CORE1_VIM|Aggregated<br>Interrupt<br>indicating MPU<br>Address Error<br>to R5SS1<br>CORE1|Level|
|MSS_CTRL|MMR_ACCESS_ERRAGGR|R5SS0_CORE0_INTR_IN_124|R5SS0_CORE0_VIM|Aggregated<br>Interrupt<br>indicating MMR<br>Access Error|Level|
|||R5SS0_CORE1_INTR_IN_124|R5SS0_CORE1_VIM|||
|||R5SS0_CORE0_INTR_IN_124|R5SS0_CORE0_VIM|||
|||R5SS1_CORE1_INTR_IN_124|R5SS1_CORE1_VIM|||
|MSS_CTRL|TPCC_A_INTAGGR|R5SS0_CORE0_INTR_IN _72|R5SS0_CORE0_VIM|Aggregated<br>Interrupt from<br>EDMA Interrupt<br>sources|Level|
|||R5SS0_CORE1_INTR_IN _72|R5SS0_CORE1_VIM|||
|||R5SS0_CORE0_INTR_IN _72|R5SS0_CORE0_VIM|||
|||R5SS1_CORE1_INTR_IN _72|R5SS1_CORE1_VIM|||
|MSS_CTRL|TPCC_A_ERRGGR|R5SS0_CORE0_INTR_IN _73|R5SS0_CORE0_VIM|Aggregated<br>Interrupt from<br>EDMA Error<br>sources|Level|
|||R5SS0_CORE1_INTR_IN _73|R5SS0_CORE1_VIM|||
|||R5SS0_CORE0_INTR_IN _73|R5SS0_CORE0_VIM|||
|||R5SS1_CORE1_INTR_IN _73|R5SS1_CORE1_VIM|||
|**ESM Events**||||||
|MSS_CTRL|TPCC_A_ERRGGR|ESM_LVL_EVENT_63|ESM|Aggregated<br>Error from<br>EDMA Error<br>sources|Level|
|MSS_CTRL|R5SS0_CORE0_CORR_ERRAGG|ESM_LVL_EVENT_47|ESM|Aggregated<br>Correctable<br>Memory ECC<br>Error from<br>R5SS0 CORE0|Level|
|MSS_CTRL|R5SS0_CORE1_CORR_ERRAGG|ESM_LVL_EVENT_49|ESM|Aggregated<br>Correctable<br>Memory ECC<br>Error from<br>R5SS0 CORE1|Level|
|MSS_CTRL|R5SS1_CORE0_CORR_ERRAGG|ESM_LVL_EVENT_55|ESM|Aggregated<br>Correctable<br>Memory ECC<br>Error from<br>R5SS1 CORE0|Level|



234 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-10. MSS_CTRL Hardware Requests (continued)** 

|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|**Interrupt Requests**|
|---|---|---|---|---|---|
|**Module**<br>**Instance**|**Module Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Description**|**Type**|
|MSS_CTRL|R5SS1_CORE1_CORR_ERRAGG|ESM_LVL_EVENT_57|ESM|Aggregated<br>Correctable<br>Memory ECC<br>Error from<br>R5SS1 CORE1|Level|
|MSS_CTRL|R5SS0_CORE0_UNCORR_ERRAGG|ESM_LVL_EVENT_48|ESM|Aggregated<br>Uncorrectable<br>Memory ECC<br>Error from<br>R5SS0 CORE0|Level|
|MSS_CTRL|R5SS0_CORE1_UNCORR_ERRAGG|ESM_LVL_EVENT_50|ESM|Aggregated<br>Uncorrectable<br>Memory ECC<br>Error from<br>R5SS0 CORE1|Level|
|MSS_CTRL|R5SS1_CORE0_UNCORR_ERRAGG|ESM_LVL_EVENT_56|ESM|Aggregated<br>Uncorrectable<br>Memory ECC<br>Error from<br>R5SS1 CORE0|Level|
|MSS_CTRL|R5SS1_CORE1_UNCORR_ERRAGG|ESM_LVL_EVENT_58|ESM|Aggregated<br>Uncorrectable<br>Memory ECC<br>Error from<br>R5SS1 CORE1|Level|
|MSS_CTRL|R5SS0_CORE0_TCM_ADDRPARITY_<br>ERRAGG|ESM_LVL_EVENT_14|ESM|Aggregated<br>TCM Address<br>parity Error<br>from R5SS0<br>CORE0|Level|
|MSS_CTRL|R5SS0_CORE1_TCM_ADDRPARITY_<br>ERRAGG|ESM_LVL_EVENT_15|ESM|Aggregated<br>TCM Address<br>parity Error<br>from R5SS0<br>CORE1|Level|
|MSS_CTRL|R5SS1_CORE0_TCM_ADDRPARITY_<br>ERRAGG|ESM_LVL_EVENT_16|ESM|Aggregated<br>TCM Address<br>parity Error<br>from R5SS1<br>CORE0|Level|
|MSS_CTRL|R5SS1_CORE1_TCM_ADDRPARITY_<br>ERRAGG|ESM_LVL_EVENT_17|ESM|Aggregated<br>TCM Address<br>parity Error<br>from R5SS1<br>CORE1|Level|
|MSS_CTRL|VBUSM_ERRAGG_H|ESM_LVL_EVENT_33|ESM|Aggregated<br>VBUSM Bus<br>Safety Error<br>High|Level|
|MSS_CTRL|VBUSM_ERRAGG_L|ESM_LVL_EVENT_34|ESM|Aggregated<br>VBUSM Bus<br>Safety Error<br>Low|Level|
|MSS_CTRL|VBUSP_ERRAGG_H|ESM_LVL_EVENT_31|ESM|Aggregated<br>VBUSP Bus<br>Safety Error|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 235 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **6.1.3.2 MSS_CTRL Functional Description** 

## _**6.1.3.2.1 R5FSS CPU Global Configuration and Control**_ 

## _**6.1.3.2.1.1 R5SS Lock Step/Dual Core Configuration**_ 

The R5SS*_CONTROL register configures the lockstep/dual core behavior of the R5SS*. 

When R5SS*_CONTROL.LOCK_STEP is programmed to 0x7, it configures R5SS* to be in lockstep. When programmed to 0x0, it configures R5SS* to be in dual core mode. 

A reset must be issued to R5SS* to switch between dual core and lockstep mode. 

When R5SS*_CONTROL.RESET_FSM_TRIGGER is programmed to 0x7, it issues a reset to R5SS*. 

## **Note** 

By default, after a device reset, both R5SS0 and R5SS1 are in lockstep. Each cluster can be independently configured to be in dual core by the application. 

## **Note** 

Lockstep to dual core switch can be programmed only once, and cannot be reprogrammed until the device's next power on reset cycle. 

R5SS*_STATUS_REG. LOCK_STEP bitfield indicates the mode of R5SS. LOCK_STEP = 0 indicates the corresponding R5SS is in dual core mode, and LOCK_STEP = 1 indicates the corresponding R5SS is in lockstep mode. 

## _**6.1.3.2.1.2 R5 Core Halting and Unhalting**_ 

The R5SS*_CORE*_HALT register halts and unhalts the respective R5 Cores. Programming R5SS*_CORE*_HALT.HALT bitfield to 0x7 halts the respective R5 Core. Programming the bitfield to 0x0 unhalts the respective R5 Core. 

## _**6.1.3.2.1.3 R5 Wait-For-Interrupt (WFI)**_ 

The R5SS*_CORE*_STAT register provides the Wait-For-Event (WFE) and Wait-For-Interrupt (WFI) status of the respective R5 Cores. 

R5SS*_CORE*_STAT.WFI_STAT = 1 indicates the respective R5 core is in WFI. 

R5SS*_CORE*_STAT.WFE_STAT = 1 indicates the respective R5 core is in WFE. 

## _**6.1.3.2.2 Memory Initialization**_ 

The SRAM memories in the device are protected by SECDED ECC for functional safety. At bootup, the memory content must be initialized for ECC. Memory initialization can be triggered by the memory initialization registers. 

## _**6.1.3.2.2.1 R5 TCM Memory Initialization**_ 

R5SS*_ATCM_MEM_INIT. MEM_INIT bitfield, when programmed to 1, initializes the ATCM memories of the corresponding R5SS. 

R5SS*_ATCM_MEM_INIT_STATUS. MEM_STATUS shows the status of memory initialization. If the bitfield reads ‘1’, it indicates the memory initialization is in progress. 

R5SS*_ATCM_MEM_INIT_DONE. MEM_INIT_DONE bitfield is set when the memory initialization is complete. Writing ‘1’ to this field clears the field. 

R5SS*_BTCM_MEM_INIT , R5SS*_BTCM_MEM_INIT_STATUS and R5SS*_BTCM_MEM_INIT_DONE are associated with R5SS BTCM memory initialization. 

## _**6.1.3.2.2.2 L2 OCRAM and Mailbox RAM and EDMA RAM Memory Initialization**_ 

The L2_MEM_INIT register is used to initialize the data and ECC of the L2OCRAM. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

236 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

The L2OCRAM is split into six banks. 

L2_MEM_INIT_PARTITION0, when programmed to 1, triggers the initialization of Bank0 of L2 OCRAM. 

Similarly PARTITION0, 1, 2 and 3 bit fields trigger initialization of Bank 0, 1, 2 and 3 of L2 OCRAM, respectively. 

The L2_MEM_INIT_STATUS register shows the status of memory initialization. If the bit field reads ‘1’, it indicates the memory initialization is in progress. 

L2_MEM_INIT_DONE_PARTITIONx bit field is set when the memory initialization of corresponding bank of L2OCRAM is complete. Writing ‘1’ to this field clears the field. 

The MAILBOX_MEM_INIT, MAILBOX_MEM_INIT_STATUS and MAILBOX_MEM_INIT_DONE registers are associated with Mailbox RAM ECC Initialization 

The TPCC_MEM_INIT, TPCC_MEMINIT_STATUS, and TPCC_MEM_INIT_DONE registers are associated with EDMA TPCC memory initialization. 

## _**6.1.3.2.3 EDMA Configuration**_ 

## _**6.1.3.2.3.1 EDMA Global Configuration and Event Aggregation**_ 

The register TPTC_DBS_CONFIG configures the burst size of the DMA transfer. The bitfields TPTC_A0 and TPTC_A1 configure the burst size of TPTC_A0 and TPTC_A1, respectively. 

The registers TPCC_A_INTAGG_MASK, TPCC_A_INTAGG_STATUS, and TPCC_A_INTAGG_STATUS_RAW are associated with the aggregated interrupt from EDMA TPCC_A_INTAGGR. The TPCC_A_INTAGG_MASK register can be configured to mask unwanted interrupt sources from EDMA from triggering the TPCC_A_INTAGGR interrupt. 

The TPCC_A_INTAGG_STATUS register indicates the status of interrupt sources which caused the TPCC_A_INTAGGR interrupt to occur. The TPCC_A_INTAGG_STATUS_RAW register indicates the raw status of interrupt sources of the TPCC_A_INTAGGR interrupt. 

## _**6.1.3.2.3.2 EDMA Error Aggregation**_ 

The registers TPCC_A_ERRAGG_MASK, TPCC_A_ERRAGG_STATUS, and TPCC_A_ERRAGG_STATUS_RAW are associated with the aggregated interrupt from EDMA TPCC_A_ERRAGGR. The TPCC_A_ERRAGG_MASK register can be configured to mask unwanted interrupt sources from EDMA from triggering the TPCC_A_ERRAGGR interrupt. The TPCC_A_ERRAGG_STATUS register indicates the status of interrupt sources which caused the TPCC_A_ERRAGGR interrupt to occur. The TPCC_A_ERRAGG_STATUS_RAW register indicates the raw status of interrupt sources of the TPCC_A_ERRAGGR interrupt. 

## _**6.1.3.2.4 CPSW Global Configuration**_ 

The CPSW_CONTROL register is used for the global configuration of CPSW modes. 

The CPSW_CONTROL.PORT*_MODE_SEL bitfield configures the Ethernet mode of the corresponding port of CPSW to be in either MII, RMII, or RGMII. 

CPSW_CONTROL.RGMII*_ID_MODE, when set to 1, enables the internal delay mode for the transmit path of the corresponding RGMII port. This provides a phase shift of a quarter cycle between clock and data. 

CPSW_CONTROL.RMII*_REF_CLK_OE_N controls how the RMII REF_CLK is generated in the system. 

As shown in Figure 6-3, the RMII*_REF_CLK can be generated from the device, fed to the CPSW module and transmitted out to device pins. Alternately, the RMII*_REF_CLK can be sourced from an external clock input to the device. 

CPSW_CONTROL.RMII*_REF_CLK_SEL is used to select the RMII*_REF_CLK source, either from the IO pad (write 0x0) or from an internal source (write 0x1). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

237 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**==> picture [499 x 361] intentionally omitted <==**

**----- Start of picture text -----**<br>
RMII2_REF_CLK<br>RMII2_REF_CLK_IN<br>OE_N<br>CPSW_CONTROL.RMII_REF2_CLK_OE_N<br>CPSW<br>CPSW_CONTROL.RMII_REF2_CLK_SEL<br>RMII1_REF_CLK<br>RMII1_REF_CLK_IN<br>OE_N<br>CPSW_CONTROL.RMII_REF1_CLK_SEL CPSW_CONTROL.RMII_REF1_CLK_OE_N<br>RGMII_50_CLK<br>(From RCM)<br>**----- End of picture text -----**<br>


**Figure 6-3. CPSW Configuration** 

## _**6.1.3.2.5 ICSSM Global Configuration**_ 

The GLOBAL_CONTROLS register enables dynamic power saving in ICSSM*. When GLOBAL_CONTROLS.NOGATE is programmed to ‘0’, it enables auto clock gating in ICSSM* with increased access latency. When this bit is programmed to ‘1’, the clock is continuously active with low latency access. 

The GPI signals of ICSSM* can be sourced either from device pins or from PWM_XBAR . This selection can be done on a per signal basis using the registers ICSSM*_PRU*_GPI_SEL, as shown in Figure 6-4. 

When the pinmux is configured to choose ICSSM* GPIO function (PR0_PRU*_GPIO*), the control of the output buffer of the device pin can be done using the registers ICSSM*_PRU*_GPIO_OUT_CTRL, as shown in Figure 6-4. 

238 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**==> picture [499 x 182] intentionally omitted <==**

**----- Start of picture text -----**<br>
ICSSM_PRU0_GPI_SEL<br>Device Pins<br>PR0_PRU0_GPIO<br>Device Pins<br>GPO*PRU0[31:0]<br>PR0_PRU0_GPIO<br>GPI*PRU0[29:0] OE_N<br>ICSSM_PRU0_GPIO_OUT_CTRL<br>ICSSM<br>GPI*PRU1[29:0]<br>Device Pins<br>Device Pins  GPO*PRU1[31:0] PR0_PRU1_GPIO<br>PR0_PRU1_GPIO OE_N<br>ICSSM_PRU1_GPIO_OUT_CTRL<br>ICSSM_PRU1_GPI_SEL<br>PWM XBAR<br>**----- End of picture text -----**<br>


Note:  Not all GPI and GPO signals of ICSSM are available on Device spins.  Refer to device specific data sheet for the signals available on pinmux. 

**Figure 6-4. ICSSM Configuration** 

## _**6.1.3.2.6 MPU Interrupt Aggregator**_ 

The system Memory Protection Units (MPU) are present on various module ports. Each MPU can generate two kinds of error types: an address error and a protection error. Refer to the Section 3.12.3.3 for a description of these errors. 

The address errors from all MPU are aggregated and generate one interrupt R5SS*_CORE*_MPU_ADDR_ERRAGG to each R5 Core. Similarly, the protection errors from all MPU are aggregated and generate one interrupt R5SS*_CORE*_MPU_PROT_ERRAGG to each R5. 

The interrupt to each R5 can be independently configured to select the MPU sources, which should generate the above interrupts. 

The registers MPU_ADDR_ERRAGG_R5SS*_CPU*_MASK , MPU_ADDR_ERRAGG_R5SS*_CPU*_STATUS, and MPU_ADDR_ERRAGG_R5SS*_CPU*_STATUS_RAW are associated with R5SS*_CORE*_MPU_ADDR_ERRAGG interrupt to the respective R5F core. 

The register MPU_ADDR_ERRAGG_R5SS*_CPU*_MASK configures interrupt sources which can generate the ADDR_ERR interrupt to the respective R5 core. MPU_ADDR_ERRAGG_R5SS*_CPU*_STATUS register indicates the status of the source which caused the ADDR_ERR interrupt to the respective R5 Core. 

The MPU_ADDR_ERRAGG_R5SS*_CPU*_STATUS_RAW register indicates the raw status of all possible interrupt sources which can generate the ADDR_ERR interrupt. 

The registers MPU_PROT_ERRAGG_R5SS0_CPU0_MASK, MPU_PROT_ERRAGG_R5SS0_CPU0_STATUS, and MPU_PROT_ERRAGG_R5SS0_CPU0_STATUS_RAW are associated with R5SS*_CORE*_MPU_PROT_ERRAGG interrupt to the respective CPU. 

The register MPU_PROT_ERRAGG_R5SS0_CPU0_MASK configures interrupt sources, which can generate the PROT_ERR interrupt to the respective R5 core. MPU_PROT_ERRAGG_R5SS0_CPU0_STATUS register indicates the status of source which caused the PROT_ERR interrupt to the respective R5 Core. 

The MPU_PROT_ERRAGG_R5SS0_CPU0_STATUS_RAW register indicates the raw status of all possible interrupt sources which can generate the PROT_ERR interrupt. 

## _**6.1.3.2.7 MMR Access Error Interrupt Aggregator**_ 

Some of the SoC Control Modules generate MMR access error interrupts (see Section 6.1.1.2) as shown in Figure 6-5. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 239 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

All control modules' MMR access error interrupts are aggregated and generate a single interrupt MMR_ACCESS_ERRAGGR to the R5 cores. The registers MMR_ACCESS_ERRAGG_MASK0, MMR_ACCESS_ERRAGG_STATUS0, and MMR_ACCESS_ERRAGG_STATUS_RAW0 are associated with this interrupt. 

The MMR_ACCESS_ERRAGG_MASK0 register selects the sources which can generate the MMR_ACCESS_ERRAGGR interrupt. The MMR_ACCESS_ERRAGG_STATUS0 register indicates the status of interrupt sources which caused the MMR_ACCESS_ERRAGGR interrupt to occur. The MMR_ACCESS_ERRAGG_STATUS_RAW0 register indicates the raw status of all interrupt sources which can cause MMR_ACCESS_ERRAGGR interrupt to occur. 

240 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**==> picture [496 x 589] intentionally omitted <==**

**----- Start of picture text -----**<br>
TOP_CTRL MMR_ACCESS_ERR_RD<br>MMR_ACCESS_ERR_WR<br>MMR_ACCESS_ERR_RD<br>MMR_ACCESS_ERR_WR<br>MSS_CTRL<br>MSS_CTRL<br>TOP_RCM<br>MMR_ACCESS_ERR_WRMMR_ACCESS_ERR_RD<br>MMR_ACCESS_ERRAGGR<br>MMR_ACCESS_ERR_RD<br>MSS_RCM MMR_ACCESS_ERR_WR<br>HSM_CTRL MMR_ACCESS_ERR_RD<br>MMR_ACCESS_ERR_WR<br>MMR_ACCESS_ERR_RD<br>HSM_SOC_CTRL<br>MMR_ACCESS_ERR_WR<br>**----- End of picture text -----**<br>


**Figure 6-5. MMR Access Error Interrupt Aggregator** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

241 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.1.3.2.8 Safety Registers**_ 

The following sections detail the Safety Registers in the device. 

## _**6.1.3.2.8.1 R5 Memory ECC Error Aggregator**_ 

ARM R5 Cores support ECC error detection on the R5 associated memories – ICache, DCache, and TCM memories. These errors are visible on the ARM R5 Event bus EVNTBUS[*] (refer to ARM documentation for more details on the event bus interface). These errors are aggregated in the Control module and presented as two errors to ESM per R5 Core: 

- R5SS*_CORE*_CORR_ERRAGG : Correctable ECC Errors, one per R5 Core 

- R5SS*_CORE*_UNCORR_ERRAGG : Uncorrectable/Fatal ECC Errors, one per R5 Core 

242 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**==> picture [500 x 560] intentionally omitted <==**

## **Figure 6-6. R5 Memory ECC Error Event Interrupt Aggregator** 

The following registers are associated with R5SS*_CORE*_CORR_ERRAGG: 

- R5SS*_CPU*_ECC_CORR_ERRAGG_MASK – Error Mask Register 

- R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS – Error Status Register/Clear Register 

- R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS_RAW – Raw Error Status Register 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

243 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

Table 6-11 lists the register fields that control the generation of R5SS*_CORE*_CORR_ERRAGG Error. 

**Table 6-11. R5SS*_CORE*_CORR_ERRAGG Error Events** 

|**Event Flag**|**Event Mask**|**Description**|
|---|---|---|
|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[0]|R5SS*_CPU*_ECC_CORR_ERRAGG_MASK[0]|ATCM single-bit ECC<br>error. From R5 event bus<br>EVNTBUS[40]<br>Register Field name -<br>R5SS*_CPU*_ATCM_CO<br>RR_ERR|
|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[1]|R5SS*_CPU*_ECC_CORR_ERRAGG_MASK[1]|B1TCM single-bit ECC<br>error. From R5 event bus<br>EVNTBUS[42]<br>Register Field name -<br>R5SS*_CPU*_B1TCM_C<br>ORR_ERR|
|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[2]|R5SS*_CPU*_ECC_CORR_ERRAGG_MASK[2]|B0TCM single-bit ECC<br>error. From R5 event bus<br>EVNTBUS[41]<br>Register Field name -<br>R5SS*_CPU*_B0TCM_C<br>ORR_ERR|
|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[3]|R5SS*_CPU*_ECC_CORR_ERRAGG_MASK[3]|Data cache tag or dirty<br>RAM parity error or<br>correctable ECC error.<br>From R5 event bus<br>EVNTBUS[24]<br>Register Field name -<br>R5SS*_CPU*_DTAG_CO<br>RR_ERR|
|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[4]|R5SS*_CPU*_ECC_CORR_ERRAGG_MASK[4]|Data cache data RAM<br>parity error or correctable<br>ECC error.<br>From R5 event bus<br>EVNTBUS[25]<br>Register Field name -<br>R5SS*_CPU*_DDATA_CO<br>RR_ERR|
|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[5]|R5SS*_CPU*_ECC_CORR_ERRAGG_MASK[5]|Instruction cache tag RAM<br>parity or correctable ECC<br>error.<br>From R5 event bus<br>EVNTBUS[22]<br>Register Field name -<br>R5SS*_CPU*_ITAG_COR<br>R_ERR|



244 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-11. R5SS*_CORE*_CORR_ERRAGG Error Events (continued)** 

|**Event Flag**|**Event Mask**|**Description**|
|---|---|---|
|R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS[6]|R5SS*_CPU*_ECC_CORR_ERRAGG_MASK[6]|Instruction cache data<br>RAM parity or correctable<br>ECC error.<br>From R5 event bus<br>EVNTBUS[23]<br>Register Field name -<br>R5SS*_CPU*_IDATA_CO<br>RR_ERR|



The following registers are associated with R5SS*_CORE*_UNCORR_ERRAGG: 

- R5SS*_CPU*_ECC_UNCORR_ERRAGG_MASK – Error Mask Register 

- R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS – Error Status Register/Clear Register 

- R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS_RAW – Raw Error Status Register 

Table 6-12 lists the register fields that control the generation of R5SS*_CORE*_UNCORR_ERRAGG Error. 

**Table 6-12. R5SS*_CORE*_UNCORR_ERRAGG Error Events** 

|**Event Flag**|**Event Mask**|**Description**|
|---|---|---|
|R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS[0]|R5SS*_CPU*_ECC_UNCORR_ERRAGG_MASK[0]|ATCM multi-bit ECC error.<br>From R5 event bus<br>EVNTBUS[37]<br>Register Field name -<br>R5SS*_CPU*_ATCM_UN<br>CORR_ERR|
|R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS[1]|R5SS*_CPU*_ECC_UNCORR_ERRAGG_MASK[1]|B1TCM multi-bit ECC<br>error. From R5 event bus<br>EVNTBUS[39]<br>Register Field name -<br>R5SS*_CPU*_B1TCM_U<br>NCORR_ERR|
|R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS[2]|R5SS*_CPU*_ECC_UNCORR_ERRAGG_MASK[2]|B0TCM multi-bit ECC<br>error. From R5 event bus<br>EVNTBUS[38]<br>Register Field name -<br>R5SS*_CPU*_B0TCM_U<br>NCORR_ERR|
|R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS[3]|R5SS*_CPU*_ECC_UNCORR_ERRAGG_MASK[3]|Data cache tag/dirty RAM<br>fatal ECC error. From R5<br>event bus EVNTBUS[34]<br>Register Field name -<br>R5SS*_CPU*_DTAG_UN<br>CORR_ERR|
|R5SS*_CPU*_ECC_UNCORR_ERRAGG_STATUS[4]|R5SS*_CPU*_ECC_UNCORR_ERRAGG_MASK[4]|Data cache data RAM<br>fatal ECC error. From R5<br>event bus EVNTBUS[33]<br>Register Field name -<br>R5SS*_CPU*_DDATA_UN<br>CORR_ERR|



## _**6.1.3.2.8.2 R5SS TCM Address Parity Error Aggregator**_ 

The R5_CORE can generate parity bits on the TCM address. R5SS implements a parity error detection mechanism and generates an error event if parity error is detected. These errors are 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

245 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

aggregated in Control module and presented as one Error per R5_CORE to the ESM module - R5SS*_CORE*_TCM_ADDRPARITY_ERRAGG. 

**==> picture [500 x 169] intentionally omitted <==**

**Figure 6-7. R5SS TCM Address Parity Error Aggregator** 

The following registers are associated with R5SS*_CORE*_TCM_ADDRPARITY_ERRAGG: 

- R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG – Error Mask register 

- R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS - Error Status Register/Clear Register 

- R5SS*_CPU*_ECC_CORR_ERRAGG_STATUS_RAW – Raw error status register 

- ERR_PARITY_ATCM0_R5SS0 – Latched Address of Parity Error location on ATCM Memory of respective R5 Core 

- ERR_PARITY_B0TCM_R5SS0 - Latched Address of Parity Error location on B0TCM Memory of respective R5 Core 

- ERR_PARITY_B1TCM_R5SS0 - Latched Address of Parity Error location on B1TCM Memory of respective R5 Core 

- TCMx_PARITY_CTRL (x = 0, 1) - Parity Error Address clear register for respective R5SS 

Table 6-13 lists the register fields that control the generation of R5SS*_CORE*_TCM_ADDRPARITY_ERRAGG. 

**Table 6-13. R5SS*_CORE*_TCM_ADDRPARITY_ERRAGG Events** 

|**Event Flag**|**Event Mask**|**Description**|
|---|---|---|
|R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_STATU<br>S [0]|R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_MASK[<br>0]|ATCM Address Parity<br>Error.<br>Register field -<br>ATCM0_PARITY_ERR|
|R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_STATU<br>S [1]|R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_MASK[<br>1]<br>B0TCM0_PARITY_ERR|B0TCM Address Parity<br>Error.<br>Register field -<br>B0TCM0_PARITY_ERR|
|R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_STATU<br>S [2]|R5SS*_CPU*_TCM_ADDRPARITY_ERRAGG_MASK[<br>2]|B1TCM Address Parity<br>Error.<br>Register field -<br>B1TCM0_PARITY_ERR|



## _**6.1.3.2.8.3 Interconnect Safety**_ 

Various MMR are present for detecting and injecting errors into VBUS interconnects. 

- *_BUS_SAFETY_CTRL – 

   - to enable the interconnect for safety 

246 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

- 

      - to clear the error status 

   - top level idea of the available bus (cmd,wr,ws,rd) for the particular port and whether the port follows the VBUS protocol or not 

- *_BUS_SAFETY_FI – To inject fault on 

   - data bus - double error detection(ded) error 

   - data bus - single error detection(sec) error 

   - read, write, command and request bus on safe interconnect 

   - read, write, command and request bus on main interconnect 

- *_BUS_SAFETY_ERR – Error status register for sec, ded and comparison error. It also indicates if the fault injection has been do successfully done. 

- *_BUS_SAFETY_ERR_STAT_* - Comparator status register for the respective bus 

## _**6.1.3.2.9 MSS_CTRL MMR Kick Protection Registers**_ 

The MSS_CTRL memory space is protected for writes using the kick registers as discussed in MMR Write Protection. 

## _**6.1.3.2.10 MSS_CTRL MMR Access Error Registers**_ 

The MSS_CTRL module can generate an Access Error interrupt which is associated with the following registers. 

- INTR_RAW_STATUS - Interrupt Raw Status/Set register 

- INTR_ENABLED_STATUS_CLEAR - Interrupt Enabled Status/Clear register 

- INTR_ENABLE - Interrupt Enable register 

- INTR_ENABLE_CLEAR - Interrupt Enable Clear register 

See Section MMR Access Error Interrupt for details. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 247 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.1.4 CONTROLSS_CTRL (CTRLMMR2)**_ 

This module consists of registers associated with the following functions: 

- Peripheral clock gating - Writing 3’b111 will gate the clock for the corresponding peripheral. Programmed as multibit. 

- Peripheral reset - Writing 3’b111 will generate the reset for the corresponding peripheral. Programmed as multibit. 

- Peripheral Halt 

   - Peripheral Halt disabled with corresponding CPU halt when programmed to 0 

   - Peripheral Halt enabled with corresponding CPU halt when programmed to 1 

248 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.1.5 IOMUX (PADCFG_CTRLMMR0)**_ 

SoC-level terminal configuration control registers 

Every device pinmux I/O pad is associated with a configuration MMR register <PAD_NAME>_CFG_REG. Table 6-14 describes each of these I/O pad configuration register fields. 

**Table 6-14. I/O Pad Configuration Register Fields** 

|**Register Field**|**Description**|
|---|---|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_func_sel|For selecting the input for the peripheral to pad mux or output of the<br>pad to peripheral demux|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_ie_override_ctrl|Active Low Input Override Control : Write 1 to select Active low<br>Input Override value to control IOs IE_N/RXACTIVE_N instead of<br>the control from hardware|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_ie_override|Active Low Input Override|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_oe_override_ctrl|Active Low Output Override Control : Write 1 to select Active low<br>Output Override value to control IOs OE_N/GZ instead of the control<br>from hardware|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_oe_override|Active Low Output Override|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_pupdsel|Pullup/PullDown Selection 0 -- Pull Down 1 - Pull Up|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_pi|Pull Inhibit/Pull Disable 0 -- Enable 1- Disable|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_sc1|Slew rate control : 0 : higher slew rate. 1: Lower slew rate.|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_gpio_sel|R5F CPU ownership select for GPIO. 0 : GPO0, 1 :GPO1, 2 : GPO2,<br>3:GPO3|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_qual_sel|select value for choosing input qualifier type for PAD. 00 : Sync, 01 :<br>3 Sample qual 10 : 6 Samples qual 11 : Async|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_inp_inv_sel|select value for choosing inverted version of PAD input for chip: 0 :<br>Non Inverted 1 : Inverted|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_hsmode|MMR bits for HSMODE pin in case of true I2C pads|
|MSS_IOMUX..<PAD_NAME>_CFG_REG_hsmaster|MMR bits for HSMASTER pin in case of true I2C pads|
|MSS_IOMUX_QUAL_GRP_*_CFG_REG_qual_period_per_sample|MMR bits for programming the qualifier clock count per sample|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

249 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.1.6 TOPRCM (RCM_CTRLMMR0): SoC-level Clock and Reset control registers**_ 

The below Table 6-15 describes the SoC Level clock and Reset Control Registers. Refer to Section 6.3.2.2 for more information on Warm Reset. 

**Table 6-15. SoC Level Reset Registers** 

|**Control/Status Register**|**Description**|
|---|---|
|TOP_RCM.WARM_RESET_CONFIG|Enable/disable individual warm reset sources|
|TOP_RCM.WARM_RESET_REQ|SW warm reset request|
|TOP_RCM.WARM_RST_CAUSE_CLR|Clear request for registered warm reset cause|
|TOP_RCM.WARM_RSTTIME1|When warm reset is triggered by internal warm reset sources, the time for which the<br>warm reset pad pin has to be asserted low.|
|TOP_RCM.WARM_RSTTIME2|When warm reset is de-asserted externally, the time delay after which the external<br>warm reset is de-asserted.|
|TOP_RCM.WARM_RSTTIME3|When warm reset is asserted externally, the time delay after which the external warm<br>reset is asserted.|
|TOP_RCM.WARM_RST_CAUSE|Status register capturing which warm reset source caused the warm reset|



The below Table 6-16 refers to the programmable values for WARM_RSTTIME1/2/3 that correspond to delays in the design. 

**Table 6-16. WARM_RSTTIMEx Programmable Delay Values** 

|**Programmable Value**|**Delay Value**|
|---|---|
|0|500ns|
|1|1μs|
|2|2μs|
|3|4μs|
|4|8μs|
|5|16μs|
|6|32μs|
|7|64μs|
|8|128μs|
|9|256μs|
|10|512μs|
|11|1.024ms|
|12|2.048ms|
|13|4.096ms|
|14|8.192ms|
|15|16.384ms|



**Table 6-17. SoC Level Clock Registers** 

|**Control/Status Register**|**Description**|
|---|---|
|TOP_RCM.x_CLK_SRC_SEL|Select line for selecting source clock for corresponding IP. Data should be loaded as<br>multibit|
|TOP_RCM.x_CLK_DIV_VAL|Divider value for corresponding selected clock. Data should be loaded as multibit.|
|TOP_RCM.x_CLK_GATE|For gating the corresponding clock. writing '111' will gate clock for the IP|
|TOP_RCM.x_CLK_STATUS_clkinuse|Status shows the source clock selected for the corresponding clock|



250 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **Table 6-17. SoC Level Clock Registers (continued)** 

|**Control/Status Register**|**Description**|
|---|---|
|TOP_RCM.x_CLK_STATUS_currdivider|Status shows the current divider value chosen for the corresponding clock|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

251 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.1.7 MSS_RCM (RCM_CTRLMMR1): SoC and Peripheral-level Clock and Reset control registers**_ 

The below describes the SoC and Peripheral Clock and Reset Control Registers 

**Table 6-18. SoC and Peripheral Reset Registers** 

|**Control/Status Registers**|**Description**|
|---|---|
|MSS_RCM.R5SSx_DBG_RST_EN|Controls enable/disable of debug reset request to reset CORE0 and CORE1|
|MSS_RCM.R5SSx_RST_ASSERDLY|Controls the number of cycles reset should be kept asserted for R5SS resets.|
|MSS_RCM.R5SSx_RST2ASSERTDLY|Controls the number of cycles reset should be to wait before asserting R5SS resets.|
|MSS_RCM.R5SSx_RST_WFICHECK|Enable/disables if WFI is required before asserting R5SS resets.|
|MSS_RCM.R5SSx_RST_CAUSE_CLR|Clear the reset cause register|
|MSS_RCM.<IP>_RST_CTRL|Controls the individual IP reset generation|
|MSS_RCM.R5SSx_RST_STATUS|Status register capturing which event caused the corresponding R5SS reset|



**Table 6-19. SoC and Preipheral Clock Registers** 

|**Control/Status Registers**|**Description**|
|---|---|
|MSS_RCM.x_CLK_SRC_SEL|Select line for selecting source clock for corresponding IP. Data should be loaded as<br>multibit|
|MSS_RCM.x_CLK_DIV_VAL|Divider value for corresponding selected clock. Data should be loaded as multibit.|
|MSS_RCM.x_CLK_GATE|For gating the corresponding clock. Writing '111' will gate clock for the IP|
|MSS_RCM.x_CLK_STATUS_clkinuse|Status shows the source clock selected for the corresponding clock|
|MSS_RCM.x_CLK_STATUS_currdivider|Status shows the current divider value chosen for the corresponding clock|



## **Note** 

[x] in MSS_RCM.x refers to various MSS peripherals. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

252 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **6.2 Power** 

This chapter describes the power-management architecture implemented in the device. 

The Power Management content is presented in several general sections: 

- Power Management Overview 

- Power Management Unit 

- Power Control Modules 

- Device Power States 

## _**6.2.1 Power Management Overview**_ 

The AM263Px Power Management System contains a Power Management Unit (PMU), which includes reference voltage generators, power rail monitors that can trigger a device reset, and a threshold based temperature monitor. The AM263Px also contains an internal BIAS LDO, which generates a 1.8-V output on the VDDS18_LDO pin, which should be externally connected to VDDS18 for IO Bias. 

Figure 6-8 shows the different power supply domains in the AM263Px . The AM263Px has the following power domains, some of which must be externally supplied and some of which are internally generated by LDO modules in the device. 

- **3.3-V IO and analog Supply** : The 3.3-V supply must be provided externally to the VDDS33 and VDDA33 pins and is used for analog logic and IOs. 

- **1.2-V Core Supply** : The 1.2-V core supply must be provided externally to the VDD and VDDR1/2/3 pins and is used for Digital logic and SRAMs. 

- **1.8-V IO BIAS Supply** : The 1.8-V IO Bias supply, VDDS18, is generated internally by the BIAS LDO from the 3.3-V Supply and connect to the VDDS18_LDO pin which can to be connected to VDDS18 on the board. The supply is used for IO Bias. 

- **1.8-V Analog Supply** : The 1.8-V Analog Supply, VDDA18, is generated internally and connected to the VDDA18_LDO pin which can be connected to VDDA18 and VDDA18_OSC_PLL (1.8V Analog Supply for PLL) on the board. The supply powers the analog logic and PLL. 

   - The 1.8V Analog Supply can be re-programmed to 1.7V to use for VPP programming. See Section 6.2.1.1 for more information. 

- **VPP 1.7-V Supply** : The 1.7-V VPP supply must be provided externally when programming the Fusible ROM (FROM) present in the device. When the FROM is not being programmed the 1.7-V supply may be disabled or disconnected from the device . 

## **Figure 6-8. AM263Px Power Supply Overview** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

253 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**==> picture [471 x 521] intentionally omitted <==**

**----- Start of picture text -----**<br>
1.2V (2A) CORE Supply VDD Logic AM263Px<br>SRAM<br>VDDAR1,2,3<br>VDD<br>CQDET<br>VDD<br>3.3V (400mA) IO &Analog Supply<br>VDDS33<br>HHV<br>IO<br>VDDS18_LDO<br>BIAS LDO<br>1.8V IO BIAS<br>SUPPLY<br>VDDS18<br>FILTER<br>VDD<br>VDDA33<br>FILTER PMU SAFETY<br>SUBSYS<br>VDD<br>VDDA18_LDO PMU REF<br>SUBSYS<br>1.8V ANALOG<br>VDDA18<br>FILTER<br>VDD<br>HHV<br>PLL/HSDIV SYSRESET<br>VDD<br>VDDA18_OSC_PLL<br>FILTER XTAL IO<br>VDDS18<br>PORz (3.3V) HHV HHV<br>Supervisor (High Heating<br>Value)<br>1.8V IO<br>VDD<br>HHV<br>VPP 1.7V (few mA) VPP FROM<br>**----- End of picture text -----**<br>


As a power saving option, the AM263Px supports clock gating for all the peripherals as well as including a power down feature for On-Chip Static Random Access Memory (OCSRAM) banks. Details of IP clock gating can be found in Section 6.2.3.1 and the power down mode of OCSRAM is explained in Section 6.2.3.2. 

## **6.2.1.1 Using the Device Analog LDO for VPP Supply** 

The device includes functionality to use the internal 1.8V Analog Supply as the source for the VPP 1.7V Supply. This feature eliminates the need for an external LDO connection to VPP in order to perform eFuse programming 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

254 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

on the device. By taking advantage of this added functionality, system BOM costs can be reduced by eliminating the external 1.7V VPP source LDO from a design. 

In order to use the 1.8V Analog Supply as the VPP source, any factory programming sequence that requires the one-time programmable eFuse necessitates a minor modification to account for the VPP power requirements. First, the VPP_EN bit in the VPP_EN_MMR register needs to be set to 1. To correctly program the eFuse, VPP requires a 1.7V supply. The default output of the 1.8V Analog Supply must be re-programmed to output 1.7V. The flow of this process is as follows: 

1. Lower the internal 1.8V Analog LDO supply to 1.7V before programming the eFuse 

2. Program eFuse 

3. Raise the internal Analog LDO supply back to the default of 1.8V 

## **Note** 

Step 3 above is critical, as the device will not function properly if this step is not performed. 

To enter eFuse programming and set the internal 1.8V Analog supply to 1.7V (all registers are under TOP_CTRL): 

1. Read the TRIM_OFFSET from EFUSE_OVERRIDE_LDO_TRIM. 

2. Assert the Mask for the Ana ISO SOC reset in the MASK_ANA_ISO register by setting the MASK field to 3b111. This prevents the lowering of the LDO voltage from triggering any systems resets. 

3. Program the LDO_PROG field of the EFUSE_OVERRIDE_LDO_TRIM register to 4b1110. 

4. Program the TRIM_OFFSET field of the EFUSE_OVERRIDE_LDO_TRIM register to the value obtained in step 1. 

5. Enable the override by setting the OVERRIDE field of the EFUSE_OVERRIDE_LDO_TRIM register to 3b111. 

6. Wait for the supply voltage to stabilize. 1 millisecond is the recommended delay interval. 

7. Program eFuse and verify. 

To exit eFuse programming and restore the internal Analog LDO supply back to 1.8V (all registers are under TOP_CTRL): 

1. Disable the override by clearing all bits of the OVERRIDE field of the EFUSE_OVERRIDE_LDO_TRIM register. 

2. Wait for the supply voltage to stabilize. 1 millisecond is the recommended delay interval. 

3. The internal Analog LDO supply will now be back to normal operation at 1.8V. 

4. De-assert the Mask for the Ana ISO SOC reset by clearing all the bits of the MASK field in the MASK_ANA_ISO register. 

5. Exit the eFuse programming routine. 

## _**6.2.2 Power Management Unit**_ 

The Power Management Unit in AM263Px consists of a Reference system and a Safety system. 

- **Reference System:** 

The Reference system generates internally used power supply and reference rails. It ensures reliable power on sequencing with the PMU and generates a reset signal based on coarse voltage level checks given to the external power supplies. The Reference system also contains the 1.8V LDO which generates a 1.8V output on the VDDA18_LDO pin. The 1.8V on VDDA18_LDO can be connected to VDDA18 and VDDA18_OSC_PLL on the board to provide the 1.8V supply to the Analog Circuit and PLL. This connection has to be done external to the device as there is no internal connection path for VDDA18_LDO to source either VDDA18 or VDDA_OSC_PLL. 

Using the 1.8V LDO as the VDDA18 source allows the 1.8V LDO to source multiple internal blocks. These blocks include the internal ADC voltage reference buffers as well as other analog loads. Because the ADC 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 255 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

reference buffers are sourced internally through the VDDA18 input, the VDDA18_LDO output should not be connected as source for the ADC VREFHI inputs. 

- **Safety System:** 

The Safety System contains the safety comparators and temperature sensor to monitor the system supplies and temperature. The glitch filtered output of the voltage monitors is connected to the Error Signaling Module (ESM) and provide an error signal if the supply is not within the voltage thresholds set for the individual monitored supplies. 

## **6.2.2.1 PMU Reference System (REFSYS)** 

The PMU Reference System consists of the following: 

- Bandgap (BGAP) and BGAP coarse level checker 

- LDO and LDO coarse lever checker 

- Supply (VDDA18 and VDD) coarse level checker 

- Power on Sequencer and reset generation circuit 

- Level Shifters 

The REFSYS generates a reset based on PORz and the stability of external voltage rails and provide outputs in three supply domains, VDD, VDDA18, and VDDA33, which are used in different domain logic. 

The power up sequence is shown in Power Up Sequence and details for the sequence from the PMU REFSYS reset are shown below: 

1. The device needs to be supplied with 3.3V (VDDS33/VDDA33) and 1.2V (VDD/VDDARx) supplies externally. As the external power supplies ramps up, PORz needs to be asserted low externally until the supplies are stable to hold the SOC in a reset state. 

2. The device can rely on an external supervisor to verify that the device external supplies (3.3V, 1.2V) are valid before releasing the reset to the device (PORz de-asserted). An inverted signal HHV (High Heating Value) is generated internally from PORz to enable isolation logic during power up for the IOs and PLL logic. 

3. When the PORz is de-asserted, i.e PORz transitions from low to High, the PMU starts the power-up sequence by enabling the Bandgap (BGAP) Voltage and Current reference voltage generators. 

4. While the reference voltages are settling, BGAP voltage is monitored by a coarse level checker and the BGAP ready signal is generated when the voltage stabilizes. This signal enables LDO and supply coarse checkers inside the reference system. 

5. Once the VDD and VDDA18 supplies are deemed ready, the internal signal VDD_OK is asserted. This releases the reset going to SOC. 

6. A rising edge on VDD_OK enables the RC Oscillator (provides the 10MHz RCCLK) and the crystal clock (XTALCLK). 

   - a. Reset and clock control module checks the presence of RCCLK for 16 clock cycle before enabling RCCLK to rest of the SOC. 

   - b. To verify the stability of XTALCLK, a 2ms counter using RCCLK is enabled. Once XTALCLK is stabilized, internal reset to CPU is released. 

7. After the RCCLK has been enabled to the rest of the system and XTALCLK is stabilized, eFuse data is read and trim values are applied to the analog domain. The internal signal _hhv_mask_ is asserted to gate the influence of comparator checks and prevent the SOC from going into reset due to changing trim values. Once the trim is completed, _hhv_mask_ is de-asserted. 

   - a. The externally applied PORz is not affected by the _hhv_mask_ signal and if PORz is asserted during trim, the device goes back to reset state. 

The trim values provided in the eFuse chain are enabled by a PORz de-assertion. The status of coarse monitors on supplies VDDA18, VDD12, 1.8V LDO, and BGAP can be monitored through TOP_CTRL.PMU_COARSE_STAT register during run time. 

256 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**==> picture [370 x 411] intentionally omitted <==**

**Figure 6-9. AM263Px Power Up Sequence** 

## **6.2.2.2 PMU Safety System (SAFETYSYS)** 

The PMU Safety System consists of a Power OK system which contains comparators to monitor supply voltages and a Thermal Manager which monitors the system temperature. 

## _**6.2.2.2.1 Power OK (POK) Modules**_ 

POK modules are responsible for accurately detecting the voltage levels. Each module is trimmed to account for process and temperature variations. The trim values are provided by eFuse chains enabled by a POR module. 

The table below shows the different voltage monitors available. Enabling/Disabling of this monitors can be controlled by the TOP_CTRL.VMON_CTRL and TOP_CTRL.ADC_REF_COMP_CTRL registers. There are corresponding status bits available in TOP_CTRL.VMON_STAT and TOP_CTRL:ADC_REF_GOOD_STATUS. The output of voltage monitors are filtered using a configurable digital glitch filter module. The configuration of the glitch filter can be done using the TOP_CTRL.VMON_FILTER_CTRL.SELECT_VALUE register to select from no filtering to a maximum of 14.4μs filtering of voltage monitor signals. The output of the voltage monitors are aggregated and the aggregated output is forwarded to the ESM. Individual mask bits in TOP_CTRL.MASK_VMON_ERROR_ESM_L and TOP_CTRL.MASK_VMON_ERROR_ESM_H can be used to MASK the corresponding monitor to trigger ESM event. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 257 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

The POK bit is set to 1 when the voltage supply is within range and to 0 when out of range. See the device data sheet for POK tolerance details. The ESM event is generated only when POK signals are out of range. 

**==> picture [238 x 153] intentionally omitted <==**

**Figure 6-10. Voltage Comparator subsystem** 

**Table 6-20. POK Module overview** 

|**Voltage Monitored**|**Comparator block**|**UV/OV**(1)|**Description**|
|---|---|---|---|
|VDDA18|C0|UV|Voltage monitor for 1.8-V LDO<br>output using 3.3-V as reference|
|VDDA18|C2|UV/OV|Voltage monitor for 1.8-V LDO<br>output using BGAP as reference|
|VBGAP09|C1|UV/OV|Voltage monitor for 0.9-V<br>bandgap.|
|VDD12|C3|UV/OV|Voltage monitor for 1.2-V I/O<br>supply|
|VDDSBIO|C5|UV/OV|Voltage monitor for 1.8-V IO bias<br>supply|
|VSYS_MON|C7|UV|Voltage monitor for external<br>VSYS_MON|
|VDDA33|C8|UV|Voltage monitor for 3.3-V I/O<br>supply|
|ADC0_REF|C4|UV/OV|Voltage monitor for ADC0_REF|
|ADC12_REF|C9|UV/OV|Voltage monitor for ADC12_REF|
|ADC34_REF|C6|UV/OV|Voltage monitor for ADC34_REF|



258 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **Note** 

In summary, there are three different systems that monitor the supplies of the device, 

1. External reset generation circuits 

2. Internal reset generation circuits (PMU_REFSYS) 

3. Safety system (PMU_SAFETY) 

See below table for a list of the supplies and where they are monitored: 

**Table 6-21. Power supply list and monitoring systems** 

|**Supply**|**External Reset**|**Internal Reset**|**Safety System**|
|---|---|---|---|
|VDDA33|Y|N|Y|
|VDDA18|N|Y|Y|
|VBGAP09|N|Y|Y|
|VDD12|Y|Y|Y|
|VDDSBIO|N|N|Y|
|VOUT_LDO*|N|Y*|N|
|VSYS_MON|Y|N|Y|
|ADC0_REF, ADC12_REF|N|N|Y|
|ADC34_REF|N|N|Y|



*:LDO output has monitoring in addition to the monitoring on VDDA18. 

## _**6.2.2.2.2 Thermal Manager**_ 

This section describes the Thermal Manager (TM) module in the device. 

The TM module on the device enables thermal management of the device by providing control of on-chip temperature sensors. 

The device has two temperature sensors (TSENSE0 and TSENSE1), each located near critical hotspots in the device die. There are two additional temperature sensors (TSENSE2, TSENSE3) at other locations in the device die. 

Active temperature monitoring is available for two temperature sensors (TSENSE0 and TSENSE1) near the hotspots. The other two temperature sensors (TSENSE2, TSENSE3) are only for temperature readout. 

## **Note** 

TSENSE0, TSENSE1, TSENSE2 are CTAT (Complementary To Absolute Temperature) sensors, while TSENSE3 is a PTAT (Proportional To Absolute Temperature) sensor. TSENSE3 is meant for internal use only. For the most accurate junction temperature readings, TSENSE0 and TSENSE 1 should be used. 

## _**6.2.2.2.2.1 Thermal Manager Features**_ 

The Thermal Manager (TM) module supports the following features: 

- Programming of temperature-crossing thresholds 

- Signals when programed thresholds are exceeded (up to 3 alerts): 

   - Temperature exceeding the TSENSE*_ALERT.ALERT_THRHLD_HOT for ALERT_HOT_INTR. 

   - Temperature exceeding the TSENSE*_ALERT.ALERT_THRHLD_COLD for ALERT_LOW_THLD_BREACH_INTR. 

   - Temperature below the TSENSE*_ALERT.ALERT_THRHLD_COLD for ALERT_HOT_INTR 

- Supports up to 4 temperature monitors. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

259 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

- Allows resolution of 2°C for temperature reading and threshold point temperature alert/interrupt generation. 

- • Maximum temperature alert. 

- Supports one shot sampling mode for the sensors. 

- Temp sense controller loops cyclically through each sensor and generates the results. Each sensor can be enabled/disabled independently. 

- Provides register control and status for all 4 sensors. Interrupt generation, FIFO registers and alerts for 2 SOC temperature monitors (TSENSE0 and TSENSE1). 

- Default threshold are controlled through efuse values. This can be also controlled through programmable registers. 

- There are four FIFOs used to store a brief history for the last few temperature measurements and are also dedicated to temperature time-stamping feature. 

- Accumulator register for cumulative sum of past temperature measurements on 2 SOC temperature monitors (TSENSE0 and TSENSE1). 

- Warm reset generation when SOC temperature monitors exceed TSHUT_HOT. 

## _**6.2.2.2.2.2 Thermal Manager Functional Description**_ 

There are four temperature sensors on the device die. Each sensor is associated with one voltage domain and is also a part of a VBGAPTS cell. The VBGAPTS cell integrates bandgap voltage reference, temperature sensor with ADC and thermal comparator shutdown. The 7-bit ADC produces a digital output, respective to the temperature measured on the SoC (PTAT or CTAT). Figure 6-11 shows the Thermal Management Functional Block Diagram. 

**==> picture [439 x 291] intentionally omitted <==**

**Figure 6-11. Thermal Management Functional Block Diagram** 

## _**6.2.2.2.2.3 Thermal FSM**_ 

The Thermal FSM is clocked by the 32KHz clock. At reset the FSM is not enabled and can be enabled by configuring the TOP_CTRL.TSENSE_CFG register. 

Software needs to configure the below register bits to enable the Temperature Sensor: 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

260 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

- TOP_CTRL.TSENSE_CFG.TMPSOFF – Temperature Sensor Controller OFF 

- TOP_CTRL.TSENSE_CFG.BGROFF – Bandgap Reference OFF 

- TOP_CTRL.TSENSE_CFG.AIPOFF - Temperature Sensor IP OFF 

- TOP_CTRL.TSENSE_CFG.SNSR_MX_HIZ – Sensor mux select high impedance 

By default these bits are set to 1, which disables the temperature sensor. To enable the temperature sensor these bits should be cleared (set to 0). Once the sensor is enabled, temperature measurement is initiated by enabling the FSM by writing 1 to TOP_CTRL.TSENSE_CFG.ENABLE. 

Once enabled, the FSM will read out the temperature values from the sensors in a round robin fashion based on TOP_CTRL.TSENSE_CFG.SENSOR_SEL bitfield value. TOP_CTRL.TSENSE_CFG.SENSOR_SEL controls the enabling/disabling of individual sensors. 

For each selected sensor, FSM requires anywhere between 51 to 54 clock cycles to start the sequence and register the result into TOP_CTRL.TSENSE*_RESULT.DTEMP register. TOP_CTRL.TSENSE_CFG.DELAY configures the number of clock cycles between end of result captured to FSM starting the sequence for the next enabled sensor. When the conversion is ongoing for a particular sensor, the corresponding TOP_CTRL.TSENSE*_RESULT.EOCZ status bits are set to 1. The EOCZ bit is reset to 0 again when the conversion completes. After this the valid temperature is written automatically by FSM in the TOP_CTRL.TSENSE*_RESULT.DTEMP bit fields, and then software is able to read it from the corresponding register. Figure 6-12 describes the sequence of sensor measurement based on SENSOR_SEL bits. 

## **Note** 

Value 0 in TOP_CTRL.TSENSE_CFG.DELAY is not valid. A non-zero value should be programmed to this register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

261 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**==> picture [290 x 111] intentionally omitted <==**

**----- Start of picture text -----**<br>
S0 disabled<br>S1 disabled<br>S1 enabled S2 enabled S3 enabled S0 enabled<br>S0 S1 S2 S3<br>S2 disabled<br>S3 disabled<br>**----- End of picture text -----**<br>


**Figure 6-12. Sensor flow diagram** 

## _**6.2.2.2.2.4 Thermal Alert Comparator**_ 

Thermal Comparators are implemented on the Temperature readouts to generate warm reset, interrupts or ESM Errors. Alert indication generated by controller is shown in Figure 6-11. 

## **Warm Reset Generation:** 

TSHUT_HOT and TSHUT_COLD comparators are used to generate a warm reset. Internal signal TSHUT is set high when temperature is greater than TSHUT_THRHLD_HOT and TSHUT is set low when temperature is less than TSHUT_THRHLD_COLD. TSHUT_ THRHLD _HOT and TSHUT_ THRHLD _COLD is taken from the efuse programmed value. They may also be overridden by writing TOP_CTRL.TSENSE*_TSHUT.EFUSE_OVERRIDE register with 0x7 and TSHUT_ THRHLD _HOT and TSHUT_ THRHLD _COLD values in TOP_CTRL.TSENSE*_TSHUT.TSHUT_THRHLD_HOT and TOP_CTRL.TSENSE*_TSHUT. TSHUT_THRHLD_COLD respectively. 

An inverted version of TSHUT is connected to warm reset. The warm reset enable for it is controlled through TOP_RCM.WARM_RESET_CONFIG.TSENSE*_RST_EN. 

## **Operation With Interrupts:** 

In this mode ALERT_HOT_INTR is used for indicating the hot and subsequent cooldown condition. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

262 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

In this mode TOP_CTRL.TSENSE*_CNTL.MASK_COLD should be set to 1 and TOP_CTRL.TSENSE*_CNTL.MASK_HOT should be set to 0 to start with. This will enable the interrupt for hot condition. 

When the temperature exceeds the TOP_CTRL.TSENSE*_ALERT.ALERT_THRHLD_HOT register value, it triggers the ALERT_HOT_INTR interrupt. The interrupt will be asserted until masked by setting TOP_CTRL.TSENSE*_CNTL.MASK_HOT to 1. This will dessert the interrupt. 

Software should additionally unmask the cold interrupt condition by setting register bit TOP_CTRL.TSENSE*_CNTL.MASK_COLD to 0. When the temperature cools down below the TOP_CTRL.TSENSE*_ALERT.ALERT_THRHLD_COLD register value, the interrupt ALERT_HOT_INTR is again triggered to indicate to the software that the device has cooled off sufficiently 

The masked interrupt signals are also routed to the TOP_CTRL.TSENSE_STATUS register and the non-masked (raw) comparator outputs are available for reading through the corresponding bits in the TOP_CTRL.TSENSE_STATUS_RAW register. 

## _**6.2.2.2.2.5 Thermal Shutdown Comparators**_ 

There is also a comparator block responsible for the thermal shutdown (TSHUT) function of the thermal management logic. This comparator block is also composed of two comparators. One dedicated to COLD TSHUT threshold and the other one to high TSHUT threshold. 

The comparator outputs for the high TSHUT thresholds of each sensor are ORed and used to generate a single EVNT_TSENSE_CRITICAL error signal to ESM.The comparator outputs for the high and low TSHUT thresholds are used to generate TSHUT_RST0 pulse signal which asserts when high TSHUT is active and deasserts when low TSHUT is active. TSHUT_RST* signasl from both sensors are routed as warm reset source to reset the chip. 

The TSHUT_HOT and TSHUT_COLD threshold values are by default controlled from EFUSE. TOP_CTRL.TSENSE*_TSHUT registers can be used to override the value from EFUSE and apply the same from the bit fields of TOP_CTRL.TSENSE*_TSHUT registers. 

## _**6.2.2.2.2.6 Temperature Timestamp Registers**_ 

Each time one of the TOP_CTRL.TSENSE*_RESULT.DTEMP bit fields is updated with new temperature value, this value is also automatically stored into a 4-level deep FIFO and a timestamp is registered too. There are four FIFOs used to store a brief history for the last few temperature measurements and are also dedicated to temperature timestamping feature. Each FIFO has two fields. 

The first one is 8 bits wide, 4 levels deep, and is intended to store the temperature values for the last four measurements. The second field is 24 bits wide, 4 levels deep, and acts like a counter for the number of temperature measurements. Each FIFO is composed of the following registers (supported for TSENSE0 and TSENSE1): 

- TOP_CTRL.TSENSE*_DATA0 

- TOP_CTRL.TSENSE*_DATA1 

- TOP_CTRL.TSENSE*_DATA2 

- • TOP_CTRL.TSENSE*_DATA3 

## _**6.2.2.2.2.7 FIFO Management**_ 

Software can stop a certain FIFO to update TOP_CTRL.TSENSE*_DATA1, TOP_CTRL.TSENSE*_DATA2, and TOP_CTRL.TSENSE*_DATA3 with new temperature and timestamp values by setting one of the FREEZE bits in the TOP_CTRL.TSENSE0_CNTL and TOP_CTRL.TSENSE1_CNTL registers to 1. These FIFO_FREEZE bits are automatically cleared by hardware after the FIFOs are cleared. 

Each FIFO is cleared by setting to 1 one of the FIFO_CLEAR bits in the TOP_CTRL.TSENSE0_CNTL and TOP_CTRL.TSENSE1_CNTL registers. These FIFO_CLEAR bits are also automatically set by hardware to 0 after the FIFOs clearing procedure completes. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 263 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

Additionally TOP_CTRL.TSENSE0_ACCU and TOP_CTRL.TSENSE1_ACCU registers store the accumulated temperature values. This are cleared by setting one of the ACCU_CLEAR bits to 1 in the TOP_CTRL.TSENSE0_CNTL and TOP_CTRL.TSENSE1_CNTL registers. 

## _**6.2.2.2.2.8 ADC Values Versus Temperature**_ 

Table 6-22 provides all the valid ADC values which correspond to the temperature measured which is read from the TOP_CTRL.TSENSE*_DATA*.DATA, TOP_CTRL.TSENSE*_RESULT.DTEMP bit fields. The table also provides the values for the temperature thresholds which are configurable through the TOP_CTRL.TSENSE*_ALERT.ALERT_THRHLD_COLD, TOP_CTRL.TSENSE*_ALERT.ALERT_THRHLD_HOT, TOP_CTRL.TSENSE*_TSHUT.TSHUT_THRHLD_COLD & TOP_CTRL.TSENSE*_TSHUT.TSHUT_THRHLD_HOT bit fields. 

## **Note** 

Table 6-22 is meant for use with the device CTAT sensors - TSENSE[0:2]. TSENSE3 is a PTAT sensor, and the below table does not apply to TSENSE3. TSENSE3 is meant for internal use only, and does not have an equivalent conversion table. For the most accurate junction temperature readings, TSENSE0 and TSENSE1 should be used. 

**Table 6-22. ADC Values Versus Temperature** 

|**ADC code**|**Temperature**|**ADC code**|**Temperature**|**ADC code**|**Temperature**|
|---|---|---|---|---|---|
|0-24|150|56|86|88|22|
|25|148|57|84|89|20|
|26|146|58|82|90|18|
|27|144|59|80|91|16|
|28|142|60|78|92|14|
|29|140|61|76|93|12|
|30|138|62|74|94|10|
|31|136|63|72|95|8|
|32|134|64|70|96|6|
|33|132|65|68|97|4|
|34|130|66|66|98|2|
|35|128|67|64|99|0|
|36|126|68|62|100|-2|
|37|124|69|60|101|-4|
|38|122|70|58|102|-6|
|39|120|71|56|103|-8|
|40|118|72|54|104|-10|
|41|116|73|52|105|-12|
|42|114|74|50|106|-14|
|43|112|75|48|107|-16|
|44|110|76|46|108|-18|
|45|108|77|44|109|-20|
|46|106|78|42|110|-22|
|47|104|79|40|111|-24|
|48|102|80|38|112|-26|
|49|100|81|36|113|-28|
|50|98|82|34|114|-30|
|51|96|83|32|115|-32|



264 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-22. ADC Values Versus Temperature (continued)** 

|**ADC code**|**Temperature**|**ADC code**|**Temperature**|**ADC code**|**Temperature**|
|---|---|---|---|---|---|
|52|94|84|30|116|-34|
|53|92|85|28|117|-36|
|54|90|86|26|118|-38|
|55|88|87|24|119-128|-40|



## **Note** 

Based on the characterization data, the Temperature mentioned in table can be offset by +/- 8 degree C. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

265 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.2.3 Power Control Modules**_ 

The Power Control Modules are divided into two sections dependent on their functionality: the Clock ICG control section and the L2OCRAM power control section. 

## **6.2.3.1 Clock ICG controls** 

Clock ICG control manages the clock to each of the IPs using software control. For each module, there is a dedicated register <IP>_CLK_GATE part of MSS_RCM register space. By default all module clocks are enabled. Writing 0x7 into field GATED of corresponding <IP>_CLK_GATE will disable the clock to the IP. 

Additionally, TOP_RCM host clock gating register R5SS0_CLK_GATE and R5SS1_CLK_GATE to disable core clock to individual R5SS. SYS_CLK_GATE disable SYS_CLK to the whole system. It is not recommended to gate R5SS_CLK and SYS_CLK as the system will hang and only option is to reset the whole system. TOP_RCM also allows clock gating for TRACE_CLK and CLKOUT0/CLKOUT1 ports. 

## **6.2.3.2 L2OCRAM Power Control** 

There are 6 memory banks each of 512KB available as L2OCRAM. 

By default all of this banks are in Power ON. 

Individual L2OCRAM banks can be powered OFF using software writes to MSS_RCM.L2OCRAM_BANK*_PD_CTRL register and by observing status bits from MSS_RCM.L2OCRAM_BANK*_PD_STATUS 

Sequence to power off each bank is captured below 

1. Write 0x7 to ISO field of the register. 

2. Write 0x0 to AONIN field of the register. 

3. Wait till AONOUT status field is 0x0. 

4. Write 0x0 to AGOODIN field of the register. 

5. Wait till AGOODOUT status field is 0x0. 

Sequence to Power On each bank is capture below 

1. Write 0x7 to AONIN field of the register. 

2. Wait till AONOUT status field is 0x1. 

3. Write 0x7 to AGOODIN field of the register. 

4. Wait till AGOODOUT field is 0x1. 

5. Write 0x0 to ISO field of the register. 

When a block is powered off, a bus error is generated on access. 

## **Note** 

It is always safe to have decent delay between each step because memory might take some time before reaching to total power on state. So even though aonout is 1’b1 does not mean memory is ON. 

266 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.2.4 Device Power States**_ 

## **6.2.4.1 Overview of Device Power Modes** 

The device does not support low power mode, where the device can be controlled to reduce power consumption when the processors and peripherals are not active. Lower power consumption comes at the cost of longer time for recovery to a running mode. 

Power states in the system can be defined in terms of controlled power consumption: 

- **ACTIVE State** : This is an initial state after the device is powered on. All the control register, processors and IPs are in active state and clock is running for entire logic. This is the normal state of device functioning. 

- **STANDBY State** : This is state defined by the power state of the processor and IP clock gating. The system processor supports low power mode where the processor cores go into low power state and internally disables the clock to reduce power consumption. This can be achieved by WFI/WFE instruction execution on the core. Details of WFI/WFE power states can be found at Arm Cortex-R52 Processor Technical Reference Manual. Additionally, IP clocks needs to be gated to reduce dynamic power consumption in the IP. 

- **OFF State** :This is the OFF state of the device where all the external power supplies are turned off and PORz is asserted. During OFF state device is not active and power up sequence should be executed to power it up. 

Figure 6-13 depicts the valid power modes for the device. 

**==> picture [74 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
ACTIVE<br>STANDBY<br>OFF<br>**----- End of picture text -----**<br>


**Figure 6-13. Power Modes** 

## **6.2.4.2 Device Power States and Transitions** 

The transition to STANDBY state always needs to be done through ACTIVE state. Initially the device remains in OFF state. After power on sequence, device moves to ACTIVE state. All the clocks to processor and peripherals are ungated during ACTIVE state. In order to move to STANDBY state, WFI/WFE should be executed from individual R5SS and clock gating can be enabled for all or required peripherals. During this state dynamic power consumption is reduced. 

Transition from STANDBY state to ACTIVE state can be done through an IRQ which will enable the clocks to processor. But IP clocks are not automatically switched ON. They need to be programmed in MSS_RCM.<IP>_CLK_GATE register to enable/disable respective IP clock. 

The Device can transition into the OFF state from any state by pulling down the external power supplies to the device, which will turn off the device. The transitioning schemes explained above are shown below: 

- OFF → ACTIVE 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 267 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

- STANDBY → ACTIVE 

- ACTIVE → OFF 

- ACTIVE → STANDBY 

- STANDBY → OFF 

**==> picture [210 x 134] intentionally omitted <==**

**Figure 6-14. Transition between Power States** 

268 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **6.3 Reset** 

This chapter describes the device reset signals and contains details on reset management. 

## _**6.3.1 Overview**_ 

At a high-level, Resets are designed to bring a device or subsystem into a predetermined or known state. Resets are triggered in our device after power-up events, as well as upon various software and hardware reset requests. They are primarily used for system initialization, error detection, and debugging purposes. This chapter introduces the various reset capabilities available in the device and their functionality. 

## **Reset Architecture Block Diagram** 

This is the device reset architecture block diagram. It represents the devices reset sources and critical internal signal connections each of which are discussed in the subsequent sections. 

**==> picture [483 x 337] intentionally omitted <==**

**----- Start of picture text -----**<br>
AM263Px<br>A<br>SAFETY_ERRORn<br>ESM<br>TOP_RCM<br>Pulse2Level<br>Warm Reset Sources DelayShot One  Warm Reset out GZ<br>0 A<br>Warm Rst WARMRSTn<br>PORz Pmu_ok_1p1v TOP_RCMMMRs Glitch Filter 10 Warm Reset in<br>PMU<br>(Analog CIO) WIR WIR<br>PMUBYPASS Release MMR<br>Mask_hhv MSS_RCM CONTROLSS<br> Reset Sequencer & Reset SyncsReset Tree/ (Efuse Done, Clock Status SignalsOK etc) MSS_RCMMMRs CONTROLSSMMRs<br>SOP[3:0]<br>Test Logic Reset Tree/ Reset Tree/<br> Reset Sequencer &   Reset Sequencer &<br>Reset Syncs Reset Syncs<br>Test logic Test logic<br>Module Reset Outs Module Reset Outs Module Reset Outs<br>SYS_CLK LOSS ESM VMON TEMP_SENSORS[0:1] SOC_WDT x4 HSM WDT DEBUGGER SYSRST<br>S/W MMR SYSRST<br>Test Logic<br>**----- End of picture text -----**<br>


**Figure 6-15. AM263Px Reset Architecture Block Diagram** 

## **Note** 

ESM (Error Signaling Module) aggregates all safety related events from throughout the SoC and gives out an error signal to the ‘SAFETY_ERRORn’ pin in the case of an error. 

## **Note** 

‘Wait In Reset’ (WIR) signal from Debugss POWER AP extends the Warm Reset till the WIR signal is deasserted (Becomes HIGH). ‘Release from WIR’ signal deasserts the Warm Reset. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

269 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **6.3.1.1 SoC Supported Resets** 

There are various resets supported by the SoC, each of which are explained below. 

- **Power-On-Reset:** 

The device Power-on-Reset (POR) resets all the logic in the SoC without any exceptions. This reset is controlled by an external pin _**‘** PORz_ _**’**_ which is driven by an external (off-chip) "Power-Good" Circuit or Power Management IC (PMIC). The PORz pin should be held active LOW (0) until all power supplies are stable. It should also be driven low whenever the external PMIC detects that the 3.3V /1.2V supply is not in range. The system comes out of the reset only after an additional delay owing to efuse shifting and High Frequency Oscillator (XTAL) clock stabilization. 

- **Warm Resets:** 

The device Warm Reset resets only the logic sensitive to warm reset and does not affect the logic that are _‘_ Reset only on PORz **’** . No memories are affected by a Warm Reset, except MCANx_MSG_RAM and PRU DRAMx. However, ROM BL performs memory initialization of TCMA, L2 Banks 0/1 and MBOX RAM during each boot. Warm reset can be triggered by certain internal reset sources and also by asserting the ‘WARMRSTn’ pin externally. Additionally, the warm reset is brought out on ‘WARMRSTn’ pin to assert reset on external board components. When the pin is LOW, it indicates that the system is in a warm reset state. When HIGH, it indicates that the system is out of warm reset. 

## • **Local Module Resets:** 

These are module level resets programmed through software using the MMRs in RCM modules, only intended for debug purposes. They are uncontrolled resets and have potential side-effects (like pending interrupts, pending bus transactions, pending DMA triggers) that will impact the rest of the SOC. Hence, it is not recommended to use these resets in production and functional mode. 

270 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.3.2 Reset Details**_ 

The Reset Details section breaks down the available device resets and also explains operating details such as timing diagrams. 

This table summarizes the available reset sources that are supported by the device. 

**Table 6-23. Device Reset Sources** 

|**Reset Name**|**Reset Type**|**Sync/**<br>**Async**|**Pin/Register/ Internal**|**Details**|
|---|---|---|---|---|
|PORz|Hardware POR|Async|PORz HW Pin|PORz Reset|
|WARMRSTn|Hardware Warm<br>Reset|Async|WARMRSTn HW Pin|WARMRSTn|
|SW_WARMRSTn|Software Warm Reset|Async|TOP_RCM.WARM_RESET_REQ|SW_WARMRSTn|
|WDT Reset|WDT Reset|Async|Internal signal|WDT Resets|
|VMON Reset|VMON Reset|Async|Internal signal|Voltage Monitor Error Reset|
|ESM Reset|ESM Reset|Async|Internal signal|ESM Reset|
|SYS_CLK clock loss Reset|SYS_CLK clock loss<br>Reset|Async|Internal signal|Section 6.3.2.2.2.2|
|Thermal Reset|Thermal Reset|Async|Internal signal|Thermal Alert Reset|
|Debugger Reset|Debugger Reset|Async|Internal signal|Debugger Reset|
|Local Resets|Software Reset|Async|RCM MMRs|Local Module Resets|



## **6.3.2.1 PORz Reset** 

The external pin 'PORz' is the primary power on reset input (active LOW) to the entire device. When LOW, it performs a POR on the entire device and puts all IOs in a safe state (Reset/HHV state). Upon PORz deassertion, IOs will enter the default state defined in the Device Data sheet and the boot process will be initiated. 

Timing sequence below shows the reset sequence for WARMRSTn pad and the Internal Reset to System during PORz deassertion. 

**==> picture [239 x 104] intentionally omitted <==**

**----- Start of picture text -----**<br>
PORz<br>~ 2ms<br>WARMRSTn<br>Pad<br>~ 0.128ms<br>Internal<br>Reset to<br>system<br>**----- End of picture text -----**<br>


**Figure 6-16. PORz timing sequence** 

## **Note** 

MMRs which get 'reset by PORz only' are captured in register description of those registers. 

## **Note** 

SOP pin pull ups/pull downs which are needed to configure the boot mode should be held steady during the PORz assertion. 

## **6.3.2.2 Warm Resets** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 271 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

When a warm reset LOW is detected, Reset Hardware generates an internal warm reset to the system logics working on warm reset (Except for logics which are reset only by PORz). All IO configurations are reset during warm reset assertion. 

The following are the sources which can trigger a system warm reset in the device. 

1. PORz (Reset by PORz Hardware Pin) 

2. WARMRSTn (Reset by WARMRSTn Hardware Pin) 

3. SW MMR in RCM (Reset by TOP_RCM.WARM_RESET_REQ) 

4. WDT reset (Reset by 4x SoC WDTs or HSM WDT) 

5. Debugger reset (Reset by ‘SYSRESET’ from debugger) 

6. Thermal reset (Tempsensor[0:1] reset) 

7. VMON reset 

8. ESM reset 

9. SYS_CLK clock loss reset 

The cause for the warm reset is captured in TOP_RCM.WARM_RST_CAUSE register. Reset status bit reads active HIGH (1) when a particular reset is triggered. After reset is deasserted, device will boot-up and software can read the register to check the reset cause. TOP_RCM.WARM_RST_CAUSE_CLR should be written 3'b111 to clear the status bits. A PORz assertion also clears status register. 

Except PORz source, all other sources can be enabled and disabled individually. The timing sequence for internal warm reset source, WARMRSTn Pad and internal system reset are discussed in the following sections. 

## _**6.3.2.2.1 Warm Reset by WARMRSTn HW Pin**_ 

This reset pin is the warm reset request (active LOW) given externally from the pad.. 

By default, the input path to trigger a warm reset from external pad is disabled. To enable, the TOP_RCM.WARM_RESET_CONFIG.PAD_BYPASS bit should be written 3’b000. 

The timing diagram shows the reset sequence during WARMRSTn pad assertion and related timing for the internal system reset. 

The input pad signal should remain LOW for at least ‘TOP_RCM.WARM_RSTTIME3’ time to register an assertion of WARMRSTn. Similarly,the signal should remain HIGH for at least ‘TOP_RCM.WARM_RSTTIME2’ continuously to register a deassertion of WARMRSTn. The glitch filter logic on ‘Warm_Reset_in’ filters out any input pad signal which is LOW for less than ‘TOP_RCM.WARM_RSTTIME3’ time and HIGH for less than ‘TOP_RCM.WARM_RSTTIME2’ time. The internal system reset gets asserted at time TOP_RCM.WARM_RSTTIME3 and deasserted at ‘TOP_RCM.WARM_RSTTIME2’ time relative to external WARMRSTn pad 

**==> picture [274 x 102] intentionally omitted <==**

**----- Start of picture text -----**<br>
> WARM_RSTTIME2<br>> WARM_RSTTIME3<br>WARMRST n<br>Pad<br>WARM_RSTTIME2<br>WARM_RSTTIME3<br>Internal Rese t<br>to system<br>**----- End of picture text -----**<br>


## **Figure 6-17. WARMRSTn Pad reset sequence** 

For more details on programmable values for WARM_RSTTIME1/2/3 Vs The Corresponding Delays, refer to Control Modules, MSS_RCM section. 

## _**6.3.2.2.2 Internal Warm Reset Sources**_ 

The different internal reset sources are: 

272 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

- WDT Reset 

- Thermal reset (Tempsensor[0:1] reset) 

- VMON reset 

- ESM reset 

- SYS_CLK clock loss reset 

- Debugger Reset 

All of the warm reset sources have a corresponding enable bit in TOP_RCM.WARM_RESET_CONFIG register. Respective bits are configured for enabling the sources to trigger a warm reset. 

The Internal System Reset and the External WARMRSTn pad assertion happen along with the assertion of Internal Reset Sources. 

The external WARMRSTn pad deassertion is controlled by TOP_RCM.WARM_RSTTIME1 register. This is to enable sufficient reset assertion time for any external device relying on the reset signal. The internal system reset deassertion is relative to the deassertion of WARMRSTn pad and can be controlled by TOP_RCM.WARM_RSTTIME2. 

The timing sequence below shows the overall sequence between assertion of Internal Reset Sources (Internal Reset Req) relative to Internal System Reset (Internal Reset to System) and WARMRSTn pad. 

**==> picture [230 x 157] intentionally omitted <==**

**----- Start of picture text -----**<br>
Internal<br>Reset<br>Req<br>WARM_RSTTIME1<br>WARMRSTn<br>Pad<br>WARM_RSTTIME2<br>Internal<br>Reset to<br>system<br>**----- End of picture text -----**<br>


**Figure 6-18. Internal Warm Reset Sequence** 

## _**6.3.2.2.2.1 Thermal Alert Reset**_ 

## **Reset Overview** 

The Thermal manager module outputs an alert signal TSHUT_RST0 and TSHUT_RST1 for the two comparators in thermal manager, when the device temperature goes beyond a maximum threshold. This alert is used as a reset trigger for warm reset to the the system. 

Thermal manager alert will be active as long as the error condition (Device Temperature > Maximum Temperature Threshold) is still TRUE. 

When the error goes away, alert will be de-asserted and device will come out of warm reset. 

For more details on Thermal manager shutdown comparator please refer to Section 6.2.2.2.2.5 

## _**6.3.2.2.2.2 SYS_CLK Clock Loss Reset**_ 

## **Reset Overview** 

This reset trigger for warm reset to the system is issued when the SYS_CLK clock loss event occurs and if reset is enabled using the register **WARM_RESET_CONFIG_MISC** . 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 273 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.3.2.2.2.3 Voltage Monitor Error Reset**_ 

## **Reset Overview** 

This reset trigger for warm reset to the system (if enabled using the registers **WARM_RESET_CONFIG_OV** and **WARM_RESET_CONFIG_UV** ) is issued when there is a loss of power on any of the voltage rails, i.e., 3.3V, 1.8V or 1.2V, which can be monitored using the power safety monitors. These monitors can be enabled by writing into the corresponding registers as explained in the section **Power OK (POK) Modules** . 

## _**6.3.2.2.2.4 ESM Errors Reset**_ 

## **Reset Overview** 

ESM module monitors the SoC errors and can cause a system warm reset if enabled using the **WARM_RESET_CONFIG_MISC** register. 

The critical priority interrupt from ESM can trigger a warm reset. 

## _**6.3.2.2.2.5 Debugger Reset**_ 

The debugger also can issue a warmreset by initiating a SYSRESET request. 

## _**6.3.2.2.2.6 WDT Resets**_ 

This reset is issued when a WDT timeout event occurs. There are 4 WDT available at SOC which can be allocated to individual R5SS cores. Additional HSM has its own dedicated WDT. 

## _**6.3.2.2.3 SW Warm Reset**_ 

This reset is triggered by a software controlled warm reset register TOP_RCM.WARM_RESET_REQ. The reset timing is the same as internal warm reset sources. 

Any processor which needs to issue a warm reset to the system, should write 3'b000 into the TOP_RCM.WARM_RESET_REQ register. 

## **6.3.2.3 Local Module Resets** 

The MSS_RCM.<IP>_RST_CTRL MMR’s in the MSS_RCM module can be used by S/w to affect reset of individual modules. This feature is for debug purpose only. Software needs to ensure the state of the Device/IP before configuring. 

## **6.3.2.4 R5FSS Reset** 

Transitions from Lockstep to Dual Core or vice-versa (on supported parts) and enforcing ROM eclipse requires triggering MSS_CTRL. R5SSx_CONTROL_RESET_FSM_TRIGGER ( Note that this resets the full cluster) or triggering the STC (Self Test Controller). 

By default, R5FWFI (Wait for Interrupt) check is enabled by MSS_RCM.R5SSx_RST_WFICHECK register. The 

FSM checks if the CPU is in WFI state before propagating the reset. 

## **Note** 

Disabling R5FWFI check is not recommended. 

Delays for asserting the reset and holding the reset can be programmed in the MSS_RCM.R5SSx_RST_ASSERDLYand MSS_RCM.R5SSx_RST2ASSERTDLY registers. 

Individual R5SS have their own status register MSS_RCM.R5SSx_RST_STATUS to capture the source of R5SS internal resets. Reset status bits are read active HIGH (1) when a particular reset is triggered. After reading this reset source register, software must clear the register. MSS_RCM.R5SSx_RST_CAUSE_CLR needs to be written 3'b111 to clear the status bits. 

The following are the R5SS Reset sources: 

274 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

- POR Reset 

- Warm Reset (Also asserted during POR Reset) 

- R5SSx STC Reset 

- Reset for CORE0 and CORE0_VIM using MSS_RCM.R5SSx_CORE0_GRST_CTRL 

- Reset for CORE1 and CORE1_VIM using MSS_RCM.R5SSx_CORE1_GRST_CTRL 

- Reset for CORE0 only using MSS_RCM.R5SSx_CORE0_LRST_CTRL 

- Reset for CORE1 only using MSS_RCM.R5SSx_CORE1_LRST_CTRL 

- Reset for CORE0 and CORE0_VIM caused because of reset request by debugger in CORE0 

- Reset for CORE1 and CORE1_VIM caused because of reset request by debugger in CORE1 

- Reset for R5SSx by the RESET FSM using MSS_CTRL.R5SSx_CONTROL_RESET_FSM_TRIGGER 

- Reset for R5SSx using MSS_RCM.R5SSx_POR_RST_CTRL0 

## **Note** 

R5SSx refers to R5SS0 and R5SS1. 

For additional details on R5SS Resets, refer to R5SS Chapter. 

## **6.3.2.5 Reset - High Heating Value (HHV)** 

IOs support HHV mode during power up. HHV is defined as a state when PORz signal is driven LOW. 

HHV is an IO Voltage Buffer feature that allows the IO cells to be tri-stated. All IO cells have HHV which is asserted (driven) by HHV generated during PORz assertion. There default pull values during this HHV/PORz assertion for each pin are specified in the device-specific data sheet. All HHV logic controlling the buffer high-impedance control and the associated default pull value will be asynchronous. 

For more details on HHV signals, refer to _Device Configuration - Power Chapter Device Configuration - Power Chapter_ 

## _**6.3.3 Core and Cluster Reset logic**_ 

**Table 6-24. Reset effect on different R5FSS modules for different reset types** 

|**Mdl**|**Both Core**|**Both Core**|**Both Core**|**Single Core**|**Single Core**|
|---|---|---|---|---|---|
|**oues**|**Device POR**|**Device WARM RSTn**|**Cluster RSTn1 **|**GRSTn2 **|**LRSTn3 **|
|R5F CPU|Yes|Yes|Yes|Yes|Yes|
|VIM|Yes|Yes|Yes|Yes|No|
|TCM Logic|Yes|Yes|Yes|Yes|No|
|VIM RAM|No|No|No|No|No|
|TCM RAM|No|No|No|No|No|



1Cluster RSTn is the reset for R5SSx by the RESET FSM using MSS_CTRL.R5SSx_CONTROL_RESET_FSM_TRIGGER 

2GRSTn is the reset for CORE0/1 and CORE0/1_VIM using MSS_RCM::R5SSx_CORE0/1_GRST_CTRL 

3LRSTn is the reset for CORE0/1 only using MSS_RCM::R5SSx_CORE0/1_LRST_CTRL 

## _**6.3.4 Reset Status**_ 

This section summarizes the Reset Status functionality. The status of a specific individual reset is represented by an Output Pin or Software Bit. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 275 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-25. Reset Status Table** 

|**Reset Status Name**|**Reset Status**<br>**Source**|**Reset Status Info**|**Signal Active Level**|**Reset Signal Details**|
|---|---|---|---|---|
|TOP_RCM.WARM_RST_CA<br>USE Status Register|Register|Status register capturing<br>which event caused the<br>warm reset|Status bits read active<br>HIGH (1) when a particular<br>reset is asserted.|WARM_RST_CAUSE|
|MSS_RCM.R5SSx_RST_ST<br>ATUS|Register|Status register capturing<br>which event caused the<br>corresponding R5SS reset|Status bits read active<br>HIGH (1) when a particular<br>reset is asserted.|R5SSx_RST_STATUS|
|WARMRSTn|Output Pin|On/Off pin status of warm<br>reset|Active LOW (0)|WARMRSTn|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

276 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.3.5 Reset Registers**_ 

The reset control registers enable, disable, and adjust specific reset operations. 

For additional details related to Reset Control registers, please refer to the Control Modules - MSS_RCM section. 

## _**6.3.6 Reset Power up Sequence**_ 

For additional details related to reset power up sequence, please refer to _Device Configuration - Power Chapter_ and the _Power On and Reset Sequencing_ section of the device data sheet. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

277 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **6.4 Clocking** 

This chapter describes the clock architecture of the device. 

## _**6.4.1 Overview**_ 

To satisfy the various subsystems requirements, the device features multiple clock sources and clock generators. The following are the components used to generate the system's root clocks: 

- External Crystal Driver (XTALCLK) 

- Internal Oscillator (RCOSC32K and CIO's RCCLK_10M) 

- Phase-Locked Loop circuits (CORE PLL and PER PLL) 

- Dividers (HSDIVIDER for each PLL) 

Figure 6-19 shows a high-level overview of the device root clocks architecture. The figure captures the key clock sources and the configuration options available to select the appropriate clock source. The detailed structure is captured under the Analog Modules section. The generated clocks are further muxed and divided to generate the appropriate clock for each IP. This is discussed in the IP Clocking section 

**==> picture [459 x 361] intentionally omitted <==**

**----- Start of picture text -----**<br>
EXT_REFCLK up to 100 MHz<br>Pad PLL_CORE_CLK_SOURCE_SEL<br>DPLL_CORE_HSDIV0_CLKOUT0  :  400 MHz<br>(Main CLK)<br>1<br>DPLL_CORE_HSDIV0_CLKOUT1  :  500 MHz<br>2000 MHz (Eth CLK)<br>CORE PLL<br>0 DPLL_CORE_HSDIV0_CLKOUT2  :  400 MHz<br>(ControlSS PLL CLK)<br>DPLL_CORE_HSDIV0_CLKOUT2  :  200 MHz<br>XTALCLK 25 MHz<br>(OPTI_FLASH CLK)<br>XTALCLK 25 MHz<br>Pad<br>PLL_PER_CLK_SOURCE_SEL<br>DPLL_PER_HSDIV0_CLKOUT0  :  160 MHz<br>1 (Alt Uart Clk)<br>1920 MHz<br>PER PLL DPLL_PER_HSDIV0_CLKOUT1  :  192 MHz<br>0 (Periph Clk)<br>DPLL_PER_HSDIV0_CLKOUT2  :  160 MHz<br>(OPTI_FLASH CLK)<br>CIO RCCLK_10M 10 MHz<br>RCOSC32K RCCLK_32K 32 KHz<br>TCK 10 MHz<br>Pad<br>HSDIVIDER<br>HSDIVIDER<br>**----- End of picture text -----**<br>


**Figure 6-19. Root Clocks** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

278 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

The device has 2 PLLs (CORE PLL and PER PLL ) which take a reference clock as input and give out the required clock frequency. The reference clock can either be external crystal driver provided through ‘XTAL_XI’ pad or external reference clock provided through ‘EXT_REFCLK0’ PAD. This selection can be provided using the TOP_RCM.PLL_REF_CLK_SRC_SEL register. The PLL clocks are further divided using ‘HSDIVIDER’ module to generate desired frequencies for all the IPs in the device. Internal oscillators generate 10MHz and 32KHz RCCLKs. TCK (JTAG clock) from the pad is used for debugging purposes. 

Additionally, CPTS_GENF0 generated in CPSW module is also used as a root clock. Refer to the CPSW chapter for more details. 

The device's root clocks are depicted in the _Root Clocks Table_ 

**Table 6-26. Root Clocks Table** 

|**Root Clocks**|**Frequency (MHz)**|
|---|---|
|DPLL_CORE_HSDIV0_CLKOUT0|400|
|DPLL_CORE_HSDIV0_CLKOUT1|500|
|DPLL_CORE_HSDIV0_CLKOUT2|400|
|DPLL_CORE_HSDIV0_CLKOUT3|200|
|DPLL_PER_HSDIV0_CLKOUT0|160|
|DPLL_PER_HSDIV0_CLKOUT1|192|
|DPLL_PER_HSDIV0_CLKOUT2|160|
|RCCLK32K|0.032|
|RCCLK10M|10|
|XTALCLK|25|
|SYS_CLK|200|
|EXT_REFCLK|100|
|CPSW CPTS GENF0|50|
|JTAG_TCK|10|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 279 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **6.4.1.1 Analog Modules** 

## _**6.4.1.1.1 PLL Module**_ 

Clock Generator PLL (Phase-Locked Loop) circuits are used in the device to multiply a lower-frequency reference clock to the required operating frequency of the respective subsystem(s). The reference clock can either be external crystal driver provided through ‘XTAL_XI’ pad or external reference clock provided through ‘EXT_REFCLK0’ pad. This selection can be provided using the TOP_RCM.PLL_REF_CLK_SRC_SEL register 

The low-jitter ADPLLLJ module is use as the Device CORE and PER PLLs. A high level block diagram of the ADPLLLJ is shown in Figure 6-20. 

**==> picture [418 x 132] intentionally omitted <==**

**----- Start of picture text -----**<br>
REGM2 value<br>, PLL_x_M2NDIV.M2<br>CLKINP 1/(N+1) PFD T2D DCO fDPLL 1/M2 CLKOUTLDO<br>PLL_x_M2NDIV.N  [REGN value]<br>ΣΔ 1/SD<br>1/M<br>PLL<br>REGM value<br>PLL_x_MN2DIV.M<br>REGSD value<br>PLL_x_FRACDIV.REGSD  ADPLLLJ<br>**----- End of picture text -----**<br>


**Figure 6-20. ADPLLLJ Architecture** 

The ADPLLLJ has the following input/output clocks 

- CLKINP is the mandatory reference clock used to generate the synthesized clock. It can also be used to generate the bypass clock whenever the ADPLLLJ enters a bypass mode. 

- CLKOUTLDO is the secondary output clock generated from the lock frequency of the PLL and post dividers. It does not have a bypass mode 

The ADPLLLJ can be programmed to be locked at any frequency given by the following equation: 

**==> picture [184 x 75] intentionally omitted <==**

Where: 

- fDPLL is the lock frequency. 

- CLKINP is the reference system clock frequency. 

- M is the 12-bit “multiplication ratio” binary value (2 – 4095). In Device it is S/W programmable via a dedicated PRCM register. 

- N is the 8-bit “division ratio” binary value (0 – 255). In Device it is S/W programmable via a dedicated PRCM register. 

- M2 is the 7-bit post divider binary value (1 – 127). In Device is S/W programmable via a dedicated PRCM register. 

PLL input values and status ouptuts are routed to TOP_RCM MMRs 

## _**6.4.1.1.2 CORE PLL Overview**_ 

CORE_PLL is primarily responsible for the following IPs: 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

280 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

|**Description**|**Key Frequencies (MHz)**|
|---|---|
|R5 Clock|400|
|Interconnect|200|
|Ethernet (CPSW)|250/50/5|
|CANFD|80|
|FSS/OSPI/OPTI_FLASH|133|
|HSM Clock|200|
|SPI Clock|50|
|FSI/SDFM PLL Clock|400|



## _**6.4.1.1.3 PER PLL Overview**_ 

PER_PLL is primarily responsible for the following IPs: 

|**Description**|**Key Frequencies (MHz)**|
|---|---|
|UART Clock|192|
|MMC Clock|50|
|SPI Clocks|48|
|I2C Clocks|48|



## _**6.4.1.1.4 PLL Hookup**_ 

The HSDIVIDER module output can be bypassed to obtain the XTALCLK clock input on any HSDIVx_CLKOUTx. For example, on the CORE_PLL, this can be done by programming the register PLL_CORE_HSDIVIDER = 0 in TOP_RCM. 

PLL input pins are driven by TOPRCM:<Clock Instance>_SRC_SEL MMRs and the outputs are mapped as status on the TOPRCM:<Clock Instance>_STATUS MMRs. 

The PHASELOCK output indicates phase tracking between output clocks (CLKOUT, CLKOUTLDO and CLKDCOLDO) and input clock (CLKINP). PHASELOCK is asserted when internally the phase difference between _FBCLK_ and _REFCLK_ is less than 6-12% of the _REFCLK_ period for 96 continuous _REFCLKs._ 

The PHASELOCK signal of CORE and PER PLL are inverted and connected as corresponding lock loss signal in ESM as shown in the following table: 

**Table 6-27. Lock Loss Event Mapping** 

|**Source**|**Event Mapping**|**Type**|**Polarity**|
|---|---|---|---|
|PLL_CORE_LOCKLOSS|ESM_LVL_EVENT_25|Level|High|
|PLL_PER_LOCKLOSS|ESM_LVL_EVENT_26|Level|High|



## _**6.4.1.1.5 HSDIVIDER Module**_ 

The PLL can be coupled with an HSDIVIDER module to generate additional clocks which are divided down from the PLL lock frequency. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

281 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**==> picture [375 x 218] intentionally omitted <==**

**----- Start of picture text -----**<br>
HSDIVIDER<br>BYPASS<br>CLKINBYPASS 1<br>CLKOUT0<br>CLKINPHIFLDO 1/(DIVx+1) 0<br>CLKOUT1<br>DIVx value<br>DIV1[4:0]<br>CLKOUT2<br>CLKOUT1EN<br>DIV2[4:0] CLKOUT3<br>CLKOUT2EN<br>DIV3[4:0]<br>CLKOUT3EN<br>DIV4[4:0]<br>CLKOUT4EN<br>**----- End of picture text -----**<br>


**Figure 6-21. HSDIVIDER Architecture** 

The HSDIVIDER has two input clocks: 

- CLKINPHIFLDO is the mandatory reference clock used to generate the divided clock outputs. 

- CLKINBYPASSis an optional clock input and is used as the bypass clock. 

The HSDIVIDER provides 4 post divider clocks whose frequency is given by: 

**==> picture [168 x 41] intentionally omitted <==**

Where: 

- CLKINPHIFLDO is the input clock frequency. 

- DIVx is the 5-bit divisor binary value (0-31) on the device, DIVx values are software programmable via dedicated TOP_RCM.PLL_CORE_HSDIVIDER_CLKOUTx.DIV and TOP_RCM.PLL_PER_HSDIVIDER_CLKOUTx.DIV registers 

## **Note** 

All the CLKOUTx are not used in all the PLLs, refer to the Root Clocks Table to see the ones supported. 

## **Note** 

The clocking subsytem provides registers to directly configure the final divide value of "DIVx+1". When specifying the desired HSDIV value to use, it should be specified as "DIVx-1". 

## **Note** 

The "DIVx+1" reset value is 4. 

## **6.4.1.2 R5SS and SYSCLK Clock Tree** 

The device’s SYS_CLK is generated using GCM and GCM_Divider modules. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

282 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

The GCM module takes 8 clock sources as inputs and gives an output clock according to the select (MODULEx_CLK_SRC_SEL) provided. Additionally, one can gate the output clock using the clock gating input (MODULEx_CLK_GATE) 

The GCM_Divider module takes in an input clock and divides it according to the divider value (MODULEx_CLK_DIV_VAL) 

R5SS/SYSCLK Clocking gives an overview of the R5 Subsystem and SYSCLK Clocking structure. 

**==> picture [478 x 298] intentionally omitted <==**

**Figure 6-22. R5SS/SYSCLK Clocking** 

R5SS_CORE_CLK:SYSCLK shows the different operation options concerning the ratio between R5SS_CORE_CLK and the SYSCLK. 

**Table 6-28. R5SS_CORE_CLK:SYSCLK Achievable Ratio** 

|**R5SS_CORE_C**<br>**LK:SYS_CLK**<br>**Ratio**|**Configuration**|**R5_CORE**<br>**Frequency**|**SYS_CLK**<br>**Frequency**|**Notes**|
|---|---|---|---|---|
|1:1|R5FSS_CLK_SELECTED = 400MHz<br>SYS_CLK_DIVIDER = Div by 2<br>MSS_CR5*_CLK_DIV_SEL = 1|200MHz|200MHz|This config is used for dynamic<br>switching from 2:1 and 1:1.<br>R5_CORE is 400MHz, only the DIV<br>bit needs to be modified|
|2:1|R5FSS_CLK_SELECTED = 400MHz<br>SYS_CLK_DIVIDER = Div by 2<br>MSS_CR5*_CLK_DIV_SEL = 0|400MHz|200MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 283 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.4.2 Clock IO**_ 

## **6.4.2.1 Overview** 

Various external clock inputs are needed to drive the device, as well as there are external sources of the clock provisioned for certain peripherals. The clocks in the AM263Px device are as depicted in External Clocks 

The device provides several system clock outputs. Summary of these output clock signals is as follows: 

- R5FSS[1:0]_CLK 

- SYS_CLK 

- CLKOUT[1:0] 

- IP Clocks 

The IP Clocks are routed directly from subsystems to device pins, and they are described in the respective module chapter. 

For more details on IP clocks generation, please refer to IP Clocking Section 

## **Figure 6-23. External Clocks** 

284 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

|XTALCLK<br>JTAG T<br>EXT_RE<br>R5FSS0_<br>SYSCL|25Mhz<br>CK<br>FCLK<br>CLK<br>K|25Mhz<br>CK<br>FCLK<br>CLK<br>K|||RCOSC_10M<br>RCOSC_32K<br>XTAL_OSC<br>JTAG<br>CLKOUT<br>I2Cx<br>CPSW<br>SPI<br>OSPIx<br>MMCSD<br>ICSS-M 0<br>PINMUX<br>FSITX<br>FSIRX<br>SDFMx<br>EQEP<br>R5FSS||CL<br>CL<br>I2<br><br> <br><br>R<br>R<br><br>P<br>R<br> <br> <br>P<br>F<br><br>P<br>P<br>P|KOUT0<br>KOUT1<br>Cx_SCL<br>SPIx_CLK<br>OSPIx_CLK (with<br>loop-back)<br>MMCSD_CLK<br>GMII1,2 TX_CLK<br>GMII1,2 RX_CLK<br>MDIO_CLK<br>RU0,1_MII TX CLK<br>MII1,2 REF_CLK<br>MII1,2 TX_CLK<br>MII1,2 RX_CLK<br>RU0,1 MII RX CLK<br>SI_TX_CLKx<br>FSI_RX_CLKx<br>RU1_ENDAT(0,1,2)_CLK<br>RU1_SD(0-8)_CLK<br>RU MDIO_CLK<br>SDFMx_CLKx<br>EQEPx STROBE|
|---|---|---|---|---|---|---|---|---|
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||XTAL_OSC||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

285 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **Note** 

While this device does not support a separate Observation Clock output signal, the system level functionality is recognized by utilizing the CLKOUT[1:0] signals 

## **Note** 

CLKOUT0 will reflect RC clock after POK is asserted and switch to XTAL_CLK after Internal SYS_RST is released 

## **6.4.2.2 Clock IO Mapping** 

Please refer to the _Terminal Configurations and Functions_ section of the device-specific Data sheet. 

## _**6.4.3 IP Clocking**_ 

The required IP clocks for the device are generated using the Root clocks mentioned in Root clocks section. 

To generate the IP clocks, the root clocks are muxed and divided using the GCM and GCD modules respectively. 

The GCM module takes 8 clock sources as inputs and gives an output clock according to the select (MODULEx_CLK_SRC_SEL) provided. Additionally, one can gate the output clock using the clock gating input (MODULEx_CLK_GATE) 

The GCM_Divider module takes in an input clock and divides it according to the divider value (MODULEx_CLK_DIV_VAL) provided. Note that to divide the input clock by ‘DIV’ value, the MMR value provided should be ‘DIV-1’ 

## **6.4.3.1 IP Clocks Having GCM** 

The structure is similar for all IP’s having dedicated GCM’s 

**==> picture [454 x 116] intentionally omitted <==**

**Figure 6-24. Generic IP clocking with GCM and Divider** 

Refer to the Clock Selection table for more details on MMRs present and clock sources for all the peripherals 

## **6.4.3.2 IP Clocks working on SYS_CLK** 

Every IP working on SYS_CLK has a separate clock gate. In the case that clock gate is implemented in the IP, clock is routed directly to the IP with no clock gate inserted at the SOC-level. The diagram below shows the generic structure for all IP sourced from SYS_CLK. 

286 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**==> picture [402 x 172] intentionally omitted <==**

**Figure 6-25. Generic IP clocking with SYS_CLK** 

## **Note** 

In the case that the peripherals implement clock gating internal to the IP, no additional ICG is provisioned in RCM. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

287 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **6.4.3.3 Clock Selection** 

Table 6-29 lists the configuration options for the clock source, divider, and gating selections for different peripheral clocks. 

**Table 6-29. Configuration Options** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|R5FSS_CLK_MUX|0|XTALCLK|R5SS_CLK_SRC_SE<br>L|R5SS0_CLK_DIV_SE<br>L|R5SS0_CLK_GATE|R5SS0|
||1|EXT_REFCLK|||||
||2|DPLL_CORE_HSDIV0_CLKOUT0|||||
||3|RCCLK10M|||||
||4|RCCLK10M||R5SS1_CLK_DIV_SE<br>L|R5SS1_CLK_GATE|R5SS1|
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|TRC_CLKOUT_CLK_<br>MUX|0|XTALCLK|TRCCLKOUT_CLK_S<br>RC_SEL|TRCCLKOUT_DIV_V<br>AL|TRCCLKOUT_CLK_G<br>ATE|Trace|
||1|DPLL_CORE_HSDIV0_CLKOUT0|||||
||2|DPLL_CORE_HSDIV0_CLKOUT1|||||
||3|DPLL_PER_HSDIV0_CLKOUT0|||||
||4|DPLL_PER_HSDIV0_CLKOUT1|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|CLKOUT0_CLK_MUX|0|XTALCLK|CLKOUT0_CLK_SRC<br>_SEL|CLKOUT0_DIV_VAL|CLKOUT0_CLK_GAT<br>E|CLKOUT0|
||1|DPLL_CORE_HSDIV0_CLKOUT0|||||
||2|DPLL_CORE_HSDIV0_CLKOUT1|||||
||3|DPLL_PER_HSDIV0_CLKOUT0|||||
||4|DPLL_PER_HSDIV0_CLKOUT1|||||
||5|RCCLK10M|||||
||6|RCCLK32K|||||
||7|CTPS_GENF0|||||



288 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|CLKOUT1_CLK_MUX|0|XTALCLK|CLKOUT1_CLK_SRC<br>_SEL|CLKOUT1_DIV_VAL|CLKOUT1_CLK_GAT<br>E|CLKOUT1|
||1|DPLL_CORE_HSDIV0_CLKOUT0|||||
||2|DPLL_CORE_HSDIV0_CLKOUT1|||||
||3|DPLL_PER_HSDIV0_CLKOUT0|||||
||4|DPLL_PER_HSDIV0_CLKOUT1|||||
||5|RCCLK10M|||||
||6|RCCLK32K|||||
||7|CTPS_GENF0|||||
|RTI0_CLK_MUX|0|XTALCLK|RTI0_CLK_SRC_SEL|RTI0_CLK_DIV_VAL|RTI0_CLK_GATE|RTI0|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT1|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|CTPS_GENF0|||||
|RTI1_CLK_MUX|0|XTALCLK|RTI1_CLK_SRC_SEL|RTI1_CLK_DIV_VAL|RTI1_CLK_GATE|RTI1|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT1|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|CTPS_GENF0|||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 289 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|RTI2_CLK_MUX|0|XTALCLK|RTI2_CLK_SRC_SEL|RTI2_CLK_DIV_VAL|RTI2_CLK_GATE|RTI2|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT1|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|CTPS_GENF0|||||
|RTI3_CLK_MUX|0|XTALCLK|RTI3_CLK_SRC_SEL|RTI3_CLK_DIV_VAL|RTI3_CLK_GATE|RTI3|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT1|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|CTPS_GENF0|||||
|WDT0_CLK_MUX|0|XTALCLK|WDT0_CLK_SRC_SE<br>L|WDT0_CLK_DIV_VAL|WDT0_CLK_GATE|WDT0|
||1|RCCLK10M|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT1|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK32K|||||



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

290 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|WDT1_CLK_MUX|0|XTALCLK|WDT1_CLK_SRC_SE<br>L|WDT1_CLK_DIV_VAL|WDT1_CLK_GATE|WDT1|
||1|RCCLK10M|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT1|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK32K|||||
|WDT2_CLK_MUX|0|XTALCLK|WDT2_CLK_SRC_SE<br>L|WDT2_CLK_DIV_VAL|WDT2_CLK_GATE|WDT2|
||1|RCCLK10M|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT1|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK32K|||||
|WDT3_CLK_MUX|0|XTALCLK|WDT3_CLK_SRC_SE<br>L|WDT3_CLK_DIV_VAL|WDT3_CLK_GATE|WDT3|
||1|RCCLK10M|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT1|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK32K|||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 291 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|OSPI_CLK_MUX|0|XTALCLK|OSPI0_CLK_SRC_SE<br>L|OSPI0_CLK_DIV_VAL|OSPI0_CLK_GATE|OSPI|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|SPI0_CLK_MUX|0|XTALCLK|MCSPI0_CLK_SRC_<br>SEL|MCSPI0_CLK_DIV_V<br>AL|MCSPI0_CLK_GATE|SPI0|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|SPI1_CLK_MUX|0|XTALCLK|MCSPI1_CLK_SRC_<br>SEL|MCSPI1_CLK_DIV_V<br>AL|MCSPI1_CLK_GATE|SPI1|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

292 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|SPI2_CLK_MUX|0|XTALCLK|MCSPI2_CLK_SRC_<br>SEL|MCSPI2_CLK_DIV_V<br>AL|MCSPI2_CLK_GATE|SPI2|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|SPI3_CLK_MUX|0|XTALCLK|MCSPI3_CLK_SRC_<br>SEL|MCSPI3_CLK_DIV_V<br>AL|MCSPI3_CLK_GATE|SPI3|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|SPI4_CLK_MUX|0|XTALCLK|MCSPI4_CLK_SRC_<br>SEL|MCSPI4_CLK_DIV_V<br>AL|MCSPI4_CLK_GATE|SPI4|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 293 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|SPI5_CLK_MUX|0|XTALCLK|MCSPI5_CLK_SRC_<br>SEL|MCSPI5_CLK_DIV_V<br>AL|MCSPI5_CLK_GATE|SPI5|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|SPI6_CLK_MUX|0|XTALCLK|MCSPI6_CLK_SRC_<br>SEL|MCSPI6_CLK_DIV_V<br>AL|MCSPI6_CLK_GATE|SPI6|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|SPI7_CLK_MUX|0|XTALCLK|MCSPI7_CLK_SRC_<br>SEL|MCSPI7_CLK_DIV_V<br>AL|MCSPI7_CLK_GATE|SPI7|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

294 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|I2C_CLK_MUX|0|XTALCLK|I2C_CLK_SRC_SEL|I2C_CLK_DIV_VAL|I2C0_CLK_GATE|I2C0|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||I2C1_CLK_GATE|I2C1|
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||I2C2_CLK_GATE|I2C2|
||5|RCCLK10M|||||
||6|XTALCLK|||I2C3_CLK_GATE|I2C3|
||7|RCCLK10M|||||
|UART0_CLK_MUX|0|XTALCLK|LIN0_UART0_CLK_S<br>RC_SEL|LIN0_UART0_CLK_DI<br>V_VAL|UART0_CLKGATE|UART0|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||LIN0_CLKGATE|LIN0|
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|DPLL_PER_HSDIV0_CLKOUT0|||||
|UART1_CLK_MUX|0|XTALCLK|LIN1_UART1_CLK_S<br>RC_SEL|LIN1_UART1_CLK_DI<br>V_VAL|UART1_CLKGATE|UART1|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||LIN1_CLKGATE|LIN1|
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|DPLL_PER_HSDIV0_CLKOUT0|||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 295 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|UART2_CLK_MUX|0|XTALCLK|LIN2_UART2_CLK_S<br>RC_SEL|LIN2_UART2_CLK_DI<br>V_VAL|UART2_CLKGATE|UART2|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||LIN2_CLKGATE|LIN2|
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|DPLL_PER_HSDIV0_CLKOUT0|||||
|UART3_CLK_MUX|0|XTALCLK|LIN3_UART3_CLK_S<br>RC_SEL|LIN3_UART3_CLK_DI<br>V_VAL|UART3_CLKGATE|UART3|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||LIN3_CLKGATE|LIN3|
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|DPLL_PER_HSDIV0_CLKOUT0|||||
|UART4_CLK_MUX|0|XTALCLK|LIN4_UART4_CLK_S<br>RC_SEL|LIN4_UART4_CLK_DI<br>V_VAL|UART4_CLKGATE|UART4|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||LIN4_CLKGATE|LIN4|
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|DPLL_PER_HSDIV0_CLKOUT0|||||



296 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|UART5_CLK_MUX|0|XTALCLK|LIN5_UART5_CLK_S<br>RC_SEL|LIN5_UART5_CLK_DI<br>V_VAL|UART5_CLKGATE|UART5|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|DPLL_PER_HSDIV0_CLKOUT0|||||
|ICSS_UART_CLK_M<br>UX|0|XTALCLK|ICSSM0_UART0_CLK<br>_SRC_SEL|ICSSM0_UART_CLK_<br>DIV_VAL|ICSSM0_UART_CLK_<br>GATE|ICSSM|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|DPLL_PER_HSDIV0_CLKOUT0|||||
|MCAN0_CLK_MUX|0|XTALCLK|MCAN0_CLK_SRC_S<br>EL|MCAN0_CLK_DIV_VA<br>L|MCAN0_CLK_GATE|MCAN0|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 297 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|MCAN1_CLK_MUX|0|XTALCLK|MCAN1_CLK_SRC_S<br>EL|MCAN1_CLK_DIV_VA<br>L|MCAN1_CLK_GATE|MCAN1|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|MCAN2_CLK_MUX|0|XTALCLK|MCAN2_CLK_SRC_S<br>EL|MCAN2_CLK_DIV_VA<br>L|MCAN2_CLK_GATE|MCAN2|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|MCAN3_CLK_MUX|0|XTALCLK|MCAN3_CLK_SRC_S<br>EL|MCAN3_CLK_DIV_VA<br>L|MCAN3_CLK_GATE|MCAN3|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||



298 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|MCAN4_CLK_MUX|0|XTALCLK|MCAN4_CLK_SRC_S<br>EL|MCAN4_CLK_DIV_VA<br>L|MCAN4_CLK_GATE|MCAN4|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|MCAN5_CLK_MUX|0|XTALCLK|MCAN5_CLK_SRC_S<br>EL|MCAN5_CLK_DIV_VA<br>L|MCAN5_CLK_GATE|MCAN5|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|MCAN6_CLK_MUX|0|XTALCLK|MCAN6_CLK_SRC_S<br>EL|MCAN6_CLK_DIV_VA<br>L|MCAN6_CLK_GATE|MCAN6|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 299 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|MCAN7_CLK_MUX|0|XTALCLK|MCAN7_CLK_SRC_S<br>EL|MCAN7_CLK_DIV_VA<br>L|MCAN7_CLK_GATE|MCAN7|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|MMCSD_CLK_MUX|0|XTALCLK|MMC0_CLK_SRC_SE<br>L|MMC0_CLK_DIV_VAL|MMC0_CLK_GATE|MMC|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|CPTS_CLK_MUX|0|XTALCLK|CPTS_CLK_SRC_SE<br>L|CPTS_CLK_DIV_VAL|CPTS_CLK_GATE|CPSW|
||1|EXT_REFCLK|||||
||2|SYS_CLK|||||
||3|DPLL_CORE_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||



300 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|HSM_RTI_CLK_MUX|0|XTALCLK|HSM_RTIA_CLK_SR<br>C_SEL|HSM_RTI_CLK_DIV_<br>VAL|HSM_RTI_CLK_GATE|RTI|
||1|XTALCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|RCCLK10M|||||
||5|RCCLK10M|||||
||6|EXT_REFCLK|||||
||7|RCCLK32K|||||
|HSM_WDT_CLK_MU<br>X|0|XTALCLK|HSM_WDT_CLK_SR<br>C_SEL|HSM_WDT_CLK_DIV<br>_VAL|HSM_WDT_CLK_GA<br>TE|WDT|
||1|XTALCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|RCCLK10M|||||
||5|RCCLK10M|||||
||6|EXT_REFCLK|||||
||7|RCCLK32K|||||
|HSM_RTC_CLK_MU<br>X|0|XTALCLK|HSM_RTC_CLK_SRC<br>_SEL|HSM_RTC_CLK_DIV<br>_VAL|HSM_RTC_CLK_GAT<br>E|RTC|
||1|XTALCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|RCCLK10M|||||
||5|RCCLK10M|||||
||6|EXT_REFCLK|||||
||7|RCCLK32K|||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 301 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

**Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|---|
|HSM_DMTA_CLK_M<br>UX|0|XTALCLK|HSM_DMTA_CLK_SR<br>C_SEL|HSM_DMTA_CLK_DI<br>V_VAL|HSM_DMTA_CLK_GA<br>TE|DMTA|
||1|XTALCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|RCCLK10M|||||
||5|RCCLK10M|||||
||6|EXT_REFCLK|||||
||7|RCCLK32K|||||
|HSM_DMTB_CLK_M<br>UX|0|XTALCLK|HSM_DMTB_CLK_SR<br>C_SEL|HSM_DMTB_CLK_DI<br>V_VAL|HSM_DMTB_CLK_G<br>ATE|DMTB|
||1|XTALCLK|||||
||2|SYS_CLK|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|RCCLK10M|||||
||5|RCCLK10M|||||
||6|EXT_REFCLK|||||
||7|RCCLK32K|||||
|CONTROLSS_PLL_C<br>LK_MUX|0|XTALCLK|CONTROLSS_PLL_C<br>LK_SRC_SEL|CONTROLSS_PLL_C<br>LK_DIV_VAL|CONTROLSS_PLL_C<br>LK_GATE|ControlSS|
||1|EXT_REFCLK|||||
||2|DPLL_CORE_HSDIV0_CLKOUT2|||||
||3|DPLL_PER_HSDIV0_CLKOUT1|||||
||4|DPLL_CORE_HSDIV0_CLKOUT0|||||
||5|RCCLK10M|||||
||6|XTALCLK|||||
||7|RCCLK10M|||||
|NA|DPLL_CORE_HSDIV0_CLKOUT1||NA|RGMII_250_CLK_DIV<br>_VAL|RGMII_250_CLK_GA<br>TE|CPSW|
|NA|DPLL_CORE_HSDIV0_CLKOUT1||NA|RGMII_50_CLK_DIV_<br>VAL|RGMII_50_CLK_GAT<br>E|CPSW|



302 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## **Table 6-29. Configuration Options (continued)** 

|**Clock Muxes**|**Clock Sources**|**MMR Select**|**MMR Divider Select**|**MMR Clock Gate**|**IP's**|
|---|---|---|---|---|---|
|NA|DPLL_CORE_HSDIV0_CLKOUT1|NA|RGMII_5_CLK_DIV_V<br>AL|RGMII_5_CLK_GATE|CPSW|
|NA|XTALCLK|NA|XTAL_MMC_32K_CL<br>K_DIV_VAL|MMC0_32K_CLK_GA<br>TE|MMC 32K|
|NA|XTALCLK|NA|XTAL_TEMPSENSE_<br>32K_CLK_DIV_VAL|TEMPSENSE_32K_C<br>LK_GATE|Temp Sensor|
|NA|SYS_CLK|NA|MSS_ELM_CLK_DIV_<br>VAL|MSS_ELM_CLK_GAT<br>E|MSS|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

303 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.4.4 Clock Gating**_ 

Clock gating on all the root clocks is Software controller through MMR, <IP>_CLK_GATE. There is no clock stop protocol implemented in the IPs and hence, software has the responsibility to gate the root clocks when the IP is idle. 

## _**6.4.5 Monitoring SYS_CLK**_ 

SYS_CLK is the main clock in the system. This clock is needed for the proper functioning of DCC, CPU, Interconnect as well as the ESM (Error Signaling module). If this clock freezes, then everything in the chip stops working, including the CPU. 

The recommended way to monitor this scenario is to do the following: 

1. Configure the ESM in PWM mode so that ERROR pin can continuously toggle when in normal mode. See Error Signaling Module (ESM) chapter for more details on this. 

2. Implement a Toggle monitor in the external PMIC or a safety monitor. 

3. Whenever ESM detects an internal ERROR, this signal stops toggling. 

4. When the SYS_CLK fails, the ESM stops receiving a clock and this too has the effect of stopping ERROR pin toggle. Hence, the external safety monitor can take appropriate action in this scenario. 

## _**6.4.6 Limp Mode**_ 

A dedicated coarse clock loss logic checks the XTAL clock against the RC CLK continuously to detect if the XTAL clock is toggling. 

When this module detects a clock error on XTAL Clock, the error signal is routed to the GCM’s to activate the Limp mode. When the limp mode is activated, all the GCM switch to RCCLK (clk source #5). This ensures the CPU continues to operate even if the XTAL Clock fails and can take the system to a safe state. 

Switch to Limp mode feature is not enabled by default. The feature needs to be explicitly enabled by S/W by TOP_RCM.LIMP_MODE_EN.XTALCLK_LOSS_EN 

In addition, error on DCC0 and CORE_PLL Phase lock loss can also trigger Limp-mode for added safety. This feature can be enabled by the bits TOP_RCM.LIMP_MODE_EN.COREPLL_LOSS_EN and TOP_RCM.LIMP_MODE_EN.DCC0_ERROR_EN 

## **Note** 

RC_CLK is not an accurate clock and hence the performance of the system is not guaranteed in Limp mode. 

304 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.4.7 Clocking Registers**_ 

For additional details related to device clocking registers, please refer to the _Control Module - MSS_RCM Registers_ section of the Register Addendum. 

## _**6.4.8 Programming Guide**_ 

## **Note** 

PLL and Root Clock configuration MMRs are present inside the TOP_RCM module. 

## **6.4.8.1 PLL and Root Clocks Programming Guide** 

## _**6.4.8.1.1 PLL Configurations**_ 

## **Note** 

This section describes the sequence in order to configure both the CORE_PLL and PER_PLL. For information on PLL configuration during boot, please refer to PLL Configuration. 

## _**6.4.8.1.1.1 Kick Protection Mechanism**_ 

The registers corresponding to the PLLs are present in TOP_RCM. Before accessing any register in MSS_RCM and TOP_RCM memory map, unlock the corresponding LOCK_KICK config registers with the following values: 

1. LOCK0_KICK0.LOCK0_KICK0 = 0x01234567 

2. LOCK0_KICK1.LOCK0_KICK1 = 0x0FEDCBA8 

The above unlock procedure should be repeated for CONTROLSS_CTRL before configuring any MMRs in that region. 

After these two steps a write access to the PLL registers is allowed. Writing any other data value to either of these two registers locks the kicker mechanism and blocks any writes to the PLL registers. 

Refer to the Control MMR chapter for more details on locking. 

## **Note** 

In order to ensure that all PLL registers are write protected, software must always re-lock the kicker mechanism after completing the register writes. 

## _**6.4.8.1.1.2 Sequence to Configure the CORE PLL**_ 

1. Check for the CRYSTAL present status from TOP_RCM.CLK_LOSS_STATUS.CRYSTAL_CLOCK_LOSS register in TOP_RCM before proceeding further in configuring the _PLL_ 

2. If the CRYSTAL is not present then abort the _PLL_ lock procedure and continue with RC_CLK for boot 

3. Program the N divider of the _PLL_ with the calculated value of 0x9 in register field in order to get _REF_CLK_ suitable for _PLL_ locking, TOP_RCM.PLL_CORE_M2NDIV.N = 0x09 

4. Program the M2 divider with the value of 0x1 in the register field to get the desired frequency after PLL locking, TOP_RCM.PLL_CORE_M2NDIV.M2 = 0x1 

5. Update the M divider setting of the _PLL_ with the value which is derived from the above formula, TOP_RCM.PLL_CORE_MN2DIV.M = 0x360 

6. Update the SELFREQDCO value based on the frequency of CLKDCOLDO 

   - a. TOP_RCM.PLL_CORE_CLKCTRL.SELFREQDCO = 010b, if DCOCLK range is from 500 MHz to 1000MHz 

   - b. TOP_RCM.PLL_CORE_CLKCTRL.SELFREQDCO = 100b, if DCOCLK range is from 1000MHz to 2000MHz 

7. Program the SD divider of the PLL with the value of 0x8 to get the optimum jitter performance, TOP_RCM.PLL_CORE_FRACDIV.REGSD = 0x8 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

305 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

8. Clear the IDLE bit from PLL_CORE_CLKCTRL register to make the _PLL_ active for locking, TOP_RCM.PLL_CORE_CLKCTRL.IDLE= 0x0 

9. Assert the TENABLE signal to make the M, N, SD divider and SELFREQDCO settings to get loaded into the _PLL_ for locking, TOP_RCM.PLL_CORE_TENABLE.TENABLE = 0x1 

10. Assert the TINTZ signal of the _PLL_ to make the _PLL_ out of SOFT reset, TOP_RCM.PLL_CORE_CLKCTRL.TINTZ = 0x1 

11. De-assert the TENABLE signal by clearing the register with the value of 0x0, TOP_RCM.PLL_CORE_TENABLE.TENABLE = 0x0 

12. Assert and de-assert the TENABLEDIV signal of the _PLL_ by setting and clearing its corresponding register field, 

TOP_RCM.PLL_CORE_TENABLEDIV.TENABLEDIV = 0x1 

TOP_RCM.PLL_CORE_TENABLEDIV.TENABLEDIV = 0x0 

13. Wait for the _PLL_ to lock by polling the PHASELOCK bit to go high in the status register, TOP_RCM.PLL_CORE_STATUS.PHASELOCK = 0x1 

14. Program the divider settings of the various PLL CORE HSDIVDER CLKOUT in their corresponding register field depending on the required output frequency, 

TOP_RCM.PLL_CORE_HSDIVIDER_CLKOUT0.DIV = 0x04 (i.e. 400MHz) 

TOP_RCM.PLL_CORE_HSDIVIDER_CLKOUT1.DIV = 0x03 (i.e. 500MHz) 

TOP_RCM.PLL_CORE_HSDIVIDER_CLKOUT2.DIV = 0x04 (i.e. 400MHz) 

15. Assert and de-assert the TENABLEDIV signal of the PLL CORE HSDIVER by setting and clearing the corresponding register field, 

TOP_RCM.PLL_CORE_HSDIVIDER.TENABLEDIV = 0x1 

TOP_RCM.PLL_CORE_HSDIVIDER.TENABLEDIV = 0x0 

16. Un-gate the clocks from all CLKOUT of PLL CORE HSDIVDER with the following configuration, 

TOP_RCM.PLL_CORE_HSDIVIDER_CLKOUT0.GATE_CTRL = 0x1 

TOP_RCM.PLL_CORE_HSDIVIDER_CLKOUT1.GATE_CTRL = 0x1 

TOP_RCM.PLL_CORE_HSDIVIDER_CLKOUT2.GATE_CTRL = 0x1 

## **Note** 

Note that PLL_CORE_HSDIVIDER.TENABLEDIV and PLL_CORE_TENABLE.TENABLE reference TENABLE fields in different registers. Make sure to address the correct registers when loading the M, N, SD dividers and SELFREQDCO settings and also when loading the HSDIVIDER values. 

## _**6.4.8.1.1.3 Sequence to Configure the PER PLL**_ 

The configuration sequence used for locking the CORE _PLL_ (point 3 to 12) to be followed along with calculated values which is dependent on PER _PLL_ lock frequency is programmed in the registers available for PER _PLL_ inside TOP_RCM memory map for locking the PERIPHERAL PLL. 

For PLL PER HSDIVDER settings follow the sequence below, 

1. Program the divider settings of the various PLL PER HSDIVDER CLKOUT in their corresponding register field depending on the required output frequency, 

TOP_RCM.PLL_PER_HSDIVIDER_CLKOUT0.DIV= 0x0B (i.e. 160MHz) 

TOP_RCM.PLL_PER_HSDIVIDER_CLKOUT1.DIV = 0x09 (i.e. 192MHz) 

2. Assert and de-assert the TENABLEDIV signal of the PLL PER HSDIVER by setting and clearing the TOP_RCM.PLL_PER_HSDIVIDER.TENABLEDIV register field, 

306 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

TOP_RCM.PLL_PER_HSDIVIDER.TENABLEDIV = 0x1 

TOP_RCM.PLL_PER_HSDIVIDER.TENABLEDIV = 0x0 

3. Un-gate the clocks from all CLKOUT of PLL PER HSDIVDER with the following configuration, 

TOP_RCM.PLL_PER_HSDIVIDER_CLKOUT0.GATE_CTRL = 0x1 

TOP_RCM.PLL_PER_HSDIVIDER_CLKOUT1.GATE_CTRL = 0x1 

## **Note** 

1. For faster PLL locking, configure the PLL settings (point 3 to 11) of both PLL’s before polling for the lock of the corresponding PLL 

2. For PLL lock using _EXT_REF_ clock, configure the PLL_REF_CLK_SRC_SEL.PLL_CORE_REF_CLK_SRC_SEL (or) 

PLL_REF_CLK_SRC_SEL.PLL_PER_REF_CLK_SRC_SEL register fields in TOP_RCM before staring the PLL configurations 

3. Configure the _DCC_ with reference clock as CRYSTAL and compare clock as _PLL_CORE_CLKOUT1_ to measure the frequency range before switching the _SYS_CLK_ / R5 CLK to PLL clock. Refer _DCC_ chapter for more information in its configuration and usage (Note - Optional configuration only used for safety purpose) 

## _**6.4.8.1.1.4 Sequence to Re-Configure the PLL**_ 

The following section provides details of steps involved in re-configuring the PLL with new frequency: 

1. Switch all the peripheral clocks which are derived from PLL to WUCPU_CLK (XTAL_CLK) so that when PLL is unlocked other peripheral are in safe state. (Refer to the IP Clock Configurations section for programming.) 

2. Change the CPU clock source to WUCPU_CLK (XTAL_CLK) by programming the R5SS GCM with the value of 0x0 and SYS_CLK GCD (optional) with the value of 0x0 so that CPU does not enter into dead lock condition. (Refer to the Root Clock Configurations for programming.) 

3. Assert the TINTZ signal of the PLL to reset the internal FSM of PLL, TOP_RCM.PLL_CORE_CLKCTRL.TINTZ = 0x0. 

4. Follow the steps mentioned in Sequence to Configure the CORE PLL from point 3 to 12 to re-configure the PLL CORE. 

## **Note** 

Follow the above-mentioned steps except point (2) to re-configure the PLL PER. 

## _**6.4.8.1.2 Root Clock Configurations**_ 

## _**6.4.8.1.2.1 Sequence for Programming SYS and R5 Clocks**_ 

1. Program SYS CLK _GCD_ register with the value of 0x111 in-order to switch to a new desired frequency, TOP_RCM.SYS_CLK_DIV_VAL.CLKDIV = 0x111 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, TOP_RCM.SYS_CLK_STATUS. CURRDIVIDER = 0x1 

3. If the R5 clock frequency needs to be same as SYS clock frequency, then program the TOP_RCM.R5SS0_CLK_DIV_SEL.CLKDIVSEL = 0x7 (or / and) TOP_RCM.R5SS1_CLK_DIV_SEL.CLKDIVSEL = 0x7 register(s) as required or else leave with default value of 0x0 without any programming 

4. After the divider configuration, update the R5SS _GCM_ register with the value of 0x222 to select the PLL_CORE_CLOCKOUT0 as its source, TOP_RCM.R5SS_CLK_SRC_SEL.CLKSRCSEL= 0x222 

5. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, TOP_RCM.R5SS_CLK_STATUS.CLKINUSE = 0x04 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 307 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.4.8.1.2.2 Sequence for Programming TRACE Clock**_ 

1. Program TRCCLKOUT _GCD_ register with the value of 0x111 in-order to switch to a new desired frequency, TOP_RCM.TRCCLKOUT_DIV_VAL.CLKDIV = 0x111 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, TOP_RCM.TRCCLKOUT_CLK_STATUS.CURRDIVIDER = 0x01 

3. Update the TRCCLKOUT _GCM_ register with the value of 0x222 to select _PLL_CORE_CLKOUT1_ as its source, TOP_RCM.TRCCLKOUT_CLK_SRC_SEL.CLKSRCSEL = 0x222 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, TOP_RCM.TRCCLKOUT_CLK_STATUS.CLKINUSE = 0x04 

## _**6.4.8.1.2.3 Sequence for Programming CLKOUT Clock**_ 

1. Program CLKOUT0 _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, TOP_RCM.CLKOUT0_DIV_VAL.CLKDIV = 0x111 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, TOP_RCM.CLKOUT0_CLK_STATUS.CURRDIVIDER = 0x01 

3. Update the CLKOUT0 _GCM_ register with the value of 0x222 to select _PLL_CORE_CLKOUT1_ as its source, TOP_RCM.CLKOUT0_CLK_SRC_SEL.CLKSRCSEL = 0x222 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, TOP_RCM.CLKOUT0_CLK_STATUS.CLKINUSE = 0x04 

## **6.4.8.2 IP Clock Configurations** 

<IP>_CLK_SRC_SEL controls the select pin of the corresponding clock GCM. The GCM can take several clock cycles before the clock switch is made. The status of the switch is available on <IP>_CLK_STATUS.CLKINUSE. 

<IP>_CLK_DIV_VALcontrols the divider value of the Glitch free divider. The GCD takes several clock cycles before the division takes effect. The status can be observed at <IP>_CLK_STATUS. CURRDIVIDER. The status is reflected only if the clock input to the GCD is available. 

## **Note** 

IP Clock configuration MMRs are present inside the MSS_RCM module. 

## _**6.4.8.2.1 RTI CLOCK**_ 

(FREQ = 200MHz ) 

1. Program RTIx _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, MSS_RCM.RTIx_CLK_DIV_VAL.CLKDIV = 0x000 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.RTIx_CLK_STATUS.CURRDIVIDER = 0x00 

3. Update the RTI0 CLK _GCM_ register with the value of 0x222 to select _SYS_CLK_ as its source, MSS_RCM.RTIx_CLK_SRC_SEL.CLKSRCSEL = 0x222 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.RTIx_CLK_STATUS.CLKINUSE = 0x04 

## _**6.4.8.2.2 WDT CLOCK**_ 

(FREQ = 200MHz ) 

1. Program WDTx _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, MSS_RCM.WDTx_CLK_DIV_VAL.CLKDIV = 0x000 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.WDTx_CLK_STATUS.CURRDIVIDER = 0x0 

3. Update the MSS WDT0 _GCM_ register with the value of 0x222 to select _SYS_CLK_ as its source, MSS_RCM.WDTx_CLK_SRC_SEL.CLKSRCSEL = 0x222 

308 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.WDTx_CLK_STATUS.CLKINUSE = 0x04 

## _**6.4.8.2.3 OSPI CLOCK**_ 

(FREQ = 133MHz, note – ROM is utilizing OSPI0 @ 33 or 50MHz so program the _GCD_ correspondingly) 

1. Program OSPI0 _GCD_ register with the value of 0x222 in-order to switch to a new desired frequency, MSS_RCM.OSPI0_CLK_DIV_VAL.CLKDIV = 0x222 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.OSPI0_CLK_STATUS.CURRDIVIDER = 0x2 

3. Update the OSPI0 _GCM_ register with the value of 0x444 to select _PLL_CORE_CLKOUT0_ clock as its source, MSS_RCM.OSPI0_CLK_SRC_SEL.CLKSRCSEL = 0x444 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.OSPI0_CLK_STATUS.CLKINUSE = 0x10 

Baud rate relationship with OSPI functional clock frequency: 

Baud rate = fOSPI / DCLK_DIV 

Where fOSPI – OSPI Functional clock frequency DCLK_DIV – Prescalar clock divider 

## _**6.4.8.2.4 MCSPI CLOCK**_ 

(FREQ = 50MHz, Baud rate = 50Mbps) 

1. Program MCSPIx _GCD_ register with the value of 0x777 in-order to switch to a new desired frequency, MSS_RCM.MCSPIx_CLK_DIV_VAL.CLKDIV = 0x777 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.MCSPIx_CLK_STATUS.CURRDIVIDER = 0x07 

3. Update the MCSPIx _GCM_ register with the value of 0x444 to select _PLL_CORE_CLKOUT0_ clock as its source, MSS_RCM.MCSPIx_CLK_SRC_SEL.CLKSRCSEL = 0x444 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.MCSPIx_CLK_STATUS.CLKINUSE = 0x8 

5. Program the CLKD field from the required channel config register of the corresponding instance with the value of 0x1, MCSPIx.CHxCONF.CLKD = 0x1 

(FREQ = 48MHz, Baud rate = 48Mbps) 

1. Program MCSPIx _GCD_ register with the value of 0x333 in-order to switch to a new desired frequency, MSS_RCM.MCSPIx_CLK_DIV_VAL.CLKDIV = 0x333 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.MCSPIx_CLK_STATUS.CURRDIVIDER = 0x03 

3. Update the MCSPI0 _GCM_ register with the value of 0x333 to select _PLL_PER_CLKOUT1_ clock as its source, MSS_RCM.MCSPIx_CLK_SRC_SEL.CLKSRCSEL = 0x333 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.MCSPIx_CLK_STATUS.CLKINUSE = 0x08 

5. Program the CLKD field from the required channel config register of the corresponding instance with the value of 0x1, MSS_RCM.MCSPIx.CHxCONF.CLKD = 0x1 

Baud rate relationship with MCSPI functional clock frequency, 

Baud rate = fSPI / CLKD 

Where fSPI – SPI Functional clock frequency CLKD – Prescalar clock divider 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

309 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.4.8.2.5 I2C CLOCK**_ 

(FREQ = 48MHz, Baud rate = 400KHz) 

1. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.I2C_CLK_STATUS.CURRDIVIDER = 0x04 (In MODE2 devices) 

2. Update the I2C _GCM_ register with the value of 0x333 to select _PLL_PER_CLKOUT1_ as its source, MSS_RCM.I2C_CLK_SRC_SEL.CLKSRCSEL = 0x333 

3. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.I2C_CLK_STATUS.CLKINUSE = 0x08 

4. Program ICCL15_ICCL0 field of ICCLKL register of the corresponding I2C instance with calculated value of 0x35 to attain the 400KHz baud rate, MSS_I2Cx.ICCLKL. ICCL15_ICCL0 = 0x35 

5. Program ICCL15_ICCH0 field of ICCLKH register of the corresponding I2C instance with calculated value of 0x35 to attain the 400KHz baud rate, MSS_I2Cx.ICCLKH. ICCL15_ICCH0 = 0x35 

Baud rate relationship with I2C functional clock frequency, 

SCL_LOW_PERIOD = [fI2C] * [IPSC+1] * [ICCLKL + d] 

SCL_HIGH_PERIOD = [fI2C] * [IPSC+1] * [ICCLKH + d] 

where fI2C – I2C functional clock frequency, 

IPSC – Prescalar value 

d – Constant w.r.t to prescaler (IPSC = 0,6 then d = 7, IPSC = 1,5 then d = 6) ICCLKL – I2C clock low divider 

ICCLKH – I2C clock high divider 

## _**6.4.8.2.6 LIN_UART CLOCK**_ 

(FREQ = 192MHz) 

1. Program LIN_UART _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, MSS_RCM.LINx_UARTx_CLK_DIV_VAL.CLKDIV = 0x000 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.LINx_UARTx_CLK_STATUS.CURRDIVIDER = 0x00 

3. Update the LIN_UART _GCM_ register with the value of 0x333 to select _PLL_PER_CLKOUT1_ as its source, MSS_RCM.LINx_UARTx_CLK_SRC_SEL.CLKSRCSEL = 0x333 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.LINx_UARTx_CLK_STATUS.CLKINUSE = 0x08 

## (FREQ = 160MHz) 

1. Program LIN_UART _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, MSS_RCM.LINx_UARTx_CLK_DIV_VAL.CLKDIV = 0x000 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.LINx_UARTx_CLK_STATUS.CURRDIVIDER = 0x00 

3. Update the LIN_UART _GCM_ register with the value of 0x777 to select _PLL_PER_CLKOUT0_ as its source, MSS_RCM.LINx_UARTx_CLK_SRC_SEL.CLKSRCSEL = 0x777 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.LINx_UARTx_CLK_STATUS.CLKINUSE = 0x80 

For LIN, Baud rate = 20 Kbps then functional clock = 48MHz 

1. Program SCI_LIN_PSL field of BRSR register of the corresponding LIN instance with calculated value of 0x95 to attain the required baud rate, MSS_LINx.BRSR.SCI_LIN_PSL = 0x95 

Baud rate relationship with LIN functional clock frequency, 

Baud rate = fLIN / [16 * (P + 1 + M/16)] 

310 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

Where FLIN – LIN Functional clock 

P – Prescalar to select baudrate 

M – Prescalar for fine tuning of baudrate 

For UART, Baud rate = 12 Mbps then functional clock = 192MHz, 

Baud rate = 10 Mbps then functional clock = 160MHz 

1. Program CLOCK_LSB field of DLL register of the corresponding UART instance with calculated value of 0x1 to attain the required baud rate, MSS_UARTx.DLL.CLOCK_LSB = 0x1 

2. Program CLOCK_MSB field of DLH register of the corresponding UART instance with calculated value of 0x0 to attain the required baud rate, MSS_UARTx.DLH.CLOCK_MSB = 0x0 

Baud rate relationship with LIN functional clock frequency, 

Baud rate = fUART / [16 * DIV] 

Where FUART – UART Functional clock DIV – Prescalar clock divider 

## _**6.4.8.2.7 ICSSM UART CLOCK**_ 

(FREQ = 192MHz) 

1. Program ICSSM UART _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, MSS_RCM.ICSSMx_UARTx_CLK_DIV_VAL.CLKDIV = 0x000 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.ICSSMx_UARTx_CLK_STATUS.CURRDIVIDER = 0x00 

3. Update the ICSSM UART _GCM_ register with the value of 0x333 to select _PLL_PER_CLKOUT1_ as its source, MSS_RCM.ICSSMx_UARTx_CLK_SRC_SEL.CLKSRCSEL = 0x333 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.ICSSMx_UARTx_CLK_STATUS.CLKINUSE = 0x08 

## _**6.4.8.2.8 MCAN CLOCK**_ 

(FREQ = 80MHz, Baud Rate = 8 Mbps) 

1. Program MCAN _GCD_ register with the value of 0x444 in-order to switch to a new desired frequency, MSS_RCM.MCANx_CLK_DIV_VAL.CLKDIV = 0x444 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.MCANx_CLK_STATUS.CURRDIVIDER = 0x04 

3. Update the MCANx _GCM_ register with the value of 0x444 to select _PLL_CORE_CLKOUT0_ as its source, MSS_RCM.MCANx_CLK_SRC_SEL.CLKSRCSEL = 0x444 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.MCANx_CLK_STATUS.CLKINUSE = 0x10 

5. Program NBRP field of the NBTP register of the corresponding CAN instance with the calculated value of 0x0 to achieve the required baud rate of 8Mbps, MSS_MCANx.NBTP. NBRP = 0x0 

6. Program NTSEG1 field of the NBTP register of the corresponding CAN instance with the value calculated from the formula to achieve the required baud rate, MSS_MCANx.NTSEG1.NBRP = 0x1 

7. Program NTSEG2 field of the NBTP register of the corresponding CAN instance with the value calculated from the formula to achieve the required baud rate, MSS_MCANx.NTSEG2.NBRP = 0x1 

Baud rate relationship with CAN functional clock frequency, 

Baud rate = fCAN / [2 * (BRP +1) * (3 + TSEG1 + TSEG2)] 

Where fCAN – MCAN Functional clock frequency BRP – Baudrate prescaler TSEG1 – Time segment before sample point TSEG2 – Time segment after sample point 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 311 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.4.8.2.9 MMCx CLOCK**_ 

(FREQ = 50MHz) 

1. Program MMCSD _GCD_ register with the value of 0x333 in-order to switch to a new desired frequency, MSS_RCM.MMCx_CLK_DIV_VAL.CLKDIV = 0x333 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.MMCx_CLK_STATUS.CURRDIVIDER = 0x03 

3. Update the MMCx _GCM_ register with the value of 0x222 to select _SYSCLK_ as its source, MSS_RCM.MMCx_CLK_SRC_SEL.CLKSRCSEL = 0x222 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.MMCx_CLK_STATUS.CLKINUSE = 0x04 

## (FREQ = 48MHz) 

1. Program MMCSD _GCD_ register with the value of 0x333 in-order to switch to a new desired frequency, MSS_RCM.MMCx_CLK_DIV_VAL.CLKDIV = 0x333 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.MMCx_CLK_STATUS.CURRDIVIDER = 0x03 

3. Update the MMCx _GCM_ register with the value of 0x333 to select _PLL_PER_CLKOUT1_ as its source, MSS_RCM.MMCx_CLK_SRC_SEL.CLKSRCSEL = 0x333 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.MMCx_CLK_STATUS.CLKINUSE = 0x08 

## _**6.4.8.2.10 CPTS CLOCK**_ 

(FREQ = 250MHz) 

1. Program CPTS _GCD_ register with the value of 0x111 in-order to switch to a new desired frequency, MSS_RCM.CPTS_CLK_DIV_VAL.CLKDIV = 0x111 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.CPTS_CLK_STATUS.CURRDIVIDER = 0x01 

3. Update the CPTS _GCM_ register with the value of 0x333 to select _PLL_CORE_CLKOUT1_ as its source, MSS_RCM.CPTS_CLK_SRC_SEL.CLKSRCSEL = 0x333 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.CPTS_CLK_STATUS.CLKINUSE = 0x08 

## _**6.4.8.2.11 HSM RTI CLOCK**_ 

(FREQ = 200MHz ) 

1. Program HSM RTI _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, MSS_RCM.HSM_RTI_CLK_DIV_VAL.CLKDIV = 0x000 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.HSM_RTI_CLK_STATUS.CURRDIVIDER = 0x00 

3. Update the HSM RTI _GCM_ register with the value of 0x222 to select _SYS_CLK_ as its source, MSS_RCM.HSM_RTI_CLK_SRC_SEL.CLKSRCSEL = 0x222 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.HSM_RTI_CLK_STATUS.CLKINUSE = 0x04 

## _**6.4.8.2.12 HSM WDT CLOCK**_ 

(FREQ = 200MHz ) 

1. Program HSM WDT _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, MSS_RCM.HSM_WDT_CLK_DIV_VAL.CLKDIV = 0x000 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.HSM_WDT_CLK_STATUS.CURRDIVIDER = 0x00 

312 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

3. Update the HSM WDT _GCM_ register with the value of 0x222 to select _SYS_CLK_ as its source, MSS_RCM.HSM_WDT_CLK_SRC_SEL.CLKSRCSEL = 0x222 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.HSM_WDT_CLK_STATUS.CLKINUSE = 0x04 

## _**6.4.8.2.13 HSM RTC CLOCK**_ 

(FREQ = 200MHz ) 

1. Program HSM RTC _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, MSS_RCM.HSM_RTC_CLK_DIV_VAL.CLKDIV = 0x000 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.HSM_RTC_CLK_STATUS.CURRDIVIDER = 0x00 

3. Update the HSM RTC _GCM_ register with the value of 0x222 to select SYS_CLKas its source, MSS_RCM.HSM_RTC_CLK_SRC_SEL.CLKSRCSEL = 0x222 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, It should read HSM_RTC_CLK_STATUS.CLKINUSE = 0x04 

## _**6.4.8.2.14 HSM DMTA CLOCK**_ 

(FREQ = 200MHz) 

1. Program HSM DMTA _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, MSS_RCM.HSM_DMTA_CLK_DIV_VAL.CLKDIV = 0x000 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.HSM_DMTA_CLK_STATUS.CURRDIVIDER = 0x00 

3. Update the HSM DMTA _GCM_ register with the value of 0x222 to select _SYS_CLK_ as its source, MSS_RCM.HSM_DMTA_CLK_SRC_SEL.CLKSRCSEL = 0x222 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.HSM_DMTA_CLK_STATUS.CLKINUSE = 0x04 

## _**6.4.8.2.15 HSM DMTB CLOCK**_ 

(FREQ = 200MHz ) 

1. Program HSM DMTB _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, MSS_RCM.HSM_DMTB_CLK_DIV_VAL.CLKDIV = 0x000 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.HSM_DMTB_CLK_STATUS.CURRDIVIDER = 0x00 

3. Update the HSM DMTB _GCM_ register with the value of 0x222 to select _SYS_CLK_ as its source, MSS_RCM.HSM_DMTB_CLK_SRC_SEL.CLKSRCSEL = 0x222 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, MSS_RCM.HSM_DMTB_CLK_STATUS.CLKINUSE = 0x04 

## _**6.4.8.2.16 CONTROLSS PLL CLOCK**_ 

(FREQ = 400MHz 

1. Program CONTROLSS PLL CLOCK _GCD_ register with the value of 0x000 in-order to switch to a new desired frequency, MSS_RCM.CONTROLLSS_PLL_CLK_DIV_VAL.CLKDIVR = 0x000 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, It should read CONTROLLSS_PLL_CLK_STATUS.CURRDIVIDER = 0x00 

3. Update the CONTROLSS _GCM_ register with the value of 0x222 to select _PLL_CORE_CLKOUT2_ as its source, MSS_RCM.CONTROLSS_PLL_CLK_SRC_SEL.CLKSRCSEL = 0x222 

4. Poll for the CLKINUSE field of corresponding status register to reflect its new frequency change, It should read MSS_RCM.CONTROLLSS_PLL_CLK_STATUS.CLKINUSE = 0x04 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 313 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.4.8.2.17 RGMII5 CLK**_ 

(FREQ = 5MHz, Default configuration) 

1. Program RGMII5 _GCD_ register with the value of 0x636363 to obtain a new desired frequency divided from _PLL_CORE_CLKOUT1_ , MSS_RCM.RGMII5_CLK_DIV_VAL.CLKDIV = 0x636363 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.RGMII5_CLK_STATUS.CURRDIVIDER = 0x63 

## _**6.4.8.2.18 RGMII50 CLK**_ 

(FREQ = 50MHz, Default configuration) 

1. Program RGMII50 _GCD_ register with the value of 0x999 to obtain a new desired frequency divided from _PLL_CORE_CLKOUT1_ , MSS_RCM.RGMII50_CLK_DIV_VAL.CLKDIV = 0x999 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.RGMII50_CLK_STATUS.CURRDIVIDER = 0x09 

## _**6.4.8.2.19 RGMII250 CLK**_ 

(FREQ = 250MHz, Default configuration) 

1. Program RGMII250 _GCD_ register with the value of 0x111 to obtain a new desired frequency divided from _PLL_CORE_CLKOUT1_ , MSS_RCM.RGMII_CLK_DIV_VAL.CLKDIV = 0x111 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.RGMII_CLK_STATUS.CURRDIVIDER = 0x01 

## _**6.4.8.2.20 XTAL MMC 32K CLOCK**_ 

(FREQ = 32 KHz, Default configuration) 

1. Program XTAL MMC 32K _GCD_ register with the value of 0x30CC330C to obtain a new desired frequency divided from XTAL_CLK, MSS_RCM.XTAL_MMC_32K_CLK_DIV_VAL.CLKDIV = 0x30CC330C 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.XTAL_MMC_32K _CLK_STATUS. CURRDIVIDER = 0x30C 

## **Note** 

Please refer to the register description in the AM263Px Sitara Processors Technical Reference Manual Register Addendum for a more detailed explanation on how to configure the XTAL MMC 32K Clock 

## _**6.4.8.2.21 XTAL TEMPSENSE 32K CLOCK**_ 

(FREQ = 32 KHz, Default configuration) 

1. Program XTAL TEMPSENSE 32K _GCD_ register with the value of 0x30CC330C to obtain a new desired frequency divided from XTAL_CLK, MSS_RCM.XTAL_TEMPSENSE_32K_CLK_DIV_VAL.CLKDIV = 0x30CC330C 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.XTAL_TEMPSENSE_32K_CLK_STATUS.CURRDIVIDER = 0x30C 

## **Note** 

Please refer to the register description in the AM263Px Sitara Processors Technical Reference Manual Register Addendum for a more detailed explanation on how to configure the XTAL TEMPSENSE 32K Clock 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

314 

Copyright © 2025 Texas Instruments Incorporated 

_Device Configuration_ 

www.ti.com 

## _**6.4.8.2.22 MSS_ELM CLOCK**_ 

(FREQ = 50MHz, Default configuration) 

1. Program MSS ELM _GCD_ register with the value of to obtain a new desired frequency divided from _SYS_CLK_ , MSS_RCM.MSS_LM_CLK_DIV_VAL.CLKDIV = 0x03 

2. Poll for the CURRDIVR field of corresponding status register to reflect its new frequency change, MSS_RCM.MSS_ELM_CLK_STATUS.CURRDIVIDER = 0x03 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

315 

Copyright © 2025 Texas Instruments Incorporated 

