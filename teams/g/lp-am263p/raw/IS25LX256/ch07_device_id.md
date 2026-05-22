**…………………………………………………… ……….IS25LX256/128 IS25WX256/128** 

## **7. DEVICE ID DATA** 

The device ID data shown in the tables here is read by the READ ID and MULTIPLE I/O READ ID operations. 

## **Table 7.1 Device ID Data** 

|**Byte#**|**Name**|**Value**|**Assigned by**|
|---|---|---|---|
|**Manufacturer ID ( 1 Byte total)**||||
|1|Manufacturer ID (1 Byte)|9Dh|JEDEC|
|**Device ID ( 2 Bytes total)**||||
|2|Memory Type (1 Byte)|5Ah = 3V|Manufacturer|
|||5Bh = 1.8V||
|3|Memory Density (1 Byte)|19h = 256Mb||
|||18h = 128Mb||
|**Unique ID ( 17 Bytes total)**||||
|4|Indicates the number of remaining ID bytes (1 Byte)|10h|Factory|
|5|Extended device ID (1 Byte)|See below Table 7.2||
|6|Device configuration information (1 Byte)|See below Table 7.3||
|7:20|Customized factory data ( 14 Bytes)|Unique ID code(UID)||



**Table 7.2 Extended Device ID Data, First Byte** 

|**Bit 7**|**Bit 6**|**Bit 6**|**Bit 5**|**Bit 4**|**Bit 3**|**Bit 2**|**Bit 1**|**Bit 1**|**Bit 0**|**Bit 0**|
|---|---|---|---|---|---|---|---|---|---|---|
|Reserved|Device Generation<br>0 = 1st generation||Reserved|Reserved|Reserved|Reserved|Sector Size:<br>**01 = Uniform 128KB**<br>10=Uniform 64KB**(1)**||||
|Note:<br>1. 64KB is for optional device. See the Ordering Information for<br>**Table 7.3 Device Configuration Information Data**||||||optional 64KB sector size.|||||
|**Bit 7**||**Bit 6**|**Bit 5**|**Bit4**|**Bit 3**|**Bit 2**||**Bit 1**||**Bit 0**|
|Reserved||Reserved|Reserved|Reserved|Reserved|Boot up protocol:<br>0 = Boot in SDR x1<br>1=Boot in DDR x8||Reserved|||



36 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 

05/12/2026 

