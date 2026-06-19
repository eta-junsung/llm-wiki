---
tags: [concept, windows, launcher, bat, powershell, encoding, utf8, python, gui]
source: 8kw-ev-wpt-tx GUI 런처 실증 (2026-06-19, chcp 65001 함정 확인 → ASCII .bat + PS .ps1 UTF-8 BOM 해법)
date: 2026-06-19
---

# Windows GUI 런처 — ASCII .bat 래퍼 + PS .ps1 UTF-8 BOM

> 파이썬 GUI 또는 임의 툴을 HW 엔지니어가 더블클릭으로 실행할 때 쓰는 검증된 패턴. 8kw-ev-wpt-tx `gui.bat` / `launch_gui.ps1`에서 실증(2026-06-19).

---

## 1. 함정: 한글 텍스트 .bat + chcp 65001

**증상**: `.bat` 파일에 한글 주석·echo를 넣고 `chcp 65001`을 추가했는데 더블클릭 시 "is not recognized as an internal or external command" 에러 다발 + 변수 미설정으로 잘못된 분기 진입. 콘솔이 즉시 닫히면 원인이 보이지 않는다.

**원인**: cmd.exe 토크나이저는 `chcp 65001` 이후에도 멀티바이트 UTF-8 바이트 시퀀스를 토큰 경계로 잘못 인식할 수 있다. 한글이 포함된 줄의 멀티바이트 바이트가 토큰을 쪼개 `serial`·`.txt` 같은 부분 문자열이 명령으로 누출되고, `set VAR=값` 줄이 실패해 변수가 미설정 상태가 된다.

**해결**: 루트 `.bat`은 **ASCII 전용 래퍼**로 유지하고 실제 로직·한글 메시지는 `.ps1`에 위임한다.

---

## 2. 검증된 패턴: ASCII .bat 래퍼 → .ps1 위임

```bat
@echo off
REM ASCII only -- no Korean text in this file
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\gui\launch_gui.ps1"
```

- `%~dp0`: `.bat` 파일이 있는 폴더 경로(드라이브 포함). cwd와 무관하게 자기 위치 기준.
- 더블클릭 `.bat`은 cwd = 자기 폴더로 시작.
- `.ps1`에 한글·로직 전부 이동. `.bat`에는 한글을 절대 넣지 않는다.

무터미널(창 즉시 닫힘) 런처가 필요하면 `wscript`로 래핑하거나 `.bat` 속성에서 "창 표시 안 함" 설정. 진단 중에는 터미널 표시 유지 권장.

---

## 3. .ps1은 UTF-8 BOM 필수

PowerShell 5.1(Windows 기본)은 BOM 없는 `.ps1`을 시스템 ANSI(cp949)로 읽어 한글이 깨진다. BOM(EF BB BF) 부여 시 5.1·7 모두 정상 처리.

```python
# BOM 부여 — raw 바이트로 처리 (디코딩·재인코딩 오염 방지)
with open("launch_gui.ps1", "rb") as f:
    content = f.read()
if not content.startswith(b"\xef\xbb\xbf"):
    with open("launch_gui.ps1", "wb") as f:
        f.write(b"\xef\xbb\xbf" + content)
```

편집기(VSCode)에서는 Status Bar 인코딩 클릭 → "UTF-8 with BOM"으로 저장.

---

## 4. Python GUI 더블클릭 런처 레시피 (.ps1 내부)

```powershell
# launch_gui.ps1 (UTF-8 BOM 필수)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $ScriptDir            # cwd 고정 → CSV 로그 등 산출물 위치 결정

# py launcher → python 폴백
$py = if (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { "python" }

# 의존성 자동설치 (requirements.txt 기반)
& $py -m pip install -r "$ScriptDir\requirements.txt" --quiet

# GUI 실행 (콘솔 표시 유지 = 진단 가능)
& $py "$ScriptDir\gui.py"

# 실패 시 일시정지
if ($LASTEXITCODE -ne 0) {
    Write-Host "오류 발생. 아무 키나 누르면 닫힙니다."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
Pop-Location
```

---

## 5. Python 진입점 cwd 독립 설계

`__file__` 기준 절대경로로 내부 자원을 참조하면 런처가 `cd` 없이도 동작한다.

```python
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "config.json")
```

- 산출물(CSV 로그 등)은 cwd에 쓰면, 런처의 `Push-Location $ScriptDir`과 조합해 위치가 예측 가능.
- 내부 자원(설정·asset)은 `BASE_DIR` 기준, 산출물은 cwd 기준으로 분리하면 최소 수정으로 임의 디렉토리에서도 동작.

---

## 함께 보기

- 이 패턴을 쓰는 프로젝트: [[pc_monitor_gui]] (8kw-ev-wpt-tx GUI)
