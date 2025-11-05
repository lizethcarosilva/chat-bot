# 🔌 API REST - Documentación de Endpoints

## 📡 Información General

**Base URL:** `http://localhost:8000`  
**Documentación Interactiva:** `http://localhost:8000/docs`  
**Formato:** JSON  
**CORS:** Habilitado para todos los orígenes

---

## 🚀 Inicio Rápido

### 1. Instalar Dependencia Adicional
```bash
pip install fastapi uvicorn
```

### 2. Iniciar el Servidor API
```bash
python api.py
```

**Salida esperada:**
```
🚀 INICIANDO API REST - PET STORE CHATBOT
✅ API lista en: http://localhost:8000
📝 Documentación: http://localhost:8000/docs
```

### 3. Probar en React
```bash
npm install axios
```

---

## 📋 Índice de Endpoints

### **General**
- `GET /` - Información de la API
- `GET /api/health` - Estado del sistema

### **Chatbot** 💬
- `POST /api/chat` - Enviar mensaje al chatbot
- `GET /api/chat/comandos` - Listar comandos disponibles

### **Estadísticas** 📊
- `GET /api/estadisticas` - Estadísticas generales

### **Análisis** 📈
- `GET /api/analisis/tipos-mascota` - Tipos de mascota más comunes
- `GET /api/analisis/dias-atencion` - Días con más atención
- `GET /api/analisis/horas-pico` - Horas pico
- `GET /api/analisis/servicios` - Servicios más utilizados

### **Predicciones IA** 🔮
- `POST /api/predicciones/tipo-mascota` - Predecir tipo de mascota
- `POST /api/predicciones/asistencia` - Predecir asistencia
- `GET /api/predicciones/tipo-mas-comun` - Análisis de tipo más común
- `GET /api/predicciones/dia-mas-atencion` - Análisis de día con más atención
- `GET /api/predicciones/estado` - Estado de los modelos

### **Consultas BD** 🔍
- `GET /api/mascotas/buscar/{nombre}` - Buscar mascota
- `GET /api/mascotas/{pet_id}/historial` - Historial médico
- `GET /api/mascotas/{pet_id}/citas` - Próximas citas
- `GET /api/mascotas/{pet_id}/vacunas` - Historial de vacunas
- `GET /api/clientes/buscar/{correo}` - Buscar cliente
- `GET /api/clientes/{client_id}/mascotas` - Mascotas de cliente
- `GET /api/servicios` - Servicios disponibles

### **Administración** ⚙️
- `POST /api/entrenar` - Entrenar modelos IA
- `GET /api/exportar/dataset` - Exportar dataset

---

## 📝 Documentación Detallada

## 1. CHATBOT

### `POST /api/chat`
Envía un mensaje al chatbot y recibe respuesta inteligente.

**Request:**
```json
{
  "mensaje": "¿Cuál es el tipo de mascota más común?",
  "usuario_id": "user123"
}
```

**Response:**
```json
{
  "respuesta": "🏆 El tipo más común es: Perro (45.5%)\n\n📊 Distribución:\n   Perro: 250 (45.5%)\n   Gato: 180 (32.7%)",
  "intencion": "tipo_mas_comun",
  "confianza": 0.9,
  "timestamp": "2024-11-03T10:30:00"
}
```

**Ejemplo React:**
```javascript
import axios from 'axios';

const ChatComponent = () => {
  const [mensaje, setMensaje] = useState('');
  const [respuesta, setRespuesta] = useState('');

  const enviarMensaje = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/chat', {
        mensaje: mensaje,
        usuario_id: 'user123'
      });
      
      setRespuesta(response.data.respuesta);
      console.log('Confianza:', response.data.confianza);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div>
      <input 
        value={mensaje} 
        onChange={(e) => setMensaje(e.target.value)}
        placeholder="Escribe tu pregunta..."
      />
      <button onClick={enviarMensaje}>Enviar</button>
      <div>{respuesta}</div>
    </div>
  );
};
```

---

### `GET /api/chat/comandos`
Obtiene lista de comandos disponibles del chatbot.

**Response:**
```json
{
  "comandos": [
    {
      "comando": "estadísticas",
      "descripcion": "Muestra estadísticas generales",
      "ejemplo": "Muéstrame las estadísticas"
    },
    {
      "comando": "tipo más común",
      "descripcion": "Muestra el tipo de mascota más común",
      "ejemplo": "¿Cuál es el tipo de mascota más común?"
    }
  ]
}
```

---

## 2. ESTADÍSTICAS

### `GET /api/estadisticas`
Obtiene estadísticas generales del sistema.

**Response:**
```json
{
  "total_mascotas": 250,
  "total_clientes": 150,
  "total_citas": 2000,
  "total_servicios": 15
}
```

**Ejemplo React:**
```javascript
import { useEffect, useState } from 'react';
import axios from 'axios';

const EstadisticasComponent = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      const response = await axios.get('http://localhost:8000/api/estadisticas');
      setStats(response.data);
    };
    
    fetchStats();
  }, []);

  if (!stats) return <div>Cargando...</div>;

  return (
    <div>
      <h2>Estadísticas Generales</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>🐾 Mascotas</h3>
          <p>{stats.total_mascotas}</p>
        </div>
        <div className="stat-card">
          <h3>👥 Clientes</h3>
          <p>{stats.total_clientes}</p>
        </div>
        <div className="stat-card">
          <h3>📅 Citas</h3>
          <p>{stats.total_citas}</p>
        </div>
        <div className="stat-card">
          <h3>🏥 Servicios</h3>
          <p>{stats.total_servicios}</p>
        </div>
      </div>
    </div>
  );
};
```

---

## 3. ANÁLISIS

### `GET /api/analisis/tipos-mascota`
Análisis de tipos de mascotas más comunes.

**Response:**
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

**Ejemplo React con Gráfico:**
```javascript
import { Bar } from 'react-chartjs-2';
import axios from 'axios';

const TiposMascotaChart = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get(
        'http://localhost:8000/api/analisis/tipos-mascota'
      );
      
      const chartData = {
        labels: response.data.estadisticas.map(item => item.tipo_mascota),
        datasets: [{
          label: 'Número de Mascotas',
          data: response.data.estadisticas.map(item => item.total_mascotas),
          backgroundColor: 'rgba(75, 192, 192, 0.6)'
        }]
      };
      
      setData(chartData);
    };
    
    fetchData();
  }, []);

  if (!data) return <div>Cargando gráfico...</div>;

  return (
    <div>
      <h2>🐾 Tipo de Mascota Más Común: {data.tipo_mas_comun}</h2>
      <Bar data={data} />
    </div>
  );
};
```

---

### `GET /api/analisis/dias-atencion`
Análisis de días con más atención.

**Response:**
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

### `GET /api/analisis/horas-pico`
Análisis de horas con más demanda.

**Response:**
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

### `GET /api/analisis/servicios`
Análisis de servicios más utilizados.

**Response:**
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

## 4. PREDICCIONES CON IA

### `POST /api/predicciones/tipo-mascota`
Predice el tipo de mascota más probable usando Red Neuronal.

**Request:**
```json
{
  "dia_semana": 5,
  "hora": 10,
  "mes": 11,
  "service_id": 1
}
```

**Response:**
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
    },
    {
      "tipo_mascota": "Ave",
      "probabilidad": 0.043
    }
  ],
  "tipo_mas_probable": "Perro",
  "confianza": 0.785
}
```

**Ejemplo React:**
```javascript
const PrediccionTipoMascota = () => {
  const [prediccion, setPrediccion] = useState(null);
  const [loading, setLoading] = useState(false);

  const predecir = async () => {
    setLoading(true);
    try {
      const response = await axios.post(
        'http://localhost:8000/api/predicciones/tipo-mascota',
        {
          dia_semana: 5,  // Viernes
          hora: 10,
          mes: 11,
          service_id: 1
        }
      );
      
      setPrediccion(response.data);
    } catch (error) {
      if (error.response?.status === 400) {
        alert('Los modelos no están entrenados. Entrena primero.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={predecir} disabled={loading}>
        {loading ? 'Prediciendo...' : 'Predecir Tipo de Mascota'}
      </button>
      
      {prediccion && (
        <div className="prediccion-result">
          <h3>🔮 Predicción: {prediccion.tipo_mas_probable}</h3>
          <p>Confianza: {(prediccion.confianza * 100).toFixed(1)}%</p>
          
          <h4>Top 3:</h4>
          <ul>
            {prediccion.predicciones.map((pred, idx) => (
              <li key={idx}>
                {pred.tipo_mascota}: {(pred.probabilidad * 100).toFixed(1)}%
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
```

---

### `POST /api/predicciones/asistencia`
Predice la probabilidad de que un cliente asista a una cita.

**Request:**
```json
{
  "dia_semana": 3,
  "hora": 14,
  "mes": 11,
  "service_id": 2,
  "edad_mascota": 5
}
```

**Response:**
```json
{
  "probabilidad_asistencia": 0.823,
  "asistira": true,
  "confianza": "Alta"
}
```

---

### `GET /api/predicciones/estado`
Verifica si los modelos están entrenados.

**Response:**
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

## 5. CONSULTAS A BASE DE DATOS

### `GET /api/mascotas/buscar/{nombre}`
Busca mascotas por nombre.

**Ejemplo:** `GET /api/mascotas/buscar/Max`

**Response:**
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

**Ejemplo React:**
```javascript
const BuscarMascota = () => {
  const [nombre, setNombre] = useState('');
  const [resultados, setResultados] = useState([]);

  const buscar = async () => {
    const response = await axios.get(
      `http://localhost:8000/api/mascotas/buscar/${nombre}`
    );
    setResultados(response.data.mascotas);
  };

  return (
    <div>
      <input 
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        placeholder="Nombre de la mascota"
      />
      <button onClick={buscar}>Buscar</button>
      
      <div className="resultados">
        {resultados.map(mascota => (
          <div key={mascota.pet_id} className="mascota-card">
            <h3>🐾 {mascota.nombre}</h3>
            <p>{mascota.tipo} - {mascota.raza}</p>
            <p>Edad: {mascota.edad} años</p>
            <p>Dueño: {mascota.propietario}</p>
          </div>
        ))}
      </div>
    </div>
  );
};
```

---

### `GET /api/mascotas/{pet_id}/historial`
Obtiene historial médico de una mascota.

**Ejemplo:** `GET /api/mascotas/45/historial`

**Response:**
```json
{
  "pet_id": 45,
  "historial": [
    {
      "fecha_atencion": "2024-10-15T10:30:00",
      "servicio": "Consulta General",
      "tipo_procedimiento": "Revisión",
      "diagnostico": "Mascota saludable",
      "tratamiento": "Control en 6 meses",
      "veterinario": "Dr. García"
    }
  ]
}
```

---

### `GET /api/servicios`
Lista todos los servicios disponibles.

**Response:**
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

## 6. ADMINISTRACIÓN

### `POST /api/entrenar`
Entrena los modelos de red neuronal en segundo plano.

**Response:**
```json
{
  "mensaje": "Entrenamiento iniciado en segundo plano",
  "tiempo_estimado": "5-10 minutos",
  "nota": "Verifica el estado con GET /api/predicciones/estado"
}
```

**Ejemplo React:**
```javascript
const EntrenarModelos = () => {
  const [entrenando, setEntrenando] = useState(false);

  const entrenar = async () => {
    if (!confirm('¿Entrenar modelos? Tardará 5-10 minutos')) return;
    
    setEntrenando(true);
    
    await axios.post('http://localhost:8000/api/entrenar');
    
    alert('Entrenamiento iniciado. Verifica el estado en unos minutos.');
    
    // Verificar estado cada 30 segundos
    const interval = setInterval(async () => {
      const response = await axios.get(
        'http://localhost:8000/api/predicciones/estado'
      );
      
      if (response.data.todos_listos) {
        clearInterval(interval);
        setEntrenando(false);
        alert('¡Entrenamiento completado!');
      }
    }, 30000);
  };

  return (
    <button onClick={entrenar} disabled={entrenando}>
      {entrenando ? 'Entrenando...' : 'Entrenar Modelos IA'}
    </button>
  );
};
```

---

## 📦 Componente React Completo

```javascript
// src/services/api.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const api = {
  // Chatbot
  enviarMensaje: (mensaje) => 
    axios.post(`${API_BASE_URL}/api/chat`, { mensaje }),
  
  // Estadísticas
  obtenerEstadisticas: () => 
    axios.get(`${API_BASE_URL}/api/estadisticas`),
  
  // Análisis
  obtenerTiposMascota: () => 
    axios.get(`${API_BASE_URL}/api/analisis/tipos-mascota`),
    
  obtenerDiasAtencion: () => 
    axios.get(`${API_BASE_URL}/api/analisis/dias-atencion`),
  
  // Predicciones
  predecirTipoMascota: (data) => 
    axios.post(`${API_BASE_URL}/api/predicciones/tipo-mascota`, data),
    
  predecirAsistencia: (data) => 
    axios.post(`${API_BASE_URL}/api/predicciones/asistencia`, data),
  
  // Consultas
  buscarMascota: (nombre) => 
    axios.get(`${API_BASE_URL}/api/mascotas/buscar/${nombre}`),
    
  obtenerServicios: () => 
    axios.get(`${API_BASE_URL}/api/servicios`),
};
```

```javascript
// src/App.js
import React from 'react';
import { api } from './services/api';

function App() {
  const [stats, setStats] = React.useState(null);

  React.useEffect(() => {
    api.obtenerEstadisticas()
      .then(response => setStats(response.data))
      .catch(error => console.error(error));
  }, []);

  return (
    <div className="App">
      <h1>🐾 Pet Store Dashboard</h1>
      
      {stats && (
        <div className="stats-grid">
          <StatCard icon="🐾" title="Mascotas" value={stats.total_mascotas} />
          <StatCard icon="👥" title="Clientes" value={stats.total_clientes} />
          <StatCard icon="📅" title="Citas" value={stats.total_citas} />
          <StatCard icon="🏥" title="Servicios" value={stats.total_servicios} />
        </div>
      )}
    </div>
  );
}

const StatCard = ({ icon, title, value }) => (
  <div className="stat-card">
    <div className="icon">{icon}</div>
    <h3>{title}</h3>
    <p className="value">{value}</p>
  </div>
);

export default App;
```

---

## 🔧 Configuración en React

### 1. Instalar Dependencias
```bash
npm install axios react-chartjs-2 chart.js
```

### 2. Configurar Proxy (opcional)
En `package.json`:
```json
{
  "proxy": "http://localhost:8000"
}
```

### 3. Crear Servicio API
Crea `src/services/api.js` con las funciones mostradas arriba.

---

## 🚨 Manejo de Errores

```javascript
const handleApiCall = async (apiFunction) => {
  try {
    const response = await apiFunction();
    return response.data;
  } catch (error) {
    if (error.response) {
      // El servidor respondió con un error
      console.error('Error del servidor:', error.response.data);
      alert(`Error: ${error.response.data.detail || 'Ocurrió un error'}`);
    } else if (error.request) {
      // La petición se hizo pero no hubo respuesta
      console.error('No hay respuesta del servidor');
      alert('No se puede conectar al servidor. ¿Está corriendo?');
    } else {
      // Error al configurar la petición
      console.error('Error:', error.message);
    }
    return null;
  }
};

// Uso:
const stats = await handleApiCall(() => api.obtenerEstadisticas());
if (stats) {
  setStats(stats);
}
```

---

## 📚 Recursos Adicionales

- **Documentación Swagger:** `http://localhost:8000/docs`
- **Documentación ReDoc:** `http://localhost:8000/redoc`
- **Estado de la API:** `GET /api/health`

---

## ✅ Checklist de Integración

- [ ] Instalar `fastapi` y `uvicorn`
- [ ] Ejecutar `python api.py`
- [ ] Verificar `http://localhost:8000/docs`
- [ ] Instalar `axios` en React
- [ ] Crear servicio API en React
- [ ] Probar endpoints básicos
- [ ] Entrenar modelos si es necesario
- [ ] Implementar manejo de errores
- [ ] Configurar CORS si es producción

---

**¡API lista para usar con tu frontend React! 🎉**

