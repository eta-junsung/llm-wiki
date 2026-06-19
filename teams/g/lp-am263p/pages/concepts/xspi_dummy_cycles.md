---
tags: [concept, xspi, flash, timing, dummy_cycles, is25lx256]
source: [[is25lx256_datasheet]] (ch06 Table 6.7, p.25-27 / ch06.4-6.5 NVCR·VCR)
date: 2026-05-22
---

# IS25LX256 xSPI dummy cycle (Octal DDR 8D-8D-8D)

xSPI Read 명령(`F8h` Fast Read, `FDh`/`FCh` Octal Fast Read, `EEh` 8DTRD, `4Bh` OTP Read, `CDh` DLPRD)의 **dummy cycle 수는 Configuration Register `01h`** 로 설정한다 (NVCR 또는 VCR 양쪽 모두 동일 주소·인코딩). 클럭이 빠를수록 dummy를 늘려야 한다. ECC 활성화 / VCC variant에 따라 보장 한계가 약간 다르다.

## 핵심 표 — Octal DDR (8D-8D-8D) 컬럼

`Table 6.7 Maximum Clock Frequencies` 발췌. 셀 값은 *해당 dummy cycle 수에서 보장되는 **최대 클럭(MHz)***.

| Dummy cycles | IS25WX (200 MHz, ECC **OFF**) | IS25WX (166 MHz, ECC **ON**) | IS25LX (133 MHz, 3.0V) |
|---|---|---|---|
| 3 | **16** | **16** | **16** |
| 4 | **33** | **33** | **33** |
| 5 | 50 | 40 | 40 |
| 6 | 66 | 50 | 50 |
| 7 | 76 | 66 | 66 |
| 8 | 86 | 83 | 83 |
| 9 | 95 | 95 | 95 |
| 10 | 105 | 105 | 105 |
| 11 | 114 | 114 | 114 |
| 12 | 124 | 124 | 124 |
| 13 | 133 | 133 | **133 (max)** |
| 14 | 143 | 143 | — |
| 15 | 152 | 152 | — |
| 16 (Octal DDR default) | 162 | 162 | — |
| 17 | 171 | **166 (max)** | — |
| 18 | 181 | — | — |
| 19 | 191 | — | — |
| ≥20 | **200 (max)** | — | — |

## 자주 묻는 값 (포팅 흔한 케이스)

| 동작 주파수 | 필요 dummy cycles (8D-8D-8D) | 비고 |
|---|---|---|
| **16.67 MHz** | **3** | 표의 "16"은 200/12 MHz 그리드 의미. 세 variant 동일. |
| **33.33 MHz** | **4** | 표의 "33"은 200/6 MHz. 세 variant 동일. |
| 50 MHz | 5 (WX 200/ECC-OFF) / 6 (WX 166 ECC-ON 또는 LX) | ECC ON 또는 LX는 5 cycles에서 40 MHz만 보장 |
| 100 MHz | 9 | 세 variant 동일 |
| 133 MHz | 13 | LX는 13에서 max 도달 |
| 166 MHz | 17 (WX 166/ECC-ON에서 max) / 16 (WX 200/ECC-OFF에서 162 MHz) | |
| 200 MHz | ≥20 | WX 200/ECC-OFF만 가능 |

## 레지스터 인코딩 (NVCR/VCR address `01h`)

| 값 | 의미 |
|---|---|
| `00h` | `1Fh`(Default)와 동일 — 0=disable 아님 |
| `01h` | 1 dummy cycle |
| `02h` | 2 dummy cycles |
| `03h`~`1Dh` | 3~29 dummy cycles |
| `1Eh` | 30 dummy cycles |
| `1Fh` | **Default** (Octal DDR의 경우 16 cycles 권장; FAST READ/OTP READ는 명령별 default. ch06 Note 1 참조) |
| 기타 | Reserved |

## DLPRD dummy = Octal DDR dummy + 2

DLP(Data Learning Pattern) Read 명령(`CDh`)의 dummy는 **Octal DDR dummy 설정 + 2 cycles**. 예:
- Octal DDR dummy = 3 → DLPRD dummy = 5
- Octal DDR dummy = 16 (default) → DLPRD dummy = 18

DQS center-align 학습 시 이 +2를 놓치면 DLP 패턴이 어긋나서 readback 실패한다.

## 함께 보기

- 레지스터 맵 원본: `raw/IS25LX256/ch06_registers.md` (Table 6.5 NVCR, Table 6.6 VCR)
- 명령 인코딩과 default dummy: `raw/IS25LX256/ch08_device_operation.md` §8.2 COMMAND SET SUMMARY
- ECC 영향: ch08 §8.21 ECC OPERATION — ECC ON 시 cell array 읽기 latency가 늘어 위 표가 보수적으로 잡힘
- 포팅 시 Spansion 가정 제거: [[is25lx256_vs_spansion_quirks]]
