<!-- AM263P TRM | 1 Introduction | 원본 p.12-26 | pymupdf4llm text+tables, images omitted -->

_Introduction_ 

www.ti.com 

## _Chapter 1_ _**Introduction**_ 

**==> picture [506 x 40] intentionally omitted <==**

This chapter introduces the features, subsystems, and architecture of the AM263Px Sitara MCU Processor Platform high-performance System-on-Chip (SoC). 

## **Note** 

This document describes the superset architecture, processors, and peripherals of the AM263Px Family of SoCs, which are part of the Sitara MCU Processors Multicore SoC architecture platform. Not all features are available on each family of devices. The superset AM263Px device will be available for preproduction software development. Software should constrain the features used to match the intended production device. For more information on the specific modules and features available on a particular device, refer to the device comparison table in the corresponding device-specific Data sheet. 

The AM263Px Sitara Processor Platform is hereinafter commonly referred to as _AM263Px_ , _platform_ , _device_ , _chip_ , or _SoC_ . 

**1.1 Overview** ......................................................................................................................................................................13 **1.2 Device Block Diagram** ................................................................................................................................................14 **1.3 Module Allocation and Instances** ..............................................................................................................................15 **1.4 Device Modules** .......................................................................................................................................................... 16 **1.5 Device Identification** ...................................................................................................................................................26 

12 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Introduction_ 

## **1.1 Overview** 

The AM263Px Sitara Arm® Microcontrollers are built to meet the complex real-time processing and control needs of next generation industrial and automotive embedded projects. AM263Px uniquely combines advanced compute with industry leading real-time control peripherals to meet the growing performance needs of applications such as HEV/EV (traction inverters, on-board chargers, and DC-DC converters), motor drives, renewable energy, energy storage, and other general real-time constrained systems. AM263Px combines up to four Cortex-R5F MCUs, a real-time control subsystem (CONTROLSS), a Hardware Security Module (HSM), and one instance of Sitara’s PRU-ICSS, making AM263Px designed for advanced motor control and digital power control applications. 

For multicore AM263Px devices, the R5F cores are arranged in clusters of two Cortex-R5F cores per cluster. Each Cortex-R5F core has 256KB of shared tightly coupled memory (TCM). AM263Px has 3MB of shared SRAM spread across 6 banks of 512kB each. The multiple Arm® cores are configured to be in lockstep mode after device reset. The cores can be optionally programmed by the bootloader to run in dual core mode instead. Extensive ECC is included with the on-chip memory, peripherals, and interconnect for enhanced reliability. The HSM on AM263Px provides cryptographic acceleration, secure boot, and manages granular firewalls, enabling developers to design the most secure systems. AM263Px also includes a Trigonometric Math Unit (TMU) on each R5F core for accelerating trigonometric functions. 

The Real-Time Control Subsystem (CONTROLSS) is a revolutionary subsystem integrated into the device. CONTROLSS contains multiple digital and analog control peripherals including: ADC, Resolver-ADC, CMPSS, EPWM, ECAP, and EQEP, among others to enable efficient execution of critical sense/process/actuate real-time signal chain control loops. The integrated crossbar (XBAR) infrastructure enables flexible configuration and routing of external signals to internal ports and internal signals to external pins. 

The Flash Subsystem (FSS) provides access to external Flash devices via Octal Serial Peripheral Interface (OSPI). The OpTIflash module features Region Based Address Translation (RAT), Fast Local Copy (FLC), and Remote L2 cache (RL2) functions that greatly improve Flash performance on the device. 

The PRU-ICSS in AM263Px provides the flexible industrial communications capability necessary to run advanced Ethernet protocols such as EtherCAT®, PROFINET®, and Ethernet/IP™, or the PRU-ICSS can be used for standard Ethernet connectivity and custom I/O interfacing. The PRU-ICSS supports two Ethernet Ports at 10/100 Mbit operation. The PRU-ICSS also enables additional interfaces in the SoC including sigma delta decimation filters and absolute encoder interfaces. In addition to the PRU-ICSS, the Common Platform Switch (CPSW) interface provides up to two Ethernet ports that can support up to 10/100/1000 Mbit operation and supports standard Ethernet connectivity. 

TI provides a complete set of microcontroller software and development tools for the AM263Px family of microcontrollers in addition to multiple pin-to-pin compatible devices for scalability and ease of use. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

13 

Copyright © 2025 Texas Instruments Incorporated 

_Introduction_ 

www.ti.com 

## **1.2 Device Block Diagram** 

**==> picture [361 x 272] intentionally omitted <==**

**----- Start of picture text -----**<br>
GPIOPRU-ICSSIEP MDIO (x1)*ETH MMC OSPI TRACE JTAG<br>OCSRAM<br>SoC PINMUX EDMA System<br>CPSW MMC OSPI DEBUGSSSTM TC0   TC1 ControlPINMUX 1.8V Analog LDOPower<br>eFUSE 1.8V IO BIAS LDO<br>CORE VBUSM Interconnect CTRLMMRRegisters Thermal Manager (TM)<br>MAILBOX  Voltage Monitor (VMON)<br>MII_RT1IEP MDIOPRU-ICSSUART MII_RT2ECAP ICACHE(16kB)R5F Core 0R5FSS0ICACHE(16kB)R5F Core 1 ICACHE(16kB)R5F Core 0R5FSS1ICACHE(16kB)R5F Core 1 Hardware Security Manager (HSM) DMA XBARVIMEvents and InterruptsTIMESYNC XBAR (2x)PRU-ICSS XBAR<br>PRU0 SPAD3x PRU1 DCACHE(16KB)TCM (128kB) DCACHE(16KB)TCM (128kB) DCACHE(16KB)TCM (128kB) DCACHE(16KB)TCM (128kB) M4F DTHE [1] GPIO XBAR CONTROLSS XBAR<br>(16kB) (ECC) BANK (16kB) (ECC) VIM VIM VIM VIM<br>DMEM0 (8kB) (ECC) MPU MPU MPU MPU Clocking Interconnect<br>DMEM1 (8kB) (ECC) TMU TMU TMU TMU RTI (8x) WDT (4x) XTAL/HFOSC MPU<br>SMEM (32kB) (ECC) CORE PLL INFRA0/1<br>PER PLL<br>CORE VBUSP Interconnect PERI VBUSP Interconnect RCM & PLLCTRL IPC<br>RCOSC (32kHz) SPINLOCK<br>RCOSC (10MHz) MAILBOX<br>XBAR Real-Time Control Subsystem (CONTROLSS)<br>OptiFlash<br>RAT RL2<br>FLC ECC<br>OTFA FOTA<br>Internal Diagnostics<br>DCC ECC Aggregator<br>ESM MCRC<br>XBAR STC PBIST<br>CCM-R5F<br>SoC PINMUX<br>CMPSSA CMPSSB<br>(x10)* (x10)*<br>RDC ADC DAC FSIRX FSITX SDFM EQEP EPWM ECAP CAN-FD LIN UART SPI I2C GPIO (PinMux)<br>(x2)* (x5)* (x1) (x4) (x4) (x2)* (x3)* (x32)* (x16) (x8) (x5) (x6) (x8) (x4) (x139) Device Pins<br>512kB 512kB 512kB 512kB 512kB 512kB MAILBOX<br>Lockstep Lockstep<br>CMPSSA CMPSSB DAC FSIRX FSITX SDFM EQEP EPWM ECAP MCAN LIN UART SPI I2C GPIO<br>4-Channel ADC 6-Channel ADC XBAR<br>**----- End of picture text -----**<br>


## **Figure 1-1. Device Block Diagram** 

## **Note** 

*See the AM263Px Device Comparison table for specific peripheral instance counts. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

14 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Introduction_ 

## **1.3 Module Allocation and Instances** 

|**Module Abbreviation**|**Module Full Name**|**Device Instances**|
|---|---|---|
|**SOC Modules**|||
|R5FSS|Dual Core Arm Cortex-R5F Subsystem|2 dual core R5FSS,<br>total of 4 cores|
|PRU-ICSS|Programmable Real-time Unit Subsystem|1|
|HSM|Hardware Security Manager (M4F-based Subsystem)|1|
|SPINLOCK|Interprocessor Communication - Spinlock|1|
|MAILBOX|Interprocessor Communication - Mailbox|1|
|EDMA|Enhanced DMA|1x (2x TC + 1x CC)|
|DEBUGSS|On-Chip Debug|1|
|**General Connectivity Peripherals**|||
|GPIO|General Purpose Input/Output|4 (1 per Cortex-R5F)<br>139x Total GPIO Pins|
|I2C|Inter-Integrated Circuit|4|
|SPI|Serial Peripheral Interface|8|
|UART|Universal Asynchronous Receiver/Transmitter|6|
|**High-speed Serial Interfaces**|||
|CPSW|2x External Port Gigabit Ethernet Switch|1|
|**Industrial and Control Interfaces**|||
|MCAN|Controller Area Network Interface|8|
|LIN|Local Interconnect Network|5|
|**Memory Interfaces**|||
|OSPI|Octal Serial Peripheral Interface|1|
|OCSRAM|On-Chip Static Random Access Memory|1|
|MMC|Multi-Media Card/Secure Digital (4-bit) Interface|1|
|**Timer Modules**|||
|WWDT|Real Time Interrupt/Windowed WatchDog Timer|4 (1 per Cortex-R5F)|
|RTI|Real Time Interrupt Timer|8|
|**Internal Diagnostics Modules**|||
|DCC|Dual Clock Comparator|4|
|ESM|Error Signaling Module|1|
|MCRC|Memory Cyclic Redundancy Check Controller|1|
|CCM-R5F|CPU Compare Module for Cortex-R5F|2|
|STC|Self-Test Controller|2|
|PBIST|Programmable Built-In Self Test|1|
|ECC|ECC Aggregator|1x-SoC<br>4x-R5FSS<br>1x-ICSSM<br>4x-MCAN<br>1x-CPSW3G<br>1x-HSM|
|**Real-time Control Subsystem (CONTROLSS)**|||
|**Analog Control Peripherals**|||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

15 

Copyright © 2025 Texas Instruments Incorporated 

_Introduction_ 

www.ti.com 

|**Module Abbreviation**|**Module Abbreviation**|**Module Full Name**|**Device Instances**|
|---|---|---|---|
|ADC||Analog to Digital Converter|5<br>(6 Channels per ADC)|
|Resolver(1)(ADC12B3M)|RDC|Resolver to Digital Converter|2|
||ADC|General Purpose Analog to Digital Converter|2 (4 Channels per<br>ADC)|
|CMPSSA||Comparator Subsystem A|10<br>(2x/ADC)|
|CMPSSB||Comparator Subsystem B|10<br>(2x/ADC)|
|DAC||Buffered Digital to Analog Converter|1|
|**Digital Control Peripherals**||||
|EPWM||Enhanced Pulse Width Modulation Module|32|
|EQEP||Enhanced Quadrature Encoder Pulse Module|3|
|ECAP||Enhanced Capture Module|16|
|SDFM||Sigma-Delta Filter Module|2|
|FSI||Fast Serial Interface (RX/TX)|4x RX<br>4x TX|
|**Crossbar Modules**||||
|INPUTXBAR||Flexible Signal Multiplex Input Crossbar|1|
|OUTPUTXBAR||Flexible Signal Multiplex Output Crossbar|1|
|DMAXBAR||EDMA Data Movement Architecture Crossbar|1|
|PWMXBAR||PWM Signal Crossbar|1|
|PWMSYNCOUTXBAR||PWM Sync Output Crossbar|1|
|MDLXBAR||Minimum Dead-band Logic (MDL) Crossbar|1|
|DELXBAR||Diode Emulation Logic (DEL) Crossbar|1|
|ICLXBAR||Illegal Combo Logic (ICL) Crossbar|1|
|INTXBAR||Peripheral Interrupt Crossbar|1|



(1) ZCZ-S, ZCZ-F package only. Resolver may only be used as ADC or RDC. If ADC is not used in resolver mode, it can be used as General Purpose ADC. 

## _**AM263Px Register Addendum Link**_ 

A Register Addendum PDF has been created in order to make the Technical Reference Manual a more effective and size-efficient collateral document, the AM263Px Register Addendum can be downloaded at https://www.ti.com/lit/pdf/SPRUJ57. 

## **1.4 Device Modules** 

This section describes the modules integrated in the device. 

## _**1.4.1 Arm Cortex-R5F Processor Sub System (R5FSS)**_ 

The ARM Dual-Core Cortex-R5F processor subsystem (R5FSS) supports the following main features: 

- Armv7-R architecture 

- Supported modes of operation (boot-time configurable): 

   - Dual Core mode: two independent free-operating cores (Asymmetric Multi-Processing, no coherence) 

   - Single Core mode: one free-operating core and one non-operating core 

   - Lockstep mode: one free-operating core and a lockstep core for safety-enabled applications 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

16 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Introduction_ 

      - There is a two clock cycle delay between CORE0 and CORE1 in lockstep mode. Any errors are routed to the Error Signal Module (ESM) which in turn is routed as an interrupt to the CPU. The ESM is also available as an I/O pin which can be used for external monitoring. See _Error Signal Module_ chapter for more details. 

- R5FSS Memory System 

   - 16KB per CPU Instruction Cache 

      - 4x4KB ways 

   - SECDED ECC protected per 64 bits 

   - – 16KB per CPU Data Cache 

      - 4x4KB ways 

      - SECDED ECC protected per 32 bits 

   - 256KB tightly-coupled memory (TCM) per CPU 

      - SECDED ECC protected per 32 bits 

      - TCM hard error cache Implemented in CPU 

      - Readable/writable from system 

      - Configurable reset initialization values through the CTRLMMR 

      - 64KB TCMA (ATCM) in lock-step and single core mode 

      - 192KB TCMB (BTCM) in lock-step and single core mode 

         - TCMB is split equally between B0 and B1 interleaved banks 

      - 32KB TCMA (ATCM) for each core in split-core mode 

      - 96KB TCMB (BTCM) for each core in split-core mode 

         - TCMB is split equally between B0 and B1 interleaved banks 

      - 128KB TCMA (ATCM) and 128KB TCMB (BTCM) for each core in Split-mode 

- Full-precision Floating Point (VFPv3) 

- 4/8/16-region Memory Protection Unit (MPU) 

- 8 breakpoints, 8 watch points 

- CoreSight Debug Access Port (DAP) 

- CoreSight ETM-R5 interface (CTI, ETM, ATB) 

- Performance Monitoring Unit (PMU) 

- Integrated Vectored Interrupt Manager (VIM) per core with 256 Interrupt Inputs each 

   - Programmable interrupt priority (4-bit) 

   - Programmable interrupt enable mask 

   - Software-generated interrupts 

   - 

Synchronous clock domain crossing on all core interfaces 

## **Note** 

The operating cores can be configured to use the full TCM memory space available to both cores. 

In Dual Core mode, CORE0 and CORE1 each have 128KB of TCM: 

- 32KB TCMA 

- 48KB TCMB0 + 48KB TCMB1 

In Single Core and Lockstep mode, CORE0 has 256KB of TCM : 

   - 64KB TCMA 

   - 192KB TCMB (96KB TCMB0 + 96KB TCMB1) 

- Trigonometric Math Unit (TMU) 

   - Each R5F subsystem contains two TMU modules 

   - Speeds up the execution of common trigonometric and arithmetic operations 

   - Operating frequency: frequency of SYS_CLK - half the frequency of R5F frequency 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

17 

Copyright © 2025 Texas Instruments Incorporated 

_Introduction_ 

www.ti.com 

      - Minimum 200MHz 

   - Operate in lock-step or dual core mode 

- Region Address Translator (RAT) 

   - Minimum granularity of 4KB 

- Fast Local Copy (FLC) Engine 

   - Accelerate boot-up 

   - Support up to four flash regions per FLC with 64KB granularity 

## **Note** 

These details describe a superset of the R5FSS memory configuration. For additional details on device memory availability, please refer to the device-specific data sheet. 

## _**1.4.2 Programmable Real-Time Unit and Industrial Communication Subsystem (PRU-ICSS)**_ 

One instance of the Programmable Real-Time Unit and Industrial Communication Subsystem (PRU-ICSS) allows implementation of various high-performance industrial control algorithms and industrial interface standards such as PROFINET™ and EtherCAT®. 

The PRU-ICSS subsystem supports the following main features, among others: 

- One Programmable Real-time Unit Subsystems (PRU-ICSS): 

   - 

   - 2x PRU (PRU0/PRU1) 

- 32KB shared general purpose RAM with ECC 

- Two 8KB data memories with ECC 

- Up to two 10/100Mbps Ethernet Ports 

- One Industrial Ethernet Peripheral (IEP) module to manage/generate Industrial Ethernet functions 

- One 16550-compatible UART module, with a dedicated 192MHz to support 12Mbps PROFIBUS[®] 

- One Industrial Ethernet 64-bit timer, with 10 capture and 16 compare events, along with slow and fast compensation 

- One Enhanced Capture (ECAP) module 

- One interrupt controller (INTC) with 160 input events supported – 96 external, 64 internal 

- ECC support for all internal memories 

Among the interfaces supported by the PRU-ICSS are real-time industrial protocols used in Controller and Peripheral mode, such as: 

- EtherCAT[®] 

- PROFINET[™] 

- EtherNet/IP[™] 

- PROFIBUS[®] 

- EnDat 2.2 

## **Note** 

See device-specific data sheet for more details related to industrial protocol support. 

## _**1.4.3 Hardware Security Module (HSM)**_ 

One Hardware Security Module (HSM) to facilitate the device security-related functionality: 

- Arm Cortex M4F Core (200MHz) 

- 1x Real-time Interrupt (RTI) module 

- 1x RTI/WWDT module used as watchdog (WD mode) 

- 2x Timers 

   - 32-bit up counter 

   - Cascading mode support for 2x 64 bit counters 

- HSM Mailbox for Messaging between HSM and host processors. 

- Designated HSM DMA to fetch and store the data for cryptography services. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

18 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Introduction_ 

- Hardware Security Accelerators (200MHz) 

   - 

   - Symmetric Encryption/Decryption 

   - AES: 128, 192 and 256-bits key 

   - Cipher modes ECB, CTR, CBC, GCM 

   - CBC-MAC, CMAC based on AES 

- Asymmetric Cryptography 

   - High-performance PKA (public key engine) for large vector math/modulus operation 

   - • RSA2048, RSA3092, RSA4096 

   - ECC Secp/NIST Curves: Curve25519, X25519, secP256r1, secP256k1, secP384r1, secP384k1, Brain pool, and others. 

- Hash-based Message Authentication Code (HMAC) 

   - SHA2 – 256, 384 and 512-bit support 

   - HMAC-SHA256, HMAC-SHA512 – Keyed Hashing 

- Random Number Generator 

   - Deterministic Random Bit Generator (DRBG) with Pseudo and True Random Number Generation (PRNG / TRNG) support 

   - Capability to seed the PRNG with TRNG seed 

## _**1.4.4 Real-time Control Subsystem (CONTROLSS)**_ 

The integrated real-time Control Subsystem (CONTROLSS) enables closed loop control systems with flexible interconnection between data acquisition, actuator modules, and other control signal resources. The CONTROLSS module consists of the following control peripherals: 

## **Analog Control Peripherals** 

- 5x Analog to Digital Converter (ADC) modules 

   - 12-bit resolution with 4MSPS sample rate 

   - Programmable 6x single-ended or 3x differential channels 

   - 3.2V full scale voltage range with 1.8V reference (32/18 internal input scaling) 

   - Support for internal or external 1.8V ADC VREF reference voltage (2% internal reference accuracy error) 

   - Two common external calibration pins for all ADCs 

   - 4x Post-processing blocks per ADC 

   - 

      - 12x Simultaneous Compare Blocks (ADC Safety Tiles) 

   - Multiple ADC trigger sources including CPU timers, GPIO/Input XBAR, and EPWM SOCa/SOCb signals. 

- 1x Resolver with 2x dedicated SAR ADCs configurable in the following modes: 

   - 2x motor position sensing units 

   - 2x General Purpose ADCs with 4x channels, 12-bit resolution with 3MSPS sample rate 

- 1x Buffered Digital to Analog (DAC) module 

   - 12-bit resolution 

- Support for internal or external 1.8V DAC VREF reference voltage (2% internal reference accuracy error) 

- • 10x Comparator Subsystem A (CMPSSA) 

   - Each instance has 2 comparators + 2 DACs 

   - Each instance supports the window comparison of one input (uses both comparators) OR 

   - Compare two inputs OR 

   - Single threshold compare of a single input 

- 10x Comparator Subsystem B (CMPSSB) 

   - Each instance has 2 comparators + 2 DACs 

   - Each instance supports the window comparison of one input (uses both comparators) OR 

   - Single threshold compare of a single input 

## **Digital Control Peripherals** 

- 32x Enhanced Pulse-width Modulation (EPWM) modules 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

19 

Copyright © 2025 Texas Instruments Incorporated 

_Introduction_ 

www.ti.com 

- 

- 

      - Each EPWM module has a dedicated 16-bit time-base counter with period and frequency control 

      - Two PWM outputs per module (EPWMxA and EPWMxB) that can be configured as: 

      - Two independent PWM outputs with single-edge operation 

      - Two independent PWM outputs with dual-edge symmetric operation 

      - One independent PWM output with dual-edge asymmetric operation 

- 16x Enhanced Capture (ECAP) modules 

   - One complete capture channel that can be instantiated multiple times 

   - – Capture modes: 

      - Single-shot capture, up to four event timestamps 

      - Continuous capture of timestamps (four-deep circular buffer) 

      - Absolute timestamp capture 

      - Difference (delta) mode timestamp capture 

- 2x Sigma-Delta Filter (SDFM) modules 

   - 4x data input pins and 4x clock input pins per module 

   - Each filter has an input control unit, primary filter (data filter) unit, and secondary filter (comparator filter) unit with 4x independent comparators 

- 3x Enhanced Quadrature Encoder Pulse (EQEP) modules 

   - Direct interface with linear or rotary incremental encoder for use in high-performance motion and position control systems 

- 4x Fast Serial Interface Transmitter (FSITX) modules 

   - Handles framing of data, CRC generation, signal generation for FSI TX signals, interrupt generation 

   - Each module has 2x data signals and 1x clock signal 

- 4x Fast Serial Interface Receiver (FSIRX) modules 

   - 

   - 

- Handles framing of data, CRC generation, frame related error-checking 

- Each module has 2x data signals and 1x clock signal 

## _**1.4.5 Spinlock (SPINLOCK)**_ 

One Spinlock module with (256 hardware semaphores) for synchronizing the processes running on multiple cores in the device. 

## _**1.4.6 Enhanced Data Movement Architecture (EDMA)**_ 

One Enhanced Data Movement Architecture (EDMA) module can be used for efficient transfer of data and support between software, firmware, and hardware in all combinations. The EDMA consists of a single Channel Controller (TPCC) and two Transfer Controllers (TPTC) to enable various data movement requirements. 

The **TPCC** is a high flexible channel controller that serves as both a user interface and an event interface for the EDMA controller. The EDMA_TPCC serves to prioritize incoming software requests or events from peripherals, and submits transfer requests (TRs) to the transfer controller. 

The **TPTC** performs read and write transfers by EDMA ports to the target peripherals, as programmed in the Active and Pending set of the registers. The transfer controllers are responsible for data movement, and issue read/write commands to the source and destination addresses programmed for a given transfer in the EDMA_TPCC. 

The **EDMA_TPCC** channel controller has the following features: 

- Fully orthogonal transfer description: 

   - Three transfer dimensions 

   - A-synchronized transfers: one dimension serviced per event 

   - AB-synchronized transfers: two dimensions serviced per event 

   - Independent indexes on source and destination 

   - Chaining feature allowing a 3-D transfer based on a single event. 

- Flexible transfer definition: 

   - Increment or FIFO transfer addressing modes 

   - Linking mechanism allows automatic PaRAM set update 

20 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Introduction_ 

   - Chaining allows multiple transfers to execute with one event 

- Interrupt generation for the following: 

   - Transfer completion 

   - Error conditions 

- Debug visibility: 

   - Queue water marking/threshold 

   - Error and status recording to facilitate debug 

- 64 DMA request channels: 

   - Event synchronization 

   - Manual synchronization (CPUs write to event set registers EDMA_TPCC_ESR and EDMA_TPCC_ESRH). 

   - Chain synchronization (completion of one transfer triggers another transfer). 

- Eight QDMA channels: 

   - QDMA channels trigger automatically upon writing to a parameter RAM (PaRAM) set entry. 

   - Support for programmable QDMA channel to PaRAM mapping. 

- Each PaRAM set can be used for a DMA channel, QDMA channel, or link set. 

- Multiple transfer controllers/event queues. 

- 16 event entries per event queue. 

The **EDMA_TPTC** transfer controller has the following features: 

- 128-bit wide read and write ports per TC 

- Supports two-dimensional transfers with independent indexes on source and destination (EDMA_TPCC manages the third dimension) 

- Support for increment or constant addressing mode transfers 

- Interrupt and error support 

- Memory-Mapped Register (MMR) bit fields are fixed position in 32-bit MMR regardless of endianness 

## _**1.4.7 General Purpose Input/Output Interface (GPIO)**_ 

Four General Purpose Input/Output (GPIO) modules, each dedicated to a specific R5FSS core. These provide general-purpose pins that can be configured as either inputs or outputs. The GPIO module main features include: 

- Support of 9 banks x 16 interrupt-capable GPIO pins 

- Interrupts can be triggered by rising and/or falling edge, specified for each GPIO pin 

- Set/clear functionality per individual GPIO pin 

- CPUs can control the GPIOs on a per pin granularity 

   - 

      - Each processor core has a separate module for controlling GPO pins and observing GPI pins 

   - IOMUX CTRLMMR register-based 4:1 multiplexer to individually assign GPO pin control to a specific processor core 

   - GPI pins are observable by all processor cores 

- Support for GPI signal conditioning chain 

   - Invert/Non-invert 

   - 

   - Signal Qualification 

   - Asynchronous input 

   - Synchronise to SYSCLK 

   - Qualification using sampling window 

- Software-based tristate control to emulate open-drain IO mode 

## _**1.4.8 Inter-Integrated Circuit Interface (I2C)**_ 

Four instances of the multi-controller Inter-Integrated Circuit (I2C) interface module, each with the following main features: 

- 1x Instances with open-drain voltage buffers in compliance with the Philips I2C-bus specification version 2.1 

- Support of standard mode (up to 100Kbps) and fast mode (up to 400Kbps) 

- Support of 7-bit and 10-bit device addressing modes 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

21 

Copyright © 2025 Texas Instruments Incorporated 

_Introduction_ 

www.ti.com 

- 

   - 8-bit-wide data access 

- Support of multi-controller transmitter/peripheral receiver and receiver/peripheral transmitter modes 

- Built-in FIFOs with programmable size of 8 to 64 bytes for buffered read or write 

## _**1.4.9 Serial Peripheral Interface (SPI)**_ 

Eight instances of the Serial Peripheral Interface (SPI) module with the following main features: 

- Serial clock with programmable frequency, polarity, and phase for each channel 

- Wide selection of SPI word lengths, ranging from 4 to 32 bits 

- Up to two channels in controller mode, or single channel in receiver mode 

- Support for various controller multichannel modes 

- Single interrupt line for multiple interrupt source events 

- Support of start-bit write command 

- Support of start-bit pause and break sequence 

- Built-in FIFO available for a single channel 

## _**1.4.10 Universal Asynchronous Receiver/Transmitter (UART)**_ 

Six instances of the configurable Universal Asynchronous Receiver/Transmitter (UART) interface module with the following main features: 

- 16C750-compatible interface 

- Support of RS-485 external transceiver auto flow control 

- Dual 64-byte FIFOs – one per each received and transmitted data paths 

- Programmable and selectable transmit and receive FIFO trigger levels for DMA and interrupt generation 

- Programmable sleep mode 

- Baud-rate from 300 bits/s up to 3.6864Mbits/s with 48MHz functional clock 

- Auto-baud between 1200 bits/s and 115.2 Kbits/s (only when 48MHz function clock is used) 

- Support of IrDA 1.4 Slow Infrared (SIR), Medium Infrared (MIR), and Fast Infrared (FIR) communications 

- Support of Consumer Infrared Remote control mode (CIR) with programmable data encoding 

## **Note** 

Only one UART instance has support for support full modem control functions. All other UART instances will support only the TX, RX, RTS, and CTS signals. 

## _**1.4.11 3-port Gigabit Ethernet Switch (CPSW)**_ 

One instance of the 3-port Gigabit Ethernet Switch (CPSW) subsystem provides Ethernet packet communication for the device. The CPSW subsystem provides the following main features: 

- Two Ethernet ports (Port 1/Port 2) with selectable MII, RMII, and RGMII interfaces and a single internal Communications Port Programming Interface (CPPI) port (Port 0) 

- Synchronous 10/100/1000 Mbit operation with Flexible logical FIFO-based packet buffer structure 

   - Full duplex mode supported in 10/100/1000 Mbps modes 

   - 

   - Half-duplex mode supported in 10/100 Mbps modes only 

- Maximum frame size of 3024 bytes 

- Management Data Input/Output (MDIO) module for PHY Management with Clause 45 support 

- Programmable interrupt control with selected interrupt pacing 

- One CPDMA CPPI 3.0 DMA Host Interface (Port 0) 

- Emulation Mode, Digital loopback, and FIFO loopback modes supported 

- RAM Error Detection and Correction (SECDED) 

- Eight priority level Quality Of Service (QOS) support (802.1p) 

- Support for Audio/Video Bridging (P802.1Qav/D6.0) 

- Support for IEEE 1588 Clock Synchronization (2008 Annex D, Annex E and Annex F) 

- DSCP Priority Mapping (IPv4 and IPv6) 

- Energy Efficient Ethernet (EEE) support (802.3az) 

- Non-Blocking switch fabric with Flow Control Support (802.3x) and Wire rate switching (802.1d) 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

22 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Introduction_ 

- Time Sensitive Network (TSN) Support 

   - IEEE 802.1Qbv Enhancements for Scheduled Traffic 

- Address Lookup Engine (ALE) with 512 ALE table entries 

- EtherStats and 802.3 Stats Remote Network Monitoring (RMON) statistics gathering (per port statistics) 

- Support for Ethernet MAC transmit to MAC receive digital loopback mode 

## _**1.4.12 Octal Serial Peripheral Interface (OSPI)**_ 

The Flash Subsystem (FSS) includes one of the OSPI instances (OSPI0). One instance of the Octal Serial Peripheral Interface (OSPI) support the following main features: 

- Support for Single, Dual, Quad, or Octal SPI mode of operation 

- Eleven pin interface for single OSPI device: DQS, DQ0, DQ1, DQ2, DQ3, DQ4, DQ5, DQ6, DQ7, CSn0, CLK 

   - Optional pins: RESET_OUT0, ECC_FAIL, LBCLKO 

   - Support for multiple OSPI devices: CSn1, RESET_OUT1 

- Up to 133MHz SDR frequency and 133MHz DDR frequency 

- Prefetcher support 

- Memory mapped direct mode of operation for flash data transfer and XIP from flash 

- Software triggered indirect mode of operation 

- 256B buffer for indirect transfers 

- Full XIP support with no limitation on R5 Cache miss wrapping burst 

- Two Chip Select signals to connect up to two external flash devices 

- PHY and Tap Mode support 

- Support for on the fly encryption and authentication(OTFA) on OSPI0 interface. OTFA enables external memory IP protection at runtime during XIP. Option to disable OTFA. Support for 4Byte and 8 Byte MAC per 32 Byte data for increased security 

- Support concurrent direct read and write requests to enable Firmware over the air update(FOTA) during XIP. 

## _**1.4.13 Multi-Media Card/Secure Digital Interface (MMCSD)**_ 

One Multi-Media Card/Secure Digital (MMCSD) controller module with the following features: 

- One controller with 4-bit wide data bus 

- Support of MMC 4.3 Host Specification 

- Support of SD Host Controller Standard Specification - SDIO 2.00 

- Multi-Media card features: 

   - 3.3V legacy modes with 1-bit single data rate (0-24MHz clock) 

   - 3.3V HS-SDR with 4-bit bus width (0-48MHz Clock) 

- SD card support: 

   - DS mode (1/4-bit, 3.3V): up to 12MBps (24MHz clock) 

   - HS mode (1/4-bit, 3.3V): up to 24MBps (48MHz clock) 

- Supports Card Detect (SDCD) and Write Protect (SDWP) 

## _**1.4.14 Controller Area Network (MCAN)**_ 

Eight Controller Area Network interfaces (MCAN) with support for classic CAN and CAN FD (CAN with Flexible Data-Rate) specifications. The MCAN module consists of the following main features: 

- Conforms with CAN Protocol version 2.0 part A, B and ISO 11898-1:2015 

- Full CAN FD (up to 64 data bytes) support 

- AUTOSAR and SAE J1939 support 

- Loopback mode for self-test 

- Up to 32 dedicated transmit buffers and 64 dedicated receive buffers 

- Two configurable receive FIFOs, up to 64 elements each 

- Configurable transmit FIFO, up to 32 elements 

- Configurable transmit queue, up to 32 elements 

- Configurable transmit event FIFO, up to 32 elements 

- Up to 128 filter elements 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

23 

Copyright © 2025 Texas Instruments Incorporated 

_Introduction_ 

www.ti.com 

- Two interrupt lines with support for maskable interrupts 

- Timestamp Counter 

## _**1.4.15 Local Interconnect Network (LIN)**_ 

Ten instances of the configurable Local Interconnect Network (LIN) interface module with the following main features: 

- 16C750-compatible 

- Compatibility with LIN 1.3, 2.0, and 2.1 protocols 

- Enhanced Baud Rate Generated configurable up to 20 kpbs – 2[31] programmable transmission rates with 7 fractional bits 

- Two external pins: LINRX and LINTX. 

- Multi-buffered receive and transmit units 

- Automatic wake-up support and bus idle detection 

- Support for common Error Detection methods 

## _**1.4.16 Timers**_ 

Two sets of timer modules are instantiated in the device: 

- Eight RTI Timer instances, implemented by the Real-time Interrupt function of the RTI/WWDT module. 

- Four Windowed Watchdog Timer (WWDT) instances (1 per core), implemented by the Digital Windowed Watchdog (DWWD) function of the RTI/WWDT module 

- The RTI/WWDT provides timer functionality for operation systems and benchmarking code with the following main features: 

   - Two independent 64 bit counter blocks 

   - Four configurable compare registers for generating operating system ticks 

   - Free running counter 0 can be incremented by either the internal pre-scale counter or by an external event 

   - Selectable RTI clock input (derived from any of the available clock sources) 

   - Fast enabling/disabling of events 

## _**1.4.17 Internal Diagnostics Modules**_ 

Instantiated in the device are various internal diagnostics modules which provide on-chip monitoring and diagnostic functions required to achieve certain safety compliance levels: 

- Four Dual Clock Comparator (DCC) modules, used to determine the accuracy of a clock signal during the time execution of an application, each having the following main features: 

   - Two independent counter blocks count clock pulses from each clock source 

   - Each counter block is programmable, however, for proper operation the counters must be programmed with seed values that respect the ratio of the two clock frequencies 

   - Configurable time base for error signal 

   - Error signal generation when one of the clocks is out of spec 

   - 

      - Clock frequency measurement 

- One Memory Cyclic Redundancy Check (MCRC) module to enable hardware-based CRC calculations. 

- Integrated on-die temperature monitor (+/- 8º C temperature accuracy) 

- One instance of Error Signaling Module (ESM) for safety-related events and/or errors aggregation from throughout the device into one location supports the following main features: 

   - Up to 1024 level or pulse error event inputs 

   - Selectable low and high priority interrupt, error pin prioritization of each error event 

   - Error signal routed out of device through MCU_ESM error signal 

   - Configurable time base for error signal 

   - Error forcing capability 

   - 

   - Internal redundant flops on safety critical fields 

- Multiple ECC Aggregator modules supporting ECC mechanism for providing increased system reliability via reduction of memory software errors by allowing single bit errors to be detected and corrected (SEC) and 

24 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Introduction_ 

double bit errors to be detected (DED). Applied to different memories in many of the subsystems, each of the ECC aggregators has the following main features: 

- Reduces memory software errors via single error correction (SEC) and double error detection (DED) 

- Provides a mechanism to control and monitor the ECC RAMs in a module or subsystem 

- Aggregates level pending status from the ECC RAMs in two interrupts to the device CPU – interrupt for correctable error (SEC) and interrupt for uncorrectable error (DED) 

- Supports up to 256 ECC endpoints (either ECC RAM or interconnect ECC component) 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

25 

Copyright © 2025 Texas Instruments Incorporated 

_Introduction_ 

www.ti.com 

## **1.5 Device Identification** 

The device part number identification data can be read in the TOP_CTRL.EFUSE_JTAG_USERCODE_ID register. See Table 1-1 for more information. 

**Table 1-1. Device Part Number Identifier** 

|**TOP_CTRL.EFUSE_JTAG_USERCOD**<br>**E_ID**<br>**Register Field**|**Value and Description**|**Comment**|
|---|---|---|
|[31-13] DEVICE_ID|Base Part Number|Refer to the Device Comparison section<br>for the DEVICE_ID value of a given part<br>number.|
|[12] SAFETY|0 = Non Functional Safety<br>1 = Functional Safety||
|[11] PACKAGE|Package<br>0x06 = ZCZ<br>Others = Reserved||
|[10-6] SPEED|Device Speed Grade<br>0x0E (Grade N):<br>400MHz R5F<br>2MB (Full speed and MIN memory)<br>0x0F (Grade O):<br>400MHz R5F<br>3MB (Full speed and full memory)<br>0x10 (Grade P):<br>200MHz R5F<br>3MB (Half speed and full memory)|Refer to the Operating Performance<br>Points section for the supported speed<br>grades and the definitions for a given<br>device.|
|[5-3] TEMP|Temperature Grade<br>0x05 = -40°C to 125°C<br>0x07 = -40°C to 150°C<br>Others = Reserved|Operating junction temperature range.|
|[2-0] FEATURE|Package Feature<br>0x01 = AM263x compatible package<br>0x02 = Sensor package + FLASH-in-Package<br>0x05 = Sensor package||



The manufacturer identity, the boundary scan part number, and the silicon revision of the device can be read from the configuration port via JTAG. 

26 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

