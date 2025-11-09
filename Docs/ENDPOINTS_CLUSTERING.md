#  ENDPOINTS DE CLUSTERING - Para Consumir desde tu Frontend

##  ENDPOINTS DISPONIBLES

### 1. Clustering de Mascotas
```
GET http://localhost:8000/api/clustering/mascotas?n_clusters=3
```

**Parámetros:**
- `n_clusters` (opcional): Número de clusters (default: 3)

**Respuesta:**
```json
{
  "n_clusters": 3,
  "total_mascotas": 500,
  "silhouette_score": 0.652,
  "clusters": [
    {
      "cluster_id": 0,
      "total_mascotas": 250,
      "edad_promedio": 3.5,
      "precio_promedio": 65.50,
      "tipo_mascota_predominante": "Perro",
      "distribucion_tipos": {
        "Perro": 200,
        "Gato": 50
      }
    }
  ],
  "metodo": "Agglomerative (Ward)",
  "metrica": "Euclidean"
}
```

---

### 2. Clustering de Clientes (Segmentación)
```
GET http://localhost:8000/api/clustering/clientes?n_clusters=4
```

**Parámetros:**
- `n_clusters` (opcional): Número de segmentos (default: 4)

**Respuesta:**
```json
{
  "n_segmentos": 4,
  "total_clientes_analizados": 150,
  "silhouette_score": 0.587,
  "segmentos": [
    {
      "segmento_id": 0,
      "nombre": "VIP - Alta frecuencia",
      "total_clientes": 35,
      "citas_promedio": 8.2,
      "gasto_promedio": 850.00,
      "tasa_asistencia_promedio": 0.92,
      "valor_total_segmento": 29750.00
    },
    {
      "segmento_id": 1,
      "nombre": "Regular - Moderado",
      "total_clientes": 60,
      "citas_promedio": 4.5,
      "gasto_promedio": 320.00,
      "tasa_asistencia_promedio": 0.78,
      "valor_total_segmento": 19200.00
    }
  ],
  "metodo": "Agglomerative (Average)",
  "calidad_clustering": "Buena"
}
```

---

### 3. Clustering de Servicios
```
GET http://localhost:8000/api/clustering/servicios?n_clusters=3
```

**Parámetros:**
- `n_clusters` (opcional): Número de grupos (default: 3)

**Respuesta:**
```json
{
  "n_grupos": 3,
  "total_servicios": 15,
  "silhouette_score": 0.612,
  "grupos": [
    {
      "grupo_id": 0,
      "total_servicios": 5,
      "servicios": ["Consulta General", "Vacunación", "Desparasitación"],
      "uso_promedio": 120.5,
      "hora_promedio": 10.3,
      "tasa_asistencia_promedio": 0.85
    }
  ],
  "metodo": "Agglomerative (Complete)"
}
```

---

### 4. Clustering Completo (Todo en uno)
```
GET http://localhost:8000/api/clustering/completo
```

**Sin parámetros** - Retorna todo el análisis

**Respuesta:**
```json
{
  "timestamp": "2024-11-04T21:30:00",
  "total_registros": 2000,
  "clustering_mascotas": { ... },
  "clustering_clientes": { ... },
  "clustering_servicios": { ... }
}
```

---

##  EJEMPLOS DE CONSUMO

### JavaScript Puro (fetch)

```javascript
// Obtener segmentación de clientes
fetch('http://localhost:8000/api/clustering/clientes')
  .then(response => response.json())
  .then(data => {
    console.log('Segmentos:', data.segmentos);
    console.log('Calidad:', data.calidad_clustering);
  });
```

### Axios

```javascript
import axios from 'axios';

const response = await axios.get('http://localhost:8000/api/clustering/clientes');
const segmentos = response.data.segmentos;
```

### React Hook

```javascript
const [segmentos, setSegmentos] = useState([]);

useEffect(() => {
  fetch('http://localhost:8000/api/clustering/clientes')
    .then(res => res.json())
    .then(data => setSegmentos(data.segmentos));
}, []);
```

### Angular

```typescript
this.http.get('http://localhost:8000/api/clustering/clientes')
  .subscribe(data => {
    this.segmentos = data.segmentos;
  });
```

### Vue.js

```javascript
async mounted() {
  const response = await fetch('http://localhost:8000/api/clustering/clientes');
  this.segmentos = (await response.json()).segmentos;
}
```

---

##  ESTRUCTURA DE DATOS

### Segmentos de Clientes

```javascript
{
  segmento_id: number,           // ID único del segmento
  nombre: string,                // "VIP - Alta frecuencia"
  total_clientes: number,        // Cantidad de clientes
  citas_promedio: number,        // Promedio de citas por cliente
  gasto_promedio: number,        // Gasto promedio por cliente
  tasa_asistencia_promedio: number, // 0.0 a 1.0 (0% a 100%)
  valor_total_segmento: number   // Valor total que genera este segmento
}
```

### Clusters de Mascotas

```javascript
{
  cluster_id: number,              // ID del cluster
  total_mascotas: number,          // Cantidad de mascotas
  edad_promedio: number,           // Edad promedio en años
  precio_promedio: number,         // Precio promedio de servicios
  tipo_mascota_predominante: string, // "Perro", "Gato", etc.
  distribucion_tipos: object       // {"Perro": 200, "Gato": 50}
}
```

### Grupos de Servicios

```javascript
{
  grupo_id: number,                  // ID del grupo
  total_servicios: number,           // Cantidad de servicios
  servicios: array,                  // ["Servicio 1", "Servicio 2"]
  uso_promedio: number,              // Frecuencia de uso
  hora_promedio: number,             // Hora promedio (0-23)
  tasa_asistencia_promedio: number   // 0.0 a 1.0
}
```

---

##  PARÁMETROS OPCIONALES

Todos los endpoints aceptan el parámetro `n_clusters`:

```javascript
// 3 clusters (default)
fetch('http://localhost:8000/api/clustering/clientes')

// 5 clusters personalizados
fetch('http://localhost:8000/api/clustering/clientes?n_clusters=5')

// 2 clusters (mínimo)
fetch('http://localhost:8000/api/clustering/mascotas?n_clusters=2')
```

**Recomendación:**
- Clientes: 3-5 segmentos
- Mascotas: 3-4 clusters
- Servicios: 3-4 grupos

---

##  EJEMPLO COMPLETO

```javascript
async function obtenerClustering() {
  try {
    // Obtener segmentación de clientes
    const response = await fetch('http://localhost:8000/api/clustering/clientes');
    const data = await response.json();
    
    // Procesar segmentos
    data.segmentos.forEach(segmento => {
      console.log(`${segmento.nombre}: ${segmento.total_clientes} clientes`);
      console.log(`  Gasto promedio: $${segmento.gasto_promedio}`);
      console.log(`  Valor total: $${segmento.valor_total_segmento}`);
    });
    
    // Encontrar segmento VIP
    const vip = data.segmentos.find(s => s.nombre.includes('VIP'));
    console.log('Clientes VIP:', vip.total_clientes);
    
  } catch (error) {
    console.error('Error:', error);
  }
}
```

---

##  RESUMEN DE ENDPOINTS

| Endpoint | Método | Qué retorna |
|----------|--------|-------------|
| `/api/clustering/mascotas` | GET | Clusters de mascotas |
| `/api/clustering/clientes` | GET | Segmentos de clientes |
| `/api/clustering/servicios` | GET | Grupos de servicios |
| `/api/clustering/completo` | GET | **TODO el clustering** |

**Base URL:** `http://localhost:8000`

---

##  VERIFICACIÓN

Prueba en tu navegador:
```
http://localhost:8000/api/clustering/clientes
```

Deberías ver JSON con los segmentos.

O desde Swagger UI:
```
http://localhost:8000/docs
```

Busca la sección: **"Clustering"**

---

##  LISTO PARA TU FRONTEND

Los endpoints están listos para consumir desde:
-  React
-  Angular
-  Vue
-  JavaScript puro
-  Cualquier framework

**Solo haz fetch a los endpoints y procesa el JSON.** 

