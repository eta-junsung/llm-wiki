**…………………………………………………… ……….IS25LX256/128 IS25WX256/128** 

## **5. SYSTEM CONFIGURATION** 

The device is divided into uniform 128KB sector (or optional 64KB sector), and each sector is divided into 4KB/32KB subsectors. 

In an optional device (option L), the memory array is divided into 4 Banks. The multi bank structure enables Read while Write operation, which means read cell array data from one bank while another bank is in the middle of program/erase operation. 

The Status Register controls how the memory is protected. 

11 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 05/12/2026 

**…………………………………………………… ……….IS25LX256/128 IS25WX256/128** 

## **5.1 BANK/BLOCK/SECTOR ADDRESSES** 

**Table 5.1 Sector/Subsector Addresses (Sector Size = 128KB)** 

|**Memory**<br>**Density**|**Memory**<br>**Density**|**Sector No.**<br>**(128Kbyte)**|**Subsector No.**<br>**(32Kbyte)**|**Subsector No.**<br>**(4Kbyte)**|**Address Range**|
|---|---|---|---|---|---|
|**128Mb**|**256Mb**|Sector 0|Subsector 0|Subsector 0|000000h - 000FFFh|
|||||:|:|
||||Subsector 1|:|:|
|||||Subsector 15|00F000h - 00FFFFh|
||||Subsector 2|Subsector 16|010000h - 010FFFh|
|||||:|:|
||||Subsector 3|:|:|
|||||Subsector 31|01F000h - 01FFFFh|
|||:||:|:|
|||Sector 127|Subsector 508|Subsector 4064|FE0000h – FE0FFFh|
|||||:|:|
||||Subsector 509|:|:|
|||||Subsector 4079|FEF000h – FEFFFFh|
||||Subsector 510|Subsector 4080|FF0000h – FF0FFFh|
|||||:|:|
||||Subsector 511|:|:|
|||||Subsector 4095|FFF000h – FFFFFFh|
|||:||:|:|
|||Sector 255|Subsector 1020|Subsector 8160|1FE0000h – 1FE0FFFh|
|||||:|:|
||||Subsector 1021|:|:|
|||||Subsector 8175|1FEF000h – 1FEFFFFh|
||||Subsector 1022|Subsector 8176|1FF0000h – 1FF0FFFh|
|||||:|:|
||||Subsector 1023|:|:|
|||||Subsector 8191|1FFF000h – 1FFFFFFh|



**Note:** 

**1. Below is the mapping for bank & Sector when Sector size is 128KB in an optional device (option L)** 

||**Bank 0**|**Bank 1**|**Bank 2**|**Bank 3**|**Remark**|
|---|---|---|---|---|---|
|256Mb|Sector 0~63|Sector64~127|Sector 128~191|Sector 192~255||
|128Mb|Sector 0~31|Sector 32~63|Sector 64~95|Sector 96~127||



12 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 05/12/2026 

**…………………………………………………… ……….IS25LX256/128** 

**IS25WX256/128** 

**Table 5.2 Table Sector/Subsector Addresses (Sector Size = 64KB)** 

|**Memory**<br>**Density**|**Memory**<br>**Density**|**Sector No.**<br>**(64Kbyte)**|**Subsector No.**<br>**(32Kbyte)**|**Subsector No.**<br>**(4Kbyte)**|**Address Range**|
|---|---|---|---|---|---|
|**128Mb**|**256Mb**|Sector 0|Subsector 0|Subsector 0|000000h - 000FFFh|
|||||:|:|
||||Subsector 1|:|:|
|||||Subsector 15|00F000h - 00FFFFh|
|||Sector 1|Subsector 2|Subsector 16|010000h - 010FFFh|
|||||:|:|
||||Subsector 3|:|:|
|||||Subsector 31|01F000h - 01FFFFh|
|||:||:|:|
|||Sector 254|Subsector 508|Subsector 4064|FE0000h – FE0FFFh|
|||||:|:|
||||Subsector 509|:|:|
|||||Subsector 4079|FEF000h – FEFFFFh|
|||Sector 255|Subsector 510|Subsector 4080|FF0000h – FF0FFFh|
|||||:|:|
||||Subsector 511|:|:|
|||||Subsector 4095|FFF000h – FFFFFFh|
|||:||:|:|
|||Sector 510|Subsector 1020|Subsector 8160|1FE0000h – 1FE0FFFh|
|||||:|:|
||||Subsector 1021|:|:|
|||||Subsector 8175|1FEF000h – 1FEFFFFh|
|||Sector 511|Subsector 1022|Subsector 8176|1FF0000h – 1FF0FFFh|
|||||:|:|
||||Subsector 1023|:|:|
|||||Subsector 8191|1FFF000h – 1FFFFFFh|



|**Note:**<br>**1. Below is the mapping for bank & Sector when Sector size is 64KB in an optional device (Call Factory)**<br>**Bank 0**<br>**Bank 1**<br>**Bank 2**<br>**Bank 3**<br>**Remark**<br>256Mb<br>Sector 0~127<br>Sector128~255<br>Sector 256~383<br>Sector 384~511<br>128Mb<br>Sector 0~63<br>Sector 64~127<br>Sector 128~191<br>Sector 192~255|**Note:**<br>**1. Below is the mapping for bank & Sector when Sector size is 64KB in an optional device (Call Factory)**<br>**Bank 0**<br>**Bank 1**<br>**Bank 2**<br>**Bank 3**<br>**Remark**<br>256Mb<br>Sector 0~127<br>Sector128~255<br>Sector 256~383<br>Sector 384~511<br>128Mb<br>Sector 0~63<br>Sector 64~127<br>Sector 128~191<br>Sector 192~255|**Note:**<br>**1. Below is the mapping for bank & Sector when Sector size is 64KB in an optional device (Call Factory)**<br>**Bank 0**<br>**Bank 1**<br>**Bank 2**<br>**Bank 3**<br>**Remark**<br>256Mb<br>Sector 0~127<br>Sector128~255<br>Sector 256~383<br>Sector 384~511<br>128Mb<br>Sector 0~63<br>Sector 64~127<br>Sector 128~191<br>Sector 192~255|**Note:**<br>**1. Below is the mapping for bank & Sector when Sector size is 64KB in an optional device (Call Factory)**<br>**Bank 0**<br>**Bank 1**<br>**Bank 2**<br>**Bank 3**<br>**Remark**<br>256Mb<br>Sector 0~127<br>Sector128~255<br>Sector 256~383<br>Sector 384~511<br>128Mb<br>Sector 0~63<br>Sector 64~127<br>Sector 128~191<br>Sector 192~255|**Note:**<br>**1. Below is the mapping for bank & Sector when Sector size is 64KB in an optional device (Call Factory)**<br>**Bank 0**<br>**Bank 1**<br>**Bank 2**<br>**Bank 3**<br>**Remark**<br>256Mb<br>Sector 0~127<br>Sector128~255<br>Sector 256~383<br>Sector 384~511<br>128Mb<br>Sector 0~63<br>Sector 64~127<br>Sector 128~191<br>Sector 192~255|**Note:**<br>**1. Below is the mapping for bank & Sector when Sector size is 64KB in an optional device (Call Factory)**<br>**Bank 0**<br>**Bank 1**<br>**Bank 2**<br>**Bank 3**<br>**Remark**<br>256Mb<br>Sector 0~127<br>Sector128~255<br>Sector 256~383<br>Sector 384~511<br>128Mb<br>Sector 0~63<br>Sector 64~127<br>Sector 128~191<br>Sector 192~255|
|---|---|---|---|---|---|
||**Bank 0**|**Bank 1**|**Bank 2**|**Bank 3**|**Remark**|
|256Mb|Sector 0~127|Sector128~255|Sector 256~383|Sector 384~511||
|128Mb|Sector 0~63|Sector 64~127|Sector 128~191|Sector 192~255||



13 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 05/12/2026 

**…………………………………………………… ……….IS25LX256/128 IS25WX256/128** 

## **5.2 SERIAL FLASH DISCOVERABLE PARAMETERS** 

The Serial Flash Discoverable Parameters (SFDP) standard defines the structure of the SFDP database within the memory device. SFDP is the standard of JEDEC JESD216. 

The JEDEC-defined header with Parameter ID FF00h and related Basic Parameter Table is mandatory. Additional parameter headers and tables are optional. 

14 

_**Integrated Silicon Solution, Inc.- www.issi.com**_ **Rev. A14** 05/12/2026 

