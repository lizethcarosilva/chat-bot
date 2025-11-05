# 🎓 PASO A PASO: CÓMO ENTRENAR LA RED NEURONAL

## 🎯 HAY 2 TIPOS DE ENTRENAMIENTO

### Tipo 1: Modelos de Predicción (predictor.py)
- Predice tipo de mascota
- Predice asistencia a citas
- ⏱️ Tiempo: 5-10 minutos
- ⭐ Dificultad: Fácil

### Tipo 2: Chatbot LSTM (entrenar_chatbot_veterinario.py)
- Mejora comprensión del lenguaje
- Clasifica intenciones con IA
- ⏱️ Tiempo: 5-10 minutos
- ⭐⭐⭐ Dificultad: Media

---

# 🚀 ENTRENAMIENTO TIPO 1: MODELOS DE PREDICCIÓN

## ✅ PASO 1: Verificar Requisitos

```bash
# Verifica que tienes las librerías
pip list | findstr tensorflow
pip list | findstr scikit-learn
pip list | findstr pandas
```

Si falta alguna:
```bash
pip install tensorflow scikit-learn pandas
```

---

## ✅ PASO 2: Iniciar la API

```bash
python api.py
```

Deberías ver:
```
✅ LISTO - Presiona Ctrl+C para detener
🌐 Servidor corriendo en: http://localhost:8000
```

---

## ✅ PASO 3: Ejecutar Entrenamiento

### Opción A: Desde Swagger UI (Recomendado - Visual)

1. Abre navegador: `http://localhost:8000/docs`

2. Busca la sección **"Administración"** (color naranja)

3. Click en `POST /api/entrenar`

4. Click en **"Try it out"**

5. Click en **"Execute"**

6. Verás respuesta:
```json
{
  "mensaje": "Entrenamiento iniciado en segundo plano",
  "tiempo_estimado": "5-10 minutos",
  "nota": "Verifica el estado con GET /api/predicciones/estado"
}
```

### Opción B: Desde terminal

```bash
curl -X POST http://localhost:8000/api/entrenar
```

---

## ✅ PASO 4: Monitorear el Progreso

**En la consola donde corre la API**, verás el progreso en tiempo real:

```
INFO:__main__:🚀 Iniciando entrenamiento de modelos...
INFO:database:📊 Obteniendo dataset completo para ML...
INFO:database:✓ Dataset obtenido: 2000 registros

INFO:predictor:
================================================================================
🚀 ENTRENANDO MODELO: Tipo de Mascota
================================================================================

INFO:predictor:📊 Preparando datos para predicción de tipo de mascota...
INFO:predictor:✓ Datos preparados: 1600 train, 400 test
INFO:predictor:✓ Clases: 7

INFO:predictor:🏗️  Construyendo modelo de predicción de tipo de mascota...
INFO:predictor:✓ Modelo construido

INFO:predictor:
📈 Entrenando...

Epoch 1/100
50/50 [==============================] - 2s 31ms/step 
  loss: 1.8234 - accuracy: 0.4562 - val_loss: 1.9123 - val_accuracy: 0.4325

Epoch 2/100
50/50 [==============================] - 1s 28ms/step
  loss: 1.5421 - accuracy: 0.5823 - val_loss: 1.6234 - val_accuracy: 0.5625

... (continúa por 100 épocas) ...

Epoch 100/100
50/50 [==============================] - 1s 27ms/step
  loss: 0.2134 - accuracy: 0.9425 - val_loss: 0.2567 - val_accuracy: 0.9125
                           ^^^^^^                         ^^^^^^
                         94.25% train                   91.25% validación ⭐

INFO:predictor:
📊 Evaluando modelo...
INFO:predictor:✓ Precisión en test: 91.25%

INFO:predictor:💾 Guardando modelos...
INFO:predictor:✓ Modelo tipo mascota guardado
INFO:predictor:✓ Encoders y scaler guardados

INFO:__main__:✅ Entrenamiento completado
```

---

## ✅ PASO 5: Verificar que se Guardó

### Método 1: API

Abre en navegador:
```
http://localhost:8000/api/predicciones/estado
```

**Debería retornar:**
```json
{
  "modelos_entrenados": true,
  "archivos_modelos": {
    "predictor_model": true,
    "scaler": true
  },
  "todos_listos": true
}
```

### Método 2: Explorador de Archivos

Navega a la carpeta: `models/`

**Deberías ver:**
```
models/
├── predictor_model.h5      ✅ (1-2 MB)
└── scaler.pkl              ✅ (10-50 KB)
```

---

## ✅ PASO 6: Probar el Modelo Entrenado

### Prueba 1: Predicción de Tipo de Mascota

Desde Swagger UI:

1. Busca: `POST /api/predicciones/tipo-mascota`
2. Click "Try it out"
3. Ingresa:
```json
{
  "dia_semana": 5,
  "hora": 10,
  "mes": 11,
  "service_id": 1
}
```
4. Click "Execute"

**Debería responder:**
```json
{
  "predicciones": [
    {
      "tipo_mascota": "Perro",
      "probabilidad": 0.785
    },
    {
      "tipo_mascota": "Gato",
      "probabilidad": 0.152
    }
  ],
  "tipo_mas_probable": "Perro",
  "confianza": 0.785
}
```

---

# 🧠 ENTRENAMIENTO TIPO 2: CHATBOT LSTM

## ✅ PASO 1: Instalar TensorFlow

```bash
pip install tensorflow
```

Verifica instalación:
```bash
python -c "import tensorflow as tf; print(tf.__version__)"
```

Deberías ver: `2.15.0` (o similar)

---

## ✅ PASO 2: Verificar Archivo de Datos

Verifica que existe: `datos_veterinarios.json`

```bash
# Windows
dir datos_veterinarios.json

# Debería mostrar el archivo
```

**Este archivo contiene:**
- Ejemplos de preguntas (patterns)
- Intenciones (tags)
- Respuestas predefinidas

**Ejemplo:**
```json
{
  "tag": "enfermedades_perros",
  "patterns": [
    "mi perro está enfermo",
    "mi perro tiene fiebre",
    "síntomas de enfermedad en perros"
  ],
  "responses": [
    "Las enfermedades más comunes en perros incluyen..."
  ]
}
```

---

## ✅ PASO 3: Ejecutar Entrenamiento

```bash
python entrenar_chatbot_veterinario.py
```

**Verás en consola:**

```
================================================================================
🧠 ENTRENANDO CHATBOT VETERINARIO CON LSTM
================================================================================

📂 Cargando datos de entrenamiento...
✓ Archivo cargado: datos_veterinarios.json
✓ Total de intenciones: 45
✓ Total de patrones: 782

📊 Preparando datos...
✓ Vocabulario: 1245 palabras únicas
✓ Secuencias tokenizadas
✓ Datos divididos: 625 train, 157 test

🏗️  Construyendo red neuronal LSTM...
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
embedding (Embedding)        (None, 50, 128)          640000    
_________________________________________________________________
bidirectional (Bidirection   (None, 50, 128)          98816     
_________________________________________________________________
dropout (Dropout)            (None, 50, 128)          0         
_________________________________________________________________
bidirectional_1 (Bidirectio  (None, 128)              98816     
_________________________________________________________________
dropout_1 (Dropout)          (None, 128)              0         
_________________________________________________________________
dense (Dense)                (None, 64)               8256      
_________________________________________________________________
dense_1 (Dense)              (None, 45)               2925      
=================================================================
Total params: 848,813
Trainable params: 848,813
Non-trainable params: 0
_________________________________________________________________

📈 Entrenando modelo (50 épocas)...

Epoch 1/50
20/20 [==============================] - 5s 215ms/step
  loss: 3.5234 - accuracy: 0.1245 - val_loss: 3.4123 - val_accuracy: 0.1532

Epoch 2/50
20/20 [==============================] - 4s 198ms/step
  loss: 3.2156 - accuracy: 0.2387 - val_loss: 3.1234 - val_accuracy: 0.2675

... (continúa) ...

Epoch 50/50
20/20 [==============================] - 4s 201ms/step
  loss: 0.1234 - accuracy: 0.9687 - val_loss: 0.2156 - val_accuracy: 0.9235
                           ^^^^^^                         ^^^^^^
                         96.87% train                   92.35% validación ⭐

📊 Evaluando modelo final...
40/40 [==============================] - 1s 18ms/step
✓ Precisión en test: 92.35%
✓ Loss en test: 0.2156

💾 Guardando modelo y componentes...
✓ Modelo guardado: models/chatbot_veterinario.h5
✓ Tokenizer guardado: models/tokenizer_veterinario.pkl
✓ Label encoder guardado: models/label_encoder_veterinario.pkl
✓ Intenciones guardadas: models/intents_veterinario.pkl

================================================================================
✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE
================================================================================

📁 Archivos creados:
   • models/chatbot_veterinario.h5 (3.2 MB)
   • models/tokenizer_veterinario.pkl (156 KB)
   • models/label_encoder_veterinario.pkl (8 KB)
   • models/intents_veterinario.pkl (45 KB)

📊 Resultados:
   • Precisión en entrenamiento: 96.87%
   • Precisión en validación: 92.35%
   • Total de parámetros: 848,813

🎉 El chatbot ahora puede usar la red neuronal LSTM para entender mejor las preguntas.
```

---

## ✅ PASO 4: Reiniciar la API

**IMPORTANTE:** Para que la API cargue los nuevos modelos:

```bash
# 1. Detén la API actual
Ctrl+C

# 2. Reinicia
python api.py
```

**Al iniciar, deberías ver:**
```
INFO:chatbot:✓ Chatbot veterinario cargado
INFO:chatbot:✓ Modelos predictivos de datos cargados
```

---

## ✅ PASO 5: Verificar Archivos Generados

```bash
# Ver archivos en models/
dir models
```

**Deberías ver:**
```
chatbot_veterinario.h5             3,245,678 bytes
tokenizer_veterinario.pkl            156,234 bytes
label_encoder_veterinario.pkl          8,123 bytes
intents_veterinario.pkl               45,678 bytes
```

---

## ✅ PASO 6: Probar el Chatbot Mejorado

Pregunta al chatbot (debería responder mejor):

```
POST http://localhost:8000/api/chat

Body:
{
  "mensaje": "mi perro tiene fiebre",
  "usuario_id": "test"
}
```

**Con modelo entrenado:**
- ✅ Mayor precisión en detección
- ✅ Entiende variaciones y sinónimos
- ✅ Mejor confianza (>0.8)

---

## 📊 INTERPRETANDO LAS MÉTRICAS

### Durante el Entrenamiento:

```
Epoch 50/50
  loss: 0.1234        ← Error en datos de entrenamiento (menor = mejor)
  accuracy: 0.9687    ← 96.87% de aciertos en entrenamiento
  val_loss: 0.2156    ← Error en validación
  val_accuracy: 0.9235 ← 92.35% de aciertos en validación ⭐⭐⭐
```

### ¿Qué es bueno?

| Métrica | Excelente | Bueno | Aceptable | Malo |
|---------|-----------|-------|-----------|------|
| **val_accuracy** | >95% | 85-95% | 70-85% | <70% |
| **val_loss** | <0.2 | 0.2-0.5 | 0.5-1.0 | >1.0 |

### ⚠️ Señales de Alerta:

**Sobreajuste (Overfitting):**
```
accuracy: 0.99    ← Muy alto en entrenamiento
val_accuracy: 0.65 ← Bajo en validación
Diferencia > 15% = SOBREAJUSTE
```

**Solución:**
- Más datos de entrenamiento
- Más Dropout (0.4-0.5)
- Regularización L2

**Subajuste (Underfitting):**
```
accuracy: 0.45     ← Bajo en ambos
val_accuracy: 0.42
```

**Solución:**
- Más épocas de entrenamiento
- Red más compleja (más capas)
- Mejores features

---

## 📂 ARCHIVOS GENERADOS DESPUÉS DEL ENTRENAMIENTO

### Predictor (Tipo 1):

```
models/
├── predictor_model.h5    ← Red neuronal entrenada
│   └─> Contiene:
│       • Arquitectura (capas, neuronas)
│       • Pesos entrenados
│       • Configuración (optimizer, loss)
│
└── scaler.pkl            ← Normalizador y encoders
    └─> Contiene:
        • StandardScaler (normaliza valores)
        • LabelEncoder (tipo_mascota → número)
```

### Chatbot LSTM (Tipo 2):

```
models/
├── chatbot_veterinario.h5            ← Red LSTM
│   └─> Contiene:
│       • Embeddings (5000 palabras × 128 dim)
│       • 2 capas Bidirectional LSTM
│       • Capas Dense
│       • ~849,000 parámetros entrenados
│
├── tokenizer_veterinario.pkl         ← Vocabulario
│   └─> Diccionario: palabra → número
│       • "perro" → 1
│       • "gato" → 2
│       • "fiebre" → 3
│       • ... (5000 palabras)
│
├── label_encoder_veterinario.pkl     ← Intenciones
│   └─> Array de intenciones
│       • [0] = 'saludo'
│       • [1] = 'sintomas'
│       • [2] = 'vacunas'
│       • ... (45 intenciones)
│
└── intents_veterinario.pkl           ← Respuestas
    └─> Diccionario de respuestas
        • {'saludo': ["Hola!", "Bienvenido!"], ...}
```

---

## 🔍 VERIFICAR QUE EL ENTRENAMIENTO FUE EXITOSO

### Check 1: Archivos Existen

```bash
# Windows
dir models\*.h5
dir models\*.pkl

# Deberías ver los archivos listados
```

### Check 2: API Reconoce los Modelos

```
GET http://localhost:8000/api/predicciones/estado
```

**Respuesta esperada:**
```json
{
  "modelos_entrenados": true,   ← ⭐ Debe ser true
  "archivos_modelos": {
    "predictor_model": true,
    "scaler": true
  },
  "todos_listos": true
}
```

### Check 3: Probar Predicción

```
POST http://localhost:8000/api/predicciones/tipo-mascota

Body: {"dia_semana": 5, "hora": 10, "mes": 11, "service_id": 1}
```

**Si está entrenado:** Retorna predicciones  
**Si NO está entrenado:** Error "Los modelos no están entrenados"

---

## ⚙️ CONFIGURACIÓN DEL ENTRENAMIENTO

Los parámetros se definen en `config.py`:

```python
PREDICTOR_CONFIG = {
    'prediction_epochs': 100,      # Número de épocas
    'prediction_batch_size': 32,   # Tamaño del batch
    'test_size': 0.2,              # 20% para validación
    'random_state': 42             # Semilla aleatoria
}

MODEL_CONFIG = {
    'epochs': 50,                  # Épocas para chatbot
    'batch_size': 32,
    'validation_split': 0.2,       # 20% para validación
    'dropout_rate': 0.3            # 30% de dropout
}
```

**Para modificar:**
1. Abre `config.py`
2. Cambia los valores
3. Guarda
4. Re-entrena

---

## 🎯 RESUMEN DEL PROCESO

### Flujo Completo:

```
1. PREPARAR
   └─> Instalar dependencias
   └─> Verificar datos

2. ENTRENAR
   └─> Ejecutar script/endpoint
   └─> Esperar 5-10 minutos
   └─> Ver métricas en consola

3. GUARDAR (Automático)
   └─> Modelo → models/predictor_model.h5
   └─> Auxiliares → models/*.pkl

4. CARGAR (Al iniciar API)
   └─> API lee archivos de models/
   └─> Modelos listos en memoria

5. USAR
   └─> Hacer predicciones
   └─> Sin re-entrenar
```

---

## 📊 MÉTRICAS QUE VERÁS

### Métricas de Entrenamiento:

| Métrica | Qué mide | Objetivo |
|---------|----------|----------|
| **loss** | Error en entrenamiento | Minimizar |
| **accuracy** | Aciertos en entrenamiento | Maximizar (>90%) |
| **val_loss** | Error en validación | Minimizar |
| **val_accuracy** | Aciertos en validación | **Maximizar >85%** ⭐ |

### División de Datos:

```
Dataset Total: 2000 registros
    ├── 80% Entrenamiento (1600)
    │   └─> Para que la red aprenda
    └── 20% Validación (400)
        └─> Para evaluar qué tan bien aprendió
```

---

## ✅ CHECKLIST COMPLETO

### Antes de Entrenar:
- [ ] Python 3.x instalado
- [ ] TensorFlow instalado
- [ ] API corriendo
- [ ] Datos en la base de datos (>100 registros)

### Durante el Entrenamiento:
- [ ] Ver métricas en consola
- [ ] Esperar a que termine (5-10 min)
- [ ] Verificar val_accuracy >85%

### Después del Entrenamiento:
- [ ] Archivos .h5 y .pkl en models/
- [ ] API reconoce modelos (estado = true)
- [ ] Predicciones funcionan sin error
- [ ] Chatbot responde mejor (si entrenaste LSTM)

---

## 🆘 PROBLEMAS COMUNES

### Error: "No module named 'tensorflow'"

```bash
pip install tensorflow
```

### Error: "No hay datos suficientes"

Necesitas al menos 100 registros en la BD.

Verifica:
```bash
curl http://localhost:8000/api/estadisticas
```

### Accuracy muy bajo (<70%)

**Causas:**
- Pocos datos de entrenamiento
- Features no relevantes
- Modelo muy simple

**Solución:**
- Más datos
- Más épocas (150-200)
- Red más compleja

### Entrenamiento muy lento

**Causas:**
- CPU lento
- Dataset muy grande
- Muchas épocas

**Solución:**
- Reduce épocas (50 en lugar de 100)
- Usa batch_size más grande (64)
- Considera usar GPU

---

## 🎉 RESUMEN EJECUTIVO

### Opción 1: Predictor (FÁCIL)
```bash
# Desde Swagger UI
http://localhost:8000/docs → POST /api/entrenar → Execute
```

### Opción 2: Chatbot LSTM (AVANZADO)
```bash
# Desde terminal
python entrenar_chatbot_veterinario.py
```

**Ambos:**
- ⏱️ Tiempo: 5-10 minutos
- 📁 Guardan en: models/
- ✅ Se cargan automáticamente
- 📊 Muestran métricas en consola

---

**¡Sigue estos pasos y tendrás tus modelos entrenados!** 🚀

**Para tu exposición:** Explica que el entrenamiento solo se hace UNA VEZ, luego los modelos se reutilizan. 🎓

