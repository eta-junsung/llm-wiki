<!-- AM263P TRM | 4 Module Integration | 원본 p.76-177 | pymupdf4llm text+tables, images omitted -->

www.ti.com 

_Module Integration_ 

## _Chapter 4_ _**Module Integration**_ 

**==> picture [506 x 40] intentionally omitted <==**

This chapter describes the integration details for each module in the device, including information about clocks, resets, interrupts, DMA events and other hardware requests. 

## **Note** 

The reset signals MOD_G_RST and MOD_POR_RST are equivalent to the reset signals MOD_G_RST_N and MOD_POR_RST_N, respectively. 

**4.1 ADC Integration** .......................................................................................................................................................... 77 **4.2 Resolver to Digital Convertor Integration** ................................................................................................................ 80 **4.3 Resolver Integration** ...................................................................................................................................................80 **4.4 DAC Integration** .......................................................................................................................................................... 82 **4.5 eCAP Integration** .........................................................................................................................................................83 **4.6 EPWM Integration** .......................................................................................................................................................84 **4.7 EQEP Integration** ........................................................................................................................................................ 85 **4.8 FSI Integration** .............................................................................................................................................................86 **4.9 SDFM Integration** ........................................................................................................................................................87 **4.10 SOC_TIMESYNC_XBAR0 Integration** ......................................................................................................................89 **4.11 SOC_TIMESYNC_XBAR1 Integration** ......................................................................................................................91 **4.12 GPIO Integration** ....................................................................................................................................................... 94 **4.13 I2C Integration** .........................................................................................................................................................100 **4.14 SPI Integration** ........................................................................................................................................................ 103 **4.15 UART Integration** .................................................................................................................................................... 112 **4.16 CPSW93G Integration** .............................................................................................................................................118 **4.17 MMCSD Integration** .................................................................................................................................................121 **4.18 OSPI Integration** ......................................................................................................................................................123 **4.19 MCAN Integration** ................................................................................................................................................... 127 **4.20 LIN Integration** ........................................................................................................................................................ 143 **4.21 RTI Integration** ........................................................................................................................................................ 149 **4.22 WWDT Integration** ...................................................................................................................................................158 **4.23 DCC Integration** ...................................................................................................................................................... 163 **4.24 ESM Integration** ...................................................................................................................................................... 165 **4.25 ECC Aggregator Integration** .................................................................................................................................. 167 **4.26 MCRC Integration** ................................................................................................................................................... 169 **4.27 ICSSM_XBAR_INTROUTER Integration** ................................................................................................................171 **4.28 GPIO_XBAR Integration** .........................................................................................................................................175 

76 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.1 ADC Integration** 

There are 5x Analog-to-Digital Converter (ADC) modules integrated in the device. 

## **Note** 

## For each ADC[0:4]: 

- Analog input channels ADCIN[0:5] have dedicated pins. 

- Analog input channels ADCIN[6:7] are tied to shared ADC_CAL[0:1] pins, respectively. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

77 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**==> picture [680 x 375] intentionally omitted <==**

**Figure 4-1. ADC Integration Diagram - Simplified** 

78 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**==> picture [680 x 290] intentionally omitted <==**

**Figure 4-2. ADC Integration Diagram - Detailed** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

79 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **4.2 Resolver to Digital Convertor Integration** 

There are 2x Resolver-to-Digital Converter (RDC) modules integrated in the device as shown in Figure 4-3. 

## **Note** 

## For each RDC Module: 

- Resolver Module input channels have ADC_R0_AIN[3:0] and ADC_R1_AIN[3:0] dedicated pins. 

- ADC_VREFLO_G3 and ADC_VREFHI_G3 are dedicated voltage reference pins for Resolver modules. 

- Refer to Figure 7-139 for full list of all RDC pins. 

**==> picture [500 x 170] intentionally omitted <==**

**----- Start of picture text -----**<br>
Resolver to Digital Convertor Sub-System ANACIO –<br>Analog<br>ADC R0 Communications<br>Input Output<br>Signal Processing – RDC0<br>ControlADC RESADC0.[#1]<br>+ resolver_adc0_mux_en<br>Sequencer<br>PinmuxGPIO/ GPO_PWM[1:0] Excitation signal Signal Processing – RDC1 RESADC1.[#1]<br>ADC R1<br>resolver_adc1_mux_en<br>CFG data<br>PWM MMRs MMRs<br>Sync FE<br>Out PWMSyncOutXBar.Out[2]<br>XBar<br>VBUSP 4.0 32-bit data peripheral<br>[#2]<br>**----- End of picture text -----**<br>


**Figure 4-3. RDC Integration Diagram** 

## **4.3 Resolver Integration** 

There are 1x Resolver with up to 2x motor position sensing modules integrated in the device. Motor position sensing utilizes two dedicated SAR ADC's. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

80 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **Note** 

## For each Resolver 

- Resolver ADC's support 12 bit/14 bit 

- Can be used for General Purpose if required 

**Figure 4-4. Resolver Integration Diagram** 

**==> picture [500 x 213] intentionally omitted <==**

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

81 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **4.4 DAC Integration** 

There is 1x DAC module integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [379 x 342] intentionally omitted <==**

**----- Start of picture text -----**<br>
External<br>VREFHI<br>0<br>Internal<br>VDDA<br>1<br>DACVAL 12-bit<br>DACREFSEL Amp +  DACOUT<br>12 DAC Buffer<br>VSSA<br>8 bit offset<br>correction<br>code<br>SYSRSN<br>DACIN - DACVAL<br>+<br>12 12 12<br>SYSCLK<br>CLRZ<br>**----- End of picture text -----**<br>


**Figure 4-5. DAC Integration Diagram** 

82 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.5 eCAP Integration** 

There are 16x eCAP modules integrated in the device. _eCAP Integration Diagram_ provides a visual representation of the device integration details. 

**==> picture [453 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
MUNIT_ENABLE<br>CAP_INT<br>SYS_CLK<br>DMA_INT<br>RSTN<br>PWM_OUT<br>See eCAP Input SelectionCAP_IN[255:0] ECAP<br>SOC_EVT<br>SYNC_IN[127:0] All EPWM SYNCOUT signals and<br>From Input XBARs<br>SYNC_OUT<br>TRIP_IN[127:0] from PWM_XBARs and EPWM_TRIPOUT<br>TRIP_OUT<br>GLDSTRB[127:0] All EPWM GLDSTRB signals<br>**----- End of picture text -----**<br>


**Figure 4-6. eCAP Integration** 

- MUNIT_Enable: This bit is used to enable/disable the signal monitoring block. 

- RSTN: This bit is used to reset the eCAP module. 

- SYS_CLK: Its 200MHz system clock which is functional clock for ECAP. 

- CAP_IN: Capture inputs can be connected using the INPUTXBAR, PWMXBAR, adc_evt, etc. (Table 7-170). 

   - 256:1 input multiplexer is used to select the capture input. 

- SYNC_IN: eCAP modules can be synchronized with each other by selecting a common SYNCIN source. SYNCIN source for eCAP can be either software sync-in or external sync-in. 

- TRIP_IN: The signal monitoring block can be disabled from monitoring the signal by external trip signals. It is re-enabled by removing the trip-in signal. 

- GLDSTRB: This signal is used to load shadow values to MIN/MAX reg while signal monitoring. 

- CAP_INT: Interrupt signal generated as a part of capture/PWM event. 

- DMA_INT: DMA request signal. 

- PWM_OUT: PWM output in APWM mode. 

- SOC_EVT: Used to generate SOC signal for ADC during any capture/PWM event. 

- SYNC_OUT: This can be used to synchronize the eCAP with other eCAPs or with other modules like PWM. 

- TRIP_OUT: Trip signal is generated upon signal monitoring error. All the signal monitoring error events are OR-ed and provided as trip out. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

83 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **4.6 EPWM Integration** 

There are 32x EPWM modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**Figure 4-7. ePWM Integration Diagram** 

**==> picture [500 x 303] intentionally omitted <==**

84 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.7 EQEP Integration** 

There are 3x EQEP modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [590 x 515] intentionally omitted <==**

**Figure 4-8. EQEP Integration Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

85 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **4.8 FSI Integration** 

There are 4x FSI modules integrated in the CONTROLSS. The diagram below provides a visual representation of the device integration details. 

**==> picture [619 x 380] intentionally omitted <==**

**----- Start of picture text -----**<br>
FSI1/2/3/4-TXFSI1/2/3/4-TXFSI1/2/3/4-TXFSITX0/1/2/3<br>Main CPU 400MHz Clock PLLRAWCLK<br>Control System Peripheral Clock SYSCLK TXCLK<br>TXD0<br>System Reset SYSRSN TXD1<br>Output<br>XBars OutputXBar.Out[15:0]<br>TX_INT1N<br>GPO[19:16] Port0 INT<br>ICSS XBars<br>GPO[19:16] Port1 EXTTRIG[63:0] TX_INT2N<br>&<br>All EPWM All SOCB Outputs (32 off) PINGTRIG[63:0] TX_DMA_EVT XBarsDMA<br>R5_0 TXCLK_RX_DLY_INTXD0_RX_DLY_IN<br>TXD1_RX_DLY_IN<br>R5_1 VBUS Port SEL_TDM_PATH<br>VBUSP GPIO<br>Bridge Mux<br>R5_2<br>(arbitrated, DMA<br>only one access to FSIx-TX All ECAP INPUTMux XBars<br>R5_3<br>allowed on any<br>TC_0 cycle) FSI1/2/3/4-RXFSI1/2/3/4-RXFSI1/2/3/4-RXFSIRX0/1/2/3<br>Control System Peripheral Clock SYSCLK RX_WIDE_PULSE_0<br>TC_1 All EPWM SYNCINMux System Resetnc SYSRSNERROR_PKT_RCVD RXCLK_DLY_OUTRXD1_DLY_OUTRXD0_DLY_OUT<br>nc PING_PKT_RCVD<br>nc DATA_PKT_RCVD<br>nc PKT_TAG[3:0] RX_INT_LB_CLK<br>RX_INT_LB_D0<br>RX_INT_LB_D1<br>nc FRAME_DONE<br>PING_FRAME_TAG_MATCH TXCLK<br>R5_0 PWM ERROR_FRAME_TAG_MATCHDATA_FRAME_TAG_MATCHRX_TRIG[3:0] TXD0TXD1<br>XBars<br>R5_1 nc RX_MSR_LINE<br>VBUSP ncnc RX_MSR_LINE_RISERX_MSR_LINE_FALL RX_INT1N INT<br>Bridge XBars<br>R5_2 (arbitrated, RX_INT2N<br>only one access to<br>R5_3 FSIx-RX VBUS Port RX_DMA_EVT XBarsDMA<br>allowed on any<br>cycle)<br>TC_0<br>TC_1<br>**----- End of picture text -----**<br>


**Figure 4-9. FSI Integration Diagram** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

86 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.9 SDFM Integration** 

There are 2x SDFM modules integrated in the CONTROLSS. The diagrams and table below provides a visual representation of the device integration details. 

**==> picture [419 x 262] intentionally omitted <==**

**----- Start of picture text -----**<br>
SDyFLTxDRINT<br>SOCA/B<br>SDyERR<br>SDyFLTxDRINT<br>SDFM<br>SDyFLTxCMPH<br>SDyFLTxCMPL<br>SDyFLTxCMPHZ<br>GLOBAL_CTRL<br>SDFM1_CLK0_SEL<br>SDy-D[0:3] SDy-CLK[1:3] SD0_CLK0 SD1_CLK0<br>GPIO/PINMUX<br>EPWMy INT  XBAR<br>DMA  XBAR<br>R5FSS<br>ECAP,<br>Registers<br>OUTPUTXBAR  & PWMXBAR<br>**----- End of picture text -----**<br>


**Figure 4-10. SDFM Integration Diagram (Simple)** 

**==> picture [500 x 256] intentionally omitted <==**

**Figure 4-11. SDFM Integration Diagram (Detailed)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

87 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

88 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.10 SOC_TIMESYNC_XBAR0 Integration** 

**==> picture [282 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
SoC TIMESYNC<br>xBAR0<br>MMR<br>Configuration<br>Port<br>MSS  SYSCLK<br>RCM SYSRSTn<br>Time Sync<br>Sources SYNCEVENT_IN[27:0]<br>Time Sync<br>SYNCEVENT_OUT[19:0]<br>Sink<br>INFRA-0<br>Interconnect<br>**----- End of picture text -----**<br>


**Figure 4-12. SOC_TIMESYNC_XBAR0 Integration** 

**Table 4-1. SOC_TIMESYNC_XBAR0 Device Integration** 

|**Module Instance**|**Module Instance**|**Device Allocation**|**Device Allocation**|**Device Allocation**|**SoC Interconnect**|**SoC Interconnect**|**SoC Interconnect**|
|---|---|---|---|---|---|---|---|
|SOC_TIMESYNC_XBAR0||✔|||VBUSP INFRA0 Interconnect|||
|**Table 4-2. SOC_TIMESYNC_XBAR0 Clocks**||||||||
|**Module**<br>**Instance**|**Module Clock Input**||**Source Clock Signal**|**Source**||**Default**<br>**Freq**|**Description**|
|SOC_TIMES<br>YNC_XBAR<br>0|CLK||SYSCLK|MSS_RCM||200 MHz|SOC_TIMESYNC_XBAR0<br>Functional and Interface<br>clock|



## **Table 4-3. SOC_TIMESYNC_XBAR0 Resets** 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|SOC_TIME<br>SYNC_XBA<br>R0|RST|SYS_RST|RCM + Warm Reset Sources|SOC_TIMESYNC_XBAR0 Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

89 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-4. SOC_TIMESYNC_XBAR0 Time Sync Output Events** 

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



90 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.11 SOC_TIMESYNC_XBAR1 Integration** 

**==> picture [280 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
SoC TIMESYNC<br>xBAR1<br>MMR<br>Configuration<br>Port<br>MSS  SYSCLK<br>RCM SYSRSTn<br>Time Sync<br>Sources SYNCEVENT_IN[15:0]<br>Time Sync<br>SYNCEVENT_OUT[33:0]<br>Sink<br>INFRA-0<br>Interconnect<br>**----- End of picture text -----**<br>


**Figure 4-13. SOC_TIMESYNC_XBAR1 Integration** 

**Table 4-5. SOC_TIMESYNC_XBAR1 Device Integration** 

|**Module Instance**|**Device Allocation**|**Device Allocation**|**Device Allocation**|**Device Allocation**|**SoC Interconnect**|**SoC Interconnect**|**SoC Interconnect**|
|---|---|---|---|---|---|---|---|
|SOC_TIMESYNC_XBAR1|✔||||VBUSP INFRA Interconnect|||
|**Table 4-6. SOC_TIMESYNC_XBAR1 Clocks**||||||||
|**Module Instance**||**Module Clock**<br>**Input**|**Source Clock**<br>**Signal**|**Source**||**Default**<br>**Freq**|**Description**|
|SOC_TIMESYNC_XBAR1||CLK|SYSCLK|MSS_RCM||200 MHz|SOC_TIMESYNC_XBAR1 Functional<br>and Interface clock|



## **Table 4-7. SOC_TIMESYNC_XBAR1 Resets** 

|**Module Instance**|**Module**<br>**Reset**<br>**Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|SOC_TIMESYNC_XB<br>AR1|RST|SYS_RST|RCM + Warm Reset Sources|SOC_TIMESYNC_XBAR1 Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

91 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-8. SOC_TIMESYNC_XBAR1 Time Sync Output Events** 

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
||SYNCEVENT_<br>OUT10|ICSS0_EDC_L<br>ATCH0_IN|PRU_ICSS0||Selectablesync event 10|
||SYNCEVENT_<br>OUT11|ICSS0_EDC_L<br>ATCH1_IN|PRU_ICSS0||Selectablesync event 11|
||SYNCEVENT_<br>OUT12|ICSS0_IEP_CA<br>P_INT R0|PRU_ICSS0||Selectablesync event 12|
||SYNCEVENT_<br>OUT13|ICSS0_IEP_CA<br>P_INT R1|PRU_ICSS0||Selectablesync event 13|
||SYNCEVENT_<br>OUT14|ICSS0_IEP_CA<br>P_INT R2|PRU_ICSS0||Selectablesync event 14|
||SYNCEVENT_<br>OUT15|ICSS0_IEP_CA<br>P_INT R3|PRU_ICSS0||Selectablesync event 15|
||SYNCEVENT_<br>OUT16|ICSS0_IEP_CA<br>P_INT R4|PRU_ICSS0||Selectablesync event 16|



92 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-8. SOC_TIMESYNC_XBAR1 Time Sync Output Events (continued)** 

|**Module Instance**|**Module Sync**<br>**Output**|**Destination**<br>**Sync Signal**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SOC_TIMESYNC_XBA<br>R1|SYNCEVENT_<br>OUT17|ICSS0_IEP_CA<br>P_INT R5|PRU_ICSS0|Edge|Selectablesync event 17|
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



**Table 4-9. SOC_TIMESYNC_XBAR1 Time Sync Input Events** 

|**Module Instance**|**Module Sync Input**|**TimeSync Event Sources**|
|---|---|---|
|SOC_TIMESYNC_XBAR1|SYNCEVENT_IN[15:0]|SeeSOC_TIMESYNC_XBAR1 Event Maptable for time sync event<br>mapping.|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

93 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **4.12 GPIO Integration** 

There are 4x GPIO modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

## **Note** 

There is a designated GPIO module per R5FSS core. Each R5FSS core has access to all GPI signals at all times. The GPO signals are assigned to a specific R5FSS core by configuring the MSS_IOMUX. _PAD_ _CFG_REG.GPIO_SEL[17:16] of the associated IOMUX Pad Configuration register. 

94 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**==> picture [488 x 247] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>GPIO<br>GPIO#_OUTEN<br>SYS_CLK GPIO#_CLK ENB<br>GPIO#_OUT<br>GPIO#_IN<br>RCM GPIO#_BANK_INTR[8:0]<br>GPIO#_RST_CTRL Bit<br>GPIO#_WARMRESET R5FSS0-CORE0<br>Warm Reset Sources<br>GPIO#_INTR[143:0]<br>R5FSS0-CORE1<br>R5FSS1-CORE0<br>PERI VBUSP Interconnect<br>R5FSS1-CORE1<br>GPIO_XBAR<br>**----- End of picture text -----**<br>


**Figure 4-14. GPIO Integration Diagram** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

95 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

This diagram describes the GPIO multiplexor connectivity. 

**==> picture [680 x 280] intentionally omitted <==**

**Figure 4-15. GPIO Mux Diagram** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

96 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## The tables below summarize the device integration details for the GPIO. 

**Table 4-10.** _**GPIO**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|GPIO0|✔|PERI VBUSP Interconnect|
|GPIO1|✔|PERI VBUSP Interconnect|
|GPIO2|✔|PERI VBUSP Interconnect|
|GPIO3|✔|PERI VBUSP Interconnect|



## **Table 4-11.** _**GPIO**_ **Clocks** 

## This table describes the module clocking signals. 

|**Module Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default Freq**|**Description**|
|---|---|---|---|---|---|
|GPIO0|GPIO0_VBUS_FICLK|SYS_CLK|PLL_CORE_CLK:HSDIV0_CLKOUT<br>0|200 MHz|GPIO0 Functional and Interface<br>Clock|
|GPIO1|GPIO1_VBUS_FICLK|SYS_CLK|PLL_CORE_CLK:HSDIV0_CLKOUT<br>0|200 MHz|GPIO1 Functional and Interface<br>Clock|
|GPIO2|GPIO2_VBUS_FICLK|SYS_CLK|PLL_CORE_CLK:HSDIV0_CLKOUT<br>0|200 MHz|GPIO2 Functional and Interface<br>Clock|
|GPIO3|GPIO3_VBUS_FICLK|SYS_CLK|PLL_CORE_CLK:HSDIV0_CLKOUT<br>0|200 MHz|GPIO3 Functional and Interface<br>Clock|



## **Table 4-12.** _**GPIO**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|GPIO0|GPIO0_RST|Warm Reset (MOD_G_RST)|RCM + Warm Reset Source|GPIO0 Reset|
|GPIO1|GPIO1_RST|Warm Reset (MOD_G_RST)|RCM + Warm Reset Source|GPIO1 Reset|
|GPIO2|GPIO2_RST|Warm Reset (MOD_G_RST)|RCM + Warm Reset Source|GPIO2 Reset|
|GPIO3|GPIO3_RST|Warm Reset (MOD_G_RST)|RCM + Warm Reset Source|GPIO3 Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 97 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **Table 4-13.** _**GPIO**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

## **Note** 

## Where GPIO# = GPIO[0:3] 

|**Module Instance**|**Module Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|GPIO#|GPIO#_[0:138]|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO#_[0:137] interrupt request|
|GPIO#|GPIO#_BANK0_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK0 interrupt request|
|GPIO#|GPIO#_BANK1_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK1 interrupt request|
|GPIO#|GPIO#_BANK2_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK2 interrupt request|
|GPIO#|GPIO#_BANK3_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK3 interrupt request|
|GPIO#|GPIO#_BANK4_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK4 interrupt request|
|GPIO#|GPIO#_BANK5_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK5 interrupt request|
|GPIO#|GPIO#_BANK6_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK6 interrupt request|
|GPIO#|GPIO#_BANK7_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK7 interrupt request|
|GPIO#|GPIO#_BANK8_INT|Programmable via GPIO_XBAR_INTR0|GPIO_XBAR_INTR0|Pulse|GPIO# BANK8 interrupt request|



## **Table 4-14.** _**GPIO**_ **DMA Requests** 

## This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|GPIO#|N/A|N/A|N/A|N/A|The GPIO module does not support DMA<br>requests.|



## **Table 4-15.** _**GPIO**_ **Capture Event Inputs** 

This table describes the module capture event inputs. 

|**Module**<br>**Instance**|**Module Capture Event Input**|**Capture Event Source Signal**|**Source**|**Type**|**Description**|
|---|---|---|---|---|---|
|GPIO#|N/A|N/A|N/A|N/A|The GPIO module does not support Capture<br>Event Inputs|



98 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 99 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **4.13 I2C Integration** 

There are 4x I2C module integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [500 x 297] intentionally omitted <==**

**Figure 4-16. I2C Integration** 

The tables below summarize the device integration details of I2C# (where # = 0, 1, 2, 3). 

**Table 4-16.** _**I2C**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|I2C0|✓|PERI VBUSP Interconnect|
|I2C1|✓|PERI VBUSP Interconnect|
|I2C2|✓|PERI VBUSP Interconnect|
|I2C3|✓|PERI VBUSP Interconnect|



100 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-17.** _**I2C**_ **Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|I2C[0:3]|I2C[0:3]_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|I2C[0:3] VBUS Clock|
||I2C[0:3]_FCLK<br>(I2C_CLK)|XTALCLK|External XTAL|25 MHz|I2C[0:3] Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



**Table 4-18.** _**I2C**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|I2C0|I2C0_RST(VBUSP_RST<br>n)|Warm Reset<br>(SYS_NPRST)|RCM + Warm Reset Sources|I2C0 Asynchronous Reset|
|I2C1|I2C1_RST|Warm Reset<br>(SYS_NPRST)|RCM + Warm Reset Sources|I2C1 Asynchronous Reset|
|I2C2|I2C2_RST|Warm Reset<br>(SYS_NPRST)|RCM + Warm Reset Sources|I2C2 Asynchronous Reset|
|I2C3|I2C3_RST|Warm Reset<br>(SYS_NPRST)|RCM + Warm Reset Sources|I2C3 Asynchronous Reset|



**Table 4-19.** _**I2C**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|I2C0|i2c0_int_req<br>|i2c0_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Pulse|I2C0 Status Event Interrupt|
|I2C1|i2c1_int_req<br>|i2c1_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Pulse|I2C1 Status Event Interrupt|
|I2C2|i2c2_int_req<br>|i2c2_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Pulse|I2C2 Status Event Interrupt|
|I2C3|i2c3_int_req<br>|i2c3_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Pulse|I2C3 Status Event Interrupt|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 101 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-20.** _**I2C**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|I2C0|I2C0_TX|i2c0_dma_req_tx|EDMA Crossbar<br>(EDMA_XBAR)|Pulse|I2C0 DMA Transmit Request|
||I2C0_RX|i2c0_dma_req_rx|||I2C0 DMA Receive Request|
|I2C1|I2C1_TX|i2c1_dma_req_tx|EDMA Crossbar<br>(EDMA_XBAR)|Pulse|I2C1 DMA Transmit Request|
||I2C1_RX|i2c1_dma_req_rx|||I2C1 DMA Receive Request|
|IC2|I2C2_TX|i2c2_dma_req_tx|EDMA Crossbar<br>(EDMA_XBAR)|Pulse|I2C2 DMA Transmit Request|
||I2C2_RX|i2c2_dma_req_rx|||I2C2 DMA Receive Request|
|I2C3|I2C3_TX|i2c3_dma_req_tx|EDMA Crossbar<br>(EDMA_XBAR)|Pulse|I2C3 DMA Transmit Request|
||I2C3_RX|i2c3_dma_req_rx|||I2C3 DMA Receive Request|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

102 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.14 SPI Integration** 

There are 8x SPI modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [500 x 344] intentionally omitted <==**

**Figure 4-17. SPI Integration** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 103 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

The tables below summarize the device integration details of SPI# (where # = 0 to 7). 

**Table 4-21.** _**SPI**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|SPI0|✓|PERI VBUSP Interconnect|
|SPI1|✓|PERI VBUSP Interconnect|
|SPI2|✓|PERI VBUSP Interconnect|
|SPI3|✓|PERI VBUSP Interconnect|
|SPI4|✓|PERI VBUSP Interconnect|
|SPI5|✓|PERI VBUSP Interconnect|
|SPI6|✓|PERI VBUSP Interconnect|
|SPI7|✓|PERI VBUSP Interconnect|



**Table 4-22.** _**SPI**_ **Clocks** 

## This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|SPI0|SPI0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI0 VBUS Clock|
||SPI0_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI0 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



104 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-22.** _**SPI**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|SPI1|SPI1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI1 VBUS Clock|
||SPI1_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI1 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|SPI2|SPI2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI2 VBUS Clock|
||SPI2_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI2 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

105 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-22.** _**SPI**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|SPI3|SPI3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI3 VBUS Clock|
||SPI3_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI3 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|SPI4|SPI4_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI4 VBUS Clock|
||SPI4_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI4 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



106 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-22.** _**SPI**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|SPI5|SPI5_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI5 VBUS Clock|
||SPI5_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI5 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|SPI6|SPI6_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI6 VBUS Clock|
||SPI6_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI6 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

107 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-22.** _**SPI**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|SPI7|SPI7_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|SPI7 VBUS Clock|
||SPI7_FCLK (SPI_CLK)|XTALCLK|External XTAL|25 MHz|SPI7 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||



**Table 4-23.** _**SPI**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|SPI0|SPI0_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|SPI0 Asynchronous Reset|
|SPI1|SPI1_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|SPI1 Asynchronous Reset|
|SPI2|SPI2_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|SPI2 Asynchronous Reset|
|SPI3|SPI3_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|SPI3 Asynchronous Reset|
|SPI4|SPI4_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|SPI4 Asynchronous Reset|
|SPI5|SPI5_RST|Warm Reset<br>(MOD_G_RST)|RCM+ Warm Reset Sources|SPI5 Asynchronous Reset|
|SPI6|SPI6_RST|Warm Reset<br>(MOD_G_RST)|RCM+ Warm Reset Sources|SPI6 Asynchronous Reset|
|SPI7|SPI7_RST|Warm Reset<br>(MOD_G_RST)|RCM+ Warm Reset Sources|SPI7 Asynchronous Reset|



**Table 4-24.** _**SPI**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SPI0|spi0_int_req|spi0_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI0 IP Status Information|



108 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-24.** _**SPI**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SPI1|spi1_int_req|spi1_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI1 IP Status Information|
|SPI2|spi2_int_req|spi2_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI2 IP Status Information|
|SPI3|spi3_int_req|spi3_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI3 IP Status Information|
|SPI4|spi4_int_req|spi4_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI4 IP Status Information|
|SPI5|spi5_int_req|spi5_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI5 IP Status Information|
|SPI6|spi6_int_req|spi6_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI6 IP Status Information|
|SPI7|spi7_int_req|spi7_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|SPI7 IP Status Information|



**Table 4-25.** _**SPI**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SPI0|SPI0_DMA_READ_0|spi0_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI0 DMA Read Request|
||SPI0_DMA_READ_1|spi0_dma_read_req[1]||||
||SPI0_DMA_READ_2|spi0_dma_read_req[2]||||
||SPI0_DMA_READ_3|spi0_dma_read_req[3]||||
||SPI0_DMA_WRITE_0|spi0_dma_write_req[0]|||SPI0 DMA Write Request|
||SPI0_DMA_WRITE_1|spi0_dma_write_req[1]||||
||SPI0_DMA_WRITE_2|spi0_dma_write_req[2]||||
||SPI0_DMA_WRITE_3|spi0_dma_write_req[3]||||
|SPI1|SPI1_DMA_READ_0|spi1_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI1 DMA Read Request|
||SPI1_DMA_READ_1|spi1_dma_read_req[1]||||
||SPI1_DMA_READ_2|spi1_dma_read_req[2]||||
||SPI1_DMA_READ_3|spi1_dma_read_req[3]||||
||SPI1_DMA_WRITE_0|spi1_dma_write_req[0]|||SPI1 DMA Write Request|
||SPI1_DMA_WRITE_1|spi1_dma_write_req[1]||||
||SPI1_DMA_WRITE_2|spi1_dma_write_req[2]||||
||SPI1_DMA_WRITE_3|spi1_dma_write_req[3]||||
|SPI2|SPI2_DMA_READ_0|spi2_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI2 DMA Read Request|
||SPI2_DMA_READ_1|spi2_dma_read_req[1]||||
||SPI2_DMA_READ_2|spi2_dma_read_req[2]||||
||SPI2_DMA_READ_3|spi2_dma_read_req[3]||||
||SPI2_DMA_WRITE_0|spi2_dma_write_req[0]|||SPI2 DMA Write Request|
||SPI2_DMA_WRITE_1|spi2_dma_write_req[1]||||
||SPI2_DMA_WRITE_2|spi2_dma_write_req[2]||||
||SPI2_DMA_WRITE_3|spi2_dma_write_req[3]||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 109 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-25.** _**SPI**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SPI3|SPI3_DMA_READ_0|spi3_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI3 DMA Read Request|
||SPI3_DMA_READ_1|spi3_dma_read_req[1]||||
||SPI3_DMA_READ_2|spi3_dma_read_req[2]||||
||SPI3_DMA_READ_3|spi3_dma_read_req[3]||||
||SPI3_DMA_WRITE_0|spi3_dma_write_req[0]|||SPI3 DMA Write Request|
||SPI3_DMA_WRITE_1|spi3_dma_write_req[1]||||
||SPI3_DMA_WRITE_2|spi3_dma_write_req[2]||||
||SPI3_DMA_WRITE_3|spi3_dma_write_req[3]||||
|SPI4|SPI4_DMA_READ_0|spi4_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI4 DMA Read Request|
||SPI4_DMA_READ_1|spi4_dma_read_req[1]||||
||SPI4_DMA_READ_2|spi4_dma_read_req[2]||||
||SPI4_DMA_READ_3|spi4_dma_read_req[3]||||
||SPI4_DMA_WRITE_0|spi4_dma_write_req[0]|||SPI4 DMA Write Request|
||SPI4_DMA_WRITE_1|spi4_dma_write_req[1]||||
||SPI4_DMA_WRITE_2|spi4_dma_write_req[2]||||
||SPI4_DMA_WRITE_3|spi4_dma_write_req[3]||||
|SPI5|SPI5_DMA_READ_0|spi5_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI5 DMA Read Request|
||SPI5_DMA_READ_1|spi5_dma_read_req[1]||||
||SPI5_DMA_READ_2|spi5_dma_read_req[2]||||
||SPI5_DMA_READ_3|spi5_dma_read_req[3]||||
||SPI5_DMA_WRITE_0|spi5_dma_write_req[0]|||SPI5 DMA Write Request|
||SPI5_DMA_WRITE_1|spi5_dma_write_req[1]||||
||SPI5_DMA_WRITE_2|spi5_dma_write_req[2]||||
||SPI5_DMA_WRITE_3|spi5_dma_write_req[3]||||
|SPI6|SPI6_DMA_READ_0|spi6_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI6 DMA Read Request|
||SPI6_DMA_READ_1|spi6_dma_read_req[1]||||
||SPI6_DMA_READ_2|spi6_dma_read_req[2]||||
||SPI6_DMA_READ_3|spi6_dma_read_req[3]||||
||SPI6_DMA_WRITE_0|spi6_dma_write_req[0]|||SPI6 DMA Write Request|
||SPI6_DMA_WRITE_1|spi6_dma_write_req[1]||||
||SPI6_DMA_WRITE_2|spi6_dma_write_req[2]||||
||SPI6_DMA_WRITE_3|spi6_dma_write_req[3]||||



110 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-25.** _**SPI**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|SPI7|SPI7_DMA_READ_0|spi7_dma_read_req[0]|EDMA Crossbar<br>(EDMA_XBAR)|Level|SPI7 DMA Read Request|
||SPI7_DMA_READ_1|spi7_dma_read_req[1]||||
||SPI7_DMA_READ_2|spi7_dma_read_req[2]||||
||SPI7_DMA_READ_3|spi7_dma_read_req[3]||||
||SPI7_DMA_WRITE_0|spi7_dma_write_req[0]|||SPI7 DMA Write Request|
||SPI7_DMA_WRITE_1|spi7_dma_write_req[1]||||
||SPI7_DMA_WRITE_2|spi7_dma_write_req[2]||||
||SPI7_DMA_WRITE_3|spi7_dma_write_req[3]||||



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 111 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **4.15 UART Integration** 

There are 6x UART modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [500 x 351] intentionally omitted <==**

**==> picture [63 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
# = 0, 1, 2, 3, 4, 5<br>**----- End of picture text -----**<br>


**Figure 4-18. UART Integration** 

The tables below summarize the device integration details of UART# (where # = 0, 1, 2, 3, 4, 5) in the device. 

**Table 4-26.** _**UART**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|UART0|✓|PERI VBUSP Interconnect|
|UART1|✓|PERI VBUSP Interconnect|
|UART2|✓|PERI VBUSP Interconnect|
|UART3|✓|PERI VBUSP Interconnect|
|UART4|✓|PERI VBUSP Interconnect|
|UART5|✓|PERI VBUSP Interconnect|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

112 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-27.** _**UART**_ **Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|UART0|UART0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART0 VBUS Clock|
||UART0_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART0 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||
|UART1|UART1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART1 VBUS Clock|
||UART1_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART1 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

113 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-27.** _**UART**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|UART2|UART2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART2 VBUS Clock|
||UART2_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART2 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||
|UART3|UART3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART3 VBUS Clock|
||UART3_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART3 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



114 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-27.** _**UART**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|UART4|UART4_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART4 VBUS Clock|
||UART4_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART4 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||
|UART5|UART5_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|UART5 VBUS Clock|
||UART5_FCLK<br>(UART_CLK)|XTALCLK|External XTAL|25 MHz|UART5 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



**Table 4-28.** _**UART**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|UART0|UART0_RST(VBUSP_R<br>STn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART0 Asynchronous Reset|
|UART1|UART1_RST(VBUSP_R<br>STn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART1 Asynchronous Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 115 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-28.** _**UART**_ **Resets (continued)** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|UART2|UART2_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART2 Asynchronous Reset|
|UART3|UART3_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART3 Asynchronous Reset|
|UART4|UART4_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART4 Asynchronous Reset|
|UART5|UART5_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|UART5 Asynchronous Reset|



**Table 4-29.** _**UART**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|UART0|uart0_int_req|uart0_int_req|ALL R5FSS Cores<br>PRU-ICSS Core|Level|UART0 IP Status Information|
|UART1|uart1_int_req|uart1_int_req|ALL R5FSS Cores<br>PRU-ICSS Core||UART1 IP Status Information|
|UART2|uart2_int_req|uart2_int_req|ALL R5FSS Cores<br>PRU-ICSS Core||UART2 IP Status Information|
|UART3|uart3_int_req|uart4_int_req|ALL R5FSS Cores<br>PRU-ICSS Core||UART3 IP Status Information|
|UART4|uart4_int_req|uart4_int_req|ALL R5FSS Cores<br>PRU-ICSS Core||UART4 IP Status Information|
|UART5|uart5_int_req|uart5_int_req|ALL R5FSS Cores<br>PRU-ICSS Core||UART5 IP Status Information|



**Table 4-30.** _**UART**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|UART0|UART0_DMA_0|UART0_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)|Level|UART0 DMA Request|
||UART0_DMA_1|UART0_dma_req[1]||||
|UART1|UART1_DMA_0|UART1_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)||UART1 DMA Request|
||UART1_DMA_1|UART1_dma_req[1]||||
|UART2|UART2_DMA_0|UART2_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)||UART2 DMA Request|
||UART2_DMA_1|UART2_dma_req[1]||||
|UART3|UART3_DMA_0|UART3_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)||UART3 DMA Request|
||UART3_DMA_1|UART3_dma_req[1]||||
|UART4|UART4_DMA_0|UART4_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)||UART4 DMA Request|
||UART4_DMA_1|UART4_dma_req[1]||||
|UART5|UART5_DMA_0|UART5_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)||UART5 DMA Request|
||UART5_DMA_1|UART5_dma_req[1]||||



116 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 117 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **4.16 CPSW93G Integration** 

There is 1x CPSW3G module integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [395 x 297] intentionally omitted <==**

**----- Start of picture text -----**<br>
DEVICE CPSW<br>ICSSM CORE<br>C0_FH_PULSE_INTR_[0:3]C0_TH_PULSE_INTR_[0:3] R5FSS0-CORE0<br>C0_THRESH_PEND_INTR_[0:3]C0_MISC_PEND_INTR_[0:3] R5FSS0-CORE1<br>CPSW_STAT_PENDCPSW_HOST_PEND R5FSS1-CORE0<br>R5FSS1-CORE1<br>ESM0<br>ESM0_LVL_IN_45 CPSW0_ECC_SEC_PEND_0<br>ESM0_LVL_IN_46 CPSW0_ECC_DED_PEND_0<br>SoC CPTS<br>Time Sync XBAR CPSW_CPTS_COMP_0<br>CPSW_CPTS_GENF0_0<br>CPSW_CPTS_GENF1_0<br>CONTROLSS CPSW_CPTS_SYNC_0<br>Time Sync XBAR<br>CPPI_ICLK GMII_RFT_CLK /2<br>SYSCLK RGMII_MHZ_250_CLK DPLL_CORE_HSDIV_CLKOUT1<br>EXT_REFCLK RGMII_MHZ_50_CLK /10<br>WUCPUCLK RGMII_MHZ_5_CLK /100<br>CORE_PLL_HSDIV0_CLKOUT1<br>CORE_PLL_HSDIV0_CLKOUT0 CPTS_RFT_CLK<br>RCCLK10M<br>XTALCLK RMII1_MHZ_50_CLK<br>PER_PLL_HSDIV0_CLKOUT1 RMII1_REF_CLK<br>RCM<br>CPSW0_CLK_SRC_SEL RMII2_MHZ_50_CLK<br>RMII2_REF_CLK<br>CPSW0_RST_CTRL<br>Warm Reset Sources<br>**----- End of picture text -----**<br>


**Figure 4-19. CPSW3G Integration Diagram** 

The tables below summarize the device integration details of CPSW0. 

**Table 4-31.** _**CPSW0**_ **Device Integration** 

## This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|CPSW0|✓|INFRA0 VBUSP Interconnect|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

118 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-32.** _**CPSW0**_ **Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|CPSW0|CPPI_ICLK|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|CPSW0 Interface Clock|
||CPTS_RFT_CLK|XTACLK|External XTAL|25 MHz|CPSW0 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz|CPSW0 Interface Clock|
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|CPSW0 Interface Clock|
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz|CPSW0 Interface Clock|
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz|CPSW0 Interface Clock|
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator (RCCLK10M)|10 MHz|CPSW0 Interface Clock|
|||XTALCLK|External XTAL|25 MHz|CPSW0 Interface Clock|
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_HSDIV0_CLKO<br>UT1|192 MHz|CPSW0 Interface Clock|
||GMII_RFT_CLK|RGMII_250_CLK|RGMII 250 MHz Clock|250 MHz|CPSW0 Interface Clock|
||RMII1_MHZ_50_CLK|RGMII_50_CLK|RGMII 50 MHz Clock|50 MHz|CPSW0 Interface Clock|
|||RMII1_REF_CLK|RMII1 Reference Clock|50 MHz1|CPSW0 Interface Clock|
||RMII2_MHZ_50_CLK|RGMII_50_CLK|RGMII 50 MHz Clock|50 MHz|CPSW0 Interface Clock|
|||RMII2_REF_CLK|RMII2 Reference Clock|50 MHz1|CPSW0 Interface Clock|
||RGMII_MHZ_50_CLK|RGMII_50_CLK|RGMII 50 MHz Clock|50 MHz|CPSW0 Interface Clock|
||RGMII_MHZ_5_CLK|RGMII_5_CLK|RGMII 5 MHz Clock|5 MHz|CPSW0 Interface Clock|
||RGMII_MHZ_250_CLK|RGMII_250_CLK|RGMII 250 MHz Clock|250 MHz|CPSW0 Interface Clock|



## **Note** 

1The RMIIx_REF_CLK input pin can be drive by an external clock reference source. 50 MHz is required for proper operation. 

**Table 4-33.** _**CPSW0**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|CPSW0|CPSW_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|CPSW0 Asynchronous Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 119 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-34.** _**CPSW0**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|CPSW0|C0_FH_PULSE_INT<br>R_[0:3]|C0_FH_PULSE_INTR|All R5FSS<br>Cores PRU-<br>ICSS Core|Level|FHost (from host to Ethernet)<br>paced pulse interrupt|
||C0_TH_PULSE_INT<br>R_[0:3]|C0_TH_PULSE_INTR|All R5FSS<br>Cores PRU-<br>ICSS Core|Level|THost (from Ethernet to host)<br>paced pulse interrupt|
||C0_TH_THRESH_P<br>END_INTR_[0:3]|C0_TH_THRESH_PEND_INTR|All R5FSS<br>Cores PRU-<br>ICSS Core|Level|THost (from Ethernet to host)<br>non-paced pulse interrupt|
||C0_MISC_PEND_IN<br>TR_[0:3]|C0_MISC_PEND_INTR|All R5FSS<br>Cores PRU-<br>ICSS Core|Level|Miscellaneous non-paced pulse<br>interrupt|
||CPSW_STAT_PEND|STAT_PEND|All R5FSS<br>Cores PRU-<br>ICSS Core|Level|Statistics level interrupt|
||CPSW_HOST_PEN<br>D|HOST_PEND|All R5FSS<br>Cores PRU-<br>ICSS Core|Level|CPDMA host error level interrupt|
||CPSW_ECC_SEC_P<br>ULSE_INTR|ECC_SEC_PULSE_INTR|ESM|Level|ECC SEC pulse interrupt –<br>output from CPSW ECC module.|
||CPSW_ECC_DED_P<br>ULSE_INTR|ECC_DED_PULSE_INTR|ESM|Level|ECC DED pulse interrupt –<br>output from CPSW ECC module.|



**Table 4-35.** _**CPSW0**_ **Time Sync and Compare Event** 

This table describes the module capture event inputs. 

|**Module**<br>**Instance**|**Module Event**|**Destination Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|CPSW0|CPSW0_CPTS_COM<br>P|SoC_TimeSyncXBAR[0:3]|CPSW0_CPTS_COM<br>P_INTR|Level|CPSW0 Compare Event Interrupt|
|||CONTROLSS_TimeSyncXBA<br>R[0:3]||||
||CPSW0_CPTS_GENF<br>0|SoC_TimeSyncXBAR[0:3]|CPSW0_CPTS_GENF<br>0_INTR|Level|CPSW0 CPTS generator function<br>event interrupt 0|
|||CONTROLSS_TimeSyncXBA<br>R[0:3]||||
||CPSW0_CPTS_GENF<br>1|SoC_TimeSyncXBAR[0:3]|CPSW0_CPTS_GENF<br>1_INTR|Level|CPSW0 CPTS generator function<br>event interrupt 1|
|||CONTROLSS_TimeSyncXBA<br>R[0:3]||||
||CPSW0_CPTS_SYNC|SoC_TimeSyncXBAR[0:3]|CPSW0_CPTS_SYNC<br>_INTR|Level|CPSW0 CPTS Sync Event<br>Interrupt|
|||CONTROLSS_TimeSyncXBA<br>R[0:3]||||



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

For pin information on RGMII_ID_MODE and RGMII_REFCLK_SEL, see Register information and the corresponding section within the Device Configuration chapter 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

120 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.17 MMCSD Integration** 

There is 1x MMCSD integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [360 x 220] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>MMCSD#_VBUSCLK MMCSD#_DMA_RD_REQ<br>EDMA<br>MMCSD#_DMA_WR_REQ<br>SYS_CLK<br>WUCPUCLK MMCSD#_WP<br>EXT_REFCLK<br>DPLL_PER_HSDIV0_CLKOUT1<br>DPLL_CORE_HSDIV0_CLKOUT0 % MMCSD#_CLK MMCSD#_CD<br>RCCLK10M (10MHz)<br>XTALCLK 4<br>RCCLK10M (10MHz) MMCSD#_D[0:3]<br>MMCSD#<br>MMCSD#_CLKSRC_SEL Bit<br>MMCSD#_CLKDIV_SEL Bit MMCSD#_CMD<br>% MMCSD#_32K_CLK<br>MMCSD#_32K_CLKDIV_SEL Bit MMCSD#_CLK<br>RCM<br>MMCSD#_RST_CTRL Bit<br>MMCSD#_INT_REQ R5FSS0-CORE0<br>M MCSD#_WARMRESET<br>Warm Reset Sources R5FSS0-CORE1<br>R5FSS1-CORE0<br>R5FSS1-CORE1<br>CORE INTERCONNECT<br>DMA XBAR<br>**----- End of picture text -----**<br>


**Figure 4-20. MMCSD Integration** 

The tables below summarize the device integration details of the MMC/SD module. 

**Table 4-36.** _**MMCSD**_ **Device Integration** 

This table describes the module integration details. 

|**MMCSD Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|MMCSD0|✓|CORE VBUSM Interconnect|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

121 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **Table 4-37.** _**MMCSD**_ **Clocks** 

This table describes the module clocking signals. 

|**MMCSD**<br>**Instance**|**MMCSD Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|MMCSD0|MMCSD0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|MMC/SD Interface Clock|
||MMCSD0_32K_CLK|MMCSD0_32K_CLK|XTALCLK|32 KHz|MMC/SD Debounce Clock|
||MMCSD0_FCLK<br>(MMCSD_CLK)|WUCPUCLK|Oscillator Clock|25 MHz|MMC/SD Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator (RCCLK10M)|10 MHz||



**Table 4-38.** _**MMCSD**_ **Resets** 

This table describes the module reset signals. 

|**MMCSD**<br>**Instance**|**MMCSD Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|MMCSD0|MMCSD0_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|MMCSD0 Asynchronous Reset|



**Table 4-39.** _**MMCSD**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**MMCSD**<br>**Instance**|**MMCSD Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MMCSD0|MMCSD0_INT_req_0|MMCSD0_INT_req_0|ALL R5FSS Cores|Level|MMC/SD Interrupt|



**Table 4-40.** _**MMCSD**_ **DMA Requests** 

This table describes the module DMA requests. 

|**MMCSD**<br>**Instance**|**MMCSD DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MMCSD0|MMCSD0_DMA_RD_<br>REQ|MMCSD0_DMA_RD_REQ|EDMA Crossbar<br>(DMA_XBAR)|Level|MMC/SD DMA Read Request|
||MMCSD0_DMA_WR_<br>REQ|MMCSD0_DMA_WR_REQ|||MMC/SD DMA Write Request|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

122 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

## **4.18 OSPI Integration** 

There is 1x OSPI module integrated in the device. The diagram below provides a visual representation of the device integration details. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

123 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**==> picture [428 x 540] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>FSS0_OSPI0<br>AHB_INTF<br>APB_INTF<br>OSPI0_HCLK<br>OSPI0_PCLK<br>FLASH_INTF<br>SYS_CLK<br>EXT_REFCLK<br>WUCPUCLK<br>DPLL_PER_HSDIV0_CLKOUT1<br>OSPI0_RCLK<br>DPLL_CORE_HSDIV0_CLKOUT0<br>RCCLK10M<br>DPLL_CORE_HSDIV0_CLKOUT3<br>DPLL_PER_HSDIV0_CLKOUT2<br>OSPI_CLK_GCM_CLKSRC_SEL<br>EDMA<br>OSPI_INTR FSS0_OSPI0_LVL_INTR<br>R5FSS0_CORE0/1<br>OSPI_LVL_INTR<br>ESM0<br>  ESM0_LVL_EVENT_39 FSS0_OSPI0_ECC_CORR_LVL_INTR<br>  ESM0_LVL_EVENT_40                   FSS0_OSPI0_ECC_UNCORR_LVL_INTR<br>FSS0_OSPI0_RST<br>**----- End of picture text -----**<br>


**Figure 4-21. OSPI Integration Diagram** 

The tables below summarize the device integration details of OSPI. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

124 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-41.** _**OSPI**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Module Instance**||**Device Allocation**|**Device Allocation**|**SoC Interconnect**|**SoC Interconnect**|
|---|---|---|---|---|---|---|
|OSPI0|||✓||CORE VBUSM Interconnect||
||||**Table 4-42. FSS0_OSPI Clocks**||||
|**Module Instance **|**Module Clock Input**||**Source Clock Signal**<br>**Source**<br>**Description**||||
|FSS0_OSPI0|OSPI0_HCLK||SYS_CLK|SYS_CLK||FSS0_OSPI0 data transfer clock|
||OSPI0_PCLK||SYS_CLK|SYS_CLK||FSS0_OSPI0 configuration clock|
||OSPI0_RCLK||OSPI_CLK|WUCPUCLK||FSS0_OSPI0 Reference clock.<br>Mux controlled by<br>_MSS_RCM:OSPI0_CLK_SRC_SEL_|
||||EXT_REFCLK|EXT_REFCLK|||
||||SYS_CLK|SYS_CLK|||
||||DPLL_PER_HSDIV0_C<br>LKOUT1|PLL_PER_CLK:HSDIV0<br>_CLKOUT1|||
||||DPLL_CORE_HSDIV0_<br>CLKOUT0|PLL_CORE_CLK:HSDIV<br>0_CLKOUT0|||
||||RCCLK10M|Internal 10 MHz RC<br>Oscillator (RCCLK10M)|||
||||DPLL_CORE_HSDIV0_<br>CLKOUT3|PLL_CORE_CLK:HSDIV<br>0_CLKOUT3|||
||||DPLL_PER_HSDIV0_C<br>LKOUT2|PLL_PER_CLK:HSDIV0<br>_CLKOUT2|||



## **Table 4-43. FSS0_OSPI Resets** 

|**Module Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|FSS0_OSPI0|FSS0_OSPI0_RST|MOD_G_RST|POR|FSS0_OSPI0 reset|



## **Table 4-44. FSS0_OSPI Interrupt Requests** 

|**Module**<br>**Instance**|**Module Interrupt Signal**<br>**Destination Interrupt Input**|**Destination**<br>**Description**<br>**Type**|
|---|---|---|
|FSS0_OSPI0|OPTI_FLASH_OSPI0_LVL_INTR<br>OSPI0_LVL_INTR<br>OPTI_FLASH_OSPI0_ECC_COR<br>R_LVL_INTR<br>ESM0_LVL_EVENT_39|All R5FSS Cores<br>ICSSM Core<br>FSS0_OSPI0 interrupt<br>Level|
|||OPTI_FLASH<br>FSS0_OSPI0 ECC<br>Aggregator correctable<br>error interrupt<br>Level|
||OPTI_FLASH_OSPI0_ECC_UNC<br>ORR_LVL_INTR<br>ESM0_LVL_EVENT_40|OPTI_FLASH<br>FSS0_OSPI0<br>ECC Aggregator<br>uncorrectable error<br>interrupt<br>Level|



**Table 4-45.** _**OSPI**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|OSPI0|OPTI_FLASH|OSPI_INTR|OPTI_FLASH_OSPI0_<br>LVL_INTR|Pulse|OSPI0 DMA Event Request|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 125 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

126 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.19 MCAN Integration** 

There are 8x MCAN modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [420 x 301] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>CAN#<br>CAN#_VBUSCLK<br>CAN#_TX_DMA_REQ<br>4 EDMA<br>CAN#_CORE_FILTER_EVENTS_DMA_REQ<br>SYS_CLK 7<br>XTALCLK<br>CAN#_TXD<br>EXT_REFCLK<br>PER_PLL_HSDIV0_CLKOUT1 ÷   CAN#_CLK CAN#_RXD<br>CORE_PLL_HSDIV0_CLKOUT0<br>RCOSC (10MHz)<br>ICSSM<br>XTALCLK<br>RCOSC (10MHz)<br>R5FSS0-CORE0<br>CAN#_EXT_TS_ROLLOVER_LVL_INT_0 R5FSS0-CORE1<br>RCM<br>CAN#_LVL_INT_0 R5FSS1-CORE0<br>CAN#_CLKSRC_SEL Bit<br>CAN#_CLKDIV_SEL Bit CAN#_LVL_INT_1 R5FSS1-CORE1<br>CAN#_RST_CTRL Bit<br>CAN#_ECC_CORR_LVL_INT<br>ESM<br>CAN#_WARMRESET CAN#_ECC_UNCORR_LVL_INT<br>Warm Reset Sources<br>PERI INTERCONNECT<br>ICSSM XBAR<br>DMA  XBAR<br>**----- End of picture text -----**<br>


**Figure 4-22. MCAN Integration Diagram** 

The tables below summarize the device integration details of MCAN# (where # = 0 to 7). 

**Table 4-46.** _**MCAN**_ **Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|MCAN0|✓|Peripheral VBUSP Interconnect|
|MCAN1|✓|Peripheral VBUSP Interconnect|
|MCAN2|✓|Peripheral VBUSP Interconnect|
|MCAN3|✓|Peripheral VBUSP Interconnect|
|MCAN4|✓|Peripheral VBUSP Interconnect|
|MCAN5|✓|Peripheral VBUSP Interconnect|
|MCAN6|✓|Peripheral VBUSP Interconnect|
|MCAN7|✓|Peripheral VBUSP Interconnect|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 127 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **Table 4-47.** _**MCAN**_ **Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|MCAN0|MCAN0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN0 Interface Clock|
||MCAN0_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN0 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|MCAN1|MCAN1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN1 Interface Clock|
||MCAN1_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN1 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|MCAN2|MCAN2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN2 Interface Clock|
||MCAN2_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN2 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||



128 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-47.** _**MCAN**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|MCAN3|MCAN3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN3 Interface Clock|
||MCAN3_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN3 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|MCAN4|MCAN4_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN4 Interface Clock|
||MCAN4_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN4 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|MCAN5|MCAN5_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN5 Interface Clock|
||MCAN5_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN5 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 129 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **Table 4-47.** _**MCAN**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|MCAN6|MCAN6_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN6 Interface Clock|
||MCAN6_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN6 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|MCAN7|MCAN7_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz|MCAN7 Interface Clock|
||MCAN7_FCLK<br>(CAN_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|MCAN7 Functional Clock|
|||EXT_REFCLK|External Reference<br>Clock(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:HSDIV0_C<br>LKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:HSDIV0_<br>CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator(RCCLK10M)|10 MHz||



**Table 4-48.** _**MCAN**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|MCAN0|MCAN0_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN0 Module Reset|
|MCAN1|MCAN1_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN1 Module Reset|
|MCAN2|MCAN2_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN2 Module Reset|
|MCAN3|MCAN3_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN3 Module Reset|
|MCAN4|MCAN4_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN4 Module Reset|
|MCAN5|MCAN5_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN5 Module Reset|



130 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-48.** _**MCAN**_ **Resets (continued)** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|MCAN6|MCAN6_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN6 Module Reset|
|MCAN7|MCAN7_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|Asynchronous MCAN7 Module Reset|



**Table 4-49.** _**MCAN**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN0|MCAN0_INT_0|R5FSS0_CORE0_INTR_IN_27|R5FSS0-0|Level|MCAN0 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_27|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_27|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_27|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_40|PRU_ICSS|||
||MCAN0_INT_1|R5FSS0_CORE0_INTR_IN_28|R5FSS0-0|Level|MCAN0 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_28|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_28|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_28|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_41|PRU_ICSS|||
||MCAN0_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_26|R5FSS0-0|Level|MCAN0 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_26|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_26|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_26|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_39|PRU_ICSS0|||
||MCAN0_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_2|ESM0|Level|MCAN0 ECC Correctable Error<br>Interrupt|
||MCAN0_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_3|ESM0|Level|MCAN0 ECC Uncorrectable<br>Error Interrupt|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

131 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-49.** _**MCAN**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN1|MCAN1_INT_0|R5FSS0_CORE0_INTR_IN_30|R5FSS0-0|Level|MCAN1 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_30|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_30|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_30|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_43|PRU_ICSS|||
||MCAN1_INT_1|R5FSS0_CORE0_INTR_IN_31|R5FSS0-0|Level|MCAN1 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_31|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_31|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_31|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_44|PRU_ICSS|||
||MCAN1_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_29|R5FSS0-0|Level|MCAN1 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_29|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_29|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_29|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_42|PRU_ICSS|||
||MCAN1_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_4|ESM0|Level|MCAN1 ECC Correctable Error<br>Interrupt|
||MCAN1_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_5|ESM0|Level|MCAN1 ECC Uncorrectable<br>Error Interrupt|
|MCAN2|MCAN2_INT_0|R5FSS0_CORE1_INTR_IN_33|R5FSS0-0|Level|MCAN1 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_33|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_33|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_33|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_46|PRU_ICSS|||
||MCAN2_INT_1|R5FSS0_CORE0_INTR_IN_34|R5FSS0-0|Level|MCAN2 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_34|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_34|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_34|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_47|PRU_ICSS|||
||MCAN2_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_32|R5FSS0-0|Level|MCAN2 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_32|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_32|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_32|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_45|PRU_ICSS|||
||MCAN2_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_6|ESM0|Level|MCAN2 ECC Correctable Error<br>Interrupt|
||MCAN2_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_7|ESM0|Level|MCAN2 ECC Uncorrectable<br>Error Interrupt|



132 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-49.** _**MCAN**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN3|MCAN3_INT_0|R5FSS0_CORE0_INTR_IN_36|R5FSS0-0|Level|MCAN3 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_36|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_36|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_36|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_49|PRU_ICSS|||
||MCAN3_INT_1|R5FSS0_CORE0_INTR_IN_37|R5FSS0-0|Level|MCAN3 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_37|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_37|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_37|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_50|PRU_ICSS|||
||MCAN3_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_35|R5FSS0-0|Level|MCAN3 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_35|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_35|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_35|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_48|PRU_ICSS|||
||MCAN3_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_8|ESM0|Level|MCAN3 ECC Correctable Error<br>Interrupt|
||MCAN3_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_9|ESM0|Level|MCAN3 ECC Uncorrectable<br>Error Interrupt|
|MCAN4|MCAN4_INT_0|R5FSS0_CORE0_INTR_IN_198|R5FSS0-0|Level|MCAN4 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_198|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_198|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_198|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_60|PRU_ICSS|||
||MCAN4_INT_1|R5FSS0_CORE0_INTR_IN_199|R5FSS0-0|Level|MCAN4 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_199|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_199|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_199|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_61|PRU_ICSS|||
||MCAN4_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_197|R5FSS0-0|Level|MCAN4 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_197|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_197|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_197|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_59|PRU_ICSS|||
||MCAN4_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_39|ESM0|Level|MCAN4 ECC Correctable Error<br>Interrupt|
||MCAN4_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_40|ESM0|Level|MCAN4 ECC Uncorrectable<br>Error Interrupt|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 133 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-49.** _**MCAN**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN5|MCAN5_INT_0|R5FSS0_CORE0_INTR_IN_201|R5FSS0-0|Level|MCAN5 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_201|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_201|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_201|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_63|PRU_ICSS|||
||MCAN5_INT_1|R5FSS0_CORE0_INTR_IN_202|R5FSS0-0|Level|MCAN5 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_202|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_202|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_202|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_64|PRU_ICSS|||
||MCAN5_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_200|R5FSS0-0|Level|MCAN5 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_200|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_200|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_200|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_62|PRU_ICSS|||
||MCAN5_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_41|ESM0|Level|MCAN5 ECC Correctable Error<br>Interrupt|
||MCAN5_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_42|ESM0|Level|MCAN5 ECC Uncorrectable<br>Error Interrupt|
|MCAN6|MCAN6_INT_0|R5FSS0_CORE0_INTR_IN_204|R5FSS0-0|Level|MCAN6 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_204|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_204|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_204|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_66|PRU_ICSS|||
||MCAN6_INT_1|R5FSS0_CORE0_INTR_IN_205|R5FSS0-0|Level|MCAN6 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_205|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_205|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_205|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_67|PRU_ICSS|||
||MCAN6_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_203|R5FSS0-0|Level|MCAN6 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_203|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_203|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_203|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_65|PRU_ICSS|||
||MCAN6_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_43|ESM0|Level|MCAN6 ECC Correctable Error<br>Interrupt|
||MCAN6_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_44|ESM0|Level|MCAN6 ECC Uncorrectable<br>Error Interrupt|



134 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-49.** _**MCAN**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN7|MCAN7_INT_0|R5FSS0_CORE0_INTR_IN_207|R5FSS0-0|Level|MCAN7 Line 0 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_207|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_207|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_207|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_69|PRU_ICSS|||
||MCAN7_INT_1|R5FSS0_CORE0_INTR_IN_208|R5FSS0-0|Level|MCAN7 Line 1 Interrupt Request|
|||R5FSS0_CORE1_INTR_IN_208|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_208|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_208|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_70|PRU_ICSS|||
||MCAN7_EXT_TS_R<br>OLLOVER_INT_0|R5FSS0_CORE0_INTR_IN_206|R5FSS0-0|Level|MCAN7 External TimeStamp<br>Counter Rollover Interrupt|
|||R5FSS0_CORE1_INTR_IN_206|R5FSS0-1|||
|||R5FSS1_CORE0_INTR_IN_206|R5FSS1-0|||
|||R5FSS1_CORE1_INTR_IN_206|R5FSS1-1|||
|||PRU_ICSS0_INTR_IN_68|PRU_ICSS|||
||MCAN7_ECC_COR<br>R_LVL_INT_0|ESM0_LVL_IN_45|ESM0|Level|MCAN7 ECC Correctable Error<br>Interrupt|
||MCAN7_ECC_UNC<br>ORR_LVL_INT_0|ESM0_LVL_IN_46|ESM0|Level|MCAN7 ECC Uncorrectable<br>Error Interrupt|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

135 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **Table 4-50.** _**MCAN**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN0|MCAN0_FE_INTR_0|EDMA_XBAR_147|EDMA|Pulse|MCAN0 Receive Filter Event 0<br>DMA Request|
||MCAN0_FE_INTR_1|EDMA_XBAR_148|EDMA|Pulse|MCAN0 Receive Filter Event 1<br>DMA Request|
||MCAN0_FE_INTR_2|EDMA_XBAR_149|EDMA|Pulse|MCAN0 Receive Filter Event 2<br>DMA Request|
||MCAN0_FE_INTR_3|EDMA_XBAR_150|EDMA|Pulse|MCAN0 Receive Filter Event 3<br>DMA Request|
||MCAN0_FE_INTR_4|EDMA_XBAR_151|EDMA|Pulse|MCAN0 Receive Filter Event 4<br>DMA Request|
||MCAN0_FE_INTR_5|EDMA_XBAR_152|EDMA|Pulse|MCAN0 Receive Filter Event 5<br>DMA Request|
||MCAN0_FE_INTR_6|EDMA_XBAR_153|EDMA|Pulse|MCAN0 Receive Filter Event 6<br>DMA Request|
||MCAN0_TXDMA_0|EDMA_XBAR_74|EDMA|Pulse|MCAN0 Transmit Core DMA<br>Request 0|
||MCAN0_TXDMA_1|EDMA_XBAR_75|EDMA|Pulse|MCAN0 Transmit Core DMA<br>Request 1|
||MCAN0_TXDMA_2|EDMA_XBAR_76|EDMA|Pulse|MCAN0 Transmit Core DMA<br>Request 2|
||MCAN0_TXDMA_3|EDMA_XBAR_77|EDMA|Pulse|MCAN0 Transmit Core DMA<br>Request 3|



136 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-50.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN1|MCAN1_FE_INTR_0|EDMA_XBAR_154|EDMA|Pulse|MCAN1 Receive Filter Event 0<br>DMA Request|
||MCAN1_FE_INTR_1|EDMA_XBAR_155|EDMA|Pulse|MCAN1 Receive Filter Event 1<br>DMA Request|
||MCAN1_FE_INTR_2|EDMA_XBAR_156|EDMA|Pulse|MCAN1 Receive Filter Event 2<br>DMA Request|
||MCAN1_FE_INTR_3|EDMA_XBAR_157|EDMA|Pulse|MCAN1 Receive Filter Event 3<br>DMA Request|
||MCAN1_FE_INTR_4|EDMA_XBAR_158|EDMA|Pulse|MCAN1 Receive Filter Event 4<br>DMA Request|
||MCAN1_FE_INTR_5|EDMA_XBAR_159|EDMA|Pulse|MCAN1 Receive Filter Event 5<br>DMA Request|
||MCAN1_FE_INTR_6|EDMA_XBAR_160|EDMA|Pulse|MCAN1 Receive Filter Event 6<br>DMA Request|
||MCAN1_TXDMA_0|EDMA_XBAR_78|EDMA|Pulse|MCAN1 Transmit Core DMA<br>Request 0|
||MCAN1_TXDMA_1|EDMA_XBAR_79|EDMA|Pulse|MCAN1 Transmit Core DMA<br>Request 1|
||MCAN1_TXDMA_2|EDMA_XBAR_80|EDMA|Pulse|MCAN1 Transmit Core DMA<br>Request 2|
||MCAN1_TXDMA_3|EDMA_XBAR_81|EDMA|Pulse|MCAN1 Transmit Core DMA<br>Request 3|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 137 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-50.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN2|MCAN2_FE_INTR_0|EDMA_XBAR_161|EDMA|Pulse|MCAN2 Receive Filter Event 0<br>DMA Request|
||MCAN2_FE_INTR_1|EDMA_XBAR_162|EDMA|Pulse|MCAN2 Receive Filter Event 1<br>DMA Request|
||MCAN2_FE_INTR_2|EDMA_XBAR_163|EDMA|Pulse|MCAN2 Receive Filter Event 2<br>DMA Request|
||MCAN2_FE_INTR_3|EDMA_XBAR_164|EDMA|Pulse|MCAN2 Receive Filter Event 3<br>DMA Request|
||MCAN2_FE_INTR_4|EDMA_XBAR_165|EDMA|Pulse|MCAN2 Receive Core Filter Event<br>4 DMA Request|
||MCAN2_FE_INTR_5|EDMA_XBAR_166|EDMA|Pulse|MCAN2 Receive Filter Event 5<br>DMA Request|
||MCAN2_FE_INTR_6|EDMA_XBAR_167|EDMA|Pulse|MCAN2 Receiver Filter Event 6<br>DMA Request|
||MCAN2_TXDMA_0|EDMA_XBAR_82|EDMA|Pulse|MCAN2 Transmit Core DMA<br>Request 0|
||MCAN2_TXDMA_1|EDMA_XBAR_83|EDMA|Pulse|MCAN2 Transmit Core DMA<br>Request 1|
||MCAN2_TXDMA_2|EDMA_XBAR_84|EDMA|Pulse|MCAN2 Transmit Core DMA<br>Request 2|
||MCAN2_TXDMA_3|EDMA_XBAR_85|EDMA|Pulse|MCAN2 Transmit Core DMA<br>Request 3|



138 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-50.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN3|MCAN3_FE_INTR_0|EDMA_XBAR_168|EDMA|Pulse|MCAN3 Receive Filter Event 0<br>DMA Request|
||MCAN3_FE_INTR_1|EDMA_XBAR_169|EDMA|Pulse|MCAN3 Receive Filter Event 1<br>DMA Request|
||MCAN3_FE_INTR_2|EDMA_XBAR_170|EDMA|Pulse|MCAN3 Receive Filter Event 2<br>DMA Request|
||MCAN3_FE_INTR_3|EDMA_XBAR_171|EDMA|Pulse|MCAN3 Receive Filter Event 3<br>DMA Request|
||MCAN3_FE_INTR_4|EDMA_XBAR_172|EDMA|Pulse|MCAN3 Receive Filter Event 4<br>DMA Request|
||MCAN3_FE_INTR_5|EDMA_XBAR_173|EDMA|Pulse|MCAN3 Receive Filter Event 5<br>DMA Request|
||MCAN3_FE_INTR_6|EDMA_XBAR_174|EDMA|Pulse|MCAN3 Receive Filter Event 6<br>DMA Request|
||MCAN3_TXDMA_0|EDMA_XBAR_86|EDMA|Pulse|MCAN3 Transmit Core DMA<br>Request 0|
||MCAN3_TXDMA_1|EDMA_XBAR_87|EDMA|Pulse|MCAN3 Transmit Core DMA<br>Request 1|
||MCAN3_TXDMA_2|EDMA_XBAR_88|EDMA|Pulse|MCAN3 Transmit Core DMA<br>Request 2|
||MCAN3_TXDMA_3|EDMA_XBAR_89|EDMA|Pulse|MCAN3 Transmit Core DMA<br>Request 3|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 139 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-50.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN4|MCAN4_FE_INTR_0|EDMA_XBAR_192|EDMA|Pulse|MCAN4 Receive Filter Event 0<br>DMA Request|
||MCAN4_FE_INTR_1|EDMA_XBAR_193|EDMA|Pulse|MCAN4 Receive Filter Event 1<br>DMA Request|
||MCAN4_FE_INTR_2|EDMA_XBAR_194|EDMA|Pulse|MCAN4 Receive Filter Event 2<br>DMA Request|
||MCAN4_FE_INTR_3|EDMA_XBAR_195|EDMA|Pulse|MCAN4 Receive Filter Event 3<br>DMA Request|
||MCAN4_FE_INTR_4|EDMA_XBAR_196|EDMA|Pulse|MCAN4 Receive Filter Event 4<br>DMA Request|
||MCAN4_FE_INTR_5|EDMA_XBAR_197|EDMA|Pulse|MCAN4 Receive Filter Event 5<br>DMA Request|
||MCAN4_FE_INTR_6|EDMA_XBAR_198|EDMA|Pulse|MCAN4 Receive Filter Event 6<br>DMA Request|
||MCAN4_TXDMA_0|EDMA_XBAR_176|EDMA|Pulse|MCAN4 Transmit Core DMA<br>Request 0|
||MCAN4_TXDMA_1|EDMA_XBAR_177|EDMA|Pulse|MCAN4 Transmit Core DMA<br>Request 1|
||MCAN4_TXDMA_2|EDMA_XBAR_178|EDMA|Pulse|MCAN4 Transmit Core DMA<br>Request 2|
||MCAN4_TXDMA_3|EDMA_XBAR_179|EDMA|Pulse|MCAN4 Transmit Core DMA<br>Request 3|



140 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-50.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN5|MCAN5_FE_INTR_0|EDMA_XBAR_199|EDMA|Pulse|MCAN5 Receive Filter Event 0<br>DMA Request|
||MCAN5_FE_INTR_1|EDMA_XBAR_200|EDMA|Pulse|MCAN5 Receive Filter Event 1<br>DMA Request|
||MCAN5_FE_INTR_2|EDMA_XBAR_201|EDMA|Pulse|MCAN5 Receive Filter Event 2<br>DMA Request|
||MCAN5_FE_INTR_3|EDMA_XBAR_202|EDMA|Pulse|MCAN5 Receive Filter Event 3<br>DMA Request|
||MCAN5_FE_INTR_4|EDMA_XBAR_203|EDMA|Pulse|MCAN5 Receive Filter Event 4<br>DMA Request|
||MCAN5_FE_INTR_5|EDMA_XBAR_204|EDMA|Pulse|MCAN5 Receive Filter Event 5<br>DMA Request|
||MCAN5_FE_INTR_6|EDMA_XBAR_205|EDMA|Pulse|MCAN5 Receive Filter Event 6<br>DMA Request|
||MCAN5_TXDMA_0|EDMA_XBAR_180|EDMA|Pulse|MCAN5 Transmit Core DMA<br>Request 0|
||MCAN5_TXDMA_1|EDMA_XBAR_181|EDMA|Pulse|MCAN5 Transmit Core DMA<br>Request 1|
||MCAN5_TXDMA_2|EDMA_XBAR_182|EDMA|Pulse|MCAN5 Transmit Core DMA<br>Request 2|
||MCAN5_TXDMA_3|EDMA_XBAR_183|EDMA|Pulse|MCAN5 Transmit Core DMA<br>Request 3|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 141 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-50.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN6|MCAN6_FE_INTR_0|EDMA_XBAR_206|EDMA|Pulse|MCAN6 Receive Filter Event 0<br>DMA Request|
||MCAN6_FE_INTR_1|EDMA_XBAR_207|EDMA|Pulse|MCAN6 Receive Filter Event 1<br>DMA Request|
||MCAN6_FE_INTR_2|EDMA_XBAR_208|EDMA|Pulse|MCAN6 Receive Filter Event 2<br>DMA Request|
||MCAN6_FE_INTR_3|EDMA_XBAR_209|EDMA|Pulse|MCAN6 Receive Filter Event 3<br>DMA Request|
||MCAN6_FE_INTR_4|EDMA_XBAR_210|EDMA|Pulse|MCAN6 Receive Filter Event 4<br>DMA Request|
||MCAN6_FE_INTR_5|EDMA_XBAR_211|EDMA|Pulse|MCAN6 Receive Filter Event 5<br>DMA Request|
||MCAN6_FE_INTR_6|EDMA_XBAR_212|EDMA|Pulse|MCAN6 Receive Filter Event 6<br>DMA Request|
||MCAN6_TXDMA_0|EDMA_XBAR_184|EDMA|Pulse|MCAN6 Transmit Core DMA<br>Request 0|
||MCAN6_TXDMA_1|EDMA_XBAR_185|EDMA|Pulse|MCAN6 Transmit Core DMA<br>Request 1|
||MCAN6_TXDMA_2|EDMA_XBAR_186|EDMA|Pulse|MCAN6 Transmit Core DMA<br>Request 2|
||MCAN6_TXDMA_3|EDMA_XBAR_187|EDMA|Pulse|MCAN6 Transmit Core DMA<br>Request 3|



142 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-50.** _**MCAN**_ **DMA Requests (continued)** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCAN7|MCAN7_FE_INTR_0|EDMA_XBAR_213|EDMA|Pulse|MCAN7 Receive Filter Event 0<br>DMA Request|
||MCAN7_FE_INTR_1|EDMA_XBAR_214|EDMA|Pulse|MCAN7 Receive Filter Event 1<br>DMA Request|
||MCAN7_FE_INTR_2|EDMA_XBAR_215|EDMA|Pulse|MCAN7 Receive Filter Event 2<br>DMA Request|
||MCAN7_FE_INTR_3|EDMA_XBAR_216|EDMA|Pulse|MCAN7 Receive Filter Event 3<br>DMA Request|
||MCAN7_FE_INTR_4|EDMA_XBAR_217|EDMA|Pulse|MCAN7 Receive Filter Event 4<br>DMA Request|
||MCAN7_FE_INTR_5|EDMA_XBAR_218|EDMA|Pulse|MCAN7 Receive Filter Event 5<br>DMA Request|
||MCAN7_FE_INTR_6|EDMA_XBAR_219|EDMA|Pulse|MCAN7 Receive Filter Event 6<br>DMA Request|
||MCAN7_TXDMA_0|EDMA_XBAR_188|EDMA|Pulse|MCAN7 Transmit Core DMA<br>Request 0|
||MCAN7_TXDMA_1|EDMA_XBAR_189|EDMA|Pulse|MCAN7 Transmit Core DMA<br>Request 1|
||MCAN7_TXDMA_2|EDMA_XBAR_190|EDMA|Pulse|MCAN7 Transmit Core DMA<br>Request 2|
||MCAN7_TXDMA_3|EDMA_XBAR_191|EDMA|Pulse|MCAN7 Transmit Core DMA<br>Request 3|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

## **4.20 LIN Integration** 

There are 5x LIN modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 143 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**==> picture [447 x 310] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>LIN#<br>LIN#_VBUSCLK LIN#_TX_DMA_REQ<br>EDMA<br>LIN#_RX_DMA_REQ<br>SYS_CLK<br>XTALCLK<br>EXT_REFCLK<br>PER_PLL_HSDIV0_CLKOUT1<br>÷   LIN#_CLK LIN#_TXD<br>CORE_PLL_HSDIV0_CLKOUT0<br>RCOSC (10MHz)<br>XTALCLK<br>LIN#_RXD<br>PER_PLL_HSDIV0_CLKOUT0<br>RCM ICSSM<br>LIN#_UART#_CLKSRC_SEL Bit<br>LIN#_UART#_CLKDIV_SEL Bit<br>LIN#_INT_REQ[1:0] R5FSS0-CORE0<br>LIN#_RST_CTRL Bit<br>R5FSS0-CORE1<br>R5FSS1-CORE0<br>LIN#_WARMRESET<br>Warm Reset Sources R5FSS1-CORE1<br>PERI INTERCONNECT<br>ICSSM XBAR<br>DMA  XBAR<br>**----- End of picture text -----**<br>


**Figure 4-23. LIN Integration** 

# = 0 to 4 

The tables below summarize the device integration details of LIN# (where # = 0 to 5). 

**Table 4-51.** _**LIN**_ **Device Integration** 

This table describes the LIN device integration details. 

|**LIN Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|LIN0|✓|Peripheral VBUSP Interconnect|
|LIN1|✓|Peripheral VBUSP Interconnect|
|LIN2|✓|Peripheral VBUSP Interconnect|
|LIN3|✓|Peripheral VBUSP Interconnect|
|LIN4|✓|Peripheral VBUSP Interconnect|



144 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-52.** _**LIN**_ **Clocks** 

This table describes the LIN clocking signals. 

|**LIN**<br>**Instance**|**LIN Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|LIN0|LIN0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|LIN0 Interface Clock<br>(LIN0_CLK must be<br>running for register access)|
||LIN0_FCLK<br>(LIN_CLK)|XTALCLK|External XTAL|25 MHz|LIN0 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||
|LIN1|LIN1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|LIN1 Interface Clock<br>(LIN1_CLK must be<br>running for register access)|
||LIN1_FCLK<br>(LIN_CLK)|XTALCLK|External XTAL|25 MHz|LIN1 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 145 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-52.** _**LIN**_ **Clocks (continued)** 

This table describes the LIN clocking signals. 

|**LIN**<br>**Instance**|**LIN Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|LIN2|LIN2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|LIN2 Interface Clock<br>(LIN2_CLK must be<br>running for register access)|
||LIN2_FCLK<br>(LIN_CLK)|XTALCLK|External XTAL|25 MHz|LIN2 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||
|LIN3|LIN3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|LIN3 Interface Clock<br>(LIN3_CLK must be<br>running for register access)|
||LIN3_FCLK<br>(LIN_CLK)|XTALCLK|External XTAL|25 MHz|LIN3 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



146 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-52.** _**LIN**_ **Clocks (continued)** 

This table describes the LIN clocking signals. 

|**LIN**<br>**Instance**|**LIN Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|LIN4|LIN4_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|LIN4 Interface Clock<br>(LIN4_CLK must be<br>running for register access)|
||LIN4_FCLK<br>(LIN_CLK)|XTALCLK|External XTAL|25 MHz|LIN4 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT0|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz||
|||RCCLK10M|Internal 10MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT0|PLL_PER_CLK:HSDIV0_C<br>LKOUT0|160 MHz||



**Table 4-53.** _**LIN**_ **Resets** 

This table describes the LIN reset signals. 

|**LIN**<br>**Instance**|**LIN Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|LIN0|LIN0_RST<br>(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|LIN0 Asynchronous Reset|
|LIN1|LIN1_RST<br>(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|LIN1 Asynchronous Reset|
|LIN2|LIN2_RST<br>(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|LIN2 Asynchronous Reset|
|LIN3|LIN3_RST<br>(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|LIN3 Asynchronous Reset|
|LIN4|LIN4_RST<br>(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|LIN4 Asynchronous Reset|



**Table 4-54.** _**LIN**_ **Interrupt Requests** 

This table describes the LIN interrupt requests. 

|**LIN Instance**|**LIN Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|LIN0|LIN0_INT_req_0<br>|LIN0_INT_req_0|ALL R5FSS<br>Cores, PRU-<br>ICSS BAR|Pulse|LIN0 Event Interrupts|
||LIN0_INT_req_1<br>|LIN0_INT_req_1||||
|LIN1|LIN1_INT_req_0<br>|LIN1_INT_req_0|ALL R5FSS<br>Cores, PRU-<br>ICSS XBAR|Pulse|LIN1 Event Interrupts|
||LIN1_INT_req_1<br>|LIN1_INT_req_1||||
|LIN2|LIN2_INT_req_0<br>|LIN2_INT_req_0|ALL R5FSS<br>Cores, PRU-<br>ICSS XBAR|Pulse|LIN2 Event Interrupts|
||LIN2_INT_req_1<br>|LIN2_INT_req_1||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 147 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-54.** _**LIN**_ **Interrupt Requests (continued)** 

This table describes the LIN interrupt requests. 

|**LIN Instance**|**LIN Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|LIN3|LIN3_INT_req_0|LIN3_INT_req_0|ALL R5FSS<br>Cores, PRU-<br>ICSS XBAR|Pulse|LIN3 Event Interrupts|
||LIN3_INT_req_1|LIN3_INT_req_1||||
|LIN4|LIN4_INT_req_0|LIN4_INT_req_0|ALL R5FSS<br>Cores, PRU-<br>ICSS XBAR|Pulse|LIN4 Event Interrupts|
||LIN4_INT_req_1|LIN4_INT_req_1||||



## **Table 4-55.** _**LIN**_ **DMA Requests** 

## This table describes the LIN DMA requests. 

|**LIN**<br>**Instance**|**LIN DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|LIN0|LIN0_TX_DMA_REQ|LIN0_tx_dma_req|EDMA Crossbar<br>(DMA_XBAR)|Pulse|LIN0 TX DMA Request|
||LIN0_RX_DMA_REQ|LIN0_rx_dma_req|||LIN0 RX DMA Request|
|LIN1|LIN1_TX_DMA_REQ|LIN1_tx_dma_req|EDMA Crossbar<br>(DMA_XBAR)|Pulse|LIN1 TX DMA Request|
||LIN1_RX_DMA_REQ|LIN1_rx_dma_req|||LIN1 RX DMA Request|
|LIN2|LIN2_TX_DMA_REQ|LIN2_tx_dma_req|EDMA Crossbar<br>(DMA_XBAR)|Pulse|LIN2 TX DMA Request|
||LIN2_RX_DMA_REQ|LIN2_rx_dma_req|||LIN2 RX DMA Request|
|LIN3|LIN3_TX_DMA_REQ|LIN3_tx_dma_req|EDMA Crossbar<br>(DMA_XBAR)|Pulse|LIN3 TX DMA Request|
||LIN3_RX_DMA_REQ|LIN3_rx_dma_req|||LIN3 RX DMA Request|
|LIN4|LIN4_TX_DMA_REQ|LIN4_tx_dma_req|EDMA Crossbar<br>(DMA_XBAR)|Pulse|LIN4 TX DMA Request|
||LIN4_RX_DMA_REQ|LIN4_rx_dma_req|||LIN4 RX DMA Request|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

148 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.21 RTI Integration** 

There are 8x RTI modules integrated in the device. The diagram and tables below show the device integration details. 

## **Figure 4-24. RTI Integration** 

The tables below summarize the integration of RTI# (where # = 0, 1, 2, 3, 4, 5, 6, 7) in the device. Each RTI# instance is supplied by dedicated RTICLK# mux. 

**==> picture [468 x 277] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device RTI #<br>RTI#_VBUSCLK RTI#_DMA[0:3] EDMA<br>SYSCLK<br>XTALCLK<br>EXT_REFCLK RTI0_INT_REQ[0] ADCTRIG1<br>PER_PLL_HSDIV0_CLKOUT1 RTI1_INT_REQ[0] ADCTRIG2<br>RTI#_CLK<br>CORE_PLL_HSDIV0_CLKOUT1 RTI2_INT_REQ[0] ADCTRIG3<br>RCCLK(10MHz)<br>XTALCLK RTI3_INT_REQ[0] ADCTRIG4<br>CPTS_GENF0 RTI4_INT_REQ[0] ADCTRIG5<br>RTI5_INT_REQ[0] ADCTRIG6<br>RCM RTI#_CAPEVT[0:1] RTI6_INT_REQ[0] ADCTRIG7<br>RTI#_CLK_SRC_SE L RTI7_INT_REQ[0] ADCTRIG8<br>RTI#_CLK_DIV_VA L RTI#_INT_REQ[0:3] R5FSS0-CORE0<br>RTI#_RST_CTR L<br>RTI#_WARMRESET<br>Warm Reset Sources R5FSS0-CORE1<br>RTI#_OVERFLOW[0:1]<br>Interrupts<br>PORz RTI#_POR R5FSS1-CORE0<br>R5FSS1-CORE0<br>PERI VBUSP Interconnect<br>DMA  XBAR<br>TIMESYNC XBAR CONTROLSS<br>**----- End of picture text -----**<br>


**Figure 4-25. RTI Integration Diagram** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|RTI0|✓|VBUSP CORE Interconnect|
|RTI1|✓|VBUSP CORE Interconnect|
|RTI2|✓|VBUSP CORE Interconnect|
|RTI3|✓|VBUSP CORE Interconnect|
|RTI4|✓|VBUSP CORE Interconnect|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 149 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|RTI5|✓|VBUSP CORE Interconnect|
|RTI6|✓|VBUSP CORE Interconnect|
|RTI7|✓|VBUSP CORE Interconnect|



## **Table 4-56.** _**RTI**_ **Clocks** 

This table table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|RTI0|RTI0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI0 VBUSP Interface<br>Clock|
||RTI0_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI0 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||
|RTI1|RTI1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI1 VBUSP Interface<br>Clock|
||RTI1_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI1 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||



150 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-56.** _**RTI**_ **Clocks (continued)** 

This table table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|RTI2|RTI2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI2 VBUSP Interface<br>Clock|
||RTI2_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI2 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||
|RTI3|RTI3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI3 VBUSP Interface<br>Clock|
||RTI3_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI3 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

151 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-56.** _**RTI**_ **Clocks (continued)** 

This table table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|RTI4|RTI4_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI4 VBUSP Interface<br>Clock|
||RTI4_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI4 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||
|RTI5|RTI5_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI5 VBUSP Interface<br>Clock|
||RTI5_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI5 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||



152 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-56.** _**RTI**_ **Clocks (continued)** 

This table table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|RTI6|RTI6_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI6 VBUSP Interface<br>Clock|
||RTI6_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI6 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||
|RTI7|RTI7_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|RTI7 VBUSP Interface<br>Clock|
||RTI7_FCLK (RTI_CLK)|XTALCLK|External XTAL|25 MHz|RTI7 Functional Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||DPLL_PER_HSDIV0_CLK<br>OUT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External XTAL|25 MHz||
|||CTPS_GENF0|CPSW CPTS GENF0<br>Clock|50 MHz||



**Table 4-57.** _**RTI**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|RTI0|RTI0_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI0 Asynchronous Reset|
||RTI0_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI0 Power-On Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 153 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-57.** _**RTI**_ **Resets (continued)** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|RTI1|RTI1_RST<br>RTI1_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI1 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI1 Power-On Reset|
|RTI2|RTI2_RST<br>RTI2_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI2 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI2 Power-On Reset|
|RTI3|RTI3_RST<br>RTI3_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI3 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI3 Power-On Reset|
|RTI4|RTI4_RST<br>RTI4_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI4 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI4 Power-On Reset|
|RTI5|RTI5_RST<br>RTI5_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI5 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI5 Power-On Reset|
|RTI6|RTI6_RST<br>RTI6_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI6 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI6 Power-On Reset|
|RTI7|RTI7_RST<br>RTI7_POR_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|RTI7 Asynchronous Reset|
|||POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|RTI7 Power-On Reset|



**Table 4-58.** _**RTI**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|RTI0|RTI0_INT_REQ_0|RTI0_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI0 Status Event Interrupt|
||RTI0_INT_REQ_1|RTI0_INT_REQ_1||||
||RTI0_INT_REQ_2|RTI0_INT_REQ_2||||
||RTI0_INT_REQ_3|RTI0_INT_REQ_3||||
||RTI0_OVL_REQ_0|RTI0_OVERFLOW_LEVEL_0|||RTI0 Counter Overflow Event<br>Interrupt|
||RTI0_OVL_REQ_1|RTI0_OVERFLOW_LEVEL_1||||
|RTI1|RTI1_INT_REQ_0|RTI1_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI1 Status Event Interrupt|
||RTI1_INT_REQ_1|RTI1_INT_REQ_1||||
||RTI1_INT_REQ_2|RTI1_INT_REQ_2||||
||RTI1_INT_REQ_3|RTI1_INT_REQ_3||||
||RTI1_OVL_REQ_0|RTI1_OVERFLOW_LEVEL_0|||RTI1 Counter Overflow Event<br>Interrupt|
||RTI1_OVL_REQ_1|RTI1_OVERFLOW_LEVEL_1||||



154 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-58.** _**RTI**_ **Interrupt Requests (continued)** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|RTI2|RTI2_INT_REQ_0|RTI2_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI2 Status Event Interrupt|
||RTI2_INT_REQ_1|RTI2_INT_REQ_1||||
||RTI2_INT_REQ_2|RTI2_INT_REQ_2||||
||RTI2_INT_REQ_3|RTI2_INT_REQ_3||||
||RTI2_OVL_REQ_0|RTI2_OVERFLOW_LEVEL_0|||RTI2 Counter Overflow Event<br>Interrupt|
||RTI2_OVL_REQ_1|RTI2_OVERFLOW_LEVEL_1||||
|RTI3|RTI3_INT_REQ_0|RTI3_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI3 Status Event Interrupt|
||RTI3_INT_REQ_1|RTI3_INT_REQ_1||||
||RTI3_INT_REQ_2|RTI3_INT_REQ_2||||
||RTI3_INT_REQ_3|RTI3_INT_REQ_3||||
||RTI3_OVL_REQ_0|RTI3_OVERFLOW_LEVEL_0|||RTI3 Counter Overflow Event<br>Interrupt|
||RTI3_OVL_REQ_1|RTI3_OVERFLOW_LEVEL_1||||
|RTI4|RTI4_INT_REQ_0|RTI4_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI4 Status Event Interrupt|
||RTI4_INT_REQ_1|RTI4_INT_REQ_1||||
||RTI4_INT_REQ_2|RTI4_INT_REQ_2||||
||RTI4_INT_REQ_3|RTI4_INT_REQ_3||||
||RTI4_OVL_REQ_0|RTI4_OVERFLOW_LEVEL_0|||RTI4 Counter Overflow Event<br>Interrupt|
||RTI4_OVL_REQ_1|RTI4_OVERFLOW_LEVEL_1||||
|RTI5|RTI5_INT_REQ_0|RTI5_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI5 Status Event Interrupt|
||RTI5_INT_REQ_1|RTI5_INT_REQ_1||||
||RTI5_INT_REQ_2|RTI5_INT_REQ_2||||
||RTI5_INT_REQ_3|RTI5_INT_REQ_3||||
||RTI5_OVL_REQ_0|RTI5_OVERFLOW_LEVEL_0|||RTI5 Counter Overflow Event<br>Interrupt|
||RTI5_OVL_REQ_1|RTI5_OVERFLOW_LEVEL_1||||
|RTI6|RTI6_INT_REQ_0|RTI6_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI6 Status Event Interrupt|
||RTI6_INT_REQ_1|RTI6_INT_REQ_1||||
||RTI6_INT_REQ_2|RTI6_INT_REQ_2||||
||RTI6_INT_REQ_3|RTI6_INT_REQ_3||||
||RTI6_OVL_REQ_0|RTI6_OVERFLOW_LEVEL_0|||RTI6 Counter Overflow Event<br>Interrupt|
||RTI6_OVL_REQ_1|RTI6_OVERFLOW_LEVEL_1||||
|RTI7|RTI7_INT_REQ_0|RTI7_INT_REQ_0|ALL R5FSS Cores|Pulse|RTI7 Status Event Interrupt|
||RTI7_INT_REQ_1|RTI7_INT_REQ_1||||
||RTI7_INT_REQ_2|RTI7_INT_REQ_2||||
||RTI7_INT_REQ_3|RTI7_INT_REQ_3||||
||RTI7_OVL_REQ_0|RTI7_OVERFLOW_LEVEL_0|||RTI7 Counter Overflow Event<br>Interrupt|
||RTI7_OVL_REQ_1|RTI7_OVERFLOW_LEVEL_1||||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 155 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **Table 4-59.** _**RTI**_ **DMA Requests** 

This table describes the module DMA requests. 

|**Module**<br>**Instance**|**Module DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|RTI0|RTI0_DMA_0|RTI0_DMA_REQ_0|EDMA Crossbar<br>(EDMA_XBAR)|Pulse|RTI0 DMA Request|
||RTI0_DMA_1|RTI0_DMA_REQ_1||||
||RTI0_DMA_2|RTI0_DMA_REQ_2||||
||RTI0_DMA_3|RTI0_DMA_REQ_3||||
|RTI1|RTI1_DMA_0|RTI1_DMA_REQ_0|||RTI1 DMA Request|
||RTI1_DMA_1|RTI1_DMA_REQ_1||||
||RTI1_DMA_2|RTI1_DMA_REQ_2||||
||RTI1_DMA_3|RTI1_DMA_REQ_3||||
|RTI2|RTI2_DMA_0|RTI2_DMA_REQ_0|||RTI2 DMA Request|
||RTI2_DMA_1|RTI2_DMA_REQ_1||||
||RTI2_DMA_2|RTI2_DMA_REQ_2||||
||RTI2_DMA_3|RTI2_DMA_REQ_3||||
|RTI3|RTI3_DMA_0|RTI3_DMA_REQ_0|||RTI3 DMA Request|
||RTI3_DMA_1|RTI3_DMA_REQ_1||||
||RTI3_DMA_2|RTI3_DMA_REQ_2||||
||RTI3_DMA_3|RTI3_DMA_REQ_3||||
|RTI4|RTI4_DMA_0|RTI4_DMA_REQ_0|||RTI4 DMA Request|
||RTI4_DMA_1|RTI4_DMA_REQ_1||||
||RTI4_DMA_2|RTI4_DMA_REQ_2||||
||RTI4_DMA_3|RTI4_DMA_REQ_3||||
|RTI5|RTI5_DMA_0|RTI5_DMA_REQ_0|||RTI5 DMA Request|
||RTI5_DMA_1|RTI5_DMA_REQ_1||||
||RTI5_DMA_2|RTI5_DMA_REQ_2||||
||RTI5_DMA_3|RTI5_DMA_REQ_3||||
|RTI6|RTI6_DMA_0|RTI6_DMA_REQ_0|||RTI6 DMA Request|
||RTI6_DMA_1|RTI6_DMA_REQ_1||||
||RTI6_DMA_2|RTI6_DMA_REQ_2||||
||RTI6_DMA_3|RTI6_DMA_REQ_3||||
|RTI7|RTI7_DMA_0|RTI7_DMA_REQ_0|||RTI7 DMA Request|
||RTI7_DMA_1|RTI7_DMA_REQ_1||||
||RTI7_DMA_2|RTI7_DMA_REQ_2||||
||RTI7_DMA_3|RTI7_DMA_REQ_3||||



156 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-60.** _**RTI**_ **Capture Events** 

This table describes the module capture events. 

|**Module**<br>**Instance**|**Module Capture**<br>**Event Input**|**Capture Event Source Signal**|**Source**|**Type**|**Description**|
|---|---|---|---|---|---|
|RTI0|RTI0_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>2|SoC Time<br>Sync Crossbar<br>(TIMESYNC_XBAR)|Pulse|RTI0 Counter Capture Input Event|
||RTI0_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>3||||
|RTI1|RTI1_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>4|||RTI1 Counter Capture Input Event|
||RTI1_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>5||||
|RTI2|RTI2_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>6|||RTI2 Counter Capture Input Event|
||RTI2_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>7||||
|RTI3|RTI3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>8|||RTI3 Counter Capture Input Event|
||RTI3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>9||||
|RT4|RTI3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>12|||RTI4 Counter Capture Input Event|
||RTI3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>13||||
|RTI5|RTI3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>14|||RTI5 Counter Capture Input Event|
||RTI3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>15||||
|RTI6|RTI3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>16|||RTI6 Counter Capture Input Event|
||RTI3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>17||||
|RTI7|RTI3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>18|||RTI7 Counter Capture Input Event|
||RTI3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>19||||



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

157 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

## **4.22 WWDT Integration** 

There are 4x WWDT modules integrated in the device. The diagram and tables below show the device integration details. 

**==> picture [496 x 361] intentionally omitted <==**

**Figure 4-26. WWDT Integration** 

The tables below summarize the integration of WWDT# (where # = 0, 1, 2, 3) in the device. 

Each WWDT# instance is supplied by dedicated WWDTCLK# mux. 

**Table 4-61.** _**WWDT**_ **Device Integration** 

This table describes the module device integration details. 

|**Module**<br>**Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|WWDT0|✓|VBUSP CORE Interconnect|
|WWDT1|✓|VBUSP CORE Interconnect|
|WWDT2|✓|VBUSP CORE Interconnect|
|WWDT3|✓|VBUSP CORE Interconnect|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

158 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **Table 4-62.** _**WWDT**_ **Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|WWDT0|WWDT0_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|WWDT0 VBUSP Interface<br>Clock|
||WWDT0_FCLK<br>(WWDT_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|WWDT0 Functional Clock|
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||PER_PLL_HSDIV0_CLKO<br>UT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCOSC (32KHz)|Internal 32 KHz RC<br>Oscillator (RCCLK_32K)|32 KHz||
|WWDT1|WWDT1_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|WWDT1 VBUSP Interface<br>Clock|
||WWDT1_FCLK<br>(WWDT_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|WWDT1 Functional Clock|
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||PER_PLL_HSDIV0_CLKO<br>UT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCOSC (32KHz)|Internal 32 KHz RC<br>Oscillator (RCCLK_32K)|32 KHz||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 159 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-62.** _**WWDT**_ **Clocks (continued)** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|WWDT2|WWDT2_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|WWDT2 VBUSP Interface<br>Clock|
||WWDT2_FCLK<br>(WWDT_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|WWDT2 Functional Clock|
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||PER_PLL_HSDIV0_CLKO<br>UT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCOSC (32KHz)|Internal 32 KHz RC<br>Oscillator (RCCLK_32K)|32 KHz||
|WWDT3|WWDT3_ICLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|WWDT3 VBUSP Interface<br>Clock|
||WWDT3_FCLK<br>(WWDT_CLK)|XTALCLK|External Crystal (XTAL)|25 MHz|WWDT3 Functional Clock|
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz||
|||PER_PLL_HSDIV0_CLKO<br>UT1|PLL_PER_CLK:<br>HSDIV0_CLKOUT1|192 MHz||
|||DPLL_CORE_HSDIV0_CL<br>KOUT1|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz||
|||RCOSC (10MHz)|Internal 10 MHz RC<br>Oscillator<br>(RCCLK10M)|10 MHz||
|||XTALCLK|External Crystal (XTAL)|25 MHz||
|||RCOSC (32KHz)|Internal 32 KHz RC<br>Oscillator (RCCLK_32K)|32 KHz||



160 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **Table 4-63.** _**WWDT**_ **Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|WWDT0|WWDT0_RST|Warm Reset<br>(MOD_G_RST)|RCM Reset Control Register +<br>Warm Reset Sources|WWDT0 Asynchronous Reset|
||WWDT0_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|WWDT0 Power-On Reset|
|WWDT1|WWDT1_RST|Warm Reset<br>(MOD_G_RST)|RCM Reset Control Register +<br>Warm Reset Sources|WWDT1 Asynchronous Reset|
||WWDT1_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|WWDT1 Power-On Reset|
|WWDT2|WWDT2_RST|Warm Reset<br>(MOD_G_RST)|RCM Reset Control Register +<br>Warm Reset Sources|WWDT2 Asynchronous Reset|
||WWDT2_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|WWDT2 Power-On Reset|
|WWDT3|WWDT3_RST|Warm Reset<br>(MOD_G_RST)|RCM Reset Control Register +<br>Warm Reset Sources|WWDT3 Asynchronous Reset|
||WWDT3_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|WWDT3 Power-On Reset|



**Table 4-64.** _**WWDT**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|WWDT0|WWDT0_NMI_REQ|ESM0_PLS_IN_0|ESM0|Pulse|WWDT0 Window Watchdog<br>Violation Non-Maskable Interrupt<br>(NMI) Event|
|||R5FSS0_0_VIM_128|R5FSS0_CORE0|||
|WWDT1|WWDT1_NMI_REQ|ESM0_PLS_IN_1|ESM0|Pulse|WWDT1 Non-Maskable Interrupt<br>(NMI) Event|
|||R5FSS0_1_VIM_128|R5FSS0_CORE1|||
|WWDT2|WWDT2_NMI_REQ|ESM0_PLS_IN_2|ESM0|Pulse|WWDT2 Non-Maskable Interrupt<br>(NMI) Event|
|||R5FSS1_0_VIM_128|R5FSS1_CORE0|||
|WWDT3|WWDT3_NMI_REQ|ESM0_PLS_IN_3|ESM0|Pulse|WWDT3 Non-Maskable Interrupt<br>(NMI) Event|
|||R5FSS1_1_VIM_128|R5FSS1_CORE1|||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 161 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-65.** _**RTI**_ **Capture Events** 

This table describes the module capture events. 

|**Module**<br>**Instance**|**Module Capture**<br>**Event Input**|**Capture Event Source Signal**|**Source**|**Type**|**Description**|
|---|---|---|---|---|---|
|WWDT0|WWDT0_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>2|SoC Time<br>Sync Crossbar<br>(TIMESYNC_XBAR)|Level|WWDT0 Counter Capture Input<br>Event|
||WWDT0_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>3||||
|WWDT1|WWDT1_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>4|||WWDT1 Counter Capture Input<br>Event|
||WWDT1_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>5||||
|WWDT2|WWDT2_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>6|||WWDT2 Counter Capture Input<br>Event|
||WWDT2_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>7||||
|WWDT3|WWDT3_CAPEVT_0|SoC_TIMESYNC_XBAROUT_<br>8|||WWDT3 Counter Capture Input<br>Event|
||WWDT3_CAPEVT_1|SoC_TIMESYNC_XBAROUT_<br>9||||



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

162 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.23 DCC Integration** 

There are 4x DCC modules integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [500 x 222] intentionally omitted <==**

**Figure 4-27. DCC Integration Diagram** 

The tables below summarize the device integration details of DCC. 

**Table 4-66. DCC Device Integration** 

This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|DCC0|✓|INFRA0 VBUSP Interconnect|
|DCC1|✓|INFRA0 VBUSP Interconnect|
|DCC2|✓|INFRA0 VBUSP Interconnect|
|DCC3|✓|INFRA0 VBUSP Interconnect|



**Table 4-67. DCC Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Descriptio**|
|---|---|---|---|---|---|
|DCC0|DCC0_CLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200MHz|DCC0 Interface Clock|
|DCC1|DCC1_CLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200MHz|DCC1 Interface Clock|
|DCC2|DCC2_CLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200MHz|DCC2 Interface Clock|
|DCC3|DCC3_CLK<br>(VBUSP_CLK)|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200MHz|DCC3 Interface Clock|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 163 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-68. DCC Resets** 

This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|DCC0|DCC0_RST|Warm Reset<br>(SYNC_RST_N)|RCM + Warm Reset Sources|Synchronous Assertion Reset, Active<br>Low|
|DCC1|DCC1_RST|Warm Reset<br>(SYNC_RST_N)|RCM + Warm Reset Sources|Synchronous Assertion Reset, Active<br>Low|
|DCC2|DCC2_RST|Warm Reset<br>(SYNC_RST_N)|RCM + Warm Reset Sources|Synchronous Assertion Reset, Active<br>Low|
|DCC3|DCC3_RST|Warm Reset<br>(SYNC_RST_N)|RCM + Warm Reset Sources|Synchronous Assertion Reset, Active<br>Low|



**Table 4-69. DCC Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|DCC0|DCC0_DONE|DCC0_DONE|ALL R5FSS<br>Cores|Level|DCC0 Done Interrupt|
||DCC0_ERROR|DCC0_ERROR|ESM|Level|DCC0 Error Interrupt|
|DCC1|DCC1_DONE|DCC1_DONE|ALL R5FSS<br>Cores|Level|DCC1 Done Interrupt|
||DCC1_ERROR|DCC1_ERROR|ESM|Level|DCC1 Error Interrupt|
|DCC2|DCC2_DONE|DCC2_DONE|ALL R5FSS<br>Cores|Level|DCC2 Done Interrupt|
||DCC2_ERROR|DCC2_ERROR|ESM|Level|DCC2 Error Interrupt|
|DCC3|DCC3_DONE|DCC3_DONE|ALL R5FSS<br>Cores|Level|DCC3 Done Interrupt|
||DCC3_ERROR|DCC3_ERROR|ESM|Level|DCC3 Error Interrupt|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

164 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.24 ESM Integration** 

Figure 4.27 provides a visual representation of the device integration details. 

**==> picture [500 x 274] intentionally omitted <==**

**Figure 4-28. ESM Integration Diagram** 

The tables below summarize the device integration details of ESM. 

**Table 4-70.** _**ESM**_ **Device Integration** 

This table describes the ESM device integration details. 

|**ESM Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|ESM|✓|INFRA0 VBUSP Interconnect|



**Table 4-71.** _**ESM**_ **Clocks** 

## This table describes the ESM clocking signals. 

|**ESM**<br>**Instance**|**ESM Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|ESM|ESM_VBUSCLK|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|ESM VBUSP Interface<br>Clock|
||ESM_CLK||||ESM Functional Clock|



**Table 4-72.** _**ESM**_ **Resets** 

## This table describes the ESM reset signals. 

|**ESM**<br>**Instance**|**ESM Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|ESM|ESM_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|ESM0 Asynchronous Reset|
||ESM_POR_RST|POR Reset<br>(MOD_POR_RST)|Device Power-On Reset|ESM0 Power-On Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 165 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-73.** _**ESM**_ **Interrupt Requests** 

This table describes the ESM interrupt requests. 

|**ESM**<br>**Instance**|**ESM Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|ESM|ESM_INT_CFG_LVL_<br>0|ESM_INT_CFG_LVL|ALL R5FSS Cores|Level|ESM Configuration Error Interrupt|
||ESM_INT_LOW_LVL_<br>0|ESM_INT_LOW_LVL|||ESM Low Priority Interrupt|
||ESM_INT_HIGH_LVL_<br>0|ESM_INT_HIGH_LVL|||ESM High Priority Interrupt|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

166 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.25 ECC Aggregator Integration** 

There is 1x ECC Aggregator integrated in the device. The diagram below provides a visual representation of the device integration details. 

**Figure 4-29. ECC Aggregator Integration** 

**==> picture [35 x 8] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>**----- End of picture text -----**<br>


**==> picture [435 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
SOC_ECCAGGR_CORR_LVL<br>ESM<br>SYS_CLK ECC_AGGR_CLK SOC_ECCAGGR_UNCORR_LVL<br>ECC_AGGR<br>ECC Protected Modules<br>FIFO/SRAM/..<br>Warm Reset Sources ECC_AGGR_WARMRESET<br>FIFO/SRAM/..<br>INFRA1 VBUSP INTERCONNECT<br>**----- End of picture text -----**<br>


The tables below summarize the device integration details of ECC Aggregator. 

**Table 4-74.** _**ECC Aggregator**_ **Device Integration** 

## This table describes the ECC Aggregator device integration details. 

|**ECC Aggregator**<br>**Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|ECC Aggregator0|✓|INFRA1 VBUSP Interconnect|



**Table 4-75.** _**ECC Aggregator**_ **Clocks** 

This table describes the ECC Aggregator clocking signals. 

|**ECC**<br>**Aggregator**<br>**Instance**|**ECC Aggregator Clock**<br>**Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|ECC<br>Aggregator0|ECC_AGGR_CLK|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|ECC Aggregator Interface<br>Clock|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 167 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-76.** _**ECC Aggregator**_ **Resets** 

This table describes the ECC Aggregator reset signals. 

|**ECC**<br>**Aggregator**<br>**Instance**|<br>**ECC Aggregator Reset**<br>**Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|ECC<br>Aggregator<br>0|ECC_AGGR_WARMRE<br>SET(VBUSP_RSTn)|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|ECC Aggregator0 Asynchronous<br>Reset|



**Table 4-77.** _**ECC Aggregator**_ **Event Requests** 

This table describes the ECC Aggregator interrupt requests. 

|**ECC**<br>**Aggregat**<br>**or**<br>**Instance**|**ECC Aggregator**<br>**Interrupt Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|ECC<br>Aggregato<br>r0|SOC_ECCAGGR_UN<br>CORR_LVL_0|SOC_ECCAGGR_UNCORR_L<br>VL_0|ESM|Level|ECC Aggregator0 uncorrectable<br>error event|
||SOC_ECCAGGR_CO<br>RR_LVL_0|SOC_ECCAGGR_CORR_LVL<br>_0|||ECC Aggregator0 correctable error<br>event|



**Table 4-78.** _**Device modules with ECC Aggregator**_ 

This table describes the ECC Aggregator interrupt requests. 

|**ECC Aggregator**|**ECC Aggregator Module instances**|
|---|---|
|ECC Aggregator0|L2OCRAM_BANK0|
||L2OCRAM_BANK1|
||L2OCRAM_BANK2|
||L2OCRAM_BANK3|
||L2OCRAM_BANK4|
||L2OCRAM_BANK5|
||MBOX_SRAM|
||TPTC00|
||TPTC01|



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

168 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.26 MCRC Integration** 

There is 1x MCRC integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [500 x 211] intentionally omitted <==**

**Figure 4-30. MCRC Integration** 

The tables below summarize the device integration details of MCRC# (where # = 1). 

**Table 4-79.** _**MCRC**_ **Device Integration** 

This table describes the MCRC device integration details. 

|**MCRC Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|MCRC0|✓|CORE VBUSM Interconnect|



**Table 4-80.** _**MCRC**_ **Clocks** 

This table describes the MCRC clocking signals. 

|**MCRC**<br>**Instance**|**MCRC Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|MCRC0|MCRC_CLK|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|MCRC0 Interface Clock|



**Table 4-81.** _**MCRC**_ **Resets** 

This table describes the MCRC reset signals. 

|**MCRC**<br>**Instance**|**MCRC Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|MCRC0|MCRC0_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|MCRC0 Asynchronous Reset|



**Table 4-82.** _**MCRC**_ **Interrupt Requests** 

This table describes the MCRC interrupt requests. 

|**MCRC**<br>**Instance**|**MCRC Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCRC0|MCRC0_INT_req|MCRC0_INT_req|ALL R5FSS<br>Cores|Level|MCRC0 Event Interrupt|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 169 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-83.** _**MCRC**_ **DMA Requests** 

This table describes the MCRC DMA requests. 

|**MCRC**<br>**Instance**|**MCRC DMA Event**|**Destination DMA Event Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|MCRC0|MCRC0_DMA_0|MCRC0_dma_req[0]|EDMA Crossbar<br>(DMA_XBAR)|Pulse|MCRC0 DMA Request|
||MCRC0_DMA_1|MCRC0_dma_req[1]||||
||MCRC0_DMA_2|MCRC0_dma_req[2]||||
||MCRC0_DMA_3|MCRC0_dma_req[3]||||



## **Note** 

For more information on the interconnects, see the System Interconnect chapter. 

For more information on power, reset, and clock management, see the corresponding sections within the Device Configuration chapter. 

For more information on the device interrupt controllers, see the Interrupt Controllers chapter. 

170 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.27 ICSSM_XBAR_INTROUTER Integration** 

The diagram below provides a visual representation of the device integration details. 

**==> picture [280 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
ICSSM interrupt<br>Router xBAR<br>MMR<br>Configuration<br>Port<br>MSS  SYSCLK<br>RCM SYSRSTn<br>Peripheral<br>ICSSM_xBAR_IN[59:0]<br> Interrupt<br>ICSSM<br>ICSSM_xBAR_OUT[15:0]<br>Interrupt<br>INFRA-0<br>Interconnect<br>**----- End of picture text -----**<br>


**Figure 4-31. ICSSM_XBAR_INTROUTER Integration** 

**Table 4-84.** _**ICSSM_XBAR_INTROUTER**_ **Device Integration** 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|ICSSM_XBAR|✓|VBUSP INFRA Interconnect|



**Table 4-85.** _**ICSSM_XBAR_INTROUTER**_ **Clocks** 

|**Module Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Source**|**Default**<br>**Freq**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|---|---|
|ICSSM_XBAR|CLK|SYSCLK|MSS_RCM||200 MHz||ICSSM_XBAR Functional<br>and Interface clock|
|**Table 4-86.****_ICSSM_XBAR_INTROUTER_ Resets**||||||||
|**Module Instance**|**Module Reset Input**|**Source Reset Signal**||**Source**||**Description**||
|ICSSM_XBAR|RST<br>|SYS_RST||RCM + Warm Reset Sources||ICSSM_XBAR Reset||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 171 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-87.** _**ICSSM_XBAR_INTROUTER**_ **Output Events** 

|**Module Instance**|**Module Sync Output **|**Destination Signal**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|ICSSM_XBAR|ICSSM_xbarout_0|PR1_SLV1_INTR_INTR[0]|ICSSM|Edge|Interrupt to ICSSM|
||ICSSM_xbarout_1|PR1_SLV1_INTR_INTR[1]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_2|PR1_SLV1_INTR_INTR[2]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_3|PR1_SLV1_INTR_INTR[3]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_4|PR1_SLV1_INTR_INTR[4]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_5|PR1_SLV1_INTR_INTR[5]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_6|PR1_SLV1_INTR_INTR[6]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_7|PR1_SLV1_INTR_INTR[7]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_8|PR1_SLV1_INTR_INTR[8]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_9|PR1_SLV1_INTR_INTR[9]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_10|PR1_SLV1_INTR_INTR[10]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_11|PR1_SLV1_INTR_INTR[11]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_12|PR1_SLV1_INTR_INTR[12]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_13|PR1_SLV1_INTR_INTR[13]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_14|PR1_SLV1_INTR_INTR[14]|ICSSM||Interrupt to ICSSM|
||ICSSM_xbarout_15|PR1_SLV1_INTR_INTR[15]|ICSSM||Interrupt to ICSSM|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

172 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-88.** _**ICSSM_XBAR_INTROUTER**_ **Input Events** 

|**Module Instance**|**Module Input**|**Interrupt Sources**|
|---|---|---|
|ICSSM_XBAR_INTROUTER|In_intr[0]|lin0_int_req[0]|
||In_intr[1]|lin0_int_req[1]|
||In_intr[2]|lin1_int_req[0]|
||In_intr[3]|lin1_int_req[1]|
||In_intr[4]|lin2_int_req[0]|
||In_intr[5]|lin2_int_req[1]|
||In_intr[6]|lin3_int_req[0]|
||In_intr[7]|lin3_int_req[1]|
||In_intr[8]|lin4_int_req[0]|
||In_intr[9]|lin4_int_req[1]|
||In_intr[10]|uart0_int_req|
||In_intr[11]|uart1_int_req|
||In_intr[12]|uart2_int_req|
||In_intr[13]|uart3_int_req|
||In_intr[14]|uart4_int_req|
||In_intr[15]|uart5_int_req|
||In_intr[16]|i2c0_int_req|
||In_intr[17]|i2c1_int_req|
||In_intr[18]|i2c2_int_req|
||In_intr[19]|i2c3_int_req|
||In_intr[20]|spi0_int_req|
||In_intr[21]|spi1_int_req|
||In_intr[22]|spi2_int_req|
||In_intr[23]|spi3_int_req|
||In_intr[24]|spi4_int_req|
||In_intr[25]|qspi_intr_req|
||In_intr[26]|tpcc_intg|
||In_intr[27]|tpcc_int0|
||In_intr[28]|tpcc_int1|
||In_intr[29]|tpcc_int2|
||In_intr[30]|tpcc_int3|
||In_intr[31]|tpcc_int4|
||In_intr[32]|tpcc_int5|
||In_intr[33]|tpcc_int6|
||In_intr[34]|tpcc_int7|
||In_intr[35]|tpcc_errint|
||In_intr[36]|tpcc_mpint|
||In_intr[37]|tptc_erint_0|
||In_intr[38]|tptc_erint_1|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

173 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-88.** _**ICSSM_XBAR_INTROUTER**_ **Input Events (continued)** 

|**Module Instance**|**Module Input**|**Interrupt Sources**|
|---|---|---|
|ICSSM_XBAR_INTROUTER|In_intr[39]|mcanss0_ext_ts_rollover_lvl_int|
||In_intr[40]|mcanss0_mcan_lvl_int_0|
||In_intr[41]|mcanss0_mcan_lvl_int_1|
||In_intr[42]|mcanss1_ext_ts_rollover_lvl_int|
||In_intr[43]|mcanss1_mcan_lvl_int_0|
||In_intr[44]|mcanss1_mcan_lvl_int_1|
||In_intr[45]|mcanss2_ext_ts_rollover_lvl_int|
||In_intr[46]|mcanss2_mcan_lvl_int_0|
||In_intr[47]|mcanss2_mcan_lvl_int_1|
||In_intr[48]|mcanss3_ext_ts_rollover_lvl_int|
||In_intr[49]|mcanss3_mcan_lvl_int_0|
||In_intr[50]|mcanss3_mcan_lvl_int_1|
||In_intr[51]|mailbox_PRU_req_0|
||In_intr[52]|mailbox_PRU_req_1|
||In_intr[53]|mailbox_PRU_ack_0|
||In_intr[54]|mailbox_PRU_ack_1|
||In_intr[55]|GPIO_xbarout_0|
||In_intr[56]|GPIO_xbarout_1|
||In_intr[57]|GPIO_xbarout_2|
||In_intr[58]|GPIO_xbarout_3|
||In_intr[59]|mcanss4_ext_ts_rollover_lvl_int|
||In_intr[60]|mcanss4_mcan_lvl_int_0|
||In_intr[61]|mcanss4_mcan_lvl_int_1|
||In_intr[62]|mcanss5_ext_ts_rollover_lvl_int|
||In_intr[63]|mcanss5_mcan_lvl_int_0|
||In_intr[64]|mcanss5_mcan_lvl_int_1|
||In_intr[65]|mcanss6_ext_ts_rollover_lvl_int|
||In_intr[66]|mcanss6_mcan_lvl_int_0|
||In_intr[67]|mcanss6_mcan_lvl_int_1|
||In_intr[68]|mcanss7_ext_ts_rollover_lvl_int|
||In_intr[69]|mcanss7_mcan_lvl_int_0|
||In_intr[70]|mcanss7_mcan_lvl_int_1|
||In_intr[71]|SPI5_intr|
||In_intr[72]|SPI6_intr|
||In_intr[73]|SPI7_intr|



174 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

## **4.28 GPIO_XBAR Integration** 

The diagram below provides a visual representation of the device integration details. 

**==> picture [405 x 203] intentionally omitted <==**

**----- Start of picture text -----**<br>
GPIO xBAR<br>MMR<br>Configuration<br>Port<br>gpio_xbar_edma_out[3:0]<br>gpio_xbar_icssm_out[3:0]<br>MSS  SYSCLK gpio_xbar_timesync_out[3:0]<br>RCM SYSRSTn gpio_xbar_r5ss0_vim1_out[3:0]gpio_xbar_r5ss0_vim0_out[3:0] initiatorsTo<br>gpio_xbar_r5ss1_vim0_out[3:0]<br>gpio_xbar_r5ss1_vim1_out[3:0]<br>gpio0_intr[143:0]<br>gpio1_intr[143:0]<br>gpio2_intr[143:0]<br>From gpio3_intr[143:0]<br>GPIOx<br>gpio0_bank_intr[8:0]<br>Interrupt gpio1_bank_intr[8:0]<br>gpio2_bank_intr[8:0]<br>gpio3_bank_intr[8:0]<br>{<br>INFRA-0<br>Interconnect<br>{<br>**----- End of picture text -----**<br>


**Figure 4-32. GPIO_XBAR Integration** 

**Table 4-89.** _**GPIO_XBAR**_ **Device Integration** 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|GPIO_TRIGGER_WRAP|✓|VBUSP INFRA Interconnect|



## **Table 4-90.** _**GPIO_XBAR**_ **Clocks** 

|**Module Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|GPIO_TRIGGER_WRAP|CLK|SYSCLK|MSS_RCM|200 MHz|GPIO_XBAR Functional<br>and Interface clock|



## **Table 4-91.** _**GPIO_XBAR**_ **Resets** 

|**Module Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|GPIO_TRIGGER_WRAP|RST|SYS_RST|RCM + Warm Reset Sources|GPIO_XBAR Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

175 

Copyright © 2025 Texas Instruments Incorporated 

_Module Integration_ 

www.ti.com 

**Table 4-92.** _**GPIO_XBAR**_ **Output Events** 

|**Module**<br>**Instance**|**Module Output**|**Destination Signal**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|GPIO_TRIGGER<br>_WRAP|OUTL_INTR[0]|gpio_xbar_edma_out[0]|EDMA_trigger_xbar_introuter|Edge|Interrupt to EDMA_XBAR|
||OUTL_INTR[1]|gpio_xbar_edma_out[1]|EDMA_trigger_xbar_introuter||Interrupt to EDMA_XBAR|
||OUTL_INTR[2]|gpio_xbar_edma_out[2]|EDMA_trigger_xbar_introuter||Interrupt to EDMA_XBAR|
||OUTL_INTR[3]|gpio_xbar_edma_out[3]|EDMA_trigger_xbar_introuter||Interrupt to EDMA_XBAR|
||OUTL_INTR[4]|gpio_xbar_icssm_out[0]|ICSSM_xbar_introuter||Interrupt to ICSSM|
||OUTL_INTR[5]|gpio_xbar_icssm_out[1]|ICSSM_xbar_introuter||Interrupt to ICSSM|
||OUTL_INTR[6]|gpio_xbar_icssm_out[2]|ICSSM_xbar_introuter||Interrupt to ICSSM|
||OUTL_INTR[7]|gpio_xbar_icssm_out[3]|ICSSM_xbar_introuter||Interrupt to ICSSM|
||OUTL_INTR[8]|gpio_xbar_timesync_out[0]|SOC_TIMESYNC1_XBAR||Interrupt to<br>SOC_TIMESYNC1_XBAR|
||OUTL_INTR[9]|gpio_xbar_timesync_out[1]|SOC_TIMESYNC1_XBAR||Interrupt to<br>SOC_TIMESYNC1_XBAR|
||OUTL_INTR[10]|gpio_xbar_timesync_out[2]|SOC_TIMESYNC1_XBAR||Interrupt to<br>SOC_TIMESYNC1_XBAR|
||OUTL_INTR[11]|gpio_xbar_timesync_out[3]|SOC_TIMESYNC1_XBAR||Interrupt to<br>SOC_TIMESYNC1_XBAR|
||OUTL_INTR[12]|gpio_xbar_timesync_out[4]|SOC_TIMESYNC1_XBAR||Interrupt to<br>SOC_TIMESYNC1_XBAR|
||OUTL_INTR[13]|gpio_xbar_timesync_out[5]|SOC_TIMESYNC1_XBAR||Interrupt to<br>SOC_TIMESYNC1_XBAR|
||OUTL_INTR[14]|gpio_xbar_vim0_out[0]|VIM0||Interrupt to VIM0|
||OUTL_INTR[15]|gpio_xbar_vim0_out[1]|VIM0||Interrupt to VIM0|
||OUTL_INTR[16]|gpio_xbar_vim0_out[2]|VIM0||Interrupt to VIM0|
||OUTL_INTR[17]|gpio_xbar_vim0_out[3]|VIM0||Interrupt to VIM0|
||OUTL_INTR[18]|gpio_xbar_vim1_out[0]|VIM1||Interrupt to VIM1|
||OUTL_INTR[19]|gpio_xbar_vim1_out[1]|VIM1||Interrupt to VIM1|
||OUTL_INTR[20]|gpio_xbar_vim1_out[2]|VIM1||Interrupt to VIM1|
||OUTL_INTR[21]|gpio_xbar_vim1_out[3]|VIM1||Interrupt to VIM1|
||OUTL_INTR[22]|gpio_xbar_vim2_out[0]|VIM2||Interrupt to VIM2|
||OUTL_INTR[23]|gpio_xbar_vim2_out[1]|VIM2||Interrupt to VIM2|
||OUTL_INTR[24]|gpio_xbar_vim2_out[2]|VIM2||Interrupt to VIM2|
||OUTL_INTR[25]|gpio_xbar_vim2_out[3]|VIM2||Interrupt to VIM2|
||OUTL_INTR[26]|gpio_xbar_vim3_out[0]|VIM3||Interrupt to VIM3|
||OUTL_INTR[27]|gpio_xbar_vim3_out[1]|VIM3||Interrupt to VIM3|
||OUTL_INTR[28]|gpio_xbar_vim3_out[2]|VIM3||Interrupt to VIM3|
||OUTL_INTR[29]|gpio_xbar_vim3_out[3]|VIM3||Interrupt to VIM3|



176 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Module Integration_ 

**Table 4-93.** _**GPIO_XBAR**_ **Input Events** 

|**Module Instance**|**Module Input**|**Interrupt Sources**|
|---|---|---|
|GPIO_TRIGGER_WRAP|gpio0_intr[143:0]|GPIO0_INTR[143:0]|
||gpio1_intr[143:0]|GPIO1_INTR[143:0]|
||gpio2_intr[143:0]|GPIO2_INTR[143:0]|
||gpio3_intr[143:0]|GPIO3_INTR[143:0]|
||gpio0_bank_intr[8:0]|GPIO0_BANK_INTR[8:0]|
||gpio1_bank_intr[8:0]|GPIO1_BANK_INTR[8:0]|
||gpio2_bank_intr[8:0]|GPIO2_BANK_INTR[8:0]|
||gpio3_bank_intr[8:0]|GPIO3_BANK_INTR[8:0]|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 177 

Copyright © 2025 Texas Instruments Incorporated 

