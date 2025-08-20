@echo off
REM Script de Inicialização do ImageClicker para Windows
REM Este script facilita a execução da aplicação

setlocal enabledelayedexpansion

echo ==========================================
echo 🎯 IMAGECLICKER - INICIALIZADOR WINDOWS
echo ==========================================

REM Verifica se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo 📝 Instale o Python antes de continuar
    echo 🔗 https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Verifica se pip está disponível
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip não encontrado!
    echo 📝 Reinstale o Python com pip incluído
    pause
    exit /b 1
)

echo ✅ pip encontrado

REM Verifica se o diretório images existe
if not exist "images" (
    echo ❌ Diretório 'images' não encontrado!
    pause
    exit /b 1
)

REM Conta arquivos PNG no diretório images
set /a PNG_COUNT=0
for %%f in (images\*.png) do (
    set /a PNG_COUNT+=1
)

if %PNG_COUNT% equ 0 (
    echo ❌ Nenhuma imagem PNG encontrada no diretório 'images'!
    echo 🔧 Configure as imagens seguindo as instruções do README.md
    echo 💡 Adicione screenshots dos elementos que deseja detectar
    pause
    exit /b 1
)

echo ✅ %PNG_COUNT% imagem^(ns^) encontrada^(s^)

REM Verifica dependências Python
echo 🐍 Verificando dependências Python...
python -c "import pyautogui, cv2, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Algumas dependências Python estão faltando
    echo 📝 Instalando dependências...
    
    if exist "requirements.txt" (
        pip install -r requirements.txt
        if !errorlevel! neq 0 (
            echo ❌ Erro ao instalar dependências!
            pause
            exit /b 1
        )
    ) else (
        echo ❌ Arquivo requirements.txt não encontrado!
        pause
        exit /b 1
    )
) else (
    echo ✅ Dependências Python OK
)

REM Avisos de segurança
echo.
echo ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
echo ⚠️  AVISO: Esta ferramenta automatiza cliques visuais!     ⚠️
echo ⚠️  Use APENAS em ambientes controlados!                  ⚠️
echo ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️
echo.
echo 🎮 CONTROLES:
echo    • Ctrl+C = Parar execução
echo    • Mouse no canto superior esquerdo = Parada de emergência
echo.

set /p "response=❓ Deseja continuar? (s/N): "
if /i "!response!"=="s" goto start
if /i "!response!"=="sim" goto start
if /i "!response!"=="y" goto start
if /i "!response!"=="yes" goto start

echo 🛑 Execução cancelada pelo usuário
pause
exit /b 0

:start
echo 🚀 Iniciando ImageClicker...
echo ----------------------------------------
python main.py
pause
