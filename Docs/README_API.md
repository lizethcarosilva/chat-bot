# 🔌 API REST - Pet Store Chatbot

## 📖 Resumen

Esta API REST proporciona **todos los endpoints necesarios** para tu frontend React. Ya no necesitas ejecutar `main.py`, solo inicia la API y consume los endpoints.

---

## ⚡ Inicio Rápido

### 1. Instalar Dependencias (Una sola vez)
```bash
pip install fastapi uvicorn pydantic
```

### 2. Iniciar la API
```bash
python api.py
```

**O alternativamente:**
```bash
python iniciar_api.py
```

### 3. Verificar que Funciona
Abre en tu navegador: `http://localhost:8000/docs`

---

## 🌐 URLs de la API

| URL | Descripción |
|-----|-------------|
| `http://localhost:8000` | Base de la API |
| `http://localhost:8000/docs` | **Documentación interactiva Swagger** ⭐ |
| `http://localhost:8000/redoc` | Documentación ReDoc |
| `http://localhost:8000/api/health` | Estado del servidor |

---

## 🔌 Endpoints Principales para tu Frontend

### 1️⃣ Chatbot
```http
POST /api/chat
Content-Type: application/json

{
  "mensaje": "¿Cuál es el tipo de mascota más común?",
  "usuario_id": "user123"
}
```

**Respuesta:**
```json
{
  "respuesta": "🏆 El tipo más común es: Perro (45.5%)",
  "intencion": "tipo_mas_comun",
  "confianza": 0.9,
  "timestamp": "2024-11-03T10:30:00"
}
```

---

### 2️⃣ Estadísticas para Dashboard
```http
GET /api/estadisticas
```

**Respuesta:**
```json
{
  "total_mascotas": 250,
  "total_clientes": 150,
  "total_citas": 2000,
  "total_servicios": 15
}
```

---

### 3️⃣ Análisis - Tipos de Mascota Más Comunes
```http
GET /api/analisis/tipos-mascota
```

**Respuesta:**
```json
{
  "tipo_mas_comun": "Perro",
  "estadisticas": [
    {
      "tipo_mascota": "Perro",
      "total_mascotas": 250,
      "total_citas": 450,
      "promedio_citas": 1.8,
      "porcentaje": 45.5
    },
    {
      "tipo_mascota": "Gato",
      "total_mascotas": 180,
      "total_citas": 320,
      "promedio_citas": 1.77,
      "porcentaje": 32.7
    }
  ]
}
```

---

### 4️⃣ Análisis - Días con Más Atención
```http
GET /api/analisis/dias-atencion
```

**Respuesta:**
```json
{
  "dia_mas_atencion": "Viernes",
  "estadisticas": [
    {
      "dia_semana": "Lunes",
      "numero_dia": 1,
      "total_citas": 85,
      "completadas": 72,
      "canceladas": 13,
      "tasa_asistencia": 84.7
    }
  ]
}
```

---

### 5️⃣ Análisis - Horas Pico
```http
GET /api/analisis/horas-pico
```

**Respuesta:**
```json
{
  "hora_pico": 10,
  "estadisticas": [
    {
      "hora": 10,
      "total_citas": 120,
      "mascotas_unicas": 95,
      "clientes_unicos": 88,
      "duracion_promedio": 45.5
    }
  ]
}
```

---

### 6️⃣ Análisis - Servicios Más Utilizados
```http
GET /api/analisis/servicios
```

**Respuesta:**
```json
{
  "servicio_mas_popular": "Consulta General",
  "estadisticas": [
    {
      "service_id": 1,
      "servicio": "Consulta General",
      "precio": 50.00,
      "total_citas": 450,
      "completadas": 385,
      "canceladas": 65,
      "tasa_asistencia": 85.5
    }
  ]
}
```

---

### 7️⃣ Predicción - Tipo de Mascota (Red Neuronal)
```http
POST /api/predicciones/tipo-mascota
Content-Type: application/json

{
  "dia_semana": 5,
  "hora": 10,
  "mes": 11,
  "service_id": 1
}
```

**Respuesta:**
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

### 8️⃣ Predicción - Asistencia a Cita
```http
POST /api/predicciones/asistencia
Content-Type: application/json

{
  "dia_semana": 3,
  "hora": 14,
  "mes": 11,
  "service_id": 2,
  "edad_mascota": 5
}
```

**Respuesta:**
```json
{
  "probabilidad_asistencia": 0.823,
  "asistira": true,
  "confianza": "Alta"
}
```

---

### 9️⃣ Buscar Mascota
```http
GET /api/mascotas/buscar/Max
```

**Respuesta:**
```json
{
  "mascotas": [
    {
      "pet_id": 45,
      "nombre": "Max",
      "tipo": "Perro",
      "raza": "Golden Retriever",
      "edad": 3,
      "sexo": "Macho",
      "propietario": "Juan Pérez",
      "telefono": "555-1234",
      "correo": "juan@example.com"
    }
  ],
  "total": 1
}
```

---

### 🔟 Listar Servicios Disponibles
```http
GET /api/servicios
```

**Respuesta:**
```json
{
  "servicios": [
    {
      "service_id": 1,
      "nombre": "Consulta General",
      "descripcion": "Revisión médica completa",
      "precio": 50.00,
      "duracion_minutos": 30
    }
  ],
  "total": 15
}
```

---

## 🔧 Integración con tu Frontend React

### Configurar Axios (Una sola vez)

**`src/services/api.js`**
```javascript
import axios from 'axios';

const API_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export default api;
```

### Ejemplos de Uso

#### Obtener Estadísticas para Dashboard
```javascript
import api from './services/api';

const Dashboard = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api.get('/api/estadisticas')
      .then(response => setStats(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h1>Mascotas: {stats?.total_mascotas}</h1>
      <h1>Clientes: {stats?.total_clientes}</h1>
    </div>
  );
};
```

#### Chatbot
```javascript
import api from './services/api';

const Chatbot = () => {
  const [mensaje, setMensaje] = useState('');
  const [respuesta, setRespuesta] = useState('');

  const enviar = async () => {
    const response = await api.post('/api/chat', {
      mensaje: mensaje,
      usuario_id: 'user123'
    });
    setRespuesta(response.data.respuesta);
  };

  return (
    <div>
      <input value={mensaje} onChange={(e) => setMensaje(e.target.value)} />
      <button onClick={enviar}>Enviar</button>
      <p>{respuesta}</p>
    </div>
  );
};
```

#### Análisis de Tipos de Mascota
```javascript
import api from './services/api';

const Analisis = () => {
  const [datos, setDatos] = useState(null);

  useEffect(() => {
    api.get('/api/analisis/tipos-mascota')
      .then(response => setDatos(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div>
      <h2>Tipo más común: {datos?.tipo_mas_comun}</h2>
      {datos?.estadisticas.map(item => (
        <div key={item.tipo_mascota}>
          <p>{item.tipo_mascota}: {item.total_mascotas} ({item.porcentaje}%)</p>
        </div>
      ))}
    </div>
  );
};
```

#### Predicción con IA
```javascript
import api from './services/api';

const Prediccion = () => {
  const [resultado, setResultado] = useState(null);

  const predecir = async () => {
    const response = await api.post('/api/predicciones/tipo-mascota', {
      dia_semana: 5,  // Viernes
      hora: 10,
      mes: 11,
      service_id: 1
    });
    setResultado(response.data);
  };

  return (
    <div>
      <button onClick={predecir}>Predecir</button>
      {resultado && (
        <div>
          <h3>{resultado.tipo_mas_probable}</h3>
          <p>Confianza: {(resultado.confianza * 100).toFixed(1)}%</p>
        </div>
      )}
    </div>
  );
};
```

---

## ⚠️ Antes de las Predicciones

**Los modelos deben estar entrenados primero:**

### Opción 1: Desde la API
```http
POST /api/entrenar
```

Este endpoint entrena los modelos en segundo plano (5-10 minutos).

### Opción 2: Desde Terminal (Solo una vez)
```bash
python main.py
# Selecciona opción 4: Entrenar Modelos
```

### Verificar Estado
```http
GET /api/predicciones/estado
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

---

## 🔄 Flujo de Trabajo

```
1. Iniciar API: python api.py
   ↓
2. API corre en: http://localhost:8000
   ↓
3. Frontend hace peticiones a: http://localhost:8000/api/*
   ↓
4. API consulta base de datos PostgreSQL
   ↓
5. API devuelve JSON al frontend
   ↓
6. Frontend muestra los datos
```

---

## 🚨 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'fastapi'"
```bash
pip install fastapi uvicorn pydantic
```

### Error: "Address already in use"
El puerto 8000 está ocupado. Cambia el puerto en `api.py` línea 798:
```python
uvicorn.run("api:app", host="0.0.0.0", port=3001, reload=True)
```

### Error: "Los modelos no están entrenados"
```bash
# Opción 1: Entrenar desde terminal
python main.py  # → Opción 4

# Opción 2: Desde tu frontend
POST http://localhost:8000/api/entrenar
```

### Error de CORS desde el frontend
En `api.py` línea ~38, actualiza:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📂 Archivos del Proyecto

```
chat-bot/
├── api.py                    ⭐ EJECUTAR ESTE
├── iniciar_api.py            ⭐ O ESTE (alternativa)
├── database.py               (usado por api.py)
├── predictor.py              (usado por api.py)
├── chatbot.py                (usado por api.py)
├── config.py                 (configuración)
├── main.py                   (NO NECESARIO - solo para terminal)
├── requirements.txt
└── .env                      (credenciales BD)
```

---

## 📚 Documentación Completa

- **API_ENDPOINTS.md** - Lista completa de todos los endpoints
- **EJEMPLOS_REACT.md** - Componentes React completos
- **README.md** - Documentación general del proyecto

---

## ✅ Checklist

- [ ] Instalar dependencias: `pip install fastapi uvicorn pydantic`
- [ ] Iniciar API: `python api.py`
- [ ] Verificar: `http://localhost:8000/docs`
- [ ] Probar endpoint: `GET http://localhost:8000/api/estadisticas`
- [ ] Configurar CORS si es necesario
- [ ] Integrar con tu frontend React
- [ ] Entrenar modelos si usarás predicciones

---

## 🎯 Endpoints Más Importantes para tu Dashboard

```javascript
// 1. Estadísticas generales
GET /api/estadisticas

// 2. Tipo de mascota más común (tu pregunta principal)
GET /api/analisis/tipos-mascota

// 3. Día con más atención (tu pregunta principal)
GET /api/analisis/dias-atencion

// 4. Horas pico
GET /api/analisis/horas-pico

// 5. Servicios más usados
GET /api/analisis/servicios

// 6. Chatbot
POST /api/chat

// 7. Predicción IA
POST /api/predicciones/tipo-mascota
```

---

## 💡 Tip Final

**Usa la documentación interactiva:**
`http://localhost:8000/docs`

Ahí puedes:
- Ver todos los endpoints
- Probar cada uno directamente
- Ver ejemplos de request/response
- Copiar el código para tu frontend

---

**¡API lista para tu frontend! 🚀**

