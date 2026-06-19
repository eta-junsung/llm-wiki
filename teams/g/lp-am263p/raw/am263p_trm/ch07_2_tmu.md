<!-- AM263P TRM | 7.2 Trigonometric Math Unit (TMU) | 원본 p.355-364 | pymupdf4llm text+tables, images omitted -->

www.ti.com 

_Processors and Accelerators_ 

**Table 7-25. CCM-R5F Polarity Control Register (CCMPOLCNTRL) Field Descriptions (continued)** 

|**Bit**|**Field**|**Value**|**Description**|
|---|---|---|---|
|3-0|POLARITYINVERT||Polarity Inversion. This value is used to invert one of the 8 output compare signals from the<br>CPU1 to the CCM-R5F. Inverting any one signal will lead to compare error by the CPU Output<br>Compare Diagnostic.<br>**Read in User and Privileged mode. Write in Privileged mode only.**|



## **7.1.3.14 R5FSS Selftest Logic** 

Additional details regarding the R5FSS Selftest Logic are described in the Self-Test Controller (STC) chapter. 

## **7.2 Trigonometric Math Unit (TMU)** 

**7.2.1 TMU Introduction** ............................................................................................................................................... 356 **7.2.2 TMU Functional Operation** ................................................................................................................................ 356 **7.2.3 TMU Data Format** ............................................................................................................................................... 362 **7.2.4 TMU Operation Pseudo Code** ........................................................................................................................... 364 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

355 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## _**7.2.1 TMU Introduction**_ 

This device integrates a TMU (Trigonometric Math Unit) module for accelerating many commonly used math functions in control applications such as SIN, COS, ATAN. The TMU module is connected to the TCMA interface of the R5 CPU as shown in Figure 1 . The TMU registers show up as TCM memory mapped registers for the R5 CPU at address 0x0006 0000. Figure 7-15 describes the connections between the TMU accelerator and the R5 CPU. 

**==> picture [501 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
0x0008 0000<br>TCMB I/F TCMB<br>RAM<br>0x0000 0000<br>R5 CPU<br>TCMA<br>RAM<br>TCMA I/F<br>TMU<br>Interrupt to<br>Adapter TMU<br>VIM<br>Bridge<br>0x0006 0000<br>ROM I/F from<br>VBUSP<br>**----- End of picture text -----**<br>


**Figure 7-15. TMU Connection to R5 CPU** 

## **7.2.1.1 TMU Supported Features** 

TMU has the following features: 

- Supports 8 critical trigonometric operations that are useful in a control loop algorithm 

   - SIN 

   - COS 

   - ATAN 

   - QUAD 

   - IEXP (base of 2) 

   - LOG (base of 2) 

- Supports 8 result registers for taking advantage of the pipelined architecture of TMU 

- TCM Adaptation logic for seamless integration of TMU to the R5 TCM port in a software transparent manner 

- Single cycle Context save and restore operation 

## **Note** 

The CLA TMU integrated in AM26x platforms has limitations with single cycle context save. AM26x hardware does **not** support nesting interrupts, and therefore full TMU context save/restore is not feasible in the MCU PLUS SDK. **Only** single context save/restore is possible on AM26x devices. The C28x TMU hardware supports nested interrupts, and therefore supports full TMU context save/restore. 

- Supports Underflow and Overflow interrupts to show mathematical operation errors 

## _**7.2.2 TMU Functional Operation**_ 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

356 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.2.2.1 Supported Functions** 

Mathematical operations supported by the TMU accelerator are shown in Table 7-26 below. 

**Table 7-26. TMU Operations** 

|**Operation**|**Description**|**Number of Inputs**|**Number of**<br>**Outputs**|**Equivalent Operation**|**Effective R5 Cycles**<br>**for Operation**(1)|
|---|---|---|---|---|---|
|SINPUF32|Returns the SINE of<br>Input value|1 : OP1|1|Sin(OP1*2pi rad)<br>OP1: -1.0 to 1.0||
|COSPUF32|Returns the COSINE<br>of Input value|1 : OP1|1|Cos(OP1*2pi rad)<br>OP1: -1.0 to 1.0||
|ATANPUF32|Returns the ATAN of<br>Input value|1 : OP1|1|Atan(OP1) rad/2pi<br>OP1: -1.0 to 1.0<br>Result: -0.125 to 0.125||
|QUADF32|Returns the quadrant<br>value and the ratio of<br>X and Y inputs which<br>are provided as per<br>unit values.|2<br>OP1 : X<br>OP2 : Y|2|Operation to assist in calculating<br>Atan<br>Result 1 : Ratio of X & Y<br>Result 2: Quadrant (X,Y)<br>SeeFigure 7-16||
|IEXP2F32|Returns inverse<br>exponent of input<br>value|1 : OP1|1|1/(2^OP1)||
|LOG2F32|Returns base-2<br>logarithm of input<br>value|1: OP1|1|Log2(OP1)||



(1) The cycles indicated in the table are the theoretical best cases for single operation with a barrier instruction inserted between operand write and result readout. The actual cycles may vary based on the ARM CPU Load/Store state. 

For pipelined operation, the effective cycle count for multiple operations will be significantly less than sum of cycle count of individual operation. 

**==> picture [500 x 267] intentionally omitted <==**

**Figure 7-16. QUADF32 Operation** 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

357 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.2.2.2 TMU Module Block diagram** 

Figure 7-17 Shows the TMU Block diagram. 

**==> picture [329 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
LVF  Operand Registers OP1<br>Interrupt<br>UVF  Operand Registers OP2<br>Interrupt Trignometric Data Path<br>ROM Parity Error<br>ROM<br>Tables<br>TMU Register<br>Interface<br>Result  Register R0 Context Save Result<br>Register CSAVE_R0<br>Context Save Result<br>Operand Registers R1<br>Register CSAVE_R1<br>Context Save Result<br>Operand Registers R7 Register CSAVE_R7<br>INT and Misc Registers<br>TMU<br>**----- End of picture text -----**<br>


**Figure 7-17. TMU Block Diagram** 

## **7.2.2.3 Operand Registers (OP1 and OP2)** 

The TMU contains two operand registers: OP1 and OP2. The operand registers contain the input operand value for a TMU operation. One or two operand registers are used depending on which operation is being performed. The supported operations and number of operand registers are listed below. Further details can be found in Table 7-26. 

- **One (OP1 ONLY):** 

   - SINPUF32 (SINE) 

   - COSPUF32 (COSINE) 

   - ATANPUF32 (ARCTAN) 

   - IEXP2F32 (Inverse exponent) 

   - LOG2F32 (Base-2 logarithm) 

- **Two (OP1 and OP2):** 

   - QUADF32 

Trigonometric operation is triggered upon writing to the OP1 register . In the case of an operation requiring two operands, OP2 should be updated first, followed by OP1 to trigger operation. For example, if performing the QUADF32 operation, input _Y_ should be written to OP2, followed by writing input _X_ to OP1, which will then trigger the operation. 

The OP1 register does not need to maintain its input value for more than a CPU cycle due to the pipeline implementation of TMU operations. OP1 can also be overwritten in consecutive cycles with a new operand value for the same or different operation. 

## **7.2.2.4 Result Registers** 

TMU operations can take 8 to 10 Effective R5 CPU cycles to return the result after OP1 is written to trigger an operation. There are 8 result registers in the TMU accelerator. The result is written to one of the result registers when the operation completes. The TMU accelerator contains multiple result registers to serve as temporary storage to enable back to back operations in consecutive cycles and keep the results separate. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

358 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

Listed below are the supported operations and number of result registers needed per operation: 

- **One Result Register:** 

   - SINPUF32 (SINE) 

   - COSPUF32 (COSINE) 

   - ATANPUF32 (ARCTAN) 

   - IEXP2F32 (Inverse exponent) 

   - LOG2F32 (Base-2 logarithm) 

- **Two Result Registers:** 

   - QUADF32 

## _**7.2.2.4.1 Operand and Result Register Structure**_ 

The Operand Register 1 (OP1) is a single physical register aliased at multiple address locations. The choice of the alias address determines which operation needs to be triggered by the application and which result register is holding the final result. Table 7-27 shows the Register Aliases for each OP1 register and the TMU Address offset. 

**Table 7-27. Operand 1 Register** 

|**OP1 Register Alias**|**TMU Address offset**<br>**(From 0x0006 0000)**|**Description**|
|---|---|---|
|SINPUF32_R0|0x40|•<br>Operand corresponds to SINE Operation<br>•<br>Result stored in Result Register R0|
|SINPUF32_R1|0x48|•<br>Operand corresponds to SINE Operation<br>•<br>Result stored in Result Register R1|
|….|||
|SINPUF32_R7|0x78|•<br>Operand corresponds to SINE Operation<br>•<br>Result stored in Result Register R7|
|COSPUF32_R0 – R7|0x80 – 0xB8|•<br>Operand corresponds to COSINE<br>Operation<br>•<br>Result stored in corresponding result<br>register (R0-R7)|
|ATANPUF32_R0-R7|||
|….|||
|….|||



The Operand Register 2 (OP2) is a single physical register. It is used only for operations needing two operands. 

**Table 7-28. Operand 2 Register** 

|**OP2 Register**|**TMU Address offset**<br>**(From 0x0006 0000)**|**Description**|
|---|---|---|
|QUADF32_OP2|0x240|Operand 2 Corresponding to QUADF32<br>operation.<br>Y : QUADF32|



There are 8 result registers in the TMU for storing the result of TMU operations. 

**Table 7-29. Result Registers** 

|**Result Register**|**TMU Address offset**<br>**(From 0x0006 0000)**|**Description**|
|---|---|---|
|RESULT_R0-R7|0x280 – 0x2B8|Result Registers R0 to R7|



SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 359 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.2.2.5 Initiating TMU Operation** 

To initiate a TMU operation, the Operand value needs to be written to a suitable aliased OP1 register. 

|0x40<br>0x44<br>0x48<br>….<br>0x80<br>0x84<br>Operand<br>Register OP1<br>address<br>SIN<br>SIN<br>SIN<br>SIN<br>COS<br>COS<br>R0<br>R1<br>R2<br>...<br>R0<br>R1<br>Opera<br>�on<br>Result reg|0x40<br>0x44<br>0x48<br>….<br>0x80<br>0x84<br>Operand<br>Register OP1<br>address<br>SIN<br>SIN<br>SIN<br>SIN<br>COS<br>COS<br>R0<br>R1<br>R2<br>...<br>R0<br>R1<br>Opera<br>�on<br>Result reg|0x40<br>0x44<br>0x48<br>….<br>0x80<br>0x84<br>Operand<br>Register OP1<br>address<br>SIN<br>SIN<br>SIN<br>SIN<br>COS<br>COS<br>R0<br>R1<br>R2<br>...<br>R0<br>R1<br>Opera<br>�on<br>Result reg|
|---|---|---|
|0x40||R0|
|0x44||R1|
|0x48||R2|
|….||...|
|0x80||R0|
|0x84||R1|



**Figure 7-18. OP1 Aliased Address Concept** 

For example, writing to offset 0x40 (SINPUF32_R0) triggers a SIN operation on the value written to OP1, and the result will be stored in the R0 result register. Note that no additional write is necessary to indicate the type of operation and destination result register. 

The OP2 register does not require the same mapping as OP1, as performing a write to OP2 does not initiate a TMU operation. In the case of an operation that requires two operands, upon writing OP1, the value contained in OP2 will be taken as the second operand. Because of this, OP2 needs to be written first followed by OP1 for the operation to return a valid value. 

In the case of an operation that requires two result registers, the OP1 address determines the pair of result registers that will contain the result. For example, if OP1 targets R0, then the result will be in R0-R1. If OP1 targets R6, then the result will be present in R6-R7 registers. The result should be read out in the same order as R0 followed by R1 , R1 followed by R2, etc. 

## _**7.2.2.5.1 Interrupt Context Save and Restore**_ 

The TMU accelerator result registers support a _context save and restore_ feature so that the TMU hardware can be used in an ISR (Interrupt Service Routine) context while simultaneously being used in the Main function. 

## **Note** 

The CLA TMU integrated in AM26x platforms has limitations with single cycle context save. AM26x hardware does **not** support nesting interrupts, and therefore full TMU context save/restore is not feasible in the MCU PLUS SDK. **Only** single context save/restore is possible on AM26x devices. The C28x TMU hardware supports nested interrupts, and therefore supports full TMU context save/restore. 

When an interrupt occurs, and thus triggers an ISR, the context save can be initiated by writing ‘1’ to the CONTEXT_SAVE.SAVE bit. TMU result registers are saved to CSAVE_<*> registers. A context save will happen only after all operations initiated before writing to CONTEXT_SAVE.SAVE are complete. This is to ensure that the context save happens at the correct point. 

Even though TMU operations are multi-cycle, the TMU operation will have completed by the time a context save operation is initiated in the ISR. Therefore, no additional measure is needed in ISR. After saving the context, the ISR can use the TMU without any restriction. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

360 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

Restoring TMU registers from CSAVE_<*> registers can be initiated by writing ‘1’ to CONTEXT_RESTORE.RESTORE. This is done as the last step of the ISR before returning to the Main function from the ISR. 

## **Note** 

It is not necessary to use the context save/restore feature if different result registers are used by Main and ISR functions. 

## _**7.2.2.5.2 Pipelined Operation**_ 

As indicated in Table 7-26, each TMU operation will take some cycles to complete and update the Result register. However, the TMU accelerator can trigger a new operation during the result waiting time provided that: 

1. The new operation result register is not same as previous result register. 

2. The new operation operands do not depend on the previous operation result 

Failing to adhere to the above conditions will lead to the TMU result values being stale. 

## **7.2.2.6 Result Reading Methods** 

The TMU accelerator is interfaced to the TCMA bus of the R5 CPU. The TMU operation takes some cycles for the result to be available. Once the operation is triggered, the TCM bus is stalled until the valid result is updated in the TMU. This process helps to avoid reading an incorrect result, if the result register is read prematurely. 

## **Note** 

TCM is treated as Normal memory by the R5 CPU. In order to ensure the write is ordered before the read, a Barrier instruction (DNB) is necessary. 

## _**7.2.2.6.1 Single Operation**_ 

A single operation using the TMU can be performed as follows 

1. Write the Operand OP2 to TMU ( _For two operand operation only_ ) 

2. Write the Operand OP1 to TMU 

3. DBN ( _Barrier instruction to Order the Write first and then read_ ) 

4. Read the Result1 from R0-R7 Register 

5. Read the Result2 from R1-R7 Register ( _For two result operation only_ ) 

## **Note** 

For two operand operations, the result registers must be read in the order of Result1 followed by Result2. For example, if Result1 is stored in R6 and Result2 is stored in R7, the registers must be read R6 followed by R7. 

## _**7.2.2.6.2 Pipelined Operation**_ 

A pipelined TMU operation can be performed as follows 

1. Write the Operand OP1 of First Operation 

2. Write the Operand OP1 for second Operation 

3. …Up to total of 8 Operations 

4. DBN ( _Barrier instruction to Order the Write first and then read_ ) 

5. NOP 

6. NOP 

7. NOP 

8. NOP ( _Four NOP’s needed for avoiding hazard and ensure result is valid for pipeline mode_ ) 

9. Read the Result for First Operation 

10. Read the Result for Second Operation 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

361 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

11. …Up to total of 8 Results 

## **7.2.2.7 ROM Parity Error** 

TMU contains a ROM internal to the module for storing the TMU coefficients. 

A parity check logic is implemented on the ROM access path internal to TMU. If a parity error is detected on the interface, an Error event is generated. 

## _**7.2.3 TMU Data Format**_ 

The treatment of the various IEEE floating-point numerical formats for this TMU are the same as the FPU implementation. 

The encoding of the floating-point formats is given in the below table 

**Table 7-30. IEEE 32Bit Single Precision Floating Point Format** 

|**S32**|**E32 (7:0)**|**M32 (22:0)**|**Value (V)**|
|---|---|---|---|
|0|0|0|Zero (V = 0)|
|1|0|0|Negative Zero (V = -0)|
|0 +ive<br>1 -ive|0|Non-zero|De-normalized (V=(-1)S*2(-126)*<br>(0.M))|
|0 +ive<br>1 -ive|1 to 254|0 to 0x7FFFFF|Normal Range (V=(-1)S *2(E-127) *<br>(1.M))|
|0|254|0x7FFFFF|Positive Max (V = +Max)|
|1|254|0x7FFFFF|Negative Max (V = -Max)|
|0|Maximum = 255|0|Positive Infinity (V = +Infinity)|
|1|Maximum = 255|0|Negative Infinity (V = -Infinity)|
|X|Maximum = 255|Non-zero|Not A Number (V = NaN)|



## **7.2.3.1 Negative Zero** 

All TMU operations generate a positive (S==0, E==0, M==0) zero, never a negative zero if the result of the operation is zero. All TMU operations treat negative zero operations as zero. 

## **7.2.3.2 De-Normalized Numbers** 

A de-normalized operand (E==0, M!=0) input is treated as zero (E==0, M==0) by all TMU operations. TMU operations never generate a de-normalized value. 

## **7.2.3.3 Underflow** 

Underflow occurs when an operation generates a value that is too small to represent in the given floating-point format. Under such cases, a zero value is returned. If a TMU operation generates an underflow condition, then the latched underflow flag (LUF) is set to 1. The LUF flag will remain latched until cleared by the user executing an instruction that clears the flag. It also generates an interrupt to the respective R5 Core **R5FSS*_CORE*_INTR_R5SS0_CPU0_TMU_LUF(#210)** 

## **7.2.3.4 Overflow** 

Overflow occurs when an operation generates a value that is too large to represent in the given floatingpoint format. Under such cases, a ± Infinity value is returned. If a TMU operation generates an overflow condition, then the latched overflow flag (LVF) is set to 1. The LVF flag will remain latched until cleared by the user executing an instruction that clears the flag. It also generates an interrupt to the respective R5 Core **R5FSS*_CORE*_INTR_R5SS0_CPU0_TMU_LVF(#209)** 

## **7.2.3.5 Rounding** 

There are various rounding formats supported by the IEEE standard. Rounding has no meaning for TMU operations (rounding is inherent in the implementation). Hence rounding mode is ignored by TMU operations. 

_AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

362 

Copyright © 2025 Texas Instruments Incorporated 

www.ti.com 

_Processors and Accelerators_ 

## **7.2.3.6 Infinity and Not a Number (NaN)** 

An NaN operand (E==maximum, M!=0) input is treated as Infinity (E==maximum, M==0) for all operations. TMU operations will never generate a NaN value but Infinity instead. 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

_AM263P Technical Reference Manual_ 

363 

Copyright © 2025 Texas Instruments Incorporated 

_Processors and Accelerators_ 

www.ti.com 

## **7.2.3.7 Common Restrictions** 

For all the TMU instructions, the inputs are conditioned as follows (LVF and LUF are not affected): 

- Negative zero is treated as positive zero 

- Positive or negative denormalized numbers are treated as positive zero 

- Positive and negative NaN are treated as positive and negative infinity, respectively 

## _**7.2.4 TMU Operation Pseudo Code**_ 

This chapter gives a pseudo code example for single operation and pipelined operation of the TMU. 

## **7.2.4.1 Single Operation** 

The pseudo code for single operand (e.g. sinpuf32) is 

1. Mov r0,#oprand1_data _// moving the operand1 to r0_ 

2. Mov r1, #oprand1_address _// moving the operand1 address to r1_ 

3. Mov r2, #resultR0_address _// moving the result R0 address to r2_ 

4. STR r0, [r1] _// write to do a single operand TMU operation_ 

5. DMB _// to ensure strongly ordered read write_ 

6. LDR r3, [r2] _// moving the TMU result R0 data into r3_ 

The pseudo code for two operands with two result (e.g. QUADF32) is 

1. Mov r0,#oprand1_data // moving the operand1 to r0 

2. Mov r1,#oprand2_data // moving the operand2 to r1 

3. Mov r2,#oprand1_address // moving the operand1 address to r2 

4. Mov r3,#oprand2_address // moving the operand2 address to r3 

5. Mov r4, #resultR0_address // moving the result R0 address to r4 

6. Mov r5, #resultR1_address // moving the result R1 address to r5 

7. STR r1, [r3] // writing TMU operand2 

8. STR r0, [r2] // writing TMU operand1 

9. DMB // to ensure strongly ordered read write 

10. LDR r6, [r4] // moving the TMU result R0 data into r6 

11. LDR r7, [r5] // moving the TMU result R1 data into r7 

## **7.2.4.2 Pipelined Operation** 

The pseudo code for single operand pipeline operation is 

1. Mov r0,#oprand1_data // moving the operand1 to r0 for First Operation 

2. Mov r1, #oprand1_address // moving the operand1 address to r1 for First Operation 

3. Mov r2, #resultR0_address // moving the result R0 address to r2 for First Operation 

4. Mov r3,#oprand1_data // moving the operand1 to r0 for Second Operation 

5. Mov r4, #oprand1_address // moving the operand1 address to r1 for Second Operation 

6. Mov r5, #resultR0_address // moving the result R0 address to r2 for Second Operation 

7. STR r0, [r1] // write to do a single operand TMU operation for First Operation 

8. STR r3, [r4] // write to do a single operand TMU operation for First Operation 

9. DMB // to ensure strongly ordered read write 

10. NOP 

11. NOP 

12. NOP 

13. NOP 

14. LDR r6, [r2] // moving the TMU result R0 data into r6 

15. LDR r7, [r5] // moving the TMU result R1 data into r7 

## **Note** 

TI recommends to read the results in the same order as the operation is performed. 

364 _AM263P Technical Reference Manual_ 

SPRUJ55D – SEPTEMBER 2023 – REVISED JULY 2025 _Submit Document Feedback_ 

Copyright © 2025 Texas Instruments Incorporated 

