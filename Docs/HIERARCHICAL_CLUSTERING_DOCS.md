#  HIERARCHICAL CLUSTERING - Análisis con IA

##  ¿Qué es Hierarchical Clustering?

**Hierarchical Clustering (Agrupamiento Jerárquico)** es un algoritmo de Machine Learning que identifica **grupos naturales** en tus datos sin necesidad de etiquetas previas.

###  Ventajas:
-  Descubre patrones ocultos en tus datos
-  Segmenta clientes automáticamente
-  Identifica grupos de mascotas similares
-  Agrupa servicios por patrones de uso
-  No requiere definir grupos de antemano

---

##  ¿Qué Agregamos al Sistema?

### 1.  Clustering de Mascotas
Agrupa mascotas por:
- Edad
- Tipo de servicios que reciben
- Precio de servicios

**Resultado:** 3 clusters que identifican perfiles de mascotas

### 2.  Clustering de Clientes
Segmenta clientes en:
- **VIP:** Alta frecuencia y gasto
- **Regular:** Visitas moderadas
- **Ocasional:** Visitas esporádicas
- **Nuevo:** Clientes exploratorios

### 3.  Clustering de Servicios
Agrupa servicios según:
- Frecuencia de uso
- Horario típico
- Tasa de asistencia

---

##  CÓMO USAR

### Opción 1: Desde el Chatbot

**Pregunta al bot:**
```
"clustering"
"segmentar clientes"
"agrupar mascotas"
```

**Respuesta esperada:**
```
 ANÁLISIS DE HIERARCHICAL CLUSTERING

 CLUSTERS DE MASCOTAS: 3 grupos
   Calidad (Silhouette): 0.652

   Cluster 0:
   • Total: 250 mascotas
   • Edad promedio: 3.5 años
   • Tipo predominante: Perro

 SEGMENTACIÓN DE CLIENTES: 4 segmentos
   Calidad: Buena

   VIP - Alta frecuencia:
   • Clientes: 35
   • Gasto promedio: $850.00
   • Citas promedio: 8.2
...
```

### Opción 2: Desde la API REST

#### Clustering de Mascotas
```javascript
fetch('http://localhost:8000/api/clustering/mascotas?n_clusters=3')
  .then(res => res.json())
  .then(data => console.log(data));
```

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
    },
    ...
  ],
  "metodo": "Agglomerative (Ward)",
  "metrica": "Euclidean"
}
```

#### Clustering de Clientes
```javascript
fetch('http://localhost:8000/api/clustering/clientes?n_clusters=4')
  .then(res => res.json())
  .then(data => {
    data.segmentos.forEach(seg => {
      console.log(`${seg.nombre}: ${seg.total_clientes} clientes`);
      console.log(`  Gasto promedio: $${seg.gasto_promedio}`);
    });
  });
```

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
    ...
  ],
  "calidad_clustering": "Buena"
}
```

#### Clustering de Servicios
```javascript
fetch('http://localhost:8000/api/clustering/servicios?n_clusters=3')
  .then(res => res.json())
  .then(data => console.log(data));
```

#### Análisis Completo
```javascript
fetch('http://localhost:8000/api/clustering/completo')
  .then(res => res.json())
  .then(data => {
    console.log('Mascotas:', data.clustering_mascotas);
    console.log('Clientes:', data.clustering_clientes);
    console.log('Servicios:', data.clustering_servicios);
  });
```

---

##  ENDPOINTS DISPONIBLES

| Endpoint | Descripción | Parámetros |
|----------|-------------|------------|
| `GET /api/clustering/mascotas` | Clusters de mascotas | `n_clusters=3` |
| `GET /api/clustering/clientes` | Segmentación de clientes | `n_clusters=4` |
| `GET /api/clustering/servicios` | Agrupación de servicios | `n_clusters=3` |
| `GET /api/clustering/completo` | Análisis completo | Ninguno |

---

##  CASOS DE USO

### 1. Segmentación de Clientes para Marketing

```javascript
const SegmentacionClientes = () => {
  const [segmentos, setSegmentos] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/clustering/clientes')
      .then(res => res.json())
      .then(data => setSegmentos(data.segmentos));
  }, []);

  return (
    <div>
      <h2> Segmentación de Clientes</h2>
      {segmentos.map(seg => (
        <div key={seg.segmento_id} className="segmento-card">
          <h3>{seg.nombre}</h3>
          <p>Clientes: {seg.total_clientes}</p>
          <p>Valor total: ${seg.valor_total_segmento.toFixed(2)}</p>
          <p>Gasto promedio: ${seg.gasto_promedio.toFixed(2)}</p>
          
          {seg.nombre.includes('VIP') && (
            <button>Ofrecer programa de lealtad</button>
          )}
        </div>
      ))}
    </div>
  );
};
```

### 2. Identificar Mascotas con Necesidades Similares

```javascript
fetch('http://localhost:8000/api/clustering/mascotas')
  .then(res => res.json())
  .then(data => {
    // Identificar cluster de mascotas jóvenes
    const clustersJovenes = data.clusters
      .filter(c => c.edad_promedio < 2);
    
    console.log('Mascotas jóvenes:', clustersJovenes);
    // Ofrecer paquetes de vacunación
  });
```

### 3. Optimizar Horarios de Servicios

```javascript
fetch('http://localhost:8000/api/clustering/servicios')
  .then(res => res.json())
  .then(data => {
    // Identificar servicios de alta demanda
    const grupoAlta = data.grupos
      .sort((a, b) => b.uso_promedio - a.uso_promedio)[0];
    
    console.log('Servicios de mayor demanda:', grupoAlta.servicios);
    // Asignar más recursos a esos horarios
  });
```

---

##  INTERPRETACIÓN DE RESULTADOS

### Silhouette Score (Calidad del Clustering)

| Rango | Interpretación |
|-------|----------------|
| 0.7 - 1.0 |  Excelente - Clusters bien definidos |
| 0.5 - 0.7 |  Bueno - Clusters claros |
| 0.3 - 0.5 |  Moderado - Algunos grupos se solapan |
| 0.0 - 0.3 |  Bajo - Clustering poco útil |

### Ejemplo de Interpretación

```json
{
  "silhouette_score": 0.652,
  "calidad_clustering": "Buena"
}
```

**Significa:** Los grupos están bien diferenciados y el clustering es útil para tomar decisiones.

---

##  VISUALIZACIÓN EN REACT

### Componente de Clustering

```jsx
import React, { useState, useEffect } from 'react';
import { Scatter } from 'react-chartjs-2';

const ClusteringVisual = () => {
  const [clustering, setClustering] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/clustering/clientes')
      .then(res => res.json())
      .then(data => setClustering(data));
  }, []);

  if (!clustering) return <div>Cargando...</div>;

  return (
    <div className="clustering-container">
      <h2> Segmentación de Clientes</h2>
      <p>Calidad: {clustering.calidad_clustering}</p>
      <p>Silhouette Score: {clustering.silhouette_score.toFixed(3)}</p>

      <div className="segmentos-grid">
        {clustering.segmentos.map(seg => (
          <div key={seg.segmento_id} className="segmento-card">
            <h3>{seg.nombre}</h3>
            <div className="stats">
              <div className="stat">
                <span className="label">Clientes</span>
                <span className="value">{seg.total_clientes}</span>
              </div>
              <div className="stat">
                <span className="label">Gasto promedio</span>
                <span className="value">${seg.gasto_promedio.toFixed(2)}</span>
              </div>
              <div className="stat">
                <span className="label">Citas promedio</span>
                <span className="value">{seg.citas_promedio.toFixed(1)}</span>
              </div>
            </div>
            <div className="valor-total">
              Valor total: ${seg.valor_total_segmento.toFixed(2)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ClusteringVisual;
```

### CSS para Visualización

```css
.clustering-container {
  padding: 20px;
}

.segmentos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.segmento-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  border-left: 4px solid #3b82f6;
}

.segmento-card h3 {
  margin: 0 0 16px 0;
  color: #1e293b;
}

.stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid #e2e8f0;
}

.stat .label {
  color: #64748b;
  font-size: 14px;
}

.stat .value {
  font-weight: bold;
  color: #1e293b;
}

.valor-total {
  margin-top: 16px;
  padding: 12px;
  background: #f1f5f9;
  border-radius: 8px;
  text-align: center;
  font-weight: bold;
  color: #0f172a;
}
```

---

##  PARÁMETROS CONFIGURABLES

### Número de Clusters

Puedes ajustar cuántos grupos quieres:

```javascript
// 3 clusters de mascotas
fetch('http://localhost:8000/api/clustering/mascotas?n_clusters=3')

// 5 segmentos de clientes
fetch('http://localhost:8000/api/clustering/clientes?n_clusters=5')

// 4 grupos de servicios
fetch('http://localhost:8000/api/clustering/servicios?n_clusters=4')
```

**Recomendación:**
- Mascotas: 3-4 clusters
- Clientes: 4-5 segmentos
- Servicios: 3-4 grupos

---

##  APLICACIONES PRÁCTICAS

### 1. Marketing Dirigido

```javascript
// Identificar clientes VIP
fetch('http://localhost:8000/api/clustering/clientes')
  .then(res => res.json())
  .then(data => {
    const vip = data.segmentos.find(s => s.nombre.includes('VIP'));
    console.log(`${vip.total_clientes} clientes VIP`);
    console.log(`Generan: $${vip.valor_total_segmento}`);
    
    // Estrategia: Programa de lealtad exclusivo
  });
```

### 2. Optimización de Recursos

```javascript
// Identificar servicios de alta demanda
fetch('http://localhost:8000/api/clustering/servicios')
  .then(res => res.json())
  .then(data => {
    const altaDemanda = data.grupos
      .sort((a, b) => b.uso_promedio - a.uso_promedio)[0];
    
    console.log('Servicios de alta demanda:', altaDemanda.servicios);
    console.log('Hora promedio:', altaDemanda.hora_promedio);
    
    // Estrategia: Asignar más veterinarios en esas horas
  });
```

### 3. Paquetes Personalizados

```javascript
// Crear paquetes según clusters de mascotas
fetch('http://localhost:8000/api/clustering/mascotas')
  .then(res => res.json())
  .then(data => {
    data.clusters.forEach(cluster => {
      if (cluster.edad_promedio < 2) {
        console.log('Paquete Cachorro:', cluster.total_mascotas);
      } else if (cluster.edad_promedio > 7) {
        console.log('Paquete Senior:', cluster.total_mascotas);
      }
    });
  });
```

---

##  EJEMPLO COMPLETO DE DASHBOARD

```jsx
import React, { useState, useEffect } from 'react';

const ClusteringDashboard = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/clustering/completo')
      .then(res => res.json())
      .then(result => setData(result));
  }, []);

  if (!data) return <div>Analizando con IA...</div>;

  return (
    <div className="clustering-dashboard">
      <h1> Análisis de Hierarchical Clustering</h1>
      
      {/* Resumen */}
      <div className="resumen">
        <div className="stat-card">
          <h3> Mascotas</h3>
          <p>{data.clustering_mascotas.n_clusters} Clusters</p>
          <small>Score: {data.clustering_mascotas.silhouette_score.toFixed(3)}</small>
        </div>
        <div className="stat-card">
          <h3> Clientes</h3>
          <p>{data.clustering_clientes.n_segmentos} Segmentos</p>
          <small>{data.clustering_clientes.calidad_clustering}</small>
        </div>
        <div className="stat-card">
          <h3> Servicios</h3>
          <p>{data.clustering_servicios.n_grupos} Grupos</p>
          <small>Score: {data.clustering_servicios.silhouette_score.toFixed(3)}</small>
        </div>
      </div>

      {/* Segmentos de Clientes */}
      <section className="segmentos-section">
        <h2>Segmentación de Clientes</h2>
        <div className="segmentos-grid">
          {data.clustering_clientes.segmentos.map(seg => (
            <div key={seg.segmento_id} className="segmento">
              <h3>{seg.nombre}</h3>
              <div className="metrics">
                <p><strong>{seg.total_clientes}</strong> clientes</p>
                <p>Gasto: <strong>${seg.gasto_promedio.toFixed(2)}</strong></p>
                <p>Citas: <strong>{seg.citas_promedio.toFixed(1)}</strong></p>
              </div>
              <div className="total-valor">
                Total: ${seg.valor_total_segmento.toFixed(2)}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default ClusteringDashboard;
```

---

##  ALGORITMO UTILIZADO

### Agglomerative Clustering

**Características:**
- **Método:** Bottom-up (de abajo hacia arriba)
- **Linkage:** Ward (minimiza varianza intra-cluster)
- **Métrica:** Euclidean distance
- **Dendrograma:** Disponible en linkage_matrix

**Proceso:**
1. Cada punto comienza como su propio cluster
2. Une los clusters más cercanos iterativamente
3. Continúa hasta tener n_clusters grupos
4. Calcula métricas de calidad (Silhouette)

---

##  MÉTRICAS DE CALIDAD

### Silhouette Score

Mide qué tan bien está cada punto en su cluster:
- **+1:** Perfectamente agrupado
- **0:** En el borde entre clusters
- **-1:** Probablemente en el cluster equivocado

**Cálculo:**
```
silhouette = (b - a) / max(a, b)
donde:
  a = distancia promedio al mismo cluster
  b = distancia promedio al cluster más cercano
```

---

##  INSTALACIÓN

### Dependencias Adicionales

```bash
pip install scipy scikit-learn
```

Estas ya deberían estar instaladas, pero si no:

```bash
pip install -r requirements.txt
```

---

##  CHECKLIST DE VERIFICACIÓN

- [ ] API reiniciada
- [ ] Endpoint `/api/clustering/completo` funciona
- [ ] Swagger UI muestra sección "Clustering"
- [ ] Chatbot responde a "clustering"
- [ ] Componente React renderiza correctamente

---

##  PRUEBA RÁPIDA

### 1. Desde el Navegador

```
http://localhost:8000/api/clustering/clientes
```

### 2. Desde Swagger UI

1. Abre: http://localhost:8000/docs
2. Busca sección: **"Clustering"**
3. Prueba: `GET /api/clustering/completo`

### 3. Desde el Chatbot

Pregunta:
```
"clustering"
"segmentar clientes"
"agrupar mascotas"
```

---

##  DECISIONES ESTRATÉGICAS CON CLUSTERING

### Clientes VIP
- Programa de lealtad exclusivo
- Descuentos especiales
- Atención prioritaria

### Clientes Ocasionales
- Campañas de reactivación
- Ofertas especiales
- Recordatorios de citas

### Mascotas Jóvenes
- Paquetes de vacunación
- Programas preventivos
- Descuentos en servicios iniciales

### Servicios de Alta Demanda
- Más veterinarios asignados
- Ampliar horarios
- Precios premium

---

##  TROUBLESHOOTING

### Error: "Datos insuficientes para clustering"

**Causa:** Menos datos que clusters solicitados  
**Solución:** Reduce `n_clusters` o verifica que haya suficientes registros

### Silhouette Score muy bajo (< 0.3)

**Causa:** Datos no tienen grupos naturales  
**Solución:** 
- Prueba con diferente número de clusters
- Verifica que haya variabilidad en los datos

### Error de importación scipy

```bash
pip install scipy
```

---

##  DOCUMENTACIÓN ADICIONAL

- **Swagger UI:** http://localhost:8000/docs (sección "Clustering")
- **Archivo:** `predictor.py` (líneas 426-713)
- **Archivo:** `api.py` (líneas 518-650)
- **Archivo:** `chatbot.py` (método `responder_clustering`)

---

##  RESUMEN

 **Hierarchical Clustering implementado**  
 **4 endpoints REST funcionando**  
 **Chatbot integrado**  
 **Análisis de mascotas, clientes y servicios**  
 **Métricas de calidad incluidas**  
 **Listo para usar en React**  

---

**¡Sistema de Clustering con IA listo para descubrir patrones en tus datos!** 

