<!-- AM263P TRM | 12 Time Sync | 원본 p.1097-1109 | pymupdf4llm text+tables, images omitted -->

_Time Sync_ 

www.ti.com 

_Chapter 12_ _**Time Sync**_ 

**==> picture [506 x 40] intentionally omitted <==**

This chapter describes the time sync modules in the device. 

**12.1 Time Sync Architecture** ........................................................................................................................................1098 **12.2 Time Sync Routers** ............................................................................................................................................... 1100 **12.3 Time Sync and Compare Events** ......................................................................................................................... 1107 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1097 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

## **12.1 Time Sync Architecture** 

This section provides a high-level overview of the SoC time synchronization architecture. 

## _**12.1.1 Time Sync Architecture Overview**_ 

Table 12-1 shows the time synchronization functions supported by the device. 

**Table 12-1. Time Synchronization Functions in the SOC** 

|**Interface**|**Time Sync Functions**|**Supported by**|
|---|---|---|
|PRU-ICSS|IEEE 1588-2008 (1/2-step), 802.1AS, TSN|PRU-ICSS firmware|
|CPSW0|IEEE 1588-2008 (2-step), 802.1AS|CPTS in CPSW0|
|EPWMx.SYNCOUT|PWM SYNCOUT|EPWMx.SYNCOUT|



## **Note** 

These time sync functions are described in detail in each respective chapter. 

Any of these functions can be a time sync controller in the system. Sync routers (SOC_TIMESYNC_XBAR0, SOC_TIMESYNC_XBAR1) provide flexibility for each time domain to choose a synch controller independently. In addition these routers also provide selection of sync and compare events for routing as CPU or DMA events. 

Figure 12-1 shows a high-level overview of the SoC time sync architecture. 

1098 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

**==> picture [500 x 598] intentionally omitted <==**

**----- Start of picture text -----**<br>
R5 VIM(x4)R5 VIM(x4)<br>R5 VIM(x4)<br>R5 VIM(x4)<br>8 (2 x4) CAPEVT WRTI (x4)DT (x4)RTI (x4)<br>RTI (x4)<br>RTI (x4)<br>COMP<br>ICSS-M 2 EPWMx SYNCIN<br>16 EPWMx<br>SYNCINMUX<br>2 EDMA Triggers<br>EDMA_TRIG_ EDMA TPCC<br>XBAR<br>COMP 16 (4 x4) CPU Interrupts<br>R5 VIM(x4)<br>R5 VIM(x4)<br>R5 VIM(x4)<br>R5 VIM(x4)<br>GENF [2]<br>CPSW0_CPTS<br>SYNC<br>CPTS0_TS_SYNC 2 EDMA Triggers<br>PR0_IEP0_EDC_SYNC_OUTn EDMA_TRIG_XBAR EDMA TPCC<br>SYNC<br>ICSS-M 2<br>8 CPTS HW Push Events<br>CPSW0_CPTS<br>4<br>SYNCOUT<br>EPWMx<br>6<br>Capture Events<br>2 ICSS-M<br>6 Latch Events<br>GPIOx INTR<br>SOC_TIMESYNC_XBAR0<br>SOC_TIMESYNC_XBAR1<br>SYNCOUTXBAR<br>CONTROLSS_PWM<br>GPIO XBAR<br>INTERRUPT<br>**----- End of picture text -----**<br>


**Figure 12-1. SoC Time Sync Architecture** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1099 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

## **12.2 Time Sync Routers** 

## _**12.2.1 Time Sync Routers Overview**_ 

## **12.2.1.1 SOC_TIMESYNC_XBAR0 Overview** 

The Time Sync Event Router0 ( **SOC_TIMESYNC_XBAR0** ) implements a set of multiplexers to provide selection of various events to EPWM SYNCIN, RTI Capture and DMA Trigger. There is one register per output that controls the selection (SOC_TIMESYNC_XBAR0_MUXCNTL_y). 

The SOC_TIMESYNC_XBAR0 module has the following configuration: 

- Number of input events: 28 

- Number of output events: 20 

- Event input type: Pulse 

## **12.2.1.2 SOC_TIMESYNC_XBAR1 Overview** 

The Time Sync Event Router1 ( **SOC_TIMESYNC_XBAR1** ) implements a set of multiplexers to provide selection of various events to CPU Interrupts, DMA Triggers, CPTS Push events, ICSS Latch and capture events. There is one register per output that controls the selection (SOC_TIMESYNC_XBAR1_MUXCNTL_y). 

The SOC_TIMESYNC_XBAR1 module has the following configuration: 

- Number of input events: 16 

- Number of output events: 34 

- Event input type: Pulse 

## _**12.2.2 Time Sync Routers Integration**_ 

This section describes the Time Sync Routers integration in the device, including information about clocks, resets, and hardware requests. 

1100 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

## **12.2.2.1 SOC_TIMESYNC_XBAR0 Integration** 

**==> picture [282 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
SoC TIMESYNC<br>xBAR0<br>MMR<br>Configuration<br>Port<br>MSS  SYSCLK<br>RCM SYSRSTn<br>Time Sync<br>Sources SYNCEVENT_IN[27:0]<br>Time Sync<br>SYNCEVENT_OUT[19:0]<br>Sink<br>INFRA-0<br>Interconnect<br>**----- End of picture text -----**<br>


**Figure 12-2. SOC_TIMESYNC_XBAR0 Integration** 

**Table 12-2. SOC_TIMESYNC_XBAR0 Device Integration** 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|SOC_TIMESYNC_XBAR0|✔|VBUSP INFRA0 Interconnect|



## **Table 12-3. SOC_TIMESYNC_XBAR0 Clocks** 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|SOC_TIMES<br>YNC_XBAR<br>0|CLK|SYSCLK|MSS_RCM|200 MHz|SOC_TIMESYNC_XBAR0<br>Functional and Interface<br>clock|



## **Table 12-4. SOC_TIMESYNC_XBAR0 Resets** 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|SOC_TIME<br>SYNC_XBA<br>R0|RST|SYS_RST|RCM + Warm Reset Sources|SOC_TIMESYNC_XBAR0 Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1101 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

**Table 12-5. SOC_TIMESYNC_XBAR0 Time Sync Output Events** 

|**Module Instance**|**Module Sync**<br>**Output**|**Module Sync**<br>**Output**|**Destination**<br>**Sync Signal**|**Destination**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|---|---|
|SOC_TIMESYNC_XBA<br>R0|SYNCEVENT_<br>OUT0||EPWMx_SYNC<br>IN58|EPWMx||Edge|Selectable sync event 0|
||SYNCEVENT_<br>OUT1||EPWMx_SYNC<br>IN59|EPWMx|||Selectable sync event 1|
||SYNCEVENT_<br>OUT2||CAPEVT0|RTI0,WDT0|||Selectable sync event 2|
||SYNCEVENT_<br>OUT3||CAPEVT1|RTI0,WDT0|||Selectable sync event 3|
||SYNCEVENT_<br>OUT4||CAPEVT0|RTI1,WDT1|||Selectable sync event 4|
||SYNCEVENT_<br>OUT5||CAPEVT1|RTI1,WDT1|||Selectable sync event 5|
||SYNCEVENT_<br>OUT6||CAPEVT0|RTI2,WDT2|||Selectable sync event 6|
||SYNCEVENT_<br>OUT7||CAPEVT1|RTI2,WDT2|||Selectable sync event 7|
||SYNCEVENT_<br>OUT8||CAPEVT0|RTI3,WDT3|||Selectable sync event 8|
||SYNCEVENT_<br>OUT9||CAPEVT1|RTI3,WDT3|||Selectable sync event 9|
||SYNCEVENT_<br>OUT10||IN_INTR111|DMA_TRIGGE<br>R_XBAR|||Selectable sync event 10|
||SYNCEVENT_<br>OUT11||IN_INTR112|Sync_Xbarout_<br>1|||Selectable sync event 11|
||SYNCEVENT_<br>OUT12||CAPEVT0|RTI4|||Selectable sync event 12|
||SYNCEVENT_<br>OUT13||CAPEVT1|RTI4|||Selectable sync event 13|
||SYNCEVENT_<br>OUT14||CAPEVT0|RTI5|||Selectable sync event 14|
||SYNCEVENT_<br>OUT15||CAPEVT1|RTI5|||Selectable sync event 15|
||SYNCEVENT_<br>OUT16||CAPEVT0|RTI6|||Selectable sync event 16|
||SYNCEVENT_<br>OUT17||CAPEVT1|RTI6|||Selectable sync event 17|
||SYNCEVENT_<br>OUT18||CAPEVT0|RTI7|||Selectable sync event 18|
||SYNCEVENT_<br>OUT19||CAPEVT1|RTI7|||Selectable sync event 19|
|||||||||
|**Module Instance**||**Module Sync Input**|||||**TimeSync Event Sources**|
|SOC_TIMESYNC_XBAR0||SYNCEVENT_IN[27:0]|||SeeSOC_TIMESYNC_XBAR0 Event Maptable for time sync event<br>mapping.|||



1102 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

## **12.2.2.2 SOC_TIMESYNC_XBAR1 Integration** 

**==> picture [280 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
SoC TIMESYNC<br>xBAR1<br>MMR<br>Configuration<br>Port<br>MSS  SYSCLK<br>RCM SYSRSTn<br>Time Sync<br>Sources SYNCEVENT_IN[15:0]<br>Time Sync<br>SYNCEVENT_OUT[33:0]<br>Sink<br>INFRA-0<br>Interconnect<br>**----- End of picture text -----**<br>


**Figure 12-3. SOC_TIMESYNC_XBAR1 Integration** 

**Table 12-6. SOC_TIMESYNC_XBAR1 Device Integration** 

|**Module Instance**|**Device Allocation**|**Device Allocation**|**Device Allocation**|**Device Allocation**|**SoC Interconnect**|**SoC Interconnect**|**SoC Interconnect**|
|---|---|---|---|---|---|---|---|
|SOC_TIMESYNC_XBAR1|✔||||VBUSP INFRA Interconnect|||
|**Table 12-7. SOC_TIMESYNC_XBAR1 Clocks**||||||||
|**Module Instance**||**Module Clock**<br>**Input**|**Source Clock**<br>**Signal**|**Source**||**Default**<br>**Freq**|**Description**|
|SOC_TIMESYNC_XBAR1||CLK|SYSCLK|MSS_RCM||200 MHz|SOC_TIMESYNC_XBAR1 Functional<br>and Interface clock|



## **Table 12-8. SOC_TIMESYNC_XBAR1 Resets** 

|**Module Instance**|**Module**<br>**Reset**<br>**Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|SOC_TIMESYNC_XB<br>AR1|RST|SYS_RST|RCM + Warm Reset Sources|SOC_TIMESYNC_XBAR1 Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1103 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

**Table 12-9. SOC_TIMESYNC_XBAR1 Time Sync Output Events** 

|**Module Instance**|**Module Sync**<br>**Output**|**Destination**<br>**Sync Signal**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SOC_TIMESYNC_XBA<br>R1|SYNCEVENT_<br>OUT0|EDMA_TRIGG<br>ERXBAR_IN11<br>1|EDMA_TRIGG<br>ERXBAR|Edge|Selectablesync event 0|
||SYNCEVENT_<br>OUT1|EDMA_TRIGG<br>ERXBAR_IN11<br>2|EDMA_TRIGG<br>ERXBAR||Selectablesync event 1|
||SYNCEVENT_<br>OUT2|R5SS0_CORE<br>0_INTR138|R5SS0_CORE<br>0_VIM||Selectablesync event 2|
||SYNCEVENT_<br>OUT3|R5SS0_CORE<br>0_INTR139|R5SS0_CORE<br>0_VIM||Selectablesync event 3|
||SYNCEVENT_<br>OUT4|R5SS0_CORE<br>0_INTR140|R5SS0_CORE<br>0_VIM||Selectablesync event 4|
||SYNCEVENT_<br>OUT5|R5SS0_CORE<br>0_INTR141|R5SS0_CORE<br>0_VIM||Selectablesync event 5|
||SYNCEVENT_<br>OUT6|R5SS0_CORE<br>1_INTR138|R5SS0_CORE<br>1_VIM||Selectablesync event 6|
||SYNCEVENT_<br>OUT7|R5SS0_CORE<br>1_INTR139|R5SS0_CORE<br>1_VIM||Selectablesync event 7|
||SYNCEVENT_<br>OUT8|R5SS0_CORE<br>1_INTR140|R5SS0_CORE<br>1_VIM||Selectablesync event 8|
||SYNCEVENT_<br>OUT9|R5SS0_CORE<br>1_INTR141|R5SS0_CORE<br>1_VIM||Selectablesync event 9|
||SYNCEVENT_<br>OUT10|ICSSM0_EDC_<br>LATCH0_IN|PRU_ICSSM0||Selectablesync event 10|
||SYNCEVENT_<br>OUT11|ICSSM0_EDC_<br>LATCH1_IN|PRU_ICSSM0||Selectablesync event 11|
||SYNCEVENT_<br>OUT12|ICSSM0_IEP_<br>CAP_INT R0|PRU_ICSSM0||Selectablesync event 12|
||SYNCEVENT_<br>OUT13|ICSSM0_IEP_<br>CAP_INT R1|PRU_ICSSM0||Selectablesync event 13|
||SYNCEVENT_<br>OUT14|ICSSM0_IEP_<br>CAP_INT R2|PRU_ICSSM0||Selectablesync event 14|
||SYNCEVENT_<br>OUT15|ICSSM0_IEP_<br>CAP_INT R3|PRU_ICSSM0||Selectablesync event 15|
||SYNCEVENT_<br>OUT16|ICSSM0_IEP_<br>CAP_INT R4|PRU_ICSSM0||Selectablesync event 16|



1104 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

**Table 12-9. SOC_TIMESYNC_XBAR1 Time Sync Output Events (continued)** 

|**Module Instance**|**Module Sync**<br>**Output**|**Destination**<br>**Sync Signal**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SOC_TIMESYNC_XBA<br>R1|SYNCEVENT_<br>OUT17|ICSSM0_IEP_<br>CAP_INT R5|PRU_ICSSM0|Edge|Selectablesync event 17|
||SYNCEVENT_<br>OUT18|CPTS_HW1_T<br>S_PUSH|CPSW0_CPTS||Selectablesync event 18|
||SYNCEVENT_<br>OUT19|CPTS_HW2_T<br>S_PUSH|CPSW0_CPTS||Selectablesync event 19|
||SYNCEVENT_<br>OUT20|CPTS_HW3_T<br>S_PUSH|CPSW0_CPTS||Selectablesync event 20|
||SYNCEVENT_<br>OUT21|CPTS_HW4_T<br>S_PUSH|CPSW0_CPTS||Selectablesync event 21|
||SYNCEVENT_<br>OUT22|CPTS_HW5_T<br>S_PUSH|CPSW0_CPTS||Selectablesync event 22|
||SYNCEVENT_<br>OUT23|CPTS_HW6_T<br>S_PUSH|CPSW0_CPTS||Selectablesync event 23|
||SYNCEVENT_<br>OUT24|CPTS_HW7_T<br>S_PUSH|CPSW0_CPTS||Selectablesync event 24|
||SYNCEVENT_<br>OUT25|CPTS_HW8_T<br>S_PUSH|CPSW0_CPTS||Selectablesync event 25|
||SYNCEVENT_<br>OUT26|R5SS1_CORE<br>0_INTR138|R5SS1_CORE<br>0_VIM||Selectablesync event 26|
||SYNCEVENT_<br>OUT27|R5SS1_CORE<br>0_INTR139|R5SS1_CORE<br>0_VIM||Selectablesync event 27|
||SYNCEVENT_<br>OUT28|R5SS1_CORE<br>0_INTR140|R5SS1_CORE<br>0_VIM||Selectablesync event 28|
||SYNCEVENT_<br>OUT29|R5SS1_CORE<br>0_INTR141|R5SS1_CORE<br>0_VIM||Selectablesync event 29|
||SYNCEVENT_<br>OUT30|R5SS1_CORE<br>1_INTR138|R5SS1_CORE<br>1_VIM||Selectablesync event 30|
||SYNCEVENT_<br>OUT31|R5SS1_CORE<br>1_INTR139|R5SS1_CORE<br>1_VIM||Selectablesync event 31|
||SYNCEVENT_<br>OUT32|R5SS1_CORE<br>1_INTR140|R5SS1_CORE<br>1_VIM||Selectablesync event 32|
||SYNCEVENT_<br>OUT33|R5SS1_CORE<br>1_INTR141|R5SS1_CORE<br>1_VIM||Selectablesync event 33|



**Table 12-10. SOC_TIMESYNC_XBAR1 Time Sync Input Events** 

|**Module Instance**|**Module Sync Input**|**TimeSync Event Sources**|
|---|---|---|
|SOC_TIMESYNC_XBAR1|SYNCEVENT_IN[15:0]|SeeSOC_TIMESYNC_XBAR1 Event Maptable for time sync event<br>mapping.|



## _**12.2.3 Time Sync Routers Registers**_ 

## **12.2.3.1 SOC_TIMESYNC_XBAR0 Registers** 

**Table 12-11. SOC_TIMESYNC_XBAR0Instances** 

|**Instance**|**Instance**|**BaseAddress**|**BaseAddress**|
|---|---|---|---|
|SOC_TIMESYNC_XBAR0||52E00000h||
|**Table 12-12. SOC_TIMESYNC_XBAR0 Registers**||||
|**Offset**|**Acronym**|**Register Name**|**Physical Address**|
|0h|SOC_TIMESYNC_XBAR0_PID|Peripheral identification register|52E00000h|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1105 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

## **Table 12-12. SOC_TIMESYNC_XBAR0 Registers (continued)** 

|**Offset**|**Acronym**|**Register Name**|**Physical Address**|
|---|---|---|---|
|4h+ (_n_*0x4) where_n_goes from 0<br>-11|SOC_TIMESYNC_XBAR0_MUX<br>CNTL_y|Eventmux control register|52E00004h+ (_n_*0x4) where_n_<br>goes from 0 -11|



## **12.2.3.2 SOC_TIMESYNC_XBAR1 Registers** 

## **Table 12-13. SOC_TIMESYNC_XBAR1Instances** 

|**Instance**|**Base Address**|
|---|---|
|SOC_TIMESYNC_XBAR1|52E04000h|



## **Table 12-14. SOC_TIMESYNC_XBAR1Registers** 

|**Offset**|**Acronym**|**RegisterName**|**Physical Address**|
|---|---|---|---|
|0h|SOC_TIMESYNC_XBAR1_PID|Peripheral identification register|52E04000h|
|4h+ (_n_*0x4) where_n_goes from 0<br>-11|SOC_TIMESYNC_XBAR1_MUX<br>CNTL_y|Eventmux control register|52E04004h+ (_n_*0x4) where_n_<br>goes from 0 -33|



1106 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

## **12.3 Time Sync and Compare Events** 

## _**12.3.1 TimeSync Event Sources**_ 

## **12.3.1.1 SOC_TIMESYNC_XBAR0 Event Map** 

Table 12-15 shows the mapping of Events to the SOC_TIMESYNC_XBAR0. The router allows any of the inputs to be routed to the output. 

**Table 12-15. SOC_TIMESYNC_XBAR0 Events** 

|**Input Event**|**Event #**|**Event Name**|**Description**|**Type**|
|---|---|---|---|---|
|SYNCEVENT_IN0|0|CPSW0_CPTS_COMP|CPTS Compare Event|Pulse|
|SYNCEVENT_IN1|1|CPSW0_CPTS_GENF0|CPTS Generate Function 0|Pulse|
|SYNCEVENT_IN2|2|CPSW0_CPTS_GENF1|CPTS Generate Function 1|Pulse|
|SYNCEVENT_IN3|3|CPSW0_CPTS_SYNC|CPTS SYNC Event|Pulse|
|SYNCEVENT_IN4|4|ICSSM0_EDC_SYNC0|ICSSM0 IEP Sync Event0|Pulse|
|SYNCEVENT_IN5|5|ICSSM0_EDC_SYNC1|ICSSM0 IEP Sync Event1|Pulse|
|SYNCEVENT_IN6|6|ICSSM0_IEP_CMP_EVT0|ICSSM0 IEP Compare Event 0|Pulse|
|SYNCEVENT_IN7|7|ICSSM0_IEP_CMP_EVT1|ICSSM0 IEP Compare Event 1|Pulse|
|SYNCEVENT_IN8|8|ICSSM0_IEP_CMP_EVT2|ICSSM0 IEP Compare Event 2|Pulse|
|SYNCEVENT_IN9|9|ICSSM0_IEP_CMP_EVT3|ICSSM0 IEP Compare Event 3|Pulse|
|SYNCEVENT_IN10|10|ICSSM0_IEP_CMP_EVT4|ICSSM0 IEP Compare Event 4|Pulse|
|SYNCEVENT_IN11|11|ICSSM0_IEP_CMP_EVT5|ICSSM0 IEP Compare Event 5|Pulse|
|SYNCEVENT_IN12|12|ICSSM0_IEP_CMP_EVT6|ICSSM0 IEP Compare Event 6|Pulse|
|SYNCEVENT_IN13|13|ICSSM0_IEP_CMP_EVT7|ICSSM0 IEP Compare Event 7|Pulse|
|SYNCEVENT_IN14|14|ICSSM0_IEP_CMP_EVT8|ICSSM0 IEP Compare Event 8|Pulse|
|SYNCEVENT_IN15|15|ICSSM0_IEP_CMP_EVT9|ICSSM0 IEP Compare Event 9|Pulse|
|SYNCEVENT_IN16|16|ICSSM0_IEP_CMP_EVT10|ICSSM0 IEP Compare Event 10|Pulse|
|SYNCEVENT_IN17|17|ICSSM0_IEP_CMP_EVT11|ICSSM0 IEP Compare Event 11|Pulse|
|SYNCEVENT_IN18|18|ICSSM0_IEP_CMP_EVT12|ICSSM0 IEP Compare Event 12|Pulse|
|SYNCEVENT_IN19|19|ICSSM0_IEP_CMP_EVT13|ICSSM0 IEP Compare Event 13|Pulse|
|SYNCEVENT_IN20|20|ICSSM0_IEP_CMP_EVT14|ICSSM0 IEP Compare Event 14|Pulse|
|SYNCEVENT_IN21|21|ICSSM0_IEP_CMP_EVT15|ICSSM0 IEP Compare Event 15|Pulse|
|SYNCEVENT_IN22|22|GPIO_INTER_XBAR_OUT8|GPIOINTERRUPT8 from GPIOINTXBAR|Pulse|
|SYNCEVENT_IN23|23|GPIO_INTER_XBAR_OUT9|GPIOINTERRUPT9 from GPIOINTXBAR|Pulse|
|SYNCEVENT_IN24|24|GPIO_INTER_XBAR_OUT10|GPIOINTERRUPT10 from GPIOINTXBAR|Pulse|
|SYNCEVENT_IN25|25|GPIO_INTER_XBAR_OUT11|GPIOINTERRUPT11 from GPIOINTXBAR|Pulse|
|SYNCEVENT_IN26|26|GPIO_INTER_XBAR_OUT12|GPIOINTERRUPT12 from GPIOINTXBAR|Pulse|
|SYNCEVENT_IN27|27|GPIO_INTER_XBAR_OUT13|GPIOINTERRUPT13 from GPIOINTXBAR|Pulse|



## **12.3.1.2 SOC_TIMESYNC_XBAR1 Event Map** 

Table 12-16 shows the mapping of Events to the SOC_TIMESYNC_XBAR1. The router allows any of the inputs to be routed to the output. 

**Table 12-16. SOC_TIMESYNC_XBAR1 Events** 

|**Input Event**|**Event**<br>**Number**|**Event Name**|**Description**|**Type**|
|---|---|---|---|---|
|SYNCEVENT_IN0|0|CPSW0_CPTS_COMP|CPTS Compare Event|Pulse|
|SYNCEVENT_IN1|1|CPSW0_CPTS_GENF0|CPTS Generate Function 0|Pulse|
|SYNCEVENT_IN2|2|CPSW0_CPTS_GENF1|CPTS Generate Function 1|Pulse|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1107 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

**Table 12-16. SOC_TIMESYNC_XBAR1 Events (continued)** 

|**Input Event**|**Event**<br>**Number**|**Event Name**|**Description**|**Type**|
|---|---|---|---|---|
|SYNCEVENT_IN3|3|CPSW0_CPTS_SYNC|CPTS SYNC Event|Pulse|
|SYNCEVENT_IN4|4|ICSSM0_EDC_SYNC0|ICSSM0 IEP Sync Event0|Pulse|
|SYNCEVENT_IN5|5|ICSSM0_EDC_SYNC1|ICSSM0 IEP Sync Event1|Pulse|
|SYNCEVENT_IN6|6|CONTROLSS_PWMSYNCOU<br>T XBAR_OUT0|EPWMSYNCOUT0 from<br>PWMSYNCOUTXBAR|Pulse|
|SYNCEVENT_IN7|7|CONTROLSS_PWMSYNCOU<br>T XBAR_OUT1|EPWMSYNCOUT1 from<br>PWMSYNCOUTXBAR|Pulse|
|SYNCEVENT_IN8|8|CONTROLSS_PWMSYNCOU<br>T XBAR_OUT2|EPWMSYNCOUT2 from<br>PWMSYNCOUTXBAR|Pulse|
|SYNCEVENT_IN9|9|CONTROLSS_PWMSYNCOU<br>T XBAR_OUT3|EPWMSYNCOUT3 from<br>PWMSYNCOUTXBAR|Pulse|
|SYNCEVENT_IN10|10|GPIO_INTER_XBAR_OUT8|GPIOINTERRUPT8 from GPIOINTXBAR|Pulse|
|SYNCEVENT_IN11|11|GPIO_INTER_XBAR_OUT9|GPIOINTERRUPT9 from GPIOINTXBAR|Pulse|
|SYNCEVENT_IN12|12|GPIO_INTER_XBAR_OUT10|GPIOINTERRUPT10 from GPIOINTXBAR|Pulse|
|SYNCEVENT_IN13|13|GPIO_INTER_XBAR_OUT11|GPIOINTERRUPT11 from GPIOINTXBAR|Pulse|
|SYNCEVENT_IN14|14|GPIO_INTER_XBAR_OUT12|GPIOINTERRUPT12 from GPIOINTXBAR|Pulse|
|SYNCEVENT_IN15|15|GPIO_INTER_XBAR_OUT13|GPIOINTERRUPT13 from GPIOINTXBAR|Pulse|



## **12.3.1.3 PRU-ICSS Event Map** 

Table 12-17 shows the mapping of events to the PRU-ICSS Latch and Compare inputs. 

**Table 12-17. PRU-ICSS Event Map** 

|**Input Event**|**Event Name**|**Description**|**Type**|
|---|---|---|---|
|ICSSM0_EDC_LATCH0_I<br>N|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT10|Selectable sync event 10|Edge|
|ICSSM0_EDC_LATCH1_I<br>N|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT11|Selectable sync event 11|Edge|
|ICSSM0_IEP_CAP_INTR<br>0|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT12|Selectable sync event 12|Pulse|
|ICSSM0_IEP_CAP_INTR<br>1|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT13|Selectable sync event 13|Pulse|
|ICSSM0_IEP_CAP_INTR<br>2|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT14|Selectable sync event 14|Pulse|
|ICSSM0_IEP_CAP_INTR<br>3|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT15|Selectable sync event 15|Pulse|
|ICSSM0_IEP_CAP_INTR<br>4|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT16|Selectable sync event 16|Pulse|
|ICSSM0_IEP_CAP_INTR<br>5|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT17|Selectable sync event 17|Pulse|



## **12.3.1.4 CPSW0_CPTS Event Map** 

Table 12-18 shows the mapping of events to the CPSW0_CPTS Hardware push inputs. 

**Table 12-18. CPSW0_CPTS Event Map** 

|**Input Event**|**Event Name**|**Description**|**Type**|
|---|---|---|---|
|CPTS_HW1_TS_PUSH|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT18|Selectable sync event 18|Pulse|
|CPTS_HW2_TS_PUSH|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT19|Selectable sync event 19|Pulse|
|CPTS_HW3_TS_PUSH|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT20|Selectable sync event 20|Pulse|



1108 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Time Sync_ 

www.ti.com 

**Table 12-18. CPSW0_CPTS Event Map (continued)** 

|**Input Event**|**Event Name**|**Description**|**Type**|
|---|---|---|---|
|CPTS_HW4_TS_PUSH|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT21|Selectable sync event 21|Pulse|
|CPTS_HW5_TS_PUSH|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT22|Selectable sync event 22|Pulse|
|CPTS_HW6_TS_PUSH|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT23|Selectable sync event 23|Pulse|
|CPTS_HW7_TS_PUSH|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT24|Selectable sync event 24|Pulse|
|CPTS_HW8_TS_PUSH|SOC_TIMESYNC_XBAR1_SYNCEVENT_OUT25|Selectable sync event 25|Pulse|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1109 

Copyright © 2025 Texas Instruments Incorporated 

