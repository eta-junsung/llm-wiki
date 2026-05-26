_Implementation Results_ 

www.ti.com 

## **3 Implementation Results** 

## **3.1 Evaluation Setups** 

The CC3351 BoosterPack can be used in the following configurations: 

- MCU and RTOS evaluation: BP-CC3351 + LaunchPad with the MCU running TCP/IP like the LP-AM243 

- Processor and Linux evaluation: BP-CC3351 + BP-CC33-BBB-ADAPT + BEAGL-BONE-BLACK 

- RF testing with PC tools: BP-CC3351 + LP-XDS110ET 

In addition, the BP-CC3351 can also be wired to any other Linux or RTOS host board running TCP/IP stack. 

## _**3.1.1 MCU and RTOS**_ 

The BP-CC3351 can be used with an MCU running TCP/IP, like the LP-AM243, and can easily integrate with the LaunchPad by stacking the 40-pin headers, as shown in Figure 3-1. 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0012-11.png)


**Figure 3-1. BP-CC3351 with LP-AM243** 

## _**3.1.2 Processor and Linux**_ 

The BP-CC3351 can integrate with a host platform running Linux OS, like the BeagleBoard.org[®] BeagleBone[® ] Black (BBB). The BeagleBone Black is a low-cost, community-supported development platform as shown below. 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0012-15.png)


**Figure 3-2. BeagleBone Black Board** 

12 _SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy BoosterPack™ Plug-In Module_ 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Implementation Results_ 

To interface with the BP-CC3351 with the BeagleBone Black, the user also needs the BP-CC33-BBB-ADAPT to BBB Adapter Board . 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0013-03.png)


**Figure 3-3. Adapter Board for the BeagleBone Black** 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0013-05.png)


**Figure 3-4. BP-CC3351 and BBB with Adapter Board** 

To make sure the BeagleBone Black boots up from the SD card, TI recommends to a remove the 100kohm resistor R68 seen on the bottom of the BBB, and add as R93 on the top of the BBB. Alternatively, press and 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

_SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy_ 13 _BoosterPack™ Plug-In Module_ 

Copyright © 2025 Texas Instruments Incorporated 

_Implementation Results_ 

www.ti.com 

hold the S2 button on the BeagleBone board during power-up if the hardware modifications were not made. (See Figure 3-5 and Figure 3-6.) 

Lastly, adding a right-angle header on the bottom of the BBB to easily connect the FTDI cable is optional. When the adapter board is attached to the BBB, the FTDI cable can get pinched between the BBB and the adapter board, which can cause communication problems. (See Figure 3-6.) 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0014-04.png)


**Figure 3-5. Modified BBB (Bottom View)** 

14 _SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy BoosterPack™ Plug-In Module_ 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Implementation Results_ 


![](teams/g/bp-cc3351/raw/bp_cc3351_evm_ug/img/evm-user-guide-bp_cc3351.pdf-0015-02.png)


**Figure 3-6. Modified BBB (Top View)** 

## _**3.1.3 Standalone RF Testing**_ 

The BP-CC3351 can be used standalone (without a host) to test RF capabilities, using Radio Tool. For more information on the Radio Tool and where to download, refer to Section 3.1.3.1. 

The BP-CC3351 has an onboard SMA connector and component antenna, and a U.FL can be populated on the board, for conducted RF testing using compatible cables (a rework can be needed). For more information, see Section 2.5. 

## **3.1.3.1 Radio Tool BP-CC3351 Hardware Setup** 

Radio Tool is a GUI-based tool for RF evaluation and testing of CC33xx designs during development and certification. The tool enables low-level radio testing capabilities by manually setting the radio into transmit or receive modes. Using the tool requires familiarity and knowledge of radio circuit theory and radio test methods. To perform conducted RF testing on the BP-CC3351, refer to Section 2.5. Note that a rework can be needed. 

The user can download this tool from the Simplelink Wi-Fi Toolbox page on ti.com. 

## **HW Prerequisites** 

- Windows 10 64-bit/ Ubuntu 18 (or higher) 64-bit operation system 

- Latest Chrome web browser 

- Installation of Simplelink Wi-Fi Toolbox 

- BP-CC3351 

- LP-XDS110ET debugger for SWD communication 

The LP-XDS110ET enables direct communication to the CC3351 device via the SWD interface. This allows external tools, such as the Radio Tool, to send commands directly to the device without the use of an embedded host. 

## **Testing with LP-XDS110ET** 

To use the LP-XDS110ET with the BP-CC3351, connect the 20-pin LP-XDS110ET connector (J11) on the BP-CC3351 to the corresponding connector on the LP-XDS110ET (see Figure 3-7). Make sure that the jumper on the LP-XDS110ET (labeled TGT VDD) is in the EXT. configuration, as shown in Figure 3-7. This verifies that the target voltage for the JTAG signals is sourced from the BP-CC3351 (which is 1.8V) instead of the default LP-XDS110 target voltage (3.3V). 

The power supply for the BP-CC3351 comes from the LP-XDS110ET in this case, but there can be usage scenarios where additional current is needed from the USB connection (J7). 

SWAU132A – APRIL 2024 – REVISED AUGUST 2025 _Submit Document Feedback_ 

_SimpleLink™ CC3351 Dual-Band Wi-Fi® 6 and Bluetooth® Low Energy_ 15 _BoosterPack™ Plug-In Module_ 

Copyright © 2025 Texas Instruments Incorporated 

