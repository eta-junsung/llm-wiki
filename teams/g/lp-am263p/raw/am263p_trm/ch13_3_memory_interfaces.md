<!-- AM263P TRM | 13.3 Memory Interfaces (MMC, OptiFlash/OSPI) | 원본 p.1375-1485 | pymupdf4llm text+tables, images omitted -->

www.ti.com 

_Peripherals_ 

## **13.3 Memory Interfaces** 

This section describes the memory interfaces in the device. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1375 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1 Multimedia Card (MMC)**_ 

This chapter describes the MMC of the device. 

## **13.3.1.1 Introduction** 

## _**13.3.1.1.1 MMCSD Features**_ 

The general features of the MMCSD host controller IP are: 

- Built-in 1024-byte buffer for read or write 

- Two DMA channels, one interrupt line 

- Clock support 

   - up to 192Mbit/sec (24MByte/sec) in MMC mode 4-bit data transfer 

   - up to 192Mbit/sec (24MByte/sec) in High-Speed SD mode 4-bit data transfer 

   - up to 24Mbit/sec (3MByte/sec) in Default SD mode 1-bit data transfer 

- Support for SDA 3.0 Part A2 programming model 

- Serial link supports full compliance with: 

   - MMC command/response sets as defined in the MMC standard specification v4.3. 

   - SD command/response sets as defined in the SD Physical Layer specification v2.00 

   - SDIO command/response sets and interrupt/read-wait suspend-resume operations as defined in the SD part E1 specification v 2.00 

   - 

- SD Host Controller Standard Specification sets as defined in the SD card specification Part A2 v2.00 

## _**13.3.1.1.2 Unsupported MMCSD Features**_ 

The MMCSD module features not supported in this device are shown in Table 13-161. 

**Table 13-161. Unsupported MMCSD Features** 

|**Feature**|**Reason**|
|---|---|
|Controller DMA (ADMA) operation|Disabled through synthesis parameter|
|Card Supply Control (MMCSD(1-2))|Signal not pinned out|
|Dual Data Rate (DDR) mode|Timing not supported|



1376 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.3.1.2 Integration** 

This device contains one instance of the Multimedia Card (MMC), Secure Digital (SD), and Secure Digital I/O (SDIO) high speed interface module (MMCSD). The controller provides an interface to an MMC, SD memory card or SDIO card. 

The application interface is responsible for managing transaction semantics; the MMC/SDIO host controller deals with MMC/SDIO protocol at transmission level, packing data, adding CRC, start/end bit and checking for syntactical correctness. Figure 13-115 through Figure 13-117 below show examples of systems using the MMCSD controller. 

**==> picture [432 x 234] intentionally omitted <==**

**Figure 13-115. MMCSD Module SDIO Application** 

**==> picture [436 x 249] intentionally omitted <==**

**Figure 13-116. MMCSD (4-bit) Card Application** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1377 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [428 x 274] intentionally omitted <==**

**Figure 13-117. MMCSD Module MMC Application** 

1378 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.1.2.1 MMCSD Integration**_ 

There is 1x MMCSD integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [510 x 312] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>MMCSD#_VBUSCLK MMCSD#_DMA_RD_REQ<br>EDMA<br>MMCSD#_DMA_WR_REQ<br>SYS_CLK<br>WUCPUCLK MMCSD#_WP<br>EXT_REFCLK<br>DPLL_PER_HSDIV0_CLKOUT1<br>% MMCSD#_CLK<br>DPLL_CORE_HSDIV0_CLKOUT0 MMCSD#_CD<br>RCCLK10M (10MHz)<br>XTALCLK<br>4<br>RCCLK10M (10MHz) MMCSD#_D[0:3]<br>MMCSD#<br>MMCSD#_CLKSRC_SEL Bit<br>MMCSD#_CLKDIV_SEL Bit MMCSD#_CMD<br>% MMCSD#_32K_CLK<br>MMCSD#_32K_CLKDIV_SEL Bit MMCSD#_CLK<br>RCM<br>MMCSD#_RST_CTRL Bit<br>MMCSD#_INT_REQ R5FSS0-CORE0<br>M MCSD#_WARMRESET<br>Warm Reset Sources R5FSS0-CORE1<br>R5FSS1-CORE0<br>R5FSS1-CORE1<br>CORE INTERCONNECT<br>DMA XBAR<br>**----- End of picture text -----**<br>


## **Figure 13-118. MMCSD Integration** 

The tables below summarize the device integration details of the MMC/SD module. 

## **Table 13-162.** _**MMCSD**_ **Device Integration** 

## This table describes the module integration details. 

|**MMCSD Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|MMCSD0|✓|CORE VBUSM Interconnect|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1379 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-163.** _**MMCSD**_ **Clocks** 

This table describes the module clocking signals. 

|**MMCSD**<br>**Instance**|**MMCSD Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|MMCSD0|MMCSD0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|MMC/SD Interface Clock|
||MMCSD0_32K_CLK|MMCSD0_32K_CLK|XTALCLK|32 KHz|MMC/SD Debounce Clock|
||MMCSD0_FCLK<br>(MMCSD_CLK)|WUCPUCLK|Oscillator Clock|25 MHz|MMC/SD Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0 (not supported)|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator (RCCLK10M)|10 MHz||



**Table 13-164.** _**MMCSD**_ **Resets** 

This table describes the module reset signals. 

|**MMCSD**<br>**Instance**|**MMCSD Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|MMCSD0|MMCSD0_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|MMCSD0 Asynchronous Reset|



**Table 13-165.** _**MMCSD**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**MMCSD**<br>**Instance**|**MMCSD Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MMCSD0|MMCSD0_INT_req_0|MMCSD0_INT_req_0|ALL R5FSS Cores|Level|MMC/SD Interrupt|



**Table 13-166.** _**MMCSD**_ **DMA Requests** 

This table describes the module DMA requests. 

|**MMCSD**<br>**Instance**|**MMCSD DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MMCSD0|MMCSD0_DMA_RD_<br>REQ|MMCSD0_DMA_RD_REQ|EDMA Crossbar<br>(DMA_XBAR)|Level|MMC/SD DMA Read Request|
||MMCSD0_DMA_WR_<br>REQ|MMCSD0_DMA_WR_REQ|||MMC/SD DMA Write Request|



1380 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

## _**13.3.1.2.2 MMCSD Connectivity Attributes**_ 

The general connectivity attributes for the three MMCSD modules are shown in Table 13-167. 

**Table 13-167. MMCSD Connectivity Attributes** 

|**Attributes**|**Type**|
|---|---|
|Power Domain|Peripheral Domain|
|Clock Domain|SYS_CLK (OCP)<br>MMCSD_FCLK (Func)<br>MMCSD_32K_CLK (Debounce)|
|Reset Signals|PER_DOM_RST_N|
|Idle/Wakeup Signals|Smart Idle|
|Interrupt Requests|1 interrupt per instance to MPU Subsystem (MMCSDxINT)|
|DMA Requests|2 DMA requests per instance to EDMA (SDTXEVTx, SDRXEVTx)<br>(Active low, need to be inverted in glue logic)|
|Physical Address|0x48300000|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1381 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1.2.3 MMCSD Clock and Reset Management**_ 

The MMCSD controller has separate bus interface and functional clocks. Table 13-168 details the MMCSD controller clocks, max frequencies, and clock sources. 

**Table 13-168. MMCSD Clock Signals** 

|**Clock Signal**|**Max Freq**|**Reference / Source**|**Comments**|
|---|---|---|---|
|CLK<br>Interface clock|100 MHz|SYS_CLK / 2|SYS_CLK|
|CLKADPI<br>Functional clock|48 MHz|PER_HSDIV0_CLKOUT1 / 4|MMCSD_FCLK<br>from PER_HSDIV0_CLKOUT1|
|CLK32<br>Input de-bounce clock|32 KHz|RCCLK_32K|MMCSD_32K_CLK<br>from RCOSC32K|



## **Note** 

Maximum MMC_CLK signal frequency is 48 MHz. 

## _**13.3.1.2.4 MMCSD Pin List**_ 

The MMCSD interface pins are summarized in Table 13-169. 

**Table 13-169. MMCSD Pin List** 

|**Pin**|**Type**|**Description**|
|---|---|---|
|MMC_x__CLK|I/O(1)|MMC/SD serial clock output|
|MMC_x__CMD|I/O|MMC/SD command signal|
|MMC_x__DAT0|I/O|MMC/SD data signal|
|MMC_x__DAT1|I/O|MMC/SD data signal, SDIO interrupt input|
|MMC_x__DAT2|I/O|MMC/SD data signal, SDIO read wait output|
|MMC_x__DAT3|I/O|MMC/SD data signal|
|MMC_x__POW|O|MMC/SD power supply control (MMCSD0<br>only)|
|MMC_x__SDCD|I|SD card detect (from connector)|
|MMC_x__SDWP|I|SD write protect (from connector)|
|MMC_x__OBI|I|MMC out of band interrupt|



(1) These signals are also used as inputs to re-time or sync data. The associated CONF_<module>_pin_RXACTIVE bit for these signals must be set to 1 to enable the inputs back to the module. It is also recommended to place a 33-ohm resistor in series (close to the processor) on each of these signals to avoid signal reflections. 

The direction of the data lines depends on the selected data transfer mode as summarized in Table 13-170. 

**Table 13-170. DAT Line Direction for Data Transfer Modes** 

||**MMC/SD**<br>**1-bit mode**|**MMC/SD**<br>**4-bit mode**|**MMC/SD**<br>**8-bit mode**|**SDIO**<br>**1-bit mode**|**SDIO**<br>**4-bit mode**|
|---|---|---|---|---|---|
|DAT[0]|I/O|I/O|I/O|I/O|I/O|
|DAT[1]|I(1)|I/O|I/O|I(2)|I/O or I(2)|
|DAT[2]|I(1)|I/O|I/O|I/O(3)|I/O or O(3)|
|DAT[3]|I(1)|I/O|I/O|I(1)|I/O|



(1) Hi-Z state to avoid bus conflict. 

(2) To support incoming interrupt from the SDIO card. 

(3) To support read wait to the SDIO card. By default it is Input, Output only in read wait period. 

The direction of the MMCSD data buffers are controlled by ADPDATDIROQ signals. ADPDATDIROQ[i] = 1 sets the corresponding DAT signal(s) in read position (input) and ADPDATDIROQ[i] = 0 sets the corresponding DAT 

1382 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

signal(s) in write position (output). Additionally, the ADPDATDIRLS signals are provided (with opposite polarity) to control the direction of external level shifters. The value of these control signals for the various data modes are summarized in Table 13-171. 

**Table 13-171. ADPDATDIROQ and ADPDATDIRLS Signal States** 

||**MMC/SD**<br>**1-bit mode**|**MMC/SD**<br>**4-bit mode**|**MMC/SD**<br>**8-bit mode**|**SDIO**<br>**1-bit mode**|**SDIO**<br>**4-bit mode**|
|---|---|---|---|---|---|
|DAT[0]|ADPDATDIRLS[0] =<br>0 / 1<br>ADPDATDIROQ[0] =<br>1 / 0|ADPDATDIRLS[0] =<br>0 / 1<br>ADPDATDIROQ[0] =<br>1 / 0|ADPDATDIRLS[0] =<br>0 / 1<br>ADPDATDIROQ[0] =<br>1 / 0|ADPDATDIRLS[0] =<br>0 / 1|ADPDATDIRLS[0] =<br>0 / 1<br>ADPDATDIROQ[0] =<br>1 / 0|
|DAT[2]|ADPDATDIRLS[2] = 0<br>ADPDATDIROQ[2] =<br>1|ADPDATDIRLS[2] =<br>0 / 1<br>ADPDATDIROQ[2] =<br>1 / 0|ADPDATDIRLS[2] =<br>0 / 1<br>ADPDATDIROQ[2] =<br>1 / 0|ADPDATDIRLS[2] =<br>0 / 1<br>ADPDATDIROQ[2] =<br>1 / 0|ADPDATDIRLS[2] =<br>0 / 1<br>ADPDATDIROQ[2] =<br>1 / 0|
|DAT[1]|ADPDATDIRLS[1] = 0<br>ADPDATDIROQ[1] =<br>1|ADPDATDIRLS[1] =<br>0 / 1<br>ADPDATDIROQ[1] =<br>1 / 0|ADPDATDIRLS[1] =<br>0 / 1<br>ADPDATDIROQ[1] =<br>1 / 0|ADPDATDIRLS[1] = 0<br>ADPDATDIROQ[1] =<br>1|ADPDATDIRLS[1] =<br>0 / 1<br>ADPDATDIROQ[1] =<br>1 / 0|
|DAT[3]||||||



ADPDATIRLSx = 0 for input and 1 for output — these signals are not pinned out on this device. ADPDATIROQx = 1 for output and 1 for input. 

Grayed cells indicate that the data line is not used in the selected transfer mode. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1383 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.3.1.3 Functional Description** 

One MMC/SD/SDIO host controller can support one MMC memory card, one SD card, or one SDIO card. 

Other combinations (for example, two SD cards, one MMC card, and one SD card) are not supported through a single controller. 

## _**13.3.1.3.1 MMC/SD/SDIO Functional Modes**_ 

## _**13.3.1.3.1.1 MMC/SD/SDIO Connected to an MMC, an SD Card, or an SDIO Card**_ 

**==> picture [438 x 209] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>MMC_clk<br>CLK MMC card<br>MMC_cmd or<br>CMD SD card<br>MMC_dat[3:0] 4 or<br>SDIO  card<br>DAT[3:0]<br>MMC/SD/SDIO0 MMC_POW<br>Host  Controller<br>MMC_SDCD<br>MMC_SDWP<br>**----- End of picture text -----**<br>


## **Figure 13-119. MMC/SD0 Connectivity to an MMC/SD Card** 

Figure 13-119 shows the MMC/SD/SDIO0 host controller connected to an MMC, SD, or SDIO card and its related external connections. 

The following MMC/SD/SDIO controller pins are used 

- **MMC_CMD** 

   - This pin is used for two-way communication between the connected card and the MMC/SD/SDIO controller. The MMC/SD/SDIO controller transmits commands to the card and the memory card drives responses to the commands on this pin. 

- **MMC_DAT[3:0]** 

   - These pins are connected based on the type of card being used. Table 13-172 outlines which pins are required based on the mode. The number of DAT pins (the data bus width) is set by the Data Transfer Width (DTW) bit in the MMC control register (MMC_HCTL). For more information see the MMCSD Registers in the Register Addendum. 

- **MMC_CLK** 

   - This pin provides the clock to the memory card from the MMC/SD controller. 

- **MMC_POW** 

   - This output pin is used for the MMC/SD card on/off power supply control. The output being high denotes the power-on condition. 

- **MMC_SDCD** 

   - Optional card detect pin with configurable active polarity detection. Optional for any type of card. This signal is received from a mechanical switch on the slot (system dependent). 

- **MMC_SDWP** 

1384 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

   - Optional write protect switch pin with configurable active polarity detection. This signal is received from a mechanical protect switch on the slot (system dependent). Applicable only for SD and SDIO cards that have a mechanical sliding switch on the side of the card. 

- **MMC_OBI** 

   - Optional Out-Of-Band interrupt generated by MMC cards with configurable active polarity detection. 

- **Note:** The MMC_CLK pin functions as an output but must be configured as an I/O to internally loopback the clock to time the inputs. 

Table 13-172 provides a summary of these pins. 

||**Table**|**13-172.**|**MMC/SD/SDIO Controller Pins and Descriptions**|**MMC/SD/SDIO Controller Pins and Descriptions**||
|---|---|---|---|---|---|
|**Pin**||**Type**|**1-Bit Mode**|**4-Bit Mode**|**Reset Value**|
|MMC_CLK(1)||O|Clock Line|Clock Line|High impedance|
|MMC_CMD||I/O|Command Line|Command Line|High impedance|
|MMC_DAT0||I/O|Data Line 0|Data Line 0|0|
|MMC_DAT1||I/O|(not used)|Data Line 1|0|
|MMC_DAT2||I/O|(not used)|Data Line 2|0|
|MMC_DAT3||I/O|(not used)|Data Line 3|0|



(1) The MMC_CLK pin functions as an output but must be configured as an I/O to internally loopback the clock to time the inputs. 

## _**13.3.1.3.1.2 Protocol and Data Format**_ 

The bus protocol between the MMC/SD/SDIO host controller and the card is message-based. Each message is represented by one of the following parts: 

**Command:** A command starts an operation. The command is transferred serially from the MMC/SD/SDIO host controller to the card on the mmc_cmd line. 

**Response:** A response is an answer to a command. The response is sent from the card to the MMC/SD/SDIO host controller. It is transferred serially on the mmc_cmd line. 

**Data:** Data are transferred from the MMC/SD/SDIO host controller to the card or from a card to the MMC/SD/ SDIO host controller using the DATA lines. 

**Busy:** The mmc_dat0 signal is maintained low by the card as far as it is programming the data received. 

**CRC status:** CRC result is sent by the card through the mmc_dat0 line when executing a write transfer. When a transmission error occurs on any of the active data lines, the card sends a negative CRC status on mmc_dat0. When a successful transmission occurs over all active data lines, the card sends a positive CRC status on mmc_dat0 and starts the data programming procedure. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1385 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1.3.1.2.1 Protocol**_ 

There are two types of data transfer: 

- Sequential operation 

- Block-oriented operation 

There are specific commands for each type of operation (sequential or block-oriented). See the _Multimedia Card System Specification_ , the _SD Memory Card Specifications_ , and the _SDIO Card Specification_ . 

## **CAUTION** 

Stream commands are supported only by MMC cards. 

Figure 13-120 and Figure 13-121 show how sequential operations are defined. Sequential operation is only for 1-bit transfer and initiates a continuous data stream. The transfer terminates when a stop command follows on the mmc_cmd line. 

**==> picture [410 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
Host to Card to Card to Host to Card to<br>card host host card host<br>cmd Command Response Command Response<br>dat0 Data stream<br>Data transfer operation Data stop operation<br>**----- End of picture text -----**<br>


**Figure 13-120. Sequential Read Operation (MMC Cards Only)** 

**==> picture [411 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
Host to Card to Host to Host to Card to<br>card host card card host<br>cmd Command Response Command Response<br>Card to<br>host<br>dat0 Data stream Busy<br>Data transfer operation Data stop operation<br>**----- End of picture text -----**<br>


**Figure 13-121. Sequential Write Operation (MMC Cards Only)** 

1386 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

Figure 13-122 and Figure 13-123 show how multiple block-oriented operations are defined. A multiple blockoriented operation sends a data block plus CRC bits. The transfer terminates when a stop command follows on the mmc_cmd line. These operations are available for all kinds of cards. 

**==> picture [418 x 167] intentionally omitted <==**

**----- Start of picture text -----**<br>
Host to Card to Card to Host to Card to<br>card host host card host<br>cmd Command Response Command Response<br>dat[3:0] Data block + CRC Data block + CRC<br>Block read operation Data stop operation<br>Multiple block read operation<br>**----- End of picture text -----**<br>


**Figure 13-122. Multiple Block Read Operation (MMC Cards Only)** 

**==> picture [416 x 228] intentionally omitted <==**

**----- Start of picture text -----**<br>
Host to Card to Host to Card to Card to Host to<br>card host card host host card<br>cmd Command Response Command Response<br>dat0 Data block+ CRC CRCStatus Busy Data block+ CRC CRCStatus Busy<br>Data block Data block<br>dat[3:1] + CRC XX XXXX + CRC XX XXXX<br>Block write operation Data stop operation<br>Multiple block write operation<br>**----- End of picture text -----**<br>


**Figure 13-123. Multiple Block Write Operation (MMC Cards Only)** 

## **Note** 

1. The card busy signal is not always generated by the card; the previous examples show a particular case. 

2. It is the software's responsibility to do a software reset after a data timeout to ensure that mmc_clk is stopped. The software reset is done by setting bit 26 in the MMC_SYSCTL register to 1. 

3. For multiblock transfer, and especially for MMC cards, you can abort a transfer without using a stop command. Use a CMD23 before a data transfer to define the number of blocks that will be transferred, then the transfer stops automatically after the last block (provided the MMC card supports this feature). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1387 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1.3.1.2.2 Data Format**_ 

## **Coding Scheme for Command Token** 

Command packets always start with 0 and end with 1. The second bit is a transmitter bit1 for a host command. The content is the command index (coded by 6 bits) and an argument (for example, an address), coded by 32 bits. The content is protected by 7-bit CRC checksum (see Figure 13-124). 

|0|1|Content|CRC|1|
|---|---|---|---|---|
|48 bits length|||||
||||||



**Figure 13-124. Command Token Format** 

## **Coding Scheme for Response Token** 

Response packets always start with 0 and end with a 1. The second bit is a transmitter bit0 for a card response. The content is different for each type of response (R1, R2, R3, R4, R5, and R6) and the content is protected by 7-bit CRC checksum. Depending on the type of commands sent to the card, the MMC_CMD register must be configured differently to avoid false CRC or index errors to be flagged on command response (see Table 13-173). For more details about response types, see the _Multimedia Card System Specification_ , the _SD Memory Card Specification_ , or the _SDIO Card Specification_ . 

**Table 13-173. Response Type Summary** 

|**Response Type**|**Index Check Enable**|**CRC Check Enable**||
|---|---|---|---|
|**MMC_CMD[17:16]**|**MMC_CMD[20]**|**MMC_CMD[19]**||
|**RSP_TYPE**(1)|**CICE**|**CCCE**|**Name of Response Type**|
|00|0|0|No Response|
|01|0|1|R2|
|10|0|0|R3 (R4 for SD cards)|
|10|1|1|R1, R6, R5 (R7 for SD cards)|
|11|1|1|R1b, R5b|



(1) The MMC/SD/SDIO host controller assumes that both clocks may be switched off, whatever the value set in the MMC_SYSCONFIG[9:8] CLOCKACTIVITY bit. 

Figure 13-125 and Figure 13-126 depict the 48-bit and 136-bit response packets. 

|0|0|Content|CRC|1|
|---|---|---|---|---|
|48 bits length|||||
||||||



**Figure 13-125. 48-Bit Response Packet (R1, R3, R4, R5, R6)** 

|0|0|Content|CRC|1|
|---|---|---|---|---|
|136 bits length|||||



**Figure 13-126. 136-Bit Response Packet (R2)** 

1388 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Coding Scheme for Data Token** 

Data tokens always start with 0 and end with 1 (see Figure 13-127, Figure 13-128, Figure 13-129, and Figure 13-130). 

|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|0<br>...<br>...<br>b7<br>b6<br>b1<br>b0<br>...<br>LSB<br>MSB<br>Sequential data<br>b7<br>b6<br>b1<br>b0<br>1<br>mmc_dat0<br>**Figure 13-127. Data Packet for Sequential Transfer (1-Bit)**<br>0<br>1<br>mmc_dat0<br>...<br>...<br>...<br>LSB<br>MSB<br>Block data<br>CRC<br>Block length *8<br>b7<br>b6<br>b1<br>b0<br>b7<br>b6<br>b1<br>b0|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||0|b7|b6|...|b1|b0|...|b7|b6|...|b1|b0|CRC|1|
|||Block length *8|||||||||||||



**Figure 13-128. Data Packet for Block Transfer (1-Bit)** 

|1<br>0<br>mmc_dat3<br>...<br>b7<br>b3<br>b7<br>b3<br>LSB<br>MSB<br>CRC<br>1<br>0<br>...<br>b6<br>b2<br>b6<br>b2<br>CRC<br>1<br>0<br>...<br>b5<br>b1<br>b5<br>b1<br>CRC<br>1<br>0<br>...<br>b4<br>b0<br>b4<br>b0<br>CRC<br>Block length *2<br>mmc_dat2<br>mmc_dat1<br>mmc_dat0|1<br>0<br>mmc_dat3<br>...<br>b7<br>b3<br>b7<br>b3<br>LSB<br>MSB<br>CRC<br>1<br>0<br>...<br>b6<br>b2<br>b6<br>b2<br>CRC<br>1<br>0<br>...<br>b5<br>b1<br>b5<br>b1<br>CRC<br>1<br>0<br>...<br>b4<br>b0<br>b4<br>b0<br>CRC<br>Block length *2<br>mmc_dat2<br>mmc_dat1<br>mmc_dat0|1<br>0<br>mmc_dat3<br>...<br>b7<br>b3<br>b7<br>b3<br>LSB<br>MSB<br>CRC<br>1<br>0<br>...<br>b6<br>b2<br>b6<br>b2<br>CRC<br>1<br>0<br>...<br>b5<br>b1<br>b5<br>b1<br>CRC<br>1<br>0<br>...<br>b4<br>b0<br>b4<br>b0<br>CRC<br>Block length *2<br>mmc_dat2<br>mmc_dat1<br>mmc_dat0|1<br>0<br>mmc_dat3<br>...<br>b7<br>b3<br>b7<br>b3<br>LSB<br>MSB<br>CRC<br>1<br>0<br>...<br>b6<br>b2<br>b6<br>b2<br>CRC<br>1<br>0<br>...<br>b5<br>b1<br>b5<br>b1<br>CRC<br>1<br>0<br>...<br>b4<br>b0<br>b4<br>b0<br>CRC<br>Block length *2<br>mmc_dat2<br>mmc_dat1<br>mmc_dat0|1<br>0<br>mmc_dat3<br>...<br>b7<br>b3<br>b7<br>b3<br>LSB<br>MSB<br>CRC<br>1<br>0<br>...<br>b6<br>b2<br>b6<br>b2<br>CRC<br>1<br>0<br>...<br>b5<br>b1<br>b5<br>b1<br>CRC<br>1<br>0<br>...<br>b4<br>b0<br>b4<br>b0<br>CRC<br>Block length *2<br>mmc_dat2<br>mmc_dat1<br>mmc_dat0|1<br>0<br>mmc_dat3<br>...<br>b7<br>b3<br>b7<br>b3<br>LSB<br>MSB<br>CRC<br>1<br>0<br>...<br>b6<br>b2<br>b6<br>b2<br>CRC<br>1<br>0<br>...<br>b5<br>b1<br>b5<br>b1<br>CRC<br>1<br>0<br>...<br>b4<br>b0<br>b4<br>b0<br>CRC<br>Block length *2<br>mmc_dat2<br>mmc_dat1<br>mmc_dat0|1<br>0<br>mmc_dat3<br>...<br>b7<br>b3<br>b7<br>b3<br>LSB<br>MSB<br>CRC<br>1<br>0<br>...<br>b6<br>b2<br>b6<br>b2<br>CRC<br>1<br>0<br>...<br>b5<br>b1<br>b5<br>b1<br>CRC<br>1<br>0<br>...<br>b4<br>b0<br>b4<br>b0<br>CRC<br>Block length *2<br>mmc_dat2<br>mmc_dat1<br>mmc_dat0|1<br>0<br>mmc_dat3<br>...<br>b7<br>b3<br>b7<br>b3<br>LSB<br>MSB<br>CRC<br>1<br>0<br>...<br>b6<br>b2<br>b6<br>b2<br>CRC<br>1<br>0<br>...<br>b5<br>b1<br>b5<br>b1<br>CRC<br>1<br>0<br>...<br>b4<br>b0<br>b4<br>b0<br>CRC<br>Block length *2<br>mmc_dat2<br>mmc_dat1<br>mmc_dat0|1<br>0<br>mmc_dat3<br>...<br>b7<br>b3<br>b7<br>b3<br>LSB<br>MSB<br>CRC<br>1<br>0<br>...<br>b6<br>b2<br>b6<br>b2<br>CRC<br>1<br>0<br>...<br>b5<br>b1<br>b5<br>b1<br>CRC<br>1<br>0<br>...<br>b4<br>b0<br>b4<br>b0<br>CRC<br>Block length *2<br>mmc_dat2<br>mmc_dat1<br>mmc_dat0|
|---|---|---|---|---|---|---|---|---|
||0|b4|b0|...|b4|b0|CRC|1|
|||Block length *2|||||||



**Figure 13-129. Data Packet for Block Transfer (4-Bit)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1389 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

|LSB<br>MSB<br>1<br>0<br>mmc_dat3<br>...<br>b3<br>b3<br>b3<br>b3<br>CRC<br>Block length<br>1<br>0<br>...<br>b2<br>b2<br>b2<br>b2<br>CRC<br>mmc_dat2<br>1<br>0<br>...<br>b1<br>b1<br>b1<br>b1<br>CRC<br>mmc_dat1<br>1<br>0<br>...<br>b0<br>b0<br>b0<br>b0<br>CRC<br>mmc_dat0<br>1<br>0<br>mmc_dat7<br>...<br>b7<br>b7<br>b7<br>b7<br>CRC<br>1<br>0<br>...<br>b6<br>b6<br>b6<br>b6<br>CRC<br>mmc_dat6<br>1<br>0<br>...<br>b5<br>b5<br>b5<br>b5<br>CRC<br>mmc_dat5<br>1<br>0<br>...<br>b4<br>b4<br>b4<br>b4<br>CRC<br>mmc_dat4|LSB<br>MSB<br>1<br>0<br>mmc_dat3<br>...<br>b3<br>b3<br>b3<br>b3<br>CRC<br>Block length<br>1<br>0<br>...<br>b2<br>b2<br>b2<br>b2<br>CRC<br>mmc_dat2<br>1<br>0<br>...<br>b1<br>b1<br>b1<br>b1<br>CRC<br>mmc_dat1<br>1<br>0<br>...<br>b0<br>b0<br>b0<br>b0<br>CRC<br>mmc_dat0<br>1<br>0<br>mmc_dat7<br>...<br>b7<br>b7<br>b7<br>b7<br>CRC<br>1<br>0<br>...<br>b6<br>b6<br>b6<br>b6<br>CRC<br>mmc_dat6<br>1<br>0<br>...<br>b5<br>b5<br>b5<br>b5<br>CRC<br>mmc_dat5<br>1<br>0<br>...<br>b4<br>b4<br>b4<br>b4<br>CRC<br>mmc_dat4|LSB<br>MSB<br>1<br>0<br>mmc_dat3<br>...<br>b3<br>b3<br>b3<br>b3<br>CRC<br>Block length<br>1<br>0<br>...<br>b2<br>b2<br>b2<br>b2<br>CRC<br>mmc_dat2<br>1<br>0<br>...<br>b1<br>b1<br>b1<br>b1<br>CRC<br>mmc_dat1<br>1<br>0<br>...<br>b0<br>b0<br>b0<br>b0<br>CRC<br>mmc_dat0<br>1<br>0<br>mmc_dat7<br>...<br>b7<br>b7<br>b7<br>b7<br>CRC<br>1<br>0<br>...<br>b6<br>b6<br>b6<br>b6<br>CRC<br>mmc_dat6<br>1<br>0<br>...<br>b5<br>b5<br>b5<br>b5<br>CRC<br>mmc_dat5<br>1<br>0<br>...<br>b4<br>b4<br>b4<br>b4<br>CRC<br>mmc_dat4|LSB<br>MSB<br>1<br>0<br>mmc_dat3<br>...<br>b3<br>b3<br>b3<br>b3<br>CRC<br>Block length<br>1<br>0<br>...<br>b2<br>b2<br>b2<br>b2<br>CRC<br>mmc_dat2<br>1<br>0<br>...<br>b1<br>b1<br>b1<br>b1<br>CRC<br>mmc_dat1<br>1<br>0<br>...<br>b0<br>b0<br>b0<br>b0<br>CRC<br>mmc_dat0<br>1<br>0<br>mmc_dat7<br>...<br>b7<br>b7<br>b7<br>b7<br>CRC<br>1<br>0<br>...<br>b6<br>b6<br>b6<br>b6<br>CRC<br>mmc_dat6<br>1<br>0<br>...<br>b5<br>b5<br>b5<br>b5<br>CRC<br>mmc_dat5<br>1<br>0<br>...<br>b4<br>b4<br>b4<br>b4<br>CRC<br>mmc_dat4|LSB<br>MSB<br>1<br>0<br>mmc_dat3<br>...<br>b3<br>b3<br>b3<br>b3<br>CRC<br>Block length<br>1<br>0<br>...<br>b2<br>b2<br>b2<br>b2<br>CRC<br>mmc_dat2<br>1<br>0<br>...<br>b1<br>b1<br>b1<br>b1<br>CRC<br>mmc_dat1<br>1<br>0<br>...<br>b0<br>b0<br>b0<br>b0<br>CRC<br>mmc_dat0<br>1<br>0<br>mmc_dat7<br>...<br>b7<br>b7<br>b7<br>b7<br>CRC<br>1<br>0<br>...<br>b6<br>b6<br>b6<br>b6<br>CRC<br>mmc_dat6<br>1<br>0<br>...<br>b5<br>b5<br>b5<br>b5<br>CRC<br>mmc_dat5<br>1<br>0<br>...<br>b4<br>b4<br>b4<br>b4<br>CRC<br>mmc_dat4|LSB<br>MSB<br>1<br>0<br>mmc_dat3<br>...<br>b3<br>b3<br>b3<br>b3<br>CRC<br>Block length<br>1<br>0<br>...<br>b2<br>b2<br>b2<br>b2<br>CRC<br>mmc_dat2<br>1<br>0<br>...<br>b1<br>b1<br>b1<br>b1<br>CRC<br>mmc_dat1<br>1<br>0<br>...<br>b0<br>b0<br>b0<br>b0<br>CRC<br>mmc_dat0<br>1<br>0<br>mmc_dat7<br>...<br>b7<br>b7<br>b7<br>b7<br>CRC<br>1<br>0<br>...<br>b6<br>b6<br>b6<br>b6<br>CRC<br>mmc_dat6<br>1<br>0<br>...<br>b5<br>b5<br>b5<br>b5<br>CRC<br>mmc_dat5<br>1<br>0<br>...<br>b4<br>b4<br>b4<br>b4<br>CRC<br>mmc_dat4|LSB<br>MSB<br>1<br>0<br>mmc_dat3<br>...<br>b3<br>b3<br>b3<br>b3<br>CRC<br>Block length<br>1<br>0<br>...<br>b2<br>b2<br>b2<br>b2<br>CRC<br>mmc_dat2<br>1<br>0<br>...<br>b1<br>b1<br>b1<br>b1<br>CRC<br>mmc_dat1<br>1<br>0<br>...<br>b0<br>b0<br>b0<br>b0<br>CRC<br>mmc_dat0<br>1<br>0<br>mmc_dat7<br>...<br>b7<br>b7<br>b7<br>b7<br>CRC<br>1<br>0<br>...<br>b6<br>b6<br>b6<br>b6<br>CRC<br>mmc_dat6<br>1<br>0<br>...<br>b5<br>b5<br>b5<br>b5<br>CRC<br>mmc_dat5<br>1<br>0<br>...<br>b4<br>b4<br>b4<br>b4<br>CRC<br>mmc_dat4|LSB<br>MSB<br>1<br>0<br>mmc_dat3<br>...<br>b3<br>b3<br>b3<br>b3<br>CRC<br>Block length<br>1<br>0<br>...<br>b2<br>b2<br>b2<br>b2<br>CRC<br>mmc_dat2<br>1<br>0<br>...<br>b1<br>b1<br>b1<br>b1<br>CRC<br>mmc_dat1<br>1<br>0<br>...<br>b0<br>b0<br>b0<br>b0<br>CRC<br>mmc_dat0<br>1<br>0<br>mmc_dat7<br>...<br>b7<br>b7<br>b7<br>b7<br>CRC<br>1<br>0<br>...<br>b6<br>b6<br>b6<br>b6<br>CRC<br>mmc_dat6<br>1<br>0<br>...<br>b5<br>b5<br>b5<br>b5<br>CRC<br>mmc_dat5<br>1<br>0<br>...<br>b4<br>b4<br>b4<br>b4<br>CRC<br>mmc_dat4|LSB<br>MSB<br>1<br>0<br>mmc_dat3<br>...<br>b3<br>b3<br>b3<br>b3<br>CRC<br>Block length<br>1<br>0<br>...<br>b2<br>b2<br>b2<br>b2<br>CRC<br>mmc_dat2<br>1<br>0<br>...<br>b1<br>b1<br>b1<br>b1<br>CRC<br>mmc_dat1<br>1<br>0<br>...<br>b0<br>b0<br>b0<br>b0<br>CRC<br>mmc_dat0<br>1<br>0<br>mmc_dat7<br>...<br>b7<br>b7<br>b7<br>b7<br>CRC<br>1<br>0<br>...<br>b6<br>b6<br>b6<br>b6<br>CRC<br>mmc_dat6<br>1<br>0<br>...<br>b5<br>b5<br>b5<br>b5<br>CRC<br>mmc_dat5<br>1<br>0<br>...<br>b4<br>b4<br>b4<br>b4<br>CRC<br>mmc_dat4|
|---|---|---|---|---|---|---|---|---|
||0|b0|b0|...|b0|b0|CRC|1|
|||Block length|||||||



**Figure 13-130. Data Packet for Block Transfer (8-Bit)** 

## _**13.3.1.3.2 Resets**_ 

## _**13.3.1.3.2.1 Hardware Reset**_ 

The module is reinitialized by the hardware. 

The MMC_SYSSTS[0] RESETDONE bit can be monitored by the software to check if the module is ready-to-use after a hardware reset. 

This hardware reset signal has a global reset action on the module. All configuration registers and all state machines are reset in all clock domains. 

This hardware reset signal has a global reset action on the module. All configuration registers and all statemachines are reset in all clock domains. 

## _**13.3.1.3.2.2 Software Reset**_ 

The module is reinitialized by software through the MMC_SYSCONFIG[1] SOFTRESET bit. This bit has the same action on the module logic as the hardware signal except for: 

- Debounce logic 

- MMC_PSTATE, MMC_CAPA, and MMC_CUR_CAPA registers (see corresponding register descriptions) 

The SOFTRESET bit is active high. The bit is automatically reinitialized to 0 by the hardware. The MMC_SYSCTL[24] SRA bit has the same action as the SOFTRESET bit on the design. 

The MMC_SYSSTS[0] RESETDONE bit can be monitored by the software to check if the module is ready-to-use after a software reset. 

Moreover, two partial software reset bits are provided: 

- MMC_SYSCTL[26] SRD bit 

1390 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- MMC_SYSCTL[25] SRC bit 

These two reset bits are useful to reinitialize data or command processes respectively in case of line conflict. When set to 1, a reset process is automatically released when the reset completes: 

- The MMC_SYSCTL[26] SRD bit resets all finite state-machines and status management that handle data transfers on both the interface and functional side. 

- The MMC_SYSCTL[25] SRC bit resets all finite state-machines and status management that handle command transfers on both the interface and functional side. 

## **Note** 

If **any** of the clock inputs are not present for the MMC/SD/SDIO peripheral, the software reset will not complete. 

## _**13.3.1.3.3 Power Management**_ 

The MMC/SD/SDIO host controller can enter into different modes and save power: 

- Normal mode 

- Idle mode 

The two modes are mutually exclusive (the module can be in normal mode or in idle mode). The MMC/SD/SDIO host controller is compliant with the PRCM module handshake protocol. When the MMC/SD/SDIO power domain is off, the only way to wake up the power domain and different MMC/SD/SDIO clocks is to monitor the mmc_dat1 input pin state via a different GPIO line for each MMC/SD/SDIO interface. 

## _**13.3.1.3.3.1 Normal Mode**_ 

The autogating of interface and functional clocks occurs when the following conditions are met: 

- The MMC_SYSCONFIG[0] AUTOIDLE bit is set to 1. 

- There is no transaction on the MMC interface. 

The autogating of interface and functional clocks stops when the following conditions are met: 

- A register access occurs through the L3 (or L4) interconnect. 

- A wake-up event occurs (an interrupt from a SDIO card). 

- A transaction on the MMC/SD/SDIO interface starts. 

Then the MMC/SD/SDIO host controller enters in low-power state even if MMC_SYSCONFIG[0] AUTOIDLE is cleared to 0. The functional clock is internally switched off and only interconnect read and write accesses are allowed. 

## _**13.3.1.3.3.2 Idle Mode**_ 

The clocks provided to MMC/SD/SDIO are switched off upon a PRCM module request. They are switched back upon module request. The MMC/SD/SDIO host controller complies with the PRCM module handshaking protocol: 

- Idle request from the system power manager 

- Idle acknowledgment from the MMC/SD/SDIO host controller 

The idle acknowledgment varies according to the MMC_SYSCONFIG[4:3] SIDLEMODE bit field: 

- 0: Force-idle mode. The MMC/SD/SDIO host controller acknowledges the system power manager request unconditionally. 

- 1h: No-idle mode. The MMC/SD/SDIO host controller ignores the system power manager request and behaves normally as if the request was not asserted. 

- 2h: Smart-idle mode. The MMC/SD/SDIO host controller acknowledges the system power manager request according to its internal state. 

- 3h: Reserved. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1391 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

During the smart-idle mode period, the MMC/SD/SDIO host controller acknowledges that the OCP and Functional clocks may be switched off based on the values set in the MMC_SYSCONFIG[9:8] CLOCKACTIVITY field. 

## _**13.3.1.3.3.3 Transition from Normal Mode to Smart-Idle Mode**_ 

Smart-idle mode is enabled when the MMC_SYSCONFIG[4:3] SIDLEMODE bit field is set to 2h or 3h. The MMC/SD/SDIO host controller goes into idle mode when the PRCM issues an idle request, according to its internal activity. The MMC/SD/SDIO host controller acknowledges the idle request from the PRCM after ensuring the following: 

- The current multi/single-block transfer is completed. 

- Any interrupt or DMA request is asserted. 

- There is no card interrupt on the MMCSD_dat1 signal. 

As long as the MMC/SD/SDIO controller does not acknowledge the idle request, if an event occurs, the MMC/SD/SDIO host controller can still generate an interrupt or a DMA request. In this case, the module ignores the idle request from the PRCM. 

As soon as the MMC/SD/SDIO controller acknowledges the idle request from the PRCM: 

- If Smart-Idle mode the module does not assert any new interrupt or DMA request 

## _**13.3.1.3.3.4 Transition from Smart-Idle Mode to Normal Mode**_ 

The MMC/SD/SDIO host controller detects the end of the idle period when the PRCM deasserts the idle request. For the wake-up event, there is a corresponding interrupt status in the MMC_STAT register. The MMC/SD/ SDIO host controller operates the conversion between wake-up and interrupt (or DMA request) upon exit from smart-idle mode if the associated enable bit is set in the MMC_ISE register. 

Interrupts and wake-up events have independent enable/disable controls, accessible through the MMC_HCTL and MMC_ISE registers. The overall consistency must be ensured by software. 

The interrupt status register MMC_STAT is updated with the event that caused the wake-up in the CIRQ bit when the MMC_IE[8] CIRQ_ENABLE associated bit is enabled. Then, the wake-up event at the origin of the transition from smart-idle mode to normal mode is converted into its corresponding interrupt or DMA request. (The MMC_STAT register is updated and the status of the interrupt signal changes.) 

When the idle request from the PRCM is deasserted, the module switches back to normal mode. The module is fully operational. 

## _**13.3.1.3.3.5 Force-Idle Mode**_ 

Force-idle mode is enabled when the MMC_SYSCONFIG[4:3] SIDLEMODE bit field is cleared to 0. Force-idle mode is an idle mode where the MMC/SD/SDIO host controller responds unconditionally to the idle request from the PRCM. Moreover, in this mode, the MMC/SD/SDIO host controller unconditionally deasserts interrupts and DMA request lines are asserted. 

The transition from normal mode to force-idle mode does not affect the bits of the MMC_STAT register. In force-idle mode, the interrupt and DMA request lines are deasserted. Interface Clock (OCP) and functional clock (CLKADPI) can be switched off. 

## **CAUTION** 

In Force-idle mode, an idle request from the PRCM during a command or a data transfer can lead to an unexpected and unpredictable result. 

When the module is idle, any access to the module generates an error as long as the OCP clock is alive. 

1392 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

The module exits the force-idle mode when the PRCM deasserts the idle request. Then the module switches back to normal mode. The module is fully operational. Interrupt and DMA request lines are optionally asserted one clock cycle later. 

## _**13.3.1.3.3.6 Local Power Management**_ 

Table 13-174 describes power-management features available for the MMC/SD/SDIO modules. 

**Table 13-174. Local Power Management Features** 

|**Feature**|**Registers**|**Description**|
|---|---|---|
|Clock Auto Gating|MMC_SYSCONFIG AUTOIDLE bit|This bit allows a local power optimization inside module, by gating|
|||the OCP clock upon the interface activity or gating the CLKADPI|
|||clock upon the internal activity.|
|Target Idle Modes|MMC_SYSCONFIG SIDLEMODE bit|Force-idle, No-idle, and Smart-idle modes|
|Clock Activity|MMC_SYSCONFIG CLOCKACTIVITY bit|Please seeTable 13-175for configuration details.|
|Global Wake-Up|MMC_SYSCONFIG ENAWAKEUP bit|This bit enables the wake-up feature at module level.|
|Enable|||
|Wake-Up Sources|MMC_HCTL register|This register holds one active high enable bit per event source able|
|Enable||to generate wake-up signal.|



**Table 13-175. Clock Activity Settings** 

||**Clock State When**|**Module is in**|||
|---|---|---|---|---|
||**IDLE State**||||
|**CLOCKACTIVITY**|||**Features Available when Module is in IDLE**||
|**Values**|**OCP Clock**|**CLKADPI**|**State**|**Wake-Up Events**|
|00|OFF|OFF|None|Card Interrupt|
|10|OFF|ON|None||
|01|ON|OFF|None||
|11|ON|ON|All||



## **CAUTION** 

The PRCM module has no hardware means of reading CLOCKACTIVITY settings. Thus, software must ensure consistent programming between the CLOCKACTIVITY and MMC clock PRCM control bits. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1393 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1.3.4 Interrupt Requests**_ 

Several internal module events can generate an interrupt. Each interrupt has a status bit, an interrupt enable bit, and a signal status enable: 

- The status of each type of interrupt is automatically updated in the MMC_STAT register; it indicates which service is required. 

- The interrupt status enable bits of the MMC_IE register enable/disable the automatic update of the MMC_STAT register on an event-by-event basis. 

- The interrupt signal enable bits of the MMC_ISE register enable/disable the transmission of an interrupt request on the interrupt line MMC_IRQ (from the MMC/SD/SDIO host controller to the MPU subsystem interrupt controller) on an event-by-event basis. 

If an interrupt status is disabled in the MMC_IE register, then the corresponding interrupt request is not transmitted, and the value of the corresponding interrupt signal enable in the MMC_ISE register is ignored. 

When an interrupt event occurs, the corresponding status bit is automatically set to 1 (the MMC/SD/SDIO host controller updates the status bit) in the MMC_STAT register. If later a mask is applied on the interrupt in the MMC_ISE register, the interrupt request is deactivated. 

When the interrupt source has not been serviced, if the interrupt status is cleared in the MMC_STAT register and the corresponding mask is removed from the MMC_ISE register, the interrupt status is not asserted again in the MMC_STAT register and the MMC/SD/SDIOi host controller does not transmit an interrupt request. 

## **CAUTION** 

If the buffer write ready interrupt (BWR) or the buffer read ready only interrupt (BRR) are not serviced and are cleared in the MMC_STAT register, and the corresponding mask is removed, then the MMC/SD/SDIOi host controller will wait for the service of the interrupt without updating the status MMC_STAT or transmitting an interrupt request. 

Table 13-176 lists the event flags, and their mask, that can cause module interrupts. 

**Table 13-176. Events** 

|**Event Flag**|**Event Mask**|**Map To**|**Description**|
|---|---|---|---|
|MMC_STAT[29] BADA|MMC_IE[29]|MMC_IRQ|Bad Access to Data space. This bit is set automatically to indicate a|
||BADA_ENABLE||bad access to buffer when not allowed. This bit is set during a read|
||||access to the data register (MMC_DATA) while buffer reads are not allowed|
||||(MMC_PSTATE[11] BRE=0). This bit is set during a write access to the data|
||||register (MMC_DATA) while buffer writes are not allowed (MMC_STATE[10]|
||||BWE=0)|
|MMC_STAT[28] CERR|MMC_IE[28]|MMC_IRQ|Card Error. This bit is set automatically when there is at least one error|
||CERR_ENABLE||in a response of type R1, R1b, R6, R5 or R5b. Only bits referenced as|
||||type E(error) in status field in the response can set a card status error. An|
||||error bit in the response is flagged only if corresponding bit in card status|
||||response errors MMC_CSRE is set. There is not card detection for auto|
||||CMD12 command.|
|MMC_STAT[25]|MMC_IE[25]|MMC_IRQ|ADMA error. This bit is set when the host controller detects errors during|
|ADMAE|ADMAE_ENABLE||ADMA based data transfer. The stat of the ADMA at an error occurrence|
||||is saved in the ADMA Error Status Register. In addition, the host controller|
||||generates this interrupt when it detects invalid descriptor data (Valid=0) at|
||||the ST_FDS state.|
|MMC_STAT[24] ACE|MMC_IE[24]|MMC_IRQ|Auto CMD12 error. This bit is set automatically when one of the bits in Auto|
||ACE_ENABLE||CMD12 Error status register has changed from 0 to 1|
|MMC_STAT[22] DEB|MMC_IE[22]|MMC_IRQ|Data End Bit error. This bit is set automatically when detecting a 0 at the|
||DEB_ENABLE||end bit position of read data on DAT line or at the end position of the CRC|
||||status in write mode.|
|MMC_STAT[21] DCRC|MMC_IE[21]|MMC_IRQ|Data CRC error. This bit is set automatically when there is a CRC16 error|
||DCRC_ENABLE||in the data phase response following a block read command or if there is|
||||a 3-bit CRC status different of a position "010" token during a block write|
||||command.|



1394 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Table 13-176. Events (continued)** 

|**Event Flag**|**Event Mask**|**Map To**|**Description**|
|---|---|---|---|
|MMC_STAT[20] DTO|MMC_IE[20]|MMC_IRQ|Data Timeout error. This bit is set automatically according to the following|
||DTO_ENABLE||conditions: A) busy timeout for R1b, R5b response. B) busy timeout after|
||||write CRC status. C) write CRC status timeout, or D) read data timeout.|
|MMC_STAT[19] CIE|MMC_IE[19]|MMC_IRQ|Command Index Error. This bit is set automatically when response index|
||CIE_ENABLE||differs from corresponding command index previously emitted. The check is|
||||enabled through MMC_CMD[20] CICE bit.|
|MMC_STAT[18] CEB|MMC_IE[18]|MMC_IRQ|Command End Bit error. This bit is set automatically when detecting a 0 at|
||CEB_ENABLE||the end bit position of a command response.|
|MMC_STAT[17] CCRC|MMC_IE[17]|MMC_IRQ|Command CRC error. This bit is set automatically when there is a CRC7|
||CCRC_ENABLE||error in the command response. CRC check is enabled through the|
||||MMC_CMD[19] CCCE bit.|
|MMC_STAT[16] CTO|MMC_IE[16]|MMC_IRQ|Command Timeout error. This bit is set automatically when no response|
||CTO_ENABLE||is received within 64 clock cycles from the end bit of the command. For|
||||commands the reply within 5 clock cycles, the timeout is still detected at 64|
||||clock cycles.|
|MMC_STAT[15] ERRI|MMC_IE[15]|MMC_IRQ|Error Interrupt. If any of the bits in the Error Interrupt Status register|
||ERRI_ENABLE||(MMC_STAT[24:15]) are set, the this bit is set to 1.|
|MMC_STAT[10] BSR|MMC_IE[10]|MMC_IRQ|Boot Status Received interrupt. This bit is set automatically when|
||BSR_ENABLE||MMC_CON[18] BOOT_CF0 is set to 1 or 2h and boot status is received|
||||on the dat0 line. This interrupt is only used for MMC cards.|
|MMC_STAT[8] CIRQ|MMC_IE[8]|MMC_IRQ|Card Interrupt. This bit is only used for SD, SDIO, and CE-ATA cards.|
||CIRQ_ENABLE||In 1-bit mode, interrupt source is asynchronous (can be a source of|
||||asynchronous wake-up). In 4-bit mode, interrupt source is sampled during|
||||the interrupt cycle. In CE-ATA mode, interrupt source is detected when the|
||||card drive CMD line to zero during one cycle after data transmission end.|
|MMC_STAT[5] BRR|MMC_IE[5]|MMC_IRQ|Buffer Read ready. This bit is set automatically during a read operation to|
||BRR_ENABLE||the card when one block specified by MMC_BLK[10:0] BLEN is completely|
||||written in the buffer. It indicates that the memory card has filled out the|
||||buffer and the local host needs to empty the buffer by reading it.|
|MMC_STAT[4] BWR|MMC_IE[4]|MMC_IRQ|Buffer Write ready. This bit is automatically set during a write operation|
||BWR_ENABLE||to the card when the host can write a complete block as specified by|
||||MMC_BLK[10:0] BLEN. It indicates that the memory card has emptied one|
||||block from the bugger and the local host is able to write one block of data|
||||into the buffer.|
|MMC_STAT[3] DMA|MMC_IE[3]|MMC_IRQ|DMA interrupt. This status is set when an interrupt is required in the ADMA|
||DMA_ENABLE||instruction and after the data transfer is complete.|
|MMC_STAT[2] BGE|MMC_IE[2]|MMC_IRQ|Block Gap event. When a stop at block gap is requested (MMC_HCTL[16]|
||BGE_ENABLE||SBGR), this bit is automatically set when transaction is stopped at the block|
||||gap during a read or write operation.|
|MMC_STAT[1] TC|MMC_IE[1]|MMC_IRQ|Transfer completed. This bit is always set when a read/write transfer is|
||TC_ENABLE||completed or between two blocks when the transfer is stopped due to a|
||||stop at block gap requested (MMC_HCTL[16 SBGR). In read mode this|
||||bit is automatically set on completion of a read transfer (MMC_PSTATE[9]|
||||RTA). In write mode, this bit is automatically set on completion of the DAT|
||||line use (MMC_PSTATE[2] DLA).|
|MMC_STAT[0] CC|MMC_IE[0]|MMC_IRQ|Command complete. This bit is set when a 1-to-0 transition occurs in the|
||CC_ENABLE||register command inhibit (MMC_PSTATE[0] CMDI). If the command is a|
||||type for which no response is expected, then the command complete|
||||interrupt is generated at the end of the command. A command timeout|
||||error (MMC_STAT[16] CTO) has higher priority than command complete|
||||(MMC_STAT[0] CC). If a response is expected but none is received, the a|
||||Command Timeout error is detected and signaled instead of the Command|
||||Complete interrupt.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1395 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1.3.4.1 Interrupt-Driven Operation**_ 

An interrupt enable bit must be set in the MMC_IE register to enable the module internal source of interrupt. 

When an interrupt event occurs, the single interrupt line is asserted and the LH must: 

- Read the MMC_STAT register to identify which event occurred. 

- Write 1 into the corresponding bit of the MMC_STAT register to clear the interrupt status and release the interrupt line (if a read is done after this write, this would return 0). 

## **Note** 

In the MMC_STAT register, Card Interrupt (CIRQ) and Error Interrupt (ERRI) bits cannot be cleared. 

The MMC_STAT[8] CIRQ status bit must be masked by disabling the MMC_IE[8] CIRQ_ENABLE bit (cleared to 0), then the interrupt routine must clear SDIO interrupt source in SDIO card common control register (CCCR). 

The MMC_STAT[15] ERRI bit is automatically cleared when all status bits in MMC_STAT[31:16] are cleared. 

## _**13.3.1.3.4.2 Polling**_ 

When the interrupt capability of an event is disabled in the MMC_ISE register, the interrupt line is not asserted: 

- Software can poll the status bit in the MMC_STAT register to detect when the corresponding event occurs. 

- Writing 1 into the corresponding bit of the MMC_STAT register clears the interrupt status and does not affect the interrupt line state. 

## **Note** 

Please see the note in Section 13.3.1.3.4.1 concerning CIRQ and ERRI bits clearing. 

## _**13.3.1.3.5 DMA Modes**_ 

The device supports DMA responder mode only. In this case, the controller is a responder on DMA transaction managed by two separated requests (SDMAWREQN and SDMARREQN) 

## _**13.3.1.3.5.1 DMA Responder Mode Operations**_ 

The MMC/SD/SDIO controller can be interfaced with a DMA controller. At system level, the advantage is to discharge the local host (LH) of the data transfers. The module does not support wide DMA access (above 1024 bytes) for SD cards as specified in the _SD Card Specification_ and _SD Host Controller Standard Specification_ . 

The DMA request is issued if the following conditions are met: 

- The MMC_CMD[0] DE bit is set to 1 to trigger the initial DMA request (the write must be done when running the data transfer command). 

- A command was emitted on the MMC_cmd line. 

- There is enough space in the buffer of the MMC/SD/SDIO controller to write an entire block (BLEN writes). 

1396 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.1.3.5.1.1 DMA Receive Mode**_ 

In a DMA block read operation (single or multiple), the request signal SDMARREQN is asserted to its active level when a complete block is written in the buffer. The block size transfer is specified in the MMC_BLK[10:0] BLEN field. 

The SDMARREQN signal is deasserted to its inactive level when the sDMA has read one single word from the buffer. Only one request is sent per block; the DMA controller can make a 1-shot read access or several DMA bursts, in which case the DMA controller must manage the number of burst accesses, according to block size BLEN field. 

New DMA requests are internally masked if the sDMA has not read exactly BLEN bytes and a new complete block is not ready. As DMA accesses are in 32-bit, then the number of sDMA read is Integer(BLEN/4)+1. 

The receive buffer never overflows. In multiple block transfers for block size above 512 bytes, when the buffer gets full, the MMC_CLK clock signal (provided to the card) is momentarily stopped until the sDMA or the MPU performs a read access, which reads a complete block in the buffer. 

Figure 13-131 provides a summary: 

- DMA transfer size = BLEN buffer size in one shot or by burst 

- One DMA request per block 

**==> picture [452 x 301] intentionally omitted <==**

**Figure 13-131. DMA Receive Mode** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1397 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1.3.5.1.2 DMA Transmit Mode**_ 

In a DMA block write operation (single or multiple), the request signal SDMAWREQN is asserted to its active level when a complete block is to be written to the buffer. The block size transfer is specified in the MMC_BLK[10:0] BLEN field. 

The SDMAWREQN signal is deasserted to its inactive level when the sDMA has written one single word to the buffer. 

Only one request is sent per block; the DMA controller can make a 1-shot write access or multiple write DMA bursts, in which case the DMA controller must manage the number of burst accesses, according to block size BLEN field. 

New DMA requests are internally masked if the sDMA has not written exactly BLEN bytes (as DMA accesses are in 32-bit, then the number of sDMA read is Integer(BLEN/4)+1) and if there is not enough memory space to write a complete block in the buffer. 

Figure 13-132 provides a summary: 

- DMA transfer size = BLEN buffer size in one shot or by burst 

- One DMA request per block 

**==> picture [430 x 293] intentionally omitted <==**

**Figure 13-132. DMA Transmit Mode** 

1398 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.1.3.6 Mode Selection**_ 

The MMC/SD/SDIO host controller can be use in two modes, MMC and SD/SDIO modes. It has been designed to be the most transparent with the type of card. The type of the card connected is differentiated by the software initialization procedure. 

Software identifies the type of card connected during software initialization. For each given card type, there are corresponding commands. Some commands are not supported by all cards. See the _Multimedia Card System Specification_ , the _SD Memory Card Specifications_ , and the _SDIO Card Specification, Part E1_ for more details. 

The purpose of the module is to transfer commands and data, to whatever card is connected, respecting the protocol of the connected card. Writes and reads to the card must respect the appropriate protocol of that card. 

## _**13.3.1.3.7 Buffer Management**_ 

## _**13.3.1.3.7.1 Data Buffer**_ 

The MMC/SD/SDIO host controller uses a data buffer. This buffer transfers data from one data bus (Interconnect) to another data bus (SD, SDIO, or MMC card bus) and vice versa. 

The buffer is the heart of the interface and ensures the transfer between the two interfaces (L4 and the card). To enhance performance, the data buffer is completed by a prefetch register and a post-write buffer that are not accessible by the host controller. 

The read access time of the prefetch register is faster than the one of the data buffer. The prefetch register allows data to be read from the data buffer at an increased speed by preloading data into the prefetch register. 

The entry point of the data buffer, the prefetch buffer, and the post-write buffer is the 32-bit register MMC_DATA. A write access to the MMC_DATA register followed by a read access from the MMC_DATA register corresponds to a write access to the post-write buffer followed by a read access to the prefetch buffer. As a consequence, it is normal that the data of the write access to the MMC_DATA register and the data of the read access to the MMC_DATA register are different. 

The number of 32-bit accesses to the MMC_DATA register that are needed to read (or write) a data block with a size of MMC_BLK[10:0] BLEN, and equals the rounded up result of BLEN divided by 4. The maximum block size supported by the host controller is hard-coded in the register MMC_CAPA[17:16] MBL field and cannot be changed. 

A read access to the MMC_DATA register is allowed only when the buffer read enable status is set to 1 (MMC_PSTATE[11] BRE); otherwise, a bad access (MMC_STAT[29] BADA) is signaled. 

A write access to the MMC_DATA register is allowed only when the buffer write enable status is set to 1 (MMC_PSTATE[10] BWE); otherwise, a bad access (MMC_STAT[29] BADA) is signaled and the data is not written. 

The data buffer has two modes of operation to store and read of the first and second portions of the data buffer: 

- When the size of the data block to transfer is less than or equal to MEM_SIZE/2 (in double buffering), two data transfers can occur from one data bus to the other data bus and vice versa at the same time. The MMC/SD/SDIO controller uses the two portions of the data buffer in a ping-pong manner so that storing and reading of the first and second portions of the data buffer are automatically interchanged from time to time so that data may be read from one portion (for instance, through a DMA read access on the interconnect bus) while data (for instance, from the card) is being stored into the other portion and vice versa. When BLEN is less than or equal to 200h (that is, less or equal to 512Bytes), each of the two portions of the buffer that can be used have a size of BLEN (that is, 32-bits x BLEN div by 4). Not more than this total size of 2 times 32-bits × BLEN div by 4 can be used. 

- When the size of the data block to transfer is larger than MEM_SIZE/2, only one data transfer can occur from one data bus to the other data bus at a time. The MMC/SD/SDIO host controller uses the entire data buffer as a single portion. In this mode, a bad access (MMC_STAT[29] BADA) is signaled when two data transfers occur from one data bus to the other data bus and vice versa at the same time. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1399 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **CAUTION** 

The MMC_CMD[4] DDIR bit must be configured before a transfer to indicate the direction of the transfer. 

Figure 13-133 shows the buffer management for writing and Figure 13-134 shows the buffer management for reading. 

**==> picture [391 x 400] intentionally omitted <==**

**----- Start of picture text -----**<br>
MEM_SIZE/8<br>Write to card<br>1<br>Portion A<br>Write to<br>SD_DATA 2’<br>Portion B<br>128 words<br>Interconnect clock domain Interface (card) clock domain<br>Write<br>to<br>the card<br>2 occurs only after 1<br>When 2 is completed, 2’ occurs only after 1’ SD_CMD[DDIR]=0<br>128 words<br>Write to<br>SD_DATA<br>Portion A<br>2<br>Write to card<br>1’<br>Portion B<br>128 words<br>and are two different transfers that  occur at the same time.<br>32 bits<br>Card bus<br>32 bits<br>Interconnect bus<br>32 bits<br>Card bus<br>32 bits<br>Interconnect bus<br>**----- End of picture text -----**<br>


**Figure 13-133. Buffer Management for a Write** 

1400 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [378 x 403] intentionally omitted <==**

**----- Start of picture text -----**<br>
MEM_SIZE/8<br>Read from card<br>4<br>Portion A<br>Read from<br>SD_DATA 3’<br>Portion B<br>Interconnect clock domain Interface (card) clock domain<br>Read<br>to<br>the card<br>4 occurs only after 3<br>SD_CMD[DDIR]=1<br>When 4 is completed, 4’ occurs only after 3’<br>MEM_SIZE/8<br>Read from<br>SD_DATA<br>Portion A<br>3<br>Read from card<br>4’<br>Portion B<br>and are two different transfers that occur at the same time.<br>32 bits<br>Card bus<br>Interconnect bus 32 bits<br>32 bits<br>Card bus<br>Interconnect bus 32 bits<br>**----- End of picture text -----**<br>


**Figure 13-134. Buffer Management for a Read** 

## _**13.3.1.3.7.1.1 Memory Size, Block Length, and Buffer Management Relationship**_ 

The maximum block length and buffer management that can be targeted by system depend on memory depth setting. 

**Table 13-177. Memory Size, BLEN, and Buffer Relationship** 

|**Memory Size([5:2] MEMSIZE in bytes)**|**512**|**1024**|**2048**|**4096**|
|---|---|---|---|---|
|Maximum block length supported|512|1024|2048|2048|
|Double-buffering for maximum block length|N/A|BLEN <= 512|BLEN <= 1024|BLEN <= 2048|
|Single-buffering for block length|BLEN<=512|512 < BLEN <= 1024|1024 < BLEN <=|N/A|
||||2048||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1401 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1.3.7.1.2 Data Buffer Status**_ 

The data buffer status is defined in the following interrupt status register and status register: 

- Interrupt status registers (see MMC_STAT): 

   - MMC_STAT[29] BADA Bad access to data space 

   - MMC_STAT[5] BRR Buffer read ready 

   - MMC_STAT[4] BWR Buffer write ready 

- Status registers (see MMC_PSTATE): 

   - MMC_PSTATE[11] BRE Buffer read enable 

   - MMC_PSTATE[10] BWE Buffer write enable 

## _**13.3.1.3.8 Transfer Process**_ 

The process of a transfer is dependent on the type of command. It can be with or without a response, with or without data. 

## _**13.3.1.3.8.1 Different Types of Commands**_ 

Different types of commands are specific to MMC, SD, or SDIO cards. See the _Multimedia Card System Specification_ , the _SD Memory Card Specifications_ , the _SDIO Card Specification, Part E1_ , or the _SD Card Specification, Part A2, SD Host Controller Standard Specification_ for more details. 

## _**13.3.1.3.8.2 Different Types of Responses**_ 

Different types of responses are specific to MMC, SD, or SDIO cards. See the _Multimedia Card System Specification_ , the _SD Memory Card Specifications_ , the _SDIO Card Specification, Part E1_ , or the _SD Card Specification, Part A2, SD Host Controller Standard Specification_ for more details. 

Table 13-178 shows how the MMC, SD, and SDIO responses are stored in the MMC_RSPxx registers. 

**Table 13-178. MMC, SD, SDIO Responses in the MMC_RSPxx Registers** 

|**Kind of Response**|**Response Field**|**Response Register**|
|---|---|---|
|R1, R1b (normal response), R3, R4, R5, R5b, R6, R7|RESP[39:8](1)|MMC_RSP10[31:0]|
|R1b (Auto CMD12 response)|RESP[39:8](1)|MMC_RSP76[31:0]|
|R2|RESP[127:0](1)|MMC_RSP76[31:0]|
|||MMC_RSP54[31:0]|
|||MMC_RSP32[31:0]|
|||MMC_RSP10[31:0]|



(1) RESP refers to the command response format described in the specifications mentioned above. 

When the host controller modifies part of the MMC_RSPxx registers, it preserves the unmodified bits. 

The host controller stores the Auto CMD12 response in the MMC_RSP76[31:0] register because the Host Controller may have a multiple block data DAT line transfer executing concurrently with a command. This allows the host controller to avoid overwriting the Auto CMD12 response with the command response stored in MMC_RSP10 register and vice versa. 

1402 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.1.3.9 Transfer or Command Status and Error Reporting**_ 

Flags in the MMC/SD/SDIO host controller show status of communication with the card: 

- A timeout (of a command, a data, or a response) 

- A CRC 

Error conditions generate interrupts. See Table 13-179 and register description for more details. 

**Table 13-179. CC and TC Values Upon Error Detected** 

|**Error hold in**|**the**||||
|---|---|---|---|---|
|**MMC_STAT Register**||**CC**|**TC**|**Comments**|
|29|BADA|||No dependency with CC or TC.|
|||||BADA is related to the register accesses. Its assertion is not dependent of the|
|||||ongoing transfer.|
|28|CERR|1||CC is set upon CERR.|
|22|DEB||1|TC is set upon DEB.|
|21|DCRC||1|TC is set upon DCRC.|
|20|DTO|||DTO and TC are mutually exclusive.|
|||||DCRC and DEB cannot occur with DTO.|
|19|CIE|1||CC is set upon CIE.|
|18|CEB|1||CC is set upon CEB.|
|17|CCRC|1||CC can be set upon CCRC - See CTO comment|
|16|CTO|||CTO and CC are mutually exclusive.|
|||||CIE, CEB and CERR cannot occur with CTO.|
|||||CTO can occur at the same time as CCRC it indicates a command abort due to a|
|||||contention on CMD line. In this case no CC appears.|



MMC_STAT[21] DCRC event can be asserted in the following conditions: 

- Busy timeout for R1b, R5b response type 

- Busy timeout after write CRC status 

- Write CRC status timeout 

- Read data timeout 

- Boot acknowledge timeout 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1403 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1.3.9.1 Busy Timeout for R1b, R5b Response Type**_ 

Figure 13-135 shows DCRD event condition asserted when there is a busy timeout for R1b or R5b responses. 

**==> picture [292 x 193] intentionally omitted <==**

**Figure 13-135. Busy Timeout for R1b, R5b Responses** 

- t1 - Data timeout counter is loaded and starts after R1b, R5b response type. 

- t2 - Data timeout counter stops and if it is 0, MMC_STAT[21] DCRC is generated. 

## _**13.3.1.3.9.2 Busy Timeout After Write CRC Status**_ 

Figure 13-136 shows DCRC event condition asserted when there is busy timeout after write CRC status. 

**==> picture [424 x 194] intentionally omitted <==**

**Figure 13-136. Busy Timeout After Write CRC Status** 

- t1 - Data timeout counter is loaded and starts after CRC status. t2 - Data timeout counter stops and if it is 0, MMC_STAT[21] DCRC is generated. 

1404 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.1.3.9.3 Write CRC Status Timeout**_ 

Figure 13-137 shows DCRC event condition asserted when there is write CRC status timeout. 

**==> picture [260 x 217] intentionally omitted <==**

**Figure 13-137. Write CRC Status Timeout** 

- t1 - Data timeout counter is loaded and starts after Data block + CRC. 

- t2 - Data timeout counter stops and if it is 0, MMC_STAT[21] DCRC is generated. 

## _**13.3.1.3.9.4 Read Data Timeout**_ 

Figure 13-138 shows DCRC event condition asserted when there is read data timeout. 

**==> picture [340 x 179] intentionally omitted <==**

**Figure 13-138. Read Data Timeout** 

- t1 - Data timeout counter is loaded and starts after Command transmission. 

- t2 - Data timeout counter stops and if it is 0, MMC_STAT[21] DCRC is generated. 

- t3 - Data timeout counter is loaded and starts after Data block + CRC transmission. 

- t4 - Data timeout counter stops and if it is 0, MMC_STAT[21] DCRC is generated. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1405 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1.3.10 Transfer Stop**_ 

Whenever a transfer is initiated, the transmission may be willed to stop whereas it is still not finished. Several cases can be faced depending on the transfer type: 

- Multiple blocks oriented transfers (for which transfer length is known) 

- Continuous stream transfers (which have an infinite length) 

## **Note** 

Since the MMC/SD/SDIO controller manages transfers based on a block granularity, the buffer will accept a block only if there is enough space to completely store it. Consequently, if a block is pending in the buffer, no command will be sent to the card because the card clock will be shut off by the controller. 

The MMC/SD/SDIO controller includes two features which make a transfer stop more convenient and easier to manage: 

- Stop at block gap 

This feature is enabled by setting the MMC_HCTL[16] SBGR bit to 1. When enabled, this capability holds the transfer on until the end of a block boundary. If a stop transmission is needed, software can use this pause to send a CMD12 to the card. 

Table 13-180 shows the common ways to stop a transfer, indicating command to send and features to enable. 

**Table 13-180. MMC/SD/SDIO Controller Transfer Stop Command Summary** 

|**WRITE Transfer**<br>**READ Transfer**|**WRITE Transfer**<br>**READ Transfer**|**WRITE Transfer**<br>**READ Transfer**|**WRITE Transfer**<br>**READ Transfer**|**WRITE Transfer**<br>**READ Transfer**|
|---|---|---|---|---|
|||MMC/SD<br>SDIO|MMC/SD|SDIO|
|Single block||Transfer ends<br>automatically<br>Wait TC<br>Transfer ends<br>automatically<br>Wait TC|Transfer ends<br>automatically<br>Wait TC|Transfer ends<br>automatically<br>Wait TC|
|Multi blocks<br>(finite or infinite)|Before the<br>programmed block<br>boundary|Send CMD12<br>Wait TC<br>Send CMD52<br>Wait TC|Send CMD12<br>Wait TC|Send CMD52<br>Wait TC|
||Stop at the end of the<br>transfer<br>(finite transfer only)|Set MMC_HCTL[16]<br>SBGR bit to 1.<br>Send CMD52<br>Wait TC||**If READ_WAIT**<br>**supported**<br>Stop at block gap<br>Wait TC|
|||||**If READ_WAIT not**<br>**supported**<br>Send CMD52<br>Wait TC|



## **Note** 

The MMC/SD/SDIO controller will send the stop command to the card on a block boundary, regardless the moment the command was written to the controller registers. 

1406 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.1.3.11 Output Signals Generation**_ 

The MMC/SD/SDIO output signals can be driven on either falling edge or rising edge depending on the MMC_HCTL[2] HSPE bit. This feature allows to reach better timing performance, and thus to increase data transfer frequency. 

## _**13.3.1.3.11.1 Generation on Falling Edge of MMC Clock**_ 

The controller is by default in this mode to maximize hold timings. In this case, MMC_HCTL[2] HSPE bit is cleared to 0. 

Figure 13-139 shows the output signals of the module when generating from the falling edge of the MMC clock. 

**==> picture [309 x 149] intentionally omitted <==**

**----- Start of picture text -----**<br>
tCP<br>clk tC2<br>tC1<br>tMOS tMOH<br>cmd, dat[x:0]<br>(Host � Card) Valid OUT<br>tMIS tMiH<br>cmd, dat[x:0]<br>(Host � Card) Valid IN<br>**----- End of picture text -----**<br>


**==> picture [57 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
Data Sampling<br>**----- End of picture text -----**<br>


**Figure 13-139. Output Driven on Falling Edge** 

- **tMOS** - tM Output Setup 

- **tMOH** - tM Output Hold 

- **tMIS** - tM Input Setup 

- **tMIH** - tM Output Hold 

## _**13.3.1.3.11.2 Generation on Rising Edge of MMC Clock**_ 

This mode increases setup timings and allows reaching higher bus frequency. This feature is activated by setting MMC_HCTL[2] HSPE bit to 1. The controller shall be set in this mode to support SDR transfers. 

## **Note** 

Do not use this feature in Dual Data Rate mode (when MMC_CON[19] DDR is set to 1). 

Figure 13-140 shows the output signals of the module when generating from the rising edge of the MMC clock. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1407 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [340 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
tCP<br>tC2<br>clk tC1<br>tMOS<br>tMOH<br>cmd, dat[x:0]<br>(Host � Card) Valid OUT<br>tMIS tMiH<br>cmd, dat[x:0]<br>(Host � Card) Valid IN<br>Data Sampling<br>**----- End of picture text -----**<br>


## **Figure 13-140. Output Driven on Rising Edge** 

- **tMOS** - tM Output Setup 

- **tMOH** - tM Output Hold 

- **tMIS** - tM Input Setup 

- **tMIH** - tM Output Hold 

1408 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.1.3.12 CE-ATA Command Completion Disable Management**_ 

The MMC/SD/SDIO controller supports CE-ATA features, in particular the detection of command completion token. When a command that requires a command completion signal (MMC_CON[12] CEATA and MMC_CMD[2] ACEN set to 1) is launched, the host system is no longer allowed to emit a new command in parallel of data transfer unless it is a command completion disable token. 

The settings to emit a command completion disable token follow: 

- MMC_CON[12] CEATA is set to 1. 

- MMC_CON[2] HR set to 1. 

- Clear the MMC_ARG register. 

- Write into MMC_CMD register with value 0000 0000h. 

When a command completion disable token was emitted (that is, MMC_STAT[0] CC received), the host system is again allowed to emit another type of command (for example a transfer abort command CMD12 to abort transfer). 

A critical case can be met when command completion signal disable (CCSD) is emitted during the last data block transfer, the sequence on command line could be sent very close to command completion signal (CCS) token sent by the card. 

Three cases can be met: 

- CCS is receive just before CCSD is emitted: 

   - An interrupt CIRQ is generated with CCS detection, CCSD is transmitted to card then an interrupt CC is generated when CCSD ends. In this case, card consider the CCSD sequence. 

- CCS is not generated or generated during the CCSD transfer: 

The CCS bit cannot be detected (conflict is not possible as they drive the same level on command line, then no CIRQ interrupt is generated; besides CC interrupt is generated when CCSD ends). 

- CCS is generated without CCSD token required: 

Only the interrupt CIRQ is generated when CCS is detected. 

## _**13.3.1.3.13 Test Registers**_ 

Test registers are available to be compliant with SD Host controller specification. This feature is useful to generate interrupts manually for driver debugging. The Force Event register (MMC_FE) is used to control the Error Interrupt Status and Auto CMD12 Error Status. The System Test register (MMC_SYSTEST) is used to control the signals that connect to I/O pins when the module is configured in system test (MMC_CON[4] MODE = 1) mode for boundary connectivity verification. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1409 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1.3.14 MMC/SD/SDIO Hardware Status Features**_ 

Table 13-181 summarizes the MMC/SD/SDIO hardware status features. 

**Table 13-181. MMC/SD/SDIO Hardware Status Features** 

|||**Register/Bit Field/Observability**||
|---|---|---|---|
|**Feature**|**Type**|**Control**|**Description**|
|Interrupt flags||SeeSection 13.3.1.3.4.||
|CMD line signal level|Status|[24] CLEV|Indicates the level of the cmd line|
|DAT lines signal level|Status|[23:20] DLEV|Indicates the level of the data lines|
|Buffer read enable|Status|[11] BRE|Readable data exists in the buffer.|
|Buffer write enable|Status|[10] BWE|Indicates whether there is enough space in the|
||||buffer to write BLEN bytes of data|
|Read transfer active|Status|[9] RTA|This status is used for detecting completion of a|
||||read transfer.|
|Write transfer active|Status|[8] WTA|This status indicates a write transfer active.|
|Data line active|Status|[2] DLA|Indicates whether the data lines are active|
|Command Inhibit (data lines)|Status|[1] DATI|Indicates whether issuing of command using data|
||||lines is allowed|
|Command inhibit (CMD line)|Status|[0] CMDI|Indicates whether issuing of command using CMD|
||||line is allowed|



1410 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.3.1.4 Low-Level Programming Models** 

## _**13.3.1.4.1 Surrounding Modules Global Initialization**_ 

This section identifies the requirements of initializing the surrounding modules when the module has to be used for the first time after a device reset. This initialization of surrounding modules is based on the integration and environment of the MMC/SD/SDIO modules. 

**Table 13-182. Global Init for Surrounding Modules** 

|**Surrounding Modules**|**Comments**|
|---|---|
|Power, Reset, and Clocking|Module interface and functional clocks must be enabled. For more information on power, reset, and|
||clock management, see the corresponding sections within the_Device Configuration_chapter.|
|Control Module|Module-specific pad muxing and configuration must be set in the control module. For more information,|
||see the section within the_Device Configuration_chapter.|
|(optional) VIM|VIM configuration must be done to enable the interrupts from the SD module. See_Interrupts_.|
|(optional) EDMA|DMA configuration must be done to enable the module DMA channel requests. See_EDMA_.|
|(optional) Interconnect|For more information about the interconnect configuration, see_System Interconnect_.|



## **Note** 

The Vector Interrupt Manager and the EDMA configurations are necessary if the interrupt and DMA based communication modes are used. 

## _**13.3.1.4.2 MMC/SD/SDIO Controller Initialization Flow**_ 

The next sections outline the four steps to initialize the MMC/SD/SDIO controller: 

- Initialize Clocks 

- Software reset of the controller 

- Set module's hardware capabilities 

- Set module's Idle and Wake-Up modes 

## _**13.3.1.4.2.1 Enable OCP and CLKADPI Clocks**_ 

Prior to any SD register access one must enable the SD OCP clock and CLKADPI clock in PRCM module registers. For more information, see , _Power, Reset, and Clock Management_ . 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1411 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.1.4.2.2 SD Soft Reset Flow**_ 

Figure 13-141 shows the soft reset process of MMC/SD/SDIO controller. 

**==> picture [184 x 255] intentionally omitted <==**

**----- Start of picture text -----**<br>
Start<br>Set the SD_SYSCONFIG[1]<br>SOFTRESET bit to 0x1<br>Read the<br>SD_SYSSTATUS[0]<br>RESETDONE bit<br>No<br>RESETDONE = 0x1?<br>Yes<br>End<br>**----- End of picture text -----**<br>


**Figure 13-141. MMC/SD/SDIO Controller Software Reset Flow** 

## _**13.3.1.4.2.3 Set SD Default Capabilities**_ 

Software must read capabilities (in boot ROM for instance) and is allowed to set (write) MMC_CAPA[26:24] and MMC_CUR_CAPA[23:0] registers before the MMC/SD/SDIO host driver is started. 

## _**13.3.1.4.2.4 Wake-Up Configuration**_ 

Table 13-183 details SD controller wake-up configuration. 

**Table 13-183. MMC/SD/SDIO Controller Wake-Up Configuration** 

|**Step**|**Access Type**|**Register/Bit Field/Programming Model**|
|---|---|---|
|Configure wake-up bit (if necessary).|W|MMC_SYSCONFIG[2] ENAWAKEUP|
|Enable wake-up events on SD card interrupt (if|W|MMC_HCTL[24] IWE|
|necessary).|||
|SDIO Card onlyEnable card interrupt (if necessary).|W|MMC_IE[8] CIRQENABLE|



## _**13.3.1.4.2.5 MMC Host and Bus Configuration**_ 

Figure 13-142 details the MMC bus configuration process. 

1412 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [424 x 556] intentionally omitted <==**

**----- Start of picture text -----**<br>
Start<br>Write SD_CON register<br>(OD, DW8, CEATA) to configure specific<br>data and command transfer<br>Write SD_HCTL register<br>(SDVS, SDBP, DTW) to configure the card voltage<br>value and power mode and data bus width<br>If the configuration set in the SDVS field is<br>not compliant with the supported voltage set<br>in the SD_CAPA register, SDBP returns to 0x0.<br>Read back the<br>SD_HCTL[8] SDBP bit<br>NO<br>SDBP = 0x1  ?<br>YES<br>Set the SD_SYSCTL[0] ICE<br>bit to 0x1 to enable the internal clock<br>For initialization sequence, you should have<br>80 clock cycles in 1ms.<br>Configure the It means clock frequency should be ≤ 80 kHz<br>SD_SYSCTL[15:6] CLKD<br>bit field<br>Read the SD_SYSCTL[1] ICS bit<br>NO<br>ICS = 0x1 ?<br>YES<br>Clock is stable<br>Write the SD_SYSCONFIG<br>CLOCKACTIVITY, SIDLEMODE, and<br>AUTOIDLE fields to configure the<br>behavior of the module in idle mode<br>End<br>**----- End of picture text -----**<br>


**Figure 13-142. MMC/SD/SDIO Controller Bus Configuration Flow** 

## _**13.3.1.4.3 Operational Modes Configuration**_ 

## _**13.3.1.4.3.1 Basic Operations for MMC/SD/SDIO Host Controller**_ 

The MMC/SD/SDIO controller performs data transfers: data to card (referred to as write transfers) and data from card (referred to as read transfers). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1413 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

The host controller requires transfers to run on a block-by-block basis, rather than on a DMA burst size basis. A single DMA request (or block request interrupt) is signaled for each block. Pipelining is supported as long as the block size is less than one half of the memory buffer size. 

## _**13.3.1.4.3.2 Card Detection, Identification, and Selection**_ 

Figure 13-143 and Figure 13-144 show the card identification and selection process. 

**==> picture [500 x 404] intentionally omitted <==**

**----- Start of picture text -----**<br>
A<br>Start<br>Send a CMD5 command<br>Module initialization<br>Read the SD_STAT<br>register<br>Set SD_CON[1] INIT bit to<br>0x1 to send an initialization stream<br>Yes<br>CC = 0x1?<br>(it is an SDIO card)<br>No<br>Write 0x0000 0000 in the<br>SD_CMD register No See the SDIO Standard Specification to<br>identify the card type:<br>CTO = 0x1? Memory only, I/O only, Combo<br>Wait 1 ms Yes<br>End<br>Set SD_SYSCTL[25] SRC<br>bit to 0x1 and wait until it returns to 0x0<br>Set SD_STAT[0] CC bit<br>to 0x1 to clear the flag<br>Send a CMD8 command<br>Set SD_CON[1] INIT bit to<br>0x0 to end the initialization sequence<br>Read the SD_STAT<br>register<br>Clear SD_STAT register<br>(write 0xFFFF FFFF) CC = 0x1? YES<br>(it is an SD card compliant<br>with standard 2.0 or later)<br>No<br>Change clock frequencyto fit protocol No See the SD Standard Specification version2.0 or later to identify the card type:<br>CTO = 0x1? High Capacity; Standard Capacity<br>Yes<br>End<br>Send a CMD0 command<br>Set SD_SYSCTL[25] SRC<br>bit to 0x1 and wait until it returns to 0x0<br>A<br>A<br>**----- End of picture text -----**<br>


**Figure 13-143. MMC/SD/SDIO Controller Card Identification and Selection - Part 1** 

1414 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [434 x 536] intentionally omitted <==**

**----- Start of picture text -----**<br>
A<br>Send an CMD55 command<br>Send an ACMD41 command<br>Read the SD_STAT<br>register<br>YES<br>CC = 0x1 ?<br>(it is a SD card compliant<br>with standard 1.x)<br>NO<br>Verify the card is busy: read the<br>SD_RSP10[31] bit<br>NO<br>CTO = 0x1 ?<br>YES NO<br>Is it equal to 0x1 ?<br>(It is a MMC card) (The card is busy)<br>Set SD_SYSCTL[25] SRC<br>YES<br>bit to 0x1 and wait until it returns to 0x0<br>(The card is not busy)<br>Send an CMD1 command*<br>B YES, and all cards<br>are not identified<br>Read the SD_STAT Send a CMD2 command to get<br>register information on how to access<br>the card content<br>(unknown<br>type of card)<br>YES<br>CTO = 0x1 ?<br>Send a CMD3 command<br>NO<br>End<br>CC = 0x1 ? NO SD cards Card type? MMC cards<br>YES<br>(It is a MMC card) Is there more than one MMC<br>connected to the same bus, and are<br>Verify the card is busy: read the<br>they all indentified<br>SD_RSP10[31] bit<br>NO, or all cards<br>are identified<br>NO<br>Is it equal to 0x1 ?<br>(The card is busy)<br>YES<br>(The card is not busy) Send a CMD7 command<br>B<br>End<br>*With OCR 0.<br>**----- End of picture text -----**<br>


**Figure 13-144. MMC/SD/SDIO Controller Card Identification and Selection - Part 2** 

## _**13.3.2 OptiFlash Submodules**_ 

## **13.3.2.1 RL2_OF** 

This section describes about RL2_OF module in this device. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1415 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.1.1 RL2_OF Overview**_ 

The SOC implements one RL2_OF module per each CPU of the R5F Subsystem, as shown in RL2_OF Block Diagram. The RL2_OF sits between the AXI2VBUSM bridge and the Core VBUSM interconnect on the data path, and on the R5SS0/1 Config Slave Interconnect on the config path. 

The RL2_OF (Remote L2 _OptiFlash) module consists of three engines for Improving the Flash Performance, as follows: 

1. RAT - Region based Address Translation. RAT enables virtualized access to shared memory code. 

2. FLC - Fast Local Copy allowing code in slow access memory to be placed into on-chip memory (such as SRAM, TCM) for fast access. 

3. RL2 - Remote L2 is a Level 2 cache controller with remote cache data storage memory for the data. That is, you can cache the system Flash into SOC memory system. 

**==> picture [434 x 393] intentionally omitted <==**

**Figure 13-145. RL2_OF Block Diagram** 

## _**13.3.2.1.2 Remote L2 (RL2)**_ 

## _**13.3.2.1.2.1 RL2 Overview**_ 

The Remote L2 (RL2) module acts as a Level 2 cache controller as it provides additional caching, specific to Flash storage, beyond CPU Core’s L1 caching. The RL2 is responsible for caching 1 to 16MB of target space, 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1416 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

using system memory for the cache data storage i.e. the actual cache memory can be part of any system memory, e.g. On-chip SRAM (remote cache data storage memory), instead of a dedicated cache storage within the controller. This allows for flexible configuration for target applications. 

The RL2 is an 8 Way set associative read allocate LRU cache. The RL2 allocation is based on full cache line reads. The SET index is based on the programmed operating size. 

The RL2 uses 32-byte cache lines which matches the R5 CPU cache line so that optimal performance is achieved. That is the RL2 does not read more data than the CPU requested. Once a cache line is in the RL2, the CPU could read any quanta of data from that cache line. Any data which is less that 32-Bytes will not be cached by RL2. 

The RL2 also supports a Dual Mode, which allows two cache lines to share a single WAY offering double the remote cache data storage memory while only using the same number of total cache line entries supported. Since Dual Mode shares the same bits within a WAY, the cache-able range is reduced to support the management for the two sub cache lines. 

## _**13.3.2.1.2.2 RL2 Supported Features**_ 

- Up to 4096 L2 cache lines supported 

- 32 byte cache line size supported 

- Configurable cache size up to 4096 entries; 8K, 16K, 32K, 64K, 128K. Note: The cacheable target space will proportionately vary based on the cache size. 

   - Up to 1MB of cacheable target space for 8KB of cache 

   - Up to 2MB of cacheable target space for 16KB of cache 

   - Up to 4MB of cacheable target space for 32KB of cache 

   - Up to 8MB of cacheable target space for 64KB of cache 

   - Up to 16MB of cacheable target space for 128KB of cache 

   - Up to 8MB of cacheable target space for 256KB of cache (Dual Mode) 

- 8-Way set associative LRU Cache 

- ECC protected Tag LRU RAM 

- Passthrough for address not within the cacheable range. 

- Support critical word first access from R5F CPU 

## _**13.3.2.1.2.3 Tightly Coupled RL2 Tag Memory**_ 

The RL2 has an integrated Tag RAM for tag information that is _SETs_ deep and _WAYs_ times _WAY_ info wide. This memory start auto initialization when a write to the _L2_CTRL.size_ field occurs that changes the current size, or the _L2_CTRL.enable_ bit is changed from a '0' to a '1' and all pending operations have completed. The RL2 performs any correctable ECC writeback in the event ECC is enabled and a single error correct occurs. The memory is not used until the L2_CTRL.size field is written and the L2_CTRL.enable bit is set. 

The tag memory auto initialization preloads the LRU info into each way of all the defined sets. The _L2_STS.ok_to_go_ status bit indicates that Tag/LRU RAM has been initialized and the cache is in an operable state. 

## _**13.3.2.1.2.4 Remote Cache Data Storage Memory**_ 

Theremote cache data storage memory stores the cache data managed by the RL2 module. RL2 cache use up to three remote cache data storage memory ranges to place the L2 data within. The _REM[n]_ADR_LSW_ (n=0,1,2) defines the least significant portion of the remote address of the remote cache data storage memory. The length of these ranges must be greater or equal to the size specified by _L2_CTRL.size_ . The _REM[n]_LEN_ (n=0,1,2) defines the amount of remote cache data storage memory in 64 byte aligned quanta used starting from the _REM[n]_ADR_LSW_ address. The RL2 consumes remote cache data storage memory ranges in numeric order. Range 0 is consumed prior to range 1, followed by range 2. 

The RL2 can cache a up to 16MB of target memory as defined by _L2_LO_ >=CachedRange<= _L2_HI_ , where _L2_LO_ defines the least significant portion of the target low address and _L2_HI_ defines the least significant portion of the target high address for RL2 to cache. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1417 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

The remote cache data storage memory stores the 8 _WAYs_ consecutively for each _SET_ address. In Dual Mode each _WAY_ has two 32-byte cache lines (64 bytes) versus other _L2_CTRL.size_ values which only hold a single 32-byte cache line _WAY._ In dual Mode the _WAY_ has a high and low sub cache line, the high is stored at the higher address and the low is stored at the _WAY_ base. 

**Table 13-184. Remote Cache Data Storage Example** 

WAY N... WAY 0 - SET 0 WAY N... WAY 0 - SET 1 ... ... WAY N... WAY 0 - SET (M-1) WAY N... WAY 0 - SET M 

## _**13.3.2.1.2.5 RL2 Cache Allocation**_ 

The RL2 allocates a WAY based on Least Recently Used (LRU) algorithm. 

The RL2 allocation is based on full 32 byte read burst within the range of the specified target area. Once cached, any size or wrapping burst request to the same line can occur and will read the cached data. In the event that an allocated cache line returns an error on the read from thecacheable target, the allocation will restore the LRU aging such that the next allocated _WAY_ is invalidated due to the target response error. 

Writing to the cacheable range will disable the RL2 caching until the error is processed. That is a write command that is within the cacheable will set the _wr_hit_ error bit in the Interrupt Raw Status Register, when any of the bits are set in the Interrupt Raw Status Register the RL2 cache is in a logically disabled state. 

That is, the RL2 is only intended to cache instruction data, any write to cacheable range will disable the cache. 

## _**13.3.2.1.2.6 RL2 Statistics**_ 

The RL2 provides two statistic registers that count the hits and misses of the RL2 cache function. 

The _L2_HIT_ Counter register holds the number of L2 Hits to the Remote data storage memory. The _L2_MISS_ Counter register holds the number of L2 Misses to the Remote data storage memory. 

These counters are cleared when the RL2 function is auto-initialized. A write to the counter will set the value written (This is mainly for debug to validate roll over). The statistics counters do not roll over, if they hit their maximum value, they will stay there. That is once the counter reaches 0xFFFFFFFF it will no longer increment. 

## _**13.3.2.1.2.7 Dual Mode**_ 

The DualMode is an extension of the RL2 that supports two times that max remote cache data storage memory while keeping the tag RAM the same size. That is each way instead of representing a single cache line, represents two consecutive cache lines. This allows the remote cache data storage memory to be twice as large using the same tag RAM. When the _L2_CTRL.size_ is set to 5 the dual mode is selected. In this mode there are the same number of cache line entries (4096),but the remote cache data storage memory is doubled. Each _WAY_ now supports 64 bytes of cache data in two halves, a high and low sub cache line. This allows twice as much memory while keeping the same number of cache entries. When in this mode, the tag field is reduced by two bits to make room for the extra valid bits for the two sub lines held. This reduction reduces the cacheable range the RL2 can cache. 

## _**13.3.2.1.2.8 Critical Word First (CWF)**_ 

Critical Word First is a CPU cache concept which states that although the CPU wishes to fetch a particular cache line, the CPU prefers to see an offset into the cache line prior to seeing the beginning of the cache line. This is also known as wrapping burst, where a burst request to a cache line is not aligned to the start of the cache line. RL2 supports critical word first access from R5F CPU. For example, if the CPU jumps to the last word of a cache line not currently in the L1, the CPU requests a cache line burst, but the starting address of the burst 

1418 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

is the last bus aligned word address. Say the cache line size is 32 bytes, and the bus width is 64 bits wide. If the CPU jumps to an address of 0x1c offset into a particular non-allocated cache line, the CPU requests address 0x18 in a wrapping burst of 32 bytes, resulting in offset addresses 0x18, 0x00, 0x08, 0x10 being the burst order requested. This is known as critical word first or wrapping burst request. That is the offset 0x18 is the critical word the CPU want to see in the cache line. 

## _**13.3.2.1.3 Fast Local Copy (FLC)**_ 

## _**13.3.2.1.3.1 FLC Overview**_ 

The FLC module consists of a DMA engine that allows a region of the slow memory like Flash to be dynamically copied to a section of system on-chip memory (such as SRAM, TCM), and while that is happening, can be running the code that was specified to be copied. The CPU does not have to wait for the entire copy to complete. It can start executing immediately after FLC copy has been triggered. 

The FLC will redirect the request to the on-chip memory on the fly if the data has been transferred to the on-chip memory. Otherwise the request is sent to the slow device. This allows the Software to specify a piece of code to be resident in the system but executed out of the flash using on-chip system memory. The on-chip memory redirection does not wait till the entire region is mirrored, but is enabled as soon as the content at that address is valid in the memory. Also, the FLC will copy data only when the CPU bus is idle. 

The FLC will transfer any enabled FLC range in order from FLC range 0 through 3. The _FLC[n]_LO_ and _FLC[n]_HI_ (n=0,1,2,3) registers defines the start and end address of the FLC range in the source memory (such as Flash). The FLC range is defined by _FLC[n]_LO>=_ FLCrang _e<FLC[n]_HI._ 

The FLC ranges can start and end on any 4K Byte boundary. Care must be taken as to not create overlapping ranges across regions. The minimum size of a FLC region is 4K Bytes. 

The _FLC[n]_RA_ (n=0,1,2,3) remote address registers specifies the base address of the destination memory (such as SRAM) that the FLC will copy data to, from the source memory. The destination memory must be large enough for the specified range. The _FLC[n]_CTRL.fenable_ enables the given range _FLC[n]_LO>=_ FLCrang _e<FLC[n]_HI_ to be copied to the _FLC[n]_RA_ SRAM memory (n=0,1,2,3). The FLC will automatically transfer FLC ranges to the FLC Remote Address specified for that range. The RL2_OF module will only transfer a single FLC range at a time. _FLC_STS.cpycmp_ will indicates which FLC range is complete. 

Disabling a FLC range during the transfer will cause the transfer to stop, and when all pending transactions for that FLC completes, the next possible enabled FLC range will commence. 

The FLC transfer will be aborted if the FLC data returned from the range has an error or the write to the FLC target memory returns an error. In this case all FLC transfers are disabled until the error interrupt is cleared. Only completed FLC transfers will operate during a FLC posted error. 

Since the copy of FLC range is independent from RAT ranges, the FLC copy function could be used to transfer the Flash data to the RAT target address. But do remember that the FLC range will access the target if it is already copied. So once copied, the FLC range should be disabled. 

## **Note** 

If FLC address Range Overlaps with RL2 range and the FLC CPU request is not in the FLC RAM as of yet, the RL2 will cache that location until the FLC copy passes that address. 

## _**13.3.2.1.3.1.1 FLC Supported Features**_ 

- Supports 4 ranges that can be copied to a remote internal SRAM 

- Ranges can start and finish on any 4KB boundary 

- Redirect access to Flash when the data is not yet available in on-chip memory. 

- Redirect access to on-chip memory when the data is available in the on-chip memory. 

- Transparent to CPU after initial configuration of regions. 

- Passthrough for address not in the programmed regions. 

- Interrupt generation when mirroring of region is complete. 

- Option to disable DMA copy and only enable memory data redirection. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1419 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.1.4 Region based Address Translation (RAT)**_ 

## _**13.3.2.1.4.1 RAT Overview**_ 

Region-based Address Translation (RAT): A mechanism that enables memory map segment relocation by modifying the target address of memory requests. RAT performs address translation only and preserves the following request attributes: 

1. Original size request 

2. Data Content 

## **Note** 

RAT purely handles address remapping and does not modify any other aspects of the memory request. 

There are up to 4 RAT regions supported. The _RAT[n]_RBA_ (n=0,1,2,3) specifies the base address of a RAT region ‘n’. It is the source address for matching to a region. The _RAT[n]_RTA_ (n=0,1,2,3) specifies the translated address of a RAT region ‘n’. It is the translated address to which the source address is mapped. 

The size of a RAT region is specified by the RAT control register field _RAT[n]_CTRL.SIZE_ . Setting the _RAT[n]_CTRL.REN_ bit will enable the address translation for that particular region. 

## **Note** 

Any enabled RAT region will not be translated or processed by (FLC) or (RL2) ranges. That is, RAT region address translation takes priority over FLC and RL2 address translation. 

## **Note** 

Configuring RAT regions that overlap with other RAT regions will result in the OR of the resultant addresses. Hence, overlapping RAT ranges are not supported. 

## _**13.3.2.1.4.1.1 RAT Supported Features**_ 

- Supports 4 regions to be translated 

   - 

- Each region can be configured for 4K to 4G Bytes. The minimum size of a RAT region is 4KB. 

## _**13.3.2.1.5 RL2_OF Interrupts and Error Handling**_ 

The RL2_OF module gives out a single interrupt combining all the FLC/RL2 error/status events as follows: 

1. FLC done: The FLC has completed the transfer to the FLC range. This is indicated by the _flc_don_ bit in the Interrupt Raw Status Register. 

2. FLC write error: A write error from FLC remote range (target memory) has occurred. This is indicated by the _flc_wrerr_ bit in the Interrupt Raw Status Register and the FLC is logically disabled. 

3. FLC read error: A read error on the data returned from FLC range has occurred. This is indicated by the _flc_rderr_ bit in the Interrupt Raw Status Register and the FLC is logically disabled. 

4. RL2 write hit: Any write to the RL2 cacheable range, while the RL2 cache is enabled and operating, has occurred potentially causing a coherency issue. This is indicated by the _wr_hit_ bit in the Interrupt Raw Status Register and the RL2 is logically disabled. 

5. RL2 write error: Any write to the remote cache data storage memory due to a read allocation (during cache miss) that returns a write error has occurred. This is indicated by the _wr_err_ bit in the Interrupt Raw Status Register and the RL2 is logically disabled. 

Any read or write error on the RAT translated memory range is pass through to the originator. Also, any read or write error on FLC ranges during the originator request is also pass through to the originator. 

For any read within cacheable range that is not currently cached, that meets RL2 allocation policy, and returns a read error, the following occurs: 

- The error is passed through to the initiator 

- The remote cache data storage memory is written with the errant data. 

1420 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- The cache line is marked invalid 

- If not in Dual Mode or only a single cache line is allocated within the WAY, the WAY LRU is reverted and marked as the oldest WAY for future allocations 

## _**13.3.2.1.6 Emulation Debug**_ 

When the _EMUDBG_ signal is set for a RAT transaction, the region address translation occurs as is. 

When the _EMUDBG_ signal is set for any FLC transaction, the FLC pauses the copy function if copying until a non _EMUDBG_ transaction is seen. This simulate what happens if user is single stepping the processor. 

When the _EMUDBG_ signal is set for a RL2 transaction, the cache state is maintained. That is, _EMUDBG_ request won't allocate a cache line in the case of a 'miss', or update the LRU state in the case of a 'hit'. But if the address is within the cache, the _EMUDBG_ request gets the data from the remote cache data storage memory. 

## _**13.3.2.1.7 RL2_OF Safety Implementation**_ 

Each R5F subsystem (R5FSS) in the device implements two instances of the RL2_OF modules that can run in lockstep. RL2 instances run in sync with the R5F CPU lockstep mode of operation, to detect faults that may result in unsafe operating conditions. The CCM-RL2_OF detects faults and signals them to the SOC error signaling module. Figure RL2_OF Lockstep Implementation shows the safety lockstep implementation of the RL2_OF modules. 

**==> picture [500 x 199] intentionally omitted <==**

**Figure 13-146. RL2_OF Lockstep Implementation** 

## **Input Handling:** 

Identical inputs are provided to both RL2_OF module copies CCM-RL2_OF compares all outputs from both copies, including: 

1. Core bus outputs 

2. RAM control signals 

## **Error Detection:** 

CCMR compare error is triggered if outputs from the two copies mismatch 

To prevent common mode failures: 

1. _Primary RL2_OF:_ Output signals are delayed by 2 cycles 

2. _Checker RL2_OF:_ Input signals are delayed by 2 cycles 

During lockstep mode, outputs are clamped to inactive safe values 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1421 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.3.2.2 Flash Subsystem (FSS)** 

This section describes the Flash Subsystem (FSS) in the device. 

## _**13.3.2.2.1 FSS Overview**_ 

The Flash Subsystem (FSS) provides access to external Flash devices via Octal Serial Peripheral Interface (OSPI) along with Encryption/Decryption, Authentication and in-line ECC protection (referred as ECCM). 

The FSS includes one OSPI. For more information, see _Octal Serial Peripheral Interface (OSPI)_ . 

Table 13-185 shows FSS allocation across device domains. 

## **Table 13-185. FSS Allocation Across Device Domains** 

**==> picture [500 x 39] intentionally omitted <==**

**----- Start of picture text -----**<br>
Domain<br>Instance<br>MAIN<br>FSS0 ✓<br>**----- End of picture text -----**<br>


Figure 13-147 shows the FSS overview. 

**==> picture [464 x 290] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>FSS0<br>CBASS<br>FSAS OSPI0 OSPI0<br>I/O Pins<br>Reset  Reset Signals<br>Controller<br>Interface clock<br>PLL Controller<br>**----- End of picture text -----**<br>


**Figure 13-147. FSS Overview** 

## _**13.3.2.2.1.1 FSS Features**_ 

The FSS module provides the following features: 

- Supports on-the-fly safety, implemented by the ECCM module, which provides SECDED ECC protection to the data path of flash. 

- Supports on-the-fly security, implemented by the OTFA module, which provides encryption/decryption and authentication. 

- OTFA and ECCM modules are independently enabled and work on data path to OSPI target 

1422 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- 4 regions configurable for ECCM and 4 regions configurable for Authentication. 

- Support Execute In Place (XIP) transactions with or without ECCM, Encryption and/or Authentication. XIP here refers to the CPU code execution from flash. Although XIP referred by this feature is a generic term for CPU code execution from flash, the Flash XIP Mode provided by flash device is also preserved regardless of whether ECCM, Encryption and/or Authentication is enabled. 

- All combinations of enabling or bypassing each of the features (ECCM, Authentication, Encryption) are supported for both reads and writes as follows: 

   - Bypass, No authentication, ECCM or address translation 

   - ECCM only 

   - Authentication only 

   - ECCM + Authentication 

- EFUSE input to enable or disable authentication 

- The OTFA module supports Modified-Read. For example, requests that are in an authentication region and have a start address that is not on a 32-byte boundary and/or the size is not multiple of 32-bytes the OTFA will issue a modified read transaction with 32-byte aligned address and a size of 32-byte multiple to ensure that authentication and decryption can be performed. The OTFA module will then return only the requested bytes back on the S0 Data interface. Please refer to OTFA specification section 

- The ECCM module supports Modified-Read. For example, requests that are in an ECCM region and have a start address that is not on a 32-byte boundary and/or the size is not multiple of 32-bytes the ECCM module will issue a modified read transaction with 32-byte aligned address and a size of 32-byte multiple to ensure that ECCM check can be performed. The ECCM module will then return only the requested bytes back on the S0 Data interface. Please refer to ECCM specification section for more information. 

- Writes to ECCM regions (when ECCM is enabled) must be 32-byte aligned and have size that is a 32-byte multiple. An error interrupt will be issued if either of these conditions are not met. 

- Writes outside ECCM regions are not required to be 32-byte aligned nor have a size that is 32-byte multiple. This applies when ECCM is enabled, but the request is outside ECCM region 

- Writes to ECCM regions when ECCM is not enabled are not required to be 32-byte aligned nor have a size that is 32-byte multiple 

- Configurable MAC size of 4, 8, 12, or 16 bytes per 32 bytes of data 

- FSS has a Second ECC S0 interface for ECC on read return data. 

- ECC calculation on read return data is at SOC side interface of OTFA (that is OTFA is NOT protected by ECC). SOC level logic performs ECC checking and error handling. 

- Double pumping for OTFA read path safety. This feature involves sending each read command and read return twice through OTFA and comparing the two commands/returns to detect any permanent or transient faults 

- Error injection support for double pumping diagnostic 

- Only the following OTFA modes are supported - AES_CTR (only encryption, no authentication), GMAC (only authentication, no encryption), GCM (both encryption and authentication), and Disabled (no encryption or authentication; bypass of crypto functions) 

- FOTA HW ENGINE for FOTA implementation 

- Write buffer (for storing one block of FOTA write data) accessible through the config interface. 

- Internal 2KB program memory for FOTA HW ENGINE. 

- Internal 256-byte data memory for FOTA HW ENGINE. 

- FOTA completion interrupt initiated by FOTA HW ENGINE firmware 

- FOTA error interrupt initiated by FOTA HW ENGINE firmware 

- JTAG debug interface for FOTA HW ENGINE (direct export to SOC level logic) 

## _**13.3.2.2.1.2 FSS Not Supported Features**_ 

The following FSS features are not supported: 

- Variable block sizes for ECCM or Authentication. Only 32-byte block size is supported when ECCM or Authentication is enabled. 

- No read-modify-writes for ECCM or Authentication. Must be done by Software in case of non-aligned writes or non-32-byte block size. Although the OTFA module supports writing into encryption-enabled and/or authentication-enabled regions with non-32B-aligned and non- 32B-size writes, and it does so by converting 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1423 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

the Write transaction to a Read-Modify- Write sequence of transactions, the rest of the FSS modules do not support this. The FSS block will generate fsas_ecc_intr_err_pend (level)/ fsas_ecc_intr_err_req (pulse) error interrupt 

- The OSPI DMA peripheral interface is not supported. 

- Please note that OSPI DMA peripheral interface only applies to OSPI INDAC reads and writes. INDAC can be used without this interface. Instead, external (SOC level) DMA can service INDAC using OSPI FIFO fill level register or OSPI watermark interrupt. Please refer to section Indirect Read Transfer process and section Indirect Write Transfer process in OSPI Controller chapter for more information on using INDAC without DMA peripheral controller. 

- Concurrent writes on S0 interface while FOTA HW ENGINE is active is NOT supported. FOTA HW ENGINE has to be held in reset when writes are performed on S0 interface. 

- Concurrent read and write while OTFA is active is NOT supported. OTFA has to be disabled by setting FSAS_OTFA_REGS_CCFG.MASTER_EN_RD to 1’b0 for concurrent read and write. 

- Write to OTFA protected address range (encryption and/or authentication) with address not aligned to 32-byte or byte count not 32-byte multiple is NOT supported. 

- FOTA write (using FOTA HW ENGINE) through OTFA protected address range and/or ECCM protected address range is NOT supported. FOTA write has to use region 3 to bypass OTFA and ECCM regions. 

## _**13.3.2.2.2 FSS Integration**_ 

This section describes the FSS integration in the device, including information about clocks, resets, and hardware requests. 

## _**13.3.2.2.2.1 FSS Integration**_ 

Figure 13-148 shows integration of FSS0. 

**==> picture [439 x 200] intentionally omitted <==**

**----- Start of picture text -----**<br>
FSS0<br>CFG_INTF<br>S0_DATA_INTF<br>FLASH_INTF<br>S0_ECC_INTF<br>JTAG_INTF<br>INTERRUPTS<br>RST_MOD_G_RST_N FSS0_RST (OSPI,FOTA,ECC)<br>ESM_INTF<br>OSPI0_RCLK FSS0_ICLK (OSPI,FOTA,OTFA<br>,ECC)<br>**----- End of picture text -----**<br>


**Figure 13-148. FSS0 Integration** 

## **Table 13-186. FSS0 Clocks** 

|**Module**|**Module Clock Input**|**Source Clock Signal**|**Description**|
|---|---|---|---|
|**Instance**||||
|FSS0|FSS0_ICLK|OSPI0_RCLK_CLK|OSPI0 Clock|
||FSS0_VBUS_CLK|VBUS_CLK|FSS CFG and DATA Clock|



1424 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Table 13-187. FSS0 Resets** 

|**Module Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|FSS0|FSS0_RST|MOD_G_RST|SYS_RST|FSS0 system reset|



## **FSS0 Hardware Requests** 

For more information, see _FSS0_OSPI Interrupt Requests_ 

## **Note** 

For more information on the OSPI Integration, see _OSPI Integration_ . 

## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1425 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.2.3 FSS Functional Description 13.3.2.2.3.1 FSS Detailed Block Diagram**_ 

**==> picture [447 x 243] intentionally omitted <==**

**----- Start of picture text -----**<br>
FSS<br>FSAS<br>Boot<br>S0 Data Interface<br>Seg<br>OTFA ECCM OSPI<br>S0 ECC Interface<br>INTD<br>FOTA Accelerator<br>FSAS<br>MMR<br>Config Interface Config CBASS<br>**----- End of picture text -----**<br>


**Figure 13-149. FSS Detailed Block Diagram** 

The FSS module consists of the following 3 interfaces: 

1. **Data Interface (S0)** : It is 64-bit multi issue data interface with coherent in-band bypass, which has access to OSPI0 and can be configured for ECCM and/or Authentication. 

2. **ECC Interface (ECC_S0)** : It is a 16-bit data interface exported to carry ECC for read return data on S0. This is in sync with S0. Please refer to section Error Correction Code (ECC) and Safety for more details. 

3. **Config Interface** : It is a 32-bit Config interface used for configuration of the memory mapped registers within the FSS through the Config CBASS. The Config CBASS takes configuration access and sends it to the appropriate FSS module. 

The FSS consists of Functional Safety And Security module (FSAS module) , which includes three main FSS engines - Safety engine (ECCM), Security engine (OTFA) and FOTA Accelerator. 

1. **Safety Engine (ECCM)** : FSS provides safety with in-line ECC (on-the-fly), implemented by the ECCM module, and provides SECDED ECC protection to the data path to flash. Inline ECC consists of 4 syndromes per 32-byte chunk. It supports on-the-fly address translation to provide software transparent view to account for additional storage of ECC data bytes. FSS also supports RAM ECC for RAMs present in OSPI and for FOTA HW ENGINE program memory. FSS also supports ECC_S0 interface that is in lockstep with S0 interface and carries ECC associated with read data provided by S0 interface. 

2. **Security Engine (OTFA)** : FSS provides security features with In-line encryption/decryption/Authentication (AES/GCM) on flash data, implemented by the OTFA module, to enable secure external flash use. It supports on-the-fly address translation to provide software transparent view to account for additional storage of MAC (Message Authentication Code). The MAC size is programmable (8/12/16/20 bytes). 

3. **FOTA Accelerator** : FSS provides Firmware Over the Air (FOTA) update feature, implemented by the FOTA Accelerator, which involves writing updated firmware to flash. This is managed by SOC software as it authenticates/validates the updated firmware, sequences the writes to flash and rebooting. The FOTA accelerator supports SOC software in performing FOTA tasks. It is possible to perform concurrent 

1426 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

XIP read(s) while FOTA update happens in background, with minimum XIP downtime and zero software overheads on MCU. 

The various MMR Modules contain the registers for use in the ECCM, OTFA, and other sub-modules inside FSS. The INTD module is used to create pulse interrupts for FSAS ECCM logic and FOTA, to give out the SOC. 

The Boot Segment module is responsible for the address remapping of FSS Region 1, as explained in section FSS Boot Region and Selection. 

## _**13.3.2.2.3.2 FSS Memory Regions**_ 

The FSS provides data transfer to OSPI through a single 64-bit S0 Data Interface, with data passing through ECCM/OTFA modules. The FSS memory space is divided into three distinct regions, each 128MB in size, for accessing flash memory. These regions are classified based on their functional features: 

- Address translation support 

- Boot capability 

- On-the-fly Encryption and Authentication (OTFA) 

- Error Correction Code (ECC) protection 

Each region can be configured independently to enable or disable these features based on system requirements. 

## **All these memory mapped regions map to the same physical location in the flash.** 

**Table 13-188. FSS Memory Regions** 

|**FSS**<br>**Regions**|**SoC Address Range**|**Size**|**Region Features**|**Description**|
|---|---|---|---|---|
|Region 0|0x60000000 - 0x67FFFFFF|128 MB|Supports OTFA + ECC|External Memory Space|
|Region 1|0x80000000 - 0x87FFFFFF|128 MB|Supports OTFA + ECC|Boot Space|
||||Supports Address Remap-ability feature||
|Region 3|0x88000000 - 0x8FFFFFFF|128 MB|NO OTFA + NO ECC|External Memory Space -<br>Bypass Region|



## **Note** 

There is no FSS Region 2. 

1. **FSS Region 0 :** Region 0 supports the following operations: 

   - Execute-In-Place (XIP) 

   - DMA reads 

   - DMA writes 

This region is designed to handle flash or RAM data that requires authentication and/or ECCM protection. It automatically performs address translation to accommodate the additional space needed for ECC and MAC data 

2. **FSS Region 1 :** This region is similar to FSS Region 0, but can select 4KB to 128MB block, defined by the __boot_segment__ and __boot_mask__ registers. See section FSS Boot Region and Selection for details. Both FSS Region 0 and 1 have address translation to make room for the authentication and ECCM words. As mentioned above the main feature of FSS Region 1 that is not present in Region 0 and FSS Region 3 is Address Remapability using __boot_segment__ and __boot_mask__ registers. 

3. **FSS Region 3 :** 

Bypass Region Primary Functions: 

- a. Bypasses both ECC and OTFA processing 

- b. Enables direct flash programming with pre-authenticated and ECCM-protected data 

- c. Supports error correction (scrubbing) operations: Used to scrub ECCM errors in the event that the Flash takes a bit hit. That is to scrub a single bit error in flash, it may be necessary to re-write an entire block 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1427 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

of flash. The FSS reports the untranslated block address; the system will translate the address based on MAC and ECCM modes to locate the real address in Flash or RAM for the scrubbing operation. 

Additional Uses: 

- a. Used for validation of MAC and ECCM block programming 

- b. FOTA (Firmware Over The Air) operations: Used by FOTA HW ENGINE for flash writes in single interface RWW mode. It expects input data to be pre-encrypted and pre-authenticated with ECC and MAC. 

## **Note** 

When using this region, data must be properly formatted with ECC and MAC before writing to flash. 

It is important to note that FSS regions are logical partitions internal to the FSS module and are completely independent from the physical bank/region organization specified in the flash device data sheet. FSS regions just defines the dataflow path to/ from flash. All FSS Regions 0,1,3 map to the same physical location in the flash. The idea behind all 3 different FSS regions pointing to the same flash physical location is so that: 

1. While writing to flash using Region 0 the data will go through the OTFA and ECC path and hence with be Encrypted and Authenticated (padded with MAC and ECC). 

2. While writing to flash using Region 3 the data will go as it is without any Encryption / Authentication. (Bypasses OTFA and ECC) 

3. FSS Region 1 is called boot space region as ROM uses FSS Region 1. If Address remap feature is enabled in MSS-CTRL and is R5F/any other controller throws access to that address range, then the access will be remapped to new location as explained in FSS Boot Region and Selection. 

## **Note** 

128MBytes can be addressed using Address Bits[26:0] -> 27 Bits. Hence the upper 5 address Bits[31:27] are not relevant from perspective of flash/memory device. 

1428 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.2.2.3.2.1 FSS Boot Region and Selection**_ 

The boot placement in the flash is controlled by the below MMRs present in MSS_CTRL: 

1. _MSS_OSPI_BOOT_CONFIG_SEG_BOOT_SEG[19:0]_ - Interface S0 Boot segment selector 

2. _MSS_OSPI_BOOT_CONFIG_MASK_BOOT_MASK[19:0]_ - Interface S0 Boot mask 

For documentation ease, the _MSS_OSPI_BOOT_CONFIG_SEG_BOOT_SEG[19:0]_ will be referred to as __boot_segment_._ and the _MSS_OSPI_BOOT_CONFIG_MASK_BOOT_SIZE [19:0]_ will be referred to as __boot_mask_._ The FSS boot region (Region 1) can be defined as a 4KB through 128MB block. Which 4KB through 128MB region of the 128M Byte is defined by the __boot_segment__ register. These __boot_segment__ bits replace the required number of bits of the 32-bit internal address based on segment size (determined by __boot_mask)_ when reading or writing region 1. The __boot_mask__ determines which bits are replaced. Since minimum boot region granularity is 4KB, the FSS boot region 1 only specifies 20 bits of address, the upper 20 bits of a 32-bit internal address will be derived from the __boot_segment__ and __boot_mask__ registers. The __boot_segment__ will replace the upper 20 bits of the internal address based on segment size derived from __boot_mask__ which will determine the bits to be replaced. 

This allows the boot sector to be placed anywhere within the translated flash space. In addition, this can be used to implement FOTA swap feature which requires CPU address map to remain the same while the firmware in flash is swapped to a different copy. Figure FSS Region 1 Remapping explains this concept in more detail. Typically, when the image binary is created, it is usually linked to load and run from a fixed address. For example, CPU could be executing from firmware A in flash while firmware B is being written (FOTA update). When swap to firmware B is required, SOC can reconfigure __boot_segment__ and __boot_mask__ to point to firmware B in flash while CPU still uses same address map as firmware A. This allows CPU address map to remain the same as previous firmware. 

**==> picture [500 x 328] intentionally omitted <==**

**Figure 13-150. FSS Region 1 Remapping** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1429 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

The maximum memory region allocated for External memory Region in SoC is 128 MBytes. This 128 MBytes is addressable with lower 27 bits [26:0]. Hence the five upper address bits[31:27] are used by SoC to identify that it is FSS Data Region 1. Since the minimum granularity is 4KB the lower 12 address bits is taken as it is and not address translated. The Upper [31:12] address bits aligns to __boot_segment__ and __boot_mask__ bits [19:0]. 

## **Pseudo Code for address remapping** 

- if (boot_mask bit[i] ==1) : Then that address bit is replaced with the corresponding bit in __boot_segment__ 

- if (boot_mask bit[i] == 0) : Then the corresponding address bits are taken as it is ( and not taken from __boot_segment__ bits ) 

Example 1: Assume Image A is Primary Boot Image of size ( <=16MB ) located at 0x8000_0000 and Image B is located at offset of 16MB of flash (0x8100_0000). So in this case any access to 0x8 **0** 00_0000 should be mapped to 0x8 **1** 00_0000 

Hence __boot_segment__ value should be = 0x1000 and __boot_mask__ = 0xFF000 as seen in Figure 13-151 

**==> picture [478 x 203] intentionally omitted <==**

**----- Start of picture text -----**<br>
_boot_segment and _boot_mask   4KB Granularity<br>Unmodified<br>Address Bits 1 0 0 0 0 0 0 0 …. 0 0 0 0 0 0 0 … 0<br>0x80000000<br>31 30 29 28 27 26 25 24 15 14 13 12 11<br>0<br>_boot_mask_ [19:0] 1 1 1 1 1 1 1 1 0 0 ….. 0 0 0 0 0 0 0 0 0 0<br>0xFF000<br>31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12<br>_boot_Segment_[19:0] 1 0 0 0 0 0 0 1 0 0 ….. 0 0 0 0 0 0 0 0 0 0<br>0x01000<br>31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12<br>Remapped Effective  1 0 0 0 0 0 0 1 Bits taken as in Address bits since corresponding boot_mask bits = 0 11 : 0 (4KB Minimum granularity)No change<br>Address =<br>0x81000000 31 30 29 28 27 26 25 24 23 22 ... 12<br>Not Significant from Flash perspectiveRemains same  Bits picked from boot_seg as the corresponding boot_mask bit = 1   No Change<br>**----- End of picture text -----**<br>


**Figure 13-151. Boot_Segment and Boot_Mask Example Configuration** 

Hence any access to address 0x8000_0000 will be remapped to address 0x8100_0000. In other words the image at location 0x8100_0000 ' _before boot_segment & boot_mask configuration_ ' as seen in memory browser will be seen at location 0x8000_0000 ( by ROM / memory browser) ' _after boot_segment & boot_mask configuration_ ' . 

|**Required offset in flash(before**<br>**ECCMaddress translation**|**_boot_mask**|**_boot_segment**|**Effective offset(before ECCM**<br>**address Translation)**|
|---|---|---|---|
|4KB (minimum granularity)|0xFFFFF|0x00001|0x0000_1000|
|8KB|0xFFFFF|0x00002|0x0000_2000|
|128KB|0xFFFE0|0x00020|0x0002_0000|
|64MB|0xFC000|0x04000|0x0400_0000|



Example 2: Consider the scenario where flash total size is 128KB, ECCM is enabled, 16-byte MAC is enabled, and boot segment size (determined by __boot_segment_)_ is 16KB. For this scenario, the highest address the __boot_segment__ can be placed is address 0xFB12. Most time the boot sector will be set to zero, but this is not required. 

1430 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

Care must be taken to account for the address translation as to not fall off or wrap the address of the flash 

## _**13.3.2.2.3.2.2 FSS Safety and Security**_ 

The FSS has Safety and Security which can be configured for Safety and/or Security enabled or disabled. These Safety and Security features manage additional in-band data (ECCM syndromes and MAC) that is added to the user data in the Flash device memory. For each 32 bytes of user data, Safety adds 4 bytes of ECCM and Security adds 4,8,12 or 16 bytes of MAC. If both Safety and Security are enabled, up to 20 bytes of overhead is going to be added to every 32 bytes of user data. 

The FSS manages flash memory access in blocks, with block sizes varying based on enabled features: 

Base Block Size: 32 bytes 

Additional Overhead Requirements: 

1. Safety (ECC) enabled: Adds 4 bytes per 32-byte block for ECCM syndrome data 

2. Security (MAC) enabled: Adds 4, 8, 12, or 16 bytes per 32-byte block (based on programmed MAC size) 

3. Both Safety and Security enabled: Total overhead is 8, 12, 16, or 20 bytes per 32-byte block. Combines ECCM syndrome (4 bytes) and MAC data (4-16 bytes) 

**Important Note:** Once Safety or Security features are enabled, the corresponding space is reserved across all memory regions, regardless of whether individual regions are configured to use these features. The block size returns to 32 bytes only when both Safety and Security features are disabled. 

The FSS HW is responsible for hiding this extra data from SOC. The FSS HW translates the accessed address, strips (on read) or adds (on writes) the necessary extra data 

## _**13.3.2.2.3.2.3 Read Optimizations**_ 

To distinguish between similar read optimization features implemented across different FSS modules, the following definitions are used: 

1. **OSPI DAC Predicted Read feature :** This optimizes read performance by issuing a predicted read if the current reads are complete. Please refer to OSPI Controller section for more information. 

2. **OSPI DAC Read PHY pipeline mode :** This feature is implemented by OSPI Controller to read extra bytes based on Controller configuration at the end of a read from flash. This ensures that chip select is not de-asserted during flash round-trip delay and sample delay associated with PHY DLL. Please refer to section PHY Pipeline Mode for more information. 

3. **FSS XIP Prefetcher :** 

The prefetcher automatically loads the next 32-byte block from flash when specific conditions are met. This feature optimizes XIP performance in two ways: 

- a. Addresses CPU request patterns: CPU XIP requests typically occur at random intervals. Requests are often non-consecutive 

- b. Reduces latency: Proactively fetches the next cache line. Eliminates waiting time for CPU requests. Particularly effective for linear code execution 

For detailed implementation and conditions, refer to the FSS XIP Prefetcher 

4. **ECCM Read Pipeline Mode :** This feature assists in maintaining address continuity to flash by reading MAC and ECCM words even if the request address is not in MAC or ECCM region. In this case, the unused MAC or ECCM words are discarded. This is implemented by the ECCM module since it is responsible for address translation and reserving space in flash for ECCM and MAC. The purpose for this is to ensure OSPI can receive continuous addresses such that it can skip sending command bytes to flash. This feature does not need continuous requests. It will predict that the next consecutive address will be requested and hence is optimizing the current request to maintain address continuity. Please refer to section _ECCM Read Pipelined mode_ for more information. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1431 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.2.3.2.4 FSS XIP Prefetcher**_ 

The FSS includes a prefetcher module optimized for XIP (Execute-In-Place) operations. When no pending requests exist, this module automatically fetches the next sequential block of data. This prefetching mechanism significantly improves performance during linear code execution 

By default, the prefetcher block is enabled, and setting the _disxip_ bit in the SYSCONFIG will disable this feature and any prefetched data will be discarded. Once the pre-fetch starts, it will continue as long as the following request occurs during the pre-fetch burst and the requested address is the same address as the pre-fetched burst address. If the read to the pre-fetch burst occurs after the bus has gone idle, the next burst will not be read. If a different block is read, then pre-fetching stops after current pre-fetch completes and the pre-fetch data is saved into a stack allowing up to 1 burst to be remembered. Any write to a pre-fetched burst address will cause that pre-fetched burst to be purged. If the _disxip_ config bit is set pre-fetching is disabled and any prefetched data is discarded. 

It is recommended to use _disxip_ as a static configuration bit that is selected based on desired mode of operation and not toggled dynamically while reads are active. For example, pulsing _disxip_ high by writing 1 and 0 in quick succession will not guarantee that prefetch buffer is purged. This is because this pulsing can occur while a prefetch read is in progress and _disxip_ may end up being 0 while prefetch buffer is written. This race condition between software _disxip_ pulsing and hardware prefetch buffer write can be avoided by ensuring that _disxip_ is selected for next read phase based on whether prefetching is required for this phase. 

Please note that this is referring to prefetching feature that is useful for linear accesses associated with XIP. This is NOT referring to XIP features implemented in flash Controller or memory device. 

Although this feature has reference to XIP, it is not limited to XIP and is applicable to any reads from flash. However, XIP is used in the name since it is most likely to be used for XIP. Block copy requests are generally provided back-to-back and hence XIP prefetcher logic may not even be activated. 

The prefetcher module also has the ability to turn all read request into 2-bytes aligned (even length) request due to OSPI limitation on DDR mode. In other words, the logic makes the OSPI address and length even and inclusive of the requested bytes. Setting the _ospi_ddr_disable_mode_ bit will disable this feature and pass all read requests unchanged. To use this feature, the _ospi_32b_disable_mode_ bit must be set. 

This module also can take any read and make it a 32-bit read aligned to a 32-bit aligned address for OSPI pipeline modes. Setting the _ospi_32b_disable_mode_ bit will disable this feature and pass all read requests unchanged. This feature has priority over the DDR feature so if both control bits are clear this feature is in operation. 

## _**13.3.2.2.3.2.5 Considerations for OSPI INDAC Read Mode with Address Translation**_ 

The OSPI Controller has an INDAC mode that involves configuration of start address and size for indirect operation. The FSS modules upstream of OSPI perform address translation in certain circumstances. It is important to understand the impact of this address translation on INDAC mode. Please refer section _Memory address translation for memory map calculation_ . Also, please refer _Indirect Read Transfer Number Bytes Register_ in OSPI Controller specification for more information on INDAC configuration. 

1432 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.2.2.4 FSS Programming Guide**_ 

## _**13.3.2.2.4.1 FSS Initialization Sequence**_ 

- Configure the main boot parameters for FSS (see FSS Boot Region and Selection): 

   - Select the boot block to be used. 

   - Select the size of the boot block to be used. 

- Enable FSS 

- Configure the FSS0_OSPI0. 

- Enable the FSS0_OSPI0 . (For more information about OSPI configuration, please see , Octal Serial Peripheral Interface (OSPI) _Octal Serial Peripheral Interface Section )_ . 

## _**13.3.2.2.4.2 Real-time operating requirements**_ 

The CPU or DMA can read any location in the memory map and ECCM, authentication or decryption will occur based on the region selection and size configuration. 

In the event of an ECCM Single Error Detect error, the 32-byte block address and associated error bits are stored and an interrupt is generated if enabled. 

The CPU can then service the interrupt and determine the error type. If a single error occurs, the CPU can scrub the flash block to determine if the error is permanent and requires reprogramming. 

In the event of an ECCM Double Error Detect error, the 32-byte block address and associated error bits are stored and an interrupt is generated if enabled. 

The CPU can then service the interrupt and determine the error type. If the Double error detect is within the flash, the region is corrupt and should not be used. 

For both ECCM Double Error Detect and authentication error, the bus status will also be set. This prevents the CPU from executing the errant data. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1433 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.2.5 Octal Serial Peripheral Interface (OSPI)**_ 

This section describes the Octal Serial Peripheral Interface (OSPI) module for the device. 

**13.3.2.2.5.1 OSPI Overview** ............................................................................................................................1435 **13.3.2.2.5.2 OSPI Environment** ......................................................................................................................1437 **13.3.2.2.5.3 OSPI Integration** ......................................................................................................................... 1440 **13.3.2.2.5.4 OSPI Functional Description** .....................................................................................................1444 **13.3.2.2.5.5 OSPI Programming Guide** ......................................................................................................... 1467 

1434 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.2.2.5.1 OSPI Overview**_ 

The Octal Serial Peripheral Interface (OSPI) module is a kind of Serial Peripheral Interface (SPI) module which allows single, dual, quad or octal read and write access to external flash devices. 

The OSPI module is used to transfer data, either in a memory mapped direct mode (for example a processor wishing to execute code directly from external flash memory), or in an indirect mode where the module is set-up to silently perform some requested operation, signaling its completion via interrupts or status registers. For indirect operations, data is transferred between system memory and external flash memory via an internal SRAM which is loaded for writes and unloaded for reads by a device controller at low latency system speeds. Interrupts or status registers are used to identify the specific times at which this SRAM should be accessed using user programmable configuration registers. 

Figure 13-152 shows the OSPI module overview. 

**==> picture [430 x 385] intentionally omitted <==**

**Figure 13-152. OSPI Overview** 

## _**13.3.2.2.5.1.1 OSPI Features**_ 

The OSPI module has the following features: 

- Support for single, dual, quad (QSPI mode) or octal I/O instructions. 

- Supports dual Quad-SPI mode for fast boot applications. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1435 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- Memory mapped ‘direct’ mode of operation for performing flash data transfers and executing code from flash memory. 

- Software triggered 'indirect' mode of operation for performing low latency and non-processor intensive flash data transfers. 

- Local SRAM of configurable size to reduce Advanced High-Performance Bus (AHB) overhead and buffer flash data during indirect transfers. 

- Set of software advanced peripheral bus accessible flash control registers to perform any flash command, including data transfers up to 8-bytes at a time. 

- Additional addressable memory bank to accommodate more than 8-bytes at a time. 

- Support for DDR Mode and DTR protocol (including Octal DDR protocol with DQS for Octal-SPI devices) 

- • Programmable device sizes. 

- Programmable write protected regions to block system writes from taking effect. 

- Programmable delays between transactions. 

- Legacy mode allowing software direct access to low level transmit and receive FIFOs, bypassing the higher layer processes. 

- An independent reference clock to decouple bus clock from SPI clock – allows slow system clocks. 

- Programmable baud rate generator to generate OSPI clocks. 

- Features included to improve high speed read data capture mechanism. 

- Option to use adapted clocks or DQS to further improve read data capturing. 

- Programmable interrupt generation. 

- Up to two external device selects - OSPI and QSPI devices can be mixed 

- Programmable data decoder, enables continuous addressing mode for each of the connected devices and auto-detection of boundaries between devices. 

- Full integration with PHY module dedicated to more flexible and power efficient transfers. 

- Supports RESET_OUT[1-0] and ECC_FAIL pins for external flash devices where ECC is checked on the flash. 

- Automatic Flash device status polling for programming operation (Auto HW Polling) 

## _**13.3.2.2.5.1.2 OSPI Not Supported Features**_ 

The following features are not supported on this family of devices: 

- DMA not supported 

- Pulse events not used. 

- In Octal-SPI and Quad-SPI mode, Mode 1, 2 are not supported. 

1436 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.2.2.5.2 OSPI Environment**_ 

The FSS0_OSPI0 module is hereinafter referred to as OSPI module. 

This section describes the OSPI external connections (environment). 

The OSPI module is primarily intended for fast booting from Octal- and Quad-SPI flash memories. Figure 13-153 shows a typical connection of the OSPI module to an external Octal-SPI flash memory. 

**==> picture [372 x 313] intentionally omitted <==**

**Figure 13-153. OSPI Connected to an External Octal-SPI Flash Memory** 

Table 13-189 lists and describes the FSS0_OSPI I/O signals. 

**Table 13-189. OSPI I/O Signals** 

|**Module Pin**|**Device Level Signal**|**I/O**(1)|**Description**|**Module Pin**|
|---|---|---|---|---|
|||||**Reset Value**(2)|
||||**FSS0_OSPI0**||
|DQ0|OSPI0_D0|IO|FSS0_OSPI0 data input/output 0|HiZ|
|DQ1|OSPI0_D1|IO|FSS0_OSPI0 data input/output 1|HiZ|
|DQ2|OSPI0_D2|IO|FSS0_OSPI0 data input/output 2|HiZ|
|DQ3|OSPI0_D3|IO|FSS0_OSPI0 data input/output 3|HiZ|
|DQ4|OSPI0_D4|IO|FSS0_OSPI0 data input/output 4|HiZ|
|DQ5|OSPI0_D5|IO|FSS0_OSPI0 data input/output 5|HiZ|
|DQ6|OSPI0_D6|IO|FSS0_OSPI0 data input/output 6|HiZ|
|DQ7|OSPI0_D7|IO|FSS0_OSPI0 data input/output 7|HiZ|
|N_SS_OUT0|OSPI0_CSn0|O|FSS0_OSPI0 external flash device chip select 0|0x1|
|N_SS_OUT1|OSPI0_CSn1|O|FSS0_OSPI0 external flash device chip select 1|0x1|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1437 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-189. OSPI I/O Signals (continued)** 

|**Module Pin**|**Device Level Signal**<br>**I/O**(1)<br>**Description**<br>**Module Pin**<br>**Reset Value**(2)|
|---|---|
|OCLK<br>ICLK<br>DQS|OSPI0_CLK<br>O<br>FSS0_OSPI0 clock output for the external flash device<br>0x0|
||OSPI0_LBCLKO<br>O<br>FSS0_OSPI0 external loopback output<br>0x0|
||NA<br>I<br>FSS_OSPI0 ICLK (Internal Loopback clock)<br>NA|
||OSPI0_DQS<br>I(3)<br>FSS0_OSPI0 data strobe / external loopback input<br>Don't care|
|RESET_OUT0|OSPI0_RESET_OUT0<br>O<br>FSS0_OSPI0 reset output 0 for the external flash device.<br>Pin is active low.<br>0x1|
|RESET_OUT1|OSPI0_RESET_OUT1<br>O<br>FSS0_OSPI0 reset output 1 for the external flash device.<br>Pin is active low.<br>0x1|
|ECC_FAIL|OSPI0_ECC_FAIL<br>I<br>FSS0_OSPI0 ECC status from the external flash device<br>0x1|



(1) I = Input; O = Output 

(2) HiZ = High Impedance 

(3) When used as an external loopback input, the DQS signal can alternatively be referred to as LBCLKI. The LBCLKI clock input signal is a looped back version of the LBCLKO clock output signal and facilitates easier timing closure at higher speeds. The loopback has to be at board level in order to support higher OSPI speeds. The source of the loopback clock is defined by MSS_OSPI_CONFIG[6:4] MSS_OSPI_CONFIG_ICLK_SEL bits in _MSS_CTRL_ . 

Table 13-190 describes the OSPI I/O connectivity to external SPI devices. 

**Table 13-190. OSPI I/O Connectivity to External SPI Devices** 

|||**Description**|
|---|---|---|
|**Module**<br>**Pin**|**I/O**(1)|**4-pin**(1)**SPI - Single**<br>**Read/Write (SIO)**<br>**(DATA_XFER_TYPE_E**<br>**XT_MODE_FLD=0x0)**<br>**4-pin**(1)**SPI - Dual Read/**<br>**Write**<br>**(DATA_XFER_TYPE_EXT_**<br>**MODE_FLD=0x1)**<br>**6-pin**(1)**SPI - Quad Read/**<br>**Write**<br>**(DATA_XFER_TYPE_EXT_**<br>**MODE_FLD=0x2)**<br>**11-pin**(1)**SPI - Octal Read/**<br>**Write**<br>**(DATA_XFER_TYPE_EXT_**<br>**MODE_FLD=0x3)**|
|DQ0<br>IO||Used as SPI data output<br>Used as SPI data input 0<br>Used as SPI data output 0<br>Used as SPI data input 0<br>Used as SPI data output 0<br>Used as SPI data input 0<br>Used as SPI data output 0|
|DQ1<br>IO||Used as SPI data input<br>Used as SPI data input 1<br>Used as SPI data output 1<br>Used as SPI data input 1<br>Used as SPI data output 1<br>Used as SPI data input 1<br>Used as SPI data output 1|
|DQ2<br>IO||Not used<br>Not used<br>Used as SPI data input 2<br>Used as SPI data output 2<br>Used as SPI data input 2<br>Used as SPI data output 2|
|DQ3<br>IO||Not used<br>Not used<br>Used as SPI data input 3<br>Used as SPI data output 3<br>Used as SPI data input 3<br>Used as SPI data output 3|
|DQ4<br>IO||Not used<br>Not used<br>Not used<br>Used as SPI data input 4<br>Used as SPI data output 4|
|DQ5<br>IO||Not used<br>Not used<br>Not used<br>Used as SPI data input 5<br>Used as SPI data output 5|
|DQ6<br>IO||Not used<br>Not used<br>Not used<br>Used as SPI data input 6<br>Used as SPI data output 6|
|DQ7<br>IO||Not used<br>Not used<br>Not used<br>Used as SPI data input 7<br>Used as SPI data output 7|
|DQS<br>I||Not used<br>Not used<br>Not used<br>Data strobe or loopback<br>clock input|
|OCLK<br>O||Output clock or loopback clock output. For more information, seeTable 13-189.|
|N_SS_OUT0<br>O||External SPI device chip-select 0|
|N_SS_OUT1<br>O||External SPI device chip-select 1|
|RESET_OUT0<br>O||External SPI device reset 0. Pin is active low.|
|RESET_OUT1<br>O||External SPI device reset 1. Pin is active low.|
|ECC_FAIL<br>I||External SPI device ECC failure indication|



(1) This is the pin count at the external SPI flash memory side. 

1438 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

For OSPI0_CLK, OSPI0_LBCLKO, and OSPI0_DQS signals to work properly, the RXACTIVE bit of the appropriate registers should be set to 0x1 because of retiming purposes. 

## **Note** 

For more information about device level signals (pull-up/down resistors, buffer type, multiplexing and others), see tables _Pin Attributes_ and _Pin Multiplexing_ in the device-specific Data sheet. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1439 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.2.5.3 OSPI Integration**_ 

This section describes module integration in the device, including information about clocks, resets, and hardware requests. 

## _**13.3.2.2.5.3.1 OSPI Integration**_ 

There is 1x OSPI module integrated in the device. The diagram below provides a visual representation of the device integration details. 

1440 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

Device 

**==> picture [415 x 461] intentionally omitted <==**

**----- Start of picture text -----**<br>
FSS0_OSPI0<br>AHB_INTF<br>APB_INTF<br>OSPI0_HCLK<br>OSPI0_PCLK<br>FLASH_INTF<br>SYS_CLK<br>EXT_REFCLK<br>WUCPUCLK<br>DPLL_PER_HSDIV0_CLKOUT1<br>OSPI0_RCLK<br>DPLL_CORE_HSDIV0_CLKOUT0<br>RCCLK10M<br>DPLL_CORE_HSDIV0_CLKOUT3<br>DPLL_PER_HSDIV0_CLKOUT2<br>OSPI_CLK_GCM_CLKSRC_SEL<br>EDMA<br>OSPI_INTR FSS0_OSPI0_LVL_INTR<br>R5FSS0_CORE0/1<br>OSPI_LVL_INTR<br>ESM0<br>  ESM0_LVL_EVENT_39 FSS0_OSPI0_ECC_CORR_LVL_INTR<br>  ESM0_LVL_EVENT_40                   FSS0_OSPI0_ECC_UNCORR_LVL_INTR<br>FSS0_OSPI0_RST<br>**----- End of picture text -----**<br>


**Figure 13-154. OSPI Integration Diagram** 

The tables below summarize the device integration details of OSPI. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1441 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-191.** _**OSPI**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Module Instance**||**Device Allocation**|**Device Allocation**|**SoC Interconnect**|**SoC Interconnect**|
|---|---|---|---|---|---|---|
|OSPI0|||✓||CORE VBUSM Interconnect||
||||**Table 13-192. FSS0_OSPI Clocks**||||
|**Module Instance **|**Module Clock Input**||**Source Clock Signal**<br>**Source**<br>**Description**||||
|FSS0_OSPI0|OSPI0_HCLK||SYS_CLK|SYS_CLK||FSS0_OSPI0 data transfer clock|
||OSPI0_PCLK||SYS_CLK|SYS_CLK||FSS0_OSPI0 configuration clock|
||OSPI0_RCLK||OSPI_CLK|WUCPUCLK||FSS0_OSPI0 Reference clock.<br>Mux controlled by<br>_MSS_RCM:OSPI0_CLK_SRC_SEL_|
||||EXT_REFCLK|EXT_REFCLK|||
||||SYS_CLK|SYS_CLK|||
||||DPLL_PER_HSDIV0_C<br>LKOUT1|PLL_PER_CLK:HSDIV0<br>_CLKOUT1|||
||||DPLL_CORE_HSDIV0_<br>CLKOUT0|PLL_CORE_CLK:HSDIV<br>0_CLKOUT0|||
||||RCCLK10M|Internal 10 MHz RC<br>Oscillator (RCCLK10M)|||
||||DPLL_CORE_HSDIV0_<br>CLKOUT3|PLL_CORE_CLK:HSDIV<br>0_CLKOUT3|||
||||DPLL_PER_HSDIV0_C<br>LKOUT2|PLL_PER_CLK:HSDIV0<br>_CLKOUT2|||



## **Table 13-193. FSS0_OSPI Resets** 

|**Module Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|FSS0_OSPI0|FSS0_OSPI0_RST|MOD_G_RST|POR|FSS0_OSPI0 reset|



## **Table 13-194. FSS0_OSPI Interrupt Requests** 

|**Module**<br>**Instance**|**Module Interrupt Signal**<br>**Destination Interrupt Input**|**Destination**<br>**Description**<br>**Type**|
|---|---|---|
|FSS0_OSPI0|OPTI_FLASH_OSPI0_LVL_INTR<br>OSPI0_LVL_INTR<br>OPTI_FLASH_OSPI0_ECC_COR<br>R_LVL_INTR<br>ESM0_LVL_EVENT_39|All R5FSS Cores<br>ICSSM Core<br>FSS0_OSPI0 interrupt<br>Level|
|||OPTI_FLASH<br>FSS0_OSPI0 ECC<br>Aggregator correctable<br>error interrupt<br>Level|
||OPTI_FLASH_OSPI0_ECC_UNC<br>ORR_LVL_INTR<br>ESM0_LVL_EVENT_40|OPTI_FLASH<br>FSS0_OSPI0<br>ECC Aggregator<br>uncorrectable error<br>interrupt<br>Level|



**Table 13-195.** _**OSPI**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|OSPI0|OPTI_FLASH|OSPI_INTR|OPTI_FLASH_OSPI0_<br>LVL_INTR|Pulse|OSPI0 DMA Event Request|



1442 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1443 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.2.5.4 OSPI Functional Description**_ 

## _**13.3.2.2.5.4.1 OSPI Block Diagram**_ 

Figure 13-155 shows the OSPI module block diagram. 

**==> picture [499 x 310] intentionally omitted <==**

**----- Start of picture text -----**<br>
OSPI module<br>OSPI controller Low level SPI protocol<br>controller<br>SRAM controller TX<br>FIFO SPI Octal-SPI<br>Serialization flash device<br>Control<br>Indirect accesscontroller RX Logic<br>(INDAC) FIFO<br>Data Data Flash<br>interface slave command<br>controller generator<br>Register<br>Direct access Optional host reference<br>interface<br>controller clock interface<br>(DAC)<br>PHY module<br>protectionBoot interfaceRegister Register PHY data<br>interface transmitter<br>Config PHY clock PHY data<br>interface arbiter receiver<br>Config slave<br>controller<br>TX delay line RX delay line<br>ospi-004<br>**----- End of picture text -----**<br>


## **Figure 13-155. OSPI Block Diagram** 

The OSPI module is composed of three main blocks. The first one is the OSPI controller, the second one is the low level SPI protocol controller, and the third one is the integrated PHY. 

The OSPI module has the following two target interfaces: 

- Data target interface intended for data transfer. 

- Configuration target interface intended for accessing the programmable set of registers. 

## _**13.3.2.2.5.4.1.1 Data Target Interface**_ 

The data interface is used for data transfer to external flash devices in direct and indirect mode of operation. The data target controller validates incoming data accesses, responds to invalid requests, performs any required byte and half-word reordering, blocks writes that violate the programmed write protection rules (only for direct access) and forwards the transfer request to either the direct access controller (DAC) or the indirect access controller (INDAC). 

The data interface bus is 32-bits wide. Therefore only byte, half-word and word accesses are permitted. When the controller is configured to work in SPI Octal DDR Mode or Octal DDR Protocol (where 2 bytes are collected within single SPI clock cycle what exceeds the size of 1 byte transfer request), 8 bit transfer size is not allowed. 

1444 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

Cache line wrap accesses over the data target port can be word aligned. 

Data target port doesn't support cache line wrap bursts of 128 bytes. 

## _**13.3.2.2.5.4.1.2 Configuration Target Interface**_ 

The configuration interface is used to configure the OSPI module and perform software controlled flash accesses using the OSPI_FLASH_CMD_CTRL_REG register (for more information refer to Section 13.3.2.2.5.4.11, _Software Triggered Instruction Generator (STIG)_ ). Depending on the address it routes the incoming interconnect transfer to the Low level SPI protocol controller or to the ECC aggregator. The configuration port is also used to interact with the OSPI configuration and SRAM ECC registers. 

## **Note** 

The configuration interface supports only 32-bit accesses. For single byte or half-word manipulations software should perform read-modify-write operations. 

## _**13.3.2.2.5.4.1.3 OSPI Clock Domains**_ 

The OSPI module has two main clock sources for the Octal-SPI controller. 

- For interface clocks 

- For reference clock 

The source for the interface clocks corresponds to the configuration and data buses. The data bus clock (OSPI_HCLK) is the main system clock used to transfer data over the data bus between a controller on the system interconnect and the OSPI module. The data bus clock also drives the internal OSPI SRAM. The configuration bus clock (OSPI_PCLK) is used to access the OSPI configuration register and perform basic configuration and for interrupt handling. The OSPI reference clock (OSPI_RCLK) drives the SPI transmit and receive logic in the OSPI module. It is also used to generate the output SPI protocol clock (OSPI_OCLK) and for oversampling of the input data. Using the reference clock (OSPI_RCLK) allows the OSPI module to decouple the frequency of the SPI flash device from the device system clocks, thereby providing more flexible clocking solution. 

## **Note** 

There is no particular clock ratio requirement between configuration (OSPI_PCLK) and data bus (OSPI_HCLK) clocks. 

## _**13.3.2.2.5.4.2 OSPI Modes**_ 

## **Note** 

Some of the OSPI features described in this section may not be supported on this family of devices. For more information, see , _OSPI Not Supported Features_ . 

The OSPI module supports four SPI modes. These modes are defined through the OSPI_CONFIG_REG[1] SEL_CLK_POL_FLD and OSPI_CONFIG_REG[2] SEL_CLK_PHASE_FLD bits. The SEL_CLK_POL_FLD bit defines the clock polarity and the SEL_CLK_PHASE_FLD bit defines the data launch and data capture relation to the OSPI clock edges. Table 13-196 gives a brief description of these modes. 

**Table 13-196. OSPI Modes** 

|**SPI Mode**<br>**SEL_CLK_POL_FLD**<br>**SEL_CLK_PHASE_FLD**|**Description**|
|---|---|
|0<br>0<br>0|Clock inactive state: low|
||Data launch edge: clock falling edge|
||Data capture edge: clock rising edge|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1445 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-196. OSPI Modes (continued)** 

|**SPI Mode**<br>**SEL_CLK_POL_FLD**<br>**SEL_CLK_PHASE_FLD**|**Description**|
|---|---|
|1<br>0<br>1|Clock inactive state: low|
||Data launch edge: clock rising edge|
||Data capture edge: clock falling edge|
|2<br>1<br>0|Clock inactive state: high|
||Data launch edge: clock rising edge|
||Data capture edge: clock falling edge|
|3<br>1<br>1|Clock inactive state: high|
||Data launch edge: clock falling edge|
||Data capture edge: clock rising edge|



Octal flash devices provide DQS signal which allows source synchronous capture, but for Quad flash devices the OSPI module has a loopback mode. In this loopback mode the clock, looped back at board level, is used for registering the input data, and the edge used is same as the launch edge, thus giving a full cycle path (for more information, see Section 13.3.2.2.5.4.2.1, _Read Data Capture_ ). 

## _**13.3.2.2.5.4.2.1 Read Data Capture**_ 

Figure 13-156 shows the Read Data Capture Logic in the OSPI module. 

**==> picture [500 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
OSPI Flash Controller<br>OSPI_RCLK OSPI_OCLK<br>Divider Clock input<br>OSPI_ICLK<br>OSPI_RD_DATA_CAPTURE_REG<br>Tap [4-1] DELAY_FLD<br>OSPI_DQS<br>generator DQS<br>PHY module<br>. . . Octal flash<br>OSPI_DEV_INSTR_RD_ device<br>CONFIG_REG[13-12] ADDR_<br>XFER_TYPE_STD_MODE_FLD To RX FIFO<br>OSPI_RCLK<br>OSPI_DQ[7-0]<br>Shift Data<br>Register<br>OSPI_RCLK<br>To RX FIFO<br>loopback enable<br>(OSPI_RD_DATA_CAPTURE_REG[0]<br>BYPASS_FLD) clock edge<br>(OSPI_RD_DATA_CAPTURE_REG[5]<br>SAMPLE_EDGE_SEL_FLD)<br>ospi-005<br>**----- End of picture text -----**<br>


**Figure 13-156. Read Data Capture Logic** 

The PHY module includes a DLL which allows adjustment of the sampling edge with respect to the incoming data to achieve maximum frequency. There are three sources for the sampling signal: 

- The reference clock 

- Output SPI clock external loopback 

- The DQS (only available in Octal Flash devices) 

1446 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

The loopback mode (only for Quad flash devices) can work in two cases. The first one is when OSPI_CONFIG_REG[2] SEL_CLK_PHASE_FLD=0. When SEL_CLK_PHASE_FLD=1 there aren’t enough clock falling edges for the register pipeline to catch the last data driven, thus causing a functional failure. Additionally, since the capture edge is falling edge, it gives a full cycle input path only in SPI mode 0, that is when SEL_CLK_POL_FLD=0 and SEL_CLK_PHASE_FLD=0. Thus SPI mode 0 is the first of two modes that support high MHz operation (greater than 50 MHz). The second mode is when SEL_CLK_PHASE_FLD=1 and SEL_CLK_PHASE_FLD=1 (SPI mode 3). In this case the missing clock falling edge is compensated inside the OSPI controller when using the incorporated PHY module by inverting the loopback clock. 

The loopback mode is enabled by writing 0x0 to OSPI_RD_DATA_CAPTURE_REG[0] BYPASS_FLD. The taps are selected by programming OSPI_RD_DATA_CAPTURE_REG[4-1] DELAY_FLD field. The taps delay the read data capturing logic by the programmed number of OSPI_RCLK cycles. 

## _**13.3.2.2.5.4.2.1.1 Mechanisms of Data Capturing**_ 

There are two mechanisms of data capturing in the OSPI module. They can be combined in some parts to ensure reliable sampling solution independent on the system requirements and the controller configuration. The mechanisms are as follows: 

- Data capturing mechanism using taps 

- Data capturing mechanism using PHY module. 

## _**13.3.2.2.5.4.2.1.2 Data Capturing Mechanism Using Taps**_ 

This section describes the data capturing mechanism where sampling point is adjusted for one of the reference clock edges inside divided OSPI clock. 

After POR, the adapted loopback clock circuit and the OSPI_RCLK delay register line both wake in a disabled state. The OSPI_RD_DATA_CAPTURE_REG register provides the control for the mechanism using taps. 

OSPI_RD_DATA_CAPTURE_REG[5] SAMPLE_EDGE_SEL_FLD bit selects the edge of the reference clock, on which data outputs from flash memory are sampled. 

OSPI_RD_DATA_CAPTURE_REG[4-1] DELAY_FLD bit field controls the additional number of read data capture cycles (this is the fast reference clock, running at least x4 of the device clock) that should be applied to the internal read data capture circuit. The large clock-to-out delay of the flash memory together with trace delays as well as other device delays may impose a maximum flash clock frequency which is less than the flash memory device itself can operate at. To compensate, software shall set this register to a value that guarantees robust data captures. 

## _**13.3.2.2.5.4.2.1.3 Data Capturing Mechanism Using PHY Module**_ 

PHY module is responsible for data capturing. More detailed description of all internal PHY sampling mechanisms is included in Section 13.3.2.2.5.4.16.2, _Read Data Capturing by the PHY Module_ . 

## _**13.3.2.2.5.4.2.1.4 External Pull Down on DQS**_ 

Per the OSPI protocol, the FLASH device drives DQS while CS is asserted. When CS is not asserted the FLASH device presents HiZ on DQS. When configured to use DQS, the controller uses the DQS as a clock, which samples the incoming data into a FIFO. Noise on the DQS when it is HiZ can cause spurious false triggering of the FIFO and filling it with invalid data. There is no way to clear this data except to reset the OSPI module. 

To avoid this issue, it is recommended to add a pull down on the DQS line. 

During device wakeup, before the IO ring is configured properly, the CS to the FLASH device is HiZ. Depending on the actual level of the CS line the FLASH device might drive the DQS High, Low or HiZ. A pull down on DQS forces the DQS input to Low, but the DQS might still be High or in the presence of noise there might be transitions between Low and High. This again can cause the same issue of capturing garbage data in the Controller FIFO. 

To avoid this issue it is recommended to release the OSPI from reset only after the IO ring is configured properly. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1447 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.2.5.4.3 OSPI Power Management**_ 

## **Note** 

The OSPI module does not provide any hardware signal for busy or idle status. Software need to ensure that the OSPI module is idle before clocks can be shut off by reading the OSPI_CONFIG_REG[31] IDLE_FLD bit. 

OSPI_PCLK and OSPI_HCLK share the same clock stop request/acknowledge and clock enable/acknowledge interface. 

## _**13.3.2.2.5.4.4 Auto HW Polling**_ 

The OSPI controller is capable of automatically testing the Flash device busy bit to guarantee no reads or writes are ignored by the flash when it is busy burning in programmed data. 

At the end of a programming transaction, the Flash device goes into a burn-in state and becomes busy. 

When Auto HW Polling is enabled, the OSPI controller keeps track of programming transactions and will initiate a Flash status read polling transactions automatically, until Flash indicates it is not busy, before any additional data read or programming operations are sent to the flash device. See OSPI_WRITE_COMPLETION_CTRL_REG register and the associated registers. 

The OSPI controller requires that the OSPI_WRITE_COMPLETION_CTRL_REG[23-16] POLL_COUNT_FLD field should always be set with values greater or equal to 3 (>=3). 

## _**13.3.2.2.5.4.5 Flash Reset**_ 

OSPI provides Flash reset out ports. These ports are active low and controlled though OSPI_CONFIG_REG register. 

## _**13.3.2.2.5.4.6 OSPI Memory Regions**_ 

OSPI Memory Map shows the OSPI memory map in domain. 

## **Note** 

For more information about the memory space, see _FSS Memory Regions_ . 

1448 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.2.2.5.4.7 OSPI Interrupt Requests**_ 

The OSPI module generates three interrupts. The ECC interrupts (FSS0_OSPI_0_OSPI_ECC_CORR_LVL_INTR_0 and FSS0_OSPI_0_OSPI_ECC_UNCORR_LVL_INTR_0) are generated by the OSPI ECC aggregator. 

The other interrupt (FSS0_OSPI_0_OSPI_LVL_INTR_0) is generated by the OSPI module. 

Table 13-197 lists the event flags and the corresponding mask bits of the sources which can cause interrupts. 

**Table 13-197. OSPI Events** 

|**Event Flag**|**Event Mask**|**Description**|
|---|---|---|
|OSPI_IRQ_STATUS_REG[0]|OSPI_IRQ_MASK_REG[0]|Event Flag and Event Mask for|
|MODE_M_FAIL_FLD|MODE_M_FAIL_MASK_FLD|the OSPI Interrupts.|
|OSPI_IRQ_STATUS_REG[1]|OSPI_IRQ_MASK_REG[1]||
|UNDERFLOW_DET_FLD|UNDERFLOW_DET_MASK_FLD||
|OSPI_IRQ_STATUS_REG[2]|OSPI_IRQ_MASK_REG[2]||
|INDIRECT_OP_DONE_FLD|INDIRECT_OP_DONE_MASK_FLD||
|OSPI_IRQ_STATUS_REG[3]|OSPI_IRQ_MASK_REG[3]||
|INDIRECT_READ_REJECT_FLD|INDIRECT_READ_REJECT_MASK_FLD||
|OSPI_IRQ_STATUS_REG[4]|OSPI_IRQ_MASK_REG[4]||
|PROT_WR_ATTEMPT_FLD|PROT_WR_ATTEMPT_MASK_FLD||
|OSPI_IRQ_STATUS_REG[5]|OSPI_IRQ_MASK_REG[5]||
|ILLEGAL_ACCESS_DET_FLD|ILLEGAL_ACCESS_DET_MASK_FLD||
|OSPI_IRQ_STATUS_REG[6]|OSPI_IRQ_MASK_REG[6]||
|INDIRECT_XFER_LEVEL_BREACH_FLD|INDIRECT_XFER_LEVEL_BREACH_MASK_FLD||
|OSPI_IRQ_STATUS_REG[7]|OSPI_IRQ_MASK_REG[7]||
|RECV_OVERFLOW_FLD|RECV_OVERFLOW_MASK_FLD||
|OSPI_IRQ_STATUS_REG[8]|OSPI_IRQ_MASK_REG[8]||
|TX_FIFO_NOT_FULL_FLD|TX_FIFO_NOT_FULL_MASK_FLD||
|OSPI_IRQ_STATUS_REG[9]|OSPI_IRQ_MASK_REG[9]||
|TX_FIFO_FULL_FLD|TX_FIFO_FULL_MASK_FLD||
|OSPI_IRQ_STATUS_REG[10]|OSPI_IRQ_MASK_REG[10]||
|RX_FIFO_NOT_EMPTY_FLD|RX_FIFO_NOT_EMPTY_MASK_FLD||
|OSPI_IRQ_STATUS_REG[11]|OSPI_IRQ_MASK_REG[11]||
|RX_FIFO_FULL_FLD|RX_FIFO_FULL_MASK_FLD||
|OSPI_IRQ_STATUS_REG[12]|OSPI_IRQ_MASK_REG[12]||
|INDRD_SRAM_FULL_FLD|INDRD_SRAM_FULL_MASK_FLD||
|OSPI_IRQ_STATUS_REG[13]|OSPI_IRQ_MASK_REG[13]||
|POLL_EXP_INT_FLD|POLL_EXP_INT_MASK_FLD||
|OSPI_IRQ_STATUS_REG[14]|OSPI_IRQ_MASK_REG[14]||
|STIG_REQ_INT_FLD|STIG_REQ_MASK_FLD||
|OSPI_IRQ_STATUS_REG[16]|OSPI_IRQ_MASK_REG[16]||
|RX_CRC_DATA_ERR_FLD|RX_CRC_DATA_ERR_MASK_FLD||
|OSPI_IRQ_STATUS_REG[17]|OSPI_IRQ_MASK_REG[17]||
|RX_CRC_DATA_VAL_FLD|RX_CRC_DATA_VAL_MASK_FLD||
|OSPI_IRQ_STATUS_REG[18]|OSPI_IRQ_MASK_REG[18]||
|TX_CRC_CHUNK_BRK_FLD|TX_CRC_CHUNK_BRK_MASK_FLD||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1449 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-197. OSPI Events (continued)** 

|**Event Flag**|**Event Mask**|**Description**|
|---|---|---|
|OSPI_IRQ_STATUS_REG[19]|OSPI_IRQ_MASK_REG[19]||
|ECC_FAIL_FLD|ECC_FAIL_MASK_FLD||
|OSPI_ECC_SEC_STATUS_REG0[0]|OSPI_ECC_SEC_ENABLE_SET_REG0[0]|Event Flag and Event Mask for|
|SRAM_PEND|SRAM_ENABLE_SET|the ECC Interrupts.|
||OSPI_ECC_SEC_ENABLE_CLR_REG0[0]||
||SRAM_ENABLE_CLR||
|OSPI_ECC_DED_STATUS_REG0[0]|OSPI_ECC_DED_ENABLE_SET_REG0[0]||
|SRAM_PEND|SRAM_ENABLE_SET||
||OSPI_ECC_DED_ENABLE_CLR_REG0[0]||
||SRAM_ENABLE_CLR||
|OSPI_ECC_AGGR_STATUS_SET[1-0]|OSPI_ECC_AGGR_ENABLE_SET[0]||
|PARITY|PARITY||
|OSPI_ECC_AGGR_STATUS_SET[3-2]|OSPI_ECC_AGGR_ENABLE_SET[1]||
|TIMEOUT|TIMEOUT||
|OSPI_ECC_AGGR_STATUS_CLR[1-0]|OSPI_ECC_AGGR_ENABLE_CLR[0]||
|PARITY|PARITY||
|OSPI_ECC_AGGR_STATUS_CLR[3-2]|OSPI_ECC_AGGR_ENABLE_CLR[1]||
|TIMEOUT|TIMEOUT||



## _**13.3.2.2.5.4.8 OSPI Data Interface**_ 

## _**13.3.2.2.5.4.8.1 Data Interface Address Remapping**_ 

The incoming data interface address, by default, maps directly to the address sent serially to the FLASH device. If the FLASH device has a 24-bit address, then the 24 LSB's of the data address is forwarded. A remap feature is available to remap all incoming data addresses to ADDRESS + N, where N is the value stored in the OSPI_REMAP_ADDR_REG[31-0] VALUE_FLD bit field. It is enabled via the OSPI_CONFIG_REG[16] ENB_AHB_ADDR_REMAP_FLD bit. This feature could be used when software needs to move boot code to another FLASH region. 

## _**13.3.2.2.5.4.8.2 Write Protection**_ 

In order to protect the FLASH device, a software controlled write protection feature is supported. Any data write detected (by using DAC), pointing to an area of the FLASH that is protected, is not permitted. 

A programmable region of the FLASH device, defined as a number of FLASH 'blocks' starting from a particular block number can be protected. Three programmable registers are provided. The first OSPI_LOWER_WR_PROT_REG register defines the FLASH block that is located at the bottom of the region to be protected. The second OSPI_UPPER_WR_PROT_REG register defines the FLASH block that is located at the top of the region to be protected. The third OSPI_WR_PROT_CTRL_REG register is a control register consisting of 2 bits. The OSPI_WR_PROT_CTRL_REG[0] INV_FLD bit allows software to invert the region that is being protected, causing the programmed region to become the only areas of FLASH memory that is not protected from writes. The OSPI_WR_PROT_CTRL_REG[1] ENB_FLD bit is the write protection enable bit. When this bit is set to 0, the FLASH device is unprotected. 

For implementation, the data interface must map the incoming address into its associated FLASH block. A block can be between 1 and 65 KB, programmed via the OSPI_DEV_SIZE_CONFIG_REG register. 

## _**13.3.2.2.5.4.8.3 Access Forwarding**_ 

For legal accesses, the data interface will forward all accesses to one of two access controllers - the direct access and the indirect access controllers. Assuming DAC has been enabled via the OSPI_CONFIG_REG[7] ENB_DIR_ACC_CTRL_FLD bit, then by default all accesses will be forwarded to this controller. Before any accesses can be forwarded to INDAC, it must first be configured by software. This process is fully explained 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1450 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

in Section 13.3.2.2.5.4.10, _Indirect Controller (INDAC)_ . If DAC is disabled, any incoming access that cannot be forwarded to INDAC will be completed immediately with an error. If DAC is enabled, the same access will be forwarded and serviced by DAC. 

## _**13.3.2.2.5.4.9 OSPI Direct Access Controller (DAC)**_ 

Direct access refers to the operation where data interface accesses directly trigger a read or write to FLASH memory. It is memory mapped and can be used to both access and directly execute code from external FLASH memory. Any incoming access that is not recognized as being within the programmable indirect trigger region is assumed to be a direct access and will be serviced by the DAC. Note that accesses that use DAC do not use the embedded SRAM. The data transfer stops when read or write burst is carried out. The amount of wait states applied will be dependent on the latency through the controller. Latency is kept to a minimum when the use of XIP read instructions are enabled (see OSPI_CONFIG_REG[18] ENTER_XIP_MODE_IMM_FLD and OSPI_CONFIG_REG[17] ENTER_XIP_MODE_FLD bits). 

## _**13.3.2.2.5.4.10 OSPI Indirect Access Controller (INDAC)**_ 

## _**13.3.2.2.5.4.10.1 Indirect Read Controller**_ 

The aim of the indirect mode of operation is to read significant numbers of bytes from FLASH memory without requiring a data interface access to trigger it. Instead indirect operations are controlled and triggered by software via specific control/configuration Indirect Read Transfer registers (OSPI_INDIRECT_READ_XFER_CTRL_REG, OSPI_INDIRECT_READ_XFER_WATERMARK_REG, OSPI_INDIRECT_READ_XFER_START_REG, and OSPI_INDIRECT_READ_XFER_NUM_BYTES_REG). This block will communicate with an embedded low level SPI protocol state machine module to perform an efficient and optimized FLASH read burst, placing the read data into the local SRAM module ready for fast and low latency delivery to any external controller. 

By default, the Indirect Read controller is disabled. Before enabling it, software must configure how much data is required and the start address. The start address and total number of bytes to be fetched is defined in OSPI_INDIRECT_READ_XFER_START_REG and OSPI_INDIRECT_READ_XFER_NUM_BYTES_REG registers, respectively. Up to two indirect operations can be programmed at any one time. The second operation can be triggered while the first is in progress. Supporting two indirect operations allows a short turnaround time between the completion of one indirect operation and the start of the second. For more information refer to Section 13.3.2.2.5.4.10.3, _Indirect Access Queuing_ . 

The total number of bytes to read in an indirect operation is not limited by the size of the SRAM. The size of SRAM will only limit the size of requests. In the case of SRAM overrun, the controller will back pressure FLASH reads until space becomes available in the SRAM. Back pressuring the reads on the SPI interface is handled by completing any current read burst, waiting until space in the SRAM becomes available and then issuing a new read burst at the address where the previous terminated burst ended. 

An external controller will be able to fetch the data that the controller has read from external FLASH memory by issuing data interface reads to the OSPI module. The address of the incoming read access must be in the range of indirect trigger address programmed via the OSPI_IND_AHB_ADDR_TRIGGER_REG register to indirect trigger address + 2**(indirect trigger address range) - 1. Default value of the range is equal to 16 locations. This allows a 16-beat burst to be applied starting from the indirect trigger address. The smaller bursts are possible to handle effectively as well with this approach. Furthermore it is not strict requirement to push consecutive address sequence. Actual address just has to be in the indirect range to grant SRAM as source. Each valid Indirect Read will cause the internal SRAM to be popped, thereby decoupling the incoming read access address from the FLASH address – that is not direct mapped. Therefore the indirect trigger address does not have any relationship with the FLASH address. It is just to indicate that data should take the SRAM as source instead of the FLASH memory array after triggering of any valid Indirect Read. The FLASH address for Indirect Read is taken from the OSPI_INDIRECT_READ_XFER_START_REG register. Assuming the requested data is present in the SRAM at the point the data interface access is received by the OSPI module, then the data will be fetched from the SRAM and the response to the read burst will be achieved with minimum latency. Once the data has been read from the SRAM, the OSPI module will free up the associated resource in the SRAM. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1451 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

If a read access is received whose address is not within the range described above then that access will not be completed using the indirect controller. It will instead be serviced by the direct access controller. 

If a read access is received whose address is within the range described above but the requested data is not immediately present in the SRAM then wait states will be applied until the data has been read from FLASH and pushed to the SRAM. 

If a read burst is received whose access elements traverse the Indirect trigger range, then the accesses within the Indirect trigger range will be processed by the indirect controller and the rest will be taken by the direct access controller. This is likely to be a software configuration error. 

The external controller is only permitted to issue 32-bit data interface reads until the last word of an indirect transfer. This helps keep the SRAM control logic less complex. On the final read, the external controller may issue a 16-bit (Halfword) or byte access to complete the transfer. It is also permitted for the external controller to always issue a 32-bit Word read on the last indirect access. The controller will pad the upper bits of the response with zero. The current expectation is that the SRAM will be kept fairly full while the read operation is carried out. The fill level of the SRAM is directly readable by software reading the OSPI_SRAM_FILL_REG register. 

An indirect operation may be cancelled at any time by setting 1 to OSPI_INDIRECT_READ_XFER_CTRL_REG[1] CANCEL_FLD bit. 

Any bus controller should be allowed to initiate an indirect access. The OSPI module provide software access mechanism to the SRAM fill-level directly via configuration registers and then decide for itself when the data should be fetched from the local SRAM. The fill level watermark register (see OSPI_INDIRECT_READ_XFER_WATERMARK_REG register) is provided. When the SRAM fill level passes this watermark, an interrupt is generated. If the watermark value is > 0, the watermark interrupt is also generated when the final byte of data has been read by the OSPI module and placed in the SRAM, even if the actual SRAM fill level has not risen above the watermark. This last feature is useful to avoid software tracking how much data has been read and resetting the watermark value for the last few bytes of an indirect read transfer. 

Two further interrupt sources are provided to help understand the status of an indirect operation. Firstly, an interrupt is generated when an indirect operation has completed. Secondly, an interrupt is generated if an Indirect Read operation was requested but could not be accepted due to the fact 2 indirect operations have already been buffered by the OSPI module. 

Setting the OSPI_INDIRECT_READ_XFER_CTRL_REG[0] START_FLD bit starts an indirect read operation. OSPI_INDIRECT_READ_XFER_CTRL_REG[2] RD_STATUS_FLD bit is available to check the status. 

## _**13.3.2.2.5.4.10.1.1 Indirect Read Transfer Process**_ 

The following sequence can be followed: 

1. Setup OSPI_CONFIG_REG register. 

2. Setup the indirect transfer's FLASH start address in the OSPI_INDIRECT_READ_XFER_START_REG register. 

3. Setup the number of bytes to be transferred in the OSPI_INDIRECT_READ_XFER_NUM_BYTES_REG register. 

4. Setup the indirect transfer's trigger address in the OSPI_IND_AHB_ADDR_TRIGGER_REG register. 

5. Setup the indirect transfer's trigger address range in the OSPI_INDIRECT_TRIGGER_ADDR_RANGE_REG register. 

6. If the watermark interrupt feature is to be used, set the OSPI_INDIRECT_READ_XFER_WATERMARK_REG register which will cause an interrupt to be generated when the fill level increases beyond the watermark level. Setting the watermark can be useful indication to software when to read the next part of the indirect read transfer. Note that if the watermark is set to a value other than zero, the watermark interrupt will always trigger once the final byte of indirect transfer has been fetched and placed in the embedded SRAM, even if the watermark value is higher than the actual completed fill level. 

7. Trigger Indirect Read access by setting the OSPI_INDIRECT_READ_XFER_CTRL_REG[0] START_FLD bit to 1. 

1452 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

8. If the watermark interrupt feature is to be used, wait for watermark interrupt. Else poll the SRAM fill level via the OSPI_SRAM_FILL_REG register to decide when sufficient data is in the SRAM to trigger data fetches. 

9. Read the expected amount of data from SRAM. If there is still more data to fetch in order to complete the indirect read transfer, then loop back to step 8. Otherwise continue to step 10. 

10. The completion status of the Indirect Read operation can be polled via the 

   - OSPI_INDIRECT_READ_XFER_CTRL_REG[5] IND_OPS_DONE_STATUS_FLD bit. 

11. An Indirect Complete interrupt will be generated when the Indirect read operation has completed. 

## _**13.3.2.2.5.4.10.2 Indirect Write Controller**_ 

The aim of the indirect mode of operation is to perform bulk transfer of data from the processor into a FLASH memory in the most efficient manner. The fewest possible write cycles inside the FLASH device will be carried out for the indirect transfer, thus maximizing the life of the device. Indirect write operation can be thought of from a software perspective as the inverse of the indirect read. It is controlled and triggered by software via specific control/configuration Indirect Write Transfer registers (for more information see the following registers: OSPI_INDIRECT_WRITE_XFER_CTRL_REG, OSPI_INDIRECT_WRITE_XFER_WATERMARK_REG, OSPI_INDIRECT_WRITE_XFER_START_REG, and OSPI_INDIRECT_WRITE_XFER_NUM_BYTES_REG). This block will await delivery of the write data via the external data interface controller, placing it in the local SRAM before communicating with the existing legacy SPI core to perform an efficient and optimized FLASH write burst. 

By default, the indirect write controller is disabled. Before enabling it, the software must configure how much data is required and the start address. The start address and total number of bytes to be written is defined in OSPI_INDIRECT_WRITE_XFER_START_REG and OSPI_INDIRECT_WRITE_XFER_NUM_BYTES_REG registers, respectively. Up to two indirect operations can be programmed at any one time. The second operation can be triggered while the first is in progress. Supporting two indirect operations allows a short turnaround time between the completion of one indirect operation and the start of the second. The Indirect write queuing is very similar to indirect read queuing. For more information refer to Section 13.3.2.2.5.4.10.3, _Indirect Access Queuing_ . 

The total number of bytes to write in an indirect operation is not limited by the size of the SRAM. The size of SRAM will only limit the amount of data that can be accepted from the external controller. In the case of an SRAM overrun, the controller will back pressure the data interface with wait states. Note the fill level of the SRAM is readable via programmable OSPI_SRAM_FILL_REG register and this can be used to avoid this situation. 

An external controller will provide the write data and will transfer this to the OSPI module by issuing data interface writes. The address of the incoming write access must be in the range of Indirect trigger address programmed via the OSPI_IND_AHB_ADDR_TRIGGER_REG register to Indirect trigger address + 2**(Indirect trigger address range) - 1. Default value of the range is equal to 16 locations. This allows a 16-beat burst to be applied starting from the Indirect trigger address. The smaller bursts are possible to handle effectively as well with this approach. Furthermore it is not strict requirement to push consecutive address sequence. Actual address just has to be in the Indirect Range to grant SRAM as source. Each write will cause the internal SRAM to be pushed, thereby decoupling the incoming write access address from the FLASH address – that is not direct mapped. Therefore Indirect trigger address does not have any relationship with FLASH address. It is just to indicate that data should take SRAM as source instead of FLASH Memory array after triggering of any valid Indirect Write. The FLASH address for Indirect Write is taken from the OSPI_INDIRECT_WRITE_XFER_START_REG register. Assuming the SRAM is not full at the point the data interface access is received by the OSPI module, then the data will be pushed to the SRAM with minimum latency. 

If a write access is received whose address is not within the range described above then that access will not be completed using the indirect controller. It will instead be serviced by the direct access controller. 

If a write access is received whose address is within the range described above but the SRAM is full then wait states will be applied until some or all of the data has been pushed from the SRAM to the FLASH. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1453 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

If a write burst is received whose access elements traverse the Indirect trigger range, then the accesses within the Indirect trigger range will be processed by the indirect controller, and the rest will be taken by the direct access controller. This is likely to be a software configuration error. 

The external controller is only permitted to issue 32-bit data interface writes until the last word of an indirect transfer. This helps keep the SRAM control logic less complex. On the final write, the external controller may issue a 32-bit word, 16-bit (halfword) or a byte access to complete the transfer. If the number of bytes to write is less than 4 on the last transfer, the controller is still permitted to issue a 32-bit transfer. In these cases, the extra bytes are discarded by the controller. 

When the SRAM holds a number of bytes equal to or greater than the size of a FLASH page (which itself is programmed into the OSPI module, with a default of 256 bytes) or when the SRAM holds all remaining bytes of the currently executing indirect transfer, the OSPI module will initiate a write burst to the flash command generator. 

An indirect operation may be cancelled at any time by setting 1 to the OSPI_INDIRECT_WRITE_XFER_CTRL_REG[1] CANCEL_FLD bit. 

Any bus controller should be allowed to initiate an indirect access. The OSPI module provide software access mechanism to the SRAM fill-level directly via the configuration registers and then decide for itself when the data should be written to the local SRAM. The fill level watermark register (see OSPI_INDIRECT_WRITE_XFER_WATERMARK_REG register) is provided. When the SRAM fill level falls below this watermark, an interrupt is generated. 

Two further interrupt sources are provided to help understand the status of an indirect operation. Firstly, an interrupt is generated when an indirect operation has completed. Secondly, an interrupt is generated if an indirect write operation was requested but could not be accepted due to the fact 2 indirect operations have already been buffered by the OSPI module. 

Setting the OSPI_INDIRECT_WRITE_XFER_CTRL_REG[0] START_FLD bit starts an indirect write operation. The OSPI_INDIRECT_WRITE_XFER_CTRL_REG[2] WR_STATUS_FLD bit is available to check the status. 

## _**13.3.2.2.5.4.10.2.1 Indirect Write Transfer Process**_ 

The following sequence can be followed: 

1. Setup OSPI_CONFIG_REG register. 

2. Setup the indirect transfer’s FLASH start address in the OSPI_INDIRECT_WRITE_XFER_START_REG register. 

3. Setup the number of bytes to be transferred in the OSPI_INDIRECT_WRITE_XFER_NUM_BYTES_REG register. 

4. Setup the indirect transfer’s trigger address in the OSPI_IND_AHB_ADDR_TRIGGER_REG register. 

5. Setup the indirect transfer's trigger address range in the OSPI_INDIRECT_TRIGGER_ADDR_RANGE_REG register. 

6. It is functionally valid for software to simply write all the data to the SRAM in one block transfer. However, if the total number of bytes to write is greater than the size of the partitioned SRAM, then it is quite likely the SRAM will become full causing the OSPI to back-pressure the system data bus for a considerable time. This time is based on the FLASH data-rate and the page-write time of the device. To avoid sending all the write data in one block transfer, software can make use of the watermark interrupt to identify a convenient time to send data a page at a time to the SRAM module. Alternatively, software can poll the SRAM fill level register directly to identify how empty the SRAM is at any one time in order to make a judgment as to when the most practical time to send the next part of the transfer. 

7. If the watermark interrupt feature is to be used, set the OSPI_INDIRECT_WRITE_XFER_WATERMARK_REG register which will cause an interrupt to be generated when the fill level falls below the watermark. The watermark should be set to a number between zero and a page size. That is if the page size is 256 bytes, then setting the watermark to a value between 10 and 250 is reasonable and will cause the interrupt to trigger when the fill level drops below the programmed number. 

1454 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

   - Setting the watermark can be useful to provide an indication to software when to write the next page of data to the SRAM. 

8. Trigger Indirect Write access by setting OSPI_INDIRECT_WRITE_XFER_CTRL_REG[0] START_FLD bit. 

9. If the remaining number of bytes still to be transferred into the SRAM for the current indirect transfer is greater than a FLASH page, then write 1 FLASH page worth of data to the SRAM. Otherwise send the remaining data from the indirect transfer to SRAM. 

10. If all the data in the indirect transfer has now been sent to the SRAM, then go to 12 and await indirect complete status. Otherwise if there is more data still to be transferred then either: 

   - If the watermark interrupt feature is being used, then wait for watermark interrupt. 

   - Alternatively the SRAM fill level can be interrogated to identify a convenient time to send more data. 

11. Loop back to 9. 

12. Optional: The completion status of the Indirect write operation can be polled via OSPI_INDIRECT_WRITE_XFER_CTRL_REG[5] IND_OPS_DONE_STATUS_FLD. 

13. An Indirect Complete interrupt will be generated when the Indirect write operation has completed. 

## _**13.3.2.2.5.4.10.3 Indirect Access Queuing**_ 

Software is permitted to queue up to two indirect transfers for both the indirect write controller and the indirect read controller. Supporting two indirect operations allows a short turnaround time between the completion of one indirect operation and the start of the second. Any attempt to queue more than two operations will cause an interrupt to be generated. To take advantage of this feature, software should attempt to keep both indirect programming slots full at all times. 

From the software perspective, indirect access queuing is achieved by triggering bit 0 of the indirect transfer control register (OSPI_INDIRECT_READ_XFER_CTRL_REG[0] START_FLD bit or OSPI_INDIRECT_WRITE_XFER_CTRL_REG[0] START_FLD bit) twice in short succession. The indirect number of bytes register (OSPI_INDIRECT_READ_XFER_NUM_BYTES_REG or OSPI_INDIRECT_WRITE_XFER_NUM_BYTES_REG register) and the indirect FLASH start address register (OSPI_INDIRECT_READ_XFER_START_REG or OSPI_INDIRECT_WRITE_XFER_START_REG register) must be setup with the relevant transfer data before START_FLD bit can be triggered for each transfer. Since these registers will change regularly, the hardware must keep sampled versions of these registers for the duration of the indirect transfer. 

The internal register block will only issue an indirect start trigger to the key underlying datapath blocks one at a time. There are 2 independent datapath blocks in the indirect access controller that will receive and independently sample this information. The first is the datapath block on the data bus side of the SRAM. For indirect reads, this is a read interface, for indirect writes, it is a write interface. The second is the datapath block on the FLASH side of the SRAM. For indirect reads, this is a write interface, for indirect writes, it is a read interface. Both blocks will process the indirect transfers at different times. For example, for an indirect read operation, the datapath block on the FLASH side of the SRAM will be able to start processing the second queued transfer as soon as the last byte of the first transfer has been written to the SRAM. Before commencing the second transfer, this block must resample the OSPI_INDIRECT_READ_XFER_NUM_BYTES_REG and OSPI_INDIRECT_READ_XFER_START_REG registers. Similarly, the datapath block on the bus side will resample the same registers locally when it has forwarded all the FLASH data associated with the first indirect transfer from the SRAM onto the data bus. 

## _**13.3.2.2.5.4.10.4 Consecutive Writes and Reads Using Indirect Transfers**_ 

It is permitted for software to trigger an indirect read operation while an indirect write operation is in progress. Similarly it is permitted to trigger an indirect write while an indirect read operation is in progress. Indirect write operations will take overall precedence. 

## _**13.3.2.2.5.4.10.5 Accessing the SRAM**_ 

The SRAM depth is separated in two segmets. The lower segment is reserved for indirect read use. The upper segment is for indirect write use only. The size of each segment is programmable via the OSPI_SRAM_PARTITION_CFG_REG register. This feature allows to allocate how many bits of the SRAM 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1455 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

address bus are allocated to indirect read. By default, this is set so that exactly half of the SRAM is portioned for use by the indirect read controller. To ensure the read data bus is not directly fed by the SRAM read data through combinatorial logic, an extra bank of holding registers is included in the indirect read data path. These registers act as an extra location to be added to the allocated number of SRAM locations for indirect read. 

To illustrate how the SRAM (and the extra bank of holding registers) can be allocated between indirect read and write, the following example is provided. The depth of the SRAM in this example is configured to be 8 bits. This is equal to 256 locations. 

- If the OSPI_SRAM_PARTITION_CFG_REG[7-0] ADDR_FLD field is set to 0x00, then 256 locations are allocated to indirect writes and 1 location to indirect reads. 

- If the OSPI_SRAM_PARTITION_CFG_REG[7-0] ADDR_FLD field is set to 0x01, then 255 locations are allocated to indirect writes and 2 locations to indirect reads. 

- If the OSPI_SRAM_PARTITION_CFG_REG[7-0] ADDR_FLD field is set to 0x02, then 254 locations are allocated to indirect writes and 3 locations to indirect reads. 

- And so on until. 

- If the OSPI_SRAM_PARTITION_CFG_REG[7-0] ADDR_FLD field is set to 0xFD, then 3 locations are allocated to indirect writes and 254 locations to indirect reads. 

- If the OSPI_SRAM_PARTITION_CFG_REG[7-0] ADDR_FLD field is set to 0xFE, then 2 locations are allocated to indirect writes and 255 locations to indirect reads. 

- If the OSPI_SRAM_PARTITION_CFG_REG[7-0] ADDR_FLD field is set to 0xFF, then 1 location is allocated to indirect writes and 256 locations to indirect reads. 

## **Note** 

A value of 0xFF or 0x00 in the OSPI_SRAM_PARTITION_CFG_REG register should be avoided by software, as only the bottom 8 bits of the SRAM fill level are accessible through software (up to 255 limit) via the OSPI_SRAM_FILL_REG register. If the fill level reaches 256 on either the indirect read or write side, it will appear when reading the Fill Level to be 0. 

There are four SRAM sources that are arbitrated and muxed onto the single SRAM port. Up to three sources can access this port at any one time. The sources are described as follows: 

- Indirect Write, Write source. This is located on the data bus side of the SRAM. 

- Indirect Write, Read source. This is located on the FLASH side of the SRAM. 

- Indirect Read, Write source. This is located on the FLASH side of the SRAM. 

- Indirect Read, Read source. This is located on the data bus side of the SRAM. 

A fixed priority arbitration scheme is implemented. Table 13-198 shows priority allocated to these sources. 

**Table 13-198. SRAM Access Priority** 

## **SRAM Access Priority** 

|Indirect Write|Write to SRAM (from System Data Bus)|3rd (exclusive with Data Bus Read Request)|
|---|---|---|
||Read from SRAM (from OSPI Module)|2nd|
|Indirect Read|Write to SRAM (from OSPI Module)|1st|
||Read from SRAM (from System Data Bus)|3rd (exclusive with Data Bus Write Request)|



## **Note** 

With the exception of the write port during an Indirect Read operation (on the FLASH side of the SRAM), the logic driving all four sources must not assume single cycle completion. Writes to the SRAM during an indirect read must be allowed to complete immediately to avoid data loss. Therefore this port is given maximum priority. 

1456 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.2.2.5.4.11 OSPI Software-Triggered Instruction Generator (STIG)**_ 

The DAC and INDAC are used to transfer data. In order to access the volatile and non-volatile configuration registers, the legacy SPI Status register, other status/protection registers as well as to perform ERASE functions, a separate software controller is required. The software triggered instruction generator (STIG) is controlled using the OSPI_FLASH_CMD_CTRL_REG register by setting up the command to issue to the FLASH device. This is a generic controller and can be used to perform any instruction that the FLASH device supports from the extended SPI protocol. Configuring of instructions which are not compliant with the specification of the FLASH devices could cause unpredicted behavior of the controller. OSPI_FLASH_CMD_CTRL_REG[31-24] CMD_OPCODE_FLD bits should be set different than OSPI_DEV_INSTR_RD_CONFIG_REG[7-0] RD_OPCODE_NON_XIP_FLD and OSPI_DEV_INSTR_WR_CONFIG_REG[7-0] WR_OPCODE_FLD. The OSPI_FLASH_CMD_CTRL_REG[0] CMD_EXEC_FLD bit is used to trigger the command. The OSPI_FLASH_CMD_CTRL_REG[1] CMD_EXEC_STATUS_FLD bit is used by software to poll the status of the command execution. For reads, when the command has been serviced (OSPI_FLASH_CMD_CTRL_REG[1] CMD_EXEC_STATUS_FLD bit toggles from '1' to '0'), up to 8 bytes of read data will be placed in the OSPI_FLASH_RD_DATA_LOWER_REG and OSPI_FLASH_RD_DATA_UPPER_REG registers. For writes, the write data should be placed in the OSPI_FLASH_WR_DATA_LOWER_REG and OSPI_FLASH_WR_DATA_UPPER_REG registers. 

The completion of the STIG request could be also checked by the corresponding interrupt. The occurrence of the interrupt indicates that the controller is ready for accepting a new STIG request. It is important to notice that completion of the STIG request is not equivalent to completion it on SPI side. For example, if STIG is configured to the command composed of data to transmit only, the data is taken from the corresponding STIG register fields and put into TX FIFO. Since all bytes to write are known, another STIG can be queued before serialization of the current one is completed. 

There are some commands which require more data to read than 8 bytes (for example READ ID command). The additional STIG Memory Bank is implemented in order to accommodate these data if needed. The STIG Memory Bank (internal component of the controller) is controlled by the OSPI_FLASH_CMD_CTRL_REG[2] STIG_MEM_BANK_EN_FLD bit. If enabled, the number of bytes to read in the STIG is extended to 16 as defined in OSPI_FLASH_COMMAND_CTRL_MEM_REG[18-16] NB_OF_STIG_READ_BYTES_FLD bit field. It should be noticed that there are very few commands (excluding Read Array ones which are not intended to handle effectively in STIG Mode but in Direct/Indirect Modes) which return more than 8 bytes to the controller. If the maximum number of bytes to Read using STIG in target application is less than 16, the depth of the STIG Memory Bank can be set smaller what will result in saving noticeable part of the area. 

If number of bytes to Read in the STIG as defined in OSPI_FLASH_COMMAND_CTRL_MEM_REG[18-16] NB_OF_STIG_READ_BYTES_FLD bit field exceeds the Memory Bank Depth, remaining data will overwrite the STIG Memory Bank locations starting from its first address. OSPI_FLASH_RD_DATA_LOWER_REG and OSPI_FLASH_RD_DATA_UPPER_REG keep the last 8 bytes read from the Flash Device by STIG when Memory Bank is enabled. Therefore, for example if the user wants to get just a single byte from the last eight bytes from long continuous read SPI data chain, there is no need to access the STIG Memory Bank since data can be taken from suitable Flash Command Read Data register. In order to access more data, STIG Memory Bank data request should be triggered. It is controlled by the OSPI_FLASH_COMMAND_CTRL_MEM_REG and works analogously for triggering STIG from the functional standpoint. 

OSPI_FLASH_COMMAND_CTRL_MEM_REG[0] TRIGGER_MEM_BANK_REQ_FLD bit is used to trigger the command, bit OSPI_FLASH_COMMAND_CTRL_MEM_REG[1] MEM_BANK_REQ_IN_PROGRESS_FLD is used by software to poll the status of the command execution. When 

MEM_BANK_REQ_IN_PROGRESS_FLD bit toggles from "1" to "0", the byte of data (OSPI_FLASH_COMMAND_CTRL_MEM_REG[15-8] MEM_BANK_READ_DATA_FLD) from corresponding address (OSPI_FLASH_COMMAND_CTRL_MEM_REG[28-20] MEM_BANK_ADDR_FLD bit field) is valid. The address should be set before triggering the STIG Memory Bank access. Each consecutive STIG access overwrites the previous one so that the data in the Bank always fit into byte index fetched by the last STIG access configured to use the Memory Bank (first incoming byte equals first address of the Memory Bank, second one equals the second address and so on). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1457 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.2.5.4.11.1 Servicing a STIG Request**_ 

A STIG request will cause the OSPI Flash controller to interrogate the OSPI_FLASH_CMD_CTRL_REG register to determine what and how many bytes it should send to the FLASH device. The OSPI_FLASH_CMD_CTRL_REG[31-24] CMD_OPCODE_FLD field of this register indicate the instruction to be sent and is always pushed first. If there is an address to send, then the address (the size of which is also programmed in the same register) is sent next. The address itself is stored in the OSPI_FLASH_CMD_ADDR_REG register. If Mode bits are enabled by OSPI_FLASH_CMD_CTRL_REG[18] ENB_MODE_BIT_FLD bit. OSPI_MODE_BIT_CONFIG_REG[7-0] MODE_FLD bit field are being sent right after address. If OSPI_FLASH_CMD_CTRL_REG[18] ENB_MODE_BIT_FLD and OSPI_CONFIG_REG[29] CRC_ENABLE_FLD are both enabled, STIG will replace XIP Mode bits (not applicable for CRC aware SPI interface) for automatically calculated address CRC byte. Therefore, to execute CRC aware STIGs (meaning the commands requiring sending address CRC byte), ENB_MODE_BIT_FLD bit should always be set. If there are any dummy cycles to send (the size of which is also programmed in OSPI_FLASH_CMD_CTRL_REG register) then those are sent next. If there is data to write or read (the size of which is also programmed in OSPI_FLASH_CMD_CTRL_REG register) then for the case of writes, up to 8 bytes can be sent (as stored in the Flash Command Write Data registers, OSPI_FLASH_WR_DATA_LOWER_REG and OSPI_FLASH_WR_DATA_UPPER_REG registers) next. In the read case, when the read data has been collected from the FLASH device, the OSPI Flash Controller stores that in the Flash Command Read Data Registers (OSPI_FLASH_RD_DATA_LOWER_REG and OSPI_FLASH_RD_DATA_UPPER_REG registers). Up to 8 bytes can be get if OSPI_FLASH_CMD_CTRL_REG[2] STIG_MEM_BANK_EN_FLD bit is disabled or up to 512 when enabled. When the OSPI Flash controller starts to service a STIG request, it sets the OSPI_FLASH_CMD_CTRL_REG[1] CMD_EXEC_STATUS_FLD bit to indicate a command execution is in progress. When the OSPI Flash controller is in the auto-polling state, servicing a STIG request is slightly different. Most of devices are largely inaccessible after a program operation until the device has completed that write. Some group of them has a possibility to suspend programming page. It can be controlled by the OSPI_POLLING_FLASH_STATUS_REG[8] DEVICE_STATUS_VALID_FLD bit, which indicate active autopolling phase. After requesting a STIG, the OSPI Flash Controller immediately issues appropriate OPCODE to Memory. During servicing a STIG (in auto-polling phase) the status bit of command execution remains steady and other parts of transfer such as ADDRESS or DUMMY BITS, and so forth, are disabled (to issued Program Suspend Command is needed OPCODE only). There is a programmable option to add delay between every repetitive poll operation (delay is defined by OSPI_WRITE_COMPLETION_CTRL_REG[31-24] POLL_REP_DELAY_FLD bit field). This feature is implemented to free up SPI bandwidth if needed. 

## **Note** 

The OSPI data is sent LSB first, while address is sent MSB first. 

## **Note** 

The STIG complete status bit gets cleared before the actual flash access completes. Software should wait for about 700 ns if there is any dependency on actual access completion. 

## _**13.3.2.2.5.4.12 OSPI Arbitration Between Direct / Indirect Access Controller and STIG**_ 

When multiple controllers are active simultaneously, a simple fixed-priority arbitration scheme is used to arbitrate between each interface and access the external FLASH. The fixed priority is defined as follows, highest priority first. 

- The Indirect Access Write 

- The Direct Access Write 

- The STIG 

- The Direct Access Read 

- The Indirect Access Read 

1458 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.2.2.5.4.13 OSPI Command Translation**_ 

Requests issued by the direct access controller, the indirect access controller or the STIG will be translated into a sequence of byte transfers to send downstream (before serialization to the FLASH device). These sequences depend on the requested transfer but an example of a typical 1-byte non sequential READ is shown below: 

INSTRUCTION OPCODE -> ADDRESS -> Mode Byte -> Dummy Bytes -> 1 byte of don't care 

For sequential accesses, an extra byte of data per read is pushed to the FLASH device on the back of the above sequence assuming it can be done so with no gap between each transferred byte. 

When PHY mode is enabled and consequently no clock divider is configured, latency caused by multi domain synchronization may make an extra byte insufficient to avoid the transfer gap. To ensure the sequential access non-interrupted and keep the maximum performance of the controller, PHY Pipeline Mode is implemented. When enabled, number of don't care bytes is calculated based on the configuration. 

The actual sequence sent to the FLASH device depends on the requested transfers, whether the transfer is non-sequential or sequential, whether the device has been configured in XIP mode and the state of the main Device Instruction Type programmable registers (OSPI_DEV_INSTR_RD_CONFIG_REG and OSPI_DEV_INSTR_WR_CONFIG_REG). 

For writes, the write enable latch (or WEL) within the FLASH device itself must be high before a write sequence can be issued. The OSPI Flash Controller will automatically issue the write enable latch command before triggering a write command via the direct or indirect access controllers (DAC/INDAC) – that is the user does not need to perform this operation. For increasing flexibility and performance user can turn off this feature by setting the OSPI_DEV_INSTR_WR_CONFIG_REG[8] WEL_DIS_FLD bit. The opcode for WREN is typically 0x06 and is common between devices. 

When write requests from the direct or indirect access controllers are no longer being received and all outstanding requests have been sent, the FLASH device will automatically start the page program write cycle. Any incoming request at this time will be held in wait states until the cycle has completed. The OSPI Flash Controller will automatically poll the FLASH device legacy SPI status register to identify when the write cycle has completed. This is achieved by sending the RDSR opcode to the FLASH device and waiting until the device itself has indicated the write cycle has completed (until the Write in Progress bit has cleared to zero and the write enable latch bit has also cleared to zero or device is ready bit has set to one). The WREN and the RDSR device instructions are the only ones that are sent by the controller under the hood. For any other specific instruction that the user determines should be sent to the device (for example if the device needs to be unprotected before a write command is issued), these should be handled separately by issuing FLASH commands via the STIG. 

There is an option to trigger HOLD or RESET feature on I/Os of the Flash Device. The HOLD one is generally common across the devices and takes an alternative function of DQ3 pin (applicable when device operates neither in Quad SPI mode nor DDR). The transfer can be hold and then resumed by dedicated software trigger field (OSPI_CONFIG_REG[4] HOLD_PIN_FLD). The devices which have the HOLD feature on DQ3 usually need another dedicated pin for hardware reset and ones without HOLD feature usually have alternative reset on DQ3 what makes the additional reset pin being redundant. The controller supports both variants and reset selection register field (OSPI_CONFIG_REG[6] RESET_CFG_FLD) allows the user to configure which hardware reset solution is implemented in the device under usage. 

After configuration is done, it is possible to trigger HOLD or RESET features using I/Os (OSPI_CONFIG_REG[4] HOLD_PIN_FLD or OSPI_CONFIG_REG[5] RESET_PIN_FLD bits). After HOLD activation the controller is introduced into waiting state and any other operations should not be requested before de-asserting of HOLD configuration bit. The HOLD feature is useful when any SPI transaction needs to be prolonged in order to adjust it into specific point in time. Note that any HOLD trigger issued during active SPI transaction may be synchronized into reference clock domain at the time the SPI transfer turns to be finished. In this case, there is nothing to hold so the low level SPI logic will not activate HOLD on DQ3. To check if HOLD request suspended the transfer OSPI_CONFIG_REG[31] IDLE_FLD bit can be polled for. If SPI is not in the IDLE state, the transfer was successfully suspended. It is important for the software to take care of resetting OSPI_CONFIG_REG[4] HOLD_PIN_FLD bit before newly triggered SPI transaction. In case HOLD 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1459 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

request is set before the beginning of the transfer it will be HOLD right after it starts what may not always be a goal. The hardware RESET needs to be activated when CS is high (no valid transaction is present on SPI bus). It can be checked by polling of OSPI_CONFIG_REG[31]. If the controller is in the IDLE state and no other transfer requests are queued to perform, the hardware RESET can be triggered. The RESET feature is useful when any write, program or erase operation needs to be cancelled. No transfer request is permitted before driving the reset back to being inactive. Triggering HOLD or RESET on DQ3 at the time the device is configured to work in Quad SPI mode or DDR will overwrite transfer data on DQ3 with '0'. This behavior is considered as a software error so it is advisable for the system to make sure that the flash device was introduced to suitable SPI mode (that is by polling its configuration register) before triggering alternative DQ3 function. There are four independent reset outputs implemented to separate between multiple devices connected to the controller (up to 4 are supported). The decision which reset output is to be activated after triggering OSPI_CONFIG_REG[5] RESET_PIN_FLD bit is made based on OSPI_CONFIG_REG[9] PERIPH_SEL_DEC_FLD and OSPI_CONFIG_REG[13-10] PERIPH_CS_LINES_FLD bits. Reset output OSPI_ECC_VECTOR is to be directly driven into corresponding dedicated RESET pins of the devices with separated RESET pin and alternatively, Reset output OSPI_ECC_VECTOR is to be control OSPI_ECC_VECTOR of the DQ3 RESET devices enabling separating of DQ3 Controller Outputs on SoC integration level. 

The controller supports all combinations of CPHA and CPOL for Serial Clock. It allows the controller to support any SPI target devices not limited to Flash Memories. Multiple-SPI flash devices use just a subset of these combinations depending on the Transfer Mode as defined in . 

**Table 13-199. Flash SPI Modes** 

|**(SEL_CLK_POL_FLD, SEL_CLK_PHASE_FLD)**|**Edge Mode**|**Support**|
|---|---|---|
|0x00 (SPI MODE 0)|SDR|Yes|
|0x01 (SPI MODE 1)|SDR|No|
|0x10 (SPI MODE 2)|SDR|No|
|0x11 (SPI MODE 3)|SDR|Yes|
|0x00 (SPI MODE 0)|DDR|Yes|
|0x01 (SPI MODE 1)|DDR|No|
|0x10 (SPI MODE 2)|DDR|No|
|0x11 (SPI MODE 3)|DDR|No|



## _**13.3.2.2.5.4.14 Selecting the Flash Instruction Type**_ 

In order to send the correct READ and WRITE opcodes, software should initialize the OSPI_DEV_INSTR_RD_CONFIG_REG and the OSPI_DEV_INSTR_WR_CONFIG_REG registers. These registers include fields to setup the required instruction opcodes that is intended to be used to access the FLASH (default is basic READ and basic page program) as well as the instruction type, edge mode (DDR or SDR) and whether the instruction uses single, dual, quad or octal pins for address and data transfer. Providing this level of control to the user provides a future proofed generic solution. To ensure the controller can operate from a reset state, the registers will be reset to an opcode compatible with SIO devices what can be modified using BOOT feature. 

Despite being applicable for both READs and WRITEs, the OSPI_DEV_INSTR_RD_CONFIG_REG[9-8] INSTR_TYPE_FLD field only appears once – it is not included in the OSPI_DEV_INSTR_WR_CONFIG_REG register. If software sets this to anything other than '0', then the address transfer type and the data transfer type bits of both OSPI_DEV_INSTR_RD_CONFIG_REG and OSPI_DEV_INSTR_WR_CONFIG_REG registers become don't care. It is made available to allow software to support the less common FLASH instructions where the opcode, address and data are sent on 2 or 4 lanes (the opcode from most instructions are sent serially to the FLASH device, even for dual/quad instructions). 

There are devices capable to handling Read Operations in Dual Data Rate Mode (DDR) (it is also called Dual Transfer Rate Mode (DTR)). That means they can issue and capture the data on both rising and falling edges during working with dedicated command type. This enables the controller to maintain throughput at twice lower 

1460 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

frequency of OSPI clock. The Device Read Instruction Register has DDR enable bit which informs Octal-SPI Flash Controller that opcode written into Read Opcode field is capable with DDR command type. The other field defined in OSPI_RD_DATA_CAPTURE_REG[19-16] DDR_READ_DELAY_FLD which enables the controller to shift the transmitted data in DDR mode. By default, data are shifted by 1 clock cycle to ensure hold timing greater than 0 during DDR transactions. It may not be sufficient for high reference clock frequency in accordance with the high dividers. 

Table 13-200 shows how software should configure the OSPI module for selected specific READ and WRITE instruction supported by the abovementioned device. 

**Table 13-200. READ and WRITE Instruction Configuration** 

|**Table 13-200. READ and WRITE Instruction Configuration**|**Table 13-200. READ and WRITE Instruction Configuration**|**Table 13-200. READ and WRITE Instruction Configuration**|**Table 13-200. READ and WRITE Instruction Configuration**|**Table 13-200. READ and WRITE Instruction Configuration**|**Table 13-200. READ and WRITE Instruction Configuration**|**Table 13-200. READ and WRITE Instruction Configuration**|**Table 13-200. READ and WRITE Instruction Configuration**|
|---|---|---|---|---|---|---|---|
|**READ**||||||||
|OPCODE|OPCODE<br>sent over<br>how many<br>lanes /<br>edge<br>mode?|ADDRESS /<br>DUMMY /<br>MODE sent<br>over how<br>many lanes /<br>edge mode?|DATA bytes<br>sent over<br>how many<br>lanes / edge<br>mode?|Instruction Type<br>(OSPI_DEV_INS<br>TR_RD_CONFIG<br>_REG[9-8]<br>INSTR_TYPE_FL<br>D)|Address transfer<br>type<br>(OSPI_DEV_INST<br>R_RD_CONFIG_R<br>EG[13-12]<br>ADDR_XFER_TY<br>PE_STD_MODE_<br>FLD)|Data transfer type<br>(OSPI_DEV_INST<br>R_RD_CONFIG_<br>REG[17-16]<br>DATA_XFER_TYP<br>E_EXT_MODE_F<br>LD)|DDR bit enable<br>(OSPI_DEV_INST<br>R_RD_CONFIG_R<br>EG[10]<br>DDR_EN_FLD)|
|READ|1/SDR|1/SDR|1/SDR|0|0|0|0|
|FAST_READ|1/SDR|1/SDR|1/SDR|0|0|0|0|
|DTR_FAST_<br>READ|1/SDR|1/DDR|1/DDR|0|0|0|1|
|DOFR (Dual O/p<br>Fast Read)|1/SDR|1/SDR|2/SDR|0|0|1|0|
|DIOFR (Dual I/O<br>Fast Read)|1/SDR|2/SDR|2/SDR|0|1|1|0|
|DDIOFR (DTR<br>Dual I/ O Fast<br>Read)|1/SDR|2/DDR|2/DDR|0|1|1|1|
|QOFR (Quad<br>O/p Fast Read)|1/SDR|1/SDR|4/SDR|0|0|2|0|
|QIOFR (Quad<br>I/O Fast Read)|1/SDR|4/SRD|4/SDR|0|2|2|0|
|DQIOFR (DTR<br>Quad I/ O Fast<br>Read)|1/SDR|4/DDR|4/DDR|0|2|2|1|
|OOFR (Octal<br>O/p Fast Read)|1/SDR|1/SDR|8/SDR|0|0|3|0|
|OIOFR (Octal<br>I/O Fast Read)|1/SDR|8/SDR|8/SDR|0|3|3|0|
|DOIOFR (DTR<br>Octal O/p Fast<br>Read)|1/SDR|1/DDR|8/DDR|0|0|3|1|
|4DOIOFR (4-<br>byte DTR Octal<br>I/O Fast Read)|1/SDR|8/DDR|8/DDR|0|3|3|1|
|DCFR (Dual<br>Command Fast<br>Read)|2/SDR|2/SDR|2/SDR|1|Don't care|Don't care|0|
|DDCFR (DTR<br>Dual Command<br>Fast Read)|2/SDR|2/DDR|2/DDR|1|Don't care|Don't care|1|
|QCFR (Quad<br>Command Fast<br>Read)|4/SDR|4/SRD|4/SDR|2|Don't care|Don't care|0|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1461 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-200. READ and WRITE Instruction Configuration (continued)** 

|DQCFR (DTR<br>Quad Command<br>Fast Read)|4/SDR|4/DDR|4/DDR|2|Don't care|Don't care|1|
|---|---|---|---|---|---|---|---|
|OCFR (Octal<br>Command Fast<br>Read)|8/SDR|8/SDR|8/SDR|3|Don't care|Don't care|0|
|4DOCFR (4-byte<br>DTR Octal<br>Command Fast<br>Read)|8/SDR|8/DDR|8/DDR|3|Don't care|Don't care|1|
|**WRITE**||||||||
|OPCODE|OPCODE<br>sent over<br>how many<br>lanes?|ADDRESS /<br>DUMMY /<br>MODE sent<br>over how<br>many lanes?|DATA bytes<br>sent over<br>how many<br>lanes?|Instruction Type<br>(OSPI_DEV_INS<br>TR_RD_CONFIG<br>_REG[9-8]<br>INSTR_TYPE_FL<br>D)|Address transfer<br>type<br>(OSPI_DEV_INST<br>R_WR_CONFIG_<br>REG[13-12]<br>ADDR_XFER_TY<br>PE_STD_MODE_<br>FLD)|Data transfer type<br>(OSPI_DEV_INSTR_WR_CONFIG_R<br>EG[17-16]<br>DATA_XFER_TYPE_EXT_MODE_FL<br>D)||
|PP|1|1|1|0|0|0||
|DIFP (Dual Input<br>Fast Program)|1|1|2|0|0|1||
|DIEFP (Dual<br>Input Extended<br>Fast Program)|1|2|2|0|1|1||
|QIFP (Quad<br>Input Fast<br>Program)|1|1|4|0|0|2||
|QIEFP (Quad<br>Input Extended<br>Fast Program)|1|4|4|0|2|2||
|OIFP (Octal<br>Input Fast<br>Program)|1|1|8|0|0|3||
|OIEFP (Octal<br>Input Extended<br>Fast Program)|1|8|8|0|3|3||
|DCPP (Dual<br>Command Fast<br>Program)|2|2|2|1|Don't care|Don't care||
|QCPP (Quad<br>Command Fast<br>Program)|4|4|4|2|Don't care|Don't care||
|OCPP (Octal<br>Command Fast<br>Program)|8|8|8|3|Don't care|Don't care||



## **Note** 

This data are applicable for both 3-byte or 4-byte address variants of the commands if did not indicate otherwise. 

1462 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

In DTR protocol all transfer phases (including opcode) take DDR edge mode independently on the command under execution. DTR protocol is to be enabled by OSPI_CONFIG_REG[24] ENABLE_DTR_PROTOCOL_FLD bit. It has higher priority than DDR Mode enable bit from OSPI_DEV_INSTR_RD_CONFIG_REG[10] DDR_EN_FLD. 

## _**13.3.2.2.5.4.15 OSPI Data Integrity**_ 

The CRC aware SPI transfer can be performed when both controller and device are configured to work in the Octal DDR Protocol. 

For write transactions (the controller transmits data throughout all transfer), the controller is responsible for sending address CRC byte (XOR of all address bytes) following address bytes and TX data CRC byte (XOR of all data bytes to write) following data chunk with size as defined in OSPI_MODE_BIT_CONFIG_REG[10-8] CHUNK_SIZE_FLD bit field. All CRC data are being calculated and sent automatically by the controller and the external device is responsible for reacting accordingly on any possible interpolation on the Flash interface. For read transactions, the controller is also responsible for sending address CRC byte (like for write) and for getting and progressing RX data CRC byte returning by the Flash Device after each chunk with size as defined in OSPI_MODE_BIT_CONFIG_REG[10-8] CHUNK_SIZE_FLD bit field. At the time when the Flash Device is returning data back to the controller, the controller dynamically calculates checksum byte by byte. Once the chunk is completed, CRC returned from Flash Device should fit to dynamically calculated CRC by the controller. In case of any deviation, controller reports CRC error to the system by corresponding interrupt (CRC error interrupt). The controller also provides the last captured CRC data in RX data chunk (defined in OSPI_MODE_BIT_CONFIG_REG[31-24] RX_CRC_DATA_LOW_FLD and OSPI_MODE_BIT_CONFIG_REG[23-16] RX_CRC_DATA_UP_FLD bit fields) to give the software driver the opportunity to further detecting any data corruption on system interfaces. The CRC data valid interrupt informs the system about the accessibility of the new RX CRC data in the registers. Once the system gets the full data word, it can calculate CRC by itself. At the time it collects all data words in chunk and then gets the CRC data valid interrupt, it can compare these data and react accordingly. 

Some devices also have embedded ECC mechanism allowing them to report data abnormal conditions on their ECC Correction Signal output. At the time this output turns low, the device expect the OSPI controller to read status register of the device in order to get more details about the source of detected abnormal situation. The OSPI controller investigates ECC status on its ECC_FAIL input and generates an interrupt when detecting this signal being low. 

## _**13.3.2.2.5.4.16 OSPI PHY Module**_ 

OSPI module fully integrates PHY module dedicated to more flexible and power efficient transfers. 

The PHY module communicates with the OSPI Flash controller via the aforementioned PHY Interface and handles data transfer on low-level stage of design hierarchy. However, when the OSPI_RCLK is configured to be equal to the SPI clock instead of alternative approach using clock divider, there is just one OSPI_RCLK cycle (not 4 or more) within single SPI period or half period for DDR Mode (SPI Control Module works on reference clock). Given that OSPI_RCLK is the input clock for RX FIFO and the output one for TX FIFO, the PHY solution incurs more restrictive requirement for value of system clock in order to synchronize data without SPI transfer interruption. For example, when the controller operates in DDR 1× octal Mode, 2 bytes of data (equivalent to one RX FIFO location) is gathered within just single OSPI_RCLK cycle. The controller cannot predict next data access while operating in the Direct Mode (meaning its size or whether it is sequential to the previous one or not). As a result, if the OSPI_HCLK is not significantly greater than OSPI_RCLK, the SPI transfer has to be suspended until the Flash Command Generator forwards new data to TX FIFO. 

An optional PHY Pipeline Mode is implemented to avoid the necessity of stable clocking of the system clock for the Direct Mode when the PHY mode is enabled and to keep maximum performance while ensuring correct operation of the OSPI controller with the PHY using low frequencies from all its domains. This mode is a trade-off between large software overhead when operating in the Indirect Mode and the described limitations 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1463 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

present in the Direct Mode. For more information about PHY Pipeline Mode, see Section 13.3.2.2.5.4.16.1, _PHY Pipeline Mode_ . 

When DDR 2× Mode is granted based on configuration – SPI transfer is automatically performed using the PHY module even if the OSPI_CONFIG_REG[3] PHY_MODE_ENABLE_FLD is de-asserted. SDR 2× commands are handled with PHY module paths being bypassed. Nevertheless, dividers of 2, 4 or 6 for DDR and divider of 2 for SDR should not be configured based on controller requirements and these configurations are perceived as a software error. 

The following steps are an example of software algorithm of adapting the OSPI controller with the PHY module incorporated to work in octal 1× clock DDR Protocol. Note that all necessary configuration steps described in Section 13.3.2.2.5.5.2, _Configuring the OSPI Controller for Optimal Use_ shall be completed before the algorithm. 

1. Set PHY mode enable (OSPI_CONFIG_REG[3] PHY_MODE_ENABLE_FLD bit) and DDR protocol (OSPI_CONFIG_REG[24] ENABLE_DTR_PROTOCOL_FLD bit). It is assumed that device is configured to work in DDR Protocol. 

2. Before setting the DLL parameters, software calibration could be needed. OSPI_PHY_MASTER_CONTROL_REG[23] PHY_MASTER_BYPASS_MODE_FLD bit controls the bypass mode of the controller and target DLLs. If this bit is set, the DLL bypass mode is enabled. This mode is intended to be used only for debug. When set to 0, a Controller operational mode is selected, when set to 1 the Bypass mode is selected. 

DLL works in normal mode of operation where the target delay line settings are used as fractional delay of the controller delay line encoder reading of the number of delays in one cycle. 

Master DLL is disabled with only 1 delay element in its delay line. The target delay lines decode delays in absolute delay elements rather than as fractional delays. 

- DLL Bypass Mode (follow only if operating in this mode): 

   - Depending on frequency of reference clock, calculate how many delay elements should be used to shift this clock by 25% of its period (best case for DDR transfers from setup/hold timings standpoint). Note that delay could be slightly different in a real design. TX Delay is configured in OSPI_PHY_CONFIGURATION_REG[22-16] PHY_CONFIG_TX_DLL_DELAY_FLD bit field. 

   - Re-synchronize DLLs by asserting OSPI_PHY_CONFIGURATION_REG[31] PHY_CONFIG_RESYNC_FLD bit (If this bit is already set by previous re-synchronization, toggle sequence from "0" to "1" must be generated in order to trigger re-synchronization DLL logic) and set PHY bypass mode enable through OSPI_PHY_MASTER_CONTROL_REG[23] PHY_MASTER_BYPASS_MODE_FLD bit. 

- DLL Master Mode (follow only if operating in this mode): 

   - Drive DLL reset bit OSPI_PHY_CONFIGURATION_REG[30] PHY_CONFIG_RESET_FLD into low. 

   - Calculate initial delay value for the Master DLL according to the OSPI_PHY_MASTER_CONTROL_REG[6-0] PHY_MASTER_INITIAL_DELAY_FLD bit field. 

   - Depending on frequency of reference clock, calculate how many delay elements should be used to shift this clock by 25% of its period (best case for DDR transfers from setup/hold timings standpoint). Note that delay could be slightly different in a real design. TX Delay is configured in OSPI_PHY_CONFIGURATION_REG[22-16] PHY_CONFIG_TX_DLL_DELAY_FLD bit field. 

   - Re-synchronize DLLs by asserting OSPI_PHY_CONFIGURATION_REG[31] PHY_CONFIG_RESYNC_FLD (If this bit is already set by previous re-synchronization, toggle sequence from "0" to "1" must be generated in order to trigger re-synchronization DLL logic) and set DLL reset bit back to high (since both bits are within the same register, it is acceptable to set both bits simultaneously). 

   - Poll OSPI_DLL_OBSERVABLE_LOWER_REG[15] DLL_OBSERVABLE_LOWER_LOOPBACK_LOCK_FLD bit. When set – lock is done. 

   - Re-synchronize Target DLLs by asserting OSPI_PHY_CONFIGURATION_REG[31] PHY_CONFIG_RESYNC_FLD bit (If this bit is already set by previous re-synchronization, toggle sequence from "0" to "1" must be generated in order to trigger re-synchronization DLL logic) and set TX DLL Delay (OSPI_PHY_CONFIGURATION_REG[22-16] PHY_CONFIG_TX_DLL_DELAY_FLD) 

1464 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

and RX DLL Delay (OSPI_PHY_CONFIGURATION_REG[6-0] PHY_CONFIG_RX_DLL_DELAY_FLD) fields which are equivalent to percentage clock offsets now. It is recommended to wait for the new configuration being propagated by 20 reference clock cycles before triggering the next SPI transfer. 

   - Consider Read Data from location where its value is predictable. This step can be performed in different ways, depending on the device. Parameter Page, ID, Status, Data from OTP region or Data from location of Flash Array the value of which is known can act as the pattern. 

   - Trigger Read request chosen from above options. 

   - Check correctness of data and store that information: 

      - Increment value of RX clock delay – it is configurable in the OSPI_PHY_CONFIGURATION_REG[6-0] PHY_CONFIG_RX_DLL_DELAY_FLD bit field. 

      - Re-synchronize DLLs. 

      - Trigger valid Read request. 

      - Check correctness of data and store information. 

      - If range boundary of RX clock delay is achieved, go to step 3. Otherwise go back to step "Increment value of RX clock delay". 

3. Set RX clock delay value for one from the middle of valid range based on information in storage. 4. Re-synchronize DLLs. 

5. Set OSPI_DEV_INSTR_RD_CONFIG_REG for Octal Read DDR Configuration (each transfer phase should be configured to work in Octal mode, Number of Dummy cycles should be set as specified in the documentation of the device or more when because of additional read paths delays of actual systems data is predicted to be flopped by PHY module with delay excesses actual cycle of SPI clock generated by the controller). 

6. Enable Pipeline mode in the OSPI_CONFIG_REG[25] PIPELINE_PHY_FLD bit. 

7. Perform Sequential Read of Data consistent with conditions indicated within Section 13.3.2.2.5.4.16.1, _PHY Pipeline Mode_ . 

8. After de-asserting the data target select signal by software – poll OSPI_CONFIG_REG[31] IDLE_FLD bit. 

9. When it is asserted to high – next transfer request can be triggered. 

## _**13.3.2.2.5.4.16.1 PHY Pipeline Mode**_ 

This mode is used for Direct Read Mode of operation. If any other operations are intended to be executed, it is recommended to disable PHY Pipeline Mode and re-enable for subsequent Direct Reads in PHY mode. Since there is comprehensive software mechanism controlling Read data transfers in Indirect Mode, pipeline of data interface accesses is not effective for this mode. Enable PHY Pipeline feature when at least four 4-byte-sized data words are predicted to be read in sequentially. The Flash Command Generator pipelines and puts them into TX FIFO which causes CS to remain active because low level SPI protocol controller controls TX FIFO fill level. In order to correctly trigger Direct Read in Pipeline Mode TX FIFO must be empty. Therefore first polling of OSPI_CONFIG_REG[31] IDLE_FLD bit needs to be done. The sequential data transfer will be interrupted when the data target select signal of the data interface is asserted to low. This information is also detected by Data Target Module which informs the Flash Command Generator that the next access is invalid and a TX FIFO locations can be flushed transparently for the system. 

In PHY Pipeline Mode it is recommended for Data Controller not to introduce wait states in between consecutive occurrences of the data interface signal that indicates transfer has finished. It will ensure regular transfer rate on data side. Introducing wait states gradually slows data transfer rate down and may finally cause SPI transfer interruption because of TX FIFO data starvation. The system, however, may need to introduce some number of wait states after completion of sequential transfer (composed of 4-byte sized data words) for progressing the data. The dedicated buffer is implemented in Data Target Controller which collects all incoming data during wait states injection. In order to keep SPI transfer uninterrupted, number of wait states should be as little as possible. The higher the OSPI_HCLK/ OSPI_RCLK ratio the more wait states can be introduced without SPI transfer interruption. In case the system is able to launch a new transfer before wait states overflow, buffered data transfer to the host will continue. It compensates slowed down transfer by introducing wait states. In case the system is not able to launch a new transfer before wait states overflow, next incoming transfer is considered non-sequential and is executed after all pipelined data is flushed. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1465 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

This mode can be enabled when following conditions are met: 

- OSPI_HCLK > OSPI_RCLK (Comparing the slow data clock with the fast reference one makes Pipeline Mode ineffective – Suspend of SPI Transfer would be possible. Consequently, this condition has to be met to operate in this mode.) 

- Only 4-byte sized Data Words are permitted (This ensures more data clock cycles for synchronization of FIFOs between consecutive pulses of the signal indicating transfer has finished.) 

- The transfer with introduced wait states or non-sequential transfers can only be triggered in between at least four 4-byte sized Data Bursts sequential accesses (16 Bytes) to be sure that Data Controller can trust buffered incoming data during wait states injection. 

- Do not use Pipeline Mode along with Continuous Mode (XIP). Benefit of XIP is limited for bulk data transfers intended to execute in Pipeline Mode. 

## _**13.3.2.2.5.4.16.2 Read Data Capturing by the PHY Module**_ 

Read Data Capturing by the PHY module is useful, as the user is not responsible for the design dedicated DLL being compatible with the Octal-SPI Flash Controller. Another benefit is an option to adjust both SPI clock and sampling clock in a very wide range to fit them into individual requirements of any system. If loopback clock (OSPI_RD_DATA_CAPTURE_REG[0] BYPASS_FLD) and PHY mode (OSPI_CONFIG_REG[3] PHY_MODE_ENABLE_FLD) are both enabled, the loopback clock is driven into RX DLL instead of gated reference clock. Because of the architecture of DLL, loopback clock needs to be provided in SPI Mode 0. If DQS (OSPI_RD_DATA_CAPTURE_REG[8] DQS_ENABLE_FLD) and PHY mode (OSPI_CONFIG_REG[3] PHY_MODE_ENABLE_FLD) are both enabled, the DQS is driven into RX DLL instead of gated reference clock. 

1466 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.2.2.5.5 OSPI Programming Guide**_ 

## _**13.3.2.2.5.5.1 Configuring the OSPI Controller for Use After Reset**_ 

The OSPI controller has been designed to wake up in a state that is suitable for performing basic reads and writes using the direct access controller. The BASIC read (opcode 0x03) and BASIC write (opcode 0x02) instructions are operations supported by all target devices. The controller also wakes up with a baud rate divider setting of divide-by-32. Assuming the reference clock is operating at 400 MHz after reset, then this means the effective SPI clock is just 12.5 MHz. This should be slow enough to meet all timing requirements of all target devices without any further device programming. 

If the target device does not use 3 address bytes, the device size configuration register must be modified to the appropriate size. 

If software plans to write to the device, and the number of bytes per device page is not equal to 256, then the device size configuration register must also be modified. 

While not a requirement, it is prudent for software to enable the write protect feature prior to enabling the OSPI controller. This will block any data writes from taking effect. To do so, the protection registers (OSPI_LOWER_WR_PROT_REG, OSPI_UPPER_WR_PROT_REG and OSPI_WR_PROT_CTRL_REG) should be setup and the number of bytes per device block in the device size configuration register should also be setup. 

After Power-on Reset (POR), software can read from and write to the FLASH device (albeit slowly). Enabling/Disabling the controller and DAC is achieved with just one write to corresponding fields of the OSPI_CONFIG_REG register. User shall take note to maintain the default values of the baud rate divisor and the default state of SEL_CLK_POL_FLD/ SEL_CLK_PHASE_FLD bits of this register. A write data value of 0x00780081 is recommended. 

## _**13.3.2.2.5.5.2 Configuring the OSPI Controller for Optimal Use**_ 

## **Note** 

When using the OSPI Controller, the opcodes in OSPI_DEV_INSTR_RD_CONFIG_REG[7-0] RD_OPCODE_NON_XIP_FLD, OSPI_DEV_INSTR_WR_CONFIG_REG[7-0] WR_OPCODE_FLD and OSPI_WRITE_COMPLETION_CTRL_REG[7-0] OPCODE_FLD bit fields shall not match the opcode in the OSPI_FLASH_CMD_CTRL_REG[31-24] CMD_OPCODE_FLD bit field. 

For high speed transfers PHY mode can be enabled and for optimal configuration PHY Pipeline mode is recommended. For more information, see Section 13.3.2.2.5.4.16.1, _PHY Pipeline Mode_ . 

To access the flash optimally, software must configure the controller accurately: 

1. Wait until any pending STIG or INDAC operation has completed or poll OSPI_CONFIG_REG[31] IDLE_FLD bit. 

2. Disable the DAC through OSPI_CONFIG_REG[7] ENB_DIR_ACC_CTLR_FLD bit. It is permitted, but not necessary to also disable the OSPI controller completely via OSPI_CONFIG_REG[0] ENB_SPI_FLD bit. 

3. Update the OSPI_DEV_INSTR_RD_CONFIG_REG and OSPI_DEV_INSTR_WR_CONFIG_REG registers for the instruction type you wish to use for indirect and direct writes and reads. 

4. Update the OSPI_MODE_BIT_CONFIG_REG[7-0] MODE_FLD bit field if mode bits have been enabled in the OSPI_DEV_INSTR_RD_CONFIG_REG[20] MODE_BIT_ENABLE_FLD bit. 

5. Update the OSPI_DEV_SIZE_CONFIG_REG if the contents are incorrect. Note parts or all of this register may have been updated after initialization. The number of address bytes is a key configuration setting required for performing reads and writes. The number of bytes per page is required for performing any write. The number of bytes per device block is only required if the write protect feature is used. If the default values are correct for the target device, or if some of the values (not including the number address bytes) were incorrect but device writes were not permitted. 

6. Update the OSPI_DEV_DELAY_REG. This register allows the user to tweak how the chip select is driven after each FLASH access. This is required as each device may have different timing requirements. As 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1467 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

the serial clock frequency is increased, these timing requirements become more important. Note the numbers programmed in this register are based on the period of reference clock. Example: A device needs 50ns minimum time before CS can be re-asserted after it has been de-asserted. By default, the controller will only provide a minimum of 1 SCLK period. When the device is operating at 100 MHz, the SCLK period is only 10ns, so 40ns extra is required. Since the register defines the number of reference clock cycles to add, and reference clock is running at 400 MHz (2.5ns period), then the user should program a value of at least 16 to the OSPI_DEV_DELAY_REG[31-24] D_NSS_FLD. This delay can be extended during auto-polling phase. There is possibility to define the polling repetition delay in the OSPI_WRITE_COMPLETION_CTRL_REG[31-24] POLL_REP_DELAY_FLD bit field. 

7. Update the OSPI_REMAP_ADDR_REG register, if required. Affects DAC path only. 

8. Setup and enable write protection registers (OSPI_LOWER_WR_PROT_REG, OSPI_UPPER_WR_PROT_REG and OSPI_WR_PROT_CTRL_REG) if they are required and if they have not already been setup from post initialization. 

9. Enable required interrupts via the OSPI_IRQ_MASK_REG register. 

10. Setup the baud rate divisor in the OSPI_CONFIG_REG[22-19] MSTR_BAUD_DIV_FLD to define the required clock frequency of the target device. 

11. Update the OSPI_RD_DATA_CAPTURE_REG register. This register will delay when the read data is captured and can help when the read data path from the device to the controller is long and the device clock frequency is high. An update to this register may not be necessary. 

12. Enable the OSPI controller and the DAC via the OSPI_CONFIG_REG. 

## _**13.3.2.2.5.5.3 Using the Flash Command Control Register (STIG Operation)**_ 

The OSPI_FLASH_CMD_CTRL_REG register provides software means to access the FLASH device in a flexible and programmable manner. This is known as a STIG operation (Software Triggered Instruction Generator). The instruction opcode, number of address bytes (if any), the address itself, number of dummy cycles (if any), number of write data bytes (if any), the write data itself and the number of read data bytes (if any) can be programmed. Once these have been programmed, software can trigger the command via OSPI_FLASH_CMD_CTRL_REG[0] CMD_EXEC_FLD bit and wait for its acceptance by polling OSPI_FLASH_CMD_CTRL_REG[1] CMD_EXEC_STATUS_FLD bit. When CMD_EXEC_STATUS_FLD bit turns de-asserted, another STIG can be triggered. This method of accessing the FLASH is the typical mechanism that software would use to access the FLASH device’s registers, as well as for performing ERASE operations. It can also be used to access the FLASH array itself, although the maximum of 8 data bytes may be read or written at any one time, defined in the Flash Command Write and Read Data registers (OSPI_FLASH_RD_DATA_LOWER_REG, OSPI_FLASH_RD_DATA_UPPER_REG, OSPI_FLASH_WR_DATA_LOWER_REG and OSPI_FLASH_WR_DATA_UPPER_REG). This number of bytes can be extended for Read Data commands using additional STIG 

Memory Bank controlled by OSPI_FLASH_CMD_CTRL_REG[2] STIG_MEM_BANK_EN_FLD and OSPI_FLASH_COMMAND_CTRL_MEM_REG. 

Commands issued using this interface have a higher priority than all other READ accesses coming from data interface, and will therefore interrupt any READ commands being requested by the indirect or direct controllers. 

1468 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.2.2.6 Firmware Upgrade Over the Air (FOTA) Accelerator**_ 

This section describes the Firmware Upgrade Over the Air (FOTA) Accelerator module for the device. 

## _**13.3.2.2.6.1 FOTA Overview**_ 

**==> picture [469 x 265] intentionally omitted <==**

**----- Start of picture text -----**<br>
Data Interface<br>Data<br>OTFA ECCM OSPI<br>Config<br>WRITE  BUS ACCESS<br>BUFFER LOGIC<br>JTAG<br>FOTA status interrupt Config<br>FOTA MCU<br>FOTA error interrupt<br>FOTA<br>MMR<br>PROGRAM  DATA<br>MEM. MEM.<br>CFG CBASS<br>Config Interface<br>**----- End of picture text -----**<br>


**Figure 13-157. FOTA Accelerator Block Diagram** 

FOTA Accelerator includes a FOTA HW ENGINE and supporting logic to provide configuration and data interface access to flash Controller (OSPI). This can be used by firmware running on the FOTA HW ENGINE to support FOTA firmware update while XIP is active. Purpose for FOTA support in hardware is to simplify software complexity associated with coordinating processes running in multiple CPUs and to reduce XIP downtime during FOTA write. This enables to perform concurrent XIP read(s) while FOTA update happen in background, with zero software overheads on processor cores. Primarily this is useful when using Read While Write (RWW) capable flash memory, which allows reads while write/erase is in progress (which can take >1ms to complete) in a different bank . 

## **Note** 

Read While Write (RWW) flash devices provide the ability to read from a given flash array while write is in progress in a different flash array. This could be partitioned by flash device as banks, where read from all banks are allowed except for the one bank that has write in progress. Alternatively, this could be partitioned using chip select, where read from all chip selects are allowed except for the chip select that has write in progress 

Figure 13-157 provides an overview of the FOTA Accelerator logic. This logic fits before the OTFA and ECCM blocks on the data path and between Config CBASS and OSPI on the configuration path. 

FOTA supporting logic includes bus access logic for arbitrating configuration accesses between FOTA HW ENGINE and SOC to OSPI configuration registers and data accesses between FOTA HW ENGINE and SOC to data path to flash. It also includes a 512-byte FOTA write buffer for storing one page of updated image for writing to flash. SOC writes the updated FOTA firmware to this memory through the configuration interface. FOTA HW ENGINE will move data from this write buffer to flash after arbitration and gaining access to data interface. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1469 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

FOTA write (using FOTA HW ENGINE) through OTFA protected address range and/or ECCM protected address range is NOT supported. FOTA write uses region 3, bypassing OTFA and ECCM regions. Thus, safety and security measures have to be taken accordingly, outside the FSS module, to ensure there is no system compromise. Also, FOTA_ADDR register has to be setup to use the actual physical address in flash. Memory Address Translation provides memory address translation information and how to pack MAC, data and ECC 

FOTA functionality is configured and managed through FOTA MMR region (FOTA_GENREGS Registers) accessible through FSS config interface. 

The FOTA HW ENGINE firmware is stored in a 2KB internal program memory (RAM). Also, an internal 256-byte data memory (RAM) is included for storing variables, context stack etc. These two memories are accessible through the 32-bit FSS config interface for preloading by system firmware. Due to limited space in the FOTA HW ENGINE program memory, firmware is expected to be specific to a given flash memory and is not intended to be a superset code covering all flash devices. 

The FOTA HW ENGINE also includes debug functionality in a submodule called OCI (On-Chip Instrumentation). This debug logic can be accessed through JTAG, which is directly exported out of FSS for SOC level connectivity. 

The FOTA HW ENGINE firmware provides FOTA completion status by writing to the IRQ status registers (FOTA_GENREGS_IRQ_STATUS_RAW) in FOTA MMR. It also gives out interrupts for FOTA completion status and error status. 

1470 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.2.6.2 FOTA High Level Sequence**_ 

**==> picture [490 x 440] intentionally omitted <==**

**Figure 13-158. FOTA Accelerator Flow Chart** 

Figure 13-158 shows the high-level sequence that can be followed by the SOC CPU and FOTA HW ENGINE firmware, for implementing FOTA writes using OSPI Controller. 

The first flowchart shows the SOC software and the second flowchart shows the FOTA HW ENGINE firmware flow described as follows: 

1. SOC CPU configures OSPI Controller based on required settings. This includes setting up DAC and/or INDAC modes in OSPI and setting up various flash parameters like dummy cycles etc. 

2. SOC CPU configures FOTA accelerator using FSAS_FOTA_GENREGS region. This includes setting up interrupt enables and general-purpose registers which have firmware defined interpretation (can contain FOTA write address etc.). 

3. SOC CPU brings the FOTA HW ENGINE out of reset by clearing _FOTA_INIT.reset_ , _FOTA_INIT.clkdis_ , and _FOTA_INIT.mem_access_ bits in FSAS_FOTA_GENREGS region. 

4. SOC CPU/DMA transfers up to one page of data into FOTA write buffer (WBUF_GENREGS Register ). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1471 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

5. SOC CPU sets _FOTA_CTRL.go_ bit to indicate that FOTA HW ENGINE can start FOTA writes. Once this is set, SOC CPU refrains from accessing OSPI Controller configuration space. This is recommended because the FOTA HW ENGINE will periodically access configuration bus (thereby blocking access to SOC) in order to write and read OSPI registers. 

6. FOTA HW ENGINE takes control of configuration and data interfaces, using bus access logic, according to arbitration rules defined in firmware. Any new data or configuration requests from the SOC are held. Also, any pending transactions on the interfaces are complete and the control switches to the FOTA. Thus, the ongoing XIP is paused. 

7. FOTA HW ENGINE firmware configures the OSPI Controller for the write transaction. This is mainly for changing any settings required for writes (for example disabling PHY pipeline mode). 

8. FOTA HW ENGINE firmware transfers data from FOTA write buffer to flash. 

9. FOTA HW ENGINE firmware polls for data transfer completion status to make sure the data has been transferred from OSPI to flash, and the OSPI data lines are now idle. 

10. FOTA HW ENGINE firmware then reverts back the OSPI Controller configuration settings (for example re-enabling PHY pipeline mode). 

11. FOTA HW ENGINE then relinquishes control of configuration and data interfaces. Thus, XIP can now resume. 

12. If flash polling is not implemented by FOTA HW ENGINE firmware, steps 12 through 20 are skipped. 

13. FOTA HW ENGINE firmware uses internal FOTA HW ENGINE timer to periodically poll flash status for write completion. 

14. When timer elapses, FOTA HW ENGINE firmware takes control of configuration and data interfaces. Any new data or configuration requests from the SOC are held. Also, any pending transactions on the interfaces are complete and the control switches to the FOTA. Thus, the ongoing XIP is paused. 

15. FOTA HW ENGINE firmware configures the OSPI Controller for the status read transaction. 

16. FOTA HW ENGINE firmware issues STIG command to OSPI Controller to read flash status. 

17. FOTA HW ENGINE firmware polls for STIG command completion. 

18. FOTA HW ENGINE firmware then reverts back the OSPI Controller configuration settings. 

19. FOTA HW ENGINE firmware relinquishes control of configuration and data interfaces. Thus, XIP can now resume. 

20. After reading the flash status, if it indicates that the write is in progress, FOTA HW ENGINE firmware repeats steps 13 through 19. 

21. Once, the page write is completed, FOTA HW ENGINE firmware reports status back to SOC CPU. This can be done using interrupt or polling by SOC CPU. 

22. If more pages have to be written to flash, the FOTA sequence can be repeated. 

23. SOC CPU puts FOTA HW ENGINE back to reset and clock disabled state by writing to _FOTA_INIT_ register in FSAS_FOTA_GENREGS region. 

## _**13.3.2.2.6.3 Programming Considerations for FOTA**_ 

1. **FOTA Logic Power saving** : All FOTA logic except FOTA MMR can be clock gated when FOTA logic is not used. By default, the clock to FOTA logic is enabled to make it easier for loading the firmware etc. However, during initialization, software can enable clock gating by setting _FOTA_INIT.clkdis_ MMR bit in FSAS_FOTA_GENREGS region. Software needs to enable clocks during FOTA sequence and disable them after FOTA sequence is done. This will ensure the logic is not consuming unnecessary power. 

2. **OSPI Controller Autopolling** : Read While Write (RWW) flash devices allow read access while write in a different bank is ongoing. Please note that if auto polling is enabled, OSPI Controller will block read access until flash write is fully complete. As a result, auto polling has to be disabled in OSPI Controller in order to utilize RWW capability of the flash. Auto polling can be performed by FOTA firmware if required. 

## **Note** 

TI will provide the FOTA MCU firmware binary as part of SDK offering. Please contact a TI representative for the same. 

1472 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.2.2.7 On the Fly Encryption and Authentication (OTFA)**_ 

This section describes the On the Fly Encryption and Authentication (OTFA) module for the device. 

## _**13.3.2.2.7.1 OTFA Overview**_ 

OptiFlash provides a Security Engine with in-line encryption/decryption/Authentication (AES/GCM) on flash data to enable secure external flash use. It supports on-the-fly address translation to provide SW transparent view to account for additional storage of MAC (Message Authentication Code). The MAC size is programmable. 

## _**13.3.2.2.7.1.1 Features Supported**_ 

This module supports the following features: 

- 4 Crypto regions each having unique 

   - Encryption modes supported are: Disabled, AES-CTR, AES-ECB+ 

   - Authentication modes supported are: Disabled, GMAC, and CBC-MAC 

   - Key Encryption key size of 128 or 256 bits 

   - Key Authentication key size of 128 bits 

   - IV seed of 128 bits 

   - Start Physical Address 

   - Size, upto 4G 

   - Start Physical Address and Size, aligned to 4 KByte boundary 

   - MAC Start Physical Address 

   - All return status/read data will be in order 

   - If OTFA is disabled, then OTFA block will consume 0 clock 

      - It can be disabled by efuse or by SW via MMR configuration bit. Note reset state is disabled. 

- Illegal OCP Transaction Detection 

- Easy SW configuration 

## _**13.3.2.2.7.1.2 Features Not Supported**_ 

This module does not support the following features 

- 192 Bit AES Key 

- Key updates during active transaction 

- OCP 2-dim transaction 

- Overlapping crypto regions 

- AES core is not DPA compliant 

- Unaligned access to 32Byte boundary 

- OTFA max burst size is 32 Bytes, so greater than 32Bytes is Not supported 

- OTFA return responses/rd data is in strict order 

- OTFA does NOT allow concurrent active Read and Writes, it must be idle before you switch times. 

## _**13.3.2.2.7.2 OTFA Functional Description**_ 

## _**13.3.2.2.7.2.1 Authentication Operations**_ 

## **Write Transactions** 

For Write transactions, for every 32Bytes of Data a 4/8/12/16 Byte MAC/TAG is generated and posted to the EMIF. 

Only 32byte aligned Write transactions are allowed. 

## **Read Transactions** 

A RdMod transaction will be issued if one of the following conditions is true: 

1. Start Address is not on a 32Byte boundary, 0x00, 0x20, etc 

2. End Address is not on a 32Byte boundary, 0x00, 0x20, etc 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1473 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

3. The size of the transaction is not a multiple of 32Bytes 

If any the above conditions are true, then a Modified Rd operation will get issued to make it compliant. Note this Rd data will get authenticated. 

## **False MAC Errors** 

In order for the MAC authentication to be valid a compliant Wrt operation must occur before the compliant Rd op for that address location. If this does not occur then a MAC Error event will get issued. 

The following conditions will create a False MAC Error: 

1. A compliant Rd op , but location was not written prior to this op. 

2. A none compliant Rd op or a Modify Rd op read a location which was not written prior to this op. 

Examples of False MAC Errors are: 

1. CPU prefetch issue a Rd op that is beyond the written code space. 

2. Data Rd op to uninitialized location 

## _**13.3.2.2.7.2.2 AES Operations**_ 

AES Operations require the following inputs: 

1. Address of data word(from the command or calculated for burst command). 

2. AES mode along with the Key size, Key and IV. 

3. RD or WRT transaction type. 

The AES operation produces a data word which is encrypted or decrypted. The MAC operation produces a MAC for Read and Write operations. 

The table below (Table 13-201) defines the possible combinations of Encryption modes and Authentication modes. A total of 9 combinations are possible, but not all of them are supported. 

## **Note** 

GCM is AES-CTR + GMAC and CCM is AES-CTR + CBC-MAC. 

**Table 13-201. Modes of Operation** 

|**Modes of operation defined by RegionCfg<n>**<br>|**Modes of operation defined by RegionCfg<n>**<br>|**Encryption modes**|**Encryption modes**|**Encryption modes**|
|---|---|---|---|---|
|**register**||**Disable**|**AES-CTR**|**AES-ECB+**|
|**Authentication modes**|**Disable**|Supported|Supported|Supported|
||**GMAC**|Supported|Supported|Not Supported|
||**CBC-MAC**|Not Supported|Supported|Not Supported|



## **Note** 

1. "Encryption Only" modes are not shown, they are the same as Encryption + Authentication mode expect Authentication operation is removed. 

2. Address used for MAC operation is the MAC Address not the data Address. 

The figures below show the different modes of operation: 

## _**13.3.2.2.7.2.3 Modes of Operation**_ 

This section describes the different modes of operation: 

1. GCM (Encryption + Authentication generation ) 

2. GCM (Decryption + Authentication verification ) 

3. GMAC (Authentication generation only ) 

1474 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

4. GMAC (Authentication verification only ) 

## _**13.3.2.2.7.2.3.1 GCM (Encryption + Authentication generation )**_ 

**==> picture [473 x 440] intentionally omitted <==**

**----- Start of picture text -----**<br>
Counter Mode Encryption(CTR)<br>Ive/Adr<br>INCR<br>Ke AES Ke AES Ke AES<br>PT Low<br>PT High<br>CT Low CT High<br>Message Authentication Code(MAC)<br>Ka<br>Ka<br>GHASH GHASH<br>Write MAC<br>**----- End of picture text -----**<br>


**Figure 13-159. GCM (Encryption + Authentication generation )** 

- **INPUTS** 

   - IVe (Initialization vector E) - 16 Bytes {Nonce (16 Bytes) Xor Address} 

   - Ke (Key Encryption) - 16 Bytes / 32 Bytes 

   - PT-Low (Plain Text Low) - 16 Bytes 

   - PT-High (Plain Text High) - 16 Bytes 

   - Ka (Key Authentication) - 16 Bytes 

- **OUTPUTS** 

   - CT-Low (Ciphertext Low) - 16 Bytes 

   - CT- High (Ciphertext High) - 16 Bytes 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1475 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- 

- Write MAC (Write Message Authentication Code) - 4 Bytes 

## **Note** 

Nonce is SW loaded value seeded optionally from TRNG as part of Boot-UP 

## _**13.3.2.2.7.2.3.2 GCM (Decryption + Authentication verification )**_ 

**==> picture [472 x 512] intentionally omitted <==**

**----- Start of picture text -----**<br>
Counter Mode Encryption(CTR)<br>Ive/Adr<br>INCR<br>Ke AES Ke AES Ke AES<br>CT Low<br>CT High<br>PT High<br>PT Low<br>Message Authentication Code(MAC)<br>Ka Ka<br>GHASH GHASH<br>READ MAC<br>WRITE MAC<br>COMPAREWrite MAC<br>MAC ERROR<br>**----- End of picture text -----**<br>


**Figure 13-160. GCM (Decryption + Authentication verification )** 

- **INPUTS** 

   - IVe (Initialization vector E) - 16 Bytes {Nonce (16 Bytes) Xor Address} 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1476 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

   - Ke (Key Encryption) - 16 Bytes / 32 Bytes 

   - CT-Low (Ciphertext Low) - 16 Bytes 

   - CT-High (Ciphertext High) - 16 Bytes 

   - Ka (Key Authentication) - 16 Bytes 

   - Write MAC (Write Message Authentication Code) - 4 Bytes 

- **OUTPUTS** 

   - PT-Low (Plain Low) - 16 Bytes 

   - PT- High (Plain High) - 16 Bytes 

   - MAC Error 

## **Note** 

Nonce is SW loaded value seeded optionally from TRNG as part of Boot-UP 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1477 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.2.7.2.3.3 GMAC (Authentication generation only )**_ 

**==> picture [443 x 446] intentionally omitted <==**

**----- Start of picture text -----**<br>
Message Authentication Code(MAC)<br>Ive/Adr<br>Write D High<br>Ke AES<br>Write D Low<br>Ka GHASH Ka GHASH<br>Write MAC<br>**----- End of picture text -----**<br>


## **Figure 13-161. GMAC (Authentication generation only )** 

- **INPUTS** 

   - IVe (Initialization vector E) - 16 Bytes {Nonce (16 Bytes) Xor Address} 

   - Ke (Key Encryption) - 16 Bytes / 32 Bytes 

   - Ka (Key Authentication) - 16 Bytes 

   - Write D-Low (Write Data Low) - 16 Bytes 

   - Write D-High (Write Data High) - 16 Bytes 

   - Ka (Key Authentication) - 16 Bytes 

- **OUTPUTS** 

   - Write MAC (Write Message Authentication Code) - 4 Bytes 

1478 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Note** 

Nonce is SW loaded value seeded optionally from TRNG as part of Boot-UP 

## _**13.3.2.2.7.2.3.4 GMAC (Authentication verification only )**_ 

**==> picture [443 x 454] intentionally omitted <==**

**----- Start of picture text -----**<br>
Message Authentication Code(MAC)<br>Ive/Adr<br>Ke AES Read D High<br>Read D Low<br>Ka GHASH Ka GHASH<br>Write MAC COMPARE<br>MAC Error<br>**----- End of picture text -----**<br>


**Figure 13-162. GMAC (Authentication verification only )** 

- **INPUTS** 

   - IVe (Initialization vector E) - 16 Bytes {Nonce (16 Bytes) Xor Address} 

   - Ke (Key Encryption) - 16 Bytes / 32 Bytes 

   - Read-Low (Read Data Low) - 16 Bytes 

   - Read-High (Read Data High) - 16 Bytes 

   - Ka (Key Authentication) - 16 Bytes 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1479 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

   - Write MAC (Write Message Authentication Code) - 4 Bytes 

- **OUTPUTS** 

   - MAC Error 

## **Note** 

Nonce is SW loaded value seeded optionally from TRNG as part of Boot-UP 

## _**13.3.2.2.7.3 OTFA Programming Model**_ 

## **Initialization** 

The following procedure is required to get OTFA operational for cryptographic functionality. 

After a reset event, the follow procedure is required. 

1. Program RegionCfg<n>, RegionMacStart<n>, RegionStart<n>, RegionSize<n>, RegionKeyE<n>, RegionKeyA<n>, RegionIV<n> 

2. Program CryptoCfg 

3. Enable cryptographic functionality, by setting CryptoCfg. _MasterEnable_ bit 

## **Note** 

Ensure NO EMIF/OTFA transactions should be active when you set this bit, this should be done before EMIF/OTFA is operational 

## **Operational Adjustments** 

The SW can make adjustments to the OTFA configuration when it is enabled if it follows a strict protocol. 

The OTFA scheduler does not support on the fly adjustments. Software will need to insure that these adjustments have no impact on current operations and near future operations by following the defined procedure. 

Stop all transactions by external methods 

1. Stop all new transactions to the EMIF/OTFA by adjusting the firewall or other methods 

2. Monitor CryptoStatus. _Busy_ wait until cleared. 

3. SW is now allowed to adjust the OTFA configuration. 

4. Enable new transactions to the EMIF/OTFA 

## **Interrupt Description** 

MAC_ERR[N] will get set when a MAC compare error event occurs for region [N] during a read operation. 

WRITE_ERR[N] will get when write transaction occurs when write_protection is set for region [N]. REGION_BV[N] will get set by one of the 3 possible source events. 

1. A transaction which start in Non-Crypto Region and end in a region [N] will be treated like a Non-Crypto Region only. 

2. A transaction which start in Region [N] and end in a region M will be treated like the Region N only. 

3. A transaction which start in Region [N] and end in Non-Crypto Region will be treated like the Region N only. 

CTR_WKV[N] will get set when OCP Write transaction violates the AES CTR mode write rule. 

1480 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.3.2.2.8 Error Correction Code (ECC) and Safety**_ 

This section describes the Error Correction Code (ECC) module for the device. 

## _**13.3.2.2.8.1 ECC Overview**_ 

OptiFlash provides a Safety Engine with in-line ECC insertion during write and checking/correction during read to provide safety and reliability with external flash. It supports on-the-fly address translation to provide SW transparent view to account for additional storage of ECC data bytes. 

## _**13.3.2.2.8.1.1 Features Supported**_ 

- The ECCM module can protect up to four regions of memory with ECC. 

- Single error correct double error detect algorithm is implemented. 

- Each 32 Bytes data is protected by 4 SECDED Bytes. 

- Each region start address has to be 4K aligned. 

- Region size has to be a 4K multiple. 

- Single transaction cannot cross 4K boundary, it is not allowed for single transaction to cross from one ECCM region to another. 

- The ECCM is calculated on either 32byte or 36 byte blocks with or without the block address. Adding the block address provides the ability to deal with bit hits in the serial interface. 

- The ECCM module formats the block data from the OTFA_L, generates ECC codes, packs MAC+Data+ECC, reformats the address and sends this to FLASH controllers. 

## _**13.3.2.2.8.1.2 ECCM Address Translation**_ 

When either authentication and/or ECCM is enabled, the address provided to the FSS in VBUSM region 0 and 1 will be translated. The translation will occur regardless of whether the incoming VBUSM address falls within the regions protected by MAC or ECCM. So for example if you enable ECCM, 4 bytes of every 32 bytes is reserved for ECC even if no ECCM regions are defined. 

## _**13.3.2.2.8.2 ECCM Calculation**_ 

The ECCM calculation is generated or checked on concatenated structure {1'b0,block_address[26:0], MAC_Auth_Word[127:0], Word1[127:0],Word0[127:0]} broken into four 103 bit chunks stored in the ECCM word. That is the ECCM word has four 8 bits values that each check a 103 bit segment of the concatenated structure. 

The 103 bit portion uses a standard seven bit ECCM calculation plus a parity bit. 

The word0 is the first 128 bit word of a block and the word1 is the second 128 bit word of a block. 

The block_address[26:0] is the upper 27 bits of the requested byte address known as the block address. This is the untranslated address input of the ECCM module. 

If the Authentication is not within this region, the MAC_Auth_Word is assumed zero. 

MAC_Auth_Word is always 128-bits regardless of MAC size. If MAC size of 4, 8, or 12 bytes is used, the remaining most significant bits in MAC_Auth_Word are padded with zeroes. 

If the _ecc_disable_adr_ is set, the block_address is assumed zero so as to not affect the ECCM calculation. 

If the ECCM detectes a double error, the _rstatus_ of 3'd4 is reported and the returned _data_ is cleared. If the bus _EMUDBG_ signal is set, the _rstatus_ is zeroed, but returned data (rdata) is still cleared. 

Both Single Correct and Double error detect are reported as ecc_error_1bit and ecc_error_2bit respectively in IRQ_STATUS register and fsas_ecc_intr_err_pend (level) / fsas_ecc_intr_err_req (pulse) interrupts are generated. 

## **Note** 

ecc_error_1bit and ecc_error_2bit are mutually exclusive and only one of these conditions is reported at any time for a given read. However, both of these interrupt flags can be set if single bit error and two bit error are in separate reads. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1481 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.3.2.2.8.3 Modes of Operation**_ 

FSS supports Octal SPI (OSPI) XIP (execute in-place) and block copy. 

ECCM and Security (Encryption/Authentication) are applicable to both XIP and block copy use cases. 

These combinations are supported for each FSAS mode of operation 

## _**13.3.2.2.8.3.1 RD Modes**_ 

- Pure bypass 

- ECCM only 

- Authentication only 

- ECCM + Authentication 

## _**13.3.2.2.8.3.2 WR Modes**_ 

- Pure bypass 

- In Non ECCM and Non Authenticated regions, any write can be processed. 

- In ECCM or Authenticated regions, only 32 byte writes are supported, non 32 byte request are dropped and reported through fsas_ecc_intr_err_pend/req interrupt. Error status is NOT provided on the fss_s0 VBUSM interface. 

## _**13.3.2.2.8.4 Read Operations**_ 

The ECCM block can read any byte or block of bytes. If the region is ECCM protected, the ECCM block reads the block and return the appropriate bytes requested. If not in an ECCM protected region, only the requested bytes are read. 

## _**13.3.2.2.8.5 Memory Address Translation**_ 

The ECCM block stores the Authentication and/or ECCM in the target memory or flash. This creates the need to translate the address from the requester to the target. The translation is fixed for a given target, that is, if a target contains ECCM, the entire target reserves an ECCM data word for each 32 byte block. If a target has only Authentication, the target reserves an Authentication word for each 32 byte block. If the target has both Authentication and ECCM that target reserves up to 5 data words for each 32 byte block. 

1482 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [458 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
ECCM=0 ECCM=1 ECCM=0 ECCM=1<br>AUTH=0 AUTH=0 AUTH=1 AUTH=1<br>A1 A1 A1 A1 A1<br>A(MAC SIZE) A(MAC SIZE)<br>A32 A32 A32<br>A32 + A32 +<br>A36  MAC SIZE  MAC SIZE<br>A36 +<br> MAC SIZE<br>AUTH AUTH<br>Block Data Data<br>Requester<br>Data<br>ECCM<br>ECCM<br>**----- End of picture text -----**<br>


**Figure 13-163. Memory Address Translation** 

So for a given input block address, the target address the block is stored at is dependent on the configured mode and not the region mode. That is, if you have any authentication modes enabled and ECCM enabled, the external block always reserves a MAC word and an ECCM word regardless of whether you are in a region with Authentication or ECCM. The MAC word is only used in regions that are authenticated and the ECCM is only used in regions that have ECCM. 

The target address equation for a given input address is defined as follows. The configuration mode for a given target is not ever expected to change once setup. 

_TargetBlockAddress = InputAddress*((32 + eccm_en*4 + mac_en*(mac_size + 1)*4))/32_ 

**==> picture [19 x 10] intentionally omitted <==**

Number of 64MB Available = (4GB/64MB) * ((32+eccm_en*4 + mac_en*(mac_size+1)*4)/32) 

**==> picture [19 x 10] intentionally omitted <==**

## Where variables: 

- eccm_en = 1 if ECCM is enabled 

- mac_en = 1 if any authentication mode is used by OFTA 

- mac_size = 0/1/2/3 based on MAC size configuration in OFTA 

The following table shows some example configurations and available blocks 

**Table 13-202. ECCM Configurations** 

|**ECCM Mode**|**Authentication Mode**|**MAC Size**|**Target Block Address**|**64MB blocks Available**|
|---|---|---|---|---|
|N|N|N/A|InputAddress/32*32|64|
|Y|N|N/A|InputAddress/32*36|56.8|
|N|Y|4 bytes|InputAddress/32*36|56.8|
|Y|Y|4 bytes|InputAddress/32*40|51.2|
|Y|Y|8 bytes|InputAddress/32*44|46.5|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1483 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-202. ECCM Configurations (continued)** 

|**ECCM Mode**|**Authentication Mode**|**MAC Size**|**Target Block Address**|**64MB blocks Available**|
|---|---|---|---|---|
|Y|Y|16 bytes|InputAddress/32*52|39.3|



It is important to note that if a target is configured to have ECCM or Authentication but not both, the total blocks available is reduced by 11%. That is, 11% of the flash is reserved for Authentication or ECCM data regardless if any regions for ECCM or authentication are used. 

If the target is configured for both ECCM and Authentication (4B MAC), the total blocks are reduced by 20%. That is, 20% of the flash is reserved for Authentication and ECCM regardless if any regions for ECCM or authentication are used. 

## _**13.3.2.2.8.6 ECCM Error Reporting**_ 

The ECCM module reports ECCM check errors (SEC and DED) and VBUSM unaligned write error (address not 32B aligned or size not 32B). The fsas_ecc_intr_err_pend/fsas_ecc_intr_err_req interrupt is issued to report these errors to SOC. 

In addition to providing interrupt, ECCM module contains two stack data structures for providing additional information to software. 

## For ECCM decode errors: 

- ECCM error information is added to a stack. The top of the stack can be read by software using ERR_ECC_BLOCK_ADDR and ERR_ECC_TYPE registers in FSAS MMR space. The stack is popped by setting bit 31 in ERR_ECC_TYPE register to 1'b1. 

- Each location in this stack contains whether the ECCM error is SEC or DED. For SEC error, it indicates whether error occurred in address, MAC, high data word (upper 16-bytes), or low data word (lower 16-bytes). There is a possibility that multiple of these fields could have SEC errors due to partitioning of ECCM input into four partitions with separate ECCM codes for each of the partition. There is also a possibility that SEC error is reported by the stack element, but none of these fields indicate error (since ECC code itself could have one bit error). 

- One entry in ECCM error stack corresponds to one read from flash that had an error. If multiple reads from flash have ECC errors, multiple entries are added to this stack. Up to four entries can be stored in this stack. If this stack becomes full, newer ECCM errors are dropped and stack remains full until popped by software as mentioned above. 

## For write errors: 

- Unaligned VBUSM write error information is added to a second stack. The top of the stack can be read by software using ERR_WRT_TYPE register in FSAS MMR space. The stack is popped by setting bit 31 in ERR_WRT_TYPE register. 

- Each location in this stack contains whether write error occurred due to unaligned address or due to noncontiguous byte enables and the CBA route ID for the host device that caused the write error. 

- One entry in the write error stack corresponds to one write to flash that had an error. If multiple writes to flash have errors, multiple entries are added to this stack. Up to four entries can be stored in this stack. If this stack becomes full, newer write errors are dropped and stack remains full until popped by software as mentioned above. 

Please note that interrupt is generated only when the error condition occurs. That is, ECCM error results in interrupt only when checking ECCM on read return data from flash. Similarly, unaligned VBUSM write error results in interrupt only when ECCM module receives an unaligned VBUSM write. So if there is one more entry in these stack after popping an entry, interrupt is NOT retriggered. Also there is no advanced information available on how many entries are pending in these stack. Software has to pop all entries in the stack when an interrupt occurs using the below sequence considering ECCM error stack as example (but same sequence applies for write error stack): 

1. Read top of the stack using ERR_ECC_BLOCK_ADDR and ERR_ECC_TYPE registers. 

2. Write 1 to bit 31 of ERR_ECC_TYPE register to pop the stack 

1484 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

3. Read bit 31 of ERR_ECC_TYPE register. If this bit is set, that means there is one more entry in the stack, so repeat from step 1 for the next entry. If this bit is clear, there no more entries in the stack 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1485 

Copyright © 2025 Texas Instruments Incorporated 

