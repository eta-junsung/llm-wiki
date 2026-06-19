_Evaluation Module Overview_ 

www.ti.com 

## **1 Evaluation Module Overview** 

## **1.1 Introduction** 

The CC3351 BoosterPack plug-in module (BP-CC3351) is a test and development board that can easily be connected to a TI LaunchPad or processor boards; thus, enabling rapid software development. 

This user's guide explains the various hardware configurations and features of the BP-CC3351. For more information about the CC335x or CC330x devices, refer to the CC3351 or CC3301 product page. 

## **Note** 

This plug-in module is designed to develop single-band (2.4GHz) CC330x and dual-band (2.4GHz and 5GHz) CC335x devices. 

## **1.2 Kit Contents** 

- BP-CC3351 PCBA 

## **1.3 Regulatory Compliance** 

The CC3351 BoosterPack plug-in module (BP-CC3351) is tested for and found to be in compliance with CE regulations regarding unlicensed intentional radiators. Hereby, Texas Instruments Inc. declares that the radio equipment type BP-CC3351 is in compliance with Directive 2014/53/EU. The BP-CC3351 is found to be RoHS compliant in accordance to EU Directives. The full text of the EU Declaration of Conformity is available. 

## **RF Exposure Information (MPE)** 

This device has been tested and meets applicable limits for Radio Frequency (RF) exposure. To comply with the RF exposure requirements, this module must be installed in a host platform that is intended to be operated in a minimum of 20-cm separation distance to the user. 

## **Frequency Bands and Max Power (e.i.r.p)** 

- Bluetooth LE: **8.58** dBm (EIRP power) 

- Wi-Fi 2.4GHz: **17.92** dBm (EIRP power) 

- Wi-Fi 5Ghz (5150MHz - 5725MHZ) : **17.51** dBm (EIRP power) 

## **Indoor Usage Restrictions** 

The device is restricted to indoor use only when operating in the 5150MHz to 5350MHz frequency range. 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0002-20.png)


||AT|BE|BG|HR|CY|CZ|DK|
|---|---|---|---|---|---|---|---|
||EE|FI|FR|DE|EL|HU|IE|
||IT|LV|LT|LU|MT|NL|PL|
||PT|RO|SK|SI|ES|SE|UK(NI)|



_**This label is not included on product packaging to maintain standard and consistent packaging required by Texas Instruments Incorporated. Users are encouraged to reference the EVM User's Guide for information on device compliance.**_ 

## _**1.3.1 Waste Electrical and Electronic Equipment (WEEE)**_ 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0002-24.png)


## **Waste Electrical and Electronic Equipment (WEEE)** 

This symbol means that according to local laws and regulations your product and/or battery shall be disposed of separately from household waste. When this product reaches its end of life, take it to a collection point designated by local authorities. Proper recycling of your product will protect human health and the environment. 

2 _SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy BoosterPack™ Plug-In Module_ 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

_Evaluation Module Overview_ 

www.ti.com 

## **1.4 Specification** 

The BP-CC3351 is a board designed to enable rapid and easy software and hardware development for the CC335x (2.GHz and 5GHz) and CC330x (2.4GHz) devices. The block diagram for the BP-CC3351 is shown in Figure 1-1. 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0003-04.png)


**----- Start of picture text -----**<br>
Antenna<br>5v LDO Dual Rail  VCC<br>(1.8v & 3.3v)<br>RF<br>UART Filtering<br>SDIO/SPI<br>2 X 20 Pin  nRESET CC3351<br>BoosterPack™   Wi-Fi 6 and Bluetooth® Low Energy  U.FL/SMA<br>Connectors Level Shifters  SLOW_CLK_IN Companion IC<br>(1.8v or 3.3v  IRQ<br>to 1.8v) COEX SWD JTAG<br>LED’s<br>ANT_SEL<br>Logger nRESET<br>3.3v Power<br>40 MHz 32.768 kHz 1.8v Power<br>XTAL Oscillator<br>Optional<br>**----- End of picture text -----**<br>


**Figure 1-1. BP-CC3351 Block Diagram** 

This kit can be used in three configurations: 

1. MCU and RTOS evaluation: BP-CC3351 and LaunchPad with the MCU running TCP or IP like the LPAM243. 

2. Processor and Linux evaluation: BP-CC3351, BP-CC33-BBB-ADAPT, BEAGL-BONE-BLACK. 

3. RF-testing with PC tools: BP-CC3351 and LP-XDS110ET. 

In addition, the BP-CC3351 can also be wired to any other Linux or RTOS host board running TCP, IP stack. 

Refer to Section 3.1 for more information. 

## **1.5 Device Information** 

The purpose of the BP-CC3351 is to showcase the hardware and software capabilities of the CC335x and CC330x devices. The other components on the board are populated for testing and support of these main devices. 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

_SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy_ 3 _BoosterPack™ Plug-In Module_ 

Copyright © 2025 Texas Instruments Incorporated 

