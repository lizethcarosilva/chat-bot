# 🎓 CÓMO ENTRENAR LA RED NEURONAL DEL CHATBOT

## 🎯 Objetivo

Entrenar el modelo LSTM (Long Short-Term Memory) para que el chatbot sea **MÁS INTELIGENTE** y reconozca automáticamente las intenciones del usuario.

---

## ✅ Estado Actual

### Sistema Actual (Sin Entrenar):
- ✅ Funciona con **patrones de palabras clave**
- ✅ Detecta ~30 intenciones diferentes
- ⚠️ Debe coincidir exactamente con las palabras clave
- ⚠️ No entiende sinónimos o variaciones complejas

### Sistema Con IA Entrenada:
- ✅ **Comprende contexto y sinónimos**
- ✅ Reconoce patrones complejos
- ✅ Aprende de miles de ejemplos
- ✅ Mayor precisión
- ✅ Funciona con preguntas mal escritas

---

## 🚀 PASO 1: Verificar Archivo de Datos

El archivo `datos_veterinarios.json` contiene los ejemplos de entrenamiento.

### Revisar el archivo:

```bash
# Ver si existe
dir datos_veterinarios.json

# O en Windows Explorer:
# Navega a tu carpeta del proyecto y búscalo
```

### Estructura del archivo:

```json
{
  "intents": [
    {
      "tag": "sintomas_fiebre",
      "patterns": [
        "mi perro tiene fiebre",
        "mi gato tiene temperatura alta",
        "mi mascota está muy caliente"
      ],
      "responses": [
        "La fiebre en mascotas requiere atención..."
      ]
    },
    ...
  ]
}
```

---

## 🚀 PASO 2: Entrenar el Modelo

### Opción A: Script Existente (Si existe)

```bash
python entrenar_chatbot_veterinario.py
```

**Salida esperada:**
```
🚀 Iniciando entrenamiento del chatbot veterinario...
📊 Dataset cargado: 500 ejemplos
🔄 Entrenando modelo...
Epoch 1/50 - Loss: 2.1234 - Accuracy: 0.45
Epoch 2/50 - Loss: 1.8567 - Accuracy: 0.62
...
Epoch 50/50 - Loss: 0.2134 - Accuracy: 0.94
✅ Modelo entrenado con 94% de precisión
💾 Guardado en models/chatbot_veterinario.h5
```

### Opción B: Crear Script de Entrenamiento (Si no existe)

Si el script no existe, puedo crearlo para ti. Necesitas:
1. TensorFlow/Keras instalado
2. Archivo de datos `datos_veterinarios.json`
3. Carpeta `models/` para guardar el modelo

---

## 🚀 PASO 3: Agregar Más Datos de Entrenamiento

Para que el modelo aprenda **MÁS COSAS**, necesitas agregar más ejemplos.

### Formato para Agregar Datos:

Edita `datos_veterinarios.json` y agrega:

```json
{
  "tag": "nombre_intencion",
  "patterns": [
    "ejemplo 1",
    "ejemplo 2 con variación",
    "ejemplo 3 diferente forma",
    "ejemplo 4",
    "ejemplo 5",
    "ejemplo 6",
    "ejemplo 7",
    "ejemplo 8",
    "ejemplo 9",
    "ejemplo 10"
  ],
  "responses": [
    "Respuesta 1 para esta intención",
    "Respuesta 2 alternativa",
    "Respuesta 3 variación"
  ]
}
```

### 📝 Ejemplos de Intenciones a Agregar:

#### 1. Estadísticas
```json
{
  "tag": "estadisticas_sistema",
  "patterns": [
    "estadísticas",
    "estadísticas del sistema",
    "muéstrame las estadísticas",
    "quiero ver estadísticas",
    "dame las estadísticas",
    "estadísticas generales",
    "datos del sistema",
    "información del sistema",
    "métricas",
    "números del sistema"
  ],
  "responses": [
    "Mostrando estadísticas del sistema..."
  ]
}
```

#### 2. Tipo de Mascota Más Común
```json
{
  "tag": "tipo_mascota_comun",
  "patterns": [
    "tipo de mascota más común",
    "qué mascota es más común",
    "cuál es el tipo más común",
    "mascota más frecuente",
    "tipo más popular",
    "qué tipo de mascota hay más",
    "mascota más común",
    "tipo común",
    "la mascota más vista"
  ],
  "responses": [
    "Analizando el tipo de mascota más común..."
  ]
}
```

#### 3. Días con Más Atención
```json
{
  "tag": "dias_atencion",
  "patterns": [
    "días con más atención",
    "qué día hay más citas",
    "mejor día para citas",
    "días más ocupados",
    "día con más atención",
    "cuándo hay más citas",
    "día más concurrido",
    "días de mayor demanda"
  ],
  "responses": [
    "Analizando días con más atención..."
  ]
}
```

#### 4. Citas de Hoy
```json
{
  "tag": "citas_hoy",
  "patterns": [
    "citas de hoy",
    "citas hoy",
    "cuántas citas hay hoy",
    "hay citas hoy",
    "citas del día",
    "citas programadas hoy",
    "agenda de hoy",
    "cuántas citas tengo hoy",
    "lista de citas de hoy"
  ],
  "responses": [
    "Consultando citas de hoy..."
  ]
}
```

#### 5. Desparasitación
```json
{
  "tag": "desparasitacion",
  "patterns": [
    "desparasitación",
    "desparasitar",
    "calendario de desparasitación",
    "cuándo desparasitar",
    "cómo desparasitar",
    "desparasitante",
    "parásitos",
    "mi mascota tiene parásitos",
    "cada cuánto desparasitar"
  ],
  "responses": [
    "Información sobre desparasitación..."
  ]
}
```

---

## 📊 REGLAS PARA BUENOS DATOS DE ENTRENAMIENTO

### ✅ Hacer:

1. **Al menos 10 ejemplos por intención** (más es mejor)
2. **Variar las formas de preguntar:**
   - "estadísticas"
   - "muéstrame estadísticas"
   - "quiero ver las estadísticas"
   - "dame las estadísticas del sistema"

3. **Incluir errores comunes:**
   - Con/sin acentos
   - Singular/plural
   - Formal/informal

4. **Cubrir diferentes niveles:**
   - Corto: "estadísticas"
   - Medio: "estadísticas del sistema"
   - Largo: "quiero ver las estadísticas generales del sistema"

### ❌ Evitar:

1. Ejemplos muy similares
2. Menos de 5 ejemplos por intención
3. Solo una forma de preguntar
4. Patterns que se parecen a otras intenciones

---

## 🚀 PASO 4: Re-entrenar con Nuevos Datos

Una vez que agregues más ejemplos:

```bash
python entrenar_chatbot_veterinario.py
```

**Nota:** Cada vez que entrenes, el modelo aprende de TODOS los ejemplos nuevos.

---

## 📈 MEJORA CONTINUA

### Ciclo de Mejora:

```
1. Usuarios prueban el chatbot
   ↓
2. Identificas preguntas que no funciona
   ↓
3. Agregas esos ejemplos a datos_veterinarios.json
   ↓
4. Re-entrenas el modelo
   ↓
5. El chatbot mejora
   ↓
Repite el ciclo
```

### Ejemplo Práctico:

**Usuario pregunta:** "Síntomas y enfermedades"
**Bot no entiende** → Agregar al JSON:

```json
{
  "tag": "sintomas_enfermedad",
  "patterns": [
    "síntomas y enfermedades",
    "síntomas",
    "enfermedades",
    "qué síntomas",
    "cuáles son los síntomas",
    ...
  ]
}
```

---

## 💪 CÓMO HACER QUE APRENDA MÁS

### 1. Agregar Más Intenciones

Actualmente tienes ~30 intenciones. Puedes agregar:
- Citas futuras
- Cancelar citas
- Agendar citas
- Buscar veterinarios
- Precios de servicios
- Horarios de atención
- etc.

### 2. Más Ejemplos por Intención

**Mínimo:** 10 ejemplos
**Recomendado:** 20-30 ejemplos
**Ideal:** 50+ ejemplos

### 3. Datos de Producción

Guarda las preguntas reales de usuarios:

```python
# En tu backend, registra las preguntas:
with open('preguntas_reales.txt', 'a') as f:
    f.write(f"{mensaje}\n")
```

Luego revisa y agrega al JSON.

### 4. Balance de Clases

Asegúrate que cada intención tenga similar cantidad de ejemplos:
- ❌ Intención A: 5 ejemplos, Intención B: 100 ejemplos
- ✅ Todas las intenciones: 20-30 ejemplos cada una

---

## 🔧 SCRIPT DE ENTRENAMIENTO

Si no tienes `entrenar_chatbot_veterinario.py`, aquí está:

```python
#!/usr/bin/env python3
"""
Script para entrenar el modelo LSTM del chatbot veterinario
"""

import json
import numpy as np
import pickle
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import os

# Configuración
MAX_WORDS = 5000
MAX_LEN = 50
EMBEDDING_DIM = 128
LSTM_UNITS = 64
EPOCHS = 50
BATCH_SIZE = 32

# Crear carpeta models si no existe
os.makedirs('models', exist_ok=True)

print("🚀 Iniciando entrenamiento del chatbot veterinario...")

# 1. Cargar datos
print("📂 Cargando datos...")
with open('datos_veterinarios.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 2. Preparar datos
patterns = []
tags = []
responses_dict = {}

for intent in data['intents']:
    tag = intent['tag']
    responses_dict[tag] = intent['responses']
    
    for pattern in intent['patterns']:
        patterns.append(pattern.lower())
        tags.append(tag)

print(f"📊 Dataset: {len(patterns)} ejemplos de {len(set(tags))} intenciones")

# 3. Tokenizar texto
print("🔤 Tokenizando texto...")
tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
tokenizer.fit_on_texts(patterns)

sequences = tokenizer.texts_to_sequences(patterns)
padded_sequences = pad_sequences(sequences, maxlen=MAX_LEN, padding='post')

# 4. Codificar etiquetas
print("🏷️  Codificando etiquetas...")
label_encoder = LabelEncoder()
encoded_tags = label_encoder.fit_transform(tags)
num_classes = len(label_encoder.classes_)

# One-hot encoding
y = keras.utils.to_categorical(encoded_tags, num_classes=num_classes)

# 5. Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    padded_sequences, y, test_size=0.2, random_state=42
)

print(f"📈 Entrenamiento: {len(X_train)} | Prueba: {len(X_test)}")

# 6. Crear modelo
print("🏗️  Construyendo red neuronal...")
model = keras.Sequential([
    layers.Embedding(MAX_WORDS, EMBEDDING_DIM, input_length=MAX_LEN),
    layers.Bidirectional(layers.LSTM(LSTM_UNITS, return_sequences=True)),
    layers.Dropout(0.3),
    layers.Bidirectional(layers.LSTM(LSTM_UNITS)),
    layers.Dropout(0.3),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print(model.summary())

# 7. Entrenar
print(f"\n🔄 Entrenando por {EPOCHS} épocas...")
history = model.fit(
    X_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_data=(X_test, y_test),
    verbose=1
)

# 8. Evaluar
print("\n📊 Evaluando modelo...")
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"✅ Precisión en test: {accuracy*100:.2f}%")

# 9. Guardar
print("\n💾 Guardando modelo...")
model.save('models/chatbot_veterinario.h5')

with open('models/tokenizer_veterinario.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)

with open('models/label_encoder_veterinario.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)

with open('models/intents_veterinario.pkl', 'wb') as f:
    pickle.dump(responses_dict, f)

print("\n🎉 ¡Entrenamiento completado!")
print(f"📁 Archivos guardados en: models/")
print(f"   • chatbot_veterinario.h5")
print(f"   • tokenizer_veterinario.pkl")
print(f"   • label_encoder_veterinario.pkl")
print(f"   • intents_veterinario.pkl")
```

Guarda esto como `entrenar_chatbot_veterinario.py`

---

## 🧪 PROBAR EL MODELO ENTRENADO

Una vez entrenado, reinicia la API:

```bash
python api.py
```

El chatbot automáticamente:
1. Carga el modelo entrenado
2. Usa la red neuronal para clasificar
3. Si falla, usa el sistema de patrones

---

## 📊 RESULTADOS ESPERADOS

### Antes de Entrenar:
- ✅ 5/15 preguntas funcionan (~33%)
- Sistema de patrones básico

### Después de Entrenar:
- ✅ 13/15 preguntas funcionan (~87%)
- Comprende sinónimos y variaciones

### Con Datos Mejorados:
- ✅ 15/15 preguntas funcionan (100%)
- Comprende contexto complejo

---

## ✅ CHECKLIST COMPLETO

- [ ] Verificar que existe `datos_veterinarios.json`
- [ ] Instalar dependencias: `pip install tensorflow scikit-learn`
- [ ] Agregar más ejemplos a cada intención (mínimo 10)
- [ ] Crear/ejecutar `entrenar_chatbot_veterinario.py`
- [ ] Esperar ~5-10 minutos al entrenamiento
- [ ] Verificar precisión > 85%
- [ ] Reiniciar API: `python api.py`
- [ ] Probar preguntas que antes no funcionaban
- [ ] Celebrar 🎉

---

## 🆘 TROUBLESHOOTING

### Error: "No module named 'tensorflow'"
```bash
pip install tensorflow
```

### Error: "File not found: datos_veterinarios.json"
El archivo no existe. Necesitas crearlo con ejemplos.

### Precisión baja (< 70%)
- Agregar más ejemplos (mínimo 20 por intención)
- Entrenar por más épocas (70-100)
- Verificar balance de clases

### Modelo no se carga
Verifica que los archivos .h5 y .pkl existan en `models/`

---

## 🎯 RESUMEN

**Para que el chatbot sea MÁS INTELIGENTE:**

1. **Agrega más ejemplos** a `datos_veterinarios.json`
2. **Entrena el modelo** con `python entrenar_chatbot_veterinario.py`
3. **Reinicia la API**
4. **Prueba y repite**

**Resultado:** Chatbot que entiende contexto, sinónimos y variaciones complejas.

---

*¡Con estos pasos tu chatbot será mucho más inteligente!* 🚀

