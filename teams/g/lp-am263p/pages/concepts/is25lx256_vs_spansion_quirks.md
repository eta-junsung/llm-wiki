---
tags: [concept, flash, xspi, porting, is25lx256, spansion_quirk, bp-3351]
source: [[is25lx256_datasheet]] (ch06.3-6.5, ch08.2, ch11) + Spansion S25Hx/S28Hx 일반 지식
date: 2026-05-22
---

# IS25LX256(ISSI) ↔ Spansion 계열 xSPI Flash — 포팅 시 충돌 포인트

bp-3351 → AM263P 포팅 작업에서 원본 드라이버가 **Spansion(현 Infineon) S25Hx/S28Hx** 계열 Octal xSPI를 가정해 짜여 있다면, **ISSI IS25LX256에 그대로 돌리면 안 된다.** JEDEC xSPI(eXpanded SPI) 표준은 공통이지만 *벤더별 레지스터 맵·opcode·sector arch가 다르다*.

이 페이지는 포팅 시 Spansion 분기를 제거/우회할 때 확인할 차이점 모음.

## 1. UNHYSA(Uniform/Hybrid Sector Architecture) 비트 — **ISSI에는 없다**

Spansion S25Hx/S28Hx는 `CFR3V`(Volatile Configuration Register 3) **bit 3 = UNHYSA** 비트로 sector 구조를 토글:
- `UNHYSA=0` → Hybrid: 어레이 끝(또는 시작)에 작은 boot block(4KB sectors) + 나머지 uniform large sectors
- `UNHYSA=1` → Uniform: 전체가 동일 크기 sector

**IS25LX256은 이 토글 자체가 없다.** 데이터시트 전 챕터에서 `UNHYSA`/`uniform`/`hybrid` 검색 시 sector arch 관련 비트 정의 없음. ISSI 모델은:

- **Sector size 고정** = 128KB uniform (런타임 토글 불가)
- **Ordering 옵션 `B`** (ch11) = factory 64KB sector size — 발주 시점 결정. 칩 받은 시점에 이미 확정.
- "Subsector" 4KB(`20h`)·32KB(`52h`) erase는 *uniform sector 내부의 부분 erase 명령*일 뿐, 별도 boot region이 아님.

**→ 포팅 액션**: 드라이버 init에서 `WRITE_REG(CFR3V, ...)` 또는 `WRAR(CFR3V_addr, UNHYSA_bit)` 호출이 보이면 **전부 제거**. ISSI에서 이 명령은 다른 레지스터/주소를 건드릴 수 있어 **silent corruption** 위험.

## 2. Register 읽기/쓰기 opcode 자체가 다르다

| 동작 | Spansion (S25Hx/S28Hx) | ISSI (IS25LX256) |
|---|---|---|
| Status Register read | `05h` (RDSR1) / `07h` (RDSR2) | `05h` |
| Status Register write | `01h` (WRR/WRSR) | `01h` |
| Any Register read (CFR1V, CFR2V, CFR3V, ...) | **`65h` (RDAR)** + 4-byte address | 레지스터별 전용 opcode: NVCR=`B5h`, VCR=`85h`, Flag Status=`70h`, etc. |
| Any Register write | **`71h` (WRAR)** + 4-byte address | NVCR write=`B1h`, VCR write=`81h`, Clear Flag=`50h`, etc. |

**ISSI 측 0x65/0x71 거동** (`raw/IS25LX256/ch08_device_operation.md` §8.1, line 9):
> "When incorrect command is inserted, the device becomes standby mode and keeps the standby mode until next S# falling edge."

→ ISSI는 0x65/0x71을 디코드하지 않고 standby로 들어간다. 데이터 phase에서 호스트가 읽는 값은 bus default(보통 0xFF) — flag status register는 변하지 않고 에러도 표시되지 않으므로 **silent garbage**.

**→ 포팅 액션**: bp-3351 코드의 `RDAR(65h)` / `WRAR(71h)` 사용 지점 찾아서, ISSI 명령표(ch08_device_operation.md §8.2)에서 **대응 opcode + 주소가 아닌 별도 명령**으로 치환. ISSI는 "any-register" universal accessor가 없고 레지스터별 전용 명령을 쓴다.

## 3. Configuration Register 주소 맵 — 의미 자체가 다르다

Spansion CFR1V/2V/3V/... vs ISSI NVCR/VCR address `00h`~`14h`. 주소가 우연히 겹쳐도 의미가 다르다. ISSI 측 주요 매핑 (ch06.4/6.5):

| Addr | ISSI NVCR/VCR 의미 |
|---|---|
| `00h` | I/O mode (FFh=Extended SPI / E7h=Octal DDR / C7h=Octal DDR w/o DQS / DFh=Extended SPI w/o DQS) |
| `01h` | Dummy cycle configuration (1Fh=Default) — [[xspi_dummy_cycles]] 참조 |
| `02h` | Reserved |
| `03h` | Programmable output drive strength (FFh=50Ω default / FEh=35Ω / FDh=25Ω / FCh=18Ω) |
| `04h` | Reserved |
| ... | ch06.4 Table 6.5 / ch06.5 Table 6.6 전체 참조 |

**→ 포팅 액션**: Spansion 드라이버가 "CFR2V bit 6 = Latency Code"처럼 비트 단위 접근하는 곳을 ISSI 주소·인코딩으로 다시 매핑. 같은 의미 비트가 ISSI에선 다른 주소·다른 인코딩에 있을 수 있다 (e.g. ISSI의 dummy cycle은 5-bit 인코딩이 NVCR/VCR `01h`에 통째로 있음).

## 4. Default I/O 모드 진입 — ordering 옵션으로 결정

| Ordering 옵션 (ch11) | 파워업 후 기본 동작 |
|---|---|
| `J = Standard` | Extended SPI (1S-xy-xy)로 파워업, 호스트가 NVCR `00h`=E7h 써서 Octal DDR로 전환 |
| `O = Default Octal DDR` | 파워업 직후 바로 Octal DDR (8D-8D-8D) — 호스트가 SPI init 없이 곧장 DDR Read 가능 |

Spansion S28Hx는 NVCR(CFR2N) 비트로 같은 선택이지만 ISSI는 발주 옵션. **부품 PN을 먼저 확인**해야 init 코드 결정 가능.

**→ 포팅 액션**: bp-3351의 init이 "전원 인가 → SPI mode 진입 확인 → register write로 DDR 전환" 시퀀스라면 ISSI `J` variant에 그대로 적용 가능. ISSI `O` variant라면 SPI 진입 단계 자체를 스킵해야 함 (이 경우 호스트도 부팅 시점에 Octal DDR로 통신해야 함, AM263P FSS 설정 변경 필요).

## 5. ECC 거동 — 의미·노출 방식 차이

- Spansion S28Hx: ECC는 default ON, 노출은 status 레지스터의 ECC error 비트 + ECC error log register
- ISSI IS25LX256: ECC default ON (16-byte 경계, 1-bit correct / 2-bit detect). ECC event counter가 **VCR address `0Ch` bit[6:3]** 에 노출, 최대 15에서 포화. 별도 ERR# 핀이 있어 *하드웨어 인터럽트로* ECC 이벤트 전파 가능 (ch08.23 ERR# SIGNAL).

**→ 포팅 액션**: Spansion 측 ECC status polling 로직을 ISSI VCR `0Ch` 읽기로 치환. 추가로 AM263P GPIO로 ERR# 핀 모니터링 옵션 검토.

## 6.5. MCU+ SDK 함정 — `Flash_quirkSpansionUNHYSADisable`가 IS25LX256에 자동 매핑됨

**TI MCU+ SDK `flash_nor_ospi.c`의 line 1374-1403** 에 정의된 Spansion 전용 quirk가 **SysConfig에서 IS25LX256을 플래시로 선택했을 때 board init에 자동 매핑된다**. 함수 본체:

```c
int32_t Flash_quirkSpansionUNHYSADisable(Flash_Config *config)
{
    /* Hybrid Sector Disable */
    status = Flash_norOspiRegRead(config, 0x65, 0x00800004, &regData);  // line 1381 — RDAR
    if (status == SystemP_SUCCESS) {
        if ((regData & (1 << 3)) == 0) {
            regData |= (1 << 3);   // UNHYSA bit set
            write = 1U;
        }
    }
    if (write) {
        status = Flash_norOspiRegWrite(config, 0x71, 0x04, regData);    // line 1399 — WRAR
    }
}
```

### ISSI에서 실제 무슨 일이 벌어지나

1. `Flash_norOspiRegRead(config, 0x65, 0x00800004, &regData)` — opcode `0x65` (Spansion RDAR)를 4-byte 주소 `0x00800004`와 함께 송신. ISSI는 이 opcode 미정의 → standby (ch08.1). regData에는 bus default(0xFF)가 들어옴.
2. `0xFF & (1<<3) != 0` → UNHYSA bit가 "이미 1이다"라고 잘못 판단 → write 스킵. **이 경우 운 좋게 조용히 no-op로 끝난다.**
3. **그러나** 어떤 이유로든 read가 `0x00` 같은 값을 반환하면 (예: 이전 부팅에서 컨트롤러 register stuck, bus pull-down) → `0x71` (Spansion WRAR) opcode로 주소 `0x04`에 `0x08` 쓰기 시도. ISSI에서 `0x71` 역시 미정의 → standby. 명령은 무시되지만 **WEL(Write Enable Latch) 상태가 의도와 어긋날 수 있다**.

### 더 큰 위험 — protocol 상태 의존성

이 quirk가 호출되는 시점이 **Extended SPI 단계인지 Octal DDR 단계인지에 따라 결과가 다르다**:

- Extended SPI(1S-1S-1S) 시점 호출이면: ISSI는 `0x65`를 8-bit opcode로 디코드 → 미정의 → standby. 위 시나리오.
- Octal DDR(8D-8D-8D) 시점 호출이면: 컨트롤러가 `0x65`를 8 cycle DDR command phase로 전송 → ISSI는 octal에서도 미정의 opcode로 판단 → standby. **단, dummy/address phase 길이가 Spansion 가정으로 맞춰져 있어 bus timing이 무너지면 다음 명령까지 영향 받을 수 있음.**

### 워크어라운드 (우선순위 순)

1. **SysConfig 측 board.syscfg에서 quirk 등록을 수동 제거** — `Flash_DevConfig.flashWriteTimingsCfg`나 quirk fxn pointer를 `NULL`로 override. 위치는 SysConfig 생성 output (`ti_board_config.c` 또는 `flash_open` 호출 전 hook).
2. **드라이버 fork** — SDK를 fork해서 ISSI 디스크립터에서 이 quirk를 제거. 갱신 부담 있음.
3. **무시** — 실제 정상 동작 케이스(read가 0xFF 리턴)에서는 silent no-op이므로 production 위험 낮음. 단 진단/디버깅 시 0x65/0x71 트래픽이 logic analyzer에 잡히면 혼란.

**권장**: 1번. SysConfig에서 IS25LX256 디바이스 디스크립터의 quirk 연결을 끊고, 필요한 ISSI 전용 init은 `Flash_quirkXxx` 형태로 별도 함수 추가.

### 검증 방법

- AM263P xSPI 핀에 logic analyzer 부착 후 `Flash_norOspiOpen` 진입~종료 구간에서 `0x65` 또는 `0x71` opcode 송신 여부 캡처.
- 보이면 → quirk가 매핑된 상태. SysConfig output(`ti_board_config.c` / `ti_board_open_close.c` 등)에서 `Flash_quirkSpansionUNHYSADisable` 참조 grep.
- IS25LX256 JSON 디스크립터(`raw/mcupsdk/source/sysconfig/board/.meta/flash/IS25LX256.json`) 자체에는 quirk 필드 없음 — quirk 매핑은 별도 SysConfig codegen 단계에서 일어남.

→ 참조: [[mcupsdk_flash_nor_ospi]]의 라인 인덱스 1374-1403 항목. 디스크립터 자체는 정상임이 검증됨 → [[sbl_app_flash_handoff]] §진단 트리.

## 6. Hardware reset / In-Band reset

- ISSI: 전용 `RESET#` 핀 + 명령 기반 reset (`66h`+`99h` 연속 = Software Reset, ch08.3). **In-Band Reset** 별도 시퀀스 존재 (ch08.27).
- Spansion S28Hx: 비슷한 `66h`+`99h` 시퀀스 지원. 호환성 양호.

**→ 포팅 액션**: reset 시퀀스 자체는 큰 변경 없을 가능성. 단, ISSI RESET# 핀 풀업이 내장(internal pull-up, ch02 PIN DESCRIPTIONS)이라 외부 풀업 회로 다를 수 있음 — 하드웨어 설계 확인.

## 포팅 체크리스트

bp-3351 드라이버에서 다음 패턴 발견 시 ISSI 전용 분기 작성:

- [ ] `RDAR(65h)` / `WRAR(71h)` 호출 → ISSI 전용 RDxxx/WRxxx opcode로 치환
- [ ] **SysConfig가 IS25LX256에 `Flash_quirkSpansionUNHYSADisable` 자동 매핑하는지 확인** → 매핑되어 있으면 board.syscfg에서 끊기 (§6.5)
- [ ] `CFR3V` UNHYSA 관련 init 분기 → 통째로 제거 (ISSI는 ordering 옵션)
- [ ] Latency/Dummy code 인코딩 차이 → [[xspi_dummy_cycles]] 표로 재계산
- [ ] Sector size 가정 (4KB hybrid boot 전제?) → 128KB uniform + subsector 4KB/32KB로 재설계
- [ ] Octal DDR 진입 시점 가정 → ordering 옵션 `J` vs `O` 따라 분기
- [ ] ECC error 폴링 위치 → VCR `0Ch` bit[6:3] 또는 ERR# 핀
- [ ] AM263P FSS 컨트롤러의 dummy/latency·DDR/SDR 설정과 칩 측 NVCR/VCR을 **양방향**으로 정렬

## 함께 보기

- 데이터시트 인덱스: [[is25lx256_datasheet]]
- Dummy cycle 권장값: [[xspi_dummy_cycles]]
- 명령표 원본: `raw/IS25LX256/ch08_device_operation.md` §8.2
- 레지스터 맵 원본: `raw/IS25LX256/ch06_registers.md` (§6.4 NVCR, §6.5 VCR)
- Ordering 디코딩: `raw/IS25LX256/ch11_ordering.md`
