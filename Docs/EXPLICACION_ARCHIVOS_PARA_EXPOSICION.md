#  EXPLICACIÓN DE ARCHIVOS .PY - PARA EXPOSICIÓN

##  ARQUITECTURA DEL SISTEMA

El sistema está compuesto por **7 archivos Python** que trabajan en conjunto:

```

                     FRONTEND (React)                        
                  (Tu aplicación web)                        

                      HTTP Requests
                     

  api.py - API REST (FastAPI)                                
   Recibe peticiones HTTP                                  
   Procesa requests                                        
   Retorna respuestas JSON                                 

                                   
                                   
  
 chatbot.py   database.py  predictor.py   
 (IA/NLP)     (PostgreSQL) (ML/Clustering) 
  
                                   
                                   

 config.py - Configuración centralizada       

```

---

##  ARCHIVOS PRINCIPALES

### 1. **api.py**  (NÚCLEO DEL SISTEMA)

**¿Para qué sirve?**
- Es el **servidor REST** que expone todos los servicios
- Recibe peticiones HTTP del frontend
- Coordina todos los módulos (chatbot, database, predictor)
- Retorna datos en formato JSON

**Componentes:**
- **FastAPI:** Framework web moderno de Python
- **Endpoints REST:** 25+ rutas (GET/POST)
- **CORS:** Permite peticiones desde tu frontend

**Endpoints principales:**
```python
POST /api/chat                    # Chatbot
GET  /api/metricas/dashboard      # Métricas de negocio
GET  /api/clustering/completo     # Clustering jerárquico
GET  /api/estadisticas            # Estadísticas
```

**Tecnologías:**
- FastAPI (web framework)
- Pydantic (validación de datos)
- Uvicorn (servidor ASGI)

**Líneas de código:** ~1247 líneas

---

### 2. **chatbot.py**  (INTELIGENCIA CONVERSACIONAL)

**¿Para qué sirve?**
- Procesa mensajes del usuario en lenguaje natural
- Detecta intenciones (¿qué quiere el usuario?)
- Genera respuestas inteligentes
- Puede usar red neuronal LSTM o patrones

**Componentes principales:**

#### a) **Normalización de Texto**
```python
def normalizar_texto(self, texto: str) -> str:
    # Convierte "¿Cuántos CLIENTES?" a "cuantos clientes"
    # Elimina acentos, puntuación y pone en minúsculas
```

#### b) **Detección de Intenciones**
```python
def detectar_intencion(self, texto: str) -> str:
    # Analiza el texto y determina qué quiere el usuario
    # Retorna: 'estadisticas', 'vacunas', 'citas_hoy', etc.
```

#### c) **Respuestas por Intención**
```python
def responder_estadisticas(self) -> str:
    # Consulta la BD y genera respuesta formateada
def responder_vacunas(self) -> str:
    # Responde con información veterinaria
def responder_clustering(self) -> str:
    # Ejecuta análisis de clustering y explica resultados
```

**Intenciones que maneja:** 30+
- Veterinarias: síntomas, vacunas, desparasitación, etc.
- Negocio: ventas, inventario, alertas
- Análisis: estadísticas, clustering, predicciones

**Tecnologías:**
- TensorFlow/Keras (red neuronal LSTM - opcional)
- NLP (procesamiento de lenguaje natural)
- Regex (expresiones regulares)

**Líneas de código:** ~1201 líneas

---

### 3. **database.py**  (CAPA DE DATOS)

**¿Para qué sirve?**
- Gestiona la conexión a PostgreSQL
- Ejecuta consultas SQL
- Retorna datos en formato Pandas DataFrame
- Maneja reconexión automática

**Consultas principales:**

#### a) **Métricas de Negocio**
```python
def obtener_citas_hoy(self) -> pd.DataFrame:
    # Consulta citas del día actual
    
def obtener_ventas_dia(self) -> Dict:
    # Calcula ventas diarias
    
def obtener_comparativa_ventas_mensual(self) -> Dict:
    # Compara mes actual vs anterior
```

#### b) **Análisis Estadístico**
```python
def obtener_tipos_mascota_mas_comunes(self) -> pd.DataFrame:
    # Cuenta y agrupa por tipo de mascota
    
def obtener_dias_con_mas_atencion(self) -> pd.DataFrame:
    # Analiza distribución semanal de citas
```

#### c) **Alertas e Inventario**
```python
def obtener_productos_proximos_vencer(self, dias: int) -> pd.DataFrame:
    # Encuentra productos próximos a vencer
    
def obtener_alerta_bajo_inventario(self) -> pd.DataFrame:
    # Identifica productos con stock crítico
```

**Tecnologías:**
- psycopg2 (driver PostgreSQL)
- Pandas (manipulación de datos)
- SQL (consultas a base de datos)

**Líneas de código:** ~740 líneas

---

### 4. **predictor.py**  (MACHINE LEARNING)

**¿Para qué sirve?**
- Implementa algoritmos de Machine Learning
- **Redes Neuronales:** Predice tipo de mascota y asistencia
- **Hierarchical Clustering:** Agrupa datos automáticamente
- Análisis estadístico avanzado

**Algoritmos implementados:**

#### a) **Redes Neuronales (Deep Learning)**
```python
def construir_modelo_tipo_mascota(self, num_features, num_classes):
    # Red neuronal para clasificación
    # Arquitectura: Dense  Dropout  Dense  Softmax
    
def predecir_tipo_mascota(self, dia, hora, mes, service_id):
    # Usa la red entrenada para predecir
```

#### b) **Hierarchical Clustering**  (NUEVO)
```python
def clustering_mascotas(self, df, n_clusters=3):
    # Agrupa mascotas por características similares
    # Algoritmo: Agglomerative Clustering (Ward)
    
def clustering_clientes(self, df, n_clusters=4):
    # Segmenta clientes en VIP, Regular, Ocasional, Nuevo
    # Usa: frecuencia, gasto, tasa de asistencia
    
def clustering_servicios(self, df, n_clusters=3):
    # Agrupa servicios por patrones de uso
```

**Métricas de Calidad:**
- Silhouette Score (0-1): Mide qué tan bien están los clusters
- Accuracy (redes neuronales)
- Matriz de confusión

**Tecnologías:**
- TensorFlow/Keras (redes neuronales)
- scikit-learn (clustering, métricas)
- scipy (clustering jerárquico)
- numpy (operaciones matemáticas)

**Líneas de código:** ~815 líneas

---

### 5. **config.py**  (CONFIGURACIÓN)

**¿Para qué sirve?**
- Centraliza toda la configuración del sistema
- Evita hardcodear valores
- Facilita cambios de ambiente (dev/prod)

**Configuraciones:**

```python
# Conexión a Base de Datos
DB_CONFIG = {
    'host': 'gondola.proxy.rlwy.net',
    'port': 22967,
    'database': 'railway',
    'user': 'postgres',
    'password': '***'
}

# Configuración de Modelos de IA
MODEL_CONFIG = {
    'max_words': 5000,
    'epochs': 50,
    'batch_size': 32
}

# Rutas de Archivos
PATHS = {
    'models_dir': 'models',
    'chatbot_model': 'models/chatbot_veterinario.h5'
}
```

**Tecnologías:**
- python-dotenv (variables de entorno)

**Líneas de código:** ~78 líneas

---

### 6. **entrenar_chatbot_veterinario.py**  (ENTRENAMIENTO)

**¿Para qué sirve?**
- Entrena la red neuronal LSTM del chatbot
- Lee datos de `datos_veterinarios.json`
- Guarda modelos entrenados en `models/`

**Proceso:**
1. Lee ejemplos de conversaciones
2. Tokeniza (convierte texto a números)
3. Crea red neuronal LSTM
4. Entrena con los ejemplos
5. Guarda modelo entrenado

**Arquitectura de la Red:**
```
Embedding Layer (128 dimensiones)
    
Bidirectional LSTM (64 unidades)
    
Dropout (30%)
    
Bidirectional LSTM (64 unidades)
    
Dropout (30%)
    
Dense (64 neuronas, ReLU)
    
Dense (Softmax)  Clasificación
```

**Tecnologías:**
- TensorFlow/Keras (deep learning)
- LSTM (memoria a largo plazo)
- Word Embeddings

**Tiempo de ejecución:** 5-10 minutos

**Líneas de código:** Variable (~200-300)

---

### 7. **verificar_deteccion.py**  (TESTING)

**¿Para qué sirve?**
- Script de prueba para verificar detecciones
- Valida que el chatbot entienda correctamente
- Usado para debugging

**NO es parte del sistema principal**, solo para desarrollo.

---

##  FLUJO COMPLETO DEL SISTEMA

### Ejemplo: Usuario pregunta "¿Cuántos clientes tengo?"

```
1. FRONTEND (React)
   > fetch('http://localhost:8000/api/chat', {
         body: {"mensaje": "¿Cuántos clientes tengo?"}
       })

2. API.PY
   > Recibe POST /api/chat
   > Llama a: bot.procesar_mensaje()

3. CHATBOT.PY
   > normalizar_texto()  "cuantos clientes tengo"
   > detectar_intencion()  "estadisticas"
   > responder_estadisticas()

4. DATABASE.PY
   > ejecutar_query()
   > SELECT COUNT(*) FROM client WHERE activo = true
   > Retorna: {total_clientes: 150}

5. CHATBOT.PY
   > Formatea respuesta:
       " ESTADÍSTICAS GENERALES:
         Clientes registrados: 150"

6. API.PY
   > Retorna JSON:
       {
         "respuesta": " ESTADÍSTICAS...",
         "intencion": "estadisticas",
         "confianza": 0.9
       }

7. FRONTEND
   > Muestra la respuesta al usuario
```

---

##  ALGORITMOS DE IA UTILIZADOS

### 1. **Red Neuronal LSTM** (chatbot.py)
- **Tipo:** Deep Learning - Recurrent Neural Network
- **Propósito:** Clasificar intenciones del usuario
- **Arquitectura:** Bidirectional LSTM
- **Input:** Texto del usuario
- **Output:** Intención detectada (probabilidad)

### 2. **Redes Neuronales Densas** (predictor.py)
- **Tipo:** Deep Learning - Feedforward
- **Propósito:** Predecir tipo de mascota y asistencia
- **Capas:** Dense  Dropout  Dense  Softmax
- **Input:** Día, hora, mes, servicio, edad
- **Output:** Predicción

### 3. **Hierarchical Clustering** (predictor.py) 
- **Tipo:** Unsupervised Learning - Clustering
- **Algoritmo:** Agglomerative Clustering
- **Métodos:** Ward, Average, Complete
- **Métrica:** Euclidean Distance
- **Evaluación:** Silhouette Score

**Propósito:**
- **Clustering de Mascotas:** Agrupa por edad, servicios, precio
- **Clustering de Clientes:** Segmenta en VIP, Regular, Ocasional, Nuevo
- **Clustering de Servicios:** Agrupa por patrones de uso

**Ventajas:**
-  No requiere etiquetas previas
-  Descubre patrones ocultos
-  Permite segmentación automática

---

##  TECNOLOGÍAS UTILIZADAS

| Tecnología | Archivo | Propósito |
|------------|---------|-----------|
| **FastAPI** | api.py | Framework web REST |
| **PostgreSQL** | database.py | Base de datos relacional |
| **Pandas** | database.py, predictor.py | Análisis de datos |
| **TensorFlow** | chatbot.py, predictor.py | Deep Learning |
| **scikit-learn** | predictor.py | Machine Learning (clustering) |
| **scipy** | predictor.py | Algoritmos científicos |
| **psycopg2** | database.py | Driver PostgreSQL |

---

##  CONCEPTOS DE IA APLICADOS

### 1. **Procesamiento de Lenguaje Natural (NLP)**

**Dónde:** chatbot.py  `normalizar_texto()`, `detectar_intencion()`

**Técnicas:**
- Tokenización
- Eliminación de stop words (implícito)
- Normalización de texto
- Pattern matching con regex

### 2. **Deep Learning - LSTM**

**Dónde:** chatbot.py  `predecir_intencion_neuronal()`

**Concepto:**
- LSTM = Long Short-Term Memory
- Tipo especial de RNN (Recurrent Neural Network)
- Recuerda contexto de palabras anteriores
- Ideal para secuencias de texto

**Arquitectura:**
```
Input: "¿Cuántos clientes tengo?"
   
Embedding: Convierte palabras a vectores [128 dim]
   
Bidirectional LSTM: Procesa secuencia (adelante y atrás)
   
Dense Layers: Clasificación final
   
Softmax: Probabilidades por intención
   
Output: "estadisticas" (90% confianza)
```

### 3. **Supervised Learning - Clasificación**

**Dónde:** predictor.py  `entrenar_modelo_tipo_mascota()`

**Concepto:**
- Aprende de ejemplos etiquetados
- Predice categorías (Perro, Gato, Ave, etc.)
- Usa features: día, hora, mes, servicio

### 4. **Unsupervised Learning - Clustering** 

**Dónde:** predictor.py  `clustering_mascotas()`, `clustering_clientes()`

**Concepto:**
- Agrupa datos sin etiquetas previas
- Descubre patrones automáticamente
- No requiere entrenamiento supervisado

**Algoritmo: Agglomerative Hierarchical Clustering**

```
Paso 1: Cada punto es su propio cluster
   [C1] [C2] [C3] [C4] ... [Cn]

Paso 2: Une clusters más cercanos
   [C1-C2] [C3] [C4] ... [Cn]

Paso 3: Continúa uniendo
   [C1-C2-C3] [C4] ... [Cn]

Paso 4: Hasta tener n_clusters grupos
   [Grupo 1] [Grupo 2] [Grupo 3]
```

**Métodos de Linkage:**
- **Ward:** Minimiza varianza (usado en mascotas)
- **Average:** Promedio de distancias (usado en clientes)
- **Complete:** Máxima distancia (usado en servicios)

**Silhouette Score:**
```
silhouette = (b - a) / max(a, b)

donde:
  a = distancia promedio dentro del cluster
  b = distancia promedio al cluster más cercano

Rango: -1 a +1
  1.0  = Perfectamente separados
  0.5  = Bien separados
  0.0  = Clusters solapados
  -1.0 = Mal agrupados
```

---

##  FLUJO DE DATOS

### Clustering de Clientes (Ejemplo Detallado)

```python
# 1. OBTENER DATOS (database.py)
df = db.obtener_dataset_completo()
# Retorna: 2000 citas con info de clientes

# 2. AGREGAR POR CLIENTE (predictor.py)
clientes_stats = df.groupby('client_id').agg({
    'appointment_id': 'count',    # Frecuencia
    'precio_servicio': 'sum',      # Gasto total
    'asistio': 'mean'              # Tasa asistencia
})
# Resultado: 150 clientes con sus métricas

# 3. ESTANDARIZAR (StandardScaler)
X_scaled = scaler.fit_transform(X)
# Normaliza valores (media=0, std=1)

# 4. APLICAR CLUSTERING
clustering = AgglomerativeClustering(n_clusters=4)
labels = clustering.fit_predict(X_scaled)
# Resultado: [0, 0, 1, 2, 0, 1, 3, 2, ...]

# 5. CARACTERIZAR CLUSTERS
for i in range(4):
    cluster_data = clientes_stats[labels == i]
    # Calcula promedios por cluster

# 6. RETORNAR RESULTADOS
return {
    "segmentos": [
        {"nombre": "VIP", "total_clientes": 35, ...},
        {"nombre": "Regular", "total_clientes": 60, ...}
    ]
}
```

---

##  CÓMO FUNCIONAN JUNTOS

```python
# EJEMPLO: Endpoint de clustering

# 1. API recibe request
@app.get("/api/clustering/clientes")
async def clustering_clientes():

    # 2. Obtiene datos de la BD
    df = db.obtener_dataset_completo()  # database.py
    
    # 3. Aplica clustering
    resultado = predictor.clustering_clientes(df)  # predictor.py
    
    # 4. Retorna JSON
    return resultado
```

---

##  RESUMEN POR RESPONSABILIDAD

| Archivo | Responsabilidad Principal |
|---------|---------------------------|
| **config.py** | Configuración centralizada |
| **database.py** | Acceso a datos (PostgreSQL) |
| **predictor.py** | Machine Learning (IA) |
| **chatbot.py** | Procesamiento de lenguaje natural |
| **api.py** | Exposición de servicios REST |
| **entrenar_chatbot_veterinario.py** | Entrenamiento de modelos |
| **verificar_deteccion.py** | Testing/debugging |

---

##  PARA TU EXPOSICIÓN

### Diapositiva 1: Arquitectura
- Muestra el diagrama de componentes
- Explica cómo se comunican

### Diapositiva 2: Archivos Principales
- api.py  Servidor REST
- chatbot.py  IA conversacional
- database.py  Datos
- predictor.py  Machine Learning

### Diapositiva 3: Algoritmos de IA
- LSTM para chatbot
- Redes neuronales para predicciones
- **Hierarchical Clustering** para segmentación 

### Diapositiva 4: Hierarchical Clustering
- Qué es
- Cómo funciona
- Aplicaciones (segmentación de clientes)

### Diapositiva 5: Resultados
- Métricas de calidad
- Ejemplos de segmentos encontrados
- Aplicaciones prácticas

---

**Ahora voy a agregar comentarios detallados al código...** 

