# 📦 DÓNDE SE GUARDA LA INFORMACIÓN DE ENTRENAMIENTO Y VALIDACIÓN

## 📂 ESTRUCTURA DE CARPETAS

Cuando entrenas los modelos de IA, se crean archivos en estas carpetas:

```
chat-bot/
├── models/           ← AQUÍ SE GUARDAN LOS MODELOS ENTRENADOS
│   ├── (archivos .h5 y .pkl)
├── data/             ← AQUÍ SE GUARDAN DATASETS
│   ├── (archivos .csv)
├── exports/          ← AQUÍ SE EXPORTAN RESULTADOS
│   ├── (archivos de análisis)
└── ...
```

---

## 🧠 MODELOS DE PREDICCIÓN (predictor.py)

Cuando ejecutas el entrenamiento de predicción:

```bash
POST http://localhost:8000/api/entrenar
# O desde código
predictor.entrenar_modelo_tipo_mascota(df)
predictor.guardar_modelos()
```

### Archivos que se crean:

```
models/
├── predictor_model.h5        ← Modelo de red neuronal (.h5 = Keras/TensorFlow)
└── scaler.pkl                ← StandardScaler + Label Encoders (.pkl = Pickle)
```

### 1. **predictor_model.h5** (Modelo de Red Neuronal)

**Formato:** HDF5 (Hierarchical Data Format)  
**Tamaño:** ~200 KB - 2 MB (depende de la arquitectura)  
**Contiene:**
- Arquitectura de la red (capas, neuronas)
- Pesos entrenados de todas las neuronas
- Configuración del optimizador
- Función de pérdida

**Qué puede hacer:**
- Predecir tipo de mascota según día/hora/servicio
- Predecir probabilidad de asistencia a citas

**Estructura interna:**
```
predictor_model.h5
├── Model Configuration
│   ├── Layers: Dense(128) → Dropout(0.3) → Dense(64) → ...
│   ├── Activation: ReLU, Softmax
│   └── Optimizer: Adam
├── Weights (Pesos de las neuronas)
│   ├── Layer 1: matriz 4x128 (512 valores)
│   ├── Layer 2: matriz 128x64 (8192 valores)
│   └── ... (miles de parámetros)
└── Training Configuration
    ├── Loss: categorical_crossentropy
    └── Metrics: accuracy
```

### 2. **scaler.pkl** (Normalizador + Codificadores)

**Formato:** Pickle (serialización de objetos Python)  
**Tamaño:** ~10-50 KB  
**Contiene:**
```python
{
    'scaler': StandardScaler(),          # Normalización de features
    'label_encoder_tipo': LabelEncoder()  # Codificación de etiquetas
}
```

**Para qué sirve:**
- **StandardScaler:** Normaliza features antes de predecir
  ```python
  # Transforma valores a media=0, std=1
  [día=5, hora=10, mes=11] → [0.23, -0.45, 0.78]
  ```

- **LabelEncoder:** Convierte tipos de mascota a números
  ```python
  "Perro" → 0
  "Gato" → 1
  "Ave" → 2
  ```

---

## 🤖 MODELOS DEL CHATBOT (entrenar_chatbot_veterinario.py)

Cuando ejecutas:

```bash
python entrenar_chatbot_veterinario.py
```

### Archivos que se crean:

```
models/
├── chatbot_veterinario.h5             ← Red neuronal LSTM
├── tokenizer_veterinario.pkl          ← Vocabulario (palabras → números)
├── label_encoder_veterinario.pkl      ← Intenciones → números
└── intents_veterinario.pkl            ← Diccionario de respuestas
```

### 1. **chatbot_veterinario.h5** (Red LSTM)

**Tamaño:** ~2-5 MB  
**Contiene:**
- Red neuronal LSTM bidireccional
- Embeddings de palabras (5000 palabras x 128 dim)
- Pesos entrenados

**Arquitectura:**
```
Input: Secuencia de palabras [145, 28, 392, 0, 0, ...]
   ↓
Embedding(5000, 128): Convierte números a vectores densos
   ↓
Bidirectional LSTM(64): Procesa secuencia (→ y ←)
   ↓
Dropout(0.3): Regularización
   ↓
Bidirectional LSTM(64): Segunda capa
   ↓
Dense(64, ReLU): Capa densa
   ↓
Dense(num_intenciones, Softmax): Clasificación
   ↓
Output: [0.05, 0.82, 0.03, ...] (probabilidades)
```

### 2. **tokenizer_veterinario.pkl** (Vocabulario)

**Tamaño:** ~50-200 KB  
**Contiene:**
```python
{
    'word_index': {
        'perro': 1,
        'gato': 2,
        'fiebre': 3,
        'vacuna': 4,
        ...
    },
    'num_words': 5000
}
```

**Ejemplo de uso:**
```python
texto = "mi perro tiene fiebre"
tokenizer.texts_to_sequences([texto])
# Resultado: [[45, 1, 28, 3]]
```

### 3. **label_encoder_veterinario.pkl** (Intenciones)

**Tamaño:** ~5-10 KB  
**Contiene:**
```python
{
    'classes_': [
        'saludo',           # 0
        'sintomas',         # 1
        'vacunas',          # 2
        'desparasitacion',  # 3
        ...
    ]
}
```

### 4. **intents_veterinario.pkl** (Respuestas)

**Tamaño:** ~20-100 KB  
**Contiene:**
```python
{
    'saludo': [
        "¡Hola! ¿En qué puedo ayudarte?",
        "¡Bienvenido! Soy tu asistente veterinario"
    ],
    'sintomas': [
        "Los síntomas que describes requieren atención...",
        "Es importante que consultes con un veterinario..."
    ]
}
```

---

## 📊 INFORMACIÓN DE VALIDACIÓN

Durante el entrenamiento, también se genera información de validación que **NO se guarda en disco** (solo se muestra en consola):

### Métricas de Entrenamiento:

```python
# Durante el entrenamiento verás:
Epoch 1/50
loss: 2.1234 - accuracy: 0.45 - val_loss: 2.3456 - val_accuracy: 0.42

Epoch 2/50
loss: 1.8567 - accuracy: 0.62 - val_loss: 1.9234 - val_accuracy: 0.58

...

Epoch 50/50
loss: 0.2134 - accuracy: 0.94 - val_loss: 0.2567 - val_accuracy: 0.91
```

**Qué significa:**
- **loss:** Función de pérdida en datos de entrenamiento (menor = mejor)
- **accuracy:** Precisión en datos de entrenamiento
- **val_loss:** Pérdida en datos de validación (20% separado)
- **val_accuracy:** Precisión en validación (la más importante)

### Si quieres GUARDAR el historial de entrenamiento:

Modifica el código en `predictor.py`:

```python
def entrenar_modelo_tipo_mascota(self, df: pd.DataFrame) -> Dict:
    # ... código de entrenamiento ...
    
    history = self.model_tipo_mascota.fit(...)
    
    # GUARDAR HISTORIAL
    import json
    with open('models/historial_entrenamiento.json', 'w') as f:
        json.dump(history.history, f)
    
    return {
        "accuracy": accuracy,
        "history": history.history  # ← Contiene todo el historial
    }
```

---

## 🗂️ RESUMEN DE ARCHIVOS GENERADOS

### Después de Entrenar Predictor:

```
models/
├── predictor_model.h5           (Red neuronal para predicciones)
└── scaler.pkl                   (Normalizador + encoders)
```

**Comando:**
```python
POST http://localhost:8000/api/entrenar
```

**Tiempo:** 5-10 minutos  
**Tamaño total:** ~300 KB - 2 MB

---

### Después de Entrenar Chatbot:

```
models/
├── chatbot_veterinario.h5           (Red LSTM del chatbot)
├── tokenizer_veterinario.pkl        (Vocabulario)
├── label_encoder_veterinario.pkl    (Intenciones)
└── intents_veterinario.pkl          (Respuestas)
```

**Comando:**
```bash
python entrenar_chatbot_veterinario.py
```

**Tiempo:** 5-10 minutos  
**Tamaño total:** ~2-7 MB

---

### TODOS los modelos juntos:

```
models/
├── predictor_model.h5              # Predicción de tipos
├── scaler.pkl                      # Normalizador
├── chatbot_veterinario.h5          # LSTM del chatbot
├── tokenizer_veterinario.pkl       # Vocabulario
├── label_encoder_veterinario.pkl   # Encoder de intenciones
└── intents_veterinario.pkl         # Diccionario de respuestas
```

---

## 📈 MÉTRICAS DE VALIDACIÓN (En Consola)

### Lo que verás durante el entrenamiento:

```
🚀 ENTRENANDO MODELO: Tipo de Mascota
================================================================================
📊 Preparando datos para predicción de tipo de mascota...
✓ Datos preparados: 1600 train, 400 test
✓ Clases: 7

🏗️  Construyendo modelo de predicción de tipo de mascota...
✓ Modelo construido

📈 Entrenando...
Epoch 1/100
50/50 [==============================] - 2s 31ms/step
  loss: 1.8234 
  accuracy: 0.4562 
  val_loss: 1.9123 
  val_accuracy: 0.4325

Epoch 2/100
50/50 [==============================] - 1s 28ms/step
  loss: 1.5421 
  accuracy: 0.5823 
  val_loss: 1.6234 
  val_accuracy: 0.5625

...

Epoch 100/100
50/50 [==============================] - 1s 27ms/step
  loss: 0.2134 
  accuracy: 0.9425 ← Precisión en entrenamiento: 94.25%
  val_loss: 0.2567 
  val_accuracy: 0.9125 ← Precisión en validación: 91.25% ⭐

📊 Evaluando modelo...
✓ Precisión en test: 91.25%

💾 Guardando modelos...
✓ Modelo tipo mascota guardado
✓ Encoders y scaler guardados
```

---

## 💾 ¿QUÉ CONTIENE CADA ARCHIVO?

### .h5 (Modelo de Keras/TensorFlow)

**Formato:** HDF5 (binario)  
**Visualizar:** No es legible como texto  
**Contiene:**
```
/ (raíz)
├── model_weights/
│   ├── dense_1/kernel    (matriz de pesos)
│   ├── dense_1/bias      (vector de bias)
│   ├── lstm_1/kernel     (pesos LSTM)
│   └── ...
├── model_config/
│   └── config.json       (arquitectura)
└── training_config/
    └── optimizer, loss, metrics
```

**Cómo ver información:**
```python
from tensorflow.keras.models import load_model

model = load_model('models/predictor_model.h5')
model.summary()  # Muestra arquitectura
```

### .pkl (Pickle - Objetos Python)

**Formato:** Pickle (binario)  
**Contiene:** Objetos Python serializados  
**Cómo ver:**
```python
import pickle

with open('models/scaler.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data.keys())  # dict_keys(['scaler', 'label_encoder_tipo'])
```

---

## 📊 INFORMACIÓN DE VALIDACIÓN (NO se guarda por defecto)

### Curvas de Aprendizaje

Durante el entrenamiento se genera el objeto `history`:

```python
history = model.fit(X_train, y_train, validation_split=0.2, epochs=100)

# history.history contiene:
{
    'loss': [2.1, 1.8, 1.5, ..., 0.21],           # Pérdida por época (train)
    'accuracy': [0.45, 0.58, 0.67, ..., 0.94],    # Precisión por época (train)
    'val_loss': [2.3, 1.9, 1.6, ..., 0.25],       # Pérdida (validation)
    'val_accuracy': [0.42, 0.56, 0.65, ..., 0.91] # Precisión (validation) ⭐
}
```

### Para guardar las métricas de validación:

```python
# Agrega esto en predictor.py después del entrenamiento:
import json

# Guardar historial
with open('models/historial_entrenamiento.json', 'w') as f:
    json.dump(history.history, f, indent=2)

# Guardar reporte de evaluación
with open('models/reporte_evaluacion.txt', 'w') as f:
    f.write(f"Precisión en test: {accuracy:.4f}\n")
    f.write(f"Total de épocas: {len(history.history['loss'])}\n")
    f.write(f"Loss final: {history.history['loss'][-1]:.4f}\n")
```

### Para graficar curvas de aprendizaje:

```python
import matplotlib.pyplot as plt

# Cargar historial
with open('models/historial_entrenamiento.json') as f:
    history = json.load(f)

# Graficar
plt.plot(history['accuracy'], label='Entrenamiento')
plt.plot(history['val_accuracy'], label='Validación')
plt.xlabel('Época')
plt.ylabel('Precisión')
plt.legend()
plt.savefig('exports/curvas_aprendizaje.png')
```

---

## 🔍 CÓMO VERIFICAR QUE SE GUARDÓ CORRECTAMENTE

### Opción 1: Desde código Python

```python
import os

# Verificar archivos del predictor
print("Predictor:")
print(f"  Modelo: {os.path.exists('models/predictor_model.h5')}")
print(f"  Scaler: {os.path.exists('models/scaler.pkl')}")

# Verificar archivos del chatbot
print("\nChatbot:")
print(f"  Modelo: {os.path.exists('models/chatbot_veterinario.h5')}")
print(f"  Tokenizer: {os.path.exists('models/tokenizer_veterinario.pkl')}")
print(f"  Encoder: {os.path.exists('models/label_encoder_veterinario.pkl')}")
print(f"  Intents: {os.path.exists('models/intents_veterinario.pkl')}")
```

### Opción 2: Desde la API

```bash
# Verificar estado de modelos
GET http://localhost:8000/api/predicciones/estado
```

**Respuesta:**
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

### Opción 3: Desde terminal

```bash
# Windows
dir models

# Linux/Mac
ls -lh models/
```

**Deberías ver:**
```
predictor_model.h5              1.2 MB
scaler.pkl                     45 KB
chatbot_veterinario.h5         3.5 MB
tokenizer_veterinario.pkl     120 KB
...
```

---

## 📥 CÓMO SE CARGAN LOS MODELOS

Cuando inicias la API, automáticamente intenta cargar los modelos:

```python
# En api.py (línea 45)
try:
    predictor.cargar_modelos()  # ← Carga modelos entrenados
    logger.info("✅ Modelos cargados exitosamente")
except:
    logger.warning("⚠️ Modelos no encontrados. Entrena primero.")
```

**Proceso de carga:**
```python
# predictor.py - cargar_modelos()
def cargar_modelos(self):
    # 1. Cargar modelo de red neuronal
    self.model_tipo_mascota = load_model('models/predictor_model.h5')
    
    # 2. Cargar scaler y encoders
    with open('models/scaler.pkl', 'rb') as f:
        data = pickle.load(f)
        self.scaler = data['scaler']
        self.label_encoder_tipo = data['label_encoder_tipo']
    
    # 3. Marcar como entrenado
    self.trained = True
```

---

## 🎯 RESUMEN PARA TU EXPOSICIÓN

### Tipos de Modelos:

| Modelo | Archivo | Tamaño | Algoritmo |
|--------|---------|--------|-----------|
| **Predictor** | predictor_model.h5 | ~1-2 MB | Red Neuronal Densa |
| **Chatbot** | chatbot_veterinario.h5 | ~3-5 MB | LSTM Bidireccional |
| **Clustering** | (No se guarda)* | - | Agglomerative |

*El clustering se ejecuta en tiempo real sobre los datos actuales

### Datos Auxiliares:

| Archivo | Qué guarda | Tamaño |
|---------|------------|--------|
| scaler.pkl | Normalizador (StandardScaler) | ~10 KB |
| tokenizer_veterinario.pkl | Vocabulario (5000 palabras) | ~100 KB |
| label_encoder_veterinario.pkl | Codificador de intenciones | ~5 KB |
| intents_veterinario.pkl | Respuestas predefinidas | ~50 KB |

---

## 📝 PARA INCLUIR EN TU EXPOSICIÓN

### Slide: "Persistencia de Modelos"

```
Modelos Entrenados se Guardan en:
  📁 models/
     ├── predictor_model.h5 (1.2 MB)
     ├── chatbot_veterinario.h5 (3.5 MB)
     └── archivos auxiliares (.pkl)

Formato: HDF5 para redes neuronales
         Pickle para objetos Python

Ventajas:
  ✅ Entrenar una vez, usar siempre
  ✅ No re-entrenar en cada inicio
  ✅ Portabilidad entre servidores
```

### Slide: "Información de Validación"

```
Métricas de Validación (durante entrenamiento):

  • Accuracy en Test: 91.25%
  • Loss: 0.2567
  • Silhouette Score: 0.587 (clustering)
  
División de Datos:
  • 80% Entrenamiento
  • 20% Validación
  
Early Stopping: Evita sobreajuste
```

---

## ✅ CHECKLIST

- [ ] Carpeta `models/` existe (se crea automáticamente)
- [ ] Después de entrenar, archivos .h5 y .pkl aparecen
- [ ] API carga modelos al iniciar
- [ ] Endpoint `/api/predicciones/estado` retorna `true`

---

## 🎉 RESUMEN

**Dónde se guarda:**
- 📁 `models/` - Todos los modelos entrenados
- Formato: .h5 (Keras) y .pkl (Pickle)

**Qué se guarda:**
- Arquitectura de red
- Pesos entrenados
- Normalizadores y encoders
- Vocabulario (chatbot)

**Validación:**
- Se muestra en consola durante entrenamiento
- No se guarda por defecto (puedes modificar para guardarlo)

---

**Para tu exposición:** Explica que los modelos se guardan en formato estándar (HDF5) para reutilizarlos sin re-entrenar. 🚀

