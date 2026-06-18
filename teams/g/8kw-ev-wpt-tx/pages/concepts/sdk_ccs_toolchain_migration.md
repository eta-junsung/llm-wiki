---
tags: [concept, build, ccs, gmake, sdk, toolchain, sysconfig, ticlang, am263p, 8kw-ev-wpt-tx]
source: 8kw-ev-wpt-tx gmake 빌드 신 스택 마이그레이션 실증 (2026-06-18, ccs2050→ccs2100, SDK 26_00_00_01→06, .out+.mcelf 경고 0 성공)
date: 2026-06-18
---

# MCU+ SDK / CCS 툴체인 마이그레이션 — 함정 6종

> **실증 범위**: gmake 빌드가 구 스택(CCS 20.5/SDK 26_00_00_01/SysConfig 1.27.0/TICLANG 4.0.4)에서 신 스택(CCS 21/SDK 26_00_00_06/SysConfig 1.28.0/TICLANG 5.1.1)으로 `.out`+`.mcelf` 경고 0 성공으로 실증(1~5). 6은 `.cproject` diff로 확인. 실보드 부팅 검증은 미완 — 툴체인 메커니즘과 무관.

---

## 1. "새 SDK = 새 툴체인" 아님 — 실제 요구 버전 읽는 법

**SDK가 요구하는 툴체인은 SDK 안에 명시돼 있다. CCS가 번들하는 툴체인 버전과 무관하다.**

- **정본**: `<SDK>/docs/api_guide_*/RELEASE_NOTES_<ver>_PAGE.html` 내 의존성 표.  
  예) `26_00_00_06` 요구 = CCS 20.5.0 / SysConfig 1.27.0+4565 / TICLANG 4.0.4.LTS — CCS 21이 번들하는 더 새 버전이 아니다.
- **SysConfig 하한**: `<SDK>/.metadata/product.json` → `"minToolVersion"` 필드(예: `"1.27.0"`). 이 값 미만 SysConfig 사용 시 SDK가 로드 거부.
- **패치 업은 같은 프로파일**: SDK `.01` → `.06`은 버그픽스 패치; 툴체인 프로파일(CCS/SysConfig/TICLANG 조합)은 동일하다.
- **결론**: 마이그레이션 범위를 잡을 때 이 표와 `minToolVersion`을 먼저 읽는다. CCS 버전 업이 툴체인 업그레이드를 강제하지 않는다.

---

## 2. `imports.mak`의 CGT 경로는 하드 `=` — override는 include 이후에

```makefile
# <SDK>/imports.mak
:43  CGT_TI_ARM_CLANG_PATH=$(CCS_PATH)/tools/compiler/ti-cgt-armllvm_4.0.4.LTS   # 하드 =
:45  # 2차 fallback: $(TOOLS_PATH)/ti-cgt-armllvm_4.0.4.LTS
:49  SYSCFG_PATH ?= $(TOOLS_PATH)/sysconfig_1.27.0                                # ?= (fallback)
```

- CGT 경로는 `?=`(조건 대입)이 아니라 `=`(무조건 대입). `config.mk`가 `imports.mak` **include 이전**에 들어가므로 `config.mk`의 어떤 값도 이미 박힌 `=`를 덮지 못한다.
- 2차 fallback 경로(`$(TOOLS_PATH)/ti-cgt-armllvm_*`)는 이름 패턴이 standalone 설치(`ti_cgt_arm_llvm_*` — 언더스코어 위치 다름)와 불일치해 자동 매칭이 깨질 수 있다.
- **SDK가 고정한 버전이 아닌 다른 컴파일러를 쓰려면**: 프로젝트 `makefile`에서 `include imports.mak` **이후**에 재정의.

```makefile
include $(SDK_PATH)/imports.mak
# imports.mak의 = 덮어쓰기 — := 로 강제
CGT_TI_ARM_CLANG_PATH := C:/ti/ccs2100/ccs/tools/compiler/ti-cgt-armllvm_5.1.1.LTS
```

- `SYSCFG_PATH`는 `?=`이므로 `include` 이전 export도 유효하지만, CGT는 그렇지 않다.

---

## 3. `export VAR ?=`가 `config.mk` include보다 앞에 있으면 `config.mk`를 가린다

gmake의 `?=`는 "값이 아직 없으면 대입"이다. makefile 상단에

```makefile
export MCU_PLUS_SDK_PATH ?= C:/ti/mcu_plus_sdk_am263px_26_00_00_01   # ← 이 줄이
...
include config.mk                                                       # ← 이 줄보다 앞에 있으면
```

`?=`가 먼저 값을 선점해, `config.mk` 안의 같은 변수 줄은 **죽은 줄**이 된다. `config.mk`만 고쳐도 실효가 없다.

- **SDK 경로를 변경할 때는** `config.mk` 수정 + makefile 상단 해당 줄도 함께 수정.
- `?=` vs `=` vs `:=` 의미 차이와 include 순서를 확인해야 어느 줄이 실효 줄인지 알 수 있다. 의심스러우면 `make -p | grep VAR=`로 실측.

---

## 4. CCS 번들 SysConfig는 CLI 전용 — gmake는 standalone 필요

| 설치 형태 | 경로 예 | 포함 내용 |
|-----------|---------|-----------|
| CCS 번들 | `<CCS>/utils/sysconfig_1.27.0/` | `dist/` + `sysconfig_cli.bat` 만. `nodejs/`·`nw/` **없음** |
| standalone | `C:/ti/sysconfig_1.27.0/` | `nodejs/`·`nw/`·GUI 런처 포함 **풀 설치** |

번들은 `<CCS>/tools/node/node.exe`(공유 Node.js)에 의존해 CLI를 구동한다. `nodejs/`가 없으므로 `SYSCFG_NODE` 변수가 가리킬 독립 바이너리가 없다.

**gmake는 `imports.mak:51`에서 `SYSCFG_NODE`를 직접 요구한다.** `SYSCFG_PATH`를 번들로 가리키면 `syscfg` 타겟(`SYSTEM_FLAG=false` 재생성 경로)이 깨진다.

해법 두 가지:

```makefile
# (a) SYSCFG_PATH를 standalone으로 (권장)
SYSCFG_PATH := C:/ti/sysconfig_1.27.0

# (b) SYSCFG_NODE를 CCS 공유 node로 override (번들 sysconfig_cli.bat 경유)
SYSCFG_NODE := C:/ti/ccs2100/ccs/tools/node/node.exe
```

- 번들과 standalone의 build 번호 차이(예: `+4712` vs `+4696`)는 cosmetic — `@versions` 불일치 경고만 발생하며, `minToolVersion` 충족 시 SDK가 로드를 거부하지 않는다.

---

## 5. SDK 버전 간 `genimage` 스크립트 리네임 — 정답은 SDK example makefile

SDK 버전이 오르면 멀티코어 이미지 생성 스크립트가 리네임될 수 있다.

| SDK 계열 | 스크립트명 |
|----------|-----------|
| 26_00_00_0x (구) | `genimage_am26x.py` |
| 26_00_00_06 (신) | `genimage.py` |
인자는 동일.

`makefile`의 `MCELF_IMAGE_GEN` 경로가 `No such file or directory`로 깨지면:

1. **추측 금지** — 이름 규칙을 짐작해 고치지 않는다.
2. `<SDK>/examples/<유사 예제>/ti-arm-clang/makefile`을 열어 `.mcelf` 생성 룰에서 **스크립트명과 인자를 그대로 본뜬다**.

> ⚠️ SDK 26_00_00_06 레퍼런스 예제의 `.mcelf` 생성 룰에는 HS-FS/OTFA 전용 분기가 있다 — **GP(General Purpose) 디바이스에는 무관**, 해당 분기 없이 단순 `genimage.py` 호출로 충분.

---

## 6. CCS workspace 로드 ≠ 프로젝트 툴체인 마이그레이션

구 workspace를 새 CCS로 열어도, **구 제품(구 SDK·구 CCS 버전)이 아직 설치돼 있으면** CCS는 `.cproject`의 툴체인 참조를 자동 마이그레이션하지 않는다. 빌더 attribute 정규화(`name`/`keepEnvironmentInBuildfile` 같은 메타데이터)만 일어난다.

**미마이그레이션 지표 — `.cproject` 안에서 확인:**

```xml
<!-- PRODUCTS 라인: 구 버전 그대로면 미마이그레이션 -->
<extension id="com.ti.MCU-PLUS-SDK-AM263PX.core" point="..." version="26.0.0.1"/>
<extension id="org.eclipse.cdt.core.sysconfig" point="..." version="1.27.0"/>

<!-- superClass: 구 CCS/컴파일러 정의 그대로면 미마이그레이션 -->
<builder superClass="com.ti.ccstudio.buildDefinition.gcc.exe.release.2050..."/>
```

**실제 마이그레이션 경로:**

1. **Project Properties → CCS Build → Products**: 구 SDK 제거 + 신 SDK 추가, 컴파일러 버전 갱신.
2. **구 제품 제거**: CCS Help → About → Installation Details에서 구 SDK/CCS 버전 제거 → 재시작 시 CCS 마이그레이션 다이얼로그 자동 표시.

> **CCS workspace 첫 로드는 "로드됨"이지 "마이그레이션됨"이 아니다.** IDE 빌드 결과물(에러 메시지·경로)이 이상하면 `.cproject` PRODUCTS와 superClass를 먼저 확인한다.

---

## 함께 보기

- SysConfig 생성물 빌드 의존 모델 (CCS managed build vs gmake, `SYSTEM_FLAG`, stub emit 함정): [[syscfg_build_model]]
- OSPI standalone 부팅·부트모드 스트랩: [[ospi_boot_mode_strap]]
- 현재 위치·다음 시작점: [[status]]
