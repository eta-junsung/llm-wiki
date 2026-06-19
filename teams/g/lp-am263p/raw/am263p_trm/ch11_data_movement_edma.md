<!-- AM263P TRM | 11 Data Movement Architecture (EDMA) | 원본 p.1030-1096 | pymupdf4llm text+tables, images omitted -->

www.ti.com 

_Data Movement Architecture_ 

## _Chapter 11_ _**Data Movement Architecture**_ 

**==> picture [506 x 40] intentionally omitted <==**

This chapter describes the data movement architecture of the device. 

1030 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## **11.1 Data Movement Architecture Overview** 

This chapter is a high-level summary of the data movement architecture implemented in the device. 

**11.1.1 Overview** ......................................................................................................................................................... 1032 **11.1.2 Definition of Terms** .........................................................................................................................................1032 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1031 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## _**11.1.1 Overview**_ 

The primary goal of the device Data Movement Architecture and related Subsystems is to ensure that data can be efficiently transferred from a producer to a consumer while meeting the real time requirements of the system. 

The Enhanced Data Movement Architecture (EDMA) module aims to facilitate direct memory access (DMA) and provides a consistent Application Programming Interface (API) to the host software. 

Data movement tasks are commonly offloaded from the host processor to peripheral hardware to increase system performance. Significant performance gains result from careful design of the interface between the host software and the underlying acceleration hardware. In networking applications, packet transmission and reception are critical tasks. In general purpose compute, ping pong buffer prefetch and store are critical tasks as well as general mis-aligned block copy operations. 

The design goals for the device Data Movement Architecture and are as follows: 

- Minimize cost 

- Minimize host overhead 

- Maximize memory use efficiency 

- Maximize bus burst efficiency 

- Maximize symmetry between transmit/receive operations 

- Maximize scalability for number of connections / buffer sizes / queue sizes / protocols supported 

- Minimize protocol specific features 

- Minimize complexity 

## _**11.1.2 Definition of Terms**_ 

Channel— A channel refers to the sub-division of information (flows) that is transported across a DMA engine. Each channel has associated state information. Channels are used to segregate information flows based on the protocol used, scheduling requirements (for example, CBR, VBR, ABR), or concurrency requirements (that is, blocking avoidance). Information flow within a channel is a stream of strongly ordered information. 

Data Buffer— A data buffer is a single data structure that contains payload information for transmission to or reception from a channel. 

Buffer Descriptor— A buffer descriptor is a single data structure that contains information about one or more data buffers. 

Packet Descriptor— A packet descriptor is another name for the first buffer descriptor within a packet. Some fields within a data buffer descriptor are only valid when it is a packet descriptor including the tags, packet length, packet type, and flags. All Monolithic type descriptors are packet descriptors (and are also a Data Buffer). 

Queue— A queue is a list of strongly ordered entries which is typically used to pass work between a producer and a consumer. Queue entries in most cases are references to a work payload which is being passed but in some cases (Transfer Request Packets for example) queue entries may actually contain data which is being transferred. Queues are used throughout DMA whenever communication is required between entities. Queues can have multiple different implementations and DMA uses two of the most common: linked lists and rings. 

Linked list— A linked list is a data structure in which each entry stores not only the entry data but also a chaining pointer to the next entry in the list. The last entry in each list has its chaining pointer set to NULL (typically encoded as 0x0). The list manager maintains a pointer to the head element on the list and to the tail element on the list. Since the chaining pointer is stored with the entry data, linked lists have a length which is dynamically changeable and limited only by the ability to allocate additional entries which are to be queued/de-queued. Linked lists are present in Host Descriptors to chain multiple descriptors to form a packet. 

Ring— A ring is a data structure in which a contiguous memory block defined by M N-byte entries (total size is M × N bytes) is statically allocated and sequentially written/read in order to pass data or data references. Rings are also referred to as circular buffers because when the last element in the contiguous memory array is written, the pointers wrap back to the beginning address for the ring and start the process all over again. The Ring Accelerator component uses rings in order to implement logical queues. 

1032 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

Memory— Memory is an area of data storage managed by the host. This area is visible to the port as a 64-bit addressable area. 

Device Driver— A device driver is application independent software that runs on the host for purposes abstracting the low level hardware so that upper level software can use the hardware without knowing every bit field location or initialization sequence.. General device driver functions include port initialization, transmit packet queuing, and receive packet processing. 

SOP— Start of Packet. This refers to the descriptor/buffer that is the first buffer in a packet. 

MOP— Middle of Packet. This refers to the descriptors/buffers that are neither the first or last buffers in a packet. 

EOP— End of Packet. This refers to the descriptor/buffer that is the last buffer in a packet. 

## **11.2 Enhanced Direct Memory Access (EDMA)** 

This section describes the Enhanced Direct Memory Access (EDMA) controller. For features applicable to the EDMA instances in the device, see the device-specific Integration section. The primary purpose of the EDMA controller is to service data transfers programmed between two memory-mapped follower endpoints on the device. The EDMA controller consists of two principle blocks: 

- EDMA channel controllers: EDMA_TPCC 

- EDMA transfer controllers: EDMA_TPTC 

Devices can have multiple instances of EDMA channel controllers, each associated with multiple EDMA transfer controllers. 

The EDMA channel controller serves as the user interface for the EDMA controller. The EDMA_TPCC includes parameter RAM (PaRAM), channel control registers, and interrupt control registers. The EDMA_TPCC serves to prioritize incoming software requests or events from peripherals, and submits transfer requests (TR) to the EDMA transfer controller. 

The EDMA transfer controllers are responsible for data movement. The transfer request packets (TRP) submitted by the EDMA_TPCC contain the transfer context, based on which the transfer controller issues read/write commands to the source and destination addresses programmed for a given transfer. 

**11.2.1 EDMA Module Overview** ................................................................................................................................ 1034 **11.2.2 EDMA Integration** ........................................................................................................................................... 1035 **11.2.3 EDMA Controller Functional Description** .....................................................................................................1039 **11.2.4 EDMA Transfer Examples** ..............................................................................................................................1088 **11.2.5 EDMA Debug Checklist and Programming Tips** ......................................................................................... 1095 **11.2.6 EDMA Event Map** ............................................................................................................................................1096 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1033 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## _**11.2.1 EDMA Module Overview**_ 

The enhanced direct memory access module, also called EDMA, performs high-performance data transfers between two target endpoints, memories and peripheral devices without microprocessor unit (MPU) or digital signal processor (DSP) support during transfer. EDMA transfer is programmed through a logical EDMA channel, which allows the transfer to be optimally tailored to the requirements of the application. 

The EDMA controller is based on two major principal blocks: 

- EDMA third-party channel controller (EDMA_TPCC) 

- EDMA third-party transfer controller (EDMA_TPTC) 

Figure 11-1 shows an overview of the EDMA module. 

**==> picture [310 x 317] intentionally omitted <==**

**----- Start of picture text -----**<br>
Enhanced DMA<br>Controller<br>Configuration<br>TPCC<br>EDMA Interrupts<br>TPTC0<br>To interrupts<br>within the<br>device TPTC1<br>Device<br>EDMA_iCLKs clock<br>EDMA Events  EDMA_iRSTs controlreset<br>from Different<br>Sources in the  DMA_EDMA_DREQ_[63:0]<br>system<br>PCR 32bit<br>SCR 128bit<br>**----- End of picture text -----**<br>


**Figure 11-1. EDMA Module Overview** 

For EDMA instances available on the device, see the device-specific integration section. 

The **TPCC** is a high flexible channel controller that serves as both a user interface and an event interface for the EDMA controller. The EDMA_TPCC serves to prioritize incoming software requests or events from peripherals, and submits transfer requests (TRs) to the transfer controller. 

The **TPTC** performs read and write transfers by EDMA ports to the target peripherals, as programmed in the Active and Pending set of the registers. The transfer controllers are responsible for data movement, and issue read/write commands to the source and destination addresses programmed for a given transfer in the EDMA_TPCC. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1034 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## **11.2.1.1 EDMA Features** 

This section shows generic EDMA features. For features applicable to the EDMA instances in the device, see the device-specific Integration section. 

The EDMA_TPCC channel controller has the following features: 

- Fully orthogonal transfer description: 

   - Three transfer dimensions 

   - A-synchronized transfers: one dimension serviced per event 

   - AB-synchronized transfers: two dimensions serviced per event 

   - Independent indexes on source and destination 

   - Chaining feature allowing a 3-D transfer based on a single event. 

- Flexible transfer definition: 

   - Increment or FIFO transfer addressing modes 

   - Linking mechanism allows automatic PaRAM set update 

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

- 64-bit wide read and write ports per TC 

- Supports two-dimensional transfers with independent indexes on source and destination (EDMA_TPCC manages the third dimension) 

- Support for increment or constant addressing mode transfers 

- Interrupt and error support 

- Memory-Mapped Register (MMR) bit fields are fixed position in 32-bit MMR regardless of endianness 

## _**11.2.2 EDMA Integration**_ 

This section describes modules integration in the device, including information about clocks, resets, and hardware requests. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1035 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## **11.2.2.1 EDMA Integration** 

**==> picture [477 x 319] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>SYS_CLK EDMA#_CLK<br>TPTC0_R<br>EDMA_REQ EDMA#_REQ TPTC0_W<br>64<br>TPTC1_R<br>TPTC1_W<br>EDMA# ICSSM<br>EDMA#_RST_CTRL Bit<br>EDMA#_TPCC_RST_CTRL Bit EDMA#_WARMRESET TPCC_A_ERRINT_PO R5FSS0-CORE0<br>RCM EDMA#_TPTC1_RST_CTRL Bit TPCC_A_INT_PO[7:0] R5FSS0-CORE1<br>EDMA#_TPTC0_RST_CTRL Bit EDMA#_TPCC_WARMRESET TPCC_A_INTG R5FSS1-CORE0<br>TPCCA_MP_INT R5FSS1-CORE1<br>EDMA#_TPTC1_WARMRESET TPTCA_ERR_INT<br>MSS_CTRL<br>TPTCA_INT<br>EDMA#_TPTC0_WARMRESET<br>Warm Reset Sources<br>ESM<br>INFRA_GO INTERCONNECT<br>VBUSM INTERCONNECT<br>ICSSM XBAR<br>TPTC0_CFG TPTC1_CFG TPCC_CFG<br>**----- End of picture text -----**<br>


**Figure 11-2. EDMA Integration Block Diagram** 

## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

## **11.2.2.2 EDMA Interrupt Aggregator** 

The following EDMA interrupts are aggregated and sent to the processor: 

- TPCC Completion Interrupt 

- TPCC Completion Region Interrupts 

- TPTCs Completion Interrupt 

Table 11-1 shows the associated interrupt and registers for each TPCC instance. 

**Table 11-1. TPCC Interrupts** 

|**TPCC**|**Interrupt**|**Registers Space**|
|---|---|---|
|TPCC_A|TPCC_A_INTAGG|*_INTAGG_MASK<br>*_INTAGG_STATUS<br>*_INTAGG_STATUS_RAW|



1036 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

For an event to generate an interrupt to the processor, the corresponding bit field must be unmasked in TPCC_x_INTAGG_MASK. 

Only an interrupt processor can read the TPCC_x_INTAGG_STATUS register to detect which event triggered the interrupt. 

The interrupt can be cleared by writing 0x1 to the corresponding bit in TPCC_x_INTAGG_STATUS. 

The software must verfiy that all the aggregated interrupts are cleared so that the level interrupt is de-asserted before exiting the ISR. Only then the software can provide a new pulse interrupt to the processor. Thus, after clearing the software can read the register to confirm a value of 0x0. 

The register TPCC_x_INTAGG_STATUS_RAW is set on an event irrespective of the value in TPCC_x_INTAGG_MASK. This field can be cleared by writing 0x1 to the corresponding bit in TPCC_x_INTAGG_STATUS_RAW. 

## **11.2.2.3 EDMA Error Interrupt Aggregator** 

The following interrupts are aggregated and sent to the processor: 

- TPCC Error 

- TPCC MPU Error 

- TPTCs Error 

- TPCC Read and Write Config Space Access error 

- TPTCs Read and Write Config Space Access error 

**Table 11-2. TPCC Error Interrupt Aggregators** 

|**TPCC**|**Interrupt**|**Registers Space**|
|---|---|---|
|TPCC_A|TPCC_A_ERRAGG|*_ERRAGG_MASK<br>*_ERRAGG_STATUS<br>*_ERRAGG_STATUS_RAW|



For an event to generate an interrupt to the processor, the corresponding bit field must be unmasked in TPCC_x_ERRAGG_MASK. 

Only an interrupt processor can read the TPCC_x_ERRAGG_STATUS register to detect which event triggered the interrupt. 

The interrupt can be cleared by writing 0x1 to the corresponding bit in TPCC_x_ERRAGG_STATUS. 

The software must ensure that all the aggregated interrupts are cleared so that the level interrupt is de-asserted before exiting the ISR. Only then is it ensured that a new pulse interrupt is generated to the processor. Thus, after clearing the software should read the register to confirm a value of 0x0 

The register TPCC_x_ERRAGG_STATUS_RAW is set on an event irrespective of the value in TPCC_x_ERRAGG_MASK. This field can be cleared by writing 0x1 to the corresponding bit in TPCC_x_ERRAGG_STATUS_RAW. 

## **11.2.2.4 EDMA Configuration** 

- The device has 1 channel controller: TPCC_A and two transfer controllers: TPTC_A0 and TPTC_A1. 

**Table 11-3. EDMA Channel Controller Configuration** 

|**Parameters**|**TPCC**|
|---|---|
|DMA Channel|64|
|PaRAM Entires|256|
|QDMA Channel|8|
|Event queues|2|
|Mem Protection|Yes|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1037 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**Table 11-3. EDMA Channel Controller Configuration (continued)** 

|**Parameters**|**TPCC**|
|---|---|
|Channel Mapping|Yes|
|Num TCs|2|
|Num Interrupt Channel|64|
|Num Regions|8|



**Table 11-4. EDMA Transfer Controller Configuration** 

|**Parameters**|**TPTC[0/1]**|
|---|---|
|FIFO Size|512|
|TR Pipe Depth|4|
|Bus Width|8|
|Read Cmd Num|8|
|Write Cmd Num|8|
|RAM ECC|Yes|



## **Default Burst Size configuration (DBS)** 

All TPTCs in the device support four different configurable default-burst-sizes. Table 11-5 shows the config-value to DBS mapping. 

**Table 11-5. Config Value to DBS Mapping** 

|**Config value**|**Burst size**|
|---|---|
|2’b00|16 bytes|
|2’b01|32 bytes|
|2’b10|64 bytes|
|2’b11|128 bytes|



## **Table 11-6. TPTC DBS Configuration Registers** 

|**TPTC instance**|**Corresponding Register**|
|---|---|
|TPTC_[A0/A1]|TPTC_DBS_CONFIG::TPTC_DBS_CONFIG_TPTC_[A0/A1]|



1038 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## _**11.2.3 EDMA Controller Functional Description**_ 

This chapter discusses the architecture of the EDMA controller. The description contained in this section is generic to the EDMA module, and not all features mentioned here are supported by the device. See the EDMA integration section of the device to determine the applicability of these features. 

## **11.2.3.1 Block Diagram** 

Figure 11-3 shows the functional block diagram of the EDMA controller. 

**==> picture [430 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
EDMA Controller Transfer<br>controllers<br>MMR<br>Channel Controller access TPTC0<br>Read/write<br>TR<br>R/W commands<br>To/from DMA/QDMA Transfer Completion and data<br>Event<br>EDMA channel PaRAM request<br>programmer logic queues submission EDMA_TC0_IRQ_ERR IRQ<br>MMR TPTC1<br>access<br>Completion TR Read/write<br>EDMA_TPCC_IRQ_ERR and error Completion R/W commands<br>EDMA_TPCC_IRQ_REGION[7:0] interrupt detection Completion and data<br>EDMA_TPCC_IRQ_MP logic EDMA_TC1_IRQ_ERR IRQ<br>edma-006<br>**----- End of picture text -----**<br>


**Figure 11-3. EDMA Controller Block Diagram** 

## _**11.2.3.1.1 Third-Party Channel Controller**_ 

The TPCC is the EDMA transfer scheduler responsible for scheduling, arbitrating, and issuing user programmed transfers to the two TPTCs. 

The functional block diagram below describes EDMA channel controller (EDMA_TPCC). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1039 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**==> picture [500 x 268] intentionally omitted <==**

## **Figure 11-4. EDMA Channel Controller Block Diagram** 

- A. Although the block is depicted twice in EDMA Channel Controller Block Diagram, there is only one physical register set for the QDMA to PaRAM set mapping block. 

The main blocks of the EDMA_TPCC are as follows: 

- Parameter RAM (PaRAM): The PaRAM maintains parameter sets for channel and reload parameter sets. The PaRAM must be written with the transfer context for the desired channels and link parameter sets. EDMA_TPCC processes and sets based on a trigger event and submits a transfer request (TR) to the transfer controllers. 

- EDMA event and interrupt processing registers: Allows mapping of events to parameter sets, enable/disable events, enable/disable interrupt conditions, and clearing interrupts. 

- Completion detection: The completion detect block detects completion of transfers by the EDMA_TPTCs or follower peripherals. The completion of transfers can be used optionally to chain trigger new transfers or to assert interrupts. 

- Event queues: Event queues form the interface between the event detection logic and the transfer request submission logic. 

- Memory protection registers: Memory protection registers define the accesses (privilege level and requestor(s)) that are allowed to access the DMA channel shadow region view(s) and regions of PaRAM. 

Other functions include the following: 

- Region registers: Region registers allow DMA resources (DMA channels and interrupts) to be assigned to unique regions that different EDMA programmers own (for example, DSPs). 

- Debug registers: Debug registers allow debug visibility by providing registers to read the queue status, controller status, and missed event status. 

The EDMA_TPCC includes two channel types: DMA channels (64 channels) and QDMA channels (8 channels). 

Each channel is associated with a given event queue/transfer controller and with a given PaRAM set. These channels are identical. The main difference between a DMA channel and a QDMA channel is the method that the system uses to trigger transfers. 

1040 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

- DMA channels are triggered by external events by the event set registers EDMA_TPCC_ESR and EDMA_TPCC_ESRH, or through chaining register EDMA_TPCC_CER. 

- QDMA channels are triggered automatically (auto-triggered) by the CPU. QDMAs allow a minimum number of linear writes to be issued to the TPCC to force a series of transfers to occur. 

The TPCC arbitrates among pending DMA and QDMA events with a fixed [64:1] and [8:1] priority encoder for these events, respectively (a low channel number corresponds to a high priority). 

DMA events are always higher priority than QDMA events. The higher-priority event is placed in the event queue to await submission to the transfer controllers, which occurs at the earliest opportunity. Each event queue is serviced in FIFO order, with a maximum of 16 queued events per event queue. If more than one TPTC is ready to be programmed with a transmission request (TR), the event queues are serviced with fixed priority: Q0 is higher than Q1. When an event is ready to be queued and the event queue and the TC channel are empty, the event bypasses the event queue and goes directly to the PaRAM processing logic for submission to the appropriate TC. If the transfer request TR bus or PaRAM processing are busy, the bypass path is not used. The bypass is not used to dequeue for a higher-priority event. 

Events are extracted from the event queue when the EDMA_TPTC is available for a new TR to be programmed into the EDMA_TPTC (signaled with the empty signal, indicating an empty program register set). As an event is extracted from the event queue, the associated PaRAM entry is processed and submitted to the TPTC as a TR. The TPCC updates the appropriate counts and addresses in the PaRAM entry in anticipation of the next trigger event for that PaRAM entry. 

The EDMA_TPCC also has an error detection logic that causes an error interrupt generation on various error conditions (for example: missed events EDMA_TPCC_EMR and EDMA_TPCC_EMRH registers, exceeding event queue thresholds in EDMA_TPCC_CCERR register, etc.). 

## _**11.2.3.1.2 Third-Party Transfer Controller**_ 

The TPTC module is the EDMA transfer engine that generates transfers as programmed in dedicated working registers, using two dedicated controller ports: a read-only port and a write-only port. 

Figure 11-5 shows a functional block diagram and of the EDMA transfer controller (EDMA_TPTC) and its connection to the EDMA_TPCC. 

**==> picture [468 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
SourceActive 64<br>64<br>Empty [1:0] Dst<br>64<br>64<br>Write status<br>**----- End of picture text -----**<br>


**Figure 11-5. TPTC Block Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1041 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## **Note** 

The port data bus width of the instances of the TPTC is fixed at 64 bits. 

Two instances of the EDMA_TPTC generate concurrent traffic on the L3_VBUSM interconnect. Each TC controller consists of the following components: 

- DMA Program Register Set: Stores the context for the DMA transfer that is loaded into the active register set when the current active register set completes. The CPU or TPCC programs the Program Register Set, not the active register set. For typical standalone operation, the CPU programs the Program Register while the TC services the Active register set. The Program Register set includes ownership control such that CPU software and the EDMA stay synchronized relative to one another. 

- Source Active Register Set : Stores the context (src/dst/cnt/etc) for the DMA Transfer Request (TR) in progress in the Read Controller. The Active register set is split into independent Source and Destination, because the source interconnect controller and the destination interconnect controller operate independently of one another. 

- Destination FIFO Register Set: Stores the context (src/dst/cnt/etc) for the DMA Transfer Request (TR) in progress, or pending, in the Write Controller. The pending register must allow the source controller to begin processing a new TR while the destination register set processes the previous TR. 

- Channel FIFO: Temporary holding buffer for in-flight data. The read return data of the source peripheral is stored in the Data FIFO, and then is written to the destination peripheral by the write command/data bus. 

- Read Controller/Interconnect Read Interface: The Interconnect read interface issues optimally sized read commands to the source peripheral, based on a burst size of 32 bytes and available landing space in the channel FIFO. 

- Write controller/Interconnect Write interface: The local interconnect write interface issues optimally sized write commands to the destination peripheral, based on a burst size of 32 bytes and available data in the channel FIFO. 

- Completion interface: sends completion codes to the EDMA_TPCC when a transfer completes and generates interrupts and chained events in the TPCC module. 

- Configuration port: Target interface that provides read/write access to program registers and read access to all memory-mapped TPTC registers. 

When one EDMA_TPTC module is idle and receive its first TR, DMA program register set receives the TR, where it transitions to the DMA source active set and the destination FIFO register set immediately. The second TR (if pending from EDMA_TPCC) is loaded into the DMA program set, ensuring it can start as soon as possible when the active transfer completes. As soon as the current active set is exhausted, the TR is loaded from the DMA program register set into the DMA source active register set as well as to the appropriate entry in the destination FIFO register set. 

The read controller issues read commands controlled by the rules of command fragmentation and optimization. These are issued only when the data FIFO has space available for the data read. When sufficient data is in the data FIFO, the write controller starts issuing a write command again following the rules for command fragmentation and optimization. 

Depending on the number of entries, the read controller can process up to two or four transfer requests ahead of the destination subject to the amount of free data FIFO. 

## **11.2.3.2 Types of EDMA Controller Transfers** 

An EDMA transfer is always defined in terms of three dimensions. Figure 11-6 shows the three dimensions used by EDMA controller transfers. These three dimensions are defined as: 

- 1st Dimension or Array (A): The 1st dimension in a transfer consists of EDMA_TPCC_ABCNT_n[15:0] ACNT contiguous bytes. 

- 2nd Dimension or Frame (B): The 2nd dimension in a transfer consists of EDMA_TPCC_ABCNT_n[31:16] BCNT arrays of ACNT bytes. Each array transfer in the 2nd dimension is separated from each other by an index programmed using bit-fields EDMA_TPCC_BIDX_n[15:0] SBIDX or EDMA_TPCC_BIDX_n[31:16] DBIDX. 

1042 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

- 3rd Dimension or Block (C): The 3rd dimension in a transfer consists of CCNT frames of BCNT arrays of ACNT bytes. The Count for 3rd Dimension is defined in PaRAM memory EDMA_TPCC_CCNT_n[15:0] CCNT. Each transfer in the 3rd dimension is separated from the previous by an index programmed using EDMA_TPCC_CIDX_n[15:0] SCIDX or EDMA_TPCC_CIDX_n[31:16] DCIDX. 

## **Note** 

The reference point for the index depends on the synchronization type. The amount of data transferred upon receipt of a trigger/synchronization event is controlled by the synchronization types (EDMA_TPCC_OPT_n[2] SYNCDIM bit). For these three dimensions, only two synchronization types are supported: A-synchronized transfers and AB-synchronized transfers. 

**==> picture [419 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
ACNT bytes in<br>Array/1st dimension<br>Frame 0 Array 1 Array 2 Array BCNT<br>Frame 1 Array 1 Array 2 Array BCNT CCNT frames in<br>Block/3rd dimmension<br>Frame CCNT Array 1 Array 2 Array BCNT<br>**----- End of picture text -----**<br>


BCNT arrays in Frame/2nd dimmension 

**==> picture [19 x 4] intentionally omitted <==**

**----- Start of picture text -----**<br>
edma-007<br>**----- End of picture text -----**<br>


## **Figure 11-6. Definition of ACNT, BCNT, and CCNT** 

## _**11.2.3.2.1 A-Synchronized Transfers**_ 

In an A-synchronized transfer, each EDMA sync event initiates the transfer of the 1st dimension of EDMA_TPCC_ABCNT_n[15:0] ACNT bytes, or one array of ACNT bytes. Each event/TR packet conveys the transfer information for one array only. Thus, BCNT × CCNT events are needed to completely service a PaRAM set. 

Arrays are always separated by EDMA_TPCC_BIDX_n[15:0]SBIDX and EDMA_TPCC_BIDX_n[31:16] DBIDX, as shown in Figure 11-7, where the start address of Array N is equal to the start address of Array N – 1 plus source (SRC) or destination (DST) in EDMA_TPCC_BIDX_n register. 

Frames are always separated by EDMA_TPCC_CIDX_n[15:0] SCIDX and EDMA_TPCC_CIDX_n[31:16] DCIDX. For A-synchronized transfers, after the frame is exhausted, the address is updated by adding SRCCIDX/ DSTCIDX to the beginning address of the last array in the frame. As in Figure 11-7, SRCCIDX / DSTCIDX is the difference between the start of Frame 0 Array 3 to the start of Frame 1 Array 0. 

Figure 11-7 shows an A-synchronized transfer of 3 (CCNT) frames of 4 (BCNT) arrays of n (ACNT) bytes. In this example, a total of 12 sync events (BCNT × CCNT) exhaust a PaRAM set. See Figure 11-7 for details on parameter set updates. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1043 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**==> picture [326 x 219] intentionally omitted <==**

**----- Start of picture text -----**<br>
(SRC|DST) (SRC|DST) (SRC|DST) Each array submit<br>as one TR<br>BIDX BIDX BIDX<br>Frame 0 Array 0 Array 1 Array 2 Array 3<br>(SRC|DST)<br>CIDX<br>(SRC|DST) (SRC|DST) (SRC|DST)<br>BIDX BIDX BIDX<br>Frame 1 Array 0 Array 1 Array 2 Array 3<br>(SRC|DST)<br>CIDX<br>(SRC|DST) (SRC|DST) (SRC|DST)<br>BIDX BIDX BIDX<br>Frame 2 Array 0 Array 1 Array 2 Array 3<br>edma-008<br>**----- End of picture text -----**<br>


**Figure 11-7. A-Synchronized Transfers (ACNT = n, BCNT = 4, CCNT = 3)** 

1044 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## _**11.2.3.2.2 AB-Synchronized Transfers**_ 

In a AB-synchronized transfer, each EDMA sync event initiates the transfer of 2 dimensions or one frame. Each event/TR packet conveys information for one entire frame of BCNT_n arrays of ACNT_n bytes. Thus, EDMA_TPCC_CCNT_n events are needed to completely service a PaRAM set. 

Arrays are always separated by EDMA_TPCC_BIDX_n[15:0] SBIDX and EDMA_TPCC_BIDX_n[31:16] DBIDX as shown in Figure 11-8. Frames are always separated by SRCCIDX and DSTCIDX. 

Note that for AB-synchronized transfers, after a TR for the frame is submitted, the address update is to add EDMA_TPCC_CIDX_n[15:0] SCIDX / EDMA_TPCC_CIDX_n[31:16] DCIDX to the beginning address of the beginning array in the frame. This is different from A-synchronized transfers where the address is updated by adding SRCCIDX/DSTCIDX to the start address of the last array in the frame. See Section 11.2.3.3.6 for details on parameter set updates. 

Figure 11-8 shows an AB-synchronized transfer of 3 (CCNT) frames of 4 (BCNT) arrays of _n_ (ACNT) bytes. In this example, a total of 3 sync events (CCNT) exhaust a PaRAM set; that is, a total of 3 transfers of 4 arrays each completes the transfer. 

**==> picture [318 x 223] intentionally omitted <==**

**----- Start of picture text -----**<br>
AB_Sync transfer<br>(SRC|DST) (SRC|DST) (SRC|DST) BCNT arrays submit<br>as one TR<br>BIDX BIDX BIDX<br>Frame 0 Array 0 Array 1 Array 2 Array 3<br>(SRC|DST)<br>CIDX<br>(SRC|DST) (SRC|DST) (SRC|DST)<br>BIDX BIDX BIDX<br>Frame 1 Array 0 Array 1 Array 2 Array 3<br>(SRC|DST)<br>CIDX<br>(SRC|DST) (SRC|DST) (SRC|DST)<br>BIDX BIDX BIDX<br>Frame 2 Array 0 Array 1 Array 2 Array 3<br>edma-009<br>**----- End of picture text -----**<br>


**Figure 11-8. AB-Synchronized Transfers (ACNT = n, BCNT = 4, CCNT = 3)** 

## **Note** 

ABC-synchronized transfers are not directly supported. It can be logically achieved by chaining between multiple AB-synchronized transfers. 

## **11.2.3.3 Parameter RAM (PaRAM)** 

The EDMA controller is a RAM-based architecture. The transfer context (source/destination addresses, count, indexes, etc.) for DMA or QDMA channels is programmed in a parameter RAM table in EDMA_TPCC. The PaRAM table is segmented into multiple PaRAM sets. Each PaRAM set includes eight four-byte PaRAM set entries (32-bytes total per PaRAM set), which includes typical DMA transfer parameters such as source address, destination address, transfer counts, indexes, options, etc. 

The PaRAM structure supports flexible ping-pong, circular buffering, channel chaining, and auto-reloading (linking). 

The contents of the PaRAM include the following: 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1045 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

- 256 PaRAM sets 

- 64 channels that are direct mapped and can be used as link for QDMA sets if not used for DMA channels 

- 8 channels remain for link or QDMA sets 

By default, all channels map to PaRAM set to 0 and should be remapped before use by EDMA_TPCC_DCHMAPN_m and EDMA_TPCC_QCHMAPN_j registers. This can be done in the device boot flow. 

**Table 11-7. EDMA Parameter RAM Contents** 

|**PaRAM Set Number**|**Base Address**|**Parameters**(1)|
|---|---|---|
|0<br>EDMA Base Address + 4000h to EDMA Base<br>Address + 401Fh<br>PaRAM set 0<br>1<br>EDMA Base Address + 4020h to EDMA Base<br>Address + 403Fh<br>PaRAM set 1<br>2<br>EDMA Base Address + 4040h to EDMA Base<br>Address + 405Fh<br>PaRAM set 2<br>3<br>EDMA Base Address + 4060h to EDMA Base<br>Address + 407Fh<br>PaRAM set 3<br>4<br>EDMA Base Address + 4080h to EDMA Base<br>Address + 409Fh<br>PaRAM set 4<br>5<br>EDMA Base Address + 40A0h to EDMA Base<br>Address + 40BFh<br>PaRAM set 5<br>6<br>EDMA Base Address + 40C0h to EDMA Base<br>Address + 40DFh<br>PaRAM set 6<br>7<br>EDMA Base Address + 40E0h to EDMA Base<br>Address + 40FFh<br>PaRAM set 7<br>8<br>EDMA Base Address + 4100h to EDMA Base<br>Address + 411Fh<br>PaRAM set 8<br>9<br>EDMA Base Address + 4120h to EDMA Base<br>Address + 413Fh<br>PaRAM set 9<br>...<br>...<br>...<br>63<br>EDMA Base Address + 47E0h to EDMA Base<br>Address + 47FFh<br>PaRAM set 63<br>64<br>EDMA Base Address + 4800h to EDMA Base<br>Address + 481Fh<br>PaRAM set 64<br>65<br>EDMA Base Address + 4820h to EDMA Base<br>Address + 483Fh<br>PaRAM set 65<br>...<br>...<br>...<br>127<br>EDMA Base Address + 5000h to EDMA Base<br>Address + 4FE0h<br>PaRAM set 127<br>128<br>EDMA Base Address + 5020h to EDMA Base<br>Address + 503Fh<br>PaRAM set 128<br>129<br>EDMA Base Address + 5040h to EDMA Base<br>Address + 505Fh<br>PaRAM set 129<br>130<br>EDMA Base Address + 5060h to EDMA Base<br>Address + 507Fh<br>PaRAM set 130<br>...<br>...<br>...<br>256<br>EDMA Base Address + 6000h to EDMA Base<br>Address + 601Fh<br>PaRAM set 256|||



(1) The device has 8 QDMA channels that can be mapped to any parameter set number from 0 to 256. 

## **Note** 

AM263Px has a maximum of 256 PaRAM sets. Additional tables and diagrams in this chapter may show a larger number (up to 511), however 256 is the maximum allowed number of entries. 

1046 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## _**11.2.3.3.1 PaRAM**_ 

Each parameter set of PaRAM is organized into eight 32-bit words or 32 bytes, as shown in PaRAM Set and described in EDMA Channel Parameter Description. Each PaRAM set consists of 16-bit and 32-bit parameters. 

**==> picture [428 x 253] intentionally omitted <==**

**Figure 11-9. PaRAM Set** 

**Note** 

Figure above is a representation of 128 bit entries. For device specific details please refer to EDMA configuration chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1047 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**Table 11-8. EDMA Channel Parameter Description** 

|**Offset Address**<br>**(bytes)**|**Acronym**|**Parameter**|**Description**|
|---|---|---|---|
|0h|OPT<br>Channel Options<br>EDMA_TPCC_OPT_n register<br>Transfer configuration options|||
|4h|SRC<br>Channel Source Address<br>EDMA_TPCC_SRC_n register<br>The byte address from which data is transferred|||
|8h(1)|ACNT<br>Count for 1st Dimension<br>EDMA_TPCC_ABCNT_n[15:0]<br>ACNT bit-field.<br>Unsigned value specifying the number of contiguous bytes<br>within an array (first dimension of the transfer). Valid values<br>range from 1 to 65 535.|||
||BCNT<br>Count for 2nd Dimension<br>EDMA_TPCC_ABCNT_n[31:16]<br>BCNT bit-field.<br>Unsigned value specifying the number of arrays in a frame,<br>where an array is ACNT bytes. Valid values range from 1 to<br>65 535.|||
|Ch|DST<br>Channel Destination Address<br>EDMA_TPCC_DST_n register<br>The byte address to which data is transferred|||
|10h(1)|SBIDX<br>Source BCNT Index<br>EDMA_TPCC_BIDX_n[15:0]<br>SBIDX bit-field.<br>Signed value specifying the byte address offset between<br>source arrays within a frame (2nd dimension). Valid values<br>range from –32 768 and 32 767.|||
||DBIDX<br>Destination BCNT Index<br>EDMA_TPCC_BIDX_n[31:16]<br>DBIDX bit-field.<br>Signed value specifying the byte address offset between<br>destination arrays within a frame (2nd dimension). Valid<br>values range from –32 768 and 32 767.|||
|14h(1)|LINK<br>Link Address<br>EDMA_TPCC_LNK_n[15:0] LINK<br>bit-field<br>The PaRAM address containing the PaRAM set to be linked<br>(copied from) when the current PaRAM set is exhausted. A<br>value of FFFFh specifies a null link.|||
||BCNTRLD<br>BCNT Reload<br>EDMA_TPCC_LNK_n[31:16]<br>BCNTRLD bit-field<br>The count value used to reload BCNT when BCNT<br>decrements to 0 (TR is submitted for the last array in 2nd<br>dimension). Only relevant in A-synchronized transfers.|||
|18h(1)|SCIDX<br>Source CCNT index.<br>EDMA_TPCC_CIDX_n[15:0]<br>SCIDX bit-field.<br>Signed value specifying the byte address offset between<br>frames within a block (3rd dimension). Valid values range<br>from –32 768 and 32 767.<br>A-synchronized transfers: The byte address offset from the<br>beginning of the last source array in a frame to the beginning<br>of the first source array in the next frame.<br>AB-synchronized transfers: The byte address offset from the<br>beginning of the first source array in a frame to the beginning<br>of the first source array in the next frame.|||
||DCIDX<br>Destination CCNT index.<br>EDMA_TPCC_CIDX_n[31:16]<br>DCIDX bit-field.<br>Signed value specifying the byte address offset between<br>frames within a block (3rd dimension). Valid values range<br>from –32 768 and 32 767.<br>A-synchronized transfers: The byte address offset from the<br>beginning of the last destination array in a frame to the<br>beginning of the first destination array in the next frame.<br>AB-synchronized transfers: The byte address offset from the<br>beginning of the first destination array in a frame to the<br>beginning of the first destination array in the next frame.|||
|1Ch|CCNT<br>Count for 3rd Dimension.<br>EDMA_TPCC_CCNT_n[15:0]<br>CCNT bit-field.<br>Unsigned value specifying the number of frames in a block,<br>where a frame is BCNT arrays of ACNT bytes. Valid values<br>range from 1 to 65 535.|||
||Reserved<br>Reserved<br>Reserved. Always write 0 to this bit; writes of 1 to this bit are<br>not supported and attempts cam result in undefined behavior.|||



(1) If OPT, SRC, or DST is the trigger word for a QDMA transfer, then it is required to do a 32-bit access to that field. Furthermore, it is recommended to perform only 32-bit accesses on the parameter RAM for best code compatibility. For example, switching the endianness of the processor swaps addresses of the 16-bit fields, but 32-bit accesses avoid the issue entirely. 

1048 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## _**11.2.3.3.2 EDMA Channel PaRAM Set Entry Fields**_ 

## _**11.2.3.3.2.1 Channel Options Parameter (OPT)**_ 

This is the control register for TPCC channel configuration options. Refer to the EDMA_TPCC_OPT_n register bitfield description in the AM263Px Register Addendum for additional details. 

## _**11.2.3.3.2.2 Channel Source Address (SRC)**_ 

The 32-bit source address parameter specifies the starting byte address of the source. For SAM in increment mode, there are no alignment restrictions imposed by EDMA. For SAM in FIFO addressing mode, it must program the source address to be aligned to a 256-bit aligned address (5 LSBs of address must be 0). If this rule is not observed, the EDMA_TPTC returns an error. Refer to Section 11.2.3.12.3 _Error Generation_ for additional details. 

## _**11.2.3.3.2.3 Channel Destination Address (DST)**_ 

The 32-bit destination address parameter specifies the starting byte address of the destination. For DAM in increment mode, there are no alignment restrictions imposed by EDMA. For DAM in FIFO addressing mode, it must program the destination address to be aligned to a 256-bit aligned address (5 LSBs of address must be 0). If this rule is not observed, the EDMA_TPTC returns an error. Refer to _Error Generation_ for additional details. 

## _**11.2.3.3.2.4 Count for 1st Dimension (ACNT)**_ 

EDMA_TPCC_ABCNT_n[15:0] ACNT represents the number of bytes within the 1st dimension of a transfer. ACNT is a 16-bit unsigned value with valid values between 1 and 65535. Therefore, the maximum number of bytes in an array is 65 535 bytes (64K – 1 bytes). ACNT must be greater than or equal to 1 for a TR to be submitted to EDMA_TPTC. A transfer with ACNT equal to 0 is considered either a null or dummy transfer. A dummy or null transfer generates a completion code depending on the settings of the completion bit fields in EDMA_TPCC_OPT_n. 

Refer to Section 11.2.3.3.5 _Dummy Versus Null Transfer Comparison_ and Section 11.2.3.5.3 _Dummy or Null Completion_ for details on dummy/null completion conditions. 

## _**11.2.3.3.2.5 Count for 2nd Dimension (BCNT)**_ 

EDMA_TPCC_ABCNT_n[15:0] BCNT is a 16-bit unsigned value that specifies the number of arrays of length ACNT. For normal operation, valid values for BCNT are between 1 and 65 535. Therefore, the maximum number of arrays in a frame is 65 535 (64K – 1 arrays). A transfer with BCNT equal to 0 is considered either a null or dummy transfer. A dummy or null transfer generates a completion code depending on the settings of the completion bit fields in EDMA_TPCC_OPT_n. 

Refer to Section 11.2.3.3.5 _Dummy Versus Null Transfer Comparison_ and Section 11.2.3.5.3 _Dummy or Null Completion_ for details on dummy/null completion conditions. 

## _**11.2.3.3.2.6 Count for 3rd Dimension (CCNT)**_ 

EDMA_TPCC_CCNT_n[15:0] CCNT is a 16-bit unsigned value that specifies the number of frames in a block. Valid values for CCNT are between 1 and 65 535. Therefore, the maximum number of frames in a block is 65 535 (64K – 1 frames). A transfer with CCNT equal to 0 is considered either a null or dummy transfer. A dummy or null transfer generates a completion code depending on the settings of the completion bit fields in EDMA_TPCC_OPT_n. 

A CCNT value of 0 is considered either a null or dummy transfer. 

Refer to Section 11.2.3.3.5 _Dummy Versus Null Transfer Comparison_ and Section 11.2.3.5.3 _Dummy or Null Completion_ for details on dummy/null completion conditions. 

## _**11.2.3.3.2.7 BCNT Reload (BCNTRLD)**_ 

EDMA_TPCC_LNK_n[31:16] BCNTRLD is a 16-bit unsigned value used to reload the EDMA_TPCC_ABCNT_n[15:0] BCNT field once the last array in the 2nd dimension is transferred. This field is only used for A-synchronized transfers. In this case, the EDMA_TPCC decrements the BCNT value by 1 on 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1049 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

each TR submission. When BCNT reaches 0, the EDMA_TPCC decrements CCNT and uses the BCNTRLD value to reinitialize the BCNT value. 

For AB-synchronized transfers, the EDMA_TPCC submits the BCNT in the TR and the EDMA_TPTC decrements BCNT appropriately. For AB-synchronized transfers, BCNTRLD is not used. 

## _**11.2.3.3.2.8 Source B Index (SBIDX)**_ 

EDMA_TPCC_BIDX_n[15:0] SBIDX is a 16-bit signed value (2s complement) used for source address modification between each array in the 2nd dimension. Valid values for EDMA_TPCC_BIDX_n[15:0] SBIDX are between –32 768 and 32 767. It provides a byte address offset from the beginning of the source array to the beginning of the next source array. It applies to both A-synchronized and AB-synchronized transfers. Some examples: 

- EDMA_TPCC_BIDX_n[15:0] SBIDX = 0000h (0): no address offset from the beginning of an array to the beginning of the next array. All arrays are fixed to the same beginning address. 

- EDMA_TPCC_BIDX_n[15:0] SBIDX = 0003h (+3): the address offset from the beginning of an array to the beginning of the next array in a frame is 3 bytes. For example, if the current array begins at address 1000h, the next array begins at 1003h. 

- EDMA_TPCC_BIDX_n[15:0] SBIDX = FFFFh (–1): the address offset from the beginning of an array to the beginning of the next array in a frame is –1 byte. For example, if the current array begins at address 5054h, the next array begins at 5053h. 

## _**11.2.3.3.2.9 Destination B Index (DBIDX)**_ 

EDMA_TPCC_BIDX_n[31:16] DBIDX is a 16-bit signed value (2s complement) used for destination address modification between each array in the 2nd dimension. Valid values for EDMA_TPCC_BIDX_n[31:16] DBIDX are between –32 768 and 32 767. It provides a byte address offset from the beginning of the destination array to the beginning of the next destination array within the current frame. It applies to both A-synchronized and AB-synchronized transfers. Refer to Section 11.2.3.3.2.8 _Source B Index (SBIDX)_ for examples. 

## _**11.2.3.3.2.10 Source C Index (SCIDX)**_ 

EDMA_TPCC_CIDX_n[15:0] SCIDX is a 16-bit signed value (2s complement) used for source address modification in the 3rd dimension. Valid values for EDMA_TPCC_CIDX_n[15:0] SCIDX are between –32 768 and 32 767. It provides a byte address offset from the beginning of the current array (pointed to by SRC address) to the beginning of the first source array in the next frame. It applies to both A-synchronized and AB-synchronized transfers. 

## **Note** 

When SCIDX is applied, the current array in an A-synchronized transfer is the last array in the frame (Figure 11-7), while the current array in an AB-synchronized transfer is the first array in the frame (Figure 11-8). 

## _**11.2.3.3.2.11 Destination C Index (DCIDX)**_ 

EDMA_TPCC_CIDX_n[31:16] DCIDX is a 16-bit signed value (2s complement) used for destination address modification in the 3rd dimension. Valid values are between –32 768 and 32 767. It provides a byte address offset from the beginning of the current array (pointed to by DST address) to the beginning of the first destination array TR in the next frame. It applies to both A-synchronized and AB-synchronized transfers. 

## **Note** 

When DCIDX is applied, the current array in an A-synchronized transfer is the last array in the frame (Figure 11-7), while the current array in a AB-synchronized transfer is the first array in the frame (Figure 11-8). 

1050 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## _**11.2.3.3.2.12 Link Address (LINK)**_ 

The EDMA_TPCC provides a mechanism, called linking, to reload the current PaRAM set upon its natural termination (that is, after the count fields are decremented to 0) with a new PaRAM set. The 16-bit parameter EDMA_TPCC_LNK_n[15:0] LINK specifies the byte address offset in the PaRAM from which the EDMA_TPCC loads/reloads the next PaRAM set during linking. 

It must program the link address to point to a valid aligned 32-byte PaRAM set. The 5 LSBs of the LINK field should be cleared to 0. 

The EDMA_TPCC ignores the upper 2 bits of the LINK entry, allowing the flexibility of programming the link address as either an absolute/literal byte address or use the PaRAM-base-relative offset address. Therefore, if it use the literal address with a range from 4000h to 7FFFh, it will be treated as a PaRAM-base-relative value of 0000h to 3FFFh. 

It should check that the programed value in the EDMA_TPCC_LNK_n[15:0] LINK field is correctly, so that link update is requested from a PaRAM address that falls in the range of the available PaRAM addresses on the device. 

Value of FFFFh in EDMA_TPCC_LNK_n[15:0] LINK bit-field is referred to as a NULL link that should cause the EDMA_TPCC to perform an internal write of 0 to all entries of the current PaRAM set, except for the EDMA_TPCC_LNK_n[15:0] LINK field is set to FFFFh. Also, see Section 11.2.3.5 _Completion of a DMA Transfer_ for details on terminating a transfer. 

## _**11.2.3.3.3 Null PaRAM Set**_ 

A null PaRAM set is defined as a PaRAM set where all count fields (EDMA_TPCC_ABCNT_n[15:0] ACNT, EDMA_TPCC_ABCNT_n[31:16] BCNT, and EDMA_TPCC_CCNT_n[15:0] CCNT) are cleared to 0. If a PaRAM set associated with a channel is a NULL set, then when serviced by the EDMA_TPCC, the bit corresponding to the channel is set in the associated event missed register (EDMA_TPCC_EMR, EDMA_TPCC_EMRH, or EDMA_TPCC_QEMR). This bit remains set in the associated secondary event register (EDMA_TPCC_SER, EDMA_TPCC_SERH, or EDMA_TPCC_QSER). 

_This implies that any future events on the same channel are ignored by the EDMA_TPCC and it is required to clear the bit in EDMA_TPCC_SER, EDMA_TPCC_SERH, or EDMA_TPCC_QSER for the channel._ This is considered an error condition, since events are not expected on a channel that is configured as a null transfer. 

## _**11.2.3.3.4 Dummy PaRAM Set**_ 

A dummy PaRAM set is defined as a PaRAM set where at least one of the count fields (EDMA_TPCC_ABCNT_n[15:0] ACNT, EDMA_TPCC_ABCNT_n[31:16] BCNT, or EDMA_TPCC_CCNT_n[15:0] CCNT) is cleared to 0 and at least one of the count fields is nonzero. 

If a PaRAM set associated with a channel is a dummy set, then when serviced by the EDMA_TPCC, it will not set the bit corresponding to the channel (DMA/QDMA) in the event missed register (EDMA_TPCC_EMR, EDMA_TPCC_EMRH, or EDMA_TPCC_QEMR) and the secondary event register (EDMA_TPCC_SER, EDMA_TPCC_SERH, or EDMA_TPCC_QSER) bit gets cleared similar to a normal transfer. Future events on that channel are serviced. A dummy transfer is a legal transfer of 0 bytes. 

## _**11.2.3.3.5 Dummy Versus Null Transfer Comparison**_ 

There are some differences in the way the EDMA_TPCC logic treats a dummy versus a null transfer request. A null transfer request is an error condition, but a dummy transfer is a legal transfer of 0 bytes. A null transfer causes an error bit (E _n_ ) in EDMA_TPCC_EMR to get set and the E _n_ bit in EDMA_TPCC_SER remains set, essentially preventing any further transfers on that channel without clearing the associated error registers. 

Table 11-9 summarizes the conditions and effects of null and dummy transfer requests. 

**Table 11-9. Dummy and Null Transfer Request** 

|**Feature**|**Null TR**|**Dummy TR**|
|---|---|---|
|EDMA_TPCC_EMR / EDMA_TPCC_EMRH / EDMA_TPCC_QEMR is set<br>Yes<br>No<br>EDMA_TPCC_SER / EDMA_TPCC_SERH / EDMA_TPCC_QSER remains set<br>Yes<br>No|||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1051 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**Table 11-9. Dummy and Null Transfer Request (continued)** 

|**Feature**|**Null TR**|**Dummy TR**|
|---|---|---|
|Link update (STATIC = 0 in EDMA_TPCC_OPT_n)<br>Yes<br>Yes<br>EDMA_TPCC_QER is set<br>Yes<br>Yes<br>EDMA_TPCC_IPR / EDMA_TPCC_IPRH, EDMA_TPCC_CER /<br>EDMA_TPCC_CERH is set using early completion<br>Yes<br>Yes|||



## _**11.2.3.3.6 Parameter Set Updates**_ 

When a TR is submitted for a given DMA/QDMA channel and its corresponding PaRAM set, the EDMA_TPCC is responsible for updating the PaRAM set in anticipation of the next trigger event. For events that are not final, this includes address and count updates; for final events, this includes the link update. 

The specific PaRAM set entries that are updated depend on the channel’s synchronization type (A-synchronized or AB-synchronized) and the current state of the PaRAM set. A B-update refers to the decrementing of EDMA_TPCC_ABCNT_n[31:16] BCNT in the case of A-synchronized transfers after the submission of successive TRs. A C-update refers to the decrementing of CCNT in the case of A-synchronized transfers after BCNT TRs for EDMA_TPCC_ABCNT_n[15:0] ACNT byte transfers have submitted. For AB-synchronized transfers, a C-update refers to the decrementing of EDMA_TPCC_CCNT_n[15:0] CCNT after submission of every transfer request. 

Refer to Table 11-10 for details and conditions on the parameter updates. A link update occurs when the PaRAM set is exhausted, as described in Section 11.2.3.3.7 _Linking Transfers_ . 

After the TR is read from the PaRAM (and is in process of being submitted to EDMA_TPTC), the following fields are updated if needed: 

- A-synchronized: BCNT, CCNT, SRC, DST. 

- AB-synchronized: CCNT, SRC, DST. 

The following fields are not updated (except for during linking, where all fields are overwritten by the link PaRAM set): 

- A-synchronized: EDMA_TPCC_ABCNT_n[15:0] ACNT, EDMA_TPCC_LNK_n[31:16] BCNTRLD, EDMA_TPCC_BIDX_n[15:0] SBIDX, EDMA_TPCC_BIDX_n[31:16] DBIDX, EDMA_TPCC_CIDX_n[15:0] SCIDX, EDMA_TPCC_CIDX_n[31:16] DCIDX, EDMA_TPCC_OPT_n, EDMA_TPCC_LNK_n[15:0]LINK. 

- AB-synchronized: EDMA_TPCC_ABCNT_n[15:0] ACNT, EDMA_TPCC_ABCNT_n[31:16] BCNT, EDMA_TPCC_LNK_n[31:16] BCNTRLD, EDMA_TPCC_BIDX_n[15:0] SBIDX, EDMA_TPCC_BIDX_n[31:16] DBIDX, EDMA_TPCC_CIDX_n[15:0] SCIDX, EDMA_TPCC_CIDX_n[31:16] DCIDX, EDMA_TPCC_OPT_n, EDMA_TPCC_LNK_n[15:0]LINK. 

## **Note** 

PaRAM updates only pertain to the information that is needed to properly submit the next transfer request to the EDMA_TPTC. Updates that occur while data is moved within a transfer request are tracked within the transfer controller, and is detailed in Section 11.2.3.12 _EDMA Transfer Controller (EDMA_TPTC)_ . For A-synchronized transfers, the EDMA_TPCC always submits a TRP for EDMA_TPCC_ABCNT_n[15:0] ACNT bytes (EDMA_TPCC_ABCNT_n[31:16] BCNT = 1 and EDMA_TPCC_CCNT_n[15:0] CCNT = 1). For AB-synchronized transfers, the EDMA_TPCC always submits a TRP for EDMA_TPCC_ABCNT_n[15:0] ACNT bytes of BCNT arrays (EDMA_TPCC_CCNT_n[15:0] CCNT = 1). The EDMA_TPTC is responsible for updating source and destination addresses within the array based on EDMA_TPCC_ABCNT_n[15:0] ACNT and EDMA_TPCC_OPT_n[10:8] FWID. For AB-synchronized transfers, the EDMA_TPTC is also responsible to update source and destination addresses between arrays based on EDMA_TPCC_BIDX_n[15:0] SBIDX and EDMA_TPCC_BIDX_n[31:16] DBIDX. 

Table 11-10 shows the details of parameter updates that occur within EDMA_TPCC for A-synchronized and AB-synchronized transfers. 

1052 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

**Table 11-10. Parameter Updates in EDMA_TPCC (for Non-Null, Non-Dummy PaRAM Set)** 

||**A-Synchronized Transfer**|**A-Synchronized Transfer**|**A-Synchronized Transfer**|**AB-Synchronized Transfer**|**AB-Synchronized Transfer**|**AB-Synchronized Transfer**|
|---|---|---|---|---|---|---|
||**B-Update**|**C-Update**|**Link Update**|**B-Update**|**C-Update**|**Link Update**|
|**Conditio**<br>**n:**|**BCNT > 1**|**BCNT ==**<br>**1 &&**<br>**CCNT > 1**|**BCNT == 1 &&**<br>**CCNT == 1**|**N/A**|**EDMA_TPCC_CC**<br>**NT_n[15:0] CCNT**<br>**> 1**|**EDMA_TPCC_CCNT_n[15:0]**<br>**CCNT == 1**|
|SRC<br>DST<br>ACNT<br>BCNT<br>CCNT<br>SBIDX<br>DBIDX<br>SCIDX<br>DCIDX<br>LINK<br>BCNTRL<br>D<br>OPT(1)|+= SBIDX += SCIDX = Link.EDMA_TPCC_SRC_n<br>+= DBIDX += DCIDX = Link.EDMA_TPCC_DST_n<br>None<br>None<br>=<br>Link.EDMA_TPCC_ABCNT_n[1<br>5:0] ACNT<br>–= 1<br>=<br>BCNTRLD<br>=<br>Link.EDMA_TPCC_ABCNT_n[3<br>1:16] BCNT<br>None<br>–= 1<br>=<br>Link.EDMA_TPCC_CCNT_n[15:<br>0] CCNT<br>None<br>None<br>=<br>Link.EDMA_TPCC_BIDX_n[15:<br>0] SBIDX<br>None<br>None<br>=<br>Link.EDMA_TPCC_BIDX_n[31:<br>16] DBIDX<br>None<br>None<br>=<br>Link.EDMA_TPCC_BIDX_n[15:<br>0] SBIDX<br>None<br>None<br>=<br>Link.EDMA_TPCC_BIDX_n[31:<br>16] DBIDX<br>None<br>None<br>=<br>Link.EDMA_TPCC_LNK_n[15:0<br>]LINK<br>None<br>None<br>=<br>Link.EDMA_TPCC_LNK_n[31:1<br>6] BCNTRLD<br>None<br>None<br>= LINK.EDMA_TPCC_OPT_n|||in<br>EDMA_TPT<br>C<br>+= SCIDX<br>= Link.EDMA_TPCC_SRC_n<br>in<br>EDMA_TPT<br>C<br>+= DCIDX<br>= Link.EDMA_TPCC_DST_n<br>None<br>None<br>=<br>Link.EDMA_TPCC_ABCNT_n[15:0]<br>ACNT<br>in<br>EDMA_TPT<br>C<br>N/A<br>=<br>Link.EDMA_TPCC_ABCNT_n[31:1<br>6] BCNT<br>in<br>EDMA_TPT<br>C<br>-=1<br>= Link.EDMA_TPCC_CCNT_n[15:0]<br>CCNT<br>in<br>EDMA_TPT<br>C<br>None<br>= Link.EDMA_TPCC_BIDX_n[15:0]<br>SBIDX<br>None<br>None<br>=<br>Link.EDMA_TPCC_BIDX_n[31:16]<br>DBIDX<br>in<br>EDMA_TPT<br>C<br>None<br>= Link.EDMA_TPCC_BIDX_n[15:0]<br>SBIDX<br>None<br>None<br>=<br>Link.EDMA_TPCC_BIDX_n[31:16]<br>DBIDX<br>None<br>None<br>=<br>Link.EDMA_TPCC_LNK_n[15:0]LIN<br>K<br>None<br>None<br>= Link.EDMA_TPCC_LNK_n[31:16]<br>BCNTRLD<br>None<br>None<br>= LINK.EDMA_TPCC_OPT_n|||



(1) In all cases, no updates occur if EDMA_TPCC_OPT_n[3] STATIC == 1 for the current PaRAM set. 

## **Note** 

The EDMA_TPCC includes no special hardware to detect when an indexed address update calculation overflows/underflows. The address update will wrap across boundaries as programmed by the user. It should ensure that no transfer is allowed to cross internal port boundaries between peripherals. A single TR must target a single source/destination peripheral endpoint. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1053 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## _**11.2.3.3.7 Linking Transfers**_ 

The EDMA_TPCC provides a mechanism known as linking, which allows the entire PaRAM set to be reloaded from a location within the PaRAM memory map (for both DMA and QDMA channels). Linking is especially useful for maintaining ping-pong buffers, circular buffering, and repetitive/continuous transfers with no CPU intervention. Upon completion of a transfer, the current transfer parameters are reloaded with the parameter set pointed that the 16-bit link address field of the current parameter set points to. Linking only occurs when the EDMA_TPCC_OPT_n[3] STATIC bit is cleared. 

## **Note** 

It should always link a transfer (EDMA or QDMA) to another useful transfer. If it must terminate a transfer, then link the transfer to a NULL parameter set. Refer to Section 11.2.3.3.3 _Null PaRAM Set_ . 

The link update occurs after the current PaRAM set event parameters have been exhausted. An event's parameters are exhausted when the EDMA channel controller has submitted all of the transfers that are associated with the PaRAM set. 

A link update occurs for null and dummy transfers depending on the state of the EDMA_TPCC_OPT_n[3] STATIC bit and the EDMA_TPCC_LNK_n[15:0] LINK field. In both cases (null or dummy), if the value of EDMA_TPCC_LNK_n[15:0] LINK is FFFFh, then a null PaRAM set (with all 0s and EDMA_TPCC_LNK_n[15:0] LINK set to FFFFh) is written to the current PaRAM set. 

Similarly, if EDMA_TPCC_LNK_n[15:0] LINK is set to a value other than FFFFh, then the appropriate PaRAM location that EDMA_TPCC_LNK_n[15:0] LINK points to is copied to the current PaRAM set. 

Once the channel completion conditions are met for an event, the transfer parameters that are located at the link address are loaded into the current DMA or QDMA channel’s associated parameter set. This indicates that the EDMA_TPCC reads the entire set (eight words) from the PaRAM set specified by EDMA_TPCC_LNK_n[15:0] LINK and writes all eight words to the PaRAM set that is associated with the current channel. Figure 11-10 shows an example of a linked transfer. 

1054 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**==> picture [500 x 602] intentionally omitted <==**

**Figure 11-10. Linked Transfer** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1055 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## **Note** 

AM263/Px has a maximum of 256 PaRAM sets. Additional tables and diagrams in this chapter may show a larger number (up to 511), however 256 is the maximum allowed number of entries. 

Any PaRAM set in the PaRAM can be used as a link/reload parameter set. The PaRAM sets associated with peripheral synchronization events (refer to Section 11.2.3.6 _Event, Channel, and PaRAM Mapping_ ) only use for linking if the corresponding events are disabled. 

If a PaRAM set location is defined as a QDMA channel PaRAM set (by EDMA_TPCC_QCHMAPN_j register), then copying the link PaRAM set into the current QDMA channel PaRAM set is recognized as a trigger event. It is latched in EDMA_TPCC_QER because a write to the trigger word was performed. This feature is used to create a linked list of transfers using a single QDMA channel and multiple PaRAM sets. Refer to Section 11.2.3.4.2 _QDMA Channels_ . 

Linking to itself replicates the behavior of auto-initialization, thus facilitating the use of circular buffering and repetitive transfers. After an EDMA channel exhausts its current PaRAM set, it reloads all of the parameter set entries from another PaRAM set, which is initialized with values that are identical to the original PaRAM set. Figure 11-11 shows an example of a linked to self transfer. Here, the PaRAM set 511 has the link field pointing to the address of parameter set 511 (linked to self). 

1056 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

**==> picture [416 x 530] intentionally omitted <==**

**----- Start of picture text -----**<br>
(a) At initialization PaRAM set 3<br>Byte Set OPT X<br>address # PaRAM SRC X<br>EDMA Base Address + 4000h 0 Parameter set 0 BCNT X ACNT X<br>EDMA Base Address + 4020h 1 Parameter set 1 DST X<br>EDMA Base Address + 4040h 2 Parameter set 2 DBIDX X SBIDX X<br>EDMA Base Address + 4060h 3 Parameter set 3 BCNTRLD X Link=7FE0h<br>DCIDX X SCIDX X<br>Reserved CCNT X<br>PaRAM set 511<br>OPT X<br>EDMA Base Address + 7FC0h 510 Parameter set 510<br>SRC X<br>EDMA Base Address + 7FE0h 511 Parameter set 511<br>BCNT X ACNT X<br>DST X<br>DBIDX Y SBIDX X<br>BCNTRLD X Link=7FE0h<br>DCIDX X SCIDX X<br>Reserved CCNT X<br>(b) After completion of PaRAM set 3<br>(link update) PaRAM set 3<br>Byte Set OPT X<br>address # PaRAM<br>SRC X<br>EDMA Base Address + 4000h 0 Parameter set 0 BCNT X ACNT X<br>EDMA Base Address + 4020h 1 Parameter set 1 DST X<br>EDMA Base Address + 4040h 2 Parameter set 2 DBIDX X SBIDX X<br>EDMA Base Address + 4060h 3 Parameter set 3 BCNTRLD X Link=7FE0h<br>DCIDX X SCIDX X<br>Reserved CCNT X<br>Link<br>PaRAM set 511<br>update<br>EDMA Base Address + 7FC0h 510 Parameter set 510 OPT X<br>SRC X<br>EDMA Base Address + 7FE0h 511 Parameter set 511<br>BCNT X ACNT X<br>DST X<br>DBIDX X SBIDX X<br>(c) After completion of PaRAM set 127 BCNTRLD X Link=7FE0h<br>(link to self) DCIDX X SCIDX X<br>Byte Set Reserved CCNT X<br>address # PaRAM<br>EDMA Base Address + 4000h 0 Parameter set 0<br>EDMA Base Address + 4020h 1 Parameter set 1 PaRAM set 3<br>EDMA Base Address + 4040h 2 Parameter set 2 OPT X<br>EDMA Base Address + 4060h 3 Parameter set 3 SRC X<br>BCNT X ACNT X<br>DST X<br>DBIDX X SBIDX X<br>BCNTRLD X Link=7FE0h<br>EDMA Base Address + 7FC0h 510 Parameter set 510 DCIDX X SCIDX X<br>EDMA Base Address + 7FE0h 511 Parameter set 511 Reserved CCNT X<br>edma-012<br>**----- End of picture text -----**<br>


**Figure 11-11. Link-to-Self Transfer** 

## **Note** 

If the in EDMA_TPCC_OPT_n[3] STATIC bit is set for a PaRAM set, then link updates are not performed. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1057 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## _**11.2.3.3.8 Constant Addressing Mode Transfers/Alignment Issues**_ 

If either EDMA_TPCC_OPT_n[0] SAM or EDMA_TPCC_OPT_n[1] DAM is set (constant addressing mode), then the source or destination address must be aligned to a 256-bit aligned address, respectively, and the corresponding EDMA_TPCC_BIDX_n is an even multiple of 32 bytes (256 bits). The EDMA_TPCC does not recognize errors here, but the EDMA_TPTC asserts an error if this is not true. Refer to Section 11.2.3.12.3 _Error Generation_ . 

## **Note** 

The constant addressing (CONST) mode has limited applicability. The EDMA is configured for the constant addressing mode (EDMA_TPCC_OPT_n[0] SAM / EDMA_TPCC_OPT_n[1] DAM = 1) only if the transfer source or destination (on-chip memory, off-chip memory controllers, target peripherals) support the constant addressing mode. If the constant addressing mode is not supported, the similar logical transfer can be achieved using the increment (INCR) mode (EDMA_TPCC_OPT_n[0] SAM / EDMA_TPCC_OPT_n[1] DAM =0) by appropriately programming the count and indices values. 

## _**11.2.3.3.9 Element Size**_ 

The EDMA controller does not use element-size and element-indexing. Instead, all transfers are defined in terms of all three dimensions: EDMA_TPCC_ABCNT_n[15:0] ACNT, EDMA_TPCC_ABCNT_n[31:16] BCNT, and EDMA_TPCC_CCNT_n[15:0] CCNT. An element-indexed transfer is logically achieved by programming EDMA_TPCC_ABCNT_n[15:0] ACNT to the size of the element and EDMA_TPCC_ABCNT_n[31:16] BCNT to the number of elements that need to be transferred. For example: If there are 16-bit audio data and 256 audio samples that must be transferred to a serial port, therefore the EDMA_TPCC_ABCNT_n[15:0] ACNT = 2 (2 bytes) and EDMA_TPCC_ABCNT_n[31:16] BCNT = 256. 

## **11.2.3.4 Initiating a DMA Transfer** 

There are multiple ways to initiate a programmed data transfer using the EDMA_TPCC channel controller. Transfers on DMA channels are initiated by three sources. 

They are listed as follows: 

- **Event-triggered transfer request** (this is the typical usage of EDMA controller): A peripheral, system, or externally-generated event triggers a transfer request. 

- **Manually-triggered transfer request:** The CPU manually triggers a transfer by writing a 1 to the corresponding bit in the event set registers (EDMA_TPCC_ESR / EDMA_TPCC_ESRH). 

- **Chain-triggered transfer request:** A transfer is triggered on the completion of another transfer or subtransfer. 

Transfers on QDMA channels are initiated by two sources. They are as follows: 

- **Auto-triggered transfer request:** Writing to the programmed trigger word triggers a transfer. 

- **Link-triggered transfer requests:** Writing to the trigger word triggers the transfer when linking occurs. 

## _**11.2.3.4.1 DMA Channels**_ 

## _**11.2.3.4.1.1 Event-Triggered Transfer Request**_ 

When an event is asserted from a peripheral or device pins, it gets latched in the corresponding bit of the event register (EDMA_TPCC_ER[31:0] E _n_ = 1). For more information about peripheral events to EDMA events mapping, refer to _the device data manual_ . 

If the corresponding event in the event enable register (EDMA_TPCC_EER) is enabled 

(EDMA_TPCC_EER[31:0] E _n_ = 1), then the EDMA_TPCC prioritizes and queues the event in the appropriate event queue. When the event reaches the head of the queue, it is evaluated for submission as a transfer request to the transfer controller. 

If the PaRAM set is valid (not a NULL set), then a transfer request packet (TRP) is submitted to the EDMA_TPTC and the EDMA_TPCC_ER[31:0] E _n_ bit is cleared. At this point, a new event can be safely received by the EDMA_TPCC. 

1058 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

If the PaRAM set associated with the channel is a NULL set (see Section 11.2.3.3.3 _Null PaRAM Set_ ), then no transfer request (TR) is submitted and the corresponding EDMA_TPCC_ER[31:0] E _n_ bit is cleared and simultaneously the corresponding channel bit is set in the event miss register (EDMA_TPCC_EMR[31:0] E _n_ = 1) to indicate that the event was discarded due to a null TR being serviced. Good programming practices should include cleaning the event missed error before re-triggering the DMA channel. 

When an event is received, the corresponding event bit in the event register is set (EDMA_TPCC_ER[31:0] E _n_ = 1), regardless of the state of EDMA_TPCC_EER[31:0] E _n_ . If the event is disabled when an external event is received (EDMA_TPCC_ER[31:0] E _n_ = 1 and EDMA_TPCC_EER[31:0] E _n_ = 0), the EDMA_TPCC_ER[31:0] E _n_ bit remains set. If the event is subsequently enabled (EDMA_TPCC_EER[31:0] E _n_ = 1), then the pending event is processed by the EDMA_TPCC and the TR is processed/submitted, after which the EDMA_TPCC_ER[31:0] E _n_ bit is cleared. 

If an event is being processed (prioritized or is in the event queue) and another sync event is received for the same channel prior to the original being cleared (EDMA_TPCC_ER[31:0] E _n_ != 0), then the second event is registered as a missed event in the corresponding bit of the event missed register (EDMA_TPCC_EMR[31:0] E _n_ = 1). 

## _**11.2.3.4.1.2 Manually-Triggered Transfer Request**_ 

The CPU or any peripheral device module initiates a DMA transfer by writing to the event set register EDMA_TPCC_ESR. Writing a 1 to an event bit in the EDMA_TPCC_ESR results in the event being prioritized/ queued in the appropriate event queue, regardless of the state of the EDMA_TPCC_EER[31:0] E _n_ bit. When the event reaches the head of the queue, it is evaluated for submission as a transfer request to the transfer controller. 

As in the event-triggered transfers, if the PaRAM set associated with the channel is valid (it is not a null set) then the TR is submitted to the associated EDMA_TPTC and the channel can be triggered again. 

If the PaRAM set associated with the channel is a NULL set (see Section 11.2.3.3.3 _Null PaRAM Set_ ), then no transfer request (TR) is submitted and the corresponding EDMA_TPCC_ER[31:0] E _n_ bit is cleared and simultaneously the corresponding channel bit is set in the event miss register EDMA_TPCC_EMR[31:0] E _n_ = 1 to indicate that the event was discarded due to a null TR being serviced. Good programming practices should include clearing the event missed error before re-triggering the DMA channel. 

If an event is being processed (prioritized or is in the event queue) and the same channel is manually set by a write to the corresponding channel bit of the event set register EDMA_TPCC_ESR[31:0] E _n_ = 1 prior to the original being cleared EDMA_TPCC_ESR[31:0] E _n_ = 0, then the second event is registered as a missed event in the corresponding bit of the event missed register EDMA_TPCC_EMR[31:0] E _n_ = 1. 

## _**11.2.3.4.1.3 Chain-Triggered Transfer Request**_ 

Chaining is a mechanism by which the completion of one transfer automatically sets the event for another channel. When a chained completion code is detected, the value of which is dictated by the transfer completion code EDMA_TPCC_OPT_n[17:12] TCC of the PaRAM set associated with the channel, it results in the corresponding bit in the chained event register EDMA_TPCC_CER to be set EDMA_TPCC_CER[31:0] E[TCC] = 1). 

Once a bit is set in EDMA_TPCC_CER, the EDMA_TPCC prioritizes and queues the event in the appropriate event queue. When the event reaches the head of the queue, it is evaluated for submission as a transfer request to the transfer controller. 

As in the event-triggered transfers, if the PaRAM set associated with the channel is valid (it is not a null set) then the TR is submitted to the associated EDMA_TPTC and the channel can be triggered again. 

If the PaRAM set associated with the channel is a NULL set (see Section 11.2.3.3.3 _Null PaRAM Set_ ), then no transfer request (TR) is submitted and the corresponding EDMA_TPCC_CER[31:0] E _n_ bit is cleared and simultaneously the corresponding channel bit is set in the event miss register EDMA_TPCC_EMR[31:0] E _n_ = 1 to indicate that the event was discarded due to a null TR being serviced. In this case, the error condition must 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1059 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

be cleared before the DMA channel can be re-triggered. Good programming practices might include clearing the event missed error before re-triggering the DMA channel. 

If a chaining event is being processed (prioritized or queued) and another chained event is received for the same channel prior to the original being cleared EDMA_TPCC_CER[31:0] E _n_ != 0), then the second chained event is registered as a missed event in the corresponding channel bit of the event missed register EDMA_TPCC_EMR[31:0] E _n_ = 1. 

## **Note** 

Chained event registers EDMA_TPCC_CER, event registers EDMA_TPCC_ER, and event set registers EDMA_TPCC_ESR operate independently. An event E _n_ can be triggered by any of the trigger sources (event-triggered, manually-triggered, or chain-triggered). 

## _**11.2.3.4.2 QDMA Channels**_ 

## _**11.2.3.4.2.1 Auto-Triggered and Link-Triggered Transfer Request**_ 

QDMA-based transfer requests are issued when a QDMA event gets latched in the QDMA event register EDMA_TPCC_QER[31:0] E _n_ = 1. A bit corresponding to a QDMA channel is set in the QDMA event register EDMA_TPCC_QER when the following occurs: 

- A CPU (or any device module) write occurs to a PaRAM address that is defined as a QDMA channel trigger word (programmed in the QDMA channel mapping register EDMA_TPCC_QCHMAPN_j for the particular QDMA channel and the QDMA channel is enabled via the QDMA event enable register EDMA_TPCC_QEER[31:0] E _n_ = 1. 

- EDMA_TPCC performs a link update on a PaRAM set address that is configured as a QDMA channel matches EDMA_TPCC_QCHMAPN_j settings and the corresponding channel is enabled via the QDMA event enable register EDMA_TPCC_QEER[31:0] E _n_ = 1. 

Once a bit is set in EDMA_TPCC_QER, the EDMA_TPCC prioritizes and queues the event in the appropriate event queue. When the event reaches the head of the queue, it is evaluated for submission as a transfer request to the transfer controller. 

As in the event-triggered transfers, if the PaRAM set associated with the channel is valid (it is not a null set) then the TR is submitted to the associated EDMA_TPTC and the channel can be triggered again. 

If a bit is already set in EDMA_TPCC_QER[31:0] E _n_ = 1 and a second QDMA event for the same QDMA channel occurs prior to the original being cleared, the second QDMA event gets captured in the QDMA event miss register EDMA_TPCC_QEMR[7:0] E _n_ = 1. 

## _**11.2.3.4.3 Comparison Between DMA and QDMA Channels**_ 

The primary difference between DMA and QDMA channels is the event/channel synchronization. 

QDMA events are either auto-triggered or link triggered. Auto-triggering allows QDMA channels to be triggered by CPU(s) with a minimum number of linear writes to PaRAM. Link triggering allows a linked list of transfers to be executed, using a single QDMA PaRAM set and multiple link PaRAM sets. 

A QDMA transfer is triggered when a CPU (or other device modules) writes to the trigger word of the QDMA channel parameter set (auto-triggered) or when the EDMA_TPCC performs a link update on a PaRAM set that has been mapped to a QDMA channel (link triggered). 

## **Note** 

The CPUs triggered (manually triggered) DMA channels, in addition to writing to the PaRAM set, it is required to write to the event set register EDMA_TPCC_ESR to kick-off the transfer. 

QDMA channels are typically for cases where a single event accomplishes a complete transfer since the CPU (or other device modules) must reprogram some portion of the QDMA PaRAM set in order to re-trigger the channel. QDMA transfers are programmed with EDMA_TPCC_ABCNT_n[31:0] BCNT =1 and 

1060 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

EDMA_TPCC_CCNT_n[15:0] CCNT = 1 for A-synchronized transfers, and EDMA_TPCC_CCNT_n[15:0] CCNT = 1 for AB-synchronized transfers. 

Additionally, since linking is also supported (if EDMA_TPCC_OPT_n[3] STATIC = 0) for QDMA transfers, it allows to initiate a linked list of QDMAs, so when EDMA_TPCC copies over a link PaRAM set (including the write to the trigger word), the current PaRAM set mapped to the QDMA channel automatically recognizes as a valid QDMA event and initiate another set of transfers as specified by the linked set. 

## **11.2.3.5 Completion of a DMA Transfer** 

A parameter set for a given channel is complete when the required number of transfer requests is submitted (based on receiving the number of synchronization events). The expected number of TRs for a non-null/ non-dummy transfer is shown in Table 11-11 for both synchronization types along with state of the PaRAM set prior to the final TR being submitted. When the counts (EDMA_TPCC_ABCNT_n[31:0] BCNT and/or EDMA_TPCC_CCNT_n[15:0] CCNT) are this value, the next TR results in: 

- Final chaining or interrupt codes sent by the transfer controllers (instead of intermediate). 

- Link updates (linking to either null or another valid link set). 

**Table 11-11. Expected Number of Transfers for Non-Null Transfer** 

|**Sync Mode**|**Counts at time 0**|**Total # Transfers**|**Counts prior to final TR**|
|---|---|---|---|
|A-synchronized<br>ACNT<br>BCNT<br>CCNT<br>(BCNT × CCNT ) TRs of ACNT bytes each<br>EDMA_TPCC_ABCNT_n[31:0]<br>BCNT == 1 &&<br>EDMA_TPCC_CCNT_n[15:0] CCNT<br>== 1||||
|AB-synchronized<br>ACNT<br>BCNT<br>CCNT<br>CCNT TRs for ACNT × BCNT bytes each<br>EDMA_TPCC_CCNT_n[15:0] CCNT<br>== 1||||



The PaRAM OPT field must program with a specific transfer completion code TCC or EDMA_TPCC_OPT_n[17:12] TCC along with the other EDMA_TPCC_OPT_n fields ([22] TCCHEN, [20] TCINTEN, [23] ITCCHEN, and [21] ITCINTEN bits) to indicate whether the completion code is to be used for generating a chained event or/and for generating an interrupt upon completion of a transfer. 

The specific EDMA_TPCC_OPT_n[17:12] TCC value (6-bit binary value) programmed dictates which of the 64bits in the chain event register EDMA_TPCC_CER [TCC] and/or interrupt pending register EDMA_TPCC_IPR [TCC] is set. 

It can selectively program whether the transfer controller sends back completion codes on completion of the final transfer request (TR) of a parameter set EDMA_TPCC_OPT_n[22] TCCHEN or EDMA_TPCC_OPT_n[20] TCINTEN, for all but the final transfer request (TR) of a parameter set EDMA_TPCC_OPT_n[23] ITCCHEN or EDMA_TPCC_OPT_n[21] ITCINTEN), or for all TRs of a parameter set (both). Refer to Section 11.2.3.8 _Chaining EDMA Channels_ for details on chaining (intermediate/final chaining) and Section 11.2.3.9 _EDMA Interrupts_ for details on intermediate/final interrupt completion. 

A completion detection interface exists between the EDMA channel controller and transfer controller(s). This interface sends back information from the transfer controller to the channel controller to indicate that a specific transfer is completed. Completion of a transfer is used for generating chained events and/or generating interrupts to the CPU(s). 

All DMA/QDMA PaRAM sets must also specify a link address value. For repetitive transfers such as ping-pong buffers, the link address value must point to another predefined PaRAM set. Alternatively, a non-repetitive transfer must set the link address value to the null link value. The null link value is defined as FFFFh. Refer to Section 11.2.3.3.7 _Linking Transfers_ for more details. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1061 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## **Note** 

Any incoming events that are mapped to a null PaRAM set results in an error condition. The error condition must clear before the corresponding channel is used again. Refer to Section 11.2.3.3.5 _Dummy Versus Null Transfer Comparison_ . 

There are three ways the EDMA_TPCC gets updated/informed about a transfer completion: normal completion, early completion, and dummy/null completion. This applies to both chained events and completion interrupt generation. 

## _**11.2.3.5.1 Normal Completion**_ 

In normal completion mode EDMA_TPCC_OPT_n[11] TCCMODE = 0, the transfer or sub-transfer is considered to be complete when the EDMA channel controller receives the completion codes from the EDMA transfer controller. In this mode, the completion code to the channel controller is posted by the transfer controller after it receives a signal from the destination peripheral. Normal completion is typically used to generate an interrupt to inform the CPU that a set of data is ready for processing. 

## _**11.2.3.5.2 Early Completion**_ 

In early completion mode EDMA_TPCC_OPT_n[11] TCCMODE = 1, the transfer is considered to be complete when the EDMA channel controller submits the transfer request (TR) to the EDMA transfer controller. In this mode, the channel controller generates the completion code internally. Early completion is typically useful for chaining, as it allows subsequent transfers to be chained-triggered while the previous transfer is still in progress within the transfer controller, maximizing the overall throughput of the set of the transfers. 

## _**11.2.3.5.3 Dummy or Null Completion**_ 

This is a variation of early completion. Dummy or null completion is associated with a dummy set Section 11.2.3.3.4 or null set Section 11.2.3.3.3. In both cases, the EDMA channel controller does not submit the associated transfer request to the EDMA transfer controller(s). However, if the set (dummy/null) has the OPT field programmed to return completion code (intermediate/final interrupt/chaining completion), then it sets the appropriate bits in the interrupt pending registers EDMA_TPCC_IPR and EDMA_TPCC_IPRH or chained event register EDMA_TPCC_CER and EDMA_TPCC_CERH. The internal early completion path is used by the channel controller to return the completion codes internally (that is, EDMA_TPCC generates the completion code). 

## **11.2.3.6 Event, Channel, and PaRAM Mapping** 

Several of the 64 DMA channels are tied to a specific hardware event, thus allowing events from device peripherals or external hardware (via the dma_evt[3:0] pins) to trigger transfers. A DMA channel typically requests a data transfer when it receives its event (apart from manually-triggered, chain-triggered, and other transfers). The amount of data transferred per synchronization event depends on the channel’s configuration (EDMA_TPCC_ABCNT_n[15:0] ACNT, EDMA_TPCC_ABCNT_n[31:16] BCNT, EDMA_TPCC_CCNT_n[15:0] CCNT, etc.) and the synchronization type (A-synchronized or AB-synchronized). 

The association of an event to a channel is fixed within the EDMA Channel Controller, that is, each DMA channel has one specific event associated with it. 

In an application, if a channel does not use the associated synchronization event or if it does not have an associated synchronization event (unused), that channel can be used for manually-triggered or chainedtriggered transfers, for linking/reloading, or as a QDMA channel. 

## _**11.2.3.6.1 DMA Channel to PaRAM Mapping**_ 

The mapping between the DMA channel numbers and the PaRAM sets is programmable (see _Parameter RAM (PaRAM)_ ). The DMA channel mapping registers EDMA_TPCC_DCHMAPN_m in the EDMA_TPCC provide programmability that allows the DMA channels to be mapped to any of the PaRAM sets in the PaRAM memory map. Figure 11-12 illustrates the use of EDMA_TPCC_DCHMAPN_m. There is one EDMA_TPCC_DCHMAPN_m register per channel. 

1062 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

**==> picture [426 x 255] intentionally omitted <==**

**----- Start of picture text -----**<br>
DCHMAPN_m QCHMAPN_j<br>31 14 13 5 4 0 31 1413 5 4 2 1 0<br>00  0000  0000  0000  0000 PAENTRY 00000 00  0000  0000  0000  0000 PAENTRY TR WORD 00<br>Byte<br>Byte Set address<br>address # PaRAM PaRAM set offset<br>EDMA Base Address + 4000h 0 Parameter set 0 OPT +0h<br>EDMA Base Address + 4020h 1 Parameter set 1 SRC +4h<br>EDMA Base Address + 4040h 2 Parameter set 2 BCNT ACNT +8h<br>EDMA Base Address + 4060h 3 Parameter set 3 DST +Ch<br>DBIDX SBIDX +10h<br>BCNTRLD LINK +14h<br>DCIDX SCIDX +18h<br>Reserved CCNT<br>+1Ch<br>EDMA Base Address + 7FC0h 510 Parameter set 510<br>EDMA Base Address + 7FE0h 511 Parameter set 511<br>edma-013<br>**----- End of picture text -----**<br>


**Figure 11-12. DMA Channel and QDMA Channel to PaRAM Mapping** 

## **Note** 

## _**11.2.3.6.2 QDMA Channel to PaRAM Mapping**_ 

The mapping between the QDMA channels and the PaRAM sets is programmable. The QDMA channel mapping register EDMA_TPCC_QCHMAPN_j in the EDMA_TPCC allows to map the QDMA channels to any of the PaRAM sets in the PaRAM memory map. Figure 11-13 illustrates the use of EDMA_TPCC_QCHMAPN_j. 

EDMA_TPCC_QCHMAPN_j[4:2] TRWORD bit-field allows to program the trigger word in the PaRAM set for the QDMA channel. A trigger word is one of the eight words in the PaRAM set. For a QDMA transfer to occur, a valid TR synchronization event for EDMA_TPCC is a write to the trigger word in the PaRAM set pointed to by EDMA_TPCC_QCHMAPN_j for a particular QDMA channel. By default, QDMA channels are mapped to PaRAM set 0. 

It must appropriately re-map PaRAM set 0 before use. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1063 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**==> picture [452 x 267] intentionally omitted <==**

**----- Start of picture text -----**<br>
QCHMAPN_j<br>31 14 13 5 4 2 1 0<br>PAENTRY TRWORD<br>QCHMAPn 0000 0000 0000 00 00<br>00 0000 01 1 111<br>Byte Set<br>address # PaRAM Byte<br>EDMA Base Address + 4000h 0 Parameter set 0 address<br>EDMA Base Address + 4020h 1 Parameter set 1 offset<br>PaRAM set<br>EDMA Base Address + 4040h 2 Parameter set 2<br>OPT +0h<br>EDMA Base Address + 4060h 3 Parameter set 3<br>SRC +4h<br>BCNT ACNT +8h<br>DST +Ch<br>DBIDX SBIDX +10h<br>BCNTRLD LINK +14h<br>DCIDX SCIDX +18h<br>Reserved CCNT +1Ch<br>EDMA Base Address + 7FC0h 510 Parameter set 510<br>EDMA Base Address + 7FE0h 511 Parameter set 511<br>edma-014<br>**----- End of picture text -----**<br>


**Figure 11-13. QDMA Channel to PaRAM Mapping** 

## **11.2.3.7 EDMA Channel Controller Regions** 

The EDMA channel controller divides its address space into eight regions. Individual channel resources are assigned to a specific region, where each region is typically assigned to a specific device module uses the EDMA controller. 

Application software can use regions or to ignore them altogether. It can be used active memory protection in conjunction with regions so that only a specific device module which uses the EDMA (for example, privilege identification) or privilege level (for example, user vs. supervisor) is allowed access to a given region, and thus to a given DMA or QDMA channel. This allows robust system-level DMA code where each EDMA initiator only modifies the state of the assigned resources. Memory protection is described in Section 11.2.3.10 _Memory Protection_ . 

## _**11.2.3.7.1 Region Overview**_ 

The EDMA channel controller memory-mapped registers are divided in three main categories: 

1. Global registers 

2. Global region channel registers 

3. Shadow region channel registers 

The global registers are located at a single/fixed location in the EDMA_TPCC memory map. These registers control EDMA resource mapping and provide debug visibility and error tracking information. 

The channel registers (including DMA, QDMA, and interrupt registers) are accessible via the global channel region address range, or in the shadow _n_ channel region address range(s). For example, the event enable register EDMA_TPCC_EER is visible at the global address of EDMA Base Address + 1020h or region addresses of EDMA Base Address + 2020h for region 0, EDMA Base Address + 2220h for region 1, … EDMA Base Address + 2E20h for region 7. 

The DMA region access enable registers EDMA_TPCC_DRAEM_k and the QDMA region access enable registers EDMA_TPCC_QRAEN_k control the underlying control register bits that are accessible via the shadow region address space (except for EDMA_TPCC_IEVAL and EDMA_TPCC_IEVAL_RN_k registers). Table 11-12 

1064 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

lists the registers in the shadow region memory map. Refer to _EDMA_TPCC register mapping summary_ for the complete global and shadow region memory maps. 

**Table 11-12. Shadow Region Registers** 

|**EDMA_TPCC_DRAE**<br>**M_k**|**EDMA_TPCC_DRAE**<br>**HM_k**|**EDMA_TPCC_QRAE**<br>**N_k**|
|---|---|---|
|EDMA_TPCC_ER<br>EDMA_TPCC_ERH<br>EDMA_TPCC_QER<br>EDMA_TPCC_ECR<br>EDMA_TPCC_ECRH<br>EDMA_TPCC_QEER<br>EDMA_TPCC_ESR<br>EDMA_TPCC_ESRH<br>EDMA_TPCC_QEEC<br>R<br>EDMA_TPCC_CER<br>EDMA_TPCC_CERH<br>EDMA_TPCC_QEES<br>R<br>EDMA_TPCC_EER<br>EDMA_TPCC_EERH<br>EDMA_TPCC_EECR<br>EDMA_TPCC_EECR<br>H<br>EDMA_TPCC_EESR<br>EDMA_TPCC_EESR<br>H<br>EDMA_TPCC_SER<br>EDMA_TPCC_SERH<br>EDMA_TPCC_SECR<br>EDMA_TPCC_SECR<br>H<br>EDMA_TPCC_IER<br>EDMA_TPCC_IERH<br>EDMA_TPCC_IECR<br>EDMA_TPCC_IECRH<br>EDMA_TPCC_IESR<br>EDMA_TPCC_IESRH<br>EDMA_TPCC_IPR<br>EDMA_TPCC_IPRH<br>EDMA_TPCC_ICR<br>EDMA_TPCC_ICRH|||
|**Register not affected by DRAE\DRAEH**|||
|EDMA_TPCC_IEVAL|||
|EDMA_TPCC_IEVAL<br>_RN_k|||



Figure 11-14 illustrates the conceptual view of the regions. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1065 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**==> picture [499 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
Shadow region 0 Physical register<br>Access address EDMA_TPCC_ER, ERH EDMA_TPCC_ER, ERH EDMABase<br>EDMA Base Address + 2000h EDMA_TPCC_DRAEM_0 EDMA_TPCC_ECR, ECRH Address + 1000h<br>EDMA Base Address + 2094h EDMA_TPCC_DRAEHM_0 EDMA_TPCC_ESR, ESRH<br>except IEV AL EDMA_TPCC_QSECR EDMA_TPCC_QRAEN_0 EDMA_TPCC_CER, CERH<br>EDMA_TPCC_IEVAL, EDMA_TPCC_EER, EERH<br>EDMA_TPCC_IEVAL_RN_k EDMA_TPCC_EECR, EECRH<br>Shadow region 0 EDMA_TPCC_EESR, EESRH<br>registers EDMA_TPCC_SER, SERH<br>EDMA_TPCC_SECR, SECRH<br>EDMA_TPCC_IER, IERH<br>EDMA_TPCC_IECR,<br>EDMA_TPCC_IESR,<br>EDMA_TPCC_IPR,<br>EDMA_TPCC_ICR,<br>EDMA_TPCC_IEVAL, IEVAL_RN_k<br>Shadow region 7<br>EDMA_TPCC_QER<br>EDMA_TPCC_ER, ERH<br>EDMA_TPCC_QEER<br>Access address EDMA_TPCC_DRAEM_7 EDMA_TPCC_QEECR<br>EDMA Base Address + 2E00h EDMA_TPCC_DRAEHM_7 EDMA_TPCC_QEESR<br>EDMA Base Address + 2E94h EDMA_TPCC_QSECR EDMA_TPCC_QRAEN_7 EDMA_TPCC_QSER EDMA<br>EDMA_TPCC_IEVAL EDMA_TPCC_QSECR Base<br>EDMA_TPCC_IEVAL_RN_k Address + 1094h<br>Shadow region 7 edma-015<br>registers<br>**----- End of picture text -----**<br>


**Figure 11-14. Shadow Region Registers** 

## _**11.2.3.7.2 Channel Controller Regions**_ 

There are eight EDMA shadow regions (and associated memory maps). Associated with each shadow region are a set of registers defining which channels and interrupt completion codes belong to that region. These registers are user-programmed per region to assign ownership of the DMA/QDMA channels to a region. 

- EDMA_TPCC_DRAEM_k and EDMA_TPCC_DRAEHM_k: One register pair exists for each of the shadow regions. The number of bits in each register pair matches the number of DMA channels (64 DMA channels). These registers need to be programmed to assign ownership of DMA channels and interrupt (or EDMA_TPCC_OPT_n[17:12] TCC codes) to the respective region. Accesses to DMA and interrupt registers via the shadow region address view are filtered through the DRAEM/DRAEHM pair. A value of 1 in the corresponding EDMA_TPCC_DRAEM_k[31:0] / EDMA_TPCC_DRAEHM_k[31:0] bit implies that the corresponding DMA interrupt channel is accessible; a value of 0 in the corresponding EDMA_TPCC_DRAEM_k[31:0] / EDMA_TPCC_DRAEHM_k[31:0] bit forces writes to be discarded and returns a value of 0 for reads. 

- EDMA_TPCC_QRAEN_k: One register exists for every region. The number of bits in each register matches the number of QDMA channels (8 QDMA channels). These registers must be programmed to assign ownership of QDMA channels to the respective region. To enable a channel in a shadow region using shadow region 0 EDMA_TPCC_QEER, the corresponding bits in QRAE must be set or writing into EDMA_TPCC_QEESR there will be no the desired effect. 

- EDMA_TPCC_MPPAN_k and EDMA_TPCC_MPPAG: One register exists for every region. This register defines the privilege level, requestor, and types of accesses allowed to a region's memory-mapped registers. 

It is typical for an application to have a unique assignment of QDMA/DMA channels (and, therefore, a given bit position) to a given region. 

The use of shadow regions allows restricted access to EDMA resources (DMA channels, QDMA channels, TCC, interrupts) by tasks in a system by setting or clearing bits in the EDMA_TPCC_DRAEM_k / EDMA_TPCC_QRAEN_k registers. 

If exclusive access to any given channel / TCC code is required for a region, then only that region's EDMA_TPCC_DRAEM_k / EDMA_TPCC_QRAEN_k have the associated bit set. 

1066 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## _**Example 11-1. Resource Pool Division Across Two Regions**_ 

This example illustrates a resource pool division across two regions, assuming region 0 must be allocated 16 DMA channels (0-15) and 1 QDMA channel (0) and 32 TCC codes (0-15 and 48-63). 

Region 1 needs to be allocated 16 DMA channels (16-32) and the remaining 7 QDMA channels (1-7) and TCC codes (16-47). 

EDMA_TPCC_DRAEM_k should be equal to the OR of the bits that are required for the DMA channels and the TCC codes: 

```
Region 0: DRAEHM, DRAEM = 0xFFFF0000, 0x0000FFFF QRAEN = 0x0000001
Region 1: DRAEHM, DRAEM = 0x0000FFFF, 0xFFFF0000 QRAEN = 0x00000FE
```

## _**11.2.3.7.3 Region Interrupts**_ 

In addition to the EDMA_TPCC global completion interrupt, there is an additional completion interrupt line that is associated with every shadow region. Along with the interrupt enable register EDMA_TPCC_IER, DRAEM acts as a secondary interrupt enable for the respective shadow region interrupts. Refer to _Hardware Request_ for more information about EDMA Interrupts. 

## **11.2.3.8 Chaining EDMA Channels** 

The channel chaining capability for the EDMA allows the completion of an EDMA channel transfer to trigger another EDMA channel transfer. The purpose is to allow the ability to chain several events through one event occurrence. 

Chaining is different from linking (Section 11.2.3.3.7 _Linking Transfers_ ). The EDMA link feature reloads the current channel parameter set with the linked parameter set. The EDMA chaining feature does not modify or update any channel parameter set. It provides a synchronization event to the chained channel (see Section 11.2.3.4.1.3 _Chain-Triggered Transfer Request_ ). 

Chaining is achieved at either final transfer completion or intermediate transfer completion, or both, of the current channel. Consider a channel _m_ (DMA/QDMA) required to chain to channel _n_ . Channel number _n_ (0-63) needs to be programmed into the EDMA_TPCC_OPT_n[17:12] TCC bit-field of channel _m_ channel options parameter (OPT) set. 

- If final transfer completion chaining EDMA_TPCC_OPT_n[22] TCCHEN = 1 is enabled, the chain-triggered event occurs after the submission of the last transfer request of channel _m_ is either submitted or completed (depending on early or normal completion). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1067 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

- If intermediate transfer completion chaining EDMA_TPCC_OPT_n[23] ITCCHEN = 1 is enabled, the chaintriggered event occurs after every transfer request, except the last of channel _m_ is either submitted or completed (depending on early or normal completion). 

- If both final and intermediate transfer completion chaining (EDMA_TPCC_OPT_n[22] TCCHEN = 1 and EDMA_TPCC_OPT_n[23] ITCCHEN = 1) are enabled, then the chain-trigger event occurs after every transfer request is submitted or completed (depending on early or normal completion). 

Table 11-13 illustrates the number of chain event triggers occurring in different synchronized scenarios. Consider channel 31 programmed with EDMA_TPCC_ABCNT_n[15:0] ACNT = 3, EDMA_TPCC_ABCNT_n[31:16] BCNT = 4, EDMA_TPCC_CCNT_n[15:0] CCNT = 5, and EDMA_TPCC_OPT_n[17:12] TCC = 30. 

**Table 11-13. Chain Event Triggers** 

||**(Number of chained event triggers on channel 30)**|**(Number of chained event triggers on channel 30)**|
|---|---|---|
|**Options**|**A-Synchronized**|**AB-Synchronized**|
|EDMA_TPCC_OPT_n[22] TCCHEN = 1,<br>EDMA_TPCC_OPT_n[23] ITCCHEN = 0<br>1 (Owing to the last TR)<br>1 (Owing to the last TR)<br>EDMA_TPCC_OPT_n[22] TCCHEN = 0,<br>EDMA_TPCC_OPT_n[23] ITCCHEN = 1<br>19 (Owing to all but the last TR)<br>4 (Owing to all but the last TR)<br>EDMA_TPCC_OPT_n[22] TCCHEN = 1,<br>EDMA_TPCC_OPT_n[23] ITCCHEN = 1<br>20 (Owing to a total of 20 TRs)<br>5 (Owing to a total of 5 TRs)|||



## **11.2.3.9 EDMA Interrupts** 

The EDMA interrupts are divided into 2 categories: transfer completion interrupts and error interrupts. 

There are nine region interrupts, eight shadow regions and one global region. The transfer completion interrupts are listed in Table 11-14. The transfer completion interrupts and the error interrupts from the transfer controllers are all routed to the device interrupt controllers INTCs. 

**Table 11-14. EDMA Transfer Completion Interrupts** 

|**Name**|**Description**|
|---|---|
|EDMA_TPCC_INT0<br>EDMA_TPCC Transfer Completion Interrupt Shadow Region 0<br>EDMA_TPCC_INT1<br>EDMA_TPCC Transfer Completion Interrupt Shadow Region 1<br>EDMA_TPCC_INT2<br>EDMA_TPCC Transfer Completion Interrupt Shadow Region 2<br>EDMA_TPCC_INT3<br>EDMA_TPCC Transfer Completion Interrupt Shadow Region 3<br>EDMA_TPCC_INT4<br>EDMA_TPCC Transfer Completion Interrupt Shadow Region 4<br>EDMA_TPCC_INT5<br>EDMA_TPCC Transfer Completion Interrupt Shadow Region 5<br>EDMA_TPCC_INT6<br>EDMA_TPCC Transfer Completion Interrupt Shadow Region 6<br>EDMA_TPCC_INT7<br>EDMA_TPCC Transfer Completion Interrupt Shadow Region 7||



**Table 11-15. EDMA Error Interrupts** 

|**Name**|**Description**|
|---|---|
|EDMA_TPCC_ERRINT<br>EDMA_TPCC Error Interrupt<br>EDMA_TPCC_MPINT<br>EDMA_TPCC Memory Protection Interrupt<br>EDMA_TC0_ERRINT<br>TC0 Error Interrupt<br>EDMA_TC1_ERRINT<br>TC1 Error Interrupt||



## _**11.2.3.9.1 Transfer Completion Interrupts**_ 

The EDMA_TPCC is responsible for generating transfer completion interrupts to the CPU(s) (and other EDMA controllers). The EDMA generates a single completion interrupt per shadow region, as well as one for the global region on behalf of all 64 channels. The various control registers and bit fields facilitate EDMA interrupt generation. 

The software architecture must either use the global interrupt or the shadow interrupts, but not both. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1068 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

The transfer completion code EDMA_TPCC_OPT_n[17:12] TCC value is directly mapped to the bits of the interrupt pending register EDMA_TPCC_IPR / EDMA_TPCC_IPRH. 

For example, if EDMA_TPCC_OPT_n[17:12] TCC = 10 0001b, EDMA_TPCC_IPRH[1] is set after transfer completion, and results in interrupt generation to the CPU(s) if the completion interrupt is enabled for the CPU. See Section 11.2.3.9.1.1 _Enabling Transfer Completion Interrupts_ for details about enabling EDMA transfer completion interrupts. 

When a completion code is returned (as a result of early or normal completions), the corresponding bit in EDMA_TPCC_IPR / EDMA_TPCC_IPRH registers is set if transfer completion interrupt (final/intermediate) is enabled in the channel options parameter (OPT) for a PaRAM set associated with the transfer. 

**Table 11-16. Transfer Complete Code (TCC) to EDMA_TPCC Interrupt Mapping** 

|**TCC values in**<br>**EDMA_TPCC_OPT_n[17:12]**<br>**TCC**<br>**(EDMA_TPCC_OPT_n[20]**<br>**TCINTEN /**<br>**EDMA_TPCC_OPT_n[21]**<br>**ITCINTEN = 1)**|**EDMA_TPCC_IPR Bit Set**|**TCC values in**<br>**EDMA_TPCC_OPT_n[17:12]**<br>**TCC**<br>**(EDMA_TPCC_OPT_n[20]**<br>**TCINTEN /**<br>**EDMA_TPCC_OPT_n[21]**<br>**ITCINTEN = 1)**|**EDMA_TPCC_IPRH Bit Set**(1)|
|---|---|---|---|
|0<br>EDMA_TPCC_IPR[0]<br>1<br>EDMA_TPCC_IPR[1]<br>2h<br>EDMA_TPCC_IPR[2]<br>3h<br>EDMA_TPCC_IPR[3]<br>4h<br>EDMA_TPCC_IPR[4]<br>...<br>...<br>1Eh<br>EDMA_TPCC_IPR[30]<br>1Fh<br>EDMA_TPCC_IPR[31]||20h<br>EDMA_TPCC_IPR[32] /<br>EDMA_TPCC_IPRH[0]<br>21h<br>EDMA_TPCC_IPR[33] /<br>EDMA_TPCC_IPRH[1]<br>22h<br>EDMA_TPCC_IPR[34] /<br>EDMA_TPCC_IPRH[2]<br>23h<br>EDMA_TPCC_IPR[35] /<br>EDMA_TPCC_IPRH[3]<br>24h<br>EDMA_TPCC_IPR[36] /<br>EDMA_TPCC_IPRH[4]<br>...<br>...<br>3Eh<br>EDMA_TPCC_IPR[62] /<br>EDMA_TPCC_IPRH[30]<br>3Fh<br>EDMA_TPCC_IPR[63] /<br>EDMA_TPCC_IPRH[31]||



(1) Bit fields EDMA_TPCC_IPR [32-63] correspond to bits 0 to 31 in EDMA_TPCC_IPRH, respectively. 

The transfer completion code (TCC) can program to any value for a DMA/QDMA channel. A direct relation between the channel number and the transfer completion code value does not need to exist. This allows multiple channels having the same transfer completion code value to cause a CPU to execute the same interrupt service routine (ISR) for different channels. 

If the channel is used in the context of a shadow region and it intends for the shadow region interrupt to be asserted, then ensure that the bit corresponding to the TCC code is enabled in EDMA_TPCC_IER / EDMA_TPCC_IERH and in the corresponding shadow region's DMA region access registers (EDMA_TPCC_DRAEM_k / EDMA_TPCC_DRAEHM_k). 

Interrupt generation can be enabled at either final transfer completion or intermediate transfer completion, or both. Consider channel _m_ as an example. 

- If the final transfer interrupt (EDMA_TPCC_OPT_n[20] TCINTEN = 1) is enabled, the interrupt occurs after the last transfer request of channel _m_ is either submitted or completed (depending on early or normal completion). 

- If the intermediate transfer interrupt (EDMA_TPCC_OPT_n[21] ITCINTEN = 1) is enabled, the interrupt occurs after every transfer request, except the last TR of channel _m_ is either submitted or completed (depending on early or normal completion). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1069 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

- If both final and intermediate transfer completion interrupts (EDMA_TPCC_OPT_n[20] TCINTEN = 1, and EDMA_TPCC_OPT_n[21] ITCINTEN = 1) are enabled, then the interrupt occurs after every transfer request is submitted or completed (depending on early or normal completion). 

Table 11-17 shows the number of interrupts that occur in different synchronized scenarios. Consider channel 31, programmed with ABCNT_n[15:0] ACNT = 3, EDMA_TPCC_ABCNT_n[31:16] BCNT = 4, EDMA_TPCC_CCNT_n[15:0]CCNT = 5, and EDMA_TPCC_OPT_n[17:12] TCC = 30. 

**Table 11-17. Number of Interrupts** 

|**Options**|**A-Synchronized**|**AB-Synchronized**|
|---|---|---|
|EDMA_TPCC_OPT_n[20] TCINTEN = 1,<br>EDMA_TPCC_OPT_n[21] ITCINTEN = 0<br>1 (Last TR)<br>1 (Last TR)<br>EDMA_TPCC_OPT_n[20] TCINTEN = 0,<br>EDMA_TPCC_OPT_n[21] ITCINTEN = 1<br>19 (All but the last TR)<br>4 (All but the last TR)<br>EDMA_TPCC_OPT_n[20] TCINTEN = 1,<br>EDMA_TPCC_OPT_n[21] ITCINTEN = 1<br>20 (All TRs)<br>5 (All TRs)|||



## _**11.2.3.9.1.1 Enabling Transfer Completion Interrupts**_ 

For the EDMA channel controller to assert a transfer completion to the external environment, the interrupts must be enabled in the EDMA_TPCC. This is in addition to setting up the EDMA_TPCC_OPT_n[20] TCINTEN and EDMA_TPCC_OPT_n[21] ITCINTEN bits of the associated PaRAM set. 

The EDMA channel controller has interrupt enable registers EDMA_TPCC_IER / EDMA_TPCC_IERH and each bit location in EDMA_TPCC_IER / EDMA_TPCC_IERH serves as a primary enable for the corresponding interrupt pending registers EDMA_TPCC_IPR / EDMA_TPCC_IPRH. 

All of the interrupt registers (EDMA_TPCC_IER, EDMA_TPCC_IESR, EDMA_TPCC_IECR, and EDMA_TPCC_IPR) are either manipulated from the global DMA channel region, or by the DMA channel shadow regions. The shadow regions provide a view to the same set of physical registers that are in the global region. 

The EDMA channel controller has a hierarchical completion interrupt scheme that uses a single set of interrupt pending registers EDMA_TPCC_IPR / EDMA_TPCC_IPRH and single set of interrupt enable registers EDMA_TPCC_IER / EDMA_TPCC_IERH. The programmable DMA region access enable registers EDMA_TPCC_DRAEM_k / EDMA_TPCC_DRAEHM_k provides a second level of interrupt masking. The global region interrupt output is gated based on the enable mask that is provided by EDMA_TPCC_IER / EDMA_TPCC_IERH, see Figure 11-15 

The region interrupt outputs are gated by EDMA_TPCC_IER and the specific EDMA_TPCC_DRAEM_k / EDMA_TPCC_DRAEHM_k associated with the region. 

Figure 11-15 shows the Interrupt diagram of the EDMA controller. 

1070 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**==> picture [352 x 309] intentionally omitted <==**

**----- Start of picture text -----**<br>
Interrupt pending<br>register (IPR)<br>X 1 0<br>Interrupt<br>enable DMA region DMA region<br>register access enable 1 access enable 7<br>(IER) (DRAEM_1) (DRAEM_7)<br>X 1 0 X 1 0 X 1 0<br>IEVAL0.EVAL IEVAL1.EVAL IEVAL7.EVAL<br>Eval Eval Eval<br>pulse pulse pulse<br>EDMA_TPCC_INT0 EDMA_TPCC_INT1 EDMA_TPCC_INT7<br>edma-016<br>**----- End of picture text -----**<br>


**Figure 11-15. Interrupt Diagram** 

The EDMA_TPCC generates the transfer completion interrupts that are associated with each shadow region, the following conditions must be true: 

- EDMA_TPCC_INT0: (EDMA_TPCC_IPR[0] E0 & EDMA_TPCC_IER[0] E0 & 

   - EDMA_TPCC_DRAEM_k.DRAEM_0[0] E0) | (EDMA_TPCC_IPR[1] E1 & EDMA_TPCC_IER[1] E1 & EDMA_TPCC_DRAEM_k.DRAEM_0[1] E1) | …|(EDMA_TPCC_IPRH[31] E63 & EDMA_TPCC_IERH[31] E63 & EDMA_TPCC_DRAEHM_k.DRAEHM_0[31] E63) 

- EDMA_TPCC_INT1: (EDMA_TPCC_IPR[0] E0 & EDMA_TPCC_IER[0] E0 & EDMA_TPCC_DRAEM_k.DRAEM_1[0] E0) | (EDMA_TPCC_IPR[1] E1 & EDMA_TPCC_IER[1] E1 & EDMA_TPCC_DRAEM_k.DRAEM_1[1] E1) | …| (EDMA_TPCC_IPRH[31] E63 & EDMA_TPCC_IERH[31] E63 & EDMA_TPCC_DRAEHM_k.DRAEHM_1[31] E63) 

- EDMA_TPCC_INT2: (EDMA_TPCC_IPR[0] E0 & EDMA_TPCC_IER[0] E0 & EDMA_TPCC_DRAEM_k.DRAEM_2[0] E0) | (EDMA_TPCC_IPR[1] E1 & EDMA_TPCC_IER[1] E1 & EDMA_TPCC_DRAEM_k.DRAEM_2[1] E1) | …|(EDMA_TPCC_IPRH[31] E63 & EDMA_TPCC_IERH[31] E63 & EDMA_TPCC_DRAEHM_k.DRAEHM_2[31] E63).... 

- Up to EDMA_TPCC_INT7: (EDMA_TPCC_IPR[0] E0 & EDMA_TPCC_IER[0] E0 & EDMA_TPCC_DRAEM_k.DRAEM_7[0] E0) | (EDMA_TPCC_IPR[1] E1 & EDMA_TPCC_IER[1] E1 & EDMA_TPCC_DRAEM_k.DRAEM_7[1] E1) | …|(EDMA_TPCC_IPRH[31] E63 & EDMA_TPCC_IERH[31] E63 & EDMA_TPCC_DRAEHM_k.DRAEHM_7[31] E63) 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1071 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## **Note** 

The EDMA_TPCC_DRAEM_k / EDMA_TPCC_DRAEHM_k for all regions are expected to be set up at system initialization and to remain static for an extended period of time. The interrupt enable registers are used for dynamic enable/disable of individual interrupts. 

Because there is no relation between the EDMA_TPCC_OPT_n[17:12] TCC value and the DMA/ QDMA channel, it is possible, the DMA channel 0 to have the EDMA_TPCC_OPT_n[17:12] TCC = 63 in its associated PaRAM set. This mean that if a transfer completion interrupt is enabled (EDMA_TPCC_OPT_n[20] TCINTEN or EDMA_TPCC_OPT_n[21] ITCINTEN is set), then based on the TCC value, EDMA_TPCC_IPRH[31] E63 is set up on completion. For proper channel operations and interrupt generation using the shadow region map - program the EDMA_TPCC_DRAEM_k / EDMA_TPCC_DRAEHM_k that is associated with the shadow region to have read/write access to both bit 0 (corresponding to channel 0) and bit 63 (corresponding to EDMA_TPCC_IPRH bit that is set upon completion). 

## _**11.2.3.9.1.2 Clearing Transfer Completion Interrupts**_ 

Transfer completion interrupts that are latched to the interrupt pending registers ( EDMA_TPCC_IPR / EDMA_TPCC_IPRH ) are cleared by writing a 1 to the corresponding bit in the interrupt pending clear register ( EDMA_TPCC_ICR / EDMA_TPCC_ICRH ). For example, a write of 1 to EDMA_TPCC_ICR[0] E0 clears a pending interrupt in EDMA_TPCC_IPR[0] E0. 

If an incoming transfer completion code TCC (EDMA_TPCC_OPT_n[17:12] TCC) gets latched to a bit in EDMA_TPCC_IPR / EDMA_TPCC_IPRH, then additional bits that get set due to a subsequent transfer completion does not result in asserting the EDMA_TPCC completion interrupt. In order for the completion interrupt to be pulsed, the required transition is from a state where no enabled interrupts are set to a state where at least one enabled interrupt is set. 

## _**11.2.3.9.2 EDMA Interrupt Servicing**_ 

Upon completion of a transfer (early or normal completion), the EDMA channel controller sets the appropriate bit in the interrupt pending registers ( EDMA_TPCC_IPR / EDMA_TPCC_IPRH ), as the transfer completion codes specify. If the completion interrupts are appropriately enabled, then the CPU enters the interrupt service routine (ISR) when the completion interrupt is asserted. 

After servicing the interrupt, the ISR should clear the corresponding bit in EDMA_TPCC_IPR/ EDMA_TPCC_IPRH, thereby enabling recognition of future interrupts. The EDMA_TPCC only asserts additional completion interrupts when all EDMA_TPCC_IPR / EDMA_TPCC_IPRH bits clear. 

When one interrupt is serviced many other transfer completions may result in additional bits being set in EDMA_TPCC_IPR / EDMA_TPCC_IPRH, thereby resulting in additional interrupts. Each of the bits in EDMA_TPCC_IPR / EDMA_TPCC_IPRH may need different types of service therefore, the ISR must check all pending interrupts and continue until all of the posted interrupts are serviced appropriately. 

Examples of pseudo code for a CPU interrupt service routine for an EDMA_TPCC completion interrupt are shown in Example 11-2 and Example 11-3. 

The ISR routine in Example 11-2 is more exhaustive and incurs a higher latency. 

## _**Example 11-2. Interrupt Servicing**_ 

The pseudo code: 

1. Reads the interrupt pending register EDMA_TPCC_IPR / EDMA_TPCC_IPRH. 

2. Performs the operations needed. 

3. Writes to the interrupt pending clear register EDMA_TPCC_ICR / EDMA_TPCC_ICRH to clear the corresponding EDMA_TPCC_IPR / EDMA_TPCC_IPRH bit(s). 

4. Reads EDMA_TPCC_IPR / EDMA_TPCC_IPRH again: 

1072 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

- a. If EDMA_TPCC_IPR / EDMA_TPCC_IPRH is not equal to 0, repeat from step 2 (implies occurrence of new event between step 2 to step 4). 

- b. If EDMA_TPCC_IPR / EDMA_TPCC_IPRH is equal to 0, assure that all of the enabled interrupts are inactive. 

## **Note** 

An event may occur during step 4 while the EDMA_TPCC_IPR / EDMA_TPCC_IPRH bits are read as 0 and the application is still in the interrupt service routine. If this happens, a new interrupt is recorded in the device interrupt controller and a new interrupt generates as soon as the application exits in the interrupt service routine. 

## _**11.2.3.9.3**_ 

Example 11-3 is less rigorous, with less burden on the software in polling for set interrupt bits, but can occasionally cause a race condition as mentioned above. 

## _**Example 11-3. Interrupt Servicing**_ 

If any enabled and pending (possibly lower priority) interrupts are left, force the interrupt logic to reassert the interrupt pulse by setting the EDMA_TPCC_IEVAL[0] EVAL bit in the interrupt evaluation register. 

The pseudo code is as follows: 

1. Enters ISR. 

2. Reads EDMA_TPCC_IPR / EDMA_TPCC_IPRH. 

3. For the condition that is set in EDMA_TPCC_IPR / EDMA_TPCC_IPRH: 

   - a. Service interrupt as the application requires. 

   - b. Clear the bit for serviced conditions (others may still be set, and other transfers may have resulted in returning the TCC to EDMA_TPCC after step 2). 

4. Reads EDMA_TPCC_IPR / EDMA_TPCC_IPRH prior to exiting the ISR: 

   - a. If EDMA_TPCC_IPR / EDMA_TPCC_IPRH is equal to 0, then exit the ISR. 

   - b. If EDMA_TPCC_IPR / EDMA_TPCC_IPRH is not equal to 0, then set EDMA_TPCC_IEVAL so that upon exit of ISR, a new interrupt triggers if any enabled interrupts are still pending. 

## _**11.2.3.9.4 Interrupt Evaluation Operations**_ 

The EDMA_TPCC has interrupt evaluate registers EDMA_TPCC_IEVAL that exist in the global region and in each shadow region. The registers in the shadow region are the only registers in the DMA channel shadow region memory map that are not affected by the settings for the DMA region access enable registers EDMA_TPCC_DRAEM_k / EDMA_TPCC_DRAEHM_k. Writing a 1 to the EDMA_TPCC_IEVAL[0] EVAL bit in the registers that are associated with a particular shadow region results in pulsing the associated region interrupt (global or shadow), if any enabled interrupt (via EDMA_TPCC_IER / EDMA_TPCC_IERH) is still pending EDMA_TPCC_IPR / EDMA_TPCC_IPRH. This register assures that the CPU does not miss the interrupts (or the EDMA controller associated with the shadow region) if the software architecture chooses not to use all interrupts. Refer to Example 11-3 about the use of EDMA_TPCC_IEVAL in the EDMA interrupt service routine (ISR). 

Similarly an error evaluation register EDMA_TPCC_EEVAL exists in the global region. Writing a 1 to the EDMA_TPCC_EEVAL[0] EVAL bit causes the pulsing of the error interrupt if any pending errors are in EDMA_TPCC_EMR / EDMA_TPCC_EMRH, EDMA_TPCC_QEMR, or EDMA_TPCC_CCERR. See Section 11.2.3.9.5 _Error Interrupts_ for additional information regarding error interrupts. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1073 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## **Note** 

While using EDMA_TPCC_IEVAL for shadow region completion interrupts, check that the EDMA_TPCC_IEVAL operated upon is from that particular shadow region memory map. 

1074 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## _**11.2.3.9.5 Error Interrupts**_ 

The EDMA_TPCC error registers provide the capability to differentiate error conditions (event missed, threshold exceed, etc.). Additionally, setting the error bits in these registers results in asserting the EDMA_TPCC error interrupt. If the EDMA_TPCC error interrupt is enabled in the device interrupt controller(s), then it allows the CPU(s) to handle the error conditions. 

The EDMA_TPCC has a single error interrupt (EDMA_TPCC_ERRINT) that is asserted for all EDMA_TPCC error conditions. There are four conditions that cause the error interrupt: 

- DMA missed events: for all 64 DMA channels. DMA missed events are latched in the event missed registers EDMA_TPCC_EMR / EDMA_TPCC_EMRH. 

- QDMA missed events: for all 8 QDMA channels. QDMA missed events are latched in the QDMA event missed register EDMA_TPCC_QEMR. 

- Threshold exceed: for all event queues. These are latched in EDMA_TPCC error register EDMA_TPCC_CCERR. 

- TCC error: for outstanding transfer requests that are expected to return completion code EDMA_TPCC_OPT_n[22] TCCHEN or EDMA_TPCC_OPT_n[23] TCINTEN bit is set to 1, exceeding the maximum limit of 63. This is also latched in the EDMA_TPCC error register EDMA_TPCC_CCERR. 

Figure 11-16 illustrates the EDMA_TPCC error interrupt generation operation. 

If any of the bits are set in the error registers due to any error condition, the EDMA_TPCC_ERRINT is always asserted, as there are no enables for masking these error events. Similar to transfer completion interrupts (EDMA_TPCC_INT), the error interrupt also only pulses when the error interrupt condition transitions from no errors being set to at least one error being set. If additional error events are latched prior to the original error bits clearing, the EDMA_TPCC does not generate additional interrupt. 

To reduce the burden on the software, there is an error evaluate register EDMA_TPCC_EEVAL that allows re-evaluation of pending set error events/bits, similar to the interrupt evaluate register EDMA_TPCC_IEVAL. Unlike the EDMA_TPCC_IEVAL functionality, the EDMA_TPCC_EEVAL register must be written with ‘1’ after any error interrupts are serviced (even when all pending errors are cleared) in order for subsequent errors to trigger a new interrupt. 

## **Note** 

It is good practice to enable the error interrupt in the device interrupt controller and to associate an interrupt service routine with it to address the various error conditions appropriately. Doing so puts less burden on the software (polling for error status), it provides a good debug mechanism for unexpected error conditions. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1075 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**==> picture [404 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
EMR / EMRH QMER CCERR<br>63 1 0 7 1 0 16 3 2 1 0<br>EEVAL[0] EVAL<br>EVAL<br>EDMA_TPCC_ERRINT<br>edma-017<br>**----- End of picture text -----**<br>


**Figure 11-16. Error Interrupt Operation** 

1076 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## **11.2.3.10 Memory Protection** 

The EDMA channel controller supports two kinds of memory protection: active and proxy. 

## _**11.2.3.10.1 Active Memory Protection**_ 

Active memory protection is a feature that allows or prevents read and write accesses to the EDMA_TPCC registers. Active memory protection is achieved by a set of memory protection permissions attribute EDMA_TPCC_MPPAN_k registers. 

The EDMA_TPCC register map is divided into three categories: 

- a global region. 

- a global channel region. 

- eight shadow regions. 

Each shadow region consists of the respective shadow region registers and the associated PaRAM. For more detailed information regarding the contents of a shadow region, refer to the associated Register Addendum. 

Each of the eight shadow regions has an associated EDMA_TPCC_MPPAN_k registers that defines the specific requestor(s) and types of requests that are allowed to the regions resources. 

The global channel region is also protected with a memory-mapped register EDMA_TPCC_MPPAG. The EDMA_TPCC_MPPAG applies to the global region and to the global channel region, except the other EDMA_TPCC_MPPAN_k registers themselves. 

Table 11-18 shows the accesses that are allowed or not allowed to the EDMA_TPCC_MPPAG and EDMA_TPCC_MPPAN_k. The active memory protection uses the EDMA_TPCC_OPT_n[31] PRIV and EDMA_TPCC_OPT_n[27:24] PRIVID attributes of the EDMA peripheral modules. TheEDMA_TPCC_OPT_n[31] PRIV is the privilege level (i.e., user vs. supervisor). 

The EDMA_TPCC_OPT_n[27:24] PRIVID refers to a privilege ID with a number that is associated with an EDMA peripheral modules. 

**Table 11-18. Allowed Accesses** 

|**Access**|**Supervisor**|**User**|
|---|---|---|
|Read<br>Yes<br>Yes<br>Write<br>Yes<br>No|||



Table 11-19 describes the EDMA_TPCC_MPPAN_k register mapping for the shadow regions (which includes shadow region registers and PaRAM addresses). 

The region-based EDMA_TPCC_MPPAN_k registers are used to protect accesses to the DMA shadow regions and the associated region PaRAM. Because there are eight regions, there are eight EDMA_TPCC_MPPAN_k region registers (MPPA[0-7]). 

**Table 11-19. MPPA Registers to Region Assignment** 

|**Register**|**Registers**<br>**Protect**|**Address Range**|**PaRAM Protect**(1)|**Address Range**|
|---|---|---|---|---|
|EDMA_TPCC_MPPAG<br>Global Range<br>0000h-1FFCh<br>N/A<br>N/A<br>EDMA_TPCC_MPPAN_k. MPPAN_0 DMA Shadow 0<br>2000h-21FCh<br>1st octant<br>4000h-47FCh<br>MPPAN_1<br>DMA Shadow 1<br>2200h-23FCh<br>2nd octant<br>4800h-4FFCh<br>MPPAN_2<br>DMA Shadow 2<br>2400h-25FCh<br>3rd octant<br>5000h-57FCh<br>MPPAN_3<br>DMA Shadow 3<br>2600h-27FCh<br>4th octant<br>5800h-5FFCh<br>MPPAN_4<br>DMA Shadow 4<br>2800h-29FCh<br>5th octant<br>6000h-67FCh<br>MPPAN_5<br>DMA Shadow 5<br>2A00h-2BFCh<br>6th octant<br>6800h-6FFCh<br>MPPAN_6<br>DMA Shadow 6<br>2C00h-2DFCh<br>7th octant<br>7000h-77FCh|||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1077 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**Table 11-19. MPPA Registers to Region Assignment (continued)** 

|**Register**|**Registers**<br>**Protect**|**Address Range**|**PaRAM Protect**(1)|**Address Range**|
|---|---|---|---|---|
|MPPAN_7<br>DMA Shadow 7<br>2E00h-2FFCh<br>8th octant<br>7800h-7FFCh|||||



(1) The PARAM region is divided into 8 regions referred to as an octant. 

## **Example** _Access denied._ 

Write access to shadow region 7's event enable set register EDMA_TPCC_EESR: 

1. The original value of the event enable register EDMA_TPCC_EER at address offset 0x1020 is 0x0. 

2. The EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[7] NS is set to prevent user level accesses (EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[1] UW = 0, EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[2] UR = 0), but it allows supervisor level accesses (EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[4] SW = 1, EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[5] SR = 1) with a privilege ID of 0. (EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[10] AID0 = 1). 

3. EDMA peripheral modules with a privilege ID of 0 attempts to perform a user-level write of a value of 0xFF00FF00 to shadow region 7's event enable set register EDMA_TPCC_EESR at address offset 0x2E30. 

## **Note** 

The EDMA_TPCC_EER is a read-only register and the only way that write to it is by writing to the EDMA_TPCC_EESR. There is only one physical register for EDMA_TPCC_EER, EDMA_TPCC_EESR, etc. and that the shadow regions only provide to the same physical set. 

4. Since the EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[1] UW = 0, though the privilege ID of the write access is set to 0, the access is not allowed and the EDMA_TPCC_EER is not written too. 

## **Example** _Access Allowed_ 

Write access to shadow region 7's event enable set register EDMA_TPCC_EESR: 

1. The original value of the event enable register EDMA_TPCC_EER at address offset 0x1020 is 0x0. 

2. The EDMA_TPCC_MPPAN_k.EDMA_TPCC_MPPAN_7 is set to allow user-level accesses (EDMA_TPCC_MPPAN_k.EDMA_TPCC_MPPAN_7[1] UW = 1, EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[2] UR = 1) and supervisor-level accesses (EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[4] SW = 1, EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[5] SR = 1) with a privilege ID of 0. (EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[10] AID0 = 1). 

3. EDMA peripheral modules with a privilege ID of 0, attempts to perform a user-level write of a value of 0xABCD0123 to shadow region 7's event enable set register EDMA_TPCC_EESR at address offset 0x2E30. 

## **Note** 

The EDMA_TPCC_EER is a read-only register and the only way that write to it is by writing to the EDMA_TPCC_EESR. There is only one physical register for EDMA_TPCC_EER, EDMA_TPCC_EESR, etc. and that the shadow regions only provide to the same physical set. 

4. Since the EDMA_TPCC_MPPAN_k. EDMA_TPCC_MPPAN_7[1] UW = 1 and EDMA_TPCC_MPPAN_k. MPPAN_7[10] AID0 = 1, the user-level write access is allowed. 

5. The accesse to shadow region registers are masked by their respective EDMA_TPCC_DRAEM_k register. In this example, the EDMA_TPCC_DRAEM_k. EDMA_TPCC_DRAEM_7 is set of 0x9FF00FC2. 

6. The value finally written to EDMA_TPCC_EER is 0x8BC00102. 

## _**11.2.3.10.2 Proxy Memory Protection**_ 

Proxy memory protection allows an EDMA transfer programmed by a given peripheral module connected to EDMA, to have its permissions travel with the transfer through the EDMA_TPTC. The permissions travel along with the read transactions to the source and the write transactions to the destination endpoints. The 

1078 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

EDMA_TPCC_OPT_n[31] PRIV bit and EDMA_TPCC_OPT_n[27:24] PRIVID bit is set with the peripheral module's PRIV value and PRIVID values, respectively, when any part of the PaRAM set is written. 

The EDMA_TPCC_OPT_n[31] PRIV is the privilege level (i.e., user vs. supervisor). The EDMA_TPCC_OPT_n[27:24] PRIVID refers to a privilege ID with a number that is associated with an peripheral module connected to EDMA. 

These options are part of the TR that are submitted to the transfer controller. The transfer controller uses the above values on their respective read and write command bus so that the target endpoints can perform memory protection checks based on these values. 

Consider a parameter set that is programmed by a CPU in user privilege level for a simple transfer with the source buffer on an L2 page and the destination buffer on an L1D page. The EDMA_TPCC_OPT_n[31] PRIV is 0 for user-level and the CPU has a EDMA_TPCC_OPT_n[27:24] PRIVID to 0. 

The PaRAM set is shown in Figure 11-17. 

## **Figure 11-17. PaRAM Set Content for Proxy Memory Protection Example** 

## _(a) EDMA Parameters_ 

|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|
|---|---|---|---|---|---|---|
||0010 0007h|||Channel Options Parameter (OPT)|||
||009F 0000h|||Channel Source Address (SRC)|||
||0001h|0004h||Count for 2nd Dimension (BCNT)|Count for 1st Dimension (ACNT)||
||00F0 7800h|||Channel Destination Address (DST)|||
||0001h|0001h||Destination BCNT Index (DBIDX)|Source BCNT Index (SBIDX)||
||0000h|FFFFh||BCNT Reload (BCNTRLD)|Link Address (LINK)||
||0001h|1000h||Destination CCNT Index (DCIDX)|Source CCNT Index (SCIDX)||
||0000h|0001h||Reserved|Count for 3rd Dimension (CCNT)||



(b) Channel Options Parameter (OPT_n) Content 

**==> picture [450 x 125] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 30 29 28 27 24 23 22 21 20 19 18 17 16<br>0 0 00 0000 0 0 0 1 00 00<br>PRIV Rsvd Rsvd PRIVID ITCCHEN TCCHEN ITCINTEN TCINTEN Reserved TCC<br>15 12 11 10 8 7 4 3 2 1 0<br>0000 0 000 0000 0 1 1 1<br>TCC TCCMOD FWID Reserved STATIC SYNCDIM DAM SAM<br>edma-018<br>**----- End of picture text -----**<br>


**Figure 11-18. Channel Options Parameter (OPT) Example** 

The EDMA_TPCC_OPT_n[31] PRIV and EDMA_TPCC_OPT_n[27:24] PRIVID information travels along with the read and write requests that are issued to the source and destination memories. 

For example, if the access attributes that are associated with the L2 page with the source buffer only allow supervisor read, write accesses (EDMA_TPCC_MPPAN_k[4] SW and EDMA_TPCC_MPPAN_k[5] SR), the user-level read request above is refused. Similarly, if the access attributes that are associated with the L1D page with the destination buffer only allow supervisor read and write accesses (EDMA_TPCC_MPPAN_k[4] SW, EDMA_TPCC_MPPAN_k[5] SR), the user-level write request above is refused. For the transfer to succeed, the source and destination pages must have user-read and user-write permissions, respectively, along with allowing accesses from a PRIVID = 0. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1079 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

Because the privilege level and privilege identification travel with the read and write requests, EDMA acts as a proxy. 

Figure 11-19 illustrates the propagation of EDMA_TPCC_OPT_n[31] PRIV and EDMA_TPCC_OPT_n[27:24] PRIVID at the boundaries of all the interacting entities (CPU, EDMA_TPCC, EDMA_TPTCs, and target memories). 

**==> picture [448 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>
Memory<br>Protection L2 Page<br>Attribute 9F 0000h<br>Read req<br>EDMA_TPCC<br>PRIVID=0,<br>PaRAM PRIV=0 AID0=1 Src Buffer<br>UR=1<br>EDMA_TPTC0<br>PRIVID=0<br>CPU User write PaRAMentry 5 TR Read Access allowed<br>from user PRIVID=0,<br>PRIV=0 Submission<br>Privilege level Write Access L1D Page<br>allowed F0 7800h<br>PRIVID = 0, AID0=1 Dst  Buffer<br>PRIV = 0 UW=1<br>Memory<br>Protection<br>Attribute<br>edma-019<br>**----- End of picture text -----**<br>


**Figure 11-19. Proxy Memory Protection Example** 

## **11.2.3.11 Event Queue(s)** 

Event queues are a part of the EDMA channel controller. Event queues form the interface between the event detection logic in the EDMA_TPCC and the transfer request (TR) submission logic of the EDMA_TPCC. Each queue is 16 entries deep. Each event queue can queue a maximum of 16 events. If there are more than 16 events, then the events that cannot find a place in the event queue remain set in the associated event register and the CPU does not stall. 

There are two event queues for the device: Queue0, Queue1. Events in Queue0 result in submission of its associated transfer requests (TRs) to TC0. The transfer requests that are associated with events in Queue1 are submitted to TC1. 

An event that wins prioritization against other DMA and/or QDMA pending events is placed at the tail of the appropriate event queue. Each event queue is serviced in FIFO order. Once the event reaches the head of its queue and the corresponding transfer controller is ready to receive another TR, the event is de-queued and the PaRAM set corresponding to the de-queued event is processed and submitted as a transfer request packet (TRP) to the associated EDMA transfer controller. 

Queue0 has highest priority and Queue1 has the lowest priority, if Queue0 and Queue1 both have at least one event entry and if both TC0 and TC1 can accept transfer requests, then the event in Queue0 is de-queued first and its associated PaRAM set is processed and submitted as a transfer request (TR) to TC0. 

Refer to _Performance Considerations_ for system-level performance considerations. All of the event entries in all of the event queues are software readable (not writeable) by accessing the event entry registers EDMA_TPCC_Q0E_p and EDMA_TPCC_Q1E_p. Each event entry register characterizes the queued event in terms of the type of event (manual, event, chained or auto-triggered) and the event number. Refer to the associated Register Addendum for EDMA_TPCC_Q0E_p / EDMA_TPCC_Q1E_p descriptions of the bit fields. 

1080 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## _**11.2.3.11.1 DMA/QDMA Channel to Event Queue Mapping**_ 

Each of the 64 DMA channels and eight QDMA channels are programmed independently to map to a specific queue, using the DMA queue number register EDMA_TPCC_DMAQNUMN_k and the QDMA queue number register EDMA_TPCC_QDMAQNUM. The mapping of DMA/QDMA channels is critical to achieving the desired performance level for the EDMA and most importantly, in meeting real-time deadlines. Refer to _System-level Performance Considerations_ . 

## **Note** 

If an event is ready to be queued and both the event queue and the EDMA transfer controller that is associated to the event queue are empty, then the event bypasses the event queue, and moves the PaRAM processing logic, and eventually to the transfer request submission logic for submission to the EDMA_TPTC. In this case, the event is not logged in the event queue status registers. 

## _**11.2.3.11.2 Queue RAM Debug Visibility**_ 

There are two event queues and each queue has 16 entries. These 16 entries are managed in a circular FIFO. There is a queue status register EDMA_TPCC_QSTATN_i associated with each queue. These along with all of the 16 entries per queue can be read via registers EDMA_TPCC_QSTATN_i and Q0E_p / Q1E_p, respectively. 

These registers provide user visibility. 

The event queue entry register (Q _x_ E _y_ Q0E_p / Q1E_p) uniquely identifies the specific event type (eventtriggered, manually-triggered, chain-triggered, and QDMA events) along with the event number (for all DMA/ QDMA event channels) that are in the queue or have been de-queued (passed through the queue). 

Each of the 16 entries in the event queue are read using the EDMA_TPCC memory-mapped register. To see the history of the last 16 TRs that have been processed by the EDMA on a given queue, read the event queue registers. This provides user/software visibility and is helpful for debugging real-time issues (typically post-mortem), involving multiple events and event sources. 

The queue status register (QSTAT _n_ EDMA_TPCC_QSTATN_i) includes fields for the start pointer EDMA_TPCC_QSTATN_i[3:0] STRTPTR which provides the offset to the head entry of an event. It also includes a field called EDMA_TPCC_QSTATN_i[12:8] NUMVAL that provides the total number of valid entries residing in the event queue at a given instance of time. The EDMA_TPCC_QSTATN_i[3:0] STRTPTR is used to index appropriately into the 16 event entries. EDMA_TPCC_QSTATN_i[12:8] NUMVAL number of entries starting from STRTPTR are indicative of events still queued in the respective queue. The remaining entry must be read to determine what's already de-queued and submitted to the associated transfer controller. 

## _**11.2.3.11.3 Queue Resource Tracking**_ 

The EDMA_TPCC event queue includes watermarking/threshold logic that allows to keep track of maximum usage of all event queues. This is useful for debugging real-time deadline violations that may result from head-of-line blocking on a given EDMA event queue. 

The maximum number of events are programed that the queue up in an event queue by programming the threshold value (between 0 to 15) in the queue watermark threshold A register EDMA_TPCC_QWMTHRA. The maximum queue usage is recorded actively in the watermark EDMA_TPCC_QSTATN_i[20:16] WM field of the queue status register, that keeps getting updated based on a comparison of number of valid entries, which is also visible in the EDMA_TPCC_QSTATN_i[12:8] NUMVAL bit and the maximum number of entries. 

If the queue usage is exceeded, this status is visible in the EDMA_TPCC registers: the QTHRXCD _n_ bits in the channel controller error register EDMA_TPCC_CCERR[7:0] and the EDMA_TPCC_QSTATN_i[24] THRXCD bit, where _n_ stands for the event queue number. Any bits that are set in EDMA_TPCC_CCERR also generate an EDMA_TPCC error interrupt. 

## _**11.2.3.11.4 Performance Considerations**_ 

The device system bus infrastructure arbitrates bus requests from all of the controllers (TCs, CPU(S), and other bus controllers) to the shared target resources (peripherals and memories). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1081 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

Therefore, the priority of unloading queues has a secondary affect compared to the priority of the transfers as they are executed by the EDMA_TPTC. 

## **11.2.3.12 EDMA Transfer Controller (EDMA_TPTC)** 

The EDMA channel controller is the user-interface of the EDMA and the EDMA transfer controller (EDMA_TPTC) is the data movement engine of the EDMA controller. The EDMA_TPCC submits transfer requests (TR) to the EDMA_TPTC and the EDMA_TPTC performs the data transfers dictated by the TR, so the EDMA_TPTC is a target to the EDMA_TPCC. 

## _**11.2.3.12.1 Architecture Details**_ 

## _**11.2.3.12.1.1 Command Fragmentation**_ 

The TC read and write controllers in conjunction with the source and destination register sets are responsible for issuing optimally-sized reads and writes to the target endpoints. An optimally-sized command is defined by the transfer controller default burst size (DBS), which is defined in the _TPTC DBS Configuration registers_ . 

The EDMA_TPTC attempts to issue the largest possible command size as limited by the DBS value or the EDMA_TPCC_ABCNT_n[15:0] ACNT and EDMA_TPCC_ABCNT_n[31:16] BCNT value of the TR. EDMA_TPTC obeys the following rules: 

- The read/write controllers always issue commands less than or equal to the DBS value. 

- The first command of a 1D transfer command always aligns the address of subsequent commands to the DBS value. 

Table 11-20 lists the TR segmentation rules that are followed by the EDMA_TPTC. In summary, if the EDMA_TPCC_ABCNT_n[15:0] ACNT value is larger than the DBS value, then the EDMA_TPTC breaks the EDMA_TPCC_ABCNT_n[15:0] ACNT array into DBS-sized commands to the source/destination addresses. Each EDMA_TPCC_ABCNT_n[31:16] BCNT number of arrays are then serviced in succession. 

For BCNT arrays of ACNT bytes (that is, a 2D transfer), if the EDMA_TPCC_ABCNT_n[15:0] ACNT value is less than or equal to the DBS value, then the TR may be optimized into a 1D-transfer in order to maximize efficiency. The optimization takes place if the EDMA_TPTC recognizes that the 2D-transfer is organized as a single dimension (EDMA_TPCC_ABCNT_n[15:0] ACNT == EDMA_TPCC_BIDX_n) and the ACNT value is a power of 2. 

Table 11-20 lists conditions in which the optimizations are performed. 

**Table 11-20. Read/Write Command Optimization Rules** 

|**ACNT ≤ DBS**|**ACNT is power of 2**|**BIDX = ACNT**|**BCNT ≤ 1023**|**SAM/DAM =**<br>**Increment**|**Description**|
|---|---|---|---|---|---|
|Yes<br>Yes<br>Yes<br>Yes<br>Yes<br>Optimized<br>No<br>x<br>x<br>x<br>x<br>Not Optimized<br>x<br>No<br>x<br>x<br>x<br>Not Optimized<br>x<br>x<br>No<br>x<br>x<br>Not Optimized<br>x<br>x<br>x<br>No<br>x<br>Not Optimized<br>x<br>x<br>x<br>x<br>No<br>Not Optimized||||||



## _**11.2.3.12.1.2 TR Pipelining**_ 

TR pipelining refers to the ability of the source active set to proceed ahead of the destination active set. Essentially, the reads for a given TR may already be in progress while the writes of a previous TR may not have completed. 

The number of outstanding TRs is limited by the number of destination FIFO register entries. 

TR pipelining is useful for maintaining throughput on back-to-back small TRs. It minimizes the startup overhead because reads start in the background of a previous TR writes. 

1082 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## _**Example 11-4. Command Fragmentation (DBS = 64)**_ 

The pseudo code: 

1. EDMA_TPTCn_PCNT[15:0] ACNT = 8, EDMA_TPTCn_PCNT[31:16] BCNT = 8, EDMA_TPTCn_PBIDX[15:0] SBIDX = 8, EDMA_TPTCn_PBIDX[31:16] DBIDX = 10, EDMA_TPTCn_PSRC[31:0] SADDR = 64, EDMA_TPTCn_SADST[31:0] DADDR = 191 

Read Controller: This is optimized from a 2D-transfer to a 1D-transfer such that the read side is equivalent to EDMA_TPTCn_PCNT[15:0] ACNT = 64, EDMA_TPTCn_PCNT[31:16] BCNT = 1. 

Cmd0 = 64 byte 

Write Controller: Because DBIDX != ACNT, it is not optimized. 

Cmd0 = 8 byte, Cmd1 = 8 byte, Cmd2 = 8 byte, Cmd3 = 8 byte, Cmd4 = 8 byte, Cmd5 = 8 byte, Cmd6 = 8 byte, Cmd7 = 8 byte. 

2. EDMA_TPTCn_PCNT[15:0] ACNT=128, EDMA_TPTCn_PCNT[31:16] BCNT = 1, EDMA_TPTCn_PSRC[31:0] SADDR = 63, EDMA_TPTCn_SADST[31:0] DADDR = 513 

Read Controller: Read address is not aligned. 

Cmd0 = 1 byte, (now the SADDR is aligned to 64 for the next command) 

Cmd1 = 64 bytes 

Cmd2 = 63 bytes 

Write Controller: The write address is also not aligned. 

Cmd0 = 63 bytes, (now the DADDR is aligned to 64 for the next command) 

Cmd1 = 64 bytes Cmd2 = 1 byte 

## _**11.2.3.12.1.3 Performance Tuning**_ 

By default, reads are as issued as fast as possible. In some cases, the reads issued by the EDMA_TPTC could fill the available command buffering for a target, delaying other (potentially higher priority) controllers from successfully submitting commands to that target. The rate at which read commands are issued by the EDMA_TPTC is controlled by the EDMA_TPTCn_RDRATE register. The EDMA_TPTCn_RDRATE register defines the number of cycles that the EDMA_TPTC read controller waits before issuing subsequent commands for a given TR, thus minimizing the chance of the EDMA_TPTC consuming all available target resources. The EDMA_TPTCn_RDRATE[2:0] RDRATE value must be set to a relatively small value if the transfer controller is targeted for high priority transfers and to a higher value if the transfer controller is targeted for low priority transfers. 

In contrast, the Write Interface does not have any performance turning knobs because writes always have an interval between commands as write commands are submitted along with the associated write data. 

## _**11.2.3.12.2 Memory Protection**_ 

The transfer controller plays an important role in handling proxy memory protection. There are two access properties associated with a transfer: for instance, the privilege id (system-wide identification assigned to a controller) of the controller initiating the transfer, and the privilege level (user versus supervisor) used to program the transfer. This information is maintained in the PaRAM set when it is programmed in the channel controller. When a TR is submitted to the transfer controller, this information is made available to the EDMA_TPTC and used by the EDMA_TPTC while issuing read and write commands. The read or write commands have the same privilege identification, and privilege level as that programmed in the EDMA transfer in the channel controller. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1083 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## _**11.2.3.12.3 Error Generation**_ 

Errors are generated if enabled under three conditions: 

- EDMA_TPTC detection of an error signaled by the source or destination address. 

- Attempt to read or write to an invalid address in the configuration memory map. 

- Detection of a constant addressing mode TR violating the constant addressing mode transfer rules (the source/destination addresses and source/destination indexes must be aligned to 32 bytes). 

Either or all error types may be disabled. If an error bit is set and enabled, the error interrupt for the concerned transfer controller is generated. 

## _**11.2.3.12.4 Debug Features**_ 

The DMA program register set, DMA source active register set, and the destination FIFO register set are used to derive a brief history of TRs serviced through the transfer controller. 

Additionally, the EDMA_TPTC status register EDMA_TPTCn_TCSTAT has dedicated bit fields to indicate the ongoing activity within different parts of the transfer controller: 

- The EDMA_TPTCn_TCSTAT[1] SRCACTV bit indicates whether the source active set is active. 

- The EDMA_TPTCn_TCSTAT[6:4] DSTACTV bit indicates the number of TRs resident in the destination register active set at a given instance. 

- The EDMA_TPTCn_TCSTAT[0] PROGBUSY bit indicates whether a valid TR is present in the DMA program set. 

## **Note** 

If the TRs are in progression, it must realize that there is a chance that the values read from the EDMA_TPTC status registers will be inconsistent since the EDMA_TPTC changes the values of these registers due to ongoing activities. 

It is recommended that to ensure no additional submission of TRs to the EDMA_TPTC in order to facilitate ease of debug. 

## _**11.2.3.12.4.1 Destination FIFO Register Pointer**_ 

The destination FIFO register pointer is implemented as a circular buffer with the start pointer being EDMA_TPTCn_TCSTAT[12:11] DFSTRTPTR and a buffer depth of usually 2 or 4. The EDMA_TPTC maintains two important status details in EDMA_TPTCn_TCSTAT that are used during advanced debugging, if necessary. The EDMA_TPTCn_TCSTAT[12:11] DFSTRTPTR is a start pointer, the index to the head of the destination FIFO register. The EDMA_TPTCn_TCSTAT[6:4] DSTACTV is a counter for the number of valid (occupied) entries. These registers are used to get a brief history of transfers. 

Examples of some register field values and their interpretation: 

- EDMA_TPTCn_TCSTAT[12:11] DFSTRTPTR = 0x0 and EDMA_TPTCn_TCSTAT[6:4] DSTACTV = 0x0 implies that no TRs are stored in the destination FIFO register. 

- EDMA_TPTCn_TCSTAT[12:11] DFSTRTPTR = 0x1 and EDMA_TPTCn_TCSTAT[6:4] DSTACTV = 0x2 implies that two TRs are present. The first pending TR is read from the destination FIFO register entry 1 and the second pending TR is read from the destination FIFO register entry 2. 

- EDMA_TPTCn_TCSTAT[12:11] DFSTRTPTR = 0x3 and EDMA_TPTCn_TCSTAT[6:4] DSTACTV = 0x2 implies that two TRs are present. The first pending TR is read from the destination FIFO register entry 3 and the second pending TR is read from the destination FIFO register entry 0. 

## **11.2.3.13 Event Dataflow** 

This section summarizes the data flow of a single event, from the time the event is latched to the channel controller to the time the transfer completion code is returned. The following steps list the sequence of EDMA_TPCC activity: 

1. Event is asserted from an external source (peripheral or external interrupt). This also is similar for a manually-triggered, chained-triggered, or QDMA-triggered event. The event is latched 

1084 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

into the EDMA_TPCC_ER[31:0]E _n_ / EDMA_TPCC_ERH[31:0] E _n_ (or EDMA_TPCC_CER[31:0] E _n_ / EDMA_TPCC_CERH[31:0] E _n_ , EDMA_TPCC_ESR[31:0] E _n_ / EDMA_TPCC_ESRH[31:0] E _n_ , EDMA_TPCC_QER[7:0] E _n_ ) bit. 

2. Once an event is prioritized and queued into the appropriate event queue, the EDMA_TPCC_SER[31:0] E _n_ \ EDMA_TPCC_SERH[31:0] E _n_ (or EDMA_TPCC_QSER[7:0] E _n_ ) bit is set to inform the event prioritization / processing logic to disregard this event since it is already in the queue. Alternatively, if the transfer controller and the event queue are empty, then the event bypasses the queue. 

3. The EDMA_TPCC processing and the submission logic evaluates the appropriate PaRAM set and determines whether it is a non-null and non-dummy transfer request (TR). 

4. The EDMA_TPCC clears the EDMA_TPCC_ER[31:0] E _n_ / EDMA_TPCC_ERH[31:0] E _n_ (or EDMA_TPCC_CER[31:0] E _n_ / EDMA_TPCC_CERH[31:0] E _n_ , EDMA_TPCC_ESR[31:0]E _n_ / EDMA_TPCC_ESRH[31:0] E _n_ , EDMA_TPCC_QER[31:0] E _n_ ) bit and the EDMA_TPCC_SER[31:0] E _n_ / EDMA_TPCC_SERH[31:0] E _n_ bit as soon as it determines the TR is non-null. In the case of a null set, the EDMA_TPCC_SER[31:0] E _n_ / EDMA_TPCC_SERH[31:0] E _n_ bit remains set. It submits the non-null/non-dummy TR to the associated transfer controller. If the TR was programmed for early completion, the EDMA_TPCC immediately sets the interrupt pending register (EDMA_TPCC_IPR[31:0] I[TCC] / EDMA_TPCC_IPRH[31:0] I[TCC] - 32). 

5. If the TR was programmed for normal completion, the EDMA_TPCC sets the interrupt pending register (EDMA_TPCC_IPR[31:0] I[TCC] / EDMA_TPCC_IPRH[31:0] I[TCC]) when the EDMA_TPTC informs the EDMA_TPCC about completion of the transfer (returns transfer completion codes). 

6. The EDMA_TPCC programs the associated EDMA_TPTC's Program Register Set with the TR. 

7. The TR is then passed to the Source Active set and the DST FIFO Register Set, if both the register sets are available. 

8. The Read Controller processes the TR by issuing read commands to the source peripheral endpoint. The Read Data lands in the Data FIFO of the EDMA_TPTC _n_ . 

9. As soon as sufficient data is available, the Write Controller begins processing the TR by issuing write commands to the destination peripheral endpoint. 

10. This continues until the TR completes and the EDMA_TPTC _n_ then signals completion status to the EDMA_TPCC. 

## **11.2.3.14 EDMA Controller Prioritization** 

The EDMA controller has many implementation rules to deal with concurrent events/channels, transfers, etc. The following subsections detail various arbitration details whenever there might be occurrence of concurrent activity. Figure 11-20 shows the different places EDMA priorities come into play. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1085 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

**==> picture [479 x 465] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>From peripherals/external events Trigger source priority<br>E63 E1 E0<br>Channel Event queues PaRAM<br>Event priority 0 Dequeue Parameter<br>register priority entry 0 TC0<br>Event (EDMA_TPCC_ER/ERH) Parameter<br>trigger Event entry 1<br>64<br>enable<br>register 15<br>(EDMA_TPCC_EER/EERH)<br>0<br>Event<br>Manual set 64<br>trigger register<br>(EDMA_TPCC_ESR/ESRH) 64 Parameter<br>entry 510<br>15<br>Chain Parameter TC1<br>Chained<br>trigger entry 511<br>event<br>register Queue bypass<br>(EDMA_TPCC_CER/CERH)<br>QDMA<br>event 8 System<br>register priority<br>(EDMA_TPCC_QER) EDMA Channel Controller<br>QDMA trigger<br>To chained event register (CER/CERH) Completion From<br>detection EDMA_TPTC0<br>From<br>EDMA_TPTC1<br>Completion<br>interface<br>Memory Error Completion<br>protection detection interrupt<br>EDMA_TPCC_MPINT Read/Write EDMA_TPCC_ERRINT EDMA_TPCC_INT[0:7]<br>to/from EDMA<br>Queue 0<br>64:1 priority encoder<br>Channel mapping<br>Queue 1<br>Transfer request process submit<br>8:1 priority encoder<br>Early completion<br>L3_MAIN<br>**----- End of picture text -----**<br>


**==> picture [18 x 3] intentionally omitted <==**

**----- Start of picture text -----**<br>
edma-020<br>**----- End of picture text -----**<br>


**Figure 11-20. EDMA Prioritization** 

## _**11.2.3.14.1 Channel Priority**_ 

The EDMA event registers EDMA_TPCC_ER and EDMA_TPCC_ERH capture up to 64 events, the QDMA event register EDMA_TPCC_QER captures QDMA events for all QDMA channels therefore, it is possible for events to occur simultaneously on the DMA/QDMA event inputs. For events arriving simultaneously, the event associated with the lowest channel number is prioritized for submission to the event queues (for DMA events, channel 0 has the highest priority and channel 63 has the lowest priority, for QDMA events, channel 0 has the highest priority and channel 7 has the lowest priority). This mechanism only sorts simultaneous events for submission to the event queues. 

If a DMA and QDMA event occurs simultaneously, the DMA event always has prioritization against the QDMA event for submission to the event queues. 

1086 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## _**11.2.3.14.2 Trigger Source Priority**_ 

If a EDMA channel is associated with more than one trigger source (event trigger, manual trigger, and chain trigger), and if multiple events are set simultaneously for the same channel (EDMA_TPCC_ER[31:0] E _n_ = 1, EDMA_TPCC_ESR[31:0] E _n_ = 1 , EDMA_TPCC_CER[31:0] E _n_ = 1) , then the EDMA_TPCC always services these events in the following priority order: event trigger (via EDMA_TPCC_ER) is higher priority than chain trigger (via EDMA_TPCC_CER) and chain trigger is higher priority than manual trigger (via EDMA_TPCC_ESR). 

This implies that if for channel 0, both EDMA_TPCC_ER[0] E0 = 1 and EDMA_TPCC_CER[0] E0 = 1 at the same time, then the EDMA_TPCC_ER[0] E0 event is always queued before the EDMA_TPCC_CER[0] E0 event. 

## _**11.2.3.14.3 Dequeue Priority**_ 

The priority of the associated transfer request (TR) is further mitigated by which event queue is being used for event submission (dictated by EDMA_TPCC_DMAQNUMN_k and EDMA_TPCC_QDMAQNUM). For submission of a TR to the transfer request, events need to be de-queued from the event queues. Queue 0 has the highest dequeue priority and queue 1 the lowest. 

## **11.2.3.15 Emulation Considerations** 

During debug when using the emulator, the CPU(s) may be halted on an execute packet boundary for singlestepping, benchmarking, profiling, or other debug purposes. During an emulation halt, the EDMA channel controller and transfer controller operations continue. Events continue to be latched and processed and transfer requests continue to be submitted and serviced. 

Since EDMA is involved in servicing multiple controller and target peripherals, it is not feasible to have an independent behavior of the EDMA for emulation halts. EDMA functionality would be coupled with the peripherals it is servicing, which might have different behavior during emulation halts. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1087 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## _**11.2.4 EDMA Transfer Examples**_ 

The EDMA channel controller performs a variety of transfers depending on the parameter configuration. The following sections provide a description and PaRAM configuration for some typical use case scenarios. 

## **11.2.4.1 Block Move Example** 

The most basic transfer performed by the EDMA is a block move. During device operation it is often necessary to transfer a block of data from one location to another, usually between on-chip and off-chip memory. 

In this example, a section of data is to be copied from external memory to internal L2 SRAM as shown in Figure 11-21. 

The source address for the transfer is set to the start of the data block in external memory, and the destination address is set to the start of the data block in L2. If the data block is less than 64K bytes, the PaRAM configuration shown in Figure 11-22 holds true with the synchronization type set to A-synchronized and indexes cleared to 0. If the amount of data is greater than or equal to 64K bytes, EDMA_TPCC_ABCNT_n[31:16] BCNT and the B-indexes need to be set appropriately with the synchronization type set to AB-synchronized. The EDMA_TPCC_OPT_n[3] STATIC bit is set to prevent linking. 

This transfer example may also be set up using QDMA. For successive transfer submissions, of a similar nature, the number of cycles used to submit the transfer are fewer depending on the number of changing transfer parameters. The QDMA trigger word must be programed to be the highest numbered offset in the PaRAM set that undergoes change. 

Figure 11-22 shows the parameters Block Move transfer. 

**==> picture [440 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
Channel Source 1 2 3 4 5 6 7 8 Channel Destination 1 2 3 4 5 6 7 8<br>Address (SRC) Address (DST)<br>9 10 11 12 13 14 15 16 9 10 11 12 13 14 15 16<br>17 18 19 20 21 ... ... 17 18 19 20 21 ... ...<br>... ... 244 245 246 247 248 ... ... 244 245 246 247 248<br>249 250 251 252 253 254 255 256 249 250 251 252 253 254 255 256<br>edma-021<br>**----- End of picture text -----**<br>


**Figure 11-21. Block Move Example** 

1088 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## **Figure 11-22. Block Move Example PaRAM Configuration** 

## _(a) EDMA Parameters_ 

|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|
|---|---|---|---|---|---|---|
||0010 0008h|||Channel Options Parameter (OPT)|||
||Channel Source Address (SRC)|||Channel Source Address (SRC)|||
||0001h|FFFFh||Count for 2nd Dimension (BCNT)|Count for 1st Dimension (ACNT)||
||Channel Destination Address (DST)|||Channel Destination Address (DST)|||
||0000h|0000h||Destination BCNT Index (DBIDX)|Source BCNT Index (SBIDX)||
||0000h|FFFFh||BCNT Reload (BCNTRLD)|Link Address (LINK)||
||0000h|0000h||Destination CCNT Index (DCIDX)|Source CCNT Index (SCIDX)||
||0000h|0001h||Reserved|Count for 3rd Dimension (CCNT)||



## _(b)Channel Options Parameter (OPT) Content_ 

- EDMA_TPCC_OPT_n[3] STATIC = 0x1 

- EDMA_TPCC_OPT_n[20] TCINTEN = 0x1 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1089 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## **11.2.4.2 Subframe Extraction Example** 

The EDMA can efficiently extract a small frame of data from a larger frame of data. By performing a 2D-to-1D transfer, the EDMA retrieves a portion of data for the CPU to process. In this example, a 640 × 480-pixel frame of video data is stored in external memory. Each pixel is represented by a 16-bit halfword. The CPU extracts a 16 × 12-pixel subframe of the image for processing. To facilitate more efficient processing time by the CPU, the EDMA places the subframe in internal L2 SRAM. Figure 11-23 shows the transfer of a subframe from external memory to L2. 

The same PaRAM entry options are used for QDMA channels, as well as DMA channels. The EDMA_TPCC_OPT_n[3] STATIC bit is set to prevent linking. For successive transfers, only changed parameters need to be programmed before triggering the channel. 

Figure 11-24 shows the parameters for Subframe Extraction transfer. 

**==> picture [500 x 198] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 Channel Destination<br>Address (DST)<br>Channel Source 0_ 1 0 _2 0_3 0 _ 4 0_5 0_6 0_7 0_8 0_9 0_A 0_B 0_C 0_D 0_E 0_F 0_10<br>Address (SRC) 1_1 1_2 1_3 1_4 1_5 1_6 1_7 1_8 1_9 1_A 1_B 1_C 1_D 1_E 1_F 1_10<br>2_1 2_2 2_3 2_4 2_5 2_6 2_7 2_8 2_9 2_A 2_B 2_C 2_D 2_E 2_F 2_10<br>3_1 3_2 3_3 3_4 3_5 3_6 3_7 3_8 3_9 3_A 3_B 3_C 3_D 3_E 3_F 3_10<br>4_1 4_2 4_3 4_4 4_5 4_6 4_7 4_8 4_9 4_A 4_B 4_C 4_D 4_E 4_F 4_10<br>5_1 5_2 5_3 5_4 5_5 5_6 5_7 5_8 5_9 5_A 5_B 5_C 5_D 5_E 5_F 5_10<br>6_1 6_2 6_3 6_4 6_5 6_6 6_7 6_8 6_9 6_A 6_B 6_C 6_D 6_E 6_F 6_10<br>7_1 7_2 7_3 7_4 7_5 7_6 7_7 7_8 7_9 7_A 7_B 7_C 7_D 7_E 7_F 7_10<br>8_1 8_2 8_3 8_4 8_5 8_6 8_7 8_8 8_9 8_A 8_B 8_C 8_D 8_E 8_F 8_10<br>9_1 9_2 9_3 9_4 9_5 9_6 9_7 9_8 9_9 9_A 9_B 9_C 9_D 9_E 9_F 9_10<br>A_1 A_2 A_3 A_4 A_5 A_6 A_7 A_8 A_9 A_A A_B A_C A_D A_E A_F A_10<br>B_1 B_2 B_3 B_4 B_5 B_6 B_7 B_8 B_9 B_A B_B B_C B_D B_E B_F B_10<br>479<br>0 6<br>3<br>9 edma-022<br>**----- End of picture text -----**<br>


**Figure 11-23. Subframe Extraction Transfer** 

**Figure 11-24. Subframe Extraction Example PaRAM Configuration** 

## _(a) EDMA Parameters_ 

|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|
|---|---|---|---|---|---|---|
||0010 000Ch|||Channel Options Parameter (OPT)|||
||Channel Source Address (SRC)|||Channel Source Address (SRC)|||
||000Ch|0020h||Count for 2nd Dimension (BCNT)|Count for 1st Dimension (ACNT)||
||Channel Destination Address (DST)|||Channel Destination Address (DST)|||
||0020h|0500h||Destination BCNT Index (DBIDX)|Source BCNT Index (SBIDX)||
||0000h|FFFFh||BCNT Reload (BCNTRLD)|Link Address (LINK)||
||0000h|0000h||Destination CCNT Index (DCIDX)|Source CCNT Index (SCIDX)||
||0000h|0001h||Reserved|Count for 3rd Dimension (CCNT)||



## _(b)Channel Options Parameter (OPT) Content_ 

- EDMA_TPCC_OPT_n[2] SYNCDIM = 0x1 

- EDMA_TPCC_OPT_n[3] STATIC = 0x1 

- EDMA_TPCC_OPT_n[20] TCINTEN = 0x1 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1090 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## **11.2.4.3 Data Sorting Example** 

Many applications require the use of multiple data arrays, it is often desirable to have the arrays arranged such that the first elements of each array are adjacent, the second elements are adjacent, and so on. Often this is not how the data is presented to the device. Either data is transferred via a peripheral with the data arrays arriving one after the other or the arrays are located in memory with each array occupying a portion of contiguous memory spaces. For these instances, the EDMA can reorganize the data into the desired format. 

To determine the parameter set values, the following need to be considered: 

- ACNT - Program this to be the size in bytes of an element. 

- BCNT - Program this to be the number of elements in a frame. 

- CCNT - Program this to be the number of frames. 

- SBIDX - Program this to be the size of the element or ACNT. 

- DBIDX - CCNT × ACNT 

- SCIDX - ACNT × BCNT 

- DCIDX - ACNT 

The synchronization type needs to be AB-synchronized and the EDMA_TPCC_OPT_n[3] STATIC bit is 0 to allow updates to the parameter set. It is advised to use normal EDMA channels for sorting. 

It is not possible to sort this with a single trigger event. Instead, the channel can be programmed to be chained to itself. After BCNT elements get sorted, intermediate chaining could be used to trigger the channel again causing the transfer of the next BCNT elements and so on. Figure 11-26 shows the parameter set programming for this transfer, assuming channel 0 and an element size of 4 bytes. 

Figure 11-25 shows the Data Sorting transfer 

|re 11-25shows the Data Sorting transfer|||||
|---|---|---|---|---|
|A_1022<br>A_1023 A_1024<br>B_1023<br>B_1022<br>B_1024<br>D_1023<br>C_1023<br>D_1022<br>C_1022<br>D_1024<br>C_1024<br>...<br>...<br>...<br>...<br>...<br>...<br>...<br>...<br>D_2<br>D_1<br>D_3<br>C_2<br>B_2<br>A_2<br>C_1<br>B_1<br>A_1<br>B_3<br>C_3<br>A_3<br>Channel Source<br>Address (SRC)<br>D_1<br>D_2<br>D_1023<br>...<br>D_3<br>...<br>D_1022<br>D_1024<br>B_1<br>C_1<br>A_1<br>B_2<br>C_2<br>A_2<br>C_1023<br>B_1023<br>A_1023<br>...<br>...<br>...<br>B_3<br>C_3<br>A_3<br>...<br>...<br>...<br>C_1022<br>B_1022<br>A_1022<br>B_1024 C_1024<br>A_1024<br>Channel<br>Destination<br>Address (DST)<br>|A_1|B_1|C_1|D_1|
||A_2|B_2|C_2|D_2|
||A_3|B_3|C_3|D_3|
||...|...|...|...|
||...|...|...|...|
||A_1022|B_1022|C_1022|D_1022|
||A_1023|B_1023|C_1023|D_1023|
||A_1024|B_1024|C_1024|D_1024|



edma-023 

**Figure 11-25. Data Sorting Example** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1091 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## **Figure 11-26. Data Sorting Example PaRAM Configuration** 

## _(a) EDMA Parameters_ 

|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|**Parameter Contents**<br>**Parameter**|
|---|---|---|---|---|---|---|
||0090 0004h|||Channel Options Parameter (OPT)|||
||Channel Source Address (SRC)|||Channel Source Address (SRC)|||
||0400h|0004h||Count for 2nd Dimension (BCNT)|Count for 1st Dimension (ACNT)||
||Channel Destination Address (DST)|||Channel Destination Address (DST)|||
||0010h|0001h||Destination BCNT Index (DSTBIDX)|Source BCNT Index (SRCBIDX)||
||0000h|FFFFh||BCNT Reload (BCNTRLD)|Link Address (LINK)||
||0001h|1000h||Destination CCNT Index (DSTCIDX)|Source CCNT Index (SRCCIDX)||
||0000h|0004h||Reserved|Count for 3rd Dimension (CCNT)||



## _(b) Channel Options Parameter (OPT) Content_ 

- EDMA_TPCC_OPT_n[2] SYNCDIM = 0x1 

- EDMA_TPCC_OPT_n[20] TCINTEN = 0x1 

- EDMA_TPCC_OPT_n[23] ITCCHEN = 0x1 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1092 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## **11.2.4.4 Setting Up an EDMA Transfer** 

The following list provides a quick guide for the typical steps involved in setting up a transfer. 

1. Initiating a DMA/QDMA channel 

   - a. Determine the type of channel (QDMA or DMA) to be used. b. Channel mapping 

      - i. If using a QDMA channel, program the EDMA_TPCC_QCHMAPN_j with the parameter set number to which the channel maps and the trigger word. 

      - ii. If using a DMA channel, program the EDMA_TPCC_DCHMAPN_m with the parameter set number to which the channel maps. 

   - c. If the channel is being used in the context of a shadow region, ensure the EDMA_TPCC_DRAEM_k / EDMA_TPCC_DRAEHM_k for the region is properly set up to allow read write accesses to bits in the event registers and interrupt registers in the Shadow region memory map. The subsequent steps in this process should be done using the respective shadow region registers. (Shadow region descriptions and usage are provided in Section 11.2.3.7.1.) 

   - d. Determine the type of triggering used. 

      - i. If external events are used for triggering (DMA channels), enable the respective event in EDMA_TPCC_EER / EDMA_TPCC_EERH by writing into EDMA_TPCC_EESR / EDMA_TPCC_EESRH. 

      - ii. If QDMA Channel is used, enable the channel in EDMA_TPCC_QEER by writing into EDMA_TPCC_QEESR. 

   - e. Queue setup 

      - i. If a QDMA channel is used, set up the EDMA_TPCC_QDMAQNUM to map the channel to the respective event queue. 

      - ii. If a DMA channel is used, set up the EDMA_TPCC_DMAQNUMN_k to map the event to the respective event queue. 

2. Parameter set setup 

   - a. Program the PaRAM set number associated with the channel. Note that 

## **Note** 

If it is a QDMA channel, the PaRAM entry that is configured as trigger word is written to last. Alternatively, enable the QDMA channel (step 1-d-ii above) just before the write to the trigger word. 

3. Interrupt setup 

   - a. Enable the interrupt in the EDMA_TPCC_IER / EDMA_TPCC_IERH by writing into EDMA_TPCC_IESR / EDMA_TPCC_IESRH. 

   - b. Ensure the EDMA_TPCC completion interrupt (this refers to either the Global interrupt or the shadow region interrupt) is enabled properly in the Device Interrupt controller. 

   - c. Set up the interrupt controller properly to receive the expected EDMA interrupt. 

4. Initiate transfer 

   - a. This step is highly dependent on the event trigger source: 

      - i. If the source is an external event coming from a peripheral, the peripheral will be enabled to start generating relevant EDMA events that can be latched to the EDMA_TPCC_ER transfer. 

      - ii. For QDMA events, writes to the trigger word (step 2-a above) will initiate the transfer. 

      - iii. Manually triggered transfers will be initiated by writes to the Event Set Registers EDMA_TPCC_ESR / EDMA_TPCC_ESRH. 

      - iv. Chained-trigger events initiate when a previous transfer returns a transfer completion code equal to the chained channel number. 

5. Wait for completion 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1093 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

- a. If the interrupts are enabled as mentioned in step 3 above, then the EDMA_TPCC will generate a completion interrupt to the CPU whenever transfer completion results in setting the corresponding bits in the interrupt pending register EDMA_TPCC_IPR / EDMA_TPCC_IPRH. The set bits must be cleared in the EDMA_TPCC_IPR / EDMA_TPCC_IPRH by writing to corresponding bit in EDMA_TPCC_ICR / EDMA_TPCC_ICRH. 

- b. If polling for completion (interrupts not enabled in the device controller), then the application code can wait on the expected bits to be set in the EDMA_TPCC_IPR / EDMA_TPCC_IPRH. Again, the set bits in the EDMA_TPCC_IPR / EDMA_TPCC_IPRH must be manually cleared via EDMA_TPCC_ICR / EDMA_TPCC_ICRH before the next set of transfers is performed for the same transfer completion code values. 

1094 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Data Movement Architecture_ 

## _**11.2.5 EDMA Debug Checklist and Programming Tips**_ 

This section lists some tips to keep in mind while debugging applications using the EDMA controller. 

## **11.2.5.1 EDMA Debug Checklist** 

Table 11-21 provides some common issues and their probable causes and resolutions. 

## **Table 11-21. Debug Checklist** 

|**Issue**|**Description/Solution**|
|---|---|
|The transfer associated with the channel<br>does not happen.<br>The channel does not get serviced.|The EDMA_TPCC may not service a transfer request, even though the associated PaRAM<br>set is programmed appropriately. Check for the following:<br>1) Verify that events are enabled, i.e., if an external/peripheral event is latched in Event<br>Registers EDMA_TPCC_ER / EDMA_TPCC_ERH, check that the event is enabled in the<br>Event Enable Registers EDMA_TPCC_EER / EDMA_TPCC_EERH. Similarly, for QDMA<br>channels, check that QDMA events are appropriately enabled in the QDMA Event Enable<br>Register EDMA_TPCC_QEER.<br>2) Verify that the DMA or QDMA Secondary Event Register EDMA_TPCC_SER /<br>EDMA_TPCC_SERH / EDMA_TPCC_QSER bits corresponding to the particular event or<br>channel are not set.|
|The Secondary Event Registers bits are set,<br>not allowing additional transfers to occur on a<br>channel.|It is possible that a trigger event was received when the parameter set associated with the<br>channel/event was a NULL set for a previous transfer on the channel. This is typical in two<br>cases:<br>1) QDMA channels: Typically if the parameter set is non-static and expected<br>to be terminated by a NULL set (i.e., EDMA_TPCC_OPT_n[3] STATIC = 0x0,<br>EDMA_TPCC_LNK_n[15:0] LINK = 0xFFFF), the parameter set is updated with a NULL<br>set after submission of the last TR. Because QDMA channels are auto-triggered, this<br>update caused the generation of an event. An event generated for a NULL set causes<br>an error condition and results in setting the bits corresponding to the QDMA channel in the<br>EDMA_TPCC_QEMR and EDMA_TPCC_QSER. This will disable further prioritization of the<br>channel.<br>2) DMA channels used in a continuous mode: The peripheral may be set up to continuously<br>generate infinite events . The parameter set may be programmed to expect only a finite<br>number of events and to be terminated by a NULL link. After the expected number of<br>events, the parameter set is reloaded with a NULL parameter set. Because the peripheral<br>will generate additional events, an error condition is set in the EDMA_TPCC_SER[31:0] E_n_<br>and EDMA_TPCC_EMR[31:0] E_n_set, preventing further event prioritization.<br>Check the number of events received is limited to the expected number of events<br>for which the parameter set is programmed, or check the bits corresponding<br>to particular channel or event are not set in the Secondary event registers<br>(EDMA_TPCC_SER / EDMA_TPCC_SERH / EDMA_TPCC_QSER) and Event Missed<br>Registers (EDMA_TPCC_EMR / EDMA_TPCC_EMRH / EDMA_TPCC_QEMR) before trying<br>to perform subsequent transfers for the event/channel.|
|Completion interrupts are not asserted, or no<br>further interrupts are received after the first<br>completion interrupt.|Check the following:<br>1) The interrupt generation is enabled in the EDMA_TPCC_OPT_n of the associated<br>PaRAM set (EDMA_TPCC_OPT_n[20] TCINTEN = 0x1 and/or EDMA_TPCC_OPT_n[20]<br>ITCINTEN = 0x1).<br>2) The interrupts are enabled in the EDMA Channel Controller, via the Interrupt Enable<br>Registers (EDMA_TPCC_IER / EDMA_TPCC_IERH ).<br>3) The corresponding interrupts are enabled in the device interrupt controller.<br>4) The set interrupts are cleared in the interrupt pending registers (EDMA_TPCC_IPR /<br>EDMA_TPCC_IPRH) before exiting the transfer completion interrupt service routine (ISR).<br>SeeSection 11.2.3.9.1.2 _Clearing Transfer Complerion Interrupts_for details on writing<br>EDMA ISRs.<br>5) If working with shadow region interrupts, make sure that the DMA Region<br>Access registers (EDMA_TPCC_DRAEM_k / EDMA_TPCC_DRAEHM_k ) are set up<br>properly, because the EDMA_TPCC_DRAEM_k / EDMA_TPCC_DRAEHM_k registers<br>act as secondary enables for shadow region completion interrupts, along with the<br>EDMA_TPCC_IER / EDMA_TPCC_IERH registers.<br>If working with shadow region interrupts, make sure that the bits corresponding to the<br>transfer completion code EDMA_TPCC_OPT_n[17:12] TCC value are also enabled in the<br>EDMA_TPCC_DRAEМ_k / EDMA_TPCC_DRAEHM_k registers. For instance, if the PaRAM<br>set associated with Channel 0 returns a completion code of 63 EDMA_TPCC_OPT_n[17:12]<br>TCC = 63, ensure that EDMA_TPCC_DRAEHM_k[31] E63 is also set for a shadow<br>region completion interrupt because the interrupt pending register bit set will be<br>EDMA_TPCC_IPRH[31] I63 (not EDMA_TPCC_IPR[0] I0).|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1095 

Copyright © 2025 Texas Instruments Incorporated 

_Data Movement Architecture_ 

www.ti.com 

## **11.2.5.2 EDMA Programming Tips** 

1. For several registers, the setting and clearing of bits needs to be done via separate dedicated registers. For example, the Event Register (EDMA_TPCC_ER / EDMA_TPCC_ERH) can only be cleared by writing a 1 to the corresponding bits in the Event Clear Registers (EDMA_TPCC_ECR / EDMA_TPCC_ECRH). Similarly, the Event Enable Register (EDMA_TPCC_EER / EDMA_TPCC_EERH) bits can only be set with writing of 0x1 to the Event Enable Set Registers (EDMA_TPCC_EESR / EDMA_TPCC_EESRH) and cleared with writing of 0x1 to the corresponding bits in the Event Enable Clear Register (EDMA_TPCC_EECR / EDMA_TPCC_EECRH). 

2. Writes to the shadow region memory maps are governed by region access registers (EDMA_TPCC_DRAE / EDMA_TPCC_DRAEHM_k / EDMA_TPCC_QRAEN_k). If the appropriate channels are not enabled in these registers, read/write access to the shadow region memory map is not enabled. 

3. When working with shadow region completion interrupts, ensure that the DMA Region Access Registers (EDMA_TPCC_DRAEM_k / EDMA_TPCC_DRAEHM_k) for every region are set in a mutually exclusive way (unless it is a requirement for an application). If there is an overlap in the allocated channels and transfer completion codes (setting of Interrupt Pending Register bits) in the region resource allocation, it results in multiple shadow region completion interrupts. 

   - For example, if EDMA_TPCC_DRAEM_k.DRAEM_0[0] E0 and EDMA_TPCC_DRAEM_k.DRAEM_1[0] E0 are both set, then on completion of a transfer that returns a TCC = 0x0, they will generate both shadow region 0 and 1 completion interrupts. 

4. While programming a non-dummy parameter set, ensure the EDMA_TPCC_CCNT_n[15:0] CCNT is not left to zero. 

5. Enable the EDMA_TPCC error interrupt in the device controller and attach an interrupt service routine (ISR) to ensure that error conditions are not missed in an application and are appropriately addressed with the ISR. 

6. Depending on the application, it can want to break large transfers into smaller transfers and use selfchaining to prevent starvation of other events in an event queue. 

7. In applications where a large transfer is broken into sets of small transfers using chaining or other methods, it chooses to use the early chaining option to reduce the time between the sets of transfers and increase the throughput. 

   - However, keep in mind that with early completion, all data might have not been received at the end point when completion is reported because the EDMA_TPCC internally signals completion when the TR is submitted to the EDMA_TPTC, potentially before any data has been transferred. 

8. The event queue entries can be observed to determine the last few events if there is a system failure (provided the entries were not bypassed). 

## _**11.2.6 EDMA Event Map**_ 

Events are mapped through DMA Trigger XBAR. 

See EDMA XBAR INTRTR0 

1096 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

