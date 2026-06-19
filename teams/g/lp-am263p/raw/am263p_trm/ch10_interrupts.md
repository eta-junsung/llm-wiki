<!-- AM263P TRM | 10 Interrupts (VIM, routers) | 원본 p.952-1029 | pymupdf4llm text+tables, images omitted -->

_Interrupts_ 

www.ti.com 

_Chapter 10_ _**Interrupts**_ 

**==> picture [506 x 40] intentionally omitted <==**

This chapter describes the interrupts in the device. 

**10.1 Interrupt Architecture** .............................................................................................................................................953 **10.2 Interrupt Controllers** ...............................................................................................................................................953 **10.3 Interrupt Routers** .................................................................................................................................................... 961 **10.4 Interrupt Sources** ....................................................................................................................................................985 

952 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

## **10.1 Interrupt Architecture** 

The SoC has many peripherals and a large number of event sources including interrupts, time sync events, and DMA requests. The use of events is completely dependent on a user's specific application, which drives a need for maximum flexibility on which event sources are used in the system. Software control must be used to service these events. 

The SoC includes the following interrupt servicing modules (hosts): 

- 2x Real-time microcontroller units (R5FSS0, R5FSS1), each supporting: 

   - Dual-R5F Cluster 

   - Vectored interrupt manager (VIM) 

- Hardware Security Module (HSM) 

   - 

      - Single Arm Cortex-M4F core 

   - Nested vectored interrupt controller (NVIC) 

- Industrial communications subsystem (PRU-ICSS): 

   - Two programmable real-time units (PRUs) 

   - Local interrupt controller (INTC) 

Most of the system events are routed directly to the various processing elements but in some cases it is impractical to route all events of a certain group (for example, GPIO events) to each processing element. For this purpose, the SoC integrates several interrupt router (INTRTR) instances. Each interrupt router aggregates a number of system events and can route each event to a given processing element by using simple combinational logic (implemented via a set of multiplexors). Event selection is controlled through the associated registers within each interrupt router. 

The following interrupt router instances are part of the SoC interrupt architecture: 

- GPIO XBAR Interrupt Router (GPIO_XBAR_INTRTR0): 

   - Provides selection of active GPIO[0:3] module interrupts 

   - Supported by dedicated device GPIO muxing that provides virtualization 

- PRU-ICSS XBAR Interrupt Router (PRU_ICSS_XBAR_INTRTR0): 

   - Provides selection of active PRU-ICSS XBAR events for routing as processor interrupts or DMA events 

- EDMA Trigger XBAR Interrupt Router (EDMA_XBAR_INTRTR0): 

   - Provides selection of DMA Trigger events from various device peripherals 

In addition, the following interrupt router instances are part of the SoC time sync architecture: 

- Time Sync Event Router0 (SOC_TIMESYNC_XBAR0): 

   - See SOC_TIMESYNC_XBAR0 Overview 

- Time Sync Event Router1 (CONTROLSS_TIMESYNC_XBAR1): 

   - See SOC_TIMESYNC_XBAR1 Overview 

## **10.2 Interrupt Controllers** 

## _**10.2.1 Vectored Interrupt Manager (VIM)**_ 

## **10.2.1.1 VIM Overview** 

The VIM aggregates device interrupts and sends them to the R5F CPU(s). It can be used in either split or single-core configuration. In split, it has two independent interrupt cores, one per CPU. In lockstep, CPU1 acts as a diagnostic on CPU0; only CPU0’s outputs are used but all outputs are compared to CPU1 to provide diagnostic coverage. 

The VIM module supports the following features: 

- 256 interrupt inputs per R5F core 

- Each interrupt has its own 4-bit programmable priority 

   - Defined via the VIM_INTPRIORITY register 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

953 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

   - The VIM provides support for priority interruption of interrupts 

- Each interrupt has its own enable mask 

   - Interrupt enable is done via the MSS_VIM_INTR_EN_SET_j register 

   - 

   - Interrupt disable is done via the MSS_VIM_INTR_EN_CLR_j register 

- Each interrupt can be programmed as either an IRQ or FIQ 

   - Defined via the MSS_VIM_INTMAP_j register 

- Each interrupt has its own programmable 32-bit vector address associated with it 

   - Defined via the MSS_VIM_INTVECTOR register 

   - Protected with SECDED 

- One IRQn and one FIQn output per core 

- Vectored interrupt interface 

   - Compatible with R5F VIC port 

- Default vector provided when a double-bit error is detected 

- Split or single-core capable 

   - In single-core mode, only interrupts connected to VIM interrupt core 0 are available 

- Software interrupt generation 

## **10.2.1.2 VIM Interrupt Inputs** 

The VIM supports 256 interrupt inputs per core. Each interrupt can be either a level or a pulse (both active-high). The interrupt mapping for the two R5F cores can be found in _Interrupt Sources_ . 

## **10.2.1.3 VIM Interrupt Outputs** 

The VIM has two interrupt outputs per core: 

- _CoreN_IRQn_ : This is a normal interrupt for core _N_ (active-low level). It can be serviced via the VIC interface or through the MMR interface.Whenever an interrupt input goes high, if that interrupt is mapped as an IRQ (via the MSS_VIM_INTMAP_j register) and is enabled (via the MSS_VIM_INTR_EN_SET_j register), then it will cause an IRQ to assert 

- _CoreN_FIQn_ : This is a fast (or non-maskable) interrupt for core _N_ (active-low level). FIQs always have priority over IRQs. An FIQ can be serviced through the MMR interface. Whenever an interrupt input goes high, if that interrupt is mapped as an FIQ and is enabled, then it will cause an FIQ to assert 

## **10.2.1.4 VIM Interrupt Vector Table (VIM RAM)** 

For each VIM interrupt core, there is an associated interrupt vector table (VIM RAM) that is used to store the address of ISRs. During register vectored interrupt and hardware vectored interrupt, VIM accesses the interrupt vector table using the vector value to fetch the address of the corresponding ISR. Note that both interrupt vector tables are identical in their memory organization. 

The VIM RAM is basically comprised of a set of interrupt vector registers (MSS_VIM_INTVECTOR). Hence, the interrupt vector table is organized in 256 words of 30 bits, with a base address corresponding to the physical address of the first register in the group. 

## **Note** 

The lower two bits of the 32-bit interrupt vector are always 0s. 

Figure 10-1 shows the VIM RAM interrupt vector map. 

954 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**==> picture [206 x 219] intentionally omitted <==**

**----- Start of picture text -----**<br>
VIM RAM Address Space VIM RAM Entries<br>Base Address + 0h Interrupt 0 Vector<br>Base Address + 4h Interrupt 1 Vector<br>Base Address + 8h Interrupt 2 Vector<br>Base Address + 3F8h Interrupt 254 Vector<br>Base Address + 3FCh Interrupt 255 Vector<br>**----- End of picture text -----**<br>


**Figure 10-1. VIM RAM Interrupt Vector Map** 

The interrupt vector table has protection by ECC to indicate corruption due to soft errors. The ECC logic inside VIM supports SECDED. See Table 7-8 for the VIM RAM ID in the ECC aggregator map. 

## **10.2.1.5 VIM Interrupt Prioritization** 

The VIM supports the interruption of the currently active interrupt by one with a higher priority. FIQs and IRQs are completely separate but both use the same mechanism. 

## **Note** 

VIM priority scheme: 00 = Highest Priority - 15 = Lowest Priority 

When an interrupt goes from pending to active (FIQ: reading the MSS_VIM_FIQVEC register; IRQ: reading the MSS_VIM_IRQVEC register, or the _coreN_IRQACK_ going high), then the interrupt is loaded into the corresponding active register (MSS_VIM_ACTFIQ / MSS_VIM_ACTIRQ), and all interrupts of an equal or lesser priority are masked (discarded). If prior to this interrupt being cleared (by writing to the MSS_VIM_FIQVEC register, or MSS_VIM_IRQVEC register) another interrupt of higher priority arrives, then the FIQn/IRQn is asserted and that interrupt made pending as normal. If the CPU switches this interrupt to active (by reading the MSS_VIM_FIQVEC / MSS_VIM_IRQVEC register), then the currently active interrupt is pushed onto a stack. When an interrupt is cleared by reading the MSS_VIM_FIQVEC / MSS_VIM_IRQVEC register, if there are any interrupts on the stack, the first entry is popped off and put back into the MSS_VIM_ACTFIQ / MSS_VIM_ACTIRQ register, so that software retains original context and continues previous operation. 

## **Note** 

"Masked off" means that the registers are masked off from priority arbitration to interrupt the currently active interrupt, this does _not_ mean that the status bits in the registers are masked off. That is, this priority masking has NO EFFECT on whether the status bits are visible in the masked registers such as the Group M Interrupt Enabled Status/Clear Register. 

## **10.2.1.6 VIM ECC Support** 

The memory that holds the interrupt vector for each interrupt is protected by SECDED ECC. Single-bit errors are corrected and written back. Double-bit errors are not corrected. If a double-bit error occurs while trying to load a vector, then the MSS_VIM_DEDVEC register is used to provide the default vector for the _coreN_IRQADDRV_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 955 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

signal, the MSS_VIM_IRQVEC register, and the MSS_VIM_FIQVEC register. The MSS_VIM_DEDVEC should point to an ISR that handles the fact that there was an uncorrectable error in the interrupt handling. 

Some possible remediating actions would be to: 

1. Reconstruct the vector table and re-start the application a. Potentially switch to a completely software interrupt handler in the mean time 

2. Restart the application from scratch 

3. Reset the device 

4. Sit in a loop (or WFI) while something external (for example, the ESM) responds to the DED interrupt that will be generated 

It is up to the user and the application to determine the appropriate action. 

## **Note** 

An interrupt that has an uncorrectable vector error (and thus uses the DED vector) will still have the priority of the original interrupt (that is, for masking purposes). This makes it possible for a higher priority interrupt to supercede the handling of the error. 

Control and reporting are done by the R5FSS ECC aggregator. When in lockstep mode, only the RAM for CPU0 is used. 

## **10.2.1.7 VIM IDLE State** 

The VIM will indicate IDLE when there are no pending unmasked interrupts or MMR accesses. The VIM does not have a clock stop interface. 

## **10.2.1.8 VIM Interrupt Handling** 

There are multiple ways to service an interrupt depending on how much of the hardware assistance offered by the VIM the software wants to take advantage of. 

For IRQs, it is recommended to use the procedure in Section 10.2.1.8.1, but the procedures in Section 10.2.1.8.2 or Section 10.2.1.8.3 (if a user wants to implement a fully software prioritization scheme) may be used as alternatives. 

For FIQs, it is recommended to use the procedure in Section 10.2.1.8.4, but the procedure in Section 10.2.1.8.5 may be used as an alternative. 

## **Note** 

These descriptions do not include steps such as stack pushes and state retention that software must take in order to return from the ISR. It is assumed that the programmer is aware of these steps. 

## _**10.2.1.8.1 Servicing IRQ Through Vector Interface**_ 

If the associated CPU has the vector (VIC) interface enabled, then the following method is used for servicing IRQs: 

1. Hardware handshake 

   - a. CPU asserts _coreN_IRQACK_ high 

   - b. VIM asserts _coreN_IRQADDRV_ to indicate that the _coreN_IRQADDR_ bus is stable with the correct vector address 

   - c. CPU reads _coreN_IRQADDR_ , jumps to that address, and de-asserts _coreN_IRQACK_ low 

   - d. VIM de-asserts _coreN_IRQn_ and _coreN_IRQADDRV_ , VIM masks (discards) all IRQs with the same or lower priority 

956 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

   - e. VIM loads the value from the MSS_VIM_PRIIRQ[9:0] NUM bit field (which corresponds to the vector address) into the MSS_VIM_ACTIRQ[9:0] NUM bit field, which causes the MSS_VIM_ACTIRQ[31] VALID bit to be set 

2. Service the interrupt 

3. Depending on whether the original source of the interrupt was a pulse or a level (determined by reading the MSS_VIM_ACTIRQ[9:0] NUM bit field to determine number, and reading the appropriate bit in the MSS_VIM_INTTYPE_j register to determine type) 

   - a. Pulse 

      - i. Clear the status by writing a '1' to the appropriate bit in the MSS_VIM_IRQSTS_j register, or MSS_VIM_STS_j register 

      - ii. Clear the interrupt at the source. This way, the source can generate another pulse, if it needs to, and the VIM will process this as a new interrupt 

   - b. Level 

      - i. Clear the interrupt at the source 

      - ii. Clear the status by writing a '1' to the appropriate bit in the MSS_VIM_IRQSTS_j register, or MSS_VIM_STS_j register. This way, the level should be gone at the input to the VIM, it will avoid falsely re-calling the interrupt. If the source maintains the level, then it means there is another interrupt 

4. Write any value to the MSS_VIM_IRQVEC register 

   - a. This will clear the priority mask and will cause all interrupts to be re-evaluated for the new highest priority interrupt 

   - b. This will also clear the MSS_VIM_ACTIRQ[31] VALID bit 

## _**10.2.1.8.2 Servicing IRQ Through MMR Interface**_ 

When an IRQ interrupt is received, the CPU should follow these steps if not using the vector interface: 

1. Read the MSS_VIM_IRQVEC register and jump to that address to service the ISR 

   - a. Reading this register will mask (discard) all interrupts of an equal or lower priority and de-assert the _coreN_IRQn_ output. If another interrupt of a higher priority becomes available, the _coreN_IRQn_ will re-assert, allowing priority interruption of an interrupt 

   - b. Reading this register will cause the value from the MSS_VIM_PRIIRQ[9:0] NUM bit field to be loaded into the MSS_VIM_ACTIRQ[9:0] NUM bit field, and the MSS_VIM_ACTIRQ[31] VALID bit to be set 

2. Service the interrupt 

3. Depending on whether the original source of the interrupt was a pulse or a level 

   - a. Pulse 

      - i. Clear the status by writing a '1' to the appropriate bit in the MSS_VIM_STS_j register, or MSS_VIM_IRQSTS_j register 

      - ii. Clear the interrupt at the source 

   - b. Level 

      - i. Clear the interrupt at the source 

      - ii. Clear the status by writing a '1' to the appropriate bit in the MSS_VIM_STS_j register, or MSS_VIM_IRQSTS_j register 

4. Write any value to the MSS_VIM_IRQVEC register 

   - a. This will clear the priority mask and will cause all interrupts to be re-evaluated for the new highest priority interrupt 

   - b. This will also clear the MSS_VIM_ACTIRQ[31] VALID bit 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

957 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

## _**10.2.1.8.3 Servicing IRQ Through MMR Interface (Alternative)**_ 

If a user does not want to use the MSS_VIM_IRQVEC register, the VIM may be used as a more traditional interrupt controller. Note that in this mode, there is no hardware priority masking (because the MSS_VIM_IRQVEC register is never read). Software would be responsible for doing all priority operations. 

1. Determine which interrupt to service 

   - a. Read the MSS_VIM_PRIIRQ register to determine which interrupt is the highest priority IRQ currently asserted, OR 

   - b. Optionally read the MSS_VIM_IRQGSTS register to determine which groups have IRQs pending, then read the MSS_VIM_IRQSTS_j register and use a software prioritization scheme to determine which IRQ to service 

2. 

## Service the interrupt 

3. Depending on whether the original source of the interrupt was a pulse or a level 

   - a. Pulse 

      - i. Clear the status by writing a '1' to the appropriate bit in the MSS_VIM_STS_j register, or MSS_VIM_IRQSTS_j register 

      - ii. Clear the interrupt at the source. 

   - b. Level 

      - i. Clear the interrupt at the source 

      - ii. Clear the status by writing a '1' to the appropriate bit in the MSS_VIM_STS_j register, or MSS_VIM_IRQSTS_j register 

## _**10.2.1.8.4 Servicing FIQ**_ 

When an FIQ interrupt is received, the CPU should follow these steps: 

1. Read the MSS_VIM_FIQVEC register and jump to that address to service the ISR 

   - a. Reading this register will mask (discard) all interrupts of an equal or lower priority and de-assert the _coreN_FIQn_ output. If another interrupt of a higher priority becomes available, the _coreN_FIQn_ will re-assert, allowing priority interruption of an interrupt. 

   - b. Reading this register will cause the value from the MSS_VIM_PRIFIQ[9:0] NUM bit field to be loaded into the MSS_VIM_ACTFIQ[9:0] NUM bit field, and the MSS_VIM_ACTFIQ[31] VALID bit to be set 

2. Service the interrupt 

3. Depending on whether the original source of the interrupt was a pulse or a level (determined by reading the MSS_VIM_ACTFIQ[9:0] NUM bit field to determine number, and reading the appropriate bit in the MSS_VIM_INTTYPE_j register to determine type) 

   - a. Pulse 

      - i. Clear the status by writing a '1' to the appropriate bit in the MSS_VIM_STS_j register, or MSS_VIM_FIQSTS_j register 

      - ii. Clear the interrupt at the source. This way, the source can generate another pulse, if it needs to, and the VIM will process this as a new interrupt 

   - b. Level 

      - i. Clear the interrupt at the source 

      - ii. Clear the status by writing a '1' to the appropriate bit in the MSS_VIM_STS_j register, or MSS_VIM_FIQSTS_j register. This way, the level should be gone at the input to the VIM, it will avoid falsely re-calling the interrupt. If the source maintains the level, then it means there is another interrupt 

4. This will also clear the MSS_VIM_ACTFIQ[31] VALID bit 

   - a. This will clear the priority mask and will cause all interrupts to be re-evaluated for the new highest priority interrupt 

958 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

- b. This will also clear the MSS_VIM_ACTFIQ[31] VALID bit 

## _**10.2.1.8.5 Servicing FIQ (Alternative)**_ 

If a user does not want to use the MSS_VIM_FIQVEC register, the VIM may be used as a more traditional interrupt controller. Note that in this mode, there is no hardware priority masking (because the MSS_VIM_FIQVEC register is never read). Software would be responsible for doing all priority operations. 

1. Determine which interrupt to service 

   - a. Read the MSS_VIM_PRIFIQ register to determine which interrupt is the highest priority FIQ currently asserted, OR 

   - b. Optionally read the MSS_VIM_FIQGSTS register to determine which groups have IRQs pending, then read the MSS_VIM_FIQSTS_j register and use a software prioritization scheme to determine which FIQ to service 

2. Service the interrupt 

3. Depending on whether the original source of the interrupt was a pulse or a level 

   - a. Pulse 

      - i. Clear the status by writing a '1' to the appropriate bit in the MSS_VIM_STS_j register, or MSS_VIM_FIQSTS_j register 

      - ii. Clear the interrupt at the source. 

   - b. Level 

      - i. Clear the interrupt at the source 

      - ii. Clear the status by writing a '1' to the appropriate bit in the MSS_VIM_STS_j register, or MSS_VIM_FIQSTS_j register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

959 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

## _**10.2.2 Other Interrupt Controllers**_ 

All other device interrupt controllers are described in their respective chapters and/or third party documentation. 

960 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

## **10.3 Interrupt Routers** 

## _**10.3.1 INTRTR Overview**_ 

The interrupt router (INTRTR) module provides a mechanism to mux _M_ interrupt inputs to _N_ interrupt outputs, where all _M_ inputs are selectable to be driven per _N_ ouput. There is one register per output (MUXCNTL_N) that controls the selection. 

There are several INTRTR modules in the device. Their purpose is described in Section 10.1 , _Interrupt Architecture_ . Table 10-1 summarizes the configuration details for the various interrupt routers. 

**Table 10-1. INTRTR Modules Configuration** 

|**Module**|**Number of Inputs**|**Number of Outputs**|**Interrupt Type**|
|---|---|---|---|
|GPIO_XBAR_INTRTR0|180|301|Pulse|
|PRU_ICSS_XBAR_INTRTR0|74|16|Pulse|
|EDMA_XBAR_INTRTR0|260|64|Pulse|
|SOC_TIMESYNC_XBAR0|16|26|Pulse|
|SOC_TIMESYNC_XBAR1|28|201|Pulse|
|CONTROLSS_INTXBAR|186|32|Pulse|



1 - Only 4 outputs from GPIO_XBAR_INTRTR0 & SOC_TIMESYNC_XBAR1 connect to each VIM[3:0] instance 

CONTROLSS_INTXBAR is described in the CONTROLSS chapter and SOC_TIMESYNC_XBAR0, SOC_TIMESYNC_XBAR1 are captured in TimeSync Event Sources. 

The user should take the following into account when programming the MUXCNTL_N register: 

- Avoid programming this register when input interrupts are active. This can lead to spurious asynchronous output toggles which can lead to unpredictable behavior. 

- All mux control settings default to '0', which means that at reset no input interrupt will be propagated to any of the INTRTR outputs. This is due to the fact that the 0th input of all internal muxes is unused in the current implementation 

The recommended general programming sequence is as follows: 

1. Disable interrupt by writing '0' to the INT_ENABLE bit field. Do not change mux control configuration settings (ENABLE bit field) at this time. 

2. Change the mux control configuration settings. INT_ENABLE needs to remain '0' at this time. 

3. Enable interrupt by writing '1' to INT_ENABLE. Do not change mux control configuration settings at this time. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

961 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

## _**10.3.2 INTRTR Integration**_ 

This section describes the INTRTR integration in the device, including information about clocks, resets, and hardware requests. 

## **10.3.2.1 PRU-ICSS XBAR INTRTR0** 

There is 1x PRU-ICSS XBAR Interrupt Router module integrated in the device. The diagram below provides a visual representation of the device integration details for the PRU-ICSS XBAR Interrupt Router. 

## **PRU_ICSS_XBAR_INTRTR0** 

**==> picture [459 x 283] intentionally omitted <==**

**----- Start of picture text -----**<br>
2x5 LIN interrupts<br>1x6 USART interrupts<br>1x4 I2C interrupts<br>1x8 SPI interrupts<br>1x1 OSPI interrupts [15:0] x16 [15:0]<br>PRU-ICSS<br>PRU-ICSS<br>XBAR<br>13 EDMA requests<br>3x8 CAN interrupts<br>4 mailbox interrupts<br>4 GPIO_XBAR interrupts<br>**----- End of picture text -----**<br>


## **Figure 10-2. PRU-ICSS XBAR Interrupt Router Integration Diagram** 

The tables below summarize the device integration details of PRU-ICSS XBAR Interrupt router. 

## **Table 10-2. PRU-ICSS XBAR Interrupt router Device Integration** 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|PRU_ICSS_XBAR_INTRT<br>R0|✓|INFRA0 VBUSP Interconnect|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

962 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-3. PRU-ICSS_XBAR_INTRTR0 Clocks** 

|**Module**<br>**Instance**|**Module Clock in_intr**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|PRU_ICSS_<br>XBAR_INTR<br>TR0|SYSCLK|SYS_CLK|MSS_RCM|200 MHz|PRU_ICSS_XBAR_INTRT<br>R0 Fnctional and Interface<br>clock|



## **Table 10-4. PRU-ICSS_XBAR_INTRTR0 Resets** 

|**Module**<br>**Instance**|**Module Reset in_intr**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|PRU_ICSS<br>_XBAR_IN<br>TRTR0<br>|RST|SYS_RST|MSS_RCM<br>|PRU_ICSS_XBAR_INTRTR0 Reset|



**Table 10-5. PRU-ICSS_XBAR_INTRTR0 Output Hardware Requests** 

|**Module**<br>**Instance**|**Module XBAR**<br>**Output**|**Destination XBAR signal**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|PRU_ICSS_<br>XBAR_INTR<br>TR0|outl_intr_0|PR1_SLV_INTR_0|PRU-ICSS|Pulse|Selectable Hardware Request 0|
||outl_intr_1|PR1_SLV_INTR_1|||Selectable Hardware Request 1|
||outl_intr_2|PR1_SLV_INTR_2|||Selectable Hardware Request 2|
||outl_intr_3|PR1_SLV_INTR_3|||Selectable Hardware Request 3|
||outl_intr_4|PR1_SLV_INTR_4|||Selectable Hardware Request 4|
||outl_intr_5|PR1_SLV_INTR_5|||Selectable Hardware Request 5|
||outl_intr_6|PR1_SLV_INTR_6|||Selectable Hardware Request 6|
||outl_intr_7|PR1_SLV_INTR_7|||Selectable Hardware Request 7|
||outl_intr_8|PR1_SLV_INTR_8|||Selectable Hardware Request 8|
||outl_intr_9|PR1_SLV_INTR_9|||Selectable Hardware Request 9|
||outl_intr_10|PR1_SLV_INTR_10|||Selectable Hardware Request 10|
||outl_intr_11|PR1_SLV_INTR_11|||Selectable Hardware Request 11|
||outl_intr_12|PR1_SLV_INTR_12|||Selectable Hardware Request 12|
||outl_intr_13|PR1_SLV_INTR_13|||Selectable Hardware Request 13|
||outl_intr_14|PR1_SLV_INTR_14|||Selectable Hardware Request 14|
||outl_intr_15|PR1_SLV_INTR_15|||Selectable Hardware Request 15|



**Table 10-6. PRU_ICSS_XBAR_INTRTR0 in_intr Hardware Requests** 

|**Module Instance**|**Source Module**|**Source in_intr**<br>**signal**|**XBAR Module**<br>**in_intr**|**Type**|**Description**|
|---|---|---|---|---|---|
|PRU_ICSS_XBAR_IN<br>TRTR0|LIN0|lin0_intr_req0|IN_INTR0|Level|LIN0 Interrupt<br>Request 0|
||LIN0|lin0_intr_req1|IN_INTR1|Level|LIN0 Interrupt<br>Request 1|
||LIN1|lin1_intr_req0|IN_INTR2|Level|LIN1 Interrupt<br>Request 0|
||LIN1|lin1_intr_req1|IN_INTR3|Level|LIN1 Interrupt<br>Request 1|
||LIN2|lin2_intr_req0|IN_INTR4|Level|LIN2 Interrupt<br>Request 0|
||LIN2|lin2_intr_req1|IN_INTR5|Level|LIN2 Interrupt<br>Request 1|
||LIN3|lin3_intr_req0|IN_INTR6|Level|LIN3 Interrupt<br>Request 0|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 963 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-6. PRU_ICSS_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr**<br>**signal**|**XBAR Module**<br>**in_intr**|**Type**|**Description**|
|---|---|---|---|---|---|
||LIN3|lin3_intr_req1|IN_INTR7|Level|LIN3 Interrupt<br>Request 1|
||LIN4|lin4_intr_req0|IN_INTR8|Level|LIN4 Interrupt<br>Request 0|
||LIN4|lin4_intr_req1|IN_INTR9|Level|LIN4 Interrupt<br>Request 1|
||UART0|uart0_irq|IN_INTR10|Level|UART0 Interrupt|
||UART1|uart1_irq|IN_INTR11|Level|UART1 Interrupt|
||UART2|uart2_irq|IN_INTR12|Level|UART2 Interrupt|
|PRU_ICSS_XBAR_IN<br>TRTR0|UART3|uart3_irq|IN_INTR13|Level|UART3 Interrupt|
||UART4|uart4_irq|IN_INTR14|Level|UART4 Interrupt|
||UART5|uart5_irq|IN_INTR15|Level|UART5 Interrupt|
||I2C0|I2C0_IRQ|IN_INTR16|Pulse|I2C0 Interrupt|
||I2C1|I2C1_IRQ|IN_INTR17|Pulse|I2C1 Interrupt|
||I2C2|I2C2_IRQ|IN_INTR18|Pulse|I2C2 Interrupt|
||I2C3|I2C3_IRQ|IN_INTR19|Pulse|I2C3 Interrupt|
||SPI0|SPI0_intr|IN_INTR20|Level|SPI0 Interrupt|
||SPI1|SPI1_intr|IN_INTR21|Level|SPI1 Interrupt|
||SPI2|SPI2_intr|IN_INTR22|Level|SPI2 Interrupt|
||SPI3|SPI3_intr|IN_INTR23|Level|SPI3 Interrupt|
||SPI4|SPI4_intr|IN_INTR24|Level|SPI4 Interrupt|
||OPTI_FLASH|OSPI_intr|IN_INTR25|Level|OSPI Interrupt|
||SOC_EDMA0|TPCC_intg|IN_INTR26|Pulse|TPCC Global<br>Interrupt|
||SOC_EDMA0|TPCC_int0|IN_INTR27|Pulse|TPCC Region0<br>Interrupt|
||SOC_EDMA0|TPCC_int1|IN_INTR28|Pulse|TPCC Region1<br>Interrupt|
||SOC_EDMA0|TPCC_int2|IN_INTR29|Pulse|TPCC Region2<br>Interrupt|
||SOC_EDMA0|TPCC_int3|IN_INTR30|Pulse|TPCC Region3<br>Interrupt|
||SOC_EDMA0|TPCC_int4|IN_INTR31|Pulse|TPCC Region4<br>Interrupt|
||SOC_EDMA0|TPCC_int5|IN_INTR32|Pulse|TPCC Region5<br>Interrupt|
||SOC_EDMA0|TPCC_int6|IN_INTR33|Pulse|TPCC Region6<br>Interrupt|
||SOC_EDMA0|TPCC_int7|IN_INTR34|Pulse|TPCC Region7<br>Interrupt|
||SOC_EDMA0|TPCC_errint|IN_INTR35|Pulse|TPCC Error Interrupt|
||SOC_EDMA0|tpcc_mpint|IN_INTR36|Pulse|TPCC Memory<br>Protection Violation<br>Interrupt|
||SOC_EDMA0|tptc_erint0|IN_INTR37|Pulse|TPCC Interrupt|
||SOC_EDMA0|tptc_erint1|IN_INTR38|Pulse|TPCC Interrupt|
||MCAN0|mcanss0_ext_ts_rollo<br>ver_lvl_int|IN_INTR39|Level|MCAN0 External<br>TimeSync Rollover<br>Interrupt|



964 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-6. PRU_ICSS_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr**<br>**signal**|**XBAR Module**<br>**in_intr**|**Type**|**Description**|
|---|---|---|---|---|---|
||MCAN0|mcanss0_mcan_lvl_in<br>t_0|IN_INTR40|Level|MCAN0 Interrupt 0|
||MCAN0|mcanss0_mcan_lvl_in<br>t_1|IN_INTR41|Level|MCAN0 Interrupt 1|
||MCAN1|mcanss1_ext_ts_rollo<br>ver_lvl_int|IN_INTR42|Level|MCAN1 External<br>TimeSync Rollover<br>Interrupt|
||MCAN1|mcanss1_mcan_lvl_in<br>t_0|IN_INTR43|Level|MCAN1 Interrupt 0|
||MCAN1|mcanss1_mcan_lvl_in<br>t_1|IN_INTR44|Level|MCAN1 Interrupt 1|
|PRU_ICSS_XBAR_IN<br>TRTR0|MCAN2|mcanss2_ext_ts_rollo<br>ver_lvl_int|IN_INTR45|Level|MCAN2 External<br>TimeSync Rollover<br>Interrupt|
||MCAN2|mcanss2_mcan_lvl_in<br>t_0|IN_INTR46|Level|MCAN2 Interrupt 0|
||MCAN2|mcanss2_mcan_lvl_in<br>t_1|IN_INTR47|Level|MCAN2 Interrupt 1|
||MCAN3|mcanss3_ext_ts_rollo<br>ver_lvl_int|IN_INTR48|Level|MCAN3 External<br>TimeSync Rollover<br>Interrupt|
||MCAN3|mcanss3_mcan_lvl_in<br>t_0|IN_INTR49|Level|MCAN3 Interrupt 0|
||MCAN3|mcanss3_mcan_lvl_in<br>t_1|IN_INTR50|Level|MCAN3 Interrupt 1|
||MSS_CTRL|ICSSM_PRU0_MBO<br>X_READ_REQ|IN_INTR51|Level|MAILBOX PRU<br>Request Interrupt 0|
||MSS_CTRL|ICSSM_PRU1_MBO<br>X_READ_REQ|IN_INTR52|Level|MAILBOX PRU<br>Request Interrupt 1|
||MSS_CTRL|ICSSM_PRU0_MBO<br>X_READ_DONE|IN_INTR53|Level|MAILBOX PRU<br>Acknowledge<br>Interrupt 0|
||MSS_CTRL|ICSSM_PRU1_MBO<br>X_READ_DONE|IN_INTR54|Level|MAILBOX PRU<br>Acknowledge<br>Interrupt 1|
||GPIO_XBAR|GPIO_xbarout_0|IN_INTR55|Pulse|GPIO XBAR0<br>Interrupt|
||GPIO_XBAR|GPIO_xbarout_1|IN_INTR56|Pulse|GPIO XBAR1<br>Interrupt|
||GPIO_XBAR|GPIO_xbarout_2|IN_INTR57|Pulse|GPIO XBAR2<br>Interrupt|
||GPIO_XBAR|GPIO_xbarout_3|IN_INTR58|Pulse|GPIO XBAR3<br>Interrupt|
||MCAN4|mcanss4_ext_ts_rollo<br>ver_lvl_int|IN_INTR59|Level|MCAN4 External<br>TimeSync Rollover<br>Interrupt|
||MCAN4|mcanss4_mcan_lvl_in<br>t_0|IN_INTR60|Level|MCAN4 Interrupt 0|
||MCAN4|mcanss4_mcan_lvl_in<br>t_1|IN_INTR61|Level|MCAN4 Interrupt 1|
||MCAN5|mcanss5_ext_ts_rollo<br>ver_lvl_int|IN_INTR62|Level|MCAN5 External<br>TimeSync Rollover<br>Interrupt|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 965 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-6. PRU_ICSS_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr**<br>**signal**|**XBAR Module**<br>**in_intr**|**Type**|**Description**|
|---|---|---|---|---|---|
||MCAN5|mcanss5_mcan_lvl_in<br>t_0|IN_INTR63|Level|MCAN5 Interrupt 0|
||MCAN5|mcanss5_mcan_lvl_in<br>t_1|IN_INTR64|Level|MCAN5 Interrupt 1|
||MCAN6|mcanss6_ext_ts_rollo<br>ver_lvl_int|IN_INTR65|Level|MCAN6 External<br>TimeSync Rollover<br>Interrupt|
||MCAN6|mcanss6_mcan_lvl_in<br>t_0|IN_INTR66|Level|MCAN6 Interrupt 0|
||MCAN6|mcanss6_mcan_lvl_in<br>t_1|IN_INTR67|Level|MCAN6 Interrupt 1|
||MCAN7|mcanss7_ext_ts_rollo<br>ver_lvl_int|IN_INTR68|Level|MCAN7 External<br>TimeSync Rollover<br>Interrupt|
|PRU_ICSS_XBAR_IN<br>TRTR0|MCAN7|mcanss7_mcan_lvl_in<br>t_0|IN_INTR69|Level|MCAN7 Interrupt 0|
||MCAN7|mcanss7_mcan_lvl_in<br>t_1|IN_INTR70|Level|MCAN7 Interrupt 1|
||SPI5|SPI5_intr|IN_INTR71|Level|SPI5 Interrupt|
||SPI6|SPI6_intr|IN_INTR72|Level|SPI6 Interrupt|
||SPI7|SPI7_intr|IN_INTR73|Level|SPI7 Interrupt|



## **10.3.2.2 EDMA XBAR INTRTR0** 

There is 1x EDMA XBAR Interrupt Router module integrated in the device. The diagram below provides a visual representation of the device integration details for EDMA XBAR Interrupt Router. 

966 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**==> picture [500 x 437] intentionally omitted <==**

**Figure 10-3. EDMA XBAR Interrupt Router Integration Diagram** 

The tables below summarize the device integration details of EDMA XBAR Interrupt router. 

**Table 10-7. EDMA XBAR Intrrupt router Device Integration** 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|EDMA_XBAR_INTRTR0|✓|INFRA0 VBUSP Interconnect|



## **Table 10-8. EDMA_XBAR_INTRTR0 Clocks** 

|**Module**<br>**Instance**|**Module Clock in_intr**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|EDMA_XBA<br>R_INTRTR0|SYSCLK|SYS_CLK|MSS_RCM|200 MHz|EDMA_XBAR_INTRTR0<br>Functional and Interface<br>clock|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

967 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

|**Table 10-9. EDMA_XBAR_INTRTR0 Resets**|**Table 10-9. EDMA_XBAR_INTRTR0 Resets**|**Table 10-9. EDMA_XBAR_INTRTR0 Resets**|**Table 10-9. EDMA_XBAR_INTRTR0 Resets**|**Table 10-9. EDMA_XBAR_INTRTR0 Resets**|
|---|---|---|---|---|
|**Module**<br>**Instance**|**Module Reset in_intr**|**Source Reset Signal**|**Source**|**Description**|
|EDMA_XB<br>AR_INTRT<br>R0|RST|SYS_RST|MSS_RCM|EDMA_XBAR_INTRTR0 Reset|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

968 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-10. EDMA_XBAR_INTRTR0 Output Hardware Requests** 

|**Module**<br>**Instance**|**Module XBAR**<br>**Output**|**Destination XBAR signal**|**Destination**|**Description**|**Type**|
|---|---|---|---|---|---|
|EDMA_XBA<br>R_INTRTR0|outl_intr_0|EDMA_Trigger_XBAROut_0|TPCC|Selectable Hardware Request 0|Pulse|
||outl_intr_1|EDMA_Trigger_XBAROut_1||Selectable Hardware Request 1||
||outl_intr_2|EDMA_Trigger_XBAROut_2||Selectable Hardware Request 2||
||outl_intr_3|EDMA_Trigger_XBAROut_3||Selectable Hardware Request 3||
||outl_intr_4|EDMA_Trigger_XBAROut_4||Selectable Hardware Request 4||
||outl_intr_5|EDMA_Trigger_XBAROut_5||Selectable Hardware Request 5||
||outl_intr_6|EDMA_Trigger_XBAROut_6||Selectable Hardware Request 6||
||outl_intr_7|EDMA_Trigger_XBAROut_7||Selectable Hardware Request 7||
||outl_intr_8|EDMA_Trigger_XBAROut_8||Selectable Hardware Request 8||
||outl_intr_9|EDMA_Trigger_XBAROut_9||Selectable Hardware Request 9||
||outl_intr_10|EDMA_Trigger_XBAROut_10||Selectable Hardware Request 10||
||outl_intr_11|EDMA_Trigger_XBAROut_11||Selectable Hardware Request 11||
||outl_intr_12|EDMA_Trigger_XBAROut_12||Selectable Hardware Request 12||
||outl_intr_13|EDMA_Trigger_XBAROut_13||Selectable Hardware Request 13||
||outl_intr_14|EDMA_Trigger_XBAROut_14||Selectable Hardware Request 14||
||outl_intr_15|EDMA_Trigger_XBAROut_15||Selectable Hardware Request 15||
||outl_intr_16|EDMA_Trigger_XBAROut_16||Selectable Hardware Request 16||
||outl_intr_17|EDMA_Trigger_XBAROut_17||Selectable Hardware Request 17||
||outl_intr_18|EDMA_Trigger_XBAROut_18||Selectable Hardware Request 18||
||outl_intr_19|EDMA_Trigger_XBAROut_19||Selectable Hardware Request 19||
||outl_intr_20|EDMA_Trigger_XBAROut_20||Selectable Hardware Request 20||
||outl_intr_21|EDMA_Trigger_XBAROut_21||Selectable Hardware Request 21||
||outl_intr_22|EDMA_Trigger_XBAROut_22||Selectable Hardware Request 22||
||outl_intr_23|EDMA_Trigger_XBAROut_23||Selectable Hardware Request 23||
||outl_intr_24|EDMA_Trigger_XBAROut_24||Selectable Hardware Request 24||
||outl_intr_25|EDMA_Trigger_XBAROut_25||Selectable Hardware Request 25||
||outl_intr_26|EDMA_Trigger_XBAROut_26||Selectable Hardware Request 26||
||outl_intr_27|EDMA_Trigger_XBAROut_27||Selectable Hardware Request 27||
||outl_intr_28|EDMA_Trigger_XBAROut_28||Selectable Hardware Request 28||
||outl_intr_29|EDMA_Trigger_XBAROut_29||Selectable Hardware Request 29||
||outl_intr_30|EDMA_Trigger_XBAROut_30||Selectable Hardware Request 30||
||outl_intr_31|EDMA_Trigger_XBAROut_31||Selectable Hardware Request 31||
||outl_intr_32|EDMA_Trigger_XBAROut_32||Selectable Hardware Request 32||
||outl_intr_33|EDMA_Trigger_XBAROut_33||Selectable Hardware Request 33||
||outl_intr_34|EDMA_Trigger_XBAROut_34||Selectable Hardware Request 34||
||outl_intr_35|EDMA_Trigger_XBAROut_35||Selectable Hardware Request 35||
||outl_intr_36|EDMA_Trigger_XBAROut_36||Selectable Hardware Request 36||
||outl_intr_37|EDMA_Trigger_XBAROut_37||Selectable Hardware Request 37||
||outl_intr_38|EDMA_Trigger_XBAROut_38||Selectable Hardware Request 38||
||outl_intr_39|EDMA_Trigger_XBAROut_39||Selectable Hardware Request 39||
||outl_intr_40|EDMA_Trigger_XBAROut_40||Selectable Hardware Request 40||
||outl_intr_41|EDMA_Trigger_XBAROut_41||Selectable Hardware Request 41||
||outl_intr_42|EDMA_Trigger_XBAROut_42||Selectable Hardware Request 42||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 969 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-10. EDMA_XBAR_INTRTR0 Output Hardware Requests (continued)** 

|**Module**<br>**Instance**|**Module XBAR**<br>**Output**|**Destination XBAR signal**|**Destination**|**Description**|**Type**|
|---|---|---|---|---|---|
||outl_intr_43|EDMA_Trigger_XBAROut_43||Selectable Hardware Request 43||
||outl_intr_44|EDMA_Trigger_XBAROut_44||Selectable Hardware Request 44||
||outl_intr_45|EDMA_Trigger_XBAROut_45||Selectable Hardware Request 45||
||outl_intr_46|EDMA_Trigger_XBAROut_46||Selectable Hardware Request 46||
||outl_intr_47|EDMA_Trigger_XBAROut_47||Selectable Hardware Request 47||
||outl_intr_48|EDMA_Trigger_XBAROut_48||Selectable Hardware Request 48||
||outl_intr_49|EDMA_Trigger_XBAROut_49||Selectable Hardware Request 49||
||outl_intr_50|EDMA_Trigger_XBAROut_50||Selectable Hardware Request 50||
||outl_intr_51|EDMA_Trigger_XBAROut_51||Selectable Hardware Request 51||
||outl_intr_52|EDMA_Trigger_XBAROut_52||Selectable Hardware Request 52||
||outl_intr_53|EDMA_Trigger_XBAROut_53||Selectable Hardware Request 53||
||outl_intr_54|EDMA_Trigger_XBAROut_54||Selectable Hardware Request 54||
||outl_intr_55|EDMA_Trigger_XBAROut_55||Selectable Hardware Request 55||
||outl_intr_56|EDMA_Trigger_XBAROut_56||Selectable Hardware Request 56||
||outl_intr_57|EDMA_Trigger_XBAROut_57||Selectable Hardware Request 57||
||outl_intr_58|EDMA_Trigger_XBAROut_58||Selectable Hardware Request 58||
||outl_intr_59|EDMA_Trigger_XBAROut_59||Selectable Hardware Request 59||
||outl_intr_60|EDMA_Trigger_XBAROut_60||Selectable Hardware Request 60||
||outl_intr_61|EDMA_Trigger_XBAROut_61||Selectable Hardware Request 61||
||outl_intr_62|EDMA_Trigger_XBAROut_62||Selectable Hardware Request 62||
||outl_intr_63|EDMA_Trigger_XBAROut_63||Selectable Hardware Request 63||



**Table 10-11. EDMA_XBAR_INTRTR0 in_intr Hardware Requests** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Desc ription**|**Type**|
|---|---|---|---|---|---|
|EDMA_XBAR_INTRTR0|LIN0|lin0_RXDMA|IN_INTR0|LIN0 RX DMA Request|Pulse|
||LIN0|lin0_TXDMA|IN_INTR1|LIN0 TX DMA Request|Pulse|
||LIN1|lin1_RXDMA|IN_INTR2|LIN1 RX DMA Request|Pulse|
||LIN1|lin0_TXDMA|IN_INTR3|LIN1 TX DMA Request|Pulse|
||LIN2|lin2_RXDMA|IN_INTR4|LIN2 RX DMA Request|Pulse|
||LIN2|lin2_TXDMA|IN_INTR5|LIN2 TX DMA Request|Pulse|
||LIN3|lin3_RXDMA|IN_INTR6|LIN3 RX DMA Request|Pulse|
||LIN3|lin3_TXDMA|IN_INTR7|LIN3 TX DMA Request|Pulse|
||LIN4|lin4_RXDMA|IN_INTR8|LIN4 RX DMA Request|Pulse|
||LIN4|lin4_TXDMA|IN_INTR9|LIN4 TX DMA Request|Pulse|
||I2C0|I2C0_TX|IN_INTR10|I2C0 RX DMA Request|Pulse|
||I2C0|I2C0_RX|IN_INTR11|I2C0 TX DMA Request|Pulse|
||I2C1|I2C1_TX|IN_INTR12|I2C1 RX DMA Request|Pulse|
||I2C1|I2C1_RX|IN_INTR13|I2C1 TX DMA Request|Pulse|
||I2C2|I2C2_TX|IN_INTR14|I2C2 RX DMA Request|Pulse|
||I2C2|I2C2_RX|IN_INTR15|I2C2 TX DMA Request|Pulse|
||I2C3|I2C3_TX|IN_INTR16|I2C3 RX DMA Request|Pulse|
||I2C3|I2C3_RX|IN_INTR17|I2C3 TX DMA Request|Pulse|
||SPI0|SPI0_dma_Read_req0|IN_INTR18|SPI0 DMA Read Request 0|Pulse|



970 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-11. EDMA_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Desc ription**|**Type**|
|---|---|---|---|---|---|
||SPI0|SPI0_dma_Read_req1|IN_INTR19|SPI0 DMA Read Request 1|Pulse|
||SPI0|SPI0_dma_Read_req2|IN_INTR20|SPI0 DMA Read Request 2|Pulse|
||SPI0|SPI0_dma_Read_req3|IN_INTR21|SPI0 DMA Read Request 3|Pulse|
||SPI0|SPI0_dma_Write_req0|IN_INTR22|SPI0 DMA Write Request 0|Pulse|
||SPI0|SPI0_dma_Write_req1|IN_INTR23|SPI0 DMA Write Request 1|Pulse|
||SPI0|SPI0_dma_Write_req2|IN_INTR24|SPI0 DMA Write Request 2|Pulse|
||SPI0|SPI0_dma_Write_req3|IN_INTR25|SPI0 DMA Write Request 3|Pulse|
||SPI1|SPI1_dma_Read_req0|IN_INTR26|SPI1 DMA Read Request 0|Pulse|
||SPI1|SPI1_dma_Read_req1|IN_INTR27|SPI1 DMA Read Request 1|Pulse|
||SPI1|SPI1_dma_Read_req2|IN_INTR28|SPI1 DMA Read Request 2|Pulse|
||SPI1|SPI1_dma_Read_req3|IN_INTR29|SPI1 DMA Read Request 3|Pulse|
||SPI1|SPI1_dma_Write_req0|IN_INTR30|SPI1 DMA Write Request 0|Pulse|
||SPI1|SPI1_dma_Write_req1|IN_INTR31|SPI1 DMA Write Request 1|Pulse|
||SPI1|SPI1_dma_Write_req2|IN_INTR32|SPI1 DMA Write Request 2|Pulse|
||SPI1|SPI1_dma_Write_req3|IN_INTR33|SPI1 DMA Write Request 3|Pulse|
||SPI2|SPI2_dma_Read_req0|IN_INTR34|SPI2 DMA Read Request 0|Pulse|
||SPI2|SPI2_dma_Read_req1|IN_INTR35|SPI2 DMA Read Request 1|Pulse|
||SPI2|SPI2_dma_Read_req2|IN_INTR36|SPI2 DMA Read Request 2|Pulse|
||SPI2|SPI2_dma_Read_req3|IN_INTR37|SPI2 DMA Read Request 3|Pulse|
||SPI2|SPI2_dma_Write_req0|IN_INTR38|SPI2 DMA Write Request 0|Pulse|
||SPI2|SPI2_dma_Write_req1|IN_INTR39|SPI2 DMA Write Request 1|Pulse|
||SPI2|SPI2_dma_Write_req2|IN_INTR40|SPI2 DMA Write Request 2|Pulse|
||SPI2|SPI2_dma_Write_req3|IN_INTR41|SPI2 DMA Write Request 3|Pulse|
||SPI3|SPI3_dma_Read_req0|IN_INTR42|SPI3 DMA Read Request 0|Pulse|
||SPI3|SPI3_dma_Read_req1|IN_INTR43|SPI3 DMA Read Request 1|Pulse|
||SPI3|SPI3_dma_Read_req2|IN_INTR44|SPI3 DMA Read Request 2|Pulse|
||SPI3|SPI3_dma_Read_req3|IN_INTR45|SPI3 DMA Read Request 3|Pulse|
||SPI3|SPI3_dma_Write_req0|IN_INTR46|SPI3 DMA Write Request 0|Pulse|
||SPI3|SPI3_dma_Write_req1|IN_INTR47|SPI3 DMA Write Request 1|Pulse|
||SPI3|SPI3_dma_Write_req2|IN_INTR48|SPI3 DMA Write Request 2|Pulse|
||SPI3|SPI3_dma_Write_req3|IN_INTR49|SPI3 DMA Write Request 3|Pulse|
||SPI4|SPI4_dma_Read_req0|IN_INTR50|SPI4 DMA Read Request 0|Pulse|
||SPI4|SPI4_dma_Read_req1|IN_INTR51|SPI4 DMA Read Request 1|Pulse|
||SPI4|SPI4_dma_Read_req2|IN_INTR52|SPI4 DMA Read Request 2|Pulse|
||SPI4|SPI4_dma_Read_req3|IN_INTR53|SPI4 DMA Read Request 3|Pulse|
||SPI4|SPI4_dma_Write_req0|IN_INTR54|SPI4 DMA Write Request 0|Pulse|
||SPI4|SPI4_dma_Write_req1|IN_INTR55|SPI4 DMA Write Request 1|Pulse|
||SPI4|SPI4_dma_Write_req2|IN_INTR56|SPI4 DMA Write Request 2|Pulse|
||SPI4|SPI4_dma_Write_req3|IN_INTR57|SPI4 DMA Write Request 3|Pulse|
||RTI0|RTI0_DMA_0|IN_INTR58|RTI0 DMA Request 0|Pulse|
||RTI0|RTI0_DMA_1|IN_INTR59|RTI0 DMA Request 1|Pulse|
||RTI0|RTI0_DMA_2|IN_INTR60|RTI0 DMA Request 2|Pulse|
||RTI0|RTI0_DMA_3|IN_INTR61|RTI0 DMA Request 3|Pulse|
||RTI1|RTI1_DMA_0|IN_INTR62|RTI1 DMA Request 0|Pulse|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 971 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-11. EDMA_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Desc ription**|**Type**|
|---|---|---|---|---|---|
||RTI1|RTI1_DMA_1|IN_INTR63|RTI1 DMA Request 1|Pulse|
||RTI1|RTI1_DMA_2|IN_INTR64|RTI1 DMA Request 2|Pulse|
||RTI1|RTI1_DMA_3|IN_INTR65|RTI1 DMA Request 3|Pulse|
||RTI2|RTI2_DMA_0|IN_INTR66|RTI2 DMA Request 0|Pulse|
||RTI2|RTI2_DMA_1|IN_INTR67|RTI2 DMA Request 1|Pulse|
||RTI2|RTI2_DMA_2|IN_INTR68|RTI2 DMA Request 2|Pulse|
||RTI2|RTI2_DMA_3|IN_INTR69|RTI2 DMA Request 3|Pulse|
||RTI3|RTI3_DMA_0|IN_INTR70|RTI3 DMA Request 0|Pulse|
||RTI3|RTI3_DMA_1|IN_INTR71|RTI3 DMA Request 1|Pulse|
||RTI3|RTI3_DMA_2|IN_INTR72|RTI3 DMA Request 2|Pulse|
||RTI3|RTI3_DMA_3|IN_INTR73|RTI3 DMA Request 3|Pulse|
||MCAN0|mcanss0_tx_dma_0|IN_INTR74|MCAN0 TX DMA Request 0|Pulse|
||MCAN0|mcanss0_tx_dma_1|IN_INTR75|MCAN0 TX DMA Request 1|Pulse|
||MCAN0|mcanss0_tx_dma_2|IN_INTR76|MCAN0 TX DMA Request 2|Pulse|
||MCAN0|mcanss0_tx_dma_3|IN_INTR77|MCAN0 TX DMA Request 3|Pulse|
||MCAN1|mcanss1_tx_dma_0|IN_INTR78|MCAN1 TX DMA Request 0|Pulse|
||MCAN1|mcanss1_tx_dma_1|IN_INTR79|MCAN1 TX DMA Request 1|Pulse|
||MCAN1|mcanss1_tx_dma_2|IN_INTR80|MCAN1 TX DMA Request 2|Pulse|
||MCAN1|mcanss1_tx_dma_3|IN_INTR81|MCAN1 TX DMA Request 3|Pulse|
||MCAN2|mcanss2_tx_dma_0|IN_INTR82|MCAN2 TX DMA Request 0|Pulse|
||MCAN2|mcanss2_tx_dma_1|IN_INTR83|MCAN2 TX DMA Request 1|Pulse|
||MCAN2|mcanss2_tx_dma_2|IN_INTR84|MCAN2 TX DMA Request 2|Pulse|
||MCAN2|mcanss2_tx_dma_3|IN_INTR85|MCAN2 TX DMA Request 3|Pulse|
||MCAN3|mcanss3_tx_dma_0|IN_INTR86|MCAN3 TX DMA Request 0|Pulse|
||MCAN3|mcanss3_tx_dma_1|IN_INTR87|MCAN3 TX DMA Request 1|Pulse|
||MCAN3|mcanss3_tx_dma_2|IN_INTR88|MCAN3 TX DMA Request 2|Pulse|
||MCAN3|mcanss3_tx_dma_3|IN_INTR89|MCAN3 TX DMA Request 3|Pulse|
||UART0|usart0_dma_0|IN_INTR90|UART0 DMA Request 0|Pulse|
||UART0|usart0_dma_1|IN_INTR91|UART0 DMA Request 1|Pulse|
||UART1|usart1_dma_0|IN_INTR92|UART1 DMA Request 0|Pulse|
||UART1|usart1_dma_1|IN_INTR93|UART1 DMA Request 1|Pulse|
||UART2|usart2_dma_0|IN_INTR94|UART2 DMA Request 0|Pulse|
||UART2|usart2_dma_1|IN_INTR95|UART2 DMA Request 1|Pulse|
||UART3|usart0_dma_0|IN_INTR96|UART3 DMA Request 0|Pulse|
||UART3|usart3_dma_1|IN_INTR97|UART3 DMA Request 1|Pulse|
||UART4|usart4_dma_0|IN_INTR98|UART4 DMA Request 0|Pulse|
||UART4|usart4_dma_1|IN_INTR99|UART4 DMA Request 1|Pulse|
||UART5|usart5_dma_0|IN_INTR100|UART5 DMA Request 0|Pulse|
||UART5|usart5_dma_1|IN_INTR101|UART5 DMA Request 1|Pulse|
||MCRC|mcrc_DMA_Event_0|IN_INTR102|MCRC DMA Event 0|Pulse|
||MCRC|mcrc_DMA_Event_1|IN_INTR103|MCRC DMA Event 1|Pulse|
||MCRC|mcrc_DMA_Event_2|IN_INTR104|MCRC DMA Event 2|Pulse|
||MCRC|mcrc_DMA_Event_3|IN_INTR105|MCRC DMA Event 3|Pulse|
||OSPI|OSPI_INTR|IN_INTR106|OSPI Interrupt|Pulse|



972 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-11. EDMA_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Desc ription**|**Type**|
|---|---|---|---|---|---|
||GPIO_XBAR|GPIO_xbarout_4|IN_INTR107|GPIO XBAR Out 4|Pulse|
||GPIO_XBAR|GPIO_xbarout_5|IN_INTR108|GPIO XBAR Out 5|Pulse|
||GPIO_XBAR|GPIO_xbarout_6|IN_INTR109|GPIO XBAR Out 6|Pulse|
||GPIO_XBAR|GPIO_xbarout_7|IN_INTR110|GPIO XBAR Out 7|Pulse|
||SOC_TimeSync_<br>XBAR|Sync_Xbarout_0|IN_INTR111|SOC TimeSync XBAR Out 0|Pulse|
||SOC_TimeSync_<br>XBAR|Sync_Xbarout_1|IN_INTR112|SOC TimeSync XBAR Out 1|Pulse|
||CONTROLSS_Ti<br>meSync_XBAR|CONTROLSS_timesync_xb<br>ar.out10|IN_INTR113|CONTROLSS TimeSync XBAR<br>Out 0|Pulse|
||CONTROLSS_Ti<br>meSync_XBAR|CONTROLSS_timesync_xb<br>ar.out11|IN_INTR114|CONTROLSS TimeSync XBAR<br>Out 1|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_0|IN_INTR115|CONTROLSS EDMA_XBAR Out<br>0|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_1|IN_INTR116|CONTROLSS EDMA_XBAR Out<br>1|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_2|IN_INTR117|CONTROLSS EDMA_XBAR Out<br>2|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_3|IN_INTR118|CONTROLSS EDMA_XBAR Out<br>3|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_4|IN_INTR119|CONTROLSS EDMA_XBAR Out<br>4|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_5|IN_INTR120|CONTROLSS EDMA_XBAR Out<br>5|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_6|IN_INTR121|CONTROLSS EDMA_XBAR Out<br>6|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_7|IN_INTR122|CONTROLSS EDMA_XBAR Out<br>7|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_8|IN_INTR123|CONTROLSS EDMA_XBAR Out<br>8|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_9|IN_INTR124|CONTROLSS EDMA_XBAR Out<br>9|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_10|IN_INTR125|CONTROLSS EDMA_XBAR Out<br>10|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_11|IN_INTR126|CONTROLSS EDMA_XBAR Out<br>11|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_12|IN_INTR127|CONTROLSS EDMA_XBAR Out<br>12|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_13|IN_INTR128|CONTROLSS EDMA_XBAR Out<br>13|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_14|IN_INTR129|CONTROLSS EDMA_XBAR Out<br>14|Pulse|
||CONTROLSS_D<br>MA_XBAR|CCSS_DMA_15|IN_INTR130|CONTROLSS EDMA_XBAR Out<br>15|Pulse|
||MMCSD|mmc_DMA_RD|IN_INTR131|MMCSD DMA Read Request|Pulse|
||MMCSD|mmc_DMA_WR|IN_INTR132|MMCSD DMA Write Request|Pulse|
||DTHE|DTHE_SHA_DMA_REQ0|IN_INTR133|DTHE SHA DMA Request 0|Pulse|
||DTHE|DTHE_SHA_DMA_REQ1|IN_INTR134|DTHE SHA DMA Request 1|Pulse|
||DTHE|DTHE_SHA_DMA_REQ2|IN_INTR135|DTHE SHA DMA Request 2|Pulse|
||DTHE|DTHE_SHA_DMA_REQ3|IN_INTR136|DTHE SHA DMA Request 3|Pulse|
||DTHE|DTHE_SHA_DMA_REQ4|IN_INTR137|DTHE SHA DMA Request 4|Pulse|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 973 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-11. EDMA_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Desc ription**|**Type**|
|---|---|---|---|---|---|
||DTHE|DTHE_SHA_DMA_REQ5|IN_INTR138|DTHE SHA DMA Request 5|Pulse|
||DTHE|DTHE_AES_DMA_REQ0|IN_INTR139|DTHE AES DMA Request 0|Pulse|
||DTHE|DTHE_AES_DMA_REQ1|IN_INTR140|DTHE AES DMA Request 1|Pulse|
||DTHE|DTHE_AES_DMA_REQ2|IN_INTR141|DTHE AES DMA Request 2|Pulse|
||DTHE|DTHE_AES_DMA_REQ3|IN_INTR142|DTHE AES DMA Request 3|Pulse|
||DTHE|DTHE_AES_DMA_REQ4|IN_INTR143|DTHE AES DMA Request 4|Pulse|
||DTHE|DTHE_AES_DMA_REQ5|IN_INTR144|DTHE AES DMA Request 5|Pulse|
||DTHE|DTHE_AES_DMA_REQ6|IN_INTR145|DTHE AES DMA Request 6|Pulse|
||DTHE|DTHE_AES_DMA_REQ7|IN_INTR146|DTHE AES DMA Request 7|Pulse|
||MCAN0|mcanss0_fe_0|IN_INTR147|MCAN0 Request 0|Pulse|
||MCAN0|mcanss0_fe_1|IN_INTR148|MCAN0 Request 1|Pulse|
||MCAN0|mcanss0_fe_2|IN_INTR149|MCAN0 Request 2|Pulse|
||MCAN0|mcanss0_fe_3|IN_INTR150|MCAN0 Request 3|Pulse|
||MCAN0|mcanss0_fe_4|IN_INTR151|MCAN0 Request 4|Pulse|
||MCAN0|mcanss0_fe_5|IN_INTR152|MCAN0 Request 5|Pulse|
||MCAN0|mcanss0_fe_6|IN_INTR153|MCAN0 Request 6|Pulse|
||MCAN1|mcanss1_fe_0|IN_INTR154|MCAN1 Request 0|Pulse|
||MCAN1|mcanss1_fe_1|IN_INTR155|MCAN1 Request 1|Pulse|
||MCAN1|mcanss1_fe_2|IN_INTR156|MCAN1 Request 2|Pulse|
||MCAN1|mcanss1_fe_3|IN_INTR157|MCAN1 Request 3|Pulse|
||MCAN1|mcanss1_fe_4|IN_INTR158|MCAN1 Request 4|Pulse|
||MCAN1|mcanss1_fe_5|IN_INTR159|MCAN1 Request 5|Pulse|
||MCAN1|mcanss1_fe_6|IN_INTR160|MCAN1 Request 6|Pulse|
||MCAN2|mcanss2_fe_0|IN_INTR161|MCAN2 Request 0|Pulse|
||MCAN2|mcanss2_fe_1|IN_INTR162|MCAN2 Request 1|Pulse|
||MCAN2|mcanss2_fe_2|IN_INTR163|MCAN2 Request 2|Pulse|
||MCAN2|mcanss2_fe_3|IN_INTR164|MCAN2 Request 3|Pulse|
||MCAN2|mcanss2_fe_4|IN_INTR165|MCAN2 Request 4|Pulse|
||MCAN2|mcanss2_fe_5|IN_INTR166|MCAN2 Request 5|Pulse|
||MCAN2|mcanss2_fe_6|IN_INTR167|MCAN2 Request 6|Pulse|
||MCAN3|mcanss3_fe_0|IN_INTR168|MCAN3 Request 0|Pulse|
||MCAN3|mcanss3_fe_1|IN_INTR169|MCAN3 Request 1|Pulse|
||MCAN3|mcanss3_fe_2|IN_INTR170|MCAN3 Request 2|Pulse|
||MCAN3|mcanss3_fe_3|IN_INTR171|MCAN3 Request 3|Pulse|
||MCAN3|mcanss3_fe_4|IN_INTR172|MCAN3 Request 4|Pulse|
||MCAN3|mcanss3_fe_5|IN_INTR173|MCAN3 Request 5|Pulse|
||MCAN3|mcanss3_fe_6|IN_INTR174|MCAN3 Request 6|Pulse|
||RESERVED|Reserved|IN_INTR175|Reserved|-|
||MCAN4|mcanss4_tx_dma_0|IN_INTR176|MCAN4 TX DMA Request 0|Pulse|
||MCAN4|mcanss4_tx_dma_1|IN_INTR177|MCAN4 TX DMA Request 1|Pulse|
||MCAN4|mcanss4_tx_dma_2|IN_INTR178|MCAN4 TX DMA Request 2|Pulse|
||MCAN4|mcanss4_tx_dma_3|IN_INTR179|MCAN4 TX DMA Request 3|Pulse|
||MCAN5|mcanss5_tx_dma_0|IN_INTR180|MCAN5 TX DMA Request 0|Pulse|
||MCAN5|mcanss5_tx_dma_1|IN_INTR181|MCAN5 TX DMA Request 1|Pulse|



974 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-11. EDMA_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Desc ription**|**Type**|
|---|---|---|---|---|---|
||MCAN5|mcanss5_tx_dma_2|IN_INTR182|MCAN5 TX DMA Request 2|Pulse|
||MCAN5|mcanss5_tx_dma_3|IN_INTR183|MCAN5 TX DMA Request 3|Pulse|
||MCAN6|mcanss6_tx_dma_0|IN_INTR184|MCAN6 TX DMA Request 0|Pulse|
||MCAN6|mcanss6_tx_dma_1|IN_INTR185|MCAN6 TX DMA Request 1|Pulse|
||MCAN6|mcanss6_tx_dma_2|IN_INTR186|MCAN6 TX DMA Request 2|Pulse|
||MCAN6|mcanss6_tx_dma_3|IN_INTR187|MCAN6 TX DMA Request 3|Pulse|
||MCAN7|mcanss7_tx_dma_0|IN_INTR188|MCAN7 TX DMA Request 0|Pulse|
||MCAN7|mcanss7_tx_dma_1|IN_INTR189|MCAN7 TX DMA Request 1|Pulse|
||MCAN7|mcanss7_tx_dma_2|IN_INTR190|MCAN7 TX DMA Request 2|Pulse|
||MCAN7|mcanss7_tx_dma_3|IN_INTR191|MCAN7 TX DMA Request 3|Pulse|
||MCAN4|mcanss4_fe_0|IN_INTR192|MCAN4 Request 0|Pulse|
||MCAN4|mcanss4_fe_1|IN_INTR193|MCAN4 Request 1|Pulse|
||MCAN4|mcanss4_fe_2|IN_INTR194|MCAN4 Request 2|Pulse|
||MCAN4|mcanss4_fe_3|IN_INTR195|MCAN4 Request 3|Pulse|
||MCAN4|mcanss4_fe_4|IN_INTR196|MCAN4 Request 4|Pulse|
||MCAN4|mcanss4_fe_5|IN_INTR197|MCAN4 Request 5|Pulse|
||MCAN4|mcanss4_fe_6|IN_INTR198|MCAN4 Request 6|Pulse|
||MCAN5|mcanss5_fe_0|IN_INTR199|MCAN5 Request 0|Pulse|
||MCAN5|mcanss5_fe_1|IN_INTR200|MCAN5 Request 1|Pulse|
||MCAN5|mcanss5_fe_2|IN_INTR201|MCAN5 Request 2|Pulse|
||MCAN5|mcanss5_fe_3|IN_INTR202|MCAN5 Request 3|Pulse|
||MCAN5|mcanss5_fe_4|IN_INTR203|MCAN5 Request 4|Pulse|
||MCAN5|mcanss5_fe_5|IN_INTR204|MCAN5 Request 5|Pulse|
||MCAN5|mcanss5_fe_6|IN_INTR205|MCAN5 Request 6|Pulse|
||MCAN6|mcanss6_fe_0|IN_INTR206|MCAN6 Request 0|Pulse|
||MCAN6|mcanss6_fe_1|IN_INTR207|MCAN6 Request 1|Pulse|
||MCAN6|mcanss6_fe_2|IN_INTR208|MCAN6 Request 2|Pulse|
||MCAN6|mcanss6_fe_3|IN_INTR209|MCAN6 Request 3|Pulse|
||MCAN6|mcanss6_fe_4|IN_INTR210|MCAN6 Request 4|Pulse|
||MCAN6|mcanss6_fe_5|IN_INTR211|MCAN6 Request 5|Pulse|
||MCAN6|mcanss6_fe_6|IN_INTR212|MCAN6 Request 6|Pulse|
||MCAN7|mcanss7_fe_0|IN_INTR213|MCAN7 Request 0|Pulse|
||MCAN7|mcanss7_fe_1|IN_INTR214|MCAN7 Request 1|Pulse|
||MCAN7|mcanss7_fe_2|IN_INTR215|MCAN7 Request 2|Pulse|
||MCAN7|mcanss7_fe_3|IN_INTR216|MCAN7 Request 3|Pulse|
||MCAN7|mcanss7_fe_4|IN_INTR217|MCAN7 Request 4|Pulse|
||MCAN7|mcanss7_fe_5|IN_INTR218|MCAN7 Request 5|Pulse|
||MCAN7|mcanss7_fe_6|IN_INTR219|MCAN7 Request 6|Pulse|
||SPI5|SPI5_dma_Read_req0|IN_INTR220|SPI5 DMA Read Request 0|Pulse|
||SPI5|SPI5_dma_Read_req1|IN_INTR221|SPI5 DMA Read Request 1|Pulse|
||SPI5|SPI5_dma_Read_req2|IN_INTR222|SPI5 DMA Read Request 2|Pulse|
||SPI5|SPI5_dma_Read_req3|IN_INTR223|SPI5 DMA Read Request 3|Pulse|
||SPI5|SPI5_dma_Write_req0|IN_INTR224|SPI5 DMA Write Request 0|Pulse|
||SPI5|SPI5_dma_Write_req1|IN_INTR225|SPI5 DMA Write Request 1|Pulse|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 975 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-11. EDMA_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Desc ription**|**Type**|
|---|---|---|---|---|---|
||SPI5|SPI5_dma_Write_req2|IN_INTR226|SPI5 DMA Write Request 2|Pulse|
||SPI5|SPI5_dma_Write_req3|IN_INTR227|SPI5 DMA Write Request 3|Pulse|
||SPI6|SPI6_dma_Read_req0|IN_INTR228|SPI6 DMA Read Request 0|Pulse|
||SPI6|SPI6_dma_Read_req1|IN_INTR229|SPI6 DMA Read Request 1|Pulse|
||SPI6|SPI6_dma_Read_req2|IN_INTR230|SPI6 DMA Read Request 2|Pulse|
||SPI6|SPI6_dma_Read_req3|IN_INTR231|SPI6 DMA Read Request 3|Pulse|
||SPI6|SPI6_dma_Write_req0|IN_INTR232|SPI6 DMA Write Request 0|Pulse|
||SPI6|SPI6_dma_Write_req1|IN_INTR233|SPI6 DMA Write Request 1|Pulse|
||SPI6|SPI6_dma_Write_req2|IN_INTR234|SPI6 DMA Write Request 2|Pulse|
||SPI6|SPI6_dma_Write_req3|IN_INTR235|SPI6 DMA Write Request 3|Pulse|
||SPI7|SPI7_dma_Read_req0|IN_INTR236|SPI7 DMA Read Request 0|Pulse|
||SPI7|SPI7_dma_Read_req1|IN_INTR237|SPI7 DMA Read Request 1|Pulse|
||SPI7|SPI7_dma_Read_req2|IN_INTR238|SPI7 DMA Read Request 2|Pulse|
||SPI7|SPI7_dma_Read_req3|IN_INTR239|SPI7 DMA Read Request 3|Pulse|
||SPI7|SPI7_dma_Write_req0|IN_INTR240|SPI7 DMA Write Request 0|Pulse|
||SPI7|SPI7_dma_Write_req1|IN_INTR241|SPI7 DMA Write Request 1|Pulse|
||SPI7|SPI7_dma_Write_req2|IN_INTR242|SPI7 DMA Write Request 2|Pulse|
||SPI7|SPI7_dma_Write_req3|IN_INTR243|SPI7 DMA Write Request 3|Pulse|
||RTI4|RTI4_DMA_0|IN_INTR244|RTI4 DMA Request 0|Pulse|
||RTI4|RTI4_DMA_1|IN_INTR245|RTI4 DMA Request 1|Pulse|
||RTI4|RTI4_DMA_2|IN_INTR246|RTI4 DMA Request 2|Pulse|
||RTI4|RTI4_DMA_3|IN_INTR247|RTI4 DMA Request 3|Pulse|
||RTI5|RTI5_DMA_0|IN_INTR248|RTI5 DMA Request 0|Pulse|
||RTI5|RTI5_DMA_1|IN_INTR249|RTI5 DMA Request 1|Pulse|
||RTI5|RTI5_DMA_2|IN_INTR250|RTI5 DMA Request 2|Pulse|
||RTI5|RTI5_DMA_3|IN_INTR251|RTI5 DMA Request 3|Pulse|
||RTI6|RTI6_DMA_0|IN_INTR252|RTI6 DMA Request 0|Pulse|
||RTI6|RTI6_DMA_1|IN_INTR253|RTI6 DMA Request 1|Pulse|
||RTI6|RTI6_DMA_2|IN_INTR254|RTI6 DMA Request 2|Pulse|
||RTI6|RTI6_DMA_3|IN_INTR255|RTI6 DMA Request 3|Pulse|
||RTI7|RTI7_DMA_0|IN_INTR256|RTI7 DMA Request 0|Pulse|
||RTI7|RTI7_DMA_1|IN_INTR257|RTI7 DMA Request 1|Pulse|
||RTI7|RTI7_DMA_2|IN_INTR258|RTI7 DMA Request 2|Pulse|
||RTI7|RTI7_DMA_3|IN_INTR259|RTI7 DMA Request 3|Pulse|



## **10.3.2.3 GPIO XBAR INTRTR0** 

There is 1x GPIO XBAR Interrupt Router module integrated in the device. The diagram below provides a visual representation of the device integration details for GPIO XBAR Interrupt router. 

976 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**==> picture [500 x 536] intentionally omitted <==**

**Figure 10-4. GPIO XBAR Interrupt Router Integration Diagram** 

The tables below summarize the device integration details of GPIO XBAR Interrupt router. 

**Table 10-12. GPIO XBAR Intrrupt router Device Integration** 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|GPIO_XBAR_INTRTR0|✓|INFRA0 VBUSP Interconnect|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

977 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

## **Table 10-13. GPIO_XBAR_INTRTR0 Clocks** 

|**Module**<br>**Instance**|**Module Clock in_intr**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|GPIO_XBAR<br>_INTRTR0|SYSCLK|SYS_CLK|MSS_RCM|200 MHz|GPIO_XBAR_INTRTR0<br>Functional and Interface<br>clock|



## **Table 10-14. GPIO_XBAR_INTRTR0 Resets** 

|**Module**<br>**Instance**|**Module Reset in_intr**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|GPIO_XBA<br>R_INTRTR<br>0|RST|SYS_RST|MSS_RCM|GPIO_XBAR_INTRTR0 Reset|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

978 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-15. GPIO_XBAR_INTRTR0 Ouput Hardware Requests** 

|**Module**<br>**Instance**|**Module XBAR**<br>**Output**|**Destination XBAR signal**|**Destination**|**Description**|**Type**|
|---|---|---|---|---|---|
|GPIO_XBAR<br>_INTRTR0|outl_intr_0|GPIO_XBAR_ICSSM_out_0|ICSSM_XBAR|Selectable Hardware Request0|Pulse|
||outl_intr_1|GPIO_XBAR_ICSSM_out_1|ICSSM_XBAR|Selectable Hardware Request1||
||outl_intr_2|GPIO_XBAR_ICSSM_out_2|ICSSM_XBAR|Selectable Hardware Request2||
||outl_intr_3|GPIO_XBAR_ICSSM_out_3|ICSSM_XBAR|Selectable Hardware Request3||
||outl_intr_4|GPIO_XBAR_EDMA_out_0|EDMA_XBAR|Selectable Hardware Request4||
||outl_intr_5|GPIO_XBAR_EDMA_out_1|EDMA_XBAR|Selectable Hardware Request5||
||outl_intr_6|GPIO_XBAR_EDMA_out_2|EDMA_XBAR|Selectable Hardware Request6||
||outl_intr_7|GPIO_XBAR_EDMA_out_3|EDMA_XBAR|Selectable Hardware Request7||
||outl_intr_8|GPIO_XBAR_TimeSync_out_0|TimeSync_XBA<br>R|Selectable Hardware Request8||
||outl_intr_9|GPIO_XBAR_TimeSync_out_1|TimeSync_XBA<br>R|Selectable Hardware Request9||
||outl_intr_10|GPIO_XBAR_TimeSync_out_2|TimeSync_XBA<br>R|Selectable Hardware Request10||
||outl_intr_11|GPIO_XBAR_TimeSync_out_3|TimeSync_XBA<br>R|Selectable Hardware Request11||
||outl_intr_12|GPIO_XBAR_TimeSync_out_4|TimeSync_XBA<br>R|Selectable Hardware Request12||
||outl_intr_13|GPIO_XBAR_TimeSync_out_5|TimeSync_XBA<br>R|Selectable Hardware Request13||
||outl_intr_14|GPIO_XBAR_VIM0_out_0|VIM_0|Selectable Hardware Request14||
||outl_intr_15|GPIO_XBAR_VIM0_out_1|VIM_0|Selectable Hardware Request15||
||outl_intr_16|GPIO_XBAR_VIM0_out_2|VIM_0|Selectable Hardware Request16||
||outl_intr_17|GPIO_XBAR_VIM0_out_3|VIM_0|Selectable Hardware Request17||
||outl_intr_18|GPIO_XBAR_VIM1_out_0|VIM_1|Selectable Hardware Request18||
||outl_intr_19|GPIO_XBAR_VIM1_out_1|VIM_1|Selectable Hardware Request19||
||outl_intr_20|GPIO_XBAR_VIM1_out_2|VIM_1|Selectable Hardware Request20||
||outl_intr_21|GPIO_XBAR_VIM1_out_3|VIM_1|Selectable Hardware Request21||
||outl_intr_22|GPIO_XBAR_VIM2_out_0|VIM_2|Selectable Hardware Request22||
||outl_intr_23|GPIO_XBAR_VIM2_out_1|VIM_2|Selectable Hardware Request23||
||outl_intr_24|GPIO_XBAR_VIM2_out_2|VIM_2|Selectable Hardware Request24||
||outl_intr_25|GPIO_XBAR_VIM2_out_3|VIM_2|Selectable Hardware Request25||
||outl_intr_26|GPIO_XBAR_VIM3_out_0|VIM_3|Selectable Hardware Request26||
||outl_intr_27|GPIO_XBAR_VIM3_out_1|VIM_3|Selectable Hardware Request27||
||outl_intr_28|GPIO_XBAR_VIM3_out_2|VIM_3|Selectable Hardware Request28||
||outl_intr_29|GPIO_XBAR_VIM3_out_3|VIM_3|Selectable Hardware Request29||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

979 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-16. GPIO_XBAR_INTRTR0 in_intr Hardware Requests** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Description**|**Type**|
|---|---|---|---|---|---|
|GPIO_XBAR_INTRTR0|GPIO_0|mux_GPIO_0|in_intr_0|gpio_144x.intr_0 in_intr|Pulse|
||GPIO_1|mux_GPIO_1|in_intr_1|gpio_144x.intr_1 in_intr||
||GPIO_2|mux_GPIO_2|in_intr_2|gpio_144x.intr_2 in_intr||
||GPIO_3|mux_GPIO_3|in_intr_3|gpio_144x.intr_3 in_intr||
||GPIO_4|mux_GPIO_4|in_intr_4|gpio_144x.intr_4 in_intr||
||GPIO_5|mux_GPIO_5|in_intr_5|gpio_144x.intr_5 in_intr||
||GPIO_6|mux_GPIO_6|in_intr_6|gpio_144x.intr_6 in_intr||
||GPIO_7|mux_GPIO_7|in_intr_7|gpio_144x.intr_7 in_intr||
||GPIO_8|mux_GPIO_8|in_intr_8|gpio_144x.intr_8 in_intr||
||GPIO_9|mux_GPIO_9|in_intr_9|gpio_144x.intr_9 in_intr||
||GPIO_10|mux_GPIO_10|in_intr_10|gpio_144x.intr_10 in_intr||
||GPIO_11|mux_GPIO_11|in_intr_11|gpio_144x.intr_11 in_intr||
||GPIO_12|mux_GPIO_12|in_intr_12|gpio_144x.intr_12 in_intr||
||GPIO_13|mux_GPIO_13|in_intr_13|gpio_144x.intr_13 in_intr||
||GPIO_14|mux_GPIO_14|in_intr_14|gpio_144x.intr_14 in_intr||
||GPIO_15|mux_GPIO_15|in_intr_15|gpio_144x.intr_15 in_intr||
||GPIO_16|mux_GPIO_16|in_intr_16|gpio_144x.intr_16 in_intr||
||GPIO_17|mux_GPIO_17|in_intr_17|gpio_144x.intr_17 in_intr||
||GPIO_18|mux_GPIO_18|in_intr_18|gpio_144x.intr_18 in_intr||
||GPIO_19|mux_GPIO_19|in_intr_19|gpio_144x.intr_19 in_intr||
||GPIO_20|mux_GPIO_20|in_intr_20|gpio_144x.intr_20 in_intr||
||GPIO_21|mux_GPIO_21|in_intr_21|gpio_144x.intr_21 in_intr||
||GPIO_22|mux_GPIO_22|in_intr_22|gpio_144x.intr_22 in_intr||
||GPIO_23|mux_GPIO_23|in_intr_23|gpio_144x.intr_23 in_intr||
||GPIO_24|mux_GPIO_24|in_intr_24|gpio_144x.intr_24 in_intr||
||GPIO_25|mux_GPIO_25|in_intr_25|gpio_144x.intr_25 in_intr||
||GPIO_26|mux_GPIO_26|in_intr_26|gpio_144x.intr_26 in_intr||
||GPIO_27|mux_GPIO_27|in_intr_27|gpio_144x.intr_27 in_intr||
||GPIO_28|mux_GPIO_28|in_intr_28|gpio_144x.intr_28 in_intr||
||GPIO_29|mux_GPIO_29|in_intr_29|gpio_144x.intr_29 in_intr||
||GPIO_30|mux_GPIO_30|in_intr_30|gpio_144x.intr_30 in_intr||
||GPIO_31|mux_GPIO_31|in_intr_31|gpio_144x.intr_31 in_intr||
||GPIO_32|mux_GPIO_32|in_intr_32|gpio_144x.intr_32 in_intr||
||GPIO_33|mux_GPIO_33|in_intr_33|gpio_144x.intr_33 in_intr||
||GPIO_34|mux_GPIO_34|in_intr_34|gpio_144x.intr_34 in_intr||
||GPIO_35|mux_GPIO_35|in_intr_35|gpio_144x.intr_35 in_intr||
||GPIO_36|mux_GPIO_36|in_intr_36|gpio_144x.intr_36 in_intr||
||GPIO_37|mux_GPIO_37|in_intr_37|gpio_144x.intr_37 in_intr||
||GPIO_38|mux_GPIO_38|in_intr_38|gpio_144x.intr_38 in_intr||
||GPIO_39|mux_GPIO_39|in_intr_39|gpio_144x.intr_38 in_intr||
||GPIO_40|mux_GPIO_40|in_intr_40|gpio_144x.intr_40 in_intr||
||GPIO_41|mux_GPIO_41|in_intr_41|gpio_144x.intr_41 in_intr||
||GPIO_42|mux_GPIO_42|in_intr_42|gpio_144x.intr_42 in_intr||
||GPIO_43|mux_GPIO_43|in_intr_43|gpio_144x.intr_43 in_intr||



980 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-16. GPIO_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Description**|**Type**|
|---|---|---|---|---|---|
||GPIO_44|mux_GPIO_44|in_intr_44|gpio_144x.intr_44 in_intr||
||GPIO_45|mux_GPIO_45|in_intr_45|gpio_144x.intr_45 in_intr||
||GPIO_46|mux_GPIO_46|in_intr_46|gpio_144x.intr_46 in_intr||
||GPIO_47|mux_GPIO_47|in_intr_47|gpio_144x.intr_47 in_intr||
||GPIO_48|mux_GPIO_48|in_intr_48|gpio_144x.intr_48 in_intr||
||GPIO_49|mux_GPIO_49|in_intr_49|gpio_144x.intr_49 in_intr||
||GPIO_50|mux_GPIO_50|in_intr_50|gpio_144x.intr_50 in_intr||
||GPIO_51|mux_GPIO_51|in_intr_51|gpio_144x.intr_51 in_intr||
||GPIO_52|mux_GPIO_52|in_intr_52|gpio_144x.intr_52 in_intr||
||GPIO_53|mux_GPIO_53|in_intr_53|gpio_144x.intr_53 in_intr||
||GPIO_54|mux_GPIO_54|in_intr_54|gpio_144x.intr_54 in_intr||
||GPIO_55|mux_GPIO_55|in_intr_55|gpio_144x.intr_55 in_intr||
||GPIO_56|mux_GPIO_56|in_intr_56|gpio_144x.intr_56 in_intr||
||GPIO_57|mux_GPIO_57|in_intr_57|gpio_144x.intr_57 in_intr||
||GPIO_58|mux_GPIO_58|in_intr_58|gpio_144x.intr_58 in_intr||
||GPIO_59|mux_GPIO_59|in_intr_59|gpio_144x.intr_59 in_intr||
||GPIO_60|mux_GPIO_60|in_intr_60|gpio_144x.intr_60 in_intr||
||GPIO_61|mux_GPIO_61|in_intr_61|gpio_144x.intr_61 in_intr||
||GPIO_62|mux_GPIO_62|in_intr_62|gpio_144x.intr_62 in_intr||
||GPIO_63|mux_GPIO_63|in_intr_63|gpio_144x.intr_63 in_intr||
||GPIO_64|mux_GPIO_64|in_intr_64|gpio_144x.intr_64 in_intr||
||GPIO_65|mux_GPIO_65|in_intr_65|gpio_144x.intr_65 in_intr||
||GPIO_66|mux_GPIO_66|in_intr_66|gpio_144x.intr_66 in_intr||
||GPIO_67|mux_GPIO_67|in_intr_67|gpio_144x.intr_67 in_intr||
||GPIO_68|mux_GPIO_68|in_intr_68|gpio_144x.intr_68 in_intr||
||GPIO_69|mux_GPIO_69|in_intr_69|gpio_144x.intr_69 in_intr||
||GPIO_70|mux_GPIO_70|in_intr_70|gpio_144x.intr_70 in_intr||
||GPIO_71|mux_GPIO_71|in_intr_71|gpio_144x.intr_71 in_intr||
||GPIO_12|mux_GPIO_72|in_intr_72|gpio_144x.intr_72 in_intr||
||GPIO_73|mux_GPIO_73|in_intr_73|gpio_144x.intr_73 in_intr||
||GPIO_74|mux_GPIO_74|in_intr_74|gpio_144x.intr_74 in_intr||
||GPIO_75|mux_GPIO_75|in_intr_75|gpio_144x.intr_75 in_intr||
||GPIO_76|mux_GPIO_76|in_intr_76|gpio_144x.intr_76 in_intr||
||GPIO_77|mux_GPIO_77|in_intr_77|gpio_144x.intr_77 in_intr||
||GPIO_78|mux_GPIO_78|in_intr_78|gpio_144x.intr_78 in_intr||
||GPIO_79|mux_GPIO_79|in_intr_79|gpio_144x.intr_79 in_intr||
||GPIO_80|mux_GPIO_80|in_intr_80|gpio_144x.intr_80 in_intr||
||GPIO_81|mux_GPIO_81|in_intr_81|gpio_144x.intr_81 in_intr||
||GPIO_82|mux_GPIO_82|in_intr_82|gpio_144x.intr_82 in_intr||
||GPIO_83|mux_GPIO_83|in_intr_83|gpio_144x.intr_83 in_intr||
||GPIO_84|mux_GPIO_84|in_intr_84|gpio_144x.intr_84 in_intr||
||GPIO_85|mux_GPIO_85|in_intr_85|gpio_144x.intr_85 in_intr||
||GPIO_86|mux_GPIO_86|in_intr_86|gpio_144x.intr_86 in_intr||
||GPIO_87|mux_GPIO_87|in_intr_87|gpio_144x.intr_87 in_intr||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 981 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-16. GPIO_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Description**|**Type**|
|---|---|---|---|---|---|
||GPIO_88|mux_GPIO_88|in_intr_88|gpio_144x.intr_88 in_intr||
||GPIO_89|mux_GPIO_89|in_intr_89|gpio_144x.intr_89 in_intr||
||GPIO_90|mux_GPIO_90|in_intr_90|gpio_144x.intr_90 in_intr||
||GPIO_91|mux_GPIO_91|in_intr_91|gpio_144x.intr_91 in_intr||
||GPIO_92|mux_GPIO_92|in_intr_92|gpio_144x.intr_92 in_intr||
||GPIO_93|mux_GPIO_93|in_intr_93|gpio_144x.intr_93 in_intr||
||GPIO_94|mux_GPIO_94|in_intr_94|gpio_144x.intr_94 in_intr||
||GPIO_95|mux_GPIO_95|in_intr_95|gpio_144x.intr_95 in_intr||
||GPIO_96|mux_GPIO_96|in_intr_96|gpio_144x.intr_96 in_intr||
||GPIO_97|mux_GPIO_97|in_intr_97|gpio_144x.intr_97 in_intr||
||GPIO_98|mux_GPIO_98|in_intr_98|gpio_144x.intr_98 in_intr||
||GPIO_99|mux_GPIO_99|in_intr_99|gpio_144x.intr_99 in_intr||
||GPIO_100|mux_GPIO_100|in_intr_100|gpio_144x.intr_100 in_intr||
||GPIO_101|mux_GPIO_101|in_intr_101|gpio_144x.intr_101 in_intr||
||GPIO_102|mux_GPIO_102|in_intr_102|gpio_144x.intr_102 in_intr||
||GPIO_103|mux_GPIO_103|in_intr_103|gpio_144x.intr_103 in_intr||
||GPIO_104|mux_GPIO_104|in_intr_104|gpio_144x.intr_104 in_intr||
||GPIO_105|mux_GPIO_105|in_intr_105|gpio_144x.intr_105 in_intr||
||GPIO_106|mux_GPIO_106|in_intr_106|gpio_144x.intr_106 in_intr||
||GPIO_107|mux_GPIO_107|in_intr_107|gpio_144x.intr_107 in_intr||
||GPIO_108|mux_GPIO_108|in_intr_108|gpio_144x.intr_108 in_intr||
||GPIO_109|mux_GPIO_109|in_intr_109|gpio_144x.intr_109 in_intr||
||GPIO_110|mux_GPIO_110|in_intr_110|gpio_144x.intr_110 in_intr||
||GPIO_111|mux_GPIO_111|in_intr_111|gpio_144x.intr_111 in_intr||
||GPIO_112|mux_GPIO_112|in_intr_112|gpio_144x.intr_112 in_intr||
||GPIO_113|mux_GPIO_113|in_intr_113|gpio_144x.intr_113 in_intr||
||GPIO_114|mux_GPIO_114|in_intr_114|gpio_144x.intr_114 in_intr||
||GPIO_115|mux_GPIO_115|in_intr_115|gpio_144x.intr_115 in_intr||
||GPIO_116|mux_GPIO_116|in_intr_116|gpio_144x.intr_116 in_intr||
||GPIO_117|mux_GPIO_117|in_intr_117|gpio_144x.intr_117 in_intr||
||GPIO_118|mux_GPIO_118|in_intr_118|gpio_144x.intr_118 in_intr||
||GPIO_119|mux_GPIO_119|in_intr_119|gpio_144x.intr_119 in_intr||
||GPIO_120|mux_GPIO_120|in_intr_120|gpio_144x.intr_120 in_intr||
||GPIO_121|mux_GPIO_121|in_intr_121|gpio_144x.intr_121 in_intr||
||GPIO_122|mux_GPIO_122|in_intr_122|gpio_144x.intr_122 in_intr||
||GPIO_123|mux_GPIO_123|in_intr_123|gpio_144x.intr_123 in_intr||



982 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-16. GPIO_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Description**|**Type**|
|---|---|---|---|---|---|
||GPIO_124|mux_GPIO_124|in_intr_124|gpio_144x.intr_124 in_intr||
||GPIO_125|mux_GPIO_125|in_intr_125|gpio_144x.intr_125 in_intr||
||GPIO_126|mux_GPIO_126|in_intr_126|gpio_144x.intr_126 in_intr||
||GPIO_127|mux_GPIO_127|in_intr_127|gpio_144x.intr_127 in_intr||
||GPIO_128|mux_GPIO_128|in_intr_128|gpio_144x.intr_128 in_intr||
||GPIO_129|mux_GPIO_129|in_intr_129|gpio_144x.intr_129 in_intr||
||GPIO_130|mux_GPIO_130|in_intr_130|gpio_144x.intr_130 in_intr||
||GPIO_131|mux_GPIO_131|in_intr_131|gpio_144x.intr_131 in_intr||
||GPIO_132|mux_GPIO_132|in_intr_132|gpio_144x.intr_132 in_intr||
||GPIO_133|mux_GPIO_133|in_intr_133|gpio_144x.intr_133 in_intr||
||GPIO_134|mux_GPIO_134|in_intr_134|gpio_144x.intr_134 in_intr||
||GPIO_135|mux_GPIO_135|in_intr_135|gpio_144x.intr_135 in_intr||
||GPIO_136|mux_GPIO_136|in_intr_136|gpio_144x.intr_136 in_intr||
||GPIO_137|mux_GPIO_137|in_intr_137|gpio_144x.intr_137 in_intr||
||GPIO_138|mux_GPIO_138|in_intr_138|gpio_144x.intr_138 in_intr||
||GPIO_139|mux_GPIO_139|in_intr_139|gpio_144x.intr_139 in_intr||
||GPIO_140|mux_GPIO_140|in_intr_140|gpio_144x.intr_140 in_intr||
||GPIO_141|mux_GPIO_141|in_intr_141|gpio_144x.intr_141 in_intr||
||GPIO_142|mux_GPIO_142|in_intr_142|gpio_144x.intr_142 in_intr||
||GPIO_143|mux_GPIO_143|in_intr_143|gpio_144x.intr_143 in_intr||
||gpio_144_0_bank<br>_intr_0|mux_GPIO_144|in_intr_144|gpio_144x.intr_144 in_intr||
||gpio_144_0_bank<br>_intr_1|mux_GPIO_145|in_intr_145|gpio_144x.intr_145 in_intr||
||gpio_144_0_bank<br>_intr_2|mux_GPIO_146|in_intr_146|gpio_144x.intr_146 in_intr||
||gpio_144_0_bank<br>_intr_3|mux_GPIO_147|in_intr_147|gpio_144x.intr_147 in_intr||
||gpio_144_0_bank<br>_intr_4|mux_GPIO_148|in_intr_148|gpio_144x.intr_148 in_intr||
||gpio_144_0_bank<br>_intr_5|mux_GPIO_149|in_intr_149|gpio_144x.intr_149 in_intr||
||gpio_144_0_bank<br>_intr_6|mux_GPIO_150|in_intr_150|gpio_144x.intr_150 in_intr||
||gpio_144_0_bank<br>_intr_7|mux_GPIO_151|in_intr_151|gpio_144x.intr_151 in_intr||
||gpio_144_0_bank<br>_intr_8|mux_GPIO_152|in_intr_152|gpio_144x.intr_152 in_intr||
||gpio_144_1_bank<br>_intr_0|mux_GPIO_153|in_intr_153|gpio_144x.intr_153 in_intr||
||gpio_144_1_bank<br>_intr_1|mux_GPIO_154|in_intr_154|gpio_144x.intr_154 in_intr||
||gpio_144_1_bank<br>_intr_2|mux_GPIO_155|in_intr_155|gpio_144x.intr_155 in_intr||
||gpio_144_1_bank<br>_intr_3|mux_GPIO_156|in_intr_156|gpio_144x.intr_156 in_intr||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

983 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-16. GPIO_XBAR_INTRTR0 in_intr Hardware Requests (continued)** 

|**Module Instance**|**Source Module**|**Source in_intr signal**|**XBAR Module**<br>**in_intr**|**Description**|**Type**|
|---|---|---|---|---|---|
||gpio_144_1_bank<br>_intr_4|mux_GPIO_157|in_intr_157|gpio_144x.intr_157 in_intr||
||gpio_144_1_bank<br>_intr_5|mux_GPIO_158|in_intr_158|gpio_144x.intr_158 in_intr||
||gpio_144_1_bank<br>_intr_6|mux_GPIO_159|in_intr_159|gpio_144x.intr_159 in_intr||
||gpio_144_1_bank<br>_intr_7|mux_GPIO_160|in_intr_160|gpio_144x.intr_160 in_intr||
||gpio_144_1_bank<br>_intr_8|mux_GPIO_161|in_intr_161|gpio_144x.intr_161 in_intr||
||gpio_144_2_bank<br>_intr_0|mux_GPIO_162|in_intr_162|gpio_144x.intr_162 in_intr||
||gpio_144_2_bank<br>_intr_1|mux_GPIO_163|in_intr_163|gpio_144x.intr_163 in_intr||
||gpio_144_2_bank<br>_intr_2|mux_GPIO_164|in_intr_164|gpio_144x.intr_164 in_intr||
||gpio_144_2_bank<br>_intr_3|mux_GPIO_165|in_intr_165|gpio_144x.intr_165 in_intr||
||gpio_144_0_bank<br>_intr_4|mux_GPIO_166|in_intr_166|gpio_144x.intr_166 in_intr||
||gpio_144_2_bank<br>_intr_5|mux_GPIO_167|in_intr_167|gpio_144x.intr_167 in_intr||
||gpio_144_2_bank<br>_intr_6|mux_GPIO_168|in_intr_168|gpio_144x.intr_168 in_intr||
||gpio_144_2_bank<br>_intr_7|mux_GPIO_169|in_intr_169|gpio_144x.intr_169 in_intr||
||gpio_144_2_bank<br>_intr_8|mux_GPIO_170|in_intr_170|gpio_144x.intr_170 in_intr||
||gpio_144_3_bank<br>_intr_0|mux_GPIO_171|in_intr_171|gpio_144x.intr_171 in_intr||
||gpio_144_3_bank<br>_intr_1|mux_GPIO_172|in_intr_172|gpio_144x.intr_172 in_intr||
||gpio_144_3_bank<br>_intr_2|mux_GPIO_173|in_intr_173|gpio_144x.intr_173 in_intr||
||gpio_144_3_bank<br>_intr_3|mux_GPIO_174|in_intr_174|gpio_144x.intr_174 in_intr||
||gpio_144_3_bank<br>_intr_4|mux_GPIO_175|in_intr_175|gpio_144x.intr_175 in_intr||
||gpio_144_3_bank<br>_intr_5|mux_GPIO_176|in_intr_176|gpio_144x.intr_176 in_intr||
||gpio_144_3_bank<br>_intr_6|mux_GPIO_177|in_intr_177|gpio_144x.intr_177 in_intr||
||gpio_144_3_bank<br>_intr_7|mux_GPIO_178|in_intr_178|gpio_144x.intr_178 in_intr||
||gpio_144_3_bank<br>_intr_8|mux_GPIO_179|in_intr_179|gpio_144x.intr_179 in_intr||



984 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

## **10.4 Interrupt Sources** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

985 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

## _**10.4.1 R5FSS0_CORE0 Interrupt Map**_ 

Table 10-17 shows the mapping of events to the R5FSS0_CORE0. 

Both R5FSS0_CORE0 and R5FSS0_CORE1 use the R5FSS0_CORE0 interrupt map when operating in lockstep mode. 

**Table 10-17. R5FSS0_CORE0 Interrupt Map** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE0_INTR_IN_0|0|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_0|Level|
|R5FSS0_CORE0_INTR_IN_1|1|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_1|Level|
|R5FSS0_CORE0_INTR_IN_2|2|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_2|Level|
|R5FSS0_CORE0_INTR_IN_3|3|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_3|Level|
|R5FSS0_CORE0_INTR_IN_4|4|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_4|Level|
|R5FSS0_CORE0_INTR_IN_5|5|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_5|Level|
|R5FSS0_CORE0_INTR_IN_6|6|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_6|Level|
|R5FSS0_CORE0_INTR_IN_7|7|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_7|Level|
|R5FSS0_CORE0_INTR_IN_8|8|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_RX_SOF_INTR_REQ_0|Pulse|
|R5FSS0_CORE0_INTR_IN_9|9|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_RX_SOF_INTR_REQ_1|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>0|10|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_TX_SOF_INTR_REQ_0|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>1|11|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_TX_SOF_INTR_REQ_1|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>2|12|R5FSS0_CORE0_INTR_CPSW0_FH_INTR|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>3|13|R5FSS0_CORE0_INTR_CPSW0_TH_INTR|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>4|14|R5FSS0_CORE0_INTR_CPSW0_TH_THRESH_INTR|Level|
|R5FSS0_CORE0_INTR_IN_1<br>5|15|R5FSS0_CORE0_INTR_CPSW0_MISC_INTR|Level|
|R5FSS0_CORE0_INTR_IN_1<br>6|16|R5FSS0_CORE0_INTR_LIN0_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>7|17|R5FSS0_CORE0_INTR_LIN0_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>8|18|R5FSS0_CORE0_INTR_LIN1_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>9|19|R5FSS0_CORE0_INTR_LIN1_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>0|20|R5FSS0_CORE0_INTR_LIN2_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>1|21|R5FSS0_CORE0_INTR_LIN2_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>2|22|R5FSS0_CORE0_INTR_LIN3_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>3|23|R5FSS0_CORE0_INTR_LIN3_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>4|24|R5FSS0_CORE0_INTR_LIN4_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>5|25|R5FSS0_CORE0_INTR_LIN4_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>6|26|R5FSS0_CORE0_INTR_MCAN0_EXT_TS_ROLLOVER_LVL_INT_0|Level|



986 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-17. R5FSS0_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE0_INTR_IN_2<br>7|27|R5FSS0_CORE0_INTR_MCAN0_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_2<br>8|28|R5FSS0_CORE0_INTR_MCAN0_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE0_INTR_IN_2<br>9|29|R5FSS0_CORE0_INTR_MCAN1_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_3<br>0|30|R5FSS0_CORE0_INTR_MCAN1_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_3<br>1|31|R5FSS0_CORE0_INTR_MCAN1_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE0_INTR_IN_3<br>2|32|R5FSS0_CORE0_INTR_MCAN2_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_3<br>3|33|R5FSS0_CORE0_INTR_MCAN2_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_3<br>4|34|R5FSS0_CORE0_INTR_MCAN2_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE0_INTR_IN_3<br>5|35|R5FSS0_CORE0_INTR_MCAN3_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_3<br>6|36|R5FSS0_CORE0_INTR_MCAN3_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_3<br>7|37|R5FSS0_CORE0_INTR_MCAN3_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE0_INTR_IN_3<br>8|38|R5FSS0_CORE0_INTR_UART0_IRQ|Level|
|R5FSS0_CORE0_INTR_IN_3<br>9|39|R5FSS0_CORE0_INTR_UART1_IRQ|Level|
|R5FSS0_CORE0_INTR_IN_4<br>0|40|R5FSS0_CORE0_INTR_UART2_IRQ|Level|
|R5FSS0_CORE0_INTR_IN_4<br>1|41|R5FSS0_CORE0_INTR_UART3_IRQ|Level|
|R5FSS0_CORE0_INTR_IN_4<br>2|42|R5FSS0_CORE0_INTR_UART4_IRQ|Level|
|R5FSS0_CORE0_INTR_IN_4<br>3|43|R5FSS0_CORE0_INTR_UART5_IRQ|Level|
|R5FSS0_CORE0_INTR_IN_4<br>4|44|R5FSS0_CORE0_INTR_I2C0_IRQ|Pulse|
|R5FSS0_CORE0_INTR_IN_4<br>5|45|R5FSS0_CORE0_INTR_I2C1_IRQ|Pulse|
|R5FSS0_CORE0_INTR_IN_4<br>6|46|R5FSS0_CORE0_INTR_I2C2_IRQ|Pulse|
|R5FSS0_CORE0_INTR_IN_4<br>7|47|R5FSS0_CORE0_INTR_I2C3_IRQ|Pulse|
|R5FSS0_CORE0_INTR_IN_4<br>8|48|R5FSS0_CORE0_INTR_DTHE_SHA_S_INT|Level|
|R5FSS0_CORE0_INTR_IN_4<br>9|49|R5FSS0_CORE0_INTR_DTHE_SHA_P_INT|Level|
|R5FSS0_CORE0_INTR_IN_5<br>0|50|R5FSS0_CORE0_INTR_DTHE_TRNG_INT|Level|
|R5FSS0_CORE0_INTR_IN_5<br>1|51|R5FSS0_CORE0_INTR_DTHE_PKAE_INT|Level|
|R5FSS0_CORE0_INTR_IN_5<br>2|52|R5FSS0_CORE0_INTR_DTHE_AES_S_INT|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 987 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-17. R5FSS0_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE0_INTR_IN_5<br>3|53|R5FSS0_CORE0_INTR_DTHE_AES_P_INT|Level|
|R5FSS0_CORE0_INTR_IN_5<br>4|54|R5FSS0_CORE0_INTR_OSPI0_INT|Level|
|R5FSS0_CORE0_INTR_IN_5<br>5|55|R5FSS0_CORE0_INTR_TPCC_A_INTG|Pulse|
|R5FSS0_CORE0_INTR_IN_5<br>6|56|R5FSS0_CORE0_INTR_TPCC_A_INT_0|Pulse|
|R5FSS0_CORE0_INTR_IN_5<br>7|57|R5FSS0_CORE0_INTR_TPCC_A_INT_1|Pulse|
|R5FSS0_CORE0_INTR_IN_5<br>8|58|R5FSS0_CORE0_INTR_TPCC_A_INT_2|Pulse|
|R5FSS0_CORE0_INTR_IN_5<br>9|59|R5FSS0_CORE0_INTR_TPCC_A_INT_3|Pulse|
|R5FSS0_CORE0_INTR_IN_6<br>0|60|R5FSS0_CORE0_INTR_TPCC_A_INT_4|Pulse|
|R5FSS0_CORE0_INTR_IN_6<br>1|61|R5FSS0_CORE0_INTR_TPCC_A_INT_5|Pulse|
|R5FSS0_CORE0_INTR_IN_6<br>2|62|R5FSS0_CORE0_INTR_TPCC_A_INT_6|Pulse|
|R5FSS0_CORE0_INTR_IN_6<br>3|63|R5FSS0_CORE0_INTR_TPCC_A_INT_7|Pulse|
|R5FSS0_CORE0_INTR_IN_6<br>4|64|R5FSS0_CORE0_INTR_TPCC_A_ERRINT|Pulse|
|R5FSS0_CORE0_INTR_IN_6<br>5|65|R5FSS0_CORE0_INTR_TPCC_A_MPINT|Pulse|
|R5FSS0_CORE0_INTR_IN_6<br>6|66|R5FSS0_CORE0_INTR_TPTC0_ERINT_0|Pulse|
|R5FSS0_CORE0_INTR_IN_6<br>7|67|R5FSS0_CORE0_INTR_TPTC0_ERINT_1|Pulse|
|R5FSS0_CORE0_INTR_IN_6<br>8|68|R5FSS0_CORE0_INTR_MCRC0_INT|Level|
|R5FSS0_CORE0_INTR_IN_6<br>9|69|R5FSS0_CORE0_INTR_MPU_ADDR_ERRAGG|Level|
|R5FSS0_CORE0_INTR_IN_7<br>0|70|R5FSS0_CORE0_INTR_MPU_PROT_ERRAGG|Level|
|R5FSS0_CORE0_INTR_IN_7<br>1|71|R5FSS0_CORE0_INTR_PBIST_DONE|Level|
|R5FSS0_CORE0_INTR_IN_7<br>2|72|R5FSS0_CORE0_INTR_TPCC_A_INTAGGR|Level|
|R5FSS0_CORE0_INTR_IN_7<br>3|73|R5FSS0_CORE0_INTR_TPCC_A_ERRAGGR|Level|
|R5FSS0_CORE0_INTR_IN_7<br>4|74|R5FSS0_CORE0_INTR_DCC0_DONE|Level|
|R5FSS0_CORE0_INTR_IN_7<br>5|75|R5FSS0_CORE0_INTR_DCC1_DONE|Level|
|R5FSS0_CORE0_INTR_IN_7<br>6|76|R5FSS0_CORE0_INTR_DCC2_DONE|Level|
|R5FSS0_CORE0_INTR_IN_7<br>7|77|R5FSS0_CORE0_INTR_DCC3_DONE|Level|
|R5FSS0_CORE0_INTR_IN_7<br>8|78|R5FSS0_CORE0_INTR_MCSPI0_INTR|Level|



988 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-17. R5FSS0_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE0_INTR_IN_7<br>9|79|R5FSS0_CORE0_INTR_MCSPI1_INTR|Level|
|R5FSS0_CORE0_INTR_IN_8<br>0|80|R5FSS0_CORE0_INTR_MCSPI2_INTR|Level|
|R5FSS0_CORE0_INTR_IN_8<br>1|81|R5FSS0_CORE0_INTR_MCSPI3_INTR|Level|
|R5FSS0_CORE0_INTR_IN_8<br>2|82|R5FSS0_CORE0_INTR_MCSPI4_INTR|Level|
|R5FSS0_CORE0_INTR_IN_8<br>3|83|R5FSS0_CORE0_INTR_MMC0_INTR|Level|
|R5FSS0_CORE0_INTR_IN_8<br>4|84|R5FSS0_CORE0_INTR_RTI0_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_8<br>5|85|R5FSS0_CORE0_INTR_RTI0_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_8<br>6|86|R5FSS0_CORE0_INTR_RTI0_INTR_2|Pulse|
|R5FSS0_CORE0_INTR_IN_8<br>7|87|R5FSS0_CORE0_INTR_RTI0_INTR_3|Pulse|
|R5FSS0_CORE0_INTR_IN_8<br>8|88|R5FSS0_CORE0_INTR_RESERVED|NA|
|R5FSS0_CORE0_INTR_IN_8<br>9|89|R5FSS0_CORE0_INTR_RTI0_OVERFLOW_INT0|Pulse|
|R5FSS0_CORE0_INTR_IN_9<br>0|90|R5FSS0_CORE0_INTR_RTI0_OVERFLOW_INT1|Pulse|
|R5FSS0_CORE0_INTR_IN_9<br>1|91|R5FSS0_CORE0_INTR_RTI1_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_9<br>2|92|R5FSS0_CORE0_INTR_RTI1_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_9<br>3|93|R5FSS0_CORE0_INTR_RTI1_INTR_2|Pulse|
|R5FSS0_CORE0_INTR_IN_9<br>4|94|R5FSS0_CORE0_INTR_RTI1_INTR_3|Pulse|
|R5FSS0_CORE0_INTR_IN_9<br>5|95|R5FSS0_CORE0_INTR_RESERVED|NA|
|R5FSS0_CORE0_INTR_IN_9<br>6|96|R5FSS0_CORE0_INTR_RTI1_OVERFLOW_INT0|Pulse|
|R5FSS0_CORE0_INTR_IN_9<br>7|97|R5FSS0_CORE0_INTR_RTI1_OVERFLOW_INT1|Pulse|
|R5FSS0_CORE0_INTR_IN_9<br>8|98|R5FSS0_CORE0_INTR_RTI2_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_9<br>9|99|R5FSS0_CORE0_INTR_RTI2_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>00|100|R5FSS0_CORE0_INTR_RTI2_INTR_2|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>01|101|R5FSS0_CORE0_INTR_RTI2_INTR_3|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>02|102|R5FSS0_CORE0_INTR_RESERVED|NA|
|R5FSS0_CORE0_INTR_IN_1<br>03|103|R5FSS0_CORE0_INTR_RTI2_OVERFLOW_INT0|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>04|104|R5FSS0_CORE0_INTR_RTI2_OVERFLOW_INT1|Pulse|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 989 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-17. R5FSS0_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE0_INTR_IN_1<br>05|105|R5FSS0_CORE0_INTR_RTI3_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>06|106|R5FSS0_CORE0_INTR_RTI3_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>07|107|R5FSS0_CORE0_INTR_RTI3_INTR_2|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>08|108|R5FSS0_CORE0_INTR_RTI3_INTR_3|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>09|109|R5FSS0_CORE0_INTR_RESERVED|NA|
|R5FSS0_CORE0_INTR_IN_1<br>10|110|R5FSS0_CORE0_INTR_RTI3_OVERFLOW_INT0|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>11|111|R5FSS0_CORE0_INTR_RTI3_OVERFLOW_INT1|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>12|112|R5FSS0_CORE0_INTR_RESERVED|NA|
|R5FSS0_CORE0_INTR_IN_1<br>13|113|R5FSS0_CORE0_INTR_ESM0_ESM_INT_CFG|Level|
|R5FSS0_CORE0_INTR_IN_1<br>14|114|R5FSS0_CORE0_INTR_ESM0_ESM_INT_HI|Level|
|R5FSS0_CORE0_INTR_IN_1<br>15|115|R5FSS0_CORE0_INTR_ESM0_ESM_INT_LOW|Level|
|R5FSS0_CORE0_INTR_IN_1<br>16|116|R5FSS0_CORE0_INTR_R5SS0_COMMRX_0|R5SS<br>Internal|
|R5FSS0_CORE0_INTR_IN_1<br>17|117|R5FSS0_CORE0_INTR_R5SS0_COMMTX_0|R5SS<br>Internal|
|R5FSS0_CORE0_INTR_IN_1<br>18|118|R5FSS0_CORE0_INTR_R5SS0_CPU0_CTI_INT|R5SS<br>Internal|
|R5FSS0_CORE0_INTR_IN_1<br>19|119|R5FSS0_CORE0_INTR_R5SS0_CPU0_VALFIQ|R5SS<br>Internal|
|R5FSS0_CORE0_INTR_IN_1<br>20|120|R5FSS0_CORE0_INTR_R5SS0_CPU0_VALIRQ|R5SS<br>Internal|
|R5FSS0_CORE0_INTR_IN_1<br>21|121|R5FSS0_CORE0_INTR_R5SS0_CPU1_CTI_INT|R5SS<br>Internal|
|R5FSS0_CORE0_INTR_IN_1<br>22|122|R5FSS0_CORE0_INTR_R5SS1_CPU0_PMU_INT|R5SS<br>Internal|
|R5FSS0_CORE0_INTR_IN_1<br>23|123|R5FSS0_CORE0_INTR_R5SS1_CPU1_PMU_INT|R5SS<br>Internal|
|R5FSS0_CORE0_INTR_IN_1<br>24|124|R5FSS0_CORE0_INTR_MMR_ACC_ERRAGG|Level|
|R5FSS0_CORE0_INTR_IN_1<br>25|125|R5FSS0_CORE0_INTR_R5SS0_LIVELOCK_1|R5SS<br>Internal|
|R5FSS0_CORE0_INTR_IN_1<br>26|126|R5FSS0_CORE0_INTR_R5SS1_LIVELOCK_0|R5SS<br>Internal|
|R5FSS0_CORE0_INTR_IN_1<br>27|127|R5FSS0_CORE0_INTR_R5SS1_LIVELOCK_1|R5SS<br>Internal|
|R5FSS0_CORE0_INTR_IN_1<br>28|128|R5FSS0_CORE0_INTR_RTI_WDT0_NMI|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>29|129|R5FSS0_CORE0_INTR_SW_IRQ|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>30|130|R5FSS0_CORE0_INTR_R5SS0_CORE0_FPU_EXP|R5SS<br>Internal|



990 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-17. R5FSS0_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE0_INTR_IN_1<br>31|131|R5FSS0_CORE0_INTR_DEBUGSS_TXDATA_AVAIL|Level|
|R5FSS0_CORE0_INTR_IN_1<br>32|132|R5FSS0_CORE0_INTR_DEBUGSS_R5SS1_STC_DONE|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>33|133|R5FSS0_CORE0_INTR_TSENSE_H|Level|
|R5FSS0_CORE0_INTR_IN_1<br>34|134|R5FSS0_CORE0_INTR_TSENSE_L|Level|
|R5FSS0_CORE0_INTR_IN_1<br>35|135|R5FSS0_CORE0_INTR_AHB_WRITE_ERR|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>36|136|R5FSS0_CORE0_INTR_MBOX_READ_REQ|Level|
|R5FSS0_CORE0_INTR_IN_1<br>37|137|R5FSS0_CORE0_INTR_MBOX_READ_ACK|Level|
|R5FSS0_CORE0_INTR_IN_1<br>38|138|R5FSS0_CORE0_INTR_SOC_TIMESYNCXBAR1_OUT_2|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>39|139|R5FSS0_CORE0_INTR_SOC_TIMESYNCXBAR1_OUT_3|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>40|140|R5FSS0_CORE0_INTR_SOC_TIMESYNCXBAR1_OUT_4|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>41|141|R5FSS0_CORE0_INTR_SOC_TIMESYNCXBAR1_OUT_5|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>42|142|R5FSS0_CORE0_INTR_GPIO_INTRXBAR_OUT_14|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>43|143|R5FSS0_CORE0_INTR_GPIO_INTRXBAR_OUT_15|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>44|144|R5FSS0_CORE0_INTR_GPIO_INTRXBAR_OUT_16|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>45|145|R5FSS0_CORE0_INTR_GPIO_INTRXBAR_OUT_17|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>46|146|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_0|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>47|147|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_1|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>48|148|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_2|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>49|149|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_3|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>50|150|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_4|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>51|151|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_5|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>52|152|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_6|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>53|153|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_7|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>54|154|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_8|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>55|155|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_9|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>56|156|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_10|Level/<br>Pulse*|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 991 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-17. R5FSS0_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE0_INTR_IN_1<br>57|157|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_11|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>58|158|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_12|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>59|159|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_13|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>60|160|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_14|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>61|161|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_15|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>62|162|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_16|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>63|163|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_17|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>64|164|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_18|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>65|165|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_19|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>66|166|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_20|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>67|167|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_21|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>68|168|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_22|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>69|169|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_23|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>70|170|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_24|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>71|171|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_25|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>72|172|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_26|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>73|173|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_27|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>74|174|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_28|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>75|175|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_29|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>76|176|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_30|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>77|177|R5FSS0_CORE0_CONTROLSS_INTRXBAR0_OUT_31|Level/<br>Pulse*|
|R5FSS0_CORE0_INTR_IN_1<br>78|178|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_0|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>79|179|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_1|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>80|180|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_2|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>81|181|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_3|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>82|182|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_4|Pulse|



992 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-17. R5FSS0_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE0_INTR_IN_1<br>83|183|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_5|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>84|184|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_6|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>85|185|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_7|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>86|186|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_8|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>87|187|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_9|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>88|188|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_10|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>89|189|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_11|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>90|190|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_12|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>91|191|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_13|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>92|192|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_14|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>93|193|R5FSS0_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_15|Pulse|
|R5FSS0_CORE0_INTR_IN_1<br>94|194|R5FSS0_CORE0_CPSW0_CPTS_COMP|Level|
|R5FSS0_CORE0_INTR_IN_1<br>95|195|R5FSS0_CORE0_INTR_RESERVED|NA|
|R5FSS0_CORE0_INTR_IN_1<br>96|196|R5FSS0_CORE0_INTR_RESERVED|NA|
|R5FSS0_CORE0_INTR_IN_1<br>97|197|R5FSS0_CORE0_INTR_MCAN4_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_1<br>98|198|R5FSS0_CORE0_INTR_MCAN4_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_1<br>99|199|R5FSS0_CORE0_INTR_MCAN4_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE0_INTR_IN_2<br>00|200|R5FSS0_CORE0_INTR_MCAN5_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_2<br>01|201|R5FSS0_CORE0_INTR_MCAN5_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_2<br>02|202|R5FSS0_CORE0_INTR_MCAN5_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE0_INTR_IN_2<br>03|203|R5FSS0_CORE0_INTR_MCAN6_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_2<br>04|204|R5FSS0_CORE0_INTR_MCAN6_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_2<br>05|205|R5FSS0_CORE0_INTR_MCAN6_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE0_INTR_IN_2<br>06|206|R5FSS0_CORE0_INTR_MCAN7_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_2<br>07|207|R5FSS0_CORE0_INTR_MCAN7_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE0_INTR_IN_2<br>08|208|R5FSS0_CORE0_INTR_MCAN7_MCAN_LVL_INT_1|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 993 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-17. R5FSS0_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE0_INTR_IN_2<br>09|209|R5FSS0_CORE0_INTR_R5SS0_CPU0_TMU_LVF|Level|
|R5FSS0_CORE0_INTR_IN_2<br>10|210|R5FSS0_CORE0_INTR_R5SS0_CPU0_TMU_LUF|Level|
|R5FSS0_CORE0_INTR_IN_2<br>11|211|R5FSS0_CORE0_INTR_HW_RESOLVER|Level|
|R5FSS0_CORE0_INTR_IN_2<br>12|212|R5FSS0_CORE0_INTR_FSS_VBUSM_TIMEOUT|Level|
|R5FSS0_CORE0_INTR_IN_2<br>13|213|R5FSS0_CORE0_INTR_OTFA_ERROR|Level|
|R5FSS0_CORE0_INTR_IN_2<br>14|214|R5FSS0_CORE0_INTR_FOTA_STAT|Level|
|R5FSS0_CORE0_INTR_IN_2<br>15|215|R5FSS0_CORE0_INTR_FOTA_STAT_ERR|Level|
|R5FSS0_CORE0_INTR_IN_2<br>16|216|R5FSS0_CORE0_INTR_MCSPI5_INTR|Level|
|R5FSS0_CORE0_INTR_IN_2<br>17|217|R5FSS0_CORE0_INTR_MCSPI6_INTR|Level|
|R5FSS0_CORE0_INTR_IN_2<br>18|218|R5FSS0_CORE0_INTR_MCSPI7_INTR|Level|
|R5FSS0_CORE0_INTR_IN_2<br>19|219|R5FSS0_CORE0_INTR_RTI4_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>20|220|R5FSS0_CORE0_INTR_RTI4_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>21|221|R5FSS0_CORE0_INTR_RTI4_INTR_2|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>22|222|R5FSS0_CORE0_INTR_RTI4_INTR_3|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>23|223|R5FSS0_CORE0_INTR_RTI4_OVERFLOW_INT0|Level|
|R5FSS0_CORE0_INTR_IN_2<br>24|224|R5FSS0_CORE0_INTR_RTI4_OVERFLOW_INT1|Level|
|R5FSS0_CORE0_INTR_IN_2<br>25|225|R5FSS0_CORE0_INTR_RTI5_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>26|226|R5FSS0_CORE0_INTR_RTI5_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>27|227|R5FSS0_CORE0_INTR_RTI5_INTR_2|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>28|228|R5FSS0_CORE0_INTR_RTI5_INTR_3|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>29|229|R5FSS0_CORE0_INTR_RTI5_OVERFLOW_INT0|Level|
|R5FSS0_CORE0_INTR_IN_2<br>30|230|R5FSS0_CORE0_INTR_RTI5_OVERFLOW_INT1|Level|
|R5FSS0_CORE0_INTR_IN_2<br>31|231|R5FSS0_CORE0_INTR_RTI6_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>32|232|R5FSS0_CORE0_INTR_RTI6_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>33|233|R5FSS0_CORE0_INTR_RTI6_INTR_2|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>34|234|R5FSS0_CORE0_INTR_RTI6_INTR_3|Pulse|



994 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-17. R5FSS0_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE0_INTR_IN_2<br>35|235|R5FSS0_CORE0_INTR_RTI6_OVERFLOW_INT0|Level|
|R5FSS0_CORE0_INTR_IN_2<br>36|236|R5FSS0_CORE0_INTR_RTI6_OVERFLOW_INT1|Level|
|R5FSS0_CORE0_INTR_IN_2<br>37|237|R5FSS0_CORE0_INTR_RTI7_INTR_0|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>38|238|R5FSS0_CORE0_INTR_RTI7_INTR_1|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>39|239|R5FSS0_CORE0_INTR_RTI7_INTR_2|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>40|240|R5FSS0_CORE0_INTR_RTI7_INTR_3|Pulse|
|R5FSS0_CORE0_INTR_IN_2<br>41|241|R5FSS0_CORE0_INTR_RTI7_OVERFLOW_INT0|Level|
|R5FSS0_CORE0_INTR_IN_2<br>42|242|R5FSS0_CORE0_INTR_RTI7_OVERFLOW_INT1|Level|
|R5FSS0_CORE0_INTR_IN_2<br>43|243|R5FSS0_CORE0_INTR_R5SS0_CPU0_RL2_ERR|Level|
|R5FSS0_CORE0_INTR_IN_2<br>44|244|R5FSS0_CORE0_INTR_R5SS0_CPU1_RL2_ERR|Level|
|R5FSS0_CORE0_INTR_IN_2<br>45|245|R5FSS0_CORE0_INTR_R5SS1_CPU0_RL2_ERR|Level|
|R5FSS0_CORE0_INTR_IN_2<br>46|246|R5FSS0_CORE0_INTR_R5SS1_CPU1_RL2_ERR|Level|



* - Behavior can be level or pulse depending on the nature of source 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

995 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

## _**10.4.2 R5FSS0_CORE1 Interrupt Map**_ 

Table 10-18 shows the mapping of events to the R5FSS0_CORE1. 

Both R5FSS0_CORE1 and R5FSS0_CORE0 use the R5FSS0_CORE0 interrupt map when operating in lockstep mode. 

**Table 10-18. R5FSS0_CORE1 Interrupt Map** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE1_INTR_IN_0|0|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_0|Level|
|R5FSS0_CORE1_INTR_IN_1|1|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_1|Level|
|R5FSS0_CORE1_INTR_IN_2|2|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_2|Level|
|R5FSS0_CORE1_INTR_IN_3|3|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_3|Level|
|R5FSS0_CORE1_INTR_IN_4|4|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_4|Level|
|R5FSS0_CORE1_INTR_IN_5|5|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_5|Level|
|R5FSS0_CORE1_INTR_IN_6|6|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_6|Level|
|R5FSS0_CORE1_INTR_IN_7|7|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_7|Level|
|R5FSS0_CORE1_INTR_IN_8|8|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_RX_SOF_INTR_REQ_0|Pulse|
|R5FSS0_CORE1_INTR_IN_9|9|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_RX_SOF_INTR_REQ_1|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>0|10|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_TX_SOF_INTR_REQ_0|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>1|11|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_TX_SOF_INTR_REQ_1|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>2|12|R5FSS0_CORE1_INTR_CPSW0_FH_INTR|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>3|13|R5FSS0_CORE1_INTR_CPSW0_TH_INTR|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>4|14|R5FSS0_CORE1_INTR_CPSW0_TH_THRESH_INTR|Level|
|R5FSS0_CORE1_INTR_IN_1<br>5|15|R5FSS0_CORE1_INTR_CPSW0_MISC_INTR|Level|
|R5FSS0_CORE1_INTR_IN_1<br>6|16|R5FSS0_CORE1_INTR_LIN0_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>7|17|R5FSS0_CORE1_INTR_LIN0_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>8|18|R5FSS0_CORE1_INTR_LIN1_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>9|19|R5FSS0_CORE1_INTR_LIN1_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>0|20|R5FSS0_CORE1_INTR_LIN2_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>1|21|R5FSS0_CORE1_INTR_LIN2_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>2|22|R5FSS0_CORE1_INTR_LIN3_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>3|23|R5FSS0_CORE1_INTR_LIN3_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>4|24|R5FSS0_CORE1_INTR_LIN4_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>5|25|R5FSS0_CORE1_INTR_LIN4_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>6|26|R5FSS0_CORE1_INTR_MCAN0_EXT_TS_ROLLOVER_LVL_INT_0|Level|



996 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-18. R5FSS0_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE1_INTR_IN_2<br>7|27|R5FSS0_CORE1_INTR_MCAN0_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_2<br>8|28|R5FSS0_CORE1_INTR_MCAN0_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE1_INTR_IN_2<br>9|29|R5FSS0_CORE1_INTR_MCAN1_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_3<br>0|30|R5FSS0_CORE1_INTR_MCAN1_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_3<br>1|31|R5FSS0_CORE1_INTR_MCAN1_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE1_INTR_IN_3<br>2|32|R5FSS0_CORE1_INTR_MCAN2_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_3<br>3|33|R5FSS0_CORE1_INTR_MCAN2_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_3<br>4|34|R5FSS0_CORE1_INTR_MCAN2_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE1_INTR_IN_3<br>5|35|R5FSS0_CORE1_INTR_MCAN3_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_3<br>6|36|R5FSS0_CORE1_INTR_MCAN3_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_3<br>7|37|R5FSS0_CORE1_INTR_MCAN3_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE1_INTR_IN_3<br>8|38|R5FSS0_CORE1_INTR_UART0_IRQ|Level|
|R5FSS0_CORE1_INTR_IN_3<br>9|39|R5FSS0_CORE1_INTR_UART1_IRQ|Level|
|R5FSS0_CORE1_INTR_IN_4<br>0|40|R5FSS0_CORE1_INTR_UART2_IRQ|Level|
|R5FSS0_CORE1_INTR_IN_4<br>1|41|R5FSS0_CORE1_INTR_UART3_IRQ|Level|
|R5FSS0_CORE1_INTR_IN_4<br>2|42|R5FSS0_CORE1_INTR_UART4_IRQ|Level|
|R5FSS0_CORE1_INTR_IN_4<br>3|43|R5FSS0_CORE1_INTR_UART5_IRQ|Level|
|R5FSS0_CORE1_INTR_IN_4<br>4|44|R5FSS0_CORE1_INTR_I2C0_IRQ|Pulse|
|R5FSS0_CORE1_INTR_IN_4<br>5|45|R5FSS0_CORE1_INTR_I2C1_IRQ|Pulse|
|R5FSS0_CORE1_INTR_IN_4<br>6|46|R5FSS0_CORE1_INTR_I2C2_IRQ|Pulse|
|R5FSS0_CORE1_INTR_IN_4<br>7|47|R5FSS0_CORE1_INTR_I2C3_IRQ|Pulse|
|R5FSS0_CORE1_INTR_IN_4<br>8|48|R5FSS0_CORE1_INTR_DTHE_SHA_S_INT|Level|
|R5FSS0_CORE1_INTR_IN_4<br>9|49|R5FSS0_CORE1_INTR_DTHE_SHA_P_INT|Level|
|R5FSS0_CORE1_INTR_IN_5<br>0|50|R5FSS0_CORE1_INTR_DTHE_TRNG_INT|Level|
|R5FSS0_CORE1_INTR_IN_5<br>1|51|R5FSS0_CORE1_INTR_DTHE_PKAE_INT|Level|
|R5FSS0_CORE1_INTR_IN_5<br>2|52|R5FSS0_CORE1_INTR_DTHE_AES_S_INT|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 997 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-18. R5FSS0_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE1_INTR_IN_5<br>3|53|R5FSS0_CORE1_INTR_DTHE_AES_P_INT|Level|
|R5FSS0_CORE1_INTR_IN_5<br>4|54|R5FSS0_CORE1_INTR_OSPI0_INT|Level|
|R5FSS0_CORE1_INTR_IN_5<br>5|55|R5FSS0_CORE1_INTR_TPCC_A_INTG|Pulse|
|R5FSS0_CORE1_INTR_IN_5<br>6|56|R5FSS0_CORE1_INTR_TPCC_A_INT_0|Pulse|
|R5FSS0_CORE1_INTR_IN_5<br>7|57|R5FSS0_CORE1_INTR_TPCC_A_INT_1|Pulse|
|R5FSS0_CORE1_INTR_IN_5<br>8|58|R5FSS0_CORE1_INTR_TPCC_A_INT_2|Pulse|
|R5FSS0_CORE1_INTR_IN_5<br>9|59|R5FSS0_CORE1_INTR_TPCC_A_INT_3|Pulse|
|R5FSS0_CORE1_INTR_IN_6<br>0|60|R5FSS0_CORE1_INTR_TPCC_A_INT_4|Pulse|
|R5FSS0_CORE1_INTR_IN_6<br>1|61|R5FSS0_CORE1_INTR_TPCC_A_INT_5|Pulse|
|R5FSS0_CORE1_INTR_IN_6<br>2|62|R5FSS0_CORE1_INTR_TPCC_A_INT_6|Pulse|
|R5FSS0_CORE1_INTR_IN_6<br>3|63|R5FSS0_CORE1_INTR_TPCC_A_INT_7|Pulse|
|R5FSS0_CORE1_INTR_IN_6<br>4|64|R5FSS0_CORE1_INTR_TPCC_A_ERRINT|Pulse|
|R5FSS0_CORE1_INTR_IN_6<br>5|65|R5FSS0_CORE1_INTR_TPCC_A_MPINT|Pulse|
|R5FSS0_CORE1_INTR_IN_6<br>6|66|R5FSS0_CORE1_INTR_TPTC0_ERINT_0|Pulse|
|R5FSS0_CORE1_INTR_IN_6<br>7|67|R5FSS0_CORE1_INTR_TPTC0_ERINT_1|Pulse|
|R5FSS0_CORE1_INTR_IN_6<br>8|68|R5FSS0_CORE1_INTR_MCRC0_INT|Level|
|R5FSS0_CORE1_INTR_IN_6<br>9|69|R5FSS0_CORE1_INTR_MPU_ADDR_ERRAGG|Level|
|R5FSS0_CORE1_INTR_IN_7<br>0|70|R5FSS0_CORE1_INTR_MPU_PROT_ERRAGG|Level|
|R5FSS0_CORE1_INTR_IN_7<br>1|71|R5FSS0_CORE1_INTR_PBIST_DONE|Level|
|R5FSS0_CORE1_INTR_IN_7<br>2|72|R5FSS0_CORE1_INTR_TPCC_A_INTAGGR|Level|
|R5FSS0_CORE1_INTR_IN_7<br>3|73|R5FSS0_CORE1_INTR_TPCC_A_ERRAGGR|Level|
|R5FSS0_CORE1_INTR_IN_7<br>4|74|R5FSS0_CORE1_INTR_DCC0_DONE|Level|
|R5FSS0_CORE1_INTR_IN_7<br>5|75|R5FSS0_CORE1_INTR_DCC1_DONE|Level|
|R5FSS0_CORE1_INTR_IN_7<br>6|76|R5FSS0_CORE1_INTR_DCC2_DONE|Level|
|R5FSS0_CORE1_INTR_IN_7<br>7|77|R5FSS0_CORE1_INTR_DCC3_DONE|Level|
|R5FSS0_CORE1_INTR_IN_7<br>8|78|R5FSS0_CORE1_INTR_MCSPI0_INTR|Level|



998 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-18. R5FSS0_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE1_INTR_IN_7<br>9|79|R5FSS0_CORE1_INTR_MCSPI1_INTR|Level|
|R5FSS0_CORE1_INTR_IN_8<br>0|80|R5FSS0_CORE1_INTR_MCSPI2_INTR|Level|
|R5FSS0_CORE1_INTR_IN_8<br>1|81|R5FSS0_CORE1_INTR_MCSPI3_INTR|Level|
|R5FSS0_CORE1_INTR_IN_8<br>2|82|R5FSS0_CORE1_INTR_MCSPI4_INTR|Level|
|R5FSS0_CORE1_INTR_IN_8<br>3|83|R5FSS0_CORE1_INTR_MMC0_INTR|Level|
|R5FSS0_CORE1_INTR_IN_8<br>4|84|R5FSS0_CORE1_INTR_RTI0_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_8<br>5|85|R5FSS0_CORE1_INTR_RTI0_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_8<br>6|86|R5FSS0_CORE1_INTR_RTI0_INTR_2|Pulse|
|R5FSS0_CORE1_INTR_IN_8<br>7|87|R5FSS0_CORE1_INTR_RTI0_INTR_3|Pulse|
|R5FSS0_CORE1_INTR_IN_8<br>8|88|R5FSS0_CORE1_INTR_RESERVED|NA|
|R5FSS0_CORE1_INTR_IN_8<br>9|89|R5FSS0_CORE1_INTR_RTI0_OVERFLOW_INT0|Pulse|
|R5FSS0_CORE1_INTR_IN_9<br>0|90|R5FSS0_CORE1_INTR_RTI0_OVERFLOW_INT1|Pulse|
|R5FSS0_CORE1_INTR_IN_9<br>1|91|R5FSS0_CORE1_INTR_RTI1_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_9<br>2|92|R5FSS0_CORE1_INTR_RTI1_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_9<br>3|93|R5FSS0_CORE1_INTR_RTI1_INTR_2|Pulse|
|R5FSS0_CORE1_INTR_IN_9<br>4|94|R5FSS0_CORE1_INTR_RTI1_INTR_3|Pulse|
|R5FSS0_CORE1_INTR_IN_9<br>5|95|R5FSS0_CORE1_INTR_RESERVED|NA|
|R5FSS0_CORE1_INTR_IN_9<br>6|96|R5FSS0_CORE1_INTR_RTI1_OVERFLOW_INT0|Pulse|
|R5FSS0_CORE1_INTR_IN_9<br>7|97|R5FSS0_CORE1_INTR_RTI1_OVERFLOW_INT1|Pulse|
|R5FSS0_CORE1_INTR_IN_9<br>8|98|R5FSS0_CORE1_INTR_RTI2_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_9<br>9|99|R5FSS0_CORE1_INTR_RTI2_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>00|100|R5FSS0_CORE1_INTR_RTI2_INTR_2|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>01|101|R5FSS0_CORE1_INTR_RTI2_INTR_3|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>02|102|R5FSS0_CORE1_INTR_RESERVED|NA|
|R5FSS0_CORE1_INTR_IN_1<br>03|103|R5FSS0_CORE1_INTR_RTI2_OVERFLOW_INT0|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>04|104|R5FSS0_CORE1_INTR_RTI2_OVERFLOW_INT1|Pulse|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 999 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-18. R5FSS0_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE1_INTR_IN_1<br>05|105|R5FSS0_CORE1_INTR_RTI3_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>06|106|R5FSS0_CORE1_INTR_RTI3_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>07|107|R5FSS0_CORE1_INTR_RTI3_INTR_2|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>08|108|R5FSS0_CORE1_INTR_RTI3_INTR_3|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>09|109|R5FSS0_CORE1_INTR_RESERVED|NA|
|R5FSS0_CORE1_INTR_IN_1<br>10|110|R5FSS0_CORE1_INTR_RTI3_OVERFLOW_INT0|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>11|111|R5FSS0_CORE1_INTR_RTI3_OVERFLOW_INT1|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>12|112|R5FSS0_CORE1_INTR_RESERVED|NA|
|R5FSS0_CORE1_INTR_IN_1<br>13|113|R5FSS0_CORE1_INTR_ESM0_ESM_INT_CFG|Level|
|R5FSS0_CORE1_INTR_IN_1<br>14|114|R5FSS0_CORE1_INTR_ESM0_ESM_INT_HI|Level|
|R5FSS0_CORE1_INTR_IN_1<br>15|115|R5FSS0_CORE1_INTR_ESM0_ESM_INT_LOW|Level|
|R5FSS0_CORE1_INTR_IN_1<br>16|116|R5FSS0_CORE1_INTR_R5SS0_COMMRX_1|R5SS<br>Internal|
|R5FSS0_CORE1_INTR_IN_1<br>17|117|R5FSS0_CORE1_INTR_R5SS0_COMMTX_1|R5SS<br>Internal|
|R5FSS0_CORE1_INTR_IN_1<br>18|118|R5FSS0_CORE1_INTR_R5SS0_CPU0_CTI_INT|R5SS<br>Internal|
|R5FSS0_CORE1_INTR_IN_1<br>19|119|R5FSS0_CORE1_INTR_R5SS0_CPU1_CTI_INT|R5SS<br>Internal|
|R5FSS0_CORE1_INTR_IN_1<br>20|120|R5FSS0_CORE1_INTR_R5SS0_CPU1_VALFIQ|R5SS<br>Internal|
|R5FSS0_CORE1_INTR_IN_1<br>21|121|R5FSS0_CORE1_INTR_R5SS0_CPU1_VALIRQ|R5SS<br>Internal|
|R5FSS0_CORE1_INTR_IN_1<br>22|122|R5FSS0_CORE1_INTR_R5SS1_CPU0_PMU_INT|R5SS<br>Internal|
|R5FSS0_CORE1_INTR_IN_1<br>23|123|R5FSS0_CORE1_INTR_R5SS1_CPU1_PMU_INT|R5SS<br>Internal|
|R5FSS0_CORE1_INTR_IN_1<br>24|124|R5FSS0_CORE1_INTR_MMR_ACC_ERRAGG|Level|
|R5FSS0_CORE1_INTR_IN_1<br>25|125|R5FSS0_CORE1_INTR_R5SS0_LIVELOCK_0|R5SS<br>Internal|
|R5FSS0_CORE1_INTR_IN_1<br>26|126|R5FSS0_CORE1_INTR_R5SS1_LIVELOCK_0|R5SS<br>Internal|
|R5FSS0_CORE1_INTR_IN_1<br>27|127|R5FSS0_CORE1_INTR_R5SS1_LIVELOCK_1|R5SS<br>Internal|
|R5FSS0_CORE1_INTR_IN_1<br>28|128|R5FSS0_CORE1_INTR_RTI_WDT1_NMI|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>29|129|R5FSS0_CORE1_INTR_SW_IRQ|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>30|130|R5FSS0_CORE1_INTR_R5SS0_CORE1_FPU_EXP|R5SS<br>Internal|



1000 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-18. R5FSS0_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE1_INTR_IN_1<br>31|131|R5FSS0_CORE1_INTR_DEBUGSS_TXDATA_AVAIL|Level|
|R5FSS0_CORE1_INTR_IN_1<br>32|132|R5FSS0_CORE1_INTR_DEBUGSS_R5SS1_STC_DONE|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>33|133|R5FSS0_CORE1_INTR_TSENSE_H|Level|
|R5FSS0_CORE1_INTR_IN_1<br>34|134|R5FSS0_CORE1_INTR_TSENSE_L|Level|
|R5FSS0_CORE1_INTR_IN_1<br>35|135|R5FSS0_CORE1_INTR_AHB_WRITE_ERR|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>36|136|R5FSS0_CORE1_INTR_MBOX_READ_REQ|Level|
|R5FSS0_CORE1_INTR_IN_1<br>37|137|R5FSS0_CORE1_INTR_MBOX_READ_ACK|Level|
|R5FSS0_CORE1_INTR_IN_1<br>38|138|R5FSS0_CORE1_INTR_SOC_TIMESYNCXBAR1_OUT_6|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>39|139|R5FSS0_CORE1_INTR_SOC_TIMESYNCXBAR1_OUT_7|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>40|140|R5FSS0_CORE1_INTR_SOC_TIMESYNCXBAR1_OUT_8|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>41|141|R5FSS0_CORE1_INTR_SOC_TIMESYNCXBAR1_OUT_9|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>42|142|R5FSS0_CORE1_INTR_GPIO_INTRXBAR_OUT_18|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>43|143|R5FSS0_CORE1_INTR_GPIO_INTRXBAR_OUT_19|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>44|144|R5FSS0_CORE1_INTR_GPIO_INTRXBAR_OUT_20|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>45|145|R5FSS0_CORE1_INTR_GPIO_INTRXBAR_OUT_21|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>46|146|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_0|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>47|147|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_1|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>48|148|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_2|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>49|149|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_3|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>50|150|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_4|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>51|151|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_5|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>52|152|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_6|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>53|153|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_7|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>54|154|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_8|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>55|155|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_9|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>56|156|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_10|Level/<br>Pulse*|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1001 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-18. R5FSS0_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE1_INTR_IN_1<br>57|157|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_11|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>58|158|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_12|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>59|159|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_13|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>60|160|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_14|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>61|161|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_15|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>62|162|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_16|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>63|163|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_17|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>64|164|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_18|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>65|165|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_19|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>66|166|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_20|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>67|167|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_21|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>68|168|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_22|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>69|169|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_23|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>70|170|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_24|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>71|171|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_25|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>72|172|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_26|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>73|173|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_27|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>74|174|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_28|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>75|175|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_29|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>76|176|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_30|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>77|177|R5FSS0_CORE1_CONTROLSS_INTRXBAR0_OUT_31|Level/<br>Pulse*|
|R5FSS0_CORE1_INTR_IN_1<br>78|178|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_0|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>79|179|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_1|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>80|180|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_2|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>81|181|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_3|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>82|182|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_4|Pulse|



1002 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-18. R5FSS0_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE1_INTR_IN_1<br>83|183|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_5|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>84|184|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_6|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>85|185|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_7|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>86|186|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_8|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>87|187|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_9|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>88|188|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_10|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>89|189|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_11|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>90|190|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_12|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>91|191|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_13|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>92|192|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_14|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>93|193|R5FSS0_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_15|Pulse|
|R5FSS0_CORE1_INTR_IN_1<br>94|194|R5FSS0_CORE1_CPSW0_CPTS_COMP|Level|
|R5FSS0_CORE1_INTR_IN_1<br>95|195|R5FSS0_CORE1_INTR_RESERVED|NA|
|R5FSS0_CORE1_INTR_IN_1<br>96|196|R5FSS0_CORE1_INTR_RESERVED|NA|
|R5FSS0_CORE1_INTR_IN_1<br>97|197|R5FSS0_CORE1_INTR_MCAN4_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_1<br>98|198|R5FSS0_CORE1_INTR_MCAN4_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_1<br>99|199|R5FSS0_CORE1_INTR_MCAN4_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE1_INTR_IN_2<br>00|200|R5FSS0_CORE1_INTR_MCAN5_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_2<br>01|201|R5FSS0_CORE1_INTR_MCAN5_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_2<br>02|202|R5FSS0_CORE1_INTR_MCAN5_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE1_INTR_IN_2<br>03|203|R5FSS0_CORE1_INTR_MCAN6_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_2<br>04|204|R5FSS0_CORE1_INTR_MCAN6_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_2<br>05|205|R5FSS0_CORE1_INTR_MCAN6_MCAN_LVL_INT_1|Level|
|R5FSS0_CORE1_INTR_IN_2<br>06|206|R5FSS0_CORE1_INTR_MCAN7_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_2<br>07|207|R5FSS0_CORE1_INTR_MCAN7_MCAN_LVL_INT_0|Level|
|R5FSS0_CORE1_INTR_IN_2<br>08|208|R5FSS0_CORE1_INTR_MCAN7_MCAN_LVL_INT_1|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1003 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-18. R5FSS0_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE1_INTR_IN_2<br>09|209|R5FSS0_CORE1_INTR_R5SS0_CPU0_TMU_LVF|Level|
|R5FSS0_CORE1_INTR_IN_2<br>10|210|R5FSS0_CORE1_INTR_R5SS0_CPU0_TMU_LUF|Level|
|R5FSS0_CORE1_INTR_IN_2<br>11|211|R5FSS0_CORE1_INTR_HW_RESOLVER|Level|
|R5FSS0_CORE1_INTR_IN_2<br>12|212|R5FSS0_CORE1_INTR_FSS_VBUSM_TIMEOUT|Level|
|R5FSS0_CORE1_INTR_IN_2<br>13|213|R5FSS0_CORE1_INTR_OTFA_ERROR|Level|
|R5FSS0_CORE1_INTR_IN_2<br>14|214|R5FSS0_CORE1_INTR_FOTA_STAT|Level|
|R5FSS0_CORE1_INTR_IN_2<br>15|215|R5FSS0_CORE1_INTR_FOTA_STAT_ERR|Level|
|R5FSS0_CORE1_INTR_IN_2<br>16|216|R5FSS0_CORE1_INTR_MCSPI5_INTR|Level|
|R5FSS0_CORE1_INTR_IN_2<br>17|217|R5FSS0_CORE1_INTR_MCSPI6_INTR|Level|
|R5FSS0_CORE1_INTR_IN_2<br>18|218|R5FSS0_CORE1_INTR_MCSPI7_INTR|Level|
|R5FSS0_CORE1_INTR_IN_2<br>19|219|R5FSS0_CORE1_INTR_RTI4_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>20|220|R5FSS0_CORE1_INTR_RTI4_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>21|221|R5FSS0_CORE1_INTR_RTI4_INTR_2|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>22|222|R5FSS0_CORE1_INTR_RTI4_INTR_3|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>23|223|R5FSS0_CORE1_INTR_RTI4_OVERFLOW_INT0|Level|
|R5FSS0_CORE1_INTR_IN_2<br>24|224|R5FSS0_CORE1_INTR_RTI4_OVERFLOW_INT1|Level|
|R5FSS0_CORE1_INTR_IN_2<br>25|225|R5FSS0_CORE1_INTR_RTI5_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>26|226|R5FSS0_CORE1_INTR_RTI5_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>27|227|R5FSS0_CORE1_INTR_RTI5_INTR_2|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>28|228|R5FSS0_CORE1_INTR_RTI5_INTR_3|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>29|229|R5FSS0_CORE1_INTR_RTI5_OVERFLOW_INT0|Level|
|R5FSS0_CORE1_INTR_IN_2<br>30|230|R5FSS0_CORE1_INTR_RTI5_OVERFLOW_INT1|Level|
|R5FSS0_CORE1_INTR_IN_2<br>31|231|R5FSS0_CORE1_INTR_RTI6_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>32|232|R5FSS0_CORE1_INTR_RTI6_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>33|233|R5FSS0_CORE1_INTR_RTI6_INTR_2|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>34|234|R5FSS0_CORE1_INTR_RTI6_INTR_3|Pulse|



1004 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-18. R5FSS0_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS0_CORE1_INTR_IN_2<br>35|235|R5FSS0_CORE1_INTR_RTI6_OVERFLOW_INT0|Level|
|R5FSS0_CORE1_INTR_IN_2<br>36|236|R5FSS0_CORE1_INTR_RTI6_OVERFLOW_INT1|Level|
|R5FSS0_CORE1_INTR_IN_2<br>37|237|R5FSS0_CORE1_INTR_RTI7_INTR_0|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>38|238|R5FSS0_CORE1_INTR_RTI7_INTR_1|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>39|239|R5FSS0_CORE1_INTR_RTI7_INTR_2|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>40|240|R5FSS0_CORE1_INTR_RTI7_INTR_3|Pulse|
|R5FSS0_CORE1_INTR_IN_2<br>41|241|R5FSS0_CORE1_INTR_RTI7_OVERFLOW_INT0|Level|
|R5FSS0_CORE1_INTR_IN_2<br>42|242|R5FSS0_CORE1_INTR_RTI7_OVERFLOW_INT1|Level|
|R5FSS0_CORE1_INTR_IN_2<br>43|243|R5FSS0_CORE1_INTR_R5SS0_CPU0_RL2_ERR|Level|
|R5FSS0_CORE1_INTR_IN_2<br>44|244|R5FSS0_CORE1_INTR_R5SS0_CPU1_RL2_ERR|Level|
|R5FSS0_CORE1_INTR_IN_2<br>45|245|R5FSS0_CORE1_INTR_R5SS1_CPU0_RL2_ERR|Level|
|R5FSS0_CORE1_INTR_IN_2<br>46|246|R5FSS0_CORE1_INTR_R5SS1_CPU1_RL2_ERR|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1005 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

## _**10.4.3 R5FSS1_CORE0 Interrupt Map**_ 

Table 10-19 shows the mapping of events to the R5FSS1_CORE0. 

Both R5FSS1_CORE0 and R5FSS1_CORE1 use the R5FSS1_CORE0 interrupt map when operating in lockstep mode. 

**Table 10-19. R5FSS1_CORE0 Interrupt Map** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE0_INTR_IN_0|0|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_0|Level|
|R5FSS1_CORE0_INTR_IN_1|1|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_1|Level|
|R5FSS1_CORE0_INTR_IN_2|2|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_2|Level|
|R5FSS1_CORE0_INTR_IN_3|3|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_3|Level|
|R5FSS1_CORE0_INTR_IN_4|4|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_4|Level|
|R5FSS1_CORE0_INTR_IN_5|5|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_5|Level|
|R5FSS1_CORE0_INTR_IN_6|6|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_6|Level|
|R5FSS1_CORE0_INTR_IN_7|7|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_7|Level|
|R5FSS1_CORE0_INTR_IN_8|8|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_RX_SOF_INTR_REQ_0|Pulse|
|R5FSS1_CORE0_INTR_IN_9|9|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_RX_SOF_INTR_REQ_1|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>0|10|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_TX_SOF_INTR_REQ_0|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>1|11|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_TX_SOF_INTR_REQ_1|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>2|12|R5FSS1_CORE0_INTR_CPSW0_FH_INTR|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>3|13|R5FSS1_CORE0_INTR_CPSW0_TH_INTR|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>4|14|R5FSS1_CORE0_INTR_CPSW0_TH_THRESH_INTR|Level|
|R5FSS1_CORE0_INTR_IN_1<br>5|15|R5FSS1_CORE0_INTR_CPSW0_MISC_INTR|Level|
|R5FSS1_CORE0_INTR_IN_1<br>6|16|R5FSS1_CORE0_INTR_LIN0_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>7|17|R5FSS1_CORE0_INTR_LIN0_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>8|18|R5FSS1_CORE0_INTR_LIN1_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>9|19|R5FSS1_CORE0_INTR_LIN1_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>0|20|R5FSS1_CORE0_INTR_LIN2_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>1|21|R5FSS1_CORE0_INTR_LIN2_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>2|22|R5FSS1_CORE0_INTR_LIN3_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>3|23|R5FSS1_CORE0_INTR_LIN3_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>4|24|R5FSS1_CORE0_INTR_LIN4_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>5|25|R5FSS1_CORE0_INTR_LIN4_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>6|26|R5FSS1_CORE0_INTR_MCAN0_EXT_TS_ROLLOVER_LVL_INT_0|Level|



1006 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-19. R5FSS1_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE0_INTR_IN_2<br>7|27|R5FSS1_CORE0_INTR_MCAN0_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_2<br>8|28|R5FSS1_CORE0_INTR_MCAN0_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE0_INTR_IN_2<br>9|29|R5FSS1_CORE0_INTR_MCAN1_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_3<br>0|30|R5FSS1_CORE0_INTR_MCAN1_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_3<br>1|31|R5FSS1_CORE0_INTR_MCAN1_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE0_INTR_IN_3<br>2|32|R5FSS1_CORE0_INTR_MCAN2_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_3<br>3|33|R5FSS1_CORE0_INTR_MCAN2_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_3<br>4|34|R5FSS1_CORE0_INTR_MCAN2_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE0_INTR_IN_3<br>5|35|R5FSS1_CORE0_INTR_MCAN3_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_3<br>6|36|R5FSS1_CORE0_INTR_MCAN3_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_3<br>7|37|R5FSS1_CORE0_INTR_MCAN3_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE0_INTR_IN_3<br>8|38|R5FSS1_CORE0_INTR_UART0_IRQ|Level|
|R5FSS1_CORE0_INTR_IN_3<br>9|39|R5FSS1_CORE0_INTR_UART1_IRQ|Level|
|R5FSS1_CORE0_INTR_IN_4<br>0|40|R5FSS1_CORE0_INTR_UART2_IRQ|Level|
|R5FSS1_CORE0_INTR_IN_4<br>1|41|R5FSS1_CORE0_INTR_UART3_IRQ|Level|
|R5FSS1_CORE0_INTR_IN_4<br>2|42|R5FSS1_CORE0_INTR_UART4_IRQ|Level|
|R5FSS1_CORE0_INTR_IN_4<br>3|43|R5FSS1_CORE0_INTR_UART5_IRQ|Level|
|R5FSS1_CORE0_INTR_IN_4<br>4|44|R5FSS1_CORE0_INTR_I2C0_IRQ|Pulse|
|R5FSS1_CORE0_INTR_IN_4<br>5|45|R5FSS1_CORE0_INTR_I2C1_IRQ|Pulse|
|R5FSS1_CORE0_INTR_IN_4<br>6|46|R5FSS1_CORE0_INTR_I2C2_IRQ|Pulse|
|R5FSS1_CORE0_INTR_IN_4<br>7|47|R5FSS1_CORE0_INTR_I2C3_IRQ|Pulse|
|R5FSS1_CORE0_INTR_IN_4<br>8|48|R5FSS1_CORE0_INTR_DTHE_SHA_S_INT|Level|
|R5FSS1_CORE0_INTR_IN_4<br>9|49|R5FSS1_CORE0_INTR_DTHE_SHA_P_INT|Level|
|R5FSS1_CORE0_INTR_IN_5<br>0|50|R5FSS1_CORE0_INTR_DTHE_TRNG_INT|Level|
|R5FSS1_CORE0_INTR_IN_5<br>1|51|R5FSS1_CORE0_INTR_DTHE_PKAE_INT|Level|
|R5FSS1_CORE0_INTR_IN_5<br>2|52|R5FSS1_CORE0_INTR_DTHE_AES_S_INT|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1007 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-19. R5FSS1_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE0_INTR_IN_5<br>3|53|R5FSS1_CORE0_INTR_DTHE_AES_P_INT|Level|
|R5FSS1_CORE0_INTR_IN_5<br>4|54|R5FSS1_CORE0_INTR_OSPI0_INT|Level|
|R5FSS1_CORE0_INTR_IN_5<br>5|55|R5FSS1_CORE0_INTR_TPCC_A_INTG|Pulse|
|R5FSS1_CORE0_INTR_IN_5<br>6|56|R5FSS1_CORE0_INTR_TPCC_A_INT_0|Pulse|
|R5FSS1_CORE0_INTR_IN_5<br>7|57|R5FSS1_CORE0_INTR_TPCC_A_INT_1|Pulse|
|R5FSS1_CORE0_INTR_IN_5<br>8|58|R5FSS1_CORE0_INTR_TPCC_A_INT_2|Pulse|
|R5FSS1_CORE0_INTR_IN_5<br>9|59|R5FSS1_CORE0_INTR_TPCC_A_INT_3|Pulse|
|R5FSS1_CORE0_INTR_IN_6<br>0|60|R5FSS1_CORE0_INTR_TPCC_A_INT_4|Pulse|
|R5FSS1_CORE0_INTR_IN_6<br>1|61|R5FSS1_CORE0_INTR_TPCC_A_INT_5|Pulse|
|R5FSS1_CORE0_INTR_IN_6<br>2|62|R5FSS1_CORE0_INTR_TPCC_A_INT_6|Pulse|
|R5FSS1_CORE0_INTR_IN_6<br>3|63|R5FSS1_CORE0_INTR_TPCC_A_INT_7|Pulse|
|R5FSS1_CORE0_INTR_IN_6<br>4|64|R5FSS1_CORE0_INTR_TPCC_A_ERRINT|Pulse|
|R5FSS1_CORE0_INTR_IN_6<br>5|65|R5FSS1_CORE0_INTR_TPCC_A_MPINT|Pulse|
|R5FSS1_CORE0_INTR_IN_6<br>6|66|R5FSS1_CORE0_INTR_TPTC0_ERINT_0|Pulse|
|R5FSS1_CORE0_INTR_IN_6<br>7|67|R5FSS1_CORE0_INTR_TPTC0_ERINT_1|Pulse|
|R5FSS1_CORE0_INTR_IN_6<br>8|68|R5FSS1_CORE0_INTR_MCRC0_INT|Level|
|R5FSS1_CORE0_INTR_IN_6<br>9|69|R5FSS1_CORE0_INTR_MPU_ADDR_ERRAGG|Level|
|R5FSS1_CORE0_INTR_IN_7<br>0|70|R5FSS1_CORE0_INTR_MPU_PROT_ERRAGG|Level|
|R5FSS1_CORE0_INTR_IN_7<br>1|71|R5FSS1_CORE0_INTR_PBIST_DONE|Level|
|R5FSS1_CORE0_INTR_IN_7<br>2|72|R5FSS1_CORE0_INTR_TPCC_A_INTAGGR|Level|
|R5FSS1_CORE0_INTR_IN_7<br>3|73|R5FSS1_CORE0_INTR_TPCC_A_ERRAGGR|Level|
|R5FSS1_CORE0_INTR_IN_7<br>4|74|R5FSS1_CORE0_INTR_DCC0_DONE|Level|
|R5FSS1_CORE0_INTR_IN_7<br>5|75|R5FSS1_CORE0_INTR_DCC1_DONE|Level|
|R5FSS1_CORE0_INTR_IN_7<br>6|76|R5FSS1_CORE0_INTR_DCC2_DONE|Level|
|R5FSS1_CORE0_INTR_IN_7<br>7|77|R5FSS1_CORE0_INTR_DCC3_DONE|Level|
|R5FSS1_CORE0_INTR_IN_7<br>8|78|R5FSS1_CORE0_INTR_MCSPI0_INTR|Level|



1008 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-19. R5FSS1_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE0_INTR_IN_7<br>9|79|R5FSS1_CORE0_INTR_MCSPI1_INTR|Level|
|R5FSS1_CORE0_INTR_IN_8<br>0|80|R5FSS1_CORE0_INTR_MCSPI2_INTR|Level|
|R5FSS1_CORE0_INTR_IN_8<br>1|81|R5FSS1_CORE0_INTR_MCSPI3_INTR|Level|
|R5FSS1_CORE0_INTR_IN_8<br>2|82|R5FSS1_CORE0_INTR_MCSPI4_INTR|Level|
|R5FSS1_CORE0_INTR_IN_8<br>3|83|R5FSS1_CORE0_INTR_MMC0_INTR|Level|
|R5FSS1_CORE0_INTR_IN_8<br>4|84|R5FSS1_CORE0_INTR_RTI0_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_8<br>5|85|R5FSS1_CORE0_INTR_RTI0_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_8<br>6|86|R5FSS1_CORE0_INTR_RTI0_INTR_2|Pulse|
|R5FSS1_CORE0_INTR_IN_8<br>7|87|R5FSS1_CORE0_INTR_RTI0_INTR_3|Pulse|
|R5FSS1_CORE0_INTR_IN_8<br>8|88|R5FSS1_CORE0_INTR_RESERVED|NA|
|R5FSS1_CORE0_INTR_IN_8<br>9|89|R5FSS1_CORE0_INTR_RTI0_OVERFLOW_INT0|Pulse|
|R5FSS1_CORE0_INTR_IN_9<br>0|90|R5FSS1_CORE0_INTR_RTI0_OVERFLOW_INT1|Pulse|
|R5FSS1_CORE0_INTR_IN_9<br>1|91|R5FSS1_CORE0_INTR_RTI1_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_9<br>2|92|R5FSS1_CORE0_INTR_RTI1_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_9<br>3|93|R5FSS1_CORE0_INTR_RTI1_INTR_2|Pulse|
|R5FSS1_CORE0_INTR_IN_9<br>4|94|R5FSS1_CORE0_INTR_RTI1_INTR_3|Pulse|
|R5FSS1_CORE0_INTR_IN_9<br>5|95|R5FSS1_CORE0_INTR_RESERVED|NA|
|R5FSS1_CORE0_INTR_IN_9<br>6|96|R5FSS1_CORE0_INTR_RTI1_OVERFLOW_INT0|Pulse|
|R5FSS1_CORE0_INTR_IN_9<br>7|97|R5FSS1_CORE0_INTR_RTI1_OVERFLOW_INT1|Pulse|
|R5FSS1_CORE0_INTR_IN_9<br>8|98|R5FSS1_CORE0_INTR_RTI2_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_9<br>9|99|R5FSS1_CORE0_INTR_RTI2_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>00|100|R5FSS1_CORE0_INTR_RTI2_INTR_2|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>01|101|R5FSS1_CORE0_INTR_RTI2_INTR_3|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>02|102|R5FSS1_CORE0_INTR_RESERVED|NA|
|R5FSS1_CORE0_INTR_IN_1<br>03|103|R5FSS1_CORE0_INTR_RTI2_OVERFLOW_INT0|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>04|104|R5FSS1_CORE0_INTR_RTI2_OVERFLOW_INT1|Pulse|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1009 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-19. R5FSS1_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE0_INTR_IN_1<br>05|105|R5FSS1_CORE0_INTR_RTI3_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>06|106|R5FSS1_CORE0_INTR_RTI3_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>07|107|R5FSS1_CORE0_INTR_RTI3_INTR_2|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>08|108|R5FSS1_CORE0_INTR_RTI3_INTR_3|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>09|109|R5FSS1_CORE0_INTR_RESERVED|NA|
|R5FSS1_CORE0_INTR_IN_1<br>10|110|R5FSS1_CORE0_INTR_RTI3_OVERFLOW_INT0|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>11|111|R5FSS1_CORE0_INTR_RTI3_OVERFLOW_INT1|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>12|112|R5FSS1_CORE0_INTR_RESERVED|NA|
|R5FSS1_CORE0_INTR_IN_1<br>13|113|R5FSS1_CORE0_INTR_ESM0_ESM_INT_CFG|Level|
|R5FSS1_CORE0_INTR_IN_1<br>14|114|R5FSS1_CORE0_INTR_ESM0_ESM_INT_HI|Level|
|R5FSS1_CORE0_INTR_IN_1<br>15|115|R5FSS1_CORE0_INTR_ESM0_ESM_INT_LOW|Level|
|R5FSS1_CORE0_INTR_IN_1<br>16|116|R5FSS1_CORE0_INTR_R5SS0_CPU0_PMU_INT|R5SS<br>Internal|
|R5FSS1_CORE0_INTR_IN_1<br>17|117|R5FSS1_CORE0_INTR_R5SS0_CPU1_PMU_INT|R5SS<br>Internal|
|R5FSS1_CORE0_INTR_IN_1<br>18|118|R5FSS1_CORE0_INTR_R5SS1_COMMRX_0|R5SS<br>Internal|
|R5FSS1_CORE0_INTR_IN_1<br>19|119|R5FSS1_CORE0_INTR_R5SS1_COMMTX_0|R5SS<br>Internal|
|R5FSS1_CORE0_INTR_IN_1<br>20|120|R5FSS1_CORE0_INTR_R5SS1_CPU0_CTI_INT|R5SS<br>Internal|
|R5FSS1_CORE0_INTR_IN_1<br>21|121|R5FSS1_CORE0_INTR_R5SS1_CPU0_VALFIQ|R5SS<br>Internal|
|R5FSS1_CORE0_INTR_IN_1<br>22|122|R5FSS1_CORE0_INTR_R5SS1_CPU0_VALIRQ|R5SS<br>Internal|
|R5FSS1_CORE0_INTR_IN_1<br>23|123|R5FSS1_CORE0_INTR_R5SS1_CPU1_CTI_INT|R5SS<br>Internal|
|R5FSS1_CORE0_INTR_IN_1<br>24|124|R5FSS1_CORE0_INTR_MMR_ACC_ERRAGG|Level|
|R5FSS1_CORE0_INTR_IN_1<br>25|125|R5FSS1_CORE0_INTR_R5SS1_LIVELOCK_1|R5SS<br>Internal|
|R5FSS1_CORE0_INTR_IN_1<br>26|126|R5FSS1_CORE0_INTR_R5SS0_LIVELOCK_0|R5SS<br>Internal|
|R5FSS1_CORE0_INTR_IN_1<br>27|127|R5FSS1_CORE0_INTR_R5SS0_LIVELOCK_1|R5SS<br>Internal|
|R5FSS1_CORE0_INTR_IN_1<br>28|128|R5FSS1_CORE0_INTR_RTI_WDT2_NMI|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>29|129|R5FSS1_CORE0_INTR_SW_IRQ|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>30|130|R5FSS1_CORE0_INTR_R5SS1_CORE0_FPU_EXP|R5SS<br>Internal|



1010 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-19. R5FSS1_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE0_INTR_IN_1<br>31|131|R5FSS1_CORE0_INTR_DEBUGSS_TXDATA_AVAIL|Level|
|R5FSS1_CORE0_INTR_IN_1<br>32|132|R5FSS1_CORE0_INTR_DEBUGSS_R5SS0_STC_DONE|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>33|133|R5FSS1_CORE0_INTR_TSENSE_H|Level|
|R5FSS1_CORE0_INTR_IN_1<br>34|134|R5FSS1_CORE0_INTR_TSENSE_L|Level|
|R5FSS1_CORE0_INTR_IN_1<br>35|135|R5FSS1_CORE0_INTR_AHB_WRITE_ERR|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>36|136|R5FSS1_CORE0_INTR_MBOX_READ_REQ|Level|
|R5FSS1_CORE0_INTR_IN_1<br>37|137|R5FSS1_CORE0_INTR_MBOX_READ_ACK|Level|
|R5FSS1_CORE0_INTR_IN_1<br>38|138|R5FSS1_CORE0_INTR_SOC_TIMESYNCXBAR1_OUT_26|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>39|139|R5FSS1_CORE0_INTR_SOC_TIMESYNCXBAR1_OUT_27|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>40|140|R5FSS1_CORE0_INTR_SOC_TIMESYNCXBAR1_OUT_28|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>41|141|R5FSS1_CORE0_INTR_SOC_TIMESYNCXBAR1_OUT_29|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>42|142|R5FSS1_CORE0_INTR_GPIO_INTRXBAR_OUT_22|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>43|143|R5FSS1_CORE0_INTR_GPIO_INTRXBAR_OUT_23|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>44|144|R5FSS1_CORE0_INTR_GPIO_INTRXBAR_OUT_24|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>45|145|R5FSS1_CORE0_INTR_GPIO_INTRXBAR_OUT_25|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>46|146|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_0|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>47|147|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_1|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>48|148|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_2|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>49|149|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_3|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>50|150|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_4|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>51|151|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_5|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>52|152|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_6|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>53|153|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_7|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>54|154|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_8|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>55|155|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_9|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>56|156|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_10|Level/<br>Pulse*|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1011 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-19. R5FSS1_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE0_INTR_IN_1<br>57|157|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_11|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>58|158|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_12|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>59|159|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_13|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>60|160|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_14|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>61|161|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_15|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>62|162|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_16|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>63|163|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_17|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>64|164|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_18|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>65|165|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_19|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>66|166|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_20|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>67|167|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_21|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>68|168|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_22|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>69|169|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_23|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>70|170|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_24|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>71|171|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_25|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>72|172|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_26|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>73|173|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_27|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>74|174|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_28|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>75|175|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_29|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>76|176|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_30|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>77|177|R5FSS1_CORE0_CONTROLSS_INTRXBAR0_OUT_31|Level/<br>Pulse*|
|R5FSS1_CORE0_INTR_IN_1<br>78|178|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_0|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>79|179|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_1|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>80|180|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_2|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>81|181|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_3|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>82|182|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_4|Pulse|



1012 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-19. R5FSS1_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE0_INTR_IN_1<br>83|183|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_5|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>84|184|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_6|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>85|185|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_7|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>86|186|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_8|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>87|187|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_9|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>88|188|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_10|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>89|189|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_11|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>90|190|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_12|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>91|191|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_13|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>92|192|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_14|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>93|193|R5FSS1_CORE0_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_15|Pulse|
|R5FSS1_CORE0_INTR_IN_1<br>94|194|R5FSS1_CORE0_CPSW0_CPTS_COMP|Level|
|R5FSS1_CORE0_INTR_IN_1<br>95|195|R5FSS1_CORE0_INTR_RESERVED|NA|
|R5FSS1_CORE0_INTR_IN_1<br>96|196|R5FSS1_CORE0_INTR_RESERVED|NA|
|R5FSS1_CORE0_INTR_IN_1<br>97|197|R5FSS1_CORE0_INTR_MCAN4_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_1<br>98|198|R5FSS1_CORE0_INTR_MCAN4_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_1<br>99|199|R5FSS1_CORE0_INTR_MCAN4_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE0_INTR_IN_2<br>00|200|R5FSS1_CORE0_INTR_MCAN5_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_2<br>01|201|R5FSS1_CORE0_INTR_MCAN5_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_2<br>02|202|R5FSS1_CORE0_INTR_MCAN5_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE0_INTR_IN_2<br>03|203|R5FSS1_CORE0_INTR_MCAN6_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_2<br>04|204|R5FSS1_CORE0_INTR_MCAN6_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_2<br>05|205|R5FSS1_CORE0_INTR_MCAN6_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE0_INTR_IN_2<br>06|206|R5FSS1_CORE0_INTR_MCAN7_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_2<br>07|207|R5FSS1_CORE0_INTR_MCAN7_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE0_INTR_IN_2<br>08|208|R5FSS1_CORE0_INTR_MCAN7_MCAN_LVL_INT_1|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1013 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-19. R5FSS1_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE0_INTR_IN_2<br>09|209|R5FSS1_CORE0_INTR_R5SS0_CPU0_TMU_LVF|Level|
|R5FSS1_CORE0_INTR_IN_2<br>10|210|R5FSS1_CORE0_INTR_R5SS0_CPU0_TMU_LUF|Level|
|R5FSS1_CORE0_INTR_IN_2<br>11|211|R5FSS1_CORE0_INTR_HW_RESOLVER|Level|
|R5FSS1_CORE0_INTR_IN_2<br>12|212|R5FSS1_CORE0_INTR_FSS_VBUSM_TIMEOUT|Level|
|R5FSS1_CORE0_INTR_IN_2<br>13|213|R5FSS1_CORE0_INTR_OTFA_ERROR|Level|
|R5FSS1_CORE0_INTR_IN_2<br>14|214|R5FSS1_CORE0_INTR_FOTA_STAT|Level|
|R5FSS1_CORE0_INTR_IN_2<br>15|215|R5FSS1_CORE0_INTR_FOTA_STAT_ERR|Level|
|R5FSS1_CORE0_INTR_IN_2<br>16|216|R5FSS1_CORE0_INTR_MCSPI5_INTR|Level|
|R5FSS1_CORE0_INTR_IN_2<br>17|217|R5FSS1_CORE0_INTR_MCSPI6_INTR|Level|
|R5FSS1_CORE0_INTR_IN_2<br>18|218|R5FSS1_CORE0_INTR_MCSPI7_INTR|Level|
|R5FSS1_CORE0_INTR_IN_2<br>19|219|R5FSS1_CORE0_INTR_RTI4_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>20|220|R5FSS1_CORE0_INTR_RTI4_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>21|221|R5FSS1_CORE0_INTR_RTI4_INTR_2|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>22|222|R5FSS1_CORE0_INTR_RTI4_INTR_3|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>23|223|R5FSS1_CORE0_INTR_RTI4_OVERFLOW_INT0|Level|
|R5FSS1_CORE0_INTR_IN_2<br>24|224|R5FSS1_CORE0_INTR_RTI4_OVERFLOW_INT1|Level|
|R5FSS1_CORE0_INTR_IN_2<br>25|225|R5FSS1_CORE0_INTR_RTI5_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>26|226|R5FSS1_CORE0_INTR_RTI5_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>27|227|R5FSS1_CORE0_INTR_RTI5_INTR_2|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>28|228|R5FSS1_CORE0_INTR_RTI5_INTR_3|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>29|229|R5FSS1_CORE0_INTR_RTI5_OVERFLOW_INT0|Level|
|R5FSS1_CORE0_INTR_IN_2<br>30|230|R5FSS1_CORE0_INTR_RTI5_OVERFLOW_INT1|Level|
|R5FSS1_CORE0_INTR_IN_2<br>31|231|R5FSS1_CORE0_INTR_RTI6_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>32|232|R5FSS1_CORE0_INTR_RTI6_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>33|233|R5FSS1_CORE0_INTR_RTI6_INTR_2|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>34|234|R5FSS1_CORE0_INTR_RTI6_INTR_3|Pulse|



1014 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-19. R5FSS1_CORE0 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE0_INTR_IN_2<br>35|235|R5FSS1_CORE0_INTR_RTI6_OVERFLOW_INT0|Level|
|R5FSS1_CORE0_INTR_IN_2<br>36|236|R5FSS1_CORE0_INTR_RTI6_OVERFLOW_INT1|Level|
|R5FSS1_CORE0_INTR_IN_2<br>37|237|R5FSS1_CORE0_INTR_RTI7_INTR_0|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>38|238|R5FSS1_CORE0_INTR_RTI7_INTR_1|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>39|239|R5FSS1_CORE0_INTR_RTI7_INTR_2|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>40|240|R5FSS1_CORE0_INTR_RTI7_INTR_3|Pulse|
|R5FSS1_CORE0_INTR_IN_2<br>41|241|R5FSS1_CORE0_INTR_RTI7_OVERFLOW_INT0|Level|
|R5FSS1_CORE0_INTR_IN_2<br>42|242|R5FSS1_CORE0_INTR_RTI7_OVERFLOW_INT1|Level|
|R5FSS1_CORE0_INTR_IN_2<br>43|243|R5FSS1_CORE0_INTR_R5SS0_CPU0_RL2_ERR|Level|
|R5FSS1_CORE0_INTR_IN_2<br>44|244|R5FSS1_CORE0_INTR_R5SS0_CPU1_RL2_ERR|Level|
|R5FSS1_CORE0_INTR_IN_2<br>45|245|R5FSS1_CORE0_INTR_R5SS1_CPU0_RL2_ERR|Level|
|R5FSS1_CORE0_INTR_IN_2<br>46|246|R5FSS1_CORE0_INTR_R5SS1_CPU1_RL2_ERR|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1015 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

## _**10.4.4 R5FSS1_CORE1 Interrupt Map**_ 

Table 10-20 shows the mapping of events to the R5FSS1_CORE1. 

Both R5FSS1_CORE1 and R5FSS1_CORE0 use the R5FSS1_CORE0 interrupt map when operating in lockstep mode. 

**Table 10-20. R5FSS1_CORE1 Interrupt Map** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE1_INTR_IN_0|0|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_0|Level|
|R5FSS1_CORE1_INTR_IN_1|1|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_1|Level|
|R5FSS1_CORE1_INTR_IN_2|2|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_2|Level|
|R5FSS1_CORE1_INTR_IN_3|3|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_3|Level|
|R5FSS1_CORE1_INTR_IN_4|4|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_4|Level|
|R5FSS1_CORE1_INTR_IN_5|5|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_5|Level|
|R5FSS1_CORE1_INTR_IN_6|6|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_6|Level|
|R5FSS1_CORE1_INTR_IN_7|7|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_HOST_INTR_PEND_7|Level|
|R5FSS1_CORE1_INTR_IN_8|8|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_RX_SOF_INTR_REQ_0|Pulse|
|R5FSS1_CORE1_INTR_IN_9|9|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_RX_SOF_INTR_REQ_1|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>0|10|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_TX_SOF_INTR_REQ_0|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>1|11|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_TX_SOF_INTR_REQ_1|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>2|12|R5FSS1_CORE1_INTR_CPSW0_FH_INTR|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>3|13|R5FSS1_CORE1_INTR_CPSW0_TH_INTR|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>4|14|R5FSS1_CORE1_INTR_CPSW0_TH_THRESH_INTR|Level|
|R5FSS1_CORE1_INTR_IN_1<br>5|15|R5FSS1_CORE1_INTR_CPSW0_MISC_INTR|Level|
|R5FSS1_CORE1_INTR_IN_1<br>6|16|R5FSS1_CORE1_INTR_LIN0_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>7|17|R5FSS1_CORE1_INTR_LIN0_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>8|18|R5FSS1_CORE1_INTR_LIN1_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>9|19|R5FSS1_CORE1_INTR_LIN1_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>0|20|R5FSS1_CORE1_INTR_LIN2_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>1|21|R5FSS1_CORE1_INTR_LIN2_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>2|22|R5FSS1_CORE1_INTR_LIN3_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>3|23|R5FSS1_CORE1_INTR_LIN3_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>4|24|R5FSS1_CORE1_INTR_LIN4_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>5|25|R5FSS1_CORE1_INTR_LIN4_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>6|26|R5FSS1_CORE1_INTR_MCAN0_EXT_TS_ROLLOVER_LVL_INT_0|Level|



1016 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-20. R5FSS1_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE1_INTR_IN_2<br>7|27|R5FSS1_CORE1_INTR_MCAN0_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_2<br>8|28|R5FSS1_CORE1_INTR_MCAN0_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE1_INTR_IN_2<br>9|29|R5FSS1_CORE1_INTR_MCAN1_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_3<br>0|30|R5FSS1_CORE1_INTR_MCAN1_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_3<br>1|31|R5FSS1_CORE1_INTR_MCAN1_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE1_INTR_IN_3<br>2|32|R5FSS1_CORE1_INTR_MCAN2_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_3<br>3|33|R5FSS1_CORE1_INTR_MCAN2_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_3<br>4|34|R5FSS1_CORE1_INTR_MCAN2_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE1_INTR_IN_3<br>5|35|R5FSS1_CORE1_INTR_MCAN3_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_3<br>6|36|R5FSS1_CORE1_INTR_MCAN3_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_3<br>7|37|R5FSS1_CORE1_INTR_MCAN3_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE1_INTR_IN_3<br>8|38|R5FSS1_CORE1_INTR_UART0_IRQ|Level|
|R5FSS1_CORE1_INTR_IN_3<br>9|39|R5FSS1_CORE1_INTR_UART1_IRQ|Level|
|R5FSS1_CORE1_INTR_IN_4<br>0|40|R5FSS1_CORE1_INTR_UART2_IRQ|Level|
|R5FSS1_CORE1_INTR_IN_4<br>1|41|R5FSS1_CORE1_INTR_UART3_IRQ|Level|
|R5FSS1_CORE1_INTR_IN_4<br>2|42|R5FSS1_CORE1_INTR_UART4_IRQ|Level|
|R5FSS1_CORE1_INTR_IN_4<br>3|43|R5FSS1_CORE1_INTR_UART5_IRQ|Level|
|R5FSS1_CORE1_INTR_IN_4<br>4|44|R5FSS1_CORE1_INTR_I2C0_IRQ|Pulse|
|R5FSS1_CORE1_INTR_IN_4<br>5|45|R5FSS1_CORE1_INTR_I2C1_IRQ|Pulse|
|R5FSS1_CORE1_INTR_IN_4<br>6|46|R5FSS1_CORE1_INTR_I2C2_IRQ|Pulse|
|R5FSS1_CORE1_INTR_IN_4<br>7|47|R5FSS1_CORE1_INTR_I2C3_IRQ|Pulse|
|R5FSS1_CORE1_INTR_IN_4<br>8|48|R5FSS1_CORE1_INTR_DTHE_SHA_S_INT|Level|
|R5FSS1_CORE1_INTR_IN_4<br>9|49|R5FSS1_CORE1_INTR_DTHE_SHA_P_INT|Level|
|R5FSS1_CORE1_INTR_IN_5<br>0|50|R5FSS1_CORE1_INTR_DTHE_TRNG_INT|Level|
|R5FSS1_CORE1_INTR_IN_5<br>1|51|R5FSS1_CORE1_INTR_DTHE_PKAE_INT|Level|
|R5FSS1_CORE1_INTR_IN_5<br>2|52|R5FSS1_CORE1_INTR_DTHE_AES_S_INT|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1017 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-20. R5FSS1_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE1_INTR_IN_5<br>3|53|R5FSS1_CORE1_INTR_DTHE_AES_P_INT|Level|
|R5FSS1_CORE1_INTR_IN_5<br>4|54|R5FSS1_CORE1_INTR_OSPI0_INT|Level|
|R5FSS1_CORE1_INTR_IN_5<br>5|55|R5FSS1_CORE1_INTR_TPCC_A_INTG|Pulse|
|R5FSS1_CORE1_INTR_IN_5<br>6|56|R5FSS1_CORE1_INTR_TPCC_A_INT_0|Pulse|
|R5FSS1_CORE1_INTR_IN_5<br>7|57|R5FSS1_CORE1_INTR_TPCC_A_INT_1|Pulse|
|R5FSS1_CORE1_INTR_IN_5<br>8|58|R5FSS1_CORE1_INTR_TPCC_A_INT_2|Pulse|
|R5FSS1_CORE1_INTR_IN_5<br>9|59|R5FSS1_CORE1_INTR_TPCC_A_INT_3|Pulse|
|R5FSS1_CORE1_INTR_IN_6<br>0|60|R5FSS1_CORE1_INTR_TPCC_A_INT_4|Pulse|
|R5FSS1_CORE1_INTR_IN_6<br>1|61|R5FSS1_CORE1_INTR_TPCC_A_INT_5|Pulse|
|R5FSS1_CORE1_INTR_IN_6<br>2|62|R5FSS1_CORE1_INTR_TPCC_A_INT_6|Pulse|
|R5FSS1_CORE1_INTR_IN_6<br>3|63|R5FSS1_CORE1_INTR_TPCC_A_INT_7|Pulse|
|R5FSS1_CORE1_INTR_IN_6<br>4|64|R5FSS1_CORE1_INTR_TPCC_A_ERRINT|Pulse|
|R5FSS1_CORE1_INTR_IN_6<br>5|65|R5FSS1_CORE1_INTR_TPCC_A_MPINT|Pulse|
|R5FSS1_CORE1_INTR_IN_6<br>6|66|R5FSS1_CORE1_INTR_TPTC0_ERINT_0|Pulse|
|R5FSS1_CORE1_INTR_IN_6<br>7|67|R5FSS1_CORE1_INTR_TPTC0_ERINT_1|Pulse|
|R5FSS1_CORE1_INTR_IN_6<br>8|68|R5FSS1_CORE1_INTR_MCRC0_INT|Level|
|R5FSS1_CORE1_INTR_IN_6<br>9|69|R5FSS1_CORE1_INTR_MPU_ADDR_ERRAGG|Level|
|R5FSS1_CORE1_INTR_IN_7<br>0|70|R5FSS1_CORE1_INTR_MPU_PROT_ERRAGG|Level|
|R5FSS1_CORE1_INTR_IN_7<br>1|71|R5FSS1_CORE1_INTR_PBIST_DONE|Level|
|R5FSS1_CORE1_INTR_IN_7<br>2|72|R5FSS1_CORE1_INTR_TPCC_A_INTAGGR|Level|
|R5FSS1_CORE1_INTR_IN_7<br>3|73|R5FSS1_CORE1_INTR_TPCC_A_ERRAGGR|Level|
|R5FSS1_CORE1_INTR_IN_7<br>4|74|R5FSS1_CORE1_INTR_DCC0_DONE|Level|
|R5FSS1_CORE1_INTR_IN_7<br>5|75|R5FSS1_CORE1_INTR_DCC1_DONE|Level|
|R5FSS1_CORE1_INTR_IN_7<br>6|76|R5FSS1_CORE1_INTR_DCC2_DONE|Level|
|R5FSS1_CORE1_INTR_IN_7<br>7|77|R5FSS1_CORE1_INTR_DCC3_DONE|Level|
|R5FSS1_CORE1_INTR_IN_7<br>8|78|R5FSS1_CORE1_INTR_MCSPI0_INTR|Level|



1018 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-20. R5FSS1_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE1_INTR_IN_7<br>9|79|R5FSS1_CORE1_INTR_MCSPI1_INTR|Level|
|R5FSS1_CORE1_INTR_IN_8<br>0|80|R5FSS1_CORE1_INTR_MCSPI2_INTR|Level|
|R5FSS1_CORE1_INTR_IN_8<br>1|81|R5FSS1_CORE1_INTR_MCSPI3_INTR|Level|
|R5FSS1_CORE1_INTR_IN_8<br>2|82|R5FSS1_CORE1_INTR_MCSPI4_INTR|Level|
|R5FSS1_CORE1_INTR_IN_8<br>3|83|R5FSS1_CORE1_INTR_MMC0_INTR|Level|
|R5FSS1_CORE1_INTR_IN_8<br>4|84|R5FSS1_CORE1_INTR_RTI0_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_8<br>5|85|R5FSS1_CORE1_INTR_RTI0_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_8<br>6|86|R5FSS1_CORE1_INTR_RTI0_INTR_2|Pulse|
|R5FSS1_CORE1_INTR_IN_8<br>7|87|R5FSS1_CORE1_INTR_RTI0_INTR_3|Pulse|
|R5FSS1_CORE1_INTR_IN_8<br>8|88|R5FSS1_CORE1_INTR_RESERVED|NA|
|R5FSS1_CORE1_INTR_IN_8<br>9|89|R5FSS1_CORE1_INTR_RTI0_OVERFLOW_INT0|Pulse|
|R5FSS1_CORE1_INTR_IN_9<br>0|90|R5FSS1_CORE1_INTR_RTI0_OVERFLOW_INT1|Pulse|
|R5FSS1_CORE1_INTR_IN_9<br>1|91|R5FSS1_CORE1_INTR_RTI1_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_9<br>2|92|R5FSS1_CORE1_INTR_RTI1_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_9<br>3|93|R5FSS1_CORE1_INTR_RTI1_INTR_2|Pulse|
|R5FSS1_CORE1_INTR_IN_9<br>4|94|R5FSS1_CORE1_INTR_RTI1_INTR_3|Pulse|
|R5FSS1_CORE1_INTR_IN_9<br>5|95|R5FSS1_CORE1_INTR_RESERVED|NA|
|R5FSS1_CORE1_INTR_IN_9<br>6|96|R5FSS1_CORE1_INTR_RTI1_OVERFLOW_INT0|Pulse|
|R5FSS1_CORE1_INTR_IN_9<br>7|97|R5FSS1_CORE1_INTR_RTI1_OVERFLOW_INT1|Pulse|
|R5FSS1_CORE1_INTR_IN_9<br>8|98|R5FSS1_CORE1_INTR_RTI2_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_9<br>9|99|R5FSS1_CORE1_INTR_RTI2_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>00|100|R5FSS1_CORE1_INTR_RTI2_INTR_2|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>01|101|R5FSS1_CORE1_INTR_RTI2_INTR_3|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>02|102|R5FSS1_CORE1_INTR_RESERVED|NA|
|R5FSS1_CORE1_INTR_IN_1<br>03|103|R5FSS1_CORE1_INTR_RTI2_OVERFLOW_INT0|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>04|104|R5FSS1_CORE1_INTR_RTI2_OVERFLOW_INT1|Pulse|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1019 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-20. R5FSS1_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE1_INTR_IN_1<br>05|105|R5FSS1_CORE1_INTR_RTI3_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>06|106|R5FSS1_CORE1_INTR_RTI3_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>07|107|R5FSS1_CORE1_INTR_RTI3_INTR_2|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>08|108|R5FSS1_CORE1_INTR_RTI3_INTR_3|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>09|109|R5FSS1_CORE1_INTR_RESERVED|NA|
|R5FSS1_CORE1_INTR_IN_1<br>10|110|R5FSS1_CORE1_INTR_RTI3_OVERFLOW_INT0|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>11|111|R5FSS1_CORE1_INTR_RTI3_OVERFLOW_INT1|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>12|112|R5FSS1_CORE1_INTR_RESERVED|NA|
|R5FSS1_CORE1_INTR_IN_1<br>13|113|R5FSS1_CORE1_INTR_ESM0_ESM_INT_CFG|Level|
|R5FSS1_CORE1_INTR_IN_1<br>14|114|R5FSS1_CORE1_INTR_ESM0_ESM_INT_HI|Level|
|R5FSS1_CORE1_INTR_IN_1<br>15|115|R5FSS1_CORE1_INTR_ESM0_ESM_INT_LOW|Level|
|R5FSS1_CORE1_INTR_IN_1<br>16|116|R5FSS1_CORE1_INTR_R5SS0_CPU0_PMU_INT|R5SS<br>Internal|
|R5FSS1_CORE1_INTR_IN_1<br>17|117|R5FSS1_CORE1_INTR_R5SS0_CPU1_PMU_INT|R5SS<br>Internal|
|R5FSS1_CORE1_INTR_IN_1<br>18|118|R5FSS1_CORE1_INTR_R5SS1_COMMRX_1|R5SS<br>Internal|
|R5FSS1_CORE1_INTR_IN_1<br>19|119|R5FSS1_CORE1_INTR_R5SS1_COMMTX_1|R5SS<br>Internal|
|R5FSS1_CORE1_INTR_IN_1<br>20|120|R5FSS1_CORE1_INTR_R5SS1_CPU0_CTI_INT|R5SS<br>Internal|
|R5FSS1_CORE1_INTR_IN_1<br>21|121|R5FSS1_CORE1_INTR_R5SS1_CPU1_CTI_INT|R5SS<br>Internal|
|R5FSS1_CORE1_INTR_IN_1<br>22|122|R5FSS1_CORE1_INTR_R5SS1_CPU1_VALFIQ|R5SS<br>Internal|
|R5FSS1_CORE1_INTR_IN_1<br>23|123|R5FSS1_CORE1_INTR_R5SS1_CPU1_VALIRQ|R5SS<br>Internal|
|R5FSS1_CORE1_INTR_IN_1<br>24|124|R5FSS1_CORE1_INTR_MMR_ACC_ERRAGG|Level|
|R5FSS1_CORE1_INTR_IN_1<br>25|125|R5FSS1_CORE1_INTR_R5SS1_LIVELOCK_0|R5SS<br>Internal|
|R5FSS1_CORE1_INTR_IN_1<br>26|126|R5FSS1_CORE1_INTR_R5SS0_LIVELOCK_0|R5SS<br>Internal|
|R5FSS1_CORE1_INTR_IN_1<br>27|127|R5FSS1_CORE1_INTR_R5SS0_LIVELOCK_1|R5SS<br>Internal|
|R5FSS1_CORE1_INTR_IN_1<br>28|128|R5FSS1_CORE1_INTR_RTI_WDT3_NMI|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>29|129|R5FSS1_CORE1_INTR_SW_IRQ|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>30|130|R5FSS1_CORE1_INTR_R5SS1_CORE1_FPU_EXP|R5SS<br>Internal|



1020 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-20. R5FSS1_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE1_INTR_IN_1<br>31|131|R5FSS1_CORE1_INTR_DEBUGSS_TXDATA_AVAIL|Level|
|R5FSS1_CORE1_INTR_IN_1<br>32|132|R5FSS1_CORE1_INTR_DEBUGSS_R5SS0_STC_DONE|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>33|133|R5FSS1_CORE1_INTR_TSENSE_H|Level|
|R5FSS1_CORE1_INTR_IN_1<br>34|134|R5FSS1_CORE1_INTR_TSENSE_L|Level|
|R5FSS1_CORE1_INTR_IN_1<br>35|135|R5FSS1_CORE1_INTR_AHB_WRITE_ERR|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>36|136|R5FSS1_CORE1_INTR_MBOX_READ_REQ|Level|
|R5FSS1_CORE1_INTR_IN_1<br>37|137|R5FSS1_CORE1_INTR_MBOX_READ_ACK|Level|
|R5FSS1_CORE1_INTR_IN_1<br>38|138|R5FSS1_CORE1_INTR_SOC_TIMESYNCXBAR1_OUT_30|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>39|139|R5FSS1_CORE1_INTR_SOC_TIMESYNCXBAR1_OUT_31|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>40|140|R5FSS1_CORE1_INTR_SOC_TIMESYNCXBAR1_OUT_32|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>41|141|R5FSS1_CORE1_INTR_SOC_TIMESYNCXBAR1_OUT_33|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>42|142|R5FSS1_CORE1_INTR_GPIO_INTRXBAR_OUT_26|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>43|143|R5FSS1_CORE1_INTR_GPIO_INTRXBAR_OUT_27|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>44|144|R5FSS1_CORE1_INTR_GPIO_INTRXBAR_OUT_28|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>45|145|R5FSS1_CORE1_INTR_GPIO_INTRXBAR_OUT_29|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>46|146|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_0|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>47|147|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_1|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>48|148|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_2|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>49|149|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_3|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>50|150|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_4|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>51|151|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_5|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>52|152|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_6|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>53|153|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_7|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>54|154|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_8|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>55|155|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_9|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>56|156|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_10|Level/<br>Pulse*|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1021 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-20. R5FSS1_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE1_INTR_IN_1<br>57|157|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_11|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>58|158|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_12|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>59|159|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_13|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>60|160|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_14|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>61|161|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_15|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>62|162|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_16|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>63|163|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_17|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>64|164|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_18|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>65|165|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_19|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>66|166|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_20|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>67|167|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_21|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>68|168|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_22|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>69|169|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_23|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>70|170|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_24|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>71|171|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_25|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>72|172|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_26|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>73|173|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_27|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>74|174|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_28|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>75|175|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_29|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>76|176|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_30|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>77|177|R5FSS1_CORE1_CONTROLSS_INTRXBAR0_OUT_31|Level/<br>Pulse*|
|R5FSS1_CORE1_INTR_IN_1<br>78|178|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_0|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>79|179|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_1|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>80|180|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_2|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>81|181|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_3|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>82|182|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_4|Pulse|



1022 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-20. R5FSS1_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE1_INTR_IN_1<br>83|183|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_5|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>84|184|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_6|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>85|185|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_7|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>86|186|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_8|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>87|187|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_9|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>88|188|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_10|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>89|189|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_11|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>90|190|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_12|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>91|191|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_13|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>92|192|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_14|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>93|193|R5FSS1_CORE1_INTR_PRU_ICSSM0_PR1_IEP0_CMP_INTR_REQ_15|Pulse|
|R5FSS1_CORE1_INTR_IN_1<br>94|194|R5FSS1_CORE1_CPSW0_CPTS_COMP|Level|
|R5FSS1_CORE1_INTR_IN_1<br>95|195|R5FSS1_CORE1_INTR_RESERVED|NA|
|R5FSS1_CORE1_INTR_IN_1<br>96|196|R5FSS1_CORE1_INTR_RESERVED|NA|
|R5FSS1_CORE1_INTR_IN_1<br>97|197|R5FSS1_CORE1_INTR_MCAN4_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_1<br>98|198|R5FSS1_CORE1_INTR_MCAN4_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_1<br>99|199|R5FSS1_CORE1_INTR_MCAN4_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE1_INTR_IN_2<br>00|200|R5FSS1_CORE1_INTR_MCAN5_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_2<br>01|201|R5FSS1_CORE1_INTR_MCAN5_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_2<br>02|202|R5FSS1_CORE1_INTR_MCAN5_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE1_INTR_IN_2<br>03|203|R5FSS1_CORE1_INTR_MCAN6_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_2<br>04|204|R5FSS1_CORE1_INTR_MCAN6_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_2<br>05|205|R5FSS1_CORE1_INTR_MCAN6_MCAN_LVL_INT_1|Level|
|R5FSS1_CORE1_INTR_IN_2<br>06|206|R5FSS1_CORE1_INTR_MCAN7_EXT_TS_ROLLOVER_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_2<br>07|207|R5FSS1_CORE1_INTR_MCAN7_MCAN_LVL_INT_0|Level|
|R5FSS1_CORE1_INTR_IN_2<br>08|208|R5FSS1_CORE1_INTR_MCAN7_MCAN_LVL_INT_1|Level|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1023 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-20. R5FSS1_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE1_INTR_IN_2<br>09|209|R5FSS1_CORE1_INTR_R5SS0_CPU0_TMU_LVF|Level|
|R5FSS1_CORE1_INTR_IN_2<br>10|210|R5FSS1_CORE1_INTR_R5SS0_CPU0_TMU_LUF|Level|
|R5FSS1_CORE1_INTR_IN_2<br>11|211|R5FSS1_CORE1_INTR_HW_RESOLVER|Level|
|R5FSS1_CORE1_INTR_IN_2<br>12|212|R5FSS1_CORE1_INTR_FSS_VBUSM_TIMEOUT|Level|
|R5FSS1_CORE1_INTR_IN_2<br>13|213|R5FSS1_CORE1_INTR_OTFA_ERROR|Level|
|R5FSS1_CORE1_INTR_IN_2<br>14|214|R5FSS1_CORE1_INTR_FOTA_STAT|Level|
|R5FSS1_CORE1_INTR_IN_2<br>15|215|R5FSS1_CORE1_INTR_FOTA_STAT_ERR|Level|
|R5FSS1_CORE1_INTR_IN_2<br>16|216|R5FSS1_CORE1_INTR_MCSPI5_INTR|Level|
|R5FSS1_CORE1_INTR_IN_2<br>17|217|R5FSS1_CORE1_INTR_MCSPI6_INTR|Level|
|R5FSS1_CORE1_INTR_IN_2<br>18|218|R5FSS1_CORE1_INTR_MCSPI7_INTR|Level|
|R5FSS1_CORE1_INTR_IN_2<br>19|219|R5FSS1_CORE1_INTR_RTI4_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>20|220|R5FSS1_CORE1_INTR_RTI4_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>21|221|R5FSS1_CORE1_INTR_RTI4_INTR_2|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>22|222|R5FSS1_CORE1_INTR_RTI4_INTR_3|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>23|223|R5FSS1_CORE1_INTR_RTI4_OVERFLOW_INT0|Level|
|R5FSS1_CORE1_INTR_IN_2<br>24|224|R5FSS1_CORE1_INTR_RTI4_OVERFLOW_INT1|Level|
|R5FSS1_CORE1_INTR_IN_2<br>25|225|R5FSS1_CORE1_INTR_RTI5_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>26|226|R5FSS1_CORE1_INTR_RTI5_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>27|227|R5FSS1_CORE1_INTR_RTI5_INTR_2|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>28|228|R5FSS1_CORE1_INTR_RTI5_INTR_3|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>29|229|R5FSS1_CORE1_INTR_RTI5_OVERFLOW_INT0|Level|
|R5FSS1_CORE1_INTR_IN_2<br>30|230|R5FSS1_CORE1_INTR_RTI5_OVERFLOW_INT1|Level|
|R5FSS1_CORE1_INTR_IN_2<br>31|231|R5FSS1_CORE1_INTR_RTI6_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>32|232|R5FSS1_CORE1_INTR_RTI6_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>33|233|R5FSS1_CORE1_INTR_RTI6_INTR_2|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>34|234|R5FSS1_CORE1_INTR_RTI6_INTR_3|Pulse|



1024 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-20. R5FSS1_CORE1 Interrupt Map (continued)** 

|**Interrupt Input Line**|**Interrupt**<br>**ID**|**Source Interrupt**|**Interrupt**<br>**type**|
|---|---|---|---|
|R5FSS1_CORE1_INTR_IN_2<br>35|235|R5FSS1_CORE1_INTR_RTI6_OVERFLOW_INT0|Level|
|R5FSS1_CORE1_INTR_IN_2<br>36|236|R5FSS1_CORE1_INTR_RTI6_OVERFLOW_INT1|Level|
|R5FSS1_CORE1_INTR_IN_2<br>37|237|R5FSS1_CORE1_INTR_RTI7_INTR_0|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>38|238|R5FSS1_CORE1_INTR_RTI7_INTR_1|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>39|239|R5FSS1_CORE1_INTR_RTI7_INTR_2|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>40|240|R5FSS1_CORE1_INTR_RTI7_INTR_3|Pulse|
|R5FSS1_CORE1_INTR_IN_2<br>41|241|R5FSS1_CORE1_INTR_RTI7_OVERFLOW_INT0|Level|
|R5FSS1_CORE1_INTR_IN_2<br>42|242|R5FSS1_CORE1_INTR_RTI7_OVERFLOW_INT1|Level|
|R5FSS1_CORE1_INTR_IN_2<br>43|243|R5FSS1_CORE1_INTR_R5SS0_CPU0_RL2_ERR|Level|
|R5FSS1_CORE1_INTR_IN_2<br>44|244|R5FSS1_CORE1_INTR_R5SS0_CPU1_RL2_ERR|Level|
|R5FSS1_CORE1_INTR_IN_2<br>45|245|R5FSS1_CORE1_INTR_R5SS1_CPU0_RL2_ERR|Level|
|R5FSS1_CORE1_INTR_IN_2<br>46|246|R5FSS1_CORE1_INTR_R5SS1_CPU1_RL2_ERR|Level|



## _**10.4.5 PRU-ICSS Interrupt Map**_ 

Table 10-21 shows the mapping of external events to the PRU-ICSS. 

**Table 10-21. PRU-ICSS External Events Mapping** 

|**Interrupt Input Line**|**Interrupt Signal name**|**Interrupt Source**|**Interrupt Signal**|
|---|---|---|---|
|PRU_ICSSM0_INTR_IN_0|PR1_SLV_INTR_0|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_0|
|PRU_ICSSM0_INTR_IN_1|PR1_SLV_INTR_1|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_1|
|PRU_ICSSM0_INTR_IN_2|PR1_SLV_INTR_2|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_2|
|PRU_ICSSM0_INTR_IN_3|PR1_SLV_INTR_3|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_3|
|PRU_ICSSM0_INTR_IN_4|PR1_SLV_INTR_4|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_4|
|PRU_ICSSM0_INTR_IN_5|PR1_SLV_INTR_5|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_5|
|PRU_ICSSM0_INTR_IN_6|PR1_SLV_INTR_6|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_6|
|PRU_ICSSM0_INTR_IN_7|PR1_SLV_INTR_7|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_7|
|PRU_ICSSM0_INTR_IN_8|PR1_SLV_INTR_8|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_8|
|PRU_ICSSM0_INTR_IN_9|PR1_SLV_INTR_9|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_9|
|PRU_ICSSM0_INTR_IN_10|PR1_SLV_INTR_10|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_10|
|PRU_ICSSM0_INTR_IN_11|PR1_SLV_INTR_11|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_11|
|PRU_ICSSM0_INTR_IN_12|PR1_SLV_INTR_12|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_12|
|PRU_ICSSM0_INTR_IN_13|PR1_SLV_INTR_13|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_13|
|PRU_ICSSM0_INTR_IN_14|PR1_SLV_INTR_14|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_14|
|PRU_ICSSM0_INTR_IN_15|PR1_SLV_INTR_15|PRU-ICSS XBAR|PRU-ICSS_XBAROUT_15|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1025 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-21. PRU-ICSS External Events Mapping (continued)** 

|**Interrupt Input Line**|**Interrupt Signal name**|**Interrupt Source**|**Interrupt Signal**|
|---|---|---|---|
|PRU_ICSSM0_INTR_IN_16|PR1_SLV_INTR_16|CONTROLSS_INTXBAR|OUTPUTXBAR.Out0|
|PRU_ICSSM0_INTR_IN_17|PR1_SLV_INTR_17|CONTROLSS_INTXBAR|OUTPUTXBAR.Out1|
|PRU_ICSSM0_INTR_IN_18|PR1_SLV_INTR_18|CONTROLSS_INTXBAR|OUTPUTXBAR.Out2|
|PRU_ICSSM0_INTR_IN_19|PR1_SLV_INTR_19|CONTROLSS_INTXBAR|OUTPUTXBAR.Out3|
|PRU_ICSSM0_INTR_IN_20|PR1_SLV_INTR_20|CONTROLSS_INTXBAR|OUTPUTXBAR.Out4|
|PRU_ICSSM0_INTR_IN_21|PR1_SLV_INTR_21|CONTROLSS_INTXBAR|OUTPUTXBAR.Out5|
|PRU_ICSSM0_INTR_IN_22|PR1_SLV_INTR_22|CONTROLSS_INTXBAR|OUTPUTXBAR.Out6|
|PRU_ICSSM0_INTR_IN_23|PR1_SLV_INTR_23|CONTROLSS_INTXBAR|OUTPUTXBAR.Out7|
|PRU_ICSSM0_INTR_IN_24|PR1_SLV_INTR_24|CONTROLSS_INTXBAR|OUTPUTXBAR.Out8|
|PRU_ICSSM0_INTR_IN_25|PR1_SLV_INTR_25|CONTROLSS_INTXBAR|OUTPUTXBAR.Out9|
|PRU_ICSSM0_INTR_IN_26|PR1_SLV_INTR_26|CONTROLSS_INTXBAR|OUTPUTXBAR.Out10|
|PRU_ICSSM0_INTR_IN_27|PR1_SLV_INTR_27|CONTROLSS_INTXBAR|OUTPUTXBAR.Out11|
|PRU_ICSSM0_INTR_IN_28|PR1_SLV_INTR_28|CONTROLSS_INTXBAR|OUTPUTXBAR.Out12|
|PRU_ICSSM0_INTR_IN_29|PR1_SLV_INTR_29|CONTROLSS_INTXBAR|OUTPUTXBAR.Out13|
|PRU_ICSSM0_INTR_IN_30|PR1_SLV_INTR_30|CONTROLSS_INTXBAR|OUTPUTXBAR.Out14|
|PRU_ICSSM0_INTR_IN_31|PR1_SLV_INTR_31|CONTROLSS_INTXBAR|OUTPUTXBAR.Out15|
|PRU_ICSSM0_INTR_IN_32|ICSSM0_EDC_LATCH0_IN|SOC_TIMESYNC_XBAR|SOC_TIMESYNC_XBAR1_SYN<br>CEVE NT_OUT10|
|PRU_ICSSM0_INTR_IN_33|ICSSM0_EDC_LATCH1_IN|SOC_TIMESYNC_XBAR|SOC_TIMESYNC_XBAR1_SYN<br>CEVE NT_OUT11|
|PRU_ICSSM0_INTR_IN_34|ICSSM0_IEP_CAP_INTR0|SOC_TIMESYNC_XBAR|SOC_TIMESYNC_XBAR1_SYN<br>CEVE NT_OUT12|
|PRU_ICSSM0_INTR_IN_35|ICSSM0_IEP_CAP_INTR1|SOC_TIMESYNC_XBAR|SOC_TIMESYNC_XBAR1_SYN<br>CEVE NT_OUT13|
|PRU_ICSSM0_INTR_IN_36|ICSSM0_IEP_CAP_INTR2|SOC_TIMESYNC_XBAR|SOC_TIMESYNC_XBAR1_SYN<br>CEVE NT_OUT14|
|PRU_ICSSM0_INTR_IN_37|ICSSM0_IEP_CAP_INTR3|SOC_TIMESYNC_XBAR|SOC_TIMESYNC_XBAR1_SYN<br>CEVE NT_OUT15|
|PRU_ICSSM0_INTR_IN_38|ICSSM0_IEP_CAP_INTR4|SOC_TIMESYNC_XBAR|SOC_TIMESYNC_XBAR1_SYN<br>CEVE NT_OUT16|
|PRU_ICSSM0_INTR_IN_39|ICSSM0_IEP_CAP_INTR5|SOC_TIMESYNC_XBAR|SOC_TIMESYNC_XBAR1_SYN<br>CEVE NT_OUT17|



## **Note** 

See tables **PRU-ICSS IP Interrupts** and **AM263Px-Specific PRU-ICSS Interrupt Mapping** in the Programmable Real-Time Unit Subsystem (PRU-ICSS) chapter of the TRM for the mapping of external/internal events to the PRU-ICSS INTC interrupt lines 0 through 63. 

1026 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

## _**10.4.6 ESM0 Interrupt Map**_ 

Table 10-22 shows the mapping of events to the ESM0. 

**Table 10-22. ESM0 Interrupt Map (Level)** 

|**Interrupt Input Line**|**Interr**<br>**upt ID**|**Interrupt Source**|**Interrupt Signal**|
|---|---|---|---|
|ESM_LVL_EVENT_0|0|EFUSE|efc_error|
|ESM_LVL_EVENT_1|1|EFUSE|efs_autoload_error|
|ESM_LVL_EVENT_2|2|MCAN0|MCAN0_ecc_corr_lvl_int|
|ESM_LVL_EVENT_3|3|MCAN0|MCAN0_ecc_uncorr_lvl_int|
|ESM_LVL_EVENT_4|4|MCAN1|MCAN1_ecc_corr_lvl_int|
|ESM_LVL_EVENT_5|5|MCAN1|MCAN1_ecc_uncorr_lvl_int|
|ESM_LVL_EVENT_6|6|MCAN2|MCAN2_ecc_corr_lvl_int|
|ESM_LVL_EVENT_7|7|MCAN2|MCAN2_ecc_uncorr_lvl_int|
|ESM_LVL_EVENT_8|8|MCAN3|MCAN3_ecc_corr_lvl_int|
|ESM_LVL_EVENT_9|9|MCAN3|MCAN3_ecc_uncorr_lvl_int|
|ESM_LVL_EVENT_10|10|R5FSS0_CORE0|R5FSS0_livelock_0|
|ESM_LVL_EVENT_11|11|R5FSS0_CORE1|R5FSS0_livelock_1|
|ESM_LVL_EVENT_12|12|R5FSS1_CORE0|R5FSS1_livelock_0|
|ESM_LVL_EVENT_13|13|R5FSS1_CORE1|R5FSS1_livelock_1|
|ESM_LVL_EVENT_14|14|R5FSS0_CORE0|R5FSS0_CORE0_TCMADDR_err|
|ESM_LVL_EVENT_15|15|R5FSS0_CORE1|R5FSS0_CORE1_TCMADDR_err|
|ESM_LVL_EVENT_16|16|R5FSS1_CORE0|R5FSS1_CORE0_TCMADDR_err|
|ESM_LVL_EVENT_17|17|R5FSS1_CORE1|R5FSS1_CORE1_TCMADDR_err|
|ESM_LVL_EVENT_18|18|HW_RESOLVER|HW_RESOLVER_SAFETY_INTR|
|ESM_LVL_EVENT_19|19|ECC_AGGREGATOR|soc_eccagg_corr_level|
|ESM_LVL_EVENT_20|20|ECC_AGGREGATOR|soc_eccagg_uncorr_level|
|ESM_LVL_EVENT_21|21|DCC0|DCC0_err|
|ESM_LVL_EVENT_22|22|DCC1|DCC1_err|
|ESM_LVL_EVENT_23|23|DCC2|DCC2_err|
|ESM_LVL_EVENT_24|24|DCC3|DCC3_err|
|ESM_LVL_EVENT_25|25|CORE_PLL|pll_core_lockloss|
|ESM_LVL_EVENT_26|26|PERI_PLL|pll_per_lockloss|
|ESM_LVL_EVENT_27|27|RCOSC|rcref_clk_loss_detect|
|ESM_LVL_EVENT_28|28|HSM|HSM_ESM_high_intr|
|ESM_LVL_EVENT_29|29|HSM|HSM_ESM_low_intr|
|ESM_LVL_EVENT_30|30|XTAL|crystal_clockloss|
|ESM_LVL_EVENT_31|31|Aggregated VBUSP Error|Aggregated_VBUSP_error_H|
|ESM_LVL_EVENT_32|32|OPTI_FLASH|FOTA_STAT_ERR_INTR|
|ESM_LVL_EVENT_33|33|Aggregated VBUSM Error|Aggregated_VBUSM_error_H|
|ESM_LVL_EVENT_34|34|Aggregated VBUSM Error|Aggregated_VBUSM_error_L|
|ESM_LVL_EVENT_35|35|Reserved|Reserved|
|ESM_LVL_EVENT_36|36|Reserved|Reserved|
|ESM_LVL_EVENT_37|37|OPTI_FLASH|FSS_VBUSM_TIMEOUT|
|ESM_LVL_EVENT_38|38|OPTI_FLASH|OTFA_ERROR|
|ESM_LVL_EVENT_39|39|OPTI_FLASH|OSPI_ECC_CORR|
|ESM_LVL_EVENT_40|40|OPTI_FLASH|OSPI_ECC_UNCORR|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1027 

Copyright © 2025 Texas Instruments Incorporated 

_Interrupts_ 

www.ti.com 

**Table 10-22. ESM0 Interrupt Map (Level) (continued)** 

|**Interrupt Input Line**|**Interr**<br>**upt ID**|**Interrupt Source**|**Interrupt Signal**|
|---|---|---|---|
|ESM_LVL_EVENT_41|41|VMON_ERR_H|voltage_monitor_err_H|
|ESM_LVL_EVENT_42|42|VMON_ERR_L|voltage_monitor_err_L|
|ESM_LVL_EVENT_43|43|OPTI_FLASH|FSAS_ECC_INTR|
|ESM_LVL_EVENT_44|44|THERMAL_MONITOR|thermal_monitor_critical|
|ESM_LVL_EVENT_45|45|CPSW|CPSW_ECC_SEC_PEND_INTR|
|ESM_LVL_EVENT_46|46|CPSW|CPSW_ECC_DED_PEND_INTR|
|ESM_LVL_EVENT_47|47|R5FSS0_CORE0|R5FSS0_CORE0_ecc_corrected_level.0|
|ESM_LVL_EVENT_48|48|R5FSS0_CORE0|R5FSS0_CORE0_ecc_uncorrected_level.0|
|ESM_LVL_EVENT_49|49|R5FSS0_CORE1|R5FSS0_CORE1_ecc_corrected_level.0|
|ESM_LVL_EVENT_50|50|R5FSS0_CORE1|R5FSS0_CORE1_ecc_uncorrected_level.0|
|ESM_LVL_EVENT_51|51|R5FSS0_CORE0|R5FSS0_ecc_de_to_esm_0.0|
|ESM_LVL_EVENT_52|52|R5FSS0_CORE1|R5FSS0_ecc_de_to_esm_1.0|
|ESM_LVL_EVENT_53|53|R5FSS0_CORE0|R5FSS0_ecc_se_to_esm_0.0|
|ESM_LVL_EVENT_54|54|R5FSS0_CORE1|R5FSS0_ecc_se_to_esm_1.0|
|ESM_LVL_EVENT_55|55|R5FSS1_CORE0|R5FSS1_CORE0_ecc_corrected_level.0|
|ESM_LVL_EVENT_56|56|R5FSS1_CORE0|R5FSS1_CORE0_ecc_uncorrected_level.0|
|ESM_LVL_EVENT_57|57|R5FSS1_CORE1|R5FSS1_CORE1_ecc_corrected_level.0|
|ESM_LVL_EVENT_58|58|R5FSS1_CORE1|R5FSS1_CORE1_ecc_uncorrected_level.0|
|ESM_LVL_EVENT_59|59|R5FSS0_CORE0|R5FSS1_ecc_de_to_esm_0.0|
|ESM_LVL_EVENT_60|60|R5FSS0_CORE1|R5FSS1_ecc_de_to_esm_1.0|
|ESM_LVL_EVENT_61|61|R5FSS0_CORE0|R5FSS1_ecc_se_to_esm_0.0|
|ESM_LVL_EVENT_62|62|R5FSS0_CORE1|R5FSS1_ecc_se_to_esm_1.0|
|ESM_LVL_EVENT_63|63|EDMA0|tpcc_a_err_intagg|



**Table 10-23. ESM0 Interrupt Map (Pulse)** 

|**Interrupt Input Line**|**Interr**<br>**upt ID**|**Interrupt Source**|**Interrupt Signal**|
|---|---|---|---|
|ESM_PLS_EVENT_0|0|WWDT0|RTI0_WWD_NMI|
|ESM_PLS_EVENT_1|1|WWDT1|RTI1_WWD_NMI|
|ESM_PLS_EVENT_2|2|WWDT2|RTI2_WWD_NMI|
|ESM_PLS_EVENT_3|3|WWDT3|RTI3_WWD_NMI|
|ESM_PLS_EVENT_4|4|EDMA0|TPCC_errint|
|ESM_PLS_EVENT_5|5|R5FSS0/CCM0|R5FSS0_bus_monitor_err_pulse.0|
|ESM_PLS_EVENT_6|6|R5FSS0/CCM0|R5FSS0_compare_err_pulse.0|
|ESM_PLS_EVENT_7|7|R5FSS0/CCM0|R5FSS0_vim_compare_err_pulse.0|
|ESM_PLS_EVENT_8|8|R5FSS0/CCM0|R5FSS0_cpu_miscompare_pulse.0|
|ESM_PLS_EVENT_9|9|R5FSS1/CCM0|R5FSS1_bus_monitor_err_pulse.0|
|ESM_PLS_EVENT_10|10|R5FSS1/CCM0|R5FSS1_compare_err_pulse.0|
|ESM_PLS_EVENT_11|11|R5FSS1/CCM0|R5FSS1_vim_compare_err_pulse.0|
|ESM_PLS_EVENT_12|12|R5FSS1/CCM0|R5FSS1_cpu_miscompare_pulse.0|
|ESM_PLS_EVENT_13|13|PRU_ICSSM0|pr1_ecc_ded_err_req|
|ESM_PLS_EVENT_14|14|PRU_ICSSM0|pr1_ecc_sec_err_req|
|ESM_PLS_EVENT_15|15|SRAM Bank 0|sram0_ecc_uncorr_pulse|
|ESM_PLS_EVENT_16|16|SRAM Bank 1|sram1_ecc_uncorr_pulse|
|ESM_PLS_EVENT_17|17|SRAM Bank 2|sram2_ecc_uncorr_pulse|



1028 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Interrupts_ 

**Table 10-23. ESM0 Interrupt Map (Pulse) (continued)** 

|**Interrupt Input Line**|**Interr**<br>**upt ID**|**Interrupt Source**|**Interrupt Signal**|
|---|---|---|---|
|ESM_PLS_EVENT_18|18|SRAM Bank 3|sram3_ecc_uncorr_pulse|
|ESM_PLS_EVENT_19|19|CCM0|CCM_0_selftest_err|
|ESM_PLS_EVENT_20|20|R5FSS0_STC|R5FSS0_stc_err|
|ESM_PLS_EVENT_21|21|CCM1|CCM_1_selftest_err|
|ESM_PLS_EVENT_22|22|R5FSS1_STC|R5FSS1_stc_err|
|ESM_PLS_EVENT_23|23|R5SS0|R5SS0_TMU_COMP_ERR|
|ESM_PLS_EVENT_24|24|R5SS0|R5SS0_CPU0_TMU_PARITY_ERR|
|ESM_PLS_EVENT_25|25|R5SS0|R5SS0_CPU1_TMU_PARITY_ERR|
|ESM_PLS_EVENT_26|26|R5SS1|R5SS1_TMU_COMP_ERR|
|ESM_PLS_EVENT_27|27|R5SS1|R5SS1_CPU0_TMU_PARITY_ERR|
|ESM_PLS_EVENT_28|28|R5SS1|R5SS1_CPU1_TMU_PARITY_ERR|
|ESM_PLS_EVENT_29|29|R5SS0|R5SS0_RL2_COMP_ERR|
|ESM_PLS_EVENT_30|30|R5SS1|R5SS1_RL2_COMP_ERR|
|ESM_PLS_EVENT_31|31|ADC_SAFETY|ADC_SAFETY_CHECKEVENT0|
|ESM_PLS_EVENT_32|32|ADC_SAFETY|ADC_SAFETY_CHECKEVENT1|
|ESM_PLS_EVENT_33|33|ADC_SAFETY|ADC_SAFETY_CHECKEVENT2|
|ESM_PLS_EVENT_34|34|ADC_SAFETY|ADC_SAFETY_CHECKEVENT3|
|ESM_PLS_EVENT_35|35|OPTI_FLASH|OTFA_ECC_UNCORR|
|ESM_PLS_EVENT_36|36|OPTI_FLASH|OTFA_ECC_CORR|
|ESM_PLS_EVENT_37|37|SRAM Bank 4|sram4_ecc_uncorr_pulse|
|ESM_PLS_EVENT_38|38|SRAM Bank 5|sram5_ecc_uncorr_pulse|
|ESM_PLS_EVENT_39|39|MCAN4|mcanss4_ecc_corr_pls_int|
|ESM_PLS_EVENT_40|40|MCAN4|mcanss4_ecc_uncorr_pls_int|
|ESM_PLS_EVENT_41|41|MCAN5|mcanss5_ecc_corr_pls_int|
|ESM_PLS_EVENT_42|42|MCAN5|mcanss5_ecc_uncorr_pls_int|
|ESM_PLS_EVENT_43|43|MCAN6|mcanss6_ecc_corr_pls_int|
|ESM_PLS_EVENT_44|44|MCAN6|mcanss6_ecc_uncorr_pls_int|
|ESM_PLS_EVENT_45|45|MCAN7|mcanss7_ecc_corr_pls_int|
|ESM_PLS_EVENT_46|46|MACN7|mcanss7_ecc_uncorr_pls_int|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1029 

Copyright © 2025 Texas Instruments Incorporated 

