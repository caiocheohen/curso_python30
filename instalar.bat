@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

:: ============================================================
::  Instalador do Curso de Python em 30 Dias — Windows
::  Cria atalhos no Desktop e no Menu Iniciar.
:: ============================================================

set "RAIZ=%~dp0"
if "%RAIZ:~-1%"=="\" set "RAIZ=%RAIZ:~0,-1%"

set "PNG_SRC=%RAIZ%\assets\icon.png"
set "ICO_DST=%RAIZ%\assets\icon.ico"
set "DESKTOP=%USERPROFILE%\Desktop"
set "MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "ATALHO_DESKTOP=%DESKTOP%\Curso Python 30 Dias.lnk"
set "ATALHO_MENU=%MENU%\Curso Python 30 Dias.lnk"

echo.
echo ========================================
echo  Instalador — Curso Python 30 Dias
echo ========================================
echo.

:: --------------------------------------------------------- python
echo ^>^> Verificando o Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERRO: Python nao encontrado no PATH.
    echo Baixe em https://www.python.org/downloads/
    echo Marque a opcao "Add Python to PATH" durante a instalacao.
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python -c "import sys; print(sys.version.split()[0])"') do set "VERSAO=%%v"
echo    Python %VERSAO% encontrado.

python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
    echo    AVISO: recomendado Python 3.10 ou superior.
    echo    Alguns exercicios podem nao funcionar nesta versao.
)

:: --------------------------------------------------------- converter PNG para ICO
echo ^>^> Preparando icone...
if exist "%PNG_SRC%" (
    python -c "
import struct
from pathlib import Path

png = Path(r'%PNG_SRC%').read_bytes()
ico = Path(r'%ICO_DST%')

# ICO com PNG embutido (suportado no Windows Vista+)
header   = struct.pack('<HHH', 0, 1, 1)
offset   = 6 + 16
direntry = struct.pack('<BBBBHHII', 0, 0, 0, 0, 1, 32, len(png), offset)
ico.write_bytes(header + direntry + png)
print('   Icone criado.')
" 2>nul
    if not exist "%ICO_DST%" (
        echo    AVISO: nao foi possivel criar o icone — atalho sera criado sem icone personalizado.
        set "ICO_DST=%SystemRoot%\System32\SHELL32.dll,167"
    )
) else (
    echo    AVISO: assets\icon.png nao encontrado.
    set "ICO_DST=%SystemRoot%\System32\SHELL32.dll,167"
)

:: --------------------------------------------------------- pythonw (sem janela de terminal)
for /f "tokens=*" %%p in ('python -c "import sys, os; print(os.path.join(os.path.dirname(sys.executable), 'pythonw.exe'))"') do set "PYTHONW=%%p"
if not exist "%PYTHONW%" set "PYTHONW=python"

:: --------------------------------------------------------- atalho no Desktop
echo ^>^> Criando atalho no Desktop...
powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell;" ^
  "$s  = $ws.CreateShortcut('%ATALHO_DESKTOP%');" ^
  "$s.TargetPath      = '%PYTHONW%';" ^
  "$s.Arguments       = '\"'+'%RAIZ%\curso_web.py'+'\"';" ^
  "$s.WorkingDirectory= '%RAIZ%';" ^
  "$s.Description     = 'Curso de Python em 30 Dias';" ^
  "$s.IconLocation    = '%ICO_DST%';" ^
  "$s.Save();" >nul 2>&1

if exist "%ATALHO_DESKTOP%" (
    echo    Criado: %ATALHO_DESKTOP%
) else (
    echo    AVISO: nao foi possivel criar o atalho no Desktop.
    echo    Clique duplo em curso_web.py para abrir o curso manualmente.
)

:: --------------------------------------------------------- atalho no Menu Iniciar
echo ^>^> Criando atalho no Menu Iniciar...
if not exist "%MENU%" mkdir "%MENU%"
powershell -NoProfile -Command ^
  "$ws = New-Object -ComObject WScript.Shell;" ^
  "$s  = $ws.CreateShortcut('%ATALHO_MENU%');" ^
  "$s.TargetPath      = '%PYTHONW%';" ^
  "$s.Arguments       = '\"'+'%RAIZ%\curso_web.py'+'\"';" ^
  "$s.WorkingDirectory= '%RAIZ%';" ^
  "$s.Description     = 'Curso de Python em 30 Dias';" ^
  "$s.IconLocation    = '%ICO_DST%';" ^
  "$s.Save();" >nul 2>&1

if exist "%ATALHO_MENU%" (
    echo    Criado: %ATALHO_MENU%
) else (
    echo    AVISO: nao foi possivel criar o atalho no Menu Iniciar.
)

:: --------------------------------------------------------- fim
echo.
echo ========================================
echo  Instalacao concluida!
echo ========================================
echo.
echo  Clique duplo no icone do Desktop, ou:
echo  python curso_web.py       (navegador)
echo  python curso.py           (terminal)
echo.
pause
