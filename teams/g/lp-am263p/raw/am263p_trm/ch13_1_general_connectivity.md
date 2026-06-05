<!-- AM263P TRM | 13.1 General Connectivity (GPIO/I2C/MCSPI/UART) | 원본 p.1111-1263 | pymupdf4llm text+tables, images omitted -->

www.ti.com 

_Peripherals_ 

## **13.1 General Connectivity Peripherals** 

This section describes the general connectivity peripherals in the device. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1111 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.1 General-Purpose Interface (GPIO)**_ 

This chapter describes the General-Purpose Input/Output (GPIO) for the device. 

## **13.1.1.1 GPIO Overview** 

The General-Purpose Input/Output (GPIO) peripheral provides dedicated general-purpose pins that can be configured as either inputs or outputs. When configured as an output, the user can write to an internal register to control the state driven on the output pin. When configured as an input, user can obtain the state of the input by reading the state of an internal register. 

In addition, the GPIO peripheral can produce host CPU interrupts and DMA synchronization events in different interrupt/event generation modes. 

The device has four instances of the GPIO module, one per R5FSS processor core. The GPIO pins are grouped into banks (16 pins per bank and 9 banks per module), which means that each GPIO module provides up to 144 dedicated general-purpose pins with input and output capabilities. 

## **Note** 

Out of the 144 available GPIOs, only 139 GPIOs were connected to PADs and 5 GPIO Pins are grounded. 

Table 13-1 shows GPIO modules allocation within device domains. 

**Table 13-1. GPIO Modules Allocation within Device Domains** 

|**Module Instance**|**Device**|
|---|---|
|GPIO0|✓(R5FSS0-CORE0)|
|GPIO1|✓(R5FSS0-CORE1)|
|GPIO2|✓(R5FSS1-CORE0)|
|GPIO3|✓(R5FSS1-CORE1)|



1112 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.1.1.2 GPIO Environment** 

The GPIO[0-3] modules are hereinafter referred to as GPIO module. 

This section describes the GPIO external connections (environment). 

The general-purpose interface combines four GPIO modules for a flexible, user-programmable, general-purpose input/output (I/O) controller. The general-purpose interface implements functions that are not implemented with the dedicated controllers in the device and require simple input and/or output software-controlled signals. The GPIO allows a variety of custom connections and expands the I/O capabilities of the system to the real world. 

The general-purpose interface can physically connect the device to a keyboard matrix and peripheral integrated circuits (ICs). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1113 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.1.1.3 GPIO Integration** 

There are 4x GPIO modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [488 x 247] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>GPIO<br>GPIO#_OUTEN<br>SYS_CLK GPIO#_CLK ENB<br>GPIO#_OUT<br>GPIO#_IN<br>RCM GPIO#_BANK_INTR[8:0]<br>GPIO#_RST_CTRL Bit<br>GPIO#_WARMRESET R5FSS0-CORE0<br>Warm Reset Sources<br>GPIO#_INTR[143:0]<br>R5FSS0-CORE1<br>R5FSS1-CORE0<br>PERI VBUSP Interconnect<br>R5FSS1-CORE1<br>GPIO_XBAR<br>**----- End of picture text -----**<br>


**Figure 13-1. GPIO Integration Diagram** 

1114 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

There is a designated GPIO module per R5FSS core. Each R5FSS core has access to all GPI signals. The GPO signals can be assigned to a specific R5FSS core by configuring the MSS_IOMUX. _PAD_ _CFG_REG.GPIO_SEL[17:16] of the associated IOMUX Pad Configuration register. 

This diagram describes the GPIO multiplexor connectivity. 

**==> picture [680 x 280] intentionally omitted <==**

**Figure 13-2. GPIO Mux Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1115 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## The tables below summarize the device integration details of GPIO# (where # = 0 to 3). 

## **Table 13-2.** _**GPIO**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|GPIO0|✔|PERI VBUSP Interconnect|
|GPIO1|✔|PERI VBUSP Interconnect|
|GPIO2|✔|PERI VBUSP Interconnect|
|GPIO3|✔|PERI VBUSP Interconnect|



## **Table 13-3.** _**GPIO**_ **Clocks** 

## This table describes the module clocking signals. 

|**Module Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default Freq**|**Description**|
|---|---|---|---|---|---|
|GPIO0|GPIO0_VBUS_FICLK|SYS_CLK|PLL_CORE_CLK:HSDIV0_CLKOUT<br>0|200 MHz|GPIO0 Functional and Interface<br>Clock|
|GPIO1|GPIO1_VBUS_FICLK|SYS_CLK|PLL_CORE_CLK:HSDIV0_CLKOUT<br>0|200 MHz|GPIO1 Functional and Interface<br>Clock|
|GPIO2|GPIO2_VBUS_FICLK|SYS_CLK|PLL_CORE_CLK:HSDIV0_CLKOUT<br>0|200 MHz|GPIO2 Functional and Interface<br>Clock|
|GPIO3|GPIO3_VBUS_FICLK|SYS_CLK|PLL_CORE_CLK:HSDIV0_CLKOUT<br>0|200 MHz|GPIO3 Functional and Interface<br>Clock|



## **Table 13-4.** _**GPIO**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|GPIO0|GPIO0_RST|Warm Reset (MOD_G_RST)|RCM + Warm Reset Source|GPIO0 Reset|
|GPIO1|GPIO1_RST|Warm Reset (MOD_G_RST)|RCM + Warm Reset Source|GPIO1 Reset|
|GPIO2|GPIO2_RST|Warm Reset (MOD_G_RST)|RCM + Warm Reset Source|GPIO2 Reset|
|GPIO3|GPIO3_RST|Warm Reset (MOD_G_RST)|RCM + Warm Reset Source|GPIO3 Reset|



**Table 13-5.** _**GPIO**_ **Interrupt Requests** 

## This table describes the module interrupt requests. 

|**Module Instance**|**Module Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|GPIO#|GPIO#_[0:138]|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO#_[0:138] interrupt request|
|GPIO#|GPIO#_BANK0_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK0 interrupt request|
|GPIO#|GPIO#_BANK1_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK1 interrupt request|



1116 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Table 13-5.** _**GPIO**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module Instance**|**Module Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|GPIO#|GPIO#_BANK2_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK2 interrupt request|
|GPIO#|GPIO#_BANK3_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK3 interrupt request|
|GPIO#|GPIO#_BANK4_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK4 interrupt request|
|GPIO#|GPIO#_BANK5_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK5 interrupt request|
|GPIO#|GPIO#_BANK6_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK6 interrupt request|
|GPIO#|GPIO#_BANK7_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK7 interrupt request|
|GPIO#|GPIO#_BANK8_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK8 interrupt request|



## **Note** 

## Where # = 0 to 3 

## **Table 13-6.** _**GPIO**_ **DMA Requests** 

## This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|GPIO#|N/A|N/A|N/A|N/A|The GPIO module does not support DMA<br>requests.|



## **Table 13-7.** _**GPIO**_ **Capture Event Inputs** 

## This table describes the module capture event inputs. 

|**Module**<br>**Instance**|**Module Capture Event Input**|**Capture Event Source Signal**|**Source**|**Type**|**Description**|
|---|---|---|---|---|---|
|GPIO#|N/A|N/A|N/A|N/A|The GPIO module does not support Capture<br>Event Inputs|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1117 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.1.1.4 GPIO Functional Description** 

## _**13.1.1.4.1 GPIO Block Diagram**_ 

Figure 13-3 shows the general-purpose interface block diagram. 

**==> picture [366 x 391] intentionally omitted <==**

**----- Start of picture text -----**<br>
GPIO peripheral<br>Data input/output<br>Direction DIR<br>Set<br>SET_DATA<br>data<br>Output OUT_DATA GP j (A)<br>data<br>Peripheral clocks<br>Clear (SYSCLK0/4) (CLK_32K_RC)<br>data CLR_DATA (MCU_SYSCLK0/6) (CLK_12M_RC)<br>Input Synchronization<br>IN_DATA<br>data logic<br>DMA event and<br>Interrupt and<br>interrupt generation Edge detection DMA event<br>logic (GPINT j (B))<br>Set rising<br>SET_RIS_TRIG<br>edge trigger<br>Rising edge (C)<br>RIS_TRIG<br>trigger<br>Clear rising<br>CLR_RIS_TRIG<br>edge trigger<br>Set falling<br>SET_FAL_TRIG<br>edge trigger<br>Falling edge (C)<br>FAL_TRIG<br>trigger<br>Clear falling<br>CLR_FAL_TRIG<br>edge trigger<br>**----- End of picture text -----**<br>


**==> picture [22 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
gpio_005<br>**----- End of picture text -----**<br>


- A. Where j = [0:143] 

- B. Some of the GPj pins are muxed with other device signals. For details, see the device-specific Data sheet. 

- C. All GPINTj can be used as host CPU interrupts via GPIO XBAR and synchronization events to the DMA. 

- D. The RIS_TRIG and FAL_TRIG registers are internal to the GPIO module and are not visible to the host CPU. 

## **Note** 

The synchronization logic and tristate buffer are present in the SoC pinmux logic. 

## **Figure 13-3. GPIO Block Diagram** 

## _**13.1.1.4.2 GPIO Function**_ 

Each GPIO pin (GPj) can be independently configured as either an input or an output using the GPIO direction registers. The GPIO direction register (DIR) specifies the direction of each GPIO signal. Logic 0 indicates the GPIO pin is configured as output, and logic 1 indicates input. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1118 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

When configured as output, writing a 0x1 to a bit in the set data register drives the corresponding GPj to a logic-high state. Writing a 0x1 to a bit in the clear data register drives the corresponding GPj to a logic-low state. The output state of each GPj can also be directly controlled by writing to the output data register. 

For example, to set GP8 to a logic-high state, the software can perform one of the following sequences: 

1. Sequence 1: 

   - Write 0h to the bit 8 of GPIO_DIR01 register to configure as output pin. 

   - Write 100h to the GPIO_SET_DATA01 register. 

2. Sequence 2: 

   - Write 0h to the to the bit 8 of GPIO_DIR01 register to configure as output pin. 

   - Read in GPIO_OUT_DATA01 register, change bit 8 to 0x1, and write the new value back to GPIO_OUT_DATA01. 

## **Note** 

From the above two sequences, Sequence 1 give results faster as sequence 2 involves readmodified-write. 

Similarly, to set GP8 to a logic-low state, the software can perform one of the following: 

1. Sequence 1: 

   - Write 0h to the to the bit 8 of GPIO_DIR01 register to configure as output pin. 

   - Write 100h to the GPIO_CLR_DATA01 register. 

2. Sequence 2: 

   - Write 0h to the to the bit 8 of GPIO_DIR01 register to configure as output pin. 

   - Read in GPIO_OUT_DATA01 register, change bit 8 to 0x0, and write the new value back to GPIO_OUT_DATA01. 

## **Note** 

From the above two sequences, Sequence 1 give results faster as sequence 2 involves readmodified-write. 

Note that writing a 0x0 to bits in the set data and clear data registers does not affect the GPIO pin state. 

Also, for GPIO pins configured as input, writing to the set data, clear data, or output data registers does not affect the pin state. 

For a GPIO pin configured as input, reading the input data register (IN_DATA) will return the pin state. Reading the SET_DATA register or the CLR_DATA data register will return the value in OUT_DATA, not the actual pin state. The pin state is available by reading the input data register. Note that when the direction is configured as input, the output state is determined by software’s programming set/clear/output registers, and may not agree with the pin state, which is driven by an external device. 

## _**13.1.1.4.3 GPIO Interrupt and Event Generation**_ 

Each GPIO pin (GPj) can be configured to generate a host CPU interrupt (GPINTj) or a synchronization event to the DMA (GPINTj). Configuration is on per-bank basis. Each bit of the BINTEN parameter dictates YES/NO option for each bank. Bit 0 controls bank 0, bit 1 controls bank 1, and so on. 

The interrupt can be generated on the rising-edge, falling-edge, or on both edges of the GPIO signal and can be routed as a DMA event through the GPIO XBAR. The edge detection logic is synchronized to the GPIO peripheral clock. 

The direction of the GPIO pin does not need to be input when using the pin to generate the interrupt or DMA event. When the GPIO pin is configured as input, transitions on the pin trigger interrupts or DMA events. When the GPIO pin is configured as output, software can toggle the GPIO output register to change the pin state and in turn trigger the interrupt or DMA event. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1119 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

Note that the direction of the pin need not be input for interrupt generation to work. When the GPIO pin is configured as input, transitions on the pin trigger interrupts. When the GPIO pin is configured as output, firmware can toggle the GPIO output register to change the pin state, and in turn trigger interrupts. 

Each interrupt output of GPIO signal are available at the module boundary. Each group of 16 GPIO_INTR_INTj signals also has their masked interrupt outputs ORed together to generate a per bank interrupt, available at the module boundary. The idea is to either connect individual interrupts or per bank interrupts to the system interrupt controller. 

## _**13.1.1.4.3.1 Interrupt Enable (per Bank)**_ 

The GPIO_BINTEN register provides interrupt enable/disable feature for each bank of 16 GPINT signals. 

## _**13.1.1.4.3.2 Trigger Configuration (per Bit)**_ 

Two internal registers, RIS_TRIG and FAL_TRIG, specify which edge of the GPj signal generates an interrupt or DMA event. Each bit in these two registers corresponds to a GPj pin. Table 13-8 describes the host CPU interrupt and DMA event generation of GPj pin based on the bit settings of the RIS_TRIG and FAL_TRIG registers. 

**Table 13-8. GPIO Interrupt and DMA Event Configuration Options** 

|**RIS_TRIG Bit n**|**FAL_TRIG Bit n**|**Host CPU Interrupt and DMA Event Generation**|
|---|---|---|
|0|0|GPINTj interrupt and DMA event is disabled|
|0|1|GPINTj interrupt and DMA event is triggered on falling<br>edge of GPj signal|
|1|0|GPINTj interrupt and DMA event is triggered on rising<br>edge of GPj signal|
|1|1|GPINTj interrupt and DMA event is triggered on both rising<br>and falling edge of GPj signal|



The RIS_TRIG and FAL_TRIG registers are not directly accessible or visible to the host CPU. These registers are accessed indirectly through four registers: SET_RIS_TRIG, CLR_RIS_TRIG, SET_FAL_TRIG, and CLR_FAL_TRIG. Writing 1 to a bit on the SET_RIS_TRIG register sets the corresponding bit on the RIS_TRIG register. Writing 1 to a bit of the CLR_RIS_TRIG register clears the corresponding bit on the RIS_TRIG register. Writing to the SET_FAL_TRIG and CLR_FAL_TRIG registers works the same way on the FAL_TRIG register. 

Reading the SET_RIS_TRIG or CLR_RIS_TRIG register returns the value of the RIS_TRIG register. Reading from the SET_FAL_TRIG or CLR_FAL_TRIG register returns the value of the FAL_TRIG register. 

To use the GPIO pins as sources for host CPU interrupts and DMA events, the associated bank interrupt enable register bit in GPIO_BINTEN must also be set to 1. For example, to enable GPIO0_19 (which is in bank 1), GPIO_BINTEN[1] = 1 should be set to enable interrupts for bank 1. 

## _**13.1.1.4.3.3 Interrupt Status and Clear (per Bit)**_ 

The INTSTAT registers provide interrupt status upon reading, and interrupt clear feature upon writing 1 to the corresponding bit position(s). Upon receiving an interrupt, the ISR can examine the interrupt status and clear the processed interrupts. 

## **Note** 

The GPIO module generates an interrupt pulse on the individual GPINT interrupt in response to each occurrence of the specified edge condition. Therefore, for GPINT signals having their interrupts routed directly to the interrupt controller, it is not necessary to clear the status bits in this module. The interrupt status and clear register is a facility for the per-bank interrupt connection. 

1120 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.1.1.4.4 Input Qualification**_ 

The input qualification scheme has been designed to be very flexible. Select the type of input qualification for each GPIO pin by configuring the MSS_IOMUX_<PAD>_CFG_REG[QUAL_SEL] registers. In the case of a GPIO input pin, the qualification can be specified as only synchronized to SYSCLK or qualification by a sampling window. For pins that are configured as peripheral inputs, the input can also be asynchronous in addition to synchronized to SYSCLK or qualified by a sampling window. The remainder of this section describes the options available. 

## _**13.1.1.4.4.1 No Synchronization (Asynchronous Input)**_ 

This mode is used for peripherals where input synchronization is not required or the peripheral performs the synchronization. Examples include communication ports UART, SPI, and I[2] C. 

## **Note** 

Using input synchronization when the peripheral performs the synchronization can cause unexpected results. The user must make sure that the GPIO pin is configured for asynchronous in this case. 

## _**13.1.1.4.4.2 Synchronization to SYSCLK Only**_ 

This is the default qualification mode of all the pins at reset. In this mode, the input signal is only synchronized to the system clock (SYSCLK). Because the incoming signal is asynchronous, a SYSCLK period of delay is needed for the input to the device to be changed. No further qualification is performed on the signal. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1121 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.1.4.4.3 Qualification Using a Sampling Window**_ 

In this mode, the signal is first synchronized to the system clock (SYSCLK) and then qualified by a specified number of cycles before the input is allowed to change. Figure 13-4 and Figure 13-5 show how the input qualification is performed to eliminate unwanted noise. Two parameters are specified by the user for this type of qualification: 1) the sampling period, or how often the signal is sampled, and 2) the number of samples to be taken. 

**==> picture [421 x 178] intentionally omitted <==**

**----- Start of picture text -----**<br>
Time between samples<br>GPxCTRL Reg<br>GPIOx SYNC Qualification Input Signal<br>Qualified By 3<br>or 6 Samples<br>GPxQSEL1/2<br>SYSCLKOUT<br>Number of Samples<br>**----- End of picture text -----**<br>


**Figure 13-4. Input Qualification Using a Sampling Window** 

## **Note** 

For AM263Px, GPxCTRL Reg = 

MSS_IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] and GPxQSEL 1/2 = IOMUX.*_CFG_REG[QUAL_SEL] in the diagram above. This qualification logic is implemented in the SOC_PINMUX and is fed to the GPIO module. 

## **Time between samples (sampling period):** 

To qualify the signal, the input signal is sampled at a regular period. The sampling period is specified by the user and determines the time duration between samples, or how often the signal is sampled, relative to the CPU clock (SYSCLK). 

The sampling period is specified by the qualification period (QUAL_PERIOD_PER_SAMPLE) bits in IOMUX_QUAL_GRP*_*_CFG_REG. The sampling period is configurable in groups of 8 input signals. For example, GPIO0 to GPIO7 use MSS_IOMUX. **QUAL_GRP_0_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] setting and GPIO8 to GPIO15 use MSS_IOMUX. **QUAL_GRP_1_CFG_REG** [QUAL_PERIOD_PER_SAMPLE]. Table 13-9 and Table 13-10 show the relationship between the sampling period or sampling frequency and the MSS_IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] setting. 

**Table 13-9. Sampling Period** 

||**Sampling Period**|
|---|---|
|If|1 × TSYSCLK|
|IOMUX.**QUAL_GRP_*_CFG_REG**[QUAL||
|_PERIOD_PER_SAMPLE] = 0||
|If|2 × IOMUX.**QUAL_GRP_*_CFG_REG**[QUAL_PERIOD_PER_SAMPLE] × TSYSCLK|
|IOMUX.**QUAL_GRP_*_CFG_REG**[QUAL||
|_PERIOD_PER_SAMPLE] ≠ 0||
||Where TSYSCLKis the period in time of SYSCLK|



1122 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-10. Sampling Frequency Sampling Frequency** If fSYSCLK IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL _PERIOD_PER_SAMPLE] = 0 If fSYSCLK × 1 ÷ (2 × IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] ) _PERIOD_PER_SAMPLE] ≠ 0 Where fSYSCLK is the frequency of SYSCLK 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1123 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

From these equations, the minimum and maximum time between samples can be calculated for a given SYSCLK frequency: 

## **Example: Maximum Sampling Frequency:** 

If IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] = 0 

then the sampling frequency is fSYSCLK 

If, for example, fSYSCLK = 200MHz 

then the signal is sampled at 200MHz or one sample every 5ns. 

## **Example: Minimum Sampling Frequency:** 

If IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] = 0xFF (255) 

then the sampling frequency is fSYSCLK × 1 ÷ (2 × IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] ) 

If, for example, fSYSCLK = 200MHz 

then the signal is sampled at 200MHz × 1 ÷ (2 × 255) (392.157kHz) or one sample every 2.5μs. 

## **Number of samples:** 

The number of times the signal is sampled is either three samples or six samples as specified in the qualification selection IOMUX.*_CFG_REG[QUAL_SEL] registers. When three or six consecutive cycles are the same, then the input change is passed through to the device. 

## **Total Sampling-Window Width:** 

The sampling window is the time during which the input signal is sampled as shown in Figure 13-5. By using the equation for the sampling period, along with the number of samples to be taken, the total width of the window can be determined. 

For the input qualifier to detect a change in the input, the level of the signal must be stable for the duration of the sampling-window width or longer. 

The number of sampling periods within the window is always one less than the number of samples taken. For a three-sample window, the sampling-window width is two sampling-periods wide where the sampling period is defined in Table 13-9. Likewise, for a six-sample window, the sampling-window width is five sampling-periods wide. Table 13-11 and Case 2: Six-Sample Sampling-Window Width show the calculations used to determine the total sampling-window width based on IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] and the number of samples taken. 

**Table 13-11. Case 1: Three-Sample Sampling-Window Width** 

||**Total Sampling-Window Width**|
|---|---|
|If|<br>2 × TSYSCLK|
|IOMUX.**QUAL_GRP_*_CFG_REG**[QUAL_||
|PERIOD_PER_SAMPLE] = 0||
|If|<br>2 × 2 × IOMUX.**QUAL_GRP_*_CFG_REG**[QUAL_PERIOD_PER_SAMPLE] × TSYSCLK|
|IOMUX.**QUAL_GRP_*_CFG_REG**[QUAL_||
|PERIOD_PER_SAMPLE] ≠ 0||
||Where TSYSCLKis the period in time of SYSCLK|



## **Table 13-12. Case 2: Six-Sample Sampling-Window Width** 

||**Total Sampling-Window Width**|
|---|---|
|If|<br>5 × TSYSCLK|
|IOMUX.**QUAL_GRP_*_CFG_REG**[QUAL_||
|PERIOD_PER_SAMPLE] = 0||



1124 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Table 13-12. Case 2: Six-Sample Sampling-Window Width (continued)** 

**Total Sampling-Window Width** If 5 × 2 × IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] × TSYSCLK Where TSYSCLK is the period in time of SYSCLK 

IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_ PERIOD_PER_SAMPLE] ≠ 0 

## **Note** 

The external signal change is asynchronous with respect to both the sampling period and SYSCLK. Due to the asynchronous nature of the external signal, the input must be held stable for a time greater than the sampling-window width to make sure the logic detects a change in the signal. The extra time required can be up to an additional sampling period + TSYSCLK. 

The required duration for an input signal to be stable for the qualification logic to detect a change is described in the data sheet. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1125 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Example Qualification Window:** 

For the example shown in Figure 13-5, the input qualification has been configured as follows: 

- IOMUX.*_CFG_REG[QUAL_SEL] = 1,0. This indicates a six-sample qualification. 

- IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] = 1. The sampling period is tw(SP) = 2 ×IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] × TSYSCLK = 2 x TSYSCLK. 

This configuration results in the following: 

- The width of the sampling window is: 

   - tw(IQSW) = 5 × tw(SP) = 5 × 2 × IOMUX. **QUAL_GRP_*_CFG_REG** [QUAL_PERIOD_PER_SAMPLE] × TSYSCLK = 5 × 2 × TSYSCLK 

- If, for example, TSYSCLK = 5ns, then the duration of the sampling window is: 

   - Sampling period, tw(SP) = 2 x TSYSCLK = 2 × 5ns = 10ns 

Sampling window, tw(IQSW) = 5 × tw(SP) = 5 × 5ns = 25ns 

- To account for the asynchronous nature of the input relative to the sampling period and SYSCLK, up to a single additional sampling period and SYSCLK period is required to detect a change in the input signal. For this example: 

tw(IQSW) + tw(SP) + TSYSCLK = 25ns + 10ns + 5ns = 40ns 

- In Figure 13-5, the glitch (A) is shorter then the qualification window and is ignored by the input qualifier. 

**==> picture [458 x 151] intentionally omitted <==**

**----- Start of picture text -----**<br>
(A)<br>GPIO Signal QUAL_SEL = 1,0 (6 samples)<br>tW(SP) Sampling Period determined by<br>GPxCTRL [QUALPRD]  [(B)]<br>tW(IQSW) (SYSCLKOUT Cycle * 2 * QUALPRD) * 5 [(C)]<br>Sampling Window<br>SYSCLKOUT<br>QUADPRD=1<br>(SYSCLKOUT/2) (D)<br>Output From<br>Qualifier<br>1 1 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 1 1 1 1 1<br>**----- End of picture text -----**<br>


**Figure 13-5. Input Qualifier Clock Cycles** 

- **A.** This glitch is ignored by the input qualifier. The QUALPRD bit field specifies the qualification sampling period and can vary from 0x00 to 0xFF. If QUALPRD = 00, then the sampling period is 1 SYSCLKOUT cycle. For any other value 'n', the qualification sampling period is 2n SYSCLKOUT cycles (that is, at every 2n SYSCLKOUT cycles, the GPIO pin is sampled). 

- **B.** The qualification period selected using the GPxCTRL register applies to groups of 8 GPIO pins. 

- **C.** The qualification block can take either 3 or 6 samples. The QUAL_SEL Register selects which samples mode is used. 

- **D.** In the example shown, for the qualifier to detect the change, the input must be stable for 10 SYSCLKOUT cycles. That makes sure of 5 sampling periods for detection to occur. Since external signals are driven asynchronously, a 13 SYSCLKOUT-wide pulse makes sure of reliable recognition. 

1126 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

For AM263Px, SYSCLKOUT = SYSCLK in the diagram above. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1127 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.1.4.5 GPIO Interrupt Connectivity**_ 

Because this device muxes GPIO signals with other functional signals, the availability of any particular GPIO, and hence the usability of the associated interrupt, changes based on the use case pin muxing. Due to the large number of possible GPIO interrupt sources, routing all interrupt events to each processing element is impractical. Since most applications do not typically require a large number of GPIO interrupts, the interrupt uncertainty is resolved by mapping all GPIO interrupts to a series of event muxes implemented using Interrupt Router (IntRouter) modules. For AM26x devices, the Interrupt Router modules are referred to as GPIO_XBAR_INTROUTER modules. These muxes allow any one of the available GPIO interrupts to be selected and passed on as an event to the various processor interrupt controllers and DMA controllers. Event selection is controlled through associated registers within each IntRouter. 

The GPIO bank interrupts already represent a consolidation of the 16 GPIO interrupts associated with each bank and are routed directly to various interrupt controllers rather than through the GPIO IntRouters. 

## _**13.1.1.4.6 GPIO Emulation Halt Operation**_ 

The GPIO peripheral is not affected by emulation halts. 

1128 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.1.2 Inter-Integrated Circuit (I2C) Interface**_ 

This section describes the Inter-Integrated Circuit (I2C) module in the device. 

## **13.1.2.1 I2C Overview** 

The I2C module is a serial bus that supports multiple controller devices. In multicontroller mode, one or more devices can be connected to the same bus and are capable of controlling the bus. Each I2C device on the bus is recognized by a unique address and can operate as either a transmitter or a receiver, depending on the function of the device. In addition to being a transmitter or receiver, a device connected to the I2C bus can also be considered a controller or a peripheral when performing data transfers. 

## **Note** 

A controller device is the device that initiates the data transfer on a bus and generates the clock signal that permits the transfer. During the transmission, any device addressed by the controller is considered the peripheral. 

Data is communicated to devices interfacing to the I2C module using the serial data pin (SDA) and the serial clock pin (SCL) as shown in Figure 13-6. These two wires carry information between the device and the other devices connected to the I2C bus. Both SDA and SCL pins on the device are bidirectional. They must be connected to a positive supply voltage through a pull-up resistor. When the bus is free, both pins are high. The driver of these two pins has an open-drain configuration to perform the wired-AND function. 

The device has a special mode that can be entered to ignore a NACK generated from non-compliant I2C devices that are incapable of generating an ACK. 

The I2C module consists of the following primary blocks: 

- A serial Interface: one data pin (SDA) and one clock pin (SCL) 

- The device register interface: 

   - Data registers to temporarily hold received data and transmitted data traveling between the SDA pin and the CPU or the DMA 

   - Control and status registers 

- A prescaler to divide down the input clock that is driven to the I2C module 

- A peripheral bus interface to enable the CPU and DMA to access the I2C module registers 

- An arbitrator to handle arbitration between the I2C module (when configured as a controller) and another controller 

- Interrupt generation logic (interrupts can be sent to the CPU) 

- A clock synchronizer that synchronizes the I2C input clock (from the system module) and the clock on the SCL pin, and synchronizes data transfers with controllers of different clock speeds. 

- A noise filter on each of the two serial pins 

- DMA event generation logic that synchronizes data reception and data transmission in the I2C module for DMA transmission 

In Figure 13-6, the CPU or the DMA writes data for transmission to ICDXR and reads received data from ICDRR. When the I2C module is configured as a transmitter, data written to ICDXR is copied to ICXSR and shifted out one bit at a time. When the I2C module is configured as a receiver, received data is shifted into ICRSR and then copied to ICDRR. 

When the I2C function is not needed, the pins may be controlled as general-purpose input/output (GPIO) pins. The I/O structure of each pin includes: 

- Programmable slew rate control of the outputs 

- Open drain mode 

- Programmable pull enable/disable on the input 

- Programmable pull up/pull down function on the input 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1129 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [500 x 280] intentionally omitted <==**

**Figure 13-6. Simple I2C Block Diagram** 

1130 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.1.2.1.1 I2C Features**_ 

Each multi controller I2C module has the following features: 

- Compliance to the Philips I[2] C bus specification, v2.1 ( _The I2C Specification_ , Philips document number 9398 393 40011) 

   - Bit/Byte format transfer 

   - 7-bit device addressing modes 

   - General call 

   - START byte 

   - Multi-controller transmitter/ peripheral receiver mode 

   - Multi-controller receiver/ peripheral transmitter mode 

   - Combined controller transmit/receive and peripheral receive/transmit mode 

   - Transfer rates from 10kbps up to 100kbps (standard mode) and 400kbps (fast mode) 

- Free data format 

- Two configurable DMA events (transmit and receive) 

- Seven interrupts that can be used by the CPU 

- Operates with VBUS frequency of 6.7MHz and up 

- Operates with module frequency between 6.7MHz to 13.3MHz 

- Module enable/disable capability 

- The SDA and SCL are optionally configurable as general purpose I/O 

- Slew rate control of the outputs 

- Open drain control of the outputs 

- Programmable pullup/pulldown capability on the inputs 

- Supports Ignore NACK mode 

## **Note** 

Only the I2C0 instance is a true I2C Open Drain buffer. I2C[1-3] are implemented with the typical LVCMOS voltage buffer and must be properly configured to operate as an Input/Output Open Drain signal type. 

## _**13.1.2.1.2 I2C Not Supported Features**_ 

- High-speed (HS) mode 

- C-bus compatibility mode 

- The combined format in 10-bit address mode (the I2C sends the peripheral address second byte every time it sends the peripheral address first byte) 

- Low power clock enable 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1131 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.1.2.2 I2C Environment** 

This section describes the I2C external connections (environment). 

## _**13.1.2.2.1 I2C Typical Application**_ 

Figure 13-7 shows the multicontroller I2C controller and their related connections with I[2] C-compliant devices. 

**==> picture [500 x 302] intentionally omitted <==**

**----- Start of picture text -----**<br>
Pullup resistors (Rp)<br>Device +1.8V I2C-1.8V  I2C-1.8V  +3.0V I2C-3.0V  I2C-3.0V<br>Multicontroller Compatible  Compatible  Compatible  Compatible<br>I2C module device device device device<br>Serial clock<br>SCL<br>line<br>Serial data<br>SDA<br>line<br>Figure 13-7. I2C and Typical Connections to I2C Devices<br>Table 13-13 describes the I2C I/O signals.<br>Table 13-13. I2C I/O Signals<br>I2C[0]<br>SCL I2C[0]_SCL I/O I [2] C serial clock line. Open-drain output buffer. 1<br>SDA I2C[0]_SDA I/O I [2] C serial data line. Open-drain output buffer. 1<br>I2C[1-3]<br>SCL I2C[1:3]_SCL I/O I [2] C serial clock line. Emulated open-drain output buffer. 1<br>SDA I2C[1:3]_SDA I/O I [2] C serial data line. Emulated open-drain output buffer. 1<br>**----- End of picture text -----**<br>


(1) I = Input; O = Output; I/O = Bidirectional 

## _**13.1.2.2.1.2**_ 

## **Note** 

For more information about device level signals (pull-up/down resistors, buffer type, multiplexing and others), see tables _Pin Attributes_ and _Pin Multiplexing_ in the device-specific Data sheet. 

## _**13.1.2.2.2 I2C Typical Connection Protocol and Data Format 13.1.2.2.2.1 I2C Serial Data Formats**_ 

The I2C module operates in byte data format. Each message put on the SDA line is 2 to 8-bits long. The number of messages that can be transmitted or received is unrestricted. The data is transferred with the most significant bit (MSB) first (Figure 13-8). Each message is followed by an acknowledge bit from the I2C if it is in receiver mode. The I2C module does not support little endian systems. 

1132 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

**==> picture [504 x 106] intentionally omitted <==**

**----- Start of picture text -----**<br>
www.ti.com Peripherals<br>SDA<br>MSB Acknowledge signal Acknowledge signal<br>from receiver from receiver<br>SCL<br>1 2 3 6 7 8 9 1 2 3 7 8 9<br>STOP<br>START R/W ACK ACK condition (P)<br>condition (S)<br>~~ ~~<br>~~ ~~<br>~~ ~~<br>**----- End of picture text -----**<br>


**Figure 13-8. I2C Module Data Transfer** 

The first byte after a START condition (S) always consists of 8 bits that comprise either a 7-bit address plus the R/ W bit, or 8 data bits. The eighth bit, R/W, in the first byte determines the direction of the data. When the R/ W bit is 0, the controller writes (transmits) data to a selected peripheral device; when the R/ W bit is 1, the controller reads (receives) data from the peripheral device. In acknowledge mode, an extra bit dedicated for the acknowledgement (ACK) bit is inserted after each message. 

The I2C module supports the following formats: 

- 7-bit addressing format (Section 13.1.2.2.2.4.1) 

- 10-bit addressing format (Section 13.1.2.2.2.4.2) 

- 7-bit/10-bit addressing format with repeated START condition (Section 13.1.2.2.2.4.3) 

- Free-data format (Section 13.1.2.2.2.4.4) 

## _**13.1.2.2.2.2 I2C Data Validity**_ 

The data on the serial data line (SDA) must be stable during the high period of the serial clock line. The high and low states of the data line can change only when the clock signal on the serial clock line (SCL) is low. 

Figure 13-9 is an example of data validity requirements. 

**==> picture [432 x 101] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDA<br>SCL<br>Data line stable Data change allowed<br>Data valid<br>**----- End of picture text -----**<br>


**==> picture [15 x 4] intentionally omitted <==**

**----- Start of picture text -----**<br>
i2c-005<br>**----- End of picture text -----**<br>


**Figure 13-9. I2C Bit Transfer on the I2C Bus** 

## _**13.1.2.2.2.3 I2C Start and Stop Conditions**_ 

START and STOP conditions are generated by a controller I2C module. 

- The START condition is defined as a high-to-low transition on the SDA line while SCL is high. A controller drives this condition to indicate the start of data transfer. The bus is considered to be busy after the START condition, and the bus busy bit (BB) in ICSTR (Interrupt Status Register) is set to 1. 

- The STOP condition is defined as a low-to-high transition on the SDA line while SCL is high. A controller drives this condition to indicate the end of data transfer. The bus is considered to be free after the STOP condition, therefore the BB bit in ICSTR (Interrupt Status Register) is cleared to 0. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1133 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [350 x 89] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDA<br>SCL<br>START STOP<br>condition (S) condition (P)<br>~~<br>~~<br>~~<br>**----- End of picture text -----**<br>


**Figure 13-10. I2C Module START and STOP Conditions** 

For the I2C module to start a data transfer with a START condition, the controller mode bit (MST) and the START condition bit (STT) in the ICMDR must both be set to 1. For the I2C module to end a data transfer with a STOP condition, the STOP condition bit (STP) must be set to 1. When the BB bit is set to 1 and the STT bit is set to 1, a repeated START condition is generated. 

## _**13.1.2.2.2.4 I2C Addressing**_ 

The I2C module supports two data formats in fast/standard (F/S) mode: 

- 7-bit/10-bit addressing format 

- 7-bit/10-bit addressing format with repeated start (Sr) condition 

## _**13.1.2.2.2.4.1 7-Bit Addressing Format**_ 

In the 7-bit addressing format (Figure 13-11), the first byte after the START condition consists of a 7-bit peripheral address followed by the R/ W bit (in the LSB). The R/ W bit determines the direction of the data transfer: 

- R/ W = 0: The controller writes (transmits) data to the addressed peripheral. 

- R/ W = 1: The controller reads (receives) data from the peripheral. 

An extra clock cycle dedicated for acknowledgment (ACK) is inserted after each byte. If the ACK is inserted by the peripheral after the first byte from the controller, it is followed by n bits of data from the transmitter (controller or peripheral, depending on the R/ W bit). The device I2C allows n to be a number between 2 to 8, programmable by the bit count (BC) field of ICMDR. After the data bits have been transferred, the receiver inserts an ACK bit. 

To select the 7-bit addressing format, write 0 to the expanded address enable (XA) bit of I2CMDR and make sure the free data format mode is off (FDF = 0 in ICMDR). 

**==> picture [436 x 37] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 7 1 1 8 1 8 1 1<br>S Target address R/W ACK Data ACK Data ACK P<br>**----- End of picture text -----**<br>


**Figure 13-11. I2C Module 7-Bit Addressing Format** 

## _**13.1.2.2.2.4.2 10-Bit Addressing Format**_ 

The 10-bit addressing format is similar to the 7-bit addressing format, but the controller sends the peripheral address in two separate byte transfers. In the 10-bit addressing format (Figure 13-12), the first byte is 11110b, the two MSBs of the 10-bit peripheral address, and the R/ W bit. The ACK bit is inserted after each byte. The second byte is the remaining 8 bits of the 10-bit peripheral address. The peripheral must send an acknowledgement after each of the two byte transfers. Once the controller has written the second byte to the peripheral, the controller can either write data or use repeated a START condition to change the data direction. 

To select the 10-bit addressing format, write 1 to the expanded address enable (XA) bit of ICMDR and make sure the free data format mode is off (FDF = 0 in ICMDR). 

1134 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

|1|7|1<br>1|1<br>1|1<br>1|8|1<br>8<br>1<br>1|1<br>8<br>1<br>1|1<br>8<br>1<br>1|1<br>8<br>1<br>1|1<br>8<br>1<br>1|
|---|---|---|---|---|---|---|---|---|---|---|
|S|Target address 1st byte||R/W|ACK|Target address 2nd byte||ACK|Data|ACK|P|



**Figure 13-12. I2C Module 10-bit Addressing Format** 

## _**13.1.2.2.2.4.3 Using the Repeated START Condition**_ 

At the end of each byte, the controller can drive another START condition (Figure 13-13). Using this capability, a controller can transmit/receive any number of data bytes before generating a STOP condition. The length of a data byte can be from 2 to 8 bits. The repeated START condition can be used with the 7-bit addressing, 10-bit addressing, or the free data formats. 

**==> picture [436 x 40] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 7 1 1 8 1 1 7 1 1 8 1 1<br>S Target address R/W ACK Data ACK S Target address R/W ACK Data ACK P<br>**----- End of picture text -----**<br>


**Figure 13-13. I2C Module 7-Bit Addressing Format with Repeated START** 

## _**13.1.2.2.2.4.4 Free Data Format**_ 

In this format (Figure 13-14), the first byte after a START condition is a data byte. The ACK bit is inserted after each byte, followed by another 8 bits of data. No address or data direction bit is sent. Therefore, the transmitter and receiver must both support the free data format. The direction of data transmission (transmit or receive) remains constant throughout the transfer. 

To select the free data format, write a 1 to the free data format (FDF) bit of the ICMDR. The free data format is not supported in the digital loop back mode. 

**==> picture [438 x 39] intentionally omitted <==**

**----- Start of picture text -----**<br>
1 8 1 8 1 8 1 1<br>S Data ACK Data ACK Data ACK P<br>**----- End of picture text -----**<br>


**Figure 13-14. I2C Module in Free Data Format** 

## _**13.1.2.2.2.5 I2C Controller Transmitter**_ 

All Controllers begin in this mode. The I2C module is a Controller and transmits control information and data to a target. In this mode, data assembled in any of the addressing formats shown in Figure 13-11, Figure 13-12, or Figure 13-13 is shifted out onto the SDA pin and synchronized with the self-generated clock pulses on the SCL pin. The clock pulses are inhibited and the SCL pin is held low when the intervention of the device is required ( XSMT = 0) after a byte has been transmitted. 

## **Note** 

If the I2C is configured for two simultaneous Controller transmissions, wait until the MST and BB have been reset before performing the second Controller transmission. 

Failure to wait for the MST and BB to reset will prevent the start condition on the second transfer from being issued and the bus BB will not be set. Typically the end of the first transfer is handled by polling BB. However, the MST bit is not reset at the same instant as the BB bit. As a result, when the second Controller transmission is initiated before the resetting of the MST, the MST bit for the second transfer is reset. This prevents the I2C from recognizing itself as the Controller, thus failing to occupy the bus. 

## _**13.1.2.2.2.6 I2C Controller Receiver**_ 

In this mode, the I2C module is a controller and receives data from a target. This mode can only be entered from the controller transmitter mode (the I2C module must first transmit a command to the target). In any of the addressing formats shown in Section 13.1.2.2.2.4.1, Section 13.1.2.2.2.4.2, or Section 13.1.2.2.2.4.3, the 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1135 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

controller receiver mode is entered after the target address byte and the R/ W bit have been transmitted (if the R/ W bit is 1). Serial data bits received on the SDA pin are shifted in with the self-generated clock pulses on the SCL pin. The clock pulses are inhibited and the SCL is held low when the intervention of the device is required (RSFULL = 1) after a byte has been received. At the end of the transfer, the controller-receiver signals the end of data to the target-transmitter by not generating an acknowledge on the last byte that was clocked out of the target. The target-transmitter then releases the data line allowing the controller-receiver to generate a STOP condition or a repeated START condition. 

In many applications, the size of the message is in the initial bytes of the message itself. Since the size of the message is not known to the controller before the transmission/reception starts, the controller must use the repeat mode in order to force the stop condition when the reception is completed. The repeat mode is enabled by setting the RM bit to 1. Due to the double buffer implementation on the receive side, the controller must generate the stop condition (STP =1) after reading the (message size - 1)[th] data. 

## _**13.1.2.2.2.7 I2C Target Transmitter**_ 

In this mode, the I2C module is a target and transmits data to a controller. This mode can only be entered from the target receiver mode (The I2C module must first receive a command from the controller). In any of the addressing formats shown in Section 13.1.2.2.2.4.1, Section 13.1.2.2.2.4.2, or Section 13.1.2.2.2.4.3, the target transmitter mode is entered if the target address byte is the same as its own address and the R/ W bit has been transmitted (if the R/ W bit is set to 1). The target transmitter shifts the serial data out on the SDA pin with the clock pulses that are generated by the controller device. The target device does not generate the clock, but it can hold the SCL pin low when intervention of the device is required (XSMT = 0) after a byte has been transmitted. 

## _**13.1.2.2.2.8 I2C Target Receiver**_ 

In this mode, the I2C module is a target and receives data from a controller. All targets begin in this mode. Serial data bits received on the SDA pin are shifted in with the clock pulses that are generated by the controller device. The target device does not generate the clock, but it can hold the SCL pin low while intervention of the device is required (RSFULL = 1) after a byte has been received. 

## _**13.1.2.2.2.9 I2C Bus Arbitration**_ 

If two or more controller transmitters simultaneously start a transmission on the same bus, an arbitration procedure is invoked. Figure 13-15 illustrates the arbitration procedure between two devices. The arbitration procedure uses the data presented on the SDA bus by the competing transmitters. The first controller transmitter that generates a high is overruled by the other controller that generates a low. The arbitration procedure gives priority to the device that transmits the serial data stream with the lowest binary value. The controller transmitter that loses the arbitration switches to the peripheral receiver mode, sets the arbitration lost (AL) flag, and generates the arbitration-lost interrupt. The data transmitted by the other controller module is salvaged, and the I2C continues to receive data from the controller module. Should two or more devices send identical first bytes, arbitration continues on the subsequent bytes. 

If, during a serial transfer, the arbitration procedure is still in progress when a repeated START condition or STOP condition is transmitted to I2C bus, the controller transmitters involved must send the repeated START condition or STOP condition at the same position in the format frame. In other words, arbitration is not allowed between: 

- A repeated START condition and a data bit 

- A STOP condition and a data bit 

- A repeated START condition and a STOP condition 

Peripherals are not involved in the arbitration procedure. 

1136 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

Device #1 lost arbitration and switches off 

**==> picture [256 x 137] intentionally omitted <==**

**----- Start of picture text -----**<br>
Data from<br>device #1 1 0<br>Data from<br>device #2 1 0 0 1 0<br>Bus line<br>SDA 1 0 0 1 0<br>Bus line<br>SCL<br>**----- End of picture text -----**<br>


**Figure 13-15. Arbitration Procedure Between Two Controller Transmitters** 

## _**13.1.2.2.2.10 I2C Clock Generation and Synchronization**_ 

Under normal conditions only one controller device generates the clock signal; the SCL. During the arbitration procedure, however, there are two or more controller devices and the clock must be synchronized so that the data output can be compared. Figure 13-16 illustrates clock synchronization. The wired-AND property of the SCL line means that a device that first generates a low period on the SCL overrules the other devices. At this high-to-low transition, the clock generators of the other devices are forced to start their own low period. The SCL line is held low by the device with the longest low period. The other devices that finish their low periods must wait for the SCL line to be released before starting their high periods. A synchronized signal on the SCL is obtained where the slowest device determines the length of the low period and the fastest device determines the length of the high period. 

If a device pulls down the clock line for a longer time, the result is that all clock generators must enter the wait state. In this way, a peripheral slows down a fast controller and the slow device creates enough time to store a received byte or to prepare a byte to be transmitted. 

## **Note** 

## **I2C Protocol Fault** 

The following conditions violate the clock spec as defined in the Philips I[2] C bus specification, v2.1 ( _The I 2 C Specification,_ Philips document number 9398 393 40011), and will result in an I2C protocol fault: I2CCLKH = 2, I2CCLKL = 2, I2CPSC = 2. This will cause the SDA data transition to occur while the SCL is high. 

**==> picture [235 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
Wait Start HIGH<br>State period<br>SCL from<br>device #1<br>SCL from<br>device #2<br>Bus line<br>SCL<br>**----- End of picture text -----**<br>


**Figure 13-16. Synchronization of Two I2C Clock Generators During Arbitration** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1137 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.1.2.3 I2C Integration** 

There are 4x I2C module integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [500 x 297] intentionally omitted <==**

**Figure 13-17. I2C Integration Diagram** 

The tables below summarize the device integration details of I2C# (where # = 0, 1, 2, 3). 

**Table 13-14.** _**I2C**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|I2C0|✓|PERI VBUSP Interconnect|
|I2C1|✓|PERI VBUSP Interconnect|
|I2C2|✓|PERI VBUSP Interconnect|
|I2C3|✓|PERI VBUSP Interconnect|



1138 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-15.** _**I2C**_ **Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|I2C[0:3]|I2C[0:3]_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|I2C[0:3] VBUS Clock|
||I2C[0:3]_FCLK<br>(I2C_CLK)|XTALCLK|External XTAL|25 MHz|I2C[0:3] Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0 (not supported)|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



**Table 13-16.** _**I2C**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|I2C0|I2C0_RST(VBUSP_RST<br>n)|Warm Reset<br>(SYS_NPRST)|RCM + Warm Reset Sources|I2C0 Asynchronous Reset|
|I2C1|I2C1_RST|Warm Reset<br>(SYS_NPRST)|RCM + Warm Reset Sources|I2C1 Asynchronous Reset|
|I2C2|I2C2_RST|Warm Reset<br>(SYS_NPRST)|RCM + Warm Reset Sources|I2C2 Asynchronous Reset|
|I2C3|I2C3_RST|Warm Reset<br>(SYS_NPRST)|RCM + Warm Reset Sources|I2C3 Asynchronous Reset|



**Table 13-17.** _**I2C**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|I2C0|i2c0_int_req<br>|i2c0_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Pulse|I2C0 Status Event Interrupt|
|I2C1|i2c1_int_req<br>|i2c1_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Pulse|I2C1 Status Event Interrupt|
|I2C2|i2c2_int_req<br>|i2c2_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Pulse|I2C2 Status Event Interrupt|
|I2C3|i2c3_int_req<br>|i2c3_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Pulse|I2C3 Status Event Interrupt|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1139 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-18.** _**I2C**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|I2C0|I2C0_TX|i2c0_dma_req_tx|EDMA Crossbar<br>(EDMA_XBAR)|Pulse|I2C0 DMA Transmit Request|
||I2C0_RX|i2c0_dma_req_rx|||I2C0 DMA Receive Request|
|I2C1|I2C1_TX|i2c1_dma_req_tx|EDMA Crossbar<br>(EDMA_XBAR)|Pulse|I2C1 DMA Transmit Request|
||I2C1_RX|i2c1_dma_req_rx|||I2C1 DMA Receive Request|
|IC2|I2C2_TX|i2c2_dma_req_tx|EDMA Crossbar<br>(EDMA_XBAR)|Pulse|I2C2 DMA Transmit Request|
||I2C2_RX|i2c2_dma_req_rx|||I2C2 DMA Receive Request|
|I2C3|I2C3_TX|i2c3_dma_req_tx|EDMA Crossbar<br>(EDMA_XBAR)|Pulse|I2C3 DMA Transmit Request|
||I2C3_RX|i2c3_dma_req_rx|||I2C3 DMA Receive Request|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

1140 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.1.2.4 I2C Functional Description** _**13.1.2.4.1 I2C Block Diagram**_ 

**==> picture [500 x 280] intentionally omitted <==**

**Figure 13-18. I2C Block Diagram** 

The I2C module consists of the following primary blocks: 

- Serial I/F 

- CPU Register Interface 

- Pre-scaler 

- VBUSP peripheral control I/F 

- VBUSP peripheral dual data I/F (DMA and CPU with CPU has higher priority) 

- Control/Status 

- Data/Address 

- I2C Clock generator 

Data is communicated to devices interfacing the I2C via the serial data pin (SDA) and the serial clock pin (SCL). These two wires carry information between the TI device and others connected to the I2C bus. Both SDA and SCL are bi-directional pins. They must be connected to a positive supply voltage via a pull-up resistor. When the bus is free, both pins are high. The driver of these two pins has an open-drain to perform the required wired-AND function. 

## _**13.1.2.4.2 I2C Clocks**_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1141 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.2.4.2.1 I2C Clocking**_ 

The I2C module is operated by the module clock. This clock is generated by way of the I2C prescaler block. The prescaler block consists of a 8-bit register, ICPSC, used for dividing down the device peripheral clock (VBUS_CLK) to obtain a module clock between 6.7 MHz and 13.3 MHz. 

As shown in Figure 13-19, the I2C module uses the input clock generated from the device clock generator to generate the module clock and controller clock. The I2C input clock is the device peripheral clock (VBUS_CLK). The clock is then divided twice more inside the I2C module to produce the module clock and the controller clock. 

**==> picture [387 x 183] intentionally omitted <==**

**----- Start of picture text -----**<br>
I2C Module<br>I2CCKL<br>I2CPSC I2CCKH<br>OSCIN I2C Input Clock Controller Clock<br>Clock To I2C Bus<br>Generator (VBUS_CLK) on SCL pin<br>Module Clock for<br>I2C Module Operation<br>**----- End of picture text -----**<br>


**Figure 13-19. Clocking Diagram for the I2C Module** 

The module clock determines the frequency at which the I2C module operates. A programmable prescaler in the I2C module divides down the input clock to produce the module clock. To specify the divide-down value, initialize the IPSC7_IPSC0 bit field of the prescaler register, ICPSC. The resulting frequency is: 

**==> picture [207 x 25] intentionally omitted <==**

**==> picture [19 x 10] intentionally omitted <==**

The module clock frequency must be between 6.7MHz and 13.3MHz. The prescaler can only be initialized while the I2C module is in the reset state (IRS = 0 in ICMDR). The prescaled frequency takes effect only when IRS is changed to 1. Changing the ICPSC value while IRS = 1 has no effect. 

The controller clock appears on the SCL pin when the I2C module is configured to be a controller on the I2C bus. This clock controls the timing of the communication between the I2C module and a peripheral. As shown in Figure 13-19, a second clock divider in the I2C module divides down the module clock to produce the controller clock. The clock divider uses the ICCLKL to divide down the low portion of the module clock signal and uses the ICCLKH to divide down the high portion of the module clock signal. 

The resulting frequency is: 

**==> picture [238 x 25] intentionally omitted <==**

**==> picture [293 x 25] intentionally omitted <==**

**==> picture [19 x 48] intentionally omitted <==**

**----- Start of picture text -----**<br>
(25)<br>(26)<br>**----- End of picture text -----**<br>


where _d_ depends on the value of ICPSC: 

|**ICPSC**|**d**|
|---|---|
|0|7|



1142 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

|**ICPSC**|**d**|
|---|---|
|1|6|
|Greater than 1|5|



## **Note** 

The controller clock frequency defined above does not include rise/fall time and latency of the synchronizer inside the module. The actual transfer rate is slower than the value calculated from the formula above. Also, due to the nature of SCL synchronization, the SCL clock period can change if SCL synchronization is taking place. 

## _**13.1.2.4.3 I2C Software Reset**_ 

The I2C module can be reset in the following two ways: 

- Through the global peripheral reset. A device reset causes a global peripheral reset. 

- By clearing the IRS bit in the I2C mode register (ICMDR). When the global peripheral reset is removed, the IRS bit is cleared to 0, keeping the I2C module in the reset state. 

## _**13.1.2.4.4 I2C Interrupt Requests**_ 

The I2C module generates seven types of interrupts. These seven interrupts are accompanied with seven interrupt mask bits in the interrupt mask register (ICIMR) and with seven interrupt flag bits in the status register (ICSTR). 

The I2C module generates the interrupt requests described below. All requests are multiplexed through an arbiter into a single I2C interrupt request to the CPU. Each interrupt request has a flag bit and an enable bit. Interrupts must be enabled prior to the occurrence of the expected interrupt condition. When one of the specified events occurs, the flag bit is set. If the corresponding enable bit is 0, the interrupt request is blocked. If the enable bit is 1, the interrupt request is forwarded to the CPU as an I2C interrupt request. As an alternative, the CPU can poll all of the bits shown in Table 13-19. 

**Table 13-19. Interrupt Requests Generated by I2C Module** 

|**Flag**|**Name**|**Generated**|
|---|---|---|
|AL|Arbitration-lost interrupt|Generated when the I2C module has lost an arbitration contest with another<br>controller-transmitter|
|NACK|No-acknowledge interrupt|Generated when the controller I2C does not receive an acknowledge from the<br>receiver|
|ARDY|Register-access-ready interrupt|Generated when the previously programmed address, data and command have<br>been performed and the status bits have been updated. The interrupt is used to<br>notify the device that the I2C registers are ready to be accessed.|
|ICRRDY|Receive-data-ready interrupt|Generated when the received data in the receive-shift register (ICSR) has been<br>copied into the data receive register (ICDRR). The RXRDY bit can also be polled<br>by the device to determine when to read the received data in the ICDRR.|
|ICXRDY|Transmit-data-ready interrupt|Generated when the transmitted data has been copied from the data transmit<br>register (ICDXR) into the transmit-shift register (ICXSR). The TXRDY bit can also<br>be polled by the device to determine when to write the next data into ICDXR.|
|SCD|Stop-condition-detect interrupt|Generated when a STOP condition has been detected.|
|AAS|Address-as-peripheral interrupt|Generated when the I2C has recognized its own peripheral address or an address<br>of all zeroes.|



## _**13.1.2.4.5 I2C Noise Filter**_ 

The noise filter is used to suppress any noises that are 50ns or less. It is designed to suppress noise with one module clock, assuming the lower and upper limits of the module clock are 6.7MHz and 13.3MHz, respectively. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1143 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.1.2.5 I2C Programming Guide** 

## _**13.1.2.5.1 I2C Low-Level Programming Models**_ 

## _**13.1.2.5.1.1 I2C Programming Model**_ 

This section describes the programming model of the multicontroller I2C controllers configured in I2C mode. Register names begin with _I2Cn_ where 'n' is the instance number of an I2C module. The instance number starts from 0 and increments up based on the number of I2C instances available on the device. 

## _**13.1.2.5.1.1.1 Main Program**_ 

## _**13.1.2.5.1.1.1.1 Module State after Reset**_ 

Before enabling the I2C controller, perform the following steps: 

1. Enable the functional and interface clocks. 

2. Program the prescaler to obtain an approximately 12-MHz internal sampling clock by programming the corresponding value in the _I2Cn_ICPSC_ I2C Prescaler Register IPSC7_IPSC0 bit field. This value depends on the frequency of the functional clock (SYS_CLK). 

3. Take the I2C controller out of reset by setting the _I2Cn_ICMDR[5]_ IRS bit to 1. 

   - a. If using interrupts for transmitting/receiving data, enable the interrupt masks in the _I2Cn_ICIMR_ I2C Interrupt Mask Register. 

   - b. If using DMA for transmitting/receiving data, enable the DMA via the _I2Cn_ICDMAC_ I2C DMA Control Register and then program the DMA controller. 

## _**13.1.2.5.1.1.1.2 Initialization Procedure**_ 

To initialize the I2C controller, use the _I2Cn_ICMDR_ I2C Mode Register bits to configure the respective modes such as controller/peripheral, transmitter/receiver, repeat mode, bit count, expanded addressing, and free run mode. 

## _**13.1.2.5.1.1.1.3 Section**_ 

Program the _I2Cn_ICCLKL_ I2C Clock Divider Low register and _I2Cn_ICCLKH_ I2C Clock Divider High register to obtain a bit rate of 100 kbps or 400 kbps. These values depend on the internal sampling clock frequency (see I2C Clocking). 

## _**13.1.2.5.1.1.1.4 Configure Address Registers**_ 

In controller mode, configure the peripheral address register to transmit by programming the _I2Cn_ICSAR[9-0]_ A9_A0 bit field. 

## **Note** 

For a 10-bit address, set the _I2Cn_ICMDR[8]_ XA bit to 1. 

In peripheral mode, configure the peripheral address for other controllers to use by programming the _I2Cn_ICOAR[9-0]_ A9_A0 bit field 

## _**13.1.2.5.1.1.1.5 Initiate a Transfer**_ 

If in controller transmitter mode, program the _I2Cn_ICDXR_ I2C Data Transmit register with the transmit data first. 

Poll the _I2Cn_ICSTR[12]_ I2C Interrupt Status register for the Bus Busy (BB) bit. If it is '0', the busy is not busy and the transfer can be initiated by configuring the start/stop condition in the _I2Cn_ICMDR_ I2C Mode Register with the STT and STP bits. 

## _**13.1.2.5.1.1.1.6 Receive Data**_ 

Poll the _I2Cn_ICSTR[3]_ I2C Interrupt Status register ICRRDY bit, or use the RRDY interrupt ( _I2Cn_ICIVR[2:0]_ I2C Interrupt Vector register INTCODE = 0b100) to read the receive data in the _I2Cn_ICDRR_ I2C Data Receive register. If the DMA is enabled, there are no I2C-specific registers for monitoring DMA activity. 

1144 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

In receive mode only, the _I2Cn_ICSTR[11]_ RSFULL bit indicates whether the receiver has experienced overrun. An overrun condition occurs when the shift register and the RX FIFO are full. An overrun condition does not result in data loss. 

## _**13.1.2.5.1.1.1.7 Transmit Data**_ 

Poll the _I2Cn_ICSTR[4]_ I2C Interrupt Status register ICXRDY bit, or use the XRDY interrupt ( _I2Cn_ICIVR[2:0]_ I2C Interrupt Vector register INTCODE = 0b101) to transmit data from the _I2Cn_ICDXR_ I2C Data Transmit register. If the DMA is enabled, there are no I2C-specific registers for monitoring DMA activity. 

## **Note** 

In transmit mode only, the _I2Cn_ICSTR[10]_ XSMT bit indicates whether the transmitter has experienced underflow. Underflow occurs when the shift register is empty and the _I2Cn_ICDXR_ register has not been loaded. 

## _**13.1.2.5.1.1.2 Interrupt Subroutine Sequence**_ 

Monitor the _I2Cn_ICIVR_ I2C Interrupt Vector register INTCODE bits to determine which interrupt occurred in the following sequence. 

1. Test for arbitration lost and resolve accordingly. 

2. Test for no acknowledgment and resolve accordingly. 

3. Test for register access ready and resolve accordingly. 

4. Test for receive data ready and resolve accordingly. 

5. Test for transmit data ready and resolve accordingly. 

6. Test for stop condition and resolve accordingly. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1145 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.3 Multichannel Serial Peripheral Interface (MCSPI)**_ 

This section describes the Multichannel Serial Peripheral Interface (MCSPI) modules for the device. 

## **13.1.3.1 MCSPI Overview** 

The MCSPI (SPI) module is a multichannel transmit/receive, controller/peripheral synchronous serial bus. There are 8 SPI modules in the device. 

## _**13.1.3.1.1 SPI Features**_ 

The SPI module includes the following main features: 

- Serial clock with programmable frequency, polarity, and phase for each channel 

- Wide selection of SPI word lengths, ranging from 4 to 32 bits 

- Up to two channels in controller mode, or single channel in receive mode 

- Each SPI controller operates at up to 50 MHz in controller mode and 25 MHz in target mode 

- SPI0 and SPI4 support 2 chip selects while SPI1, SPI2, SPI3, SPI5, SPI6, and SPI7 support 1 chip select 

- Supports DMA access (read/write req per channel) 

- Controller multichannel mode: 

   - Full duplex/half duplex 

   - Transmit-only/receive-only/transmit-and-receive modes 

   - Flexible input/output (I/O) port controls per channel 

   - Programmable clock granularity 

   - Per channel configuration for clock definition, polarity enabling, and word width 

- Single interrupt line for multiple interrupt source events 

- Enable the addition of a programmable start-bit for MCSPI transfer per channel (start-bit mode) 

- • Supports start-bit write command 

- Programmable timing control between chip select and external clock generation 

- Built-in FIFO available for a single channel 

## _**13.1.3.1.2 SPI Not Supported Features**_ 

The following features are not supported on this family of devices: 

- Peripheral mode wake-up 

- Retention during power down 

- In peripheral mode only channel 0 is used 

- Local power management of clock activity 

1146 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.1.3.2 SPI Environment** 

The SPI[0:7] modules are hereinafter referred to as the SPI or MCSPI module. 

This section describes the SPI external connections (environment). 

## _**13.1.3.2.1 MCSPI Protocol and Data Format**_ 

The synchronous MCSPI protocol allows a controller device to initiate serial data transfers to a peripheral device. A peripheral select line (SPIEN[i]) allows selection of an individual peripheral MCSPI device. Peripheral devices that are not selected do not interfere with MCSPI bus activities. 

MCSPI offers the flexibility to modify the following parameters to adapt to the device features: 

- Word length 

   - MCSPI supports any MCSPI word ranging from 4 bits to 32 bits long (the MCSPI_CHCONF_0/1/2/3[11-7] WL bit field). 

MCSPI word length can be changed between transmissions to allow the controller device to communicate with peripheral peripherals that have different requirements. 

- MCSPI enable (SPIEN[i], for channel i) 

The polarity of the MCSPI enable signals is programmable (the MCSPI_CHCONF_0/1/2/3[6] EPOL bit). SPIEN[i] signals can be active high or low. 

Assertion of the SPIEN[i] signals is programmable and can be done manually or automatically. The manual assertion mode is available in single controller mode only. SPIEN[i] can be kept active between words with the MCSPI_CHCONF_0/1/2/3[20] FORCE bit. 

Two consecutive words for two different peripheral devices can go along with active SPIEN[i] signals with different polarity. 

- Programmable start-bit 

In start-bit mode a start-bit is added before the MCSPI word length to indicate how the next MCSPI word must be handled. The start-bit is enabled by setting the MCSPI_CHCONF_0/1/2/3[23] SBE bit to 1. The MCSPI_CHCONF_0/1/2/3[24] SBPOL bit defines the polarity of the start-bit. 

- Programmable MCSPI clock 

   - Bit rate 

In controller mode, the baud rate of the MCSPI serial clock is programmable using the 50-MHz reference clock (from the device clock management module). Table 13-20 lists the SPICLK bit rates obtained for data transfer when programming the clock divider (the MCSPI_CHCONF_0/1/2/3[5-2] CLKD bit field). This is valid when MCSPI_CHCONF_0/1/2/3[29] CLKD bit field is 0. 

**Table 13-20. MCSPI Controller Clock Rates** 

|**Divider**|**Clock Rate**|
|---|---|
|1|50 MHz(1)|
|2|25 MHz(1)|
|4|12.5 MHz|
|8|6.25 MHz|
|16|3.125 MHz|
|32|1.5625 MHz|
|64|781.25 kHz|
|128|390.625 kHz|
|256|~195 kHz|
|512|~97.7 kHz|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1147 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-20. MCSPI Controller Clock Rates (continued)** 

|**Divider**|**Clock**|**Rate**|
|---|---|---|
|1024|~48.8|kHz|
|2048|~24.4|kHz|
|4096|~12.2|kHz|



(1) These frequencies are not necessarily supported by all MCSPI modules. For more information, see the _Timing Requirements and Switching Characteristics_ chapter in the device-specific Data sheet. 

- Polarity and phase 

The polarity (the MCSPI_CHCONF_0/1/2/3[1] POL bit) and the phase (the MCSPI_CHCONF_0/1/2/3[0] PHA bit) of the MCSPI serial clock (SPICLK) are configurable to offer four combinations. Software selects the right combination, depending on the device. See Table 13-21 and Figure 13-20. 

**Table 13-21. Phase and Polarity Combinations** 

|**Polarity (POL)**|**Phase (PHA)**|**MCSPI Mode**|**Description**|**Description**|
|---|---|---|---|---|
|0|0|Mode 0|SPICLK is inactive low and sampling occurs at the rising edge.||
|0|1|Mode 1|SPICLK is inactive low and sampling occurs at the falling edge.||
|1|0|Mode 2|SPICLK is inactive high and sampling occurs at the falling edge.||
|1|1|Mode 3|SPICLK is inactive high and sampling occurs at the rising edge.||
|||Sampling<br>Shift out|||
|||Mode 0|||
|||SPICLK|||
|||Mode 1|||
|||SPICLK|||
|||Mode 2|||
|||SPICLK|||
|||Mode 3|||
|||SPICLK|||



spi-004 

## **Figure 13-20. Phase and Polarity Combinations** 

## _**13.1.3.2.1.1 Transfer Format**_ 

In controller and peripheral modes, the MCSPI drives the data lines when SPIEN[i] is asserted. 

Each word is transmitted starting with the most-significant bit (MSB). 

This section explains the two cases of data transmission determined by the clock phase (PHA) and the type of data transmission using a start-bit (SBE) called the start-bit mode: 

- Transmission in mode 0 and mode 2 (PHA = 0) 

When PHA = 0, the first bit of the MCSPI word to transmit (on the controller or the peripheral data output pin) is valid one-half cycle of SPICLK after the assertion of SPIEN[i]. 

Therefore, the first edge of the SPICLK line is used by the controller to sample the first data bit sent by the peripheral. On the same edge, the first data bit sent by the controller is sampled by the peripheral. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1148 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

On the next SPICLK edge, the received data bit is shifted into the receive shift register and a new data bit is transmitted on the serial data line. 

This process continues for a number of pulses on the SPICLK line defined by the MCSPI word length programmed in the controller device, with data being latched on odd-numbered edges and shifted on evennumbered edges, see Figure 13-21. 

**==> picture [440 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transfer start Transfer end<br>SPICLK edge number 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16<br>SPICLK (POL=0)<br>SPICLK (POL=1)<br>Sample<br>Data from the controller MSB Bit6 Bit5 Bit4 Bit3 Bit2 Bit1 LSB<br>Data from the peripheral MSB Bit6 Bit5 Bit4 Bit3 Bit2 Bit1 LSB<br>Peripheral select<br>(SPIEN[i])<br>(SPIEN[i]) Half cycle of SPICLK Synchronization delay<br>spi-005<br>**----- End of picture text -----**<br>


## **Figure 13-21. Full-Duplex Transfer Format With PHA = 0** 

- Transmission in mode 1 and mode 3 (PHA = 1) 

When PHA = 1, the first bit of the MCSPI word to transmit (on the controller or the peripheral data output pin) is valid on the following SPICLK edge (one-half cycle later). This is the sampling edge for the controller and peripheral. A synchronization delay is added between the activation of SPIEN[i] and the first SPICLK edge. 

The received data bit is shifted into the shift register on the third SPICLK edge. 

This process continues for a number of pulses on the SPICLK line defined by the MCSPI word length programmed in the controller device, with data being latched on even-numbered edges and shifted on odd-numbered edges. 

## **Note** 

The minimum synchronization delay is one cycle of SPICLK, if the frequency of SPICLK equals the frequency of MCSPI_FCLK (MCSPI functional clock) in controller mode. The minimum synchronization delay is one-half cycle of SPICLK, if the frequency of SPICLK is lower than the frequency of MCSPI_FCLK in the controller and peripheral modes. 

- Transmission with a start-bit (SBE = 1) 

When the MCSPI_CHCONF_0/1/2/3[23] SBE bit is set to 1, a start-bit is added before the MSB to indicate whether the next MCSPI word must be handled as a command or as data. 

Figure 13-22 shows an example of a data transfer with an extra start-bit. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1149 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [454 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transfer start Transfer end<br>SPICLK edge number 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18<br>SPICLK (POL=0)<br>SPICLK (POL=1)<br>Sample<br>Data from the controller D/CX MSB Bit6 Bit5 Bit4 Bit3 Bit2 Bit1 LSB<br>Data from the peripheral D/CX MSB Bit6 Bit5 Bit4 Bit3 Bit2 Bit1 LSB<br>Peripheral select<br>(SPIEN[i])<br>tLead<br>spi-006<br>**----- End of picture text -----**<br>


**Figure 13-22. Extended MCSPI Transfer With a Start-Bit (SBE = 1)** 

## _**13.1.3.2.2 MCSPI in Controller Mode**_ 

Figure 13-23 shows a case in controller mode (full-duplex) where the MCSPI module is connected with one peripheral device. 

**==> picture [375 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>Generic SPI<br>Controller Device<br>SPI_CLK<br>SCLK<br>MCSPI SPI_D0<br>SI<br>Module<br>SPI_D1<br>SO<br>SPI_CS0<br>CS<br>**----- End of picture text -----**<br>


- A. Direction of D0 and D1 depends on MCSPI_CHCONF_0/1/2/3[16] DPE0, MCSPI_CHCONF_0/1/2/3[17] DPE1 and MCSPI_CHCONF_0/1/2/3[18] IS bits 

## **Figure 13-23. MCSPI Controller Mode (Full Duplex)** 

1150 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

Figure 13-24 shows the controller single mode, which can also be configured in receive-only mode. 

**==> picture [375 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>Generic SPI<br>Peripheral Device<br>SPI_CLK<br>SCLK<br>MCSPI<br>Module SPI_Dk<br>MI<br>SPI_CS0<br>CS<br>**----- End of picture text -----**<br>


k = 0 or 1 depending on MCSPI_CHCONF_0/1/2/3[16] DPE0, MCSPI_CHCONF_0/1/2/3[17] DPE1 and MCSPI_CHCONF_0/1/2/3[18] IS bits 

## **Figure 13-24. MCSPI Controller Single Mode (Receive Only)** 

## _**13.1.3.2.3 MCSPI in Peripheral Mode**_ 

Figure 13-25 shows a case in peripheral mode (full-duplex). 

## **Note** 

Only channel 0 can be configured as peripheral, but the chip-enable signal can be connected to any SPIEN[i] pin and then rerouted internally to channel 0 (the MCSPI_CHCONF_0[22-21] SPIENSLV bit field). For more information, see MCSPI Peripheral Mode. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1151 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [375 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>Generic SPI<br>Controller Device<br>SPI_CLK<br>SCLK<br>MCSPI SPI_D0<br>SI<br>Module<br>SPI_D1<br>SO<br>SPI_CS0<br>CS<br>**----- End of picture text -----**<br>


- A. Direction depends on MCSPI_CHCONF_0/1/2/3[16] DPE0, MCSPI_CHCONF_0/1/2/3[17] DPE1 and MCSPI_CHCONF_0/1/2/3[18] IS bits 

## **Figure 13-25. MCSPI Peripheral Mode (Full Duplex)** 

Figure 13-26 shows the peripheral single mode, which can also be configured in transmit-only mode. 

1152 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [375 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>Generic SPI<br>Controller Device<br>SPI_CLK<br>SCLK<br>MCSPI<br>Module SPI_Dk<br>MI<br>SPI_CS0<br>CS<br>**----- End of picture text -----**<br>


k = 0 or 1 depending on MCSPI_CHCONF_0/1/2/3[16] DPE0, MCSPI_CHCONF_0/1/2/3[17] DPE1 and MCSPI_CHCONF_0/1/2/3[18] IS bits 

## **Figure 13-26. MCSPI Peripheral Single Mode (Transmit Only)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1153 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.1.3.3 SPI Integration** 

There are 8x SPI modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [500 x 344] intentionally omitted <==**

**Figure 13-27. SPI Integration** 

1154 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

The tables below summarize the device integration details of SPI# (where # = 0 to 7). 

**Table 13-22.** _**SPI**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|SPI0|✓|PERI VBUSP Interconnect|
|SPI1|✓|PERI VBUSP Interconnect|
|SPI2|✓|PERI VBUSP Interconnect|
|SPI3|✓|PERI VBUSP Interconnect|
|SPI4|✓|PERI VBUSP Interconnect|
|SPI5|✓|PERI VBUSP Interconnect|
|SPI6|✓|PERI VBUSP Interconnect|
|SPI7|✓|PERI VBUSP Interconnect|



**Table 13-23.** _**SPI**_ **Clocks** 

## This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|SPI0|SPI0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI0 VBUS Clock|
||SPI0_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI0 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1155 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-23.** _**SPI**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|SPI1|SPI1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI1 VBUS Clock|
||SPI1_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI1 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|SPI2|SPI2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI2 VBUS Clock|
||SPI2_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI2 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



1156 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-23.** _**SPI**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|SPI3|SPI3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI3 VBUS Clock|
||SPI3_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI3 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|SPI4|SPI4_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI4 VBUS Clock|
||SPI4_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI4 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1157 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-23.** _**SPI**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|SPI5|SPI5_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI5 VBUS Clock|
||SPI5_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI5 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|SPI6|SPI6_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI6 VBUS Clock|
||SPI6_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI6 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



1158 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-23.** _**SPI**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|SPI7|SPI7_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI7 VBUS Clock|
||SPI7_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI7 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



**Table 13-24.** _**SPI**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|SPI0|SPI0_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|SPI0 Asynchronous Reset|
|SPI1|SPI1_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|SPI1 Asynchronous Reset|
|SPI2|SPI2_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|SPI2 Asynchronous Reset|
|SPI3|SPI3_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|SPI3 Asynchronous Reset|
|SPI4|SPI4_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|SPI4 Asynchronous Reset|
|SPI5|SPI5_RST|Warm Reset<br>(MOD_G_RST)|RCM+ Warm Reset Sources|SPI5 Asynchronous Reset|
|SPI6|SPI6_RST|Warm Reset<br>(MOD_G_RST)|RCM+ Warm Reset Sources|SPI6 Asynchronous Reset|
|SPI7|SPI7_RST|Warm Reset<br>(MOD_G_RST)|RCM+ Warm Reset Sources|SPI7 Asynchronous Reset|



**Table 13-25.** _**SPI**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SPI0|spi0_int_req|spi0_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI0 IP Status Information|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1159 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-25.** _**SPI**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SPI1|spi1_int_req|spi1_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI1 IP Status Information|
|SPI2|spi2_int_req|spi2_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI2 IP Status Information|
|SPI3|spi3_int_req|spi3_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI3 IP Status Information|
|SPI4|spi4_int_req|spi4_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI4 IP Status Information|
|SPI5|spi5_int_req|spi5_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI5 IP Status Information|
|SPI6|spi6_int_req|spi6_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI6 IP Status Information|
|SPI7|spi7_int_req|spi7_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI7 IP Status Information|



**Table 13-26.** _**SPI**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SPI0|SPI0_DMA_READ_0|spi0_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI0 DMA Read Request|
||SPI0_DMA_READ_1|spi0_dma_read_req[1]||||
||SPI0_DMA_READ_2|spi0_dma_read_req[2]||||
||SPI0_DMA_READ_3|spi0_dma_read_req[3]||||
||SPI0_DMA_WRITE_0|spi0_dma_write_req[0]|||SPI0 DMA Write Request|
||SPI0_DMA_WRITE_1|spi0_dma_write_req[1]||||
||SPI0_DMA_WRITE_2|spi0_dma_write_req[2]||||
||SPI0_DMA_WRITE_3|spi0_dma_write_req[3]||||
|SPI1|SPI1_DMA_READ_0|spi1_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI1 DMA Read Request|
||SPI1_DMA_READ_1|spi1_dma_read_req[1]||||
||SPI1_DMA_READ_2|spi1_dma_read_req[2]||||
||SPI1_DMA_READ_3|spi1_dma_read_req[3]||||
||SPI1_DMA_WRITE_0|spi1_dma_write_req[0]|||SPI1 DMA Write Request|
||SPI1_DMA_WRITE_1|spi1_dma_write_req[1]||||
||SPI1_DMA_WRITE_2|spi1_dma_write_req[2]||||
||SPI1_DMA_WRITE_3|spi1_dma_write_req[3]||||
|SPI2|SPI2_DMA_READ_0|spi2_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI2 DMA Read Request|
||SPI2_DMA_READ_1|spi2_dma_read_req[1]||||
||SPI2_DMA_READ_2|spi2_dma_read_req[2]||||
||SPI2_DMA_READ_3|spi2_dma_read_req[3]||||
||SPI2_DMA_WRITE_0|spi2_dma_write_req[0]|||SPI2 DMA Write Request|
||SPI2_DMA_WRITE_1|spi2_dma_write_req[1]||||
||SPI2_DMA_WRITE_2|spi2_dma_write_req[2]||||
||SPI2_DMA_WRITE_3|spi2_dma_write_req[3]||||



1160 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-26.** _**SPI**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SPI3|SPI3_DMA_READ_0|spi3_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI3 DMA Read Request|
||SPI3_DMA_READ_1|spi3_dma_read_req[1]||||
||SPI3_DMA_READ_2|spi3_dma_read_req[2]||||
||SPI3_DMA_READ_3|spi3_dma_read_req[3]||||
||SPI3_DMA_WRITE_0|spi3_dma_write_req[0]|||SPI3 DMA Write Request|
||SPI3_DMA_WRITE_1|spi3_dma_write_req[1]||||
||SPI3_DMA_WRITE_2|spi3_dma_write_req[2]||||
||SPI3_DMA_WRITE_3|spi3_dma_write_req[3]||||
|SPI4|SPI4_DMA_READ_0|spi4_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI4 DMA Read Request|
||SPI4_DMA_READ_1|spi4_dma_read_req[1]||||
||SPI4_DMA_READ_2|spi4_dma_read_req[2]||||
||SPI4_DMA_READ_3|spi4_dma_read_req[3]||||
||SPI4_DMA_WRITE_0|spi4_dma_write_req[0]|||SPI4 DMA Write Request|
||SPI4_DMA_WRITE_1|spi4_dma_write_req[1]||||
||SPI4_DMA_WRITE_2|spi4_dma_write_req[2]||||
||SPI4_DMA_WRITE_3|spi4_dma_write_req[3]||||
|SPI5|SPI5_DMA_READ_0|spi5_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI5 DMA Read Request|
||SPI5_DMA_READ_1|spi5_dma_read_req[1]||||
||SPI5_DMA_READ_2|spi5_dma_read_req[2]||||
||SPI5_DMA_READ_3|spi5_dma_read_req[3]||||
||SPI5_DMA_WRITE_0|spi5_dma_write_req[0]|||SPI5 DMA Write Request|
||SPI5_DMA_WRITE_1|spi5_dma_write_req[1]||||
||SPI5_DMA_WRITE_2|spi5_dma_write_req[2]||||
||SPI5_DMA_WRITE_3|spi5_dma_write_req[3]||||
|SPI6|SPI6_DMA_READ_0|spi6_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI6 DMA Read Request|
||SPI6_DMA_READ_1|spi6_dma_read_req[1]||||
||SPI6_DMA_READ_2|spi6_dma_read_req[2]||||
||SPI6_DMA_READ_3|spi6_dma_read_req[3]||||
||SPI6_DMA_WRITE_0|spi6_dma_write_req[0]|||SPI6 DMA Write Request|
||SPI6_DMA_WRITE_1|spi6_dma_write_req[1]||||
||SPI6_DMA_WRITE_2|spi6_dma_write_req[2]||||
||SPI6_DMA_WRITE_3|spi6_dma_write_req[3]||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1161 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-26.** _**SPI**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SPI7|SPI7_DMA_READ_0|spi7_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI7 DMA Read Request|
||SPI7_DMA_READ_1|spi7_dma_read_req[1]||||
||SPI7_DMA_READ_2|spi7_dma_read_req[2]||||
||SPI7_DMA_READ_3|spi7_dma_read_req[3]||||
||SPI7_DMA_WRITE_0|spi7_dma_write_req[0]|||SPI7 DMA Write Request|
||SPI7_DMA_WRITE_1|spi7_dma_write_req[1]||||
||SPI7_DMA_WRITE_2|spi7_dma_write_req[2]||||
||SPI7_DMA_WRITE_3|spi7_dma_write_req[3]||||



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

1162 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.1.3.4 MCSPI Functional Description** _**13.1.3.4.1 SPI Block Diagram**_ 

Figure 13-28 shows the SPI module. 

**==> picture [366 x 387] intentionally omitted <==**

**Note** 

For single channel operation (i=0 or i=1), MCSPI_CHiCON[20]FORCE is asserted over the SPIENIi and SPIENOi lines. 

**Figure 13-28. SPI Block Diagram** 

## _**13.1.3.4.2 MCSPI Reset**_ 

The MCSPI module can be reset either by hardware or by software reset. All configuration registers and all state machines are reset by the hardware reset signal (MCSPI_RST). MCSPI can be reset by software through the MCSPI_SYSCONFIG[1] SOFTRESET bit. This bit has the same impact on the module as the hardware reset signal. The only exception is that the MCSPI_SYSCONFIG register is not affected by that software reset. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1163 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.3.4.3 MCSPI Controller Mode**_ 

## _**13.1.3.4.3.1 Controller Mode Features**_ 

The MCSPI controller mode supports multichannel communication with up to four independent MCSPI communication channel contexts. The MCSPI initiates a data transfer on the data lines (SPIDAT[0] and SPIDAT[1]) and generates clock (SPICLK) and control (SPIEN[i]) signals. 

Connected to multiple external devices, the MCSPI exchanges data with one MCSPI device at a time through two main modes (available in peripheral mode): 

- Two-data-pins interface mode (transmit-and-receive mode for full-duplex transmission) 

- Single-data-pin interface mode (recommended for half-duplex transmission) 

## **Note** 

There is a fixed chip select line allocation in multichannel controller mode. Channel i is mapped to SPIEN[i]. 

Two DMA request events (read and write) allow synchronized accesses of the DMA controller with the activity of MCSPI. 

Three interrupt events can be used for data transmission and reception in controller mode (for more information about interrupts, see Section 13.1.3.4.7.1, _Interrupt Events in Controller Mode_ ). 

## _**13.1.3.4.3.2 Controller Transmit-and-Receive Mode (Full Duplex)**_ 

In full-duplex transmission, data is transmitted (shifted out serially on SPIDAT[0]) and received (shifted in serially on SPIDAT[1]) simultaneously on separate data lines. 

The controller transmit-and-receive mode is programmable per channel (the MCSPI_CHCONF_0/1/2/3[13-12] TRM bit field). 

Channel access to the shift registers for transmission/reception is based on the MCSPI_TX_0/1/2/3 transmitter register state, the MCSPI_RX_0/1/2/3 receiver register state, and round-robin arbitration. 

Channels that meet the following rules are included in the round-robin list of active channels scheduled for transmission and/or reception. The arbiter skips channels that do not meet the rules and searches in the rotation for the next enabled channel. 

- Rule 1: Only enabled channels (the MCSPI_CHCTRL_0/1/2/3[0] EN bit) can be scheduled for transmission and/or reception. 

- Rule 2: If its MCSPI_TX_0/1/2/3 transmitter register is not empty (the MCSPI_CHSTAT_0/1/2/3[1] TXS bit), an enabled channel can be scheduled when the shift register is assigned. If the MCSPI_TX_0/1/2/3 register is empty when the shift register is assigned, the TXx_UNDERFLOW event is activated, and the next enabled channel with new data to transmit is scheduled (see also transmit-only mode). 

- Rule 3: An enabled channel can be scheduled if its receive register is not full (the MCSPI_CHSTAT_0/1/2/3[0] RXS bit) when the shift register is assigned (see also receive-only mode). Therefore, the MCSPI_RX_0/1/2/3 register cannot be overwritten. The MCSPI_IRQSTATUS[3] RX0_OVERFLOW bit is never set to this mode. 

When MCSPI word transfer completes (the MCSPI_CHSTAT_0/1/2/3[2] EOT bit is set), the updated MCSPI_TX_0/1/2/3 register of the next scheduled channel is loaded into the shift register. The serialization (transmit-and-receive) starts depending on the channel communication configuration. When serialization completes, the received data transfers to the channel receive register. 

The serial clock (SPICLK) synchronizes shifting and sampling of the information on the two serial data lines (SPIDAT[0] and SPIDAT[1]). Each time a bit transfers out from the controller, 1 bit transfers in from the peripheral. 

Figure 13-29 shows an example of a full-duplex system with a controller device on the left and a peripheral device on the right. After eight cycles of the serial clock SPICLK, WordA transfers from the controller to the peripheral. At the same time, WordB transfers from the peripheral to the controller. 

1164 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [435 x 226] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transmitter buffer Transmitter buffer<br>SPIDAT[0]<br>SPIDAT[1]<br>Shift register Shift register<br>SPICLK<br>Controller Control Control Peripheral<br>SPIEN[i]<br>Receiver register Receiver register<br>Controller SPI shift register Peripheral SPI shift register<br>Initial WordA Initial WordB<br>After 8 SPICLK After 8 SPICLK<br>clock cycles WordB clock cycles WordA<br>spi-013<br>**----- End of picture text -----**<br>


**Figure 13-29. MCSPI Full-Duplex Transmission (Example)** 

## _**13.1.3.4.3.3 Controller Transmit-Only Mode (Half Duplex)**_ 

The controller transmit-only mode prevents the processor from reading the MCSPI_RX_0/1/2/3 register (minimizing data movement) when only transmission is meaningful. 

The controller transmit-only mode is programmable per channel (the MCSPI_CHCONF_0/1/2/3[13-12] TRM bit field). Transmission starts only after data is loaded into the MCSPI_TX_0/1/2/3 register. 

Rule 1 and Rule 2, defined in Section 13.1.3.4.3.2, apply in this mode. 

Rule 3, defined in Section 13.1.3.4.3.2, does not apply. 

In controller transmit-only mode, the MCSPI_RX_0/1/2/3 register state FULL does not prevent transmission and the MCSPI_RX_0/1/2/3 register is always overwritten with the new MCSPI word. This event is not significant when only transmission is meaningful. Thus, the RX0_OVERFLOW bit in the MCSPI_IRQSTATUS register is never set in this mode. 

The hardware automatically disables the RX_FULL interrupt and the DMA read requests. 

The transfer status is given by the MCSPI_CHSTAT_0/1/2/3[2] EOT bit. 

## _**13.1.3.4.3.4 Controller Receive-Only Mode (Half Duplex)**_ 

The controller receive mode prevents the processor from refilling the MCSPI_TX_0/1/2/3 register (minimizing data movement) when only reception is meaningful. 

The controller receive mode is programmable per channel (the MCSPI_CHCONF_0/1/2/3[13-12] TRM bit field). 

The controller receive-only mode enables channel scheduling only on the empty state of the MCSPI_RX_0/1/2/3 register. 

Rule 1 and Rule 3, defined in Section 13.1.3.4.3.2, apply in this mode. 

Rule 2, defined in Section 13.1.3.4.3.2, does not apply. 

In the controller receive-only mode, software must write dummy data to the MCSPI_TX_0/1/2/3 register. Only one dummy write is enough to receive any number of words from the peripheral. Software must ensure that the MCSPI_TX_0/1/2/3 register is always full (the TXx_EMPTY bits of MCSPI_IRQSTATUS) when receiving. The content of the MCSPI_TX_0/1/2/3 register is always loaded into the shift register when the shift 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1165 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

register is assigned. After writing the dummy data to the MCSPI_TX_0/1/2/3 register, the TXx_EMPTY and TXx_UNDERFLOW bits in the MCSPI_IRQSTATUS register are never set in receive-only mode. 

The MCSPI_CHSTAT_0/1/2/3[2] EOT bit gives the status of serialization. The RXx_FULL bits of the MCSPI_IRQSTATUS register are set when received data is loaded from the shift register to the corresponding MCSPI_RX_0/1/2/3 register. The MCSPI_IRQSTATUS[3] RX0_OVERFLOW bit is never set in this mode. 

## _**13.1.3.4.3.5 Single-Channel Controller Mode**_ 

When the MCSPI is configured as a controller device with a single enabled channel (MCSPI_MODULCTRL[2] MS = 0 and MCSPI_MODULCTRL[0] SINGLE = 1), the assertion of the SPIEN[i] signal is optional depending on device connected to the controller. In 3-pin mode (MCSPI_MODULCTRL[1] PIN34 = 1) the controller starts transmitting data when a write to the MCSPI_TX_0/1/2/3 register or the FIFO is performed. In 4-pin mode (MCSPI_MODULCTRL[1] PIN34 = 0) the assertion and de-assertion of SPIEN[i] is controlled by software using the MCSPI_CHCONF_0/1/2/3[20] FORCE bit. 

## _**13.1.3.4.3.5.1 Programming Tips When Switching to Another Channel**_ 

When a single channel is enabled and data transfer is ongoing: 

- Wait for the MCSPI word transfer to complete (wait until the MCSPI_CHSTAT_0/1/2/3[2] EOT bit is set to 1) before disabling the current channel and enabling a different channel. 

- Disable the current channel, and then enable the other channel. 

## _**13.1.3.4.3.5.2 Force SPIEN[i] Mode**_ 

Continuous transfers are allowed manually by keeping the SPIEN[i] signal active for successive MCSPI words transfer. Several sequences (configuration/enable/disable of the channel) can be run without deactivating the SPIEN[i] line. This mode is supported by all channels and any controller sequence can be used (transmitreceive, transmit-only, receive-only). 

Keeping the SPIEN[i] active mode is supported when: 

- A single channel is used (with the MCSPI_MODULCTRL[0] SINGLE bit set to 1). 

- Transfer parameters are loaded in the configuration register of the appropriate channel (MCSPI_CHCONF_0/1/2/3). 

The state of the SPIEN[i] signal is programmable: 

   - Writing 1 to the MCSPI_CHCONF_0/1/2/3[20] FORCE bit drives the SPIEN[i] line high when the MCSPI_CHCONF_0/1/2/3[6] EPOL bit is set to 0. SPIEN[i] is driven low when the MCSPI_CHCONF_0/1/2/3[6] EPOL bit is set to 1. 

   - Writing 0 to the MCSPI_CHCONF_0/1/2/3[20] FORCE bit drives the SPIEN[i] line low when the MCSPI_CHCONF_0/1/2/3[6] EPOL bit is set to 0. SPIEN[i] is driven high when the MCSPI_CHCONF_0/1/2/3[6] EPOL bit is set to 1. 

- A single channel is enabled (the MCSPI_CHCTRL_0/1/2/3[0] EN bit is set to 1). The first enabled channel activates the SPIEN[i] line. 

When the channel is enabled, the SPIEN[i] signal activates with the programmed polarity. As in the multichannel controller mode, the transfer start depends on the status of the MCSPI_TX_0/1/2/3 register (the MCSPI_CHSTAT_0/1/2/3[1] TXS bit), the status of the MCSPI_RX_0/1/2/3 register (the MCSPI_CHSTAT_0/1/2/3[1] RXS bit), and the defined mode (the MCSPI_CHCONF_0/1/2/3[13-12] TRM bit field) of the channel enabled. 

The MCSPI_CHSTAT_0/1/2/3[2] EOT bit gives the transfer status of each MCSPI word. The RXx_FULL bit in the MCSPI_IRQSTATUS register is set when received data is loaded from the shift register to the MCSPI_RX_0/1/2/3 register. 

A change in the configuration parameters is propagated directly on the MCSPI interface. If the SPIEN[i] signal is activated, ensure that the configuration is changed only between MCSPI words to avoid corrupting the current transfer. 

1166 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

To avoid data corruption, SPIEN[i] polarity and SPICLK phase and SPICLK polarity must not be modified when the SPIEN[i] signal is activated. 

A delay between MCSPI words that requires the connected MCSPI peripheral device to switch from one configuration to another (for instance, from transmit-only to receive-only) must be handled by software. 

At the end of the last MCSPI word, the channel must be deactivated (the MCSPI_CHCTRL_0/1/2/3[0] EN bit set to 0) and SPIEN[i] can be forced to its INACTIVE state using the MCSPI_CHCONF_0/1/2/3[20] FORCE bit. 

Figure 13-30 and Figure 13-31 show successive transfers with SPIEN[i] maintained active low with a different configuration for each MCSPI word in single-data-pin and dual-data-pin interface modes, respectively. 

**==> picture [363 x 97] intentionally omitted <==**

**----- Start of picture text -----**<br>
SPIEN[i]<br>SPIDAT[0] Word Word Word<br>SPICLK<br>**----- End of picture text -----**<br>


spi-014 

**Figure 13-30. Continuous Transfers With SPIEN[i] Maintained Active (Single-Data-Pin Interface Mode)** 

**==> picture [362 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
SPIEN[i]<br>SPIDAT[0] Word Word<br>SPIDAT[1] Word<br>SPICLK<br>**----- End of picture text -----**<br>


**==> picture [18 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
spi-015<br>**----- End of picture text -----**<br>


**Figure 13-31. Continuous Transfers With SPIEN[i] Maintained Active (Dual-Data-Pin Interface Mode)** 

## **Note** 

The SPIEN[i] signal can be maintained active via software using the MCSPI_CHCONF_0/1/2/3[20] FORCE bit only when the MCSPI_MODULCTRL[0] SINGLE bit is set to 0x1. 

## _**13.1.3.4.3.5.3 Turbo Mode**_ 

Turbo mode improves the throughput of the MCSPI interface when a single channel is enabled by allowing transfers until the shift register and the MCSPI_RX_0/1/2/3 register are full. Turbo mode is time saving when a transfer exceeds two words. This mode is programmable per channel (through the MCSPI_CHCONF_0/1/2/3[9] TURBO bit). 

When several channels are enabled, the TURBO bit has no effect and the channel access to the shift registers remains as previously described. 

In turbo mode, Rule 1 and Rule 2 apply, but Rule 3 does not (see Section 13.1.3.4.3.2, _Controller Transmitand-Receive Mode (Full Duplex)_ ). An enabled channel can be scheduled if its receive register is full (the MCSPI_CHSTAT_0/1/2/3[0] RXS bit) when the shift-register is assigned until the shift register is full. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1167 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

The MCSPI_RX_0/1/2/3 register cannot be overwritten in turbo mode. Consequently, the MCSPI_IRQSTATUS[3] RX0_OVERFLOW bit is never set in this mode. 

## _**13.1.3.4.3.6 Start-Bit Mode**_ 

In start-bit mode, an extended bit is added before the MCSPI word to indicate whether the next MCSPI word must be handled as a command or as data. This feature is available only in controller mode. Start-bit mode cannot be used at the same time as turbo mode and/or force SPIEN[i] mode. In this case, only one channel can be used; round-robin arbitration is not possible. 

This mode is programmable per channel by setting the MCSPI_CHCONF_0/1/2/3[23] SBE bit to 1. The polarity of the extended bit is programmable per channel. When the MCSPI_CHCONF_0/1/2/3[24] SBPOL bit is set to 0, the MCSPI word must be handled as a command. When the MCSPI_CHCONF_0/1/2/3[24] SBPOL bit is set to 1, the MCSPI word must be handled as data. Moreover, start-bit polarity can be changed dynamically during start-bit transfer without disabling the channel for reconfiguration; in this case, users must configure the MCSPI_CHCONF_0/1/2/3[24] SBPOL bit before writing the MCSPI word to be transmitted to the TX register. 

## _**13.1.3.4.3.7 Chip-Select Timing Control**_ 

The chip-select (CS) timing control is available only in controller mode with automatic CS generation (the MCSPI_MODULCTRL[0] SINGLE bit set to 0) to add a programmable delay between CS assertion and first clock edge, or CS removal and last clock edge. This option is available only in 4-pin mode when MCSPI_MODULCTRL[1] PIN34 set to 0. 

This mode is programmable per channel through the MCSPI_CHCONF_0/1/2/3[26-25] TCS0 bit field. 

Figure 13-32 shows the CS SPIEN timing controls. 

**==> picture [500 x 196] intentionally omitted <==**

**----- Start of picture text -----**<br>
SPI shift clock<br>(SPICLKREF)<br>SPICLK (POL = 0)<br>SPICLK (POL = 1)<br>peripheral select<br>(SPIEN[i])<br>TCS = 0.5 TCS = 0.5<br>TCS = 1.5 TCS = 1.5<br>TCS = 2.5 TCS = 2.5<br>TCS = 3.5 TCS = 3.5<br>spi-016<br>**----- End of picture text -----**<br>


**Figure 13-32. CS SPIEN Timing Controls** 

## **Note** 

Because of the design implementation for transfers using a clock divider ratio set to 1 (clock bypassed), a half cycle must be added to the value between CS assertion and the first clock edge with PHA = 1 or between CS removal and the last clock edge with PHA = 0. 

## _**13.1.3.4.3.8 Programmable MCSPI Clock (SPICLK)**_ 

In controller mode, the baud rate of the MCSPI serial clock is programmable. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1168 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

An internal reference clock, SPICLKREF, is used as input of a programmable divider (the MCSPI_CHCONF_0/1/2/3[5-2] CLKD bit field) to generate the bit rate of the serial output clock SPICLK. Table 13-27 summarizes the supported divisor values. 

**Table 13-27. MCSPI Controller Clock Rates** 

||**Divider**|**Clock Rate**|
|---|---|---|
||1|50 MHz(1)|
||2|25 MHz(1)|
||4|12.5 MHz|
||8|6.25 MHz|
||16|3.125 MHz|
||32|1.5625 MHz|
||64|781.25 kHz|
||128|390 kHz(2)|
||256|195 kHz(2)|
||512|97.7 kHz(2)|
||1024|48.8 kHz(2)|
||2048|24.4 kHz(2)|
||4096|12.2 kHz(2)|
|8192|and higher: Division not supported|–|



(1) These frequencies are not necessarily supported by all MCSPI modules. For more information, see the _Timing Requirements and Switching Characteristics_ chapter in the device-specific Data sheet. (2) Approximate Frequency 

## _**13.1.3.4.3.8.1 Clock Ratio Granularity**_ 

By default, the clock division ratio is defined by the MCSPI_CHCONF_0/1/2/3[5-2] CLKD bit field with powerof-2 granularity leading to a clock division in the range 1 to 4096; in this case, the duty cycle is always 50 percent. With the MCSPI_CHCONF_0/1/2/3[29] CLKG bit, clock division granularity can be changed to one clock cycle; in that case the MCSPI_CHCTRL_0/1/2/3[15-8] EXTCLK bit field is concatenated with the MCSPI_CHCONF_0/1/2/3[5-2] CLKD bit field to give a 12-bit-wide division ratio in the range 1 to 4096. 

When granularity is one clock cycle (the CLKG bit set to 1), for the odd value of the clock ratio, the clock high level lasts one clock cycle more than the low level, depending on the MCSPI_CHCONF_0/1/2/3[1] POL and MCSPI_CHCONF_0/1/2/3[0] PHA bits (see Table 13-28). 

**Table 13-28. CLKSPIO High/Low Time Computation** 

|**Clock Ratio FRATIO**|**CLKSPIO High Time**|**CLKSPIO Low Time**|
|---|---|---|
|1|THIGH_REF|TLOW_REF|
|Even >= 2|T_ref * (FRATIO/2)|T_ref * (FRATIO/2)|
|Odd >= (POL = PHA)|T_ref * (FRATIO– 1)/2|T_ref * (FRATIO+ 1)/2|
|Odd >= (POL =! PHA)|T_ref * (FRATIO+ 1)/2|T_ref * (FRATIO– 1)/2|



## **Note** 

FRATIO = SPICLK frequency (FOUT) division ratio THIGH = SPICLK high time period 

TLOW = SPICLK low time period T_ref = MCSPI_FCLK period THIGH_REF = MCSPI_FCLK high time period 

TLOW_REF = MCSPI_FCLK low time period 

If the CLKG bit is set to 1; FRATIO = EXTCLK concatenated with CLKD + 1. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1169 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

For odd ratio values, the duty cycle is calculated as follows: 

Duty_cycle = (1 – 1/FRATIO)/2 

Table 13-29 shows examples of clock granularity with a clock source frequency of 50 MHz. 

**Table 13-29. Clock Granularity Examples** 

|**EXTCLK**|**CLKD**|**CLKG**|**FRATIO**|**PHA**|**POL**|**THIGH (ns)**|**TLOW (ns)**|**TPERIOD**|**Duty**|**FOUT**|
|---|---|---|---|---|---|---|---|---|---|---|
|||||||||**(ns)**|**Cycle**|**(MHz)**|
|X|0|0|1|X|X|10.0|10.0|20.0|50–50|50|
|X|1|0|2|X|X|20.0|20.0|40.0|50–50|25|
|X|2|0|4|X|X|40.0|40.0|80.0|50–50|12.5|
|X|3|0|8|X|X|80.0|80.0|160.0|50–50|6.2|
|0|0|1|1|X|X|10.0|10.0|20.0|50–50|50|
|0|1|1|2|X|X|20.0|20.0|40.0|50–50|25|
|0|2|1|3|1|0|40.0|20.0|60.0|66–33|16.6|
|0|2|1|3|1|1|20.0|40.0|60.0|33–66|16.6|
|0|3|1|4|X|X|40.0|40.0|80.0|50–50|12.5|
|5|0|1|81|1|0|820.0|800.0|1620.0|50.6–49.4|0.617|
|5|7|1|88|X|X|880.0|880.0|1760.0|50–50|0.568|



## _**13.1.3.4.4 MCSPI Peripheral Mode**_ 

To select the MCSPI peripheral mode, set the MCSPI_MODULCTRL[2] MS bit. 

A MCSPI peripheral device can be connected to up to four external MCSPI controller devices but handles transactions with one MCSPI controller device at a time. 

In peripheral mode, the MCSPI initiates data transfer on the data lines (SPIDAT[0] and SPIDAT[1]) when it is selected by an active control signal (SPIEN[i]) and receives an MCSPI clock (SPICLK) from the external MCSPI controller device. Only channel 0 can be configured as a peripheral but through the MCSPI_CHCONF_0[22-21] SPIENSLV bit field any of the SPIEN[i] signals can be used to select the MCSPI module. In peripheral mode and when the MCSPI_MODULCTRL[1] PIN34 is set to 0x0 (default behaviour), the MCSPI uses the edge of SPIEN[i] to detect word length. For this reason, SPIEN[i] must become inactive between each word. 

When the MCSPI_MODULCTRL[1] PIN34 is set to 0x0, the MCSPI does not support SPIEN[i] active between MCSPI words. In this case, the MCSPI uses the edge to detect word length. 

When the MCSPI_MODULCTRL[1] PIN34 is set to 0x1, a multiword transfer can be performed without needing the external MCSPI controller to deactivate SPIEN[i] between each word as in this case the MCSPI module works in 3-pin peripheral mode and SPIEN[i] is not needed. 

## _**13.1.3.4.4.1 Dedicated Resources**_ 

Only channel 0 can be enabled in peripheral mode. 

Figure 13-33 shows an example of four peripherals wired on a single controller device. 

1170 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [384 x 401] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>SPI_CLK<br>(1)<br>SPI_D0<br>MCSPI<br>module SPI_D1(1)<br>in peripheral<br>mode SPI_CS0<br>Generic Generic<br>SCLK SCLK<br>SPI peripheral SPI controller<br>device device<br>SIMO SIMO<br>SOMI SOMI<br>CS CS0<br>CS1<br>CS2<br>Generic<br>SCLK<br>SPI peripheral CS3<br>device<br>SIMO<br>SOMI<br>CS<br>Generic<br>SCLK<br>SPI peripheral<br>device<br>SIMO<br>SOMI<br>CS<br>**----- End of picture text -----**<br>


spi-017 

- A. Direction depends on MCSPI_CHCONF_0/1/2/3[16] DPE0, MCSPI_CHCONF_0/1/2/3[17] DPE1 and MCSPI_CHCONF_0/1/2/3[18] IS bits 

## **Figure 13-33. Example of MCSPI Peripheral With One Controller and Multiple Peripheral Devices on Channel 0** 

Channel 0 in peripheral mode has the following resources: 

- Its own channel enable, programmable with the MCSPI_CHCTRL_0[0] EN bit. This channel must be enabled before transmission and reception. 

- For this mode, the peripheral-select signal can be detected on any of the SPIEN[i] ports. This is programmable with the MCSPI_CHCONF_0[22-21] SPIENSLV bit field. 

- Its own transmitter register, MCSPI_TX_0, on top of the common transmit shift register. If the MCSPI_TX_0 register is empty, the MCSPI_CHSTAT_0[1] TXS bit is set. If MCSPI is selected by an external controller (the active signal on the SPIEN[i] port assigned to channel 0), the MCSPI_TX_0 register content of channel 0 is always loaded into the shift register, whether its content is updated or not. The MCSPI_TX_0 register must be loaded before MCSPI is selected by a controller. 

- Its own receiver register, MCSPI_RX_0, on top of the common receive shift register. If the MCSPI_RX_0 register is full, the MCSPI_CHSTAT_0[0] RXS bit is set. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1171 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Note** 

The MCSPI_TX_1/2/3 and MCSPI_RX_1/2/3 registers are not used. Reading from or writing to a channel register other than channel 0 has no effect. 

- Its own communication configuration with the following parameters through the MCSPI_CHCONF_0: 

   - Transmit and receive modes, programmable with the TRM field 

   - Interface mode (two data pins or single data pin) and data pins assignment, both programmable with the IS and DPE bits. (The MCSPI modules are in peripheral mode after reset and must be properly configured for the modules to act in controller mode.) 

   - MCSPI word length, programmable with the WL bit 

   - SPIEN[i] polarity, programmable with the EPOL bit 

   - SPICLK polarity, programmable with the POL bit 

   - 

- SPICLK phase, programmable with the PHA bit 

The SPICLK frequency of a transfer is controlled by the external MCSPI controller connected to the MCSPI peripheral device. The MCSPI_CHCONF_0[5-2] CLKD bit field is not used in peripheral mode. 

## **Note** 

The configuration of the channel can be loaded in the MCSPI_CHCONF_0 only when the channel is disabled. 

- Two DMA request events, read and write, synchronize read/write accesses of the DMA controller with the activity of MCSPI. DMA requests are asserted using the MCSPI_CHCONF_0[15] DMAR bit for reading and the MCSPI_CHCONF_0[14] DMAW bit for writing. 

- Four interrupt events (see Section 13.1.3.4.7.2, _Interrupt Events in Peripheral Mode_ ). 

## _**13.1.3.4.4.2 Peripheral Transmit-and-Receive Mode**_ 

The peripheral receive mode is programmable (set the MCSPI_CHCONF_0[13-12] TRM bit field to 0x0). 

In peripheral transmit-and-receive mode, the MCSPI_TX_0 register must be loaded before MCSPI is selected by an external MCSPI controller device. 

After a channel is enabled, transmission and reception proceed with interrupt and DMA request events. 

The MCSPI_TX_0 register content is always loaded in the shift register whether it is updated or not. The event TX0_UNDERFLOW is activated accordingly and does not prevent transmission. 

When the MCSPI word transfer completes (the MCSPI_CHSTAT_0[2] EOT bit is set to 1), the received data is transferred to the channel receive register. 

To use MCSPI as a peripheral transmit-only device, the RX0_FULL and RX0_OVERFLOW interrupts and DMA read requests must be disabled due to the state of the MCSPI_RX_0 register (see Section 13.1.3.4.7.2, _Interrupt Events in Peripheral Mode_ ). 

## _**13.1.3.4.4.3 Peripheral Transmit-Only Mode**_ 

The peripheral transmit-only mode is programmable (set the MCSPI_CHCONF_0[13-12] TRM bit field to 0x2) and avoids the requirement for the processor to read the MCSPI_RX_0 register (minimizing data movement) only when transmission is meaningful. 

To use the MCSPI as a peripheral transmit-only device, the RX0_FULL and RX0_OVERFLOW interrupts and DMA read requests must be disabled due to the state of the MCSPI_RX_0 register. 

When the MCSPI word transfer completes, the MCSPI_CHSTAT_0[2] EOT bit is set. 

Figure 13-34 shows a half-duplex system with a controller device on the left and a transmit-only peripheral device on the right. Each time a bit transfers out from the peripheral, 1 bit transfers in the controller. After eight cycles of the serial clock SPICLK, WordB transfers from the peripheral to the controller. 

1172 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [411 x 223] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transmitter buffer Transmitter buffer<br>SPIDATk<br>(single line)<br>Shift register Shift register<br>SPICLK<br>Controller Control Control<br>SPIEN[i] Peripheral<br>(transmit only)<br>Receiver register<br>Controller SPI shift register Peripheral SPI shift register<br>Initial WordA Initial WordB<br>After 8 After 8<br>SPICLK WordB SPICLK WordC<br>clock cycles clock cycles<br>**----- End of picture text -----**<br>


spi-018 

k = 0 or 1 depending on MCSPI_CHCONF_0/1/2/3[16] DPE0, MCSPI_CHCONF_0/1/2/3[17] DPE1 and MCSPI_CHCONF_0/1/2/3[18] IS bits 

## **Figure 13-34. MCSPI Half-Duplex Transmission (Transmit-Only peripheral)** 

## _**13.1.3.4.4.4 Peripheral Receive-Only Mode**_ 

The peripheral receive mode is programmable (set the MCSPI_CHCONF_0[13-12] TRM bit field to 0x1). 

In receive-only mode, the MCSPI_TX_0 register must be loaded before the MCSPI is selected by an external MCSPI controller device. The MCSPI_TX_0 register content is always loaded into the shift register whether it is updated or not. The TX0_UNDERFLOW event is activated accordingly and does not prevent transmission. 

When the MCSPI word transfer completes (the MCSPI_CHSTAT_0[2] EOT bit is set to 1), the received data is transferred to the channel receive register. 

To use the MCSPI as a peripheral receive-only device, the TX0_EMPTY and TX0_UNDERFLOW interrupts and the DMA write requests must be disabled due to the state of the MCSPI_TX_0 register. 

For a full-duplex transmission, the serial clock (SPICLK) synchronizes shifting and sampling of the information on the two serial data lines. If SPICLK synchronizes on a single serial data line, the data line should be half-duplex. 

Figure 13-35 shows a half-duplex system with a controller device on the left and a receive-only peripheral device on the right. Each time a bit transfers out from the controller, 1 bit transfers in from the peripheral. After eight cycles of the serial clock SPICLK, WordA transfers from the controller to the peripheral. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1173 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [412 x 223] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transmitter buffer<br>SPIDATk<br>(single)<br>Shift register Shift register<br>SPICLK<br>Peripheral<br>Controller Control SPIEN[i] Control<br>(receive only)<br>Receiver register Receiver register<br>Controller SPI shift register Peripheral SPI shift register<br>Initial WordA Initial WordB<br>After 8 After 8<br>SPICLK WordC SPICLK WordA<br>clock cycles clock cycles<br>**----- End of picture text -----**<br>


spi-019 

k = 0 or 1 depending on MCSPI_CHCONF_0/1/2/3[16] DPE0, MCSPI_CHCONF_0/1/2/3[17] DPE1 and MCSPI_CHCONF_0/1/2/3[18] IS bits 

## **Figure 13-35. MCSPI Half-Duplex Transmission (Receive-Only Peripheral)** 

## _**13.1.3.4.5 MCSPI 3-Pin or 4-Pin Mode**_ 

Depending on targeted application the MCSPI interface can be configured to use 3 or 4 pins through the MCSPI_MODULCTRL[1] PIN34 bit. If this bit is set to 0, MCSPI is in 4-pin mode using the SPICLK, SPIDAT[0], SPIDAT[1] and SPIEN[i] signals. If PIN34 is set to 1 the controller is in 3-pin mode and SPIEN[i] is not used. In this mode all options related to chip select management are useless (EPOL, FORCE and TCS0 bits of MCSPI_CHCONF_0/1/2/3). 3-pin and 4-pin operation applies to both controller and peripheral modes. 

## _**13.1.3.4.6 MCSPI FIFO Buffer Management**_ 

The MCSPI controller has a built-in 64-byte buffer to unload the DMA or interrupt handler and improve data throughput. 

This buffer can be used by only one channel at a time and is selected by setting the MCSPI_CHCONF_0/1/2/3[28] FFER or MCSPI_CHCONF_0/1/2/3[27] FFEW bit to 1. If several channels are selected and several FIFO enable bit fields are set to 1, the controller forces the buffer not to be used; the driver must set only one FIFO enable bit field. 

The buffer can be used in the following modes: 

- Controller or peripheral mode 

- Transmit-only, receive-only, or transmit-and-receive mode 

- Single channel or turbo mode, or normal round-robin mode. In round-robin mode the buffer is used by only one channel. 

Every word length (MCSPI_CHCONF_0/1/2/3[11-7] WL) is supported. 

In transmit-and-receive mode, the buffer can be used in transmit (see Figure 13-36) or receive (see Figure 13-37) directions, or in both directions. If only one direction is chosen in transmit-and-receive mode, the full buffer is used for this direction. In both directions, the buffer is split into two halves, one for each direction (see Figure 13-38). 

1174 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [333 x 142] intentionally omitted <==**

**----- Start of picture text -----**<br>
FIFO SPIDATI<br>TXx register<br>Shift register SPIDATO<br>Depth<br>=<br>64 bytes<br>RXx register RX buffer<br>spi-020<br>**----- End of picture text -----**<br>


**Figure 13-36. Buffer Used in Transmit Direction Only** 

**==> picture [332 x 139] intentionally omitted <==**

**----- Start of picture text -----**<br>
FIFO SPIDATI<br>TXx register<br>Shift register SPIDATO<br>Depth<br>=<br>64 bytes<br>RXx register RX buffer<br>**----- End of picture text -----**<br>


**==> picture [17 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
spi-021<br>**----- End of picture text -----**<br>


**Figure 13-37. Buffer Used in Receive Direction Only** 

**==> picture [332 x 142] intentionally omitted <==**

**----- Start of picture text -----**<br>
FIFO SPIDATI<br>Depth<br>TXx register =<br>32 bytes Shift register SPIDATO<br>Depth<br>RXx register = RX buffer<br>32 bytes<br>spi-022<br>**----- End of picture text -----**<br>


**Figure 13-38. Buffer Used for Transmit and Receive Directions** 

Two levels (MCSPI_XFERLEVEL[5-0] AEL and MCSPI_XFERLEVEL[13-8] AFL) rule the buffer management. The granularity of these levels is 1 byte; it is not aligned with the MCSPI word length. The driver must set these values as a multiple of the MCSPI word length defined in WL. Table 13-30 lists the number of bytes written in the FIFO, depending on the word length. 

**Table 13-30. FIFO Writes, Word Length Relationship** 

|||**MCSPI Word Length (WL)**|**MCSPI Word Length (WL)**|
|---|---|---|---|
||**3 ≤ WL≤ 7**|**8 ≤ WL ≤ 15**|**16 ≤ WL ≤ 31**|
|Number of bytes written|1 byte|2 bytes|4 bytes|
|in the FIFO||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1175 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

The FIFO buffer pointers are reset when the corresponding channel is enabled or the FIFO configuration changes. 

## _**13.1.3.4.6.1 Buffer Almost Full**_ 

The MCSPI_XFERLEVEL[15-8] AFL bit field is needed when the buffer is used to receive an MCSPI word from a peripheral (the MCSPI_CHCONF_0/1/2/3[28] FFER bit must be set to 1). It defines the almost-full buffer status. See Figure 13-39. 

When the FIFO pointer reaches this level, an interrupt or a DMA request is sent to the processor to enable the system to read AFL + 1 bytes from the receive register. 

## **Note** 

AFL + 1 must correspond to a multiple value of the MCSPI_CHCONF_0/1/2/3[11-7] WL bit field. 

When DMA is used, the request is de-asserted after the first receive register read. 

No new request is asserted again as long as the system has not performed the correct number of read accesses. 

**==> picture [384 x 151] intentionally omitted <==**

**----- Start of picture text -----**<br>
full FIFO size<br>MCSPI_XFERLEVEL<br>[13-8] AFL (bytes)<br>empty 0<br>MCSPI_IRQSTATUS<br>RXx_FULL bit<br>RX0_OVERFLOW bit<br>(peripheral mode) spi-023<br>Next peripheral MCSPI<br>reception<br>CPU read<br>MCSPI reception<br>**----- End of picture text -----**<br>


**Figure 13-39. Buffer Almost Full Level (AFL)** 

## **Note** 

The MCSPI_IRQSTATUS register bits are not available in DMA mode. In DMA mode, the SPI_DMA_READ_i request is asserted on the same conditions as the MCSPI_IRQSTATUS RXx_FULL flag. 

## _**13.1.3.4.6.2 Buffer Almost Empty**_ 

The MCSPI_XFERLEVEL[7-0] AEL bit field is needed when the buffer is used to transmit an MCSPI word to a peripheral (the MCSPI_CHCONF_0/1/2/3[27] FFEW bit must be set to 1). It defines the almost-empty buffer status. See Figure 13-40. 

When the FIFO pointer does not reach this level, an interrupt or a DMA request is sent to the processor to enable the system to write AEL + 1 bytes to the transmit register. 

## **Note** 

AEL + 1 must correspond to a multiple value of the MCSPI_CHCONF_0/1/2/3[11-7] WL bit field. 

When DMA is used, the request is de-asserted after the first transmit register write. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1176 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

No new request is asserted again as long as the system has not performed the correct number of write accesses. 

**==> picture [395 x 157] intentionally omitted <==**

**----- Start of picture text -----**<br>
full FIFO size<br>MCSPI_XFERLEVEL<br>[5-0] AEL (bytes)<br>empty 0<br>MCSPI_IRQSTATUS<br>TXx_EMPTY bit<br>TXx_UNDERFLOW bit<br>spi-024<br>Next MCSPI<br>transmission<br>CPU write<br>MCSPI transmission<br>**----- End of picture text -----**<br>


**Figure 13-40. Buffer Almost Empty Level (AEL)** 

## **Note** 

The MCSPI_IRQSTATUS register bits are not available in DMA mode. In DMA mode, the SPI_DMA_WRITE_i request is asserted on the same conditions as the MCSPI_IRQSTATUS TXx_EMPTY flag. 

## _**13.1.3.4.6.3 End of Transfer Management**_ 

When the FIFO buffer is enabled for a channel, the user must previously configure in the MCSPI_XFERLEVEL register the AEL and AFL levels and especially the MCSPI_XFERLEVEL[31-16] WCNT bit field to define the number of MCSPI words to be transferred using the FIFO before enabling the channel. 

This counter lets the controller stop the transfer correctly after a defined number of MCSPI word transfers. If WNCT is set to 0x0000, the counter is not used and the user must stop the transfer manually by disabling the channel; in this case, the user does not know how many MCSPI transfers have been done. For received words, software must poll the MCSPI_CHSTAT_i[5] RXFFE bit and read the MCSPI_RX_0/1/2/3 receive register to empty the FIFO buffer. 

When the end-of-word count interrupt is generated (the MCSPI_IRQSTATUS[17] EOW bit is set), the user can disable the channel and poll the MCSPI_CHSTAT_0/1/2/3[5] RXFFE bit to know the last MCSPI words in the FIFO buffer and read them. 

## _**13.1.3.4.6.4 Multiple MCSPI Word Access**_ 

The processor has the ability to perform multiple MCSPI word access to the receive or transmit registers within a single 32-bit interface access by setting the MCSPI_MODULCTRL[7] MOA to 1 under specific conditions: 

- The channel selected has the FIFO enable. 

- Only FIFO sense enabled support the kind of access. 

- MCSPI_MODULCTRL[7] MOA is set to 1. 

- Only 32-bit interface access and data width can be performed to receive or transmit registers, for other kind of access the processor must de-assert MCSPI_MODULCTRL[7] MOA bit. 

- The level MCSPI_XFERLEVEL[7-0] AEL and MCSPI_XFERLEVEL[15-8] AFL must be 32-bit aligned, it means that AEL[0] = AEL[1] = 1 or AFL[0] = AFL[1] = 1. 

- If MCSPI_XFERLEVEL[31-16] WCNT is used it must be configured according to MCSPI word length. 

- The word length of MCSPI words allows to perform multiple MCSPI access, that means that MCSPI_CHCONF_0/1/2/3[11-7] WL is <16. 

The number of MCSPI word access depends on MCSPI word length: 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1177 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- 3 ≤ WL ≤ 7, MCSPI word length smaller or equal to byte length, 4 MCSPI words accessed per 32-bit interface read/write. If word count is used (MCSPI_XFERLEVEL[31-16] WCNT), set the bit field to WCNT[0] = WCNT[1] = 0. 

- 8 ≤ WL ≤ 15, MCSPI word length greater than byte or equal to 16-bit length, 2 MCSPI words accessed per 32-bit interface read/write. If word count is used (MCSPI_XFERLEVEL[31-16] WCNT]), set the bit field to WCNT[0] = 0. 

- 16 ≤ WL Multiple MCSPI word access is not applicable. 

## _**13.1.3.4.6.5 First MCSPI Word Delay**_ 

Figure 13-41 shows the MCSPI controller ability to delay the first MCSPI word transfer to give time for system to complete some parallel processes or fill the FIFO in order to improve transfer bandwidth. This delay is applied only on first MCSPI word after MCSPI channel enabled and first write in transmit register. It is based on output clock frequency. 

This option is meaningful in controller mode and single channel mode asserted through MCSPI_MODULCTRL[0] SINGLE. 

**==> picture [500 x 195] intentionally omitted <==**

**----- Start of picture text -----**<br>
MCSPI shift clock<br>(SPICLKREF)<br>Channel enabled<br>Internal start request<br>SPICLK (POL = 0)<br>SPIEN[i]<br>Initial delay on first MCSPI word<br>(MCSPI_MODULCTRL[6-4] INITDLY value)<br>spi-016a<br>**----- End of picture text -----**<br>


**Figure 13-41. Controller Single Channel Initial Delay** 

Few delay values are available: No delay, 4/8/16/32 MCSPI cycles. 

Its accuracy is half cycle in clock bypass mode and depends on clock polarity and phase. 

## _**13.1.3.4.7 MCSPI Interrupts**_ 

Each channel can issue interrupt events. 

Each interrupt event has status bits in the MCSPI_IRQSTATUS register (RXx_FULL, TXx_UNDERFLOW, TXx_EMPTY, etc.) (where x = 0, 3) that indicate whether service is required. Each status bit has an interrupt enable bit (a mask) in the MCSPI_IRQENABLE register (RXx_FULL_ENABLE, TXx_UNDERFLOW_ENABLE, TXx_EMPTY_ENABLE, etc.). 

When an interrupt occurs and a mask is later applied on it, the interrupt line is not asserted again, even if the interrupt source is not serviced. 

The MCSPI supports interrupt-driven and polling operations. 

## _**13.1.3.4.7.1 Interrupt Events in Controller Mode**_ 

In controller mode, the interrupt events related to the state of the MCSPI_TX_0/1/2/3 register are TXx_EMPTY and TXx_UNDERFLOW. The interrupt event related to the state of the MCSPI_RX_0/1/2/3 register is RXx_FULL. 

1178 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.1.3.4.7.1.1 TXx_EMPTY**_ 

The TXx_EMPTY event is activated when a channel is enabled and its MCSPI_TX_0/1/2/3 register is empty (transient event). Enabling a channel automatically triggers this event, except in controller receiveonly mode (see Section 13.1.3.4.3.4, _Controller Receive-Only Mode_ ). When the FIFO buffer is enabled (the MCSPI_CHCONF_0/1/2/3[27] FFEW bit is set to 1), the MCSPI_IRQSTATUS TXx_EMPTY bit is set as soon as there is enough space in the buffer to write a number of bytes defined by the MCSPI_XFERLEVEL[5-0] AEL bit field. 

The MCSPI_TX_0/1/2/3 register must be loaded with data to remove the source of the interrupt; the MCSPI_IRQSTATUS TXx_EMPTY interrupt status bit must be cleared for interrupt line deassertion (if the event is enabled as the interrupt source). 

When FIFO is enabled, no new TXx_EMPTY event is asserted as long as the processor has not performed the number of writes into the MCSPI_TX_0/1/2/3 register defined by the MCSPI_XFERLEVEL[5-0] AEL bit field. The processor must perform the correct number of writes. 

## _**13.1.3.4.7.1.2 TXx_UNDERFLOW**_ 

The event TXx_UNDERFLOW is activated when the channel is enabled and if the MCSPI_TX_0/1/2/3 register or the FIFO is empty (not updated with new data) when an external controller device starts a data transfer with the MCSPI (transmit and receive). 

The TXx_UNDERFLOW is a harmless warning in controller mode. 

To avoid having a TXx_UNDERFLOW event at the beginning of a transmission, the TXx_UNDERFLOW event is not activated when no data has been loaded into the MCSPI_TX_0/1/2/3 register, because the channel is enabled. To avoid having a TXx_UNDERFLOW event, the MCSPI_TX_0/1/2/3 register must seldom be loaded. 

The MCSPI_IRQSTATUS TXx_UNDERFLOW interrupt status bit must be cleared for interrupt line deassertion (if the event is enabled as the interrupt source). 

## _**13.1.3.4.7.1.3 RXx_ FULL**_ 

The RXx_FULL event is activated when a channel is enabled and the MCSPI_RX_0/1/2/3 register becomes filled (transient event). When the FIFO buffer is enabled (the MCSPI_CHCONF_0/1/2/3[28] FFER bit is set to 1), RXx_ FULL is asserted as soon as the number of bytes held in the FIFO to be read reaches the MCSPI_XFERLEVEL[13-8] AFL threshold. 

The MCSPI_RX_0/1/2/3 register must be read to remove the source of the interrupt; the MCSPI_IRQSTATUS RXx_FULL interrupt status bit must be cleared for interrupt line deassertion (if the event is enabled as the interrupt source). 

When FIFO is enabled, no new RXx_FULL event is asserted as long as the processor has not performed AFL + 1 reads into MCSPI_RX_0/1/2/3. The processor must perform the correct number of reads. 

## _**13.1.3.4.7.1.4 End Of Word Count**_ 

The MCSPI_IRQSTATUS[17] EOW event (end of word count) is activated when the channel is enabled and configured to use the built-in FIFO. This interrupt is raised when the controller performs the number of transfers defined in the MCSPI_XFERLEVEL[31-16] WCNT bit field. If WCNT is set to 0x0000, the counter is not enabled and this interrupt is not generated. 

The end of word count interrupt also indicates that the MCSPI transfer is halted on the channel using the FIFO buffer as soon as MCSPI_XFERLEVEL[31-16] WCNT is not reloaded and the channel is not re-enabled. 

The MCSPI_IRQSTATUS[17] EOW interrupt status bit must be cleared for interrupt line deassertion (if the event is enabled as the interrupt source). 

## _**13.1.3.4.7.2 Interrupt Events in Peripheral Mode**_ 

In peripheral mode, the interrupt events related to the state of the MCSPI_TX_0/1/2/3 register are TX0_EMPTY and TX0_UNDERFLOW. The interrupt events related to the state of the MCSPI_RX_0/1/2/3 are RX0_FULL 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1179 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

and RX0_OVERFLOW (channels 1, 2, and 3 do not have a receiver overflow status bit). See the MCSPI_IRQSTATUS register. 

## _**13.1.3.4.7.2.1 TXx_EMPTY**_ 

The TXx_EMPTY event is activated when a channel is enabled and its MCSPI_TX_0/1/2/3 register is empty. Enabling the channel automatically raises this event. If the FIFO buffer is enabled (the MCSPI_CHCONF_0/1/2/3[27] FFEW bit is set to 1), the TXx_EMPTY event is asserted as soon as there is enough space in buffer to write a number of bytes defined by the MCSPI_XFERLEVEL[5-0] AEL bit field. 

The MCSPI_TX_0/1/2/3 register must be loaded with data to remove the source of the interrupt; the MCSPI_IRQSTATUS TXx_EMPTY interrupt status bit must be cleared for interrupt line deassertion (if the event is enabled as the interrupt source). 

When FIFO is enabled, no new TXx_EMPTY event is asserted as long as the processor has not performed the number of writes into the MCSPI_TX_0/1/2/3 register defined by MCSPI_XFERLEVEL[5-0] AEL bit field. The processor must perform the correct number of writes. 

## _**13.1.3.4.7.2.2 TXx_UNDERFLOW**_ 

The TXx_UNDERFLOW event is activated when a channel is enabled and if the MCSPI_TX_0/1/2/3 register is empty (not updated with new data) when an external controller device starts a data transfer with the MCSPI (transmit and receive). 

When FIFO is enabled, the data emitted while the underflow event is raised is not the last data written in the FIFO but the old data in the FIFO (an old transmitted value or a dummy data in the FIFO has been reset). 

TXx_UNDERFLOW indicates an error (data loss) in peripheral mode. 

To avoid having a TXx_UNDERFLOW event at the beginning of a transmission, the TXx_UNDERFLOW event is not activated when no data has been loaded into the MCSPI_TX_0/1/2/3 register because the channel is enabled. 

The MCSPI_IRQSTATUS TXx_UNDERFLOW interrupt status bit must be cleared for interrupt line deassertion (if the event is enabled as the interrupt source). 

## _**13.1.3.4.7.2.3 RXx_FULL**_ 

The RXx_FULL event is activated when a channel is enabled and the MCSPI_RX_0/1/2/3 register is being filled (transient event). When the FIFO buffer is enabled (the MCSPI_CHCONF_0/1/2/3[28] FFER bit is set to 1), RXx_FULL is asserted as soon as the number of bytes held in the buffer to read defined by the MCSPI_XFERLEVEL[13-8] AFL bit field. 

The MCSPI_RX_0/1/2/3 register must be read to remove the source of the interrupt; the MCSPI_IRQSTATUS RXx_FULL interrupt status bit must be cleared for interrupt line deassertion (if the event is enabled as the interrupt source). 

When FIFO is enabled, no new RXx_FULL event is asserted as long as the processor has not performed AFL + 1 reads into MCSPI_RX_0/1/2/3. The processor must perform the correct number of reads. 

## _**13.1.3.4.7.2.4 RX0_OVERFLOW**_ 

The RX0_OVERFLOW event is activated in peripheral mode in transmit-and-receive mode or receive-only mode when a channel is enabled and the MCSPI_RX_0/1/2/3 register or FIFO is full when a new MCSPI word is received. The MCSPI_RX_0/1/2/3 register is always overwritten with the new MCSPI word. If the FIFO is enabled, data within the FIFO are overwritten; it must be considered as corrupted. The RX0_OVERFLOW event should not appear in peripheral mode using the FIFO. 

The RX0_OVERFLOW event indicates an error (data loss) in peripheral mode. 

The MCSPI_IRQSTATUS[3] RX0_OVERFLOW interrupt status bit must be cleared for interrupt line deassertion (if the event is enabled as the interrupt source). 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1180 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.1.3.4.7.2.5 End Of Word Count**_ 

The MCSPI_IRQSTATUS[17] EOW event (end of word count) is activated when the channel is enabled and configured to use the built-in FIFO. This interrupt is raised when the controller performs the number of transfers defined in the MCSPI_XFERLEVEL[31-16] WCNT bit field. If WCNT is set to 0x0000, the counter is not enabled and this interrupt is not generated. 

The end of word count interrupt also indicates that the MCSPI transfer is halted on the channel using the FIFO buffer as soon as WCNT is not reloaded and the channel is not re-enabled. 

The MCSPI_IRQSTATUS[17] EOW interrupt status bit must be cleared for interrupt line deassertion (if the event is enabled as the interrupt source). 

## _**13.1.3.4.7.3 Interrupt-Driven Operation**_ 

An interrupt enable bit in the MCSPI_IRQENABLE register can be set to enable each event to generate interrupt requests when the corresponding event occurs. Status bits are automatically set by hardware logic conditions. 

When an event occurs (the single interrupt line is asserted), the processor must: 

1. Read the MCSPI_IRQSTATUS register to identify which event occurred. 

2. Read the MCSPI_RX_0/1/2/3 register that corresponds to the event to remove the source of an RXx_FULL event or write into the MCSPI_TX_0/1/2/3 register that corresponds to the event to remove the source of a TXx_EMPTY event. No action is required to remove the source of the TXx_ UNDERFLOW and RX0_OVERFLOW events. 

3. Set the corresponding bit of the MCSPI_IRQSTATUS register to 1 to clear an interrupt status and then release the interrupt line. 

The interrupt status bit must always be reset after channel enabling and before events are enabled as interrupt sources. 

## _**13.1.3.4.7.4 Polling**_ 

When the interrupt capability of an event is disabled in the MCSPI_IRQENABLE register, the interrupt line is not asserted, but the status bits in the MCSPI_IRQSTATUS register can be polled by software to detect when the corresponding event occurs. 

Once the expected event occurs: 

- RXx_FULL: To remove the source of the event, the processor must read the corresponding MCSPI_RX_0/1/2/3 register. 

- TXx_EMPTY: To remove the source of the event, the processor must write into the corresponding MCSPI_TX_0/1/2/3 register. 

- TXx_UNDERFLOW and RX0_OVERFLOW: No action is required to remove the source of the event. 

To clear an interrupt, set the corresponding status bit of the MCSPI_IRQSTATUS register to 1. This does not affect the interrupt line state. 

## _**13.1.3.4.8 MCSPI DMA Requests**_ 

Each MCSPI channel, if enabled, can issue DMA requests. There are two DMA request lines per MCSPI channel (one for read and one for write). 

The DMA read request line is asserted when the MCSPI channel is enabled and new data is available in the receive register of the MCSPI channel. A DMA read request can be individually masked with the MCSPI_CHCONF_0/1/2/3[15] DMAR bit. The DMA read request line is de-asserted when reading of the MCSPI_RX_0/1/2/3 register of the MCSPI channel completes. 

The DMA write request line is asserted when the MCSPI channel is enabled and the MCSPI_TX_0/1/2/3 register of the MCSPI channel is empty. A DMA write request can be individually masked with the MCSPI_CHCONF_0/1/2/3[14] DMAW bit. The DMA write request line is de-asserted when loading of the MCSPI_TX_0/1/2/3 register of the channel completes. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1181 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.1.3.5 MCSPI Programming Guide** 

This section describes the low-level hardware programming sequences for the configuration and use of the MCSPI module. 

## _**13.1.3.5.1 MCSPI Global Initialization**_ 

## _**13.1.3.5.1.1 MCSPI Global Initialization**_ 

## _**13.1.3.5.1.1.1 Main Sequence – MCSPI Global Initialization**_ 

The procedure in Table 13-31 can be used to initialize MCSPI when performing software reset. 

**Table 13-31. MCSPI Global Initialization** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Perform a software reset.|MCSPI_SYSCONFIG[1] SOFTRESET|1|
|Wait until reset is finished?|MCSPI_SYSSTATUS[0] RESETDONE|=1|
|Configure static settings (such as SPI controller or|MCSPI_MODULCTRL[8-0]|0x-|
|peripheral) as required.|||
|Write MCSPI_SYSCONFIG|MCSPI_SYSCONFIG|0x-|



## _**13.1.3.5.2 MCSPI Operational Mode Configuration**_ 

## _**13.1.3.5.2.1 MCSPI Operational Modes**_ 

The selection of the working mode is done with the MCSPI_CHCONF_0/1/2/3 register. 

**Table 13-32. MCSPI Receive Mode Initialization** 

|**Step**||**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|---|
|Set receive mode for the channel.||MCSPI_CHCONF_0/1/2/3[13-12] TRM|0x1|
|Configure SPI clock polarity/phase, clock divider, word||MCSPI_CHCONF_0/1/2/3|0x-|
|length, and others for the channel.||||
|Reset the status bits.||MCSPI_IRQSTATUS|0x0|
||**Table 13-33. MCSPI Transmit Mode Initialization**|||
|**Step**||**Register/Bit Field/Programming Model**|**Value**|
|Set transmit mode for the channel.||MCSPI_CHCONF_0/1/2/3[13-12] TRM|0x2|
|Configure SPI clock polarity/phase, clock divider, word||MCSPI_CHCONF_0/1/2/3|0x-|
|length, and others for the channel.||||
|Reset the status bits.||MCSPI_IRQSTATUS|0x0|
|**Table**|**13-34. MCSPI**|**Transmit-and-Receive Mode Initialization**||
|**Step**||**Register/Bit Field/Programming Model**|**Value**|
|Set transmit and receive mode for the channel.||MCSPI_CHCONF_0/1/2/3[13-12] TRM|0x0|
|Configure SPI clock polarity/phase, clock divider, word||MCSPI_CHCONF_0/1/2/3|0x-|
|length, and others for the channel.||||
|Reset the status bits.||MCSPI_IRQSTATUS|0x0|



## _**13.1.3.5.2.1.1 Common Transfer Sequence**_ 

MCSPI module allows the transfer of one or several words, according to different modes: 

- CONTROLLER Normal, CONTROLLER Turbo, PERIPHERAL 

- TRANSMIT–RECEIVE, TRANSMIT-ONLY, RECEIVE-ONLY 

- Write and Read requests: Interrupts, DMA 

- SPIEN[i] lines assertion/deassertion: automatic, manual 

For all these sequences, the host process contains the main process and the interrupt routines. 

The interrupt routines are called on the interrupt signals or by an internal call if the module is used in polling mode. 

1182 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

Table 13-35 represents the main sequence which is common to all transfers. 

In multi-channel controller mode, the sequences of different channels can be run simultaneously. 

**Table 13-35. Common Transfer Sequence (Main Process)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Write MCSPI_IRQSTATUS to reset channel status bits|MCSPI_IRQSTATUS[channel i bits]|0b1111|
|Write MCSPI_IRQENABLE to enable interrupts|MCSPI_IRQENABLE|0x-|
|Write MCSPI_CHCONF_0/1/2/3 to configure the|MCSPI_CHCONF_0/1/2/3|0x-|
|channel|||
|Start the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Wait for the first write request (TX empty or DMA write)|||
|Write the transmitter register with data|MCSPI_TX_0/1/2/3|0x-|
|Wait for the host event for end of transfer|||
|Stop the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|0|



## _**13.1.3.5.2.1.2 End of Transfer Sequences**_ 

The end of transfer depends on the transfer mode. Table 13-36 summarizes the type of end of transfer per transfer mode and gives a reference to the appropriate section for details. 

**Table 13-36. End of Transfer Sequences** 

|||**TRANSMIT-AND-RECEIVE**|**TRANSMIT-AND-RECEIVE**|**TRANSMIT-ONLY**|**TRANSMIT-ONLY**|**RECEIVE-ONLY**|**RECEIVE-ONLY**|
|---|---|---|---|---|---|---|---|
|||**INTERRUPT**|**DMA**|**INTERRUPT**|**DMA**|**INTERRUPT**|**DMA**|
|**CONTROL**<br>**LER**<br>**Normal**|End of transfer<br>sequence|SeeSection 13.1.3.5.2.1.3||SeeSection<br>13.1.3.5.2.1.4.1|SeeSection<br>13.1.3.5.2.1.4.2|SeeSection<br>13.1.3.5.2.1.5.1|SeeSection<br>13.1.3.5.2.1.5.<br>2|
||Minimum number<br>of word|1|1|1|1|1|2|
||DMA transfer size||N||N||N-1|
|**CONTROL**<br>**LER Turbo**|End of transfer<br>sequence|SeeSection 13.1.3.5.2.1.3||SeeSection<br>13.1.3.5.2.1.4.1|SeeSection<br>13.1.3.5.2.1.4.2|SeeSection<br>13.1.3.5.2.1.6.1|SeeSection<br>13.1.3.5.2.1.6.<br>2|
||Minimum number<br>of word|1|1|1|1|2|3|
||DMA transfer size||N||N||N-2|
|**PERIPHER**<br>**AL**|End of transfer<br>sequence|SeeSection 13.1.3.5.2.1.3||SeeSection<br>13.1.3.5.2.1.4.1|SeeSection<br>13.1.3.5.2.1.4.2|SeeSection 13.1.3.5.2.1.7||
||Minimum number<br>of word|1|1|1|1|1|1|
||DMA transfer size||N||N|N|N|



The transfer to execute has a size of N words. 

The different sequences can be merged in one process to manage transfers of several types. The end of transfer sequences are described from the start of the channel. 

In these sequences, some soft variables are used: 

- write_count = 0 

- read_count = 0 

- channel_enable = FALSE 

- last_transfer = FALSE 

- last_request = FALSE 

They are initialized before starting the channel. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1183 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.3.5.2.1.3 Transmit-and-Receive (Controller and Peripheral)**_ 

If the requests are configured in DMA, write_count and read_count are assigned with ‘N’ when the DMA handlers have completed their ‘N’ CBASS0 accesses. 

**Table 13-37. Transmit-and-Receive (Controller and Peripheral) (Main Process)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Start the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Wait for write_count = N**AND**read_count = N|||
|Stop the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|0|



## **Table 13-38. Transmit-and-Receive (Controller and Peripheral) (Interrupt Routine)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Read MCSPI_IRQSTATUS|MCSPI_IRQSTATUS|0x-|
|Write MCSPI_IRQSTATUS to reset channel status bits|MCSPI_IRQSTATUS[channel i bits]|0b1111|
|**IF:**TXx_EMPTY|||
|Write the transmitter register with data|MCSPI_TX_0/1/2/3|0x-|
|Increment write_count +1|||
|**IF:**RXx_FULL|||
|Read the receiver register|MCSPI_RX_0/1/2/3||
|Increment read_count +1|||
|**ENDIF**|||



## _**13.1.3.5.2.1.4 Transmit-Only (Controller and Peripheral)**_ 

## _**13.1.3.5.2.1.4.1 Based on Interrupt Requests**_ 

**Table 13-39. Transmit-Only With Interrupts (Controller and Peripheral) (Main Process)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Start the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Wait until last transfer = TRUE|||
|Wait for end of transfer|MCSPI_CHSTAT_0/1/2/3[2] EOT|=1|
|Stop the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|0|



## **Table 13-40. Transmit-Only With Interrupts (Controller and Peripheral) (Interrupt Routine)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Read MCSPI_IRQSTATUS|MCSPI_IRQSTATUS|0x-|
|Write MCSPI_IRQSTATUS to reset channel status bits|MCSPI_IRQSTATUS[channel i bits]|0b1111|
|**IF:**TXx_EMPTY**AND**write_count < N|||
|Write the transmitter register with data|MCSPI_TX_0/1/2/3|0x-|
|Increment write_count +1|||
|**ELSEIF:**write_count ≥ N|||
|last_transfer = TRUE|||
|**ENDIF**|||



## _**13.1.3.5.2.1.4.2 Based on DMA Write Requests**_ 

When the DMA handler has completed its ‘N’ CBASS0 accesses, write_count is assigned with ‘N’. 

**Table 13-41. Transmit-Only With DMA (Controller and Peripheral) (Main Process)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Start the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Wait until write_count = N|||



1184 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-41. Transmit-Only With DMA (Controller and Peripheral) (Main Process) (continued)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Disable DMA write request|MCSPI_CHCONF_0/1/2/3[14] DMAW|0|
|Wait until last_transfer = TRUE|||
|Wait for end of transfer|MCSPI_CHSTAT_0/1/2/3[2] EOT|=1|
|Stop the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|0|



**Table 13-42. Transmit-Only With DMA (Controller and Peripheral) (Interrupt Routine)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Read MCSPI_IRQSTATUS|MCSPI_IRQSTATUS|0x-|
|Write MCSPI_IRQSTATUS to reset channel status bits|MCSPI_IRQSTATUS[channel i bits]|0b1111|
|**IF:**TXx_EMPTY**AND**write_count = N|||
|last_transfer = TRUE|||
|**ENDIF**|||



## _**13.1.3.5.2.1.5 Controller Normal Receive-Only**_ 

_**13.1.3.5.2.1.5.1 Based on Interrupt Requests**_ 

**Table 13-43. Receive-Only With Interrupt (Controller Normal) (Main Process)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Start the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Wait until last_request = TRUE|||
|Stop the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|0|
|Read the receiver register|MCSPI_RX_0/1/2/3|0x-|
|Increment read_count +1|||



**Table 13-44. Receive-Only With Interrupt (Controller Normal) (Interrupt Routine)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Read MCSPI_IRQSTATUS|MCSPI_IRQSTATUS|0x-|
|Write MCSPI_IRQSTATUS to reset channel status bits|MCSPI_IRQSTATUS[channel i bits]|0b1111|
|**IF:**RXx_FULL**AND**read_count = N - 1|||
|last_request = TRUE|||
|**ELSEIF:**read_count ≠ N - 1|||
|Read the receiver register|MCSPI_RX_0/1/2/3|0x-|
|Increment read_count +1|||
|**ENDIF**|||



## _**13.1.3.5.2.1.5.2 Based on DMA Read Requests**_ 

When the DMA handler has completed its ‘N-1’ CBASS0 accesses, read_count is assigned with ‘N-1’. 

**Table 13-45. Receive-Only With DMA (Controller Normal) (Main Process)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Start the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Wait until read_count = N - 1|||
|Disable DMA read request|MCSPI_CHCONF_0/1/2/3[15] DMAR|0|
|Wait until last_transfer = TRUE|||
|Stop the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|0|
|Read the receiver register|MCSPI_RX_0/1/2/3|0x-|
|Increment read_count +1|||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1185 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-46. Receive-Only With DMA (Controller Normal) (Interrupt Routine)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Read MCSPI_IRQSTATUS|MCSPI_IRQSTATUS|0x-|
|Write MCSPI_IRQSTATUS to reset channel status bits|MCSPI_IRQSTATUS[channel i bits]|0b1111|
|**IF:**RXx_FULL**AND**read_count = N-1|||
|last_transfer = TRUE|||
|**ENDIF**|||



## _**13.1.3.5.2.1.6 Controller Turbo Receive-Only**_ 

## _**13.1.3.5.2.1.6.1 Based on Interrupt Requests**_ 

**Table 13-47. Receive-Only With Interrupt (Controller Turbo) (Main Process)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Start the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Wait until channel_enable = TRUE|||
|Wait until last_transfer = TRUE|||
|Wait for end of transfer|MCSPI_CHSTAT_0/1/2/3[2] EOT|=1|
|Stop the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|0|
|Wait until channel_enable = FALSE|||



**Table 13-48. Receive-Only With Interrupt (Controller Turbo) (Interrupt Routine)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Read MCSPI_IRQSTATUS|MCSPI_IRQSTATUS|0x-|
|Write MCSPI_IRQSTATUS to reset channel status bits|MCSPI_IRQSTATUS[channel i bits]|0b1111|
|**IF:**RXx_FULL|||
|**IF:**read_count = N - 2|||
|last_transfer = TRUE|||
|channel_enable = FALSE|||
|**ENDIF**|||
|**IF:**read_count < N|||
|Read the receiver register|MCSPI_RX_0/1/2/3|0x-|
|Increment read_count +1|||
|**ENDIF**|||
|**ENDIF**|||



## _**13.1.3.5.2.1.6.2 Based on DMA Read Requests**_ 

When the DMA handler has completed its ‘N-2’ CBASS0 accesses read_count is assigned with ‘N-2‘. 

**Table 13-49. Receive-Only With DMA (Controller Turbo) (Main Process)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Start the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Wait until channel_enable = TRUE|||
|Wait until read_count = N-2|||
|Disable DMA read request|MCSPI_CHCONF_0/1/2/3[15] DMAR|0|
|Wait until last_transfer = TRUE|||
|Wait for end of transfer|MCSPI_CHSTAT_0/1/2/3[2] EOT|=1|
|Stop the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|0|
|Wait until channel_enable = FALSE|||



1186 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-50. Receive-Only With DMA (Controller Turbo) (Interrupt Routine)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Read MCSPI_IRQSTATUS|MCSPI_IRQSTATUS|0x-|
|Write MCSPI_IRQSTATUS to reset channel status bits|MCSPI_IRQSTATUS[channel i bits]|0b1111|
|**IF:**RXx_FULL|||
|**IF:**read_count = N - 2|||
|last_transfer = TRUE|||
|channel_enable = FALSE|||
|**ENDIF**|||
|**IF:**read_count < N|||
|Read the receiver register|MCSPI_RX_0/1/2/3|0x-|
|Increment read_count +1|||
|**ENDIF**|||
|**ENDIF**|||



## _**13.1.3.5.2.1.7 Peripheral Receive-Only**_ 

If the requests are configured in DMA, read_count is assigned with ‘N’ when the DMA handler has completed its ‘N‘ CBASS0 accesses. 

**Table 13-51. Receive-Only (Peripheral) (Main Process)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Start the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Wait until read_count = N|||
|Stop the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|0|



**Table 13-52. Receive-Only (Peripheral) (Interrupt Routine)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Read MCSPI_IRQSTATUS|MCSPI_IRQSTATUS|0x-|
|Write MCSPI_IRQSTATUS to reset channel status bits|MCSPI_IRQSTATUS[channel i bits]|0b1111|
|**IF:**RXx_FULL|||
|Read the receiver register|MCSPI_RX_0/1/2/3|0x-|
|Increment read_count +1|||
|**ENDIF**|||



## _**13.1.3.5.2.1.8 Transfer Procedures With FIFO**_ 

These flows describe the transfer with FIFO. 

The MCSPI module allows the transfer of one or several words, according to different modes: 

- CONTROLLER Normal, CONTROLLER Turbo, PERIPHERAL 

- TRANSMIT–RECEIVE, TRANSMIT-ONLY, RECEIVE-ONLY 

- Write and Read requests: IRQ, DMA 

For all these flows, the host process contains the main process and the interrupt routine. This routine is called on the IRQ signals or by an internal call if the module is used in polling mode. 

For more information, see Section 13.1.3.4.6, _MCSPI FIFO Buffer Management_ . 

**Table 13-53. FIFO Mode Common Sequence (Controller) (Main Process)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Write MCSPI_IRQSTATUS to reset channel status bits|MCSPI_IRQSTATUS|1|
|Write MCSPI_IRQENABLE to enable interrupts|MCSPI_IRQENABLE|1|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1187 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-53. FIFO Mode Common Sequence (Controller) (Main Process) (continued)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Write MCSPI_CHCONF_0/1/2/3 to configure the|MCSPI_CHCONF_0/1/2/3|0x-|
|channel|||
|Write MCSPI_XFERLEVEL|MCSPI_XFERLEVEL|0x-|
|Start the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|**IF:**Receive only|||
|Wait for the write request (TX empty or DMA write)|||
|Write for the transmitter register with data|MCSPI_TX_0/1/2/3|0x-|
|**ENDIF**|||
|Wait for the host event for end of transfer|||
|Stop the channel|MCSPI_CHCTRL_0/1/2/3[0] EN|0|



## _**13.1.3.5.2.1.8.1 Common Transfer Sequence in FIFO Mode**_ 

This flow describes the host sequence for a transfer of any type defined in Section 13.1.3.5.2.1.8, _Transfer Procedures With FIFO_ . 

In multi-channel, only one channel can use the FIFO. 

Before enabling the FIFO for a channel (MCSPI_CHCONF_0/1/2/3[28] FFER and MCSPI_CHCONF_0/1/2/3[27] FFEW bits), the host must check that the FIFO is not enabled for another channel, even if these channels are not used. 

In transmit-and-receive mode, the FIFO can be enabled for write or read request only, without FIFO for the other request. 

In Peripheral mode, the channel 0 only can be activated. The correct SPIEN line is chosen in MCSPI_CHCONF_0[22-21] SPIENSLV bits. 

The MCSPI module can start the transfer only when the first write request has been released by writing the MCSPI_TX_0/1/2/3 register, even in receive-only mode (only one write request occurs in this case). 

## _**13.1.3.5.2.1.8.2 End of Transfer Sequences in FIFO Mode**_ 

Table 13-54 summarizes the type of end of transfer per transfer mode and gives a reference to the appropriate section for details. 

**Table 13-54. End of Transfer Sequences in FIFO Mode** 

|**Word count**|**TRANSMIT AND RECEIVE**|**TRANSMIT-ONLY**|**RECEIVE-ONLY**|
|---|---|---|---|
|Yes|SeeFigure 13-42|SeeFigure 13-44|SeeFigure 13-45|
|No|SeeFigure 13-43|SeeFigure 13-44|SeeFigure 13-46|



The end of transfer sequences are described from the start of the channel. 

In these sequences, some soft variables are used: 

- write_count = N 

- read_count = N 

- last_request = FALSE 

They are initialized before starting the channel. 

## _**13.1.3.5.2.1.8.3 Transmit-and-Receive With Word Count**_ 

Figure 13-42 shows the flow of a transfer in transmit-and-receive mode, with word count. 

1188 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [500 x 339] intentionally omitted <==**

**----- Start of picture text -----**<br>
Main process FIFO request routine<br>Start the channel:<br>Write 1 in MCSPI_CHCTRL_0/1/2/3[0] EN bit No Yes<br>TXx_EMPTY ?<br>EOW interrupt<br>No write_count ≥ Yes<br>Stop the channel: write_request_size ?<br>Write 0 in MCSPI_CHCTRL_0/1/2/3[0] EN bit<br>Write last_write_request_size Write write_request_size<br>words to MCSPI_TX_0/1/2/3 words to MCSPI_TX_0/1/2/3<br>write_count = 0 decrement write_count<br>with write_request_size<br>Yes<br>read_count = 0 ?<br>No<br>Return<br>Read last_read_request_size words<br>from MCSPI_RX_0/1/2/3<br>read_count = 0<br>Next command<br>**----- End of picture text -----**<br>


**==> picture [25 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
mcspi_025<br>**----- End of picture text -----**<br>


**Figure 13-42. FIFO Mode Transmit-and-Receive With Word Count (Controller)** 

## _**13.1.3.5.2.1.8.4 Transmit-and-Receive Without Word Count**_ 

Figure 13-43 shows the flow of a transfer in transmit-and-receive mode, without word count. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1189 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [495 x 484] intentionally omitted <==**

**----- Start of picture text -----**<br>
Main process FIFO request routine<br>Start the channel: No Yes<br>Write 1 in MCSPI_CHCTRL_0/1/2/3[0] EN bit TXx_EMPTY ?<br>last_request = TRUE<br>No write_count ≥ Yes<br>write_request_size ?<br>Read<br>MCSPI_CHSTAT_0/1/2/3<br>Write last_write_request_size Write write_request_size<br>words to MCSPI_TX_0/1/2/3 words to MCSPI_TX_0/1/2/3<br>write_count = 0 decrement write_count<br>with write_request_size<br>No<br>MCSPI_CHSTAT_0/1/2/3<br>[3  TXFFE and]<br>[2] EOT ?<br>Yes<br>Yes<br>RXx_FULL ?<br>Stop the channel:<br>Write 0 in MCSPI_CHCTRL_0/1/2/3[0] EN bit No Read read_request_size<br>words to MCSPI_RX_0/1/2/3<br>decrement read_count<br>with read_request_size<br>Yes<br>read_count = 0 ?<br>Yes read_count ≥<br>read_request_size ?<br>No<br>No<br>Read last_read_request_size words<br>from MCSPI_RX_0/1/2/3 last_request = TRUE<br>read_count = 0<br>Next command Return<br>**----- End of picture text -----**<br>


**==> picture [25 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
mcspi_026<br>**----- End of picture text -----**<br>


**Figure 13-43. FIFO Mode Transmit-and-Receive Without Word Count (Controller)** 

## _**13.1.3.5.2.1.8.5 Transmit-Only**_ 

Figure 13-44 shows the flow of a transfer in transmit-only mode, with or without word count. The difference between word count enabled or not is just on the condition after starting the channel: 

- word count enable: wait for EOW interrupt 

- word count disable: wait for write_count = 0 

1190 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [80 x 9] intentionally omitted <==**

**----- Start of picture text -----**<br>
FIFO request routine<br>**----- End of picture text -----**<br>


**==> picture [495 x 331] intentionally omitted <==**

**----- Start of picture text -----**<br>
Main process FIFO request routine<br>Start the channel: No Yes<br>Write 1 in MCSPI_CHCTRL_0/1/2/3[0] EN bit TXx_EMPTY ?<br>EOW interrupt<br>or<br>write_count = 0 No write_count ≥ Yes<br>write_request_size ?<br>Read<br>MCSPI_CHSTAT_0/1/2/3 Write last_write_request_size Write write_request_size<br>words to MCSPI_TX_0/1/2/3 words to MCSPI_TX_0/1/2/3<br>write_count = 0 decrement write_count<br>with write_request_size<br>No MCSPI_CHSTAT_0/1/2/3<br>[3  TXFFE and [2] EOT ?]<br>Yes Return<br>Stop the channel:<br>Write 0 in MCSPI_CHCTRL_0/1/2/3[0] EN bit<br>Next command<br>**----- End of picture text -----**<br>


**==> picture [25 x 5] intentionally omitted <==**

**----- Start of picture text -----**<br>
mcspi_027<br>**----- End of picture text -----**<br>


**Figure 13-44. FIFO Mode Transmit-Only (Controller)** 

## _**13.1.3.5.2.1.8.6 Receive-Only With Word Count**_ 

Figure 13-45 shows the flow of a transfer in receive-only mode, with word count. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1191 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [422 x 329] intentionally omitted <==**

**----- Start of picture text -----**<br>
Main process FIFO request routine<br>Start the channel:<br>Write 1 in MCSPI_CHCTRL_0/1/2/3[0] EN bit Yes<br>RXx_FULL ?<br>EOW interrupt<br>No Read read_request_size<br>words to MCSPI_RX_0/1/2/3<br>Stop the channel: decrement read_count<br>Write 0 in MCSPI_CHCTRL_0/1/2/3[0] EN bit with read_request_size<br>Yes<br>read_count = 0 ?<br>Return<br>No<br>Read last_read_request_size words<br>from MCSPI_RX_0/1/2/3<br>read_count = 0<br>Next command<br>**----- End of picture text -----**<br>


**==> picture [25 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
mcspi_028<br>**----- End of picture text -----**<br>


**Figure 13-45. FIFO Mode Receive-Only With Word Count (Controller)** 

## _**13.1.3.5.2.1.8.7 Receive-Only Without Word Count**_ 

Figure 13-46 shows the flow of a transfer in receive-only mode, with word count. 

1192 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Main process** 

## **FIFO request routine** 

**==> picture [435 x 448] intentionally omitted <==**

**----- Start of picture text -----**<br>
Start the channel:<br>Yes<br>Write 1 in MCSPI_CHCTRL_0/1/2/3[0] EN bit<br>RXx_FULL ?<br>last_request = TRUE<br>No Read read_request_size<br>words to MCSPI_RX_0/1/2/3<br>decrement read_count<br>Yes with read_request_size<br>read_count = 0 ?<br>No Yes read_count ≥<br>read_request_size ?<br>Read No<br>MCSPI_CHSTAT_0/1/2/3<br>last_request = TRUE<br>No<br>RXx_FULL ?<br>Yes<br>Return<br>Read 1 word from MCSPI_RX_0/1/2/3<br>decrement read_count with 1<br>Stop the channel:<br>Write 0 in MCSPI_CHCTRL_0/1/2/3[0] EN bit<br>Next command<br>**----- End of picture text -----**<br>


mcspi_029 

## **Figure 13-46. FIFO Mode Receive-Only Without Word Count (Controller)** 

## _**13.1.3.5.2.1.9 Common Transfer Procedures Without FIFO – Polling Method 13.1.3.5.2.1.9.1 Receive-Only Procedure – Polling Method**_ 

Table 13-55 lists the receive-only procedure using the polling method. 

**Table 13-55. Receive-Only Procedure – Polling Method** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure the channel according to the mode.|SeeTable 13-32.||
|Start the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Wait for end-of-transfer.|MCSPI_CHSTAT_0/1/2/3[2] EOT|=1|
|Read the receiver register.|MCSPI_RX_0/1/2/3|0x-|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1193 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-55. Receive-Only Procedure – Polling Method (continued)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Stop the channel if no more data is expected.|MCSPI_CHCTRL_0/1/2/3[0] EN|0|



## _**13.1.3.5.2.1.9.2 Receive-Only Procedure – Interrupt Method**_ 

Table 13-56 lists the receive-only procedure using the interrupt method. 

**Table 13-56. Receive-Only Procedure – Interrupt Method** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure the channel according to the mode.|SeeTable 13-32.||
|Start the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Enable the interrupt for the receiver register.|MCSPI_IRQENABLE[2] RX_FULL_ENABLE|1|
|Wait for interrupt.|||
|Read the status register.|MCSPI_IRQSTATUS[2] RX_FULL|1|
|Disable the interrupt if no more data is expected.|MCSPI_IRQENABLE[2] RX_FULL_ENABLE|0|
|Stop the channel if no more data is expected.|MCSPI_CHCTRL_0/1/2/3[0] EN|0|
|Read the receiver register.|MCSPI_RX_0/1/2/3|0x-|



## _**13.1.3.5.2.1.9.3 Transmit-Only Procedure – Polling Method**_ 

Table 13-57 lists the transmit-only procedure using the polling method. 

**Table 13-57. Transmit-Only Procedure – Polling Method** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure the channel according to the mode.|SeeTable 13-33.||
|Start the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Write the transmitter register with data.|MCSPI_TX_0/1/2/3|0x-|
|Wait until end of transfer?|MCSPI_CHSTAT_0/1/2/3[2] EOT|=1|
|Stop the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|0|



## _**13.1.3.5.2.1.9.4 Transmit-and-Receive Procedure – Polling Method**_ 

Table 13-58 lists the transmit-and-receive procedure using the polling method. 

**Table 13-58. Transmit-and-Receive Procedure – Polling Method** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure the channel according to the mode.|SeeTable 13-34.||
|Start the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Write the transmitter register with data.|MCSPI_TX_0/1/2/3|0x-|
|Wait until transmit/receive word?|MCSPI_CHSTAT_0/1/2/3[2] EOT|=1|
|Stop the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|0|
|Read the receiver register.|MCSPI_RX_0/1/2/3|0x-|



## _**13.1.3.5.3 Common Transfer Procedures Without FIFO – Polling Method**_ 

## _**13.1.3.5.3.1 Receive-Only Procedure – Polling Method**_ 

Table 13-59 lists the receive-only procedure using the polling method. 

**Table 13-59. Receive-Only Procedure – Polling Method** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure the channel according to the mode.|SeeTable 13-32.||
|Start the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Wait for end-of-transfer.|MCSPI_CHSTAT_0/1/2/3[2] EOT|=1|



1194 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-59. Receive-Only Procedure – Polling Method (continued)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Read the receiver register.|MCSPI_RX_0/1/2/3|0x-|
|Stop the channel if no more data is expected.|MCSPI_CHCTRL_0/1/2/3[0] EN|0|



## _**13.1.3.5.3.2 Receive-Only Procedure – Interrupt Method**_ 

Table 13-60 lists the receive-only procedure using the interrupt method. 

**Table 13-60. Receive-Only Procedure – Interrupt Method** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure the channel according to the mode.|SeeTable 13-32.||
|Start the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Enable the interrupt for the receiver register.|MCSPI_IRQENABLE[2] RX_FULL_ENABLE|1|
|Wait for interrupt.|||
|Read the status register.|MCSPI_IRQSTATUS[2] RX_FULL|1|
|Disable the interrupt if no more data is expected.|MCSPI_IRQENABLE[2] RX_FULL_ENABLE|0|
|Stop the channel if no more data is expected.|MCSPI_CHCTRL_0/1/2/3[0] EN|0|
|Read the receiver register.|MCSPI_RX_0/1/2/3|0x-|



## _**13.1.3.5.3.3 Transmit-Only Procedure – Polling Method**_ 

Table 13-61 lists the transmit-only procedure using the polling method. 

**Table 13-61. Transmit-Only Procedure – Polling Method** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure the channel according to the mode.|SeeTable 13-33.||
|Start the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Write the transmitter register with data.|MCSPI_TX_0/1/2/3|0x-|
|Wait until end of transfer?|MCSPI_CHSTAT_0/1/2/3[2] EOT|=1|
|Stop the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|0|



## _**13.1.3.5.3.4 Transmit-and-Receive Procedure – Polling Method**_ 

Table 13-62 lists the transmit-and-receive procedure using the polling method. 

**Table 13-62. Transmit-and-Receive Procedure – Polling Method** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure the channel according to the mode.|SeeTable 13-34.||
|Start the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|1|
|Write the transmitter register with data.|MCSPI_TX_0/1/2/3|0x-|
|Wait until transmit/receive word?|MCSPI_CHSTAT_0/1/2/3[2] EOT|=1|
|Stop the channel.|MCSPI_CHCTRL_0/1/2/3[0] EN|0|
|Read the receiver register.|MCSPI_RX_0/1/2/3|0x-|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1195 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.4 Universal Asynchronous Receiver/Transmitter (UART)**_ 

This chapter describes the function, operation, and configuration of the Universal Asynchronous Receiver/ Transmitter (UART)/RS-485/Infrared Data Association (IrDA)/Consumer Infrared (CIR)/ISO 7816 module in the device. 

## **Note** 

UART and USART acronyms are used interchangeably in this section. 

## **13.1.4.1 UART Overview** 

The UART is a target peripheral that utilizes the DMA for data transfer or interrupt polling via host CPU. There are six UART modules in the device. Each module can be used in the following modes: UART, IrDA, CIR or ISO 7816. The UART modules support IrDA and CIR modes when a 48 MHz functional clock frequency is used. Each UART can be used for configuration and data exchange with a number of external peripheral devices or interprocessor communication between devices. 

## _**13.1.4.1.1 UART Features**_ 

The UART includes the following features: 

- 16C750-compatible 

- RS-485 external transceiver auto flow control support 

- 64-byte FIFO buffer for receiver and 64-byte FIFO buffer for transmitter 

- Programmable interrupt trigger levels for FIFOs 

- Programmable sleep mode 

- The 48 MHz functional clock is default option and allows baud rates up to 3.6 Mbps 

- Auto-baud between 1200 bits/s and 115.2 Kbits/s (only when 48 MHz function clock is used) 

- Optional multi-drop transmission 

- Configurable time-guard feature 

- Configurable data format: 

   - Data bit: 5, 6, 7, or 8 bits 

   - Parity bit: Even, Odd, None 

   - Stop-bit: 1, 1.5, 2 bit 

- Flow control: Hardware (RTS/CTS) or software (XON/XOFF) 

- False start bit detection 

- Line break generation and detection 

- Fully prioritized interrupt system controls 

- Internal test and loopback capabilities 

- Modem control functions (CTS, RTS) 

- Only UART1 module instance has extended modem control signals (DCD, RI, DTR, DSR) 

- Independent TX/RX 

- Supports both little and big Endian operating mode 

- Internal test and loopback capabilities 

## _**13.1.4.1.2 IrDA Features**_ 

The IrDA includes the following features: 

- Support of IrDA 1.4 slow infrared (SIR), medium infrared (MIR), and fast infrared (FIR) communications: 

   - Slow infrared (SIR 115.2 KBAUD), medium infrared (MIR 0.576 MBAUD) and fast infrared (FIR 4.0 MBAUD) operations (very fast infrared (VFIR) is not supported) 

   - Frame formatting: addition of variable beginning-of-frame (xBOF) characters and end-of-frame (EOF) characters 

   - 

   - Asynchronous transparency (automatic insertion of break character) 

   - Eight-entry status FIFO (with selectable trigger levels) to monitor frame length and frame errors 

   - Framing error, CRC error, illegal symbol (FIR), and abort pattern (SIR, MIR) detection 

1196 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- IrDA mode when 48 MHz function clock is used 

## _**13.1.4.1.3 CIR Features**_ 

The CIR mode uses a variable pulse-width modulation (PWM) technique (based on multiples of a programmable _t_ period) to encompass the various formats of infrared encoding for remote-control applications. The CIR logic transmits data packets based on a user-definable frame structure and packet content. 

The CIR includes the following features to provide CIR support for remote-control applications: 

- Transmit and receive mode 

- Free data format (supports any remote-control private standards) 

- Selectable bit rate 

- Configurable carrier frequency 

- 1/2, 5/12, 1/3, or 1/4 carrier duty cycle 

- CIR mode when 48 MHz function clock is used 

## _**13.1.4.1.4 ISO 7816 (Smartcard) Functions**_ 

ISO 7816 mode is a half duplex protocol that uses the TX line of the UART peripheral in a bidirectional mode. It is a low-level interface supporting protocols T=0 and T=1. The features of this mode are listed below: 

- Includes features to control repetition 

- Acknowledges cases of parity mismatch in T=0 mode 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1197 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.1.4.2 UART Environment** 

The UART[0-5] modules are hereinafter referred to as UART module. 

This section describes the UART/RS-485/IrDA/CIR external connections (environment). 

- The UART interface is described in Section 13.1.4.2.1, _UART Functional Interfaces_ . 

- The RS-485 interface is described in Section 13.1.4.2.2, _RS-485 Functional Interfaces_ . 

- The IrDA interface is described in Section 13.1.4.2.3, _IrDA Functional Interfaces_ . 

- The CIR interface is described in Section 13.1.4.2.4, _CIR Functional Interfaces_ . 

## _**13.1.4.2.1 UART Functional Interfaces**_ 

## _**13.1.4.2.1.1 System Using UART Communication With Hardware Handshake**_ 

Each UART instance can be easily connected to the UART port of an external IC (see Figure 13-47 ). 

**==> picture [417 x 261] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>UARTi Other device with<br>UART port<br>UARTi_TXD<br>TX TX<br>UARTi_RXD<br>RX RX<br>UARTi_RTSn<br>RTS RTS<br>UARTi_CTSn<br>CTS CTS<br>UARTj_DCDn<br>DCD* DCD<br>UARTj_DSRn<br>DSR* DSR<br>UARTj_DTRn<br>DTR* DTR<br>UARTj_RIN<br>RIN* RIN<br>* See UART Environment for extended modem control signals support<br>**----- End of picture text -----**<br>


**Figure 13-47. UART Mode Interface Signals** 

1198 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.1.4.2.1.2 UART Interface Description**_ 

Table 13-63 lists the UART interface input/output (I/O) signals. 

**Table 13-63. UART I/O Signals** 

|**Module Pin Name**|**Device Level Signal Name**|**I/O**(1)|**Description**|**Module Pin Reset Value**(2)|
|---|---|---|---|---|
|||**UART[0-5]**|||
|RX|UART[0-5]_RXD|I|Serial data input|HiZ|
|TX|UART[0-5]_TXD|O|Serial data output(3)|1|
|CTS|UART[0-5]_CTSn|I|Clear to send(4)|HiZ|
|RTS|UART[0-5]_RTSn|O|Request to send(5)|1|
|||**UART1 Modem Signals**|||
|DCD|UART1_DCDn|I|Data Carrier Detect(6)|HiZ|
|DSR|UART1_DSRn|I|Data Set Ready(7)|HiZ|
|DTR|UART1_DTRn|O|Data Terminal Ready(8)|1|
|RIN|UART1_RIN|I|Ring Indicator(9)|HiZ|



(1) I = Input; O = Output 

- (2) HiZ = High Impedance 

- (3) Because this pin is active high in IrDA mode and the output is muxed, this pin is set to low on reset (when the UART_MDR1[2-0] bit field is set to 0x7) and takes the defined inactive level of that signal corresponding to when and how the UART_MDR1 register is programmed; that is, the output is 1 (inactive for UART modem modes) and 0 (inactive for IrDA modes). 

- (4) Active-low modem status signal. Reading the UART_MSR[4] NCTS_STS bit checks the condition of CTS. Reading the UART_MSR[0] CTS_STS bit checks a change of state of CTS since the last read of the modem status register. The auto-CTS mode uses CTS to control the transmitter. 

- (5) When active (low), the module is ready to receive data. Setting the UART_MCR[1] RTS bit activates RTS signal, which becomes inactive as the result of a module reset, loopback mode, or clearing the UART_MCR[1] RTS bit. In auto-RTS mode, RTS signal becomes inactive as a result of the receiver threshold logic. 

- (6) Active-low modem status signal. The condition of DCD can be checked by reading the UART_MSR[7] NCD_STS bit. Any change in its state can be detected by reading the UART_MSR[3] DCD_STS bit. 

- (7) Active-low modem status signal. Reading the UART_MSR[5] NDSR_STS bit checks the condition of DSR. Reading the UART_MSR[1] DSR_STS bit checks a change of state of DSR since the last read of the UART_MSR register. 

- (8) When active (low), this signal informs the modem that the module is ready to communicate. It is activated by setting the UART_MCR[0] DTR bit. 

- (9) Active-low modem status signal. The condition of RIN can be checked by reading the UART_MSR[6] NRI_STS bit. Any change in its state can be detected by reading the UART_MSR[2] RI_STS bit. 

## **Note** 

For more information about device level signals (pull-up/down resistors, buffer type, multiplexing and others), see tables _Pin Attributes_ and _Pin Multiplexing_ in the device-specific Data sheet. 

## _**13.1.4.2.1.3 UART Protocol and Data Format**_ 

The UART device operates in three modes: 

- UART 16× (<= 230.4 kbps) 

- UART 16× with autobauding (>= 1200 bps and <= 115.2 kbps) 

- UART 13× (>= 460.8 kbps) 

## **CAUTION** 

To be used as a UART, the operating mode must be programmed appropriately in the UART_MDR1[2-0] MODE_SELECT bit field to select UART, IrDA, or CIR mode, and the UART_MDR3[4] DIR_EN bit field to select RS-485 mode. 

The UART uses a wired interface for serial communication with a remote device. 

The UART is functionally compatible with the TL16C750 UART and earlier designs such as the TL16C550. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1199 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

Figure 13-48 shows the UART frame data format. 

**==> picture [436 x 92] intentionally omitted <==**

**----- Start of picture text -----**<br>
Start-bit 5, 6, 7, or 8 bits of data according to UART_LCR register Parity bit 1 or 2<br>(see stop-bits<br>UART_LCR according<br>register)<br>to UART_LCR<br>register<br>**----- End of picture text -----**<br>


**==> picture [18 x 4] intentionally omitted <==**

**----- Start of picture text -----**<br>
uart-005<br>**----- End of picture text -----**<br>


**Figure 13-48. UART Frame Data Format** 

## _**13.1.4.2.2 RS-485 Functional Interfaces**_ 

## _**13.1.4.2.2.1 System Using RS-485 Communication**_ 

The RS-485 network physical layer consists of two-wire differential bus, usually twisted pair. External RS-485 transceiver IC is needed to access a RS-485 bus by the RS-485 mode. Figure 13-49 shows an example connection of UART in RS-485 mode. 

**==> picture [456 x 134] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>     UART[0-5] RS-485 RS-485 transceiver VCC RS-485 portDevice with<br>RX UART[0-5]_RXD R R RFS<br>RE A A<br>DIR UART[0-5]_RTSn DE B RT<br>B<br>TX UART[0-5]_TXD D D RFS<br>GND<br>**----- End of picture text -----**<br>


**==> picture [16 x 4] intentionally omitted <==**

**----- Start of picture text -----**<br>
uart-037<br>**----- End of picture text -----**<br>


## **Figure 13-49. RS-485 Mode Interface Signals** 

## _**13.1.4.2.2.2 RS-485 Interface Description**_ 

Table 13-64 lists the RS-485 interface input/output (I/O) signals. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1200 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-64. UART I/O Signals (RS-485 Mode)** 

|**Module Pin**|**Device Level Signal**|**I/O**(1)|**Description**|**Module Pin Reset Value**(2)|
|---|---|---|---|---|
||||**UART[0-5]**||
|RX|UART[0-5]_RXD|I|Serial data input|HiZ|
|TX|UART[0-5]_TXD|O|Serial data output|1|
|DIR|UART[0-5]_RTSn|O|RS-485 Direction|1|



(1) I = Input; O = Output 

(2) HiZ = High Impedance 

## **Note** 

For more information about device level signals (pull-up/down resistors, buffer type, multiplexing and others), see tables _Pin Attributes_ and _Pin Multiplexing_ in the device-specific Data sheet. 

## _**13.1.4.2.3 IrDA Functional Interfaces**_ 

## _**13.1.4.2.3.1 System Using IrDA Communication Protocol**_ 

Figure 13-50 shows an example connection of UART0 to an external infrared transceiver in the IrDA modes (FIR, SIR, and MIR). 

**==> picture [411 x 150] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>     UART[0-5] IrDA transceiver<br>IrDA<br>UART[0-5]_TXD<br>TXTX RX<br>UART[0-5]_RXD<br>RX TX<br>UART[0-5]_RTSn<br>SD SD<br>**----- End of picture text -----**<br>


**Figure 13-50. IrDA Mode Interface Signals** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1201 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.4.2.3.2 IrDA Interface Description**_ 

Table 13-65 lists the IrDA interface I/O signals. 

**Table 13-65. UART I/O Signals (IrDA Mode)** 

|**Module Pin**|**Device Level Signal**|**I/O**(1)|**Description**|**Module Pin Reset**|
|---|---|---|---|---|
|||||**Value**(2)|
||||**UART[0-5]**||
|RX|UART[0-5]_RXD|I|Serial data input|HiZ|
|TX|UART[0-5]_TXD|O|Serial data output in IrDA modes (SIR, MIR, and FIR).(3)|0|
|SD|UART[0-5]_RTSn|O|SD mode is used to configure the transceivers.(4)|1|



(1) I = Input; O = Output 

(2) HiZ = High Impedance 

(3) In other modes, this pin is set to the reset value (inactive state). 

(4) The SD pinout (see UART_ACREG[6] SD_MOD bit). 

## **Note** 

For more information about device level signals (pull-up/down resistors, buffer type, multiplexing and others), see tables _Pin Attributes_ and _Pin Multiplexing_ in the device-specific Data sheet. 

## _**13.1.4.2.3.3 IrDA Protocol and Data Format**_ 

## _**13.1.4.2.3.3.1 SIR Mode**_ 

In SIR mode, data is transferred between the Host CPU and peripheral devices at speeds of up to 115200 baud. A SIR transmit frame begins with start flags (a single 0xC0, a multiple 0xC0, or a single 0xC0 preceded by a number of 0xFF flags), followed by frame data and a CRC-16, and ends with a stop flag (0xC1). 

The bit format for a single word uses 1 start-bit, 8 data bits, and 1 stop-bit, and is unaffected by the use and settings of the UART_LCR register. 

The UART_BLR[6] XBOF_TYPE bit selects whether the 0xC0 or 0xFF start patterns are used when multiple start flags are required. 

The SIR transmit state-machine attaches start flags, CRC-16, and stop flags, and checks the outgoing data to establish whether data transparency is required. 

The SIR transparency is carried out if the outgoing data between the start and stop flags contains 0xC0, 0xC1, or 0x7D. If one of these start flags is about to be transmitted, the SIR state-machine sends an escape character (0x7D), inverts the fifth bit of the real data to be sent, and then sends this data immediately after the 0x7D character. 

The SIR receive state-machine recovers the receive clock, removes the start flags and any transparency from the incoming data, and determines the frame boundary with reception of the stop flag. The SIR state-machine also checks for errors such as a frame abort (0x7D character followed immediately by a 0xC1 stop flag without transparency), a CRC error, or a frame-length error. At the end of a frame reception, the Host CPU reads the line status register (UART_LSR_IRDA) to find possible errors of the received frame. 

## **Note** 

The module can transmit and receive data, but when the device is transmitting, the IR RX circuitry is automatically disabled by hardware. See the description of the UART_ACREG[5] DIS_IR_RX bit. This applies to all three modes: SIR, MIR, and FIR. 

Infrared output in SIR mode can be 1.6-µs or 3/16 encoding, selected by the UART_ACREG[7] PULSE_TYPE bit. In 1.6-µs encoding, the infrared pulse width is 1.6 µs; and in 3/16th encoding, the infrared pulse width is 3/16th of a bit duration (1/baud rate). 

1202 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

For back-to-back frames, the transmitting device must send at least two start flags at the start of each frame. 

**==> picture [24 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
Note<br>**----- End of picture text -----**<br>


Reception supports variable-length stop-bits. 

## _**13.1.4.2.3.3.1.1 Frame Format**_ 

Figure 13-51 shows the IrDA SIR frame format. 

**==> picture [337 x 139] intentionally omitted <==**

**----- Start of picture text -----**<br>
2 × 8<br>N × 8 bits 8 bits 8 bits 8 bits M × 8 bits 8 bits<br>bits<br>xBOF BOF A C I CRC EOF<br>FIFO data<br>uart-006<br>**----- End of picture text -----**<br>


**Figure 13-51. IrDA SIR Frame Format** 

The CRC is applied on the address (A), control (C), and information (I) bytes. 

**==> picture [24 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
Note<br>**----- End of picture text -----**<br>


The two words of CRC are written to the FIFO in reception. 

## _**13.1.4.2.3.3.1.2 Asynchronous Transparency**_ 

Before transmitting a byte, the UART IrDA controller examines each byte of the payload and the CRC field (between BOF and EOF). For each byte equal to 0xC0 (BOF), 0xC1 (EOF), or 0x7D (control escape), the controller performs certain tasks: 

- In transmission: 

   - Inserts a control escape (CE) byte preceding the byte 

   - Complements bit 5 of the byte (that is, exclusive ORs the byte with 0x20) 

The byte sent for the CRC computation is the initial byte written in the TX FIFO (before the XOR with 0x20). 

- In reception: 

For the A, C, I, and CRC fields: 

- Compares the byte with the CE byte; if they are not equal, sends the byte to the CRC detector and stores it in the RX FIFO. 

- If the byte is equal to the CE byte, discards the CE byte 

- Complements bit 5 of the byte following the CE 

- Sends the complemented byte to the CRC detector and stores it in the RX FIFO 

## _**13.1.4.2.3.3.1.3 Abort Sequence**_ 

The transmitter can prematurely close a frame (abort) by sending the sequence 0x7DC1. The abort pattern closes the frame without a CRC field or an ending flag. 

When a 0x7D character that is followed immediately by a 0xC1 character is received without transparency, the receiver treats the frame as an aborted frame. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1203 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.4.2.3.3.1.4 Pulse Shaping**_ 

The SIR mode supports the 3/16 and the 1.6-µs pulse duration methods. The UART_ACREG[7] PULSE_TYPE bit selects the pulse-width method in transmit mode. 

## _**13.1.4.2.3.3.1.5 Encoder**_ 

Serial data from the transmit state-machine are encoded to transmit data to the optoelectronics. While the TX FIFO output is high, the TX line is always low, and the counter used to form a pulse on TX is cleared continuously. 

After the TX FIFO output resets to 0, TX rises on the falling edge of the seventh 16XCLK. On the falling edge of the tenth 16XCLK pulse, TX falls, creating a 3-clock-wide pulse. While the TX FIFO output stays low, a pulse is transmitted during the seventh clock to the tenth clock of each 16-clock bit cycle. 

Figure 13-52 shows the IrDA SIR encoding mechanism. 

**==> picture [430 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
TX FIFO<br>output<br>16XCLK<br>1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16<br>TX<br>uart-007<br>**----- End of picture text -----**<br>


**Figure 13-52. IrDA SIR Encoding Mechanism** 

## _**13.1.4.2.3.3.1.6 Decoder**_ 

After reset, the RX FIFO input is high and the 4-bit counter is cleared. When a rising edge is detected on RX, the RX FIFO input falls on the next rising edge of 16XCLK with sufficient setup time. The RX FIFO input stays low for 16 cycles (16XCLK) and then returns to high as required by the IrDA specification. As long as no pulses (rising edges) are detected on the RX, the RX FIFO input remains high. 

Figure 13-53 shows the IrDA SIR decoding mechanism. 

**==> picture [448 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX output of<br>transceiver on RX<br>Internal RX signal<br>(UART_MDR2[6]<br>IRRXINVERT bit set to 1)<br>16XCLK<br>1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16<br>RX FIFO input<br>**----- End of picture text -----**<br>


**==> picture [17 x 4] intentionally omitted <==**

**----- Start of picture text -----**<br>
uart-008<br>**----- End of picture text -----**<br>


**Figure 13-53. IrDA SIR Decoding Mechanism** 

1204 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

The module can transmit and receive data, but when the device is transmitting, the IR RX circuitry is automatically disabled by hardware. The operation of the RX input can be disabled using the UART_ACREG[5] DIS_IR_RX bit. The UART_MDR2[6] IRRXINVERT bit can invert the signal from the transceiver (RX) pin to the IR RX logic in the UART. This inversion is performed by default. 

## _**13.1.4.2.3.3.1.7 IR Address Checking**_ 

In all IR modes, when address checking is enabled by setting the UART_EFR[1-0] bit field (see Table 13-66), only frames intended for the device are written to the RX FIFO. This is to avoid receiving frames not meant for this device in a multipoint infrared environment. To program two frame addresses that the UARTi receives in IrDA mode, use the UART_XON1_ADDR1[7-0] and UART_XON2_ADDR2[7-0] bit fields. 

**Table 13-66. UART_EFR[1-0] IR Address Checking Options** 

|**UART_EFR[1]**|**UART_EFR[0]**|**IR Address Checking**|
|---|---|---|
|0|0|All address-checking operations disabled|
|0|1|Only address 1 checking enabled|
|1|0|Only address 2 checking enabled|
|1|1|All address-checking operations enabled|



## _**13.1.4.2.3.3.2 SIR Free-Format Mode**_ 

To allow complete software flexibility when transmitting and receiving infrared data packets, the SIR free-format (FF) mode is a subfunction of the existing SIR mode. In FF mode, all frames going to and from the FIFO buffers are untouched with respect to appending and removing control characters and CRC values. 

The FF mode corresponds to a UART mode with a pulse modulation of 3/16 of baud rate pulse width. 

For example, a normal SIR packet has BOF control and CRC error-checking data appended (transmitting) or removed (receiving) from the data going to and from the FIFOs. 

Figure 13-54 shows SIR FF mode. 

**==> picture [278 x 110] intentionally omitted <==**

**----- Start of picture text -----**<br>
M × 8 bits<br>Free format<br>FIFO data<br>uart-009<br>**----- End of picture text -----**<br>


**Figure 13-54. SIR FF Mode** 

In SIR FF mode, the Host CPU software must construct (that is, encode and decode) the entire FIFO data packet. 

The SIR Free Format mode is selected by setting the module in UART mode (MDR1[2:0] = 000) and the MDR2[3] register bit to one to allow the pulse shaping. As the bit format is to remain the same, some UART mode configuration registers need to be set at specific value: 

- LCR[1:0] = "11" (8 data bits) 

- LCR[2] = 0 (2 stop bit) 

- LCR[3] = 0 (no parity) 

- ACREG[7] = 0 (3/16 of baud-rate pulse width) 

The features defined through MDR2[6] and ACREG[5] are also supported, however: 

- All other configuration registers need to be at the reset value 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1205 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- The same UART mode interrupts used for the SIR FF mode are not necessarily relevant (XOFF, RTS, CETS, Modem Status Register) 

## _**13.1.4.2.3.3.3 MIR Mode**_ 

In MIR mode, data is transferred between the Host CPU and the peripheral devices at 0.576 Mbps or 1.152 Mbps. A MIR transmit frame starts with at least two start flags, followed by a frame data and a CRC-16, and ends with a stop flag (see Figure 13-55). 

**==> picture [378 x 141] intentionally omitted <==**

**----- Start of picture text -----**<br>
xn<br>Start flags Start flag Frame data CRC-16 Stop flag<br>Bit-stuffing<br>.............0111110111110110........................................................<br>5x1 5x1<br>FIFO data<br>..............01111111111110........................................................<br>uart-010<br>**----- End of picture text -----**<br>


**Figure 13-55. MIR Transmit Frame Format** 

On transmit, the MIR state-machine attaches start flags, a CRC-16, and stop flags, as in SIR mode. All fields are transmitted least-significant bit (LSB) of each byte first. 

In MIR mode: 

- The state-machine looks for consecutive 1s in the frame data and automatically inserts 0 after five consecutive 1s (this is called bit-stuffing). 

- 0x7E is used for start and stop flags (unambiguously, not data, because of bit-stuffing). 

- An abort sequence requires a minimum of seven consecutive 1s (unambiguously, not data, because of bit-stuffing). 

- Back-to-back frames are allowed with three or more stop flags between them. If two consecutive frames are not back to back, the gap between the last stop flag of the first frame and the start flag of the second frame must be separated by at least seven bit durations. 

On receive, the MIR receive state-machine recovers the receive clock, removes the start flags, destuffs the incoming data, and determines the frame boundary with reception of the stop flag. The state-machine also checks for errors such as frame abort, CRC error, and frame-length error. At the end of a frame reception, the Host CPU reads the line status register (UART_LSR_IRDA) to detect errors of the received frame. 

The module can transmit and receive data, but when the device is transmitting, the IR RX circuitry is automatically disabled by hardware. 

## _**13.1.4.2.3.3.3.1 MIR Encoder/Decoder**_ 

To meet the MIR baud rate tolerance of 0.1 percent with a 48-MHz clock input, a 42-41-42 encoding/decoding adjustment is performed. The reference start point is the first start flag, and the 42-41-42 cyclic pattern is repeated until the stop flag is sent or detected. 

The jitter created this way is within MIR tolerances. The pulse width is not exactly 1/4, but it is within the tolerances defined by IrDA specifications. 

Figure 13-56 shows the MIR baud rate adjustment mechanism. 

1206 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [381 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
Baud adjustment cyclic pattern (3 MIR periods)<br>42x 41x 42x 10x<br>TX<br>Ideal edge<br>placement<br>Jitter Jitter<br>RX<br>(inverter enabled)<br>Sampling<br>window<br>42x 41x 42x<br>**----- End of picture text -----**<br>


**==> picture [17 x 4] intentionally omitted <==**

**----- Start of picture text -----**<br>
uart-011<br>**----- End of picture text -----**<br>


**Figure 13-56. MIR Baud Rate Adjustment Mechanism** 

## _**13.1.4.2.3.3.3.2 SIP Generation**_ 

In the MIR and FIR operation modes, the transmitter must send a serial infrared interaction pulse (SIP) at least once every 500 ms. The SIP informs slow devices (operating in SIR mode) that the medium is occupied. Figure 13-57 shows the SIP. 

**==> picture [155 x 96] intentionally omitted <==**

**----- Start of picture text -----**<br>
8. 7 �s<br>1. 6 �s<br>S IP<br>uart-012<br>**----- End of picture text -----**<br>


**Figure 13-57. SIP** 

When the SIP_MODE bit of the Mode Definition Register 1 is equal to 1 (MDR1[6]), the TX state machine will always send one SIP at the end of the transmission frame. When MDR1[6] is equal to 0, the transmission of the SIP depends on the SEND_SIP bit of the Auxiliary Control Register (ACREG[3]). The system (Host CPU) can set ACREG[3] at least once every 500ms. The advantage of this approach over the default approach is that the TX state machine does not need to send the SIP at the end of each frame, which may reduce the overhead required. 

## _**13.1.4.2.3.3.4 FIR Mode**_ 

In FIR mode, data is transferred between the Host CPU and the peripheral devices at 4 Mbps. A FIR transmit frame starts with a preamble that is followed by a start flag, frame data, CRC-32, and ends with a stop flag. 

Figure 13-58 shows the FIR transmit frame format. 

**Figure 13-58. FIR Transmit Frame Format** 

Preamble (16x) Start flag Frame data CRC-32 Stop flag 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1207 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

On transmit, the FIR transmit state-machine attaches the preamble, start flag, CRC-32, and stop flag. An abort sequence requires at least two transmissions of 0000. Back-to-back frames are allowed, but each frame must be complete. 

The state-machine also encodes the transmit data into 4-PPM format (see Table 13-67) and generates the SIP (see Section 13.1.4.2.3.3.3.2, _SIP Generation_ ). 

**Table 13-67. 4-PPM Format** 

|**Data Bit Pair (Bin)**|**4-PPM Data Symbol (Bin)**|
|---|---|
|00|1000|
|01|0100|
|10|0010|
|11|0001|



The four symbols described in Table 13-67 are the legal, encoded data symbols. All other combinations are illegal for encoding data. Some of these illegal symbols are used in the definition of the preamble, start flag, and stop flag because they are unambiguously not data (see Table 13-68). 

**Table 13-68. FIR Preamble, Start Flag, and Stop Flag** 

|**Frame Part**||**Transmitted Frame (Bin)**|
|---|---|---|
||Preamble|1000 0000 1010 1000 (16 repeated transmissions)|
||Start flag|0000 1100 0000 1100 0110 0000 0110 0000|
||Stop flag|0000 1100 0000 1100 0000 0110 0000 0110|



All fields are transmitted LSBs of each byte first (see Table 13-69). 

**Table 13-69. FIR Data Byte Transmission Order Example** 

|**Data Byte (Hex)**|**Data Byte Pair (Bin)**<br>**4-PPM Data Symbol (Bin)**<br>**Transmission Order**|
|---|---|
|0x0B|00<br>1000<br>4|
||00<br>1000<br>3|
||10<br>0010<br>2|
||11<br>0001<br>1|



On receive, the FIR receive state-machine recovers the receive clock, removes the preamble and the start flag, decodes the 4-PPM incoming data, and determines the frame boundary with reception of the stop flag. The state-machine also checks for errors such as illegal symbol, CRC error, and frame-length error. At the end of a frame reception, the Host CPU reads the line status register (UART_LSR_IRDA) to detect errors of the received frame. 

The module can transmit and receive data, but when the device is transmitting, the IR RX circuitry is automatically disabled by hardware. 

## _**13.1.4.2.4 CIR Functional Interfaces**_ 

## _**13.1.4.2.4.1 System Using CIR Communication Protocol With Remote Control**_ 

All UART modules can be connected to an external infrared transceiver in CIR mode. Figure 13-59 shows an example connection of UART0 in CIR mode. 

1208 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [411 x 149] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>     UART[0-5]  CIR transceiver<br> CIR<br>UART[0-5]_TXD<br>TXTX RX<br>UART[0-5]_RXD<br>RX TX<br>UART[0-5]_RTSn<br>SD SD<br>**----- End of picture text -----**<br>


## **Figure 13-59. CIR Mode Interface Signals** 

## _**13.1.4.2.4.2 CIR Interface Description**_ 

Table 13-70 lists the CIR interface I/O signals. 

**Table 13-70. UART I/O Signals (CIR Mode)** 

||**Module Pin**|**Device Level Signal**|**I/O**(1)|**Description**|**Module Pin Reset**|
|---|---|---|---|---|---|
||||||**Value**(2)|
|||||**UART[0-5]**||
|RX||UART[0-5]_RXD|I|Serial data input|HiZ|
|TX||UART[0-5]_TXD|O|Serial data output in CIR mode.(3)|0|
|SD||UART[0-5]_RTSn|O|SD mode is used to configure the transceivers.(4)|1|



(1) I = Input; O = Output 

(2) HiZ = High Impedance 

(3) In other modes, this pin is set to the reset value (inactive state). 

(4) The SD pinout is an inverted value of the UART_ACREG[6] SD_MOD bit. 

## **Note** 

For more information about device level signals (pull-up/down resistors, buffer type, multiplexing and others), see tables _Pin Attributes_ and _Pin Multiplexing_ in the device-specific Data sheet. 

## _**13.1.4.2.4.3 CIR Protocol and Data Format**_ 

In CIR mode, the infrared operation functions as a programmable (universal) remote control. 

The CIR mode uses a variable PWM technique (based on multiples of a programmable _t_ period) to encompass the various formats of infrared encoding for remote-control applications. The CIR logic transmits data packets based on user-defined frame structure and packet content. 

## _**13.1.4.2.4.3.1 Carrier Modulation**_ 

Each modulated pulse that constitutes a digit is a train of on/off pulses (see Figure 13-60). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1209 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [324 x 306] intentionally omitted <==**

**----- Start of picture text -----**<br>
01 011<br>t t t t t<br>Carrier<br>Nominal  t<br>Modulation pulse<br>Effective  t  length<br>uart-014<br>**----- End of picture text -----**<br>


**Figure 13-60. CIR Pulse Modulation** 

## _**13.1.4.2.4.3.2 Pulse Duty Cycle**_ 

The programmer can choose one of four duty cycles for modulation pulses by setting the appropriate value in the UART_MDR2[5-4] CIR_PULSE_MODE bit field (1/4, 1/3, 5/12, or 1/2). 

Figure 13-61 shows the CIR modulation duty cycles. 

**==> picture [450 x 185] intentionally omitted <==**

**----- Start of picture text -----**<br>
12x baud<br>multiple<br>0.25 or 1/4 duty cycle pulse<br>0.33 or 1/3 duty cycle pulse<br>0.42 or 5/12 duty cycle pulse<br>0.5 or 1/2 duty cycle pulse<br>uart-015<br>for<br>used generation<br>clock pulse<br>Internal modulation<br>**----- End of picture text -----**<br>


**Figure 13-61. CIR Modulation Duty Cycle** 

The transmission logic ensures that all pulses are transmitted completely (no cutoff during transmission). While transmitting continuous bytes back-to-back, no delay is inserted between 2 transmitted bytes. Thus, software must handle the delay between consecutively transmitted bytes if the receiving end requires it. 

1210 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.1.4.2.4.3.3 Consumer IR Encoding/Decoding**_ 

There are two methods of encoding for remote-control applications: 

- Pulse duration encoding (time-extended bit forms): A variable pulse distance, or duration, in which the difference between logic 1 and logic 0 is the length of the pulse width 

- Biphase encoding: The encoding of logic 0 and logic 1 is in the change of signal level from 1 to 0 or 0 to 1, respectively. 

Japanese manufacturers favor pulse duration encoding; European manufacturers favor biphase encoding. 

CIR mode uses a completely flexible free-format encoding in which 1 is transmitted from the TX FIFO as a modulated pulse with duration _t_ . 

Similarly, 0 is transmitted as a blank duration T. The Host CPU constructs and deciphers the protocol of the data. For example, the RC-5 protocol using Manchester encoding can be emulated as using a 01 pair for 1 and a 10 pair for 0 (see Figure 13-62). 

**==> picture [210 x 179] intentionally omitted <==**

**----- Start of picture text -----**<br>
RC-5 bit encoding<br>t t t t<br>1 0 0 1<br>1.778 ms 1.778 ms<br>0 1<br>uart-016<br>**----- End of picture text -----**<br>


**Figure 13-62. UART RC-5 Bit Encoding** 

Because CIR mode logic does not impose a fixed format for infrared packets of data, the Host CPU software can define the format using simple data structures that are then modulated into an industry standard, such as RC-5 or SIRC. To send a sequence of 0101 in RC-5, the Host CPU software must write an 8-bit binary character of 10011001 to the data FIFO of the UART. 

For SIRC, the modulation length (multiples of _t_ ) is used to distinguish between 1 and 0. The subsequent SIRC digits show the difference in encoding between this and, for example, RC-5. The pulse width is extended for one digit. 

Figure 13-63 shows SIRC bit encoding. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1211 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [248 x 182] intentionally omitted <==**

**----- Start of picture text -----**<br>
SIRC bit encoding<br>t t t t t<br>0.6 ms 0.6 ms 0.6 ms 1.2 ms<br>0 1<br>uart-017<br>**----- End of picture text -----**<br>


**Figure 13-63. UART SIRC Bit Encoding** 

To construct comprehensive packets constituting remote-control commands, the Host CPU software must combine a number of 8-bit data characters in a sequence that follows one of the universally accepted formats. 

Figure 13-64 shows a standard RC-5 frame as detected by UART in CIR mode (the SIRC format follows this). Each field in RC-5 can be considered as two _t_ pulses (digital bits) from the TX FIFO. 

|S1|S2|T|A4|A3|A2|A1|A0|C5|C4|C3|C2|C1|C0|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|



**Figure 13-64. UART RC-5 Standard Packet Format** 

Where: 

|S1, S2:|Start-bits (always 1)|
|---|---|
|T:|Toggle bit|
|A4..A0:|Address (or system) bits|
|C5..C0:|Command bits|



The toggle bit T changes when a new command is transmitted to detect when the same key is pressed twice (effectively receiving the same data from the host consecutively). A brief delay in the transmission of the same command is detected by the use of the toggle bit because a code is sent while the Host CPU transmits characters to the UART for transmission. The address bits define the machine or device for which the infrared transmission is intended, and the command defines the operation. 

To accommodate an extended RC-5 format, the S2 bit is replaced by an additional command bit (C6) that lets the command range increase to 7 bits. This format is known as the extended RC-5 format. 

The SIRC encoding uses the duration of modulation for mark and space; therefore, the duration of data bits in the standard frame length varies. 

Figure 13-65 shows the packet format and bit encoding. As Figure 13-66 shows, 1 start-bit of 2.4 ms and control codes are followed by data that constitute the entire frame. 

**==> picture [356 x 43] intentionally omitted <==**

**----- Start of picture text -----**<br>
S C0 C1 C2 C3 C4 C5 C6 D0 D1 D2 D3 D4<br>uart-019<br>**----- End of picture text -----**<br>


**Figure 13-65. UART SIRC Packet Format** 

1212 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

The encoding must take a standard duration, but the contents of the data can vary. This implies that the control software for sending and receiving data packets must exercise a scheme of interpacket delay, where successive packets can be sent only after a real-time delay expires. 

**==> picture [440 x 80] intentionally omitted <==**

**----- Start of picture text -----**<br>
Start-bit 0 1 T Frame space<br>(variable)<br>2.4 ms 1.2 ms 1.8 ms<br>Complete frame<br>(45 ms)<br>uart-020<br>**----- End of picture text -----**<br>


**Figure 13-66. UART SIRC Bit Transmission Example** 

## **Note** 

This document does not describe all encoding methods and techniques; the previous information discusses the considerations required to employ different encoding methods for different industrystandard protocols. See industry-standard documentation for specific methods of encoding and protocol use. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1213 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.1.4.3 UART Integration** 

There are 6x UART modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [500 x 352] intentionally omitted <==**

**==> picture [63 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
# = 0, 1, 2, 3, 4, 5<br>**----- End of picture text -----**<br>


**Figure 13-67. UART Integration** 

The tables below summarize the device integration details of UART# (where # = 0, 1, 2, 3, 4, 5) in the device. 

**Table 13-71.** _**UART**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|UART0|✓|PERI VBUSP Interconnect|
|UART1|✓|PERI VBUSP Interconnect|
|UART2|✓|PERI VBUSP Interconnect|
|UART3|✓|PERI VBUSP Interconnect|
|UART4|✓|PERI VBUSP Interconnect|
|UART5|✓|PERI VBUSP Interconnect|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1214 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-72.** _**UART**_ **Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|UART0|UART0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART0 VBUS Clock|
||UART0_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART0 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0 (not supported)|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||
|UART1|UART1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART1 VBUS Clock|
||UART1_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART1 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0 (not supported)|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1215 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-72.** _**UART**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|UART2|UART2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART2 VBUS Clock|
||UART2_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART2 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0 (not supported)|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||
|UART3|UART3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART3 VBUS Clock|
||UART3_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART3 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0 (not supported)|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



1216 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-72.** _**UART**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|UART4|UART4_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART4 VBUS Clock|
||UART4_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART4 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0 (not supported)|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||
|UART5|UART5_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART5 VBUS Clock|
||UART5_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART5 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0 (not supported)|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



**Table 13-73.** _**UART**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|UART0|UART0_RST(VBUSP_R<br>STn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART0 Asynchronous Reset|
|UART1|UART1_RST(VBUSP_R<br>STn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART1 Asynchronous Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1217 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-73.** _**UART**_ **Resets (continued)** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|UART2|UART2_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART2 Asynchronous Reset|
|UART3|UART3_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART3 Asynchronous Reset|
|UART4|UART4_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART4 Asynchronous Reset|
|UART5|UART5_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART5 Asynchronous Reset|



**Table 13-74.** _**UART**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|UART0|uart0_int_req|uart0_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|UART0 IP Status Information|
|UART1|uart1_int_req|uart1_int_req|ALL R5FSS Cores<br>PRU-ICSS Core||UART1 IP Status Information|
|UART2|uart2_int_req|uart2_int_req|ALL R5FSS Cores<br>PRU-ICSS Core||UART2 IP Status Information|
|UART3|uart3_int_req|uart4_int_req|ALL R5FSS Cores<br>PRU-ICSS Core||UART3 IP Status Information|
|UART4|uart4_int_req|uart4_int_req|ALL R5FSS Cores<br>PRU-ICSS Core||UART4 IP Status Information|
|UART5|uart5_int_req|uart5_int_req|ALL R5FSS Cores<br>PRU-ICSS Core||UART5 IP Status Information|



**Table 13-75.** _**UART**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|UART0|UART0_DMA_0|UART0_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)|Level|UART0 DMA Request|
||UART0_DMA_1|UART0_dma_req[1]||||
|UART1|UART1_DMA_0|UART1_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)|Level|UART1 DMA Request|
||UART1_DMA_1|UART1_dma_req[1]||||
|UART2|UART2_DMA_0|UART2_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)|Level|UART2 DMA Request|
||UART2_DMA_1|UART2_dma_req[1]||||
|UART3|UART3_DMA_0|UART3_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)|Level|UART3 DMA Request|
||UART3_DMA_1|UART3_dma_req[1]||||
|UART4|UART4_DMA_0|UART4_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)|Level|UART4 DMA Request|
||UART4_DMA_1|UART4_dma_req[1]||||
|UART5|UART5_DMA_0|UART5_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)|Level|UART5 DMA Request|
||UART5_DMA_1|UART5_dma_req[1]||||



1218 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1219 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.1.4.4 UART Functional Description** 

## _**13.1.4.4.1 UART Block Diagram**_ 

The UART module can be divided into three main blocks: 

- FIFO management 

- Mode selection 

- Protocol formatting 

FIFO management is common to all functions and enables the transmission and reception of data from the host processor point of view. 

There are two modes: 

- Function mode: Routes the data to the chosen function (UART, RS-485, IrDA, or CIR) and enables the mechanism corresponding to the chosen function. 

- Register mode: Enables conditional access to registers. 

For more information about mode configuration, see _Mode Selection_ . 

Protocol formatting has three subcategories: 

- Clock generation: The 48-MHz input clock generates all necessary clocks. 

- Data formatting: Each function uses a dedicated state-machine that is responsible for the transition between FIFO data and the associated frame data. 

- Interrupt management: Different interrupt types are generated depending on the chosen function. In each mode, when an interrupt is generated, the UART_IIR_UART register indicates the interrupt type. 

   - UART mode interrupts: Seven interrupts prioritized in six different levels 

   - IrDA mode interrupts: Eight interrupts. The interrupt line is activated when any interrupt is generated (there is no priority). 

   - CIR mode interrupts: A subset of existing IrDA mode interrupts is used. 

In parallel with these functional blocks, a power-saving strategy exists for each function. 

The UART block diagram is shown below. 

1220 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [480 x 253] intentionally omitted <==**

**----- Start of picture text -----**<br>
UARTi_DMA0 Clock DATA Interrupt UARTi_IRQ<br>Mode selection  generation formatting  management<br>UART_MDR1[2-0]<br>MODE_SELECT UART mode<br>UART_MDR3[4] UART clock UART data UART interrupt<br>DIR_EN generation formatting management<br>FIFO FIFO UART/RS-485 pins<br>Transmit Transmit<br>interrupt DMA request<br>generation generation<br>FIFO Transmit IrDA mode<br>IrDA  SIR/MIR/FIR IrDA interrupt<br>(SIR/MIR/FIR) data formatting management<br>FIFO management clock generation IrDA pins<br>FIFO Receive<br>FIFO Receive FIFO CIR mode<br>Transmit<br>interrupt DMA request CIR clock CIR data CIR interrupt<br>generation generation generation formatting management<br>CIR pins<br>UARTi_DMA1<br>PERI_VBUSP Interconnect<br>**----- End of picture text -----**<br>


**Figure 13-68. UART Functional Block Diagram** 

## _**13.1.4.4.2 UART Clock Configuration**_ 

Each UART uses a 48-MHz functional clock for its logic and to generate external interface signals. Each UART uses an interface clock for register accesses. 

## _**13.1.4.4.3 UART Software Reset**_ 

The UART_SYSC[1] SOFTRESET bit controls the software reset; setting this bit to 1 triggers a software reset functionally equivalent to hardware reset. 

## _**13.1.4.4.3.1 Independent TX/RX**_ 

The receiver and transmitter are enabled by default after reset. Software can choose to disable, re-enable or to reset either the RX or the TX side independently of the other through the UART_ECR register. 

## _**13.1.4.4.4 UART Power Management**_ 

## _**13.1.4.4.4.1 UART Mode Power Management**_ 

## _**13.1.4.4.4.1.1 Module Power Saving**_ 

In UART modes, sleep mode is enabled by setting the UART_IER_UART[4] SLEEP_MODE bit to 1 (when the UART_EFR[4] ENHANCED_EN bit is set to 1). 

Sleep mode is entered when all of the following conditions exist: 

- The serial data input line, RX, is idle. 

- The TX FIFO and TX shift register are empty. 

- The RX FIFO is empty. 

- The only pending interrupts are THR interrupts. 

Sleep mode is a good way to lower UART power consumption, but this state can be achieved only when the UART is set to modem mode. Therefore, even if the UART has no key role functionally, it must be initialized in a functional mode to take advantage of sleep mode. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1221 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

In sleep mode, the module clock and baud rate clock are stopped internally. Because most registers are clocked by these clocks, this greatly reduces power consumption. The module wakes up when a change is detected on the RX line, when data is written to the TX FIFO, and when there is a change in the state of the modem input pins. 

An interrupt can be generated on a wake-up event by setting the UART_SCR[4] RX_CTS_WU_EN bit to 1. To understand how to manage the interrupt, see Section 13.1.4.4.5.1.2, _Wake-Up Interrupt_ . 

## **Note** 

There must be no writing to the divisor latches, UART_DLL and UART_DLH, to set the baud clock (BCLK) while in sleep mode. It is advisable to disable sleep mode using the UART_IER_UART[4] SLEEP_MODE bit before writing to the UART_DLL or UART_DLH register. 

## _**13.1.4.4.4.1.2 System Power Saving**_ 

Sleep and auto-idle modes are embedded power-saving features. Power-reduction techniques can be applied at the system level by shutting down certain internal clock and power domains of the device. 

For more information, see _Power_ , in the _Device Configuration_ . 

## _**13.1.4.4.4.2 IrDA Mode Power Management**_ 

## _**13.1.4.4.4.2.1 Module Power Saving**_ 

In IrDA modes, sleep mode is enabled by setting the UART_MDR1[3] IR_SLEEP bit to 1. 

Sleep mode is entered when all of the following conditions exist: 

- The serial data input line, RXD, is idle. 

- The TX FIFO and TX shift register are empty. 

- The RX FIFO is empty. 

- No interrupts are pending except THR interrupts. 

The module wakes up when a change is detected on the RXD line or when data is written to the TX FIFO. 

## _**13.1.4.4.4.2.2 System Power Saving**_ 

System power saving for the IrDA mode has the same function as for the UART mode (see Section 13.1.4.4.4.1.2, _System Power Saving_ ). 

## _**13.1.4.4.4.3 CIR Mode Power Management**_ 

## _**13.1.4.4.4.3.1 Module Power Saving**_ 

Module power saving for the CIR mode has the same function as for the IrDA mode (see Section 13.1.4.4.4.2.1, _Module Power Saving_ ). 

## _**13.1.4.4.4.3.2 System Power Saving**_ 

System power saving for the CIR mode has the same function as for the UART mode (see Section 13.1.4.4.4.1.2, _System Power Saving_ ). 

## _**13.1.4.4.4.4 Local Power Management**_ 

Table 13-76 describes power-management features available for the UART. 

## **Note** 

For information about source clock gating and the sleep/wake-up transitions description, see _Power_ , in the _Device Configuration_ . 

1222 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-76. UART Local Power-Management Features** 

|**Feature**|**Registers**|**Description**|
|---|---|---|
|Clock autogating|N/A|Feature not available|
|Peripheral idle modes|N/A|Feature not available|
|Clock activity|N/A|Feature not available|
|Controller standby|N/A|Feature not available|
|modes|||
|Global wake-up|UART_SYSC[2] ENAWAKEUP|This bit enables the wake-up feature at module level.|
|enable|||
|Wake-Up sources|N/A|Feature not available|
|enable|||



## _**13.1.4.4.5 UART Interrupt Requests**_ 

## _**13.1.4.4.5.1 UART Mode Interrupt Management**_ 

## _**13.1.4.4.5.1.1 UART Interrupts**_ 

The UART mode includes seven possible interrupts prioritized to six levels. 

When an interrupt is generated, the interrupt identification register (UART_IIR_UART) sets the UART_IIR_UART[0] IT_PENDING bit to 0 to indicate that an interrupt is pending, and indicates the type of interrupt through the UART_IIR_UART[5-1] bit field. Table 13-77 summarizes the interrupt control functions. 

**Table 13-77. UART Mode Interrupts** 

|**IIR[5:0]**|**Priority Level**|**Interrupt Type**|**Interrupt Source**|**Interrupt Reset Method**|
|---|---|---|---|---|
|000001|N/A|No Interrupt|N/A|N/A|
|000110|1|Receiver line|OE, FE, PE, or BI errors occur in|FE, PE, BI: Read the|
|||status|characters in the RX FIFO.|UART_RHR register. OE: Read the|
|||||UART_LSR_UART register.|
|001100|2|RX time-out|Stale data in RX FIFO|Read the UART_RHR register if|
|||||using the default timeout behavior:|
|||||EFR2[6]=0|
|||||Cleared by reading its value (IIR) if|
|||||using the periodic timeout behavior:|
|||||EFR2[6]=1|
|000100|2|RHR interrupt|DRDY (data ready) (FIFO disabled)|Read the UART_RHR register until the|
||||RX FIFO above trigger level (FIFO|interrupt condition disappears|
||||enabled)||
|000010|3|THR interrupt|TFE (THR empty) (FIFO disabled)|Write to the UART_THR until the|
||||TX FIFO below trigger level (FIFO|interrupt condition disappears|
||||enabled)||
|000000|4|Modem status|See the UART_MSR register.|Read the MSR register|
|010000|5|XOFF interrupt/|Receive XOFF characters/special|Receive XON character(s), if XOFF|
|||special character|character|interrupt/read of the UART_IIR_UART|
|||interrupt||register, if special character interrupt|
|100000|6|CTS, RTS|RTS pin or CTS pin change state from|Read the UART_IIR_UART register|
||||active (low) to inactive (high)||



For the receiver-line status interrupt, the UART_LSR_UART[7] RX_FIFO_STS bit generates the interrupt. 

For the XOFF interrupt, if an XOFF flow character detection caused the interrupt, the interrupt is cleared by an XON flow character detection. If special character detection caused the interrupt, the interrupt is cleared by a read of the UART_IIR_UART register. 

## _**13.1.4.4.5.1.2 Wake-Up Interrupt**_ 

Wake-up interrupt is a special interrupt that works differently from other interrupts. This interrupt is enabled when the RX_CTS_DSR_WAKE_UP_ENABLE bit of the Supplementary Control Register (SCR[4]) is set to 1. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1223 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

The IIR register is not modified when it occurs, SSR[1] must be checked to detect a wake-up event. When a wake-up event occurs, the only way to clear it is to reset SCR[4] to 0. Wake-up can also occur if the WER[7] TX_WAKEUP_EN is set to 1 and one of the following events occurs: 

1. THR interrupt is enabled and occurs (omitted if TX DMA request is enabled) 

2. TX DMA request is enabled and occurs 

3. TX_STATUS_IT is enabled and occurs (only IrDA and CIR modes). Cannot be used with THR Interrupt. 

## _**13.1.4.4.5.2 IrDA Mode Interrupt Management**_ 

## _**13.1.4.4.5.2.1 IrDA Interrupts**_ 

The IrDA function generates interrupts. All interrupts can be enabled and disabled by writing to the appropriate bit in the interrupt enable register (UART_IER_IRDA). The interrupt status of the device can be checked by reading the interrupt identification register (UART_IIR_IRDA). 

The UART, IrDA, and CIR modes have different interrupts in the UART module and, therefore, different UART_IER_IRDA and UART_IIR_IRDA mappings, depending on the selected mode. 

The IrDA modes have eight possible interrupts (see Table 13-78). The interrupt line is activated when any interrupt is generated (there is no priority). 

|||**Table 13-78. IrDA Mode Interrupts**||
|---|---|---|---|
|**IIR_IRDA Bit**|**Interrupt Type**|**Interrupt Source**|**Interrupt Reset Method**|
|0|RHR interrupt|DRDY (data ready) (FIFO disabled)|Read the UART_RHR register until the|
|||RX FIFO above trigger level (FIFO enabled)|interrupt condition disappears.|
|1|THR interrupt|TFE (UART_THR empty) (FIFO disabled)|Write to the UART_THR until the interrupt|
|||TX FIFO below trigger level (FIFO enabled)|condition disappears.|
|2|Last byte in RX FIFO|Last byte of frame in RX FIFO is available to|Read the UART_RHR register.|
|||be read at the UART_RHR port.||
|3|RX overrun|Write to the UART_RHR register when the|Read UART_RESUME register.|
|||RX FIFO is full.||
|4|Status FIFO interrupt|Status FIFO triggers level reached.|Read STATUS FIFO.|
|5|TX status|UART_THR empty before EOF sent. Last bit|Read the UART_RESUME register|
|||of transmission of the IrDA frame occurred,|OR|
|||but with an underrun error|Read the UART_IIR_IRDA register.|
|||OR||
|||Transmission of the last bit of the IrDA frame||
|||completed successfully.||
|6|Receiver line status|CRC, ABORT, or frame-length error is written|Read the STATUS FIFO (read until empty -|
||interrupt|into the STATUS FIFO.|maximum of eight reads required).|
|7|Received EOF|Received end-of-frame|Read the UART_IIR_IRDA register.|



## _**13.1.4.4.5.2.2 Wake-Up Interrupts**_ 

The wake-up interrupt for IrDA mode has the same function as that for UART mode (see Section 13.1.4.4.5.1.2, _Wake-Up Interrupt_ ). 

## _**13.1.4.4.5.3 CIR Mode Interrupt Management**_ 

## _**13.1.4.4.5.3.1 CIR Interrupts**_ 

The CIR function generates interrupts that can be enabled and disabled by writing to the appropriate bit in the interrupt enable register (UART_IER_CIR). The interrupt status of the device can be checked by reading the interrupt identification register (UART_IIR_CIR). 

The UART, IrDA, and CIR modes have different interrupts in the UART module and, therefore, different UART_IER_CIR and UART_IIR_CIR mappings, depending on the selected mode. 

Table 13-79 lists the interrupt modes to be maintained. In CIR mode, the sole purpose of the UART_IIR_CIR[5] TX_STATUS_IT bit is to indicate that the last bit of infrared data was passed to the TX pin. 

1224 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-79. CIR Mode Interrupts** 

|**IIR_CIR Bit Number**|**Interrupt Type**|**Interrupt Source**|**Interrupt Reset Method**|
|---|---|---|---|
|0|RHR interrupt|DRDY (data ready) (FIFO disable)|Read RHR until interrupt condition|
|||RX FIFO above trigger level (FIFO enable)|disapppears.|
|1|THR interrupt|TFE (THR empty) (FIFO disabled)|Write to the UART_THR register until the|
|||TX FIFO below trigger level (FIFO enabled)|interrupt condition disappears|
|2|RX_STOP_IT|Receive stop interrupt (depending on value|Read the UART_IIR_CIR register|
|||set in the BOF Length register (EBLR))||
|3|RX overrun|Write to RHR when RX FIFO is full.|Read the RESUME register.|
|4|N/A for CIR mode|N/A for CIR mode|N/A for CIR mode|
|5|TX status|Transmission of the last bit of the frame is|Read the UART_IIR_CIR register|
|||complete successfully||
|6|N/A for CIR mode|N/A for CIR mode|N/A for CIR mode|
|7|N/A for CIR mode|N/A for CIR mode|N/A for CIR mode|



## _**13.1.4.4.5.3.2 Wake-Up Interrupts**_ 

The wake-up interrupt for CIR mode has the same function as that for UART mode (see Section 13.1.4.4.5.1.2, _Wake-Up Interrupt_ ). 

## _**13.1.4.4.6 UART FIFO Management**_ 

The FIFO is accessed by reading and writing the UART_RHR and UART_THR registers. Parameters are controlled using the FIFO control register (UART_FCR) and supplementary control register (UART_SCR). Reading the UART_SSR[0] TX_FIFO_FULL bit at 1 means the FIFO is full. 

The UART_TLR register controls the FIFO trigger level, which enables DMA and interrupt generation. After reset, transmit (TX) and receive (RX) FIFOs are disabled; thus, the trigger level is the default value of 1 byte. Figure 13-69 shows the FIFO management registers. 

## **Note** 

Data in the UART_RHR register is not overwritten when an overflow occurs. 

## **Note** 

The UART_SFLSR, UART_SFREGL, and UART_SFREGH status registers are used in IrDA mode only. For information about their use, see Section 13.1.4.4.8.3.3, _IrDA Data Formatting_ . 

## **Note** 

Bits UART_FCR[2] TX_FIFO_CLEAR and UART_FCR[1] RX_FIFO_CLEAR are automatically cleared by hardware after 4 × UARTi_ICLK + 5 × UARTi_FCLK clock cycles. This delay is needed to finish the resetting of the corresponding FIFO and DMA control registers. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1225 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [440 x 408] intentionally omitted <==**

**----- Start of picture text -----**<br>
FIFO management<br>FIFO transmit<br>UART_SSR[0]<br>UART_THR 64-byte transmit FIFO<br>UART_FCR<br>FIFO transmit interrupt FIFO transmit<br>UART_SCR<br>generation DMA request generation<br>UART_TLR<br>FIFO receive interrupt FIFO receive<br>generation DMA request generation<br>FIFO receive<br>64-byte receive FIFO<br>UART_RHR<br>UART_SFREGL<br>UART_SFLSR<br>UART_SFREGH<br>Name Register name REG<br>Control Status<br>uart-023<br>**----- End of picture text -----**<br>


**Figure 13-69. UART FIFO Management Registers** 

## _**13.1.4.4.6.1 FIFO Trigger**_ 

## _**13.1.4.4.6.1.1 Transmit FIFO Trigger**_ 

Table 13-80 lists the TX FIFO trigger level settings. 

**Table 13-80. UART TX FIFO Trigger Level Setting Summary** 

|**SCR[6]**|**TLR[3:0]**|**TX FIFO Trigger Level**|
|---|---|---|
|0|= 0x0|Defined by the UART_FCR[5-4] TX_FIFO_TRIG bit field (8,16, 32, or 56 spaces)|
|0|!= 0x0|Defined by the UART_TLR[3-0] TX_FIFO_TRIG_DMA bit field (from 4 to 60 spaces|
|||with a granularity of 4 spaces)|
|1|Value|Defined by the concatenated value of TLR[3:0] (higher bits) and FCR[5:4] (lower bits)|
|||from 1 to 63 spaces with a granularity of 1 space.|
|||**Note:**The combination of TLR[3:0]=0000 and FCR[5:4]=00 (all zeros) is not supported|
|||(min 1 space required). All zeros will result in unsupported behavior.|



## _**13.1.4.4.6.1.2 Receive FIFO Trigger**_ 

Table 13-81 lists the RX FIFO trigger-level settings. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1226 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-81. UART RX FIFO Trigger-Level Setting Summary** 

|**SCR[7]**|**TLR[7:4]**|**RX FIFO Trigger Level**|
|---|---|---|
|0|= 0x0|Defined by the UART_FCR[7-6] RX_FIFO_TRIG bit field (8,16, 56, or 60 characters)|
|0|!= 0x0|Defined by the UART_TLR[7-4] RX_FIFO_TRIG_DMA bit field (from 4 to 60|
|||characters with a granularity of 4 characters)|
|1|Value|Defined by the concatenated value of TLR[7:4] and FCR[7:6] from 1 to 63 characters|
|||with a granularity of one character.|
|||**Note:**The combination of TLR[7:4]=0000 and FCR[7:6]=00 (all zeros) is not supported|
|||(min 1 character required). All zeros will result in unsupported behavior.|



The receive threshold is programmed using the UART_TCR[7-4] RX_FIFO_TRIG_START and UART_TCR[3-0] RX_FIFO_TRIG_HALT bit fields: 

- Trigger levels from 0 to 60 bytes are available with a granularity of 4 (trigger level = 4 × [4-bit register value]). 

- To ensure correct device operation, ensure that RX_FIFO_TRIG_HALT > RX_FIFO_TRIG when auto-RTS is enabled. 

Delay = [4 + 16 × (1 + CHAR_LENGTH + Parity + Stop – 0.5)] × Baud_rate + 4 × FCLK 

## **Note** 

The RTS signal is deasserted after the UART module receives the data over RX_FIFO_TRIG_HALT. Delay means how long the UART module takes to deassert the RTS signal after reaching RX_FIFO_TRIG_HALT. 

- In FIFO interrupt mode with flow control, ensure that the trigger level to HALT transmission is greater than or equal to the RX FIFO trigger level (the UART_TCR[7-4] RX_FIFO_TRIG_START bit field or the UART_FCR[7-6] RX_FIFO_TRIG bit field); otherwise, FIFO operation stalls. In FIFO DMA mode with flow control, this concept does not exist, because a DMA request is sent when a byte is received. 

## _**13.1.4.4.6.2 FIFO Interrupt Mode**_ 

In FIFO interrupt mode (the FIFO control register UART_FCR[0] FIFO_EN bit is set to 1 and relevant interrupts are enabled by the UART_IER_UART register), an interrupt signal informs the processor of the status of the receiver and transmitter. These interrupts are raised when the RX/TX FIFO threshold (the UART_TLR[7-4] RX_FIFO_TRIG_DMA and UART_TLR[3-0] TX_FIFO_TRIG_DMA bit fields or the UART_FCR[7-6] RX_FIFO_TRIG and UART_FCR[5-4] TX_FIFO_TRIG bit fields, respectively) is reached. 

The interrupt signals instruct the Host CPU to transfer data to the destination (from the UART in receive mode and/or from any source to the UART FIFO in transmit mode). 

When UART flow control is enabled with interrupt capabilities, the UART flow control FIFO threshold (the UART_TCR[3-0] RX_FIFO_TRIG_HALT bit field) must be greater than or equal to the RX FIFO threshold. 

Figure 13-70 shows the generation of the RX FIFO interrupt request. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1227 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [406 x 190] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU acknowledged interrupt request<br>and transferred enough bytes to<br>recover FIFO level below<br>RX FIFO level<br>threshold<br>Programmable flow control threshold<br>Programmable FIFO threshold<br>Zero byte<br>Time<br>Interrupt request<br>Interrupt request active high<br>Time<br>uart-024<br>**----- End of picture text -----**<br>


**Figure 13-70. UART RX FIFO Interrupt Request Generation** 

In receive mode, no interrupt is generated until the RX FIFO reaches its threshold. Once low, the interrupt can be deasserted only when the Host CPU has handled enough bytes to put the FIFO level below threshold. The flow control threshold is set at a higher value than the FIFO threshold. 

Figure 13-71 shows the generation of the TX FIFO interrupt request. 

**==> picture [365 x 195] intentionally omitted <==**

**----- Start of picture text -----**<br>
TX FIFO level<br>Full level<br>Number<br>of<br>spaces<br>Programmable FIFO threshold<br>Zero byte<br>Time<br>Interrupt request<br>Interrupt request<br>active high<br>Time<br>uart-025<br>**----- End of picture text -----**<br>


**Figure 13-71. UART TX FIFO Interrupt Request Generation** 

In transmit mode, an interrupt request is automatically asserted when the TX FIFO is empty. This request is deasserted when the TX FIFO crosses the threshold level. The interrupt line is deasserted until a sufficient number of elements is transmitted to go below the TX FIFO threshold. 

## _**13.1.4.4.6.3 FIFO Polled Mode Operation**_ 

In FIFO polled mode (the UART_FCR[0] FIFO_EN bit is set to 0 and the relevant interrupts are disabled by the UART_IER_UART register), the status of the receiver and transmitter can be checked by polling the line status register (UART_LSR_UART). 

This mode is an alternative to the FIFO interrupt mode of operation in which the status of the receiver and transmitter is automatically determined by sending interrupts to the Host CPU. 

1228 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.1.4.4.6.4 FIFO DMA Mode Operation**_ 

There are four modes of DMA operation, DMA mode 0/1/2/3. Mode 2 and mode 3 are legacy modes that use only one DMA request for each module. 

In mode 2, the remaining DMA request is used for RX. In mode 3, the remaining DMA request is used for TX. 

DMA requests in mode 2 and mode 3 use the USARTi_DMA0 signals (where i = 0 to 5). 

The DMA mode and signals usage can be selected as follows: 

- When SCR[0]=0: 

   - Setting FCR[3] to 0 enables DMA mode 0 

   - Setting FCR[3] to 1 enables DMA mode 1 

- When SCR[0]=1: 

   - SCR[2:1] determines DMA mode 0 to 3 according to the Supplementary Control Register (SCR) description. 

For example: 

- If no DMA operation is desired: set SCR[0] to 1 and SCR[2:1] to 00 (FCR[3] is discarded) 

- If DMA mode 1 is desired: either set SCR[0] to 0 and FCR[3] to 1 or set SCR[0] to 1 and SCR[2:1] to 01 (FCR[3] is discarded) 

If the FIFOs are disabled (FCR[0]=0), DMA operations occur in single character transfers. 

Note that when DMA Mode 0 has been programmed, the signals associated with DMA operation are not active. 

Depending on UART_MDR3[2] SET_DMA_TX_THRESHOLD, the threshold can be programmed different ways: 

- SET_TX_DMA_THRESHOLD = 1: 

The threshold value will be the value of the UART_TX_DMA_THRESHOLD register. If 

SET_TX_DMA_THRESHOLD + TX trigger spaces 64, then the default method of threshold is used: threshold value = TX FIFO size. 

- SET_TX_DMA_THRESHOLD = 0: 

The threshold value = TX FIFO size TX trigger space. The TX DMA line is asserted if the TX FIFO level is lower then the threshold. It remains asserted until TX trigger spaces number of bytes are written into the FIFO. The DMA line is then deasserted and the FIFO level is compared with the threshold value. 

## _**13.1.4.4.6.4.1 DMA sequence to disable TX DMA**_ 

In order to disable TX DMA if it is not needed anymore (e.g. all transfers are done and UART idle mode is desired), the following sequence must be use 

1. DMA mode 1 is set (both TX/RX DMA) by registers UART_SCR[0] DMA_MODE_CTL = 0 and UART_FCR[3] DMA_MODE = 1: 

   - a. Set the UART_SCR[2-1] DMA_MODE_2 bit fields to 01 (DMA mode 1) 

   - b. Set the UART_SCR[0] DMA_MODE_CTL bit to1 (this setting of UART_SCR[0] DMA_MODE-CTL will ignores UART_FCR[3] DMA_MODE_CTL bit) 

## **Note** 

It is strongly suggested to do steps ‘a’ and ‘b’ in two separate write in order to avoid malfunction of the device. 

- c. Set the UART_FCR[3] DMA_MODE bit to 0. It is not necessary but suggested to avoid restore of DMA mode 1 during accidental reset of UART_SCR[0] DMA_MODE_CTL bit. Be sure that all data was read out from RX FIFO and if it possible disable the RX side. In UART mode the RTS/CTS or XOFF/XON protocol can be used. In IrDA modes RX can be forcibly disabled by setting UART_ACREG[5] DIS_IR_RX bit 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1229 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Note** 

There can be RX DATA loss during the next steps if all DATA was not read out or there was an ongoing reception! 

   - d. Set the UART_FCR[2-1] DMA_MODE bit field to 11 (clear TX and RX FIFO and resets its counter logic to 0. Returns to 0 after clearing FIFO). 

   - e. Set the UART_SCR[2-1] DMA_MODE_2 bit field to 10 (DMA mode 2, RX only). 

   - f. Set the UART_FCR[2-1] DMA_MODE bit field to 11 (clear TX and RX FIFO and the DMA request again). g. Set the UART_SCR[2-1] DMA_MODE_2 bit field to 00 (no DMA) or keep 10 if RX DMA is needed. 

2. DMA mode 1 is set (both TX/RX DMA) by registers UART_FCR[3] DMA_MODE = 0 and UART_SCR[0] DMA_MODE_CTL = 1, UART_SCR[2-1] DMA_MODE_2 = 01. It is almost the same as above, but steps ‘a’, and ‘b’ can be skipped: 

   - a. Set the UART_FCR[3] DMA_MODE bit to 0. It is not necessary but suggested to avoid restore of DMA mode 1 during accidental reset of UART_SCR[0] DMA_MODE_CTL bit. Be sure that all data was read out from RX FIFO and if it possible disable the RX side. In UART mode the RTS/CTS or XOFF/XON protocol can be used. In IrDA modes RX can be forcibly disabled by setting UART_ACREG[5] DIS_IR_RX bit 

## **Note** 

There can be RX DATA loss during the next steps if all DATA was not read out or there was an ongoing reception! 

   - b. Set the UART_FCR[2-1] DMA_MODE bit field to 11 (clear TX and RX FIFO and resets its counter logic to 0. Returns to 0 after clearing FIFO). 

   - c. Set the UART_SCR[2-1] DMA_MODE_2 bit field to 10 (DMA mode 2, RX only). 

   - d. Set the UART_FCR[2-1] DMA_MODE bit field to 11 (clear TX and RX FIFO and the DMA request again). e. Set the UART_SCR[2-1] DMA_MODE_2 bit field to 00 (no DMA) or keep 10 if RX DMA is needed. 

3. DMA mode 3 is set (TX DMA only) by registers UART_FCR[3] DMA_MODE = 0 and UART_SCR[0] DMA_MODE_CTL = 1, UART_SCR[2-1] DMA_MODE_2 = 11. It is the same as above: 

   - a. Set the UART_FCR[3] DMA_MODE bit to 0. It is not necessary but suggested to avoid restore of DMA mode 1 during accidental reset of UART_SCR[0] DMA_MODE_CTL bit. Be sure that all data was read out from RX FIFO and if it possible disable the RX side. In UART mode the RTS/CTS or XOFF/XON protocol can be used. In IrDA modes RX can be forcibly disabled by setting UART_ACREG[5] DIS_IR_RX bit 

## **Note** 

There can be RX DATA loss during the next steps if all DATA was not read out or there was an ongoing reception! 

- b. Set the UART_FCR[2-1] DMA_MODE bit field to 11 (clear TX and RX FIFO and resets its counter logic to 0. Returns to 0 after clearing FIFO). 

- c. Set the UART_SCR[2-1] DMA_MODE_2 bit field to 10 (DMA mode 2, RX only). 

- d. Set the UART_FCR[2-1] DMA_MODE bit field to 11 (clear TX and RX FIFO and the DMA request again). 

- e. Set the UART_SCR[2-1] DMA_MODE_2 bit field to 00 (no DMA) or keep 10 if RX DMA is needed. 

## _**13.1.4.4.6.4.2 DMA Transfers (DMA Mode 1, 2, or 3)**_ 

Figure 13-72 through Figure 13-75 show the supported DMA operations. 

1230 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [500 x 287] intentionally omitted <==**

**Figure 13-72. UART Receive FIFO DMA Request Generation (32 Characters)** 

In receive mode, a DMA request is generated when the RX FIFO reaches its threshold level defined in the trigger level register (UART_TLR). This request is deasserted when the number of bytes defined by the threshold level is read by the device DMA controllers. 

In transmit mode, a DMA request is automatically asserted when the TX FIFO is empty. This request is deasserted when the number of bytes defined by the number of spaces in the UART_TLR register is written by the device DMA controllers. If an insufficient number of characters is written, the DMA request stays active. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1231 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [500 x 284] intentionally omitted <==**

**Figure 13-73. UART Transmit FIFO DMA Request Generation (56 Spaces)** 

The DMA request is again asserted if the FIFO can receive the number of bytes defined by the UART_TLR register. 

The threshold can be programmed in a number of ways. Figure 13-73 shows a DMA transfer operating with a space setting of 56 that can arise from using the auto settings in the UART_FCR[5-4] TX_FIFO_TRIG bit field or the UART_TLR[3-0] TX_FIFO_TRIG_DMA bit field concatenated with the TX_FIFO_TRIG bit field. 

The setting of 56 spaces in the UART module must correlate with the settings of the device DMA controllers, so that the buffer does not overflow (program the DMA request size of the LH controller to equal the number of spaces in the UART module). 

Figure 13-74 shows an example with eight spaces to show the buffer level crossing the space threshold. The LH DMA controller settings must correspond to those of the UART module. 

1232 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [500 x 284] intentionally omitted <==**

## **Figure 13-74. UART Transmit FIFO DMA Request Generation (8 Spaces)** 

The next example shows the setting of one space that uses the DMA for each transfer of one character to the transmit buffer (see Figure 13-75). The buffer is filled faster than the baud rate at which data is transmitted to the TX pin. Eventually, the buffer is completely full and the DMA operations stop transferring data to the transmit buffer. 

On two occasions, the buffer holds the maximum amount of data words; shortly after this, the DMA is disabled to show the slower transmission of the data words to the TX pin. Eventually, the buffer is emptied at the rate specified by the baud rate settings of the UART_DLL and UART_DLH registers. 

The DMA settings must correspond to the system LH DMA controller settings to ensure correct operation of this logic. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1233 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [500 x 263] intentionally omitted <==**

**Figure 13-75. UART Transmit FIFO DMA Request Generation (1 Space)** 

The final example illustrates the setting of eight spaces but setting the TX DMA threshold directly by setting UART_MDR3[1] NONDEFAULT_FREQ bit and UART_TX_DMA_THRESHOLD register (see Figure 13-76). In the example, the UART_TX_DMA_THRESHOLD[5-0] TX_DMA_THRESHOLD = 3 and the trigger level is 8. The buffer is filled at a faster rate than the BAUD rate transmits data to the TX pin. The buffer is filled with 8 bytes and the DMA operations stop transferring data to the transmit buffer. When the buffer is emptied to the threshold level by transmission, the DMA operation activates again to fill the buffer with 8 bytes. 

Eventually, the buffer will be emptied at the rate specified by the BAUD Rate settings of the UART_DLL and UART_DLH registers. 

If the selected threshold level + trigger level exceeds max buffer size, then the original TX DMA threshold method is used to prevent TX overrun, regardless of the UART_MDR3[1] NONDEFAULT_FREQ value. 

The DMA settings should correspond to the system Local Host DMA controller settings in order to ensure the correct operation of this logic. 

1234 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [435 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
Programmable<br>threshold<br>+ trigger level<br>(3 + 8 = 12)<br>Trigger level (8)<br>Programmable<br>threshold (3)<br>Zero byte<br>Example: DMA is disabled to<br>show the end of the transfer. Time<br>DMA active periods; this<br>does not represent the<br>DMA signaling.<br>**----- End of picture text -----**<br>


uart-036 

**Figure 13-76. UART Transmit FIFO DMA Request Generation Using Direct TX DMA Threshold Programming. (Threshold = 3; Spaces = 8)** 

## _**13.1.4.4.6.4.3 DMA Transmission**_ 

Figure 13-77 shows DMA transmission. 

**==> picture [406 x 112] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>memory UART/ TX FIFO threshold<br>DMA request IrDA/CIR<br>Reserved for<br>Data to be UART/IrDA/CIR TX FIFO<br>DMA<br>transmitted transmission Transmitted<br>data<br>uart-030<br>**----- End of picture text -----**<br>


## **Figure 13-77. DMA Transmission** 

1. Data to be transmitted are put in the device memory reserved for UART transmission by the DMA: 

   - a. Until the TX FIFO trigger level is not reached, a DMA request is generated 

   - b. An element (1 byte) is transferred from the SDRAM to the TX FIFO at each DMA request (DMA element synchronization). 

2. Data in the TX FIFO are automatically transmitted. 

3. The end of the transmission is signaled by the UART_THR empty (TX FIFO empty). 

## **Note** 

In IrDA mode, the transmission does not end immediately after the TX FIFO empties, at which point the last data byte, the CRC field, and the stop flag still must be transmitted; thus, the end of transmission occurs a few milliseconds after the UART_THR register empties. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1235 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.4.4.6.4.4 DMA Reception**_ 

Figure 13-78 shows DMA reception. 

**==> picture [392 x 133] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>UART/ RX FIFO threshold memory<br>IrDA/CIR<br>RX FIFO<br>Reserved for<br>Received data<br>DMA UART/IrDA/CIR<br>reception<br>DMA request<br>uart-031<br>**----- End of picture text -----**<br>


## **Figure 13-78. DMA Reception** 

1. Enable the reception. 

2. Received data are put in the RX FIFO. 

3. Data are transferred from the RX FIFO to the device memory by the DMA: 

   - a. At each received byte, the RX FIFO trigger level (one character) is reached and a DMA request is generated. 

   - b. An element (1 byte) is transferred from the RX FIFO to the SDRAM at each DMA request (DMA element synchronization). 

4. The end of the reception is signaled by the EOF interrupt. 

## _**13.1.4.4.7 UART Mode Selection**_ 

## _**13.1.4.4.7.1 Register Access Modes**_ 

## _**13.1.4.4.7.1.1 Operational Mode and Configuration Modes**_ 

Register access depends on the register access mode, although register access modes are not correlated to functional mode selection. Three different modes are available: 

- Operational mode 

- Configuration mode A 

- Configuration mode B 

Operational mode is the selected mode when the function is active; serial data transfer can be performed in this mode. 

Configuration mode A and configuration mode B are used during module initialization steps. These modes enable access to configuration registers, which are hidden in the operational mode. The modes are used when the module is inactive (no serial data transfer processed) and only for initialization or reconfiguration of the module. 

The value of the UART_LCR register determines the register access mode (see Table 13-82). 

**Table 13-82. UART Register Access Mode Programming (Using UART_LCR)** 

|**Mode**|**Condition**|
|---|---|
|Configuration mode A|UART_LCR[7] = 0x1 and UART_LCR[7-0] != 0xBF|
|Configuration mode B|UART_LCR[7] = 0x1 and UART_LCR[7-0] = 0xBF|
|Operational mode|UART_LCR[7] = 0x0|



1236 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.1.4.4.7.1.2 Register Access Submode**_ 

In each access register mode (operational mode or configuration mode A/B), some register accesses are conditional on the programming of a submode (MSR_SPR, TCR_TLR, and XOFF). These registers are identified in Table 13-107, _UART Load FIFO Triggers Defined by the Concatenated Value_ . 

Table 13-83 through Table 13-85 summarize the register access submodes. 

**Table 13-83. UART Subconfiguration Mode A Summary** 

||**Mode**|**Condition**|
|---|---|---|
|MSR_SPR||(UART_EFR[4] = 0x0 or UART_MCR[6] = 0x0)|
|TCR_TLR||UART_EFR[4] = 0x1 and UART_MCR[6] = 0x1|
||**Table 13-84.**|**UART Subconfiguration Mode B Summary**|
||**Mode**|**Condition**|
|TCR_TLR||UART_EFR[4] = 0x1 and UART_MCR[6] = 0x1|
|XOFF||(UART_EFR[4] = 0x0 or UART_MCR[6] = 0x0)|
||**Table 13-85. UART Suboperational Mode Summary**||
||**Mode**|**Condition**|
|MSR_SPR||UART_EFR[4] = 0x0 or UART_MCR[6] = 0x0|
|TCR_TLR||UART_EFR[4] = 0x1 and UART_MCR[6] = 0x1|



## _**13.1.4.4.7.1.3 Registers Available for the Register Access Modes**_ 

Table 13-86 lists the names of the register bits in each access register mode. Gray shading indicates that the register does not depend on the register access mode (available in all modes). 

**Table 13-86. UART Register Access Mode Overview** 

|**Address**<br>|**Registers**|
|---|---|
|**Offset**|**Configuration Mode A**<br>**Configuration Mode B**<br>**Operational Mode**|
||**Read**<br>**Write**<br>**Read**<br>**Write**<br>**Read**<br>**Write**|
|0x000|UART_DLL<br>UART_DLL<br>UART_DLL<br>UART_DLL<br>UART_RHR<br>UART_THR|
|0x004|UART_DLH<br>UART_DLH<br>UART_DLH<br>UART_DLH<br>UART_IER_UART<br>UART_IER_UART|
|0x008|UART_IIR_UART<br>UART_FCR<br>UART_EFR<br>UART_EFR<br>UART_IIR_UART<br>UART_FCR|
|0x00C|UART_LCR<br>UART_LCR<br>UART_LCR<br>UART_LCR<br>UART_LCR<br>UART_LCR|
|0x010|UART_MCR<br>UART_MCR<br>UART_XON1_AD<br>DR1<br>UART_XON1_AD<br>DR1<br>UART_MCR<br>UART_MCR|
|0x014|UART_LSR_UART –<br>UART_XON2_AD<br>DR2<br>UART_XON2_AD<br>DR2<br>UART_LSR_UART –|
|0x018|UART_MSR /<br>UART_TCR<br>UART_TCR<br>UART_TCR /<br>UART_XOFF1<br>UART_TCR /<br>UART_XOFF1<br>UART_MSR /<br>UART_TCR<br>UART_TCR|
|0x01C|UART_SPR /<br>UART_TLR<br>UART_SPR /<br>UART_TLR<br>UART_TLR /<br>UART_XOFF2<br>UART_TLR /<br>UART_XOFF2<br>UART_SPR /<br>UART_TLR<br>UART_SPR /<br>UART_TLR|
|0x020|UART_MDR1<br>UART_MDR1<br>UART_MDR1<br>UART_MDR1<br>UART_MDR1<br>UART_MDR1|
|0x024|UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2|
|0x028|UART_SFLSR<br>UART_TXFLL<br>UART_SFLSR<br>UART_TXFLL<br>UART_SFLSR<br>UART_TXFLL|
|0x02C|UART_RESUME<br>UART_TXFLH<br>UART_RESUME<br>UART_TXFLH<br>UART_RESUME<br>UART_TXFLH|
|0x030|UART_SFREGL<br>UART_RXFLL<br>UART_SFREGL<br>UART_RXFLL<br>UART_SFREGL<br>UART_RXFLL|
|0x034|UART_SFREGH<br>UART_RXFLH<br>UART_SFREGH<br>UART_RXFLH<br>UART_SFREGH<br>UART_RXFLH|
|0x038|UART_UASR<br>–<br>UART_UASR<br>–<br>UART_BLR<br>UART_BLR|
|0x03C|–<br>–<br>–<br>–<br>UART_ACREG<br>UART_ACREG|
|0x040|UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1237 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-86. UART Register Access Mode Overview (continued)** 

|**Address**<br>|**Registers**|
|---|---|
|**Offset**|**Configuration Mode A**<br>**Configuration Mode B**<br>**Operational Mode**|
||**Read**<br>**Write**<br>**Read**<br>**Write**<br>**Read**<br>**Write**|
|0x044|UART_SSR<br>–<br>UART_SSR<br>–<br>UART_SSR<br>–|
|0x048|–<br>–<br>–<br>–<br>UART_EBLR<br>UART_EBLR|
|0x050|UART_MVR<br>–<br>UART_MVR<br>–<br>UART_MVR<br>–|
|0x054|UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC|
|0x058|UART_SYSS<br>–<br>UART_SYSS<br>–<br>UART_SYSS<br>–|
|0x05C|UART_WER<br>UART_WER<br>UART_WER<br>UART_WER<br>UART_WER<br>UART_WER|
|0x060|UART_CFPS<br>UART_CFPS<br>UART_CFPS<br>UART_CFPS<br>UART_CFPS<br>UART_CFPS|
|0x064|UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL|
|0x068|UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L|
|0x06C|UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2|
|0x070|UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2|
|0x074|UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL|
|0x080|UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3|
|0x084|UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD|



## _**13.1.4.4.7.2 UART/RS-485/IrDA (SIR, MIR, FIR)/CIR Mode Selection**_ 

To select a mode, set the UART_MDR1[2:0] MODE_SELECT bit field (see Table 13-87). 

**Table 13-87. UART Mode Selection** 

|**Value**|**Mode**|
|---|---|
|0x0:|UART 16× mode|
|0x1:|SIR mode|
|0x2:|UART 16× auto-baud|
|0x3:|UART 13× mode|
|0x4:|MIR mode|
|0x5:|FIR mode|
|0x6:|CIR mode|
|0x7:|Disable (default state)|



MODE_SELECT is effective when the module is in operational mode (see Section 13.1.4.4.7.1, _Register Access Modes_ ). 

To select a RS-485 mode, set the UART_MDR3[4] DIR_EN bit field to 0x1. 

## _**13.1.4.4.7.2.1 Registers Available for the UART Function**_ 

Only the registers listed in Table 13-88 are used for the UART function. 

**Table 13-88. UART Mode Register Overview** 

|**Address**<br>|**Registers**(1) (2)|
|---|---|
|**Offset**|**Configuration Mode A**<br>**Configuration Mode B**<br>**Operational Mode**|
||**Read**<br>**Write**<br>**Read**<br>**Write**<br>**Read**<br>**Write**|
|0x000|UART_DLL<br>UART_DLL<br>UART_DLL<br>UART_DLL<br>UART_RHR<br>UART_THR|
|0x004|UART_DLH<br>UART_DLH<br>UART_DLH<br>UART_DLH<br>UART_IER_UART<br>(UART)<br>UART_IER_UART<br>(UART)|



1238 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-88. UART Mode Register Overview (continued)** 

|**Address**<br>|**Registers**(1) (2)|
|---|---|
|**Offset**|**Configuration Mode A**<br>**Configuration Mode B**<br>**Operational Mode**|
||**Read**<br>**Write**<br>**Read**<br>**Write**<br>**Read**<br>**Write**|
|0x008|UART_IIR_UART<br>UART_FCR<br>UART_EFR [4]<br>UART_EFR [4]<br>UART_IIR_UART<br>(UART)<br>UART_FCR<br>(UART)|
|0x00C|UART_LCR<br>UART_LCR<br>UART_LCR<br>UART_LCR<br>UART_LCR<br>UART_LCR|
|0x010|UART_MCR<br>UART_MCR<br>UART_XON1_AD<br>DR1<br>UART_XON1_AD<br>DR1<br>UART_MCR<br>UART_MCR|
|0x014|UART_LSR_UART<br>(UART)<br>–<br>UART_XON2_AD<br>DR2<br>UART_XON2_AD<br>DR2<br>UART_LSR_UART<br>(UART)<br>–|
|0x018|UART_MSR/<br>UART_TCR<br>UART_TCR<br>UART_XOFF1/<br>UART_TCR<br>UART_XOFF1/<br>UART_TCR<br>UART_MSR/<br>UART_TCR<br>UART_TCR|
|0x01C|UART_TLR/<br>UART_SPR<br>UART_TLR/<br>UART_SPR<br>UART_TLR/<br>UART_XOFF2<br>UART_TLR/<br>UART_XOFF2<br>UART_TLR/<br>UART_SPR<br>UART_TLR/<br>UART_SPR|
|0x020|UART_MDR1<br>UART_MDR1 [2-0] UART_MDR1 [2-0] UART_MDR1 [2-0] UART_MDR1 [2-0] UART_MDR1 [2-0]|
|0x024|UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2|
|0x028|–<br>–<br>–<br>–<br>–<br>–|
|0x02C|–<br>–<br>–<br>–<br>–<br>–|
|0x030|–<br>–<br>–<br>–<br>–<br>–|
|0x034|–<br>–<br>–<br>–<br>–<br>–|
|0x038|UART_UASR<br>–<br>UART_UASR<br>–<br>–<br>–|
|0x03C|–<br>–<br>–<br>–<br>–<br>–|
|0x040|UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR|
|0x044|UART_SSR<br>–<br>UART_SSR<br>–<br>UART_SSR<br>–|
|0x048|–<br>–<br>–<br>–<br>–<br>–|
|0x050|UART_MVR<br>–<br>UART_MVR<br>–<br>UART_MVR<br>–|
|0x054|UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC|
|0x058|UART_SYSS<br>–<br>UART_SYSS<br>–<br>UART_SYSS<br>–|
|0x05C|UART_WER<br>UART_WER<br>UART_WER<br>UART_WER<br>UART_WER<br>UART_WER|
|0x060|–<br>–<br>–<br>–<br>–<br>–|
|0x064|UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL|
|0x068|UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L|
|0x06C|UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2|
|0x070|UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2|
|0x074|UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL|
|0x080|UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3|
|0x084|UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD|



(1) REGISTER_NAME(UART) notation indicates that the register exists for other functions (IrDA or CIR), but fields have different meanings for other functions (described separately in _UART Registers_ ). 

(2) REGISTER_NAME[m:n] notation indicates that only register bits numbered m to n apply to the UART function. 

## _**13.1.4.4.7.2.2 Registers Available for the IrDA Function**_ 

Only the registers listed in Table 13-89 are used for the IrDA function. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1239 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-89. IrDA Mode Register Overview** 

|**Address**<br>|**Registers**(1) (2)|
|---|---|
|**Offset**|**Configuration Mode A**<br>**Configuration Mode B**<br>**Operational Mode**|
||**Read**<br>**Write**<br>**Read**<br>**Write**<br>**Read**<br>**Write**|
|0x000|UART_DLL<br>UART_DLL<br>UART_DLL<br>UART_DLL<br>UART_RHR<br>UART_THR|
|0x004|UART_DLH<br>UART_DLH<br>UART_DLH<br>UART_DLH<br>UART_IER_UART<br>(IrDA)<br>UART_IER_UART<br>(IrDA)|
|0x008|UART_IIR_UART<br>UART_FCR<br>UART_EFR [4]<br>UART_EFR [4]<br>UART_IIR_UART<br>(IrDA)<br>UART_FCR (IrDA)|
|0x00C|UART_LCR [7]<br>UART_LCR [7]<br>UART_LCR [7]<br>UART_LCR [7]<br>UART_LCR [7]<br>UART_LCR [7]|
|0x010|–<br>–<br>UART_XON1_AD<br>DR1<br>UART_XON1_AD<br>DR1<br>–<br>–|
|0x014|UART_LSR_UART<br>(IrDA )<br>–<br>UART_XON2_AD<br>DR2<br>UART_XON2_AD<br>DR2<br>UART_LSR_UART<br>(IrDA)<br>–|
|0x018|UART_MSR/<br>UART_TCR<br>UART_TCR<br>UART_TCR<br>UART_TCR<br>UART_MSR/<br>UART_TCR<br>UART_TCR|
|0x01C|UART_TLR/<br>UART_SPR<br>UART_TLR/<br>UART_SPR<br>UART_TLR<br>UART_TLR<br>UART_TLR/<br>UART_SPR<br>UART_TLR/<br>UART_SPR|
|0x020|UART_MDR1<br>UART_MDR1<br>UART_MDR1<br>UART_MDR1<br>UART_MDR1<br>UART_MDR1|
|0x024|UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2|
|0x028|UART_SFLSR<br>UART_TXFLL<br>UART_SFLSR<br>UART_TXFLL<br>UART_SFLSR<br>UART_TXFLL|
|0x02C|UART_RESUME<br>UART_TXFLH<br>UART_RESUME<br>UART_TXFLH<br>UART_RESUME<br>UART_TXFLH|
|0x030|UART_SFREGL<br>UART_RXFLL<br>UART_SFREGL<br>UART_RXFLL<br>UART_SFREGL<br>UART_RXFLL|
|0x034|UART_SFREGH<br>UART_RXFLH<br>UART_SFREGH<br>UART_RXFLH<br>UART_SFREGH<br>UART_RXFLH|
|0x038|–<br>–<br>–<br>–<br>UART_BLR<br>UART_BLR|
|0x03C|–<br>–<br>–<br>–<br>UART_ACREG<br>UART_ACREG|
|0x040|UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR|
|0x044|UART_SSR<br>–<br>UART_SSR<br>–<br>UART_SSR<br>–|
|0x048|–<br>–<br>–<br>–<br>UART_EBLR<br>UART_EBLR|
|0x050|UART_MVR<br>–<br>UART_MVR<br>–<br>UART_MVR<br>–|
|0x054|UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC|
|0x058|UART_SYSS<br>–<br>UART_SYSS<br>–<br>UART_SYSS<br>–|
|0x05C|UART_WER [6-4]<br>UART_WER [6-4]<br>UART_WER [6-4]<br>UART_WER [6-4]<br>UART_WER [6-4]<br>UART_WER [6-4]|
|0x060|–<br>–<br>–<br>–<br>–<br>–|
|0x064|UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL|
|0x068|UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L|
|0x06C|UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2|
|0x070|UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2|
|0x074|UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL|
|0x080|UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3|
|0x084|UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD|



(1) REGISTER_NAME(IrDA) notation indicates that the register exists for other functions (UART or CIR), but fields have different meanings for other functions (described separately in _UART Registers_ ). 

(2) REGISTER_NAME[m:n] notation indicates that only register bits numbered m to n apply to the IrDA function. 

## _**13.1.4.4.7.2.3 Registers Available for the CIR Function**_ 

Only the registers listed in Table 13-90 are used for the CIR function. 

1240 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-90. CIR Mode Register Overview** 

|**Address**<br>|**Registers**(1) (2)|
|---|---|
|**Offset**|**Configuration Mode A**<br>**Configuration Mode B**<br>**Operational Mode**|
||**Read**<br>**Write**<br>**Read**<br>**Write**<br>**Read**<br>**Write**|
|0x000|UART_DLL<br>UART_DLL<br>UART_DLL<br>UART_DLL<br>–<br>UART_THR|
|0x004|UART_DLH<br>UART_DLH<br>UART_DLH<br>UART_DLH<br>UART_IER_UART<br>(CIR)<br>UART_IER_UART<br>(CIR)|
|0x008|UART_IIR_UART<br>UART_FCR<br>UART_EFR<br>UART_EFR<br>UART_IIR_UART<br>(CIR)<br>UART_FCR (CIR)|
|0x00C|UART_LCR<br>UART_LCR [7]<br>UART_LCR [7]<br>UART_LCR [7]<br>UART_LCR [7]<br>UART_LCR [7]|
|0x010|–<br>–<br>–<br>–<br>–<br>–|
|0x014|UART_LSR_UART<br>(CIR)<br>–<br>–<br>–<br>UART_LSR_UART<br>(CIR)<br>–|
|0x018|UART_MSR/<br>UART_TCR<br>UART_TCR<br>UART_TCR<br>UART_TCR<br>UART_MSR/<br>UART_TCR<br>UART_TCR|
|0x01C|UART_TLR/<br>UART_SPR<br>UART_TLR/<br>UART_SPR<br>UART_TLR<br>UART_TLR<br>UART_TLR/<br>UART_SPR<br>UART_TLR/<br>UART_SPR|
|0x020|UART_MDR1 [3-0] UART_MDR1 [3-0] UART_MDR1 [3-0] UART_MDR1 [3-0] UART_MDR1 [3-0] UART_MDR1 [3-0]|
|0x024|UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2<br>UART_MDR2|
|0x028|–<br>–<br>–<br>–<br>–<br>–|
|0x02C|UART_RESUME<br>–<br>UART_RESUME<br>–<br>UART_RESUME<br>–|
|0x030|–<br>–<br>–<br>–<br>–<br>–|
|0x034|–<br>–<br>–<br>–<br>–<br>–|
|0x038|–<br>–<br>–<br>–<br>–<br>–|
|0x03C|–<br>–<br>–<br>–<br>UART_ACREG<br>UART_ACREG|
|0x040|UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR<br>UART_SCR|
|0x044|UART_SSR<br>–<br>UART_SSR<br>–<br>UART_SSR<br>–|
|0x048|–<br>–<br>–<br>–<br>UART_EBLR<br>UART_EBLR|
|0x050|UART_MVR<br>–<br>UART_MVR<br>–<br>UART_MVR<br>–|
|0x054|UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC<br>UART_SYSC|
|0x058|UART_SYSS<br>–<br>UART_SYSS<br>–<br>UART_SYSS<br>–|
|0x05C|UART_WER [6-4]<br>UART_WER [6-4]<br>UART_WER [6-4]<br>UART_WER [6-4]<br>UART_WER [6-4]<br>UART_WER [6-4]|
|0x060|UART_CFPS<br>UART_CFPS<br>UART_CFPS<br>UART_CFPS<br>UART_CFPS<br>UART_CFPS|
|0x064|UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL<br>UART_RXFIFO_L<br>VL|
|0x068|UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L<br>UART_TXFIFO_LV<br>L|
|0x06C|UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2<br>UART_IER2|
|0x070|UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2<br>UART_ISR2|
|0x074|UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL UART_FREQ_SEL|
|0x080|UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3<br>UART_MDR3|
|0x084|UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD<br>UART_TX_DMA_T<br>HRESHOLD|



(1) REGISTER_NAME(CIR) notation indicates that the register exists for other functions (IrDA or UART), but fields have different meanings for other functions (described separately in _UART Registers_ ). 

(2) REGISTER_NAME[m:n] notation indicates that only register bits numbered m to n apply to the CIR function. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1241 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.1.4.4.8 UART Protocol Formatting**_ 

## _**13.1.4.4.8.1 UART Mode**_ 

## _**13.1.4.4.8.1.1 UART Clock Generation: Baud Rate Generation**_ 

The UART function contains a programmable baud generator and a set of fixed dividers that divide the 48-MHz clock input down to the expected baud rate. 

Figure 13-79 shows the baud rate generator and associated controls. 

**==> picture [414 x 141] intentionally omitted <==**

**----- Start of picture text -----**<br>
14 bits divisor: 16x 13x divisor<br>48 MHz 1/(DLH,DLL) TX UART clock<br>UART MODE 16x<br>UART MODE 13x<br>UART_DLH UART_DLL UART_MDR1[2-0]<br>MODE_SELECT bit field<br>RX UART clock<br>uart-032<br>**----- End of picture text -----**<br>


**Figure 13-79. UART Baud Rate Generation** 

## **CAUTION** 

Before initializing or modifying clock parameter controls (UART_DLH, UART_DLL), UART_MDR1[2-0] MODE_SELECT = DISABLE must be set to 0x7. Failure to observe this rule can result in unpredictable module behavior. 

## _**13.1.4.4.8.1.2 Choosing the Appropriate Divisor Value**_ 

Two divisor values are: 

- UART 16× mode: Divisor value = Operating frequency / (16× baud rate) 

- UART 13× mode: Divisor value = Operating frequency / (13× baud rate) 

**Table 13-91. UART Baud Rate Settings (48-MHz Clock)** 

|**Baud Rate**|**Baud Multiple**|**DLH, DLL (Decimal)**|**DLH, DLL (Hex)**|**Actual Baud Rate**|**Error (%)**|
|---|---|---|---|---|---|
|0.3 kbps|16x|10000|0x27, 0x10|0.3 kbps|0|
|0.6 kbps|16x|5000|0x13, 0x88|0.6 kbps|0|
|1.2 kbps|16x|2500|0x09, 0xC4|1.2 kbps|0|
|2.4 kbps|16x|1250|0x04, 0xE2|2.4 kbps|0|
|4.8 kbps|16x|625|0x02, 0x71|4.8 kbps|0|
|9.6 kbps|16x|312|0x01, 0x39|9.6153 kbps|+0.16|
|14.4 kbps|16x|208|0x00, 0xD0|14.423 kbps|+0.16|
|19.2 kbps|16x|156|0x00, 0x9C|19.231 kbps|+0.16|
|28.8 kbps|16x|104|0x00, 0x68|28.846 kbps|+0.16|
|38.4 kbps|16x|78|0x00, 0x4E|38.462 kbps|+0.16|
|57.6 kbps|16x|52|0x00, 0x34|57.692 kbps|+0.16|
|115.2 kbps|16x|26|0x00, 0x1A|115.38 kbps|+0.16|
|230.4 kbps|16x|13|0x00, 0x0D|230.77 kbps|+0.16|
|460.8 kbps|13x|8|0x00, 0x08|461.54 kbps|+0.16|
|921.6 kbps|13x|4|0x00, 0x04|923.08 kbps|+0.16|
|1.843 Mbps|13x|2|0x00, 0x02|1.846 Mbps|+0.16|



1242 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-91. UART Baud Rate Settings (48-MHz Clock) (continued)** 

|**Baud Rate**|**Baud Multiple**|**DLH, DLL (Decimal)**|**DLH, DLL (Hex)**|**Actual Baud Rate**|**Error (%)**|
|---|---|---|---|---|---|
|3.6884 Mbps|13x|1|0x00, 0x01|3.6923 Mbps|+0.16|
||**Table**|**13-92. UART Baud Rate Settings (160-MHz**||**Clock)**||
|**Baud Rate**|**Baud Multiple**|**DLH, DLL (Decimal)**|**DLH, DLL (Hex)**|**Actual Baud Rate**|**Error (%)**|
|2 Mbps|16x|5|0x00, 0x05|2 Mbps|0|
|5 Mbps|16x|2|0x00, 0x02|5 Mbps|0|
|10 Mbps|16x|1|0x00, 0x01|10 Mbps|0|
||**Table**|**13-93. UART Baud Rate Settings (192-MHz**||**Clock)**||
|**Baud Rate**|**Baud Multiple**|**DLH, DLL (Decimal)**|**DLH, DLL (Hex)**|**Actual Baud Rate**|**Error (%)**|
|12 kbps|16x|1|0x00, 0x01|12 Mbps|0|



## _**13.1.4.4.8.1.3 Multi-drop Parity Mode with Address Match**_ 

Multi-drop mode is enabled in the UART_EFR2 register. 

Address matching mode is only available with 8 bit character length setting. UART_LCR[1-0] CHAR_LENGTH bit fields should always be set to 0x11 (8 bits) prior to enabling the feature. 

This mode allows the transmitter to send data on a line where multiple receivers are connected, when supported. In this mode, a set parity bit is used to mark an address, and a parity of 0 denotes data. 

This setting affects how the parity is generated. Writing a 0x1 into the UART_ECR[0] A_MULTIDROP bit will set the parity bit for the next byte to be sent, which will then be considered an address, for sending a data frame, the UART_ECR[0] A_MULTIDROP bit has to be cleared. 

On reception if the feature is enabled by setting the UART_EFR2[2] MULTIDROP bit to 0x1 incoming frames with parity set to 0x1 are treated as address frames and with parity set to 0x0 as data frames. The receiver will drop all data frames until a matching address frame was found. 

The matching address is determined by the values set in UART_MAR, UART_MMR and UART_MBR registers and the value set in UART_EFR2[7] BROADCAST bit. 

Table 13-94 summarizes the operation of address matching based on the mentioned values. 

**Table 13-94. Details of address matching** 

|**Received**|**Received**|**Frame type **|**UART_MAR**|**UART_MMR**|**UART_MBR**|**UART_EFR2[7]**|**Operation**|**Address**|
|---|---|---|---|---|---|---|---|---|
|**frame**|**parity**|||||**BROADCAST**|**of receiver**|**matching**|
|0xXX(2)|0|DATA|X(1)|X(1)|0xXX(2)|X(1)|Drops data|N/A|
||||||||until||
||||||||matching||
||||||||address||
||||||||found||
|0xXX(2)|1|ADDRESS|0xXX(2)|0x00|0xXX(2)|0|Matches any|Yes|
||||||||address||
|0xEF|1|ADDRESS|0xXX(2)|0xXX(2)|0xEF|1|Matches|Yes|
||||||||broadcast||
||||||||address||
|0x1A|1|ADDRESS|0x1A|0xFF|0xXX(2)|0|Single|Yes|
||||||||address||
||||||||match||
|0xF5|1|ADDRESS|0xF3|0xF9|0xXX(2)|0|Group|Yes|
||||||||address||
||||||||match||



(1) X indicates a do not care bit value 

(2) 0xXX indicates a do not care 8 bit hexadecimal value 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1243 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

The possible values for matching address can be calculated in the following way: 

- Single and Group addresses can be formed by masking the UART_MAR registers value with the value set in the UART_MMR register, bits set to 0x0 in the UART_MMR register result in do not care values. 

- Broadcast addresses can be set in the UART_MBR register if broadcast address is enabled in the UART_EFR2[7] BROADCAST bit, the module will match on received address frames containing the broadcast address. 

- For more details, see example below: 

   - UART_MAR: 0xF3, UART_MMR: 0xF9, UART_MBR: 0xFF 

   - Single and Group addresses: 0xF1, 0xF3, 0xF5, 0xF7 

   - Broadcast addresses: 0xFF 

If an address match occurred the matching address value can be obtained from the UART_RHR register in the following way: 

- If the FIFO is disabled or the threshold is set to 0x1, the matching address can be directly read from UART_RHR as the FIFO will not be overwritten. 

- If the FIFO is enabled or the threshold is greater than 0x1, the matching address will be the latest frame in the FIFO with a parity error bit set. 

For received data, the parity error bit in the UART_LSR_UART register is set when a bit with a parity of 0x1 is received indicating an address frame and the received address matches based on the values of UART_MAR, UART_MMR, UART_MBR and UART_EFR2[2] MULTIDROP bit. 

In Multi-drop mode no parity is used, as the parity bit is used to differentiate address and data frames. The parity error bit is used for indicating an address match. 

For enabling the interrupt generation for address matching UART_IER_UART[2] LINE_STS_IT bit has to be set to 0x1. 

An interrupt for the matching address can be identified by reading the UART_IIR_UART[5-1] IT_TYPE bit fields, a value of 0x00011 indicates a receiver line status error. After the UART_LSR_UART[2] RX_PE bit has to be read, a value of 0x1 indicates that an address match occurred. The reception of a frame is indicated with a value of 0x1 in the UART_LSR_UART[0] RX_FIFO_E bit as the matching value is written into the FIFO regardless of the frame type (data or address). UART_LSR_UART[7] RX_FIFO_STS bit will also be set to 0x1 as the parity error bit is used to indicate a matching address. 

Note that the operation of the UART_LSR_UART[2] RX_PE bit depends on the value set in UART_EFR2[2] MULTIDROP bit. If UART_EFR2[2] MULTIDROP bit is set to 0x0, UART_LSR_UART[2] RX_PE bit is used to indicate a received parity error. If UART_EFR2[2] MULTIDROP bit is set to 0x1, the receiver is in Multi-drop Address Match mode, thus the value in UART_LSR_UART[2] RX_PE bit is used to indicate an address match. 

The interrupt is cleared the same way in both operation modes: reading the UART_LSR_UART register updates the values. 

This feature is available in UART and synchronous modes. The ISO7816 has not defined Multidrop Parity Mode, so the feature should be left off. 

## _**13.1.4.4.8.1.4 Time-guard**_ 

The time-guard feature enables the UART interface to operate with slow remote devices. 

When set, it will insert a number of idle states between transmitting two characters, the length of which can be set in the UART_TIMEGUARD register. The value in the register defines the number of baud clocks of idle period to insert. 

This idle state essentially acts like a long stop bit. In UART and synchronous modes, a Timeguard is added in addition to the stop bit. In ISO7816 there is a waiting period rather than an actual stop bit. Software should set 1-2 or more Timeguard cycles according to the protocol used and the card requirements. 

1244 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.1.4.4.8.1.5 UART Data Formatting**_ 

The UART can use hardware flow control to manage transmission and reception. Hardware flow control significantly reduces software overhead and increases system efficiency by automatically controlling serial data flow using the RTS output and CTS input signals. 

The UART is enhanced with the autobauding function. In control mode, autobauding lets the speed, the number of bits per character, and the parity selected be set automatically. 

## _**13.1.4.4.8.1.5.1 Frame Formatting**_ 

When autobauding is not used, frame format attributes must be defined in the UART_LCR register. 

Character length is specified using the UART_LCR[1-0] CHAR_LENGTH bit field. 

The number of stop-bits is specified using the UART_LCR[2] NB_STOP bit. 

The parity bit is programmed using the UART_LCR[5-3] PARITY_EN, UART_LCR[5-3] PARITY_TYPE_1, and UART_LCR[5-3] PARITY_TYPE_2 bit fields (see Table 13-95). 

**Table 13-95. UART Parity Bit Encoding** 

|**PARITY_EN**|**PARITY_TYPE_1**|**PARITY_TYPE_2**|**Parity**|
|---|---|---|---|
|0|N/A|N/A|No parity|
|1|0|0|Odd parity|
|1|1|0|Even parity|
|1|0|1|Forced 1|
|1|1|1|Forced 0|



## _**13.1.4.4.8.1.5.2 Hardware Flow Control**_ 

Hardware flow control is composed of auto-CTS and auto-RTS. Auto-CTS and auto-RTS can be enabled and disabled independently by programming the UART_EFR[7] AUTO_CTS_EN and UART_EFR[6] AUTO_RTS_EN bit fields, respectively. 

With auto-CTS, CTS signal must be active before the module can transmit data. 

Auto-RTS activates the RTS output only when there is enough room in the RX FIFO to receive data. It deactivates the RTS output when the RX FIFO is sufficiently full. The HALT and RESTORE trigger levels in the UART_TCR register determine the levels at which RTS is activated and deactivated. 

If auto-CTS and auto-RTS are enabled, data transmission does not occur unless the RX FIFO has empty space. Thus, overrun errors are eliminated during hardware flow control. If auto-CTS and auto-RTS are not enabled, overrun errors occur if the transmit data rate exceeds the RX FIFO latency. 

- Auto-RTS: 

Auto-RTS data flow control originates in the receiver block. The RX FIFO trigger levels used in auto-RTS are stored in the UART_TCR register. RTS is active if the RX FIFO level is below the HALT trigger level in the UART_TCR[3-0] RX_FIFO_TRIG_HALT bit field. When the RX FIFO HALT trigger level is reached, RTS is deasserted. The sending device (for example, another UART) can send an additional byte after the trigger level is reached because it may not recognize the deassertion of RTS until it begins sending the additional byte. 

RTS is automatically reasserted when the RX FIFO reaches the RESUME trigger level programmed by the UART_TCR[7-4] RX_FIFO_TRIG_START bit field. This reassertion requests the sending device to resume transmission. 

In this case, RTS is an active-low signal. 

- Auto-CTS: 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1245 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

The transmitter circuitry checks CTS before sending the next data byte. When CTS is active, the transmitter sends the next byte. To stop the transmitter from sending the next byte, CTS must be deasserted before the middle of the last stop-bit currently sent. 

The auto-CTS function reduces interrupts to the host system. When auto-CTS flow control is enabled, the CTS state changes do not have to trigger host interrupts because the device automatically controls its own transmitter. Without auto-CTS, the transmitter sends any data present in the transmit FIFO, and a receiver overrun error can result. 

In this case, CTS is an active-low signal. 

## _**13.1.4.4.8.1.5.3 Software Flow Control**_ 

Software flow control is enabled through the enhanced feature register (UART_EFR) and the modem control register (UART_MCR). Different combinations of software flow control can be enabled by setting different combinations of the UART_EFR[3-0] bit field (see Table 13-96). 

Two other enhanced features relate to software flow control: 

- XON-any function (UART_MCR[5] XON_EN): Operation resumes after receiving any character after the XOFF character is recognized. If special character detect is enabled and special character is received after XOFF1, it does not resume transmission. The special character is stored in the RX FIFO. 

## **Note** 

The XON-any character is written into the RX FIFO even if it is a software flow character. 

- Special character (UART_EFR[5] SPECIAL_CHAR_DETEC T): Incoming data is compared to XOFF2. When the special character is detected, the XOFF interrupt (UART_IIR_UART) is set, but it does not halt transmission. The XOFF interrupt is cleared by a read of UART_IIR_UART. The special character is transferred to the RX FIFO. Special character does not work with XON2, XOFF2, or sequential XOFFs. 

**Table 13-96. UART_EFR[3:0] Software Flow Control Options** 

|**Bit**|**3**|**Bit**|**2**|**Bit**|**1**|**Bit**|**0**|**TX, RX Software Flow Controls**|
|---|---|---|---|---|---|---|---|---|
|0||0||X||X||No transmit flow control|
|1||0||X||X||Transmit XON1, XOFF1|
|0||1||X||X||Transmit XON2, XOFF2|
|1||1||X||X||Transmit XON1, XON2: XOFF1, XOFF2(1)|
|X||X||0||0||No receive flow control|
|X||X||1||0||Receiver compares XON1, XOFF1|
|X||X||0||1||Receiver compares XON2, XOFF2|
|X||X||1||1||Receiver compares XON1, XON2: XOFF1, XOFF2(1)|



(1) In these cases, the XON1 and XON2 characters or the XOFF1 and XOFF2 characters must be transmitted/received sequentially with XON1/XOFF1 followed by XON2/XOFF2. 

- XON1 is defined in the UART_XON1_ADDR1[7-0] XON_WORD1 bit field. XON2 is defined in the UART_XON2_ADDR2[7-0] XON_WORD2 bit field. 

- XOFF1 is defined in the UART_XOFF1[7-0] XOFF_WORD1 bit field. XOFF2 is defined in the UART_XOFF2[7-0] XOFF_WORD2 bit field. 

## _**13.1.4.4.8.1.5.3.1 Receive (RX)**_ 

When software flow control operation is enabled, the UART compares incoming data with XOFF1/2 programmed characters (in certain cases, XOFF1 and XOFF2 must be received sequentially). When the correct XOFF characters are received, transmission stops after transmission of the current character completes. Detection of XOFF also sets the UART_IIR_UART[4] bit (if enabled by UART_IER_UART[5]) and causes the interrupt line to go low. 

To resume transmission, an XON1/2 character must be received (in certain cases, XON1 and XON2 must be received sequentially). When the correct XON characters are received, the UART_IIR_UART[4] bit is cleared and the XOFF interrupt disappears. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1246 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

When a parity, framing, or break error occurs while receiving a software flow control character, this character is treated as normal data and is written to the RX FIFO. 

When XON-any and special character detect are disabled and software flow control is enabled, no valid XON or XOFF characters are written to the RX FIFO. For example, when UART_EFR[1-0] = 0x2, if XON1 and XOFF1 characters are received, they are not written to the RX FIFO. 

When pairs of software flow characters are programmed to be received sequentially (UART_EFR[1-0] = 0x3), the software flow characters are not written to the RX FIFO if they are received sequentially. However, received XON1/XOFF1 characters must be written to the RX FIFO if the subsequent character is not XON2/XOFF2. 

## _**13.1.4.4.8.1.5.3.2 Transmit (TX)**_ 

Two XOFF1 characters are transmitted when the RX FIFO passes the trigger level programmed by UART_TCR[3-0] RX_FIFO_TRIG_HALT. As soon as the RX FIFO reaches the trigger level programmed by UART_TCR[7-4] RX_FIFO_TRIG_START, two XON1 characters are sent, so the data transfer recovers. 

## **Note** 

If software flow control is disabled after an XOFF character is sent, the module transmits XON characters automatically to enable normal transmission. 

The transmission of XOFF(s)/XON(s) follows the same protocol as transmission of an ordinary byte from the TX FIFO. This means that even if the word length is 5, 6, or 7 characters, the 5, 6, or 7 LSBs of XOFF1/2 and XON1/2 are transmitted. The 5, 6, or 7 bits of a character are seldom transmitted, but this function is included to maintain compatibility with earlier designs. 

It is assumed that software flow control and hardware flow control are never enabled simultaneously. 

## _**13.1.4.4.8.1.5.4 Autobauding Modes**_ 

In autobauding mode, the UART can extract transfer characteristics (speed, length, and parity) from an "at" (AT) command (ASCII code). These characteristics are used to receive data after an AT and to send data. 

The following AT commands are valid: 

|AT|DATA|<CR>|
|---|---|---|
|at|DATA|<CR>|
|A/|||
|a/|||



A line break during the acquisition of the sequence AT is not recognized, and an echo function is not implemented in hardware. 

A/ and a/ are not used to extract characteristics, but they must be recognized because of their special meaning. A/ or a/ is used to instruct the software to repeat the last received AT command; therefore, an a/ always follows an AT, and transfer characteristics are not expected to change between an AT and an a/. 

When a valid AT is received, AT and all subsequent data, including the final <CR> (0x0D), are saved to the RX FIFO. The autobaud state-machine waits for the next valid AT command. If an a/ (A/) is received, the a/ (A/) is saved in the RX FIFO and the state-machine waits for the next valid AT command. 

On the first successful detection of the baud rate, the UART activates an interrupt to signify that the AT (upper or lower case) sequence is detected. The UART_UASR register reflects the correct settings for the baud rate detected. Interrupt activity can continue in this fashion when a subsequent character is received. Therefore, it is recommended that the software enable the RHR interrupt when using the autobaud mode. 

The following settings are detected in autobaud mode with a module clock of 48 MHz: 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1247 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

• Speed: – 115.2K baud – 57.6K baud – 38.4K baud – 28.8K baud – 19.2K baud – 14.4K baud – 9.6K baud – 4.8K baud – 2.4K baud – 1.2K baud • Length: 7 or 8 bits • Parity: Odd, even, or space 

**==> picture [24 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
Note<br>**----- End of picture text -----**<br>


The combination of 7-bit character plus space parity is not supported. 

Autobauding mode is selected when the UART_MDR1[2-0] MODE_SELECT bit field is set to 0x2. In UART autobauding mode, UART_DLL, UART_DLH, and UART_LCR[5-0] bit field settings are not used; instead, the UART_UASR register is updated with the configuration detected by the autobauding logic. 

## **UASR Autobauding Status Register Use** 

This register is used to set up transmission according to the characteristics of the previous reception instead of the UART_LCR, UART_DLL, and UART_DLH registers when the UART is in autobauding mode. 

To reset the autobauding hardware (to start a new AT detection) or to set the UART in standard mode (no autobaud), the UART_MDR1[2-0] MODE_SELECT bit field must be set to reset state (0x7) and then to the UART in autobauding mode (0x2) or to the UART in standard mode (0x0). 

Use limitation: 

- Only 7- and 8-bit characters (5- and 6-bit not supported) 

- 7-bit character with space parity not supported 

- Baud rate between 1200 and 115.2 bps (10 possibilities) 

## _**13.1.4.4.8.1.5.5 Error Detection**_ 

When the UART_LSR_UART register is read, the UART_LSR_UART[4:2] bit field reflects the error bits (BI: break condition, FE: framing error, PE: parity error) of the character at the top of the RX FIFO (the next character to be read). Therefore, reading the UART_LSR_UART register and then reading the UART_RHR register identifies errors in a character. 

Reading the UART_RHR register updates the BI, FE, and PE bits (see Table 13-77 for the UART mode interrupts). 

The UART_LSR_UART[7] RX_FIFO_STS bit is set when there is an error in the RX FIFO and is cleared only when no errors remain in the RX FIFO. 

## **Note** 

Reading the UART_LSR_UART register does not cause an increment of the RX FIFO read pointer. The RX FIFO read pointer is incremented by reading the UART_RHR register. 

Reading the UART_LSR_UART register clears the OE bit if it is set (see Table 13-77 for the UART mode interrupts). 

1248 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.1.4.4.8.1.5.6 Overrun During Receive**_ 

Overrun during receive occurs if the RX state-machine tries to write data into the RX FIFO when it is already full. When overrun occurs, the device interrupts the Host CPU with the UART_IIR_UART[5-1] IT_TYPE bit field set to 0x3 (receiver line status error) and discards the remaining portion of the frame. 

Overrun also causes an internal flag to be set, which disables further reception. Before the next frame can be received, the Host CPU must: 

- Reset the RX FIFO. 

- Read the UART_RESUME register, which clears the internal flag. 

## _**13.1.4.4.8.1.5.7 Time-Out and Break Conditions**_ 

## _**13.1.4.4.8.1.5.7.1 Time-Out Counter**_ 

An RX idle condition is detected when the receiver line (RX) is high for a time that equals 4x the programmed word length + 12 bits or manually configured amount of baud clocks, if a value other zero is set in the timeout register. RX is sampled midway through each bit. 

For sleep mode, the counter is reset when there is activity on RX. 

There are two modes of operation: 

- In default operation on the UART_EFR2[6] TIMEOUT_BEHAVE is set to 0. For the time-out interrupt, the counter counts only when there is data in the RX FIFO, and the count is reset when there is activity on RX or when the UART_RHR register is read. 

- Optionally, for choose to enable the timeout counter even if no character has been received by setting UART_EFR2[6] TIMEOUT_BEHAVE bit. This will generate periodic interrupts if the RX line remains idle. In this mode the counter will auto-reset when a timeout has been reached. Reading the UART_IIR_UART will clear the interrupt, but not the counter. 

## _**13.1.4.4.8.1.5.7.2 Break Condition**_ 

When a break condition occurs, TX is pulled low. A break condition is activated by setting the UART_LCR[6] BREAK_EN bit. The break condition is not aligned on word stream (a break condition can occur in the middle of a character). The only way to send a break condition on a full character is: 

1. Reset the TX FIFO (if enabled). 

2. Wait for the transmit shift register to empty (the UART_LSR_UART[6] TX_SR_E bit is set to 1). 

3. Take a guard time according to stop-bit definition. 

4. Set the BREAK_EN bit to 1. 

The break condition is asserted while the BREAK_EN bit is set to 1. 

The time-out counter and break condition apply only to UART modem operation and not to IrDA/CIR mode operation. 

## _**13.1.4.4.8.2 RS-485 Mode**_ 

## _**13.1.4.4.8.2.1 RS-485 External Transceiver Direction Control**_ 

The UART_MDR3[4] DIR_EN bit enables hardware control over an external transceiver to support RS-485. The direction signal comes across the DIR port. The direction polarity is controlled by the UART_MDR3[3] DIR_POL bit. The direction is determined by the hardware monitoring the TX FIFO and the TX shift register. When both are empty the transceiver is set to RX. There is a guard band delay counter of 3 bit clock cycles after the TX shift register is going empty to allow time for the stop bit to transition through the transceiver before a direction change to receive might be applied. 

Figure 13-80 shows the direction control. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1249 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [62 x 7] intentionally omitted <==**

**----- Start of picture text -----**<br>
TIMEGUARD = 3<br>**----- End of picture text -----**<br>


**==> picture [392 x 172] intentionally omitted <==**

**----- Start of picture text -----**<br>
Baud<br>Clock<br>TX<br>Start D0 D1 D2 D3 D4 D5 D6 D7 Parity Stop<br>Bit Bit Bit<br>Write<br>THR<br>RTS [(1)]<br>uart-038<br>**----- End of picture text -----**<br>


- (1) Assumes DIR_POL = 1 

**Figure 13-80. RS-485 External Transceiver Direction Control** 

## _**13.1.4.4.8.3 IrDA Mode**_ 

## _**13.1.4.4.8.3.1 IrDA Clock Generation: Baud Generator**_ 

The IrDA function contains a programmable baud generator and a set of fixed dividers that divide the 48-MHz clock input down to the expected baud rate. 

Figure 13-81 shows the baud rate generator and associated controls. 

**==> picture [384 x 331] intentionally omitted <==**

**----- Start of picture text -----**<br>
RX SIR/MIR<br>16x divisor (SIR)<br>14 bits divisor:<br>1/(DLH,DLL) 41x,42x (MIR) TX SIR/MIR<br>SIR<br>MIR<br>UART_MDR1[2-0]<br>UART_DLH UART_DLL<br>MODE_SELECT bit field<br>FIR<br>6x divisor TX FIR<br>RX FIR<br>1.6/7.1 us SIP (MIR or FIR)<br>77x divisor (1.6 us on)<br>341x divisor (7.1 us off) or<br>1.6 us pulse (SIR)<br>uart-033<br>**----- End of picture text -----**<br>


**Figure 13-81. IrDA Baud Rate Generator** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1250 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **CAUTION** 

Before initializing or modifying clock parameter controls (UART_DLH, UART_DLL), MODE_SELECT=DISABLE (UART_MDR1[2-0] MODE_SELECT) must be set to 0x7). Failure to observe this rule can result in unpredictable module behavior. 

## _**13.1.4.4.8.3.2 Choosing the Appropriate Divisor Value**_ 

Three divisor values are: 

- SIR mode: Divisor value = Operating frequency/(16× baud rate) 

- MIR mode: Divisor value = Operating frequency/(41×/42× baud rate) 

- FIR mode: Divisor value = None 

Table 13-97 lists the IrDA baud rate settings. 

## **Table 13-97. IrDA Baud Rate Settings** 

|**Baud Rate**|**IR Mode**|**Baud**|**Encoding**|**DLH, DLL**|**Actual Baud**|**Error (%)**|**Source Jitter**|**Pulse Duration**|
|---|---|---|---|---|---|---|---|---|
|||**Multiple**||**(Decimal)**|**Rate**||**(%)**||
|2.4 kbps|SIR|16x|3/16|1250|2.4 kbps|0|0|78.1 µs|
|9.6 kbps|SIR|16x|3/16|312|9.6153 kbps|+0.16|0|19.5 µs|
|19.2 kbps|SIR|16x|3/16|156|19.231 kbps|+0.16|0|9.75 µs|
|38.4 kbps|SIR|16x|3/16|78|38.462 kbps|+0.16|0|4.87 µs|
|57.6 kbps|SIR|16x|3/16|52|57.692 kbps|+0.16|0|3.25 µs|
|115.2 kbps|SIR|16x|3/16|26|115.38 kbps|+0.16|0|1.62 µs|
|0.576 Mbps|MIR|41×/42×|1/4|2|0.5756 Mbps(1)|0|+1.63/-0.80|416 ns|
|1.152 Mbps|MIR|41×/42×|1/4|1|1.1511 Mbps(1)|0|+1.63/-0.80|208 ns|
|4 Mbps|FIR|6×|4 PPM|–|4 Mbps|0|0|125 ns|



(1) Average value 

## **Note** 

Baud rate error and source jitter table values do not include 48-MHz reference clock error and jitter. 

## _**13.1.4.4.8.3.3 IrDA Data Formatting**_ 

The methods described in this section apply to all IrDA modes (SIR, MIR, and FIR). 

## _**13.1.4.4.8.3.3.1 IR RX Polarity Control**_ 

The UART_MDR2[6] IRRXINVERT bit provides the flexibility to invert the RX pin in the UART to ensure that the protocol at the output of the transceiver has the same polarity at module level. By default, the RX pin is inverted because most transceivers invert the IR receive pin. 

## _**13.1.4.4.8.3.3.2 IrDA Reception Control**_ 

The module can transmit and receive data, but when the device is transmitting, the IR RX circuitry is automatically disabled by hardware. 

Operation of the RX input can be disabled by the UART_ACREG[5] DIS_IR_RX bit. 

## _**13.1.4.4.8.3.3.3 IR Address Checking**_ 

In all IR modes, when address checking is enabled, only frames intended for the device are written to the RX FIFO. This restriction avoids receiving frames not meant for this device in a multipoint infrared environment. It is possible to program two frame addresses that the UART IrDA receives, with the UART_XON1_ADDR1[7-0] XON_WORD1 and UART_XON2_ADDR2[7-0] XON_WORD2 bit fields. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1251 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

Setting the UART_EFR[0] bit to 1 selects address1 checking. Setting the UART_EFR[1] bit to 1 selects address2 checking. Setting the UART_EFR[1-0] bit field to 0 disables all address checking operations. If both bits are set, the incoming frame is checked for private and public addresses. 

If address checking is disabled, all received frames write to the RX FIFO. 

## _**13.1.4.4.8.3.3.4 Frame Closing**_ 

A transmission frame can be terminated in two ways: 

- Frame-length method: Set the UART_MDR1[7] FRAME_END_MODE bit to 0. The Host CPU writes the value of the frame length to the UART_TXFLH and UART_TXFLL registers. The device automatically attaches end flags to the frame when the number of bytes transmitted equals the value of the frame length. 

- Set-EOT bit method: Set the UART_MDR1[7] FRAME_END_MODE bit to 1. The Host CPU writes 1 to the UART_ACREG[0] EOT bit just before it writes the last byte to the TX FIFO. When the Host CPU writes the last byte to the TX FIFO, the device internally sets the tag bit for that character in the TX FIFO. As the TX state-machine reads data from the TX FIFO, it uses this tag-bit information to attach end flags and correctly terminate the frame. 

## _**13.1.4.4.8.3.3.5 Store and Controlled Transmission**_ 

In store and controlled transmission (SCT) mode, the Host CPU starts writing data to the TX FIFO. Then, after writing a part of a frame (for a bigger frame) or an entire frame (a small frame; that is, a supervisory frame), the Host CPU writes 1 to the UART_ACREG[2] SCTX_EN bit (deferred TX start) to start transmission. 

SCT mode is enabled by setting the UART_MDR1[5] SCT bit to 1. This transmission method differs from normal mode, in which data transmission starts immediately after data is written to the TX FIFO. SCT mode is useful for sending short frames without TX underrun. 

## _**13.1.4.4.8.3.3.6 Error Detection**_ 

When the UART_LSR_UART register is read, the UART_LSR_UART[4-2] bit field reflects the error bits [FL, CRC, ABORT] of the frame at the top of the STATUS FIFO (the next frame status to be read). 

The error is triggered by an interrupt (for IrDA mode interrupts, see Table 13-78). The STATUS FIFO must be read until empty (a maximum of eight reads is required). 

## _**13.1.4.4.8.3.3.7 Underrun During Transmission**_ 

Underrun during transmission occurs when the TX FIFO is empty before the end of the frame is transmitted. When underrun occurs, the device closes the frame with end flags but attaches an incorrect CRC value. The receiving device detects a CRC error and discards the frame; it can then ask for a retransmission. 

Underrun also causes an internal flag to be set, which disables additional transmissions. Before the next frame can be transmitted, the Host CPU must: 

- Reset the TX FIFO. 

- Read the UART_RESUME register, which clears the internal flag. 

This function can be disabled by the UART_ACREG[4] DIS_TX_UNDERRUN bit, compensated by the extension of the stop-bit in transmission if the TX FIFO is empty. 

## _**13.1.4.4.8.3.3.8 Overrun During Receive**_ 

Overrun during receive for the IrDA mode has the same function as that for the UART mode (see Section 13.1.4.4.8.1.5.6, _Overrun During Receive_ ). 

## _**13.1.4.4.8.3.3.9 Status FIFO**_ 

In IrDA modes, a status FIFO records the received frame status. When a complete frame is received, the length of the frame and the error bits associated with the frame are written to the status FIFO. 

1252 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

Reading the UART_SFREGH[3-0] MSB and UART_SFREGL[3-0] (LSB) bit fields obtains the frame length. The frame error status is read in the UART_SFLSR register. Reading the UART_SFLSR register increments the status FIFO read pointer. Because the status FIFO is eight entries deep, it can hold the status of eight frames. 

The Host CPU uses the frame-length information to locate the frame boundary in the received frame data. The Host CPU can screen bad frames using the error status information and can later request the sender to resend only the bad frames. 

This status FIFO can be used effectively in DMA mode because the Host CPU must be interrupted only when the programmed status FIFO trigger level is reached, not each time a frame is received. 

## _**13.1.4.4.8.3.4 SIR Mode Data Formatting**_ 

This section provides specific instructions for SIR mode programming. 

## _**13.1.4.4.8.3.4.1 Abort Sequence**_ 

The transmitter can prematurely close a frame (abort) by sending the sequence 0x7DC1. The abort pattern closes the frame without a CRC field or an ending flag. 

A transmission frame can be aborted by setting the UART_ACREG[1] ABORT_EN bit to 1. When this bit is set to 1, 0x7D and 0xC1 are transmitted and the frame is not terminated with CRC or stop flags. 

When a 0x7D character followed immediately by a 0xC1 character is received without transparency, the receiver treats a frame as an aborted frame. 

## **CAUTION** 

When the TX FIFO is not empty and the UART_MDR1[5] SCT bit is set to 1, the UART IrDA starts a new transfer with data of a previous frame when the aborted frame is sent. Therefore, the TX FIFO must be reset before sending an aborted frame. 

## _**13.1.4.4.8.3.4.2 Pulse Shaping**_ 

SIR mode supports the 3/16 or the 1.6-µs pulse duration methods. The UART_ACREG[7] PULSE_TYPE bit selects the pulse width method in the transmit mode. 

## _**13.1.4.4.8.3.4.3 SIR Free Format Programming**_ 

The SIR FF mode is selected by setting the module in the UART mode (UART_MDR1[2-0] MODE_SELECT = 0x0) and the UART_MDR2[3] PULSE bit to 1 to allow pulse shaping. 

Because the bit format stays the same, some UART mode configuration registers must be set at specific values: 

- UART_LCR[1-0] CHAR_LENGTH bit field = 0x3 (8 data bits) 

- UART_LCR[2] NB_STOP bit = 0x0 (1 stop-bit) 

- UART_LCR[3] PARITY_EN bit = 0x0 (no parity) 

The UART mode interrupts are used for the SIR FF mode, but many are not relevant (XOFF, RTS, CTS, modem status register, etc.). 

## _**13.1.4.4.8.3.5 MIR and FIR Mode Data Formatting**_ 

This section describes common instructions for FIR and MIR mode programming. 

At the end of a frame reception, the CPU reads the line status register (UART_LSR_UART) to detect errors in the received frame. 

When the UART_MDR1[6] SIP_MODE bit is set to 1, the TX state-machine always sends one SIP at the end of a transmission frame. However, when the SIP_MODE bit is set to 0, SIP transmission depends on the UART_ACREG[3] SEND_SIP bit. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1253 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

The CPU can set the SEND_SIP bit at least once every 500 ms. The advantage of this approach over the default approach is that the TX state-machine does not have to send the SIP at the end of each frame, thus reducing the overhead required. 

## _**13.1.4.4.8.4 CIR Mode**_ 

## _**13.1.4.4.8.4.1 CIR Mode Clock Generation**_ 

Depending on the encoding method (variable pulse distance/biphase), the Host CPU must develop a data structure that combines 1 and 0 with a _t_ period to encode the complete frame to transmit. This can then be transmitted to the infrared output with a modulation method, as shown in Figure 13-82. 

**==> picture [438 x 385] intentionally omitted <==**

**----- Start of picture text -----**<br>
Data from<br>TX FIFO<br>CIR transmitter<br>48-MHz / 1 to (214 – 1) / 16 Shift reg (no<br>clock delays between<br>bytes on TX) RCTX<br>16T<br>DLH + DLL<br>12CF<br>CF: Carrier frequency<br>/ 1 to (28 – 1) / 12<br>16T 12CF<br>CFPS Pulse duty 1/3 or 1/4<br>or 5/12 or 1/2<br>Carrier frequency CIR receiver<br>prescaler<br>VOTE3 DEMOD<br>RX<br>Auto Start<br>SHIFT Detect<br>DATA TO RX FIFO Manual or<br>Automatic stop<br>**----- End of picture text -----**<br>


**==> picture [20 x 4] intentionally omitted <==**

**----- Start of picture text -----**<br>
uart-034<br>**----- End of picture text -----**<br>


**Figure 13-82. CIR Mode Block Components** 

Based on the requested modulation frequency, the UART_CFPS register must be set with the correct dividing value to provide an accurate pulse frequency: 

Dividing value = (FCLK / 12) / MODfreq 

Where: 

FCLK = System clock frequency (48 MHz) 

12 = Real value of baud multiple 

1254 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

MODfreq = Effective frequency of the modulation (MHz) 

Example: For a targeted modulation frequency of 36 kHz, the value of CFPS must be set to 0x7 (decimal), which provides a modulation frequency of 36.04 kHz. 

## **Note** 

The UART_CFPS register starts with a reset value of 105 (decimal), which translates to a frequency of 38.1 kHz. 

The duty cycle of these pulses is user-defined by the pulse duty register bits in the UART_MDR2 register. Table 13-98 shows the duty cycle. 

**Table 13-98. CIR Duty Cycle** 

|**UART_MDR2[5-4]**|**Duty Cycle (High-Level)**|
|---|---|
|**CIR_PULSE_MODE**||
|00|1/4|
|01|1/3|
|10|5/12|
|11|1/2|



## _**13.1.4.4.8.4.2 CIR Data Formatting**_ 

The methods described in this section apply to all CIR modes. 

## _**13.1.4.4.8.4.2.1 IR RX Polarity Control**_ 

The IR RX polarity control for CIR mode has the same function as that for IrDA mode (see Section 13.1.4.4.8.3.3.1, _IR RX Polarity Control_ ). 

## _**13.1.4.4.8.4.2.2 CIR Transmission**_ 

In transmission, the Host CPU software must exercise an element of real-time control to transmit data packets, each of which must be emitted at a constant delay from the start-bits of each individual packet. Thus, when sending a series of packets, the packet-to-packet delay must respect a specific delay. Two methods can be used to control this delay: 

- Filling the TX FIFO with a number of zero bits that are transmitted with a _t_ period 

- Using an external system timer to control the delay between each start-of-frame or between the end of a frame and the start of the next one. This can be performed by: 

   - Controlling the start of the frame using the UART_MDR1[5] SCT bit and the UART_ACREG[2] SCTX_EN bit, depending on the timer status 

   - Using the UART_IIR_UART[5] TX_STATUS_IT interrupt bit to preload the next frame in the TX FIFO and to control the start of the timer (in case of control delay between the end of a frame and the start of the next frame) 

## _**13.1.4.4.8.4.2.3 CIR Reception**_ 

There are 2 ways to stop a CIR reception: 

- The Host CPU can disable the reception by setting the UART_ACREG[5] DIS_IR_RX bit to 1. When it considers that the reception is finished because a large number of 0 has been received. To receive a new frame, the UART_ACREG[5] DIS_IR_RX bit must be set to 0. 

- An automatic stop mechanism can configured by setting a value in the BOF length register (UART_EBLR). If the value set in the UART_EBLR register is different than 0, this features is enabled and the number of bits received will begin counting from 0. When the counter reaches the value defined in the UART_EBLR register, reception is automatically disabled and UART_IIR_CIR[2] RX_STOP_IT bit is set. When a 1 is detected on the RX pin, reception is automatically re-enabled. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1255 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

There is a limitation when receiving data in UART CIR mode. Certain IrDA transceivers on the market have a characteristic that causes shrinking of the received modulation pulse hold-time. The UART receive filtering schema is based on the same encoding mechanism used for transmission. 

For the following scenario: 

- Shift register period: 0.9μs 

- Modulation frequency: 36kHz 

- Duty cycle: 1/4 of a modulation frequency period 

Data sent with these conditions would contains 7μs pulses within a 28μs period. The UART expects to receive similar incoming data on receive, but various transceiver timing characteristics typically only send 2μs modulated pulses. These 2μs pulses will be filtered out and RX FIFO will not receive data. This does not affect UART CIR mode in transmission. 

CIR RX demodulation can be bypassed by setting the UART_MDR3[0] DISABLE_CIR_RX_DEMOD bit. 

1256 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.1.4.5 UART Programming Guide** 

This section describes the procedure for operating the UART with FIFO and DMA or interrupts. This three-part procedure ensures the quick start of the UART. It does not cover every UART feature. 

The first programming model covers software reset of the UART. The second programming model describes FIFO and DMA configuration. The last programming model describes protocol, baud rate, and interrupt configuration. 

## **Note** 

Each programming model can be used independently of the other two; for instance, reconfiguring the FIFOs and DMA settings only. 

Each programming model can be executed starting from any UART register access mode (register modes, submodes, and other register dependencies). However, if the UART register access mode is known before executing the programming model, some steps that enable or restore register access are optional. For more information, see Section 13.1.4.4.7.1, _Register Access Modes_ . 

## _**13.1.4.5.1 UART Global Initialization**_ 

## _**13.1.4.5.1.1 Surrounding Modules Global Initialization**_ 

This section identifies the requirements for initializing the surrounding modules when the UART module is to be used for the first time after a device reset. This initialization of surrounding modules is based on the integration of the UART. 

For more information, see . 

## _**13.1.4.5.1.2 UART Module Global Initialization**_ 

The procedure in Table 13-99 can be used to initialize UART when performing software reset. 

**Table 13-99. UART Global Initialization** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Perform a software reset.|UART_SYSC[1] SOFTRESET|1|
|Wait until reset is finished.|UART_SYSS[0] RESETDONE|=1|



## _**13.1.4.5.2 UART Mode selection**_ 

Table 13-100 describes how to set different register access mode. 

**Table 13-100. UART Configure Register Access Mode** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Set the register access mode A|UART_LCR[7] DIV_EN|1|
||UART_LCR[7-0]|≠0xBF|
|Set the register access mode B|UART_LCR[7-0]|0xBF|
|Set the operational mode|UART_LCR[7] DIV_EN|0|



## _**13.1.4.5.3 UART Submode selection**_ 

This section describes how to set different register access submode. 

**Table 13-101. UART Configure Register Access Submode TCR_TLR** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure the submode TCR_TLR|||
|Configure mode B|seeTable 13-100||
|Enable writing to register bits UART_MCR[7-5]|UART_EFR[4] ENHANCED_EN|1|
|Configure mode A|seeTable 13-100|0x1|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1257 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

|**Table 13-101. UART Configure Register Access Submode TCR_TLR(continued)**|**Table 13-101. UART Configure Register Access Submode TCR_TLR(continued)**|**Table 13-101. UART Configure Register Access Submode TCR_TLR(continued)**|
|---|---|---|
|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|Set the submode TCR_TLR|UART_MCR[6] TCR_TLR|1|
|**Table 13-102. UART Configure Register Access Submode MSR_SPR**|||
|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|First option: configure the submode MSR_SPR|||
|Configure mode B|seeTable 13-100||
|Set the submode MSR_SPR|UART_EFR[4] ENHANCED_EN|0|
|Second option: configure the submode MSR_SPR|||
|Configure mode B|seeTable 13-100||
|Enable writing to register bits UART_MCR[7-5]|UART_EFR[4] ENHANCED_EN|1|
|Set the submode MSR_SPR|UART_MCR[6] TCR_TLR|0|



||**Table 13-103. UART Configure Register Access Submode XOFF**||
|---|---|---|
|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|Configure of the XOFF|||
|Configure B|seeTable 13-100||
|Set the submode XOFF|UART_EFR[4] ENHANCED_EN|0|



## _**13.1.4.5.4 UART Load FIFO trigger and DMA mode settings**_ 

## _**13.1.4.5.4.1 DMA mode Settings**_ 

To enable and configure program the DMA mode, perform the following steps: 

**Table 13-104. DMA Mode Settings** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Set the option of DMA mode configuration|UART_SCR[0] DMA_MODE_CTL|-|
|**IF**Configure DMA mode 0 and 1|UART_SCR[0] DMA_MODE_CTL|=0|
|Select the DMA mode, for more information seeSection|UART_FCR[3] DMA_MODE|-|
|13.1.4.4.6.4|||
|**IF**Configure DMA mode from 0 to 3|UART_SCR[0] DMA_MODE_CTL|=1|
|Select the DMA mode, for more information seeSection|UART_SCR[2-1] DMA_MODE_2|-|
|13.1.4.4.6.4|||



## _**13.1.4.5.4.2 FIFO Trigger Settings**_ 

In this section is described configuration and settings of FIFO trigger level, which enable DMA and interrupt generation. 

**Table 13-105. Load FIFO Triggers Defined by the FCR** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure register submode TCR_TLR|seeTable 13-101|0x-|
|Set the desire RX FIFO trigger level|UART_FCR[5-4] TX_FIFO_TRIG|0x-|
|Set the desire TX FIFO trigger level|UART_FCR[7-6] RX_FIFO_TRIG|0x-|



## **Table 13-106. Load FIFO Triggers Defined by the TLR** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure register submode TCR_TLR|seeTable 13-101|0x-|
|Set the desire RX FIFO trigger level|UART_TLR[7-4] RX_FIFO_TRIG_DMA|0x-|
|Set the desire TX FIFO trigger level|UART_TLR[3-0] TX_FIFO_TRIG_DMA|0x-|



1258 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-107. Load FIFO Triggers Defined by the Concatenated Value** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure register submode TCR_TLR|seeTable 13-101|0x-|
|Set the register bit|UART_SCR[7] RX_TRIG_GRANU1|1|
|Set the desire RX FIFO trigger level|UART_TLR[7-4] RX_FIFO_TRIG_DMA|0x-|
||UART_FCR[7-6] RX_FIFO_TRIG||
|Set the register bit|UART_SCR[6] TX_TRIG_GRANU1|1|
|Set the desire TX FIFO trigger level|UART_TLR[3-0] TX_FIFO_TRIG_DMA|0x-|
||UART_FCR[5-4] TX_FIFO_TRIG||



## _**13.1.4.5.5 UART Protocol, Baud rate and interrupt settings**_ 

## _**13.1.4.5.5.1 Baud rate settings**_ 

**Table 13-108. UART Baud Rate Settings** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Disable UART mode|UART_MDR1[2-0] MODE_SELECT|0x7|
|Switch to register configuration mode B|seeTable 13-100||
|Enable access to UART_IER_UART[7-4]|UART_EFR[4] ENHANCED_EN|1|
|Switch register operational mode|seeTable 13-100||
|Disable sleep mode|UART_IER_UART[4] SLEEP_MODE|0|
|Switch to register configuration mode A or B|seeTable 13-100||
|Set the appropriate divisor value|UART_DLL[7-0] CLOCK_LSB|0x-|
||UART_DLH[5-0] CLOCK_MSB||



## _**13.1.4.5.5.2 Interrupt settings**_ 

**Table 13-109. UART Interrupt Settings** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Switch to register configuration mode B|seeTable 13-100|0x7|
|Enable access to UART_IER_UART[7-4]|UART_EFR[4] ENHANCED_EN|1|
|Switch register operational mode|seeTable 13-100||
|Set the desired interrupt configuration (0: Disable the|UART_IER_UART[7] CTS_IT|0x-|
|interrupt; 1: Enable the interrupt)|UART_IER_UART[6] RTS_IT||
||UART_IER_UART[5] XOFF_IT||
||UART_IER_UART[4] SLEEP_MODE||
||UART_IER_UART[3] MODEM_STS_IT||
||UART_IER_UART[2] LINE_STS_IT||
||UART_IER_UART[1] THR_IT||
||UART_IER_UART[0] RHR_IT||



## _**13.1.4.5.5.3 Protocol settings**_ 

Load the desired protocol formatting (parity, stop-bit, character length) and switch to register operational mode. 

**Table 13-110. UART Protocol Settings** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Load desired protocol formatting, seeSection|UART_LCR[5] PARITY_TYPE_2|0x-|
|13.1.4.4.8.1.5.1 _, Frame Formatting_|UART_LCR[4] PARITY_TYPE_1||
||UART_LCR[3] PARITY_EN||
||UART_LCR[2] NB_STOP||
||UART_LCR[1-0] PARITY_LENGTH||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1259 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-110. UART Protocol Settings (continued)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Switch to register operational mode|UART_LCR[7] DIV_EN|0|
||UART_LCR[6] BREAK_EN||



## _**13.1.4.5.5.4 UART/RS-485/IrDA(SIR/MIR/FIR)/CIR**_ 

## **Table 13-111. UART Mode Selection** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Load the desired UART/IrDA (SIR, MIR, FIR)/CIR modes,|UART_MDR1[2-0] MODE_SELECT|0x-|
|seeSection 13.1.4.4.7.2,_UART/RS-485/IrDA (SIR, MIR,_|||
|_FIR)/CIR Mode Selection_|||
|Load the desire RS-485 mode, seeSection 13.1.4.4.7.2,|UART_MDR3[4] DIR_EN|0x1|
|_UART/RS-485/IrDA (SIR, MIR, FIR)/CIR Mode Selection_|||



## _**13.1.4.5.5.5 UART Multi-drop Parity Address Match Mode Configuration**_ 

**Table 13-112. UART Multi-drop Parity Address Match Mode Configuration** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Disable receive mode|UART_ECR[3] RX_EN|0|
|Enable Multi-drop parity Address match mode|UART_EFR2[2] MULTIDROP|1|
|Set the matching device address|UART_MAR[7-0] ADDRESS|0x-|
|Set the address match masking|UART_MMR[7-0] MASK|0x-|
|Set the broadcast address match|UART_MBR[7-0] BROADCAST_ADDRESS|0x-|
|Enable broadcast address matching if needed|UART_EFR2[7] BROADCAST|1|
|Enable receive mode|UART_ECR[3] RX_EN|1|



## _**13.1.4.5.6 UART Hardware and Software Flow Control Configuration**_ 

This section describes the programming steps to enable and configure hardware and software flow control. Hardware and software flow control cannot be used at the same time. 

## _**13.1.4.5.6.1 Hardware Flow Control Configuration**_ 

**Table 13-113. UART Hardware Flow Control Configuration** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Configure register submode TCR_TLR|seeTable 13-101|0x7|
|Load the start and halt trigger value.|UART_TCR[7-4] AUTO_RTS_START|0x-|
||UART_TCR[3-0] AUTO_RTS_HALT||
|Enable or disable receive and transmit hardware flow|UART_EFR[7] AUTO_CTS_EN|0x-|
|control mode.|UART_EFR[6] AUTO_RTS_EN||



## _**13.1.4.5.6.2 Software Flow Control Configuration**_ 

**Table 13-114. UART Software Flow Control Configuration** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Set the register access submode XOFF|seeTable 13-103||
|Load the software control characters|UART_XON1_ADDR1[7-0] XON_WORD1|0x-|
||UART_XON2_ADDR2[7-0] XON_WORD2||
||UART_XOFF1[7-0] XOFF_WORD1||
||UART_XOFF2[7-0] XOFF_WORD2||
|Set the register access submode TCR_TLR|seeTable 13-101||
|Enable or disable XON any function (0: Disable; 1:|UART_MCR[5] XON_EN|--|
|Enable).|||



1260 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-114. UART Software Flow Control Configuration (continued)** 

|**Step**|**Register/Bit Field/Programming Model**<br>**Value**|
|---|---|
|Load start and halt trigger value for software flow control|UART_TCR[7-4] AUTO_RTS_START<br>0x-<br>UART_TCR[3-0] AUTO_RTS_HALT|
|Enable or disable special character function (0: Disable; 1:<br>Enable)|UART_EFR[5] SPEC_CHAR<br>0x-|
|Set the software flow control mode|UART_EFR[3-0] SW_FLOW_CONTROL<br>0x-|



## _**13.1.4.5.7 IrDA Programming Model**_ 

## _**13.1.4.5.7.1 SIR mode**_ 

## _**13.1.4.5.7.1.1 Receive**_ 

The following programming model explains how to program the module to receive an IrDA frame with parity forced to 1, baud rate = 115.2 kbps, FIFOs disabled, 2 stop-bits, and 8-bit word length: 

**Table 13-115. SIR Mode Receive Settings** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Disable UART mode|UART_MDR1[2-0] MODE_SELECT|0x7|
|Grant access to the UART_DLL and UART_DLH registers|UART_LCR[7-0]|0x80|
|Load the baud rate(115.2 Kbps)|UART_DLL[7-0] CLOCK_LSB|0x1A|
||UART_DLH[5-0] CLOCK_MSB|0x00|
|Set SIR mode|UART_MDR1[2-0] MODE_SELECT|0x1|
|Disable access to the UART_DLL and UART_DLH|UART_LCR[7-0]|0x00|
|registers|||
|Enable the UART_RHR interrupt|UART_IER_IRDA[0] RHR_IT|1|



## _**13.1.4.5.7.1.2 Transmit**_ 

The following programming model explains how to program the module to transmit an IrDA 6-byte frame with no parity, baud rate = 115.2 kbps, FIFOs disabled, 3/16 encoding, 2 stop-bits, and 7-bit word length: 

## **Table 13-116. SIR Mode Transmit Settings** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Disable UART mode|UART_MDR1[2-0] MODE_SELECT|0x7|
|Grant access to the UART_DLL and UART_DLH registers|UART_LCR[7-0]|0x80|
|Load the baud rate (115.2 Kbps)|UART_DLL[7-0] CLOCK_LSB|0x1A|
||UART_DLH[5-0] CLOCK_MSB|0x00|
|Set SIR mode|UART_MDR1[2-0] MODE_SELECT|0x1|
|Disable access to the UART_DLL and UART_DLH|UART_LCR[7-0]|0x00|
|registers|||
|Force output DTR to active|UART_MCR[0] DTR|1|
|Enable the UART_THR interrupt|UART_IER_IRDA[1] THR_IT|0x1|
|Set transmit frame length to 6 bytes|UART_TXFLL[7-0] TXFLL|0x06|
|Set the seven starts of frame transmission|UART_EBLR[7-0] EBLR|0x08|
|Set SIR pulse width to be 1.6 μs|UART_ACREG[7] PULSE_TYPE|1|



## _**13.1.4.5.7.2 MIR mode**_ 

## _**13.1.4.5.7.2.1 Receive**_ 

The following programming model explains how to program the module to receive an IrDA frame with no parity, baud rate = 1.152 Mpbs, and FIFOs disabled. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1261 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-117. MIR Mode Receive Settings** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Disable UART mode|UART_MDR1[2-0] MODE_SELECT|0x7|
|Grant access to the UART_DLL and UART_DLH registers|UART_LCR[7-0]|0x80|
|Load the baud rate (1.152 bps)|UART_DLL[7-0] CLOCK_LSB|0x01|
||UART_DLH[5-0] CLOCK_MSB|0x00|
|Set MIR mode|UART_MDR1[2-0] MODE_SELECT|0x4|
|Disable access to the UART_DLL and UART_DLH|UART_LCR[7-0]|0x00|
|registers|||
|Force outputs DTR and RTS to active|UART_MCR[1-0]|0x3|
|Enable the UART_RHR interrupt|UART_IER_IRDA[0] RHR_IT|1|



## _**13.1.4.5.7.2.2 Transmit**_ 

The following programming model explains how to program the module to transmit an IrDA 60-byte frame with no parity, baud rate = 1.152 Mpbs, and FIFOs disabled. 

**Table 13-118. MIR Mode Transmit Settings** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Disable UART mode|UART_MDR1[2-0] MODE_SELECT|0x7|
|Grant access to the UART_DLL and UART_DLH registers|UART_LCR[7-0]|0x80|
|Load the baud rate (115.2 kbps)|UART_DLL[7-0] CLOCK_LSB|0x01|
||UART_DLH[5-0] CLOCK_MSB|0x00|
|Set SIR mode|UART_MDR1[2-0] MODE_SELECT|0x4|
|Disable access to the UART_DLL and UART_DLH|UART_LCR[7-0]|0x00|
|registers|||
|Force output DTR to active|UART_MCR[0] DTR|1|
|Enable the UART_THR interrupt|UART_IER_IRDA[1] THR_IT|0x1|
|Set transmit frame length to 60 bytes|UART_TXFLL[7-0] TXFLL|0x3C|
|Set the eight additional starts of frame transmission|UART_EBLR[7-0] EBLR|0x08|
|SIP is sent at the end of transmission|UART_ACREG[3] SEND_SIP|1|



## _**13.1.4.5.7.3 FIR mode**_ 

## _**13.1.4.5.7.3.1 Receive**_ 

The following programming model explains how to program the module to receive the IrDA frame with no parity, baud rate = 4 Mbps, FIFOs enabled, 8-bit word length. 

**Table 13-119. FIR Mode Receive Settings** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Disable UART mode|UART_MDR1[2-0] MODE_SELECT|0x7|
|Grant access to the UART_DLL and UART_DLH registers|UART_LCR[7-0]|0x80|
|Enable access to change UART_FCR[0]|UART_DLL[7-0] CLOCK_LSB|0x0|
||UART_DLH[7-0] CLOCK_MSB||
|FIFO clear and enable|UART_FCR[2-0]|0x7|
|Set the FIFO trigger level|seeSection 13.1.4.5.4,_Load FIFO trigger and DMA mode_||
||_settings_||
|Set FIR mode|UART_MDR1[2-0] MODE_SELECT|0x5|
|Set frame length|UART_RXFLL[7-0] RXFLL|0xA|
|Disable access to the UART_DLL and UART_DLH|UART_LCR[7-0]|0x00|
|registers|||



1262 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Table 13-119. FIR Mode Receive Settings (continued)** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Enable the UART_RHR interrupt|UART_IER_IRDA[0] RHR_IT|1|



## _**13.1.4.5.7.3.2 Transmit**_ 

The following programming model explains how to program the module to transmit an IrDA 4-byte frame with no parity, baud rate = 4 Mbps, FIFOs enabled, and 8-bit word length. 

**Table 13-120. FIR Mode Transmit Settings** 

|**Step**|**Register/Bit Field/Programming Model**|**Value**|
|---|---|---|
|Disable UART mode|UART_MDR1[2-0] MODE_SELECT|0x7|
|Grant access to the UART_DLL and UART_DLH registers|UART_LCR[7-0]|0x80|
|Enable access to change UART_FCR[0]|UART_DLL[7-0] CLOCK_LSB|0x0|
||UART_DLH[5-0] CLOCK_MSB||
|FIFO clear and enable|UART_FCR[2-0]|0x7|
|Set the FIFO trigger level|seeSection 13.1.4.5.4,_Load FIFO trigger and DMA mode_||
||_settings_||
|Set FIR mode|UART_MDR1[2-0] MODE_SELECT|0x1|
|Disable access to the UART_DLL and UART_DLH|UART_LCR[7-0]|0x00|
|registers|||
|Set FIR mode and enable auto-SIP mode|UART_MDR1[7-0]|0x45|
|Set frame length|UART_TXFLL[7-0] TXFLL|0x4|
||UART_TXFLH[7-0] TXFLH|0x0|
|Force output DTR to active|UART_MCR[0] DTR|1|
|Enable the UART_THR interrupt|UART_IER_IRDA[1] THR_IT|1|
|Set the eight additional starts of frame transmission|UART_EBLR[7-0] EBLR|0x08|
|SIP is sent at the end of transmission|UART_ACREG[3] SEND_SIP|1|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1263 

Copyright © 2025 Texas Instruments Incorporated 

