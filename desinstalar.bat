@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

:: ============================================================
::  Desinstalador do Curso de Python em 30 Dias — Windows
::  Remove atalhos do Desktop e do Menu Iniciar.
::  NAO remove os arquivos do curso nem o progresso salvo.
:: ============================================================

set "RAIZ=%~dp0"
if "%RAIZ:~-1%"=="\" set "RAIZ=%RAIZ:~0,-1%"

set "DESKTOP=%USERPROFILE%\Desktop"
set "MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "ATALHO_DESKTOP=%DESKTOP%\Curso Python 30 Dias.lnk"
set "ATALHO_MENU=%MENU%\Curso Python 30 Dias.lnk"
set "ICO_DST=%RAIZ%\assets\icon.ico"

echo.
echo ========================================
echo  Desinstalador — Curso Python 30 Dias
echo ========================================
echo.
echo Isso vai remover:
echo   - Atalho do Desktop
echo   - Atalho do Menu Iniciar
echo   - Arquivo de icone temporario (icon.ico)
echo.
echo NAO sera removido:
echo   - Os arquivos do curso (esta pasta)
echo   - Seu progresso salvo em %%USERPROFILE%%\curso_python30\
echo.
set /p "CONFIRMA=Continuar? [s/N] "
if /i not "%CONFIRMA%"=="s" (
    if /i not "%CONFIRMA%"=="sim" (
        echo Desinstalacao cancelada.
        echo.
        pause
        exit /b 0
    )
)

echo.
set "REMOVIDOS=0"

:: --------------------------------------------------------- atalho Desktop
if exist "%ATALHO_DESKTOP%" (
    del /f /q "%ATALHO_DESKTOP%"
    echo ^>^> Removido: %ATALHO_DESKTOP%
    set /a REMOVIDOS+=1
)

:: --------------------------------------------------------- atalho Menu Iniciar
if exist "%ATALHO_MENU%" (
    del /f /q "%ATALHO_MENU%"
    echo ^>^> Removido: %ATALHO_MENU%
    set /a REMOVIDOS+=1
)

:: --------------------------------------------------------- icone temporario
if exist "%ICO_DST%" (
    del /f /q "%ICO_DST%"
    echo ^>^> Removido: %ICO_DST%
    set /a REMOVIDOS+=1
)

:: --------------------------------------------------------- resultado
echo.
if "%REMOVIDOS%"=="0" (
    echo Nada encontrado para remover.
    echo O curso pode nao ter sido instalado com instalar.bat
) else (
    echo ========================================
    echo  %REMOVIDOS% item(s) removido(s). Tudo limpo!
    echo ========================================
    echo.
    echo Seu progresso continua salvo em %%USERPROFILE%%\curso_python30\
    echo Para reinstalar, execute instalar.bat
)
echo.
pause
