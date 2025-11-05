"""
SCRIPT DE ENTRENAMIENTO - CHATBOT VETERINARIO CON RED NEURONAL
Entrena una red neuronal LSTM para clasificar intenciones veterinarias
"""

import numpy as np
import json
import pickle
import re
from typing import List, Tuple
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, Dropout, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

print("=" * 80)
print("🧠 ENTRENAMIENTO DE CHATBOT VETERINARIO CON RED NEURONAL")
print("=" * 80)


# =============================================================================
# CONFIGURACIÓN
# =============================================================================
MAX_WORDS = 5000        # Vocabulario máximo
MAX_LEN = 50            # Longitud máxima de secuencias
EMBEDDING_DIM = 128     # Dimensión de embeddings
LSTM_UNITS = 64         # Unidades LSTM
EPOCHS = 150            # Épocas de entrenamiento
BATCH_SIZE = 8          # Tamaño del batch
VALIDATION_SPLIT = 0.2  # 20% para validación


# =============================================================================
# PASO 1: CARGAR Y PREPROCESAR DATOS
# =============================================================================
print("\n📚 PASO 1: Cargando datos de entrenamiento...")

with open('datos_veterinarios.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

patterns = []
labels = []
intents_dict = {}

# Extraer patrones y etiquetas
for intent in data['intents']:
    tag = intent['tag']
    intents_dict[tag] = intent['responses']
    
    for pattern in intent['patterns']:
        # Normalizar texto
        pattern_normalized = pattern.lower().strip()
        pattern_normalized = re.sub(r'[^a-záéíóúñü\s]', '', pattern_normalized)
        pattern_normalized = re.sub(r'\s+', ' ', pattern_normalized)
        
        patterns.append(pattern_normalized)
        labels.append(tag)

print(f"✓ Patrones cargados: {len(patterns)}")
print(f"✓ Intenciones únicas: {len(set(labels))}")
print(f"✓ Intenciones: {', '.join(set(labels))}")


# =============================================================================
# PASO 2: TOKENIZACIÓN Y CODIFICACIÓN
# =============================================================================
print("\n🔧 PASO 2: Tokenizando texto...")

# Tokenizar patrones (convertir palabras a números)
tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
tokenizer.fit_on_texts(patterns)

# Convertir textos a secuencias numéricas
sequences = tokenizer.texts_to_sequences(patterns)

# Padding (rellenar/truncar para que todas tengan la misma longitud)
X = pad_sequences(sequences, maxlen=MAX_LEN, padding='post')

print(f"✓ Vocabulario: {len(tokenizer.word_index)} palabras")
print(f"✓ Forma de X (datos de entrada): {X.shape}")
print(f"✓ Ejemplo de secuencia: {X[0][:10]}...")

# Codificar etiquetas (convertir intenciones a números)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(labels)

# Convertir a formato categórico (one-hot encoding)
y = keras.utils.to_categorical(y_encoded)

print(f"✓ Clases codificadas: {len(label_encoder.classes_)}")
print(f"✓ Forma de y (etiquetas): {y.shape}")


# =============================================================================
# PASO 3: DIVIDIR DATOS EN ENTRENAMIENTO Y PRUEBA
# =============================================================================
print("\n📊 PASO 3: Dividiendo datos...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    stratify=y_encoded
)

print(f"✓ Datos de entrenamiento: {X_train.shape[0]} muestras")
print(f"✓ Datos de prueba: {X_test.shape[0]} muestras")


# =============================================================================
# PASO 4: CONSTRUIR LA RED NEURONAL
# =============================================================================
print("\n🏗️  PASO 4: Construyendo arquitectura de red neuronal...")

"""
ARQUITECTURA DE LA RED:

1. Embedding Layer (Capa de Embeddings):
   - Convierte palabras (números) en vectores densos
   - Cada palabra se representa en un espacio de 128 dimensiones
   - Captura relaciones semánticas entre palabras

2. Bidirectional LSTM (LSTM Bidireccional):
   - Procesa la secuencia en ambas direcciones (adelante y atrás)
   - Captura el contexto completo de cada palabra
   - 64 unidades de memoria

3. Dropout:
   - Desactiva aleatoriamente 30-50% de neuronas durante entrenamiento
   - Previene overfitting (memorización)

4. Dense Layers (Capas Densas):
   - Capas completamente conectadas
   - Aprenden patrones complejos
   - ReLU activation para no-linealidad

5. Output Layer (Capa de Salida):
   - Softmax activation
   - Una neurona por cada intención
   - Produce probabilidades que suman 1
"""

num_classes = len(label_encoder.classes_)

model = Sequential([
    # Capa 1: Embeddings (palabras → vectores)
    Embedding(
        input_dim=MAX_WORDS,      # Tamaño del vocabulario
        output_dim=EMBEDDING_DIM,  # Dimensión de los vectores
        input_length=MAX_LEN      # Longitud de las secuencias
    ),
    
    # Capa 2: LSTM Bidireccional (contexto en ambas direcciones)
    Bidirectional(LSTM(LSTM_UNITS, return_sequences=True)),
    Dropout(0.5),  # 50% de dropout
    
    # Capa 3: Segunda LSTM
    Bidirectional(LSTM(32)),
    Dropout(0.5),
    
    # Capas 4-5: Densas (aprendizaje de patrones)
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    
    # Capa 6: Salida (clasificación)
    Dense(num_classes, activation='softmax')
])

# Compilar modelo
model.compile(
    optimizer='adam',                    # Optimizador Adam (adaptativo)
    loss='categorical_crossentropy',     # Loss para clasificación multiclase
    metrics=['accuracy']                 # Métrica: precisión
)

print("\n📋 Resumen de la arquitectura:")
model.summary()


# =============================================================================
# PASO 5: ENTRENAR LA RED NEURONAL
# =============================================================================
print("\n🚀 PASO 5: Entrenando red neuronal...")
print(f"⏱️  Esto puede tardar varios minutos...\n")

# Callbacks para mejorar el entrenamiento
early_stop = keras.callbacks.EarlyStopping(
    monitor='val_loss',          # Monitorear pérdida en validación
    patience=15,                 # Parar si no mejora en 15 épocas
    restore_best_weights=True    # Restaurar mejor modelo
)

reduce_lr = keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss',          # Monitorear pérdida
    factor=0.5,                  # Reducir learning rate a la mitad
    patience=7,                  # Esperar 7 épocas sin mejora
    min_lr=0.00001              # Learning rate mínimo
)

# Entrenar
history = model.fit(
    X_train, y_train,
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    validation_split=VALIDATION_SPLIT,
    callbacks=[early_stop, reduce_lr],
    verbose=1
)


# =============================================================================
# PASO 6: EVALUAR EL MODELO
# =============================================================================
print("\n📊 PASO 6: Evaluando modelo en datos de prueba...")

# Evaluar en datos de prueba
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)

print(f"\n✓ Pérdida en prueba: {test_loss:.4f}")
print(f"✓ Precisión en prueba: {test_accuracy:.2%}")

# Hacer predicciones en datos de prueba
y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_test_classes = np.argmax(y_test, axis=1)

# Métricas detalladas
from sklearn.metrics import classification_report, confusion_matrix

print("\n📈 Reporte de clasificación:")
print(classification_report(
    y_test_classes, 
    y_pred_classes, 
    target_names=label_encoder.classes_,
    zero_division=0
))


# =============================================================================
# PASO 7: GUARDAR EL MODELO ENTRENADO
# =============================================================================
print("\n💾 PASO 7: Guardando modelo entrenado...")

# Guardar modelo
model.save('models/chatbot_veterinario.h5')
print("✓ Modelo guardado: models/chatbot_veterinario.h5")

# Guardar tokenizer
with open('models/tokenizer_veterinario.pkl', 'wb') as f:
    pickle.dump(tokenizer, f)
print("✓ Tokenizer guardado: models/tokenizer_veterinario.pkl")

# Guardar label encoder
with open('models/label_encoder_veterinario.pkl', 'wb') as f:
    pickle.dump(label_encoder, f)
print("✓ Label encoder guardado: models/label_encoder_veterinario.pkl")

# Guardar diccionario de intenciones
with open('models/intents_veterinario.pkl', 'wb') as f:
    pickle.dump(intents_dict, f)
print("✓ Intenciones guardadas: models/intents_veterinario.pkl")


# =============================================================================
# PASO 8: PROBAR EL MODELO
# =============================================================================
print("\n" + "=" * 80)
print("🧪 PASO 8: Probando el modelo entrenado")
print("=" * 80)

def predecir_intencion(texto, threshold=0.6):
    """Predice la intención de un texto"""
    # Normalizar
    texto_norm = texto.lower().strip()
    texto_norm = re.sub(r'[^a-záéíóúñü\s]', '', texto_norm)
    texto_norm = re.sub(r'\s+', ' ', texto_norm)
    
    # Tokenizar
    sequence = tokenizer.texts_to_sequences([texto_norm])
    padded = pad_sequences(sequence, maxlen=MAX_LEN, padding='post')
    
    # Predecir
    prediction = model.predict(padded, verbose=0)[0]
    max_confidence = np.max(prediction)
    predicted_class = np.argmax(prediction)
    
    if max_confidence < threshold:
        return "desconocido", max_confidence
    
    intent = label_encoder.inverse_transform([predicted_class])[0]
    return intent, max_confidence

# Pruebas
pruebas = [
    "hola",
    "mi perro tiene fiebre",
    "qué vacunas necesita un cachorro",
    "mi gato vomita mucho",
    "cómo desparasitar a mi mascota",
    "qué tipo de mascota es más común",
    "mi perro está enfermo"
]

print("\nPruebas del modelo:\n")
for texto in pruebas:
    intent, confidence = predecir_intencion(texto)
    response = intents_dict.get(intent, ["No tengo respuesta"])[0]
    
    print(f"❓ Pregunta: {texto}")
    print(f"🎯 Intención detectada: {intent} (confianza: {confidence:.2%})")
    print(f"💬 Respuesta: {response[:100]}...")
    print("-" * 80)


# =============================================================================
# RESUMEN FINAL
# =============================================================================
print("\n" + "=" * 80)
print("✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
print("=" * 80)
print(f"""
📊 RESUMEN:
   • Patrones de entrenamiento: {len(patterns)}
   • Intenciones: {len(label_encoder.classes_)}
   • Vocabulario: {len(tokenizer.word_index)} palabras
   • Precisión en prueba: {test_accuracy:.2%}
   • Modelo guardado en: models/chatbot_veterinario.h5

🚀 PRÓXIMOS PASOS:
   1. El chatbot ahora puede responder preguntas veterinarias
   2. Usa la API para consultar el chatbot
   3. Para agregar más datos, edita datos_veterinarios.json y vuelve a entrenar

💡 USAR EL MODELO:
   python api.py
   POST http://localhost:8000/api/chat
   {{
     "mensaje": "mi perro tiene fiebre",
     "usuario_id": "user123"
   }}
""")
print("=" * 80)

