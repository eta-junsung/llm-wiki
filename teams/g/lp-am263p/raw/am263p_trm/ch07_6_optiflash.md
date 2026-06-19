<!-- AM263P TRM | 7.6 OptiFlash | 원본 p.933-936 | pymupdf4llm text+tables, images omitted -->

www.ti.com 

_Processors and Accelerators_ 

## **7.6 OptiFlash** 

This section describes the OptiFlash module in the device. 

## _**7.6.1 OptiFlash Overview**_ 

OptiFlash memory technology is a Tl patented technology that enables cost effective and scalable high performance Microcontrollers (MCU) with external flash. AM26x SoC with integrated OptiFlash Technology aims to solve the limitations faced by traditional High Performance MCUs with external Flash by providing hybrid execution from internal SRAM and direct execution from external Flash. This functionality is also referred to as Execute in Place (XIP). XIP's(equipped with Optiflash accelerators) goal is for execution from external Flash to reach the performance of execution from internal SRAM. 

## **OptiFlash Technology - Key HW Components** 

There are two types of Optiflash accelerators as seen in Optiflash Technology – Key Hardware Components diagram 

- RL2_OF Accelerators 

- FSS Accelerators 

## **Figure 7-388. Optiflash Technology – Key Hardware Components** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

933 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [494 x 413] intentionally omitted <==**

**----- Start of picture text -----**<br>
MCU<br>CPU CPU CPU CPU<br>Core 0 Core 1 Core 2 Core 3<br>RL2_OF  RL2_OF  RL2_OF  RL2_OF<br>Accelerators Accelerators Accelerators Accelerators<br>Interconnect<br>FSS Accelerators<br>SRAM<br>Banks<br>Flash Controller<br>External Flash<br>**----- End of picture text -----**<br>


The OptiFlash module has three hardware accelerator submodules inline to the **CPU data path** to improve memory operations performance. 

- RAT - Region Based Address Translation. 

- FLC - Fast Local Copy allowing code in slow access memory to be placed into on-chip SRAM for fast access. 

- RL2 - Remote L2 is an L2 cache with remote cache data storage memory. That is, you can cache the system Flash into the SoC memory system. 

The OptiFlash FSS hardware accelerator also has three submodules inline to the Flash controller and Interface path to improve flash performance. 

- ECC/Safety Engine 

- OTFA - On-The-Fly Authentication 

- FOTA - Firmware upgrade Over The Air 

## _**7.6.2 OptiFlash Components**_ 

## **7.6.2.1 Octal Serial Peripheral Interface (OSPI)** 

On the AM26x SoC, the Octal-SPI (OSPI) flash controller runs at a maximum speed of 133 MHz DDR over 8 data lines. 

934 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

For more information on the OSPI flash controller, see Section 13.3.2.2.5 

## **7.6.2.2 Remote Layer 2 Cache (RL2)** 

OptiFlash supports a Remote L2 controller (RL2) for caching that is customized for optimized flash and application system performance. It can reduce external Flash access by up to 65-95% based on application profile. It acts as a Level 2 cache controller as it provides additional caching - specific to Flash storage - beyond the CPU Core’s L1 caching. The cache is remote, meaning the actual cache memory can be part of any system memory, such as On-chip Memory (remote cache data storage memory) instead of a dedicated cache storage within the controller. The user has flexibility to specify the size of cache based on target application needs. 

Because external flash holds only read-only data, the L2 cache is effectively caching code and read-only data only. 

For more information on the RL2 module, see Section 13.3.2.1.2. 

## **7.6.2.3 Fast Local Copy (FLC)** 

OptiFlash supports a Fast Local Copy (FLC) engine for image download acceleration during boot or run time to enable code download along with CPU execution in parallel. It redirects the CPU access to Flash when the copy is in progress and redirects the access to SRAM when the content is in valid in SRAM, as shown in Figure 7-389. This enables CPU to execute immediately without waiting for the copy to complete. The operation is transparent to CPU, and results in reduced boot time, in order to meet startup time goals similar to an embedded flash and also provide dynamic overlay for run time performance. 

**==> picture [472 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
AM26x MCU<br>Content in<br>Start DMA SRAM<br>CPU Core ‘n’ Address SRAM<br>Address<br>FLC HWA External Flash<br>L1 Cache<br>Check if content in SRAM<br>Content has not reached to SRAM<br>**----- End of picture text -----**<br>


**Figure 7-389. FLC Block Diagram** 

When the CPU requests an address, the FLC HWA looks for the copied address in the internal SRAM, and returns the data corresponding to that address. Otherwise, the data is fetched from the external flash. Because the data is returned from internal SRAM rather than external flash, the fetch time is reduced, thus providing a boost in overall performance. 

For more information on FLC, see Section 13.3.2.1.3. 

## **7.6.2.4 On-the-Fly Authentication (OTFA)** 

On-the-fly encryption and Authentication (OTFA) enables external memory IP protection at runtime during XIP. The device has an option to disable OTFA. For more information on OTFA, see Section 13.3.2.2.7. 

## **7.6.2.5 Region Address Translation (RAT)** 

The Region based Address Translation (RAT) allows segments of the memory map to be relocated to a different address in the system. It is a dynamic address translator for common code (placed in SRAM) instead of duplicated/redundant code across multiple cores that is downloaded to on-chip SRAM during boot-time. 

For more information on RAT, see Section 13.3.2.1.4 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 935 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.6.2.6 Firmware Upgrade Over the Air (FOTA)** 

The Firmware Upgrade Over the Air (FOTA) module is a hardware accelerator that is a component of the OptiFlash technology to schedule reads and writes over the same 8 data lines of the OSPI module. The purpose of this hardware accelerator is to minimize XIP downtime. 

For applications like ADAS,Automotive Gateway,and IndustryAutomation,Firmware Over the Air (FOTA) updates are required toaddress bug fixes and security vulnerabilities.In order to meet the systemcost,a single flash solution isrequired,which would require topause the application execution until the update (firmware download) is completed. To reduce overall down-time of the system during a firmware update,FOTA allows the system toupdate new firmware/software image during concurrent system operation - reading from external flash **(XIP) .** 

**==> picture [466 x 167] intentionally omitted <==**

**----- Start of picture text -----**<br>
AM26x MCU<br>Simple SW FOTA<br>Writer<br>XIP<br>XIP<br>CPU FOTA  Flash  External Flash<br>Update HWA Controller Update (RWW)<br>**----- End of picture text -----**<br>


**Figure 7-390. FOTA Block Diagram** 

Typical FOTA solutions address this problem by performing read while write in software. However, without any hardware support, it becomes complex as it requires complex synchronisation across threads/CPUs, increasing the XIP downtime.With the OptiFlash FOTA Hardware Accelerator IP, as shown in the above figure,it is possible to further reduce the XIP downtime and be able to perform concurrent XIP read(s) while FOTA update happens in the background, with zero software overheads on the MCU.Primarily, this is useful when using Read While Write (RWW) capable flash memory with dual/multiple banks, which allows reads while write/erase is in progress (which can take >1ms to complete) in a different bank. 

For more information on FOTA, see Section 13.3.2.2.6. 

936 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

