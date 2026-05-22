
![](img/25LX-WX256-128.pdf-0001-00.png)


## **IS25LX256      IS25WX256 IS25LX128      IS25WX128** 

**256/128Mb Serial Flash Memory Octal I/O xSPI (eXpanded Serial Peripheral) Interface with On-CHIP ECC** 

**200MHZ (1.8V), 133MHZ (3.0V)** 

## **DATA SHEET** 

**…………………………………………………… ……….IS25LX256/128 IS25WX256/128** 

## **256/128Mb SERIAL FLASH MEMORY Octal I/O xSPI (eXpanded SPI) with On Chip ECC 200[(5)] MHz (1.8V), 133MHz (3.0V)** 

## **FEATURES** 

- **Industry Standard Serial Interface** 

- IS25LX256: 256Mbit/32Mbyte 

- IS25LX128: 128Mbit/16Mbyte 

- IS25WX256: 256Mbit/32Mbyte 

- IS25WX128: 128Mbit/16Mbyte 

- JEDEC Standard xSPI (eXpanded SPI) compliant 

- Protocol: Extended SPI (1S-xy-xy)[(2)] Octal DDR (8D-8D-8D) 

- **Low Power with Wide Temp. Ranges** 

- Single Voltage Supply IS25LX: 2.70V to 3.60V IS25WX: 1.70V to 2.0V 

- 6 µA Standby Current 

- 1 µA Deep Power Down 

- Temp Grades: Extended: -40°C to +105°C Auto A3 Grade: -40°C to +125°C 

## • **Flexible & Efficient Memory Architecture** 

## • **High Performance** 

- Support clock frequency up to; - IS25WX (1.8V): SDR - 166MHz DDR – 200[(5)] MHz 

- IS25LX (3.0V): SDR /DDR - 133MHz 

- Execute-in-place (XIP) 

- 2-bit Detection and 1-bit Correction per 16-byte boundary (with ECC) 

- Program Array Data CRC/ Address Parity function supported. 

- Optional PSC (Phase Shifted Clock)[ (1)] is supported to put DQS on the center of read data valid window. 

- Data Learning Pattern for training operation 

- More than 100,000 Erase/Program Cycles 

- - **More than 20-year Data Retention** 

## • **Security and Write Protection** 

- Volatile and nonvolatile locking and software write protection for each 128KB sector 

- Password Protection 

- Hardware write protection: nonvolatile bits (BP [3:0] and TB) define protected area size. 

## • **Efficient Read and Program modes** 

## - Input Data Format 

SPI: 1-byte command+3/4 byte Address Octal: 2-byte command+4 byte Address 

- PROGRAM/ERASE SUSPEND operation 

- 128KB Sector Erase[(3)] and 4KB/32KB Subsector Erase 

- 4-Bank Architecture for READ While Ptogram/Erase Operations[(4)] 

- Program 1 to 256byte per Page 

- Dedicated 64-byte OTP area outside main memory 

## • **Hardware Features** 

- C Input : Serial Clock Input 

- DQ0 – DQ7 : Serial Data Input and Output 

- RESET#: Hardware Reset pin 

- DQS: Data Strobe Signal 

- ERR#: Error Indication Signal 

- W# : Optional Write Protection Signal[(1)] 

## • **Electronic signature** 

- JEDEC –standard 3-byte signature 

- Extended device ID: two additional bytes identify device factory options 

## • **Configuration** 

- Boot in SDR x1 

- Boot in DDR x8 

## • **Industry Standard Pin-out & Packages** 

- H = 24-ball TFBGA 6x8mm (5x5 ball array) 

- KGD (Call Factory) 

- Green Package (RoHS Compliant, Halogen-Free) and TSCA Compliant Notes: 

   1. Dedicated W# is supported in optional devices only. 

   2. x= I/O width (x1 or x8), y= SDR or DDR 

   3. 64KB Sector Erase is supported as an option. 

   4. Read while Program/Erase function is supported with option L 

   5. 166MHz when ECC is ON. 

2 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 

05/12/2026 

**…………………………………………………… ……….IS25LX256/128** 

**IS25WX256/128** 

## **GENERAL DESCRIPTION** 

The IS25LX256/128 and IS25WX256/128 Serial Flash memory offer a versatile storage solution with high flexibility and performance in a simplified pin count package. ISSI’s “Industry Standard Serial Interface” Flash is for systems that require limited space, a low pin count, and low power consumption. The device is compliant with JEDEC Standard xSPI (eXpanded Serial Peripheral Interface). 

Nonvolatile and volatile configuration registers enable respective default and temporary settings such as READ operation dummy cycles and wrap modes, memory protection, output buffer impedance, SPI protocol type, and XIP mode. 

Memory is organized as uniform 128KB sectors, 4KB and 32KB subsectors, and 256 byte pages. Optional 64KB sectors are also supported. 

The device includes 64-byte OTP area that can be permanently locked. 

Direct boot in Octal DDR protocol provides high performance and ease of use, enabling communication between host and device without need to configure extended SPI protocol operations. However, the devices still support both extended SPI and Octal DDR protocols to ensure legacy system support and easy migration path. The extended SPI protocol supports address and data transmission on one or eight data lines, depending on the command. 

XIP feature is supported in extended SPI because its commands are sent through DQ0 only. 

Information in octal DDR protocol is always transmitted via eight data lines on both rising and falling clock edges. When accessing cell array (Read/Program), **minimum transferred data size is 2-bytes in DDR mode, so the LSB of starting address must be always “0”.** 

Most legacy x1 SPI commands are supported, but require only one clock cycle because command is latched on both rising and falling edges of the clock. 

## **Address cycles are fixed at 4-byte (32-bit) operations from the flash array in octal DDR protocol.** 

The host does not need to drive DQS during the input operation to the memory. The data input (DQ) to the memory still relies on clock (C) to latch all address and data operations. Most register outputs require dummy clock cycles due to the critical timing from command decoding. With the help of DQS for output data latching, the number of dummy clock is transparent to the host. 

Suspend and resume commands provide the ability to pause and resume PROGRAM/ERASE operations. 

In an optional device (option L), Read while Write operation provides beginning of read operation from one of 3- banks while programming or erase operation is in progress at specific bank, without interruption of program or erase operation. 

There are three type of data integrity check functions: 

- ECC to prevent errors from stored data 

- Address Parity check to prevent address transmission errors in Octal DDR mode only 

- Program array data CRC (Data Parity) to prevent data transmission errors in Octal DDR mode only. 

Optional PSC (Phase Shifted Clock) is supported for Read operation only, to offset DQS signal, phase shifted from main clock (C) for controller to put DQS signal within valid data window in Octal DDR mode only. 

Package, Voltage & Data Transfer Rate vs. Max. Frequency 

|Voltage|SDR|DDR|
|---|---|---|
|1.8V|166MHz|200(1)MHz|
|3.0V|133MHz|133MHz|



**Note:** 

**1. 166MHz when ECC is ON.** 

3 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 

05/12/2026 

**…………………………………………………… ……….IS25LX256/128** 

**IS25WX256/128** 

## **TABLE OF CONTENTS** 

|FEATURES ............................................................................................................................................................ 2|FEATURES ............................................................................................................................................................ 2|
|---|---|
|GENERAL DESCRIPTION .................................................................................................................................... 3||
|TABLE OF CONTENTS ......................................................................................................................................... 4||
|1.|PIN CONFIGURATION ................................................................................................................................... 6|
|2.|PIN DESCRIPTIONS ...................................................................................................................................... 7|
|3.|BLOCK DIAGRAM .......................................................................................................................................... 8|
|4.|xSPI Signal Protocol Description .................................................................................................................... 9|
|5.|SYSTEM CONFIGURATION ........................................................................................................................ 11|
||5.1 BANK/BLOCK/SECTOR ADDRESSES.................................................................................................. 12|
||5.2 SERIAL Flash Discoverable ParameterS ............................................................................................... 14|
|6.|REGISTERS ................................................................................................................................................. 15|
||6.1 STATUS REGISTER .............................................................................................................................. 15|
||6.2 FLAG STATUS REGISTER .................................................................................................................... 18|
||6.3 Internal CONFIGURATION REGISTER ................................................................................................. 19|
||6.4 NONVOLATILE CONFIGURATION REGISTER .................................................................................... 20|
||6.5 VOLATILE CONFIGURATION REGISTER ............................................................................................ 22|
||6.6 SECURITY REGISTERS ........................................................................................................................ 29|
||6.7 NONVOLATILE LOCK BIT AND VOLATILE LOCK BIT SECURITY REGISTERS ............................... 31|
||6.8 PROTECTION MANAGEMENT REGISTER .......................................................................................... 34|
|7.|DEVICE ID DATA ......................................................................................................................................... 36|
|8.|DEVICE OPERATION .................................................................................................................................. 37|
||8.1 Basic Device OPERATION ..................................................................................................................... 37|
||8.2 COMMAND SET SUMMARY ................................................................................................................. 38|
||8.3 SOFTWARE RESET OPERATIONS ...................................................................................................... 41|
||8.4 READ ID Operation................................................................................................................................. 42|
||8.5 READ SFDP OPERATION ..................................................................................................................... 43|
||8.6 READ MEMORY OPERATION .............................................................................................................. 44|
||8.7 WRITE ENABLE/DISABLE OPERATION .............................................................................................. 48|
||8.8 READ REGISTER OPERATION ............................................................................................................ 49|
||8.9 WRITE REGISTER OPERATION ........................................................................................................... 51|
||8.10 CLEAR FLAG STATUS REGISTER OPERATION .............................................................................. 53|
||8.11 PROGRAM OPERATION ..................................................................................................................... 54|
||8.12 ERASE OPERATION ........................................................................................................................... 57|
||8.13 SUSPEND/RESUME Operations ......................................................................................................... 59|
||8.14 ONE-TIME PROGRAMMABLE Operation ........................................................................................... 61|
||8.15 ONE-TIME PROGRAMMABLE Operation ........................................................................................... 62|
||8.16 ADDRESS MODE Operation ................................................................................................................ 63|
||8.17 State Table ............................................................................................................................................ 64|



4 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 05/12/2026 

**…………………………………………………… ……….IS25LX256/128 IS25WX256/128** 

|<br>|**…………………………………………………… ……….IS25LX256/128**<br>**IS25WX256/128**|
|---|---|
||8.18 XIP MODE ............................................................................................................................................ 65|
||8.19 POWER-UP and POWER-DOWN ........................................................................................................ 68|
||8.20 DATA LEARNING PATTERN READ Operation FOR TRAINING (DLPRD) ........................................ 70|
||8.21 ECC OPERATION ................................................................................................................................ 72|
||8.22 PROGRAM ADDRESS Parity CHECK and PROGRAM ARRAY Data CRC CHECK OPERATION ... 73|
||8.23 ERR# SiGNAL OPERATION ................................................................................................................ 74|
||8.24 Clear ERRB Operation ......................................................................................................................... 75|
||8.25 READ WHILE PROGRAM/ERASE OPERATION ................................................................................ 76|
||8.26 Phase Shifted Clock for CENTER ALIGNED DQS in Octal DDR OPERATION .................................. 77|
||8.27 In-Band RESET .................................................................................................................................... 78|
|9.|ELECTRICAL CHARACTERISTICS ............................................................................................................. 80|
||9.1<br>ABSOLUTE MAXIMUM RATINGS(1).................................................................................................. 80|
||9.1 OPERATING Conditions ......................................................................................................................... 80|
||9.2 PIN CAPACITANCE(1)........................................................................................................................... 80|
||9.3 AC TIMING I/O CONDITIONS ................................................................................................................ 81|
||9.4 DC CURRENT CHARACTERISTICS AND OPERATING CONDITIONS .............................................. 82|
||9.5 AC CHARACTERISTICS ........................................................................................................................ 83|
||9.6 PROGRAM/ERASE SUSPEND/RESUME SPECIFICATIONS .............................................................. 94|
|10.|PACKAGE TYPE INFORMATION ........................................................................................................... 95|
||10.1 24-BALL THIN PROFILE FINE PITCH BGA 6x8mm 5x5 BALL ARRAY (H) ....................................... 95|
|11.|ORDERING INFORMATION – Valid Part Numbers ................................................................................ 96|



5 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 05/12/2026 

