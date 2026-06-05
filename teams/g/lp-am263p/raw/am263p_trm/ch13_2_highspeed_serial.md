<!-- AM263P TRM | 13.2 High-speed Serial (CPSW) | 원본 p.1264-1374 | pymupdf4llm text+tables, images omitted -->

_Peripherals_ 

www.ti.com 

## **13.2 High-speed Serial Interfaces** 

This section describes the high-speed serial interfaces in the device. 

1264 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.2.1 Gigabit Ethernet Switch (CPSW)**_ 

This chapter describes the Gigabit Ethernet Switch (CPSW) subsystem in the device. 

**13.2.1.1 CPSW0 Overview** .....................................................................................................................................1266 **13.2.1.2 CPSW0 Environment** ...............................................................................................................................1269 **13.2.1.3 CPSW Integration** .................................................................................................................................... 1274 **13.2.1.4 CPSW0 Functional Description** ..............................................................................................................1277 **13.2.1.5 CPSW0 Programming Guide** .................................................................................................................. 1369 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1265 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.2.1.1 CPSW0 Overview** 

The 3-port Gigabit Ethernet Switch (CPSW0) subsystem provides Ethernet packet communication for the device and can be configured as an Ethernet switch. 

The device has one 3-port Gigabit Ethernet Switch subsystem named CPSW0 which supports two external Ethernet interfaces and one internal CPDMA host interface. 

Figure 13-83 shows the CPSW0 module overview. 

**==> picture [370 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>CPSW0<br>Reset Reset Signals Resets<br>Controllers<br>MII/RMII/RGMII<br>PLL Interface and Functional Clocks<br>Clocks<br>Controllers<br>MDIO<br>Interrupt Interrupt Signals<br>Interrupt Requests<br>Controllers<br>CBASS0<br>**----- End of picture text -----**<br>


**Figure 13-83. CPSW Module Overview** 

## _**13.2.1.1.1 CPSW0 Features**_ 

The 3-port CPSW0 subsystem provides the following features: 

- Two Ethernet ports (Port 1/Port 2) with selectable MII, RMII, and RGMII interfaces and a single internal Communications Port Programming Interface (CPPI) port (Port 0) 

- Synchronous 10/100/1000Mbit operation with Flexible logical FIFO-based packet buffer structure 

   - Full duplex mode supported in 10/100/1000Mbps modes 

   - Half-duplex mode supported in 10/100Mbps modes only 

- Maximum frame size of 2024 bytes 

- Management Data Input/Output (MDIO) module for PHY Management with Clause 45 support 

- Programmable interrupt control with selected interrupt pacing 

- One CPDMA CPPI 3.0 DMA Host Interface (Port 0) 

- Emulation Mode, Digital loopback, and FIFO loopback modes supported 

- RAM Error Detection and Correction (SECDED) 

- Eight priority level Quality Of Service (QOS) support (802.1p) 

- Support for Audio/Video Bridging (P802.1Qav/D6.0) 

- Support for IEEE 1588 Clock Synchronization (2008 Annex D, Annex E and Annex F) 

   - 

      - Timestamp module capable of time stamping external timesync events like generating Pulse-Per-Second outputs 

   - CPTS module that supports time stamping for IEEE1588 with support for 8 hardware push events and generation of compare output pulses 

- DSCP Priority Mapping (IPv4 and IPv6) 

- Energy Efficient Ethernet (EEE) support (802.3az) 

- Non-Blocking switch fabric with Flow Control Support (802.3x) and Wire rate switching (802.1d) 

1266 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- Time Sensitive Network (TSN) Support 

   - IEEE 802.1Qbv Enhancements for Scheduled Traffic 

- Address Lookup Engine (ALE) 

   - 512 ALE table entries with configurable number of addresses plus VLANs 

   - Wire rate lookup with spanning tree support 

   - Host controlled time-based aging and/or auto-aging 

   - L2 address lock and L2 filtering support 

   - MAC authentication (802.1x) and address blocking 

   - Receive/Destination-based Multicast and Broadcast rate limits 

   - OUI (Vendor ID) host accept/deny feature and Source port locking 

   - Configurable number of classifier/policers (32) 

   - VLAN support 

      - 802.1Q compliant 

         - Auto add port VLAN for untagged frames on ingress 

         - Auto VLAN removal on egress and auto pad to minimum frame size 

- EtherStats and 802.3 Stats Remote Network Monitoring (RMON) statistics gathering (per port statistics) 

- Support for Ethernet MAC transmit to MAC receive digital loopback mode 

## _**13.2.1.1.2 CPSW0 Not Supported Features**_ 

The following features are not supported by the CPSW0 switch: 

- Maximum frame size of 9600 bytes 

- GMII Mode 

- SGMII Mode 

- MACSEC 

- Synchronous Ethernet 

- Cut-thru switching 

- Time Sensitive Network Support 

   - IEEE P802.3br/D2.0 Interspersing Express Traffic 

## _**13.2.1.1.3 CPSW Terminology**_ 

|**AVB**|Audio Video Bridging|
|---|---|
|**AVBTP**|Audio Video Bridging Transport Protocol|
|**BCCA**|Best Controller Clock Algorithm|
|**CFI**|Canonical Format Indicator|
|**CPPI**|Communications Port Programming Interface|
|**CPSW**|Common Platform Switch|
|**DLR**|Device Level Ring|
|**DSCP**|Differentiated Services Code Point|
|**EEE**|Energy Efficient Ethernet|
|**EMAC**|Ethernet Media Access Control|
|**EOP**|End of Packet|
|**EOQ**|End of Queue|
|**IPG**|Inter-Packet Gap|
|**LPI**|Low Power Indicator|
|**MDIO**|Management Data Input/Output|
|**MOF**|Middle of Frame|
|**OUI**|Organizationally Unique Identifier|
|**PFC**|Priority based Flow Control|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1267 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

|**PTP**|Precision Time Protocol|
|---|---|
|**RMON**|Remote Monitoring|
|**RTCP**|RTP Control Protocol|
|**RTP**|Real-time Transport Protocol|
|**SCR**|Switched Central Resource|
|**SRP**|Stream Reservation Protocol|
|**TOS**|Type of Service|
|**VLAN**|Virtual Local Area Network|



_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1268 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.2.1.2 CPSW0 Environment** 

This section describes the CPSW0 external connections (environment). 

## _**13.2.1.2.1 CPSW0 MII Interface**_ 

Figure 13-84 shows a device with integrated EMAC and MDIO interfaced via a MII connection in a typical system. The EMAC module also includes a transmit error (MTXER) pin for Energy Efficient Ethernet operations. 

The individual EMAC and MDIO signals for the MII interface are summarized in Table 13-121. 

**==> picture [320 x 228] intentionally omitted <==**

**----- Start of picture text -----**<br>
MII_TXCLK<br>MII_TXD[3−0]<br>2.5 MHz<br>MII_TXEN<br>or<br>25 MHz<br>MII_COL<br>MII_CRS<br>Physical<br>System MII_RXCLK layer<br>core device Transformer<br>MII_RXD[3−0]<br>(PHY)<br>MII_RXDV<br>MII_RXER<br>RJ−45<br>MDIO_CLK<br>MDIO_D<br>EMAC<br>MDIO<br>**----- End of picture text -----**<br>


**Figure 13-84. Ethernet Configuration—MII Connections** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1269 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-121. EMAC and MDIO Signals for MII Interface** 

|**Signal**|**Type**|**Description**|
|---|---|---|
|MII_TXCLK<br>I<br>Transmit clock (MII_TXCLK). The transmit clock is a continuous clock that provides the timing reference for<br>transmit operations. The MII_TXD and MII_TXEN signals are tied to this clock. The clock is generated by<br>the PHY and is 2.5 MHz at 10 Mbps operation and 25 MHz at 100 Mbps operation.<br>MII_TXD[3-0]<br>O<br>Transmit data (MII_TXD). The transmit data pins are a collection of 4 data signals comprising 4 bits of<br>data. MTDX0 is the least-significant bit (LSB). The signals are synchronized by MII_TXCLK and valid when<br>MII_TXEN is asserted or de-asserted.<br>MII_TXEN<br>O<br>Transmit enable (MII_TXEN). The transmit enable signal indicates that the MII_TXD pins are generating<br>nibble data for use by the PHY. It is driven synchronously to MII_TXCLK.<br>MII_COL<br>I<br>Collision detected (MII_COL). In half-duplex operation, the MII_COL pin is asserted by the PHY when it<br>detects a collision on the network. It remains asserted while the collision condition persists. This signal is<br>not necessarily synchronous to MII_TXCLK nor MII_RXCLK.<br>In full-duplex operation, the MII_COL pin is used for hardware transmit flow control. Asserting the MII_COL<br>pin will stop packet transmissions; packets in the process of being transmitted when MII_COL is asserted<br>will complete transmission. The MII_COL pin should be held low if hardware transmit flow control is not<br>used.<br>MII_CRS<br>I<br>Carrier sense (MII_CRS). In half-duplex operation, the MII_CRS pin is asserted by the PHY when the<br>network is not idle in either transmit or receive. The pin is deasserted when both transmit and receive are<br>idle. This signal is not necessarily synchronous to MII_TXCLK nor MII_RXCLK.<br>In full-duplex operation, the MII_CRS pin should be held low.<br>MII_RXCLK<br>I<br>Receive clock (MII_RXCLK). The receive clock is a continuous clock that provides the timing reference for<br>receive operations. The MII_RXD, MII_RXDV, and MII_RXER signals are tied to this clock. The clock is<br>generated by the PHY and is 2.5 MHz at 10 Mbps operation and 25 MHz at 100 Mbps operation.<br>MII_RXD[3-0]<br>I<br>Receive data (MII_RXD). The receive data pins are a collection of 4 data signals comprising 4 bits of<br>data. MRDX0 is the least-significant bit (LSB). The signals are synchronized by MII_RXCLK and valid when<br>MII_RXDV is asserted or de-asserted.<br>MII_RXDV<br>I<br>Receive data valid (MII_RXDV). The receive data valid signal indicates that the MII_RXD pins are<br>generating nibble data for use by the EMAC. It is driven synchronously to MII_RXCLK.<br>MII_RXER<br>I<br>Receive error (MII_RXER). The receive error signal is asserted for one or more MII_RXCLK periods to<br>indicate that an error was detected in the received frame. This is meaningful only during data reception<br>when MII_RXDV is active.<br>MDIO_CLK<br>O<br>Management data clock (MDIO_CLK). The MDIO data clock is sourced by the MDIO module on the<br>system. It is used to synchronize MDIO data access operations done on the MDIO pin. The frequency of<br>this clock is controlled by the CLKDIV bits in the MDIO control register (CONTROL).<br>MDIO_D<br>I/O<br>Management data input output (MDIO_D). The MDIO data pin drives PHY management data into and out<br>of the PHY by way of an access frame consisting of start of frame, read/write indication, PHY address,<br>register address, and data bit cycles. The MDIO_D pin acts as an output for all but the data bit cycles at<br>which time it is an input for read operations.|||



## _**13.2.1.2.2 CPSW0 RMII Interface**_ 

Figure 13-85 shows a device with integrated EMAC and MDIO interfaced via a RMII connection in a typical system. The individual CPSW0 and MDIO signals for the RMII interface are summarized in Table 13-122. 

The CPSW0 module integrated in the device supports internal and external clock sources in RMII mode. Figure 13-85 shows the internal clock source for RMIIn_MHZ_50_CLK clock. It is 50 MHz clock source that is provided on the CLKOUT0 device pin. This clock has to be routed on the PCB to the RMII_REF_CLK device pin and the external PHY, RMII clock input. 

For more information, refer to either the IEEE 802.3 standard or ISO/IEC 8802-3:2000(E). 

1270 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [352 x 252] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>CLKOUT<br>CPSW0 PHY IC<br>RMIIn_TXD[1:0]<br>RMIIn_TX_EN<br>RMII_MHZ_50_CLK<br>TXP/TXN Transformer<br>and<br>RXP/RXN<br>RJ45<br>RMIIn_RXD[1:0]<br>RMIIn_CRS_DV<br>RMIIn_RX_ER<br>MDIO_MCLK<br>MDIO_MDIO<br>cpsw-002<br>EMAC<br>MDIO<br>**----- End of picture text -----**<br>


**==> picture [35 x 7] intentionally omitted <==**

**----- Start of picture text -----**<br>
n = 1 to 2<br>**----- End of picture text -----**<br>


**Figure 13-85. RMII Interface Typical Application (Internal Clock Source)** 

Figure 13-86 shows the external clock source for RMIIn_MHZ_50_CLK clock. In this case a 50 MHz clock is available on the PCB and it can be sourced from an oscillator or from the Ethernet PHY. This externally generated clock should be routed to both RMII_REF_CLK device pin and the external PHY, RMII clock input. 

**==> picture [352 x 260] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>CLKOUT<br>CPSW0 PHY IC<br>RMIIn_TXD[1:0]<br>RMIIn_TX_EN<br>RMII_MHZ_50_CLK<br>External Clock source TXP/TXN Transformer<br>(Oscillator or Ethernet PHY) RXP/RXN and<br>RJ45<br>RMIIn_RXD[1:0]<br>RMIIn_CRS_DV<br>RMIIn_RX_ER<br>MDIO_MCLK<br>MDIO_MDIO<br>cpsw-002a<br>n = 1 to 2<br>EMAC<br>MDIO<br>**----- End of picture text -----**<br>


**Figure 13-86. RMII Interface Typical Application (External Clock Source)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1271 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-122. RMII I/O Description** 

|**Signal**(2)|**Device Pin(s)**|**I/O**(1)|**Description**|
|---|---|---|---|
||||Transmit data. The transmit data pins are a collection of 2 bits of data.|
|RMIIn_TXD[1:0]|RMIIn_TXD[1:0]|O|TXD0 is the least-significant bit (LSB). The signals are synchronized by|
||||RMII_MHZ_50_CLK and valid only when RMIIn_TX_EN is asserted.|
||||RMII transmit enable. The transmit enable signal indicates that the|
|RMIIn_TX_EN|RMIIn_TX_EN|O|RMIIn_TXD[1:0] pins are generating data for use by the PHY.|
||||RMIIn_TX_EN is synchronous to RMII_MHZ_50_CLK.|
|RMII_MHZ_50_CLK|RMII_REF_CLK|I|RMII 50MHz reference clock.|
||||The reference clock is used to synchronize all RMII signals.|
||||RMII_MHZ_50_CLK must be continuous and fixed at 50 MHz.|
||||Receive data. The receive data pins are a collection of 2 bits of data.|
|RMIIn_RXD[1:0]|RMIIn_RXD[1:0]|I|RXD0 is the least-significant bit (LSB). The signals are synchronized by<br>RMII_MHZ_50_CLK and valid only when RMIIn_CRS_DV is asserted and|
||||RMIIn_RX_ER is de-asserted.|
|RMIIn_CRS_DV|RMIIn_CRS_DV|I|Carrier sense/receive data valid. Multiplexed signal between carrier sense<br>and receive data valid.|
|RMIIn_RX_ER|RMIIn_RX_ER|I|Receive error. The receive error signal is asserted to indicate that an error<br>was detected in the received frame.|
||||Management data clock (MDIO_MCLK). The MDIO data clock is sourced|
|MDIO_MCLK|MDIO0_MDC|O|by the MDIO module on the system. It is used to synchronize MDIO data|
||||access operations done on the MDIO0_MDIO data pin.|
||||MDIO data pin drives PHY management data into and out of the PHY by|
||||way of an access frame consisting of start of frame, read/write indication,|
|MDIO_MDIO|MDIO0_MDIO|I/O|PHY address, register address, and data bit cycles. The MDIO0_MDIO pin|
||||acts as an output for all but the data bit cycles at which time it is an input|
||||for read operations.|



(1) I = Input; O = Output 

(2) n 1 to 2 

## _**13.2.1.2.3 CPSW0 RGMII Interface**_ 

Figure 13-87 shows a device with integrated EMAC and MDIO interfaced via a RGMII connection in a typical system. The individual CPSW0 and MDIO signals for the RGMII interface are summarized in Table 13-123. 

**==> picture [356 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device<br>CPSW0 PHY IC<br>RGMIIn_TCLK<br>RGMIIn_TD[3:0]<br>RGMIIn_TCTL<br>A+/-<br>RJ45<br>B+/-<br>and<br>RGMIIn_RCLK C+/- Transformer<br>RGMIIn_RD[3:0] D+/-<br>RGMIIn_RCTL<br>MDIO_MCLK<br>MDIO_MDIO<br>cpsw-003<br>n = 1 to 2<br>EMAC<br>MDIO<br>**----- End of picture text -----**<br>


**Figure 13-87. RGMII Interface Typical Application** 

1272 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Table 13-123. RGMII I/O Description** 

|**Signal**(2)|**Device Pin(s)**|**I/O**(1)|**Description**|
|---|---|---|---|
||||The transmit data pins are a collection of 4 bits of data. TD0 is the least-|
|RGMIIn_TD[3:0]|RGMIIn_TD[3:0]|O|significant bit (LSB). The signals are valid only when RGMIIn_TCTL is|
||||asserted.|
|RGMIIn_TCTL|RGMIIn_TX_CTL|O|Transmit Control/enable. The transmit enable signal indicates that the TD pins<br>are generating data for use by the PHY.|
|RGMIIn_TCLK|RGMIIn_TXC|O|The transmit reference clock. The clock is 2.5 MHz at 10 Mbps operation, 25<br>MHz at 100 Mbps operation, and 125 MHz at 1000 Mbps of operation.|
|RGMIIn_RD[3:0]|RGMIIn_RD[3:0]|I|The receive data pins are a collection of 4 bits of data. RD0 is the least-<br>significant bit (LSB).|
||||The signals are valid only when RGMIIn_RX_CTL is asserted|
|RGMIIn_RCTL|RGMIIn_RX_CTL|I|The receive data valid/control signal indicates that the RD pins are nibble data<br>for use by the EMAC.|
||||The receive clock is a continuous clock that provides the timing reference for|
|RGMIIn_RCLK|RGMIIn_RXC|I|receive operations. The clock is generated by the PHY and is 2.5 MHz at 10<br>Mbps operation, 25 MHz at 100 Mbps operation, 125 MHz at 1000 Mbps of|
||||operation.|
||||Management data clock (MDIO_MCLK). The MDIO data clock is sourced by|
|MDIO_MCLK|MDIO0_MDC|O|the MDIO module on the system. It is used to synchronize MDIO data access|
||||operations done on the MDIO0_MDIO pin.|
||||The MDIO0_MDIO pin drives PHY management data into and out of the PHY|
||||by way of an access frame consisting of start of frame, read/write indication,|
|MDIO_MDIO|MDIO0_MDIO|I/O|PHY address, register address, and data bit cycles. The MDIO0_MDIO pin|
||||acts as an output for all but the data bit cycles at which time it is an input for|
||||read operations.|



(1) I = Input; O = Output 

(2) n 1 to 2 

## **Note** 

The Control Module registers assign the specific function to the device pads. For more information on Control Module settings, see Pad Configuration Registers in _Control Module (CTRL_MMR)_ and the device-specific Data sheet. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1273 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **13.2.1.3 CPSW Integration** 

There is 1x CPSW module integrated in the device. The diagram below provides a visual representation of the device integration details. 

**==> picture [395 x 296] intentionally omitted <==**

**----- Start of picture text -----**<br>
DEVICE CPSW<br>ICSSM CORE<br>C0_FH_PULSE_INTR_[0:3]C0_TH_PULSE_INTR_[0:3] R5FSS0-CORE0<br>C0_THRESH_PEND_INTR_[0:3]C0_MISC_PEND_INTR_[0:3] R5FSS0-CORE1<br>CPSW_STAT_PENDCPSW_HOST_PEND R5FSS1-CORE0<br>R5FSS1-CORE1<br>ESM0<br>ESM0_LVL_IN_45 CPSW0_ECC_SEC_PEND_0<br>ESM0_LVL_IN_46 CPSW0_ECC_DED_PEND_0<br>SoC CPTS<br>Time Sync XBAR CPSW_CPTS_COMP_0<br>CPSW_CPTS_GENF0_0<br>CPSW_CPTS_GENF1_0<br>CONTROLSS CPSW_CPTS_SYNC_0<br>Time Sync XBAR<br>CPPI_ICLK GMII_RFT_CLK /2<br>SYSCLK RGMII_MHZ_250_CLK DPLL_CORE_HSDIV_CLKOUT1<br>EXT_REFCLK RGMII_MHZ_50_CLK /10<br>WUCPUCLK RGMII_MHZ_5_CLK /100<br>CORE_PLL_HSDIV0_CLKOUT1<br>CORE_PLL_HSDIV0_CLKOUT0 CPTS_RFT_CLK<br>RCCLK10M<br>XTALCLK RMII1_MHZ_50_CLK<br>PER_PLL_HSDIV0_CLKOUT1 RMII1_REF_CLK<br>RCM<br>CPSW0_CLK_SRC_SEL RMII2_MHZ_50_CLK<br>RMII2_REF_CLK<br>CPSW0_RST_CTRL<br>Warm Reset Sources<br>**----- End of picture text -----**<br>


**Figure 13-88. CPSW Integration Diagram** 

The tables below summarize the device integration details of CPSW0. 

**Table 13-124.** _**CPSW0**_ **Device Integration** 

## This table describes the module device integration details. 

|**Module Instance**|**Device Allocation**|**SoC Interconnect**|
|---|---|---|
|CPSW0|✓|INFRA0 VBUSP Interconnect|



1274 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Table 13-125.** _**CPSW0**_ **Clocks** 

This table describes the module clocking signals. 

|**Module**<br>**Instance**|**Module Clock Input**|**Source Clock Signal**|**Source**|**Default**<br>**Freq**|**Description**|
|---|---|---|---|---|---|
|CPSW0|CPPI_ICLK|SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|CPSW0 Interface Clock|
||CPTS_RFT_CLK|XTACLK|External XTAL|25 MHz|CPSW0 Interface Clock|
|||EXT_REFCLK|External Reference Clock<br>(EXT_REFCLK)|100 MHz|CPSW0 Interface Clock|
|||SYS_CLK|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|200 MHz|CPSW0 Interface Clock|
|||DPLL_CORE_HSDIV0_CL<br>KOUT1 (not supported)|PLL_CORE_CLK:<br>HSDIV0_CLKOUT1|500 MHz|CPSW0 Interface Clock|
|||DPLL_CORE_HSDIV0_CL<br>KOUT0 (not supported)|PLL_CORE_CLK:<br>HSDIV0_CLKOUT0|400 MHz|CPSW0 Interface Clock|
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator (RCCLK10M)|10 MHz|CPSW0 Interface Clock|
|||XTALCLK|External XTAL|25 MHz|CPSW0 Interface Clock|
|||RCCLK10M|Internal 10 MHz RC<br>Oscillator (RCCLK10M)|10 MHz|CPSW0 Interface Clock|
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

**Table 13-126.** _**CPSW0**_ **Resets** 

## This table describes the module reset signals. 

|**Module**<br>**Instance**|**Module Reset Input**|**Source Reset Signal**|**Source**|**Description**|
|---|---|---|---|---|
|CPSW0|CPSW_RST|Warm Reset<br>(MOD_G_RST)|RCM + Warm Reset Sources|CPSW0 Asynchronous Reset|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1275 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-127.** _**CPSW0**_ **Interrupt Requests** 

This table describes the module interrupt requests. 

|**Module**<br>**Instance**|**Module Interrupt**<br>**Signal**|**Destination Interrupt Input**|**Destination**|**Type**|**Description**|
|---|---|---|---|---|---|
|CPSW0|C0_FH_PULSE_INT<br>R_[0:3]|C0_FH_PULSE_INTR|All R5FSS<br>Cores PRU-<br>ICSS Core|Level|FHost (from host to Ethernet)<br>paced pulse interrupt|
||C0_TH_PULSE_INT<br>R_[0:3]|C0_TH_PULSE_INTR|All R5FSS<br>CoresPRU-<br>ICSS Core|Level|THost (from Ethernet to host)<br>paced pulse interrupt|
||C0_TH_THRESH_P<br>ULSE_INTR_[0:3]|C0_TH_THRESH_PULSE_INTR|All R5FSS<br>CoresPRU-<br>ICSS Core|Level|THost (from Ethernet to host)<br>non-paced pulse interrupt|
||C0_MISC_PULSE_I<br>NTR_[0:3]|C0_MISC_PULSE_INTR|All R5FSS<br>CoresPRU-<br>ICSS Core|Level|Miscellaneous non-paced pulse<br>interrupt|
||CPSW_STAT_PEND|STAT_PEND|All R5FSS<br>Cores ICSSM<br>Core|Level|Statistics level interrupt|
||CPSW_HOST_PEN<br>D|HOST_PEND|All R5FSS<br>CoresPRU-<br>ICSS Core|Level|CPDMA host error level interrupt|
||CPSW_ECC_SEC_P<br>ULSE_INTR|ECC_SEC_PULSE_INTR|ESM|Level|ECC SEC pulse interrupt –<br>output from CPSW ECC module.|
||CPSW_ECC_DED_P<br>ULSE_INTR|ECC_DED_PULSE_INTR|ESM|Level|ECC DED pulse interrupt –<br>output from CPSW ECC module.|



**Table 13-128.** _**CPSW0**_ **Time Sync and Compare Event** 

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

For pin information on RGMII_ID_MODE and RGMII_REFCLK_SEL, see Register information and the corresponding section within the _Device Configuration_ chapter 

1276 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **13.2.1.4 CPSW0 Functional Description** 

The three-port switch Ethernet subsystem module (CPSW) is compliant to the IEEE Std 802.3 Specification. The CPPI CPDMA is compliant to the CPPI 3.0 and- CBA 3.1 specifications. The CPSW top level functional block diagram is shown in Figure 13-89. 

## _**13.2.1.4.1 Functional Block Diagram**_ 

The three-port Ethernet subsystem consists of: 

- CPSW Peripheral Core 

- One RGMIIn (where n = 1 to 2) interface module 

- One RMIIn (where n = 1 to 2) interface module 

- One MIIn (where n = 1 to 2) interface module 

- One Host Port 0 CPPI 3.0 CPDMA 

- CPSW subsystem control registers (REG) 

- One MDIO interface module 

- One Interrupt Controller module 

**==> picture [462 x 308] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPSW<br>CPSW<br>TH_VBUSP RGMIIn<br>CPRGMII<br>CPDMA<br>Interface FH_VBUSP<br>RMIIn<br>CPRMII<br>Interrupts INT<br>MIIn<br>CPMII<br>VBUS<br>Interface<br>Clocks<br>REG<br>MDIO<br>MDIO<br>Reset<br>Control<br>n = 1 to 2<br>**----- End of picture text -----**<br>


**Figure 13-89. CPSW Functional Block Diagram** 

## _**13.2.1.4.2 CPSW Ports**_ 

The Ethernet Subsystem has three ports. Port 0 is the Host port (internal to the Subsystem). Port 1 and 2 are the external ports connected to RGMII, RMII, MII interfaces as per the interface selected. 

Naming conventions followed in this chapter: 

- Port0 is referred to the CPDMA Host Port 

- Port1 and 2 are referred to the interfaces RGMII/RMII/MII 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1277 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.2.1 Interface Mode Selection**_ 

The three-port switch (CPSW) Ethernet Subsystem has one 10/100/1000 Ethernet port with selectable RMII, RGMII, and MII interfaces. 

The interface modes for all 2 Ethernet ports are selected by configuring the Ethernet interface mode selection bitfield (PORT_MODE_SEL) in the CTRLMMR_ENET1_CTRL and CTRLMMR_ENET2_CTRL registers. 

See the device-specific Data sheet for configuring the pin mux mode as per the interface selected. 

## _**13.2.1.4.3 Clocking**_ 

## _**13.2.1.4.3.1 Subsystem Clocking**_ 

CPSW clocking summary is shown in _CPSW Integration_ . 

## _**13.2.1.4.3.2 Interface Clocking**_ 

Data is transmitted and received with respect to the reference clocks of the interface pins. 

## _**13.2.1.4.3.2.1 RGMII Interface Clocking**_ 

RGMII_RXC, RGMII_TXC frequencies are: 

- 2.5 MHz at 10 Mbps 

- 25 MHz at 100 Mbps 

- 125 MHz at 1000 Mbps 

## **Note** 

RGMII has ID_MODE for TX internal delay that is fixed and cannot be changed. 

## _**13.2.1.4.3.2.2 RMII Interface Clocking**_ 

RMII interface clock RMII_50MHZ_CLK frequency is: 

- 50 MHz at 10 Mbps 

- 50 MHz at 100 Mbps 

For more details on RMII clocking, please see _CPSW0 Integration_ 

CTRLMMR_CLKOUT_CTRL[4]CLK_EN and CTRLMMR_CLKOUT_CTRL[0]CLK_SEL bits are used to enable and select the clock source for CLKOUT device pin. 

## _**13.2.1.4.3.2.3 MDIO Clocking**_ 

The MDIO clock is based on a divide-down of the interface (CPPI_ICLK) clock. The application software or driver must control the divide-down value. 

See the CPSW_MDIO_CONTROL_REG register for configuring the Clock Divider ([15-0]CLKDIV) value. 

## _**13.2.1.4.4 Software IDLE**_ 

The submodule software idle register bits enable CPSW operation to be completely or partially suspended by software control. There are two CPSW submodules that contain software idle register bits. Each of the two submodules may be individually commanded to enter the idle state. The idle state is entered at packet boundaries, and no further packet operations will occur on an idled submodule until the idle command is removed. The CPSW software idle inhibits packages from starting to be unloaded from each port switch FIFO, but packets already in process are unaffected. 

## _**13.2.1.4.5 Interrupt Functionality**_ 

CPSW Ethernet Subsystem has six interrupt outputs: 

- Cn_FH_PEND_INTR - FHost (from host to Ethernet) level interrupt 

- Cn_TH_PEND_INTR - THost (from Ethernet to host) level interrupt 

- Cn_TH_THRESH_PEND_INTR - THost (from Ethernet to host) non-paced level interrupt 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1278 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- Cn_MISC_PEND_INTR - Miscellaneous level interrupt 

   - ECC_SEC_PEND_INTR: ECC SEC level interrupt - from CPSW ECC module. This interrupt is also included in the C0_MISC_PEND_INTR if enabled or can be used separately if desired. 

   - ECC_DED_PEND_INTR: ECC DED level interrupt - from CPSW ECC module. This interrupt is also included in the C0_MISC_PEND_INTR if enabled or can be used separately. 

- STAT_PEND_INTR - Statistics level interrupt 

- HOST_PEND_INTR - CPDMA host error level interrupt 

## **Note** 

n = 0 to $num_cores-1 

## _**13.2.1.4.6 CPSW**_ 

The CPSW RMII/ RGMII interface is compliant to the IEEE Std 802.3 Specification. 

The CPSW contains two Ethernet port interfaces (Ethernet port 1 and 2), one CPPI packet streaming interface host port (port 0), Common Platform Time Sync (CPTS), ALE Engine and Statistics (STATS). A top-level block diagram of the CPSW is shown in Figure 13-90. 

**==> picture [500 x 313] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPSW<br>ALE<br>CPTS EVNT_PEND<br>CPSW_FIFO CPGMAC_SL RMII1/RGMII1<br>CPSW_FIFO CPGMAC_SL RMII2/RGMII2<br>CR<br>STATS STAT_PEND0<br>TH_VBUSP<br>CPSW_CPPI_FIFO CPDMA FH_VBUSP<br>SCR CPSW_REGS<br>**----- End of picture text -----**<br>


**Figure 13-90. CPSW Block Diagram** 

## _**13.2.1.4.6.1 Address Lookup Engine (ALE)**_ 

The Address Lookup Engine (ALE) is a sub-block of the CPSW Switch that processes all received packets and determines to which port(s) the packet should be forwarded. The ALE uses the incoming packet received port number, destination address, source address, length/type, and VLAN information to determine how the packet should be forwarded. The ALE outputs the port mask to the switch fabric that indicates the port(s) the packet should be forwarded to. The ALE is enabled when the ENABLE_ALE bit in the CPSW_ALE_CONTROL register is set. All packets are dropped when the ENABLE bit is cleared to 0. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1279 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.6.1.1 Error Handling**_ 

In normal operation, the Ethernet port modules are configured to drop received packages that contain errors (runt, frag, oversize, jabber, crc, alignment, code etc.). However, when the CPSW_PN_MAC_CONTROL_REG_k configuration bit(s) RX_CEF_EN, RX_CSF_EN, or RX_CMF_EN are set, received Ethernet packets with errors are transferred to the host. When the ALE receives a packet that contains errors (due to a set header error bit), or a MAC control frame and does not receive an abort, the packet will be forwarded only to the host port (port 0). Packets with errors that are forwarded to the host have no VLAN untagging or drop due to rate limiting. No ALE learning occurs on packets with errors or mac control frames. Learning is based on source address and lookup is based on destination address. Directed packets from the host are not learned, updated, or touched. 

## _**13.2.1.4.6.1.2 Bypass Operations**_ 

The ALE may be configured to operate in bypass mode by setting the ENABLE_BYPASS bit in the CPSW_ALE_CONTROL register. When in bypass mode, all Ethernet port received packets are forwarded only to the host port (port 0). In bypass mode, the ALE processes host port transmit packets the same as in normal mode. In general, packets would be directed by the host in bypass mode. 

## _**13.2.1.4.6.1.3 OUI Deny or Accept**_ 

The ALE may be configured to operate in OUI deny mode by setting the ENABLE_OUI_DENY bit in the CPSW_ALE_CONTROL register. When in OUI deny mode, a packet with a non-matching OUI source address will be dropped unless the destination address matches a supervisory table entry. When ENABLE_OUI_DENY bit is cleared, any packet source address matching an OUI address table entry will be dropped to the host unless the destination address matches with a supervisory address table entry. Broadcast packets will be dropped unless the broadcast address is entered into the table with the SUPER bit set. Unicast packets will be dropped unless the unicast address is in the table with BLOCK and SECURE both set (supervisory unicast packet). 

## _**13.2.1.4.6.1.4 Statistics Counting**_ 

The ALE sends per port statistics along with the frame routing to be counted in the CPSW statistics. There are multiple reasons that frames are dropped by the ALE. Each drop is counted in the CPSW statistics. For more information on ALE statistics refer to the _CPSW Network Statistics_ section. 

## _**13.2.1.4.6.1.5 Automotive Security Features**_ 

The ALE has many automotive security features that most enterprise switches do not require. 

- VLANs can be configured to not allow fragmented IPv4 frames. 

- VLANs can be configured to only allow up to four different IPv4 Protocols or IPv6. Next Header values, for example a VLAN can be configured to only allow TCP traffic in both IPv4 and IPv6 packets. 

- Drop invalid Source Addresses - drop Source Addresses with bit 40 set (Multicast/Broadcast indicator on Destination Addresses) 

- IEEE802.3 Length Check, drop frames that the IEEE802.3 Length is not contained within the frame. (Ether Types 0-1500) 

- Any Source Address can be secured to a port dropping any attempts from other ports to masquerade as a service. 

- Any source or destination address can be blocked. 

- Per Port or Per VLAN ingress checking, dropping traffic from non-member ports. 

- Classification, Policing on L2 and L3 information. 

## _**13.2.1.4.6.1.6 CPSW Switching Solutions**_ 

The host port can operate in many different modes as well depending on the functionality of the host. It is important to understand the modes and configure them properly. 

The ALE Table is designed to maximize the modes without compromise of the system functionality as well. 

1280 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.2.1.4.6.1.6.1 Basics of 3-port Switch Type**_ 

The 3-port switch has a host port that can operate in two fundamental modes. Bridge mode allows the host to extent the switched domain to another network like Wi-Fi or another multi-port switch. In this case the host must be able to see unknown unicast addresses so they can be broadcast to the other network. In Port mode the host need not see any unknown unicast traffic. The CPSW_ALE_CONTROL[8] EN_HOST_UNI_FLOOD bit determines the host mode for unknown unicast traffic. This bit should only be set if the user is bridging two or more networks together. 

The 3-port switch can operate like a two-port switch using the ALE table just for the host info, the only adder is now other VLANs need to be supported for transit traffic between the external ports. This can easily be done using the default VLAN rules so no ALE table entries are used. 

The 3-port switch can also operate in a fully authenticated environment where all network nodes are registered via the 802.1x based protocols. In this case the ALE table is filled with network node addresses that have been authenticated 

## _**13.2.1.4.6.1.7 VLAN Routing and OAM Operations**_ 

## _**13.2.1.4.6.1.7.1 InterVLAN Routing**_ 

The CPSW module supports wire rate InterVLAN routing for a small number of routes between the host port and MAC ports. The host will setup an ALE classifier with an associated egress operation that will cause the CPSW to perform those particular egress operations. The ALE can optionally check time to live validity as well. InterVLAN routing is not intended to be used for packet duplication, but instead allows the CPSW to route specific packets without host port involvement. 

The ALE uses the classifier along with an egress opcode, destination port mask and TTL check field to tell the CPSW how to manipulate the packet on the egress. The CPSW will use the opcode along with a per port operation table to process the packet. By setting up the CPSW egress operation table you can replace the DA, SA and VLAN along with optionally updating the time to live IP header field. This allows the CPSW to perform the routing function for a small set of routes without getting the local host/CPU involved. 

The Egress opcode will only be use for a classifier match and the packet would normally be sent only to the host. Instead of the host routing the packet, the CPSW has been configured to do the work instead. In the event that the time-to-live check feature is enabled and the time-to-live is either 0 or 1, the packet will not get the egress opcode and instead be sent to the host as if the route is not setup. This allows the host to deal with invalid TTL fields. 

## _**13.2.1.4.6.1.7.2 OAM Operations**_ 

The ALE supports OAM loopback on ports so that a remote link can be tested. TA port placed in OAM loopback will echo packets received on a port back to the port with an egress opcode of 0xFF which will swap the SA and DA on egress in the CPSW. 

Any supervisory packet will not be affected, so the spanning tree and other bridging functions are not affected. 

Packets will only be echoed if the port is in OAM loopback mode, the received packet in not a supervisor packet, the port is in a forwarding state, the packet received DA!=SA, and there are no errors in the packet. 

When a port is in OAM loopback the port will not egress traffic from other ports, no address for loop backed traffic will be learned if enabled. Any packet received on the OAM loopback port with an error will be processed as if the port is not in OAM. That is if the host has enabled copy errored frames the errored frames will be sent to the host instead. 

## _**13.2.1.4.6.1.8 Supervisory packets**_ 

Multicast supervisory packets are designated by the SUPER bit in the table entry. Unicast supervisory packets are indicated when BLOCK and SECURE are both set. Supervisory packets are not dropped due to rate limiting, OUI, or VLAN processing. The purpose of supervisory packets is to allow packets that would be otherwise blocked to be forwarded for special purposes. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1281 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.6.1.9 Address Table Entry**_ 

The ALE table contains multiple table entry types. Each table entry represents a free entry, an address, a VLAN, an address/VLAN pair, or an OUI address. Software should ensure that there are no double address entries in the table. The double entry used would be indeterminate. Reserved table bits must be written with zeroes. 

Source Address learning occurs for packets with a unicast, multicast or broadcast destination address and a unicast or multicast (including broadcast) source address. Multicast source addresses have the group bit (bit 40) cleared before ALE processing begins, changing the multicast source address to a unicast source address. A multicast address of all ones is the broadcast address which may be added to the table. A learned unicast source address is added to the table with the following control bits: 

**Table 13-129. Learned Address Control Bits** 

|**Bit(s)**||**Value**||
|---|---|---|---|
||Ageable||1|
||Touch||1|
||BLOCK||0|
||SECURE||0|



If a received packet has a source address that is equal to the destination address then the following occurs: 

- The address is learned if the address is not found in the table. 

- The address is updated if the address is found. 

- The packet is dropped. 

## **Table Entry Type** 

00 - Free Entry 

01 - Address Entry : unicast or multicast determined by destination **address bit 40.** 

10 - VLAN entry 

11 - VLAN Address Entry : unicast or multicast determined by **address bit 40.** 

## _**13.2.1.4.6.1.9.1 Free Table Entry**_ 

## **Table 13-130. Free Table Entry Bit Values** 

|70:62|61:60|59:0|
|---|---|---|
|Reserved|ENTRY_TYPE (00)|Reserved|



## **Table Entry Type (ENTRY_TYPE)** 

## 00: Free entry 

## _**13.2.1.4.6.1.9.2 OUI Unicast Address Table Entry**_ 

## **Table 13-131. OUI Unicast Address Table Entry Bit Values** 

|70:64|63:62|61:60|59:48|47:24|23:0|
|---|---|---|---|---|---|
|Reserved|UNICAST_TYPE (10)|ENTRY_TYPE (01)|Reserved|UNICAST_OUI|Reserved|



## **Unicast Type (UNICAST_TYPE)** 

This field indicates the type of unicast address the table entry contains. 

00 - Unicast address that is not ageable. 

- 01 - Ageable unicast address that has not been touched. 

10 - OUI address - lower 24-bits are don't cares (not ageable). 

1282 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

11 - Ageable unicast address that has been touched. 

## **Table Entry Type (ENTRY_TYPE)** 

Address entry. Unicast or multicast determined by address bit 40. 

## 01: Address entry. Unicast or multicast determined by address bit 40. 

## **Packet Address (UNICAST_OUI)** 

For an OUI address, only the upper 24-bits of the address are used in the source or destination address lookup. 

## _**13.2.1.4.6.1.9.3 Unicast Address Table Entry (Bit 40 == 0)**_ 

**Table 13-132. Unicast Address Table Entry Bit Values** 

|70:69|68|67:66|65|64|63|62|61:60|59:48|47:0|
|---|---|---|---|---|---|---|---|---|---|
|RESERVED|TRUNK|PORT_NU|BLOCK|SECURE|TOUCH|AGEABLE|ENTRY_TY|RESERVE|UNICAST_|
|||MBER|||||PE (3h)|D|ADDRESS|



## **Trunk Indicator (TRUNK)** 

0h = The port bits in the entry are the port number 

1h = The port bits in the entry are the trunk number 

## **Port Number (PORT_NUMBER)** 

This field indicates the port number (not port mask) that the packet with a unicast destination address may be forwarded to. Packets with unicast destination addresses are forwarded only to a single port (but not the receiving port).] 

## **Block (BLOCK)** 

The block bit indicates that a packet with a matching source or destination address should be dropped (block the address). 

0h = Address is not blocked. 

1h = Drop a packet with a matching source or destination address (secure must be zero) 

If block and secure are both set, then they no longer mean block and secure. When both are set, the block and secure bits indicate that the packet is a unicast supervisory (super) packet and they determine the unicast forward state test criteria. If both bits are set then the packet is forwarded if the receive port is in the Forwarding/ Blocking/Learning state. If both bits are not set then the packet is forwarded if the receive port is in the Forwarding state. 

## **Secure (SECURE)** 

This bit indicates that a packet with a matching source address should be dropped if the received port number is not equal to the table entry PORT_NUMBER. 

0h = Received port number is a don't care. 

1h = Drop the packet if the received port is not the secure port for the source address and do not update the address (block must be zero) 

## **Touch Indicator (TOUCH)** 

Only valid when AGEABLE it a 1h. 

0h = Ageable unicast address has not been touched 

1h = Ageable unicast address that has been touched 

## **Ageable (AGEABLE)** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1283 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

This bit indicates that the address is ageable. 

- 0h = Unicast address that is not ageable 

- 1h = Unicast address that is ageable 

## **Table Entry Type (ENTRY_TYPE)** 

Address entry. Unicast or multicast determined by address bit 40. 

- 01: Address entry. Unicast or multicast determined by address bit 40. 

## **Packet Address (UNICAST_ADDRESS)** 

This is the 48-bit packet MAC address. All 48-bits are used in the lookup. 

## _**13.2.1.4.6.1.9.4 Multicast Address Table Entry (Bit 40==1)**_ 

**Table 13-133. Multicast Address Table Entry Bit Values** 

|70:69|68:66|65|64|63:62|61:60|59:48|47:0|
|---|---|---|---|---|---|---|---|
|RESERVED|PORT_MASK|SUPER|IGNMBITS|FWDSTLVL|ENTRY_TYPE|RESERVED|MULTICAST_A|
||||||(1h)||DDRESS|



## **Port Mask(2:0) (PORT_MASK)** 

This 3-bit field is the port bit mask that is returned with a found multicast destination address. There may be multiple bits set indicating that the multicast packet may be forwarded to multiple ports (but not the receiving port). 

## **Supervisory Packet (SUPER)** 

When set, this field indicates that the packet with a matching multicast destination address is a supervisory packet. 

- 0: Non-supervisory packet 

- 1: Supervisory packet 

## **Ignore Multicast Bits (IGNMBITS)** 

Indication that the Multicast Address has ignored bits. 

## **Forward State Level (FWDSTLVL)** 

Indicates the port state(s) required for the received port on a destination address lookup in order for the multicast packet to be forwarded to the transmit port(s). 

A transmit port must be in the Forwarding state in order to forward the packet. If the transmit port_mask has multiple set bits then each forward decision is independent of the other transmit port(s) forward decision. 

- 0h = Forwarding 

- 1h = Blocking/Forwarding/Learning 

- 2h = Forwarding/Learning 

## 3h = Forwarding 

The forward state test returns a true value if both the RX and TX ports are in the required state. 

## **Table Entry Type (ENTRY_TYPE)** 

Address entry type. Unicast or multicast determined by address bit 40. 

- 01: Address entry. Unicast or multicast determined by address bit 40. 

## **Packet Address (MULTICAST_ADDRESS)** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1284 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

This is the 48-bit packet MAC address. For an OUI address, only the upper 24-bits of the address are used in the source or destination address lookup. Otherwise, all 48-bits are used in the lookup. 

## _**13.2.1.4.6.1.9.5 VLAN/Unicast Address Table Entry (Bit 40 == 0)**_ 

## **Table 13-134. Unicast Address Table Entry Bit Values** 

|70:69|68|67:66|65|64|63|62|61:60|59:48|47:0|
|---|---|---|---|---|---|---|---|---|---|
|RESERVED|TRUNK|PORT_NU|BLOCK|SECURE|TOUCH|AGEABLE|ENTRY_TY|VLAN_ID|UNICAST_|
|||MBER|||||PE (3h)||ADDRESS|



## **Trunk Indicator (TRUNK)** 

0h = The port bits in the entry are the port number 

- 1h = The port bits in the entry are the trunk number 

## **Port Number (PORT_NUMBER)** 

This field indicates the port number (not port mask) that the packet with a unicast destination address may be forwarded to. Packets with unicast destination addresses are forwarded only to a single port (but not the receiving port).] 

## **Block (BLOCK)** 

The block bit indicates that a packet with a matching source or destination address should be dropped (block the address). 

0h = Address is not blocked. 

1h = Drop a packet with a matching source or destination address (secure must be zero) 

If block and secure are both set, then they no longer mean block and secure. When both are set, the block and secure bits indicate that the packet is a unicast supervisory (super) packet and they determine the unicast forward state test criteria. If both bits are set then the packet is forwarded if the receive port is in the Forwarding/ Blocking/Learning state. If both bits are not set then the packet is forwarded if the receive port is in the Forwarding state. 

## **Secure (SECURE)** 

This bit indicates that a packet with a matching source address should be dropped if the received port number is not equal to the table entry PORT_NUMBER. 

0h = Received port number is a don't care. 

1h = Drop the packet if the received port is not the secure port for the source address and do not update the address (block must be zero) 

## **Touch Indicator (TOUCH)** 

Only valid when AGEABLE is a 1h. 

0h = Ageable unicast address has not been touched 

1h = Ageable unicast address that has been touched 

## **Ageable (AGEABLE)** 

This bit indicates that the address is ageable. 

0h = Unicast address that is not ageable 

1h = Unicast address that is ageable 

## **Table Entry Type (ENTRY_TYPE)** 

Address entry. Unicast or multicast determined by address bit 40. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1285 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

3h: VLAN address entry. Unicast or multicast determined by address bit 40. 

## **VLAN ID (VLAN_ID)** 

The unique identifier for VLAN identification. This is the 12-bit VLAN ID. 

## **Packet Address (UNICAST_ADDRESS)** 

This is the 48-bit packet MAC address. All 48-bits are used in the lookup. 

## _**13.2.1.4.6.1.9.6 VLAN/Multicast Address Table Entry (Bit 40==1)**_ 

## **Table 13-135. VLAN/Multicast Address Table Entry Bit Values** 

|70:69|68:66|65|64|63:62|61:60|59:48|47:0|
|---|---|---|---|---|---|---|---|
|RESERVED|PORT_MASK|SUPER|IGNMBITS|FWDSTLVL|ENTRY_TYPE|VLAN_ID|MULTICAST_AD|
||||||(11)||DRESS|



## **Port Mask(2:0) (PORT_MASK)** 

This 3-bit field is the port bit mask that is returned with a found multicast destination address. There may be multiple bits set indicating that the multicast packet may be forwarded to multiple ports (but not the receiving port). 

## **Supervisory Packet (SUPER)** 

When set, this field indicates that the packet with a matching multicast destination address is a supervisory packet. 

## 0: Non-supervisory packet 

## 1: Supervisory packet 

## **Ignore Multicast Bits (IGNMBITS)** 

Indication that the Multicast Address has ignored bits. 

## **Forward State Level (FWDSTLVL)** 

Indicates the port state(s) required for the received port on a destination address lookup in order for the multicast packet to be forwarded to the transmit port(s). 

A transmit port must be in the Forwarding state in order to forward the packet. If the transmit port_mask has multiple set bits then each forward decision is independent of the other transmit port(s) forward decision. 

0h = Forwarding 

- 1h = Blocking/Forwarding/Learning 

- 2h = Forwarding/Learning 

## 3h = Forwarding 

The forward state test returns a true value if both the RX and TX ports are in the required state. 

## **Table Entry Type (ENTRY_TYPE)** 

Address entry type. Unicast or multicast determined by address bit 40. 

- 11: VLAN address entry. Unicast or multicast determined by address bit 40. 

## **VLAN ID (VLAN_ID)** 

The unique identifier for VLAN identification. This is the 12-bit VLAN ID. 

## **Packet Address (MULTICAST_ADDRESS)** 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1286 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

This is the 48-bit packet MAC address. For an OUI address, only the upper 24-bits of the address are used in the source or destination address lookup. Otherwise, all 48-bits are used in the lookup. 

## _**13.2.1.4.6.1.9.7 Inner VLAN Table Entry**_ 

**Table 13-136. Inner VLAN Table Entry** 

|70:69|68:66<br>65||64:62|61:60|59:48|47|46:39|38:36|
|---|---|---|---|---|---|---|---|---|
|RESERVED|NO_LEARN_M<br>VLAN_FORCE||0h|ENTRY_TYPE|VLAN_ID|NOFRAG|RESERVED|REG_MCAST_F|
||ASK<br>_INGRESS_C|||(2h)||||LOOD_INDEX|
||HECK||||||||
||||||||||
|35:27|26:24||23|22:15||14:12|11:3|2:0|
|RESERVED|FORCE_UNTAGGE|LMTNXTHDR||RESERVED|UREGMSK||RESERVED|VLAN_MEMBER_LI|
||D_EGRESS|||||||ST|



## **No Learn Mask (NO_LEARN_MASK)** 

When a bit is set in this mask, a packet with an unknown source address received on the associated port will not be learned (i.e. When a VLAN packet is received and the source address is not in the table, the source address will not be added to the table). 

## **VLAN Force Ingress Check (VLAN_FORCE_INGRESS_CHECK)** 

If the receive port is not a member of this VLAN then the packet is dropped. This is similar to the Iy_REG_Py_VID_INGRESS_CHECK bit in the CPSW_Iy_ALE_PORTCTL0_y registers except this check is for this VLAN only (not all VLANs). 

## **Table Entry Type (ENTRY_TYPE)** 

2h: VLAN entry 

## **VLAN ID (VLAN_ID)** 

The unique identifier for VLAN identification. This is the 12-bit VLAN ID. 

## **(NOFRAG)** 

VLAN No IPv4 Fragmented frames Control - Causes IPv4 fragmented IP frames to be dropped. 

## **Registered Multicast Flood Index (REG_MCAST_FLOOD_INDEX)** 

This field indicates which port(s) are the registered multicast flood mask. 

## **Force Untagged Packet Egress (FORCE_UNTAGGED_EGRESS)** 

This field causes the packet VLAN tag to be removed on egress for the specified port(s) (except on port 0). 

## **VLAN Limit Next Header Control (LMTNXTHDR)** 

This bit causes frames to be dropped if the Protocol/Nxt Header does not match the CPSW_ALE_NXT_HDR register values. 

## **VLAN Unregister Multicast Mask (UREGMSK)** 

This field indicates which port(s) are the unregistered multicast flood mask. 

## **VLAN Member List (VLAN_MEMBER_LIST)** 

This field indicates which port(s) are members of the associated VLAN. One bit per port. 

## _**13.2.1.4.6.1.9.8 Outer VLAN Table Entry**_ 

## **Table 13-137. Outer VLAN Table Entry** 

70:69 68:66 65 64:62 61:60 59:48 47 46:39 38:36 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1287 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## **Table 13-137. Outer VLAN Table Entry (continued)** 

|RESERVED|NO_LEARN_M<br>VLAN_FORCE|NO_LEARN_M<br>VLAN_FORCE|2h|ENTRY_TYPE|VLAN_ID|NOFRAG|RESERVED|REG_MCAST_F|
|---|---|---|---|---|---|---|---|---|
||ASK<br>_INGRESS_C|||(2h)||||LOOD_INDEX|
||HECK||||||||
||||||||||
|35:27|26:24||23|22:15||14:12|11:3|2:0|
|RESERVED|FORCE_UNTAGGE|LMTNXTHDR||RESERVED|UREGMSK||RESERVED|VLAN_MEMBER_LI|
||D_EGRESS|||||||ST|



## **No Learn Mask (NO_LEARN_MASK)** 

When a bit is set in this mask, a packet with an unknown source address received on the associated port will not be learned (i.e. When a VLAN packet is received and the source address is not in the table, the source address will not be added to the table). 

## **VLAN Force Ingress Check (VLAN_FORCE_INGRESS_CHECK)** 

If the receive port is not a member of this VLAN then the packet is dropped. This is similar to the Iy_REG_Py_VID_INGRESS_CHECK bit in the CPSW_Iy_ALE_PORTCTL0_y registers except this check is for this VLAN only (not all VLANs). 

## **Table Entry Type (ENTRY_TYPE)** 

2h: VLAN entry 

## **VLAN ID (VLAN_ID)** 

The unique identifier for VLAN identification. This is the 12-bit VLAN ID. 

## **(NOFRAG)** 

VLAN No IPv4 Fragmented frames Control - Causes IPv4 fragmented IP frames to be dropped. 

## **Registered Multicast Flood Index (REG_MCAST_FLOOD_INDEX)** 

Index into CPSW_ALE_MSK_MUX0 to CPSW_Ix_ALE_MSK_MUXx register array that is used to create the registered multicast flood mask. 

## **Force Untagged Packet Egress (FORCE_UNTAGGED_EGRESS)** 

This field causes the packet VLAN tag to be removed on egress for the specified port(s) (except on port 0). 

## **VLAN Limit Next Header Control (LMTNXTHDR)** 

This bit causes frames to be dropped if the Protocol/Nxt Header does not match the CPSW_ALE_NXT_HDR register values. 

## **VLAN Unregister Multicast Mask (UREGMSK)** 

This field indicates which port(s) are the unregistered multicast flood mask. 

## **VLAN Member List (VLAN_MEMBER_LIST)** 

This field indicates which port(s) are members of the associated VLAN. One bit per port. 

## _**13.2.1.4.6.1.9.9 EtherType Table Entry**_ 

**Table 13-138. EtherType Table Entry** 

|70:65|64:62|61:60|59:16|15:0|
|---|---|---|---|---|
|RESERVED|4h|ENTRY_TYPE (2h)|RESERVED|ETHERTYPE|



## **Table Entry Type (ENTRY_TYPE)** 

2h: VLAN entry 

## **Ether Type (ETHERTYPE)** 

1288 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## 16-bits Ether Type field. 

## _**13.2.1.4.6.1.9.10 IPv4 Table Entry**_ 

## **Table 13-139. IPv4 Table Entry** 

|70|69:65|64:62|61:60|59:32|31:0|
|---|---|---|---|---|---|
|RESERVED|IGNBITS|6h|ENTRY_TYPE (2h)|RESERVED|IPV4ADR|



## **Ignore Bits (IGNBITS)** 

Indicates the number of lower address bits to be ignored starting at bit zero. Ignored bits must be zero value in the table entry. 

## **Table Entry Type (ENTRY_TYPE)** 

## 2h: VLAN entry 

## **IPv4 Address (IPV4ADR)** 

32-bit IPv4 Address. Any ignored bits must be zero value in the table entry. 

## _**13.2.1.4.6.1.9.11 IPv6 Table Entries**_ 

## **Note** 

IPV6 table address entries operate differently than all other table entry types. IPv6 table entries have a high entry(IPv6 Table Entry High) concatenated with a low entry(IPv6 Table Entry). For a given IPv6 address, the IPv6 Entry High must have an table index value equal to the IPv6 Entry Low table index value plus 0x40 (for the ALE ramdepth of 64). As an example, an IPv6 Entry Low designated by a table index of 0x05 would have its respective IPv6 Entry High located at table index 0x05 + 0x40. 

## _**13.2.1.4.6.1.9.11.1 IPv6 Table Entry High**_ 

## **Table 13-140. IPv6 Table Entry High** 

|70:64|63|62|61:60|59:0|
|---|---|---|---|---|
|IGNBITS|RESERVED|(1h)|ENTRY_TYPE (2h)|IPV6ADR[127:68]|



## **Ignore Bits (IGNBITS)** 

Indicates the number of lower address bits to be ignored starting at bit zero. Ignored bits must be zero value in the table entry. 

## **Table Entry Type (ENTRY_TYPE)** 

2h: VLAN entry 

## **IPv6 Address - upper 60 bits (IPV6ADR[127:68])** 

Upper 60 bits of the 128-bit IPv6 Address. This address is split into three fields in the IPv6 High and IPv6 Low table entry. Any ignored bits must be zero in the table entries. 

## _**13.2.1.4.6.1.9.11.2 IPv6 Table Entry Low**_ 

## **Table 13-141. IPv6 Table Entry Low** 

|70:63|62|61:60|59:0|
|---|---|---|---|
|IPV6ADR[67:60]|1h|ENTRY_TYPE (2h)|IPV6ADR[59:0]|



## **Table Entry Type (ENTRY_TYPE)** 

## 2h: VLAN entry 

## **IPv6 Address - upper 8 bits (IPV6ADR[67:60])** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1289 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

Bits [67:60] of the 128-bit IPv6 Address. This address is split into three fields in the IPv6 High and IPv6 Low table entry. Any ignored bits must be zero in the table entries. 

## **IPv6 Address - lower 60 bits (IPV6ADR[59:0])** 

Lower 60 bits of the 128-bit IPv6 Address. This address is split into three fields in the IPv6 High and IPv6 Low table entry. Any ignored bits must be zero in the table entries. 

## _**13.2.1.4.6.1.10 Multicast Address**_ 

Multicast addresses are addresses with bit 40 set. Only destination addresses can be Multicast addresses. The group bit (bit 40) of the source address is reserved in the IEEE standard. 

A multicast address of all ones is the broadcast address which can be added to the lookup table if forwarding of broadcast packets need be modified. 

## _**13.2.1.4.6.1.10.1 Multicast Ranges**_ 

Added IgnMbits to indicate at least one bit of the multicast address is ignored. Up to 10 bits of the multicast address can be ignored to provide the ability to create multiple multicast address ranges. 

if ((IgnMbits)&(MultiCastAddress[0] ==0x000)) { MultiCastAddress[0] is ignored in compare} 

if ((IgnMbits)&(MultiCastAddress[1:0]==0x001)) { MultiCastAddress[1:0] is ignored in compare} if ((IgnMbits)&(MultiCastAddress[2:0]==0x003)) { MultiCastAddress[2:0] is ignored in compare} if ((IgnMbits)&(MultiCastAddress[3:0]==0x007)) { MultiCastAddress[3:0] is ignored in compare} if ((IgnMbits)&(MultiCastAddress[4:0]==0x00F)) { MultiCastAddress[4:0] is ignored in compare} if ((IgnMbits)&(MultiCastAddress[5:0]==0x01F)) { MultiCastAddress[5:0] is ignored in compare} 

if ((IgnMbits)&(MultiCastAddress[6:0]==0x03F)) { MultiCastAddress[6:0] is ignored in compare} 

if ((IgnMbits)&(MultiCastAddress[7:0]==0x07F)) { MultiCastAddress[7:0] is ignored in compare} 

if ((IgnMbits)&(MultiCastAddress[8:0]==0x0FF)) { MultiCastAddress[8:0] is ignored in compare} 

if ((IgnMbits)&(MultiCastAddress[9:0]==0x1FF)) { MultiCastAddress[9:0] is ignored in compare} 

Below is 'C' code to modify ALE MultiCastAddress and IgnMbits when iNumOfBitsToIgnore is greater than zero. Where fGenMask(iOffset,iBitsToMask) creates a Mask for the value provided. For example fGenMast(0,5) will return 0x1F. 

if(iNumOfBitsToIgnore) 

{ 

int iIgnClrMsk,iIgnSetMsk; 

iIgnClrMsk=fGenMask(0, iNumOfBitsToIgnore); 

iIgnSetMsk=fGenMask(0, iNumOfBitsToIgnore -1); 

MultiCastAddress &= ~iIgnClrMsk; 

MultiCastAddress |= iIgnSetMsk; 

IgnMbits = 1; 

} else 

{ 

IgnMbits = 0; 

1290 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## } 

Multicast Addresses or Ranges can overlap, in the event of an overlap; the higher ALE index will be used. 

## _**13.2.1.4.6.1.11 Aging and Auto Aging**_ 

The ALE supports software control or automatic aging of agable addresses. 

Any time an agable address is seen as a source address entering from a port the source address entry will be marked as touched. 

If the aging timer expires or the software sets the [29] AGE_OUT_NOW bit in the CPSW_ALE_CONTROL, the aging process will be started. 

The aging process will read each ALE entry and for all entries that are an address with or without VLAN that is also agable, the touch check process will be done. 

The touch check process will test the TOUCH bit and if clear, the entry will be marked as free, else the TOUCH bit will be cleared. 

What this means is that if the aging interval was programmed as one second, any unused entry could stay in the ALE table for 1.000001 to 1.999999 seconds 

## _**13.2.1.4.6.1.12 ALE Policing and Classification**_ 

The ALE has a number of configurable classifier engines (policers) that can be used for classification. Classification is a subset of the policing function and uses a policer without the color marking or rate limiting functions. A policer is a hardware engine that is used for policing. The POLCNTDIV8 field in the CPSW_ALE_STATUS register indicates the number of policers available to be used for classification. Each policer can be enabled to match on one or more of any of the below packet fields for classification. All but Port and Priority are index references to the ALE table entries. 

- Port Number 

- Priority extracted from VLAN, mapped from DSCP if enabled, or Default Port Priority 

- Organization Network Unique identifier - ONU 

- Destination Address - DA 

- Source Address - SA 

- Outer VLANID -S-VLANID 

- Inner VLANID -C-VLANID 

- Ether Type 

- IP Source Address - IPSA with full CIDR masking for IPv4 and IPv6 

- IP Destination Address - IPSA with full CIDR masking for IPv4 and IPv6 

- Support Host Thread/Flow ID mapping based on any packet classification above 

## _**13.2.1.4.6.1.12.1 ALE Policing**_ 

The policing function on each policer engine is implemented as dual-counter three-color marking engine as described in the IETF RFC2698. The first counter is the Committed Information Rate (CIR) counter and the second counter is the Peak Information Rate (PIR) counter. The policing function can use either or both counters. Based on the counter values the packet color is determined. The color is used to determine whether the packet is dropped or forwarded. The ALE has a local feature that can drop packets regardless of queue state. 

The policing rates are determined by the below equations: 

CIR policing rate in Mbit/s = ((ALE frequency in Mhz) * CPSW_ALE_POLICECFG7[31-0] CIR_IDLE_INC_VAL) / 32768 

PIR policing rate in Mbit/s = ((ALE frequency in Mhz) * CPSW_ALE_POLICECFG6[31-0] PIR_IDLE_INC_VAL) / 32768 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1291 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

Each policer has 10 different match operations (see Section 13.2.1.4.6.1.12). Since multiple policing entries can be hit on a single packet this provides the ability to create precise traffic stream control. 

Packets are colored at ALE lookup time. Packets can be colored RED, YELLOW, or GREEN. If multiple policers are configured for a packet stream then the packet color is merged from all matching (hit) policers. If any policer is RED then the packet is marked RED. Else if any policer is YELLOW then the packet is marked YELLOW. Otherwise the packet is marked GREEN. 

The Policing engine supports several modes such that packets that don't hit a policing/classifier match can be treated as RED, YELLOW, GREEN or policer 0 color. Using policer 0 allows for a system to regulate unregulated traffic. 

## _**13.2.1.4.6.1.12.2 Classifier to Host Thread Mapping**_ 

The ALE module allows Host Thread mapping based on any packet classification. That is the ALE can generate a thread ID used by the host based on ALE classifier matches. 

When enabled the highest classifier match can map to a particular thread ID value. 

The ALE also supports an optional default Thread ID value in the event that no classifier match. 

Each Thread ID, including the default thread ID, has an enable functionality such that, if no classifier matches occur the default value is used, if the default is not enabled, the switch will use the 6-bit {port[2:0], switch_priority[2:0]} value instead. If multiple classifier matches occur, the highest matching entry with a thread enable bit set will be used. 

Three registers are used for ALE classification thread mapping configuration (CPSW_ALE_THREADMAPDEF, CPSW_ALE_THREADMAPCTL and CPSW_ALE_THREADMAPVAL). The three thread mapping registers are used independently and are separate from the other ALE policing registers. The CPSW_ALE_THREADMAPCTL register allows the CPSW_ALE_THREADMAPVAL register contents to be written to the selected classifier. There is a CPSW_ALE_THREADMAPDEF register that is used for all classifiers. The thread mapping registers can be written or changed at any time but any packets that are already processed will not have their thread altered. 

## _**13.2.1.4.6.1.12.3 ALE Classification**_ 

When the policers are configured as classifiers, the color marking and policing functions of the policing/classifier engines are not used. One or multiple classifiers can be configured to match on a single packet. For example, a classifier can be enabled to match on priority while another classifier could match IP address. 

## _**13.2.1.4.6.1.13 Mirroring**_ 

The ALE supports three mirroring modes: destination port, source port and or table entry. 

**Destination port mirroring** allows packets from any ingress port or trunk which ends up switching to a particular egress destination port or trunk to be mirrored to yet another egress destination port or trunk. For example any traffic from any port that is switched to port 'A' can be also mirrored to port 'B'. (MIRROR_DP=A, MIRROR_DEN=1h, MIRROR_TOP=B in the CPSW_ALE_CONTROL register). 

**Source port mirroring** allows packets received on any enabled ingress source port or trunk to be switched to the mirror egress port as well as the actual egress destination ports. For example traffic received on ingress port 'A' can be switched to egress port 'B' as well as the intended egress destination port.(Iy_REG_Py_MIRROR_SP=1h in the CPSW_Iy_ALE_PORTCTL0_y register, MIRROR_SEN=1h, MIRROR_TOP=B in the CPSW_ALE_CONTROL register). 

**Table entry mirroring** allows for any MAC Address, MAC Address with VLAN, ONU Address or VLAN entry that matches on ingress to be switched to the egress destination as well as the actual egress destination. For example all traffic for VLAN ID of 35 can be mirrored to port 'B'. That is any traffic switched on VLAN ID of 35 will be mirrored. ({VLAN ID of 35 in ALE Table entry index=C}, MIRROR_MIDX=C, MIRROR_MEN=1h, MIRROR_TOP=B) 

1292 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

In the event that mirrored packets are mirrored to or from a port that is also the mirror port the packet will not be duplicated or marked as a mirror packet since the packet has already been on the port as ingress or egress. The packet sent to the mirror port may have modified VLAN info based on the port and VLAN lookup table entries. The mirror port need not be a member of the VLAN ID it is mirroring, the ALE will forward traffic to the mirror port after ingress and egress filters are applied. 

The switch may decide to drop any mirror traffic based on switch buffer thresholds as to prevent required traffic from becoming congested. 

Port mirroring is controlled by register fields in CPSW_ALE_CONTROL, CPSW_ALE_CTRL2 and the port control registers. 

- MIRROR_DP - The destination port that will have its traffic mirrored (CPSW_ALE_CONTROL register). 

- MIRROR_TOP - The port to which mirrored traffic is sent (CPSW_ALE_CONTROL register). 

- MIRROR_MEN - The enable for mirroring traffic that matches a supported lookup table entry (CPSW_ALE_CONTROL register). 

- MIRROR_DEN - The Enable for destination port mirroring (CPSW_ALE_CONTROL register). 

- MIRROR_SEN - The Enable for source port mirroring (CPSW_ALE_CONTROL register). 

- MIRROR_MIDX - The index of a lookup table entry that will be mirrored (CPSW_ALE_CTRL2 register). 

- Iy_REG_Py_MIRROR_SP - The enable for the Source port to be mirrored. Although multiple source ports can be mirrored concurrently, a mirror traffic bandwidth issue may occur on the mirror egress port (CPSW_Iy_ALE_PORTCTL0_y register). 

## _**13.2.1.4.6.1.14 Trunking**_ 

The ALE supports port trunking of any port in any of four trunk groups. That is, four trunk groups can be supported with up to eight ports in each trunk group. There are no port adjacency rules for trunk groups. When ports are a member of a trunk group, addresses added and used in the lookup table will refer to the trunk group rather than port as indicated in the lookup table entries. If ports are removed from a trunk group, the ALE will redistribute the traffic based on the crc polynomial of enabled fields and the remaining ports within the trunk group. A trunk group may contain only one port. Packet priority, DA, SA, C-VLAN ID, IPv4SA, IPv4DA, IPv6SA, and/or IPv6DA can be used in the hash to generate destination port within the trunk group. If all hash enables are disabled, the packet can be directed to a particular port within the trunk group which allows for testing paths etc. A host directed frame is directed to the directed port regardless of trunk group settings. 

Trunking is controlled through fields in the CPSW_ALE_CTRL2 register and in each ALE CPSW_Iy_ALE_PORTCTL0_y register: 

- TRK_EN_DST - Enable destination address hashing for trunk port calculation. 

- TRK_EN_SRC - Enable source address hashing for trunk port calculation. 

- TRK_EN_PRI - Enable priority hashing for trunk port calculation. 

- TRK_EN_IVLAN - Enable inner C-VLAN ID hashing for trunk port calculation. 

- TRK_EN_SIP - Enable source IP address hashing for trunk port calculation. 

- TRK_EN_DIP - Enable destination IP address hashing for trunk port calculation. 

- TRK_BASE - Hashing formula starting value and test port offset. 

- Iy_REG_Py_TRUNKEN - Enable this port as a trunk group 

- Iy_REG_Py_TRUNKNUM - Trunk group number defines this port as a member of a particular trunk group. 

## _**13.2.1.4.6.1.15 DSCP**_ 

The ALE can map DSCP field to priority prior to classification matching. When enabled the DSCP is mapped via 64 priority entries such that any DSCP value can be mapped to any of the eight priorities. When a packet is received without a VLAN priority this remapped priority can be used instead of the default Port VLAN priority field. See CPSW_P0_RX_DSCP_MAP_REG_y and CPSW_PN_RX_DSCP_MAP_REG_y registers in the Register Manual section for DSCP mapping. 

## _**13.2.1.4.6.1.16 Packet Forwarding Processes**_ 

There are three processes that an incoming received packet may go through to determine packet forwarding. The processes are _Ingress Filtering_ , _VLAN Lookup_ , and _Egress._ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1293 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

Packet processing begins in the Ingress Filtering process. Each port has an associated packet forwarding state that can be one of four values (Disabled, Blocked, Learning, or Forwarding). The default state for all ports is Disabled. The host sets the packet forwarding state for each port. 

In the packet ingress process (receive packet process), there is a forward state test for unicast destination addresses and a forward state test for multicast addresses. The multicast forward state test indicates the port states required for the receiving port in order for the multicast packet to be forwarded to the transmit port(s). A transmit port must be in the Forwarding state for the packet to be forwarded for transmission. The MCAST_FWD_STATE indicates the required port state for the receiving port as indicated in the preceding table. The unicast forward state test indicates the port state required for the receiving port in order to forward the unicast packet. The transmit port must be in the Forwarding state in order to forward the packet. The BLOCK and SECURE bits determine the unicast forward state test criteria. If both bits are set then the packet is forwarded if the receive port is in the Forwarding/Blocking/Learning state. If both bits are not set then the packet is forwarded if the receive port is in the Forwarding state. The transmit port must be in the Forwarding state regardless. The forward state test used in the ingress process is determined by the destination address packet type (multicast/unicast). 

In general, packets received with errors are dropped by the address lookup engine without learning, updating, or touching the address. The error condition and the abort are indicated by the Ethernet port to the ALE. Packets with errors may be passed to the host (not aborted) by an ingress port, if the switch port setting has the RX_CMF_EN, RX_CEF_EN, or RX_CSF_EN bit(s) set in the CPSW_PN_MAC_CONTROL_REG register. Error packets that are passed to the host by the Ethernet port are considered to be bypass packets by the ALE and are sent only to the host. Error packets do not learn, update, or touch addresses regardless of whether they are aborted or sent to the host. Packets with long or short errors received by the host are dropped. Packets with errors received by the host are forwarded as normal. 

The following control bits are in the CPSW_PN_MAC_CONTROL_REG register: 

- [22] RX_CEF_EN - enables frames that are fragments, long, jabber, CRC, code, and alignment errors to be forwarded 

- [23] RX_CSF_EN - enables short frames to be forwarded 

- [24] RX_CMF_EN - enables MAC control frames to be forwarded. 

## _**13.2.1.4.6.1.16.1 Ingress Filtering Process**_ 

|**Condition and action**|
|---|
|If ((ALE BYPASS) and (host port is not the receive port))|
|then use host portmask and go to Egress process|
|if (directed packet)|
|then use directed port number and go to Egress process|
|If (Rx Iy_REG_Py_PORTSTATE is Disabled)|
|then discard the packet|
||
|if ((error packet) and (host port is not the receive port))|
|then use host portmask and go to Egress process|
|if (((BLOCK) and (unicast source address found)) or ((BLOCK) and (unicast destination address found)))|
|then discard the packet|
|if ((ENABLE_RATE_LIMIT) and (rate limit exceeded) and (not RATE_LIMIT_TX)|
|then if (((Multicast/Broadcast destination address found) and (not SUPER)) or (Multicast/Broadcast destination address not found))|
|then discard the packet|
|if ((not forward state test valid) and (destination address found))|
|then discard the packet to any port not meeting the requirements|
|•<br>Unicast destination addresses use the unicast forward state test and multicast destination addresses use the multicast forward state|
|test.|



1294 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

if ((destination address not found) and ((not transmit port forwarding) or (not receive port forwarding))) then discard the packet to any ports not meeting the above requirements if (source address found) and (secure) and (not block) and (receive port number != port_number)) then discard the packet if ((not super) and (drop_untagged) and ((non-tagged packet) or ((priority tagged) and not(en_vid0_mode))) then discard the packet If (VLAN_Unaware) CPSW_ALE_UVLAN_UNTAG = “000000” CPSW_ALE_UVLAN_URCAST = “111111” CPSW_ALE_UVLAN_URCAST = “111111” UVLAN_MEMBER_LIST = “111111” else if (VLAN not found) CPSW_ALE_UVLAN_UNTAG = CPSW_ALE_UVLAN_UNTAG CPSW_ALE_UVLAN_RMCAST = CPSW_ALE_UVLAN_RMCAST CPSW_ALE_UVLAN_RMCAST = CPSW_ALE_UVLAN_RMCAST CPSW_ALE_UVLAN_MEMBER = CPSW_ALE_UVLAN_MEMBER else CPSW_ALE_UVLAN_UNTAG = found CPSW_ALE_UVLAN_UNTAG CPSW_ALE_UVLAN_URCAST = found CPSW_ALE_UVLAN_URCAST CPSW_ALE_UVLAN_RMCAST = found CPSW_ALE_UVLAN_RMCAST UVLAN_MEMBER_LIST = found UVLAN_MEMBER_LIST if ((not SUPER) and (Iy_REG_Py_VID_INGRESS_CHECK) and (Rx port is not VLAN member)) then discard the packet if ((ENABLE_AUTH_MODE) and (source address not found) and not(destination address found and (SUPER))) then discard the packet if (destination address equals source address) then discard the packet goto VLAN_Lookup process 

## _**13.2.1.4.6.1.16.2 VLAN Lookup Process**_ 

**Condition and action** if ((unicast packet) and (destination address found with or without VLAN) and (not SUPER) then portmask is the logical "AND" of the PORT_NUMBER and UVLAN_MEMBER_LIST and goto Egress process if ((unicast packet) and (destination address found with or without VLAN) and (SUPER)) then portmask is the PORT_NUMBER and goto Egress process if ((Unicast packet) and (destination address not found)) then portmask is UVLAN_MEMBER_LIST less host port (if UNI_FLOOD_TO_HOST is not set) and goto Egress process 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1295 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

if ((Multicast packet) and (destination address found with or without VLAN) and (not SUPER)) 

then portmask is the logical “AND” of CPSW_ALE_UVLAN_URCAST and found destination address/VLAN portmask (PORT_MASK) and UVLAN_MEMBER_LIST 

and goto Egress process 

if ((Multicast packet) and (destination address found with or without VLAN) and (SUPER)) then portmask is the PORT_MASK 

and goto Egress process 

if ((Multicast packet) and (destination address not found)) then portmask is the logical “AND” of CPSW_ALE_UVLAN_URCAST and UVLAN_MEMBER_LIST then goto Egress process 

if (Broadcast packet) then use found UVLAN_MEMBER_LIST and goto Egress process 

## **Note** 

The UVLAN_MEMBER_LIST, UVLAN_UNREG_MCAST_FLOOD_MASK, 

UVLAN_REG_MCAST_FLOOD_MASK and UVLAN_FORCE_UNTAGGED_EGRESS are set in the Section 13.2.1.4.6.1.16.1 _Ingress Filtering Process_ , based on VLAN_Unaware, Unknown_VLAN rules and VLAN table entries. 

## _**13.2.1.4.6.1.16.3 Egress Process**_ 

## **Condition and action** 

Clear Rx port from portmask (don’t send packet to Rx port). 

Clear disabled ports from portmask. 

if ((ENABLE_OUI_DENY) and (OUI source address not found) and (not ALE_BYPASS) and (not error packet) and (not ((destination address) and (SUPER)))) 

then Clear host port from portmask 

if ((not ENABLE_OUI_DENY) and (OUI source address found) and (not ALE BYPASS) and (not error packet) and not ((destination address) and (SUPER)))) 

then Clear host port from portmask 

if ((ENABLE_RATE_LIMIT) and (RATE_LIMIT_TX)) 

then if (not SUPER) and (rate limit exceeded on any tx port) 

then clear rate limited tx port from portmask 

If address not found then SUPER cannot be set. 

If portmask is zero then discard packet 

Send packet to portmask ports 

## _**13.2.1.4.6.1.16.4 Learning/Updating/Touching Processes**_ 

The learning, updating, and touching processes are applied to each receive packet that is not aborted. The processes are concurrent with the packet forwarding process. In addition to the following, a packet must be received without error in order to learn/update/touch an address. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1296 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.2.1.4.6.1.16.4.1 Learning Process**_ 

The learning process is applied to each receive packet that is not aborted. The learning process is a concurrent process with the packet forwarding process. 

## **Condition and action** 

If (directed) then do not learn, update, or set touched else continue If (not (Learning or Forwarding) or (ENABLE_AUTH_MODE) or (packet error) or (Iy_REG_Py_NO_LEARN)) then do not learn address if ((Non-tagged packet) and (Iy_REG_Py_DROP_UN_TAGGED)) then do not learn address if ((VLAN_AWARE) and (VLAN not found) and (unknown UVLAN_MEMBER_LIST = “000”)) then do not learn address if ((Iy_REG_Py_VID_INGRESS_CHECK) and (Rx port is not VLAN member) and (VLAN found)) then do not learn address if ((source address found) and (receive port_number != PORT_NUMBER) and (SECURE or BLOCK)) then do not update address else continue if ((source address found) and (receive port number != PORT_NUMBER)) then update address else continue if ((source address not found) and (VLAN_AWARE) and not (LEARN_NO_VLANID)) then learn address with VLAN if ((source address not found) and ((not VLAN_AWARE) or (VLAN_AWARE and LEARN_NO_VLANID))) then learn address without VLAN 

## _**13.2.1.4.6.1.16.4.2 Updating Process**_ 

**Condition and action** if (directed) then do not update address If (not(Learning or Forwarding) or (ENABLE_AUTH_MODE) or (packet error) or (Iy_REG_Py_NO_LEARN)) then do not update address if ((Non-tagged packet) and (Iy_REG_Py_DROP_UN_TAGGED)) then do not update address if ((VLAN_AWARE) and (VLAN not found) and (unknown UVLAN_MEMBER_LIST = “000”)) then do not update address if ((Iy_REG_Py_VID_INGRESS_CHECK) and (Rx port is not VLAN member) and (VLAN found)) then do not update address if ((source address found) and (receive port number != PORT_NUMBER) and (SECURE or BLOCK)) then do not update address if ((source address found) and (receive port number != PORT_NUMBER)) then update address 

## _**13.2.1.4.6.1.16.4.3 Touching Process**_ 

if ((source address found) and (ageable) and (not touched)) then set touched 

## _**13.2.1.4.6.1.17 VLAN Aware Mode**_ 

The CPSW is in VLAN aware mode when the VLAN_AWARE bit is set in the CPSW_CONTROL_REG register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1297 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

In VLAN aware mode, transmitted packet data is changed depending on the packet type (PKT_TYPE), packet priority (PKT_PRI), and VLAN information. 

The VLAN_LTYPE_SEL value is selected by the S_CN_SWITCH bit in the CPSW_CONTROL_REG register and is either the VLAN_LTYPE_INNER (8100h default) or VLAN_LTYPE_OUTER (88A8h default) value. 

## _**13.2.1.4.6.1.18 VLAN Unaware Mode**_ 

An egress port is operating in the VLAN unaware mode when the VLAN_AWARE bit in the CPSW_CONTROL_REG register is cleared to 0h. In VLAN unaware mode, transmit (egress) packets are not modified on egress. 

## _**13.2.1.4.6.1.19 Transmit VLAN Processing**_ 

Transmit packets are NOT modified during switch egress when the VLAN_AWARE bit in the CPSW_CONTROL_REG register is cleared to 0h. This means that the switch is not in VLAN-aware mode. 

The next three sections cover transmit processing when the switch is in VLAN-aware mode for different packet types. The Gigagibit Ethernet switch is in VLAN-aware mode when the VLAN_AWARE bit is set in the CPSW_CONTROL_REG register. While in VLAN-aware mode, VLAN is added, removed, or replaced according to the type of packet as well as the CPSW_ALE_UVLAN_UNTAG[1-0] UVLAN_FORCE_UNTAGGED_EGRESS bit in the packet header as explained below. 

## _**13.2.1.4.6.1.19.1 Untagged Packets (No VLAN or Priority Tag Header)**_ 

Untagged packets are all packets that are not a VLAN packet or a priority tagged packet. According to the CPSW_ALE_UVLAN_UNTAG[1-0] UVLAN_FORCE_UNTAGGED_EGRESS bit in the packet header the packet may exit the switch with a VLAN tag inserted or the packet may leave the switch unchanged. The two cases are discussed below. 

- Insert VLAN Case: 

Untagged input packets have the header packet VLAN inserted when the CPSW_ALE_UVLAN_UNTAG[1-0] UVLAN_FORCE_UNTAGGED_EGRESS bit in the transmit packet header is de-asserted. For untagged packets, the VLAN EtherType = 0x8100 is inserted after the source address followed by the two byte header packet VLAN. The header packet VLAN is composed of the header packet priority along with the PORT_CFI and PORT_VID values from the CPSW_PN_PORT_VLAN_REG register (where N is the port that the untagged packet entered the switch) through. The packet length/type field is output four bytes later than it is input and is not removed or replaced. 

- No Change Case: 

Untagged input packets are output unchanged when the CPSW_ALE_UVLAN_UNTAG[1-0] UVLAN_FORCE_UNTAGGED_EGRESS transmit packet header bit is asserted. 

## _**13.2.1.4.6.1.19.2 Priority Tagged Packets (VLAN VID == 0 && EN_VID0_MODE ==0h)**_ 

Priority tagged packets are packets that contain a VLAN header with VID = 0. According to the CPSW_ALE_UVLAN_UNTAG[1-0] UVLAN_FORCE_UNTAGGED_EGRESS bit in the packet header, priority tagged packets may exit the switch with their VLAN ID and priority replaced or they may have their priority tag completely removed. The two cases are discussed below. 

## **Note** 

In order for a priority tagged packet to fall into this category the ENABLE_VID0_MODE bit in the CPSW_ALE_CONTROL register must also be set to 0h. If the ENABLE_VID0_MODE bit in the CPSW_ALE_CONTROL register is set to 1h, then packets with a VLAN VID of 0 will fall into the VLAN Tagged Packets category in Section 13.2.1.4.6.1.19.3 below. 

- Replace Priority and VLAN ID Case: 

1298 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

Priority tagged input packets have the packet VLAN ID and the packet priority replaced with the header packet VLAN ID and the header packet priority when the transmit packet header CPSW_FORCE_UNTAGGED_EGRESS_REG[1-0] MASK bit is de-asserted. The header packet VLAN ID comes from the PORT_VID bits in the CPSW_PN_PORT_VLAN_REG register (where N is the port where the packet entered the switch). The header packet priority is based on the packet priority to header packet priority mapping in the CPSW_PN_RX_PRI_MAP_REG register (where N is the port where the packet entered the switch). 

- Remove VLAN Header Case: 

Priority tagged input packets have the 4-byte packet VLAN information removed when the transmit packet header CPSW_ALE_UVLAN_UNTAG[1-0] UVLAN_FORCE_UNTAGGED_EGRESS bit is asserted. The 0x8100 EtherType is removed as is the two byte packet VLAN. Input 64-67 byte priority tagged packets go out with the VLAN removed and padded to 64-bytes if the PASS_CRC input bit is asserted. The input CRC bytes are used as the pad data. Input 64-byte priority-tagged packets use all four input CRC bytes as pad, input 65-byte priority-tagged packets use three of the input CRC bytes as pad, and so on. No pad is performed if the PASS_CRC input bit is not asserted - input 64-67 byte (on the wire) priority-tagged packets go out as 60-63 byte packets. The output CRC is replaced with a generated CRC when the VLAN is removed. 

## _**13.2.1.4.6.1.19.3 VLAN Tagged Packets (VLAN VID != 0 || (EN_VID0_MODE ==1h && VLAN VID ==0))**_ 

VLAN tagged packets are packets that contain a VLAN header specifying the VLAN the packet belongs to (VID), the packet priority (PRI), and the drop eligibility indicator (CFI). According to the CPSW_ALE_UVLAN_UNTAG[1-0] UVLAN_FORCE_UNTAGGED_EGRESS bit in the packet header, VLAN tagged packets may exit the switch with their VLAN priority replaced or they may have their VLAN header completely removed. The two cases are discussed below. 

- Replace Priority Case: 

VLAN tagged input packets are output with the packet priority replaced with the header packet priority when the transmit packet header CPSW_ALE_UVLAN_UNTAG[1-0] UVLAN_FORCE_UNTAGGED_EGRESS bit is deasserted. 

- Remove VLAN Header Case: 

VLAN tagged input packets have the 4-byte packet VLAN information removed when the transmit packet header CPSW_ALE_UVLAN_UNTAG[1-0] UVLAN_FORCE_UNTAGGED_EGRESS bit is asserted. The VLAN_LTYPE_SEL length/type is removed as is the two byte packet VLAN. Input 64-67 byte VLAN tagged packets go out with the VLAN removed and padded to 64-bytes. The input CRC bytes are used as the pad data. Input 64-byte VLAN tagged packets use all four input CRC bytes as pad, input 65-byte priority tagged packets use three of the input CRC bytes as pad, and so on. The output CRC is replaced with a generated CRC when the VLAN is removed. 

## **Note** 

VLAN tagged receive packets of 64 to 67 bytes will be padded to 64 bytes on egress (Ethernet and host port egress) if the VLAN is to be removed on egress. 

## _**13.2.1.4.6.2 Packet Priority Handling**_ 

There are three priorities that are used inside the CPSW: **packet priority** , **header packet priority** , and **switch priority** . The **packet priority** is the determined priority for the ingress packet. The **header packet priority** is used as the outgoing VLAN priority if the packet is egressing from the switch with a VLAN tag. The **switch priority** determines which of the 8 FIFO priority queues the packet uses during egress. 

The VLAN_LTYPE_SEL value below is selected by the S_CN_SWITCH bit in the CPSW Control register and is either the VLAN_LTYPE_INNER (0x8100 default) or the VLAN_LTYPE_OUTER (0x88A8 default) value. 

Packets are received on two types of ports (Ethernet and CPDMA host port). Received packets have a received packet priority (0 to 7, with 7 being the highest priority). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1299 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.6.2.1 Ethernet Port Receive**_ 

The received packet priority for Ethernet receive packets is determined as follows: 

1. If the first packet LTYPE = VLAN_LTYPE_SEL then the received packet priority is the packet priority (VLAN tagged and priority tagged packets). 

2. Else if the first packet LTYPE = 0x0800 and byte 14 (following the LTYPE) is equal to 0x4X, and DSCP_IPV4_EN is set in CPSW_PN_CONTROL_REG, then the received packet priority is the 6-bit TOS field in byte 15 (upper 6 bits) mapped through the port’s DSCP priority mapping registers (IPv4 packet). 

3. Else if the first packet LTYPE = 0x86DD and the most significant nibble of byte 14 (following the LTYPE) is equal to 0x6, and DSCP_IPV6_EN is set in CPSW_PN_CONTROL_REG, then the received packet priority is the 6-bit priority (in the 6-bits following the upper nibble 0x6) mapped through the port’s DSCP priority mapping registers (IPv6 packet). 

4. Else the received packet priority is the source (ingress) port priority taken from the port's ENET_PN_PORT_VLAN register. 

The packet priority is mapped through the receive ports associated packet-priority-to-header-packet-prioritymapping register (CPSW_PN_RX_PRI_MAP_REG) to obtain the header packet priority. The header packet priority is then used as the actual transmit packet priority if the VLAN information is to be sent on egress. The header packet priority is mapped at each destination FIFO through the CPSW_PN_TX_PRI_MAP_REG register (header priority to switch priority mapping register) to obtain the hardware switch priority (hardware queue 0 through 7). 

## _**13.2.1.4.6.2.2 CPDMA Port Receive**_ 

The received packet priority for CPDMA host port receive packets is determined as follows: 

1. If the first packet LTYPE = VLAN_LTYPE_SEL then the received packet priority is the packet priority (VLAN tagged and priority tagged packets). 

2. Else if the first packet LTYPE = 0x0800 and byte 14 (following the LTYPE) is equal to 0x4X, and DSCP_IPV4_EN is set in CPSW_P0_CONTROL_REG, then the received packet priority is the 6-bit TOS field in byte 15 (upper 6 bits) mapped through the port’s DSCP priority mapping registers (IPv4 packet). 

3. Else if the first packet LTYPE = 0x86DD and the most significant nibble of byte 14 (following the LTYPE) is equal to 0x6, and DSCP_IPV6_EN is set in CPSW_P0_CONTROL_REG, then the received packet priority is the 6-bit priority (in the 6-bits following the upper nibble 0x6) mapped through the port’s DSCP priority mapping registers (IPv6 packet). 

4. Else the received packet priority is the source (ingress) port priority taken from the port's P0_PORT_VLAN register. 

The packet priority is mapped through the receive ports associated packet-priority-to-header-packet-prioritymapping register (CPSW_P0_RX_PRI_MAP_REG) to obtain the header packet priority. The header packet priority is then used as the actual transmit packet priority if the VLAN information is to be sent on egress. 

For CPDMA host port receive packets, the destination port hardware switch priority is the below selected value remapped through CPSW_P0_RX_PRI_MAP_REG: 

1. If the receive packet is priority or VLAN tagged: 

   - a. If CPSW_P0_RX_REMAP_VLAN_REG is clear then the destination hardware switch priority is the host receive channel number. 

   - b. If CPSW_P0_RX_REMAP_VLAN_REG is set then the destination hardware switch priority is the packet priority value. Port transmit remapping (ENET_PN_TX_PRI_MAP should remain the default value) is not compatible with this bit being set, but remapping can be configured on port 0 receive. 

2. Else if the receive packet has the first packet LTYPE = 0x0800 and byte 14 (following the LTYPE) is equal to 0x4X, and DSCP_IPV4_EN is set in CPSW_P0_CONTROL_REG: 

   - a. If P0_RX_REMAP_DSCP_IPV4 is clear then the destination hardware switch priority is the host receive priority. 

1300 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

   - b. If P0_RX_REMAP_DSCP_IPV4 is set then the destination hardware switch priority is the 6-bit TOS field in byte 15 (upper 6 bits) mapped through the port's DSCP priority mapping registers (IPV4 packet). Port transmit remapping (ENET_PN_TX_PRI_MAP should remain the default value) is not compatible with this bit being set, but remapping can be configured on port 0 receive. 

3. Else if the receive packet has the first packet LTYPE = 0x86DD and the most significant nibble of byte 14 (following the LTYPE) is equal to 0x6, and DSCP_IPV6_EN is set in CPSW_P0_CONTROL_REG: 

   - a. If P0_RX_REMAP_DSCP_IPV6 is clear then the destination hardware switch priority is the host receive priority. 

   - b. If P0_RX_REMAP_DSCP_IPV6 is set then the destination hardware switch priority is the 6-bit priority (in the 6 bits following the upper nibble 0x6) mapped through the port's DSCP priority mapping registers (IPV6 packet). Port transmit remapping (ENET_PN_TX_PRI_MAP should remain the default value) is not compatible with this bit being set, but remapping can be configured on port 0 receive. 

4. Else the receive packet is non-tagged and the destination hardware switch priority is the host receive channel number. 

## _**13.2.1.4.6.2.3 CPDMA Port Transmit**_ 

If the TH_CH_OVERRIDE bit in the CPDMA Control register is clear, then the CPDMA packet transmit channel number is the port 0 hardware **switch priority** . If TH_CH_OVERRIDE is set, then for packets with a classification match the transmit channel number is the lower three bits of the 6-bit address lookup engine classification match value (THREADVAL[2:0] in ALE register THREADMAPVAL). The FLOW value in the VLAN encapsulation word is all 6 bits of the THREADVAL for classifier matches regardless of the setting of TH_CH_OVERRIDE if the encapsulation word is transferred. 

## _**13.2.1.4.6.2.4 Priority Mapping and Transmit VLAN Priority**_ 

Figure 13-91 below, as well as the corresponding explanation that follows, explains each of the priorities, how they are determined, and how they are used. A number in parentheses in the figure indicates a process (Ethernet port ingress, host port egress, etc.). Each bullet in the text following the diagram explains one of the 5 processes pointed out in the figure. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1301 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [363 x 274] intentionally omitted <==**

**----- Start of picture text -----**<br>
Port 1 TX FIFO<br>(3)<br>To<br>Ethernet<br>(2) Port 1<br>Port 0 TX FIFO Port 1 RX FIFO<br>(3)<br>TH_VBUSPTo  (4) (1) Ethernet Port 1From<br>SCR<br>Port 0 RX FIFO Port N TX FIFO<br>(3)<br>To<br>From  Ethernet<br>FH_VBUSP (5) (2) Port N<br>Port N RX FIFO<br>From<br>Ethernet<br>(1) Port N<br>...<br>**----- End of picture text -----**<br>


**Figure 13-91. Gigabit Ethernet Switch Priority Mapping and Transmit VLAN Processing** 

1302 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

From Figure 13-91 above: 

- (1) is the ingress process that occurs at the external Ethernet ports 

   - The incoming packet is assigned a **packet priority** based on either its VLAN priority, IPv4 or IPv6 DSCP value, or the ingress port’s priority. This **packet priority** is then mapped to a **header packet priority** using the CPSW_PN_RX_PRI_MAP_REG register where N is the port where the packet entered the switch. This process is explained in further detail in Section 13.2.1.4.6.2. 

- (2) is the egress process that occurs at the external Ethernet ports 

   - If the switch is in VLAN Aware mode then the VLAN header may be added, replaced, or removed during the egress process. If the VLAN header is to be added or replaced, the VLAN priority will come from the **header packet priority** that was determined in process (1) or (5). Transmit VLAN processing is the same for both the host port and the external Ethernet ports and is described in Section 13.2.1.4.6.1.19. 

- (3) is the process by which it is decided which priority TX queue to place the packet on in the Port N TX FIFO during egress 

   - Each Port’s TX FIFO has 8 queues that each correspond to a priority that is used when determining which packet will egress from the switch next at that port. The **header packet priority** (Ethernet port ingress, process (1)) or the receive packet channel (host port 0 ingress, process (5)) gets mapped through the CPSW_PN_RX_PRI_MAP_REG register (where N is the egress port number) to determine the **switch priority** of the packet. The **switch priority** determines which TX FIFO queue to place the packet in. The FIFO architecture is described in Section 13.2.1.4.6.10.5. The header packet priority to switch priority mapping is discussed in Section 13.2.1.4.6.2. 

- (4) is the egress process that occurs at CPDMA Host Port 0 

   - The egress process for CPDMA Host Port 0 is discussed in Section 13.2.1.4.6.2.3. 

   - If the switch is in VLAN Aware mode then the VLAN header may be added, replaced, or removed during the egress process. If the VLAN header is to be added or replaced, the VLAN priority will come from the **header packet priority** that was determined in process (1). Transmit VLAN processing is the same for both the host port and the external Ethernet ports and is described in Section 13.2.1.4.6.1.19. 

- (5) is the ingress process that occurs at CPDMA Host Port 0 

   - The incoming packet is assigned a **packet priority** based on either its VLAN priority, IPv4 or IPv6 DSCP value, or the host port’s priority. This packet priority is then mapped to a **header packet priority** using the CPSW_P0_RX_PRI_MAP_REG register. 

   - The process to determine the destination hardware **switch priority** is discussed in Section 13.2.1.4.6.2.2. 

## _**13.2.1.4.6.3 CPPI Port Ingress**_ 

Packets received on the CPDMA host port have a received packet priority (0 to 7 with 7 being the highest priority). 

The received packet priority is determined as follows: 

1. If the first packet LTYPE = VLAN_LTYPE_SEL then the received packet priority is the packet priority (VLAN tagged and priority tagged packets). 

2. Else if the first packet LTYPE = 0x0800 and byte 14 (following the LTYPE) is equal to 0x4X, and DSCP_IPV4_EN is set in CPSW_P0_CONTROL_REG or CPSW_PN_CONTROL_REG register, then the received packet priority is the 6-bit TOS field in byte 15 (upper 6 bits) mapped through the port’s DSCP priority mapping registers (IPv4 packet). 

3. Else if the first packet LTYPE = 0x86DD and the most significant nibble of byte 14 (following the LTYPE) is equal to 0x6, and DSCP_IPV6_EN is set in CPSW_P0_CONTROL_REG or CPSW_PN_CONTROL_REG register, then the received packet priority is the 6-bit priority (in the 6-bits following the upper nibble 0x6) mapped through the port’s DSCP priority mapping registers (IPv6 packet). 

4. Else the received packet priority is the source (ingress) port priority 

For CPPI ingress packets, the destination port hardware switch priority is the below selected value remapped through CPSW_PN_RX_PRI_MAP_REG: 

1. If the ingress packet is priority tagged or vlan tagged: 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1303 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

   - If RX_REMAP_VLAN in CPSW_P0_CONTROL_REG register is clear then the destination hardware switch priority is the CPPI receive channel number. 

   - If RX_REMAP_VLAN in CPSW_P0_CONTROL_REG register is set then the destination hardware switch priority is the packet priority value. Port transmit remapping (CPSW_PN_TX_PRI_MAP_REG should remain the default value) is not compatible with this bit being set, but remapping can be configured on port 0 receive. 

2. Else if the ingress packet has the first packet LTYPE = 0x0800 and byte 14 (following the LTYPE) is equal to 0x4X, and DSCP_IPV4_EN is set in CPSW_P0_CONTROL_REG register: 

   - If RX_REMAP_DSCP_V4 bit in CPSW_P0_CONTROL_REG register is clear then the destination hardware switch priority is the CPPI receive channel number. 

   - If RX_REMAP_DSCP_V4 bit in CPSW_P0_CONTROL_REG register is set then the destination hardware switch priority is the 6-bit TOS field in byte 15 (upper 6-bits) mapped through the port’s DSCP priority mapping registers (IPV4 packet). Port 1 transmit remapping (CPSW_PN_TX_PRI_MAP_REG should remain the default value) is not compatible with this bit being set, but remapping can be configured on port 0 receive. 

3. Else if the ingress packet has the first packet LTYPE = 0x86DD and the most significant nibble of byte 14 (following the LTYPE) is equal to 0x6, and DSCP_IPV6_EN is set in P0_CONTROL_REG register: 

   - If RX_REMAP_DSCP_V6 bit in CPSW_P0_CONTROL_REG register is clear then the destination hardware switch priority is the CPPI receive channel number. 

   - If RX_REMAP_DSCP_V6 bit in CPSW_P0_CONTROL_REG register is set then the destination hardware switch priority is the 6-bit priority (in the 6-bits following the upper nibble 0x6) mapped through the port’s DSCP priority mapping registers (IPV6 packet). Port 1 transmit remapping (CPSW_PN_TX_PRI_MAP_REG should remain the default value) is not compatible with this bit being set, but remapping can be configured on port 0 receive. 

4. Else the ingress packet is non-tagged and the destination hardware switch priority is the CPPI receive channel number. 

## _**13.2.1.4.6.4 Packet CRC Handling**_ 

The P0_TX_CRC_REMOVE bit in the CPSW_CONTROL_REG register determines if host port egress packets have CRC included or not. If P0_TX_CRC_REMOVE is set to 1h then all packets that are transmitted from port 0 do not contain CRC. If P0_TX_CRC_REMOVE bit is cleared to 0h then all packets that are transmitted from port 0 contain CRC. The CRC type, if present, is determined by the CRC_TYPE bit in the CPSW_PN_MAC_CONTROL_REG register. If the CRC_TYPE bit is cleared to 0h then the CRC present in each packet after host port egress is Ethernet CRC. If the CRC_TYPE bit is set to 1h then the CRC present in each packet after host port egress is Castagnoli CRC. 

## **Note** 

The CRC type present in the packet after host port egress is determined solely by the CRC_TYPE bit in the CPSW_PN_MAC_CONTROL_REG register regardless of the CRC type present in the packet during Ethernet port ingress. 

## _**13.2.1.4.6.4.1 Ethernet Port Ingress Packet CRC**_ 

All Ethernet ports check the ingress packet CRC in all modes/speeds. The receive port can check either Ethernet CRC or Castagnoli CRC as determined by the CRC_TYPE bit in the CPSW_PN_MAC_CONTROL_REG register. 

## _**13.2.1.4.6.4.2 Ethernet Port Egress Packet CRC**_ 

Ethernet ports transmit each egress packet with the CRC selected by the CRC_TYPE bit in the CPSW_PN_MAC_CONTROL_REG register, regardless of the type of CRC that the packet had on ingress to the switch. At the egress port after passing through the switch, the packet CRC is checked for correctness and if the CRC is correct then the packet is output with the generated selected output CRC. If the packet CRC is incorrect, due either to a bit flip in a memory or an error CRC passed in on host ingress, then the generated 

1304 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

egress CRC type is used with at least a single byte of the CRC inverted to indicate the error. If the packet length including CRC is divisible by 4 then all 4 CRC bytes will be inverted on error. If there are three bytes remainder after dividing the packet length by 4 then three bytes will be inverted (and so on down to one byte remainder). 

## _**13.2.1.4.6.4.3 CPPI Port Ingress Packet CRC**_ 

CPPI port ingress packets can be passed in with or without a CRC. The ingress packet CRC type is indicated in the buffer descriptor word CRC_TYPE bit and can be Ethernet (or Castagnoli if $cppi_cast = 1). The packet CRC_TYPE can change from packet to packet if Castagnoli is supported ($cppi_cast = 1). The P0_RX_PASS_CRC_ERR bit in the CPSW Control register determines if ingress packets with CRC errors are passed or dropped. Passed packets with CRC errors will be transmitted on Ethernet egress with a CRC error. 

## _**13.2.1.4.6.4.4 CPPI Port Egress Packet CRC**_ 

The P0_TX_CRC_REMOVE bit in the CPSW_CONTROL_REG register determines if CPPI egress packet have a CRC included or not. If present, the CRC type for all packets is determined by the P0_TX_CRC_TYPE bit in the CPSW Control register. Egress packets not filtered on Ethernet ingress due to PN_RX_CEF_EN have the packet error CRC included (not replaced by the egress CRC type_) if the CRC is not removed on egress. The error is indicated in the buffer descriptor. CPPI egress packets that detected a CRC error on the internally generated Castagnoli CRC, due to a bit flip in logic or memory, will indicate the error with the drop bit set in the buffer descriptor. 

## _**13.2.1.4.6.5 FIFO Memory Control**_ 

Each of the two CPSW ports has an identical associated FIFO. Each FIFO contains a single logical receive queue and eight logical transmit queues (priority 0 through 7 with 7 the highest priority). Each FIFO memory contains 20,480 bytes (20k) total contained in a single memory instance. The FIFO memory is used for the associated port transmit and receive queues. The TX_MAX_BLKS field in the FIFOs associated CPSW_PN_MAX_BLKS_REG register determines the maximum number of 1k FIFO memory blocks to be allocated to the eight logical transmit queues (transmit total). The RX_MAX_BLKS field in the FIFO's associated CPSW_PN_MAX_BLKS_REG register determines the maximum number of 1k memory blocks to be allocated to the logical receive queue. The TX_MAX_BLKS value plus the RX_MAX_BLKS value must sum to 20 (the total number of blocks in the FIFO). If the sum were less than 20, then some memory blocks would be unused. The default is 16 (decimal) transmit blocks and four receive blocks. The FIFOs follow the naming convention of the Ethernet ports. Host Port is Port0 and External Ports is Port1. 

Each transmit FIFO contains a total of twenty 1k blocks that can be allocated to any priority. 

## _**13.2.1.4.6.6 FIFO Transmit Queue Control**_ 

There are eight transmit queues in the Ethernet port transmit FIFO. Software has some flexibility in determining how packets are loaded into the queues and on how packet priorities are selected for transmission (how packets are removed and transmitted from queues). 

## _**13.2.1.4.6.7 Rate Limiting (Traffic Shaping)**_ 

Rate-limit mode is intended to allow some CPPI ingress channels and some Ethernet transmit (switch egress) priorities to be rate-limited. Non rate-limited traffic (bulk traffic) is allowed on lower priority non ratelimited channels and FIFO priorities. Rate-limited traffic must be configured to be sent to rate-limited queues (via packet priority handling). The allocated rates for rate-limited traffic must not be oversubscribed. For example, if port 1 is sending 15% rate limited traffic to port 2 priority 3, and port 0 is also sending 10% rate-limited traffic to port 2 priority 3, then the port 2 priority 3 egress rate must be configured to be 25% plus a percent or two for margin. The switch must be configured to allow some percentage of non ratelimited traffic. Non rate-limited traffic must be configured to be sent to non rate-limited queues. No packets from the host should be dropped, but non rate-limited Ethernet ingress traffic can be dropped. For rate limited priorities, the configured transfer rate includes the committed information rate and the excess information rate. The excess information rate will only be attempted to be sent when there is no packet backlog on every priority that does not have the excess information rate enabled. The committed information rate will be sent regardless of network traffic as long as the configuration is not oversubscribed. The excess information rate will be sent only when network conditions allow. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1305 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.6.7.1 CPPI Port Receive Rate Limiting**_ 

Port 0 receive operations can be configured to rate limit the packet data for each receive channel (priority). Receive has 8 priorities for QOS. There is a committed information rate (CPSW_P0_PRI_CIR_REG_y, where y = 0 to 7) and an excess information rate for each priority (CPSW_P0_PRI_EIR_REG_y, where y = 0 to 7). Rate limiting is enabled for a priority when the committed information rate for the priority is non-zero. The excess information rate for a priority is enabled when the excess information rate for the priority is non-zero. The committed information rate must be non-zero if the excess information rate is configured to be non-zero. That is, there must be a configured non-zero committed information rate for there to be a configured non-zero excess information rate. Bulk traffic on other non-rate limited priorities does not impact the committed information traffic on a priority. However, bulk traffic on other non-rate limited threads does impact the excess information rates. No bulk priority will be enabled to send unless there are CPSW_PN_PRI_CTL_REG[15-12] TX_HOST_BLKS_REM number of unused blocks remaining in each of the Ethernet port transmit FIFOs. The “blocks remaining check” ensures that bulk traffic from the host will not block rate-limited traffic from the host. Rate limited channels must be the highest priority channels. For example, if two rate limited channels are required then priorities 7 and 6 should be configured for committed information (and excess information if desired). When any channels are configured to be rate-limited, the priority type must be fixed for receive. Round-robin priority type is not allowed when rate-limiting is configured for any priority. The configured transfer rate includes the inter-packet gap (12 bytes) and the preamble (8 bytes). The rate in Mbits/second that each priority is configured to receive is controlled by the below equation. If the configured excess information rate is zero, then only the committed information rate is transferred: 

Priority Transfer rate [Mbit/s] = ((((Frequency in MHZ) * CPSW_P0_PRI_CIR_REG_y) / 32768) + (((Frequency in MHZ) * CPSW_P0_PRI_EIR_REG_y) / 32768)) 

Where the _frequency_ is the VBUSP_GCLK frequency (in MHz) and priority 0 to 7. 

For example, 10Mbps on priority 7 would give the below: 

10Mbps = ~ ((350 * 936) / 32768), at 350Mhz and CPSW_P0_PRI_CIR_REG_y[27-0] PRI_CIR value = 936 (no excess information rate) 

## _**13.2.1.4.6.7.2 Ethernet Port Transmit Rate Limiting**_ 

Ethernet port transmit operations can be configured to rate limit egress data for each egress priority. There is a committed information rate (CPSW_NC_ETH_MAC_PN_PRI_CIR_REG_y, where y = 0 to 7) and an excess information rate for each priority (CPSW_NC_ETH_MAC_PN_PRI_EIR_REG_y, where y = 0 to 7). Rate limiting is enabled for a priority when the committed information rate for the priority is non-zero. The excess information rate for a priority is enabled when the excess information rate for the priority is non-zero. The committed information rate must be non-zero if the excess information rate is configured to be non-zero. That is, there must be a configured non-zero committed information rate for there to be a configured non-zero excess information rate. Bulk traffic on other non-rate limited priorities does not impact the committed information traffic on a priority. However, bulk traffic on other non-rate limited priorities does impact the excess information rates. Rate limited channels must be the highest priority channels. For example, if two rate limited channels are required then priorities 7 and 6 should be configured for committed information (and excess information if desired). The configured transfer rate includes the inter-packet gap (12 bytes) and the preamble (8 bytes). The rate in Mbits/ second that each priority is configured to send is controlled by the below equation. If the excess information rate is disabled then the committed information rate only is transferred: 

Priority Transfer rate [Mbit/s] = ((((Frequency in MHZ) * CPSW_NC_ETH_MAC_PN_PRI_CIR_REG_y) / 32768) + (((Frequency in MHZ) * CPSW_NC_ETH_MAC_PN_PRI_EIR_REG_y) / 32768)) 

Where the _frequency_ is the VBUSP_GCLK frequency (in MHz) and priority 0 to 7. 

## _**13.2.1.4.6.8 Enhanced Scheduled Traffic (EST – P802.1Qbv/D2.2)**_ 

## _**13.2.1.4.6.8.1 Enhanced Scheduled Traffic Overview**_ 

- When enabled and configured, EST allows express queue traffic to be scheduled (placed) on the wire at specific repeatable time intervals. 

1306 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- EST operates on a repeating time interval generated by the CPTS EST function generator. For example, a 125us repeating time interval can be configured. 

- Each Ethernet port has 128 EST fetch commands maximum in the global EST fetch RAM. 

- Each 22-bit fetch command consists of a 14-bit fetch count (14 MSB’s) and an 8-bit priority fetch allow (8 LSB’s) that will be applied for the fetch count time in wireside clocks. 

- The configured port fetch commands are executed in sequence, beginning at port address zero each time through the time interval beginning at cycle start. 

- EST allows non-scheduled express and prempt queue traffic to be cleared from the wire to ensure that the scheduled traffic is transmitted at the proper time (zero allow). 

- EST can be used with or without premption. The CPSW_PN_IET_CONTROL_REG[23-16] MAC_PREMPT value determines whether the priority is enabled on the express or prempt queue. Whether a priority is on the express or prempt queue only effects the wire clear time from an EST operation perspective. 

- Software should not move priorities to the prempt queue unless preemption is configured, enabled, and verified allowing preemption to occur. 

- Express packet time stamp events can be enabled to assist software in configuring and timing EST operations. 

## _**13.2.1.4.6.8.2 Enhanced Scheduled Traffic Fetch RAM**_ 

- The EST fetch RAM is read/writable in the CPSW configuration address space. 

- The Ethernet transmit port has 128 locations in the global EST fetch RAM. 

   - Ethernet port 1 has EST fetch RAM addresses 0x000-0x07F. 

- **One buffer operation:** When CPSW_PN_EST_CONTROL_REG[0] EST_ONEBUF is set to 1h, the 128 port locations operate as one buffer. The EST_BUFACT bit in CPSW_PN_FIFO_STATUS_REG register is the upper address bit of the port’s fetch RAM address indicating whether operation is currently in the upper or lower 64 locations of the port’s fetch RAM. 

- **Two buffer operation:** When CPSW_PN_EST_CONTROL_REG[0] EST_ONEBUF is cleared there are two 64-location buffers with CPSW_PN_EST_CONTROL_REG[1] EST_BUFSEL selecting the buffer to be used. When the buffer is switched by changing the CPSW_PN_EST_CONTROL_REG[1] EST_BUFSEL value, the actual switch occurs on cycle start. The actual buffer being used is indicated by the EST_BUFACT bit in CPSW_PN_FIFO_STATUS_REG. Software should avoid writing the switched out buffer fetch RAM locations until it detects that the actual switch has occurred. 

- The first address location in the port’s fetch RAM space (location zero) is read at the beginning of each EST time interval (cycle start). Addresses are then read in ascending order for the duration of the interval. The port address zero is then read again at the beginning of the next cycle repeating the time interval packet operations. 

## _**13.2.1.4.6.8.3 Enhanced Scheduled Traffic Time Interval**_ 

- Each Ethernet port has an Enhanced Scheduled Traffic Function (ESTF) generator in the CPTS submodule. 

- The EST function generator generates the EST time interval as a configured number of CPTS reference clocks (CPTS_RFT_CLK). 

- The EST function generator rising edge is the cycle start time and the cycle repeats (cycle start occurs) after every time interval. 

- The first fetch allowed value is at the port base address zero in the EST fetch RAM and is actually applied 16 wireside clocks after cycle start. The 16 clock cycle delay allows the first fetch value time to be fetched from the EST fetch RAM (prefetch time at cycle start). 

- Each successive fetch allow is applied for the associated fetch count thereafter. The minimum non-zero fetch count is 16. The minimum value of 16 guarantees that the next fetch value has time to be fetched before the current fetch count is over. There are 64 maximum fetch values when CPSW_PN_EST_CONTROL_REG[0] EST_ONEBUF = 0h, and 128 maximum fetch values when CPSW_PN_EST_CONTROL_REG[0] EST_ONEBUF = 1h. 

- The next cycle start then causes the fetch to once again start at the port address zero. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1307 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.6.8.4 Enhanced Scheduled Traffic Fetch Values**_ 

- The 22-bit fetch value is made up of the 14-bit fetch count and the 8-bit fetch allow. 

- The fetch time indicates the number of wireside clocks that the fetch allow will be active. 

- The fetch count is in Ethernet wireside clocks which is bytes in Gigabit mode (CPSW_PN_MAC_CONTROL_REG[7] GIG = 1h) and nibbles in 10/100Mbps mode. 

- When a fetch allow bit is set, the corresponding priority is enabled to begin packet transmission on an allowed priority subject to rate limiting. The actual packet transmission on the wire may carry over into the next fetch count and is the reason for the wire clear time in the fetch zero allow. 

- When a fetch allow bit is cleared, the corresponding priority is not enabled to transmit for the fetch count time. 

- A non-zero fetch allow value with a non-zero fetch count causes the fetch allow value to be applied for the fetch count number of wireside clocks. 

- A zero fetch count causes the associated fetch allow to be held for the duration of the cycle (until the next cycle start). 

- A zero fetch allow with a non-zero fetch count is intended to clear the wire for a scheduled (timed) express packet in the next fetch. A zero fetch allow indicates that no packet can be started for transmission for the associated fetch count. The associated fetch count must be sufficient to guarantee that the wire is cleared given that a packet on an allowed priority in the previous fetch could have been started on the previous clock and that there is hardware latency in the clear time. The timed packet should be sent on a priority that is enabled in the next fetch but disabled in the current zero allow fetch. The fetch allow previous to a zero allow should have only prempt priorities enabled or only express priorities enabled but not both. 

- The number of clocks required to clear the wire varies depending Ethernet wire speed and on whether express or prempt priorities were allowed in the previous fetch command. 

## _**13.2.1.4.6.8.5 Enhanced Scheduled Traffic Packet Fill**_ 

Packet fill can be configured and enabled to occur in the fetch count time associated with a fetched zero allow that preceeds a timed express packet. The intention with fill is that a smaller packet on a non-timed priority might be able to be inserted on the wire during the wire clear time which would increase wire utilization. Fill must be configured to ensure that any fill packet does not conflict with the timed express packet allowed in the next fetch. Incorrect configuration might push out in time any express timed packet which indicates that the fill margin needs to be increased 

Fill Configuration: 

- The **est_fill_margin** value in **PN_EST_CONTROL_REG** should be written with a 0x100 value 

- The **est_prempt_comp** value in **PN_EST_CONTROL_REG** should be written with a 0x12 value (if IET is to be configured and enabled). This value times eight is the number of wireside clocks required to clear prempt packets off the wire at the end of a zero allow 

- The **est_fill_en** bit in **PN_EST_CONTROL_REG** should be set 

## _**13.2.1.4.6.8.6 Enhanced Scheduled Traffic Time Stamp**_ 

The EST can be configured to generate CPTS timestamp events for selected express traffic. The EST timestamp events use the CPTS host event type (CPSW_CPTS_EVENT_1_REG[23-20] EVENT_TYPE = 7 decimal. The EST timestamps will not override host sent timestamps for packets that were sent from the host with an enabled host timestamp. 

- EST Events (host events) contain the below information: 

   - Time Stamp of the selected express packet. 

   - The event CPSW_CPTS_EVENT_1_REG[28-24] PORT_NUMBER indicates the transmit port number. 

   - The event CPSW_CPTS_EVENT_1_REG[23-20] EVENT_TYPE is decimal 7 (host event). 

   - The event CPSW_CPTS_EVENT_1_REG[23-20] MESSAGE_TYPE indicates the packet transmit hardware switch priority. 

   - The event CPSW_CPTS_EVENT_1_REG[15-0] SEQUENCE_ID upper nibble indicates the packet receive port number. 

1308 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

   - The event CPSW_CPTS_EVENT_1_REG[15-0] SEQUENCE_ID lower byte indicates the sequence number of the express packet in numerical order. The first event is event one, the second is event two and so on. The sequence ID rolls over to zero after 0xFF (8-bits). 

   - The event domain is the value from the CPSW_EST_TS_DOMAIN_REG[7-0] EST_TS_DOMAIN register. 

- When CPSW_PN_EST_CONTROL_REG[2] EST_TS_EN is set, timestamp events will be generated on selected express traffic. 

- When CPSW_PN_EST_CONTROL_REG[3] EST_TS_FIRST is also set, events will be generated only on the first express packet in each time interval. If CPSW_PN_EST_CONTROL_REG[4] EST_TS_ONEPRI is also set then the event will only be on the first CPSW_PN_EST_CONTROL_REG[7-5] EST_TS_PRI express packet in the time interval. If CPSW_PN_EST_CONTROL_REG[4] EST_TS_ONEPRI is clear then the event will be generated on the first express packet in the time interval on any priority. 

- When CPSW_PN_EST_CONTROL_REG[3] EST_TS_FIRST is clear, events will be generated on every express packet. If CPSW_PN_EST_CONTROL_REG[4] EST_TS_ONEPRI is set then the event will be generated on every CPSW_PN_EST_CONTROL_REG[7-5] EST_TS_PRI express packet. If CPSW_PN_EST_CONTROL_REG[4] EST_TS_ONEPRI is clear then event will be generated on every express packet on any priority. 

## _**13.2.1.4.6.9 Audio Video Bridging**_ 

Audio Video Bridging is an ongoing project of IEEE 802.1 concerned with enabling low-latency streaming of time-sensitive audiovisual data over networks. Devices are designated as talkers (transmitters), bridges, or listeners (receivers). It is suggested that the maximum latency could be 2 ms over 7 hops for Class A devices and 20 ms over 7 hops for Class B devices. A hop is essentially a single local area network stage in the journey of a packet. Every time a bridge is encountered between one network section and another a hop is involved. One of the performance goals is that AVB streams will not use more than 75 percent of a link's bandwidth, leaving the remaining capacity for non-AVB streams. 

The goal of developing AVB is simply--extend Ethernet's data-networking capabilities to the realm of reliable real-time audio/video networking. 

An "Audio Video Bridging" network is one that implements a set of protocols being developed by the IEEE 802.1 Audio/Video Bridging Task Group. There are four primary differences between the proposed Audio Video Bridging architecture and existing 802 architectures (from now on the term "AVB" will be used instead of "Audio Video Bridging"): 

1. Precise synchronization - IEEE 802.1AS: " _Timing and Synchronization for Time-Sensitive Applications in Bridged Local Area Networks._ "a.k.a. Precision Time Protocol (PTP). 

2. Traffic shaping for media streams - IEEE 802.1Qav: " _Virtual Bridged Local Area Networks:_ Forwarding and Queuing for Time-Sensitive Streams." 

3. Admission controls - IEEE 802.1Qat: " _Virtual Bridged Local Area Networks - Amendment 9:_ Stream Reservation Protocol (SRP)." 

4. Identification of non-participating devices - IEEE 802.1BA: "Audio/Video Bridging (AVB) Systems" 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1309 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [214 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
Control Applications<br>(UPnP/DLNA, A/VC, HiQnet, etc.)<br>Grand Controller<br>Clock Streaming Media API<br>Selection<br>IEEE1722 TCP/IP<br>Layer 2 AVB Protocol<br>Transport Stack<br>IEEE802.1AS IEEE802.1Qat Protocol<br>Precision Bandwith<br>Time Protocol Reservation<br>IEEE<br>802.1Qav<br>Shaping<br>IEEE 802 Ethernet Driver<br>cpsw-008<br>**----- End of picture text -----**<br>


**Figure 13-92. The Network Static with AVB** 

The following sections describe the media transport protocols that work within the AVB framework. 

## _**13.2.1.4.6.9.1 IEEE 802.1AS: Timing and Synchronization for Time-Sensitive Applications in Bridged Local Area Networks (Precision Time Protocol (PTP))**_ 

The protocol defined by 802.1AS automatically selects a device to be the controller clock, and then distributes this clock throughout the bridged LAN / IP subnet to all other network devices using link-specific transmit/receive time-stamping. However, we only use a two-step solution only on transmit. That is, we do not modify a packet with the timestamp on the way out. The timestamp packet is sent out and then a separate message with the timestamp is sent by the host afterward. Receive can be one or two step. 

## **Note** 

The 802.1AS-distributed clock is not used as a media clock. Rather, the shared 802.1AS clock reference is used to regenerate the media clock at the listener/renderer. Such a reference removes the need to force the latency of the network to be constant, or compute long running averages in order to estimate the actual media rate of the transmitter in the presence of substantial network jitter. IEEE 802.1AS is based on the ratified IEEE 1588 standard. 

Based on IEEE 1588:2002,A PTP devices exchange standard Ethernet messages that synchronize network nodes to a common time reference by defining clock controller selection and negotiation algorithms, link delay measurement and compensation, and clock rate matching and adjustment mechanisms. 

Designed as a simplified profile of IEEE 1588, a primary difference between 1588 and IEEE 802.1AS is that PTP is a layer 2-in other words, a non-IP routable protocol. Like IEEE 1588, PTP defines an automatic method for negotiating the network clock controller, the Best Controller Clock Algorithm (BCCA). PTP nodes can be assigned one of eight priority levels, presumably based on clock quality. BMCA defines the underlying negotiation and signaling mechanism whose purpose is to identify the AVB LAN Grandcontroller. Once a Grandcontroller has been selected, synchronization automatically begins. 

At the core of 802.1AS synchronization is time-stamping. In short, during PTP message ingress/egress from the 802.1AS-capable MAC, the PTP Ether type triggers the sampling of the value of a local real-time counter (RTC). Target nodes compare the value of their RTC against the PTP Grandcontroller and, by use of link delay measurement and compensation techniques, match their RTC value to the time of the AVB LAN PTP domain. After network time throughout the AVB LAN has converged, periodic SYNC and FOLLOW_UP messages provide the information that enables the PTP rate matching adjustment algorithms. The result is all PTP nodes are then synchronized to the same "Wall Clock" time. PTP assures 1-µs accuracy over seven network hops. 

1310 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [362 x 237] intentionally omitted <==**

**----- Start of picture text -----**<br>
dev<br>Grand Controller dev<br>CC<br>AV Bridge<br>AV bridges send a synch message and a<br>correcting follow up from the controller port to<br>the target ports in other devices<br>AV CT<br>Bridge CC<br>AV<br>Bridge CC CT<br>dev<br>CC clock controller port<br>CT clock target port CT<br>dev<br>cpsw-009<br>CT<br>CT CC<br>CC CC<br>CT<br>**----- End of picture text -----**<br>


**Figure 13-93. AVB Network & PTP Clock Entities** 

The media transport protocols that work within the AVB framework are: 

## _**13.2.1.4.6.9.1.1 IEEE 1722: "Layer 2 Transport Protocol for Time-Sensitive Streams"**_ 

AVBTP or 1722 sits above the IEEE 802.1 AVB plumbing and below the application layer. It acts as the conduit between an Ethernet MAC and a streaming application. AVBTP abstracts the underlying network transmission channel to enable the virtual connection of distributed audio and video CODECs over reliable Ethernet networks. A complete AVBTP Ethernet packet is shown in Figure 13-94 and illustrates how IEC 61883-6 AM824 uncompressed audio samples are encapsulated in an Ethernet frame. 

## **IEEE 1722 Packet Construction** 

**==> picture [428 x 178] intentionally omitted <==**

**----- Start of picture text -----**<br>
8 bytes 6 bytes 6 bytes 4 bytes 2 bytes 0-1,500 bytes<br>AVBTP Dest. Source VLAN Ether-<br>Ethernet Frame Preamble address address tag type IEEE P1722 data stream CRC<br>24 bytes 0-1,476 bytes<br>IEEE P1722 Header Stream AVBTP Payload IEC 61883 audio/video packet<br>Packet ID timestamp info<br>8 bytes 0-1468 bytes<br>IEC 61883 IEC 61883 Audio/video samples<br>Packet header<br>8 bytes 8 bytes 8 bytes 8 bytes 8 bytes 8 bytes<br>I S Samples2 Samples 1I S2 Samples 2I S2 Samples 3I S2 Samples 4I S2 Samples 5I S2 SamplesI S2 n<br>cpsw-010<br>**----- End of picture text -----**<br>


**Figure 13-94. IEEE 1722 Packets** 

1722 or AVBTP Presentation Time and Synchronization: 

Synchronization in an AVB network starts with the Precision Time Protocol but ends with synchronized media clocks. PTP is responsible for synchronizing all nodes in an AVB network to identical wall clock time; not for 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1311 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

synchronizing media clocks. In other words, PTP does not actually transport synchronized media clocks but instead provides a low-level building block crucial for managing a distributed media synchronization system. 

A crucial benefit of this approach is coexistence of multiple, independent media clock domains on an AVB network. Unrelated audio and video streams can simultaneously exist in the same LAN. 

## _**13.2.1.4.6.9.1.1.1 Cross-timestamping and Presentation Timestamps**_ 

AVBTP assumes that AVB node media clocks are clocked by free-running oscillators. It is also assumed that the node's internal concept of wall clock time has been synchronized to the PTP Grandcontroller. AVBTP media clock sources embed "AVBTP Presentation Timestamps" in AVBTP streaming packets. Figure 13-95 illustrates the relationship between PTP network time and AVBTP Presentation Timestamps. 

## **Presentation timestamps** 

## **Cross-time stamped clock recovery** 

**==> picture [405 x 327] intentionally omitted <==**

**----- Start of picture text -----**<br>
Outgoing stream Incoming stream<br>Timestamps Data Timestamps Data<br>0 0<br>0 0<br>0 0<br>9000000 00 7166667 00<br>0 0<br>0 0<br>0 0<br>0 0<br>0 0<br>0 0<br>8833333 00 7333333 00<br>0 0<br>0 0<br>0 0<br>0 0<br>0 0<br>0 0<br>8666667 00 ... 00<br>0 0<br>0 0<br>0 0<br>0 0<br>0 0<br>0 0<br>... 00 8666667 00<br>0 0<br>0 0<br>0 0<br>0 0<br>0 0<br>0 802.1AS 0<br>Wall time802.1AS 7333333 0000 Wall time 8833333 0000<br>0 0<br>0 0<br>0 0<br>0 0<br>7166667 00 9000000 00<br>0 0<br>0 0<br>0 0<br>AVBTP timestamp<br>AVBTP comparator<br>timestamp<br>generator<br>Clock generator<br>Media clock (local oscillator)<br>ADC 1722 Data Generated<br>media<br>clock<br>Incoming<br>analog data<br>Outgoing<br>DAC<br>analog<br>data<br>cpsw-011<br>**----- End of picture text -----**<br>


**Figure 13-95. Cross Time Stamping and Presentation Timestamps** 

## _**13.2.1.4.6.9.1.2 IEEE 1733: Extends RTCP for RTP Streaming over AVB-supported Networks**_ 

This standard specifies the protocol, data encapsulations, connection management and presentation time procedures used to ensure interoperability between audio and video based end stations that use standard networking services provided by all IEEE 802 networks meeting QoS requirements for time-sensitive applications by leveraging the Real-time Transport Protocol (RTP) family of protocols and IEEE 802.1 Audio/ Video Bridging (AVB) protocols. 

## _**13.2.1.4.6.9.2 IEEE 802.1Qav: "Virtual Bridged Local Area Networks: Forwarding and Queuing for Time-Sensitive Streams"**_ 

This standard allows bridges to provide guarantees for time-sensitive (that is, bounded latency and delivery variation), loss-sensitive real-time audio video (AV) data transmission (AV traffic). It specifies per priority ingress 

1312 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

metering, priority regeneration, and timing-aware queue draining algorithms. This standard uses the timing derived from IEEE 802.1AS. Virtual Local Area Network (VLAN) tag encoded priority values are allocated, in aggregate, to segregate frames among controlled and non-controlled queues, allowing simultaneous support of both AV traffic and other bridged traffic over and between wired and wireless Local Area Networks (LANs). 

Such a guarantee in bandwidth is provided by two functional entities: 

- A registration protocol, which registers the service and its maximum network utilization with a device or switch (IEEE 802.1Qat: "Virtual Bridged Local Area Networks - Amendment 9: Stream Reservation Protocol (SRP)") 

- A hardware bandwidth management service. 

   - Receive policing 

   - Transmit rate control. 

## **End Station Behavior** 

In order for an end station to successfully participate in the transmission and reception of time-sensitive streams, it is necessary for their behavior to be compatible with the operation of the forwarding and queuing mechanisms employed in bridges. 

The requirements for end stations that participate as "talkers" i.e., sources of time-sensitive streams are different from the requirements that apply to "listeners", the destination station(s) for the streams. 

## **Talker Behavior** 

In order for Talker-originated data streams to make use of the credit-based shaper behavior in Bridges, it is a requirement for a Talker to use the priorities that the Bridges in the network recognize as being associated with SR classes exclusively for transmitting stream data. 

It is also necessary for the Talker and the Bridges in the path to the Listener(s), to have a common view of the bandwidth required in order to transmit the Talker's streams, and for that bandwidth to be reserved along the path to the Listener(s). This latter requirement can be met by means of stream reservation mechanisms, such as defined in SRP, or by other management means. 

End stations that are Talkers shall exhibit transmission behavior for frames that are part of "time-sensitive streams" that is consistent with the operation of the credit-based shaper algorithm, both in terms of the way they transmit frames that are part of an individual data stream, and in terms of the way they transmit stream data frames from a Port. 

In effect, the queuing model for a Talker Port (and a Listener port), and for given priorities, can be considered to look like Figure 13-96. 

## **Listener Behavior** 

The primary requirement for a listener station is that it is capable of buffering the amount of data that could be transmitted for a stream during a time period equivalent to the accumulated maximum jitter that could be experienced by stream data frames in transmission between Talker and Listener. 

From the point of view of the specification of the forwarding and queuing requirements for time-sensitive streams, it is assumed that the listener will assess the buffering required for a stream as part of the stream bandwidth reservation mechanisms employed by the implementation. 

The credit-based shaper's operation details are beyond the scope of this document. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1313 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [418 x 271] intentionally omitted <==**

**----- Start of picture text -----**<br>
End Station A End Station B End Station C<br>MAC/Switch<br>Talker Media Listener Media Listener Media<br>Applications CA CA Applications Applications<br>P P<br>H CB CB H<br>Stream Y Y Presentation Presentation<br>Shapers BE BE Time Ingress Time Ingress<br>X Y Z X Y X Z<br>BE CB CA<br>PHY<br>MAC MAC MAC<br>Class Shapers (priorty?) (priorty?)<br>CA CB BE CA CB BE CA CB CA<br>PHY PHY PHY<br>Key:<br>Optional<br>BE: Best Effort; CB: Class B; CA: Class A Queue, Shape and/or Schedule:<br>Policer:<br>X: Stream X; Y: Stream Y; Z: Stream Z<br>cpsw-012<br>**----- End of picture text -----**<br>


**Figure 13-96. AV Stream Queuing/Policing** 

## _**13.2.1.4.6.9.2.1 Configuring the Device for 802.1Qav Operation**_ 

There is no dedicated register-set to be configured for the time-sensitive stream handling. The list of functional features of CPSW that will have to be configured are: 

- DESCRIPTORS and CHANNEL CONFIGURATIONS: 

   - CPPI TX and RX descriptors 

   - VLAN and Priority tags 

**Table 13-142. Example of TX Configuration** 

|**TX DMA CHANNEL**||**Packet Priority**|**Switch Queue Priority**|
|---|---|---|---|
|7||7|3|
|6||5|2|
|5||3|1|
|4||1|0|
||**Table**|**13-143. Example of RX Configuration**||
|**RX DMA CHANNEL**||**Packet Priority**|**Switch Queue Priority**|
|0||7|0|
|0||5|0|
|0||3|0|
|0||1|0|



- ALE Configuration: 

   - ALE in VLAN-ware mode, Non-ALE in bypass mode. 

## _**13.2.1.4.6.10 Ethernet MAC Sliver**_ 

The Ethernet port peripheral is compliant to the IEEE Std 802.3 Specification. Half-duplex mode is supported in 10/100 Mbps mode, but not in 1000 Mbps (gigabit) mode. 

1314 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## Features: 

- Synchronous 10/100/1000 Mbit operation 

- RMII/RGMII Interface 

- Hardware Error handling including CRC 

- Full-Duplex Gigabit operation (half-duplex gigabit is not supported) 

- EtherStats and 802.3Stats RMON statistics gathering support for external statistics collection module 

- Transmit CRC generation selectable on a per channel basis 

- Emulation Support 

- VLAN Aware Mode Support 

- Hardware flow control 

- Programmable Inter Packet Gap (IPG). 

## _**13.2.1.4.6.10.1 Ethernet MAC Sliver Overview**_ 

## _**13.2.1.4.6.10.1.1 CRC Insertion**_ 

The MAC generates and appends a 32-bit Ethernet CRC onto the transmitted data, if the transmit packet header PASS_CRC bit is 0h. For the Ethernet port generated CRC case, a CRC at the end of the input packet data is not allowed. 

If the header word PASS_CRC bit is set, then the last four bytes of the TX data are transmitted as the frame CRC. The four CRC data bytes should be the last four bytes of the frame and should be included in the packet byte count value. The MAC performs no error checking on the outgoing CRC when the PASS_CRC bit is set. 

## _**13.2.1.4.6.10.1.2 MTXER**_ 

The MTXER signal is only used for EEE. If an underflow condition occurs on a transmitted frame, the frame CRC will be inverted to indicate the error to the network. Underflow is a hardware error. 

## _**13.2.1.4.6.10.1.3 Adaptive Performance Optimization (APO)**_ 

The Ethernet MAC port incorporates Adaptive Performance Optimization (APO) logic that may be enabled by setting the TX_PACE bit in the CPSW_PN_MAC_CONTROL_REG register. Transmission pacing to enhance performance is enabled when set. Adaptive performance pacing introduces delays into the normal transmission of frames, delaying transmission attempts between stations, reducing the probability of collisions occurring during heavy traffic (as indicated by frame deferrals and collisions) thereby increasing the chance of successful transmission. 

When a frame is deferred, suffers a single collision, multiple collisions or excessive collisions, the pacing counter is loaded with an initial value of 31. When a frame is transmitted successfully (without experiencing a deferral, single collision, multiple collision or excessive collision) the pacing counter is decremented by one, down to zero. 

With pacing enabled, a new frame is permitted to immediately (after one IPG) attempt transmission only if the pacing counter is zero. If the pacing counter is non zero, the frame is delayed by the pacing delay, a delay of approximately four inter-packet gap delays. APO only affects the IPG preceding the first attempt at transmitting a frame. It does not affect the back-off algorithm for re-transmitted frames. 

## _**13.2.1.4.6.10.1.4 Inter-Packet-Gap Enforcement**_ 

The measurement reference for the IPG of 96-bit times is changed depending on frame traffic conditions. If a frame is successfully transmitted without collision, and MCRS is de-asserted within approximately 48-bit times of MTXEN being de-asserted, then 96-bit times is measured from MTXEN. If the frame suffered a collision, or if MCRS is not de-asserted until more than approximately 48-bit times after MTXEN is de-asserted, then 96-bit times (approximately, but not less) is measured from MCRS. 

The Ethernet port transmit inter-packet gap (IPG) may be shortened by eight bit times when short gap is enabled and triggered. Setting the [10] TX_SHORT_GAP_ENABLE bit in the CPSW_PN_MAC_CONTROL_REG register enables the gap to be shortened when triggered. The condition is triggered when the ports associated transmit packet FIFO has a user defined number of FIFO blocks used. The associated transmit FIFO blocks used value determines if the gap is shortened, and so on. The CPSW_GAP_THRESH_REG register value determines the 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1315 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

short gap threshold. If the FIFO blocks used is greater than or equal to the GAP_THRESH value then short gap is triggered. 

## _**13.2.1.4.6.10.1.5 Back Off**_ 

The Gigabit Ethernet Mac Sliver implements the 802.3 binary exponential back-off algorithm. 

## _**13.2.1.4.6.10.1.6 Programmable Transmit Inter-Packet Gap**_ 

The transmit inter-packet gap (IPG) is programmable through the CPSW_PN_MAC_CONTROL_REG register. The default value is decimal 12. The transmit IPG may be increased to the maximum value of 1FFh. Increasing the IPG is not compatible with transmit pacing. The short gap feature will override the increased gap value, so the short gap feature may not be compatible with an increased IPG. 

## _**13.2.1.4.6.10.1.7 Speed, Duplex and Pause Frame Support Negotiation**_ 

The Ethernet port can operate in half duplex or full duplex in 10/100 Mbit modes, and can operate in full duplex only in 1000 Mbit mode. Pause frame support is included in 10/100/1000 Mbit modes as configured by the host. 

## _**13.2.1.4.6.10.2 RMII Interface**_ 

The CPRMII peripheral is compliant to the RMII specification document. 

## _**13.2.1.4.6.10.2.1 Features**_ 

- Source Synchronous 10/100 Mbit operation 

- Full and Half Duplex support 

## _**13.2.1.4.6.10.2.2 RMII Receive (RX)**_ 

The CPRMII receive (RX) interface converts the input data from the external RMII PHY (or switch) into the required MII (CPGMAC) signals. The carrier sense and collision signals are determined from the RMII input data stream and transmit inputs as defined in the RMII specification. 

An asserted RMII_RXER on any di-bit in the received packet will cause an MII_RXER assertion to the CPGMAC during the packet. In 10Mbps mode, the error is not required to be duplicated on 10 successive clocks. Any di-bit which has an asserted RMII_RXER during any of the 10 replications of the data will cause the error to be propagated. 

Any received packet that ends with an improper nibble boundary aligned RMII_CRS_DV toggle will issue an MII_RXER during the packet to the CPGMAC. Also, a change in speed or duplex mode during packet operations will cause packet corruption. 

The CPRMII can accept receive packets with shortened preambles, but 0x55 followed by a 0x5D is the shortest preamble that will be recognized (1 preamble byte with the start of frame byte). At least one byte of preamble with the start of frame indicator is required to begin a packet. An asserted RMII_CRS_DV without at least a single correct preamble byte followed by the start of frame indicator will be ignored. 

## _**13.2.1.4.6.10.2.3 RMII Transmit (TX)**_ 

The CPRMII transmit (TX) interface converts the CPGMAC MII input data into the RMII transmit format. The data is then output to the external RMII PHY. 

The CPGMAC does not source the transmit error (MII_TXERR) signal. Any transmit frame from the CPGMAC with an error (underrun) will be indicated as an error by an error CRC. Transmit error is assumed to be de-asserted at all times and is not an input into the CPRMII module. Zeroes are output on RMII_TXD[1:0] for each clock that RMII_TXEN is de-asserted. 

## _**13.2.1.4.6.10.3 RGMII Interface**_ 

The CPRGMII peripheral is compliant to the RGMII specification document. 

## _**13.2.1.4.6.10.3.1 Features**_ 

- Supports 1000/100/10 Mbps speed 

- Full and Half Duplex support (CPGMAC supports only Full duplex in Gigabit mode). 

1316 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- MII mode support 

- Energy Efficient Ethernet Support 

## _**13.2.1.4.6.10.3.2 RGMII Receive (RX)**_ 

The CPRGMII receive (RX) interface converts the source synchronous DDR input data from the external RGMII PHY into the required G/MII (CPGMAC) signals. 

## _**13.2.1.4.6.10.3.3 In-Band Mode of Operation**_ 

The CPRGMII is operating in the in-band mode of operation when the RGMII_RX_INBAND input is asserted. RGMII_RX_INPUT is asserted by configuring the CTL_EN bit to 1h of the CPSW_PN_MAC_CONTROL_REG register. The link status, duplexity, and speed are determined from the RGMII input data stream RXD[3:0] when RX_CTL is deasserted, as defined in the RGMII specification. The PHY might need to be configured beforehand to output in-band data. The in-band data is indicated as shown in Table 13-144. 

**Table 13-144. In-Band Data** 

|**RXD3**|**RXD[2:1]**|**RXD[2:1]**|**RXD0**|
|---|---|---|---|
|Duplex status:<br>0h: half-duplex<br>1h: full-duplex|Link Speed:<br>0h: 10-Mbps mode<br>1h: 100-Mbps mode<br>2h: 1000-Mbps mode<br>3h: Reserved|RXC_CLK Speed:<br>2.5 MHz<br>25 MHz<br>125 MHz<br>Reserved|Link Status:<br>0h: Link is down<br>1h: Link is up|



## _**13.2.1.4.6.10.3.4 Forced Mode of Operation**_ 

The CPRGMII is operating in the forced mode of operation when the RGMII_RX_INBAND input is deasserted by setting to 0h bit CTL_EN of the CPSW_PN_MAC_CONTROL_REG register. In the forced mode of operation, the in-band data is ignored if present. The link status is forced high, and the duplexity and speed are determined from the CPSW_PN_MAC_CONTROL_REG[0] FULLDUPLEX and CPSW_PN_MAC_CONTROL_REG[7] GIG bits. If bit [7] GIG = 1h, then CPRGMII is operating in Gigabit mode. If bit [7] GIG is cleared (0h), then CPRGMII is operating in 100 Mbps mode. 

## _**13.2.1.4.6.10.3.5 RGMII Transmit (TX)**_ 

The CPRGMII transmit (TX) interface converts the CPGMAC G/MII input data into the DDR RGMII format. The DDR data is then output to the external PHY. 

The CPGMAC does not source the transmit error (TXERR) signal. Any transmit frame from the CPGMAC with an error (underrun) will be indicated as an error by an error CRC. Transmit error is assumed to be deasserted at all times and is not an input into the CPRGMII module. 

In 10/100 Mbps mode, the TXD[7:0] data bus uses only the lower nibble. The CPRGMII will output the lower nibble twice in 10/100 Mbps mode to avoid unnecessary signal switching. 

Packets will be precluded from transmission through the CPRGMII module for 4096 transmit clocks after the rising edge of RGMII_LINK. Packet transmission will begin on the first TX_CTL rising edge after the 4096 transmit clock count has expired. 

## _**13.2.1.4.6.10.4 Frame Classification**_ 

Received frames are proper (good) frames if they are between 64 and CPSW_P0_RX_MAXLEN_REG[13-0] RX_MAXLEN in length (inclusive) and contain no errors (code/align/CRC). 

Received frames are long frames if their frame count exceeds the value in the CPSW_P0_RX_MAXLEN_REG/ CPSW_PN_RX_MAXLEN_REG register. The register reset (default) value is 1518 (decimal). Long received frames are either oversized or jabber frames. Long frames with no errors are oversized frames. Long frames with CRC, code, or alignment errors are jabber frames. 

Received frames are short frames if their frame count is less than 64 bytes. Short frames that contain no errors are undersized frames. Short frames with CRC, code, or alignment errors are fragment frames. If RX_CSF_EN 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1317 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

bit in CPSW_PN_MAC_CONTROL_REG is set to 1h, undersized frames from 33 to 63 bytes will be forwarded only to the host on a best effort basis (meaning that the ALE may or may not be able to keep up with the packet rate and the short packet may be dropped due to bandwidth limitations). If RX_CSF_EN and RX_CEF_EN in CPSW_PN_MAC_CONTROL_REG are set, fragment frames from 33 to 63 bytes will also be forwarded only to the host on a best effort basis. Ethernet port received frames shorter than 33 bytes are dropped in all cases. 

A received long packet will always contain RX_MAXLEN number of bytes transferred to memory (if CPSW_PN_MAC_CONTROL_REG[22]RX_CEF_EN = 1h). An example with RX_MAXLEN = 1518 is: 

- If the frame length is 1518, then the packet is not a long packet and there will be 1518 bytes transferred to memory. 

- If the frame length is 1519, there will be 1518 bytes transferred to memory. The last three bytes will be the first three CRC bytes. 

- If the frame length is 1520, there will be 1518 bytes transferred to memory. The last two bytes will be the first two CRC bytes. 

- If the frame length is 1521, there will be 1518 bytes transferred to memory. The last byte will be the first CRC byte. 

If the frame length is 1522, there will be 1518 bytes transferred to memory. The last byte will be the last data byte. 

## _**13.2.1.4.6.10.5 Receive FIFO Architecture**_ 

This section describes the architecture of the Ethernet port’s receive FIFOs. Internal to the Gigabit Ethernet switch, all Ethernet ports have an identical associated packet FIFO. Each transmit packet FIFO contains eight logical transmit queues (priority 0 through 7 with 7 the highest priority). Each transmit FIFO memory contains 81,920 bytes total organized as 2560 by 256-bit words. Each FIFO also contains a single memory for the receive queue. Each receive FIFO memory contains a total of 32768 bytes total organized as 1024 by 256-bit words. 

## _**13.2.1.4.6.11 Embedded Memories**_ 

**Table 13-145. Embedded Memories** 

|**Memory Type Description**|**Number of Instances**|**Number of Instances**|
|---|---|---|
|Single-port 3072-word × 64 RAM|1|(Combined FIFO RAM)|
|Single-port 128-word × 28-bit RAM|1|1 (EST)|



1318 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.2.1.4.6.12 Memory Error Detection and Correction**_ 

The CPSW error detection and correction logic uses the ECC Aggregator Module. 

The ECC CPSW_ECC_VECTOR register is used to select which ECC RAM's status and control registers are currently being read or written as shown in Table 13-146. The CPSW FIFO RAMs implement ECC only on packet headers. The packet data is protected by Ethernet CRC. The ALE and EST RAMs have complete ECC as normal. 

**Table 13-146. ECC RAM to CPSW RAM Mapping** 

|**ECC RAM Number**|**CPSW RAM**|
|---|---|
|0|ALE RAM|
|1|Port 0 FIFO RAM|



## _**13.2.1.4.6.12.1 Packet Header ECC**_ 

Only packet headers bits are protected by ECC in the FIFO RAMs. The ECC_ERR_CTRL1[31-0] ECC_ROW bit is not implemented. ECC_ERR_CTRL2 [15-0] ECC_BIT1 is implemented to determine which bit of the header is flipped for an SEC error when the ECC_CRC_MODE bit is cleared in the CPSW_CONTROL_REG register. The ECC status registers return the RAM row address flipped (ECC_ROW) along with the ECC_BIT1 value. Forcing double-bit errors in testing can cause indeterminate operation if multiple used packet header bits are flipped given that only single-bit errors are fixed by the ECC logic. Header bits 207 down to 200 are not currently used in the CPSW and may be used to test double bit errors without the possibility of requiring a reset for the switch to recover from the double bit error. No header bits are flipped when ECC_CRC_MODE is set to 1h. Either the RX_ECC_ERR_EN (enable receive ECC error operations) or the TX_ECC_ERR_EN (enable transmit ECC error operations) bits must be set in the CPSW_P0_CONTROL_REG register to test ECC header errors. 

The header ECC code is stored in bits 255 down to 208. If any bit is flipped in the ECC code, the flipped bit will be corrected, but the index of the flipped bit will be reported as bit zero. This implies that when the aggregator reports that there is a SEC on bit 0, it can mean two things: either SEC on data bit 0 or SEC somewhere inside the ECC code. Any packet header with ECC error issues a pulse interrupt (ECC_PULSE_INTR) as does an ALE RAM ECC error. 

## _**13.2.1.4.6.12.2 Packet Protect CRC**_ 

Each packet received without error is passed through the CPSW memories with a generated Ethernet protect CRC. The protect CRC is checked on egress for correctness and is replaced. If the CRC is correct (no RAM bit errors), then the packet is output with the selected port CRC type. If a protect CRC error is detected on host egress then the MEMORY+PROTECT_ERROR buffer descriptor bit will be asserted so that the packet is dropped to the host. If a protect CRC error is detected on Ethernet egress then the egress CRC will be generated on the packet and at least one byte of the CRC will be inverted on output. CRC memory protect errors do not assert the ECC_PULSE_INTR signal. CRC memory protect errors are counted in the associated port statistics registers and issue an interrupt on STAT_PEND_INTR if any CRC memory protect error occurs (and the statistics for that port are enabled). When the ECC_CRC_MODE bit in the CPSW_CONTROL_REG register is set, the ECC_ERR_CTRL2 [15-0] ECC_BIT1 bit field will flip the associated column bit in any FIFO memory read operation, inducing a CRC protect error when the protect CRC is checked. No header bits are flipped when ECC_CRC_MODE is set. Either the RX_ECC_ERR_EN or the TX_ECC_ERR_EN bits must be set in the CPSW_P0_CONTROL_REG register to test packet CRC errors. 

## _**13.2.1.4.6.12.3 Aggregator RAM Control**_ 

The ECC logic for each FIFO RAM (receive and transmit) is divided into eight separate ECC encoders/decoders that encode/decode 26-bits of data each. Each of the 8 encoders (0 to 7) generates 6-bits of ECC code (48 code bits total), and each of the eight decoders (0 to 7) checks 6-bits of ECC code across the 26-bits of data (208 data bits total). The 48-bits of ECC code are passed through the RAM in the upper 48 unused bits in the header word. The header data bits and ECC code bits are shown in Table 13-147. The [15-0] ECC_BIT1 value returned on error is a 16-bit value that is the concatenation of 5 bits of zero, 3 bits of the encoder/decoder number (0 to 7), 3 bits of zero, and 5 bits of index into the indicated 26-bit encoder/decoder. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1319 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

For example, an ECC_BIT1 value of 0x0308 is bit 8 of encoder/decoder 3, which is header bit 86 (that is, (26×3) + 8). 

**Table 13-147. ECC Submodule Header Data Bit to** 

**Encoder/Decoder Mapping** 

|**Header Data Bits**|**Encoder/Decoder**|
|---|---|
|25:0|Encoder/Decoder 0 Data|
|51:26|Encoder/Decoder 1 Data|
|77:52|Encoder/Decoder 2 Data|
|103:78|Encoder/Decoder 3 Data|
|129:104|Encoder/Decoder 4 Data|
|155:130|Encoder/Decoder 5 Data|
|181:156|Encoder/Decoder 6 Data|
|207:182|Encoder/Decoder 7 Data|
|213:208|Encoder/Decoder 0 ECC|
|219:214|Encoder/Decoder 1 ECC|
|225:220|Encoder/Decoder 2 ECC|
|231:226|Encoder/Decoder 3 ECC|
|237:232|Encoder/Decoder 4 ECC|
|243:238|Encoder/Decoder 5 ECC|
|249:244|Encoder/Decoder 6 ECC|
|255:250|Encoder/Decoder 7 ECC|



## _**13.2.1.4.6.13 Ethernet Port Flow Control**_ 

The Ethernet port have flow control available for transmit and receive. Transmit flow control stops the Ethernet port from transmitting packets to the wire (switch egress) in response to a received pause frame. Transmit flow control does not depend on FIFO usage. 

The Ethernet port have flow control available for receive operations (packet ingress). Ethernet port receive flow control is initiated when enabled and triggered. Packets received on an Ethernet port can be sent to the CPPI port. The destination port can trigger the receive Ethernet port flow control. An Ethernet destination port triggers another Ethernet receive flow control when the destination port is full. 

When a packet is received on an Ethernet port interface with enabled flow control the below occurs: 

- The packet will be sent to all ports that currently have room to take the entire packet. 

- The packet will be retried until successful to all ports that indicate they don't have room for the packet. 

The flow control trigger to the Ethernet port will be asserted until the packet has been sent, and there is room in the logical receive FIFO for packet runout from another flow control trigger (RX_BLK_CNT = 0h). Ethernet port receive flow control is disabled by default on reset. Ethernet port receive flow control requires that the RX_FLOW_EN bit in CPSW_PN_MAC_CONTROL_REG be set to 1h. When receive flow control is enabled on a port, the port's associated FIFO block allocation must be adjusted. The port RX allocation must increase from the default three blocks to accommodate the flow control runout. A corresponding decrease in the TX block allocation is required. If a sending port ignores a pause frame then packets may overrun on receive (and be dropped) but will not be dropped on transmit. 

## _**13.2.1.4.6.13.1 Ethernet Receive Flow Control**_ 

For every Ethernet port to be configured for fullduplex receive flow control, write a value of decimal 7 to the CPSW_PN_MAX_BLKS_REG[7-0] RX_MAX_BLKS bit field, and a value of decimal 13 to the CPSW_PN_MAX_BLKS_REG[15-8] TX_MAX_BLKS register. This re-allocation allows for flow control runout on the receive FIFO at the expense of FIFO memory on the Ethernet transmit side. 10/100Mbps half-duplex 

1320 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

collision based receive flow control does not need this re-allocation. Receive flow control is enabled by the RX_FLOW_EN bit in the CPSW_PN_MAC_CONTROL_REG register. 

## _**13.2.1.4.6.13.1.1 Collision Based Receive Buffer Flow Control**_ 

Collision-based receive buffer flow control provides a means of preventing frame reception when the port is operating in half-duplex mode (FULLDUPLEX is cleared in CPSW_PN_MAC_CONTROL_REG). When receive flow control is enabled and triggered, the port will generate collisions for received frames. The jam sequence transmitted will be the twelve byte sequence C3.C3.C3.C3.C3.C3.C3.C3.C3.C3.C3.C3 (hex). The jam sequence will begin no later than approximately as the source address starts to be received. Note that these forced collisions will not be limited to a maximum of 16 consecutive collisions, and are independent of the normal backoff algorithm. Receive flow control does not depend on the value of the incoming frame destination address. A collision will be generated for any incoming packet, regardless of the destination address. 

## _**13.2.1.4.6.13.1.2 IEEE 802.3X Based Receive Flow Control**_ 

IEEE 802.3x based receive flow control provides a means of preventing frame reception when the port is operating in full-duplex mode (FULLDUPLEX bit is set in the CPSW_PN_MAC_CONTROL_REG register). When receive flow control is enabled and triggered, the port will transmit a pause frame to request that the sending station stop transmitting for the period indicated within the transmitted pause frame. 

The Ethernet port will transmit a pause frame to the reserved multicast address at the first available opportunity (immediately if currently idle, or following the completion of the frame currently being transmitted). The pause frame will contain the maximum possible value for the pause time (FFFFh). The MAC will count the receive pause frame time (decrements FF00h down to 0) and retransmit an outgoing pause frame if the count reaches zero. When the flow control request is removed, the MAC will transmit a pause frame with a zero pause time to cancel the pause request. 

Note that transmitted pause frames are only a request to the other end station to stop transmitting. Frames that are received during the pause interval will be received normally (provided the RX FIFO is not full at which time the receive FIFO will overrun and CPSW_STAT0_RX_BOTTOM_OF_FIFO_DROP/ CPSW_STAT1_RX_BOTTOM_OF_FIFO_DROP[31-0] COUNT value will increment). 

Pause frames will be transmitted if enabled and triggered regardless of whether or not the port is observing the pause time period from an incoming pause frame. 

The Ethernet port will transmit pause frames as described below: 

- The 48-bit reserved multicast destination address 01.80.C2.00.00.01. 

- The 48-bit source address - from SL_SA[47-0] input. 

- The 16-bit length/type field containing the value 88.08 

- The 16-bit pause opcode equal to 00.01 

- The 16-bit pause time value FF.FF. A pause-quantum is 512 bit-times. Pause frames sent to cancel a pause request will have a pause time value of 00.00. 

- Zero padding to 64-byte data length (The Ethernet port will transmit only 64 byte pause frames). 

- The 32-bit frame-check sequence (CRC word). 

All quantities above are hexadecimal and are transmitted most-significant byte first. The least-significant bit is transferred first in each byte. 

If CPSW_PN_MAC_CONTROL_REG[3] RX_FLOW_EN is cleared to 0h while the pause time is nonzero, then the pause time will be cleared to 0h and a 0 count pause frame will be sent. 

## _**13.2.1.4.6.13.2 Flow Control Trigger**_ 

Receive flow control is triggered (when enabled), when the number of words in the receive FIFO is greater than or equal to the value written in the CPSW_PN_RX_FLOW_THRESH_REG[8-0] COUNT bit field. The flow control packet runout is then contained in the remainder of the receive FIFO. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1321 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.6.13.3 Ethernet Transmit Flow Control**_ 

Incoming pause frames are acted upon, when enabled, to prevent the Ethernet port from transmitting any further frames. Incoming pause frames are only acted upon when the [0] FULLDUPLEX and [4] TX_FLOW_EN bits in the CPSW_PN_MAC_CONTROL_REG register are set. Pause frames are not acted upon in half-duplex mode. Pause frame action will be taken if enabled, but normally the frame will be filtered and not transferred to memory. MAC control frames will be transferred to memory if the [24] RX_CMF_EN (RX Copy MAC Control Frames Enable) bit in the CPSW_PN_MAC_CONTROL_REG register is set. The [4] TX_FLOW_EN and [0] FULLDUPLEX bits effect whether or not MAC control frames are acted upon, but they have no effect upon whether or not MAC control frames are transferred to memory or filtered. 

Pause frames are a subset of MAC Control Frames with an opcode field = 0001h. Incoming pause frames will only be acted upon by the port if: 

- [4] TX_FLOW_EN is set in CPSW_PN_MAC_CONTROL_REG register, and 

- the RX maximum frame length is 64 bytes inclusive (CPSW_PN_RX_MAXLEN_REG[13-0] RX_MAXLEN), and 

- the frame contains no CRC error or align/code errors. 

The pause time value from valid frames will be extracted from the two bytes following the opcode. The pause time will be loaded into the port's transmit pause timer and the transmit pause time period will begin. 

If a valid pause frame is received during the transmit pause time period of a previous transmit pause frame then: 

- if the destination address is not equal to the reserved multicast address or any enabled or disabled unicast address, then the transmit pause timer will immediately expire, or 

- if the new pause time value is zero then the transmit pause timer will immediately expire, else the port transmit pause timer will immediately be set to the new pause frame pause time value. (Any remaining pause time from the previous pause frame will be discarded). 

If [4] TX_FLOW_EN in CPSW_PN_MAC_CONTROL_REG register is cleared, then the pause-timer will immediately expire. 

The port will not start the transmission of a new data frame any sooner than 512-bit times after a pause frame with a non-zero pause time has finished being received (MRXDV going inactive). No transmission will begin until the pause timer has expired (the port may transmit pause frames in order to initiate outgoing flow control). Any frame already in transmission when a pause frame is received will be completed and unaffected. 

Incoming pause frames consist of the below: 

- A 48-bit destination address equal to: 

   - The reserved multicast destination address 01.80.C2.00.00.01, or the Ethernet port SL_SA [47:0] input. 

- The 48-bit source address of the transmitting device. 

- The 16-bit length/type field containing the value 88.08 

- The 16-bit pause opcode equal to 00.01 

- The 16-bit CPSW_PN_MAC_TX_PAUSETIMER_REG[15-0] TX_PAUSETIMER. A pause-quantum is 512 bit-times. 

- Padding to 64-byte data length. 

- The 32-bit frame-check sequence (CRC word). 

All quantities above are hexadecimal and are transmitted most-significant byte first. The least-significant bit is transferred first in each byte. 

The padding is required to make up the frame to a minimum of 64 Bytes. The standard allows pause frames longer than 64 Bytes to be discarded or interpreted as valid pause frames. The Ethernet port will recognize any pause frame between 64 Bytes and CPSW_PN_RX_MAXLEN_REG[13-0] RX_MAXLEN bytes in length. 

## _**13.2.1.4.6.14 Energy Efficient Ethernet Support (802.3az)**_ 

Energy Efficient Ethernet (EEE) allows the LPSC to turn off the module clock during inactive periods as determined by network and host traffic. The module can then be awakened by host queued transmit packet(s) 

1322 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

or by a port’s external Ethernet PHY. The module EEE clock stop interface is used by the external controller to control module EEE operations. EEE operations are configured as shown below: 

1. The 12-bit EEE clock pre-scale value is written to the CPSW_EEE_PRESCALE_REG register. The prescaler is used to clock all EEE-related counters 

2. The port Idle to LPI count values (CPSW_PN_IDLE2LPI_REG[23-0] COUNT) are written with the desired values 

3. The port LPI to Wake count values (CPSW_PN_LPI2WAKE_REG[23-0] COUNT) are written with the desired values 

4. The [0] EEE_EN bit is set in the switch CPSW_SS_CONTROL_REG register 

EEE operation can begin after configuration. The host allows (through LPSC) the CPSW to enter a low power state by asserting the EEE_CLKSTOP_REQ signal. There are no requirements on host queues or traffic in order for the host to assert or de-assert EEE_CLKSTOP_REQ to the CPSW. 

Each Ethernet port has a transmit and a receive LPI (low power indicate) state. The PHY indicates LPI by asserting MRXER with a MRXD[7:0] value of 0x01 while MRXDV is deasserted (inter-packet gap). The Ethernet transmit port indicates LPI after the CPSW_PN_IDLE2LPI_REG value has been counted (the transmit port has gone idle for the configured amount of time). If another packet is received for transmit during the count then the count is restarted. When the transmit port has been idle for the Idle to LPI time, the transmit port enters the LPI state and indicates LPI to the associated PHY. The LPI is indicated to the external PHY by an asserted MTXER with a MTXD[7:0] while MTXEN is deasserted (inter-packet gap). The CPPI (port 0) LPI state includes transmit and receive. The CPPI LPI state is entered when the CPPI transmit and receive have both been idle for the Idle to LPI time (CPSW_P0_IDLE2LPI_REG). The Idle to LPI time value for all ports must be large relative to the switch latency to ensure that the count is not able to complete between successive packets. 

## **Note** 

External PHY signaling has the following conditions: 

- RGMII is a DDR interface. TXEN and TXER are the sampled values of TX_CTL at the rising and the falling TXC edges, respectively. RXDV and RXER are the sampled values of RX_CTL at the rising and the falling RXC clock edges, respectively 

- In RMII mode, EEE is not supported. 

When all transmit and receive ports are in the LPI state (CPSW LPI state), the EEE_CLKSTOP_ACK signal is asserted, and the LPSC is allowed to stop the module clock. When EEE_CLKSTOP_ACK is asserted, the clock may be turned on and off as desired by the host. The host is allowed to restart the clock, perform target read/write operations to the CPSW memory address space, and then turn off the clock again while EEE_CLKSTOP_ACK is asserted. 

The software can remove and disable from re-entering the CPSW LPI state by restarting the module clock and then de-asserting EEE_CLKSTOP_REQ. There must be at least one rising edge of the clock before EEE_CLKSTOP_REQ is de-asserted. The module EEE_CLKSTOP_ACK output signal will be deasserted on the clock after the de-assertion of EEE_CLKSTOP_REQ. The host may queue CPPI receive packets at any time without regard to the CPSW module LPI state. The Host must deassert EEE_CLKSTOP_REQ on wakeup for a minimum of two clock periods. If EEE_CLKSTOP_REQ is deasserted for less than 5 clock periods for a wakeup event from the host to a particular Ethernet port (or visa versa), then the wakeup event will not cause the other Ethernet port to awaken. 

The external Ethernet PHY’s can also wakeup the LPSC by removing the Ethernet receive LPI indication. If the CPSW module is in Idle state with EEE_CLKSTOP_ACK asserted and the receive LPI indication is removed, the EEE_CLKSTOP_WAKEUP signal will be asynchronously asserted. On wakeup, the LPSC restarts the clock and de-assert the EEE_CLKSTOP_REQ signal. The EEE_CLKSTOP_WAKEUP signal will be synchronously deasserted with EEE_CLKSTOP_ACK. Upon the deassertion of EEE_CLKSTOP_REQ, the Ethernet ports will count the CPSW_PN_LPI2WAKE_REG time for each port at which time the port is available for transmit. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1323 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.6.15 Ethernet Switch Latency**_ 

When CPSW is configured as a store and forward switch, the switch latency is defined as the amount of time between the end of packet reception of the received packet to the start of the output packet transmit. 

The store and forward latency is shown in Table 13-148: 

**Table 13-148. Switch Latency** 

|**Mode**||**Latency**||
|---|---|---|---|
||Gig (1000)||880 ns|
||100||1.3 µs|
||10||6.5 µs|



## _**13.2.1.4.6.16 MAC Emulation Control**_ 

The emulation control input (EMUSUSP) and submodule emulation control registers allow CPSW operation to be completely or partially suspended. Each Ethernet port has associated emulation control registers (CPSW_EM_CONTROL_REG and CPSW_PN_MAC_EMCONTROL_REG). The submodule emulation control registers must be accessed to facilitate CPSW emulation control. The CPSW module enters the emulation suspend state if all three submodules are configured for emulation suspend and the emulation suspend input is asserted. A partial emulation suspend state is entered if one or two submodules is configured for emulation suspend and the emulation suspend input is asserted. Emulation suspend occurs at packet boundaries. The emulation control feature is implemented for compatibility with other peripherals. 

## **Ethernet port Emulation Control** 

The emulation control input (TBEMUSUP) and register bits (SOFT and FREE bits in the CPSW_PN_MAC_EMCONTROL_REG register) allow Ethernet port operation to be suspended. When the emulation suspend state is entered, the Ethernet port will stop processing receive and transmit frames at the next frame boundary. Any frame currently in reception or transmission will be completed normally without suspension. For receive, frames that are detected by the Ethernet port after the suspend state is entered are ignored. 

Table 13-149 shows the operations of the emulation control input and register bits. 

**Table 13-149. Emulation Control Input** 

|**EMUSUSP**||**SOFT**||**FREE**||**Description**|
|---|---|---|---|---|---|---|
||0||X||X|Normal Operation|
||1||0||0|Normal Operation|
||1||1||0|Emulation Suspend|
||1||X||1|Normal Operation|



## _**13.2.1.4.6.17 MAC Command IDLE**_ 

The CMD_IDLE bit in the CPSW_PN_MAC_CONTROL_REG register allows MAC operation to be suspended. When the idle state is commanded, the MAC will stop processing receive and transmit frames at the next frame boundary. Any frame currently in reception or transmission will be completed normally without suspension. For transmission, any complete or partial frame in the TX cell FIFO will be transmitted. For receive, frames that are detected by the MAC after the suspend state is entered are ignored. No statistics will be kept for ignored frames. Commanded idle is similar in operation to emulation control and clock stop. 

## _**13.2.1.4.6.18 CPSW Network Statistics**_ 

The CPSW has a set of statistics that record events associated with frame traffic on selected switch ports. The statistics values are cleared to zero 38 clocks after the rising edge of CPSW0_RST. When one or more port enable (Pn_STAT_EN) bits in the CPSW_STAT_PORT_EN_REG register are set, all statistics registers are write to decrement. The value written will be subtracted from the register value with the result being stored in the register. If a value greater than the statistics value is written, then zero will be written to the register (writing 

1324 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

0xFFFF FFFF clears a statistics location). When all port enable bits are cleared to zero, all statistics registers are read/write (normal write direct, so writing 0x0000 0000 clears a statistics location). All write accesses must be 32-bit accesses. 

The statistics interrupt (STAT_PEND0) will be issued if enabled when any statistics value is greater than or equal to 0x8000 0000. The statistics interrupt is removed by writing to decrement any statistics value greater than 0x8000 0000. The statistics are mapped into internal memory space and are 32-bits wide. All statistics rollover from 0xFFFF FFFF to 0x0000 0000. 

Table 13-150 and Table 13-151 summarize network statistics. 

## _**13.2.1.4.6.18.1 Rx-only Statistics Descriptions**_ 

## _**13.2.1.4.6.18.1.1 Good Rx Frames (Offset = 3A000h)**_ 

## **All ports** 

The total number of good frames received on the port. A good frame is defined to be: 

- Any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Had a length of 64 to RX_MAXLEN bytes inclusive 

- Had no CRC error, alignment error or code error. 

See the Section 13.2.1.4.6.18.1.6, _Rx Align/Code Errors_ and Section 13.2.1.4.6.18.1.5, _Rx CRC errors_ statistic descriptions for definitions of alignment, code and CRC errors. 

Overruns have no effect upon this statistic. 

## _**13.2.1.4.6.18.1.2 Broadcast Rx Frames (Offset = 3A004h)**_ 

## **All ports** 

The total number of good broadcast frames received on the port. A good broadcast frame is defined to be: 

- Any data or MAC control frame which was destined for address FF.FF.FF.FF.FF.FF 

- Had a length of 64 to RX_MAXLEN bytes inclusive 

- Had no CRC error, alignment error or code error. 

See the Section 13.2.1.4.6.18.1.6, _Rx Align/Code Errors_ and Section 13.2.1.4.6.18.1.5, _Rx CRC errors_ statistic descriptions for definitions of alignment, code and CRC errors. 

Overruns have no effect upon this statistic. 

## _**13.2.1.4.6.18.1.3 Multicast Rx Frames (Offset = 3A008h)**_ 

## **All ports** 

The total number of good multicast frames received on the port. A good multicast frame is defined to be: 

- Any data or MAC control frame which was destined for any multicast address other than FF.FF.FF.FF.FF.FF 

- Had a length of 64 to RX_MAXLEN bytes inclusive 

- Had no CRC error, alignment error or code error 

See the Section 13.2.1.4.6.18.1.6, _Rx Align/Code Errors_ and Section 13.2.1.4.6.18.1.5, _Rx CRC errors_ statistic descriptions for definitions of alignment, code and CRC errors. 

Overruns have no effect upon this statistic. 

## _**13.2.1.4.6.18.1.4 Pause Rx Frames (Offset = 3A00Ch)**_ 

## **Ethernet port N where N = 1 to 2** 

The total number of IEEE 802.3X pause frames received by the port (whether acted upon or not). Such a frame: 

- Contained any unicast, broadcast, or multicast address 

- Contained the length/type field value 88.08 (hex) and the opcode 0x0001 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1325 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- Was of length 64 to RX_MAXLEN bytes inclusive 

- Had no CRC error, alignment error or code error 

- Pause-frames had been enabled on the port (TX_FLOW_EN = 1h). 

The port could have been in either half or full-duplex mode. 

See the Section 13.2.1.4.6.18.1.6, _Rx Align/Code Errors_ and Section 13.2.1.4.6.18.1.5, _Rx CRC errors_ statistic descriptions for definitions of alignment, code and CRC errors. 

Overruns have no effect upon this statistic. 

## _**13.2.1.4.6.18.1.5 Rx CRC Errors (Offset = 3A010h)**_ 

## **All ports** 

The total number of frames received on the port that experienced a CRC error. Such a frame: 

- Was any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Was of length 64 to RX_MAXLEN bytes inclusive 

- Had no code/align error 

- Had a CRC error 

Overruns have no effect upon this statistic. 

A CRC error is defined to be: 

- A frame containing an even number of nibbles, and 

- Failing the Frame Check Sequence test. 

## _**13.2.1.4.6.18.1.6 Rx Align/Code Errors (Offset = 3A014h)**_ 

## **Ethernet port N where N = 1 to 2** 

The total number of frames received on the port that experienced an alignment error or code error. Such a frame: 

- Was any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Was of length 64 to RX_MAXLEN bytes inclusive 

- Had either an alignment error, or a code error. 

Overruns have no effect upon this statistic. 

An alignment error is defined to be: 

- A frame containing an odd number of nibbles 

- Failing the Frame Check Sequence test if the final nibble is ignored 

A code error is defined to be a frame which has been discarded because the port’s MRXER pin driven with a one for at least one bit-time’s duration at any point during the frame’s reception. 

## **Note** 

RFC 1757 etherStatsCRCAlignErrors Ref. 1.5 can be calculated by summing Rx Align/Code Errors and Rx CRC errors. 

## _**13.2.1.4.6.18.1.7 Oversize Rx Frames (Offset = 3A018h)**_ 

## **All ports** 

The total number of oversized frames received on the port. An oversized frame is defined to be: 

- Was any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Was greater than RX_MAXLEN in bytes 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1326 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- Had no CRC error, alignment error, or code error. 

See the Section 13.2.1.4.6.18.1.6, _Rx Align/Code Errors_ and Section 13.2.1.4.6.18.1.5, _Rx CRC errors_ statistic descriptions for definitions of alignment, code and CRC errors. 

Overruns have no effect upon this statistic. 

## _**13.2.1.4.6.18.1.8 Rx Jabbers (Offset = 3A01Ch)**_ 

## **All ports** 

The total number of jabber frames received on the port. A jabber frame: 

- Was any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Was greater than RX_MAXLEN in bytes 

- Had a CRC error, alignment error or code error 

See the Section 13.2.1.4.6.18.1.6, _Rx Align/Code Errors_ and Section 13.2.1.4.6.18.1.5, _Rx CRC errors_ statistic descriptions for definitions of alignment, code and CRC errors. 

Overruns have no effect upon this statistic. 

## _**13.2.1.4.6.18.1.9 Undersize (Short) Rx Frames (Offset = 3A020h)**_ 

## **All ports** 

The total number of undersized frames received on the port. An undersized frame is defined to be: 

- Was any data frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Was less than 64 bytes 

- Had no CRC error, alignment error, or code error 

See the Section 13.2.1.4.6.18.1.6, _Rx Align/Code Errors_ and Section 13.2.1.4.6.18.1.5, _Rx CRC errors_ statistic descriptions for definitions of alignment, code and CRC errors. 

Overruns have no effect upon this statistic. 

## _**13.2.1.4.6.18.1.10 Rx Fragments (Offset = 3A024h)**_ 

## **Ethernet port N where N = 1 to 2** 

The total number of frame fragments received on the port. A frame fragment is defined to be: 

- Any data frame (address matching does not matter) 

- Less than 64 bytes long 

- Having a CRC error, an alignment error, or a code error 

- Not the result of a collision caused by half-duplex, collision-based flow control 

See the Section 13.2.1.4.6.18.1.6, _Rx Align/Code Errors_ and Section 13.2.1.4.6.18.1.5, _Rx CRC errors_ statistic descriptions for definitions of alignment, code and CRC errors. 

Overruns have no effect upon this statistic. 

## _**13.2.1.4.6.18.1.11 RX IPG Error (Offset = 3A05Ch)**_ 

The total number of 10G frames received on a port that had a correct preamble but did not have at least five bytes of IDLE preceding the frame. This does not indicate if the frame with the IPG error was kept or ignored. 

## _**13.2.1.4.6.18.1.12 ALE Drop (Offset = 3A028h)**_ 

## **All ports** 

The total number of frames received on a port such that the destination address was not equal to the source address and the packet was not destined to the port it was received on, but the frame was not forwarded to any port (the PORT_MASK was zero). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1327 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- Any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Any length (including less than 64 bytes and greater than RX_MAXLEN bytes) 

- had no CRC error, alignment error, or code error 

- the destination address was not equal to the source address 

- the packet was not destined for the port it was receive on 

- had a zero PORT_MASK 

## _**13.2.1.4.6.18.1.13 ALE Overrun Drop (Offset = 3A02Ch)**_ 

## **All ports (non cut-thru mode)** 

The total number of frames received on a port that were dropped (zero PORT_MASK) due to exceeding the maximum ALE lookup rate (Port 0 should not have ALE Overrun Drops because the ingress rate is controlled to prevent it). This statistic should be zero and when non-zero indicates a system clock issue or indicates that short packets were sent with RX_CSF_EN at a rate that exceeded the maximum lookup rate. 

- Any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Any length (including less than 64 bytes and greater than RX_MAXLEN bytes) 

- The port has no receive priorities enabled for cut-thru, and 

- the maximum ALE lookup rate was exceeded so the lookup was aborted and the packet was dropped. 

## _**13.2.1.4.6.18.1.14 Rx Octets (Offset = 3A030h)**_ 

## **All ports** 

The total number of bytes in all good frames received on the port. A good frame is defined to be: 

- Any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Of length 64 to RX_MAXLEN bytes inclusive 

- Had no CRC error, alignment error or code error 

See the Section 13.2.1.4.6.18.1.6, _Rx Align/Code Errors_ and Section 13.2.1.4.6.18.1.5, _Rx CRC errors_ statistic descriptions for definitions of alignment, code and CRC errors. 

Overruns have no effect upon this statistic. 

## _**13.2.1.4.6.18.1.15 Rx Bottom of FIFO Drop (Offset = 3A084h)**_ 

## **Ethernet port N where N = 1 to 2** 

The total number of frames received on a port that overran the port’s receive FIFO and were dropped (bottom of receive FIFO). Port 0 (CPPI receive port) should not drop packets on receive because port 0 receive flow control should be enabled. The Ethernet ports will only drop packets in the receive FIFO when receive flow control is enabled and the sending port ignores sent pause frame and then overruns the receive FIFO. An overrun frame is defined to be: 

- Any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Any length (including less than 64 bytes and greater than RX_MAXLEN bytes) 

- Was dropped on port 0 due to a lack of memory space in the receive FIFO. 

## **Note** 

This statistic should be zero if proper flow control is being followed. 

## **Host port 0** 

1328 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

This statistic also counts frames dropped on port 0 that were 17 to 33 bytes (only for port 0). For Ethernet ports, the drop count for frames shorter than 33 bytes is included in the undersized or fragment count. Port 0 simply gives an indication that a packet was dropped. No other statistics are counted for frames shorter than 33 bytes. 

## _**13.2.1.4.6.18.1.16 Portmask Drop (Offset = 3A088h)**_ 

## **All ports** 

The total number of frames received on a port that were dropped by the ALE (the ALE did not forward the packet to any port). Port mask drop frame is defined to be: 

- Any data or MAC control frame 

- Any length greater than 32 bytes 

- Was dropped by the ALE due to PORT_MASK=0 (was not sent to any destination port) 

- The frame could have been dropped due to error or other counted reason, so it could be counted elsewhere also. 

## **Note** 

This statistic does not count in the overall total as it includes every packet received greater than 32 bytes that had a zero PORT_MASK. 

## _**13.2.1.4.6.18.1.17 Rx Top of FIFO Drop (Offset = 3A08Ch)**_ 

## **All ports** 

The total number of frames received on a port that had a start-of-frame (SOF) overrun on any destination port egress (when attempting to load the packet from the top of the ingress port receive FIFO into any other port’s transmit FIFO). If a multicast/broadcast packet is dropped by multiple destination ports then this statistic will increment by the number of ports that dropped the packet. Rx Top Of FIFO Drop is defined to be: 

- Any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Any length (including less than 64 bytes and greater than RX_MAXLEN bytes) 

- had no CRC error, alignment error or code error 

- had a SOF of frame overrun on another port egress. 

## _**13.2.1.4.6.18.1.18 ALE Rate Limit Drop (Offset = 3A090h)**_ 

## **All ports** 

The total number of frames received on a port that were dropped (zero PORT_MASK) due to receive rate limiting on this port or due to transmit rate limiting on any destination port (not sent to all expected destination ports if transmit rate limiting). 

- Any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Any length (including less than 64 bytes and greater than RX_MAXLEN bytes) 

- had no CRC error, alignment error, or code error 

- the receive rate was exceeded and the packet was dropped, or the transmit rate was exceeded to any destination port and the packet was dropped to one or more expected destination ports (indicates that the destinations were reduced due to rate limiting). 

## _**13.2.1.4.6.18.1.19 ALE VLAN Ingress Check Drop (Offset = 3A094h)**_ 

## **All ports** 

The total number of frames received on a port that were dropped (zero PORT_MASK) due to VLAN ingress check failure. 

- Any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1329 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- Any length (including less than 64 bytes and greater than RX_MAXLEN bytes) 

- had no CRC error, alignment error, or code error 

- the VLAN ID ingress check failed (the receive port was not in the group) 

- The address lookup did not return a match with the SUPER bit set. 

## _**13.2.1.4.6.18.1.19.1 ALE DA=SA Drop (Offset = 3A098h)**_ 

## **All ports** 

The total number of frames received on a port that were dropped (zero PORT_MASK) due to destination address equal to source address. 

- Any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode 

- Any length (including less than 64 bytes and greater than RX_MAXLEN bytes) 

- had no CRC error, alignment error, or code error 

- the destination address was equal to the source address 

- the source address was not an entry in the table. 

## _**13.2.1.4.6.18.1.19.2 Block Address Drop (Offset = 3A09Ch)**_ 

The total number of frames received on a port that were dropped (zero PORT_MASK) due to the destination or source address being blocked. 

- was any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode, and 

- Any length (including less than 64 bytes and greater than RX_MAXLEN bytes) 

- had no CRC error, alignment error, or code error, and 

- the source or destination address matched a table entry with the block bit set. 

## _**13.2.1.4.6.18.1.19.3 ALE Secure Drop (Offset = 3A0A0h)**_ 

The total number of frames received on a port that were dropped (zero port_mask) due to a secure violation (the source address is owned by a different receive port). 

- was any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode, and 

- Any length (including less than 64 bytes and greater than RX_MAXLEN bytes) 

- had no CRC error, alignment error, or code error, and 

- the source address is an entry in the table with the SECURE bit set and a port number for a different receive port. 

## _**13.2.1.4.6.18.1.19.4 ALE Authentication Drop (Offset = 3A0A4h)**_ 

The total number of frames received on a port that were dropped (zero port_mask) due to authentication failure. 

- was any data or MAC control frame which matched a unicast, broadcast or multicast address, or matched due to promiscuous mode, and 

- Any length (including less than 64 bytes and greater than RX_MAXLEN bytes) 

- had no CRC error, alignment error, or code error, and 

- CPSW_ALE_CONTROL[1] ENABLE_AUTH_MODE is set to 1h, and 

- the source address is not equal to the destination address, and 

- the source address is not a table entry, and 

- the destination address is not a table entry with the SUPER bit set. 

## _**13.2.1.4.6.18.1.19.5 ALE Unknown Unicast (Offset = 3A0A8h)**_ 

## **All ports** 

The total number of frames received on a port that had a unicast destination address with an unknown source address. 

- was any data frame with a unicast destination address 

- the source address was not a table entry 

1330 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- was of length 64 to RX_MAXLEN bytes inclusive 

- had no CRC error, alignment error, or code error 

Note: The ALE Unknown Unicast Bytecount statistic is the number of bytes contained in the ALE Unknown Unicast frames. 

## _**13.2.1.4.6.18.1.19.6 ALE Unknown Unicast Bytecount (Offset = 3A0ACh)**_ 

The total number of bytes received on a port that had a unicast destination address with an unknown source address. 

## _**13.2.1.4.6.18.1.19.7 ALE Unknown Multicast (Offset = 3A0B0h)**_ 

The total number of frames received on a port that had a multicast destination address with an unknown source address. The frame is defined to be: 

- was any data frame with a multicast destination address 

- the source address was not a table entry, and 

- was of length 64 to RX_MAXLEN bytes inclusive 

- had no CRC error, alignment error or code error 

Note: The ALE Unknown Multicast Bytecount statististic is the number of bytes contained in the ALE Unknown Multicast frames. 

## _**13.2.1.4.6.18.1.19.8 ALE Unknown Multicast Bytecount (Offset = 3A0B4h)**_ 

The total number of bytes received on a port that had a multicast destination address with an unknown source address. 

## _**13.2.1.4.6.18.1.19.9 ALE Unknown Broadcast (Offset = 3A0B8h)**_ 

The total number of frames received on a port that had a broadcast destination address with an unknown source address. The frame is defined to be: 

- was any data frame with a broadcast destination address 

- the source address was not a table entry, and 

- was of length 64 to RX_MAXLEN bytes inclusive 

- had no CRC error, alignment error or code error 

Note: The ALE Unknown Broadcast Bytecount statistic is the number of bytes contained in the ALE Unknown Broadcast frames. 

## _**13.2.1.4.6.18.1.19.10 ALE Unknown Broadcast Bytecount (Offset = 3A0BCh)**_ 

The total number of bytes received on a port that had a broadcast destination address with an unknown source address. 

## _**13.2.1.4.6.18.1.19.11 ALE Policer Match (Offset = 3A0C0h)**_ 

## **All ports** 

The total number of frames received on a port that matched a policer. The frame is defined to be: 

- was any data frame 

- matched a condition on a policer, 

- was of length 64 to RX_MAXLEN bytes inclusive 

- had no CRC error, alignment error, or code error 

## _**13.2.1.4.6.18.1.19.12 ALE Policer Match Red (Offset = 3A0C4h)**_ 

The total number of frames received on a port that had matched a policer and the condition was red. The frame is defined to be: 

- was any data frame 

- matched the condition red on a policer, 

- was of length 64 to RX_MAXLEN bytes inclusive 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1331 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- had no CRC error, alignment error, or code error 

## _**13.2.1.4.6.18.1.19.13 ALE Policer Match Yellow (Offset = 3A0C8h)**_ 

The total number of frames received on a port that had matched a policer and the condition was yellow. The frame is defined to be: 

- was any data frame 

- matched the condition yellow on a policer, 

- was of length 64 to RX_MAXLEN bytes inclusive 

- had no CRC error, alignment error, or code error 

## _**13.2.1.4.6.18.2 Tx-only Statistics Descriptions**_ 

The maximum and minimum transmit frame size is software controllable. 

Transmit overruns have no effect on TX statistics. They are counted separately. 

## _**13.2.1.4.6.18.2.1 Good Tx Frames (Offset = 3A034h)**_ 

## **All ports** 

The total number of good frames transmitted on the port. A good frame is defined to be: 

- Any data or MAC control frame which matched a unicast, broadcast or multicast address 

- Any length 

- Had no late or excessive collisions, no carrier loss and no underrun 

## _**13.2.1.4.6.18.2.2 Broadcast Tx Frames (Offset = 3A038h)**_ 

## **All ports** 

The total number of good broadcast frames transmitted on the port. A good broadcast frame is defined to be: 

- Any data or MAC control frame which was destined for only address FF.FF.FF.FF.FF.FF 

- Any length 

- Had no late or excessive collisions, no carrier loss and no underrun 

## _**13.2.1.4.6.18.2.3 Multicast Tx Frames (Offset = 3A03Ch)**_ 

## **All ports** 

The total number of good multicast frames transmitted on the port. A good multicast frame is defined to be: 

- Any data or MAC control frame which was destined for any multicast address other than FF.FF.FF.FF.FF.FF 

- • Any length 

- Had no late or excessive collisions, no carrier loss and no underrun 

## _**13.2.1.4.6.18.2.4 Pause Tx Frames (Offset = 3A040h)**_ 

## **Ethernet port N where N = 1 to 2** 

This statistic indicates the number of IEEE 802.3X pause frames transmitted by the port. 

Pause frames cannot contain a CRC error because they are created in the transmitting MAC, so these error conditions have no effect upon the statistic. Pause frames sent by software will not be included in this count. 

Since pause frames are only transmitted in full duplex, carrier loss and collisions have no effect upon this statistic. 

Transmitted pause frames are always 64-byte multicast frames so will appear in the _Tx Multicast Frames_ and _64octet Frames_ statistics. 

## _**13.2.1.4.6.18.2.5 Deferred Tx Frames (Offset = 3A044h)**_ 

## **Ethernet port N where N = 1 to 2** 

The total number of frames transmitted on the port that first experienced deferment. Such a frame: 

1332 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- Was any data or MAC control frame destined for any unicast, broadcast or multicast address 

- Was any size 

- Had no carrier loss and no underrun 

- Experienced no collisions before being successfully transmitted 

- Found the medium busy when transmission was first attempted, so had to wait. 

CRC errors have no effect upon this statistic. 

## _**13.2.1.4.6.18.2.6 Collisions (Offset = 3A048h)**_ 

## **Ethernet port N where N = 1 to 2** 

This statistic records the total number of times that the port experienced a collision. Collisions occur under two circumstances. 

1. When a transmit data or MAC control frame: 

   - Was destined for any unicast, broadcast or multicast address 

   - Was any size 

   - Had no carrier loss and no underrun 

   - Experienced a collision. A jam sequence is sent for every non-late collision, so this statistic will increment on each occasion if a frame experiences multiple collisions (and increments on late collisions) 

CRC errors have no effect upon this statistic. 

2. When the port is in half-duplex mode, flow control is active, and a frame reception begins. 

## _**13.2.1.4.6.18.2.7 Single Collision Tx Frames (Offset = 3A04Ch)**_ 

## **Ethernet port N where N = 1 to 2** 

The total number of frames transmitted on the port that experienced exactly one collision. Such a frame: 

- Was any data or MAC control frame destined for any unicast, broadcast or multicast address 

- Was any size 

- Had no carrier loss and no underrun 

- Experienced one collision before successful transmission. The collision was not late. 

CRC errors have no effect upon this statistic. 

## _**13.2.1.4.6.18.2.8 Multiple Collision Tx Frames (Offset = 3A050h)**_ 

## **Ethernet port N where N = 1 to 2** 

The total number of frames transmitted on the port that experienced multiple collisions. Such a frame: 

- Was any data or MAC control frame destined for any unicast, broadcast or multicast address 

- • Was any size 

- Had no carrier loss and no underrun 

- Experienced 2 to 15 collisions before being successfully transmitted. None of the collisions were late. 

CRC errors have no effect upon this statistic. 

## _**13.2.1.4.6.18.2.9 Excessive Collisions (Offset = 3A054h)**_ 

## **Ethernet port N where N = 1 to 2** 

The total number of frames for which transmission was abandoned due to excessive collisions. Such a frame: 

- Was any data or MAC control frame destined for any unicast, broadcast or multicast address 

- Was any size 

- Had no carrier loss and no underrun 

- Experienced 16 collisions before abandoning all attempts at transmitting the frame. None of the collisions were late. 

CRC errors have no effect upon this statistic. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1333 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.6.18.2.10 Late Collisions (Offset = 3A058h)**_ 

## **Ethernet port N where N = 1 to 2** 

The total number of frames on the port for which transmission was abandoned because they experienced a late collision. Such a frame: 

- Was any data or MAC control frame destined for any unicast, broadcast or multicast address 

- • Was any size 

- Experienced a collision later than 512 bit-times into the transmission. There may have been up to 15 previous (non-late) collisions which had previously required the transmission to be re-attempted. The _Late Collisions_ statistic dominates over the single-, multiple- , and excessive- collision statistics. If a late collision occurs, the frame will not be counted in any of these other three statistics. 

CRC errors, carrier loss, and underrun have no effect upon this statistic. 

## _**13.2.1.4.6.18.2.11 Carrier Sense Errors (Offset = 3A060h)**_ 

## **Ethernet port N where N = 1 to 2** 

The total number of frames on the port that experienced carrier loss. Such a frame: 

- Was any data or MAC control frame destined for any unicast, broadcast or multicast address 

- • Was any size 

- The carrier sense condition was lost or never asserted when transmitting the frame (the frame is not retransmitted). This is a transmit only statistic. Carrier Sense is a don’t care for received frames. Transmit frames with carrier sense errors are sent until completion and are not aborted. 

CRC errors and underrun have no effect upon this statistic. 

## _**13.2.1.4.6.18.2.12 Tx Octets (Offset = 3A064h)**_ 

## **All ports** 

The total number of bytes in all good frames transmitted on the port. A good frame is defined to be: 

- Any data or MAC control frame which was destined for any unicast, broadcast or multicast address 

- • Was any size 

- Had no late or excessive collisions, no carrier loss and no underrun. 

## _**13.2.1.4.6.18.2.13 Transmit Priority 0-7 (Offset = 3A180h to 3A1A8h)**_ 

The total number of frames transmitted on the port from transmit FIFO priority 0-7. Collision retries do not affect this statistic. Pause frames do not affect this statistic. 

- Any frame transmitted from priority 0-7, and 

- Was less than or equal to CPSW_TX_PRI0_MAXLEN_REG to CPSW_TX_PRI7_MAXLEN_REG 

- Collision retries are not counted in this statistic. 

- Pause frames are not counted in this statistic. 

- Carrier sense errors do not affect this statistic. 

Note: The Transmit Priority 0-7 Bytecount statistic is the number of bytes contained in the frames of the Transmit Priority 0-7 statistic. 

## _**13.2.1.4.6.18.2.14 Transmit Priority 0-7 Drop (Offset = 3A1C0h to 3A1E8)**_ 

The total number of transmit frames on the port that overran the transmit FIFO priority 0-7 and were dropped. This count includes frames dropped due to CPSW_TX_PRI0_MAXLEN_REG to CPSW_TX_PRI7_MAXLEN_REG. 

- Any frame destined to be transmitted from priority 0-7, and 

- Was any size, and 

- Was dropped due to priority 0-7 FIFO overrun (Start of packet overrun). 

- Was dropped due to frame size larger than CPSW_TX_PRI0_MAXLEN_REG to CPSW_TX_PRI7_MAXLEN_REG. 

1334 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

Note: The Transmit Priority 0-7 Drop Bytecount statistic is the number of bytes contained in the frames of the Transmit Priority 0-7 Drop statistic. 

## _**13.2.1.4.6.18.2.15 Tx Memory Protect Errors (Offset = 3A17Ch)**_ 

## **All ports** 

The total number of transmit frames on the port that had a memory protect CRC error on egress: 

- Any frame destined to be transmitted, 

- Was any size 

- Had a memory protect CRC error on egress. 

## **Note** 

1. Frames to the host with memory protect errors are indicated to be dropped with a set receive buffer descriptor **drop** bit. Ethernet frames will have at least one byte of the generated port type CRC inverted on egress. 

2. This statistic is 8-bits wide only and will not rollover but will limit at 0xFF. 

3. A non-zero value in this statistic will issue a STAT_PEND0 interrupt for the associated port. 

## _**13.2.1.4.6.18.2.16 Tx CRC Errors**_ 

The total number of frames transmitted on the port with a CRC error. Such a frame: 

- was any data frame destined for any unicast, broadcast or multicast address, and 

- was any size, and 

- was sent cut-thru by the receive port and was received with a CRC error, or 

- was a transmitted frame that also had a memory protect error (counted also in CPSW_STATN_TX_MEMORY_PROTECT_ERROR_k). 

## **Note** 

For port0 this statistics location (CPSW_STAT0_TXDROP) counts the number of drops to the host due to a memory protect error, or due to a cut-thru packet having an error on reception but was forwarded with the error. The Ethernet port receive error could be long, CRC, jabber, or code. For Ethernet ports, the receive error could be the same but the packet is transmitted with at least one byte of the actual outgoing packet CRC inverted to indicate the error. 

## **Note** 

A nonzero CPSW_STATN_TXDEFERREDFRAMES_k value should be subtracted from the CPSW_STATN_TXGOODFRAMES_k value to obtain the actual good frames value (the good frames statistic also increments on a transmitted CRC error). 

## _**13.2.1.4.6.18.3 Rx- and Tx (Shared) Statistics Descriptions**_ 

## _**13.2.1.4.6.18.3.1 Rx + Tx 64 Octet Frames (Offset = 3A068h)**_ 

## **All ports** 

The total number of 64-byte frames received and transmitted on the port. Such a frame is defined to be: 

- Any data or MAC control frame which was destined for any unicast, broadcast or multicast address 

- Did not experience late collisions, excessive collisions, or carrier sense error 

- Was exactly 64 bytes long. (If the frame was being transmitted and experienced carrier loss that resulted in a frame of this size being transmitted, then the frame will be recorded in this statistic). 

CRC errors, code/align errors and overruns do not affect the recording of frames in this statistic. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1335 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.6.18.3.2 Rx + Tx 65–127 Octet Frames (Offset = 3A06Ch)**_ 

## **All ports** 

The total number of frames of size 65 to 127 bytes received and transmitted on the port. Such a frame is defined to be: 

- Any data or MAC control frame which was destined for any unicast, broadcast or multicast address 

- Did not experience late collisions, excessive collisions, or carrier sense error 

- Was 65 to 127 bytes long 

CRC errors, code/align errors, underruns and overruns do not affect the recording of frames in this statistic. 

## _**13.2.1.4.6.18.3.3 Rx + Tx 128–255 Octet Frames (Offset = 3A070h)**_ 

## **All ports** 

The total number of frames of size 128 to 255 bytes received and transmitted on the port. Such a frame is defined to be: 

- Any data or MAC control frame which was destined for any unicast, broadcast or multicast address 

- Did not experience late collisions, excessive collisions, or carrier sense error 

- Was 128 to 255 bytes long 

CRC errors, code/align errors, underruns and overruns do not affect the recording of frames in this statistic. 

## _**13.2.1.4.6.18.3.4 Rx + Tx 256–511 Octet Frames (Offset = 3A074h)**_ 

## **All ports** 

The total number of frames of size 256 to 511 bytes received and transmitted on the port. Such a frame is defined to be: 

- Any data or MAC control frame which was destined for any unicast, broadcast or multicast address 

- Did not experience late collisions, excessive collisions, or carrier sense error 

- • Was 256 to 511 bytes long 

CRC errors, code/align errors, underruns and overruns do not affect the recording of frames in this statistic. 

## _**13.2.1.4.6.18.3.5 Rx + Tx 512–1023 Octet Frames (Offset = 3A078h)**_ 

## **All ports** 

The total number of frames of size 512 to 1023 bytes received and transmitted on the port. Such a frame is defined to be: 

- Any data or MAC control frame which was destined for any unicast, broadcast or multicast address 

- Did not experience late collisions, excessive collisions, or carrier sense error 

- • Was 512 to 1023 bytes long 

CRC errors, code/align errors, underruns and overruns do not affect the recording of frames in this statistic. 

## _**13.2.1.4.6.18.3.6 Rx + Tx 1024_Up Octet Frames (Offset = 3A07Ch)**_ 

## **All ports** 

The total number of frames of size 1024 to RX_MAXLEN bytes for receive or 1024 up for transmit on the port. Such a frame is defined to be: 

- Any data or MAC control frame which was destined for any unicast, broadcast or multicast address 

- Did not experience late collisions, excessive collisions, or carrier sense error 

- Was 1024 to RX_MAXLEN bytes long on receive, or any size on transmit 

CRC errors, code/align errors, underruns and overruns do not affect the recording of frames in this statistic. 

1336 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.2.1.4.6.18.3.7 Net Octets (Offset = 3A080h)**_ 

## **All ports** 

The total number of bytes of frame data received and transmitted on the port. Each frame counted: 

- was any data or MAC control frame destined for any unicast, broadcast or multicast address (address match does not matter) 

- Any length (including less than 64 bytes and greater than RX_MAXLEN bytes) 

Also counted in this statistic is: 

- Every byte transmitted before a carrier-loss was experienced 

- Every byte transmitted before each collision was experienced, (that is, multiple retries are counted each time) 

- • Every byte received if the port is in half-duplex mode until a jam sequence was transmitted to initiate flow control. (The jam sequence was not counted to prevent double-counting) 

Error conditions such as alignment errors, CRC errors, code errors, overruns and underruns do not affect the recording of bytes by this statistic. 

The objective of this statistic is to give a reasonable indication of Ethernet utilization. 

## _**13.2.1.4.6.18.4**_ 

**Table 13-150. Rx Statistics Summary** 

||**Frame Type**<br>**Frame Size (bytes)**<br>**Event**|**Frame Type**<br>**Frame Size (bytes)**<br>**Event**|**Frame Type**<br>**Frame Size (bytes)**<br>**Event**|
|---|---|---|---|
|**Rx Statistic**<br>**Fra**<br>**me/**<br>**Oct**<br>**Rx/**<br>**Rx+**<br>**Tx**|**MAC**<br>**control**<br>**Data**(5)<br>**<64**<br>**64**<br>**65-1**<br>**27**<br>**128-**<br>**255**<br>**256-**<br>**511**<br>**512-**<br>**1023**<br>**1024**<br>**-rx_**<br>**max**<br>**len**<br>**>rx_**<br>**max**<br>**len**<br>**Flo**<br>**w**<br>**Coll.**<br>(8)<br>**CRC**<br>**Erro**<br>**r**<br>**Alig**<br>**n/**<br>**Cod**<br>**e**<br>**Ove**<br>**rrun**<br>**Add**<br>**r.**<br>**Disc**<br>**.**<br>**Pau**<br>**se**<br>**fram**<br>**e**<br>**Non**<br>**-pau**<br>**se**(4)<br>**Mult**<br>**i**<br>**cast**<br>**Bro**<br>**ad**<br>**cast**<br>**Uni**<br>**cast**|||
|Good Rx<br>Frames<br>F<br>Rx|(y|(1)<br>y|<br>y|<br>y|<br>y)|n<br>(y|<br>y|<br>y|<br>y|<br>y|<br>y)<br>n|-(2)<br>n<br>n<br>-<br>n|
|Broadcast Rx<br>Frames<br>F<br>Rx|(%|<br>(6)<br>%|<br>n<br>y)<br>n|n<br>(y|<br>y|<br>y|<br>y|<br>y|<br>y)<br>n|-<br>n<br>n<br>-<br>n|
|Multicast Rx<br>Frames<br>F<br>Rx|(%|<br>%|<br>y)<br>n<br>n|n<br>(y|<br>y|<br>y|<br>y|<br>y|<br>y)<br>n|-<br>n<br>n<br>-<br>n|
|Pause Rx<br>Frames<br>F<br>Rx|y<br>n<br>n<br>n<br>n|n<br>(y|<br>y|<br>y|<br>y|<br>y|<br>y)<br>n|-<br>n<br>n<br>-<br>-|
|Rx CRC<br>Errors<br>F<br>Rx|(y|<br>y|<br>y|<br>y|<br>y)|n<br>(y|<br>y|<br>y|<br>y|<br>y|<br>y)<br>n|-<br>y<br>n<br>-<br>n|
|Rx Align/Code<br>Errors<br>F<br>Rx|(y|<br>y|<br>y|<br>y|<br>y)|n<br>(y|<br>y|<br>y|<br>y|<br>y|<br>y)<br>n|-<br>-<br>y<br>-<br>n|
|Oversized Rx<br>Frames<br>F<br>Rx|(y|<br>y|<br>y|<br>y|<br>y)|n<br>n<br>n<br>n<br>n<br>n<br>n<br>y|-<br>n<br>n<br>-<br>n|
|Rx Jabbers<br>F<br>Rx|(y|<br>y|<br>y|<br>y|<br>y)|n<br>n<br>n<br>n<br>n<br>n<br>n<br>y|-<br>(y|<br>y)<br>-<br>n|
|Undersized<br>Rx Frames<br>F<br>Rx|n<br>n<br>(y|<br>y|<br>y)|y<br>n<br>n<br>n<br>n<br>n<br>n<br>n|-<br>n<br>n<br>-<br>n|
|Rx Fragments<br>F<br>Rx|n<br>n<br>(y|<br>y|<br>y)|y^(7)<br>n<br>n<br>n<br>n<br>n<br>n<br>n|-<br>(y|<br>y)<br>-<br>-|
|Rx<br>Overruns(9)<br>F<br>Rx|(y|<br>y|<br>y|<br>y|<br>y)|(y|<br>y|<br>y|<br>y|<br>y|<br>y|<br>y|<br>y)|-<br>-<br>-<br>y<br>n|
|64octet<br>Frames<br>F<br>Rx+<br>Tx(3)|(y|<br>y|<br>y|<br>y|<br>y)|n<br>y<br>n<br>n<br>n<br>n<br>n<br>n|-<br>-<br>-<br>-<br>n|
|65-127octet<br>Frames<br>F<br>Rx+<br>Tx|(y|<br>y|<br>y|<br>y|<br>y)|n<br>n<br>y<br>n<br>n<br>n<br>n<br>n|-<br>-<br>-<br>-<br>n|
|128-255octet<br>Frames<br>F<br>Rx+<br>Tx|(y|<br>y|<br>y|<br>y|<br>y)|n<br>n<br>n<br>y<br>n<br>n<br>n<br>n|-<br>-<br>-<br>-<br>n|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1337 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-150. Rx Statistics Summary (continued)** 

||**Frame Type**<br>**Frame Size (bytes)**<br>**Event**|**Frame Type**<br>**Frame Size (bytes)**<br>**Event**|**Frame Type**<br>**Frame Size (bytes)**<br>**Event**|
|---|---|---|---|
|**Rx Statistic**<br>**Fra**<br>**me/**<br>**Oct**<br>**Rx/**<br>**Rx+**<br>**Tx**|**MAC**<br>**control**<br>**Data**(5)<br>**<64**<br>**64**<br>**65-1**<br>**27**<br>**128-**<br>**255**<br>**256-**<br>**511**<br>**512-**<br>**1023**<br>**1024**<br>**-rx_**<br>**max**<br>**len**<br>**>rx_**<br>**max**<br>**len**<br>**Flo**<br>**w**<br>**Coll.**<br>(8)<br>**CRC**<br>**Erro**<br>**r**<br>**Alig**<br>**n/**<br>**Cod**<br>**e**<br>**Ove**<br>**rrun**<br>**Add**<br>**r.**<br>**Disc**<br>**.**<br>**Pau**<br>**se**<br>**fram**<br>**e**<br>**Non**<br>**-pau**<br>**se**(4)<br>**Mult**<br>**i**<br>**cast**<br>**Bro**<br>**ad**<br>**cast**<br>**Uni**<br>**cast**|||
|256-511octet<br>Frames<br>F<br>Rx+<br>Tx|(y|<br>y|<br>y|<br>y|<br>y)|n<br>n<br>n<br>n<br>y<br>n<br>n<br>n|-<br>-<br>-<br>-<br>n|
|512-1023octet<br>Frames<br>F<br>Rx+<br>Tx|(y|<br>y|<br>y|<br>y|<br>y)|n<br>n<br>n<br>n<br>n<br>y<br>n<br>n|-<br>-<br>-<br>-<br>n|
|1024-UPoctet<br>Frames<br>F<br>Rx+<br>Tx|(y|<br>y|<br>y|<br>y|<br>y)|n<br>n<br>n<br>n<br>n<br>n<br>y<br>n|-<br>-<br>-<br>-<br>n|
|Rx Octets<br>O<br>Rx|(y|<br>y|<br>y|<br>y|<br>y)|n<br>(y|<br>y|<br>y|<br>y|<br>y|<br>y)<br>n|-<br>n<br>n<br>-<br>n|
|Net Octets<br>O<br>Rx+<br>Tx|(y|<br>y|<br>y|<br>y|<br>y)|(y|<br>y|<br>y|<br>y|<br>y|<br>y|<br>y|<br>y||y)<br>-<br>-<br>-<br>-|



(1) “AND” is assumed horizontally across the table between all conditions which form the statistic (marked y or n) except where (y|y), meaning “OR” is indicated. Parentheses are significant. 

- (2) “-“ indicates conditions which are ignored in the formations of the statistic. 

(3) Statistics marked “Rx+Tx” are formed by summing the Rx and Tx statistics, each of which is formed independently. 

(4) The non-pause column refers to all MAC control frames (for example, frames with length/type=88.08) with opcodes other than 0x0001. The pauseframe column refers to MAC frames with the opcode=0x0001. 

(5) The multicast, broadcast and unicast columns in the table refer to non-MAC Control/non-pause frames (i.e. data frames). 

(6) “%” If either a MAC control frame or pause frame has a multicast or broadcast destination address then the appropriate statistics will be updated. 

(7) “y^” Frame fragments are not counted if less than 8 bytes. 

(8) Flow coll. are half-duplex collisions forced by the MAC to achieve flow-control. A collision will be forced during the first 8 bytes so should not show in frame fragments. Some of the ‘-‘s in this column might in reality be ‘n’s. 

- (9) The rx_overruns stat is for RX_MOF_OVERRUNS and RX_SOF_OVERRUNS added together. 

**Table 13-151. Tx Statistics Summary** 

||**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Event**|**Event**|**Event**|**Event**|**Event**|**Event**|**Event**|**Event**|**Event**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Tx**<br>**Statistic**(9)<br>**Fra**<br>**me/**<br>**Oct**<br>**Tx/**<br>**Rx**<br>**+Tx**|**MAC**<br>**control**<br>(4)<br>**Data**<br>**64**<br>**65-**<br>**127**<br>**128**<br>**-25**<br>**5**<br>**256**<br>**-51**<br>**1**<br>**512**<br>**-10**<br>**23**<br>**102**<br>**4-1**<br>**535**<br>**>15**<br>**35**<br>**CR**<br>**C**<br>**Err**<br>**or**<br>**Pau**<br>**se-**<br>**MA**<br>**C**<br>**An**<br>**y-**<br>**CP**<br>**U**<br>**Mul**<br>**ti**<br>**cas**<br>**t**<br>**Bro**<br>**ad**<br>**cas**<br>**t**<br>**Uni**<br>**cas**<br>**t**|||||||||||||**Collision Type**<br>**No**<br>**Car**<br>**rier**<br>**Qu**<br>**eue**<br>**d**<br>**Def**<br>**err**<br>**ed**<br>**Un**<br>**der**<br>**run**<br>**Flo**<br>**w**(8)<br>**1**<br>**2-1**<br>**5**<br>**16**<br>**Lat**<br>**e**|||||||||
|Good Tx<br>Frames<br>F<br>Tx|(y|<br>(1)|y||y||y||y)|(y||y||y||y||y||y||y)|-(2)|-|-|-|n|n|n|-|-|n|
|Broadcast<br>Tx Frames<br>F<br>Tx|n|(%|<br>(5)|n|y)|n|(y||y||y||y||y||y||y)|-|-|-|-|n|n|n|-|-|n|
|Multicast Tx<br>Frames<br>F<br>Tx|(y||%||y)|n|n|(y||y||y||y||y||y||y)|-|-|-|-|n|n|n|-|-|n|
|Pause Tx<br>Frames<br>F<br>Tx|y|n|n|n|n|y|n|n|n|n|n|n|-|-|-|-|-|-|-|-|-|-|
|Collisions<br>F<br>Tx|n|(y||y||y||y)|(y||y||y||y||y||y||y)|-|(+<br>(6)|+|+|+|+)|n|-|-|-|
|Single<br>Collision Tx<br>Frames<br>F<br>Tx|n|(y||y||y||y)|(y||y||y||y||y||y||y)|-|-|y|n|n|n|n|-|-|-|
|Multiple<br>Collision Tx<br>Frames<br>F<br>Tx|n|(y||y||y||y)|(y||y||y||y||y||y||y)|-|-|n|y|n|n|n|-|-|-|
|Excessive<br>Collisions<br>F<br>Tx|n|(y||y||y||y)|(y||y||y||y||y||y||y)|-|-|n|n|y|n|n|-|-|-|



1338 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Table 13-151. Tx Statistics Summary (continued)** 

||**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Frame Type**<br>**Frame Size (bytes)**|**Event**|**Event**|**Event**|**Event**|**Event**|**Event**|**Event**|**Event**|**Event**|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|**Tx**<br>**Statistic**(9)<br>**Fra**<br>**me/**<br>**Oct**<br>**Tx/**<br>**Rx**<br>**+Tx**|**MAC**<br>**control**<br>(4)<br>**Data**<br>**64**<br>**65-**<br>**127**<br>**128**<br>**-25**<br>**5**<br>**256**<br>**-51**<br>**1**<br>**512**<br>**-10**<br>**23**<br>**102**<br>**4-1**<br>**535**<br>**>15**<br>**35**<br>**CR**<br>**C**<br>**Err**<br>**or**<br>**Pau**<br>**se-**<br>**MA**<br>**C**<br>**An**<br>**y-**<br>**CP**<br>**U**<br>**Mul**<br>**ti**<br>**cas**<br>**t**<br>**Bro**<br>**ad**<br>**cas**<br>**t**<br>**Uni**<br>**cas**<br>**t**|||||||||||||**Collision Type**<br>**No**<br>**Car**<br>**rier**<br>**Qu**<br>**eue**<br>**d**<br>**Def**<br>**err**<br>**ed**<br>**Un**<br>**der**<br>**run**<br>**Flo**<br>**w**(8)<br>**1**<br>**2-1**<br>**5**<br>**16**<br>**Lat**<br>**e**|||||||||
|Late<br>Collisions<br>F<br>Tx|n|(y||y||y||y)|n|(y||y||y||y||y||y)|-|-|-|-|-|y|-|-|-|-|
|Deferred Tx<br>Frames<br>F<br>Tx|n|(y||y||y||y)|(y||y||y||y||y||y||y)|-|-|n|n|n|n|n|-|y|n|
|Carrier<br>Sense<br>Errors<br>F<br>Tx|(y||y||y||y||y)|(y||y||y||y||y||y||y)|-|-|-|-|-|-|y|-|-|-|
|64octet<br>Frames<br>F<br>Rx+<br>Tx<br>(3)|(y||y||y||y||y)|y|n|n|n|n|n|n|-|-|-|-|n|n|n|-|-|-|
|65-127octet<br>Frames<br>F<br>Rx+<br>Tx|(y||y||y||y||y)|n|y|n|n|n|n|n|-|-|-|-|n|n|n|-|-|-|
|128-255octe<br>t Frames<br>F<br>Rx+<br>Tx|(y||y||y||y||y)|n|n|y|n|n|n|n|-|-|-|-|n|n|n|-|-|-|
|256-511octe<br>t Frames<br>F<br>Rx+<br>Tx|(y||y||y||y||y)|n|n|n|y|n|n|n|-|-|-|-|n|n|n|-|-|-|
|512-1023oct<br>et Frames<br>F<br>Rx+<br>Tx|(y||y||y||y||y)|n|n|n|n|y|n|n|-|-|-|-|n|n|n|-|-|-|
|1024-<br>UPoctet<br>Frames<br>F<br>Rx+<br>Tx|(y||y||y||y||y)|n|n|n|n|n|y|y|-|-|-|-|n|n|n|-|-|-|
|Tx Octets<br>O<br>Tx|(y||y||y||y||y)|(y||y||y||y||y||y||y)|-|-|-|-|n|n|n|-|-|n|
|Net Octets<br>O<br>Rx+<br>Tx|(y||y||y||y||y)|(y||y||y||y||y||y||y)|-|-|$(7)|$|$|$|$|-|-|-|



(1) "AND" is assumed horizontally across the table between all conditions which form the statistic (marked y or n) except where (y|y), meaning “OR” is indicated. Parentheses are significant. 

(2) “-“ indicates conditions which are ignored in the formations of the statistic. 

(3) Statistics marked “Rx+Tx” are formed by summing the Rx and Tx statistics, each of which is formed independently. 

(4) Pause (MAC) frames are issued in the MAC as perfect (no CRC error) 64 byte frames in full duplex only, so they cannot collide. 

(5) “%” If a CPU sourced MAC control frame has a multicast or broadcast destination address then the appropriate statistics will be updated. 

(6) “+” indicates collisions which are “summed” (i.e. every collision is counted in the Collisions statistic). Jam sequences used for halfduplex flow control are also counted. 

(7) “$” Every byte written on the wire during each retry attempt is also counted in addition to frames which experience no collisions or carrier loss. 

(8) The flow collision type is for half-duplex collisions forced by the MAC to achieve flow control. Some of the ‘-‘s in this column might in reality be ‘n’s. To prevent double-counting, Net Octets are unaffected by the jam sequence – the ‘received’ bytes, however, are counted. (See Table 13-150.) 

(9) When the transmit Tx FIFO is drained due to the MAC being disabled or link being lost, then the frames being purged will not appear in the Tx statistics. 

## _**13.2.1.4.7 Common Platform Time Sync (CPTS)**_ 

The Common Platform Time Sync (CPTS) module is used to facilitate host control of time sync operations. It enables compliance with the IEEE 1588-2008 standard for a precision clock synchronization protocol. 

Main features of CPTS module are: 

- Supports the selection of multiple external clock sources 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1339 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

- Software control of time sync events via interrupt or polling 

- Supports up to 8 hardware timestamp push inputs 

- Supports timestamp counter compare output (CPTS_COMP) 

- Supports timestamp counter bit output (CPTS_SYNC) 

- Supports a configurable number of timestamp Generator bit outputs (CPTS_GENFn). 

- Supports Ethernet Enhanced Scheduled Traffic Operations (CPTS_ESTFn). 

- 32-bit and 64-bit timestamp modes with PPM and nudge adjustment. 

## _**13.2.1.4.7.1 CPTS Architecture**_ 

Figure 13-97 shows the architecture of the CPTS module inside the CPSW Ethernet Subsystem. Time stamp values for every packet transmitted or received on external port of the CPSW are recorded. At the same time, each packet is decoded to determine if it is a valid time sync event. If so, an event is loaded into the Event FIFO for processing containing the recorded time stamp value when the packet was transmitted or received. 

In addition, both hardware (HWn_TS_PUSH) and software (TS_PUSH) can be used to read the current time stamp value though the Event FIFO. The reference clock used for the time stamp (CPTS_RFT_CLK) can be derived from several sources. 

**==> picture [364 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPTS_GENFm<br>TS_GENF<br>CPTS_ESTFm<br>TS_EST<br>Registers<br>CPTS_COMP<br>TS_COMP<br>TS_PUSH<br>CPTS_SYNC<br>TSPUSH<br>Event FIFO<br>EVENT_PEND<br>TSCNTROLL<br>CPTS_RFT_CLK<br>P1_TS_RX_DEC<br>CPTS_HW1_TS_PUSH HW1_TS_PUSH GMII_RX_0 P1_TS_RX_MII<br>P1_TS_TX_DEC<br>CPTS_HW2_TS_PUSH<br>HW2_TS_PUSH GMII_TX_0 P1_TS_TX_MII<br>SRC<br>P2_TS_RX_DEC<br>GMII_RX_1 P2_TS_RX_MII<br>P2_TS_TX_DEC<br>... GMII_TX_1 P2_TS_TX_MII<br>CPTS_HW8_TS_PUSH<br>HW8_TS_PUSH<br>...<br>m = 0 to 1 cpsw-013<br>**----- End of picture text -----**<br>


**Figure 13-97. CPTS Block Diagram** 

## **Note** 

See _CPSW0 CPTS Integration_ for CPTS integration in the device CPSW0 module. 

## _**13.2.1.4.7.2 CPTS Initialization**_ 

The CPTS module should be configured as follows: 

1. Reset the CPTS module. 

2. Write the CPTS_CLKSEL value in the CTRLMMR_CPTS_CLKSEL register with the desired reference clock selection. This value is allowed to be written only when the CPTS_EN bit in the CPSW_CPTS_CONTROL_REG register is cleared to zero. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1340 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

3. Set the CPTS_EN bit in the CPSW_CPTS_CONTROL_REG register. 

4. If using interrupts and not polling, enable the interrupt by setting the TS_PEND_EN bit in the CPSW_CPTS_INT_ENABLE_REG register. 

## _**13.2.1.4.7.3 32-bit Time Stamp Value**_ 

The time stamp value is a 32-bit value that increments on each CPTS_RFT_CLK rising edge when CPTS_EN bit is set to 1h. When CPTS_EN bit is cleared to 0h, the time stamp value is reset to 0h. 

If more than 32-bits of time stamp are required by the application, the host software must maintain the necessary number of upper bits. The upper time stamp value should be incremented by the host when the rollover event is detected. 

For test purposes, the time stamp can be written via the time stamp load function (CPSW_CPTS_TS_LOAD_VAL_REG / CPSW_CPTS_TS_LOAD_HIGH_VAL_REG and CPSW_CPTS_TS_LOAD_EN_REG registers). 

## _**13.2.1.4.7.4 64-bit Time Stamp Value**_ 

The time stamp value is a 64-bit value that increments on each CPTS_RFT_CLK rising edge when CPTS_EN bit is set to 1h. When CPTS_EN bit is cleared to 0h, the time stamp value is reset to 0h. 

64-bit mode is selected when CPSW_CPTS_CONTROL_REG[5] MODE bit set to 1h. 

For test purposes, the time stamp value can be written via the time stamp load function (CPSW_CPTS_TS_LOAD_EN_REG, CPSW_CPTS_TS_LOAD_VAL_REG, and CPSW_CPTS_TS_LOAD_HIGH_VAL_REG registers). The CPSW_CPTS_TS_ADD_VAL_REG feature is included to allow 1ns timestamp operations with an CPTS_RFT_CLK rate less than 1Ghz. Table 13-152 shows the CPTS_RFT_CLK and CPSW_CPTS_TS_ADD_VAL_REG values for 1ns operations. 

**Table 13-152. ADD_VAL feature** 

|**CPTS_RFT_CLK (MHz)**|**CPSW_CPTS_TS_ADD_VAL_R**|
|---|---|
||**EG[2-0] ADD_VAL**|
|1 GHz|0|
|500 MHz|1|
|333.33 MHz|2|
|250 MHz|3|
|200 MHz|4|
|166.66 MHz|5|
|142.85714 MHz|6|
|125 MHz|7|



## _**13.2.1.4.7.5 64-Bit Timestamp Nudge**_ 

The 64-bit TIME_STAMP value can be adjusted by writing the CPSW_CPTS_TS_NUDGE_VAL_REG[7-0] TS_NUDGE_VAL bit field value which is a two's complement value. A value of FFh will subtract 1 clock cycle from the next incremented 64-bit time stamp value (CPSW_CPTS_EVENT_0_REG[31-0] TIME_STAMP and CPSW_CPTS_EVENT_3_REG[31-0] TIME_STAMP value). A nudge value of 1h will add 1 clock cycle to the next incremented TIME_STAMP[63-0] value. For example, if the current TIME_STAMP value is F06h, and CPSW_CPTS_TS_ADD_VAL_REG[2-0] ADD_VAL = 3h, the next incremented timestamp value would be F0Ah without a nudge and F0Ah +/- [7-0] TS_NUDGE_VAL with a nudge. The [7-0] TS_NUDGE_VAL value is cleared to zero when the nudge has occurred. 

## _**13.2.1.4.7.6 64-bit Timestamp PPM**_ 

The 64-bit TIME_STAMP can be adjusted by parts per million or by parts per hour. Writing a non-zero value to the CPSW_CPTS_TS_PPM_LOW_VAL_REG[31-0] TS_PPM_LOW_VAL (Time stamp PPM Low value) and CPSW_CPTS_TS_PPM_HIGH_VAL_REG[9-0] TS_PPM_HIGH_VAL (Time stamp PPM High value) enables PPM operations. The adjustment is up or down depending on the [7] TS_PPM_DIR bit in the 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1341 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

CPSW_CPTS_CONTROL_REG register. The TIME_STAMP value is increased by the PPM value when [7] TS_PPM_DIR bit is cleared. The TIME_STAMP value is decreased by the PPM value when [7] TS_PPM_DIR bit is set. 

## **Parts Per Million example:** 

To adjust for 100 parts per million the configured value for TS_PPM[41-0] (through CPSW_CPTS_TS_PPM_LOW_VAL_REG[31-0] TS_PPM_LOW_VAL and CPSW_CPTS_TS_PPM_HIGH_VAL_REG[9-0] TS_PPM_HIGH_VAL) is: 1,000,000/100 = 10,000(decimal) 

## **Parts Per Hour example:** 

To adjust for 1 part per hour at 1 GHz CPTS_RFT_CLK the configured value for TS_PPM[41-0] (through CPSW_CPTS_TS_PPM_LOW_VAL_REG[31-0] TS_PPM_LOW_VAL and CPSW_CPTS_TS_PPM_HIGH_VAL_REG[9-0] TS_PPM_HIGH_VAL) is: (1,000,0000,000Hz/1pph) * (3600 seconds/hour) = 34630B8A000 (hex) 

## _**13.2.1.4.7.7 Event FIFO**_ 

All time sync events are pushed onto the Event FIFO. There are 32 locations in the event FIFO with no overrun indication supported. Software must service the event FIFO in a timely manner to prevent FIFO overrun. 

## _**13.2.1.4.7.8 Timestamp Compare Output**_ 

CPTS features one Time Stamp Compare (CPTS_COMP) output. The CPTS_COMP function is a software oriented feature that is intended to be replaced going forward by the hardware oriented GENF function. CPTS_COMP is not compatible with timestamp PPM or a non-zero CPSW_CPTS_TS_ADD_VAL_REG[2-0] ADD_VAL value. 

## _**13.2.1.4.7.8.1 Non-Toggle Mode: 32-bit**_ 

The CPTS_COMP output is asserted for CPSW_CPTS_TS_COMP_LEN_REG[31-0] TS_COMP_LENGTH periods when the CPSW_CPTS_EVENT_0_REG[31-0] TIME_STAMP value (lowe 32-bits) compares with the CPSW_CPTS_TS_COMP_VAL_REG[31-0] TS_COMP_VAL and the length value is non-zero. The CPTS_COMP rising edge occurs three CPTS_RFT_CLK clock periods after the values compare. A timestamp compare event is pushed into the event FIFO when CPTS_COMP is asserted. The polarity of the CPTS_COMP output is determined by the CPSW_CPTS_CONTROL_REG[2] TS_COMP_POLARITY bit. The output is asserted low when the polarity bit is 0h. 

## _**13.2.1.4.7.8.2 Non-Toggle Mode: 64-bit**_ 

64-bit mode operation is identical to 32-bit mode except that all 64-bits of the TIME_STAMP are used (CPSW_CPTS_EVENT_0_REG and CPSW_CPTS_EVENT_3_REG). In 32-bit mode only the lower 32-bits (CPSW_CPTS_EVENT_0_REG) are used. 

## _**13.2.1.4.7.8.3 Toggle Mode: 32-bit**_ 

The CPTS_COMP output is asserted (CPSW_CPTS_TS_COMP_LEN_REG[31-0] TS_COMP_LENGTH) for CPTS_RFT_CLK clock periods when the TIME_STAMP[31:0] value compares with the 

CPSW_CPTS_TS_COMP_VAL_REG and the length value is non-zero. The CPTS_COMP toggles thereafter on CPSW_CPTS_TS_COMP_VAL_REG[31-0] TS_COMP_LENGTH for CPTS_RFT_CLK periods. The length high or low can be adjusted by writing the CPSW_CPTS_TS_COMP_NUDGE_REG[7-0] NUDGE bit field value which is a two's complement value. A value of FFh will subtract one CPTS_RFT_CLK period from the CPSW_CPTS_TS_COMP_VAL_REG[31-0] TS_COMP_LENGTH value. A value of 0x01h will add one CPTS_RFT_CLK period to the CPSW_CPTS_TS_COMP_LEN_REG[31-0] TS_COMP_LENGTH value. Only a single high or low time is adjusted (nudged) and the CPSW_CPTS_TS_COMP_NUDGE_REG[7-0] NUDGE value is cleared to zero when the nudge has occurred. The CPTS_COMP output is asserted low when the CPSW_CPTS_CONTROL_REG[2] TS_COMP_POLARITY bit is 0h. No compare events and no CPTS_EVNT interrupts are generated in toggle mode. The CPSW_CPTS_CONTROL_REG[6] TS_COMP_TOG bit must be set for toggle mode (value 1h). Note this bit must be set before writing a non-zero value to CPSW_CPTS_TS_COMP_VAL_REG register. 

1342 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.2.1.4.7.8.4 Toggle Mode: 64-bit**_ 

64-bit mode operation is identical to 32-bit mode except that all 64-bits of the TIMESTAMP are used (CPSW_CPTS_EVENT_0_REG and CPSW_CPTS_EVENT_3_REG). In 32-bit mode only the lower 32-bits (CPSW_CPTS_EVENT_0_REG) are used. 

**==> picture [500 x 207] intentionally omitted <==**

**----- Start of picture text -----**<br>
RCLK<br>CPTS_COMP<br>Non-Toggle Mode<br>TS_COMP_LOW_VAL_REG[31:0]<br>Toggle Mode<br>TS_COMP_LOW_VAL_REG[31:0] TS_COMP_HIGH_VAL_REG[31:0]<br>cpsw-0013a<br>**----- End of picture text -----**<br>


**Figure 13-98. CPTS_COMP Output in Toggle and Non-Toggle Mode** 

## _**13.2.1.4.7.9 Timestamp Sync Output**_ 

The CPTS_SYNC output is a selected bit of the [31-0]TIME_STAMP counter value. One of bits 17-31 can be selected in CPSW_CPTS_CONTROL_REG[31-28] TS_SYNC_SEL. The CPTS_SYNC output is disabled when CPSW_CPTS_CONTROL_REG[31-28] TS_SYNC_SEL is zero. 

If the selected counter bit is 1 at the time when TS_SYNC_SEL value is written then a rising edge will not occur on the CPTS_SYNC output. A rising edge will occur on the CPTS_SYNC output upon the next transition to 1 of the selected counter bit. The TS_SYNC_SEL value must be written to zero before changing to a different non-zero value. No events are generated due to the CPTS_SYNC operation. The CPTS_SYNC output is two CPTS_RFT_CLK periods after the actual count value. 

## _**13.2.1.4.7.10 Timestamp GENFn Output**_ 

The CPTS_GENFn outputs have a programmable cycle (frequency) with a PPM feature and software nudge feature. The CPTS_GENFn output cycle is CPSW_GENF0_LENGTH_REG_L[31-0] CPTS_RFT_CLK periods (which is different than CPTS_COMP operation). Figure 13-99 represents the CPTS_GENFn output signal. 

The CPTS_GENFn output cycle is CPSW_GENF0_LENGTH_REG_L[31-0] CPTS_RFT_CLK periods beginning when the 64-bit TIME_STAMP value compares with the 64-bit GENFn_COMP value (CPSW_GENF0_COMP_LOW_REG_L and CPSW_GENF0_COMP_HIGH_REG_L registers) and the length value is non-zero. The CPTS_GENFn output cycle repeats thereafter every 

CPSW_GENF0_LENGTH_REG_L[31-0] CPTS_RFT_CLK periods. The upper 32-bit word should be written first for 64-bit values. The length should be zero while the comparison value and other configuration parameters are being configured. The length should be written non-zero to enable operations last. The first cycle after comparison is active high when the CPSW_CPTS_CONTROL_REG[2] TS_COMP_POLARITY bit is low. No compare events and no CPTS_EVNT interrupts are generated. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1343 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [500 x 192] intentionally omitted <==**

**----- Start of picture text -----**<br>
TIME_STAMP[63-0] = CPTS_GENFn_COMP[63-0]<br>RCLK<br>CPTS_GENFn<br>CPTS_GENFn_LENGTH[31-0]<br>cpsw-0013b<br>**----- End of picture text -----**<br>


**Figure 13-99. CPTS_GENFn Output Signal Diagram** 

## _**13.2.1.4.7.10.1 GENFn Nudge**_ 

The cycle length can be adjusted by writing the CPSW_CPTS_TS_COMP_NUDGE_REG[7-0] NUDGE register value which is a two's complement value. A value of FFh will subtract 1 CPTS_RFT_CLK from the CPSW_GENF0_LENGTH_REG_L[31-0] value. A value of 1h will add 1 CPTS_RFT_CLK to the CPSW_GENF0_LENGTH_REG_L[31-0] value. The CPSW_CPTS_TS_COMP_NUDGE_REG[7-0] NUDGE value is cleared to zero when the nudge has occurred. 

## _**13.2.1.4.7.10.2 GENFn PPM**_ 

The CPTS_GENFn output cycle can be adjusted by parts per million or by parts per hour. Writing a non-zero value to CPSW_GENF0_PPM_LOW_REG_L/ CPSW_GENF0_PPM_HIGH_REG_L enables PPM operations. The PPM counter continually loads and decrements to zero and then loads again. A single CPTS_RFT_CLK adjustment is made when the PPM counter decrements to zero. The adjustment is up or down depending on the CPSW_GENF0_TS_GENF_CONTROL_REG[0] PPM_DIR bit. When PPM_DIR bit is set a single CPTS_RFT_CLK time is subtracted from the generate function counter which has the effect of increasing the generate function frequency by the PPM amount. When PPM_DIR bit is cleared a single CPTS_RFT_CLK time is added to the generate function counter which has the effect of decreasing the generate function frequency by the PPM amount. 

## **Parts Per Million example:** 

To adjust for 100 parts per million the configured value for GENF_PPM[41-0] (through CPSW_GENF0_PPM_LOW_REG_L and CPSW_GENF0_PPM_HIGH_REG_L) is: 1,000,000/100 = 10,000(decimal) 

## **Parts Per Hour example:** 

To adjust for 1 part per hour at 1 GHz CPTS_RFT_CLK the configured value for GENF_PPM[41-0] (through CPSW_GENF0_PPM_LOW_REG_L and CPSW_GENF0_PPM_HIGH_REG_L) is: (1,000,0000,000Hz/1pph) * (3600 seconds/hour) = 34630B8A000 (hex) 

## _**13.2.1.4.7.11 Timestamp ESTFn**_ 

Each Ethernet port has a dedicated ESTFn generator which operates identically to the GENFn function. 

## _**13.2.1.4.7.12 Time Sync Events**_ 

Time Sync events are 96-bit values that are pushed onto the event FIFO and read by software in 32-bit reads. Four 32-bit registers, CPSW_CPTS_EVENT_0_REG through CPSW_CPTS_EVENT_3_REG hold the data of a time sync event. There are eight types of sync events: 

- Time Stamp Push Event 

1344 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

- Time Stamp Counter Rollover Event (32-bit mode only) 

- Time Stamp Counter Half-rollover Event (32-bit mode only) 

- Hardware Time Stamp Push Event 

- Ethernet Receive Event 

- Ethernet Transmit Event 

- Time Stamp Compare Event 

- Host Transmit Event 

## _**13.2.1.4.7.12.1 Time Stamp Push Event**_ 

Software can obtain the current time stamp value (at the time of the write) by initiating a time stamp push event. The push event is initiated by setting the [0]TS_PUSH bit of the CPSW_CPTS_TS_PUSH_REG register. The time stamp value is returned in the event, along with a time stamp push event code. The upper 32-bits (CPSW_CPTS_EVENT_3_REG register) of the timestamp are zero in 32-bit mode. 

## _**13.2.1.4.7.12.2 Time Stamp Counter Rollover Event (32-bit mode only)**_ 

The CPTS module contains a 32-bit time stamp value (CPSW_CPTS_EVENT_0_REG). The counter upper bits are maintained by host software. The rollover event indicates to software that the time stamp counter has rolled over from 0xFFFF FFFF to 0x0000 0000 and the software-maintained upper count value should be incremented. This event occurs only in 32-bit mode. 

## _**13.2.1.4.7.12.3 Time Stamp Counter Half-rollover Event (32-bit mode only)**_ 

The CPTS includes a time stamp counter half-rollover event. The half-rollover event indicates to software that the time stamp value (CPSW_CPTS_EVENT_0_REG[31-0] TIME_STAMP) has incremented from 0x7FFF FFFF to 0x8000 0000. The half-rollover event is included to enable software to correct a misaligned event condition. This event occurs only in 32-bit mode. 

The half-rollover event is included to enable software to determine the correct time for each event that contains a valid time stamp value, such as an Ethernet event. If an Ethernet event occurs around a counter rollover (full rollover), the rollover event could possibly be loaded into the event FIFO before the Ethernet event, even though the Ethernet event time was actually taken before the rollover. Figure 13-100 shows a misalignment condition. This misaligned event condition arises because an Ethernet event time stamp occurs at the beginning of a packet and time passes before the packet is determined to be a valid synchronization packet. The misaligned event condition occurs if the rollover occurs in the middle, after the packet time stamp has been taken, but before the packet has been determined to be a valid time sync packet. 

Host software must detect and correct for misaligned event conditions. For every event time stamp after a rollover and before a half-rollover, software must examine the time stamp most significant bit. If bit 31 of the time stamp value is low (0x0000 0000 through 0x7FFF FFFF), then the event time stamp was taken after the rollover and no correction is required. If the value is high (0x8000 0000 through 0xFFFF FFFF), the time stamp value was taken before the rollover and a misalignment is detected. The misaligned case indicates to software that it must subtract one from the upper count value stored in software to calculate the correct time for the misaligned event. The misaligned event occurs only on the rollover boundary and not on the half-rollover boundary. Software only needs to check for misalignment from a rollover event to a half-rollover event. 

When a rollover occurs, software increments the software time stamp upper value. The misaligned case indicates to software that the misaligned event time stamp has a valid upper value that is pre-increment, so one must be subtracted from the upper value to allow software to calculate the correct time for the misaligned event. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1345 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**==> picture [282 x 226] intentionally omitted <==**

**----- Start of picture text -----**<br>
Ethernet Event 1 EVENT FIFO<br>Time: 0xFFFF_FF00<br>Ethernet Event 1 Entry 1<br>Ethernet Event 2<br>Time: 0xFFFF_FFF0 Rollover Event Entry 2<br>Ethernet Event 2<br>Rollover Event (misaligned) Entry 3<br>Time: 0x0000_0000<br>Entry 4<br>Misalignment Condition<br>· Ethernet Event 2 happened …<br>before Rollover Event<br>· However, Ethernet Event 2 is Entry 15<br>loaded into the Event FIFO after<br>the Rollover Event<br>· Without software correction, Entry 16<br>Ethernet Event 2 will be<br>calculated with the wrong time.<br>cpsw-014<br>**----- End of picture text -----**<br>


## **Figure 13-100. Event FIFO Misalignment Condition** 

## _**13.2.1.4.7.12.4 Hardware Time Stamp Push Event**_ 

There are four hardware time stamp inputs ( CPTS_HW[1:4]_TS_PUSH events) that can cause hardware time stamp push events to be loaded into the Event FIFO. Each time stamp input is mapped in the device as shown in _CPSW0 CPTS Integration_ . The event is loaded into the event FIFO on the rising edge of the timer, and the PORT_NUMBER field in the CPSW_CPTS_EVENT_1_REG register indicates the hardware push input that caused the event (encoded). 

The hardware time stamp inputs are asynchronous and are low frequency signals. The CPTS logic synchronizes and performs a rising edge detect on the incoming asynchronous input. 

Each hardware time stamp input must be asserted for at least 10 periods of the selected CPTS_RFT_CLK clock. Each input can be enabled or disabled by setting the respective bits in the CPSW_CPTS_CONTROL_REG register. 

Hardware time stamps are intended to be an extremely low frequency signals, such that the event FIFO does not overrun. Software must keep up with the event FIFO and ensure that there is no overrun, or events will be lost. 

## _**13.2.1.4.7.12.5 Ethernet Port Events**_ 

Packets transmitted or received on each Ethernet port can generate Ethernet Transmit Events or Ethernet Receive Events, respectively. The CPTS hardware will decode each packet to determine if it is a valid CPTS time sync event. 

According to the IEEE 802.3 Ethernet standard, each Ethernet frame contains a 2-octet EtherType field to indicate which protocol is encapsulated in the PayLoad field, as shown in Figure 13-101. For standard time sync packets, this will contain the EtherType for the Precision Time Protocol (IEEE 1588), which is defined as 0x88F7. The CPTS hardware will compare this field to the TS_LTYPE1 field in the CPSW_PN_TS_SEQ_LTYPE_REG or the TS_LTYPE2 field in CPSW_PN_TS_CTL_LTYPE2_REG register (depending on which enable bit was set) , which should also be programmed to 88F7h. 

When a virtual LAN is used, an additional 4-octet 802.1Q tag is inserted in the Ethernet frame before the EtherType field, as shown in Figure 13-101. To indicate to the CPTS hardware that a virtual LAN is in use, the TS_TX_VLAN_LTYPE1_EN (or TS_TX_VLAN_LTYPE2_EN) enable bit must be set in the 

1346 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

CPSW_PN_TS_CTL_REG register. The EtherType for the 802.1Q tag is defined as 0x8100, and the CPTS hardware will compare this value to the TS_VLAN_LTYPE1 (or TS_VLAN_LTYPE2 depending on which enable bit was set) field in the CPSW_PN_TS_VLAN_LTYPE_REG register, which should also be programmed to 0x8100. 

When two stacked VLANs are used, two additional 4-octet 801.Q tags are inserted in the Ethernet frame before the EtherType field, as shown in Figure 13-101. In this case, both TS_VLAN_LTYPE1 and TS_VLAN_LTYPE2 must be enabled. The outer tag must match the value of the TS_VLAN_LTYPE1 field, and the inner tag must match the value of the TS_VLAN_LTYPE2 field. 

**==> picture [419 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
Source MAC EtherType/Size PayLoad<br>1 2 3 4 5 6 1 2 1 . . . n<br>ts_ltype<br>(1)<br>Source MAC 808.1Q Tag EtherType/Size PayLoad<br>1 2 3 4 5 6 1 2 3 4 1 2 1 . . . n<br>vlan_ltype1 ts_ltype1<br>or<br>vlan_ltype2<br>(2)<br>Source MAC MetroTag PE-VLAN808.1Q OuterTag 808.1Q Inner Tag EtherType/Size PayLoad<br>1 2 3 4 5 6 1 2 3 4 1 2 3 4 1 2 1 . . . n<br>vlan_ltype1 vlan_ltype2 ts_ltype<br>(3)<br>**----- End of picture text -----**<br>


cpsw-015 

## **Figure 13-101. Partial Ethernet-II Frames Showing Register Mapping of EtherTypes for a Simple Frame (1), a Single 1Q Tag Added (2), and Two 1Q Tags Added (3)** 

## _**13.2.1.4.7.12.5.1 Ethernet Port Receive Event**_ 

This section describes Ethernet port receive events. Ethernet port generates time synchronization events for valid received time sync packets. For every packet received on the Ethernet port, a timestamp will be captured by the receive module inside the CPTS for the corresponding port. The time stamp will be captured by the receive module regardless of whether or not the packet is a time synchronization packet to make sure that the time stamp is captured as soon as possible. The packet is sampled on both the rising and falling edges of the CPTS_RFT_CLK, and the time stamp will be captured once the start of frame delimiter for the receive packet is detected. 

After the time stamp has been captured, the receive interface will begin parsing the packet to determine if it is a valid Ethernet time synchronization packet. The CPSW decoder determines if the packet is a valid Ethernet receive time synchronization event. The receive interface for the port will use the following criteria to determine if the packet is a valid Annex D, Annex E, or Annex F time synchronization Ethernet receive event: 

## _**Annex D (IPv4)**_ 

1. Receive annex D time sync is enabled (TS_RX_ANNEX_D_EN is set in the CPSW_PN_TS_CTL_REG register). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1347 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

2. One of the sequences below is true. 

   - a. The first packet LTYPE matches 0x0800 

   - b. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches 0x0800 

   - c. The first packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches 0x0800 

   - d. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the third packet LTYPE matches 0x0800 

3. Byte 14 (the byte after the LTYPE) contains 0x45 (IPv4). 

## **Note** 

The byte numbering assumes that there are no VLANs. The byte number is intended to show the relative order of the bytes. 

4. Byte 20 contains 0bXXX00000 (5 lower bits zero) and Byte 21 contains 0x00 (fragment offset zero) 5. Byte 22 contains 0x01 (HOP Limit = 1) if the TS_TTL_NONZERO bit in the switch CPSW_PN_TS_CTL_LTYPE2_REG register is cleared to 0h, or byte 22 contains any value if CPSW_PN_TS_CTL_LTYPE2_REG is set to 1h. Byte 22 is the TTL/HOP field. 

6. Byte 23 contains 0x11 (Next Header UDP Fixed). 

7. The TS_UNI_EN bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is cleared to 0h and Bytes 30 through 33 contain: 

   - a. Decimal 224.0.1.129 and the TS_129 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - b. Decimal 224.0.1.130 and the TS_130 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - c. Decimal 224.0.1.131 and the TS_131 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - d. Decimal 224.0.1.132 and the TS_132 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - e. Decimal 224.0.0.107 and the TS_107 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set 

## -OR- 

The TS_UNI_EN bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set and Bytes 30 through 33 contain any values. 

8. Bytes 36 and 37 contain: 

   - a. Decimal 0x01 and 0x3F respectively and the TS_319 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set -OR- 

   - b. Decimal 0x01 and 0x40 respectively and the TS_320 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set. 

9. The PTP message begins in byte 42. 

10. The packet message type is enabled in the TS_MSG_TYPE_EN field in the CPSW_PN_TS_CTL_REG register. 

11. The packet was received without error (not long/short/mac_ctl/CRC/code/align). 

## _**Annex E (IPv6)**_ 

1. Receive annex E time sync is enabled (TS_RX_ANNEX_E_EN bit is set in the switch CPSW_PN_TS_CTL_REG register). 

2. One of the sequences below is true. 

   - a. The first packet LTYPE matches 0x86dd. 

1348 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

   - b. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches 0x86dd 

   - c. The first packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches 0x86dd 

   - d. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the third packet LTYPE matches 0x86dd 

3. Byte 14 (the byte after the LTYPE) contains 0x6X (IPv6). 

4. Byte 20 contains 0x11 (UDP Fixed Next Header). 

5. Byte 21 contains 0x01 (Hop Limit = 1) if the TS_TTL_NONZERO bit in the switch CPSW_PN_TS_CTL_LTYPE2_REG register is cleared to 0h, or byte 21 contains any value if TS_TTL_NONZERO is set to 1h. Byte 21 is the TTL/HOP field. 

6. The TS_UNI_EN bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is cleared to 0 and Bytes 38 through 53 contain: 

   - a. FF0M:0:0:0:0:0:0:0181 and the TS_129 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - b. FF0M:0:0:0:0:0:0:0182 and the TS_130 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - c. FF0M:0:0:0:0:0:0:0183 and the TS_131 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - d. FF0M:0:0:0:0:0:0:0184 and the TS_132 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - e. FF0M:0:0:0:0:0:0:006B and the TS_107 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set 

## **Note** 

All values above are 16-bit hex numbers where M is enabled in the TS_MCAST_TYPE_EN field in the CPSW_PN_TS_CTL2_REG register. 

-OR- 

The TS_UNI_EN bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set to 1h and Bytes 38 through 53 contain any value. 

7. Bytes 56 and 57 contain (UDP Header in bytes 54 through 61): 

   - a. Decimal 0x01 and 0x3F respectively and the TS_319 bit in the CPSW_PN_TS_CTL2_REG register is set, or 

   - b. Decimal 0x01 and 0x40 respectively and the TS_320 bit in the CPSW_PN_TS_CTL2_REG register is set. 

8. The PTP message begins in byte 62. 

9. The packet message type is enabled in the MSG_TYPE_EN field in the CPSW_PN_TS_CTL2_REG register. 

10. The packet was received without error (not long/short/mac_ctl/CRC/code/align). 

## _**Annex F (IEEE 802.3)**_ 

1. Receive Annex F time sync is enabled (TS_RX_ANNEX_F_EN is set in the switch CPSW_PN_TS_CTL_REG register). 

2. One of the sequences below is true: 

   - a. The first packet LTYPE matches TS_LTYPE1 in the CPSW_PN_TS_SEQ_LTYPE_REG/ CPSW_PN_TS_SEQ_LTYPE_REG register. LTYPE 1 should be used when only one time sync LTYPE is to be enabled. 

   - b. The first packet LTYPE matches TS_LTYPE2 in the CPSW_PN_TS_CTL_LTYPE2_REG register and LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1349 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

   - c. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_LTYPE1 in the CPSW_PN_TS_SEQ_LTYPE_REG register 

   - d. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_LTYPE2 in the CPSW_PN_TS_CTL_LTYPE2_REG register and TS_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register. 

   - e. The first packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_LTYPE1 in the CPSW_PN_TS_SEQ_LTYPE_REG register. 

   - f. The first packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_LTYPE2 in the CPSW_PN_TS_CTL_LTYPE2_REG register and TS_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register. 

   - g. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the third packet LTYPE matches TS_LTYPE1 in the CPSW_PN_TS_SEQ_LTYPE_REG register. 

   - h. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_RX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the third packet LTYPE matches TS_LTYPE2 in the CPSW_PN_TS_CTL_LTYPE2_REG register and TS_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register 

3. The PTP message begins in the byte after the LTYPE. 

4. The packet message type is enabled in the TS_MSG_TYPE_EN field in the CPSW_PN_TS_CTL_REG register. 

5. The packet was received without error (not long/short/mac_ctl/CRC/code/align). 

If all of the criteria described above are met for either Annex D, Annex E, or Annex F, and the packet is determined to be a valid time synchronization packet, then the RX interface will push an Ethernet receive event into the event FIFO. 

## _**13.2.1.4.7.12.5.2 Ethernet Port Transmit Event**_ 

This section describes Ethernet port transmit events. For every packet transmitted on the Ethernet ports, the port transmit interface will begin parsing the packet to determine if it is a valid Ethernet time synchronization packet. The CPTS transmit interface for the port will use to the following criteria to determine if the packet is a valid time synchronization Ethernet transmit event. The CPSW decoder determines if the packet is a valid ethernet receive time synchronization event. To be a valid Ethernet transmit time synchronization event, the conditions listed below must be true for either Annex D, Annex E, or Annex F: 

## _**Annex D (IPv4)**_ 

1. Transmit time sync is enabled (TS_TX_ANNEX_D_EN is set in the CPSW_PN_TS_CTL_REG register). 

2. One of the sequences below is true. 

   - a. The first packet LTYPE matches 0x0800 

   - b. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches 0x0800 

   - c. The first packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches 0x0800 

   - d. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second 

1350 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the third packet LTYPE matches 0x0800 

3. Byte 14 (the byte after the LTYPE) contains 0x45 (IPv4). 

## **Note** 

The byte numbering assumes that there are no VLANs. The byte number is intended to show the relative order of the bytes. 

4. Byte 20 contains 0bXXX00000 (5 lower bits zero) and Byte 21 contains 0x00 (fragment offset zero) 

5. Byte 22 contains 0x01 (HOP Limit = 1) if the TS_TTL_NONZERO bit in the switch CPSW_PN_TS_CTL_LTYPE2_REG register is cleared to 0h, or byte 22 contains any value if TS_TTL_NONZERO is set to 1h. Byte 22 is the TTL/HOP field. 

6. Byte 23 contains 0x11 (Next Header UDP Fixed). 

7. The TS_UNI_EN bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is cleared to 0h and Bytes 30 through 33 contain: 

   - a. Decimal 224.0.1.129 and the TS_129 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - b. Decimal 224.0.1.130 and the TS_130 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - c. Decimal 224.0.1.131 and the TS_131 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - d. Decimal 224.0.1.132 and the TS_132 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - e. Decimal 224.0.0.107 and the TS_107 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - f. The TS_UNI_EN bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set and Bytes 30 through 33 contain any values. 

8. Bytes 36 and 37 contain: 

   - a. Decimal 0x01 and 0x3F respectively and the TS_319 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - b. Decimal 0x01 and 0x40 respectively and the TS_320 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set. 

9. The PTP message begins in byte 42. 

10. The packet message type is enabled in the TS_MSG_TYPE_EN field in the CPSW_PN_TS_CTL_REG register. 

11. The packet was sent by host port 0. 

## _**Annex E (IPv6)**_ 

1. Transmit annex E time sync is enabled (TS_TX_ANNEX_E_EN bit is set in the switch CPSW_PN_TS_CTL_REG register). 

2. One of the sequences below is true. 

   - a. The first packet LTYPE matches 0x86dd. 

   - b. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches 0x86dd 

   - c. The first packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches 0x86dd 

   - d. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the third packet LTYPE matches 0x86dd 

3. Byte 14 (the byte after the LTYPE) contains 0x6X (IPv6). 

4. Byte 20 contains 0x11 (UDP Fixed Next Header). 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1351 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

5. Byte 21 contains 0x01 (Hop Limit = 1) if the TS_TTL_NONZERO bit in the switch CPSW_PN_TS_CTL_LTYPE2_REG register is cleared to 0h, or byte 21 contains any value if TS_TTL_NONZERO is set to 1h. Byte 21 is the TTL/HOP field.. 

6. The TS_UNI_EN bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is cleared to 0 and Bytes 38 through 53 contain: 

   - a. FF0M:0:0:0:0:0:0:0181 and the TS_129 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - b. FF0M:0:0:0:0:0:0:0182 and the TS_130 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - c. FF0M:0:0:0:0:0:0:0183 and the TS_131 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - d. FF0M:0:0:0:0:0:0:0184 and the TS_132 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - e. FF0M:0:0:0:0:0:0:006B and the TS_107 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set 

## **Note** 

All values above are 16-bit hex numbers where M is enabled in the TS_MCAST_TYPE_EN field in the CPSW_PN_TS_CTL2_REG register. 

## -OR- 

The TS_UNI_EN bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set to 1h and Bytes 38 through 53 contain any value. 

7. Bytes 56 and 57 contain (UDP Header in bytes 54 through 61): 

   - a. Decimal 0x01 and 0x3F respectively and the TS_319 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set, or 

   - b. Decimal 0x01 and 0x40 respectively and the TS_320 bit in the CPSW_PN_TS_CTL_LTYPE2_REG register is set. 

8. The PTP message begins in byte 62. 

9. The packet message type is enabled in the TS_MSG_TYPE_EN field in the CPSW_PN_TS_CTL_REG register. 

10. The packet was sent by host port 0. 

## _**Annex F (IEEE 802.3)**_ 

1. Transmit time sync is enabled (TS_TX_ANNEX_F_EN is set in the switch CPSW_PN_TS_CTL_REG register). 

2. One of the sequences below is true: 

   - a. The first packet LTYPE matches TS_LTYPE1 in the CPSW_PN_TS_SEQ_LTYPE_REG register. LTYPE 1 should be used when only one time sync LTYPE is to be enabled. 

   - b. The first packet LTYPE matches TS_LTYPE2 in the CPSW_PN_TS_CTL_LTYPE2_REG register and TS_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register. 

   - c. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_LTYPE2 in the CPSW_PN_TS_CTL_LTYPE2_REG register. 

   - d. The first packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_LTYPE1 in the CPSW_PN_TS_SEQ_LTYPE_REG register. 

   - e. The first packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_LTYPE2 in the CPSW_PN_TS_CTL_LTYPE2_REG register. 

   - f. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_LTYPE2 in the CPSW_PN_TS_CTL_LTYPE2_REG register and TS_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register. 

   - g. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and 

1352 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

TS_TX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the third packet LTYPE matches TS_LTYPE2 in the CPSW_PN_TS_CTL_LTYPE2_REG register. 

   - h. The first packet LTYPE matches TS_VLAN_LTYPE1 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE1_EN is set in the CPSW_PN_TS_CTL_REG register and the second packet LTYPE matches TS_VLAN_LTYPE2 in the CPSW_PN_TS_VLAN_LTYPE_REG register and TS_TX_VLAN_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register and the third packet LTYPE matches TS_LTYPE2 in the CPSW_PN_TS_CTL_LTYPE2_REG register and TS_LTYPE2_EN is set in the CPSW_PN_TS_CTL_REG register 

3. The packet message type is enabled in the TS_MSG_TYPE_EN field in the CPSW_PN_TS_CTL_REG register. 

4. The packet was sent by host port 0. 

If all of the criteria described above are met, and the packet is determined to be a valid time synchronization packet, then the time stamp for the transmit event will not be generated until the start of frame delimiter of the packet is actually transmitted. The start of frame delimiter will be sampled on every rising and falling edge of the CPTS_RFT_CLK. Once the packet is transmitted, then the TX interface will push an Ethernet transmit event into the event FIFO. 

**Table 13-153. Values of Message Type Field** 

|**Message Type**|**Value (hex)**||
|---|---|---|
|Sync||0|
|Delay_Req||1|
|Pdelay_Req||2|
|Pdelay_Resp||3|
|Reserved||4:7|
|Follow_Up||8|
|Delay_Resp||9|
|Pdelay_Resp_Follow_Up||A|
|Announce||B|
|Signaling||C|
|Management||D|
|Reserved||E:F|



Once a transmitted or received packet is determined to be a valid time sync packet, the Ethernet Transmit Event or Ethernet Receive Event is loaded onto the Event FIFO. 

The CPSW_CPTS_EVENT_1_REG register contains the Message Type and Sequence ID values from the original time sync packet. The CPSW_CPTS_EVENT_0_REG (and CPSW_CPTS_EVENT_3_REG) register contains the time stamp value when the packet arrived at the corresponding port. 

**Table 13-154. Values of Message Type Field** 

|**Message Type**|**Value (hex)**||
|---|---|---|
|Sync||0|
|Delay_Req||1|
|Pdelay_Req||2|
|Pdelay_Resp||3|
|Reserved||4:7|
|Follow_Up||8|
|Delay_Resp||9|
|Pdelay_Resp_Follow_Up||A|
|Announce||B|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1353 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

**Table 13-154. Values of Message Type Field** 

**(continued)** 

|**Message Type**|**Value (hex)**||
|---|---|---|
|Signaling||C|
|Management||D|
|Reserved||E:F|



Once a transmitted or received packet is determined to be a valid time sync packet, the Ethernet Transmit Event or Ethernet Receive Event is loaded onto the Event FIFO. 

The CPSW_CPTS_EVENT_1_REG register contains the Message Type and Sequence ID values from the original time sync packet. The CPSW_CPTS_EVENT_0_REG (and CPSW_CPTS_EVENT_3_REG) register contains the time stamp value when the packet arrived at the corresponding port. 

## _**13.2.1.4.7.12.5.3**_ 

**Table 13-155. Values of Message Type Field** 

|**Message Type**|**Value (hex)**||
|---|---|---|
|Sync||0|
|Delay_Req||1|
|Pdelay_Req||2|
|Pdelay_Resp||3|
|Reserved||4:7|
|Follow_Up||8|
|Delay_Resp||9|
|Pdelay_Resp_Follow_Up||A|
|Announce||B|
|Signaling||C|
|Management||D|
|Reserved||E:F|



Once a transmitted or received packet is determined to be a valid time sync packet, the Ethernet Transmit Event or Ethernet Receive Event is loaded onto the Event FIFO. 

The CPSW_CPTS_EVENT_1_REG register contains the Message Type and Sequence ID values from the original time sync packet. The CPSW_CPTS_EVENT_0_REG (and CPSW_CPTS_EVENT_3_REG) register contains the time stamp value when the packet arrived at the corresponding port. 

## _**13.2.1.4.7.13 Timestamp Compare Event**_ 

**Note** 

Timestamp compare events are generated for non-toggle mode only. 

The CPTS can generate an event for a time stamp comparison in 32-bit or 64-bit mode. 

## _**13.2.1.4.7.13.1 32-Bit Mode**_ 

The CPTS_COMP output is also asserted when the event is generated. The event is generated when the 32-bit time stamp value (CPSW_CPTS_EVENT_0_REG) compares with the CPSW_CPTS_TS_COMP_VAL_REG register and the CPSW_CPTS_TS_COMP_LEN_REG value is non-zero. The CPSW_CPTS_TS_COMP_LEN_REG value should be written by software after the CPSW_CPTS_TS_COMP_VAL_REG register is written and should be zero when the comparison value is written. 

1354 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## _**13.2.1.4.7.13.2 64-Bit Mode**_ 

The CPTS_COMP output is also asserted when the event is generated. The event is generated when the 64-bit time stamp value (CPSW_CPTS_EVENT_0_REG and CPSW_CPTS_EVENT_3_REG) compares with the CPSW_CPTS_TS_COMP_VAL_REG and CPSW_CPTS_TS_COMP_HIGH_VAL_REG registers and the CPSW_CPTS_TS_COMP_LEN_REG value is non-zero. The CPSW_CPTS_TS_COMP_LEN_REG value should be written by software after the CPSW_CPTS_TS_COMP_VAL_REG register is written and should be zero when the comparison value is written. 

## _**13.2.1.4.7.14 Host Transmit Event**_ 

The host can send a packet to be transmitted on an Ethernet port that will generate a time synchronization event. The host sets the TSTAMP_EN bit and sends the DOMAIN, MESSAGE_TYPE, and SEQUENCE_ID in the additional control information that resides in the protocol specific section of the descriptor that is transmitted to the CPSW. An event is then generated and placed on the event FIFO once the packet is transmitted. Host events allow the user to timestamp exactly when a software generated packet exits the device. 

## _**13.2.1.4.7.15 CPTS Interrupt Handling**_ 

When an event is push onto the Event FIFO, an interrupt can be generated to indicate to software that a time sync event occurred. The following steps should be taken to process time sync events using interrupts: 

1. Enable the TS_PEND interrupt by setting the TS_PEND_EN bit of the CPSW_CPTS_INT_ENABLE_REG register. 

2. Upon interrupt, read the CPSW_CPTS_EVENT_0_REG through CPSW_CPTS_EVENT_3_REG registers values. 

3. Set the CPSW_CPTS_EVENT_POP_REG[0] EVENT_POP bit to 1h to pop the previously read value off of the event FIFO. 

4. Process the interrupt as required by the application software. 

Software has the option of processing more than a single event from the event FIFO in the interrupt service routine in the following way: 

1. Enable the TS_PEND interrupt by setting the TS_PEND_EN bit of the CPSW_CPTS_INT_ENABLE_REG 2. Upon interrupt, enter the CPTS service routine. 

3. Read the CPSW_CPTS_EVENT_0_REG through CPSW_CPTS_EVENT_3_REG registers values. 

4. Set the CPSW_CPTS_EVENT_POP_REG[0] EVENT_POP bit to 1h to pop the previously read value off of the event FIFO. 

5. Wait for an amount of time greater than four CPTS_RFT_CLK periods plus four CPPI_ICLK periods. 6. Read the TS_PEND_RAW bit in the CPSW_CPTS_INTSTAT_RAW_REG register to determine if another valid event is in the event FIFO. If bit TS_PEND_RAW is asserted, go to step 3. If bit TS_PEND_RAW is not asserted proceed with step 7. 

7. Process the interrupt(s) as required by the application software. 

Software also has the option of disabling the interrupt and polling the TS_PEND_RAW bit of the CPSW_CPTS_INTSTAT_RAW_REG register to determine if a valid event is on the event FIFO. 

## _**13.2.1.4.8 CPDMA Host Interface**_ 

The CPDMA submodule is a CPPI 3.0 and CBA 3.1 compliant packet DMA transfer controller. The CPPI interface is port 0. 

## _**13.2.1.4.8.1 Functional Operation**_ 

Host software sends and receives network frames via the CPDMA CPPI 3.0 compliant host interface. The host interface includes module registers and host memory data structures. The host memory data structures are buffer descriptors and data buffers. Buffer descriptors are data structures that contain information about a single data buffer. Buffer descriptors may be linked together to describe frames of queues of frames for transmission of data from the host to Ethernet and free buffer queues available for packet data from Ethernet to the host. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1355 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

After reset, initialization, and configuration the host may initiate CPDMA host interface operations. Receive DMA operations are initiated by host writes to the appropriate receive channel head descriptor pointer. The receive DMA controller then fetches the first packet in the packet chain from memory in accordance with CPPI 3.0 protocol and proceeds with packet operations. The DMA controller fetches the packet data in 64-byte (maximum) bursts. 

Host CPDMA transmit operation are initiated by host writes to the appropriate transmit channel head descriptor pointer after host initialization and configuration. The transmit DMA controller writes Ethernet received packet data to external host memory in accordance with CPPI 3.0 protocol. 

## _**13.2.1.4.8.2 Transmit CPDMA Interface**_ 

The transmit CPDMA (Ethernet to host) is an eight channel CPPI 3.0 compliant interface. Each priority/channel has a single queue for frame reception. 

## _**13.2.1.4.8.2.1 Transmit CPDMA Host Configuration**_ 

To configure the CPDMA for transmit operations the host must do the following: 

1. Initialize the TX_HDP registers to 0. 

2. Enable the desired transmit interrupts in the CPDMA_TX_INTMASK_SET register. 

3. Write the thost_buffer_offset register value. 

4. Setup the transmit channel(s) buffer descriptors in host memory as defined in CPPI 3.0. 

5. Enable the CPDMA controller by setting the thost_en bit in the CPDMA_TX_CONTROL register. 

## _**13.2.1.4.8.2.2 Transmit CPDMA Buffer Descriptors**_ 

A transmit buffer descriptor is a contiguous block of four 32-bit data words aligned on a 32-bit word boundary. 

## **Figure 13-102. TX Buffer Descriptor Format (Word 1)** 

|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|
|---|---|---|
|NEXT_DESCRIPTOR_POINTER|||
||||
|15<br>14<br>13<br>12<br>11<br>10<br>9<br>8<br>7<br>6<br>5<br>4<br>3<br>2<br>1<br>0|||
|NEXT_DESCRIPTOR_POINTER|||
||||
|**Bit**|**Field**|**Description**|
|31-0|NEXT_DESCRIPTOR_POINTER|The 32-bit word aligned memory address of the next buffer descriptor in the RX queue.<br>This is the mechanism used to reference the next buffer descriptor from the current<br>buffer descriptor. If the value of this pointer is zero, then the current buffer is the last<br>buffer in the queue. Set by the host.|
|**Figure 13-103. TX Buffer Descriptor Format(Word 2)**|||
|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|||
|BUFFER_POINTER|||
||||
|15<br>14<br>13<br>12<br>11<br>10<br>9<br>8<br>7<br>6<br>5<br>4<br>3<br>2<br>1<br>0|||
|BUFFER_POINTER|||
||||
|**Bit**|**Field**|**Description**|
|31-0|BUFFER_POINTER|The byte aligned memory address of the buffer associated with the buffer descriptor.<br>Set by the host.|
|**Figure 13-104. TX Buffer Descriptor Format(Word 3)**|||
|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|||



1356 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**Figure 13-104. TX Buffer Descriptor Format (Word 3) (continued)** 

|RESERVED|RESERVED|BUFFER_OFFSET|BUFFER_OFFSET|
|---|---|---|---|
|||||
|15<br>14<br>13<br>12<br>11<br>10<br>9<br>8<br>7<br>6<br>5<br>4<br>3<br>2<br>1<br>0||||
|RESERVED||BUFFER_LENGTH||
|||||
|**Bit**|**Field**||**Description**|
|31-28|RESERVED||Reserved|
|27-16|BUFFER_OFFSET||Indicates how many unused bytes are at the start of the buffer. The buffer offset is<br>reduced to 12-bits. A value of 0x0000 indicates that there are no unused bytes at the<br>start of the buffer and that valid data begins on the first byte of the buffer. A value of<br>0x000F indicates that the first 15 bytes of the buffer are to be ignored by the port and<br>that valid buffer data starts on byte 16 of the buffer. The port writes BUFFER_OFFSET<br>with the value from the CPDMA_TH_BUFFER_OFFSET_REG register value. The host<br>initializes the BUFFER_OFFSET to zero for free buffers. The BUFFER_LENGTH must<br>be greater that the CPDMA_TH_BUFFER_OFFSET_REG register value. The buffer<br>offset is valid only on SOP.|
|15-12|RESERVED||Reserved|
|11-0|BUFFER_LENGTH||Indicates how many valid data bytes are in the buffer. The buffer length is reduced<br>to 12-bits. Unused or protocol specific bytes at the beginning of the buffer are not<br>counted in the Buffer Length field. The host initializes the BUFFER_LENGTH, but<br>the port may overwrite the host initiated value with the actual buffer length value on<br>SOP and/or EOP buffer descriptors. SOP buffer length values will overwritten if the<br>packet size is less than the size of the buffer or if the offset is nonzero. EOP buffer<br>length values will be overwritten if the entire buffer is not filled up with data. The<br>BUFFER_LENGTH must be greater than zero.|



## **Figure 13-105. TX Buffer Descriptor Format (Word 4)** 

|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|
|---|---|---|---|---|---|---|---|---|---|---|---|---|
|SOP|EOP|OWNE<br>RSHIP|EOQ|TEAR<br>DOWN<br>_COM<br>PLETE|PASSE<br>D_CR<br>C|LONG|SHOR<br>T|MAC_<br>CTL|OVER<br>RUN|PKT_ERR|VLAN_<br>ENCA<br>P|FROM_PORT|
||||||||||||||
|15<br>14<br>13<br>12<br>11<br>10<br>9<br>8<br>7<br>6<br>5<br>4<br>3<br>2<br>1<br>0|||||||||||||
|TS_EN<br>CAP|MEMO<br>RY_PR<br>OTEC<br>T_ERR<br>OR|CRC_T<br>YPE|CHKS<br>UM_E<br>NCAP|PACKET_LENGTH|||||||||



|**Bit**|**Field**|**Description**|
|---|---|---|
|31|SOP|Start of Packet- Indicates that the descriptor buffer is the first buffer in the packet. The<br>port sets the SOP bit.<br>0h - Not start of packet buffer<br>1h - Start of packet buffer|
|30|EOP|End of Packet- Indicates that the descriptor buffer is the last buffer in the packet. The<br>port sets the EOP bit.<br>0h - Not end of packet buffer<br>1h - End of packet buffer|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1357 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

|**Bit**|**Field**|**Description**|
|---|---|---|
|29|OWNERSHIP|Ownership- Indicates ownership of the packet and is valid only on SOP. This bit must<br>be set by the host and is cleared by the port when the packet has been transferred<br>(and the TH_OWNERSHIP bit is clear). The host uses this bit to reclaim buffers. If the<br>TH_OWNERSHIP bit is set then the port does not clear this bit which can reduce the<br>host workload in some applications.<br>0h - The packet is owned by the host<br>1h - The packet is owned by the port|
|28|EOQ|End of Queue- Set by the port to indicated that the RX queue empty condition exists.<br>This bit is valid only on EOP. The port determines the end of queue condition by a zero<br>NEXT_DESCRIPTOR_POINTER.<br>0h - The RX queue has more buffers available for reception.<br>1h - The Descriptor buffer is the last buffer in the last packet in the queue.|
|27|TEARDOWN_COMPLETE|Teardown Complete- Set by the port to indicate that the host commanded teardown<br>process is complete, and the channel buffers may be reclaimed by the host. The bit is<br>valid only on SOP.<br>0h - The port has not completed the teardown process<br>1h - The port has completed the commanded teardown process.|
|26|PASSED_CRC|Set by the port to indicate that the CRC was passed with the data. The<br>PACKET_LENGTH includes the CRC bytes. The PASSED_CRC bit is valid only on<br>SOP. The P0_TX_CRC_REMOVE bit in the CPDMA_CONTROL register determines<br>if CPPI 3.0 transmit packets have a CRC included or not. The CRC type if present is<br>determined by the P0_TX_CRC_TYPE bit in the CPDMA_Control register.|
|25|LONG|Jabber Frame - Indicates that the frame is a jabber frame and<br>was not discarded because RX_CEF_EN was set in the ingress port<br>ETH_MAC_0_PN_MAC_CONTROL_REG register. Valid only on SOP.|
|24|SHORT|Fragment Frame - Indicates that the frame is a fragment and was<br>not discarded because RX_CEF_EN was set in the ingress port<br>ETH_MAC_0_PN_MAC_CONTROL_REGregister. Valid only on SOP.|
|23|MAC_CTL|Control Frame - Indicates that the frame is a MAC control frame and<br>was not discarded because the RX_CMF_EN was set in the ingress port<br>ETH_MAC_0_PN_MAC_CONTROL_REG register. Valid only on SOP.|
|22|OVERRUN|Overrun - Set by the port to indicate that the frame reception was aborted due to<br>transmit buffer overrun. This bit is valid only on SOP.<br>0h - no overrun occurred on the packet<br>1h - The packet was aborted due to overrun|
|21-20|PKT_ERROR|Packet Contained Error on Ethernet Ingress. This field is valid on SOP.<br>00h - no error<br>01h - CRC error on ingress<br>10h - Code error on ingress<br>11h - align error on ingress|
|19|VLAN_ECAP|VLAN Encapsulated Packet- Indicates when set that the packet data contains a 32-bit<br>VLAN header word that is included in the packet byte count. This field is set by the<br>port to be the value of the CPDMA_CONTROL_REG register TH_VLAN_ENCAP bit. If<br>both VLAN_ENCAP and TS_ENCAP are set then the VLAN is first. This encapsulated<br>word also contains the ALE classification FLOW (threadval). This bit is valid on SOP.|
|18-16|FROM_PORT|Indicates the Ethernet ingress port number. This field is valid only on SOP.|



1358 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

|**Bit**|**Field**|**Description**|
|---|---|---|
|15|TS_ENCAP|Timestamp Encapsulated Packer - Indicates when set that the packet data contains a<br>64-bit timestamp (two 32-bit words with the lower 32-bit word first) that is included<br>in the packet byte count. This field is set by the port to be the value of the<br>CPDMA_CONTROL_REG register TH_TS_ENCAP bit. If both VLAN_ENCAP and<br>TS_ENCAP are set then the VLAN is first. This bit is valid on SOP.|
|14|MEMORY_PROTECT_ERROR|An error was detected in the packet Castignoli protect CRC. The packet should be<br>dropped by the host.|
|13|CRC_TYPE|The packet CRC type.<br>0h: Ethernet CRC<br>1h: Castagnoli CRC|
|12|CHKSUM_ENCAP|Checksum Encapsulated Packet - Indicates when set that the packet data contains<br>4-bytes of transmit checksum information at the end of the packet (last 4 bytes). The<br>packet length includes the checksum bytes. This bit will be set for every packet to the<br>Host when P0_TX_CHKSUM_EN is set. This bit is valid on SOP|
|11-0|PACKET_LENGTH|Specifies the number of bytes in the entire packet. Offset bytes are not included. The<br>sum of the BUFFER_LENGTH fields should equal the PACKET_LENGTH. Valid only<br>on SOP.|



## _**13.2.1.4.8.2.3 Transmit Channel Teardown**_ 

The host commands a transmit channel teardown by writing the channel number to the CPDMA_TX_TEARDOWN register. When a teardown command is issued to an enabled transmit channel the following will occur: 

- Any frame currently in transmission will complete normally 

- The TEARDOWN_COMPLETE bit will be set in the next transmit buffer descriptor (if there is one). 

- The channel head descriptor pointer will be cleared to 0. 

- An interrupt will be issued to inform the host of the channel teardown. 

- The software should acknowledge a teardown interrupt with a FFFF FFFCh acknowledge value 

Channel teardown may be commanded on any channel at any time. The host is informed of the teardown completion by the set TEARDOWN_COMPLETE buffer descriptor bit. The port does not clear any channel enables due to a teardown command. A teardown command to an inactive channel issues an interrupt that software should acknowledge with a FFFF FFFCh acknowledge value (note that there is no buffer descriptor in this case). Software may read the interrupt acknowledge location to determine if the interrupt was due to a commanded teardown. The read value will be FFFF FFFCh if the interrupt was due to a teardown command. 

## _**13.2.1.4.8.3 Receive CPDMA Interface**_ 

The receive CPDMA is an eight channel CPPI 3.0 compliant interface. Each channel has a single queue for frame reception. Priority between the eight queues may either be fixed or round robin as selected by FH_PTYPE in the CPDMA_Control register. If the priority type is fixed, then channel 7 has the highest priority and channel 0 has the lowest priority. Round robin priority proceeds from channel 0 to channel 7. Packet Data transfers occur on the TX_VBUSP interface in 64-byte maximum burst transfers. Any packet can be designated by the host to generate a host timesync event on Ethernet egress by setting the HOST_EVENT bit in the packet buffer descriptor. 

## _**13.2.1.4.8.3.1 Receive CPDMA Host Configuration**_ 

To configure the RX CPDMA for receive operations the software must perform the following: 

1. Initialize the RX_HDP registers to 0. 

2. Enable the desired receive interrupts in the CPDMA_RX_INTMASK_SET register. 

3. Setup the transmit channel(s) buffer descriptors in host memory as required by CPPI 3.0 

4. Configure and enable the receive operation as desired in the CPDMA_RX_CONTROL register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1359 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

5. Write the appropriate RX_HDP registers with the appropriate values to start packet operations. 

## _**13.2.1.4.8.3.2 Receive DMA Host Configuration**_ 

A receive buffer descriptor is a contiguous block of four 32-bit data words aligned on a 32-bit word boundary. 

## **Figure 13-106. RX Buffer Descriptor Format (Word 1)** 

|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|
|---|---|---|
|NEXT_DESCRIPTOR_POINTER|||
||||
|15<br>14<br>13<br>12<br>11<br>10<br>9<br>8<br>7<br>6<br>5<br>4<br>3<br>2<br>1<br>0|||
|NEXT_DESCRIPTOR_POINTER|||
||||
|**Bit**|**Field**|**Description**|
|31-0|NEXT_DESCRIPTOR_POINTER|The 32-bit word aligned memory address of the next buffer descriptor in the RX queue.<br>This is the mechanism used to reference the next buffer descriptor from the current<br>buffer descriptor. If the value of this pointer is zero, then the current buffer is the last<br>buffer in the queue. Set by the host.|
|**Figure 13-107. RX Buffer Descriptor Format(Word 2)**|||
|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|||
|BUFFER_POINTER|||
||||
|15<br>14<br>13<br>12<br>11<br>10<br>9<br>8<br>7<br>6<br>5<br>4<br>3<br>2<br>1<br>0|||
|BUFFER_POINTER|||
||||
|**Bit**|**Field**|**Description**|
|31-0|BUFFER_POINTER|The byte aligned memory address of the buffer associated with the buffer descriptor.<br>Set by the host.|
|**Figure 13-108. RX Buffer Descriptor Format(Word 3)**|||
|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|||
|BUFFER_OFFSET|||
||||
|15<br>14<br>13<br>12<br>11<br>10<br>9<br>8<br>7<br>6<br>5<br>4<br>3<br>2<br>1<br>0|||
|BUFFER_LENGTH|||



|**Bit**|**Field**|**Description**|
|---|---|---|
|32-16|BUFFER_OFFSET|Indicates how many unused bytes are at the start of the buffer. The buffer offset is<br>reduced to 12-bits. A value of 0x0000 indicates that there are no unused bytes at the<br>start of the buffer and that valid data begins on the first byte of the buffer. A value of<br>0x000F indicates that the first 15 bytes of the buffer are to be ignored by the port and<br>that valid buffer data starts on byte 16 of the buffer. The port writes BUFFER_OFFSET<br>with the value from the THost_BUFFER_OFFSET register value. The host initializes<br>the BUFFER_OFFSET to zero for free buffers. The BUFFER_LENGTH must be<br>greater that the THost_BUFFER_OFFSET register value. The buffer offset is valid<br>only on SOP.|
|15-0|BUFFER_LENGTH|Indicates how many valid data bytes are in the buffer. Unused or protocol specific<br>bytes at the beginning of the buffer are not counted in the Buffer_Length field. The<br>host sets the BUFFER_LENGTH. The BUFFER_LENGTH must be greater than zero.|



1360 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Figure 13-109. RX Buffer Descriptor Format (Word 4)** 

|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16|
|---|---|---|---|---|---|---|---|---|---|
|SOP|EOP|OWNE<br>RSHIP|EOQ|TEAR<br>DOWN<br>_COM<br>PLETE|PASS_<br>CRC|CRC_T<br>YPE|RESERVED|TO_P<br>ORT_E<br>N|TO_PORT|
|||||||||||
|15<br>14<br>13<br>12<br>11<br>10<br>9<br>8<br>7<br>6<br>5<br>4<br>3<br>2<br>1<br>0||||||||||
|HOST_<br>EVENT|CHKS<br>UM_E<br>NCAP|RESERVED||PACKET_LENGTH||||||



|**Bit**|**Field**|**Description**|
|---|---|---|
|31|SOP|Start of Packet- Indicates that the descriptor buffer is the first buffer in the packet. The<br>port sets the SOP bit.<br>0h - Not start of packet buffer<br>1h - Start of packet buffer|
|30|EOP|End of Packet- Indicates that the descriptor buffer is the last buffer in the packet. The<br>port sets the EOP bit.<br>0h - Not end of packet buffer<br>1h - End of packet buffer|
|29|OWNERSHIP|Ownership- Indicates ownership of the packet and is valid only on SOP. This bit must<br>be set by the host and is cleared by the port when the packet has been transferred<br>and the TH_OWNERSHIP bit is zero. The host uses this bit to reclaim buffers. If the<br>TH_OWNERSHIP bit is set then the port does not clear this bit which can reduce the<br>host workload in some applications.<br>0h - The packet is owned by the host<br>1h - The packet is owned by the port|
|28|EOQ|End of Queue- Set by the port to indicated that the RX queue empty condition exists.<br>This bit is valid only on EOP. The port determines the end of queue condition by a zero<br>NEXT_DESCRIPTOR_POINTER on an EOP buffer.<br>0h - The RX queue has more buffers available for reception.<br>1h - The Descriptor buffer is the last buffer in the last packet in the queue.|
|27|TEARDOWN_COMPLETE|Teardown Complete- Set by the port to indicate that the host commanded teardown<br>process is complete, and the channel buffers may be reclaimed by the host. The bit is<br>valid only on SOP.<br>0h - The port has not completed the teardown process<br>1h - The port has completed the commanded teardown process.|
|26|PASS_CRC|Pass CRC - Valid only on SOP<br>0h - A CRC is not included with the packet data. The Ethernet port(s) will generate the<br>CRC on Ethernet egress. A CRC (or placeholder) at the end of the data is allowed,<br>but not required, and the BUFFER_COUNT and PACKET_LENGTH fields should not<br>include the CRC bytes if they are present.<br>1h - A CRC is included with the host packet data. The PACKET_LENGTH and<br>BUFFER_COUNT fields should include the four CRC bytes. The host SUPPLIED CRC<br>should be in the last four bytes of the data.|
|25|CRC_TYPE|The packet CRC type.<br>0h: Ethernet CRC<br>1h: Castagnoli CRC|
|24-21|RESERVED|Reserved|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1361 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

|**Bit**|**Field**|**Description**|
|---|---|---|
|20|TO_PORT_EN|To Port Enable- Indicates when set that the packet is a directed packet to be sent to<br>the TO_PORT field port number. This field is set by the host. The packet is sent to one<br>port only (index not mask). This bit is valid on SOP.<br>0h - Not a directed packet<br>1h - Directed packet|
|19-16|TO_PORT|To Port - Port number to send the directed packet to. This field is set by the host. The<br>field is valid on SOP. Directed packets go to the directed port, but an ALE lookup is<br>performed to determine untagged egress in VLAN_AWARE more.<br>1h - Send the packet to port 1 if TO_PORT_EN is asserted.<br>2h - Send the packet to port 2 if TO_PORT_EN is asserted.|
|15|HOST_EVENT|Host Timesync Event - Generate a host timesync event on Ethernet egress. The<br>upper 28-bits of the packet SOP buffer descriptor address are the domain[7:0],<br>message_type[3:0], and sequence_id[15:0] in that order.<br>0h - The packet will not generate a host event on Ethernet egress.<br>1h - The packet will generate a host event on Ethernet egress.|
|14|CHKSUM_ENCAP|Checksum Encapsulated Packet - Indicates when set that the packet data contains<br>4-bytes of transmit checksum information at the end of the packet (last 4 bytes). The<br>packet length includes the checksum bytes.|
|13-12|RESERVED|Reserved|
|11-0|PACKET_LENGTH|Specifies the number of bytes in the entire packet. Offset bytes are not included.<br>The sum of the BUFFER_LENGTH fields should equal the PACKET_LENGTH. Valid<br>only on SOP. The packet length must be greater than zero. The packet data will be<br>truncated to the packet length if the packet length is shorter than the sum of the packet<br>buffer descriptor buffer lengths. A host error occurs if the packet length is greater than<br>the sum of the packet buffer descriptor buffer lengths.|



## _**13.2.1.4.8.3.3 Receive Channel Teardown**_ 

The host commands a receive channel teardown by writing the channel number to the CPDMA_RX_TEARDOWN register. When a teardown command is issued to an enabled receive channel the following will occur: 

- Any current frame in reception will complete normally. 

- The TEARDOWN_COMPLETE bit will be set in the next buffer descriptor in the chain (if there is one). 

- The channel head descriptor pointer will be cleared to 0. 

- A receive interrupt for the channel will be issued to the host. 

- The software should acknowledge a teardown interrupt with a FFFF FFFCh Acknowledge value. 

Channel teardown may be commanded on any channel at any time. The host is informed of the teardown completion by a set teardown complete buffer descriptor bit. The port does not clear any channel enables due to a teardown command. A teardown command to an inactive channel issues an interrupt that software should acknowledge with a FFFF FFFCh acknowledge value (note that there is no buffer descriptor in this case). Software may read the interrupt acknowledge location to determine if the interrupt was due to a commanded teardown. The read value will be FFFF FFFCh if the interrupt was due to a teardown command. 

## _**13.2.1.4.8.3.4 Receive CPDMA Hardware Controlled Packet Transmission**_ 

When configured with hardware packet transmission the receive interface can be enabled to transfer packets due to rising edges on a channel's corresponding RX_HW_TRIG[7:0] input. Each channel has a corresponding independent internal sent_cnt[15:0] counter. To enable hardware controlled packet transmission for a channel, software sets the channel's corresponding bit in the rx_hw_trig_en[7:0] field in the CPDMA_RX_Control2 register. Hardware packet transmission then operates as described below: 

1362 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

1. The channel send_cnt[15:0] is cleared to zero when the channel HDP is zero (IDLE). 

2. Software writes the channel HDP to begin the packet chain operation. 

3. An asserted RX_HW_TRIG[7:0] input increments the associated channel sent_cnt[15:0] when the channel's HDP is non-zero. 

4. A single packet is transferred when send_cnt is greater than 0 and then the send_cnt is decremented. 

5. Go to IDLE (#1) on EOQ (which also zeroes the HDP), otherwise continue with packet transmission (#4). 

## **Note** 

- Each channel has an associate send_cnt[15:0]. the send_cnt[15:0] register will not overflow or underflow. 

- The RX_HW_TRIG[7:0] inputs are asynchronous. They are synchronized and rising edge detected by the CPTS_RFTCLK. The pulse must be asserted high long enough for the high to be seen by the synchronizer, and asserted low long enough for the low to be seen by the synchronizer. 

- A rising edge on the RX_HW_TRIG bit increments the count regardless of the status of any previous packet transfer when the head descriptor pointer is nonzero. 

## _**13.2.1.4.8.4 VLAN Aware Mode**_ 

The CPSW is in VLAn Aware mode when the CPSW Control register vlan_aware bit is set. In VLAN aware mode port 0 transmit packets may or may not be VLAN encapsulated depending on the CPSW Control register TX_VLAN_ENCAP bit. The header packet VLAN is generated as described in later sections of this specification. VLAN encapsulated packets are specified by a set VLAN_ENCAP bit in the packet buffer descriptor. The VLAN encapsulation header is included in the packet length and has the below format: 

|The CPSW is in VLAn Aware mode when the CPSW Control register vlan_aware bit is set. In VLAN aware<br>mode port 0 transmit packets may or may not be VLAN encapsulated depending on the CPSW Control register<br>TX_VLAN_ENCAP bit. The header packet VLAN is generated as described in later sections of this specification.<br>VLAN encapsulated packets are specified by a set VLAN_ENCAP bit in the packet buffer descriptor. The VLAN<br>encapsulation header is included in the packet length and has the below format:|The CPSW is in VLAn Aware mode when the CPSW Control register vlan_aware bit is set. In VLAN aware<br>mode port 0 transmit packets may or may not be VLAN encapsulated depending on the CPSW Control register<br>TX_VLAN_ENCAP bit. The header packet VLAN is generated as described in later sections of this specification.<br>VLAN encapsulated packets are specified by a set VLAN_ENCAP bit in the packet buffer descriptor. The VLAN<br>encapsulation header is included in the packet length and has the below format:|The CPSW is in VLAn Aware mode when the CPSW Control register vlan_aware bit is set. In VLAN aware<br>mode port 0 transmit packets may or may not be VLAN encapsulated depending on the CPSW Control register<br>TX_VLAN_ENCAP bit. The header packet VLAN is generated as described in later sections of this specification.<br>VLAN encapsulated packets are specified by a set VLAN_ENCAP bit in the packet buffer descriptor. The VLAN<br>encapsulation header is included in the packet length and has the below format:|The CPSW is in VLAn Aware mode when the CPSW Control register vlan_aware bit is set. In VLAN aware<br>mode port 0 transmit packets may or may not be VLAN encapsulated depending on the CPSW Control register<br>TX_VLAN_ENCAP bit. The header packet VLAN is generated as described in later sections of this specification.<br>VLAN encapsulated packets are specified by a set VLAN_ENCAP bit in the packet buffer descriptor. The VLAN<br>encapsulation header is included in the packet length and has the below format:|The CPSW is in VLAn Aware mode when the CPSW Control register vlan_aware bit is set. In VLAN aware<br>mode port 0 transmit packets may or may not be VLAN encapsulated depending on the CPSW Control register<br>TX_VLAN_ENCAP bit. The header packet VLAN is generated as described in later sections of this specification.<br>VLAN encapsulated packets are specified by a set VLAN_ENCAP bit in the packet buffer descriptor. The VLAN<br>encapsulation header is included in the packet length and has the below format:|The CPSW is in VLAn Aware mode when the CPSW Control register vlan_aware bit is set. In VLAN aware<br>mode port 0 transmit packets may or may not be VLAN encapsulated depending on the CPSW Control register<br>TX_VLAN_ENCAP bit. The header packet VLAN is generated as described in later sections of this specification.<br>VLAN encapsulated packets are specified by a set VLAN_ENCAP bit in the packet buffer descriptor. The VLAN<br>encapsulation header is included in the packet length and has the below format:|
|---|---|---|---|---|---|
|**Figure 13-110. 32-bit VLAN Header Encapsulation Word Format**||||||
|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16||||||
|HDR_PKT_PRIORITY||HDR_<br>PKT_C<br>FI|HDR_PKT_VID|||
|||||||
|15<br>14<br>13<br>12<br>11<br>10<br>9<br>8<br>7<br>6<br>5<br>4<br>3<br>2<br>1<br>0||||||
|FLOW||||PKT_TYPE|RESERVED|
|||||||
|**Bit**|**Field**|||**Description**||
|31-29|HDR_PKT_PRIORITY|||Header Packet VLAN priority (7 is highest priority)||
|28|HDR_PKT_CFI|||Header Packet VLAN CFI bit||
|27-16|HDR_PKT_VID|||Header Packet VLAN ID||
|15-10|FLOW|||FLOW - A nonzero value indicates that the ALE matched a classifier with the FLOW<br>(threadval)||
|9-8|PKT_TYPE|||Packet Type - Indicates whether the packet is a VLAN tagged, priority tagged, or<br>non-tagged packet.<br>00h - VLAN tagged packet<br>01h - Reserved<br>10h - priority tagged packet<br>11h - non-tagged packet||
|7-0|RESERVED|||Reserved||



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1363 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.8.5 VLAN Unaware Mode**_ 

The CPSW is in VLAN unaware mode when the CPSW Control register vlan_aware bit is cleared. Port 0 transmit packets (egress) may or may not be VLAn encapsulated depending on the CPSW Control register TX_VLAN_ENCAP bit. 

## _**13.2.1.4.8.6 CPDMA Big Endian Mode**_ 

When the CPSW_BIG_ENDIAN input is asserted, the CPDMA assumes that the packet data is contained in memory in big endian format. When the CPDMA_BIG_ENDIAN input is deasserted, the CPDMA assumes that packet data is contained in memory in little endian format. The CPDMA_BIG_ENDIAN input causes big endian packet data to go out on the wire in the same order that the little endian packet data goes out on the wire when the input is not asserted (byte 0 first). The CPDMA_BIG_ENDIAN input has no effect on buffer descriptor data reads or writes because buffer descriptor data is a 32-bit quantity (unlike packet data which is an 8-bit quantity). 

**Table 13-156. Little Endian** 

|**High Add**|||**Low Add**|
|---|---|---|---|
|Byte 3|Byte 2|Byte 1|Byte 0|
|Byte 7|Byte 6|Byte 5|Byte 4|
|Byte 11|Byte 10|Byte 9|Byte 8|
||||...|



**Table 13-157. Big Endian** 

|**High Add**|||**Low Add**|
|---|---|---|---|
|Byte 0|Byte 1|Byte 2|Byte 3|
|Byte 4|Byte 5|Byte 6|Byte 7|
|Byte 8|Byte 9|Byte 10|Byte 11|
||||...|



## _**13.2.1.4.8.7 CPDMA Command IDLE**_ 

The cmd_idle bit in the CPDMA_Control register allows CPDMA operation to be suspended. When the idle state is commanded, the CPDMA will stop processing transmit and receive frames at the next frame boundary. Any frame currently in reception or transmission will be completed normally without suspension. For receive, and frame in process will be completed. For transmit, frames that are detected by the CPDMA after the suspend state is entered are ignored. No statistics will be kept for ignored frames. Commanded idle is similar in operation to emulation control and clock stop. 

## _**13.2.1.4.8.8 CPDMA CPPI 3.0 Interface Bandwidth**_ 

The HOST CPPI 3.0 Receive and Transmit interfaces are capable of supporting linerate on the Ethernet ports provided that the clock frequency is sufficient, and provided that the Host controller VBUSP read/write latency is low. 

## _**13.2.1.4.9 CPPI Checksum Offload**_ 

The CPPI host port can be enabled to perform checksum offload on host port packet ingress and egress. UDP (User Datagram Protocol) and TCP (Transmission Control Protocol) over IPV4 and IPV6 are supported. For the purposes of checksum description, the first packet byte (the first byte of the destination address) is byte 1 (not byte 0). That is, a 64 byte packet goes from byte 1 to byte 64. For all packet types, the S_CN_SWITCH bit in the CPSW_CONTROL_REG register must be set for the Outer VLAN L type to be supported. 

## _**13.2.1.4.9.1 CPPI Transmit Checksum Offload**_ 

IPV4 and IPV6 UDP and TCP packets that are received on any Ethernet port and destined for port 0 egress are checked for correct checksum as described below. The EOP Transmit buffer descriptor bit CHKSUM_ENCAP indicates whether or not the transmit checksum information is included with the egress packet or not. If the checksum information is included in the packet, the PACKET_LENGTH includes the four checksum information 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

1364 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

bytes. The byte counts below are shown for packets with no VLAN’s. The byte counts vary with one or two packet VLAN's. Packets received on an Ethernet port with errors are not checked for a correct checksum if they are passed to the host (no checksum information with the error packet). 

## _**13.2.1.4.9.1.1 IPV4 UDP**_ 

- Byte 15 Upper Nibble = 4 for IPV4 

- Byte 15 Lower Nibble = IHL - Nibble with number of 32-bit words in IPV4 header (5 to 15 supported). 

- Bytes 20-21 = fragment[15-0] – Bit 13 is the MF bit and bits [12-0] are the Fragment offset. A packet is a fragment if the MF bit is set or if the fragment offset is non-zero. The first packet fragment has MF=1 with a zero offset. Middle fragments have MF=1 with a nonzero offset. The last packet fragment has MF=0 with a nonzero offset. Non-fragmented packets have MF=0 and a zero offset. A count is output for packet fragments but no errors are reported. First fragments have the UDP header included in the count. Middle and last fragments have only data included in the count (there is no UDP header). 

- Byte 24 = 0x11 for UDP protocol. 

- Received packet UDP checksum of zero means that there is no IPV4 checksum sent with the packet so no error will be issued. 

- Received packet UDP checksum of 0xFFFF means that the checksum was calculated to be 0xFFFF or 0x0000 but was sent in the transmitted packet as 0xFFFF by the sending originating entity. 

## _**13.2.1.4.9.1.2 IPV4 TCP**_ 

- Byte 15 Upper Nibble = 4 for IPV4 

- Byte 15 Lower Nibble = IHL - Nibble with number of 32-bit words in IPV4 header (5 to 15 supported). 

- Bytes 20-21 = fragment[15-0] – Bit 13 is the MF bit and bits [12-0] are the Fragment offset. A packet is a fragment if the MF bit is set or if the fragment offset is non-zero. The first packet fragment has MF=1 with a zero offset. Middle fragments have MF=1 with a nonzero offset. The last packet fragment has MF=0 with a nonzero offset. Non-fragmented packets have MF=0 and a zero offset. A count is output for packet fragments but no errors are reported. First fragments have the UDP header included in the count. Middle and last fragments have only data included in the count (there is no TCP header). 

- Byte 24 = 0x06 for TCP protocol. 

## _**13.2.1.4.9.1.3 IPV6 UDP**_ 

- Byte 15 upper nibble = 6 for IPV6. 

- Byte 21 = 0x11 for UDP protocol as next header. 

- Fragment extension headers are supported. First fragments have a fragment extension header (byte 21 = 0x2C) followed by a UDP header (byte 55 = 0x11). Middle and last fragments have a fragment extension header followed by data only (no UDP header). The first packet fragment has MF=1 with a zero offset. Middle fragments have MF=1 with a nonzero offset. The last packet fragment has MF=0 with a nonzero offset. Non-fragmented packets do not have a fragment extension header. A count is output for packet fragments but no errors are reported. 

- Received packet UDP checksum of zero means that there is no IPV6 checksum sent with the packet so no error will be issued. 

- Received packet UDP checksum of 0xFFFF means that the checksum was calculated to be 0xFFFF or 0x0000 but was sent in the transmitted packet as 0xFFFF by the sending originating entity. 

## _**13.2.1.4.9.1.4 IPV6 TCP**_ 

- Byte 15 upper nibble = 6 for IPV6. 

- Byte 21 = 0x06 for TCP protocol as next header. 

- Fragment extension headers are supported. First fragments have a fragment extension header (byte 21 = 0x2C) followed by a UDP header (byte 55 = 0x06). Middle and last fragments have a fragment extension header followed by data only (no TCP header). The first packet fragment has MF=1 with a zero offset. Middle fragments have MF=1 with a nonzero offset. The last packet fragment has MF=0 with a nonzero offset. Non-fragmented packets do not have a fragment extension header. A count is output for packet fragments but no errors are reported. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1365 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.9.1.5 Transmit Checksum Encapsulation Word**_ 

The 4-byte checksum encapsulation word is included as the last 4-bytes of the transmit packet data when EOP buffer descriptor CHKSUM_ENCAP is set. The PACKET_LENGTH includes the four encapsulation bytes. 

|The 4-byte checksum encapsulation word is included as the last 4-bytes of the transmit packet data when EOP<br>buffer descriptor CHKSUM_ENCAP is set. The PACKET_LENGTH includes the four encapsulation bytes.|The 4-byte checksum encapsulation word is included as the last 4-bytes of the transmit packet data when EOP<br>buffer descriptor CHKSUM_ENCAP is set. The PACKET_LENGTH includes the four encapsulation bytes.|The 4-byte checksum encapsulation word is included as the last 4-bytes of the transmit packet data when EOP<br>buffer descriptor CHKSUM_ENCAP is set. The PACKET_LENGTH includes the four encapsulation bytes.|The 4-byte checksum encapsulation word is included as the last 4-bytes of the transmit packet data when EOP<br>buffer descriptor CHKSUM_ENCAP is set. The PACKET_LENGTH includes the four encapsulation bytes.|The 4-byte checksum encapsulation word is included as the last 4-bytes of the transmit packet data when EOP<br>buffer descriptor CHKSUM_ENCAP is set. The PACKET_LENGTH includes the four encapsulation bytes.|The 4-byte checksum encapsulation word is included as the last 4-bytes of the transmit packet data when EOP<br>buffer descriptor CHKSUM_ENCAP is set. The PACKET_LENGTH includes the four encapsulation bytes.|
|---|---|---|---|---|---|
|**Figure 13-111. Transmit Checksum Encapsulation Word Format**||||||
|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16||||||
|RESERVED|IPV4_<br>VALID|IPV6_<br>VALID|TCP_U<br>DP_N|FRAG<br>MENT|CHKS<br>UM_E<br>RROR|
|||||||
|15<br>14<br>13<br>12<br>11<br>10<br>9<br>8<br>7<br>6<br>5<br>4<br>3<br>2<br>1<br>0||||||
|CHECKSUM_ADD||||||



|**Bit**|**Field**|**Description**|
|---|---|---|
|31-21|RESERVED|Reserved|
|20|IPV4_VALID|An IPV4 TCP or UDP packet was detected|
|19|IPV6_VALID|An IPV6 TCP or UDP Packet was detected|
|18|TCP_UDP_N|TCP or UDP packet - Valid only when either the IPV4_VALID or IPV6_VALID bits are<br>set<br>0h - Indicates UDP packet was detected<br>1h - Indicates TCP packet was detected|
|17|FRAGMENT|Indicates that an IP fragment was detected. Valid only when either the IPV4_VALID or<br>IPV6_VALID bits are set.|
|16|CHKSUM_ERROR|Checksum Error detected. Valid only when either the IPV4_VALID or IPV6_VALID bits<br>are set.|
|15-0|CHECKSUM_ADD|Checksum Add Value - this is the value that was summed during the checksum<br>computation. This value is 0xFFFF for IPV4/6 UDP/TCP packets with no checksum<br>error.|



## _**13.2.1.4.9.2 CPPI Receive Checksum Offload**_ 

Packets sent from host port 0 (switch ingress) to any Ethernet port can have a checksum calculated and inserted into the Ethernet egress packet. The RX_CHECKSUM_EN bit in the CPSW_P0_CONTROL_REG register must be set for receive checksum operation to be enabled. When bit RX_CHECKSUM_EN is enabled and when the CHKSUM_ENCAP SOP receive buffer descriptor is set, the first four packet bytes contain the checksum information which determines how the checksum is calculated. The CHECKSUM_RESULT field determines where the checksum is inserted in the egress packet. The checksum result location is adjusted by the egress port if a VLAN is to be inserted or removed on Ethernet port egress. 

## _**13.2.1.4.9.2.1 Receive Checksum Encapsulation Word**_ 

The 4-byte checksum encapsulation word is included as the first 4-bytes of the receive packet data when SOP buffer descriptor CHKSUM_ENCAP is set. The PACKET_LENGTH includes the four encapsulation bytes. 

|The 4-byte checksum encapsulation word is included as the first 4-bytes of the receive packet data when SOP<br>buffer descriptor CHKSUM_ENCAP is set. The PACKET_LENGTH includes the four encapsulation bytes.|The 4-byte checksum encapsulation word is included as the first 4-bytes of the receive packet data when SOP<br>buffer descriptor CHKSUM_ENCAP is set. The PACKET_LENGTH includes the four encapsulation bytes.|
|---|---|
|**Figure 13-112. Receive Checksum Encapsulation Word Format**||
|31<br>30<br>29<br>28<br>27<br>26<br>25<br>24<br>23<br>22<br>21<br>20<br>19<br>18<br>17<br>16||
|CHECKSUM_RESULT|CHECKSUM_START_BYTE|
|||
|15<br>14<br>13<br>12<br>11<br>10<br>9<br>8<br>7<br>6<br>5<br>4<br>3<br>2<br>1<br>0||



1366 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

## **Figure 13-112. Receive Checksum Encapsulation Word Format (continued)** 

CHKS RESE CHECKSUM_BYTECOUNT UM_IN RVED V 

|**Bit**|**Field**|**Description**|
|---|---|---|
|31-24|CHECKSUM_RESULT|Checksum Result Byte Location. This is the packet byte number where the checksum<br>result will be placed in the egress packet. The first packet byte which is the first byte of<br>the destination address is byte 1 (not byte zero).|
|23-16|CHECKSUM_START_BYTE|Checksum Start Byte. This is the packet byte number to start the checksum calculation<br>on. The first packet byte is byte 1.|
|15|CHKSUM_INV|Checksum Invert Zero. When set, a zero checksum value will be inverted and sent as<br>0xFFFF.|
|14|RESERVED|Reserved|
|13-0|CHECKSUM_BYTECOUNT|Checksum Byte Count. This is the number of bytes to calculate the checksum on. The<br>outgoing Ethernet packet will have a checksum inserted when this value is non-zero.|



## _**13.2.1.4.10 Egress Packet Operations**_ 

Each CPSW egress port (Ethernet and Host) is capable of performing egress packet processing operations (CPSW_ALE_EGRESSOP). IntraVLAN processing either adds, removes, or replaces VLAN information or does nothing. InterVLAN routing allows hardware routing between a limited number of VLANs - thereby allowing high-bandwidth or other routing operations to be offloaded from software to the CPSW (hardware). IntraVLAN processing and InterVLAN routing operations are mutually exclusive. In addition, the packet source and destination addresses can be swapped on egress to facilitate OAM or generic testing operations. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

1367 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

## _**13.2.1.4.11 MII Management Interface (MDIO)**_ 

The MII Management interface module implements the 802.3 serial management interface to interrogate and control external Ethernet PHY using a two-wire bus. 

## _**13.2.1.4.11.1 MDIO Frame Formats**_ 

Table 13-158 shows the address, Table 13-159 shows the read format and Table 13-160 shows the write format of the supported Clause 45 MII Management interface frames. Post-increment accesses are not supported. 

**Table 13-158. MDIO Clause 45 Address Frame Format** 

|**Pre-amble**|**Start Delimiter**|**Operation**<br>**Code**|**PHY Address**|**MMD Number**|**Turnaround**|**Data**|
|---|---|---|---|---|---|---|
|FFFF FFFFh|00|00|AAAAA|RRRRR|10|AAAA.AAAA.AAAA.AAAA|
|||**Table 13-159. MDIO Clause 45 Read Frame Format**|||||
|**Pre-amble**|**Start Delimiter**|**Operation**<br>**Code**|**PHY Address**|**MMD Number**|**Turnaround**|**Data**|
|FFFF FFFFh|00|11|AAAAA|RRRRR|Z0|DDDD.DDDD.DDDD.DDDD|
|||**Table 13-160. MDIO Clause 45 Write Frame Format**|||||
|**Pre-amble**|**Start Delimiter**|**Operation**<br>**Code**|**PHY Address**|**MMD Number**|**Turnaround**|**Data**|
|FFFF FFFFh|00|01|AAAAA|RRRRR|10|DDDD.DDDD.DDDD.DDDD|



The default or idle state of the two wire serial interface is a logic one. All tri-state drivers should be disabled and the PHY's pull-up resistor will pull the MDIO line to a logic 1. Prior to initiating any other transaction, the station management entity shall send a preamble sequence of 32 contiguous logic 1 bits on the MDIO line with 32 corresponding cycles on MDCLK to provide the PHY with a pattern that it can use to establish synchronization. A PHY shall observe a sequence of 32 contiguous logic one bits on MDIO with 32 corresponding MDCLK cycles before it responds to any other transaction. The MDIO CPSW_MDIO_USER_ADDR0_REG register must be written before a read or write operation is performed to set the address used in the operation. Each read or write operation has a preceeding address frame. 

## **Preamble** 

The start of a frame is indicated by a preamble, which consists of a sequence of 32 contiguous bits all of which are a 1. This sequence provides the PHY a pattern to use to establish synchronization. The preamble is required in clause 45 operation. 

## **Start Delimiter** 

The preamble is followed by the start delimiter which is indicated by a 00 pattern. 

## **Operation Code** 

The operation code for an address transaction is 00. The operation code for a read is 11, while the operation code for a write is a 01. 

## **PHY Address** 

The PHY address is 5 bits allowing 32 unique values. The first bit transmitted is the MSB of the PHY address. 

## **MMD Number** 

The MMD number is the 5 bits allowing 32 unique values. The first bit transmitted is the MSB. 

## **Turnaround** 

An idle bit time during which no device actively drives the MDIO signal shall be inserted between the register address field and the data field of a read frame in order to avoid contention. During a read frame, the PHY shall 

1368 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

drive a zero bit onto MDIO for the first bit time following the idle bit and preceding the Data field. During a write frame, this field shall consist of a one bit followed by a zero bit. 

## **Address** 

The address field is 16 bits on address operations. The first bit transmitted is the MSB of the address word. Each read/write operation initiated has an automatic address operation initiated first that uses the MDIO CPSW_MDIO_USER_ADDR0_REG/ CPSW_MDIO_USER_ADDR1_REG register values as the 16-bit address. 

## **Data** 

The Data field is 16 bits on read and write operations. The first bit transmitted and received is the MSB of the data word. 

## _**13.2.1.4.11.2 MDIO Functional Description**_ 

The MII Management I/F will remain idle until enabled by setting the ENABLE bit in the CPSW_MDIO_CONTROL_REG register. The MII Management I/F will then continuously poll the link status from within the Generic Status Register of all possible 32 PHY addresses in turn recording the results in the MDIO CPSW_MDIO_LINK_REG register. Individual PHY’s can be enabled or disabled for polling the associated bit in the CPSW_MDIO_POLL_EN_REG register. The CPSW_MDIO_LINK_REG and CPSW_MDIO_ALIVE_REG register bit values are updated on the poll of each PHY. The LINKSEL bit in the CPSW_MDIO_USER_PHY_SEL_REG_k register determines the status input that is used. A change in the link status of the two PHYs being monitored will set the appropriate bit in the MDIO CPSW_MDIO_LINK_INT_RAW_REG register and the MDIO CPSW_MDIO_LINK_INT_MASKED_REG register, if enabled by the LINKINT_ENABLE bit in the CPSW_MDIO_USER_PHY_SEL_REG_k register. 

The MDIO CPSW_MDIO_ALIVE_REG register is updated by the MII Management I/F module if the PHY acknowledged the read of the generic status register. In addition, any PHY register read transactions initiated by the host also cause the MDIO CPSW_MDIO_ALIVE_REG register to be updated. 

At any time, the host can define a transaction for the MII Management interface module to undertake using the DATA, PHYADR, REGADR, and WRITE fields in a CPSW_MDIO_USER_ACCESS_REG_k register. When the host sets the GO bit in this register, the MII Management interface module will begin the transaction without any further intervention from the host. Upon completion, the MII Management interface will clear the GO bit and set the USERINTRAW field in the CPSW_MDIO_USER_INT_RAW_REG register corresponding to the CPSW_MDIO_USER_ACCESS_REG_k register being used. The corresponding bit in the CPSW_MDIO_USER_INT_MASKED_REG register may also be set depending on the mask setting in the MDIO CPSW_MDIO_USER_INT_MASK_SET_REG and CPSW_MDIO_USER_INT_MASK_CLEAR_REG registers. A round-robin arbitration scheme is used to schedule transactions that may be queued by the host in different CPSW_MDIO_USER_ACCESS_REG_k registers. The host should check the status of the GO bit in the MDIO CPSW_MDIO_USER_ACCESS_REG_k register before initiating a new transaction to ensure that the previous transaction has completed. The host can use the ACK bit in the MDIO CPSW_MDIO_USER_ACCESS_REG_k register to determine the status of a read transaction. 

It is necessary for software to use the MII Management interface module to setup the auto-negotiation parameters of each PHY attached to a MAC port, retrieve the negotiation results, and setup the CPSW_PN_MAC_CONTROL_REG register in the corresponding MAC. 

## **13.2.1.5 CPSW0 Programming Guide** 

## _**13.2.1.5.1 Initialization and Configuration of CPSW Subsystem**_ 

To configure the CPSW Ethernet Subsystem for operation, the host must perform the following: 

1. Select the Interface (RMII, or RGMII ) Mode. See the CTRLMMR_ENET1_CTRL and CTRLMMR_ENET2_CTRL[2-0] PORT_MODE_SEL fields. 

2. Configure pads (pin muxing), as per the interface selected. Refer to _Pad Configuration Registers_ and the device-specific Data sheet. 

3. Enable the CPSW Ethernet Subsystem clocks. See _CPSW Integration_ 

4. Ensure that at least 2000 CPPI_ICLK periods are run after reset is de-asserted. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1369 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

5. Configure the CPSW_CONTROL_REG register 

6. Configure the Ethernet Port Source Address registers (CPSW_PN_SA_L_REG_k and CPSW_PN_SA_H_REG_k) 

7. Configure the CPSW statistic port enable register CPSW_STAT_PORT_EN_REG 

8. Configure the ALE (Section 13.2.1.4.6.1, _Address Lookup Engine_ ) 

9. Configure the MDIO (Section 13.2.1.5.5.1, _Initializing the MDIO Module_ ) 

10. Configure Ethernet port, as per the desired mode of operations 

## _**13.2.1.5.2 Transmit Operation**_ 

After reset, the host must write zeroes to all TX DMA State head descriptor pointers. The TX port may then be enabled. To initiate packet transmission the host constructs transmit queues in memory (one or more packets for transmission) and then writes the appropriate TX DMA state head descriptor pointers. For each buffer added to a transmit queue, the host must initialize the TX buffer descriptor values as follows: 

1. Write the Next Descriptor Pointer with the 32-bit aligned address of the next descriptor in the queue (zero if last descriptor) 

2. Write the Buffer Pointer with the byte aligned address of the buffer data 

3. Write the Buffer Length with the number of bytes in the buffer 

4. Write the Buffer Offset with the number of bytes in the offset to the data (nonzero with SOP only) 

5. Set the SOP, EOP, and Ownership bits as appropriate 

6. Clear the End Of Queue bit 

The port begins TX packet transmission on a given channel when the host writes the channel's TX queue head descriptor pointer with the address of the first buffer descriptor in the queue (nonzero value). Each channel may have one or more queues, so each channel may have one or more head descriptor pointers. The first buffer descriptor for each TX packet must have the Start of Packet (SOP) bit and the Ownership bit set to one by the host. The last buffer descriptor for each TX packet must have the End of Packet (EOP) bit set to one by the host. The port will transmit packets until all queued packets have been transmitted and the queue(s) are empty. When each packet transmission is complete, the port will clear the Ownership bit in the packet's SOP buffer descriptor and issue an interrupt to the host by writing the packet's last buffer descriptor address to the queue's TX DMA State Completion Pointer. The interrupt is generated by the write, regardless of the value written. When the last packet in a queue has been transmitted, the port sets the End Of Queue bit in the EOP buffer descriptor, clears the Ownership bit in the SOP Descriptor, zeroes the appropriate DMA state head descriptor pointer, and then issues a TX interrupt to the host by writing to the queue's associated TX completion pointer (address of the last buffer descriptor processed by the port). The port issues a maskable level interrupt (which may then be routed through external interrupt control logic to the host). 

On interrupt from the port, the host processes the buffer queue, detecting transmitted packets by the status of the Ownership bit in the SOP buffer descriptor. If the Ownership bit is cleared to zero, then the packet has been transmitted and the host may reclaim the buffers associated with the packet. The host continues queue processing until the end of the queue or until a SOP buffer descriptor is read that contains a set Ownership bit indicating that the packet transmission is not complete. The host determines that all packets in the queue have been transmitted when the last packet in the queue has a cleared Ownership bit in the SOP buffer descriptor, the End of Queue bit is set in the last packet EOP buffer descriptor, and the Next Descriptor Pointer of the last packet EOP buffer descriptor is zero. The host acknowledges an interrupt by writing the address of the last buffer descriptor to the queue's associated TX Completion Pointer in the TX DMA State. If the host written buffer address value is different from the buffer address written by the port, then the level interrupt remains asserted. If the host written buffer address value is equal to the port written value, then the level interrupt is de-asserted. The port write to the completion pointer actually stores the value in the state register (RAM). The host written value is actually not written to the register location. The host written value is compared to the register contents (which was written by the port) and if the two values are equal, the interrupt is removed, otherwise the interrupt remains asserted. The host may process multiple packets previous to acknowledging an interrupt, or the host may acknowledge interrupts for every packet. 

1370 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

A mis-queued packet condition may occur when the host adds a packet to a queue for transmission as the port finishes transmitting the previous last packet in the queue. The mis-queued packet is detected by the host when queue processing detects a cleared Ownership bit in the SOP buffer descriptor, a set End of Queue bit in the EOP buffer descriptor, and a nonzero Next Descriptor Pointer in the EOP buffer descriptor. A mis-queued packet means that the port read the last EOP buffer descriptor before the host added the new last packet to the queue, so the port determined queue empty just before the last packet was added. The host corrects the mis-queued packet condition by initiating a new packet transfer for the mis-queued packet by writing the mis-queued packet's SOP buffer descriptor address to the appropriate DMA State TX Queue head Descriptor Pointer. 

The host may add packets to the tail end of an active TX queue at any time by writing the Next Descriptor Pointer to the current last descriptor in the queue. If a TX queue is empty (inactive), the host may initiate packet transmission at any time by writing the appropriate TX DMA State head descriptor pointer. The host software should always check for and reinitiate transmission for mis-queued packets during queue processing on interrupt from the port. In order to preclude software underrun, the host should avoid adding buffers to an active queue for any TX packet that is not complete and ready for transmission. 

The port determines that a packet is the last packet in the queue by detecting the End of Packet bit set with a zero Next Descriptor Pointer in the packet buffer descriptor. If the End of Packet bit is set and the Next Descriptor Pointer is nonzero, then the queue still contains one or more packets to be transmitted. If the EOP bit is set with a zero Next Descriptor Pointer, then the port will set the EOQ bit in the packet's EOP buffer descriptor and then zero the appropriate head descriptor pointer previous to interrupting the port (by writing the completion pointer) when the packet transmission is complete. 

**==> picture [345 x 277] intentionally omitted <==**

**----- Start of picture text -----**<br>
SOP Descriptor<br>Buffer<br>Descriptor<br>Buffer<br>EOP Descriptor<br>Buffer<br>SOP Descriptor<br>Buffer<br>EOP Descriptor<br>Buffer<br>Host<br>Memory<br>Port Tx<br>Tx Queue Head Descriptor Pointer State RAM<br>Entry<br>cpsw-016<br>**----- End of picture text -----**<br>


**Figure 13-113. TX Queue Head Descriptor** 

## _**13.2.1.5.3 Receive Operation**_ 

After reset, the host must write zeroes to all RX DMA State head descriptor pointers. The RX port may then be enabled. To initiate packet reception, the host constructs receive queues in memory and then writes the appropriate RX DMA state head descriptor pointer. For each RX buffer descriptor added to the queue, the host must initialize the RX buffer descriptor values as follows: 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1371 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

1. Write the Next Descriptor Pointer with the 32-bit aligned address of the next descriptor in the queue (zero if last descriptor) 

2. Write the Buffer Pointer with the byte aligned address of the buffer data 

3. Clear the Offset field 

4. Write the Buffer Length with the number of bytes in the buffer 

5. Clear the SOP, EOP, and EOQ bits 

6. Set the Ownership bit 

The host enables packet reception on a given channel by writing the address of the first buffer descriptor in the queue (nonzero value) to the channel's head descriptor pointer in the channel's RX DMA state. When packet reception begins on a given channel, the port fills each RX buffer with data in order starting with the first buffer and proceeding through the RX queue. If the Buffer Offset in the RX DMA State is nonzero, then the port will begin writing data after the offset number of bytes in the SOP buffer. The port performs the following operations at the end of each packet reception: 

1. Overwrite the buffer length in the packet's EOP buffer descriptor with the number of bytes actually received in the packet's last buffer. The host initialized value is the buffer size. The overwritten value will be less than or equal to the host initialized value. 

2. Set the EOP bit in the packet's EOP buffer descriptor. 

3. Set the EOQ bit in the packet's EOP buffer descriptor if the current packet is the last packet in the queue. 

4. Overwrite the packet's SOP buffer descriptor Buffer Offset with the RX DMA state value (the host initialized the buffer descriptor Buffer Offset value to zero). All non SOP buffer descriptors must have a zero Buffer Offset initialized by the host. 

5. Overwrite the packet's SOP buffer descriptor buffer length with the number of valid data bytes in the buffer. If the buffer is filled up, the buffer length will be the buffer size minus buffer offset. 

6. Set the SOP bit in the packet's SOP buffer descriptor. 

7. Write the SOP buffer descriptor Packet Length field. 

8. Clear the Ownership bit in the packet's SOP buffer descriptor. 

9. Issue an RX host interrupt by writing the address of the packet's last buffer descriptor to the queue's RX DMA State Completion Pointer. The interrupt is generated by the write to the RX DMA State Completion Pointer address location, regardless of the value written. 

On interrupt the host processes the RX buffer queue detecting received packets by the status of the Ownership bit in each packet's SOP buffer descriptor. If the Ownership bit is cleared then the packet has been completely received and is available to be processed by the host. The host may continue RX queue processing until the end of the queue or until a buffer descriptor is read that contains a set Ownership bit indicating that the next packet's reception is not complete. The host determines that the RX queue is empty when the last packet in the queue has a cleared Ownership bit in the SOP buffer descriptor, a set End of Queue bit in the EOP buffer descriptor, and the Next Descriptor Pointer in the EOP buffer descriptor is zero. 

A mis-queued buffer may occur when the host adds buffers to a queue as the port finishes the reception of the previous last packet in the queue. The mis-queued buffer is detected by the host when queue processing detects a cleared Ownership bit in the SOP buffer descriptor, a set End of Queue bit in the EOP buffer descriptor, and a nonzero Next Descriptor Pointer in the EOP buffer descriptor. A mis-queued buffer means that the port read the last EOP buffer descriptor before the host added buffer descriptor(s) to the queue, so the port determined queue empty just before the host added more buffer descriptor(s). In the transmit case, the packet transmission is delayed by the time required for the host to determine the condition and reinitiate the transaction, but the packet is not actually lost. In the receive case, receive overrun condition may occur in the mis-queued buffer case. If a new packet reception is begun during the time that the port has determined the end of queue condition, then the received packet will overrun (start of packet overrun). If the mis-queued buffer occurs during the middle of a packet reception then middle of packet overrun may occur. If the mis-queued buffer occurs after the last packet has completed, and is corrected before the next packet reception begins, then overrun will not occur. The host acts on the mis-queued buffer condition by writing the added buffer descriptor address to the appropriate RX DMA State Head Descriptor Pointer. 

1372 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Peripherals_ 

**==> picture [317 x 292] intentionally omitted <==**

**----- Start of picture text -----**<br>
Descriptor<br>Buffer<br>Descriptor<br>Buffer<br>Descriptor<br>Buffer<br>Descriptor<br>Buffer<br>Descriptor<br>Buffer<br>Host<br>Memory<br>Port Rx<br>Rx Queue Head Descriptor Pointer DMA State<br>cpsw-017<br>**----- End of picture text -----**<br>


**Figure 13-114. RX Queue Head Descriptor** 

## _**13.2.1.5.4 CPSW Reset**_ 

To reset the Ethernet port, the host must perform the following: 

1. Set CMD_IDLE bit to 1h in the Ethernet port control register: CPSW_PN_MAC_CONTROL_REG. 

2. Wait for IDLE bit to be set to 1h, which is indicated in the Ethernet port status register: CPSW_PN_MAC_STATUS_REG. 

3. Set SOFT_RESET bit to 1h in the Ethernet port software reset register: CPSW_PN_MAC_SOFT_RESET_REG. 

4. Wait for SOFT_RESET bit in the CPSW_PN_MAC_SOFT_RESET_REG registers to be cleared to confirm reset completion. 

5. Configure the Ethernet ports. 

6. Re-configure registers reset to default value by CPSW_PN_MAC_SOFT_RESET_REG. 

## _**13.2.1.5.5 MDIO Software Interface**_ 

## _**13.2.1.5.5.1 Initializing the MDIO Module**_ 

The following steps are performed by the application software or device driver to initialize the MDIO device: 

1. Configure the PREAMBLE and CLKDIV bits in the MDIO Control register (CPSW_MDIO_CONTROL_REG). 

2. Enable the MDIO module by setting the ENABLE bit in CPSW_MDIO_CONTROL_REG. 

3. The MDIO PHY alive status register (MDIO CPSW_MDIO_ALIVE_REG) can be read in polling fashion until a PHY connected to the system responded, and the MDIO PHY link status register (MDIO CPSW_MDIO_LINK_REG) can determine whether this PHY already has a link. 

4. Set the appropriate PHY addresses in the MDIO user PHY select register (CPSW_MDIO_USER_PHY_SEL_REG_k, where k = 0 or 1), and set the LINKINT_ENABLE bit to enable a link change event interrupt if desirable. 

5. Set the appropriate LINKSEL bit in the CPSW_MDIO_USER_PHY_SEL_REG_k register (where k = 0 or 1). 

6. Set the appropriate USERINTMASKSET bit field in the CPSW_MDIO_USER_INT_MASK_SET_REG register. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 1373 

Copyright © 2025 Texas Instruments Incorporated 

_Peripherals_ 

www.ti.com 

7. If an interrupt on general MDIO register access is desired, set the corresponding bit in the MDIO user command complete interrupt mask set register (MDIO CPSW_MDIO_USER_INT_MASK_SET_REG) to use the MDIO user access register (MDIO CPSW_MDIO_USER_ACCESS_REG_k, where k = 0 or 1). 

## _**13.2.1.5.5.2 Writing Data To a PHY Register**_ 

The MDIO module includes a user access register (MDIO CPSW_MDIO_USER_ACCESS_REG_k, where k = 0 or 1) to directly access a specified PHY device. To write a PHY register, perform the following: 

1. Check to ensure that the GO bit in the MDIO user access register (MDIO CPSW_MDIO_USER_ACCESS_REG_k) is cleared. 

2. Write to the GO, WRITE, REGADR, PHYADR, and DATA bits in MDIO CPSW_MDIO_USER_ACCESS_REG_k corresponding to the PHY and PHY register SW wants to write. 

3. The write operation to the PHY is scheduled and completed by the MDIO module. Completion of the write operation can be determined by polling the GO bit in MDIO CPSW_MDIO_USER_ACCESS_REG_k for a 0. 

4. Completion of the operation sets the corresponding USERINTRAW bit (0 or 1) in the MDIO user command complete interrupt register (CPSW_MDIO_USER_INT_RAW_REG) corresponding to MDIO CPSW_MDIO_USER_ACCESS_REG_k used. If interrupts have been enabled on this bit using the MDIO user command complete interrupt mask set register (CPSW_MDIO_USER_INT_MASK_SET_REG), then the bit is also set in the MDIO user command complete interrupt register 

   - (CPSW_MDIO_USER_INT_MASKED_REG) and an interrupt is triggered on the host processor. 

## _**13.2.1.5.5.3 Reading Data From a PHY Register**_ 

The MDIO module includes a user access register (MDIO CPSW_MDIO_USER_ACCESS_REG_k, where k = 0 or 1) to directly access a specified PHY device. To read a PHY register, perform the following: 

1. Check to ensure that the GO bit in the MDIO user access register (CPSW_MDIO_USER_ACCESS_REG_k, where k = 0 or 1) is cleared. 

2. Write to the GO, REGADR, and PHYADR bits in the CPSW_MDIO_USER_ACCESS_REG_k register corresponding to the PHY and PHY register SW wants to read. 

3. The read data value is available in the DATA bit field in MDIO CPSW_MDIO_USER_ACCESS_REG_k register after the module completes the read operation on the serial bus. Completion of the read operation can be determined by polling the GO and ACK bits in CPSW_MDIO_USER_ACCESS_REG_k register. After the GO bit has cleared, the ACK bit is set on a successful read. 

4. Completion of the operation sets the corresponding USERINTRAW bit (0 or 1) in the MDIO user command complete interrupt register (CPSW_MDIO_USER_INT_RAW_REG) corresponding to MDIO CPSW_MDIO_USER_ACCESS_REG_k used. If interrupts have been enabled on this bit using the MDIO user command complete interrupt mask set register (CPSW_MDIO_USER_INT_MASK_SET_REG), then the bit is also set in the MDIO user command complete interrupt register 

   - (CPSW_MDIO_USER_INT_MASKED_REG) and an interrupt is triggered on the host processor. 

1374 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

