#!/bin/bash

# ============================================================================
# SCRIPT DE PRUEBA RÁPIDA - CHATBOT TRANSFORMER (Linux/Mac)
# ============================================================================

echo ""
echo "================================================================================"
echo "    CHATBOT CON TRANSFORMER - PRUEBA RAPIDA"
echo "================================================================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "api.py" ]; then
    echo "ERROR: No se encuentra api.py"
    echo "Asegúrate de ejecutar este script desde el directorio del proyecto"
    exit 1
fi

echo "[1/4] Verificando archivos necesarios..."
echo ""

ARCHIVOS_OK=1

if [ -f "transformer_chatbot.py" ]; then
    echo "[OK] transformer_chatbot.py"
else
    echo "[ERROR] transformer_chatbot.py NO ENCONTRADO"
    ARCHIVOS_OK=0
fi

if [ -f "config_transformer.py" ]; then
    echo "[OK] config_transformer.py"
else
    echo "[ERROR] config_transformer.py NO ENCONTRADO"
    ARCHIVOS_OK=0
fi

if [ -f "entrenar_transformer.py" ]; then
    echo "[OK] entrenar_transformer.py"
else
    echo "[ERROR] entrenar_transformer.py NO ENCONTRADO"
    ARCHIVOS_OK=0
fi

if [ -f "api.py" ]; then
    echo "[OK] api.py"
else
    echo "[ERROR] api.py NO ENCONTRADO"
    ARCHIVOS_OK=0
fi

if [ $ARCHIVOS_OK -eq 0 ]; then
    echo ""
    echo "ERROR: Faltan archivos necesarios"
    exit 1
fi

echo ""
echo "[2/4] Verificando Python..."
echo ""

python3 --version
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Python no está instalado o no está en el PATH"
    echo "Instala Python desde https://www.python.org/"
    exit 1
fi

echo ""
echo "[3/4] Verificando dependencias..."
echo ""

python3 -c "import torch" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] PyTorch no instalado"
    echo "          Ejecuta: pip install torch"
    echo "          El sistema funcionará en modo híbrido"
else
    echo "[OK] PyTorch instalado"
fi

python3 -c "import tensorflow" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] TensorFlow no instalado"
else
    echo "[OK] TensorFlow instalado"
fi

python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[ERROR] FastAPI no instalado"
    echo "        Ejecuta: pip install -r requirements.txt"
    exit 1
else
    echo "[OK] FastAPI instalado"
fi

echo ""
echo "[4/4] Ejecutando prueba del transformer..."
echo ""

python3 << EOF
from transformer_chatbot import PetStoreBotTransformer

bot = PetStoreBotTransformer()
resultado = bot.procesar_mensaje('Hola')

print('\nRESPUESTA DEL BOT:')
print(resultado['respuesta'])
print(f'\nModelo: {resultado["modelo"]}')
print(f'Confianza: {resultado["confianza"]:.0%}')
EOF

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Hubo un problema al ejecutar el chatbot"
    echo "Revisa los errores arriba"
    exit 1
fi

echo ""
echo "================================================================================"
echo "    PRUEBA COMPLETADA EXITOSAMENTE"
echo "================================================================================"
echo ""
echo "Siguientes pasos:"
echo ""
echo "1. Iniciar la API:"
echo "   python3 api.py"
echo ""
echo "2. Probar el chatbot interactivo:"
echo "   python3 demo_transformer.py"
echo ""
echo "3. (Opcional) Entrenar el transformer:"
echo "   python3 entrenar_transformer.py"
echo ""
echo "4. Usar desde el navegador:"
echo "   http://localhost:8000/docs"
echo ""
echo "================================================================================"
echo ""

