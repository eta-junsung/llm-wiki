_Hardware_ 

www.ti.com 

## **2 Hardware** 

Figure 2-1 shows the overview of the BP-CC3351. 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0004-04.png)


**----- Start of picture text -----**<br>
SMA  Chip Antenna<br>Connector<br>20 Pin  20 Pin<br>BoosterPack™  BoosterPack™<br>Connector (P1) Connector (P2)<br>CC3351<br>Engine Area Dual-Band Wi-Fi 6 and Bluetooth® Low<br> Energy Companion IC<br>Level Shifters<br>LDO<br>Dual Rail<br>Current<br>Measurement<br>USB Micro-B<br>Power Supply option<br>20 pin LP-XDS110<br>Header<br>**----- End of picture text -----**<br>


**Figure 2-1. BP-CC3351 Overview** 

## **2.1 Hardware Features** 

- CC3351 Wi-Fi 6 and Bluetooth Low Energy combo device which can interface with MPU or MCU systems; adding connectivity 

- Two 20-pin stackable connectors (BoosterPack standard) 

- Onboard chip dual-band antenna with on-board SMA/U.FL connector for conducted RF testing 

- Power from on board dual rail (3.3V and 1.8V) LDO using USB or LaunchPad 

- Three level shifters for voltage translation (3.3V to 1.8V) 

- JTAG header pins for SWD interface with XDS110 or LP-XDS110ET 

- Jumper for current measurement on both power supplies (3.3V and 1.8V) with the provision to mount 0.1-ohm (0603) resistors for measurement with voltmeter 

- 32kHz oscillator for lower power evaluation 

4 _SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy BoosterPack™ Plug-In Module_ 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Hardware_ 

## **2.2 Connector and Jumper Descriptions** 

## _**2.2.1 LED Indicators**_ 

Table 2-1 lists the LED descriptions. 

**Table 2-1. LEDs** 

|**Reference**|**Color**|**Usage**|**Comments**|
|---|---|---|---|
|D4|Green|3.3V power indication|On: 3.3V power rail is up.<br>Off: no 3.3V power supplied.|
|D6|Red|1.8V power indication|On: 1.8V power rail is up.<br>Off: no 1.8V power supplied.|
|D5|Yellow|nRESET|The LED indicates the state of the nReset pin. If that<br>LED is on, the device is functional which means the<br>nReset is high.|



Figure 2-2 shows the mentioned LEDs on the board. 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0005-08.png)


**----- Start of picture text -----**<br>
D4<br>D4<br>**----- End of picture text -----**<br>


**Figure 2-2. LEDs D4 and D5** 

## _**2.2.2 Jumper Settings**_ 

Table 2-2 lists the jumper settings. To reference the default jumper configurations, see Figure 2-1. 

**Table 2-2. Jumper Settings** 

|**Reference**|**Usage**|**Comments**|
|---|---|---|
|J1, J2|RF test|SMA connector (J1) or U.FL connector (J2) for conducted testing in<br>the lab. SeeSection 2.5.|
|J6, J8|Power to board|Used to enable power to board for both supplies. SeeSection 2.3.|
|J15, J16|Current measurement|Used to measure power to device only. SeeSection 2.3.1.|
|J7|USB connector|For powering the BoosterPack standalone (not connected to<br>LaunchPad).|
|J10,J11|JTAG connectors|Headers to interface with XDS110 debug probe. SeeSection 2.2.4.|
|J9|20-pin header (J11) 5V power|Enables 5V power supply to come from LP-XDS110.|
|J12, J13, J14|Level shifter host voltage|Set to 3.3V or 1.8V to enable relevant level shifters to translate to<br>correct host voltage level.|
|P1, P2|BoosterPack header|2 × 20 pins each connected to LaunchPad. SeeSection 2.2.3.|



SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

_SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy BoosterPack™ Plug-In Module_ 

5 

Copyright © 2025 Texas Instruments Incorporated 

_Hardware_ 

www.ti.com 

## _**2.2.3 BoosterPack Header Assignment**_ 

The CC3351 BoosterPack has 2 × 20-pin connectors that provide access to many of the CC3351 pins and features. The signal assignment on these 2 × 20-pin connectors is shown in the figure below and described in Table 2-3 and Table 2-4. 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0006-04.png)


**----- Start of picture text -----**<br>
SimpleLink™ CC3351 Dual-band Wi-Fi 6 and Bluetooth [®]<br>Low Energy Booster Pack™<br>Development kit featuring for rapid prototyping featuring the CC3351 companion IC<br>PART NO. BP-CC3351<br>1 GND 20<br>2 SLOW_CLK_IN 19<br>3 UART_TX SDIO_D3 SPI_CS 18<br>4 UART_RX FAST_CLK 17<br>5 nRESET 16<br>6 SDIO_CMD SPI_PICO 15<br>7 SDIO_CLK SDIO_D0 SPI_POCI 14<br>8 IRQ_WL 13<br>9 COEX_GRANT 12<br>10 ANT_SEL IRQ_BLE 11<br>21 5V 40<br>22 GND SDIO_D2 39<br>23 SDIO_D1 38<br>24 UART_CTS 37<br>25 UART_RTS 36<br>26 35<br>27 LOGGER 34<br>28 33<br>29 COEX_REQ 32<br>30 COEX_PRIORITY 31<br>**----- End of picture text -----**<br>


**Figure 2-3. BP-CC3351 BoosterPack Header Pinout** 

**Table 2-3. P1 Header Pin Assignment** 

|**Pin**|**Name (in Schematic)**|**Type/ Direction**|**Description**|
|---|---|---|---|
|P1.1|VCC_MCU_3V3|Input|No functional purpose|
|P1.2|Reserved|N/A|N/A|
|P1.3|UART_TX_3V3 (from<br>CC3351)|Output|The CC3351 UART TX to host for Bluetooth Low<br>Energy host controller interface|
|P1.4|UART_RX_3V3 (to CC3351)|Input|The CC3351 UART RX from host for Bluetooth<br>Low Energy host controller interface|
|P1.5|LP_RESET|Input|Reset line for CC3351 used to enable or disable<br>(active low). Driven by host through LaunchPad<br>pins|
|P1.6|Reserved|N/A|N/A|
|P1.7|SDIO_CLK_3V3|Input|SDIO clock or SPI clock. Must be driven by host|
|P1.8|IRQ_WL_3V3|Output|Interrupt request from CC3351 to host for Wi-Fi<br>activity|
|P1.9|COEX_GRANT_3V3|Output|External coexistence interface - grant (reserved<br>for future use)|



6 _SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy BoosterPack™ Plug-In Module_ 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Hardware_ 

**Table 2-3. P1 Header Pin Assignment (continued)** 

|**Pin**|**Name (in Schematic)**|**Type/ Direction**|**Description**|
|---|---|---|---|
|P1.10|ANT_SEL_3V3|Output|Antenna select control|
|P1.21|VCC_MCU_5V|Power|5V supply to board|
|P1.22|GND|GND|Board ground|
|P1.23|Reserved|N/A|N/A|
|P1.24|Reserved|N/A|N/A|
|P1.25|Reserved|N/A|N/A|
|P1.26|Reserved|N/A|N/A|
|P1.27|Reserved|N/A|N/A|
|P1.28|Reserved|N/A|N/A|
|P1.29|COEX_REQ_3V3|Input|External coexistence interface — request<br>(reserved for future use)|
|P1.30|COEX_PRIORITY_3V3|Input|External coexistence interface — priority<br>(reserved for future use)|



**Table 2-4. P2 Header Pin Assignment** 

|**Pin**|**Name (in schematic)**|**Type/Direction**|**Description**|
|---|---|---|---|
|P2.11|IRQ_BLE_3V3|Output|Interrupt request from CC3351 to host for<br>Bluetooth Low Energy activity|
|P2.12|Reserved|N/A|N/A|
|P2.13|Reserved|N/A|N/A|
|P2.14|SDIO_D0_3V3 (POCI)|Input/Output|SDIO data D0 or SPI POCI|
|P2.15|SDIO_CMD_3V3 (PICO)|Input/Output|SDIO command or SPI PICO|
|P2.16|Reserved|N/A|N/A|
|P2.17|FAST_CLK_REQ_3V3|Output|Fast clock request from CC3351 to host|
|P2.18|SDIO_D3_3V3 (CS)|Input/Output|SDIO data D3 or SPI CS|
|P2.19|SLOW_CLK_IN_3V3|Input|Input for external RTC clock 32.768kHz|
|P2.20|GND|GND|Board ground|
|P2.31|Reserved|N/A|N/A|
|P2.32|Reserved|N/A|N/A|
|P2.33|Reserved|N/A|N/A|
|P2.34|LOGGER_3V3|Output|Tracer from CC3351 (UART TX debug logger)|
|P2.35|Reserved|N/A|N/A|
|P2.36|UART_RTS_3V3 (from<br>CC3351)|Output|UART RTS from CC3351 to host for Bluetooth<br>Low Energy HCI flow control|
|P2.37|UART_CTS_3V3 (to<br>CC3351)|Input|UART CTS to CC3351 from host for Bluetooth<br>Low Energy HCI flow control|
|P2.38|SDIO_D1_3V3|Input/Output|SDIO data D1|
|P2.39|SDIO_D2_3V3|Input/Output|SDIO data D2|
|P2.40|Reserved|N/A|N/A|



SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

_SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy_ 7 _BoosterPack™ Plug-In Module_ 

Copyright © 2025 Texas Instruments Incorporated 

_Hardware_ 

www.ti.com 

## _**2.2.4 JTAG Headers**_ 

The BP-CC3351 was designed with 2 JTAG headers (J10, J11) for SWD interface with the XDS110 debug probe. The signal assignment for these headers is described in the figures and tables below. 

The main JTAG interface for the BP-CC3351 is via the LP-XDS110 (ET) that is connected to the 20-pin header (J11). An XDS110 debug probe can also interface with this board via a 10-pin header (J10), however, this header is not populated with the default kit. 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0008-05.png)


**Figure 2-4. ARM 10-Pin JTAG Connector (J10)** 

**Table 2-5. ARM 10 pin JTAG Connector (J10) Assignment** 

|**Pin**|**Signal Name**|**Description**|
|---|---|---|
|J10.1|VCC_BRD_1V8|1.8V supply for reference voltage to connector|
|J10.2|SWDIO|Serial wire data in/out|
|J10.4|SWCLK|Serial wire clock|
|J10.10|RESET_1V8|nReset (Enable line for CC3351)|
|J10.3, J10.5, J10.7, J10.9|GND|Board ground|




![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0008-09.png)


**----- Start of picture text -----**<br>
GND<br>SWCLK nRESET UART_RX VCC_BRD_5V<br>SWDIO UART_TX VCC_BRD_1V8<br>**----- End of picture text -----**<br>


**Figure 2-5. 20-Pin LP-XDS110ET Connector (J11)** 

8 _SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy BoosterPack™ Plug-In Module_ 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Hardware_ 

**Table 2-6. 20-Pin LP-XDS110ET Connector (J11) Assignment** 

|**Pin**|**Signal Name**|**Description**|
|---|---|---|
|J11.6|SWCLK|Serial wire clock|
|J11.8|SWDIO|Serial wire data in/out|
|J11.10|RESET_1V8|nReset (Enable line for the CC3351)|
|J11.12|UART_TX_1V8|The CC3351 UART TX to host for BLE host controller interface|
|J11.14|UART_RX_1V8|The CC3351 UART RX from host for BLE host controller<br>interface|
|J11.16|VCC_BRD_1V8|1.8V supply for reference voltage to connector|
|J11.18|VCC_BRD_5V|5V supply to BP-CC3351 from LP-XDS110ET|
|J11.1, J11.7, J11.13, J11.19, J11.20|GND|Board ground|



## **2.3 Power** 

The board is designed to accept power from a connected LaunchPad kit. Some LaunchPad kits cannot source the peak current requirements for Wi-Fi, which can be as high as 500mA. In such cases, the USB connector (J7) on the BP-CC3351 can be used to aid in extra current. The use of Schottky diodes make sure that load sharing occurs between the USB connectors on the LaunchPad kit and the BoosterPack module without any board modifications. The jumpers labeled J6 (1.8V) and J8 (3.3V) can be used to measure the total current consumption of the board from the onboard LDO. 

## _**2.3.1 Measure the CC3351 Current Draw**_ 

## **2.3.1.1 Low Current Measurement (LPDS)** 

To measure the current draw of the CC3351 device for both power supplies (3.3V or 1.8V), a jumper labeled J16 (for 3.3V supply) and a jumper labeled J15 (for 1.8V supply) is provided on the board. By removing J16, users can place an ammeter into this path to observe the current on the 3.3V supply. The same process can be used for observing the current on the 1.8V supply with J15. TI recommends this method for measuring the LPDS. 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0009-09.png)


**----- Start of picture text -----**<br>
mA<br>mA<br>**----- End of picture text -----**<br>



![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0009-10.png)


**Figure 2-6. Low Current Measurement** 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

_SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy_ 9 _BoosterPack™ Plug-In Module_ 

Copyright © 2025 Texas Instruments Incorporated 

_Hardware_ 

www.ti.com 

## **2.3.1.2 Active Current Measurement** 

To measure active current in a profile form, TI recommends using a 0.1Ω 1% 0603 resistor on the board, and measuring the differential voltage across the resistor. This can be done using a voltmeter or an oscilloscope for measuring the current profile for both power supplies (3.3V or 1.8V). 

Jumper J15 shunt is removed and a 0.01 resistor is populated in parallel to measure the active currents on the 1.8V supply (see Figure 2-8). Similar operation with J16 and 3.3V supply. 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0010-05.png)


**----- Start of picture text -----**<br>
V<br>V<br>**----- End of picture text -----**<br>



![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0010-06.png)


**Figure 2-7. Active Current Measurement** 

## **2.4 Clocking** 

The BP-CC3351 provides two clock inputs to the CC3351 device: 

- Y1 is a 40MHz crystal for fast clock input. 

- Y2 is a 32.768kHz oscillator for slow clock input. 

If the user desires to provide the own external slow clock through the Slow Clock Input pin (P2.19), then some re-work must be performed. The Y2 oscillator needs to be removed, and populate a 0201-sized, 0-ohm resistor on the R29 pad. See Figure 2-8. The slow clock can also be generated internally to save on BOM. 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0010-13.png)


**----- Start of picture text -----**<br>
Slow Clock<br>R29<br>**----- End of picture text -----**<br>



![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0010-14.png)


**----- Start of picture text -----**<br>
40 MHz XTAL<br>**----- End of picture text -----**<br>


**Figure 2-8. BP-CC3351 Clock Circuitry** 

10 _SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy BoosterPack™ Plug-In Module_ 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Hardware_ 

## **2.5 Performing Conducted Testing** 

As seen in Figure 2-9, the BP-CC3351 has an on-board SMA connector and component antenna. The SMA connector (J1) provides a way for testing conducted measurements. Alternately, a track pad for a U.FL connector (J2) is provided on-board to replace the SMA connector and provide a way to test in the lab using a compatible cable (see Figure 2-9). 

A rework is needed before using the connector on J1/J2. This involves swapping the position of the existing 3.9pF capacitor to lead the transmission line on the desired connection (see Figure 2-9). 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0011-05.png)


**----- Start of picture text -----**<br>
Chip Antenna<br>Mounted<br>3.9pF Capacitor<br>SMA  U.FL<br>Connector Connector<br>Diplexer<br>2.4Ghz BPF<br>**----- End of picture text -----**<br>


**Figure 2-9. RF Path on BP-CC3351** 

## **Note** 

For single band (2.4GHz) usage only, the user can swap the position of the two existing 10pF capacitors to bypass the diplexer. Additionally, the user must add a 50-ohm termination resistor (see Figure 2-10). 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0011-09.png)


**----- Start of picture text -----**<br>
Chip Antenna<br>SMA<br>Connector<br>Mounted<br>10pF Capacitor<br>Mounted<br>50 �  Resistor<br>**----- End of picture text -----**<br>


**Figure 2-10. BP-CC3351 Single-Band Rework** 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

_SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy BoosterPack™ Plug-In Module_ 

11 

Copyright © 2025 Texas Instruments Incorporated 

