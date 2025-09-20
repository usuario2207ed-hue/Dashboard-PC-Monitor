@echo off
cd /d "%~dp0"

:menu
cls
echo ==============================
echo       Menu do Servidor
echo ==============================
echo 1. Iniciar servidor
echo 2. Parar servidor
echo 3. Sair
echo ==============================
set /p escolha=Escolha uma opcao (1-3): 

if "%escolha%"=="1" goto startServer
if "%escolha%"=="2" goto stopServer
if "%escolha%"=="3" exit
goto menu

:startServer
echo Iniciando servidor PC Monitor...
start "" server.exe
timeout /t 2 >nul

echo Abrindo interface HTML no navegador padrão...
start "" "index.html"

echo Servidor iniciado e interface aberta.
pause
goto menu

:stopServer
echo Tentando parar servidor...
taskkill /im server.exe /f >nul 2>&1
echo Servidor parado.

echo Fechando interface HTML (força fechar todas as janelas do navegador padrão)...
:: OBS: Fechar somente a aba específica não é trivial via BAT
taskkill /im chrome.exe /f >nul 2>&1
taskkill /im msedge.exe /f >nul 2>&1
taskkill /im firefox.exe /f >nul 2>&1

pause
goto menu
