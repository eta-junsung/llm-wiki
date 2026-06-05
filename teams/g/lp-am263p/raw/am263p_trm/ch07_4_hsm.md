<!-- AM263P TRM | 7.4 Hardware Security Module (HSM) | 원본 p.506-508 | pymupdf4llm text+tables, images omitted -->

_Processors and Accelerators_ 

www.ti.com 

## **7.4 Hardware Security Module (HSM)** 

This chapter describes the Hardware Security Module (HSM) in the device. 

The HSM module is responsible for booting up of the device, enabling the main R5FSS core, defining/controlling overall security of the device based on boot options provided. It also has a DTHE (Data Transform and Hashing Engine) which is a wrapper around crypto IP with some additional capability including CRC and Checksum. 

## **Note** 

The TRM provides a high-level overview of the HSM. For details on specific modules and the HSM Register Map, please request access to the HSM Addendum. 

Table 7-110 provides a list of abbreviations related to hardware security. 

**Table 7-110. Abbreviations** 

|**Abbreviation**|**Description**|
|---|---|
|AES|Advanced Encryption Standard|
|DRBG|Deterministic random bit generator|
|ECC|Elliptic curve cryptography|
|HMAC|Keyed-hashing for message authentication|
|ISC|Initiator-side security control|
|PKA|Public key cryptography|
|RSA|Rivest–Shamir–Adleman cryptosystem|
|SHA|Secure hash algorithm|
|TRNG|True random number generator|



## _**7.4.1 Security Features**_ 

- Hardware Security Module (HSM) supports stacks like Auto SHE 1.1/EVITA 

   - Cortex-M4 based dedicated security controller. 

   - Isolated and secured RAMs. 

   - 

      - Peripherals like Timers, WDT, RTC, Interrupt Controller. 

   - Safety related peripherals like CRC, ESM, PBIST. 

- Secure Boot Support 

   - Hardware-enforced Root-of-Trust (RoT). 

   - Support for two sets of RoT keys. 

   - Authenticated boot support. 

   - Encrypted boot support. 

   - Software Anti-rollback protection. 

- Debug security 

   - Secure device debug only after cryptographic authentication. 

   - Support for permanent debug/JTAG disable. 

- Device ID and Key Management 

   - Unique ID (SoC ID). 

   - Support for OTP Memory (FUSEROM). 

- Extensive Firewall support 

   - System Memory Protection Unit (MPU) - present at various interfaces in the SoC. 

   - Cortex-M4 MPU. 

- Cryptographic Acceleration 

   - Cryptographic cores with DMA Support. 

   - AES - 128/192/256-bit key sizes. 

   - SHA2 - 256/384/512-bit support. 

   - DRBG with pseudo and true random number generator. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

506 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

- PKA (Public key accelerator) to assist in RSA/ECC processing. 

## _**7.4.2 Security Features not Supported**_ 

- Embedded Trace Macrocell (ETM) is not supported. 

- No big endian support. 

- Debug not maintained during warm reset, as warm reset resets all debug logic in HSM, including DAP in Cortex-M4. 

- Monotonic counter 

   - Assumed to be realized using an external non-volatile memory layer (NVMEM). 

## _**7.4.3 Security Device Types**_ 

The HSM architecture supports different "Device Types" controlled by eFuse settings programmed during device manufacturing. Each Device Type offers different capabilities as well as different behaviors in functional operating modes. Depending on this, some security mechanisms are relaxed or enforced. 

The eFuse settings that determine device type are scanned into registers in the Security Manager module within the HSM as part of the power-on-reset process, so these settings are stable before the device starts booting. The device_type_raw is a 16-bit value, with the device type information contained in the lower bytes. For security and redundancy, the upper byte is programmed as the bit-wise inverse of the lower bytes and the Security Manager will set the device type to "BAD" if this condition is not satisfied. Refer to the Security Manager section in the HSM Addendum for more details. 

Table 7-111 describes the device type and associated feature differences for each device type. 

**Table 7-111. Available Device Types** 

|**Device Type**|**eFUSE Field (8 bit)**|**Description**|
|---|---|---|
|HS|0b 1100 1100|High security devices have 2 sub-types that represent the state of HS<br>device.<br>**HS-FS (HS- Field Securable)**: This is the state before “customer keys<br>Revision” and “customer keys count” is blown in the device. In this state,<br>the device forces authentication for HSM Runtime image only. This is the<br>state at which the HS device leaves the TI factory.<br>**HS-SE (HS – Security Enforced)**: This is the state after “customer keys<br>Revision” and “customer keys count” is blown in the device. In the HS-SE<br>device, all security features are enabled. All secrets within the device are<br>fully protected and all of the security goals are fully enforced. The device<br>forces secure booting.|



The different stages in the life cycle of the secure device are shown in Figure 7-97. The enforcement of the secure boot only happens when the customer keys are blown, along with the customer key count and customer key revision fields. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 507 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

**==> picture [512 x 263] intentionally omitted <==**

**Figure 7-97. Device Life Cycle** 

The device transitions from HS-FS to HS-SE only if "Customer Keys Revision" is non-zero AND "Customer Keys Count" is non-zero. Mere writing of the eFuse keys SMPK/BMPK will not change the HS-FS to HS-SE. 

The motivation for HS-FS (Field Securable) device is to allow customers to run unauthenticated code before devices are seeded with customer's keys (SMPK, SMEK, and so forth) and keys are effective. Once the customers injects the booting keys in the device along with non-zero value of "Customer Keys Revision" and "Customer Keys Count" , the device will always force authentication and behave as an HS-SE device. This is a one way change. 

## **Note** 

TI software for High Secure devices provides OTP key writer utility to program customer programmable fields in the Fuse ROM. 

## **Note** 

Only HS-FS and HS-SE are supported any references to GP device type be ignored. 

## **Note** 

Device Requires PORZ for transitioning from HSFS to HSSE state after programming the Customer Keys Count and Customer Keys Revision e-fuse Keys. 

## _**7.4.4 How to Request Access for HSM Addendum**_ 

More details about SoC Security and hardware features supported are described in the HSM Addendum. To request access to the HSM Addendum, please visit the respective web links provided below. 

- Submit Request for AM263Px HSM Addendum here. 

508 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

