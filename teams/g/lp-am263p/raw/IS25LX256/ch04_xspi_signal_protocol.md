**…………………………………………………… ……….IS25LX256/128 IS25WX256/128** 

## **4. xSPI Signal Protocol Description** 

xSPI command protocol is for Octal DDR (x8) protocols and Extended SPI (x1) protocol. 

- Octal DDR protocol 

- Traditional Extended SPI protocol 

|**Protocol**|**Command**|**Address**|**Remark**|
|---|---|---|---|
|Octal DDR|2 byte, DDR (Valid byte + Repeated byte)(1)<br>via DQ [7:0]|4-byte only|Command is valid byte and<br>command extension is repeated<br>byte.|
|Extended SPI|1 byte, SDR (Valid byte) via DQ0 only|3 or 4 byte|Defaults 3 byte address mode|



## **Note:** 

**1. The device actually decodes 1[st] byte of valid byte on the rising edge of clock only in command, so repeated byte of command extension becomes dummy byte.** 

ISSI xSPI device supports below operation: 

- Extended SPI mode : 1S-xy-xy operation (x=bit width, y=SDR or DDR) 

   - Command is always sent through DQ0 bit (x1), command with 3-byte address is default. 

   - `o` 1S-1S-1S: Traditional SPI protocol 

   - 1S-1S-8S: Fast Read Octal Output operation and Octal Input Page Program operation 

   - 1S-1D-8D: DDR Fast Read Octal Output operation. 

   - 1S-8S-8S: Fast Read Octal IO operation and Extended Octal IO Page Program operation. 

   - 1S-8D-8D: DDR Fast Read Octal IO operation (exceptional command with 4-byte address only). 

- Octal DDR mode : 8D-8D-8D operation, command with 4-byte address only 

   - Eight IO signals are used during command transfer, address transfer, and data transfer. . All phases are DDR. 

**Note: Minimum transferred data size is 2-bytes in DDR data transfer operation, so the LSB of starting address must be always “0”.(1S-1D-8D, 1S-8D-8D, 8D-8D-8D)** 

9 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 05/12/2026 

**…………………………………………………… ……….IS25LX256/128** 

**IS25WX256/128** 

In 1S-1S-1S mode, bit transfer uses DQ [0] to transfer information from master to slave and DQ [1] to transfer information from slave to master. On each IO, information is placed on the IO line in Most Significant Bit (MSB) to Least Significant Bit (LSB) order within each byte. Sequential command modifier bytes are transferred in highest order to lowest order sequence. Sequential data bytes are transferred in lowest address to highest address order. 

## **Table 4.1 1S-1S-1S Bit Positions** 

|DQ|Command Bits|Command Modifier<br>Bits (address)(1)|Latency|Data Byte 0|Data Byte 1|
|---|---|---|---|---|---|
|0|7, 6, 5, 4, 3, 2, 1, 0|31 (23), 30 (22), … 1, 0|X …|X …|X …|
|1|X …|X …|X …|7, 6, 5, 4, 3, 2, 1, 0|7, 6, 5, 4, 3, 2, 1, 0|
|2|X …|X …|X …|X …|X …|
|3|X …|X …|X …|X …|X …|
|4|X …|X …|X …|X …|X …|
|5|X …|X …|X …|X …|X …|
|6|X …|X …|X …|X …|X …|
|7|X …|X …|X …|X …|X …|



**Note:** 

## **1. 3-byte or 4-byte address is followed.** 

In 8D-8D-8D mode, bit transfer uses eight DQ signals of DQ [7:0]. The LSB of each byte is placed on DQ [0] with each higher order bit on the successively higher numbered DQ signals. Command is composed of valid command byte of bits [7:0]. Command Modifier Bits are composed of command extension byte (repeated byte) and address bytes (4-byte). All transfer is in DDR mode. **Minimum size of transferred Read/Write data is 2 byte (1 word) in DDR mode.** 

**Table 4.2 8D-8D-8D Bit Positions** 

|DQ|Command<br>Bits|Command Modifier Bits<br>(command ext. & address)|Command Modifier Bits<br>(command ext. & address)|Command Modifier Bits<br>(command ext. & address)|Command Modifier Bits<br>(command ext. & address)|Command Modifier Bits<br>(command ext. & address)|Latency|Data Word 0|Data Word 0|Data Word 1|Data Word 1|
|---|---|---|---|---|---|---|---|---|---|---|---|
|0|0|0|24|16|…|0|X …|0|0|0|0|
|1|1|1|25|17|…|1|X …|1|1|1|1|
|2|2|2|26|18|…|2|X …|2|2|2|2|
|3|3|3|27|19|…|3|X …|3|3|3|3|
|4|4|4|28|20|…|4|X …|4|4|4|4|
|5|5|5|29|21|…|5|X …|5|5|5|5|
|6|6|6|30|22|…|6|X …|6|6|6|6|
|7|7|7|31|23|…|7|X …|7|7|7|7|



10 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 

05/12/2026 

