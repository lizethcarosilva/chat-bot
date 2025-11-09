#  DOCUMENTACIÓN TÉCNICA COMPLETA
## Sistema de Chatbot Veterinario con Red Neuronal y Análisis Predictivo

---

##  Tabla de Contenidos

1. [Arquitectura del Sistema](#arquitectura-del-sistema)
2. [Módulo: Database (database.py)](#módulo-database)
3. [Módulo: Predictor (predictor.py)](#módulo-predictor)
4. [Módulo: Chatbot (chatbot.py)](#módulo-chatbot)
5. [Entrenamiento del Chatbot](#entrenamiento-del-chatbot)
6. [API REST (api.py)](#api-rest)
7. [Flujo de Datos](#flujo-de-datos)
8. [Cómo Entrenar los Modelos](#cómo-entrenar-los-modelos)

---

##  Arquitectura del Sistema

El sistema está compuesto por 4 componentes principales:

```

                        FRONTEND REACT                           
                   (Tu aplicación web)                           

                          HTTP Requests
                         

                      API REST (api.py)                          
              FastAPI - Endpoints HTTP/JSON                      

                                               
                                               
    
 CHATBOT          PREDICTOR          DATABASE         
 chatbot.py       predictor.py       database.py      
                                                      
 Red Neuronal     Red Neuronal       PostgreSQL       
 LSTM             Dense              Consultas SQL    
 (Intenciones)    (Predicciones)                      
    
                                               
                                               
    
 Datos            Modelos            Railway DB       
 Veterinarios     Predictivos        PostgreSQL       
    
```

### Flujo de una Petición:

1. **Frontend** envía petición HTTP a la API
2. **API** recibe la petición y llama al módulo correspondiente
3. **Módulo** procesa (chatbot, predictor o database)
4. **Módulo** retorna resultado a la API
5. **API** formatea y envía respuesta JSON al Frontend

---

##  Módulo: Database (database.py)

### Propósito
Gestiona TODAS las conexiones y consultas a la base de datos PostgreSQL.

### Clase Principal: `PetStoreDatabase`

```python
class PetStoreDatabase:
    def __init__(self):
        self.conn = None
        self.conectar()
```

#### Método: `conectar()`

**QUÉ HACE:**
- Establece conexión a PostgreSQL usando credenciales de `config.py`
- Usa psycopg2 para la conexión

**CÓDIGO:**
```python
def conectar(self):
    try:
        self.conn = psycopg2.connect(**DB_CONFIG)
        # DB_CONFIG contiene: host, port, database, user, password
        logger.info(" Conexión exitosa")
    except Exception as e:
        logger.error(f" Error: {e}")
        raise
```

**POR QUÉ ASÍ:**
- psycopg2 es el driver estándar para PostgreSQL en Python
- El try/except maneja errores de conexión gracefully
- Logger registra el estado para debugging

---

#### Método: `ejecutar_query(query, params)`

**QUÉ HACE:**
- Ejecuta cualquier consulta SQL y retorna un DataFrame de pandas

**CÓDIGO:**
```python
def ejecutar_query(self, query: str, params: tuple = None) -> pd.DataFrame:
    try:
        if params:
            df = pd.read_sql(query, self.conn, params=params)
        else:
            df = pd.read_sql(query, self.conn)
        return df
    except Exception as e:
        logger.error(f" Error: {e}")
        return pd.DataFrame()
```

**POR QUÉ ASÍ:**
- pandas.read_sql() convierte automáticamente resultados SQL a DataFrame
- params previene SQL injection
- Retorna DataFrame vacío en caso de error (evita crashes)

---

#### Método: `obtener_dataset_completo()`

**QUÉ HACE:**
- Obtiene TODOS los datos necesarios para entrenar modelos de predicción
- Une múltiples tablas (appointment, pet, service, client)

**CÓDIGO SIMPLIFICADO:**
```python
def obtener_dataset_completo(self) -> pd.DataFrame:
    query = """
    SELECT 
        -- Características temporales
        EXTRACT(YEAR FROM a.fecha_hora) AS año,
        EXTRACT(MONTH FROM a.fecha_hora) AS mes,
        EXTRACT(DAY FROM a.fecha_hora) AS dia,
        EXTRACT(DOW FROM a.fecha_hora) AS dia_semana,
        EXTRACT(HOUR FROM a.fecha_hora) AS hora,
        
        -- Características de servicio
        s.nombre AS servicio,
        s.precio AS precio_servicio,
        s.duracion_minutos,
        
        -- Características de mascota
        p.tipo AS tipo_mascota,
        p.raza,
        p.edad AS edad_mascota,
        p.sexo AS sexo_mascota,
        
        -- Target (lo que queremos predecir)
        CASE WHEN a.estado = 'COMPLETADA' THEN 1 ELSE 0 END AS asistio
    FROM appointment a
    JOIN service s ON a.service_id = s.service_id
    JOIN pet p ON a.pet_id = p.pet_id
    WHERE a.activo = true
    ORDER BY a.fecha_hora DESC;
    """
    return self.ejecutar_query(query)
```

**POR QUÉ ESTA CONSULTA:**
- **EXTRACT()**: Convierte fecha/hora en features numéricos útiles para ML
- **JOIN**: Une tablas para obtener información completa
- **CASE WHEN**: Crea variable binaria (0/1) para clasificación
- **WHERE activo = true**: Solo datos válidos

**FEATURES EXTRAÍDOS:**
- **Temporales**: año, mes, día, día_semana, hora
- **Servicio**: nombre, precio, duración
- **Mascota**: tipo, raza, edad, sexo
- **Target**: asistió o no (1/0)

---

#### Método: `obtener_tipos_mascota_mas_comunes()`

**QUÉ HACE:**
- Analiza cuántas mascotas hay de cada tipo
- Calcula porcentajes y promedios

**CÓDIGO:**
```python
def obtener_tipos_mascota_mas_comunes(self) -> pd.DataFrame:
    query = """
    SELECT 
        p.tipo AS tipo_mascota,
        COUNT(DISTINCT p.pet_id) AS total_mascotas,
        COUNT(a.appointment_id) AS total_citas,
        ROUND(COUNT(a.appointment_id)::numeric / 
              NULLIF(COUNT(DISTINCT p.pet_id), 0), 2) AS promedio_citas,
        ROUND(COUNT(DISTINCT p.pet_id)::numeric * 100.0 / 
              (SELECT COUNT(*) FROM pet WHERE activo = true), 2) AS porcentaje
    FROM pet p
    LEFT JOIN appointment a ON p.pet_id = a.pet_id AND a.activo = true
    WHERE p.activo = true
    GROUP BY p.tipo
    ORDER BY total_mascotas DESC;
    """
    return self.ejecutar_query(query)
```

**ANÁLISIS DEL SQL:**
- **COUNT(DISTINCT p.pet_id)**: Cuenta mascotas únicas (no duplicados)
- **LEFT JOIN**: Incluye mascotas aunque no tengan citas
- **NULLIF()**: Evita división por cero
- **Subquery**: Calcula porcentaje del total
- **GROUP BY**: Agrupa por tipo de mascota

**RESULTADO:**
```
tipo_mascota | total_mascotas | total_citas | promedio_citas | porcentaje
Perro        | 250            | 450         | 1.80           | 45.5
Gato         | 180            | 320         | 1.77           | 32.7
Ave          | 70             | 95          | 1.36           | 12.7
```

---

#### Método: `obtener_dias_con_mas_atencion()`

**QUÉ HACE:**
- Analiza qué días de la semana tienen más citas
- Calcula tasas de asistencia

**CÓDIGO:**
```python
def obtener_dias_con_mas_atencion(self) -> pd.DataFrame:
    query = """
    SELECT 
        CASE EXTRACT(DOW FROM a.fecha_hora)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Lunes'
            WHEN 2 THEN 'Martes'
            ...
        END AS dia_semana,
        COUNT(a.appointment_id) AS total_citas,
        COUNT(CASE WHEN a.estado = 'COMPLETADA' THEN 1 END) AS completadas,
        COUNT(CASE WHEN a.estado = 'CANCELADA' THEN 1 END) AS canceladas,
        ROUND(COUNT(CASE WHEN a.estado = 'COMPLETADA' THEN 1 END)::numeric * 100.0 / 
              NULLIF(COUNT(a.appointment_id), 0), 2) AS tasa_asistencia
    FROM appointment a
    WHERE a.activo = true
    GROUP BY EXTRACT(DOW FROM a.fecha_hora)
    ORDER BY numero_dia;
    """
    return self.ejecutar_query(query)
```

**TÉCNICAS SQL:**
- **EXTRACT(DOW)**: Day Of Week (0=Domingo, 6=Sábado)
- **CASE WHEN**: Condicional para contar estados específicos
- **Tasa de asistencia**: (completadas / total) * 100

---

##  Módulo: Predictor (predictor.py)

### Propósito
Usa redes neuronales para predecir patrones y hacer análisis predictivos.

### Clase Principal: `PetStorePredictor`

```python
class PetStorePredictor:
    def __init__(self):
        self.model_tipo_mascota = None
        self.model_asistencia = None
        self.label_encoder_tipo = LabelEncoder()
        self.scaler = StandardScaler()
        self.trained = False
```

---

### Red Neuronal 1: Predicción de Tipo de Mascota

#### Método: `preparar_datos_tipo_mascota(df)`

**QUÉ HACE:**
- Prepara datos para entrenar la red neuronal
- Convierte texto a números
- Normaliza valores

**CÓDIGO:**
```python
def preparar_datos_tipo_mascota(self, df: pd.DataFrame) -> Tuple:
    # 1. Limpiar datos nulos
    df_clean = df.dropna(subset=['tipo_mascota', 'dia_semana', 'hora', 'mes'])
    
    # 2. Seleccionar features (X)
    X = df_clean[['dia_semana', 'hora', 'mes', 'service_id']].values
    
    # 3. Seleccionar target (y)
    y = self.label_encoder_tipo.fit_transform(df_clean['tipo_mascota'])
    
    # 4. Dividir en train/test (80%/20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 5. Escalar features (normalización)
    X_train = self.scaler.fit_transform(X_train)
    X_test = self.scaler.transform(X_test)
    
    # 6. Convertir y a categorical (one-hot encoding)
    y_train_cat = keras.utils.to_categorical(y_train)
    y_test_cat = keras.utils.to_categorical(y_test)
    
    return X_train, X_test, y_train_cat, y_test_cat
```

**POR QUÉ CADA PASO:**

1. **dropna()**: Elimina filas con valores nulos (la red no puede procesarlos)

2. **Features (X)**: Variables que la red usa para predecir
   - `dia_semana`: 0-6 (patrones temporales)
   - `hora`: 0-23 (patrones horarios)
   - `mes`: 1-12 (estacionalidad)
   - `service_id`: tipo de servicio

3. **LabelEncoder**: Convierte texto a números
   ```
   "Perro"  0
   "Gato"   1
   "Ave"    2
   ```

4. **train_test_split**: Divide datos
   - 80% para entrenar
   - 20% para probar
   - `stratify=y`: Mantiene proporciones de clases

5. **StandardScaler**: Normaliza valores
   ```
   hora = 10  (10 - mean) / std = 0.5
   ```
   **POR QUÉ:** Las redes neuronales funcionan mejor con valores normalizados

6. **to_categorical**: One-hot encoding
   ```
   Clase 0  [1, 0, 0]
   Clase 1  [0, 1, 0]
   Clase 2  [0, 0, 1]
   ```

---

#### Método: `construir_modelo_tipo_mascota()`

**QUÉ HACE:**
- Define la arquitectura de la red neuronal

**CÓDIGO:**
```python
def construir_modelo_tipo_mascota(self, num_features: int, num_classes: int):
    model = Sequential([
        # Capa 1: Entrada y primera capa oculta
        Dense(128, activation='relu', input_shape=(num_features,)),
        Dropout(0.3),
        
        # Capa 2: Segunda capa oculta
        Dense(64, activation='relu'),
        Dropout(0.3),
        
        # Capa 3: Tercera capa oculta
        Dense(32, activation='relu'),
        Dropout(0.2),
        
        # Capa 4: Salida
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model
```

**EXPLICACIÓN DE CADA CAPA:**

**Capa 1: Dense(128, activation='relu')**
- 128 neuronas
- ReLU: max(0, x) - No linealidad
- Aprende patrones simples

**Dropout(0.3)**
- Apaga 30% de neuronas aleatoriamente
- Previene overfitting (memorización)

**Capa 2: Dense(64, activation='relu')**
- 64 neuronas
- Aprende patrones más complejos

**Capa 3: Dense(32, activation='relu')**
- 32 neuronas
- Refina patrones

**Capa 4: Dense(num_classes, activation='softmax')**
- Una neurona por cada clase (Perro, Gato, Ave...)
- Softmax: Convierte a probabilidades que suman 1
```
Output: [0.78, 0.15, 0.05, 0.02]
                    
      Perro Gato  Ave  Otros
```

**Compilación:**
- **optimizer='adam'**: Algoritmo de optimización (aprende automáticamente)
- **loss='categorical_crossentropy'**: Función de pérdida para clasificación
- **metrics=['accuracy']**: Mide precisión

---

#### Método: `entrenar_modelo_tipo_mascota(df)`

**QUÉ HACE:**
- Entrena la red neuronal con los datos

**CÓDIGO:**
```python
def entrenar_modelo_tipo_mascota(self, df: pd.DataFrame) -> Dict:
    # 1. Preparar datos
    X_train, X_test, y_train, y_test = self.preparar_datos_tipo_mascota(df)
    
    # 2. Construir modelo
    self.model_tipo_mascota = self.construir_modelo_tipo_mascota(
        X_train.shape[1],  # Número de features
        y_train.shape[1]   # Número de clases
    )
    
    # 3. Callbacks (mejoras durante entrenamiento)
    early_stop = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    )
    
    # 4. Entrenar
    history = self.model_tipo_mascota.fit(
        X_train, y_train,
        epochs=100,
        batch_size=32,
        validation_split=0.2,
        callbacks=[early_stop],
        verbose=1
    )
    
    # 5. Evaluar
    y_pred = self.model_tipo_mascota.predict(X_test)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_test_classes = np.argmax(y_test, axis=1)
    
    accuracy = accuracy_score(y_test_classes, y_pred_classes)
    
    return {"accuracy": accuracy, "history": history.history}
```

**EXPLICACIÓN:**

**EarlyStopping:**
- Monitorea la pérdida en validación
- Si no mejora en 10 épocas consecutivas (patience=10), detiene
- Restaura el mejor modelo

**fit():**
- **epochs=100**: Máximo 100 pasadas por todos los datos
- **batch_size=32**: Procesa 32 ejemplos a la vez
- **validation_split=0.2**: Usa 20% para validar durante entrenamiento

**Proceso de Entrenamiento:**
```
Época 1: loss: 1.5, val_loss: 1.3, accuracy: 45%
Época 2: loss: 1.2, val_loss: 1.1, accuracy: 52%
...
Época 50: loss: 0.3, val_loss: 0.4, accuracy: 85%
```

---

#### Método: `predecir_tipo_mascota()`

**QUÉ HACE:**
- Usa el modelo entrenado para hacer predicciones

**CÓDIGO:**
```python
def predecir_tipo_mascota(self, dia_semana: int, hora: int, 
                         mes: int, service_id: int) -> Dict:
    # 1. Crear array de features
    X = np.array([[dia_semana, hora, mes, service_id]])
    
    # 2. Escalar (usar mismo scaler del entrenamiento)
    X_scaled = self.scaler.transform(X)
    
    # 3. Predecir con la red neuronal
    pred = self.model_tipo_mascota.predict(X_scaled, verbose=0)[0]
    
    # 4. Obtener top 3
    top_indices = np.argsort(pred)[-3:][::-1]
    
    predicciones = []
    for idx in top_indices:
        predicciones.append({
            "tipo_mascota": self.label_encoder_tipo.classes_[idx],
            "probabilidad": float(pred[idx])
        })
    
    return {
        "predicciones": predicciones,
        "tipo_mas_probable": predicciones[0]["tipo_mascota"],
        "confianza": predicciones[0]["probabilidad"]
    }
```

**EJEMPLO:**
```python
# Input
predecir_tipo_mascota(
    dia_semana=5,  # Viernes
    hora=10,
    mes=11,
    service_id=1
)

# Output
{
    "predicciones": [
        {"tipo_mascota": "Perro", "probabilidad": 0.785},
        {"tipo_mascota": "Gato", "probabilidad": 0.152},
        {"tipo_mascota": "Ave", "probabilidad": 0.043}
    ],
    "tipo_mas_probable": "Perro",
    "confianza": 0.785
}
```

---

##  Módulo: Chatbot (chatbot.py)

### Propósito
Chatbot inteligente que responde preguntas sobre veterinaria usando red neuronal LSTM.

### Clase Principal: `PetStoreBot`

```python
class PetStoreBot:
    def __init__(self):
        self.db = PetStoreDatabase()
        self.predictor = PetStorePredictor()
        
        # Red neuronal para el chatbot
        self.chatbot_model = None
        self.tokenizer = None
        self.label_encoder = None
        self.intents = {}
        
        # Cargar modelo entrenado
        self.cargar_modelo_chatbot()
```

---

### Red Neuronal del Chatbot: LSTM

**DIFERENCIA CON LA RED DE PREDICCIÓN:**
- Red de Predicción: Dense layers (datos numéricos)
- Red del Chatbot: LSTM (secuencias de texto)

**ARQUITECTURA:**
```
Input: "mi perro tiene fiebre"
   
Tokenización: [45, 12, 3, 67]
   
Embedding: [[0.2, 0.5, ...], [0.8, 0.1, ...], ...]
   
Bidirectional LSTM: Procesa secuencia  vectores
   
Dense Layers: Aprende patrones
   
Softmax: Probabilidades por intención
   
Output: {"saludo": 0.05, "enfermedad": 0.85, ...}
```

---

#### Método: `predecir_intencion_neuronal(texto)`

**QUÉ HACE:**
- Clasifica la intención del usuario usando la red neuronal

**CÓDIGO:**
```python
def predecir_intencion_neuronal(self, texto: str) -> Tuple[str, float]:
    # 1. Normalizar texto
    texto_norm = self.normalizar_texto(texto)  # "mi perro tiene fiebre"
    
    # 2. Tokenizar: convertir palabras a números
    sequence = self.tokenizer.texts_to_sequences([texto_norm])
    # [[45, 12, 3, 67]]
    
    # 3. Padding: rellenar/truncar a longitud fija
    padded = pad_sequences(sequence, maxlen=50, padding='post')
    # [[45, 12, 3, 67, 0, 0, 0, ...]] (50 elementos)
    
    # 4. Predecir con red neuronal
    prediction = self.chatbot_model.predict(padded, verbose=0)[0]
    # [0.02, 0.03, 0.85, 0.05, ...]  (probabilidades)
    
    # 5. Obtener intención con mayor probabilidad
    max_confidence = float(np.max(prediction))  # 0.85
    predicted_class = np.argmax(prediction)     # 2
    
    # 6. Verificar threshold de confianza
    if max_confidence < 0.6:
        return "desconocido", max_confidence
    
    # 7. Convertir índice a etiqueta
    intent = self.label_encoder.inverse_transform([predicted_class])[0]
    # 2  "enfermedad_perros"
    
    return intent, max_confidence  # ("enfermedad_perros", 0.85)
```

**PROCESO COMPLETO:**
```
"mi perro tiene fiebre"
    normalizar
"mi perro tiene fiebre"
    tokenizar
[45, 12, 3, 67]
    padding
[45, 12, 3, 67, 0, 0, ..., 0]  (50 elementos)
    red neuronal
[0.02, 0.03, 0.85, 0.05, ...]  (probabilidades)
    argmax + decoder
("enfermedad_perros", 0.85)
```

---

#### Método: `procesar_mensaje(mensaje)`

**QUÉ HACE:**
- Procesa mensaje del usuario y genera respuesta

**CÓDIGO:**
```python
def procesar_mensaje(self, mensaje: str) -> Dict:
    # 1. Detectar intención con red neuronal
    intencion, confianza = self.predecir_intencion_neuronal(mensaje)
    
    # 2. Si es intención veterinaria, responder de inmediato
    if intencion in self.intents:
        respuestas = self.intents[intencion]
        respuesta = random.choice(respuestas)
    
    # 3. Si es consulta de datos, consultar BD
    elif intencion == 'tipo_mascota_comun':
        respuesta = self.responder_tipo_mas_comun()
    
    elif intencion == 'dia_mas_atencion':
        respuesta = self.responder_dia_mas_atencion()
    
    # 4. Si no entiende, respuesta por defecto
    else:
        respuesta = "No entendí tu pregunta..."
    
    return {
        "respuesta": respuesta,
        "intencion": intencion,
        "confianza": confianza,
        "timestamp": datetime.now().isoformat()
    }
```

**FLUJO:**
```
Usuario: "mi perro tiene fiebre"
   
Red Neuronal: intencion="enfermedad_perros", confianza=0.85
   
Buscar respuesta en self.intents["enfermedad_perros"]
   
Retornar: "Las enfermedades más comunes en perros incluyen..."
```

---

##  Entrenamiento del Chatbot

### Script: `entrenar_chatbot_veterinario.py`

**PROCESO COMPLETO:**

#### PASO 1: Cargar Datos

```python
# Leer archivo JSON con intenciones
with open('datos_veterinarios.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extraer patrones y etiquetas
for intent in data['intents']:
    tag = intent['tag']  # "enfermedad_perros"
    for pattern in intent['patterns']:
        patterns.append(pattern)  # "mi perro está enfermo"
        labels.append(tag)
```

**Datos:**
```json
{
  "tag": "enfermedad_perros",
  "patterns": [
    "mi perro está enfermo",
    "enfermedades comunes en perros",
    "mi perro tiene fiebre"
  ],
  "responses": [
    "Las enfermedades más comunes en perros incluyen..."
  ]
}
```

#### PASO 2: Tokenización

```python
# Crear tokenizer
tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
tokenizer.fit_on_texts(patterns)

# Convertir textos a secuencias
sequences = tokenizer.texts_to_sequences(patterns)

# Padding
X = pad_sequences(sequences, maxlen=50, padding='post')
```

**Ejemplo:**
```
"mi perro está enfermo"
    fit_on_texts (construye vocabulario)
word_index = {"mi": 1, "perro": 2, "está": 3, "enfermo": 4, ...}
    texts_to_sequences
[1, 2, 3, 4]
    pad_sequences
[1, 2, 3, 4, 0, 0, 0, ..., 0]  (50 elementos)
```

#### PASO 3: Codificar Etiquetas

```python
# Convertir etiquetas a números
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(labels)

# One-hot encoding
y = keras.utils.to_categorical(y_encoded)
```

**Ejemplo:**
```
labels = ["saludo", "enfermedad", "saludo", "vacuna"]
    fit_transform
y_encoded = [0, 1, 0, 2]
    to_categorical
y = [[1, 0, 0],
     [0, 1, 0],
     [1, 0, 0],
     [0, 0, 1]]
```

#### PASO 4: Construir Red Neuronal LSTM

```python
model = Sequential([
    # Embedding: palabras  vectores densos
    Embedding(
        input_dim=5000,      # Tamaño vocabulario
        output_dim=128,      # Dimensión del vector
        input_length=50      # Longitud secuencia
    ),
    
    # LSTM Bidireccional: procesa en ambas direcciones
    Bidirectional(LSTM(64, return_sequences=True)),
    Dropout(0.5),
    
    # Segunda LSTM
    Bidirectional(LSTM(32)),
    Dropout(0.5),
    
    # Capas densas
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    
    # Salida: una neurona por intención
    Dense(num_classes, activation='softmax')
])
```

**POR QUÉ LSTM Y NO DENSE:**
- LSTM mantiene memoria de palabras anteriores
- Entiende contexto: "no me siento bien" vs "me siento bien"
- Bidirectional lee en ambas direcciones

#### PASO 5: Entrenar

```python
history = model.fit(
    X_train, y_train,
    epochs=150,
    batch_size=8,
    validation_split=0.2,
    callbacks=[early_stop, reduce_lr]
)
```

#### PASO 6: Guardar Modelo

```python
model.save('models/chatbot_veterinario.h5')
pickle.dump(tokenizer, open('models/tokenizer_veterinario.pkl', 'wb'))
pickle.dump(label_encoder, open('models/label_encoder_veterinario.pkl', 'wb'))
```

---

##  API REST (api.py)

### Propósito
Expone todos los módulos como endpoints HTTP para consumo desde frontend.

### Endpoint Principal: `POST /api/chat`

```python
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. Recibir mensaje del frontend
    mensaje = request.mensaje  # "mi perro tiene fiebre"
    
    # 2. Procesar con el chatbot
    resultado = bot.procesar_mensaje(mensaje)
    # {"respuesta": "...", "intencion": "...", "confianza": 0.85}
    
    # 3. Retornar como JSON
    return ChatResponse(**resultado)
```

**FLUJO COMPLETO:**
```
Frontend  POST /api/chat
            
         api.py recibe
            
         bot.procesar_mensaje()
            
         Red Neuronal clasifica
            
         Genera respuesta
            
         api.py retorna JSON
            
         Frontend muestra
```

---

##  Cómo Entrenar los Modelos

### 1. Entrenar Chatbot Veterinario

```bash
python entrenar_chatbot_veterinario.py
```

**QUÉ HACE:**
- Lee `datos_veterinarios.json`
- Entrena red neuronal LSTM
- Guarda modelo en `models/chatbot_veterinario.h5`
- Tarda: 2-5 minutos

**AGREGAR MÁS DATOS:**
Edita `datos_veterinarios.json`:
```json
{
  "tag": "nueva_intencion",
  "patterns": [
    "pregunta 1",
    "pregunta 2"
  ],
  "responses": [
    "respuesta"
  ]
}
```

### 2. Entrenar Predictor de Datos

**Opción A: Desde API**
```bash
curl -X POST http://localhost:8000/api/entrenar
```

**Opción B: Desde Python**
```bash
python
>>> from database import PetStoreDatabase
>>> from predictor import PetStorePredictor
>>> db = PetStoreDatabase()
>>> pred = PetStorePredictor()
>>> df = db.obtener_dataset_completo()
>>> pred.entrenar_modelo_tipo_mascota(df)
>>> pred.guardar_modelos()
```

---

##  Resumen de Flujo de Datos

### Consulta Simple (Estadísticas)
```
Frontend  API  database.py  PostgreSQL  DataFrame  JSON  Frontend
```

### Predicción (Red Neuronal)
```
Frontend  API  predictor.py  Red Neuronal  Predicción  JSON  Frontend
```

### Chatbot (Red Neuronal LSTM)
```
Frontend  API  chatbot.py
                    
                Red Neuronal LSTM
                    
            Clasificación Intención
                    
            Respuesta  JSON  Frontend
```

---

##  Conceptos Clave

### ¿Qué es una Red Neuronal?
Modelo matemático inspirado en el cerebro que aprende patrones de los datos.

### ¿Cómo aprende?
1. Hace predicción
2. Mide error
3. Ajusta pesos
4. Repite hasta minimizar error

### ¿Por qué LSTM para texto?
- Mantiene memoria de secuencias
- Entiende contexto
- Mejor que Dense para texto

### ¿Por qué Dense para números?
- Más simple
- Suficiente para features numéricos
- Más rápido

---

##  Checklist de Entrenamiento

- [ ] Datos suficientes en BD (>100 registros)
- [ ] Ejecutar `python entrenar_chatbot_veterinario.py`
- [ ] Verificar archivos en `models/`
- [ ] Iniciar API: `python api.py`
- [ ] Probar endpoint de chat
- [ ] ¡Listo!

---

**Documentación completa del sistema PetStore - Noviembre 2024**

