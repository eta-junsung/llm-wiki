---
tags: [source, ti_mcupsdk, ospi, flash, driver, am263p]
source: TexasInstruments/mcupsdk-core@next:source/board/flash/ospi/flash_nor_ospi.c
date: 2026-05-22
---

# TI MCU+ SDK — `flash_nor_ospi.c`

TI MCU+ SDK가 제공하는 **OSPI NOR flash 공용 드라이버**. AM263P/AM243X/AM261X/AM64X 등 TI SoC 공통. IS25LX256 등 디바이스별 특성은 별도 `Flash_DevConfig` 디스크립터로 주입.

## 출처

- 리포: `https://github.com/TexasInstruments/mcupsdk-core`
- 브랜치: `next`
- 파일: `source/board/flash/ospi/flash_nor_ospi.c`
- 받은 시점 commit: `05d3aebbc8d6e9ef7fdb69a646c68676146ff5b5` (2025-05-30 author / 2025-10-16 committer)
- 크기: 1429 lines, 48 KB
- 라이선스: BSD 3-Clause
- raw 사본: `teams/g/lp-am263p/raw/mcupsdk/source/board/flash/ospi/flash_nor_ospi.c`

## 역할

- `Flash_Fxns` ops 테이블 (open/close/read/write/erase/eraseSector/reset/enableDacMode/disableDacMode) 구현
- Protocol switching: 1S_1S_1S, 1S_1S_2S, 1S_1S_4S, 1S_1S_8S, 4S_4S_4S, 4S_4D_4D, 8S_8S_8S, **8D_8D_8D**
- 3B/4B addressing 전환, QE/OE bit, 444/888 mode entry 시퀀스
- Dummy cycle / mode bit 컨트롤러+chip 양쪽 설정
- PHY tuning (attack vector + DDR tune)
- Read capture delay sweep
- Vendor quirks (예: `Flash_quirkSpansionUNHYSADisable` line 1374)

## 라인 인덱스 (자주 참조하는 진입점)

| 라인 | 심볼 | 역할 |
|---|---|---|
| 55-66 | `gFlashToSpiProtocolMap[]` | `FLASH_CFG_PROTO_*` → `OSPI_NOR_PROTOCOL(p,a,d,ddr)` 매핑 |
| 68-80 | `gFlashNorOspiFxns` | ops 테이블 |
| 213-252 | `Flash_norOspiSetRegCfg` | 일반화된 register read-modify-write |
| 254-300 | `Flash_norOspiSet4ByteAddrMode` | 4B addr 진입 시퀀스 (5가지 variant) |
| 302-345 | `Flash_norOspiSetAddressBytes` | OSPI 컨트롤러에 3/4B 셋 + chip 측 enable |
| 507-547 | `Flash_norOspiSetModeDummy` | mode bit + dummy clocks (컨트롤러+chip) |
| 549-573 | `Flash_norOspiSetDTR` | DTR(8D) 진입 |
| 575-643 | `Flash_set444mode` | 4-4-4 mode entry (seq 비트별 분기) |
| 645-728 | `Flash_set888mode` | 8-8-8 mode entry (Octal DDR 포함) |
| 730-845 | `Flash_norOspiSetProtocol` | protocol switch 메인 디스패치 (`switch(protocol)`) |
| 1136-1193 | `Flash_norOspiReset` | flash chip reset (clocks 8/10/16, `0xF0`, `0x66+0x99`) |
| 1195-1353 | `Flash_norOspiOpen` | 메인 init 진입점. [[flash_open_sequence]] 참조 |
| 1355-1372 | `Flash_norOspiClose` | PHY disable + flash reset |
| 1374-1403 | `Flash_quirkSpansionUNHYSADisable` | Spansion UNHYSA 분기 — [[is25lx256_vs_spansion_quirks]] 참조 |
| 1405-1428 | `Flash_norOspiDacMode{Enable,Disable}` | DAC(direct-access) mode 토글 |

## 파생 페이지

- [[flash_open_sequence]] — `Flash_norOspiOpen` 종료 시 OSPI 컨트롤러 + flash chip 상태
- [[sbl_app_flash_handoff]] — `skipHwInit` 게이트, SBL → 앱 핸드오프 시 dummy mismatch 위험
- [[is25lx256_vs_spansion_quirks]] (갱신) — `Flash_quirkSpansionUNHYSADisable` 실체 위치 보강

## 아직 안 읽은 것 (후속 ingest 후보)

- `flash_nor_ospi.h` — `FlashCfg_ProtoEnConfig`, `Flash_DevConfig`, `FlashCfg_RegConfig` 구조체 정의 (dummy/protocol 필드 의미)
- IS25LX256용 `Flash_DevConfig` 디스크립터 — 실제 dummy cycle 숫자가 박힌 곳. SBL 예제 board 패키지 혹은 SysConfig output 위치 추적 필요
- `Flash_setQeBit` / `Flash_setOeBit` / `Flash_set444mode` / `Flash_set888mode`의 별도 구현 파일 (이 파일에선 호출만)
- PHY tuning 동작 — `OSPI_phyReadAttackVector` / `OSPI_phyTuneDDR` (OSPI 드라이버 측)
