# 🎓 GUÍA PARA EXPOSICIÓN - SISTEMA PET STORE CON IA

## 📋 RESUMEN EJECUTIVO

**Proyecto:** Sistema inteligente para gestión de Pet Store  
**Tecnología:** Python + Machine Learning + API REST  
**Algoritmos de IA:** LSTM, Redes Neuronales, Hierarchical Clustering  

---

## 🏗️ ARQUITECTURA DEL SISTEMA

### Capas del Sistema:

```
┌────────────────────────────────────────────────┐
│           CAPA DE PRESENTACIÓN                 │
│         Frontend (React/Angular/Vue)           │
│   Muestra datos, formularios, dashboards      │
└──────────────────┬─────────────────────────────┘
                   │ HTTP/REST
                   ↓
┌────────────────────────────────────────────────┐
│         CAPA DE APLICACIÓN (api.py)            │
│           API REST con FastAPI                 │
│   • Recibe requests HTTP                       │
│   • Coordina servicios                         │
│   • Retorna JSON                               │
└─────┬──────────────┬──────────────┬────────────┘
      │              │              │
      ↓              ↓              ↓
┌──────────┐  ┌───────────┐  ┌──────────────┐
│chatbot.py│  │database.py│  │predictor.py  │
│   (IA)   │  │   (SQL)   │  │  (ML/DL)     │
└──────────┘  └───────────┘  └──────────────┘
      │              │              │
      └──────────────┴──────────────┘
                     │
            ┌────────────────┐
            │   config.py    │
            │ (Configuración)│
            └────────────────┘
```

---

## 📂 DESCRIPCIÓN DE ARCHIVOS .PY

### 1️⃣ **config.py** - Configuración Centralizada

**Líneas:** ~78  
**Complejidad:** ⭐ Baja  

**¿Qué hace?**
- Define constantes del sistema
- Configuración de base de datos
- Parámetros de modelos de IA
- Rutas de archivos

**Contenido principal:**
```python
# Conexión a PostgreSQL
DB_CONFIG = {
    'host': 'gondola.proxy.rlwy.net',
    'port': 22967,
    'database': 'railway',
    'user': 'postgres',
    'password': '***'
}

# Configuración de IA
MODEL_CONFIG = {
    'max_words': 5000,      # Vocabulario máximo
    'epochs': 50,           # Ciclos de entrenamiento
    'embedding_dim': 128    # Dimensión de embeddings
}
```

**Para la exposición:**
- "Separamos configuración del código"
- "Facilita cambios entre desarrollo y producción"

---

### 2️⃣ **database.py** - Capa de Acceso a Datos

**Líneas:** ~740  
**Complejidad:** ⭐⭐ Media  

**¿Qué hace?**
- Conecta a PostgreSQL
- Ejecuta consultas SQL
- Procesa datos con Pandas
- Maneja reconexión automática

**Métodos principales:**

#### Conexión y Queries
```python
def conectar(self):
    # Establece conexión con PostgreSQL
    
def ejecutar_query(self, query, params=None):
    # Ejecuta SQL y retorna DataFrame
    # Incluye reconexión automática si falla
```

#### Métricas de Negocio (NUEVO)
```python
def obtener_citas_hoy(self):
    # SELECT de citas del día actual
    
def obtener_ventas_dia(self):
    # Calcula ventas diarias con SUM, COUNT
    
def obtener_comparativa_ventas_mensual(self):
    # Compara mes actual vs anterior usando CTE
```

#### Análisis Estadístico
```python
def obtener_tipos_mascota_mas_comunes(self):
    # GROUP BY tipo, COUNT, porcentaje
```

**Tecnologías:**
- **psycopg2:** Driver PostgreSQL para Python
- **Pandas:** Manipulación y análisis de datos
- **SQL:** Consultas relacionales

**Para la exposición:**
- "Capa que abstrae la complejidad de SQL"
- "Retorna datos listos para analizar"
- "Manejo robusto de conexiones"

---

### 3️⃣ **chatbot.py** - Inteligencia Conversacional

**Líneas:** ~1201  
**Complejidad:** ⭐⭐⭐⭐ Alta  

**¿Qué hace?**
- Procesa mensajes en lenguaje natural
- Detecta intenciones del usuario
- Genera respuestas inteligentes
- Puede usar IA (LSTM) o patrones

**Componentes clave:**

#### A. Normalización de Texto
```python
def normalizar_texto(self, texto: str) -> str:
    # Entrada: "¿Cuántos CLIENTES tengo?"
    # Salida: "cuantos clientes tengo"
    #
    # Proceso:
    # 1. Minúsculas: "cuántos clientes tengo?"
    # 2. Quitar puntuación: "cuántos clientes tengo"
    # 3. Quitar acentos: "cuantos clientes tengo"
    # 4. Normalizar espacios
```

#### B. Detección de Intenciones (30+ intenciones)
```python
def detectar_intencion(self, texto: str) -> str:
    # Analiza texto normalizado
    # Busca palabras clave
    # Retorna intención detectada
    
    # Ejemplos:
    texto = "cuantos clientes tengo"
    if 'clientes' in texto and 'cuantos' in texto:
        return 'estadisticas'  # ← Intención detectada
```

#### C. Predicción con Red Neuronal (Opcional)
```python
def predecir_intencion_neuronal(self, texto: str):
    # Usa modelo LSTM entrenado
    # Proceso:
    # 1. Tokeniza texto (palabras → números)
    # 2. Padding (ajusta longitud)
    # 3. Pasa por red LSTM
    # 4. Softmax da probabilidades por intención
    # 5. Retorna intención con mayor probabilidad
```

**Modelo LSTM (si está entrenado):**
- **Entrada:** Secuencia de palabras
- **Embedding:** Convierte palabras a vectores (128 dim)
- **Bidirectional LSTM:** Procesa secuencia en ambas direcciones
- **Salida:** Probabilidades por cada intención

**Para la exposición:**
- "Dos niveles: Patrones simples + Red neuronal avanzada"
- "LSTM entiende contexto y sinónimos"
- "Maneja 30+ intenciones diferentes"

---

### 4️⃣ **predictor.py** - Machine Learning y Clustering

**Líneas:** ~815  
**Complejidad:** ⭐⭐⭐⭐⭐ Muy Alta  

**¿Qué hace?**
- Implementa 3 tipos de algoritmos de IA
- Predice con redes neuronales
- **Agrupa datos con Hierarchical Clustering** 🔬

**Algoritmos implementados:**

#### A. Redes Neuronales para Predicción
```python
def entrenar_modelo_tipo_mascota(self, df):
    # Red neuronal densa (feedforward)
    # Predice: Tipo de mascota según día/hora/servicio
    
    # Arquitectura:
    # Input (4 features) 
    #   → Dense(128, ReLU) 
    #   → Dropout(0.3)
    #   → Dense(64, ReLU)
    #   → Dropout(0.3)
    #   → Dense(num_clases, Softmax)
    # Output (probabilidades)
```

#### B. Hierarchical Clustering 🔬 (ESTRELLA DEL PROYECTO)

**Clustering de Mascotas:**
```python
def clustering_mascotas(self, df, n_clusters=3):
    # OBJETIVO: Agrupar mascotas similares
    
    # FEATURES: edad, servicio, precio
    # 
    # ALGORITMO: Agglomerative Hierarchical
    # - Linkage: Ward (minimiza varianza)
    # - Métrica: Euclidiana
    # 
    # PROCESO:
    # 1. Estandarizar datos (StandardScaler)
    # 2. Aplicar AgglomerativeClustering
    # 3. Evaluar con Silhouette Score
    # 4. Caracterizar cada cluster
    # 
    # RESULTADO:
    # - Cluster 0: Perros jóvenes (< 2 años)
    # - Cluster 1: Gatos adultos (3-7 años)
    # - Cluster 2: Mascotas senior (> 7 años)
```

**Clustering de Clientes:** (MÁS IMPORTANTE)
```python
def clustering_clientes(self, df, n_clusters=4):
    # OBJETIVO: Segmentar clientes por comportamiento
    
    # FEATURES:
    # - total_citas: Frecuencia de visitas
    # - gasto_total: Valor del cliente
    # - tasa_asistencia: Confiabilidad
    # 
    # ALGORITMO: Agglomerative
    # - Linkage: Average
    # - Métrica: Euclidiana
    # 
    # SEGMENTOS ENCONTRADOS:
    # 1. VIP - Alta frecuencia
    #    • Visitas: 8+ citas
    #    • Gasto: $800+
    #    • Asistencia: 90%+
    #    → Estrategia: Programa de lealtad
    # 
    # 2. Regular - Moderado
    #    • Visitas: 4-7 citas
    #    • Gasto: $300-800
    #    • Asistencia: 75-85%
    #    → Estrategia: Mantener satisfacción
    # 
    # 3. Ocasional - Bajo
    #    • Visitas: 1-3 citas
    #    • Gasto: $100-300
    #    • Asistencia: 60-75%
    #    → Estrategia: Reactivación
    # 
    # 4. Nuevo - Exploratorio
    #    • Visitas: 1-2 citas
    #    • Gasto: < $100
    #    • Asistencia: Variable
    #    → Estrategia: Onboarding
```

**Métrica de Calidad: Silhouette Score**
```python
# Fórmula:
s(i) = (b(i) - a(i)) / max(a(i), b(i))

donde:
  a(i) = distancia promedio al mismo cluster
  b(i) = distancia promedio al cluster más cercano

# Interpretación:
#  1.0 = Cluster perfecto
#  0.5 = Bien separado
#  0.0 = En el borde
# -1.0 = Probablemente mal asignado
```

**Para la exposición:**
- "Clustering encuentra grupos automáticamente"
- "No necesita entrenamiento supervisado"
- "Útil para segmentación de clientes"

---

### 5️⃣ **api.py** - Servidor REST

**Líneas:** ~1247  
**Complejidad:** ⭐⭐⭐ Media-Alta  

**¿Qué hace?**
- Servidor web con FastAPI
- Expone 25+ endpoints REST
- Coordina todos los módulos
- Maneja CORS para frontend

**Endpoints por categoría:**

#### Clustering (NUEVO)
```python
@app.get("/api/clustering/clientes")
async def clustering_clientes(n_clusters: int = 4):
    # 1. Obtiene datos de la BD
    df = db.obtener_dataset_completo()
    
    # 2. Aplica clustering
    resultado = predictor.clustering_clientes(df, n_clusters)
    
    # 3. Retorna JSON
    return resultado
```

#### Chatbot
```python
@app.post("/api/chat")
async def chat(request: ChatRequest):
    # 1. Recibe mensaje del usuario
    # 2. Procesa con chatbot
    # 3. Retorna respuesta + intención + confianza
```

#### Métricas
```python
@app.get("/api/metricas/dashboard")
async def obtener_dashboard_completo():
    # Retorna todas las métricas en una sola llamada
```

**Tecnologías:**
- **FastAPI:** Framework web moderno asíncrono
- **Pydantic:** Validación automática de datos
- **Uvicorn:** Servidor ASGI de alto rendimiento

**Para la exposición:**
- "API REST permite acceso desde cualquier frontend"
- "FastAPI genera documentación automática"
- "Arquitectura asíncrona para mejor rendimiento"

---

### 6️⃣ **entrenar_chatbot_veterinario.py** - Entrenamiento

**Líneas:** Variable  
**Complejidad:** ⭐⭐⭐ Media  

**¿Qué hace?**
- Entrena red neuronal LSTM del chatbot
- Lee ejemplos de `datos_veterinarios.json`
- Guarda modelos entrenados

**Proceso de entrenamiento:**

```python
# 1. CARGAR DATOS
with open('datos_veterinarios.json') as f:
    data = json.load(f)
# Ejemplos: "mi perro tiene fiebre" → intención: "sintomas"

# 2. TOKENIZACIÓN
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(patterns)
# Convierte: "perro" → 145, "tiene" → 28, "fiebre" → 392

# 3. PADDING
padded = pad_sequences(sequences, maxlen=50)
# Ajusta todas las secuencias a la misma longitud

# 4. CREAR RED NEURONAL LSTM
model = Sequential([
    Embedding(5000, 128),              # Capa de embeddings
    Bidirectional(LSTM(64)),           # LSTM bidireccional
    Dense(num_intenciones, softmax)    # Clasificación
])

# 5. ENTRENAR
model.fit(X_train, y_train, epochs=50)
# Aprende de los ejemplos

# 6. GUARDAR
model.save('models/chatbot_veterinario.h5')
```

**Para la exposición:**
- "LSTM aprende de ejemplos etiquetados"
- "Proceso de entrenamiento supervisa

do"
- "Mejora con más datos de entrenamiento"

---

### 7️⃣ **verificar_deteccion.py** - Testing

**Líneas:** ~90  
**Complejidad:** ⭐ Baja  

**¿Qué hace?**
- Script de prueba
- Verifica que las detecciones funcionen
- Usado solo en desarrollo

**No incluir en exposición** (es solo para debugging)

---

## 🔬 ALGORITMO PRINCIPAL: HIERARCHICAL CLUSTERING

### ¿Qué es?

Algoritmo de **aprendizaje no supervisado** que agrupa datos similares sin necesidad de etiquetas previas.

### ¿Cómo funciona?

**Proceso Bottom-Up (Agglomerative):**

```
Inicio: N puntos, N clusters
  [C1] [C2] [C3] [C4] [C5] ... [C150]

Iteración 1: Une los 2 más cercanos
  [C1-C2] [C3] [C4] [C5] ... [C150]

Iteración 2: Une los 2 más cercanos
  [C1-C2-C5] [C3] [C4] ... [C150]

...continúa...

Final: 4 clusters
  [Grupo 1: VIP]  [Grupo 2: Regular]  
  [Grupo 3: Ocasional]  [Grupo 4: Nuevo]
```

### Métodos de Linkage:

**Ward (usado en mascotas):**
- Minimiza la varianza dentro de cada cluster
- Crea clusters compactos y esféricos

**Average (usado en clientes):**
- Promedio de distancias entre todos los puntos
- Balance entre single y complete

**Complete (usado en servicios):**
- Máxima distancia entre puntos
- Crea clusters más separados

### Fórmula de Distancia Euclidiana:

```
d(p, q) = √((p₁-q₁)² + (p₂-q₂)² + (p₃-q₃)²)

Ejemplo con 2 clientes:
Cliente A: [5 citas, $500 gasto, 0.8 asistencia]
Cliente B: [3 citas, $300 gasto, 0.6 asistencia]

Después de estandarizar:
Cliente A: [0.5, 0.3, 0.7]
Cliente B: [-0.2, -0.4, -0.5]

Distancia = √((0.5-(-0.2))² + (0.3-(-0.4))² + (0.7-(-0.5))²)
          = √(0.49 + 0.49 + 1.44)
          = √2.42
          = 1.56
```

### Silhouette Score - Métrica de Calidad:

```python
# Para cada punto i:
a(i) = distancia promedio a puntos del mismo cluster
b(i) = distancia promedio al cluster más cercano

silhouette(i) = (b(i) - a(i)) / max(a(i), b(i))

# Promedio de todos los puntos = Silhouette Score global
```

**Interpretación visual:**
```
Score = 0.9  →  ●●●●●  ·····  ●●●●●  (Muy separados)
Score = 0.5  →  ●●●   ····   ●●●●   (Bien separados)
Score = 0.2  →  ●●··●● ·●··●  ●··●●  (Solapados)
```

---

## 📊 TECNOLOGÍAS DE IA UTILIZADAS

| Tecnología | Tipo | Dónde se usa | Propósito |
|------------|------|--------------|-----------|
| **TensorFlow** | Deep Learning | chatbot.py, predictor.py | Redes neuronales |
| **LSTM** | RNN | chatbot.py | Procesamiento de secuencias |
| **scikit-learn** | Machine Learning | predictor.py | Clustering, métricas |
| **AgglomerativeClustering** | Clustering | predictor.py | Agrupamiento jerárquico |
| **StandardScaler** | Preprocessing | predictor.py | Normalización |
| **Silhouette Score** | Métrica | predictor.py | Validación de clusters |

---

## 🎯 FLUJO COMPLETO: Ejemplo Real

### Usuario pregunta: "clustering"

```
1. FRONTEND
   └─> POST /api/chat
       Body: {"mensaje": "clustering"}

2. API.PY (línea 135)
   └─> @app.post("/api/chat")
   └─> bot.procesar_mensaje("clustering")

3. CHATBOT.PY (línea 945)
   └─> normalizar_texto("clustering")
       Resultado: "clustering"
   
   └─> detectar_intencion("clustering")
       Encuentra: "clustering" in texto
       Retorna: 'clustering'
   
   └─> procesar_mensaje() → línea 1078
       elif intencion == 'clustering':
           responder_clustering()

4. CHATBOT.PY → responder_clustering() (línea 887)
   └─> db.obtener_dataset_completo()
       (2000 citas de la BD)
   
   └─> predictor.analisis_clustering_completo(df)

5. PREDICTOR.PY → analisis_clustering_completo() (línea 729)
   └─> clustering_mascotas(df, 3)    # Agrupa mascotas
   └─> clustering_clientes(df, 4)    # Segmenta clientes
   └─> clustering_servicios(df, 3)   # Agrupa servicios

6. PREDICTOR.PY → clustering_clientes() (línea 545)
   # PASO 1: Agrupar por cliente
   clientes_stats = df.groupby('client_id').agg({...})
   
   # PASO 2: Seleccionar features
   X = clientes_stats[['total_citas', 'gasto_total', 'tasa_asistencia']]
   
   # PASO 3: Estandarizar
   X_scaled = StandardScaler().fit_transform(X)
   
   # PASO 4: Clustering
   clustering = AgglomerativeClustering(n_clusters=4, linkage='average')
   labels = clustering.fit_predict(X_scaled)
   
   # PASO 5: Caracterizar segmentos
   for cada segmento:
       calcular promedios
       asignar nombre (VIP, Regular, etc.)
   
   # Retorna JSON con segmentos

7. CHATBOT.PY
   └─> Formatea respuesta bonita con emojis
   └─> Retorna a API

8. API.PY
   └─> Retorna JSON al frontend

9. FRONTEND
   └─> Muestra resultado al usuario
```

---

## 🎓 PUNTOS CLAVE PARA LA EXPOSICIÓN

### Slide 1: Introducción
- Sistema completo de Pet Store
- Backend en Python
- Frontend separado (React/Angular/etc.)

### Slide 2: Arquitectura
- 4 capas: Presentación, API, Lógica, Datos
- 7 archivos Python con responsabilidades claras

### Slide 3: Tecnologías de IA
- **LSTM:** Chatbot inteligente
- **Redes Neuronales:** Predicciones
- **Hierarchical Clustering:** Segmentación automática 🔬

### Slide 4: Hierarchical Clustering (DESTACAR)
- Qué es: Aprendizaje no supervisado
- Cómo funciona: Agglomerative bottom-up
- Aplicación: Segmentación de clientes

### Slide 5: Resultados
- 4 segmentos de clientes encontrados
- Silhouette Score: 0.587 (Buena calidad)
- Aplicaciones: Marketing, CRM, Retención

### Slide 6: Demo
- Mostrar Swagger UI: http://localhost:8000/docs
- Ejecutar: GET /api/clustering/clientes
- Mostrar resultados

---

## 📚 ARCHIVOS DE REFERENCIA

| Archivo | Para qué leerlo |
|---------|-----------------|
| `EXPLICACION_ARCHIVOS_PARA_EXPOSICION.md` | Resumen de cada archivo |
| `HIERARCHICAL_CLUSTERING_DOCS.md` | Teoría del clustering |
| `ENDPOINTS_CLUSTERING.md` | Endpoints disponibles |

---

## ✅ RESUMEN PARA TU EXPOSICIÓN

**Sistema:** Pet Store con IA  
**Archivos Python:** 7 (4 principales)  
**Algoritmos de IA:** 3 tipos  
**Destacar:** Hierarchical Clustering para segmentación  
**Métricas:** Silhouette Score, Accuracy  
**Endpoints:** 25+ servicios REST  

**Mensaje clave:**  
*"Sistema que combina bases de datos, IA y clustering para descubrir patrones automáticamente y segmentar clientes sin supervisión humana"*

---

**¡Listo para tu exposición!** 🎓📊🔬

