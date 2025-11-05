# 📊 MÉTRICAS DE NEGOCIO - Documentación

## 🎯 Nuevas Funcionalidades Incorporadas

El sistema ahora incluye métricas de negocio completas para análisis de ventas, inventario y operaciones diarias. La IA puede analizar estos datos y responder preguntas sobre el estado del negocio.

---

## 🚀 Configuración Inicial

### 1. Crear Tablas en la Base de Datos

Si tu base de datos aún no tiene las tablas de productos y ventas, ejecuta:

```bash
psql -h <host> -U <usuario> -d <database> -f crear_tablas_productos_ventas.sql
```

O desde tu cliente PostgreSQL favorito, ejecuta el contenido de `crear_tablas_productos_ventas.sql`.

### 2. Verificar la Instalación

```bash
python api.py
```

Abre: `http://localhost:8000/docs`

Busca la sección **"Métricas de Negocio"** en la documentación Swagger.

---

## 📡 Endpoints de la API

### 1. 📅 Citas de Hoy

**Endpoint:** `GET /api/metricas/citas-hoy`

Obtiene todas las citas programadas para el día actual.

**Respuesta:**
```json
{
  "citas": [
    {
      "appointment_id": 123,
      "fecha_hora": "2024-11-04 10:00:00",
      "hora": 10,
      "mascota": "Max",
      "tipo_mascota": "Perro",
      "cliente": "Juan Pérez",
      "telefono": "555-1234",
      "servicio": "Consulta General",
      "precio": 50.00,
      "estado": "PROGRAMADA",
      "veterinario": "Dr. García"
    }
  ],
  "total_citas": 8,
  "fecha": "2024-11-04"
}
```

**Uso en React:**
```javascript
const response = await fetch('http://localhost:8000/api/metricas/citas-hoy');
const data = await response.json();
console.log(`Citas hoy: ${data.total_citas}`);
```

---

### 2. 📦 Cantidad de Productos

**Endpoint:** `GET /api/metricas/cantidad-productos`

Obtiene el total de productos únicos en inventario.

**Respuesta:**
```json
{
  "total_productos": 150,
  "mensaje": "Total de productos en inventario: 150"
}
```

---

### 3. 💰 Ventas del Día

**Endpoint:** `GET /api/metricas/ventas-dia`

Obtiene las ventas del día actual.

**Respuesta:**
```json
{
  "fecha": "2024-11-04",
  "total_ventas": 1250.50,
  "total_transacciones": 15,
  "total_items_vendidos": 45,
  "cantidad_productos": 45,
  "ticket_promedio": 83.37
}
```

**Ejemplo de Dashboard:**
```javascript
const VentasDia = () => {
  const [ventas, setVentas] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/metricas/ventas-dia')
      .then(res => res.json())
      .then(data => setVentas(data));
  }, []);

  if (!ventas) return <div>Cargando...</div>;

  return (
    <div className="ventas-card">
      <h3>💰 Ventas del Día</h3>
      <p className="total">${ventas.total_ventas.toFixed(2)}</p>
      <div className="stats">
        <span>Transacciones: {ventas.total_transacciones}</span>
        <span>Ticket promedio: ${ventas.ticket_promedio.toFixed(2)}</span>
      </div>
    </div>
  );
};
```

---

### 4. 📅 Ventas del Mes

**Endpoint:** `GET /api/metricas/ventas-mes`

Obtiene las ventas del mes actual.

**Respuesta:**
```json
{
  "mes": "November 2024",
  "total_ventas": 35420.80,
  "total_transacciones": 280,
  "total_items_vendidos": 850,
  "cantidad_productos": 850,
  "ticket_promedio": 126.50,
  "clientes_unicos": 120
}
```

---

### 5. ⚠️ Productos Próximos a Vencer

**Endpoint:** `GET /api/metricas/productos-proximos-vencer?dias=30`

Obtiene productos que vencen en los próximos N días.

**Parámetros:**
- `dias` (opcional): Días de anticipación (default: 30)

**Respuesta:**
```json
{
  "productos": [
    {
      "producto_id": 15,
      "producto": "Alimento Premium Perro 15kg",
      "categoria": "Alimento",
      "fecha_vencimiento": "2024-11-20",
      "stock_actual": 25,
      "precio_venta": 65.00,
      "dias_hasta_vencer": 16,
      "valor_inventario": 1625.00
    }
  ],
  "total_productos": 5,
  "valor_total_inventario": 4850.00,
  "dias_anticipacion": 30
}
```

**Alerta en Dashboard:**
```javascript
const AlertaVencimiento = () => {
  const [productos, setProductos] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/metricas/productos-proximos-vencer?dias=30')
      .then(res => res.json())
      .then(data => setProductos(data.productos));
  }, []);

  const criticos = productos.filter(p => p.dias_hasta_vencer <= 7);

  return (
    <div className="alerta-card">
      <h3>⚠️ Productos por Vencer</h3>
      {criticos.length > 0 && (
        <div className="alert alert-danger">
          <strong>🔴 CRÍTICO:</strong> {criticos.length} productos vencen en 7 días
        </div>
      )}
      <ul>
        {productos.map(p => (
          <li key={p.producto_id}>
            {p.producto} - {p.dias_hasta_vencer} días
          </li>
        ))}
      </ul>
    </div>
  );
};
```

---

### 6. 🚨 Alerta de Bajo Inventario

**Endpoint:** `GET /api/metricas/alerta-bajo-inventario`

Obtiene productos con stock por debajo del mínimo.

**Respuesta:**
```json
{
  "productos": [
    {
      "producto_id": 23,
      "producto": "Collar Antipulgas Grande",
      "categoria": "Medicamentos",
      "stock_actual": 3,
      "stock_minimo": 10,
      "stock_maximo": 50,
      "unidades_faltantes": 7,
      "porcentaje_stock": 30.00,
      "precio_compra": 12.00,
      "costo_reposicion": 84.00,
      "proveedor": "VetMed Inc"
    }
  ],
  "total_alertas": 8,
  "costo_total_reposicion": 1250.00
}
```

---

### 7. 📊 Comparativa de Ventas Mensual

**Endpoint:** `GET /api/metricas/comparativa-ventas`

Compara las ventas del mes actual vs mes anterior.

**Respuesta:**
```json
{
  "ventas_mes_actual": 35420.80,
  "ventas_mes_anterior": 32100.50,
  "transacciones_mes_actual": 280,
  "transacciones_mes_anterior": 265,
  "diferencia_ventas": 3320.30,
  "porcentaje_cambio": 10.35,
  "tendencia": "crecimiento",
  "icono_tendencia": "📈",
  "mensaje": "Las ventas aumentaron +10.35% respecto al mes anterior"
}
```

**Gráfico de Tendencia:**
```javascript
import { Line } from 'react-chartjs-2';

const ComparativaVentas = () => {
  const [comparativa, setComparativa] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/metricas/comparativa-ventas')
      .then(res => res.json())
      .then(data => setComparativa(data));
  }, []);

  if (!comparativa) return <div>Cargando...</div>;

  const data = {
    labels: ['Mes Anterior', 'Mes Actual'],
    datasets: [{
      label: 'Ventas',
      data: [
        comparativa.ventas_mes_anterior,
        comparativa.ventas_mes_actual
      ],
      borderColor: comparativa.tendencia === 'crecimiento' ? 'green' : 'red',
      fill: false
    }]
  };

  return (
    <div className="comparativa-card">
      <h3>{comparativa.icono_tendencia} Comparativa Mensual</h3>
      <Line data={data} />
      <p>{comparativa.mensaje}</p>
      <div className="stats">
        <span className={comparativa.porcentaje_cambio > 0 ? 'positive' : 'negative'}>
          {comparativa.porcentaje_cambio > 0 ? '+' : ''}
          {comparativa.porcentaje_cambio.toFixed(2)}%
        </span>
      </div>
    </div>
  );
};
```

---

### 8. 🎯 Dashboard Completo

**Endpoint:** `GET /api/metricas/dashboard`

Obtiene todas las métricas en una sola llamada (optimizado).

**Respuesta:**
```json
{
  "citas_hoy": {
    "total": 8,
    "proxima_cita": {...}
  },
  "productos": {
    "total": 150
  },
  "ventas_dia": {
    "total_ventas": 1250.50,
    ...
  },
  "ventas_mes": {
    "total_ventas": 35420.80,
    ...
  },
  "productos_proximos_vencer": {
    "total": 5,
    "criticos": 2
  },
  "bajo_inventario": {
    "total_alertas": 8
  },
  "comparativa_ventas": {
    "porcentaje_cambio": 10.35,
    "tendencia": "crecimiento"
  },
  "timestamp": "2024-11-04T10:30:00"
}
```

**Dashboard React Completo:**
```javascript
const Dashboard = () => {
  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      const response = await fetch('http://localhost:8000/api/metricas/dashboard');
      const data = await response.json();
      setDashboard(data);
    };
    
    fetchDashboard();
    
    // Actualizar cada 5 minutos
    const interval = setInterval(fetchDashboard, 300000);
    return () => clearInterval(interval);
  }, []);

  if (!dashboard) return <div>Cargando dashboard...</div>;

  return (
    <div className="dashboard">
      <h1>📊 Dashboard Pet Store</h1>
      
      <div className="metrics-grid">
        <MetricCard
          icon="📅"
          title="Citas Hoy"
          value={dashboard.citas_hoy.total}
        />
        <MetricCard
          icon="📦"
          title="Productos"
          value={dashboard.productos.total}
        />
        <MetricCard
          icon="💰"
          title="Ventas del Día"
          value={`$${dashboard.ventas_dia.total_ventas.toFixed(2)}`}
        />
        <MetricCard
          icon="📈"
          title="Ventas del Mes"
          value={`$${dashboard.ventas_mes.total_ventas.toFixed(2)}`}
        />
      </div>
      
      <div className="alerts-section">
        {dashboard.productos_proximos_vencer.criticos > 0 && (
          <Alert type="danger">
            🔴 {dashboard.productos_proximos_vencer.criticos} productos críticos por vencer
          </Alert>
        )}
        
        {dashboard.bajo_inventario.total_alertas > 0 && (
          <Alert type="warning">
            🚨 {dashboard.bajo_inventario.total_alertas} productos con bajo inventario
          </Alert>
        )}
      </div>
      
      <div className="tendencia">
        <h3>Tendencia de Ventas</h3>
        <p>
          {dashboard.comparativa_ventas.tendencia === 'crecimiento' ? '📈' : '📉'}
          {' '}
          {dashboard.comparativa_ventas.porcentaje_cambio > 0 ? '+' : ''}
          {dashboard.comparativa_ventas.porcentaje_cambio.toFixed(2)}%
        </p>
      </div>
    </div>
  );
};
```

---

## 🤖 Interacción con el Chatbot

El chatbot ahora puede responder preguntas sobre estas métricas:

### Ejemplos de Preguntas:

**Citas:**
- "¿Cuántas citas hay hoy?"
- "Muéstrame las citas de hoy"
- "¿Qué citas tenemos?"

**Ventas:**
- "¿Cuánto hemos vendido?"
- "Muéstrame las ventas"
- "¿Cómo van las ventas del mes?"

**Inventario:**
- "¿Cuántos productos tenemos?"
- "Muéstrame el inventario"
- "¿Hay productos en stock?"

**Alertas:**
- "¿Hay productos por vencer?"
- "Muéstrame las alertas"
- "¿Tenemos bajo inventario?"

### Ejemplo de Uso del Chatbot:

```javascript
const Chat = () => {
  const [mensaje, setMensaje] = useState('');
  const [respuesta, setRespuesta] = useState('');

  const enviar = async () => {
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        mensaje: mensaje,
        usuario_id: 'user123'
      })
    });
    
    const data = await response.json();
    setRespuesta(data.respuesta);
  };

  return (
    <div className="chat">
      <div className="mensajes">
        {respuesta && <div className="bot-message">{respuesta}</div>}
      </div>
      <input
        value={mensaje}
        onChange={(e) => setMensaje(e.target.value)}
        placeholder="Pregunta al bot..."
        onKeyPress={(e) => e.key === 'Enter' && enviar()}
      />
      <button onClick={enviar}>Enviar</button>
    </div>
  );
};
```

---

## 📈 Casos de Uso

### 1. Dashboard de Gerencia

Monitorea las métricas clave en tiempo real:
- Ventas diarias y mensuales
- Tendencia de ventas
- Citas programadas
- Alertas de inventario

### 2. Gestión de Inventario

Previene pérdidas por:
- Productos vencidos
- Stock agotado
- Sobre-stock

### 3. Análisis Predictivo

La IA puede:
- Identificar tendencias de ventas
- Sugerir reposiciones de productos
- Alertar sobre productos críticos

### 4. Optimización de Operaciones

- Ver citas del día para planificar recursos
- Analizar patrones de ventas
- Comparar rendimiento mensual

---

## 🎨 Componentes UI Sugeridos

### Card de Métricas
```jsx
const MetricCard = ({ icon, title, value, trend }) => (
  <div className="metric-card">
    <div className="icon">{icon}</div>
    <h4>{title}</h4>
    <p className="value">{value}</p>
    {trend && <span className={`trend ${trend.direction}`}>{trend.text}</span>}
  </div>
);
```

### Alerta
```jsx
const Alert = ({ type, children }) => (
  <div className={`alert alert-${type}`}>
    {children}
  </div>
);
```

### CSS Sugerido
```css
.dashboard {
  padding: 20px;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.metric-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  text-align: center;
}

.metric-card .icon {
  font-size: 3em;
  margin-bottom: 10px;
}

.metric-card .value {
  font-size: 2em;
  font-weight: bold;
  color: #333;
}

.alert {
  padding: 15px;
  border-radius: 8px;
  margin: 10px 0;
}

.alert-danger {
  background: #fee;
  border-left: 4px solid #f00;
  color: #900;
}

.alert-warning {
  background: #ffe;
  border-left: 4px solid #fa0;
  color: #960;
}

.trend.positive {
  color: green;
}

.trend.negative {
  color: red;
}
```

---

## 🔧 Configuración Avanzada

### Actualización Automática del Dashboard

```javascript
// Hook personalizado para auto-actualización
const useDashboard = (refreshInterval = 300000) => {
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:8000/api/metricas/dashboard');
        if (!response.ok) throw new Error('Error al cargar dashboard');
        const data = await response.json();
        setDashboard(data);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboard();
    const interval = setInterval(fetchDashboard, refreshInterval);
    
    return () => clearInterval(interval);
  }, [refreshInterval]);

  return { dashboard, loading, error };
};

// Uso
const Dashboard = () => {
  const { dashboard, loading, error } = useDashboard(60000); // Actualizar cada minuto

  if (loading) return <Spinner />;
  if (error) return <Error message={error} />;

  return <DashboardContent data={dashboard} />;
};
```

---

## ✅ Checklist de Implementación

- [ ] Ejecutar script SQL para crear tablas
- [ ] Verificar que la API esté corriendo
- [ ] Probar endpoints en Swagger UI
- [ ] Insertar datos de ejemplo
- [ ] Crear componentes del dashboard
- [ ] Implementar actualización automática
- [ ] Configurar alertas visuales
- [ ] Probar interacción con chatbot
- [ ] Estilizar componentes
- [ ] Implementar manejo de errores

---

## 🆘 Troubleshooting

### Error: "Tabla 'producto' no existe"

**Solución:** Ejecuta el script SQL `crear_tablas_productos_ventas.sql`

### Las métricas muestran ceros

**Solución:** Inserta datos de ejemplo o registra ventas reales.

### El chatbot no responde a preguntas de ventas

**Solución:** Verifica que el chatbot tenga acceso a los nuevos métodos. Reinicia la API.

### Error de conexión a la API

**Solución:** 
1. Verifica que `python api.py` esté corriendo
2. Confirma que el puerto 8000 esté disponible
3. Revisa configuración de CORS si usas otro puerto en React

---

## 📚 Recursos Adicionales

- **Documentación Swagger:** `http://localhost:8000/docs`
- **Script SQL:** `crear_tablas_productos_ventas.sql`
- **Archivo de API:** `api.py` (líneas 502-782)
- **Chatbot:** `chatbot.py` (líneas 379-502)
- **Base de Datos:** `database.py` (líneas 377-711)

---

## 🎯 Próximos Pasos

1. **Implementar el dashboard en React**
2. **Agregar gráficos con Chart.js o Recharts**
3. **Configurar notificaciones push para alertas críticas**
4. **Exportar reportes en PDF**
5. **Agregar filtros por fecha**
6. **Implementar sistema de objetivos de ventas**

---

**¡Sistema de métricas de negocio listo para usar! 🚀**

