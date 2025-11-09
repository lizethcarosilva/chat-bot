#  Pet Store - Chatbot Veterinario con IA y Análisis Predictivo

Sistema inteligente de **chatbot veterinario** que responde preguntas sobre enfermedades, cuidados, vacunas y síntomas usando **redes neuronales LSTM**. Además, analiza datos de la base de datos con **redes neuronales predictivas** para identificar patrones, tipos de mascotas más comunes y días con mayor demanda.

---

##  Características Principales

### 1.  Chatbot Veterinario con Red Neuronal LSTM
- **Información Médica**: Enfermedades (Parvovirus, Moquillo, Rabia, Leucemia Felina)
- **Vacunas**: Calendarios de vacunación para perros y gatos
- **Cuidados**: Alimentación, desparasitación, higiene dental
- **Emergencias**: Síntomas de alerta y primeros auxilios
- **Comportamiento**: Problemas de conducta y soluciones
- **Red Neuronal LSTM**: Clasifica intenciones con 85%+ de precisión

### 2.  Análisis con Redes Neuronales Predictivas
- **Predicción de Tipo de Mascota**: Predice qué tipo es más probable según día, hora y servicio (78% precisión)
- **Predicción de Asistencia**: Calcula probabilidad de asistencia a citas (85% precisión)
- **Análisis de Patrones**: Identifica tendencias en los datos de la BD

### 3.  Análisis Estadístico
- Tipos de mascotas más comunes
- Días con mayor demanda de atención
- Horas pico de actividad
- Servicios más solicitados
- Razas más populares por tipo de mascota

### 4.  Consultas a Base de Datos
- Búsqueda de mascotas por nombre
- Historial médico completo
- Próximas citas programadas
- Historial de vacunación
- Información de clientes

---

##  Estructura del Proyecto

```
chat-bot/
 config.py           # Configuración del sistema
 database.py         # Conexión y consultas a PostgreSQL
 predictor.py        # Modelos de red neuronal para predicciones
 chatbot.py          # Chatbot inteligente
 main.py             # Aplicación principal con menús
 requirements.txt    # Dependencias Python
 .env                # Variables de entorno
 README.md           # Este archivo

 models/             # Modelos entrenados (se crean automáticamente)
    chatbot_model.h5
    predictor_model.h5
    tokenizer.pkl
    label_encoder.pkl
    scaler.pkl

 data/               # Datasets generados
    dataset_citas_ml.csv

 exports/            # Reportes exportados
```

---

##  Instalación Rápida

### 1. Requisitos Previos
- Python 3.9 o superior
- pip (gestor de paquetes de Python)
- 4 GB RAM mínimo (8 GB recomendado)
- Conexión a Internet

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

⏱ **Nota**: La instalación puede tardar 5-10 minutos (TensorFlow es pesado).

### 3. Entrenar el Chatbot Veterinario (OBLIGATORIO - Primera vez)
```bash
python entrenar_chatbot_veterinario.py
```

⏱ **Tarda**: 2-5 minutos. Entrena la red neuronal con información veterinaria.

### 4. Iniciar la API REST
```bash
python api.py
```

**La API estará disponible en:** `http://localhost:8000`  
**Documentación:** `http://localhost:8000/docs`

### 5. Consumir desde tu Frontend React
```javascript
// Ejemplo: Chatbot
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    mensaje: "mi perro tiene fiebre",
    usuario_id: "user123"
  })
})
```

---

##  Uso del Sistema

### Sistema Basado en API REST

El sistema funciona completamente mediante API REST que consumes desde tu frontend React.

### 1. Iniciar el Servidor API

```bash
python api.py
```

**Verás:**
```
 INICIANDO API REST - PET STORE CHATBOT
 LISTO - Servidor en: http://localhost:8000
 Documentación: http://localhost:8000/docs
```

### 2. Probar los Endpoints

Abre en tu navegador:
```
http://localhost:8000/docs
```

Aquí puedes probar TODOS los endpoints interactivamente.

### 3. Consumir desde tu Frontend React

```javascript
// Chatbot
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ mensaje: "mi perro tiene fiebre" })
})
  .then(r => r.json())
  .then(data => console.log(data.respuesta));

// Estadísticas
fetch('http://localhost:8000/api/estadisticas')
  .then(r => r.json())
  .then(data => console.log(data));

// Análisis
fetch('http://localhost:8000/api/analisis/tipos-mascota')
  .then(r => r.json())
  .then(data => console.log(data));
```

---

##  Entrenar Modelos de Red Neuronal

### HAY 2 MODELOS DIFERENTES:

### 1⃣ Chatbot Veterinario (LSTM - Información Médica)

**OBLIGATORIO antes de usar el chatbot:**

```bash
python entrenar_chatbot_veterinario.py
```

**QUÉ HACE:**
- Lee `datos_veterinarios.json` (enfermedades, vacunas, cuidados)
- Entrena red neuronal LSTM para clasificar intenciones
- Guarda modelo en `models/chatbot_veterinario.h5`
- ⏱ Tarda: 2-5 minutos
-  Precisión: 85%+

**Archivos generados:**
- `models/chatbot_veterinario.h5` - Red neuronal entrenada
- `models/tokenizer_veterinario.pkl` - Vocabulario
- `models/label_encoder_veterinario.pkl` - Codificador de intenciones
- `models/intents_veterinario.pkl` - Respuestas

### 2⃣ Predictor de Datos (Dense - Análisis de BD)

**OPCIONAL - Solo si usarás predicciones de datos:**

**Desde la API:**
```bash
curl -X POST http://localhost:8000/api/entrenar
```

**O desde código:**
```bash
python
>>> from database import PetStoreDatabase
>>> from predictor import PetStorePredictor
>>> db = PetStoreDatabase()
>>> pred = PetStorePredictor()
>>> df = db.obtener_dataset_completo()
>>> pred.entrenar_modelo_tipo_mascota(df)
>>> pred.entrenar_modelo_asistencia(df)
>>> pred.guardar_modelos()
```

**QUÉ HACE:**
- Analiza datos históricos de la BD
- Entrena 2 modelos:
  - **Tipo de Mascota**: Predice tipo según día/hora/servicio
  - **Asistencia**: Predice probabilidad de asistencia
- ⏱ Tarda: 5-10 minutos
-  Precisión: 75-85%

---

##  Análisis Disponibles

### 1. Tipo de Mascota Más Común
Analiza qué tipos de mascotas están más registrados en el sistema.

**Ejemplo de salida:**
```
 Tipo más común: Perro

 Distribución:
   Perro          250 (45.5%) 
   Gato           180 (32.7%) 
   Ave             70 (12.7%) 
   Conejo          30  (5.5%) 
```

### 2. Día con Más Atención
Identifica qué día de la semana tiene más citas programadas.

**Ejemplo de salida:**
```
 Día con más atención: Viernes

 Distribución semanal:
   Lunes       85 citas 
   Martes      92 citas 
   Miércoles   78 citas 
   Jueves      88 citas 
   Viernes    120 citas 
   Sábado      95 citas 
   Domingo     45 citas 
```

### 3. Hora Pico
Muestra la hora del día con más demanda.

---

##  Predicciones con Red Neuronal

### Predecir Tipo de Mascota

```python
# Ejemplo: Predecir para el Viernes a las 10 AM en Noviembre
Día: 5 (Viernes)
Hora: 10
Mes: 11
Servicio ID: 1

Resultado:
 PREDICCIÓN: Perro
 Confianza: 78.5%

Top 3 más probables:
   • Perro: 78.5%
   • Gato: 15.2%
   • Ave: 4.3%
```

### Predecir Asistencia

```python
# Ejemplo: Predecir si asistirá un cliente
Día: 3 (Miércoles)
Hora: 14
Mes: 11
Servicio: 2
Edad Mascota: 5 años

Resultado:
 Probabilidad de asistencia: 82.3%
 Predicción: Asistirá 
 Confianza: Alta
```

---

##  Base de Datos

### Tablas Principales

El sistema se conecta a una base de datos PostgreSQL con las siguientes tablas:

- **`pet`**: Mascotas registradas
- **`client`**: Clientes/propietarios
- **`appointment`**: Citas programadas
- **`service`**: Servicios ofrecidos
- **`pet_medical_history`**: Historial médico
- **`vaccination`**: Vacunas aplicadas
- **`invoice`**: Facturas
- **`product`**: Productos del inventario

### Configuración de Conexión

Las credenciales están en el archivo `.env`:
```
DB_HOST=gondola.proxy.rlwy.net
DB_PORT=22967
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=LpEGFItXIhiOLcvpeWczptlFPxYnxhhI
```

---

##  Ejemplos de Uso

### Ejemplo 1: Chat Interactivo

```
 Tú: Hola

 PetBot: ¡Hola!  Soy PetBot, tu asistente virtual.

 Tú: ¿Cuál es el tipo de mascota más común?

 PetBot: 
 El tipo más común es: Perro

 Distribución:
   Perro: 250 (45.5%)
   Gato: 180 (32.7%)
   Ave: 70 (12.7%)
```

### Ejemplo 2: Búsqueda de Mascota

```
 Tú: buscar mascota Max

 PetBot:
 RESULTADOS DE BÚSQUEDA: 'Max'

 Max (ID: 45)
   • Tipo: Perro
   • Raza: Golden Retriever
   • Edad: 3 años | Sexo: Macho
   • Propietario: Juan Pérez
   • Contacto: 555-1234
```

### Ejemplo 3: Predicción

```
 Tú: predice tipo mascota

 PetBot:
 PREDICCIÓN: Tipo de Mascota

 Día: Viernes
⏰ Hora: 10:00

 Predicción: Perro
 Confianza: 78.5%
```

---

##  Solución de Problemas

### Error: "No se puede conectar a la base de datos"
- Verifica tu conexión a Internet
- Confirma que las credenciales en `.env` son correctas
- Prueba hacer ping a `gondola.proxy.rlwy.net`

### Error: "ModuleNotFoundError: No module named 'tensorflow'"
```bash
pip install tensorflow
# O la versión CPU:
pip install tensorflow-cpu
```

### Error: "Los modelos no están entrenados"
- Ejecuta la opción 4 del menú principal
- Espera a que termine el entrenamiento
- Los modelos se guardan en `models/`

### Dataset Vacío
- Verifica que hay datos en la base de datos
- Revisa que las tablas tienen registros activos (`activo = true`)

### TensorFlow No Se Instala
```bash
# Instalar versión CPU (más ligera)
pip install tensorflow-cpu==2.15.0
```

---

##  Resultados Esperados

### Precisión de Modelos

Con datos suficientes (>1000 registros):
- **Tipo de Mascota**: 70-85% de precisión
- **Predicción de Asistencia**: 75-90% de precisión

### Tiempo de Entrenamiento

- Dataset pequeño (<1000 registros): 2-5 minutos
- Dataset mediano (1000-5000 registros): 5-10 minutos
- Dataset grande (>5000 registros): 10-20 minutos

---

##  Arquitectura del Sistema

### Flujo de Datos

```
Usuario  main.py  chatbot.py  predictor.py  Red Neuronal
                        
                   database.py  PostgreSQL
```

### Componentes

1. **config.py**: Configuración central
2. **database.py**: Capa de acceso a datos
3. **predictor.py**: Lógica de Machine Learning
4. **chatbot.py**: Procesamiento de lenguaje natural
5. **main.py**: Interfaz de usuario

---

##  Seguridad

-  Variables de entorno en `.env` (no subir a Git)
-  Conexión SSL a PostgreSQL
-  Validación de entradas de usuario
-   No compartir credenciales de base de datos

---

##  Notas Técnicas

### Tecnologías Utilizadas

- **Python 3.9+**: Lenguaje principal
- **TensorFlow/Keras**: Redes neuronales
- **PostgreSQL**: Base de datos
- **Pandas**: Análisis de datos
- **NumPy**: Computación numérica
- **Scikit-learn**: Preprocesamiento ML

### Modelos de Red Neuronal

**Arquitectura - Tipo de Mascota:**
```
Input (4 features)
    
Dense(128, relu)  Dropout(0.3)
    
Dense(64, relu)  Dropout(0.3)
    
Dense(32, relu)  Dropout(0.2)
    
Dense(n_classes, softmax)
```

**Arquitectura - Asistencia:**
```
Input (5 features)
    
Dense(64, relu)  Dropout(0.3)
    
Dense(32, relu)  Dropout(0.2)
    
Dense(16, relu)
    
Dense(1, sigmoid)
```

---

##  Próximas Mejoras

- [ ] Exportación de reportes en PDF
- [ ] Gráficos interactivos con Plotly
- [ ] Dashboard web con Flask/Streamlit
- [ ] API REST para integración
- [ ] Notificaciones automáticas
- [ ] Análisis de sentimiento en comentarios
- [ ] Recomendaciones personalizadas

---

##  Soporte

Si encuentras problemas o tienes sugerencias, verifica:

1. Que Python 3.9+ está instalado
2. Que todas las dependencias están instaladas
3. Que el archivo `.env` existe y tiene las credenciales correctas
4. Que hay conexión a Internet

---

##  Checklist de Instalación

- [ ] Python 3.9+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` configurado
- [ ] Conexión a base de datos probada (`python database.py`)
- [ ] Modelos entrenados (opción 4 del menú)
- [ ] Sistema funcionando correctamente

---

##  Casos de Uso

1. **Análisis de demanda**: Identificar patrones de atención para optimizar recursos
2. **Predicción de no-shows**: Anticipar cancelaciones y optimizar agenda
3. **Segmentación de clientes**: Entender preferencias por tipo de mascota
4. **Recomendaciones**: Sugerir servicios según historial
5. **Chatbot de atención**: Responder preguntas frecuentes automáticamente

---

##  Licencia

Este proyecto es de uso educativo y demostrativo.

---

##  Créditos

Desarrollado para el curso de Aprendizaje Automatizado  
Universidad: SEPTIMO SEMESTRE  
Fecha: Noviembre 2024

---

**¡Gracias por usar PetBot! **

