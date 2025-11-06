# 🚀 GUÍA RÁPIDA: Chatbot con Transformer

## ⚡ Inicio Rápido (3 pasos)

### 1. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 2. (Opcional) Entrenar el Transformer

```bash
python entrenar_transformer.py
```

**Nota**: Si no entrenas el modelo, el sistema usará modo híbrido automáticamente.

### 3. Iniciar la API

```bash
python api.py
```

La API estará disponible en: `http://localhost:8000`

## 📝 Usar el Chatbot

### Desde el Navegador

Abre: `http://localhost:8000/docs`

Prueba el endpoint `/api/chat`:

```json
{
  "mensaje": "¿Cuántas citas hay hoy?",
  "usuario_id": "user123"
}
```

### Desde JavaScript/Frontend

```javascript
const response = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        mensaje: "Muéstrame las estadísticas",
        usuario_id: "user123"
    })
});

const data = await response.json();
console.log(data.respuesta);
```

### Desde Terminal

```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"mensaje": "Hola"}'
```

## 🎮 Demos Disponibles

```bash
# Demo interactivo
python demo_transformer.py

# Prueba del transformer
python transformer_chatbot.py
```

## 🔧 Configuración Rápida

Edita `config_transformer.py` para cambiar:

- **temperature**: Creatividad (0.1-1.5)
- **num_layers**: Profundidad del modelo
- **d_model**: Tamaño de embeddings

## 💬 Ejemplos de Preguntas

Prueba estas consultas:

- "Muéstrame las estadísticas"
- "¿Cuántas citas hay hoy?"
- "Dame el reporte de ventas"
- "¿Cuál es el tipo de mascota más común?"
- "¿Hay productos próximos a vencer?"
- "Análisis de clustering"

## 📊 Respuesta del API

```json
{
  "respuesta": "📊 **Estadísticas del Sistema:**...",
  "intencion": "transformer_generation",
  "confianza": 0.85,
  "timestamp": "2024-11-06T10:30:00",
  "modelo": "Transformer"
}
```

## 🐛 Troubleshooting

### Problema: Módulo no encontrado

```bash
pip install torch
```

### Problema: Puerto ocupado

Cambia el puerto en `api.py`:

```python
uvicorn.run("api:app", port=8001)
```

### Problema: Modelo no entrenado

El sistema funciona sin entrenar el modelo (modo híbrido). Para mejor rendimiento, ejecuta:

```bash
python entrenar_transformer.py
```

## 📖 Más Información

- **Documentación completa**: `README_TRANSFORMER.md`
- **Documentación técnica**: `Docs/DOCUMENTACION_TECNICA.md`
- **Ejemplos de código**: `ejemplo_uso_frontend.js`

## 🎯 Arquitectura

```
Usuario → Frontend → API (FastAPI) → Transformer → Base de Datos
                                          ↓
                                    Respuesta Generada
```

## ✨ Características

- ✅ Transformer con Multi-Head Attention
- ✅ Generación autoregresiva de texto
- ✅ Enriquecimiento con datos en tiempo real
- ✅ Modo híbrido sin entrenamiento
- ✅ API REST con FastAPI
- ✅ Documentación interactiva (Swagger)

## 🔗 Enlaces Útiles

- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/api/health

---

**¡Listo para usar! 🚀**

