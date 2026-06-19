**…………………………………………………… ……….IS25LX256/128** 

**IS25WX256/128** 

## **2. PIN DESCRIPTIONS** 

|**SYMBOL**|**TYPE**|**DESCRIPTION**|
|---|---|---|
|C|INPUT|**Clock:**Provides timing for the serial interface. Command, address, or data inputs<br>are latched on the rising edge of C. Data is shifted out on the falling edge of C.|
|S#|INPUT|**Chip Select:**The Chip select (S#) pin enables and disables the device operation.|
|RESET#|INPUT|**RESET#:**The RESET# pin is a hardware RESET signal. When RESET# is driven<br>HIGH, the memory is in the normal operating mode. When RESET# is driven LOW,<br>the memory enters reset mode and output is High-Z. If RESET# is driven LOW while<br>an internal WRITE, PROGRAM, or ERASE operation is in progress, data may be<br>lost. Internal Pull-Up.|
|W#(1)|INPUT|**Write Protect:**This input signal is used to freeze the status register in conjunction<br>with the enable/disable bit of the status register. When the enable/disable bit of the<br>status register is set to 1 and W# signal is driven LOW, the status registor nonvolatile<br>bits become read-only and the WRITE STATUS REGISTER operation will not be<br>executed. During the extended-SPI protocol with OCTAL READ/PROGRAM<br>instructions, and during octal DDR protocol, this pin functions an input/output (DQ2<br>functionality).<br>But Dedicated W# ball instead of Vpp ball is available in BGA PKG (C5 ball) as an<br>option. At that time, C4 ball will become DQ2 instead of DQ2/W#.|
|DQ[7:0]|INPUT/<br>OUTPUT|**Serial IO:**Bidirectional signals that transfer address, data, and command<br>information. In extended-SPI protocol, DQ0 functions as an input for command. But<br>address and data transfer on DQ [7:0] depends on the command. Input (address,<br>write data) can be latched on the rising edge of C (SDR) or on both edges of C (DDR).<br>Output data can be shifted out on the falling edge of C (SDR) or on both edges of C<br>(DDR).<br>In Octal DDR protocol, DQ[7:0] always function as I/O, input is latched on both edges<br>of C, and output is shifted out on both edges of C.DQ2 is used also as write protection<br>control.|
|DQS|OUTPUT|**Data Strobe Signal:**Indicates output data valid and is required to support high<br>speed data output. Not necessary required in extended-SPI protocol except to<br>achieve high frequency for specific DDR commands. Used for READ but not for<br>WRITE operations. Configured by nonvolatile and volatile configuration register bit<br>5 at address 00h. When enabled, DQS is driven to ground at S# LOW and until the<br>device is driving output data, in which case DQS toggles to synchronize data<br>output. When not enabled, DQS is not driven.|
|ERR#|OUTPUT|**ECC Error Indication Signal:**<br>Indicates ECC Event occurrence. Open Drain. External Pull-Up is required when<br>using ERR# signal.|
|PSC(1)|INPUT|**Phase Shifted Clock:**Optional 2ndclock to offset DQS signal from main clock (C)<br>PSC feature is available in Octal DDR mode only in BGA PKG as an option.|
|VCC, VCCQ|SUPPLY|**Supply voltage:**Core Power Supply (B4), I/O Power Supply (D1, E4)|
|Vpp|SUPPLY|**Supply voltage:**If Vpp is in the voltage of VPPH, the signal acts as an additional<br>power supply for programming operation, as defined in the Operating Condition<br>table. The Vpp pad will be internally pulled up to VCC, so customer can leave Vpp<br>pin floated if not used.|
|VSS, VSSQ|GROUND|**Ground:**Core Ground (B3), I/O Ground (C1, E5).|
|RFU|-|**Reserved for future use:**Must be left floating.|
|DNU|-|**Do Not Use:**Must be left floating.|



## **Note:** 

**1. Dedicated W# and PSC are supported in the optional device.** 

7 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 

05/12/2026 

