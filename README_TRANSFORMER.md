# 🤖 Chatbot con Transformer - Pet Store

## 📋 Descripción

Sistema de chatbot inteligente que utiliza **arquitectura Transformer** (similar a GPT) para generar respuestas contextuales y naturales. El sistema combina:

- **Red Neuronal Transformer** con Multi-Head Attention
- **Generación autoregresiva** de texto
- **Enriquecimiento con datos** en tiempo real de la base de datos
- **Respuestas contextuales** basadas en el historial de conversación

## 🏗️ Arquitectura del Transformer

### Componentes Principales

```
Input → Embedding → Positional Encoding
                          ↓
        ┌─────────────────────────────┐
        │   Transformer Block 1       │
        │   - Multi-Head Attention    │
        │   - Feed-Forward Network    │
        │   - Layer Normalization     │
        └─────────────────────────────┘
                          ↓
        ┌─────────────────────────────┐
        │   Transformer Block N       │
        └─────────────────────────────┘
                          ↓
              Linear → Softmax → Output
```

### Parámetros del Modelo

- **d_model**: 256 (dimensión de embeddings)
- **num_heads**: 8 (cabezas de atención)
- **num_layers**: 4 (bloques transformer)
- **d_ff**: 1024 (dimensión feed-forward)
- **vocab_size**: ~5000 palabras
- **max_length**: 128 tokens

## 🚀 Instalación

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- **PyTorch** (framework de deep learning)
- **TensorFlow** (para LSTM legacy)
- **FastAPI** (API REST)
- Otras dependencias necesarias

### 2. Verificar Instalación

```bash
python -c "import torch; print(f'PyTorch {torch.__version__} instalado correctamente')"
```

## 📚 Entrenamiento del Modelo

### Opción 1: Entrenamiento Completo

```bash
python entrenar_transformer.py
```

Este script:
1. ✅ Genera datos de entrenamiento (pares pregunta-respuesta)
2. ✅ Construye el vocabulario
3. ✅ Entrena el modelo Transformer
4. ✅ Guarda el modelo en `models/transformer_chatbot.pth`

**Tiempo estimado**: 10-30 minutos (dependiendo de epochs y hardware)

### Opción 2: Usar Modelo Pre-entrenado

Si no deseas entrenar desde cero, el sistema funciona en **modo híbrido**:
- Detecta intenciones con patrones
- Enriquece respuestas con datos reales
- Genera respuestas contextuales

## 🎯 Uso del Chatbot

### Desde la API REST

```bash
# Iniciar servidor
python api.py
```

Luego desde tu frontend o herramienta (Postman, curl, etc.):

```javascript
// Ejemplo con JavaScript/Fetch
const response = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        mensaje: "¿Cuál es el tipo de mascota más común?",
        usuario_id: "user123"
    })
});

const data = await response.json();
console.log(data.respuesta);
console.log(`Modelo usado: ${data.modelo}`);
console.log(`Confianza: ${data.confianza * 100}%`);
```

```bash
# Ejemplo con curl
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"mensaje": "Muéstrame las estadísticas"}'
```

### Alternar entre Modelos

Puedes elegir entre el **Transformer** (nuevo) o **LSTM** (clásico):

```javascript
// Usar Transformer (por defecto)
fetch('http://localhost:8000/api/chat?use_transformer=true', {...})

// Usar LSTM clásico
fetch('http://localhost:8000/api/chat?use_transformer=false', {...})
```

### Desde Python Directamente

```python
from transformer_chatbot import PetStoreBotTransformer

bot = PetStoreBotTransformer()

resultado = bot.procesar_mensaje("Hola, ¿cómo estás?")
print(resultado['respuesta'])
print(f"Confianza: {resultado['confianza']:.0%}")
print(f"Modelo: {resultado['modelo']}")
```

## 💬 Capacidades del Chatbot

### Consultas Soportadas

#### 📊 Estadísticas y Métricas
- "Muéstrame las estadísticas"
- "¿Cuántas mascotas hay registradas?"
- "Dame un reporte del negocio"
- "Métricas actuales"

#### 📅 Citas y Agenda
- "¿Cuántas citas hay hoy?"
- "Muéstrame la agenda"
- "Próximas citas programadas"

#### 💰 Ventas e Ingresos
- "¿Cuánto vendimos hoy?"
- "Ventas del mes"
- "Reporte de ingresos"
- "Comparativa con mes anterior"

#### 🐾 Información de Mascotas
- "¿Cuál es el tipo de mascota más común?"
- "Tipos de mascotas registradas"
- "Búsqueda de mascota por nombre"

#### 📦 Inventario y Productos
- "¿Cuántos productos tenemos?"
- "Productos próximos a vencer"
- "Alertas de bajo stock"
- "Inventario actual"

#### 🔮 Predicciones con IA
- "Predice el tipo de mascota"
- "Análisis predictivo"

#### 🔬 Clustering y Segmentación
- "Análisis de clustering"
- "Segmentación de clientes"
- "Agrupa mascotas por características"

## 🎨 Respuesta del API

### Estructura de Respuesta

```json
{
  "respuesta": "📊 **Estadísticas del Sistema:**\n\n🐾 Mascotas registradas: 150...",
  "intencion": "transformer_generation",
  "confianza": 0.85,
  "timestamp": "2024-11-06T10:30:00",
  "modelo": "Transformer"
}
```

### Campos

- **respuesta**: Texto generado por el bot (puede incluir Markdown)
- **intencion**: Tipo de intención detectada
- **confianza**: Nivel de confianza (0.0 - 1.0)
- **timestamp**: Momento de la respuesta
- **modelo**: Modelo usado ("Transformer" o "Híbrido")

## ⚙️ Configuración

### Archivo: `config_transformer.py`

Puedes modificar:

```python
TRANSFORMER_CONFIG = {
    'd_model': 256,          # Dimensión del modelo
    'num_heads': 8,          # Cabezas de atención
    'num_layers': 4,         # Bloques transformer
    'temperature': 0.8,      # Creatividad (0.1-1.5)
    'top_k': 50,             # Top-K sampling
    'max_generate_length': 100,  # Longitud máxima
}
```

### Ajustar Temperatura

- **temperature = 0.1**: Respuestas más deterministas y consistentes
- **temperature = 0.8**: Balance (recomendado)
- **temperature = 1.5**: Respuestas más creativas y variadas

## 🧪 Testing

### Probar el Modelo

```bash
python transformer_chatbot.py
```

Esto ejecutará ejemplos de prueba automáticamente.

### Endpoints de Prueba

```bash
# Health check
curl http://localhost:8000/api/health

# Comandos disponibles
curl http://localhost:8000/api/chat/comandos

# Estado del modelo
curl http://localhost:8000/api/predicciones/estado
```

## 📈 Performance

### Métricas Esperadas

| Métrica | Valor |
|---------|-------|
| Tiempo de respuesta | < 1s |
| Confianza promedio | 75-90% |
| Vocabulario | ~5000 palabras |
| Parámetros del modelo | ~2M |

### Optimizaciones

- ✅ **Caché de respuestas** frecuentes
- ✅ **Batch processing** para múltiples consultas
- ✅ **GPU support** (si disponible)
- ✅ **Modo híbrido** como fallback

## 🔧 Troubleshooting

### Problema: Modelo no encontrado

**Solución**: Entrena el modelo primero
```bash
python entrenar_transformer.py
```

### Problema: Out of Memory (OOM)

**Solución**: Reduce el batch_size en `config_transformer.py`
```python
'batch_size': 16  # En lugar de 32
```

### Problema: Respuestas repetitivas

**Solución**: Aumenta la temperature
```python
'temperature': 1.0  # En lugar de 0.8
```

### Problema: Respuestas inconsistentes

**Solución**: Reduce la temperature
```python
'temperature': 0.5  # En lugar de 0.8
```

## 📊 Comparación: Transformer vs LSTM

| Característica | Transformer | LSTM |
|----------------|-------------|------|
| Arquitectura | Multi-Head Attention | Recurrente |
| Paralelización | ✅ Excelente | ❌ Limitada |
| Contexto | ✅ Largo alcance | ⚠️ Corto |
| Respuestas | ✅ Más naturales | ⚠️ Predefinidas |
| Entrenamiento | ⚠️ Más lento | ✅ Más rápido |
| Memoria | ⚠️ Mayor | ✅ Menor |

## 🎓 Conceptos Técnicos

### Multi-Head Attention

Permite al modelo enfocarse en diferentes partes de la entrada simultáneamente:

```python
Attention(Q, K, V) = softmax(QK^T / √d_k)V
```

### Positional Encoding

Agrega información de posición a los embeddings:

```python
PE(pos, 2i) = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

### Generación Autoregresiva

El modelo genera una palabra a la vez, usando las anteriores como contexto:

```
Input: "Hola" → Output: "¡Hola!"
Input: "¡Hola! Estoy" → Output: "aquí"
Input: "¡Hola! Estoy aquí" → Output: "para"
...
```

## 🔐 Seguridad

- ✅ Sanitización de entradas
- ✅ Validación de longitud
- ✅ Rate limiting (FastAPI)
- ✅ CORS configurado

## 📝 Logs

Los logs se guardan en:
- `logs/transformer_chatbot.log`

Ver logs en tiempo real:
```bash
tail -f logs/transformer_chatbot.log
```

## 🚀 Producción

### Consideraciones

1. **Usar GPU**: Mejora el rendimiento 10-50x
2. **Caché Redis**: Para respuestas frecuentes
3. **Load Balancer**: Para múltiples instancias
4. **Monitoreo**: Prometheus + Grafana

### Deploy con Docker

```dockerfile
FROM python:3.10

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📚 Referencias

- [Attention Is All You Need (Paper original)](https://arxiv.org/abs/1706.03762)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contribuciones

Para mejorar el modelo:

1. Agrega más datos de entrenamiento en `entrenar_transformer.py`
2. Ajusta hiperparámetros en `config_transformer.py`
3. Experimenta con diferentes arquitecturas

## 📄 Licencia

Este proyecto es para fines educativos.

## 👥 Soporte

Si tienes dudas:
1. Revisa la documentación técnica en `/Docs`
2. Consulta los ejemplos en el código
3. Revisa los logs para debugging

---

**Hecho con ❤️ y 🤖 Transformers**

