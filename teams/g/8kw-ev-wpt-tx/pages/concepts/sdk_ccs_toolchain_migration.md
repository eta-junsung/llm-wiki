---
tags: [concept, build, ccs, gmake, sdk, toolchain, sysconfig, ticlang, am263p, 8kw-ev-wpt-tx]
source: 8kw-ev-wpt-tx gmake 빌드 신 스택 마이그레이션 실증 (2026-06-19, ccs2050→ccs2100, SDK 26_00_00_01→06, .out+.mcelf 경고 0 + 실보드 부팅·기능 정상)
date: 2026-06-19
---

# MCU+ SDK / CCS 툴체인 마이그레이션 — 함정 7종

> 각 항목은 독립 교훈 — **증상 → 원인 → 해결·교훈** 순.  
> **실증 범위**: gmake(build/) 신 스택(CCS21/SDK_06/SysConfig1.28/TICLANG5.1.1) 경고 0 + 실보드 부팅·기능 정상(2026-06-19, branch `toolchain-ccs21-sdk2606`).

---

## 1. SDK 릴리스노트 툴체인 표는 하한선 — 상위 스택도 동작한다

**증상**: SDK 26_00_00_06 릴리스노트가 "CCS20.5/SysConfig1.27/TICLANG4.0.4 검증"이라 적혀 있어, CCS21/SysConfig1.28/TICLANG5.1.1로 올리면 안 될 것 같다는 의심이 생긴다.

**원인**: 릴리스노트의 표는 TI가 해당 SDK 출시 시점에 검증한 스택(= 하한선·권장 조합)이다. "이 버전 이하만 된다"는 상한선이 아니다. SDK 패치 업(`.01` → `.06`)은 프로파일 고정 — 툴체인 조합이 바뀌지 않는다.

**해결·교훈**: 신 스택(CCS21/SysConfig1.28/TICLANG5.1.1)으로 올려도 빌드·부팅·기능 정상. 표는 "최소 지원 버전" 기준으로만 읽는다.
- 툴체인 하한 확인: `<SDK>/.metadata/product.json` → `"minToolVersion"` 필드.
- 실제 의존성 표 위치: `<SDK>/docs/api_guide_*/RELEASE_NOTES_<ver>_PAGE.html`.

---

## 2. imports.mak CGT 경로는 하드 `=` — include 이후에 `:=` 재정의

**증상**: `config.mk`에 신버전 TICLANG 경로를 써도 gmake가 여전히 구버전 `ti-cgt-armllvm_4.0.4.LTS`를 가리킨다.

**원인**: SDK `imports.mak`이 `CGT_TI_ARM_CLANG_PATH`를 `=`(하드 대입)로 고정한다. `config.mk`가 `imports.mak` include **이전**에 처리되므로, `config.mk`의 어떤 값도 이미 박힌 `=` 줄을 덮지 못한다.

```makefile
# imports.mak (SDK 내부) — 발췌
CGT_TI_ARM_CLANG_PATH = $(CCS_PATH)/tools/compiler/ti-cgt-armllvm_4.0.4.LTS   # 하드 =
SYSCFG_PATH           ?= ...                                                    # ?= (조건)
```

**해결·교훈**: `include imports.mak` **이후** 줄에서 `:=`로 재정의.

```makefile
include $(MCU_PLUS_SDK_PATH)/imports.mak
# include 이후 재정의 — imports.mak의 = 를 덮어씀
CGT_TI_ARM_CLANG_PATH := C:/ti/ccs2100/ccs/tools/compiler/ti-cgt-armllvm_5.1.1.LTS
SYSCFG_NODE           := C:/ti/ccs2100/ccs/tools/node/node
```

- `SYSCFG_PATH`는 `?=`이므로 include 이전 export도 유효. CGT는 반드시 include 이후.

---

## 3. makefile 상단의 `?=`가 config.mk를 가린다

**증상**: `config.mk`의 `MCU_PLUS_SDK_PATH`를 신 SDK로 고쳤는데 구 SDK가 계속 잡힌다.

**원인**: `build/makefile` 상단에

```makefile
export MCU_PLUS_SDK_PATH ?= C:/ti/mcu_plus_sdk_am263px_26_00_00_01   # ← 먼저 평가
...
-include config.mk                                                      # ← 나중
```

`?=`가 먼저 값을 선점해 `config.mk` 안의 같은 변수 줄은 **죽은 줄**이 된다.

**해결·교훈**: SDK 경로 변경 시 `config.mk` + makefile 상단 `?=` 줄 **둘 다** 수정. 의심되면 `make -p | grep MCU_PLUS_SDK_PATH=`로 실효값 확인.

---

## 4. CCS 번들 SysConfig는 CLI 전용 — SYSCFG_NODE override로 충분

**증상**: gmake `syscfg` 타겟(SysConfig 재생성, `SYSTEM_FLAG=false`)이 번들 SysConfig를 가리킬 때 `nodejs/` 없음 오류로 깨진다.

**원인**: CCS 번들 SysConfig(`ccs2100/.../sysconfig_1.28.0/`)는 `dist/`·`sysconfig_cli.bat`만 포함, `nodejs/`·`nw/`·GUI 런처가 없다. `imports.mak`이 `SYSCFG_NODE`로 독립 Node.js 바이너리를 직접 호출하는데 번들에는 그 경로가 없다.

| 설치 형태 | 경로 예 | 포함 내용 |
|-----------|---------|-----------|
| CCS 번들 | `<CCS>/utils/sysconfig_1.28.0/` | `dist/` + `sysconfig_cli.bat` 만 |
| standalone | `C:/ti/sysconfig_1.28.0/` | `nodejs/`·`nw/`·GUI 런처 포함 |

**해결·교훈**: **standalone SysConfig 별도 설치 불필요** — CCS 공유 node를 override로 지목하면 된다.

```makefile
SYSCFG_NODE := C:/ti/ccs2100/ccs/tools/node/node
```

- 번들과 standalone의 build 번호 차이(예: `+4712` vs `+4696`)는 cosmetic — `@versions` 경고만 발생하며 `minToolVersion` 충족 시 SDK 로드를 거부하지 않는다.

---

## 5. genimage 스크립트가 SDK 버전 간 리네임됨

**증상**: SDK 신버전으로 교체 후 `.mcelf` 생성 룰이 `No such file or directory`로 실패한다.

**원인**: SDK 버전이 오르면 멀티코어 이미지 생성 스크립트가 리네임될 수 있다.

| SDK 계열 | 스크립트명 |
|----------|-----------|
| 26_00_00_0x (구) | `genimage_am26x.py` |
| 26_00_00_06 (신) | `genimage.py` |

인자는 동일. 신 SDK에 `--otfaConfigFile` 인자가 추가됐으나 HS-FS/OTFA 전용 — GP 디바이스는 무관.

**해결·교훈**: **추측으로 이름 고치지 말 것**. `<SDK>/examples/<유사 예제>/ti-arm-clang/makefile`의 `.mcelf` 생성 룰에서 스크립트명과 인자를 그대로 본뜬다. makefile의 `MCELF_IMAGE_GEN` 변수 경로 수정.

---

## 6. CCS workspace 로드 ≠ 프로젝트 툴체인 마이그레이션

**증상**: CCS21로 구 workspace를 열었는데 IDE 빌드 경로·에러가 이상하다. `.cproject`를 열어보면 제품·superClass가 구버전 그대로다.

**원인**: 구 제품이 아직 설치돼 있으면 CCS는 `.cproject` 툴체인 참조를 자동 마이그레이션하지 않는다. workspace 로드 시 일어나는 것은 빌더 attribute 정규화(cosmetic)뿐.

미마이그레이션 지표 — `.cproject` 안에서 확인:

```xml
<extension id="com.ti.MCU-PLUS-SDK-AM263PX.core" ... version="26.0.0.1"/>  <!-- 구 SDK -->
<extension id="org.eclipse.cdt.core.sysconfig"    ... version="1.27.0"/>   <!-- 구 SysConfig -->
<builder superClass="com.ti.ccstudio...2050..."/>                           <!-- 구 CCS -->
```

**해결·교훈**: `.cproject`를 직접 손편집하지 말 것 — superClass 재생성은 IDE가 해야 한다.

1. **Project Properties → CCS Build → Products**: 구 SDK 제거 + 신 SDK 추가, 컴파일러 버전 갱신.
2. 또는 구 제품 제거(Help → About → Installation Details) → CCS 재시작 시 마이그레이션 다이얼로그 자동 표시.

---

## 7. 빌드 툴 셀렉터를 단일 진실 소스에 묶어라

**증상**: 여러 CCS 버전이 설치된 머신에서 GUI 빌드 스크립트가 사전순으로 구버전 CCS를 잡아 "머신마다 다른 툴체인으로 빌드"되는 비결정성이 생긴다.

**원인**: GUI 빌드 스크립트가 gmake.exe 경로를 glob 첫 매치(`glob("C:\ti\ccs*\...")`)로 결정하면 알파벳 순으로 가장 이른 `ccs2050/`가 선택된다. makefile(→ `config.mk`)과 GUI 스크립트가 각자 CCS를 찾으므로 서로 다른 버전을 가리킬 수 있다.

**해결·교훈**: **`config.mk`의 `CCS_PATH`를 파싱해 지목하라** — 빌드(makefile)와 GUI 스크립트가 동일 `config.mk`를 단일 소스로 읽으면 어떤 머신에서든 같은 CCS로 빌드됨.

```python
# run.ps1 / gui 빌드 스크립트 내 예시
ccs_path = parse_config_mk("build/config.mk")["CCS_PATH"]
gmake_exe = f"{ccs_path}/utils/bin/gmake"
```

- 확인: `make -p | grep CCS_PATH=` 와 스크립트가 실제 잡은 경로를 비교.

---

## 함께 보기

- SysConfig 생성물 빌드 의존 모델: [[syscfg_build_model]]
- OSPI standalone 부팅·부트모드 스트랩: [[ospi_boot_mode_strap]]
- OSPI flash 스크립팅 툴링: [[ospi_flash_tooling]]
- 현재 위치·다음 시작점: [[status]]
