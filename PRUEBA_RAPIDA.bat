@echo off
REM ============================================================================
REM SCRIPT DE PRUEBA RÁPIDA - CHATBOT TRANSFORMER
REM ============================================================================

echo.
echo ================================================================================
echo     CHATBOT CON TRANSFORMER - PRUEBA RAPIDA
echo ================================================================================
echo.

REM Verificar que estamos en el directorio correcto
if not exist "api.py" (
    echo ERROR: No se encuentra api.py
    echo Asegurate de ejecutar este script desde el directorio del proyecto
    pause
    exit /b 1
)

echo [1/4] Verificando archivos necesarios...
echo.

set ARCHIVOS_OK=1

if exist "transformer_chatbot.py" (
    echo [OK] transformer_chatbot.py
) else (
    echo [ERROR] transformer_chatbot.py NO ENCONTRADO
    set ARCHIVOS_OK=0
)

if exist "config_transformer.py" (
    echo [OK] config_transformer.py
) else (
    echo [ERROR] config_transformer.py NO ENCONTRADO
    set ARCHIVOS_OK=0
)

if exist "entrenar_transformer.py" (
    echo [OK] entrenar_transformer.py
) else (
    echo [ERROR] entrenar_transformer.py NO ENCONTRADO
    set ARCHIVOS_OK=0
)

if exist "api.py" (
    echo [OK] api.py
) else (
    echo [ERROR] api.py NO ENCONTRADO
    set ARCHIVOS_OK=0
)

if %ARCHIVOS_OK%==0 (
    echo.
    echo ERROR: Faltan archivos necesarios
    pause
    exit /b 1
)

echo.
echo [2/4] Verificando Python...
echo.

python --version
if errorlevel 1 (
    echo.
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Instala Python desde https://www.python.org/
    pause
    exit /b 1
)

echo.
echo [3/4] Verificando dependencias...
echo.

python -c "import torch" 2>nul
if errorlevel 1 (
    echo [WARNING] PyTorch no instalado
    echo           Ejecuta: pip install torch
    echo           El sistema funcionara en modo hibrido
) else (
    echo [OK] PyTorch instalado
)

python -c "import tensorflow" 2>nul
if errorlevel 1 (
    echo [WARNING] TensorFlow no instalado
) else (
    echo [OK] TensorFlow instalado
)

python -c "import fastapi" 2>nul
if errorlevel 1 (
    echo [ERROR] FastAPI no instalado
    echo         Ejecuta: pip install -r requirements.txt
    pause
    exit /b 1
) else (
    echo [OK] FastAPI instalado
)

echo.
echo [4/4] Ejecutando prueba del transformer...
echo.

python -c "from transformer_chatbot import PetStoreBotTransformer; bot = PetStoreBotTransformer(); resultado = bot.procesar_mensaje('Hola'); print('\nRESPUESTA DEL BOT:'); print(resultado['respuesta']); print(f'\nModelo: {resultado[\"modelo\"]}'); print(f'Confianza: {resultado[\"confianza\"]:.0%%}')"

if errorlevel 1 (
    echo.
    echo ERROR: Hubo un problema al ejecutar el chatbot
    echo Revisa los errores arriba
    pause
    exit /b 1
)

echo.
echo ================================================================================
echo     PRUEBA COMPLETADA EXITOSAMENTE
echo ================================================================================
echo.
echo Siguientes pasos:
echo.
echo 1. Iniciar la API:
echo    python api.py
echo.
echo 2. Probar el chatbot interactivo:
echo    python demo_transformer.py
echo.
echo 3. (Opcional) Entrenar el transformer:
echo    python entrenar_transformer.py
echo.
echo 4. Usar desde el navegador:
echo    http://localhost:8000/docs
echo.
echo ================================================================================
echo.

pause

