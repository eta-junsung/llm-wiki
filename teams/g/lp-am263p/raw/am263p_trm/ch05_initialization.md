<!-- AM263P TRM | 5 Initialization | 원본 p.178-223 | pymupdf4llm text+tables, images omitted -->

_Initialization_ 

www.ti.com 

## _Chapter 5_ _**Initialization**_ 

**==> picture [506 x 40] intentionally omitted <==**

This chapter describes the steps for non-secure device initialization. 

**5.1 Initialization Overview** ..............................................................................................................................................179 **5.2 Boot Process** ............................................................................................................................................................ 183 **5.3 Boot Mode Pins** .........................................................................................................................................................188 **5.4 Boot Modes** ............................................................................................................................................................... 189 **5.5 Redundant boot support** ..........................................................................................................................................200 **5.6 PLL Configuration** .................................................................................................................................................... 201 **5.7 Secure Boot Flow** ..................................................................................................................................................... 201 **5.8 Boot Image Format** ...................................................................................................................................................218 **5.9 Boot Memory Maps** ...................................................................................................................................................222 

178 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## **5.1 Initialization Overview** 

This section describes different stages involved in initialization, starting from SoC power-on to loading and running an application. Following are the stages involved as shown in the Figure 5-1: 

- Hardware Startup Process 

- RBL Process 

- SBL Process 

- **Hardware Startup Process** : 

   - **Preinitialization** : Must provide necessary hardware inputs for the device to function i.e., power, clock, control connections and the boot configuration pins. All the control and boot configuration pins must be held at the desired logical levels. 

   - **Power, clock, reset ramp sequence:** Specific sequence that is applied by the power-management chip(s) 

**Hardware Startup** requires an understanding of the process of configuring system interface pins i.e., pads on the device, which have software-configurable functionality. This configuration is an essential part of the chip configuration and is application-dependent. This chapter discusses these system-interface pins, the associated configuration registers, and memory structures that are vital for the proper initialization of the device. 

- **RBL (ROM Bootloader) Process** : 

   - **R5F ROM** : ROM code running on R5F0 core is responsible for identifying the boot interface, downloading, and executing the Secondary Boot Loader (SBL) software. 

   - **HSM ROM** : HSM ROM code runs on M4 core performs image integrity/authentication and it allows or forbids the initial software (SBL) execution. 

R5F ROM and HSM ROM primarily focuses on executing the SBL. 

ROM Code Overview describes RBL process in detail. 

- **SBL (Secondary Bootloader) Process :** 

   - **Initial software or SBL:** Primary software responsible for configuring SoC, that loads and passes control to the application software. 

   - **HSM RunTime or TIFS-MCU:** Firmware running on secure island i.e Cortex M4. This will enable security services as needed by the application software. 

   - **R5F Runtime or Application:** FreeRTOS/ NO RTOS or bare-metal application which runs on main processor(s). 

HSM ROM and SBL collectively boot the HSM RunTime, and the SBL and HSM RunTime collectively boot the R5F Run Time/ Application 

**==> picture [500 x 167] intentionally omitted <==**

**Figure 5-1. Initialization and Boot Process** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

179 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## _**5.1.1 ROM Code Overview**_ 

ROM bootloader (or ROM Code) is a multi-core software that resides in a on-chip read-only memory (ROM) to assist the customer in transferring and executing their SBL and application code. The device has two ROM codes operating in tandem – the Public ROM code (run on R5F core), and the HSM ROM code (run on M4 core). 

The figure below gives a pictorial representation of the various stages of the Boot flow. The HSM ROM starts after the power-on sequence where PORz/RSTz is provided without any glitches on the pads. HSM ROM assumes the R5 core is out of reset and halted. The HSM then clears the R5SS0_COREA_HALT register to un-halt the R5 core. Interprocessor communication between the R5 core and HSM is established using messages through dedicated Mailbox RAM. Write/Read and ACK signals are interrupt based. 

**==> picture [500 x 120] intentionally omitted <==**

**Figure 5-2. Boot Flow** 

In order to accommodate various system scenarios, the ROM Code supports several boot modes. These boot modes can be broadly classified as: 

- Host boot modes 

- Memory boot modes 

During a host boot, the device is configured to receive code from a host via the UART interface. ROM Code receives the application code on the UART interface and stores it in the internal L2 memory. 

During a memory boot, the device transfers code from non-volatile memory to internal memory for execution. 

The HSM and R5F_0 core will collectively download the SBL image to the internal L2 RAM from the external QSPI/OSPI flash (in case of QSPI/OSPI boot mode), the external PC (in the case of UART boot mode), or the USB host in the case of USB DFU boot mode. 

In all boot modes, the entire boot operation can be partitioned into two sections: 

1. Hardware initialization phase 

2. Boot process. 

During initialization, the ROM Code configures the device resources (PLLs, peripherals, pins) as needed to support the boot process. The resources used depend on the boot mode requirements. 

During the boot process the boot image can be loaded into device memory and executed. HSM will perform code verification and allow, or forbid, the image execution. 

The main configuration source for boot after power-up are the BOOTMODE pins sampled automatically after reset release and stored in device status registers. At ROM Code startup, these pin values are read from the registers to create the boot peripheral list and the boot configuration tables which are used later to initialize and startup the PLLs and boot peripherals. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

180 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## _**5.1.2 Bootloader Modes**_ 

Table 5-1 shows the boot modes supported by ROM code. 

**Table 5-1. ROM Code Boot Modes** 

|**Boot Mode**|**Boot Mode**|**Boot Media**|**ZCZ-C & ZCZ-S Package**|**ZCZ-F (SIP)**<br>**Package**|**ROM activity**|
|---|---|---|---|---|---|
|QSPI(4S),50MHz||QSPI Flash|Supported|Not Supported|ROM configures OSPI controller<br>in QSPI 4S mode and downloads<br>image from external flash, supports<br>UART fallback boot mode if any<br>failures|
|UART||External Host|Supported|Supported|ROM configures UART0 with baud<br>rate of 115200 bps and downloads<br>image from external PC terminal<br>using x-modem protocol|
|QSPI(1S),50MHz||OSPI Flash|Supported|Not Supported|ROM configures OSPI controller<br>in QSPI 1S mode and downloads<br>image from external flash , ,<br>supports UART fallback boot mode<br>if any failures|
|OSPI(8S),50 MHz, 0x8B||OSPI Flash|Supported|Supported|ROM configures OSPI controller in<br>8S mode and downloads image<br>from external flash, , supports UART<br>fallback boot mode if any failures|
|DevBoot||N/A|Supported|Supported|To support SBL development,R5-will<br>come up with ROM eclipsed, PLLs<br>are not initialized, No L2, TCMA and<br>TCMB PBIST are performed, No L2<br>memInit|
|xSPI (1S->8D) , 25 MHz,<br>SFDP||OSPI Flash|Supported|Supported|ROM configures OSPI controller in<br>xSPI 8D mode ,Reads SFDP table<br>for read command and downloads<br>image from external flash, Flashes<br>with SFDP are of JEDEC standard<br>Rev D only supported|
||**Note**<br>1.<br>1S Boot is supported on Flash memories that support 0xB commands<br>2.<br>4S boot is supported on Flash memories that support 0x6B|||||



## _**5.1.3 Boot Terminology**_ 

- **Boot Mode Pins:** Boot mode pins provide vital information to ROM code for boot. These pins must be properly set up before power ramp. 

- **Bootstrap:** Initial software launched by the ROM code during the memory booting phase. 

- **Downloaded software:** Initial software downloaded into on-chip RAM by the ROM code during the peripheral booting phase. 

- **eFuse:** A one-time programmable memory location usually set at the factory. 

- **Flash loader:** Downloaded software launched by the ROM code during the preflashing stage and programs an image in external memories. 

- **HS device:** HS-Security device (SoC) 

- **HS-FS device:** (HS-Field Securable) - This is the HS device state before the customer keys are provisioned in the device (the state at which HS device leaves TI factory). In this state, secure features are not available and the device protects the ROM code, TI keys and certain security peripherals. In this state, the device does not force authentication for booting. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 181 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

- **HS-SE device:** (HS-Security Enforced) - This is the HS device state after the customer keys are successfully provisioned in the device. In an HS-SE device, all security features are enabled, all secrets within the device are fully protected, all of the security goals are fully enforced, debug override sequence is supported and the device forces secure booting. 

- **Initial software:** Software executed by any of the ROM code mechanisms (memory booting or peripheral booting). Initial software is a generic term for bootstrap and downloaded software. This can be the SBL (secondary bootloader) responsible for loading an OS. 

- **Memory booting:** ROM code mechanism that consists of downloading initial software from external memory to OCSRAM and executing. 

- **Controller CPU:** The Arm® Cortex® CPU for which CPU-ID is 0. This core configures the multicore platform and starts the ROM code to boot device from a mass storage memory (memory booting) or a peripheral interface (peripheral booting). 

- **Peripheral booting:** ROM code mechanism that consists of polling selected interfaces, downloading, and executing initial software (in this case, downloaded software) in the internal RAM. 

- **Preflashing:** A specific case of peripheral booting where the ROM code mechanism is used to program the external flash memory. 

- **ROM Code:** or ROM bootloader (RBL), the on-chip software in device ROM that executes first and implements booting. 

- **ROM Code-controlled Boot Phase:** This phase covers the sequence operations from the time the platform releases the reset to the time first user- or customer-owned software starts execution. This phase is fully controlled by the device ROM code. 

- **Booting Parameter Table:** A logical structure stored in the on-chip RAM memory and contains information for the boot, such as the boot file name or an address to boot from. 

182 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## **5.2 Boot Process** 

## _**5.2.1 Public ROM Code Architecture**_ 

The Public ROM code (run on the R5 core) has the following components and is described in the Figure 5-3 diagram: 

- Public ROM Entry 

- Boot loop 

- Modules 

- Drivers 

- IPC 

- Logger 

**==> picture [500 x 373] intentionally omitted <==**

**Figure 5-3. Public ROM Code Architecture** 

## **5.2.1.1 Public ROM Entry** 

After the HSM unhalts the R5 core, execution starts at this entry point with the following sequence: 

1. Clears core registers 

2. Performs PBIST on TCMB 

3. Sets up exception and main stack 

4. Performs TI auto Init 

5. Branch to main() 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 183 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## **5.2.1.2 Main Module** 

The Main module performs the following configurations required for the boot on R5 core before entering the boot loop and then enters the boot loop. 

1. System MPU initialization 

2. Core PLL initialization (ROM uses only core PLL) 

3. Logger module Initialization 

4. System Initialization 

   - VIM module Initialization 

   - RTIA Initialization 

5. Performs PBIST on TCMA and L2 

6. Performs TCMA and L2 memory initialization 

7. Initializes the IPC module (Mbox RAM memInit is done part of it) 

8. R5 sends ‘Hello message to HSM’ (R5 core indicates HSM that it is ready for boot) 

## **5.2.1.3 Boot Loop** 

Boot loop starts with the identification of the boot interface by reading boot-strap pins. The device supports two boot interfaces i.e OSPI and UART. Boot parameters are initialized for the identified interface 

## **OSPI** : 

- Clock Frequency : Depends on 1S or 4S or 8S/8D (See the respective section explained later in the chapter) 

- Primary flash image address : **0x0** (See _Redundant Boot Support_ in case of redundant SBL image boot) 

- Interface support : Supports **fast single, Quad and Octal (SDR and DDR)** read modes only with separate boot pin configuration 

## **UART** : 

- Baud rate : **115200 bps** 

- Parity : **None** 

- Data bits : **8** 

- Stop bits : **1** 

- Flow control : **None** 

## **5.2.1.4 Modules** 

Modules are the interface between main module and the drivers. Following are the modules present. 

- **Boot interface** : Reads the boot mode and identifies the boot interface i.e., UART or OSPI 

- **Certificate** : Reads the length of the certificate and image load address 

- **Serial x-modem** : Handles x-modem protocol needs while receiving image via UART host 

- **System** : Handles VIM and RTIA initializations, provides APIs for timeout handling and interrupt handling 

- **ipcMsg** : The IPC Message Layer is used to exchange messages between the R5 and HSM RBL 

- **SoCID** : Describes the SOC Identifier data which is exported by the R5 Boot ROM over the supported peripherals 

- **Pinmux** : This module is used to configure the peripheral IOs to function for the boot interface 

- **Logger** : To log boot info, warnings and errors 

## **5.2.1.5 Drivers** 

Drivers are the software components which configure the various blocks present in the SoC as per the boot interface selected by the user. 

Following are the drivers used: 

- **OSPI:** ROM configures OSPI to support fast single Read, Quad Read and Octal Readmodes. 

- **Flash interface:** Handles flash read APIs for device info and high level APIs for data read 

- **UART:** Handles APIs for UART FIFO Write/Read in interrupt mode 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

184 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

- **EDMA:** DMA module to transfer image from flash to internal L2 memory 

- **RTI:** Timer module to handle timeouts and logger timestamp 

- **VIM:** Vector interrupt module to handle interrupt routines and APIs to configure VIM 

## **5.2.1.6 IPC** 

R5F boot rom and HSM boot rom communicate via IPC (Inter processor communication) using shared mailbox RAM. The Mailbox architecture is a distributed architecture with the Mailbox memory present in the Receiving processors Subsystem. 

Following is the processor numbering: 

|**Processor**|**Number**|
|---|---|
|R5FSS0 Core0|0|
|HSM M4|6|



Following is the Tx and Rx mailbox addressing: 

|**Mailbox**|**Address**|
|---|---|
|R5 Tx Mailbox|0x44000000|
|R5 Rx Mailbox|0x72000000|



## Following are the mailbox interrupts: 

|**Interrupt Type**|**Interrupt Line**|
|---|---|
|R5 Mailbox Read Request|136|
|R5 Mailbox Read Done Acknowledge|137|
|HSM Mailbox Read Request|0|
|HSM Mailbox Read Done Acknowledge|40|



Mailbox message scheme: 

1. PROC_WRITE writes the message in the PROC_READ mailbox 

2. PROC_WRITE triggers an interrupt to PROC_READ by writing 1 to **<PROC_WRITE_SS>_CTRL: <PROC_WRITE>_MBOX_WRITE_DONE [PROC_READ]** . Note. It is writing to its own CTRL space. 

3. PROC_READ gets a single interrupt for all inter processor communication which is an aggregated interrupt. PROC_READ Reads the register **<PROC_READ_SS>_CTRL::<PROC_READ>_MBOX_READ_REQ** and sees bit [PROC_WRITE] is 0x1 

4. PROC_READ Writes to 0x1 to **<PROC_READ_SS>>_CTRL:: <PROC_READ>_MBOX_READ_REQ [PROC_WRITE]** to clear the interrupt. 

5. PROC_READ Reads the Message 

6. PROC_READ Writes to 0x1 to **<PROC_READ_SS>>_CTRL:: <PROC_READ>_MBOX_READ_DONE_ACK[PROC_WRITE]** to generate an acknowledgment interrupt to PROC_WRITE. 

7. PROC_WRITE gets a single interrupt for all inter processor communication which is an aggregated ACK interrupt. PROC_WRITE reads the register **<PROC_WRITE_SS>_CTRL: <PROC_WRITE>_MBOX_READ_DONE** and sees bit [PROC_READ] is 0x1 

8. PROC_WRITE writes 0x1 to **<PROC_WRITE_SS>_CTRL: <PROC_WRITE>_MBOX_READ_DONE [PROC_READ]** to clear the interrupt. 

The supported messages are as follows: 

- IPC_MsgType_HELLO : It’s a hello message from R5 to HSM. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 185 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

- IPC_MsgType_CERT : It’s a message type of certificate from R5 to HSM. 

- IPC_MsgType_IMAGE : It’s a message type of image from R5 to HSM. 

- IPC_MsgType_GET_SOC_ID : SOCID message from R5 to HSM for asking SOCID. 

- IPC_MsgType_RESULT_ACK : Result acknowledge message from R5 to HSM. 

- IPC_MsgType_CANCEL : It’s a cancel message from R5 to HSM. 

- IPC_MsgType_SOC_ID : SOCID message from HSM to R5 for providing SOCID. 

- IPC_MsgType_RESULT : It’s a result message from HSM to R5. 

- IPC_MsgType_CANCEL_ACK : It’s a cancel acknowledge message from HSM to R5. 

The message flow between HSM and R5 as follows: 

**==> picture [500 x 289] intentionally omitted <==**

## **HSM State machine** : 

- **Wait for Hello…** : After unhalting R5 core, HSM ROM waits for ‘Hello…’ message from R5 core. R5 ROM starts execution and initializes core PLL and other necessary modules, configures clocks i.e., R5 Core@400MHz and HSM Core@200MHz and then sends the message **IPC_MsgType_HELLO.** 

- **Wait for Certificate** : R5 core downloads certificate from the identified boot interface and sends message to HSM i.e **., IPC_MsgType_CERT** . HSM validates the certificate based on the device type. 

All the certificate extensions are validated against the above table. 

- **Receive Image** : R5 core updates SBL image information in chunks to HSM, chunk size is >= 2KB. 

HSM performs the following two operations on the image: 

- – SHA512 of the image 

      - Image hash is calculated on the chunks received, and after receiving entire image the computed HASH is compared with hash present in the certificate 

   - Image Decryption 

      - Decryption of the image is optional. If certificate is enabled with decryption, decryption will start only after certificate verification and image integrity checks are passed. 

- **R5 wait Sleep** : 

186 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

- HSM checks for the valid certificate and the image 

- On successful validation of the certificate and the image, HSM ROM will eclipse R5 ROM and issues R5 core reset, then **SBL starts execution from 0x0** 

- In case of any failures observed with the certificate or image validation , HSM retries the boot, state machine jumps to Wait for certificate state. 

_**Note**_ : Refer to section R5 SBL Handoff for more details 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

187 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## **5.3 Boot Mode Pins** 

Boot Mode pins provide means to select the boot mode and options before the device is powered up. After every POR, they are the main source to populate the Boot Parameter Tables. See _Boot Parameter Tables_ for table list and description. 

Boot mode pins can be divided into the following categories: 

- **BOOTMODE[3:0]** – Select the requested boot (primary) mode after POR, that is, the peripheral/memory to boot from. 

## **Note** 

It is user's responsibility to set the boot mode pins (via pullups or pulldowns, and jumpers/switches) depending on the desired boot scenario. 

## _**5.3.1 BOOTMODE Pin Mapping**_ 

The ROM execution is directed through the main boot mode pins. This provides flexibility through additional booting peripherals. The device must be powered and functional. 

Main boot mode pins are shown in Table 5-2. 

Any Bootmode pins marked as Reserved or not used must be tied high or low with pull resistors. They should not be left floating. 

**Table 5-2. BOOTMODE Pin Mapping** 

|**Boot Mode**|**SPI0_D0_pad**<br>**(SOP3)**|**SPI0_CLK_pad**<br>**(SOP2)**|**QSPI_D1 (SOP1)**|**QSPI_D0 (SOP0)**|
|---|---|---|---|---|
|OSPI (4S) - Quad Read Mode|0|0|0|0|
|UART|0|0|0|1|
|OSPI (1S) - Single Read Mode|0|0|1|0|
|OSPI (8S) - Octal Read Mode|0|0|1|1|
|DevBoot|1|0|1|1|
|xSPI 8D (SFDP)|1|1|0|0|
|Unsupported Boot Mode|All other combinations not defined above||||



188 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## **5.4 Boot Modes** 

## _**5.4.1 OSPI Boot**_ 

The following apply to all or multiple boot modes that are OSPI-related. 

## **Note** 

When using a OSPI\SPI flash device greater than 128 Mb, a flash device package with a RESET signal must be used. The reason is that the ROM only uses 3 byte addressing mode (address is 24-bits). To address the full memory address range, software typically switches to 4-byte addressing mode. If a reset to the processor occurs (for example, due to a warm reset), the ROM executes expecting 3-byte addressing mode, but the flash will have been left in 4-byte addressing mode. For the flash device to return to 3-byte addressing mode, it must be reset using this signal. This typically can be achieved by using the RESET signal on the flash memory device. ROM code does not issue a software reset command. 

Refer to the AM263Px OSPI,QSPI Flash Selection Guide for additional details. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

189 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## **5.4.1.1 OSPI (8S) and xSPI (8D)** 

Refer to Section 5.4.1 for more information about all OSPI boot modes. 

_OSPI (8S) and xSPI (8D) Boot Pinmux_ summarizes the QSPI pin configuration done by ROM code for OSPI boot device on port 0. 

**Table 5-3. OSPI (8S) and xSPI (8D) Boot Pinmux** 

|**Package Name**|**Function Name**|**GPI**<br>**O #**|**Input**<br>**Override**|**Input**<br>**Override**<br>**Control**|**Output**<br>**Override**|**Output**<br>**Override**<br>**Control**|**PinMux**<br>**Mode #**|**PI**|**PU/P**<br>**D Sel**|**SC1 **|**GPI**<br>**O**<br>**Sel**|**Qua**<br>**l**<br>**Sel**|**Input**<br>**Invert**<br>**Sel**|**Safety**<br>**Override**<br>**Sel**|**HS Mode**|**HS**<br>**Controller**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|QSPI0_CSn0|OSPI0_CSn0|0|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_CLK0|OSPI0_CLK|2|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_D0|OSPI0_D0|3|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_D1|OSPI0_D1|4|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_D2|OSPI0_D2|5|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_D3|OSPI0_D3|6|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|MCAN0_RX|OSPI0_D4|7|0|0|0|0|2|1|0|1|0|0|0|0|0|0|
|MCAN0_TX|OSPI0_D5|8|0|0|0|0|2|1|0|1|0|0|0|0|0|0|
|MCAN1_RX|OSPI0_D6|9|0|0|0|0|2|1|0|1|0|0|0|0|0|0|
|MCAN1_TX|OSPI0_D7|10|0|0|0|0|2|1|0|1|0|0|0|0|0|0|



## **Note** 

All signals in the table are configured, even though some may not be used by this particular boot mode. 

190 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## _**5.4.1.1.1 OSPI (8S) Bootloader Operation**_ 

The OSPI protocol is described according to bit-width (1 or 8) and data rate (Single Data Rate (S) or Double Data rate (D)) for the Command/Address/Data segments of the protocol. Device supports the 1S-1S-8S mode of OSPI configuration. The Command and Address issued are 8 bits and 24 bits respectively followed by 8 dummy cycles. The frequency of operation supported is 33MHz. 

OSPI (8S) Module Configuration: 

- OSPI has two associated memory regions, the first memory region is dedicated to the configuration port i.e all internal registers can be programmed and serial transfers made from the supported external OSPI flash devices. Configuration region is available at 0x5380_8000 in the SoC address map. 

- The second memory region is associated mainly with the memory-mapped port and is used for communication directly with external flash devices, the memory region starts at 0x6000_0000. Code will be copied from this region to internal RAM and then execution starts. 

- Serial data clock is derived from the clock source “SYS_CLK” (200MHz). This clock is divided by a factor 6 and results in a 33MHz interface clock. 

- MODE3 of OSPI clock mode is used, Clock phase and polarity are set to 1, when data is not being transferred SCK=1, data shifted on falling edge and input on rising edge. 

ROM Sequence: 

- Command issued by ROM in this mode is 0x8B. 

- RBL looks for SBL image at address 0x0000_0000, in case of boot failures due to corrupted image or any other reason, RBL tries to boot with redundant images as explained in _Redundant Boot Support_ . 

Flash dependency: 

- RBL does not perform any specific action to detect, reset, or power up the OSPI device. OSPI is assumed to be properly powered and reset completed before every attempt to boot by RBL. 

## _**5.4.1.1.1.1 OSPI (8S) Loading Process**_ 

OSPI (8S) boot mode is not eXecute-In-Place (XIP). ROM code first copies boot image into on-chip RAM and then executes it. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

191 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## **5.4.1.2 OSPI (8S) and xSPI (8D) - SIP Package** 

Refer to Section 5.4.1 for more information about all OSPI boot modes. 

_OSPI (8S) and xSPI (8D)- SIP Package Boot Pinmux_ summarizes the QSPI pin configuration done by ROM code for OSPI boot device on port 0. 

**Table 5-4. OSPI (8S) and xSPI (8D) Boot Pinmux** 

|**Package Name**|**Function Name**|**GPI**<br>**O**<br>**Nu**<br>**mb**<br>**er**<br>**(GP**<br>**IOx)**|**Input**<br>**Override**|**Input**<br>**Override**<br>**Control**|**Output**<br>**Override**|**Output**<br>**Override**<br>**Control**|**PinMux**<br>**Mode #**|**PI**|**PU/P**<br>**D Sel**|**SC1 **|**GPI**<br>**O**<br>**Sel**|**Qua**<br>**l**<br>**Sel**|**Input**<br>**Invert**<br>**Sel**|**Safety**<br>**Override**<br>**Sel**|**HS Mode**|**HS**<br>**Controller**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|QSPI0_CSn0|OSPI0_CSn0|65|0|0|0|0|6|1|0|1|0|0|0|0|0|0|
|QSPI0_CLK0|OSPI0_CLK|9|0|0|0|0|6|1|0|1|0|0|0|0|0|0|
|QSPI0_D0|OSPI0_D0|0|0|0|0|0|6|1|0|1|0|0|0|0|0|0|
|QSPI0_D1|OSPI0_D1|66|0|0|0|0|6|1|0|1|0|0|0|0|0|0|
|QSPI0_D2|OSPI0_D2|8|0|0|0|0|6|1|0|1|0|0|0|0|0|0|
|QSPI0_D3|OSPI0_D3|69|0|0|0|0|6|1|0|1|0|0|0|0|0|0|
|MCAN0_RX|OSPI0_D4|6|0|0|0|0|6|1|0|1|0|0|0|0|0|0|
|MCAN0_TX|OSPI0_D5|67|0|0|0|0|6|1|0|1|0|0|0|0|0|0|
|MCAN1_RX|OSPI0_D6|5|0|0|0|0|6|1|0|1|0|0|0|0|0|0|
|MCAN1_TX|OSPI0_D7|68|0|0|0|0|6|1|0|1|0|0|0|0|0|0|



## **Note** 

All signals in the table are configured, even though some may not be used by this particular boot mode. 

192 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## _**5.4.1.2.1 OSPI (8S) - Bootloader Operation of SIP Package**_ 

The OSPI protocol is described according to bit-width (1 or 8) and data rate (Single Data Rate (S) or Double Data rate (D)) for the Command/Address/Data segments of the protocol. Device supports the 1S-1S-8S mode of OSPI configuration. The Command and Address issued are 8 bits and 24 bits respectively followed by 8 dummy cycles. The frequency of operation supported is 33MHz. 

OSPI (8S) Module Configuration: 

- OSPI has two associated memory regions, the first memory region is dedicated to the configuration port i.e all internal registers can be programmed and serial transfers made from the supported external OSPI flash devices. Configuration region is available at 0x5380_8000 in the SoC address map. 

- The second memory region is associated mainly with the memory-mapped port and is used for communication directly with external flash devices, the memory region starts at 0x6000_0000. Code will be copied from this region to internal RAM and then execution starts. 

- Serial data clock is derived from the clock source “SYS_CLK” (200MHz). This clock is divided by a factor 6 and results in a 33MHz interface clock. 

- MODE3 of OSPI clock mode is used, Clock phase and polarity are set to 1, when data is not being transferred SCK=1, data shifted on falling edge and input on rising edge. 

ROM Sequence: 

- Command issued by ROM in this mode is 0x8B. 

- RBL looks for SBL image at address 0x0000_0000, in case of boot failures due to corrupted image or any other reason, RBL tries to boot with redundant images as explained in Section 5.5 . 

Flash dependency: 

- RBL does not perform any specific action to detect, reset, or power up the OSPI device. OSPI is assumed to be properly powered and reset completed before every attempt to boot by RBL. 

## _**5.4.1.2.1.1 OSPI (8S) - Loading Process of SIP Pacakge**_ 

OSPI (8S) boot mode is not eXecute-In-Place (XIP). ROM code first copies boot image into on-chip RAM and then executes it. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

193 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## **5.4.1.3 Quad Read (4S)** 

Refer to Section 5.4.1 section for more information about all SPI boot modes. 

summarizes the OSPI pin configuration done by ROM code for OSPI boot device on port 0. 

**Table 5-5. OSPI (4S) Boot Pinmux** 

|**Package Name**|**Function**<br>**Name**|**GPIO**<br>**#**|**Input**<br>**Override**|**Input**<br>**Override**<br>**Control**|**Output**<br>**Override**|**Output**<br>**Override**<br>**Control**|**PinMux**<br>**Mode #**|**PI**|**PU/PD**<br>**Sel**|**SC1**|**GPIO**<br>**Sel**|**Qual Sel**|**Input**<br>**Invert**<br>**Sel**|**Safety**<br>**Override**<br>**Sel**|**HS**<br>**Mode**|**HS**<br>**Controll**<br>**er**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|QSPI0_CSn0|OSPI0_CSn0|0|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_CLK0|OSPI0_CLK|2|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_D0|OSPI0_D0|3|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_D1|OSPI0_D1|4|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_D2|OSPI0_D2|5|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_D3|OSPI0_D3|6|0|0|0|0|0|1|0|1|0|0|0|0|0|0|



## **Note** 

All signals in the table will be configured even though some may not be used by this particular boot mode. 

194 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## _**5.4.1.3.1 OSPI (4S) Bootloader Operation**_ 

Device supports 1S-1S-4S mode of OSPI configuration for fast read operation. This means that command and address are issued in single bit transfer mode and data access occurs in quad bit mode. The Command and Address issued are 8 bits and 24 bits followed by 8 dummy cycles. 50MHz is the supported frequency of operation. 

OSPI (4S) Module Configuration: 

- OSPI has two associated memory regions, the first memory region is dedicated to the configuration port i.e all internal registers can be programmed and serial transfers made from the supported external OSPI flash devices. Configuration region is available at 0x5380_8000 in the SoC address map. 

- The second memory region is associated mainly with the memory-mapped port and is used for communication directly with external flash devices, the memory region starts at 0x6000_0000. Code will be copied from this region to internal RAM and then execution starts. 

- Serial data clock is derived from the clock source “SYS_CLK” (200MHz). This clock is divided by a factor 4 and results in a 50MHz interface clock. 

- MODE3 of OSPI clock mode is used, Clock phase and polarity are set to 1, when data is not being transferred SCK=1, data shifted on falling edge and input on rising edge. 

## ROM Sequence: 

- Command issued by ROM in this mode is 0x6B. 

- RBL looks for SBL image at address 0x0000_0000, in case of boot failures due to corrupted image or any other reason, RBL tries to boot with redundant image as explained in the section Section 5.5 . 

Flash dependency: 

- RBL does not perform any specific action to detect, reset, or power up the OSPI device. OSPI is assumed to be properly powered and reset completed before every attempt to boot by RBL. 

- RBL also expects the QE bit is SET in non-volatile configuration so that flash is active in quad mode by default after POR. 

## _**5.4.1.3.1.1 OSPI (4S) Loading Process**_ 

OSPI (4S) boot mode is not eXecute-In-Place (XIP). ROM code first copies boot image into on-chip RAM and then executes it. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

195 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## **5.4.1.4 OSPI (1S)** 

Table 5-6 summarizes the OSPI pin configuration done by ROM code for OSPI (1S) boot device on port 0. 

**Table 5-6. OSPI (1S) Boot Pinmux** 

|**Package Name**|**Function Name**|**GPIO #**|**Input**<br>**Overrid**<br>**e**|**Input**<br>**Overrid**<br>**e**<br>**Control**|**Output**<br>**Overrid**<br>**e**|**Output**<br>**Overrid**<br>**e**<br>**Control**|**PinMux**<br>**Mode #**|**PI**|**PU/PD**<br>**Sel**|**SC1**|**GPIO**<br>**Sel**|**Qual**<br>**Sel**|**Input**<br>**Invert**<br>**Sel**|**Safety**<br>**Overrid**<br>**e Sel**|**HS**<br>**Mode**|**HS**<br>**Controll**<br>**er**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|QSPI0_CSn0|OSPI0_CSn0|0|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_CLK0|OSPI0_CLK|2|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_D0|OSPI0_D0|3|0|0|0|0|0|1|0|1|0|0|0|0|0|0|
|QSPI0_D1|OSPI0_D1|4|0|0|0|0|0|1|0|1|0|0|0|0|0|0|



## **Note** 

All signals in the table will be configured even though some may not be used by this particular boot mode. 

196 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## _**5.4.1.4.1 OSPI (1S) Bootloader Operation**_ 

Device supports the 1S-1S-1S mode of OPSI configuration. This means that command, address, and data access are in single bit mode. The Command and Address issued are 8 bits and 24 bits followed by 8 dummy cycles. 50 MHz is the supported frequency of operation. 

OSPI (1S) Module Configuration: 

- OSPI has two associated memory regions, the first memory region is dedicated to the configuration port i.e all internal registers can be programmed and serial transfers made from the supported external OSPI flash devices. Configuration region is available at 0x5380_8000 in the SoC address map. 

- The second memory region is associated mainly with the memory-mapped port and is used for communication directly with external flash devices, the memory region starts at 0x6000_0000. Code will be copied from this region to internal RAM and then execution starts. 

- Serial data clock is derived from the clock source “SYS_CLK” (200MHz). This clock is divided by a factor 4 and results in a 50MHz interface clock. 

- MODE3 of OSPI clock mode is used, Clock phase and polarity are set to 1, when data is not being transferred SCK=1, data shifted on falling edge and input on rising edge. 

## ROM Sequence: 

- Command issued by ROM in this mode is 0x0B. 

- RBL looks for SBL image at address 0x0000_0000, in case of boot failures due to corrupted image or any other reason, RBL tries to boot with redundant image placed as explained in the section _Redundant boot support_ . 

Flash Dependency: 

- RBL does not perform any specific action to detect, reset, or power up the OSPI device. OSPI is assumed to be properly powered and reset completed before every attempt to boot by RBL. 

## _**5.4.1.4.1.1 OSPI (1S) Loading Process**_ 

OSPI (1S) boot mode is not eXecute-In-Place (XIP). ROM code first copies boot image into on-chip RAM and then executes it. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

197 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## _**5.4.2 UART Boot**_ 

ROM Code always configures the UART port to 115200 kbaud, 8-n-1 mode, and the XMODEM protocol is used to transfer the boot data. 

Table 5-7 summarizes the UART pin configuration done by ROM code for UART host on port 0. 

**Table 5-7. UART Boot Pinmux** 

|**Function**<br>**Name**|**GPIO #**|**Input**<br>**Override**|**Input**<br>**Override**<br>**Control**|**Output**<br>**Override**|**Output**<br>**Override**<br>**Control**|**Pinmux**<br>**Sel**|**PI**|**PUPD Sel**|**SC1**|**GPIO Sel**|**Qual Sel**|**Inp Inv Sel **|**HS Mode**|**HS**<br>**Controller**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|UART0_TXD|28|0|0|0|0|0|1|0|1|0|0|0|0|0|
|UART0_RXD|27|0|0|0|0|0|1|0|1|0|0|0|0|0|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

198 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## **5.4.2.1 UART Bootloader Operation** 

## _**5.4.2.1.1 Initialization Process**_ 

In the UART boot mode, the selected UART module (port) is the only peripheral configured. The baud rate, data, parity, and stop bits are configured based on the information in the UART boot parameter table. The boot parameter table definitions and the boot configuration values that can be set are in _UART Boot Device Configuration_ and _UART Boot Parameter Table_ . 

Once the ROM Code configures the UART, it sends the UART pings for few seconds, which can be seen in the host. The pings consist of an ASCII capital _C_ character. The UART boot mode supports only the CRC mode of XMODEM and does not support CHECKSUM mode. Both 128 and 1024 byte block sizes are supported. 

## _**5.4.2.1.2 UART Loading Process**_ 

Before the ping from the device stops, load the boot image from the host using the XMODEM protocol. 

## _**5.4.2.1.2.1 UART XMODEM**_ 

The XMODEM protocol is used to transfer boot data. Only CRC mode is supported (not checksum), with both 128- and 1024-byte block sizes. The general, format of received frames is shown in Table 5-8 and Table 5-9. 

**Table 5-8. XMODEM 1024- and 128-byte Data Frames** 

|STX|Block Num|Inv Block<br>Num|1024 data bytes|1024 data bytes|1024 data bytes|1024 data bytes|CRC|CRC|
|---|---|---|---|---|---|---|---|---|
|SOH|Block Num|Inv Block<br>Num|128 data bytes|CRC|CRC||||



**Table 5-9. XMODEM Data Frame Fields** 

|**Field**|**Value**|**Description**|
|---|---|---|
|STX|0x02|The start character for 1024-byte CRC data blocks|
|SOH|0x01|The start character for 128-byte CRC data block|
|Block Num|0x01-0xFF – 0x00|The block number. The first block has value 1, and the block number wraps around 0xFF to 0|
|Inv Block Num|0xFE-0x00|The inverse block number (bit inverse of the block number)|
|CRC|Calculated|The 16-bit CRC generated from the polynomial 0x1021|



The XMODEM protocol is implemented as a half-duplex protocol as shown in Table 5-10. 

**Table 5-10. Example of XMODEM Transfer protocol** 

|**Transmitter Sends**||**Receiver Sends**|
|---|---|---|
||←|Ping (‘C’)|
|Frame 1|→||
||←|ACK (or NACK)|
|Frame 2|→||
||←|ACK (or NACK)|
|EOT|→||
||←|ACK (or NACK)|



## _**5.4.2.1.3 UART Hand-Over Process**_ 

Once the complete image has been read and found in good integrity, the ROM Code will branch to the address defined in the Boot Info field of the boot header. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

199 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## _**5.4.3 DevBoot**_ 

This boot mode is useful for the development of SBL and for the JTAG based KeyWriter. 

## **5.5 Redundant boot support** 

Redundant boot is supported on OSPI flash boot modes. ROM tries to boot SBL at the Region1 address and if it fails to boot, then ROM tries to boot from the locations in the order Region1 → Region2 → Region3 → Region4 until boot is successful. 

**Table 5-11.** 

|**Region**|**Address**|
|---|---|
|**1**|**0x0_0000**|
|**2**|**0x2_0000**|
|**3**|**0x4_0000**|
|**4**|**0x6_0000**|



Following are the failures which can lead to redundant boot: 

1. Certificate corruption, ex. Image size, hash of the image, extension IDs, signature etc. 

2. Image corruption, ex. bit corruption, byte corruption due to aging of the flash, external interferences etc. 

## **Note** 

AM263Px supports max image size of 256KB with redundant image support and 512KB without redundant image support. Successfully booted flash Image offset Address is available at the address **0000x84100** 

200 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## **5.6 PLL Configuration** 

ROM code must be aware of the reference clock provided to PLLs. That is, the speed of the quartz crystal, or the clock supplied by an external clock oscillator. 

## **Note** 

This device requires 25MHz XTAL clock source. 

The Public ROM code configures PLLs which are required during boot. ROM configures only core PLL during boot. The ROM Core PLL configuration details is as follows: 

- InputClockDiv (N) = 0xB 

- Multiplier (M) = 0x180 

- Divider (N2) = 0x1 

- Post-Divider (M2) = 0X1 

- Fractional Multiplier (Frac) = 0x0 

Using the above values, the PLL output frequency is computed as follows: 

- XTAL_IN/(N + 1) = 25/12 = 2.0833 MHz 

- (XTAL_IN * M) /(N + 1) = 2.08333 * 384 = 800MHz 

- (XTAL_IN * M) /[(N2 +1) * (N + 1)] = 800 / 2 = 400MHz 

- 400/ M2 = 400MHz 

## **Note** 

See ADPLLLJ Module section in the Clocking section of Device configuration chapter for more details on PLL configuration sequence and the PLL output frequency equation. 

Where, XTAL_IN is the XTAL Clock source frequency (25MHz) 

This Core PLL output (ADPLL0) is used to configure R5 clock = 400MHz and SysClk = 200MHz 

## **5.7 Secure Boot Flow** 

## _**5.7.1 Overview**_ 

The secure boot flow is as depicted in Figure 5-4. The ROM-based secure boot is realized by interactions between the MSS R5F ROM and the HSM ROM. When the secondary bootloader (SBL) and the HSM runtime firmware is brought into the respective (MSS R5F and HSM CM4) cores, it is then the responsibility of the SBL to download the further application images. First, the ROM bootloader downloads the SBL. The SBL begins execution (MSS R5F ROM is eclipsed at this point and ROM services are not available anymore) and in turn invokes an API into HSM ROM to download the HSM runtime firmware. When the HSM runtime firmware is downloaded, the HSM ROM is eclipsed and ROM services not available anymore. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

201 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

**==> picture [500 x 329] intentionally omitted <==**

**Figure 5-4. Secure Boot Flow** 

## _**5.7.2 x509 Certificate Structure**_ 

The X.509 certificate is defined in Annex A of ITU-T X.509 specification [1]. Certificate is encoded using ASN.1 encoding [2] with DER (Distinguished Encoding Rules) [3]. The main body of the certificate is illustrated below. Essentially, the signed certificate is the concatenation of the certificate itself and the signature. Certificate includes mandatory and optional fields. The supported version shall be v2. V3 and higher versions support is desired but not guaranteed. Various fields of the x509 certificate are as shown below. 

```
SIGNATURE ::= SEQUENCE {
            algorithmIdentifier algorithmIdentifier{{SupportedAlgorithms}},
            signature BIT STRING,
            ... }
SIGNED{ToBeSigned} ::= SEQUENCE {
            toBeSigned toBeSigned,
            COMPONENTS OF SIGNATURE,
            ... }
Certificate ::= SIGNED{TBSCertificate}
TBSCertificate ::= SEQUENCE {
            version [0] Version DEFAULT v1,
            serialNumber CertificateSerialNumber,
            signature AlgorithmIdentifier{{SupportedAlgorithms}},
            issuer Name,
            validity Validity,
            subject Name,
            subjectPublicKeyInfo SubjectPublicKeyInfo,
            issuerUniqueIdentifier [1] IMPLICIT UniqueIdentifier OPTIONAL,
            ...,
            [[2: -- if present, version shall be v2 or v3
            subjectUniqueIdentifier [2] IMPLICIT UniqueIdentifier OPTIONAL]],
            [[3: -- if present, version shall be v2 or v3
            extensions [3] Extensions OPTIONAL]]
```

202 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

```
            -- If present, version shall be v3]]
```

```
} (CONSTRAINED BY { -- shall be DER encoded -- } )
```

In order to meet the security goals, the R5F SBL and the HSM runtime image needs to have an X.509 certificate attached to the binary images. The Boot-ROM will only load images which have a valid X.509 certificate attached to them. 

## _**5.7.3 Certificate expectations**_ 

ROM expectations from the certificate for HS-FS and HS-SE devices is as follows: 

|**Device Type**|**Validation requirements for SBL**|**Validation requirements for SBL**|**Validation requirements for SBL**|**Validation requirements for HSM RT**|**Validation requirements for HSM RT**|**Validation requirements for HSM RT**|
|---|---|---|---|---|---|---|
||**Certificate**<br>**Verification**|**Image**<br>**Integrity**|**Image**<br>**Decryption**|**Certificate**<br>**Verification**|**Image**<br>**Integrity**|**Image**<br>**Decryption**|
|HSFS|No authentication,<br>only Dummy<br>certificate for<br>metadata|It’s supported, but<br>not mandatory,<br>SBL can boot with<br>or without image<br>integrity. Based<br>on the certificate<br>extension Image<br>integrity will<br>be carried out.<br>SHA512 only<br>supported.|Not supported on<br>HS-FS devices for<br>SBL. Boot fails if<br>encrypted images<br>are loaded.|Authentication is<br>must and it’s with<br>TI root of trust<br>(RoT). RSA4K<br>only supported.|It’s mandatory,<br>ensure that<br>certificate<br>extension is<br>present. SHA512<br>only supported.|It’s optional.<br>HSMRt can<br>boot without<br>image decryption.<br>Certificate<br>extension for<br>Image decryption<br>will decide<br>this feature.<br>AES256-CBC only<br>supported.|
|HSSE|Authentication is<br>must and it’s<br>with Customer<br>root of trust<br>(RoT). RSA4K<br>only supported.|It’s mandatory,<br>ensure that<br>certificate<br>extension is<br>present. SHA512<br>only supported.|It’s optional. SBL<br>can boot without<br>image decryption.<br>Certificate<br>extension for<br>Image decryption<br>will decide<br>this feature.<br>AES256-CBC only<br>supported.|Authentication is<br>must and it’s<br>with Customer<br>root of trust<br>(RoT). RSA4K<br>only supported.|It’s mandatory,<br>ensure that<br>certificate<br>extension is<br>present. SHA512<br>only supported.|It’s optional.<br>HSMRt can<br>boot without<br>image decryption.<br>Certificate<br>extension for<br>Image decryption<br>will decide<br>this feature.<br>AES256-CBC only<br>supported.|



## _**5.7.4 Object Identifiers**_ 

Oject Identifiers or OIDs are an identifier mechanism standardized by ITU and ISO/IEC for naming any object, concept, or "thing" with a globally unambiguous persistent name. 

An OID corresponds to a node in the "OID tree" or hierarchy, which is formally defined using the ITU's OID standard, X.660. 

OID denoting 1.3.6.1.4.1.294.1 is used and followings are the OID Tree. 

- 1 ISO, 

- 1.3 identified-organization, 

- 1.3.6 dod, 

- 1.3.6.1 internet, 

- 1.3.6.1.4 private, 

- 1.3.6.1.4.1 enterprise, 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

203 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

- 1.3.6.1.4.1.294 Texas Instruments, 

- 1.3.6.1.4.1.294.1 Device-Boot 

## **5.7.4.1 Boot Information OID (1.3.6.1.4.1.294.1.1)** 

The Boot Information Object Identifier has the following format:- 

```
bootInfo ::=  SEQUENCE {
    cert_type:  INTEGER,        -- identifies the certificate type
    boot_core:    INTEGER,        -- identifies the boot core
    core_opts:    INTEGER,        -- Core Options
    load_addr:    OCTET STRING,    -- Global address image destination
    image_size:    INTEGER,        -- Image size in bytes
}
```

## **DESCRIPTION** 

The Boot Information Object identifier provides information about the image which is being loaded. This information is mandatory and needs to be present in the all the X.509 certificates else the image boot will fail. 

## **OPTIONS** 

Certificate Type: The certificate type defines the type of the image which is being loaded by the Boot-ROM. The following table illustrates the supported values. 

|**Value**|**Description**|
|---|---|
|0x1|R5 SBL Boot Image|
|0x2|HSM Runtime Image|



**Boot core:** The boot core identifies the core on which the image will be executing. 

|**Value**|**Description**|
|---|---|
|0x0|HSM Core|
|0x10|R5 Core|



**Core Options:** The core options are documented in the table below. 

|**Value**|**Description**|
|---|---|
|0x0|Lock Step Mode|
|**Non-Zero**|Dual Core Mode|



The core options work in conjunction with the following EFUSE configurations:- 

1. DUAL_CORE_BOOT_ENABLE 

2. DUAL_CORE_SWITCH_DISABLE 

These will determine the final operational mode in which the R5 will be executed. The following table summarizes the operation: 

204 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

|**Dual Core Boot Enable**|**Dual Core Switch Disable**|**Core**<br>**Options**|**Description**|
|---|---|---|---|
|**0**|1|0|**Case1:**<br>Executing in Lock Step Mode<br>Switching to dual boot is<br>*Disabled*<br>Certificate requests to execute in<br>Lock Step Mode<br>**Result:**<br>R5 will be started in Lock Step<br>Mode.|
|**0**|1|1|**Case2:**<br>Executing in Lock Step Mode<br>Switching to dual boot is<br>*Disabled*<br>Certificate requests to execute in<br>Dual Core Mode<br>**Result:**<br>Error: Dual Boot Switching is<br>disabled|
|**0**|0|0|**Case3:**<br>Executing in Lock Step Mode<br>Switching to dual boot is<br>*Enabled*<br>Certificate requests to execute in<br>Lock Step Mode<br>**Result:**<br>R5 will continue to execute in<br>Lock Step Mode|
|**0**|0|1|**Case4:**<br>Executing in Lock Step Mode<br>Switching to dual boot is<br>*Enabled*<br>Certificate requests to execute in<br>Dual Core Mode<br>**Result:**<br>R5 will switch from Lock Step to<br>Dual Core Mode.|
|**1**|1|0|**Case5:**<br>Executing in Dual Core Mode<br>Switching to dual boot is<br>*Disabled*<br>Certificate requests to execute in<br>Lock Step Mode<br>**Result:**<br>Error: Switching from Dual Core<br>to Lock Step is not allowed.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

205 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

|**Dual Core Boot Enable**|**Dual Core Switch Disable**|**Core**<br>**Options**|**Description**|
|---|---|---|---|
|**1**|1|1|**Case6:**<br>Executing in Dual Core Mode<br>Switching to dual boot is<br>*Disabled*<br>Certificate requests to execute in<br>Dual Core Mode<br>**Result:**<br>R5 will continue to execute in<br>Dual Core Mode.|
|**1**|0|0|**Case7:**<br>Executing in Dual Core Mode<br>Switching to dual boot is<br>*Enabled*<br>Certificate requests to execute in<br>Lock Step Mode<br>**Result:**<br>Error: Switching from Dual Core<br>to Lock Step is not allowed.|
|**1**|0|1|**Case8:**<br>Executing in Dual Core Mode<br>Switching to dual boot is<br>*Enabled*<br>Certificate requests to execute in<br>Dual Core Mode<br>**Result:**<br>R5 will continue to execute in<br>Dual Core Mode.|



Core options are applicable only for the R5 SBL Images and will be ignored for HSM Runtime certificates. 

**Load Address:** The load address will be the address in the system where the image will be loaded. This information is provided and the R5 SBL and HSM Runtime developers need to ensure that the images account for this. 

|**Value**|**Description**|
|---|---|
|0x70002000|R5 SBL Load Address|
|0x0|HSM Runtime Load Address|



Image Size: This is the size in bytes of the R5 SBL or HSM Runtime Image to which the certificate has been attached. 

## **5.7.4.2 Software Revision OID (1.3.6.1.4.1.294.1.3)** 

The Software Revision Object Identifier has the following format: - 

```
softwareRevision: = SEQUENCE {
   revision:    INTEGER -- Software revision
}
```

## **DESCRIPTION** 

The information in the software revision is used to indicate the version of the image which is being loaded. 

## **revision:** 

206 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

This is the version number. This will be matched to the EFUSE programmed version to indicate if the image loading should be done or not. 

## **Note** 

This is applicable only for HSSE devices. HSM Runtime + R5 SBL 

## The following table summarizes the behavior: 

|**EFUSE Revision**|**Certificate Revision**|**Description**|
|---|---|---|
|0|0|Ignore the revision checking. Images will<br>*always* be loaded|
|0|>0|Device does not mandate revision checking.<br>Images will be loaded|
|>0|0|EFUSE Version > Certificate Version. Image<br>will *never* be loaded.|
|>0|>0|Image will be loaded only if the Certificate<br>revision >= EFUSE revision|



Revision Information is read from the following EFUSE fields. 

|**EFUSE**|**Description**|
|---|---|
|SWRV_SBL|This is used to perform the revision checking while loading the R5<br>SBL|
|SWRV_HSM|This is used to perform the revision checking while loading the HSM<br>Runtime|



The number of bits for each of the EFUSE in the table above is 64bits. The revision EFUSE supports dual redundancy; this implies that a maximum of 32 revisions can be supported. 

Note: The EFUSE SWRV_APP is read and is passed as is by the HSM Boot ROM to the application via the Asset Interface. This EFUSE has a length of 192bits and the interpretation of this is left to the HSM Runtime developers. 

## **5.7.4.3 Image Integrity OID (1.3.6.1.4.1.294.1.2)** 

The Image Integrity Object Identifier has the following format: - 

```
imageIntegrity ::= SEQUENCE {
    sha_type:    OID,            -- Identifies the SHA type
    hash:        OCTET STRING    -- The SHA of the boot image
}
```

## **DESCRIPTION** 

If the X.509 certificate provides the image integrity boot extension the Boot-ROM will perform the SHA-512 on the entire image and will verify the computed hash with the hash provided in the boot extension. In the case of a mismatch the boot will fail. 

**SHA Type:** The Boot-ROM only supports SHA-512. 

|**Value**|**Description**|
|---|---|
|2.16.840.1.101.3.4.2.3|SHA-512 Object Identifier|



Please refer to the Section 2.4 of the RFC-5754 for the SHA-512 Object Identifier. 

**Hash:** This is SHA-512 hash which is calculated over the image (R5 SBL/HSM Runtime) 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

207 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## **5.7.4.4 Image Encryption OID (1.3.6.1.4.1.294.1.4)** 

The Image Encryption Object Identifier has the following format: - 

```
imageEncryption ::= SEQUENCE {
   iv:        OCTET STRING -- The initialization vector
   rs:          OCTET STRING -- Random string
   iter:        INTEGER      -- Iteration count
   salt:        OCTET STRING -- encryption salt value
}
```

## **DESCRIPTION** 

The Boot-ROM only supports AES-CBC mode with 256bit keys. The information in the image encryption object identifier is used to decrypt the image. 

## IV: 

The initialization vector is used during the AES-CBC decryption procedure. The initialization vector needs to be 16bytes. 

## rs: 

This is the random string which is 32bytes long and is added by the X.509 certificate generator at the end of the image. The Boot-ROM will decrypt the image and will perform a random string comparison to determine if the decryption was successful. 

## iter: 

Iteration Count which is used to determine if the HKDF needs to be performed and key derivation needs to be done. If the iteration count is 0 then the key from the e-fuse is used as is for the decryption. If the iteration count is non-zero then the Boot-ROM will perform the HKDF key derivation using the salt. The derived key is then used for the decryption operation. 

## salt: 

The salt is used only if the iteration count is non-zero and key derivation is being done. The salt is fed to the HKDF module to derive the key. The salt fields should be 32bytes. 

## **5.7.4.5 Derivation OID (1.3.6.1.4.1.294.1.5)** 

The Derivation Object Identifier has the following format:- 

```
derivationKey ::= SEQUENCE {
   salt:      OCTET STRING -- encryption salt value
   info:      OCTET STRING –- [optional]information
}
```

## **DESCRIPTION** 

The Boot-ROM will leave a derived key in the assets interface for the HSM Runtime. The key is derived using HKDF from the parameters specified here. 

salt: The salt is limited to be 32bytes and is used for key derivation 

info: The information is optional in which case the size of the information is set to 0 but if specified is limited to 32bytes. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

208 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## **Note** 

- If this extension is not present, derived key will be the same across SBL/hsmRT and application 

- If this extension is present, derived key will not be the same as SBL/hsmRT 

## **5.7.4.6 Debug OID (1.3.6.1.4.1.294.1.8)** 

The Debug Object Identifier has the following format:- 

```
Debug::= SEQUENCE {
      uid          OCTET STRING     -- Device unique ID
      debugType    INTEGER          -- Debug type
      coreDbgEn    INTEGER          -- Enable core debug mask
      secCoreDbgEn INTEGER          -- Enable secure core debug mask
}
```

## **DESCRIPTION** 

The debug object identifier if specified allows the debug ports to be enabled for a specific device. It also can be used to specify the Key protections. 

## OPTIONS 

UID: This is the unique identifier associated with the device. Device specific unique identifiers can be retrieved using the following: - 

1. SOC Identifier while operating in a peripheral boot mode 

2. Assets on the successful load of the HSM Runtime 

The UID field of all 0’s is considered to be a wildcard. 

## **Debug Type:** 

The debug type is described as follows:- 

|**31**|**18**|**16**|**15**|||**0**|
|---|---|---|---|---|---|---|
|Reserved||CUST|Debug Type||||



## **Key Protections:** 

|**Key Protection**|**Value**|**Description**|
|---|---|---|
|**CUST**|0|Do not disable access to customer keys|
||1|Disable access to customer keys|



## **Debug Type:** 

|**Value**|**Description**|
|---|---|
|**0**|Disable debug|
|**1**|Preserve debug state|
|**2**|Enable non-secure debug (Public Debug)|
|**3**|Reserved|
|**4**|Enable secure and non-secure debug (Full Debug)|
|**5-65635**|Reserved|



**coreDbgEn and secCoreDbgEn:** These fields are not used and will be ignored. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 209 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## **Note** 

|R5 SBL Image:|R5 SBL Image:|•<br>Optional.<br>•<br>Wildcard UID is allowed.<br>•<br>Key Protections are ignored<br>•<br>Debug Type = 0, 1 and 2 for HS-SE devices<br>•<br>Debug Type = 0 and 1 for HS-FS devices since R5 JTAG is opened by default.<br>•<br>Debug Type = 4 is Invalid|
|---|---|---|
|HSM Runtime Image:||•<br>Debug OID is not applicable and is ignored|
||||
|Outer certificate|•<br>Certificate verification is done with the TI Public Key<br>•<br>Debug Boot Extension is**mandatory**.<br>•<br>UID in the debug extension could either be wild-carded or match the device<br>•<br>Key protection is ignored<br>•<br>Debug Type shall be 4 since we need to unlock the JTAG to debug the HSM Boot-ROM||



## _**5.7.5 Binary Image Creation**_ 

For secure devices, the process is illustrated in Figure 5-5, and includes the following steps: 

1. Create X.509 certificate (1a). 

2. Populate certificate extension fields: write image load address and value of the Magic Number from the unencrypted image (1b). 

3. Populate image SW version (1c). 

4. Encrypt (AES-256-CBC) binary image using derived 256-bit Symmetric Key (2). 

5. Compute hash (SHA-512) of encrypted image (3a), and write the digest value to the certificate (3b). 

6. Public key is written into the certificate. This can be RSA based public key information. 

7. Whole certificate is hashed (SHA-512) (4a), encrypted with private key (4b) using RSA and signature is inserted back into certificate (4c). 

210 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

**==> picture [500 x 426] intentionally omitted <==**

**Figure 5-5. Binary Image Creation** 

## **Note** 

When creating a binary image for an HS-FS device, only step 1 is required. Optionally, binary image hashing (step 5) can be performed to verify image integrity. 

TI provides reference scripts and tools for certificate generation and boot image creation in the HSM/ Security software package provided through TI Secure Resources. 

ROM bootloader supports only RSA4K, SHA512 and AES-CBC-256. 

## _**5.7.6 Binary Image Verification**_ 

Binary images are verified by HS-SE devices, as illustrated in Figure 5-6. The process includes the following steps: 

1. Compute hash (SHA-512) of the public key in certificate (1a), and compare with the stored public key hash value (1b). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

211 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

2. Hash (SHA-512) the certificate (2a), decrypt the signature using the public key (2b), and verify the match (2c). 

3. Determine whether software revision is allowed (3). 

4. Read the binary image load address from the certificate. 

5. Compute hash (SHA-512) of the encrypted image (4a), and compare with the code hash value from the certificate (4b). 

6. Decrypt code (AES-256-CBC) using the 256-bit key derived from the symmetric key (5), if required. 

7. Verify the value of the magic number from the certificate and from clear text binary image. 

**==> picture [480 x 300] intentionally omitted <==**

**----- Start of picture text -----**<br>
fuseROM<br>fuseROM<br>**----- End of picture text -----**<br>


**Figure 5-6. Binary Image Verification** 

## _**5.7.7 R5 SBL Handoff**_ 

**Figure 5-7** shows the different stages involved after successful validation of the certificate and the image of the SBL: 

1. R5 SBL available at L2 address 0x70002000 

2. HSM copies 640 bytes from the address 0x70002000 to TCMA start address 0x20000. These 640 bytes consists of IVT and initialization code 

3. After the copy, R5 ROM eclipse process is initiated which involves masking R5 ROM and mapping TCMA start address to 0x0 address 

4. R5 core reset is issued 

5. R5 starts execution from 0x0 

212 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

**==> picture [500 x 256] intentionally omitted <==**

**Figure 5-7. R5 SBL HandOff** 

## _**5.7.8 HSM RunTime Handoff**_ 

**Figure 5-8** shows different stages involved in the HSM RunTime boot 

1. HSM Runtime available at L2 address 

2. SBL sends ‘ **LoadHSMRt** ’ message to HSM ROM , message will have L2 address pointing to hsmRT image 

3. HSM ROM validates the certificate 

4. On successful validation of the certificate, HSM ROM copies entire binary from L2 to IRAM address 0x20000 

5. After the binary is copied, HSM ROM validates the image against integrity followed by image decryption (image decryption is optional). 

6. HSM ROM eclipse process is initiated after image validation is success. This involves masking HSM ROM and mapping IRAM start address to 0x0 address 

7. HSM core reset is issued 

8. HSMRt starts execution from 0x0 

When HSM gets eclipsed, the IRAM RAM address region is mapped to ROM address region. Address mapping during normal and ROM Eclipse Mode is captured in the below tables. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 213 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

**==> picture [500 x 290] intentionally omitted <==**

**Figure 5-8. HSM RunTime HandOff** 

**Table 5-12. Address Mapping when HSM ROM is not eclipsed** 

|**M4 Address**|**SCR Hardware Address**<br>**Translation**|**Size(KB)**|**Category**|
|---|---|---|---|
|0x0000 0000|0x2000 0000|48|Non-secure ROM|
|…|…|||
|0x0000 BFFF|0x2000 BFFF|||
|0x0001 0000|0x2001 0000|48|Secure ROM|
|…|…|||
|0x0001 BFFF|0x2001 BFFF|||



214 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

**Table 5-12. Address Mapping when HSM ROM is not eclipsed (continued)** 

|0x0002 0000|0x2002 0000|256|IRAM|
|---|---|---|---|
|…|…|||
|0x0000 7FFF|0x2000 7FFF|||
|0x0002 8000|0x2002 8000|||
|…|…|||
|0x0002 FFFF|0x2002 FFFF|||
|0x0003 0000|0x2003 0000|||
|…|…|||
|0x0003 FFFF|0x2003 FFFF|||
|0x0004 0000|0x2004 0000|||
|…|…|||
|0x0004 FFFF|0x2004 FFFF|||
|0x0005 0000|0x2005 0000|||
|…|…|||
|0x0005 FFFF|0x2005 FFFF|||
|**Table 5-13. Address Mapping when HSM ROM is eclipsed**||||
|**M4 Address**|**SCR + Eclipse Hardware**<br>**Address Translation**|**Size**|**Category**|
|0x0000 0000|0x2002 0000|256KB|RAM|
|…|…|||
|…|…|||
|0x0003 FFFF|0x2005 FFFF|||
|0x0004 0000|0x2000 0000|64KB|Reserved space|
|…|…|||
|0x0004 FFFF|0x2000 FFFF|||
|0x0005 0000|0x2001 0000|64KB|Reserved space|
|…|…|||
|0x0005 FFFF|0x2001 FFFF|||



## _**5.7.9 Post Boot Status**_ 

## **5.7.9.1 R5** 

## _**5.7.9.1.1 Memory**_ 

Memory used by R5 Boot-Rom and their status is shown in Table 5-14. Memory not used by R5 is untouched by Boot-Rom. 

**Table 5-14. R5 Memory** 

|**Memory type**|**Status**|
|---|---|
|TCMA|SBL IVT and init code runs from TCMA have been copied to TCMA. The maximum size of code in<br>TCMA is 640 bytes (refer to example SBL linker command file for more details).|
|TCMB|Open to be used by SBL|
|L2|Contains SBL image and certificate|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

215 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## _**5.7.9.1.2 Clock**_ 

**Table 5-15. R5 Clock** 

|**Clock type**|**Status**|
|---|---|
|R5 PLL_CORE_CLK|Running at 400MHz|
|R5 VCLK|Running at 200MHz|
|DPLL_CORE_HSDIV0_CLKOUT0|Running at 400MHz|



## _**5.7.9.1.3 IP Blocks**_ 

This is the state where the ROM Bootloader hands over the control to the Secondary BootLoader (SBL) 

**Table 5-16. R5 IP Blocks** 

|**IP**|**Status**|
|---|---|
|Timer|Disabled|
|VIM|All interrupts are disabled<br>VIM memory is cleared|
|Mail Box|Memory cleared|
|OSPI(OSPI Boot)|OSPI clock is disabled<br>OSPI is set to “Force idle”|
|EDMA (OSPI boot)|EDMA channel is disabled<br>paramSet memory is cleared<br>Channel to paramSet mapping is cleared|
|UART(UART boot)|UART0 is reset through IP’s soft reset|



## _**5.7.9.1.4 Pinmux Settings**_ 

Pinmux settings are left with the settings used for the boot mode. 

For OSPI flash boot, OSPI interface pins are left configured as OSPI boot. UART pins are NOT touched in this boot mode. 

For UART boot, UART pins are left configured as UART boot. OSPI pins are NOT touched in this boot mode. 

**Table 5-17. R5 Pinmux Settings** 

|**Boot Mode**|**OSPI Pin Status**|**UART Pin Status**|
|---|---|---|
|OSPI|MCAN1_TX=>MCAN1_TX(Default Pull)<br>MCAN1_RX=>MCAN1_RX (Default Pull)<br>MCAN0_TX=>MCAN0_TX(Default Pull)<br>MCAN0_RX=>MCAN0_RX(Default Pull)<br>QSPI0_D3=>QSPI_D3(Default Pull)<br>QSPI0_D2=>QSPI_D2 (Default Pull)<br>QSPI0_D1=>QSPI_D1(Default Pull)<br>QSPI0_D0=>QSPI_D0(Default Pull)<br>QSPI0_CLK0=>QSPI_CLK (Default Pull)<br>QSPI0_CSn0=>QSPI_CS (Default Pull)<br>QSPI_CLKLB =>QSPI_CLKLB(Default Pull)|Same as reset|
|UART|Same as reset|UART0_TXD=>UART0_TX D(Default Pull)<br>UART0_RXD=>UART0_RXD (Default Pull)|



## _**5.7.9.1.5 PBIST**_ 

BootRom executes the PBIST test for the following memory groups used by ROM during boot: 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

216 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## **Table 5-18. R5 PBIST** 

|**Memory Group Number**|**Memory Group Description**|**Memory Group**|
|---|---|---|
|15|MEM_TOP_PBISTROM|PBIST_RINFOL[14]|
|23|MEM_MSS_L2_0|PBIST_RINFOL[22]|
|24|MEM_MSS_L2_1|PBIST_RINFOL[23]|
|40|MEM_MSS_CR5A_ATCM0_R5SS0 Core0<br>TCMA|PBIST_RINFOU[7]|
|41|MEM_MSS_CR5A_ATCM0_R5SS1 Core0<br>TCMA|PBIST_RINFOU[8]|
|42|MEM_MSS_CR5A_BTCM0_R5SS0 Core0<br>TCMB|PBIST_RINFOU[9]|
|43|MEM_MSS_CR5A_BTCM0_R5SS1 Core0<br>TCMB|PBIST_RINFOU[10]|



## **Note** 

ROM does not perform LBIST 

## **Note** 

PBIST status information available at: 

- pbistStatus_l @0x00084104 

- pbistStatus_u @0x00084108 

## **Note** 

ROM always loads SBL to L2 bank 0, so that the SBL can still do a PBIST on L2_1 as there is nothing in it from ROM’s perspective 

## **5.7.9.2 Assets** 

Once the HSM Boot-ROM has loaded the HSM Runtime, it will leave behind Assets which are located at the beginning of the SECURE RAM. This information is made available for the development of the HSM Runtime. Please refer to _ROM External Interface documentation_ in HSM/Security software package which describes this asset structure details and the start address. 

Assets recorded are as follows: 

1. HSM Boot ROM Version 

2. Device Type (HS-FS, HS-SE etc.) 

3. Key revision and count 

4. Derived Key (Using the Derivation Object Id) 

5. Public Key 

6. Unique Device Identifier, etc. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 217 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## **5.8 Boot Image Format** 

## _**5.8.1 Overall Structure**_ 

The boot image consists of an X.509 Certificate followed immediately by a boot image blob. 

X.509 Certificate (Variable Size) (Optional) Boot Image Blob (Variable Size) 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

218 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## _**5.8.2 Generating X.509 Certificates**_ 

X.509 Certificates are generated using OpenSSL and a configuration script to supply values in the extension fields. 

## **5.8.2.1 Key Generation** 

The SBL must always be signed with a given OpenSSL key. Secure devices must have encryption and authentication. The key used for authentication can be random or specific. If a random key is generated and SBL is signed with this,the ROM will copy the SBL image for authentication using memcopy. With this key, ROM code will be directed to use DMA to load the SBL for authentication which saves boot time. 

## _**5.8.2.1.1 RSA Key Generation**_ 

Signature = digestprivExp mod nprivExp mod n[privExp] 

(1) 

Where n is the key size. Since the hash used is SHA-512 and the signature is an ASN.1 sequence containing the OID defining which has was used as well as the hash value, the degenerate RSA must have a value of n greater than the maximum digest size. Typically 4096-bit is chosen. 

## **Note** 

AM263Px Supports the following parameters: 

- Public Key Length: RSA4K 

- Decryption: AES-256 CBC 

- Hashing: SHA512 

The following sequence is used to generate degenerate RSA keys: 

1. Create a random RSA key: 

```
openssl genrsa –out key.pm 4096
```

2. Convert to text: 

```
openssl rsa –in key.pem –text –noout > key.txt
```

3. Create an asn1 template for the degenerate key called degenerateKey.txt. Simply copy the values for modulus, prime (listed as p in key.txt), prime 2 (listed as q), and coefficient (listed as coeff). Set the public and private key exponents to 1, as well as the values for e1 and e2. See the example below. 

4. Convert the template to DER: 

```
openssl asn1parse -genconf degenerateKey.txt -out degenerateKey.der
```

5. Sanity check the key: 

```
 openssl rsa –in degenerateKey.der –inform der -text -check
```

6. If there are no errors create the degenerate key pem file: 

```
openssl rsa –in degenerateKey.der –inform der –outform pem -out degenerateKey.pem
```

An example degenerateKey.txt file is shown. 

```
asn1=SEQUENCE:rsa_key
[rsa_key]
version=INTEGER:0
modulus=INTEGER<copied from key.txt>
pubExp=INTEGER:1
privExp=INTEGER:1
p=INTEGER:<copied from key.txt>
q=INTEGER<copied from key.txt>
```

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

219 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

```
e1=INTEGER:1
e2=INTEGER:1
coeff=INTEGER<copied from key.txt>
```

Note that when copying the multi-byte fields from key.txt it is necessary to remove the colons, concatenate the lines and add a preceding 0x. 

Degenerate RSA keys are valid RSA keys with the private exponent set to 1. This results in the signature field being equal to the digest. 

## **5.8.2.2 Configuration Script** 

An example openssl configuration script is shown below. Not all extensions are required, but all possible are shown. 

```
[ req ]
distinguished_name = req_distinguished_name
X509_extensions = v3_ca
prompt = no
dirstring_type = nobmp
[ req_distinguished_name ]
C = GB
ST = HI
L = Boston
O = Texas Instruments., Inc.
OU = DSP
CN = Bob
emailAddress = Bob@hou.ti.com
[ v3_ca ]
basicConstraints = CA:true
1.3.6.1.4.1.294.1.1 = ASN1:SEQUENCE:boot_seq
1.3.6.1.4.1.294.1.2 = ASN1:SEQUENCE:image_integrity
1.3.6.1.4.1.294.1.3 = ASN1:SEQUENCE:swrv
1.3.6.1.4.1.294.1.4 = ASN1:SEQUENCE:encryption
1.3.6.1.4.1.294.1.5 = ASN1:SEQUENCE:key_derivation
1.3.6.1.4.1.294.1.8 = ANSI:SEQUENCE:debug
[ boot_seq ]
certType =INTEGER:1
bootCore = INTEGER:16
bootArchWidth = INTEGER:32
destAddr = FORMAT:HEX,OCT:bc934b00
imageSize = INTEGER:0x00004860
[ image_integrity ]
shaType = OID:2.16.840.1.101.3.4.2.3
shaValue = FORMAT:HEX,OCT:4cf4d59ef77b5d9ab28d2ceb3c9fe83cb52ae6d2
[ swrv ]
rollback = INTEGER:0x00010001
[ encryption ]
Iv =FORMAT:HEX,OCT:00112233445566778899aabbccddeeff
Rstring = FORMAT:HEX,OCT:00112233445566778899aabbccddeeff101112131415161718191a1b1c1d1e1f
Icount = INTEGER:1
Salt = FORMAT:HEX,OCT:00112233445566778899aabbccddeeff
[ pllControl ]
[ debug ]
uid = FORMAT:HEX,OCT:00345678900
type = INTEGER:1
dbgE = INTEGER:0
secDbgEn = INTEGER:0
```

The certificate is then generated using the following openssl command: 

```
openssl req -new -x509 -key <private_key_pem_file> -nodes -out <output_X.509_pem_file> -config
<config_file> -sha512
```

If a delegate key is being signed, then add the option -signkey <sign_key_pem_file> to the command above. 

220 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## **5.8.2.3 Image Data** 

The image data (blob) is considered simply as a byte stream. On devices that are multiple bytes wide (for example, PCIe) the image must be formatted so that all multi-byte fields match the endianness of the device. The MCU will always run in little endian mode. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 221 

Copyright © 2025 Texas Instruments Incorporated 

_Initialization_ 

www.ti.com 

## **5.9 Boot Memory Maps** 

## _**5.9.1 Memory Layout/MPU**_ 

Table 5-19 shows an overview of the MPU configuration. In the R5FSS MPU, higher numbered regions have priority, therefore, where two regions overlap, the right-most region column defines the memory attributes in the table. 

**Table 5-19. Memory Layout/MPU** 

|**Memory Address**|**Regions**|**Regions**|
|---|---|---|
|0x0000_0000|Region 1 - Non-executable Full Access|Region 2 - ROM Read-only Exec|
|0x0001_FFFF|||
|………….|||
|0x0002_0000||Region 3 - TCM User Access|
|0x0002_3FFF|||
|………….|||
|0x0008_0000||Region 4 - ROM User Access|
|0x0008_3FFF|||
|………….|||
|0x4400_0000||Region 7 - TX Mailbox RAM|
|0x440F_FFFF|||
|………….|||
|0x5380_0000||Region 10 - OSPI Config Space|
|0x5380_FFFF|||
|………….|||
|0x6000_0000||Region 9 - OSPI Memory|
|0x67FF_FFFF|||
|………….|||
|0x7000_0000||Region 5 - All OCSRAM|
|0x703F_FFFF|||
|………….|||
|0x7200_0000||Region 8 - RX Mailbox RAM|
|0x720F_FFFF|||
|………….|||
|0xFFFF_FFFF|||



222 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Initialization_ 

## _**5.9.2 Logger**_ 

The ROM code uses logger module for debug information. They are shown in the below table: 

**Table 5-20. Global Memory Addresses** 

|**Group**|**Address**|**Size (bytes)**|**Content**|
|---|---|---|---|
|Infor/Warning/Error Logs|0x0008_2800|4096|Log Entry size: 8 words (128 bits)<br>Word 1: Log_type -<br>0xABCD001 - lnfo 0xABCD002<br>- Warning 0xABCD003 - Error<br>0xABCD004 - Critical<br>2nd word: FileName - source file<br>name<br>3rd word: Line number - line at<br>which log reported in the source<br>file<br>4th word: Value1 - Debug word1<br>5th word: Value2 - Debug word2<br>6th word: Timer count (lower) -<br>lower 32-bit timer count 7th word:<br>Timer count (upper) - upper 32-bit<br>timer count|



## **Failure and recovery** 

Any failures detected by R5 or HSM while booting, will lead to SoC warm reset issued by WDT (watchdog timer) after 180 sec. From the ROM perspective, cold reset and warm reset are the same as far as boot flow is considered. 

The ROM code version information is a structure shown in Table 5-21 

**Table 5-21. ROM Code Version** 

|**Field**<br>**Address**<br>**Size (bytes)**<br>**Value**|**Field**<br>**Address**<br>**Size (bytes)**<br>**Value**|**Field**<br>**Address**<br>**Size (bytes)**<br>**Value**|**Field**<br>**Address**<br>**Size (bytes)**<br>**Value**|
|---|---|---|---|
|Version Number|0x4605_0940|4|"0x0001_0000" (1.0.0)|
|Device Name|0x4605_0944|12|"am263Px"|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

223 

Copyright © 2025 Texas Instruments Incorporated 

