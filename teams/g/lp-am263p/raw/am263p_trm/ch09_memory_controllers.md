<!-- AM263P TRM | 9 Memory Controllers | 원본 p.950-951 | pymupdf4llm text+tables, images omitted -->

www.ti.com 

_Memory Controllers_ 

## _Chapter 9_ _**Memory Controllers**_ 

**==> picture [506 x 40] intentionally omitted <==**

This chapter describes the memory controllers in the device. **9.1 Memory Controllers Overview** .................................................................................................................................951 

950 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Memory Controllers_ 

www.ti.com 

## **9.1 Memory Controllers Overview** 

The AM263Px family of devices utilize an integrated On-Chip Static Random Access Memory (OCSRAM). Controllers for external memory sources such as DDR are not included. The key functionality of the OCSRAM module includes: 

- Total of up to 3MB of RAM 

   - Can be used as code and data memory by the R5FSS cores 

   - Can be used as data buffers accessible by EDMA 

- Four 64-bit wide independent banks of size 512KB with 200Mhz operating frequency 

- Accessible by all initiator modules via the CORE_VBUSM interconnect as detailed in _CORE_VBUSM Interconnect_ . 

- Protected with MPU firewalls as detailed in _System Memory Protection Unit (MPU)/Firewalls_ 

- Loadable space for the Secondary Bootloader (SBL) as detailed in Initialization Overview 

- 64-bit ECC Support 

   - Read-Modify-Write mechanism to support ECC update on memory writes less then 64-bits. Read-ModifyWrite operation works independently per bank and requires one additional cycle to update. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

951 

Copyright © 2025 Texas Instruments Incorporated 

